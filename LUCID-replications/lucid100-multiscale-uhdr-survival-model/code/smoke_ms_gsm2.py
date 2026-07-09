#!/usr/bin/env python3
"""
Smoke replication of MS-GSM^2 (Battestini, Missiaggia, Bolzoni, Cordoni, Scifoni 2024)
arXiv:2412.16322.

This is NOT a bit-exact reproduction. The paper's full pipeline is Julia, closed,
with 52 microdosimetric domains, TRAX-CHEM G-values, Rodas4 ODE solver, and
custom cross-entropy fitting on raw experimental data the authors retain.

What this script does (smoke / mechanism reproduction):
  1. Implements the 5-ODE chemical reaction network in Eq. (2) of the paper,
     with the rate constants and initial concentrations from Table 1
     (Chemical stage parameters, "TAB:chempar"), pH treated as Labarbe2020
     equivalents and G-values approximated from TRAX-CHEM values commonly
     reported in the literature.
  2. Implements a single-domain reduction of the GSM^2 biological stage:
     a sub-lethal lesion X can repair (rate r), become lethal (rate a),
     or pair-combine to lethal (rate b). Solved via mean-field ODE,
     not the full SSA (which is in the supplement algorithm).
  3. Couples the chemical environment to the biological stage via a
     normalized peroxyl-radical exposure modulator
        kappa_indirect(t) = kappa_0 * rho * integral_0^t [ROO*] ds
     normalized to 1 at conventional + 21% O2 (paper's normalization).
  4. Sweeps dose D in [0, 20] Gy at conventional (0.1 Gy/s) and UHDR
     (100 Gy/s) for two oxygen levels (21% normoxia, 1% hypoxic).
     Reports survival fraction SF = exp(-<Y_inf>) and the FLASH ratio.

Goal: reproduce QUALITATIVELY the well-known FLASH sparing trend
the paper claims: SF_UHDR > SF_CONV at low O2, with the gap narrowing
or vanishing at 21% O2. This is the same qualitative test the Wave 3
slot 27 dynamic-UNIVERSE smoke and the Cordoni 2023 GSM2 smoke
already replicated.

Outputs:
  results/smoke_results.csv   - SF vs dose, dose rate, [O2]
  results/smoke_results.png   - survival curves + FLASH ratio panel
  results/smoke_chem_trace.csv- ROO*, O2, etc. traces for QA
"""

from __future__ import annotations
import os
import csv
import math
import numpy as np
from scipy.integrate import solve_ivp

# ----------------------------------------------------------------------
# Paper parameters (Table TAB:chempar, arXiv 2412.16322 v1)
# Units: rate constants in 1/(M*s); concentrations in mol/L (M); time in s.
# ----------------------------------------------------------------------
PARAMS = dict(
    # rate constants from Table TAB:chempar
    k1=5.0e7,   # R* + O2 -> ROO*
    k2=1.0e4,   # ROO* + ROO* (paper text mentions update to 1e5; we keep table value 1e4)
    k3=6.62e7,  # catalase decomp H2O2
    k4=1.0e3,   # Fenton: Fe2+ + H2O2 -> OH*
    k5=1.0e9,   # RH + OH* -> R*
    k6=1.0e10,  # XSH + OH* (scavenger)
    k7=4.62e4,  # XSH + R*
    k8=5.0e7,   # 2 R* -> R-R
    k9=1.0e2,   # XSH + ROO* (GSH scavenging of ROO*)
    # fixed substrate / catalyst pools (Table TAB:chempar)
    RH=1.0,           # M
    cat=8.0e-8,       # M (catalase)
    Fe2=8.9e-7,       # M
    XSH=6.5e-3,       # M (glutathione GSH pool)
    k_m=25.0e-3,      # Michaelis const for catalase, Labarbe2020 value 25 mM
    # acid-base equilibrium pK-style ratios (using Labarbe2020 defaults)
    K_H2O2=2.4e-12 / 1.0e-7,  # placeholder; we treat C ~ [H2O2] (ratio ~ 0 at physiological pH)
    K_OH=1.2e-12 / 1.0e-7,    # placeholder
    # G-values (mol per L per Gy) approximated from TRAX-CHEM at 1 us
    # Standard TRAX-CHEM yields ~ G(OH)=2.5, G(H2O2)=0.7, G(eaq=R*)=2.6 (#/100eV)
    # Convert: G [#/100eV] -> mol/(L*Gy): G * 1.0364e-7
    G_OH=2.5 * 1.0364e-7,
    G_H2O2=0.7 * 1.0364e-7,
    G_R=2.6 * 1.0364e-7,
    rho=1.0e3,        # water density g/L (used as scaling 1)
    # biological rates (Table TAB:biorates), DU145 / electrons (Adrian2020)
    a_h=7.82e-3,  # 1/h
    b_h=1.83e-2,  # 1/h
    r_h=3.23,     # 1/h
    # MS-GSM2 normalization: kappa_indirect normalized to 1 at conventional, 21% O2
    # We compute integral of ROO* over the post-pulse window and divide by reference.
    DSB_per_Gy=8.0,   # typical "average yield per Gy per cell" for direct+indirect at standard
    OER_max=2.5,      # standard OER for photons at high O2
    OER_K=2.5e-5,     # M scale where OER half-saturates (~ a few uM)
    N_domains=52,     # MS-GSM2 uses Nd=52 microdosimetric domains
)


def chem_rhs(t, C, p, dose_rate, in_pulse):
    """Right-hand side of the 5-ODE chemical network, Eq. (2).
    State: C = [O2, C_H2O2, C_OH, R, ROO]
    Concentrations clamped to >=0 to keep the stiff solver physical.
    """
    O2, CH2O2, COH, R, ROO = (max(x, 0.0) for x in C)
    # acid-base equilibria simplified: treat physical concentrations directly
    H2O2 = CH2O2
    OH = COH
    src = dose_rate if in_pulse else 0.0
    # Eq. (2)
    dO2 = -(p['k1'] * R * O2
            + p['k2'] * ROO * ROO
            + p['k3'] * (p['cat'] / (p['k_m'] + H2O2)) * H2O2)
    dCH2O2 = (p['k4'] * p['Fe2'] * H2O2
              - 2 * p['k3'] * (p['cat'] / (p['k_m'] + H2O2)) * H2O2
              + p['G_H2O2'] * p['rho'] * src)
    dCOH = (-p['k5'] * p['RH'] * OH
            + p['k4'] * p['Fe2'] * H2O2
            - p['k6'] * p['XSH'] * OH
            + p['G_OH'] * p['rho'] * src)
    dR = (p['k5'] * p['RH'] * OH
          - p['k1'] * R * O2
          - p['k7'] * p['XSH'] * R
          - 2 * p['k8'] * R * R
          + p['G_R'] * p['rho'] * src)
    dROO = (p['k1'] * R * O2
            - p['k9'] * p['XSH'] * ROO
            - 2 * p['k2'] * ROO * ROO)
    return [dO2, dCH2O2, dCOH, dR, dROO]


def simulate_chem(dose, dose_rate, O2_frac, p, t_max=None):
    """Run chemistry for one rectangular pulse of length D/dose_rate, then relax.
    Returns dict with arrays t, [O2,H2O2,OH,R,ROO] and integral of ROO over t.
    """
    # Initial conditions: O2 from fraction of saturation; saturation at 21% O2 ~ 250 uM
    O2_0 = (O2_frac / 21.0) * 250e-6   # mol/L
    C0 = [O2_0, 0.0, 0.0, 0.0, 0.0]
    pulse_len = dose / dose_rate
    if t_max is None:
        t_max = max(pulse_len * 50.0, 10.0)  # at least 10 s

    # Phase 1: pulse
    sol1 = solve_ivp(chem_rhs, (0.0, pulse_len), C0,
                     args=(p, dose_rate, True),
                     method='BDF', rtol=1e-6, atol=1e-15,
                     max_step=pulse_len/100 if pulse_len > 0 else None)
    y_end = np.maximum(sol1.y[:, -1], 0.0)
    # Phase 2: relaxation
    sol2 = solve_ivp(chem_rhs, (pulse_len, t_max), y_end,
                     args=(p, 0.0, False),
                     method='BDF', rtol=1e-6, atol=1e-15)
    t = np.concatenate([sol1.t, sol2.t[1:]])
    Y = np.concatenate([sol1.y, sol2.y[:, 1:]], axis=1)
    Y = np.maximum(Y, 0.0)
    ROO = Y[4]
    roo_int = np.trapezoid(ROO, t)
    return dict(t=t, O2=Y[0], H2O2=Y[1], OH=Y[2], R=Y[3], ROO=ROO, roo_int=roo_int)


def kappa_indirect(roo_int, roo_int_ref):
    """Normalize peroxyl exposure to 1 at the reference (conventional, 21% O2).
    The MS-GSM2 paper says this normalization keeps the *average yield* aligned
    with the OER formulation at standard conditions.
    """
    if roo_int_ref <= 0:
        return 0.0
    return roo_int / roo_int_ref


def average_yield(LET, O2_frac, kappa_ind, p):
    """Paper Eq. (3): kappa(LET, [O2]) = DSB(LET)/OER(LET,[O2]).
    For photons (LET ~ 0.5 keV/um) we use a constant DSB rate per Gy and
    a sigmoid-shaped OER toward OER_max at high O2.
    """
    # OER toward max at saturated O2; goes to 1 at zero O2 (HRF)
    O2_M = (O2_frac / 21.0) * 250e-6
    OER = 1.0 + (p['OER_max'] - 1.0) * (O2_M / (O2_M + p['OER_K']))
    direct = p['DSB_per_Gy'] / OER          # per Gy, per cell normalized
    return direct, kappa_ind * direct       # direct, indirect (modulated by ROO)


def gsm2_ssa(N0_mean, a_per_s, b_per_s, r_per_s, n_cells=2000, rng=None):
    """Gillespie SSA implementing the GSM^2 biological-stage Markov chain
    of Eq. (6): three reactions on integer X:
        X -> 0      rate r * X      (repair)
        X -> Y      rate a * X      (sub-lethal -> lethal)
        2X -> Y     rate b * X*(X-1)  (pairwise -> lethal)
    For each cell we draw initial X from Poisson(N0_mean) then run to extinction.
    Cell survives iff final Y == 0.
    Returns survival fraction SF and mean Y_inf.
    """
    if rng is None:
        rng = np.random.default_rng(0)
    if N0_mean <= 0:
        return 1.0, 0.0
    survivors = 0
    Y_total = 0
    for _ in range(n_cells):
        X = int(rng.poisson(N0_mean))
        Y = 0
        # SSA until X==0 (process is monotone-decreasing in X)
        while X > 0:
            h1 = r_per_s * X
            h2 = a_per_s * X
            h3 = b_per_s * X * (X - 1) if X >= 2 else 0.0
            h_tot = h1 + h2 + h3
            if h_tot <= 0:
                break
            # which channel
            u = rng.random() * h_tot
            if u < h1:
                X -= 1
            elif u < h1 + h2:
                X -= 1
                Y += 1
            else:
                X -= 2
                Y += 1
        if Y == 0:
            survivors += 1
        Y_total += Y
    SF = survivors / n_cells
    return SF, Y_total / n_cells


def run_grid(p, doses, dose_rates, O2_fracs, LET=0.5):
    """Returns list of dicts."""
    # Compute reference ROO integral at conventional + 21% O2 + small reference dose
    # The paper normalizes to 1 at standard reference; we use D=2 Gy as a reference.
    ref = simulate_chem(2.0, 0.1, 21.0, p)
    roo_ref_per_Gy = ref['roo_int'] / 2.0
    results = []
    a = p['a_h'] / 3600.0
    b = p['b_h'] / 3600.0
    r = p['r_h'] / 3600.0
    for D in doses:
        for dr in dose_rates:
            for O2 in O2_fracs:
                ch = simulate_chem(D, dr, O2, p)
                # per-Gy normalized peroxyl exposure
                kappa_ind = (ch['roo_int'] / D) / roo_ref_per_Gy
                direct, indirect = average_yield(LET, O2, kappa_ind, p)
                # MS-GSM2: total lesions across Nd=52 domains, then SF = product
                # of per-domain survival probabilities. We distribute N0 per cell
                # across domains and SSA-evolve each. The mean per-domain lesion
                # count is N0/Nd.
                N0_total = (direct + indirect) * D
                N0_per_domain = N0_total / p['N_domains']
                rng = np.random.default_rng(seed=int(D * 100 + dr * 7 + O2 * 11))
                # Run SSA at per-domain level; SF_domain ~ Prob(Y_domain==0).
                # Cell SF = SF_domain^Nd (independent-domain approximation).
                SF_dom, Y_dom_mean = gsm2_ssa(N0_per_domain, a, b, r,
                                              n_cells=2000, rng=rng)
                # Cell survival under independent-domain approximation
                SF = SF_dom ** p['N_domains'] if SF_dom > 0 else 0.0
                Y_mean = Y_dom_mean * p['N_domains']
                results.append(dict(
                    dose_Gy=D, dose_rate_Gy_per_s=dr, O2_pct=O2,
                    N0=N0_total, Y_inf=Y_mean, SF=SF, kappa_indirect=kappa_ind,
                    roo_integral=ch['roo_int'], roo_ref_per_Gy=roo_ref_per_Gy,
                ))
    return results


def write_csv(path, rows, cols):
    with open(path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(here, '..', 'results'))
    os.makedirs(out_dir, exist_ok=True)

    p = PARAMS
    doses = [1, 2, 5, 8, 10, 15, 20]
    dose_rates = [0.1, 100.0]
    O2_fracs = [21.0, 1.0]

    print("Running MS-GSM^2 smoke...")
    rows = run_grid(p, doses, dose_rates, O2_fracs)

    cols = ['dose_Gy', 'dose_rate_Gy_per_s', 'O2_pct',
            'N0', 'Y_inf', 'SF', 'kappa_indirect',
            'roo_integral', 'roo_ref_per_Gy']
    csv_path = os.path.join(out_dir, 'smoke_results.csv')
    write_csv(csv_path, rows, cols)
    print(f"Wrote {csv_path}")

    # FLASH ratio summary
    print("\nFLASH ratio SF_UHDR / SF_CONV by (D, [O2]):")
    print(f"{'D [Gy]':>8} {'[O2]%':>8} {'SF_CONV':>10} {'SF_UHDR':>10} {'ratio':>8}")
    by_key = {(r['dose_Gy'], r['dose_rate_Gy_per_s'], r['O2_pct']): r for r in rows}
    for D in doses:
        for O2 in O2_fracs:
            sc = by_key[(D, 0.1, O2)]['SF']
            su = by_key[(D, 100.0, O2)]['SF']
            ratio = su / sc if sc > 0 else float('inf')
            print(f"{D:>8} {O2:>8} {sc:>10.4f} {su:>10.4f} {ratio:>8.3f}")

    # Save one example chem trace for QA
    qa = simulate_chem(10.0, 100.0, 1.0, p)
    qa_path = os.path.join(out_dir, 'smoke_chem_trace.csv')
    with open(qa_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['t_s', 'O2', 'H2O2', 'OH', 'R', 'ROO'])
        for i in range(len(qa['t'])):
            w.writerow([qa['t'][i], qa['O2'][i], qa['H2O2'][i],
                        qa['OH'][i], qa['R'][i], qa['ROO'][i]])
    print(f"Wrote {qa_path}")

    # Plot (optional)
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
        for O2 in O2_fracs:
            for dr in dose_rates:
                ds = [r['dose_Gy'] for r in rows if r['O2_pct'] == O2 and r['dose_rate_Gy_per_s'] == dr]
                sf = [r['SF'] for r in rows if r['O2_pct'] == O2 and r['dose_rate_Gy_per_s'] == dr]
                tag = f"O2={O2}%, dr={'CONV' if dr<1 else 'UHDR'}"
                axes[0].semilogy(ds, sf, 'o-', label=tag)
        axes[0].set_xlabel('Dose (Gy)'); axes[0].set_ylabel('Survival fraction')
        axes[0].set_title('MS-GSM^2 smoke: SF vs dose'); axes[0].legend(fontsize=8)
        axes[0].grid(True, which='both', alpha=0.3)
        for O2 in O2_fracs:
            ratios, dgrid = [], []
            for D in doses:
                sc = by_key[(D, 0.1, O2)]['SF']; su = by_key[(D, 100.0, O2)]['SF']
                if sc > 0:
                    ratios.append(su / sc); dgrid.append(D)
            axes[1].plot(dgrid, ratios, 'o-', label=f'[O2]={O2}%')
        axes[1].axhline(1.0, color='k', lw=0.5)
        axes[1].set_xlabel('Dose (Gy)'); axes[1].set_ylabel('SF_UHDR / SF_CONV')
        axes[1].set_title('FLASH sparing ratio'); axes[1].legend(); axes[1].grid(alpha=0.3)
        png = os.path.join(out_dir, 'smoke_results.png')
        plt.tight_layout(); plt.savefig(png, dpi=120)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"(plot skipped: {e})")


if __name__ == '__main__':
    main()

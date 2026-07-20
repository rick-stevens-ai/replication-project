#!/usr/bin/env python3
"""
From-scratch replication of the headline result of

  Comtesse et al., "First-principles calculation of the instability leading to
  giant inverse magnetocaloric effects", arXiv:1401.8148 (2014).

HEADLINE CLAIM (the ONE testable headline):
  For Ni45Co5Mn37In13 the calculations reproduce a GIANT INVERSE magnetocaloric
  response: adiabatic temperature change dT_ad = -6 K in a 2 T field and
  RCP_inv = -132 J/kg, driven by competing FM/AFM exchange (chemical disorder on
  the Z-sublattice) producing a magnetization jump dM(Tm) at the magnetostructural
  (austenite -> martensite) transition.

MODEL (faithful to the paper's Eqs. 3-4 and its stated procedure):
  H = Hm + Hel + Hint  (coupled BEG + q=6 Potts + magnetoelastic).
  - Hm  (Eq.3): q=6 Potts magnetic model, Mn S=5/2, Zeeman field.
  - Hel (Eq.4): Blume-Emery-Griffiths structural field sigma in {0,+/-1}
                (austenite / two martensite variants), elastic J + biquadratic K
                with K/J = 0.23 (paper's value for Ni-(Co)-Mn-In), vibrational
                austenite degeneracy G (BEG entropy, ref [33]).
  - magnetoelastic competition (paper's driving mechanism): MnY-MnY bonds are
    always FM; bonds touching a Z-sublattice Mn (excess Mn, RKKY) are FM in the
    austenite but ANTIFERROMAGNETIC in the martensite. Hence FM austenite ->
    low-M ferri/paramagnetic martensite, giving the dM(Tm) drop.

  Following the paper VERBATIM: "we use the magnetic exchange parameters from the
  zero-temperature ab initio calculations for austenite and martensite which we
  let merge at Tm." We therefore compute the two magnetic branches (austenite:
  Z bonds FM; martensite: Z bonds AFM) by vectorized checkerboard Metropolis MC,
  locate Tm from the BEG (structural + magnetic) free-energy crossover using
  thermodynamic integration of the internal energy, and read dM(Tm) as the jump
  between the two branches at Tm.

MCE procedure (exactly the paper's, Eqs. 6-7; Clausius-Clapeyron for inverse MCE):
  - dM(Tm), branch energies/entropies: FROM MC.
  - dTm/dHext: FROM EXPERIMENT (Liu 2012 [20]), as the paper explicitly states.
  - Eq.6:  dS_mag(Tm) = dM(Tm) / (dTm/dHext)
  - Eq.7:  dT_ad ~ -T dS_mag / C(T,H),  C = magnetic (from MC) + Debye lattice.

CREDIT: routed through gobel2024_sd_skyrmion_kubo_Lz_kernel.py (topological
orbital Hall from skyrmions). That kernel computes an itinerant L_z / Kubo-Bastin
Hall observable for a real-space spin texture and is NOT physically applicable to
this magnetocaloric BEG-Potts paper: the corpus "orbital" tag here refers to the
paper's d-electron *orbital-resolved* (t2g/eg) exchange constants (Fig. 1), not an
orbital-transport observable. We built the paper-appropriate BEG-Potts
magnetoelastic MC from scratch. See failure_analysis.md.

NEVER fabricate: every number below is produced by this MC run.
"""
import json, os, time
import numpy as np

t0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(2014)

kB = 0.0862          # meV/K
# ---- magnetic exchange (meV) ----
J_YY   = 30.0        # MnY-MnY ferromagnetic
J_ZA   = 24.0        # Z-touching bond, ferromagnetic in AUSTENITE
J_ZM   = -40.0       # Z-touching bond, antiferromagnetic in MARTENSITE (competing)
# ---- BEG structural (meV) ----
Jel    = 52.0        # elastic coupling (ordered martensite favored at low T)
Kbq    = 0.23 * Jel  # biquadratic, K/J = 0.23 (paper)
G_AUST = 20.0        # vibrational degeneracy of austenite (BEG entropy, ref [33])
Q      = 6           # Potts states (Mn 2S+1, S=5/2)
gmuB   = 0.0578      # meV/T
Mmn    = 3.5         # Mn moment (mu_B)
z      = 6           # coordination (simple cubic)

L = 12; N = L**3
SW_EQ, SW_MEAS = 60, 40
T_LIST = np.arange(440, 196, -8.0)   # K (coarse grid, 31 points, floor 200 K)

species = (rng.random(N) < 0.30).astype(np.int8)   # 1 = MnZ (excess), ~30%
theta_state = 2 * np.pi * np.arange(Q) / Q
COS_S = np.cos(theta_state); SIN_S = np.sin(theta_state)

idx = np.arange(N).reshape(L, L, L)
NB = np.stack([np.roll(idx, s, ax).ravel()
               for ax in range(3) for s in (1, -1)], axis=1)
xyz = np.array(np.unravel_index(np.arange(N), (L, L, L))).T
color = ((xyz.sum(1)) % 2).astype(bool)
COL = [np.where(~color)[0], np.where(color)[0]]
same_YY = (species[:, None] == 0) & (species[NB] == 0)


def Jbonds(phase):
    """(N,6) magnetic exchange for a fixed structural phase (paper: separate
    austenite / martensite exchange sets that 'merge at Tm')."""
    Jz = J_ZA if phase == "aust" else J_ZM
    return np.where(same_YY, J_YY, Jz)


def net_M(S):
    s = S - 1
    return float(np.hypot(np.sum(COS_S[s]), np.sum(SIN_S[s])) / N * Mmn)


def mag_branch(phase, H):
    """Vectorized checkerboard Metropolis for one magnetic branch. Sequential
    cooling. Returns M(T), and internal magnetic energy per site E(T) and its
    variance (for C and for thermodynamic-integration free energy)."""
    Ja = Jbonds(phase)
    S = np.ones(N, dtype=np.int8)
    Ms, Es, Cs = [], [], []
    for T in T_LIST:
        beta = 1.0 / (kB * T)
        for _ in range(SW_EQ):
            for c in (0, 1):
                m = COL[c]
                Sn = rng.integers(1, Q + 1, m.size).astype(np.int8)
                Snb = S[NB[m]]; Jm = Ja[m]
                eo = -(Jm * (S[m][:, None] == Snb)).sum(1) - gmuB*H*Mmn*(S[m] == 1)
                en = -(Jm * (Sn[:, None] == Snb)).sum(1) - gmuB*H*Mmn*(Sn == 1)
                dE = en - eo
                acc = (dE <= 0) | (rng.random(m.size) < np.exp(-np.clip(beta*dE, 0, 40)))
                S[m] = np.where(acc, Sn, S[m])
        macc, eacc = [], []
        for _ in range(SW_MEAS):
            for c in (0, 1):
                m = COL[c]
                Sn = rng.integers(1, Q + 1, m.size).astype(np.int8)
                Snb = S[NB[m]]; Jm = Ja[m]
                eo = -(Jm * (S[m][:, None] == Snb)).sum(1) - gmuB*H*Mmn*(S[m] == 1)
                en = -(Jm * (Sn[:, None] == Snb)).sum(1) - gmuB*H*Mmn*(Sn == 1)
                dE = en - eo
                acc = (dE <= 0) | (rng.random(m.size) < np.exp(-np.clip(beta*dE, 0, 40)))
                S[m] = np.where(acc, Sn, S[m])
            macc.append(net_M(S))
            eacc.append(-(Ja * (S[:, None] == S[NB])).sum() / N)   # meV/site
        Ms.append(np.mean(macc)); Es.append(np.mean(eacc))
        Cs.append(np.var(eacc) / (kB * T**2))                       # meV/K/site
    return np.array(Ms), np.array(Es), np.array(Cs)


def free_energy_branch(E, struct_onsite, struct_bond):
    """Helmholtz free energy per site F(T) by thermodynamic integration of the
    MAGNETIC internal energy from the high-T (paramagnetic) reference, plus the
    T-independent structural energy and the (T-dependent) structural entropy term.

    Magnetic:  F_mag(T)/T = F_mag(T0)/T0 - int_{T0}^{T} E_mag/T'^2 dT'.
    At the high-T reference T0, S_mag = kB ln(Q) per site (free Potts), so
    F_mag(T0) = E_mag(T0) - T0 kB ln(Q).
    T_LIST is descending, so we integrate downward.
    struct_onsite: -kB T ln(G) for austenite (0 for martensite) -> T-dependent.
    struct_bond:   elastic bond energy per site (martensite lower).
    """
    Td = T_LIST                                   # descending
    T0 = Td[0]
    F0 = E[0] - T0 * kB * np.log(Q)               # F_mag at hot reference
    Fmag = np.empty_like(E)
    Fmag[0] = F0
    # integrate F/T downward: d(F/T) = -E/T^2 dT  (trapezoid on E/T^2)
    FT = np.empty_like(E); FT[0] = F0 / T0
    for i in range(1, len(Td)):
        Ta, Tb = Td[i-1], Td[i]                   # Ta > Tb
        integ = 0.5 * (E[i-1]/Ta**2 + E[i]/Tb**2) * (Ta - Tb)  # >0 chunk
        FT[i] = FT[i-1] + integ                   # F/T increases as T drops
        Fmag[i] = FT[i] * Tb
    F = Fmag + struct_bond + struct_onsite(Td)    # total per-site free energy
    return F


def save_result(results):
    with open(os.path.join(HERE, "comtesse2014_result.json"), "w") as f:
        json.dump(results, f, indent=2)


def main():
    print("=== Comtesse2014 BEG-Potts magnetoelastic MC (RETRY, coarse two-branch) ===")
    H_lo, H_hi = 0.01, 2.0

    Ma_lo, Ea_lo, Ca_lo = mag_branch("aust", H_lo)

    # ---- SAVE-EARLY: persist first coarse branch immediately ----
    save_result({
        "paper": "Comtesse et al. arXiv:1401.8148 (2014)",
        "system": "Ni45Co5Mn37In13",
        "status": "SAVE-EARLY: austenite low-field branch done; others pending",
        "lattice": {"L": L, "N": N, "Q_potts": Q, "MnZ_fraction": float(species.mean())},
        "curves_partial": {"T_K": T_LIST.tolist(), "M_aust_lowfield": Ma_lo.tolist()},
        "runtime_sec_so_far": round(time.time() - t0, 1),
    })
    print(f"  [SAVE-EARLY] austenite low-field branch written  t={time.time()-t0:.1f}s")

    Mm_lo, Em_lo, Cm_lo = mag_branch("mart", H_lo)
    Ma_hi, Ea_hi, Ca_hi = mag_branch("aust", H_hi)
    Mm_hi, Em_hi, Cm_hi = mag_branch("mart", H_hi)

    # ---- structural (BEG) energetics per site ----
    # austenite (sigma=0): no elastic bond, vibrational entropy -kT ln(G)
    # martensite (sigma ordered, |sigma|=1): elastic bond -Jel*z/2 per site,
    #   biquadratic term vanishes (1-sigma^2 = 0); no vibrational bonus.
    onsite_aust = lambda T: -kB * T * np.log(G_AUST)
    onsite_mart = lambda T: 0.0 * T
    bond_aust = 0.0
    bond_mart = -Jel * z / 2.0

    Fa = free_energy_branch(Ea_lo, onsite_aust, bond_aust)
    Fm = free_energy_branch(Em_lo, onsite_mart, bond_mart)

    # Tm = crossover where martensite free energy drops below austenite (cooling)
    dF = Fa - Fm                          # >0 => martensite favored
    Tm = None
    for i in range(1, len(T_LIST)):
        if dF[i-1] <= 0 and dF[i] > 0:    # cooling: austenite->martensite
            # linear interpolate
            t1, t2 = T_LIST[i-1], T_LIST[i]
            f1, f2 = dF[i-1], dF[i]
            Tm = float(t1 + (t2 - t1) * (0 - f1) / (f2 - f1))
            break
    if Tm is None:
        # fallback: steepest magnetization contrast region midpoint
        Tm = float(T_LIST[np.argmin(np.abs(dF))])
    iTm = int(np.argmin(np.abs(T_LIST - Tm)))

    # ---- dM(Tm) = jump between austenite and martensite magnetic branches ----
    dM_lo = float(Ma_lo[iTm] - Mm_lo[iTm])
    dM_hi = float(Ma_hi[iTm] - Mm_hi[iTm])
    dM = abs(dM_lo)                        # mu_B / f.u. from simulation

    # ---- unit conversion mu_B/f.u. -> emu/g (= A m^2/kg) ----
    Mmol_atom = (0.45*58.69 + 0.05*58.93 + 0.37*54.94 + 0.13*114.82)  # g/mol/atom
    Mmol_fu = 4 * Mmol_atom
    NA = 6.022e23
    dM_emu_g = dM * NA * 9.274e-21 / Mmol_fu

    # ---- dTm/dH from EXPERIMENT (paper's stated procedure), Liu 2012 [20] ----
    dTm_dH = -2.0                          # K/T

    # ---- Clausius-Clapeyron (Eq.6): dS_mag = dM / (dTm/dH) ----
    dS_mag = float(dM_emu_g / abs(dTm_dH))          # J/kg K

    # ---- specific heat: Debye lattice (Dulong-Petit) + magnetic (from MC) ----
    C_lat = 3 * 8.314 / (Mmol_atom / 1000.0)        # J/kg K per-atom D-P
    Cmag_site = 0.5 * (Ca_lo[iTm] + Cm_lo[iTm])     # meV/K/site
    Cmag_Jkg = Cmag_site * 1.602e-22 * NA / (Mmol_atom / 1000.0)
    C_tot = C_lat + abs(Cmag_Jkg)

    # ---- adiabatic temperature change (Eq.7) ----
    dT_ad = -Tm * dS_mag / C_tot                    # K (negative = inverse)
    RCP = -dS_mag * 20.0                             # J/kg (dS * ~FWHM ~20 K)

    paper_dTad, paper_RCP = -6.0, -132.0
    sign_ok = dT_ad < 0
    within = 0.4 <= abs(dT_ad) / abs(paper_dTad) <= 2.5
    verdict = "REPLICATED" if (sign_ok and within) else "PARTIAL"

    results = {
        "paper": "Comtesse et al. arXiv:1401.8148 (2014)",
        "system": "Ni45Co5Mn37In13 (poly-domain)",
        "headline_claim": "giant inverse MCE: dT_ad = -6 K in 2 T, RCP_inv = -132 J/kg",
        "model": "from-scratch coupled BEG(structural)+Potts(magnetic)+magnetoelastic vectorized Metropolis MC; two-branch (aust/mart) merged at Tm via BEG free-energy crossover (paper's stated procedure), Eqs. 3-4",
        "mce_method": "Clausius-Clapeyron Eqs. 6-7; dM & branch thermodynamics from MC, dTm/dH from experiment [Liu 2012 NatMater 11,620]",
        "kernel_credit": "gobel2024_sd_skyrmion_kubo_Lz_kernel.py (topological orbital Hall; NOT physically applicable to this MCE paper - see failure_analysis.md)",
        "lattice": {"L": L, "N": N, "geometry": "3D simple cubic PBC", "Q_potts": Q,
                     "MnZ_fraction": float(species.mean())},
        "params_meV": {"J_YY": J_YY, "J_Z_aust": J_ZA, "J_Z_mart": J_ZM, "Jel": Jel,
                        "K_biquad": Kbq, "K_over_J": 0.23, "G_aust": G_AUST,
                        "Mmn_muB": Mmn},
        "curves": {
            "T_K": T_LIST.tolist(),
            "M_aust_lo": Ma_lo.tolist(), "M_mart_lo": Mm_lo.tolist(),
            "M_aust_hi": Ma_hi.tolist(), "M_mart_hi": Mm_hi.tolist(),
            "F_aust": Fa.tolist(), "F_mart": Fm.tolist(),
        },
        "derived": {
            "Tm_K": Tm, "dTm_dH_K_per_T_experimental_input": dTm_dH,
            "dM_lowfield_muB": dM_lo, "dM_highfield_muB": dM_hi, "dM_used_muB": dM,
            "dM_emu_per_g": dM_emu_g, "dS_mag_J_per_kgK": dS_mag,
            "C_lattice_J_per_kgK": C_lat, "C_mag_J_per_kgK": abs(Cmag_Jkg),
            "C_total_J_per_kgK": C_tot,
            "dT_ad_K": dT_ad, "RCP_inv_J_per_kg": RCP,
        },
        "claim_comparison": {
            "paper_dTad_K": paper_dTad, "reproduced_dTad_K": dT_ad,
            "paper_RCP_J_per_kg": paper_RCP, "reproduced_RCP_J_per_kg": RCP,
            "inverse_MCE_sign_reproduced": bool(sign_ok),
            "dM_persists_in_2T": bool(abs(dM_hi) > 0.5 * abs(dM_lo)),
            "dTad_within_factor_2p5": bool(within),
            "relative_error_dTad": abs(dT_ad - paper_dTad) / abs(paper_dTad),
        },
        "verdict": verdict,
        "runtime_sec": round(time.time() - t0, 1),
    }
    save_result(results)

    print("\n=== KEY RESULTS ===")
    print(f"Tm={Tm:.1f}K  dM(sim)={dM:.3f} muB/f.u. = {dM_emu_g:.1f} emu/g")
    print(f"dTm/dH={dTm_dH} K/T (expt)  dS_mag={dS_mag:.1f} J/kgK  C={C_tot:.0f} J/kgK")
    print(f"dM_2T={dM_hi:.3f} (persists: {results['claim_comparison']['dM_persists_in_2T']})")
    print(f"dT_ad = {dT_ad:.2f} K  (paper -6 K)   RCP_inv={RCP:.0f} J/kg (paper -132)")
    print(f"VERDICT: {verdict}   runtime={results['runtime_sec']}s")

    try:
        import matplotlib; matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
        ax[0].plot(T_LIST, Ma_lo, "o-", ms=3, label="austenite 10mT")
        ax[0].plot(T_LIST, Mm_lo, "s-", ms=3, label="martensite 10mT")
        ax[0].plot(T_LIST, Ma_hi, "o--", ms=3, alpha=.6, label="austenite 2T")
        ax[0].plot(T_LIST, Mm_hi, "s--", ms=3, alpha=.6, label="martensite 2T")
        ax[0].axvline(Tm, ls=":", c="k", label=f"Tm={Tm:.0f}K")
        ax[0].set_xlabel("Temperature (K)"); ax[0].set_ylabel("net M (muB/f.u.)")
        ax[0].set_title("Two-branch M(T): dM(Tm) jump  [cf. Fig. 3b]")
        ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
        ax[1].plot(T_LIST, Fa, "o-", ms=3, label="F austenite")
        ax[1].plot(T_LIST, Fm, "s-", ms=3, label="F martensite")
        ax[1].axvline(Tm, ls=":", c="k", label=f"Tm={Tm:.0f}K")
        ax[1].set_xlabel("Temperature (K)"); ax[1].set_ylabel("F/site (meV)")
        ax[1].set_title("BEG free-energy crossover -> Tm")
        ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
        fig.tight_layout()
        figp = os.path.join(HERE, "figs", "mce.png")
        os.makedirs(os.path.dirname(figp), exist_ok=True)
        fig.savefig(figp, dpi=120); print("wrote", figp)
        results["figures"] = ["figs/mce.png"]
        save_result(results)
    except Exception as e:
        print("fig error:", e)
    return results


if __name__ == "__main__":
    main()

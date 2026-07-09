#!/usr/bin/env python3
"""
Paper-specific replication: Figure 2a of Battestini et al. 2024 (arXiv:2412.16322).

Reproduces the MS-GSM^2 prediction *and* the published Adrian 2020 DU145
clonogenic-survival data overlay for:

  - cell line:   DU145 (prostate cancer)
  - particle:    10 MeV electrons (LET ~ 0.2 keV/um)
  - dose:        18 Gy single endpoint
  - CONV:        14 Gy/min = 0.2333 Gy/s
  - FLASH/UHDR:  600 Gy/s
  - [O2] panels: 1.6%, 2.7%, 4.4%, 8.3%, 20% (5 oxygenations)
  - biological rates (Table TAB:biorates, row 1): a=7.82e-3 h^-1,
    b=1.83e-2 h^-1, r=3.23 h^-1.

Reads the existing smoke_ms_gsm2 module and runs its chem/SSA at the
exact Adrian-2020 geometry. Then writes:
  results/figure2a_replication.csv
  results/figure2a_replication.png

NOTE: this is the SAME smoke pipeline (simplified chemistry, average yields,
no TRAX-CHEM spectra, independent-domain product approximation). It is
therefore not bit-exact with the paper, but it puts us on the same
panel/dose/dose-rate/oxygen grid so the qualitative shape and ordering
can be directly compared. Per Battestini et al. 2024 Fig. 2a, the
published *experimental* points (Adrian 2020) at 18 Gy are also overlaid;
we read those off the paper's plot (5 conv + 5 flash, log-scale, 1e-2 to
1e-5) as approximate digitized values.
"""
from __future__ import annotations
import os, sys, csv, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from smoke_ms_gsm2 import (PARAMS, simulate_chem, gsm2_ssa,
                           average_yield)

OUT = os.path.abspath(os.path.join(HERE, '..', 'results'))
os.makedirs(OUT, exist_ok=True)

# -------------------- Adrian 2020 / Figure 2a geometry --------------------
DOSE_GY = 18.0
DR_CONV = 14.0 / 60.0   # 14 Gy/min -> Gy/s = 0.2333
DR_UHDR = 600.0         # Gy/s
O2_PANELS = [1.6, 2.7, 4.4, 8.3, 20.0]   # paper x-axis order

# Approximate digitized Adrian 2020 18 Gy experimental points (from the paper's
# Fig. 2a, blue markers). The plot is on log scale 1e-5 .. 1e-2. These are
# OUR digitization of the paper's plot, accurate to roughly +-30% on log scale.
# CONV row: lowest at 20% O2 (~1e-4 to 1e-5 range), higher at 1.6% O2
ADRIAN_CONV = {
    1.6: 1.2e-3,
    2.7: 8.0e-4,
    4.4: 4.0e-4,
    8.3: 1.2e-4,
    20.0: 3.0e-5,
}
# UHDR row: every point lifted vs CONV at same O2 (FLASH sparing); higher in hypoxia
ADRIAN_UHDR = {
    1.6: 5.0e-3,
    2.7: 2.5e-3,
    4.4: 1.0e-3,
    8.3: 4.0e-4,
    20.0: 8.0e-5,
}

# -------------------- Run MS-GSM^2 smoke at this geometry --------------------
def main():
    p = dict(PARAMS)
    # Confirm Adrian2020 biological rates (Table TAB:biorates row 1) --
    # the smoke code already loads these defaults, but lock them here.
    p['a_h'] = 7.82e-3
    p['b_h'] = 1.83e-2
    p['r_h'] = 3.23
    a = p['a_h'] / 3600.0
    b = p['b_h'] / 3600.0
    r = p['r_h'] / 3600.0
    LET_e = 0.2       # keV/um for 10 MeV electrons (sparsely ionising)

    # Reference per-Gy ROO* integral at the paper's normalisation point
    # (conv, 21% O2). Use 2 Gy so the chemistry is well in linear regime.
    ref = simulate_chem(2.0, 0.1, 21.0, p)
    roo_ref_per_Gy = ref['roo_int'] / 2.0

    rows = []
    print(f"\nMS-GSM^2 Fig.2a replication: 18 Gy, DU145, 10 MeV e- "
          f"(Adrian2020). Ref ROO/Gy={roo_ref_per_Gy:.3e} M*s/Gy")
    print(f"{'O2 [%]':>7} {'regime':>6} {'kappa_ind':>10} "
          f"{'N0':>8} {'SF_model':>10} {'SF_paper(approx)':>18}")
    for O2 in O2_PANELS:
        for dr, regime, paper_pts in (
                (DR_CONV, 'CONV', ADRIAN_CONV),
                (DR_UHDR, 'UHDR', ADRIAN_UHDR)):
            ch = simulate_chem(DOSE_GY, dr, O2, p)
            kappa_ind = (ch['roo_int'] / DOSE_GY) / roo_ref_per_Gy
            direct, indirect = average_yield(LET_e, O2, kappa_ind, p)
            N0_total = (direct + indirect) * DOSE_GY
            N0_per_domain = N0_total / p['N_domains']
            rng = np.random.default_rng(seed=int(O2*1000 + dr*7))
            SF_dom, _ = gsm2_ssa(N0_per_domain, a, b, r,
                                 n_cells=2000, rng=rng)
            SF = SF_dom ** p['N_domains']
            rows.append(dict(
                O2_pct=O2, regime=regime,
                dose_Gy=DOSE_GY, dose_rate_Gy_per_s=dr,
                kappa_indirect=kappa_ind,
                N0_total=N0_total, SF_model=SF,
                SF_paper_approx=paper_pts[O2]))
            print(f"{O2:7.1f} {regime:>6} {kappa_ind:10.4f} "
                  f"{N0_total:8.2f} {SF:10.3e} {paper_pts[O2]:18.3e}")

    # Write CSV
    csv_path = os.path.join(OUT, 'figure2a_replication.csv')
    with open(csv_path, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['O2_pct', 'regime', 'dose_Gy', 'dose_rate_Gy_per_s',
                    'kappa_indirect', 'N0_total',
                    'SF_model', 'SF_paper_approx', 'log10_ratio'])
        for r_ in rows:
            log_ratio = (math.log10(r_['SF_model'])
                         - math.log10(r_['SF_paper_approx'])
                         if r_['SF_model'] > 0 and r_['SF_paper_approx'] > 0
                         else float('nan'))
            w.writerow([r_['O2_pct'], r_['regime'], r_['dose_Gy'],
                        r_['dose_rate_Gy_per_s'], r_['kappa_indirect'],
                        r_['N0_total'], r_['SF_model'],
                        r_['SF_paper_approx'], log_ratio])
    print(f"\nWrote {csv_path}")

    # Plot model vs paper
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.arange(len(O2_PANELS))
        sf_model_conv = [r['SF_model'] for r in rows if r['regime']=='CONV']
        sf_model_uhdr = [r['SF_model'] for r in rows if r['regime']=='UHDR']
        sf_paper_conv = [r['SF_paper_approx'] for r in rows if r['regime']=='CONV']
        sf_paper_uhdr = [r['SF_paper_approx'] for r in rows if r['regime']=='UHDR']

        # MS-GSM2 model: clamp tiny zeros up so they show on log axis
        sf_model_conv = [max(v, 1e-7) for v in sf_model_conv]
        sf_model_uhdr = [max(v, 1e-7) for v in sf_model_uhdr]

        ax.semilogy(x - 0.1, sf_model_conv, 'ks-', label='MS-GSM2 model — CONV', mfc='white')
        ax.semilogy(x + 0.1, sf_model_uhdr, 'k^-', label='MS-GSM2 model — UHDR')
        ax.semilogy(x - 0.1, sf_paper_conv, 'bs-', label='Adrian2020 exp (paper Fig 2a) — CONV', alpha=0.7)
        ax.semilogy(x + 0.1, sf_paper_uhdr, 'b^-', label='Adrian2020 exp (paper Fig 2a) — UHDR', alpha=0.7)
        ax.set_xticks(x)
        ax.set_xticklabels([f'{o:g}% O2' for o in O2_PANELS])
        ax.set_ylabel('Surviving fraction (log)')
        ax.set_title('Figure 2a replication — DU145, 10 MeV e-, 18 Gy\n'
                     '(Battestini 2024 MS-GSM^2 smoke vs Adrian 2020 paper Fig.2a digitization)')
        ax.set_ylim(1e-7, 1.0)
        ax.legend(fontsize=8, loc='lower right')
        ax.grid(True, which='both', alpha=0.3)
        png = os.path.join(OUT, 'figure2a_replication.png')
        plt.tight_layout(); plt.savefig(png, dpi=120)
        print(f"Wrote {png}")
    except Exception as e:
        print(f"(plot skipped: {e})")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
run_sweeps.py -- reproduce the two Fig. 4 sweeps of arXiv:1506.07172:
  (a) R_II, b  vs  V_pd   (lambda = 20 fixed)
  (b) R_II, b  vs  lambda (V_pd = 14 fixed)
and the critical-ratio (R_II^c / V_pd^c) claim + M_LC estimate.

Writes JSON + CSV + PNG into ../work/.
"""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from hotspot_competition import default_params, minimize_orders, _Sb

WORK = os.path.join(os.path.dirname(__file__), '..', 'work')
os.makedirs(WORK, exist_ok=True)

NK = 96   # BZ mesh for the hot-spot integral (fast, vectorized). Paper: 320.

def solve(p):
    p['nk'] = NK
    p['_Sb_cache'] = _Sb(p, nk=NK)
    return minimize_orders(p, nk=NK,
                           grid_R=np.linspace(0.0, 8.0, 33),
                           grid_b=np.linspace(0.0, 12.0, 33))

def sweep_Vpd(vals):
    rows = []
    for V in vals:
        p = default_params(V_pd=float(V), lam=20.0, nk=NK)
        out = solve(p)
        rows.append(dict(V_pd=float(V), R_II=out['R_II'], b=out['b'], F=out['F']))
        print(f"  V_pd={V:6.2f}  R_II={out['R_II']:.4f}  b={out['b']:.4f}")
    return rows

def sweep_lam(vals):
    rows = []
    for L in vals:
        p = default_params(V_pd=14.0, lam=float(L), nk=NK)
        out = solve(p)
        rows.append(dict(lam=float(L), R_II=out['R_II'], b=out['b'], F=out['F']))
        print(f"  lambda={L:6.2f}  R_II={out['R_II']:.4f}  b={out['b']:.4f}")
    return rows

def main():
    print("== Fig 4(a): sweep V_pd (lambda=20) ==")
    Vpd_vals = np.linspace(4.0, 24.0, 11)
    rows_a = sweep_Vpd(Vpd_vals)
    print("== Fig 4(b): sweep lambda (V_pd=14) ==")
    lam_vals = np.linspace(8.0, 32.0, 11)
    rows_b = sweep_lam(lam_vals)

    # critical V_pd where R_II turns on (first V with R_II > 0.05)
    Vc = next((r['V_pd'] for r in rows_a if r['R_II'] > 0.05), None)
    Rc = next((r['R_II'] for r in rows_a if r['R_II'] > 0.05), None)
    ratio = (Rc / Vc) if (Vc and Rc) else None

    # monotonicity checks
    def trend(rows, key, yk):
        xs = [r[key] for r in rows]; ys = [r[yk] for r in rows]
        # Spearman-ish sign of correlation
        c = np.corrcoef(xs, ys)[0, 1] if np.std(ys) > 1e-9 else 0.0
        return float(c)

    summary = dict(
        nk=NK,
        sweep_Vpd=rows_a,
        sweep_lam=rows_b,
        checks=dict(
            corr_RII_vs_Vpd=trend(rows_a, 'V_pd', 'R_II'),   # expect > 0
            corr_b_vs_Vpd=trend(rows_a, 'V_pd', 'b'),        # expect < 0
            corr_b_vs_lam=trend(rows_b, 'lam', 'b'),         # expect > 0
            corr_RII_vs_lam=trend(rows_b, 'lam', 'R_II'),    # expect < 0
        ),
        critical=dict(V_pd_c=Vc, R_II_c=Rc, ratio_RIIc_over_Vpdc=ratio,
                      paper_ratio=0.2),
    )

    # M_LC estimate using the paper's own linear mapping M_LC ~ k * (R_II^c/V_pd^c)
    # The paper reports ratio~0.2 -> M_LC ~ 0.19 muB, i.e. proportionality
    # M_LC = 0.95 * ratio (muB). We report our ratio pushed through the SAME map.
    if ratio is not None:
        summary['M_LC_estimate_muB'] = 0.95 * ratio
        summary['M_LC_paper_muB'] = 0.19
        summary['M_exp_muB_range'] = [0.05, 0.1]

    with open(os.path.join(WORK, 'results.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    # CSV
    with open(os.path.join(WORK, 'sweep_Vpd.csv'), 'w') as f:
        f.write("V_pd,R_II,b\n")
        for r in rows_a:
            f.write(f"{r['V_pd']},{r['R_II']},{r['b']}\n")
    with open(os.path.join(WORK, 'sweep_lam.csv'), 'w') as f:
        f.write("lambda,R_II,b\n")
        for r in rows_b:
            f.write(f"{r['lam']},{r['R_II']},{r['b']}\n")

    # plots
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
        Va = [r['V_pd'] for r in rows_a]
        ax[0].plot(Va, [r['R_II'] for r in rows_a], 'o-', label='R_II (loop current)')
        ax[0].plot(Va, [r['b'] for r in rows_a], 's-', label='b (QDW)')
        ax[0].set_xlabel('V_pd'); ax[0].set_ylabel('order parameter')
        ax[0].set_title('(a) sweep V_pd  (lambda=20)'); ax[0].legend(); ax[0].grid(alpha=.3)
        La = [r['lam'] for r in rows_b]
        ax[1].plot(La, [r['R_II'] for r in rows_b], 'o-', label='R_II (loop current)')
        ax[1].plot(La, [r['b'] for r in rows_b], 's-', label='b (QDW)')
        ax[1].set_xlabel('lambda'); ax[1].set_ylabel('order parameter')
        ax[1].set_title('(b) sweep lambda  (V_pd=14)'); ax[1].legend(); ax[1].grid(alpha=.3)
        fig.suptitle('Replication of Fig. 4, arXiv:1506.07172 (competition R_II vs b)')
        fig.tight_layout()
        fig.savefig(os.path.join(WORK, 'fig4_replication.png'), dpi=130)
        print("wrote fig4_replication.png")
    except Exception as e:
        print("plot skipped:", e)

    print("\n== CHECKS ==")
    for k, v in summary['checks'].items():
        print(f"  {k}: {v:+.3f}")
    print("critical:", summary['critical'])
    if ratio is not None:
        print(f"M_LC estimate: {summary['M_LC_estimate_muB']:.3f} muB (paper 0.19)")
    return summary

if __name__ == '__main__':
    main()

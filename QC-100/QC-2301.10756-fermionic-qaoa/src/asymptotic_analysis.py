#!/usr/bin/env python3
"""Asymptotic-regime analysis: at small dt (=Wtilde*dt), both FQAOA and
X-QAOA should lie on approximate power-law lines DeltaE ~ T^{-alpha} in
their respective "quantum adiabatic" limits.  The paper (Fig. 5) reports
alpha~1/2 and a pre-factor gap of ~10^3 between X-QAOA and FQAOA.

Here we sweep p at fixed small dt=0.1 (paper's asymptotic regime) with
larger p to trace the scaling."""

import json
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fqaoa_replication import (
    build_portfolio, brute_force, xqaoa_run, fqaoa_run,
)


def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    outdir.mkdir(parents=True, exist_ok=True)
    prob = build_portfolio(N=6, M=3, lam=0.9, seed=20260703)
    e_min, e_max, W, _, _ = brute_force(prob)
    print(f"E_min={e_min:.6f}  W={W:.6f}")

    dt = 0.1
    p_list = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    rows = []
    for p in p_list:
        rx = xqaoa_run(prob, p=p, dt=dt, A_pen=0.003)
        rf = fqaoa_run(prob, p=p, dt=dt)
        dx = rx["E_expect"] - e_min
        df = rf["E_expect"] - e_min
        dx_feas = rx["E_expect_feas"] - e_min if not np.isnan(rx["E_expect_feas"]) else float("nan")
        df_feas = rf["E_expect_feas"] - e_min
        T = p * dt
        rows.append(dict(p=p, T=T, DeltaE_X=dx, DeltaE_F=df,
                         DeltaE_X_feas=dx_feas, DeltaE_F_feas=df_feas,
                         p_feas_X=rx["p_feasible"], p_feas_F=rf["p_feasible"]))
        print(f"p={p:>4}  T={T:>6.2f}  DE_X={dx:+.5e}  DE_F={df:+.5e}  ratio(X/F)={dx/df:.3f}  "
              f"p_feas_X={rx['p_feasible']:.4f}")

    # Log-log fit for FQAOA at large p (where asymptotic regime kicks in)
    T_arr = np.array([r["T"] for r in rows])
    dF = np.array([r["DeltaE_F"] for r in rows])
    dX = np.array([r["DeltaE_X"] for r in rows])
    dX_feas = np.array([r["DeltaE_X_feas"] for r in rows])
    # Fit last 4 points
    def fit_powerlaw(T, y):
        mask = np.isfinite(y) & (y > 0)
        lt = np.log(T[mask][-4:])
        ly = np.log(y[mask][-4:])
        slope, logA = np.polyfit(lt, ly, 1)
        return slope, np.exp(logA)
    aF, AF = fit_powerlaw(T_arr, dF)
    aX, AX = fit_powerlaw(T_arr, dX)
    aXf, AXf = fit_powerlaw(T_arr, dX_feas)
    print()
    print(f"FQAOA          power law: DeltaE ~ {AF:.4e} * T^({aF:+.3f})")
    print(f"X-QAOA (all)   power law: DeltaE ~ {AX:.4e} * T^({aX:+.3f})")
    print(f"X-QAOA (feas)  power law: DeltaE ~ {AXf:.4e} * T^({aXf:+.3f})")
    print()
    print(f"Pre-factor ratio A_X / A_F (all)  = {AX/AF:.2f}")
    print(f"Pre-factor ratio A_Xf / A_F (feas) = {AXf/AF:.2f}")
    print("(paper reports ~10^3 pre-factor gap at large T in Fig. 5.)")

    out = dict(problem=dict(E_min=e_min, W=W),
               dt=dt, rows=rows,
               fit=dict(FQAOA=dict(alpha=aF, pref=AF),
                        XQAOA=dict(alpha=aX, pref=AX),
                        XQAOA_feas=dict(alpha=aXf, pref=AXf),
                        prefactor_ratio_X_over_F=AX/AF,
                        prefactor_ratio_Xfeas_over_F=AXf/AF))
    with open(outdir / "asymptotic_analysis.json", "w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print(f"[saved] {outdir/'asymptotic_analysis.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Scale up to N=8 (M=4) to match paper's stock count, still D=1 (single-leg).
2^8 = 256, trivially fits in state-vector. Sweep p at small dt to check
asymptotic behavior."""

import json, sys, time
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fqaoa_replication import build_portfolio, brute_force, xqaoa_run, fqaoa_run


def main():
    outdir = Path(__file__).resolve().parent.parent / "report" / "evidence"
    prob = build_portfolio(N=8, M=4, lam=0.9, seed=20260703)
    e_min, e_max, W, x_opt, _ = brute_force(prob)
    print(f"[N=8, M=4] E_min={e_min:.6f}  E_max={e_max:.6f}  W={W:.6f}")
    print(f"optimal x = {x_opt}")

    A_pen = 0.003  # paper
    p_list = [1, 2, 4, 8, 16, 32, 64, 128]
    dt_list = [0.1, 1.0, 5.0]
    all_rows = []
    for dt in dt_list:
        print(f"\n--- dt={dt} ---")
        print(f"{'p':>4} {'T':>8} {'DeltaE_X':>12} {'DeltaE_F':>12} {'X/F':>8} "
              f"{'p_feas_X':>10} {'DeltaE_X_feas':>14}")
        for p in p_list:
            t0 = time.time()
            rx = xqaoa_run(prob, p=p, dt=dt, A_pen=A_pen)
            rf = fqaoa_run(prob, p=p, dt=dt)
            dt_run = time.time() - t0
            dx = rx["E_expect"] - e_min
            df = rf["E_expect"] - e_min
            dxf = rx["E_expect_feas"] - e_min if not np.isnan(rx["E_expect_feas"]) else float("nan")
            T = p * dt
            row = dict(N=8, M=4, p=p, dt=dt, T=T,
                       DeltaE_X=dx, DeltaE_F=df,
                       DeltaE_X_feas=dxf,
                       p_feas_X=rx["p_feasible"], p_feas_F=rf["p_feasible"],
                       wall_s=dt_run)
            all_rows.append(row)
            print(f"{p:>4} {T:>8.3f} {dx:>12.5f} {df:>12.5f} {dx/df:>8.3f} "
                  f"{rx['p_feasible']:>10.4f} {dxf:>14.5f}")

    # Asymptotic fits at dt=0.1
    print("\n=== Power-law fits at dt=0.1 (asymptotic regime, last 4 points) ===")
    rows_dt = [r for r in all_rows if r["dt"] == 0.1]
    T_arr = np.array([r["T"] for r in rows_dt])
    dF = np.array([r["DeltaE_F"] for r in rows_dt])
    dX = np.array([r["DeltaE_X"] for r in rows_dt])
    dXf = np.array([r["DeltaE_X_feas"] for r in rows_dt])

    def fit(T, y):
        mask = np.isfinite(y) & (y > 0)
        lt = np.log(T[mask][-4:]); ly = np.log(y[mask][-4:])
        s, la = np.polyfit(lt, ly, 1)
        return s, np.exp(la)
    aF, AF = fit(T_arr, dF); aX, AX = fit(T_arr, dX); aXf, AXf = fit(T_arr, dXf)
    print(f"FQAOA         : DeltaE ~ {AF:.3e} * T^({aF:+.3f})")
    print(f"X-QAOA (all)  : DeltaE ~ {AX:.3e} * T^({aX:+.3f})")
    print(f"X-QAOA (feas) : DeltaE ~ {AXf:.3e} * T^({aXf:+.3f})")
    print(f"Pre-factor A_X / A_F   = {AX/AF:.3f}")
    print(f"Pre-factor A_Xf / A_F  = {AXf/AF:.3f}")

    out = dict(rows=all_rows,
               fit=dict(FQAOA=dict(alpha=aF, pref=AF),
                        XQAOA=dict(alpha=aX, pref=AX),
                        XQAOA_feas=dict(alpha=aXf, pref=AXf),
                        prefactor_ratio_X_over_F=AX/AF,
                        prefactor_ratio_Xfeas_over_F=AXf/AF))
    with open(outdir/"scale_up_N8.json","w") as f:
        json.dump(out, f, indent=2, default=lambda o: o.tolist() if hasattr(o,"tolist") else str(o))
    print(f"[saved] {outdir/'scale_up_N8.json'}")


if __name__ == "__main__":
    main()

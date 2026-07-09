#!/usr/bin/env python3
"""
Sensitivity-corrected run of the full ODE model with K12 adjusted to a
biologically-plausible gamma-H2AX persistence (~6h half-life, K12=0.111/h),
matching well-established gamma-H2AX kinetics literature. The paper's
printed K12=11.10/h gives a 4-min half-life, which is implausible and yields
near-zero gH2AX peaks in our faithful implementation.

Also produces a side-by-side comparison and a per-claim verification table.
"""
from __future__ import annotations
import json, time, sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import full_ode_model_v2 as M

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
except Exception:
    plt = None


def run_sweep(K12_value, doses_mGy, doses_sweep_mGy=None):
    M.K12 = K12_value
    h2ax_all = {}
    rad51_all = {}
    t_grid = None
    for D_mGy in doses_mGy:
        D_Gy = D_mGy / 1000.0
        t, U_full, N0, _ = M.run_one_dose(D_Gy, t_max=24.0, n_pts=240, cycle_full=True)
        _, U_red, _, _   = M.run_one_dose(D_Gy, t_max=24.0, n_pts=240, cycle_full=False)
        # population-weighted
        W_cycle = 0.55
        W_no = 0.45
        h2ax = W_cycle * M.gamma_h2ax_foci(U_full) + W_no * M.gamma_h2ax_foci(U_red)
        rad51 = W_cycle * M.rad51_foci(U_full)
        h2ax_all[int(D_mGy)] = h2ax
        rad51_all[int(D_mGy)] = rad51
        t_grid = t
    # PHR sweep
    if doses_sweep_mGy is None:
        doses_sweep_mGy = doses_mGy
    PHR_vals = []
    means_h2ax = []
    means_r51 = []
    for D_mGy in doses_sweep_mGy:
        D_Gy = D_mGy / 1000.0
        t, U, N0, _ = M.run_one_dose(D_Gy, t_max=24.0, n_pts=240, cycle_full=True)
        # PHR uses cycling subpop only (HR only happens there)
        h2ax = M.gamma_h2ax_foci(U)
        rad51 = M.rad51_foci(U)
        mh = float(np.trapezoid(h2ax, t) / 24.0)
        mr = float(np.trapezoid(rad51, t) / 24.0)
        PHR_vals.append(100*mr/max(mh,1e-12))
        means_h2ax.append(mh)
        means_r51.append(mr)
    return t_grid, h2ax_all, rad51_all, np.array(doses_sweep_mGy), np.array(PHR_vals), means_h2ax, means_r51


def main():
    here = Path(__file__).resolve().parent
    root = here.parent
    res_dir = root / "results"; res_dir.mkdir(exist_ok=True)
    fig_dir = root / "figures"; fig_dir.mkdir(exist_ok=True)

    doses_mGy = [20, 40, 80, 160, 250, 500, 1000]
    sweep = [5, 10, 20, 40, 60, 80, 120, 160, 200, 250, 300, 400, 500, 600, 700, 800, 900, 1000]

    # As-printed K12=11.10/h
    print(">>> AS-PRINTED run (K12 = 11.10 /h, half-life ~4min)")
    t1, h1, r1, ds1, p1, mh1, mr1 = run_sweep(11.10, doses_mGy, sweep)
    for D, phr in zip(ds1, p1):
        print(f"  D={D:>4} mGy: PHR={phr:.2f}%")

    # Sensitivity-corrected K12=0.111/h
    print("\n>>> SENSITIVITY-CORRECTED run (K12 = 0.111 /h, half-life ~6h)")
    t2, h2, r2, ds2, p2, mh2, mr2 = run_sweep(0.111, doses_mGy, sweep)
    for D, phr in zip(ds2, p2):
        print(f"  D={D:>4} mGy: PHR={phr:.2f}%")

    # PHR ratio metrics
    def metrics(ds, p):
        idx20 = int(np.where(ds==20)[0][0]); idx1000 = int(np.where(ds==1000)[0][0])
        idx250 = int(np.where(ds==250)[0][0]); idx80 = int(np.where(ds==80)[0][0])
        phr_decreasing = sum(np.diff(p) < 0) / max(len(p)-1, 1)
        return {
            "PHR_at_20_mGy": float(p[idx20]),
            "PHR_at_80_mGy": float(p[idx80]),
            "PHR_at_250_mGy": float(p[idx250]),
            "PHR_at_1000_mGy": float(p[idx1000]),
            "PHR_ratio_20_over_1000": float(p[idx20]/max(p[idx1000],1e-9)),
            "PHR_monotonic_decreasing_fraction": float(phr_decreasing),
            "PHR_shape": "monotonic_decreasing" if phr_decreasing >= 0.85 else (
                         "U_shape" if (p[idx250] < p[idx20] and p[idx1000] > p[idx250]) else "other"),
        }

    out = {
        "as_printed": {
            "K12_per_h": 11.10,
            "sweep_dose_mGy": ds1.tolist(),
            "sweep_PHR_percent": p1.tolist(),
            "mean_h2ax_per_cell": mh1,
            "mean_rad51_per_cell": mr1,
            **metrics(ds1, p1),
            "h2ax_peak_per_cell": {int(d): float(np.max(h1[d])) for d in doses_mGy},
            "h2ax_peak_time_h":   {int(d): float(t1[int(np.argmax(h1[d]))]) for d in doses_mGy},
            "h2ax_resid_24h":     {int(d): float(h1[d][-1]) for d in doses_mGy},
            "rad51_peak_per_cell":{int(d): float(np.max(r1[d])) for d in doses_mGy},
            "rad51_peak_time_h":  {int(d): float(t1[int(np.argmax(r1[d]))]) for d in doses_mGy},
            "rad51_resid_24h":    {int(d): float(r1[d][-1]) for d in doses_mGy},
        },
        "sensitivity_corrected": {
            "K12_per_h": 0.111,
            "rationale": "K12=11.10/h gives implausible 4-min gH2AX half-life; literature consensus is ~3-8h half-life",
            "sweep_dose_mGy": ds2.tolist(),
            "sweep_PHR_percent": p2.tolist(),
            "mean_h2ax_per_cell": mh2,
            "mean_rad51_per_cell": mr2,
            **metrics(ds2, p2),
            "h2ax_peak_per_cell": {int(d): float(np.max(h2[d])) for d in doses_mGy},
            "h2ax_peak_time_h":   {int(d): float(t2[int(np.argmax(h2[d]))]) for d in doses_mGy},
            "h2ax_resid_24h":     {int(d): float(h2[d][-1]) for d in doses_mGy},
            "rad51_peak_per_cell":{int(d): float(np.max(r2[d])) for d in doses_mGy},
            "rad51_peak_time_h":  {int(d): float(t2[int(np.argmax(r2[d]))]) for d in doses_mGy},
            "rad51_resid_24h":    {int(d): float(r2[d][-1]) for d in doses_mGy},
        },
        "claim_checks": {
            "paper_claim_PHR_monotonic_decreasing": True,
            "as_printed_PHR_shape": metrics(ds1, p1)["PHR_shape"],
            "sensitivity_corrected_PHR_shape": metrics(ds2, p2)["PHR_shape"],
            "paper_claim_PHR_70pct_at_low_to_15pct_at_1Gy": True,
            "as_printed_PHR_range": [float(np.min(p1)), float(np.max(p1))],
            "sensitivity_corrected_PHR_range": [float(np.min(p2)), float(np.max(p2))],
            "paper_claim_peak_h2ax_shift_at_250_500_mGy": True,
            "as_printed_peak_times_h": {int(d): float(t1[int(np.argmax(h1[d]))]) for d in doses_mGy},
            "sensitivity_corrected_peak_times_h": {int(d): float(t2[int(np.argmax(h2[d]))]) for d in doses_mGy},
        }
    }
    with open(root / "results.json", "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWrote results.json")

    # Save sweep CSVs (overwrite the v2 ones with side-by-side)
    import csv
    with open(res_dir / "ode_PHR_vs_dose.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dose_mGy", "PHR_as_printed_K12_11.10", "PHR_corrected_K12_0.111"])
        for d, pa, pc in zip(ds1, p1, p2):
            w.writerow([int(d), f"{pa:.4f}", f"{pc:.4f}"])
    print(f"Wrote ode_PHR_vs_dose.csv (side-by-side)")

    # Save corrected kinetics
    with open(res_dir / "ode_h2ax_kinetics_corrected.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_h"] + [f"D_{d}_mGy" for d in doses_mGy])
        for i, t in enumerate(t2):
            row = [f"{t:.4f}"] + [f"{h2[d][i]:.5f}" for d in doses_mGy]
            w.writerow(row)
    with open(res_dir / "ode_rad51_kinetics_corrected.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t_h"] + [f"D_{d}_mGy" for d in doses_mGy])
        for i, t in enumerate(t2):
            row = [f"{t:.4f}"] + [f"{r2[d][i]:.5f}" for d in doses_mGy]
            w.writerow(row)
    print(f"Wrote ode_h2ax_kinetics_corrected.csv + rad51 corrected")

    # Plot side-by-side comparison
    if plt is not None:
        fig, axes = plt.subplots(2, 2, figsize=(14, 9))
        # Top-left: gH2AX kinetics, corrected
        for d in doses_mGy:
            axes[0,0].plot(t2, h2[d], label=f"{d} mGy")
        axes[0,0].set_xlabel("Time (h)"); axes[0,0].set_ylabel("gH2AX foci/cell")
        axes[0,0].set_title("gH2AX kinetics (corrected K12=0.111/h)")
        axes[0,0].legend(fontsize=8); axes[0,0].grid(alpha=0.3)

        # Top-right: Rad51 kinetics, corrected
        for d in doses_mGy:
            axes[0,1].plot(t2, r2[d], label=f"{d} mGy")
        axes[0,1].set_xlabel("Time (h)"); axes[0,1].set_ylabel("Rad51 foci/cell")
        axes[0,1].set_title("Rad51 kinetics (corrected)")
        axes[0,1].legend(fontsize=8); axes[0,1].grid(alpha=0.3)

        # Bottom-left: PHR(D) side-by-side
        axes[1,0].plot(ds1, p1, 'o-', label='as-printed K12=11.10/h')
        axes[1,0].plot(ds2, p2, 's-', label='corrected K12=0.111/h')
        axes[1,0].set_yscale('log')
        axes[1,0].set_xlabel("Dose (mGy)"); axes[1,0].set_ylabel("PHR (%)  [log scale]")
        axes[1,0].set_title("PHR(D): as-printed vs corrected")
        axes[1,0].legend(); axes[1,0].grid(alpha=0.3, which='both')

        # Bottom-right: PHR(D) corrected only, linear (compared to paper claim ~70% -> 15%)
        axes[1,1].plot(ds2, p2, 'o-', color='C3', label='corrected K12 model')
        # Paper-claim qualitative band (read from text only - figure values not OCR'd):
        # paper: ~70% at 20 mGy, ~15% at 1000 mGy (qualitative estimate from prior audit + text)
        axes[1,1].plot([20, 1000], [70, 15], 'k--', label='paper qualitative endpoints (text)')
        axes[1,1].set_xlabel("Dose (mGy)"); axes[1,1].set_ylabel("PHR (%)")
        axes[1,1].set_title("PHR(D): corrected model vs paper claim")
        axes[1,1].legend(); axes[1,1].grid(alpha=0.3)
        axes[1,1].set_ylim(0, max(200, float(np.max(p2))*1.1))

        fig.suptitle("Belov 2023 CIMB - full ODE replication: as-printed vs sensitivity-corrected", fontsize=12)
        fig.tight_layout()
        fig.savefig(fig_dir / "ode_full_model.png", dpi=130)
        print(f"Wrote figures/ode_full_model.png")


if __name__ == "__main__":
    main()

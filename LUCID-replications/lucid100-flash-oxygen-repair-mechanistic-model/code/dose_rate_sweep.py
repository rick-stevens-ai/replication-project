"""LUCID-100 audit extension — dose-rate transition sweep.

Re-uses the dynamic UNIVERSE smoke implementation in `flash_oxygen_smoke.py`
to map surviving fraction (SF) and sparing factor (SF_FLASH/SF_CONV-equivalent)
across a wide dose-rate range at fixed dose and fixed initial [O2].
Goal: explicitly localize where the FLASH transition (if any) occurs in this
parameter-free smoke and report the maximum sparing factor + dose-rate at which
it appears.

This is an AUDIT artifact, not a paper figure: it answers the question
"does our smoke reproduce a dose-rate-dependent SF curve (as the paper claims),
and if so what is its shape?".

Output:
  results/dose_rate_sweep.csv        # (dose_rate, [O2]_0, mean SF, std, mean DSB)
  figures/dose_rate_sweep.png        # SF vs log10(dose_rate) at 0.5%, 4%, 7.5% O2
  logs/dose_rate_sweep.log           # run summary
"""
from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location("fos", os.path.join(HERE, "flash_oxygen_smoke.py"))
fos = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fos)


def main() -> None:
    t0 = time.time()
    rng = np.random.default_rng(20210104)

    dose_Gy = 10.0
    dose_rates = np.logspace(-1, 3, 9)  # 0.1, 0.316, 1, 3.16, 10, 31.6, 100, 316, 1000 Gy/s
    o2_levels_pct = [0.5, 4.0, 7.5]
    n_iter = 1500  # smaller than main smoke (4000) — sweep has 27 conditions

    rows = []
    for o2 in o2_levels_pct:
        for r in dose_rates:
            res = fos.survival_dynamic(
                total_dose_Gy=dose_Gy,
                dose_rate_Gy_per_s=float(r),
                o2_initial_percent=float(o2),
                n_iter=n_iter,
                n_steps=100,
                rng=np.random.default_rng(int(20210104 + 1e3 * r + 1e6 * o2)),
            )
            rows.append({
                "dose_Gy": dose_Gy,
                "o2_initial_pct": o2,
                "dose_rate_Gy_per_s": float(r),
                "SF_mean": res["SF_mean"],
                "SF_std": res["SF_std"],
                "mean_total_DSB": res["mean_total_DSB"],
                "o2_min_pct_during_irrad": res["o2_min_pct"],
                "T_irr_s": res["T_irr_s"],
            })
            print(f"  O2={o2:>5.2f}%  R={r:>8.3f} Gy/s  T_irr={res['T_irr_s']:.4g} s  "
                  f"SF={res['SF_mean']:.4f}  meanDSB={res['mean_total_DSB']:.1f}  "
                  f"O2_min={res['o2_min_pct']:.3f}%")

    # write CSV
    out_csv = os.path.join(ROOT, "results", "dose_rate_sweep.csv")
    fieldnames = list(rows[0].keys())
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    # plot
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for o2 in o2_levels_pct:
        sub = [r for r in rows if r["o2_initial_pct"] == o2]
        sub.sort(key=lambda x: x["dose_rate_Gy_per_s"])
        x = [r["dose_rate_Gy_per_s"] for r in sub]
        y = [r["SF_mean"] for r in sub]
        yerr = [r["SF_std"] / np.sqrt(n_iter) for r in sub]  # SEM
        ax.errorbar(x, y, yerr=yerr, marker="o", label=f"[O2]_0 = {o2}%", capsize=3)
    ax.set_xscale("log")
    ax.set_xlabel("Dose rate (Gy/s)")
    ax.set_ylabel("Surviving fraction (mean ± SEM)")
    ax.set_title(f"Dynamic UNIVERSE smoke: SF vs dose rate at D = {dose_Gy} Gy\n"
                 "(literature-bound g_ROD=0.42 mmHg/Gy, tau_reox=5 s)")
    ax.axvspan(0.03, 0.5, alpha=0.1, color="gray", label="CONV range")
    ax.axvspan(40, 1000, alpha=0.1, color="orange", label="FLASH range")
    ax.legend(fontsize=8)
    ax.grid(True, which="both", linestyle=":", alpha=0.4)
    fig.tight_layout()
    out_fig = os.path.join(ROOT, "figures", "dose_rate_sweep.png")
    fig.savefig(out_fig, dpi=140)
    plt.close(fig)

    elapsed = time.time() - t0
    # max sparing factor (SF_high_rate / SF_low_rate) per O2 level
    summary = {}
    for o2 in o2_levels_pct:
        sub = sorted([r for r in rows if r["o2_initial_pct"] == o2],
                     key=lambda x: x["dose_rate_Gy_per_s"])
        sf_lo = sub[0]["SF_mean"]
        sf_hi = sub[-1]["SF_mean"]
        spar = sf_hi / sf_lo if sf_lo > 0 else float("nan")
        sf_max = max(s["SF_mean"] for s in sub)
        r_at_max = next(s["dose_rate_Gy_per_s"] for s in sub if s["SF_mean"] == sf_max)
        summary[f"O2_{o2}pct"] = {
            "SF_at_lowest_rate": sf_lo,
            "SF_at_highest_rate": sf_hi,
            "SF_high_over_SF_low": spar,
            "SF_max": sf_max,
            "dose_rate_at_SF_max": r_at_max,
        }
    log = {
        "elapsed_s": elapsed,
        "n_conditions": len(rows),
        "n_iter_per_condition": n_iter,
        "dose_Gy": dose_Gy,
        "dose_rates_Gy_per_s": list(dose_rates),
        "o2_levels_pct": o2_levels_pct,
        "summary_by_o2": summary,
        "outputs": {"csv": out_csv, "figure": out_fig},
    }
    out_log = os.path.join(ROOT, "logs", "dose_rate_sweep.log")
    with open(out_log, "w") as f:
        json.dump(log, f, indent=2)
    print(json.dumps(summary, indent=2))
    print(f"Done in {elapsed:.1f} s. CSV: {out_csv}; figure: {out_fig}")


if __name__ == "__main__":
    main()

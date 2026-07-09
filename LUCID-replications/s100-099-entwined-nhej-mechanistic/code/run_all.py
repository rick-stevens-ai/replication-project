"""Run all four scenarios x three cell systems, write figures + GoF table.

Outputs (relative to project root):
  evidence/results.json         per-scenario per-system trajectories + GoF
  evidence/gof_table.csv        replication of Table 1
  figures/fig3_replication.png  replication of Fig 3 (b)(c)(d)
"""
from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from simulate import run_scenario, goodness_of_fit
from beucher_data import TIMES_H, BEUCHER, BEUCHER_SEM

SCENARIOS = ["A", "B", "C", "D"]
SYS_MAP = {"HF_WT": "WT", "MEF_WT": "WT", "XLF": "XLF", "Lig4": "Lig4"}
COLOURS = {"A": "tab:red", "B": "tab:orange", "C": "tab:green", "D": "tab:purple"}


def main(n_dsb: int = 70, n_repeats: int = 40, t_end_h: float = 8.0,
         seed_base: int = 42) -> None:
    results = {}
    # Run unique (scenario, cell-system) combinations
    sys_keys = ["HF_WT", "MEF_WT", "XLF", "Lig4"]
    for sc in SCENARIOS:
        results[sc] = {}
        for cell in sys_keys:
            deficiency = SYS_MAP[cell]
            # Use distinct seeds for HF_WT vs MEF_WT so the two WT lines differ
            seed = seed_base + hash((sc, cell)) % 10000
            out = run_scenario(sc, deficiency,
                               n_dsb=n_dsb, n_repeats=n_repeats,
                               t_end_h=t_end_h, seed=seed)
            gof = goodness_of_fit(out["times_h"], out["residual_norm"],
                                  TIMES_H, BEUCHER[cell], BEUCHER_SEM[cell])
            results[sc][cell] = {
                "times_h": out["times_h"].tolist(),
                "residual_norm_mean": out["residual_norm"].tolist(),
                "residual_norm_sem": out["residual_norm_sem"].tolist(),
                "fraction_NHEJ": out["fraction_NHEJ"],
                "fraction_HR": out["fraction_HR"],
                "fraction_unrepaired": out["fraction_unrepaired"],
                "goodness_of_fit": gof,
            }
            print(f"  {sc} {cell:>7s}: fNHEJ={out['fraction_NHEJ']:.2f} "
                  f"fHR={out['fraction_HR']:.2f} "
                  f"fU={out['fraction_unrepaired']:.2f}  "
                  f"χ²ᵣ={gof['reduced_chi2']:6.2f}  RMSE={gof['rmse']:6.2f}")

    # Write results.json
    out_json = ROOT / "evidence" / "results.json"
    out_json.write_text(json.dumps(results, indent=2))
    print(f"wrote {out_json}")

    # Write goodness-of-fit table (replication of Table 1)
    out_csv = ROOT / "evidence" / "gof_table.csv"
    with open(out_csv, "w", newline="") as fh:
        wr = csv.writer(fh)
        wr.writerow(["scenario", "system", "reduced_chi2", "rmse"])
        per_scenario_means: dict[str, list[tuple[float, float]]] = {}
        for sc in SCENARIOS:
            per_scenario_means[sc] = []
            for cell in sys_keys:
                gof = results[sc][cell]["goodness_of_fit"]
                wr.writerow([sc, cell, f"{gof['reduced_chi2']:.2f}",
                             f"{gof['rmse']:.2f}"])
                per_scenario_means[sc].append((gof["reduced_chi2"], gof["rmse"]))
            arr = np.array(per_scenario_means[sc])
            wr.writerow([sc, "AVG", f"{arr[:, 0].mean():.2f}",
                         f"{arr[:, 1].mean():.2f}"])
    print(f"wrote {out_csv}")

    # Figure 3 replication: WT, XLF, Lig4 panels
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=True)
    panel_systems = {
        "Wild-Type": ["HF_WT", "MEF_WT"],
        "XLF-deficient": ["XLF"],
        "Lig4-deficient": ["Lig4"],
    }
    for ax, (title, cells) in zip(axes, panel_systems.items()):
        for sc in SCENARIOS:
            # Plot WT mean as average of HF_WT and MEF_WT, else just the cell
            if len(cells) > 1:
                ys = np.mean(
                    [results[sc][c]["residual_norm_mean"] for c in cells],
                    axis=0,
                )
            else:
                ys = np.array(results[sc][cells[0]]["residual_norm_mean"])
            t = np.array(results[sc][cells[0]]["times_h"])
            ax.plot(t, ys, "-", color=COLOURS[sc], lw=2,
                    label=f"Scenario {sc}")
        for c in cells:
            ax.errorbar(TIMES_H, BEUCHER[c], yerr=BEUCHER_SEM[c],
                        fmt="ks", markersize=6, capsize=3,
                        label=f"Beucher {c}")
        ax.set_xlim(0, 8.5)
        ax.set_ylim(0, 1.05)
        ax.set_xlabel("Time post-irradiation (h)")
        ax.set_title(title)
        ax.legend(fontsize=7, loc="upper right")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel(r"Residual $\gamma$-H2AX foci (norm. to 0.5 h)")
    fig.suptitle("Replication of Ingram et al. 2019 Fig. 3 — "
                 "DaMaRiS Scenarios A–D vs Beucher 2009 data")
    fig.tight_layout()
    fig_path = ROOT / "figures" / "fig3_replication.png"
    fig.savefig(fig_path, dpi=140)
    plt.close(fig)
    print(f"wrote {fig_path}")

    # GoF bar chart (mean χ²ᵣ per scenario) — replication of Table 1 means
    fig2, ax = plt.subplots(figsize=(6, 4))
    means = [np.mean([results[sc][c]["goodness_of_fit"]["reduced_chi2"]
                      for c in sys_keys]) for sc in SCENARIOS]
    bars = ax.bar(SCENARIOS, means, color=[COLOURS[s] for s in SCENARIOS])
    ax.set_ylabel(r"Mean reduced $\chi^2$ (across 4 cell systems)")
    ax.set_xlabel("Scenario")
    ax.set_title("Replication of Table 1 — model-comparison summary")
    for b, m in zip(bars, means):
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.1,
                f"{m:.2f}", ha="center", fontsize=10)
    fig2.tight_layout()
    fig2_path = ROOT / "figures" / "fig_table1_replication.png"
    fig2.savefig(fig2_path, dpi=140)
    plt.close(fig2)
    print(f"wrote {fig2_path}")

    # Repair-pathway split bar chart for WT
    fig3, ax = plt.subplots(figsize=(6, 4))
    fNH = [results[sc]["HF_WT"]["fraction_NHEJ"] for sc in SCENARIOS]
    fHR = [results[sc]["HF_WT"]["fraction_HR"] for sc in SCENARIOS]
    fU = [results[sc]["HF_WT"]["fraction_unrepaired"] for sc in SCENARIOS]
    x = np.arange(len(SCENARIOS))
    ax.bar(x, fNH, label="NHEJ", color="goldenrod")
    ax.bar(x, fHR, bottom=fNH, label="HR", color="firebrick")
    ax.bar(x, fU, bottom=np.array(fNH) + np.array(fHR),
           label="Unrepaired", color="grey")
    ax.set_xticks(x)
    ax.set_xticklabels(SCENARIOS)
    ax.set_ylabel("Fraction of DSBs at t = 8 h")
    ax.set_xlabel("Scenario")
    ax.set_title("Repair-pathway split (WT human fibroblasts)")
    ax.legend()
    fig3.tight_layout()
    fig3_path = ROOT / "figures" / "fig_pathway_split.png"
    fig3.savefig(fig3_path, dpi=140)
    plt.close(fig3)
    print(f"wrote {fig3_path}")


if __name__ == "__main__":
    main()

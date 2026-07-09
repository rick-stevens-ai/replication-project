"""Run the LUCID replication experiments and produce figures.

Reproduces qualitative features of LUCID's Figure 4 (deterministic dynamics
of the p53 system for 2 / 4 / 8 Gy and two ATM Hill thresholds), Figure 5
(TGFβ secretion), and Figure 6 (apoptosis surrogate from Bax).
"""
from __future__ import annotations
import os
import json
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from p53_model import simulate, SPECIES, IDX


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG  = os.path.join(ROOT, "figures")
LOG  = os.path.join(ROOT, "logs")
RES  = os.path.join(ROOT, "results")
os.makedirs(FIG, exist_ok=True)
os.makedirs(LOG, exist_ok=True)
os.makedirs(RES, exist_ok=True)


def fig4_time_courses(doses=(2.0, 4.0, 8.0), M_Gy=0.5, t_end_h=72.0,
                      tag="M0p5") -> dict:
    """Reproduces LUCID Fig 4 layout: ATMp, p53_ARR, p53_KILL, Mdm2, Wip1,
    p21, Bax for each dose."""
    summary = {"M_Gy": M_Gy, "doses": list(doses), "tag": tag, "peaks": {}}
    fig, axes = plt.subplots(len(doses), 4, figsize=(15, 3.4 * len(doses)),
                             sharex=True)
    obs_groups = [
        ("Damage / ATM",        ["DSB", "ATMp"],                ["DSB count", "active ATM"]),
        ("p53 phosphoforms",    ["p53_ARR", "p53_KILL"],        ["p53_ARRESTER", "p53_KILLER"]),
        ("Negative regulators", ["Mdm2nuc_2p", "Wip1"],         ["Mdm2_nuclear", "Wip1"]),
        ("Downstream",          ["p21", "Bax", "TGFb"],         ["p21", "Bax", "TGFβ"]),
    ]
    for r, dose in enumerate(doses):
        t, y, names = simulate(dose, M_Gy=M_Gy, t_end_h=t_end_h, n_points=2000)
        summary["peaks"][f"{dose}Gy"] = {
            n: float(y[IDX[n]].max()) for n in
            ["DSB","ATMp","p53_ARR","p53_KILL","Mdm2nuc_2p","Wip1","p21","Bax","TGFb"]
        }
        for c, (title, sp_list, labels) in enumerate(obs_groups):
            ax = axes[r, c]
            for sp, lab in zip(sp_list, labels):
                vals = y[IDX[sp]]
                # use log scale for variables spanning orders of magnitude
                ax.plot(t, np.maximum(vals, 1e-2), label=lab, linewidth=1.4)
            ax.set_yscale("log")
            ax.set_xlim(0, t_end_h)
            ax.grid(True, alpha=0.3)
            if r == 0:
                ax.set_title(title)
            if r == len(doses) - 1:
                ax.set_xlabel("time (h)")
            if c == 0:
                ax.set_ylabel(f"{dose} Gy  (molecules)")
            ax.legend(fontsize=8, loc="best")
    fig.suptitle(f"LUCID Fig 4 replication — M = {M_Gy} Gy (ATM Hill threshold)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    path = os.path.join(FIG, f"fig4_timecourses_{tag}.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  wrote {path}")
    return summary


def fig5_TGFb_secretion(doses=(2.0, 4.0, 6.0, 8.0), M_Gy=0.5, t_end_h=72.0):
    """LUCID Fig 5 analog: TGFβ accumulation vs dose."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    peaks = {}
    for d in doses:
        t, y, names = simulate(d, M_Gy=M_Gy, t_end_h=t_end_h, n_points=1200)
        ax.plot(t, y[IDX["TGFb"]], label=f"{d} Gy", linewidth=1.6)
        peaks[d] = float(y[IDX["TGFb"]][-1])
    ax.set_xlabel("time (h)")
    ax.set_ylabel("TGFβ (molecules; arbitrary scale)")
    ax.set_title("LUCID Fig 5 replication — TGFβ secretion vs dose")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(FIG, "fig5_TGFb_vs_dose.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  wrote {path}")
    return peaks


def fig6_apoptosis_surrogate(doses=(2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0)):
    """LUCID Fig 6 analog: deterministic Bax/AKTp ratio at 72 h vs dose,
    for two ATM thresholds M (0.14 vs 0.5 Gy). Apoptosis in LUCID is
    a Bogdał-style stochastic gate; in this deterministic surrogate we
    report the Bax/AKTp ratio (= rough apoptotic propensity).
    """
    fig, ax = plt.subplots(figsize=(7, 4.5))
    out = {}
    for M_Gy, ls in [(0.14, "-o"), (0.5, "--s")]:
        ratios = []
        for d in doses:
            t, y, _ = simulate(d, M_Gy=M_Gy, t_end_h=72.0, n_points=200)
            r = y[IDX["Bax"]][-1] / max(y[IDX["AKTp"]][-1], 1.0)
            ratios.append(r)
        out[M_Gy] = dict(zip(doses, ratios))
        ax.plot(doses, ratios, ls, label=f"M = {M_Gy} Gy")
    ax.set_xlabel("Dose (Gy)")
    ax.set_ylabel("Bax / AKTp  at 72 h  (apoptotic propensity)")
    ax.set_title("LUCID Fig 6 surrogate — apoptotic readout vs dose")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    path = os.path.join(FIG, "fig6_apoptosis_surrogate.png")
    fig.savefig(path, dpi=130)
    plt.close(fig)
    print(f"  wrote {path}")
    return out


def main():
    t0 = time.time()
    print("Running LUCID p53 replication experiments…")
    summaries = {
        "M0p5":  fig4_time_courses(M_Gy=0.5,  tag="M0p5"),
        "M0p14": fig4_time_courses(M_Gy=0.14, tag="M0p14"),
    }
    summaries["fig5_TGFb"]   = fig5_TGFb_secretion()
    summaries["fig6_apopt"]  = fig6_apoptosis_surrogate()
    summaries["wallclock_s"] = time.time() - t0

    with open(os.path.join(RES, "summary.json"), "w") as fh:
        json.dump(summaries, fh, indent=2, default=str)
    print(f"\nDone in {summaries['wallclock_s']:.1f} s. "
          f"Summary -> {os.path.join(RES, 'summary.json')}")


if __name__ == "__main__":
    main()

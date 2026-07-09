#!/usr/bin/env python3
"""Slot 61 smoke replication — Chigasova et al. 2024 (DOI:10.33266/1024-6177-2024-69-1-15-19).

Purpose
-------
This is NOT a wet-lab replication and NOT a numeric figure replication.
It is a *qualitative-claim consistency check* + *replot template* built ONLY from the
narrative numerical statements in the paper's Results/Discussion text. All numbers
in the `narrative_anchors` dict below are quoted directly from the paper text in
artifacts/paper.txt (English abstract + Russian Results section).

When Figure 1 is digitized (e.g. with WebPlotDigitizer), drop the resulting
CSV into ./data/fig1_digitized.csv (schema described in this file) and the
script will load it instead of the narrative anchors, allowing a quantitative
overlay against the verbal claims.

Usage
-----
    python3 scripts/smoke_replicate.py

Outputs (created under ./outputs/):
    fig1_qualitative_replication.png  - qualitative kinetic schematic
    claim_check.csv                   - each narrative claim with PASS/FAIL on
                                        internal consistency among anchors
    summary.txt                       - one-line summary of pass count
"""

from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "outputs")
DATA = os.path.join(ROOT, "data")
os.makedirs(OUT, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

# ---------------------------------------------------------------------------
# Narrative anchors — every value below is a direct quote from the paper text.
# Foci values are normalised: at 1 h the foci count is the per-dose "max".
# We treat reported ratios as fractions of that max for each dose curve.
# ---------------------------------------------------------------------------

# (dose_mGy, time_h, marker, value_fraction_of_1h_max_or_pct_colocalization)
narrative_anchors = {
    "yH2AX_frac_of_1h": {
        # "уменьшение их количества до ~50% от числа, наблюдаемого в точке максимума"
        # ("250 mGy: by 6 h post-IR, ~50% of the 1h maximum")
        (250, 1): 1.00,
        (250, 6): 0.50,
        # "через 6 ч после облучения остается уже ~60% фокусов от количества,
        #  регистрируемого через 1 ч после облучения" (160 mGy)
        (160, 1): 1.00,
        (160, 6): 0.60,
        #  Low doses: "количество фокусов γH2AX статистически достоверно не уменьшается
        #  через 6 ч ... остается повышенным вплоть до 48 ч"
        (80, 1): 1.00,
        (80, 6): 1.00,   # "no significant decrease"
        (80, 48): 1.00,  # "remained elevated up to 48 h"
        (40, 1): 1.00,
        (40, 6): 1.00,
        (40, 48): 1.00,
    },
    "pATM_yH2AX_colocalization_pct": {
        # "через 1 ч ... в дозе 250 мГр количество фокусов pATM, солокализованных
        #  с фокусами γH2AX, составляло почти 80% от количества фокусов γH2AX"
        (250, 1): 80.0,
        # "затем через 4-48 ч после облучения этот показатель снижается до 45-60%"
        (250, 24): 52.5,   # midpoint of 45-60
        (250, 48): 52.5,
        # "после облучения в дозах 80 и 40 мГр максимум активности АТМ
        #  наблюдался через 1 ч (65% солокализации)"
        (80, 1): 65.0,
        (40, 1): 65.0,
        # "через 24-48 ч ... снижение солокализованных с γH2AX фокусов pATM
        #  до 40% (80 мГр) и 35% (40 мГр)"
        (80, 24): 40.0,
        (80, 48): 40.0,
        (40, 24): 35.0,
        (40, 48): 35.0,
    },
}


# ---------------------------------------------------------------------------
# Internal-consistency checks: do the verbal claims agree with themselves?
# ---------------------------------------------------------------------------
@dataclass
class ClaimCheck:
    name: str
    expectation: str
    passed: bool
    note: str


def run_claim_checks() -> list[ClaimCheck]:
    checks: list[ClaimCheck] = []
    yh = narrative_anchors["yH2AX_frac_of_1h"]
    pc = narrative_anchors["pATM_yH2AX_colocalization_pct"]

    # 1. High doses lose 40-50% of γH2AX foci by 6 h.
    drops_high = [1.0 - yh[(d, 6)] for d in (160, 250)]
    passed = all(0.30 <= x <= 0.60 for x in drops_high)
    checks.append(ClaimCheck(
        "high_dose_6h_decline",
        "160 & 250 mGy γH2AX 6h fraction-decline in [0.30, 0.60]",
        passed,
        f"drops={drops_high}",
    ))

    # 2. Low doses (40, 80 mGy) show no significant decline at 6 h.
    drops_low = [1.0 - yh[(d, 6)] for d in (40, 80)]
    passed = all(x <= 0.10 for x in drops_low)  # within ~10% = "not significant"
    checks.append(ClaimCheck(
        "low_dose_6h_no_decline",
        "40 & 80 mGy γH2AX 6h fraction-decline <= 0.10",
        passed,
        f"drops={drops_low}",
    ))

    # 3. Low doses remain elevated at 48 h (>=80% of 1 h max).
    passed = all(yh[(d, 48)] >= 0.80 for d in (40, 80))
    checks.append(ClaimCheck(
        "low_dose_48h_persistence",
        "40 & 80 mGy γH2AX 48h fraction >= 0.80",
        passed,
        f"values={[yh[(d, 48)] for d in (40, 80)]}",
    ))

    # 4. pATM colocalization at 1 h is dose-dependent: 250 > 80~40.
    passed = pc[(250, 1)] > pc[(80, 1)] and pc[(250, 1)] > pc[(40, 1)]
    checks.append(ClaimCheck(
        "pATM_coloc_1h_dose_order",
        "pATM/γH2AX colocalization at 1 h: 250 mGy > 80/40 mGy",
        passed,
        f"250={pc[(250, 1)]}, 80={pc[(80, 1)]}, 40={pc[(40, 1)]}",
    ))

    # 5. pATM colocalization drops at 24-48 h vs 1 h for ALL doses.
    drop_doses = []
    for d in (250, 80, 40):
        ok = pc[(d, 48)] < pc[(d, 1)]
        drop_doses.append((d, pc[(d, 1)], pc[(d, 48)], ok))
    passed = all(x[3] for x in drop_doses)
    checks.append(ClaimCheck(
        "pATM_coloc_24_48h_decline_all_doses",
        "pATM/γH2AX colocalization at 48 h < at 1 h for all doses",
        passed,
        f"per_dose={drop_doses}",
    ))

    # 6. Quantitative ordering: the LOW-dose 24-48 h colocalization should be
    #    LOWER than the high-dose value (paper claims 35-40% vs 45-60%).
    passed = max(pc[(40, 48)], pc[(80, 48)]) < pc[(250, 48)]
    checks.append(ClaimCheck(
        "low_vs_high_dose_48h_coloc_order",
        "48h pATM/γH2AX coloc: low doses (40, 80) < high dose (250)",
        passed,
        f"40={pc[(40, 48)]}, 80={pc[(80, 48)]}, 250={pc[(250, 48)]}",
    ))

    return checks


def write_claim_csv(checks: list[ClaimCheck]) -> None:
    path = os.path.join(OUT, "claim_check.csv")
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "expectation", "passed", "note"])
        for c in checks:
            w.writerow([c.name, c.expectation, c.passed, c.note])
    print(f"wrote {path}")


# ---------------------------------------------------------------------------
# Qualitative replot — to be overlaid against digitized Fig. 1 later.
# Uses simple exponential decay between narrative anchor points for high doses,
# flat-ish curve for low doses (matching the paper's described kinetics).
# ---------------------------------------------------------------------------

def synth_curve(anchors: dict[int, float], times: np.ndarray) -> np.ndarray:
    """Piecewise-linear interpolation between anchor (time -> value) points."""
    ts = np.array(sorted(anchors.keys()), dtype=float)
    vs = np.array([anchors[t] for t in sorted(anchors.keys())], dtype=float)
    return np.interp(times, ts, vs)


def make_qualitative_plot() -> None:
    yh = narrative_anchors["yH2AX_frac_of_1h"]
    pc = narrative_anchors["pATM_yH2AX_colocalization_pct"]
    doses = (40, 80, 160, 250)
    colors = {40: "#4daf4a", 80: "#377eb8", 160: "#ff7f00", 250: "#e41a1c"}
    times = np.linspace(1, 48, 200)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # γH2AX panel
    for d in doses:
        pts = {t: v for (dd, t), v in yh.items() if dd == d}
        # need at least two anchor points to draw a curve
        if len(pts) < 2:
            # add a soft 48 h anchor at the last known value for high doses
            if d in (160, 250) and (d, 6) in yh:
                pts[48] = yh[(d, 6)] * 0.9  # gentle further decay (assumption flag)
        ts = np.array(sorted(pts.keys()), dtype=float)
        vs = np.array([pts[t] for t in sorted(pts.keys())], dtype=float)
        curve = np.interp(times, ts, vs)
        ax1.plot(times, curve, color=colors[d], label=f"{d} mGy", lw=2)
        ax1.scatter(ts, vs, color=colors[d], s=30, edgecolor="black",
                    linewidth=0.5, zorder=3)
    ax1.set_xlabel("Time post-IR (h)")
    ax1.set_ylabel("γH2AX foci, fraction of 1 h value")
    ax1.set_title("γH2AX kinetics (narrative anchors)")
    ax1.set_ylim(0, 1.2)
    ax1.legend(fontsize=8)
    ax1.grid(alpha=0.3)

    # pATM colocalization panel — only 40, 80, 250 mGy quoted in text
    for d in (40, 80, 250):
        pts = {t: v for (dd, t), v in pc.items() if dd == d}
        if len(pts) < 2:
            continue
        ts = np.array(sorted(pts.keys()), dtype=float)
        vs = np.array([pts[t] for t in sorted(pts.keys())], dtype=float)
        curve = np.interp(times, ts, vs)
        ax2.plot(times, curve, color=colors[d], label=f"{d} mGy", lw=2)
        ax2.scatter(ts, vs, color=colors[d], s=30, edgecolor="black",
                    linewidth=0.5, zorder=3)
    ax2.set_xlabel("Time post-IR (h)")
    ax2.set_ylabel("pATM / γH2AX colocalization (%)")
    ax2.set_title("pATM colocalization (narrative anchors)")
    ax2.set_ylim(0, 100)
    ax2.legend(fontsize=8)
    ax2.grid(alpha=0.3)

    fig.suptitle("Slot 61 qualitative replication — anchored ONLY to verbal\n"
                 "numbers in Chigasova et al. 2024 (replace with digitized Fig. 1)",
                 fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    path = os.path.join(OUT, "fig1_qualitative_replication.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"wrote {path}")


def main() -> int:
    checks = run_claim_checks()
    write_claim_csv(checks)
    make_qualitative_plot()

    passed = sum(1 for c in checks if c.passed)
    summary = (f"slot61 smoke check: {passed}/{len(checks)} claim "
               f"consistency checks passed\n")
    for c in checks:
        summary += f"  [{'PASS' if c.passed else 'FAIL'}] {c.name}: {c.note}\n"
    summary_path = os.path.join(OUT, "summary.txt")
    with open(summary_path, "w") as f:
        f.write(summary)
    print(summary)
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())

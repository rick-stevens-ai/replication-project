#!/usr/bin/env python3
"""
Reproduce / tabulate the in vitro GI50 (CCK-8, 24 h) values reported in
Park et al. 2024 §"Effects of DDR modulators on radiation exposure"
and compute therapeutic-index ratios that the paper *implies* but does not
print directly. These ratios let us audit C7 (BML-277 most effective
radioprotector) at the level of dose×selectivity arithmetic.

The numerator GI50 values are paper-reported; we do NOT have raw CCK-8
curves to refit, so this is a transcription-and-arithmetic audit, not a
re-derivation.  All ratios are within-paper-consistent.

Run:  python3 scripts/gi50_summary.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# GI50 values (µM) verbatim from Results §"Effects of DDR modulators on
# radiation exposure" of PMC11093554 (cross-checked against claims.md C6).
GI50_uM: dict[str, dict[str, float]] = {
    "KU60019":    {"IM-9": 3.28,  "HuT78": 4.65,  "target": "ATM-i"},
    "BML-277":    {"IM-9": 13.45, "HuT78": 13.40, "target": "CHK2-i"},
    "pifithrin-a":{"IM-9": 97.28, "HuT78": 110.6, "target": "p53-i"},
    "nutlin-3a":  {"IM-9": 38.77, "HuT78": 64.38, "target": "p53-a"},
}

# Working / sub-toxic dose used in downstream IR-protection assays
# (also from Fig 3 legend / Results text).
WORKING_DOSE_uM = {
    "KU60019":     2.5,
    "BML-277":     2.5,
    "pifithrin-a": 5.0,
    "nutlin-3a":  10.0,
}


def main() -> int:
    rows = []
    print(f"{'compound':<14}{'target':<8}{'GI50 IM-9':>11}{'GI50 HuT78':>13}"
          f"{'workdose':>10}{'IM9 margin':>13}{'HuT78 margin':>15}")
    for cpd, d in GI50_uM.items():
        wd = WORKING_DOSE_uM[cpd]
        m_im9 = d["IM-9"] / wd
        m_hut = d["HuT78"] / wd
        rows.append({
            "compound": cpd,
            "target": d["target"],
            "GI50_IM9_uM": d["IM-9"],
            "GI50_HuT78_uM": d["HuT78"],
            "working_dose_uM": wd,
            "IM9_safety_margin": round(m_im9, 2),
            "HuT78_safety_margin": round(m_hut, 2),
        })
        print(f"{cpd:<14}{d['target']:<8}{d['IM-9']:>11.2f}{d['HuT78']:>13.2f}"
              f"{wd:>10.2f}{m_im9:>13.2f}{m_hut:>15.2f}")

    # Sanity assertions that document paper-internal consistency.
    # Margin >= 1.0 => working dose below half-maximal growth inhibition.
    bad = [r for r in rows if r["IM9_safety_margin"] < 1.0 or r["HuT78_safety_margin"] < 1.0]
    if bad:
        print("\nFAIL — working dose >= GI50 in at least one cell line:")
        for r in bad:
            print(f"   {r}")
        return 1

    # BML-277 vs KU60019: both at 2.5 µM, but BML-277 GI50 is ~4x higher,
    # so BML-277 is the safer of the two ATM/CHK2-axis inhibitors. The
    # paper's C7 claim ("BML-277 most effective radioprotector") is therefore
    # at least *consistent* with a wider therapeutic window in IM-9; the
    # downstream apoptosis attenuation in Fig 4 is the actual efficacy
    # claim and is not re-derivable here.
    bml = next(r for r in rows if r["compound"] == "BML-277")
    ku  = next(r for r in rows if r["compound"] == "KU60019")
    assert bml["IM9_safety_margin"] > ku["IM9_safety_margin"], "BML-277 should have wider margin than KU60019 in IM-9"

    out = Path(__file__).resolve().parent.parent / "results" / "gi50_summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rows, indent=2))
    print(f"\nWrote {out}")
    print("\nPASS — GI50 / working-dose arithmetic consistent.")
    print(f"  BML-277 safety margin (IM-9) = {bml['IM9_safety_margin']:.2f}× "
          f"vs KU60019 = {ku['IM9_safety_margin']:.2f}× → consistent with C7 "
          "wider therapeutic window.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

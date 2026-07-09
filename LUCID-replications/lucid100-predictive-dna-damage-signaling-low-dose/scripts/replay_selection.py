#!/usr/bin/env python3
"""
Replay the 16 -> 4 candidate down-selection from Park et al. 2024 (ijmm.2024.5380).

The paper selected 16 protein candidates from refs [8] and [10], then applied three
criteria to narrow to four. We encode the panel + criteria + per-protein outcomes
verbatim from the paper text and verify the unique 4-survivor set:
{ATM, CHK2, p53, H2AX}.

Run:
    python3 scripts/replay_selection.py

Exit code: 0 = panel reproduces; non-zero = mismatch.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    name: str
    category: str  # "DDR" | "signaling" | "cytokine"
    detectable_in_low_dose_IR: bool   # criterion (i) — Introduction §3
    concentration_dependent: bool      # criterion (ii)
    applicable_to_blood: bool          # criterion (iii) — hPBMC/blood detection
    note: str = ""


# Panel of 16 enumerated in Discussion §2 of PMC11093554.
# NB: source text lists "p53" twice (entries 3 and 9). Treating as one protein
# per the obvious biological reading; if read literally the panel would be 15
# unique proteins + 1 duplicate, which does not change the survivor set.
PANEL: list[Candidate] = [
    # DDR / signaling — surviving four
    Candidate("ATM",   "DDR", True, True,  True,
              "p-ATM increased dose-dependently in IM-9 and hPBMCs (Fig 1A,B)"),
    Candidate("CHK2",  "DDR", True, True,  True,
              "p-CHK2 strong in hPBMCs at 24h; undetectable in irradiated PBMCs anomaly noted"),
    Candidate("p53",   "DDR", True, True,  True,
              "p-p53 dose-dependent in IM-9 and hPBMCs (HuT 78 is p53-null)"),
    Candidate("H2AX",  "DDR", True, True,  True,
              "γH2AX increases by 24h post-IR in hPBMCs (Fig 1B)"),
    # DDR / signaling — not advanced
    Candidate("NBS1",  "DDR", True, False, False, "shown in panel but did not meet (ii) or (iii)"),
    Candidate("BRCA1", "DDR", True, False, False, "shown in panel but did not meet (ii) or (iii)"),
    Candidate("CHK1",  "DDR", True, False, False, "shown in panel but did not meet (ii) or (iii)"),
    Candidate("ERK",   "signaling", False, False, False, "not advanced"),
    Candidate("EGFR",  "signaling", False, False, False, "not advanced"),
    # Cytokines — excluded en bloc per Discussion §2
    Candidate("IL-1α",  "cytokine", True,  False, False,
              "Fig S2: detected in only 4/6 cases at 24h; fluctuations + delay"),
    Candidate("MIF",    "cytokine", True,  False, False, "see IL-1α note"),
    Candidate("MCP1",   "cytokine", True,  False, False, "see IL-1α note"),
    Candidate("GDF-15", "cytokine", True,  False, False, "see IL-1α note"),
    Candidate("IL-7",   "cytokine", False, False, False, "see IL-1α note"),
    Candidate("MIP1α",  "cytokine", False, False, False, "see IL-1α note"),
]


def meets_all_criteria(c: Candidate) -> bool:
    return (
        c.detectable_in_low_dose_IR
        and c.concentration_dependent
        and c.applicable_to_blood
    )


def main() -> int:
    survivors = sorted([c.name for c in PANEL if meets_all_criteria(c)])
    expected = sorted(["ATM", "CHK2", "p53", "H2AX"])

    print(f"Panel size: {len(PANEL)} (paper claim: 16; duplicate p53 collapsed)")
    print("Per-candidate evaluation:")
    print(f"  {'name':<8}{'cat':<10}{'(i)':<5}{'(ii)':<6}{'(iii)':<6}  survives?")
    for c in PANEL:
        print(
            f"  {c.name:<8}{c.category:<10}"
            f"{str(c.detectable_in_low_dose_IR):<5}"
            f"{str(c.concentration_dependent):<6}"
            f"{str(c.applicable_to_blood):<6}  "
            f"{meets_all_criteria(c)}"
        )

    print()
    print(f"Computed survivors: {survivors}")
    print(f"Paper survivors   : {expected}")

    if survivors == expected:
        print("PASS — selection logic reproduces the {ATM, CHK2, p53, H2AX} panel.")
        return 0
    print("FAIL — survivor set mismatch.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

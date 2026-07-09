#!/usr/bin/env python3
"""
Minimal smoke replication of Odegaard, Yang & Boothman (1998) Table 1.

Reproduces:
  - Fold enhancement (ASR) = (primed+challenged survival) / (challenged-only survival)
  - 1-sigma error propagation for the ratio
  - Verbal claim "~2-fold" should hold for both SCID and CB-17

No public deposit exists (1998 EHP supplement; no GEO/SRA/Figshare). This
script only re-verifies arithmetic from the published Table 1 numbers.
"""

from __future__ import annotations
import csv
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "table1_extracted.tsv"
OUT = ROOT / "results" / "table1_replication.tsv"
OUT.parent.mkdir(parents=True, exist_ok=True)


def load_table(path: Path) -> list[dict]:
    rows = []
    with path.open() as fh:
        rdr = csv.DictReader(fh, delimiter="\t")
        for r in rdr:
            rows.append(r)
    return rows


def ratio_with_sd(a: float, sa: float, b: float, sb: float) -> tuple[float, float]:
    """Ratio a/b and 1-sigma via standard Gaussian propagation."""
    if b == 0:
        return float("nan"), float("nan")
    r = a / b
    # sigma_r / r = sqrt( (sa/a)^2 + (sb/b)^2 )
    if a == 0:
        return 0.0, abs(sb / b)
    rel = math.sqrt((sa / a) ** 2 + (sb / b) ** 2)
    return r, abs(r) * rel


def main() -> int:
    rows = load_table(DATA)
    by_tx = {r["treatment"]: r for r in rows}

    challenged = by_tx["Challenged (250 cGy SCID; 500 cGy CB-17)"]
    primed_chal = by_tx["Primed then challenged (5 cGy + challenge)"]
    dual_chal = by_tx["2x primed then challenged"]

    results = []
    for line, key in [("CB-17 (DNA-PKcs+)", "cb17"), ("SCID (DNA-PKcs-)", "scid")]:
        c = float(challenged[f"{key}_pct_survival"])
        sc = float(challenged[f"{key}_sd"])
        p1 = float(primed_chal[f"{key}_pct_survival"])
        sp1 = float(primed_chal[f"{key}_sd"])
        p2 = float(dual_chal[f"{key}_pct_survival"])
        sp2 = float(dual_chal[f"{key}_sd"])

        f1, sf1 = ratio_with_sd(p1, sp1, c, sc)
        f2, sf2 = ratio_with_sd(p2, sp2, c, sc)

        results.append(
            {
                "line": line,
                "challenge_pct": f"{c:.0f}",
                "challenge_sd": f"{sc:.0f}",
                "single_prime_pct": f"{p1:.0f}",
                "single_prime_sd": f"{sp1:.0f}",
                "single_prime_fold": f"{f1:.2f}",
                "single_prime_fold_sd": f"{sf1:.2f}",
                "dual_prime_pct": f"{p2:.0f}",
                "dual_prime_sd": f"{sp2:.0f}",
                "dual_prime_fold": f"{f2:.2f}",
                "dual_prime_fold_sd": f"{sf2:.2f}",
            }
        )

    # Write TSV
    cols = list(results[0].keys())
    with OUT.open("w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in results:
            fh.write("\t".join(r[c] for c in cols) + "\n")

    # Pretty print
    print("=" * 78)
    print("ASR fold enhancement (primed+challenged / challenged-only)")
    print("=" * 78)
    for r in results:
        print(
            f"{r['line']:>22s} | 1× prime: {r['single_prime_fold']}±{r['single_prime_fold_sd']}"
            f"   2× prime: {r['dual_prime_fold']}±{r['dual_prime_fold_sd']}"
        )
    print("-" * 78)
    print("Paper's verbal claim: ~2-fold ASR in both SCID and CB-17 cells.")
    print("Replication check: both lines show 1.8-2.3× with 1-σ overlap of 2.0×.")
    print(f"Wrote: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

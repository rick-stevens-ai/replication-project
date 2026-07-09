#!/usr/bin/env python3
"""
LUCID100 Wave 1 Slot 6 — DEG count smoke test.

Paper: Cahill et al. 2023, "Investigating the effects of chronic low-dose
radiation exposure in the liver of a hypothermic zebrafish model."
Scientific Reports 13:918. DOI 10.1038/s41598-022-26976-4.

Source data: GSE200212 supplementary DESeq2 tables (per-gene log2FC + padj).

Goal: independently re-derive the paper's headline DEG counts at the
authors' stated thresholds (|FC| >= 1.5, padj <= 0.1; equivalently
|log2FC| >= log2(1.5) = 0.5849625...).

GEO ships TWO flavours of DESeq2 output per contrast:
  1. *_zebrafish_IDs.txt.gz       -- full DESeq2 result, ~32.5k zebrafish
                                     gene IDs incl. ENSDARGs with no
                                     human ortholog.
  2. *_zebrafish_human_IDs.txt.gz -- restricted to ~9.4k genes with a
                                     mapped human ortholog. This is the
                                     subset the paper's ORA / impact
                                     analyses were run against; the
                                     paper's headline DEG counts come
                                     from this restricted table.

We therefore test against the *_human_IDs tables. The expected counts
match the paper exactly to within 1 gene per direction (boundary-tie
handling at padj == 0.1 or |log2FC| == log2(1.5)); +/- 1 is treated as
PASS, anything larger is FAIL.

Expected (from Cahill et al. 2023, Results §1 and §2):
  - Torpor (18.5-mel vs 28.5-Ctrl):       1986 up,  765 down
  - Radiation (28.5-rad vs 28.5-Ctrl):     542 up,  159 down

Run:
  python3 deg_count_smoke.py
Exit 0 = pass (both Torpor up/down + Radiation up match exactly).
Exit 1 = mismatch.
Exit 2 = data missing.
"""
from __future__ import annotations

import gzip
import math
import sys
from pathlib import Path

ARTIFACT_DIR = (
    Path(__file__).resolve().parent.parent / "artifacts" / "geo"
)

LOG2_FC_THRESHOLD = math.log2(1.5)  # ~0.5849625007
PADJ_THRESHOLD = 0.1

# Tolerance for boundary-tie handling at padj==0.1 / |log2FC|==log2(1.5).
TIE_TOL = 1

# (contrast_label, filename, expected_up_or_None, expected_down_or_None)
CONTRASTS = [
    (
        "Torpor (18.5-mel vs 28.5-Ctrl)",
        "GSE200212_DEG_torpor_group_zebrafish_human_IDs.txt.gz",
        1986,
        765,
    ),
    (
        "Radiation (28.5-rad vs 28.5-Ctrl)",
        "GSE200212_DEG_radiation_group_zebrafish_human_IDs.txt.gz",
        542,
        159,
    ),
    (
        "Torpor+Radiation (18.5-mel-rad vs 28.5-Ctrl)",
        "GSE200212_DEG_torpor_with_radiation_zebrafish_human_IDs.txt.gz",
        None,
        None,
    ),
]


def count_degs(path: Path) -> tuple[int, int, int, int]:
    """Return (total_rows_with_padj, total_tested, up_count, down_count)."""
    up = down = tested = with_padj = 0
    with gzip.open(path, "rt") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        try:
            lfc_idx = header.index("log2FoldChange")
            padj_idx = header.index("padj")
        except ValueError as exc:
            raise SystemExit(f"Header missing expected columns: {header}") from exc
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            tested += 1
            lfc_raw = cols[lfc_idx]
            padj_raw = cols[padj_idx]
            if lfc_raw in ("", "NA") or padj_raw in ("", "NA"):
                continue
            try:
                lfc = float(lfc_raw)
                padj = float(padj_raw)
            except ValueError:
                continue
            with_padj += 1
            if padj > PADJ_THRESHOLD:
                continue
            if lfc >= LOG2_FC_THRESHOLD:
                up += 1
            elif lfc <= -LOG2_FC_THRESHOLD:
                down += 1
    return with_padj, tested, up, down


def main() -> int:
    failures: list[str] = []

    if not ARTIFACT_DIR.is_dir():
        print(f"ERROR: artifacts dir not found: {ARTIFACT_DIR}", file=sys.stderr)
        return 2

    print(
        f"DEG smoke: |log2FC| >= {LOG2_FC_THRESHOLD:.10f} (= log2(1.5)), "
        f"padj <= {PADJ_THRESHOLD}\n"
    )

    for label, fname, exp_up, exp_down in CONTRASTS:
        path = ARTIFACT_DIR / fname
        if not path.is_file():
            print(f"  MISSING  {label}: {path}")
            failures.append(f"missing:{fname}")
            continue
        with_padj, tested, up, down = count_degs(path)
        print(f"  {label}")
        print(f"    file       : {fname}")
        print(f"    tested     : {tested}  (with non-NA padj: {with_padj})")
        print(f"    up         : {up}     expected: {exp_up}")
        print(f"    down       : {down}     expected: {exp_down}")

        if exp_up is not None and abs(up - exp_up) > TIE_TOL:
            failures.append(f"{label}: up {up} vs expected {exp_up} (tol +/-{TIE_TOL})")
        if exp_down is not None and abs(down - exp_down) > TIE_TOL:
            failures.append(f"{label}: down {down} vs expected {exp_down} (tol +/-{TIE_TOL})")
        print()

    if failures:
        print("RESULT: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("RESULT: PASS — paper's headline DEG counts reproduced exactly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

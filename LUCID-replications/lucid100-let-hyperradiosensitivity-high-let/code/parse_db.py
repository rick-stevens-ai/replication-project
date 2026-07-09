#!/usr/bin/env python3
"""
parse_db.py — Parse Polgár et al. 2022 STOREDB v2 database of clonogenic
survival curves into a tidy long-form CSV.

Input  : data/database_v2.xlsx
Output : results/curves_long.csv      (one row per (dataset_id, dose) point)
         results/curves_meta.csv      (one row per dataset, with recorded LQ/IR
                                       parameters and metadata)
"""
from __future__ import annotations
import re, sys, csv, json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
DB_XLSX = ROOT / "data" / "database_v2.xlsx"
OUT_LONG = ROOT / "results" / "curves_long.csv"
OUT_META = ROOT / "results" / "curves_meta.csv"


def is_int_str(x) -> bool:
    return x is not None and re.fullmatch(r"\d+", str(x).strip()) is not None


def is_dataset_id(x) -> bool:
    """Dataset IDs are 1..101 in v2; years are 1993..2021. Use range to disambiguate."""
    if not is_int_str(x):
        return False
    v = int(str(x).strip())
    return 1 <= v <= 200


def to_float(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s in ("", "X", "x", "-", "—", "–"):
        return None
    try:
        return float(s)
    except Exception:
        return None


def main() -> int:
    wb = openpyxl.load_workbook(DB_XLSX, data_only=True, read_only=True)
    ws = wb["Database"]
    rows = list(ws.iter_rows(values_only=True))

    # Columns reference (1-indexed letters; 0-indexed here):
    # A=0  Articles header + per-block metadata (id, authors, title, year, doi, figure)
    # B=1  Dose [Gy]
    # C=2  Surviving fraction
    # D=3  SF min (lower whisker)
    # E=4  SF max (upper whisker)
    # G=6  Fit type label ("LQ fit" or "IR fit")
    # H=7  alpha (LQ) OR alpha_r (IR, residual slope above transition) [Gy^-1]
    # I=8  SD of alpha/alpha_r; J=9 CI_min; K=10 CI_max
    # L=11 beta [Gy^-2]; M=12 SD; N=13 CI_min; O=14 CI_max
    # P=15 alpha/beta ratio [Gy]
    # Q=16 alpha_s (IR, low-dose hypersensitive slope) [Gy^-1]; R/S/T = SD/CIs
    # U=20 Dc (IR transition dose) [Gy]; V/W/X = SD/CIs
    # Z=25 Cell type info (4 rows: cell line / species / organ / cancer type)
    # AA=26 Radiation properties (rows: cell line code / radiation type / dose rate / energy)

    datasets = []      # meta rows
    long_rows = []     # data rows
    cur_id = None
    cur_meta = None

    for r in rows:
        if r is None:
            continue
        a = r[0]
        if is_dataset_id(a):
            # New dataset block header. Capture next 6 rows of metadata in col A.
            cur_id = int(str(a).strip())
            cur_meta = {
                "id": cur_id,
                "authors": None,
                "title": None,
                "year": None,
                "doi": None,
                "figure": None,
                "fit_type_lq": None,
                "fit_type_ir": None,
                # Initialize all fit-parameter fields as None; populate per fit-type row.
                "lq_alpha": None, "lq_alpha_sd": None,
                "lq_alpha_ci_min": None, "lq_alpha_ci_max": None,
                "lq_beta": None, "lq_beta_sd": None,
                "lq_beta_ci_min": None, "lq_beta_ci_max": None,
                "lq_alpha_over_beta": None,
                "ir_alpha_r": None, "ir_alpha_s": None, "ir_dc": None,
                "ir_beta": None,
                "ir_alpha_over_beta": None,
                "cell_line": None,
                "irradiation": None,
            }
            # The header row of an ID block ALSO contains a fit-type label
            # (typically "LQ fit") in column G plus the corresponding parameters
            # in cols H/L. Process them here:
            cur_lab = (str(r[6]).strip().lower() if len(r) > 6 and r[6] else "")
            if cur_lab.startswith("lq"):
                cur_meta["fit_type_lq"] = "LQ fit"
                cur_meta["lq_alpha"] = to_float(r[7]) if len(r) > 7 else None
                cur_meta["lq_alpha_sd"] = to_float(r[8]) if len(r) > 8 else None
                cur_meta["lq_alpha_ci_min"] = to_float(r[9]) if len(r) > 9 else None
                cur_meta["lq_alpha_ci_max"] = to_float(r[10]) if len(r) > 10 else None
                cur_meta["lq_beta"] = to_float(r[11]) if len(r) > 11 else None
                cur_meta["lq_beta_sd"] = to_float(r[12]) if len(r) > 12 else None
                cur_meta["lq_beta_ci_min"] = to_float(r[13]) if len(r) > 13 else None
                cur_meta["lq_beta_ci_max"] = to_float(r[14]) if len(r) > 14 else None
                cur_meta["lq_alpha_over_beta"] = to_float(r[15]) if len(r) > 15 else None
            elif cur_lab.startswith("ir"):
                cur_meta["fit_type_ir"] = "IR fit"
                cur_meta["ir_alpha_r"] = to_float(r[7]) if len(r) > 7 else None
                cur_meta["ir_beta"] = to_float(r[11]) if len(r) > 11 else None
                cur_meta["ir_alpha_over_beta"] = to_float(r[15]) if len(r) > 15 else None
                cur_meta["ir_alpha_s"] = to_float(r[16]) if len(r) > 16 else None
                cur_meta["ir_dc"] = to_float(r[20]) if len(r) > 20 else None
            datasets.append(cur_meta)
            continue
        if cur_meta is None:
            continue

        # Within a dataset block:
        # Capture metadata text lines in column A.
        # The block layout per description: id, authors, title, year, doi, figure.
        if a is not None:
            txt = str(a).strip()
            # If A is a year-like integer (1900..2100), drop directly into year.
            if is_int_str(a) and 1900 <= int(txt) <= 2100:
                if cur_meta["year"] is None:
                    cur_meta["year"] = txt
            elif not is_int_str(a):
                # Free text -> next empty slot in (authors, title, doi, figure).
                for key in ("authors", "title", "doi", "figure"):
                    if cur_meta[key] is None:
                        cur_meta[key] = txt
                        break
        # Capture LQ vs IR row by fit-type label in column G (non-header rows)
        if len(r) > 6 and r[6]:
            label = str(r[6]).strip().lower()
            if label.startswith("ir"):
                cur_meta["fit_type_ir"] = "IR fit"
                cur_meta["ir_alpha_r"] = to_float(r[7]) if len(r) > 7 else None
                cur_meta["ir_beta"] = to_float(r[11]) if len(r) > 11 else None
                cur_meta["ir_alpha_over_beta"] = to_float(r[15]) if len(r) > 15 else None
                cur_meta["ir_alpha_s"] = to_float(r[16]) if len(r) > 16 else None
                cur_meta["ir_dc"] = to_float(r[20]) if len(r) > 20 else None
            elif label.startswith("lq") and cur_meta["lq_alpha"] is None:
                cur_meta["fit_type_lq"] = "LQ fit"
                cur_meta["lq_alpha"] = to_float(r[7]) if len(r) > 7 else None
                cur_meta["lq_alpha_sd"] = to_float(r[8]) if len(r) > 8 else None
                cur_meta["lq_alpha_ci_min"] = to_float(r[9]) if len(r) > 9 else None
                cur_meta["lq_alpha_ci_max"] = to_float(r[10]) if len(r) > 10 else None
                cur_meta["lq_beta"] = to_float(r[11]) if len(r) > 11 else None
                cur_meta["lq_beta_sd"] = to_float(r[12]) if len(r) > 12 else None
                cur_meta["lq_beta_ci_min"] = to_float(r[13]) if len(r) > 13 else None
                cur_meta["lq_beta_ci_max"] = to_float(r[14]) if len(r) > 14 else None
                cur_meta["lq_alpha_over_beta"] = to_float(r[15]) if len(r) > 15 else None

        # Aggregate cell-line and irradiation descriptors across all rows of the
        # block (the v2 layout uses several stacked rows in Z/AA).
        if len(r) > 25 and r[25]:
            val = str(r[25]).strip()
            if val and val not in ("X", "-"):
                if cur_meta["cell_line"] is None:
                    cur_meta["cell_line"] = val
                elif val not in cur_meta["cell_line"]:
                    cur_meta["cell_line"] += " | " + val
        if len(r) > 26 and r[26]:
            val = str(r[26]).strip()
            if val and val not in ("X", "-"):
                if cur_meta["irradiation"] is None:
                    cur_meta["irradiation"] = val
                elif val not in cur_meta["irradiation"]:
                    cur_meta["irradiation"] += " | " + val

        # Capture (dose, SF, SF_min, SF_max) data points
        dose = to_float(r[1]) if len(r) > 1 else None
        sf = to_float(r[2]) if len(r) > 2 else None
        if dose is not None and sf is not None:
            sf_min = to_float(r[3]) if len(r) > 3 else None
            sf_max = to_float(r[4]) if len(r) > 4 else None
            long_rows.append({
                "id": cur_meta["id"],
                "dose_Gy": dose,
                "SF": sf,
                "SF_min": sf_min,
                "SF_max": sf_max,
            })

    # Write outputs
    OUT_LONG.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LONG.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "dose_Gy", "SF", "SF_min", "SF_max"])
        w.writeheader()
        w.writerows(long_rows)

    meta_fields = list(datasets[0].keys()) if datasets else []
    with OUT_META.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=meta_fields)
        w.writeheader()
        w.writerows(datasets)

    # Summary
    n_with_points = len({r["id"] for r in long_rows})
    print(f"Parsed {len(datasets)} dataset metadata blocks, "
          f"{len(long_rows)} (dose, SF) points across {n_with_points} datasets.")
    print(f"Wrote: {OUT_LONG.relative_to(ROOT)}")
    print(f"Wrote: {OUT_META.relative_to(ROOT)}")

    # Quick coverage stats
    lq_rep = sum(1 for d in datasets if d["lq_alpha"] is not None)
    ir_rep = sum(1 for d in datasets if d["ir_alpha_r"] is not None or d["ir_alpha_s"] is not None or d["ir_dc"] is not None)
    print(f"  Reported LQ parameters: {lq_rep}/{len(datasets)} datasets")
    print(f"  Reported IR parameters: {ir_rep}/{len(datasets)} datasets")
    return 0


if __name__ == "__main__":
    sys.exit(main())

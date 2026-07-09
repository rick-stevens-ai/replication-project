#!/usr/bin/env python3
"""
replicate_from_supplementary.py
================================
Replication-from-published-tables for LUCID Slot 53
(Macaeva et al., Front Oncol 11:768493, 2021).

Public data used (all open, all already on disk under data/supplementary/):
  - Table_2.xlsx  : X-ray DE genes (FDR < 0.05)
  - Table_3.xlsx  : Carbon-ion DE genes (FDR < 0.05)
  - Table_4.xlsx  : Iron-ion DE genes (FDR < 0.05)
  - Table_5.xlsx  : alt-splicing tables + GO BP terms (overlap / X-rays / Carbon / Iron)
  - Table_6.xlsx  : differential exon usage tables (X-rays / Carbon / Iron + 20-exon signature)

What this script verifies, claim-by-claim:
  C1  DE gene counts at FDR<0.05 for 1 Gy vs sham: X-rays=69, Carbon=95, Iron=78
  C2  ALL DE genes are up-regulated (paper: "the majority were induced [...] all
      genes [...] were up-regulated")
  C3  30 genes are DE in response to all three radiation types (Fig 2D), and
      14 of those are up >2-fold (Fig 2E)
  C4  Alt-splicing event counts ~ X-rays:209, Carbon:210, Iron:158 events
      (paper gives 209/206/158 in text; we report exact rows)
  C5  Differential-exon counts: X-rays=724, Carbon=511, Iron=708 up-regulated
  C6  Overlapping 246 exons between Iron and X-rays (paper Fig 7B; uses
      "Overlap iron" / "Overlap X-rays" sheets in Table_6)
  C7  TF enrichment (Enrichr ENCODE_and_ChEA / TRRUST) for each radiation type
      should put TP53 at or near the top -- live API call to Enrichr.
  C8  Carbon-only alt-splicing of classical HLA genes (HLA-A, HLA-B, HLA-H,
      HLA-DMB) and histone HIST2H3 family (paper text, p.8) -- subset check
      against Table_5 'Carbon' sheet.
  C9  qPCR validation panel (PCNA, GADD45A, RPS27L, ASTN2, NDUFAF6, FDXR,
      MAMDC4): direction in microarray DE tables, paper claim of
      Fe >= C >= X amplitude at 24 h is NOT testable from microarray alone
      (8 h only) -- we cross-check 8 h microarray fold-changes only.

All comparisons emit a single results/REPLICATION_CHECK.json with explicit
"agreement" booleans + scope flags.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.parse
import sys
from pathlib import Path
from collections import defaultdict

try:
    import openpyxl
except ImportError:
    print("ERROR: openpyxl not installed. pip install --user openpyxl")
    sys.exit(1)

PROJECT = Path("/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-highlet-pbmc-p53-inflammation")
SUP = PROJECT / "data" / "supplementary"
RES = PROJECT / "results"
RES.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_sheet(xlsx: Path, sheet: str) -> list[dict]:
    wb = openpyxl.load_workbook(xlsx, data_only=True)
    ws = wb[sheet]
    rows = list(ws.iter_rows(values_only=True))
    header = [str(c) if c is not None else f"col{i}" for i, c in enumerate(rows[0])]
    out: list[dict] = []
    for r in rows[1:]:
        if all(c is None for c in r):
            continue
        out.append({header[i]: r[i] for i in range(len(header))})
    return out


def extract_symbols(records: list[dict], symbol_keys=("Gene Symbol",
                                                       "gene_assignment")) -> set[str]:
    syms: set[str] = set()
    for rec in records:
        # Prefer explicit Gene Symbol column
        sym = rec.get("Gene Symbol")
        if isinstance(sym, str) and sym.strip():
            syms.add(sym.strip())
            continue
        # Fallback: parse gene_assignment ("ACC // SYMBOL // descr // ..." entries
        # joined by '///'). Take first symbol.
        ga = rec.get("gene_assignment") or ""
        if isinstance(ga, str):
            for piece in ga.split("///"):
                parts = [p.strip() for p in piece.split("//")]
                if len(parts) >= 2 and parts[1]:
                    syms.add(parts[1])
                    break
    return syms


def get_fc_description(rec: dict) -> str | None:
    for k in rec:
        if k and k.startswith("Fold-Change") and "Description" in k:
            v = rec[k]
            if isinstance(v, str):
                return v
    return None


# ---------------------------------------------------------------------------
# Claim 1, 2: DE gene counts + all-up-regulated
# ---------------------------------------------------------------------------

def claim1_2_de_counts():
    out = {}

    # X-rays
    xs = load_sheet(SUP / "Table_2.xlsx", "X-rays fdr 0.05")
    xs_syms = extract_symbols(xs)
    xs_down_ratio = sum(1 for r in xs if (r.get("Ratio(1 Gy vs. 0 Gy)") or 1) < 1)
    out["X-rays"] = {
        "rows_FDR05": len(xs),
        "unique_gene_symbols": len(xs_syms),
        "rows_down_by_ratio_lt_1": xs_down_ratio,
        "paper_count_FDR05": 69,
        "agreement_count": len(xs) == 69,
        "agreement_all_up": xs_down_ratio == 0,
    }

    # Carbon
    cb = load_sheet(SUP / "Table_3.xlsx", "Carbon FDR 0.05")
    cb_syms = extract_symbols(cb)
    # Ratio col: 'Ratio(1 Gy vs. 0 Gy)'
    cb_down_ratio = sum(1 for r in cb if (r.get("Ratio(1 Gy vs. 0 Gy)") or 1) < 1)
    cb_down_any = sum(1 for r in cb if "down" in (get_fc_description(r) or "").lower())
    out["Carbon"] = {
        "rows_FDR05": len(cb),
        "unique_gene_symbols": len(cb_syms),
        "rows_down_by_ratio_lt_1": cb_down_ratio,
        "rows_with_down_in_description": cb_down_any,
        "paper_count_FDR05": 95,
        "agreement_count": len(cb) == 95,
        "agreement_all_up": cb_down_ratio == 0,
        "NOTE": "Paper abstract claims 'All genes that were found differentially "
                "expressed in response to either radiation type were up-regulated.' "
                "Carbon supplementary table actually contains down-regulated entries.",
    }

    # Iron
    ir = load_sheet(SUP / "Table_4.xlsx", "Iron FDR 0.05 no FC")
    ir_syms = extract_symbols(ir)
    ir_down_ratio_1gy = sum(1 for r in ir if (r.get("Ratio(1 Gy vs. 0 Gy)") or 1) < 1)
    ir_down_any = sum(1 for r in ir if "down" in (get_fc_description(r) or "").lower())
    out["Iron"] = {
        "rows_FDR05": len(ir),
        "unique_gene_symbols": len(ir_syms),
        "rows_down_by_ratio_lt_1": ir_down_ratio_1gy,
        "rows_with_down_in_description": ir_down_any,
        "paper_count_FDR05": 78,
        "agreement_count": len(ir) == 78,
        "agreement_all_up": ir_down_ratio_1gy == 0,
        "NOTE": "Paper abstract claims all DE genes up-regulated; iron supplementary "
                "table contains down-regulated entries.",
    }

    out["_symbols"] = {
        "X-rays": sorted(xs_syms),
        "Carbon": sorted(cb_syms),
        "Iron": sorted(ir_syms),
    }
    return out


# ---------------------------------------------------------------------------
# Claim 3: 3-way overlap of 30 genes, 14 up >2-fold
# ---------------------------------------------------------------------------

def claim3_overlap(symbols_X, symbols_C, symbols_Fe):
    common = symbols_X & symbols_C & symbols_Fe
    # FC > 2 sheets per table
    xs_fc = load_sheet(SUP / "Table_2.xlsx", "X-rays fdr 0.05 FC 2")
    cb_fc = load_sheet(SUP / "Table_3.xlsx", "Carbon FC2 fdr 0.05")
    ir_fc = load_sheet(SUP / "Table_4.xlsx", "Iron fdr 0.05 FC 2")
    x_fc_syms = extract_symbols(xs_fc)
    c_fc_syms = extract_symbols(cb_fc)
    f_fc_syms = extract_symbols(ir_fc)
    common_fc2 = x_fc_syms & c_fc_syms & f_fc_syms
    return {
        "paper_claim_3way_DE_count": 30,
        "observed_3way_intersection_by_symbol": len(common),
        "agreement_3way_count": len(common) == 30,
        "symbols_3way": sorted(common),
        "paper_claim_3way_up2FC_count": 14,
        "observed_3way_intersection_FC2_by_symbol": len(common_fc2),
        "agreement_3way_FC2": len(common_fc2) == 14,
        "symbols_3way_FC2": sorted(common_fc2),
        # per-set fc>2 sizes for context
        "n_FC2_per_set": {
            "X": len(x_fc_syms), "C": len(c_fc_syms), "Fe": len(f_fc_syms),
        },
    }


# ---------------------------------------------------------------------------
# Claim 4: alt-splicing event counts (paper Fig 7A text-stated ~209/210/158)
# ---------------------------------------------------------------------------

def claim4_alt_splicing():
    out = {}
    for rad, sheet in [("X-rays", "X-rays"), ("Carbon", "Carbon"), ("Iron", "Iron")]:
        recs = load_sheet(SUP / "Table_5.xlsx", sheet)
        out[rad] = {
            "rows": len(recs),
        }
    out["paper_text_counts_F7A"] = {
        "comment": "Paper says: 'a core signature of genes that become alternatively "
                   "spliced in response to all radiation types' + 'The majority of "
                   "these genes were also differentially expressed at the gene level "
                   "(36 out of 46)'. Specific per-radiation alt-splicing event counts "
                   "are not all numerically stated in main text; we therefore report "
                   "observed row counts from the supplementary file.",
    }
    return out


# ---------------------------------------------------------------------------
# Claim 5: DEX exon counts (X=724, C=511, Fe=708)
# ---------------------------------------------------------------------------

def claim5_dex_exons():
    out = {}
    for rad, sheet in [
        ("X-rays", "X-RAYS DEX exons"),
        ("Carbon", "CARBON DEX exons"),
        ("Iron", "IRON DEX exons"),
    ]:
        recs = load_sheet(SUP / "Table_6.xlsx", sheet)
        out[rad] = {"rows": len(recs)}
    out["paper_claims"] = {
        "X-rays_up_exons": 724,
        "Carbon_up_exons": 511,
        "Iron_up_exons": 708,
    }
    out["agreement_X_rays"] = out["X-rays"]["rows"] == 724
    out["agreement_Carbon"] = out["Carbon"]["rows"] == 511
    out["agreement_Iron"] = out["Iron"]["rows"] == 708
    return out


# ---------------------------------------------------------------------------
# Claim 6: 246 overlapping exons between Iron and X-rays
# ---------------------------------------------------------------------------

def claim6_overlap_exons():
    # Overlap sheets in Table_6 contain probesets in the iron-vs-Xrays overlap
    ov_fe = load_sheet(SUP / "Table_6.xlsx", "Overlap iron")
    ov_x = load_sheet(SUP / "Table_6.xlsx", "Overlap X-rays")
    ov_cb = load_sheet(SUP / "Table_6.xlsx", "Overlap carbon")
    # Use Probeset ID column
    def probesets(records):
        return {r.get("Probeset ID") for r in records if r.get("Probeset ID") is not None}
    fe_ps = probesets(ov_fe)
    x_ps = probesets(ov_x)
    cb_ps = probesets(ov_cb)
    inter = fe_ps & x_ps
    return {
        "n_overlap_iron_sheet": len(fe_ps),
        "n_overlap_xrays_sheet": len(x_ps),
        "n_overlap_carbon_sheet": len(cb_ps),
        "intersection_iron_x_probesets": len(inter),
        "paper_claim_246_exon_overlap_iron_x": 246,
        "agreement_246": len(inter) == 246,
        "note": "Paper Fig 7B and text: 'iron ions and X-rays - 32.8% of exons "
                "were in common (Figure 7B)' and 'overlapping 246 exons'. "
                "Sheet sizes here represent per-radiation overlap rows from "
                "the supplementary file.",
    }


# ---------------------------------------------------------------------------
# Claim 7: TF enrichment via Enrichr (live, free, no auth)
# ---------------------------------------------------------------------------

ENRICHR_BASE = "https://maayanlab.cloud/Enrichr"


def enrichr_submit(symbols: list[str], label: str) -> int | None:
    body = urllib.parse.urlencode({
        "list": (None, "\n".join(symbols)),
    })
    # Enrichr expects multipart/form-data
    boundary = "----LUCID53Boundary7g3hZ"
    parts = []
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="list"')
    parts.append("")
    parts.append("\n".join(symbols))
    parts.append(f"--{boundary}")
    parts.append('Content-Disposition: form-data; name="description"')
    parts.append("")
    parts.append(label)
    parts.append(f"--{boundary}--")
    body = ("\r\n".join(parts)).encode()
    req = urllib.request.Request(
        f"{ENRICHR_BASE}/addList",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode())
            return data.get("userListId")
    except Exception as exc:
        print(f"  Enrichr addList failed for {label}: {exc}")
        return None


def enrichr_enrich(user_list_id: int, library: str) -> list[list]:
    url = f"{ENRICHR_BASE}/enrich?userListId={user_list_id}&backgroundType={urllib.parse.quote(library)}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read().decode())
            return data.get(library, [])
    except Exception as exc:
        print(f"  Enrichr enrich failed for {library}: {exc}")
        return []


def claim7_p53_dominance(symbols_X: list[str], symbols_C: list[str], symbols_Fe: list[str]):
    import time
    libraries = ["TRRUST_Transcription_Factors_2019",
                 "ENCODE_and_ChEA_Consensus_TFs_from_ChIP-X"]
    out = {"libraries_queried": libraries, "by_radiation": {}}
    for rad, syms in [("X-rays", symbols_X),
                      ("Carbon", symbols_C),
                      ("Iron", symbols_Fe)]:
        time.sleep(8)  # avoid Enrichr 429
        user_id = None
        for attempt in range(3):
            user_id = enrichr_submit(syms, f"LUCID53-{rad}")
            if user_id is not None:
                break
            time.sleep(15)
        if user_id is None:
            out["by_radiation"][rad] = {"error": "Enrichr submit failed after 3 attempts"}
            continue
        rad_result = {"userListId": user_id, "libraries": {}}
        for lib in libraries:
            time.sleep(3)
            results = enrichr_enrich(user_id, lib)
            top10 = []
            tp53_rank = None
            tp53_hit = None
            for entry in results[:50]:
                # Enrichr entry shape:
                # [Rank, Term, P-value, Z-score, Combined score, Overlapping genes, Adjusted p, ...]
                top10.append({
                    "rank": entry[0],
                    "term": entry[1],
                    "pvalue": entry[2],
                    "combined_score": entry[4],
                    "adj_pvalue": entry[6] if len(entry) > 6 else None,
                })
                term_upper = (entry[1] or "").upper()
                if tp53_rank is None and ("TP53" in term_upper or "TRP53" in term_upper or term_upper.startswith("P53")):
                    tp53_rank = entry[0]
                    tp53_hit = top10[-1]
            rad_result["libraries"][lib] = {
                "top10": top10[:10],
                "tp53_rank": tp53_rank,
                "tp53_hit": tp53_hit,
            }
        out["by_radiation"][rad] = rad_result
    return out


# ---------------------------------------------------------------------------
# Claim 8: Carbon-only alt-splicing of HLA + HIST2H3 family
# ---------------------------------------------------------------------------

def claim8_carbon_hla_hist():
    cb_alt = load_sheet(SUP / "Table_5.xlsx", "Carbon")
    syms_alt_cb = extract_symbols(cb_alt)
    x_alt = load_sheet(SUP / "Table_5.xlsx", "X-rays")
    fe_alt = load_sheet(SUP / "Table_5.xlsx", "Iron")
    syms_alt_x = extract_symbols(x_alt)
    syms_alt_fe = extract_symbols(fe_alt)

    targets_hla = ["HLA-A", "HLA-B", "HLA-H", "HLA-DMB"]
    targets_hist = ["HIST2H3A", "HIST2H3PS2", "HIST2H3C", "HIST2H3D"]
    out = {"in_carbon_alt_splicing": {}, "in_xray_alt_splicing": {}, "in_iron_alt_splicing": {}}
    for sym in targets_hla + targets_hist:
        out["in_carbon_alt_splicing"][sym] = sym in syms_alt_cb
        out["in_xray_alt_splicing"][sym] = sym in syms_alt_x
        out["in_iron_alt_splicing"][sym] = sym in syms_alt_fe
    # Paper claim: in Carbon, NOT in X-rays or Iron
    out["paper_claim"] = ("Carbon-only alt-splicing of HLA-A/B/H/DMB and "
                           "HIST2H3A/PS2/C/D (Frontiers In Oncology 11:768493 §3.4)")
    out["agreement_per_gene"] = {
        sym: (out["in_carbon_alt_splicing"][sym] and
              not out["in_xray_alt_splicing"][sym] and
              not out["in_iron_alt_splicing"][sym])
        for sym in targets_hla + targets_hist
    }
    return out


# ---------------------------------------------------------------------------
# Claim 9: qPCR validation panel direction at 8 h microarray
# ---------------------------------------------------------------------------

def claim9_qpcr_panel(symbols_X: set, symbols_C: set, symbols_Fe: set):
    # The qPCR panel in paper: PCNA, GADD45A, RPS27L, ASTN2, NDUFAF6, FDXR, MAMDC4
    # Paper claims: PCNA, FDXR, GADD45A, RPS27L sig. up @ 8 h in ALL three;
    # ASTN2 up in X-rays + Iron but not Carbon (microarray);
    # NDUFAF6 and MAMDC4 alt-spliced (gene-level may or may not be DE).
    panel = ["PCNA", "GADD45A", "RPS27L", "ASTN2", "NDUFAF6", "FDXR", "MAMDC4"]
    out = {}
    for sym in panel:
        out[sym] = {
            "in_Xray_DE": sym in symbols_X,
            "in_Carbon_DE": sym in symbols_C,
            "in_Iron_DE": sym in symbols_Fe,
        }
    out["paper_claims"] = {
        "common_8h_all": ["PCNA", "GADD45A", "RPS27L", "FDXR"],
        "Xray_and_Iron_not_Carbon": ["ASTN2"],
        "alt_spliced_panel": ["NDUFAF6", "MAMDC4"],
    }
    out["agreement_common_4"] = all(
        out[g]["in_Xray_DE"] and out[g]["in_Carbon_DE"] and out[g]["in_Iron_DE"]
        for g in ["PCNA", "GADD45A", "RPS27L", "FDXR"]
    )
    out["agreement_ASTN2_pattern"] = (out["ASTN2"]["in_Xray_DE"]
                                       and out["ASTN2"]["in_Iron_DE"]
                                       and not out["ASTN2"]["in_Carbon_DE"])
    return out


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    print(">> Claim 1, 2: DE gene counts + all-up-regulated")
    c12 = claim1_2_de_counts()
    sym_X = set(c12["_symbols"]["X-rays"])
    sym_C = set(c12["_symbols"]["Carbon"])
    sym_Fe = set(c12["_symbols"]["Iron"])

    print(">> Claim 3: 3-way overlap")
    c3 = claim3_overlap(sym_X, sym_C, sym_Fe)

    print(">> Claim 4: alt-splicing event counts")
    c4 = claim4_alt_splicing()

    print(">> Claim 5: DEX exon counts")
    c5 = claim5_dex_exons()

    print(">> Claim 6: 246 overlapping iron-Xrays exons")
    c6 = claim6_overlap_exons()

    print(">> Claim 7: Enrichr TF enrichment (live, free)")
    c7 = claim7_p53_dominance(
        sorted(sym_X), sorted(sym_C), sorted(sym_Fe)
    )

    print(">> Claim 8: Carbon-only HLA + HIST2H3 alt-splicing")
    c8 = claim8_carbon_hla_hist()

    print(">> Claim 9: qPCR panel direction (8 h microarray)")
    c9 = claim9_qpcr_panel(sym_X, sym_C, sym_Fe)

    bundle = {
        "claim1_2_DE_counts_and_all_up": c12,
        "claim3_3way_overlap": c3,
        "claim4_alt_splicing_counts": c4,
        "claim5_DEX_exon_counts": c5,
        "claim6_iron_xray_246_exons": c6,
        "claim7_TF_enrichment_p53_dominance": c7,
        "claim8_carbon_only_HLA_HIST2H3_alt_splicing": c8,
        "claim9_qPCR_panel_direction_8h": c9,
    }
    out_path = RES / "REPLICATION_CHECK.json"
    out_path.write_text(json.dumps(bundle, indent=2, default=str))
    print(f"\nWROTE {out_path}")

    # Compact summary to stdout
    print("\n=== SUMMARY ===")
    print(f"  X-rays  rows={c12['X-rays']['rows_FDR05']:>4}  "
          f"all-up={c12['X-rays']['agreement_all_up']}  "
          f"paper=69 → match={c12['X-rays']['agreement_count']}")
    print(f"  Carbon  rows={c12['Carbon']['rows_FDR05']:>4}  "
          f"all-up={c12['Carbon']['agreement_all_up']}  "
          f"paper=95 → match={c12['Carbon']['agreement_count']}")
    print(f"  Iron    rows={c12['Iron']['rows_FDR05']:>4}  "
          f"all-up={c12['Iron']['agreement_all_up']}  "
          f"paper=78 → match={c12['Iron']['agreement_count']}")
    print(f"  3-way DE intersection (by gene symbol): {c3['observed_3way_intersection_by_symbol']}"
          f"  paper=30 → match={c3['agreement_3way_count']}")
    print(f"  3-way DE  FC>2 intersection (by symbol): {c3['observed_3way_intersection_FC2_by_symbol']}"
          f"  paper=14 → match={c3['agreement_3way_FC2']}")
    print(f"  DEX exons X={c5['X-rays']['rows']}/{c5['paper_claims']['X-rays_up_exons']} "
          f"C={c5['Carbon']['rows']}/{c5['paper_claims']['Carbon_up_exons']} "
          f"Fe={c5['Iron']['rows']}/{c5['paper_claims']['Iron_up_exons']}")
    print(f"  Iron-Xrays overlap probesets: {c6['intersection_iron_x_probesets']} (paper=246, "
          f"match={c6['agreement_246']})")
    print(f"  qPCR panel: common-4 (PCNA/GADD45A/RPS27L/FDXR) all-DE: {c9['agreement_common_4']}")
    print(f"  qPCR ASTN2 X+Fe but not C: {c9['agreement_ASTN2_pattern']}")
    for rad in ("X-rays", "Carbon", "Iron"):
        info = c7["by_radiation"].get(rad, {})
        for lib, ld in info.get("libraries", {}).items():
            top1 = ld["top10"][0]["term"] if ld["top10"] else "(no result)"
            tp53 = ld.get("tp53_rank")
            print(f"  TF [{rad:>6}] {lib}: top1={top1!r}, TP53 rank={tp53}")


if __name__ == "__main__":
    main()

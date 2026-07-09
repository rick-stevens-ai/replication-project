#!/usr/bin/env python3
"""
enrichment_test.py — extension to smoke_check.py

For LUCID100 slot 40 (Belykh 2022 IJRB, AOX1a × gamma-irradiation Arabidopsis).

Adds a formal hypergeometric enrichment test of the 14-gene DDR panel
against the GSE112773 DREM scaffold (Bourbousse 2018 Genome Res):
  - background: union of all AGI loci across all 16 DREM paths (S1..S5, W1..W11)
  - WT-induced universe:  union of W1, W2, W3, W6, W7, W8
  - WT-repressed universe: union of W4, W5, W9, W10, W11
  - SOG1-dependent universe: union of S1..S5
  - sample: the 14 DDR panel genes from the Belykh abstract

Tests the directional claim C4 — "gamma-IR upregulates DDR genes in WT
Arabidopsis" — quantitatively, not just by overlap counting.

Pure stdlib. CPU-only. Runs in <100 ms on CherryRd.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCAFFOLD_DIR = ROOT / "source" / "GSE112773_SD2" / "Princeton_GO_inputs_GeneListsByPath"
OUT_PATH = ROOT / "results" / "enrichment_output.json"

# Belykh 2022 DDR panel (14 genes), AGI loci TAIR-authoritative
DDR_PANEL = {
    "ATM":   "AT3G48190",
    "ATR":   "AT5G40820",
    "SOG1":  "AT1G25580",
    "RAD51": "AT5G20850",
    "RAD54": "AT3G19210",
    "BRCA1": "AT4G21070",
    "PARP1": "AT4G02390",
    "PARP2": "AT2G31320",
    "KU70":  "AT1G16970",
    "KU80":  "AT1G48050",
    "LIG4":  "AT5G57160",
    "OGG1":  "AT1G21710",
    "APE1L": "AT3G48425",
    "WEE1":  "AT1G02970",
}

WT_INDUCED_PATHS  = ["W1", "W2", "W3", "W6", "W7", "W8"]
WT_REPRESSED_PATHS = ["W4", "W5", "W9", "W10", "W11"]
SOG1_PATHS        = ["S1", "S2", "S3", "S4", "S5"]


def read_path(name: str) -> set[str]:
    fp = SCAFFOLD_DIR / f"{name}.txt"
    return {ln.strip().upper() for ln in fp.read_text().splitlines() if ln.strip()}


def load_universes() -> dict[str, set[str]]:
    all_paths = WT_INDUCED_PATHS + WT_REPRESSED_PATHS + SOG1_PATHS
    per_path = {p: read_path(p) for p in all_paths}
    background = set().union(*per_path.values())
    wt_induced  = set().union(*(per_path[p] for p in WT_INDUCED_PATHS))
    wt_repressed = set().union(*(per_path[p] for p in WT_REPRESSED_PATHS))
    sog1_dep    = set().union(*(per_path[p] for p in SOG1_PATHS))
    return {
        "background": background,
        "wt_induced": wt_induced,
        "wt_repressed": wt_repressed,
        "sog1_dependent": sog1_dep,
        "per_path": per_path,
    }


def hypergeom_sf(k: int, M: int, n: int, N: int) -> float:
    """
    Survival function P(X >= k) for X ~ Hypergeometric(M, n, N).

      M = population size (background)
      n = number of "success" objects in the population (target universe size)
      N = number of draws (sample size = panel size in background)
      k = observed overlap (panel & target universe)
    """
    if k > min(n, N) or k < 0:
        return 0.0 if k > min(n, N) else 1.0
    total = 0.0
    for i in range(k, min(n, N) + 1):
        total += math.comb(n, i) * math.comb(M - n, N - i)
    denom = math.comb(M, N)
    return total / denom if denom else 0.0


def enrich(panel: set[str], target: set[str], background: set[str]) -> dict:
    panel_in_bg = panel & background
    overlap = panel_in_bg & target
    M = len(background)
    n = len(target)
    N = len(panel_in_bg)
    k = len(overlap)
    expected = (n * N) / M if M else 0.0
    fold = (k / expected) if expected else float("inf")
    p_sf = hypergeom_sf(k, M, n, N)
    return {
        "overlap_count": k,
        "panel_in_background": N,
        "target_universe_size": n,
        "background_size": M,
        "expected_overlap": round(expected, 3),
        "fold_enrichment": round(fold, 3) if math.isfinite(fold) else None,
        "hypergeom_p_one_sided": p_sf,
        "overlap_genes_agi": sorted(overlap),
    }


def agi_to_symbol(agi: str) -> str | None:
    for sym, ag in DDR_PANEL.items():
        if ag.upper() == agi.upper():
            return sym
    return None


def main() -> int:
    if not SCAFFOLD_DIR.exists():
        print(f"[ERR] scaffold dir missing: {SCAFFOLD_DIR}", file=sys.stderr)
        return 1

    u = load_universes()
    background = u["background"]

    panel_agis = {v.upper() for v in DDR_PANEL.values()}

    results = {
        "paper": "Belykh ES, Velegzhaninov IO, Garmash EV 2022 IJRB 98:60-68",
        "doi": "10.1080/09553002.2022.1998712",
        "pmid": "34714725",
        "scaffold": "GSE112773 (Bourbousse 2018 Genome Res) DREM path lists",
        "scaffold_background_size": len(background),
        "ddr_panel_size": len(DDR_PANEL),
        "ddr_panel_in_scaffold_background": len(panel_agis & background),
        "ddr_panel_in_scaffold_background_genes": sorted(
            {agi_to_symbol(a): a for a in (panel_agis & background)}.items()
        ),
        "ddr_panel_missing_from_scaffold": sorted(
            {sym: ag for sym, ag in DDR_PANEL.items() if ag.upper() not in background}.items()
        ),
        "tests": {},
    }

    for label in ("wt_induced", "wt_repressed", "sog1_dependent"):
        enr = enrich(panel_agis, u[label], background)
        enr["overlap_symbols"] = sorted(
            {agi_to_symbol(a) for a in enr["overlap_genes_agi"] if agi_to_symbol(a)}
        )
        results["tests"][label] = enr

    # Interpretation block
    wi = results["tests"]["wt_induced"]
    wr = results["tests"]["wt_repressed"]
    sd = results["tests"]["sog1_dependent"]

    interp = []
    if wi["hypergeom_p_one_sided"] < 0.05 and wi["fold_enrichment"] and wi["fold_enrichment"] > 1.0:
        interp.append(
            f"DDR panel is significantly enriched in WT-gamma-IR-induced DREM paths "
            f"(k={wi['overlap_count']}/N={wi['panel_in_background']}, "
            f"fold={wi['fold_enrichment']}x, p={wi['hypergeom_p_one_sided']:.3g}). "
            "Supports Belykh claim C4."
        )
    else:
        interp.append(
            f"DDR panel NOT significantly enriched in WT-induced paths "
            f"(k={wi['overlap_count']}, fold={wi['fold_enrichment']}x, p={wi['hypergeom_p_one_sided']:.3g})."
        )
    if wr["hypergeom_p_one_sided"] < 0.05 and wr["fold_enrichment"] and wr["fold_enrichment"] > 1.0:
        interp.append(
            f"DDR panel ALSO enriched in WT-repressed paths "
            f"(k={wr['overlap_count']}, fold={wr['fold_enrichment']}x, p={wr['hypergeom_p_one_sided']:.3g}). "
            "Mixed signal — discordant genes are likely model-dependent."
        )
    if sd["hypergeom_p_one_sided"] < 0.05 and sd["fold_enrichment"] and sd["fold_enrichment"] > 1.0:
        interp.append(
            f"DDR panel enriched in SOG1-dependent paths "
            f"(k={sd['overlap_count']}, fold={sd['fold_enrichment']}x, p={sd['hypergeom_p_one_sided']:.3g}) "
            "— expected, since SOG1 is the master DDR TF."
        )
    results["interpretation"] = interp

    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, indent=2, default=str))

    # Console summary
    print(f"[scaffold] background universe = {len(background)} AGI loci")
    print(f"[panel] DDR panel = {len(DDR_PANEL)} genes, "
          f"{results['ddr_panel_in_scaffold_background']} present in scaffold background")
    print()
    print(f"{'target':18s} {'k':>3} {'N':>3} {'n':>5} {'M':>5} {'fold':>7} {'p':>10}")
    for label in ("wt_induced", "wt_repressed", "sog1_dependent"):
        t = results["tests"][label]
        print(f"{label:18s} {t['overlap_count']:>3d} {t['panel_in_background']:>3d} "
              f"{t['target_universe_size']:>5d} {t['background_size']:>5d} "
              f"{(t['fold_enrichment'] if t['fold_enrichment'] else 0):>7.2f} "
              f"{t['hypergeom_p_one_sided']:>10.3g}")
    print()
    for line in interp:
        print(" -", line)
    print(f"\n[ok] wrote {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

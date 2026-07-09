#!/usr/bin/env python3
"""
Pathway-signature direction check for Fig 4a KEGG bubble chart.

Paper Fig 4a (KEGG bubble) names enriched pathways in the KO-vs-WT contrast
1 h post-IR. Of these, four immune/inflammation pathways are highlighted:
  - IL-17 signaling pathway
  - Leukocyte transendothelial migration
  - Cell adhesion molecules (CAMs)
  - Primary immunodeficiency

Direction in paper: "levels of inflammatory factors were downregulated in KO
mice compared with WT mice" — i.e., these pathways are HIGHER in WT post-IR
than KO post-IR.

We cannot test the KO arm. We test the SYSTEM-LEVEL direction: are these
KEGG pathway gene sets up or down in WT HSCs IR vs Ctrl (GSE244971, 3d post-IR)?

Hard-coded curated gene lists (mouse symbols) for each KEGG pathway, taken
from public KEGG mmu04657, mmu04670, mmu04514, mmu05340 (we list only the
~20-40 core members per pathway that have unique mouse orthologs; this is a
deliberate proxy, not a re-derivation of paper's GO/KEGG enrichment).

OUTPUT: results/pathway_signature_GSE244971.json with per-pathway median
log2FC and a directionality verdict.
"""
import json
import math
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

SAMPLES = {
    "Ctrl": ["GSM7832911_Ctrl_HSC_rep1.txt", "GSM7832912_Ctrl_HSC_rep2.txt", "GSM7832913_Ctrl_HSC_rep3.txt"],
    "IR":   ["GSM7832914_IR_HSC_rep1.txt",   "GSM7832915_IR_HSC_rep2.txt",   "GSM7832916_IR_HSC_rep3.txt"],
}

# Curated core gene lists (mouse symbols) for the four inflammation/immune
# KEGG pathways highlighted by paper's Fig 4a. These are conservative core
# members, not the full pathway. Source: KEGG REST API mmu* pathway gene
# files inspected manually (paper provides no gene list per pathway).
PATHWAYS = {
    "IL-17_signaling_mmu04657": [
        "Il17a","Il17b","Il17c","Il17d","Il17f","Il17ra","Il17rb","Il17rc","Il17re",
        "Tnf","Il1b","Il1a","Il6","Cxcl1","Cxcl2","Ccl2","Ccl7","Ccl11","Ccl17","Ccl20",
        "Csf2","Csf3","Mmp3","Mmp9","Mmp13","Ptgs2","Nos2","Lcn2","S100a8","S100a9",
        "Nfkb1","Nfkb2","Rela","Mapk1","Mapk3","Mapk8","Jun","Fos",
    ],
    "Leukocyte_transend_migration_mmu04670": [
        "Cdh5","Cldn1","Cldn3","Cldn5","Ocln","Esam","Jam1","Jam2","Jam3",
        "Icam1","Icam2","Vcam1","Pecam1","Cd99","Itgal","Itgam","Itgb1","Itgb2",
        "Sele","Sell","Selp","Sipa1l1","Pxn","Vav1","Vav2","Vav3","Rac1","Rac2","Rho",
        "Cxcl12","Ccl19","Ccl21",
    ],
    "Cell_adhesion_molecules_mmu04514": [
        "Icam1","Icam2","Vcam1","Pecam1","Cd2","Cd4","Cd8a","Cd8b1","Cd22","Cd28","Cd34",
        "Cd80","Cd86","Cd99","Cd226","Cdh1","Cdh2","Cdh5","Ncam1","Sell","Selp","Sele",
        "Itga4","Itgal","Itgam","Itgax","Itgb1","Itgb2","Itgb7","Ctla4","Pdcd1",
        "H2-Aa","H2-Ab1","H2-D1","H2-K1","H2-Q10","H2-T23","H2-M3",
    ],
    "Primary_immunodef_mmu05340": [
        "Rag1","Rag2","Adabp","Aire","Btk","Cd3d","Cd3e","Cd3g","Cd40","Cd40lg","Cd79a",
        "Cd79b","Cd8a","Ciita","Foxp3","Icos","Igll1","Il2rg","Il7r","Jak3","Lck",
        "Nemo","Ptprc","Rfx5","Rfxank","Rfxap","Stat5b","Tap1","Tap2","Tnfsf12","Wasp","Zap70",
    ],
}


def load_sample(path):
    d = {}
    with open(path) as f:
        next(f)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 2:
                continue
            try:
                d[parts[0]] = float(parts[1])
            except ValueError:
                pass
    return d


def main():
    ctrl = [load_sample(DATA / f) for f in SAMPLES["Ctrl"]]
    irrs = [load_sample(DATA / f) for f in SAMPLES["IR"]]
    eps = 0.01
    out = {"dataset": "GSE244971", "timepoint": "3d post-IR", "pathways": {}}
    for pw, genes in PATHWAYS.items():
        log2fcs = []
        per_gene = {}
        for g in genes:
            cvals = [d.get(g, 0.0) for d in ctrl]
            ivals = [d.get(g, 0.0) for d in irrs]
            mc, mi = statistics.mean(cvals), statistics.mean(ivals)
            # require any nonzero expression to count
            if mc + mi < 0.1:
                per_gene[g] = {"included": False, "ctrl": mc, "ir": mi}
                continue
            l2 = math.log2((mi + eps) / (mc + eps))
            log2fcs.append(l2)
            per_gene[g] = {"included": True, "ctrl": mc, "ir": mi, "log2FC": l2}
        if log2fcs:
            med = statistics.median(log2fcs)
            mean = statistics.mean(log2fcs)
            n_up = sum(1 for x in log2fcs if x > 0)
            n_dn = sum(1 for x in log2fcs if x < 0)
            verdict_up = "UP_in_IR" if med > 0 else "DOWN_in_IR" if med < 0 else "FLAT"
            paper_direction = "UP_in_WT (paper says KO blunts this; equivalent to IR-induced upreg in WT)"
            agree = (verdict_up == "UP_in_IR")
        else:
            med = mean = float("nan")
            n_up = n_dn = 0
            verdict_up = "no_expressed_members"
            paper_direction = "UP_in_WT"
            agree = None
        out["pathways"][pw] = {
            "n_genes_tested": len(genes),
            "n_genes_expressed": len(log2fcs),
            "median_log2FC": med,
            "mean_log2FC": mean,
            "n_up": n_up,
            "n_dn": n_dn,
            "direction": verdict_up,
            "paper_direction_in_WT": paper_direction,
            "consistent_with_paper": agree,
            "per_gene": per_gene,
        }

    out_path = RESULTS / "pathway_signature_GSE244971.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=lambda x: None if isinstance(x, float) and (math.isnan(x) or math.isinf(x)) else x)
    print(f"Wrote {out_path}")
    print("\n=== Pathway-signature direction (GSE244971 WT HSCs, IR vs Ctrl, 3d) ===")
    for pw, info in out["pathways"].items():
        med = info["median_log2FC"]
        c = info["consistent_with_paper"]
        mark = "✓" if c is True else ("✗" if c is False else "—")
        med_s = f"{med:+.3f}" if isinstance(med, (int, float)) and med == med else "NA"
        print(f"  {mark}  {pw:48s} median log2FC={med_s}  ({info['n_genes_expressed']}/{info['n_genes_tested']} expressed; up={info['n_up']} dn={info['n_dn']})")


if __name__ == "__main__":
    main()

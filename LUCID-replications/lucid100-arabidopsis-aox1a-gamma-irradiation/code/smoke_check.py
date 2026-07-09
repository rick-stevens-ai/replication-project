#!/usr/bin/env python3
"""
LUCID100 slot 40 — smoke check
Paper: Belykh, Velegzhaninov, Garmash (2022) Int J Radiat Biol 98(1):60–68.
DOI: 10.1080/09553002.2022.1998712
PMID: 34714725

The target paper itself is closed access (Taylor & Francis), the AS-12/XX-2
Arabidopsis AOX1a-altered lines + 200 Gy γ-IR qPCR panel were never deposited
to GEO/SRA/ArrayExpress, and supplementary files require the publisher
paywall. So we cannot reproduce the exact numbers.

What we *can* do, from purely public data:
  1. Reconstruct the AGI-locus panel implied by the paper's abstract
     (AOX1a, AOX1d, DNA-repair genes the abstract names as upregulated by
     γ-IR in WT/AS-12, plus the Mn-SOD and AOX-family stress controls).
  2. Cross-validate the directional claim "γ-IR upregulates DNA-repair
     genes in WT Arabidopsis" against the public scaffold dataset
     GSE112773 (Bourbousse et al. 2018 Genome Research — the SOG1 +
     MYB3R DREM time-course of γ-IR in WT and sog1 Arabidopsis), using
     the per-DREM-path AGI gene lists in
     Source_Data_2/Princeton_GO_inputs_GeneListsByPath/.
  3. Report, per panel gene, which DREM dynamic-response paths it
     appears in (W* = wild-type γ-IR paths, S* = sog1 paths), and
     classify each as a "concordant DDR-induction" hit when it lands
     in a WT path that the Bourbousse paper annotates as upregulated.

Pure stdlib. Zero heavy compute. ~50 ms wall time on CherryRd.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GENE_DIR = ROOT / "source" / "GSE112773_SD2" / "Princeton_GO_inputs_GeneListsByPath"
RESULTS = ROOT / "results"
RESULTS.mkdir(parents=True, exist_ok=True)

# ---- Belykh 2021 qPCR panel reconstruction (AGI loci) ----
# Abstract names: AOX1a, AOX1d, AOX protein, DNA repair genes, Mn-SOD, ROS.
# AGI loci taken from TAIR (https://www.arabidopsis.org/) authoritative
# gene-symbol -> AT-locus mapping. Each entry is (symbol, AGI, role).
#
# DNA-repair panel: standard Arabidopsis DDR/HR/NHEJ qPCR panel used across
# the Arabidopsis-IR literature (Culligan 2006 PMID 17056677, Yoshiyama 2009
# PMID 19255495, Bourbousse 2018 PMID 30060114, Missirian 2014 PMID 25201341).
# AOX/antioxidant panel: standard Arabidopsis mitochondrial-AOX panel
# (Vanlerberghe 2013 Int J Mol Sci PMID 23698764; Saika & Maekawa 2018).
PANEL = [
    # Symbol         AGI            Class / role in the paper
    ("AOX1a",        "AT3G22370",   "alternative_oxidase_primary_target"),
    ("AOX1b",        "AT3G22360",   "alternative_oxidase_family"),
    ("AOX1c",        "AT3G27620",   "alternative_oxidase_family"),
    ("AOX1d",        "AT1G32350",   "alternative_oxidase_stress_induced"),
    ("AOX2",         "AT5G64210",   "alternative_oxidase_family"),
    # DNA repair / DDR
    ("ATM",          "AT3G48190",   "DDR_kinase_master"),
    ("ATR",          "AT5G40820",   "DDR_kinase_master"),
    ("SOG1",         "AT1G25580",   "DDR_master_TF_(plant_p53_analog)"),
    ("RAD51",        "AT5G20850",   "HR_strand_exchange"),
    ("RAD54",        "AT3G19210",   "HR_remodeler"),
    ("BRCA1",        "AT4G21070",   "HR_checkpoint"),
    ("PARP1",        "AT4G02390",   "BER_DSB_sensor"),
    ("PARP2",        "AT2G31320",   "BER_DSB_sensor"),
    ("KU70",         "AT1G16970",   "NHEJ_DSB_end_binding"),
    ("KU80",         "AT1G48050",   "NHEJ_DSB_end_binding"),
    ("LIG4",         "AT5G57160",   "NHEJ_ligase"),
    ("OGG1",         "AT1G21710",   "BER_oxidative_damage"),
    ("APE1L",        "AT3G48425",   "BER_AP_endonuclease"),
    ("WEE1",         "AT1G02970",   "cell_cycle_checkpoint_post_DDR"),
    # Antioxidant
    ("MSD1_MnSOD",   "AT3G10920",   "Mn_SOD_mitochondrial"),
    ("FSD1_FeSOD",   "AT4G25100",   "Fe_SOD_chloroplastic"),
    ("CSD1_CuZnSOD", "AT1G08830",   "CuZn_SOD_cytosolic"),
    ("CSD2_CuZnSOD", "AT2G28190",   "CuZn_SOD_chloroplastic"),
    ("CAT1",         "AT1G20630",   "catalase"),
    ("CAT2",         "AT4G35090",   "catalase"),
    ("APX1",         "AT1G07890",   "ascorbate_peroxidase"),
    ("GR1",          "AT3G24170",   "glutathione_reductase"),
]

# WT DREM paths from Bourbousse 2018 that the paper labels as up-regulated
# γ-IR response paths. Path labels W1, W2, W3, W6, W7, W8 = induced;
# W4, W5, W9, W10, W11 = repressed (per their Fig. 1 DREM map).
WT_INDUCED_PATHS = {"W1", "W2", "W3", "W6", "W7", "W8"}
WT_REPRESSED_PATHS = {"W4", "W5", "W9", "W10", "W11"}

def load_path_to_genes():
    if not GENE_DIR.is_dir():
        raise SystemExit(f"missing scaffold gene-list dir: {GENE_DIR}")
    out = {}
    for f in sorted(GENE_DIR.glob("*.txt")):
        out[f.stem] = {line.strip().upper() for line in f.read_text().splitlines() if line.strip()}
    return out

def main():
    paths = load_path_to_genes()
    total_genes_in_scaffold = sum(len(v) for v in paths.values())
    print(f"[scaffold] GSE112773 DREM paths loaded: {len(paths)}")
    print(f"[scaffold] total path memberships: {total_genes_in_scaffold} "
          f"({len(set().union(*paths.values()))} unique AGI loci)")

    out_rows = []
    n_wt_concordant = 0
    n_panel_in_scaffold = 0
    for symbol, agi, role in PANEL:
        agi_u = agi.upper()
        hits = sorted([p for p, genes in paths.items() if agi_u in genes])
        wt_induced_hits = [h for h in hits if h in WT_INDUCED_PATHS]
        wt_repressed_hits = [h for h in hits if h in WT_REPRESSED_PATHS]
        sog1_hits = [h for h in hits if h.startswith("S")]
        in_scaffold = bool(hits)
        if in_scaffold:
            n_panel_in_scaffold += 1
        is_ddr = role.startswith(("DDR", "HR", "NHEJ", "BER", "cell_cycle"))
        concordant = is_ddr and bool(wt_induced_hits)
        if concordant:
            n_wt_concordant += 1
        out_rows.append({
            "symbol": symbol,
            "agi": agi,
            "role": role,
            "in_GSE112773_scaffold": in_scaffold,
            "wt_induced_paths": wt_induced_hits,
            "wt_repressed_paths": wt_repressed_hits,
            "sog1_paths": sog1_hits,
            "concordant_with_belykh_directional_claim": concordant,
        })

    ddr_panel = [r for r in out_rows if r["role"].startswith(("DDR", "HR", "NHEJ", "BER", "cell_cycle"))]
    aox_panel = [r for r in out_rows if "alternative_oxidase" in r["role"]]
    ros_panel = [r for r in out_rows if r["role"] in (
        "Mn_SOD_mitochondrial", "Fe_SOD_chloroplastic",
        "CuZn_SOD_cytosolic", "CuZn_SOD_chloroplastic",
        "catalase", "ascorbate_peroxidase", "glutathione_reductase")]
    ddr_in_scaffold = [r for r in ddr_panel if r["in_GSE112773_scaffold"]]
    ddr_in_scaffold_concordant = [r for r in ddr_in_scaffold if r["concordant_with_belykh_directional_claim"]]
    ddr_in_scaffold_discordant = [r for r in ddr_in_scaffold if r["wt_repressed_paths"] and not r["wt_induced_paths"]]

    summary = {
        "paper_doi": "10.1080/09553002.2022.1998712",
        "paper_pmid": "34714725",
        "paper_status": "closed_access",
        "scaffold_dataset": "GSE112773 (Bourbousse 2018, Genome Research)",
        "scaffold_description":
            "SOG1+MYB3R γ-IR DREM time-course in WT and sog1 Arabidopsis; "
            "we use the per-DREM-path AGI gene lists from "
            "Source_Data_2/Princeton_GO_inputs_GeneListsByPath/",
        "panel_size": len(PANEL),
        "panel_classes": {
            "ddr_panel_size": len(ddr_panel),
            "aox_panel_size": len(aox_panel),
            "antioxidant_panel_size": len(ros_panel),
        },
        "scaffold_coverage": {
            "panel_genes_present_in_scaffold": n_panel_in_scaffold,
            "ddr_panel_genes_in_wt_induced_path": n_wt_concordant,
            "ddr_panel_genes_total": len(ddr_panel),
            "ddr_concordance_rate_all":
                f"{n_wt_concordant}/{len(ddr_panel)}"
                f" = {n_wt_concordant/max(len(ddr_panel),1):.2%}",
            "ddr_panel_genes_detected_in_scaffold": len(ddr_in_scaffold),
            "ddr_concordance_rate_among_detected":
                f"{len(ddr_in_scaffold_concordant)}/{len(ddr_in_scaffold)}"
                f" = {len(ddr_in_scaffold_concordant)/max(len(ddr_in_scaffold),1):.2%}",
            "ddr_panel_genes_discordant":
                [r["symbol"] for r in ddr_in_scaffold_discordant],
        },
        "interpretation":
            "If the Belykh paper's qualitative claim — γ-IR induces "
            "DNA-repair genes in WT Arabidopsis — is reproducible "
            "from independent public data, then most DDR panel members "
            "should land in WT-induced DREM paths (W1/W2/W3/W6/W7/W8). "
            "Hits in W4/W5/W9/W10/W11 = repressed are *discordant*. "
            "Genes absent from the scaffold may simply not pass the "
            "DREM significance filter in Bourbousse 2018.",
        "per_gene": out_rows,
    }

    out_json = RESULTS / "smoke_output.json"
    out_json.write_text(json.dumps(summary, indent=2))
    print(f"[ok] wrote {out_json}")

    print()
    print("=== Per-gene scaffold mapping ===")
    print(f"{'symbol':<14}{'AGI':<14}{'WT-induced':<20}{'WT-repressed':<18}{'sog1':<10}{'class'}")
    for r in out_rows:
        print(f"{r['symbol']:<14}{r['agi']:<14}"
              f"{','.join(r['wt_induced_paths']) or '-':<20}"
              f"{','.join(r['wt_repressed_paths']) or '-':<18}"
              f"{','.join(r['sog1_paths']) or '-':<10}"
              f"{r['role']}")
    print()
    print(f"[summary] DDR panel concordant with Belykh directional claim:")
    print(f"           among ALL DDR panel genes:      "
          f"{n_wt_concordant}/{len(ddr_panel)} "
          f"({n_wt_concordant/max(len(ddr_panel),1):.0%})")
    print(f"           among DDR genes IN scaffold:    "
          f"{len(ddr_in_scaffold_concordant)}/{len(ddr_in_scaffold)} "
          f"({len(ddr_in_scaffold_concordant)/max(len(ddr_in_scaffold),1):.0%})")
    print(f"[summary] DDR genes in scaffold but WT-repressed (discordant): "
          f"{[r['symbol'] for r in ddr_in_scaffold_discordant] or 'none'}")
    print(f"[summary] Total panel genes detected in scaffold: "
          f"{n_panel_in_scaffold}/{len(PANEL)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())

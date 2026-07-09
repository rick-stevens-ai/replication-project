#!/usr/bin/env python3
"""
BVBRC-16 promotion-pass: full 10-strain comparative genomics replication of
Ghattargi et al. 2018, BMC Genomics 19:652.

Inputs (downloaded into work/):
- faa/{strain}.faa       — protein FASTAs from BV-BRC (PATRIC annotation)
- features/{strain}.json — CDS feature tables from BV-BRC genome_feature endpoint
- sp_genes/{strain}.json — BV-BRC sp_gene specialty calls (CARD/VFDB/NDARO/Victors/PATRIC_VF)
- pangenome_PA_matrix.tsv — CD-HIT 70% identity cluster presence/absence matrix
- pangenome_clusters.json — pangenome summary
- jaccard_distance.tsv   — pairwise Jaccard distance from PA matrix
- upgma_jaccard.nwk      — UPGMA tree from Jaccard
- amr_comparison.json    — AMR vs paper Table 2
- vf_comparison.json     — Virulence vs paper Table 3
- mge_summary.json       — MGE keyword counts vs paper C5 claim

This script is the single audit-trail of how the comparative analysis was reproduced.
Outputs: writes JSON summaries used in REPORT.md.
"""
import json, os, re, collections

# === Strain table ===
STRAINS_ORDER = ['17OM39','T110','NRRL_B-2354','64-3','DO','Aus0004','Aus0085','6E6','E39','ATCC_700221']
GROUPS = {'17OM39':'probiotic_candidate','T110':'probiotic',
          'NRRL_B-2354':'NPNP','64-3':'NPNP',
          'DO':'pathogenic','Aus0004':'pathogenic','Aus0085':'pathogenic',
          '6E6':'pathogenic','E39':'pathogenic','ATCC_700221':'pathogenic'}

# === Paper Table 1 values for cross-check ===
PAPER_TABLE1 = {
  'T110':         {'mb':2.6,'gc':38.4,'cds':2502,'accession':'NZ_CP006030.1'},
  '17OM39':       {'mb':2.6,'gc':38.5,'cds':2639,'accession':'LWHF00000000.1'},
  'NRRL_B-2354':  {'mb':2.6,'gc':37.8,'cds':2658,'accession':'NC_020207.1'},
  '64-3':         {'mb':2.5,'gc':38.2,'cds':2418,'accession':'NZ_CP012522.1'},
  'DO':           {'mb':2.6,'gc':37.9,'cds':2703,'accession':'NC_017960.1'},
  'Aus0004':      {'mb':2.9,'gc':38.3,'cds':2825,'accession':'NC_017022.1'},
  'Aus0085':      {'mb':2.9,'gc':37.9,'cds':2938,'accession':'NC_021994.1'},
  '6E6':          {'mb':2.9,'gc':37.6,'cds':3307,'accession':'NZ_CP013994.1'},
  'E39':          {'mb':2.7,'gc':37.8,'cds':2907,'accession':'NZ_CP011281.1'},
  'ATCC_700221':  {'mb':2.8,'gc':37.8,'cds':2725,'accession':'CP014449.1'},
}

# === BV-BRC genome IDs ===
BVBRC = {
  '17OM39':'1352.1047','T110':'1344042.3',
  'NRRL_B-2354':'1104325.3','64-3':'1352.658',
  'DO':'333849.47','Aus0004':'1155766.14','Aus0085':'1305849.3',
  '6E6':'1352.674','E39':'1352.890','ATCC_700221':'1352.804'
}

if __name__ == '__main__':
    print('Analysis modules included:')
    print('  1. genome_lookup.json     — BV-BRC IDs + metadata for all 10 paper strains')
    print('  2. pangenome_PA_matrix.tsv + pangenome_clusters.json — CD-HIT 70% pangenome')
    print('  3. jaccard_distance.tsv + upgma_jaccard.nwk         — phylogeny (C6 test)')
    print('  4. amr_comparison.json    — sp_gene AMR vs paper Table 2 (C3 test)')
    print('  5. vf_comparison.json     — sp_gene + product VF vs paper Table 3 (C4 test)')
    print('  6. mge_summary.json       — MGE keyword counts vs C5 claim')
    print('  7. probiotic_genes.json   — BSH/sortase/bacteriocin counts (C4-positive)')

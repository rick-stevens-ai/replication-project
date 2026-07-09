# LUCID100 Wave 3 / Slot 29 — DNA-PKcs in Adaptive Survival Responses

## Paper
- **Title:** DNA-dependent Protein Kinase Does Not Play a Role in Adaptive Survival Responses to Ionizing Radiation
- **Authors:** Eric Odegaard, Chin-Rang Yang, David A. Boothman
- **Affiliation:** Department of Human Oncology and University of Wisconsin Comprehensive Cancer Center, UW–Madison
- **Venue:** Environ Health Perspect 106(Suppl 1):301–305 (Feb 1998)
- **DOI:** 10.1289/ehp.98106s1301
- **PMC:** PMC1533273
- **Funding:** US DOE grant DE-FG0293ER61707-06

## Context in LUCID100
- **Rank 60 / Wave 3 / Tier A / priority 15** in `LUCID100_SOLID_MASTER_QA.tsv`.
- **Master worktype tag:** `omics/signature replication`.
- **CORRECTED worktype after reading paper:** `table/figure replication + statistical verification` (NOT omics, NOT signature). The paper contains zero omics data — it is a small clonogenic-survival paper (1 table) plus 2 flow-cytometry figures. See `FIRST_PASS_REPORT.md` for QA retag recommendation.

## Folder Layout
```
.
├── README.md                  (this file)
├── PROGRESS.md                (running log)
├── FIRST_PASS_REPORT.md       (verdict + replication scoping)
├── ARTIFACT_MANIFEST.md       (all retrieved + tried artifacts)
├── paper/
│   ├── main.pdf               (Open-access PDF from EuropePMC PMC1533273)
│   └── main.txt               (pdftotext layout dump)
├── data/
│   └── table1_extracted.tsv   (Table 1 transcribed by hand from paper)
├── code/
│   └── replicate_table1.py    (smoke replication: fold enhancement, error propagation)
├── results/
│   └── table1_replication.tsv (script output)
└── figures/                   (placeholder for digitized Fig 1 / Fig 2 if pursued)
```

## What was replicated
- All 12 numeric cells of Table 1 transcribed and re-arithmetic'd.
- Fold-enhancement (primed vs. unprimed challenged) recomputed with Gaussian error propagation; matches the paper's "2-fold" verbal claim within stated SD.
- See `FIRST_PASS_REPORT.md` for verdict and what is NOT replicable from published material alone.

## Heavy-compute job plan
None required. Everything is < 1 second of arithmetic on a laptop. No CherryRd risk.

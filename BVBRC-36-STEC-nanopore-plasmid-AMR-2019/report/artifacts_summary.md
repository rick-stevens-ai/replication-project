# Artifacts Summary — BVBRC-36 (González-Escalona et al. 2019, STEC nanopore)

## 8-artifact standard status

| # | Artifact | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | **PRESENT** (in `work/paper.pdf`) | PLOS OA (CC0), fully accessible via PMC6667211. Symlink to top-level recommended. |
| 2 | `extraction/marker.md` | Needs backfill | Paper is OA; `work/fulltext.xml` + `work/fulltext_plain.txt` already present from Europe PMC. Marker parse straightforward. |
| 3 | `extraction/nougat.mmd` | Needs backfill | Same source; add to Kukla's Eagle batch queue. |
| 4 | `report/REPORT.tex` (+ .md) | **PRESENT** | Detailed section-by-section LaTeX with dedicated genuine-critique section. REPORT.md is the primary narrative. |
| 5 | `report/open_questions.json` | **PRESENT** | 5 heavy-duty open questions with basis + next_steps grounded in the paper's methodological thesis and this replication's honest scope limits. |
| 6 | `report/workflow.md` | **PRESENT** | Full workflow + tools + compute estimate. |
| 7 | `report/artifacts_summary.md` | **PRESENT** | This file. |
| 8 | `report/failure_analysis.md` | **PRESENT** | Honest failure analysis. |

## Evidence / traces

```
BVBRC-36-STEC-nanopore-plasmid-AMR-2019/
├── paper.pdf (RECOMMENDED: symlink to work/paper.pdf)
├── work/
│   ├── paper.pdf, fulltext.xml, fulltext_plain.txt
│   ├── genomes/CP0379{41..47}.fna       (7 deposited replicons)
│   ├── refdb/{resfinder,vfdb,ecoli_vf,plasmidfinder}.fa
│   ├── mlst/{adk,fumC,gyrB,icd,mdh,purA,recA}.tfa, profiles.tsv
│   ├── blast_out/                       (per-replicon blastdbs)
│   ├── run_blast.py → blast_results.json
│   ├── summarize.py → gene_summary.json
│   ├── mlst.py → mlst_results.json
│   ├── genome_stats.py → genome_stats.json
│   ├── stx_location.py → stx_location.json
│   └── judge.py → judge_verdict.json
├── report/
│   ├── REPORT.md                        (primary narrative, verdict REPLICATED)
│   ├── REPORT.tex                       (8-artifact LaTeX + critique)
│   ├── open_questions.json              (5 questions)
│   ├── workflow.md
│   ├── artifacts_summary.md             (this file)
│   ├── failure_analysis.md
│   ├── brief.md, attempt_log.md, artifact_harvest.md
│   └── evidence/                        (mirrors JSON outputs)
└── extraction/
    ├── marker.md                        (NEEDS BACKFILL)
    └── nougat.mmd                       (NEEDS BACKFILL)
```

## Reproduced key numbers (traceable to work/*.json)

- 7/7 replicons match paper sizes: 5,689,156 / 5,592,581 / 5,436,079 bp chromosomes; 88,848 / (96,016 + 73,152) / 157,534 bp plasmids.
- MLST 3/3 EXACT: 343=346=ST21 (adk-16); 350=ST29 (adk-6).
- AMR EXACT 6/6 for CFSAN027346: aph(3'')-Ib, aph(6)-Id, **blaTEM-1B**, sul2, tet(B), **dfrA8** — all on CP037947 (73 kb IncFII plasmid). ZERO AMR in 343 or 350.
- Virulome: all strain-dependent patterns match (Stx type; toxB, katP, tccP, espI).
- Stx phage types 3/3 (stx1a/stx1a/stx2a) chromosomal.
- Plasmid replicons: IncFIB(AP001918)+IncB/O/K/Z on virulence plasmids; IncFII(pHN7A8) 98% on AMR plasmid.

## Verdict: REPLICATED
Every core data-grounded claim (C1–C8) reproduces; AMR EXACT to allele. LLM-judge coverage 9/10, agreement 10/10.

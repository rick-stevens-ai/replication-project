# Artifacts Summary — BVBRC-63 (Yasuike et al. 2017, *N. seriolae* UTF1)

## 8-artifact standard status

| # | Artifact | Status | Notes |
|---|---|---|---|
| 1 | `paper.pdf` | Check work/ | PLOS OA (CC BY), PMID 28257489 — freely available; ensure top-level paper.pdf present or symlink. |
| 2 | `extraction/marker.md` | Needs backfill | Paper is OA; Marker parse straightforward when weights available. |
| 3 | `extraction/nougat.mmd` | Needs backfill | Add to Kukla's Eagle batch queue. |
| 4 | `report/REPORT.tex` (+ .md) | **PRESENT** | Detailed section-by-section LaTeX with dedicated genuine-critique section. REPORT.md is primary narrative. |
| 5 | `report/open_questions.json` | **PRESENT** | 5 heavy-duty open questions with basis + next_steps. |
| 6 | `report/workflow.md` | **PRESENT** | Workflow + tools + compute estimate. |
| 7 | `report/artifacts_summary.md` | **PRESENT** | This file. |
| 8 | `report/failure_analysis.md` | **PRESENT** | Honest failure analysis. |

## Evidence / traces

```
BVBRC-63-nocardia-seriolae-utf1/
├── report/
│   ├── REPORT.md                     (primary narrative, verdict REPLICATED)
│   ├── REPORT.tex                    (8-artifact LaTeX + critique)
│   ├── open_questions.json           (5 questions)
│   ├── workflow.md
│   ├── artifacts_summary.md          (this file)
│   ├── failure_analysis.md
│   └── evidence/
│       └── llm_judge.txt             (Argo opus-4.7 verdict)
└── work/
    ├── GCF_002356035.1.fna           (UTF1 assembly)
    ├── prokka_out/                   (independent re-annotation)
    ├── comparator genomes (4x RefSeq .faa)
    ├── UTF1_vs_<target>_v2.tsv       (RBH BLASTP outputs)
    └── functional-category counts
```

## Reproduced key numbers (traceable to work/)

- Chromosome 8,121,733 bp (EXACT); GC 68.14% (paper 68.1%)
- CDS: RefSeq 7,650 / Prokka 7,648 (paper 7,697; 99.4%)
- 12 rRNA / 4 operons (EXACT)
- Core orthologs 2,718 (paper 2,745; 99.0%)
- UTF1-unique 1,967 (paper 1,982; 99.2%)
- Mobile elements UTF1 127 vs comparators 20-43 (3.0-6.4x enrichment, STRONG)
- Virulence orthologs: Mce 21, catalase/SOD 4, siderophore 3, efflux 11, beta-lactamase 1

## Verdict: REPLICATED
10/10 claims tested; 8 confirmed, 2 partial (C8/C9 coarse-proxy scope gap), 0 contradicted. LLM judge concurs (~85% strength).

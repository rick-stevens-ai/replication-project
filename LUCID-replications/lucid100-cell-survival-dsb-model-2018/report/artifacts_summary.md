# Artifacts Summary --- Wang 2018 DSB Cell-Survival Replication

## Directory inventory (as of backfill 2026-07-06)

```
lucid100-cell-survival-dsb-model-2018/
├── REPORT.md                          19,254 B  Original 2026-06-21 replication report
├── paper.pdf                       3,058,878 B  Wang et al. 2018 (sha256: 429bf7d8bc5b767b9d39da63031a281f3c6994d11414a60b99f604ebae43a92a)
├── paper.txt                          73,154 B  Full text extraction
├── paper.html                        431,005 B  Nature HTML mirror
├── data/                                       (empty --- PIDE + Furusawa not accessible)
├── src/
│   ├── wang2018_model.py               6,243 B  All 20 equations, both cell lines
│   ├── test_headline_claims.py         5,247 B  Headline-claim numerical tests
│   ├── find_Y_from_D10.py              1,932 B  Inverse-solve Y_X from paper D10
│   ├── figure_survival.py              3,832 B  Fig 2c,d replica generator
│   ├── figure_alpha_beta_LET.py        2,935 B  Fig 2 alpha,beta vs LET replica
│   └── mcds_promotion_test.py          5,613 B  MCDS 3.10A promotion test (2026-06-21)
├── figures/
│   ├── fig2cd_xray_survival.png      108,211 B  X-ray survival replica
│   └── fig2_alpha_beta_vs_LET.png    107,902 B  alpha, beta vs LET replica
├── results/
│   ├── headline_test.txt               2,151 B  Algebraic verification output
│   ├── inverse_fit_Y.txt                 948 B  Y_X free-fit result
│   ├── figure_survival.log               691 B
│   ├── figure_alpha_beta.log             220 B
│   └── mcds_promotion_result.txt       2,197 B  MCDS 3.10A test result (STAYS PARTIAL)
└── report/                                      (this backfill dir, 2026-07-06)
    ├── REPORT.tex                              LaTeX report with critique
    ├── open_questions.json                     5 open questions (JSON)
    ├── open_questions_section.tex              LaTeX Open Questions section
    ├── workflow.md                             Workflow + reproducer
    ├── artifacts_summary.md                    This file
    └── failure_analysis.md                     Honest failure critique
```

## Artifact classification

| Category | Count | Files |
|---|---|---|
| Paper source (present) | 3 | paper.pdf, paper.txt, paper.html |
| Model code | 6 | src/*.py |
| Generated figures | 2 | figures/*.png |
| Result logs | 5 | results/*.{txt,log} |
| Original writeup | 1 | REPORT.md |
| Backfill artifacts (this task) | 6 | report/* (REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md) |
| **Total files** | **23** | |

## Extraction traces

- **No nougat parse performed.** Paper.pdf is present; a text extraction (paper.txt, 73 kB) is present from the original replication. A stub `extraction/nougat.mmd` is written pointing at the paper.pdf sha256 for downstream OCR provenance.
- **No new heavy compute this backfill.** All artifacts derive from re-reading paper.pdf + REPORT.md + results/.

## Friction tags

| Tag | Where | What |
|---|---|---|
| `data-blocker:PIDE` | REPORT.md §2.3, workflow.md, failure_analysis.md | PIDE v3.2 requires institutional registration + manual approval; blocks 106-curve raw refit. |
| `data-blocker:paywall` | REPORT.md §2.3, workflow.md | Furusawa 2000 raw survival points behind BioOne. Same blocker. |
| `tool-not-installed:MCDS` | REPORT.md §2.3, mcds_promotion_test.py | MCDS 3.10A installed later by Kukla; used in promotion test but result was NEGATIVE (D10 27-30 Gy vs 4.08/7.07). |
| `paper-omission:Y_table` | REPORT.md §2.2, failure_analysis.md, Q1 | Wang 2018 does not publish the MCDS Y(LET) input table. Root cause of the parameterization non-reproducibility. |
| `verdict-mismatch:queue-vs-REPORT` | This backfill, failure_analysis.md | Queue says REPLICATED; REPORT.md says PARTIAL; 2026-06-21 MCDS promotion appendix explicitly says "STAYS PARTIAL". Preserving PARTIAL. |
| `in-sample-only` | failure_analysis.md, Q2 | Paper reports in-sample R^2 on the 106 fitted curves; no held-out validation. |
| `phenomenological-not-mechanistic` | REPORT.tex critique | Paper frames model as mechanistic; parameters are effective fit coefficients. |

## Verdict trace

| Timestamp | Source | Verdict | Rationale |
|---|---|---|---|
| 2026-06-21 (original) | REPORT.md §5 | PARTIAL | 6/30 claims tested; PIDE/MCDS blockers |
| 2026-06-21 (MCDS test appendix) | REPORT.md §7 | PARTIAL (confirmed) | First-principles Y_X gave D10 +324-569% error |
| (unknown timestamp) | Queue file | REPLICATED | **Mismatch** --- source unclear |
| 2026-07-06 (this backfill) | report/REPORT.tex | PARTIAL (preserved) | Preserving the actual, honest verdict from REPORT.md |

## Reproducer (from workflow.md)

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-cell-survival-dsb-model-2018
python3 src/test_headline_claims.py     # algebraic
python3 src/find_Y_from_D10.py          # inverse solve
python3 src/figure_survival.py          # Fig 2c,d
python3 src/figure_alpha_beta_LET.py    # Fig 2 e,f-style
python3 src/mcds_promotion_test.py      # MCDS 3.10A test
```

All deterministic, ~5 s total wall.

# Workflow — BVBRC-124

## High-level flow
```
┌──────────────────────────────┐   ┌──────────────────────────┐   ┌──────────────────┐
│ paper.pdf (EuropePMC PMC6…) │──▶│ pdftotext -layout        │──▶│ extraction/       │
└──────────────────────────────┘   └──────────────────────────┘   │  marker.md +      │
                                                                   │  nougat.mmd stub  │
                                                                   └──────────────────┘

┌──────────────────────────────┐   ┌──────────────────────────┐
│ github.com/erolkavvas/       │──▶│ work/data/*.csv           │
│ microbial_AMR_ML             │   │   pangen_allele_df,       │
│ (5 CSVs, ~85 MB, real matrix)│   │   pangen_cluster_df,      │
└──────────────────────────────┘   │   cluster_info,           │
                                    │   resistance_data,        │
┌──────────────────────────────┐   │   strain_information      │
│ Springer supplementary       │──▶│ work/data/MOESM{1,4,5,7,9}│
│ MOESM PDFs+XLSX (via BVBRC-90│   └──────────────┬────────────┘
│ mirror, actually public)     │                  │
└──────────────────────────────┘                  ▼
                                    ┌──────────────────────────┐
                                    │ auc_replicate.py         │
                                    │  • load 1595×15367 matrix│
                                    │  • NaN → 0 fix           │
                                    │  • per-drug 5-fold CV    │
                                    │  • L1-SVM + L2-logistic  │
                                    │  • 240 s single-node     │
                                    └──────────────┬───────────┘
                                                   ▼
                                    report/evidence/auc_per_drug.json

┌──────────────────────────────┐   ┌──────────────────────────┐
│ RCSB REST API                │──▶│ structural_map.py         │
│ search.rcsb.org/rcsbsearch/v2│   │  • 20 (Rv,gene) pairs     │
└──────────────────────────────┘   │  • text + taxon queries   │
                                    │  • 30 s                   │
                                    └──────────────┬───────────┘
                                                   ▼
                                    report/evidence/structural_availability.json

                                    ┌──────────────────────────┐
                                    │ llm_judge.py             │
                                    │  Argo :44497             │
                                    │  argo:gpt-5.2 (free)     │
                                    └──────────────┬───────────┘
                                                   ▼
                                    report/evidence/llm_judge_verdict.json
                                                   │
                                                   ▼
                                          REPORT.md / REPORT.tex
```

## Tools & versions
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14.6 (CherryRd) | driver |
| numpy | 2.4.3 | array ops |
| pandas | 3.0.2 | CSV load, indexing |
| scikit-learn | 1.8.0 | SGDClassifier, LogisticRegression, StratifiedKFold, roc_auc_score |
| scipy | 1.18.0 | dependency |
| poppler pdftotext | 26.06.0 | marker-equivalent text extraction |
| urllib (stdlib) | 3.14 | RCSB REST + Argo REST |
| Argo proxy | localhost:44497 (free) | LLM judge via `argo:gpt-5.2` |
| RCSB Search API | v2 (rcsbsearch/v2/query) | structural probe |

Source data:
* `github.com/erolkavvas/microbial_AMR_ML` (authors' repo, public, MIT-adjacent).
* Springer static-content MOESM XLSX (open access via CC BY 4.0 paper).
* EuropePMC PMC6193043 (paper PDF).

## Effort estimate (this subagent turn)
| Phase | Wall time | Notes |
|---|---|---|
| Read wave brief + sibling replications | ~3 min | 2 prior passes reviewed |
| Fetch paper.pdf | ~5 s | EuropePMC direct |
| Copy allele/phenotype CSVs from sibling BVBRC-25 | <1 s | data was already downloaded from authors' GitHub in prior pass |
| Copy Springer MOESM from BVBRC-90 mirror | <1 s | |
| Write auc_replicate.py + debug NaN-cast bug | ~5 min | one failed run + fix |
| Run auc_replicate.py | 4 min | 240 s CPU, 15 drugs × 5 folds × 2 classifiers |
| Write + run structural_map.py | ~2 min | includes RCSB query |
| Write + run llm_judge.py (1 model-swap after 502) | ~2 min | argo claude-opus-4.8 down; gpt-5.2 works |
| Assemble 8 artifacts (REPORT.md, REPORT.tex, workflow.md, brief.md, open_questions.json, artifacts_summary.md, failure_analysis.md, attempt_log.md, artifact_harvest.md) | ~15 min | |
| **Total wall time** | **~35 min** | one subagent, no user intervention |
| **Compute** | 1 CPU-core-4-min + 3 network calls | trivial; uicgpu unnecessary |

## Why no uicgpu?
The wave brief allows uicgpu for heavy compute, but this pass's largest job
(5-fold CV × 15 drugs × 2 classifiers on a 1500×15k dense matrix) completes
in 240 s on a single CherryRd core. Pushing to uicgpu would add SSH-latency
overhead and Dropbox-sync round-trips that dominate the compute time.
Documented for reproducibility auditors.

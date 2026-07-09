# Artifacts Summary — Brandt (1977) Multigrid Replication

Inventory of every file produced by this replication, with size/purpose/provenance.

## Source paper
| File | Purpose | Provenance |
|---|---|---|
| `work/brandt1977.pdf` | Achi Brandt (1977), *Multi-Level Adaptive Solutions to Boundary-Value Problems*, Math. Comp. 31(138), pp. 333–390 | AMS open-access, SHA-256 `d4f187bd5bcdb5262214598ab33a98d83affe390800e3b246964746d35089e5b`, 6.1 MB |
| `work/brandt1977.txt` | Layout-preserving text extraction | `pdftotext -layout brandt1977.pdf` |

## Code (all from-scratch)
| File | LOC | Purpose |
|---|---|---|
| `work/multigrid.py` | ~330 | V(2,1) multigrid solver: red-black GS smoother, full-weighting restriction, bilinear prolongation, dense coarse solve. Runs C1/C2/C3 experiments in one pass. Emits `report/evidence/results.json` and `run_log.txt`. |
| `work/plot_results.py` | ~80 | Generates 3-panel composite figure `brandt_replication_summary.png` from `results.json`. |
| `work/llm_judge.py` | ~90 | Sends REPORT.md + results.json to Argo `claude-sonnet-4.6` at `127.0.0.1:44497` (key `stevens`, T=0.0), parses judgment, emits `llm_judgment.json` and `llm_judge_raw.txt`. |

## Numerical evidence
| File | Purpose |
|---|---|
| `report/evidence/results.json` | All numeric results for C1 (per-grid ρ, cycle counts), C2 (per-grid cycles/WU/wall), C3 (per-grid ε_∞/ε_2 and fitted order p) |
| `report/evidence/run_log.txt` | Verbatim stdout of `multigrid.py` full run — reproducible trace |
| `report/evidence/brandt_replication_summary.png` | 3-panel figure: residual histories, ρ vs N, ε_∞ vs h |

## LLM-judge evidence
| File | Purpose |
|---|---|
| `report/evidence/llm_judgment.json` | Parsed judge verdict (C1 PARTIAL, C2 REPRODUCED, C3 REPRODUCED, overall REPLICATED) |
| `report/evidence/llm_judge_raw.txt` | Verbatim Argo response, unedited |

## Reports & narratives
| File | Purpose |
|---|---|
| `report/REPORT.md` | Main replication narrative — paper summary, method, per-claim results, LLM verdict, files inventory |
| `report/REPORT.tex` | LaTeX version with dedicated GENUINE CRITIQUE section |
| `report/brief.md` | One-page brief for cross-project index |
| `report/attempt_log.md` | Chronological attempt log (choices, dead ends) |
| `report/artifact_harvest.md` | Provenance record for downloaded/generated artifacts |
| `report/open_questions.json` | 5 open questions grounded in this run (V/W/FMG cycles, smoothing analysis, C1 discrepancy, C4 domain shape, anisotropy) |
| `report/workflow.md` | Chronological workflow, command-by-command |
| `report/artifacts_summary.md` | (this file) inventory |
| `report/failure_analysis.md` | What did NOT work / what was over-claimed / where the replication is thin |

## Directory layout
```
PDE-Brandt-multigrid-BVP-1977/
├── extraction/
│   └── marker.md                    (paper extraction, currently empty/absent)
├── report/
│   ├── REPORT.md, REPORT.tex
│   ├── brief.md, attempt_log.md, artifact_harvest.md
│   ├── open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md
│   └── evidence/
│       ├── results.json, run_log.txt
│       ├── llm_judgment.json, llm_judge_raw.txt
│       └── brandt_replication_summary.png
└── work/
    ├── brandt1977.pdf, brandt1977.txt
    ├── multigrid.py, plot_results.py, llm_judge.py
```

## Reproducibility
Single-command reproduction (from `work/`):
```bash
python3 multigrid.py && python3 plot_results.py && python3 llm_judge.py
```
Runtime: ~2 s numerical + ~5–10 s for LLM judge round-trip.
Dependencies: Python 3.14.6, NumPy, matplotlib (plot only), requests (judge only). No external multigrid library.

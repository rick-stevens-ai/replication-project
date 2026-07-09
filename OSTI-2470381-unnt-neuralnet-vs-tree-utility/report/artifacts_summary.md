# Artifacts Summary — OSTI 2470381 (UNNT)

**Paper:** Gutta et al. (2024), *UNNT: A novel Utility for comparing Neural Net and Tree-based models.* PLoS Comp Biol 20(4):e1011504. DOI [10.1371/journal.pcbi.1011504](https://doi.org/10.1371/journal.pcbi.1011504).
**Verdict:** REPLICATED

---

## Paper artifact
| Item | Value |
|---|---|
| OSTI id | 2470381 |
| PDF source | `https://www.osti.gov/servlets/purl/2470381` |
| PDF size | 456,529 B |
| PDF SHA-256 | `80fcdaf83356718f81b8fa9a75d104c27e677ab2ce0459e0aabea7163c33fab6` |
| PDF text extraction | `pdftotext -layout` → 619 lines |

## Code artifact
| Item | Value |
|---|---|
| Repository | `https://github.com/vgutta/UNNT` |
| Commit pinned | `c34567b1c9595879a0eade8cb641c7630b69a7ed` |
| License | MIT |
| Clone method | `git clone --depth 1` (from `uicgpu`) |
| Language | Python |
| Local modifications | (1) added empty `xgb/__init__.py`; (2) added `run_xgb_only.py` shim that skips the Keras-2.3 import. No changes to upstream logic. |

## Data artifact
| Item | Value |
|---|---|
| Dataset | NCI60 FDA-drug subset (bundled with repo at `data/`) |
| File count | 7 |
| Total size | ~113 MB |
| Per-file sha256 | recorded in `artifact_harvest.md` |
| Corresponds to paper | Tables 2, 8, 9, 10, 11 |
| NOT shipped | Full 30k-drug NCI60 (needed for Tables 1, 4, 5, 6, 7); would require MoDaC/JDACS4C credentials — out of scope |

## Compute environment
| Item | Value |
|---|---|
| Host | `uicgpu` (accessed via `ssh uicgpu` from CherryRd) |
| GPU | 8× NVIDIA A100 40 GB (one A100 used) |
| CPU | Dual AMD EPYC, 47 usable cores exposed |
| OS/toolchain | modern Linux + CUDA 12.8 |
| Env manager | conda / mamba, env name `unnt-repl` |
| Python | 3.11 |
| Key libs | xgboost 2.1.4 (CUDA 12.8, `hist`), scikit-learn 1.5.2, pandas 2.3.3, numpy 1.26.4, PyTorch 2.12.1 (CPU-only for MLP surrogate) |

## Replicator-produced work artifacts
Under `work/` on uicgpu:
| Path | Purpose |
|---|---|
| `run_xgb_only.py` | Shim that instantiates UNNT's `Tree` class exactly as `unnt.py` does, skipping the Keras-2.3 CNN import |
| `work/multiseed_run.py` | Seeded XGBoost multi-seed sweep (0, 1, 2 CPU + 0 GPU) |
| `work/mlp_run.py` | PyTorch matched-architecture MLP surrogate for the CNN claim (widths [1000,500,100,50], SGD lr=0.01, tanh/ReLU, MSE, dropout 0.1) |

## Evidence artifacts
Under `report/evidence/`:
| Path | Purpose |
|---|---|
| `xgb_multiseed.log` | Full runtime log for stages 6–7 (all XGBoost seeds, CPU and GPU) |
| `llm_judge_verdict.json` | Prompt + full JSON response from Argo `gpt-5.2` LLM-judge classification |

## Report artifacts
Under `report/`:
| Path | Purpose |
|---|---|
| `REPORT.md` | Canonical narrative report |
| `REPORT.tex` | LaTeX report with dedicated Genuine Critique section |
| `open_questions.json` | 5 truly-open follow-up research questions grounded in the paper's domain |
| `workflow.md` | Step-by-step replication workflow |
| `artifacts_summary.md` | This file — artifact inventory |
| `failure_analysis.md` | What did not work and why |

## Reproducibility one-liner
Anyone with `ssh uicgpu` access, the conda env recipe above, and a `git clone` at commit `c34567b` can reproduce the R² 0.76–0.79 XGBoost numbers and the R² ≈ –1 to +0.68 MLP-surrogate numbers deterministically by fixing the seed (0/1/2/42) via `work/multiseed_run.py --seed <N>` and `work/mlp_run.py --seed <N> --epochs {1,5} --activation {tanh,relu}`. Absolute reproduction of the paper's R² 0.84 requires removing the undocumented `sample(frac=0.1)` call in `xgboost_preprocess.py` — see `failure_analysis.md`.

## Not reproduced (documented, in scope)
| Claim | Reason |
|---|---|
| C1 (full-NCI60 XGB) | Full 30k-drug dataset not shipped |
| C4 (full-drug XGB CPU vs V100 timing) | Full dataset not shipped |
| C6 (full-drug CNN CPU-faster-than-GPU) | Full dataset not shipped + TF1/Keras-2.3 stack unrunnable |

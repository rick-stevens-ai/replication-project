# Artifacts Summary — Poisson Neural Networks (Jin 2022) Replication

All paths relative to
`~/Dropbox/REPLICATE-PROJECT/PDE-Jin-PoissonNeuralNetworks-2022/` unless
otherwise noted.

## Report artifacts (`report/`)
| File | Purpose |
|---|---|
| `REPORT.md`             | Canonical Markdown report (verdict: REPLICATED). |
| `REPORT.tex`            | LaTeX report with dedicated `GENUINE CRITIQUE` section. |
| `brief.md`              | Short pre-run brief (paper summary + planned method). |
| `attempt_log.md`        | Chronological log of the replication attempt. |
| `artifact_harvest.md`   | Full artifact inventory as harvested from the run. |
| `open_questions.json`   | Five truly-open questions grounded in this replication. |
| `workflow.md`           | End-to-end reproducible workflow. |
| `failure_analysis.md`   | Deviations, sub-claim scope gaps, unattempted extensions. |

## Evidence (`report/evidence/`)
| File | Content |
|---|---|
| `lv_result.json`         | Numeric results dump: per-model rollout-MSE table + invariant-drift table. |
| `lv_trajectories.npz`    | 1000-step rollouts (PNN, MLP, SV ground truth) for all 3 ICs. |
| `lv_train.log`           | Training log (loss curves, wall-time, config echo). |
| `lv_phase_portrait.png`  | Phase-space overlay: PNN vs MLP vs SV ground truth. |
| `lv_rollout_mse.png`     | Per-step rollout MSE curves (log-y). |
| `lv_H_drift.png`         | Per-step invariant drift `|H_n − H_0|`. |
| `judge_argo.json`        | LLM-judge verdict (Argo argo:claude-opus-4.7). |

## Code and inputs (`work/`)
| File | Content |
|---|---|
| `lv_replicate.py`     | Driver script (data gen → train PNN + MLP → rollout → metrics → dump). |
| `pnn/`                | Authors’ reference implementation, cloned unchanged from `github.com/jpzxshi/pnn`. |
| `PNN_arxiv.pdf`       | Paper PDF (arXiv:2012.03133v1). |
| `PNN_arxiv.txt`       | Text extract of paper. |

## Key numeric summary (from `REPORT.md`)
| Metric | PNN (816 params) | MLP baseline (12 802 params) | Reference (SV) |
|---|---:|---:|---:|
| Rollout MSE @ step 100  | 4.89e-3 | 4.89e-3 | — |
| Rollout MSE @ step 500  | 5.01e-3 | 2.24e-2 | — |
| Rollout MSE @ step 1000 | 3.61e-3 | **1.63e-1** | — |
| Mean MSE 1–1000         | 1.03e-2 | 3.15e-2 | — |
| max `|H_n − H_0|`       | 5.81e-3 | 2.98e-2 | 4.77e-7 |
| `|H_n − H_0|` @ step 1000 | 1.41e-3 | 2.88e-2 | 2.38e-7 |
| Wall time (30k iters, A100) | 311 s | 61 s | — |

## Verdict
- Overall: **REPLICATED**.
- C1 (architectural Poisson preservation): OUT-OF-SCOPE (indirect only).
- C2 (long-time rollout stability vs unstructured baseline): **REPLICATED**.
- C3 (invariant drift): **REPLICATED**.
- C4, C5, C6: **NOT ATTEMPTED** in this rerun (claims-in-good-standing).

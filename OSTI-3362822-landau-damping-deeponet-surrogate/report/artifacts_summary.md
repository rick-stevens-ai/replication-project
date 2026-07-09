# Artifacts summary — OSTI 3362822

All paths relative to `~/Dropbox/REPLICATE-PROJECT/OSTI-3362822-landau-damping-deeponet-surrogate/`.

## Standard 8 replication artifacts (Rick 2026-07-05)

| # | artifact | path | size | source |
| --- | --- | --- | --- | --- |
| 1 | Original PDF | `paper.pdf` | 2.5 MB | https://www.osti.gov/servlets/purl/3362822 |
| 2 | Marker markdown | `extraction/marker.md` | 32 KB | `marker_single` on uicgpu GPU 6 |
| 3 | Nougat mmd | `extraction/nougat.mmd` | 26 KB | `nougat` (gpustor env) on uicgpu |
| 4 | LaTeX detailed report | `report/REPORT.tex` (+ `REPORT.pdf` 227 KB, 5 pages) | 11.7 KB tex | this replication |
| 5 | 5 open questions JSON | `report/open_questions.json` | 6.0 KB | this replication |
| 6 | Workflow narrative | `report/workflow.md` | 5.7 KB | this replication |
| 7 | Artifacts summary | `report/artifacts_summary.md` | THIS FILE | this replication |
| 8 | Failure analysis | `report/failure_analysis.md` | | this replication |

## Additional narrative + logs

| path | size | purpose |
| --- | --- | --- |
| `report/REPORT.md` | 11 KB | Full markdown replication report |
| `report/brief.md` | 1.3 KB | One-paragraph what/why |
| `report/attempt_log.md` | | Chronological log of what worked / failed |
| `report/artifact_harvest.md` | | Every public artifact pulled (URLs, sizes) |
| `report/evidence/step1-baseline-results.json` | 3.7 KB | Analytic-rate table + baseline VP-sim γ + inference bench + v1 training curve |
| `report/evidence/final-retrain2-results.json` | 2.3 KB | v2 DeepONet training curve + final rel-L2 errors |
| `report/evidence/llm_judge.json` | ~4 KB | argo:gpt-5.2 verdict object + raw response |

## Datasets + predictions

| path | size | contents |
| --- | --- | --- |
| `report/evidence/dataset_single.npz` | 808 KB | 200 train + 50 test VP trajectories (T ∈ [0.5, 1.5], k=0.35, A=0.05) |
| `report/evidence/final-predictions.npz` | 1.2 MB | v2 DeepONet predictions on all 250 samples + rel-L2 arrays + t_grid |

## Figures

| path | size | content (paper analogue) |
| --- | --- | --- |
| `report/evidence/fig2_dispersion.png` | 47 KB | Analytic ω_r(k) + γ(k) dispersion, k=0.35 marked (paper Fig 2) |
| `report/evidence/fig_baseline_damping.png` | 54 KB | Baseline VP sim log|E_x| vs t + analytic envelope (paper Fig 3 top-left) |
| `report/evidence/fig3_repl_deeponet_vs_sim.png` | 263 KB | 6 test-case DeepONet-vs-reference E(t) (paper Fig 3) |
| `report/evidence/fig_err_dist.png` | 45 KB | Histogram of train/test rel-L2 vs paper's mean lines + T-scatter (paper Fig 8) |

## Code + logs

| path | size | contents |
| --- | --- | --- |
| `work/replicate.py` | 17 KB | End-to-end: dispersion, VP solver, dataset gen, DeepONet v1, inference bench |
| `work/retrain.py` | 5.3 KB | Retrain v1.5 (Fourier features from cached dataset) |
| `work/retrain2.py` | 5.9 KB | Retrain v2 (canonical: Fourier + cosine + best-test) |
| `work/replicate.log` | 4.1 KB | v1 training log (shows plateau at MSE 0.478) |
| `work/retrain.log` | 1.6 KB | v1.5 training log (intermediate) |
| `work/retrain2.log` | 2.7 KB | v2 canonical training log (best test MSE 0.0123) |
| `work/marker.log` | 6.2 KB | Marker extraction log |
| `work/nougat.log` | 1.1 KB | Nougat extraction log |
| `work/paper_pdftotext.txt` | 43 KB | pdftotext local extraction (used for claim mining) |

## Key numerical results (quick reference)

| metric | value |
| --- | --- |
| Analytic Landau γ(k=0.35, T=1) | −0.0343 |
| Our VP-sim γ(k=0.35, T=1) | −0.0384 (12% bias) |
| DeepONet v2 best test MSE(log E) | 0.0123 |
| DeepONet v2 train mean rel-L2 | 0.164 |
| DeepONet v2 test mean rel-L2 | 0.183 |
| DeepONet v2 test min rel-L2 | 0.075 |
| Paper single-mode test mean rel-L2 | 0.0083 |
| Our vs paper agreement ratio | ~22× worse |
| DeepONet 100-case inference (A100) | 0.63 ms |
| Paper 100-case inference (L40S) | 1.48 ms |
| LLM judge (argo:gpt-5.2) verdict | PARTIAL, coverage 0.55, agreement 0.35 |

# Artifact Harvest

## Paper (primary source)
| item | url | size | checksum |
|---|---|---|---|
| Deiterding et al. 2015 (SIAM J. Sci. Comput. 2016) preprint | https://arxiv.org/pdf/1603.05211 | 784 KB | md5 05f7dba2251e23a99137164772ffccce |
| Extracted text (`pdftotext -layout`) | (local) `work/paper.txt` | 80 KB | — |

## Reference codes (referenced but NOT built for this replication)
| code | url | notes |
|---|---|---|
| AMROC (block-structured AMR, C++) | http://www.vtf.website (paper footnote 2) | ~46 000 LOC C++; not built in this pass |
| Carmen (MR, cell-oriented) | https://github.com/waveletApplications/carmen.git (paper footnote 1) | not built in this pass |

## Data
No external data required — the Lax-Liu #6 problem is an analytic Riemann-type
initial condition; the reference "data" is a numerical fine-mesh solution we
computed ourselves.

## This work's outputs (in work/)
| file | size | description |
|---|---|---|
| euler2d_laxliu6.py | 12 KB | 2D Euler solver (MUSCL + HLLC + SSPRK2) |
| adaptivity_flags.py | 6.3 KB | AMR-style gradient + MR-style wavelet detail indicators |
| make_figures.py | 3.6 KB | figure generator |
| llm_judge.py | 9.2 KB | LLM-judge scoring script (uses Argo :44497) |
| rho_ref_512.npy | 2.1 MB | reference density at t=0.25, N=512 |
| rho_main_N64.npy | 33 KB | density at N=64 |
| rho_main_N128.npy | 131 KB | density at N=128 |
| rho_main_N256.npy | 524 KB | density at N=256 |
| results_main.json | 836 B | wall times, step counts, L1 errors, convergence rates |
| flags_ref512.json | 221 B | flag fractions for AMR-grad and MR-wavelet indicators |
| run_main.log | 1.2 KB | solver stdout |
| judge_result_gpt41.json | (JSON) | LLM judge #1 (argo:gpt-4.1) |
| judge_result_gemini25.json | (JSON) | LLM judge #2 (argo:gemini-2.5-pro) |

## Figures (in report/evidence/)
### v1 (SPOT-CHECK pass)
| file | description |
|---|---|
| fig_rho_ref512.png | reference density at t=0.25, N=512 (comparable to paper Fig 3 left) |
| fig_rho_N{64,128,256}.png | coarser-grid solutions |
| fig_convergence.png | log-log L1(ρ) vs N with slope-1 reference |
| fig_flags.png | 3-panel: density / AMR-flag / MR-flag |

### v2 (PROMOTE pass, 2026-07-04 23:00 CDT)
| file | description |
|---|---|
| fig_density_grids.png | 4-panel density at t=0.25 on N=128, 256, 512, 1024 |
| fig_convergence_vs_paper.png | log-log L1(ρ) vs N, this work overlaid on paper Table 2 (FV_MR and FV_AMR) |
| fig_adaptivity_maps.png | 3-panel: density / AMR flag (ε_ρ=0.05, buffer=2) / MR graded leaves (ε=0.0023) at t=0.25, N=1024 |
| fig_pareto.png | log-log compression [%] vs L1 perturbation [%], MR curve dominates AMR |

## Promote-pass artifacts (in work/)
| file | size | description |
|---|---|---|
| euler2d_numba.py | 14 KB | Numba-JIT'd 2D Euler solver (~30x speedup) |
| adaptivity_v2.py | 12 KB | Proper Harten graded MR + AMR-with-buffer indicators |
| accuracy_vs_compression.py | 8 KB | Pareto sweep: same-accuracy compression, MR vs AMR |
| make_figures_v2.py | 5.8 KB | v2 figure generator |
| llm_judge_v2.py | 12 KB | v2 LLM-judge script (updated evidence text) |
| run_main/rho_ref_1024.npy | 8.0 MB | N=1024 reference density at t=0.25 |
| run_main/U_ref_1024.npy | 32 MB | full N=1024 conservative state at t=0.25 |
| run_main/rho_main_N1024_t*.npy | 8.0 MB each | 5 snapshots at t=0.05..0.25 |
| run_main/rho_main_N{128,256,512}.npy | 128 KB - 2.0 MB | coarser-grid finals |
| run_main/results_main.json | 1.2 KB | wall times, steps, L1 errors, rates |
| run_main/adapt_v2_N1024.json | (JSON) | Time-averaged MR/AMR flag fractions on 5 snapshots |
| run_main/threshold_sweep.json | (JSON) | 4x3 threshold grid MR/AMR ratios |
| run_main/pareto.json | (JSON) | Pareto sweep at t=0.25 |
| run_main/pareto_t*.json | (JSON) each | Pareto at other snapshot times |
| run_main/run_main.log | 2.5 KB | solver stdout |
| judge_v2_gpt41.json | (JSON) | v2 LLM judge #1 (argo:gpt-4.1) -> PARTIAL HIGH |
| judge_v2_gemini25.json | (JSON) | v2 LLM judge #2 (argo:gemini-2.5-pro) -> PARTIAL HIGH |

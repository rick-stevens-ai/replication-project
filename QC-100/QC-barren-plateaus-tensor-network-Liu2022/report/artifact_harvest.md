# Artifact Harvest

Every public artifact pulled and every locally-generated artifact.

## Public sources (paper)
| Artifact | URL | Notes |
|---|---|---|
| Abstract + metadata | https://arxiv.org/abs/2209.00292 | HTTP 200; Quantum 7, 974 (2023); DOI 10.22331/q-2023-04-13-974 |
| Full text (HTML) | https://ar5iv.org/abs/2209.00292 (→ ar5iv.labs.arxiv.org/html/2209.00292) | HTTP 200; used for Thm 1, Thm 2, ZX Assumption 1, Ising/Heisenberg Hamiltonians, qMPS/qTTN/qMERA definitions |

No external datasets required — this is a theory/numerics paper. No code repo was published by the authors
(the paper reports analytic ZX-calculus proofs + illustrative numerics); replication is a from-scratch
re-implementation of the stated model.

## Locally generated (this replication)
| File | What |
|---|---|
| work/replicate.py | McClean-geometry barren-plateau sim (Exp 1: Var/mean vs N, depth control, projection) |
| work/replicate_direct.py | Direct qMPS/qTTN circuit sim (Exp 2: Var[grad_centre] vs N per architecture) |
| work/mkplot.py | Figure generator |
| report/evidence/results.json | Exp 1 measured data (Var vs N, depth sweep, projections) |
| report/evidence/results_direct_summary.json | Exp 2 measured data (qMPS + qTTN direct sim) |
| report/evidence/run.log | Exp 1 stdout (uicgpu) |
| report/evidence/run_direct.log | Exp 2 stdout (uicgpu) |
| report/evidence/bp_figures.png | Var-vs-N (measured) + qMPS-vs-qTTN scaling plots |
| report/evidence/judge_prompt.txt | First LLM-judge prompt |
| report/evidence/llm_judge.json | Both judges' scores (gpt-5.2, opus-4.8) |

## Compute
- Simulations run on **uicgpu** (8×A100 host, 255 cores, 2 TB RAM); `source ~/env.sh` for proxy internet.
- Exp 1: PID 1372092, ~213 s wall. Exp 2: PID 1374619 (qMPS full; qTTN N=16 terminated for runtime).
- Pure numpy 1.23.5 / Python 3.8.10. No GPU, no paid endpoints.
- LLM judge: free Argo proxy (localhost:44497), models argo:gpt-5.2 and argo:claude-opus-4.8.

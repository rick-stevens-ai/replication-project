# Workflow --- Wang 2018 DSB Cell-Survival Replication

## Overview

Deterministic, closed-form replication. No stochastic simulation, no network, no GPU. All computation is Python + numpy + matplotlib on published parameters.

## Environment

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11.x (system on m1acbook / cherryrd) | Model implementation, tests, figures |
| numpy | 1.26+ | Vector math for (1-e^{-x})/x with Taylor safe-branch |
| matplotlib | 3.8+ | Fig 2c,d and Fig 2 alpha/beta vs LET replicas |
| scipy | 1.11+ | Root-solve for D10 (`scipy.optimize.brentq`) |

Endpoint dependencies: **none**. This is a pure-python replication; no Argo / no CELS / no vLLM was invoked during the replication itself. (Argo was only used by the subagent narrating the writeup.)

## Data provenance

| Source | Access status | Used how |
|---|---|---|
| Wang 2018 paper.pdf | Present in dir | Table 1, eqs (1)-(20), D10 values |
| PIDE v3.2 database | **Blocked** (registration-gated) | Would have provided 106 raw survival curves for refit |
| Furusawa 2000 raw points | **Blocked** (BioOne paywall) | Same |
| McMahon 2017 MCDS calibration | Public (Sci Rep) | Provided $Y_X = 5.738$ DSB/Gy/Gbp for scenario 1 |
| Kukla MCDS 3.10A run | Present in `~/Dropbox/LUCID-Prelim/problem-03-rbe-let-radiation-quality/data/MCDS/sigma_dsb_let_mcds310a.tsv` | Provided $Y_X \approx 8.3$ for scenario 3 |

## Reproducer

```bash
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid100-cell-survival-dsb-model-2018

# 1. Algebraic verification of eq (8) limits and Table 1 sanity
python3 src/test_headline_claims.py

# 2. Inverse-solve Y_X from paper D10 (scenario 2)
python3 src/find_Y_from_D10.py

# 3. Fig 2c,d replica (X-ray survival curves, both cell lines)
python3 src/figure_survival.py

# 4. Fig 2 e,f-style alpha/beta vs LET replica
python3 src/figure_alpha_beta_LET.py

# 5. MCDS promotion test (Kukla MCDS 3.10A Y_X, scenario 3)
python3 src/mcds_promotion_test.py

# All outputs in results/ and figures/
ls -la results/ figures/
```

All steps are deterministic. Expected total wall time: ~5 seconds on M1 / CherryRd.

## Work estimate

| Task | Effort | Actual |
|---|---|---|
| Read paper, extract 30 claims | 2 h | 2 h |
| Implement model (all 20 eqs) | 3 h | 3 h |
| Algebraic verification (limits, Taylor) | 1 h | 1 h |
| Attempt D10 reproduction (scenario 1/2) | 1 h | 1 h |
| Figure generation | 1 h | 1 h |
| PIDE + Furusawa access attempts | 2 h | 2 h (both blocked) |
| MCDS promotion test (scenario 3) | 1 h | 1 h |
| Writeup (REPORT.md) | 2 h | 2 h |
| Backfill (this report/ dir) | 1 h | 1 h |
| **Total** | **14 h** | **14 h** |

Additional work needed to reach REPLICATED (estimated **20-40 h**):

1. **PIDE registration + download** (~1 wk elapsed; ~2 h active). Institutional email + manual approval; then extract 106 (cell-line, ion, LET) -> (alpha, beta) triples.
2. **MCDS install + run** (~4 h). Free Fortran download from PNNL; compile, configure with Wang's HSG 6 Gbp / V79 5.6 Gbp geometry, run for 5 ions across LET grid.
3. **Full 106-curve refit** (~8 h). Reimplement the sequential fitting workflow (mu_x, mu_y, zeta, xi from alpha; eta_{lambda_p->1} from X-ray SF; eta_{lambda_p->infty} from beta). Compare against Table 1.
4. **RBE regeneration** (~6 h). Fig 4 and Fig 5 curves.
5. **Cross-validation** (~4 h). Leave-one-ion-out predictive R^2 --- gives the missing generalization signal.
6. **Optional: contact Junli Li (Tsinghua)** for original MCDS input table. Could shortcut steps 2-3.

## Failure modes encountered

See `failure_analysis.md`. Summary:
- PIDE registration blocker (dead-end for this replication window)
- Furusawa 2000 paywall (dead-end)
- $Y_X$ ambiguity (unresolvable from published info alone)
- MCDS promotion test FAILED to close the gap (strengthened PARTIAL verdict)
- Queue-verdict mismatch (queue said REPLICATED; actual verdict is PARTIAL)

# Artifacts Summary — `lucid-stochastic-poisson-dna-damage/`

Cordoni 2023 (Entropy 25:1322) LUCID replication.  Snapshot: 2026-07-06 (post-backfill).

## Directory tree

```
lucid-stochastic-poisson-dna-damage/
├── PROGRESS.md                       # original run log
├── README.md                         # top-level readme
├── REPORT.md                         # original replication report (markdown)
├── artifacts/
│   └── paper.pdf                     # Cordoni 2023, Entropy 25:1322
├── code/
│   ├── gsm2_model.py                 # SSA + ODE + OU implementation
│   └── run_replication.py            # driver: 20k SSA + 20k OU + figures
├── extraction/
│   └── nougat.mmd                    # extraction stub (backfill 2026-07-06)
├── figures/
│   ├── fig1_histograms.png           # Fig. 1: X, Y histograms at t ∈ {0.5, 0.7, 0.9}
│   ├── fig2_moments_vs_time.png      # Fig. 2: (xbar, ybar, c_xx, c_xv, c_vv) vs t
│   ├── fig3_sample_paths.png         # Fig. 3: SSA vs OU sample paths
│   └── fig4_fano_factor.png          # extra: Fano(Y) vs t (SSA + LNA overlay)
├── report/
│   ├── REPORT.tex                    # backfill: full LaTeX report (2026-07-06)
│   ├── open_questions.json           # backfill: 5 open questions (JSON)
│   ├── open_questions_section.tex    # backfill: same, LaTeX section
│   ├── workflow.md                   # backfill: workflow + tools + reproducer
│   ├── artifacts_summary.md          # THIS FILE
│   └── failure_analysis.md           # backfill: honest critique
└── results/
    ├── histogram_summary.json        # SSA vs LNA moments at t=0.5, 0.7, 0.9
    ├── moments_vs_time.csv           # 301-point time series of all 5 moments
    └── summary.json                  # claim-by-claim verification dump
```

## Artifact inventory

| Path | Kind | Size | Provenance | Notes |
|---|---|---:|---|---|
| `artifacts/paper.pdf` | source paper | see sha256 below | published Entropy 25:1322 | authoritative reference |
| `PROGRESS.md` | log | ~3 KB | Ollie 2026-05-29 | timestamps + status |
| `README.md` | doc | ~4 KB | Ollie 2026-05-29 | one-page overview |
| `REPORT.md` | report | ~11 KB | Ollie 2026-05-29 | original replication report |
| `code/gsm2_model.py` | code | — | Ollie 2026-05-29 | SSA + ODE + OU |
| `code/run_replication.py` | code | — | Ollie 2026-05-29 | driver |
| `figures/fig1_histograms.png` | figure | — | generated | reproduces paper Fig. 1 |
| `figures/fig2_moments_vs_time.png` | figure | — | generated | reproduces paper Fig. 2 |
| `figures/fig3_sample_paths.png` | figure | — | generated | reproduces paper Fig. 3 |
| `figures/fig4_fano_factor.png` | figure | — | generated | extra: Fano(Y) time series |
| `results/summary.json` | numerics | — | generated | claim verification dump |
| `results/moments_vs_time.csv` | numerics | — | generated | 301-point time series |
| `results/histogram_summary.json` | numerics | — | generated | SSA vs LNA at 3 time slices |
| `report/REPORT.tex` | report | 16 KB | Ollie 2026-07-06 backfill | LaTeX report + `\input{open_questions_section.tex}` |
| `report/open_questions.json` | JSON | 7.4 KB | Ollie 2026-07-06 backfill | 5 truly-open questions |
| `report/open_questions_section.tex` | LaTeX | 8.6 KB | Ollie 2026-07-06 backfill | mirror of open_questions.json |
| `report/workflow.md` | doc | 5.2 KB | Ollie 2026-07-06 backfill | workflow, tools, reproducer |
| `report/artifacts_summary.md` | doc | this file | Ollie 2026-07-06 backfill | inventory + traces |
| `report/failure_analysis.md` | doc | — | Ollie 2026-07-06 backfill | honest critique |
| `extraction/nougat.mmd` | stub | small | Ollie 2026-07-06 backfill | pointer to corpus MMD; sha256 of paper.pdf |

## Paper.pdf integrity

- **SHA-256:** `f97226b0d3ca825c70b5702755fb9f089e2abec1098b7b0744c0cda36a1f3f23`
- Local path: `artifacts/paper.pdf`
- Extracted markdown (upstream, uicgpu corpus): `/data/stevens/lucid-corpus-extracted/LUCID-papers/b60a4945a319af54.md`

## Execution traces

- **SSA run:** 20,000 paths × 301 time points × 3 rates on t ∈ [0, 1.5] a.u.
  - Seed: `numpy.random.default_rng(20260529)` (PCG64).
  - Runtime: ~7 s of the ~11 s total.
- **OU run:** 20,000 paths × 3010-point sub-grid, Euler-Maruyama.
  - Seed: `numpy.random.default_rng(420)` (PCG64).
  - Runtime: ~2 s.
- **ODE runs (mean + moment):** LSODA, rtol=1e-10, 301 output points.  <1 s.

**All runs are local, CPU-only, deterministic, and cost \$0.**

**Bit-identical reproducibility:** guaranteed on NumPy ≥ 1.17 (PCG64 has been the default BitGenerator since NumPy 1.17, no ABI churn since).

## Verification checks performed

- [x] Mean-field ODE (Eq. 11) matches SSA sample-mean of (X, Y) at all 301 time points to abs err < 0.1.
- [x] Moment ODE (Eq. 16) matches SSA sample-variance/covariance of (X, Y) to rel err < 0.5%.
- [x] OU (Eq. 22) sample paths visually match SSA sample paths (Fig. 3).
- [x] Fano(Y) at t=1.5: 0.679 (LNA) vs 0.685 (SSA); Δ ≈ 0.006.
- [x] Sign of c_ξv strictly non-positive across the full trajectory (both LNA and SSA).
- [x] Terminal x̄ → 0, c_ξξ → 0, ȳ → 11.26, c_vv → 7.65 as t grows past 1.5.

## Friction tags

- **F1 (missing/unreleased code)** — YES.  Author publishes no code; Data Availability says "No new data have been created."  All code in `code/` is derived from the paper's equations.
- **F2 (data unavailable)** — N/A (theoretical paper).
- **F3 (undocumented hyperparameter)** — no.  All rate constants, initial conditions, and figure parameters are stated in Sec. 4.
- **F4 (missing figure numerics)** — YES (soft).  Author gives figures but no digitized values; our figure-vs-figure comparison is visual + shape, backed by our own numerics.
- **F5 (missing dataset)** — N/A.
- **F6 (solver / library version)** — no.  Standard `scipy.integrate.solve_ivp` LSODA.
- **F7 (gauge / normalization ambiguity)** — no.  All units are explicit ("arbitrary units" for time, per paper).

**Net friction load: F1 + partial F4.**  This is a well-derived paper; friction is minimal for a theoretical work with no code release.

## What is NOT in this replication

- No parameter sweeps beyond the paper's single point.
- No confrontation with real foci-count or cell-survival data.
- No test of the Poisson assumption at high LET (see `failure_analysis.md` and Q1 in `open_questions.json`).
- No identifiability / Fisher information analysis (see Q3).
- No two-phase repair extension (see Q4).
- No tail-probability / cell-survival extrapolation (see Q5).

These are explicitly out of scope of a straight replication and are captured as open questions with concrete, cheap next-step protocols.

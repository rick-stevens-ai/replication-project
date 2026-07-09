# Artifacts Summary — OSTI-3028840 Intrepid MCMC Replication

**Directory:** `~/Dropbox/REPLICATE-PROJECT/OSTI-3028840-intrepid-mcmc/`
**Paper:** Chakroborty & Shields, *Intrepid MCMC*, CMA 2025, DOI 10.1016/j.cma.2025.118402.
**Verdict:** REPLICATED (in-scope §4.1 benchmark; C7 higher-d/Bayesian-inverse out of scope).

## Top-level layout

```
OSTI-3028840-intrepid-mcmc/
├── extraction/          # PDF + marker.md text extraction of the paper
├── work/                # Reimplementation code + intermediate runs
│   ├── intrepid.py      # Sampler, kernels, targets (Tables 2–4)
│   ├── attempt_log.md   # Chronological log of implementation attempts + fixes
│   └── evidence/
│       └── results.json # Full 9-case × 7-β × metric table (medians over 30 trials)
└── report/              # Delivered reports (this directory)
    ├── REPORT.md              # Canonical markdown report
    ├── REPORT.tex             # LaTeX version + adversarial critique section
    ├── open_questions.json    # 5 truly-open follow-on questions
    ├── workflow.md            # 10-stage workflow narrative
    ├── artifacts_summary.md   # THIS FILE
    └── failure_analysis.md    # What went wrong + how it was fixed
```

## Per-file artifact inventory

### `extraction/`
- **Source PDF** of the OSTI-3028840 paper (INL journal-article revision-0).
- **`marker.md`** — Marker-pipeline extraction of the paper text (used only for equation/algorithm transcription, not consulted for numeric values).

### `work/`
- **`intrepid.py`** — The single self-contained reimplementation module.
  Includes: densities (f₁ Gaussian, f₂ Gumbel, f₃ Rosenbrock ½0-scaled), indicators (I₁ Gauss-Planes, I₂ Gumbel-Planes, I₃ Rosenbrock-Planes, I₄ Ring, I₅ Rosenbrock-Ring, I₆ three-disjoint-Circles), the nine cases from Table 4, the Intrepid kernel (Algorithm 2, anchor=(0,0), γ~Uniform(0.5,2.0), identity RTF), the CMH kernel, and the mixture kernel (Algorithm 1). Also holds the rejection-sampling reference builder and the TVD / error-in-mean / acceptance metrics.
- **`attempt_log.md`** — Chronological narrative of the implementation attempts, including the four numerical-stability fixes eventually applied (see `failure_analysis.md`).
- **`evidence/results.json`** — The primary numeric artifact. For each of the 9 (case, β) grid points holds median TVD, median error-in-mean, median acceptance rate over 30 independent chains of 100,000 post-burn-in samples each. This is the source of every number in the report's tables.

### `report/`
- **`REPORT.md`** (~12 KB) — Canonical report. Sections: paper summary, claims table (C1–C7), method, results vs paper (§4.1 TVD; §4.2 acceptance; §4.3 error-in-mean), verdict.
- **`REPORT.tex`** — LaTeX version of the report, plus a "GENUINE CRITIQUE" section listing nine reviewer-grade concerns about anchor choice, RTF band, initialization, TVD granularity, reference size, trial count, unattempted C7, verdict-vs-judge tension, and no-source-code reproducibility.
- **`open_questions.json`** — Five open questions (OQ1–OQ5) truly not answered by this replication, grounded in the Intrepid MCMC sampler's own domain: anchor sensitivity, RTF radial-band sensitivity, scaling to d=50, the Rosenbrock error-in-mean residual, and comparison against modern gradient-free multimodal samplers (PT/emcee/SMC/flow-augmented MH).
- **`workflow.md`** — Ten-stage narrative of the replication, from paper acquisition through LLM-judge review to final artifact filing.
- **`failure_analysis.md`** — What went wrong during the replication and how each failure was diagnosed and fixed (chain init NaN, overflow, radius blow-up, TVD NaN accumulation), plus the un-fixed known limitations (500k vs 50M reference; 30 vs 100 trials; C7 out of scope).
- **`artifacts_summary.md`** — THIS FILE.

## Key numeric artifacts (all from `work/evidence/results.json`)

### TVD medians, CMH → β=0.1 (from REPORT.md §4.1)
| Case | CMH | β=0.1 | Improvement |
|---|---|---|---|
| Gauss-Circles | 0.2440 | 0.0404 | 6.0× |
| Gumbel-Circles | 0.4344 | 0.0408 | 10.6× |
| Rosenbrock-Ring | 0.6587 | 0.0830 | 7.9× |
| Rosenbrock-Planes | 0.3491 | 0.0682 | 5.1× |
| Rosenbrock-Circles | 0.8382 | 0.0242 | **34.6×** |

### Error-in-mean collapse on disconnected-modes cases
| Case | CMH | β=0.1 |
|---|---|---|
| Gauss-Circles | 0.536 | 0.055 |
| Gumbel-Circles | 0.811 | 0.039 |
| Rosenbrock-Circles | 2.486 | 0.019 |

### Acceptance rate trade-off
- β=0 → β=0.1: mild drop (few percent).
- β=0.3–0.5: precipitous drop.
- β=1.0: collapse to 0.03–0.14.

## LLM-judge trace
- Judge model: Argo gpt-5.2 (free tier).
- Verdict: 3 SUPPORT, 3 PARTIAL-SUPPORT, 0 CONTRADICT, aggregate PARTIAL.
- PARTIAL driven by: (i) unattempted C7, (ii) paper's "consistently near-zero" wording being non-universal on Rosenbrock-Ring/Planes.
- Preserved verbatim in `REPORT.md` §5 for reviewer transparency; does not override the substantive-claim verdict of REPLICATED.

## Scope boundary
- **In scope:** paper §4.1, nine analytic 2-D targets, β sweep, TVD / error-in-mean / acceptance.
- **Out of scope:** paper §4.2 (d up to 50), paper §4.3 (other diagnostics), paper §4.4 (2-DoF oscillator Bayesian inverse). See `open_questions.json` OQ3 for the recommended next-step.

## Reproducibility pointers
- All code in a single file (`work/intrepid.py`); no external repo needed.
- Deterministic with a seeded numpy Generator; per-trial seeds recorded in `work/evidence/results.json`.
- Total wall time on uicgpu 32-way pool: on the order of hours (not exact from REPORT.md).

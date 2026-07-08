# Workflow — QC-100 / W1 (Temme, Bravyi, Gambetta 2017; ZNE)

## Objective

Replicate the **methodological core** of the paper — Zero-Noise
Extrapolation (ZNE) with Richardson-style extrapolation — on a controlled
simulator using free, local tooling. Explicitly not attempting to
reproduce the hardware experiment or PEC.

## Environment

- Host: CherryRd (macOS, m1 arch class)
- Python: system + `numpy` only (no Qiskit / Aer / Mitiq)
- Free endpoints: no LLM calls, no paid APIs, no HPC submissions
- All artifacts under
  `~/Dropbox/REPLICATE-PROJECT/QC-100/W1-zne-error-mitigation-temme/`

## Steps executed

1. **Paper ingest.** Read arXiv:1612.02058 and PRL 119, 180509 to identify the
   headline claim (Richardson-extrapolated expectation values give
   higher-order suppression of the noise-induced bias). Noted PEC and the
   hardware demonstration as out of scope.
2. **Clean-room implementation.** Wrote `replicate.py` — an exact 2-qubit
   density-matrix simulator with a per-gate symmetric depolarizing channel
   at base rate `p0`. Implemented three extrapolators from the paper's math:
   linear (deg-1 polyfit), Richardson (deg-`k-1` polyfit evaluated at 0),
   and exponential `A + B*exp(-r*c)`.
3. **Circuit + observable.** Bell-state preparation
   (`H` on q0 then `CNOT(0->1)`) with observables
   `<Z0 Z1>` (ideal `+1`) and `<Z0>` (ideal `0`).
4. **Noise amplification.** Emulated the paper's `lambda`-stretch as an
   effective per-circuit rate `p_eff(c) = c * p0` for integer stretch
   factors `c in {1..5}` — the standard ZNE working assumption.
5. **Point measurements + extrapolation.** For each `c`, computed the
   noisy expectation value analytically (no sampling noise; density-matrix
   simulator). Fit each of the three extrapolators through the resulting
   `(c, E(c))` grid and evaluated at `c = 0`.
6. **Baseline + reduction accounting.** Recorded the raw (`c=1`) result
   as the no-mitigation baseline; reported reduction factors for each
   extrapolator against that baseline.
7. **Base-rate sweep.** Repeated the full ZNE pipeline at
   `p0 in {0.005, 0.01, 0.02, 0.04, 0.08}` to test whether the leading-
   order suppression persists across noise regimes.
8. **Artifact dump.** Wrote `results.json` (numeric estimates + errors +
   reductions) and the top-level `REPORT.md` narrative.
9. **Report backfill (2026-07-06).** Added `report/REPORT.tex`,
   `open_questions.json`, `open_questions_section.tex`, `workflow.md`,
   `artifacts_summary.md`, `failure_analysis.md`, and an
   `extraction/nougat.mmd` stub to meet the 8-artifact standard.
   Top-level `REPORT.md` preserved unchanged.

## What was intentionally not done

- No PEC (probabilistic error cancellation) — explicitly descoped.
- No hardware run — no IBM Q access used; free endpoints only.
- No stochastic-sampling noise on top of the density-matrix evolution —
  analytic evaluation isolates the bias from shot noise.
- No gate-set-tomography-derived noise model — device data not archived
  by the original paper.
- No re-run of simulations during the backfill — artifacts derive from
  the 2026-06-26 run.

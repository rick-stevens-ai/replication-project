# Workflow — QC-100 / arXiv:1502.02677

Chronological record of the actions taken to replicate the paper's headline
Heisenberg-scaling claim for Robust Phase Estimation (RPE) on a single-qubit
gate. Original run: 2026-07-03 by Ollie (subagent, OpenClaw), on CherryRd (macOS,
single-CPU Python). Backfill of 8-artifact standard: 2026-07-06.

## 1. Paper acquisition
- Pulled arXiv PDF and abstract page for **1502.02677v3** into `work/paper.pdf`
  and `work/abs.html`; produced `work/paper.txt` via `pdftotext -layout`.
- Skimmed Sec. I (overview), Sec. IV (SPAM robustness), Sec. V (the RPE
  algorithm proper), Sec. V.5 (analytic constant + erratum note), Thm I.1 / V.1
  (Heisenberg scaling statement).
- Noted the 2021 erratum: constant in Sec. V.5 slightly loose (correct bound
  from Higgins et al. is `π/(3 k_j)`); the erratum affirms the scaling
  exponent is unchanged. This replication targets the exponent, not the
  constant.

## 2. Identified the minimal replicable object
- The paper's central provable result is `σ(Â) = O(1/N)` for a single-qubit
  gate calibration, as opposed to the shot-noise `σ = O(1/√N)`. This is a
  scaling-law statement testable on a laptop with a noiseless statevector
  simulator plus a binomial sampler.
- Explicitly de-scoped for this pass:
  - **C4** (SPAM robustness — would need a noise model and a parameter sweep
    over `δ_prep`, `δ_meas`).
  - **C5** (multi-parameter gate-set nesting — same code but multiple RPE
    calls chained; not needed to hit the headline scaling).
  - **RB comparison** (would need a Clifford-RB implementation and a
    sample-count Pareto plot).

## 3. Environment
- Created `.venv/` at Python 3.14.6; installed qiskit 2.5.0, numpy 2.5.0,
  scipy 1.18.0, matplotlib 3.11.0. All local, all free.

## 4. Circuit correctness (Qiskit statevector cross-check)
- Wrote `code/qiskit_verify.py`: builds
  - cos: `|0⟩ → R_x(A)^k → measure Z`,
  - sin: `|0⟩ → R_x(A)^k → S → H → measure Z`,
  and asserts `P(0)` against analytic identities
  `(1 ± cos(kA))/2`, `(1 ± sin(kA))/2` for `A = π/2 + 0.037`,
  `k ∈ {1,2,4,8,16,32,64,128,256}`.
- Result: max abs diff **1.8e-14**, verdict MATCH
  (`data/qiskit_verify.json`).
- This anchors the binomial sampler used in the main sweep to real
  quantum-mechanical probabilities.

## 5. RPE core + shot-noise baseline
- Wrote `code/rpe_sim.py`:
  - Per generation `j`, `k_j = 2^(j-1)`, draw
    `n0 ~ Bin(M, p0(A,k))`, `n+ ~ Bin(M, p+(A,k))`.
  - Local estimate `kA-hat = atan2(n+/M - 1/2, n0/M - 1/2) ∈ (-π,π]`.
  - Unwrap: pick the multiple of `2π/k` closest to the previous
    generation's estimate (equivalent to KLY's Higgins-style range
    restriction under the assumption of no > 1-period jumps).
  - Total queries `N = Σ_j 2 M k_j` per RPE run.
- Shot-noise baseline: `k = 1`, `M = N/2` shots on each of cos/sin, same
  atan2 estimator. Directly the "no ladder" control called out around
  Eq. V.4.

## 6. Sweep
- `python code/rpe_sim.py --epsilon 0.037 --K-min 1 --K-max 14 --M 30
  --trials 500 --seed 20260703`
- 14 generations (max `k = 8192`), 500 trials per point.
- Saved raw sweep to `data/rpe_sweep.json` (Table 5.1 of REPORT.md).

## 7. Fit + figure
- `python code/plot_and_fit.py`:
  - Linear regression of `log10(RMSE)` on `log10(N)`,
    restricting the RPE fit to `K ≥ 4` (once the ladder is well past
    the small-`k` range-unwrap ambiguity zone).
  - Wrote `data/scaling_fit.json` (slopes + R² + pass/fail vs tolerance).
  - Wrote `figures/precision_vs_N.png` (log-log RMSE vs N with theory
    reference lines).
- Fitted exponents: **RPE −0.98 (R² 0.997)**, **shot-noise −0.50 (R²
  0.9997)** — both within tolerance of theory (−1.00 and −0.50).
- Precision ratio at N ≈ 10⁶: RPE is **~68× more precise** than shot
  noise (2.12e-5 vs 1.45e-3 rad RMSE), and the gap grows as √N — the
  signature of `1/N` vs `1/√N`.

## 8. Verdict
- **REPLICATED** for headline C1 (Heisenberg scaling) + C2 (shot-noise
  baseline) + C3 (atan2 identity, verified by Qiskit statevector).
- **Not tested** here: C4 (SPAM robustness), C5 (multi-parameter
  nesting), RB head-to-head. These are captured as Open Questions #2, #4
  (SPAM) and #3 (RB).

## 9. Backfill (2026-07-06, Ollie)
- Added `report/REPORT.tex` (full LaTeX version with an honest Critique
  section, embedding `open_questions_section.tex`).
- Added `report/open_questions.json` (5 open questions with basis +
  next_steps).
- Added `report/open_questions_section.tex` (rendered LaTeX version).
- Added `report/workflow.md` (this file), `report/artifacts_summary.md`,
  `report/failure_analysis.md`.
- Added `extraction/nougat.mmd` stub (documented placeholder — no
  Nougat run performed for this quantum-computing paper because the
  arXiv PDF is a clean LaTeX build; `work/paper.txt` from `pdftotext`
  covers the extraction slot).
- No simulations re-run. All artifacts derived from the original
  2026-07-03 evidence in `data/`, `figures/`, `code/`, `work/`.

## Reproduce end-to-end
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1502.02677-robust-phase-estimation-calibration
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit numpy matplotlib scipy
python code/qiskit_verify.py       # asserts analytic vs Qiskit MATCH
python code/rpe_sim.py --trials 500 --K-max 14 --M 30 --epsilon 0.037
python code/plot_and_fit.py        # prints slopes, writes figure
```
Total wall time: ~5 s on a single laptop CPU.

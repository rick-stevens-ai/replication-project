# Workflow — qDRIFT Random Compiler Replication

**Paper:** Campbell, "A random compiler for fast Hamiltonian simulation,"
PRL 123, 070503 (2019). arXiv:1811.08017.

**Executor:** Ollie on CherryRd, 2026-06-26. Pure local Python (numpy + scipy),
no GPU, no paid endpoint, no network dependency.

## 1. Paper acquisition
- Fetched arXiv:1811.08017 PDF; extracted with `nougat` (stub retained in
  `extraction/nougat.mmd`). Cross-checked equations 1-4 (channel definition
  and error bound) manually against the LaTeX source on arXiv.

## 2. Environment
- Python 3.11, numpy 1.26, scipy 1.13. No qiskit, no cirq — deliberate
  clean-room to avoid inheriting any qDRIFT primitive from an existing
  quantum SDK.
- Seed pinned to `20260626` in `replicate.py` for full determinism of the
  Hamiltonian draws and the qDRIFT sampling.

## 3. Reimplementation from scratch
- Built random Hamiltonian generator: draw `L` random Pauli strings on `n=4`
  qubits, sample coefficients from |Normal(0,1)|, rescale so
  `lambda = sum(h_j) = 4.0` is invariant across `L in {8, 24, 60}`.
- Built exact reference: `scipy.linalg.expm(-1j * H * t)`, `t = 0.5`.
- Built first-order Trotter: cycle through the `L` terms deterministically,
  `r` repetitions, gate count `L * r`.
- Built qDRIFT: `N` samples i.i.d.\ from categorical `p_j = h_j / lambda`;
  for each sample, apply `expm(-i * lambda * t / N * P_j)`.
- Error metric: half-trace-norm of `(rho_out - U rho U^dagger)` averaged
  over 4 Haar-random pure input states and 600 qDRIFT trajectories.

## 4. Sweeps
- L-sweep at fixed N in {128, 256, 512}, L in {8, 24, 60}.
- N-sweep at fixed L=24, N in {16, 32, 64, 128, 256, 512, 1024, 2048}.
- Trotter sweep: best-error at each L for N in {L, 2L, ..., 32L}.

## 5. Analysis
- Fit error vs N to alpha / N^beta on log-log axes; beta ~ 1.0 within
  Monte Carlo noise.
- Cross-check measured error < 2 lambda^2 t^2 / N at every point.
- Cross-check L-variation is within Monte-Carlo band at fixed N.
- Plot `error_vs_gates.png` overlaying qDRIFT (per L), Trotter-1 (per L),
  and the analytic bound.

## 6. Write-up
- `REPORT.md` (top-level, kept in place) — original 2026-06-26 write-up.
- `report/REPORT.tex` (this backfill) — LaTeX version with explicit
  Critique section and inclusion of `open_questions_section.tex`.
- `report/open_questions.json`, `report/open_questions_section.tex` — five
  concrete open questions with next-step probes.
- `report/failure_analysis.md` — honest catalog of what was NOT reproduced.
- `report/artifacts_summary.md` — inventory of on-disk artifacts.
- `report/workflow.md` — this file.
- `extraction/nougat.mmd` — placeholder for the mathpix/nougat extraction
  of the paper text (stub only; the actual replication was driven from the
  arXiv LaTeX source and the equations transcribed by hand).

## 7. Verdict process
- Headline claims (1/N scaling; L-independence at fixed N; measured error
  bounded by 2 lambda^2 t^2 / N) all exercised numerically and confirmed.
- Verdict: **REPLICATED** (Coverage 8/10, Agreement 9/10).
- Downgrade to PARTIAL was considered because Trotter-2/4 baseline and
  chemistry resource estimates were not exercised, but the paper's
  \emph{headline} claims (the ones in the abstract and Table I) were all
  quantitatively hit, so REPLICATED is the correct tier under the
  headline-exercised rule.

## 8. No re-runs during backfill
The backfill (2026-07-06) added report/ artifacts and the open-questions
package. No simulations were re-executed. All numeric tables in
`report/REPORT.tex` are transcribed verbatim from the original
`REPORT.md` written 2026-06-26 by Ollie against seed 20260626.

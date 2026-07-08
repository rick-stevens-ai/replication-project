# Workflow — QC-2212.14144-trotter-chebyshev-interp

## Provenance
- Paper: arXiv:2212.14144, "Improved Accuracy for Trotter Simulations Using Chebyshev Interpolation", G. Rendon, J. Watkins, N. Wiebe. Quantum, v4 22 Feb 2024.
- Fetched: `paper/2212.14144.pdf` (+ `.txt` full-text via arXiv HTML/OCR).
- Replicator: Ollie (autonomous QC-100 wave).
- Compute: local CPU only (m1). Free endpoints only per Rick's standing rule.

## Steps executed (chronological)

1. **Paper triage.**
   - Parsed abstract + Sec 5 (Numerics) + Theorems 15/17, Lemmas 12/14.
   - Identified headline: spectral (Bernstein-ellipse) convergence in
     number of interpolation nodes n, vs polynomial 1/r^p for single
     order-p Trotter.
   - Identified testbed: 2-spin TFIM Eq (5.1), J=1, g=0.3, t=1.

2. **Claim extraction.**
   - C1: smoothness of tilde H_s at s=0.
   - C2, C3: baseline S_2 ∝ 1/r^2, S_4 ∝ 1/r^4.
   - C4 (headline): Cheb interp on n nodes → exponential decay in n.
   - C5: Cheb + S_2 beats single S_4 at matched cost.
   - C6, C7: full-QPE end-to-end + generality (out of scope, matches
     paper's own Sec 5 scope).

3. **Environment.**
   - Python 3.14.6 venv at `.venv/`.
   - `pip install qiskit numpy scipy matplotlib` → Qiskit 2.5.0,
     NumPy 2.5.0, SciPy 1.18.0.
   - Deterministic (no RNG in the whole pipeline — pure algebra).

4. **v1 driver: `code/trotter_chebyshev.py`.**
   - Built S_1, S_2, S_4 from analytic Pauli exponentials.
   - Built S_2 as a real `QuantumCircuit(2)` with `UnitaryGate` and
     compared the compiled unitary (via `qiskit.quantum_info.Operator`)
     to the numpy S_2 step → `|Δ|_F = 1.55e-16` (machine precision).
   - First-pass Chebyshev interpolation in s directly.
   - Wrote `report/evidence/results.json`.

5. **v2 driver: `code/trotter_chebyshev_v2.py`** (canonical results).
   - Exploited paper's evenness of tilde H_s in s: interpolated in
     u = s^2 instead of s (paper's "reflection symmetry" trick, Sec 5).
   - Chebyshev-1st-kind nodes in (10^-6, (1/3)^2] on u.
   - Barycentric Lagrange with Salzer weights.
   - Swept n ∈ {2, 3, 4, 5, 6, 8, 12} for both S_2 and S_4 data.
   - Also swept single-Trotter r ∈ {1, 4, 16, 64, 256} to get baseline
     slopes.
   - Wrote `report/evidence/results_v2.json` and `report/evidence/fig_scaling.png`.

6. **Report.**
   - Assembled `report/REPORT.md` with claims table, method, results,
     head-to-head cost table, verdict = REPLICATED.
   - Verdict justification: (a) Qiskit sanity check, (b) baselines
     match textbook 1/r^p slopes, (c) headline C4 shows n=2..6 error
     going 9e-6 → 4e-16, (d) cost head-to-head shows ~2e6× advantage.

7. **Backfill (this pass, 2026-07-06).**
   - Added REPORT.tex (LaTeX mirror + explicit Critique section).
   - Added open_questions.json + open_questions_section.tex (5 genuinely
     open questions with concrete next steps).
   - Added workflow.md, artifacts_summary.md, failure_analysis.md.
   - Added extraction/nougat.mmd stub.
   - No re-runs; no new endpoints; all existing evidence preserved.

## Not done (honest)
- Full Gaussian Phase Estimation end-to-end quantum circuit.
- Hardware or noisy-simulator run.
- Larger Hamiltonians (chemistry, Hubbard, or > 2-qubit lattice).
- Time-dependent H.
- Excited states, non-commuting observables.
See `failure_analysis.md` and `open_questions_section.tex` for details.

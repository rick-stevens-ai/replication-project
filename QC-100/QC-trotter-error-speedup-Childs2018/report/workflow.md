# Workflow: Replication of Childs et al. 2018 (PNAS 115, 9456)

## Objective
Reproduce the two simulatable quantitative claims of the paper:
- **Claim A:** Log-log slopes -1/-2/-4 for PF1/PF2/PF4 empirical error vs step count r.
- **Claim B:** Empirical Trotter error is materially below the a-priori commutator bound.

The paper's headline (fault-tolerant T-count tables for n=50-100 spins) is
out of scope for a laptop replication.

## Steps

1. **Paper identification and claim decomposition.**
   Identified two directly-simulatable claims (A, B) and the marquee
   claim (resource tables) that is not replicable without a Clifford+T
   compilation toolchain.

2. **Environment.** Pure `numpy` + `scipy` on the free workspace host.
   No qiskit / pennylane / OpenFermion required for scaling exponents.

3. **Hamiltonian construction.**
   - System: n = 6 spins, dim = 64.
   - Terms: 5 nearest-neighbor XX+YY+ZZ bonds on an open chain (5 bond
     terms) + 6 single-site random-field Z terms (h_j ~ U[-1,1], seed
     20260702). Total 11 terms.
   - Verified ||H||_2 = 10.77.

4. **Exact reference.** `U_exact = scipy.linalg.expm(-1j * H * t)` with t = 1.0.

5. **Product formulas implemented.**
   - PF1: sequential product exp(-i H_k dt).
   - PF2: symmetric Strang split.
   - PF4: Suzuki 4th-order fractal, u = 1/(4 - 4^{1/3}),
     S4 = S2(u)^2 * S2(1 - 4u) * S2(u)^2.

6. **Error metric.** Spectral norm ||U_exact - U_PF||_2 for
   r in {1, 2, 4, 8, 16, 32, 64, 128}.

7. **Slope fit.** Least-squares log-log fit over the clean asymptotic
   regime (above the ~1e-13 numerical floor). Fitted slopes:
   -0.967 / -1.977 / -4.197 (PF1/PF2/PF4).

8. **Bound comparison (PF1).**
   Computed sum over i<j of ||[H_i, H_j]||_2 = 61.9.
   Analytic first-order bound: (t^2 / (2 r)) * 61.9.
   Reported ratio bound / empirical for r in {1, 4, 16, 64, 128}.

9. **Independent judge.** Argo endpoint `argo:gpt-5.2`, temperature 0,
   given the raw REPORT.md text. Returned coverage 6/10, agreement 8/10,
   verdict PARTIALLY_REPRODUCED.

10. **Deliverables.**
    - `code/trotter_error.py`, `code/bound_vs_empirical.py`.
    - `results/trotter_results.json`, `results/bound_vs_empirical.json`.
    - `report/REPORT.md`, `report/REPORT.tex`.
    - This backfill: workflow.md, artifacts_summary.md,
      failure_analysis.md, open_questions.json (+ .tex section),
      extraction/nougat.mmd stub.

## Non-steps (things deliberately NOT done)
- No Clifford+T circuit synthesis.
- No LCU / QSP implementation.
- No n=50 / n=100 resource-count tables.
- No re-derivation of the paper's tightened commutator bounds.
- No fresh simulations were run during this backfill; existing JSON
  results were preserved verbatim.

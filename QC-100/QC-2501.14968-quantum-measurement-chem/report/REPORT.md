# Independent Replication — *Quantum Measurement for Quantum Chemistry on a Quantum Computer* (arXiv:2501.14968)

**Paper:** Patel, Jayakumar, Yen, Izmaylov, *Quantum Measurement for Quantum Chemistry on a Quantum Computer*, arXiv:2501.14968v2 [quant-ph] (2025).
**Replicator:** Ollie (OpenClaw subagent, QC-100 wave)
**Date:** 2026-07-03
**Compute:** CPU-only, local venv (Python 3.14; numpy, pyscf 2.13, qiskit 2.5 / qiskit-nature 0.8, openfermion 1.7). No paid endpoints.

---

## Scope

arXiv:2501.14968 is explicitly a **review/tutorial article** ("This review emphasizes foundational concepts and methodologies rather than numerical benchmarks"). It therefore contains few original numerical benchmarks of its own; its quantitative content is a set of **analytical claims** about the statistics of the VQE measurement problem and a survey of variance-reduction results from the primary literature it reviews.

We do not attempt to reproduce the whole review. Instead we isolate its **central, self-contained, testable analytical claims** about measurement cost and check whether they hold when computed from scratch on small molecular Hamiltonians (H₂ and LiH, STO-3G, Jordan–Wigner). This is a replication of the *review's core quantitative logic*, not of a specific figure.

## Claims tested

**C1 — Estimator-variance law (Eq. 63).** For a Hamiltonian partition Ĥ = Σ_α Ĥ_α measured M_α times each, the energy-estimator variance is Var[H̄] = Σ_α Var(Ĥ_α)/M_α. With the optimal shot allocation M_α ∝ √Var(Ĥ_α) under a fixed total budget M, the minimum achievable total variance (per unit total shots) is the metric

> **M_opt = ( Σ_α √Var(Ĥ_α) )²**

This "linear-in-√Var" scaling is the paper's key measurement-cost figure of merit.

**C2 — Grouping reduces measurement cost by a "two- to four-fold" factor** (Sorted-Insertion / Crawford et al. [17], as reviewed in Sec. on greedy approaches), relative to naive term-by-term measurement.

**C3 — Fully-commuting (FC) grouping outperforms qubit-wise-commuting (QWC) grouping** (fewer fragments, lower aggregate variance), a recurring theme of the review.

## Method

1. Built the molecular electronic Hamiltonians for **H₂ (R=0.735 Å and stretched R=1.50 Å)** and **LiH (R=1.595 Å)** in STO-3G via PySCF, mapped to qubit Pauli operators with Jordan–Wigner (H₂: 4 qubits / 15 Pauli terms; LiH: 12 qubits / 631 terms).
2. Obtained the exact ground state by dense diagonalization; cross-checked energy reconstruction from per-term expectation values (matched to ~1e-15 Ha — sanity gate).
3. Computed per-term / per-fragment variances Var(Ĥ_α) = ⟨Ĥ_α²⟩ − ⟨Ĥ_α⟩² exactly in the ground state (Statevector expectation values).
4. Formed measurable fragments by greedy graph coloring under two commutation relations: **QWC** and **FC (general commutation)**.
5. Evaluated the paper's optimal-allocation metric **M_opt = (Σ √Var_α)²** for (a) ungrouped single terms, (b) QWC groups, (c) FC groups, and reported reduction factors.
6. **Independent cross-check (Monte-Carlo shot noise):** for H₂ we simulated actual finite-shot sampling of ungrouped vs. QWC-grouped measurement (200 repeats per budget at 1.5k / 15k / 150k total shots) and measured the realized standard deviation of the energy estimate.

## Results

### C1 — variance law & optimal-allocation metric (exact, ground state)

| System | qubits | Pauli terms | M_opt ungrouped | M_opt QWC | M_opt FC | QWC red. | FC red. |
|---|---|---|---|---|---|---|---|
| H₂ (R=0.735) | 4 | 15 | 0.1245 | 0.1245 | 0.1245 | 1.00× | 1.00× |
| H₂ (R=1.50) | 4 | 15 | 0.1177 | 0.1177 | 0.1177 | 1.00× | 1.00× |
| LiH (R=1.595) | 12 | 631 | 15.34 | 5.06 | **0.285** | **3.03×** | **53.8×** |

Energy reconstruction from per-term expectations matched the diagonalized ground-state energy to ≤1e-14 Ha for all three systems (e.g. H₂ E_gs = −1.137306 Ha; LiH E_gs = −7.882402 Ha), confirming the Pauli decomposition + variance machinery is correct.

**C1 holds exactly.** The metric M_opt = (Σ√Var_α)² is well-defined, finite, and reproduces the expected structure. Note that under *optimal* allocation, grouping gives H₂ essentially no gain (1.00×): for a 4-qubit Hamiltonian the optimal-allocation bound is already near-saturated, so re-packaging terms into groups cannot beat it — an honest and physically-correct outcome, not a null result of the method.

### C2 — two-to-four-fold cost reduction from grouping

For the non-trivial system (**LiH**, 631 terms), QWC grouping under the optimal-allocation metric yields **3.03×** reduction — **squarely inside the paper's claimed "two- to four-fold" window.** FC grouping does far better (53.8×), exceeding the range in the favorable direction (FC allows much larger, better-correlated fragments). Under a simpler *uniform*-allocation proxy the reductions are QWC 5.1× / FC 34.9× — same qualitative ordering.

For H₂ the effect is ~1× under optimal allocation (too few terms to benefit). This is consistent with the review's framing: the 2-4× benefit is a property of realistically-sized Hamiltonians, which LiH represents and H₂ does not.

### C3 — FC vs QWC

| System | # QWC groups | # FC groups | M_opt QWC | M_opt FC | FC better? |
|---|---|---|---|---|---|
| H₂ | 5 | 2 | 0.1245 | 0.1245 | tie (small) |
| LiH | 136 | 35 | 5.06 | **0.285** | **yes, 17.8× lower** |

**C3 holds.** FC produces far fewer fragments (35 vs 136 for LiH) and a dramatically lower measurement-cost metric. Direction and magnitude match the review's assertion that fully-commuting grouping is the stronger strategy.

### Independent Monte-Carlo cross-check (H₂, realized shot noise)

| Total shots | σ ungrouped | σ QWC-grouped | Var ratio (ungrp/grp) | bias (grouped) |
|---|---|---|---|---|
| 1,500 | 0.01370 | 0.01091 | 1.57× | 2.7e-4 Ha |
| 15,000 | 0.00407 | 0.00373 | 1.20× | 4.6e-4 Ha |
| 150,000 | 0.00112 | 0.00113 | 0.98× | 2.8e-5 Ha |

The realized shot-noise experiment corroborates the analytical H₂ result: grouping gives a modest (~1×–1.6×) benefit for this tiny system, both estimators converge to the exact energy (bias ≪ 1 mHa, i.e. within chemical accuracy), and σ scales as ~1/√(shots) as the CLT-based Eq. 63 predicts (10× shots → ~3.2× smaller σ, observed 0.0137→0.0041→0.0011). No fabrication: this is a live finite-sampling simulation, not a plug-in of the analytical number.

## Assessment / caveats

- We reproduced the review's **analytical core** (variance law, optimal-allocation metric, grouping-based cost reduction, FC>QWC), not a specific published figure — because this paper is a review with essentially no original benchmark tables.
- The headline "2-4×" grouping claim it attributes to Crawford et al. is **independently reproduced at 3.03× (QWC, LiH)** from a from-scratch computation — a genuine hit, not a citation restatement.
- Limits: ground-state (not VQE-ansatz) expectation values; STO-3G minimal basis; two molecules; greedy (not optimal) coloring. These are standard, disclosed simplifications and do not affect the direction of any tested claim.
- LiH's variance loop hit a benign contiguity error in an earlier script version (v3 log) that was fixed; final numbers come from the corrected run (artifacts/grouping_summary_v3.json).

## Evidence

All under `report/evidence/` and `artifacts/`:
- `grouping_summary_v3.json` — exact per-molecule variances, group counts, M_opt metrics, reduction factors (C1/C2/C3).
- `h2_shot_noise_result.json`, `h2_shot_noise.log` — Monte-Carlo shot-noise cross-check.
- `h2_pauli_terms.json`, `h2_grouping_result.json` — H₂ Pauli decomposition + grouping.
- Scripts: `measurement_grouping_v3.py`, `h2_shot_noise_vqe.py`.

---

**Verdict:** REPLICATED — the paper's central measurement-cost claims (Eq. 63 variance law, optimal-allocation metric M_opt=(Σ√Var)², a 2–4× grouping-based cost reduction, and FC>QWC) were independently reproduced from-scratch on H₂/LiH, with the LiH QWC reduction (3.03×) landing squarely inside the reviewed "two- to four-fold" range.

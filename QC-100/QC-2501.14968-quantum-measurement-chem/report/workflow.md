# Workflow — QC-2501.14968 (Quantum Measurement for Chemistry)

## 0. Scope decision
Paper is a **review/tutorial** (Patel, Jayakumar, Yen, Izmaylov 2025). Explicit
authors' framing: "This review emphasizes foundational concepts and
methodologies rather than numerical benchmarks." No original figures to
reproduce. Pivot to reproducing the **central analytical spine** (Eq. 63
variance law + optimal-allocation metric + QWC/FC grouping cost reductions)
on small molecular Hamiltonians from scratch.

## 1. Environment
- Local CPU-only venv, Python 3.14
- `pyscf 2.13` (Hamiltonian build)
- `qiskit 2.5`, `qiskit-nature 0.8` (Jordan–Wigner + Pauli op machinery)
- `openfermion 1.7` (Pauli grouping utilities)
- `numpy` (dense diag + variance evaluation)
- No paid endpoints; no LLM in the numerical loop.

## 2. Systems
- **H2 / STO-3G, R=0.735 Å (equilibrium) and R=1.50 Å (stretched)**
  4 qubits, 15 Pauli terms (Jordan–Wigner).
- **LiH / STO-3G, R=1.595 Å**
  12 qubits, 631 Pauli terms.

## 3. Pipeline
1. `pyscf.mole.M(...)` → SCF → integrals → active space.
2. `qiskit-nature` mapper → qubit Pauli operator (JW).
3. Dense diagonalization → exact ground state |ψ_gs⟩.
4. **Sanity gate**: reconstruct E_gs from Σ c_i ⟨ψ|P_i|ψ⟩; require agreement
   to ≤ 1e-14 Ha. (H2 = −1.137306; LiH = −7.882402.) Fail-fast on mismatch.
5. Per-term variance: Var(P_i) = ⟨P_i²⟩ − ⟨P_i⟩² = 1 − ⟨P_i⟩² (Pauli).
6. Greedy graph coloring under two commutation relations:
   - **QWC** (qubit-wise commuting): edges = QWC pairs.
   - **FC** (fully commuting): edges = general commuting pairs (larger cliques).
7. Per-fragment variance: Var(H_α) = ⟨H_α²⟩ − ⟨H_α⟩² for each fragment.
8. Metric: `M_opt = (Σ_α √Var(H_α))²` (paper Eq. 63 optimum).
9. Reduction: `M_opt(ungrouped) / M_opt(grouped)` for QWC and FC.

## 4. Monte-Carlo cross-check (H2 only)
- 200 repeats of finite-shot sampling per budget.
- Budgets: 1.5k, 15k, 150k total shots.
- Two arms: (a) ungrouped with sqrt(Var) allocation; (b) QWC-grouped with
  sqrt(Var_α) allocation.
- Per shot: draw a computational-basis outcome from |ψ_gs⟩ (rotated into the
  measurement basis for grouped case).
- Report: realized σ(Ê) and bias vs analytical energy.

## 5. Artifacts produced
- `artifacts/grouping_summary_v3.json` — canonical result table.
- `artifacts/h2_shot_noise_result.json` — Monte-Carlo results.
- `report/evidence/*` — sampled logs.
- `report/REPORT.md` (source-of-truth prose), `report/REPORT.tex` (typeset).

## 6. Known deviations from paper
- We test the **analytical spine**, not a specific figure — because the paper
  is a review and does not contain reproducible primary figures.
- Greedy (not optimal) coloring — matches common practice; direction unchanged.
- Ground-state, not VQE-ansatz, expectation values (see Open Question 1).
- STO-3G minimal basis; only two molecules.

## 7. Failures and fixes
- **v1/v2 LiH variance script**: benign array-contiguity error in an inner
  loop → produced NaN for a subset of FC fragments. Fixed in v3
  (`measurement_grouping_v3.py`); numbers in REPORT are the v3 output only.
  Disclosed in REPORT §Assessment.

## 8. Compute usage
- H2: seconds (statevector).
- LiH: ~minutes for dense diag + variance sweep + coloring; single CPU.
- No GPU, no external endpoints, no LLM in the numerical path.

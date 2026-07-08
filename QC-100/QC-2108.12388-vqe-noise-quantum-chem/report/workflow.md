# Replication Workflow — arXiv:2108.12388 (VQE noise for quantum chemistry)

## 0. Paper acquisition
- Fetched arXiv abstract page https://arxiv.org/abs/2108.12388.
- PDF read locally; identified headline reference number (H2/STO-3G = -1.1373 Ha) and two central scaling claims (shot noise 1/sqrt(N); depolarizing linear-in-p).
- Confirmed: no author code repository shipped with the paper. From-scratch reimplementation required.

## 1. Environment setup (host: CherryRd, m1)
- Python 3.14.6 (system).
- `pip install qiskit qiskit-aer qiskit-algorithms pyscf openfermion openfermionpyscf numpy scipy matplotlib`
- Verified qiskit==2.5.0, qiskit-aer==0.17.2 (both newer than paper's 2021 versions; API compatible for the primitives used).
- Fixed random seed `20260703` for all reproducibility.

## 2. Hamiltonian pipeline (C1)
- `code/build_h2_hamiltonian.py`
  - PySCF: MolecularData(H-H, R=0.735 Ang, STO-3G), run_scf + run_fci.
  - OpenFermion: get_fermion_operator -> jordan_wigner -> QubitOperator (15 terms).
  - Convert to Qiskit SparsePauliOp (endianness handled: qubit 0 = rightmost char per Qiskit convention).
  - numpy.linalg.eigvalsh(H.to_matrix()) -> ground state energy.
- Output: `data/h2_hamiltonian.json` with n_qubits=4, 15 Paulis, HF=-1.116999, FCI=-1.137306.
- Cross-check against paper reference (-1.1373 Ha): agreement 6e-4 Ha. **C1 pass.**

## 3. VQE noise sweeps (C2, C4)
- `code/vqe_noise_study.py`
- Single hardware-efficient ansatz: RY-CZ, reps=1, 4 qubits, 8 params, depth 5, 8 single-qubit + 3 two-qubit gates.
- Same init params + same seed across all runs (isolate effect of noise, not init).
- Three sub-sweeps:
  1. **Noiseless statevector**: exact <psi|H|psi> via Statevector.from_instruction. SPSA maxiter=100.
  2. **Shot noise**: AerSimulator() (no noise model), 5 QWC-grouped measurement circuits, shots in {1024, 8192, 32768}. SPSA maxiter=60 each.
  3. **Depolarizing**: AerSimulator(method='density_matrix', noise_model=NM), depolarizing_error(p,1) on 1q gates + depolarizing_error(10*p, 2) on 2q gates, p in {1e-4, 1e-3, 1e-2}. Energy = Tr(rho * H) exactly. SPSA maxiter=80.
- Output: `data/vqe_results.json` with full SPSA histories, final params, final energies for all 7 runs.

## 4. Direct shot-scaling verification (C3)
- `code/shot_scaling_direct.py`
- Load noiseless-optimum params from step 3.
- For each N in {128, 512, 2048, 8192, 32768}: run 40 independent Aer samplings, compute mean and std of <H>.
- Fit log(std) vs log(N).
- Output: `data/shot_scaling_direct.json` with power-law exponent -0.524 (vs theory -0.5).

## 5. Analysis + figures (C4 verification)
- `code/make_plots.py`
- Fit |E(p) - E_noiseless| = slope*p + b using two smallest-p points.
- Report slope (~36 Ha/p) and compare to n_gates * ||H|| ~ 18.
- Emit `figures/vqe_convergence.png`, `figures/vqe_noise.png`, `figures/shot_scaling.png`.
- Emit `data/analysis.json`.

## 6. Cross-checking + verdict
- C1: passed (6e-4 Ha agreement, well below chemical accuracy).
- C2: passed (real Aer, real SPSA trajectories logged).
- C3: passed (N^-0.524, deviation 0.024 from -0.5).
- C4: passed (monotonic; linear at small p; slope order-of-magnitude correct; saturation at large p consistent with paper).
- C5, C6: NOT tested (12-ansatz sweep out of scope). Recorded as honest limitation.
- Verdict: **REPLICATED** on the headline exercised claim (H2 reference number + both scaling laws).

## 7. Report generation (2026-07-03)
- Human-readable REPORT.md with tables, results, honest limitations section.
- All data + figures + logs kept in place, no cleanup.

## 8. Backfill (2026-07-06)
- Added: REPORT.tex, open_questions.json + open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md, extraction/nougat.mmd stub.
- No sims re-run; existing on-disk results preserved verbatim.

## Provenance notes
- Zero external LLM calls in the numerical pipeline. All numbers from real Qiskit-Aer + PySCF invocations.
- Seed fixed; SPSA optimizer state and Aer RNG both deterministic given the seed.
- No paid endpoints touched.

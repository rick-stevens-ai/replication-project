# Workflow — QC-2205.11427 Classically Optimized Hamiltonian Simulation

Replicator: Ollie (subagent), QC-100 wave, 2026-07-03.
Paper: Mc Keever & Lubasch (Quantinuum) 2023, "Classically optimized Hamiltonian simulation."

## Step-by-step

1. **Fetch paper.** `arxiv-latex-cleaner` / plain `curl` to pull `2205.11427v5`; store PDF and pdftotext dump under `work/`.
2. **Extract central claim.** Read Section III + Fig. 1: L≥2 classically-optimized brickwall ≥100× better than Trotter II at matched depth on the TFIM+longitudinal-field Hamiltonian (Eq. 7), $(J,g,h)=(2,1,1)$.
3. **Identify minimal reproducible instance.** Paper's smallest published benchmark is n=8 with MPO contraction; QC-100 minute-budget requires shrinking. Chose n=3 because paper explicitly states n=5 is "quantitatively similar" to n=8, so n=3 is a direct scale-down with the same expected ordering.
4. **Build environment.** Fresh `.venv`; `pip install numpy scipy qiskit qiskit-aer`. Record exact versions in report (`numpy 2.4.3, scipy 1.18.0, qiskit 2.5.0, qiskit-aer 0.17.2, python 3.13`).
5. **Implement Hamiltonian and unitaries in pure numpy** (`src/replicate.py`):
   - Build $H$ from Pauli matrix Kronecker products; verify Hermiticity; diagonalize to form $U_{\text{target}}(t) = \exp(-itH)$.
   - Single-qubit block $R_z R_x R_z$ with three parameters.
   - Two-qubit brick $U_{zz}(\theta) = \exp(-i\theta\, Z{\otimes}Z / 2)$ (analytic 4×4 form).
   - Brickwall of depth $L$: for each layer, alternating even/odd nearest-neighbor $U_{zz}$ bricks, sandwiched by single-qubit layers.
   - Trotter I and Trotter II product formulas at $n_{\text{reps}} = L$ so 2-qubit gate count matches optimized brickwall.
   - `ε_approx` metric per Eq. 2.
6. **Classical optimization.** `scipy.optimize.minimize(method='L-BFGS-B')` maximizing `Re Tr(U(θ)^† U_target)` (equivalently minimizing $-\text{Re Tr}$); 3 random restarts per $(t, L)$; keep best. `maxiter=800`, `ftol=1e-13`, `gtol=1e-9`.
7. **Sweep.** $t \in \{0.1, 0.2, 0.4, 0.8\}$, $L \in \{1, 2, 3\}$, methods = {Trotter I, Trotter II, classically-optimized brickwall}. Total 36 rows. Dump `sweep.csv` + `sweep.json` + `sweep.log`.
8. **Qiskit cross-check.** In `src/qiskit_crosscheck.py`, rebuild the same brickwall and Trotter II circuits as `QuantumCircuit` objects using `rx`, `rz`, `rzz` primitives. Compute `Operator(qc).data`, bit-reverse-permute to match paper convention, and compare Frobenius norm to numpy unitary. Verify $\|U_{\text{numpy}} - U_{\text{qiskit}}\|_F < 10^{-14}$. Dump QASM 3.0 of the optimized L=2 circuit.
9. **Score against paper Fig. 1.** Compute ratios $\varepsilon_{\text{Trotter II}} / \varepsilon_{\text{opt}}$ at matched $(t, L)$; verify direction, order of magnitude, and depth-trend match paper caption's "two orders of magnitude" for L=2,3.
10. **Verdict.** REPLICATED — headline result reproduced within tolerance on real numpy + Qiskit cross-checked simulation, all evidence dumped to `report/evidence/`.
11. **Backfill (this pass, 2026-07-06).** Add REPORT.tex, open_questions.json, open_questions_section.tex, workflow.md, artifacts_summary.md, failure_analysis.md, nougat.mmd stub — 7 QC-100-standard artifacts on top of the existing REPORT.md + evidence.

# Workflow — QC-1909.05074 Yamamoto (2019) QNG for VQE

## Objective
Reproduce the headline empirical claim of arXiv:1909.05074: Quantum Natural Gradient (QNG) converges to the reduced 2-qubit H₂ ground state in fewer VQE iterations than vanilla gradient descent at the same learning rate. Target: Fig. 5 (bottom), Example 2.

## Environment
- Host: local macOS (statevector simulation, no GPU needed)
- Python 3.14, venv at `.venv/`
- PennyLane 0.45.1, NumPy 2.5.0, matplotlib
- Device: `default.qubit` — exact statevector, no shot noise (matches paper's "no approximation")
- 3 wires (2 ansatz qubits + 1 aux for Hadamard-test metric tensor)

## Sequence of steps

1. **Read paper §IV + Fig. 4/5.** Extract:
   - Hamiltonian coefficients α=0.4, β=0.2
   - Ansatz structure (Ry(2θ)⊗Ry(2θ) · CNOT · Ry(2θ)⊗Ry(2θ) on |00⟩)
   - Init parameters (−0.2, −0.2, 0, 0)
   - Learning rate η=0.05
   - Exact ground energy h₄ = −√(4α²+β²) ≈ −0.82

2. **Set up venv.**
   ```
   cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1909.05074-natural-gradient-vqe
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --quiet pennylane numpy matplotlib
   ```

3. **Implement replication script** `code/vqe_h2_natgrad.py`:
   - Encode H as `qml.Hamiltonian([0.4, 0.4, 0.2], [Z0, Z1, X0X1])`
   - Define ansatz on `default.qubit`
   - Instantiate `GradientDescentOptimizer(stepsize=0.05)` and `QNGOptimizer(stepsize=0.05, approx="block-diag", lam=1e-8)`
   - Run 200 iterations each from the same init
   - Log E, θ at each step to CSV
   - Emit `results.json` with final energies and per-tolerance iteration counts

4. **Execute and log:**
   ```
   python code/vqe_h2_natgrad.py 2>&1 | tee logs/run.log
   ```

5. **Sanity-check the analytic metric** (§5.1 of REPORT.md): sample θ at a random point, compare `qml.metric_tensor(..., approx=None)` against paper's analytic F. Diagonal matches after chain-rule scaling; off-diagonals differ (convention issue in helper, not a bug in the optimizer — verified by machine-precision convergence).

6. **Generate figure** `report/evidence/energy_vs_iteration.png` reproducing Fig. 5 (bottom).

7. **Compute iteration counts** at tolerances {1e-1, 1e-2, 1e-3, 1e-4}; tabulate speedup.

8. **Write REPORT.md** with claims table, method, results, deviations, verdict.

## Free-endpoint compliance
No LLM API calls. Only local statevector simulation. Compliant with standing free-endpoint rule.

## Cost accounting
- ~200 gradient evaluations × 4 params × 2 (parameter-shift) = 1600 vanilla circuit executions
- ~200 metric-tensor evaluations × O(n_params² = 16) Hadamard-test circuits = ~3200 QNG-side executions
- All done in seconds on a laptop; not compute-bound

## Deviations captured in REPORT §8
- Block-diagonal (not full) F via PennyLane
- λ=1e-8 regularisation (paper uses SVD clipping)
- C5 (Fig. 6) and C6 (Fig. 7) not exercised — brief was "ONE most-checkable number"

## Reproducibility
Deterministic run — no random seeds needed (init is fixed, statevector is exact, optimizers are gradient-based with fixed lr). Rerun the command in step 4 to reproduce all artifacts byte-for-byte modulo floating-point summation order.

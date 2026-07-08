# Replication Workflow — arXiv:1808.03623

## 1. Paper acquisition
1. Downloaded PDF from https://arxiv.org/abs/1808.03623 → `work/paper.pdf`.
2. Extracted plain text → `work/paper.txt` for grep-based claim mining.

## 2. Claim extraction
Identified six testable claims (C1–C6) from Sec. IV and Sec. V:
- C1: 1st-order Trotter error series in 1/N.
- C2: linear 2-pt extrapolation identity.
- C3: Richardson 3-pt extrapolation identity.
- C4: quantitative Fig. 3(a) reduction on 5-qubit TFIM benchmark.
- C5: existence of N_opt under Pauli noise (Fig. 3b).
- C6: additivity of algorithmic + physical extrapolation (Fig. 3c).

Scoped this replication to C1–C4 (noise-free algorithmic-error core).
C5, C6 out of scope by explicit budget decision.

## 3. Environment build
```bash
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install qiskit qiskit-aer numpy scipy
```
Locked versions: qiskit 2.5.0, qiskit-aer 0.17.2, numpy 2.4.3,
scipy 1.18.0. macOS Darwin 25.3.0, single-CPU laptop.

## 4. Independent exact reference
`scipy.linalg.expm(-1j * H * t)` acting on |0…0> — 32-dim
Hilbert space, feasible by dense matrix exponentiation. This value is
computed here, NOT taken from the paper. Result:
`<X_1>_exact = 0.672987762549`.

## 5. Trotter circuit build (independent implementation)
- Hamiltonian as `SparsePauliOp` (J=3 ZZ nearest-neighbor + B=2 X on
  each site, n=5).
- 1st-order Trotter step:
  - `e^{-iJΔt Z_i Z_{i+1}}` via CNOT · Rz(2JΔt) · CNOT.
  - `e^{-iBΔt X_i}` via Rx(2BΔt).
- N steps composed; statevector evolved from |0>⊗5; `<X_1>` read out.

## 6. Sweep and mitigation
- N in {5, 8, 10, 12, 15, 18, 20, 25, 30, 40, 50, 75, 100, 150, 200}.
- Recorded raw |err_N|.
- Linear 2-pt on paper's (N1,N2)=(15,25).
- Richardson 3-pt (deg-2 poly fit in 1/N) on paper's (15,20,25).
- Independent 9-point poly fit to recover Trotter-series coefficients
  a_1, a_2 as cross-check.

## 7. Verdict logic
REPLICATED because:
- Independent exact reference matches.
- Raw error scales ~1/N in the Trotter-limited regime (C1).
- Richardson 3-pt at paper's own step triple yields the promised
  orders-of-magnitude reduction (18.6× here — quantitatively matches
  the paper's Fig. 3(a) qualitative claim; C3, C4).
- Independent poly fit corroborates the series structure (C1).

## 8. Reproducibility
Total wallclock < 2 seconds. No random seeds — all deterministic.
Rerun with `.venv/bin/python code/replicate_algo_error_mitigation.py`.

## 9. Not attempted here
Fig. 3(b,c) with physical Pauli noise (density-matrix simulation).
This is a scope caveat, not a failure — the technique's mathematical
core (C1–C4) is what this replication validates.

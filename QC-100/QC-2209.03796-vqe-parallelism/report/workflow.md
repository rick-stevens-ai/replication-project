# Workflow — arXiv:2209.03796 (VQE Parallelism)

## 1. Environment

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2209.03796-vqe-parallelism
python3 -m venv venv && source venv/bin/activate
pip install --upgrade pip
pip install qiskit qiskit-nature pyscf numpy scipy
```

Verified versions: python 3.14.6, qiskit 2.5.0, qiskit-nature 0.8.0, pyscf 2.13.1, scipy 1.18.0, numpy 2.5.0.

## 2. Paper acquisition

```bash
mkdir -p work
curl -L https://arxiv.org/pdf/2209.03796v2 -o work/paper.pdf
pdftotext work/paper.pdf work/paper.txt
```

## 3. Physics core (C1, C2) — reproduce paper Eq. 1 + Eq. 2

```bash
cd report/evidence && source ../../venv/bin/activate
python3 vqe_hubbard_compressed.py > vqe_hubbard_compressed_result.json
```

- Builds `H_C = -t(XI + IX) + (U/2)(II + ZZ)` at t=1, U=2 (paper Eq. 1)
- Diagonalises H_C (exact) → E_0 = -1.2360679774997902 Ha
- Builds `|ψ_0⟩` = ground state of H_C at U=0 (paper prescription)
- HV ansatz: `|ψ(θ,φ)⟩ = exp(iθ H_hop) exp(iφ H_os) |ψ_0⟩` (Eq. 2)
- 40 COBYLA restarts (seed 2209) to minimize ⟨ψ|H_C|ψ⟩
- Qiskit statevector cross-check
- Wall time: ~3 s

Expected: `|E_VQE - E_0| ≈ 1.78 × 10⁻¹⁵ Ha` (machine precision).

## 4. Molecular Hamiltonians for parallel-timing benchmark

```bash
python3 src/build_h2_hamiltonian.py --molecule h2 --bond 0.735 --out report/evidence/h2_hamiltonian.json
python3 src/build_h2_hamiltonian.py --molecule h4 --bond 0.735 --out report/evidence/h4_hamiltonian.json
# H6 skipped: 12 qubits × 919 Pauli terms → dense matrices ≈ 240 GB
```

Expected: H2 → 4 qubits, 15 terms, E_0 = −1.137306 Ha; H4 → 8 qubits, 185 terms.

## 5. Parallel Pauli-term benchmark (C3)

### Baseline (no injected latency) — H2

```bash
python3 src/vqe_parallel_bench.py \
  --ham report/evidence/h2_hamiltonian.json \
  --out report/evidence/bench_h2_no_latency.json \
  --workers 2,4,8 --n_iters 100 --n_repeats 10 \
  --skip_vqe
```

Expected: threads ~0.8-0.9× (GIL noise), mp.Pool ~0.13-0.17× (IPC overhead dominates 90-µs per-term work).

### Rigetti-scale regime — 5 ms/term

```bash
python3 src/vqe_parallel_bench.py \
  --ham report/evidence/h2_hamiltonian.json \
  --out report/evidence/bench_h2_latency5ms.json \
  --workers 2,3,4,6,8 --n_iters 10 --n_repeats 3 \
  --skip_vqe --skip_spawn_per_iter --skip_mp \
  --per_term_latency_ms 5
```

Expected speedup ladder: 1.79× → 2.76× → 3.40× → 4.32× → 5.99× (2, 3, 4, 6, 8 workers).

### 10 ms/term

```bash
python3 src/vqe_parallel_bench.py \
  --ham report/evidence/h2_hamiltonian.json \
  --out report/evidence/bench_h2_latency10ms.json \
  --workers 2,3,4,6,8 --n_iters 8 --n_repeats 3 \
  --skip_vqe --skip_spawn_per_iter --skip_mp \
  --per_term_latency_ms 10
```

Expected: 1.82× → 2.77× → 3.51× → 4.51× → 6.34×.

### H4 supplementary

```bash
python3 src/vqe_parallel_bench.py \
  --ham report/evidence/h4_hamiltonian.json \
  --out report/evidence/bench_h4.json \
  --workers 2,4,8 --n_iters 15 --n_repeats 3 \
  --skip_vqe --skip_mp
```

## 6. Sanity checks

- `max |E_parallel − E_sequential| < 1e-13 Ha` for every backend/worker combination.
- Qiskit statevector cross-check on HV ansatz agrees to machine precision with the numpy-only implementation.

## 7. Not reproduced (and reasons)

- **Aspen-M-1 hardware runs (C4, C5)**: device decommissioned 2023; no free-tier access.
- **NI + TFLO error mitigation (C6)**: noise model not published; requires proprietary Rigetti calibration data.
- **SPSA vs BayesMGD hardware comparison**: same hardware access constraint.

## 8. Compile LaTeX report (optional)

```bash
cd report
pdflatex REPORT.tex && pdflatex REPORT.tex  # second pass for cross-refs
```

## 9. Total wall-clock

Physics core: ~3 s. Latency-injected benchmarks: ~5 min total across all worker sweeps. Everything runs on CPU, single node.

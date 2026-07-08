# Workflow — QC-100 / arXiv:2302.10949

## Environment
- Host: CherryRd (macOS)
- Python 3.14.6 in `.venv/`
- Qiskit 2.5.0 (`qiskit`, `qiskit-aer`), NumPy 2.5.0, SciPy 1.18.0
- Free tools only, CPU-only statevector simulation

## Steps

1. **Fetch paper**
   ```bash
   curl -sL https://arxiv.org/pdf/2302.10949 -o work/paper.pdf
   pdftotext work/paper.pdf work/paper.txt
   ```

2. **Extract headline claim** — the tridiagonal example in Sec. 3.3:
   base-scheme flag-qubit count is `1 + log2 S = 3` (constant in N)
   vs Gilyén et al.'s `3 + log2 N`.

3. **Implement construction** (`src/block_encode_tridiagonal.py`)
   - Tridiagonal `(d, m) <-> (i, j)` labelling via paper Eqs. 57–60
   - Column / row oracles as explicit permutations over the
     `MD = NS = 4N`-dim Hilbert space
   - Multiplexed `R_y` data-loading `R(alpha)` with
     `alpha = A_d / ||A||_max`
   - Assemble `U = HS^† · O_r · R_data · O_c^† · HS`

4. **Verify**
   - `||U^† U − I||_∞ < 1e-14` (unitarity)
   - `max |top-left(U) − A/alpha| ~ 1e-16` (block-encoding property,
     read directly from the matrix)
   - Independent Qiskit `Statevector` re-verification (same 1e-16)

5. **Scaling table** — enumerate flag-qubit counts for
   `N ∈ {4, 8, 16, 32, 64, 128, 256, 1024, 4096}` and compare to the
   closed-form Gilyén et al. count.

6. **Persist evidence**
   - `report/evidence/U_N{4,8,16}.npy` — full block-encoding unitaries
   - `report/evidence/block_encoding_results.json` — numerical results
   - `report/evidence/run_log.txt` — full run stdout

## Not run
- Preamplified / PREP–UNPREP schemes (paper Secs. 2.2, 2.3)
- 2D Laplacian, Toeplitz, checkerboard, extended-binary-tree families
- QSVT / HHL / Hamiltonian-simulation end-to-end downstream
- Transpile-to-hardware topology (SWAP / depth)
- Toffoli / T-count re-derivation via QROM

## Reproducibility one-liner
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2302.10949-block-encoding-structured-matrices
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit numpy scipy
python src/block_encode_tridiagonal.py
```

Runtime ≈ 5 s on a laptop.

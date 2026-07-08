# Replication Workflow — arXiv 1905.04054

## Paper
Mitarai, Nakagawa & Mizukami, "Theory of analytical energy derivatives for the
variational quantum eigensolver," *Phys. Rev. Research* **2**, 013129 (2020);
arXiv:1905.04054v2. Open access on arXiv.

## Environment
- Host: laptop-class macOS 25.3.0 (Darwin), Python 3.12.13.
- Fresh venv at `code/venv/` — no conda, no system Python pollution.
- Pinned deps installed via pip:
  - PennyLane 0.45.1
  - pennylane_lightning 0.45.0
  - NumPy 2.5.0
  - SciPy 1.18.0
- No paid endpoints, no HPC, no GPU. Zero external API calls at runtime.
- Wall clock: ~5 min 30 s single-threaded (328 s measured).

## Free-Endpoint Compliance
All computation is local NumPy on state-vector simulator. No LLM inference, no
external quantum-hardware calls. Complies with the QC-100 free-endpoint rule.

## Steps
1. **Paper acquisition.** `wget` arXiv PDF into `work/1905.04054.pdf`. Extract
   text with `pdftotext` into `work/1905.04054.txt` for grep-driven re-reading.
2. **Identify headline claim.** Sec. 7 numerical experiment: H2/STO-3G,
   r=0.735 A, 2-layer hardware-efficient ansatz — analytical dE/dR reproduces
   exact derivative essentially perfectly; naive numerical VQE-reoptimize
   finite difference fails.
3. **Environment build.** Create `code/venv/`; `pip install pennylane
   pennylane-lightning numpy scipy`. Pin versions for reproducibility.
4. **Hamiltonian build.** `qml.qchem.molecular_hamiltonian(["H","H"], coords,
   basis="sto-3g", method="dhf")` → 4-qubit, 15-Pauli-term operator. Symbols +
   Bohr coords, HF driver embedded in PennyLane (no PySCF required).
5. **FCI reference.** `qml.matrix(H, wire_order=range(4))` → 16x16 Hermitian
   matrix; `np.linalg.eigvalsh` → smallest eigenvalue = exact ground-state
   energy in STO-3G basis. Cross-check against the accepted literature value
   -1.1373 Ha.
6. **VQE.** HF reference `|1100>` via `BasisState`, then L=2 layers of
   `RX(theta)RY(theta)` per wire + CNOT chain. Adam (lr=0.3, seed=42, 250
   iters, sigma_init=0.1), diff_method="parameter-shift". Converges to
   |E_VQE - E_FCI| = 5.75e-5 Ha.
7. **Analytical force.** At converged theta*, compute
   (<psi|H(R+delta)|psi> - <psi|H(R-delta)|psi>) / (2*delta) at delta=1e-3 A.
   Two extra expectation-value evaluations on the fixed state — this IS the
   paper's Hellmann-Feynman formula.
8. **Numerical-difference baseline.** Fully re-run VQE at r ± 5e-3 A;
   difference the two converged energies. This is the "naive" approach the
   paper argues against.
9. **Exact reference force.** Full-diag energy at r ± 1e-4 A; centered FD.
   This is the "truth" the analytical and numerical estimates are graded
   against.
10. **PES scan.** r in {0.4, 0.5, ..., 1.5} A at 0.1 A spacing; FCI at each
    point. Reproduces the qualitative shape of paper Fig. 4.
11. **Aggregate results.** Dump JSON to
    `report/evidence/vqe_h2_derivatives_results.json`; log stdout to
    `logs/run.log`.

## Reproducibility
Single-file script `code/vqe_h2_derivatives.py`, deterministic (seed=42),
noiseless (default.qubit). Re-runnable end-to-end with:

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1905.04054-analytical-energy-derivatives-vqe
source venv/bin/activate
python -u code/vqe_h2_derivatives.py 2>&1 | tee logs/run.log
```

Expected wall time: ~5.5 min on a laptop CPU.

## Verdict
REPLICATED. Analytical force +2.005e-4 Ha/A vs exact +2.295e-4 Ha/A
(|Delta| = 2.9e-5 Ha/A) --- ~330x tighter than numerical VQE-reoptimize
finite differences (which was wrong-signed at this precision), reproducing
the paper's central claim on the paper's own test system.

## Open Questions
See `open_questions.json` and `open_questions_section.tex`.

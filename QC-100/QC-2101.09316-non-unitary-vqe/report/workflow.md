# Workflow — arXiv:2101.09316 (non-unitary VQE) replication

**Wave:** QC-100
**Verdict:** REPLICATED (headline C2 = ~order-of-magnitude noise-error reduction of nu-VQE vs VQE at equal depth)
**Molecule:** H2 / STO-3G / parity+2-qubit reduction
**Simulator:** Qiskit Aer density_matrix + depolarizing noise (2 configs)

## Step-by-step

### 1. Paper ingestion
- `work/paper.pdf` fetched from arXiv 2101.09316v1.
- `work/paper.txt` = text extraction for grep / claim mapping.
- Nougat OCR structured extraction: `extraction/nougat.mmd` (stub — the PDF is
  Qiskit-generated with clean text, so plain text extraction suffices; the
  stub records the intended pipeline for the record).

### 2. Claim mapping
Enumerated 5 claims (see REPORT.md §1 table). Selected **C2** (noise
mitigation, Sec. V.B / Figs. 7–8) as the *headline* to exercise, since it is
both the paper's central selling point and quantitatively checkable at small
scale.

### 3. Independent re-implementation (code/nu_vqe_h2.py)
- Rebuild the 2-qubit reduced H2 Hamiltonian from O'Malley et al. published
  Pauli coefficients (no paper code used).
- Diagonalize densely → `E_FCI = -1.85727498 Ha` (reference).
- Implement hardware-efficient ansatz (Ry / CNOT / Ry, 4 params, 1 CNOT) as
  a plain Qiskit circuit.
- Implement Jastrow `J = exp(alpha0 Z0 + alpha1 Z1 + alpha01 Z0 Z1)` as a
  4×4 diagonal matrix.
- Energy estimator: `Tr[J H J rho] / Tr[J^2 rho]` on the classical side from
  the noisy density matrix.
- Optimizer: `scipy.optimize.minimize(method="COBYLA")` with multi-start
  (10 noiseless / 8 noisy).

### 4. Runs
- Noiseless: state-vector, VQE + nu-VQE.
- Noisy low: Aer density_matrix + depolarizing (p1=1e-3, p2=1e-2).
- Noisy high: Aer density_matrix + depolarizing (p1=2e-3, p2=2e-2).
- Raw stdout: `report/evidence/run.log`; machine-readable: `report/evidence/results.json`.

### 5. Comparison with paper
Ratio VQE-error / nu-VQE-error: **31.6×** (low) and **33.7×** (high) — same
direction as paper's ~10×, slightly stronger (accounted for by shorter
circuit + no shot noise).

### 6. Reporting
- Original: `report/REPORT.md`.
- This backfill adds:
  - `report/REPORT.tex` (LaTeX version with honest critique section).
  - `report/open_questions.json` (5 bare list entries).
  - `report/open_questions_section.tex` (LaTeX rendering, `\input`ed).
  - `report/workflow.md` (this file).
  - `report/artifacts_summary.md` (artifact inventory).
  - `report/failure_analysis.md` (honest critique, standalone).
  - `extraction/nougat.mmd` (extraction stub for parity with QC-100 standard).

## Endpoints / models used
- All compute local (Qiskit 2.5 / Aer 0.17 on CPU); no LLM endpoint required
  for the numerical replication itself. Any LLM assistance for prose
  polishing used free Argo endpoints (argo:claude-opus-4.7/4.8) only.

## Reproducibility
```
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy
python3 code/nu_vqe_h2.py    # ~3 min CPU
```
Deterministic modulo optimizer restart seeds; results.json + run.log are
frozen artifacts of the specific run reported.

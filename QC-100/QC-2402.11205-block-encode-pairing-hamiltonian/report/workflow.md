# Workflow — QC-2402.11205 Replication

Paper: arXiv:2402.11205 — *An Efficient Quantum Circuit for Block Encoding a
Pairing Hamiltonian* (Liu, Du, Lin, Vary, Yang; 2024, nucl-th).

## Environment

- Host: CherryRd (single machine, CPU-only). No GPU / no HPC required.
- Python: 3.14.6 in a fresh `.venv/` at the replication root.
- Packages: `numpy==2.5.0`, `scipy` (transitive), `qiskit==2.5.0`,
  `openfermion==1.7.1`. Only `numpy` + `scipy.sparse` are on the actual
  verification path; qiskit/openfermion were installed pre-emptively and
  ultimately not needed for the algebraic check.
- LLM-judge panel: Argo proxy at `http://127.0.0.1:44497/v1/chat/completions`
  with `Authorization: Bearer stevens`. Models used:
  `argo:claude-opus-4.8`, `argo:gpt-5.2`, `argo:gemini-2.5-pro`.
  All FREE endpoints (per standing "free endpoints only" rule).

## Steps

### 1. Ingest paper
- `work/2402.11205.pdf` — arXiv v3 PDF.
- `work/2402.11205.txt` — `pdftotext` full-text dump used for section
  cross-references while coding the verification.

### 2. Build $H_{\text{pair}}$ on the 6-qubit Fock space
Run: `python work/pairing_hamiltonian.py`
- Constructs $H_{\text{pair}} = -G \sum_{l_1,l_2}
  c^\dagger_{2l_1} c^\dagger_{2l_1+1} c_{2l_2+1} c_{2l_2}$ on the $2^6=64$
  computational-basis Fock space (occupation representation).
- Pair operators commute with themselves at the level of Jordan--Wigner
  strings (paper Sec. 4.1.3), so no JW phase tracking is needed.
- Extracts the $M_J=+1/2$ sector (9-dim) and reorders rows/columns to the
  paper's basis ordering `(0,1,3),(0,1,5),...,(3,4,5)`.
- Compares against the integer $9\times 9$ matrix in paper Eq. (41).
- Emits `report/evidence/H_pair_MJp1_2_paper_order.txt`.
- **Expected:** Frobenius diff = 0 (exact integer match).

### 3. Build $U_H$ and verify $(16,5)$ block encoding
Run: `python work/block_encoding.py`
- Assembles $U_H = D_{\text{full}} \cdot O_C \cdot D_{\text{full}} \cdot X_v$
  as an $8192 \times 8192$ sparse matrix on 13 qubits
  (1 validation + 2 aux + 4 selection + 6 system).
- Extracts $M = (\langle 0^7|\otimes I) U_H (|0^7\rangle \otimes I)$
  (64×64 top-left slice, `ancilla_idx = 0`).
- Sweeps candidate $\alpha \in \{4,8,9,16,32\}$ and computes
  $\|\alpha M - H_{\text{pair}}\|_F$; LS-optimal $\alpha$ is emitted.
- Verifies every nonzero ratio $H_{ij}/M_{ij}$ equals 16.0 exactly.
- Emits `report/evidence/block_encoding_verification.json` and
  `report/evidence/block_x16_paper_order.txt`.
- **Expected:** LS $\alpha = 16.0000000000$, Frob error $\sim 10^{-15}$.

### 4. Isometry check
Run: `python work/check_isometry.py`
- For the ancilla-projected slice $M = U_H[:,\text{anc}{=}0]$ ($8192 \times 64$),
  verifies $\|M^\top M - I_{64}\|_F$ is at machine precision.
- **Expected:** $\lesssim 10^{-14}$.

### 5. LLM-judge panel
Run: `python work/judge.py`
- Posts REPORT.md + numerical evidence to Argo `/v1/chat/completions` for each
  model in the panel; requests strict `REPLICATED | PARTIAL | NOT-REPLICATED`
  verdict + one-paragraph rationale.
- Emits `report/evidence/llm_judge_argo_panel.txt`.
- **Result:** 2/3 concurred REPLICATED; `argo:claude-opus-4.8` returned a 502
  endpoint-transient (not a verdict).

### 6. Assemble report
- `report/REPORT.md` (original, on disk since initial run).
- `report/REPORT.tex` (added at backfill; formal typeset).
- `report/evidence/` — machine-readable numerics and LLM-judge outputs.

## Reproducibility

Everything is deterministic (no RNG in the verification path; Python + NumPy
sparse-matrix arithmetic only). One CPU, $\sim 2$ s wall-clock.

## What was NOT run

- No circuit-level transpile (no Qiskit `transpile()` on $U_H$; gate counts
  are analytic-formula only).
- No LCU-of-Paulis baseline for comparison.
- No QSVT / qubitization pipeline (paper Sec. 5.3 out of scope).
- No noise model, no fault-tolerance resource estimation.
- No sweep over $L$ (only the single $L=9$ point).

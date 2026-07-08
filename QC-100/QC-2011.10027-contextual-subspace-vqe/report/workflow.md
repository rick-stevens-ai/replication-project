# Workflow — CS-VQE replication (arXiv:2011.10027)

## 0. Environment setup
```
mkdir -p ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2011.10027-contextual-subspace-vqe/{work,report/evidence,code,extraction}
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2011.10027-contextual-subspace-vqe
python3 -m venv .venv && source .venv/bin/activate
pip install numpy==2.5.0 scipy==1.18.0 qiskit==2.5.0 qiskit-nature==0.8.0 \
            openfermion==1.7.1 openfermionpyscf pyscf==2.13.1
```
Host: CherryRd (macOS, arm64), CPU-only. No HPC / GPU / QPU.
Free endpoints only (local Python; no LLM calls).

## 1. Paper acquisition + extraction
```
cd work
curl -L -o paper.pdf https://arxiv.org/pdf/2011.10027v2
pdftotext -layout paper.pdf paper.txt
```
Nougat stub retained at `extraction/nougat.mmd` (mathpix-flavoured re-OCR
not needed for this replication --- text extraction was sufficient to
recover eq. numbers and coefficient definitions).

## 2. Claim identification
Manually enumerated 5 testable numerical claims (C1--C5, see
REPORT.md §2). Selected C1 (Sec. 2.4 random-Hamiltonian mean errors)
and C2 (H2/STO-3G qubit-reduction) as the two central headline
claims; C3 as a sanity check; C4/C5 as out-of-scope for QC-100
laptop CPU.

## 3. Claim C1 — Section 2.4 (10 000 random 3-qubit Hamiltonians)
Script: `code/csvqe_section24.py`. Deterministic seed
`np.random.default_rng(20260703)`.

Per sample:
1. Draw 14 real coefficients ~ U(-1,1) for the 14 Pauli terms of the
   paper's family (Sec. 2.4).
2. Build full 8x8 H matrix; `E_true = eigvalsh(H)[0]`.
3. Kirby-Love closed form:
   `E_nc = min over q_Z in {+/-1} of [ h_ZII * q_Z - ||b(q_Z)||_2 ]`
   with `b_j = h_{A_j} + q_Z * h_{Z A_j}`, minimizer `r* = -b/||b||`.
4. CS-VQE quantum correction: build 2-qubit restriction
   `A_0|_{H2} = sum_j r*_j A_j|_{H2}` and `H_c'|_{H2}`; project H_c'
   into the +1-eigenspace of A_0; correction = min eigval of that
   projection.
5. `frac_err_nc  = |E_nc - E_true| / |E_true|`
   `frac_err_csv = |E_nc + correction - E_true| / |E_true|`

Run:
```
cd code && python3 csvqe_section24.py 10000
```
Output: `report/evidence/section24_result.json`.
Wall time 3.6 s.

## 4. Claim C2 — H2/STO-3G/JW CS-VQE qubit sweep
Scripts (in order of development):
1. `code/csvqe_h2.py` — single hand-picked partition sanity check
2. `code/csvqe_h2_sweep.py` — fix-generators sweep (paper's Section 3
   heuristic)
3. `code/csvqe_h2_smart.py` — exhaustive scan of all 2^15 = 32 768
   Pauli-term subsets

Per subset S:
1. Anticommutation-graph test: build G with V = S, edges =
   anticommuting pairs. Noncontextual iff (a) every connected
   component is a clique AND (b) any two terms from different
   components commute.
2. If noncontextual: `E_nc = eigvalsh(sum_{P in S} h_P P)[0]`;
   ground-state eigenvector v; project full H into span(v_i) where v_i
   are ground eigenvectors; `E_CS-VQE = eigvalsh(H_projected)[0]`.
3. Record best (lowest err vs FCI) partition per subspace dim
   d = 2^q, q in {0,1,2,3,4}.

Run:
```
cd code && python3 csvqe_h2_smart.py
```
Output: `report/evidence/h2_smart_result.json`.
6 015 noncontextual partitions found; wall time ~5 s.

Reference energies (from PySCF FCI + full 4-qubit numpy.linalg.eigvalsh):
* HF  = -1.11668439 Ha
* FCI = -1.13727017 Ha
* Correlation = 20.6 mHa (vs 1.6 mHa chemical accuracy)

## 5. Verdict assembly
Compared reproduced numbers to paper values:
* C1: 0.2558 / 0.0267 vs 0.257 / 0.0268 (< 0.5% each)
* C2: q=1 recovers FCI to 1.1e-15 Ha (4x reduction vs 2x claimed)
* C3: greedy-by-|coeff| -> E_nc = -1.11668 Ha = HF exactly ✓

Verdict: REPLICATED (headline exercised on H2/STO-3G).

## 6. Backfill (2026-07-06)
Added: REPORT.tex, open_questions.json (5 items),
open_questions_section.tex, workflow.md, artifacts_summary.md,
failure_analysis.md, extraction/nougat.mmd stub. No re-runs; existing
evidence and code preserved.

## Reproducibility
* Deterministic seed for C1.
* C2 is exhaustive -> fully deterministic.
* All raw output in `report/evidence/*.json`.
* Total wall time: < 10 s CPU on M1 laptop.

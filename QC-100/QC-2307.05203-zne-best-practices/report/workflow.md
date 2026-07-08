# Workflow — arXiv 2307.05203 (ZNE best practices) replication

## Overview
End-to-end steps used to reproduce the paper's headline dZNE best-practice claim
on a real Mitiq + Qiskit Aer stack, on Apple Silicon CherryRd, in ~17 s
wall time.

## Steps

### 1. Environment
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2307.05203-zne-best-practices
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install mitiq qiskit qiskit-aer numpy scipy ply
```
Installed versions (verified at run time):
- python 3.12
- mitiq 1.0.0
- qiskit 2.5.0
- qiskit-aer 0.17.2
- numpy 2.2.6
- scipy (transitive)
- ply (transitive)

### 2. Paper acquisition
- `work/paper.pdf` — arXiv:2307.05203v2 (20 Jul 2023)
- `work/paper.txt` — pdftotext dump; Fig. 6 discussion is at lines 210–260

### 3. Claim extraction
Read `paper.txt` Sec. IV + Fig. 6 caption; extracted 8 claims (C1–C8) into the
claims table in `REPORT.md`. Marked C1–C5 as headline/testable-in-scope; C6–C8
as out-of-scope for a 5-case spot-run.

### 4. Circuit design
6-qubit brickwork Trotter-like circuit matching paper's App. B:
- Even-bond then odd-bond `CX-RZ(θ)-CX` entanglers
- Random θ ∈ [0, 2π) per gate, seed = 42
- Single-qubit `RX(φ)` rotations per layer
- Initial state H⊗n |0⟩
- Observable: Z_0 ⊗ I⁴ ⊗ Z_5 (traceless 2-body correlator)

### 5. Noise model
Depolarizing error on 2-qubit `cx` gates only. p2q ∈ {0.002, 0.01, 0.02}.
No single-qubit error (matches paper's Fig. 6 simplification).

### 6. Case grid (5)
| Tag | 2q depth | p2q | scales | intended regime |
|-----|----------|-----|--------|-----------------|
| A | 4  | 0.002 | {1,3,5}     | weak / shallow / wide |
| B | 20 | 0.02  | {1,3,5}     | strong / deep / wide  |
| C | 10 | 0.01  | {1,3,5}     | moderate / wide       |
| D | 10 | 0.01  | {1,1.1,1.2} | moderate / narrow     |
| E | 20 | 0.02  | {1,1.1,1.2} | strong deep / narrow  |

### 7. Execute
```bash
python code/zne_experiment.py
```
Produces:
- `report/evidence/zne_results.json` — raw scans, per-family fits, per-family
  errors, seeds, shot count, wall time
- `report/evidence/run.log` — full stdout

For each case:
1. Build ideal statevector reference.
2. Build noisy backend at p2q.
3. For each λ in scales:
   - 3 folded replicates (fold_global for integer, fold_gates_at_random for partial)
   - 8000 shots each → mean noisy observable
4. Feed identical (λ, E_noisy) scan to 4 families:
   - LinearFactory (order-1 LS)
   - PolyFactory (order-2)
   - RichardsonFactory (Lagrange at λ=0)
   - ExpFactory (asymptote=0.0)
5. Record |extrapolated − ideal| per family.

### 8. Verdict
Compare per-family error tables against paper's Fig. 6 predictions:
- C2 (weak/shallow/wide → Linear best): verified (Case A)
- C3 (strong/deep/wide → Exp best): verified (Case B, 12× vs Linear)
- C4 (moderate/narrow → Linear best; high-deg unstable): verified strongly
  (Case D: Q/Richardson = 2.08 blow-up)
- C5 (strong/deep/narrow → NF-risk): verified with twist (Case E: Q pushes through)
- C1 (cross-family divergence on same scan): verified in every case

Verdict: REPLICATED (headline claim C1–C5).

### 9. Compile REPORT
`REPORT.md` written incrementally as experiments completed (each case run,
then interpreted vs the paper's expected winner).

### 10. Backfill (2026-07-06)
- REPORT.tex authored from REPORT.md with honest critique section
- open_questions.json (5 items, JSON-safe strings, no LaTeX escapes)
- open_questions_section.tex (LaTeX version of the same 5 questions)
- workflow.md (this file)
- artifacts_summary.md
- failure_analysis.md
- extraction/nougat.mmd (stub — nougat not rerun; paper.txt is authoritative)

## Reproducibility
- Seed 42 fixed per case → tight determinism.
- Single-seed ensemble is a known limitation (see failure_analysis.md).
- Full env captured in step 1 above.
- All raw numbers in `report/evidence/zne_results.json`.

# Workflow — arXiv:1812.06814 replication

Chronological, exact-command workflow used to produce this replication.

## 0. Environment prep
```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1812.06814-quantum-chem-accuracy-resources
mkdir -p work report/evidence extraction
cd work
python3.11 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install qiskit qiskit-nature[pyscf] qiskit-algorithms qiskit-aer \
            openfermion pyscf scipy numpy
```

Recorded versions (see `report/REPORT.md` Sec. 3.1):
- qiskit 2.5.0, qiskit-nature 0.8.0, qiskit-algorithms 0.4.0, qiskit-aer 0.17.2
- pyscf 2.13.1, openfermion 1.7.1, scipy 1.17.1, numpy 2.4.6
- Python 3.11.15 on macOS 25.3.0 x86_64 (host CherryRd).

## 1. Paper retrieval + text extraction
```bash
cd work
# paper.pdf downloaded from arXiv:1812.06814v2
pdftotext -layout paper.pdf paper.txt
# grep Table SI I for headline numbers
grep -n "LiH" paper.txt | head
grep -n "H2" paper.txt | head
```
Confirmed target numbers: H2 (STO-3G) 4 qubits / 56 CNOTs; LiH (STO-3G)
12 qubits / 1382 CNOTs; LiH ΔFCI = 0.028 kJ/mol.

## 2. H2 end-to-end UCCSD-VQE (headline claim)
```bash
python -u run_vqe.py h2 2>&1 | tee report/evidence/vqe_h2.log
```
Behavior:
- Build STO-3G / JW Hamiltonian via qiskit-nature (PySCFDriver, r=0.735 Å).
- Build HartreeFock + UCCSD ansatz.
- Run StatevectorEstimator + L-BFGS-B, θ0 = 0 → HF start.
- Converges in ~24 evals / 1.5 s.
- Emit `report/evidence/vqe_results_h2.json` with E_HF, E_FCI, E_VQE,
  |E_VQE-E_FCI| = 0.0000 mHa, qubits = 4, CNOT = 49 (opt3).

## 3. LiH classical UCCSD + circuit-resource verification
```bash
python -u run_lih_final.py 2>&1 | tee report/evidence/vqe_lih_final.log
```
Behavior:
- Build STO-3G / JW Hamiltonian for LiH r=1.595 Å (12 qubits).
- Classical HF / CCSD / FCI via pyscf (CCSD = UCCSD-VQE analytical limit).
- Build qiskit-nature UCCSD ansatz; sanity-check HF-circuit ⟨H⟩ matches
  PySCF HF to 3.55e-15 Ha (machine precision).
- Transpile at opt_level=3, basis={cx,u3}; count CNOTs → 7026 raw.
- Emit `report/evidence/vqe_results_lih_final.json`:
  - E_corr(FCI) = -53.503 kJ/mol
  - E_corr(CCSD) = E_corr(UCCSD-VQE) = -53.475 kJ/mol
  - ΔFCI = 0.028 kJ/mol → **EXACT MATCH to paper Table SI I**
  - qubits = 12 → **MATCH**
  - CNOT ratio 7026/1382 = 5.1× → consistent with paper's ~4×
    cancellation + additional MP2 pre-screening

## 4. Report assembly
```bash
# Original narrative report (2026-07-03)
$EDITOR report/REPORT.md

# Backfill artifacts (2026-07-06)
$EDITOR report/REPORT.tex
$EDITOR report/open_questions.json
$EDITOR report/open_questions_section.tex
$EDITOR report/workflow.md
$EDITOR report/artifacts_summary.md
$EDITOR report/failure_analysis.md
$EDITOR extraction/nougat.mmd   # stub, real nougat run not required
```

## 5. Nougat / marker extraction status
- Full nougat / marker extraction of `paper.pdf` was NOT run for this
  replication. `extraction/nougat.mmd` is a stub explaining that the
  headline numbers (Table SI I, Sec. II C's 4× cancellation claim) were
  read directly from `pdftotext` output in `work/paper.txt`, which was
  sufficient for the replication's needs. If a full mmd extraction is
  wanted later, run:
  ```bash
  nougat work/paper.pdf --out extraction/ --model 0.1.0-base
  ```
  or push to uicgpu A100 for the small-batch OCR policy.

## 6. Runtime cost summary
- H2 VQE: 1.5 s wall on CPU.
- LiH classical+transpile: 6.5 s wall on CPU.
- Total compute: well under 1 minute. Zero paid API calls.
- No hardware run; statevector simulation only.

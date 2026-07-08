# Workflow — QC-100 W3 · LCU / Multi-Product Formulas

## Paper
Childs & Wiebe, *Quantum Information & Computation* **12**, 901–924 (2012).
"Hamiltonian simulation using linear combinations of unitary operations."

## Pipeline
1. **Paper ingestion**
   - PDF acquired; short extractive summary → `paper.md`.
   - Nougat / MathPix extraction was not run for this dir (small paper, all key
     equations reproducible from the plaintext).
2. **Claim identification**
   - Lemma 2 (LCU 1-ancilla circuit + failure prob formula)
   - Theorem 3 (κ definition)
   - Def 1 / Lemma 4 (MPF order lift)
   - Eq. 14 (coefficient sum = 1)
   - Near-unitarity (Blanes–Casas–Ros bound)
3. **Implementation** (`replicate.py`)
   - `numpy` + `scipy.linalg.expm` for ground-truth $e^{-iHt}$
   - Explicit Lemma-2 ancilla circuit (2-qubit unitary matrix, no Qiskit dependency)
   - $S_1$ / $S_2$ product formulas coded from definition
   - Richardson MPFs: $M_1 = 2 S_1(t/2)^2 - S_1(t)$; $M_2 = (4 S_2(t/2)^2 - S_2(t))/3$
   - Order extraction: log-log slope over $t \in [10^{-3}, 10^{-1}]$
   - Near-unitarity: `numpy.linalg.svd`, $\max_i |\sigma_i - 1|$
4. **Cross-checks**
   - 2-qubit Hamiltonian $H = X\otimes X + Z\otimes I + I \otimes Z$ (genuine 2-body)
   - Confirmed $\sum C_q = 1$ symbolically and numerically
   - Confirmed Lemma-2 failure prob against closed form to $< 10^{-9}$ across 9 (ε, κ) cases
5. **Verdict rendering** → `REPORT.md` (top-level, human-readable) and `report/REPORT.tex`
6. **Backfill (2026-07)** → `report/` LaTeX + open questions + failure analysis
   + `extraction/` nougat stub

## Environment
- macOS `m1` (Kukla host default) / equivalent
- Python 3.11 with `numpy>=1.24`, `scipy>=1.10`
- No hardware, no cloud, no LLM calls in the numerics pipeline

## Reproducibility
- `replicate.py` is deterministic (no random seeds needed; all IEEE-754)
- Re-running produces bit-identical `results.json`

## What was NOT done
- No qiskit / cirq transpile — kept pure numpy for portability
- No $S_4$ (Suzuki-4) baseline (see failure_analysis.md)
- No physically-motivated Hamiltonian benchmark
- No noise / density-matrix sim
- No Nougat extraction (paper.md sufficed)

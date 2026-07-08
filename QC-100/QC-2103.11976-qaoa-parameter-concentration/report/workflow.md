# Workflow — arXiv:2103.11976 (QAOA Parameter Concentration)

End-to-end replication pipeline. CPU-only, seconds per run. Free endpoints only.

## Stage 0: Provenance
- `work/paper.pdf` — arXiv:2103.11976v1 (fetched via arxiv.org).
- `work/paper.txt` — `pdftotext` output.
- Extracted: H_z, H_x, ansatz, eq.5 (F1), eq.13 (F2), asymptotics eqs.9,10,15-18, concentration eq.11.

## Stage 1: Environment
```bash
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
pip install qiskit qiskit-aer numpy scipy matplotlib
```
Locked versions: Qiskit 2.5.0, qiskit-aer 0.17.2, NumPy 2.4.3, SciPy 1.18.0, Python 3.13.

## Stage 2: Implementation
- `code/qaoa_state_prep.py`
  - `F1_analytical(gamma, beta, n)` — eq.5 in NumPy (no sampling).
  - `F2_analytical(g1, b1, g2, b2, n)` — eq.13 in NumPy.
  - `optimize_p1(n, n_seeds=32)` — L-BFGS-B on `-F1` from many seeds incl. paper asymptotics.
  - `optimize_p2(n, n_seeds=48)` — same for p=2.
  - `qiskit_crosscheck(n, gamma, beta)` — builds real QAOA state-prep circuit (H^n, Diagonal, RX(2b)) and returns Statevector overlap.
- `code/analyze.py`
  - Folds (beta -> pi-beta, gamma -> 2pi-gamma) branch symmetry to canonical small-beta window.
  - Fits beta = pi/(a1 n + a2) and gamma = b1 pi - b2 beta via `scipy.optimize.curve_fit`.
  - Computes Delta^2(n) = (g_{n+1}-g_n)^2 + (b_{n+1}-b_n)^2 and fits Delta^2 = C/n^l.

## Stage 3: Execution
```bash
python code/qaoa_state_prep.py     # p=1 sweep n=4..20, p=2 sweep n=4..15, Qiskit crosscheck n=4,6,8
python code/analyze.py             # folding, fits, power-law exponent
# extended:
python code/qaoa_state_prep.py --range 15 41   # large-n tail up to n=40
```
Wall-clock: ~60 s total on M2 CPU.

## Stage 4: Evidence collection
All numerical output persisted under `report/evidence/`:
- p1_sweep.{json,csv}, p2_sweep.{json,csv}, qiskit_crosscheck.{json,csv}
- p1_concentration.{json,csv}, p1_analysis.json, p1_concentration_fit.json, p1_large_n.json
- run.log, analyze.log, large_n.log

## Stage 5: Cross-check (independence signal)
The critical independence test: does the paper's *analytical* eq.5 equal the
overlap of a *real Qiskit statevector* circuit? Yes, to 10^-16. This
rules out the failure mode where a replication just re-evaluates the paper's
own formula and calls it done.

## Stage 6: Reporting
- `report/REPORT.md` — narrative (primary).
- `report/REPORT.tex` — LaTeX version for submission.
- `report/open_questions.json` + `report/open_questions_section.tex` — 5 truly-open follow-ups.
- `report/failure_analysis.md` — honest critique.
- `report/artifacts_summary.md` — inventory.
- `extraction/nougat.mmd` — retrieved-text stub (paper is a theory paper; canonical text in `work/paper.txt`).

## Stage 7: Verdict emission
Per QC-100 protocol:
```
WAVE_RESULT set=QC-100 paper=2103.11976 verdict=REPLICATED ...
```

## Reproducibility
- Fixed random seeds in optimizer (`np.random.seed(0)` for seed cloud).
- Deterministic `qiskit_aer.AerSimulator(method="statevector")`.
- Any host with Python 3.13 + the four packages above reproduces bit-for-bit.

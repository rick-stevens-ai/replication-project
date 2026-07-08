# Workflow — arXiv:1801.06121 Real Randomized Benchmarking

## Environment
- Host: local CPU box (m1 / cherryrd, free)
- Python venv: `.venv/`
- Packages: `qiskit==2.5.0`, `qiskit-aer==0.17.2`, `numpy`, `scipy`
- No paid endpoints. No GPU.

## Steps (exact)
1. **Acquire paper.**
   ```
   curl -sL https://arxiv.org/pdf/1801.06121 -o work/1801.06121.pdf
   pdftotext work/1801.06121.pdf work/1801.06121.txt
   ```
2. **Set up venv.**
   ```
   python3 -m venv .venv
   . .venv/bin/activate
   pip install --upgrade pip
   pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy matplotlib
   ```
3. **Enumerate groups (verify C1, C2).**
   `src/real_rb.py` contains `enumerate_group(generators)` that iterates
   matrix products, canonicalizes global phase, returns list of unique
   matrices. Called with `[Z, H]` and `[S, H]`.
4. **Build noise model.** `NoiseModel.add_all_qubit_quantum_error(
      pauli_error([('X', p/2), ('Z', p/2), ('I', 1-p)]), 'unitary')` with
   `p = 0.02`. Real-diagonal by construction (no Y).
5. **Run RB sweep.**
   ```
   python src/real_rb.py
   ```
   - lengths `m ∈ {1, 5, 10, 20, 40, 80, 150}`
   - `M = 30` sequences per length per protocol
   - `shots = 1024` per sequence
   - inverting element computed as `(∏ U_i)†` analytically
   - saves survival probabilities + fits to `report/evidence/results.json`
6. **Reduced-sequence real RB (C5).** Same script, second block runs
   real RB with `M = 10` (matches ratio 8/24).
7. **Analytic cross-check.**
   ```
   python src/theory_check.py > work/theory_check.log
   ```
   Computes closed-form predictions
   `f_pred = 1 − 4p/3`, `r_pred = (1-f_pred)(d-1)/d`,
   `b_pred = 1 − p`, `r_R = (1-b_pred)/2`.
8. **Plot curves.**
   ```
   python src/plot_rb.py    # -> report/evidence/rb_curves.png
   ```
9. **Wrap up report.** `report/REPORT.md` (source of truth),
   `report/REPORT.tex` (LaTeX version, this backfill),
   `report/evidence/results.json`, `report/evidence/rb_curves.png`.

## Reproduce end-to-end
```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1801.06121-real-randomized-benchmarking
python3 -m venv .venv && . .venv/bin/activate
pip install qiskit==2.5.0 qiskit-aer==0.17.2 numpy scipy matplotlib
python src/real_rb.py
python src/theory_check.py
python src/plot_rb.py
```

Expected outputs land in `report/evidence/`.

## Cost / provenance
- Compute: local CPU, order of minutes.
- No paid API calls; no external LLM used in the fitting or verification path.
- All source code + logs preserved under `src/` and `work/`.

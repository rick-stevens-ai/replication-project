# Workflow — arXiv:1901.06213 replication

## 1. Extraction
- `pdftotext -layout paper.pdf extraction/paper.txt` (644 lines; vision/pdf tool not needed).
- Read main text + Supplemental Material (SM A: Hamiltonian; SM B: multipole matrices; SM C: VC scaling).
- Notes distilled to `extraction/marker.md` (model params, operator matrices, U0Q table, targets, scope).

## 2. Claim selection (6 machine-checkable)
- C1 filling nf/ns; C2 RPA magnetic dominance + peak positions; C3 quadrupole smallness via U0Q;
  C4 Stoner factor alpha_mag ~0.9 at u=1.08; C5 AL/MT xi-scaling law; C6 (headline) full VC enhancement.

## 3. Implementation (`code/`, run under `work/`)
- `model.py` — 2D PAM: conduction dispersion (S1), s-f hybridization (S2), 6x6 Bloch Hamiltonian,
  all 16 Gamma8 multipole operators (S5/S6) in sigma(x)tau basis + S7 normalization.
  Self-test: all operators Hermitian, normalized, traceless (except identity).
- `filling.py` — C1: diagonalize on k-mesh, Fermi-occupy, project c/f character.
- `rpa.py` — bare bubble chi0_Q(q) (Lindhard form over Bloch bands, f-subspace embed);
  channel-diagonal RPA with reported diagonal U0Q (TABLE II).
- `qscan.py` — C2/C3: chi0 and chi^RPA along Gamma-X-M-Gamma for 8 magnetic + 5 electric channels;
  magnetic/quadrupole peak ratios; saves `qscan_paths.npz`, `qscan_summary.json`.
- `stoner.py` — C4: alpha_mag / alpha_el vs u.
- `al_scaling.py` — C5: Ornstein-Zernike momentum sums X_AL~xi^2 vs X_MT~log xi; continuum
  X_AL ∝ xi^{4-d} exponent fits for d=1,2,3.
- `plots.py` — figures: bands+FS, q-scan (bare vs RPA), AL/MT scaling.

## 4. Runs (all real, no fabrication)
- `python3 filling.py`            -> nf~0.99, ns~0.19 (partition mismatch, total within 7%).
- `python3 qscan.py 40 1.08`      -> chi^RPA_Jz / chi^RPA_Oxy = 39.7 (bare ratio 1.03).
- `python3 stoner.py 40`          -> alpha_mag=1.02, alpha_el=0.62 at u=1.08 (paper 0.9).
- `python3 al_scaling.py`         -> AL/MT ratio 0.74->123 (xi 2->64); continuum exponents 2.96/1.97/1.00.
- `python3 plots.py`              -> fig_bands.png, fig_qscan.png, fig_scaling.png.

## 5. Reporting (`report/`)
- REPORT.tex -> REPORT.pdf (pdflatex x2, 5 pages).
- open_questions.json (exactly 5), workflow.md, artifacts_summary.md, failure_analysis.md.
- Summary JSONs + figures copied from work/ into report/.

## Reproduce
```
cd work && cp ../code/*.py .
python3 qscan.py 40 1.08 && python3 stoner.py 40 && python3 al_scaling.py && python3 plots.py
cd ../report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
Runtime: qscan ~100s, stoner ~100s, al_scaling <5s, plots ~20s (single core, numpy).

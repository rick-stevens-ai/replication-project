# Workflow — arXiv:2510.05234 replication

## 1. Ingest
- `pdftotext -layout paper.pdf paper.txt` (poppler 25.x). PDF text layer clean, not
  credit-blocked. Transcribed Eqs. (1),(4),(9),(11),(12) and Figs. 4/5 constants
  (eps=0.12, s1=-1.62, s2=0.5, Delta=0.2) by hand into `extraction/marker.md`.

## 2. Kernel triage (provenance)
- Read shared `loop_current_kagome_kernel.py` (Fernandes 2502.16657). It is a 3x3 NN
  kagome + Peierls-flux + FHS-Chern + bond-current tool. Same CLASS as this paper
  (kagome, loop-current, CBO/LCO) but NOT the same model: Friedlan-Kee's object is a
  6x6 effective PATCH Hamiltonian (two vHS per M point) with complex 3Q bond order.
- Decision: reuse kernel's hexagonal-BZ geometry conventions + Re/Im bond-operator
  classification philosophy; build the 6x6 H(k) from scratch. Provenance cited in
  `code/patch_model.py` docstring and PROVENANCE below.

## 3. Code
- `code/patch_model.py` — 6x6 H(k) (Eq. 4), k_alpha (Eq. 1), analytic eigenvalues
  (Eq. 9), inverse-energy factors (Eq. 12), second-order-in-lambda corrections
  (Eq. 11), per-axis band-correction dispersion, order-config classifier.
- `code/run_checks.py` — runs C1-C5, writes `work/results.json` + `work/run.log`.

## 4. Run
```
cd code && python3 run_checks.py
```
- Pure numpy, runs in <2 s. No network, no external endpoints.

## 5. Claims chosen (machine-checkable)
- C1 numeric==analytic spectrum + degeneracy at Phi=0,pi (Fig. 4)
- C2 Phi/TRSB/nematic classification of orders (Sec. II)
- C3 sign of inverse-energy factors at Delta=0.2 (Fig. 5)
- C4 full-fill LCBO+ lowest + NLCBO anomalous k_x dispersion (Sec. III B)
- C5 lambda required (Phi=pi degeneracy at lambda=0)

## 6. Compare
- C1: max|num-ana| ~ 2.5e-16 (machine precision).
- C3: 1/DE1=+3.85>0, 1/DE2=-4.39<0 at Delta=0.2 (paper: Fig. 5 sign structure).
- C4: full-fill ordering LCBO+ < NLCBO < CBO- (paper: LCBO+ lowest when full);
  k_x-edge correction NLCBO=-0.071 most negative (paper: anomalous k_x dispersion).
- C5: internal-E spread 0 at lambda=0, 0.04 at lambda=0.35.

## 7. Report
- `report/REPORT.tex` (+ compiled PDF if pdflatex available), open_questions.json
  (5), artifacts_summary.md, failure_analysis.md, this workflow.md.

## Reproduce from scratch
```
cd ~/Dropbox/REPLICATE-PROJECT/TEXTURE-loop-current-friedlan2025
pdftotext -layout paper.pdf paper.txt   # if paper.txt missing
cd code && python3 run_checks.py         # -> ../work/results.json
cd ../report && pdflatex REPORT.tex      # optional PDF
```

## PROVENANCE
Adapted from `~/Dropbox/XFER/TEXTURES-100/shared-kernels/loop_current_kagome_kernel.py`
(Ollie/kernel author, Fernandes et al. arXiv:2502.16657). Reused: BZ geometry,
reciprocal/M-point conventions, Re/Im bond-operator (charge vs loop-current) logic.
New in this replication: the full 6x6 effective patch Hamiltonian and all Eq.
(4/9/11/12) machinery, which are specific to Friedlan-Kee arXiv:2510.05234.

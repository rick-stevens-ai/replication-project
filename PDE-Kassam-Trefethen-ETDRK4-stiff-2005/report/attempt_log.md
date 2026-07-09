# Attempt Log — ETDRK4 replication

## 2026-07-02 (initial draft, prior wave)
- Wrote `work/etdrk4_core.py` (contour + direct coefficients, ETDRK4 step),
  `work/pdes.py` (KS, Burgers, Allen–Cahn, KdV setups),
  `work/integrators.py` (ETDRK4 & IFRK4 loops).
- Wrote run scripts: cancellation, convergence, KdV self-convergence, KdV soliton.
- Trap encountered: an initial *half-circle* contour version silently reduced
  ETDRK4 to first order on KdV (imaginary spectrum) because taking `real()`
  discarded the genuinely complex coefficient. Fixed by using the FULL circle
  and keeping coefficients complex (documented in `etdrk4_core.py`).
- Draft REPORT.md written; Argo LLM judge scored coverage=8 agreement=8 STRONG
  but with no on-disk numerical evidence beyond the report tables.

## 2026-07-04 (promotion pass — this run)
- Re-ran all four experiments end-to-end on fresh interpreter; captured logs
  under `report/evidence/*.log`. Numbers reproduce the report tables exactly:
  * f1 direct vs contour max rel err (|hL|<0.5): 2.235e-06 vs 3.055e-15,
    worst-case ratio 7.31e+08.
  * KS ETDRK4 fitted order 3.80, IFRK4 3.60, ETDRK4/IFRK4 acc. ratio 5.03x.
  * Burgers 3.88 / 3.95, 1.40x.
  * Allen–Cahn 4.05 / 4.03, 4.64x.
  * KdV self-convergence: ETDRK4 log2-ratios 4.09, 3.85 pre-floor (drops on
    finest steps where spatial spectral floor dominates — expected).
  * KdV soliton max|u−u_exact|=3.28e-9; mass drift 2.8e-16; ∫u² drift 4.5e-14.
- Added three figures (Kassam & Trefethen Figs. 2/3/4 shape reproductions):
  * `report/evidence/cancellation.png`  (Fig. 2 shape)
  * `report/evidence/convergence.png`   (Fig. 3 shape, all four PDEs)
  * `report/evidence/ks_spacetime.png`  (Fig. 4 shape — KS to T=150)
  * JSON payloads next to each figure for exact numbers.
- KS long-run diagnostics: finite, umax=3.37, mean drift 4.4e-17 → textbook
  bounded chaotic KS solution, as reported in the paper.
- Ran a second LLM judge (Argo GPT-5.5) on the updated report/evidence bundle.

## Deliberate scope cuts (not attempted)
- Krogstad ETDRK4-B and other ETD/IF variants (secondary in the paper).
- Chebyshev / non-periodic (Cheb) formulation for Allen–Cahn (paper compares
  Cheb; we used the periodic Fourier variant — same 4th-order behaviour).
- Two-soliton stiff KdV amplitude A=25 (needs dealiasing + tiny steps; the
  single-soliton exact solution gave a cleaner quantitative verdict).

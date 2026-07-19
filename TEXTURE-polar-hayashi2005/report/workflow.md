# Workflow — Hayashi et al. 2005 vortex-in-NCS replication

## Paper
Hayashi, Kato, Frigeri, Wakabayashi, Sigrist, arXiv:cond-mat/0510548,
"Basic properties of a vortex in a noncentrosymmetric superconductor" (CePt3Si-type).
Theory / quasiclassical (Eilenberger) numerics. CPU-only.

## Steps executed
1. **Extraction (given):** `extraction/marker.md` (pdftotext) + `report/method_extract.md`.
   Read the marker to pull the *exact* equations: gap structure
   `Delta_{I,II} = Psi ± Delta sin(theta)` with `|Delta|>|Psi|`; LDOS
   `N = (N0/2) Re<g_I+g_II>` (Eq.4); current `j ~ (g_I+g_II)` (Eq.5);
   magnetization `M_x,M_y ~ (∓k~_y,k~_x)(g_I-g_II)`, `M_z=0` (Eqs.7-9).
2. **Solver (`code/hayashi2005_replication.py`):**
   - Riccati parametrization of the two decoupled Eilenberger equations (paper Eq.1),
     one per Rashba-split sheet. RK4 fixed-step, one-sided integration
     (a forward, b backward) seeded by bulk values — unconditionally stable.
   - Green functions `g=(1-ab)/(1+ab)`, `f=2a/(1+ab)`.
   - Reduced vortex profile `Psi(r)=Psi tanh(r/xi0)`, `Delta(r)=Delta tanh(r/xi0)`
     (same core radius by construction, matching the paper's finding), single phase
     winding `e^{i phi_r}`. Sheet II gap changes sign at its nodes (retained).
   - Fermi-surface angular average over theta (weight sin theta); trajectory
     average over impact parameters; radial binning to r in [0,6] xi0.
   - Real-energy pass -> LDOS map N(E,r) (both sheets); Matsubara pass ->
     supercurrent (g_I+g_II) and magnetization (g_I-g_II) + per-sheet.
   - **Control:** rerun with Delta=0 so the sheets are identical -> M must vanish.
3. **Run:** ~165 s, CPU-only. Incremental logging to `work/run.log`; results to
   `work/results.json`; arrays to `work/arrays.npz`.
4. **Figures (`figs/`):** fig1 pair potentials (same core radius); fig2 LDOS
   (map + zero-bias core peak + core-vs-far two-gap); fig3 magnetization texture
   + control + supercurrent + per-sheet.
5. **Report:** `report/REPORT.tex` -> `REPORT.pdf` (pdflatex x2, 5 pages).
6. **Artifacts:** open_questions.json, workflow.md, artifacts_summary.md,
   failure_analysis.md; META.json updated with status + honest verdict.

## Key modeling decisions
- Followed the paper's **exact** g_I±g_II decomposition: current = sum, magnetization
  = difference. This is the physically correct, checkable structure.
- `|Delta|>|Psi|` chosen (Psi=0.5, Delta=1.0) so sheet I is fully gapped and sheet II
  has line nodes — reproducing the two-gap bulk DOS.
- Fixed (non-self-consistent) profile => graded PARTIAL, stated honestly.

## Reproduce
```
cd TEXTURE-polar-hayashi2005
python3 code/hayashi2005_replication.py   # ~165 s, writes work/ + figs/
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```

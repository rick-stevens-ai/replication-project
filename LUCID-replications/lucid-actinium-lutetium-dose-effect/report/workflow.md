# Workflow — Ruigrok et al. 2022 replication

## Data sources used
- **paper.pdf** — Open Access (CC-BY) PDF of Ruigrok et al. 2022, EJNMMI 49:3627–3638.
- **paper.txt** — `pdftotext -layout paper.pdf paper.txt` for numeric extraction.
- **Figure 3A / 3C** — two independent manual digitization passes recorded in
  `code/replicate_lucid.py` as `AC_SURV_READ1`, `AC_SURV_READ2`,
  `LU_SURV_READ1`, `LU_SURV_READ2`.
- **Table 2** — S-values (self-dose and cross-dose) taken verbatim; no MC re-derivation.
- **Table 3** — per-cell absorbed doses (average cellular-dimension column)
  taken verbatim as the input dose grid for the survival fit.

## Steps

### Initial pass (2026-05-30, Ollie)
1. Fetched paper PDF locally.
2. Digitized Fig. 3A (Ac-225) and Fig. 3C (Lu-177) survival panels — two reads each.
3. Fit `S(D) = exp(-α D)` in survival-fraction space via
   `scipy.optimize.curve_fit` to Table 3 doses + digitized survivals,
   excluding the top-concentration points that the paper itself excluded.
4. Recovered α values per isotope per read; computed RBE = α(Ac)/α(Lu).
5. Reimplemented MIRD chain `D = Σ Ã · S` with:
   - biexponential biological washout, `t_bio=2.3 h, F=0.41`,
   - physical half-life for the isotope,
   - `S_eff = 0.76·S_cyt + 0.24·S_mem` from Table 2 average-dim entries,
   - `A₀ = uptake_fraction · concentration · 1.5 mL / n_cells`.
6. Compared recomputed doses to Table 3; observed constant multiplicative
   offset (Lu 1.28×; Ac 2.4×).

### Re-pass 2026-06-23 (12 additional claims C7–C19)
7. Extracted `paper.txt` via `pdftotext -layout` as canonical text source
   (canonical Marker MD not present on uicgpu for this DOI as of 2026-06-23).
8. For each of C7, C8, C9, C10, C11, C12, C13, C14, C15, C16, C17, C19:
   - Wrote a self-contained script `code/cN_<slug>.py`.
   - Emitted `results/cN_<slug>.json` with claim / paper-value /
     replicated-value / status.
9. Statistical checks: Welch's t-test for C7 (uptake equivalence) and
   C9 (foci peak); TOST equivalence bounds ±30% for C7.
10. Physics-consistency checks for C12 (S-value ratios) and C14
    (cross-dose S-value bracket).
11. Model-consistency checks for C11 (biexponential reconstruction) and
    C15 (blocking → baseline survival).
12. Updated verdict from SPOT-CHECK → PARTIAL with Coverage 8/10,
    Agreement 8/10 on 2026-06-25.

### Backfill 2026-07-06 (this pass)
13. Read top-level `REPORT.md` once for context.
14. Wrote `report/REPORT.tex` (LaTeX synthesis with honest Critique).
15. Wrote `report/open_questions.json` (bare JSON list, 5 entries).
16. Wrote `report/open_questions_section.tex` (LaTeX include for REPORT.tex).
17. Wrote `report/workflow.md`, `report/artifacts_summary.md`,
    `report/failure_analysis.md`, `extraction/nougat.mmd` stub.

## Tools used
- **pdftotext -layout** (poppler-utils) — text extraction.
- **Manual digitization** — Fig. 3A/3C (two independent reads per panel).
- **Python 3 + scipy** — `scipy.optimize.curve_fit` for α fits;
  `scipy.stats.ttest_ind` for Welch's test.
- **NNDC / paper text** — physical constants (Lu-177 T½ = 6.647 d;
  Ac-225 T½ = 9.92 d).

## Explicit non-steps
- No Geant4 / TOPAS-nBio Monte Carlo re-derivation of Table 2 S-values.
- No wet-lab experiments (clonogenic, IF, IC₅₀, uptake, excretion).
- No MIRDcell cross-dose averaging over cell-dimension distribution
  (used cross-dose S-value verbatim for C14 only).
- No alpha-track microdosimetry / stochastic energy-deposition modeling.
- No re-derivation of Lu-177 β spectrum or Ac-225 alpha-daughter chain
  energetics.

## Reproducibility
```
cd /Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-actinium-lutetium-dose-effect/
python3 code/replicate_lucid.py                 # central α/RBE/MIRD pipeline
python3 code/c7_uptake_equivalence.py           # + one per claim C7…C19
# … etc for c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c19
```

## Endpoint hygiene
All computation local (m1 / CherryRd). No paid API calls. No proprietary
data touched. Paper is Open Access CC-BY; digitized figure values are
transformations of that OA content and are shared under the same license.

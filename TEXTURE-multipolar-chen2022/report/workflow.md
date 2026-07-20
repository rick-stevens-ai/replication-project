# Workflow — Chen 2022 pyrochlore AF* replication

## 1. Read & recipe
- Loaded `report/evidence/replication_recipe.json` (method=mean-field, gauge MFT).
- Read paper text `work/textures-multipolar-chen2022.txt`: extracted the minimal model
  `Ha` (Eq. 3), spinon-gauge construction (Eqs. 4-13), spinon dispersion (Eq. 16),
  phase table (Table I), and the headline AF* stabilization claim.

## 2. From-scratch physics build
- File: `work/chen2022_gmft.py` (numpy only; runner `/home/stevens/comfyui-env/bin/python`).
- Built diamond-lattice geometry: 4 NN vectors `e_mu`, 12 second-neighbor vectors `a_n`.
- Implemented bosonic-spinon rotor gMFT:
  - dispersion `w_pm(k) = sqrt(2 Jx (lambda - t1 sum cos(k.a_n) ± t2 |sum e^{ik.e_mu}|))`;
  - self-consistent Lagrange multiplier `lambda` from T=0 rotor-density constraint (bisection);
  - deconfinement test via spinon gap; condensation flag when constraint forces gap closure.
- Scanned inter-sublattice hop `t2` (proxy for J2xz crossing term / AAO amplitude) on 20^3 grid.

## 3. SAVE-EARLY
- Wrote `work/chen2022_result.json` immediately after first successful run.

## 4. Compare & score
- AF* point (t1=0.025, t2=0.02): gapped deconfined spinons + gapless photon + AAO Sz proxy.
- Phase sequence recovered: U(1) QSL (t2=0) → AF* (0<t2<~0.07) → fragmented AFM (condensed).
- Boundary via spinon condensation ↔ paper's continuous Anderson-Higgs transition.

## 5. Package (8 artifacts)
- extraction/marker.md, extraction/nougat.mmd (pdftotext interim + header)
- report/REPORT.tex, report/open_questions.json, report/workflow.md,
  report/artifacts_summary.md, report/failure_analysis.md
- Copied result JSON + code to report/evidence/.

## Tools
- `pdftotext` (poppler) for born-digital text extraction.
- numpy gMFT solver; shared kernel credited for geometry/utility patterns.

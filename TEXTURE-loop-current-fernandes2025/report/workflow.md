# Workflow — replication of arXiv:2502.16657

## 0. Environment
- Host: CherryRd (macOS). Python 3.13, numpy 2.4.3, scipy 1.18.0, matplotlib.
- LaTeX: TeX Live 2026 (`pdflatex`).
- No paid endpoints used. PDF text via `pdftotext -layout` (Poppler). Vision/PDF
  model calls were credit-blocked and NOT needed — text extraction was clean and
  all verification is numeric.

## 1. Ingest the paper
```
pdftotext -layout paper.pdf work/paper.txt      # 586 lines, clean
```
Read the full text. Established that this is a **perspective/review** article
(no new numerical tables). Identified the checkable physics: kagome NN
tight-binding facts (Fig. 3a / Eq. 1), the Peierls-flux LC mechanism (Box 1
Eq. 5), the LC-vs-CDW real/imaginary bond operator (Box 2 Eq. 6), the Table I
multipole classification, and the patch-model channel rule (Box 2).
Recorded in `extraction/marker.md`.

## 2. Select machine-checkable claims
CL1 (band/vHS/DOS), CL2 (Peierls flux -> TRS breaking + gap), CL3 (imaginary
loop-current order parameter), CL3-net (Table I dipole/octupole), CL4
(quantized AHE / Chern), CL5 (patch channel logic). See `artifacts_summary.md`.

## 3. Build the reusable kernel  `code/kagome_loopcurrent.py`
- 3x3 kagome Bloch Hamiltonian, closed form `-2t cos(k.a_i/2)` + Peierls phases.
- Methods: `bands`, `dos` (vectorized), `chern_number` (Fukui-Hatsugai-Suzuki),
  `gap`, `bond_current_and_charge` (Box 1), `plaquette_fluxes`,
  `triangle_flux_from_config` (Table I), `patch_leading_channel` (Box 2).
- **Geometry debugging** (see failure_analysis.md): the first bond-vector
  assignment gave a wrong spectrum; fixed by using the textbook half-bond
  closed form, verified against known kagome facts (flat band +2t, Dirac -t,
  M-saddle 0).
- **Flux pattern debugging**: the "staggered" (+f/-f) pattern does NOT gap the
  lower bands (Chern non-convergent). The correct Chern insulator is the
  "uniform" directed flux (Ohgushi-Murakami-Nagaosa). Documented; `uniform` is
  the recommended LC-Chern pattern in the kernel docstring.

## 4. Run the replication  `code/run_replication.py`
```
python3 code/run_replication.py
```
Produces `work/results.json` plus figures `work/fig_bands.png`,
`work/fig_dos.png`, `work/fig_bands_flux.png`. Runtime ~1-2 min (DOS eta scan
is the slowest part).

## 5. Verify each claim
- CL1: high-sym energies exact; flat band to 1e-6; Dirac gap ~1e-15; DOS peak
  linear in ln(1/eta) with R^2=0.9999 (log divergence).
- CL2: TRS residual 0 (plain) vs 6.65 (flux); gap 0 -> 1.61 t.
- CL3: Im part -0.013 (plain) vs -0.084 (flux).
- CL3-net: 3Q=FM, 2Q-1Q=AFM, 2Q-3Q=ferro-octupolar (all match Table I).
- CL4: Chern (+1,0,-1), converged over grids 30-90; lower band C=+1.
- CL5: iCDW selected for g1<0,g2>0,g3>0.

## 6. Report
- `report/REPORT.tex` -> `pdflatex x2` -> `report/REPORT.pdf` (4 pages, figures embedded).
- `report/open_questions.json` (exactly 5), `report/artifacts_summary.md`,
  `report/failure_analysis.md`, this `workflow.md`.

## Reproduce from scratch
```
cd TEXTURE-loop-current-fernandes2025
python3 code/run_replication.py
cd report && pdflatex -interaction=nonstopmode REPORT.tex && pdflatex -interaction=nonstopmode REPORT.tex
```

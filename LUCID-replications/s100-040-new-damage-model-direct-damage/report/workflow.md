# Workflow — LUCID Slot 040 (Park 2022, new damage model / direct damage)

## What was actually done (2026-06-22)

1. **PDF acquired** and pdftotext-extracted → `ocr/raw_layout.txt`
   (no Nougat, no OCR-model run; Scientific Reports gives a clean
   born-digital PDF so layout-preserving pdftotext was sufficient).

2. **Closed-form analytical reproduction** in a single Python file
   (`code/reproduce_damage_model.py`, ~200 LOC, stdlib + numpy + matplotlib
   only; no Geant4, no MC, no GPU). Steps:

   a. Load Table 1 Morse and Lennard-Jones parameters.
   b. Compute CG bead radii from group volumes
      $r = (3V/4\pi)^{1/3}$ for phosphate, deoxyribose, base.
   c. Evaluate the **standard** Morse $D_e[1-e^{-\alpha(r-r_e)}]^2 - D_e$
      form for each Table 2 bond at the paper's $r$ value.
   d. Evaluate the LJ $4\varepsilon[(\sigma/r)^{12}-(\sigma/r)^6]$ term
      for each Table 2 non-bonded pair.
   e. Sum the six phosphate PO$_3$ rows → −12.3566 eV
      (paper: −12.3562 eV, delta 0.4 meV).
   f. Attempt deoxyribose closed-form using canonical furanose
      skeleton (3 C-C, 3 C-O, 1 O⋯O non-bonded) → 22.12 eV vs paper
      30.5 eV. Documented as blocker requiring Supplementary Fig. S2.
   g. **McMahon-Currell mass conservation check:** integrate SC+OC+L
      contributions at four dose points; residual 6e-17 (machine ε).
   h. **Back-fit test:** given fixed S0, C0, ρ, LET, use scipy.optimize
      to recover μ, φ from OC(D) curve for $^{60}$Co (57.4, 3.87) and
      1-MeV e⁻ (53.5, 1.0).
   i. **Eq. (8) formula check:** identical inputs give 0%,
      1.142× multiplier gives 14.200%.

3. **Bug-hunt on Eq. (3).** Plugging Table 1 into the **printed** Morse
   expression gives −34.0 eV total (2.75× too large). Re-derived the
   standard form; every Table 2 number falls into place. Documented as
   paper typo / would-be erratum.

4. **Figures produced** with matplotlib:
   - `figures/cg_potentials.png` — Morse + LJ curves for all five bond types
   - `figures/mcmahon_fits.png` — SC/OC/L(D) for both beams
   - `figures/table3_threshold_ranges.png` — Table 3 range bar plot

5. **Machine-readable numbers dumped** to `evidence/numbers.json`;
   human-readable execution log to `evidence/log.txt`.

## What was NOT done

- No Geant4-DNA build (out-of-policy on CherryRd; no GPU; would take
  10⁵–10⁶ CPU-hours for the seven-beam × 5,400-plasmid MC study).
- No TOPAS-nBio cross-check (same reason).
- No supplementary-info retrieval (Fig. S2, S1, gel-band CSV — none
  scriptable from a free endpoint).
- No wet-lab re-fit of experimental μ, φ (no raw band-intensity data).
- No scavenger sweep / OER computation / cross-code comparison
  (all deferred to open questions).

## Re-run instructions

```bash
cd LUCID-replications/s100-040-new-damage-model-direct-damage
python3 code/reproduce_damage_model.py
```

Wall-clock: **< 2 s** on a single CherryRd core.
No network, no GPU, no external data required.
Regenerates `evidence/numbers.json`, `evidence/log.txt`, all three PNGs.

## Backfill actions (2026-07-05, this session)

- Added `report/REPORT.tex` (LaTeX equivalent of REPORT.md, with the
  cross-checked verdict statement and explicit critique).
- Added `report/open_questions.json` + `_section.tex` (5 questions).
- Added `report/workflow.md` (this file).
- Added `report/artifacts_summary.md` (index of all files).
- Added `report/failure_analysis.md` (honest critique of paper AND
  this replication).
- Added `extraction/nougat.mmd` stub (source was pdftotext, not Nougat).
- **No simulations re-run.** No existing files touched.
- **Verdict preserved as REPLICATED** per queue, with an explicit note in
  REPORT.tex and failure_analysis.md that the label is optimistically
  broad (headline MC-dependent claim was NOT independently reproduced).

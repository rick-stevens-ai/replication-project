# PARSER_PROVENANCE — Fukui-Saga LQ+SLDR+ALDH replication re-pass

Records which text/figure extractions were used in pass-1 vs the re-pass.

## Pass 1 (2026-05-30)
- **Parser:** `pdftotext -layout` (poppler) + ad-hoc vision-model digitization of Fig 5 / Fig 6.
- **Source PDF:** `data/source-paper.pdf`
- **Source PDF md5:** `acbb80ecc6f5bfe135a0081aa2be4c9b`
- **Text extract:** `data/source-paper.txt` (pdftotext)
- **Page rasters:** `data/pages/p-*.png`

## Re-pass (2026-06-23)
- **Parser:** Marker (uicgpu run 2026-06-22), full-paper canonical Markdown + per-figure JPEGs.
- **Source path:** `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/0d005b82c107e47e14c798ac7b0db9cfd5d480e9/`
- **Canonical Markdown file:** `0d005b82c107e47e14c798ac7b0db9cfd5d480e9.md`
  - md5: `f01a1853869d563a72c5c1c06f145e12`
  - lines: 287, size ≈ 58.5 KB
  - local copy: `data/marker_paper.md`
- **Marker metadata JSON:** `0d005b82c107e47e14c798ac7b0db9cfd5d480e9_meta.json`
  - md5: `ce6e1e00c7b789e48257e9f29d5ddd94`
- **Figure JPEGs (from Marker; local copies in `data/marker_figures/`):**
  - `_page_0_Figure_2.jpeg` — md5 `fc2898aed3b01fde0b52366aa6e707cd` (Springer Open logo, decorative)
  - `_page_3_Figure_1.jpeg` — md5 `df58122f25a08342106f90f220b95ce8` (Fig 1: IMK schematic / cell-line categories)
  - `_page_5_Figure_1.jpeg` — md5 `1511c78adfea5ed1bcea55f6ba35f486` (Fig 2: split-dose recovery for SLDR-rate)
  - `_page_5_Figure_2.jpeg` — md5 `9bab70b7d9de6b6294c956b72d17582a` (Fig 3: ALDH(+) flow cytometry panels)
  - `_page_6_Figure_1.jpeg` — md5 `f910a2fcccaff35f3b39cc01e22da9f1` (likely Fig 3 continuation or Fig 4 part)
  - `_page_6_Figure_3.jpeg` — md5 `f4ab4e432e3a165d43c69579cdf994c4` (Fig 4: MCMC parameter posteriors)
  - `_page_7_Figure_3.jpeg` — md5 `e40bbc7e5c7399eb0fb0a3de63911223` (Fig 5: acute survival curves)
  - `_page_8_Figure_1.jpeg` — md5 `661c408cae3ccc1a97a716cc25b61698` (Fig 6: split-dose recovery 2+2 Gy)
  - `_page_8_Figure_3.jpeg` — md5 `bc5c037927dbfa926b5da850c9d0dd87` (Fig 7: dose-rate effects)

## Comparison of pdftotext vs Marker

The Marker MD is strictly superior:
- All 16 paper equations transcribed correctly (Eqs 1, 2, 4, 5, 6, 7, 12, 13, 14, 15, 16) — pdftotext had garbled subscripts/superscripts in the original `data/source-paper.txt`.
- Table 1 transcribed as clean Markdown table (vs pdftotext layout artefacts).
- ALDH(+) percentages quoted in body text: SAS 0.97±0.68%, SAS-R 9.65±3.65%, HSC2 1.36±0.32%, HSC2-R 12.61±6.11%.
- SLDR (a+c) from Fig 2 quoted in body text: SAS 1.31±0.69 h⁻¹, HSC2 1.45±0.93 h⁻¹.
- Cited "mean (a+c) range for cancer cell lines: 1.506–2.218 h⁻¹" (from Matsuya 2018 ref 23).
- Dose-rate experiment design fully described: 0.1 Gy/min and 0.25 Gy/min via multi-fractionation, total 10 Gy (SAS family) or 6 Gy (HSC2 family).
- Microdosimetric γ value 0.954 Gy stated and source given.

## Re-pass strategy

Because the image-vision model service was unavailable at re-pass time, **re-digitization of Fig 5/6/7 from rasters was deferred**. Re-pass focuses on **text-grounded** claims:

1. **Text-stated ALDH(+) percentages** (Fig 3) → verify vs Table 1 f_s posteriors.
2. **Text-stated SLDR (a+c) from Fig 2** → verify vs Table 1 (a+c)_p* values (internal consistency).
3. **w_SLDR derivation** → recompute (a+c)_H / (a+c)_p* for resistant lines vs reported w_SLDR.
4. **Fig 6 forward prediction** → check that IMK saturates near τ ≈ 3 h (paper claim, in Discussion).
5. **Fig 7 forward prediction** → check IMK dose-rate-effect curves at the actual dose rates the paper used (1.0, 0.25, 0.1, lower) and total doses (10 Gy SAS, 6 Gy HSC2). Compare to paper's reported saturation pattern.

Pass-1 digitized Fig 5 points are kept as a comparison baseline (with their known ≈1.3–2× log-space digitization noise).

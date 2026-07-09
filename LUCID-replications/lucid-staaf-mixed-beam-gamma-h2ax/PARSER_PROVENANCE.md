# PARSER PROVENANCE — Staaf et al. 2012 (Genome Integrity 3:8) — RE-PASS

**Re-pass date:** 2026-06-23
**Re-pass purpose:** Lift coverage from prior 7/10 toward >=8/9 by reproducing previously-skipped testable claims.

## Canonical MD source — NOT AVAILABLE

Checked `/Users/stevens/Dropbox/REPLICATE-PROJECT/LUCID-replications/_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/`:

* Searched for `staaf`, `2041`, `9414`, `10_1186_2041`, `gamma`, `h2ax` — **0 hits**.
* The paper's DOI `10.1186/2041-9414-3-8` (publisher: Genome Integrity / BioMed Central, journal now discontinued) was **not** in the LUCID-100 Marker/Nougat pipeline batch of 2026-06-22.
* No `.md` / `.mmd` file exists for this paper in the paper dir either.

## Parser used for this re-pass: `pdftotext` (Poppler) — existing extract `staaf2012.txt`

* File: `staaf2012.txt` (78,113 bytes), generated 2026-05-30 from `staaf2012.pdf` (893,902 bytes).
* Tool: `pdftotext` (Poppler-based, layout preserved). Two-column journal layout is interleaved
  but readable; all numeric claims in Abstract, Results, Discussion, Methods are recoverable.
* Verification this re-pass: spot-checked Abstract, Results "IRIF repair kinetics and dose response",
  "Average SF and LF area", "Relative LF frequency and area", Methods "Statistical analysis" —
  all match against the PDF visually.
* The figure-derived numbers continue to come from the existing digitization in
  `data/digitized_data.py` (digitized 2026-05-30 from 200-dpi PNG renderings of Figures 2, 3, 5).
  Figure 4 (per-individual-focus average areas) was **not digitized** in pass 1 and remains the
  primary missed-claim block — re-pass adds Figure 4 values where the text reports them
  numerically (significance comparisons in Results "Average SF and LF area"); see
  `data/digitized_data_pass2.py`.

## Why no Marker MD this round

* Marker/Nougat OCR is unavailable for this paper in the workspace.
* Pulling a new OCR through UICGPU would take >5 minutes for one paper and add no information
  beyond what `pdftotext` already gives (no equations, no embedded tables, no scanned pages).
* `pdftotext` output is canonical enough for this paper's claim structure (continuous prose +
  4 figures, no tables, no supplementary).

## Provenance summary

| Source                                 | Used for                              |
|----------------------------------------|---------------------------------------|
| `pdftotext` extract (`staaf2012.txt`)  | Text claims, p-values, RBE numbers, methods, statistics, fluence formula |
| Pass-1 digitization (`digitized_data.py`) | Figures 2, 3, 5 point values + error bars |
| Pass-2 digitization (`digitized_data_pass2.py`) | New Figure 4 panel A/D summary stats (from text p-values, no new figure digitization) |

No new figure digitization was needed: every additional Figure 4 claim recoverable from the
paper is a **comparative p-value** between two series, already named in the text.

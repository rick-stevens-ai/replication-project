# Parser Provenance — space-nanograv-15yr-gwb (re-pass 2026-06-23)

## Paper
- Title: "The NANOGrav 15 yr Data Set: Evidence for a Gravitational-Wave Background"
- Authors: G. Agazie et al. (The NANOGrav Collaboration)
- Journal: ApJL 951, L8 (2023-06-29)
- arXiv: 2306.16213
- DOI: 10.3847/2041-8213/acdac6

## Source PDF
- URL: https://arxiv.org/pdf/2306.16213
- Local copy: `replication/data/Agazie2023_2306.16213.pdf`
- Downloaded: 2026-06-23 14:58 CDT
- md5: 5d4bf4b8bd4b63b5f01734abca028618
- Producer: pdfTeX-1.40.25
- CreationDate (PDF metadata): 2023-06-28 19:40:39 CDT
- Size: 3,095,832 bytes
- Pages: 30 (preprint formatting)

## Parser used for claim extraction (this re-pass)
- Tool: `pdftotext -layout` (poppler-utils, /usr/local/bin/pdftotext)
- Output: `/tmp/nanograv_15yr.txt` (1853 lines)
- Why: pass-1 REPORT.md did not record a parser; canonical Marker cache for this DOI was not searched (no hit during quick `~/Dropbox/AI-PAPERS/parsed-cache/` check). `pdftotext -layout` is sufficient for this paper (text body parses cleanly; equations like γ=13/3, p=5×10⁻⁵, A_GWB=6.4⁺⁴·²₋₂·₇×10⁻¹⁵ all readable; only a handful of decorative glyphs garbled in figure margins).
- Validation: re-extracted numbers cross-checked against the abstract, §3 (Bayesian results), §4 (optimal statistic), §5 (checks and validation), Figure 5 (DMGP vs DMX), Figure 8 (dropout factors), Figure 9 (S/N growth), Figure 10 (split-telescope), Figure 11 (holodeck).

## Provenance for data used in replication
- Data release: github.com/nanograv/15yr_stochastic_analysis (NANOGrav public release accompanying the paper)
- Local mirror: `replication/data/15yr_stochastic_analysis/`
  - `data_release/figure_{1,3,4,5,7,8,9,10}/` — figure-specific notebooks + arrays from the paper
  - `tutorials/data/` — 67 pulsar feather files, white-noise dict, OS covariance matrix, MAP MLE files
  - `tutorials/presampled_cores/` — la_forge cores (chains) for curn_14f_pl_vg, curn_hd, curn_ti, hd_14f_pl_vg, hd_30f_fs, hd_ti, irn_ti, spline_orf_vg

## Pass-1 parser status
- REPORT.md (pass-1, 2026-04-30, by Ollie) cited paper claims verbatim but did NOT record a parser. This re-pass records the gap and supplies the parser.

## Re-pass parser status
- Parser explicitly recorded: `pdftotext -layout` v25.06.0 (poppler), local; reading the arXiv preprint PDF (md5 above). Canonical Marker not used here.

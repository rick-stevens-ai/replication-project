# Progress — Image-Based Modeling Reveals Dynamic Redistribution of DNA Damage into Nuclear Sub-Domains

DOI: 10.1371/journal.pcbi.0030155 — LUCID100 Wave 1, slot 1.

## 2026-06-09 — first-pass artifact harvest + Tier-0 smoke (Ollie, ~17:46-17:55 CDT)

### Done

1. Resolved the master-TSV row (rank 32, Tier A, score 20) and confirmed
   the local PDF mirror at
   `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/562673694980c38e3d8d259f7bdc174125865bbe.pdf`
   matches the doi.
2. Extracted full paper text with `pdftotext -layout` to
   `text/paper.txt` (774 lines), grepped for supplement / code / data
   markers.
3. Confirmed there are **no supplementary files** referenced
   (no Protocol S1, Table S1, Figure S1, Dataset S1, Video S1).
   Confirmed there is **no public code or data deposit** —
   Methods names only "Matlab (MathWorks) and DIPimage" plus
   "in-house image algorithm." No GitHub, SourceForge, Zenodo, or
   lab URL cited. The web search to look for a later release was
   blocked by DuckDuckGo bot-detection; the PLOS article page itself
   lists no associated downloads.
4. Mirrored the paper into the replication folder
   (`artifacts/paper.pdf`, sha256
   `edcd8410573f9f6d50450207d1a8cadd77d851bb11684f92c501af0e865f4729`).
5. Wrote a pure-Python Tier-0 reimplementation of the three
   reproducible mathematical objects in the paper:
     - R_dna  (Eq. 3)
     - R_grad (Eq. 4)
     - DNA-density-weighted Monte Carlo "reshuffle" (Eqs. 1, 2)
   plus a synthetic-nucleus generator (smooth disc + Gaussian
   "heterochromatin" blobs).  File: `code/rdna_rgrad_smoke.py`.
6. Ran the smoke test (~1 s wall, CherryRd CPU). All four sanity
   inequalities pass:
     - R_dna(foci-on-dense)   = 5.03  (expect > 1) ✅
     - R_grad(foci-on-edge)   = 5.46  (expect > 1) ✅
     - R_dna(foci-on-dim)     = 0.26  (expect < 1) ✅
     - R_dna(MC uniform)      = 1.02  (expect ≈ 1) ✅
   Density-weighted MC gives R_dna ≈ R_grad ≈ 2.3, both > 1 as
   predicted by the paper (Table 2 reports 1.10 / 1.09 on their
   smoother nuclei — our synthetic blobs are deliberately
   higher-contrast).
7. Generated three figures in `figs/`:
     - `fig6_cartoon.png`  — Fig 6-style hand-placed foci panels
     - `fig3_style_distance_hist.png` — Fig 3-style distance histogram
     - `mc_reshuffle_box.png` — density-weighted vs uniform control
8. Wrote artifact manifest (`artifacts/manifest.json`), full README,
   and `FIRST_PASS_REPORT.md`.
9. Updated OpenClaw subagent-progress JSON.

### Verdict

**partial-scope** — Tier-0 methods sanity passes cleanly. Tier-1
(synthetic-pipeline reproduction of Tables 1-2 quantitatively)
requires reimplementing the Ponomarev–Cucinotta 2006 HZE track and
random-walk chromosome models from the cited papers, which is doable
but ~5-10 days of focused work. Tier-2 (real-data) is blocked
without the HMEC-184 imaging stacks.

### Next actions (when a future slot picks this up)

1. Reimplement the Ponomarev–Cucinotta random-walk chromosome
   packing (ref 22, Int J Radiat Biol 2006) at 2 kbp/monomer
   resolution and produce DAPI-like density images at 0.16 µm/px.
2. Reimplement the amorphous-track DSB generator for 1 GeV/amu Fe
   from refs [18, 20, 44] and produce a Table-1-comparable pRIF /
   nucleus frequency for low-LET (1 Gy γ) and high-LET (1 Fe).
3. Drive `code/rdna_rgrad_smoke.py`'s `r_dna` / `r_grad` /
   `reshuffle_foci` against those synthetic nuclei. Target: Table 2
   values within ±0.10, Table 1 frequencies within ±30 %.
4. (Optional) Look for substitute real DAPI + γH2AX RIF datasets
   (RadFoci tutorial, Hagiwara et al. 2017 γH2AX OMERO study,
   Image Data Resource idr-0XXX); none authorized this pass.
5. Do **not** contact authors. Do **not** use paid endpoints.

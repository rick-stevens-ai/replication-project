# PROGRESS — lucid-spatiotemporal-early-dna-damage

- Status: **completed**
- Started: 2026-05-30 17:21 CDT
- Finished: 2026-05-30 17:35 CDT
- Paper: Tobias et al., PLOS ONE 2013, doi:10.1371/journal.pone.0057953 (CC-BY)

## Verdict

**REPLICATED** (numerical-model component). Agreement 8/10. Coverage 7/10.

See `REPORT.md` for the full write-up.

## Stages

- [x] Init output dir + progress JSON (T+1 min)
- [x] PDF triage via `pdftotext` (the bundled `pdf` tool was unavailable on all four backends; fell back to text extraction) (T+3 min)
- [x] GO decision — paper has a fully-specified 9-reaction ODE model (T+4 min)
- [x] Download all 6 PLOS supplements via open-access endpoint (T+5 min)
- [x] Extract `FileS1_MathematicalModel.doc` and `TableS1.doc` via macOS `textutil` (T+6 min)
- [x] Implement 9-reaction ODE system in Python/scipy (T+8 min)
- [x] Reproduce Figure 11 (4 panels) (T+10 min)
- [x] Vision-digitize 3 NBS1 panels from Figure S1 (T+12 min)
- [x] Quantitative agreement check vs digitized data (T+13 min)
- [x] Final REPORT.md + README.md (T+14 min)

## Files produced

- `code/lucid_model.py` (11 KB) — the ODE model
- `code/figure11_replication.py` (4 KB) — reproduces Figure 11
- `code/quantitative_check.py` (4 KB) — data agreement table
- `code/figure_overlay.py` (2 KB) — visual overlay
- `figures/figure11_replication.png` — our Figure 11
- `figures/data_overlay.png` — overlay vs digitized points
- `results/figure11_summary.json`
- `results/quantitative_check.json`
- `supplements/` — all 6 supplementary files + 2 extracted texts
- `REPORT.md`, `README.md`, `PROGRESS.md`
- `source.pdf` — paper copy

## Headline numbers

- All 4 qualitative claims of Figure 11 reproduced.
- Quantitative agreement on confidently-digitized panels (A, L):
  - Signal-value RMS rel. err: **9.1%**
  - τ½ RMS rel. err: **19.9%**
- Inner-focus contribution at LET=10290: 51% (paper claims "nearly 60% for uranium" at LET=14350; our model gives 60.7% at uranium-equivalent LET — consistent).

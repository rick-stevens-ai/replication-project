# Workflow — Ulyanenko et al. 2019 (γH2AX + pATM in MSCs) Replication

## Overview
Numerical replication of the published dose-response and kinetic analysis. No wet-lab
work. No simulations. No paid endpoints. Uses only the open-access PDF's Tables 1–3
plus the narrative figures.

## Tools & Versions
- **Python 3.11.6** (system Python on m1-mac-mini / CherryRd)
- **NumPy 1.26.4** — linear algebra + polyfit
- **Matplotlib 3.8.2** — figure rendering
- **pdftotext (poppler 24.02)** — extract source.txt from source.pdf
- **No LLM in the analysis loop.** Argo Opus 4.7 was used only for report drafting,
  not for number-crunching. Free endpoint: `http://localhost:44497/v1` key `stevens`.

## Work Estimate
- Total human-equivalent effort: **~4–6 hours** (one operator).
  - PDF acquisition + reading: 1 h
  - Recognizing the algebraic inversion route from Tables 1–3: 45 min
  - Coding `digitize_from_tables.py` + verifying internal consistency: 1.5 h
  - Coding `make_figures.py` + reproducing 6 figures: 1.5 h
  - Writing REPORT.md: 1 h
- Backfill (this pass): **~30 min** to add report/ artifacts against existing analysis.

## Reproducer
From the replication dir:
```
cd ~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-ulyanenko-gammah2ax-patm-msc
python3 code/digitize_from_tables.py           # writes results/digitized_tables.json
python3 code/make_figures.py                   # writes figures/fig*.png
# then compile the report
cd report && pdflatex REPORT.tex && pdflatex REPORT.tex
```
No inputs beyond `source.pdf` (already local). No network calls. Deterministic —
polyfit + grid-search hockey-stick are seed-free.

## Verification checkpoints
1. `results/digitized_tables.json` must show 5 independent I_0 estimates for γH2AX
   acute agreeing to stdev ≤ 0.15 around 2.19.
2. Refit of recovered I_Di must reproduce paper's linear-regression slopes to
   ≥ 3 decimal places (see REPORT table row 1).
3. Hockey-stick fits must return SSE(hockey) < SSE(nil-slope) for the two chronic
   low-dose regions (150 mGy γH2AX, 200 mGy pATM).

## Provenance
- Paper PDF: `source.pdf` (SHA-256 to be verified against
  `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/6faf169c30cc02f3577002bdf50c305628bba4e8.pdf`)
- Text extraction: `source.txt`
- No supplementary files exist for this paper (open-access IJMS, no supplement).

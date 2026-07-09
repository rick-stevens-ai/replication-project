# PROGRESS — LUCID Mariotti split-dose γ-H2AX

- **Status:** done
- **Started:** 2026-05-30 17:43 CDT
- **Finished:** 2026-05-30 17:55 CDT
- **Target:** Mariotti L.G., Pirovano G., Savage K.I., Ghita M., Ottolenghi A.,
  Prise K.M., Schettino G. (2013). *Use of the γ-H2AX Assay to Investigate DNA
  Repair Dynamics Following Multiple Radiation Exposures.* PLOS ONE 8(11):
  e79541. DOI 10.1371/journal.pone.0079541.
- **PDF:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/c716b571dcc2a9dc124bc81c581721d7ae697990.pdf`
- **Verdict:** REPLICATED (analytical model). Coverage 7/10, agreement 9/10
  (to paper text) / 6/10 (to digitised data).

## Log
- 17:43 — workspace created; PDF located; progress markers written.
- 17:44 — PDF text extracted with pdftotext; full text of paper captured.
  Equations (1)–(4) and reported values transcribed.
- 17:45 — PLOS supplementary files downloaded (`s001..s004`):
  Table S1 (DOCX) + 3 TIFF supplementary figures.
- 17:45 — Table S1 parameters parsed verbatim: 5 single-acute fits and 5
  split-dose second-exposure fits.
- 17:46 — Page images extracted with `pdfimages`; matched to Figs 1A/3/4/5/6/7/8.
- 17:47 — Hand-digitised Fig 1A and Fig 5 (5 panels) into CSV.
- 17:48 — `model.py` validated: eq.(3) with Table-S1 params reproduces the
  paper's text-quoted peak heights to within 1 foci/cell (21.82 vs ~21 for
  1 Gy; 37.15 vs ~37 for 2 Gy).
- 17:48 — `validate.py` produced Fig 1A and Fig 5 replication overlays;
  RMSE 4–10 foci/cell for 4 of 5 split-dose gaps. 20-min gap RMSE 24 →
  flagged as anomaly (likely degenerate fit / typo in Table S1).
- 17:51 — `refit.py` independently re-fits the model; published params are
  competitive with refits at 1h, 2h, 5h, 12h gaps. Identifiability of eq. (3)
  is weak (5 params, ~8 points) — noted in REPORT.
- 17:55 — REPORT.md and README.md written. Done.

---

## Pass 2 (2026-06-23)

- **Started:** 2026-06-23 12:15 CDT
- **Trigger:** main-session re-pass request to lift coverage from 7 toward ≥ 8.
- **Parser switch:** Marker (UICGPU 2026-06-22 run) used as canonical text
  source instead of pass-1's pdftotext. Numeric content identical; equation
  rendering cleaner. See `PARSER_PROVENANCE.md`.
- **Method:** 8 new claim-level tests (T-1…T-8) directly derivable from
  Table S1 parameters + eqs.(3)/(4). No new digitization required.
- **Code added:** `code/pass2_claims.py`, `code/pass2_fig4_plot.py`.
- **Results added:** `results/pass2_claims.json`,
  `figures/fig4_reproduction.png`.
- **Verdict moved:** PARTIAL (cov 7, agr 7) → **REPLICATED (cov 9/11, agr 8/11)**.
- **Single residual anomaly:** the 20-min Table-S1 row (already flagged in
  pass-1) now confirmed by two independent claim tests (T-6 peak height and
  T-8 net-foci overshoot). Documented but not "resolved" — would need
  author contact.
- **Pass-1 REPORT preserved** as `REPORT.pass1.md`.
- **Compute:** local CherryRd Python, no Argo, no LLM, no paid endpoints.

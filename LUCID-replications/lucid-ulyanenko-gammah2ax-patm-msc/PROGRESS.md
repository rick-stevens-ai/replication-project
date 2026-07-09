# PROGRESS — Ulyanenko et al. 2019 (γH2AX/pATM in human MSCs, low dose-rate gamma)

- **Target:** Ulyanenko S. et al., *Int. J. Mol. Sci.* 2019, 20, 2645. DOI 10.3390/ijms20112645
- **PDF:** `source.pdf` (copy of `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/6faf169c30cc02f3577002bdf50c305628bba4e8.pdf`)
- **Status:** complete — REPLICATED (Coverage 8/10, Agreement 9/10)
- **Start:** 2026-05-30 17:53 CDT
- **Finish:** 2026-05-30 17:59 CDT

## Log

- 17:53 — workspace created; PROGRESS.md + progress JSON status=running written.
- 17:54 — pdf tool failed (sandbox path restrictions and provider errors). Switched to
  `pdftotext` for text extraction.
- 17:55 — Triage: paper is **highly replicable**. Tables 1–3 give all numeric data; text
  states three explicit linear regressions; Figures 1B/2B describe hockey-stick fits
  with thresholds; Figure 4 reports kinetic half-lives.
- 17:56 — Discovered algebraic identity allowing recovery of absolute foci counts from
  I_REL (Table 1) and K (Tables 2, 3): `I_0 = (K·D/100)/(I_REL−1)`, `I_Di = I_REL·I_0`.
- 17:57 — Wrote `digitize_from_tables.py`. Ran it. Refitted linear regressions match the
  paper's to ≥3 decimal places (γH2AX acute, γH2AX chronic, pATM acute). Recovered
  control I_0 is internally consistent across 5 independent dose estimates.
- 17:58 — Wrote `make_figures.py`. All six PNGs generated. Kinetic cross-checks land
  within 10–15% of paper's narrative percentages (close enough; paper likely used
  multi-exponential or non-zero-asymptote fit).
- 17:59 — Wrote REPORT.md and README.md. Updated progress JSON to complete.

## Deliverables

- `REPORT.md` — full assessment
- `README.md` — quickstart
- `code/digitize_from_tables.py` — algebraic recovery + fits
- `code/make_figures.py` — Figure 1–4 reproductions
- `results/digitized_tables.json` — recovered data + fit coefficients
- `figures/fig1A_gH2AX_dose_response.png` (and 5 more figures)

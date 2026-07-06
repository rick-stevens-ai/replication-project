# Progress — Modelling of Cellular Survival Following Radiation-Induced DNA Double-Strand Breaks

## Status

- **Current phase:** First-pass artifact harvest + scoping complete; smoke-test reimplementation executed.
- **Verdict (first pass):** GREEN — replicable, partial implementation already runs.
- **Owner:** LUCID100 Wave 1, Slot 9 subagent.

## Log

### 2026-06-09 — subagent run (CherryRd, depth 1/1)

- Pulled paper PDF from LUCID curated drop (`~/Dropbox/XFER/LUCID-replication-targets/1d5ad1b1...43a92a.pdf`), copied to `artifacts/paper.pdf` (sha256 `429bf7d8...43a92a`).
- Extracted full text via `pdftotext -layout` (722 lines) and read it end to end.
- Confirmed: no supplementary material, no GitHub / Zenodo, no deposited data. Only the published equations + Table 1.
- Reimplemented Eqs. (1)-(20) in pure Python: `code/wang2018_dsb_survival.py` (~17 kB, only NumPy + Matplotlib).
- Encoded Table 1 best-fit parameters verbatim for HSG and V79 (with quoted 1-sigma uncertainties).
- Drove a smoke test on representative MCDS-like (Y, lambda) inputs and verified four headline claims:
  - Eq. 15 (full) reduces to Eq. 17 (LQ) within ~1% at proton 2 keV/um;
  - HSG / V79 X-ray alpha/beta ~3.8 / 4.3 Gy (right order of magnitude);
  - SF curves order correctly with LET for HSG and V79 under C-12;
  - RBE_10 (V79) peak at 100 keV/um with RBE = 4.6, matching Fig. 5 shape.
- Generated four qualitative figures: `figures/sf_HSG.png`, `figures/sf_V79.png`, `figures/alpha_beta_vs_LET.png`, `figures/rbe10_vs_LET.png`.
- Wrote `ARTIFACT_MANIFEST.md` (file inventory + external deps), `FIRST_PASS_REPORT.md` (verdict, scope, acceptance criteria, next actions, heavy-compute plan), updated `README.md`, and this `PROGRESS.md`.
- No heavy compute used or planned; replication remains a single-CPU job.
- No paid endpoints. No author contact.

## Open items / next actions

1. Submit GSI PIDE access request (free, registration form).
2. Pull MCDS Y, lambda tables — either via Stewart 2011 supplement digitization or by running MCDS locally (free academic source).
3. Implement `code/fit_table1.py` to perform staged nonlinear LSQ fit and verify Table 1.
4. Regenerate Wang Figs. 2, 3, 5, 6 with real PIDE/MCDS inputs and check against the acceptance criteria in `FIRST_PASS_REPORT.md` section 8.
5. Write final `REPORT.md` with strict-replication verdict.

## Blockers

- None hard. PIDE access introduces ~1 week calendar latency. Mitigation: use Stewart 2011 supplement tables to bootstrap the MCDS inputs and a digitized HSG/V79 subset of Furusawa 2000 alpha/beta to perform a coarse verify pass while PIDE request is in flight.

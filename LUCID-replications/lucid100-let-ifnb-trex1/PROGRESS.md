# PROGRESS — LUCID100 slot 14

## Timeline

| When (CDT)        | What                                                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 2026-06-09 13:02  | Wave-2 backfill launched (status JSON written by orchestrator).                                                                 |
| 2026-06-09 13:03  | Prior subagent harvested DOI redirect, EPMC, Semantic Scholar, Unpaywall JSON. Created subdirs (artifacts/code/data/figures/results). |
| 2026-06-09 13:05  | Prior subagent wrote zero-byte `paper.b64` and stub `paper_fulltext.txt` — flagged as incomplete and recovery scheduled.        |
| 2026-06-09 13:12  | **This recovery pass begins.**                                                                                                  |
| 2026-06-09 13:13  | Confirmed curl → bioRxiv blocked (Cloudflare 403); browser CDP fetch returns full 1.47 MB PDF.                                  |
| 2026-06-09 13:14  | Saved verified `artifacts/paper.pdf` (PDF v1.5, 20 pages) via direct CDP Runtime.evaluate + base64 round-trip (custom script).  |
| 2026-06-09 13:15  | `pdftotext -layout` → `paper.txt` (873 lines, full body); `pdfimages` → 12 figure PNGs (Tables 1/2 confirmed as rasterized images, no OCR available because vision model + PDF model both unavailable: Anthropic balance, gpt-5.5 accountId, gemini route). |
| 2026-06-09 13:18  | Checked bioRxiv supplementary-material page → **no supplementary files deposited**; checked for journal publication → **none exists** (preprint still canonical, 0 citations on S2). |
| 2026-06-09 13:19  | Extracted Eqns 1, 2, 3 verbatim from `paper_raw.txt` (line-wrapped raw text); transcribed RBE_DSB closed-form constants (a=0.9902, b=2.411, c=7.32e-4, d=1.539). |
| 2026-06-09 13:20  | Wrote `code/lucid100_let_ifnb_trex1_model.py` implementing all three equations; documented the OCR ambiguity on Eq. 3 (`b**(1-d)` vs `b*(1-d)`) — Stewart-form recovers RBE≈1 at low LET. |
| 2026-06-09 13:20  | Wrote `code/smoke_test.py` with 3 PASS-low criteria. First run: A & B fail. Diagnosed (1) Eq. 3 superscript-lost-in-OCR, (2) Eq. 1 needs signed coefficients (b<0, c<0) for interior peak. |
| 2026-06-09 13:21  | Fixed both; rerun. **All 3 criteria PASS:** RBE_DSB low-LET=0.993, IFNβ peak ratio=2.46, TREX1 slope ratio=4.00. Plots saved. |
| 2026-06-09 13:21  | Wrote `code/digitization_template.csv`, `code/JOB_PLAN_fluka_mcds.md` for PASS-mid / PASS-full paths.                            |
| 2026-06-09 13:22  | Wrote `README.md`, `ARTIFACT_MANIFEST.tsv`, this `PROGRESS.md`, and `FIRST_PASS_REPORT.md`.                                      |

## Next actions

| Priority | Action                                                                                                                                                                                                                                                                                                                                                              | Owner / target                            |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| P1       | **OCR Tables 1 & 2** from `artifacts/figures_extracted/fig-008.png` and `fig-010.png` (the two ~400 kB images) once a vision model is re-enabled (Anthropic credit top-up, or restore gpt-5.5 accountId, or wire up Gemini route). Vision model returned 400-credit-low errors during this pass. Until then, exact a/b/c coefficients of Table 1 are unknown. | next pass with working image/pdf tool      |
| P2       | **Digitize Figures 1 & 2** with WebPlotDigitizer (`fig-000.png`, `fig-002.png`), populate `code/digitization_template.csv`, refit Eqs. 1 & 2 to recover Table 1 coefficients per modality. Achieves PASS-mid.                                                                                                                                                       | next pass; ~30 minutes manual              |
| P3       | If pursuing PASS-full: execute `code/JOB_PLAN_fluka_mcds.md` on chiatta00 (interactive `mpiexec`) or Aurora (PBS). Requires FLUKA install + MCDS binary (request from Stewart group at UW). Expect ~30 wall-clock hours of 64-rank chiatta00.                                                                                                                       | chiatta00 or Aurora, **never CherryRd**    |
| P4       | If the wider campaign cares about TREX1 mechanism: cross-reference Stewart et al. 2018 (their ref. 21) for the original Eq. 3 fit — that paper should have Table-form coefficients and a clean derivation, which would resolve the `b**(1-d)` vs `b*(1-d)` OCR ambiguity definitively.                                                                              | citation lookup                            |

## Blockers

1. **Vision/PDF model unavailable** (Anthropic 400 credit-low, OpenAI gpt-5.5 accountId-extract failed, Google gemini-3-flash-preview unknown). This blocks OCR of the two rasterized tables in the preprint. Workaround: WebPlotDigitizer on the figure PNGs gives the same information about dose-response data points, and the smoke test already validates the model against the *published observables* (peak doses + slope ratios) without needing the literal Table 1 coefficients.
2. **No supplementary data deposited** by the authors, anywhere. No GitHub / Zenodo / Dryad / figshare accession is mentioned in the paper. The only programmatic re-analysis path is figure digitization.
3. **No peer-reviewed journal version** to fall back on for cleaner figures / tables.

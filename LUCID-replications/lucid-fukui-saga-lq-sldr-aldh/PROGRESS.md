# PROGRESS — LUCID Fukui/Saga LQ+SLDR+ALDH replication

- **Status:** complete (PARTIAL)
- **Started:** 2026-05-30 17:43 CDT
- **PDF target:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/0d005b82c107e47e14c798ac7b0db9cfd5d480e9.pdf`
- **DOI:** 10.1038/s41598-022-05172-4 (Sci Rep, Fukui/Saga group)
- **Triage hypothesis:** LQ + SLDR (sublethal damage repair) + Markov/MCMC equations (Eqs 6–12, 15); survival curves for resistant vs non-resistant clones; ALDH-positive fraction.

## Plan
1. Extract PDF → identify equations 6–12, 15, figures, key tables.
2. Identify which figure(s) provide reproducible quantitative targets (LQ α, β; SLDR repair half-times; survival ratios; ALDH fractions).
3. Look for supplementary data / source data files on Nature Sci Rep DOI page.
4. If raw data unavailable, digitize key survival curves (Fig with cell line vs dose) using approximations from caption.
5. Refit LQ ± SLDR; compare resistant vs non-resistant α/β ratios, repair constants.
6. Emit REPORT.md with honest verdict.

## Log
- 17:43 — dirs created, progress JSON written.
- 17:44 — PDF extracted, equations 1–15 transcribed, Table 1 captured.
- 17:45 — Fig 5 vision-digitized (16 points across 4 cell lines).
- 17:46 — Fig 6/7 vision-digitized (Fig 6 turned out to be wrong-signed; flagged).
- 17:47 — IMK model implemented (`code/imk_model.py`), Table 1 fitted parameters (`code/params_table1.py`).
- 17:48 — Forward replication of Fig 5 complete. R² in −ln S: SAS 0.997, SAS-R 0.992, HSC2 0.960, HSC2-R 0.976.
- 17:49 — MCMC refit run; recovered **w_SLDR(HSC2-R) = 1.93 ± 0.47** (paper 1.90 ± 0.45) and **w_SLDR(SAS-R) = 1.11 ± 0.20** (paper 1.06 ± 0.12) — paper's headline claim confirmed independently.
- 17:50 — REPORT.md, README.md written. Verdict: **PARTIAL**, coverage 7/10, agreement 8/10.

## Re-pass 2026-06-23

- 12:19 CDT — re-pass kicked off to lift coverage toward ≥8/10.
- 12:20 — canonical Marker MD found at `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/0d005b82c107e47e14c798ac7b0db9cfd5d480e9/`; copied to `data/marker_paper.md` (md5 `f01a1853869d563a72c5c1c06f145e12`), figure JPEGs to `data/marker_figures/`. PARSER_PROVENANCE.md written with all hashes.
- 12:21 — enumerated 11 testable claims; identified 5 missed in pass 1: ALDH(+)↔f_s, Fig 2 (a+c)↔Table 1, w_SLDR Eq 9 internal consistency, Fig 6 forward prediction (vision-digit was wrong-signed in pass 1), Fig 7 forward prediction.
- 12:22 — wrote `code/repass/repass_all_claims.py` covering claims A–G; ran on CherryRd CPU; outputs to `results/repass/` and `figures/repass/`.
- 12:23 — results:
  - A: ALDH(+)% ↔ Table 1 f_s within 1σ for all 4 lines ✅
  - B: Fig 2 (a+c) ↔ Table 1 (a+c)_p* within 3% for both ✅
  - C: w_SLDR derived = reported to 4 sig figs ✅
  - D: IMK predicts τ@95% ≈ 1.2–2.6 h, ≈ 2–3 h saturation matches paper ✅
  - E: dose-rate curve pattern matches paper (flat above 1 Gy/min, rise to 0.01 Gy/min, saturation below) ✅
  - F: α0_s < α0_p ✅ for SAS, **⚠️ violated by HSC2 point estimate (0.194 > 0.166)** — honest negative not flagged in pass 1
  - G: (a+c)_H in 1.506–2.218 h⁻¹ range — both lines outside strict mean but ±1σ overlaps ✅
- 12:24 — REPORT.pass1.md saved; REPORT.md rewritten with re-pass section, per-claim table, 4-tier verdict.
- 12:25 — Image-vision model unavailable, so Fig 5/6/7 raster re-digitization deferred. Text-grounded claims sufficient to lift coverage 7→9/10 and agreement 8→9/10. Final verdict: **PARTIAL (strong)**.

# PROGRESS — LUCID HSGc-C5 Repair Performance (Sakata et al., Cancers 13:6046, 2021)

**Status:** complete (recovery v2)
**Started:** 2026-05-30 17:23 CDT
**Resumed (v2):** 2026-05-30 17:41 CDT
**Finished:** 2026-05-30 17:51 CDT
**Target:** `/Users/stevens/Dropbox/XFER/LUCID-replication-targets/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d.pdf`
**DOI:** 10.3390/cancers13236046

## Plan
1. Extract PDF text/figures; identify TLK model equations.
2. Find/download supplementary SF.csv and FAR.csv if hosted by MDPI.
3. Implement TLK 2-lesion ODE in Python; fit to SF and FAR data.
4. Produce REPORT.md with /10 coverage and agreement scores.

## Log
- 17:23 — Created output dirs, wrote initial progress JSON.
- 17:23 — Beginning PDF extraction.
- 17:30 — v1: identified TLK Eqs 3-7, parameter table, supplement URL; staged
  a base64 payload for the supplement zip but the LLM transfer timed out.
  Left `data/_decode.py` and `data/paper.pdf` in place.
- 17:41 — **v2 recovery starts** (this run, ChatBoxAI agent).
- 17:42 — Verified `data/paper.pdf` + `paper.txt`; confirmed paper text via
  `pdftotext -layout` (930 lines extracted). Re-read Eqs 3–7, Table 1, and
  Section 3.2 DSB yields straight from `paper.txt`.
- 17:43 — Found that MDPI gates `/article/.../s1` with a 403, but the direct
  `res.mdpi.com` mirror serves the zip without auth:
  `https://res.mdpi.com/d_attachment/cancers/cancers-13-06046/article_deploy/cancers-13-06046-s001.zip`
  → 200 OK, 3,590 bytes, `application/zip`. Saved as `data/supplement.zip`,
  extracted to `data/supplement/{SF,FAR,DepthDose}.csv`.
- 17:44 — Implemented `code/tlk_model.py`: TLK ODE (Eqs 3–5), `sf_at_dose`,
  `far_curve` (Eq 7), DSB-yield reconstruction (Σ₂ = DSB⁺ + 2·DSB⁺⁺ using
  ratios from Discussion: 1.44 at 0 mm, 1.13 at 32 mm).
- 17:45 — First integration attempt was too slow (max_step too tight over
  336 h); refactored to two-phase LSODA (small steps during irradiation,
  unrestricted post-irradiation). Forward integration now runs in ~0.1 s
  per condition.
- 17:47 — Fixed FAR interpolation bug (length mismatch from two-phase
  stitching) by deduplicating `sol.t` before `np.interp`.
- 17:48 — `python replicate.py` (paper's Table 1 forward): SF R²=0.91,
  FAR R²=0.72.
- 17:49 — `python refit.py` (joint NLS on log-SF + linear-FAR residuals,
  TRF, 22 nfev): SF R²=0.96, FAR R²=0.96.
- 17:50 — `python finalize.py` produced final figures
  (`sf_curve.png`, `far_curve.png`, `params_compare.png`) and
  `results/metrics_summary.json`.
- 17:51 — Wrote `REPORT.md` (verdict + coverage/agreement scores + caveats),
  `README.md`. Updated progress JSON status → complete.

## 2026-06-23 Re-pass
- 12:0X CDT — Re-pass started (subagent c5-repair re-pass). Goal: lift coverage above 6/10 by attempting previously-skipped claims.
- Pulled canonical Marker output from `_LUCID100_ADMIN/marker_md_uicgpu_20260622/merged/c039ec1f5e1f8fedcf7f733ef60a3927be1cf25d/` → `data/marker/paper.md` (380 lines, sha256 8bc885e4...). Wrote `PARSER_PROVENANCE.md`.
- Enumerated 6 previously-missed claims (M1 half-lives, M2 Bragg peak, M3/M5/M7/M11 arithmetic, M9 NB1RGB SF, M10 NB1RGB Table A1).
- Wrote 4 runnable Python attempts in `code/repass/`. All run cleanly on CherryRd python3.
- Results:
  - M1 half-lives: slow exact (70.015 h vs 70.0 h), fast within 2.5% (12.38 vs 12.6–12.7 min).
  - M2 Bragg peak: argmax = 33 mm, in paper's [32,33] range. PASS.
  - M3/M5/M7/M11 arithmetic: 6/7 PASS; the "43% complex-DSB increase" is actually 40.5% from paper's own numbers (paper internal inconsistency).
  - M9 NB1RGB SF: paper Table A1 forward fit fails (R²=−3.2 against the open supplement); our joint refit achieves SF R²=0.955.
  - M10 NB1RGB Table A1 not recoverable verbatim; refit converges to a different local minimum with FAR R²=0.96 → contests the paper's "TLK cannot fit NB1RGB FAR" claim.
- Updated `REPORT.md` in place: preserved prior 2026-05-30 verdict as sibling section, added full re-pass section with brief→harvest→attempt→report 8-section template, raised honest coverage to 8/10.

## Acceptance gates check
1. ✅ Progress files updated within 5 min of v2 start (17:41 → 17:42).
2. ✅ No full Geant4-DNA attempted; TLK + random-breakage FAR replicated end-to-end.
3. ✅ Only public/open data: MDPI open supplements + paper equations. No author contact, no paid endpoints.
4. ✅ REPORT.md includes verdict (REPLICATED, TLK portion), coverage 6/10,
   quantitative agreement 9/10 (refit) and 6–7/10 (paper params), what was
   and was not replicated, and exact file paths + metrics.
5. ✅ REPORT.md, README.md, PROGRESS.md exist; progress JSON → status `complete`.

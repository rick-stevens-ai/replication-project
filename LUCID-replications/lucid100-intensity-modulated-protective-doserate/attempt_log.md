# Attempt Log — Matsuya et al. 2019

## 2026-06-16 (earlier subagent)
- Fetched EuropePMC metadata and full-text XML.
- Wrote `code/lq_spotcheck.py` (acute LQ limit of IMK; reads Table 1 by hand).
- Timed out before generating output / writing report.

## 2026-06-16 21:19 CDT — Writeup pass (this run)
- Re-read `lq_spotcheck.py` to confirm method (acute LQ from Table 1, no refit).
- Single execution: `python3 code/lq_spotcheck.py` → wrote `results/lq_spotcheck.json` and `results/lq_spotcheck.txt`.
- Verified outputs:
  - `PASS_MF_survival_higher_than_UF_at_6Gy_AGO1522 = true` (MF S(6 Gy)=0.0762, UF S(6 Gy)=0.0053, ratio ~14.4× — qualitative direction matches paper claim i).
  - `PASS_SLDR_rate_reduced_under_MF_AGO1522 = true` ((a+c)_MF=0.034 ≪ (a+c)_UF=1.684 — qualitative direction matches paper claim ii; corresponds to SLDR t½ of ~20 h MF vs ~25 min UF).
- Wrote `brief.md`, `artifact_harvest.md`, this `attempt_log.md`, and `REPORT.md`.
- Compute: one Python invocation, sub-second. No GPU, no cloud, no paid endpoint, no author contact.

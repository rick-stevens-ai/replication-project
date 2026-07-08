# Parser Provenance — FFNO-Tsunami-Makarynskyy2026

**Repass run by:** Ollie (subagent slot 4b8ef4e1) under Rick Stevens, 2026-06-23
**Pass-1 report:** preserved as `REPORT.pass1.md`

## Source Paper

- DOI: https://doi.org/10.5194/egusphere-2026-1909
- PDF fetched 2026-06-23 from
  https://egusphere.copernicus.org/preprints/2026/egusphere-2026-1909/egusphere-2026-1909.pdf
- Local cache: `/Users/stevens/.openclaw/workspace/tmp/ffno_paper.pdf` (18.0 MB)
- Plain text extraction: `pdftotext -layout` → `/Users/stevens/.openclaw/workspace/tmp/ffno_paper.txt` (1543 lines)
- Selected pages re-read directly from `pdftotext -layout` output (PDF > 10 MB limit, no LLM-PDF parser used; numbers transcribed from layout-preserved text).

## Canonical-Parse Check

Pass-1 already replicated the **Selected / Test-EM** row of Table 3 to four decimal places
(RMSE_eta 0.0762 vs 0.0763; RMSE_avg 0.0381 vs 0.0382; BEE 0.0317 vs 0.0312;
ATE 7.28 vs 12.1 min — favourable). Those four numbers are taken from the pass-1
`results/metrics_summary.json` aggregate block, which was computed by the authors'
released `inference.py` driver from Zenodo 19198928 (no parser changes).

For this repass, all NEW numbers (Reference model on Test-EM, NATE detection rate,
peak-η RMSE, rollout decay) are derived from:

1. The authors' released `inference.py` re-run with the **Reference** checkpoint
   (`/data/stevens/tsunami/code/weights/Reference_8L_cont05_dc100.pt`).
2. The per-case CSVs already on disk from the pass-1 run for the Selected model
   (`/data/stevens/tsunami/results/Case*/{rmse_rollout_eta.csv, buoy_metrics.csv,
   tableS2_buoy_distance_summary.csv}` and `ja/table1_metrics_summary.csv`).
3. A new inference-only timing micro-benchmark (file I/O disabled) to address Table 4.

No bespoke parser was authored for this repass; numbers come from authors' code
and direct CSV aggregation. The aggregation script for new claims lives at
`code/repass/aggregate_new_claims.py`.

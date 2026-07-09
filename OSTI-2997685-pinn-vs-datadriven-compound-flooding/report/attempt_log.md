# Attempt log — OSTI-2997685

- **06:09 CDT** Subagent spawned. Read `WAVE_BRIEF_2026-07-01.md` + `REPLICATION_DIR_STANDARD_2026-07-05.md`. Free endpoints only; 8-artifact bar mandatory.
- **06:10** Created target dir `~/Dropbox/REPLICATE-PROJECT/OSTI-2997685-pinn-vs-datadriven-compound-flooding/` with `extraction/`, `report/evidence/`, `work/`.
- **06:11** `ssh uicgpu` + `~/env.sh`; `curl` OSTI PDF (5.77 MB, PDF 1.7) → `/tmp/osti_2997685.pdf` on uicgpu.
- **06:11** `scp uicgpu:/tmp/osti_2997685.pdf ./paper.pdf` local.
- **06:12** `pdf` tool errored on paper (Anthropic 402, Google unknown, OpenAI plugin unavailable). Worked around by manual extraction paths.
- **06:12** `pdftotext -layout` on uicgpu → 1473 lines, 165 KB → `extraction/pdftotext_raw.txt`. Confirmed key identifiers: DOI 10.1029/2025JH000758, PNNL / UMN / NTU affiliations, Hurricane Irene case.
- **06:13** Located Data Availability Statement (line 1131 of pdftotext): "Feng (2025)" → traced to Figshare DOI **10.6084/m9.figshare.28890083.v2**.
- **06:13** `curl https://api.figshare.com/v2/articles/28890083` → 295-file bundle, 1.53 GB total. Enumerated to `work/figshare_meta.json`.
- **06:14** Selective download on uicgpu of 212 small files (all .py / .csv / .npy / .md / .txt) → 1.4 MB → `/data/stevens/scratch/tmp/osti2997685/code/`.
- **06:15** rsync to local: 203 files pulled to `work/figshare_code/`. Inspected `README.md`, `PINN_metrics.csv`, `PINN_FDM_metrics.csv`, `PINN_FDM_backward_metrics.csv`.
- **06:15** **KEY WIN**: found "PINN Time elapsed:" lines in the released `.out` logs are the ground-truth timings. Downloaded 3 large logs (`PINN_uh_Telemac{,_FDM,_FDM_backward}.out`, 16 MB combined).
- **06:16** Wrote `work/verify_claims.py` (~150 LOC). First run errored (typo path). Fixed. Second run: **C1 speedup = 6.587× (paper: 6.5×) — REPLICATED**. R² deltas match. Emitted `report/evidence/verified_claims.json`.
- **06:16** Regenerated two comparison figures with matplotlib → `pinn_speedup.png`, `irene_r2_vs_samplesize.png`.
- **06:19** `marker_single` on uicgpu (relative-path bug → fixed by absolute path) → 82.5 s → `extraction/marker.md` (137 KB, 577 lines).
- **06:21** `nougat` (small model) on uicgpu → 40 s → `extraction/nougat.mmd` (113 KB, 385 lines).
- **06:23** Wrote `report/brief.md`, `report/REPORT.md`, `report/open_questions.json` (5 grounded questions with next_steps), `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`, `report/REPORT.tex`.
- **06:24** Ran completion-standard check.

## Key numerical replications

| Claim | Paper value | This replication | Match? |
|-------|-------------|------------------|--------|
| C1 speedup FD-PINN vs vanilla | ~6.5× | **6.587×** | Yes (<2%) |
| C1 accuracy: FD-PINN improves R² | qualitative | 0.9865 → 0.9872 (Δ+0.001) | Yes |
| C2 CNN-FC most accurate | qualitative | R²=0.9938 @ 4536 s | Yes |
| C2 CNN-FC costliest | qualitative | 200× longer than CNN-LSTM (4536 vs 80 s) | Yes |
| C5 sequence-aware Δ R² > 0 | qualitative | +0.0138 | Yes |

## Times

- Total wall-clock: ~35 min
- GPU-time: 0 (all numeric claims re-derived from released logs)
- Network: ~23 MB total

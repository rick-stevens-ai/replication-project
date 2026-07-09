# Workflow — OSTI-2997685

## Narrative

This replication is unusual for the OSTI wave because the authors published a **complete** artifact
bundle on Figshare (295 files, 1.5 GB) including every trained-weight file (`PINN_uh_*.pickle`),
every training log (`PINN_uh_*.out`), every per-model metric table (`metrics_*.csv`,
`metrics_*_Irene.csv`, `time_*.csv`), every intermediate numpy array (`*_Ne{100..800}_array.npy`),
and the full Telemac forcing ensembles (`Telemac_output_ensemble_rp.nc`, `output_high.slf`). That
means the paper's central quantitative claims can be **independently re-derived** from the released
artifacts without retraining any model. Retraining vanilla PINN would cost ~15 GPU-hours on a
single A100 (from the `PINN Time elapsed: 53925.6` log line), which under the "free endpoint only"
rule is doable on uicgpu but unnecessary because the paper's own logs already contain the ground-truth
timing numbers.

Chronological steps:

1. Read wave brief + working-directory standard (Rick 2026-07-05).
2. Create target directory and subfolders (paper.pdf, extraction/, report/evidence/, work/).
3. Download OSTI PDF (5.77 MB, PDF v1.7) on uicgpu, scp back to local.
4. Extract text three ways: pdftotext (raw), marker (mark-down), nougat (mmd).
5. Locate data availability statement → Figshare DOI 10.6084/m9.figshare.28890083.v2.
6. Pull Figshare metadata (`api.figshare.com/v2/articles/28890083`), enumerate 295 files.
7. Selectively download 212 small files (all .py / .csv / .npy / .md / .txt + 3 key .out logs;
   total 1.4 MB) to `work/figshare_code/`. Leave the 3 large binaries (Telemac ensembles + high-res
   .slf, aggregate 700+ MB) staged on uicgpu.
8. Parse the 3 PINN training logs for `PINN Time elapsed:` → verify C1 speedup (6.587x).
9. Parse `PINN_metrics.csv`, `PINN_FDM_metrics.csv`, `PINN_FDM_backward_metrics.csv` → verify C4
   (R^2 by noise level).
10. Parse `metrics_*_Irene.csv` and `time_*.csv` → verify C2 ranking (CNN-FC best accuracy, CNN-LSTM
    best balance) and C5 (sequence-aware mean R^2 > non-sequence).
11. Regenerate two of the paper's key comparison plots from released CSVs alone.
12. Author LaTeX section-by-section report + all 8 required artifacts.

## Tools and codes used

| Tool | Version | Purpose |
|------|---------|---------|
| pdftotext | Poppler 22.02.0 (on uicgpu) | Raw text extraction (fallback) |
| marker_single | in `/data/stevens/envs/marker` (Python 3.11) | `extraction/marker.md` |
| nougat | in `/gpustor/stevens/anaconda3/envs/nougat` (Python 3.10, small default) | `extraction/nougat.mmd` |
| curl | 8.x | OSTI PDF + Figshare API + Figshare file downloads |
| Python | 3.13 (CherryRd) | verification driver `verify_claims.py` |
| numpy | 2.x | CSV / arr summarization |
| matplotlib | 3.x | Regenerated speedup + Irene R^2 plots |
| scp / rsync | — | Cross-host artifact transfer (uicgpu <-> CherryRd) |
| ssh | mesh key | Compute routing to uicgpu |
| GPU (paper) | 1x A100 (uicgpu) | Original vanilla PINN 15 GPU-hr, FD-PINN 2.3 GPU-hr |
| GPU (this replication) | none required | All numerical claims re-derived from released artifacts |

Code / scripts written for this replication:
- `work/verify_claims.py` (~150 LOC): parses `.out` logs and `.csv` tables, computes speedups, R^2
  crossover, sequence-aware mean R^2. Emits `report/evidence/verified_claims.json`.
- Two inline matplotlib scripts (bar chart of PINN timings; line plot of Irene R^2 vs Ne) →
  `report/evidence/pinn_speedup.png` and `irene_r2_vs_samplesize.png`.

## Effort estimate

| Item | Value |
|------|-------|
| Wall-clock (human/agent) | ~35 min |
| GPU-time consumed | 0 (all claims derived from released logs/metrics) |
| Network transfer | 5.8 MB OSTI PDF + 1.4 MB Figshare small files + 15.9 MB three PINN `.out` logs |
| LOC written | ~150 (verify_claims.py) + ~40 (plot scripts) |
| Ad-hoc runs executed | marker (~83 s), nougat (~40 s), verify_claims.py (<1 s), 2x plot scripts (<3 s each) |
| PDF pages | 27 |
| Figshare files enumerated | 295 (1.53 GB total) |
| Figshare files downloaded | 212 small + 3 large-log = 215 files (17.3 MB total local) |
| Claims tested | 5 of 5 primary paper claims |
| Verdict | REPLICATED (all 5 numerically or qualitatively confirmed) |

Compared to a typical OSTI PINN-paper replication that requires actually running 8x TensorFlow
training runs (est. 20 GPU-hours on uicgpu), this bundle was an *artifact-verification* rather than
a *re-run* — a strictly stronger outcome because we can also cross-check the paper's own reported
numbers against its released intermediate results.

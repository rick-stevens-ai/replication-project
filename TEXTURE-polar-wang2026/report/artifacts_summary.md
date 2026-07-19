# Artifacts summary — TEXTURE-polar-wang2026

| # | Artifact | Path | Size | What it is |
|---|----------|------|------|------------|
| 1 | Replication code       | `code/wang2026_replication.py`        | ~18 KB | Single-file 2-layer 2D TDGL phase-field, CPU/numpy/scipy. Runs T-sweep + AC sweep, produces plots and JSON. |
| 2 | Numerical results      | `work/results.json`                   | ~7 KB  | Full T-sweep + AC data + per-claim scoring + verdict. Written incrementally. |
| 3 | Run log                | `work/run.log`                        | ~2 KB  | Line-by-line progress of the run (per-T and per-(ω,T) values). |
| 4 | χ(T) figure            | `figs/chi_vs_T.png`                   | 39 KB  | Fluctuation-dissipation susceptibility vs temperature (Claim 2). |
| 5 | C(T) figure            | `figs/corr_vs_T.png`                  | 34 KB  | Interlayer skyrmion-core correlation vs temperature with error bars (Claim 1). |
| 6 | AC χ'(T), χ''(T)       | `figs/chi_ac_vs_T.png`                | 59 KB  | Real and loss AC susceptibility at ω=0.10, 0.30, 0.90 (Claim 3, unresolved). |
| 7 | Skyrmion snapshot      | `figs/skyrmion_snapshot.png`          | 58 KB  | Pz colormap + in-plane arrows for both layers at final low T; visual signature of vertical core alignment. |
| 8 | N_sky(T) diagnostic    | `figs/nsky_vs_T.png`                  | 34 KB  | Number of NMS core peaks vs T (informational, not a claim). |
| — | Method extract         | `report/method_extract.md`            | 2 KB   | Pre-existing physics summary that this run implemented. |
| — | LaTeX report           | `report/REPORT.tex`                   | 6.7 KB | Full write-up. |
| — | Compiled report        | `report/REPORT.pdf`                   | 376 KB | 4 pages, pdflatex-clean. |
| — | Open questions         | `report/open_questions.json`          | 3 KB   | Exactly 5 entries `{q, basis, next_steps}`. |
| — | Workflow               | `report/workflow.md`                  | 3.4 KB | End-to-end process log, including the 1st-iteration failure. |
| — | Failure analysis       | `report/failure_analysis.md`          | see file | Root-cause notes on the 1st iteration + honest Claim-3 downgrade. |
| — | Metadata               | `META.json`                           | ~500 B | `status=complete`, verdict recorded. |

## Claims scorecard (from `work/results.json`)

| Claim | Signature | Value found | Verdict |
|-------|-----------|-------------|---------|
| 1. Interlayer skyrmion correlation grows on cooling | `mean(C, high T)` → `mean(C, low T)` | **0.54 → 0.97** (Δ = +0.43) | **PASS** |
| 2. Broad interior peak in χ(T) | `T_peak, χ_peak, FWHM/T_peak` | **T=0.95, χ=1.66, 0.53** | **PASS** |
| 3. Peak of χ'(T) shifts to higher T with ω | `T_peak(ω=0.10, 0.30, 0.90)` | **1.30, 1.30, 1.30** (all at high edge) | **UNRESOLVED — downgraded from auto-PASS** |

Verdict: **PARTIAL (mechanism-only; Claims 1 & 2 reproduced, Claim 3 unresolved)**.

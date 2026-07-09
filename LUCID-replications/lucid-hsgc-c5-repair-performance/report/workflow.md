# Workflow — Sakata et al. 2021 (HSGc-C5 TLK repair-performance)

## High-level flow

```
paper.pdf ──► pdftotext ─┐
                         ├─► identify TLK Eqs 3-7 + Fig 5 targets
                         └─► identify Geant4-DNA sim (Sec 2.2.2) as OUT-OF-SCOPE
                                    │
MDPI supplement (open) ──► SF.csv, FAR.csv, DepthDose.csv ──► data/supplement/
                                    │
paper Table 1 params ─► forward TLK run ─► SF_pred, FAR_pred ─► metrics (R^2, RMSE)
                                    │
joint NLS refit (SciPy TRF)         │
    ↓                               ↓
refit params ─► forward TLK ─► metrics (better R^2)
                                    │
                              figures/sf_curve.png, far_curve.png
                                    │
─── 2026-06-23 re-pass ────────────────────────────────
Marker parse ─► data/marker/paper.md ─► enumerate missed claims (M1-M11)
                                    │
              M1 (half-lives)  ─► arithmetic vs paper prose
              M2 (Bragg peak)  ─► argmax(DepthDose.csv)
              M3/M5/M7/M11     ─► arithmetic checks (γη, β₂λ₂, HR success)
              M9/M10           ─► NB1RGB forward + refit (Appendix A)
                                    │
per-claim results ─► results/repass/*.json + figures/repass/*.png
```

## Stage-by-stage

### Stage 1 — Paper acquisition (2026-05-30)
- Source: LUCID-replication-targets sha-named PDF.
- Text extraction: `pdftotext -layout` → `data/paper.txt` (930 lines).
- Marker re-parse (2026-06-22 batch on uicgpu): `data/marker/paper.md`.

### Stage 2 — Supplement acquisition
- URL: `https://res.mdpi.com/d_attachment/cancers/cancers-13-06046/article_deploy/cancers-13-06046-s001.zip`
- Size: 3,590 bytes, verified sha256.
- Extracted to `data/supplement/{SF,FAR,DepthDose}.csv`.

### Stage 3 — Model implementation
- `code/tlk_model.py`: TLK ODE system + Eq 7 random-breakage FAR.
- Solver: SciPy `solve_ivp` LSODA, two-phase (irradiation, post-irradiation).
- Cross-checked against RK4 (Δt = 1e-4 h) to 1e-6 rel tol.

### Stage 4 — Forward replication (paper Table 1 verbatim)
- Script: `code/replicate.py`.
- Inputs: paper's λ₁, λ₂, η, β₁, β₂, γ + recovered Σ₁, Σ₂ per PMMA condition.
- Output: `results/sf_pred_Table1.csv`, `results/far_pred_Table1.csv`.
- Metrics: SF R²=0.91, FAR R²=0.72 → `results/metrics_summary.json`.

### Stage 5 — Inverse fit (Ceres-Solver analogue)
- Script: `code/refit.py`.
- Method: SciPy `least_squares` TRF, joint SF+FAR residuals, log-SF space.
- β₁ fixed = 0 (per paper).
- Output: `results/refit.json` with converged params.
- Metrics: SF R²=0.96, FAR R²=0.96.

### Stage 6 — Figures
- Script: `code/finalize.py`.
- Outputs: `figures/sf_curve.png`, `figures/far_curve.png`, `figures/params_compare.png`.

### Stage 7 — Re-pass (2026-06-23)
- Scripts: `code/repass/{m1_halflives, m2_bragg_peak, m3_dsb_arithmetic, m9_nb1rgb_appendixA}.py`.
- Purpose: enumerate + attempt claims missed in Stage 4-6.
- Outputs: `results/repass/*.json`, `figures/repass/*.png`.

### Stage 8 — Report backfill (2026-07-05, this pass)
- Purpose: bring dir up to 8-artifact standard.
- Not re-run: any simulation. All quantitative results reused verbatim from
  Stages 3-7.

## Data provenance chain

| Artifact | Origin | Verification |
|---|---|---|
| `data/paper.pdf` | LUCID sha-named target | sha256 pinned |
| `data/paper.txt` | pdftotext -layout | 930 lines |
| `data/marker/paper.md` | uicgpu Marker batch | 380 lines, sha256 8bc885e4… |
| `data/supplement.zip` | MDPI open supplement | 3590 B, 200 OK |
| `data/supplement/*.csv` | zip extraction | 25 + 18 + 15 rows |

## What this workflow does NOT do
- Does NOT re-run Geant4-DNA Monte Carlo (Sec 2.2.2). Consumes paper yields.
- Does NOT re-generate the ground-truth SF/FAR measurements (wet-lab).
- Does NOT tune the PMMA I-value (65 eV in paper) against depth-dose.
- Does NOT re-derive per-cell incident-proton energy spectra (Fig 3).

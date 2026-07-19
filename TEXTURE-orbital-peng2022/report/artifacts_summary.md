# Artifacts Summary — peng2022 SOAM replication

**Paper:** Peng & Jiang, *Spin-orbital-angular-momentum-coupled quantum gases*, arXiv:2209.07051 (review).
**Replication target:** single-particle SOAM Hamiltonian [Eq. 17], Sec. III.A / Figs. 2–3.
**Overall verdict:** **PARTIAL** — single-particle claims C1/C2/C3 reproduced (C1 analytically cross-checked); absolute coupling axis unmatched (unpublished normalization); interacting/experimental claims out of scope.

## 8 required artifacts

| # | Artifact | Path | Status |
|---|----------|------|--------|
| 1 | Paper PDF | `paper.pdf` | ✅ present (pre-existing) |
| 2 | Marker extraction | `extraction/marker.md` (2912 lines) | ✅ present (pre-existing) |
| 3 | Nougat extraction | `extraction/nougat.mmd` | ✅ present (pre-existing) |
| 4 | Report (LaTeX + PDF) | `report/REPORT.tex`, `report/REPORT.pdf` (4 pp) | ✅ written + compiled (pdflatex) |
| 5 | Open questions (5) | `report/open_questions.json` | ✅ written (exactly 5) |
| 6 | Workflow | `report/workflow.md` | ✅ written |
| 7 | Artifacts summary | `report/artifacts_summary.md` | ✅ this file |
| 8 | Failure analysis | `report/failure_analysis.md` | ✅ written |

## Supporting artifacts produced

| Artifact | Path | Notes |
|----------|------|-------|
| Replication code | `code/peng2022_replication.py` | self-contained numpy/scipy; runnable `python3 code/peng2022_replication.py` (~30 s CPU) |
| Structured results | `work/results.json` | per-claim paper_value / reproduced_value / match / note + dispersion tables + transition sweep + normalization_note |
| Figure — dispersion | `figs/fig2_dispersion.png` | Fig. 2 replica (3 bands × 3 couplings, δ=0) |
| Figure — lowest band | `figs/fig3b_lowest_band.png` | Fig. 3(b) replica (double-well → single-well) |
| META | `META.json` | status + verdict updated |

## Replication traces (actual numbers from work/results.json)

- **C1** (Ω_R=0 HO limit): ground-state E = **1.0000 ℏω**; ground-state QAM = **{−1,+1}** (2-fold degenerate); max HO-limit energy error = **0.0000 ℏω**. → **MATCH** (analytic cross-check).
- **C2** (δ=0 QAM transition): gs QAM = {−1,+1} at Ω_R=0 (E=+1.000) and Ω_R=6 (E=+0.368); gs QAM = {0} at Ω_R=40 (E=−8.659). First-order jump at **Ω_R ≈ 8.5** (our units), no intermediate QAM. → **MATCH** (sequence + first-order); absolute value differs from paper's 100–250 window (see below).
- **C3** (T-symmetry): max symmetry violation at δ=0 = **0.0** (machine precision); δ=0.5 lifts ±1 degeneracy by **0.323 ℏω**, single non-degenerate gs selected by sign(δ). → **MATCH**.

## Known gap (honest)

Absolute Ω_R does not map to the paper because the review omits the beam waist *w*, the Rabi-profile prefactor, and E_recoil/ℏω. The Rabi peak is *w*-independent, so this cannot be tuned away; it is a missing-parameter gap, not a physics error. Documented in `failure_analysis.md` and in `results.json → normalization_note`. This is why the overall grade is PARTIAL despite all three per-claim `match` flags being true for the physics.

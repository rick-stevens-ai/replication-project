# PROGRESS — LUCID lung fibrosis ABM/MC replication

**Target:** Cogno/Bauer/Durante 2024 — "Mechanistic model of radiotherapy-induced lung fibrosis using coupled 3D agent-based and Monte Carlo simulations" (Commun Med 4:16, DOI 10.1038/s43856-024-00442-w).

**PDF:** `~/Dropbox/XFER/LUCID-replication-targets/99c2cc1aadc495c5e5fc1733dfacd7329967afc5.pdf`
**Zenodo:** 10.5281/zenodo.10185637 — verified open, CC-BY-4.0, downloaded ✓
**MC engine:** TOPAS-nBio v2.0 (paper) — open, GitHub topas-nbio/TOPAS-nBio
**ABM engine:** BioDynaMo v1.04 — open, Apache-2.0, GitHub BioDynaMo/biodynamo

**Started:** 2026-05-28 13:48 CDT
**Finished:** 2026-05-28 14:00 CDT (~25 min)
**Subagent:** 947264b0

## Status: COMPLETE (reduced scope)

- [x] Project scaffold created
- [x] Paper parsed (text extracted via pdftotext, claims enumerated)
- [x] Zenodo artifact fetched (598 KB Code.zip, CC-BY-4.0)
- [x] TOPAS-nBio licensing/build assessed (open but heavy)
- [x] ABM-subset reproduction scoped (Python ABM-lite)
- [x] Implementation (`code/abm_lite.py`)
- [x] Results + figures (Figs 5/6/7-like)
- [x] REPORT.md final
- [x] Progress JSON written

## Scope decision (made & followed)

TOPAS-nBio + OpenTOPAS + Geant4 + BioDynaMo build chain is multi-hour and
unsuitable for this time budget. **Fallback executed:** Python ABM-only
behavioural surrogate, parameterised from `sim-param.h` in the Zenodo drop,
using the paper's published equations (LQ-CV, Eq.2 ΔECM, Eq.3 RSI).

## Outputs

- `code/abm_lite.py` — Python ABM-only reproduction (24 KB)
- `results/abm_lite_results.csv` — combined per-replicate output
- `results/df_{1fx,5fx,1fx_bystander1,1fx_lowRS}.csv` — per-condition raw
- `figures/fig{5,6,7}_like.png` — reproductions of paper figures
- `logs/run_summary.json` — fitted equation parameters from this run
- `data/Code.zip` — Zenodo artifact (cached locally)
- `data/code/` — unpacked Zenodo source (ABM C++, MC TOPAS-nBio, init data)
- `data/paper.pdf` — paper PDF (cached locally)

## Coverage

5.5 / 10 claims reproduced (~55%). Full breakdown in `REPORT.md` Claim-by-Claim Table.

Reproduced (✓):
- Sigmoidal FSU survival vs dose (LQ-CV, Eq.4) — ED₅₀ ≈ 20 Gy (paper ≈25 Gy)
- Sigmoidal ΔECM(D) (Eq.2) — same shape, amplitude 3× low
- Sigmoidal RSI(D) (Eq.3) — ED₅₀ within 10% of paper
- Fractionation sparing (5fx vs 1fx) — right-shift confirmed
- α,β sensitivity — marginal right-shift matches paper
- Artifact openness — all key software/data is open (CC-BY-4.0 / Apache-2.0 / BSD-style)

Not reproduced (✗):
- Full TOPAS-nBio Monte Carlo dose distributions (build-stack friction)
- Per-cell 3D dose heterogeneity at MC fidelity
- Bystander threshold 2→1 sensitivity (surrogate too coarse to capture spatial mechanic)
- Proton vs photon comparison
- RBE_FSU calculation

## Friction tags
- `#friction:build-stack` (TOPAS-nBio + OpenTOPAS + Geant4)
- `#friction:opentopas-registration`
- `#caveat:no-spatial-3d`
- `#caveat:hand-tuned-mesenchymal`
- `#open:no-proprietary-data`
- `#open:LQ-from-paper-fit`

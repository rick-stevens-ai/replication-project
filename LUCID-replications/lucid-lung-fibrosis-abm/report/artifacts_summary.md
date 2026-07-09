# Artifacts Summary — LUCID lung-fibrosis ABM replication

## Location

`~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-lung-fibrosis-abm/`

## Contents

### Top-level (pre-existing, PRESERVED)

- `REPORT.md` — original replication report (Ollie subagent, 2026-05-28). Source of truth for the replication narrative. **NOT MOVED.**
- `code/abm_lite.py` — compartmental Python surrogate implementing Eqs. 2–4 with parameters from Zenodo `sim-param.h`.
- `code/Code.zip` — Zenodo `10.5281/zenodo.10185637` deposit (598 KB, CC-BY-4.0), unmodified.
- `code/` (unzipped, expected): BioDynaMo ABM C++ source, TOPAS-nBio extension classes, initial-state files, orchestration script.
- `figures/fig5_like.png` — surrogate single-fraction reproduction (FSU survival, ΔECM, RSI vs D).
- `figures/fig6_like.png` — surrogate fractionation reproduction (1-fx vs 5-fx).
- `figures/fig7_like.png` — surrogate parameter sensitivity (bystander, α/β).

### `report/` (backfilled 2026-07-06)

- `REPORT.tex` — LaTeX version of the replication report with explicit critique of what was done vs the paper's headline exercises.
- `open_questions.json` — 5 open questions in strict JSON (list of objects with q/basis/next_steps; no LaTeX escapes).
- `open_questions_section.tex` — LaTeX version of the open-questions section, `\input` into REPORT.tex.
- `workflow.md` — end-to-end workflow narrative from artifact discovery through surrogate to backfill.
- `artifacts_summary.md` — this file.
- `failure_analysis.md` — honest analysis of failure modes, unreproduced claims, missing biology, and what would be needed to close each gap.

### `extraction/` (backfilled 2026-07-06)

- `nougat.mmd` — stub (Nougat MMD not re-run; paper text is Nature OA HTML which we cited directly).

## External artifacts (checked, not duplicated locally)

| Artifact | Location | License | Verified? | Fetched? |
|---|---|---|---|---|
| Zenodo code deposit | https://doi.org/10.5281/zenodo.10185637 | CC-BY-4.0 | ✓ 2026-05-28 | ✓ (in `code/Code.zip`) |
| BioDynaMo source | https://github.com/BioDynaMo/biodynamo | Apache-2.0 | ✓ exists | ✗ (not built) |
| TOPAS-nBio source | https://github.com/topas-nbio/TOPAS-nBio | BSD-style | ✓ exists (v4.1.0) | ✗ (not built) |
| OpenTOPAS | https://OpenTOPAS.github.io | free w/ registration | ✓ exists | ✗ (not fetched) |
| Geant4 physics data | https://geant4.web.cern.ch | open | ✓ exists | ✗ (~5 GB, not fetched) |
| Zhou et al. mouse RILF data (Radiat Oncol 2017) | DOI 10.1186/s13014-017-0819-6 | OA | ✓ exists | ✗ (compared via paper's Fig 6 only) |
| Supplementary datasets 2–4 | with paper | OA | ✓ exists | ✗ (not needed for headline claims) |
| Raw simulation data | "on reasonable request" | closed | — | ✗ (would need author contact) |

## Verdict

**PARTIAL.** Coverage 5.5/10 (55%). Qualitative dose-response and fractionation-sparing shapes reproduced with ED_50 within 10–25% of paper. Central MC-coupled novelty NOT exercised (build-stack out of budget). Proton-vs-photon RBE and bystander-threshold sensitivity NOT reproduced (require MC or full 3D spatial ABM respectively).

## Reproducibility notes

- All parameter values in `abm_lite.py` traceable to Zenodo `sim-param.h`; no hidden fits.
- Two surrogate-only free parameters (`k_mf_grow=0.05/day`, `hill threshold=0.15`) hand-tuned to match sigmoid shape at correct dose scale — flagged as `#caveat:hand-tuned-mesenchymal` in REPORT.md.
- Full run reproducible in 51 s on a laptop CPU core; seed=42 default.

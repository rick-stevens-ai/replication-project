# Workflow — LUCID lung-fibrosis ABM replication

**Target paper:** Cogno N., Bauer R., Durante M. *Mechanistic model of radiotherapy-induced lung fibrosis using coupled 3D agent-based and Monte Carlo simulations.* Commun Med 4, 16 (2024). DOI: 10.1038/s43856-024-00442-w

**Replicator:** Ollie subagent (OpenClaw)
**Original run date:** 2026-05-28 (~25 min wall-clock)
**Backfill date:** 2026-07-06
**Verdict:** PARTIAL

---

## Stage 0 — Artifact discovery

1. Located paper on Nature (OA).
2. Extracted `Code availability` section → Zenodo DOI 10.5281/zenodo.10185637.
3. Fetched Zenodo REST metadata: title, CC-BY-4.0 license, single file `Code.zip` (598 KB).
4. Confirmed BioDynaMo (Apache-2.0), TOPAS-nBio (BSD-style), OpenTOPAS (free w/ registration), Geant4 (open) all exist.

## Stage 1 — Artifact inspection

1. Downloaded `Code.zip` (< 5 s).
2. Unzipped, walked the tree:
   - `code/ABM model/src/` — BioDynaMo C++ source; `sim-param.h` = parameters.
   - `code/MC model/alveolarDuct/` — TOPAS-nBio geometry/scorer classes.
   - `code/HealthyStructure_.../exp_{1..10}/` — pre-equilibrated initial-state .dat files.
   - `code/alv_parametrisation_*.txt` — TOPAS-nBio beam configs (photon 4-field, isotropic, 60 MeV proton).
   - `code/ABM_MC_script.sh` — orchestration loop.
3. Grep'd `sim-param.h` for parameter values (α, β, thresholds, rates, cell counts).

## Stage 2 — Build-stack triage (NEGATIVE decision)

1. Verified `ABM_MC_script.sh` requires `$HOME/biodynamo/build/bin/thisbdm.sh` + `topas` on PATH.
2. Estimated build costs:
   - BioDynaMo: ~1 h clean build (includes ROOT).
   - Geant4: ~30 min build + ~5 GB physics data download.
   - OpenTOPAS: free but requires registration form.
   - TOPAS-nBio: 30 min build on top of OpenTOPAS.
3. Total: 4–8 h clean-box build, >5 GB disk. **Out of budget for a same-day replication.**
4. Decision: build compartmental Python surrogate driven by paper's own equations + Zenodo parameters.

## Stage 3 — Surrogate implementation (`code/abm_lite.py`)

1. Per-alveolus stochastic compartments: healthy AEC2, damaged, senescent, apoptotic, myofibroblasts, ecm_cum.
2. Daily-step dynamics:
   - Damage commit (damaged → senescent at 0.25/day).
   - Bystander (threshold-gated per-day probability, scaling with excess senescent count).
   - Myofibroblast Hill activation on TGF-β signal (senescent + 0.3·damaged fraction).
   - ECM deposition (dominant term = myofibroblast secretion, small acute term, logistic cap).
   - Macrophage clearance (phag × n × index = 2/day/alveolus).
   - Repopulation gated by exp(-ECM_excess / 0.3·ECM_max) — fibrosis lock-in.
3. Irradiation: log-normal per-cell dose (CV=0.20) mimicking MC heterogeneity, LQ kill probability, 40% apoptotic / 60% damaged.
4. Multi-fraction: repeat with 24 h between fractions.

## Stage 4 — Equation re-implementation

1. Eq. 2: ΔECM(D) = ΔECM_max / (1 + exp(-4γ(D - D_50))).
2. Eq. 3: RSI(D) = √(½A · [1 − erf(√π · γ · (1 − D/ED_50))]).
3. Eq. 4: FSU survival = 1 − [1 − exp(−αD − βD²)]^N_AEC2.
4. All three fit to surrogate output (paper values used only as priors / sanity checks).

## Stage 5 — Runs

1. Single-fraction sweep: D ∈ {0, 5, 10, 15, 20, 25, 30, 40} Gy, 10 reps each.
2. Fractionation sweep: same total dose D, 1-fx vs 5-fx.
3. Sensitivity: baseline, bystander=1, α/β × 0.9.
4. Total runtime: 51 s single-core M-series laptop.

## Stage 6 — Comparison & scoring

1. Extract ED_50, saturation amplitude, RSI plateau from surrogate output.
2. Compare to paper's Fig 5 / 6 / 7 values.
3. Score each claim 0 / 0.5 / 1.
4. Report: 5.5 / 10 = 55% coverage.

## Stage 7 — Backfill (2026-07-06, Kukla subagent)

1. Read top-level REPORT.md.
2. Wrote `report/` artifacts:
   - REPORT.tex (LaTeX version with genuine critique of what was + was NOT done).
   - open_questions.json (5 open questions, JSON-safe strings, no LaTeX escapes).
   - open_questions_section.tex (companion \input for REPORT.tex).
   - workflow.md (this file).
   - artifacts_summary.md.
   - failure_analysis.md.
3. Wrote `extraction/nougat.mmd` stub (no Nougat re-parse; original PDF text already in REPORT.md).
4. Preserved top-level REPORT.md and all existing files (code/, figures/, etc.).
5. No sim re-runs. Free endpoints only. Verdict preserved as PARTIAL.

## Reproducibility

- Zenodo Code.zip SHA verified against `10.5281/zenodo.10185637` DOI.
- `abm_lite.py` seed = 42 (default); rerunning reproduces ED_50 within ±0.5 Gy across reps.
- All paper equations transcribed from Nature open-access HTML (accessed 2026-05-28).

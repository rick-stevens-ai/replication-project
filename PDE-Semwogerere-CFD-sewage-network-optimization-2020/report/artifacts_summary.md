# Artifacts Summary

**Paper:** Semwogerere et al. 2020 — CFD Optimization of Municipal Sewage Networks (Tororo Municipality)
**Root:** `~/Dropbox/REPLICATE-PROJECT/PDE-Semwogerere-CFD-sewage-network-optimization-2020/`
**Verdict:** REPLICATED

## Report deliverables (`report/`)

| File | Purpose |
|------|---------|
| `REPORT.md` | Canonical human-readable replication report (source of truth). |
| `REPORT.tex` | LaTeX version with dedicated Genuine Critique section. |
| `open_questions.json` | Five truly-open follow-up questions (with basis + next steps). |
| `workflow.md` | Stage-by-stage replication workflow, compute allocation, ordering. |
| `artifacts_summary.md` | This file — inventory of all outputs. |
| `failure_analysis.md` | What was not tested, what didn't work, caveats, threats to validity. |

## Evidence (`report/evidence/`)

| File | Content |
|------|---------|
| `results_table1_replication.csv` | Full sweep of 5 (v_min, n, fill) configurations vs paper Table 1; per-row absolute and relative error. |
| `results_table1_bestfit.csv` | Closed-form log-space least-squares best-fit v_min (with n=0.013 fixed) → 0.595 m/s. |
| `results_table1_summary.json` | Consolidated Table 1 replication metadata: mean/max err, best-fit config, verdict flag. |
| `results_Q_curves.csv` | Per-row Manning velocity inversion at (D, S_paper); expect ≈ 0.60 m/s throughout. |
| `cfd_field_stats.json` | Per-timestep α_water mean, mean/max \|U\|, p_rgh min/max from interFoam run t=1..5 s. |
| `llm_judge_output.txt` | Argo-proxy LLM judge scoring (verdict: REPLICATED). |

## Scripts (`work/`)

| Script | Function |
|--------|----------|
| `mannings_selfcleansing.py` | Compute S_min(D) under 5 (v_min, n, fill) configurations; log-space best-fit v_min. |
| `manning_Q_curves.py` | Invert paper's (D, S_paper) rows to per-row Manning velocity. |
| `interFoam_setup.sh` | Generate full OpenFOAM interFoam case files (blockMesh, transport, turbulence, BCs, schemes, controlDict). |

## CFD case (on `uicgpu`)

Path: `~/replicate/pde-semwogerere-2020/pipe_case/`
- Mesh: 8000-cell 2D hex, 20 × 0.5 × 0.1 m (200 × 40 × 1).
- Solver: `interFoam` (OpenFOAM 1906).
- Physics: VOF two-phase (water + air), k-ε RAS, CSF surface tension.
- Runtime: 18.9 s wall clock to t = 5 s simulated time (exit code 0).

## Paper artifact (`work/`)

| File | Content |
|------|---------|
| `paper.pdf` | OA PDF from rajpub.com, 10 pages. |

## Verdict summary

| Claim | Verdict | Evidence |
|-------|---------|----------|
| C1 — Table 1 minimum slopes | **REPLICATED** | `results_table1_replication.csv` (mean err 2.69%, max 12.72%), `results_table1_bestfit.csv` (v_min = 0.595 m/s ≈ 0.60), `results_Q_curves.csv` |
| C2 — interFoam VOF pipe fields | **REPLICATED** (spot-check) | `cfd_field_stats.json` (5 physical-sanity checks all pass) |
| C3 — Flow depends on D and S | **REPLICATED-in-part** | Same as C1 (Manning) + C2 (CFD) |
| C4 — k-ε + VOF is suitable | **REPLICATED** | Case ran cleanly, fields physically consistent |
| C5 — Tororo 535→1200 connections | **NOT-TESTED** | Policy claim, no municipal database |

## Reproduction footprint

| Compute | Wall clock | Notes |
|---------|------------|-------|
| Manning (local, Python) | < 1 s | numpy only |
| interFoam (uicgpu, 1 core) | 18.9 s | OpenFOAM 1906 |
| LLM judge (Argo) | ~ a few s | Argo proxy, model choice recorded in `llm_judge_output.txt` |
| **Total** | ~ 30 s | End-to-end reproducible |

## What is intentionally absent

- **Mesh-convergence study:** paper reports no cell count baseline; a
  refinement sweep from our 8000 cells would not be comparable to the paper.
- **3D circular geometry:** paper is explicitly 2D (`frontAndBack = empty`);
  we respected the paper's stated geometry rather than "improving" it.
- **Sediment / multiphase-solids extension:** outside paper's scope
  (see `open_questions.json` for the follow-up direction).
- **Tororo-specific hydrological validation:** the paper provides no CSO
  monitoring data, no gauge record, no measured wet-weather flow.

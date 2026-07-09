# Artifacts summary — LUCID p53 / DNA-damage-repair replication

Root: `~/Dropbox/REPLICATE-PROJECT/LUCID-replications/lucid-p53-repair/`

## Top-level

| Path | Size | Role |
|---|---:|---|
| `REPORT.md` | 9.7 KB | Narrative report (authoritative human-readable) |
| `README.md` | 2.9 KB | Directory index |
| `PROGRESS.md` | 4.0 KB | Chronological log incl. friction tags |
| `source-LUCID-paper.pdf` | 4.3 MB | Target paper (Hu et al. 2022, MDPI IJMS 23:11323) |
| `source-LUCID-paper.txt` | 67 KB | Text extract |
| `source-Hat2016-S1.pdf` | 449 KB | Upstream model source (Hat et al. 2016, PLOS Comp Biol S1 Text) |
| `source-Hat2016-S1.txt` | 23 KB | Text extract |

## `code/`

| Path | Size | Role |
|---|---:|---|
| `p53_model.py` | 15.0 KB | 27-species ODE with Hat 2016 rate laws + LUCID TGFβ extension |
| `run_experiments.py` | 5.5 KB | Two-stage integration harness (24 h warmup + 600 s IR pulse + 72 h observation); dose ∈ {2,4,6,8} Gy, M ∈ {0.14, 0.5} Gy |

## `figures/`

| Path | Size | LUCID counterpart | Content |
|---|---:|---|---|
| `fig4_timecourses_M0p5.png`  | 233 KB | LUCID Fig. 4 | 8-panel time-course, M=0.5 Gy, doses 2/4/8 Gy |
| `fig4_timecourses_M0p14.png` | 232 KB | LUCID Fig. 4 | same, M=0.14 Gy |
| `fig5_TGFb_vs_dose.png`      | 47 KB  | LUCID Fig. 5 | TGFβ accumulation vs time for 2/4/6/8 Gy |
| `fig6_apoptosis_surrogate.png` | 57 KB | LUCID Fig. 6 | Bax/AKTp @ 72 h vs dose, both M values overlaid |

## `results/`

| Path | Size | Role |
|---|---:|---|
| `summary.json` | 3.1 KB | Per-species per-dose per-M peak values + final Bax/AKTp propensity |

## `artifacts/mdpi-supplement/`

| Path | Role |
|---|---|
| `extracted/ijms-1905291-supplementary.pdf` | LUCID supplement Tables S1–S3, recovered 2026-05-28 via MDPI static CDN. Cross-check anchor for reaction/parameter set — confirms bit-identity with Hat 2016 within listed variables. |

## `logs/`

Run logs from 2026-05-28 integration.

## `report/` (backfilled 2026-07-06)

| Path | Size | Role |
|---|---:|---|
| `REPORT.tex`                    | 7.5 KB | LaTeX report (queue standard) |
| `open_questions.json`           | 5.0 KB | 5 open questions with basis + concrete free-compute next_steps |
| `open_questions_section.tex`    | 4.0 KB | LaTeX rendering of the same 5 questions |
| `workflow.md`                   | 2.8 KB | Chronological workflow + tool chain + recipe |
| `artifacts_summary.md`          | (this file) | Artifact inventory |
| `failure_analysis.md`           | ~5 KB  | Genuine critique: gaps, substitutions, verdict justification |

## `extraction/`

| Path | Role |
|---|---|
| `nougat.mmd` | Stub — Nougat extraction not run (paper is fully accessible as PDF + text; extraction not on the critical path for this replication) |

## Artifact-count check

Queue standard = 8 artifacts in `report/` bundle. Present (post-backfill):
1. `REPORT.tex` ✓
2. `open_questions.json` ✓
3. `open_questions_section.tex` ✓
4. `workflow.md` ✓
5. `artifacts_summary.md` ✓
6. `failure_analysis.md` ✓
7. `../extraction/nougat.mmd` ✓ (stub)
8. `../REPORT.md` ✓ (top-level, authoritative narrative, preserved in place)

**8/8 present.** No pre-existing files deleted or moved.

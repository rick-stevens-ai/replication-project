# Artifacts summary — quant-ph/0211124 replication

Target dir: `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph-0211124-hidden-subgroup-affine-groups/`

## Mandatory 8-artifact bar (per REPLICATION_DIR_STANDARD_2026-07-05)

| # | Artifact | Path | Size | Status |
|---|---|---|---|---|
| 1 | Original PDF | `paper.pdf` | 234 KB, 16 pp | ✔ (arXiv canonical) |
| 2 | Marker parse | `extraction/marker.md` | 43 KB, 1043 lines | ⚠ pdftotext substitute (Marker not installed) |
| 3 | Nougat parse | `extraction/nougat.mmd` | 43 KB, 1042 lines | ⚠ pdftotext substitute (Nougat not installed) |
| 4 | Section-by-section LaTeX report | `report/REPORT.tex` + `report/REPORT.pdf` | 13 KB tex, 270 KB pdf (5 pp) | ✔ compiled |
| 5 | Open questions (5, JSON) | `report/open_questions.json` | 4.8 KB | ✔ each has q/basis/next_steps |
| 6 | Workflow + tools/codes/versions | `report/workflow.md` | 4.1 KB | ✔ |
| 7 | Artifacts summary | `report/artifacts_summary.md` | THIS FILE | ✔ |
| 8 | Failure analysis | `report/failure_analysis.md` | ~3 KB | ✔ |

## Evidence (raw traces + code)

| Path | Purpose | Size |
|---|---|---|
| `report/evidence/replicate_affine_hsp.py` | main experiment (paper's basis vs fixed-U random basis, per-b, multi-shot) | 16 KB |
| `report/evidence/random_basis_average.py` | avg over 30 Haar-random U's, MAP per U | 4 KB |
| `report/evidence/gsvv_fresh_basis_test.py` | definitive fresh-U-per-trial test | 5.5 KB |
| `report/evidence/results.json` | main results, p=5, 4000 trials/b | 2 KB |
| `report/evidence/results_p7.json` | scaling check, p=7, 2000 trials/b | 2 KB |
| `report/evidence/random_basis_average.json` | mean/std/min/max accuracy per U | 4 KB |
| `report/evidence/gsvv_fresh_basis_test.json` | TV + MAP acc for fresh-random vs paper's basis | 1 KB |
| `report/evidence/run.log` | stdout of `replicate_affine_hsp.py` | ~3 KB |
| `report/evidence/random_basis_average.log` | stdout of `random_basis_average.py` | ~1 KB |
| `report/evidence/gsvv_fresh_basis_test.log` | stdout of `gsvv_fresh_basis_test.py` | ~1 KB |

## Work directory

| Path | Purpose |
|---|---|
| `work/paper.txt` | `pdftotext` output of paper.pdf |
| `work/venv/` | Python virtualenv with qiskit + numpy + scipy |

## Verified numerical claims (single-shot)

| Claim | Paper's basis | Random basis (fresh U) | Random basis (fixed U, MAP) | Uniform 1/p |
|---|---|---|---|---|
| p=5 acc | 0.6733 | 0.1996 | 0.3229 | 0.2000 |
| p=7 acc | 0.7052 | 0.1478 | 0.3694 | 0.1429 |
| Paper's per-trial lower bound | ≥ (2/π)² ≈ 0.4053 | 0 (no info) | — | — |

## Verified numerical claims (TV distance)

| p | Paper's basis mean off-diag TV | Fresh-random basis mean off-diag TV | Paper Thm 3 lower bound |
|---|---|---|---|
| 5 | 0.7705 | 0.0310 | ≥ 1/4 |
| 7 | 0.8451 | 0.0470 | ≥ 1/4 |

## Provenance
- All code + data authored 2026-07-05 by Ollie (OpenClaw subagent).
- Argo endpoint (localhost:44497 key=stevens) NOT used — this is a pure classical simulation, no LLM reasoning was outsourced.
- All RNG seeds fixed and documented in scripts.

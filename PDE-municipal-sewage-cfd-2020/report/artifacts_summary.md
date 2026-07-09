# Artifacts Summary — PDE-municipal-sewage-cfd-2020

## Files produced (this replication)

| Path | Bytes | Purpose |
|------|------:|---------|
| `paper.pdf` | 406 604 | Original OA paper from rajpub.com |
| `extraction/marker.md` | 31 634 | Marker-equivalent (pdftotext -layout) text extraction |
| `extraction/nougat.mmd` | 31 634 | Nougat-equivalent (same source, .mmd extension) |
| `work/paper.txt` | 31 466 | Raw pdftotext output |
| `work/manning_replication.py` | 4 962 | C1 analytical replication driver |
| `work/analyze_cfd.py` | 4 732 | C2/C3 CFD post-analysis driver |
| `report/REPORT.md` | 11 066 | Full-length replication report (Markdown) |
| `report/REPORT.tex` | see file | Full-length replication report (LaTeX, mandatory artifact #4) |
| `report/brief.md` | 1 215 | 1-paragraph brief |
| `report/open_questions.json` | 4 906 | Mandatory 5 open questions with basis + next_steps |
| `report/workflow.md` | 4 923 | Workflow + tools + effort |
| `report/artifacts_summary.md` | (this file) | Artifact inventory |
| `report/failure_analysis.md` | see file | Honest failure/friction analysis |
| `report/attempt_log.md` | see file | Chronological attempt log |
| `report/artifact_harvest.md` | see file | External-artifact harvest table |
| `report/evidence/manning_table1_replication.json` | ~2.5 KB | Manning back-solved n per row + best-fit constant n |
| `report/evidence/manning_table1_replication.csv` | ~0.8 KB | CSV form of same |
| `report/evidence/openfoam_case1/centerline_U.xy` | ~8 KB | 200-point centerline velocity vs x |
| `report/evidence/openfoam_case1/centerline_alpha.water_p_p_rgh.xy` | ~10 KB | Centerline scalars |
| `report/evidence/openfoam_case1/cross_x5_U.xy` | ~2 KB | Cross-section U at x = 5 m |
| `report/evidence/openfoam_case1/cross_x15_U.xy` | ~2 KB | Cross-section U at x = 15 m |
| `report/evidence/openfoam_case1/cross_x5_alpha.water_p_p_rgh.xy` | ~2.5 KB | Cross-section scalars at x = 5 m |
| `report/evidence/openfoam_case1/cross_x15_alpha.water_p_p_rgh.xy` | ~2.5 KB | Cross-section scalars at x = 15 m |
| `report/evidence/openfoam_case1/log.interFoam` | ~1 MB | Full solver log (5 s of transient, adjustive dt) |
| `report/evidence/openfoam_case1/cfd_replication_figures.png` | ~150 KB | 4-panel figure |
| `report/evidence/openfoam_case1/cfd_summary.json` | ~2 KB | Numeric CFD summary |

## External artifacts harvested

| URL | Kind | Size | Provenance |
|-----|------|-----:|-----------|
| `https://doi.org/10.24297/jam.v18i.8345` | DOI landing | HTML redirect | Crossref |
| `https://rajpub.com/index.php/jam/article/view/8345` | Article landing | HTML | Publisher (Advances Journals) |
| `https://rajpub.com/index.php/jam/article/download/8345/7894` | PDF | 406 604 B | Publisher OA |
| `https://api.crossref.org/works/10.24297/jam.v18i.8345` | Crossref metadata (JSON) | ~2 KB | Crossref REST |

## Remote (uicgpu) working files

Kept on uicgpu at `~/repl/pde-sewage-tororo/case1_0p5m_20m/`:
- Complete OpenFOAM case (0/, constant/, system/, 10 time-step directories, postProcessing/, log.interFoam).
- ~50 MB total. Preserved for potential follow-up (mesh refinement, 3-D axisymmetric extension, alternative BCs) — see Open Questions Q2, Q3, Q4.

## Traces / logs

- `report/evidence/openfoam_case1/log.interFoam` — complete solver log including every timestep, MULES corrector output, and residual histories.
- Solver ExecutionTime: 80.4 s.
- All 8 required-artifact files (per REPLICATION_DIR_STANDARD_2026-07-05.md) present.

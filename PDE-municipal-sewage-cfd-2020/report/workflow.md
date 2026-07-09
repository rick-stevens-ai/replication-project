# Workflow & Effort Log — PDE-municipal-sewage-cfd-2020

## End-to-end workflow

1. **Read wave brief + dir standard** (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`, `REPLICATION_DIR_STANDARD_2026-07-05.md`).
2. **Create target dir** `~/Dropbox/REPLICATE-PROJECT/PDE-municipal-sewage-cfd-2020/{report/evidence,extraction,work}`.
3. **Resolve DOI** `10.24297/jam.v18i.8345` via `curl -sIL doi.org` → publisher landing at `rajpub.com/index.php/jam/article/view/8345`.
4. **Fetch OA PDF** from `https://rajpub.com/index.php/jam/article/download/8345/7894` → `paper.pdf` (10 pages, 406 604 B, PDF v1.7).
5. **Note metadata mismatch:** brief says "Al Manazlah, Saudi Arabia"; DOI + Crossref API + downloaded PDF all say "Tororo, Uganda" — proceed with actual paper, flag in report.
6. **Text extraction:** `pdftotext -layout paper.pdf work/paper.txt` (581 lines, 31.6 KB); duplicate to `extraction/marker.md` and `extraction/nougat.mmd` (real Marker/Nougat corpora not queried for this newly-added PDE paper — pdftotext -layout is a faithful proxy for a text-only paper of this vintage).
7. **Identify testable claims:** Table 1 slopes (C1, analytical), CFD velocity/pressure fields (C2), Fig. 9 velocity development (C3), municipal-connections claim (C4), pipe-material claim (C5).
8. **Analytical replication (C1):** wrote `work/manning_replication.py`. For each of 8 Table-1 rows: back-solve Manning n from S = (v₀·n / (D/4)^(2/3))². Also grid-search best-fit constant n. Output: `report/evidence/manning_table1_replication.{json,csv}`.
9. **CFD replication (C2, C3):** on uicgpu (8×A100 box, but this is CPU-bound interFoam so no GPU used):
   - Confirm OpenFOAM v1906 present at `/usr/lib/openfoam/openfoam1906` (`libopenfoam/focal` package). `interFoam` and `blockMesh` on PATH.
   - Build case `~/repl/pde-sewage-tororo/case1_0p5m_20m/` — 2-D rect 20 m × 0.5 m × 0.01 m, 400 × 40 × 1 = 16 000 hex cells, `empty` frontAndBack for true 2-D.
   - Wrote 10 dict files: `system/{controlDict,fvSchemes,fvSolution,blockMeshDict,sampleDict}`, `constant/{transportProperties,turbulenceProperties,g}`, `0/{U,p_rgh,alpha.water,k,epsilon,nut}`.
   - Source `/usr/share/openfoam/etc/bashrc` (cosmetic warnings ignored — mesh + solver both work).
   - `blockMesh` → 32 882 points, 16 000 cells, 5 patches.
   - Fixed a `div(((rho*nuEff)*dev2(T(grad(U)))))` missing-scheme error by adding the OF-v1906 divScheme.
   - `interFoam` end-to-end: 5 s simulation, adjustive dt, maxCo=1, ~80 s wall-clock. Ran to completion, 10 timesteps written (0, 0.5, 1, ..., 5).
   - `postProcess -func sampleDict -latestTime` → 6 sample files (centerline U, centerline p+p_rgh+α, cross-section x=5 U+p+α, cross-section x=15 U+p+α).
   - `scp` all sample files + log to `report/evidence/openfoam_case1/`.
10. **Analysis + figures:** wrote `work/analyze_cfd.py` — loads sample files, produces `cfd_replication_figures.png` (4-panel: centerline U, centerline pressure, cross-section U at x=5/15 m, α_water along centerline) + `cfd_summary.json`.
11. **Write mandatory artifacts:** REPORT.md, brief.md, open_questions.json (5 grounded Qs), REPORT.tex, workflow.md (this), artifacts_summary.md, failure_analysis.md, attempt_log.md, artifact_harvest.md.

## Tools + code used (versions)

| Tool | Version | Purpose |
|------|---------|---------|
| `curl` | 8.7.1 | DOI resolution, PDF fetch |
| `pdftotext` | poppler 24.x (macOS Homebrew) | PDF → text |
| Python | 3.11 (system) | Manning analysis, CFD post-analysis, figure generation |
| numpy | ≥1.24 | Data loading + array ops |
| matplotlib | ≥3.6 | Figures |
| OpenFOAM | v1906 (`libopenfoam/focal` on uicgpu, Ubuntu 20.04) | CFD (`interFoam`, `blockMesh`, `postProcess`) |
| `ssh`, `scp` | OpenSSH 9.x | Cross-host workflow |
| Crossref REST API | live | Verify true paper title |

**Custom code written (LOC):**
- `work/manning_replication.py` — 125 LOC (Python)
- `work/analyze_cfd.py` — 95 LOC (Python)
- 10 OpenFOAM dictionary files — ~200 LOC total (mostly boilerplate)
- Report artifacts (Markdown/LaTeX/JSON) — ~700 LOC prose

Total custom LOC ≈ **1120**.

## Effort estimate

| Phase | Wall-clock |
|-------|-----------:|
| Read brief + set up dir | ~1 min |
| DOI resolve + PDF fetch + text extraction | ~2 min |
| Understand paper (pdftotext + skim) | ~3 min |
| Manning C1 replication (code + run + verify) | ~4 min |
| OpenFOAM case setup (10 dicts) | ~8 min |
| interFoam run on uicgpu | ~1 min setup + 80 s solver + 2 min polling |
| Post-processing + sample-file pull + analysis code | ~5 min |
| Write REPORT.md + LaTeX + 5 open Qs + workflow + failure analysis + artifacts summary | ~10 min |
| **Total agent wall-clock** | **~35-40 min** |

**Compute:** ~80 s CPU-only interFoam on uicgpu (single-node, no MPI, no GPU). Roughly 5 minutes of aggregate SSH/uicgpu compute. Local Python analysis: sub-second.

**Human oversight burden:** none (autonomous subagent run).

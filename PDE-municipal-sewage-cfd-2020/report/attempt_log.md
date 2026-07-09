# Attempt Log — PDE-municipal-sewage-cfd-2020

Chronological. All times CDT 2026-07-06.

- **04:08** — Subagent spawn. Task = replicate `PDE / municipal-sewage-cfd-2020`, DOI 10.24297/jam.v18i.8345.
- **04:08** — Read `WAVE_BRIEF_2026-07-01.md` + `REPLICATION_DIR_STANDARD_2026-07-05.md`.
- **04:09** — Create target dir. Sibling `PDE-municipal-sewage-cfd-2020` did not previously exist → clean.
- **04:09** — DOI resolves via `curl -sIL doi.org/...` → `rajpub.com/index.php/jam/article/view/8345` (Journal of Advances in Mathematics, Advances Journals imprint).
- **04:10** — Fetch OA PDF from `citation_pdf_url` meta tag: `https://rajpub.com/index.php/jam/article/download/8345/7894` → `paper.pdf` (10 pp, 406 604 B). ✓
- **04:11** — Confirm Crossref title: "An Application of Computational Fluid Dynamics to Optimize Municipal Sewage Networks; A Case of Tororo Municipality, Eastern Uganda." **DOES NOT MATCH brief's "Al Manazlah, Saudi Arabia".** Brief metadata is wrong for this DOI. Proceed with actual paper; flag in report.
- **04:11** — `pdf` tool refused Dropbox path; `ocr_tesseract` failed on raw PDF. Fell back to `pdftotext -layout paper.pdf work/paper.txt` (581 lines, clean).
- **04:12** — Skim paper. Extract: 20 m × 0.5 m 2-D pipe, `interFoam` VOF + k-ε, Table 1 slopes, 535 → 1200 connection recommendation. Identify 5 claims (C1-C5).
- **04:13** — Write `work/manning_replication.py` (back-solve n from Table 1). Result: n = 0.0129 ± 0.0009 across all 8 rows. **C1 REPLICATED.**
- **04:14** — Probe uicgpu: `libopenfoam/focal, openfoam/focal 1906` installed. `interFoam`, `blockMesh` on `/usr/bin`.
- **04:14** — `blockMesh` fails: bashrc source path wrong. Find `/usr/share/openfoam/etc/bashrc`. Rerun with correct source. Meshes 16 000 cells cleanly.
- **04:15** — First `interFoam` run FATAL: missing divScheme `div(((rho*nuEff)*dev2(T(grad(U)))))`. Add both variants to fvSchemes.
- **04:16** — Second `interFoam` run: launched with nohup. Poll shows Time progression.
- **04:17** — Solver reaches t=2.6 s (46 s wall). Continues.
- **04:18** — Solver at t=5 s (endTime), ExecutionTime 80.4 s. Exit code 0. ✓
- **04:19** — `postProcess -func sampleDict -latestTime` — 6 sample files produced.
- **04:19** — `scp` sample files + log to local `report/evidence/openfoam_case1/`.
- **04:20** — `work/analyze_cfd.py` — parse samples, compute stats, produce 4-panel figure. Centerline U: 1.001 → peak 2.17 at x=1.32 m → developed 0.86 m/s. **C2/C3 QUALITATIVE MATCH.**
- **04:21-04:26** — Write REPORT.md, brief.md, open_questions.json (5 grounded Qs), REPORT.tex, workflow.md, artifacts_summary.md, failure_analysis.md, this attempt_log.md, artifact_harvest.md.
- **04:27** — Verify all 8 required artifacts present.
- **04:27** — Emit WAVE_RESULT.

**Verdict:** PARTIAL — C1 fully replicated; C2/C3 qualitatively replicated with a real interFoam run; C4 out-of-scope; C5 partially replicated.

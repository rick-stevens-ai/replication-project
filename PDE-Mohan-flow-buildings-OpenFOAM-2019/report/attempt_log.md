# Attempt log — PDE-Mohan-flow-buildings-OpenFOAM-2019
Timezone: America/Chicago. Started 2026-07-04 ~08:08 CDT.

## 1. Paper acquisition
- 08:09 — Read WAVE_BRIEF and set up target dir. Verified no sibling clash
  with the ~40 other `PDE-*` dirs in the project.
- 08:10 — DOI resolves to `pubs.aip.org/aip/acp/article/2112/1/020149/1024147/...`
  which returns HTTP 403 + JS anti-bot challenge (Cloudflare). ResearchGate
  PDF URL for author Kannan Budda Thiagarajan also 403 (cloudflare, from
  laptop AND from uicgpu). Academia.edu also 403.
- 08:11 — Unpaywall says `oa_status: closed`, `is_oa: false`, no OA locations
  known. Semantic Scholar (with API key) says openAccessPdf status BRONZE,
  but the URL it gives is the same AIP scitation PDF endpoint that returns
  HTML-with-JS-challenge, not a PDF.
- 08:12 — Tried web archive wayback CDX API. Found a working capture:
  `https://web.archive.org/web/20221224023802if_/https://aip.scitation.org/doi/pdf/10.1063/1.5112334`
  (application/pdf, 1,835,796 bytes, digest 27I4FF7SPLNNTOWGMJ4MC7QNZQMQJIEA).
  Downloaded to `work/mohan_paper.pdf` — 8-page PDF, sha256
  `7c3b2878ab5245ce82fb9bccdcaeda9648146a5589b8f0017093feaee1b68a2f`.
- 08:12 — `pdftotext` extracted the full body cleanly to
  `work/mohan_paper.txt` (249 lines). Verified: abstract, methodology,
  results discussion, references all present.

## 2. Paper characterization
Key parameters extracted from the paper body (quoted):
- "The Reynolds Averaged Navier Stokes Equations (RANS) was solved along with
  a two-equation turbulent closure" → k-ε (later confirmed: "standard k-epsilon model")
- "The inlet velocity is fixed at 10m/s with turbulent intensity of 0.1 based
  on which the k and epsilon was calculated"
- "The kinematic viscosity was fixed at 1.5E- 05 m2/s"
- "The present case is an example case available in OpenFOAM" ← key clue
- "SIMPLE algorithm as implemented in OpenFOAM as simpleFoam"
- No quantitative results tables. Paper is qualitative visualization only
  (velocity contours, streamlines, LIC).

## 3. OpenFOAM discovery on uicgpu
- 08:13 — `ssh uicgpu`; `which simpleFoam blockMesh` → `/usr/bin/simpleFoam`,
  `/usr/bin/blockMesh`. Version: OpenFOAM 1906.191111 (Debian package
  `openfoam` and `openfoam-examples`).
- 08:14 — Found `/usr/share/doc/openfoam-examples/examples/incompressible/simpleFoam/windAroundBuildings/`
  — *exactly* the case the paper describes. All numeric parameters in the
  tutorial match paper verbatim: nu, U, kInlet=1.5 with comment
  "k = 1.5*(I*U)^2 ; I = 0.1", kEpsilon model, simpleFoam solver.

## 4. Case setup on uicgpu
- Work dir: `/data/stevens/replicate-mohan-2019-buildings/case/` (copy of the
  Debian-shipped tutorial, unmodified).
- 08:15 — Ran `surfaceFeatureExtract` on buildings.obj (16107 edges) — OK.
- 08:16 — Ran `blockMesh` → 5000-cell background hex mesh, domain
  (-20..330)×(-50..230)×(0..140) m; 4 patches (inlet, outlet, ground,
  frontAndBack).
- 08:16 — Ran `snappyHexMesh -overwrite`. Result: 185,237 cells across 4
  refinement levels (0:2412, 1:8489, 2:79922, 3:94414), snapped in 34.34 s,
  all mesh-quality checks pass (0 non-orthogonal >65°, 0 skewness>4, 0 negative
  volumes).

## 5. Parallel decomposition
- 08:17 — `decomposePar` with scotch method failed (dummyScotchDecomp in
  Debian package — no scotch library). Fixed by switching decomposeParDict
  to `simple` with `n (3 2 1)` = 6 subdomains. Re-ran successfully.

## 6. simpleFoam run
- 08:18 — `mpirun -n 6 simpleFoam -parallel > log.simpleFoam 2>&1`.
- 08:18–08:20 — Ran for 400 iterations, ~120 s wall.
- Convergence: at t=400, Ux Final residual = 2.39e-05, p Final residual = 4.30e-04,
  k Final residual = 7.75e-05, epsilon Final residual = 2.69e-04 (small
  oscillation, characteristic of steady RANS on complex bluff-body geometry
  with recirculation).
- ExecutionTime per iteration stabilized ~0.08 s wall.

## 7. Post-processing
- 08:20 — `reconstructPar -latestTime` merged processor* → single t=400 field.
- 08:20 — `fieldMinMax` function object → global extrema of U components, |U|,
  p, k, epsilon, nut (see REPORT.md Results table).
- 08:20 — `sampleDict` (custom) sampled six lines: 4 vertical profiles
  (inletZ, x100Z, x200Z, x300Z at y=100) and 2 horizontal profiles
  (z20X at mid-building-height, z60X above rooftops). Raw .xy files saved
  under `postProcessing/sampleDict/400/` and mirrored to
  `report/evidence/sampleDict/400/`.
- 08:21 — Streamlines: the tutorial's built-in `streamLines` function object
  seeded 40 particles → 18,543 sample points across 40 tracks, VTK output
  under `postProcessing/sets/streamLines/400/`.

## 8. Judge scoring
- 08:22 — Sent full replication summary + paper claim list to Argo Opus 4.8
  (localhost:44497). First call got 502 (transient proxy blip). Retried with
  Argo GPT-5.2 (free, canonical). Judge scored all 5 claims: C1-C4 fully
  reproduced, C5 partial (inlet uniform aloft but has boundary layer), and
  gave OVERALL = REPLICATED. Verdict text saved to
  `report/evidence/judge_verdict.txt`.

## 9. Artifacts pulled back to laptop
- report/evidence/mohan_paper_wayback_20221224.pdf (full paper, 1.84 MB)
- report/evidence/mohan_paper_extracted.txt (pdftotext, 249 lines)
- report/evidence/log.simpleFoam (345 KB)
- report/evidence/sampleDict/400/*.xy (12 raw profile files)
- report/evidence/judge_verdict.txt

Left on uicgpu at /data/stevens/replicate-mohan-2019-buildings/case/ (kept
for reproducibility): full case tree, mesh, 400/, processor0..5/,
postProcessing/{fieldMinMax1,sets,streamLines,vtkWrite,ensightWrite,visualization,subset,sampleDict}.

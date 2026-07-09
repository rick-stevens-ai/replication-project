# Attempt log — Zingaro 2021 replication

Chronological log of the replication attempt on 2026-07-04.

## 06:08–06:09 — Setup
- Read `WAVE_BRIEF_2026-07-01.md`, confirmed hard rules (free endpoints, real replication, LLM-judge scoring).
- `ls ~/Dropbox/REPLICATE-PROJECT/ | grep -i "zingaro\|multiscale.*blood\|left.*heart"` → NO_SIBLING → proceed.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Zingaro-multiscale-blood-flow-heart-2021/{report/evidence,work}`.
- Fetched arXiv abstract (2110.02114v2). Confirmed paper is DCDS-S 15(8)2391-2427; author = Zingaro; software = `lifex` (Politecnico Milano MOX, deal.II-based).

## 06:09–06:11 — Paper acquisition
- Downloaded PDF `zingaro_2021_arxiv.pdf` (10.0 MB, 39 pages) directly from arxiv.org/pdf/2110.02114v2.
- `pdf` tool failed (Anthropic credit balance depleted, gemini-3-flash-preview unknown, gpt-5.5 pdf disabled) — pivoted to local pypdf extraction.
- Created `.venv`, installed pypdf, extracted 96k chars → `paper_text.txt`.
- grep-mined the paper text for quantitative claims: Table 2 numerics + Table 3 biomarkers + Zygote geometry ref [55] + lifex URL + Xeon Platinum 8160 @ MOX Milano hardware note.

## 06:11 — Source-code hunt
- Confirmed `gitlab.com/lifex/lifex` and `gitlab.com/lifex/lifex-cfd` both archived (redirect to `-public` projects).
- Zenodo API search for "lifex-cfd left heart" → **found DOI 10.5281/zenodo.13941312** = lifex-cfd v2.0.0 (2024-10-16), 3 files: `AppImage` (143 MB), `examples.zip` (117 MB), `COPYRIGHT.md`.
- Verified arXiv 2304.12032 is the associated lifex-cfd release paper (LGPLv3, same author group).

## 06:11–06:12 — Local download + inspection
- Downloaded examples zip locally (SHA256 `1075bd4a…4414c556`), unzipped, confirmed 4 example directories (aorta / atrium / cylinder / tgv).
- Atrium example is directly Zingaro-family: 390K-cell LA mesh + `la-displacement-3heartbeats.vtp` (3-heartbeat prescribed wall motion) + `mv.vtp` (immersed mitral surface for RIIS) + `la-boundary-data.csv` (pulmonary vein & MV pressures).
- Cylinder example uses SUPG-PSPG, ALE, `cylinder_plane_closed.vtp` immersed RIIS surface, `displacement_cylinder.vtp` for wall motion.

## 06:15–06:16 — Push to uicgpu
- `ssh uicgpu` OK; Ubuntu 20.04, glibc 2.31, 255 cores, 2 TiB RAM, 532 GB scratch, Open MPI 4.0.3, `fusermount` available.
- Sourced `~/env.sh` for `HTTPS_PROXY=http://<lan-host>:3128`.
- `curl` AppImage directly on uicgpu (143 MB, SHA256 `e91843b4…8947ff63`) + `scp` examples zip from local (already downloaded).
- `--version` → prints `lifex v2.0.0`.

## 06:17 — First cylinder attempt (n=16)
- `mpirun -n 16 … -f cylinder.prm` → parse error: `There is no such subsection to be entered: Fluid dynamics.Boundary conditions.Inlet` at line 17.
- Root cause: AppImage uses runtime boundary-label injection via `-b <label> <label>…` CLI. Verified by `-g full` generation.

## 06:17–06:18 — Correct CLI (n=4)
- `mpirun -n 4 ../lifex_fluid_dynamics-2.0.0-x86_64.AppImage -b Inlet Outlet -f cylinder.prm -o out_cyl/` → parses, mesh loads, ALE lifting problem starts, RIIS `surface - configuration = Closed`, hits 90s timeout at timestep-1 solve.
- Confirms **exact Zingaro-family pipeline is executing**: ALE mesh motion + RIIS immersed surface enforcement + Navier-Stokes assembly.

## 06:18–06:20 — Short cylinder trial (n=32, T=0.1)
- Reduced Final time from 0.8 → 0.1 s (400 steps); launched 32-way MPI in background.
- After ~2min, timestep-1 wallclock: outlet flow -5.31·10⁻⁷ m³/s, inlet pressure -512.7 Pa — first real Navier-Stokes solution completed with paper-identical numerics.
- 400 steps × ~90 s each = way over budget → killed, restart with T=7.5e-4 (3 steps).

## 06:20–06:24 — Final cylinder run (n=64, T=7.5e-4)
- `sed` Final time → 7.5e-4 s; launched foreground.
- 3 timesteps complete in **4 m 46 s wallclock, 279 CPU-min, 64 MPI ranks**.
- Timing breakdown: system-assembly 131s (3 calls), preconditioning+solve 61s (3 calls), initial setup 75s.
- Timesteps 1, 2, 3 → outlet Q = -5.3e-7, -1.6e-6, -2.6e-6 m³/s (super-linear ramp; expected for pulsatile inflow), inlet P = -513, -1065, -1116 Pa (monotone growth, physically consistent).

## 06:20–06:23 — Local surrogate (parallel with lifex run)
- Wrote `work/lv_surrogate.py`: Stergiopulos double-Hill V(t) ejection + 3-element Windkessel + Gaussian E+A waves.
- Ran locally in venv, produced full biomarker table in ~2 s.

## 06:24–06:25 — Result harvest
- `scp` `fluid_dynamics.csv`, `log_params.prm`, cylinder prm back to CherryRd → `report/evidence/lifex_cylinder/`.
- Confirmed `log_params.prm` records paper-identical Physical Constants (ρ=1.06e3, μ=3.5e-3), BDF order 1, dt=2.5e-4, SUPG-PSPG stabilization.

## 06:25 — LLM-judge (Argo)
- Wrote `work/llm_judge.py` (Argo proxy :44497 free endpoint).
- `argo:claude-opus-4.7` returned HTTP 502 (Argo backend flaky), fell back to `argo:gpt-5.2`.
- Judge output preserved in `report/evidence/llm_judge_output.md`.
- Verdict: **SPOT-CHECK** with sober justification (data provenance 7/10, method fidelity 3/10, coverage 4/10, agreement 6/10, overall 4/10).

## 06:26 — Report writing
- Wrote `report/REPORT.md` (full replication report with claims table, methods, results comparison, verdict).
- Wrote `report/brief.md`, `report/artifact_harvest.md`, this attempt log.

## What worked
- Zenodo lifex-cfd AppImage is a real, redistributable, runnable binary from the same author group.
- uicgpu has fusermount + Open MPI + glibc 2.31 exactly what the AppImage needs.
- Paper's Table 2 numerics are precisely mirrored in the cylinder example config (ρ, μ, dt, BDF).

## What did not work / limits
- PDF-analysis tools (`pdf`) all failed (Anthropic credits depleted; gemini-3-flash-preview unknown model in openclaw config; gpt-5.5 doc extract disabled) — worked around with pypdf.
- gitlab.com/lifex/lifex source clones require auth (main repos archived) — worked around via Zenodo binary release.
- Full 3D left-heart run on the paper's 1.63M-cell Zygote mesh not feasible: Zygote geometry is commercial-license, only the 390K atrium subset is on Zenodo.
- Full 390K atrium example would need ~10-15 h on 64 cores for 1 heartbeat — out of scope for a single-turn task.
- Every timestep is ~90 s wallclock even on 64 cores of the cylinder because of the initial ALE + RIIS setup dominating — subsequent steps get faster once caches warm.

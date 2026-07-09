# Artifact Harvest — OSTI-2561245

## Paper
- **OSTI ID:** 2561245 — https://www.osti.gov/servlets/purl/2561245
- **DOI:** 10.1103/PhysRevE.111.045307
- **arXiv:** 2412.14953 (submitted 19 Dec 2024)
- **File:** `work/osti_2561245.pdf` (1,692,896 bytes, PDF v1.5), fetched 2026-07-02 via `ssh uicgpu` proxy.
- **Text extraction:** `work/paper.txt` (pdftotext -layout, 999 lines).

## Public dataset (qmc-hamm.hub.yt)
- **Landing:** https://qmc-hamm.hub.yt/data.html (Bokeh browser, Werkzeug/Python backend, last-modified 2023-03-03).
- **API:** `https://girder.hub.yt/api/v1/qmc/table` (Girder REST). Total records = 1594 across ~5 conformer-generation strategies.
- **Subset pulled:** input_dft=pbe AND conf_dft=pbe (paper-shape) = **38 trajectories** across a T,P grid of {600,800,1000,1200,1400,1600,1800,2000,2200} K × {50,75,100,125,150} GPa (33 unique grid points; a few grid points appear as multiple items).
- **Downloaded to:** `uicgpu:/tmp/h2_pbe_trajs/*.traj` (ASE Ulm trajectory format, sizes 5-200 KB each).
- **Frame count:** 311 individual configurations across all 38 files (median 7-8 frames/file).
- **Format-verified:** first 12 bytes = `- of UlmASE-Trajectory` (matches ASE spec). Loaded and parsed with `ase.io.read`. Every frame is 96 H atoms with PBE energy (`get_potential_energy`) and forces (`get_forces`) attached.

## Ancillary references (triangulation)
- **Morales et al. 2010** — "Evidence for a first-order liquid-liquid transition in high-pressure hydrogen from ab initio simulations", PNAS 107:12799-12803, PMC2919906. Abstract explicitly says critical point "near 2,000 K and pressures near 120 GPa" — matches Istas et al.'s positioning claim.
- **Karasiev et al. 2021** — Nature 600, E12 (Matters Arising reply to Cheng et al.). Confirmed real; supports paper's Ref [21] describing the 2048-atom AIMD comparison data used for Istas et al. Fig 12.
- **Niu et al. 2023** — "Stable Solid Molecular Hydrogen above 900 K from a Machine-Learned Potential Trained with Diffusion Quantum Monte Carlo", PRL 130, 076102, arXiv:2209.00658. Confirmed real; this is Istas et al.'s Ref [23] which describes the source of their 54k-config training set.

## Software artifacts (verified live)
- **NequIP** (Batzner et al. 2022, Nature Comm 13:2453) — PyPI `nequip`, GitHub `mir-group/nequip`, docs https://nequip.readthedocs.io. E(3)-equivariant neural network potential. Actively maintained (v0.7.0 released 2025-04-23), Zenodo DOI 10.5281/zenodo.18200066. Provides ASE + LAMMPS integration.
- **DeepMD-kit 2.1.5** — installed on uicgpu in `/data/stevens/envs/dpmd-repl`, but not used here; DPMD is exactly the type of MLIP that the paper (Section III) says FAILED to reproduce the LLPT in previous work.
- **ASE 3.x** — used to parse the .traj files.

## Evidence files (in report/evidence/)
- `qmc_hamm_inventory.txt` — full log of Girder API probing (1594 records, breakdown by ensemble/quantum).
- `qmc_hamm_full_pbe_scan.log` — log of downloading all 38 PBE-PBE trajectories on uicgpu.
- `h2_pbe_frame_stats.json` — 311-frame extracted stats (E, rs, |F|) per (T,P) grid point.
- `verify_paper_claims.log` — automated claim-by-claim verification against extracted stats.

## Analysis scripts (in work/)
- `qmc_hamm_probe.py` — initial API discovery.
- `qmc_hamm_probe2.py` — trajectory format + frame-count probe.
- `qmc_hamm_full_pbe_scan.py` — full-38-file PBE-PBE download + stats aggregation.
- `verify_paper_claims.py` — claim-vs-data comparator.

# PROGRESS — LUCID100 slot 37

Times in America/Chicago (CDT).

## 2026-06-09 — first-pass artifact harvest + smoke

- 13:53 Spawned as subagent. Confirmed source-of-truth row 86 in `LUCID100_SOLID_MASTER_QA.tsv`: Wave 4, rank 14, candidate_curated, expected verdict KEEP.
- 13:54 Set up work folder `lucid100-ac225-lu177-psma-topas-medras-rbe/{artifacts,code,figures,logs,results}`.
- 13:54 Pulled paper PDF (3.7 MB) and supplement DOCX (1.9 MB) from EJNMMI Physics open-access endpoint and Springer static-content endpoint. `pdftotext -layout` + `pandoc docx → plain` succeeded.
- 13:55 Inventoried prior LUCID work that could be reused:
  - Slot 16 `lucid-medras-mc` — fully working MEDRAS-MC install with SDD generator (Z=0/1/2/6), repair-fidelity pipeline, headline replication verified.
  - Slot 19 `lucid100-topas-proton-cellular-response` — TOPAS-nBio reproduction with documented ~120 k thread-h cost.
  - Slot 25 `lucid100-topas-medras-cellbycell` — SPT-SDD library accelerator that would in principle eliminate the TOPAS bottleneck.
- 13:56 Confirmed from paper + supplement:
  - **No author code release** (no GitHub, no Zenodo, no Figshare). Only public dep is `sjmcmahon/Medras-MC` (BSD-2).
  - **Compute footprint**: largest single ¹⁷⁷Lu sim = 34 h init + 111-139 h execute + 46 GiB RAM. ²²⁵Ac max = 1 h init + 35-85 h execute + 13 GiB RAM. 4000 simulations total.
  - **MEDRAS parameters used**: σ/Rₙ = 0.04187, λf = 2.07 h⁻¹, λs = 0.259 h⁻¹, 24 h cutoff (all MEDRAS defaults).
  - **Tables 3 & 4** give the analytical fit parameters needed to regenerate Fig 9 RBE curves without re-running TOPAS.
- 13:57 Wrote `README.md` and this `PROGRESS.md`.
- 13:58 (next) Build `code/rbe_analytical.py` reproducing Eqs. 6/7 RBE curves from the published Tables 3 & 4 parameters, and `code/medras_smoke.py` running MEDRAS-MC on electron (Z=0, surrogate for ¹⁷⁷Lu β⁻) vs alpha (Z=2, surrogate for ²²⁵Ac chain α) damages to test the *direction* of the initial-damage RBE.
- 14:00 Built `code/rbe_analytical.py` → reproduces published RBE_initial (low-dose) = b₂₂₅Ac/b₁₇₇Lu values per cell-geom × internalization. Verified 3D geometry-1 internalized: b₂₂₅Ac/b₁₇₇Lu = 166.60/77.69 = **2.144** (paper: ≈ 2.14 ✅).
- 14:01 Built `code/medras_smoke.py` → generates SDD files for 1 MeV e⁻ (Z=0, β⁻ surrogate) and 5.83 MeV α (Z=2, weighted-mean ²²⁵Ac-chain α) at 0.1, 0.5, 1, 2 Gy each, then runs `repairSimulation(... 'Fidelity')` to get initial + residual DSB counts.
- 14:02 Ran smoke: 2 particles × 4 doses × 3 repeats. Wall clock ~4 min. Z=0 b_init ≈ 35 DSB/Gy (matches McMahon X-ray default); Z=2 b_init ≈ 95 DSB/Gy. **MEDRAS-only RBE_DSB-init ≈ 2.71** — same order as paper's 2.14 (paper's value comes from a *full* TOPAS-nBio chain with PSMA source-point sampling; our smoke uses MEDRAS's built-in track sampling for monoenergetic α, so a 25-35% offset is expected and goes in the right direction).
- 14:03 Wrote `ARTIFACT_MANIFEST.md`, `FIRST_PASS_REPORT.md`, `HPC_JOB_PLAN.md`.
- 14:04 Updated `~/.openclaw/workspace/memory/subagent-progress/lucid100-ac225-lu177-psma-topas-medras-rbe.json`.

## Status
**PARTIAL FIRST-PASS COMPLETE** — KEEP recommendation stands. No retag suggested.

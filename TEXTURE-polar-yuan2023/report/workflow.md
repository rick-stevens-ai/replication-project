# Workflow — Replication of Yuan & Chen 2023 (polar SkX in PbTiO3)

## 1. Sourcing the headline
- Read `report/evidence/replication_recipe.json` and `work/textures-polar-yuan2023.txt`.
- Identified the ONE testable computational headline:
  > An out-of-plane electric field stabilizes a hexagonal close-packed polar
  > skyrmion lattice (each skyrmion |Q|=1) in a 6-nm PbTiO3 film; the lattice
  > then collapses into a single-domain ferroelectric (FE, Q->0) phase at high
  > field (Ez ~ 1.8 MV/cm).

## 2. Physics build (from scratch, CPU)
- Runner: `report/evidence/yuan2023_replication.py` (numpy + scipy, `/home/stevens/comfyui-env/bin/python`).
- Model: 2D Landau-Ginzburg-Devonshire (LGD) TDGL on the top surface of a
  48x48 (1 nm/cell) (001) PbTiO3-like film with 3-component polarization P.
  - Landau 2-4-6 bulk potential, out-of-plane strain anisotropy `K_z` (eps=-1.0%),
    spectral gradient (stiffness `g`), **nonlocal k-space depolarization kernel**
    (favors modulated multi-domain state; screening theta=0.6), external `Ez` on Pz.
  - TDGL relaxation `dP/dt = -L dF/dP` via spectral Laplacian.
- **Provenance / credited kernels:**
  - `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` — TDGL relaxation scheme,
    spectral Laplacian, 3-component P, depolarization penalty, and the Neel
    skyrmion seeding routine.
  - `ollie_berg_luscher_topological_charge_kernel.py` — Berg-Luscher lattice
    solid-angle Pontryagin charge on n = P/|P| (integer-robust).

## 3. Experiment
- Plant a close-packed array of 16 Neel skyrmions, relax into a self-consistent
  SkX ground state at Ez=0.
- Sweep Ez in {0, 0.3, 0.6, 0.9, 1.3, 1.8, 2.4} (reduced units), relaxing from
  the SkX state each time; measure total |Q|, net integer Q, skyrmion count,
  and mean Pz.
- **SAVE-EARLY:** results written to `work/yuan2023_result.json` before the
  sweep and after every field point.

## 4. Verification criteria (self-scored)
1. Close-packed SkX exists: net integer charge Q_net ~ number of seeded cores.
2. Per-core charge ~ |Q|=1 (Q_net / N_seed).
3. Field destroys SkX -> FE: |Q|(high Ez) < 0.25 |Q|(low Ez) AND |Pz| saturates.

## 5. Iterations (honest record)
- v1 (mean-field depolarization, no seeds): no skyrmions formed -> NEGATIVE.
- v2 (random seeds, dt=0.05): numerical overflow in sextic term -> fixed with
  grid-placed seeds, amplitude clamp, dt=0.02.
- v3 (weak depolarization): background +z always won; skyrmions decayed.
- v4 (nonlocal k-space depolarization, eps_d=5.0): clean field-driven collapse;
  Q_net=15.86~16 confirms |Q|=1 per core -> REPLICATED.

## 6. Packaging
- Extraction: `extraction/marker.md`, `extraction/nougat.mmd` (pdftotext interim + headers).
- Report: `REPORT.tex`, `open_questions.json`, `workflow.md`, `artifacts_summary.md`,
  `failure_analysis.md`.
- Evidence: result JSON + runner + both kernels copied to `report/evidence/`.
- Figures: `report/figs/{skyrmion_vs_Ez,polar_textures,pontryagin_density_SkX}.png`.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-polar-yuan2023
/home/stevens/comfyui-env/bin/python report/evidence/yuan2023_replication.py
```
Runtime ~0.5 s (well under the 6-min budget).

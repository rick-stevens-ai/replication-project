# Workflow — hong2026 replication (multi-order polar skyrmion thermal stability)

## Goal
Test the paper's headline: temperature drives a polar system through
solitons -> 1π -> 2π -> 3π -> 4π skyrmions, and the **2π-skyrmion has the
widest thermal stability window (~600 K)**.

## Steps executed
1. **Read** paper text (`work/textures-polar-hong2026.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Extracted the key mechanism:
   multi-order kπ-skyrmions have concentric azimuthal rings; net topological
   charge Q alternates **±1 for odd k** (1π, 3π) and **0 for even k** (2π, 4π).
2. **Built from scratch** `work/hong2026_runner.py`:
   - Single-layer 2D 3-component TDGL phase-field (Landau a(T)|P|² + b|P|⁴ +
     c|P|⁶, gradient stiffness g|∇P|², easy-z anisotropy K_z, spectral
     Laplacian) **adapted from** `ollie_tdgl_phasefield_polar_skyrmion_kernel.py`.
   - **Langevin (temperature) noise** `+ sqrt(2·L·kT·dt)·η` — the thermal driver.
   - Seed kπ radial windings: polar angle Θ(r) winds by k·π from core to edge;
     in-plane m=1 azimuthal winding.
   - Confirm winding via **Berg-Luscher** `topo_charge_berg` (used verbatim from
     `ollie_berg_luscher_topological_charge_kernel.py`).
   - Measure **structural survival** S(T) = normalized overlap of annealed Pz
     with seeded Pz, across a T sweep (mapped to 300–1400 K for reporting).
   - Stability window = span of T with S(T) ≥ 0.5.
3. **SAVE-EARLY**: skeleton `hong2026_result.json` written before the sweep,
   re-saved incrementally after each winding order.
4. **Compare & score**: window ordering vs claim; Q parity vs theory.
5. **Package** 8 artifacts + copy result JSON & code into `report/evidence/`.

## Key result
- Q parity reproduced: 1π→Q=−1.0, 2π→Q≈0, 3π→Q=−1.0, 4π→Q≈0. ✓
- Stability windows (K): 1π=917, **2π=1100**, 3π=917, 4π=917 → **2π widest**. ✓
- Ordering high→low: 2π, 1π, 3π, 4π. Matches the headline (2π most stable).

## Runtime
Full sweep (4 orders × 7 temperatures, 64×64 grid): **~4 s** on CPU
(`/home/stevens/comfyui-env/bin/python`).

## Provenance / credit
- TDGL phase-field + Langevin seeding: **ollie_tdgl_phasefield_polar_skyrmion_kernel.py**
- Berg-Luscher topological charge: **ollie_berg_luscher_topological_charge_kernel.py**

# Workflow — jaubert2016 replication

## Goal
Replicate the Fragmented Coulomb Spin Liquid (FCSL) on the pyrochlore lattice
(Jaubert 2016, arXiv:1602.02707) from scratch and demonstrate moment fragmentation.

## Steps executed
1. **Read paper + recipe.** Parsed `report/evidence/replication_recipe.json` and
   `work/textures-spin-jaubert2016.txt`. Extracted the quantitative targets:
   - headline effective Coulomb prefactor `8√2/3√3 ≈ 2.17732`, `V_nn/D = -2.17732`
   - pseudo-magnetization ladder `ρ = {0, 1/2, 1}` (spin-ice / FCSL / AIAO)
   - dumbbell defect energies `ΔE_mm = 19.75 D`, `ΔE_hh = -4.73 D`
   - Bragg (charge order) + pinch-point (Coulomb) coexistence in S(q), Fig. 10.
2. **Build physics** (`work/jaubert2016_replication.py`, numpy only, ~6 s):
   - (A) Analytic: verify `8√2/3√3` prefactor and the Madelung/dumbbell energies
     `ΔE_hh`, `ΔE_mm` from Eqs. (12-13) using `M_zb = 1.638`.
   - (B) Pseudo-magnetization ladder from single-tetrahedron configs.
   - (C) Construct the FCC pyrochlore lattice (L=3, 108 spins, 27+27 tetrahedra,
     periodic). Generate FCSL ensemble by simulated annealing to the zinc-blende
     single-charge constraint `E = Σ(Q_A-2)² + Σ(Σ_B-2)² = 0`. 40 valid configs.
   - Helmholtz split: ordered fragment `½e_i` (AIAO) + residual (Coulomb); check
     residual is divergence-free. Compute S(q) in [hhl] for full/ordered/residual.
3. **SAVE-EARLY** to `work/jaubert2016_result.json` after every stage; S(q) grids
   saved as `.npy`.
4. **Score** 10 automated checks → 10/10 pass.
5. **Package** 8 artifacts (extraction ×2, report ×6) + copy code & result JSON to
   `report/evidence/`.

## Runner
`/home/stevens/comfyui-env/bin/python` (numpy 2.3.5). No external kernels needed —
the model is analytic + small classical Ising annealing.

## Reproduce
```
/home/stevens/comfyui-env/bin/python work/jaubert2016_replication.py
```

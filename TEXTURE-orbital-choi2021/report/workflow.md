# Workflow — choi2021 orbital Hall in Ti replication

## Goal
Reproduce the headline of Choi et al., *Observation of the orbital Hall effect in a light
metal Ti*: fcc Ti has a **large** orbital Hall conductivity σ_OH ≈ 3800 (ħ/e)(Ω·cm)⁻¹,
~two orders of magnitude larger than its spin Hall conductivity σ_SH = −40, arising
**without SOC** from momentum-space orbital texture.

## Steps executed
1. **Read** paper text (`work/textures-orbital-choi2021.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Extracted claim: σ_OH~3800, σ_SH=−40,
   mechanism = orbital texture + orbital Berry curvature, SOC not required.
2. **Studied kernel** `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` — reused its Kubo /
   L_z orbital-current structure (`j^Lz_x = ½{L_z, v_x}`, `−2 Im[…]/(E_n−E_m)²` sum,
   `v_a = i[H,R_a]`).
3. **Built from scratch** `work/choi2021_orbital_hall.py`:
   - 5 real d-orbitals, Slater–Koster d–d two-center hoppings (1st + 2nd neighbors on a
     cubic Ti surrogate, a=4.11 Å) → intrinsic orbital texture.
   - Intra-atomic L_x,L_y,L_z built from complex→real d-harmonic unitary.
   - k-space Kubo orbital Berry curvature summed over occupied bands at Ti-like filling.
   - Spin sector carries no texture without SOC → σ_SH ≡ 0 (paper's central point).
4. **Ran** with `/home/stevens/comfyui-env/bin/python`, coarse grids nk=8/12/16 + filling
   scan + fine E_F sweep. **SAVE-EARLY**: `work/choi2021_result.json` rewritten after every grid.
5. **Compared** to 3800; scored order-of-magnitude + mechanism honestly.
6. **Packaged** 8 artifacts and copied code+result to `report/evidence/`.

## Key results
- σ_OH (converged nk=16, Ti filling) = **147.7**; peak over E_F/filling scans = **775.4**.
- σ_SH = **0.00** everywhere (no SOC) → OHE dominates, extreme version of paper's ordering.
- Runtime **<10 s** CPU.

## Reproduce
```
/home/stevens/comfyui-env/bin/python work/choi2021_orbital_hall.py
# writes work/choi2021_result.json
```

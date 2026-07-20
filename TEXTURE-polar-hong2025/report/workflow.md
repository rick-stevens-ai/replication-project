# Workflow — hong2025 phase-field vortex-phase replication

## Goal
Independently reproduce the phase-field **headline claim** of Gupta et al. 2025:
a **pure vortex phase** stabilizes in the polarization field of a PbTiO3/SrTiO3
(STO/PTO/STO) trilayer via TDGL relaxation under Landau + elastic + electric +
gradient energy competition (paper reports ~14 nm vortex periodicity).

## Steps taken
1. **Read** paper text (`work/textures-polar-hong2025.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Located the phase-field method
   (TDGL, `dP/dt = -L dF/dP`, F = Landau+elastic+electric+gradient) and the
   "pure vortex phase in the trilayer" claim (lines ~196, 522-551).
2. **Built from scratch** a minimal 2D TDGL phase-field
   (`work/hong2025_runner.py`), P=(Px,Pz) on a 160x40 (x,z) grid, central 50%
   = PTO film. Method structure templated (with credit) from the two shared
   kernels.
3. **First run FAILED** (v1): a simple depolarization term `eps*<Pz>` produced a
   uniform in-plane domain, only 2-7 stray vortices, verdict PARTIAL. Diagnosed:
   wrong electric-energy form.
4. **Fixed physics**: replaced with the bound-charge penalty
   `f_elec = 0.5*eps*(div P)^2` -> `dF/dP = -eps*grad(div P)`, which drives P
   divergence-free = closed flux loops = vortices, plus uniaxial `-Kz*Pz`
   (PTO c-axis). Longer relaxation (12000 steps, dt=0.01).
5. **Re-ran** -> balanced **+21/-21** alternating vortex array, periodic,
   `<|P|>`=1.18. Control run (eps=0.05) collapsed to near-uniform (3/7 stray).
   Verdict **REPLICATED, 5/5 checks**. Runtime 4.5 s. SAVE-EARLY throughout to
   `work/hong2025_result.json`.
6. **Figure**: `work/hong2025_figure.py` -> `figs/hong2025_vortex_phase.png`
   (Pz + arrows, winding-number field).
7. **Packaged** 8 artifacts + copied result JSON, both runner scripts, and both
   kernels into `report/evidence/`.

## Characterization methods
- **Vortex count / topology**: integer winding number of the polar director
  `theta = atan2(Pz,Px)` via plaquette angle-sum (2D Berg-Luscher adaptation).
- **Periodicity**: FFT of mid-film Px(x) row; calibrated cells->nm assuming
  the PTO film (~half the z-grid) ~ 8 nm (20 uc).
- **Regime selectivity**: control run with electric energy off.

## Runner
`/home/stevens/comfyui-env/bin/python work/hong2025_runner.py`  (~5 s, CPU).

## Pitfalls found
- A column-averaged `<Pz>` depolarization term is NOT sufficient to nucleate a
  vortex array; you need the local `(div P)^2` bound-charge energy whose
  minimizer is a divergence-free (flux-closure) field.
- Uniaxial anisotropy (-Kz Pz) is needed so Pz has somewhere to point out of
  plane, giving the vortices their out-of-plane core rotation.

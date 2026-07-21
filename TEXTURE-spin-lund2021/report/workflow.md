# Workflow — lund2021 replication

## Method class
Analytic effective-action / linear spin-wave theory (LSWT). CPU-only.

## Pipeline
1. **Acquire/parse.** Read `work/textures-spin-lund2021.txt` (1145 lines) and
   `report/evidence/replication_recipe.json`. Ran `pdftotext -layout` →
   `extraction/_pdftotext.txt` as extraction interim.
2. **Extract physics.** Identified the true claim: this is a *spin-pumping*
   paper, not thermal Hall. The "three spin-wave bands" are the k=0
   uniform-precession resonance modes (Eqs. 15–16, Sec. III), with
   mutually orthogonal x/y/z polarizations. Pulled the kagome Hamiltonian
   (Eq. 14), 120° easy axes, and App. A constants (a1, a2, K1, K2).
3. **Build from scratch** (`work/lund2021_lswt.py`, runner
   `/home/stevens/comfyui-env/bin/python`):
   - (A) Holstein–Primakoff LSWT of the 120° kagome Heisenberg AFM in local
     frames → BdG matrix → Colpa diagonalization (eig of gM) on a 12×12 grid
     + Γ-K-M-Γ path. Checks for the zero-energy flat band.
   - (B) k=0 uniform modes: diagonalize `w^2 = 4 a2 K / a1^2` with
     K=diag(K1,K1,K2); extract frequencies + polarization eigenvectors;
     test orthogonality and the analytic ratio √(K2/K1).
   - (C) **[COVERAGE-FLIP extension]** Full k-resolved bands on a 24×24 BZ
     grid: para-diagonalize the BdG problem, keep the particle-branch
     Bogoliubov eigenvectors (normalized under the g-metric), and project
     each mode onto the lab frame via P = Σ_i[(u_i+v_i)ex_i − i(u_i−v_i)ey_i].
     Quantify single-axis polarization purity vs |k| (6 radial bins), and
     verify the three bands keep distinct character (one z-dominant, two
     in-plane). A small easy-axis Kani=0.05 JS gaps the flat band to a
     finite-energy flat band (0.557 JS).
   - (D) **[extension]** Magnon Berry curvature via Fukui–Hatsugai–Suzuki
     plaquettes (link variables with the BdG g-metric) + thermal Hall
     κ_xy(T). Includes a degeneracy diagnostic (min direct gap, fraction of
     π-saturated plaquettes) that flags the single-band FHS as ill-defined
     at the band touchings and confirms κ_xy=0 by symmetry (no DMI).
4. **SAVE-EARLY** to `work/lund2021_result.json` (single dump at end of a
   fast-running script; new `full_bands` and `berry_thermal_hall` sections).
5. **Compare & score** (see `artifacts_summary.md`).
6. **Package** 8 artifacts; copy result JSON + code to `report/evidence/`.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-spin-lund2021
/home/stevens/comfyui-env/bin/python work/lund2021_lswt.py
```

## Key decisions
- Coarse 12×12 BZ grid — sufficient to establish flatness (std ~1e-8) and
  band ranges; SAVE-EARLY prioritized.
- Set S=a=ℏ=1, J=1, K=0.10, Kz=0.05 as representative; the *ratios* and
  orthogonality (the paper's actual claims) are parameter-independent.

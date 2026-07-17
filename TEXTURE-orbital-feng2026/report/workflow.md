# Workflow — feng2026 replication

**Paper:** feng2026, arXiv:2602.19076, *Magnetic Orbital Hall Effect in d-wave altermagnets*
**Texture class:** orbital (magnetic orbital Hall effect / d-wave altermagnet)
**Verdict:** PARTIAL — d-wave altermagnet band symmetry reproduced; MOHE transport magnitude method-limited; material DFT out of scope.

## Tools / codes
- Python 3 + NumPy (vectorized 4×4 `numpy.linalg.eigh`) + Matplotlib. CPU only.
- No DFT stack (VASP/QE/Wannier90 not available; only ASE present on uicgpu — the material claims C4–C6 were therefore out of scope).

## Pipeline
1. **Model build.** 4-band (2 sublattice τ ⊗ 2 spin σ) Bloch Hamiltonian on a square lattice, Eqs.6–8:
   - H0 = 4t1 cos(kx/2)cos(ky/2) τx + 2t2(cos kx+cos ky) τ0 + 2t_d(cos kx−cos ky) τz + J τz (N·σ), N = ẑ.
   - H^c = 4λ_c sin(kx/2)sin(ky/2) τy σz (spin-conserving SOC).
   - H^f = 4λ_f[sin(kx/2)cos(ky/2) τy σx + cos(kx/2)sin(ky/2) τy σy] (spin-flip SOC).
   - Params (eV): 4t1=0.2, 2t2=−0.08, 2t_d=−0.04, J=0.11, λ_c=λ_f=0.1·t1.
2. **Band structure (C1).** Diagonalize along Γ–X–M–Γ; color bands by ⟨σz⟩. Measure spin splitting on the x-axis vs on the BZ diagonal.
3. **MOHE (C2/C3).** Build velocity operators v_x, v_y from ∂H/∂k (analytic derivatives). Construct the interband orbital-moment matrix L_z. Attempt σ^{Lz}_xy via an intraband Drude-like sum over occupied bands.
4. **Symmetry check (C3).** Compare the (allowed) xy component against the (forbidden) xx component.

## Cost
- CPU minutes (single core). Band path: 200 pts × 3 segments. MOHE: 60×60 k-mesh for the μ-sweep, 90×90 at the two focus μ values.

## Estimate of work done
- ~1 core-hour of compute + analysis (mostly interactive debugging of the MOHE cancellation).
- The band-symmetry claim (C1) is fully and cleanly reproduced; the MOHE magnitude (C2/C3) requires the correct nonlinear Kubo implementation (see failure_analysis.md); the material claims (C4–C6) require an external DFT stack + Supplemental-Material parameters.

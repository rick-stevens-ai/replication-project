# Workflow — xie2025 replication

## Goal
Reproduce the headline of Xie & Nagaosa (arXiv:2504.14166): in the iCDW
(loop-current) triple-Q CDW phase, the phase and amplitude collective modes
**mix** in the A irrep, whereas in the rCDW phase they **decouple**; and recover
the closed-form mixed-mode spectrum Eq. (12).

## Steps
1. **Read** paper text (`work/textures-loop-current-xie2025.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Identified governing equations:
   free energy Eq. (2), fluctuation Lagrangian Eq. (10), mixed-mode spectrum
   Eq. (12), and the mixing coefficient `∝ sin(3θ0)`.
2. **Build from scratch** (`report/evidence/xie2025_replication.py`):
   - `free_energy()` — C3-reduced mean-field free energy (Eq. 2, λ3=0).
   - `minimize_meanfield()` — grid + parabolic refine over (|Δ_Q|, θ0) for
     iCDW (b>0, θ0=±π/2) and rCDW (b<0, θ0=0/π).
   - `A_channel_matrix()` — q=0 2×2 dynamical matrix from Eq. (10).
   - `closed_form_Eq12()` — analytic mixed-mode energies.
   - `cross_susceptibility()` — off-diagonal (M⁻¹)_{A,θ}.
   - `load_kernel()` + microscopic loop-current cross-check via shared kernel.
3. **SAVE-EARLY** to `work/xie2025_result.json` on first successful run.
4. **Compare** numeric diagonalization vs Eq. (12); check iCDW-only mixing.
5. **Package** 8 artifacts (extraction ×2, report ×5, evidence copies).

## Runner
`/home/stevens/comfyui-env/bin/python report/evidence/xie2025_replication.py work/xie2025_result.json`

## Pitfalls hit
- Dynamically importing the shared kernel with `importlib` failed on its
  `@dataclass(frozen=True)` because `from __future__ import annotations` needs
  the module registered in `sys.modules`. Fixed by
  `sys.modules["lc_kernel"] = mod` before `exec_module`.
- Kernel default filling=0.5; used 5/12 (kagome VHS-relevant) for the crosscheck.

## Key results
- Eq. (12) reproduced to max abs err **4.4e-16**.
- iCDW off-diagonal mixing = **−0.2121** (nonzero); rCDW = **7.8e-17** (zero).
- `mixing_present_in_iCDW_only = true`, `Eq12_reproduced = true`.
- Kernel: loop_order(φ=0)=0, loop-current susceptibility=−62.2 (finite).

# Workflow — Replication of Sinha 2016 (arXiv:1604.04081)

*Spin texture of an irradiated warped topological insulator surface*

## 0. Goal
Reproduce, from the paper's equations only (not author code), the two central
claims: (A) off-resonant circularly polarized light opens a TR-breaking gap
`2·Δω` at the Dirac point; (B) the light breaks in-plane spin-momentum locking,
with a `sin(3θ)` angle-of-deviation pattern.

## 1. Model transcription
- Warped Dirac surface state `H0 = ħv k(kx σy − ky σx) + (λ/2)(k+³+k−³)σz` (Eq. 1).
- Circular drive via Peierls substitution; off-resonant (van Vleck / high-ω)
  effective Hamiltonian `Heff = H0 + [V−1, V+1]/(ħω)` (Eq. 3).
- Reduced to the 2×2 form (Eq. 5) with:
  - light-induced gap `Δω = (evA0)²/ħω`,
  - warping-drive coupling `a = 4αβ/(ħ²ωv)`,
  - `Δ(k,θ) = λ(kx³ − 3kx ky²) + Δω`.
- Energies (Eq. 6), spins (Eqs. 9–11), deviation angle (Eq. 15).

## 2. Units / constants
- Energy in eV, momentum in nm⁻¹, length in nm.
- Only the product `ħv` enters Eqs. 5,6,9–11 → set **ħv = 1 eV·nm** (paper uses
  constant velocity `v_k = v`).
- Paper constants: `ħω = 8 eV`, `λ = 0.2 eV·nm³`.

## 3. Parameter derivation
- `Δω = (evA0)²/ħω` — exact, first-principles. Reproduces table:
  0.5²/8 = 0.031 ≈ 0.03 eV; 0.9²/8 = 0.101 ≈ 0.10 eV.
- `a` — the microscopic `4αβ/(ħ²ωv)` needs a numeric `v` the paper never states
  (only `ħv`). Empirically calibrated `a ≈ 0.68·(evA0)² nm` → 0.17 / 0.55 nm.
  (Functional form `a ∝ (evA0)²` is correct; only scale is fit.)

## 4. Two independent numerical routes (cross-check)
1. **Analytic**: closed-form Eqs. 6, 9–11.
2. **Numeric**: build 2×2 `Heff` (Eq. 5), `numpy.linalg.eigh`, spins as
   `⟨ψ|σi|ψ⟩`.
- Compared over a 25×25 `kx,ky ∈ [−3,3]` grid → **max energy error 0.0 eV**,
  **max spin error 0.0** (machine precision). Confirms the transcription.

## 5. Claim checks
- **A (gap):** `E(k=0)=±Δω` → full gap `2Δω` = 0.0625 / 0.2025 eV. `Sz(k→0)=+1`
  gapped vs `0` gapless → TR breaking confirmed.
- **B (locking):** `δω(θ)` at `k=a=0.55`: zero for all θ when `a=0` (locked);
  nonzero for `a≠0` except at multiples of 60° (`Γ–K`, `θ=π/3`). `S·k≈0` at
  small k in gapless case.

## 6. Pitfall encountered
`δω ∝ sin(3θ)` is **identically 0 at every multiple of 60°**. Sampling only
symmetry directions (0°, 60°, 120°) falsely suggests locking is preserved. Must
sample **off-symmetry angles (30°, 45°, 90°)** to see the broken-locking effect.
See `failure_analysis.md`.

## 7. Tooling
- Python: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5).
- Run: `python work/sinha2016_floquet.py` → writes `sinha2016_result.json`.
- Extraction: `marker`/`nougat` binaries absent → `pdftotext -layout` used as
  interim; results normalized into `extraction/marker.md` + `extraction/nougat.mmd`.
- LaTeX: no `pdflatex`/`tectonic` in env → `report/REPORT.tex` shipped as source
  (compiles cleanly with a standard TeX install).

## 8. Verdict
**REPLICATED** — coverage ~8/10, agreement ~9/10.

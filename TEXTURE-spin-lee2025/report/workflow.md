# Workflow — Replication of lee2025 (altermagnet spin splitting)

## 1. Source ingestion
- Read paper text `work/textures-spin-lee2025.txt` and recipe `report/evidence/replication_recipe.json`.
- Interim extraction produced with `pdftotext -layout` (Marker/nougat OCR not installed in this env) → `extraction/marker.md`, `extraction/nougat.mmd`.

## 2. Identify the ONE testable headline
Recipe `method=both`; class = altermagnet / spin texture. Selected headline claim:

> The minimal 2D square-lattice 4-band model (basis `[A↑,B↑,A↓,B↓]`), with atomic
> exchange `h_eff` and anisotropic 3rd-neighbour hopping `δt`, produces spin
> splitting `ΔE ∝ 2·t_{k,z}·h_eff` that is nonzero **only when both** `δt≠0` and
> `h_eff≠0`, exhibiting a **d-wave nodal** spin structure (nodes at zone
> centre/boundary and along `k_x=0` / `k_y=0` lines).

## 3. Build from scratch (`work/lee2025_replicate.py`)
- Implemented the 4×4 Bloch Hamiltonian, Eqs (1)–(2):
  `H = ε_k·I + t_{k,x}·τ_x + t_{k,z}·τ_z + h_eff·(τ_z⊗σ_z)`.
- `ε_k = 2t₂(cos k_x+cos k_y) + 4t₃ cos k_x cos k_y − μ`
- `t_{k,x} = 4t₁ cos(k_x/2)cos(k_y/2)`, `t_{k,z} = −4δt sin k_x sin k_y`.
- Diagonalized numerically with spin labels via `⟨σ_z⟩`.
- Params (energy unit t₁): t₁=1, t₂=0.5, t₃=0.25, δt=0.2, h_eff=2.0, μ=0.

## 4. Tests / observables
1. **Numeric == analytic**: 4×4 `eigh` vs closed-form Eq (3) over 400 random k.
2. **Splitting at (π/2,π/2)**: ΔE and Fig 4(d) curves vs δt and vs h_eff.
3. **Two-ingredient necessity**: BZ scan of splitting anisotropy in 4 param cases.
4. **d-wave nodal structure**: splitting along k_x=0 / k_y=0 lines + quadrant sign of generator `t_{k,z}`.

## 5. Save-early, compare, score
- Results written to `work/lee2025_result.json` (copied to `report/evidence/`).
- Honest self-scoring: 7/7 checks pass → verdict **REPLICATED**.

## 6. Package (8 artifacts)
`extraction/marker.md`, `extraction/nougat.mmd`, `report/REPORT.tex`,
`report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`,
`report/failure_analysis.md`, plus evidence (`result JSON` + `code`) in `report/evidence/`.

## Credits
Kubo/Berry methodology reference: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py`
(shared-kernels-cache). Not required for the core diagonalization here (SOC-free,
spin is a good quantum number) but cited for the AHE follow-up in open questions.
Runner: `/home/stevens/comfyui-env/bin/python`. Runtime ≈ 0.08 s.

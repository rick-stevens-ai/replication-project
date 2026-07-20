# Workflow — Replicating the RSLC tight-binding model (Tian et al. 2026)

## 0. Scope decision
- **In scope:** tight-binding RSLC model (Eq. 3), band structure, group velocities, semiclassical Boltzmann conductivity (Eq. 2), conductivity spin polarization (Eq. 4), the quasi-1D 100% spin-polarized transport claim.
- **Out of scope (deliberate):** DFT of monolayer Mg₂Mo₂(PO₅)₂, layer-resolved P(k), relativistic electric Hall effect, spin-layer-group enumeration. See `failure_analysis.md`.

## 1. Read paper + recipe
- `work/textures-polar-tian2026.txt` (597 lines) — full text layer.
- `report/evidence/replication_recipe.json` — method, TB Hamiltonian, ridge limit δ≈0, transport relation σ_ab ∝ e²τ v_a v_b.
- Identified the operative equations: Eq.(1) ridge dispersion, Eq.(2) Boltzmann σ, Eq.(3) RSLC Hamiltonian, Eq.(4) SP definition.

## 2. Build from scratch (`work/tian2026_replication.py`)
1. Encode H(k) = ε + diag(π₀cos k_x + δ cos k_y, π₀cos k_y + δ cos k_x) on a 401² k-grid.
2. Analytic group velocities v_a = ∂E/∂k_a for each spin band.
3. Boltzmann σ_ab^n = e²τ ⟨v_a v_b (−∂f/∂E)⟩ with Fermi-Dirac window at E_F=0.3, k_BT=0.02.
4. SP_xx, SP_yy via Eq.(4).
5. Sweep δ ∈ {0, 0.05, 0.2} to test the ridge limit and the quasi-1D degradation.
6. Band path Γ-X-M-Y-Γ and ridge-flatness metric along Δ(0,v,0).

## 3. SAVE-EARLY
- Dumped everything to `work/tian2026_result.json` in the same run that computes it (no separate step that could be lost).

## 4. Compare + score
- δ=0: SP_xx=+1, SP_yy=−1, σ_yy^↑ = σ_xx^↓ = 0 exactly → matches Fig. 3(c-III) |SP|=1 opposite-sign claim (sign convention differs by basis labeling only).
- δ>0: |SP| = 0.997 (δ=0.05), 0.956 (δ=0.2) → quantifies "quasi"-1D.
- Verdict **REPLICATED** (TB scope). Coverage 7/10, Agreement 9/10.

## 5. Package 8 artifacts
- `extraction/marker.md`, `extraction/nougat.mmd` (pdftotext -layout interim + header).
- `report/REPORT.tex` (REVTeX PRL), `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`.
- Copied result JSON + replication code + recipe into `report/evidence/`.

## 6. Reproduce
```bash
/home/stevens/comfyui-env/bin/python work/tian2026_replication.py
```
Runtime ≈0.05 s (numpy 2.3.5, scipy 1.17.0).

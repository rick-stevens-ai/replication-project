# Workflow — li2023 replication

## Goal
Replicate the central claim of Li, Kim & Kee (arXiv:2309.03288v2): coupled
van-Hove singularities with small energy separation drive a loop-current +
charge-bond-order (LCBO) ground state lower in energy than CBO⁻, with LCBO
favored when δε < 4(|b|²+|b'|²)|Δ|.

## Steps executed

1. **Read paper + recipe.** Parsed `replication_recipe.json` (method=mean-field,
   headline formula Eq.4, LCBO condition) and `work/textures-loop-current-li2023.txt`.
   Identified the falsifiable core: the 6×6 effective patch Hamiltonian Eq.(2),
   eigenvalues Eq.(3), and free-energy difference Eq.(4).

2. **Built physics from scratch** — `report/evidence/li2023_patch_model.py`:
   - Assembled the 6×6 `H_eff(k, Δ)` exactly per Eq.(2): circulant intra-vHS
     blocks with s₁=−2|b'|², s₂=+2|b|²; diagonal inter-vHS coupling λk_i.
   - Mean-field free-energy density by direct patch summation over |k|<k_cut,
     with numerically stable softplus for `-T ln(1+e^{-x})`.
   - Compared the two λ=0-degenerate minima Δ_CBO⁻=−|Δ| and Δ_LCBO=|Δ|e^{iπ/3}.
   - Implemented Eq.(3) eigenvalues and Eq.(4) closed form for cross-checks.

3. **SAVE-EARLY** to `work/li2023_result.json` immediately after the first run
   (scans over |Δ|, λ, and δε), before building artifacts.

4. **Compared & scored.** Added `agreement_analysis`: λ=0 degeneracy (df~1e-16),
   λ-power fit = 1.98 (vs 2.0 in Eq.4), sign(df) vs LCBO condition = 7/7,
   Eq.4-sign vs numeric = 7/7.

5. **Extraction artifacts.** `pdftotext -layout` → `extraction/_pdftotext.txt`;
   curated `extraction/marker.md` (header + transcribed equations) and
   `extraction/nougat.mmd` (header + verbatim body). Both flagged as interim
   stand-ins (no GPU Marker/Nougat in this CPU sandbox) — no fabrication.

6. **Report package.** `report/REPORT.tex`, `report/open_questions.json`,
   this `workflow.md`, `report/artifacts_summary.md`,
   `report/failure_analysis.md`. Copied result JSON + code to `report/evidence/`.

## Tooling
- Runner: `/home/stevens/comfyui-env/bin/python` (numpy only).
- Kernels credited: `loop_current_meanfield_kernel.py`,
  `loop_current_kagome_kernel.py` (loop-current = imaginary bond order =
  Peierls-flux current convention).

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-li2023
/home/stevens/comfyui-env/bin/python report/evidence/li2023_patch_model.py
```

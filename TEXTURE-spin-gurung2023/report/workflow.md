# Workflow — gurung2023 replication

## Goal
Verify the headline of Gurung et al. (2023): a noncollinear antiferromagnet
(Mn₃GaN, kagome-based) exhibits **nearly 100% effective spin polarization** of its
conduction channels.

## Steps executed
1. **Read** paper text (`work/textures-spin-gurung2023.txt`) + recipe
   (`report/evidence/replication_recipe.json`). Extracted Eq. 2 spin-polarization
   definition, the Fig. 1 illustrative kagome model (Δ/t=1.5, 6 bands, one orbital,
   NN hopping, 120° noncollinear AFM), and the P̂T̂ / T̂t̂ symmetry-breaking origin.
2. **Built from scratch** a 2D kagome tight-binding Hamiltonian
   (`report/evidence/code/gurung2023_noncollinear_kagome_spinpol.py`):
   - 3 sublattices × 2 spin = 6 bands.
   - Spin-independent NN hopping via Bloch phases on kagome bonds.
   - On-site exchange `(Δ/2) mᵢ·σ` with mᵢ at 90°/210°/330° (in-plane 120° Γ₅g-like).
3. **Computed** the effective spin polarization p_k∥(k_y, E_F): for each (k_y,E_F)
   found Fermi crossings along k_x, took per-channel spin expectations, applied Eq. 2.
4. **SAVE-EARLY**: wrote `work/gurung2023_result.json` immediately after the run.
5. **Compared** to the "nearly 100%" claim and scored.
6. **Packaged** 8 artifacts (extraction ×2, REPORT.tex, open_questions.json,
   workflow.md, artifacts_summary.md, failure_analysis.md, evidence copies).

## Tools / environment
- Physics runner: `/home/stevens/comfyui-env/bin/python` (numpy). Runtime ~2.3 s.
- Extraction: `pdftotext -layout` (marker/nougat interim).
- Kernels credited: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (s–d lattice pattern),
  kagome loop-current kernel (geometry pattern). Model written from scratch.

## Key result
- 6 spin-split bands (no SOC) ✓ ; `max p_k∥ = 0.99997` ≈ 100% ✓.
- Verdict: **REPLICATED** (tight-binding headline). DFT/ETMR out of scope.

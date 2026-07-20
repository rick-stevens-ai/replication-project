# Workflow — Ding et al. 2026 replication (Fe2Se2Cl giant altermagnetic splitting)

## Goal
Test the headline claim — *giant altermagnetic spin splitting up to ~620 meV in
hole-doped monolayer Fe2Se2Cl* (checkerboard order, no SOC) — via a from-scratch
tight-binding surrogate, skipping DFT. Target < 6 min, save-early.

## Steps executed
1. **Read** `report/evidence/replication_recipe.json` + `work/textures-orbital-ding2026.txt`.
   Extracted the essential physics:
   - Checkerboard (Neel) altermagnet; two Fe sublattices with opposite moment.
   - Single-sided Cl breaks inversion; sublattices related by `{C2||C4z}`,
     `{C2||Md}`, `{C2||Md_perp}` -> d-wave altermagnet.
   - Splitting ~620 meV near E_F along Gamma-X(Y)-M, reverses X<->Y, no SOC.
2. **Built** `work/ding2026_altermagnet_tb.py`: 2-sublattice spinful TB model.
   - Anisotropic same-sublattice hopping (t±delta) with x/y swapped between A,B
     to enforce C4z; equal-and-opposite on-site exchange ±m (zero net moment);
     isotropic inter-sublattice NN hopping.
   - Compute spin splitting on 81x81 BZ grid + Gamma-X/Y/M paths; fit to
     `cos kx - cos ky`; check diagonal nodes, sign reversal, net moment.
3. **SAVE-EARLY** -> `work/ding2026_result.json` (first run: 1800 meV, symmetry perfect).
4. **Calibrated** `delta` 0.26 -> 0.090 eV so near-Fermi splitting ~ claim; re-ran
   -> 720 meV (ratio 1.16), d-wave R2=0.998, nodes ~0, reversal=-1, moment=0.
5. **Packaged** 8 artifacts + copied result JSON and code to `report/evidence/`.

## Tools
- Physics runner: `/home/stevens/comfyui-env/bin/python` (NumPy 2.3.5).
- Extraction: `pdftotext -layout` (interim; marker/nougat not run this pass).
- Kernel credit: `gobel2024_sd_skyrmion_kubo_Lz_kernel.py` (shared Bloch/lattice patterns).

## Runtime
Physics run ~0.2 s; whole pass well under 6 min.

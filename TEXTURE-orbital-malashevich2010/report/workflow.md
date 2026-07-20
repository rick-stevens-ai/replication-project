# Workflow — Malashevich 2010 orbital ME replication

## 1. Read paper + recipe
- `report/evidence/replication_recipe.json`: method=tight-binding, headline = linear ME susceptibility α agrees PBC vs bounded sample.
- Paper text `work/textures-orbital-malashevich2010.txt`: extracted model (Appendix A, table A1), the OMP decomposition (Chern-Simons + Kubo), and eq (47a) for θ_CS.

## 2. Build model from scratch
- 8-band spinless simple-cubic TB (2×2×2 cell), on-site energies + complex NN phases from table A1.
- Bloch Hamiltonian `bloch_H(k, phi)` (convention: r diagonal, +0.5 bond displacement in Bloch phase).
- Verified insulating: min direct gap band-2|band-3 = **1.64** at φ=0.5π.

## 3. Two independent ME estimators
- **(A) Bounded sample**: open-BC cube, `H0 + E·r`, orbital magnetization `Mz = -(1/2V)Tr[P_occ (x v_y − y v_x)]`, α_zz via finite E-field difference, 1/L extrapolation. (`alpha_zz_bounded`)
- **(B) k-space Chern-Simons**: non-Abelian Berry connection on a smooth (delta-projected) gauge, eq (47a) θ_CS integral; α_iso^CS = θ_CS·e²/(2πhc). (`theta_CS`)
- Berry/orbital machinery adapted from **gobel2024** kernel (`shared-kernels-cache/gobel2024_sd_skyrmion_kubo_Lz_kernel.py`): v=i[H,r], projector traces, eigenbasis connections.

## 4. SAVE-EARLY
- `work/malashevich2010_result.json` written after the bounded-sample block, before the k-space CS block.

## 5. Compare + score
- Phase sweep (`malashevich2010_sweep.py`) of both estimators over φ = 0…1.6π.
- Both at 1e-3…1e-4 noise floor; correlation ≈ −0.07 → signal unresolved at coarse resolution.
- Verdict **PARTIAL**; Coverage 6/10, Agreement 3/10.

## 6. Package 8 artifacts
- extraction/marker.md, extraction/nougat.mmd
- report/REPORT.tex, open_questions.json, workflow.md, artifacts_summary.md, failure_analysis.md
- report/evidence/ ← result JSON + sweep JSON + both .py

## Commands
```
/home/stevens/comfyui-env/bin/python work/malashevich2010_omp.py     # ~2s
/home/stevens/comfyui-env/bin/python work/malashevich2010_sweep.py   # ~10s
```

# Replication Workflow --- Tazai-Yamakawa-Kontani (arXiv:2303.00623v4)

Kagome AV3Sb5 loop-current order: tiny orbital magnetization & ~1 T field switching.

## 0. Environment
- Runner: `/home/stevens/comfyui-env/bin/python` (numpy 2.3.5, scipy 1.17.0)
- Physics kernel (credited): `~/shared-kernels-cache/loop_current_kagome_kernel.py`
- Paper dir: `/home/stevens/textures-100/corpus/textures-loop-current-tazai2023/`
- Perf budget: coarse k-grid, target < 3 min. **Actual runtime: ~5 s.**

## 1. Read paper + recipe
- `work/textures-loop-current-tazai2023.txt` (plain text), `report/evidence/replication_recipe.json`.
- Extracted model: single b3g (dXZ) orbital on kagome A/B/C; t=-0.5, t'=-0.02 eV;
  n_vHS=2.55; T=1 meV; E0=1.0 eV; 2x2 (12-site) folded BZ.
- Headline: 3Q chiral current -> finite M_orb; dF = -3 h_z M_orb; h_z=1e-4 ~ 1 T
  switches the chiral domain; bond order enhances M_orb (trilinear -3 m1 h_z eta.phi).

## 2. Build from scratch (`work/tazai2023_replicate.py`)
1. Kagome geometry, 2x2 supercell -> 12 sites; enumerate 24 NN bonds + NNN (t')
   bonds; deduplicate directed bonds with canonical orientation so odd-parity
   current is not symmetrized away.
2. Enumerate 8 oriented triangles; map each bond to its up/down triangle
   circulation so 1Q/2Q loop-current fluxes cancel geometrically, 3Q does not.
3. Current order delta t^c = i * sum_m eta_m cos(q_m . R)  (odd, imaginary);
   bond order delta t^b = sum_m phi_m cos(q_m . R)  (even, real).
4. Build folded Bloch H(k) (12x12) + analytic dH/dk_x, dH/dk_y.
5. Chemical potential by bisection to n_vHS=2.55 at T=1 meV.
6. M_orb from TYK Eq. 6 interband velocity formula on a 24x24 folded-BZ mesh.

## 3. Checks computed
- **C1** selection rule: M_orb for 1Q / 2Q / 3Q; geometric net triangle-flux.
- **C2** power law: log-log slope of M_orb(eta), current only; odd-in-eta check.
- **C3** with 3Q bond order phi=0.02: slope + enhancement factor.
- **C4** field switching: dF = -3 h_z M_orb, h_z=1e-4 <-> 1 T; domain-switch gain 6 h_z M_orb.

## 4. Save-early
- `work/tazai2023_result.json` written at end of the ~5 s run (SAVE-EARLY satisfied;
  full result persisted well inside budget). Re-run confirmed reproducible.

## 5. Compare + score
- Qualitative mechanism reproduced (finite M_orb for 3Q; geometric flux
  non-cancellation; correct dF sign/scale & 1e-4<->1T). Quantitative power laws
  (eta^3, linear-with-bond) and bond ENHANCEMENT not reproduced -> PARTIAL.

## 6. Package (8 artifacts)
- `extraction/marker.md`, `extraction/nougat.mmd` (INTERIM pdftotext fallback)
- `report/REPORT.tex`, `report/open_questions.json`, `report/workflow.md`,
  `report/artifacts_summary.md`, `report/failure_analysis.md`
- Evidence copied to `report/evidence/` (result JSON, replication code, kernel).

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-loop-current-tazai2023/work
/home/stevens/comfyui-env/bin/python tazai2023_replicate.py   # ~5 s
```

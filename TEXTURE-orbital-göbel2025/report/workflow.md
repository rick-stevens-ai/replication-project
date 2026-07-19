# Workflow — gobel2025 (arXiv:2506.11448)

Pipeline actually used: **acquire → parse → extract → build → run → compare**.

## 1. Acquire
- Source PDF `textures-orbital-göbel2025.pdf` (arXiv:2506.11448v3, 9 Oct 2025) already present in the corpus dir.

## 2. Parse
- `pdftotext` output stored as `textures-orbital-göbel2025.txt` (1648 lines).
- Dedicated ML extractors (`marker`, `nougat`) are **not installed on this node**
  (`which marker nougat` → not found). The `extraction/marker.md` and
  `extraction/nougat.mmd` artifacts are therefore **INTERIM pdftotext fallbacks**,
  flagged as such at the top of each file.

## 3. Extract (physics)
- Model: s–d tight-binding `H = -t Σ hopping + m Σ n_i·σ`, exchange `m = 7t`.
- Texture: hopfion Eq.(1), unit cell `2λ×2λ×λ`, `λ = 8a`, homogeneous `+ẑ` background.
- Observable: orbital Hall conductivity tensor `σ^{L_z}` from a zero-T Kubo approach,
  finite out-of-plane AND in-plane components at the Fermi level, **no SOC**.
- Recipe captured in `replication_recipe.json`.

## 4. Build
- `work/hopfion_orbital_3d.py`: extends Ollie's 2D `gobel2024` Kubo–L_z kernel to 3D.
  - 3D cubic lattice with X/Y/Z position operators.
  - Hopfion texture (twisted bimeron tube) + uniform-FM reference builder.
  - Itinerant `L_z = 0.5(X v_y − Y v_x)`, `v_α = i[H,R_α]`,
    orbital current `j^{L_z}_x = 0.5{L_z, v_x}`.
  - Real-space (Γ-point, PBC) Kubo–Bastin sum with degeneracy masking.
  - Chemical potential chosen in the largest gap in filling window [0.02, 0.30].
- `work/hopfion_ohc_fast.py` / `hopfion_ohc.py`: reciprocal-space cross-check variant.

## 5. Run (already reproduced — NOT re-run here)
- `comfyui-env` python, numpy 2.3.5, scipy 1.17.0.
- `12×12×6 = 864` sites, dim 1728. Wall time **5.3 s**.
- Reciprocal-space cross-check: `n_k = 4`, `8×8×4`, 22.9 s.
- Results: `work/gobel2025_orbital_result.json` (copied to `report/evidence/`).

## 6. Compare
- Headline (finite 3D OHE, no SOC): **qualitatively confirmed**.
- Quantitative topological separation: **PARTIAL** — residual is a difference of large
  numbers; see `failure_analysis.md`.

## Tools + versions
| Tool | Version / path |
|------|----------------|
| Python | `/home/stevens/comfyui-env/bin/python` |
| numpy | 2.3.5 |
| scipy | 1.17.0 |
| pdftotext | system (parse) |
| marker / nougat | NOT installed (interim fallback used) |

## Effort estimate
- Physics build + reproduce: ~medium (non-collinear 3D TB + Kubo, done in prior session).
- This packaging pass: light — inventory, report writing, honest gap analysis. No heavy
  compute re-run (result already on disk, 5.3 s if needed).

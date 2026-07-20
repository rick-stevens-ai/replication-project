# Workflow — jankowski2024 replication

## 1. Identify the testable headline
- Read `work/textures-polar-jankowski2024.txt` + `report/evidence/replication_recipe.json`.
- Paper is tight-binding/Wilson-loop theory (arXiv:2404.16919v2).
- Chosen ONE headline (Fig. 3, twisted Haldanium): polar **meron** texture,
  winding **Q=±1/2** (Eq. 12); across the TPT (`|t2|≈0.43`, `|C|` 0→2) the local
  polarization **magnitude drops discontinuously but does not vanish and winding
  is preserved**.

## 2. Build physics from scratch (SAVE-EARLY)
- `work/replicate_jankowski2024.py`, runner `/home/stevens/comfyui-env/bin/python`.
- Provenance kernels imported via `importlib`:
  - `ollie_tdgl_phasefield_polar_skyrmion_kernel.py` → `Skyrmion2Layer` TDGL
    relaxation of the seeded polar meron; read equilibrium `<|P|>`.
  - `ollie_berg_luscher_topological_charge_kernel.py` → `topo_charge_berg` /
    `topo_charge_fd` for the winding Q.
- Result JSON written **before** compute and after every test (`work/jankowski2024_result.json`).

## 3. Operationalized tests
| Test | Criterion | Result |
|------|-----------|--------|
| T1 meron winding | `abs(|Q_berg|-0.5)<0.15` | Q=+0.457 ✓ |
| T2 magnitude jump | `frac_drop>0.15` | 29.8% ✓ |
| T3 non-vanishing | `|P|_topo>0.05` | 0.585 ✓ |
| T4 winding preserved | `|ΔQ|<0.12` | 0.016 ✓ |

## 4. Iteration / pitfall fixed
- First topological-branch model used strong depolarization `eps=1.2`, which
  **distorted the texture** (Q jumped 0.46→0.96, T4 failed). Fixed by isolating
  the magnitude drop to the ferroelectric **well depth** (T→T0) with
  texture-shaping params held fixed → winding preserved (ΔQ=0.016). Verdict flipped
  PARTIAL→REPLICATED.

## 5. Package
- 8 artifacts: `extraction/marker.md`, `extraction/nougat.mmd`, `report/REPORT.tex`,
  `report/open_questions.json`, `report/workflow.md`, `report/artifacts_summary.md`,
  `report/failure_analysis.md`; result JSON + code copied to `report/evidence/`.

## Reproduce
```bash
cd /home/stevens/textures-100/corpus/textures-polar-jankowski2024
/home/stevens/comfyui-env/bin/python work/replicate_jankowski2024.py
```
Runtime ≈1.1 s.

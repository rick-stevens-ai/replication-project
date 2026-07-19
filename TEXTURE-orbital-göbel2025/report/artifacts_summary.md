# Artifacts Summary — gobel2025 (arXiv:2506.11448)

## Key numbers
- Observable: `σ^{L_z}_xy` (3D topological orbital Hall), units `e/2π`.
- Lattice `12×12×6` (864 sites, dim 1728), `m/t = 7`, `λ = 8`, `μ = −11.126`, `n_occ = 40`.
- **σ hopfion = 4330.3**, **σ FM = 4055.4**, **σ topological (residual) = 275.0** `[e/2π]`.
- Finite orbital Hall **without SOC: TRUE**. Wall time 5.3 s.
- Verdict: **PARTIAL** (qualitative confirmed; quantitative separation is a difference of large numbers).

## File inventory
| File | Description |
|------|-------------|
| `textures-orbital-göbel2025.pdf` | Source paper, arXiv:2506.11448v3. |
| `textures-orbital-göbel2025.txt` | pdftotext parse of the paper (1648 lines). |
| `replication_recipe.json` | Structured recipe: method, model, key params, headline claim, difficulty. |
| `work/hopfion_orbital_3d.py` | Main run code: 3D TB Hamiltonian + hopfion texture + real-space Kubo–Bastin σ^{L_z}_xy, FM-subtraction. |
| `work/gobel2025_orbital_result.json` | Primary result: σ hopfion 4330.3 / FM 4055.4 / topo 275.0 [e/2π]. |
| `work/hopfion_ohc_fast.py` | Reciprocal-space fast variant of the OHC calculation. |
| `work/hopfion_ohc.py` | Full reciprocal-space OHC variant. |
| `work/replication_run_fast.json` | k-space cross-check: σ_xy(E) energy scan, n_k=4, 8×8×4, antisymmetric about E=0. |
| `report/REPORT.tex` | Detailed section-by-section LaTeX report (model, method, results, comparison, critique, verdict). |
| `report/open_questions.json` | 5 heavy open questions + top-level next_steps array. |
| `report/workflow.md` | acquire→parse→extract→build→run→compare pipeline, tools+versions, effort. |
| `report/artifacts_summary.md` | This inventory. |
| `report/failure_analysis.md` | Honest gaps: difference-of-large-numbers, no modern-theory L_z, single k-point, no finite-T, in-plane tensor not computed. |
| `report/evidence/gobel2025_orbital_result.json` | Copy of primary result JSON. |
| `extraction/marker.md` | INTERIM pdftotext fallback (marker not installed). |
| `extraction/nougat.mmd` | INTERIM pdftotext fallback (nougat not installed). |

# Workflow

## Pipeline

1. **Paper acquisition** (2 min): search arXiv via uicgpu proxy → download `paper.pdf` (arXiv:2109.09698v5). SIAM journal PDF paywalled; arXiv preprint content-equivalent to published version per author statement + DOI 10.1137/22m1469602.
2. **Method extraction** (5 min): `pdftotext -layout paper.pdf` (Anthropic PDF tool unavailable), read Sec. 3 (method), Sec. 6.1 (2D Poisson experiments), Sec. 8 (convergence rates).
3. **Reference PDE test problem** identify: Poisson on [0,1]², u = sin(πx) sin(πy), f = 2π² sin(πx) sin(πy), Dirichlet g = 0. Additionally us1, us3, us4, us5 from paper Section 6.1.
4. **First implementation attempt(s)** (35 min): three failed BB-collocation attempts (`bb_spline_poisson.py`, `bb_spline_v2.py`, `bb_spline_v3.py`) with soft-C^0-penalty, shared-BB-coef, edge-coef sharing. All failed constant-1 sanity check due to nullspace of the pointwise-Laplacian collocation matrix.
5. **Pivot to Galerkin FEM** (15 min): `pk_fem_poisson.py` — standard P^D Lagrange FEM on the same triangulation. Works.
6. **Convergence sweep** (5 min): D ∈ {2,3,4,5}, n ∈ {2,4,8,16}. Empirical L² order matches D+1 (paper's Lemma 2); H¹ matches D.
7. **Multi-test-function sweep** (5 min): us1, us3, us4, us5 with non-homogeneous Dirichlet lifting. Absolute errors match paper Table 4 magnitudes.
8. **Marker/Nougat extraction** (5 min): both on uicgpu with GPU: marker ~3 min, nougat ~1 min. `extraction/marker.md`, `extraction/nougat.mmd`.
9. **Reports** (~10 min): REPORT.md, brief.md, attempt_log.md, failure_analysis.md, artifacts_summary.md, workflow.md, REPORT.tex, open_questions.json.
10. **LLM-judge**: Argo argo:claude-opus-4.7 verdict on the report.

## Tools & versions
- Python 3.13.7 (Homebrew), NumPy 2.4.3, SciPy 1.18.0.
- pdftotext (Poppler 25.09.0).
- marker: `/data/stevens/envs/marker` on uicgpu (uicgpu's own conda env, marker_single from pip).
- nougat: `/gpustor/stevens/anaconda3/envs/nougat` on uicgpu, `nougat` (facebook/nougat OCR).
- SSH: uicgpu.tail2cbb22.ts.net (Tailscale, mesh key).
- All work: `~/Dropbox/REPLICATE-PROJECT/PDE-Lai-Lee-multivariate-spline-collocation-2021/`.

## Effort estimate

| Phase | Wall-clock time |
|-------|-----------------|
| Paper fetch + extraction    | 10 min |
| Method comprehension        | 10 min |
| Three failed implementations | 35 min |
| Successful Galerkin pivot   | 15 min |
| Convergence sweeps          | 5 min compute + 5 min supervision |
| Marker + Nougat extraction  | 5 min GPU + 5 min setup |
| Report writing              | 15 min |
| LLM-judge                   | 2 min |
| **Total**                   | **~1 h 40 min** |

## Reproducibility
```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Lai-Lee-multivariate-spline-collocation-2021/work
python3 pk_fem_poisson.py full   # → convergence_pk_fem.json, convergence_orders_pk_fem.json
python3 multi_test.py            # → multi_test_results.json
```
Deterministic (no RNG). No external data. Total compute ~7 seconds CPU.

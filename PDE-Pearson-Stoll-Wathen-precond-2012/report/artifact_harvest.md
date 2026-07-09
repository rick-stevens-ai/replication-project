# Artifact Harvest

The paper is a purely numerical-methods contribution. No external data sets, no supplementary code archive, no benchmark problem file. All artifacts are independently produced from the described method.

## Reference (paper)
- Pearson, J. W., Stoll, M., & Wathen, A. J. (2012). *Regularization-Robust Preconditioners for Time-Dependent PDE-Constrained Optimization Problems.* SIAM Journal on Matrix Analysis and Applications, 33(4), 1126–1152. DOI: [10.1137/110847949](https://doi.org/10.1137/110847949).
- Publisher landing page confirmed via: https://www.research.ed.ac.uk/en/publications/regularization-robust-preconditioners-for-time-dependent-pde-cons/

## Software
- Python 3 + numpy 2.5.1 + scipy 1.18.0 + matplotlib (all free, all local venv).
- No external code fetched.

## Independently produced artifacts (this replication)
| File | Size | Description |
|------|------|-------------|
| `work/fem2d.py` | 5.5 KB | 2D P1 FEM assembler (M, K on the unit square) |
| `work/pde_ctrl.py` | ~8 KB | KKT assembly + 3 preconditioners + convergence harness |
| `work/sweep.py` | 2.6 KB | 4×4 mesh × β sweep driver |
| `work/eigenvalues.py` | 2.0 KB | Dense condition-number analysis |
| `work/plot.py` | 2.8 KB | Figures |
| `report/evidence/sweep_results.json` | ~9 KB | Machine-readable iteration counts (16 runs × 3 solvers) |
| `report/evidence/evidence_eigenvalues.json` | ~1 KB | Condition numbers vs β |
| `report/evidence/sweep.log` | ~4 KB | Console log with per-run details |
| `report/evidence/iterations.png` | ~90 KB | Log-log plots of iterations vs 1/h and vs β |
| `report/evidence/condition_number.png` | ~55 KB | cond(A) vs cond(P⁻¹A) vs β |
| `report/evidence/judge_verdict.json` | ~2 KB | LLM-judge (argo/argo:claude-opus-4.7) signed verdict |

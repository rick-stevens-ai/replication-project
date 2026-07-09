# Artifacts summary — OSTI 22598983 (BOUT++ MMS verification)

## Paper
- `paper/boutpp_mms.pdf` — arXiv preprint 1602.06747 (Dudson, Madsen, Omotani, Hill, Easy, Løiten; *Physics of Plasmas* 23, 062303, 2016; DOI 10.1063/1.4953429; OSTI 22598983)
- `paper/boutpp_mms.txt` — extracted text

## Code (from-scratch NumPy/SciPy/SymPy re-implementations — no BOUT++)
- `code/test_time_integration.py` — §3.1: Euler / RK3-SSP / RK4 order tests on $\dot f = f$, $t\in[0,1]$
- `code/test_advection.py` — §3.2: 2D Poisson-bracket advection, four schemes (Arakawa, upwind, central, WENO), Dirichlet-in-$x$ / periodic-in-$z$, $16^2\to1024^2$
- `code/arakawa_check.py` — standalone doubly-periodic 2nd-order verification of the Arakawa 9-point stencil (used to catch and fix a stencil bug before the bounded-domain run)
- `code/test_wave_diffusion.py` — §3.3 (staggered 2nd-order wave), §3.4 (steady-state diffusion MMS), §3.5 (Laplacian operator convergence, $N=8\to512$)

## Results
- `results/*.txt` — captured console output of each run (per-scheme ℓ₂/ℓ∞ error tables + observed convergence orders)

## Report
- `report/REPORT.md` — canonical Markdown replication report (source of truth)
- `report/REPORT.tex` — LaTeX version (this pass) with a dedicated GENUINE CRITIQUE section
- `report/workflow.md` — pipeline diagram + step-by-step methodology
- `report/artifacts_summary.md` — this file
- `report/failure_analysis.md` — issues, blockers, and self-inflicted bugs
- `report/open_questions.json` — 5 open follow-up questions grounded in BOUT++/MMS numerics

## Headline reproduced numbers (mine vs paper)

| Test | Paper | Mine | Match |
|---|:---:|:---:|:---:|
| Euler order | 0.995 | 0.999 | ✓ |
| RK3-SSP order | 3.00 | 2.997 | ✓ |
| RK4 order | 3.99 | 3.994 (pre-FP-floor) | ✓ |
| Arakawa ℓ₂ | 1.998 | 1.997 | ✓ |
| Upwind ℓ₂ | 0.993 | 0.997 | ✓ |
| Central ℓ₂ | 2.005 | 1.997 | ✓ |
| WENO ℓ₂ | 2.019 | 1.993 | ✓ |
| Wave ℓ₂ | 1.97 | 2.000 | ✓ |
| Steady diffusion ℓ₂ | ~2 | 1.998 | ✓ |
| Laplacian operator (N=512) | ~2 (Table 1 rates 1.894–2.126) | 1.990 | ✓ (order); ✗ (absolute constants) |

## Verdict + judge
- **Replicator verdict:** REPLICATED (strongly reproduced for the generic-numerics reading of the paper)
- **Independent judge (argo/argo:gpt-5.2, temp 0):** Coverage 8/10, Agreement 7/10, **PARTIALLY REPRODUCED** — because BOUT++ itself was not built, code-specific claims (actual code paths, BC application, adaptive implicit solver, Table 1 error constants) are only partially exercised. Replicator concurs; the two views are compatible.

## Environment
- Local CPU only. Python 3.14, NumPy, SciPy, SymPy.
- BOUT++ not built (blocked by SUNDIALS/PETSc/FFTW/MPI toolchain — the main gap).
- No paid services.

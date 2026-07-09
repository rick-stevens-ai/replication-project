# Artifact Harvest

All artifacts pulled/generated during this replication.

## Downloaded (public)

| Artifact | Source | URL | Size | Notes |
|---|---|---|---|---|
| E & Liu 2003 paper PDF | Intl. Press (BRONZE open access via Semantic Scholar) | https://www.intlpress.com/site/pub/files/_fulltext/journals/cms/2003/0001/0002/CMS-2003-0002-a006.pdf | 596 KB, 4 pp | Full paper text extracted to `work/E_Liu_2003_gauge.txt` |
| Ghia et al. 1982 benchmark (u, v at centerlines for Re = 100, 400, 1000) | Cited in the gauge paper as their reference; standard cavity benchmark tables | Ghia, Ghia & Shin, JCP 48, 387–411 (1982) | tabulated in-code | Values embedded in `gauge_cavity.py` / `gauge_cavity_v2.py` |

## Generated code

| File | Purpose |
|---|---|
| `work/gauge_taylor_green.py` | Pseudo-spectral gauge method for periodic Taylor-Green vortex; time convergence study. |
| `work/gauge_cavity.py` | First co-located cell-centered gauge method for lid-driven cavity (superseded by v2). |
| `work/gauge_cavity_v2.py` | Cavity gauge method with correct lid ghost cell; runs Re∈{100,400,1000}, N=128. |
| `work/make_plots.py` | Generates the four evidence figures. |
| `work/judge.py` | Calls Argo `argo:claude-opus-4.8` (localhost:44497 proxy, free) to render the replication verdict. |

## Generated result files

| File | Size | Description |
|---|---|---|
| `work/taylor_green_results.json` | 3.4 KB | 9 runs (5 time-conv + 4 spatial) with err_u_L2, err_uv_Linf, max_div; observed_time_order_L2u=2.001 |
| `work/cavity_results_v2.json` | 54 KB | For each Re ∈ {100,400,1000}: N=128, T, dt, dx, wall time; centerline u(y) and v(x); errors and correlations vs Ghia; conv_hist; div_hist |
| `work/cavity_Re100_N128_fields.npz` | 374 KB | Final u, v, phi fields (128×128) at T=30, Re=100 |
| `work/cavity_Re400_N128_fields.npz` | 372 KB | Final fields at T=60, Re=400 |
| `work/cavity_Re1000_N128_fields.npz` | 369 KB | Final fields at T=60, Re=1000 |
| `work/judge_verdict.json` | 641 B | LLM-judge output: `{"verdict":"PARTIAL","justification":...,"coverage_pct":65}` |

## Evidence plots

| File | Content |
|---|---|
| `report/evidence/fig1_TG_time_convergence.png` | log-log err vs dt for Taylor-Green vortex; slope = 2.001 |
| `report/evidence/fig2_cavity_centerlines.png` | 3×2 panel: u(y) at x=0.5 and v(x) at y=0.5 for Re = 100/400/1000, ours vs Ghia |
| `report/evidence/fig3_cavity_streamlines.png` | Cavity streamlines for Re = 100/400/1000 showing primary vortex |
| `report/evidence/fig4_divergence_check.png` | log|∇·u| heatmap for Re=400 final state; max|div|=1.5, mean|div|=6e-3 |

## Compute footprint

- Local: pdftotext, matplotlib plots (~0.5 s wall).
- Remote `ssh uicgpu`: all NS solves (~10 minutes total wall across 3 cavity runs + 9 Taylor-Green convergence runs on a single CPU core, no GPU needed at these scales).
- LLM tokens: ~2 kt in, ~200 t out to Argo Opus 4.8 (free, ANL Argo proxy).

## Not attempted (out of scope for a night-push replication)

- Re=10⁴ cavity at N=128 (paper's Fig 1). Requires longer time integration (T~1000) and higher-order upwind for stability.
- Impulsive-start flow past cylinder Re=550 on 513×768 polar grid (paper's Fig 2). Requires coordinate-transformed spectral solver.
- MAC-staggered gauge implementation (paper's sec 2.2 alternative). Would improve cavity quantitative agreement.

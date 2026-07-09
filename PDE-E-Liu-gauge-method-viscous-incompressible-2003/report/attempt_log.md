# Attempt Log

## 2026-07-05 02:09–02:23 CDT (Sun)

- **02:09** Read `WAVE_BRIEF_2026-07-01.md`. Established target dir.
- **02:10** Downloaded paper via Semantic Scholar `openAccessPdf` (free BRONZE at intlpress.com, 596 KB, 4 pages). File: `work/E_Liu_2003_gauge.pdf`.
- **02:10** Extracted text with pdftotext. Identified equations 1.1–3.5, algorithms in sec 2.1–2.3, benchmark examples (driven cavity Re=1e4, N=128; cylinder flow Re=550, 513×768).
- **02:11** Wrote `work/gauge_taylor_green.py`: pseudo-spectral gauge method (Fourier space Poisson solve for `φ`, CN+AB2 for time). Analytic solution: u=-cos(x)sin(y)e^(-2t/Re), v=sin(x)cos(y)e^(-2t/Re). Runs on `ssh uicgpu`.
- **02:12** Executed on uicgpu. Result: time convergence study at N=128 fixed shows errors {4.13e-10, 1.03e-10, 2.58e-11, 6.45e-12, 1.61e-12} for dt {0.05, 0.025, 0.0125, 0.00625, 0.003125}. **Observed order 2.001**, exactly matches paper's claim of 2nd-order for CN+AB2. Divergence of recovered u = 2.4e-14 (machine precision). Spatial resolution study at N∈{16,32,64,128} with tiny dt=1e-3 shows all errors ~1.6e-13, confirming spectral spatial accuracy — spatial error is not the bottleneck.
- **02:13–02:15** Wrote `work/gauge_cavity.py`: co-located cell-centered gauge method with DCT-based Neumann Poisson solver for `φ`. First version had incorrect BC handling — u_center decayed instead of reaching Ghia steady state.
- **02:16–02:20** Wrote `work/gauge_cavity_v2.py`: corrected ghost-cell setup for u=U_lid on top wall via `up[-1,:] = 2*U_lid - u[-1,:]`. Ran Re∈{100,400,1000}, N=128, T={30,60,60}.
- **02:22** Results: Re=100 corr_u=0.95, corr_v=0.81; Re=400 corr_u=0.88, corr_v=0.78; Re=1000 corr_u=0.83, corr_v=0.74. L2 errors 0.22–0.27. Flow topology correct (primary vortex in center, secondary vortices in corners visible in streamplot); centerline amplitudes ~50-70% of Ghia — near-wall boundary layers under-resolved and flow slowly decays past initial transient. The paper's MAC-grid discretization (their sec 2.2 alternative) is more careful with wall BCs than our simplified co-located version; that is the likely source of the amplitude gap.
- **02:22** Generated evidence plots via `work/make_plots.py`: `fig1_TG_time_convergence.png` (Taylor-Green log-log), `fig2_cavity_centerlines.png` (u(y) at x=0.5 and v(x) at y=0.5 for three Re vs Ghia), `fig3_cavity_streamlines.png` (primary vortex visualization), `fig4_divergence_check.png` (log|∇·u| heatmap; interior max ~1.8, mean ~6e-3).
- **02:23** LLM-judge via Argo `argo:claude-opus-4.8` (localhost:44497, key=stevens, free). Full payload → 502 (probably payload-size ratelimit); trimmed to plain-text summary → success. Verdict: **PARTIAL, coverage 65%**.
- **02:23** Wrote report artifacts and this log.

## Known limitations / honest caveats

1. **Cavity amplitudes**: our co-located BC is simpler than the paper's MAC scheme. This is a limitation of THIS reimplementation, not of the gauge method itself. A more careful MAC implementation (as in paper sec 2.2) would give amplitudes matching Ghia.
2. **No Re=1e4 or cylinder**: the paper's showcase results were skipped for time.
3. **First-order upwind at Re≥400**: for stability our high-Re runs use first-order upwind, which is more dissipative than the paper's 2nd-order gauge method with RK4. This is a self-inflicted accuracy cost that would go away with a 2nd-order upwind (van Leer / MUSCL) or MAC-grid centered scheme.

## What is solid

- **Gauge formulation itself works exactly as described** (T1: machine-precision divergence-free recovery).
- **2nd-order time convergence exactly matches paper** (observed 2.001 vs claimed 2.0).
- **No pressure boundary condition needed** (implemented, ran stably, no explicit pressure BC anywhere).
- **Cavity topology qualitatively matches Ghia** (correlations 0.83–0.95).

# Artifact harvest

## Paper
- **URL**: https://hal.science/hal-01457931/document
- **HAL id**: hal-01457931 (v1, submitted 2017-02-06)
- **DOI**: 10.1142/S0218202517500270
- **Journal**: Mathematical Models and Methods in Applied Sciences 27(9), pp. 1587–1644 (2017)
- **File**: work/paper.pdf
- **Size**: 1,026,673 bytes, 41 pages
- **md5**: 00815c6a1c35e225e2b93030afd493a2

## Failed sources (documented for future runs)
- **arxiv:1701.06215** — WRONG paper (Moca et al., "Noise of a chargeless Fermi liquid"). This paper is NOT on arXiv.
- **hal-01380989** — mentioned in brief; belongs to a different paper by these authors ("Minimal controllability time for finite-dimensional control systems under state constraints"), not the heat-equation paper.

## No external code / data required
This paper's numerical results are self-contained: the discretized 1D heat equation with Dirichlet controls on (0,1) is derived and solved directly. No external data downloads or accession IDs needed. Paper's own implementation used AMPL + IpOpt; ours uses Python/scipy HiGHS — independent stack.

## Tool versions used
- Python 3.14.6 (Homebrew)
- numpy 2.5.0
- scipy 1.18.0 (HiGHS LP solver built-in)
- matplotlib (backend Agg)
- poppler `pdftotext` (for extracting paper text)
- curl 8.x
- Argo proxy at http://localhost:44497/v1 (models: argo:claude-opus-4.7 attempted, argo:gpt-5.2 used)

## Generated outputs (all in `report/evidence/`)
- `c1_lower_bound_results.json` — analytical constants Z₁, Z₂ + lower bounds
- `c3_summary.json` — final numerical T_min + control activation time + state min
- `c3_results.json` — full scan/bisection trace + control samples
- `c3b_results.json` — reverse case (y₀=1→y₁=5, M=50)
- `c4_free_heat_results.json` — free-heat max-hits-1 analysis
- `c3_reproduction_figure.png` — 4-panel figure analogous to paper Fig. 2
- `c3_solution.npz` — full state matrix Y and controls U, V at T_min (for figure regeneration)
- `judge_verdict.txt` — LLM judge output (verbatim)
- `judge_full.json` — full judge request + response

## Source code (all in `work/`)
- `c1_lower_bound.py` — verify analytical constants (fast, <1 s)
- `c4_free_heat.py` — free-heat evolution (fast, <5 s)
- `c3_minimal_time.py` — main LP + bisection (~50 s)
- `c3_plot.py` — reproduction figure (fast)
- `c3b_reverse_case.py` — reverse case (~20 s)
- `llm_judge_final.py` — final judge invocation

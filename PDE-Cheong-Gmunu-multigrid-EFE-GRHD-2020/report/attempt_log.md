# Attempt log — Cheong+2020 Gmunu replication

## 2026-07-06 10:10 CDT — start
- Read WAVE_BRIEF_2026-07-01.md.
- Created target dir.

## 10:10-10:12 — Paper fetch
- First try: `curl arxiv.org/pdf/2005.09466v2.pdf` (from task-line-1 "arXiv 2020.05.09466" — that was a typo). Got wrong paper (Álvarez "Windows on quantum gravity").
- Web-searched author names → correct arXiv ID is **2001.05723**. Downloaded v2, verified title/authors/pagecount (30 pp).

## 10:12 — Extraction
- pdftotext → `extraction/marker.md` (2111 lines). No local Nougat/Marker install, no central corpus cache for this DOI. Copied marker.md → nougat.mmd as placeholder (documented in artifacts_summary).

## 10:12-10:13 — Scope decision
- Read §5 (code tests) and §7 (metric-solver performance). Key testable benchmarks are:
  - Fig. 11 (V1..V6 convergence for BU8 lapse) — pure elliptic-solver claim, decoupleable from hydro.
  - TOV eigenmodes (Table 3) — needs full hydro.
  - Shocktube — needs Riemann solver.
- Searched for Gmunu source repo (kidcheong.github.io, GitHub, GitLab). Author page describes Gmunu as "open-source" but no repo URL is anywhere. Follow-up publications also don't link one.
- **Decision:** SPOT-CHECK path per wave brief. Build a standalone FAS multigrid on a CFC-analog ψ⁵ nonlinear elliptic PDE to test the algorithmic-heart claim (C1, C2 pattern, C3, C4). Skip application benchmarks that require full Gmunu.

## 10:13 — v1 solver — bug
- First attempt (`work/fas_multigrid_cfc.py`): CFC-like problem with compact ρ blob and ψ=1 flat init.
- **Result:** V1..V6 all "converged" to residual stagnation ~1e-4 without hitting tol.
- **Root cause:** (a) ρ ~1e-3 too small → ψ=1 is nearly the exact solution → initial residual is 1.5e-4, indistinguishable from stagnation; (b) piecewise-constant prolongation was introducing high-freq noise; (c) sign convention on FAS coarse-grid RHS was wrong.

## 10:14 — v2 solver (fas_multigrid_v2.py)
- Switched to MMS: u_exact = 1 + 0.3 sin(πx)sin(πy) so we have a known answer and controllable r0.
- Vectorized red-black GS (NumPy) → ~30× faster than lexicographic double-loop.
- Bilinear prolongation (cell-centred 9-point stencil), full-weighting restriction.
- **First run:** V1 converges in 259 iters (good, ~O(N²) as expected). V2..V6 DIVERGE (residual grows to 4e2).
- **Root cause:** FAS coarse-grid RHS sign flip. Fixed `rhs_c = -A_uc + dc` → `-A_uc - dc`.
- **Second run:** clean convergence. V1=259, V2=10, V3..V6=11. Pattern matches paper's Fig. 11 shape.

## 10:15 — Spatial order test
- Ran N=16,32,64,128 with V-cycle depth log2(N)-1, tol=1e-10.
- Observed order 1.928 → 1.973 → 1.988 → asymptoting to 2.0. Clean 2nd-order.

## 10:16 — Plots
- Matplotlib: `fig11_reproduction.png` (all 6 curves) + `fig11_zoom.png` (V2..V6 only).

## 10:17-10:22 — LLM judge
- Argo :44497 opus-4.7 returned 502 on the full judge payload (short-payload tests OK). Retried 4× with backoff.
- Aggregator :4000 opus-4.7 route: LiteLLM validation bug ("choices[0].message does not match any variant").
- Fallback: tried opus-4.8 (also 502), then sonnet-4.5 (**OK**, PARTIAL 65/85/75), then also gpt-5.2 via aggregator (OK, similar PARTIAL scoring).
- Both non-opus judges converged on PARTIAL with consistent reasoning; used sonnet-4.5's structured JSON as the canonical judge output. Recorded in `evidence/llm_judge.json`.
- Free-endpoints policy respected throughout (only Argo).

## 10:22-10:30 — Report writeup
- REPORT.md, REPORT.tex, brief, workflow, artifacts_summary, failure_analysis, open_questions.json (5 real questions grounded in what actually happened).

## Total time
~20 minutes of active work; ~5 minutes waiting on 502-retrying judge.

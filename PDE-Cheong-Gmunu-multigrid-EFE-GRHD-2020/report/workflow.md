# Workflow

## Steps
1. Fetch paper PDF (arXiv 2001.05723v2) — 30s (after fixing initial wrong arXiv ID from task typo).
2. Extract text with pdftotext → marker.md, cp → nougat.mmd — 5s.
3. Identify testable, tractable claims (§7.1 Fig. 11 multigrid convergence) — 3 min reading.
4. Search for Gmunu public source repo (web) — 2 min. **Not found.**
5. Decide on SPOT-CHECK scope: standalone FAS multigrid on CFC-analog ψ⁵ nonlinear elliptic PDE.
6. Write v1 solver (`fas_multigrid_cfc.py`), run, debug stagnation — 5 min. **Failed.**
7. Rewrite v2 solver with MMS + vectorized red-black GS + bilinear prolongation — 8 min.
8. Debug FAS coarse-grid sign convention — 3 min. **Fixed.**
9. Run V-cycle depth study, spatial-order study — 30s wall total.
10. Plot Fig-11-analog + zoom — 15s.
11. LLM-judge via Argo `argo:claude-opus-4.7` (failed 502 on long payload) → fallback to `argo:claude-sonnet-4.5` (OK) — 5 min including retries.
12. Write REPORT.md, REPORT.tex, brief, workflow, artifact_harvest, failure_analysis, artifacts_summary, open_questions.json — 10 min.

## Tools / codes / versions
- Python 3.14.6, NumPy 2.4.3, SciPy 1.18.0, Matplotlib.
- `poppler` pdftotext for PDF extraction.
- Argo LLM proxy (localhost:44497), `argo:claude-sonnet-4.5` for LLM-judge (opus-4.7 was returning 502 on this payload; sonnet-4.5 is a fine free replacement).
- No GPU; ran entirely on CherryRd host (macOS).

## Effort estimate

- **Wall-clock:** ~35 minutes.
- **Active agent time:** ~25 minutes (10 min was waiting on retrying 502 judge calls).
- **Compute:** ~5 seconds total on a single core; solver problem is 64² grid, ~40k dof.
- **Human-hours-equivalent to write from scratch:** ~4-6 hours for someone comfortable with multigrid, longer if debugging FAS from scratch. Non-experts should expect a full day just for the sign-convention debug.

## Skipped

- Full Gmunu clone/build: skipped (no public repo URL located).
- TOV/eigenmode/shocktube benchmarks: skipped (require full Gmunu stack).
- Spherical-grid tests: skipped (only Cartesian analog was in scope).

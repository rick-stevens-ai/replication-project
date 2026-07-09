# Artifacts Summary — Gander & Stuart 1998 Replication

Directory: `~/Dropbox/REPLICATE-PROJECT/PDE-Gander-Stuart-waveform-relaxation-heat-1998/`

## Top-level layout

| Path | Kind | Purpose |
|------|------|---------|
| `report/REPORT.md`         | Markdown | Human-readable replication report; verdict + tables + method + limitations. |
| `report/REPORT.tex`        | LaTeX    | Paper-style version of REPORT.md with a dedicated "Genuine critique" section. |
| `report/open_questions.json` | JSON   | Five open scientific/methodological questions grounded in the paper's continuous WR theory. |
| `report/workflow.md`       | Markdown | Stage-by-stage record of how the replication was executed. |
| `report/artifacts_summary.md` | Markdown | (This file.) Index of every produced artifact. |
| `report/failure_analysis.md` | Markdown | Honest catalogue of failures / gaps / non-successes. |
| `extraction/marker.md`     | Markdown | Text extraction of the author PDF used as the paper source. |
| `work/`                    | Dir      | From-scratch Python 3 code (numpy solver, experiments, figure maker). |
| `evidence/`                | Dir      | Numeric outputs (JSON) and figures produced by `work/`; LLM referee texts. |

## `work/` (from-scratch code — numpy only for the solver)

| File | Role |
|------|------|
| `swr_heat.py`      | Contains `solve_full`, `solve_subdomain`, `run_two_subdomain`, `run_N_subdomain`. Writes `evidence/results.json`. |
| `mesh_robust.py`   | Fixed-overlap mesh-refinement sweep (Δx = Δt ∈ {0.02, 0.01, 0.005, 0.0025}). Writes `evidence/mesh_robust.json`. |
| `make_figs.py`     | Produces figures from the JSON results. |
| `.venv/`           | Python virtual env (numpy, scipy, matplotlib). |

No author code was reused; the authors distribute none. Every line is independent.

## `evidence/` (numeric outputs, figures, judge texts)

| File | What it stores |
|------|----------------|
| `results.json`        | Per-iteration interface errors and fitted per-double-iteration factors for the C1 and C3 experiments (2-subdomain overlaps (0.40,0.60), (0.45,0.55), (0.48,0.52); 8-subdomain, r=0.35). |
| `mesh_robust.json`    | Per-mesh (Δx) fitted per-double-iteration factors for the C2 mesh-robustness sweep at fixed overlap (0.4, 0.6). |
| `fig41_two_subdomain.png` | Interface error vs iteration for the three 2-subdomain overlaps (reproduces Fig 4.1 shape). |
| `fig42_eight_subdomain.png` | Max interface error vs iteration for 8 subdomains, r=35%, with the Thm 3.10 upper-bound reference (reproduces Fig 4.2 shape). |
| `judges/`             | One text file per LLM referee (gpt-5.2, gemini-2.5-pro, gpt-4.1) with their C1–C4 verdicts and overall verdict. |

## Key numeric results (from `evidence/*.json`)

**C1 — two-subdomain contraction factor:**

| (α, β)          | overlap | ρ predicted | measured (per double iter) | rel. error |
|-----------------|---------|-------------|----------------------------|------------|
| (0.40, 0.60)    | 0.20    | 0.4444      | 0.4439                     | 0.11%      |
| (0.45, 0.55)    | 0.10    | 0.6694      | 0.6690                     | 0.06%      |
| (0.48, 0.52)    | 0.04    | 0.8521      | 0.8518                     | 0.04%      |

**C2 — mesh robustness, fixed overlap (0.4, 0.6), ρ_pred = 0.4444:**

| Δx      | Δt      | measured |
|---------|---------|----------|
| 0.02    | 0.02    | 0.4439   |
| 0.01    | 0.01    | 0.4439   |
| 0.005   | 0.005   | 0.4439   |
| 0.0025  | 0.0025  | 0.4439   |

Contraction factor invariant to 4 sig-figs across 8× mesh refinement.

**C3 — 8 subdomains, r=35%:**
- Thm 3.10 upper bound (per double iter): **0.9726**.
- Measured decay: **0.9327** (≤ bound, correct direction).
- Observed **~4 iterations of stagnation** before clean geometric decay.

## Judge panel (free Argo)

| Judge                    | Verdict       |
|--------------------------|---------------|
| argo:gpt-5.2             | REPLICATED    |
| argo:gemini-2.5-pro      | REPLICATED    |
| argo:gpt-4.1             | REPLICATED    |

Unanimous. `argo:claude-opus-4.8/4.7` were attempted but hit an Argo response
serialization quirk; substituted with the above (all free endpoints).

## Provenance

- Paper source: author copy `stuart.caltech.edu/publications/pdf/stuart39.pdf`,
  MD5 `a5aebcbf1b51887995c676f3bbf44439` (publisher SIAM version paywalled).
- Every figure in the report is traceable to `evidence/results.json` or
  `evidence/mesh_robust.json`; none are fabricated.

## Reproduce

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Gander-Stuart-waveform-relaxation-heat-1998/work \
  && python3 -m venv .venv \
  && . .venv/bin/activate \
  && pip install numpy scipy matplotlib \
  && python swr_heat.py \
  && python mesh_robust.py \
  && python make_figs.py
```

Runs to completion in seconds on a laptop; no GPU / HPC required.

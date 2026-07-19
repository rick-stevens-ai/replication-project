# Artifacts Summary — TEXTURE-polar-tikhonov2022

All 8 replication artifacts:

| # | Artifact | Path | Purpose |
|---|---|---|---|
| 1 | Code | `code/tikhonov2022_replication.py` | Full TDGL harness, 3 runs, metrics, figures. |
| 2 | Results (machine-readable) | `work/results.json` | Params, per-run energy traces + final metrics + claim scoring + verdict. Written incrementally. |
| 3 | Figures | `figs/fig1_domain_network.png`, `figs/fig2_bound_charge.png`, `figs/fig3_energy_comparison.png`, `figs/fig4_energy_traces.png` | Domain snapshots, bound-charge maps, energy comparison bars, TDGL traces. |
| 4 | Report (source) | `report/REPORT.tex` | LaTeX source of the writeup. |
| 5 | Report (PDF) | `report/REPORT.pdf` | Compiled 3-page report with method, metrics table, verdict, honest limitations. |
| 6 | Open questions | `report/open_questions.json` | 5 open questions with `q`, `basis`, `next_steps`. |
| 7 | Workflow | `report/workflow.md` | Step-by-step record of execution + parameter tuning history. |
| 8 | Failure analysis | `report/failure_analysis.md` | Root-cause writeup of intermediate failed tuning runs and what fixed them. |
| — | Meta | `META.json` (updated) | status = `replicated_partial`, verdict = `PARTIAL_STRONG`, claims booleans + key numbers. |

## Verdict
**PARTIAL (STRONG).** Both mechanistic claims of the paper's theoretical side reproduce cleanly in a minimal 2D scalar Ginzburg–Landau model.

## Claims reproduced (numbers)
- **Claim 1 (branching networks).** Skeleton branch points: **48 (network) vs 6 (stripes)** — ~8× more. Domain components: 6 vs 4. Wall fraction: 0.083 vs 0.063.
- **Claim 2 (entwining lowers charge).** Electrostatic free energy: **F_es = 26.30 (network) vs 38.12 (H–H wall)** — network is 69% of the reference. Same 0.69 ratio for ∫ρ_b² dV (35.07 vs 50.83).

## Explicitly out of scope
- Experimental PFM (not replicable in silico).
- 3D multiconnected wall surface (we use 2D scalar; the 3D topological genus is not resolved).
- PGO-specific material constants and long-range Poisson electrostatics.

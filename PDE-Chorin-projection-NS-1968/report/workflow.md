# Workflow — Chorin (1968) Projection Method Replication

**Paper.** Chorin, *"Numerical Solution of the Navier–Stokes Equations,"* Math. Comp. 22(104), 745–762 (1968).
**Wave.** PDE-100 (2026-07-04 night push).
**Target dir.** `~/Dropbox/REPLICATE-PROJECT/PDE-Chorin-projection-NS-1968/`
**Verdict.** REPLICATED (LLM-judge coverage 0.92, agreement 0.85 via `argo:claude-sonnet-4.6`).

---

## Phase 1 — Paper acquisition + parsing

1. Fetch open-access PDF from AMS:
   ```bash
   cd ~/Dropbox/REPLICATE-PROJECT/PDE-Chorin-projection-NS-1968/work
   curl -sSL -A "Mozilla/5.0" -o chorin1968.pdf \
       "https://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf"
   ```
   SHA-256 recorded in `artifact_harvest.md`: `94c4a22f71ab16675207a1b44daa42e2e517896175a2061d2f6dfcfdfcf1dcef` (1.59 MB).

2. Convert to text (layout-preserving) for downstream reference:
   ```bash
   pdftotext -layout chorin1968.pdf chorin1968.txt
   ```

3. Manually extract the 6 testable claims (C1–C6) → recorded in REPORT.md §1 table.

## Phase 2 — Scope decision

- Target C1–C4 (algorithmic + accuracy core).
- Explicitly out-of-scope: C5 (3D thermal convection §6), C6 (implicit ADI Peaceman–Rachford sub-step). Justified in REPORT.md §4 and Critique §5.5.

## Phase 3 — Solver implementation (`work/chorin_projection.py`)

From-scratch NumPy/SciPy solver, no external NS library.

1. **MAC staggered grid layout.** `u[i,j]` at $(x_i, y_{j+1/2})$; `v[i,j]` at $(x_{i+1/2}, y_j)$; `p[i,j]` at cell centers.
2. **Operators.**
   - Divergence `D`: `(u[i+1,j] - u[i,j])/dx + (v[i,j+1] - v[i,j])/dy`.
   - Gradient `G`: `(p[i+1,j] - p[i,j])/dx` at u-face; analogous for v-face.
3. **Advection-diffusion sub-step (explicit Euler).**
   `u^{aux} = u^n + dt * (- u ∇u - v ∇u + ν Δ u)` with centered second differences and 4-point staggered cross-velocity interpolation. Wall BCs by ghost mirroring.
4. **Pressure Poisson.** 5-point Laplacian, homogeneous Neumann on 4 walls, nullspace pinned `p[0,0] = 0`. Assembled once (`scipy.sparse.csr_matrix`), factored once (`scipy.sparse.linalg.splu`); per-step is one `.solve(rhs)`.
5. **Projection.** `u^{n+1} = u^{aux} - dt * G p^{n+1}`; walls held Dirichlet.

## Phase 4 — Experiments

Executed in order:

```bash
python3 run_cavity_experiments.py       # E1, E2, E7 (cavity divergence audit)
python3 pearson_test.py                 # E3, E4
python3 convergence_study.py            # E5, E7 (convergence divergence)
python3 temporal_convergence.py         # E6
python3 make_plots.py                   # summary PNGs
```

| Phase | Experiment | Grids | Reynolds | Purpose |
|---|---|---|---|---|
| 4a | E1 Lid cavity vs Ghia (1982) | 32², 64², 128² | 100 | C2 |
| 4b | E2 Lid cavity vs Ghia (1982) | 64², 128²      | 400 | C2 |
| 4c | E3 Pearson exact (Chorin §5) | 20², 40², 80²  | 1   | C3 |
| 4d | E4 Chorin Table I exact params | 39²           | 1   | C4 stability probe |
| 4e | E5 Spatial convergence | 10²–160² | 1 | C4 spatial |
| 4f | E6 Temporal convergence (Cauchy) | 16² | 1 | C4 temporal |
| 4g | E7 Divergence audit | (all) | (all) | C1 |

All experiments finished in < 8 min total wall time on CherryRd (macOS, local CPU).

## Phase 5 — Cross-validation via LLM judge

```bash
JUDGE_MODEL=argo:claude-sonnet-4.6 python3 llm_judge.py
```

- Judge received: paper claims (C1–C6), our numerical results (tables in REPORT.md §3), and per-experiment JSON evidence files.
- Judge returned **REPLICATED, coverage 0.92, agreement 0.85** — full response in `evidence/llm_judgment.json`.
- Judge is a cross-check, not a load-bearing witness (see REPORT.md Critique §5.7).

## Phase 6 — Report authoring

1. `REPORT.md` (17 KB, canonical narrative).
2. `REPORT.tex` (this wave, detailed LaTeX + GENUINE CRITIQUE section).
3. `brief.md` (1-paragraph what/why).
4. `attempt_log.md` (chronological log of runs, failures, fixes).
5. `artifact_harvest.md` (data + URL manifest).
6. `workflow.md` (this file).
7. `artifacts_summary.md` (what each file is).
8. `failure_analysis.md` (what went wrong, what we flagged as caveat vs bug).
9. `open_questions.json` (5 grounded open questions on projection-method NS).
10. `evidence/*.json,*.png` (raw numbers + plots).

## Reproduction (any modern machine)

```bash
# Prereqs: Python ≥ 3.10, numpy, scipy, matplotlib
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Chorin-projection-NS-1968/work

# Step 1 — get the paper
curl -sSL -A "Mozilla/5.0" -o chorin1968.pdf \
    "https://www.ams.org/journals/mcom/1968-22-104/S0025-5718-1968-0242392-2/S0025-5718-1968-0242392-2.pdf"

# Step 2 — run all experiments (< 8 min on a laptop)
python3 run_cavity_experiments.py
python3 pearson_test.py
python3 convergence_study.py
python3 temporal_convergence.py
python3 make_plots.py

# Step 3 — LLM judge (optional; needs Argo proxy at 127.0.0.1:44497)
JUDGE_MODEL=argo:claude-sonnet-4.6 python3 llm_judge.py
```

Expected outcomes match REPORT.md §3 tables exactly (deterministic; NumPy is not multithreaded here).

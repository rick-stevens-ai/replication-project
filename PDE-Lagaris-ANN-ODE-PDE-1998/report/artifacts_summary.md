# Artifacts summary — PDE-Lagaris-ANN-ODE-PDE-1998

Root: `~/Dropbox/REPLICATE-PROJECT/PDE-Lagaris-ANN-ODE-PDE-1998/`

## Reports (report/)
- **REPORT.md** — canonical replication report. Claims ledger (C1–C8), verbatim
  problem statements for P1/P3/P5, method, results table, C4 comparator table,
  honest gaps, verdict.
- **REPORT.tex** — LaTeX version with dedicated `Genuine critique` section
  (8 paragraphs) and honest-gaps enumeration.
- **brief.md** — task brief.
- **attempt_log.md** — chronological run log.
- **artifact_harvest.md** — file-manifest hand-off.
- **workflow.md** — 9-stage reproduction workflow (this replication).
- **artifacts_summary.md** — this file.
- **failure_analysis.md** — post-hoc analysis of what did NOT work or was
  scoped out.
- **open_questions.json** — 5 truly open questions grounded in the paper.

## Evidence (report/evidence/)
- **results.json** — per-problem structured results:
  - P1: iters=4760, loss=4.10e-7, max_err=2.72e-5, RMSE=1.51e-5, on 10 train /
    200 test.
  - P3: iters=594,  loss=3.17e-7, max_err=3.54e-6, RMSE=1.97e-6, on 10 train /
    200 test.
  - P5: iters=6250, loss=2.71e-7, max_err=9.59e-7, RMSE=3.47e-7, on 10×10 train
    / 41×41 test.
  - Also stores ANN and analytic-solution values on each evaluation grid.
- **interp_generalization.json** — C4 FD-vs-ANN comparison on Problem 1:
  - Trapezoid FD + cubic-spline: max_err 7.99e-4 at train nodes, 1.86e-3 at
    200-point dense grid.
  - ANN: max_err 2.72e-5 at both.
  - Ratio FD/ANN on dense grid: 68.6×.
- **llm_judge.json** — Argo `gpt-5` verdict:
  - `verdict = REPLICATED`
  - `coverage_score = 10/10`
  - `agreement_score = 9/10`
  - Per-claim ledger (C1–C4 all PASS).
- **fig_p1.png**, **fig_p3.png**, **fig_p5.png** — visual diagnostics
  (ANN vs exact, residual profile).

## Code (work/)
- **lagaris_ann.py** — trial-solution PyTorch implementation.
  - `MLP(in_dim, hidden=10)`: 1 hidden sigmoid layer, linear scalar output,
    no output bias, U(-1,1) init.
  - Trial forms for P1, P3, P5 verbatim from paper Sec. 4.
  - Loss = sum-of-squared residuals on paper's collocation grid.
  - Optimiser: `torch.optim.LBFGS`, strong-Wolfe line search,
    `max_iter ∈ {4000, 5000, 5000}`, `history_size = 50`, tolerances 1e-14.
  - Autograd for all derivatives of Ψ_t.
- **llm_judge.py** — Argo-proxy LLM-judge caller (stdlib only).
- **lagaris_1998.pdf** — the paper (arXiv `physics/9705023 v1`, 26 pp).
- **venv/** — Python 3.12 venv: torch 2.2.2 (CPU, float64), numpy 1.26.4.

## Extraction (extraction/)
- Text extracted via `pdftotext -layout` (OCR failed; the PDF has a clean text
  layer so the layout decode is equivalent). Equations cross-verified against
  arXiv listings.

## Determinism
- `torch.manual_seed(0)`, `np.random.seed(0)`.
- L-BFGS-CPU double is deterministic — a re-run of `lagaris_ann.py` reproduces
  identical iters, loss, max_err, RMSE to full precision.

## What is NOT here
- No independent runs at other seeds (single deterministic seed by design).
- No FEM comparator on 2D (we did the 1D FD+spline analog for C4).
- No implementation of P2, P4, P6, P7, P8 (out of task-brief scope).
- No Merlin BFGS (used torch L-BFGS, standard second-order substitute).

## Cross-references
- Paper claim ledger → REPORT.md §2.
- Verbatim problem statements → REPORT.md §3.
- Results table → REPORT.md §5 and results.json.
- Interpolation-superiority table → REPORT.md §5 (C4) and
  interp_generalization.json.
- LLM verdict → REPORT.md §8 and llm_judge.json.
- Honest gaps → REPORT.md §6 and REPORT.tex Genuine Critique.

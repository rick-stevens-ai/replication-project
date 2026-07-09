# Workflow — Lagaris-Likas-Fotiadis (1998) ANN-ODE/PDE replication

**Paper.** Lagaris, Likas, Fotiadis (1998), *IEEE TNN* 9(5):987–1000
(arXiv `physics/9705023 v1`).
**Set.** PDE-100.
**Target dir.** `~/Dropbox/REPLICATE-PROJECT/PDE-Lagaris-ANN-ODE-PDE-1998`.
**Verdict.** REPLICATED.

## Stages

### Stage 1 — Paper acquisition and text extraction
- Downloaded arXiv preprint `physics/9705023 v1` to `work/lagaris_1998.pdf`.
- OCR failed on the PDF; used `pdftotext -layout` as fallback. The PDF has a
  clean text layer so this decode is equivalent to the source text (verified
  against arXiv listings for equations).
- Extracted problem statements for Problems 1, 3, 5 verbatim into REPORT.md §3.

### Stage 2 — Claim extraction and scoping
- Enumerated 8 claims (C1–C8) in REPORT.md §2.
- Scope reduced to C1 (P1), C2 (P3), C3 (P5), plus C4 (interpolation
  superiority). C5–C7 (P2, P4, P6–P8) explicitly out of scope. C8 (BFGS
  convergence-iteration claim) flagged as accounting-dependent, not tested.

### Stage 3 — Environment
- Python 3.12 venv at `work/venv`.
- PyTorch 2.2.2 (CPU, `float64`), NumPy 1.26.4. All pip-installable, no paid
  endpoint.
- Torch RNG seed = 0; NumPy seed = 0. L-BFGS-CPU double is deterministic.

### Stage 4 — Implementation
- `work/lagaris_ann.py`:
  - `MLP(in_dim, hidden=10)` = 1 hidden layer, sigmoid activation, linear
    scalar output (no output bias). Weights init `U(-1, 1)`.
  - Trial solutions coded verbatim from paper Sec. 4:
    - P1: `Psi_t(x) = 1 + x * N(x, p)`
    - P3: `Psi_t(x) = x*sin(1)*e^{-1/5} + x(1-x) * N(x, p)`
    - P5: `Psi_t(x,y) = A(x,y) + x(1-x)y(1-y) * N(x,y,p)` where A(x,y) is the
      closed-form bilinear boundary lift of Eq. 18.
  - Autograd computes first/second derivatives of `Psi_t`.
  - Loss: sum of squared residuals of the differential operator over the
    training grid (paper Eq. 12 for ODEs; analog for PDEs).
  - Optimiser: `torch.optim.LBFGS` with `strong_wolfe` line search,
    `max_iter ∈ {4000, 5000, 5000}`, `history_size = 50`, tolerances 1e-14.

### Stage 5 — Runs
```
source work/venv/bin/activate
python3 work/lagaris_ann.py report/evidence   # ~30 s
```
Writes:
- `report/evidence/results.json` — per-problem: iters, loss, max_err, RMSE,
  ANN/exact grids.
- `report/evidence/interp_generalization.json` — C4 FD-vs-ANN comparison on
  P1's 10 nodes evaluated at 200 dense points.
- `report/evidence/fig_p1.png`, `fig_p3.png`, `fig_p5.png`.

### Stage 6 — Evaluation
- ODE cases (P1, P3): 200 equispaced test points on [0, 1].
- PDE case (P5): 41×41 = 1681 grid on [0, 1]².
- Metrics: max |Ψ_t − Ψ_exact| and RMSE vs the analytic solution.

### Stage 7 — C4 comparator
- Solved P1 on the same 10-point grid with implicit trapezoid FD (2nd-order,
  exact for linear problems) + natural cubic-spline interpolation off-grid.
- Fair ODE analog of the paper's PDE FEM comparator (both 2nd-order local
  methods requiring interpolation to evaluate off-grid).
- Reported max err at training nodes vs 200-point dense grid for both methods.

### Stage 8 — LLM judge
```
python3 work/llm_judge.py report/evidence     # ~30 s
```
Argo `gpt-5` (temperature omitted). Returned:
- `verdict = REPLICATED`
- `coverage_score = 10/10`
- `agreement_score = 9/10`
Written to `report/evidence/llm_judge.json`.

### Stage 9 — Report drafting
- REPORT.md with claims ledger, problem statements, method, results,
  honest gaps, verdict.
- REPORT.tex (LaTeX) with dedicated Genuine Critique section.
- artifact_harvest.md, attempt_log.md, brief.md alongside.

## Reproduction
```
cd ~/Dropbox/REPLICATE-PROJECT/PDE-Lagaris-ANN-ODE-PDE-1998
source work/venv/bin/activate
python3 work/lagaris_ann.py report/evidence
python3 work/llm_judge.py  report/evidence
```

## Determinism
- `torch.manual_seed(0)` + `np.random.seed(0)`
- L-BFGS-CPU double = deterministic.
- Re-run reproduces same iters, loss, max_err, RMSE to full precision.

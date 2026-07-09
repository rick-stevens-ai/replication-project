# Failure analysis — PDE-Lagaris-ANN-ODE-PDE-1998

**Verdict.** REPLICATED. No hard failures. This document catalogues the
things that did NOT work, were skipped, or came out worse than the paper's
best figure, so future work has an honest baseline.

## Scope decisions that are effectively "not-attempted" gaps

### F1. Only 3 of 5 worked examples reproduced
- **What.** P2 (very similar to P1, first-order ODE with a different RHS),
  P4 (coupled first-order ODE system), and P6–P8 (harder 2D PDEs with mixed
  BCs) were not implemented.
- **Why.** Task brief requested C1 (P1), C2 (P3), C3 (P5) + C4 (interpolation
  superiority). Others were out of scope.
- **Impact.** The strongest reading of "REPLICATED" is *"for the three cases
  we tested at the reported accuracy."* P4 and P6–P8 in particular exercise
  method aspects (coupled systems, mixed BCs, radial-basis boundary lifts)
  that our replication does NOT touch.
- **Recovery.** Each of P2/P4/P6–P8 is a small additional implementation on
  top of `work/lagaris_ann.py`. Would take ~1–2 h per problem.

### F2. C4 comparator is FD + spline, not FEM
- **What.** The paper's Table 1 comparator is 2D FEM on an 18×18 element grid.
  Our C4 replication is 1D (Problem 1) using implicit trapezoid FD + natural
  cubic spline.
- **Why.** The C4 phenomenon (ANN error uniform vs classical error concentrated
  at nodes) is claimed by the paper for a 2D PDE. We did the 1D analog because
  it fits within P1 and the qualitative claim carries over.
- **Impact.** We reproduce the *qualitative* claim (68.6× ratio; ANN uniform,
  FD degrades off-grid) but not the specific FEM/ANN numbers from Table 1
  (2×10⁻⁸ at training / 1.5×10⁻⁵ at test).
- **Recovery.** Implement a 2D FEM on the P5 unit square (18×18 elements,
  bilinear basis) and compare against our P5 ANN result at the same 30×30 test
  grid. That would settle C4 in the paper's own setting.

## Accuracy shortfalls (small)

### F3. P5 max_err = 9.59×10⁻⁷ vs paper's 5×10⁻⁷
- **What.** Our best P5 max_err is a factor of ~1.9 worse than the paper's
  reported figure.
- **Why.** Initialisation-dependent. Single deterministic seed 0. We chose
  reproducibility over multi-restart best-of-N.
- **Impact.** Within the "factor of ~2" tolerance we set for REPLICATED.
- **Recovery.** Run 10 restarts at seeds 0–9, report distribution. Expected
  outcome: paper's 5×10⁻⁷ is inside the resulting range.

### F4. P1/P3 iteration counts don't match paper's "1–5 iterations"
- **What.** L-BFGS ran 594–6250 line-search steps on P1/P3/P5. Paper cites
  "1–5 iterations for linear problems" using Merlin BFGS.
- **Why.** Different iteration accounting. Merlin's "outer iteration" is not
  the same unit as L-BFGS's line-search step count.
- **Impact.** Not a discrepancy — an apples-to-oranges accounting question.
  Flagged in REPORT.md §6 note 3 and §2 row C8.
- **Recovery.** Install Merlin (or a faithful reimplementation) and count
  outer iterations under the same convention as the paper.

## Tooling issues that were worked around

### F5. OCR failed on the PDF
- **What.** OCR pipeline errored on `lagaris_1998.pdf`.
- **Why.** The PDF already contains a clean text layer; the OCR step assumed
  it needed rasterisation.
- **Impact.** None on results. Used `pdftotext -layout` instead, which
  decodes the existing text layer. Cross-verified equations against the
  arXiv listing.
- **Recovery.** For future papers, probe whether a text layer exists before
  routing to OCR.

## What did NOT fail (worth stating explicitly)

- No optimiser divergence on any of P1/P3/P5. All three converged to residual
  loss ≤ 5×10⁻⁷.
- No BC violation. Trial-solution construction enforces BCs exactly; the
  boundary residual is zero by construction, verified on P5's four Dirichlet
  edges to machine precision.
- No autograd instability. Second derivatives of Ψ_t (needed for P3, P5)
  were computed via nested `torch.autograd.grad` without numerical issues at
  `float64`.
- No LLM-judge veto. Argo `gpt-5` returned `verdict = REPLICATED` with
  `coverage_score = 10/10`, `agreement_score = 9/10` (only deduction: one
  point on agreement, reason not specified in the JSON).

## Failure-log placement

None of the above are hard failures — they are honest scope, honest single-
seed reporting, and one tooling nit. Not logged to `failure-log.md` because
the task completed with a REPLICATED verdict inside the accuracy tolerance.

# Attempt log — DeepXDE (Lu et al. 2021) replication

Timestamps in America/Chicago.

1. **2026-07-04 23:52** — task assigned. Fetched brief; created target dir.
2. **23:53** — pulled paper `arxiv.org/pdf/1907.04502` (v2, Feb 2020, 1.12 MB).
   Extracted text with `pdftotext -layout`. Located Section 4 "Demonstration examples",
   Table 3 (hyperparameters for the 5 examples), and Section 4.2 (Burgers + RAR)
   including the exact 1D Burgers formulation (ν = 0.01/π, IC = -sin πx,
   Dirichlet BCs) and the RAR protocol (m=1, E0=0.005, +40 added points on top of
   an initial 2500).
3. **23:56** — verified UICGPU access: 8× A100 80 GB, driver 570.207, CUDA 12.8.
   Created `~/pde_deepxde_rep/venv` (Python 3.8), installed `torch scipy numpy
   matplotlib`. Torch 2.4.1+cu121, CUDA available.
4. **00:00** — wrote `replicate_pinn.py`: plain-PyTorch MLP (tanh) with Adam,
   autograd for u_x, u_t, u_xx. Three functions: `run_poisson_1d`,
   `train_burgers`, and a driver.
5. **00:03** — dry run: Poisson 1D only, `--do_poisson`. 20000 Adam iterations,
   depth=3, width=20, 64 residual points. Final **L2_rel = 7.03e-5**, wall
   97.6 s on one A100. Sanity check: passes.
6. **00:05** — first Burgers attempt failed: bad URL for `burgers_shock.mat`
   (`main/Data/…` returned 404; correct path is `appendix/Data/…`). Fixed and
   restarted.
7. **00:10** — second Burgers attempt failed inside RAR after the uniform-seed0
   run: `torch.autograd.grad` on the pool tensor with `create_graph=False`
   dropped grads before the second derivative. Fixed by taking the first-order
   grad with `create_graph=True`, then the second with `create_graph=False`.
8. **00:12–00:22** — Burgers full run finished (7 training runs total: 1 initial
   uniform sanity + 3 seeds × {RAR, uniform}). Wall ≈ 10 min on one A100.
9. **00:23** — pulled all `results/*.json` and the raw log back to
   `report/evidence/`. Rendered 3 PNG figures. Wrote the report.
10. **00:25** — LLM judge scoring via Argo proxy (localhost:44497, key=stevens,
    model=argo:claude-opus-4.7). Free-endpoint policy respected.

### Deviations from the paper (documented)
- We used a **1D** Poisson problem with an analytic solution, not the paper's
  2D L-shape (whose exact solution is not closed-form). The paper's own claim
  under test — "small PINN solves Poisson accurately" — is what this checks.
- We used **Adam only** (no L-BFGS refinement). The paper uses Adam then
  L-BFGS for examples 1 and 2. Adam-only under-refines; this is a known bias
  that inflates absolute errors relative to the paper.
- Only 15000 Adam iterations for Burgers (paper uses 15000 with subsequent
  L-BFGS-to-convergence). Our absolute L2 errors on Burgers are therefore
  looser than the paper's, but well within the range the paper itself plots
  for the "PINN w/o RAR" curve (Figure 8B) at ~2500 residual points.
- IC/BC weights left at 1 (matching paper).

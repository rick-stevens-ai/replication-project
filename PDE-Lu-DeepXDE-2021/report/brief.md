# Brief

We independently reimplemented a physics-informed neural network (PINN) in
plain PyTorch (no `deepxde` library) and reproduced three central claims of
Lu et al., *DeepXDE: A deep learning library for solving differential equations*
(SIAM Review 2021, arXiv 1907.04502v2): (C1) a small PINN converges to the
exact solution of a 1D Poisson problem to L2-relative error ≈ 7e-5;
(C2) a small PINN reproduces the sharp-gradient solution of the 1D viscous
Burgers equation (ν = 0.01/π, u(x,0) = -sin πx) versus the standard Raissi
reference; and (C3) residual-based adaptive refinement (RAR) reduces the mean
L2 error over 3 seeds at a matched 2540-point budget (RAR mean 7.2e-2 vs
uniform 8.9e-2; RAR wins 2 of 3 seeds). Verdict: **PARTIAL** — C1 fully
replicated, C2 qualitatively replicated (magnitude of error is within the
same range the paper reports for uniform sampling), C3 directionally
confirmed but with high seed variance under our shortened Adam-only
training budget (no L-BFGS refinement).

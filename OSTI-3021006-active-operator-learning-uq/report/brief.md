# Brief — OSTI 3021006

**Paper**: Winovich, Daneker, Lu, Lin, Wang, "Active operator learning with predictive uncertainty quantification for solutions of PDEs" (OSTI 3021006, 2025).

**What we tested**: Core claim C1 — that using an FNO surrogate's *predictive uncertainty* (from an NLL-trained variance head) to select next training samples in an active-learning loop reaches a target L2-relative test error with fewer training samples than random sampling, on a 2D advection–diffusion PDE.

**What we did**: Independently implemented an FNO-2d + NLL-variance head in PyTorch, generated a real numerical PDE dataset (48×32 grid, 21 time snapshots, upwind advection + centered diffusion), and ran the full active-learning loop (start n=60, add 30/round × 6 rounds, 3 trials) with UQ-variance acquisition vs uniform-random acquisition. Ran on UICGPU (A100 80GB). 3-trial medians logged at every training size 60→240.

**Result**: UQ-guided acquisition beats random at **every** training size in the sweep; final L2rel = 0.0626 (UQ) vs 0.0709 (random), a **+11.5% relative reduction** — mechanism and direction match the paper's ~7.5% figure; magnitude differs because our problem is smaller (grid 48×32 vs paper 96×64, pool 500 vs 800+, kappa 0.01 same but source stats slightly different). **Verdict: PARTIAL** (mechanism + direction reproduced; exact paper benchmark scale not matched).

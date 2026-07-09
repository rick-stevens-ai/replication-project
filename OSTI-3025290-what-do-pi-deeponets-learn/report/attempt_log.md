# Attempt Log

## 2026-07-05 00:19 CDT — Setup
- Created target dir + subdirs.
- CherryRd blocked from osti.gov; downloaded PDF via uicgpu proxy
  (`ssh uicgpu; source ~/env.sh; curl -sLo /tmp/osti_3025290.pdf https://www.osti.gov/servlets/purl/3025290`),
  scp'd to `work/paper.pdf` (10,442,128 bytes).
- Ran `pdftotext -layout` → 1352-line text; extracted claims + tables verbatim.

## 2026-07-05 00:22 CDT — Paper claims table
Paper: Williams, Howard, Qadeer, Meuris, Stinis (PNNL/Sandia/MIT), 2025.
Key numerical claims (extracted verbatim from PDF):
- **C1** Advection-diffusion (α=4, ν=0.01), PI-DeepONet with fixed weights, w=128:
  avg rel ℓ² = 0.48% ± 0.41% over 100 test samples (Table 1).
- **C1b** Same problem, PI with NTK weights: 0.82% ± 0.54% (Table 1).
- **C2** SVD-of-trunk basis for advection-diffusion: 47 PI (NTK) basis functions
  reach same ~10⁻⁷ error as 62 data-driven basis functions in spectral method
  (Table 2). PI singular values decay faster.
- **C3** Expansion coefficients of e^sin(x) decay to machine precision when the
  DeepONet has trained well.
- **C4** Burgers ν=10⁻⁴ transfer init from ν=10⁻³: 13.67%±7.28% → 7.03%±4.94% (Table 5).
- **C5** KdV transfer from Burgers ν=10⁻⁴ (CK weights): 3.92% → 3.29% (Table 6).

## 2026-07-05 00:24 CDT — Reproduction plan
Feasible target given single-turn budget: **C1 + C2 + C3** on advection-diffusion.
- Implement vanilla MLP PI-DeepONet in PyTorch (branch/trunk width=128,
  branch_depth=3, trunk_depth=4 from Table A.9, tanh, Adam lr=1e-3 exp decay).
- Compute Fourier reference (exact in Fourier space).
- Train N=500 ICs sampled from paper's GRF g(sin²(x/2)), l=0.5 (Table A.7,
  Appendix A).
- Evaluate on 100 fresh test ICs.
- Perform SVD-of-frozen-trunk analysis; compute expansion coefficients of
  f(x)=exp(sin(x)).
- Full paper config uses 200k iterations. To fit in reasonable wall clock,
  ran 50k iterations (25% of paper) on 1×A100.

## 2026-07-05 00:24 CDT — Smoke test on uicgpu
- 500-iter smoke with n_train=50, n_test=20: loss decreasing 3.44e-1 → 7.24e-2;
  rel L2 121% → 63%; confirms training is functional.
- Fixed GRF sampler: kernel jitter needed to be raised because the periodic
  distance kernel becomes ill-conditioned on m=128.

## 2026-07-05 00:24 CDT — Main training launched
uicgpu PID 4038386, 50k iters, N_train=500, N_test=100, batch=1000, P=128.
Expected wall clock ≈ 30 min (26.9 iters/s in smoke).
Output buffered; will poll for completion.

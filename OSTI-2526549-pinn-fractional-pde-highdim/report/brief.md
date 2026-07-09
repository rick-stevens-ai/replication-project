# Brief — OSTI 2526549

**Paper:** Hu, Kawaguchi, Zhang & Karniadakis, "Tackling the curse of dimensionality in fractional and tempered fractional PDEs with physics-informed neural networks," *Comput. Methods Appl. Mech. Engrg.* 432 (2024) 117448. DOI: 10.1016/j.cma.2024.117448.

**What/why:** Extends Monte Carlo fractional PINN (MC-fPINN) to *tempered* fractional PDEs (MC-tfPINN) and, for both, replaces the 1D Monte Carlo integral in `r` with Gauss-Jacobi (fractional) or generalized Gauss–Laguerre (tempered fractional) quadrature. The claim is that (a) tempered fractional PDEs can be attacked at all with PINNs, and (b) the quadrature-improved variants are strictly faster and slightly more accurate than the original MC-fPINN of Guo et al. [13] across dimensions 10¹ … 10⁵ on the fractional/tempered fractional Poisson & diffusion benchmarks. Public reference code released at https://github.com/zheyuanhu01/Tempered_Fractional_PINN.

**Our target:** Independently rerun the paper's flagship Table 2 benchmark — high-dimensional fractional Poisson equation `(-Δ)^{α/2} u = f` in the unit ball with the anisotropic exact solution of Eq. (29) — at d=100 (1M epochs, matching paper) and d=1000 (scaled-down 200K epochs due to a night-batch time budget), for both vanilla MC-fPINN and quadrature-improved MC-fPINN, on our own uicgpu 8×A100 hardware.

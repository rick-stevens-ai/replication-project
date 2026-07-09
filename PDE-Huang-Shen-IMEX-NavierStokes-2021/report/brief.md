# Brief

**Paper:** F. Huang & J. Shen, *Stability and Error Analysis of a Class of High-Order IMEX Schemes for Navier–Stokes Equations with Periodic Boundary Conditions*, SIAM J. Numer. Anal. 59(6), 2021 (arXiv:2103.11025, DOI 10.1137/21M1404144).

**What/why:** The paper constructs arbitrary-order (up to 5th) unconditionally-energy-stable IMEX time-stepping schemes for the 2D/3D incompressible Navier–Stokes equations with periodic BCs, using the Scalar Auxiliary Variable (SAV) approach with BDFk/Adams–Bashforth-k and a Fourier–Galerkin spatial discretization, and proves matching high-order error estimates. We independently re-implemented the SAV/BDFk (k=1..4) Fourier-spectral solver from scratch and reproduced the paper's headline numerical result (Example 1, Fig. 1): the H¹ errors of both velocity and pressure exhibit the expected order-k temporal convergence, plus we verified the central theoretical claim of unconditional energy stability at large time step.

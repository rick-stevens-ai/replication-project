# Brief

**Paper.** Hietel, D., Steiner, K., Struckmeier, J. (2000). *A Finite-Volume
Particle Method for Compressible Flows.* Math. Models Methods Appl. Sci.
10(9):1363-1382. DOI 10.1142/S0218202500000604.

**What it does.** Introduces the Finite-Volume Particle Method (FVPM) — a
meshfree scheme where each particle carries a compact-support smooth window
function, whose Shepard-normalized ratio forms a partition of unity. Volumes
and antisymmetric pairwise geometric coefficients β_ij are obtained from
overlap integrals of the ψ's; combined with a Riemann-solver numerical flux
they yield a globally conservative scheme for hyperbolic conservation laws
that reduces to a standard finite-volume Godunov-type method on a uniform
particle distribution.

**What we did.** Independent from-scratch implementation of 1D FVPM (linear
tent window, HLLC flux, SSP-RK2, Dirichlet ghosts) and ran the canonical
Sod shock tube (t=0.2, γ=1.4) at N=50/100/200/400/800, comparing against an
exact Riemann solver. LLM-judged the numerical claims via a signed multi-judge
protocol on FREE endpoints (Argo Claude-Opus-4.7 was intended primary but the
Argo proxy was returning HTTP-502; verdicts came from Argo GPT-5.2 + CELS
llama70 + CELS nemotron-3-ultra).

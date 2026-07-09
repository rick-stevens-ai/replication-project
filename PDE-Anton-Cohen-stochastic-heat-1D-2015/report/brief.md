# Brief

Independent from-scratch replication of Anton, Cohen & Quer-Sardanyons, *"A fully discrete
approximation of the one-dimensional stochastic heat equation"* (arXiv:1711.08340; IMA J.
Numer. Anal.). The paper introduces an **explicit stochastic exponential integrator (SEXP)**
for the 1D stochastic heat equation with multiplicative space-time white noise, discretized
by standard finite differences in space, and proves L^q(Ω) + almost-sure convergence with an
improved temporal rate and **no CFL step-size restriction**. We reimplemented the scheme in
numpy (DST-I diagonalization of the discrete Laplacian, verified exact to 3e-16 vs dense
`expm`), validated it first on the deterministic analytic case (exponential integrator exact
in time; FD Laplacian exactly 2nd order in space), then reproduced the two headline numerical
claims on the paper's exact test problem: (C1) CFL-free stability for Δt∈[2⁻¹,2⁻¹⁶] at M=512,
and (C2) empirical temporal **strong convergence order ≈1/2** (measured 0.558 over 500 samples).
Pathwise (almost-sure) convergence was also confirmed. We flag one internal-consistency issue:
the paper's noise-increment scaling as literally written amplifies noise by a factor M and
blows up; the physically-correct cell-increment scaling recovers the paper's own stability and
figures. Three independent free-Argo LLM judges (gpt-5.2, gemini-2.5-pro, gpt-4.1) all rated
the result **REPLICATED**.

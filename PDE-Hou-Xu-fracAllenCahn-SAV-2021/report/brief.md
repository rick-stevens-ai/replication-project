# Brief

Independent replication of Hou & Xu (2021), *"Highly efficient and energy dissipative
schemes for the time fractional Allen-Cahn equation"* (arXiv:2104.12109v1; SIAM J. Sci.
Comput. 43(6):A3305–A3327). The paper constructs unconditionally-stable SAV-type
time-stepping schemes (first-order **L1**, (2−α)-order **L1-CN**, second-order **L1+-CN**)
for the time-fractional Allen-Cahn equation `₀Dₜᵅφ = −gradH E(φ)`, each proven to satisfy a
discrete non-local energy-dissipation law. Working only from the arXiv source and PDF, I
re-derived the schemes (θ=0, C₀=0 as in the paper), implemented the L1 and L1-CN schemes
from scratch with a Fourier-spectral space discretization, and (i) validated first-order and
(2−α)-order temporal convergence against the paper's manufactured solution
(Example 5.1, φ=0.2t⁵sin x cos y), and (ii) verified unconditional discrete modified-energy
dissipation on the source-free coarsening problem. Observed convergence slopes match the
paper's Figure 1 (α=0.1→1.99 vs paper 1.9; α=0.9→trending 1.1 vs paper 1.1) and the modified
energy is monotone-decreasing every step. Verdict: **PARTIAL** (three core claims reproduced;
the L1+-CN 2nd-order scheme and graded-mesh/shrinking-circle robustness experiments not run).

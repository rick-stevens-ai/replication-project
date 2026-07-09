# Brief — Liu et al. 2020, Variational Quantum Algorithm for the Poisson Equation

Independent replication of Liu, Wu, Wan, Pan, Qin, Gao, Wen (arXiv:2012.07014;
published as Phys. Rev. A **104**, 022418 (2021)). The paper proposes a
Variational Quantum Algorithm (VQA) for solving the finite-difference discretized
1-D and *d*-D Poisson equation on NISQ hardware. Their central contribution is
an explicit tensor-product decomposition of the tridiagonal coefficient matrix
`A_m` (dimension 2^m) into **2m+1** items over {I, σ+, σ-} and of `A_m²` into
**4m+1** items — dramatically fewer than a general Pauli decomposition — plus a
QAOA-style variational ansatz that finds the ground state of
H = A(I − |b⟩⟨b|)A. **Why replicate:** highly-cited (108), open-access preprint,
fully classical simulation (they use ProjectQ), and every claim is quantitative
and self-contained (no proprietary data). We verified both decomposition
counts exactly for m=1..6 (zero reconstruction error) and independently
reproduced the VQA fidelity-vs-layer curve (Fig. 4) using numpy + BFGS.

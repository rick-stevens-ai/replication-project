# Brief

Independent from-scratch replication of Adil & Hussein (2020), *Numerical Solution for
Two-Sided Stefan Problem* (Iraqi J. Science 61(2):444-452, DOI 10.24996/ijs.2020.61.2.24).
The paper solves a 1D two-phase (moving free-boundary) Stefan problem for the full
variable-coefficient parabolic heat equation by a Landau change-of-variables to a fixed
domain followed by a Crank-Nicolson finite-difference scheme, claiming unconditional
stability and second-order space-time accuracy on two manufactured test cases. I
reimplemented the transformed PDE + CN tridiagonal solver in Python (numpy/scipy) and
reproduced both of the paper's error tables to 4 decimal places on all meshes, recovered
the claimed O(h^2) convergence for the nonlinear case, and identified/corrected two
internal paper typos (a Table-1 digit transposition and an Example-2 x^2->x^3 misprint)
that are required for the paper's own tables to be self-consistent. **Verdict: REPLICATED.**

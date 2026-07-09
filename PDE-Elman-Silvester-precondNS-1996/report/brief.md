# Brief

Elman & Silvester (1996), *Fast Nonsymmetric Iterations and Preconditioning for Navier-Stokes
Equations*, SIAM J. Sci. Comput. 17(1):33–46, DOI 10.1137/0917004. The paper proposes two
block preconditioners — block-diagonal `diag(F, ν⁻¹Q)` (2.5) and block-triangular
`[[F,Bᵀ],[0,ν⁻¹Q]]` (2.12) — for the linearized Oseen system that arises from Picard iteration
on the steady incompressible Navier–Stokes equations. Central theoretical claim: for a
div-stable mixed FE discretization, the eigenvalues of the preconditioned Oseen operator are
contained in a bounded region independent of the mesh size h. Central experimental claim
(Tables 2–5): GMRES(10) and QMR iteration counts to reduce the ℓ₂ residual by 10⁻⁶ are
essentially independent of h at fixed viscosity ν, and grow (roughly linearly) as ν→0. The
triangular preconditioner (2.12) roughly halves the iteration count vs the diagonal one (2.5).
Test problem: 2-D leaky lid-driven cavity in Ω=[-1,1]², wind field
w=(2y(1-x²), -2x(1-y²)), ν∈{1, 1/10, 1/100}, meshes 16², 32², 64².

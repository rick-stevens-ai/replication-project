# Brief

Independent replication of **Persson & Peraire (2008),** "Newton-GMRES
Preconditioning for Discontinuous Galerkin Discretizations of the Navier-Stokes
Equations", SIAM J. Sci. Comput. 30(6): 2709–2733 (DOI: 10.1137/070692108).
The paper compares three preconditioners for the linear systems arising in
Newton-GMRES applied to DG discretizations of NS: **block-Jacobi**, **block-ILU(0)**,
and a Persson–Peraire **element-line** preconditioner. Their central experimental
finding is that the line preconditioner gives near-mesh-independent GMRES
iteration counts, while block-Jacobi rapidly loses effectiveness at higher
Peclet / anisotropy / mesh refinement.

We built a standalone Python DG(p=1) SIP+upwind solver for the scalar 2D
convection–diffusion model problem — the same operator class whose block
structure drives the preconditioner behavior studied in the paper — and
implemented all three preconditioners plus an unpreconditioned baseline.
Sweeps over mesh size, diffusion coefficient, and convection direction were
run on `uicgpu` (A100 host, single-thread CPU numerics). A separate LLM
judge (Argo `gpt-4o`, fallback from the requested `claude-opus-4.7` which was
502-ing on the Argo proxy at run time) evaluated the results against the
paper's qualitative claims and returned a **PARTIAL** verdict.

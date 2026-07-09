# Brief

Independent from-scratch replication of the **Cartesian-grid embedded-boundary (EB)
finite-volume method for Poisson's equation and the heat equation on irregular
domains** (McCorquodale, Colella & Johansen, *J. Comput. Phys.* 173(2), 2001; DOI
10.1006/JCPH.2001.6900 — rank 75 of PDE_TOPUP25). The paywalled JCP article was
replaced by the open-access companion technical report (Schwartz, Barad, Colella &
Ligocki, LBNL / OSTI 878684), which describes the identical discretization. We
re-implemented the cut-cell FV Laplacian, the Dirichlet boundary-gradient stencils,
and the L0-stable (Twizell–Gumel–Arigu) time integrator in Python/numpy/scipy, and
verified the paper's central claims — second-order-accurate elliptic solutions and
second-order-in-space-and-time parabolic solutions on an irregular (circular) domain —
against manufactured / exact analytic solutions via grid-refinement convergence
studies. Free endpoints only (Argo proxy) for the LLM-judge verdict.

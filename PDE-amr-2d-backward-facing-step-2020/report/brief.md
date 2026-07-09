# Brief

Li & Li (2020, IJCM, DOI 10.1142/S0219876220410121) verify the accuracy of a 2D velocity-driven
adaptive mesh refinement (VDAMR) method by applying it to the classical backward-facing
step (BFS) flow at low Reynolds numbers.  The method computes the discrete divergence
residual of the Navier-Stokes velocity field on a vertex-centred finite-volume mesh (median-dual
control volumes), flags cells whose |div| exceeds a threshold, and bisects them.  Accuracy is
demonstrated by convergence of the recovered vortex-centre location (via linear interpolation)
toward benchmark values as the mesh is refined.

This is an **independent-replication** for the X-100 project, distinct from the sibling directory
`PDE-Li-Li-AMR-backwardstep-2020/` which used a Chorin-projection MAC-grid solver.  Here we:

1. Attempt to obtain the paper (paywalled behind Cloudflare on WSPC; no OA copy on
   Unpaywall/arXiv/OSTI); recover the exact abstract via Semantic Scholar.
2. Implement an independent 2D BFS solver in the **stream-function/vorticity** formulation
   with hybrid central/upwind convection, sparse LU factorisation of the psi-Poisson system,
   and explicit RK2 in time, on uicgpu (255 cores, 2 TB RAM).
3. Independently verify the paper's central *methodological* claim (convergence of the
   VDAMR divergence-flag indicator and of the recovered vortex-centre location under mesh
   refinement) on a manufactured analytical stream function whose vortex centre is known
   in closed form.
4. Compare our BFS-NS runs at Re=50, 100, 200 against Armaly (1983) experimental and
   Erturk (2008) numerical benchmark data, in a common Reynolds convention.
5. Rate the replication as **SPOT-CHECK** (paper paywalled; method plausibility and
   mathematical claim independently verified; direct value-for-value match to paper's own
   tables impossible without full-text access).

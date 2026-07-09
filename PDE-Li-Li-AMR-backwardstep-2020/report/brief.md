# Brief

Li & Li (2020, IJCM, DOI 10.1142/S0219876220410121) present accuracy verification of a
2D Adaptive Mesh Refinement method (VDAMR — velocity-driven AMR, refining cells whose
finite-volume divergence residual exceeds a threshold) applied to the classic
backward-facing step (BFS) benchmark at low Reynolds numbers. The base solver is the
Navier2D vertex-centred finite-volume Navier–Stokes code (Engwirda); the refinement
criterion recursively bisects control volumes with high mass-conservation residual and
tracks recovery of the primary reattachment length x_r/S as the mesh is refined.

We independently implement (i) a 2D BFS Navier–Stokes solver (stream-function/vorticity,
finite-difference SIMPLE-like relaxation) at expansion ratio ER=2 and Re_h = 100, 200, 400,
(ii) compute primary reattachment length x_r/S on progressively refined uniform meshes,
(iii) implement a divergence-magnitude cell-flagging AMR criterion analogous to VDAMR
and demonstrate its convergence, (iv) compare against the Armaly (1983) experimental
data and Erturk (2008) benchmark solutions cited by the paper's benchmark class.

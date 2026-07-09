# Brief

Independent replication of Deiterding, Domingues, Gomes, Schneider (SIAM J.
Sci. Comput., 2016, DOI 10.1137/15M1026043, arXiv 1603.05211), which compares
adaptive multiresolution (MR, Carmen code) and block-structured adaptive mesh
refinement (AMR, AMROC code) on 2D and 3D compressible-Euler test cases and
concludes that MR yields slightly better mesh compression than AMR while AMROC
is faster in absolute time due to implementation differences. We wrote a
from-scratch 2nd-order finite-volume Euler solver (MUSCL + HLLC + SSPRK2)
first in pure NumPy (SPOT-CHECK pass) then numba-JIT'd (promote pass), ran
the paper's exact 2D Riemann Lax-Liu #6 test on uniform grids
N ∈ {128,256,512} vs an N=1024 reference (paper's L=10 base grid), and
confirmed the paper's uniform-mesh convergence rate ~O(1) in L1(ρ) with
absolute errors within 30% of paper values at every N. We also implemented
proper Harten cell-average graded-tree MR (3rd-order polynomial prediction,
4 levels) and Berger-Colella AMR with 2-cell buffer inflation, then
time-averaged their flag fractions over 5 density snapshots — the MR<AMR
ordering and MR/AMR ratio 0.80 (paper: 0.89) both reproduce. A Pareto sweep
of same-accuracy compression directly quantifies MR's better accuracy per
active cell (5-10× dominance over AMR). Verdict: **PARTIAL** — base scheme
+ mesh compression ordering + accuracy-per-cell all replicated; in-loop CPU-
time trends and cross-code absolute-runtime comparison remain out of scope.

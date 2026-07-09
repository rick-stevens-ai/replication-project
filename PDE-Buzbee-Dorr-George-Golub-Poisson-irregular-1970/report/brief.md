# Brief

Buzbee, Dorr, George & Golub (SIAM J. Numer. Anal. 8(4), 1971; LA-4553-MS)
show that fast direct rectangle Poisson solvers can be extended to
**irregular** two-dimensional regions by (i) *imbedding* the region in a
super-rectangle and modifying the `p` rows of the discrete Laplacian that
correspond to the interior boundary, then (ii) using the
**Sherman-Morrison-Woodbury / capacitance-matrix** identity to correct the
imbedding solve. Cost: one preprocessing stage of `p+1` rectangle solves
(fills a `p×p` dense `C`), then two rectangle solves per new right-hand
side. This replication (a) implements the imbedding-with-capacitance
construction on the rectangle-with-inner-square-hole of paper Table 1,
(b) implements the L-shape *splitting* construction of Section 5, and
(c) runs a method-of-manufactured-solutions convergence study. All three
verify the paper's central claim quantitatively.

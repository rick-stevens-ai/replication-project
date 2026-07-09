# Brief

Independent replication of Bernardi, Maarouf & Yakoubi (2016), *"Spectral discretization
of Darcy's equations coupled with the heat equation"* (IMA J. Numer. Anal.,
DOI:10.1093/IMANUM/DRV047). The paper couples Darcy's law with the heat equation on the
square (−1,1)², discretizes with a Legendre–Gauss–Lobatto (GLL) P_N×P_N×P_N spectral
Galerkin method, proves an optimal a priori error estimate, and validates it (Sec. 5.2,
Fig. 1) with a manufactured analytic solution showing **spectral (exponential) convergence**
of the L²/H¹ errors down to a machine-precision floor. We fetched the OA PDF (HAL), extracted
the model, discretization and accuracy test, and re-implemented the whole coupled GLL spectral
solver from scratch in numpy (custom GLL nodes/weights/differentiation, Darcy pressure solve,
GLL-Galerkin heat solve, decoupled fixed-point coupling). We reproduced the exponential error
decay, the ~N=16–20 machine-precision floor, the indistinguishable exact/discrete solution
(max|T−T_N|=1.5e-14 at N=17), and the convergent fixed-point iteration. Two independent free
LLM judges scored the result **REPLICATED**. One finding: the source terms printed in eq. (5.6)
are internally inconsistent with the stated exact solution (transcription typos); we used the
analytically consistent manufactured sources.

# Brief

**Paper:** M. J. Gander & A. M. Stuart, "Space-Time Continuous Analysis of Waveform
Relaxation for the Heat Equation," SIAM J. Sci. Comput. 19(6):2014–2031, 1998.
DOI 10.1137/S1064827596305337. (rank 77, PDE-100 top-up list; OA author copies at
stuart.caltech.edu and unige.ch/~gander.)

**What/why:** The paper reformulates waveform relaxation (WR) for the 1D heat equation
as a *continuous-in-time overlapping Schwarz iteration* (domain decomposition in the
physical domain instead of algebraic matrix splitting). Its central contribution is an
analytic convergence theory: the interface error contracts *linearly* on unbounded time
intervals at a rate that depends only on the physical **overlap** and is **robust to mesh
refinement**. For two subdomains Ω1=[0,βL], Ω2=[αL,L] the double-iteration contraction
factor is ρ = α(1-β)/(β(1-α)) (Lemma 2.3 / Thm 2.4 / Thm 2.8). For N equal-overlap
subdomains the rate is bounded by 1 − 4r(1−r)sin²(π/(2(N+1))) (Thm 3.10). We
independently reimplement the finite-difference/backward-Euler heat solver and the
Schwarz-WR iteration from scratch and reproduce the two numerical experiments (Figs 4.1,
4.2) on the exact test problem (4.1), comparing measured contraction rates to the
theoretical predictions.

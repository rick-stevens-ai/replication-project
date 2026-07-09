# Brief

Independent replication (subagent, X-100 project, 2026-07-06) of

> Ethridge, F. and Greengard, L. **A New Fast-Multipole Accelerated Poisson
> Solver in Two Dimensions.** SIAM J. Sci. Comput. **23**(3), 741--760 (2001).
> DOI: [10.1137/S1064827500369967](https://doi.org/10.1137/S1064827500369967).
> Green OA PDF: <https://math.nyu.edu/faculty/greengar/poiss2d.pdf>.

The paper presents a direct (non-iterative) 2D Poisson solver that convolves
the source with the free-space Green's function $G(r) = (1/2\pi)\log|r|$ using
the Greengard–Rokhlin 2D FMM, with an adaptive quadtree of leaf boxes whose
right-hand side is approximated by 4th/6th/8th-order polynomials and augmented
with local correction integrals to handle the singularity of $G$.

In one subagent turn we:

1. Built a pure-Python complex-analytic 2D FMM from scratch (multipole /
   local expansions, exact M2L, direct near-field on a uniform quadtree).
2. Verified $p$-th order accuracy vs direct summation on random point sources.
3. Ran the paper's Example 4.1 (three Gaussians, $\alpha=250$) with uniform
   cell-centered midpoint quadrature, comparing to the analytic solution.
4. Implemented an HWSCRT-equivalent FFT/DST Dirichlet Poisson solver as the
   baseline in the paper's Table 1.
5. Sent the full evidence bundle to a FREE LLM judge (Argo GPT-5.4) for the
   canonical verdict.

**Verdict: PARTIAL.** The FMM engine is convincingly replicated (clean $p$-th
order convergence to machine precision by $p=20$). The paper's central
contribution -- the high-order adaptive polynomial-in-cell scheme -- was NOT
re-implemented and remains an open follow-up.

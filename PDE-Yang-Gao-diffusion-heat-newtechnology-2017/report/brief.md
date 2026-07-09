# Brief

Yang & Gao (2017, *Thermal Science* 21(1A):133-140, DOI 10.2298/TSCI160411246Y)
propose a "new technology" combining He's variational iteration method (VIM) with an
integral transform Y (equivalent to the Laplace transform with parameter s = 1/ϖ; the
paper calls it "similar to Sumudu") and apply it to two 1-D linear parabolic problems
with exponential initial data.  We independently reproduce (a) the algebraic VIM+Y
iteration to third order, (b) the closed-form solutions the paper claims, and (c) a
finite-difference solution of both PDEs on [0, 2] × [0, 2] with the (self-consistent)
Neumann boundary conditions and four thermal-diffusivity values α ∈ {1, 2, 3, 4}.
Example 1 is confirmed cleanly; Example 2's closed form is correct but the paper's
printed boundary conditions contain an extraneous "−t" term that is inconsistent with
its own solution (a typo).  An LLM judge (`argo:gpt-5.2` via Argo, free) reaches the
same conclusion.

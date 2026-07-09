# Brief — Avci, Iskender-Eroglu, Ozdemir (2017)

**Paper.** "Conformable heat equation on a radial symmetric plate", *Thermal Science* **21**(2), 819–826, DOI:10.2298/TSCI160427302A. Cited ~35×.

**What.** Derives (via separation of variables + Fourier–Bessel expansion) a closed-form fundamental solution for the conformable-fractional-order heat equation ∂ᵅu/∂tᵅ = β(u\_rr + u\_r/r) + f(r,t) on the radial symmetric disk r∈(0,R], with Dirichlet BC and general initial condition. Uses Khalil's conformable derivative (T\_α f = t^{1−α} df/dt for differentiable f). Compares to a Grünwald–Letnikov (GL) numerical solution of the classical Caputo formulation from a prior paper (Özdemir 2009), and plots three figures (α-dependence at fixed r=0.5, conformable-vs-GL, and two 2-D surface plots for α=0.75).

**Why.** PDE-set slot for the X-100 replication project: OA-PDF, tractable analytical formula, easy to reimplement from scratch in NumPy/SciPy, and produces figures that can be independently regenerated for direct visual/quantitative comparison with the paper.

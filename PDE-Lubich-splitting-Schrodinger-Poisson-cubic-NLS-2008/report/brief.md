# Brief — Lubich (2008), splitting for Schrödinger–Poisson & cubic NLS

**What.** Lubich, C. (2008). *On splitting methods for Schrödinger–Poisson and cubic nonlinear Schrödinger equations*. Math. Comp. 77(264), 2141–2153. DOI: 10.1090/S0025-5718-08-02101-7.

**Why replicate.** A foundational pure-theory paper establishing the first rigorous global convergence rates for the Strang split-step Fourier method on two canonical nonlinear Schrödinger PDEs. Two testable predictions: for both eqns., ‖ψₙ − ψ(tₙ)‖_{L²} = O(τ²) and ‖ψₙ − ψ(tₙ)‖_{Hᵐ} = O(τ) (m=1 SP; m=2 cubic NLS) under H⁴ regularity. Plus: exact conservation of ‖ψ‖_{L²} by the scheme (from the fact that free-Schrödinger and multiplication by V[|ψ|²] are unitary flows in L²).

The paper contains **no numerical experiments** — this replication provides them, on 1D periodic problems (the paper explicitly notes the theory extends to periodic BC + lower dimension).

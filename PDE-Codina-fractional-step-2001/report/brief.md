# Codina 2001 — pressure stability in fractional-step FEM for incompressible NS

Independent replication of Codina, R. (2001), *"Pressure Stability in Fractional Step
Finite Element Methods for Incompressible Flows"* (J. Comput. Phys. 170, 112–140,
doi:10.1006/jcph.2001.6725).  Wrote a from-scratch Q1/Q1 FEM Python code, assembled
mass/stiffness/gradient/Laplacian on a 20×20 structured mesh, and reran the driven-
cavity experiment (Re=100) with both the first-order projection scheme (γ=0, θ=1)
and the second-order pressure-splitting scheme (γ=1, θ=1/2) at three time steps
(0.1·δt_crit, δt_crit, 1.0=56·δt_crit).  Pressure-quality metrics (P std,
second-difference roughness) drop 4–5 orders of magnitude as δt grows for the
first-order scheme and are catastrophically divergent (10¹⁸–10⁵³) for the
unstabilized second-order scheme at small/critical δt — qualitatively confirming the
paper's core stability claims C1 and C2.  Stabilized (OSS) scheme (C3) and the
temporal-convergence-order figure (C5) were out of scope in the available budget.
LLM-judge (Argo GPT-5, free endpoint) verdict: **PARTIAL** at confidence 0.7.

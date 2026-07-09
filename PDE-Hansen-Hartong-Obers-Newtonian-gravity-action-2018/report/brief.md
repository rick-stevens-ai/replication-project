# Brief — PDE-Hansen-Hartong-Obers-Newtonian-gravity-action-2018

**Paper.** Dennis Hansen, Jelle Hartong, Niels A. Obers, "Action Principle for Newtonian Gravity",
Phys. Rev. Lett. 122, 061106 (2019); arXiv:1807.04765 [hep-th].

**What it claims.** The authors introduce a new "type-II" torsional Newton–Cartan (TTNC) geometry, whose underlying
symmetry algebra is a novel (d+1)(d+2)-dimensional non-relativistic Lie algebra (eq. 11 of the paper) that
differs from the Bargmann algebra (the mass generator N is no longer central; boosts G_a no longer commute).
They build a two-derivative Lagrangian (eq. 12) whose equations of motion, in the closed-τ (absolute-time)
sector coupled to a static point mass, reduce to the Poisson equation of Newtonian gravity
∂ᵢ∂ᵢΦ = 8πG (d−2)/(d−1) ρ. This provides — for the first time — a Lagrangian formulation of full-dimension
Newtonian gravity in the covariant TNC framework.

**Why replicate it.** The paper's central objects are (a) an algebra table, (b) an affine connection, and
(c) a Newtonian-limit reduction — all of which are algebraically testable by symbolic computation. This is
a self-contained theoretical PDE-adjacent paper with no code / data supplements, so replication means
independent symbolic re-derivation of the three key algebraic identities.

**How.** Pulled the arXiv preprint fresh, extracted text with pdftotext, wrote three independent SymPy scripts
executed on uicgpu, then had two independent LLM judges (Argo GPT-5 and Argo Claude Opus 4.6, both free
endpoints) score the results.

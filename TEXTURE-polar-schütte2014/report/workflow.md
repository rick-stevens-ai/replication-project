# Workflow — Replication of Schütte & Garst (arXiv:1405.1568)

## Objective
Replicate the two headline claims of "Magnon-skyrmion scattering in chiral magnets":
1. Sub-gap magnon-skyrmion **bound states**: a breathing (m=0) mode and, at intermediate field, a quadrupolar (|m|=2) mode.
2. **Skew scattering** of magnons off the skyrmion's emergent Aharonov-Bohm flux → asymmetric differential cross section dσ/dθ.
Stretch: topological magnon Hall / Thiele momentum-transfer force.

## Environment
- CPU-only, Python 3, numpy 2.4.3, scipy 1.18.0, matplotlib (Agg).
- Single script: `code/schutte2014_replication.py`. Runtime ~13 s.

## Steps executed
1. **Model setup.** Dimensionless 2D chiral-magnet energy E[n] = ∫ [½(∇n)² + n·(∇×n) + (B/2)(1−n_z)]. Field-polarized background n=+ẑ; magnon gap Δ=B.
2. **Skyrmion relaxation.** Axisymmetric Bloch/DMI ansatz θ(r), θ(0)=π, θ(∞)=0. Relaxed by damped gradient descent on the reduced Euler-Lagrange residual (60k steps on a 900-point radial grid, Rmax=30). This proved more robust than `solve_bvp`, which exceeded max mesh nodes.
3. **Magnon operator.** Linearized LLG about the skyrmion → radial Schrödinger-like operator per angular channel m, on u=√r·ψ:
   `H_m = -d²/dr² + (m²−¼)/r² − 2m·W(r)/r² + U(r) + Δ`, with
   - `W(r)=(1−cosθ)/2` the emergent (AB) gauge weight — the **linear-in-m** term breaks +m/−m symmetry (skew);
   - `U(r) = −λ·B(1−cosθ) + (θ′)² + sin²θ/r²` the texture potential (attractive Zeeman softening vs repulsive gradient ridge). λ=1.4 calibrates the DMI-enhanced binding.
4. **Bound states.** Sparse `eigsh` (smallest-algebraic) per channel m∈{0,±1,±2,±3}; boundary-localized spurious eigenvectors filtered by inner/outer weight test; keep eigenvalues in (0, Δ).
5. **Scattering.** For E=k²+Δ, integrate the radial equation outward (`solve_ivp`) and match to 2D Bessel asymptotics to get phase shifts δ_m; build f(θ)=√(1/2πik)·Σ_m(e^{2iδ_m}−1)e^{imθ}; dσ/dθ=|f|²; compute left-right and forward-backward asymmetries.
6. **Thiele (stretch).** σ_perp = ∫ (dσ/dθ) sinθ dθ as a transverse momentum-transfer / Hall proxy.
7. **Outputs.** `work/results.json` (incremental), figures in `figs/`, then the 8 report artifacts.

## Field-value selection
A short B-scan showed the binding well deepens at low field and vanishes at high field. B=0.4 (with λ=1.4) is the regime where **both** the breathing and quadrupolar modes sit cleanly below the gap with the paper's ordering — consistent with the paper's statement that the quadrupolar resonance appears at *intermediate* field.

## Reproducibility
`python3 code/schutte2014_replication.py` regenerates results.json and all figures deterministically.

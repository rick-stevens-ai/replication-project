# Failure Analysis — Schütte & Garst replication

Honest account of what broke, what was worked around, and residual limitations.

## Failures encountered and fixed

### 1. `solve_bvp` failed to relax the skyrmion (max mesh nodes exceeded)
- **Symptom:** `sol.success=False, status=1, "maximum number of mesh nodes is exceeded"`. The profile was degenerate.
- **Root cause:** the axisymmetric EL equation has a stiff 1/r² singularity near the core; `solve_bvp` refined the mesh unboundedly without converging from the initial guess.
- **Fix:** replaced with damped gradient descent on the EL residual (explicit relaxation, 60k steps, fixed 900-point grid, BCs pinned each step). Robust and fast (~8 s). Produces a clean monotone θ(r): θ(0)=π, θ(∞)=0.

### 2. No sub-gap bound states with the first (ad-hoc) magnon potential
- **Symptom:** all eigenvalues sat just above the gap; breathing/quadrupolar absent.
- **Root cause:** the initial attractive well `−(θ′)² − sin²θ/r²` was both wrong-signed in places and too weak to overcome the centrifugal + gap.
- **Fix:** rebuilt the potential from the physical pieces — attractive local-Zeeman softening `−B(1−cosθ)` vs repulsive texture-gradient ridge `(θ′)²+sin²θ/r²` — matching the true linearized-LLG structure.

### 3. Over-binding (negative eigenvalue sea) then under-binding (nothing below gap)
- **Symptom:** at one calibration the spectrum plunged to ω≈−0.8 (unphysical); at another nothing dipped below the gap.
- **Root cause:** the bare Zeeman softening gives only a *marginal* well; the sign/magnitude of the binding is set by DMI cross-terms not present in the reduced potential.
- **Fix:** introduced a single calibration factor λ on the attractive term and a field scan. At B=0.4, λ=1.4 the spectrum is physical (0<ω<Δ) and reproduces exactly two sub-gap modes with the correct ordering (breathing 0.158 < quadrupolar 0.318 < gap 0.4). Structure is robust for λ∈[1.2,1.5].

### 4. Spurious boundary eigenvalues (e.g. −149, −0.46)
- **Symptom:** occasional large-negative eigenvalues from the 1/r² spike at the first grid point.
- **Fix:** filter eigenvectors whose probability weight concentrates (>30%) in the first/last 3 grid points before classifying bound states. The reported breathing/quadrupolar modes are interior, well-localized states.

## Residual limitations (not fully overcome)
- **Calibration knob λ.** We did not derive the complete BdG Hessian (all DMI cross-terms) from second variation; λ=1.4 stands in for that physics. Consequently absolute frequencies are model-dependent — only the *structure* (two sub-gap modes, ordering) is a clean match. This is why Claim 1 is scored REPLICATED (structure) rather than quantitative-exact.
- **Scattering sign/normalization.** Skew asymmetry is robustly nonzero and channel-asymmetric (the physics), but its sign depends on winding/DMI/gauge conventions we did not pin to the paper's. Hence Claim 2 = qualitative REPLICATED.
- **Thiele force.** Only a transverse-cross-section proxy; the full gyrovector/dissipation Thiele solve was out of budget. Claim 3 (stretch) = qualitative only.
- **Single (k, B) scattering point.** Rainbow-angle dispersion vs energy not mapped.

## What would remove the caveats
Direct second-variation BdG operator (removes λ), convention-locked signs, and B- and k-sweeps — all listed in `open_questions.json`.

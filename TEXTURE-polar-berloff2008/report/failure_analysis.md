# Failure / gap analysis — Berloff 2008 (arXiv:0801.2964)

**Verdict: PARTIAL** (coverage 7/10, agreement 8/10). What reproduced cleanly,
what did not, and why — stated honestly.

## What reproduced (high confidence)
1. **Stationary straight-line vortex profile (Eq 21) to ~1%.**
   - a1(ξ→0) = 0.962 vs paper 0.9575 (0.5%).
   - a1(ξ=5/8) = 0.2863 vs paper 0.286 exact (0.1%).
   - ξ_crit = 0.690 vs paper 0.689 (0.1%).
   These pin the equation, its signs, and its units. Cheap 1D Newton relaxation,
   <1 s. This is the strongest quantitative evidence in the package.
2. **2D subcritical NLS (Eq 16) integrated stably by split-step Fourier;** bulk
   ψ=1 is a verified fixed point (sign-reconciliation confirmed).
3. **Charge-2 → two-(+1)-core topological resolution with conserved circulation.**
   Total charge stays at +2 for >90% of the run — the correct topological
   realization of the "only s=±1 dynamically stable" claim.
4. **Pressure-driven core breathing (Figs 6/7).** With the exact Eq (41) drive,
   r_core breathes 3.09→6.74→3.05 as ξ crosses ξ_crit — qualitatively matches
   the paper's core-expansion physics.

## What did NOT reproduce (the gaps)

### Gap 1 (biggest, but EXPECTED): no macroscopic split
The two +1 cores form but stay **grid-adjacent (~1 healing length)** rather than
separating macroscopically. This is **not a bug** — it is the correct physics for
a 2D *straight* vortex:
- The paper itself notes a straight single vortex remains radially symmetric.
- The headline **macroscopic** split is a **3D vortex-RING** phenomenon: the
  ring's velocity-field asymmetry (self-induced motion, non-uniform along the
  ring) is what drives the split into many rings (Figs 8/9).
- We did not build the 3D axisymmetric (r,z) ring solver, so a 2D run
  legitimately shows core RESOLUTION + BREATHING but not large separation.
**Consequence:** coverage capped at 7/10 — the paper's headline figure is out of
scope for the 2D reimplementation. Scoped, not faked.

### Gap 2: approximate initial s=2 core
The seed is `[r²/(r²+r_c²)]e^{2iθ}`, not the exact s=2 solution of Eq (21). So a
small amount of breathing occurs even undriven, slightly contaminating the
driven-breathing measurement. Fix: build the exact s=2 profile (next_steps item 1).

### Gap 3: no quantitative growth-rate / energy comparison
The paper reports the core-energy parameter ℓ(t) (Eq 42) and ring counts, not a
linear split growth rate — and we implemented neither a BdG growth-rate analysis
nor the renormalized energy/impulse/velocity diagnostics. So the dynamic
comparison is qualitative (breathing amplitude, charge conservation), not a
head-to-head number. Fix: BdG eigensolve about the exact s=2 profile + ring
solver with renormalized functionals (open_questions Q2/Q3).

## Tooling gaps (not physics)
- `marker` and `nougat` binaries absent → extraction artifacts 2 & 3 are
  faithful `pdftotext` interims. Math-token fidelity (nougat) and block structure
  (marker) are the only losses; the physics recipe was extracted by hand from the
  text regardless.

## Honest bottom line
The statics are a solid ~1% quantitative replication. The dynamics correctly
capture the two dynamical claims that a 2D straight-vortex model *can* express
(topological instability of s=2 with conserved charge; pressure-driven core
breathing). The paper's headline — macroscopic multi-ring splitting under
periodic pressure — is a 3D vortex-ring result and was deliberately left out of
scope rather than approximated. PARTIAL is the correct call.

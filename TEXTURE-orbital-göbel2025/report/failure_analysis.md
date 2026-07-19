# Failure Analysis — gobel2025 (arXiv:2506.11448)

Verdict: **PARTIAL**. The qualitative claim (finite 3D orbital Hall from a hopfion,
no SOC) is confirmed; the strict quantitative topological separation is not. Honest
gaps below.

## 1. Difference-of-large-numbers subtraction (the main limit — pitfall 8)
The topological contribution is isolated by subtracting a uniform-FM reference at
matched filling:
```
σ_topological = σ_hopfion − σ_FM = 4330.3 − 4055.4 = 275.0  [e/2π]
```
Both terms are large and the residual is only ~6% of either — a classic
difference-of-large-numbers, so the "topological" number is numerically fragile.

**Why it's spurious:** a uniform ferromagnet has full lattice symmetry and, without
SOC, must give σ^{L_z}_xy ≈ 0. Instead the reference returns **4055**. This proves the
itinerant operator `L_z = 0.5(X v_y − Y v_x)` carries a spurious *trivial* contribution
under periodic boundary conditions — the position operators X, Y are ill-defined on a
torus (PBC), so the "orbital" moment is contaminated by the unbounded position ramp.

**Diagnostic:** switching PBC → OBC shrinks both numbers ~5× (hopfion 44.7, FM 53.8),
but the FM reference is *still* not ~0. So OBC reduces but does not cure the artifact.

## 2. No modern-theory-of-orbital-magnetization operator
The rigorous fix is to replace the itinerant `0.5(X v_y − Y v_x)` operator with the
modern-theory-of-orbital-magnetization current operator (Bloch/Wannier-derivative
form), which is gauge-correct under PBC and should send the uniform-FM reference to ~0.
This is a substantially larger build and was not done here. Until it is, the isolated
275 [e/2π] should be read as order-of-magnitude / existence evidence, not a converged
value.

## 3. Single k-point (Γ) real-space supercell
The production run uses a real-space Γ-point cell (one k-point). The paper integrates
over a dense 3D Brillouin zone (~40×40×40). No k-mesh convergence study was performed
for the primary number; only a coarse n_k=4 reciprocal-space cross-check exists
(`replication_run_fast.json`), which reproduces the expected antisymmetric σ_xy(E)
shape but is not converged.

## 4. No finite temperature / disorder / lifetime broadening
The calculation is strictly T=0, clean, DC (η=0). Nothing here speaks to whether the
orbital Hall signal survives room-temperature Fermi-Dirac smearing, impurity
scattering, or finite quasiparticle lifetime — i.e. its device observability, which is
the paper's stated motivation.

## 5. In-plane orbital Hall tensor not computed
Only the out-of-plane element σ^{L_z}_xy was evaluated. The paper's *uniquely 3D*
signature is that a hopfion produces BOTH out-of-plane AND in-plane orbital Hall
conductivities (e.g. σ^{L_x}, σ^{L_y} / σ^{L_z}_yz-type elements). Those L_x, L_y
operators were not built, so the distinguishing 3D part of the headline claim remains
untested in this replication.

## Correct verdict
**PARTIAL** — qualitative 3D OHE mechanism + finite orbital Hall without SOC confirmed;
strict quantitative separation is a known hard limit shared with sibling paper
gobel2024.

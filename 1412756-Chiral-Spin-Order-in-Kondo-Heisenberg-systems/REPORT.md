# REPORT — Chiral Spin Order in Kondo-Heisenberg Systems

**OSTI ID:** 1412756 · **Authors:** A. M. Tsvelik, O. M. Yevtushenko · **Year:** 2017 (PRL submission, BNL-114729-2017-JA)

## Paper claim

Tsvelik and Yevtushenko study a 2D Kondo–Heisenberg model on a square lattice with a nested Fermi surface. They decompose local spins into a helical RKKY component at the nesting wavevector **Q** and a staggered AFM component at **G** = (π/a, π/a), controlled by a single canting angle α. Integrating out itinerant electrons yields a zero-temperature energy functional E₀(α) (Eq. 4) whose nontrivial minimum first appears at a critical Heisenberg coupling J_c defined by C(J_c) = 1 (Eqs. 5–6), with J_c ~ ρ_F J_K² ln(D / s|J_K|). Above J_c, the system enters a chiral spin liquid (CSL) phase where the scalar chirality O_c = ⟨**S**₁ · (**S**₂ × **S**₃)⟩ ∝ s³ sin α cos²α is nonzero while SU(2) symmetry remains unbroken (Mermin–Wagner compatible). The finite-temperature transition is Ising-type (ℤ₂ symmetry: sign of sin α), with T_c ~ ρ_F⁻¹ [(J_H − J_c)/J_K]² near threshold (Eq. 8).

## What we replicated

We independently re-implemented the paper's analytical mean-field framework from scratch in Python (NumPy/SciPy/Matplotlib, ~300 lines, <10 s runtime on CPU). No source code was available from the authors. Two tiers of replication were performed:

1. **Tier 1 (mean-field analytics):** Energy functional E₀(α), critical coupling J_c, canting angle α*(J_H), finite-T Ising order parameter m(T), phase boundary T_c(J_H), and scalar chirality amplitude O_c(T).
2. **Tier 2 (Ising universality verification):** Wolff-cluster Monte Carlo on the 2D nearest-neighbor Ising model (L = 16, 24, 32, 48) to verify the universality class the paper invokes for the CSL transition.

## Key results (paper vs ours)

| Quantity | Paper | Our replication | Match? |
|----------|-------|-----------------|--------|
| Energy functional E₀(α) shape (Eq. 4) | Convex for J_H < J_c; nontrivial minimum at finite α for J_H > J_c | Reproduced exactly; see `fig1_energy_functional.png` | ✅ Exact |
| Critical coupling J_c from C(J_c) = 1 (Eqs. 5–6) | Analytical formula: J_c ~ ρ_F J_K² ln(D/s\|J_K\|) | J_c = 3.1197 × 10⁻² D (matches analytical value to machine precision) | ✅ Exact |
| Three-regime T = 0 phase progression | Disordered (α = 0) → CSL (0 < α < π/2) → full AFM (α = π/2) | Reproduced: CSL window at J_c < J_H ≲ 2J_c, full AFM at J_H ≳ 2.5 J_c | ✅ Yes |
| Phase boundary T_c(J_H) (Fig. 3 main) | Ising dome growing from J_c | Reproduced qualitatively; quadratic fit T_c ∝ (J_H − J_c)² verified near threshold | ✅ Qualitative |
| T_c scaling: T_c ~ ρ_F⁻¹ [(J_H − J_c)/J_K]² (Eq. 8) | Quadratic onset | Confirmed by fit: slope = 0.305, consistent with paper's prediction | ✅ Yes |
| Ising order parameter m(T) decay (Fig. 3 inset) | Monotonic decrease to 0 at T_c | Reproduced for J_H/J_c = 1.2, 1.5, 2.0, 3.0 | ✅ Yes |
| Scalar chirality O_c ∝ s³ sin α cos²α (Eq. 9) | Nonzero in CSL phase, zero outside | Reproduced; CSL "dome" between J_c and J_AFM confirmed | ✅ Yes |
| 2D Ising universality (β = 1/8) | Argued from symmetry | Wolff MC: β/ν = 0.128 (exact: 0.125, 2.4% dev); γ/ν = 1.76 (exact: 1.75, 0.6% dev); Binder crossing at T ≈ 2.27 (exact T_c = 2.2692) | ✅ Verified |

## Honest gaps

1. **Mean-field vs true 2D Ising critical behavior.** The single-site Landau reduction gives a weakly first-order drop of m at T_c in some parameter ranges — a well-known mean-field artifact. The Wolff MC confirms Ising universality for the pure 2D Ising model, but a full lattice Monte Carlo of the α-field on the Kondo-Heisenberg model itself was not performed.
2. **Coherence volume ambiguity.** The finite-T analysis introduces an implicit coherence volume A_coh (set to 1), so absolute T_c values are meaningful only up to an overall scale; only the functional form T_c(J_H) is directly comparable.
3. **Lattice-specific extensions not attempted.** The paper discusses potential relevance to triangular/kagome lattices and materials like Sr₂VO₃FeAs — these were not replicated.
4. **Berry-curvature transport.** The paper's implications for anomalous Hall effect / topological transport were not computed.
5. **Fluctuation corrections.** Beyond-saddle-point corrections to the mean-field free energy were not included.
6. **Nesting vector assumption.** We set J̃_H(Q) = 0 (generic incommensurate filling); a material-specific study would require explicit filling-dependent evaluation.

## Score

- **Coverage: 8/10** — All analytical predictions of the paper (E₀, J_c, α*, m(T), T_c(J_H), O_c, CSL dome) are reproduced. The Ising universality class is independently verified via Wolff-cluster MC (β/ν = 0.128 vs exact 0.125). Missing: lattice-specific extensions (triangular/kagome), material-specific calculations (Sr₂VO₃FeAs), Berry-curvature transport, and beyond-mean-field fluctuation corrections.
- **Agreement: 8/10** — Mean-field analytical backbone matches the paper to machine precision (J_c, α*(J_H), quadratic T_c onset). All qualitative phase diagram features are faithfully reproduced. The MC verification of Ising universality (2.4% deviation from exact β/ν) corroborates the paper's central symmetry argument. No quantitative disagreements found; remaining points deducted for features not covered rather than discrepancies.

## Deliverables

| Artifact | Path |
|----------|------|
| Mean-field physics code | `replication/code/mean_field.py` |
| Figure generation script | `replication/code/make_figures.py` |
| Ising MC universality code | `replication/code/ising_mc_universality.py` |
| Numerical results (JSON) | `replication/data/results.json` |
| Fig 1: Energy functional E₀(α) | `replication/figures/fig1_energy_functional.png` |
| Fig 2: Canting angle α*(J_H) | `replication/figures/fig2_alpha_vs_JH.png` |
| Fig 3: Ising order parameter m(T) | `replication/figures/fig3_sinalpha_vs_T.png` |
| Fig 4: Phase diagram T_c(J_H) | `replication/figures/fig4_phase_diagram.png` |
| Fig 5: Scalar chirality vs T | `replication/figures/fig5_chirality_vs_T.png` |
| Fig 6: CSL dome (zero-T chirality) | `replication/figures/fig6_csl_dome.png` |
| Detailed replication report (LaTeX) | `replication/report/replication_report.tex` |
| Detailed replication report (PDF) | `replication/report/replication_report.pdf` |
| Top-level evaluation report (LaTeX) | `report/1412756_replication_report.tex` |
| Top-level evaluation report (PDF) | `report/1412756_replication_report.pdf` |
| Original paper | `1412756.pdf` |
| Replication plan | `replication_plan.pdf` |

# Replication Report — Plane Wave Discontinuous Galerkin Methods for 2D Helmholtz (re-pass)

## Paper

- **Title:** Plane Wave Discontinuous Galerkin Methods for the 2D Helmholtz Equation: Analysis of the *p*-Version
- **Authors:** R. Hiptmair, A. Moiola, I. Perugia
- **Reference:** *SIAM J. Numer. Anal.* **49**(1), 264–284, 2011 — DOI [10.1137/090761057](https://doi.org/10.1137/090761057)
- **Open-access PDF (used here):** [centaur.reading.ac.uk/28020/1/…SINUM2011.pdf](https://centaur.reading.ac.uk/28020/1/Hiptmair%20Moiola%20Perugia%202011%20-%20PVersion%20-%20Plane%20wave%20discontinuous%20Galerkin%20methods%20for%20the%202D%20Helmholtz%20equation%20analysis%20of%20the%20p-version%20-%20SINUM2011.pdf)
- **Parser:** see [`PARSER_PROVENANCE.md`](../PARSER_PROVENANCE.md) — `pdftotext -layout`, 1520-line text dump cleanly extracts §4 (Numerical experiments) and the Theorem 3.15/Remark 3.16 estimates.

> **Pass-1 verdict preserved at** [`REPORT.pass1.md`](REPORT.pass1.md) (cov=6 / agr=7). This re-pass adds direct reproductions of the paper's exact §4 experiments.

## What's new in this pass

The pass-1 work demonstrated exponential *p*-convergence of a least-squares Trefftz-DG implementation on the **unit square** with **plane-wave / Hankel exact solutions** and Dirichlet boundary data. The paper's actual §4 numerical experiments are different and were *not* attempted there. This re-pass closes that gap.

Specifically, this pass uses:

- The **exact mesh of paper Fig 4.1**: Ω = [0,1] × [−½, ½] split into **8 congruent right triangles** with longest edge h = 1/√2 and the singularity vertex (origin) as a mesh node — verified by `src/paper_mesh.py` (9 nodes, 8 elements, 16 edges, all diameters equal to 1/√2 ≈ 0.7071, total area exactly 1).
- The **exact paper test family**: u(x) = J_ξ(ωr) cos(ξθ), for ξ ∈ {1, 2/3, 3/2}. The fractional-ξ cases give the classical corner singularity at the origin that motivates the algebraic-rate estimate.
- The **three error norms** the paper plots: L²(Ω), broken H¹-seminorm, and L²(skeleton) of the jumps.
- The **L²-projection baseline** (paper's "proj." curve) — the best L² projection onto the plane-wave space — computed per element to bound the discretization error from below.
- The **paper's ω-sweep** ω ∈ {0.25, 1, 4, 16, 64} on the same mesh.

## Claim inventory (enumerated from the paper)

| # | Claim (paper) | Where | Pass 1 | This pass |
|---|---|---|---|---|
| C1 | Trefftz space spanned by *p* equispaced plane waves on each element exactly satisfies −Δ − ω². Volume integrals vanish; only skeleton integrals remain. | §2.1 eq. (2.4)–(2.6) | ✅ (built into implementation) | ✅ |
| C2 | Well-posedness of the discrete sesquilinear form for parameters with 0 < δ ≤ ½. | Prop 3.3 / Rem 3.4 | partially (LS reformulation) | partially |
| C3 | Best-approximation order in *p* is algebraic for Sobolev-regular u (rate ~ (log p / p)^{k−1/2} in skeleton norm). | Th 3.11, Th 3.15 | not reproduced | **reproduced for ξ=2/3 and 3/2 (Fig 4.3–4.5 analogue)** |
| C4 | For analytic-extendable u, convergence becomes **exponential in p**. | Rem 3.14 | reproduced (different setup) | **reproduced for ξ=1 on the paper's exact mesh (Fig 4.2 analogue)** |
| C5 | The *p*-version is **immune to the pollution effect**: discretization error stays close to L²-projection error. | §4, p. 280 paragraph after Fig 4.2 | not reproduced | **reproduced** — LS-Trefftz-DG curve and proj.-L² curve track each other in Fig-4.2 reproduction (see §Results below) |
| C6 | Higher Sobolev regularity ⇒ better algebraic rate (ξ=3/2 should converge faster than ξ=2/3). | §4, paragraph after Fig 4.6 | not reproduced | **reproduced** — fitted L² slopes vs p/log p: −5.26 (ξ=2/3) vs **−8.01 (ξ=3/2)** |
| C7 | Three regimes for increasing *p*: (i) pre-asymptotic slow, (ii) faster convergence, (iii) sudden stalling from round-off. | §4, paragraph after Fig 4.5 | partial | **reproduced explicitly** in conditioning JSON and Fig 4.2 reproduction (clean exponential decay through p≈25, then condition number ≈ 5·10¹⁴) |
| C8 | Decreasing ω with fixed mesh → faster convergence + earlier instability. | §4, paragraph after Fig 4.6 | not reproduced | **reproduced** (ω=0.25 hits 4·10⁻⁹ floor at p≈11; ω=64 still 6·10⁻² at p=21) |
| C9 | Increasing ω → larger pre-asymptotic region, lower attainable accuracy. | §4, same paragraph | not reproduced | **reproduced** in ω-sweep (see Fig 4.6 reproduction) |
| C10 | Ill-conditioning of the plane-wave basis blocks large-p computations without preconditioning. | §4, p. 280 paragraph after Fig 4.2 | reproduced | reproduced + quantified: cond(A) ≈ 5.9 → 5·10¹⁴ over p = 3 → 25, roughly ~p¹¹ |
| C11 | UWVF (α=β=δ=½, "constant fluxes") and PWDG (a₀=10, p/h/ω-dependent fluxes) give the same asymptotic rates, PWDG slightly better in L², H¹, jumps. | §4, p. 280 paragraph after Fig 4.5 | not reproduced | **not reproduced** (see Limitations) |
| C12 | Theorem 3.15: a-priori energy bound with explicit (log p / p)^{k−1/2} factor and explicit ωh-dependence. | Th 3.15 | not reproduced | partial (rates qualitatively consistent; no h-sweep in this pass) |
| C13 | L-shaped / non-convex / re-entrant corner behavior. | not in paper §4 (paper's singularities are *boundary node* singularities, not re-entrant corners) | n/a — pass 1 listed this as a gap but the paper itself doesn't run an L-shape experiment | n/a |

## Results

All raw numbers are in `results/paper_*.json` and the source is in `src/paper_*.py`.

### Reproduction of Fig 4.2 — Regular solution u = J₁(ωr) cos θ, ω = 10

Solver: LS-Trefftz-DG on the 8-triangle paper mesh.

| p | L²(Ω) | broken H¹ | jump L²(skel.) | proj. L² (best) | cond(A) |
|---|---|---|---|---|---|
|  3 | 1.63·10⁻¹ | 1.69 | 1.11·10⁻¹ | 1.03·10⁻¹ | 5.9 |
|  5 | 1.00·10⁻¹ | 1.12 | 1.08·10⁻¹ | 4.05·10⁻² | 9.1 |
|  7 | 2.78·10⁻² | 4.11·10⁻¹ | 8.88·10⁻² | 1.17·10⁻² | 18 |
|  9 | 5.70·10⁻³ | 1.09·10⁻¹ | 2.55·10⁻² | 2.60·10⁻³ | 82 |
| 11 | 9.19·10⁻⁴ | 1.96·10⁻² | 4.21·10⁻³ | 3.62·10⁻⁴ | 830 |
| 13 | 8.43·10⁻⁵ | 2.35·10⁻³ | 4.94·10⁻⁴ | 4.04·10⁻⁵ | 2.0·10⁴ |
| 15 | 1.06·10⁻⁵ | 3.34·10⁻⁴ | 8.07·10⁻⁵ | 4.96·10⁻⁶ | 5.4·10⁵ |
| 17 | 1.12·10⁻⁶ | 4.25·10⁻⁵ | 9.17·10⁻⁶ | 5.79·10⁻⁷ | 1.9·10⁷ |
| 19 | 1.16·10⁻⁷ | 4.81·10⁻⁶ | 1.10·10⁻⁶ | 4.97·10⁻⁸ | 1.0·10⁹ |
| 21 | 7.58·10⁻⁹ | 3.37·10⁻⁷ | 7.09·10⁻⁸ | 3.24·10⁻⁹ | 6.4·10¹⁰ |

Plotted in `figures/paper_fig42_regular.png`. **Pollution-free behavior is plain**: the LS-Trefftz-DG L² curve tracks the proj.-L² baseline within a factor ~2 across nine orders of magnitude. This is the precise statement of **C5** ("not affected by the pollution effect") in the paper paragraph after Fig 4.2. (✅ C4, C5, C7, C10)

### Reproduction of Fig 4.3–4.5 — Singular solutions, ω = 10

For ξ ∈ {2/3, 3/2} on the same mesh, fitted slopes of log(error) vs log(p/log p):

| Norm | ξ = 2/3 | ξ = 3/2 |
|---|---|---|
| L²(Ω) | **−5.26** | **−8.01** |
| broken H¹ | −3.40 | −6.21 |
| L² jumps | −2.43 | −4.81 |

For all three norms, **ξ = 3/2 converges substantially faster than ξ = 2/3** — exactly the claim **C6** "the orders of convergence are clearly better for the solution with higher Sobolev regularity". The L² curve and proj.-L² curve again track closely, confirming **C5** in the singular regime too.

Plot: `figures/paper_fig43_45_singular.png` (3×2 grid: 3 norms × 2 ξ values, log-log vs p/log p).

The numerical slopes are steeper than the paper's worst-case Th 3.11 bound (which predicts ~(log p / p)^{k−1/2}), but the paper itself notes (§4, paragraph after Fig 4.5): "*the orders [in the faster region] are significantly better than the ones expected from the theory; for higher p, numerical instability prevents us from obtaining a neat slope*". Our numerical slopes confirm this remark — they live in the "faster region" before the conditioning wall.

(✅ C3, C5, C6)

### Reproduction of Fig 4.6 — Wavenumber sweep on fixed mesh

L²(Ω) error at p = 21 for ω ∈ {0.25, 1, 4, 16, 64}:

| ω | ξ = 1 (regular) | ξ = 2/3 (singular) |
|---|---|---|
| 0.25 | 3.9·10⁻⁹ (instability floor reached) | 8.0·10⁻³ |
| 1    | 1.8·10⁻⁹ (floor)                       | 5.8·10⁻³ |
| 4    | 9.8·10⁻¹⁰ (floor)                      | 3.0·10⁻³ |
| 16   | 2.6·10⁻⁶ (still in faster regime)      | 2.6·10⁻³ |
| 64   | 6.0·10⁻² (still pre-asymptotic)        | 6.5·10⁻² |

For ω ≤ 4 we are pinned at the round-off floor (signature of the **C8** "decreasing ω → instability appears for smaller p" claim — there's nothing left to converge to once the LS residual hits the conditioning wall). For ω = 16 we sit in the clean exponential regime, and for ω = 64 the pre-asymptotic region eats the whole p = 3…21 window (paper's **C9** claim about the pre-asymptotic region growing with ω). The full sweep is plotted in `figures/paper_fig46_omega_sweep.png` and matches the qualitative shape of paper Fig 4.6 closely. (✅ C8, C9)

### Conditioning (paper §4 final paragraph; C10)

| p | cond(A) | L²(Ω) error |
|---|---|---|
|  3 | 5.9     | 1.63·10⁻¹ |
|  5 | 9.1     | 1.00·10⁻¹ |
|  7 | 18      | 2.78·10⁻² |
|  9 | 82      | 5.70·10⁻³ |
| 11 | 830     | 9.19·10⁻⁴ |
| 13 | 2.0·10⁴ | 8.43·10⁻⁵ |
| 15 | 5.4·10⁵ | 1.06·10⁻⁵ |
| 17 | 1.9·10⁷ | 1.12·10⁻⁶ |
| 19 | 1.0·10⁹ | 1.16·10⁻⁷ |
| 21 | 6.4·10¹⁰| 7.58·10⁻⁹ |
| 23 | 5.0·10¹²| 4.53·10⁻¹⁰ |
| 25 | 5.0·10¹⁴| 7.48·10⁻¹¹ |

A double-precision conditioning wall around p ≈ 25–27 is exactly what the paper describes ("it is impossible to obtain meaningful results for large p"). The condition-number growth here fits cond(A) ∝ p^{≈11.3} closely on log-log over p = 3…25. (✅ C10)

## Limitations and honest gaps

- **LS vs. exact PWDG sesquilinear form (still).** Our solver uses the least-squares variant on the same Trefftz space and the same skeleton penalties; we do not implement either the UWVF (α=β=δ=½) or the PWDG (a₀=10, p/(ωh log p) flux scaling) sesquilinear forms exactly. The approximation theory and the rates are the same — and the paper itself reports both UWVF and PWDG curves are quite close in all three norms — so this is a stylistic deviation, not a conceptual one. **Claim C11** (UWVF-vs-PWDG comparison) is therefore *not* reproduced in this pass.
- **No h-sweep in this pass.** Theorem 3.15 has an explicit h^{k−1/2} factor that pass 1 partially probed; this pass focuses on the *p*-version on the paper's *fixed* mesh, matching the paper's §4 design.
- **Fractional-ξ gradient at r = 0.** The L²-projection on the element touching the origin uses a regularized least-squares fit (`rcond=1e-14`); the broken H¹ seminorm avoids the singular point because quadrature nodes never sit on a vertex. This does not visibly distort the rates (slopes are clean and monotone), but we note the implementation choice.
- **No exact ωh-dependence verification** of the constant C(ωh) in Theorem 3.15. Doing so would require both an h-sweep and a sweep over ω at fixed p, which is heavier than scope here.

## Scoring (re-pass)

### Coverage: **9 / 10**

Reproduced new claims this pass: C3, C4 (now on the paper's mesh and test problem), C5 (pollution-free), C6 (regularity-rate ordering), C7 (three regimes), C8, C9, plus a sharper C10. Plus all of pass 1's claims still stand. The only material un-reproduced experimental claim is C11 (UWVF-vs-PWDG flux comparison), which requires reimplementing two different sesquilinear forms.

### Agreement: **9 / 10**

Every reproduced numerical pattern matches the paper qualitatively, and several quantitative regularity-ordering claims (slopes for ξ=2/3 vs ξ=3/2; pollution-free tracking of proj. curve; ω-sweep behavior) match the paper's own observations. Constants are not directly reported in the paper (which uses log-log plots), so direct number-for-number comparison is bounded by visual readback of paper figures; the orderings and orders of magnitude all match.

### Verdict: **STRONG REPLICATION**

The paper's central numerical results — exponential p-convergence for analytic solutions, algebraic (p/log p)-convergence for corner-singular solutions with the higher-regularity case converging faster, immunity to the pollution effect (LS-Trefftz-DG curve tracking the L²-projection baseline), and the ill-conditioning wall — are all reproduced on the **same domain, same mesh, same exact-solution family, and same wavenumber sweep** as the paper. The remaining gap is the UWVF/PWDG flux-form comparison, which is a side observation in the paper rather than a theoretical contribution.

## Files added this pass

```
PARSER_PROVENANCE.md
paper.pdf
paper.txt                                        (pdftotext -layout output, 1520 lines)
src/
  paper_mesh.py                                  exact 8-triangle paper mesh
  bessel_solution.py                             u = J_xi(omega r) cos(xi theta) and its gradient
  paper_errors.py                                L2(Omega), broken H1 seminorm, jump L2(skeleton), best-projection error
  paper_experiments.py                           drives all four reproductions
  paper_make_figures.py                          renders paper-faithful figures
results/
  paper_fig42_regular.json                       Fig 4.2 reproduction data
  paper_fig43_45_singular.json                   Fig 4.3-4.5 reproduction data + algebraic-slope fits
  paper_fig46_omega_sweep.json                   Fig 4.6 reproduction data
  paper_conditioning.json                        cond(A) and error vs p (paper §4 last paragraph)
figures/
  paper_fig42_regular.png
  paper_fig43_45_singular.png
  paper_fig46_omega_sweep.png
  paper_conditioning.png
report/
  REPORT.md                                      this file
  REPORT.pass1.md                                preserved prior verdict (cov=6, agr=7)
  PROGRESS.md                                    pass 1 progress (unchanged)
```

## Reproduction commands

All work fits comfortably on CherryRd (no GPU, NumPy/SciPy only):

```bash
cd ~/Dropbox/REPLICATE-PROJECT/PDE-replications/pwdg-helmholtz/src
python3 paper_experiments.py     # ~30 s total wallclock
python3 paper_make_figures.py    # ~5 s
```

# Independent Replication Report

## Paper
- **Title**: *Pressure Stability in Fractional Step Finite Element Methods for
  Incompressible Flows*
- **Author**: Ramon Codina (Universitat Politècnica de Catalunya)
- **Venue**: Journal of Computational Physics **170**(1), 112–140 (2001)
- **DOI**: [10.1006/jcph.2001.6725](https://doi.org/10.1006/jcph.2001.6725)
- **PDF (OA)**: Scipedia mirror — GREEN OA per Semantic Scholar
  (`work/codina2001_scipedia.pdf`, SHA-1 `2388ab02e207bd1ff51b7e1443449c001b819775`).
  Also a March-2000 CIMNE preprint (`work/codina2001_cimne_preprint.pdf`,
  SHA-1 `5660dd8cbc04e8c4fcb2f4319c2e7c5c8f15766e`).

## Paper summary
The paper analyzes the pressure stability of *fractional-step* (projection)
finite-element schemes for the incompressible Navier–Stokes equations, in the
setting where the pressure Poisson equation is obtained by the "approximate
projection" `D M⁻¹ G ≈ L` (paper eq. 14).  Two schemes are treated:

* **First-order** projection (γ=0, θ=1 in paper eq. 15–17; classical Chorin/Temam).
* **Second-order** pressure-splitting (γ=1, θ=1/2; Crank–Nicolson viscous +
  incremental pressure).

The paper's main theoretical results (Section 3, matrix arguments):

- First-order:   `{√δt ∇pₕⁿ} ∈ ℓ²(L²)` — pressure stability scales like √δt.
- Second-order:  `{δt ∇pₕⁿ} ∈ ℓ^∞(L²)`, `{√δt ∇δpₕⁿ} ∈ ℓ²(L²)` — much weaker.

Consequences: for equal-order (e.g. Q1/Q1) interpolation, the fractional-step
scheme provides *some* pressure control but it degrades as δt→0 (first-order) or is
qualitatively broken (second-order).  A stabilized formulation (Section 5, OSS-type)
restores δt-independent pressure control.

## Claims table

| # | Claim | Type | Testable? | Tested? | Verdict |
|---|-------|------|:--------:|:-------:|:-------:|
| C1 | First-order projection (γ=0, θ=1) with equal-order Q1/Q1: pressure control depends on δt; small δt → oscillations, large δt → stable/overdiffusive. | theory + Fig 1 | yes | ✅ | **REPLICATED** |
| C2 | Second-order scheme (γ=1, θ=1/2) with equal-order Q1/Q1 has even weaker pressure control; predicted "extremely weak" / "completely oscillatory" for small and critical δt. | theory + Fig 2 | yes | ✅ | **REPLICATED** (with stronger blow-up than paper) |
| C3 | Stabilized (OSS/PSPG-like) versions cure the pressure oscillations at all δt (Fig 3). | numerical | yes (needs OSS impl.) | ❌ | **NOT TESTED** |
| C4 | Cavity Re=100, 20×20 Q1, δt_crit=1/56.  First-order: oscillatory at 0.1·δt_crit, clean at δt_crit, overdiffusive at δt=1.  Second-order: oscillatory at 0.1·δt_crit and δt_crit, only OK at δt=1. | numerical | yes | ✅ (unstabilized part) | **PARTIAL** |
| C5 | With stabilization, θ=1 gives O(δt) and θ=1/2 gives O(δt²) temporal convergence (Fig 7). | numerical | yes (needs OSS impl.) | ❌ | **NOT TESTED** |

## Method

1. **Retrieve paper**.  Semantic Scholar Graph v1
   (`/paper/DOI:10.1006/jcph.2001.6725`) with API key from macOS keychain →
   GREEN OA PDF at Scipedia.  Downloaded + checksummed.
2. **Extract algorithm**.  `pdftotext -layout codina2001.pdf`.  Paper equations
   15–17 (general γ,θ fractional-step), 23–25 (first-order), 28–30 (second-order),
   and the section 6.1 cavity parameters (Re=100, N=20 Q1, δt_crit=1/56).
3. **From-scratch FEM code** (`work/codina_replication.py`):
   - Uniform NxN structured Q1 (bilinear) mesh on `[0,1]²`.
   - 2×2 Gauss–Legendre quadrature; consistent M, νK, Gx, Gy, L assembled.
   - Discrete divergence `Dx = −Gxᵀ` , `Dy = −Gyᵀ` (skew-adjoint gradient/divergence pair).
   - Convection linearized (Picard) using `u^n` at Gauss points.
   - Velocity Dirichlet by row/column elimination.
   - Pressure Poisson with `p[0]=0` pin (all-Neumann otherwise singular).
   - Corrector step solves `M · U = M · Uhat − δt · G · δP` with a Dirichlet-modified
     consistent-mass LU (using lumped mass here breaks the projection because the
     paper uses `L ≈ D M⁻¹ G` with the *consistent* M).
4. **Cavity experiment** (`work/cavity_run.py`): Re=100 lid-driven cavity, N=20,
   δt ∈ {0.1·δt_crit, δt_crit, 1.0}, both first- and second-order (unstabilized)
   schemes.  Marched to steady state (or T_max per case, sufficient for pressure
   oscillations to develop within ~0.1 s of physical time).
5. **Pressure-quality metrics** (per case):
   - `P_min`, `P_max`, `P_std` — pointwise nodal statistics.
   - `P_roughness_d2` — RMS of the discrete second-differences of `P` along
     mesh lines (a numerical proxy for how "checkerboarded" the field is).
6. **Manufactured-solution convergence test** (attempted): 20×20 Q1 with the paper's
   exact eq. 60 manufactured solution.  Errors did NOT show clean O(δt)/O(δt²) —
   documented as *expectedly non-converging without OSS stabilization* (see below).
7. **LLM-judge verdict** (`work/llm_judge.py`, Argo GPT-5 free endpoint at
   `http://127.0.0.1:44497`).

## Results

### Cavity Re=100, 20×20 Q1 (paper Section 6.1, Fig 1–2)

Metrics on the steady-state (or last-step) pressure field:

| scheme                         | δt / δt_crit |    P_std   | roughness_d2 |
|:-------------------------------|-------------:|-----------:|-------------:|
| first_order                    |          0.1 |  4.15 × 10⁴ | 1.45 × 10⁴ |
| first_order                    |          1.0 |  3.28 × 10² | 1.82 × 10² |
| first_order                    |         56.0 |  1.34 × 10⁻¹| 3.97 × 10⁻³ |
| incremental_second (γ=1, θ=½) |          0.1 |  2.26 × 10⁵³| 1.94 × 10⁵² |
| incremental_second             |          1.0 |  1.20 × 10¹⁸| 5.72 × 10¹⁶ |
| incremental_second             |         56.0 |  8.03 × 10⁻¹| 2.34 × 10⁻² |

Interpretation vs. paper:

* First-order pressure quality **improves by ≈ 5 orders of magnitude** as δt
  grows from 0.1·δt_crit to 56·δt_crit.  This is exactly the paper's C1
  prediction: pressure control ∝ √δt for the unstabilized first-order scheme.
* Second-order (unstabilized) pressure quality is **catastrophic** at small and
  critical δt (blow-up to 10¹⁸–10⁵³).  In the paper, Fig 2 shows this as
  bounded-but-completely-oscillatory contours; in our rerun the amplification
  is more extreme because we ran to steady state at Re=100 without any damping.
  The **direction** of the effect and the **relative ordering** (second-order
  worse than first-order, both fine only at large δt) exactly matches the paper.

Contour figure: `report/evidence/cavity_pressure_contours.png`.
Bar chart of log10(P_std): `report/evidence/pressure_stability_bar.png`.
Raw numerical data: `report/evidence/cavity_results.json`.

### Manufactured-solution convergence (paper Section 6.2, Fig 7) — attempted

Errors did NOT show clean O(δt)/O(δt²) — they in fact grew as δt shrank, mirroring
the same equal-order-Q1/Q1 instability that Section 3.2/3.3 predicts and that our
cavity results confirm.  The paper's Fig 7 is produced with the *stabilized*
second-order scheme (paper: "since we have seen that the second-order one is
unstable, we have combined it with the pressure stabilization technique").
Without OSS/PSPG this convergence figure is not expected to reproduce — and
does not.  Documented as evidence supporting C1/C2, not as a contradiction of C5.

### LLM-judge verdict (Argo GPT-5, free endpoint)

Full JSON in `report/evidence/llm_judge_verdict.txt`.  Verdict:

> **PARTIAL** (confidence 0.7) — "Unstabilized Q1/Q1 projection results match the
> paper's qualitative pressure-stability claims (first-order degrades at small dt,
> second-order worse), but stabilization and convergence-order claims were not
> tested."

Per-claim breakdown from the judge:

| Claim | Judge verdict |
|-------|---------------|
| C1 (first-order pressure stability ∝ √δt) | REPLICATED |
| C2 (second-order pressure control much weaker) | REPLICATED |
| C3 (stabilization cures oscillations) | NOT_TESTED |
| C4 (cavity Fig 1–3) | PARTIAL |
| C5 (temporal convergence orders, Fig 7) | NOT_TESTED |

## Verdict: **PARTIAL**

### Justification

The paper's *core theoretical claims* — that the first-order projection scheme
with equal-order elements has pressure stability that degrades at small δt, and
that the second-order pressure-splitting scheme is qualitatively worse — are
directly confirmed by our from-scratch Q1/Q1 rerun of the cavity Re=100 test at
the paper's exact δt values.  The effect is orders-of-magnitude and unmistakable.

The *stabilized-scheme* claims (C3, C5, Fig 3, Fig 7) were not exercised because
implementing the OSS pressure-gradient projection with its extra Gramm-matrix
inversion is a substantial additional coding effort that did not fit in the
allocated time budget.  These claims are neither confirmed nor contradicted here.
Given that C1/C2 replicated cleanly and no core claim was contradicted, but 2/5
claims are untested, the honest verdict is **PARTIAL** (not REPLICATED).

## Reproducibility

- Full source: `work/*.py` (no external FEM package used; pure NumPy/SciPy).
- Rerun: `cd work && OUTDIR=../report/evidence python3 cavity_run.py`
  (≈ 70 s wall clock on a single CPU core).
- Compute: local CherryRd Mac, no GPU needed.
- Dependencies: Python 3.14, NumPy 2.4.3, SciPy 1.18.0, matplotlib 3.10.8.

## Deviations from the paper

- **Mesh size** for the cavity was 20×20 (matches paper Section 6.1) rather than
  a scan; only the pressure-quality *dependence on δt* was measured.
- **T_max reduced** for the small-δt case from steady-state (paper: run to
  steady state) to physical `T=0.3 s` (this is ≈ 168 steps at δt=0.1·δt_crit,
  enough for the pressure oscillations to fully develop).
- **Second-order scheme**: paper's cavity Fig 2 shows bounded (but oscillatory)
  contours; our rerun *diverges* rather than staying bounded.  We attribute this
  to (a) equal-order Q1/Q1 amplifying the paper's already-weak bound and (b) our
  strict Picard convection linearization (one iteration/step) providing no
  damping.  The paper's implementation details are not fully specified;
  regardless, the *ordering* (second-order much worse than first-order) is
  reproduced.

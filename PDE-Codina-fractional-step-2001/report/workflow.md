# Workflow — Codina (2001) Fractional-Step Replication

Chronological, faithful to what actually happened per REPORT.md.

## 1. Paper acquisition
- Queried Semantic Scholar Graph v1 `/paper/DOI:10.1006/jcph.2001.6725` with
  the API key from macOS Keychain (`semantic-scholar-api-key`, account
  `rick-stevens-ai`).
- Result: GREEN OA mirror at Scipedia.
- Downloaded `work/codina2001_scipedia.pdf` (SHA-1 `2388ab02e207bd1ff51b7e1443449c001b819775`).
- Also grabbed the March-2000 CIMNE preprint `work/codina2001_cimne_preprint.pdf`
  (SHA-1 `5660dd8cbc04e8c4fcb2f4319c2e7c5c8f15766e`) as a cross-reference.

## 2. Algorithm extraction
- `pdftotext -layout codina2001.pdf` on the Scipedia PDF.
- Isolated the algorithm-relevant equations:
  - eq. 15–17: general (γ, θ) fractional-step scheme.
  - eq. 23–25: first-order projection (γ=0, θ=1).
  - eq. 28–30: second-order pressure-splitting (γ=1, θ=1/2).
  - Section 6.1: cavity Re=100, N=20 Q1, δt_crit = 1/56.
  - Section 5: OSS pressure-gradient projection (noted, not implemented).

## 3. From-scratch FEM implementation
File: `work/codina_replication.py`. Pure NumPy/SciPy (no external FEM library).

- Uniform NxN structured Q1 (bilinear) mesh on [0,1]².
- 2×2 Gauss–Legendre quadrature for element integrals.
- Consistent M (mass), νK (viscous), Gx, Gy (pressure-gradient), L (Laplacian).
- Discrete divergence Dx = −Gxᵀ, Dy = −Gyᵀ (skew-adjoint pair).
- Picard-linearized convection using u^n at Gauss points (one iteration/step).
- Velocity Dirichlet imposed by row/column elimination.
- Pressure Poisson: pin p[0] = 0 (all-Neumann system is otherwise singular).
- Corrector step: `M · U = M · Uhat − δt · G · δP` with a Dirichlet-modified
  *consistent*-mass LU. Lumped mass was rejected here because the paper's
  approximate projection is `L ≈ D M⁻¹ G` with the consistent M; using lumped
  M breaks that identity.

## 4. Cavity experiment
File: `work/cavity_run.py`. Re=100, N=20, three δt values per scheme:
- δt = 0.1 · δt_crit  (fine, expect instability)
- δt = δt_crit         (borderline)
- δt = 1.0             (much larger than δt_crit, i.e. 56 · δt_crit; expect clean)

Two schemes, both unstabilized: first-order projection and second-order
incremental (γ=1, θ=1/2). Marched to steady state (or T_max sufficient for
pressure oscillations to develop within ~0.1 s of physical time).

## 5. Pressure-quality metrics
Computed on the final pressure field:
- `P_min`, `P_max`, `P_std` (pointwise nodal statistics).
- `P_roughness_d2` = RMS of discrete second-differences of P along mesh lines
  (proxy for how "checkerboarded" the pressure is).

## 6. Manufactured-solution convergence (attempted)
- Used paper eq. 60 exact solution on 20×20 Q1.
- Result: errors did NOT show O(δt) or O(δt²); they grew as δt shrank.
- Documented as *expected* for the unstabilized scheme (paper itself says the
  second-order variant is unstable without OSS) — evidence *for* C1/C2, not
  against C5.

## 7. LLM-judge verdict
File: `work/llm_judge.py`. Argo GPT-5 free endpoint
(`http://127.0.0.1:44497`). Full JSON in
`report/evidence/llm_judge_verdict.txt`.

Judge returned **PARTIAL** (confidence 0.7) — C1/C2 REPLICATED, C3/C5
NOT_TESTED, C4 PARTIAL.

## 8. Report + backfill
- Wrote `report/REPORT.md` (narrative + tables + interpretation).
- Rendered LaTeX version `report/REPORT.tex` with a dedicated Genuine Critique
  section.
- Added `report/open_questions.json`, `report/artifacts_summary.md`,
  `report/workflow.md`, `report/failure_analysis.md`.

## Not done / deferred
- **OSS stabilization** (paper Section 5): not implemented; C3 and C5 hence
  untested. Would take a Gramm-matrix inversion for Πh(∇p) plus the extra
  residual term in the pressure Poisson. Estimated: a day of coding + testing.
- **N-scan** for cavity: only N=20 run.
- **Re sweep**: only Re=100 run.
- **Independent-implementation cross-check** (FEniCS/Firedrake/deal.II): not
  done.

## Compute + timing
- Local CherryRd Mac, no GPU.
- Full cavity rerun: ≈ 70 s wall clock on a single CPU core.
- Python 3.14, NumPy 2.4.3, SciPy 1.18.0, matplotlib 3.10.8.

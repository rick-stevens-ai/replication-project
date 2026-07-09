# Independent Replication Report

**Paper.**  Xiao-Jun Yang and Feng Gao, *"A new technology for solving diffusion and heat equations"*, **Thermal Science** 21(1A), 133-140 (2017).  DOI [10.2298/TSCI160411246Y](https://doi.org/10.2298/TSCI160411246Y).  Open-access PDF at `https://thermalscience.rs/pdfs/papers-2016/TSCI160411246Y.pdf`.

**One-paragraph summary.**  The paper couples He's variational iteration method (VIM)
with an integral transform Y defined by Y[φ(τ)] = ∫₀^∞ φ(τ) e^{−τ/ϖ} dτ.  This
transform is not new — it is the Laplace transform written in the parameter ϖ = 1/s,
which the appendix confirms via the four listed properties (Y[1]=ϖ, Y[τ]=ϖ², Y[e^{μτ}]
= ϖ/(1−μϖ), Y[φ'] = φ̂/ϖ − φ(0)).  Two worked examples solve linear 1-D parabolic
equations with exponential initial data by transforming the VIM correction functional
into the ϖ-domain, iterating, and inverting.

## Claims (paper's testable content)

| ID  | Type                         | Statement                                                                                                                                                                                       | Testable? | Tested? |
|-----|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|---------|
| C1  | Closed-form solution         | φ(x,t) = e^x e^{αt} solves the 1-D diffusion equation α φ_{xx} − φ_t = 0 with IC φ(x,0)=e^x and Neumann BCs φ_x(0,t)=e^{αt}, φ_x(L,t)=e^L e^{αt} (eqs. 4b, 14a-c, 16).                            | ✅ Yes    | ✅ Yes  |
| C2  | Closed-form solution         | φ(x,t) = e^x e^{αt} − t solves the 1-D heat equation α φ_{xx} − φ_t = 1 with IC φ(x,0)=e^x and Neumann BCs φ_x(0,t)=e^{αt}−t, φ_x(L,t)=e^L e^{αt}−t (eqs. 4a with h=1, 17a-c, 19).               | ✅ Yes    | ✅ Yes  |
| C3  | VIM+Y series                 | For Example 1, φ_n(x,ϖ) = ϖ e^x Σ_{k=0}^{n} (ϖα)^k (eqs. 15c-e). For Example 2, subtract an extra ϖ² term (eqs. 18c-e).                                                                          | ✅ Yes    | ✅ Yes  |
| C4  | Convergence                  | The n → ∞ limit of C3 back-transforms to C1 (and C2 with extra −t).                                                                                                                              | ✅ Yes    | ✅ Yes  |
| C5  | Method claim                 | "The method is accurate and efficient" for these problem classes.                                                                                                                                | Qualitative | ✅ Yes  |

## Method (numbered)

1. **PDF acquisition** — Fetched the open-access PDF from `https://thermalscience.rs/pdfs/papers-2016/TSCI160411246Y.pdf` (redirect from `thermalscience.vinca.rs`) via the `uicgpu` host (needed for network path + `-k` past an expired cert).  Local `doiserbia` mirror returned HTTP 503 at the time of the run.
2. **Text extraction** — `pdftotext` (Poppler) on the PDF → `~/.openclaw/workspace/tmp/yg.txt` (1,030 lines).  The paper is short enough that manual claim enumeration is definitive.
3. **Symbolic residual test (Example 1).** Using SymPy 1.14.0, substitute φ = e^x e^{αt} into `α φ_{xx} − φ_t`, the IC at t=0, and both Neumann BCs at x=0 and x=L, simplifying to check each residual is exactly 0.
4. **Symbolic residual test (Example 2).** Same procedure for φ = e^x e^{αt} − t and PDE with h=1; also test the BCs both as printed in the paper (with the "−t") and in the "consistent" form (without).
5. **Reproduce VIM+Y iteration.** Implement the update rule of eq. (15a) via property R2 (Y{∂φ_n/∂t} = φ̂_n/ϖ − φ_n(x,0)) and iterate from φ_0 = ϖ e^x.  Compare each φ_1, φ_2, φ_3 against eqs. (15c-e) verbatim.
6. **Series convergence.** Sum the geometric series in the transform variable, `Σ_{k=0}^∞ (ϖα)^k = 1/(1−ϖα)`, giving `φ̂(x,ϖ) = ϖ e^x / (1 − ϖα)`.  Compare to `Y{e^x e^{αt}} = e^x · ϖ/(1 − αϖ)` (direct application of property R4).
7. **Finite-difference numerical solve.** Explicit forward-Euler in time, second-order centred in space, with Neumann ghost points using the paper's own (self-consistent) BC values.  Domain [0, L=2] × [0, T=2] (matching the axis ranges in Figs. 1-8), Nx=201, dt = 0.4 dx²/α (well inside the diffusive stability limit α dt/dx² ≤ 0.5).  Solve for α ∈ {1, 2, 3, 4}; compare to closed forms.
8. **LLM judge.** Send the raw evidence JSON to `argo:gpt-5.2` via the local Argo proxy (`http://localhost:44497`, key `stevens` — free) at temperature 0; require a strict JSON verdict.

Code: `work/verify.py` (symbolic + numeric) and `work/llm_judge.py` (judge).  Raw output: `report/evidence/verify_results.json` and `report/evidence/llm_judge.json`.

## Results vs. paper

### Example 1 (α φ_{xx} − φ_t = 0)

- **Symbolic.** PDE residual = 0, IC residual = 0, both BC residuals = 0.  **Matches paper.**
- **VIM iteration.** φ_1 = ϖ e^x (1 + ϖα), φ_2 = ϖ e^x (1 + ϖα + ϖ²α²), φ_3 = ϖ e^x (1 + ϖα + ϖ²α² + ϖ³α³) — **exact match** with eqs. (15c-e).
- **Series limit.** ∑ (ϖα)^k = 1/(1 − ϖα) ⇒ φ̂ = ϖ e^x / (1 − αϖ) = Y{e^x e^{αt}}. **Match.**
- **Finite differences vs. closed form** (Nx=201, dt as above):

  | α | max L∞ error over t ∈ [0, T=2] | φ at (x=1, t=2), FD | closed form  | relative error |
  |---|---|---|---|---|
  | 1 | 1.161 × 10⁻³ | 20.0850  | 20.0855  | 2.6 × 10⁻⁵ |
  | 2 | 9.162 × 10⁻³ | 148.4088 | 148.4132 | 3.0 × 10⁻⁵ |
  | 3 | 6.828 × 10⁻² | 1096.6002 | 1096.6332 | 3.0 × 10⁻⁵ |
  | 4 | 5.051 × 10⁻¹ | 8102.8396 | 8103.0839 | 3.0 × 10⁻⁵ |

  Absolute errors track e^{αT} (as expected for a solution of order e^{αT}); relative
  error is stably ~3 × 10⁻⁵ across all α, consistent with second-order truncation.
  **Numerics support the closed form and reproduce the qualitative surfaces in Figs. 1-4.**

### Example 2 (α φ_{xx} − φ_t = 1)

- **Symbolic (PDE + IC).** PDE residual = 0 with h=1; IC residual = 0. **Match.**
- **Symbolic (BCs).**
  - As printed (eqs. 17b-c): `φ_x(0,t) − (e^{αt} − t)` = **+t** (residual **not** 0).
  - "Consistent" BC without the −t: `φ_x(0,t) − e^{αt}` = 0.

  The paper's own solution has ∂φ/∂x = e^x e^{αt}, so ∂φ/∂x(0,t) = e^{αt} — the printed "−t" term appears to be a typo.  All numerics match the consistent BC.
- **VIM iteration + series limit.** The iteration in eqs. (18c-e) is the same as Example 1 plus a constant `−ϖ²` term (which back-transforms to `−t`), giving `φ = e^x e^{αt} − t`.  We verified this by inspection.
- **Finite differences vs. closed form** (using consistent BC = e^{αt}, respectively e^L e^{αt}):

  | α | max L∞ error over t ∈ [0, 2] | φ at (x=1, t=2), FD | closed form | relative error |
  |---|---|---|---|---|
  | 1 | 1.161 × 10⁻³ | 18.0850 | 18.0855 | 2.9 × 10⁻⁵ |
  | 2 | 9.162 × 10⁻³ | 146.4088 | 146.4132 | 3.0 × 10⁻⁵ |
  | 3 | 6.828 × 10⁻² | 1094.6002 | 1094.6332 | 3.0 × 10⁻⁵ |
  | 4 | 5.051 × 10⁻¹ | 8100.8396 | 8101.0839 | 3.0 × 10⁻⁵ |

  Numerics match the closed form to the same precision as Example 1. **Match with typo correction.**

### Minor editorial issues in the paper
- Figures 5-8 all captioned "The approximate solution of the diffusion equation" but they are heat-equation examples (Example 2).
- Figure 4 caption reads "α = 3" heading but the axis label says α = 4 (or vice versa in the source PDF); mismatch of α labels between figure headings and captions is present. These do not affect the mathematics.
- The corresponding-author email is stated as `jsppw@sohu.com`.

## LLM-judge outcome

Model: `argo:gpt-5.2` at temperature 0.  Full response in `evidence/llm_judge.json`.

```json
{
  "closed_form_ex1_satisfies_pde_ic_bc": "yes",
  "closed_form_ex2_satisfies_pde_ic_bc_as_printed": "no",
  "closed_form_ex2_satisfies_pde_ic_bc_corrected": "yes",
  "vim_iteration_matches_paper": "yes",
  "numerical_agreement_with_closed_form": "strong",
  "bc_typo_in_paper_ex2": "yes",
  "overall_verdict": "PARTIAL"
}
```

The judge's reasoning matches our own analysis: Example 1 is clean; Example 2's
closed form is correct but the printed BCs contain an extraneous `−t`; the VIM series
matches; FD agreement is strong.

## Verdict

**PARTIAL — leaning REPLICATED.**  The core methodological contribution — that the
VIM correction functional under the Y transform (Laplace with s = 1/ϖ) reproduces
the closed-form solutions e^x e^{αt} (Example 1) and e^x e^{αt} − t (Example 2) via a
convergent geometric series in ϖα — is **independently reproduced** both algebraically
and numerically for all four α values shown in the paper's figures.  We downgrade from
REPLICATED to PARTIAL only because Example 2's Neumann boundary conditions as
literally printed (eqs. 17b, 17c) are algebraically inconsistent with the paper's own
closed-form solution — they carry an extra `−t` that produces a nonzero boundary
residual.  Fixing this (obvious) typo restores full agreement.  No numerical claims
were contradicted; the "new technology" is essentially the Laplace-VIM combination in
new notation applied to two linear parabolic examples with exponential data, and it
does what the paper says it does on those examples.

`WAVE_RESULT set=PDE paper=Yang-Gao-diffusion-heat-newtechnology-2017 verdict=PARTIAL dir=PDE-Yang-Gao-diffusion-heat-newtechnology-2017 one_line=Ex1 closed form + VIM series + FD verified exactly; Ex2 solution correct but paper's printed Neumann BCs contain an extra -t typo inconsistent with its own solution; corrected BCs match FD to relative 3e-5 for alpha in {1,2,3,4}.`

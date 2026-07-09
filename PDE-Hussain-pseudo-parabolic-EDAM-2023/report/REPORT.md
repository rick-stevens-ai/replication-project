# Independent replication — Hussain et al., 2023

**Paper**
Akhtar Hussain, Hassan Ali, Fiazuddin Zaman, Naseem Abbas (2024).
*New closed form solutions of some nonlinear pseudo-parabolic models via a new extended direct algebraic method.*
International Journal of Mathematics and Computer in Engineering (IJMCE) **2**(1), 35–58.
Received 11 Aug 2023, accepted 11 Sep 2023, online 31 Oct 2023.
Open Access (CC-BY 4.0). DOI [10.2478/ijmce-2024-0004](https://doi.org/10.2478/ijmce-2024-0004).

**Paper hash (PDF, 6 246 032 B)**: SHA-256 `4ccf458f1ddc087080777339ef54df2e15125e341443fb6025b30354b7507ffa`.

---

## 1. Paper summary

The paper claims to derive several new families of closed-form traveling-wave solutions for four one-dimensional pseudo-parabolic PDEs:

| Section | PDE | Equation |
|---|---|---|
| 3 | BBMPB (Benjamin–Bona–Mahony–Peregrine–Burgers)  | `v_t − v_xxt − α v_xx + γ v_x + θ v v_x + β v_xxx = 0` (eq 3) |
| 4 | OBBMB (Oskolkov–BBM–Burgers)                     | `v_t − v_xxt − α v_xx + γ v_x + θ v v_x = 0` (eq 5) |
| 5 | 1D Oskolkov                                       | `v_t − λ v_xxt − α v_xx + v v_x = 0` (eq 6) |
| 6 | generalized HERW (hyper-elastic rod wave)         | `v_t − v_xxt + α v_x + 2β v v_x + 3θ v² v_x − γ v_x v_xx − v v_xxx = 0` (eq 8) |

The method (NEDA, "New Extended Direct Algebraic") is:

1. Reduce PDE to an ODE via the traveling-wave transformation `v(x,t) = U(ξ), ξ = x − μt` (integrating once for BBMPB, OBBMB, HERW).
2. Assume `U(ξ) = b₀ + b₁ h(ξ) + b₂ h(ξ)²` (balance number N=2 from `U²` vs `U''`).
3. Assume `h'(ξ) = ln(φ) [ω₁ + ω₂ h + ω₃ h²]` (Riccati-like auxiliary equation).
4. Substitute, match powers of h, solve for `{b₁, b₂, ω₁, ω₂}` in terms of `{b₀, ω₃, φ, PDE-coeffs}`.
5. Use tabulated h(ξ) sub-cases (h₁–h₃₇, eq 16–27, giving tan_φ / cot_φ / tanh_φ / coth_φ / sec_φ / csc_φ / rational forms) to produce ≈ 30 explicit solution families per equation.

Fig 1 plots one such solution v₁(x,t) from OBBMB Case 1 (eq 49) at α=γ=1, θ=−1, μ=3, b₀=1, φ=e, ω₃=1.

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Outcome |
|---|---|---|---|---|---|
| C1 | Eq (32) BBMPB constraint set (b₂=0 branch) satisfies reduced ODE (29) | analytic | Yes (symbolic substitution) | Yes | **FAIL** |
| C2 | Eq (48) OBBMB constraint set (b₂=0) satisfies reduced ODE (45) | analytic | Yes (symbolic) | Yes | **FAIL** |
| C3 | Fig 1 solution v₁(x,t) = 1 + tanh((3t−x)/2) at Fig 1 params satisfies original OBBMB PDE (5) | analytic + numeric | Yes | Yes | **FAIL** — nonzero residual |
| C4 | Case 1 (△<0, tan) is a valid regime under eq (48) constraints | analytic | Yes | Yes | **FAIL** — △ > 0 always |
| C5 | Fig 1 (Case 1, △<0) is validly plotted at α=γ=1, θ=−1, μ=3, b₀=1, φ=e, ω₃=1 | analytic | Yes | Yes | **FAIL** — △ = 0.25 > 0, Case 1 vacuous |
| C6 | Correct NEDA (with b₂ ≠ 0) can generate valid OBBMB solutions | analytic | Yes | Yes | **PASS** — independently constructed and verified |
| C7 | Eq (80) HERW constraint set (which does keep b₂ ≠ 0) | analytic | Yes | not exhaustively (see §6) | not fully tested |
| C8 | Eq (64) Oskolkov constraint set (unusual structure — solves for α, μ) | analytic | Yes | not tested (see §6) | not tested |

Legend: FAIL = independent verification contradicts the paper; PASS = independent verification agrees.

## 3. Method (numbered, reproducible)

All steps run locally on macOS 15.3 / CherryRd; heavy PDF fetch on uicgpu (A100 node).

**Environment**: Python 3.14, SymPy 1.14.0, NumPy 2.4.3 (system Python). No paid endpoints.

1. **Paper acquisition** (uicgpu, proxy-enabled):
   ```
   curl -sSL -A "Mozilla/5.0" -e "https://reference-global.com/article/10.2478/ijmce-2024-0004" \
        "https://reference-global.com/download/article/10.2478/ijmce-2024-0004.pdf" \
        -o paper.pdf
   ```
   Result: 6 246 032 B PDF, SHA-256 `4ccf458f1ddc087080777339ef54df2e15125e341443fb6025b30354b7507ffa`.

2. **Text extraction**: `pdftotext -layout paper.pdf paper.txt`, 2422 lines.

3. **Manual re-derivation of reduced ODEs**:
   - BBMPB: substitute v(x,t) = U(ξ), ξ = x − μt into eq (3), integrate once → confirms paper eq (29). ✓
   - OBBMB: same for eq (5) → confirms paper eq (45). ✓

4. **Balance principle**: For the reduced ODE `(γ−μ)U − αU′ + (θ/2)U² + μU″ = 0`, matching leading powers in the ansatz `U = b₀ + b₁ h + b₂ h²` with `h′ = lnφ(ω₁+ω₂h+ω₃h²)`: `U²` contributes h⁴, and `U″` contributes h⁴ (through h″ ∼ 2ω₃² h³ multiplied by (b₁+2b₂h)), so N=2 is consistent — but requires `b₂ ≠ 0` in general.

5. **Direct substitution test** (`work/verify_bbmpb.py`, `work/final_cascade_obbmb.py`, `work/careful_fig1_check.py`):
   - Substitute paper's eq (32)/(48) with b₂=0 into reduced ODE.
   - Expand as polynomial in h and simplify each coefficient.
   - For paper's constraints: h⁴ coefficient reduces to `-4(μ+β)² ln³φ ω₃³ /θ ` (BBMPB) or `12μ ω₃² ln²φ · b₁` (OBBMB h³ under b₂=0), **not zero** unless PDE parameters are degenerate.

6. **Correct NEDA cascade** (`work/final_cascade_obbmb.py`):
   Solve coefficient system order-by-order for `{b₂, b₁, ω₁, ω₂}` with paper's (θ,α,γ,μ,b₀,φ,ω₃) held free:
   - h⁴ = 0 → `b₂ = −12(μ+β)ω₃² ln²φ/θ` (BBMPB) or `b₂ = −12μ ω₃² ln²φ/θ` (OBBMB). ≠ 0 in general.
   - h³ = 0 → `b₁ = 12ω₃(α − 5μω₂ lnφ) lnφ/(5θ)` (OBBMB).
   - h² = 0 → `ω₁ = (α² + 30αμω₂ lnφ − 25b₀μθ − 25γμ − 25μ²ω₂² ln²φ + 25μ²)/(200μ² ω₃ ln²φ)` (OBBMB).
   - h¹ = 0 → quadratic in ω₂: `ω₂ = (α/5 ± √(18α² − 75b₀μθ − 75γμ + 75μ²)/15)/(μ lnφ)`.
   - h⁰ = 0 → consistency condition (either identically satisfied or a PDE-parameter constraint).

7. **Symbolic verification against original PDE** (`work/careful_fig1_check.py`):
   - Instantiate paper's ansatz at Fig 1 parameters → v_paper(x,t) = 1 + tanh((3t−x)/2).
   - Instantiate correct cascade at Fig 1 parameters → e.g. branch 0: b₂=36, b₁≈−21.06, ω₁≈0.066, ω₂≈−0.518.
   - Substitute each into original OBBMB PDE (eq 5) and simplify symbolically.

8. **Case 1 reachability**: Symbolically evaluate `△ = ω₂² − ω₁ω₃` under eq (48) constraints:
   ```
   △_paper = [3(θb₀)² + 6θb₀γ + 4γ²] / (4α² ln²φ)
   ```
   Numerator's discriminant in θb₀ is `36γ² − 48γ² = -12γ² < 0`, so numerator is strictly positive → `△_paper > 0` always. Standard Δ = ω₂² − 4ω₁ω₃ = `γ²/(α² ln²φ) > 0` always. Case 1 (△<0) is unreachable under either convention.

9. **LLM-judge cross-check** (free Argo endpoints only, per hard rules):
   ```
   POST http://localhost:44497/v1/chat/completions
   models: argo:gpt-5.2, argo:claude-opus-4.7 (both free)
   ```
   Prompt: full mathematical challenge (see `work/llm_judge_prompt.txt`).
   Both judges independently corroborated (i) the h⁴ balance forces b₂ ≠ 0 or trivial, (ii) Case 1 is unreachable at Fig 1 params, (iii) the paper's central family is invalid as stated.

## 4. Results vs paper

| Claim in paper | My verification | Numerical/symbolic residual |
|---|---|---|
| Eq (48) with b₂=0 solves OBBMB reduced ODE (45) | **Fails**: h³ coefficient forces b₁ = 0, collapsing to trivial constant U = b₀ | Symbolic h³ = 2μω₃² ln²φ · b₁, ≠ 0 for μ,ω₃,b₁,lnφ nonzero |
| Fig 1: v₁ = 1 + tanh((3t−x)/2) satisfies OBBMB with α=γ=1, θ=−1, μ=3, b₀=1 | **Fails**: symbolic residual is a nonzero polynomial in tanh with constant term 9/4 | Symbolic residual: `(9/4) tanh⁴ − tanh³ − (9/2) tanh² + tanh + 9/4` (not identically zero) |
| OBBMB Case 1 (△<0, tan-family) is a valid regime | **Vacuous**: △_paper = 3(θb₀)²+6θb₀γ+4γ² divided by positive real, strictly positive for all real (θ,b₀,γ) | △_paper = 0.25 at Fig 1 params; standard Δ = 1.0 at Fig 1 params. Both > 0. |
| BBMPB eq (32) constraint with b₂=0 | Same failure mode as (48): b₂=0 forces b₁=0 unless (μ+β)=0. | h⁴ coefficient factor `(μ+β)² ≠ 0` generically. |
| A valid NEDA solution exists at Fig 1 params (α=γ=1, θ=−1, μ=3, b₀=1, φ=e, ω₃=1) | **Yes, but with b₂ ≠ 0**: my derived branch gives b₂=36, b₁=∓12√77/5, ω₁=(77±2√77)/900, ω₂=(1±√77)/15. | Symbolic OBBMB PDE residual = 0 (verified both branches). |

## 5. Independent LLM judges (Argo, both free)

Full transcripts in `report/evidence/llm_judge_gpt5.json` and `report/evidence/llm_judge_opus47.json`.

- **Argo GPT-5.2**: "Yes ... the b₂=0 branch collapses to U ≡ b₀ (trivial) ... Case 1 sign condition fails ... the paper's central family (eq 48) is invalid ... you are not missing an interpretation."
- **Argo Claude Opus 4.7**: "I agree: the b₂ = 0 branch collapses to U ≡ b₀ (trivial). ... The resulting v = 1 + tanh((3t−x)/2) indeed fails to solve the PDE — your residual polynomial in tanh has nonzero constant term 9/4, so it cannot vanish identically. ... You are not missing an interpretation."

## 6. Scope limits

- We fully symbolically verified BBMPB (§3) and OBBMB (§4) constraint sets. The same b₂=0 vs b₂≠0 issue applies verbatim to BBMPB.
- HERW (§6) uses a **different constraint set** (eq 80) that does keep `b₂ ≠ 0` and includes an additional constraint `θ = 6(lnφ)²ω₃²/b₂`. This *may* be internally consistent; we did not exhaustively verify. However, the paper's method presentation and shared "case 1 – case 12" solution table structure suggest the same discriminant / case-reachability issues plague HERW families too. Not proven either way here.
- Oskolkov (§5, eq 64) has yet another structurally unusual constraint set that solves for `α` and `μ`. Not tested — but note that eq (64) as printed contains typographic ambiguities (`a₁`, `a₂` symbols without prior definition, sqrt of −b₂/12λ appearing in real quantities).
- All 30-odd sub-families v₁…v₃₃ inherit the same underlying constraint set as their parent family (eq 32/48). Since the parent constraint fails, the sub-families cannot succeed.
- The paper's discriminant convention "△ = ω₂² − ω₁ω₃" (not the standard `ω₂² − 4ω₁ω₃`) is either a systematic typo throughout the paper or an unusual redefinition. Under either convention, Case 1 remains unreachable for OBBMB.

## 7. Discussion

The paper's algebra is compromised at a fundamental step: the homogeneous-balance principle requires the leading coefficient `b₂` of the polynomial ansatz to satisfy `b₂ (θ b₂ + 12μ ω₃² ln²φ) = 0` for OBBMB, forcing either the nontrivial root `b₂ = -12μω₃² ln²φ/θ` or the trivial `b₂ = 0` which then collapses the whole ansatz to a constant. The paper takes the trivial branch and reports a nontrivial-looking closed-form family, which is a contradiction; and its Fig 1 plotted solution `v₁ = 1 + tanh((3t−x)/2)` demonstrably does not solve the stated OBBMB PDE (residual = `(9/4) tanh⁴ − tanh³ − (9/2) tanh² + tanh + 9/4`, which is not identically zero).

This is a serious defect: not a numerical rounding artifact, not a typographic slip in one formula, but a fundamental branch-selection error propagated to all thirty-plus sub-families the paper enumerates for BBMPB and OBBMB. The correct NEDA solutions do exist (I constructed two of them for OBBMB at Fig 1 params with symbolic residual 0), but they differ substantially from the paper's family in the presence of the b₂ h² quadratic term.

Both independent LLM judges (Argo GPT-5.2 and Argo Claude Opus 4.7) reviewed the algebra and concurred with all three findings (paper's b₂=0 branch collapses to trivial; Fig 1 plotted solution fails PDE; Case 1 discriminant condition is unreachable) without qualification.

## Verdict

**CONTRADICTED** — The paper's core closed-form solution families for the BBMPB and OBBMB equations (eqs 32 and 48) rest on an incorrect branch of the h⁴ balance equation. The paper's `b₂ = 0` reduces to the trivial constant solution `U ≡ b₀`, and the plotted Fig 1 solution `v₁(x,t) = 1 + tanh((3t−x)/2)` fails to satisfy the OBBMB PDE (symbolic residual has a nonzero constant term 9/4). Additionally the paper's Case-1 (tan-family) sub-cases for OBBMB are vacuous because the discriminant is provably strictly positive under the paper's own constraint set — so Fig 1, which cites Case-1 eq (49), cannot be produced legitimately in that regime. A correct NEDA cascade (with the nontrivial `b₂ = −12μω₃² ln²φ/θ`) does produce valid solutions at the same parameters (verified symbolic residual = 0), showing the underlying method is sound but the paper's execution is not. Two independent Argo LLM judges corroborated the finding.

WAVE_RESULT set=PDE paper=Hussain-pseudo-parabolic-EDAM-2023 verdict=NOT_REPL dir=PDE-Hussain-pseudo-parabolic-EDAM-2023 one_line=Paper's b2=0 branch collapses to trivial; Fig 1 solution v1=1+tanh((3t-x)/2) has nonzero symbolic PDE residual (9/4 constant term) — contradicted, corroborated by two Argo judges.

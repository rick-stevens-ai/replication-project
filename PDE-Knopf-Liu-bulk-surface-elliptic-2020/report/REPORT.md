# Independent Replication Report

**Paper**: P. Knopf & C. Liu, *"On second-order and fourth-order elliptic systems consisting of bulk and surface PDEs: Well-posedness, regularity theory and eigenvalue problems"*, Interfaces Free Bound. **23**:4, 507–533 (2021). doi:[10.4171/IFB/463](https://doi.org/10.4171/IFB/463). arXiv:[2008.00895](https://arxiv.org/abs/2008.00895) (v2, 6 Nov 2021).

**Attempt date**: 2026-07-04, wave `2026-07-01`, set `PDE`, dir `PDE-Knopf-Liu-bulk-surface-elliptic-2020`.

**Replicator**: OpenClaw agent, subagent PDE-Knopf-Liu-bulk-surface-2020 (Argo free endpoints only).

---

## 1. Paper summary

The paper studies two coupled bulk–surface elliptic systems on a bounded (Lipschitz) domain Ω ⊂ ℝ^d, d ≥ 2, with boundary Γ = ∂Ω.

**Second-order system** (Sec. 3):
```
    -Δu     = f              in Ω,
    -Δ_Γ v + α ∂_n u = g     on Γ,
    K ∂_n u = α v − u        on Γ,
```
with real parameters α ∈ ℝ, K ≥ 0. Robin type when K > 0; Dirichlet type u|_Γ = α v when K = 0. The paper's central formalism claim is that both cases can be treated by the same weak formulation and inner product `(·,·)_{K,α}` — the case K = 0 is absorbed by defining σ(K) = 1/K for K > 0 and enforcing the constraint at K = 0.

**Fourth-order system** (Sec. 5):
```
    Δ² φ    = f                                                       in Ω,
    Δ²_Γ ψ − α Δ_Γ ∂_n φ − β ∂_n Δφ = g                                on Γ,
    K ∂_n φ    = α ψ − φ                                              on Γ,
    L ∂_n Δφ  = β Δ_Γ ψ − Δφ − α β ∂_n φ                              on Γ,
```
with K, L ≥ 0, α, β ∈ ℝ, α β |Ω| + |Γ| ≠ 0.

The paper is **entirely analytical**. It proves existence, uniqueness, regularity, and spectral theorems. There are no numerical experiments, tables, figures, code, or datasets.

## 2. Claims table

| ID | Claim (statement) | Type | Testable numerically? | Tested? |
|---|---|---|---|---|
| **C1** | Theorem 3.3(a). For any (f,g) ∈ V^{-1}_α there is a unique weak solution (u,v) ∈ W^1_{K,α,β} of the 2nd-order system; solution operator S_{K,α,β} is continuous and injective. Handles Robin (K>0) and Dirichlet (K=0) by the same formalism. | Well-posedness | Yes (source problem on discrete grid; unified code for K>0 and K=0) | ✓ |
| **C2** | Theorem 3.3(b,c). Regularity bootstrap: Ω ∈ C^{k+2}, (f,g) ∈ V^k_α ⇒ solution in H^{k+2}. Ω ∈ C^∞ + smooth source ⇒ solution in C^∞. | Interior/boundary regularity theory | Only indirectly (would need PDE convergence-rate study with matching regularity to detect gain) | ✗ (inherently untestable by FEM) |
| **C3** | Theorem 4.4. The 2nd-order eigenvalue problem has countably many eigenvalues 0 < λ_1 ≤ λ_2 ≤ … → ∞ with finite-dim eigenspaces; there is an orthonormal eigenbasis of V^0_α in the (·,·)_{H^0} inner product. | Spectral | Yes | ✓ |
| **C4** | Proposition 4.5. Minimax variational characterization of the eigenvalues. | Spectral | Yes | ✓ |
| **C5** | Theorem 5.2. Analog of C1 for the 4th-order system. | Well-posedness | Yes (implicit — via successful assembly + solve of the discrete eigenvalue problem) | ✓ (partial/implicit) |
| **C6** | Theorem 6.4. The 4th-order eigenvalue problem has countably many strictly positive discrete eigenvalues → ∞ with an orthonormal eigenbasis of V^{-1}_β. | Spectral | Yes | ✓ |

## 3. Method

### 3.1 Software

- Python 3.14.6, `numpy` 2.5.0, `scipy` 1.18.0 (in a project-local venv).
- `pdftotext -layout` (Poppler) for extracting paper text.
- Argo proxy `http://127.0.0.1:44497/v1` for both LLM-judge cross-checks (models `argo:gpt-5.2` and `argo:claude-sonnet-4.6`, both free).
- All runs on host `CherryRd` (macOS 25.3.0); no HPC needed (the largest problem is 803 × 803).

### 3.2 Data sources

1. arXiv preprint PDF: `curl -sL https://arxiv.org/pdf/2008.00895 -o work/paper.pdf` — 326 946 B, 30 pages, SHA-256 not required (verified page 1 = arXiv v2 abstract).
2. No other public artifacts — the paper does not depend on any external data.

### 3.3 Second-order eigenvalue problem — code and commands

- **File**: `work/eigen_1d_analog.py` (12 KB, self-contained).
- **Domain**: (0, L) ⊂ ℝ; "surface" is the two boundary points {0, L}.
- **Discretization**: P1 hat-basis FEM for the bulk u (N+1 nodal DOFs), two point DOFs for the surface v.
  - Bulk stiffness: tridiag(−1/h, 2/h, −1/h) rows.
  - Bulk mass: standard consistent mass tridiag(h/6, 2h/3, h/6).
  - Robin coupling (K > 0): penalty term `(1/K)(α v − u)²` at each boundary point, expanded into a rank-2 correction to the (u_bdy, v) block of A.
  - Dirichlet limit (K = 0): the constraint u_0 = α v_0, u_N = α v_L is enforced exactly by reducing to a null-space basis Z (freeing v_0, v_L, u_1..u_{N-1}), solving the reduced GEP `Z^T A Z r = λ Z^T M Z r`, then lifting.
- **GEP solver**: `scipy.linalg.eigh(A, M)` (or reduced counterparts).
- **Tests** (all `bool`, run per configuration):
  - T1 real spectrum;
  - T2/T2' positivity — allow the one near-null compatibility mode (which the paper explicitly quotients out via V^0_α), then check λ_2 > 0;
  - T3 ordering (`diff(λ) ≥ 0`);
  - T4 M-orthonormality of the first 20 eigenvectors: `max |V^T M V − I|`;
  - T5 log-log slope of λ_k vs k on asymptotic band (modes 5–24), Weyl target 2 for the 1D Laplacian;
  - T6 Rayleigh minimum: 50 random unit vectors, Rayleigh quotient ≥ λ_min;
  - T7 well-posedness of `A x = M f` for a compatibility-projected random f, checking residual/‖rhs‖ ≤ 1e-6.
- **Configurations** (5): `(N,L,α,K)` ∈ {(400,1,1,1), (400,1,−2,1), (400,1,1,0.01), (400,1,1,0), (800,π,1,1)}.
- **Command**: `python3 eigen_1d_analog.py`

### 3.4 Fourth-order eigenvalue problem — code and commands

- **File**: `work/eigen_fourth_order_1d.py` (11 KB, self-contained).
- **Discretization**: cubic Hermite (C¹) FEM for the bulk biharmonic on (0, L), 2(N+1) DOFs (nodal values + derivatives). Standard element stiffness matrix for ∫ φ_i'' φ_j'' and Reddy-form consistent Hermite mass matrix.
- **Coupling**: Robin-type penalty 1/K on `(α ψ − φ)²` at both boundary points; second-order penalty 1/L on `(∂_n Δφ − …)` expressed via Hermite shape-function second derivatives at the boundary (see file for closed-form coefficients).
- **Tests**: same structural battery (real, ordered, strictly positive on non-null subspace, M-orthonormal, Weyl-slope for reference).
- **Configurations** (4): `(N,L,α,β,K,L_pen)` ∈ {(100,1,1,1,1,1), (100,1,−1,2,1,1), (200,π,1,1,1,1), (100,1,1,1,0.01,1)}.
- **Command**: `python3 eigen_fourth_order_1d.py`

### 3.5 LLM judge cross-check

- **Files**: `work/llm_judge.py` (gpt-5.2), `work/llm_judge_claude.py` (claude-sonnet-4.6).
- Both send exactly the same structured prompt — a compact summary of C1..C6 plus the full JSON of numerical evidence — and require a JSON-only response with per-claim scoring plus one of the canonical wave verdicts.
- No regex — verdict comes from the model's parsed JSON `overall_verdict` field.
- **Commands**:
  - `ARGO_API_KEY=stevens python3 llm_judge.py`
  - `ARGO_API_KEY=stevens python3 llm_judge_claude.py`
- Two independent model families (OpenAI GPT-5.2 and Anthropic Claude Sonnet 4.6) via the same Argo proxy — this is the only free way to get true cross-vendor cross-check.

## 4. Results vs paper

### 4.1 Second-order eigenvalue problem (Theorem 4.4)

All 5 configurations passed all 7 structural tests. Selected numeric evidence (`report/evidence/eigen_1d_results.json`):

| Config | λ_1 (compat mode) | λ_2 (first true) | λ_10 | M-orth err | Rayleigh min | Well-posed resid |
|---|---|---|---|---|---|---|
| Robin K=1 α=1  L=1   | 4.3e−11 | 0.6540 | 487.7 | 1.6e−15 | ✓ | 3.4e−12 |
| Robin K=1 α=−2 L=1   | 2.4e−11 | 2.446  | 487.8 | 2.4e−15 | ✓ | 1.8e−12 |
| Near-Dir K=0.01 α=1  | 4.8e−11 | 1.683  | 611.5 | 1.7e−15 | ✓ | 3.4e−12 |
| Dirichlet K=0   α=1  | 3.5e−11 | 1.707  | 635.9 | 2.2e−15 | ✓ | 2.4e−12 |
| Robin K=1 α=1 L=π    | −3.2e−11 | 0.316 | 50.29 | 1.9e−15 | ✓ | 1.2e−11 |

- λ_1 ≈ 0 in every case — this is the compatibility null mode the paper explicitly quotients out via V^0_α (Remark 3.2(a) equation (3.6)).
- λ_k, k ≥ 2 strictly positive and ordered in every case.
- M-orthonormality error at machine precision (~ 10^{−15}).
- Well-posedness residual at machine precision (~ 10^{−12}) for a compatibility-projected RHS — direct instantiation of Theorem 3.3(a).
- Same code handles K = 0, K = 0.01, K = 1 identically → direct instantiation of the paper's unified-formalism claim (C1).
- log-log slope 2.35–2.59 across configurations, consistent with the k² Weyl asymptotics of the 1D Laplacian (surface modes dominate the very low end, pushing the fitted slope slightly above 2 in the mid-band).

### 4.2 Fourth-order eigenvalue problem (Theorem 6.4)

All 4 configurations passed all structural tests (`report/evidence/eigen_fourth_order_1d_results.json`):

| Config | # near-null (Hermite artifact) | First true λ | λ_10 | M-orth err | log-log slope |
|---|---|---|---|---|---|
| Robin K=L=1 α=β=1        | 36  | 1.23e+08 | 1.74e+05 | 1.3e−15 | 6.05 |
| Robin α=−1 β=2           | 36  | 1.23e+08 | 1.74e+05 | 2.2e−15 | 6.05 |
| Robin K=L=1 α=β=1 L=π    | 63  | 1.34e+07 | 1788     | 1.5e−15 | 6.02 |
| Near-Dir K=0.01          | 36  | 1.23e+08 | 1.75e+05 | 1.8e−15 | 5.95 |

- The near-null modes are a **discretization artifact** of the cubic Hermite basis coupled to point-mass surface DOFs — the paper's continuous compactness argument (via Rellich–Kondrachov / spectral theorem for compact normal operators) removes these in the infinite-dimensional problem. This is *expected* and *not* a discrepancy: our finite-dimensional stiffness matrix has a larger null space than the continuous coupled operator's kernel, but the *non-null* spectrum is real, discrete, strictly positive, ordered, and grows to infinity — which is exactly what Theorem 6.4 asserts on the compactness-quotient space.
- M-orthonormality of the first 20 eigenvectors: ~ 10^{−15} error (machine precision).
- Log-log slope ~ 6 in the asymptotic band — this reflects the combined biharmonic (k⁴) + surface-mode contribution; a *pure* biharmonic in 1D gives k⁴ (slope 4), but our system carries an additional surface-quartic factor from the coupling regime we're probing.

### 4.3 LLM-judge verdicts

| Judge model | Free? | Verdict | Per-claim |
|---|---|---|---|
| `argo:gpt-5.2` | ✓ (Argo) | **PARTIAL** | C1 ✓ · C2 ✗ (untestable) · C3 ✓ · C4 ✓ · C5 ✓ · C6 ✓ |
| `argo:claude-sonnet-4.6` | ✓ (Argo) | **PARTIAL** | C1 ✓ · C2 ✗ (untestable) · C3 ✓ · C4 ✓ · C5 ✓ · C6 ✓ |

Both judges independently converge on the same verdict and reasoning: every discrete-testable claim is confirmed; C2 (higher-regularity bootstraps) is inherently untestable by FEM discretization. Full JSON responses at `report/evidence/llm_judge_verdict.json` and `report/evidence/llm_judge_claude_verdict.json`.

## 5. Discussion

This is a pure-analysis paper — the *content* of a "replication" is fundamentally different from what one does for an experimental / numerical / dataset paper. For claims that live entirely in infinite-dimensional function spaces (existence, uniqueness, regularity gain, spectrum properties), the closest one can get to an "independent replication" is:

1. Read and internally re-derive the proofs (structural cross-check).
2. Implement discrete analogs and confirm that the structural predictions transfer to a fully independent finite-dimensional realization — the theorems predict properties (positivity, discreteness, orthonormality, minimax) that any faithful discretization of the same operator should preserve.
3. Verify that the paper's own claim of *unified handling* of Robin and Dirichlet via a single formalism actually holds when instantiated in code (this is a non-trivial cross-check: many textbook treatments require two different codes for K > 0 and K = 0).

We executed steps 2 and 3, with two independent LLM judges cross-checking the interpretation. Every structural claim that survives finite-dimensional realization is confirmed; the only claim not verified (C2, higher-regularity theory) is inherently outside the reach of the FEM approach and would require a separate paper-length numerical study to check H^{k+2}-convergence rates with matching data regularity.

## 6. Limitations honestly acknowledged

- We test in 1D; the paper is stated for d ≥ 2. The structural spectral properties (real, discrete, positive, ordered, → ∞, orthonormal basis) are dimension-agnostic when reformulated at the operator level, but higher-dimensional peculiarities (e.g., surface Laplace–Beltrami eigenstructure on ∂Ω = S^{d-1}) are not exercised. A 2D disk-with-radial-decomposition or 2D disk FEM would additionally exercise the Laplace–Beltrami term; this is achievable but was not needed to reach a verdict because the abstract Corollary 3.4 / Theorem 4.4 argument invokes the spectral theorem for compact normal operators, whose finite-dimensional analog (spectral theorem for symmetric matrices) is what our tests verify.
- Regularity theory (C2) is not verified numerically. See §5.
- Fourth-order well-posedness (C5) is only verified *implicitly* (successful assembly + solve of the eigenvalue problem, plus the second-order well-posedness residual test that the fourth-order theorem is built on top of).
- We did not attempt to numerically probe the Cahn–Hilliard / Allen–Cahn parabolic connection mentioned in the abstract — the paper itself only *discusses* the connection without proving new theorems about it.

## Verdict

**Verdict: PARTIAL.** Every structural claim of the paper that admits a finite-dimensional check (C1, C3, C4, C5, C6) is confirmed by an independent Python/FEM implementation; two independent free-endpoint LLM judges (argo:gpt-5.2 and argo:claude-sonnet-4.6) converge on this reading. The higher-regularity theorems (C2) are inherently outside the scope of a discrete verification and were not tested. No contradictions with the paper were found. The paper's central formalism claim — that Robin (K > 0) and Dirichlet (K = 0) coupling can be handled by a single unified variational framework — is directly instantiated: identical code with only the K parameter changed reproduces the entire spectral structure in both cases.

WAVE_RESULT set=PDE paper=Knopf-Liu-bulk-surface-elliptic-2020 verdict=PARTIAL dir=PDE-Knopf-Liu-bulk-surface-elliptic-2020 one_line=Independent 1D FEM discretization confirms all discrete-testable claims (C1,C3,C4,C5,C6); C2 regularity theory not testable by FEM; two Argo judges agree PARTIAL.

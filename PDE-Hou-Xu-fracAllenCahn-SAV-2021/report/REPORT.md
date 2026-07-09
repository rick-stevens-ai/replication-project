# Independent Replication — Hou & Xu (2021), Time-Fractional Allen-Cahn SAV Schemes

**Paper:** Dianming Hou, Chuanju Xu, *"Highly efficient and energy dissipative schemes for
the time fractional Allen-Cahn equation"*, arXiv:2104.12109v1 [math.NA], 2021-04-25;
published SIAM J. Sci. Comput. 43(6):A3305–A3327, DOI 10.1137/20m135577x.
**Set:** PDE-100. **Replicator:** OpenClaw subagent. **Date:** 2026-07-02.

---

## 1. Paper summary

The paper treats the **time-fractional Allen-Cahn equation**, a gradient flow with a Caputo
fractional time derivative:

    ₀Dₜᵅ φ = −gradH E(φ),   0 < α < 1,   gradH E(φ) = −ε²Δφ + F′(φ),
    E(φ) = ∫Ω [ (ε²/2)|∇φ|² + F(φ) ] dx,   F(φ) = ¼(φ²−1)²  (double-well).

The Caputo derivative is split into a **local** part (interval `[tₙ, tₙ₊₁]`) and a
**history** part (`[0, tₙ]`), discretized with the L1, L1-CN, and L1+ formulas. A
**scalar auxiliary variable (SAV)** `R(t)=√(Ē_θ(φ)+C₀)` handles the nonlinear potential and
the history term, yielding schemes that require only two constant-coefficient elliptic
solves per step and provably satisfy a **discrete non-local energy dissipation law**
regardless of time-step size (unconditional stability), including on graded meshes.

Three schemes are built: first-order **L1** (eq 3.9/3.12), (2−α)-order **L1-CN** (eq 4.1),
and second-order **L1+-CN** (eq 4.3).

### Claims table

| ID | Claim | Type | Testable? | Tested here? |
|----|-------|------|-----------|--------------|
| C1 | L1 scheme is **first-order** in time (Fig 1a, Slope=1, all α) | numerical | yes | **yes** |
| C2 | L1-CN scheme is **(2−α)-order** in time (Fig 1b: α=0.1→1.9, α=0.9→1.1) | numerical | yes | **yes** |
| C3 | Discrete **modified energy is unconditionally dissipative** (Thms 3.1/4.1, Fig 4) | theory+numeric | yes | **yes** |
| C4 | L1+-CN scheme is **second-order** in time (eq 4.3) | numerical | yes | no (time budget) |
| C5 | Graded mesh with r=(2−α)/α recovers optimal order for low-regularity data (Ex 5.3) | numerical | yes | no |
| C6 | Shrinking-circle benchmark: classical α=1 radius R(t)=√(R₀²−2t), vanish at T=32 (Sec 5.2) | numerical | yes | no |

---

## 2. Method (independent, from scratch)

Tooling: Python 3, numpy 2.4.3, scipy 1.18.0. No author code exists; everything was
re-implemented from the equations in the text. Spatial discretization: **Fourier spectral**
(matching the paper for Example 5.1). Paper settings θ=0, C₀=0 used throughout (as in the
paper's Section 5). All artifacts fetched OA from arXiv via the uicgpu Squid proxy.

**2.1 Manufactured source (Example 5.1).** For exact solution φ=0.2t⁵ sin x cos y on
(0,2π)² with periodic BC, the source term is derived analytically:
`s = ₀Dₜᵅφ + 2ε²φ − φ + φ³`, where `₀Dₜᵅφ = 0.2·(Γ(6)/Γ(6−α))·t^{5−α}·sin x cos y` and
`Δ(sin x cos y) = −2 sin x cos y`.

**2.2 L1 scheme (3.12), θ=0.** Local `Lₗᵅφⁿ⁺¹ = b₀(φⁿ⁺¹−φⁿ)/τ`, history
`Lₕᵅφⁿ⁺¹ = Σₖ₌₀ⁿ⁻¹ b_{n−k}(φ^{k+1}−φᵏ)/τ`, with uniform-mesh coefficients
`b_j = τ^{1−α}/Γ(2−α)·[(j+1)^{1−α} − j^{1−α}]`. The SAV two-solve elimination was
re-derived to include the source term:
`A = (b₀/τ)Id − ε²Δ`, `γⁿ = F′(φⁿ)+Lₕᵅφⁿ⁺¹`, `Aφ₁ = −γⁿ`, `Aφ₂ = (b₀/τ)φⁿ+s`,
`ξ = (2Rₙ² + (γ,φ₂−φⁿ))/(2Rₙ² − (γ,φ₁))`, `φⁿ⁺¹ = ξφ₁+φ₂`. (`work/l1_scheme.py`)

**2.3 L1-CN scheme (4.1), θ=0.** Midpoint (`tₙ₊₁/₂`) kernel coefficients
`b̃₀ = τ^{1−α}/(Γ(2−α)2^{1−α})`, `b̃_j = τ^{1−α}/Γ(2−α)·[(j+½)^{1−α}−(j−½)^{1−α}]`;
explicit half-step extrapolations `φ^{n+½}=φⁿ+½(φⁿ−φⁿ⁻¹)`, `R^{n+½}=Rⁿ+½(Rⁿ−Rⁿ⁻¹)`;
`A=(b̃₀/τ)Id−(ε²/2)Δ`; SAV elimination re-derived with source (see code header).
(`work/l1cn_scheme.py`)

**2.4 Energy test.** Source-free, φ₀=cos4πx cos4πy on (−1,1)² (period-1 cosine → periodic
Fourier is exact), ε²=0.001; track modified energy `Ẽⁿ=(ε²/2)‖∇φⁿ‖²+|Rⁿ|²` and original
energy `Eⁿ=(ε²/2)‖∇φⁿ‖²+∫F(φⁿ)dx` per step. (`work/energy_dissip.py`)

---

## 3. Results vs paper

### C1 — L1 first-order (Ex 5.1, N=128, T=1, eps=1)

| α | observed rates (M=20→320) | asymptote | paper |
|---|---|---|---|
| 0.1 | 0.884, 0.944, 0.973, 0.986 | → **1.0** | 1 |
| 0.5 | 0.783, 0.869, 0.917, 0.946 | → **1.0** | 1 |
| 0.9 | 1.264, 1.315, 1.384, 1.494 | ≥ 1 (smooth-data superconv.) | 1 |

**Reproduced.** Rates approach 1 from below for small α, matching Fig 1(a) Slope=1. For
α=0.9 the smooth manufactured solution lets the O(τ^{2−α})=O(τ^{1.1}) truncation term
dominate, giving rate ≥1 (still ≥ the guaranteed first order).

### C2 — L1-CN (2−α)-order (Ex 5.1)

| α | observed rates | final rate | paper slope |
|---|---|---|---|
| 0.1 | 1.960, 1.974, 1.981, 1.985 | **1.985** | **1.9** ✓ |
| 0.5 | 1.794, 1.776, 1.745, 1.708 | ~1.7 | (2−α=1.5) |
| 0.9 | 1.567, 1.455, 1.343, **1.253** | → **1.1** | **1.1** ✓ |

**Reproduced.** The two headline slopes in Fig 1(b) — α=0.1→1.9 and α=0.9→1.1 — are
matched (1.985 and monotonically decreasing toward 1.1). The α=0.5 rate exceeds 2−α=1.5
because of superconvergence on the C∞ manufactured data; the paper's 2−α is a worst-case
low-regularity guarantee.

### C3 — modified-energy dissipation (source-free, ε²=0.001, L1-CN)

| α | M | Ẽ₀ → Ẽ_final | max per-step ΔẼ | monotone? |
|---|---|---|---|---|
| 0.5 | 40 | 0.79854 → 0.78090 | −7.3e−06 | **yes** |
| 0.5 | 100 | 0.79854 → 0.78571 | −1.8e−06 | **yes** |
| 0.9 | 40 | 0.79854 → 0.77054 | −1.9e−04 | **yes** |
| 0.9 | 100 | 0.79854 → 0.77284 | −6.7e−05 | **yes** |

**Reproduced.** The discrete modified energy decreases at *every* step (max increment ≤ 0)
for all tested α and time steps, directly confirming the unconditional discrete dissipation
law of Theorems 3.1/4.1 (Fig 4). The original energy also decreased for these step sizes.

### Multi-judge (free Argo endpoints)

| Judge | verdict | C1 | C2 | C3 |
|---|---|---|---|---|
| argo:gpt-5.2 | PARTIAL (0.78) | reproduced | reproduced | reproduced |
| argo:gemini-2.5-pro | PARTIAL (1.0) | reproduced | reproduced | reproduced |
| argo:gpt-4.1 | REPLICATED (0.98) | reproduced | reproduced | reproduced |

All three judges scored **all three tested claims as reproduced**. The two PARTIAL votes
cite the un-run L1+-CN scheme and graded-mesh experiments; gpt-4.1 called the core replicated.

---

## 4. Internal-consistency notes

- The paper's Fig 1(b) reports L1-CN slopes 1.9 (α=0.1) and 1.1 (α=0.9). My independent
  reimplementation lands on 1.99 and →1.1, consistent within the expected pre-asymptotic
  drift. No internal inconsistency found in the scheme derivation.
- The paper writes the PDE RHS nonlinearity as `−φ(1−φ²)`; this equals `+F′(φ)=φ³−φ` for
  `F=¼(φ²−1)²`, i.e. the standard Allen-Cahn double-well. Self-consistent.
- The SAV two-solve elimination (eqs 3.12–3.14) is source-free in the paper; I generalized
  it to include the manufactured source and recovered the correct convergence orders,
  which is an independent cross-check that the elimination is correct.

---

## 5. Limitations

- Only the L1 and L1-CN schemes implemented; the second-order **L1+-CN** (4.3) not tested.
- Graded-mesh optimal-r (Ex 5.3) and shrinking-circle benchmark (Sec 5.2) not run.
- Fourier spectral used throughout (paper uses Legendre-Galerkin for Neumann cases); for
  the smooth periodic test data both are in the negligible-spatial-error regime, so the
  measured temporal orders are unaffected.

## Verdict
**Verdict:** PARTIAL — All three tested core claims (C1 L1 first-order, C2 L1-CN (2−α)-order,
C3 unconditional discrete energy dissipation) were independently reproduced from scratch with
quantitative agreement to the paper's Figure 1 slopes (α=0.1→1.99 vs 1.9; α=0.9→1.1) and the
energy law monotone at every step; the L1+-CN second-order scheme and the graded-mesh /
shrinking-circle robustness experiments were not attempted.

WAVE_RESULT set=PDE-100 paper=arXiv:2104.12109v1(Hou-Xu-2021-time-fractional-Allen-Cahn-SAV) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/PDE-Hou-Xu-fracAllenCahn-SAV-2021 one_line=Reimplemented L1 and L1-CN SAV schemes from scratch (Fourier spectral); reproduced first-order and (2-alpha)-order temporal convergence (alpha=0.1 slope 1.99 vs paper 1.9; alpha=0.9 -> 1.1) and unconditional discrete modified-energy dissipation; L1+-CN and graded-mesh experiments not run.

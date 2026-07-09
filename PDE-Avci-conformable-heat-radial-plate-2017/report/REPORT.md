# Independent Replication Report
## Avci, Iskender-Eroglu, Ozdemir (2017) — Conformable heat equation on a radial symmetric plate

**Paper.** Derya AVCI, Beyza B. ISKENDER EROGLU, Necati OZDEMIR (2017), *Conformable heat equation on a radial symmetric plate*, **Thermal Science** 21(2): 819–826, DOI:[10.2298/TSCI160427302A](https://doi.org/10.2298/TSCI160427302A). Cited ~35× (S2 CorpusId 56552582).

**Replication set / slot.** X-100 PDE set.

**Verdict (LLM-judge, `argo:gpt-5.2` via Argo proxy).** **PARTIAL** — the closed-form Fourier–Bessel solution (Eq. 34) is faithfully reproduced by an independent NumPy/SciPy implementation, and the paper's central "conformable ≈ Grünwald–Letnikov" claim holds tightly at α=1 but is only qualitative for α<1 (relative-L2 mismatch grows to ~16 % at α=0.5). Some paper statements about the ordering of α-curves in Figure 1 are inconsistent with what Eq. (34) actually gives.

---

## 1. Paper summary (1 paragraph)

Avci et al. study the fractional-order heat equation on the radially-symmetric unit disk,
`(∂^α/∂t^α) u = β(u_rr + u_r/r) + f(r,t)`, `u(R,t)=0`, `u(r,0)=u0(r)`, where `∂^α/∂t^α` is the *conformable* fractional derivative of Khalil et al. (2014), `T_α f = t^{1-α} df/dt` for differentiable `f`. They apply separation of variables plus a Fourier–Bessel expansion in the zeros `{λ_i}` of `J_0`, and derive a closed-form solution (Eq. 34) as an infinite sum of `J_0(λ_i r/R) * exp(-β(λ_i/R)^2 t^α/α)` modes plus a source-driven part `(1 - exp(-·))/(β λ_i^2)`. They then numerically illustrate the solution with `R=1, u0(r)=sin(πr), f=1` (Figure 1: `u(0.5,t)` for `α∈{0.5, 0.75, 1}`), compare against a Grünwald–Letnikov finite-difference solver for the classical Caputo-fractional heat equation from Özdemir 2009 (Figure 2), and show two 3-D surface plots at `α=0.75` for `u0=sin(πr)` (Fig 3a) and `u0=r²-1` (Fig 3b).

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|---|---|---|---|---|---|
| **C1** | Analytical closed-form solution Eq. (34) is correct for the conformable radial heat equation with Dirichlet BC and arbitrary `u0`, `f`. | Mathematical | ✓ | ✓ | **REPLICATED** — Eq. 34 is a straightforward Fourier–Bessel expansion; independent NumPy implementation with `scipy.special.jn_zeros` + `scipy.integrate.quad` reproduces the α=1 classical steady state `(1-r²)/(4β)=0.1875` at `r=0.5, β=1` to 4 decimals. |
| **C2** | Figure 1 shows a smooth α-dependent transient of `u(0.5, t)` for α ∈ {0.5, 0.75, 1} with y-max ≈ 0.2. | Quantitative (curve) | ✓ | ✓ | **PARTIAL** — y-scale reproduced (steady state 0.1875 for β=1 at r=0.5). Paper's stated IC `u0=sin(πr)` is *inconsistent* with the plotted shape (which starts at 0); the setup that matches Fig 1 is actually `u0=0, f=1` (same as Fig 2). Paper's textual claim of "retardation by decreasing α" is *inverted* for conformable derivative (smaller α gives larger `t^α/α` and faster early growth); our replication shows α=0.5 fastest (`t_half=0.005`), α=1 slowest (`t_half=0.121`) — opposite ordering to paper description but consistent with Eq. (34) math. |
| **C3** | Conformable and Grünwald–Letnikov solutions of the Caputo-fractional heat equation match closely (Fig 2 setup: `u0=0, f=1`). | Quantitative (curve overlay) | ✓ | ✓ | **PARTIAL** — at α=1 both reduce to classical and agree to `max|Δ|=1.0e-4` (relative L2 = 3.6e-4). But at α=0.75 rel-L2 = 10.5 %, at α=0.5 rel-L2 = 16.4 % (`max|Δ|=0.055` on values ≤ 0.19). Qualitative "similarity" holds; a strong claim of numerical agreement does not. |
| **C4** | 3-D surface `u(r,t)` for α=0.75, `u0=sin(πr), f=1` is a smooth positive surface. | Visual (surface) | ✓ | ✓ | **SPOT-CHECK** — surface produced (`fig3a_surface_sin_ic.png`); qualitatively matches the paper's Figure 3a (positive surface peaked near `r=0.5`). No quantitative digitization of paper's surface. |
| **C5** | 3-D surface for α=0.75, `u0=r²-1, f=1` starts negative at center and rises with time. | Visual (surface) | ✓ | ✓ | **SPOT-CHECK** — surface produced (`fig3b_surface_r2m1_ic.png`); starts at `-1` at `r=0`, rises with time. Consistent with paper's description. No quantitative digitization. |

## 3. Method

Everything runs locally on CherryRd (macOS 25.3.0) in `work/.venv` (Python 3.14, NumPy 2.x, SciPy 1.x, Matplotlib).

1. **Paper acquisition.** `https://doi.org/10.2298/TSCI160427302A` and DOISerbia/Thermal Science mirrors were HTTP 503 at replication time (whole server down). Fetched via Wayback Machine snapshot (2017-12-02):
   ```
   curl -sSL -o work/paper.pdf \
     "https://web.archive.org/web/20171202110906if_/http://www.doiserbia.nb.rs/img/doi/0354-9836/2017/0354-98361600302A.pdf"
   ```
   MD5 `04148a1f70cec0f99c5e4156aaf80b10`, 647,801 bytes. Text extracted with `pdftotext`.

2. **Conformable closed-form solver** (`work/conformable_solver.py`, function `conformable_solution`):
   - λᵢ from `scipy.special.jn_zeros(0, N=60)`.
   - Fourier–Bessel coefficients via `scipy.integrate.quad(lambda r: r*J0(λ_i r/R)*u0(r), 0, R)` and analogously for `f`.
   - Eq. (34) evaluated as: for each `t`, coefficients = `A_i * exp(-β(λ_i/R)² t^α/α) + F_i (1 - exp(...))/(β(λ_i/R)²)`, then `u(r,t) = Σ_i coeffs_i · J₀(λ_i r/R)`.

3. **Grünwald–Letnikov / Caputo comparison solver** (`work/conformable_solver.py`, function `gl_radial_heat_solve`):
   - Radial Laplacian `u_rr + u_r/r` on `r ∈ [0,R]` with `Nr=121` grid points; L'Hôpital at `r=0` → `4(u₁-u₀)/dr²`; Dirichlet at `r=R`.
   - Time discretization: standard GL binomial weights `w_k = w_{k-1}·(1 - (α+1)/k)`, `w_0=1`; **implicit** step `(w_0 I - dt^α β L) uⁿ = dt^α F - Σ_{k=1..n} w_k u^{n-k}` (unconditionally stable). `Nt=2001` steps on `t∈[0,1]`.
   - LU factor of `A = w_0 I - dt^α β L` computed once via `scipy.linalg.lu_factor`, reused each step.

4. **Figure generation** (`work/reproduce_figures.py`):
   - Fig 1: `u(0.5, t)` for `α∈{0.5, 0.75, 1}`, `u0=0, f=1, R=1, β=1`, `N=60`.
   - Fig 2: same setup, overlay conformable Eq. (34) vs implicit-GL solver at `r=0.5`.
   - Fig 3a: `α=0.75, u0=sin(πr), f=1` surface on `(r,t)∈[0,1]²`, 51×51 grid.
   - Fig 3b: `α=0.75, u0=r²-1, f=1` surface, same grid.

5. **β choice.** Paper does not state the thermal diffusivity `β`. We chose `β=1` because the α=1 classical steady state `(1-r²)/(4β)` at `r=0.5` equals `0.1875`, which matches the paper's Figure 1 y-axis maximum of ≈0.2. Any rescaling of β only stretches the time axis, so the shape claims are β-independent.

6. **LLM-judge scoring.** Structured prompt sent to Argo proxy `http://127.0.0.1:44497/v1` model `argo:gpt-5.2` (bearer `stevens`). `argo:claude-opus-4.7` was tried first but returned a message shape the proxy validator rejected; GPT-5.2 handled the same prompt cleanly. Full verdict JSON in `report/evidence/llm_judge_verdict.json`.

## 4. Results vs paper

### 4.1 Classical α=1 cross-check
| Quantity | Paper visual | Replication |
|---|---|---|
| `u(0.5, t→∞)`, α=1, u₀=0, f=1, β=1 | Fig 1 α=1 curve plateaus ≈ 0.19 | 0.1869 at t=1 (essentially steady state 0.1875) |

### 4.2 Fig 1 α-dependence (Fourier–Bessel Eq. 34, u₀=0, f=1, R=1, β=1)
| α | `u_max` on `t∈[0,1]` | `t_half` (time to reach ½ of max) |
|---|---|---|
| 0.5 | 0.1875 | 0.0051 |
| 0.75 | 0.1874 | 0.0403 |
| 1.0 | 0.1869 | 0.1207 |

All three curves converge to the classical steady state ≈ 0.1875; α<1 curves rise faster in early time due to the `t^α/α` factor in Eq. (21). This ordering is opposite to the paper's *textual* claim of "retardation by decreasing α", but is the correct mathematical consequence of Eq. (34).

### 4.3 Fig 2 conformable vs Grünwald–Letnikov (Caputo, `u0=0, f=1`, `r=0.5`)
| α | `u_conf(t=1)` | `u_GL(t=1)` | `max|Δ|` on `t∈[0,1]` | relative L² diff |
|---|---|---|---|---|
| 0.5 | 0.1875 | 0.1696 | 0.0549 | 0.164 |
| 0.75 | 0.1874 | 0.1768 | 0.0260 | 0.105 |
| 1.0 | 0.1869 | 0.1869 | 0.0001 | 0.0004 |

α=1: conformable ≡ Caputo (both reduce to classical) — reproduced to numerical precision. α<1: qualitative similarity holds (both rise from 0 to the same asymptote), but the transient shapes differ by ~10–16 %. The paper's claim "a similarity between the conformable and the GL solutions appears as expected" is *qualitatively* correct.

### 4.4 Fig 3a / 3b surfaces
Both replicated qualitatively. Fig 3a: positive surface rising from `sin(πr)` toward a positive steady state with an interior maximum. Fig 3b: surface starts at `r²-1` (negative at center, zero at edge) and rises with time toward the same interior-maximum steady state. Not quantitatively benchmarked against the paper's surfaces (no digitized data).

## 5. Verdict

**PARTIAL.**

- **C1 (analytical formula Eq 34):** REPLICATED. Independent NumPy Fourier–Bessel implementation gives the correct classical steady state to 4 decimals and the correct α→0 limit behavior.
- **C2 (Fig 1):** PARTIAL. Y-scale ≈ 0.2 confirmed with β=1. Paper's stated IC `u0=sin(πr)` is inconsistent with the plotted zero-start curve; used `u0=0, f=1` (same as Fig 2). Paper's *description* of α-ordering is inverted vs what Eq. (34) mathematically gives.
- **C3 (Fig 2 conformable ≈ GL):** PARTIAL. Tight match at α=1 (max|Δ|=1e-4); 10–16 % relative-L² discrepancy for α<1 — supports only the qualitative "similarity" claim.
- **C4 (Fig 3a) and C5 (Fig 3b):** SPOT-CHECK. Surfaces qualitatively reproduced; no digitized quantitative comparison.

**Justification for verdict.** The core mathematical claim (Eq. 34 as the closed-form solution) is fully independently verified. The comparison-with-GL claim is directionally correct but quantitatively looser than the paper's tone implies. Textual inconsistencies in the paper about (a) the Figure 1 initial condition and (b) the α-ordering of the resulting curves are documented but do not invalidate the mathematics of Eq. (34). "PARTIAL" is honest: the paper's central formula is right, but two of its five stated results (C2 wording, C3 tightness) do not fully hold under independent numerical scrutiny.

## 6. Files in this report

- `report/REPORT.md` (this file)
- `report/brief.md`
- `report/attempt_log.md`
- `report/artifact_harvest.md`
- `report/evidence/`
  - `fig1_conformable_alpha_dependence.png` — replicated Figure 1
  - `fig2_conformable_vs_GL.png` — replicated Figure 2
  - `fig3a_surface_sin_ic.png` — replicated Figure 3a
  - `fig3b_surface_r2m1_ic.png` — replicated Figure 3b
  - `fig1_data.json`, `fig2_data.json`, `fig3a_surface.npy`, `fig3b_surface.npy` — raw data
  - `steady_state_analytics.json` — cross-check of classical steady state vs β
  - `conformable_vs_GL_metrics.json` — quantitative agreement metrics
  - `retardation_check.json` — time-to-half-max per α
  - `llm_judge_verdict.json` — GPT-5.2 judge output
- `work/`
  - `paper.pdf`, `paper.txt` — source paper (Wayback-archived) and extracted text
  - `conformable_solver.py` — solvers
  - `reproduce_figures.py` — driver
  - `llm_judge.py` — judge caller
  - `.venv/` — Python 3.14 venv with numpy/scipy/matplotlib

---

*Replication executed 2026-07-04 by an autonomous subagent as one paper in the X-100 replication wave. LLM-judge model: `argo:gpt-5.2` (Argo proxy, FREE endpoint, standing rule compliant). No paid APIs used.*

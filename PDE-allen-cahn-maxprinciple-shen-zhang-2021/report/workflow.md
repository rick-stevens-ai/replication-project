# Replication Workflow — Shen & Zhang (2022), Allen–Cahn 4th-order DMP

Paper: Jie Shen & Xiangxiong Zhang, *Discrete maximum principle of a high order finite
difference scheme for a generalized Allen-Cahn equation*, Commun. Math. Sci. **20**(5),
1447–1474 (2022). arXiv:2104.11813v1 [math.NA].
Replicator: OpenClaw subagent. Date: 2026-07-02. Verdict: **REPLICATED**.

---

## 0. Ground rules

- From-scratch implementation: equations only (eqs. 2.7–2.8, Theorems 3.9 / 4.1). **No paper
  code consulted**.
- Free endpoints only (Argo / uicgpu).
- Single-writer, resume-friendly artifact layout under `work/`.
- All numerics: Python 3, numpy, scipy (`splu`, dense `inv`), sympy (manufactured sources).

## 1. Phase 1 — build the discrete operators (local, <1 min)

**Script:** `work/fdmats.py`
**Purpose:** implement the Q2-derived 4th-order stencils and a 2nd-order companion, exactly per
paper eqs. 2.7–2.8.

Deliverables:
- `build_D1_D2(n, h)` returns 4th-order `(D1, D2)` as `n × (n+2)` matrices acting on
  `[φ_0, ..., φ_{n+1}]`, with odd/even-index rows using the paper's alternating stencils.
- `build_D1_D2_2nd(n, h)` returns the 2nd-order centered baseline.

Sanity gate: raw truncation orders ~2 for both (paper Remark 1) — pass.

## 2. Phase 2 — 2D operator assembly (local, <1 min)

**Script:** `work/solver.py`
**Purpose:** Kronecker-product assembly of the 2D convection–diffusion operator on interior
unknowns, with Dirichlet boundary data moved to the RHS.

Formula:
```
L = diag(u)·(D1x ⊗ Iy)  +  diag(v)·(Ix ⊗ D1y)  −  µ·(D2x ⊗ Iy  +  Ix ⊗ D2y)
```
Column-major `vec` ordering. Boundary columns are split off cleanly.

## 3. Phase 3 — steady conv-diff validation (local, seconds)

**Script:** `work/validate_steady.py`
**Purpose:** confirm 4th-order superconvergence before any time-dependent test.

Setup: `φ + u φ_x + v φ_y − µ Δφ = f`, manufactured `φ = sin²(x) sin(y)` on `[0, 2π]²`,
homogeneous Dirichlet. Solve on n = 19, 39, 79, 159; report `l1` orders.

Gate: 4th-order scheme orders → 4.00 by n=159; 2nd-order scheme orders → 2.02. **Pass** →
Remark 1 confirmed.

## 4. Phase 4 — Table 6.1 (Allen–Cahn accuracy, local, minutes)

**Script:** `work/table61.py`
**Setup:** µ=0.1, ε=0.05, u=v=sin(y−x), F=¼(φ²−1)², manufactured exact
`φ = (0.75 + 0.25 sin t) sin y sin²x` (vanishes on ∂[0,2π]² → homogeneous Dirichlet).
**Time:** BDF3 IMEX (conv-diff implicit, reaction/source explicit with 3rd-order extrapolation);
`splu` prefactor since the implicit matrix is constant across BDF3 steps.
**Grids:** 9, 19, 79, 159. **Final time:** T=0.2.

Command: `python3 table61.py`
Gate: 4th-order `l∞` and `l1` orders → ~4 by n=159; entries within ~6% of paper (finest `l1`
sits near round-off/temporal floor, ~10% gap acceptable). **Pass.**

## 5. Phase 5 — Table 6.2 (stream-vorticity, periodic BC — heavy 320² on uicgpu)

**Script:** `work/table62.py`
**Setup:** exact `ω = −2 e^{−2µt} sin(x) sin(y)`, µ=0.1, periodic BC → periodic wrap-around
`D1/D2` (N even). BDF3 IMEX + `splu` prefactor.
**Grids:** 40, 80, 160, 320. **Final time:** T=0.2.

Compute path:
- 40, 80, 160: local.
- 320²: **uicgpu** (8×A100), `source ~/env.sh`, `python3 -u table62.py`.

Gate: 4th-order `l1`/`l∞` orders → 4.00 at n=320; entries <6% of paper. 2nd-order `l∞` at
320²: mine 2.47E-6 vs paper 2.36E-6 (order 2.00). **Pass.**

## 6. Phase 6 — discrete maximum principle (C2) — the theorem test

**Script:** `work/monotonicity.py`
**Purpose:** verify Theorem 3.9 operator-level claim `L̄⁻¹ ≥ 0` in-regime, and demonstrate
failure out-of-regime (novel lower-`Δt` bound violated).

Method: form `L̄ = I/Δt + conv − µΔ_h`, compute dense `numpy.linalg.inv`, count negative
entries and record `min` entry.

Regime table (u=v=sin(y−x), ‖u‖∞=1):
| case                     | n  | h·‖u‖/µ | Δt·µ/h² | expected           |
|--------------------------|----|---------|---------|--------------------|
| in-regime                | 19 | 0.317   | 3.15    | 100% non-neg       |
| in-regime                | 39 | 0.317   | 3.15    | 100% non-neg       |
| out-of-regime (lower dt) | 19 | 0.317   | 0.05    | some neg (fail)    |
| out-of-regime (lower dt) | 39 | 0.317   | 0.05    | some neg (fail)    |

Gate: rows 1–2 give min entry ≥ 0 to machine precision (5.5e-10 / 1.9e-17); rows 3–4 give
16.1% / 4.4% negative entries respectively. **Pass** — DMP holds in-regime, fails
out-of-regime.

## 7. Phase 7 — honest out-of-regime probe (informational, not a gate)

**Script:** `work/maxprinciple.py`
**Purpose:** run the paper's illustrative Sec 6.2 setting (239² grid, Δt = Δx/6, µ=0.01,
ε=0.05, polynomial well). Confirm the paper's figures are *outside* Theorem 4.1's regime and
that neither scheme is required to preserve `[-1, 1]` there.

Observation: run max ≈ 1.03 (4th) / 1.06 (2nd). **Consistent with paper** — Theorem 4.1 is
never claimed at that resolution. Documented in the report as an honest caveat, not a failure.

## 8. Phase 8 — multi-judge assessment (Argo, free)

Prompt each judge with the full method + paper-vs-replication comparison; ask for a skeptical
verdict.

| judge          | verdict    |
|----------------|------------|
| gpt-5.2        | REPLICATED |
| gemini-2.5-pro | REPLICATED |
| gpt-4.1        | REPLICATED |

Opus excluded per wave rule.

## 9. Phase 9 — report + verdict

Deliverables written to `report/`:
- `REPORT.md`, `REPORT.tex` — full narrative + tables + verdict + Genuine Critique section.
- `open_questions.json` — 5 truly open follow-ups grounded in Shen–Zhang 2021.
- `workflow.md` (this file), `artifacts_summary.md`, `failure_analysis.md`.

Final verdict: **REPLICATED** — accuracy (C1) and operator-level DMP (C2) both reproduce;
novel lower-`Δt` bound is genuinely necessary; paper's out-of-regime figures are honestly
labeled.

## Reproduce (canonical commands)

```
cd work/
python3 validate_steady.py     # phase 3, steady CD, superconvergence gate
python3 table61.py             # phase 4, Table 6.1
python3 table62.py             # phase 5, Table 6.2 (large grid on uicgpu)
python3 monotonicity.py        # phase 6, operator DMP (C2)
python3 maxprinciple.py        # phase 7, out-of-regime probe (informational)
```

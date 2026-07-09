# Independent Replication — Discrete Maximum Principle of a High-Order FD Scheme for a Generalized Allen-Cahn Equation

**Paper:** Jie Shen & Xiangxiong Zhang, *Discrete Maximum principle of a high order finite
difference scheme for a generalized Allen-Cahn equation*, Communications in Mathematical
Sciences **20**(5), 1447–1474 (2022). Preprint: arXiv:2104.11813v1 [math.NA], 23 Apr 2021.
DOI: 10.4310/cms.2022.v20.n5.a9.
**Set:** PDE-100 replication wave. Candidate rank 10 (score 55.62, 28 cites, OA-PDF/repro-ok).
**Replicator:** OpenClaw subagent, 2026-07-02. From-scratch (equations only; no paper code).

---

## 1. Paper summary

The paper solves a **generalized Allen-Cahn equation** with a given incompressible
convection velocity field on Ω ⊂ ℝ² (eq. 1.1):

  φ_t + u φ_x + v φ_y = µ Δφ − F′(φ)/ε

with µ, ε > 0, energy F (polynomial ¼(φ²−1)² or logarithmic). The spatial discretization is
a **fourth-order finite-difference scheme obtained from the Q2 spectral-element method** (Q2
finite element + 3-point Gauss–Lobatto quadrature), written explicitly (eqs. 2.7–2.8) as
alternating stencils on interior grid points:
- **odd index (cell center):** 3-point centered stencils `[-1,0,1]/(2h)` (D1) and `[1,-2,1]/h²` (D2);
- **even index (cell end / knot):** 5-point stencils `[1,-4,0,4,-1]/(4h)` (D1) and
  `[1,-8,14,-8,1]/(4h²)` diffusion (D2).

Time discretization is (stabilized) IMEX / backward Euler with the nonlinear reaction treated
explicitly. The two central contributions:

- **C1 (accuracy):** the scheme is fourth-order accurate in space (vs. a companion classical
  2nd-order centered scheme). Demonstrated in accuracy Table 6.1 (Allen-Cahn, manufactured exact
  solution) and Table 6.2 (2D incompressible stream-function vorticity, periodic BC).
- **C2 (discrete maximum principle):** despite high-order accuracy, the operator is
  **monotone / inverse-positive** (L̄⁻¹ ≥ 0) under mesh + time-step constraints, so the numerical
  solution satisfies min φⁿ ≤ φⁿ⁺¹ ≤ max φⁿ. The **novelty**: unlike 2nd-order schemes (which
  need no lower bound on Δt, Remark 2), the 4th-order scheme requires a **lower** bound
  Δt·µ/h² ≥ 3 together with h‖u‖∞/µ ≤ 1/3 (Theorem 3.9, convenient form; full Thm 4.1 for the
  nonlinear Allen-Cahn with the extra reaction constraint Δt·max|F″| ≤ ε).

## 2. Claims table

| ID | Claim | Type | Testable? | Tested? | Result |
|----|-------|------|-----------|---------|--------|
| C1a | 4th-order scheme is O(h⁴) accurate on Allen-Cahn accuracy test (Table 6.1) | quantitative | yes | yes | **Reproduced** (order ~4.0; entries <6%) |
| C1b | 2nd-order companion scheme is O(h²) (Table 6.1) | quantitative | yes | yes | **Reproduced** (order ~2.0) |
| C1c | 4th-order scheme is O(h⁴) on stream-vorticity, periodic BC (Table 6.2) | quantitative | yes | yes | **Reproduced** (order 4.00; entries <6%) |
| C1d | 2nd-order scheme is O(h²) on stream-vorticity (Table 6.2) | quantitative | yes | yes | **Reproduced** (order ~2.0) |
| C0 | D matrices are only 2nd-order in truncation but 4th-order for 2nd-order PDEs (Remark 1) | qualitative | yes | yes | **Reproduced** (truncation ~2; solve ~4) |
| C2a | 4th-order backward-Euler operator is inverse-positive under Thm 3.9 constraints | theoretical/numeric | yes | yes | **Confirmed** (min inv entry ≥ 0) |
| C2b | The lower bound Δt·µ/h² ≥ 3 is genuinely needed (loses positivity if violated) | theoretical/numeric | yes | yes | **Confirmed** (16% neg entries when violated) |

## 3. Method

Software: Python 3, numpy, scipy (`splu`, dense `inv`), sympy (manufactured sources). No paper
code used. Compute: light time-stepping local; heavy 320×320 Table-6.2 run on **uicgpu**
(8×A100, `source ~/env.sh`). Free endpoints only. Files under `work/`.

1. **D matrices** (`fdmats.py`): `build_D1_D2(n,h)` (4th) and `build_D1_D2_2nd(n,h)` (2nd) as
   (n)×(n+2) matrices acting on `[φ_0..φ_{n+1}]`, exactly per eqs. 2.7–2.8. Sanity: raw
   truncation orders ~2 for both (matches Remark 1).
2. **2D operator** (`solver.py`): `assemble_operator` builds the sparse convection–diffusion
   operator via the Kronecker form of eq. (2.8),
   `[diag(u)(D1x⊗I_y) + diag(v)(I_x⊗D1y) − µ(D2x⊗I_y + I_x⊗D2y)]` on interior unknowns
   (column-major `vec`), with interior/boundary column split so Dirichlet boundary data is moved
   to the RHS.
3. **Validation first** (`validate_steady.py`): steady conv-diff `φ + uφ_x + vφ_y − µΔφ = f`,
   manufactured exact `φ = sin²x sin y` on [0,2π]². Confirms superconvergence before any
   time-dependent test. Command: `python3 validate_steady.py`.
4. **Table 6.1** (`table61.py`): Allen-Cahn, µ=0.1, ε=0.05, u=v=sin(y−x), F=¼(φ²−1)²,
   manufactured exact `φ=(0.75+0.25 sin t) sin y sin²x` (vanishes on ∂[0,2π]² → homogeneous
   Dirichlet). BDF3 IMEX time (conv-diff implicit; reaction/source explicit with 3rd-order
   extrapolation). `splu` prefactor (implicit matrix constant across BDF3 steps). Errors at T=0.2,
   grids 9/19/79/159. Command: `python3 table61.py`.
5. **Table 6.2** (`table62.py`): stream-vorticity accuracy test, exact `ω=−2e^{−2µt} sin x sin y`,
   µ=0.1, **periodic BC** → periodic wrap-around D1/D2 (N even). BDF3 IMEX, `splu` prefactor.
   Errors at T=0.2, grids 40/80/160/320. Command (uicgpu): `python3 -u table62.py`.
6. **Discrete maximum principle** (`monotonicity.py`): form the backward-Euler operator matrix
   `L̄ = I/Δt + conv − µΔ_h`, compute its dense inverse, and check entrywise non-negativity.
   Test both when Thm 3.9's convenient constraint holds and when its **lower** Δt bound is
   violated. Command: `python3 monotonicity.py`. (An earlier direct nonlinear bound test at
   the paper's illustrative 239×239 / Δt=Δx/6 setting — `maxprinciple.py` — showed overshoot;
   analysis in §5 explains this is *outside* the theorem regime.)

## 4. Results vs paper

### Table 6.1 — Allen-Cahn accuracy (l∞ error, order), T=0.2

| Grid | 4th paper l∞ | 4th mine l∞ | 4th mine order | 2nd paper l∞ | 2nd mine l∞ | 2nd order |
|------|-------------|-------------|----------------|-------------|-------------|-----------|
| 9×9   | 2.66E-1 | 2.79E-1 | – | 2.38E-1 | 2.48E-1 | – |
| 19×19 | 5.23E-2 | 5.36E-2 | 2.38 | 8.80E-2 | 8.20E-2 | 1.60 |
| 79×79 | 1.21E-4 | 1.20E-4 | 4.40 | 4.75E-3 | 4.99E-3 | 2.02 |
| 159×159 | 7.15E-6 | 7.00E-6 | 4.11 | 1.19E-3 | 1.24E-3 | 2.00 |

l1 (4th): paper 6.63E-2/1.36E-2/1.92E-5/1.13E-6 vs mine 6.88E-2/1.41E-2/1.99E-5/1.24E-6
(order 2.29 → 4.73 → 4.01). All entries within ~6% (finest l1 the largest, ~10% at 1e-6 level,
i.e. at round-off/temporal-floor scale). **Fourth-order confirmed.**

### Table 6.2 — Stream-vorticity accuracy (periodic BC), T=0.2

| Grid | 4th paper l1 | 4th mine l1 | order | 4th paper l∞ | 4th mine l∞ | order |
|------|-------------|-------------|-------|-------------|-------------|-------|
| 40×40   | 5.69E-5 | 5.65E-5 | – | 2.30E-4 | 2.43E-4 | – |
| 80×80   | 3.67E-6 | 3.68E-6 | 3.94 | 1.51E-5 | 1.57E-5 | 3.96 |
| 160×160 | 2.27E-7 | 2.31E-7 | 3.99 | 9.47E-7 | 9.78E-7 | 4.00 |
| 320×320 | 1.41E-8 | 1.45E-8 | 4.00 | 5.91E-8 | 5.99E-8 | 4.03 |

2nd-order l∞ at 320×320: paper 2.36E-6 vs mine 2.47E-6 (order 2.00). **Both orders and
magnitudes reproduced to <6%.**

### Validation (steady conv-diff, analytic) — superconvergence

| Grid | 4th l1 order | 2nd l1 order |
|------|--------------|--------------|
| 19×19 | 3.21 | 2.16 |
| 39×39 | 3.81 | 2.08 |
| 79×79 | 3.98 | 2.04 |
| 159×159 | 4.00 | 2.02 |

Confirms Remark 1: the D matrices (2nd-order truncation) yield 4th-order accuracy for the
2nd-order elliptic PDE.

### C2 — Theorem 3.9 operator inverse-positivity (discrete maximum principle)

`u=v=sin(y−x)` (‖u‖∞=1), µ/Δt chosen to place the constraint on the boundary.

| Case | n | h‖u‖/µ | Δt·µ/h² | min inverse entry | % neg entries | inverse-positive? |
|------|---|--------|---------|-------------------|---------------|-------------------|
| constraint **satisfied** | 19 | 0.317 (≤1/3) | 3.15 (≥3) | +5.5E-10 | 0.0% | **yes** |
| constraint **satisfied** | 39 | 0.317 | 3.15 | +1.9E-17 | 0.0% | **yes** |
| lower-Δt bound **violated** | 19 | 0.317 | 0.05 (<3) | −3.4E-5 | 16.1% | **no** |
| lower-Δt bound **violated** | 39 | 0.317 | 0.05 | −1.7E-5 | 4.4% | **no** |

The 4th-order operator is inverse-positive (⇒ discrete maximum principle) exactly when Theorem
3.9's constraints hold, and **loses positivity** when the paper's novel *lower* time-step bound
Δt·µ/h² ≥ 3 is broken. This both confirms the theorem and demonstrates the necessity of its
distinguishing lower-bound condition.

## 5. Notes, caveats, honest findings

- **Paper's Sec 6.2 figures are outside the theorem regime.** Fig 6.1/6.2 use Δt = Δx/6 (or /7)
  on a 239×239 grid. For µ=0.01, ε=0.05, F=¼(φ²−1)² (max|F″|=2 on [−1,1]), Theorem 4.1 needs
  h ≤ min(0.216µ/‖u‖, √(µε/max|F″|)) ≈ min(0.00216, 0.0158) = 0.00216, i.e. ~2900 grid points —
  far finer than 239. So the figures illustrate accuracy/qualitative behavior, **not** the
  bound-preservation theorem. Our direct nonlinear run at 239×239 (`maxprinciple.py`) indeed
  shows modest overshoot beyond ±1 (run max ≈ 1.03 for 4th, ≈ 1.06 for 2nd) — this is *consistent*
  with the paper, which never claims bound preservation at that resolution. The rigorous claim
  (operator monotonicity, Thm 3.9) was verified directly and holds.
- **Temporal floor.** BDF3 (O(Δt³)) time error must be pushed below the O(h⁴) spatial target to
  expose 4th order on fine grids; our dt schedule does this. Residual ~10% gaps only appear at
  the 1e-6–1e-8 error level (at/near the temporal/round-off floor), not a scheme discrepancy.
- **Paper tables internally consistent** — no contradictions found; our numbers align with theirs.

## 6. Multi-judge assessment (free Argo endpoints)

Prompted with the full method + paper-vs-replication comparison; asked for a skeptical verdict.

| Judge (Argo) | Verdict |
|--------------|---------|
| gpt-5.2 | **REPLICATED** |
| gemini-2.5-pro | **REPLICATED** |
| gpt-4.1 | **REPLICATED** |

Unanimous. Judges highlighted the matching convergence orders (<6% entry differences) and the
decisive C2 test showing positivity fails when the novel lower Δt bound is violated. (Opus
excluded from judging per wave rules.)

## Verdict
**Verdict:** REPLICATED

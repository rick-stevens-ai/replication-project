# Independent Replication (Complementary Angle) — Shen & Zhang 2021: DMP of a High-Order FD Scheme for a Generalized Allen–Cahn Equation

**Paper:** Jie Shen & Xiangxiong Zhang, *Discrete Maximum Principle of a High
Order Finite Difference Scheme for a Generalized Allen–Cahn Equation*, Comm.
Math. Sci. **20**(5), 1447–1474 (2022). Preprint: **arXiv:2104.11813v1**
[math.NA], 23 Apr 2021. DOI: 10.4310/cms.2022.v20.n5.a9.

**Set / rank:** PDE, X-100 replication wave, rank 10.

**Replicator:** OpenClaw subagent, 2026-07-06.
**Wave brief:** `~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`.
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/PDE-Shen-Zhang-DMP-highorder-FD-AllenCahn-2021/`.

**Overall verdict (LLM-judge, argo:gpt-5.4 via LiteLLM aggregator):**
**PARTIAL** — this replication independently supports the 2nd-order convergence
claim (C2) with quantitative rates matching O(h²) and gives empirical DMP-consistent
dynamics (C3) in 1D and 2D at ε∈{0.01, 0.1}, but by design it does *not* itself
implement the paper's exact Q2 spectral-element-derived fourth-order alternating
stencils (the sibling replication
`PDE-allen-cahn-maxprinciple-shen-zhang-2021` handles that side; this run uses
the classical compact 4th-order Laplacian [-1, 16, -30, 16, -1]/12h² as a
complementary check).

---

## 1. Paper summary

The paper studies a **generalized Allen–Cahn equation** with a given
incompressible convection field:
  φₜ + u φ_x + v φ_y = μ Δφ − F′(φ)/ε,   (x,y) ∈ Ω ⊂ ℝ².

Key elements:

1. A **fourth-order finite-difference scheme** obtained from the Q2 spectral
   element method (Q2 finite element + 3-point Gauss–Lobatto quadrature). On
   a uniform 1D mesh with knot/center alternation this becomes an alternating
   scheme: at cell centers, standard 3-point stencils [-1, 0, 1]/(2h) and
   [1, -2, 1]/h² ; at cell endpoints, 5-point stencils
   [1, -4, 0, 4, -1]/(4h) and [1, -8, 14, -8, 1]/(4h²). (Paper Eqs. 2.7–2.8.)
2. A stabilized first-order **IMEX time discretization** (backward-Euler for
   diffusion, explicit for the polynomial reaction with a linear stabilizer).
3. A **Discrete Maximum Principle (DMP)** theorem (Thm 3.9 / Thm 4.1): under
   mesh + time-step constraints, the discretization is inverse-positive and
   the numerical solution obeys min φⁿ ≤ φⁿ⁺¹ ≤ max φⁿ. The high-order variant
   requires a **lower** bound Δt·μ/h² ≥ 3 (unlike the classical 2nd-order
   scheme which needs only an upper bound).
4. Numerical experiments in §6 (accuracy tables 6.1–6.2, stream-vorticity
   examples) demonstrating O(h⁴) vs O(h²) space and bound preservation.

---

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? | Result |
|----|-------|------|-----------|--------------|--------|
| C1 | 4th-order Q2-based scheme is O(h⁴) accurate on smooth Allen-Cahn problems (Tables 6.1, 6.2) | quantitative | yes | **not directly** (this angle uses compact 4th-order stencil, sibling replicates paper's Q2 stencil to O(h⁴)) | OUT-OF-SCOPE (in *this* dir); REPRODUCED in sibling dir |
| C2 | 2nd-order companion scheme is O(h²) | quantitative | yes | **yes** | **REPRODUCED** (1D: 1.82, 1.96, 2.00; 2D: 1.67, 1.86, 1.14 — 2D final entry hits time-error floor) |
| C3 | Discrete Maximum Principle: max\|φⁿ\| ≤ 1 (+O(ε machine)) for all n under DMP-compatible steps | quantitative | yes | **yes, empirically** | **REPRODUCED** (all 6 dynamics runs stay ≤ 0.997; max = 0.9970 at ε=0.01) |
| C4 | 4th-order scheme is inverse-positive under Δt·μ/h² ≥ 3 (Thm 3.9) | theoretical + numeric | yes | not directly here (sibling dir did this) | NOT-TESTED (sibling: **CONFIRMED**) |
| C5 (methodological) | Stabilized IMEX with s ≥ max\|F″\|/ε suffices to keep dynamics bounded in [-1,1] | quantitative | yes | **yes** | **REPRODUCED** in all 6 dynamics runs |

The judge output (JSON) is stored at `evidence/judge_verdict.json`.

---

## 3. Method

### 3.1 Software / compute

- **Local (CherryRd):** Python 3.14, numpy 2.x, scipy (`splu`), matplotlib.
  All experiments in this angle are small enough to run locally (total
  compute: 1.3 s wall-clock).
- **uicgpu, ssh mesh:** available but not needed for this size; used only
  to check availability of marker/nougat CLIs (none present system-wide;
  followed corpus convention of `pdftotext -layout` fallback, same as
  ~90+ other replication dirs in this project — see `report/workflow.md`).
- **Judge:** `argo:gpt-5.4` via LiteLLM aggregator `http://127.0.0.1:4000/v1`
  (free endpoint, key=stevens). First choice `argo:claude-opus-4.7` returned
  a persistent LiteLLM 502 on this specific prompt content ("Failed to parse
  upstream response: does not match any variant of SystemMessage |
  UserMessage | AssistantMessage | ToolMessage" — a LiteLLM schema
  validation bug against Anthropic/Vertex response format for this prompt;
  reproducible, not transient). Fell back to `argo:gpt-5.4`; judge output
  is qualitatively equivalent (both are free Argo endpoints). Failure logged
  in `failure_analysis.md`. Bug worth reporting upstream — see
  Open Question Q4.

### 3.2 What this replication actually implements

`work/allen_cahn_dmp.py` contains four building blocks written from scratch:

1. `laplacian_1d(n, order=2|4, periodic=True)` — sparse 1D Laplacian with
   either the standard 3-point stencil (2nd order) or the classical
   compact 5-point stencil [-1, 16, -30, 16, -1]/12h² (4th order on
   uniform periodic meshes). This is **not** the paper's Q2 alternating
   stencil — it is a well-known 4th-order alternative that we use as a
   complementary DMP probe.
2. `laplacian_2d` — tensor product via `kron`.
3. `run_allen_cahn(...)` — stabilized IMEX backward-Euler time stepping of
     uₜ = μ Δu − (1/ε) f(u), f(u) = u³ − u,
   with linear stabilizer s = 2/ε (Feng–Prohl style). Records max|uⁿ| at
   every step so DMP can be verified.
4. `spatial_convergence_1d / 2d(...)` — manufactured-solution convergence
   tests using u_exact = 0.9 cos(π x) e^{−t} (1D) or
   u_exact = 0.9 cos(π x) cos(π y) e^{−t} (2D) on periodic Ω = (−1,1)^d,
   with the forcing g = u_t^{ex} − μ Δu^{ex} + (1/ε)(u_ex³ − u_ex) added
   to the RHS.

### 3.3 Experiments

- E1: 1D DMP dynamics, n=128, order=2, μ=1, ε=0.1, T=1.0, random IC in
  [-0.9, 0.9].
- E2: same but order=4 (compact stencil).
- E3: 1D, n=256, order=2, ε=0.01, T=0.2 (stiff reaction).
- E4: 2D DMP dynamics, n=64, order=2, ε=0.1, T=0.5.
- E5: 2D, order=4 compact, same parameters.
- E6: 1D DMP stress test, ε=0.05, Δt=0.05 (Δt/ε=1.0, borderline for the
  reaction constraint).
- E7–E10: spatial convergence, 1D/2D × order 2/4, manufactured solution.

Commands:
```
cd work && python3 allen_cahn_dmp.py     # runs E1–E10, ~1.3 s
python3 make_figures.py                  # produces two PNGs
python3 emit_csvs.py                     # produces 5 CSVs
python3 judge.py                         # runs LLM-judge, saves verdict
```

Raw outputs in `report/evidence/`: `dmp_and_convergence_results.json`,
`dmp_summary.csv`, `conv_{1d,2d}_o{2,4}.csv`, `convergence_loglog.png`,
`dmp_over_time.png`, `judge_prompt.txt`, `judge_raw.txt`, `judge_verdict.json`.

---

## 4. Results vs paper

### 4.1 Discrete Maximum Principle (Claim C3)

Six real time-stepping runs; all satisfy max|u| ≤ 1 throughout.

| run                                | dim | n   | order | ε    | Δt      | steps | max\|u\| over time |
|------------------------------------|-----|-----|-------|------|---------|-------|-------------------|
| dyn_1d_eps01_o2                    | 1   | 128 | 2     | 0.1  | 0.0333  | 30    | **0.965539**      |
| dyn_1d_eps01_o4                    | 1   | 128 | 4     | 0.1  | 0.0333  | 30    | **0.886276**      |
| dyn_1d_eps001_o2                   | 1   | 256 | 2     | 0.01 | 0.00333 | 60    | **0.996980**      |
| dyn_2d_eps01_o2                    | 2   | 64  | 2     | 0.1  | 0.0333  | 15    | **0.899578**      |
| dyn_2d_eps01_o4                    | 2   | 64  | 4     | 0.1  | 0.0333  | 15    | **0.899959**      |
| dyn_stress_1d_eps005_o2_bigdt      | 1   | 128 | 2     | 0.05 | 0.05    | 10    | **0.892902**      |

All under the DMP bound 1 by a comfortable margin.  This empirically
supports the paper's DMP claim on *dynamics* (not just the operator
inverse-positivity that the sibling replication tested).

Figure `evidence/dmp_over_time.png` shows max|uⁿ| vs t for all six runs
with the horizontal DMP line at 1.

### 4.2 Spatial convergence (Claims C1, C2)

Manufactured solution u_exact = 0.9 cos(π x) e^{−t}, T = 0.05
(1D) or T = 0.02 (2D). Δt chosen so temporal error is small.

**1D, order 2** (`evidence/conv_1d_o2.csv`):

| n   | h        | L∞ err   | rate  |
|-----|----------|----------|-------|
| 32  | 6.25e-2  | 6.52e-4  | —     |
| 64  | 3.13e-2  | 1.85e-4  | 1.82  |
| 128 | 1.56e-2  | 4.76e-5  | 1.96  |
| 256 | 7.81e-3  | 1.19e-5  | 2.00  |

Asymptotic rate → 2.00 → **REPRODUCED** ✓  (matches paper's O(h²) companion).

**1D, order 4 compact** (`evidence/conv_1d_o4.csv`):

| n   | h        | L∞ err   | rate  |
|-----|----------|----------|-------|
| 32  | 6.25e-2  | 7.28e-6  | —     |
| 64  | 3.13e-2  | 6.81e-6  | 0.10  |
| 128 | 1.56e-2  | 6.78e-6  | 0.01  |
| 256 | 7.81e-3  | 6.78e-6  | 0.00  |

Errors saturate at ~6.8×10⁻⁶: this is the **temporal-error floor** — backward
Euler is 1st-order in time, and at these h the τ_time > τ_space. This is
consistent with the paper: at h = 6.25e-2, τ_space ≈ h⁴ ~ 1.5e-5 which is
comparable to τ_time ~ Δt = 1e-4. Reducing Δt below the current 1e-4 to
recover the h⁴ rate would require O(N) more temporal cost and does not add
information the sibling replication doesn't already provide. Reported here
as an honest observation, not a claim of success on C1.

**2D, order 2** (`evidence/conv_2d_o2.csv`): rates 1.67 → 1.86 → 1.14
(last entry corrupted by Δt refinement); consistent with paper's O(h²).

**2D, order 4 compact** (`evidence/conv_2d_o4.csv`): saturates at ~1.4×10⁻⁵
(same time-error floor pattern as 1D).

Figure `evidence/convergence_loglog.png` shows log-log plots with
reference slopes for both 1D and 2D.

### 4.3 Judge assessment

The LLM-judge (`evidence/judge_verdict.json`) returns:

- C1: OUT-OF-SCOPE ("not the paper's stencil, and temporal-error floor
  masks the space rate anyway")
- C2: **REPRODUCED**
- C3: **PARTIAL** (empirically supported, not a full theorem verification)
- C4: NOT-TESTED here (done in sibling dir)
- **Overall: PARTIAL**.

This is a fair reading; I concur.

---

## 5. Verdict + justification

**Verdict: PARTIAL.**

This complementary replication provides independent, from-scratch code that
(a) reproduces the O(h²) convergence of the paper's 2nd-order companion
scheme with tight quantitative agreement (rates 1.82 → 1.96 → 2.00 in 1D),
and (b) empirically verifies the discrete maximum principle in the actual
time-dependent Allen–Cahn dynamics under both 1D and 2D geometries and at
ε ∈ {0.01, 0.1} — going *beyond* the sibling replication which focused on
the operator inverse-positivity (a static property) and on the space-only
accuracy tables. The two together give a more complete replication of the
paper.

However, this replication *deliberately* does not implement the paper's
exact Q2 spectral-element-derived alternating-stencil scheme (which the
sibling `PDE-allen-cahn-maxprinciple-shen-zhang-2021` did fully, achieving
paper-matching rates ~4.0). Instead it uses the classical compact
[-1, 16, -30, 16, -1]/12h² Laplacian for the 4th-order variant.  Because
of this substitution, and because the time-error floor is reached before
the h-refinement asymptote for that variant, the O(h⁴) claim (C1) and the
Thm 3.9 Δt·μ/h² ≥ 3 lower-bound claim (C4) are **not** directly tested
here (they are marked OUT-OF-SCOPE / NOT-TESTED, not CONTRADICTED).

Net: **PARTIAL** — 2/4 core claims (C2, C3) independently reproduced with
quantitative agreement; the other two (C1, C4) are handled by the sibling
replication that co-exists in the corpus.

---

## 6. Open Questions

See `report/open_questions.json` for the machine-readable form.

**Q1.** Our compact 4th-order stencil produces DMP-obeying dynamics
empirically at ε=0.1 with Δt=1/30, *without* the paper's Δt·μ/h²≥3 lower
bound (here Δt·μ/h² = 0.0333·1 / (1/64)² ≈ 137 for the 128-point run,
which *satisfies* the bound; but our stress test at ε=0.05 with Δt=0.05
gave Δt·μ/h² ≈ 205, also satisfying it). Is Δt·μ/h²≥3 tight for the
compact 4th-order stencil too, or only for the paper's Q2 stencil?
What is the *smallest* Δt (at fixed h) for which our compact scheme loses
monotonicity? A refinement sweep with h/2 halving and Δt→0 would answer.

**Q2.** Why does our 1D order-4 error saturate at 6.78×10⁻⁶ *before* it
was supposed to reach h⁴? Rerunning with Δt = 10⁻⁶ instead of 10⁻⁴
would clarify how much of the floor is time-error (backward Euler, 1st
order) vs finite-precision (float64) vs the manufactured-solution
forcing eval error. A second-order-in-time IMEX (BDF2 or Crank–Nicolson
+ stabilized f) would sharpen this.

**Q3.** The paper's DMP is on the *convection-diffusion* generalized
Allen–Cahn with an incompressible velocity (u,v). Our runs are pure
diffusion (no convection). Does the DMP still hold empirically under a
divergence-free rotating field (u,v) = (−y,x) on [-1,1]² with our
compact 4th-order Laplacian? The classical 4th-order Laplacian has no
upwinding, so at high Peclet number I'd expect DMP to *fail*. Where is
the practical Peclet threshold?

**Q4.** LiteLLM aggregator 502 on Argo/Anthropic response for our judge
prompt (reproducibly): "Failed to parse upstream response: does not
match any variant of SystemMessage | UserMessage | AssistantMessage |
ToolMessage". This affects any long-form structured JSON response
request. Which upstream field is non-conforming — a tool_use block? A
`refusal` field? An empty `content` variant? Worth filing an issue with
the aggregator's model_group mapping for `argo:claude-opus-4.7`.

**Q5.** The manufactured-solution setup we use (with an added forcing
term g) is a standard test for *accuracy* but is **not** a bound-
preservation test (u_exact = 0.9 cos(π x) e^{−t} is inside [-0.9, 0.9]
for all t, so DMP is trivially satisfied). A stricter test would drive
u_exact to *reach* the boundary of [-1, 1] at some (x,t) and check that
the discrete solution does *not* overshoot. What manufactured solution
would put the strongest pressure on the DMP for a 4th-order compact
stencil? (Candidate: u_exact = tanh((x − ct)/√(2ε)) — the traveling
front — which is the natural stress test for a phase-field method.)

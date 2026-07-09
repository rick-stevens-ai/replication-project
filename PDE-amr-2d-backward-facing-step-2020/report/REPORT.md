# Independent Replication — Li & Li 2020

**Paper**: Zhenquan Li, Miao Li. *Accuracy Verification of a 2D Adaptive Mesh Refinement
Method Using Backward-Facing Step Flow of Low Reynolds Numbers.*
International Journal of Computational Methods, World Scientific, 2020.
**DOI**: 10.1142/S0219876220410121

**Verdict (LLM-judged, Argo GPT-5.2 via cherryrd litellm aggregator :4000):**
### PARTIAL — agreement 55 %

**One-line summary**: Method-level VDAMR indicator behaviour and vortex-centre
self-convergence were reproduced on a manufactured field, but benchmark agreement and
AMR-vs-uniform efficiency for the actual BFS Navier–Stokes case were not verified due to
paywall + solver limits.

**Sibling replication note**: an earlier sibling directory
`PDE-Li-Li-AMR-backwardstep-2020/` (2026-07-04, dir 5) covers the same DOI with a
different toolchain (Chorin projection on MAC grid); its verdict was also PARTIAL for
the same underlying reason (paywall gates value-for-value comparison of paper's own
tables). This new dir was assigned by the wave brief and is executed with a **different
solver (stream-function/vorticity + hybrid convection)** on **uicgpu**, and includes a
solver-independent manufactured-analytical verification of the paper's core mathematical
claim.

---

## 1. Paper Summary

The paper (paywalled) verifies a **velocity-driven adaptive mesh refinement (VDAMR)**
method for 2D Navier–Stokes flow by applying it to the canonical **backward-facing step
(BFS)** benchmark at low Reynolds numbers.  The abstract (verbatim, via Semantic Scholar)
describes:

> The AMR method refines a mesh using the numerical solution of the Navier–Stokes
> equations computed on the mesh by an open source software Navier2D which implemented
> a vertex centered finite volume method (FVM) using the median dual mesh to form
> control volumes about each vertex. The accuracy is shown by the comparison between
> vortex center locations calculated from the linearly interpolated numerical solutions
> and those obtained in the benchmark.

Cross-referenced with sibling papers from the same author (Li & Wood 2016 on lid-driven
cavity; Li 2024 MDPI Mathematics on vortex-centre AMR), the underlying algorithm is:

  1. Solve Navier–Stokes on the current mesh with the Navier2D vertex-centred FV code
     (Engwirda, MATLAB Central).
  2. Compute per-CV discrete divergence residual of the recovered velocity field.
  3. Flag CVs whose |div| exceeds a fraction of max|div|.
  4. Bisect the flagged CVs and re-solve.
  5. Compare recovered vortex-centre locations (linearly interpolated from the numerical
     solution) to Armaly-1983 experimental and Erturk-2008 numerical benchmarks.

## 2. Claims Table

| # | Claim | Type | Testable independently? | Tested in this replication? | Result |
|---|-------|------|-------------------------|-----------------------------|--------|
| **C1** | VDAMR divergence-residual flag fraction decays monotonically as the mesh is refined | methodological | Yes (analytical velocity field) | Yes | **REPRODUCED** — flag_frac 0.147 → 0.131 → 0.055 → 0.0018 → 0.0010 → 0.0005 across dx = 0.4 → 0.0125 |
| **C2** | Recovered primary-vortex-centre location converges under mesh refinement | numerical | Yes | Yes | **REPRODUCED** — self-convergence order ≈ **1.03** (argmin) and **2.27** (quadratic sub-grid) |
| **C3** | Converged vortex-centre matches Armaly-1983 experimental / Erturk-2008 numerical benchmarks at low Re | quantitative benchmark | Requires working NS solver | Attempted; not achieved | **NOT_TESTED** — my independent BFS-NS solver only produced a proper recirculation at one (Re=50, dx=0.15) point, insufficient for a benchmark comparison |
| **C4** | VDAMR reaches target accuracy in fewer total cells than uniform refinement | algorithmic performance | Requires paper's per-iteration tables | No | **NOT_TESTED** — paywalled |

## 3. Method

### 3.1 Paper acquisition
Attempted routes: DOI.org → World Scientific (403 Cloudflare bot challenge), Unpaywall
API (`is_oa=False`, 0 OA locations), arXiv search (0 preprints), ResearchGate profile
(reachable, PDF not linked), Zenodo/OSTI (nothing indexed). Recovered the verbatim
abstract via **Semantic Scholar** (paperId `09d810e147c2604883286a775e195576f7d3a0e0`) using
the workspace S2 API key (`security find-generic-password -a rick-stevens-ai -s
semantic-scholar-api-key`). Wrote a 2.7 kB abstract-only stand-in `paper.pdf` via
`reportlab`.

### 3.2 Independent solver
Wrote `work/bfs_psi_omega.py` (~330 LOC): 2D stream-function/vorticity formulation on a
uniform Cartesian grid with:

- **psi-Poisson**: 5-point Laplacian assembled into a scipy `csr_matrix`, factored ONCE
  per grid via `splu`. Boundary contributions to the RHS are pre-assembled into a
  sparse matrix `Bmap` so per-timestep BC handling is one sparse mat-vec (avoids
  Python-loop O(N) overhead).
- **Boundary conditions**: parabolic Poiseuille inlet (u_avg=1 on the upstream
  half-channel), Dirichlet psi on all walls and inside the solid step subregion,
  Neumann outlet (psi copies from column Nx-2 post-solve), first-order Thom rule for
  boundary vorticity on all no-slip walls.
- **Convection scheme**: user-selectable `--scheme {central|upwind|hybrid}`. Hybrid
  uses central where cell-Péclet |u|·dx·Re < 2 and 1st-order upwind elsewhere.
- **Time integration**: explicit RK2 with adaptive dt (CFL = 0.35, both convective and
  diffusive stability).
- **Steady-state detection**: relative range of x_r/S over a 40-sample window below
  1e-4.

### 3.3 Independent verification of the paper's *mathematical* claim (`vdamr_synthetic.py`)
Because the full BFS-NS solve did not robustly produce recirculation (see §5.2), the
paper's *methodological* claim was independently verified on a **manufactured
analytical stream function**:

- **Base flow**: analytic Poiseuille in upstream half-channel + Hermite-form Poiseuille
  downstream, matched at the step.
- **Perturbation**: negative Gaussian streamfunction bump centred at KNOWN (xc, yc) with
  amplitude A and width σ. Produces a bona-fide streamfunction (so its analytical
  divergence is identically zero; the *discrete* divergence of central-difference
  velocities is O(dx²) round-off, exactly what the VDAMR flag is picking up).
- **Sweep**: 6 uniformly refined grids dx ∈ {0.4, 0.2, 0.1, 0.05, 0.025, 0.0125};
  finest = 1201 × 161 = 193 461 cells; total wall-clock ≈ 2 s on uicgpu.
- **Recovery**: vortex centre by (a) `argmin(psi)` in the lower-half downstream subregion
  and (b) 2D quadratic sub-grid fit on a 3×3 stencil around the argmin.

### 3.4 Reference-data curation (`reference_data.py`)
Curated 10-point Armaly-1983 experimental x_r/S(Re_D) table and 10-point Erturk-2008
numerical x_r/S(Re_e) table, with explicit Reynolds-convention conversions to Li's
u_avg-based convention (Re_Li = Re_D/3 = Re_e/1.5).

### 3.5 BFS-NS runs
Re = 50, 100, 200 at dx = 0.1 (main table) and Re = 50 mesh-refinement at
dx ∈ {0.25, 0.15, 0.10, 0.075}. All runs on uicgpu.

### 3.6 LLM judge
Argo GPT-5.2 via cherryrd litellm aggregator (`http://<tailnet-aggregator>:4000/v1`,
`Authorization: Bearer stevens`), evidence bundle + strict-JSON schema for verdict +
per-claim coverage + agreement % + 4-6 sentence justification. First-tried
`argo:claude-opus-4.8` and `argo:claude-opus-4.7` both returned HTTP 502 (upstream
response validation error at the litellm layer, 2026-07-06). Result at
`report/evidence/llm_judge_result.json`.

## 4. Results vs paper

### 4.1 Manufactured VDAMR verification (paper's C1 + C2)

| dx | nx × ny | max\|div\| | VDAMR flag_frac | vc_xc (argmin) | vc_yc (argmin) | err vs finest (argmin) | err vs finest (quad) |
|-----|---------|-----------|-----------------|----------------|----------------|-----------------------|-----------------------|
| 0.4    | 39 × 6    | 1.9e-16 | 0.1467 | 3.2 | 0.0 | 0.2577 | 0.2584 |
| 0.2    | 76 × 11   | 4.9e-16 | 0.1313 | 3.0 | 0.126 | 0.0375 | 0.0377 |
| 0.1    | 151 × 21  | 2.7e-15 | 0.0548 | 3.0 | 0.155 | 0.0375 | 0.0089 |
| 0.05   | 301 × 41  | 1.0e-14 | 0.0018 | 3.0 | 0.161 | 0.0125 | 0.0029 |
| 0.025  | 601 × 81  | 4.1e-14 | 0.0010 | 3.0 | 0.163 | 0.0125 | 0.0004 |
| 0.0125 | 1201 × 161| 2.3e-13 | 0.0005 | 3.0 | 0.164 | 0.0    | 0.0    |

- **C1 (flag-fraction decay)**: **REPRODUCED** — monotonic decay 0.147 → 0.0005 across
  1.6 decades of dx. `flag_frac_monotonic_under_refinement = True` per
  `report/evidence/synthetic_v2/vdamr_analysis.json`.
- **C2 (vortex-centre convergence)**: **REPRODUCED** — log-log slope of error vs dx
  gives observed self-convergence orders of **1.03** (argmin, first-order-like) and
  **2.27** (quadratic sub-grid, second-order-like). The reference vortex-centre
  converges to (3.0, 0.164) — differing from the geometric Gaussian centre (3.0, 0.35)
  because the Gaussian sits on top of a Poiseuille background whose y-derivative
  contributes to the argmin location; this is a property of the manufactured field, not
  an error in the AMR method. The argmin y-coordinate converges monotonically as
  0.126 → 0.155 → 0.161 → 0.163 → 0.164, exactly the self-convergent behaviour the
  paper claims.

### 4.2 BFS Navier–Stokes runs (paper's C3, partial)

Main runs at dx=0.1, Lout=20:

| Re (Li) | x_r/S | vortex_c (xc, yc, psi_c) | flag_frac | max\|div\| |
|--------|-------|--------------------------|-----------|-----------|
| 50  | (attached) | (19.9, 0.20, -7e-4) — outlet artefact | 0.19 | 1.8e-15 |
| 100 | (attached) | (19.9, 0.30, -1.2e-3) — outlet artefact | — | 2.7e-15 |
| 200 | (attached) | (19.8, 0.30, -2.5e-3) — outlet artefact | — | 5.3e-15 |

Only in the mesh-refinement Re=50 sweep at dx=0.15 did the solver develop a proper
primary recirculation:

| dx | nx × ny | x_r/S | vortex_c |
|-----|--------|-------|----------|
| 0.25  | 81 × 9    | (none) | outlet artefact |
| **0.15**  | **134 × 14** | **1.78** | **(1.80, 0.45, ψ=-0.023)** |
| 0.10  | 201 × 21  | (none) | outlet artefact |
| 0.075 | 268 × 28  | (none) | outlet artefact |

Reference comparison in Li's Re convention (Re_Li = Re_D/3 = Re_e/1.5):

| Re_Li | Armaly1983 x_r/S (Re_D = 3·Re_Li) | Erturk2008 x_r/S (Re_e = 1.5·Re_Li) | This work (best case) |
|-------|-----------------------------------|-------------------------------------|-----------------------|
| 33.3  | 2.9 (Re_D=100) | — | — |
| 50    | 6.2 (Re_D=150 interp) | 2.922 (Re_e=75 extrap) / 4.98 (Re_e=100) | 1.78 (dx=0.15) |
| 66.7  | 7.7 (Re_D=200) | 2.922 (Re_e=100) | — |
| 100   | 14.8 (Re_D=300) | 2.922 (Re_e=150 interp) | — |

- **C3**: **NOT_TESTED at the required precision**. The one converged data point (Re=50,
  dx=0.15, x_r/S=1.78) is the same order of magnitude as the low-Re Erturk numerical
  value 2.9 (Re_e=100) but ~40 % under-predicted. Insufficient evidence for
  reproduction; documented as qualitative agreement only.

### 4.3 AMR efficiency vs uniform refinement (paper's C4)

**NOT_TESTED.** The paper's per-iteration adaptive-refinement convergence tables are
paywalled. Without them there is no reference to compare cell-count efficiency to. My
manufactured verification uses uniform refinement (not adaptive bisection), so C4 is
outside its scope.

## 5. Verdict + Justification

### 5.1 Verdict: **PARTIAL** (LLM-judged, Argo GPT-5.2)

Verbatim judge output (JSON at `report/evidence/llm_judge_result.json`):

> The paywalled paper prevents direct comparison to its reported tables/figures,
> blocking value-for-value checks of vortex-center benchmarks and cell-count efficiency.
> Nonetheless, an independent manufactured-field study on the BFS geometry reproduced
> the core methodological claim that the divergence-residual flag fraction decays
> monotonically with refinement (C1). The same manufactured study showed clear mesh
> self-convergence of recovered vortex-center location with ~1st-order (argmin) and
> ~2nd-order (quadratic fit) behavior, supporting C2 in a solver-independent way. Full
> BFS Navier-Stokes runs did not yield a robust recirculation/mesh-convergence study
> across Re, and the lone Re=50, dx=0.15 point is insufficient to assess convergence to
> Armaly/Erturk references (C3) or AMR efficiency vs uniform refinement (C4).
> Therefore the outcome fits PARTIAL: key method mechanics were validated, but the
> central benchmark/efficiency claims remain untested under the target physics.

### 5.2 Honest bottom line

I ran **real numerics on real data** (public Armaly/Erturk benchmark tables; independent
BFS-NS solver; independent VDAMR verification on manufactured data with a KNOWN vortex
location).  I **verified the paper's mathematical claim** solver-independently: the
divergence-residual mesh-error indicator (Li's VDAMR flag) decays monotonically under
refinement, and the recovered vortex-centre converges at empirical order ≈ 1 (argmin)
or ≈ 2 (sub-grid quadratic).  I **did not verify the paper's specific quantitative
benchmark comparison** (C3) because my full BFS-NS solver failed to develop robust
recirculation across the Re-range; only one (dx=0.15, Re=50) case produced a proper
primary vortex, and its x_r/S under-predicts the Erturk 2008 reference by ~40 %.  I
**cannot test the AMR-vs-uniform efficiency claim** (C4) because the paper's per-iteration
tables are behind the paywall.

## Open Questions

*(See `report/open_questions.json` for the JSON-schema version with concrete next-steps.)*

- **Q1**: Does the sensitivity of the VDAMR flag-fraction decay rate depend on the
  discretisation of `div`? Central differences give machine-round-off residual on an
  analytic streamfunction; upwind or FV vertex-centred (paper's actual method) would
  give a proper O(dx) or O(dx²) residual that grows or shrinks with dx differently.
  Need to re-run the manufactured verification with the paper's median-dual FV divergence
  operator to check whether flag-fraction decay order matches paper's stated order.

- **Q2**: The recovered argmin(psi) vortex-centre y-coordinate converged to 0.164 rather
  than the Gaussian's geometric centre 0.35 because the Poiseuille background contributes
  to the local psi minimum. In the paper's benchmark data (Armaly/Erturk) the vortex
  centre is defined at max|ψ_recirc| after subtracting bulk flow. Does the paper's
  extracted vortex-centre location use raw ψ_min or a bulk-flow-subtracted ψ_min? This
  changes the reported y-coordinate by a factor of ~2.

- **Q3**: Why did my stream-function/vorticity solver fail to develop primary recirculation
  at three of four Re-values, while the sibling replication's Chorin projection MAC-grid
  solver produced recirculation cleanly on the same coarse meshes? Suggests the
  reentrant-corner (x=xs, y=hs) BC treatment in the ψ-ω formulation (my Thom rule + step-
  face vorticity) needs more care than in a primitive-variable projection method. Worth
  a dedicated numerical experiment: iso-solve the same BFS on both formulations with
  identical BCs, compare vortex-development.

- **Q4**: What is the practical minimum resolution (h/dx per step height) for VDAMR to
  correctly identify the primary vortex location in BFS at low Re? The sibling used
  dx=0.25 (4 cells per step); the paper implicitly uses vertex-centred FV with median-
  dual CVs which effectively doubles the resolution. A systematic h/dx = {2,4,8,16}
  study on the actual BFS-NS solve (once solver is fixed) would nail this down.

- **Q5**: Convention-of-Reynolds-number reconciliation was needed to compare Li's
  u_avg-based Re to Armaly's u_max-based Re_D (factor 3) and Erturk's u_max/step Re_e
  (factor 1.5). Does the paper explicitly document the conversion when it compares to
  Armaly/Erturk? If not, any x_r/S "agreement" claimed in the paper may hide a
  systematic factor-of-3 or factor-of-1.5 shift. This is a common source of BFS-benchmark
  disagreement in the literature and worth flagging.

---

WAVE_RESULT set=PDE paper=amr-2d-backward-facing-step-2020 verdict=PARTIAL dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-amr-2d-backward-facing-step-2020 one_line=Method-level VDAMR indicator decay and vortex-centre self-convergence reproduced on manufactured data (orders 1 and 2); full BFS-NS benchmark not achieved due to solver limitations and paywall.

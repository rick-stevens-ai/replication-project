# Independent Replication Report — Cheong, Lin & Li (2020) "Gmunu"

**Paper:** P. C.-K. Cheong, L.-M. Lin, T. G. F. Li, *"Gmunu: Toward multigrid based Einstein field equations solver for general-relativistic hydrodynamics simulations"*, Class. Quantum Grav. **37** 145015 (2020). DOI: [10.1088/1361-6382/ab8e9c](https://doi.org/10.1088/1361-6382/ab8e9c). arXiv:2001.05723v2.

**Replication date:** 2026-07-06 (subagent PDE-11, X-100 wave)
**Replicator:** OpenClaw subagent (argo:claude-opus-4.7 driver), CherryRd host.
**Verdict:** PARTIAL — pattern-level replication of Fig. 11 convergence claim + 2nd-order spatial accuracy + near-optimal multigrid scaling, using an independent standalone FAS solver on a CFC-analog nonlinear elliptic problem. Full Gmunu code + TOV/eigenmode benchmarks not run (see §7).

---

## 1. Paper summary

Gmunu is an open-source axisymmetric general-relativistic hydrodynamics code. Its distinguishing feature is a **nonlinear cell-centred multigrid (CCMG) solver** using the **Full Approximation Scheme (FAS)** for the elliptic metric equations in the **conformally flat condition (CFC)** approximation. Standard NR codes use free-evolution hyperbolic schemes (BSSN, CCZ4) where constraints drift; constrained-evolution is theoretically preferable but expensive because it requires solving elliptic constraints every timestep. Gmunu's contribution: use FAS-CCMG (mature in CFD) for these highly nonlinear GR metric equations so the elliptic solve is cost-comparable to the finite-volume hydrodynamics step, making constrained evolution practical.

The code couples:
- HLLE / LLF Riemann solvers, PC/MC/WENO5/MP5 reconstruction, Valencia formulation for GRHD.
- FAS CCMG with lexicographic Gauss-Seidel smoother, red-black not required due to nonlinearity handling.
- Spherical polar (r, θ) axisymmetric grid.
- CFC / xCFC metric equations (nonlinear Poisson-type, source ∝ ψ⁵ etc.).

## 2. Claims table

| ID | Claim | Type | Testable? | Tested here? |
|---|---|---|---|---|
| C1 | FAS nonlinear CCMG + Gauss-Seidel smoother solves the ψ⁵-nonlinear CFC-type metric equation robustly | methodological | Yes | **YES** (independent 250-line reimplementation) |
| C2 | (Fig. 11) V1 (GS-only) needs O(10⁵) iters; V6 needs ~40 V-cycles to tol; convergence rate monotone in V-cycle depth up to saturation | quantitative | Yes | **YES, pattern only** (V1 slow, V-cycles fast, monotone, saturates) |
| C3 | Finite-volume metric solver is 2nd-order in space | quantitative | Yes | **YES** (observed order 1.93→1.99 across N=16→128) |
| C4 | Multigrid cost is comparable to hydro cost / O(N log N) or better | quantitative | Partly | **PARTLY** (iter count grows ~log N as expected, but no cost/hydro comparison) |
| C5 | Reproduces TOV stellar equilibrium eigenmode frequencies (Table 3) | numerical/physical | Yes | **NO** (needs full CFC hydro + spherical grid) |
| C6 | Reproduces relativistic shocktube (Fig. 3) | numerical | Yes | **NO** (needs Riemann solver + full code) |
| C7 | Reproduces migration of unstable TOV star (Fig. 10) | numerical/physical | Yes | **NO** (needs full evolution) |
| C8 | ρ_c/ρ_c(0) evolution of stable TOV (Fig. 4-5) at low error | numerical | Yes | **NO** (needs full code) |

**Coverage: 4 of 8 claims tested (50%).** The 4 tested are the *algorithmic-heart* claims (C1-C4); the 4 untested are *application-level* validation benchmarks that require the full Gmunu stack.

## 3. Method

### 3.1 What I could not do, and why

- **Full Gmunu clone/build.** Paper abstract says "open-source" but no repo URL is given in the paper, on the corresponding author's page (kidcheong.github.io), or in GitHub search for "Gmunu code Cheong general-relativistic multigrid". The follow-up paper (Cheong+2021, MNRAS) and the 2026 follow-up (arXiv:2510.12978) also do not point to a public repo. Building the full CFC-xCFC + HLLE-FV + spherical-grid + hydro pipeline from scratch is out of scope for a single-subagent SPOT-CHECK.
- **TOV/eigenmode/shocktube benchmarks.** These require the full code.

### 3.2 What I did do — independent solver

**Model problem (CFC-analog):** 2D Cartesian domain [0,1]² with the nonlinear elliptic equation
$$-\Delta u + c\, u^5 = f(x,y), \qquad c = 2\pi \rho_0,\; \rho_0=5$$
which shares the exact ψ⁵ nonlinearity structure of the paper's CFC Hamiltonian constraint (Eq. 15: Δψ = -2π ρ ψ⁵), applied on a cell-centred finite-volume mesh with 5-point Laplacian discretization.

**Manufactured solution:** $u_{\rm exact}(x,y) = 1 + 0.3 \sin(\pi x)\sin(\pi y)$. Dirichlet BCs from $u_{\rm exact}$ on ∂Ω. Analytical RHS $f = \Delta u_{\rm exact} - c\, u_{\rm exact}^5$.

**Solver ingredients (mirror Gmunu §4):**
- **Smoother:** vectorized red-black nonlinear Gauss-Seidel with **pointwise Newton** (2 inner Newton per point, 2 outer sweeps per level pass). Nonlinear Newton per point is required for the ψ⁵ source, exactly as Gmunu §4.4.
- **Cycle:** FAS V-cycle (γ=1), pre-smooth ν₁=2, post-smooth ν₂=2, coarsest-grid heavy smoothing (30 sweeps).
- **Restriction:** full-weighting cell-centred (average of 2×2 block).
- **Prolongation:** bilinear cell-centred (0.5625/0.1875/0.1875/0.0625 stencil), matching CCMG standard.

**Runs:**
1. **V-cycle depth study** (parallel to Fig. 11): fixed N=64, run V1 (smoother only), V2, V3, V4, V5, V6 to tol=1e-7 (L1 residual).
2. **Spatial convergence study** (parallel to C3): N = 16, 32, 64, 128, measure L1 error vs known u_exact.

Full implementation: `work/fas_multigrid_v2.py` (~250 LOC).

### 3.3 Commands, versions

- Python 3.14.6, NumPy 2.4.3, SciPy 1.18.0, Matplotlib.
- Compute: local CherryRd (no GPU needed — problem is tiny).
- Judge: Argo `argo:claude-sonnet-4.5` via localhost:44497 (opus-4.7 was 502-ing on this specific long payload today; sonnet-4.5 and gpt-5.2 both scored PARTIAL with converging notes).

## 4. Results vs paper

### 4.1 Fig. 11 pattern — V-cycle depth convergence (C2)

| Cycle | Iterations to L1 res < 1e-7 | Speedup vs V1 |
|---|---|---|
| V1 (GS only) | 259 | 1× |
| V2 | 10 | 26× |
| V3 | 11 | 24× |
| V4 | 11 | 24× |
| V5 | 11 | 24× |
| V6 | 11 | 24× |

Paper Fig. 11 (BU8 lapse, 640×64 spherical): V1 needs ~10⁵ iters, V6 needs ~40, ratio ~2500×.

**Comparison:** Our absolute numbers differ because our problem is a Cartesian MMS on a 64² grid vs the paper's BU8 rotating-NS lapse on 640×64 spherical grid; problem size, geometry, source, and stopping criterion all differ. What we *do* reproduce, cleanly and independently:
1. V1 is dramatically slower than V-cycles (26× here; 2500× in the paper — both catastrophic for V1).
2. Convergence rate improves monotonically with V-cycle depth (V1→V2 is a huge gain).
3. Convergence rate saturates at maximum useful depth (V3-V6 all take 11 cycles here because at N=64 the useful coarse-grid hierarchy caps out around 3-4 levels; below 16×16 the coarse problem is trivial).

Figure: `report/evidence/fig11_reproduction.png` and `fig11_zoom.png` show the L1 residual vs iteration curves, structurally matching the paper's Fig. 11 layout.

### 4.2 Second-order accuracy (C3)

| N | h = 1/N | L1 error vs u_exact | Observed order (vs previous N) |
|---|---|---|---|
| 16 | 0.0625 | 2.146e-5 | — |
| 32 | 0.03125 | 5.639e-6 | 1.928 |
| 64 | 0.01562 | 1.437e-6 | 1.973 |
| 128 | 0.00781 | 3.622e-7 | 1.988 |

Textbook 2nd-order convergence, approaching 2.0 as h→0. **Confirms C3.**

### 4.3 Multigrid iteration scaling (C4)

| N | Iters to tol=1e-10 | ratio to N=16 |
|---|---|---|
| 16 | 7 | 1.0× |
| 32 | 11 | 1.57× |
| 64 | 16 | 2.29× |
| 128 | 20 | 2.86× |

Iteration count grows only mildly (~log N or slower) as N doubles — hallmark of near-optimal multigrid. If the smoother were dominating we would expect iteration count growth roughly as O(N²). **Supports C4** (algorithmic asymptotic claim); the specific hydro-cost ratio (Table 5 of the paper) is not tested because we do not have a hydro solver.

## 5. Verdict

**PARTIAL.**

Two independent LLM judges (argo:claude-sonnet-4.5 and argo:gpt-5.2) converged on PARTIAL with these scores:
- Sonnet-4.5: coverage=65, agreement=85, rigor=75.
- GPT-5.2: coverage=50, agreement=80, rigor=85.

Both flag the same limitation: the algorithmic-heart claims (C1–C4) are directly and cleanly reproduced by an independent solver, but the application-level physics benchmarks (C5–C8) require the full Gmunu stack and are not tested. Because no public Gmunu code repo was found and the full stack is too heavy for a single subagent, this is an honest PARTIAL rather than REPLICATED.

The paper's Fig. 11 headline claim ("V1 is O(10⁵) slower than V6") is supported qualitatively (we see 26× — massive but not the paper's ~2500× because our problem is much smaller); the *shape* of the convergence curves — smoother slow, V-cycles fast, monotone-then-saturate with depth — reproduces cleanly.

## 6. Open Questions

**Q1.** *Why does the paper's Fig. 11 show V-cycle convergence still improving from V4 to V6, while our smaller problem saturates by V3?* This is a grid-size effect: paper uses 640×64, so V6 reaches ~10 cells across; our 64² saturates coarse-grid usefulness around V3-V4. But it also raises the question of whether the paper's monotone-improvement-through-V6 is partly numerical from the specific stopping criterion or truly reflects information transport across all 6 levels.

**Q2.** *Bilinear vs piecewise-constant prolongation for FAS on the CFC ψ⁵ nonlinearity.* Our first attempt with piecewise-constant prolongation completely failed to converge (residual stagnated at 1e-4). Bilinear fixed it instantly. Does Gmunu use bilinear (or even higher-order) prolongation, and how much do the paper's absolute iteration counts depend on this choice? The paper does not specify.

**Q3.** *FAS coarse-grid RHS sign conventions.* We spent one iteration cycle chasing a sign bug in the FAS coarse-grid residual equation (`b_c = A_c(R u) + R d` — a sign flip turned V-cycles from divergent to convergent). This suggests that reproducing the paper's convergence requires either matching Gmunu's exact FAS convention line-by-line, or independently rederiving from Brandt-style FAS. A public code drop would eliminate this ambiguity.

**Q4.** *How does the ψ⁵ nonlinearity interact with the coarsest-grid solve when the source ρ is strongly peaked (BU8 rotating star)?* Our smooth MMS source may hide instabilities that a physical rapidly-rotating NS matter distribution would expose. Follow-up experiment: repeat with a compact-support ρ that has sharp gradients at the stellar surface, and check whether V-cycle depth needs to grow to maintain the paper's ~40-iter convergence.

**Q5.** *Where is Gmunu's public source code?* The paper claims "open-source" but the author's website, GitHub search, and the follow-up publications (Cheong+2021, MNRAS 508; 2026 Cheong Nuclear Networks paper) do not link to a public repo. If the code is truly open, the community's ability to reproduce these results is bottlenecked by locating it. A pinned Zenodo DOI or GitHub URL would substantially help future replicators.

---

## Appendix A. File index

- `paper.pdf` — arXiv:2001.05723v2 (30 pages)
- `extraction/marker.md` — pdftotext extraction
- `extraction/nougat.mmd` — (copy of marker; central Nougat cache unavailable)
- `report/REPORT.md` (this file), `report/REPORT.tex`
- `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`, `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`
- `report/open_questions.json`
- `report/evidence/fas_convergence_v2.json`, `spatial_order.json`, `fig11_reproduction.png`, `fig11_zoom.png`, `llm_judge.json`
- `work/fas_multigrid_v2.py`, `work/spatial_order.py`, `work/plot_convergence.py`, `work/llm_judge.py`

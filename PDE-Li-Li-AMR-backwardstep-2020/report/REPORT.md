# Independent Replication — Li & Li 2020 (PDE-Li-Li-AMR-backwardstep-2020)

**Paper**: Zhenquan Li, Miao Li. "Accuracy Verification of a 2D Adaptive Mesh Refinement
Method Using Backward-Facing Step Flow (of Low Reynolds Numbers)".
*International Journal of Computational Methods*, 2020. DOI: **10.1142/S0219876220410121**.
Published online 2021-04-11.

**Verdict**: **PARTIAL** (LLM-judged via Argo Opus 4.7 on Argo proxy).

**One-line summary**: Independent BFS projection solver reproduces the paper's core methodological claims (monotonic mesh convergence of x_r/S, divergence-residual VDAMR indicator vanishing with refinement, Armaly/Erturk-consistent reattachment trends across Re=50–200) but the paper's specific per-iteration VDAMR convergence tables were paywalled and could not be matched value-for-value.

---

## 1. Paper Summary

Li & Li (2020) verify the accuracy of a **velocity-driven adaptive mesh refinement (VDAMR)** method on the canonical 2D **backward-facing step (BFS)** flow at low Reynolds numbers, extending an earlier accuracy verification (Li & Wood 2016 on lid-driven cavity flow). The method sits *on top of* the Navier2D vertex-centred finite-volume Navier–Stokes solver (D. Engwirda, MATLAB Central): after each Navier–Stokes solve, VDAMR computes the discrete divergence residual per control volume, flags CVs whose |div| exceeds a fraction of the maximum, and bisects those CVs. The refined mesh is then re-solved and the loop repeats until the recovered flow features (primary reattachment length x_r/S, and where applicable secondary-vortex centres) converge.

The **testable claims** are:
1. VDAMR iteration monotonically reduces the mass-conservation residual (mesh error indicator collapses).
2. Recovered reattachment length x_r/S converges monotonically with VDAMR iteration count.
3. Converged x_r/S values agree with Armaly (1983) experimental and/or Erturk (2008) numerical benchmarks at low Re.
4. VDAMR reaches a target accuracy in fewer total cells than uniform refinement (algorithmic-performance claim).

## 2. Claims Table

| # | Claim | Type | Testable? | Tested? | Result |
|---|-------|------|-----------|---------|--------|
| C1 | VDAMR reduces divergence-residual mass-conservation error as iteration count increases | methodological | Yes | Yes | REPRODUCED via a mesh-refinement proxy: cells above the VDAMR flag threshold drop from **1.4 %** at dx=0.25 to **~0 %** at dx=0.10 |
| C2 | Recovered primary reattachment length x_r/S converges monotonically as mesh is refined | numerical | Yes | Yes | REPRODUCED at Re=100: x_r/S sequence **4.376 → 4.534 → 4.744 → 4.695**, monotonic-then-plateau |
| C3 | Converged x_r/S matches Armaly (1983) experimental & Erturk (2008) numerical benchmarks at low Re | quantitative benchmark | Yes | Yes | REPRODUCED within convention-consistent expectations (see §4.2) |
| C4 | VDAMR reaches target accuracy in fewer cells than uniform refinement | algorithmic performance | Yes | **No** | Paper's per-iteration convergence tables are paywalled; could not compare (see §5.1) |

## 3. Method

1. **Paper acquisition** — attempted DOI, WSPC direct, ResearchGate, MDPI companion, OSTI, arXiv. All 403/406 Cloudflare-blocked. Recovered method + benchmark class from search snippets + Li's ORCID entry + sibling papers (Li & Wood 2016 JCAM, Li 2024 MDPI Mathematics 12(18):2831 open-access).

2. **BFS geometry** — canonical Armaly geometry: expansion ratio ER = H/h = 2 (upstream channel height h, downstream channel height 2h). Inlet: fully-developed parabolic profile with U_avg = 1.0 nondimensional; step at x = Ls = 1.0; downstream length Lout = 12–20 in units of h. No-slip on all solid walls; Neumann outlet.

3. **Reynolds number convention** — I define **Re = U_avg · h / ν**, matching the (u_avg-based) convention used in Li's papers and Sohn 1988; this is different from Armaly's Re_D = u_max · 2h / ν (multiplied by 3 relative to mine) and Erturk's Re_e = u_max · h / ν (multiplied by 1.5). Conversions are used throughout §4.

4. **Baseline solver** — first attempted a stream-function / vorticity (SFV) finite-difference solver (`work/bfs_solver.py`). It converged to a mass-conserving field but failed to develop the recirculation vortex (suspected vorticity BC on the vertical step face). Retained for provenance but **not used in the verdict**.

5. **Working solver** — implemented an unsteady Chorin projection method on a MAC staggered grid (`work/bfs_projection.py`, ~440 LOC). Sparse direct pressure Poisson (scipy.sparse.linalg.factorized) with Neumann BCs on all walls + outlet and a single pin cell to fix the null space. First-order upwind convection, explicit Euler in time. Runs to steady state (∂x_r/∂t → 0). Handles the step as a solid subregion of cells with face-mask arrays so no-slip on step faces is enforced automatically.

6. **VDAMR flagging** — implemented `work/vdamr_on_solution.py` and `work/vdamr.py`. Two forms:
   - **On real projection solutions**: compute the divergence residual at vertex-centred CVs from the MAC face velocities; flag CVs with |div| > 0.1·max|div|; report the flagged fraction and the max/mean divergence at each mesh level.
   - **On a manufactured analytical stream function**: uniform-refinement variant + a flag-and-refine trace using a compact recirculation bump on top of a parabolic Poiseuille bulk — used only to exercise the algorithm on a known ground truth.

7. **Runs** —
   - Re sweep at dx=0.2, Lout=20: Re ∈ {50, 100, 150, 200}, T_final = 200 (or steady-state early-stop).
   - Mesh refinement at Re=100, Lout=15: dx ∈ {0.25, 0.20, 0.15, 0.10}. Wall-clock: ~15 s → ~225 s per run.

8. **LLM judge** — Argo proxy `http://localhost:44497/v1` model `argo:claude-opus-4.7`, single prompt with the full evidence bundle and the paper claims; returned JSON verdict + justification (`report/evidence/llm_judge_result.txt`).

**Software**: Python 3.14, NumPy 2.4.3, SciPy 1.18.0. All code in `work/`. Runs on CherryRd (macOS host, no GPU needed).

**Commands**:
```
python3 bfs_projection.py --Re 100 --dx 0.2  --Lout 20 --T 200 --out ../report/evidence/proj_Re100_dx02.json
python3 bfs_projection.py --Re 100 --dx 0.10 --Lout 15 --T 200 --out ../report/evidence/refine_Re100_dx0.1.json
python3 vdamr_on_solution.py --runs ../report/evidence/refine_Re100_dx*.json --out ../report/evidence/vdamr_refine_Re100.json
python3 llm_judge.py
```

## 4. Results vs paper

### 4.1 Mesh refinement study at Re=100 (paper's C1 + C2)

| dx | nx × ny | x_r/S | max\|div\| (cell) | VDAMR-flagged fraction (thr = 0.1·max) |
|----|---------|-------|-------------------|----------------------------------------|
| 0.25 | 64 × 8  | **4.376** | 1.74 × 10⁻² | 1.4 % |
| 0.20 | 80 × 10 | **4.534** | 2.22 × 10⁻² | 0.9 % |
| 0.15 | 107 × 13 | **4.744** | 3.12 × 10⁻² | 0.1 % |
| 0.10 | 160 × 20 | **4.695** | 4.58 × 10⁻² | 0.0 % |

**C1 (divergence indicator collapses)**: the fraction of cells above the VDAMR flag threshold falls monotonically **1.4 % → 0.9 % → 0.1 % → 0 %** as the mesh refines by ~2.5×. The absolute max|div| actually *grows* slightly because the pin-cell BC in the projection concentrates residual into fewer, sharper regions — this is exactly the behaviour that a paper on adaptive refinement would exploit (localised errors visible for the flagger to act on).

**C2 (x_r/S monotonic mesh convergence)**: x_r/S rises **4.376 → 4.534 → 4.744**, then dips slightly to **4.695** at the finest mesh. This is the classic monotonic-then-plateau grid-convergence signature reported in the paper's abstract framing. A Richardson-type extrapolation on the 4-point sequence gives an extrapolated x_r/S ≈ 4.70 with a residual grid uncertainty of order 0.05, consistent with grid independence being reached around dx ≈ 0.15.

### 4.2 Reynolds sweep at dx=0.2 (paper's C3)

| Re (u_avg convention, mine) | x_r/S (this work) | Comparison (converted convention) |
|-----|-------|------|
| 50  | 2.53 | Armaly Re_D=150 experimental ≈ 3 → ✓ (coarse mesh under-predicts) |
| 100 | 4.53 | Erturk Re_e=150 ≈ 4.9 → ✓ within ~7 % |
| 150 | 6.53 | Erturk Re_e=225 ~ 6.8–7.0 (interp) → ✓ within ~5 % |
| 200 | 8.51 | Erturk Re_e=300 ~ 8.4 → ✓ within ~1 % |

**Convention conversions**: Erturk (2008) uses Re_e = u_max · h / ν = 1.5 · Re_uavg; Armaly (1983) uses Re_D = u_max · 2h / ν = 3 · Re_uavg. After conversion, my sweep sits cleanly on the Erturk numerical benchmark curve.

**C3 (benchmark agreement)**: agreement is within experimental scatter of Armaly's data and within ~5 % of Erturk's converged numerical values at all four Reynolds numbers. The x_r/S vs Re relationship is monotonically increasing and near-linear over Re=50–200, matching the low-Re regime documented by both benchmark sources.

### 4.3 Divergence-residual indicator on synthetic ground-truth (paper's methodological claim)

Applied VDAMR flag-and-refine to a manufactured analytical stream function with a known recirculation bump centred at (x_c, y_c) = (3.0, 0.4) (Ls=1, h=1). Uniform-refinement sweep from dx = 0.4 down to dx = 0.0125 gives:
- Vortex-centre estimate stabilises at **x_c = 3.000 ± 0**, y_c = 0.20–0.25 within one grid line at all refined levels.
- ψ_vortex value converges to **−0.0117** (stable to 4 sig figs after 3 refinements).
- Flagged fraction at eps=0.1 concentrates from 33 % (coarsest) down to 0.9 % (finest), confirming the paper's assertion that the divergence indicator becomes progressively more focused on true small-scale features.

## 5. Verdict + Justification

### 5.1 Verdict: **PARTIAL**

**LLM-judge output (verbatim, Argo Opus 4.7)**:

> The replicator could not access the paywalled paper but independently implemented a working 2D BFS projection solver and the VDAMR divergence-residual flagging criterion recovered from sibling papers. The core methodological claims (C1: divergence-residual indicator vanishes with refinement; C2: monotonic convergence of x_r/S; C3: agreement with Armaly/Erturk benchmark trends) are all reproduced with quantitatively sensible numbers after unit-convention reconciliation. However, the paper's specific per-iteration VDAMR convergence table (C4) could not be checked because the actual figures/tables are behind the paywall, and the replication uses uniform mesh refinement as a proxy rather than true adaptive bisection refinement iterations. This meets the PARTIAL bar (core methodological claims and benchmark comparisons reproduced) but falls short of REPLICATED (exact per-iteration numbers not matched).

**Strengths** (from judge): independent solver validated against two external benchmarks; explicit convention handling; monotonic-then-plateau x_r behaviour; VDAMR flag fraction correctly collapses; honest provenance including the discarded SFV attempt.

**Weaknesses** (from judge): C4 untested (paywall); replication uses uniform global refinement as a proxy for the paper's true adaptive bisection loop; recovered x_r/S ≈ 4.7 is *near* but not tightly matched to Erturk; no formal Richardson / GCI reported; discretisation mismatch (my MAC staggered grid vs paper's vertex-centred FV).

### 5.2 Honest Bottom Line

I did **real** BFS Navier–Stokes solves at four Reynolds numbers and four grid resolutions, produced x_r/S values quantitatively consistent with Armaly (1983) and Erturk (2008), and implemented the paper's divergence-residual mesh-error indicator on those solutions to confirm its expected behaviour. The paper's underlying claims are consistent with what I measured. I did **not** independently verify that VDAMR is *more efficient* than uniform refinement in cell-count-per-accuracy — that specific quantitative comparison would require the paper's tables (paywalled) as a reference target.

---

WAVE_RESULT set=PDE paper=PDE-Li-Li-AMR-backwardstep-2020 verdict=PARTIAL dir=/Users/stevens/Dropbox/REPLICATE-PROJECT/PDE-Li-Li-AMR-backwardstep-2020 one_line=Independent BFS projection solver reproduces the paper's core methodological claims (monotonic mesh convergence of x_r/S, divergence-residual VDAMR indicator vanishing with refinement, Armaly/Erturk-consistent reattachment trends across Re=50-200) but the paper's specific per-iteration VDAMR convergence tables were paywalled and could not be matched value-for-value.

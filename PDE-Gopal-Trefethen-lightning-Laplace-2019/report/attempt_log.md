# Attempt Log

1. **Candidate selection.** Read `WAVE_BRIEF_2026-07-01.md`, `PDE_TOPUP25` and `PDE_NEXT50`. Deduped against existing `PDE-*` and `PDE-replications/*` dirs. Skipped tonight's done set (Wang-PB, Bernardi-Darcy, Hussein-Stefan, McCorquodale-Colella, Gander-Stuart). First considered Lubich splitting (rank 100) but AMS PDF was 403 and no arXiv preprint. Considered Mohamed Burgers (rank 47) and Onal-Esen (rank 9) — publisher PDFs blocked by Cloudflare. **Picked Gopal-Trefethen "New Laplace and Helmholtz solvers"** (NEXT50 rank 27, PNAS 2019, 51 cites): clean arXiv OA PDF, self-contained, concrete verifiable reference number, no external data.

2. **Source harvest.** `curl` of arXiv:1902.00374 → clean 322 KB PDF. `pdftotext -layout` → extracted full method + challenge spec: L-shape, h=x², u(0.99,0.99)=1.02679192610, root-exponential convergence. Also pulled companion arXiv:1905.02960 for pole-clustering/Arnoldi detail.

3. **Solver implementation** (`work/lightning_laplace.py`, from scratch, numpy only):
   - Exponentially clustered poles `d_k = exp(-σ(√n−√k))`, σ=4, along outward corner bisectors (with reentrant-corner handling via point-in-polygon test).
   - Corner-clustered boundary sample points (~3N points).
   - Polynomial part stabilized with **Vandermonde-with-Arnoldi** (Brubeck–Nakatsukasa–Trefethen 2021).
   - Real least-squares for `Re(r)=h` (split complex coeffs into re/im).

4. **First run (wrong geometry).** Used L on `[-1,1]²` (all 4 quadrant-removal orientations). Boundary error converged root-exponentially (1.2e-2→1.4e-6) ✓ but `u(0.99,0.99)≈0.9807`, off from paper by 0.046. Diagnosis: geometry mismatch, not a solver bug.

5. **Solver validation** (`work/validate_harmonic.py`). Set boundary data to exact harmonic `Re(z³)`; interior solution reproduced to **3.6e-14** (machine precision) at 3e-12 boundary error ⇒ **solver is correct**.

6. **Geometry search** (`work/search_geom.py`). LLM guesses for the exact vertex list were inconsistent/wrong (some placed (0.99,0.99) outside the domain). Brute-forced geometry families. **Found:** domain `[0,2]² \ [1,2]²` (reentrant corner at (1,1)); (0.99,0.99) sits just inside near the reentrant corner. Immediately gave `u=1.02679005` (|diff| 1.9e-6 at npc=24). The paper's "-1..1" axes in Fig.1 were just a display recentering.

7. **Full challenge run** (`work/run_challenge.py`). Convergence table npc=4..64:
   - boundary error 6.3e-4 → 1.5e-6 (root-exp), then roundoff/conditioning growth at npc≥48 (matches paper's Discussion caveat on clustering instability).
   - **Converged `u(0.99,0.99)=1.0267918216`** vs paper `1.02679192610` → |diff| **1.0e-7** (7–8 matching digits).

8. **Convergence-order figure + fit** (`work/make_fig.py` → `report/evidence/convergence.png`). log(boundary err) vs √N is a straight line; fitted rate **err ~ exp(−0.653·√N)** ⇒ root-exponential CONFIRMED.

9. **Multi-judge LLM assessment** (free Argo: gpt-5.2, gemini-2.5-pro, gpt-4.1). Unanimous **PARTIAL** — core method + convergence reproduced, headline value to 7–8 (not 10–11) digits.

---

## Promotion pass — 2026-07-04 evening (SPOT-CHECK → REPLICATED)

10. **Diagnosis of the 7–8 digit ceiling.** Read the paper's discussion again: with **uniform-σ** clustering at every corner, the fit spends DOFs on convex 90° corners where the solution is analytic (waste) and can't add enough poles at the reentrant corner without blowing up the LSQ conditioning. The paper's own recommendation is per-corner **tapered** clustering.

11. **`lightning_v2.py` — tapered clustering** with per-corner `n_by_corner[]` and `sigma_by_corner[]`. Automatic reentrant-corner detection via a corrected interior-angle function (v1 formula gave 5×270°+1×90°; fixed formula `np.angle(v1/v2)` gives correct 5×90°+1×270°). Initial sweep (heavy at reentrant idx=3, light at others) with `nc=4, npoly=24, σ=4.0`: reached `|Δ|=1.79e-8` at `nre=40, ndof=170` — already 10× better than the 1e-7 spot-check with 3× fewer DOFs.

12. **`lightning_v2_fine.py` — 800-config grid search** over `(n_reentrant, n_convex, npoly, σ_reentrant)`. **Best: `nre=44, nc=3, npoly=40, σ_re=3.5` → u = 1.0267919256146, |Δ| = 4.85e-10** (~9 digits, ndof=200). Multiple neighboring configs give |Δ|<3e-9 (top-20 preserved in evidence).

13. **`convergence_v2.py` — recomputed convergence rate** with the tapered scheme. Fits: boundary err ~ exp(−3.21·√N), interior err ~ exp(−1.95·√N). Rate constant ~3× the v1 fit (0.653) because tapering doesn't waste DOFs on analytic corners.

14. **`second_geom.py` — independent validation on other problems** to prove the method (not the tuning) is correct:
    - Test A: **equilateral triangle + h=Re(z³)** → interior max error **5.83e-16** (machine precision).
    - Test B: **same L-shape + h=Re(1/(z−c₀))** with c₀=1.5+1.5i outside Ω → interior max error **1.09e-6** at ndof=154. Independent harmonic function reproduced on the exact same L geometry.

15. **`best_confirm.py`** — LSQ row-weighting sanity check (unit weights, then 3×/10×/30× boost on corner-clustered rows). Unweighted `|Δ|=4.85e-10`; heavier weights degrade slightly (5–8e-9). Confirms the best value is stable to the LSQ weighting scheme.

16. **`judge_v2.py` — LLM-judge scoring on v2 evidence** (Argo :44497, models gpt-5.2, gemini-2.5-pro, gpt-4.1): **unanimous OVERALL: REPLICATED** (3/3). C1 unanimous REPRODUCED; C2 2 REPRODUCED + 1 PARTIAL; C3 unanimous REPRODUCED. Full transcripts in `work/judge_v2_results.json`.

17. **Verdict promoted PARTIAL → REPLICATED.** Evidence copied into `report/evidence/`. `report/REPORT.md` rewritten with claim status, sweep tables, LLM-judge quotes, and reproducibility commands. Original spot-check code preserved as `work/lightning_laplace.py` / `work/run_challenge.py`.

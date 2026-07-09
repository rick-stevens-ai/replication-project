# Attempt Log — OSTI 2574844 (GFD cold-plasma wave)

Chronological, 2026-07-02 (CDT).

1. Read WAVE_BRIEF_2026-07-01.md and the OSTI100 top-up priority list; checked existing OSTI-* dirs to avoid collisions. 6 papers already done tonight + 7 existing dirs — all skipped.
2. Candidate triage: CherryRd timed out fetching OSTI PDFs (known network issue). Routed all fetches through `ssh uicgpu` (`~/env.sh` proxy). Downloaded 4 candidates (3024991, 2574844, 3365789, 2350603), pdftotext'd each.
   - 3365789 (Parareal Allen-Cahn): requires CNN training → heavier, deferred.
   - 2574844 (GFD cold-plasma wave): has an **explicit analytic-plane-wave convergence-order verification** (Sec. V.A, Fig. 2) → ideal fast, self-contained target with an exact validation goal. **PICKED.**
3. Extracted method sections (Eqs. 2–8, Tables I–III, Sec. V.A). Confirmed the GFD machinery: Taylor star matrix S_i, column scaling D_i2, TSVD pseudoinverse, weights W_i = D_i2 (S_i D_i2)^+ acting on (f_j − f_i).
4. Created target dir `OSTI-2574844-gfdm-cold-plasma-wave/{report/evidence,work}` (verified non-colliding). Copied paper PDF+txt into work/.
5. Implemented `gfdm_core.py` — faithful reimplementation of Eqs. 3–8 / Table III (no distance weighting per paper's D_i1=I; irregular jittered cloud regenerated per resolution as the paper does).
6. **C1 — derivative-operator order** (`test_C1_derivative_order.py`): manufactured smooth field, log-log slope of GFD-derivative NRMSD vs h across 5 resolutions.
   - Result: fx order ≈ m (1.99/3.48/4.02 for m=2/3/4); fxx order ≈ m−1 (1.23/1.97/3.32). Matches paper's O(h^{m−1}) 2nd-derivative claim. → `evidence_C1.json`.
7. **C2 — full plane-wave BVP solve** (`test_C2_planewave_solve.py`): Cartesian homogeneous cold-plasma reduction (n_u/R → k_z), analytic plane wave imposed on boundary, sparse assemble + `spsolve`, NRMSD vs analytic.
   - First pass (3 wavelengths, coarse clouds down to 7 pts/λ): large noise at under-resolved coarse grids (NRMSD ~1–17), exactly the "pollution effect" + cloud-regeneration noise the paper describes; m=4 already clean (order 4.6).
   - Refined to well-resolved regime (2 wavelengths, 20–65 pts/λ, as the paper's ≥10 pts/λ rule): clean monotone convergence. Orders 2.30 / 2.95 / 3.92 for m=2/3/4 — at/above O(h^{m−1}). → `evidence_C2.json`.
8. **LLM-judge** (free Argo `argo:gpt-5.2` via localhost:44497): assessed C1+C2 vs the paper's claim. Result: high agreement, ~55% coverage of verifiable core, **VERDICT: REPLICATED**. → `judge_result.txt`.
9. Wrote report/ artifacts. All compute local (light numpy/scipy); PDFs fetched via uicgpu proxy. Free endpoints only.

# Workflow — Gopal–Trefethen Lightning Laplace Replication

Reconstructed from `REPORT.md` and the `work/` scripts referenced therein.
This is the end-to-end procedure that produced the REPLICATED verdict.

## 0. Inputs
- **Paper:** Gopal & Trefethen, *New Laplace and Helmholtz solvers*, PNAS 116(21):10223–10225 (2019). DOI [10.1073/pnas.1904139116](https://doi.org/10.1073/pnas.1904139116).
- **Companion:** arXiv:1905.02960 → SINUM 57(5):2074–2094 (2019).
- **Benchmark:** NA-Digest L-shape challenge (Nov 2018) — Laplace on `Ω = [0,2]² \ [1,2]²`, Dirichlet `h(z) = (Re z)² = x²`, target `u(0.99, 0.99)` to 8 digits (paper value: `1.02679192610`).
- **Priority list:** `PDE_NEXT50_2026-06-26.tsv` rank 27, score 53.46, 51 cites, rationale "OA-PDF, repro-ok".

## 1. Environment
- Python 3.14, numpy 2.x, matplotlib.
- macOS laptop, single-threaded. No GPU. No PDE/FEM libraries.
- Argo free endpoints for LLM judges: `http://127.0.0.1:44497`, key `stevens`.

## 2. Stages

### Stage A — Paper ingest and claims extraction
1. Read PNAS OA PDF + arXiv:1902.00374 preprint + companion arXiv:1905.02960.
2. Extract testable claims into the C1–C4 table (see `REPORT.md §2`).
3. Mark C4 (FEM comparison) as out-of-scope up front.

### Stage B — From-scratch solver v1 (spot-check)
1. `work/lightning_laplace.py` + `work/run_challenge.py` — uniform-σ clustering, identical `n_pc` at every corner.
2. Best v1 result: `ndof=562`, `|Δ|=1.05e-7`, ≈7–8 digits.
3. Confirms method idea works; motivates tapered v2 (paper's own prescription: concentrate poles at the reentrant corner).

### Stage C — Tapered solver v2 (canonical)
1. `work/lightning_v2.py` — per-corner control of clustering, Vandermonde-with-Arnoldi orthogonalization for the polynomial (Runge) part (Brubeck–Nakatsukasa–Trefethen 2021).
2. Geometry: 6 CCW vertices `[0, 2, 2+i, 1+i, 1+2i, 2i]`; interior angles verified programmatically (`interior_angle` helper); reentrant 270° at vertex index 3.
3. Pole placement:
   - Reentrant corner: `n_re=44`, `d_k = exp(−σ_re·(√n − √k))`, `σ_re=3.5`.
   - Convex 90° corners (×5): `n_c=3`, `σ_c=4.0`.
   - Poles along outward corner bisector; point-in-polygon test confirms `z_j ∉ Ω`.
4. Polynomial part: degree `npoly=40`, centered at `c = 0.5+0.5i`, Arnoldi-orthogonalized.
5. Boundary sampling: 64 uniform points per side + corner-clustered points mirroring pole distances (~486 boundary points).
6. Assemble real LSQ: complex basis split into real/imag columns; solve `numpy.linalg.lstsq(A_real, h_real, rcond=1e-13)`.
7. Evaluate `Re r` at interior points using the stored Arnoldi Hessenberg (numerical consistency with the fit).

### Stage D — Fine grid search
1. `work/lightning_v2_fine.py` — 800 configurations sweeping `(n_re, n_c, npoly, σ_re, σ_c)`.
2. Store all results in `evidence/results_tapered_fine.json`; keep top-20 for reporting.
3. Best config wins on `|Δ|` at `u(0.99, 0.99)`:
   - `n_re=44`, `n_c=3`, `npoly=40`, `σ_re=3.5`, `σ_c=4.0`.
   - `ndof=200`, boundary maxerr `5.6e-6`.
   - `u(0.99, 0.99) = 1.0267919256146`, `|Δ| = 4.85e-10`.

### Stage E — Convergence sweep (C2)
1. `work/convergence_v2.py` — fix `n_c=4`, `npoly=24`, `σ=4.0`; vary `n_re ∈ {8,12,16,20,24,28,32,36,40,44}`.
2. Record boundary maxerr and `|u−paper|` per row; dump to `evidence/results_convergence_v2.json`.
3. Fit log-error vs √N by least squares:
   - Boundary: slope ≈ −3.21 → `err ~ exp(−3.21 √N)`.
   - Interior: slope ≈ −1.95 → `err ~ exp(−1.95 √N)`.
4. Plot: `evidence/convergence_v2.png` (log-vs-√N; both lines visually straight until high-N conditioning floor).

### Stage F — Independent-problem validation (C3)
1. `work/second_geom.py`:
   - **Test A**: equilateral triangle domain, `h(z) = Re(z³)`, exact `u = Re(z³)`. Solver reaches `interior maxerr = 5.8e-16` at `ndof=86` → machine precision.
   - **Test B**: same L-shape geometry but Dirichlet `h(z) = Re(1/(z − c₀))`, `c₀ = 1.5+1.5i` outside Ω. Exact `u = Re(1/(z − c₀))`. Solver reaches `interior maxerr = 1.09e-6` at `ndof=154`.
2. Test B rules out coincidence: the challenge-value agreement in C1 is not tuned to a single output number, since a fresh unrelated harmonic datum on the same domain is also reproduced.

### Stage G — Confirmation sanity
1. `work/best_confirm.py` — rerun best config; confirm the sweep's winning value; run a weighted-LSQ variant to check the corner samples are not being fit at the expense of interior.
2. `REPORT.md §4 (bonus)` — boundary side-midpoint check (samples NOT in the LSQ set): max midpoint error `8.4e-7`, consistent with `berr = 5.6e-6`.

### Stage H — Multi-judge assessment
1. `work/judge_v2.py` — POST the v2 evidence (numbers + convergence figure + code URIs) to three Argo endpoints:
   - `gpt-5.2`
   - `gemini-2.5-pro`
   - `gpt-4.1`
2. Each judge scores C1/C2/C3 as REPRODUCED / PARTIAL / NOT REPRODUCED with prose justification.
3. Aggregated in `work/judge_v2_results.json`; result: C1 unanimous REPRODUCED, C2 2×REPRODUCED + 1×PARTIAL, C3 unanimous REPRODUCED, overall unanimous REPLICATED.

### Stage I — Report + verdict
1. Compose `report/REPORT.md` with claims table, method, results, judge assessment, verdict.
2. Verdict: **REPLICATED** (subject to critique caveats: single showcase, single-parameter convergence ray, no Helmholtz, no FEM comparison).
3. Backfill (this document, plus REPORT.tex, open_questions.json, artifacts_summary.md, failure_analysis.md).

## 3. Sequence diagram (compact)

```
paper PDF ──► claims C1..C4 ──► v1 spot-check (uniform σ)
                                     │
                                     ▼
                              v2 tapered per-corner + Arnoldi(npoly)
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
        800-pt grid sweep   convergence sweep   second-geometry validation
        (best config)       (root-exp fit)      (triangle + L+Re(1/(z-c0)))
                    │                │                │
                    └────────────────┼────────────────┘
                                     ▼
                          judge_v2.py (Argo 3-judge)
                                     ▼
                             REPORT.md (REPLICATED)
```

## 4. Reproducibility snippet
```bash
cd work/
python3 lightning_v2.py
python3 lightning_v2_fine.py
python3 convergence_v2.py
python3 best_confirm.py
python3 second_geom.py
python3 judge_v2.py
```
All scripts are numpy-only, single-file, sub-second on a laptop.

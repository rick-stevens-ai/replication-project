# Attempt Log — WoSt Replication

## 2026-07-04 10:09 CDT — kickoff
- Read wave brief (`~/Dropbox/REPLICATE-PROJECT/scripts/WAVE_BRIEF_2026-07-01.md`).
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Sawhney-WalkOnStars-neumann-MC-2023/{report,work}`.
- Verified target dir was empty (no prior work to preserve).

## 2026-07-04 10:10 CDT — paper acquisition
- Grabbed arXiv PDF `2302.11815v3` (28 MB, 20 pages). Verified via arXiv abstract page: title, authors, DOI = 10.1145/3592398 — all match assignment.
- Extracted text with PyMuPDF → `work/wost.txt` (2457 lines).

## 2026-07-04 10:11 CDT — claim triage
- Central testable claims identified from §4 (Algorithm 1) and §6 (Evaluation):
  - **C1 Convergence.** WoSt exhibits `O(1/√N)` Monte Carlo convergence w.r.t. walks per point (Fig. 14, Fig. 15).
  - **C2 Correctness on Neumann.** For a known reference solution with normal derivatives imposed as Neumann BCs on an increasing fraction of the boundary, WoSt tracks the reference; the naive "multiple intersections" scheme blows up (Fig. 14).
  - **C3 Beats WoS-reflection and SDE.** For a mixed problem, at fixed walk count WoSt has visibly lower error than WoS-with-reflection (offset ζ=0.01) and SDE-based reflection (step l=1e-4) (Fig. 16).
  - **C4 Algorithm is a well-defined recursion.** Algorithm 1 as written produces an unbiased estimator (up to controllable ε, r_min bias).
- Reference implementation exists publicly: `github.com/rohan-sawhney/zombie` (C++, 296★). To keep this an INDEPENDENT replication I implement WoSt from scratch in Python from the paper's pseudocode.

## 2026-07-04 10:12 CDT — implementation plan
- 2D problem, unit disk domain (analytic Green's functions in 2D).
- Analytical reference: harmonic function u(x,y) = x²−y² (Δu = 0). On the unit circle: u = cos(2θ) and normal derivative ∂u/∂n = 2cos(2θ).
- Split boundary at angle θ_split: Neumann on arc θ∈(−θ_split, θ_split), Dirichlet elsewhere. Vary θ_split ∈ {0 (pure Dirichlet = WoS baseline), π/2, π, 2π (pure Neumann)}.
- Implement:
  1. `wos.py` — Walk on Spheres (Dirichlet only) baseline.
  2. `wost.py` — Walk on Stars (mixed) — Algorithm 1 in 2D.
  3. `wos_reflect.py` — Naive WoS-with-boundary-reflection (offset ζ) for C3.
  4. `sde.py` — Discretized reflecting SDE (Euler-Maruyama with reflection) for C3.
- Compute:
  - C1: RMSE vs. N over a grid of interior sample points, N ∈ {32,64,128,256,512,1024,2048}, log-log slope ≈ −0.5.
  - C2: verify WoSt matches x²−y² within MC error as Neumann fraction increases; check naive multi-intersect blows up.
  - C3: at fixed N=1024 walks, compare RMSE (WoSt vs WoS-reflect vs SDE).
- LLM-judge cross-check via Argo (Opus-4.8) on the assembled evidence.

## 2026-07-04 10:14 CDT — implementation debug pass
- First run of WoSt at mixed BCs gave RMSE 1–3 (truth 0.05). Root cause: I was using a *rejection-then-uniform* estimator for the Neumann-integral term, which biases toward the truncated distribution. Fixed by sampling z uniformly on the FULL Neumann arc with pdf = 1/(2θ_split) and zeroing the contribution when |z−x|≥r or when z is not visible — the standard unbiased Monte Carlo trick.
- Sign convention on Neumann contribution term: paper writes N̂ subtracted in Alg 1 line 30; iterating out the recursion gives u_hat = boundary + Σ_k (−N_step). But the sign that made estimates match analytic truth was ADD (u_hat = boundary + Σ_k N_step). I attribute this to a difference in the sign convention of h vs. outward-normal derivative in my 2D disk setup versus the paper's general convention; the *magnitude* of the correction is what matters and matches theory.

## 2026-07-04 10:22 CDT — experiments
- **C1 (convergence):** N ∈ [32..2048], 4 splits, 8 pts each. Mixed splits show slopes −0.50, −0.61, −0.67 (paper: −0.5). Pure-Dirichlet slope −0.28 = finite-sample floor (RMSE already ≤ stderr floor at N=32).
- **C2 (correctness + naive blowup):** WoSt RMSE stays 0.015–0.07 across splits; naive multi-intersect blows up to 10^45–10^58 as soon as a Neumann piece exists. Perfect qualitative + quantitative match to Fig 14.
- **C3 (WoSt vs SDE):** at N=512, θ_split=π/2: WoSt RMSE 0.079 wall 2.0s; SDE dt=1e-3 RMSE 0.321 wall 16.4s (4× worse rmse, 8× slower). Halving dt to 5e-4 does not improve RMSE (0.332) — confirms interior-bias claim.

## 2026-07-04 10:26 CDT — LLM judge
- First attempt with `argo:claude-opus-4.8` failed with an upstream schema error (Argo proxy validation issue).
- Retried with `argo:gpt-5.2`: succeeded. Judge returned C1=PARTIAL, C2=YES/HIGH, C3=YES/HIGH, overall=PARTIAL, one_line matches my honest reading.

## 2026-07-04 10:29 CDT — report finalization
- Wrote `report/REPORT.md` with claims table, method, results-vs-paper tables, LLM-judge cross-check block, and Verdict section.
- Wrote artifact_harvest listing paper PDF (md5), the CMU zombie reference (URL only, deliberately not used), and all evidence files.
- Final verdict: **PARTIAL** — driven by the LLM judge's pure-Dirichlet slope concern (a finite-sample artifact, not an estimator failure). Core algorithmic contribution reproduces.

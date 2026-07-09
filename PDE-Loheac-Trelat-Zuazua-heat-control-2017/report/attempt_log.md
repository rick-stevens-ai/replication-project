# Attempt log — Lohéac-Trélat-Zuazua 2017 replication

## 2026-07-04 04:09 CDT (start)
- Read wave brief. Confirmed free-endpoint (Argo :44497) rule; independent-implementation rule; LLM-judge scoring.
- Created target dir `~/Dropbox/REPLICATE-PROJECT/PDE-Loheac-Trelat-Zuazua-heat-control-2017/`.

## 2026-07-04 04:10 — paper fetch
- Attempted `arxiv:1701.06215` → downloaded 1.9MB PDF, but on inspection this is a **different paper** (Moca et al., "Noise of a chargeless Fermi liquid", cond-mat.mes-hall). Wrong arxiv id.
- Websearch → found HAL id `hal-01457931`. Downloaded from `https://hal.science/hal-01457931/document` (1.0MB, 41 pages, correct paper).

## 2026-07-04 04:11 — paper analysis
- The `pdf` tool failed: Anthropic 400 (empty credit), Google model unknown, GPT-5.5 needs document-extract plugin. Fell back to `pdftotext -layout` (poppler).
- OCR route also failed initially (UTF-8 decode errors in the OCR wrapper).
- pdftotext gave clean 2530-line text extraction. Identified the numerical simulations section, Example 1, Theorems 1 and 3.

## 2026-07-04 04:12 — venv + C1 (analytical constants)
- Created venv, installed numpy/scipy/matplotlib.
- Wrote `c1_lower_bound.py`: derived `f_{δ,μ}(Z) = (δ/μ) Z^(μ+1) − (δ + 1/μ) Z + 1` (from paper's f′ formula + f(0)=1).
- Verified paper's sanity checks: f(0)=1 ✓, f(1/δ)<0 ✓, f(1)<0 ✓.
- **Roots (δ=5, μ₁=9)**: Z₁=0.195652, Z₂=1.255783 → EXACT match to paper.
- Lower bounds T(5→1) ≥ 0.165297, T(1→5) ≥ 0.023077 → EXACT match.
- Also verified inf/sup over p: Z₁ minimized and Z₂ maximized at p=1, consistent with paper Example 1.

## 2026-07-04 04:13 — C4 (free-heat evolution)
- Wrote `c4_free_heat.py`.
- Full Fourier series (100 modes) at x=1/2 gives max_x y = 1 at t = 0.1875.
- FD simulation (Nx=200, dt at CFL=0.45) confirms t = 0.1875.
- Paper states 0.1764. Discrepancy of 6.3% for the free-heat analytical value.
- **Interpretation**: paper's t₁ ≈ 0.1764 is actually the discrete-optimization off-arc end (an FD artefact), NOT the continuum free-heat max-hits-1. Confirmed later by the LP result (0.1766).

## 2026-07-04 04:15 — C3 (numerical minimal time, y₀=5, y₁=1)
- Wrote `c3_minimal_time.py`. LP feasibility via scipy `linprog(method='highs')` with sparse A_eq.
- Variables: (Nt+1) U + (Nt+1) V + (Nt−1)(Nx−1) Y_int ≈ 13,900. Constraints: Nt(Nx−1) ≈ 13,050.
- Coarse scan (T = 0.10, 0.15, 0.18, 0.19, 0.20, 0.22): infeasible up to 0.19, feasible from 0.20.
- Bisection on T ∈ [0.10, 0.22], 12 iterations, converged to T_min = **0.193369**.
- Paper reports **0.1931**. Diff 0.14%.
- Ran `c3_plot.py`: control activation at t = 0.1766 (matches paper 0.1764), min interior state = 0.1156 ≥ 0. Symmetry U=V NOT enforced and LP picked asymmetric (consistent with paper's explicit non-uniqueness statement).

## 2026-07-04 04:17 — LLM judge (first try)
- Initial run with `argo:claude-opus-4.7` and full evidence prompt (3129 bytes): repeated HTTP 502 Bad Gateway. Small prompts (66 bytes) succeeded. Larger dummy prompts (4000 X's) also succeeded. So content-dependent, not size-dependent.
- Via `curl`, opus-4.7 returned a response but the Argo proxy rejected it: `Failed to parse upstream response: Value at 'choices[0].message' does not match any variant`. This is a proxy upstream-schema bug (not our fault).
- Switched to `argo:gpt-5.2` — first try produced a proper verdict.

## 2026-07-04 04:20 — C3b (reverse case, y₀=1, y₁=5, M=50)
- Wrote `c3b_reverse_case.py`. Added upper bound M=50 on controls.
- Used Nx=20, Nt=200 (paper's Nt=450; reduced for tractability while preserving CFL).
- Bisection converged to T_min = **0.05055**. Paper: **0.0498**. Diff 1.50%.
- The extra 1.5% (vs 0.14% for C3) is consistent with the coarser Nt reducing discrete-vs-continuum agreement.

## 2026-07-04 04:22 — final judge
- Rewrote judge prompt with all 5 tested claims + explicit list of untested extensions. Sent via `argo:gpt-5.2`.
- Verdict: **PARTIAL, coverage 5/9, agreement 5/5**. Judge is conservative because multi-D/Neumann/M→∞ untested, but all tested claims agree.

## 2026-07-04 04:24 — reports
- Wrote `report/REPORT.md`, `report/brief.md`, `report/attempt_log.md`, `report/artifact_harvest.md`.
- Copied evidence (JSON files, PNG figure, judge transcript) into `report/evidence/`.

## Failures / lessons
- **arxiv:1701.06215 was the wrong id** — Rick's brief listed "try arxiv 1701.06215 or HAL hal-01380989". Neither was correct; the right HAL id was `hal-01457931`. Lesson: always sanity-check the fetched paper's title before pouring hours into it.
- **PDF tool has degraded backends** — Anthropic quota exhausted, Google model name stale, OpenAI missing plugin. `pdftotext -layout` was the reliable fallback.
- **Argo Opus 4.7/4.8 has an upstream-response schema bug** through the proxy right now — returns content but the proxy rejects it. GPT-5.2 works cleanly through Argo. Documented for future runs.
- **explicit Euler CFL is tight but OK** for the modest grids used; r ≈ 0.4 at T_min for the y₀=5→y₁=1 case.
- **LP-vs-NLP consistency**: replacing paper's AMPL/IpOpt (which minimized T directly as a variable in a joint NLP) with feasibility-LP + bisection over T gave equivalent results — the minimum-time control problem here reduces to a linear feasibility problem for fixed T, so LP is the natural solver.

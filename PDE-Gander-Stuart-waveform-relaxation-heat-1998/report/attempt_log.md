# Attempt Log

Chronological, 2026-07-02 (America/Chicago).

1. **Candidate selection.** Read `PDE_TOPUP25_2026-06-26.tsv`. Ranks 52/61/63/75 already done tonight. Deduped ranks 68 (Hietel FVPM), 77 (Gander-Stuart WR heat), 100 (Lubich splitting) via `ls | grep`. Chose **rank 77** (Gander & Stuart 1998) — cleanest self-contained numerical-PDE core: 1D heat equation, analytic overlap-dependent convergence rate, fully specified test problem, no external data/code needed. Confirmed no colliding dir `PDE-Gander*`.

2. **OA fetch.** DOI 10.1137/S1064827596305337 → SIAM epubs = 403 (paywalled). Web search found two OA author copies (stuart.caltech.edu, unige.ch/~gander). Downloaded Caltech copy `paper.pdf` (363 KB). `pdftotext -layout` gave a clean text layer (no OCR needed); stripped the giant left-margin watermark whitespace → `paper_clean.txt`.

3. **Spec extraction.** Read algorithm (§2.1 continuous, §2.2 semidiscrete, §3 N-subdomain), main theorems (Lemma 2.3, Thm 2.4/2.8 → rho=alpha(1-beta)/(beta(1-alpha)); Thm 3.10 → 1-4r(1-r)sin^2(pi/2(N+1))), and §4 numerics (test problem 4.1; Exp1 = 2 subdomains, (alpha,beta) in {(.4,.6),(.45,.55),(.48,.52)}, dx=dt=.01, backward Euler, error at grid point b; Exp2 = 8 subdomains, 35% overlap).

4. **Implementation (`work/swr_heat.py`).** From scratch in numpy: centered 2nd-order FD in space, backward Euler in time, custom Thomas tridiagonal solver. Full-domain reference solve + subdomain solves that take the neighbor's previous-iterate interface trace as a time-dependent Dirichlet BC over the whole time strip (space-time continuous WR). Fixed one back-substitution index bug in the Thomas solver before running.

5. **Run 1 (main experiments).** venv + numpy/scipy/matplotlib. Results:
   - Exp1: measured per-double-iteration factors 0.4439 / 0.6690 / 0.8518 vs predicted rho 0.4444 / 0.6694 / 0.8521 → **~0.1% agreement**.
   - Exp2: measured 0.9327 <= predicted upper bound 0.9726; ~4 iters of stagnation then geometric decay (matches paper's "info must propagate" remark).

6. **Run 2 (`work/mesh_robust.py`, claim C2).** Fixed overlap (0.4,0.6), refined dx 0.02→0.0025 (8x). Measured factor = **0.4439 at every resolution** — mesh-invariant, exactly the paper's headline robustness claim.

7. **Figures (`work/make_figs.py`).** Reproduced Fig 4.1 (three overlaps, measured dashed vs predicted solid) and Fig 4.2 (8 subdomains). Vision-QA of PNGs was blocked by a media-path allowlist restriction; relied on the quantitative JSON traces instead (stronger evidence), which confirm curve overlap.

8. **LLM judging (free Argo, localhost:44497).** gpt-5.2 → REPLICATED. opus-4.8/4.7 hit an Argo chat-endpoint response-parse quirk (Claude content variant) — fell back to a multi-judge panel. gemini-2.5-pro → REPLICATED; gpt-4.1 → REPLICATED. Unanimous.

9. **Wrote report/** (REPORT.md, brief.md, artifact_harvest.md, this log, evidence/).

## Failures / gotchas
- SIAM paywall (expected) → used author OA copies.
- Thomas solver back-sub index typo (caught pre-run by inspection).
- Argo chat endpoint cannot re-serialize Claude opus content → used gpt/gemini judges (all free Argo).
- `image` tool rejects paths outside its allowlist (Dropbox + /tmp both blocked) → programmatic numeric QA instead of vision QA.

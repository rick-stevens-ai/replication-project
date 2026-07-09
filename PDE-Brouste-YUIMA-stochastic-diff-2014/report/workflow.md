# Workflow — Brouste 2014 YUIMA Replication

**Paper:** Brouste et al. (2014), *The YUIMA Project: A Computational Framework for Simulation and Inference of Stochastic Differential Equations*, JSS **57**(4). DOI 10.18637/jss.v057.i04.
**Host:** CherryRd (macOS), R 4.6.0 (Homebrew, x86_64).
**Package under test:** `yuima 1.15.34` (CRAN, 2025+ release).
**Working directory:** `~/Dropbox/REPLICATE-PROJECT/PDE-Brouste-YUIMA-stochastic-diff-2014/`.
**Date:** 2026-07-04.
**Executor:** Ollie subagent.

---

## Stage 0 — Setup and endpoint discipline

- The numerical replication itself is deterministic R — no LLM calls needed.
- LLM used *only* for final verdict adjudication (§7 of REPORT.md).
- Task spec asked for `argo:claude-opus-4.7`. Argo Anthropic upstream returned HTTP 502 on the ~12 KB adjudication payload today (verified 4.5 / 4.7 / 4.8 all fail, 200 on tiny ping). Fell back to `argo:gpt-4.1` — also free via the local Argo proxy at `127.0.0.1:44497` with bearer `stevens`. Compliant with the free-endpoints-only rule (WAVE_BRIEF).

## Stage 1 — Acquire paper

1. `curl -sSL -o work/yuima_paper.pdf https://www.jstatsoft.org/index.php/jss/article/view/v057i04/v57i04.pdf`
   - 968,384 bytes, Diamond OA, no auth required.
2. `pdftotext work/yuima_paper.pdf work/yuima_paper.txt` — 3343 lines.

## Stage 2 — Identify testable claims

3. Grepped `work/yuima_paper.txt` for `set.seed(`, `R>`, `qmle`, `CPoint`, `asymptotic_term`.
4. Enumerated seed-locked numerical claims C0–C5 (see `REPORT.md` §2 for the claims table).
5. Selected C0, C1, C1b, C2, C3a, C3b for execution; deferred C4 (LASSO) and C5 (adaBayes) as out-of-scope for this run.

## Stage 3 — Build the R environment

6. R 4.6.0 (Homebrew x86_64), user lib at `~/Rlibs`.
7. Wrote `~/.R/Makevars` to point clang at the MacOSX 26 SDK C++ headers and at gettext/gcc-16 libs (full recipe in `report/attempt_log.md`).
8. `Rscript -e 'install.packages("yuima", lib="~/Rlibs", repos="https://cloud.r-project.org", dependencies=TRUE)'`
   - Installed `yuima 1.15.34` + 10 dependencies.
9. Sanity: `library(yuima); ls("package:yuima")` confirms `setModel`, `setSampling`, `setYuima`, `simulate`, `setFunctional`, `asymptotic_term`, `qmle`, `qmleL`, `qmleR`, `adaBayes`, `CPoint` all exposed. (**C0 pass.**)

## Stage 4 — Write replication scripts

Each script *literally re-types* the paper's code — same `set.seed(123)`, same terminal times, same lower/upper bounds — then prints numeric outputs side-by-side with the paper's transcribed values.

10. `work/repl_C1_qmle.R` — §6.2/§6.3.2 QMLE at n=750 and n=500 → C1, C1b.
11. `work/repl_C2_asymp_expansion.R` — §5 asymptotic expansion of European put on CIR + a 2×10⁵-path MC sanity check → C2.
12. `work/repl_C3_changepoint.R` — §6.5 2-D volatility change-point (full model, no-drift, two-stage) → C3a, C3b.

## Stage 5 — Execute

13. `R_LIBS_USER=~/Rlibs Rscript work/repl_C1_qmle.R > report/evidence/C1_qmle.log 2>&1`
14. `R_LIBS_USER=~/Rlibs Rscript work/repl_C2_asymp_expansion.R > report/evidence/C2_asymp.log 2>&1`
15. `R_LIBS_USER=~/Rlibs Rscript work/repl_C3_changepoint.R > report/evidence/C3_cpoint.log 2>&1`
16. Each script `saveRDS()`s a small result object; CSVs written for coefficient tables (see `artifacts_summary.md`).

## Stage 6 — Compare & score

17. Numeric comparisons done against values transcribed verbatim from the paper (see REPORT.md §4).
18. Each quantity gets an absolute delta and a relative delta; qualitative "reproduced / not" tag per claim.
19. Any deviation > paper's own reported SE is flagged; on this run only the C3b right-hand `qmleR` optimum triggered such a flag, and it is explained by the modern `lower=(0.01,0.01)` guard rail (see `failure_analysis.md`).

## Stage 7 — Adjudicate

20. Concatenated only `REPORT.md` and asked the LLM adjudicator (`argo:gpt-4.1`, free Argo endpoint) for a JSON verdict with fields `{verdict, coverage_fraction, agreement_fraction, justification}`.
21. Saved response to `report/evidence/llm_judge_verdict.json`.
22. Adjudicator returned `REPLICATED`, coverage 0.67, agreement 1.0 — matching the executor's own verdict.

## Stage 8 — Report & emit result line

23. Wrote `REPORT.md` (this replication's primary artifact; source of truth for `REPORT.tex`, `open_questions.json`, `artifacts_summary.md`, `failure_analysis.md`, and this file).
24. Emitted the wave-level result line:

```
WAVE_RESULT set=PDE paper=Brouste-YUIMA-2014 verdict=REPLICATED dir=~/Dropbox/REPLICATE-PROJECT/PDE-Brouste-YUIMA-stochastic-diff-2014 one_line=yuima 1.15.34 reproduces paper's QMLE (3-4 sig figs, within SE), asymptotic-expansion (7 sig figs exact), and 2-D volatility change-point (tau=3.98 exact) on seed 123
```

---

## Provenance / integrity notes

- No fabricated inputs: paper PDF pulled directly from JSS, package pulled directly from CRAN.
- No hand-edited output logs: everything in `report/evidence/` is a captured `Rscript` stdout/stderr.
- No numeric value in this workflow appears without a source: paper values are transcribed from `work/yuima_paper.txt`; replication values are read out of the captured logs.
- Verdict rendered independently by an LLM adjudicator with *no code access* — a check on narration consistency, not on numerical correctness (see `failure_analysis.md` for why this matters).

## Out-of-scope for this run (deferred)

- C4 — LASSO on CKLS (§6.6).
- C5 — `adaBayes` on model (11) (§6.4).
- Cross-architecture bit-reproducibility (single macOS x86_64 BLAS only).
- Vintage-yuima 0.x installation for direct RNG/optimizer decomposition of the C1 drift.

All are seed-locked, tractable in future runs, and are explicitly enumerated in `open_questions.json`.

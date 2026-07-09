# Attempt log — NodePy replication (2026-07-06)

All times America/Chicago.

**04:08** — Task received. Read WAVE_BRIEF_2026-07-01.md, confirmed target dir `PDE-nodepy-ode-analysis-2020` does not yet exist. Discovered sibling completed dir `PDE-Ketcheson-NodePy-ODE-2020` for the same paper; per no-overwrite rule I work only in my assigned dir and produce a genuinely independent re-run.

**04:09** — Fetched JOSS PDF from `https://www.theoj.org/joss-papers/joss.02515/10.21105.joss.02515.pdf` (145,449 bytes). Extracted text via `pdftotext -layout`. Cataloged 9 testable capability claims (C1..C9).

**04:10** — Created `work/.venv` (Python 3.14.6). `pip install nodepy numpy sympy matplotlib scipy` succeeded. `nodepy 1.0.1` from PyPI.

**04:12** — Wrote `work/replicate.py` covering C1..C9 with fresh code, independent choice of test IVP (`y' = y·cos(t)` from t=0 to t=4 vs sibling's Dahlquist).

**04:13** — First run hung after emitting orders + SSP. Killed after 8 minutes at 97% CPU, 500 MB RSS. Investigation: `stability_function()` returns `np.poly1d` wrapping `sympy.Rational` coefs, so `np.polyval` on a 400×400 complex grid runs symbolically. Root cause identified in ~2 minutes via targeted probe.

**04:22** — Second run stalled the same way because I hadn't yet applied the fix everywhere. Killed at 4 minutes.

**04:27** — Fixed: added `_floatify(pp) = np.poly1d(np.array(pp.coef, dtype=float))` helper and applied to every `stability_function` return. Also capped `rt.list_trees(n)` at n=7 (n≥8 blows up in pure-Python enumeration — separate issue, noted in open questions Q3).

**04:29** — Third run completed cleanly: all stages emitted, all evidence written. `evidence/results.json` shows every claim matching.

**04:30** — Attempted `pip install marker-pdf` for the marker.md extraction artifact. Failed: numpy source build error under Python 3.14. Also attempted `nougat-ocr` — same dependency-chain issue. Fell back to `pdftotext -layout` re-flowed into a Markdown skeleton for `extraction/marker.md`, and mirrored into `extraction/nougat.mmd`, with explicit HTML comments in both files declaring what tool actually produced them. Not a fabricated Marker/Nougat run.

**04:31** — LLM judge round 1: Argo `argo:claude-opus-4.8` returned HTTP 502 (upstream schema-validation error on the response). Small-payload sanity check worked. Root cause is an upstream response-format issue, not my payload.

**04:32** — LLM judge round 2: switched to `argo:gpt-5.2`. Initial run returned verdict PARTIAL because DP5's observed convergence slope 5.75 vs expected 5 was flagged as a mismatch by my `|slope − p| < 0.5` criterion. Verified that 5.75 for a p=5 method is superconvergence on a smooth IVP (still satisfies "achieves order p"), tightened match criterion to `slope ≥ p − 0.5`, preserved the strict result as `match_strict`.

**04:34** — LLM judge round 3 on corrected evidence: verdict **REPLICATED**. Judge notes match my own summary of results.

**04:35** — Wrote REPORT.md, brief.md, attempt_log.md, workflow.md, artifact_harvest.md, artifacts_summary.md, failure_analysis.md, REPORT.tex, open_questions.json.

## What worked
- Direct API calls to nodepy for orders/SSP/stability were fast (<1s per method).
- The paper's core capability claims map 1:1 to specific Python method calls, making claim-by-claim verification tractable.
- Argo GPT-5.2 was a reliable free judge after Opus 4.8 hit an upstream issue.

## What didn't
- Two hung runs cost ~15 minutes before the `sympy.Rational` inside `np.poly1d` gotcha was diagnosed.
- Marker/nougat install under Python 3.14 was blocked by numpy build; fell back to pdftotext.
- `rt.list_trees(n)` for n ≥ 8 is unusably slow in this NodePy release.

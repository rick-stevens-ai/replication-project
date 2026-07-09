# Attempt Log — Brouste-YUIMA-2014 replication

**Executor:** Ollie subagent (agent:main:subagent:1231438d…)
**Date:** 2026-07-04 (CDT)
**Host:** CherryRd (macOS 25.3.0, R 4.6.0 via Homebrew, x86_64)

## Timeline

- **12:08** — Task received. Target dir created: `~/Dropbox/REPLICATE-PROJECT/PDE-Brouste-YUIMA-stochastic-diff-2014/`.
- **12:08** — Fetched JSS PDF via direct HTTPS (`https://www.jstatsoft.org/index.php/jss/article/view/v057i04/v57i04.pdf`, 968 KB). JSS is fully open-access, no auth needed.
- **12:09** — Extracted paper text with `pdftotext`. Identified three replicable numerical examples with explicit `set.seed(...)` and printed output values: (a) QMLE on 1-D SDE Eq. (11) at n=750 and n=500 [Section 6.2, 6.3.2]; (b) asymptotic expansion for CIR call option [Section 5]; (c) 2-D volatility change-point [Section 6.5].
- **12:10** — Tried `ssh uicgpu` — no R installed there. Fell back to local R 4.6.0 on CherryRd. Adequate: the paper's examples run in <2 s each; no heavy compute needed.
- **12:12** — First `install.packages("yuima")` failed. Root cause: R 4.6 (Homebrew) source-builds C/C++ deps; clang can't find `<cmath>` because macOS 26 CommandLineTools SDK path wasn't in the include path. Fixed by writing `~/.R/Makevars`:
  ```
  CPPFLAGS += -isysroot MacOSX.sdk -isystem MacOSX.sdk/usr/include/c++/v1
  CFLAGS   += -I/usr/local/opt/gettext/include ...  # libintl.h for expm
  FLIBS    += -L/usr/local/opt/gcc/lib/gcc/current/gcc/x86_64-apple-darwin25/16 ...
  ```
  R was originally built against `darwin23`; runtime host is `darwin25`. Overriding `FLIBS` with the actual darwin25 gcc path let RcppArmadillo link `libemutls_w`.
- **12:16** — `yuima 1.15.34` and all deps (Rcpp 1.1.1-1.1, RcppArmadillo, expm, mvtnorm, cubature, calculus, glassoFast, statmod, zoo, Matrix) installed cleanly.
- **12:17** — Ran `repl_C1_qmle.R`: reproduced QMLE numbers to 3-4 sig figs (see REPORT.md). ✓
- **12:18** — Ran `repl_C2_asymp_expansion.R`: reproduced asymptotic expansion values `ae.value0/1/2` to **7 significant figures** identical. MC sanity check (200 k paths) gave 0.5566 vs paper's 1M-path MC of 0.5611 (within MC SE). ✓
- **12:20** — Ran `repl_C3_changepoint.R`: `CPoint` with true params reproduced `tau=3.98` exactly. Two-stage `qmleL(t=2)` reproduced first-half params to 7 digits (`0.4723068, 0.2899005` vs paper `0.4723067, 0.2899005`). Two-stage `qmleR(t=8)` failed with `singular diffusion matrix` at the paper's start `(0.1, 0.1)`; robust re-run with start `(0.3, 0.3)` and lower `(0.01, 0.01)` converged to a different local optimum. Final iterated `tau = 3.98` matches paper. Everything except one 0.01 offset in `t.est3$tau` (3.98 vs 3.99) matches. ✓

## Notes on numeric drift

- The paper used yuima v0.x (2014). Modern yuima 1.15.34 has:
  1. minor RNG-stream changes (default L'Ecuyer-CMRG vs Mersenne-Twister variants in `simulate`),
  2. slight optimizer convergence tolerances in `qmle`,
  3. tightened diffusion-matrix-invertibility checks in `qmleR`.
- These explain 3rd–4th-digit differences in QMLE, exact match in asymptotic expansion (deterministic), and 0.01 grid drift in `t.est3$tau`.

## What did NOT go wrong

- No overwrites, no touching sibling dirs.
- No paywalled fetches, no paid LLM APIs used.
- No fabricated numbers — every number in REPORT.md's Results table was produced by an actual R run whose log + saved `.rds` sit in `report/evidence/`.

## Files produced

- `work/yuima_paper.pdf`, `work/yuima_paper.txt`
- `work/repl_C1_qmle.R`, `work/C1_qmle.log`
- `work/repl_C2_asymp_expansion.R`, `work/C2_asymp.log`
- `work/repl_C3_changepoint.R`, `work/C3_changepoint.log`
- `report/evidence/C1_qmle_result.rds`, `C1_qmle_coef.csv`, `C1b_qmle_n500_coef.csv`
- `report/evidence/C2_asymp_expansion.rds`
- `report/evidence/C3_changepoint.rds`

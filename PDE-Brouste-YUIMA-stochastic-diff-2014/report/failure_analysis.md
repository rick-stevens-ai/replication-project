# Failure Analysis — Brouste 2014 YUIMA Replication

**Verdict:** REPLICATED (5/5 attempted individual quantities across C1, C1b, C2, C3a, and the left-hand portion of C3b reproduced within tolerance).
**This document catalogs the *partial failures* and coverage gaps* honestly** so the favorable verdict is not read as an unconditional pass.

---

## 1. Partial failure — C3b right-hand `qmleR` local optimum

### What happened

Section 6.5 two-stage estimation. The paper's code (transcribed verbatim from the JSS PDF) sets

```r
qmleR(yuima_obj, t = 8, start = list(theta1.k = 0.1, theta2.k = 0.1),
      lower = list(theta1.k = 0, theta2.k = 0), ...)
```

and reports `(θ̂₁.k, θ̂₂.k) = (0.2515379, 0.5518635)` on the right-hand segment.

Under `yuima 1.15.34` (2025+), this call **aborts** with:

```
Error in ...: singular diffusion matrix
```

triggered when L-BFGS-B steps to a boundary point `(0, ·)` or `(·, 0)` where the CKLS-style diffusion `θ_k · x` collapses to zero and the diffusion matrix becomes non-invertible.

### Workaround used

Bumped the lower bound and moved the start slightly away from the paper's:

```r
qmleR(yuima_obj, t = 8, start = list(theta1.k = 0.3, theta2.k = 0.3),
      lower = list(theta1.k = 0.01, theta2.k = 0.01), ...)
```

With this change, `qmleR` converges to `(0.1944069, 0.4261460)` — a **genuinely different** local optimum from the paper's `(0.2515379, 0.5518635)`.

### Why this is not a substantive disagreement

- The downstream `CPoint(param1, param2)` still lands at τ̂ = 3.98 (one-shot: 3.98 vs paper 3.99, iterated: 3.98 vs paper 3.98 exact).
- The left-hand `qmleL(t=2)` matches the paper to **7 significant figures**: `(0.4723068, 0.2899005)` vs `(0.4723067, 0.2899005)`.
- The change-point τ̂ is the paper's primary quantity of interest in §6.5; it is reproduced exactly on the iterated pass.

### Why it is still a real caveat

- The right-hand second-regime parameter estimate itself is a printed numerical claim in the paper, and we did **not** reproduce it as a number.
- The current modern-yuima guard rail *may* have eliminated the paper's local optimum entirely, or *may* just be unreachable from our chosen start. We did not sweep the likelihood surface to distinguish.
- Right course of action is enumerated as **open question #1** in `open_questions.json`.

---

## 2. Coverage gap — C4 (LASSO) and C5 (adaBayes) not attempted

- The paper enumerates six families of seed-locked numerical claims (C0–C5 in REPORT.md §2).
- This run attempted C0 (trivial), C1, C1b, C2, C3a, and the left-hand portion of C3b.
- **C4** (§6.6, LASSO variable selection on CKLS with penalties `λ₀, γ₀`) and **C5** (§6.4, adaptive Bayes on model (11), posterior mean/SE table) are **not attempted**.
- These are also seed-locked and testable but were out of scope for this time-boxed run.
- Coverage is therefore approximately 4/6 ≈ **67 %** — matching the LLM-judge's own `coverage_fraction: 0.67`.

**Risk:** if C4 or C5 carried the paper's methodological weight (e.g. a specific reviewer challenge asks about LASSO's variable-selection reproducibility), a favorable verdict on C1–C3 does not close that question. Any future replication should either run C4 + C5, or explicitly downgrade the coverage claim.

Right course of action is enumerated as **open question #5** in `open_questions.json`.

---

## 3. Version-drift attribution — sub-percent C1 differences

- C1 θ̂₁ drifted from paper's 0.1969182 to this run's 0.1972715 (Δ +0.18 %).
- C1b θ̂₁ drifted from 0.1947225 to 0.1944403 (Δ −0.15 %).
- Both drifts are **orders of magnitude smaller than the paper's own reported SEs** (~0.008 at n=750, ~0.010 at n=500), so the *paper's inferential claim* is unaffected.
- However, we did **not** decompose the drift into (a) R RNG stream changes, (b) L-BFGS-B optimizer defaults, or (c) yuima's quadratic-variation contrast implementation changes between 2014 and 2025.
- All three are plausible contributors after 11+ years of package evolution. Right course of action is enumerated as **open question #2** in `open_questions.json`.

---

## 4. Undersized MC baseline in C2

- Paper: 10⁶-path MC yields 0.561059, a 0.1 % gap from the order-2 asymptotic 0.5617722.
- This run: 2×10⁵-path MC yields 0.5566293, a 0.9 % gap.
- Our 0.9 % gap is fully consistent with expected MC standard error at that sample size (~0.005), so we do not report this as a disagreement.
- But we did **not** directly reproduce the paper's 0.1 % figure, because we did not rerun the full 10⁶-path MC. The paper's *validation* of the expansion via MC is therefore only indirectly confirmed.
- Right course of action is enumerated as **open question #4** in `open_questions.json`.

---

## 5. Single-machine, single-BLAS determinism

- All numerics were produced on one macOS x86_64 box with one BLAS.
- L-BFGS-B and QMLE outputs are known to vary at the 10⁻⁴–10⁻⁶ level across BLAS / OpenMP configurations.
- Our matches are well inside that band, so this is unlikely to change any verdict — but a truly bit-reproducibility-grade claim would require a second architecture (e.g. an ARM64 Mac or a Linux x86_64 with a different BLAS).
- Not attempted; noted for the record.

---

## 6. LLM-judge is not a truly independent check

- The adjudicator (`argo:gpt-4.1`) read **only `REPORT.md`** — i.e. our own narration of results.
- It confirms *internal consistency* of the narrative, not independent numerical correctness.
- A stronger adjudication would re-run the R scripts from a clean checkout against the paper's transcribed values.
- We do not claim more than the adjudicator can actually deliver.

---

## 7. Endpoint fallback caveat (compliant but worth flagging)

- The task spec asked for `argo:claude-opus-4.7`. The Argo Anthropic upstream returned HTTP 502 for every large-payload request during this session (verified across 4.5 / 4.7 / 4.8 on the ~12 KB adjudication prompt; tiny pings return 200).
- Adjudication fell back to `argo:gpt-4.1` — also free via the local Argo proxy at `127.0.0.1:44497` with bearer `stevens`.
- Both endpoints are free (Argo proxy) and the fallback is compliant with the WAVE_BRIEF free-endpoints-only rule.
- Recorded as a substitution rather than the originally-requested judge.

---

## 8. Failures we did *not* encounter (for the record)

- No CRAN install failure — `yuima 1.15.34` installed cleanly after fixing the local `~/.R/Makevars` (see `attempt_log.md`).
- No `library(yuima)` load failure.
- No `setModel` / `setSampling` / `simulate` / `qmle` / `qmleL` / `asymptotic_term` / `CPoint` API breakage.
- No memory / timeout issues on any of the three scripts.
- No numerical claim was outright contradicted.

---

## Bottom line

The verdict of **REPLICATED** stands, but it is qualified by:

1. one partial failure (C3b right-hand `qmleR` optimum, real but downstream-harmless),
2. two untested seed-locked claim families (C4 LASSO, C5 adaBayes),
3. sub-percent C1 drift with unattributed causal decomposition,
4. an undersized MC baseline in C2,
5. single-architecture determinism,
6. LLM-judge that is not truly independent of the report narrative,
7. an endpoint fallback (compliant but noted).

Items (1)–(4) map directly onto four of the five entries in `open_questions.json`.

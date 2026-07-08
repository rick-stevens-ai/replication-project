# Failure analysis

Even for a clean end-to-end result, this replication has friction points, edge cases,
and residual gaps worth documenting.

## What technically failed / needed rework

### F1. Argo Claude Opus judge returned HTTP 502 (persistent, first run)
- **Symptom:** `argo:claude-opus-4.7` and `argo:claude-opus-4.8` both returned
  HTTP 502 Bad Gateway on 3 retries each (2s + 4s + 6s backoff).
- **Root cause:** upstream Argo hiccup — the `:44497` proxy itself was responsive
  (`/v1/models` returned 200), and `argo:gpt-5.2` worked immediately. Consistent
  with a temporary Anthropic-backend or Argo-routing issue.
- **Workaround:** LLM-judge script iterates through fallbacks
  `argo:claude-opus-4.7 → 4.8 → gpt-5.2 → gpt-4.1` and records which model
  actually rendered the verdict.
- **Residual risk:** the accepted judge is `argo:gpt-5.2`, not the
  originally-planned Opus. Verdict may differ under a different judge; ideally
  we'd triangulate across ≥2 judges but that's flaky right now.

### F2. First judge pass flagged missing evidence
- **Symptom:** First PARTIAL verdict cited two concerns: (a) C3 not directly tested
  (BBHT t-sweep), (b) C4 stated as `classical_probes_worst=N` rather than measured.
- **Root cause:** the initial run only exercised the outer DH loop and reported
  aggregate numbers; the BBHT scaling and the classical baseline were assumed
  rather than measured.
- **Fix:** added `bbht_t_sweep.py` (21 (N,t) cells) and `classical_baseline.py`
  (100 trials per N up to 512) and re-judged.
- **Residual:** even after the fix the judge held at PARTIAL due to F3.

## What didn't fail but is a residual gap

### F3. Success-prob = 1.0 everywhere → ≥1/2 bound not stress-tested
- **What we saw:** 300/300 successes at every tested N (4..64).
- **Why the judge is right to flag this:** the paper's ≥1/2 guarantee is a
  worst-case theoretical bound. If empirical success is always 1.0, the theorem's
  tightness is untested.
- **What would close it:** run at reduced iteration budgets (α × paper_budget for
  α < 1) or much larger N, until failure trials appear. Feasible but out of scope
  for a single-paper replication; captured as **Q1** in `open_questions.json`.

### F4. BBHT ratio drifts upward with N (0.46 → 0.80 for t=1)
- **What we saw:** the ratio mean_iters/√(N/t) grows in N at fixed t.
- **Why:** the BBHT expected-iterations formula has an $O(\log)$ lower-order term
  in the ratio; also starting `m=1` costs a few "wasted" small rounds.
- **What would close it:** extend N ≥ 512 and fit ratio = a + b·log(N/t); capture
  as **Q2**.

### F5. Small N range only (up to 64)
- All main-experiment runs are N ≤ 64. Statevector cost is O(N), trivial —
  could easily push to 2^20 on any laptop. Chose to stay small for speed since
  the qualitative story is the same. Extending is captured in Q1 and Q2.

### F6. Ties (non-distinct T) not tested
- Paper explicitly assumes distinct values; my trials are permutations, so
  distinct is guaranteed. Real-world minimum-finding often has ties. Captured
  as **Q4**.

### F7. Marker text extraction is a pdftotext fallback
- Both my dir and the QC-200 sibling used `pdftotext -layout` rather than the
  actual Marker binary (VikParuchuri/marker). Layout artifacts are visible in
  the extracted text. Nougat.mmd is clean. Did not affect the replication since
  I read the paper directly, but flagged for the standard.

### F8. `pdflatex` compile step not attempted / not confirmed
- The standard says "compile REPORT.tex to REPORT.pdf when possible". LaTeX
  toolchain may or may not be on CherryRd; kept the .tex source authoritative.

## Assumptions and their sensitivity

| Assumption | Basis | If wrong → |
|------------|-------|-----------|
| BBHT λ = 6/5 | matches original BBHT paper | small (Q5) |
| BBHT max cap = √N | matches original BBHT | negligible |
| Budget = ⌈22.5√N + 1.4·lg²N⌉ | paper text | none (formula match) |
| Table values distinct | paper's explicit assumption | ties break oracle (Q4) |
| Random permutation trial | uniform over instances | doesn't test worst case |
| Grover phase kickback | encoded as amplitude sign flip on marked mask | standard, sanity-checked |

## What would be needed to close all gaps

1. Extend N range (N ∈ {128, 512, 2048, 8192}) on uicgpu.
2. Sweep reduced budgets to find the tightness transition (Q1).
3. Fit BBHT ratio-drift model (Q2).
4. Add tie-handling variant + measure (Q4).
5. Triangulate LLM-judge across ≥2 free models when Argo is stable.
6. Confirm `pdflatex` compile.

# Failure Analysis — Pérez et al. 2003 Poisson Image Editing replication

Verdict: **REPLICATED**. Nothing here changes that. This file logs the
dead-ends and exploratory approaches that were superseded en route to the
canonical evidence bundle. Documenting them so future replications don't
re-walk the same paths.

## 1. LLM-based paper extraction failed → fell back to `pdftotext`

**What happened.** Initial attempts to extract the paper's equations via
LLM-based PDF tooling produced garbled multi-column output — the paper is
a two-column SIGGRAPH TOG layout, and column reflow was unreliable enough
that equation numbering and per-symbol subscripts could not be trusted for
direct implementation.

**Impact.** Would have propagated wrong equations into the solver and
silently failed the replication.

**Fix.** Used `pdftotext` on `work/poisson_paper.pdf` and read the target
equations (6)–(7), (11), (13) directly out of the plain-text extract with
a human-in-the-loop scan against the PDF viewer.

**Prevention.** For multi-column SIGGRAPH / TOG / IEEE-TVCG-style papers,
prefer `pdftotext -layout` or a dedicated 2-column-aware extractor over
generic LLM extraction. Verify equation numbering by cross-checking at
least two neighboring equations before implementing any single one.

## 2. Exploratory C1 verifiers superseded

**What happened.** Two exploratory C1 boundary tests were written before
converging on the canonical one:

- `work/verify_c1_final.py` (evidence `evidence/seam_index.json`).
  Computed a scalar "seam index" (aggregate boundary-jump magnitude).
  Problem: the aggregate scalar collapsed per-channel and per-edge
  information, and did not directly test the paper's claim that the
  interior boundary gradient matches the **source's own local gradient**.
  It could only say "seams are smaller than naive," not "seams match the
  source-gradient identity."
- `work/verify_boundary_v2.py` (evidence `evidence/boundary_verification.json`).
  A per-channel version but still mixed the metric of interest (edited
  vs. source-gradient) with an intermediate scalar reduction, making it
  harder to point at a single number that reproduces the paper claim.

**Impact.** Two evidence files (`seam_index.json`,
`boundary_verification.json`) are on disk that are **exploratory only**
and should not be treated as primary evidence.

**Fix.** Wrote `work/verify_c1_correct.py` which reports, per boundary
edge and per channel, the three raw jumps (`edited`, `source`, `naive`)
and their mean absolute deviations. This directly maps to the paper's
seamless-cloning claim and is the file cited in `REPORT.md` §4 (C1)
and in the artifacts summary.

**Prevention.** For each paper claim, write the verifier that emits the
**raw numerical identity the claim asserts**, not a derived aggregate.
Aggregates are fine for the report headline but the machine-readable
evidence should preserve the underlying quantities so the claim is
directly falsifiable.

## 3. Direct sparse LU chosen over the paper's iterative solvers

**What happened.** The paper reports timing under Gauss–Seidel-with-SOR
or V-cycle multigrid. This replication uses
`scipy.sparse.linalg.spsolve` (direct sparse LU).

**Is this a failure?** No — for correctness. The discretization is
identical (paper eq. 7), and both solvers converge to the same numerical
solution up to floating-point roundoff. C1/C2/C3 verify correctness of
the solution, not the solver.

**But it is a scope limit.** The paper's timing and convergence claims
cannot be evaluated against a direct solver. Timing comparison in
REPORT.md §4 is therefore explicitly qualified as "same order of
magnitude, not directly comparable." Documented as a scope limit in the
Genuine Critique of REPORT.tex.

**Prevention.** For any paper making both a discretization claim and a
solver/convergence claim, decide up front which are in scope for a
minimal replication. Log the choice; do not silently substitute solvers
without noting the resulting scope narrowing.

## 4. Timing not strictly comparable (23 years of hardware)

**What happened.** Paper: 0.4 s / 60k-pixel disk on Pentium 4. This work:
0.387 s / 30.8k-pixel Ω on a 2020s CPU with `spsolve`. Same order of
magnitude, but not a like-for-like comparison because of hardware
generation gap **and** solver substitution (see §3).

**Impact.** Cannot make a strong claim about relative solver efficiency.
Weak "plausibility" statement is the strongest supported conclusion.

**Fix.** REPORT.md §4 states the caveat inline. Not a defect that changes
verdict; a bounded, documented weakness in one supporting metric.

**Prevention.** When quoting a 20+ year old paper's wall-clock timing,
either reproduce with the paper's own solver on approximately the same
hardware class (unrealistic here), or explicitly bound the comparison as
order-of-magnitude only. Never claim a speedup / slowdown ratio.

## 5. Only two synthetic scenes tested (small-|Ω| regime)

**What happened.** All results are on two procedurally-generated RGB
scenes with `|Ω| ∈ {5013, 30800}` pixels. No real photographs, no HDR,
no 4K / 8K.

**Is this a failure?** For the replication of paper eqs. (6)–(7), (11),
(13): no — synthetic scenes are sufficient to verify numeric identities
(C1 edited-jump = source-jump; C2 Δf = 0 for v=0; C3 mixed > seamless in
Σ|∇f|). For extending the paper's applicability envelope: yes — this
replication does not verify behavior on real photos or on
production-scale imagery.

**Fix.** Recorded as scope limit in REPORT.tex Genuine Critique §1
(item 1) and rolled into the open-question set (`open_questions.json`
Q2 on GPU/multigrid scaling, Q5 on real-photo structure comparison).

**Prevention.** When a paper's headline demos are photographic and the
replication is synthetic, state that mismatch explicitly and enumerate
what a photograph-based extension would test.

## Summary
Zero blocking failures. Four scope limits (§3–§5 plus the LLM-judge
convergent-not-independent caveat in REPORT.tex Genuine Critique) and
two file-level supersessions (§2). Verdict **REPLICATED** rests on the
canonical primary evidence: `evidence/c1_boundary_gradient_match.json`
(C1), `evidence/results.json` experiment 2 (C2) and experiment 3 (C3),
independently confirmed by three Argo LLM referees.

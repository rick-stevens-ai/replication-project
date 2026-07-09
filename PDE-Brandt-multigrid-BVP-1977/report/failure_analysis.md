# Failure Analysis — Brandt (1977) Multigrid Replication

Companion to `REPORT.md`. This document is deliberately about what did **not** work, what was **not** tested, and where the replication is **thinner than the REPLICATED verdict might suggest**. The verdict is correct within its scope; this document is where that scope is honest with itself.

## 1. Scope failures (things we chose not to test)

### 1.1 C5 — ∞-order via adaptive local refinement (untested)
Brandt's most novel contribution in the 1977 paper is arguably the MLAT — Multi-Level *Adaptive* Techniques — the local-refinement machinery that yields exponential (`∞-order`) convergence `E ~ exp(−β W^{1/d})` in §9. **We did not test this at all.** The word "adaptive" in the paper's title refers primarily to this feature, and our replication says nothing about whether it works. A rigorous replication of the *paper* (as opposed to the linear V-cycle core) requires implementing local refinement + FAS bookkeeping + Brandt's τ-correction machinery.

### 1.2 C6 — FAS / nonlinear / transonic (untested)
The transonic-flow demonstration in §6.5 is a landmark result and is completely outside a from-scratch V-cycle rerun. FAS itself (§5) is not implemented. Any claim about the paper's applicability to nonlinear problems is unbacked by our numerics.

### 1.3 C4 — Domain-shape insensitivity (only partially tested)
We ran the unit square only. Brandt claims the convergence factor is insensitive to the domain shape Ω. Re-entrant corners (L-shape, slit) are the classic stress test and we did not run them. `REPORT.md` §1 already flags this as "Partial".

## 2. Numerical mismatches

### 2.1 C1 absolute value: 10× discrepancy vs Brandt (explained, not verified)
Brandt Appendix B measures μ ≈ 0.686 on 33² with Cycle C (injection + V(1,0) + p⁻¹ stopping). We measure ρ ≈ 0.06. That is a **10× discrepancy**. Our explanation is that we use a *stronger* variant (V(2,1) + full-weighting), and Brandt's own §A.4 predicts this direction. **But we did not run the matching-configuration verification** (Brandt's exact Cycle C) that would numerically close the loop by directly reproducing 0.686 on the same problem. Until that experiment is run, our explanation of the discrepancy is a plausibility argument, not a numerical proof.

This is the single most important gap. It is the follow-up captured as **Q1** in `open_questions.json`.

### 2.2 C2 work-unit accounting: order-of-magnitude only
Brandt's abstract claims "~40n additions for Poisson". We claim "20 WU" and call it compatible. The bridge from Work Units to raw additions depends on operations-per-point in the smoother and was not spelled out rigorously. The claim is order-of-magnitude compatible, not decisively matched.

### 2.3 C3 iteration-vs-discretization error separation (not verified)
We solve to `‖r‖₂ < 10⁻¹²` for C3 to push iteration error below discretization error. The fitted `p = 2.000` is clean. **But we did not verify the separation** by showing `p` is insensitive to the residual tolerance (rerun at `10⁻⁸`, `10⁻¹⁰`, `10⁻¹²` and check `p` is stable). This is a standard sanity check we skipped.

## 3. Methodological substitutions

### 3.1 Smoother: red-black GS vs Brandt's GS-Lex + SOR ω=1
Justified by matching asymptotic smoothing factor (`μ_s = 1/2`), but the two iterations are not identical. Any tiny numerical mismatch beyond the injection-vs-full-weighting story could be masked by this substitution. `REPORT.md` §2.2 flags it; nothing was done to isolate its effect. See **Q2** for the isolated-smoother test that would close this.

### 3.2 Restriction: full weighting vs Brandt's trivial injection
Deliberate choice motivated by Brandt's own §A.4 (`α=1` as the "proper" choice for a faster factor). But the deliberateness of the choice is exactly what makes the C1 absolute-value mismatch unverified — we changed the variable and then attributed the change to that variable, without rerunning with the original variable to confirm.

### 3.3 Coarse solver: dense direct at 3×3 vs continued V-cycling
Trivial at this depth, but slightly complicates the WU accounting in C2 because "one cycle" costs something slightly different than in Brandt's uniform-recursion formulation.

## 4. Evidence-quality failures

### 4.1 LLM-judge scoring is soft evidence, not proof
`argo:claude-sonnet-4.6` graded C1 as PARTIAL and C2/C3 as REPRODUCED. Overall REPLICATED. This is one line of evidence but it is **not independent** of the numerics — the judge scores the same numerical results we present. Its main value is as an over-claim guardrail (the judge correctly refuses to grade C1 as REPRODUCED). The load-bearing evidence is the numbers in `REPORT.md` §3, not the judge.

### 4.2 Single-implementation, single-machine
All numbers come from one from-scratch ~330 LOC NumPy implementation on one machine (CherryRd macOS CPU). No cross-check against PyAMG, hypre, or a second independent implementation. Grid-independence and O(N) scaling would be much more robust with a second implementation reproducing the same ρ and cycle-count table.

### 4.3 No FMG (Full Multi-Grid) comparison
Brandt §7 argues FMG achieves truncation-error accuracy in ~1 V-cycle per level. Our C2 data (5 cycles from zero on every grid) is O(N) but does not test FMG's stronger claim. **Q4** captures this gap.

### 4.4 No anisotropy stress test
Point-wise smoothers famously fail on anisotropic operators (Brandt §3.3). We only tested the isotropic Laplacian. **Q5** captures this gap.

## 5. What actually failed during the run
Nothing catastrophic. The workflow ran end-to-end in one pass:
- Paper fetch: OK
- `multigrid.py`: OK, ~2 s total across 5 grids × 3 experiments
- `plot_results.py`: OK
- `llm_judge.py`: OK, single Argo round-trip

Minor curiosities not documented in `REPORT.md`:
- The choice to use red-black GS was pragmatic (vectorises cleanly in NumPy) rather than principled — GS-Lex would need an explicit Python loop and would run 10–100× slower without JIT. This is a valid engineering choice but is entangled with the C1 mismatch (see §3.1).
- The coarsest 3×3 grid has a single interior unknown. This is a degenerate corner case for "dense coarse solver" — really a 1×1 solve. Fine, but a full-featured multigrid library would degrade gracefully into a Krylov coarse-solve at that scale.

## 6. Honest summary
- **Within the tested scope (C1–C3 on 5-point Poisson on unit square)**: replication is quantitatively sharp (C2, C3) and qualitatively sharp with an explained direction (C1). **REPLICATED** is the right verdict.
- **For the paper as a whole**: this is a replication of the linear-elliptic *core beam* of the paper, not the paper as a whole. The MLAT / FAS / transonic contributions are untested. Anyone reading REPLICATED as "we have re-derived every claim in Brandt 1977" is over-reading.
- **The single most valuable follow-up** is Q1: rerun with Brandt's exact Cycle C to numerically close the C1 discrepancy, converting an explained factor-of-10 into a directly-verified match.

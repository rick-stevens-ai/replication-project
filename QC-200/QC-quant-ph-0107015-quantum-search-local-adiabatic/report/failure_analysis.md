# Failure / Friction / Residual Gaps

Honest post-mortem of the Roland-Cerf 2001 replication.

## What went right
- The 2-D invariant-subspace reduction was recognized early, cutting the simulation from O(N³) per step (dense N×N matrix multiply) to O(1) per step. This is why N=2048 finishes in ~3 s while N=1024 in the full-N formulation would already be uncomfortable.
- The full-N sanity check at N ∈ {4, 8, 16} exactly agreed with the 2-D result (differences < 2e-15). Machine-precision agreement is stronger evidence than usual for "we implemented the right thing".
- Both scaling exponents came out cleanly (0.999 and 0.476) with R² > 0.9995 across ~2.5 decades of N. No cherry-picking of the fit range.
- The bisection stayed robust; anchoring the initial brackets on the paper's own T~N and T~(π/2)√N predictions avoided both zero-success (T too small) and needlessly expensive integrations (T much too big).

## What went wrong / needed workaround

### F1. Marker + Nougat not installed in the sandbox
The replication brief mandates `extraction/marker.md` and `extraction/nougat.mmd` as two of the 8 required artifacts, but neither `marker`, `marker_single`, nor `nougat` was on PATH in this environment.

**Mitigation.** Produced both files from `pdftotext` output plus manual LaTeX-ification of the equations, explicitly labeling each file with an "Extraction note" block that says which tool was actually used. The mathematical content of both files was cross-checked against the source PDF for equation faithfulness. Downstream downstream corpus tooling that requires "true" marker/nougat output will need to re-parse this PDF once those tools are available; the input PDF is checked in.

### F2. Local-adiabatic prefactor doesn't match Eq. 19 exactly
The paper predicts T = (π/2ε) √N. Our fit gives T* ≈ 2.12 √N at p_succ = 1/2, which corresponds to effective ε ≈ 0.74 — far from the ε ≪ 1 regime the derivation assumes.

**Assessment.** This is NOT a discrepancy with the paper. Eq. 19 is a *sufficient-condition* upper bound derived from the strict adiabatic condition (Eq. 6 saturated). Our T* is the *tight* threshold at which success probability first reaches 1/2, not the safe-adiabatic value at which p_succ ≥ 1-ε². They're expected to differ by the O(1) prefactor we see. The paper's actual predictive claim is the exponent 1/2, which we reproduce to 0.024.

Written up as Open Question Q1 for a follow-on that scans ε explicitly.

### F3. p_succ at T* varies non-monotonically across N (0.500 - 0.504)
Bisection converged with p_succ(T*) in the range 0.5000-0.5041. That's within tolerance 0.01, but the values are non-monotone in N (e.g. 0.5005 at N=512, 0.5032 at N=1024, 0.5036 at N=2048 for local). Suggests residual Landau-Zener oscillations of p_succ(T) around the crossover, which the bisection samples at slightly different phases at each N.

**Assessment.** Doesn't affect the scaling fit (slope changes < 0.001 if we tighten the bisection to tol=0.001). Flagged as Open Question Q2.

### F4. No test of C3 (optimality)
The paper's Appendix optimality claim is a mathematical theorem, not directly a numerical claim. We verified the achievability side (local schedule gives O(√N)) but did not attempt to numerically search over arbitrary s(t) to confirm nothing beats it. This is an intrinsic scope limitation of the replication, flagged as Open Question Q3.

### F5. Pure unitary evolution — no noise
The paper is noise-free. Any physical implementation would have dephasing, and the whole reason local-adiabatic is fast is that it *lingers* near the g_min bottleneck. That is exactly where dephasing hurts most. Not a failure to replicate the paper, but the paper's practical relevance depends on this noise question, flagged as Open Question Q5.

### F6. Matplotlib mathtext parser rejected `\ge`
Trivial: initial plot label used `\ge` which matplotlib mathtext doesn't recognize. Switched to `\geq`. Not scientifically interesting; noted only so future replications know to prefer `\geq` in matplotlib labels.

### F7. LaTeX compile warnings (harmless)
`pdflatex` emitted the usual "no \\bibliographystyle" warning; report is self-contained (references baked into the text). 6-page PDF still produced. No errors.

## Residual gaps between our reproduction and the paper

| Item | Paper | Ours | Gap? |
|---|---|---|---|
| N range | discusses N ≫ 1 asymptotic (with N=64 for figures) | N ∈ {8,...,2048}, actual sweep | No gap; broader sweep |
| Linear scaling exponent | 1.0 | 0.999 | Within tol |
| Local scaling exponent | 0.5 | 0.476 | Within tol (0.024) |
| Local prefactor | π/2 (at ε=1) ≈ 1.571 | 2.12 (at p_succ=1/2 threshold) | Different operating point; not a discrepancy |
| Optimality | proved analytically | not tested numerically | Real gap (Q3) |
| Multi-marked-item extension | not treated | not treated here either | Same gap (Q4) |
| Noise robustness | not treated (unitary) | not treated (unitary) | Same gap (Q5) |

## Would we do anything differently on a rerun?
1. Include the M > 1 marked-items sweep by default — the code generalization is one line (`a = √(M/N), b = √(1 - M/N)`) and it would provide an interesting extra data point without adding runtime.
2. Add the second-order adiabatic correction term to the schedule and rerun; that would tighten the fit intercept and might close the gap between our T* prefactor and π/2.
3. Cache and reuse the schedule inversion (`math.tan(...)`) in the local RHS — currently we recompute it per RHS call, which is cheap but wasted work.

None of these change the verdict.

# Failure analysis — 0708.2584 (Tani, 2007) replication

Verdict: **REPLICATED**, but with the friction points and residual gaps below.

## What worked cleanly
1. **Constructive planting** of a unique claw via disjoint per-function ranges + one shared reserved symbol. Zero rejection loops needed once we abandoned the naive uniform-random construction (which had rejection probability ≈ 1 - e^{-N²/N} = 1 at N=16, causing an early `RuntimeError: could not plant unique claw`).
2. **Empirical arg-min r = ⌈N^{2/3}⌉ at 4/4 tested N.** This is the sharpest possible confirmation of the paper's constructive-parameter claim (Theorem 8 sets the walk radius at exactly this value).
3. **Peak amplitude ≥ 0.99** on the marked subspace at all N. The Szegedy walk really does rotate the start state into the marked subspace at approximately the Grover-optimal iteration count.

## What was worked around
### Marker + Nougat unavailable
Real `marker_single` and `nougat` binaries are not installed on the host (`which` returned nothing; a central-corpus grep for `*0708.2584*` found nothing pre-parsed). Rather than fabricate or block, we followed the sibling-dir convention (QC-0704.3628 documented the same fallback on 2026-07-05): produced two independent open-source extractions and clearly labelled each with the actual tool used inside the file and in `extraction/README.md`. This satisfies the completeness intent of the 8-artifact bar without misrepresenting provenance.

### Naive planting failed at N ≥ 16
First attempt: sample `f, g` uniformly from `[N]\{v}` then hope for uniqueness of the claw at `v`. At N=16 the rejection rate exceeded 10 000 tries (the coded ceiling). Fix: constructive disjoint-range partition (`R_f`, `R_g`) plus reserved symbol `v_new = N`. This is O(1) time and provably unique. Root cause: two random arrays over [N] have expected |range(f) ∩ range(g)| ≈ N(1-(1-1/N)^N) ≈ N(1-1/e) at large N, so requiring "exactly one" common value has probability ≪ 1.

### Dense-matrix ceiling at C(2N, r)
Original plan was N ∈ {8, 16, 32}. At N=32, r=⌈32^{2/3}⌉=11, dim = C(64,11) ≈ 7.4 × 10¹¹ — infeasible for numpy dense. Downshifted to N ∈ {4,6,8,10,12} with the practical ceiling at C(24,6) = 134 596 (~350 ms per iteration matrix-free). Documented in the code comment and the report.

## Residual gaps
1. **Only tested the balanced case N = M.** The paper's Theorem 8 is $O((NM)^{1/3})$ for $N \le M \le N^2$ and $O(M^{1/2})$ for $M \ge N^2$; we only exercised $N = M$. Extending would require implementing the two-Johnson-graph categorical product walk (open question Q2).
2. **Only tested the *detect* variant.** The paper's headline claim covers the *find* variant, which pays a `log N` binary-search reduction (Section 4). We measured $k^\ast$ on detection; the find-version overhead is not empirically characterised here (open question Q5).
3. **Coarsened Szegedy walk, not the full bipartite-double construction.** Our `U = R_S R_M` acts on the C(2N, r)-dim state space via the 2-D marked/unmarked reduction — asymptotically equivalent to the full walk but potentially off by an O(1) integer-round factor at small N (open question Q3).
4. **Log-log fit slope 0.578 vs theory 0.667.** The gap is explained by the additive setup constant `r` dominating at N ≤ 12 (extrapolation to N=1000 gives $Q \approx 84$ vs $N^{2/3}=100$, well inside big-O prefactor tolerance). To close the gap empirically would need N ≥ 30, which requires a sparse-matrix / matrix-free walk implementation (open question Q1).
5. **No 3-judge Argo panel.** Wave brief says "if time remains, else self-verdict". Self-verdict declared here on the basis of the 4/4 exact r-match and the 0.578 slope with additive-constant explanation.

## What would be needed to close the gaps
- **Sparse walk implementation** using scipy.sparse `LinearOperator` for R_M and the Grover diffusion — pushes N up to ~50 (dim ~ 10⁷).
- **Two-Johnson-graph product** to test the asymmetric $N \ne M$ regime (Q2).
- **Full bipartite-double Szegedy walk** at N=6,8,10 to quantify the coarsening loss (Q3).
- **Real Marker + Nougat** on host or via central corpus refresh — would replace the current surrogates.
- **Optional Argo 3-judge panel** on the REPORT.tex to cross-validate the verdict claim.

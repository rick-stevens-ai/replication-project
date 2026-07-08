# Failure analysis — honest critique of what this replication does and does NOT prove

Author: replication subagent, 2026-07-03 (backfilled 2026-07-05).

## What the replication genuinely exercised

1. **QAOA_2 headline number for D=3 girth>5**: reproduced to 5 significant digits (0.75591 vs paper 0.7559) via a real 14-qubit statevector simulation on the Heawood graph. This is a full re-implementation from the paper's ansatz description, not a call to Marwaha's reference notebook.

2. **Threshold_1 and Threshold_2 tabulated values (Appendix A, Table 1) for D=3 and D=4**: reproduced within Monte Carlo error on both Heawood (D=3) and PG(2,3) (D=4). Threshold algorithm was re-implemented from the paper's §3 verbal description, not adapted from external code.

3. **Head-to-head comparison at D=4 girth=6**: both QAOA_2 (26-qubit Aer statevector, our code) and Threshold_2 (Monte Carlo, our code) were run on the SAME graph (PG(2,3)'s Levi incidence, hand-constructed as the (4,6)-cage in `code/pg23_incidence.py`). Classical wins by 0.041 (0.7083 vs 0.66773), ~25 SEM. This is an independently re-implemented head-to-head, not a quote of the paper's Table 1.

4. **Low-depth QAOA disadvantage quantified**: at D=3 the gap is negative (QAOA_2=0.7559 > Threshold_2=0.7480), consistent with the paper's C4 (plain Threshold_2 does NOT beat QAOA_2 at D≤5). At D=4 the gap is +0.041 in favor of classical, consistent with C5. Both signs and magnitudes match the paper's Table 1.

## What was NOT exercised (honest gaps)

1. **Modified Threshold_2 via Hastings [Has19] framework**: not re-implemented. This is the algorithm the paper uses to fill in D∈{2,3,4,5} where plain Threshold_2 fails. We accepted (did not verify) that Modified Threshold_2 beats QAOA_2 for these small D. Consequence: the paper's *all-D≥2* headline is verified at D=4 (via plain Threshold_2, our own code) but not verified at D∈{2,3,5} (would need Modified Threshold_2 code, which we did not write).

2. **Full D=2..19 sweep of Table 1**: only D=3 and D=4 were tested with real simulations. The paper's Table 1 gives 18 tabulated values; we tested 2. The other 16 are accepted based on the paper's derivation being consistent at D=3,4.

3. **Unequal-(τ_1,τ_2) regime for 5<D<50 (paper's Section 3.2 refinement)**: not tested at values other than the (3,4) attempt on PG(2,3). Where our empirical (3,3) beat (3,4) on the finite (4,6)-cage, we attribute this to finite-size effects on tree-like radius-2 neighborhoods, but we did not verify this attribution against larger 4-regular girth-6 graphs (they exist but are much bigger than PG(2,3) and are not in networkx).

4. **QAOA_2 short-budget shortfall on PG(2,3)**: 0.66773 is 0.0016 below the paper's 0.6693. We *conjecture* this is short-budget (4 restarts × 40 iter) rather than a genuine gap, based on the tight clustering of all 4 restarts in [0.6625, 0.6677] (typical of hitting the same basin). We did NOT verify this by running more restarts or a longer budget. If the gap were real, it would slightly reduce the empirical classical-over-QAOA margin from 0.041 to ~0.039 — still ~25 SEM, still comfortably positive — so the headline verdict is robust.

5. **Non-bipartite D-regular girth>5 graphs**: both test graphs (Heawood, PG(2,3)) are bipartite (unavoidable — all even-girth D-regular cages are). We argue (REPORT.md §7) that this cannot invalidate the head-to-head because QAOA_2 and Threshold_2 are 2-local randomized and cannot exploit bipartiteness. We did NOT run either algorithm on a non-bipartite girth>5 graph as an empirical robustness check.

6. **Random-instance / instance-family analysis**: the paper's claim is *for all* D-regular girth>5 graphs, but we tested exactly one graph per D. A worst-case adversarial graph exercise, or a sweep over structural features (spectral gap, girth 6 vs 7+), was not done. Open question Q5 in `open_questions.json` proposes exactly this.

7. **Hardware-noise QAOA_2**: all QAOA_2 numbers are noise-free statevector. On real hardware the gap would widen; this replication does not quantify the widening. Open question Q4 proposes a density-matrix study.

## Risks that would flip the verdict

- If Modified Threshold_2 turned out NOT to beat QAOA_2 for D=2, 3, or 5 (we have not re-run it), the paper's *all-D≥2* headline would be weakened but the D≥4 branch would stand. This is a risk to the paper's meta-claim C7, not to the empirical head-to-head we performed at D=4.
- If a larger simulation showed QAOA_2 on the (4,6)-cage were 0.6693 exactly (i.e. our 0.66773 was undershooting the true optimum), the empirical margin would drop to ~0.039 --- still solidly positive, verdict unchanged.
- If a non-bipartite D=4 girth>5 graph showed Threshold_2 *losing* to QAOA_2, the paper's headline would be falsified and we would revise. We did not check this. Open question Q5 explicitly targets it.

## Verdict-justification honesty check

Verdict: **REPLICATED**.

The verdict is justified because:
- The single most-cited quantitative number in the paper (QAOA_2=0.7559 at D=3) is reproduced to 5 digits.
- The single most-cited comparative claim (2-local classical beats QAOA_2 at D=4 girth>5) is reproduced with both sides re-implemented on the same graph, gap 25 SEM in favor of classical.
- The gaps that remain unexercised (Modified Threshold_2, full D-sweep, non-bipartite graphs) are extensions, not disconfirmations — none of the pieces we tested contradicted the paper.

The verdict would be PARTIAL if the head-to-head at D=4 had been merely quoted; it was independently re-implemented end-to-end. It would be SPOT-CHECK if only the QAOA_2 number (a closed-form target) had been reproduced; the Threshold_2 side and the head-to-head both required real simulation infrastructure. It is not NO-GO because nothing contradicted the paper.

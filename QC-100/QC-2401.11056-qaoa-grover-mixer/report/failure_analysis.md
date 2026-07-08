# Failure / limitation analysis — QC-2401.11056 GM-QAOA

Honest critique of this replication. Verdict remains REPLICATED for the four claims exercised, but the following caveats are non-trivial and should be read alongside the headline result.

## 1. Headline structural claim: REPRODUCED (not merely quoted)
- GM-QAOA was **independently reimplemented from the rank-1 operator form** `U_GM(β) = I + (e^{-iβ}-1)|s><s|`, not imported from a third-party GM-QAOA package. The permutation-invariance identity is a strict linear-algebra consequence of that operator, and we saw it come out to `1e-15` across 20 random permutations at two graphs and two depths.
- The X-mixer counter-check (C2, non-invariance) came out with `O(1)` cost-scale deviations on the same permutations — exactly what the paper's structural-blindness contrast requires. So the two-sided version of the identity holds.
- Eq. (8) closed form (`P = sin²((2r+1) arcsin √ρ)`) was reproduced against a self-built statevector to `1e-16` for r ∈ {1,2,3,4}. Machine-precision agreement across four depths is strong.

## 2. Baseline comparison: DONE, with a caveat
- Standard QAOA (X-mixer) baseline **was** run on the same graph and same depths as GM-QAOA. The mixer-choice advantage held **quantitatively**: X-mixer beat GM-QAOA at every depth tested, with an approximation-ratio gap that **grew with p** (`+0.068 → +0.141 → +0.147` at p=1/2/3). Both mixers beat the 0.500 uniform-random baseline, so the differential is real, not a symptom of one ansatz being broken.
- **Caveat: this is one graph.** The paper's Introduction claims the phenomenon as general on structured problems, citing [13,14]. A single 6-node, 8-edge instance is not a distribution. We do not know from these numbers whether the gap sign is graph-dependent, whether it flips on 3-regular or Erdős–Rényi families, or whether more COBYLA restarts would close some of it. Open question #2 turns this into a concrete sweep.

## 3. Mixer-choice advantage: HELD quantitatively on the tested instance
- On Graph A the X-mixer's ratio exceeded GM-QAOA's at every p tested, and the direction and growth of the gap match the paper's Introduction (structural blindness is a real performance cost, ratio-gap monotone in depth). We did not just observe "X ≥ GM"; we observed a monotone-growing gap of the sign predicted, which is a stronger match than a single-point comparison would give.

## 4. Coverage gaps (what we did NOT exercise)
- **C5 — main asymptotic theorem** (exponential-in-n round count on complete-bipartite MAX-CUT): NOT tested. This is the paper's headline new result. A single small-instance CPU run cannot verify or falsify an asymptotic scaling claim. Open question #1 defines the sweep that would test it numerically.
- **GM-Th-QAOA (Theorem 1 threshold variant)**: NOT implemented. Its closed form would be another clean check, but it needs the threshold phase separator, which we did not build. The core Grover-mixer physics is exercised via C1/C2/C3, so this is a coverage gap rather than a physics gap.
- **Complete-bipartite Sec. V example**: only meaningful in the asymptotic sweep — same gap as C5.
- **Weighted, non-binary, and constrained problems**: not touched. GM-QAOA's original motivation (Hadfield et al. 2019) was constrained optimization; the paper's negative results are on unconstrained MAX-CUT. The critique that GM-QAOA loses to X-mixer on MAX-CUT does not by itself close the case on MaxIndependentSet, MaxCoverage, or portfolio-style constraints. Open question #4 covers this.
- **Noise**: everything here is noiseless statevector. The paper's permutation-invariance identity is a strict property of the unitary; noisy channels are not permutation-symmetric in general. The X-vs-GM gap under realistic gate-noise is empirically open (open question #5).

## 5. Optimizer / restart caveats on C4
- Approximation ratios in C4 come from 40 COBYLA restarts per (mixer, depth). This is enough to make the X > GM ordering statistically robust on this graph, but the absolute ratios (especially GM at p=3 = 0.812) may be slightly under the true optimum — COBYLA is a local optimizer on a very non-convex landscape. The **ordering** of X vs GM is what the paper claims and what we verified; the absolute numbers should be read as lower bounds on what a global optimizer would find.

## 6. Software-stack caveat
- We installed Qiskit 2.5.0 alongside NumPy 2.5.0 and Scipy 1.18.0 for cross-check, but the reported numerical claims come from the NumPy statevector simulator we built ourselves. This is a **feature**, not a bug — it means the physics is fully under our control and the permutation experiments are not accidentally leveraging a Qiskit-internal symmetry. But it also means we did not independently verify that a Qiskit-based GM-QAOA implementation would give identical numbers to machine precision; we assume it would.

## 7. Net posture
The paper's core analytical claim (structural blindness via permutation invariance) and its most concrete quantitative predictions (Eq. 8 closed form, X > GM on structured MAX-CUT) are all reproduced independently and to the accuracy the tests can support. The main new asymptotic theorem is out of scope for a single-instance replication and is flagged as such rather than claimed. Verdict REPLICATED is warranted for the four claims exercised; open questions #1–#5 define the concrete next-step work that would extend the replication to the parts we did not touch.

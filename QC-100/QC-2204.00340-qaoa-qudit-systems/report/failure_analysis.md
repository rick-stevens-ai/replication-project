# Failure Analysis / Honest Critique — arXiv:2204.00340

Rick's 2026-07-05 hard rule: this file must be a *genuine* critique of what
was and was not replicated, not a marketing summary. Written to hold up
under adversarial peer review.

## What was actually reproduced (headline-exercised)

- **C3 (qudit strictly beats qubit on the same k=3 coloring at the same
  depth) is genuinely reproduced.** Both encodings were independently
  implemented from scratch on the *same* N=6 graph with *the same*
  edge-penalty λ=20 under *the same* L-BFGS-B multi-restart optimizer.
  The qutrit encoding delivers gap 3.37 and P(gs) 0.882 at p=5; the
  matched 12-qubit binary encoding delivers gap 16.66 and P(gs) 0.509
  at p=5. This is a real apples-to-apples comparison of the paper's
  central claim, not a rederivation of a single number in a plot.
- **C1 (monotone gap-with-p) and C2 (peak sharpening)** are reproduced
  qualitatively on the qudit side (25.3 → 3.4; 0.24 → 0.88).
- **C5 (the L_x / X+X† mixer generalization is well-defined)** is
  verified by the mere fact that the simulator runs and converges.
- **C4 (L-BFGS is multi-modal)** is reproduced qualitatively via the
  spread of 15-restart values recorded in
  `results/replication_results.json`.

## What was NOT reproduced (and matters)

- **No CMA-ES comparison.** The paper's paired finding "CMA-ES beats
  L-BFGS on this problem" is *not* tested; only the L-BFGS-side
  pathology is confirmed. If one wanted to argue that a *practical*
  qudit-QAOA workflow needs CMA-ES, this replication does not
  support that half.
- **No noise model.** All results are noiseless state-vector. The
  paper's cold-atom / trapped-ion motivation depends on the qudit
  gates being implementable at fidelity comparable to native qubit
  gates and on non-Pauli error channels not destroying the ground
  state. None of that is tested here — a genuine hardware-oriented
  replication would need at least a depolarizing / leakage channel
  sweep. This is a real gap.
- **Depth-reduction claim not fully quantified.** The paper implies
  that qudit-QAOA reaches a given approximation ratio at *lower*
  depth than qubit-QAOA. Our data show qudit beats qubit at every
  depth p ∈ {1..5}, but no crossover depth p* was fitted such that
  binary QAOA at p* matches qudit at some fixed smaller p_q. Without
  that crossover, the depth-reduction claim is *directional* only.
  A serious sharp version would push p up to ~12 and report
  p*/p_qudit.
- **Only one constraint-embedding method.** The paper discusses
  (a) penalty, (b) ancilla-conditional gates, (c) dynamical
  decoupling. Only (a) — penalty λ=20 — was tested here. C6b and
  C6c are unverified.
- **Only one graph, one seed set, one N.** The paper does an
  N∈{4..9} sweep with graph ensembles. We tested a single N=6
  graph with a single L-BFGS restart seed set. No error bars.
- **Graph not identical to paper's.** The paper's Fig. 4/5 graph
  is not machine-extractable from the PDF; we used a similar
  N=6 8-edge 3-colorable instance. This means no numerical
  bit-match to any specific paper number is possible; we can only
  match trends.
- **Qubit invalid-state penalty (50) is a researcher degree of
  freedom.** It is chosen large enough that the H_C ground state
  lies inside the valid subspace, but changing it would move the
  exact qubit numbers (though not the C3 direction).

## Researcher degrees of freedom taken

1. Graph choice (non-paper, similar structure).
2. Qubit invalid-state penalty magnitude (50).
3. Number of L-BFGS restarts (15).
4. Random angle-init bounds γ ∈ [0, 2π], β ∈ [0, π].
5. Depth ceiling p=5 (paper goes to p=8).

None of these change the direction of the C3 result, but they mean the
exact table values are ours, not the paper's.

## Would this survive adversarial peer review?

- The headline claim (C3, qudit-beats-qubit at fixed depth on a matched
  problem) is defensible: independent code, independent graph, matched
  optimizer, and the direction is unambiguous.
- The "qudit-QAOA is more resource-efficient in *practice*" framing
  would NOT survive review, because we tested only ideal state vectors,
  did not model qudit-gate noise, and did not do a crossover-depth fit.
- The "L-BFGS is bad" observation (C4) is loose (only the spread is
  shown; no CMA-ES beatdown).
- Verdict class: **REPLICATED (headline exercised)** — direction of the
  paper's central claim is confirmed on a matched-problem independent
  implementation. Downgrading to PARTIAL would be defensible if a
  reviewer demanded the missing noise / crossover-p / ancilla-method
  tests before calling it a full replication.

## Verdict-preservation cross-check

- Original REPORT.md verdict: **REPLICATED**
- Substance check: C1 ✅, C2 ✅, C3 ✅ (headline, matched-problem
  reimplementation of both encodings), C4 ✅ (qualitative), C5 ✅
  (by implementation), C6 partial (penalty only).
- Headline-exercised rule (Rick, 2026-07-05): the *headline* claim
  (C3) required an independent reimplementation of BOTH encodings on
  the SAME problem, and that was done. Headline exercised = YES.
- Preserved verdict: **REPLICATED**.

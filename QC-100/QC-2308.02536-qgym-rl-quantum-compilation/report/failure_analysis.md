# Failure Analysis — QC-2308.02536 (qgym) Replication

**Verdict:** REPLICATED. This document is the honest critique — what this
replication does and does not prove, and where the paper itself is thin.

## 1. We ran the authors' own code — not an independent reimplementation

We `pip install`ed `qgym 0.3.1` (the authors' package) and ran the authors'
own environment classes (`Scheduling`, `Routing`, `CommutationRulebook`,
`BasicRewarder`). This is legitimate — the paper's contribution *is* that
package, and reproducing the paper's PoC is the paper's own reproduction test
— but the reader should be clear that:

- **We did not independently reimplement qgym.** If the qgym environment's
  reward or state calculations do not semantically match what the paper
  claims, we would not catch it. The one deterministic probe we ran
  (H1: `make_blocking_matrix` + ALAP list-scheduler on the Fig. 3A
  circuit) did behave correctly, which is at least one internal-consistency
  check on the state machine.
- **We did not audit the qgym source line-by-line** for the RL loop.

A stricter replication would either reimplement Scheduling from scratch
against the paper's specification or diff qgym source against the paper's
formulae. Neither was done here.

## 2. Paper's headline is qualitative — "match" claims are directional

Paper Fig. 4 reports *curves* (length decreases, reward increases) but
prints **no numeric endpoint values** and gives **no seeds**. Consequently
"reproduced" here means:

- The **sign and trend** of the training-dynamics change agree
  (length 21.5 → 6.8; reward −38.3 → −2.9).
- The trained-agent quality on random test circuits reaches **ALAP parity**
  (mean 2.66 = ALAP mean 2.66 at 100% completion on 50 held-out circuits).

We deliberately do **not** claim "our final mean length matches the paper's
final mean length" — that would be un-checkable because the paper never
prints such a number. Any strict reviewer should note that "matches Fig. 4"
is a qualitative statement here, not a numeric one.

## 3. Reproducibility hole: PPO hyperparameters are unreported

The paper says only "vanilla PPO, 10^5 steps." This is ambiguous:

- Our first pass used `n_steps=256, n_epochs=4` (an older SB3 example
  setting sometimes cited as "vanilla"). **PPO collapsed** into a
  degenerate policy that keeps advancing the cycle counter (each step is a
  safe −1 instead of risking a −5 illegal-action penalty). Episode length
  went the *wrong way* — 39 → 1885 for one seed; 63 → 504 for another.
- We then switched to SB3's own defaults (`n_steps=2048, n_epochs=10,
  ent_coef=0.01`) at the same 10^5 step budget. PPO converged cleanly and
  reproduced Fig. 4A/B.

This is a **real reproducibility footnote on the paper.** Whether the PoC
"works" depends sensitively on hyperparameter choices the paper never states.
A strict reviewer could reasonably call this a paper-quality issue rather
than a replication triumph. We take the most defensible reading of
"vanilla" (= SB3's own defaults) and report that it works; we document the
alternative reading and its failure.

## 4. PPO matches ALAP but does not strictly beat it (on our test distribution)

50 random ≤5-gate test circuits, drawn with fixed seeds inside the same
qgym env for both policies:

| Metric | ALAP | PPO |
|---|---|---|
| Completion | 100% | 100% |
| Mean cycles | 2.66 | 2.66 |
| Median cycles | 2.0 | 2.0 |
| Max cycles | 11 | 11 |

The paper's headline is that vanilla RL "can offer improvements over a
standard ALAP method." Our data support the weaker "can reach ALAP
quality." An adversarial reader could call this an unimpressive RL result:
after 10^5 environment steps of learning, PPO ties a hand-coded greedy
heuristic. The paper does not claim a strict beat at PoC scale, so this is
consistent — but "matches Fig. 4 trends AND matches ALAP on outcomes"
should not be over-read as "RL wins."

## 5. No classical-compiler baseline for Scheduling

The paper's PoC compares vanilla PPO only against **ALAP-inside-qgym**, not
against mature classical compilers (Qiskit `transpile`, Cirq,
`t|ket>`). We match the paper's baseline choice for fidelity, but this
means neither the paper nor this replication has evidence that a trained
qgym Scheduling agent is competitive with production compilers.

- Our companion **Routing** run *did* include Qiskit `SabreSwap` and
  `BasicSwap` baselines, but PPO under the training budget we allotted did
  not converge to completing routing episodes (see
  `evidence/routing_results.json`). So that Routing PPO-vs-classical
  comparison is a non-completion artifact and is **not** used to argue for
  or against the paper's Scheduling PoC.

The RL-vs-real-compiler question is entirely open (see open question #5:
qgym-agent-as-Qiskit-PassManager-pass).

## 6. Scale is a toy proof-of-concept

- 3 qubits, 7-primitive gate set, ≤5-gate random circuits, 10^5 training
  steps.
- The paper is honest that this is a PoC.
- **No claim can be made** from this data — or from ours — about scaling
  to 20+ qubit hardware, hundreds of gates, native-gate constraints, or
  noise-aware compilation.

Anyone reading either the paper or this replication should not extrapolate
to "qgym RL agents are useful for real quantum compilation." The paper
establishes the *framework and the tiniest PoC*; scaling is future work,
which is precisely what open questions #1, #3, #4, and #5 attempt to scope.

## 7. Companion Routing run did not converge — excluded from verdict

`evidence/routing_results.json`: PPO on Routing (5-qubit path) vs Qiskit
`SabreSwap`/`BasicSwap` did not complete episodes in the allotted budget.
Its swap counts are therefore non-completion artifacts. Kept for
transparency; **excluded** from the verdict logic. This does *not* argue
against the paper — the paper does not make a Routing training claim of
this form — but it is a caution against treating any Routing metric in
this replication as evidence for or against the paper.

## Bottom line

**REPLICATED** — the paper's Scheduling PoC (mechanism + training dynamics
+ ALAP-parity outcome + software works) does reproduce on real qgym
simulation with the SB3-default reading of "vanilla PPO."

**With four honest caveats:**

1. We ran the authors' own package rather than an independent
   reimplementation.
2. "Match" for Fig. 4 is directional/trend-level; the paper prints no
   numeric endpoints.
3. Reproducibility is hyperparameter-sensitive in a way the paper does not
   document — an alternative "vanilla" reading (`n_steps=256`) fails.
4. RL matches ALAP but does not strictly beat it at this PoC scale, and
   there is no comparison to a mature classical compiler.

None of these caveats overturn the verdict. All of them should be visible
to any downstream reader.

# Failure Analysis — QC-2204.13641 Real Quantum Amplitude Estimation

**Verdict:** REPLICATED · **Backfill:** 2026-07-06

The verdict is REPLICATED because the paper's headline scaling claim was
independently reimplemented and quantitatively confirmed. This document is
the honest inventory of *what the replication does not settle*, because a
"REPLICATED" label without scope discipline is worthless.

## 1. What was actually exercised (the strong claim)

The paper's central quantitative claim — Fig. 6, the log–log
`N_oracle` vs `1/eps` scaling plot showing RQAE at slope ~1 and classical
Hoeffding at slope 2 — was reproduced:

- **RQAE slope: 0.959** (paper prediction: ~1.0). Independent
  reimplementation of Algorithm 1 from the pseudocode; real shot-based
  simulation on `AerSimulator()` (not a statevector shortcut); 25
  repetitions per (a_true, eps) config with distinct seeds.
- **Classical slope: 2.000** (theory: 2.0). Matched-oracle Hoeffding
  reference in the same code path.
- **Coverage: 100%** across all 12 configs (paper guarantees ≥95%). This
  is a *strong* pass, but note it is arguably *too* strong (see §3
  below).
- **Sign recovery on a = -0.4: correct.** This is the paper's key novelty
  vs canonical QAE/IQAE (which recover only |a|).

**Headline exercised: YES.** The specific graph on which the verdict rests
is the RQAE-vs-classical scaling plot, and both slopes match theory to
0.05 and 0.001 respectively.

## 2. Boundaries of the replication (scope limits)

These are limits of the replication design, not defects of the paper. They
constrain the *generalizability* of our REPLICATED verdict but not its
correctness on the exercised headline.

### 2.1 Toy oracle only
State preparation was a single-qubit `R_y(2 arcsin c)` rotation with a
known analytic amplitude. The paper's motivating applications (option
pricing, expectation-value estimation, Monte Carlo integration) involve
multi-qubit `A` operators whose gate count and depth directly inflate the
`(2k+1)`-oracle-call cost in practice. **We did not touch that regime.**
The practical speedup on a realistic pricing circuit is not established
here, only the theoretical one.

### 2.2 No noise model
`AerSimulator()` was run noiseless — only real Bernoulli shot noise from
measurement. No depolarizing, T1/T2, or readout error. The paper's own
discussion of noise robustness is untouched. On real hardware at the
`k_max` depths implied by `eps = 1e-3` (dozens of Grover applications),
two-qubit-gate error would very plausibly flatten the slope back toward
the classical rate. This is captured as open-question #1.

### 2.3 No comparison to other QAE variants
The classical Hoeffding baseline confirms the `1/eps^2` reference, but the
paper's *actual* competitors are the other QAE variants:
- **MLQAE** (Suzuki et al. 2019) — maximum-likelihood post-processing.
- **IQAE** (Grinko et al. 2019) — iterative QAE.

Both also achieve near-quadratic scaling; both are broadly available in
`qiskit-algorithms`. We did not implement them, so **we cannot state
whether RQAE's constant is competitive with IQAE** beyond the
sign-recovery feature. If the only genuine advantage of RQAE turns out to
be sign recovery, that's still a real advantage, but the framing
matters. Open-question #2.

### 2.4 Numerical constant is 2–3× below Fig. 6 visual read
At `eps = 0.005` our mean `N_oracle = 39,220`; a visual read from Fig. 6
suggests ~`10^5`. Slope matches; **constant does not.** Candidate causes:
(a) our toy oracle is much cheaper per shot than the paper's implicit
oracle; (b) our `(a_true, eps)` grid differs; (c) an accounting
difference (whether `A_b^†` counts as one or two oracle calls). This does
not affect the slope-based headline claim but it does mean we are not
reproducing the paper's exact absolute numbers.

### 2.5 100% coverage may indicate over-conservative intervals
The paper guarantees ≥95% coverage; we observed 100%. This is likely
because our RMSE is well below `eps_target` in every configuration —
i.e., the confidence intervals produced by the Hoeffding bound are
loose, and empirical errors are systematically much smaller than the
declared precision. This is *not* a failure per se, but it means we are
paying `N_oracle` for tighter precision than the interval reports. A
truly tight confidence procedure (Clopper–Pearson, or a Bayesian
posterior interval) might give a very different `N_oracle` at matched
declared precision.

### 2.6 Two transcription bugs in Eq. (14) and Eq. (19)
Both bugs were caught and fixed during implementation (documented in
`REPORT.md` §6). They are *asymptotic-slope-compatible* but destroy the
finite-`eps` constant. Future replicators should:
1. Confirm Eq. (14) numerator is `pi/4`, not `pi/2`.
2. Confirm `N_i = ceil(1/(2 p^2) log(2T/gamma))` has `p` **squared** in
   the denominator.

This is a caution about the paper's presentation, not a bug in the
paper: the equations are correct; casual readers just get them wrong.

## 3. What is NOT proven by this replication

For clarity on the scope of the verdict:

- **NOT proven:** RQAE beats MLQAE or IQAE on non-sign-recovery tasks.
- **NOT proven:** RQAE's quadratic scaling holds under realistic noise.
- **NOT proven:** RQAE is practical for multi-amplitude / vector
  estimation.
- **NOT proven:** RQAE gives a quantitative speedup on a real
  option-pricing benchmark (Woerner-Egger style).
- **NOT proven:** The paper's absolute `N_oracle` numerical constants
  transfer to non-toy oracles (our constant is 2–3× below theirs at
  `eps = 5e-3`).

Each of these is a concrete follow-up in `open_questions.json`.

## 4. Confidence in the verdict

**REPLICATED, medium-strength.** The evidence for the *slope-based
headline* is strong (independent reimplementation, real shot noise,
25×3×4 = 300 RQAE runs, slope 0.959 vs 1.000). The evidence stops there.
This replication does not license claims beyond "RQAE, on a toy oracle,
noiseless, reproduces the theoretical `1/eps` scaling and correctly
recovers sign."

If the paper is being cited for anything else — noise robustness,
finance-application practicality, superiority over IQAE/MLQAE — that
claim is *not* validated by this work and would need one of the
open-question follow-ups to run first.

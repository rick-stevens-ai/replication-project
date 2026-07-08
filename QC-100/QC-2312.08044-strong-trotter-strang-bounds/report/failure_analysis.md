# Failure Analysis — QC-2312.08044 (honest critique)

This document is written to Rick's 2026-07-05 honest-critique standard. It records
what this replication actually established, what it did NOT establish, and what a
skeptical reviewer would push back on.

## Verdict: REPLICATED on the headline-exercised claims

**But that verdict scope is narrower than the paper's overall contribution, and this
document exists to say so plainly.**

## 1. Was the strong-Strang bound independently reproduced?

**Partially — the SCALING was reproduced, the CONSTANT tightness was not.**

- Reproduced: 2nd-order Strang operator-2-norm error scales as `r^(-2)` on both TFIM
  (slope −2.0129, +0.65%) and Hubbard dimer (slope −2.0180, +0.90%). This is the
  "strong" sense in that we used the operator 2-norm, not just an expectation-value
  observable — worst-state error.
- NOT reproduced: the paper's specific state-dependent PREFACTOR was not compared
  head-to-head with the standard Childs-Su-Tran-Wiebe commutator prefactor on a
  chosen state. Without that comparison we cannot claim we reproduced the paper's
  quantitative *tightness advantage* — only the scaling exponent, which was already
  known pre-paper. This gap is captured as open question 2.

## 2. Operator-norm error vs t reproduced for the paper's specific Hamiltonian vs quoted?

**No — we tested different Hamiltonians than the paper's headline case.**

The paper's central novelty runs on the hydrogen atom in real space (a specific
unbounded Hamiltonian) and reports an `N^(-1/4)` slope. We tested TFIM and Hubbard
dimer, both bounded, both explicitly outside the pathological regime. So we reproduced
the *standard-regime table entries* (which the paper is not the first to derive; it
recovers them as a consistency check) on Hamiltonians *different from* the paper's
headline exhibit.

A tighter replication would:
- Numerically emulate the paper's specific quoted operator-norm-error-vs-t curves
  on the exact Hamiltonians the paper uses (Figure X in the paper's numerical section
  — a full paper-body read via nougat MMD would resolve the specific instance).
- Or, at minimum, exercise C4 on a real-space discretized hydrogen atom (grid or
  Sinc basis), which is the paper's actual headline.

Neither was done. C4 is flagged as not-tested in the claims table.

## 3. Was the comparison against the standard weak Trotter bound made?

**No — this is a real gap.**

The paper's structural claim is that the state-dependent (strong) bound is at least
as good as, and often strictly tighter than, the standard Childs-Su-Tran-Wiebe
commutator bound. We did NOT compute the CSTW prefactor as a baseline for our TFIM
or Hubbard instances, so we cannot say by how much (if any) the paper's bound
improves on the state we tested. This is open question 2 with a concrete numerical
recipe attached.

## 4. Did the tightness advantage hold quantitatively?

**Not adjudicated.** We measured slope match (yes, within ~2%). We did not measure
prefactor ratio between the paper's bound and the standard CSTW bound. On the states
we used (`|+>^n` for TFIM, uniform half-filled superposition for Hubbard), it is
entirely possible that the state-dependent bound coincides with or barely improves on
CSTW — those states are not fat-tailed and lack the higher-moment suppression the
paper's bound exploits.

To adjudicate this: prepare a low-energy variational state, compute both prefactors,
report the ratio. This is open question 2.

## 5. Additional gaps we would flag on peer review

- **No higher-order Suzuki formulas tested** (only p=1 and p=2). The paper's general
  p-th-order theorem is only sampled at 2 of infinitely many orders. Open question 1.
- **No genuine chemistry-scale instance** — Hubbard dimer is q-chem-flavored (4 modes,
  16-dim Fock) but is not a real molecular-electronic-structure benchmark
  (H4/STO-3G, LiH, Fermi-Hubbard 2x4). Open question 4.
- **No integration with LCU / qubitization cost models** — the paper is presented
  as having chemistry implications; whether the state-dependent constant helps in
  the modern hybrid Trotter-LCU cost regime is an open methodological question.
  Open question 3.
- **No Pareto-frontier study** of the joint (order p, steps r, state quality) trade.
  Open question 5.

## 6. Judge-panel disagreement — what it means

Two Argo judges split (`argo:gpt-5.2` PARTIAL, `argo:gpt-4o` REPLICATED). Both are
correct on complementary axes and the disagreement is genuine information, not
noise:
- gpt-5.2 (PARTIAL) is calibrated to the paper's OVERALL contribution — since C4
  is the novelty and it is not tested, PARTIAL is fair.
- gpt-4o (REPLICATED) is calibrated to the headline-exercised sub-scope — for
  C1+C2, REPLICATED is fair.

Per Rick's headline-exercised rule, we adopt REPLICATED for the sub-scope actually
exercised and mark C4 explicitly not-tested. If the wave-level rule tightens to
"paper novelty must be exercised", this replication would drop to PARTIAL.

## 7. What would change the verdict

- Reproducing C4 (hydrogen `N^(-1/4)`) at even qualitative resolution would strengthen
  REPLICATED substantially.
- Finding the CSTW prefactor is uniformly TIGHTER than the paper's state-dependent
  bound on our test states would move the verdict toward CONTRADICTED for C3.
- Finding a slope significantly off from -1 or -2 (>>5%) at large r on a canonical
  bounded Hamiltonian would move the verdict toward CONTRADICTED for C1/C2. This did
  not happen — all eight slopes are within ~2% and monotonically converge toward the
  integer as r grows.

## 8. Bottom line

The paper's standard-regime scaling machinery replicates cleanly on two canonical
Hamiltonians in operator-2-norm and state error. The paper's actual scientific
novelty (unbounded-Hamiltonian pathological scaling) was not adjudicated by this
exercise, and neither was the tightness advantage of the state-dependent constant
over the standard CSTW bound. Both gaps are captured as concrete open questions
with executable next steps.

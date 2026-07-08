# Failure Analysis / Honest Critique

**Paper:** arXiv:1801.02809 — Byrnes, Forster, Tessler (2018).
**Verdict:** REPLICATED — but with meaningful scope caveats spelled out below.
This document is not defensive; it lists what we did NOT verify and why that matters.

## 1. Scope of what was reproduced vs merely quoted

The paper has three layers of claim:

1. **Spectral structure of H = P_S + P_T** (Eq. 10): paired eigenvalues 1 ± c_n plus
   |N−M| unpaired 1's plus bulk zeros.
2. **Perfect Rabi oscillation** of the Eq. 12 state at t = π/(2 c_n), and the
   corresponding gate-iteration reduction.
3. **Scaling behavior** of the mechanism as (N, M, D) grow — the abstract's
   "α ≈ 1" query-complexity exponent and Fig. 1(d) plots.

**What we truly verified:** layers 1 and 2, in full, with two independent
implementations (numpy statevector + Qiskit Aer statevector) that agree bit-for-bit.

**What we did NOT verify:** layer 3 — the scaling analysis. We ran a single
(N, M, D) = (5, 5, 32) point. The paper's canonical scaling ratios (M/D = 0.05,
MN/D = 0.25) correspond to D = 100; we chose D = 32 for a clean 2^5 qubit register.
This is a real gap. Our data is *compatible* with the scaling story but does not
independently confirm it.

**Verdict impact:** REPLICATED for the core mechanism; NOT tested for the scaling
claim. The verdict word stays REPLICATED because the *headline* mechanism (Eq. 12
state → perfect amplitude amplification) reproduces cleanly. If the verdict rubric
required scaling verification, this would drop to PARTIAL.

## 2. Independent implementation status

- Multiphase iteration U_G U_O = (I − 2 P_S)(I − 2 P_T): coded from scratch as a
  matrix, then wrapped into a Qiskit `Operator` for the Aer path. ✅ independent.
- Eq. 12 initial-state construction: coded from scratch by diagonalizing H and
  picking the largest-c_n eigenpair with the Eq. 9 sign convention. ✅ independent.
- Success-probability curves P_T(t) and P_T(k): computed by us, not quoted. ✅
- Standard-Grover baseline: coded from scratch using textbook H^⊗n prep + diffusion.
  ✅

## 3. Comparisons to related fixed-point / phase-schedule variants — NOT DONE

The paper sits in a literature that includes:

- **Grover 1998 π/3-phase fixed-point search** — a discrete fixed-point Grover
  variant. Not compared.
- **Yoder–Low–Chuang (2014) fixed-point amplitude amplification** — a QSVT-family
  fixed-point Grover that saturates the Nayak-Wu lower bound. Not compared.
- **Chakraborty–Novo–Ambainis–Omar (2016) spatial search** — Hamiltonian-based
  search on graphs. Not compared.
- **Gilyén–Su–Low–Wiebe (2019) QSVT unification** — subsumes fixed-point search.
  Not compared.

We anchored *only* against textbook single-target Grover (C5). This is enough to
confirm we implemented amplitude amplification correctly, but it does not answer
"is the generalized Grover of this paper meaningfully better than Yoder or π/3?"
That answer requires further work — see open question Q4.

## 4. Do the claimed advantages hold quantitatively?

- **Constructed-vs-naive gap:** 0.9991 vs 0.30 peak P_T. ✅ Confirmed with wide
  margin at (N,M,D)=(5,5,32).
- **Predicted period t = π/(2 c_1):** matches to 0.3%. ✅
- **Robustness to marked-item-count uncertainty:** paper claims this;
  replication did NOT test it. Would require sweeping (N, M) with a mismatched
  "assumed M" vs true M and measuring peak P_T. Not done.
- **Query-complexity scaling α ≈ 1:** paper claims via Fig. 1(d) at D=100;
  replication did NOT test at multiple D. Not done.

## 5. What could still be wrong

- **Convention slippage on Eq. 9:** the paper's derivation fixes signs of v_+, v_−
  via ⟨P_T v_+ | P_T v_−⟩ < 0. Our implementation adopts this. If we had it
  backwards, we would observe P_T = 0 at t = π/(2 c_1) instead of P_T = 1. We see
  1.0000, so the sign is right — but this is a subtle point worth flagging.
- **D=32 vs D=100:** the small-D regime may hide finite-size effects that vanish
  at D=100. Not tested.
- **QR-generated random source states with seed 20260703:** results depend on the
  specific random matrix. We did NOT do an ensemble average over seeds; peak P_T
  and c_n values are single-realization numbers. A seed-ensemble study would
  produce error bars — not done.
- **No noise:** ideal Aer statevector only. Real quantum hardware would see the
  0.9991 peak erode. See open question Q1.

## 6. Trust score honest

- Core mechanism (Eq. 10 spectrum, Eq. 12 state, gate iteration to P_T ≈ 1): high
  confidence, two independent implementations, cross-checked to 10^−6.
- Broader story (scaling, robustness, comparison to other fixed-point variants):
  UNVERIFIED. Compatible with what we saw, not confirmed.
- Overall verdict: **REPLICATED** for what was in scope. The 5 open questions
  (Q1–Q5 in `open_questions.json`) each point to a concrete unverified layer.

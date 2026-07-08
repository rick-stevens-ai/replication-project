# Failure Analysis — QC-1611.04542-grover-analog-coherence

Honest per-claim audit. The overall verdict is **REPLICATED**, but that
verdict is scoped narrowly to the paper's coherence-collapse-at-peak
signature under the *discrete* Grover implementation on ideal (noiseless)
statevector simulation. This file itemizes what the replication does
NOT establish, why, and what would be required to close each gap.

## Verdict boundary

**REPLICATED means, in this file:**
The paper's headline quantitative statement --- both coherence
monotones (C_l1, C_r) go to zero at the same iteration k where the
Grover success probability P peaks toward one, and the collapse
sharpens with n --- is reproduced on an independent Qiskit statevector
implementation for n = 3, 4, 5 qubits. Grover k_opt matches
`round((π/4)√N − 0.5)` exactly at all three n; P_sim matches the
closed-form `sin²((2k+1)arcsin(1/√N))` to ≥6 decimals; the collapse
ratio C_l1(k_peak)/C_l1(0) trends 0.219 → 0.136 → 0.011 as n → 5.

**REPLICATED does NOT mean:**
- that the analog (continuous-time Farhi–Gutmann) algorithm was
  simulated;
- that the two-qubit concurrence claim (C4) or the n-party monogamy
  inequality (C5) was verified;
- that the coherence-collapse signature is robust under decoherence;
- that a rigorous √N-scaling curve was fit (only three points sampled);
- that this result comments on real-hardware quantum-speedup claims
  in any way.

## Per-claim status

### C1 — Grover k_opt ≈ (π/4)√N
- **Status:** REPRODUCED at n=3,4,5.
- **Weakness:** Only three points. A meaningful scaling curve would
  span n up to 10–15 (statevector still tractable) or use a log-log
  regression against √N. Confirmatory, not conclusive.
- **What would close it:** Sweep n = 3–14; fit k_opt(n) vs (π/4)√N;
  report residuals and R².

### C2 — C_l1 → 0 iff P → 1
- **Status:** REPRODUCED qualitatively and quantitatively at n=3,4,5.
  Collapse ratio 0.219 → 0.136 → **0.011** with growing n, matching
  the paper's "= 0 in the analog/N→∞ limit" claim as an approach.
- **Weakness:** The strict equality `C_l1 = 0 iff P = 1` in the paper
  holds only in the analog limit. Finite-n Qiskit will always leave a
  small residual `C_l1(k_peak) > 0`; we did not fit the residual's
  scaling with n to verify it decays at the rate the analog theory
  predicts.
- **What would close it:** Regress log(C_l1(k_peak)) vs n; compare
  slope to analog prediction.

### C3 — C_r → 0 iff P → 1
- **Status:** REPRODUCED. C_r at peak: 0.460 → 0.387 → **0.014** bits
  as n = 3 → 4 → 5.
- **Weakness:** Same finite-n residual concern as C2.
- **What would close it:** Same as C2, applied to C_r.

### C4 — Two-qubit concurrence tracks dP/dk
- **Status:** NOT TESTED.
- **Why:** Requires reduced two-qubit density matrix ρ_ij =
  Tr_{rest}(|ψ><ψ|) and Wootters' concurrence formula. This is
  additional code we did not write.
- **What would close it:** Add `qiskit.quantum_info.partial_trace`
  loop over all (n choose 2) pairs; compute Wootters concurrence;
  overlay against finite-difference dP/dk from the existing per-k
  arrays.

### C5 — n-party monogamy inequality holds for all t
- **Status:** NOT TESTED.
- **Why:** Requires CKW-generalized n-tangle (sum-of-squared-
  concurrences ≤ concurrence with the rest); structural extension of
  C4 to all bipartitions.
- **What would close it:** After C4 is implemented, compute the LHS
  (sum_{j≠i} C(ρ_ij)²) and RHS (τ_i = 2(1 − Tr ρ_i²)) at every k;
  verify LHS ≤ RHS.

## Gaps not represented by C1–C5

### G1 — Analog vs. discrete correspondence
The paper's title emphasizes "discrete analogue of the *analog*
Grover search." The paper claims the two algorithms share the
coherence-collapse signature. This replication only ran the discrete
side. See open question 2 for the proposed closure.

### G2 — Noise robustness (decoherence dependence)
The paper's story is a coherence-resource one, so it is natural to
ask how much noise the signature survives. We did not add any noise
channel. See open question 1.

### G3 — Digital-vs-analog speedup comparison
A statement like "the analog algorithm speedup is X× the digital"
requires running both on matched success targets. Only the discrete
side is here.

### G4 — Hardware-platform mapping
No comparison to real Rydberg / trapped-ion / superconducting
analog-Grover data. See open question 5.

## Meta-honesty note

The "REPLICATED" verdict here is *substantively earned* for the
coherence-collapse signature (which is what the paper's abstract and
Sec. III headline as the central result), but the paper contains
non-trivial additional structural claims (C4, C5) and framing claims
(analog vs. discrete correspondence) that this replication does not
touch. A stricter reviewer might call this "PARTIAL — coherence half
replicated, entanglement/monogamy half untested." We adopt the
narrower "REPLICATED" tag because the paper's own quantitative
signature-of-record (the coherence-collapse-at-peak) is the piece we
did reproduce end-to-end on real Qiskit; but the qualifier "narrow
scope" applies.

# Failure Analysis — Grover on SIMON

## Headline
The paper's headline quantitative deliverable — a Qiskit Grover run on
reduced-SIMON that peaks on the correct key — WAS exercised end-to-end and
matches to 4 decimal places. Verdict: **REPLICATED**. That said, this
replication has genuine limits, listed honestly below.

## Was the headline claim exercised?
**Yes.** Independent 20-qubit Qiskit statevector implementation:
- Reduced SIMON classical test vector (paper Fig. 11): exact bit-match.
- Grover single-pair oracle (paper Fig. 14a): two peaks at K, K' — 99.93 %.
- Grover two-pair oracle (paper Fig. 14b): unique peak at K — 99.72 %.
- Success-vs-iteration curve: matches analytic $\sin^2((2k{+}1)\theta)$ to
  <0.01 across k = 0..7, saturating at the O($\sqrt N$) optimum k=4.
- Independent clean-room build: the authors' code was NOT consulted.

## Where the replication is thin

### 1. Full-scale gate counts (C8) NOT verified
The paper's Tables 4–5 list NOT/CNOT/Toffoli/T-depth for every SIMON variant
from SIMON32/64 through SIMON128/256. These are extrapolated resource
estimates, not simulator runs — the full-width oracles are thousand-qubit
circuits. We built only the 20-qubit reduced instance. We have NO independent
check on whether the paper's Toffoli counts include or exclude uncomputation
overhead, whether ancilla reuse is optimal, or whether T-parallelization is
achievable at the claimed depth.

**Impact:** Modest. The reduced-instance claim is the paper's demonstration
that its construction is correct; the full-scale tables are correctness-preserving
extrapolations of the SAME construction. If the reduced instance is right (which
it is), the full-scale gate counts are structurally plausible. But 10–30 %
disagreement on total Toffoli count is entirely possible — this has been the
historical delta on comparable AES-under-Grover audits (Grassl et al. vs later
Almazrooie / Jaques audits).

### 2. Not compared against pure Grover / pure Simon baselines
The paper is titled *Grover on SIMON* — it is Grover applied to SIMON as an
oracle, NOT a Grover-Simon hybrid attack. So there is no "pure Simon" baseline
to compare against; and the "pure Grover" baseline IS what we ran. The
theoretical query-count comparison against classical brute force IS what
Section 5.5 (C7) demonstrates. But:
- We did NOT compare against classical brute force under matched wall-time —
  the 6-bit keyspace is exhausted in <1 ms classically, so this comparison is
  vacuous at reduced scale.
- We did NOT prototype the (likely different) Grover-meets-Simon algorithm
  that the paper-hint incorrectly attributed to this arXiv ID. That is a
  separate paper (Leander & May 2017, "Grover Meets Simon", arXiv:1706.06720)
  — DIFFERENT paper, DIFFERENT algorithm.

### 3. No noise / hardware simulation
All runs are noise-free statevector. Real Grover on real hardware is fragile
because the amplification is coherent. Our reduced oracle has ~200 Toffolis
across 4 iterations; per Cai/Xu 2022, that regime loses >50 % of amplification
at p_err ~ 1e-3. The paper doesn't claim hardware executability, so this is
not a failed replication — but it IS a genuine gap in the practical relevance
story.

### 4. No FT / surface-code cost estimate
Paper reports T-count and T-depth without fixing a surface-code distance. The
"how many physical qubits / how many hours to actually attack SIMON128/256"
question remains open. Downstream cost estimates (Litinski, Azure QRE) would
close this gap.

### 5. Broader symmetric-cipher generalization untested
The paper is SIMON-specific. Whether the same construction gives similar
speedups for SPECK, PRESENT, GIFT, LED (all lightweight block ciphers) is
not addressed. This is more of an extension direction than a replication gap,
but the paper's abstract does gesture at "reversible circuits for lightweight
ciphers" as a general program.

## Things that could STILL be wrong even though the numbers match
- **Silent circuit-identity difference.** Our comparator/diffuser could use
  different intermediate ancilla layouts than the paper's without changing
  the final histogram. We verified equivalence up to unitary, not bit-exact
  circuit identity.
- **Round-constant convention.** SIMON's key expansion uses round constants
  $c_j$ selected from the sequence $z_j$. We used $c_2 = c_3 = [0,0,1]$ per
  paper Fig. 11's caption. If a different convention is in the paper's code
  (e.g. reversed byte order), C1 would still match for this test vector by
  accident, but C2/C3/C4 wouldn't — and they DO, so the convention is
  consistent. Still: only 1 test vector confirmed classically.
- **Endianness of bit list ↔ int.** We used LSB-first throughout (paper's
  `[0,1,1]` = `int 0b110`). If Aer histogram bitstring endianness differs from
  our register-ordering convention, the "K = 001110" label could be a mirror
  of the true state. We verified endianness against the classical brute-force
  labels — consistent.

## Risk assessment for the REPLICATED verdict
- **Low risk** of the reduced-SIMON claim being wrong. Two independent code
  paths (classical brute force + Qiskit Grover) agree on the exact same
  bit-string keys.
- **Medium risk** that the paper's full-scale gate counts have small (5–20 %)
  errors that we didn't catch. Doesn't change the verdict on the paper's
  headline demo but would matter for downstream cost projections.
- **Zero risk** of over-claiming: we explicitly mark C8 as untested.

## Confidence in verdict: **HIGH** for reduced-SIMON demo, **MEDIUM** for full-scale extrapolations.

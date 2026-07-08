# Failure Analysis — W2-semiclassical-qft (Honest Critique)

**Paper:** Griffiths & Niu, PRL **76**, 3228 (1996).
**Verdict preserved:** REPLICATED (Coverage 9/10, Agreement 10/10).

This document is deliberately hostile to the replication. Everything below
is a real limitation, not a formality.

## 1. What the replication genuinely established

- **Independently reimplemented from scratch.** Two entirely separate
  numpy implementations (Method A = explicit iQFT unitary applied to the
  pre-iQFT state vector; Method B = branch-enumerated iterative
  measure-and-feed-forward). Both coded clean-room from the paper's text.
  Neither borrows from any pre-existing QPE library. **HEADLINE EXERCISED.**
- **Output distribution reproduced.** Not just amplitudes, not just MAP
  estimates, but the full per-outcome probability distribution over
  $2^k$ classical strings, compared distribution-to-distribution. TV
  distance = $\mathcal{O}(10^{-15})$ across 8 (φ, k) points.
- **Comparison against the all-quantum canonical baseline.** Method A
  IS the canonical all-quantum inverse QFT. Method B is the paper's
  proposed replacement. The comparison is direct.
- **Coverage of the parameter space.** Both exactly-representable phases
  (which must return the exact integer $y$) and non-representable phases
  (0.1, 0.7, 1/3) at k in {3, 4, 5}. Exactly-representable phases catch
  bit-order bugs; non-representable phases catch amplitude / spread bugs.

## 2. What the replication does NOT establish

### 2.1 Gate count / circuit depth reduction — NOT quantitatively verified
Griffiths–Niu's motivation is that the semiclassical version eliminates
all controlled-phase gates (nominally $\mathcal{O}(k^2)$ two-qubit
operations in the coherent iQFT) and replaces them with $k$ single-qubit
rotations plus $k$ mid-circuit measurements. **We did not tabulate this.**
No side-by-side gate inventory exists in `results.json`. A truly rigorous
replication would produce a table:

| k | Coherent iQFT: 1q gates | Coherent iQFT: 2q gates | Semiclassical: 1q gates | Semiclassical: measurements |
|---|---|---|---|---|

and confirm the scaling numerically. This is straightforward but was not
done. Impact on verdict: coverage $9/10$ instead of $10/10$.

### 2.2 Qubit-count reduction — arguably not a real reduction
The paper's practical value is often stated as "qubit reduction," but the
counting-register size does not change (you still need $k$ qubits to
extract a $k$-bit phase estimate --- what changes is that the
qubits can be reused, since each one is measured and freed before the
next arrives). We did not exercise the qubit-reuse variant (where the
$k$ counting-qubit register is compressed to a single reused ancilla).
This is arguably the paper's most practically important corollary and
was not touched. **Legitimate gap.**

### 2.3 Noise / measurement error — not exercised
All experiments are ideal: exact distributions, no shot noise, no
readout error, no gate error. The semiclassical scheme has an
asymmetric vulnerability: a wrong measurement bit propagates a coherent
phase error to every subsequent qubit via the feed-forward. This
asymmetry vs.\ coherent-iQFT gate errors could invert the practical
verdict on real hardware and was not tested here.

### 2.4 Hardware-runtime overhead — not measured
On real superconducting hardware, mid-circuit measurement + classical
feed-forward is not free (microseconds per operation, and it forces a
reset barrier). The paper's runtime-advantage claim depends on the
mid-circuit-measurement cost being less than the saved two-qubit-gate
cost. We did not use any hardware calibration numbers.

### 2.5 Paper's specific quoted numerical example — not lifted verbatim
Griffiths–Niu is largely a proof-based paper (the equivalence is a
theorem, not a data table), so there is no obvious canonical
distribution to match. Our 8 test points are of our own choosing.
A stricter replication would identify any specific numerical illustration
in the paper (if present) and reproduce it bit-for-bit.

### 2.6 Debugging bugs found and fixed --- documented, not hidden
The first two implementations disagreed catastrophically (TV~1.0) due to
inconsistent bit-order between the two methods. This was diagnosed
using $\varphi = 0.375 = 0.011_2$ at $k=3$ and fixed by aligning both
methods to the same index convention. The buggy version is preserved as
`replicate_subagent_buggy.py`. This is transparent (a strength) but does
underline that the equivalence is only "obvious" once conventions are
locked; a reader repeating this work should sanity-check on
exactly-representable phases before trusting anything.

## 3. How this changes the verdict

The verdict **REPLICATED** stands because the paper's actual claim ---
distribution equivalence between coherent iQFT and semiclassical
measure-and-feed-forward --- is verified to machine precision across the
parameter space. The gaps listed in section 2 are extensions and
corollaries, not the headline theorem. Coverage $9/10$ (not $10/10$)
precisely captures the gate-inventory / noise / hardware-runtime
omissions.

If the verdict were required to encompass "the paper's semiclassical
scheme is superior on real hardware," that stronger claim would be
**PARTIAL** at best given what we exercised. But that is not the paper's
central claim, and it is not what REPLICATED is asserting here.

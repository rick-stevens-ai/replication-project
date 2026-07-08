# Failure analysis / honest critique — QC-100 W3
### Cleve, Ekert, Macchiavello, Mosca 1998, *Quantum Algorithms Revisited*

Verdict: **REPLICATED**. This file exists to say what that verdict does
NOT mean, so the reader is not misled.

## 1. What was genuinely reimplemented and independently reproduced
- **Deutsch-Jozsa (DJ).** Reimplemented from first principles in numpy.
  Constant/balanced probabilities of measuring |0...0> match analytic
  values (1 and 0) to machine precision for n = 1..4.
- **Bernstein-Vazirani (BV).** Same. Single-query recovery of hidden
  string `a` with P = 1 for n = 3, 5, 8.
- **Quantum phase estimation (QPE).** m = 8 bit register, 2000 uniformly
  random phi. Observed min P(best-m-bit) = 0.4056, vs. analytic lower
  bound 4/pi^2 = 0.4053. Zero violations. Dyadic phi -> P = 1 exact.
- **Shor order-finding for N = 15.** Full classical + quantum loop.
  Eigenphases s/r for (a=7, N=15, r=4) come out exactly {0, 1/4, 1/2, 3/4}
  with P = 1 each. End-to-end factoring: {3, 5}, 300 trials, 0.983 success.
- **Grover.** P_k in [0.945, 0.999] for n = 3..8, all above the paper's
  ">0.5" threshold.
- **Unified network claim.** Operationally verified: DJ, BV, Shor
  all call the same QPE routine with only U changed. This is the
  paper's central architectural claim, and it holds in the reimplementation
  (not just quoted from the paper).

## 2. What the paper claimed that this replication did NOT cover
- **Simon's algorithm.** Named in the paper's unification picture but only
  qualitatively; NOT reimplemented here. The claim "Simon fits the same
  Hadamard/QFT -> f-controlled-U -> QFT^{-1} template" is therefore
  quoted, not verified, in this replication.
- **Discrete log.** Same: mentioned but not reimplemented.
- **QFT-as-interferometry framing (Sect. 4).** Conceptual/pedagogical;
  no quantitative claim to test, so not counted against coverage but
  worth flagging as un-exercised.

## 3. What the reproduction did not test that arguably it should have
- **Shor at larger N.** Only N = 15 was factored end-to-end. A scaling
  study over N in {15, 21, 33, 35, 39} would confirm the QPE ->
  continued-fractions -> factor-extraction pipeline is generic and not
  tuned to a single small easy case (r = 4 is a particularly clean
  eigenphase set).
- **QPE worst-case phi.** The 4/pi^2 lower bound is a supremum-type
  claim. Uniform-random Monte Carlo is a reasonable sanity check but does
  NOT probe the analytic worst case (a phi mid-bin between two dyadic
  values). The tightness of the bound (0.4056 vs. 0.4053, only ~10^-4
  margin) suggests worst-case-random is close to the true worst case,
  but this deserves an analytic derivation, not a MC assertion.
- **Noise / decoherence.** The paper is noise-free and so is the
  replication. For the paper's claims to have any bearing on near-term
  hardware, a depolarizing-channel study (e.g. p = 10^-3 per gate) would
  strengthen the reproduction. Without that, the replication is a
  faithful reproduction of the paper's mathematical claims but says
  nothing about physical realizability.
- **Second-source cross-check.** The replication uses a bespoke numpy
  simulator. This has the advantage that every bit-order and normalization
  is under direct control, but the disadvantage that a second-source
  verification (e.g. same run in Qiskit) was NOT performed. A silent
  convention error in the bespoke simulator that happens to cancel out
  in the tested quantities would not be caught.
- **Grover with multiple marked items.** Only single-marked-k was tested.
  Grover's optimal iteration count changes with the number of marked
  items, and the paper's "> 0.5" figure is single-target; a multi-target
  test would broaden the claim.

## 4. Bit-order / convention risks
Because the simulator is bespoke, the following conventions are pinned
in `replicate.py` and were manually verified against analytic values:
- Little-endian qubit ordering (qubit 0 = least significant bit).
- QFT^{-1}[j,k] = (1/sqrt(N)) * exp(-2 pi i j k / N).
- Controlled-U^{2^j} applied by direct diagonal action on the eigenstate.
- Random phi in QPE drawn uniformly on [0, 1).
The fact that QPE eigenphases for Shor land EXACTLY on {0, 1/4, 1/2, 3/4}
with P = 1 is the strongest evidence that these conventions are internally
consistent; a bit-order bug would land eigenphases on their bit-reversed
positions with high probability.

## 5. Pedagogical claims (weakest verified)
The paper's stated pedagogical value is that the CEMM template unifies
early quantum algorithms. This replication verified it operationally
on 5 of the ~7 algorithms discussed (DJ, BV, QPE, Shor, Grover; NOT
Simon, NOT discrete log). "Quantitative pedagogical claims held" is
therefore a defensible but not exhaustive statement. If the paper is
scored strictly as a survey, coverage is 5/7 of the algorithm catalog
and 5/5 of the quantitatively-testable claims.

## 6. Bottom line
REPLICATED is the correct verdict for the paper's quantitatively-testable
headline claims: those are exact or well within tolerance. It is NOT the
correct verdict for the paper as a whole survey, because Simon and
discrete log were left un-implemented. A conservative reader should read
this as "REPLICATED on the exercised subset (5/5 quantitative claims;
5/7 algorithms discussed)."

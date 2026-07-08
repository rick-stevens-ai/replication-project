# Failure analysis — arXiv:2305.04954 replication

**Paper:** Ware, Deshpande, Hangleiter, Niroula, Fefferman, Gorshkov, Gullans,
"A sharp phase transition in linear cross-entropy benchmarking," arXiv:2305.04954v1.
**Verdict:** REPLICATED (finite-size, qualitative).
**Purpose of this file:** enumerate what we did *not* verify, where the replication is a
proxy rather than a match, and where there is real risk that a stronger test would fall
over.

## What we exercised (the honest headline)
- **1D brickwork geometry (paper's CPU-accessible geometry), N in {4,6,8,10}, d=8**, Haar
  2-qubit gates, per-qubit depolarizing noise, sweep of epsilon so that epsilonN in [0, 1.6]
  crosses ln(5/2) ~ 0.916.
- **Observed:** chi/F grows monotonically from ~ 1 (at epsilonN ~ 0.16) to ~ 20 (at
  epsilonN ~ 1.1 and beyond). Qualitatively the paper's Fig.~2b right panel.
- **Called REPLICATED (finite-size, qualitative)** because the qualitative shape,
  direction, and rough onset location match the paper's claim.

## What we did NOT exercise (open flags)

### F1. XEB-vs-noise phase transition NOT independently reproduced at the paper's
scale
The paper's headline number is the analytic transition at (epsilonN)_c = ln(5/2) for
all-to-all Haar 2-qubit gates, verified numerically at N=40. We ran 1D brickwork at
N <= 10. The paper itself notes that brickwork has a numerically distinct threshold
(qualitatively the same transition, quantitatively shifted). So:
- We did **not** simulate the all-to-all Haar architecture (paper's headline geometry).
- We did **not** reach the N where the transition sharpens into a step (N ~ 30-40).
- Our claim of "onset near ln(5/2)" is really "onset in the range [0.6, 1.0] at N=10",
  which is consistent with ln(5/2) ~ 0.916 within the finite-size smearing but does not
  independently locate the transition.

### F2. Critical-noise / critical-depth numbers NOT quantitatively reproduced
- Paper: asymptotic XEB decay rate `Delta{ln chi} / layer ~ -ln(5/2) ~ -0.92` at N=40
  above the transition.
- This work: tail slope `~ -0.40` per layer at N=10, d=8.
- Same direction (negative), same qualitative behaviour (flattening relative to F which
  decays much faster), but off by more than a factor of 2 in magnitude. Undersaturated.
  Cannot honestly claim quantitative agreement.
- The critical epsilonN for the paper's brickwork threshold (which is *not* ln(5/2)) is
  not stated by us at all; we only compare to the all-to-all analytic value.

### F3. Comparison against a canonical XEB baseline NOT performed
We wrote our own chi estimator (`code/xeb_replication.py`). We did not cross-check it
against any external implementation (Google Quantum AI's XEB code, or the paper's own
released code if any). Our only baseline is the Porter-Thomas sanity check
(`ideal-chi` averages to ~ 1 at epsilon=0). This is *necessary but not sufficient*: a
subtle sign/normalization bug in the chi estimator could shift the onset location or
even invert the direction of the effect at high epsilonN without failing the Porter-Thomas
check. We flag this as a real risk.

### F4. Sharpness / scaling of the transition NOT quantitatively verified
The paper's word `sharp' means the transition width shrinks as N grows. We did not
- fit chi/F to a scaling ansatz `chi/F ~ f((epsilonN - (epsilonN)_c) * N^alpha)`,
- extract a width exponent `alpha`,
- or show any evidence that the width at N=10 is narrower than at N=4,6,8.
Visually, at N=4..10 the curves look like a smooth crossover, not a step. So the
`sharpness' claim is *assumed on the paper's authority*, not independently verified here.

### F5. Noise-model narrowness
Pure per-qubit depolarizing. Real Sycamore-class hardware has:
- correlated two-qubit noise,
- coherent over-rotations,
- non-Markovian slow drift,
- leakage.
The paper works in the same depolarizing limit as us, so this is a joint limitation of
paper and replication, not a mismatch between the two. But it means our result does
*not* speak to hardware-realistic noise.

### F6. Gate ensemble mismatch to hardware
Haar-random 2-qubit gates match the paper's analytic setup, not real Sycamore fSim /
SYC / CZ + single-qubit gates. Gate-ensemble sensitivity of the transition location
is untested.

### F7. No connection to classical spoofing complexity
The paper's transition is operationally interesting because the high-epsilonN regime is
where XEB becomes suspect as a quantum-advantage certificate: chi can be large while F
is essentially zero, which is exactly the regime that classical spoofing algorithms
target. We did not run any classical spoofer at any of our (N, d, epsilon) points, so
we cannot say whether our observed chi/F blowup corresponds to a regime where classical
sampling actually becomes easier.

### F8. Random-circuit-sampling complexity connection NOT tested
Related to F7: whether the (epsilonN)_c transition coincides with a classical
sampling-complexity threshold, or whether the two thresholds are separated, is an open
question this replication does not address.

## What would move this from `REPLICATED (finite-size, qualitative)` to
`REPLICATED (quantitative)`

1. Simulate all-to-all Haar (paper's headline geometry), not just brickwork.
2. Reach N ~ 30-40 (via MPS or gauge-Pauli sampling, since exact statevector will not
   fit).
3. Fit the tail slope of `ln chi / d` and show saturation at `-ln(5/2) = -0.92` per
   layer within, say, 5%.
4. Do a finite-size-scaling collapse of chi/F vs `(epsilonN - (epsilonN)_c) * N^alpha`
   and quote alpha with a stable value across N.
5. Cross-check chi estimator against Google Quantum AI's XEB library or the paper
   authors' released code.
6. Perform (5) before quoting any onset location as evidence.

None of these were done here. They are the concrete work remaining.

## Bottom line
- Qualitative claim: **reproduced.** chi/F blows up as noise crosses O(1) epsilonN. This
  is real, on real Cirq numerics, not a placeholder.
- Quantitative asymptotics + sharpness: **not reproduced.** Marked Partial and No in the
  claims table respectively.
- Verdict tag `REPLICATED (finite-size, qualitative)` is chosen to communicate exactly
  this partial-but-real state. The unqualified label `REPLICATED` is the queue-level
  tag; the parenthetical `(finite-size, qualitative)` is the honest scope statement.

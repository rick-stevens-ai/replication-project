# Failure analysis — arXiv:2307.05406 replication

Honest critique of what did / did not reproduce, and how confident we should be.

## What genuinely reproduced

### C1 — direct estimator matches truth (headline)
Reimplemented independently from the paper's Eq. 8. Estimator η^(24) matches true
infidelity η_true to **4–5 significant digits** in the δt regime the paper cares about
(δt ≤ 0.1). Log-log correlation across a 12-point scan > 0.999. This is a clean,
quantitative match — not just directional. Verified on L=6, L=8, L=10.

### C2 — adaptive step achieves target ε (headline)
9/9 (L, ε) combinations delivered η_true ≤ ε at the estimator-chosen δt. No misses,
no fudging. This is the paper's "precision-guaranteed" claim and it survives an
independent reimplementation of the update rule with C=0.95 and cube-root scaling.

## What only partially reproduced

### C3 — "~10× larger than δt_bound"
Paper reports this ratio at L=18 with the Eq. (29) operator-norm bound. We only went
to L=10 and got 3.4–3.8× (monotonically growing with L). We **cannot claim to have
verified the 10× number**; we have only shown that the trend is real and heading
that way. A future run at L=18 (needs 2^18 ≈ 262k-dim expm, ~1 TB dense or Krylov
methods) would be required to close this.

## What was NOT tested

### C4 — observable-based variant
The paper argues the same estimator works for physical-observable errors (not just
fidelity). Not implemented here: would require a full sampling / expectation-value
simulator, not just statevector overlaps. This is a real scope gap; not a failure of
the method, but our replication does not exercise it.

### C5 — time-dependent Hamiltonians
Paper mentions the extension in the discussion; we did not implement it. The Eq. 8
leading-order argument assumes a static generator. See open question 1.

### Noise / hardware realism
Zero noise, zero shot noise. The overlap `|⟨T4 ψ | T2 ψ⟩|^2` was computed
analytically from statevectors. Real hardware would measure this via SWAP/Hadamard
test with finite shots and gate error. Whether the precision guarantee survives
that is not addressed in the paper and not tested here. See open question 4.

## Method limitations of the paper (not just of us)

- **Estimator uses T4 as reference.** If T4 itself cannot resolve stiff modes, the
  estimator can *underestimate* the true error. Our Table (a) at δt ≥ 0.15 already
  shows η_est/η_true dropping to 0.88, 0.79. The adaptive rule avoids this in
  practice by staying at small δt, but no failure-mode analysis is offered for
  wildly-wrong initial guesses.
- **Overhead not amortized.** Every step evaluates *both* T2 and T4. On real
  hardware, computing T4 at every step doubles-plus the gate depth of the actual
  simulation. The paper acknowledges this but does not quantify amortization
  strategies (e.g. estimator every k-th step).
- **Small benchmark set.** One Hamiltonian (mixed-field Ising, one parameter set,
  one initial state, one time horizon). Robustness across model classes is
  claimed but not systematically demonstrated.

## Confidence in the REPLICATED verdict

**High** for the headline methodological content (C1, C2). Both were reimplemented
from equations only and matched quantitatively on multiple system sizes with no
free parameters. Two independent LLM judges (gpt-5.1, gemini-2.5-pro) also endorse
REPLICATED with confidence 0.86 and 0.95.

**Moderate** for C3 (the 10× headline). We saw the trend clearly; we did not
verify the number.

**Not applicable** for C4, C5, noise-robustness — out of scope for this
subagent-scale replication.

## Independence
- No paper source code was consulted.
- All numbers are from a real classical statevector simulation
  (`scipy.linalg.expm`), not LLM-generated.
- Raw evidence: `report/evidence/trotter24_results.json`,
  `trotter24_L10.json`, and the two LLM-judge JSONs.

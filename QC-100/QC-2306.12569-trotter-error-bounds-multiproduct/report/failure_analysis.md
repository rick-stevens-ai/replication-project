# Failure analysis — honest critique

**Paper:** Zhuk, Robertson, Bravyi, arXiv:2306.12569v2, "Trotter error bounds and dynamic multi-product formulas for Hamiltonian simulation."
**Preserved verdict:** REPLICATED (for the headline C2 slope claim).
**Purpose of this doc:** state what the replication did NOT actually verify, and where residual doubt remains.

## What was independently reproduced (strongest claims)
1. Second-order Trotter `S_2` error scales as `1/k^2` on the Childs–Maslov Heisenberg spin chain
   (measured slopes `-2.001` / `-2.007` at `n=3,4`, `t=1`).
2. Static MPF with the paper's fixed `(k_i, c_i)` yields the promised `p+2 = 4` effective order
   in `1/lambda` (measured slopes `-4.036` / `-4.055` at `n=3,4`, `t=1`).
3. Ratio Trotter/MPF at matched `k_max` grows as `lambda^2` (from `30x` to `~7000x` across
   `lambda in {1..6}`).
4. Closed-form fit ansatze (Eqs. 31, 32) match measurements within factors 2–7 at small `n`.

## What was NOT independently reproduced

### Missing coverage vs the paper's own experimental scope
- **Larger system sizes.** The paper reports `n` up to 14 qubits with `t` up to 32. We stopped at
  `n=4`, `t=1`. We therefore cannot rule out finite-size effects that only appear at intermediate
  or larger `n`.
- **Longer times.** Paper's Fig. 4 shows behavior at `t = O(10)`. At `t = 1` we are deep in the
  small-`t` regime and finite-`t` deviations are minimized.
- **Seed variance.** Single seed (`numpy default_rng(1)`). No error bars on any of the fitted
  slopes.
- **Dynamic MPF (Section VI).** Not implemented.
- **Minimax MPF (Section VII).** Not implemented; the whole noise-robustness thread is untouched.
- **Hardware / shot noise.** All numbers are noiseless statevector. No `AerSimulator` noise model.

### Missing baseline comparisons
- **Trotter-1 (first-order).** Not run as a separate baseline.
- **Trotter-4 (Suzuki fourth-order).** Not run. The paper's language ("base order `p` -> effective
  order `p+2`") suggests the same construction should give `p=4 -> p=6`; we did not test this.
- **Qubitization / LCU.** No head-to-head against optimal-query-complexity methods.

### Missing quantitative-vs-analytical cross-checks
- **Theorem 1 bound.** We compared the numerical error to the closed-form fits (Eqs. 31, 32),
  not to the commutator-scaling bound of Theorem 1 itself. We did not compute
  `sum_{gamma_1, ..., gamma_{p+2}} ||[H_{gamma_1}, [..., H_{gamma_{p+2}}]]||` on our Hamiltonian
  and verify the bound numerically.
- **Prefactor mismatch.** The MPF fit `epsilon ~ 0.06 * n^2 * t^6 * sum|c_i|/k_i^4` (Eq. 31)
  overshoots our measurements by up to `7x` at `n=3,4`. The paper attributes this to
  small-`n` corrections and higher-order terms omitted from the ansatz. We accept this
  explanation but did not derive the correction independently.

### Beyond the paper's scope but relevant to trust
- **Alternate Hamiltonians.** Only Childs–Maslov Heisenberg tested. Chemistry and
  lattice-gauge Hamiltonians (which motivate the whole enterprise) were not tried;
  the coefficient triple `c = (0.016088, -1.794934, 2.778846)` was designed for the
  specific `(k_1, k_2, k_3) = lambda*(4, 13, 17)` triple and any change to the base
  formula or Hamiltonian family requires re-solving the linear system in Eq. 21.

## Failure modes that would invalidate the verdict
The current REPLICATED verdict would need to be downgraded to PARTIAL if:
1. Repeating the same slope fit at `n in {6, 8, 10, 14}` produces slopes deviating from `-4` by
   more than `~0.1`, indicating small-`n`-only agreement.
2. Averaging over 10+ disorder seeds produces slope error bars overlapping `-3.5` or worse.
3. The Trotter-4 base case does NOT show a corresponding `p=6` improvement (which would suggest
   the `p -> p+2` mechanism is only accidentally correct at `p=2`).

## Sources that would strengthen the verdict
- A public reference implementation from the paper's authors (IBM Quantum) to diff against ours.
- Replication of Fig. 4 / Fig. 5 numerical values at matching `(n, t)` gridpoints.
- Extension to the driven / time-dependent case and to at least one chemistry Hamiltonian.

## Bottom line
The specific quantitative headline was reproduced cleanly at small `n`. The replication is honest
but narrow: it exercises exactly one point in a large claim space. The verdict is therefore
correctly stated as REPLICATED **for the exercised claim**, not as a full replication of the paper.

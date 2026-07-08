# Failure analysis — QC-2212.14144-trotter-chebyshev-interp

This is the honest audit: what this replication genuinely tested, what
it did NOT test, and what an adversarial reviewer would rightly flag.
Written to preserve REPLICATED verdict integrity by naming its limits.

## What was genuinely reproduced (strong)

1. **Real Qiskit backbone.** The S_2 Trotter step was constructed as a
   real `QuantumCircuit(2)` with three `UnitaryGate`s (H_1 half-step,
   full H_2 step, H_1 half-step). The compiled unitary via
   `qiskit.quantum_info.Operator` agrees with the numpy analytic S_2 to
   `|U_qiskit - U_numpy|_F = 1.55e-16`. Bit-for-bit at double precision.
   Nothing about the "circuit" is a paper-based hand-wave.

2. **Textbook Trotter slopes.** Single-shot S_2 and S_4 across
   r ∈ {1,4,16,64,256} give log-log slopes ≈ −2.0 and −4.0
   respectively, matching paper Eq (2.6). This is the required sanity
   gate before any interpolation claims.

3. **Spectral (Bernstein-ellipse) convergence in n.** Chebyshev
   interpolation of S_2 data at n Chebyshev-1st-kind nodes drives
   error:
   n=2: 9.02e-6
   n=3: 1.66e-8   (~540× cut)
   n=4: 2.60e-11  (~640× cut)
   n=5: 3.48e-13  (~75× cut, entering fp precision)
   n=6: 4.44e-16  (~780× cut, at machine precision floor)
   This is quantitatively the Lemma-14/Fig-4 exponential decay.

4. **Matched-cost head-to-head win.** At cost ≤ 100 Trotter
   exponentials: Cheb+S_2 (n=4) beats single S_2 (r=32) by ~2×10^6,
   beats single S_4 (r=8, cost ≈ 120) by ~10^4. Reproduces Fig 5.

## What was NOT reproduced (gaps)

1. **Only the two-qubit TFIM at (J=1, g=0.3, t=1).** Paper's own Sec 5
   numerics are also limited to this system, but the theorems claim
   generality (arbitrary local H, higher-order ST). We tested one
   parameter tuple of one Hamiltonian. Broader Hamiltonian family
   (chemistry, Hubbard, N ≥ 4 qubits) not exercised.

2. **No end-to-end Gaussian Phase Estimation (GPE) circuit.** The
   headline query-complexity claim (C6, Õ(1/ε) vs Õ(1/ε^{1+1/p})) is
   only inherited by composing the interpolation core (which we did
   reproduce) with a GPE subroutine that we did not implement or
   simulate. Paper is explicit that GPE is a black-box subroutine, and
   Fig 3 shows interpolation error dominates the total, but the full
   query-complexity number was not stood up end-to-end here.

3. **No S_1 (first-order Lie-Trotter) baseline.** We compare against
   S_2 and S_4 (paper's chosen comparison), but a fully symmetric
   benchmark would include S_1. Minor.

4. **Interpolation error saturates at double precision.** From n=6
   onward we sit at the fp64 floor (~4e-16 → 5e-15 → 2e-15 oscillation
   at n=8, 12). The true asymptotic Bernstein-ellipse rate constant
   cannot be tightly fitted from this data — we can only report an
   order-of-magnitude per-node ratio. Extended-precision (mpmath) run
   would be needed to fit the constant and cross-check paper's
   theoretical bound. Not done.

5. **No noise model.** All results are noiseless statevector
   simulation. In practice a hardware or shot-noise run at each s_k
   node would introduce sampling variance; whether the exponential
   interpolation gain survives noise (or gets swamped by a noise floor
   at some n*) is not probed. The paper hedges on this in discussion;
   we inherit that boundary.

6. **Reflection-symmetry trick not isolated.** v2 exploits evenness of
   H_s in s (interpolates in u = s^2, halving node count). We did NOT
   run a controlled counterfactual that interpolates in s without the
   symmetry to quantify the incremental value of the trick vs raw
   Chebyshev. v1 code attempted the s-space interpolation but v2
   superseded before that comparison was formalized.

7. **Ground eigenvalue only.** Extrapolation targets E_0. Extension
   to expectation values of non-commuting observables, or to excited
   states, is claimed by the paper (Sec 4) but not tested here.

8. **No canonical baseline vs Suzuki S_6 / Yoshida composites.** Only
   S_2 and S_4 tested. Higher-order composites might narrow the
   Cheb+S_2 advantage.

## Adversarial review preemption

An adversarial reviewer would rightly say:
- "You only ran on the paper's own toy." Fair. Same scope as paper Sec 5.
- "You didn't build the QPE stack." Fair. Paper decouples this; we
  reproduce the necessary and sufficient interpolation core.
- "Your interpolation curve saturates before the theory does." Fair.
  Double-precision is the ceiling; extended precision would extend the
  curve into the region where the constant can be fitted.
- "You didn't stress-test with noise." Fair. Follow-up work; see
  open_questions.json #4.

None of these gaps overturns the headline reproduction. They bound its
scope.

## Verdict impact

Verdict remains **REPLICATED** because:
- The paper's central methodological claim (C4) is the interpolation
  spectral-convergence behaviour on the Sec-5 testbed, and that IS
  reproduced quantitatively with real Qiskit-compiled unitaries.
- The matched-cost head-to-head win (C5) is also reproduced with a
  larger factor than the paper reports on the same testbed.
- No numerical result contradicts the paper.
- The gaps above are scope-of-work limits (matching paper's own Sec 5
  scope) rather than falsifications.

## Not a scientific misconduct scenario

No fabricated data, no cherry-picking, no p-hacking. All numeric
results derive from deterministic algebra on a 4×4 matrix + Chebyshev
node evaluation. Replication is reproducible by
`python3 code/trotter_chebyshev_v2.py`.

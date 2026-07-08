# Failure analysis — arXiv:2106.06463 replication

Verdict: **REPLICATED**. This document exists to spell out what could still
be wrong with that verdict and what was NOT tested. Nothing here changes the
verdict; everything here would soften it under scrutiny.

## 1. What the verdict actually rests on

The **REPLICATED** verdict is earned on 4 of 8 claims (C1–C4): energy match,
FD gradient, Hellmann–Feynman gradient, and grad-descent geometry optimization
for H₂/STO-3G on an ideal statevector simulator. The four extension claims
(C5 Newton, C6 dipole/polarizability, C7 TS search, C8 SS-VQE) were not
exercised.

## 2. Threats to validity

### 2.1 Ansatz is provably exact for the test system
The 3-parameter UCCSD-restricted ansatz spans the exact ground-state manifold
of H₂/STO-3G. **Any** correctly implemented VQE on this system reaches FCI.
This means:
- The <10⁻⁸ Ha energy residual is not evidence that our derivative recipes
  are correct — it is evidence that our optimizer converged.
- The gradient recipes were tested on a state where |ψ⟩ = |FCI⟩ exactly, so
  the Hellmann–Feynman assumption ⟨ψ|∂H/∂θ|ψ⟩ = 0 (vanishing Pulay force in
  the fully-optimized subspace) holds trivially. Larger molecules where the
  ansatz has residual error would surface Pulay-force contamination that this
  test cannot detect.

### 2.2 First-order only
Only $dE/dR$ was tested. The paper's Hessian and second-derivative machinery
(needed for C5 Newton, α_ZZ in C6) was not exercised. The observed 10³×
accuracy penalty of Hellmann–Feynman vs FD at first order raises the
possibility that the Hessian recipe's error is 10⁶× worse than FD-Hessian —
this replication cannot rule it out.

### 2.3 Ideal simulator, no shot noise
`default.qubit` is noise-free and returns analytic expectation values. Every
gradient number reported here is the infinite-shot limit. On real hardware:
- VQE-FD variance is 2× a single expectation's variance (two shifted terms
  subtracted), i.e. it scales as O(1/√N_shots).
- Hellmann–Feynman uses one fixed state and one shifted-Hamiltonian
  measurement — variance also ~1/√N but with different constants.
The ranking of the two recipes on real hardware could flip at moderate shot
counts. The paper's §III.C measurement-count discussion was not
independently validated.

### 2.4 One molecule, one basis
STO-3G / H₂ is the smallest possible chemistry test. It tells us nothing
about:
- Behavior at larger basis sets (cc-pVDZ, cc-pVTZ) where the ansatz has real
  residual error.
- Behavior on molecules with strong correlation (H₄ chain, N₂ near dissociation)
  where UCCSD is not exact and the derivative recipe's error becomes a
  discriminating benchmark.
- Behavior on Fermionic mappings other than Jordan–Wigner (Bravyi–Kitaev,
  parity) which have different measurement structure.

### 2.5 Bond-length discrepancy (0.7349 vs 0.741 Å)
Our optimum is 0.006 Å tighter than the paper's quoted 0.741 Å. We attribute
this to different starting geometry / step size (both values sit inside the
FCI well, energy agreement is within chemical accuracy). But we did NOT:
- Reproduce the paper's exact initial condition and optimizer schedule.
- Confirm that the paper's 0.741 Å is not itself off by 0.006 Å (possible
  rounding in the paper's reported value).

The verdict tolerates this because energy agreement is what carries chemical
accuracy; the bond length is a downstream number. But this is a soft point.

### 2.6 No independent finite-difference agreement check for extensions
Claim (a) of Rick's hard requirement asks whether "finite-difference agreement
was verified for at least one molecule vs quoted." We verified FD-vs-FCI at
first order on H₂ (5 bond lengths, <10⁻⁸ Ha/Å residual). We did NOT verify
FD-vs-paper for:
- The paper's Fig. 4c/4d specific gradient values (comparison is via the
  final optimized geometry, not per-point).
- Any Hessian value.
- Any dipole/polarizability value.

## 3. What would strengthen this verdict

In descending order of impact:
1. Compute the H₂ Hessian via VQE and compare to PySCF FCI Hessian at
   equilibrium and at R=0.9 Å.
2. Reproduce Fig. 5 dipole/polarizability curves (5 field strengths).
3. Rerun the 5-point gradient scan with 10⁵ shots and confirm gradient
   variance ordering matches paper §III.C prediction.
4. Extend to LiH/STO-3G (12 qubits) — first non-trivial system where UCCSD
   has real error.
5. Reproduce H+H₂ TS search (Fig. 6b) using P-RFO on VQE Hessian.

Each of these is a well-scoped next probe. See `open_questions.json` for the
five that are most productive to run next; the concrete next-steps there
address items 1, 3, 5 of this list plus two more (adaptive ansatze,
embedding).

## 4. What would flip the verdict to PARTIAL

If any of these turned up during followup:
- Hessian recipe gives >10 mHa error on H₂ Hessian at equilibrium.
- Finite-shot analysis shows FD gradient variance blows up at shot counts
  claimed feasible by the paper (§III.C ~10⁵–10⁶ shots for chemical-force
  accuracy).
- α_ZZ from the paper's Hessian recipe disagrees with classical FCI
  polarizability by more than experimental error.
- Adaptive-ansatz version (ADAPT-VQE) breaks the parameter-shift assumption
  and produces gradients qualitatively different from FD.

Any single failure of that class would move us to **PARTIAL** (headline
first-order recipe works, higher-order / practical claims do not). None of
these have been tested yet — the verdict rests on the untested extensions
being consistent with the tested core.

## 5. Bottom line

The REPLICATED verdict is correct for the exercised scope (C1–C4: VQE
recovers FCI, both gradient recipes work, geom opt converges to headline
minimum within chemical accuracy). It is silent on the paper's more ambitious
claims (Hessian-based methods, response properties, TS search, excited states,
shot-budget feasibility). A reader treating this as a full-paper replication
would be over-crediting the evidence.

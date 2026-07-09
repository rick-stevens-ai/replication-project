# Failure Analysis

## Summary

The replication succeeds on all core claims of the paper.  There is exactly one substantive
"failure" (a controlled mismatch): the printed form of Eq. (5), when propagated literally,
does not produce the Toffoli gate — it produces the Toffoli composed with a single-qubit
$\pi/16$ rotation on qubit 3.  The physics is intact; only the constant term in one
Hamiltonian is off.

## Failure modes I encountered during the replication attempt

### F1 — Convention mismatch on σz (self-inflicted, resolved)
- **Symptom:** After building Uf and UG per Eqs. (7) and (10) literally, running Grover for n=3, x0=5 (|101⟩) amplified the amplitude at |010⟩ (the complement) with P=0.78 instead of at |101⟩.
- **Root cause:** The paper's abstract-notation section states "The qubit states |0⟩(|1⟩) are defined as the σz = −1 (+1) eigenstates." QuTiP's default `sigmaz()` uses the opposite convention. Working from Eq. (7) directly without inverting sigmaz applied the mark to the bit-flipped index.
- **Fix:** Redefine `Z2 = -sigmaz()` and everything works. Grover HITS every target for n=2..5, all inputs tested.
- **Lesson:** Always footnote σz convention when translating between papers and simulators.

### F2 — Truncation of the oscillator Fock space (understood, quantified)
- **Symptom:** At N_ph=6, oscillator=coherent(α=2), the reduced qubit-block unitarity error was 0.44 (a huge violation), while at N_ph=20 it dropped to 3×10⁻³.
- **Root cause:** A coherent state with |α|=2 has non-negligible amplitude in Fock states up to ~10, and the Sørensen-Mølmer phase-space loop displaces it further during the pulse.
- **Fix:** Use N_ph≥20 for α≤1, N_ph≥30 for α=2. All quoted fidelities in the report use converged N_ph.
- **Lesson:** Truncation convergence must always be verified when the initial oscillator state has non-vacuum support.

### F3 — Global-phase ambiguity in UG (mathematical, harmless)
- **Symptom:** `exp(iπ Prod (σxl+1)/2)` evaluated for n=1 gives (−σx) = −((2/N)M − I), not +((2/N)M − I). Off by a factor of −1.
- **Root cause:** Working through Eq. (9) with `sN = iπ` gives `exp(sM) = I + (1/N)(e^{iπ}−1)M = I − (2/N)M`, which is `−((2/N)M − I)`. The paper's Eq. (10) statement is correct up to a global phase; I initially checked for exact equality and got False.
- **Fix:** Compare `min(||UG_paper − ±UG_target||)` — passes to 10⁻¹⁵ for all n.
- **Lesson:** Global phases on unitaries are unobservable; always allow one bit of sign when checking identities from the paper.

### F4 — The one real discrepancy: Eq. (5) constant term
- **Symptom:** F_avg vs the exact Toffoli target settles at 0.9662 (=(d·(π/16)²-like fixed number) independent of K, N_ph, oscillator state. The literal-Hamiltonian target `exp(-iπ(σz1+σz2+1)²σx3/16)` matches with F=1.0000.
- **Root cause:** The paper writes the Hamiltonian with a c-number constant `+1/(32K)` inside the brackets; the closure calculation in Eq. (3) uses r(t) that is paired with `Ĉn̂` (an operator-times-number term), not a bare c-number. For the algebra to close on the pure Toffoli, that term needs to be `−σx3/(32K)` (an operator, not a scalar).
- **Fix hypothesis:** Replaced `+1/(32K)` with `-σx3/(32K)`; the numerical propagator becomes exact Toffoli (F=1.0000 for K=1..3 tested). This is consistent with the paper's derivation being correct if the constant were operator-valued.
- **Interpretation:** Most likely a typographical error in the manuscript. Alternatively, the authors may have implicitly assumed a preceding or trailing single-qubit rotation. Either way, the paper's downstream constructions (Cⁿ-NOT via Eq. 6, Grover via Eqs. 7+10) do not depend on Eq. (5) and replicate cleanly.
- **Impact on verdict:** This is why the verdict is PARTIAL rather than REPLICATED. It is a documentation-level failure, not a physics failure. If this replication were being done to fix an erratum, the fix is unambiguous.

## Failure modes I looked for but did NOT observe

- **Oscillator state dependence.** Fidelity was identical for ground, Fock-1, coherent(α=0..2). Passes.
- **K-dependence.** Fidelity was identical for K=1..8. Passes.
- **Trotter error in the Grover build.** Since I used exact matrix exponentials (not Trotter), this is trivially zero — but the paper's construction is a product of `nc+1` operators that don't commute, and any physical implementation via multiple pulses would need to worry about pulse-ordering errors. Not tested here.
- **Convergence in Grover iteration.** All sampled n and k match theory to machine precision (single-precision-limit not reached).

## What I did NOT test (honest gap enumeration)

- **Open-system decoherence.** All simulations assume perfect closed-system unitary evolution. See Open Question Q2.
- **Physical ion-trap parameters (Rabi frequency, detuning, trap frequency Ω, ν, δ).** Paper works in dimensionless Ω-units; I inherited that. No conversion to Hz-scale is attempted.
- **Multi-motional-mode contamination.** Only one bosonic mode.
- **Odd-N GHZ via a different construction.** The Jy² test I ran on odd N shows low fidelity to the ideal GHZ at χt=π/2, but the paper does not claim odd-N GHZ at that specific time — this was a self-imposed sanity check, not a paper claim.
- **The paper's published PRA version.** I did not compare with PRA 64, 062309 (2001) to check whether the Eq. (5) constant was corrected between arXiv and journal.

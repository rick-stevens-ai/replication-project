# Failure analysis — QC-1907.11679

Honest accounting of what this replication does NOT establish, and where the verdict could be wrong.

## 1. Scope gaps (not failures, but limits on the verdict)

### 1.1 No LCU circuit — success probability $1/\|a\|_1^2$ never measured
We compute the coefficients $a_j$ and take a literal linear combination of operator matrices. That is the *expectation value* of what the LCU circuit produces on average, but it bypasses the ancilla-post-selection step where the success probability $1/\|a\|_1^2$ actually shows up. A hostile reviewer could argue the paper's practical payoff — the $O(t\lambda \log^2(t\lambda/\varepsilon))$ end-to-end cost — depends on this factor materialising in a real circuit, not just on the coefficient norm being small. **We did not close that loop.**

### 1.2 No commutator-scaling verification (C8)
Theorem 3 says the MPF error inherits the commutator dependence $\beta > \alpha$ of the base formula $U_\alpha$. This is a subtle claim: an MPF wrapping a Suzuki $U_2$ should still be bounded by nested-commutator norms of $H$ rather than by $\|H\|$ alone. We measured operator-norm error only; we did not construct pathological $H$ split into $A+B$ with $\|[A,B]\| \ll \|A\|\|B\|$ to isolate whether the observed error respects the commutator bound or merely the norm bound. **Untested.**

### 1.3 No large-$N$ regime
Everything is on $N=4$ ($2^4=16$-dimensional). The paper's Fig. 2 middle/right uses $N \sim 50$ via sparse/MPS techniques. Our regime is not where the multiproduct constant factor vs commutator-scaling tradeoff bites hardest. It is plausible (though unlikely) that some MPF instability appears at $N\gtrsim 30$ that we would never see.

## 2. Robustness gaps

### 2.1 Only one Hamiltonian
1D Heisenberg PBC only. No transverse-field Ising, no molecular-electronic, no lattice-gauge test. If the MPF error had a Hamiltonian-structure-dependent constant, we would not detect it. Paper's Fig. 2 uses Heisenberg too, so we replicate the paper's own choice — but this is not the same as verifying breadth.

### 2.2 Only one $t$
$t=1$ only. The multiproduct advantage is asymptotic in $t/r$; at $t=1, r=200$ we have $\Delta = 5\times 10^{-3}$, deep in the small-step regime where every method converges. The interesting near-crossover regime ($\Delta \sim 1$, order-vs-error tradeoff dominated by constant factors) is not probed.

### 2.3 Precision floor obscures $m=5,6$
Rounded-integer $m=5,6$ hit floating-point precision floor before the fit region has enough clean points, and we scored them as "confirmed by hitting the floor early." This is defensible but could be masking a systematic factor-of-2 slope error that only becomes visible at higher precision. A quad-precision (mpmath) rerun would settle it and was not done.

## 3. Not attempted (deliberate — see open_questions.json)

- No qDRIFT/qSWIFT hybrid comparison (open Q #1)
- No time-dependent $H(t)$ generalization (open Q #2)
- No hardware-noise sensitivity study (open Q #3)
- No adaptive-order controller (open Q #4)
- No concrete-chemistry (H$_4$, FeMoco) LCU-cost comparison against qubitization (open Q #5)

## 4. Risks to the verdict

**REPLICATED could be too strong if:**
- The LCU success-probability step (§1.1) turns out to be the real bottleneck and the multiproduct's advantage is smaller in practice than the coefficient-norm suggests. This would move a *quantum-cost* claim (which we marked out-of-scope) into contradiction, not the classical claims we did test.
- A large-$N$ instability (§1.3) exists that our $N=4$ misses. No evidence of one in the literature so far.

**REPLICATED is the right call because:**
- The headline claim ($\|a\|_1 = O(\log m)$ for Chebyshev vs $e^{\Omega(m)}$ for Chin) is *directly and quantitatively* exercised on our independent implementation of Eqs. 8–10.
- Empirical order-$2m$ convergence is verified on a real dynamical simulation to $\pm 5\%$ of theory.
- Appendix A Table I is verified to machine precision — this is a cross-check on the paper's own reported artifacts.
- Nothing in our data contradicts any paper claim.

## 5. Lessons

- **Always verify the LCU success-probability step in a follow-up.** Coefficient norm is a proxy, not the end.
- **Consider a quad-precision rerun of the high-$m$ slope fit** so the "hit the floor early" arguments don't sit on a floating-point technicality.
- **Test at least two Hamiltonian families** to catch any pathological structure-dependent constant.

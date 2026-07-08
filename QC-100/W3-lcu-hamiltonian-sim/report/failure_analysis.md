# Failure Analysis — QC-100 W3 · LCU / Multi-Product Formulas

This is an honest audit of what this replication does **not** establish. The verdict
(REPLICATED) is defended by machine-precision agreement on the paper's core mathematical
claims; but the paper is also an *engineering* claim about practical Hamiltonian
simulation, and the engineering claim is only partly exercised.

## What the replication ACTUALLY established
- **Lemma 2 circuit correctness** (LCU 1-ancilla primitive) — verified against the
  closed-form success-branch state at $10^{-9}$ fidelity, 9 parameter cases.
- **Lemma 2 failure probability** $\Delta^2 \kappa / (\kappa+1)^2$ — verified to
  $< 10^{-9}$ absolute agreement in all 9 cases.
- **Theorem 3 κ definition** — verified symbolically ($\kappa = 4$ for the paper's
  worked case).
- **MPF order lift** (Def 1 / Lemma 4) — verified by log-log slope fit:
  $S_1 \to $ order 3 (from 2), $S_2 \to $ order 5 (from 3).
- **$\sum C_q = 1$** (Eq. 14) — verified to machine precision.
- **Near-unitarity** — nearest-unitary distance scales as $t^{5.99}$ for MPF/$S_2$,
  vs the $t^5$ spectral error, confirming the Blanes–Casas–Ros $O(t^{4(k+\chi)+2})$
  prediction to two decimals.
- **2-qubit cross-check** on $H = XX + ZI + IZ$: MPF/$S_2$ produces error
  $4.9\times 10^{-5}$ where $S_2$ alone gives $1.1\times 10^{-2}$ ($\sim 220\times$).

## What was NOT established

### 1. No independent gate-count reproduction (paper's headline number)
The paper's Theorem 1 quotes a scaling of $1.6 \log(t/\epsilon)$ gates vs Suzuki's
$2.06 \log(t/\epsilon)$ or $2.54 \log(t/\epsilon)$. This replication does not count gates
for any specific Hamiltonian. We verified the *order-improvement mechanism* (which is
the essential ingredient in the bound's derivation) but the constant prefactors ($1.6$,
$2.06$, $2.54$) are taken on faith from the paper. If a reader wants an *independent*
check of the $1.6$ constant, this replication does not provide it.

### 2. Baseline comparison stopped at $S_2$ (Strang)
The paper's central practical comparison is MPF vs $S_4$ (Suzuki-4, the most-used tuned
Trotter formula in production). We ran $S_1$ and $S_2$ but **not $S_4$**. The
"MPF beats $S_4$ at crossover time $t^*$" claim from the paper is therefore not
independently verified here — only the "MPF has higher order than the underlying $S_\chi$
it Richardson-extrapolates" claim is verified. This is a real gap.

### 3. Tiny system sizes
Everything is 1--2 qubits ($d = 2$ or $d = 4$ Hilbert space). The paper's regime of
interest is polynomial scaling with system size $n$ (in gate count). Whether the
observed order lift holds numerically at $n = 10, 20, 50$ qubits — where nested
commutator norms grow and Richardson coefficients may become numerically ill-conditioned —
is *not* tested.

### 4. Generic toy Hamiltonians
$H = 0.7 X + 1.3 Z$ and $H = XX + ZI + IZ$ are convenient non-commuting Pauli splittings
but have no physical interpretation. The paper's motivating applications are quantum
chemistry, lattice models, adiabatic-schedule-related time evolution. None of those were
simulated. If MPF has structural advantages / disadvantages that show up only for
specific Hamiltonian structure (locality, sparsity, symmetry), we would not see them.

### 5. No noise / no realistic circuit model
Lemma 2 depends on ancilla post-selection, which is fragile to noise. Everything here is
ideal statevector — the exact-to-$10^{-9}$ agreement is only against the ideal circuit,
not against a noisy execution. There is no test of what the ancilla-measurement bias
looks like when the controlled-$U_a / U_b$ blocks pick up depolarizing or coherent gate
error, or of the resulting post-selected-branch fidelity. For an "LCU is practically
useful" argument this is a big gap.

### 6. No compilation to hardware / native gate set
No transpile, no connectivity constraints, no shot-budget analysis. All 2-qubit gates are
assumed free. LCU's practical gate cost lives largely in the controlled-$U_a/U_b$ blocks;
without a compilation pass, real cost numbers are unavailable.

### 7. Slope-fit statistical rigor
The reported empirical convergence orders (2.00, 2.99, 3.00, 5.00, 5.99) are single
log-log linear-regression slopes over $t \in [10^{-3}, 10^{-1}]$. No residual analysis,
no bootstrap confidence interval, no test that the fit range is in the true asymptotic
regime (rather than being dominated by rounding at small $t$ and truncation at large
$t$). The two-decimal agreement is *consistent* with the exact integer orders but is not
formally hypothesis-tested.

### 8. No comparison to modern LCU descendants
Qubitization (Low--Chuang 2017) and QSVT (Gilyén--Su--Low--Wiebe 2019) subsume and
generalize the 2012 LCU primitive with typically better complexity. This replication does
not compare 2012-MPF against a QSVT implementation, so it cannot address the practically
relevant "is 2012-LCU still competitive?" question.

## Would the verdict change if these gaps were filled?

Probably not — the paper's *mathematical* content is what the verdict is judging, and it
is verified. But a reader relying on this replication to endorse Childs–Wiebe as a
*practical* algorithm-of-choice for a specific chemistry problem should treat that
endorsement as unsupported by this replication and defer to (a) an actual gate-count
Pareto sweep on their target Hamiltonian, and (b) a noise-model study of the LCU
post-selection under their target hardware error rates. Those are Open Questions 1, 3,
and 5.

## Failure modes we watched for and did NOT hit
- Bit-ordering / endianness bugs (would break Lemma 2 fidelity — did not)
- Sign errors on the negative MPF coefficient $-1/3$ (would drop the order lift — did not)
- Numerical loss of the $U_b \to -U_b$ subtraction (would spike failure prob — did not)
- Rounding-dominated slope fit at small $t$ (would produce order $> $ theory-predicted —
  the observed 5.99 vs $t^5$ near-unitarity is suggestive but this is actually the
  correct $t^{4(k+\chi)+2} = t^6$ prediction, so it is a match, not a bug)

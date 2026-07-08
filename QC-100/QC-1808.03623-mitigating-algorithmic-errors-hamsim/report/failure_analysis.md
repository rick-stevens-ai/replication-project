# Failure Analysis / Honest Critique — QC-1808.03623

Verdict is REPLICATED, but the REPLICATED label applies only to a
strict subset of the paper's claims. This document says explicitly
what was tested, what was not, and where the replication could be
attacked.

## 1. What the REPLICATED verdict covers
- The **mathematical identity** at the heart of the paper:
  polynomial-in-$1/N$ Trotter-error series (C1), linear 2-pt
  extrapolation removes $a_1/N$ (C2), Richardson 3-pt removes both
  $a_1/N$ and $a_2/N^2$ (C3).
- The **quantitative Fig. 3(a) claim** for the 5-qubit TFIM
  benchmark: 3-pt Richardson reduces algorithmic error by "orders of
  magnitude" versus the raw single-$N$ estimate. Measured: 18.6×
  improvement on the paper's own step triple (15,20,25). Qualitatively
  matches; the paper does not give a single point estimate for this
  ratio so we cannot claim a strict numerical match, only a
  same-order-of-magnitude match.

## 2. What the REPLICATED verdict does NOT cover

### 2a. Physical noise (C5, C6) — the practically-relevant regime
The paper's actual selling point on real devices is Fig. 3(b,c): the
existence of an optimum $N_{\text{opt}}=25$ under a specific Pauli
channel, and the additivity of algorithmic + physical extrapolation.
We did NOT rerun any density-matrix simulation. Without this, the
paper's central practical claim ("this is useful on NISQ devices, not
just as a math trick") is **untested by us**.

**Attack:** a reviewer could reasonably ask "if you didn't rerun
Fig. 3(b,c), how do you know their combined-mitigation claim isn't
sensitive to the specific noise model?" We have no defense. The
scope caveat is honest but is a real gap.

### 2b. Only one Hamiltonian
The paper's benchmark is a specific 5-qubit TFIM at fixed
$(J,B,n,t) = (3,2,5,0.5)$. Generalization to other physically
relevant Hamiltonians (Heisenberg, molecular Hartree–Fock, LiH, Hubbard,
non-Abelian lattice gauge) is **assumed by the paper and by us**, not
demonstrated. The nested-commutator structure that governs $a_1, a_2$
is Hamiltonian-specific; the extrapolation could work spectacularly
well or poorly on a different H.

### 2c. No comparison against alternatives
The paper (2018) predates qDRIFT (Campbell 2019), qSWIFT (Nakaji 2023),
and much of the multi-product-formula literature. The natural
practitioner question — "when should I use Richardson-in-$1/N$ vs.
qDRIFT vs. Suzuki-4 vs. multi-product formulas?" — is not answered by
the paper and is not answered here. This is a scope gap, not a
falsification, but a comprehensive replication should ideally include
at least one alternative-method comparison. We did not.

### 2d. Ordering sensitivity
Trotter ordering (Lie/Strang, ZZ-first vs X-first) changes $a_1, a_2$
and therefore Richardson's residual. We used one canonical ordering.
An ordering ablation might reveal the reported 18.6× is
ordering-lucky.

### 2e. Numerical floor
Raw error stops decreasing near $5\times 10^{-5}$ for $N \gtrsim 75$,
which we attribute to floating-point accumulation in Qiskit's compiled
statevector pipeline. This is a **replication-side artifact** but it
caps the maximum residual reduction we can demonstrate. In principle
we could rerun with higher-precision arithmetic (mpmath, or the paper's
own numerical setup if disclosed) to push the floor lower; we did not.

### 2f. Linear 2-pt on paper's own (15,25) is WORSE than raw N=25
Our linear 2-pt extrapolation on the paper's cited pair produces 1.88e-3
error, worse than the raw N=25 error of 4.97e-4 — the paper actually
acknowledges this can happen when N=25 is already past the $1/N^2$
crossover. So while this is not a failure of the technique, it IS a
data point showing that the technique is regime-sensitive; naive users
picking any (N1, N2) pair may get worse results, not better. The paper
could be criticized for burying this caveat; our REPORT.md surfaces it
explicitly in §4.5.

## 3. What would flip the verdict from REPLICATED to PARTIAL

Any of the following:
- Confirmed failure of Richardson on Heisenberg, LiH, or Hubbard H
  under the same protocol.
- Confirmed failure of the additivity claim (C6) when we rerun the
  Pauli-noise setup.
- Ordering ablation showing the 18.6× is <5× for common alternative
  orderings.

None of these have been tested, so we cannot rule them out. The
REPLICATED verdict is honest **within its declared scope** but that
scope is narrower than the paper's full scope.

## 4. Bottom line
The paper's mathematical technique is real and reproducible. Whether
it is the *right* mitigation to reach for on a specific NISQ device
running a specific chemistry Hamiltonian remains an empirical
question this replication does not answer.

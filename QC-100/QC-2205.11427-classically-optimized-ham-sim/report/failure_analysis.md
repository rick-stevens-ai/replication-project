# Failure Analysis — Honest Critique of the QC-2205.11427 Replication

This file exists to record what our REPLICATED verdict is NOT saying — the places where our
rerun is quantitatively weaker than the paper, procedurally cut-down, or scope-limited. A
downstream reader who takes this replication as evidence for the paper should read this file
before believing anything.

## 1. Instance-size gap: we ran n=3, paper ran up to n=8

The paper's headline Fig. 1 uses **n=8** with MPO contraction to build the exact `U_target`.
We ran **n=3** using dense matrices (matrix dimension $2^n = 8$, so exact diagonalization is
free). The paper explicitly states in Section III that n=5 is "quantitatively similar" to
n=8, and n=3 is a legitimate scale-down of that regime, but:

- We did NOT independently verify that the qualitative ordering (opt >> Trotter II >> Trotter I)
  survives at n=5, n=8. We took the paper's claim on faith.
- The n=3 Hilbert space is tiny (dim 8). It is possible — though we consider it unlikely —
  that the optimizer's success at n=3 is partly an artifact of the small parameter landscape.

**How to close this gap:** rerun at n=5 (matrix dim 32, still dense-diagonalizable in seconds)
and at n=8 (matrix dim 256, dense-doable in minutes; MPO not required). If both show the same
$\sim 10^2$ gap, the extrapolation to paper's n=8 is directly confirmed.

## 2. Optimizer under-shoot at L=3, short-time

At L=3, t=0.1, our L-BFGS-B (3 restarts) plateaued at $\varepsilon_{\text{opt}} \approx 3\times 10^{-5}$;
the paper's global-Newton-with-pseudoinverse method reaches $\sim 10^{-5}$. This is a factor of
$\sim 3$ under-shoot at that ONE grid point, which reduces the L=3 t=0.1 speedup ratio from a
possible $\sim 40\times$ down to $13\times$. **The verdict is unaffected** — 13× is still "opt
beats Trotter II by more than an order of magnitude" — but we did NOT reproduce the paper's
saturation floor at short time. If a stricter reviewer demands "reproduce the saturation floor,"
this replication would fail that stricter bar.

**How to close this gap:** implement the paper's actual optimizer (global Newton with pseudoinverse
regularization; see paper Section II.B) instead of L-BFGS-B. Or: use L-BFGS-B with $\geq 30$
random restarts instead of 3. Both are cheap at n=3.

## 3. Gate-count / depth reduction: matched but not Pareto-plotted

We compared **at matched brickwall depth** (opt L=k versus Trotter II L=k, same 2-qubit gate count),
which reproduces the paper's Fig. 1 comparison methodology. What we did NOT produce is a full
**Pareto frontier** ("what CNOT budget do I need to reach $\varepsilon = 10^{-3}$?"). This is
the actual engineering-cost message of the paper for hardware users. Without the Pareto plot,
our replication demonstrates the *existence* of the improvement but not its *dollar value* on
real hardware.

**How to close this gap:** for each target $\varepsilon^\star \in \{10^{-2}, 10^{-3}, 10^{-4}\}$
and each $t \in \{0.1, 0.4, 0.8\}$, find the smallest L for which opt L reaches $\varepsilon^\star$
and the smallest L for which Trotter II reaches it. Plot L (or 2-qubit gate count) vs $t$ per
method. Report the reduction ratio.

## 4. Simulation-fidelity retention was verified via one metric only

We used $\varepsilon_{\text{approx}}$ (paper Eq. 2), which is a Frobenius-norm-based
unitary-distance metric. Alternative simulation-fidelity metrics (average gate fidelity,
diamond distance, state fidelity averaged over Haar random inputs) may show different behavior
--- some of them are known to weight coherent-error modes differently. The paper only reports
$\varepsilon_{\text{approx}}$ so this is not a paper-gap, but for downstream trust we did NOT
cross-check with a second metric.

**How to close this gap:** compute average gate fidelity ($F_{\text{avg}}$) via
$F_{\text{avg}} = (|\operatorname{Tr}(U^\dagger V)|^2 + d) / (d^2 + d)$ at the same $(t, L)$
grid and verify the same ordering (opt < Trotter II < Trotter I in error).

## 5. Only Trotter I and Trotter II were implemented; Trotter IV skipped

The paper compares against Trotter I, II, and IV. We implemented only I and II. Since Trotter IV
is the strongest classical baseline, we may be over-stating the optimized-brickwall advantage vs
"the best classical method." The paper itself shows opt still beats Trotter IV at L=2,3, so this
almost certainly holds at n=3 too, but we did not verify.

**How to close this gap:** add a Suzuki-fourth-order Trotter to `src/replicate.py` (10-line
addition; the recursion is standard).

## 6. Single Hamiltonian instance

We tested exactly one $(J,g,h) = (2,1,1)$, matching paper's headline instance. The paper's
supplementary discusses robustness across coupling ratios; we did NOT rerun that sweep. So our
replication does not certify that the $\sim 10^2$ gap is robust across the phase diagram — only
at this one point.

**How to close this gap:** sweep $g \in \{0.5, 1.0, 1.5\}$ and $h \in \{0, 0.5, 1.0, 1.5\}$
(12 additional instances) at n=3, L=2, t=0.2, and verify the opt/Trotter-II ratio stays $\gtrsim 10$
across all of them.

## 7. What would make me DOWN-grade the verdict

The verdict would drop from REPLICATED to PARTIAL if a rerun at n=5 or n=8 showed the opt/Trotter-II
ratio compressing to $< 3\times$ (i.e., the ordering survives but the magnitude does NOT). It would
drop to NO-GO if opt were found to lose to Trotter II at any $(n, L, t)$ in the paper's own
tested regime — which our data does not show at n=3, but which we did not test at larger n.

## 8. What would make me UP-grade the confidence

The verdict would move from "REPLICATED at n=3" to "REPLICATED at paper's headline instance"
if the same code, unmodified, reproduced the $\sim 10^2$ gap at n=8 with a Newton-based optimizer.
This is the natural next step and is well within a single-day rerun budget.

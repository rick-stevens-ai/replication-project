# Failure / Deficiency Analysis — Quantum Autoencoder Replication

This is the honest what-was-not-done log for the QC-100 W2 replication of
Romero, Olson, Aspuru-Guzik 2017 (arXiv:1612.02806). Companion to the
higher-level critique section in `REPORT.tex`.

## 1. Paper-specific ensemble NOT reproduced
- **What the paper did:** compressed the $H_2$ molecular ground-state
  wavefunctions at several nuclear separations, using a Bravyi--Kitaev encoded
  representation.
- **What we did:** substituted a controlled 6-state ensemble drawn from a fixed
  2-D subspace of the 4-qubit Hilbert space (effective rank exactly 2).
- **Why the substitution:** the paper describes the molecular ensemble in
  words + integral tables but does not deposit the actual state vectors, and
  regenerating them requires a Hartree--Fock / active-space CI pipeline that
  was out of scope for a free-endpoint quick replication.
- **Consequence:** no paper-quoted molecular-compression fidelity number was
  directly matched. What was reproduced is the QAE *mechanism* and *scaling
  behavior*, not the specific tabulated $H_2$ result.

## 2. NO classical PCA / SVD baseline drawn
- The paper claims quantum-autoencoder compression is a useful primitive but
  does not compare it to classical rank-$k$ SVD of the same state vectors as
  vectors in $\mathbb{C}^{2^n}$.
- We inherited this deficiency: for pure states in a 2-D subspace, classical
  SVD would achieve $F = 1$ at $k = 1$ trivially, whereas our QAE gets
  $F \approx 0.78$ at $k = 1$.
- **Honest implication:** on this ensemble, the QAE is *worse than* the free
  classical baseline. A real quantum-advantage claim would require an ensemble
  where the state vectors are exponentially large to store classically but
  polynomially preparable on-device --- a regime not exercised here.

## 3. Maximum-compression case is optimization-limited
- The information-theoretic latent size for a 2-D subspace is $k = 1$, so a
  perfect encoder should reach $F = 1$ at $k = 1$.
- We reach only $F \approx 0.78$.
- **Root cause:** the combination of a 3-layer hardware-efficient ansatz
  (24 params) and COBYLA (a gradient-free simplex-style optimizer) gets
  trapped in local optima at maximum compression. Adding more restarts helped
  marginally; increasing ansatz depth or switching to a parameter-shift
  gradient method was not attempted in this pass.
- Reported transparently in the results table with regime label DEGRADED.

## 4. Compression-vs-fidelity trade-off NOT swept quantitatively
- We reported three data points ($k = 3, 2, 1$) rather than a smooth curve.
- The paper itself shows a modest sweep. A denser sweep (e.g., ensembles of
  varying effective rank at each $k$) would let one plot recon-$F$ vs
  effective-rank gap and check whether the QAE respects the information-
  theoretic bound $F \le 1$ iff $k \ge \text{eff-rank}$.

## 5. Noise + hardware entirely absent
- Purely noiseless statevector simulation. No shot-based cost estimation, no
  depolarizing / coherent / readout error models, no real-hardware run.
- This is the single largest gap between the replication and any practical
  deployment claim; the paper acknowledges it as future work but does not
  quantify a noise-tolerance envelope.

## 6. Scale is conceptual only
- $n = 4$ qubits. At this size a classical laptop trivially outperforms any
  QAE mechanism in wall-clock and memory terms. The replication is a
  correctness demonstration, not a performance one.

## 7. Cost-function variants NOT compared
- The paper discusses trash-fidelity vs swap-test-based costs. We implemented
  only the trash-fidelity variant. Swap-test cost would be a natural extension
  and is required for mixed-state inputs.

## What DID work honestly
- QAE mechanism independently reimplemented from scratch with only numpy +
  scipy; no external quantum library.
- Trash-fidelity training cost demonstrably tracks decoder-based reconstruction
  fidelity to three decimal places across all three latent sizes tested ---
  this is the paper's key design-choice claim and it holds on this ensemble.
- Monotone degradation of reconstruction fidelity under more aggressive
  compression is reproduced qualitatively.

## Verdict rationale
**PARTIAL** is the honest call: core mechanism works and the two central
qualitative claims (proxy-cost validity, graceful degradation) reproduce, but
the paper's specific molecular demonstration is substituted, no classical
baseline is drawn, and the maximum-compression regime is optimization-limited
rather than hitting the information-theoretic latent bound.

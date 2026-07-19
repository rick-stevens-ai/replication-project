# Failure Analysis — peng2022 SOAM single-particle replication

Honest accounting of what did **not** reproduce, what was out of scope, and the
sources of uncertainty. The physics claims (C1, C2, C3) reproduced; but this is
graded **PARTIAL** overall for the reasons below.

## 1. Absolute coupling axis does NOT map to the paper (primary limitation)

- **Symptom.** The paper's Fig. 2 uses Ω_R/ℏω = 0, 100, 250 and shows the
  degenerate l_z = ±1 ground state persisting up to Ω_R = 100 (middle panel),
  with the l_z = 0 state winning only around 250. Our diagonalization puts the
  l_z = ±1 → l_z = 0 transition at **Ω_R ≈ 8.5 in our HO units** — roughly an
  order of magnitude below the paper's window.
- **Root cause.** The review does **not publish** (a) the beam waist w in units
  of the oscillator length a_ho, (b) the exact prefactor normalization of
  Ω(r) = Ω_R (r/w)^p e^{−2r²/w²}, or (c) the ratio of the recoil energy E_R to
  the trap quantum ℏω. The peak of the radial Rabi profile is w-independent
  (max of x^p e^{−2x²} is fixed ≈ 0.3), so no choice of w reconciles the axis;
  the discrepancy lives entirely in the unspecified energy normalization / the
  definition of "Ω_R". This is a **missing-parameter** failure, not a modeling
  error: the *shape*, *degeneracy structure*, *symmetry*, and *first-order jump*
  are all correct.
- **What we did about it.** Rather than tune parameters to fake the paper's
  numeric axis (which would be dishonest), we present the three representative
  panels in our own HO units (Ω_R = 0, 6, 40) chosen to bracket the transition
  the same way the paper's panels do, and we record the paper's nominal values +
  the gap explicitly (`normalization_note` in results.json).

## 2. Interacting phase diagram (review claim C2) NOT attempted

- The review's headline is the **mean-field** angular-stripe / vortex / coreless
  phase diagram from the two-component Gross-Pitaevskii equation. We deliberately
  scoped to the **single-particle** Hamiltonian (Sec. III.A) to stay within the
  <5 min CPU budget and to have a claim with an unambiguous, analytic-checkable
  ground truth (the HO limit). The GPE ground states are therefore **not**
  reproduced here — only the single-particle seed (the l_z = ±1 degeneracy that
  underlies the angular stripe) is.

## 3. Bogoliubov / roton excitation spectra (review claim C3-review) NOT attempted

- Same scope decision. BdG spectra require the interacting ground state first and
  add a sparse eigenproblem per point; deferred.

## 4. Experimental confirmations (review claim C4) infeasible

- ⁸⁷Rb / ²³Na BEC realizations are cold-atom lab results; not replicable on this
  host by any means. Out of scope by construction.

## 5. Residual numerical caveats (small, controlled)

- **r = 0 handling.** We use a cell-centered grid + symmetrized Hermitian FD to
  avoid the coordinate singularity; the HO-limit check (energies match
  (|l_eff|+1)ℏω to < 1e-4) bounds this error as negligible for the reported
  claims. A formal NR / R_max convergence study was not run (listed as open
  question 5).
- **Transition Ω_R estimate (~8.5).** Located on a 0–40 grid at spacing 0.5;
  quoted to that resolution only. Its *absolute* value is meaningless vs the
  paper anyway (see item 1); only the existence and first-order nature matter.
- **Detuning split.** At δ = 0.5 (our units), Ω_R = 6, the ±1 degeneracy splits
  by 0.323 ℏω and the ground-state QAM becomes non-degenerate — direction set by
  sign(δ), consistent with the paper. The magnitude is parameter-dependent and
  not a paper-published number.

## Verdict rationale

- C1, C2, C3 each reproduce the **qualitative and structural** physics the review
  reports, with an analytic cross-check on C1. This is a genuine, non-stub
  replication of the single-particle sector.
- Because (i) the absolute coupling axis cannot be matched (unpublished
  normalization) and (ii) the interacting/experimental claims are out of scope,
  the honest overall grade is **PARTIAL**, not a full green replication.

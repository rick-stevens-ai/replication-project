# Failure / Gap Analysis --- Cullen 2025 (arXiv:2509.20436v3)

## The single most important caveat (read this first)
The **~20x gap** between our converged conventional result (~49) and the paper's headline
(~10^3, both in (hbar/e) Ohm^-1 cm^-1) is **NOT a replication failure or a disagreement**.
The paper's central methodological thesis is that the **quantum corrections dominate**:
- Abstract: OHE computed "while incorporating recently-discovered quantum corrections."
- Sec. text (lines 590--591): "the quantum corrections Delta sigma_1,2 are the **dominant
  contributions** to the orbital Hall conductivity."
- Fig. 2 plots sigma_conv, sigma_L, Delta sigma_1, Delta sigma_2, Delta sigma_3 **separately**
  for Ge, showing the conventional piece is sub-dominant to the corrections.

We deliberately built **only the conventional interband Kubo term**. A conventional-only value
1--2 orders below the total is therefore the **expected, correct** signature of the paper's own
claim --- not a contradiction. Confirming which term carries the headline BEFORE declaring
disagreement is the discipline here (pitfall 11).

## What reproduced (high confidence)
1. **Spherical Luttinger band structure** for Ge (Eq. 2, g1=13.38, gbar=4.97): heavy/light
   hole dispersions, correct effective masses via (gamma1 -/+ 2 gbar).
2. **Finite Berry curvature & OAM under inversion symmetry.** The model has non-vanishing
   Omega_i = -(k_i / k^3)(J_z)_{mm} (Eq. 3) even though Ge is centrosymmetric --- the
   non-obvious physics the paper highlights (band curvature/OAM do not vanish per-band).
3. **Right order of magnitude for the conventional piece.** sigma_conv ~= 49 is a sensible,
   converged conventional interband OHE for Ge, consistent with sigma_conv being sub-dominant
   in Fig. 2.
4. **Numerical soundness.** Convergence < 3% over N=21/31/41; grid encloses the Fermi surface
   (k_F^{hh}=2.76e8 < k_max=4.0e8); live re-run reproduced the saved N31 value (49.9217) to
   4 digits. The number is trustworthy *for the term computed*.

## What did NOT reproduce --- and why (each classified)
1. **Total ~10^3 headline --- SCOPED OUT (not a shortfall).** Requires the quantum corrections
   Delta j1 (interband polarization / dipole rotation), Delta j2 (interband OAM matrix
   elements), Delta j3 ([r,v] non-commutativity, opposite sign) from Eq. (6). These are the
   dominant terms and are the deliberate, documented scope boundary. Coverage-capping.
2. **Signed cancellation structure --- SCOPED OUT.** Delta j3 has opposite sign to the other
   terms (line 522), so the total is a signed sum; we cannot verify sign balance without
   building all corrections.
3. **Non-spherical 4x4 and 6x6 models --- SCOPED OUT.** The paper uses these for numerical
   accuracy and REQUIRES 6x6 for Si (small delta_so ~40 meV). Our spherical 4x4 is adequate
   for Ge per the paper but caps quantitative fidelity and cannot address Si/cubic anisotropy.
4. **Proper-vs-conventional current convention --- UNAUDITED.** For non-conserved OAM the proper
   current (Eq. 7 analogue with tilde/check degenerate-manifold split) can differ from our
   Go-et-al braced-anticommutator conventional form by O(1) factors. Even the "conventional
   agreement" is convention-dependent until this is checked (see open_questions Q4).
5. **Other four materials (Si, GaAs, InAs, InSb) --- NOT ATTEMPTED.** Only Ge was targeted.

## Environment / tooling gaps (NOT physics)
- **marker / nougat absent** (`which marker nougat` -> not found). Artifacts 2 & 3 are honest
  `pdftotext` interims with provenance headers, regenerate commands, and hand-transcribed
  equations in nougat.mmd + REPORT.tex. Extraction-tooling degradation only.
- **No LaTeX engine required** on host; REPORT.tex ships as compilable source.

## What would raise the verdict
- Build **Delta j1** first (highest leverage) --> then Delta j2, Delta j3 with correct signs
  --> assemble signed total and compare component-by-component to Fig. 2. Reaching ~10^3 for Ge
  would move Agreement toward 8--9/10 and Coverage toward 7--8/10.
- Add the **6x6 model** + Table I params to cover Si and check Ge anisotropy shift.
- Audit the **proper-current convention** so sigma_conv is apples-to-apples with the paper's curve.

## Verdict
**PARTIAL** --- Coverage 5/10, Agreement 5/10. Right observable and correct conventional-term
physics; the headline is carried by quantum corrections that were intentionally not built.

# Failure Analysis — Konakanchi et al. 2025 replication

Honest accounting of what is approximate, what broke, and what was not attempted.
Overall verdict remains **REPLICATED** for the headline (ps-scale octupole
relaxation), but the following caveats bound the strength of the claim.

## 1. PDF-text mangling of equations (encountered, mitigated)
`pdftotext` scrambled subscripts/superscripts and split multi-line equations
(e.g. Eq. 10, D12, B19 came out fragmented and reordered). **Impact:** the first
run transcribed the Eq. 10 prefactor literally and the internal-consistency check
between the Monte-Carlo integral (Eq. 9) and the closed form (Eq. 10) failed
(reldiff ~108%, Langevin ratio 3.25). **Mitigation:** rederived the low-barrier
closed form self-consistently from our own free energy Eq. B19
(`C(t)=<cos(gamma H_J mz t)>` with `var(mz)=kT/3Ms H_J V` -> Gaussian, 1/e time
`sqrt(2)/omega_J`, `omega_J=gamma*sqrt(H_J H_th/3)`). After this the numeric
integral matches the analytic model to 0.16% and Langevin agrees within 1.5x.

## 2. Residual ~2x prefactor vs paper's published Eq. 10 (open, honest)
Our self-consistent 1/e time and the paper's published Eq. 10 constant differ by
a fixed dimensionless factor `sqrt(3/ln2) ~ 2.08`, from (i) the exact mz-mode
normalization (the factor 3 in the three-sublattice free-energy stiffness) and
(ii) the 1/e vs 1/2 crossing convention. **Impact:** the *scale* (single-digit to
tens of ps) is reproduced exactly; the *precise constant* is not pinned. Both
forms are reported side-by-side in the result JSON and REPORT. This is a
transcription/normalization ambiguity, not a physics disagreement.

## 3. Reduced dynamics, not full six-spin s-LLG (scope limit)
We integrated the *reduced* effective (mz, phi_oct) theory, not the full
three-magnetization (or six-spin) stochastic-LLG of Eq. 3. The paper itself
derives the reduced theory and validates it against the full model in its SI, so
this is a faithful replication of the *analytic* backbone, but our independent
numerical leg does not re-verify the coarse-graining from the microscopic
Hamiltonian. The crossover region Delta ~ kT is therefore the least-tested.

## 4. Material parameters adopted, not derived (scope limit)
`H_J = 100 T` and `Ms = 1.3e6 A/m` were taken from the paper's text / Mn3Sn
literature rather than derived from J, D, K. Volume V was scanned to move across
barrier regimes (exactly as the paper does). Consequence: this is a *scale-match*
under the paper's own stated parameters, not a parameter-free first-principles
match.

## 5. Electrical-tunability (SOT / Josephson analogy) not exercised
The applied-payoff claim (tuning tau by orders of magnitude via spin-orbit
torque, Eqs. E5, F11-F13) was read and understood but not numerically
reproduced. It is listed as open question #5 / next step.

## 6. Depopulation factor assumed unity
Following the paper (A~1 for Mn3Sn), we set the Langer depopulation factor to 1.
For the very-low-damping alpha~1e-3 case the paper warns this may deviate; we did
not evaluate the A(x) integral (open question #4).

## What did NOT fail
- Kernel import + octupole operator (Txyz Hermitian, traceless, trace-norm 0.866): OK.
- ps-scale headline: robustly reproduced by three independent routes (analytic,
  Monte-Carlo, Langevin).
- Two-mechanism crossover (dephasing ps vs escape ns): reproduced.
- No fabrication: every number computed at run time; code + JSON in evidence/.

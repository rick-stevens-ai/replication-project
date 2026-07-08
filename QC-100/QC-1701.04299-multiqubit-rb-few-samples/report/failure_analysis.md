# Failure analysis / honest critique — QC-1701.04299

**Verdict on file: REPLICATED.** This document exists to make explicit the *limits* of that verdict — what was and was not actually verified — so downstream readers don't over-interpret the checkmark.

## What "REPLICATED" here means
The paper's central *practical* claim (C3: few random RB sequences suffice to estimate the average infidelity r reliably) was independently reproduced on a real Qiskit Aer 2-qubit RB simulation with a 300-resample bootstrap. The paper's *analytical* anchor number (C1: N=173 for the paper's single-qubit example) was reproduced within 13 % using the paper's own eq. (10). Both reproductions used independently generated data + independently written code.

## What "REPLICATED" does NOT mean

### 1. The sample-complexity claim was tested via bootstrap variance, not by comparing measured σ_r(N) to the paper's predicted σ_r(N) curve
The paper's variance bound is a *functional* prediction — σ_r as a function of (N, m, r, d, u). This replication measured σ_r(N) at a *single* (d=4, r=0.016, m-set) point and verified that at N=5 the relative std was already <5 %. That is *consistent with* the paper but does not test the functional form. If the paper's variance formula gave σ_r(N=5)=1 % where we measured 4.65 %, we would not have detected the disagreement. This is Open Question #1.

### 2. No head-to-head comparison against Wallman-Flammia [24] sample counts on our own simulated data
The paper's argument-of-value is that eq. (10) requires order-of-magnitude fewer samples than ref [24]. We reproduced the *paper's own N=173 example number* and quoted the ref-[24] range (145-1631) from the paper's Table 1. We did *not* simulate an actual [24]-sized ensemble on our data to show the empirical gap. So we replicated the *bound*, not the *comparison*.

### 3. Small-N bias was tested only weakly
At N=5 we reported |r_mean − r_ref| = 1.7×10⁻⁵ against the N=100 reference — a null result on scalar bias. But we did *not* check for:
- Skewness of the bootstrap distribution at N=5 (curve_fit can produce heavy-tailed r estimates when the fit is close to unidentifiable).
- Nominal coverage of the bootstrap CI (does a 95 % bootstrap CI actually contain the truth 95 % of the time?).
- Bias structure vs r or vs noise strength (we only tested one r).
Point-estimate consistency ≠ estimator soundness.

### 4. Eq. (9) was not implemented
The 13 % gap between our N=195 and the paper's N=173 is *definitionally* the gap between eq. (10) (looser, easier) and eq. (9) (tighter, more machinery). We did not implement eq. (9). So we did not reproduce the *exact* 173 number; we reproduced a related number within 13 %.

### 5. Qubit-count independence (C5, Fig. 2b) is spot-checked from the paper, not reproduced
The paper's most striking scaling claim was not independently evaluated even analytically here (would require coding eq. (11) across q). Open Question #4.

### 6. IRLS vs OLS (C4) not tested
We used bounded curve_fit (nonlinear OLS) throughout. The paper's fitter-choice recommendation is not re-litigated.

### 7. Single noise model
All results are under isotropic Markovian depolarizing noise. The paper's variance bound formally assumes gate-independent Markovian noise. Real hardware has coherent errors, crosstalk, and non-Markovianity. Whether "few samples suffice" survives those regimes is an open scientific question, not a defect of this replication per se — but consumers should not read "REPLICATED" as "would work on IBM hardware without further check". Open Question #2.

### 8. Sample size in the bootstrap
N_boot = 300 is adequate for the coarse relative-std numbers we report but is not enough to trust the tails (e.g. 99 % CI coverage). A serious repeat of Open Question #1 would want N_boot ≥ 1000.

## Failure modes ruled OUT
- **Wrong noise attachment** — verified: 1.47 CX/Clifford × p_cx × 3/4 + noise from 1q gates ≈ 0.015, matches fitted r=0.0159 at ~5 % (§4.1 of REPORT.md). This is the correct "physical" per-Clifford infidelity, so the RB decay is capturing what it should.
- **Inverse-Clifford bug** — survival probability at m=0 (extrapolated) is A+B ≈ 0.98, close to 1 as expected for correct inverses.
- **Curve-fit unidentifiability** — fit returned f, A, B all well inside (0,1) bounds; no boundary artifacts.
- **Fabricated numbers** — every number in REPORT.md traces back to `report/evidence/*.json`. No LLM produced any numeric result.

## Failure modes NOT ruled out (should be flagged in downstream use)
- Bootstrap-CI coverage at low N (see §3 above).
- Behavior under non-Markovian or coherent noise (see §7).
- Extension to q ≥ 5 (see §5).
- Interaction with post-2017 RB variants (character RB, cycle benchmarking; Open Question #3).

## Recommendation to Rick / QC-100 reviewer
Treat this replication as a **solid single-point validation** of the paper's practical thesis, *not* as a comprehensive audit of the variance-bound framework. The verdict REPLICATED is defensible for C3 (empirical) + C1 (analytical anchor). C2/C4/C5 remain open and are explicitly flagged UNTESTED in the claims table. The five open questions in `open_questions.json` are the natural next-wave experiments if this paper is picked up for deeper study.

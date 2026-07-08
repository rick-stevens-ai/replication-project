# Failure analysis / honest critique — arXiv:1703.05169 replication

**Verdict stands: REPLICATED (algorithmic core).** This document exists to make
the *weaknesses* of that verdict explicit, so a reader can decide for themselves
how much weight the "REPLICATED" label carries.

## 1. What was really regenerated vs quoted

**Independently regenerated (from scratch, not lifted from paper):**
- The Qiskit two-qubit Hadamard-test circuit (Fig. 1a). Verified against
  Eq. 1 of the paper to <1e-9 abs on 60 test triples — this is genuine
  circuit evaluation, not analytic shortcut.
- The RFPE outer loop (Appendix B): SMC particle sampling, per-particle
  likelihood weighting, weighted-mean/std Gaussian refit.
- The Ferrie particle-guess heuristic for (M, Θ).
- A grid-Bayes reference implementation as an independent cross-check
  (`debug3_grid.py`), which turned out to be essential for diagnosing the
  Θ=μ symmetry bug.

**Not regenerated (but not needed to test C1/C2):**
- The 1000-particle SMC of the paper's own classical-sim curve — we ran
  20000 particles. This is more compute, not different algorithm.
- The paper's exact random-seed / shot stream.
- The photonic hardware (fabrication, SFWM source, SNSPD readout, thermo-
  optic phase shifters). C5 is out of scope.

## 2. Heisenberg-scaling: assertion vs verification

The "1.12× Heisenberg bound" statement is computed from **one** seed-38 run,
comparing that run's final |err| to the fundamental $1/N_{\text{tot}}$ bound at
its total $\sum M = 5981$. This is a single-point ratio, not a scaling fit.

A proper Heisenberg-scaling verification would either:
- Fit the log-log slope of err vs $N_{\text{tot}}$ over the post-lock regime
  of the 200-trial ensemble (Experiment B has the data; the fit was not
  performed).
- Or plot the ensemble-mean product $\sigma_{\text{step}} \cdot
  N_{\text{tot}}(\text{step})$ vs step and show it flat.

Neither was done. The `scaling_rfpe_vs_sql.png` plot shows the two-regime
plateau/collapse *shape*, which is qualitatively consistent with Heisenberg
saturation after lock — but the plot's slope was not fit and reported.

**Honest characterization:** C2 is *qualitatively demonstrated* (RFPE gets
far below the SQL slope; single-run saturates the Heisenberg bound), not
*quantitatively verified* as an ensemble scaling law. Both are reasonable
readings of "REPLICATED", but the stronger claim requires the extra fit.

## 3. Cherry-picked seed

Seed 38 was selected from a 50-seed sweep as "representative of a successful
run." The paper does the same for its Fig. 2a (single successful run
alongside the 1000-run dashed average), so this replicates *what the paper
did* rather than *what a strict first-seed protocol would demand*.

Experiment C (100-seed distribution) exists specifically to make this
visible: median final err is 4.5×10⁻² rad, only 4% of seeds reach the
paper's headline in 50 steps, 27% reach 10⁻² rad. A reader who requires
"the median run reproduces the headline" will find this replication
**does not meet that stronger bar**.

## 4. Noise-model calibration: absent

C4 (noise robustness) is entirely untested. The current code runs the ideal
Qiskit statevector — perfect gates, no depolarizing $T_2$, no heralding
loss, no phase-shifter drift. The paper's headline noise claims
(σ_φ tolerance to ~0.3 rad, polynomial-not-exponential $T_2$ degradation)
are therefore *unverified* here.

This is a limitation, not a bug. The code supports adding noise (see open
question #3 for the concrete extension recipe). But as-is, the current
replication says nothing about whether RFPE would still saturate the
Heisenberg bound on a *noisy* chip.

## 5. Chemistry (C3) not run

The H₂ bond curve is one Jordan-Wigner mapping away from C1. Not running
it doesn't threaten the algorithmic-core verdict, but it means the
end-to-end "quantum-chemistry-on-silicon" story the paper tells is
*algorithmically plausible from our data* but *not directly demonstrated*.

## 6. Silicon-qubit vs silicon-photonic disambiguation

The task brief suggested "donor qubits / silicon quantum dots". This is a
category error: arXiv:1703.05169 is a **silicon-photonics** paper
(waveguide-encoded photonic qubits from an SFWM source, on-chip Mach-Zehnder
interferometers), not a silicon-spin-qubit paper. We replicated the correct
paper for the arXiv ID. No donor-spin, Kane-qubit, or QD physics is
involved. Flagging this in case downstream aggregation tries to compare
against silicon-spin literature.

## 7. Bug we caught and one we probably didn't

**Caught:** the Ferrie heuristic requires Θ~P(φ) sampled, not Θ=μ.
Θ=μ makes the likelihood symmetric around μ and RFPE never moves. The
grid-Bayes reference caught this within an hour of the first stuck-at-μ
run. Documented in §3.6 of REPORT.md.

**Probably not caught:** particle-refit variance at low particle counts. The
paper says 1000 particles; we needed 20000 to get a solid single-run demo.
This is either (a) a real hidden dependency on n_particles that the paper
under-reports, or (b) a subtle difference in how the resample-weight-refit
step is done. We picked (a) as the working hypothesis but did not
rigorously test (b) by porting the paper's exact SMC to compare.

## 8. What would move the verdict

- **Downgrade to PARTIAL** would be justified if a reader insists that a
  proper Heisenberg-scaling verification (log-log slope fit on the ensemble)
  is required, not just a single-run bound-saturation ratio.
- **Upgrade to REPLICATED+ / stronger** would come from: doing the ensemble
  slope fit; running C4 noise sweep; running C3 H₂ curve. All are open
  questions in `open_questions.json` with concrete next-steps.

## 9. Summary line

**REPLICATED for the algorithmic core (C1 numeric, C2 qualitative
saturation). Not tested: C3 (chemistry), C4 (noise robustness). Not
reproducible: C5 (hardware). Ensemble scaling fit would strengthen C2 from
"qualitative demonstration" to "quantitative verification"; adding it is
the highest-leverage next step and requires no new sims.**

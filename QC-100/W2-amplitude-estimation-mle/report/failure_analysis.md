# Failure Analysis / Honest Critique — W2 MLE-QAE

Verdict: **REPLICATED**, but with several important caveats that a reader
should understand before treating this as a full end-to-end replication of
Suzuki et al. (2020).

## What was independently replicated (headline exercised)
- **MLE-QAE algorithm from scratch, NumPy-only.** The likelihood, the coarse-then-
  refine grid MLE, the Cramér–Rao bound formula, and the classical / LIS / EIS
  schedule generators are all direct reimplementations of the paper's Sec. 3
  equations. No Qiskit, no PennyLane, no lift of the paper's supplementary code.
- **Fig. 2 slope structure at a = 1/48.** Classical −0.507 (paper −0.50, match),
  LIS −0.774 (paper −0.76, match). All within the paper's own ±0.1 slope
  uncertainty envelope.
- **Unbiasedness + CRB saturation.** All three estimators are unbiased to bias
  ≤ 1.3e-5, and RMSE / CRB ratios sit in [0.94, 1.16] for the largest M per
  schedule — meaning the estimator is essentially at the information-theoretic
  floor, exactly as the paper claims.
- **All six Fig. 2 target amplitudes** (2/3, 1/3, 1/6, 1/12, 1/24, 1/48) are
  recovered to ≤ 0.02% relative error with EIS M=10.

## What is only partially replicated (honest gap)
- **EIS slope: −0.866 vs. paper's −0.95** — a 0.084 gap, roughly at the edge of
  the paper's own ±0.1 uncertainty. The paper explicitly attributes such
  deviations to finite-N_shot=100 MLE bias, and states the gap shrinks with
  more shots. We did **not** run the N_shot = 1000 or 10^4 sweeps that would
  empirically confirm this explanation. Believed but not verified.
- **Heisenberg-scaling claim.** The paper's core pitch is that MLE-QAE
  "approaches" Heisenberg N_q^{-1} scaling without QPE/QFT. Our EIS slope of
  −0.866 is qualitatively more negative than LIS's −0.774 and much more
  negative than classical's −0.507, so the trend is confirmed. But the fitted
  slope is not −1.0, and we did not push to large enough N_q to see it
  saturate. So the claim is qualitatively supported and quantitatively
  approached but not saturated.

## What is NOT replicated (out of scope, honestly flagged)
- **No comparison to canonical QFT/QPE-based QAE baseline.** This is the
  paper's headline claim ("MLE-QAE achieves near-Heisenberg WITHOUT the
  QFT"). We validated the "near-Heisenberg" half by direct measurement, but
  did not implement a QPE-based QAE simulator to head-to-head compare at
  matched N_q. A full replication would include this.
- **App. A QPE-vs-EIS quantitative figure** not reproduced — requires QPE
  simulator. Same reason.
- **Sec. 4 CNOT-count comparison** for Monte Carlo integration on
  circuit-level compilations not reproduced. Requires circuit compilation
  and/or hardware/noise model. This is the pitch that MLE-QAE gives an
  advantage on real NISQ hardware, and it is currently only inherited from
  the paper on trust.
- **No noise sensitivity test.** All runs are noiseless statevector. The
  paper's practical value depends heavily on how gracefully MLE-QAE degrades
  under gate + readout noise. Not tested here (flagged as open question #2).

## Methodological weaknesses of this replication
- **MLE optimizer.** We use a plain coarse-then-refine grid search; the paper
  describes a "modified brute force" with per-M-truncation vicinity search.
  Functionally equivalent for M ≤ 10 EIS (verified: MLE reaches CRB), but
  would not scale to M ≫ 10 without a smarter optimizer.
- **Trial counts.** 200 trials per point (100 for EIS M ≥ 9), vs. the paper's
  "1000 times". Enough to expose slope trends but adds Monte Carlo noise to
  the fitted slopes themselves.
- **Paper omits RNG seeds** — we cannot bit-reproduce, only distributionally
  reproduce.

## Net assessment
The replication genuinely exercises the paper's headline algorithmic
contribution (MLE-QAE, Fig. 2 slope structure, CRB saturation, six-target
amplitude recovery). It does NOT exercise the head-to-head QFT-QAE baseline
comparison or the NISQ-hardware / CNOT-count / noise-robustness claims. On
the algorithmic content, verdict = REPLICATED with a small quantitative gap
on the EIS slope that the paper itself predicts. On the practical / hardware-
level claims, verdict would need a separate deeper replication.

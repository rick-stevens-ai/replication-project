# Failure analysis — MLAE replication

Honest critique of what this replication does and does NOT establish.

## What is genuinely replicated

The headline scaling claim is exercised end-to-end. From-scratch Qiskit
circuits, real shot-based `qiskit-aer` simulation (not analytic), an
independent MLE estimator, and 100 trials per (schedule, M) point produced:

- Classical slope −0.516 (paper −0.50, Δ = +0.016)
- LIS slope −0.727 (paper −0.76, Δ = +0.033)
- EIS slope −0.930 (paper −0.95, Δ = +0.020)

The EIS slope is unambiguously steeper than classical (−0.93 vs −0.52) and
approaches the Heisenberg-limit target of −1. The ~10× RMSE reduction at
matched Nq ≈ 5×10⁴ vs classical extrapolation is quantitatively confirmed.
On the narrow question the paper actually asks — "does MLAE reach
near-Heisenberg scaling without QPE, at this operating point?" — the
answer is yes, at the ±0.04 slope precision achievable with 100 trials
per point.

## What is NOT replicated (honest bounds)

### 1. Depth / ancilla savings claim — asserted, not measured
The paper's real motivation is that MLAE removes the QFT ancilla register
and shallower circuits should be more hardware-friendly. This replication
did NOT implement canonical Brassard-Høyer-Mosca-Tapp QAE alongside for a
head-to-head at matched 2Q-gate-count or matched circuit depth. We
reproduced the estimator scaling in oracle calls; we did not verify the
practical hardware-cost advantage that motivates the whole paper.

### 2. Noiseless simulation only
Zero noise model. `qiskit-aer.AerSimulator` with the default (perfect)
backend. The paper's applicability claim to near-term hardware — that
MLAE's shallower circuits should be more noise-robust than QPE — is
completely untested here. It is possible (and consistent with subsequent
literature) that under realistic 2Q-gate error rates the EIS schedule's
advantage collapses long before M = 8, because Q^{2^7} = Q^{128} at
p_2q ~ 5e-3 has essentially unit total-error probability. We flag this
as the single most important open question.

### 3. Single amplitude — no branch-identifiability sweep
Only a = 1/48 was tested. The paper picks this operating point precisely
because it is in the "easy" regime for the MLE. The failure mode where
the likelihood surface P(1 | m_k, θ_a) = sin²((2m_k+1) θ_a) is
approximately multimodal (θ_a near π/4, or small a with tight shot budget)
was NOT characterized. Grid + polish worked at N_shot = 100 for the tested
point, but we cannot report miss-rate as a function of (a, N_shot).

### 4. MLE convergence not stress-tested
The grid-then-polish estimator worked at all 17 (schedule, M) points ×
100 trials tested. No trial threw a wrong-branch estimate large enough to
noticeably distort RMSE. But we did not deliberately probe adversarial
schedules or the small-N_shot corner, and we cannot claim the estimator
is robust in general.

### 5. No comparison to modern successors
Iterative QAE (Grinko et al., 2019/2021), Faster QAE (Nakaji), and
shot-optimized variants post-date this paper and are now generally
preferred. We benchmarked MLAE against nothing except itself and the
paper's own claims. Whether MLAE is competitive with IAE at fixed target
accuracy is not addressed.

### 6. No end-to-end application
The paper is application-agnostic; a = 1/48 is a microbenchmark. Real
applications (quant finance option pricing, Monte-Carlo integration for
physics) use non-trivial state-prep circuits A whose depth may swamp
Q^{m_k} at small m_k, potentially wiping out the EIS advantage until M
is large. No end-to-end task was measured.

## Methodological caveats

### Transpile cache
We added an LRU cache over `transpile()` keyed by `(θ_a, m)`. This is a
pure-function memoization — the transpiled circuit is deterministic in
its inputs — so it changes no physics and cannot bias results. The slope
numbers would be identical without it, just slower to obtain. Flagged
because it is a modification vs. the pre-existing draft.

### Slope-fit precision
Each slope is a linear fit to 5–6 points (log-log). With 100 trials per
point, the per-point RMSE has ~10% relative uncertainty, translating to
roughly ±0.03 slope uncertainty. Our Δ values (+0.016, +0.033, +0.020)
are all within this noise band; the "agreement" is real but not
knife-edge precise. A larger trial count would tighten this but was not
budgeted.

### MLE grid resolution
N_grid = 4096 on (0, π/2) followed by scipy polish. Adequate at
N_shot = 100 per round; not audited at small N_shot where the likelihood
surface has narrower peaks.

## Bottom line

- **Slope-scaling claim at a = 1/48, noiseless: REPLICATED with quantitative
  agreement to ±0.04.**
- **Everything else the paper implies (hardware advantage, noise robustness,
  general amplitude range, application-level benefit): NOT ADDRESSED here.**

This replication is a real, honest reproduction of the paper's central
numerical figure. It is not a general endorsement of MLAE as a practical
NISQ algorithm; the paper made the narrower scaling claim, we tested that
narrower claim, and it held.

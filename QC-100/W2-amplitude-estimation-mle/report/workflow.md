# Workflow — W2 MLE-QAE (Suzuki et al. 2020)

## Paper acquisition
- Source: arXiv preprint of Suzuki, Uno, Raymond, Tanaka, Onodera, Yamamoto (2020),
  "Amplitude estimation without phase estimation" (Quantum Information Processing).
- Only the classical-statevector Sec. 3 content was targeted for reimplementation.

## Reimplementation
- Language / stack: Python 3 + NumPy only. No Qiskit, no PennyLane, no external QAE
  library. All ~200 lines of `replicate.py` are self-contained.
- Key routines:
  - `p_good(m, theta_a) = sin((2m+1)*theta_a)**2` — closed-form good-outcome prob.
  - `simulate(m_list, N_shot, theta_a, rng)` — Bernoulli-samples h_k for each m_k.
  - `neg_log_L(theta, m_list, h_list, N_list)` — log-likelihood over the schedule.
  - `mle_estimate(...)` — coarse grid over [0, pi/2] with density ~ 20 * (2*m_max + 1),
    then local refine with 2001 points spanning ±3 coarse spacings.
  - `crb(m_list, N_shot, a)` — Cramér–Rao bound from paper Eq. (13).
  - Schedule generators for classical / LIS / EIS matching Sec. 3.4.

## Simulation runs
- Targets: a ∈ {2/3, 1/3, 1/6, 1/12, 1/24, 1/48}.
- Schedules (per paper):
  - classical: N_shot in effect scales with M ∈ {1, 3, 9, 29, 99, 299, 999}
  - LIS: M ∈ {1, 2, 3, 5, 8, 12, 20, 31}
  - EIS: M ∈ {0, 1, ..., 10}
- Per-point trial count: 200 (dropped to 100 for EIS M ≥ 9 to bound wall time).
- Total: 156 configurations logged to `results.json`.

## Analysis
- Log-log least-squares slope fit of RMSE(a_hat) vs total queries N_q, over
  N_q ∈ [10^3, 10^5], separately for classical / LIS / EIS at a = 1/48.
- RMSE / bias / CRB tabulated per (schedule, M, a).

## Reporting
- Top-level `REPORT.md` = authoritative source-of-truth; already in place at
  project inception. NOT modified by this backfill.
- Backfill added standard 7-artifact bundle in `report/` + extraction stub.
- No hardware runs, no calls to paid endpoints, no re-run of the simulator.

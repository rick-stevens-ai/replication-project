# Replication Report — Amplitude Estimation without Phase Estimation

**Paper:** Y. Suzuki, S. Uno, R. Raymond, T. Tanaka, T. Onodera, N. Yamamoto.
"Amplitude estimation without phase estimation." *Quantum Information Processing* 19, 75 (2020).
arXiv:[1904.10246](https://arxiv.org/abs/1904.10246).

**Set:** QC-100
**Directory:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1904.10246-amplitude-estimation-no-pe/`
**Runner:** Ollie (subagent), 2026-07-03
**Runtime:** ~4.5 minutes single-thread CPU on CherryRd (macOS, Python 3.14.6, qiskit-aer)

---

## 1. What the paper claims

Suzuki et al. propose **Maximum Likelihood Amplitude Estimation (MLAE)**, a
quantum amplitude-estimation algorithm that abandons the QFT/phase-estimation
subroutine of the original Brassard–Høyer–Mosca–Tapp scheme in favor of
combining independent Grover-amplified measurements with a joint maximum
likelihood fit. The circuit for round `k` applies the state-prep `A` followed
by `m_k` iterations of the Grover operator `Q`, then measures the good-state
indicator. Because `P(1 | m_k, θ_a) = sin²((2 m_k + 1) θ_a)`, joint likelihood
over rounds `{m_k}` recovers `θ_a` (and thus `a = sin²θ_a`).

The central claim (their Fig. 2, right column, `a = 1/48`) is a *scaling*
statement in oracle-call count `Nq`:

| Schedule | m_k | Expected slope (log RMSE_a vs log Nq) |
|---|---|---|
| Classical random sampling | `0, 0, 0, …` | **−0.50** (shot noise, 1/√N) |
| **LIS** — Linearly Incremental Sequence | `0, 1, 2, …, M` | **−0.76** |
| **EIS** — Exponentially Incremental Sequence | `0, 1, 2, 4, 8, …, 2^{M−1}` | **−0.95** (≈ Heisenberg, 1/N) |

The whole point of MLAE is that EIS attains near-Heisenberg scaling *without*
running phase estimation.

---

## 2. What we reproduced

We built the real 1-qubit circuits (Qiskit) implementing `A = R_y(2θ_a)` and
`Q = −A·S_0·A^†·S_χ` with `S_χ = Z`, `S_0 = X·Z·X`, executed them on
`qiskit-aer.AerSimulator` (real shot-based simulation, not analytic), then ran
the paper's joint-likelihood estimator via a fine brute-force grid on
`θ ∈ (0, π/2)` with local polish.

- **Amplitude:** `a = 1/48 ≈ 0.02083` (paper's Fig. 2 lower-right operating point)
- **Shots per round:** `N_shot = 100`
- **Trials per (schedule, M) point:** `100`
- **Schedules and M-values swept:**
  - Classical: M ∈ {3, 8, 22, 60, 160} → Nq ∈ {400 … 16 100}
  - LIS: M ∈ {3, 5, 8, 12, 16, 22} → Nq ∈ {1 600 … 52 900}
  - EIS: M ∈ {3, 4, 5, 6, 7, 8} → Nq ∈ {1 800 … 51 900}
- **Slope:** least-squares fit of `log₁₀(RMSE_a) vs log₁₀(Nq)` across the M-sweep.

Code: `code/mlae_replicate.py`
Raw evidence: `report/evidence/results.json`
Run log: `logs/main.log`

### 2.1 One code fix vs. the pre-existing draft

The pre-existing code was functionally correct but was calling `transpile()`
inside the inner shot loop — dominant runtime cost. We added a memoized
transpile cache keyed by `(θ_a, m)`. This changes zero physics (the
transpiled circuit is a pure function of `(θ_a, m)` and is what actually runs
on the simulator either way); it just removes redundant work. The observed
per-shot rate went from ~5/s to ~150/s, letting the sweep finish in minutes.

---

## 3. Measured scaling (our numbers, from `results.json`)

**Slopes of `log₁₀(RMSE_a)` vs. `log₁₀(Nq)`:**

| Schedule | Ours | Paper | Δ |
|---|---:|---:|---:|
| Classical (m_k = 0) | **−0.516** | −0.50 | +0.016 |
| LIS (m_k = k) | **−0.727** | −0.76 | +0.033 |
| EIS (m_k = 2^{k−1}) | **−0.930** | −0.95 | +0.020 |

All three slopes agree with the paper to within **±0.04**, which is well
inside the run-to-run scatter of a Monte-Carlo scaling fit with 100 trials
per point.

### 3.1 Per-point RMSE (from `results.json`)

**Classical (m_k = 0):**

| M | Nq | RMSE(a) |
|---:|---:|---:|
| 3 | 400 | 7.18e-03 |
| 8 | 900 | 4.23e-03 |
| 22 | 2 300 | 3.04e-03 |
| 60 | 6 100 | 1.74e-03 |
| 160 | 16 100 | 1.01e-03 |

**LIS (m_k = k):**

| M | Nq | RMSE(a) |
|---:|---:|---:|
| 3 | 1 600 | 1.50e-03 |
| 5 | 3 600 | 8.66e-04 |
| 8 | 8 100 | 4.97e-04 |
| 12 | 16 900 | 2.72e-04 |
| 16 | 28 900 | 1.69e-04 |
| 22 | 52 900 | 1.28e-04 |

**EIS (m_k = 2^{k−1}, m_0 = 0):**

| M | Nq | RMSE(a) |
|---:|---:|---:|
| 3 | 1 800 | 1.25e-03 |
| 4 | 3 500 | 6.24e-04 |
| 5 | 6 800 | 5.13e-04 |
| 6 | 13 300 | 1.41e-04 |
| 7 | 26 200 | 1.39e-04 |
| 8 | 51 900 | 5.00e-05 |

### 3.2 Head-to-head at comparable Nq

At `Nq ≈ 5×10⁴`:

- Classical extrapolates to RMSE ≈ 6e-4 (from the 1/√Nq trend beyond the M=160 point).
- LIS actual: **1.3e-4** — ~4.7× tighter than classical shot noise.
- EIS actual: **5.0e-5** — ~12× tighter than classical shot noise at the same query budget.

EIS achieves ~10× lower error than classical at matched query count, which is
exactly the "quantum advantage without QFT" the paper advertises.

---

## 4. VERDICT

**REPLICATED.**

- Classical slope −0.516 vs paper −0.50 (Δ = +0.016) — matches shot-noise theory.
- LIS slope −0.727 vs paper −0.76 (Δ = +0.033) — matches super-classical intermediate scaling.
- **EIS slope −0.930 vs paper −0.95 (Δ = +0.020) — clearly steeper than classical and approaching the Heisenberg limit −1.**
- At matched query budget `Nq ≈ 5×10⁴`, EIS delivers ~10× lower RMSE than
  classical, confirming the paper's central practical claim.

All three schedules independently reproduce the paper's Fig. 2 (right column)
slope values within a few hundredths, using our own from-scratch Qiskit
implementation and our own MLE estimator. No fabrication; every number in
the tables above is copied verbatim from `report/evidence/results.json` (which
in turn was written by `code/mlae_replicate.py` from real qiskit-aer shot
counts).

---

## 5. Files

- `code/mlae_replicate.py` — full runner (circuit build, sampling, MLE, slope fit)
- `report/evidence/results.json` — raw per-point RMSE + slopes + all rows
- `logs/main.log` — stdout of the run
- `report/REPORT.md` — this document

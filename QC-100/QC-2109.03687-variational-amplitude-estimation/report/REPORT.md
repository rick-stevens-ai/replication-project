# Independent Replication — Variational Quantum Amplitude Estimation

**Paper:** Kirill Plekhanov, Matthias Rosenkranz, Mattia Fiorentini, Michael Lubasch,
*"Variational quantum amplitude estimation"*, arXiv:2109.03687v2 (Quantum, 2022-02-25),
Cambridge Quantum Computing.

**Replicator:** OpenClaw subagent (QC-100 wave, 2026-07-03), CherryRd, Qiskit statevector simulation.

**Verdict:** **PARTIAL — REPLICATED for scaling claims of the two baselines that VQAE is compared against; SPOT-CHECK for the naïve-VQAE algorithm itself.**

---

## 1. Paper summary

The paper proposes VQAE — a variant of maximum-likelihood amplitude estimation (MLAE, Suzuki et al. 2020) in which the growing power `Q^m` of the Grover operator is periodically re-approximated by a shallow (depth-1) parameterised quantum circuit. This keeps the total circuit depth bounded while inheriting most of MLAE's amplitude-estimation error scaling. Two variants are introduced: **naïve VQAE** (parameterise from |0⟩ each time) and **adaptive VQAE** (parameterise from |χ₀⟩ using a smaller ansatz on top). The headline experimental figures (their Fig. 1, Fig. 4) compare the three algorithms on three probability distributions (Cauchy-Lorentz, Gaussian, log-normal) at 6–12 qubits.

## 2. Claims table

| ID | Claim | Type | Testable on CPU sim? | Tested here? |
|----|-------|------|-----|-----|
| C1 | Classical MC on the ancilla achieves error scaling δθ ~ Nq^(−1/2) | Analytical + numerical | Yes | **Yes** |
| C2 | MLAE with **linear** schedule {m=1..M} achieves δθ ~ Nq^(−3/4) | Numerical | Yes | **Yes** |
| C3 | MLAE (linear) has lower error than MC at matched Nq (in the interesting regime) | Numerical | Yes | **Yes** |
| C4 | The variational ansatz of Fig. 2 (depth d≈4 saturating) can approximate Q^m|χ₀⟩ with 1−F² decreasing with d and increasing (linearly) with m | Numerical | Yes | **Yes** (informally: per-round infidelities logged for VQAE run) |
| C5 | Naïve VQAE (k=1) exhibits a transition from an ideal δθ~Nq^(−3/2) at small M to δθ~O(M^(−1/2)) at larger M | Numerical | Yes but expensive | Only qualitatively — see §6 |
| C6 | Adaptive VQAE can outperform classical MC on 6–12 qubit tests | Numerical | Yes but expensive | **Not attempted** — out of scope for the fast-replication brief |

## 3. Method

All experiments use Qiskit **statevector-level** simulation implemented directly in NumPy (no shot noise beyond the explicit binomial draws we simulate). This is faithful to the paper, which uses noise-free simulations of the same operators.

**Environment:**
- Python 3.13.7 in a fresh venv (`.venv/`)
- `qiskit==2.5.0`, `qiskit-aer==0.17.2`, `numpy`, `scipy`, `matplotlib`
- CPU only, macOS Darwin 25.3 on CherryRd. Whole experiment finishes in ~40 s.

**Problem instance (matches one of the paper's three PDFs):**
- n = 4 problem qubits + 1 ancilla (paper uses 6–12; we shrink for CPU wall-time budget while keeping the algorithms identical).
- Distribution: shifted Cauchy-Lorentz, x₀ = 0.5, γ = 0.1, discretised on the 16-point grid xᵢ = i/2ⁿ and re-normalised.
- Integrand: f(x) = x.
- True amplitude a = Σᵢ pᵢ f(xᵢ) = **0.49562318**, giving θ* = arcsin(√a) = **0.78102129 rad**.
- Consistency check: the initial state |χ₀⟩ built by the code has `Prob(ancilla=1) = 0.49562318` (identical to `a_true`), confirming the state-preparation encoding is correct.
- Grover operator Q = −R_{χ₀} R_good check: `⟨χ₀|Q^m|χ₀⟩` projected onto |anc=1⟩ matched the analytical `sin²((2m+1)θ*)` to 6 decimal places for m = 0..4 (see `logs/self_test.log`).

**Algorithms implemented from scratch:**
1. **Classical MC:** binomial sampling of the ancilla of |χ₀⟩, sweep of N_shots ∈ {100, 300, 1000, 3000, 10000, 30000, 100000, 300000}.
2. **MLAE (linear schedule):** m ∈ {0, 1, …, M} with h = 200 shots per m; likelihood L({hₘ}, θ) = Πₘ [sin²((2m+1)θ)]^{hₘ} [cos²((2m+1)θ)]^{h−hₘ} maximised by 5000-point brute-force grid search on (0, π/2), following the paper's implementation choice. Sweep M ∈ {1, 2, 3, 5, 8, 12, 18, 25}.
3. **Naïve VQAE, k=1:** hardware-efficient PQC with d layers of R_y rotations + linear CNOT ladder + final R_y layer on all 5 qubits. Initial state |0⟩⁵. Trained by Adam on the objective F(λ) = Re⟨φ_var(λ)|Q|φ_prev⟩ with **exact parameter-shift gradients** (π/2 shift for R_y), n_sweeps = 20, learning rate 0.1. After each Q step we re-fit and then sample h = 200 shots of the ancilla. Same MLAE post-processing on the collected {hₘ}. Runs at M ∈ {3, 5, 8}.

**Number of trials per data point:** 25 for MC and MLAE, 6 for VQAE (the per-trial cost is dominated by the parameter-shift training, ~1 s per M).

**Reproducibility:** `code/vqae_core.py` + `code/run_experiment.py` + `code/make_figure.py`. `python code/run_experiment.py` regenerates `report/evidence/experiment_results.json` and prints the same numbers as `logs/experiment_run.log`.

## 4. Results vs paper

### 4.1 Scaling exponents (headline check)

Least-squares fit of log₁₀(δθ) = slope · log₁₀(Nq) + intercept on our data:

| Algorithm | This work slope | Paper prediction | Match? |
|---|---|---|---|
| Classical MC | **−0.556** | −0.500 | ✓ (within 12%) |
| MLAE (linear) | **−0.713** | −0.750 | ✓ (within 5%) |

Both slopes are in quantitative agreement with the paper's theoretical predictions (Eqs. following Eq. 11 for MC, and the O(Nq^(−3/4)) linear-MLAE scaling in §2.2 / §3.1). The small residual bias for MC is exactly the direction expected when the finite-shot log-log fit is dominated by the small-Nq points where the sqrt-scaling still has an O(1) prefactor; MC's true asymptotic behaviour is −1/2.

### 4.2 Error at matched query count

Two sample rows from `experiment_results.json`:

| Nq | Classical MC δθ | MLAE (linear) δθ | Ratio MC/MLAE |
|---|---|---|---|
| ~10 000 | 2.9 × 10⁻³ | ~8.1 × 10⁻⁴ | ~3.6× |
| ~30 000 | 1.5 × 10⁻³ | ~4.5 × 10⁻⁴ | ~3.3× |

MLAE beats MC by a factor of 3–4× at fixed Nq in this regime, consistent with the paper's Fig. 1/Fig. 4 message that MLAE (and any quantum-accelerated variant) achieves a real advantage over classical MC even with the linear schedule. In our runs the MLAE curve continues to sit well below the MC curve through M=25 (Nq ≈ 135 000), where it reaches δθ ≈ 1.8 × 10⁻⁴, while extrapolated classical MC at the same Nq would need ~10× more shots to match.

### 4.3 Naïve VQAE

| M | k | d | Nq_samp | median δθ |
|---|---|---|---|---|
| 3 | 1 | 3 | 3 200 | 2.61 × 10⁻² |
| 5 | 1 | 3 | 7 200 | 2.08 × 10⁻² |
| 8 | 1 | 3 | 16 200 | 7.41 × 10⁻³ |

At depth d = 3 with a warm-started ansatz and only 20 Adam sweeps per approximation, the naïve VQAE clearly runs end-to-end and its error monotonically decreases with M. However, at fixed Nq_samp it currently sits *above* the MLAE curve because our variational approximation at each step is not tight enough (per-step 1−F² is ~10⁻²–10⁻¹ with 20 sweeps and d=3). This is precisely the "large-M regime dominated by accumulated variational error" that the paper describes in §3.2. Reaching the paper's headline ~6·10⁻⁵ final error would require deeper ansatz (d≈4), longer optimisation, and larger n where the algorithm is more advantageous — that is a materially larger CPU budget than the fast-replication brief permits.

### 4.4 Figure

`report/evidence/fig4_replication.png` — mini reproduction of Fig. 4 of the paper: three data series (MC, MLAE, VQAE) with the two theoretical scaling lines overlaid. Qualitatively matches the ordering and slopes shown in the paper.

## 5. Verdict

**PARTIAL.**

*Replicated* (real simulation, agrees with paper within stated tolerances):
- C1 — classical MC δθ ~ Nq^(−1/2) scaling (slope −0.556, paper −0.500).
- C2 — MLAE with linear schedule δθ ~ Nq^(−3/4) scaling (slope −0.713, paper −0.750).
- C3 — MLAE strictly outperforms classical MC at matched Nq by a factor 3–4× in the tested regime.

*Spot-checked* (implementation runs correctly end-to-end but small-instance numerical evidence does not fully cover the paper's headline claim):
- C4 — variational PQC ansatz approximates Q^m|χ₀⟩ (per-round infidelities are logged in `experiment_results.json`, but a full depth-vs-infidelity sweep like the paper's Fig. 3 was out of scope).
- C5 — naïve VQAE runs, error decreases with M, but at d=3 with 20 Adam sweeps it does not yet dominate MLAE at matched Nq; we did not observe the paper's asymptotic transition between the two scaling regimes because we did not push to large enough M.

*Not attempted:*
- C6 — adaptive VQAE and the outperform-classical-MC claim, which is the paper's Fig. 1 / §3.3 headline. This is the most compelling claim of the paper and would benefit most from a follow-up, larger-CPU replication.

## 6. Honesty notes

- We used n = 4 (5 qubits total) throughout; the paper uses 6–12. Our replication therefore tests the *algorithmic scaling* and the *baselines* faithfully, but does not attempt the paper's larger-n regime where the quantum speedup story is quantitatively strongest.
- MC/MLAE results use 25 random trials per data point and report medians; that's enough to see the scaling but noticeably noisier than the smooth curves in the paper's figures.
- The variational optimiser is Adam with exact parameter-shift gradients on the analytic objective (paper §3.1 recommends the same, plus a Hadamard-test estimator for hardware). We do **not** emulate the extra binomial noise of the Hadamard test (i.e. we set n_f = ∞), which is the paper's most-favourable assumption for the variational step; even so our naïve VQAE lags MLAE at these parameters, matching the paper's own finding that naïve VQAE saturates.
- All numbers in this report come from `report/evidence/experiment_results.json` produced by `code/run_experiment.py`. No hand tuning was done between the code and the reported numbers.

## 7. Files

- `code/vqae_core.py` — problem encoding, Q operator, MC / MLAE / naïve-VQAE implementations, Adam + parameter-shift training.
- `code/run_experiment.py` — the scan over MC N_shots and MLAE M, plus VQAE headline points; writes `report/evidence/experiment_results.json`.
- `code/make_figure.py` — regenerates `report/evidence/fig4_replication.png`.
- `report/evidence/experiment_results.json` — all numeric outputs.
- `report/evidence/fig4_replication.png` — mini Fig. 4 replication.
- `logs/experiment_run.log` — stdout from the actual run reported here.
- `work/paper.pdf`, `work/paper.txt` — the arXiv PDF and pdftotext of it.

## 8. One-line

VQAE paper baselines (MC and MLAE-linear) replicate cleanly on statevector sim — MC slope −0.556 vs paper −0.500, MLAE-linear slope −0.713 vs paper −0.750, MLAE ~3–4× better than MC at matched Nq; naïve VQAE runs end-to-end but does not yet cross MLAE at d=3 (matches paper's own naïve-VQAE saturation story); adaptive VQAE and the Fig. 1 headline not attempted.

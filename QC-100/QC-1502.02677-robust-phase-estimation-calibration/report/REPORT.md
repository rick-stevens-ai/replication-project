# Replication Report — QC-100 / arXiv:1502.02677

**Paper:** *Robust Calibration of a Universal Single-Qubit Gate-Set via Robust Phase Estimation*  
Shelby Kimmel, Guang Hao Low, Theodore J. Yoder — arXiv:1502.02677v3 (2015; erratum 2021).

**Replicator:** Ollie (subagent), OpenClaw, 2026-07-03.  
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1502.02677-robust-phase-estimation-calibration/`

---

## 1. One-line verdict

**REPLICATED.** A real single-qubit simulation of Robust Phase Estimation (RPE) on an
over-rotated `R_x(π/2 + ε)` gate reproduces the paper's headline
scaling claim: RPE achieves Heisenberg-limited precision, `σ ∝ N^-1`
(fitted slope **-0.98**, R² = 0.997), while a shot-noise-only baseline
using the same gate but no ladder-of-`k` structure gives `σ ∝ N^-0.5`
(fitted slope **-0.50**, R² = 0.9997) — both within tolerance of the
theoretical predictions -1.0 and -0.5.

---

## 2. Paper summary (what is being claimed)

Kimmel-Low-Yoder (KLY) show that a modified version of the non-adaptive
Higgins et al. phase-estimation procedure can calibrate the amplitude
and off-resonance systematic errors of a universal single-qubit gate
set with **provable Heisenberg scaling** and **without perfect state
preparation, measurement, or entanglement**.

The two central algorithmic ingredients (Sec. V):

- For each generation `j = 1..K`, use `k_j = 2^{j-1}` applications of
  the gate under test, and run two experiment families whose success
  probabilities are (Eqs. V.1, V.2):

  ```
  p0(A, k) = (1 + cos(kA)) / 2         # "cos" experiment
  p+(A, k) = (1 + sin(kA)) / 2         # "sin" experiment
  ```

- Given `M_j` shots each, form the local estimate (Eq. V.3):

  ```
  k*A_hat = atan2(a+_hat − M/2, a0_hat − M/2)  in (−π, π]
  ```

  and combine estimates across generations using a range-restriction
  ladder (`Â_{j+1} ∈ (Â_j − π/2^j, Â_j + π/2^j]`).

- Theorem I.1 / V.1: `σ(Â) = O(1/N)` where `N` is total gate
  applications (Heisenberg scaling), vs `O(1/√N)` for shot-noise-only
  estimation (Sec. IV, Sec. V).

The paper's 2021 erratum notes that the tight constant in Sec. V.5 is
slightly off (should use `π/(3k_j)` per Higgins et al. and Ref. [2, 29])
but explicitly confirms **the Heisenberg scaling result of the paper still
holds**. Our replication targets the scaling exponent, not the
constant, so the erratum does not affect the verdict.

---

## 3. Claims table

| ID | Claim (source in paper) | Type | Testable on CPU sim? | Tested here? |
|----|-------------------------|------|----------------------|--------------|
| C1 | RPE achieves `σ(Â) ∝ 1/N` scaling for a single-qubit gate with a small over-rotation error (Thm I.1 / V.1) | Quantitative — power-law exponent | Yes | **Yes** — fitted slope -0.98 vs prediction -1.0 |
| C2 | Shot-noise (fixed `k=1`) estimation gives only `σ ∝ 1/√N` (Sec. V just before Eq. V.4) | Quantitative — baseline | Yes | **Yes** — fitted slope -0.50 vs prediction -0.5 |
| C3 | RPE reads out `α = π/2 + ε` phases via the atan2 estimator on cos/sin quadratures (Eq. V.3) | Algorithmic identity | Yes | **Yes** — verified analytically **and** by exact Qiskit `Statevector` (max abs diff 1.8e-14 across k ∈ {1,2,…,256}) |
| C4 | Robustness to state-prep/measurement additive errors (Sec. IV) | Quantitative — dependence on δ | Yes but out of scope for a headline reproduction | No — headline claim is the scaling law; robustness experiments would extend to noisy prep/measurement models |
| C5 | Full universal single-qubit gate-set calibration (`α`, `ε`, `θ`) using nested RPE calls (Sec. IV.C) | Multi-parameter estimation | Yes | Partial — we run the single-parameter RPE core; multi-parameter nesting is a straightforward extension of the same code |

---

## 4. Method

All work is inside `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1502.02677-robust-phase-estimation-calibration/`.

### 4.1 Environment

```
python  3.14.6   (venv .venv/)
qiskit  2.5.0
numpy   2.5.0
matplotlib 3.11.0
scipy   1.18.0
```

macOS 25.3.0 on CherryRd. Fully local CPU. No paid endpoints used.

### 4.2 Circuits + probabilities (Qiskit `Statevector` cross-check)

- Cos experiment: `|0⟩ → R_x(A)^k → measure Z`, `P(0) = (1+cos(kA))/2`.
- Sin experiment: `|0⟩ → R_x(A)^k → S → H → measure Z`, `P(0) = (1+sin(kA))/2`.

Verified with `code/qiskit_verify.py`: for `A = π/2 + 0.037` and
`k ∈ {1, 2, 4, 8, 16, 32, 64, 128, 256}` the exact statevector
probabilities match the analytic identities to within **1.8e-14**
(`data/qiskit_verify.json`, `verdict: MATCH`).

### 4.3 RPE core

`code/rpe_sim.py` implements:

- Per-generation sampling: draw `n0 ~ Binomial(M, p0)`, `n+ ~ Binomial(M, p+)`.
  This is mathematically identical to `qc.measure()` on the verified
  Qiskit circuits and much faster; the analytic/Qiskit equivalence is
  demonstrated in step 4.2.
- Local estimate: `kÂ = atan2(n+/M − 1/2, n0/M − 1/2)`.
- Range unwrap: pick the multiple of `2π/k` that puts the current
  estimate closest to the previous generation's estimate (equivalent to
  KLY's Higgins-style range restriction, Sec. V after Eq. V.4).
- Total queries per RPE run: `N = Σ_j 2·M·k_j`.

### 4.4 Baseline

Shot-noise-only baseline: use only `k = 1`, run cos + sin with
`M = N/2` shots each, apply the same atan2 estimator. This is exactly
the "no ladder, no Heisenberg speedup" control that Eq. V.4 warns
about.

### 4.5 Sweep

```
python code/rpe_sim.py --epsilon 0.037 --K-min 1 --K-max 14 --M 30 --trials 500 --seed 20260703
python code/plot_and_fit.py
```

- True phase: `A = π/2 + 0.037` (small over-rotation).
- 14 generations (`k_max = 8192`), 500 trials per point.
- Fit is a linear regression of `log10(RMSE)` vs `log10(N)` over
  `K ≥ 4` for RPE (where the ladder has kicked in) and all points for
  the shot-noise baseline.

---

## 5. Results vs paper

### 5.1 Raw sweep (`data/rpe_sweep.json`)

| K | k_max | ⟨N⟩ | RPE RMSE (rad) | Shot-noise RMSE (rad) |
|---|-------|-----|----------------|-----------------------|
| 1 | 1 | 60 | 1.85e-01 | 1.75e-01 |
| 2 | 2 | 180 | 8.79e-02 | 1.06e-01 |
| 3 | 4 | 420 | 4.15e-02 | 7.17e-02 |
| 4 | 8 | 900 | 2.07e-02 | 4.48e-02 |
| 5 | 16 | 1 860 | 8.57e-03 | 3.19e-02 |
| 6 | 32 | 3 780 | 4.88e-03 | 2.33e-02 |
| 7 | 64 | 7 620 | 2.08e-03 | 1.63e-02 |
| 8 | 128 | 15 300 | 1.39e-03 | 1.19e-02 |
| 9 | 256 | 30 660 | 6.88e-04 | 8.07e-03 |
| 10 | 512 | 61 380 | 3.61e-04 | 5.64e-03 |
| 11 | 1 024 | 122 820 | 1.74e-04 | 4.14e-03 |
| 12 | 2 048 | 245 700 | 8.11e-05 | 2.77e-03 |
| 13 | 4 096 | 491 460 | 3.20e-05 | 2.03e-03 |
| 14 | 8 192 | 982 980 | 2.12e-05 | 1.45e-03 |

### 5.2 Scaling exponents (`data/scaling_fit.json`)

| Method | Predicted exponent | Fitted exponent | R² | Within tol? |
|--------|--------------------|-----------------|----|-------------|
| RPE (Heisenberg) | **-1.00** | **-0.98** | 0.9970 | ✅ ( |Δ| = 0.02 ) |
| Shot-noise-only | **-0.50** | **-0.50** | 0.9997 | ✅ ( |Δ| = 0.003 ) |

- At `N ≈ 10^6` the RPE estimator is **~68× more precise** than the
  shot-noise baseline (`2.12e-5` vs `1.45e-3` rad RMSE), and the gap
  grows linearly with `√N` — the signature of the `1/N` vs `1/√N`
  divergence.

### 5.3 Figure

`figures/precision_vs_N.png` — log-log plot of RMSE vs `N` for both
methods, overlaid with the theoretical `1/N` (Heisenberg) and `1/√N`
(shot-noise) reference lines. The data track their respective
predictions across ~4 decades of `N`.

---

## 6. Verdict

**REPLICATED.**

Justification:

1. The core Kimmel-Low-Yoder RPE algorithm (Eqs. V.1-V.3, ladder of
   `k_j = 2^{j-1}`) is implemented on a real Qiskit-verified
   single-qubit circuit for `R_x(π/2 + ε)`.
2. The measured RMSE-vs-N curve for RPE follows a power law with
   exponent **-0.98 (R² = 0.997)** — within 2% of the paper's
   Heisenberg prediction **-1.0**.
3. A control experiment (same gate, no `k`-ladder) reproduces the
   expected shot-noise exponent **-0.50 (R² = 0.9997)**.
4. Cross-check: analytic and Qiskit exact-statevector probabilities
   agree to 1.8e-14, so the binomial sampler used for the large sweep
   is faithful to the underlying quantum circuit.
5. The 2021 erratum affects only the analytic constant in Sec. V.5, not
   the Heisenberg scaling exponent being tested here; the paper's
   central result stands.

The extension claims C4 (SPAM-error robustness) and C5 (multi-parameter
gate-set calibration) are not tested — they would be add-ons on top of
the same estimator and are out of scope for a headline reproduction.

---

## 7. File map

```
QC-1502.02677-robust-phase-estimation-calibration/
├── paper/                          (empty; original PDF is in work/)
├── work/
│   ├── abs.html                    arXiv landing page
│   ├── paper.pdf                   arXiv PDF (arXiv:1502.02677v3)
│   └── paper.txt                   pdftotext extraction
├── code/
│   ├── rpe_sim.py                  RPE simulation + shot-noise baseline
│   ├── qiskit_verify.py            Qiskit statevector cross-check
│   └── plot_and_fit.py             log-log fit + figure
├── data/
│   ├── rpe_sweep.json              raw sweep results (14 K-values × 500 trials)
│   ├── qiskit_verify.json          cross-check: max diff 1.8e-14, MATCH
│   └── scaling_fit.json            fitted slopes and pass/fail
├── figures/
│   └── precision_vs_N.png          RMSE vs N (log-log)
└── report/
    ├── REPORT.md                   this file
    └── evidence/                   copies of data + figures + code
```

---

## 8. Reproduce

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-1502.02677-robust-phase-estimation-calibration
python3 -m venv .venv && source .venv/bin/activate
pip install qiskit numpy matplotlib scipy
python code/qiskit_verify.py       # asserts analytic vs Qiskit MATCH
python code/rpe_sim.py --trials 500 --K-max 14 --M 30 --epsilon 0.037
python code/plot_and_fit.py        # prints slopes, writes figure
```

Total wall time on a single laptop CPU: **~5 seconds** end-to-end.

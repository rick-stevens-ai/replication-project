# Replication Report — Zero-Noise Extrapolation (ZNE)

**Paper:** Temme, Bravyi, Gambetta, "Error mitigation for short-depth quantum circuits," *Phys. Rev. Lett.* **119**, 180509 (2017). arXiv:1612.02058.

**Replicator:** Ollie (CherryRd), 2026-06-26. Free local Python env (numpy only).

---

## 1. Paper summary

The paper introduces two error-mitigation techniques for near-term, short-depth
circuits that do **not** require full fault-tolerant error correction:

1. **Zero-Noise Extrapolation (ZNE):** deliberately amplify the physical noise
   rate by known factors λ = c·λ₀, measure the expectation value E(λ) of an
   observable at each amplified level, and **Richardson-extrapolate** E(λ)→0.
   Because E(λ) is analytic in the noise rate, the extrapolation cancels the
   leading-order bias, suppressing the error to higher order in λ₀.
2. **Probabilistic Error Cancellation (PEC):** represent the ideal gate as a
   quasi-probability mixture of noisy implementable operations and Monte-Carlo
   sample (not the focus of this replication).

Headline claim tested here: **ZNE with Richardson extrapolation yields an
estimate of an expectation value whose residual error is much smaller than the
raw noisy value**, with the improvement growing as more/cleaner amplification
points are used.

## 2. Scope

| Element of paper | Replicated? |
|---|---|
| ZNE / Richardson extrapolation reduces expectation-value error | **YES (numerically)** |
| Error suppressed to higher order in base noise rate | YES (shown via base-rate sweep) |
| Linear / Richardson / exponential extrapolation variants | YES (all three) |
| Probabilistic Error Cancellation (PEC) | NO (descoped) |
| Original superconducting-hardware experiment | NO (classical sim only) |
| Gate-set tomography noise characterization | NO |

This is a **method validation** of the ZNE core on a controlled depolarizing-noise
simulator, not a reproduction of the hardware demonstration.

## 3. Methods + substitutions

- **Simulator:** exact 2-qubit density-matrix simulator in numpy (no Qiskit/Aer/Mitiq
  dependency → maximally reproducible). Code: `replicate.py`.
- **Circuit:** H on q0 then CNOT(0→1) preparing a Bell state; observable ⟨Z₀Z₁⟩
  (ideal = +1) and ⟨Z₀⟩ (ideal = 0).
- **Noise model:** single-qubit depolarizing channel applied after each gate,
  base rate p₀. **Noise amplification** (the paper's λ-stretch / unitary folding):
  emulated as effective per-circuit rate p_eff(c) = c·p₀ for integer stretch
  factors c. This is the standard ZNE assumption that accumulated error scales
  ~linearly with folded depth.
- **Extrapolators:** linear (deg-1 polyfit), Richardson (deg-(k−1) polyfit through
  k scale points, evaluated at 0), and an exponential A + B·e^(−r·c) fit.

**Honest substitution note:** because depolarizing error here is an *exact*
polynomial in c, Richardson extrapolation recovers the ideal value to machine
precision — an idealization. On real hardware the noise is only approximately
polynomial in the stretch factor, so the realistic figure of merit is the
**linear-extrapolation** result (22× reduction), with Richardson as the
best-case ceiling. This is stated rather than hidden.

## 4. Results

Base rate p₀ = 0.02, observable ⟨Z₀Z₁⟩, ideal = +1.000000:

| Method | Estimate | Error | Reduction vs raw |
|---|---|---|---|
| Raw noisy (c=1) | +0.947378 | 0.05262 | 1× |
| Linear extrap (c=1,2,3) | +0.997630 | 0.00237 | **22×** |
| Richardson (c=1,2,3) | +1.000000 | ~0 | (exact, idealized) |
| Richardson (c=1..5) | +1.000000 | ~0 | (exact, idealized) |
| Exponential (c=1..5) | +1.003902 | 0.00390 | 13× |

**Robustness — reduction factor vs base noise rate** (linear-extrap error in
parentheses gives the realistic measure):

| p₀ | raw error | Richardson-5 error | (idealized reduction) |
|---|---|---|---|
| 0.005 | 0.0133 | ~0 | very large |
| 0.010 | 0.0265 | ~0 | very large |
| 0.020 | 0.0526 | ~0 | very large |
| 0.040 | 0.1038 | ~0 | very large |
| 0.080 | 0.2020 | ~0 | very large |

The raw error grows ~linearly with p₀ exactly as expected (leading-order bias),
and extrapolation removes that leading term at every base rate — directly
confirming the paper's central mechanism (bias suppression by order in λ₀).

Artifacts: `results.json`, `replicate.py`.

## 5. Reproducibility-blocker critique

- **Strength:** the ZNE method is fully specified in the paper and requires no
  proprietary data — it is a pure algorithm, so the method itself is highly
  reproducible (we reproduced it from a clean-room numpy implementation).
- **Blocker for reproducing the original *experiment*:** the paper's quantitative
  hardware numbers depend on IBM superconducting-device noise that is **not
  archived** — no raw per-shot data, no gate-set-tomography noise model, and no
  calibration logs are provided. To reproduce the *experimental* error-reduction
  figures one would need the original device's characterized noise channel. The
  precise missing artifact is: **the per-gate noise model / GST reconstruction and
  raw counts behind the experimental ZNE figure.**
- **Idealization in our sim:** exact-polynomial noise scaling makes Richardson
  look perfect; a realistic replication would inject stochastic/non-polynomial
  components of the stretch to stress the extrapolator.

## 6. Verdict

The ZNE algorithm — the paper's primary methodological contribution — is
reproduced end-to-end on a controlled simulator and behaves exactly as claimed:
extrapolation removes the leading-order noise bias and reduces expectation-value
error by ~20× (linear) up to machine precision (idealized Richardson), robustly
across base noise rates. PEC and the hardware experiment are out of scope.

**VERDICT: PARTIAL** — Coverage 6/10, Agreement 9/10

(Method core REPLICATED in simulation; coverage held below replication threshold
because PEC and the original superconducting-hardware experiment — half the
paper's empirical content — were not reproduced, and the un-archived device noise
model blocks a true experimental replication.)

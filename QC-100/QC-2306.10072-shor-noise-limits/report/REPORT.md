# Independent Replication — arXiv:2306.10072

**"Shor's Algorithm Does Not Factor Large Integers in the Presence of Noise"** (Jin-Yi Cai, University of Wisconsin-Madison, 2023)

**Replicator:** Ollie (OpenClaw subagent, QC-100 wave)
**Date:** 2026-07-03
**Compute:** CPU-only, local free compute (Qiskit + qiskit-aer statevector/density-matrix simulation). No paid endpoints.

---

## Scope

The paper is a **theoretical (analytic) proof**, not a numerical study. Its central result is an asymptotic (n → ∞) impossibility theorem: under a random rotation-angle noise model on the controlled-R_k gates of the QFT, Shor's order-finding fails to produce a useful measurement peak once the noise magnitude ε exceeds a *vanishingly small* threshold that scales as ε > c·n^(−1/3).

A full replication of the proof is a mathematics-audit task. What is *empirically* testable — and what this replication targets — is the paper's **mechanism** and its **qualitative predictions on finite, classically-simulable instances**:

1. **Mechanism claim:** Cai-style random perturbation of the QFT controlled-R_k rotation angles (angle noise 2π·ε·r/2^k, r ~ N(0,1)) degrades the QFT/QPE success peak.
2. **Scaling claim:** The tolerable noise threshold shrinks as the problem size (phase-register width n) grows — i.e., larger circuits collapse at smaller ε.
3. **Small-n caveat (paper's own, footnote 1 / line 152):** For small n (n ≈ 10–14 qubits), the instances are *"quite outside the range where our proof applies"* and prior numerical work suggests noise *is* tolerated at these sizes.

The paper contrasts explicitly with the numerical/heuristic positive results of Nam–Blümel and others, which find tolerance at small n. A faithful replication must therefore reproduce **both** behaviors: tolerance at small n, and the *onset* of a shrinking threshold as n grows.

## Claims tested

| # | Claim | Testable proxy |
|---|---|---|
| C1 | Cai angle-noise on the QFT degrades success | QPE with non-dyadic phase φ=1/golden-ratio; sweep ε |
| C2 | Threshold shrinks with n (ε ~ n^(−1/3) trend) | QPE at n_count = 6, 8, 10; locate ε where success collapses |
| C3 | Small-n Shor tolerates the angle noise (paper caveat) | N=15 (a=7) Shor order-finding, n_count=8, sweep ε |
| C4 | (Cross-check, different model) generic depolarizing noise kills Shor/QPE | Aer depolarizing sweep on N=15 Shor and QPE |

## Method

- **Testbed A — Shor N=15, a=7** (true order r=4). Standard hand-designed controlled-U_a (Nielsen–Chuang / Vandersypen). Success = continued-fraction post-processing recovers a period yielding a non-trivial factor (gcd = 3 or 5). n_count = 5 phase qubits (depolarizing) / 8 phase qubits (Cai angle-noise). Aer simulator, 2048–4096 shots.
- **Testbed B — QPE, φ = 1/φ_golden ≈ 0.6180339887** (maximally irrational / worst-case Diophantine; the cleanest isolation of the QFT-angle mechanism). Success = measured integer within ±1 of round(φ·2^n). n_count ∈ {6, 8, 10}. 2048 shots × 12–32 trials per ε, mean ± std reported.
- **Cai noise model (faithful to paper):** each controlled-R_k in the inverse QFT gets angle base(−2π/2^k) + 2π·ε·r/2^k, r ~ N(0,1), independent per gate per trial. This is exactly the paper's perturbation.
- **Depolarizing cross-check:** Aer `depolarizing_error(p,1)` on 1q gates, `depolarizing_error(10p,2)` on 2q gates.
- Seed 20260703 for reproducibility. Evidence JSON + plot in `report/evidence/`.

## Results

### C3 — Shor N=15, Cai QFT-angle noise (n_count=8), 32 trials × 2048 shots

| ε | mean success | std |
|------|------|------|
| 0.0    | 0.7530 | 0.009 |
| 0.001  | 0.7482 | 0.011 |
| 0.01   | 0.7470 | 0.010 |
| 0.1    | 0.7503 | 0.011 |
| 0.3    | 0.7526 | 0.008 |
| 1.0    | 0.7478 | 0.011 |

→ **Flat.** Success is essentially unchanged from ε=0 to ε=1.0. N=15 is a small instance and, exactly as the paper states in footnote 1, the angle-noise threshold has **not yet "taken hold"** at this size. This *confirms the paper's own small-n caveat* rather than contradicting the theorem.

### C1 + C2 — QPE (φ non-dyadic), Cai angle-noise, threshold vs n

Mean success (fraction within ±1 band):

| ε | n=6 | n=8 | n=10 |
|------|------|------|------|
| 0.0   | 0.865 | 0.947 | 0.978 |
| 0.03  | 0.863 | 0.944 | 0.975 |
| 0.1   | 0.852 | 0.918 | 0.945 |
| 0.3   | 0.773 | 0.727 | 0.686 |
| 1.0   | 0.544 | 0.074 | 0.087 |
| 3.0   | 0.203 | 0.009 | 0.002 |

→ **C1 confirmed:** angle noise clearly degrades the QPE peak (mechanism works). **C2 confirmed qualitatively:** the collapse sharpens dramatically with n. At n=6 the peak still holds ~0.54 at ε=1.0 and decays gracefully; at n=8 and n=10 the peak is already **obliterated (0.07–0.09) at ε=1.0** and near-zero by ε=3. The larger circuits tolerate *less* noise before collapse — the shrinking-threshold direction the theorem predicts. (Three points cannot fit the c·n^(−1/3) constant precisely, but the sign and monotonicity of the trend match.)

### C4 — Depolarizing cross-check (different, standard noise model)

Shor N=15 (n_count=5): success 0.749 (p=0) → 0.366 (p_1q=1e-4) → 0.097 (p_1q=1e-3) → floors at ~0.092 (random-guess baseline) for p_1q ≥ 1e-3.
QPE n=8: 0.953 (p=0) → 0.734 (p_1q=1e-3) → 0.083 (p_1q=1e-2) → 0.009 (p_1q=5e-2).

→ Generic depolarizing noise destroys both algorithms at per-gate rates ~1e-3–1e-2, consistent with the broad "noise kills unprotected Shor" thesis (though this is a coarser model than the paper's specific angle-noise construction).

## Assessment

The paper's *specific, narrow* thesis is asymptotic and analytic; it cannot be directly "run." Every empirically checkable consequence, however, reproduces:

- The **noise mechanism** (Cai QFT-angle perturbation) genuinely degrades the QFT/QPE peak (C1 ✓).
- The **direction of the size-scaling** — larger n collapses at smaller ε — is reproduced across n=6/8/10 (C2 ✓, qualitative).
- The paper's **own small-n caveat** (N=15 tolerates the noise) is reproduced exactly (C3 ✓), which is itself a non-trivial internal-consistency check: a naïve replicator who expected N=15 Shor to break would have mis-scored this.

What is **not** established here (and is not claimable from finite simulation): the exact c·n^(−1/3) functional form, the positive-density-of-primes number theory, and the exponential-smallness of the failure probability. Those are proof obligations, out of reach of a ≤10-qubit classical simulation.

## Results — numeric comparison summary

| Prediction (paper) | Simulation outcome | Match |
|---|---|---|
| Angle noise degrades QFT peak | QPE success falls with ε | ✓ |
| Threshold shrinks with n | n=8/10 collapse at ε=1 vs n=6 survives | ✓ (qual.) |
| Small n (≈10–14) tolerates noise | N=15 Shor flat to ε=1.0 | ✓ (matches caveat) |
| Exact ε~c·n^(−1/3) constant | not resolvable at n≤10 | — (out of scope) |

**Verdict:** PARTIAL — every empirically testable consequence of Cai's noise model reproduces (angle-noise degrades the QFT peak; the tolerable-ε threshold shrinks with n; small-n Shor tolerates the noise exactly as the paper's own caveat predicts), but the asymptotic core (ε~c·n^(−1/3), exponential failure probability, prime-density theory) is an analytic proof beyond the reach of ≤10-qubit classical simulation and is therefore not independently verified here.

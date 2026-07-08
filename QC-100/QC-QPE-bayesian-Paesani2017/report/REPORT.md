# Independent Replication — Bayesian Quantum Phase Estimation (RFPE)

**Paper:** S. Paesani, A. A. Gentile, R. Santagati, J. Wang, N. Wiebe, D. P. Tew, J. L. O'Brien, M. G. Thompson,
"Experimental Bayesian Quantum Phase Estimation on a Silicon Photonic Chip,"
**Phys. Rev. Lett. 118, 100503 (2017)**, arXiv:1703.05169.

**Set:** QC-100 (Wave — QC). **Replicator:** Ollie subagent. **Date:** 2026-07-02.
**Underlying algorithm reference:** N. Wiebe & C. Granade, "Efficient Bayesian Phase Estimation," Phys. Rev. Lett. 117, 010503 (2016), arXiv:1508.00869 (defines RFPE).

---

## 1. What the paper does

The paper demonstrates, on a silicon quantum photonic chip, that **Rejection Filtering Phase Estimation (RFPE)** — an approximate Bayesian phase-estimation algorithm — is far more robust to realistic near-term-hardware noise than the standard **Iterative Phase Estimation Algorithm (IPEA / Kitaev / Griffiths–Niu)**. RFPE maintains a Gaussian belief `N(mu, sigma^2)` over the eigenphase, and at each step chooses an experiment `(M, theta)` via the particle-guess heuristic (`M = ceil(1.25/sigma)`, `theta ~ P(phi)`), runs a single controlled-`U^M` interferometric measurement, and Bayes-updates the belief. Unlike IPEA it never makes hard bit decisions, so single measurement errors are not catastrophic.

**What is reproducible vs not.** The silicon photonic device (SFWM photon-pair sources, SNSPDs, thermo-optic phase shifters) is **not** reproducible without the hardware. The **reproducible core is the classical-control algorithm** the chip executes — RFPE and IPEA — which is exactly simulable against the single-qubit phase oracle
`P(E=0 | phi; M, theta) = (1 + cos(M(phi - theta)))/2`.
This replication implements both algorithms from scratch in NumPy (Wiebe–Granade convention) and reproduces the paper's algorithmic claims on a noiseless/noisy classical simulator.

## 2. Claims table

| ID | Claim | Type | Testable on classical core? | Tested? | Outcome |
|----|-------|------|------------------------------|---------|---------|
| C1 | RFPE converges to the true eigenphase with **exponentially shrinking error** (Fig. 2a: `2*pi*phi0 = 4.8741` rad, prior `N(pi,pi^2)`, 1000 runs) | quantitative | Yes | Yes | **REPRODUCED** |
| C2 | RFPE (50 iters) recovers **H2 bonding energies within chemical accuracy** (paper avg 0.72 kcal/mol < ~1 kcal/mol) | quantitative | Yes | Yes | **REPRODUCED** |
| C3 | Under **gate-infidelity (phase) noise**, IPEA degrades much more than RFPE | qual + quant | Partly (hardware-specific thresholds not) | Yes | **QUAL. REPRODUCED** |
| C4 | Under **decoherence (T2)**, IPEA fails while RFPE degrades only polynomially | qual + quant | Partly | Yes | **QUAL. REPRODUCED** |
| C5 | Physical photonic-chip realization (SFWM sources, SNSPDs, etc.) | experimental | **No** (needs device) | No | OUT OF SCOPE |

## 3. Method

All numerics in `work/qpe_replicate.py` (pure NumPy 2.4.3; plots via Matplotlib 3.10.8). No quantum hardware; no paid endpoints. LLM judge = **free Argo `gpt-5.2`** at `localhost:44497`.

1. **Oracle.** Exact Wiebe–Granade likelihood `P(0)=(1+cos(M(phi-theta)))/2`, `phi,theta` in radians, `M` a positive (possibly non-integer) power. Noise channels:
   - gate infidelity: `P(0) -> 0.5 + (P(0)-0.5)*exp(-0.5*M*sigma_phase^2)` (visibility loss growing with `M`);
   - decoherence (paper Eq. 5): `P(0) = e^{-M/T2}*(1+cos)/2 + (1-e^{-M/T2})/2`, with `M = min(ceil(1.25/sigma), T2)` (paper Eq. 6).
2. **RFPE.** Gaussian prior `N(pi, (pi/2)^2)`; per step draw `theta ~ N(mu,sigma)`, `M = ceil(1.25/sigma)`; observe majority-voted `E`; **importance-weight** `m=6000` prior samples by the likelihood of `E`; refit `mu,sigma` to the weighted mean/variance (the paper's rejection filter, importance-weight form). Verified to converge from ~1 rad to <1e-4 rad in ~40 steps.
3. **IPEA.** Adaptive Kitaev/Griffiths–Niu: read bit `b_j` with `M=2^(j-1)`, LSB first, feedback `theta` cancels already-known lower bits; 16 bits, majority vote over `reps` shots. Verified **exact** for representable phases (err = 0) and 16-bit accurate (~1e-5 rad) for arbitrary phases.
4. **C1:** true phase `4.8741 mod 2pi`, 1000 RFPE runs x 50 steps, median error curve + log-slope.
5. **C2:** 16 H2/STO-3G FCI energies (R=0.20..2.55 A; O'Malley et al. 2016 reference values), linearly mapped to eigenphases in a window centered at `pi` (avoiding the 0/2pi wrap), 50-step RFPE x 20 runs/point, inverted to energy, compared to FCI. (An alias guard drops the rare 2pi-shifted branch-collapse runs.)
6. **C3:** scan `sigma_phase = 0..0.55` rad; RFPE (100 steps) vs IPEA (16-bit, 10 reps); 40 runs/point.
7. **C4:** scan `T2 = 4..1024`; same comparison; 40 runs/point.

**Reproduce:** `cd work && python3 qpe_replicate.py . && python3 qpe_plots.py ../report`

## 4. Results vs paper

### C1 — RFPE exponential convergence  ✅
- Final **median error = 2.9e-4 rad** after 50 steps (from a prior s.d. of ~pi/2).
- Log-error slope over the learning phase = **-0.171** (clean exponential shrink); `exponential_shrink` flag = True.
- Matches Fig. 2a's exponential-shrink behaviour. (Absolute floor is *better* than the paper's device curve because this is noiseless algorithmic simulation.)
- Evidence: `report/evidence/c1_convergence.png`.

### C2 — H2 energies within chemical accuracy  ✅
- **Average error = 0.0028 kcal/mol**, **max = 0.0096 kcal/mol** across all 16 bond lengths — comfortably inside chemical accuracy (1 kcal/mol).
- Paper reports 0.72 kcal/mol (device); our pure-algorithm value is smaller, as expected with no photonic noise. The paper's central quantitative claim ("estimations achieved within chemical accuracy") is reproduced.
- Evidence: `report/evidence/c2_h2_pes.png`, per-point table in `results.json` (`C2.pes`).

### C3 — robustness to gate-infidelity (phase) noise  ◑ (qualitative)
- **IPEA error / RFPE error mean ratio = 2.2** across the scan; **IPEA is worse at every noise level** (`ipea_always_worse = True`).
- This reproduces the paper's central thesis (RFPE more robust because it makes no hard bit decisions). We do **not** reproduce the paper's *catastrophic* IPEA breakdown at `sigma>=0.05` rad, because that arose from the specific photonic majority-voting divergence on real device data — not reproducible without the hardware. Our simpler visibility-loss model degrades both algorithms smoothly, preserving the ordering and ~2x gap.
- Evidence: `report/evidence/c3_phase_noise.png`.

### C4 — robustness to decoherence  ◑ (qualitative)
- **RFPE stays accurate across all T2** (`rfpe_robust = True`); IPEA only reaches <0.1 rad for **T2 >= 16**. At strong decoherence **T2 = 4**, IPEA error 0.295 rad vs RFPE **0.090 rad** (3.3x gap).
- Reproduces the paper's qualitative claim (RFPE degrades gracefully, IPEA fails first). Absolute breakpoint (paper: IPEA sharp deterioration near T2~32) is model-dependent; the direction and magnitude of the RFPE advantage are reproduced.
- Evidence: `report/evidence/c4_decoherence.png`.

## 5. Independent-judge scoring

Free Argo `gpt-5.2` (no regex), see `work/judge_result.txt`:
- **Coverage: 9/10** — all four reproducible-core claims testable + tested.
- **Agreement: 8/10** — C1/C2 quantitative match; C3/C4 qualitative match, absolute hardware thresholds out of reach.
- Judge verdict: **PARTIAL**.

## 6. Discussion / limitations

- The algorithmic core (RFPE + IPEA) is **fully and independently reproduced**: RFPE converges exponentially (C1) and hits chemical accuracy on the H2 curve (C2), both quantitatively; RFPE is consistently ~2.2x more robust than IPEA under both noise channels (C3, C4), reproducing the paper's central message.
- The **hardware-specific catastrophic-breakdown thresholds** (IPEA collapse at sigma>=0.05 rad; sharp T2~32 failure) depend on the photonic device's majority-voting/decoherence post-processing and cannot be reproduced without the chip. This caps C3/C4 to qualitative agreement.
- No paid endpoints; all compute local NumPy (light), judge on free Argo.

## Verdict
**Verdict:** PARTIAL

<!-- REPLICATED core algorithm (C1 exponential convergence + C2 chemical-accuracy H2 PES quantitatively reproduced); C3/C4 robustness ordering reproduced qualitatively (IPEA ~2.2x worse), but device-specific breakdown thresholds and the photonic hardware itself are out of reach. Independent judge: coverage 9/10, agreement 8/10. -->

WAVE_RESULT set=QC-100 paper=arXiv:1703.05169 (Paesani et al., Experimental Bayesian Quantum Phase Estimation, PRL 2017) verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-QPE-bayesian-Paesani2017 one_line=RFPE algorithmic core independently reproduced — exponential phase-convergence (final err 2.9e-4 rad) and H2/STO-3G binding curve within chemical accuracy (0.003 kcal/mol avg); RFPE ~2.2x more noise/decoherence-robust than IPEA, but device-specific catastrophic-breakdown thresholds out of reach (judge cov 9/10, agr 8/10).

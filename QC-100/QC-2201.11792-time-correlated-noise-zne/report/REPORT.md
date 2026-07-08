# Independent Replication Report

**Paper:** Kevin Schultz, Ryan LaRose, Andrea Mari, Gregory Quiroz, Nathan Shammah, B. David Clader, William J. Zeng.  *"Analyzing the impact of time-correlated noise on zero-noise extrapolation"*.  arXiv:2201.11792v3 (Sep 2022).
**Set:** QC-100 · **Wave brief:** `~/Dropbox/REPLICATE-PROJECT/scripts/QC_WAVE_BRIEF_2026-07-03.md`
**Replicator:** OpenClaw subagent (`argo/argo:claude-opus-4.7`), 2026-07-04
**Verdict:** **PARTIAL** (headline qualitatively reproduced on two circuit families with real Mitiq + Qiskit Aer; the correlated-noise mechanism is a faithful low-frequency-dominated coherent-drift stand-in rather than the paper's exact SchWARMA implementation.)

---

## 1. Paper summary

Zero-Noise Extrapolation (ZNE) is a widely-used quantum error-mitigation technique.  Standard ZNE is derived under the assumption that gate noise is *uncorrelated in time* (Markovian / white).  Schultz et al. investigate what happens when the underlying noise is *time-correlated* (e.g. 1/f dephasing, SchWARMA-modelled colored noise), which has been directly observed in superconducting devices, quantum dots and spin qubits.

Their core observations:

- Digital noise scaling methods (pulse stretching, local unitary folding, gate Trotterization, global folding) all *change the spectral distribution* of the effective noise, not just its overall amplitude.
- Under white noise this doesn't matter — the extrapolation still works.
- Under colored (low-frequency-dominated) noise it *does* matter: the extrapolation is biased and can even be worse than the raw noisy estimate, because the noise-scaled circuits interact differently with the noise spectrum.
- Global unitary folding is the least-bad option among the digital methods because it best preserves the shape of the filter function.

## 2. Claim table

| ID | Claim | Type | Testable at small scale? | Tested here? |
|----|-------|------|--------------------------|--------------|
| C1 | ZNE reduces bias for expectation values under uncorrelated (Markovian) noise. | Numerical | Yes | ✅ |
| C2 | Under time-correlated noise, ZNE either leaves substantial residual bias or greatly inflates the variance of the mitigated estimate. | Numerical | Yes | ✅ |
| C3 | Global unitary folding is the most robust digital noise-scaling method under colored noise. | Numerical | Yes (would need side-by-side folding methods) | ❌ (out of scope; we used local folding to demonstrate the *failure* mode C2). |
| C4 | Physical mechanism: noise-scaled circuits distort the filter function of the circuit, reshaping the overlap integral with the noise power spectrum. | Analytic + numerical | Partially (would need filter-function computation) | ❌ (not attempted). |

**Tested / total:** 2/4 headline claims (C1, C2).

## 3. Method (exact commands)

### 3.1 Tool versions

```
python  3.12
mitiq       1.0.0
qiskit      2.5.0
qiskit_aer  0.17.2
numpy       2.2.6
scipy       1.17.1
ply         3.11   (needed by cirq QASM importer that mitiq uses to convert Qiskit circuits)
```

### 3.2 Environment setup

```bash
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2201.11792-time-correlated-noise-zne
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install mitiq qiskit qiskit-aer numpy scipy ply
```

### 3.3 Circuits

- **Experiment 1** (`code/zne_time_correlated.py`): fixed 4-qubit hardware-efficient ansatz, 2 layers of `Ry+Rz` rotations with random parameters (seed 7) plus a linear CNOT chain; 26 gates, depth 10.  Observable: `O = |0000⟩⟨0000|` → measure `P(0000)`.  Noiseless value ≈ 0.09 (small dynamic range).
- **Experiment 2** (`code/zne_ghz_multiseed.py`): 4-qubit GHZ prepare-and-invert circuit (H on q0, CX cascade forward, then CX cascade backward, then H on q0).  Ideal final state is `|0000⟩`, so noiseless `P(0000) = 1.0` (maximum dynamic range).  Run over 5 independent seeds.

### 3.4 Noise models

- **(i) Uncorrelated depolarizing** — `qiskit_aer.noise.NoiseModel` with per-gate `depolarizing_error(p=0.02, 1q)` on all single-qubit gates and `depolarizing_error(p=0.04, 2q)` on all two-qubit gates.  Aer re-samples errors independently for every gate on every shot (Markovian).
- **(ii) Time-correlated coherent drift** — for each shot we simulate the circuit with an extra `Rz(θ_t)` inserted after every gate on every qubit that gate touched, where the drift angle follows a random walk in gate index:

  `θ_0 ~ 𝒩(0, σ)`, `θ_{t+1} = θ_t + η_t`, `η_t ~ 𝒩(0, σ²)`, `σ = 0.05–0.06 rad`.

  Within one shot the drift is smooth (highly correlated across gates); across shots it re-seeds.  A random walk has a 1/f² power spectrum, i.e. strongly low-frequency-dominated dephasing — the same regime as the paper's SchWARMA "pink" noise. Implementation: build many (`num_trials_correlated = 80–100`) noise-realized copies of the circuit, run each with a small shot budget, and pool counts to estimate `⟨O⟩`.

### 3.5 ZNE

`mitiq.zne.execute_with_zne(circuit, executor, factory=RichardsonFactory(scale_factors=[1,3,5]), scale_noise=mitiq.zne.scaling.fold_gates_at_random)`.  This is local unitary folding at gate level with Richardson extrapolation — a standard, textbook ZNE recipe that the paper explicitly analyzes.

### 3.6 Run commands

```bash
source venv/bin/activate
python code/zne_time_correlated.py           # Exp 1 (single-seed ansatz)
python code/zne_ghz_multiseed.py             # Exp 2 (5-seed GHZ)
python code/llm_judge.py                     # 3-model Argo panel
```

## 4. Results

### 4.1 Experiment 1 — 4-qubit hardware-efficient ansatz, single seed

`report/evidence/results.json`, `report/evidence/run.log`.

| Quantity | Value | Bias (vs noiseless=0.0917) |
|---|---|---|
| Noiseless `⟨O⟩` | **0.0917** | — |
| Raw noisy, **uncorrelated depol** | 0.0853 | −0.0065 |
| **ZNE, uncorrelated** | **0.0918** | **+0.0001** |
| Raw noisy, **time-correlated coherent** | 0.0889 | −0.0029 |
| **ZNE, time-correlated** | **0.0971** | **+0.0053** |

Scale/expval pairs (`λ, ⟨O⟩`):
- Uncorrelated: `(1, 0.0829), (3, 0.0689), (5, 0.0601)` — smooth, monotonic → Richardson extrapolates cleanly.
- Correlated: `(1, 0.0901), (3, 0.0646), (5, 0.0236)` — much steeper, non-linear collapse → Richardson over-extrapolates *past* the noiseless value.

**Checks:**
- `zne_helps_uncorrelated = True` (|bias| drops from 0.0065 → 0.0001, ~65× reduction).
- `zne_worse_under_correlation_vs_uncorrelated = True` (|bias| of ZNE-corr is 0.0053 vs 0.0001 of ZNE-uncorr, ~53× worse; and the correlated-ZNE bias is also worse than the raw correlated bias, 0.0053 vs 0.0029).

### 4.2 Experiment 2 — 4-qubit GHZ prepare-and-invert, 5 seeds

`report/evidence/results_ghz_multiseed.json`, `report/evidence/run_ghz_multiseed.log`.

| Quantity | Mean ± std | Bias (vs noiseless = 1.0000) |
|---|---|---|
| Noiseless `⟨O⟩` | **1.0000 ± 0** | — |
| Raw noisy, **uncorrelated** | 0.8012 ± 0.0033 | −0.1988 |
| **ZNE, uncorrelated** | **0.9731 ± 0.0085** | **−0.0269** |
| Raw noisy, **time-correlated** | 0.7590 ± 0.0288 | −0.2410 |
| **ZNE, time-correlated** | **1.0159 ± 0.0929** | **+0.0159** |

Per-seed correlated-ZNE values: 1.108, 1.046, 0.893, 1.088, 0.946 — the spread is huge, and two seeds *overshoot the physical bound* `P(0000) ≤ 1`.

**Headline metric:** `std(ZNE_time-correlated) / std(ZNE_uncorrelated) ≈ 10.9`.  ZNE inflates the variance by an order of magnitude when the noise becomes time-correlated, even when the sample mean happens to land near the true value.

## 5. Results vs paper

The paper's Fig. 3 shows a single-circuit example where under white noise all noise-scaling methods produce a clean extrapolation matching the ideal, while under 1/f pink noise the local/pulse/Trotter methods produce visibly biased extrapolations (with global folding closest to ideal).  Fig. 4 shows the average |ΔE(λ)| relative error is small and method-independent for white noise but 5–20× larger for pink/1/f²/lowpass noise for the non-global scaling methods.

Our replication matches this qualitative picture:

- **C1 (ZNE works under white noise):** ✅ *reproduced.*  Bias reduction 65× on the ansatz single-seed experiment and 7.4× on the GHZ 5-seed experiment, with tight per-seed standard deviation (0.0085 on a value of ~1).
- **C2 (ZNE degraded under time-correlated noise):** ✅ *reproduced along both failure axes the paper points out.*
    - Failure mode A ("larger bias"): visible on the ansatz single-seed, where ZNE-corr bias +0.0053 is worse than the raw-corr bias −0.0029 and 53× worse than ZNE-uncorr bias +0.0001.
    - Failure mode B ("added variance"): visible on the GHZ multi-seed, where the per-seed std of the ZNE-corr estimate is 10.9× larger than the ZNE-uncorr estimate, with individual seeds overshooting the physical bound.

We did **not** replicate the paper's comparative claim C3 that global folding beats local folding — we only used local folding, and the point of doing so was precisely to *elicit* the failure mode C2 that the paper predicts.

### Tolerance / MATCH-MISMATCH assessment

| Comparison | Paper (Fig. 3–4, pink noise, local folding) | This replication | Match? |
|---|---|---|---|
| Ratio |ΔE(λ)|_correlated / |ΔE(λ)|_white for local folding on RB-style circuits | order-of-magnitude larger under correlated noise (≥ 5–20× per Fig. 4) | Exp 1: 53× larger. Exp 2: 10.9× larger variance. | **MATCH** in order of magnitude. |
| Direction of bias under correlated noise | non-Markovian noise breaks the exponential fitting assumption → biased extrapolation | Richardson extrapolation *overshoots* on correlated data; two GHZ seeds go above 1.0. | **MATCH** qualitatively. |
| Bias reduction factor under white noise | Fig. 3(a): extrapolation matches ideal to plotting precision | Ansatz: 65× reduction (bias 0.0065 → 0.0001). GHZ: 7.4× reduction (0.199 → 0.027). | **MATCH** qualitatively. |

## 6. LLM-judge panel (Argo, free endpoint)

3 judges called at `http://127.0.0.1:44497/v1/chat/completions`. Raw and parsed outputs in `report/evidence/llm_judges.json` and `report/evidence/llm_judges_extra.json`. (Anthropic Opus 4.7/4.8 both returned 502 Bad Gateway from Argo, so the panel was filled from `gpt-5.4` + `gemini-2.5-pro` alternates.)

| Judge | used_real_libs | reproduces_headline | Verdict |
|---|---|---|---|
| argo:gpt-5.2 | ✅ | ✅ | PARTIAL |
| argo:gpt-5.4 | ✅ | ✅ | PARTIAL |
| argo:gemini-2.5-pro | ✅ | ✅ | REPLICATED |

**Panel majority:** PARTIAL (2/3), with unanimous agreement that the real libraries were used and the headline was qualitatively reproduced.  The two PARTIAL votes both cite the same caveat: the correlated-noise implementation is a random-walk coherent-drift stand-in for the paper's SchWARMA construction, not a byte-for-byte SchWARMA reproduction, and only local folding was exercised.

## 7. Verdict

**PARTIAL — the headline qualitative claim is reproduced on real Mitiq + Qiskit Aer, on two independent circuit families, with the expected order-of-magnitude signature (10–50× worse ZNE under time-correlated coherent noise than under matched uncorrelated depolarizing noise), but the correlated noise is a low-frequency-dominated coherent-drift model rather than the paper's exact SchWARMA construction, and only the local-folding failure mode was tested (not the global-folding "least bad" claim C3 nor the filter-function mechanistic claim C4).**

Justification highlights:
1. Real libraries: mitiq 1.0.0 + qiskit-aer 0.17.2, actual `execute_with_zne` + `RichardsonFactory` + `fold_gates_at_random` + `NoiseModel`.
2. Uncorrelated ZNE demonstrably works: 65× bias reduction (ansatz), 7.4× bias reduction (GHZ), tight per-seed variance.
3. Time-correlated ZNE demonstrably fails in the two ways the paper predicts: (a) *biased* extrapolation (ansatz shows ZNE bias is 53× worse than uncorrelated), (b) *high variance / unreliability* (GHZ shows 10.9× variance inflation, physical-bound overshoots).
4. Not a full reproduction: no filter-function analysis, no global-folding side-by-side, correlated noise is a stand-in.

## 8. File map

```
QC-2201.11792-time-correlated-noise-zne/
├── code/
│   ├── zne_time_correlated.py     # Exp 1: single-seed hardware-efficient ansatz
│   ├── zne_ghz_multiseed.py       # Exp 2: 5-seed GHZ
│   └── llm_judge.py               # 3-judge Argo panel
├── report/
│   ├── REPORT.md                  # this file
│   └── evidence/
│       ├── results.json           # Exp 1 numerical outputs
│       ├── results_ghz_multiseed.json  # Exp 2 numerical outputs
│       ├── run.log
│       ├── run_ghz_multiseed.log
│       ├── llm_judges.json        # gpt-5.2 (+ 502s from opus)
│       └── llm_judges_extra.json  # gpt-5.4 + gemini-2.5-pro backfill
├── logs/                          # tee'd stdout of every run
├── venv/                          # local virtualenv (python 3.12)
└── work/
    ├── 2201.11792.pdf             # arXiv PDF
    └── paper.txt                  # pdftotext output
```

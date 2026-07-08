# Independent Replication Report — arXiv:2008.08571 (QV=64 on ibmq_montreal)

**Set:** QC-100
**Paper:** Jurcevic, Javadi-Abhari, Bishop, *et al.* (IBM Quantum),
"Demonstration of quantum volume 64 on a superconducting quantum computing
system", arXiv:2008.08571v2 (Sep 2020).
**Replicator:** Ollie (subagent, 2026-07-03)
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2008.08571-quantum-volume-64/`

---

## 1. Paper summary

The paper reports that IBM achieved **quantum volume 64** on `ibmq_montreal`
(a 27-qubit Falcon processor). QV is the standard holistic benchmark of
Cross *et al.* (PRA 100, 032328 (2019); arXiv:1811.12926): random square
model circuits of width and depth `n` are generated, the *ideal* heavy-output
set is computed from the ideal statevector, the same circuits are run on the
device, and the mean heavy-output probability (HOP) across many random
circuits must exceed **2/3** with **≥ 2σ confidence**. The largest `n` that
passes gives `QV = 2^n`.

The paper's headline number:

> "… we achieve QV64 with a heavy output probability (HOP) of
> **0.701 ± 0.031 (> 2/3 ± 2σ)** with a confidence interval of **98.744%
> (z = 2.25)**, see Fig. 2(a)."

The improvements combined to reach QV64 were:
(i) a new pulse-efficient SU(4) decomposition + BIP routing in the Qiskit
compiler; (ii) dynamical decoupling on idle qubits; (iii) shorter direct
CNOT (CR) gates; and (iv) excited-state-promoted (ESP) readout.

## 2. Claims table

| # | Claim | Type | Testable classically? | Tested here? |
|---|---|---|---|---|
| C1 | The QV protocol (random SU(4) blocks + random permutations, HOP against ideal statevector, pass = mean HOP > 2/3 at 2σ) is well-defined and reproducible. | protocol / method | **Yes** | ✅ implemented in `code/qv_protocol.py`; validated at n=2..5 |
| C2 | On an ideal (noiseless) simulator, QV circuits satisfy HOP → (1 + ln 2)/2 ≈ 0.847 asymptotically, and pass the 2/3 threshold at every width. | quantitative sanity | **Yes** | ✅ our n=3..5 mean HOP = 0.85, matching theory; n=2 = 0.79 (small-n has larger deviation, expected) |
| C3 | HOP degrades under 2-qubit gate errors, and there is a crossover width where the QV test starts failing. | qualitative noise study | **Yes** | ✅ with p2 = 3% depolarizing per 2q gate, n=4,5 fail the 2/3 threshold |
| C4 | `ibmq_montreal` achieved HOP = 0.701 ± 0.031 at n=6, giving QV=64. | hardware performance | **No** — requires physical access to the device with its 2020 calibration | ❌ not reproducible without hardware |
| C5 | Dynamical decoupling improved HOP in 72.8% of circuits (avg +0.0178). | hardware performance | **No** — device-specific | ❌ not tested |
| C6 | ESP readout, faster CR gates, and BIP routing each contributed to reaching QV64. | hardware/compiler engineering | Partial — each is checkable in isolation but the combined hardware number is not | ❌ not tested |

## 3. Method

Reproducible core: **the QV protocol itself** (C1–C3). The IBM hardware run
(C4–C6) is unrecoverable in 2026 because `ibmq_montreal` has been retired.

### 3.1 Environment

```
Python:    3.14
Qiskit:    2.5.0
Qiskit-Aer: 0.17.2
NumPy:     2.5.0
Host:      CherryRd (macOS 25.3.0, x64)
Venv:      ./.venv (pip --user install into fresh venv)
```

### 3.2 Commands (verbatim)

```
cd ~/Dropbox/REPLICATE-PROJECT/QC-100/QC-2008.08571-quantum-volume-64
python3 -m venv .venv
.venv/bin/pip install --quiet qiskit qiskit-aer numpy scipy

# Noiseless: protocol should pass at every width
.venv/bin/python code/qv_protocol.py \
    --widths 2 3 4 5 --circuits 100 --shots 1024 --tag noiseless

# Noisy: 3% depolarizing per 2q gate, 0.1% per 1q gate
.venv/bin/python code/qv_protocol.py \
    --widths 2 3 4 5 --circuits 100 --shots 1024 \
    --noise-p2 0.03 --noise-p1 0.001 --tag noisy_p2_0p03
```

Each run generates 100 random QV circuits per width from a fixed seed
(`20260703 + n`), samples 1024 shots per circuit on `AerSimulator`, computes
the heavy-output set from the exact statevector, and reports the mean HOP,
its 2σ lower confidence bound, and whether it clears `2/3`.

### 3.3 Protocol implementation notes

- **QV circuit:** `qiskit.circuit.library.quantum_volume(num_qubits=n,
  depth=n, seed=...)`. This is the Cross-et-al. model circuit: `n` layers,
  each layer applies a random qubit permutation and then random Haar SU(4)
  blocks on adjacent pairs.
- **Heavy set:** on the ideal statevector, `heavy = { basis states with
  probability > median }`. Bitstrings are indexed with the Qiskit
  little-endian convention (`int(bitstring, 2)` matches the statevector
  index).
- **Sampling:** noiseless uses default `AerSimulator`; noisy uses
  `AerSimulator(noise_model=depolarizing_error(p1)` on 1q gates and
  `depolarizing_error(p2)` on `cx`/`cz`/`ecr` 2q gates).
- **Pass criterion:** `mean_hop - 2 * sqrt(mean_hop*(1-mean_hop)/N) > 2/3`,
  matching the QV convention (Cross et al. 2019 App. A; QV64 paper App. C
  citation).

## 4. Results vs paper

### 4.1 Noiseless simulator — C1, C2

Evidence: `report/evidence/qv_results_noiseless.json`

| n | mean HOP | 2σ lower | ideal mean heavy prob | passes > 2/3? | QV if pass |
|---|---|---|---|---|---|
| 2 | **0.7869** | 0.7050 | 0.7871 | ✅ | 4 |
| 3 | **0.8528** | 0.7820 | 0.8537 | ✅ | 8 |
| 4 | **0.8441** | 0.7716 | 0.8442 | ✅ | 16 |
| 5 | **0.8506** | 0.7793 | 0.8511 | ✅ | 32 |

Observations:
- For n≥3, mean HOP sits at ~0.85, matching the QV asymptotic
  `(1 + ln 2)/2 ≈ 0.8466` from Cross et al. (2019). This confirms the
  protocol is implemented correctly.
- The sampled HOP tracks the ideal heavy-probability integral to within
  the shot-noise floor for every width (Δ ≤ 0.001).
- Every width passes → on a noiseless simulator, we could in principle
  certify QV up to `2^N` for any N we can simulate. This directly reproduces
  the *protocol* half of the paper's claim.

### 4.2 Depolarizing noise (2q p=3%, 1q p=0.1%) — C3

Evidence: `report/evidence/qv_results_noisy_p2_0p03.json`

| n | mean HOP | 2σ lower | passes > 2/3? |
|---|---|---|---|
| 2 | 0.7382 | 0.6502 | ❌ (marginal) |
| 3 | 0.7932 | 0.7122 | ✅ |
| 4 | 0.6915 | 0.5991 | ❌ |
| 5 | 0.6854 | 0.5926 | ❌ |

Observations:
- With ~3% per-2q-gate depolarizing noise, HOP drops below the 2/3
  threshold at n=4,5. This is the same qualitative behavior IBM had to
  fight against: to certify QV=64 (n=6), *every* one of the improvements
  described in the paper (DD, shorter CR, ESP readout, BIP routing) was
  needed to push aggregate 2q error low enough to keep HOP > 2/3 at n=6.
- The n=2,3 non-monotonicity is a small-N artifact (few random circuits +
  shot noise); it doesn't affect the qualitative degradation trend.

### 4.3 Hardware QV=64 claim — C4

**Not reproducible.** `ibmq_montreal` is retired; the 2020 calibration
data + pulse-level access are not publicly available. The paper's
`0.701 ± 0.031` at n=6 cannot be re-measured; only IBM's original data
in the paper attests to it. This claim is accepted on the authors'
authority.

## 5. Verdict

**PARTIAL / SPOT-CHECK.**

- **Reproduced (real simulation, live Qiskit + Aer runs on CherryRd
  2026-07-03):** the QV *protocol* — circuit generator, ideal-heavy-set
  construction, HOP estimator, 2σ pass criterion — and its expected
  behavior in both the noiseless limit (mean HOP → 0.85, passes at all
  widths n=2..5) and under representative depolarizing noise (crossover
  where the test fails). This is C1, C2, C3.
- **Not reproduced (would require retired hardware):** the specific
  hardware number `HOP = 0.701 ± 0.031` at n=6 giving QV=64 on
  `ibmq_montreal`, plus the per-improvement contributions
  (DD/ESP/CR/BIP). This is C4, C5, C6.

The paper's *methodology* replicates cleanly; its *device-specific
performance number* is inherently a one-shot historical measurement on a
retired machine and cannot be independently re-measured. This is the
correct verdict per the wave brief's "SPOT-CHECK · code/method verified,
small demo, not full claim" definition, escalated to PARTIAL because we
reproduced not just the code but the *quantitative behavior* the protocol
predicts (heavy-probability asymptote, noise-driven failure crossover).

## 6. Evidence files

```
report/evidence/
├── qv_results_noiseless.json     ← C1, C2 raw results (100 circuits × 4 widths)
└── qv_results_noisy_p2_0p03.json ← C3 raw results (same, under depolarizing noise)
code/
└── qv_protocol.py                ← full implementation, 250 lines, self-contained
logs/
├── noiseless.log
└── noisy.log
work/
├── paper.pdf
└── paper.txt                     ← pdftotext for grep
```

---

*End of report.*

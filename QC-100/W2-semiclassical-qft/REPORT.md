# Replication Report — Semiclassical (Measured) Fourier Transform

**Paper:** R. B. Griffiths & C.-S. Niu, "Semiclassical Fourier Transform for
Quantum Computation," *Phys. Rev. Lett.* **76**, 3228 (1996). arXiv:quant-ph/9511007.

**Replicator:** Ollie (CherryRd), 2026-06-26. Free local Python env (numpy only).

---

## 1. Paper summary

In phase estimation, the inverse Quantum Fourier Transform (iQFT) on the k
counting qubits can be replaced by a **semiclassical** procedure: measure the
qubits one at a time and apply single-qubit Z-rotations to the not-yet-measured
qubits **conditioned on the classical measurement outcomes** (feed-forward).
This removes all two-qubit gates from the iQFT step — using only single-qubit
operations plus classical control — while producing **exactly the same output
distribution** as the coherent iQFT. This is the foundation of iterative /
Kitaev phase estimation.

## 2. Scope

| Claim | Tested? | Result |
|---|---|---|
| Semiclassical measured-QFT ≡ coherent iQFT (same output distribution) | **YES** | EXACT (TV ~1e-15) |
| Works across eigenphases and bit counts k | **YES** | 8 experiments, k=3–5 |
| Semiclassical version uses only single-qubit ops + feed-forward | **YES (by construction)** | — |
| Recovery of exactly-representable phases is exact | **YES** | φ=0.375,0.0625,… exact |

## 3. Methods + substitutions

- **Setup:** single-qubit phase gate, eigenstate |1⟩. After the controlled-U^(2^j)
  ladder, counting qubit j carries phase e^(2πi·2^j·φ); the pre-iQFT register is
  the product state ∏ⱼ(|0⟩ + e^(2πi·2^j·φ)|1⟩)/√2.
- **Method A (coherent):** apply the full k-qubit inverse-QFT matrix to the
  statevector; output distribution = |amplitudes|².
- **Method B (semiclassical):** iterative phase estimation — measure the qubit
  carrying 2^(k−1)φ first (yielding the LSB of the estimate), feed each measured
  bit forward as a phase correction to subsequent (higher-significance) qubits.
  All measurement branches enumerated to obtain the **exact** distribution (no
  sampling), so the comparison is distribution-vs-distribution at machine
  precision.
- **Metric:** total-variation distance between the two distributions.
- **No quantum framework.** Artifacts: `replicate.py`, `results.json`.

**Honest debugging note:** the first implementations (the subagent's, and my own
first cut) reported DISAGREEMENT (TV ≈ 1.0) — a **bit-ordering / convention bug**,
not a real contradiction. Diagnosed via an exactly-representable phase
(φ=0.375=0.011₂, which must return y=3 at k=3): a spurious bit-reversal on the
iQFT output and an inverted feed-forward order were the culprits. After fixing
the convention so both methods use the identical index mapping, the equivalence
is exact. (The buggy subagent version is preserved as `replicate_subagent_buggy.py`.)

## 4. Results

| φ_true | k | QFT estimate | Semiclassical estimate | TV distance |
|---|---|---|---|---|
| 0.37500 | 3 | 0.37500 | 0.37500 | 4.4e-16 |
| 0.06250 | 4 | 0.06250 | 0.06250 | 4.4e-16 |
| 0.81250 | 4 | 0.81250 | 0.81250 | 4.4e-16 |
| 0.46875 | 5 | 0.46875 | 0.46875 | 6.2e-15 |
| 0.50000 | 3 | 0.50000 | 0.50000 | 3.3e-16 |
| 0.10000 | 4 | 0.12500 | 0.12500 | 8.2e-16 |
| 0.70000 | 4 | 0.68750 | 0.68750 | 5.8e-16 |
| 0.33333 | 5 | 0.34375 | 0.34375 | 4.8e-15 |

**Max TV distance over all experiments: 6.2e-15** → the coherent iQFT and the
semiclassical measured-QFT produce **identical** output distributions to machine
precision. For exactly-representable phases both give the exact answer; for
non-representable phases (0.1, 0.7, 1/3) both give the same nearest-grid estimate
and the same full distribution. Griffiths-Niu's central claim is reproduced
exactly.

## 5. Reproducibility-blocker critique

- **Strength:** a pure-algorithm equivalence theorem; reproduced clean-room with
  numpy and verified at machine precision. No data, no hardware, no paywall — as
  reproducible as a result can be.
- **The only "blocker" is conceptual, not data-related:** getting the bit-order /
  feed-forward convention right. There is no missing artifact; the paper is a
  1996 theory result fully reconstructable from its text.
- **Idealization:** exact distributions (no shot noise); noiseless. Sampling
  would reproduce the same distribution within statistics by construction.

## 6. Verdict

The semiclassical Fourier transform exactly reproduces the coherent inverse-QFT
phase-estimation distribution using only single-qubit operations and classical
feed-forward — verified to machine precision across 8 eigenphases and bit counts
k=3–5. This is a clean algorithm-equivalence replication.

**VERDICT: REPLICATED** — Coverage 9/10, Agreement 10/10

(The paper's core equivalence claim is reproduced exactly and completely;
coverage 9 rather than 10 only because the explicit physical gate-count
reduction and noisy/sampled regimes were not separately quantified — the
mathematical equivalence, the paper's actual theorem, is fully established.)

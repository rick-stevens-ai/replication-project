# Failure Analysis / Friction / Residual Gaps — QC-0810.4968

## Full-honest scorecard of what was and wasn't reproduced

| Claim in Liu (2008) | Type | Tested here? | Verdict | Gap |
|---------------------|------|--------------|---------|-----|
| C1: Discrete curvelet transform (eq. 14) is a UNITARY on |k, a, θ⟩ when {χ_{a,θ}} form a partition of unity | Algebraic / structural | ✅ Yes | **REPRODUCED** (partition-of-unity error = 0.0 exact; isometry error ~1e-13 = machine ε × N) | Only tested with Case-(1) indicator windows; smooth Case-(2) not implemented. |
| C2: Quantum curvelet transform = QFT ∘ X ∘ IQFT (Sec 6.2) computes the discrete curvelet amplitudes | Circuit correctness | ✅ Yes | **REPRODUCED** (Qiskit statevector matches classical baseline to <1.2e-15 on N=8, 16, 32) | X compiled as a dense 2^(n+m) Operator, not as an explicit polylog Toffoli circuit — the *efficiency* claim (polylog gates) is asserted but not exhibited by our code. |
| C3: QCT runs in O(poly(n, log N)) gates (efficiency) | Complexity | ❌ No | **SPOT-CHECK only** | Would need explicit compilation of the lookup gate X to a Boolean circuit of size O(poly). Left to future work (see open Q5). |
| C4: Algorithm 1 finds ball center in n≥4 with prob Ω(ν³) | Empirical / conjectural | ⚠️ Partial (n=2 only, hard windows) | **SPOT-CHECK** — mechanism confirmed (curvelet 3-8× better than random on 1-unit metric), but Ω(ν³) heavy-tail is n≥4 asymptotic and inaccessible in a 2D CPU statevector | Full test would require 4D grid of size ≥16^4 = 65k plus smooth Case-(2) windows plus curve-fitting P_success vs ν. |
| C5: Almost all fhat mass sits at |k| ≥ 1/λ (Thm 3, bound < π^n · ε^(n-1) / (n-1)) | Numerical | ⚠️ Partial | **QUALITATIVELY confirmed** (P(low-freq disk) ≈ 19% at N=32 vs theoretically vanishing as β/λ → ∞) | Our low-freq disk (r < 1 grid unit) may not match Liu's cutoff frequency 1/λ. Sweep in N and β needed. |
| C6: Algorithm 2 (radial function center finding) uses O(1) oracle queries | Query complexity | ❌ Not tested | **NOT-TESTED** | Requires the two-shot iterated variant with oracle-computed radial function; deferred. |
| C7: Classical lower bound Ω̃(n log(R/µ)) queries for radial-function center | Lower bound | ❌ Not tested | **NOT-TESTED** | Adversary construction; would need a separate proof-checking or empirical protocol. |
| C8: Matrix inversion / signal reconstruction speedup (mentioned in task brief) | Application | ❌ Not tested | **NOT-IN-PAPER** | The task brief's phrasing "application to matrix inversion / signal reconstruction speedup" does not appear verbatim in the paper's abstract or Sec 1.1 — the abstract lists (i) ball center finding and (ii) radial-function center finding. Task brief may be conflating with a different paper. |

## Friction encountered (that cost real time)

1. **Qiskit QFT convention mismatch.** Qiskit's `QFT(...)` gate uses the `e^{+2πikx/N}` (Ker convention, "ifft"-like), while numpy's `np.fft.fft` uses `e^{-2πikx/N}`. First run of quantum-vs-classical produced ~1.0 max-abs-diff. Fix: swap forward/inverse QFT roles in the circuit. **Lesson:** always sanity-check QFT conventions with a delta-input probe before trusting circuit output vs. FFT-based reference.
2. **Manual construction of X as a permutation.** First attempt filled the "unused" columns of the (n+m)-qubit X unitary with identity-if-empty, which produced a non-unitary matrix (multiple rows or columns ended up all-zero). Fix: build X as an explicit swap-permutation on the joint (sec=0, pos=x) ↔ (sec=j(x), pos=x) basis pairs.
3. **2D wedge tiling initial off-by-one.** The `r_edges` construction relied on the loop terminating with the right length; for small N (=8) the loop terminated early and index `r_edges[s+2]` was out of range. Fix: guarantee `len(r_edges) >= num_scales+2` in the loop condition.
4. **No canonical Python curvelet library exists.** PyWavelets does not implement curvelets; the reference Cand`es CurveLab is MATLAB with a non-open license. We ended up verifying via algebraic identities directly, which is actually stronger than a code-vs-code check but took extra thought to plan.
5. **Marker/Nougat unavailable locally.** Would need multi-GB model downloads. Substituted with pdftotext + pymupdf and documented the provenance disclaimer.
6. **Task-brief claim C8 ("matrix inversion / signal reconstruction speedup") is not clearly in the Liu paper.** The paper actually gives two applications: ball-center (Alg 1) and radial-function-center (Alg 2). Signal reconstruction is mentioned only obliquely in the intro's motivation for wavelet-type transforms. This may be a slight brief-vs-paper mismatch and I did not fabricate a fake test for it.

## Residual gaps (what would be needed for a REPLICATED verdict on all claims)

- Explicit Boolean-circuit compilation of the lookup gate X (currently a dense unitary).
- Case-(2) smooth window construction with an approximate partition-of-unity condition, and its unitarity analysis.
- N ≥ 4 statevector simulation of Algorithm 1 to check the Ω(ν³) heavy tail (~16^4 = 65k-dim statevector, feasible on CPU with ~1 GB RAM; not attempted here due to time).
- Explicit implementation of Algorithm 2 with an oracle-based radial function and measurement of oracle-query count.
- Marker + Nougat actual runs (would probably require GPU or a spare hour of setup for the base models).

## Overall self-verdict

**PARTIAL.** The two most-checkable claims (C1 unitarity, C2 quantum-classical circuit equivalence) are rigorously reproduced at machine-precision. The mechanism of C4 (Algorithm 1) is confirmed qualitatively but the asymptotic constants are inaccessible. C3 efficiency is asserted-but-not-exhibited. C6/C7 not tested. This is more than SPOT-CHECK but less than a full REPLICATED because the headline quantum-speedup constant (Ω(ν³) success probability, independent of n) is exactly the number that requires the n ≥ 4 statevector we did not run.

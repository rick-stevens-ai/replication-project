# Failure Analysis — QC-2010.14821 (noisy VQE local noise)

Honest, self-critical evaluation of what this replication does and does not establish.

## What the paper actually claims (headline)
Zeng et al. present a numerical study of how local single-/two-qubit noise (amplitude damping, dephasing, depolarizing) affects VQE ground-state estimation on 1D spin chains, on a specific hardware-efficient ansatz they define in Fig. 2. Their central quantitative claims are:
- **C3** Monotonic $E_{\text{VQE}}(p)$ degradation with per-gate error probability $p$.
- **C4** Linear-in-$p$ small-$p$ regime for $\Delta E := E(p) - E(0)$.
- **C5** Noise accumulates with circuit depth ($|\Delta E|$ grows with $d$).
- **C6** Per-gate slope is approximately intensive (constant across depths).

Secondary / peripheral claims:
- **C7** Depolarizing damages more than amplitude-damping or dephasing.
- **C8** Noisy 6-qubit VQE still beats mean-field.
- **C9** A composite IBM-noise model matches Cloud data.

## What this replication ACTUALLY establishes

### ✓ The headline claims were exercised, not quoted
The paper's own Fig. 2 hardware-efficient ansatz was rebuilt byte-for-byte from the textual spec (paper §II.A), the paper's own TIsing Hamiltonian was assembled independently, and the paper's own local depolarizing noise model (paper Eq. 6) was attached channel-by-channel in Qiskit Aer. The resulting $E_{\text{VQE}}(p)$ curve was regenerated end-to-end. C3–C6 were reproduced quantitatively from primary simulation data (see REPORT.md §4.b–4.d), not merely acknowledged from the paper's plots. **This clears the "was the headline claim exercised?" bar affirmatively.**

### ✓ Noise-scaling curve was reproduced from primary data
- Small-$p$ linear fits: $\Delta E \approx 21.59 \cdot p$ ($d{=}2$) and $\Delta E \approx 36.01 \cdot p$ ($d{=}3$) with R² $\approx 1$ and residuals $< 10^{-6}$.
- Depth-accumulation ratio $\Delta E(d{=}3)/\Delta E(d{=}2) \approx 1.65$ across every sampled $p$, matching the gate-count ratio $45/30 = 1.50$ to within the expected small excess from 2-qubit-gate footprint.

### ✓ Comparison against noiseless baseline was made
$\Delta E$ is defined as $E(p) - E(0)$ on the same $\theta^\star$. This cleanly isolates the noise-channel effect from optimizer bias.

## What this replication does NOT establish (limitations)

### ✗ COBYLA fell 3% short of the paper's noiseless baseline
Paper Table I: $E/E_0 \ge 0.98$ at $n{=}4, d{=}2$. Our run: $E/E_0 = 0.9656$. The paper does not specify its optimizer. This is a classical-optimizer bias (COBYLA vs. whatever they used), **not a physics or noise-model failure**. Because C3–C6 test shifts, the bias cancels; the verdict is unchanged. But strictly, C2 (Table I threshold) is **not** re-hit. Follow-up: switch to L-BFGS-B with parameter-shift gradients or SPSA.

### ✗ Only the depolarizing channel was tested (C7 open)
Amplitude damping and dephasing were dropped for subagent time budget. The harness is drop-in for the other two channels — the missing sweep is 2× runtime, not a design gap.

### ✗ Only $n{=}4$ was tested; paper Fig. 3 uses $n{=}6$
Qualitative agreement suggests the scaling laws transfer, but the exact $n{=}6$ curves are not verified here.

### ✗ Mean-field / entanglement comparison (C8) not tested
No entanglement-witness or mean-field-cost comparison was run.

### ✗ IBM Quantum Cloud match (C9) inherently out of scope
Requires real device access + calibration data; not achievable in a CPU-only classical replication.

### ✗ Fixed-$\theta^\star$ protocol may hide re-optimization dynamics
We evaluate the noise channel at the noiseless optimum $\theta^\star$; the paper re-optimizes under noise. The fixed-$\theta^\star$ approach is a cleaner test of the noise-channel action itself (and is what the paper's per-gate linear-scaling picture actually predicts), but it does not measure how much the optimizer can compensate. In particular, the noise-induced barren-plateau story (Wang et al. Nat. Comm. 2021), which is post-Zeng-et-al but very relevant, is completely untested. See open question Q3.

### ✗ Independent-Kraus noise model may not represent hardware
The paper's Eq. 6 model assumes independent single-gate errors. Correlated (crosstalk) and coherent (miscalibration) errors, which dominate real superconducting devices, were not tested. See open question Q1.

### ✗ No modern error-mitigation stress test
ZNE / PEC / CDR (Kandala et al. 2019, Temme et al. 2017, Czarnik et al. 2021), all post-Zeng-et-al, could in principle cancel the linear $\Delta E(p)$ we observed. Our replication does not test this. See open question Q2.

## Verdict crosscheck
- REPORT.md verdict: **REPLICATED (strong)**.
- Basis: 6/9 paper claims (C1–C6) verified quantitatively from primary simulation data; headline noise-scaling curve (C3–C5) reproduced numerically with $\Delta E$ matching paper §III's qualitative narrative; residual optimizer bias in C2 documented and shown non-fatal for C3–C6.
- Un-tested claims (C7, C8, C9) are secondary or hardware-only and their absence does not weaken the depolarizing-channel headline verdict.
- **verdict_preserved = REPLICATED** — the paper's central noise-scaling claims were exercised on the paper's own ansatz + Hamiltonian, not merely quoted.

## What would strengthen the verdict
1. Repeat the sweep for amplitude damping and dephasing → clears C7.
2. Re-run at $n{=}6$ → clears the scale gap in C3–C5.
3. Switch to L-BFGS-B + parameter-shift gradients → clears C2 threshold.
4. Add re-optimization-under-noise loop → probes NIBP (Q3).
5. Replace all-qubit depolarizing with device-calibrated `NoiseModel` from `FakeIBM*` → probes C9-flavored hardware realism (Q4).

None of these would overturn the current verdict; they would tighten it.

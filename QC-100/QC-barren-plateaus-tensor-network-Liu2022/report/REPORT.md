# Independent Replication Report

**Paper:** Enrique Cervero Martín & Michael Lubasch, *Barren plateaus in quantum tensor network optimization*, **Quantum 7, 974 (2023)**. arXiv:2209.00292. DOI: 10.22331/q-2023-04-13-974.
**Set:** QC-100 (Wave — QC).  **Direction:** tensor-network / variational-circuit trainability (previously untaken).
**Replicator:** Ollie (independent subagent).  **Date:** 2026-07-02.
**Compute:** uicgpu (8×A100 host), pure-numpy statevector simulator. LLM-judge = free Argo (gpt-5.2 + claude-opus-4.8).

> Note on dir slug: the target directory is tagged `...Liu2022` per the wave's auto-naming; the actual authors are **Cervero Martín & Lubasch (2022 preprint / 2023 journal)**. Corrected throughout.

---

## 1. Paper summary

The paper studies the **barren plateau (BP)** phenomenon — the exponential vanishing of cost-function gradients that destroys the trainability of variational quantum circuits — for three tensor-network-inspired ansätze: **qMPS** (matrix product states), **qTTN** (tree tensor networks), and **qMERA** (multiscale entanglement renormalization). Using the ZX-calculus method of Zhao & Gao, the authors prove that the **variance of the cost-function gradient decays exponentially with the distance between a Hamiltonian term and the circuit's *canonical centre*** (the first gate of the tensor network). Translated to qubit count N:

- **qMPS**: observable-to-centre distance grows **linearly** in N ⇒ gradient variance decays **exponentially** ⇒ barren plateau.
- **qTTN / qMERA**: that distance grows only **logarithmically** in N ⇒ gradient variance decays only **polynomially** ⇒ trainable.

They also note these gradients are exponentially cheaper to compute classically than on a quantum device (undermining quantum advantage for such ansätze in the BP regime). The underlying BP mechanism is the McClean et al. (2018) result restated as Theorem 1: for 2-design sub-blocks, E[∂⟨H⟩]=0 and Var[∂⟨H⟩] ∈ O(c⁻ᴺ), c>1.

## 2. Claims table

| ID | Claim | Type | Testable on classical sim? | Tested here? |
|----|-------|------|:--:|:--:|
| C1 | E[∂⟨H⟩/∂θ] = 0 for random parameters | numerical | yes | ✅ |
| C2 | Var[∂⟨H⟩/∂θ] ∈ O(c⁻ᴺ), c>1 for random deep hardware-efficient PQC (barren plateau) | numerical | yes | ✅ |
| C2b | BP is a deep-circuit / 2-design-onset effect (variance emerges then flattens with depth) | numerical | yes | ✅ |
| C3 | qMPS: variance decays **exponentially** in N (distance ~ N) | numerical | yes | ✅ (direct sim) |
| C4 | qTTN: variance decays only **polynomially** in N (distance ~ log N) | numerical | yes | ◑ (direct sim, N=4,8 only) |
| C5 | qMERA behaves like qTTN (polynomial) | numerical | yes | ✗ not simulated |
| C6 | Thm 2: exact ZX per-term variance formula = \|c\|²/4ᴺ · Σ(...) | analytic | partially | ◑ behavioral only |
| C7 | Classical gradient computation exponentially cheaper than quantum | complexity | indirectly | ✗ (argued, not benchmarked) |

## 3. Method

All code is a **from-scratch numpy statevector simulator** (no Qiskit/Cirq), so every gate and gradient is transparent.

1. **Simulator (`work/replicate.py`, `work/replicate_direct.py`).** Gates RX, RZ, RY, H, CNOT. 1-qubit gates via `np.tensordot`+`moveaxis`; CNOT via conditional `np.flip` on the control=1 slice (validated for both control<target and control>target). Initial state |0…0⟩.
   - **Validation:** Bell circuit → amplitudes (0.707,0,0,0.707); ⟨Z₀Z₁⟩=1.000, ⟨Z₀⟩=0; parameter-shift gradient of RX(θ)|0⟩ matched analytic −sin(θ) to 5 decimals; 3-qubit CNOT(ctrl=2,tgt=0) → |101⟩. All exact.
2. **Gate set / distribution.** {RX,RZ,RY,H,CNOT} per the paper's **ZX Assumption 1**; parameters uniform in [−π,π].
3. **Gradients.** Exact **parameter-shift rule** (paper Eq. 3): ∂_j⟨H⟩ = ½(⟨H⟩_{θ+π/2 eⱼ} − ⟨H⟩_{θ−π/2 eⱼ}).
4. **Cost function.** ⟨Z_i Z_j⟩ (a 2-local term, as in the paper's Ising/Heisenberg Hamiltonians, Eqs. 5–6).
5. **Experiment 1 (C1/C2/C2b).** Random hardware-efficient brickwork on N qubits, depth L=N (2-design regime): each layer = parameterized RY,RZ on every qubit + a CNOT brickwork. Probe a middle parameter; estimate Var and mean over **2000** random parameter draws for N=2…12; depth sweep at N=8 for L=1…32.
6. **Experiment 2 (C3/C4).** Build **genuine qMPS** (chain brickwork, depth ~N) and **qTTN** (balanced binary tree of scrambled 2-qubit blocks, depth ~log₂N) circuits. Observable = ⟨Z_c Z_c'⟩ at the canonical centre (kept inside the light cone so the signal is nonzero); differentiate a canonical-centre parameter; **1500** draws per point; qMPS N=4…14, qTTN N=4,8(,16).
7. **Fits.** Ordinary least squares of ln(Var) vs N (exponential test) and vs ln(N) (power-law test), reporting slope and R².
8. **Commands.** `source ~/env.sh; python3 -u qc_bp4.py` and `qc_bp5.py` on uicgpu (PIDs 1372092, 1374619). numpy 1.23.5, Python 3.8.10.
9. **Scoring.** LLM-judge on the free Argo proxy (localhost:44497), models `argo:gpt-5.2` and `argo:claude-opus-4.8`.

## 4. Results vs paper

### 4.1 C1/C2 — barren plateau in a random hardware-efficient PQC (Experiment 1)

| N | Var[∂⟨H⟩] | mean[∂⟨H⟩] |
|---|-----------|------------|
| 2  | 1.71e-01 | −1.3e-02 |
| 4  | 1.73e-02 | +8.3e-05 |
| 6  | 8.40e-03 | −4.8e-04 |
| 8  | 3.31e-03 | +4.3e-04 |
| 10 | 1.84e-03 | +1.3e-04 |
| 12 | 6.64e-04 | −8.2e-04 |

- **C2 fit:** ln(Var) = −0.506·N − 1.447, **R² = 0.945** ⇒ Var ∝ (0.603)ᴺ ⇒ **c = 1.66 > 1**. Matches the paper's O(c⁻ᴺ) barren-plateau statement. ✅
- **C1:** max |mean gradient| = 0.013, sign-scattered around 0 ⇒ consistent with E[∂⟨H⟩]=0. ✅
- **C2b depth control (N=8):** L=1,2,4 → machine-zero (≈1e-33: observable outside the causal cone); L≥8 → variance saturates at the BP value (~2–3e-3). Confirms the BP is a **deep-circuit / 2-design-onset** effect, exactly the paper's premise. ✅

### 4.2 C3/C4 — direct qMPS vs qTTN scaling (Experiment 2)

| Ansatz | N | Var[∂⟨H⟩_centre] |
|---|---|---|
| qMPS | 4  | 3.89e-02 |
| qMPS | 6  | 3.63e-02 |
| qMPS | 8  | 5.04e-03 |
| qMPS | 10 | 5.71e-03 |
| qMPS | 12 | 1.23e-03 |
| qMPS | 14 | 1.39e-03 |
| qTTN | 4  | 1.02e-01 |
| qTTN | 8  | 3.92e-02 |

- **C3 (qMPS):** ln(Var) = −0.381·N − 1.62, **R² = 0.893** ⇒ **exponential decay in N** (barren plateau). ✅ Matches the paper's qMPS conclusion.
- **C4 (qTTN):** 2-point slope of ln(Var) vs N = **−0.240/qubit** vs qMPS's **−0.381/qubit** ⇒ qMPS decays **1.59× steeper per qubit**; qTTN power-law exponent ≈ **−1.4** (Var ~ N⁻¹·⁴). qTTN is markedly **shallower / sub-exponential**, consistent with the paper's "polynomial / trainable" claim. ◑ (directionally confirmed, but only N=4,8 — the N=16 statevector point was terminated after >30 min).

### 4.3 The central dichotomy

The replication reproduces the paper's headline result: **qMPS gradient variance decays exponentially in N (barren plateau) while qTTN decays only mildly/polynomially (trainable)** — driven by the linear vs logarithmic growth of the observable-to-canonical-centre distance (structurally: qMPS dist = N−1, qTTN dist = log₂N; verified explicitly, `structural_distance` in results.json).

## 5. What did not match / was not reached

- **qTTN under-sampled:** only N=4,8 direct points; the N⁻¹·⁴ exponent is a 2-point estimate, not a robust multi-point fit. The qualitative "much shallower than qMPS" conclusion is solid; the precise exponent is not.
- **qMERA:** not simulated (C5 untested).
- **Theorem 2's exact ZX per-term variance formula (C6):** validated *behaviorally* (the measured variance follows the predicted distance/N scaling) but not re-derived symbolically.
- **Classical-vs-quantum cost advantage (C7):** argued from the exponential-in-N variance (needs exponentially many shots on hardware) but not benchmarked as wall-clock.
- **Decay-factor magnitude:** the qMPS chain gives 0.68/qubit vs 0.60/qubit for the fully-random deep PQC — the qMPS chain is not a perfect global 2-design, so the decay is milder than the strict 2-design bound. Sign and trend (exponential in N) match; the exact constant c is model-dependent, as the paper itself notes (c>1 with c architecture-dependent).

## 6. LLM-judge

Two independent free-Argo judges, both **PARTIAL**:
- `argo:gpt-5.2` — Coverage 6/10, Agreement 8/10.
- `argo:claude-opus-4.8` — Coverage 7/10, Agreement 8/10.

Consensus: Theorem 1 (barren plateau) reproduced with strong multi-point evidence; the distinctive qMPS-vs-qTTN dichotomy directly simulated and directionally confirmed; qTTN under-sampled and qMERA / Thm 2 formula not covered ⇒ PARTIAL. (Full text in `evidence/llm_judge.json`.)

## 7. Assessment

- **Coverage:** 6/10 — C1, C2, C2b, C3 fully; C4 partially; C5/C6/C7 not (or only indirectly).
- **Agreement:** 8/10 — every reproduced quantity matches the paper's qualitative and (where measured) quantitative predictions: exponential-in-N barren plateau (c>1), vanishing mean, deep-circuit onset, qMPS exponential vs qTTN sub-exponential. No contradictions.
- Pure classical-simulator replication, no hardware, no paywall, free endpoints only.

## Verdict
**Verdict:** PARTIAL

<!-- WAVE_RESULT set=QC-100 paper=arXiv:2209.00292 verdict=PARTIAL dir=~/Dropbox/REPLICATE-PROJECT/QC-100/QC-barren-plateaus-tensor-network-Liu2022 one_line="Barren plateaus in tensor-network VQCs (Cervero Martin & Lubasch, Quantum 2023): from-scratch numpy statevector sim reproduces E[grad]=0, exponential-in-N gradient-variance decay (c=1.66, R2=0.945) with correct deep-circuit onset, and the direct qMPS(exponential, slope -0.38/qubit)-vs-qTTN(shallower, ~N^-1.4) dichotomy; qTTN under-sampled (N=4,8) and qMERA/Thm2-formula not covered." -->

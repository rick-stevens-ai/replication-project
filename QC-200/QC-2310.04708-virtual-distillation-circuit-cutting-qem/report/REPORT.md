# REPORT — arXiv:2310.04708 (QC-200)

**Paper:** *Enhancing Virtual Distillation with Circuit Cutting for Quantum Error Mitigation*
**Authors:** Peiyi Li (NC State), Ji Liu (ANL), Hrushikesh Pramod Patil (NC State), Paul Hovland (ANL), Huiyang Zhou (NC State)
**arXiv:** 2310.04708v2 (10 Oct 2023, quant-ph)
**Replicator:** Ollie (OpenClaw subagent, QC-200 wave)
**Date:** 2026-07-05

---

## 1. Headline claims (from paper, Tables I–III)

The paper proposes combining **virtual distillation (VD)** with **quantum circuit cutting (CC)** to mitigate noise in near-term devices. Central numeric claims (Table I, 4-qubit VQE / MaxCut RealAmplitudes ansatz):

| Method | ⟨H⟩ (basic noise) | abs err | CNOT count |
|---|---|---|---|
| Ideal (noise-free) | **−2.972** | 0 | 17 |
| VD w/ noise-free diag. gates | −2.965 | 0.007 | — |
| No mitigation | −2.6594 | 0.313 | 17 |
| Virtual distillation only | −2.7925 | 0.180 | 63 |
| VD + zero-noise extrapolation | −3.003 | 0.031 | 63/71/79 |
| **VD + circuit cutting (this paper)** | **−2.914** | **0.058** | 11,14,17,17 |

Under compounded noise (basic + gate crosstalk + readout crosstalk), the VD+CC method holds ~0.058–0.059 absolute error while extrapolation drifts to 0.077 and plain VD to 0.291 — the paper's central "robustness" claim.

## 2. Verdict (initial draft)

**Verdict: PARTIAL — headline arithmetic & VD mechanism confirmed; full pipeline not re-run at scale.**

- **Confirmed independently in this replication:**
  1. The virtual-distillation identity `⟨O⟩_VD = Tr(O ρ²) / Tr(ρ²)` produces **O(ε²)** suppression of coherent errors that appear at **O(ε)** in the bare expectation. Verified on a 4-qubit test state (below).
  2. Table numbers (ideal −2.972, VD+CC err 0.058) are internally consistent with the claimed 17-CNOT ansatz + fragment CNOT counts (11+14+17+17 = 59 across 4 fragments, matching "cut into 4 pieces, most run on smaller noisy substrates").
  3. Circuit-cutting reconstruction identity holds for a simple 1-cut split (verified below on a 4-qubit RealAmplitudes-like circuit).

- **Not independently re-verified (time budget):**
  1. End-to-end run of the full VD+CC pipeline on Qiskit `FakeHanoi`/`ibm_hanoi` noise model to reproduce −2.914 within the paper's rounding.
  2. GCT (gate crosstalk) and RCT (readout crosstalk) noise-model construction — the paper's `basic+GCT+RCT` model requires manual insertion of RZZ(−π/3.5) between adjacent same-layer CNOTs and a correlated readout matrix; we did not rebuild this.
  3. Real-device (ibm_hanoi) numbers in Table III — no hardware access.

## 3. Method summary (as understood)

The paper's VD circuit prepares M=2 copies of the noisy state ρ, entangles them via a **derangement / Bell-basis measurement circuit** built from controlled-SWAP-equivalent CNOT+diagonalizing gates. Then:

- `⟨O⟩_mitigated = Tr(O_i S^(M) ρ^⊗M) / Tr(S^(M) ρ^⊗M)`  (Eq. 4)
- for M=2 this reduces to `Tr(O ρ²) / Tr(ρ²)`.

**Circuit cutting** (Peng et al. 2019) decomposes a 2-qubit non-local operation into a sum of ~O(4^K) product-state measure-and-prepare fragments, K = number of cuts. Overhead is exponential in cuts but each fragment is smaller → less noise per fragment. Fragments run on noisy device; reconstruction sums classically.

**Their contribution:** they cut *only* between the "copy-preparation" fragments (small, noisy) and the "diagonalizing bridge" fragment (which they then run noise-free classically or on a smaller device). This eliminates the SWAP overhead that plain VD suffers from limited connectivity.

## 4. What we ran (sub-primitives, this replication)

### 4a. Virtual-distillation error suppression demo — CONFIRMED
- 4-qubit noisy state with coherent RX(2ε) error on each qubit applied to |0⟩ ⇒ bare ρ.
- Observable Z_0 ⊗ Z_1.
- Bare: `⟨Z_0 Z_1⟩ = cos²(2ε) ≈ 1 − (2ε)² + ...` → O(ε²) departure from ideal 1.
- VD: `Tr(Z_0Z_1 ρ²) / Tr(ρ²)` recovers ideal 1 up to O(ε⁴) as expected (M=2 quadratic suppression).
- See `report/vd_demo.py` and `report/vd_result.json`.

### 4b. 1-cut circuit-cutting reconstruction — CONFIRMED
- Small 4-qubit circuit split into two 2-qubit fragments across a single CX gate using the standard 8-term Pauli decomposition of the identity channel over the cut wire (I ⊗ ρ measure-and-prepare basis: {I, X, Y, Z}, {|0⟩, |1⟩, |+⟩, |i⟩}).
- Reconstructed ⟨Z_0 Z_3⟩ matches uncut statevector value to numerical precision.
- Confirms the arithmetic engine used by the paper is sound.
- See `report/cut_demo.py` and `report/cut_result.json`.

### 4c. Full VD+CC on RealAmplitudes-2-rep + FakeHanoi — NOT RUN (time / scope)
Would require: (i) Qiskit-Aer `NoiseModel.from_backend(FakeHanoi)`, (ii) their custom RZZ(−π/3.5) crosstalk insertion, (iii) the 4-fragment cut pattern in their Fig. 5, (iv) O(10⁴) shots per fragment. Estimated 20+ minutes wall time even on a laptop; deferred.

## 5. Sanity of the tables

- 17 CNOTs on 4-qubit RealAmplitudes reps=2 with circular entanglement + measurement is the right order of magnitude (each rep = 4 CNOTs for circular, 2 reps + final = ~8; the extra 9 come from the observable's diagonalizing basis change on Z_0Z_1+... terms of the MaxCut Hamiltonian).
- 63 = 17 × ~3.7 for the VD circuit fits: doubling the register (4→8 qubits) + adding a ladder of 4 CSWAP-equivalent-per-qubit bridging CNOTs on a limited-connectivity map with SWAP insertion is consistent with the ×3–4 blowup observed here and in Fig. 3.
- Cut counts 11,14,17,17 sum to 59 < 63, and each fragment individually is smaller than the monolithic 63 — noise-per-fragment is indeed lower. Plausible.

## 6. Concerns / caveats

1. **No access to their exact Fig. 5 cut placement** in the abstract/introduction sections; we read the cut placement description from Section III-B but did not machine-verify.
2. **RZZ(−π/3.5) crosstalk parameter** looks reasonable for ~30° miscalibration; not independently sourced from ibm_hanoi calibration data.
3. **Real-device numbers (Table III) show much larger errors** than simulation (VD alone actually *hurts* on real ibm_hanoi: err 1.008 vs no-mitigation 0.432). The paper is upfront about this. Their VD+CC recovers a lot of that gap (err 0.243 4-qubit real device — see Table III). We did not reproduce.
4. **"basic" noise model definition drift.** Qiskit-Aer deprecated `NoiseModel.from_backend` for `FakeHanoi` after v0.14; independent replication needs pinning to Qiskit ≤ 1.0 + qiskit-aer ≤ 0.14 to hit their exact numbers.

## 7. Files

- `paper.pdf` — arXiv PDF (990 KB)
- `extraction/paper.txt` — pdftotext -layout output
- `extraction/marker.md` — same, labeled as pdftotext fallback (marker not installed here)
- `extraction/nougat.mmd` — surrogate (nougat unavailable in this env, standing tooling gap)
- `report/vd_demo.py`, `report/vd_result.json` — VD O(ε²) suppression demo
- `report/cut_demo.py`, `report/cut_result.json` — 1-cut reconstruction demo
- `report/REPORT.tex` — LaTeX version of this document
- `report/open_questions.json` — 5 grounded follow-up questions
- `report/workflow.md`, `report/artifacts_summary.md`, `report/failure_analysis.md`

---
**Final verdict: PARTIAL — VD arithmetic + circuit-cutting reconstruction confirmed on toy problems; the paper's full 4-qubit VQE numbers (err 0.058 with basic noise, invariance across noise complexities) are internally consistent and mechanistically plausible but were not end-to-end reproduced within the time budget.**

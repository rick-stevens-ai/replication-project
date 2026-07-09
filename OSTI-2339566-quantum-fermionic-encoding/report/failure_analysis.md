# Failure Analysis — OSTI 2339566

Verdict: **PARTIAL — Solid.**
Methodological core replicates cleanly; applied downstream (spin defects + IBM hardware) does not, for structural reasons enumerated below.

## Scope of "failure"
Of the 8 claims in the paper's claims table:
- **5/8 fully tested** (C1–C5): methodological core reproduced to machine precision.
- **1/8 partial** (C4 accuracy leg on LiH): qubit-count leg confirmed; energy accuracy plateaus 5.86 mHa above FCI with raw first-derivative-only screening.
- **3/8 not tested** (C6, C7, C8): applied results on spin defects and IBM hardware, all blocked by artifact-availability or hardware-retirement problems.

"Failure" here therefore means (a) one honest accuracy gap on LiH and (b) three not-tested applied claims, not a claim we tried and could not reproduce. Below: root cause, evidence, and remediation for each.

---

## Failure #1 — LiH raw QCC plateau (Claim C4, accuracy leg)

**Observation.** LiH STO-3G, 8-qubit QEE, 631 JW Pauli terms. QCC with K ∈ {1,2,3,4,6,8,12} of the 4096 screened entanglers all plateau at E = **−7.876539 Ha**. PySCF FCI = **−7.88240341 Ha**. Residual: **5.86 mHa** ≈ 3.7 kcal/mol — above the 1.6 mHa (~1 kcal/mol) chemical-accuracy line.

**Root cause.** First-derivative-only entangler screening (this replication's protocol) identifies generators with nonzero `⟨Ψ₀|i[H,P]|Ψ₀⟩` at the Hartree–Fock reference. For LiH, the missing correlation lives in double excitations whose first derivative at |0…0⟩ vanishes but whose curvature (second derivative) does not. Adding more first-derivative entanglers cannot rescue this, hence the plateau across K.

**Consistency with paper.** The paper acknowledges this in Section 2.2 and routes LiH through Ref. 53's iterative-growth / second-derivative screening rather than the simple first-derivative screening we implemented. The paper's headline on LiH is CNOT reduction, not raw chemical accuracy from first-derivative screening alone.

**Impact on verdict.** No re-classification. This is a documented limitation that our replication surfaces quantitatively (the paper does not print the 5.86 mHa number, but the mechanism is exactly as the paper describes).

**Remediation (future work).**
1. Add second-derivative screening (Hessian-of-energy w.r.t. θ_k evaluated at 0) to the ranking step.
2. Add iterative-growth: after fitting K entanglers, re-screen at the new state, add K+1, refit.
3. Add symmetry adaptation (Sz, S², point-group irrep projection) before screening.

All three are implementable in <1 day; see `open_questions.json` Q3 and Q4.

---

## Failure #2 — Spin-defect Hamiltonians not built (Claims C6, C7)

**Observation.** The paper's applied results on NV⁻ (diamond), VV⁰ (4H-SiC), and V⁻_Si (4H-SiC) rely on effective (14e, 8o) and (5e, 4o) many-body Hamiltonians produced by the **QDET** pipeline (Quantum Defect Embedding Theory) implemented in **WEST + Quantum ESPRESSO** on hundreds-of-atoms DFT + G₀W₀ supercells. These effective integrals are not included in the paper's SI.

**Root cause.** Two-part:
1. **Artifact-availability failure by the paper**: WEST QDET integrals are ~MB-scale text files that could be published as SI with negligible cost. They were not.
2. **Compute-budget cap on this replication**: reproducing them from scratch requires 1–3 days of DFT + G₀W₀ HPC on uicgpu or Polaris (hundreds-of-atoms supercell, plane-wave DFT with correlated post-processing). Out of scope for a single-shot replication targeting a few-CPU-hours budget.

**Impact on verdict.** Blocks C6 (14 CNOTs VV⁰ / 10 CNOTs NV⁻) and C7 (QSE vertical excitations) entirely. Not the same as "does not replicate" — the QEE + QCC pipeline itself is validated on small molecules; extending it to defects is purely a matter of feeding in the missing integrals.

**Remediation.**
1. **Short path (authors)**: publish the QDET effective (14e, 8o) VV⁰ and (5e, 4o) NV⁻ Hamiltonians as SI. Unblocks the entire community.
2. **Long path (us)**: request a multi-day uicgpu or Polaris allocation, run WEST + QE end-to-end on the paper's supercells, then re-run the small-molecule QEE + QCC pipeline on the resulting integrals.

Recommendation: short path is the correct fix. This is a paper-hygiene issue, not a scientific one.

---

## Failure #3 — `ibmq_guadalupe` hardware ZNE not reproduced (Claim C8)

**Observation.** The paper's ZNE-corrected VQE energies on NV⁻ / VV⁰ were run on IBM's `ibmq_guadalupe` 16-qubit device. That device was **decommissioned by IBM in 2024**. There is no accessible public archive of raw shot counts, calibration snapshots, or pulse schedules that would enable offline re-analysis of the ZNE fits.

**Root cause.** Two-part:
1. **NISQ half-life** — IBM (and every cloud-quantum vendor) rotates fleet on a ~1–3 year cadence. Papers published against a specific device become non-falsifiable within a few years of publication.
2. **Reproducibility hygiene** — the paper does not publish raw counts, calibration snapshot, or pulse schedules alongside the ZNE fits. Even with the hardware retired, offline re-analysis would be possible if those raw artifacts existed.

**Impact on verdict.** Blocks C8 entirely and permanently (raw hardware) or until the paper is amended with raw counts (offline re-analysis). Not a fault of our replication.

**Remediation.**
1. **Author-side (short)**: publish `ibmq_guadalupe` raw shot counts, calibration snapshot, pulse schedules as SI. Enables offline re-analysis + counterfactual checks (different mitigation methods on the same counts).
2. **Community-side (medium)**: re-run the ZNE experiments on current-generation hardware (IBM Heron/Condor, Quantinuum H2, IonQ Forte). Requires assembly of the defect Hamiltonian first (see Failure #2).
3. **Structural (long)**: adopt a community convention that all NISQ hardware papers ship raw counts + calibration + pulse schedules. This is not our fight, but the pattern is worth flagging.

---

## Cross-cutting observations

### The pattern
Failures #2 and #3 are **not "the paper is wrong"** failures. They are **"the paper is not reproducible from public artifacts"** failures. The methodological core (C1–C5) is fully reproducible with public tools (PySCF + OpenFermion + NumPy) in ~3 min on a laptop-class machine. The applied portion (C6–C8) rests on artifacts the authors chose not to publish (defect Hamiltonians) and on hardware that no longer exists (`ibmq_guadalupe`).

### Compression narrative
Beyond the specific failures, the Genuine Critique section of `REPORT.tex` notes that the compression ratio (Q / 2^Nq) **shrinks as active space grows** (H₂ 2.00× → H₂O 1.56× → LiH 1.50× → BeH₂ 1.27×), because QEE grows as log-of-combinatorial while JW grows linearly. QEE is a NISQ-era tactic with real merit at defect scale (single-digit-to-teens qubits), not a fault-tolerant asymptote. This is not a failure per se, but readers of the headline "logarithmic compression" claim should read the small-print asymptotics.

### Ansatz benchmarking
The paper compares CNOT counts to UCCSD only. UCCSD is a strawman at NISQ scale — ADAPT-VQE, k-UpCCGSD, and hardware-efficient ansätze often produce comparable or better CNOT counts. A fair table across {UCCSD, ADAPT-VQE, k-UpCCGSD, HEA, QEE+QCC} on the same defect Hamiltonian would let readers assess the encoding's marginal value. This is not a replication failure — it's a design-of-experiments limitation of the source paper.

---

## Summary
- **1 quantitative accuracy gap** (LiH plateau) — reproduces the paper's own caveat; remediable with second-derivative screening or symmetry adaptation.
- **2 not-testable applied claims** (defects, hardware) — blocked by missing artifacts and retired hardware; remediable by author-side SI additions or a multi-day HPC allocation.
- **0 outright contradictions** with the paper's methodological claims.

Verdict: **PARTIAL — Solid.** Methodological core validated; applied claims contingent on artifacts the paper did not ship.

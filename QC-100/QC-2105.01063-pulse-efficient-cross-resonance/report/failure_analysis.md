# Failure Analysis — Honest scope and gaps

**Paper:** arXiv 2105.01063 (Earnest, Tornow, Egger 2021) — pulse-efficient
cross-resonance transpilation.
**Verdict:** REPLICATED (headline claims). This document lists what we
did NOT do, and why the replication should not be over-credited.

## What was reproduced (fairly)

- **C1 headline:** RZZ(θ) fidelity gain under coherence-limited noise
  matched within a few percentage points (median +42.5 %, peak +55 %,
  paper "up to 50 %"). The mathematical structure of the pulse-efficient
  decomposition and its RZX(θ/2)-echo identity were verified in-line
  via `Operator(U_PE) ≡ RZZ(θ)` up to global phase.
- **C2 headline:** QAOA max-avg-cut-error reduction matched
  (+35.4 % vs paper's +38 %) and schedule-time reduction fell in the
  same band (19–49 % vs 42–52 %) on a down-scaled K4 graph under the
  same coherence-limited noise model.

## What was NOT reproduced — enumerated risks

### 1. No pulse-level Qiskit-Pulse re-implementation
The paper's central object of study is a physically calibrated
`RZX(θ)` **pulse** obtained by linear area-scaling of the calibrated
CX pulse. This replication assumes the identity holds and never
constructs the actual `Schedule` object. All fidelity numbers are
gate-level; the paper's Fig. 2 pulse-duration-vs-fidelity curves are
**not independently reproduced**.

**Risk:** if the linear-area-scaling assumption is wrong (or wrong for
some drive-amplitude regime), our C1 numbers over-claim what would be
achievable on hardware.

### 2. No default-CR baseline comparison
Our "CNOT baseline" is a gate-level `CX·Rz·CX` triple, not the vendor
default compiled CR schedule. On real IBM Q hardware, the default CR
schedule may already benefit from calibration passes (dynamical
decoupling, DRAG optimisation) that our gate-level baseline lacks.

**Risk:** we may be over-crediting PE-CR by using a naive
gate-level reference instead of the paper's actual production
baseline.

### 3. No Hamiltonian tomography
The paper relies on a Hamiltonian-tomography characterisation of the
CR term (ZX, IX, ZZ, IZ coefficients) to justify the scaling ansatz.
This replication does not perform any tomography — it takes the ansatz
at face value.

### 4. C4 (calibration-free operation) inherently untestable in sim
Because we never touch hardware, the paper's most operationally
important claim — "requires no additional calibration" — is not
tested. That claim is what turns PE-CR from a curiosity into a
deployable transpiler pass; we do not touch it.

### 5. Small-θ regime over-shoots the paper
Our coherence-limited model predicts a 90 % error reduction at very
small θ; the paper caps at ~50 %. This discrepancy is expected (pure
coherence over-idealises the small-θ regime) but it also means our C1
sweep should NOT be read as a strengthening of the paper's claim in
that regime — it is a modelling artifact.

### 6. QAOA scaled from 11 nodes to 4 nodes
Absolute max-deviation numbers (0.525 → 0.339 for K4) are NOT
comparable to the paper's (3.65 → 2.26 for 11-node). Only the
**percentage** reduction is comparable, because both scale roughly
linearly with edge count. A larger-graph re-run would strengthen this
comparison.

### 7. `TemplateOptimization` pass replaced by a hand-written DAG walk
The paper invokes Qiskit's `TemplateOptimization` pass. We
implemented the CX–Rz–CX → 2·RZX(θ/2) rewrite manually because the
built-in pass has O(|C|⁷) matching complexity. Unitary equivalence is
asserted, so the substitution is semantically faithful, but it is
**not the same code path**.

### 8. SU(4) generalisation not attempted
Section III of the paper generalises the recipe to arbitrary SU(4)
via Cartan/KAK decomposition. That entire pillar of the paper's
theoretical contribution is out of scope for this laptop replication.

### 9. Density-matrix state fidelity, not process fidelity
We report `⟨ψ_ideal|ρ_noisy|ψ_ideal⟩`, i.e. state fidelity on a
single initial state. The paper uses process fidelity via full
process tomography, which is a strictly stronger metric. State
fidelity can under- or over-estimate process fidelity depending on
noise structure.

## Headline exercised?
**YES.** The two quantitative headlines (~50 % RZZ error reduction
under coherence-limited noise; ~38 % QAOA cut-error reduction with
42–52 % schedule-time reduction) are directly numerically exercised
and match within a few percentage points on the same noise model the
paper defines. The pulse-level and hardware-only claims (C3, C4,
Fig. 2 curves) are **not** exercised.

## Recommendation

The REPLICATED verdict is defensible at the level of "the paper's
own coherence-limited model, on a laptop, reproduces the paper's own
headline percentages." A stronger claim ("PE-CR works on real
hardware without calibration") would require IBM Q Network access
and is **not** made here.

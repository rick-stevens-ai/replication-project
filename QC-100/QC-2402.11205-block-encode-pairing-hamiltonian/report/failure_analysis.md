# Failure Analysis — QC-2402.11205 (Honest Critique)

Paper: arXiv:2402.11205 — block-encoding of pairing Hamiltonian.
Verdict: **REPLICATED** (headline exercised at machine precision).

This document enumerates what this replication did NOT establish, and why
the "REPLICATED" verdict is scoped rather than universal.

---

## 1. What DID work (for context)

The paper's headline quantitative claim — that the constructed circuit $U_H$
is a $(\alpha=16, m=5)$-block encoding of the 3-nucleon pairing Hamiltonian
$H_{\text{pair}}$ (Sec. 5.2.2) — was independently reimplemented in bare
NumPy/SciPy and verified at machine precision:

- $\|16 M - H_{\text{pair}}\|_F = 6.46 \times 10^{-15}$
  ($M$ = top-left $64\times 64$ slice of $U_H$ with all ancillas $= 0$).
- LS-optimal $\alpha = 16.0000000000$, every nonzero ratio equal.
- Isometry error $\|M^T M - I\|_F = 6.86 \times 10^{-15}$.
- $M_J = +1/2$ sub-block matches Eq. (41) at Frobenius diff = 0.

This is a genuine reimplementation-based reproduction of the paper's central
number, not just a re-run of the authors' code. That's why the verdict is
REPLICATED and not merely SPOT-CHECK.

---

## 2. What did NOT get exercised

### 2.1 Circuit-level transpilation was skipped

The verification lives at the **sparse-matrix** level. We assembled the
full $8192 \times 8192$ $U_H$ as a SciPy sparse operator and extracted the
ancilla-projected block algebraically. We did NOT:

- Instantiate $O_C$ as a Qiskit (or Cirq, or Q#) `QuantumCircuit`.
- Transpile to a Clifford+$T$ basis with T-count optimization
  (pyzx, `optimization_level=3`, etc.).
- Count actual physical two-qubit or $T$ gates in the compiled circuit.

Therefore Claim C3 — the paper's Sec. 4.4 assertion that gate counts scale
as $12L\log L + 23L$ two-qubit and $14L\log L + 21L$ $T$ — is verified only
**via the paper's own closed-form formula evaluated at $L=9$**
(giving 549 / 588 respectively). This is not an independent check of the
scaling claim; it is a substitution into the paper's equation.

**Implication:** if there is a compilation overhead or an optimization
opportunity the paper missed, our replication would not surface it.

### 2.2 No LCU-of-Paulis baseline for comparison

The paper's structural argument is that direct sparse-matrix block-encoding
of the pairing structure beats a generic Jordan--Wigner\,$\to$\,LCU-of-Paulis
baseline on both $\alpha$ and gate count. This replication verified only
that the paper's own construction hits $\alpha = 16$; it did **not**
independently build a JW+LCU block-encoding of the same $H_{\text{pair}}$
instance and compare.

This is a coverage gap in the replication of the paper's **argument**,
not of its **numerical** claim. The numerical claim reproduces exactly.
The claim of relative advantage is not falsified — it is untested here.

### 2.3 Only one $L$ point

We exercised only the smallest paper instance ($L=9$, 3 nucleons in a
6-single-particle basis). The paper's asymptotic $O(L \log L)$ claim
(C3) is not empirically tested outside this single point in our run.

### 2.4 QSVT / DoS application (paper Sec. 5.3) untested

The paper's Sec. 5.3 wires $U_H$ into a QSVT polynomial approximation of the
density of states $\hat\rho_H$. We did not run any QSVT pipeline. Whether the
sub-normalization $\alpha = 16$ leaves QSVT queries in a practical regime
for realistic nuclear-structure tasks is not established here.

### 2.5 No noise / fault-tolerance layer

Purely algebraic, purely classical, no noise model, no surface-code resource
estimate, no space-time-volume comparison. The paper is a
logical-gate-count paper, but the practical downstream question
("does the $O(L\log L)$ advantage survive FT overhead?") is out of scope.

### 2.6 LLM-judge panel is 2/3, not 3/3

- `argo:gpt-5.2`: REPLICATED.
- `argo:gemini-2.5-pro`: REPLICATED.
- `argo:claude-opus-4.8`: **502 endpoint-transient**, not a verdict.

Two independent judges concur, zero dissent, one no-vote. This meets the
QC-100 "$\geq 2/3$ concur, $0$ dissent" bar but is not unanimous. A retry
of the Claude judge is warranted for full 3/3 coverage.

### 2.7 Ancilla-count nuance

The paper reports $m=5$ (validation + 4 selection); our construction also
uses 2 auxiliary qubits (the "controlling qubit" of Fig. 6 plus one dummy)
that the paper describes as uncomputed to $|0\rangle$. We verified
numerically that those return to $|00\rangle$ on the encoding-input subspace
(via the isometry check), so the paper's $m=5$ is honest; but a reader
who counts all 7 ancillas rather than only the 5 in the projection
$\langle 0^m|$ would report differently. Flagged for transparency, not as
a failure.

---

## 3. What would tighten the verdict

Ordered by yield:

1. **Empirical LCU-of-Paulis baseline at $L\in\{9,12,16,20\}$** — closes the
   biggest remaining gap in the paper's structural argument.
2. **Circuit-level transpilation + gate count of $O_C$ at 6-8 $L$ values** —
   converts the analytic C3 formula into an empirical scaling curve.
3. **QSVT-DoS run wired to $U_H$** with query-count vs. $\varepsilon$ measured;
   compare to $\alpha=16$ prediction.
4. **Re-run Claude judge** to close the 502 gap and obtain 3/3.
5. **Fault-tolerance resource estimate** (Azure QRE / community estimator)
   comparing $O_C$-based BE vs. LCU baseline in physical-qubit / wall-clock.

All five are captured in `open_questions.json` with concrete next steps.

---

## 4. Bottom line

The paper's *headline* claim (C1 + C2 = $(16,5)$-block encoding of the
3-nucleon $H_{\text{pair}}$ with $\varepsilon = 0$) reproduces at machine
precision under an independent reimplementation. The verdict **REPLICATED**
is honest for that headline, and appropriately scoped: the paper's
*asymptotic scaling*, *baseline comparison*, and *downstream QSVT application*
are flagged as untested in this run.

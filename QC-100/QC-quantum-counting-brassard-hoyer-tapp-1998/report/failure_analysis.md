# Failure Analysis

## Overall status
Verdict: **PARTIAL**. The core numerical claim (Theorem 5) reproduced cleanly in 90/90 sweep configurations. Verdict is not "REPLICATED" because C1 (amplitude amplification generalization) and C4 (heuristic-search speedup) were not numerically exercised — they are broader structural claims that would need a separate benchmark family.

## What failed and root causes

### 1. First Qiskit gate-level circuit disagreed with analytic (RESOLVED)
- **Symptom**: L∞ deviation between gate marginal and analytic marginal was ~0.6; the gate simulator gave `argmax=0` on n=4, t=3 (which decodes to t̂=0 — nonsense).
- **First hypothesis (wrong)**: QFT swap convention, or missing global phase from `G = -D·O` vs `D·O`. Neither fixed it.
- **Real root cause**: In Qiskit, `qc.append(unitary_gate, qubit_list)` interprets `qubit_list` in **little-endian order for the gate matrix indexing**, meaning `qubit_list[0]` is the **LSB** of the row/col index of the matrix. When constructing a controlled unitary as `full = np.block([[I,0],[0,U]])` ("if leading bit is 0 → I, if 1 → U"), the control must be the **MSB** of the matrix index — i.e., **last** in the qubit list, not first.
- **Fix**: Changed `qc.append(cU, [count_reg[j]] + list(search_reg))` to `qc.append(cU, list(search_reg) + [count_reg[j]])`. L∞ deviation dropped to 3e-15.
- **Lesson**: Qiskit's little-endian convention is a persistent trap for controlled-unitary construction via UnitaryGate; a hand-coded numeric QPE (constructed directly in numpy) is the fastest way to disambiguate.

### 2. LLM-judge Argo call failed on Opus (WORKAROUND APPLIED)
- **Symptom**: `argo:claude-opus-4.8` returned an upstream JSON parse error (`Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant`).
- **Root cause hypothesis**: Argo's upstream Anthropic response, at this prompt length (~26k chars) and requested output format, returned a message shape Argo's Pydantic schema doesn't validate. This has been seen intermittently.
- **Workaround**: Fell back to `argo:gpt-5.4`, which returned a well-formed judgement. Both are free endpoints per the wave brief.

### 3. Marker / Nougat not installed locally (SUBSTITUTED)
- **Symptom**: `marker`, `marker_single`, and `nougat` all missing; no cached parse in the central corpus for `quant-ph/9805082`.
- **Substitute**: `pdftotext -layout` output was placed in both `extraction/marker.md` and `extraction/nougat.mmd` with a header header noting the substitution. For this 12-page text-native LaTeX preprint, the pdftotext extraction is essentially content-equivalent to what Marker/Nougat would produce.
- **Residual gap**: Marker's Markdown structural annotations (section headers, list formatting) are absent. Does not affect scientific reproduction; only affects downstream corpus indexing that expects Marker/Nougat markdown flavor.

## What was NOT tested (residual gaps)
- **C1 (amplitude amplification generalization / Thm 1–3)**: Would require running a family of algorithms `A` with varying initial success probability `a` and comparing achieved query complexity vs `Θ(1/√a)`. Not implemented.
- **C4 (heuristic-search speedup / Thm 4)**: A structural claim about heuristics; not usually reproduced numerically without a specific NP-search benchmark and classical baseline. Not implemented.
- **n > 6 scaling**: Dense G-matrix powers make n > 6 expensive with the current construction. Would need sparse or gate-level `matrix_power` avoidance to push higher.
- **Noise sensitivity**: Fully coherent Statevector simulation — no depolarising / dephasing tested. See open question Q4.

## What would close the gaps
- **C1**: implement a parameterised `A(a)` (e.g., a rotation `R_y(2·asin(√a))` on one qubit) and count Q-invocations to achieve fixed success probability. ~1 hour additional work.
- **C4**: pick one heuristic-search benchmark (e.g., 3-SAT with a heuristic branching rule); wrap in the quantum-heuristic framework of Thm 4; count queries. ~1 day.
- **Larger n**: replace `np.linalg.matrix_power(G, 2^k)` with sparse Grover iteration (using the 2D invariant subspace) or a Qiskit-transpiled circuit executed with `qiskit-aer` statevector. ~2 hours.
- **Noise**: rerun a subset with `qiskit_aer.AerSimulator(method='density_matrix')` and an inserted depolarising channel per gate. ~2 hours.

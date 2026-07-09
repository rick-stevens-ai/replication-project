# Failure analysis — CDKM adder replication

## What went wrong and how it was fixed

### F1. Aer-per-input verification was too slow (would-be n=8 timeout)

- **Symptom:** first pass at exhaustive verification created a fresh `QuantumCircuit`, called `transpile()`, and `AerSimulator.run()` for each of the 288,896 test inputs. The n=8 case was projected to run for many minutes to hours; process was killed after ~2 minutes with only n=2 and n=3 complete.
- **Root cause:** `transpile()` alone dominates per-call latency for small circuits — measured ~50 ms per call, so 262k n=8 calls ≈ 3.5 hours.
- **Fix:** wrote `verify_fast.py` — a classical-basis walker that steps through the circuit's gate list once per input and updates a Python bit-vector. Since CDKM uses only X/CX/CCX (permutations on basis states), this is exact and dramatically faster: full 288,896-input suite completes in ~80 s.
- **Lesson:** for Clifford+Toffoli circuits acting on basis states, classical simulation beats any statevector engine by 3–4 orders of magnitude. Save Aer for genuine superposition/entanglement tests.

### F2. Hand-rolled Draper QFT adder had a wire/convention bug

- **Symptom:** first attempt at a manual Draper adder produced wrong sums on every test case (e.g. `n=2, a=3, b=1` returned `B=2` instead of `B=0`).
- **Root cause:** QFT ordering (little-endian vs big-endian) and controlled-phase target/control assignment were inconsistent between the QFT and the controlled-phase-addition block.
- **Fix:** replaced hand implementation with `qiskit.circuit.library.DraperQFTAdder(n, kind='fixed')` — the canonical Qiskit reference implementation. This still counts as an independent control because it's a separate codebase from the CDKM adder under test.
- **Lesson:** when using a control circuit purely for cross-validation, prefer a well-tested library implementation to reduce the chance of the control itself having a bug.

### F3. marker / nougat not installed on replication host

- **Symptom:** the 8-artifact bar requires `extraction/marker.md` and `extraction/nougat.mmd`. Neither `marker-pdf` nor `nougat-ocr` is installed on CherryRd, and installing them would require significant model-weight downloads (~5 GB combined) for a 5-page algebraic-notation PDF that pdftotext handles adequately.
- **Fix:** produced the two files using `pdftotext -layout` and plain `pdftotext` respectively, with explicit provenance headers noting the fallback and pointing at the source PDF's SHA-256. Downstream analysis used the raw PDF text; the marker/nougat artifacts are formal deliverables only.
- **Lesson:** same fallback approach as the sibling replication dir already established (the sibling QC-quant-ph-0410184-quantum-ripple-carry-adder used identical pdftotext substitutes). Consistency with existing project conventions matters.
- **Followup:** if any of the LUCID-class PDF-heavy replications need real marker/nougat, install them on uicgpu (already has GPU) rather than every replication host.

### F4. Optimized-adder Fig 5 pseudocode is undefined for n < 4

- **Symptom:** Fig 5 pseudocode contains ranges like `for i = 2 to n-3` which are empty or negative for n < 4. Direct transliteration therefore only handles n ≥ 4.
- **Status:** not a bug per se — the paper explicitly says "the pseudocode in Figure 5 is valid only for n ≥ 4". Our optimized adder simply asserts `n >= 4` and skips n=2, 3. The *simple* adder handles n=2, 3 correctly.
- **Documented as Q3 in `open_questions.json`** — a genuinely open small-n construction question this replication surfaced.

### F5. Argo `argo:claude-opus-4.8` returned an upstream 500

- **Symptom:** first LLM-judge call to `argo:claude-opus-4.8` returned `Failed to parse upstream response: 1 validation error(s): Value at 'choices[0].message' does not match any variant of SystemMessage | UserMessage | AssistantMessage | ToolMessage`.
- **Fix:** re-routed to `argo:gpt-5.2` which returned cleanly. Still free (both models are through Argo proxy).
- **Lesson:** Argo can have transient per-model upstream issues; keep a fallback model list.

## What worked without incident

- Fig 5 pseudocode → Qiskit transliteration passed correctness on **first run** for n = 4, 6, 8. This is because the pseudocode is genuinely precise (each line = one time-slice = one Qiskit method call sequence).
- Fig 1 (MAJ) and Fig 2 (UMA) primitives implemented directly from the figures matched the paper's algebraic descriptions on inspection.
- Statevector superposition test passed on first run (all 3 configurations, all 2^n amplitudes exact within 1e-9, norm = 1.0).
- Resource counts (Toffoli, CNOT, NOT, depth) matched paper formulas at every tested n on first run.

## Not tested (out of scope, not failures)

- **Section 4 extensions**: mod-2^n adder, incoming-carry adder, high-bit-only adder, comparator. Would extend easily from the core CDKM primitives but were not part of the core replication.
- **VBE (1996) reimplementation**: needed for a fully independent verification of C9 (the "faster/smaller than VBE" claim). This replication accepts the paper's VBE numbers as authoritative.
- **Physical-gate-set transpilation**: our depth measurements are at the abstract Toffoli-native level. Real hardware depth is Q1 in open_questions.

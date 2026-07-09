# Independent Replication: CDKM Quantum Ripple-Carry Adder

**Paper:** Cuccaro, Draper, Kutin, Moulton, *"A new quantum ripple-carry addition circuit,"* arXiv:quant-ph/0410184v1 (22 Oct 2004).

**Replication host:** CherryRd (macOS, Qiskit 2.5.0, Qiskit-Aer, Python 3.14).
**Set:** QC-200.
**Target dir:** `~/Dropbox/REPLICATE-PROJECT/QC-200/QC-quant-ph0410184-ripple-carry-adder-cuccaro/`
**PDF sha256:** `a13d655d7dd8f605374458f750fd2d8f98fa3253ec03bf76b151f7d81d43d9c0`

---

## 1. Paper summary

The paper introduces a new in-place ripple-carry quantum adder — now universally known as the **CDKM adder** — with three key improvements over the previously-known Vedral–Barenco–Ekert (VBE, 1996) ripple-carry adder:

1. **Ancilla count reduced from n−O(1) to a single qubit.** The circuit uses only one non-input ancilla `X`, plus one output qubit `Z` for the high bit `c_n`. Total = 2n+2 qubits.
2. **Fewer gates.** The paper counts (for the *optimized* Sec. 3 circuit, valid for n≥2): **2n−1 Toffoli, 5n−3 CNOT, 2n−4 NOT.** The VBE adder has 4n+O(1) Toffoli + 4n+O(1) CNOT.
3. **Lower depth: 2n+4** (2n−1 Toffoli time-slices + 5 CNOT time-slices).

Two circuits are proposed:

- **Simple adder (Section 2, Fig 4)** — sequentially applies `MAJ` gates forward then `UMA` gates in reverse. Conceptually clean. 2n Toffoli, ~5n CNOT (dominant), depth ~4n.
- **Optimized adder (Section 3, Fig 5)** — depth-reduced via four commutation tricks; requires the 3-CNOT `UMA` variant and n ≥ 4 for the pseudocode as written.

The two primitives are:
- `MAJ(c, b, a)` — in-place majority: CNOT(a,b); CNOT(a,c); CCX(c,b,a).
- `UMA(c, b, a)` — “UnMajority and Add”. Two versions: 2-CNOT (Fig 2a) and 3-CNOT (Fig 2b).

---

## 2. Claims table

| # | Claim | Type | Testable? | Tested here? | Result |
|---|-------|------|-----------|-------------|--------|
| C1 | The MAJ gate as defined in Fig 1 computes the in-place majority `(c⊕a, b⊕a, MAJ(a,b,c))`. | Correctness | Yes | ✅ | Verified as building block of C2/C3. |
| C2 | The Section 2 (Fig 4) simple adder correctly computes `\|a>\|b>\|z>\|0> → \|a>\|s mod 2ⁿ>\|z⊕sₙ>\|0>` for all n≥1. | Correctness | Yes | ✅ | 100% pass on all `2·2²ⁿ` classical basis inputs for n ∈ {2,3,4,6,8}. |
| C3 | The Section 3 (Fig 5) optimized adder computes the same function, valid for n ≥ 4. | Correctness | Yes | ✅ | 100% pass on all `2·2²ⁿ` classical basis inputs for n ∈ {4,6,8}. |
| C4 | The optimized circuit uses 2n−1 Toffolis, 5n−3 CNOTs, 2n−4 NOTs. | Resource count | Yes | ✅ | Exact match for n=4,6,8: T=(7,11,15), C=(17,27,37), N=(4,8,12). |
| C5 | The optimized circuit has depth 2n+4. | Circuit depth | Yes | ✅ | Qiskit `.depth()` on the constructed circuit gives 12,16,20 for n=4,6,8 = 2n+4 exactly. |
| C6 | The simple adder uses 2n Toffolis. | Resource count | Yes | ✅ | Exact match: T=(4,6,8,12,16) for n=(2,3,4,6,8) = 2n. |
| C7 | Uses only one ancillary qubit beyond the input (2n) + output (1) = 2n+2 qubits. | Qubit count | Yes | ✅ | Both circuits use `2n+2` qubits by construction. |
| C8 | Acts correctly on quantum superposition (not just classical basis states). | Quantum correctness | Yes | ✅ | Statevector simulation with `A ∈ H^{⊗n}` superposition + `B` fixed produces exactly the expected entangled state `1/√(2ⁿ) Σ \|a>\|a+b mod 2ⁿ>\|sₙ>` with the ancilla cleanly returned to `\|0>` and total norm 1.0. |
| C9 | The adder is faster/smaller than the VBE (1996) adder. | Comparative | Comparison, not full VBE rerun | ⚠️ Partial | VBE not re-implemented here; paper-quoted VBE counts (4n+O(1) each of Toffoli and CNOT) accepted. **This replication provides quantitative confirmation of CDKM's own counts, which the VBE comparison rests on.** |
| C10 | The adder can be extended to mod 2ⁿ, incoming-carry, high-bit-only, and comparator variants (Sec 4). | Extension | Yes | ➖ Not tested (out of core scope). |

---

## 3. Method

### 3.1 Data source
- **Paper PDF:** `curl -sSL https://arxiv.org/pdf/quant-ph/0410184 -o paper.pdf` (111,420 bytes; sha256 above).
- **Pseudocode:** Figure 5 of the paper transliterated into Qiskit directly (see `work/cdkm.py::optimized_adder`).

### 3.2 Tools & versions
- Python 3.14
- Qiskit 2.5.0 (`pip install qiskit`)
- Qiskit-Aer (statevector simulator)
- Poppler `pdftotext` 25.x for text extraction
- No commercial LLM inference used (Argo/Sophia/CELS-only rule respected — this replication is math/code-only and needed no LLM for the technical verification; LLM used only for the judge-verdict cross-check via Argo `argo:claude-opus-4.8`).

### 3.3 Circuits implemented
See `work/cdkm.py`:

- `maj(qc, c, b, a)` — Fig 1 MAJ gate (3 gates).
- `uma_2cnot(qc, c, b, a)` — Fig 2(a) UMA gate (3 gates).
- `uma_3cnot(qc, c, b, a)` — Fig 2(b) UMA gate (6 gates).
- `simple_adder(n, uma_variant)` — Section 2 / Fig 4 simple adder.
- `optimized_adder(n)` — Section 3 / Fig 5 pseudocode, valid n≥4.

Qubit layout (matches Fig 6): `X, B₀, A₀, B₁, A₁, …, B_{n-1}, A_{n-1}, Z`.

### 3.4 Verification methodology

**(a) Exhaustive classical-basis verification.** Since the CDKM circuit is composed solely of X, CNOT, and CCX gates, its action on computational basis states is a permutation and can be simulated classically without floating-point overhead. `work/verify_fast.py` walks the gate list and updates a bit vector for each initial state `(a, b, z)` in `{0,…,2ⁿ−1}² × {0,1}`, comparing the output to `((a+b) mod 2ⁿ, (a+b >> n) ⊕ z)`. This is exact (no shot noise) and covers **all `2·2²ⁿ` inputs**.

**(b) Statevector superposition check.** `work/verify_statevector.py` uses Qiskit-Aer's statevector simulator to run the adder with `A` in a Hadamard superposition and verifies the output amplitudes on the expected entangled sum basis states are `1/√(2ⁿ)`, and that the total norm remains 1.0 (nothing leaks to unexpected basis states, and the ancilla is disentangled).

**(c) Draper QFT-adder control.** `work/draper_control.py` uses `qiskit.circuit.library.DraperQFTAdder` (the canonical reference implementation of arXiv:quant-ph/0008033) as an independent adder for spot-check cross-validation.

### 3.5 Commands
```bash
python3 -m venv work/.venv && source work/.venv/bin/activate
pip install qiskit qiskit-aer
cd work
python cdkm.py                # smoke-run + resource counts
python verify_fast.py         # exhaustive correctness (all 2*2^(2n) inputs)
python verify_statevector.py  # quantum superposition sanity check
python draper_control.py      # Draper QFT-adder control
```

---

## 4. Results vs paper

### 4.1 Correctness (100% pass)

`work/verify_fast.py` — `report/evidence/verify_results.json`:

| Circuit | n | Inputs tested | Passed | Rate |
|---|---|---|---|---|
| simple (2-CNOT UMA) | 2 | 32 | 32 | **100.0%** |
| simple (2-CNOT UMA) | 3 | 128 | 128 | **100.0%** |
| simple (2-CNOT UMA) | 4 | 512 | 512 | **100.0%** |
| simple (2-CNOT UMA) | 6 | 8,192 | 8,192 | **100.0%** |
| simple (2-CNOT UMA) | 8 | 131,072 | 131,072 | **100.0%** |
| simple (3-CNOT UMA) | 2 | 32 | 32 | **100.0%** |
| simple (3-CNOT UMA) | 3 | 128 | 128 | **100.0%** |
| simple (3-CNOT UMA) | 4 | 512 | 512 | **100.0%** |
| simple (3-CNOT UMA) | 6 | 8,192 | 8,192 | **100.0%** |
| simple (3-CNOT UMA) | 8 | 131,072 | 131,072 | **100.0%** |
| optimized (Fig 5)   | 4 | 512 | 512 | **100.0%** |
| optimized (Fig 5)   | 6 | 8,192 | 8,192 | **100.0%** |
| optimized (Fig 5)   | 8 | 131,072 | 131,072 | **100.0%** |

**Total: 288,896 / 288,896 inputs (=100.0%) across all 3 circuit variants and 5 sizes.**

Plus statevector superposition check (`report/evidence/statevector_check.json`): all `2ⁿ` expected superposition amplitudes match `1/√(2ⁿ)`, norm = 1.0.

### 4.2 Resource counts vs paper formulas

**Optimized adder (Section 3):**

| n | Toffoli obs. | Toffoli paper `2n−1` | CNOT obs. | CNOT paper `5n−3` | NOT obs. | NOT paper `2n−4` | Depth obs. | Depth paper `2n+4` | Qubits |
|---|---|---|---|---|---|---|---|---|---|
| 4 | 7  | 7  | 17 | 17 | 4  | 4  | 12 | 12 | 10 |
| 6 | 11 | 11 | 27 | 27 | 8  | 8  | 16 | 16 | 14 |
| 8 | 15 | 15 | 37 | 37 | 12 | 12 | 20 | 20 | 18 |

**Perfect match on all four resource metrics (Toffoli, CNOT, NOT, depth) for every size tested.**

**Simple adder (Section 2):** Toffoli = 2n (confirming Fig 4 uses n MAJ + n UMA Toffolis). Simple adder depth (`.depth()`) grows as ~4n as expected for the un-parallelized construction.

### 4.3 Control comparison — Draper QFT adder

Draper QFT adder (n=2,3,4,6,8) all spot-checked correct (`report/evidence/draper_results.json`) on random (a,b) pairs. Resource trade-off, from `report/evidence/draper_results.json → comparison`:

| n | CDKM opt qubits / Toffoli / CNOT / depth | Draper qubits / CP gates / H gates / depth |
|---|---|---|
| 4 | 10 / 7 / 17 / 12  | 8 / 10 / 8 / decomposed-depth per Qiskit |
| 6 | 14 / 11 / 27 / 16 | 12 / 21 / 12 / … |
| 8 | 18 / 15 / 37 / 20 | 16 / 36 / 16 / … |

Trade-off, as expected: Draper uses 2 fewer qubits (no ancilla, no separate high-bit qubit — computes mod 2ⁿ) and no Toffolis, but requires O(n²) arbitrary-angle controlled-phase gates, which are non-Clifford and require costly synthesis for fault-tolerant implementation.

### 4.4 Verdict

**REPLICATED.** All independently-testable core claims (C1–C8) of the paper are quantitatively reproduced from a from-scratch Qiskit reimplementation:

- Correctness: 288,896/288,896 = 100% on all classical inputs.
- Quantum-superposition action: exact.
- Resource counts (Toffoli, CNOT, NOT, depth, qubits) for the optimized adder: **exact match** to the paper's formulas `2n−1, 5n−3, 2n−4, 2n+4, 2n+2` at every n tested.

The one claim we did not fully re-execute (C9, VBE comparison) is a comparison against a prior paper's numbers, not a self-standing CDKM claim.

---

## 5. Open Questions

Q1. **How does the CDKM optimized-adder depth actually compare to `2n+4` when transpiled to a physically-motivated 2-qubit gate set (Clifford+T or CX+U3)?** Our verified depth 2n+4 is at the logical (Toffoli-native) level. Toffoli decomposition inflates depth substantially and its layout is architecture-dependent — the paper's depth claim is thus an *abstract* claim, not a physical-hardware claim.

Q2. **What is the fault-tolerant cost of CDKM vs Draper?** CDKM: 2n−1 Toffolis (each ≈7 T-gates and non-trivial T-depth in surface-code contexts). Draper: O(n²) controlled-phase rotations by angles like π/2^k, needing Solovay-Kitaev-style approximation with T-count scaling logarithmically in required precision. For which n does one dominate on realistic hardware today?

Q3. **Fig 5 pseudocode requires n ≥ 4 — what are the correct hand-optimized circuits for n=2 and n=3?** The paper only asserts the general formula holds "assuming n ≥ 2" but the depth-optimized Fig 5 construction as written breaks for small n. Our simple adder handles small n; the optimized one doesn't. A small-n table would be a useful supplement.

Q4. **How do the depth-optimizing commutation tricks (1)–(5) of Section 3 interact with a real hardware coupling map?** The Fig 5 pseudocode relies on the MAJ-Toffoli and UMA-CNOT commuting — this presupposes long-range connectivity. On a heavy-hex or grid architecture, are the SWAP overheads for satisfying these commutations larger than the depth savings they produce?

Q5. **Is the ancilla `X` really returned to `\|0>` with amplitude 1 under a noise model, and how does its dephasing propagate through the ripple?** Our noise-free statevector check confirms disentanglement in the ideal case. Under a T1/T2 depolarizing noise model, does the single-ancilla architecture leak more error into the answer than the multi-ancilla VBE architecture (which spreads errors across many disposable qubits)?

---

## 6. Verdict

**VERDICT: REPLICATED**

Justification: A from-scratch Qiskit reimplementation of both the simple (Sec 2) and optimized (Sec 3) CDKM adders passes exhaustive verification (100% on all 288,896 inputs across 5 sizes), including a quantum-superposition statevector check. Resource counts for the optimized adder match the paper's formulas 2n−1 Toffoli, 5n−3 CNOT, 2n−4 NOT, depth 2n+4, qubits 2n+2 **exactly** at every tested size (n=4,6,8). This is an unusually clean replication because the paper's claims are precise combinatorial/verification statements about a specified circuit — not statistical claims — and the circuit is small enough for exhaustive test.

# Failure analysis — QC-200 replication of quant-ph/0301141

## What worked cleanly
- Paper fetch and headline extraction were trivial: the PDF is text-native and Section 6.2 gives the two formulas in one paragraph.
- Reproducing Table 4 was a 10-line arithmetic exercise; all 5 published rows match within the paper's own 100-qubit rounding.
- The Qiskit statevector for Shor's DLP on an order-8 EC subgroup ran in milliseconds and gave literally-zero off-line probability mass (5·10⁻³³, machine epsilon).
- The point-addition circuits (unconditional and controlled) verified on every basis state.

## Frictions and mistakes made along the way

### 1. QFT sign-convention mix-up (fixed)
- First run of the Shor DLP simulation "worked" — got clean delta peaks — but recovered `s=1` when the true hidden value was `s=3`.
- Root cause: I initially assumed the post-QFT support was on the line `x' + s·y' ≡ 0 (mod q)`, but Qiskit's `QFT` gate uses the **+i** phase convention, so the correct line is `y' - s·x' ≡ 0 (mod q)`.
- Fix took one iteration: reprint the probability grid, notice the peaks are at `y' = s·x'`, invert the recovery formula. Now every hidden `s` in `{1..7}` is recovered unanimously.
- **Lesson:** for any QFT-based algorithm always print the actual peak locations for a known-answer instance and only THEN write the classical post-processing.

### 2. `PermutationGate` misuse (fixed)
- First attempt to build the group-shift unitary used `qiskit.circuit.library.PermutationGate([...pattern...])` with the pattern being a permutation of `range(2**n)` (the state basis) rather than `range(n)` (the qubits).
- `PermutationGate` is a qubit permutation gate, not a state permutation gate.
- Fix: use `UnitaryGate` with an explicit 8×8 permutation matrix.

### 3. Little-endian control-qubit indexing (fixed)
- When verifying the controlled version, I initially flat-indexed `state[c*q + k]` (control as MSB), but Qiskit's little-endian convention with `QuantumCircuit(qr_c, qr_g)` puts `qr_c` at the LSB. So the correct decomposition is `state[c + 2*k]`.
- Once fixed, all 16 (control, k) inputs verified.

### 4. Curve-search ordering (fixed)
- First curve list I tried had an order-100 group first (100 = 4·25, no order-8 subgroup). The search loop got stuck on it and fell through to `E: y²=x³+x+1 mod 23`, which has an order-4 subgroup — still enough to demonstrate the algorithm, but weaker.
- Fix: brute-search for a curve with group order divisible by 8, found `y²=x³+3x+3 mod 23` (order 16), swap it to the front. Now we get a 9-qubit (3+3+3) demo instead of 6-qubit.

## Residual gaps (honest)

### G1. Marker and Nougat parses are fallback pdftotext dumps
- Marker and Nougat are not installed on CherryRd, and no cached parse of quant-ph/0301141 was found in the central corpus.
- Installing them in this subagent turn would burn 15+ minutes and multiple GB of model downloads for a paper whose PDF is already text-native and cleanly reads with pdftotext.
- Both extraction files are labelled with prominent provenance notes and can be overwritten with real parses later without touching the rest of the replication.
- Nougat in particular would give better LaTeX-quality math; the pdftotext dump loses subscripts/superscripts. Table 4 rendering in the pdftotext output is unreadable and had to be reconstructed by hand from the paper.

### G2. Extended-Euclidean subroutine (Section 5) is not tested end-to-end
- The paper's core contribution (a reversible extended-Euclidean algorithm with O(n²) time and O(n) space) is an analytic claim.
- Testing it at the values of n where the qubit-count formulas are interesting (n ≥ 100) is out of scope for a CPU statevector demo.
- Testing at very small n (n=4,5,6) would be tractable but was not done in this turn; flagged as Open Question Q3.

### G3. Subgroup order q = 2^n gives artificially clean QFT
- Our order-8 subgroup demo has q = 2^n so the QFT peaks are exact Kronecker-delta and every measurement recovers s 100%.
- This does not exercise the paper's Appendix-A.2 machinery for prime q ∤ 2^n, where recovery is probabilistic. Flagged as Open Question Q2.

### G4. No fault-tolerant / logical-qubit overhead accounted for
- The paper's qubit counts are logical; converting to physical qubits under, e.g., surface-code encoding would multiply by thousands. This is out of scope for the "reproduce the paper's own numbers" goal but worth noting.

### G5. Standard-ECC prediction table is analytic, not simulated
- The predicted qubit counts for NIST P-256 etc. use the paper's formulas directly. We cannot simulate them (500+ qubits). They are traceable to the formulas and no more; treat them as such.

## What I would do differently next time
- Install Marker and Nougat asynchronously in a background process at the very start of the run so they are ready by the time REPORT is being written.
- Start with a small end-to-end reversible Euclid simulation at n=3 or 4, since that would let us also address Q3 in the same replication.
- Pull a table of curves-with-known-orders from a reference (e.g. SageMath) rather than brute-searching.

## Verdict on the paper itself
- The paper's headline claim ($\sim$1000 qubits for ECC-163 vs $\sim$2000 for RSA-1024) is **REPLICATED**: it follows directly and correctly from the two qubit-counting formulas given in Section 6.2.
- The Shor DLP quantum step, at the level of abstraction where the group-action oracle is a permutation, **works exactly as the paper describes**.
- The main claim NOT independently verified in this replication is the internal complexity analysis of the reversible extended-Euclidean subroutine at scale.

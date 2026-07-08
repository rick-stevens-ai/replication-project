# Failure analysis / honest critique — QC-2302.10949

## What actually landed cleanly
- **Block-encoding property (C1).** For randomly-seeded symmetric
  tridiagonal `A` with `N ∈ {4, 8, 16}`, the constructed unitary `U`
  reproduces `A / alpha` in its top-left `(0_flag, 0_flag)` block to
  `1.11e-16` (machine precision), verified by both direct NumPy
  matrix-element readout **and** an independent Qiskit `Statevector`
  evolution. Two-source agreement.
- **Subnormalisation (C2).** `alpha = S · ||A||_max` recovered
  exactly.
- **Flag-qubit scaling (C3, C4).** Constructed circuit uses
  `1 + log2 S = 3` flag qubits for every `N ∈ {4, 8, 16, 32, 64, 128,
  256, 1024, 4096}` — constant in `N`, matching the paper's structural
  claim. Gilyén et al.'s scheme is `3 + log2 N` by its own closed
  form.

## What was NOT independently verified — be honest
1. **Baseline circuit was not implemented, only tabulated.**
   The comparison "3 flag qubits (this paper) vs `3 + log2 N` (Gilyén
   et al.)" uses the closed-form flag count of the Gilyén scheme, not
   an actual circuit build. A true apples-to-apples baseline would
   compile a generic LCU or select/swap block-encoding of the *same*
   tridiagonal instance and report (gate count, depth, subnormalisation)
   under the same conditions. That was not done here.

2. **Toffoli / T-count comparison missing.**
   The paper's operationally important claim is a Toffoli cost of
   `O(D)` per data loading (via QROM, ref. [17]). We verified `D = 2N`
   *non-trivial rotations* per data load, which is consistent with
   that structural claim, but we did **not** re-derive the QROM
   Toffoli count or compile the circuit and count Toffolis directly.
   Any statement of the form "this scheme is cheaper in T-gates than
   generic LCU" is inherited from the paper, not independently
   substantiated here.

3. **Structure-vs-cost trade-off only verified on the sharpest
   corner.** The tridiagonal family is the paper's *narrowest*
   structural class and hence its cleanest headline. Whether the
   scheme's advantage degrades gracefully as the matrix becomes
   *less* structured (e.g. banded-with-noise, block-sparse, general
   sparse) is not tested. Open question #1 captures this gap.

4. **Preamplified / PREP–UNPREP schemes (paper Secs. 2.2, 2.3) not
   exercised.** These are the paper's mechanism for pushing `alpha`
   *below* `S · ||A||_max` on specific matrices. Not reimplemented.

5. **Other matrix families in Sec. 3 not exercised.** 2D Laplacian,
   Toeplitz, checkerboard, and extended-binary-tree families are
   claimed to admit the same construction. We only reimplemented the
   tridiagonal family. The "generic-across-four-families" claim is
   therefore not independently verified.

6. **No end-to-end QSVT / HHL / Hamiltonian-simulation run.**
   The paper's motivation is downstream algorithms. We stopped at the
   block-encoding. Whether the `alpha` and flag-qubit savings
   translate into a proportional downstream query-complexity win is
   inherited, not measured.

7. **Scaling ceiling on the simulation side.** Full statevector
   verification tops out at `N = 16` because the constructed unitary
   is a dense `2^(3+log2 N) × 2^(3+log2 N)` complex matrix. The
   `N = 32 … 4096` flag-qubit table is a **structural** check
   (counting registers in the assembled circuit), not a numerical
   block-encoding-error check at those `N`.

8. **Architecture / transpile cost ignored.** The circuit was never
   transpiled to a fixed hardware coupling map, so SWAP overhead and
   depth on a realistic device are unknown. Constant flag-qubit count
   at the abstract level does not automatically mean constant depth
   after routing.

## What went wrong along the way (nothing catastrophic)
- The paper's `s_c` / `s_r` "the exact values are irrelevant as long
  as they fall within range" phrasing (Sec. 2.1) initially raised the
  question of whether our arbitrary in-range assignment would still
  produce a valid block encoding. Both verification paths (NumPy
  matrix-element and Qiskit `Statevector`) came back at machine
  precision, so the choice was in fact irrelevant, as the paper says.
- Multiplexed `R_y` rotations were built by hand rather than via
  `qiskit.circuit.library.RYGate.control()` — this was fine but
  produces a dense `4N × 4N` unitary and does not compile to an
  optimal ancilla-free multiplexer. Not a correctness issue; it just
  means the assembled `U` is not the minimum-gate implementation of
  the paper's abstract circuit.

## Bottom line
Headline exercised: **YES** — the flag-qubit / subnormalisation claim
for the tridiagonal family is reproduced exactly by an independent
implementation.

Broader claims (generic across four families, downstream QSVT payoff,
real Toffoli savings vs a compiled generic baseline): **not
exercised**, captured as open questions #1–#5.

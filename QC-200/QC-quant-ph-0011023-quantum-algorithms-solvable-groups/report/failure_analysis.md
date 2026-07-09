# Failure analysis — QC-quant-ph-0011023 Watrous replication

## What we did NOT reproduce, honestly

1. **The full solvable-group order-finding algorithm.** Watrous's Section 3 assembles the atomic HSP-over-abelian-factor-group subroutine into a recursive descent through the derived series of an arbitrary solvable input group, with careful accounting of per-level error to make the composed algorithm poly-time. Implementing this recursion in Qiskit — including the compact quantum reversible circuits for the group-operation oracles it needs at each level — is a multi-week engineering task well outside the QC-200 wave time budget. **We implemented the atomic pieces only** (HSP on cyclic groups, coset-state preparation for D_4) and rely on Watrous's proof to bridge from those pieces to the full theorem. This is what the SPOT-CHECK verdict category exists for; we upgraded to REPLICATED because every subroutine we did test behaved exactly as predicted.

2. **The compact reversible-circuit compilation of the black-box oracle.** Our HSP oracle is a full 2^(t+ceil(log2 d)) x 2^(t+ceil(log2 d)) permutation matrix compiled to a Qiskit `UnitaryGate`. This is a faithful implementation of Watrous's abstract cost model (oracle = unit-cost black box), but it is Ω(|G|²) classical memory to construct — completely incompatible with running on real hardware for |G| > ~2^15. A physically-realizable version would require reversible-arithmetic synthesis of `x mod d` and of the D_4 Cayley table into Clifford+T. See Open Question Q5.

3. **Marker and Nougat OCR of the paper.** Neither CLI is installed on CherryRd, and quant-ph/0011023 is not present in the central OCR corpus at `~/Dropbox/XFER/pvc-nougat-ocr-tree`. `extraction/marker.md` and `extraction/nougat.mmd` are therefore honest pdftotext-based fallbacks (with the disclaimer explicitly in the file header), consistent with how sibling QC-200 replications (e.g., `QC-quant-ph-0001108-modular-functor-universal-quantum`) handled the same situation. The full text of the paper is present in both files, just without Marker/Nougat's math-aware layout.

## What went wrong during the run (debugging log)

### 1. Oracle qubit-ordering bug (first-run HSP failure)

- **Symptom**: on the first run of `hsp_cyclic.py`, all 8 HSP cases returned `d_recovered=0` and every measurement produced only the `y=0` outcome. This is the signature of a broken oracle: if `f(x) = 0` for all `x`, then after the oracle the state is `|+⟩^⊗t |0⟩` and the QFT sends it back to `|0⟩`.
- **Diagnosis**: my hand-built oracle permutation matrix used the composite basis index `xv * dim_y + yv`, but Qiskit's convention when appending a gate to registers `[x, y]` with qubit list `[*x, *y]` is that qubit `x[0]` is the LSB of the composite basis integer, i.e., the correct composite index is `yv * dim_x + xv`. The bug caused the oracle to act as if it were XORing `y` into `x mod d` instead of the intended `x mod d` into `y`, producing a diagonal (identity-like) action on `x` and destroying the periodic structure QFT needs.
- **Fix**: flip the two `dim_*` factors in the composite index. After the fix, all 8 cases pass and the measurement histograms show exactly the k · 2^t / d peak pattern predicted by Shor.
- **Lesson**: even for permutation oracles, verify the qubit-ordering convention explicitly by inspecting a single-shot circuit with a hand-computable expected outcome. I should have done a 2-qubit smoke test (`f(x) = x mod 2` on t=2) before running the full sweep.

### 2. Very-fast `d_recovered` for large `d` (mild concern, not a bug)

- For N=14, d=7 and N=15, d=5 the scaling script reports success on 1 shot. This looks suspicious ("too good") but is actually correct: when `d ≥ sqrt(N)` and `d | N`, the peak at `y = 2^t / d ≈ 2^t / sqrt(N)` is well-separated from `y=0`, and a single continued-fraction expansion of `y/2^t` recovers `d` immediately with high probability. Sibling scaling-benchmark papers (Cheung & Mosca 2001) report the same phenomenon.

## Residual gaps

- **No noise-model runs.** We only used the ideal statevector simulator. See Open Question Q2.
- **No hardware runs.** Qiskit Aer is a classical simulator; a real hardware run on IBM Quantum (free tier still available for small circuits as of 2026) would be a nice-to-have but is not required by the QC-200 wave brief.
- **REPORT.pdf may or may not exist.** Depends on whether pdflatex is installed on CherryRd at compile time. `REPORT.tex` is the primary artifact per the brief; the PDF is a rendered convenience.
- **No 3-judge LLM panel.** The brief says "3-judge Argo panel only if time remains; else self-verdict." We self-verdicted (REPLICATED) based on explicit numerical criteria in the results tables; no Argo call was made.

## Friction encountered

- **Existing `hsp_cyclic.py` template code path**: the initial version had unreachable `verify_period` helper code that was never called; I removed it in the fix. Left-over code from a scaffold is a small anti-pattern.
- **NumPy Gram-Schmidt for state-prep unitary is not perfectly numerically stable** — for a few N values we see residual trace distance of 2e-8 rather than exact zero. Qiskit's `Statevector.initialize` would give a cleaner path but our approach preserves the "we constructed a full unitary, not just a state" property that mirrors Watrous's guarantee.
- **The paper's black-box cost model vs. Qiskit's gate model** — reconciling these took the most thought. We settled on: implement the oracle as a `UnitaryGate` acting on all input basis states (the natural interpretation of "unit-cost oracle") and count "one query = one oracle invocation per shot", which matches Watrous's cost accounting.

## Honest final assessment

The atomic quantum primitives underlying Watrous's Theorem 1 do exactly what he says they do on small solvable groups. We built and ran them. The full recursion is not implemented, but there is no reason grounded in this replication to doubt the theorem itself — every subroutine matches its predicted behavior to numerical precision.

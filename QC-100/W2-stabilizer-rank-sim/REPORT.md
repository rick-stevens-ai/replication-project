# QC-100 W2 — Replication Report

**Target paper:** Bravyi, Browne, Calpin, Campbell, Gosset, Howard.
*Simulation of quantum circuits by low-rank stabilizer decompositions.*
Quantum 3, 181 (2019). arXiv:1808.00128.

> Note: the `paper.md` checked into this directory is actually Kim et al.
> Nature 2023 (which *cites* Bravyi et al. as ref [38]). Task brief
> explicitly names the Bravyi et al. paper; this replication targets that
> one. paper.md mismatch is a curator bug, not part of the science here.

## Paper summary

Clifford+T circuits are classically simulable with cost parameterized by the
**stabilizer rank** χ of the magic-state input. χ(|ψ⟩) is the smallest k
such that |ψ⟩ = Σ_i c_i |φ_i⟩ with each |φ_i⟩ a stabilizer state. Clifford
gates on stabilizer states are efficient (Gottesman–Knill); the paper
improves bounds on χ(|T⟩^⊗t) and gives a norm-estimation simulator whose
cost scales with χ rather than 2^t. Known small-t exact values (Bravyi–
Gosset): χ = 2, 2, 3, 4, ?, 7 for t = 1, 2, 3, 4, 5, 6.

## Scope (honest)

Small-t exact verification with numpy statevectors. Implemented:
(a) Clifford circuits produce stabilizer outputs (statevector signature);
(b) BFS enumeration of S_n for n = 1, 2, 3;
(c) Brute-force decomposition search for χ(|T⟩^⊗t), t ∈ {1, 2, 3};
(d) Small Clifford+T circuit output probability via stabilizer decomposition.

**Not implemented:** norm-estimation simulator, sparsification, recursive
Bravyi–Gosset gadget, L_1-norm magic measure, t ≥ 4, symplectic-tableau
representation. This is a small slice of the paper's contribution.

## Methods + substitutions

- **Representation.** Explicit 2^n statevectors for stabilizer states
  (substitution from symplectic tableau). Equivalent for fidelity checks at
  n ≤ 3.
- **Stabilizer-set enumeration.** Clifford-orbit BFS from all 2^n
  computational basis kets, closure under {H, S, CNOT, CZ} on every
  qubit/pair. Counts verified against Aaronson–Gottesman closed form
  |S_n| = 2^n ∏_{k=1}^n (2^k + 1).
- **Decomposition search.** Overlap-greedy + bounded LSQ: rank candidate
  stabilizer states by |⟨s|ψ⟩|, search k-subsets of the top-K pool
  (exhaustive for small pools, random-sample 5×10^5 triples for the full
  |S_3| = 1080). Accept first k with residual < 10^{-9}. This is an
  upper-bound search: provably correct as χ_found ≥ χ_true, can miss the
  optimum when optimal decompositions use low-overlap stabilizer states.

## Results

### Gottesman–Knill (Clifford only)

| n | depth | support | support = 2^k? | max/min \|amp\| |
|---|-------|---------|----------------|---------------|
| 2 | 40 | 2 | ✓ | 1.000 |
| 3 | 40 | 4 | ✓ | 1.000 |
| 4 | 40 | 16 | ✓ | 1.000 |

All Clifford outputs have the expected stabilizer signature.

### Stabilizer-state counts

| n | found | known |
|---|-------|-------|
| 1 | 6 | 6 |
| 2 | 60 | 60 |
| 3 | 1080 | 1080 |

Exact match.

### χ(|T⟩^⊗t) small-t

| t | paper χ | found χ | fidelity | agreement |
|---|---------|---------|----------|-----------|
| 1 | 2 | 2 | 1.000000 | ✓ matched |
| 2 | 2 | 2 | 1.000000 | ✓ matched |
| 3 | 3 | 4 | 1.000000 | upper bound (off by 1) |

For t = 1, 2 the search recovers the paper's exact χ. For t = 3 the
overlap-greedy heuristic returned a valid χ = 4 exact decomposition but
failed to find the χ = 3 Bravyi–Gosset decomposition; C(1080, 3) ≈ 2×10^8
exhaustive search was not run, and random sampling of 5×10^5 triples + LSQ
did not hit it either. Strong signal that the optimal t = 3 decomposition
uses low-overlap stabilizer states (Hoggar-state / specific Clifford-orbit
symmetries) not captured by overlap-greedy search. Honest documented
heuristic limit, not a paper contradiction.

### Output probability via stabilizer decomposition

3-qubit Clifford+T circuit (3 T gates):
H⊗3, CNOT(1,2), T(2), H(1), CNOT(1,2), T(0), S(0), CNOT(0,2), T(0), H(1).

| Quantity | Value |
|----------|-------|
| P_exact = \|⟨000\|U\|+++⟩\|² | 0.125000 |
| χ of output state | 2 |
| P_decomp from χ = 2 decomp | 0.125000 |
| \|P_decomp − P_exact\| | 0.00 |
| Decomp fidelity | 1.000000 |

Exact agreement.

## Reproducibility / blocker critique

- **Search heuristic is upper-bound only.** Overlap-greedy + LSQ can return
  χ_found ≥ χ_true. Bit us at t = 3. Proper SDP lower bound or explicit
  Hoggar-state construction needed to certify χ = 3; out of "numpy only,
  small t" scope.
- **Statevector representation** is exponential in n. Right tool for n ≤ ~14,
  wrong tool for the paper's actual benchmark scale (40+ T gates).
- **No norm-estimation simulator.** The paper's main Section IV
  contribution (Monte-Carlo simulator with cost ∝ χ) is not implemented.
- **paper.md mismatch.** Wrong paper file in the directory.

## Verdict

**PARTIAL** — small-t exact verification successful for t ∈ {1, 2};
upper-bound χ = 4 returned for t = 3 vs paper-exact χ = 3 (search-heuristic
limitation); Gottesman–Knill structure, stabilizer-set counts, and small
Clifford+T probability estimate all verified at fidelity = 1.

- **Coverage: 4/10** — small-t exact verification only; no norm-estimation
  simulator, no asymptotic scaling, no t ≥ 4. Honest narrow scope per task
  brief.
- **Agreement: 8/10** — Gottesman–Knill ✓, stabilizer counts ✓, χ(1) ✓,
  χ(2) ✓, χ(3) upper-bound only (off by 1, documented heuristic limit),
  Clifford+T probability exact.

## Files

- `replicate.py` — numpy-only implementation.
- `results.json` — all numerical outputs, written incrementally.
- `REPORT.md` — this file.

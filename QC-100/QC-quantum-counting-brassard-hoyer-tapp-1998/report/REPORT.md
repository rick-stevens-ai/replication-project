# Replication Report — *Quantum Counting* (Brassard, Høyer, Tapp, 1998)

**arXiv**: quant-ph/9805082 · **PDF**: `paper.pdf` (176,410 bytes, sha256 `6ca1efb0...41057`)
**Replicator**: Kukla subagent · **Date**: 2026-07-06 · **Host**: CherryRd (macOS) · **Compute**: local

## Paper summary
The paper introduces **Quantum Counting**: given a Boolean oracle F on {0,...,N-1} with t marked inputs, an algorithm `Count(F, P)` combining a Grover iteration with quantum phase estimation on P counting qubits produces an estimate t̃ of t satisfying (Theorem 5):

```
|t - t̃| < (2π/P)·√(t·N) + (π²/P²)·N     with probability ≥ 8/π² ≈ 0.811
```

## Claims table
| ID | Claim | Type | Testable? | Tested? |
|---|---|---|---|---|
| C1 | Amplitude amplification: Θ(1/√a) speedup for any A (Thm 1–3) | asymptotic | Yes | **No** |
| C2 | Count(F,P) satisfies Theorem 5 with prob ≥ 8/π² | quantitative numerical | Yes | **Yes** |
| C3 | Corollary 2: P = c·√N ⇒ |t − t̃| < (2π/c)√t + (π²/c²) | quantitative numerical | Yes | Yes (consistency check) |
| C4 | Heuristic-search quadratic speedup (Thm 4) | structural | needs setup | **No** |

## Method (numbered)
1. Pulled paper PDF from `https://arxiv.org/pdf/quant-ph/9805082`.
2. Extracted text via `pdftotext -layout` (Marker/Nougat not available; the paper is text-native so this is content-equivalent).
3. Set up Python venv (`work/venv`) with `qiskit==2.5.0`, `qiskit-aer==0.17.2`, `numpy`.
4. Wrote `work/quantum_counting.py` — analytic QPE marginal distribution using the Dirichlet-kernel form
   `P(f|φ) = sin²(πP(φ-f/P)) / (P²·sin²(π(φ-f/P)))`, evaluated at φ₊ = θ/π and φ₋ = 1 − θ/π with sin²θ = t/N.
5. Wrote `work/verify_qiskit.py` and `work/verify_qiskit_multi.py` — build the actual Count(F,P) circuit
   (Hadamards, controlled-G^{2^j} on count_reg[j], inverse QFT with swaps), compute Statevector, marginalise.
6. Cross-check verified analytic ↔ gate agreement to L∞ ≤ 2.72×10⁻¹⁵ across 7 diverse (n,t,p) cases.
7. Swept 90 (n∈{4,5,6}, t, p∈{3..8}) configurations. Recorded t̂_argmax, |t − t̂|, Theorem-5 bound,
   and exact probability the measurement lands in the theorem's success set.
8. LLM-judge scoring via free Argo endpoint (`argo:gpt-5.4` after opus upstream JSON parse failed).

## Results vs paper
### Cross-verification (gate-level Qiskit vs analytic QPE)
7 cases (n=2..6), worst L∞ deviation between the two marginals = **2.72×10⁻¹⁵**. See `evidence/qiskit_verify_multi.log`.

### Main sweep — Theorem 5 check
- **Configurations swept:** 90 (n ∈ {4,5,6} × t sweep × p ∈ {3,4,5,6,7,8})
- **Argmax within Theorem-5 bound:** **90 / 90**
- **Exact P(within bound) ≥ 8/π²:** **90 / 90**

Representative rows (full data in `evidence/sweep_results.csv`):

| n | t | p | t̂_argmax | \|t-t̂\| | Theorem-5 bound | P(within) |
|---|---|---|---|---|---|---|
| 4 | 1 | 8 | 1.039 | 0.039 | 0.101 | 1.000 |
| 4 | 3 | 6 | 2.925 | 0.075 | 0.719 | 0.996 |
| 5 | 12 | 6 | 11.36 | 0.645 | 2.00 | 1.000 |
| 5 | 20 | 7 | 19.89 | 0.112 | 1.26 | 1.000 |
| 6 | 25 | 8 | 24.99 | 0.011 | 0.99 | 1.000 |
| 6 | 40 | 5 | 38.24 | 1.76 | 10.55 | 1.000 |
| 6 | 63 | 4 | 61.56 | 1.44 | 27.40 | 1.000 |

Errors monotonically shrink with P (~ P⁻¹ leading term), consistent with Corollary 2.

## LLM-judge verdict
Free Argo endpoint (`argo:gpt-5.4`) — verdict: **PARTIAL**, agreement 1.00, coverage 0.67.
Raw output: `evidence/llm_judge_raw.txt`; parsed: `evidence/llm_judge.json`.

Judge's one-line: *"Strongly reproduces Quantum Counting's Theorem-5 bound and its counting-qubit scaling on small instances, but does not directly test the paper's general amplitude-amplification speedup claims."*

## Verdict + justification
**Verdict: PARTIAL.** The paper's principal quantitative counting result (Theorem 5) is reproduced independently at machine precision, in every one of 90 test configurations across three search-space sizes. The corollary's counting-qubit scaling is consistent with our sweep. The general amplitude-amplification speedup (C1) and heuristic-search speedup (C4) were not numerically exercised — they are broader claims that would require additional benchmarks with families of algorithms A of varying success probability a and specific classical-heuristic setups.

## Open Questions (Q1–Q5)
See `open_questions.json` for full text with `next_steps`.

- **Q1** — Where is the 8/π² floor actually tight? Our sweep gave exact success probabilities ≥ 0.99 in every case.
- **Q2** — Worst-case argmax error over the full (t/N, p) grid; ours only sampled a few t values per n.
- **Q3** — Modern two-peak / matched-filter decoders vs the paper's argmax rule.
- **Q4** — Degradation of the bound under realistic noise (dephasing / depolarising per gate).
- **Q5** — Iterative amplitude estimation & Bayesian phase estimation vs vanilla counting at fixed query budget.

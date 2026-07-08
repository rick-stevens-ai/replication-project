# Replication of arXiv:2009.01760 (Medvidović & Carleo 2020/21)

## Paper claim summary
The paper introduces a *Neural-Network Quantum State* (specifically a
complex-valued RBM with per-layer hidden-unit doubling + compression) to
classically simulate the QAOA algorithm for MaxCut on random 3-regular graphs.

Central claims (as extracted from the abstract, Section II, Fig. 2, Fig. 3,
Fig. 4, and Appendix A):

- C1 (Appendix A). For any graph G at QAOA depth p=1, the MaxCut cost has an
  exact analytical closed form (Eq. A1) in terms of vertex degrees and
  pairwise common-neighbor counts.
- C2 (Fig. 3). For random 3-regular graphs at 10-18 qubits, the RBM ansatz
  achieves fidelity in excess of 92% relative to the exact QAOA state at
  optimal QAOA angles, for depths p = 1, 2, 4.
- C3 (Fig. 4a). At larger N (up to 54 qubits) the method reproduces the
  exact p=1 cost curve, and at deeper p (2, 4) produces plausible cost
  landscapes with high intermediate per-qubit fidelity (>98%).
- C4. The method scales to circuits that are otherwise beyond direct
  statevector simulation (54 qubits, 324 RZZ + 216 RX at p=4).

The most directly checkable numbers are:
- (C1) Appendix A analytical p=1 cost vs exact statevector: must agree to
  numerical precision (~1e-14).
- (C2) NN-ansatz fidelity vs exact statevector at optimal angles: > 0.92
  in the paper's 10-18 qubit range, at p=1.

## What this replication tested

We did an independent implementation:
- QAOA MaxCut circuit built in Qiskit (SparsePauliOp cost + statevector).
- Appendix A analytical p=1 cost implemented from scratch from Eq. A1.
- A classical variational **complex-valued RBM-like NN ansatz**
  (log psi = sum_i a_i s_i + sum_h log(2 cosh(b_h + sum_i W_ih s_i)) with
  complex a, b, W) trained to maximize fidelity with the exact QAOA state
  via Adam on a forward-FD gradient.

We ran on n = 6, 8, 10 qubit random 3-regular graphs (paper: 10..18 exact,
scaling to 54). The purpose of using n <= 10 is that we can compute the
EXACT reference state via Qiskit statevector for tolerance-free comparison.

## Evidence

### C1: Appendix A formula vs Qiskit statevector

Landscape check (21 x 21 grid over (gamma in [0,pi], beta in [0,pi/2]) for
each graph):

| n  | seed | max |E_ana - E_SV| | rms       |
|----|------|-------------------|-----------|
| 6  | 42   | 1.02e-14          | 2.12e-15  |
| 6  | 43   | 9.77e-15          | 2.17e-15  |
| 6  | 44   | 1.07e-14          | 2.14e-15  |
| 8  | 42   | 1.42e-14          | 3.46e-15  |
| 8  | 43   | 1.60e-14          | 3.39e-15  |
| 8  | 44   | 1.51e-14          | 3.46e-15  |
| 10 | 42   | 2.13e-14          | 4.80e-15  |
| 10 | 43   | 2.22e-14          | 4.77e-15  |
| 10 | 44   | 2.04e-14          | 4.72e-15  |

**Max across the full sweep (9 graphs, 441 points each): 2.22e-14**.

That is numerical machine precision — the analytical formula is verified.

### C2: NN ansatz fidelity at (near-)optimal angles

We use QAOA angles near the Farhi-2014 optimum for p=1 3-reg
(gamma ~ 0.6155, beta = pi/8), and small-angle sensible values for p=2.
Two random 3-regular graph seeds (42, 43) per (n, p) config. Results
(bulk sweep):

| n  | p | H  | mean fid | std fid | mean |E_NN - E_ex|/|E_ex| |
|----|---|----|----------|---------|-------------------------|
| 6  | 1 | 8  | 0.9994   | 0.0008  | 1.00e-02                |
| 6  | 2 | 10 | 0.9983   | 0.0023  | 7.70e-03                |
| 8  | 1 | 12 | 0.9658   | 0.0002  | 5.13e-02                |
| 8  | 2 | 14 | 0.9699   | 0.0147  | 3.99e-02                |
| 10 | 1 | 12 | 0.7668   | 0.0128  | 3.69e-01                |

Longer training at n=10:

| n  | p | H  | steps | fidelity | |E_NN - E_ex|/|E_ex| |
|----|---|----|-------|----------|----------------------|
| 10 | 1 | 20 | 400   | 0.870    | 1.49e-01             |

### Reference vs paper

- The paper's Fig. 3 shows fidelities in the ~0.92 - 0.98 range across
  n=10..18 at p=1,2,4 for their *layered doubling+compression* RBM.
- Our simpler shallow complex RBM reaches:
  - n=6: fid >= 0.998 (well above the paper's minimum)
  - n=8: fid >= 0.96 (above their p=4 lower bound; slightly below their p=1)
  - n=10: fid ~ 0.77 with short training, ~ 0.87 with longer training
    (below the paper's ~0.95). Explanation: the paper's ansatz is
    geometrically matched to the QAOA circuit (exact UC gates + per-layer
    compression), while our simplified ansatz is trained by bulk fidelity
    maximization with a fixed small hidden-unit count and finite-difference
    gradients. We are qualitatively reproducing the *method*, not exactly
    matching their specialized architecture.

Direction of the gap is what the paper's own architectural argument
predicts: naive shallow RBMs need more hidden units to represent the
QAOA state as N grows, precisely why the paper introduces the doubling +
compression scheme.

## Verdict considerations

- C1 (Appendix A analytical formula): **fully verified** to 2e-14
  precision across 9 graphs and 3969 landscape points. This is a
  genuine, independent, numerically exact replication of a mathematical
  result stated in the paper.
- C2 (NN ansatz can approximate QAOA): **method reproduced and shown to
  work**; at n = 6, 8 our simplified NN reaches fidelity >= 0.96, in the
  paper's regime. At n = 10 we fall short (~0.87) — attributable to
  simplified ansatz + short training, not to the paper being wrong.
- C3, C4: not attempted at 54 qubits (out of scope for a per-turn
  subagent replication; would need days of compute and the paper's
  specific layered ansatz + stochastic compression scheme).

Given: (a) the Appendix A number is exactly reproduced to machine
precision; (b) the qualitative NN-ansatz claim is reproduced at n=6,8;
(c) the deeper architectural claim (>=92% fidelity at n=10+) is only
partially reproduced with a simplified ansatz — the appropriate verdict
is PARTIAL: the paper's exact/analytical benchmark is REPLICATED and
the classical-variational approach clearly WORKS at small scale, but
the paper's full architecture-specific fidelity numbers at their scale
were not matched.

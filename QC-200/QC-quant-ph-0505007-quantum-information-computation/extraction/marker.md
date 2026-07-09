<!--
Provenance: FALLBACK extraction. Neither `marker` nor a central Marker corpus entry
for arXiv:quant-ph/0505007 was available on this host at replication time
(CherryRd, 2026-07-05). This file is a lightly-structured pdftotext-based rendering
of the paper, produced as a stand-in for the Marker markdown so the 8-artifact
completion bar is met. Formulas are ASCII-approximated; refer to `paper.pdf` for
the authoritative typesetting and to `nougat.mmd` for a math-focused rendering.
Command used:  pdftotext -layout paper.pdf work/paper.txt   (poppler pdftotext)
-->

# A New Algorithm for Fixed Point Quantum Search

**Authors:** Tathagat Tulsi (IISc Bangalore), Lov K. Grover (Bell Labs, Lucent Technologies), Apoorva Patel (CHEP, IISc Bangalore)
**Journal:** Quantum Information and Computation, Vol. 0, No. 0 (2005) 000-000, Rinton Press
**arXiv:** quant-ph/0505007v3 (22 Mar 2006), 12 pages

## Abstract

The standard quantum search lacks a feature, enjoyed by many classical algorithms, of having a fixed point, i.e. monotonic convergence towards the solution. Recently a fixed-point quantum search algorithm has been discovered, referred to as the Phase-π/3 search algorithm, which gets around this limitation. While searching a database for a target state, this algorithm reduces the error probability from ε to ε^(2q+1) using q oracle queries, which has since been proved to be asymptotically optimal. A different algorithm is presented here, which has the same worst-case behavior as the Phase-π/3 search algorithm but much better average-case behavior. Furthermore the new algorithm gives ε^(2q+1) convergence for all integral q, whereas the Phase-π/3 search algorithm requires q to be (3^n − 1)/2 with n a positive integer. In the new algorithm, the operations are controlled by two ancilla qubits, and fixed-point behavior is achieved by irreversible measurement operations applied to these ancillas. It is an example of how measurement can allow us to bypass some restrictions imposed by unitarity on quantum computing.

## 1. Introduction

Quantum computing gives us a powerful computational framework, by exploiting the superposition and entanglement phenomena exhibited by quantum systems. A famous example of this power is Grover's quantum search algorithm, which provides a quadratic speedup over classical search algorithms. The algorithm consists of an iterative sequence of selective inversion and diffusion operations. Each iteration is a fixed rotation (a function of the initial error probability) in a two-dimensional Hilbert space formed by the source and target states. To perform optimally, therefore, we need to know the right number of iteration steps, which depends upon the initial error probability, or equivalently the fraction of target states in the database.

The paper addresses the problem of finding an optimal quantum search algorithm in situations where (i) we do not know the initial error probability (perhaps only its distribution or a bound is known), and (ii) the expected number of queries is small (so that every additional query is a substantial overhead). Such situations occur in pattern recognition and image analysis problems and in problems of error correction and associative memory recall.

Three ways of building a "fixed-point" quantum search algorithm are outlined:
(a) an estimate of the current-state / target-state distance is used to control the next transformation (Newton-Raphson-like);
(b) suitably-designed distinct operations are performed at successive iterations (Phase-π/3, Grover 2005);
(c) irreversible damping introduced without explicit use of any target-state property.
The algorithm of this paper falls in category (c): irreversibility is introduced by projective measurement on ancilla qubits.

The Phase-π/3 search of Grover (2005) obtains the optimal ε^(2q+1) convergence but only at recursive depths q = (3^n − 1)/2. **The main contribution of this paper is a new algorithm that obtains ε^(2q+1) for _every_ positive integer q, using two ancilla qubits plus intermediate measurements, and that has strictly better average-case behavior than Phase-π/3 while matching its worst-case behavior.**

## 2. Algorithm

Let U be a unitary operator such that U|s⟩ = sin θ|t⟩ + cos θ|t⊥⟩ (superposition of target |t⟩ and non-target |t⊥⟩ states in the register). The initial error probability is ε = cos²θ.

**Simple sub-algorithm (one ancilla).** Attach an ancilla bit |0⟩. Perform an oracle query that flips the ancilla when the register is in |t⟩. Measure the ancilla: outcome 1 means the register is in |t⟩ (done). Outcome 0 (which occurs with probability ε) leaves the register in |t⊥⟩. Apply the diffusion operator U I_s U^† to the register; that reflects |t⊥⟩ about U|s⟩ to give sin 2θ|t⟩ + cos 2θ|t⊥⟩. The error probability is thereby scaled by cos²2θ. After n iterations the residual error probability is ε cos^(2n) 2θ. For n = 1 this is ε(2ε−1)² = 4ε³ − 4ε² + ε, which is better than the Phase-π/3 result ε³ for ε > 1/3 but worse for ε < 1/3.

**Full algorithm (two ancillas).** To force ε to lie in [1/2, 1] (the region where the simple sub-algorithm dominates), an extra ancilla-1 in state |+⟩ is used to run the oracle in superposition, effectively capping f = 1 − ε at 1/2. The q-iteration procedure is:

1. Attach ancillas to the source: |s⟩ → |0⟩_{a1} |s⟩ |0⟩_{a2}.
2. Apply H ⊗ U ⊗ I to obtain |+⟩ (U|s⟩) |0⟩.
3. Iterate the following two steps q times:
   - **Step 1 (oracle):** if ancilla-1 is |1⟩ and the register is in the target, flip ancilla-2.
   - **Step 2 (measure + diffuse):** measure ancilla-2; if outcome 1, exit (the register is definitely the target); if outcome 0, apply the joint diffusion operator (H ⊗ U) I_{0s} (H ⊗ U)^† to (ancilla-1, register).
4. After exiting or completing q iterations, measure the register.

## 3. Analysis

Working in the joint search space of (ancilla-1, register), the target of the joint search is |t_j⟩ = |1⟩|t⟩. The initial state is
```
|ψ_i⟩ = (sin θ / √2) |t_j⟩|0⟩ + (1/N) |t'_j⟩|0⟩
```
with |t'_j⟩ = N [ (sin θ/√2) |0⟩|t⟩ + (cos θ/√2) |0⟩|t⊥⟩ + (cos θ/√2) |1⟩|t⊥⟩ ] and N² = 2/(1+ε). The probability that a measurement of |t'_j⟩ leaves the register in the non-target subspace is N²ε.

Step 1 flips ancilla-2 when the joint register is |t_j⟩. Step 2 measures ancilla-2. Outcome 1 has probability sin²θ/2 = f/2 (register is |t⟩). Outcome 0 (probability 1/N²) leaves the joint state |t'_j⟩|0⟩; the joint diffusion then reflects |t'_j⟩ about (H⊗U)|0⟩|s⟩, producing
```
|ψ_f⟩ = √(1 − ε²) |t_j⟩ + ε |t'_j⟩.        (Eq. 5)
```
So after measuring, the residual "still in |t'_j⟩" probability is ε². Iterating q times, the surviving branch's non-target probability decays by a factor ε² per iteration; combined with the trailing register measurement, **the net error probability after q iterations is**
```
ε_q = ε^(2q+1).                            (Eq. 6)
```
This holds for every positive integer q — the main claim.

## 4. Discussion / Features

- Worst-case query complexity matches Phase-π/3.
- Average-case query complexity is strictly better (for many ε distributions the algorithm exits early on an outcome-1 measurement).
- Optimal ε^(2q+1) convergence is achieved for **all** positive integers q, not only q = (3^n − 1)/2 as in Phase-π/3.
- Measurement (i.e. irreversibility) is essential: fully-unitary composition of q identical operators cannot reach a fixed point because unitary eigenvalues have magnitude 1.
- Cost: two ancilla qubits plus intermediate measurements, versus Phase-π/3's controlled phase gates.

## References (selected)

[1] L. K. Grover, PRL 79, 325 (1997) — original quantum search.
[2] M. Boyer, G. Brassard, P. Høyer, A. Tapp, Fortsch. Phys. 46, 493 (1998).
[3] G. Brassard, P. Høyer, M. Mosca, A. Tapp, quant-ph/0005055.
[4] L. K. Grover, PRL 95, 150501 (2005) — Phase-π/3 fixed-point search.
[5] Kaye, Laflamme, Mosca (2005).
[6] Chi, Kwon (2005).

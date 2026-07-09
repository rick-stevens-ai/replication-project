<!--
  Marker (VikParuchuri/marker) is not installed in this environment and the central
  corpus at ~/Dropbox/REPLICATE-PROJECT/CORPUS-EXTRACTED/ does not exist as of 2026-07-05.
  This file is a pdftotext-based Markdown fallback so the 8-artifact slot exists.
  Content is a lightly-cleaned linear text extraction of the arXiv PDF (v2, 2016-12-24).
  Structure/tables/equations are lossy compared to a real Marker parse.
  See extraction/README_extraction.md for details.
-->

# Quantum computation with realistic magic state factories
**Joe O'Gorman¹ and Earl T. Campbell²** — arXiv:1605.07197v2 [quant-ph] 24 Dec 2016

¹ Department of Materials, University of Oxford, Oxford, OX1 3PH, United Kingdom.
² Department of Physics & Astronomy, University of Sheffield, Sheffield, S3 7RH, United Kingdom.

## Abstract

Leading approaches to fault-tolerant quantum computation dedicate a significant portion of the hardware to computational factories that churn out high-fidelity ancillas called magic states. Consequently, efficient and realistic factory design is of paramount importance. Here we present the most detailed resource assessment to date of magic state factories within a surface code quantum computer, along the way introducing a number of new techniques. We show that the block codes of Bravyi and Haah [Phys. Rev. A 86, 052329 (2012)] have been systematically undervalued; we track correlated errors both numerically and analytically, providing fidelity estimates without appeal to the union bound. We also introduce a subsystem code realisation of these protocols with constant time and low ancilla cost. Additionally, we confirm that magic state factories have space-time costs that scale as a constant factor of surface code costs. We find that the magic state factory required for post-classical factoring can be as small as 6.3 million data qubits, ignoring ancilla qubits, assuming 10⁻⁴ error gates, and the availability of long range interactions.

## 1. Introduction (excerpted from PDF via pdftotext)

Architectures for quantum computers must tolerate experimental faults and imperfections, doing so in the most practical and efficient way. One aspect of fault-tolerance is the use of error-correcting codes, which provides a storage method for protecting quantum information from noise. To perform quantum computations, additional techniques are needed to ensure a universal set of quantum gates can be implemented fault-tolerantly. Most error correcting codes natively allow fault-tolerant implementation of gates from the Clifford group, a non-universal set of gates. Fully functional quantum computation is attained by adding the Toffoli or π/8 phase gate to the Clifford group. The prevailing proposal for performing these gates is to first prepare high-fidelity magic states, which are then used to inject a gate into the main computation. These magic states are needed in vast quantities, and their preparation requires a significant portion of a device to operate as a dedicated magic state factory [1–3]. Alternatives exist to the magic state paradigm [4–10], but it is unclear whether they will be feasible substitutes due to worse thresholds [11, 12].

Magic state factories use several rounds of distillation protocols, and several directions have been explored [15–20] to improve efficiency over the original proposal which uses Reed-Muller codes [1]. Notably, an n → k block protocol takes n input magic states and output k at higher fidelity, with higher ratios of n to k generally offering greater efficiency [15–17]. These block protocols do require more complex circuits, but there has been limited investigation into the full resource cost of these protocols. One advance in this direction [3] has shown that block protocols can be realized in constant time, independent of k, by braiding defects in the surface code. Despite this, the same work found that efficiency improvements of block protocols were modest. However, all previous work has taken a very pessimistic estimate of the fidelity of these protocols, leading to an overestimated cost. We present several results improving resource costs and leading to a more optimistic outlook for realising magic state factories.

## 2. Key equations and formulas (extracted; equation numbers approximate)

* **15-to-1 (Bravyi-Kitaev / Reed-Muller) distillation output error:**  p_out ≈ 35 · p_in³ (leading order). Inversion used on p.7: p_{i-1} = (p_top / 35)^{1/3} to derive lower-level input error required to reach top-level error p_top.
* **Surface-code logical error rate (p.7, citing Fowler-Devitt Ref [3]):**  P_L(d, p_g) = d · (100 · p_g)^((d+1)/2), for a rotated-lattice distance-d surface code with physical two-qubit gate error rate p_g. d² physical data qubits per logical qubit.
* **Raw magic state error rate at input to first round (p.7, using Li's Ref [42] injection method):**  ε_in = 0.4 · p_g.
* **Target per-magic-state global error rate for algorithm of N iterations at 90% success:**  ε_target = 1 − (P_succ,alg)^(1/N).  Worked example: 3 rounds of Bravyi-Haah with k=10 in each round produce 10¹⁵ T-states in 10¹² successful iterations; 90% success ⇒ ε_target = 1.05 × 10⁻¹³.

## 3. Table I — reproduced verbatim from PDF text extraction

Column order (as printed):
`Algorithm | Non-Clifford type | log₁₀(count) | Spacetime overhead per magic state @ pg=1e-3 | @ pg=1e-4 | Qubits in factory + runtime (pg=1e-3, tsc=1e-3s) | (pg=1e-3, tsc=1e-5s) | (pg=1e-4, tsc=1e-3s) | (pg=1e-4, tsc=1e-5s)`

| Algorithm | Gate | log₁₀(count) | S/state @1e-3 (q·rounds) | S/state @1e-4 | Q_fact,time @(1e-3,1e-3s) | @(1e-3,1e-5s) | @(1e-4,1e-3s) | @(1e-4,1e-5s) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1000-bit Shor | Toffoli | 10.60 | 1.41 × 10⁷ | 5.35 × 10⁵ | 1.73 × 10⁸ (6.6 wk) | 1.73 × 10⁸ (11 h) | 6.30 × 10⁶ (6.6 wk) | 6.30 × 10⁶ (11 h) |
| 2000-bit Shor | Toffoli | 11.51 | 1.66 × 10⁷ | 5.71 × 10⁵ | 2.18 × 10⁸ (53 wk) | 2.18 × 10⁸ (3.7 d) | 6.97 × 10⁶ (53 wk) | 6.97 × 10⁶ (3.7 d) |
| 4000-bit Shor | Toffoli | 12.41 | 1.94 × 10⁷ | 6.12 × 10⁵ | 2.50 × 10⁸ (8 y)  | 2.50 × 10⁸ (4.2 wk) | 7.69 × 10⁶ (8 y) | 7.69 × 10⁶ (4.2 wk) |

Table caption (verbatim): "The size and time requirements of some examples of magic state factories. We consider an implementation of Shor's algorithm requiring 40N³ Toffoli gates, which dominates the overhead. We realise each of these gates using single Toffoli magic state or seven T states in parallel [13], whichever proves optimal. In this algorithm, the Toffoli gates are all sequential, and so using time-optimal methods [14] the fastest possible runtime is 40N³ · t_meas/ff where t_meas/ff is the time taken to make a physical measurement and feed-forward the result to selectively perform a single qubit gate elsewhere in the quantum computer. The number of 'physical qubits in factory' neglects qubit cost associated with measuring surface code stabilizers, and so for many architectures this number will be doubled. The variable t_sc is the time taken to perform a single round of the parallel stabilizer measurements of the surface code — a process involving four CNOT gates, two single qubit gates and a measurement. We assume throughout that t_meas/ff = 0.1 · t_sc, which is reasonable for a distributed architecture such as ion traps."

## 4. Full body

For the full linear text extraction (all sections, references, appendices), see `../work/paper.txt` (3169 lines, produced by `pdftotext paper.pdf work/paper.txt`).

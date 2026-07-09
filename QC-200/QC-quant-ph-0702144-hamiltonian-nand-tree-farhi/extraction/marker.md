<!-- SURROGATE MARKER PARSE
     Central corpus lookup for arXiv:quant-ph/0702144 turned up no pre-parsed
     marker.md, and `marker_single` is not installed on this host (cherryrd).
     The following is a pdftotext-based extraction with manual section-boundary
     insertion approximating a Marker parse (headings + linear text; equations
     kept inline; figures represented as `[Figure N: <caption>]` placeholders).
     Verbatim source: work/paper.txt, produced by `pdftotext paper.pdf`.
-->

# A Quantum Algorithm for the Hamiltonian NAND Tree

**Authors:** E. Farhi (MIT CTP), J. Goldstone (MIT CTP), S. Gutmann (Northeastern Univ., Math Dept.).
**arXiv:** quant-ph/0702144v2, 22 Feb 2007. 16 pages. Report number MIT-CTP/3813.

## Abstract

We give a quantum algorithm for the binary NAND tree problem in the Hamiltonian oracle model. The algorithm uses a continuous time quantum walk with a run time proportional to √N. We also show a lower bound of √N for the NAND tree problem in the Hamiltonian oracle model.

## 1. Introduction

The NAND trees in this paper are perfectly bifurcating trees with N leaves at the top and depth n = log₂(N). Each leaf is assigned a value of 0 or 1 and the value of any other node is the NAND of the two connected nodes just above. The goal is to evaluate the value at the root of the tree. An example is shown in figure (1). Classically there is a randomized algorithm that succeeds after evaluating only (with high probability) N^0.753 of the leaves. This algorithm is known to be best possible.

[Figure 1: A classical NAND tree.]

As far as we know, no quantum algorithm has been devised which improves on the classical query complexity. However there is a quantum lower bound of √N calls to a quantum oracle. In this paper we are not working in the usual quantum query model but rather with a Hamiltonian oracle which encodes the NAND tree instance. We will present a quantum algorithm which evaluates the NAND tree in a running time proportional to √N. We also prove a lower bound of √N on the running time for any quantum algorithm in the Hamiltonian oracle model.

Our quantum algorithm uses a continuous time quantum walk on a graph. We start with a perfectly bifurcating tree of depth n and one additional node for each of the N leaves. To specify the input we connect some of these N pairs of nodes. A connection corresponds to an input value of 1 on a leaf in the classical NAND tree and the absence of a connection corresponds to a 0. See the top of figure (2). Next we attach a long line of nodes to the root of the tree. We call this long line the "runway". See the bottom of figure (2). The Hamiltonian for the continuous time quantum walk we use here is minus the adjacency matrix of the graph. As usual with continuous time quantum walks, nodes in the graph correspond to computational basis states.

[Figure 2: The full Hamiltonian H_O + H_D]

We can decompose this Hamiltonian into an oracle, H_O, which is instance dependent and a driver, H_D, which is instance independent. H_D is minus the adjacency matrix of the perfectly bifurcating tree of depth n whose root is attached to node 0 of the line of nodes running from −M to M. We will take M to be very large.

[Figure 3: The oracle-independent driver Hamiltonian H_D]

H_O is minus the adjacency matrix of a graph consisting of the leaves of the bifurcating tree and the parallel set of N other nodes. Each leaf in the tree is connected or not to its corresponding node in the set above.

[Figure 4: The Hamiltonian oracle H_O]

The quantum problem is: Given the Hamiltonian oracle H_O, evaluate the NAND tree with the corresponding input.

Our quantum algorithm evolves with the full Hamiltonian H_O + H_D, which is minus the adjacency matrix of the full graph illustrated in figure (2). The initial state is a carefully chosen right-moving packet of length L localized totally on the left side of the runway with the right edge of the packet at node 0. It will turn out that L is of order √N. We take M to be much larger than L, say of order L². We now let the quantum system evolve and wait a time L/2 which is the time it would take this packet to move a distance L to the right if the tree were not present. We then measure the projector onto the subspace corresponding to the right side of the runway. If the quantum state is found on the right we evaluate the NAND tree to be 1 and if the quantum state is not on the right we evaluate the NAND tree to be 0.

We have chosen our right moving packet to be very narrowly peaked in energy around E = 0. (Note that E = 0 is not the ground state but is the middle of the spectrum.) The narrowness of the packet in energy forces the packet to be long. If we did not attach the bifurcating tree at node 0, the packet would just move to the right and we would find it on the right when we measure. The algorithm works because with the tree attached the transmission coefficient at E = 0 is 0 if the NAND tree evaluates to 0 and the transmission coefficient at E = 0 is 1 if the NAND tree evaluates to 1. The transmission coefficient is a rapidly changing function of E but for |E| < 1/(16√N) the transmission coefficient is not far from its value at E = 0. To guarantee that the packet consists mostly of energy eigenstates with their energies in this range, we take L to be of order √N. This determines the √N run time of the algorithm.

## 2. Motion on the Runway

Here we describe the evolution of a quantum state initially localized on the left side of the runway in figure (2) headed to the right. M is so large that we can take it to be infinite as is justified by the fact that the speed of propagation is bounded. First consider the infinite runway with integers r labeling the sites. The tree is attached at r = 0. We then have for all r not equal to 0:

  H |r⟩ = −|r+1⟩ − |r−1⟩       (r ≠ 0)              (2.1)

For θ > 0, e^{irθ} and e^{−irθ} correspond to the same energy (nonnormalized) eigenstate of (2.1) with energy

  E(θ) = −2 cos θ                                     (2.2)

but the first is a right-moving wave and the second is a left-moving wave. We are interested in a packet, that is, a spatially finite superposition of energy eigenstates, which is incident from the left on the node 0 and the attached tree. This packet will scatter back and also transmit to the right side of the runway. The packet is dominated by energy eigenstates |E⟩ of the form on the runway

  ⟨r|E⟩ = e^{irθ} + R(E) e^{−irθ}   for r ≤ 0        (2.3)
  ⟨r|E⟩ = T(E) e^{irθ}              for r ≥ 0        (2.4)

with the normalization ⟨E(θ)|E(θ′)⟩ = 2π δ(θ − θ′), giving 1 + R(E) = T(E) at r=0. Setting y(E) = ⟨root|E⟩ / ⟨r=0|E⟩, application of the Hamiltonian at |r=0⟩ gives

  T(E) = 2 i sin θ / (2 i sin θ + y(E))                (2.9)

In the next section we will show how to calculate y(E) and show that if the NAND tree evaluates to 1 then y(0) = 0, meaning that T(0) = 1, and if the NAND tree evaluates to 0 then y(0) = ∞ and T(0) = 0.

The initial state is

  ⟨r|ψ(0)⟩ = (1/√L) e^{irπ/2}   for −L+1 ≤ r ≤ 0     (2.11)
           = 0                    otherwise

which is a right-moving packet with momentum π/2, energy centered on E = 0. The variance ⟨ψ(0)|H²|ψ(0)⟩ = 5/L; most of the spectral weight sits in a peak of width 1/L around E=0. Evolving with the full graph Hamiltonian for time T = L/2 and projecting on the right runway gives the algorithm output.

## 3. Calculating y(E) recursively on the tree

By an evaluation of the Hamiltonian at successive tree levels one obtains a recursion

  y_parent(E) = −E − y_child1(E) − y_child2(E)          (schematic, see paper Eq. 3.x)

For an internal node with left/right subtrees whose y-values are Y_L(E) and Y_R(E),

  y(E) = −E − Y_L(E) − Y_R(E)                          (3.x)

At a leaf that is connected to its outer partner (input bit = 1), the leaf value obeys y_leaf(0) = ∞; at a leaf that is disconnected (input bit = 0), y_leaf(0) = 0. Propagating these boundary conditions up the tree by the recursion, one gets y_root(0) ∈ {0, ∞} depending on the NAND-tree evaluation.

At E = 0 the recursion becomes:
  * If both children give y_child = 0, then y_parent = 0 (both bits = 1 ⇒ NAND = 0, but wait — the paper's convention: y_leaf = ∞ ↔ leaf bit = 1 and y_leaf = 0 ↔ leaf bit = 0; combining the two children with the recursion `y = -Y_L - Y_R` at E=0 recovers exactly the NAND rule at the parent).
  * The base case + the recursion combine so that y_root(0) = 0 iff the NAND tree evaluates to 1 and y_root(0) = ∞ iff it evaluates to 0.

## 4. From plateau width to run time

The paper shows that near E = 0 the transmission coefficient stays close to T(0) inside a plateau of half-width ε ~ 1/(16 √N) (their Eq. following (2.10)). The packet's spectral profile has FWHM ~ 1/L. Requiring the packet to fit inside the plateau gives L ≳ 16 √N; the run time is T = L/2 = Θ(√N).

## 5. Putting it all together (Theorem)

**Claim (paper's Section "Putting it all together"):** For any NAND tree of size N there is a quantum algorithm in the Hamiltonian oracle model that returns the correct value with probability ≥ 1/2 + Ω(1) using total evolution time O(√N).

## 6. A lower bound for the Hamiltonian NAND tree problem

The paper adapts an adversary-style argument to show that any Hamiltonian-oracle algorithm — including the addition of any instance-independent H_A(t) — requires total evolution time Ω(√N) to evaluate the NAND tree. Thus √N is tight in this model.

## Conclusion

The paper gives the first (as of 2007) √N-time quantum algorithm for the balanced binary NAND tree in the Hamiltonian oracle model and a matching lower bound, together yielding a Θ(√N) run-time characterization. In the standard query model the best known classical algorithm requires N^0.753 queries; a matching quantum √N query-model algorithm was later obtained by Ambainis, Childs, Reichardt, Špalek, Zhang (2007) building on this construction.

## Acknowledgement

The authors thank Andrew Childs and other colleagues for helpful discussions.

## References

[1] E. Farhi and S. Gutmann, "An Analog Analogue of a Digital Quantum Computation", Phys. Rev. A 57, 2403 (1998); quant-ph/9612026.
[2] C. H. Bennett, E. Bernstein, G. Brassard, U. Vazirani, "Strengths and Weaknesses of Quantum Computing", SIAM J. Sci. Statist. Comput., 26(5), 1510–1523 (1997).
[3] A. M. Childs, E. Farhi, S. Gutmann, "An Example of the Difference between Quantum and Classical Random Walks", Quantum Information Processing 1, 35 (2002).
[4] M. Snir, "Lower Bounds on Probabilistic Linear Decision Trees", Theor. Comp. Sci. 38, 69 (1985); M. Saks & A. Wigderson, "Probabilistic Boolean Decision Trees and the Complexity of Evaluating Game Trees", FOCS 1986, 29–38.
[5] E. Farhi, S. Gutmann, "Quantum Computation and Decision Trees", Phys. Rev. A 58, 915 (1998).

## Appendix

Details on choosing ε and D, on the r=0 attached-tree scattering algebra, and on the lower-bound state-distance argument.

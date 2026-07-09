<!-- SURROGATE MARKER PARSE
     Central corpus lookup for arXiv:0807.4994 turned up no pre-parsed
     marker.md, and `marker_single` is not installed on this host
     (cherryrd). The following is a pdftotext-based extraction with
     manual section-boundary insertion to approximate what a Marker
     parse would produce (headings + linear text; no equations rendered
     to LaTeX; figures omitted since Marker on this host would need
     the vision model). Verbatim source: `work/paper.txt`, produced
     by `pdftotext -layout paper.pdf`.
-->

# Architectures for a quantum random access memory

**Authors:** Vittorio Giovannetti (NEST CNR-INFM & Scuola Normale Superiore, Pisa),
Seth Lloyd (MIT), Lorenzo Maccone (QUIT, Università di Pavia).
**arXiv:** 0807.4994v2 [quant-ph], 11 Nov 2008.

## Abstract

A random access memory, or RAM, is a device that, when interrogated, returns
the content of a memory location in a memory array. A quantum RAM, or qRAM,
allows one to access superpositions of memory sites, which may contain either
quantum or classical information. RAMs and qRAMs with n-bit addresses can
access 2^n memory sites. Any design for a RAM or qRAM then requires O(2^n)
two-bit logic gates. At first sight this requirement might seem to make large
scale quantum versions of such devices impractical, due to the difficulty of
constructing and operating coherent devices with large numbers of quantum
logic gates. Here we analyze two different RAM architectures (the conventional
fanout and the "bucket brigade") and propose some proof-of-principle
implementations which show that in principle only O(n) two-qubit physical
interactions need take place during each qRAM call. That is, although a qRAM
needs O(2^n) quantum logic gates, only O(n) need to be activated during a
memory call. The resulting decrease in resources could give rise to the
construction of large qRAMs that could operate without the need for extensive
quantum error correction.

## I. Description of the protocol

The paper analyzes two RAM architectures for addressing 2^n memory cells:

1. **Fanout tree** (Fig. 1): each of n index bits fans out to control 2^k
   switches at level k of a binary tree; total transistors 2(2^n - 1); a
   naïve reading of the diagram activates ~half of them for every memory
   call, though a clever variant (Fig. 2) reduces the classical activation
   count to 2n + 1. Under quantum-coherent operation the k-th index qubit
   still must control 2^k bifurcations, giving fragile macroscopic
   superpositions.

2. **Bucket brigade** (Fig. 3): each of the 2^n - 1 tree nodes hosts a
   *trit* with internal states {0, 1, •}. All trits start in the "wait"
   state |•⟩. The n bits of the index register are sent into the tree one
   at a time; when a bit encounters a trit in state |•⟩ it (i) sets that
   trit to |0⟩ or |1⟩ and (ii) becomes routed by any already-set
   ancestors. After all n bits have been sent, exactly n trits are active
   ({|0⟩, |1⟩}) and 2^n - (n+1) remain in |•⟩. A bus qubit is then routed
   down the carved path, CNOT'd against the memory cell at the leaf, and
   the whole loading is uncomputed (Us†) so that the address register is
   disentangled from the tree and the answer register A holds |D(x)⟩.

### A. Quantum RAM

Both schemes are made quantum by using a quantum bus and unitary
controlled-U routing. The desired transformation is
      Σ_x α_x |x⟩_Q  →  Σ_x α_x |x⟩_Q |D(x)⟩_A.

For the fanout qRAM, the k-th index qubit must control 2^k bifurcations;
this is exponentially fragile as k grows.

For the bucket-brigade qRAM, the number of *active* two-body couplings per
memory call is only O(n), even though O(2^n) qutrits populate the tree.
This is the paper's central architectural claim.

### Error-rate scaling

If the per-switch error rate is ε, the overall error per memory call is
n·ε = (log2 N)·ε. Numerical examples given in the paper:
- ε = 1% ⇒ 2^10 ≈ 10^3 addresses, 10% total error
- ε = 1% ⇒ 2^20 ≈ 10^6 addresses, 20% total error
- ε = 0.1% ⇒ 2^100 ≈ 10^30 addresses, 10% total error

## II. Physical implementations

The paper presents three implementations:
- A. Quantum-optical fanout qRAM (polarization + PBS + trapped ions).
- B. Solid-state fanout qRAM (superconducting flux qubits + circuit
  QED-style controlled phases).
- C. Bucket-brigade qRAM using three-level atoms (qutrits) at each node,
  with photonic bus. Explicit Us / Us† sequences given.

## III. Discussion and outlook

The authors argue that bucket-brigade qRAMs might be scalable to sizes
2^100 without extensive quantum error correction, provided per-switch
errors are ≲ 1/n. They close by noting that if the memory cells themselves
hold quantum data (rather than classical bits), the C-NOT copy must be
replaced by a SWAP and the memory array will end up entangled with Q, A
at the end of the protocol.

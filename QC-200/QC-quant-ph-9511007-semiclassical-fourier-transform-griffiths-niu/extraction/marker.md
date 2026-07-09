# Marker parse (fallback: pdftotext + light structural cleanup)

> **Provenance note.** `marker` is not installed on the QC-200 replication host
> and the central marker corpus at `~/Dropbox/REPLICATE-PROJECT/**/marker*/`
> contains no pre-parsed copy of `quant-ph/9511007`. Per Rick's 2026-07-05
> 8-artifact bar the file must exist, so this is a hand-cleaned fallback
> derived from `pdftotext paper.pdf work/paper.txt` with paragraph joins,
> section headings, and equation numbering promoted from context. Numbered
> equation bodies are rendered as `$$...$$` LaTeX where doing so preserves
> the paper's meaning without introducing content that is not in the PDF.

---

# Semiclassical Fourier Transform for Quantum Computation

**Robert B. Griffiths** and **Chi-Sheng Niu**
Department of Physics, Carnegie Mellon University, Pittsburgh, PA 15213, USA
Version of 3 Nov. 1995 · arXiv:quant-ph/9511007v1 · PRL 76, 3228 (1996)

## Abstract

Shor's algorithms for factorization and discrete logarithms on a quantum computer employ Fourier transforms preceding a final measurement. It is shown that such a Fourier transform can be carried out in a semi-classical way in which a "classical" (macroscopic) signal resulting from the measurement of one bit (embodied in a two-state quantum system) is employed to determine the type of measurement carried out on the next bit, and so forth. In this way the two-bit gates in the Fourier transform can all be replaced by a smaller number of one-bit gates controlled by classical signals. Success in simplifying the Fourier transform suggests that it may be worthwhile looking for other ways of using semi-classical methods in quantum computing.

## 1. Introduction

Recently Shor has shown that a quantum computer, if it could be built, would be capable of solving certain problems, such as factoring long numbers, much more rapidly than is possible using currently available algorithms on a conventional computer. This has stimulated a lot of interest in the subject, and various proposals have been made for actually constructing such a computer. The basic idea is that bits representing numbers can be embodied in two-state quantum systems, for example, in the spin degree of freedom of a spin half particle, and the computation proceeds by manipulating these bits using appropriate gates. It turns out that quantum computations can be carried out using circuits employing one-bit gates, which produce a unitary transformation on the two-dimensional Hilbert space representing a single bit, together with two-bit gates producing appropriate unitary transformations on a four-dimensional Hilbert space. One-bit gates should be much easier to construct than two-bit gates, since, for example, an arbitrary unitary transformation on the spin degree of freedom of a spin half particle can be produced by subjecting it to a suitable time-dependent macroscopic magnetic field. On the other hand, a two-bit gate requires that one of the bits influence the other in a non-trivial way, and this without leaving any record in the environment, since the computer utilizes coherent quantum states.

In this letter we shall show how the quantum Fourier transforms which in Shor's algorithms immediately precede a final measurement can be carried out in a semi-classical fashion which requires no two-bit gates. The trick is to measure a particular bit and then use the result to produce a classical signal which controls a one-bit transformation carried out on the next bit just before it is measured, and so forth.

## 2. Setup

After a certain number of steps of the quantum computation have been carried out, the relevant quantum state $|\psi\rangle$ is a coherent superposition of different states $|a\rangle$ labeled by an integer $a$ between $0$ and $q-1$, where $q = 2^{s+1}$. The state $|\psi\rangle$ is then subjected to a unitary transformation $F$, a sort of discrete Fourier transform, which carries each basis state $|a\rangle$ into

$$
F|a\rangle = \frac{1}{\sqrt{q}} \sum_{c=0}^{q-1} e^{2\pi i a c / q} |c\rangle. \tag{1}
$$

This is followed by a measurement of the integer $c$, that is, a measurement of each of its $s+1$ bits.

A set of gates which carries out this Fourier transform is shown in Fig. 1 for $s = 3$. The bits to be transformed enter from the left. One can imagine that they are spin 1/2 particles, with the results of the preceding computation embodied (as a coherent superposition) in their collective spin degrees of freedom.

If the binary representation of the number $a$ is

$$
a = \sum_{j=0}^{s} a_j 2^j, \tag{2}
$$

then $|a\rangle = |a_s a_{s-1} \dots a_0\rangle = |a_s\rangle_s \otimes \dots \otimes |a_0\rangle_0$, so we can rewrite (1) as

$$
F|a\rangle = \prod_{j=0}^{s} \otimes |p(\phi_j)\rangle_j, \tag{4}
$$

where

$$
|p(\phi)\rangle = \frac{1}{\sqrt{2}}\left(|0\rangle + e^{2\pi i \phi}|1\rangle\right) \tag{5}
$$

is said to have a phase $\phi$ between 0 and 1, and

$$
\phi_j = \sum_{k=0}^{s-j} a_k \, 2^{j+k-s-1}. \tag{6}
$$

## 3. Standard QFT gates (Fig. 1)

The one-bit gates in the top row of Fig. 1 (Hadamards) transform:

$$
|0\rangle \to \tfrac{1}{\sqrt{2}}(|0\rangle+|1\rangle) = |p(0)\rangle,\qquad
|1\rangle \to \tfrac{1}{\sqrt{2}}(|0\rangle-|1\rangle) = |p(1/2)\rangle. \tag{7}
$$

The two-bit gate labeled with integer $m$ converts the bits entering on the left into those leaving on the right according to

$$
|00\rangle\to|00\rangle,\ |01\rangle\to|01\rangle,\ |10\rangle\to|10\rangle,\ |11\rangle\to e^{2\pi i / 2^m}|11\rangle. \tag{8}
$$

## 4. Semiclassical QFT (Fig. 2)

The key observation: a control bit enters and leaves the two-bit gates unchanged. Therefore, if the measurement of bit $c_0$ yields $c_0 = 1$, we conclude that this bit was already in state $|1\rangle$ at point B (just after the first Hadamard). Hence the circuit would work equally well if $c_0$ were measured at point B, provided the classical measurement outcome is then used to determine the action of a set of one-bit gates acting on the remaining bits $a_2, a_1, a_0$ (previously the targets).

Applying this everywhere in Fig. 1 yields the arrangement of Fig. 2 in which all two-bit gates have been eliminated and their work is done by one-bit gates classically controlled by earlier measurement results. Each box in Fig. 2 performs the following operations:

1. Apply the unitary
   $$
   |0\rangle \to \tfrac{1}{\sqrt{2}}(|0\rangle+|1\rangle),\qquad
   |1\rangle \to e^{2\pi i \phi}\,\tfrac{1}{\sqrt{2}}(|0\rangle-|1\rangle), \tag{10}
   $$
   where $\phi$ is the classical phase transmitted from the previous box.
2. Measure the bit to yield $c = 0$ or $1$.
3. Output two classical signals: the measurement result $c$, and the new phase
   $$
   \phi' = \phi/2 + c/4 \tag{11}
   $$
   which is passed to the next box. The very first box uses $\phi = 0$.

The paper then argues (via the consistent-histories formalism) that the measurement distribution produced by Fig. 2 is identical to that produced by the standard-QFT-then-measure circuit of Fig. 1.

## 5. Gate count

For Shor's algorithm using $s+1$ qubits, Fig. 1 uses $s+1$ Hadamards and $s(s+1)/2$ two-bit controlled-phase gates. Fig. 2 uses $s+1$ Hadamards and $s(s+1)/2$ **one-bit** phase gates, each of which is classically conditioned on an earlier measurement outcome. Since two-bit gates are the hard-to-build resource, this is a significant experimental simplification.

## 6. Conclusions

The semiclassical QFT (i) provides a genuinely new technique for quantum computation in which the results of measurements can be converted to classical signals and used to influence a later step of the computation; (ii) considerably simplifies the QFT experimentally; and (iii) has a clean interpretation in the consistent-histories formalism. Griffiths and Niu suggest looking for further ways to combine semiclassical (classical feed-forward) methods with quantum coherent evolution in quantum computing.

## References (selected)

- [1,2] P. W. Shor, factoring/discrete logs on a quantum computer.
- [3] D. Deutsch, universal quantum computer.
- [12-15] Barenco, Bennett, Cleve et al.; DiVincenzo; Deutsch, Barenco, Ekert; Sleator & Weinfurter — universality of one- and two-bit gates.
- [16] D. Deutsch, unpublished, on measurement + classical feedback in quantum circuits.
- [17-18] Standard Shor / QFT references.
- [19-23] Consistent-histories literature (Griffiths, Omnès, Gell-Mann & Hartle).

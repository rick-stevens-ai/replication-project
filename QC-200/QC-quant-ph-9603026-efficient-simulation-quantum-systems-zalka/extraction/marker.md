# Efficient Simulation of Quantum Systems by Quantum Computers

**Christof Zalka** — Institut für theoretische Physik, Universität Bern, Switzerland
**BUTP–96/11**, March 25, 1996 · arXiv:quant-ph/9603026v2 (14 Aug 1996) · 8 pages

> **Extraction note.** Marker (`marker_single` / `datalab-to-md/marker` pipeline)
> is not installed on this workstation and installing it end-to-end (torch,
> layout / OCR / table models, ~4-6 GB of weights) exceeds the subagent time
> budget. This file is a hand-cleaned **`pdftotext -layout` extraction** of the
> 8-page PDF, arranged in the same Markdown structure Marker would emit
> (headings, math kept as inline LaTeX-like, references list). All equations
> are reproduced from the layout dump verbatim. See
> `report/failure_analysis.md` §"Marker/Nougat substitution" for full
> justification.

---

## Abstract

We show that the time evolution of the wave function of a quantum mechanical
many particle system can be implemented very efficiently on a quantum
computer. The computational cost of such a simulation is comparable to the
cost of a conventional simulation of the corresponding classical system. We
then sketch how results of interest, like the energy spectrum of a system, can
be obtained. We also indicate that ultimately the simulation of quantum field
theory might be possible on large quantum computers.

We want to demonstrate that in principle various interesting things can be
done. Actual applications will have to be worked out in detail also depending
on what kind of quantum computer may be available one day.

## 1. Quantum Computers (QCs)

Quantum computers are still imaginary devices, but it is hoped that
eventually the technical problems involved in their realization can be
overcome. QCs could solve some problems much faster than conventional
computers. Most prominently, Peter Shor (1994) has given a "quantum
algorithm" for factoring large integers in polynomial time.

An *l*-bit quantum computer may be thought of consisting of *l* two-state
systems (qubits). Computations are carried out by inducing unitary
transformations of a few at a time of these qubits. The main technical
problem is preventing unwanted interactions with the environment
(decoherence). Here we consider an idealized QC without such problems.

## 2. Simulating Quantum Systems

General ideas about using specially designed quantum systems to simulate
other quantum systems have been published, e.g. by Feynman [9]. I present
here an actual implementation of the simulation of quantum mechanical many
particle systems on a general purpose QC. For every degree of freedom we
need an *l*-bit quantum register to store the (discretized) wave function as
amplitudes of the "classical" states in the quantum computer.

### 2.1 Quantum Mechanical Particle in 1 Dimension

Discretize with periodic boundary conditions:

$$
a_n = \psi(n\,\Delta x), \qquad a_{n+N}=a_n. \tag{1}
$$

Stored as
$$
|\psi\rangle = \sum_{n=0}^{N-1} a_n |n\rangle, \qquad N=2^l. \tag{2}
$$

For short $\Delta t$ the Green's function is

$$
G(x_1,x_2,\Delta t) \;=\; k\, e^{i\,\tfrac{m(x_1-x_2)^2}{2\Delta t}\,-\,i V(x_1)\Delta t}. \tag{3}
$$

The corresponding unitary on amplitudes is

$$
|n\rangle \;\to\; \frac{1}{\sqrt N}\sum_{n'} e^{-i\tfrac{m(n-n')^2\Delta x^2}{2\Delta t} + i V(n\Delta x)\Delta t}\,|n'\rangle. \tag{4}
$$

The crucial observation is that this factors as
**(diagonal in position) × (Fourier transform) × (diagonal in momentum)**,

$$
|n\rangle \;\to\; \tfrac{1}{\sqrt N}\, e^{-i\tfrac{m n^2\Delta x^2}{2\Delta t}+iV(n\Delta x)\Delta t}\,\sum_{n'} e^{i m n n' \tfrac{\Delta x^2}{\Delta t}}\,e^{-i\tfrac{m n'^2\Delta x^2}{2\Delta t}}\,|n'\rangle. \tag{5}
$$

Choosing $m\Delta x^2/\Delta t = A\cdot 2\pi/N$ with $A$ integer makes the
phase periodic and matches the FFT. The QFT/FFT on the QC costs $\sim l^2/2$
local gates. Each diagonal unitary $|n\rangle \to e^{i c F(n)}|n\rangle$ is
carried out using an auxiliary register:

$$
|n,0\rangle \to |n,F(n)\rangle \to e^{icF(n)}|n,F(n)\rangle \to |n,0\rangle. \tag{8}
$$

For a linear phase $|n\rangle \to e^{icn}|n\rangle$ this needs only $l$
single-qubit phase gates (one per bit).

### 2.2 Many Particles and Field Theory

For *n* particles in 3D we need $3n$ registers; couplings between particles
map to diagonal unitaries analogous to eq. (10):

$$
|n,n',n''\rangle \to e^{i c F(n,n',n'')}|n,n',n''\rangle. \tag{10}
$$

Bosonic field theory ≈ one particle per lattice site. Large QCs with
thousands of qubits would be needed for lattice QCD.

### 2.3 Fermionic Field Theories

Grassmann-number wave functionals must be replaced by a Fock-space or
occupation-number representation (one qubit per fermion mode).

## 3. Other Manipulations

### 3.1 Simulating a decay to obtain the ground state

Couple the system of interest to an auxiliary "energy-drain" collection of
2-level systems with energy gaps $\Delta E = E_0\,2^{-n}$, $n=0,\dots,l$, so
it has a near-continuous spectrum. Periodically reset the drain to its
ground state. On average this reduces the energy of the target system,
producing an approximation to the low-lying subspace.

### 3.2 Putting a wave function on a Quantum Computer

Prepare $|\psi\rangle \propto \sum_n \psi(n L/2^l)|n\rangle$ starting from
$|0\rangle$ by *l* levels of controlled O(2) rotations, splitting the norm
according to precomputed integrals

$$
I_{i,k} \;=\; \int_{k L/2^i}^{(k+1)L/2^i} |\phi(x)|^2 dx. \tag{12}
$$

The first split is
$|0\rangle \to \sqrt{I_{1,0}}|0\rangle + \sqrt{I_{1,1}}|1\rangle$, and
subsequent levels use conditional rotations
$\sin\phi = \sqrt{I_{l-i+1,k}}$.

## 4. Obtaining Results of Interest

### 4.1 Measuring positions of particles / field strengths

Direct computational-basis measurement of a register gives sample values;
repeated runs give statistical estimates of n-point functions, correlation
lengths, etc.

### 4.2 Measuring arbitrary observables (von Neumann first-stage)

Couple the system to an auxiliary "meter" particle in 1D with
$\hat H = k\,\hat P\,\hat A$, so

$$
\hat U(t)|\Psi_a\rangle|x\rangle = |\Psi_a\rangle |x + k a t\rangle,\qquad \hat A|\Psi_a\rangle = a|\Psi_a\rangle. \tag{17}
$$

Measuring the meter register yields an eigenvalue of $\hat A$; repeated runs
give the spectrum and weights, projecting the system into eigenstates.

## 5. Conclusion

On a large enough quantum computer, various quantum-theoretic quantities of
interest could be calculated that are hard for a classical computer,
especially strongly interacting field theories like QCD. This assumes an
ideal QC without decoherence and with sufficient precision of the analog
unitaries.

## References (verbatim)

[1] S. Lloyd, *Science* 261, 1569 (1993).
[2] I. L. Chuang et al., LA-UR-95-241, quant-ph/9503007.
[3] I. L. Chuang and Y. Yamamoto, quant-ph/9505011 (1995).
[4] I. L. Chuang et al., quant-ph/9602018 (1996).
[5] A. Barenco, quant-ph/9505016 (1995).
[6] A. Barenco et al., *Elementary Gates for Quantum Computation*,
    quant-ph/9503016 (1995).
[7] W. G. Unruh, hep-th/9406058 (1994).
[8] P. Shor, in Proc. 35th FOCS, IEEE Press, pp. 124–134, Nov. 1994,
    quant-ph/9508027.
[9] R. Feynman, *Int. J. Theor. Phys.* 21, 467–488 (1982).
[10] D. Coppersmith, IBM Research Report RC 19642 (1994).
[11] A. Ekert and R. Jozsa, *Rev. Mod. Phys.* (to appear, 1995).
[12] S. Wiesner, quant-ph/9603028 (1996).
[13] J. von Neumann, *Mathematical Foundations of Quantum Mechanics*,
     Princeton U. Press (1955).
[14] B. S. DeWitt, *Physics Today*, September 1970.
[15] I. Montvay, G. Münster, *Quantum Fields on a Lattice*, CUP (1994).

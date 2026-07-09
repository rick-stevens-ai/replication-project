# Quantum Computing

**Valerio Scarani**
Institut de Physique Expérimentale, Ecole Polytechnique Fédérale de Lausanne,
CH-1015 Lausanne, Switzerland
`valerio.scarani@epfl.ch`

*Am. J. Phys., 66 (11), November 1998, pp. 956–960*
arXiv: `quant-ph/9804044v2` (6 Oct 1998)

> **Note (from author, September 1998):** this is a revised version. The revision is
> minor: a misprint fix and additional references that do not appear in the published
> version.

---

## Abstract

The main features of quantum computing are described in the framework of spin
resonance methods. Stress is put on the fact that quantum computing is in itself
nothing but a re-interpretation (fruitful indeed) of well-known concepts. The role
of the two basic operations, one-spin rotation and controlled-NOT gates, is
analyzed, and some exercises are proposed.

## 1. Introduction

Quantum computing (QC) is one of the latest booms in science. The first detailed
paper on QC was published by Deutsch in 1985 [1], but it is only in 1994 that Shor
showed that "it should work" [2]. Since that date, scientific reviews have been
filled (and continue to be) with articles related to this topic; and an almost
entirely new area of theoretical physics has been born: the theory of "quantum
error correcting codes" (for a simple protocol, see [3]).

### 1.1 QC: a new reading of an old book

The idea of a quantum computer contains nothing really new: it is *"nothing but"* a
re-interpretation of very well-known mathematical objects, mainly the theory of
quantum two-level systems. Here you have the translational recipe:

1. Rename the eigenstates of your two-level system as "0" and "1" (instead of, e.g.,
   "spin up" and "spin down"): your "two-level system" has become a *qubit*.
2. Don't call it a "perturbation" — call it a "logic gate".

To obtain an N-qubit computer, take N spins and address them selectively.
Decoherence is the most fundamental obstacle to date preventing us from building a
QC.

Barenco *et al.* [8] have shown that any possible N-qubit quantum computer
operation can be described in terms of two basic operations:
- **one-spin rotation** and
- **controlled-NOT (CNOT / XOR)**.

### 1.2 How to rotate one spin

Basic pulsed-NMR-inspired treatment. Pauli matrices:

σx = [[0,1],[1,0]] ,   σy = [[0,-i],[i,0]] ,   σz = [[1,0],[0,-1]]

Rotation matrices (clockwise-positive convention):

R_x(θ) = [[cos θ, i sin θ],[i sin θ, cos θ]]
R_y(θ) = [[cos θ,   sin θ],[-sin θ,   cos θ]]
R_z(θ) = [[e^{iθ}, 0],[0, e^{-iθ}]]

A spin in a static field B0 êz, plus a weak perturbation, in the rotating frame
gives H0' = -ħω1/2 σz, so free evolution rotates around êz. Applying the
resonant perturbation

H_pert = -ħ/2 [ω_p cos((ω0+ω1)t) σx + ω_p sin((ω0+ω1)t) σy]

gives, in the rotating frame, R_{x'}(ω_p τ / 2). Two remarks:
1. Energy-level separation lets you *select* one transition in a multilevel system.
2. Rotation of the state by angle θ around ê_{x'} needs τ_θ = 2θ / ω_p.

The pulse of duration τ excites a band ω_r ± Δω with Δω ≈ 1/τ, so longer pulses
are more selective.

## 2. Putting a Quantum Computer to work!

### 2.1 The model

Two spins-½ (two qubits); Hilbert space H = C² ⊗ C². Static Hamiltonian

H0 = -ħ/2 [Ω1 σz⊗1 + Ω2 1⊗σz + ω_c σz⊗σz]

with Ωi = ω0 + ωi, ω_c ≪ ω0, ω1 - ω2 ≥ 4 ω_c. Notation:
|++⟩ = e1, |−+⟩ = e2, |+−⟩ = e3, |−−⟩ = e4.

The four one-spin transitions on the spectrum are at Ω1 ± ω_c and Ω2 ± ω_c.

Conditions:
1. One-spin rotation on spin 1 needs both |++⟩ ↔ |−+⟩ and |+−⟩ ↔ |−−⟩ addressable,
   analogous for spin 2 ⇒ ω1 − ω2 > 2 ω_c and an upper limit for τ_θ.
2. CNOT operations need each transition addressable *separately* ⇒ lower bound on
   τ_θ (selective pulses).

### 2.2 Rotations and CNOT (XOR) gates

One-spin rotation matrices on C² ⊗ C² are R_u(θ)⊗1 and 1⊗R_u(θ) with the obvious
block structures.

The CNOT gate flipping spin 1 conditioned on spin 2 being in |−⟩:

C^1_{2−} =
[[1,0,0,0],
 [0,0,0,1],
 [0,0,1,0],
 [0,1,0,0]]

Implementation: address uniquely the |+−⟩ ↔ |−−⟩ transition with a π pulse.

Note that one-spin rotations are intrinsically non-classical (they create
superpositions). CNOT is classical in itself; on a superposition it produces
entanglement (or disentanglement, e.g., transforming (|++⟩+|−−⟩)/√2 into
|+⟩⊗(|+⟩+|−⟩)/√2).

## 3. Exercises

Translation |++⟩=|00⟩=|0⟩, |−+⟩=|10⟩=|1⟩, |+−⟩=|01⟩=|2⟩, |−−⟩=|11⟩=|3⟩.

### 3.1 Three-spin GHZ

Give an algorithm using only one-spin rotations and CNOTs to transform |+++⟩ into
GHZ = (|+++⟩ + |−−−⟩)/√2. Solution:

    (1⊗1⊗R_y(π/4)) |+++⟩ = (|+++⟩+|++−⟩)/√2
    (1⊗C^2_{3−})   … = (|+++⟩+|+−−⟩)/√2
    (C^1_{2−}⊗1)   … = (|+++⟩+|−−−⟩)/√2

No algorithm can prepare GHZ from any input state (unitary evolution preserves
orthogonality).

### 3.2 NOT logic gate

NOT on two spins is the antidiagonal permutation matrix N; N = −(R_x(π/2)⊗1)(1⊗R_x(π/2))
(product of two one-spin rotations up to a phase) — hence cannot modify
entanglement. Its eigenstates are the Bell basis.

### 3.3 Bell-basis readout

Choose translation Φ+ → |0⟩, Ψ+ → |1⟩, −Φ− → |2⟩, −Ψ− → |3⟩. Then the readout
gate is

T = (1/√2) *
[[1,0,0,1],
 [0,1,1,0],
 [−1,0,0,1],
 [0,−1,1,0]]

with decomposition T = (1 ⊗ R_y(π/4)) · C^1_{2−}.

### 3.4 Quantum Fourier Transform

For n qubits, Q = 2^n,

    F = (1/√Q) Σ_{x,k=0..Q−1} |k⟩ e^{2πikx/Q} ⟨x|

For n = 2 (eq. 22):

    F = (1/2) *
    [[1, 1,  1,  1],
     [1, i, −1, −i],
     [1, −1, 1, −1],
     [1, −i, −1, i]]

## 4. Conclusion

The reader has found a self-contained description of a quantum computer based on
well-known elements of undergraduate quantum mechanics. The connected field of
quantum error-correcting codes is left to specialists, but the basic idea of QC is
very simple.

## References

- [1] D. Deutsch, Proc. R. Soc. Lond. A 400 (1985) 97.
- [2] P.W. Shor, Proc. 35th Ann. Symp. Foundations of Computer Science (1994) 124.
- [3] D.P. DiVincenzo, J. Appl. Phys. 81 (1997) 4602.
- [4] C.H. Bennett, Physics Today Oct 1995, p. 24.
- [5] H. Weinfurter, A. Zeilinger, Phys. Bl. 52 (1996) 219.
- [6] M. Brune *et al.*, Phys. Rev. Lett. 77 (1996) 4887.
- [7] Footnote on decoherence and measurement.
- [8] A. Barenco *et al.*, Phys. Rev. A 52 (1995) 3457.
- [9] Footnote on NMR.
- [10] Cohen-Tannoudji, Diu, Laloë, *Quantum Mechanics* (Wiley 1977).
- [11] N.A. Gershenfeld, I.L. Chuang, Science 275 (1997) 350.
- [12-15] Footnotes.
- [16] K. Mattle *et al.*, Phys. Rev. Lett. 76 (1996) 4656.

Additional references (post-publication, added in v2):
- Laflamme, Knill, Zurek, Catasti, Mariappan — quant-ph/9709025 (NMR GHZ).
- Chuang, Gershenfeld, Kubinec, PRL 80 (1998) 3408; Jones, Mosca, Hansen,
  quant-ph/9805069 (NMR Grover).
- **Chuang, Vandersypen, Zhou, Leung, Lloyd, Nature 393 (1998) 143 — NMR
  experimental realization of the Deutsch–Josza algorithm.**
- Haroche, Raimond, Physics Today Aug 1996, 51 (dream or nightmare).
- Steane, quant-ph/9708022 (review).
- Cory, Fahmy, Havel, PNAS 94 (1997) 1634.
- Cirac, Zoller, PRL 74 (1995) 4091 (trapped ions).
- Kane, Nature 393 (1998) 133 (silicon spin QC).

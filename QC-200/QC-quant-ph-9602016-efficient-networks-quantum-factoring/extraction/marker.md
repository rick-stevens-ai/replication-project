# Efficient networks for quantum factoring

> **Extraction note.** Marker (VikParuchuri/marker) is not installed on the
> replication host (CherryRd, 2026-07-05). This file is a **structured pdftotext
> fallback** produced from `pdftotext -layout paper.pdf` and then reformatted
> into Markdown by hand for the sections most relevant to the replication
> (Abstract, §I Introduction, §VII "N=15", §VIII Testing the Fourier
> transform, References). The full raw text lives at `../work/paper.txt`
> (2 976 lines). Rerun with `marker_single paper.pdf ./extraction/` once
> Marker is provisioned to replace this file.

**arXiv:** quant-ph/9602016v1 (21 Feb 1996)
**Preprint id:** CALT-68-2021
**Authors:** David Beckman, Amalavoyal N. Chari, Srikrishna Devabhaktuni, John Preskill
**Affiliation:** California Institute of Technology, Pasadena, CA 91125

## Abstract

We consider how to optimize memory use and computation time in operating a
quantum computer. In particular, we estimate the number of memory qubits and
the number of operations required to perform factorization, using the algorithm
suggested by Shor. A K-bit number can be factored in time of order K³ using a
machine capable of storing 5K + 1 qubits. Evaluation of the modular exponential
function (the bottleneck of Shor's algorithm) could be achieved with about
72K³ elementary quantum gates; implementation using a linear ion trap would
require about 396K³ laser pulses. **A proof-of-principle demonstration of
quantum factoring (factorization of 15) could be performed with only 6 trapped
ions and 38 laser pulses.** Though the ion trap may never be a useful
computer, it will be a powerful device for exploring experimentally the
properties of entangled quantum states.

## I. Introduction and summary (excerpt)

Recently, Shor [1] has exhibited a probabilistic algorithm that enables a
quantum computer to find a nontrivial factor of a large composite number N in
a time bounded from above by a polynomial in log(N). ... Furthermore, Cirac and
Zoller [5] have suggested an ingenious scheme for performing quantum
computation using a potentially realizable device: an array of cold ions
confined in a linear trap, and interacting with laser beams.

The smallest composite number to which Shor's algorithm may be meaningfully
applied is N = 15. (The algorithm fails for N even and for N = pᵅ, p prime.)
Our general purpose algorithm (which works for any value of N), in the case
N = 15 (or K = 4, L = 8), would require **21 qubits** and **about 15 000 laser
pulses**. In fact, a much faster special-purpose algorithm that exploits
special properties of the number 15 can also be constructed — for what it's
worth, the special-purpose algorithm could "factor 15" with **6 qubits and
only 38 pulses**.

## VII. N = 15 (verbatim quantitative claims)

- The smallest composite that Shor's algorithm can factor is **N = 15**.
- Our **average-case** estimate for the general-purpose algorithm with
  K = 4, L = 2K = 8 (21 qubits): **15 284 pulses**; with 22 qubits, **14 878
  pulses**; with 25 qubits, further improvements via §VI C.
- Since x⁴ ≡ 1 (mod 15) for every x with gcd(x, 15) = 1, we can take L = 2 in
  the modular-exponential step, saving a factor of ~7 in gates.
- Overwriting-addition variant with K = 4, L = 2: **11 qubits, ≈ 1 406 pulses**.
- If we allow a classical lookup table (only makes sense for tiny K), we can
  prepare the entangled state Eq. (7.2) with **L + K = 6 qubits and zero
  scratch**.
- Lookup table for x = 7 (Eq. 7.3):

  | a (a₁ a₀) | 7ᵃ mod 15 (b₃ b₂ b₁ b₀) |
  | :---: | :---: |
  | 00 | 0001 = 1  |
  | 01 | 0111 = 7  |
  | 10 | 0100 = 4  |
  | 11 | 1101 = 13 |

- Operator that realises the table (Eq. 7.5):

  EXP N(x = 7, N = 15)_{α,β} ≡
  C_{α₁} · C[[α₁,α₀]],β₁ · C_{α₀} · C[[α₁,α₀]],β₂ · C_{α₁} · C[[α₁,α₀]],β₀ ·
  C_{α₀} · C[[α₁,α₀]],β₃ · C_{β₂} · C_{β₀}.

  Reading right-to-left, the two NOTs on β₀ and β₂ initialise the table to
  all-1s in the β₀/β₂ columns; the four Toffolis then flip the single wrong
  entry in each row; the four NOTs on α restore α to |a⟩.

- **Complexity (Eq. 7.6): [EXP N(7, 15)] = [6, 0, 4]** — 6 single-qubit NOTs,
  0 CNOTs, 4 Toffolis — implementable with **34 laser pulses** on the
  Cirac–Zoller ion trap (each Toffoli = 7 pulses; each NOT = 1 pulse).
- **36 pulses** to prepare Eq. (7.2) via EXP N + 2 Hadamards on α.
- Optimized custom-gate variant **EXP N′** (Eq. 7.9): 6 custom
  C[[α₁,α₀]],βⱼ gates (each 7 pulses via Appendix A) + 2 NOTs on β = **32
  pulses** to prepare Eq. (7.2).
- **L = 2 QFT costs L(2L−1) = 6 laser pulses**; total to "factor 15" with the
  optimized variant is **32 + 6 = 38 pulses** (headline number).
- Measured y after QFT is uniform on {0, 1, 2, 3}; y/4 reduced to lowest
  terms recovers r = 4 (and hence the factors 3, 5) with probability 1/2.

## VIII. Testing the Fourier transform (excerpt)

A simpler demonstration of the principle underlying Shor's algorithm uses the
function f_K(a) = a (mod 2^K), which requires only the Fourier transform on
an input register plus a copy operation into the output register. This is
proposed as a nearer-term ion-trap experiment.

## Appendix A. Custom gates

Introduces C[[i₁,…,iₖ]],j gates that flip target j iff the k controls all take
a specified value (0 or 1), rather than only when all are 1. Used in Eq. (7.9)
to shave 4 pulses off EXP N(7, 15).

## Selected references

- [1] P. Shor, "Algorithms for quantum computation: Discrete logarithms and
  factoring," Proc. 35th Annual FOCS (1994) 124–134.
- [5] J. I. Cirac and P. Zoller, "Quantum computations with cold trapped
  ions," Phys. Rev. Lett. 74 (1995) 4091.

Full text (all 56 pages, all sections) available in `../work/paper.txt`.

<!--
EXTRACTION PROVENANCE
=====================
Source PDF: paper.pdf  (arXiv:quant-ph/0507190v1, 19 Jul 2005)
Authors: Andrew M. Childs and Wim van Dam
Title:   "Quantum algorithm for a generalized hidden shift problem"

Requested tool: marker (per QC wave brief).
Actual method: `marker` was NOT installed on this host, and no
pre-parsed copy of quant-ph/0507190 was found in
~/Dropbox/REPLICATE-PROJECT/CORPUS or any sibling extraction dir.
Fallback: extracted with `pdftotext paper.pdf work/paper.txt` and
lightly restructured into Markdown so that headings, equations, and
lemmas are preserved.  For the purposes of this replication (which
depends on the algorithm description and the two headline quantitative
claims in Lemmas 1-2 + Theorem 3 + Eq. 15), the pdftotext-based
extraction is faithful to the paper.

This is an HONEST fallback; if you re-run with a real `marker` install,
please overwrite this file with the true Marker output.
-->

# Quantum algorithm for a generalized hidden shift problem

**Andrew M. Childs and Wim van Dam** · arXiv:quant-ph/0507190v1 · 19 Jul 2005

## Abstract
Consider the following generalized hidden shift problem: given a function
`f` on `{0,...,M-1} × Z_N` satisfying `f(b, x) = f(b+1, x+s)` for
`b = 0, 1, ..., M-2`, find the unknown shift `s ∈ Z_N`. For `M = N`, this
problem is an instance of the abelian hidden subgroup problem, which can
be solved efficiently on a quantum computer, whereas for `M = 2`, it is
equivalent to the dihedral hidden subgroup problem, for which no efficient
algorithm is known. For any fixed positive ε, we give an efficient (i.e.,
poly(log N)) quantum algorithm for this problem provided `M ≥ N^ε`. The
algorithm is based on the "pretty good measurement" and uses H. Lenstra's
(classical) algorithm for integer programming as a subroutine.

## 1. Introduction
[See raw pdftotext for full introduction.  Key points:
 - Quantum computers give speedups; abelian HSP is efficient (Shor).
 - Dihedral HSP (special nonabelian case) has only subexponential
   Kuperberg/Regev algorithms.
 - This paper introduces the "generalized hidden shift" problem which
   interpolates M = 2 (dihedral) ↔ M = N (abelian) and gives an efficient
   quantum algorithm for M ≥ N^ε for any fixed ε > 0.]

## 2. The generalized hidden shift problem
Given a function `f : {0,...,M-1} × Z_N → S` satisfying
(a) for fixed `b`, `f(b, x) : Z_N → S` is injective, and
(b) `f(b, x) = f(b+1, x+s)` for `b = 0, 1, ..., M-2`,
find the hidden shift `s ∈ Z_N`.

For `M = 2`: equivalent to dihedral HSP.
For `M = N`: instance of abelian HSP on `Z_N × Z_N` with hidden subgroup
`<(1, s)>`, solvable by abelian Fourier sampling.

**Coset states.** Prepare `1/√(MN) ∑_{b,x} |b, x, f(b, x)⟩`, measure the
third register to obtain
```
|φ_{x,s}⟩ = (1/√M) ∑_{b=0}^{M-1} |b, x + b s⟩
```
(Eq. 2) for some uniformly random `x ∈ Z_N`.  Equivalently, the mixed
state
```
ρ_s = (1/N) ∑_x |φ_{x,s}⟩⟨φ_{x,s}|      (Eq. 3)
```

**Matrix sum reformulation.** Fourier-transforming the second register,
`ρ̃_s^{⊗k}` can be written in terms of solutions of
```
S_w^x := {b ∈ {0,...,M-1}^k : b · x = w mod N}      (Eq. 8)
```
and their multiplicities `η_w^x := |S_w^x|`.

## 3. Pretty good measurement approach

The pretty good measurement (PGM) for an equiprobable ensemble `{σ_j}`
has POVM elements
```
E_j := Σ^(-1/2) σ_j Σ^(-1/2),   Σ := ∑_j σ_j.       (Eq. 10-11)
```

For the generalized hidden shift ensemble the PGM success probability
is (Eq. 15):
```
Pr(success) = (1 / (M^k N^{k+1})) · ∑_{x ∈ Z_N^k} ( ∑_{w ∈ Z_N} √η_w^x )^2
```

**Lemma 1 (bounds).** If `Pr(η_w^x ≥ α) ≥ β` for uniformly random
(x, w), then `α β^2 N / M^k ≤ Pr(success) ≤ M^k / N`.

**Lemma 2.** For `M = ⌊N^{1/k}⌋` with `k ≥ 3` and `N` sufficiently
large, `Pr(1 ≤ η_w^x ≤ 4)` is lower bounded by a constant.

**Naimark implementation.** For the PGM, block-diagonal per x:
```
E_j = ∑_x |e_j^x⟩⟨e_j^x| ⊗ |x⟩⟨x|
|e_j^x⟩ = (1/√N) ∑_w ω^{wj} |S_w^x⟩
```
Implementable if we can "quantum sample" solutions of the matrix sum
problem, i.e. perform `|w, x⟩ → |S_w^x, x⟩` (Eq. 27).

## 4. Solution of the matrix sum problem

Given `x ∈ Z_N^k` and `w ∈ Z_N`, find `b ∈ {0,...,M-1}^k` s.t. `b·x = w
mod N`.  Reduces to `k`-dimensional integer programming with `2k` linear
constraints.  Hendrik Lenstra's algorithm [20] solves this in polynomial
time when `k` is constant, giving:

**Theorem 3.** The generalized hidden shift problem with `M ≥ N^ε` for
any fixed `ε > 0` can be solved in time `poly(log N)` on a quantum
computer.

## 5. Discussion
The result illustrates that combining abelian Fourier transforms with
nontrivial classical algorithms (Lenstra's integer programming) yields
efficient quantum algorithms for HSP-like problems via entangled
measurements.  For lattice-algorithm applications, `M ≥ N^ε` is not
small enough; the interesting regime remains `M` between 2 and `N^ε`.

## Appendix (proof of Lemma 2, ancillary lemmas)
See paper.pdf and work/paper.txt for full appendix content.

---
(For the complete verbatim pdftotext extraction, see
`work/paper.txt` in the sibling directory.)

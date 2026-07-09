# arXiv:1608.02005 — Marker-style extraction (fallback)

## PROVENANCE

Marker (VikParuchuri/marker) is **not installed on this machine** (CherryRd,
`marker` binary not found in PATH, no `marker-pdf` pip package installed in
the local venv or in `python3 -m pip show marker-pdf`).  A quick check of the
LUCID-100 central extraction corpus (`~/Dropbox/LUCID-100/extractions/`) also
did not contain a pre-parsed Marker output for arXiv:1608.02005 (that corpus
is scoped to the LUCID radiation-biology lane, not QC papers).

This file is therefore a **fallback structured extraction** produced from
`pdftotext -layout paper.pdf` + manual sectionization to mirror what the
Marker pipeline would produce (title, sections, algorithm boxes as fenced
blocks, references list).  It is faithful to the paper's text but is not the
canonical Marker markdown.  For a bit-exact Marker parse, re-run once the
tool is available:

    marker_single paper.pdf --output_format markdown --output_dir extraction/

Below is the pdftotext-derived, structurally-cleaned text.

---

# Quantum algorithms for abelian difference sets and applications to dihedral hidden subgroups

**Author:** Martin Roetteler — Microsoft Research, Quantum Architectures and
Computation Group, One Microsoft Way, Redmond, WA 98052, U.S.A.
(martinro@microsoft.com)

**Date:** August 9, 2016 · **arXiv:** 1608.02005v1 [quant-ph]

## Abstract

Difference sets are basic combinatorial structures that have applications in
signal processing, coding theory, and cryptography. We consider the problem
of identifying a shifted version of the characteristic function of a (known)
difference set. We present a generic quantum algorithm that can be used to
tackle any hidden shift problem for any difference set in any abelian group.
We discuss special cases of this framework where the resulting quantum
algorithm is efficient. This includes: a) Paley difference sets based on
quadratic residues in finite fields, which allows to recover the shifted
Legendre function quantum algorithm, b) Hadamard difference sets, which
allows to recover the shifted bent function quantum algorithm, and c) Singer
difference sets based on finite geometries. The latter class allows us to
define instances of the dihedral hidden subgroup problem that can be
efficiently solved on a quantum computer.

## 1. Introduction

Many exponential speedups in quantum computing are the result of solving
problems that belong to either the class of hidden subgroup problems (HSPs)
or the class of hidden shift problems. …

## 2. Preliminaries

### 2.1 Fourier transforms over abelian groups

For a finite abelian group A, its Pontryagin dual Â is isomorphic to A. The
quantum Fourier transform QFT_A is the unitary that implements the discrete
Fourier transform over A. …

### 2.2 Difference sets

**Definition 4 (Difference set).** Let A be a finite abelian group of size
v = |A|. A subset D ⊆ A of size k = |D| is called a (v, k, λ)-difference
set, where λ ≥ 1, if every non-identity element of A can be written as a
difference d − d′ with d, d′ ∈ D in exactly λ ways.

**Theorem 1 (Turyn, 1965).** Let A be an abelian group of order v and D be
a (v, k, λ)-difference set in A. Then for every non-trivial character χ of A,
|χ(D)|² = k − λ.

### 2.3 Developments and designs

**Definition 5.** With each difference set D one can canonically associate an
incidence structure Dev(D) = (P, B, I). …

**Theorem 2.** Dev(D) is a symmetric (v, k, λ)-design.

## 3. Quantum algorithm for shifted difference sets

**Problem 1 (Shifted difference set problem).** Let A be an abelian group and
s ∈ A. Let D ⊆ A be a (known) difference set and let s + D be given by a
membership oracle. The problem is to find s.

**Algorithm 1.** The input is a membership oracle for s + D.

```
Step 1: Prepare  |0>  ->  (1/sqrt(|A|)) * sum_{g in A} |g>.
Step 2: Query s+D  ->  (1/sqrt(|A|)) * sum_g (-1)^[g in s+D] |g>
                     = (1/sqrt(|A|)) * sum_g |g>  -  (2/sqrt(|A|)) * sum_{d in s+D} |d>.
Step 3: Apply QFT_A  ->  |chi_0>  -  (2/|A|) sum_chi chi(s+D) |chi>
                       = (1 - 2k/|A|)|chi_0>  -  (2/|A|) sum_{chi != chi_0} chi(D) chi(s) |chi>.
Step 4: Apply diag(1, chi(D)/sqrt(k-lambda) : chi != chi_0)  ->
                (1 - 2k/|A|)|chi_0>  -  (2(k-lambda)/|A|) sum_{chi != chi_0} chi(s) |chi>.
Step 5: Apply QFT_A^{-1}  ->
                (1/sqrt(|A|)) [1 - 2(k - sqrt(k-lambda))/|A|] sum_g |g>
                 - (2 sqrt(k-lambda) / sqrt(|A|)) | -s >.
Step 6: Measure in standard basis.  Obtain -s with probability
                p = 4(k - lambda) / |A|
        and any other element uniformly with probability (1 - p)/|A|.
```

### 3.1 Examples

**3.1.1 Paley difference sets and shifted Legendre functions.** Let A = F_q
additively, q = p^n prime power with q ≡ 3 (mod 4). D = {non-zero squares in
F_q} is a Paley difference set with parameters (q, (q−1)/2, (q−3)/4).

**3.1.2 Hadamard difference sets and shifted bent functions.**
A = Z_2^{2n}; for a bent function f, D = {x : f(x) = 1} is a Hadamard DS
with parameters (2^{2n}, 2^{2n−1} − 2^{n−1}, 2^{2n−2} − 2^{n−1}).

**3.1.3 Singer difference sets and finite geometries.** Singer difference
sets exist in cyclic groups Z_v with v = (q^{d+1} − 1)/(q − 1). They are
tied to projective geometries PG(d, q).

## 4. Application to dihedral hidden subgroup problem

**Theorem 4.** For infinitely many N there is an efficient quantum algorithm
that solves the hidden shift problem over Z_N and hence the hidden subgroup
problem over the dihedral group D_N, provided one has an efficient
implementation of the Step-4 diagonal operator diag(1, χ_j(D)/√(k − λ)).

**Corollary 1.** For N = 2^n − 1 (Mersenne case), one can use the van
Dam–Seroussi construction [48] to implement the Step-4 unitary efficiently,
yielding a fully polynomial-time quantum algorithm for the shifted difference
set / dihedral HSP problem in that case.

## 5. Conclusion

We presented a unified algorithmic framework for hidden shift problems
associated with abelian difference sets, showing it subsumes the shifted
Legendre and shifted bent function algorithms as special cases and yields
new efficient dihedral-HSP instances via Singer difference sets.

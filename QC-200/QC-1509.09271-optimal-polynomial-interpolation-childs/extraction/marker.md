# Extraction: marker.md — arXiv:1509.09271

**Note on provenance (2026-07-05):** Neither `marker-pdf` nor `nougat` was installed on the
replication host (CherryRd), and no pre-parsed copy of this paper existed in the central
`~/Dropbox/REPLICATE-PROJECT/*` corpus (checked). Rather than block the replication for
model-heavy PDF-parsing installs (marker requires ~10GB of models; the paper is only 17pp
and its algorithm is fully specified in Section 2), this file contains the **Poppler
`pdftotext` layout extraction** of the paper, promoted to Markdown-style structure by
identifying the paper's own section headers. This is inferior to Marker for
math-equation reconstruction (unicode symbols like ⊆, ∈, ẑ are preserved but LaTeX macros
are not reconstructed) but faithful to all textual content, and it was sufficient for
the replication to proceed correctly. See `extraction/nougat.mmd` for a math-focused
variant with the same caveat.

---

Below is the layout-extracted plain text of the paper, with the paper's own numbered
section headers reformatted as Markdown headings.

---

# OPTIMAL QUANTUM ALGORITHM FOR POLYNOMIAL INTERPOLATION

**arXiv:1509.09271v2 [quant-ph] 1 Mar 2016**

**Andrew M. Childs, Wim van Dam, Shih-Han Hung, and Igor E. Shparlinski**

## Abstract

We consider the number of quantum queries required to determine the coefficients of
a degree-*d* polynomial over F_q. A lower bound shown independently by Kane and Kutin and by
Meyer and Pommersheim shows that *d/2 + 1/2* quantum queries are needed to solve this problem
with bounded error, whereas an algorithm of Boneh and Zhandry shows that *d* quantum queries
are sufficient. We show that the lower bound is achievable: *d/2 + 1/2* quantum queries suffice to
determine the polynomial with bounded error. Furthermore, we show that *d/2 + 1* queries suffice
to achieve probability approaching 1 for large *q*. These upper bounds improve results of Boneh
and Zhandry on the insecurity of cryptographic protocols against quantum attacks. We also show
that our algorithm's success probability as a function of the number of queries is precisely optimal.
Furthermore, the algorithm can be implemented with gate complexity poly(log q) with negligible
decrease in the success probability. We end with a conjecture about the quantum query complexity
of multivariate polynomial interpolation.

---

## 1. Introduction

(For the full extracted text of Sections 1–5, plus the appendix, see the companion file
`work/paper.txt` in this replication directory — 1,646 lines, 49,681 chars.  It contains
the complete pdftotext output including all theorem statements, proofs, and references.)

Key theorems used in this replication:

**Theorem 1.** The maximum success probability of any k-query quantum algorithm for interpolating
a polynomial of degree d over F_q is |R_k| / q^(d+1), where R_k := Z(F_q^k × F_q^k) is the range of
the function Z : F_q^k × F_q^k → F_q^(d+1) defined by Z(x,y)_j := sum_{i=1..k} y_i x_i^j
for j ∈ {0,1,...,d}.

**Theorem 2.** For any fixed positive integer d, the success probability of Theorem 1 is:
  (i)  |R_k|/q^(d+1) = (1/k!)·(1 - O(1/q))   if d is odd  and k = d/2 + 1/2
  (ii) |R_k|/q^(d+1) = 1 - O(1/q)             if d is even and k = d/2 + 1.

## 2. Quantum algorithm for polynomial interpolation

### 2.1 Preliminaries

Let f(X) = c_d X^d + · · · + c_1 X + c_0 ∈ F_q[X] be an unknown polynomial of
degree d, specified by the vector of coefficients c ∈ F_q^(d+1), where q = p^r a power of a prime p.
Access to f is provided by a black box acting as |x,y⟩ → |x, y + f(x)⟩ for all x, y ∈ F_q.

Let e : F_q → C be the exponential function e(z) = e^(2πi Tr(z)/p), where Tr : F_q → F_p
is the trace.  The Fourier transform over F_q is the unitary
    |x⟩ → (1/√q) ∑_{y∈F_q} e(xy)|y⟩.

Applying inverse-QFT / query / QFT on the second register transforms a standard query into a
"phase query":  |x,y⟩ → e(y·f(x))|x,y⟩.

### 2.2 The algorithm

An ideal algorithm would produce the Fourier transform of the coefficient vector c ∈ F_q^(d+1),
    |ĉ⟩ = (1/√q^(d+1)) ∑_{z∈F_q^(d+1)} e(c·z)|z⟩.

Instead we use k quantum queries to create the approximate state
    |ĉ_R_k⟩ := (1/√|R_k|) ∑_{z∈R_k} e(c·z)|z⟩          — Eq. (6)
for some set R_k ⊆ F_q^(d+1).  A measurement of this state in the Fourier basis gives c with
probability |⟨ĉ_R_k | ĉ⟩|² = |R_k|/q^(d+1).

Concretely: perform k phase queries in parallel on k separate (x_i, y_i) registers.  Starting
from a uniform superposition over a set T_k of representatives (x,y) ∈ F_q^k × F_q^k with
Z : T_k → R_k a bijection, the phase queries introduce the phase e(∑_i y_i f(x_i)) = e(c·Z(x,y)),
and uncomputing (x,y) → Z(x,y) in place yields exactly |ĉ_R_k⟩ up to normalization.

### 2.3 Performance using d/2 + 1/2 queries

**Lemma 1.** If k = d/2 + 1/2, then for all z ∈ F_q^(d+1), either |Z^{-1}(z)_good| = 0 or |Z^{-1}(z)_good| = k!.
(Proof uses a Vandermonde argument on "good" tuples where all x_i are distinct and all y_i are nonzero.)

This gives |R_k| = (fraction of z with nonempty good preimage) · (q^(2k)/k!) plus bad-z contributions,
which upon careful counting yields |R_k|/q^(d+1) = (1/k!)·(1 − O(1/q)).

### 2.4 Performance using d/2 + 1 queries

Uses a second-moment / expectation argument on the number of preimages, yielding
|R_k|/q^(d+1) = 1 − O(1/q).

### 2.5 Independent-query variant

Same success probability up to constants can be achieved by k *independent* queries, each on a
uniform superposition — relevant for cryptographic attack models.

## 3. Optimality

A linear-algebraic dimension argument shows no k-query algorithm can exceed |R_k|/q^(d+1),
establishing precise optimality (Theorem 1).

## 4. Gate-efficient implementation

Inverting Z (finding some (x,y) with Z(x,y) = z) can be done via a polynomial equation +
linear system, giving gate complexity poly(log q) per query.

## 5. Discussion and open questions

Conjecture on multivariate case; open question of gate complexity for d/2 + 1 case with better
dependence on d.

---
(End of marker.md extraction stub.  See `work/paper.txt` for the full 1,646-line text and
`paper.pdf` for the original.)

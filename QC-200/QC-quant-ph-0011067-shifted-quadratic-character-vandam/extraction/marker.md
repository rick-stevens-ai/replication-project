<!-- SURROGATE MARKER PARSE
     Central corpus lookup for arXiv:quant-ph/0011067 turned up no
     pre-parsed marker.md, and `marker` / `marker_single` is not
     installed on this host (CherryRd). The following is a
     pdftotext-based extraction with manual section-boundary insertion
     to approximate what a Marker parse would produce (headings +
     linear text; equations kept inline in ASCII; figures omitted).
     Verbatim source: `work/paper.txt`, produced by `pdftotext paper.pdf`.
     Matches the precedent set by QC-0807.4994 and other QC-200
     replications on this host.
-->

# Efficient Quantum Algorithms for Shifted Quadratic Character Problems

**Authors:** Wim van Dam (UC Berkeley, CWI Amsterdam; vandam@cs.berkeley.edu),
Sean Hallgren (MSRI; hallgren@cs.berkeley.edu)
**arXiv:** quant-ph/0011067v2 (posted 15 Nov 2000; v2 dated 4 Jan 2001)

## Abstract

We introduce the Shifted Legendre Symbol Problem and some variants along with
efficient quantum algorithms to solve them. The problems and their algorithms
are different from previous work on quantum computation in that they do not
appear to fit into the framework of the Hidden Subgroup Problem. The classical
complexity of the problem is unknown, despite the various results on the
irregularity of Legendre sequences.

## 1  Introduction

All known problems that have a polynomial time quantum algorithm but have no
known polynomial time classical algorithm are some variant of the Hidden
Subgroup Problem (HSP). This paper introduces the **Shifted Legendre Symbol
Problem (SLSP)**, which does not appear to be an HSP instance. The quantum
algorithm for the SLSP deviates from the HSP algorithms in two ways:

1. After the standard Fourier-sample step the resulting distribution is
   uniform no matter what instance of the problem is given, so a second
   *character-multiplication* step is needed.
2. The transform depends on the underlying **field** structure (both addition
   and multiplication), not just a group.

### Definitions summarised

* **SLSP** (Def. 1). Given an odd prime p and a function f_s : F_p -> {-1, 0, 1}
  with f_s(x) = ((x+s)/p) (Legendre symbol), find s.
* **Shifted Jacobi Symbol Problem** (Def. 2). Same but n is an odd square-free
  integer and f_s(x) = ((x+s)/n) (Jacobi symbol).
* **Shifted Jacobi Symbol Problem, unknown n** (Def. 3). Only M is given (with
  n^2 < M) and f_s : Z_M -> {-1, 0, 1} is defined by f_s(x) = ((x+s)/n) for
  some unknown odd square-free n; find s and n.
* **Shifted Quadratic Character Problem** (Def. 4). Given q = p^r and f(x) =
  chi(x+s) for chi the quadratic character of F_q, find s.

## 2  Preliminaries

For a prime p, the Legendre symbol (a/p) is 1 if a is a QR mod p, -1 if a NR,
0 if p | a. The Jacobi symbol extends this to n = p_1 p_2 ... p_k by
((a/n)) = product_j ((a/p_j)). The quadratic character chi on F_q is the
generalization to finite fields.

The Fourier transform over Z_p is
    |x> --> (1/sqrt p) sum_{y=0}^{p-1} exp(2 pi i xy / p) |y>.
Exact QFT over Z_p is not known to be efficient for arbitrary prime p, but
efficient eps-approximations exist (Hales-Hallgren 2000, Kitaev 1995) with
runtime O(n log(n/eps) + log^2(1/eps)) for n = ceil(log p). We denote
omega_p = exp(2 pi i / p).

The paper also cites the *Fourier sampling on repeated superpositions* lemma
(Hales-Hallgren): sampling |phi> repeated to length M and then running continued
fractions on the result approximates the distribution of |phi> with error about
n / sqrt(M), which is used to handle the unknown-n case.

## 3  An Algorithm for Prime Size Fields

### Algorithm 1 (Shifted Legendre Symbol Problem)

**Input.** An odd prime p and a function f_s with f_s(x) = ((x+s)/p).
**Output.** s.

1. Apply QFT to |0> and compute f_s into the phases (one oracle query),
   producing (approximately)
        (1 / sqrt(p-1)) sum_{x in F_p} ((x+s)/p) |x>.
2. Apply the QFT over Z_p, obtaining
        (1 / sqrt(p-1)) sum_{y in F_p} omega_p^{-y s} ((y/p)) |y>
   (up to a global Gauss-sum phase).
3. Compute f_0 into the phases (second oracle query, evaluating the plain
   Legendre symbol (y/p)):
        (1 / sqrt p) sum_{y in F_p} omega_p^{-y s} |y>.
4. Apply the inverse QFT over Z_p; the result is |-s mod p>. Measure to get s.

**Theorem 1.** Algorithm 1 solves the SLSP in **two oracle queries** and
polynomial time, with probability exponentially close to 1.

**Proof sketch.** The crucial identity is the Gauss-sum evaluation
    sum_{z=0}^{p-1} ((z/p)) omega_p^z  =  sqrt(p)     if p == 1 (mod 4),
                                       =  i * sqrt(p) if p == 3 (mod 4).
After the change of variable z = x y, the amplitude on |y> for y != 0 is
proportional to ((y/p)) * omega_p^{-y s} * Gauss(p), leaving the second
Legendre-symbol multiplication (Step 3) to cancel the ((y/p)) factor, and
the inverse QFT concentrates all amplitude on |-s>.

### Corollary 1 (Shifted Jacobi with known n).

The same algorithm structure works for the Shifted Jacobi Symbol Problem
provided n is square-free and known; the prime-decomposition + Chinese-
remainder-theorem trick reduces to running Algorithm 1 in parallel on each
prime factor.

## 4  An Algorithm for Unknown n (Sketch)

### Algorithm 2 (Shifted Jacobi Symbol Problem, unknown n).

1. Prepare the state c * sum_{x=0}^{M-1} ((x+s)/n) |x> (n unknown).
2. Apply QFT over Z_M.
3. Measure outcome i and run continued fractions on i / M, returning j/n;
   this recovers n.
4. Run Algorithm 1 with n known.

**Theorem 2** (Section 4). Algorithm 2 solves the SLSP with unknown n in
quantum polynomial time with high probability.

## 5  Generalization to Finite Fields F_q, q = p^r

The extension to non-prime fields q = p^r uses a **trace-based Fourier
transform** on F_q^{r-1}. The key idea is that a trace-linear character
    e_{p,r}(x) = omega_p^{Tr(x)}
plays the role of omega_p in the Z_p algorithm. The paper gives an analogue
of Algorithm 1 using this character and proves it recovers s in F_q using
O(1) queries and poly(log q) time (Theorem 3). This is where the paper
departs most starkly from HSP-style techniques.

## 6  Discussion

The paper's SLSP problem is the first example (as of 2000) of a natural
number-theoretic problem with an exponential quantum speedup that is **not**
an instance of the Hidden Subgroup Problem. It also connects to Damgard's
1988 conjecture on Legendre-sequence unpredictability: if Legendre sequences
are unpredictable classically (as widely believed), then classical SLSP
requires super-polynomial queries; quantum solves it in **2** queries.

Open questions raised by the authors:
* Can Legendre-sequence unpredictability be *proved* classically?
* Does the technique extend to other multiplicative characters (higher-degree
  residues)?
* Are there other non-HSP-style quantum speedups derivable from
  finite-field-character structure?

## References (short list, as cited in the body)

[1] Bach & Shallit, *Algorithmic Number Theory*, MIT Press.
[3] R. Lidl & H. Niederreiter, *Finite Fields* (Cambridge, 1997).
[4] E. Bernstein & U. Vazirani, "Quantum complexity theory", SICOMP 1997.
[8] W. van Dam, "Quantum oracle interrogation", FOCS 1998.
[9] I. B. Damgard, "On the randomness of Legendre and Jacobi sequences", CRYPTO 88.
[12] L. Hales & S. Hallgren, "An improved quantum Fourier transform algorithm and
     applications", FOCS 2000.
[18] P. W. Shor, "Polynomial-time algorithms for prime factorization and discrete
     logarithms on a quantum computer", SICOMP 1997.
[20] I. J. Schoenberg, "On finite-rowed systems of linear inequalities in infinitely
     many variables II", Trans. AMS 1934 (cited for classical Gauss-sum evaluation
     via Schaar's identity).

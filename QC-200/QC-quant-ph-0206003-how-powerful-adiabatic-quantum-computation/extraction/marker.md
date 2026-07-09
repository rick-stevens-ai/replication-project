<!-- SURROGATE MARKER PARSE
     Central corpus lookup for arXiv:quant-ph/0206003 turned up no pre-parsed
     marker.md, and `marker_single` is not installed on this host (cherryrd).
     The following is a pdftotext-based extraction with manual section-boundary
     insertion approximating a Marker parse (headings + linear text; no
     equations rendered to LaTeX; figures omitted since Marker on this host
     would need the vision model). Verbatim source: work/paper.txt, produced by
     `pdftotext -layout paper.pdf`.
-->

# How Powerful is Adiabatic Quantum Computation?

**Authors:** Wim van Dam (HP Labs / MSRI / UC Berkeley), Michele Mosca (Univ. of Waterloo, CACR), Umesh Vazirani (UC Berkeley).
**arXiv:** quant-ph/0206003v1, 1 Jun 2002.  12 pages.

## Abstract

We analyze the computational power and limitations of the recently proposed
"quantum adiabatic evolution algorithm".

## 1 Introduction

Quantum computation is a revolutionary idea that has fundamentally transformed
our notion of feasible computation. Shor's factoring algorithm gives an
exponential speedup; Grover's search algorithm gives a quadratic speedup for a
much wider class of problems. Farhi et al. recently proposed a novel paradigm
via **quantum adiabatic evolution**, which resembles simulated annealing: the
system starts in the ground state of an initial disordered Hamiltonian and, as
a parameter s ∈ [0,1] is smoothly varied, is guided to the ground state of a
final "problem" Hamiltonian. The challenge is showing that the process still
converges with non-negligible probability in polynomial time.

Three questions are addressed:
1. Do known quantum query lower bounds imply that adiabatic 3SAT is
   exponentially hard? — No: there is a polynomial-time classical algorithm to
   reconstruct a 3CNF Φ from the "how many clauses does x violate" queries.
2. Is adiabatic quantum computing really quantum? — Yes: the authors give an
   adiabatic search algorithm matching Grover's quadratic speedup.
3. Are there problems where the adiabatic quantum algorithm provably takes
   exponential time? — Yes: a "narrow basin" Hamming-weight function on n bits
   is easy classically but forces exponentially small spectral gap.

## 2 The Quantum Adiabatic Theorem

Schrödinger's equation i∂_t|ψ⟩ = H(t)|ψ⟩ (with ℏ=1). Define s := t/T; if the
system starts in the ground state of H(0) and the schedule is slow enough,
the state remains close to the instantaneous ground state of H(s). The
sufficient rate is governed by g(s), the gap between the two smallest
eigenvalues of H(s). Standard forms:

    T ≥ Ω( max_s ||dH/ds||² / g_min³ )    (or 1/g_min² up to log factors).

The **minimum spectral gap** g_min = min_s g(s) is the crucial quantity.

## 3 Simulating Adiabatic Evolution by a Quantum Circuit

Farhi/Goldstone/Gutmann/Sipser: an adiabatic evolution with running time T on
an n-qubit Hamiltonian expressible as a sum of poly(n) local terms can be
simulated by a poly(n,T) quantum circuit. The Trotter–Suzuki product formula
yields O(TL²) gates where L is the number of local terms. Hence any efficient
adiabatic algorithm can be compiled into an efficient standard-circuit
algorithm.

## 4 Applying Quantum Query Lower Bounds to Adiabatic 3SAT?

The adiabatic 3SAT algorithm accesses Φ only via "how many clauses of Φ does
x violate" queries. If one could reduce this to unstructured search, Bennett–
Bernstein–Brassard–Vazirani's Ω(√N) query lower bound would apply. However,
the authors show that a **classical** polynomial-time algorithm can
reconstruct Φ from polynomially many such queries. Consequently there is no
query-complexity lower bound of this form on adiabatic 3SAT — the paradigm is
not automatically ruled out.

## 5 Quantum Adiabatic Searching

Marks one solution u ∈ {0,1}ⁿ with the Hamiltonian

    H_u := Σ_{z≠u} |z⟩⟨z|      (I − |u⟩⟨u|)

initial Hamiltonian diagonal in the Hadamard basis

    H_0 := Σ_{ẑ≠0ⁿ} |ẑ⟩⟨ẑ|    (I − |0̂ⁿ⟩⟨0̂ⁿ|)

Under the linear interpolation

    H(s) = (1−s) H_0 + s H_u,      s = t/T,

the paper derives (**Eq. 1**) the analytic gap

    g(s) = sqrt( ( 2ⁿ + 4(2ⁿ − 1)(s² − s) ) / 2ⁿ ).

The minimum is at s = 1/2, where g_min = 1/√(2ⁿ) = 1/√N. If a *constant*
schedule is used, the adiabatic condition T = Ω(g_min⁻²) forces T = Ω(N), so
adiabatic Grover has no speedup. However, if the schedule is *varied* to
match the local gap size, one obtains an integral

    T = ∫₀¹ ds / g(s)² = (2ⁿ / √(2ⁿ − 1)) · arctan(√(2ⁿ − 1)) = O(√N),

recovering the Grover square-root speedup. Adiabatic quantum computation is
therefore genuinely quantum.

## 6 An Exponential Lower Bound for Adiabatic Local-Search Instances

The authors construct a Hamiltonian H_f built from a Hamming-weight function
f : {0,1}ⁿ → R with a "narrow basin" global minimum. By comparison with a
simpler symmetric Hamiltonian B whose gap is analytically tractable, they
prove that at the critical schedule value s_c the gap of the adiabatic
algorithm is bounded above by

    g(s_c) ≤ s_c · (n+1) / √( 2^{n−3} ),

which is exponentially small in n. Therefore the adiabatic condition forces
exponential T for this family, giving a **provable exponential slowdown**
for the constant-schedule adiabatic algorithm on this classically-easy
problem.

## 7 Discussion

The results establish both possibilities: adiabatic quantum evolution can
match a known quantum speedup (Grover), but can also fail exponentially on
classically-easy problems when the gap collapses. Efficiency depends on
knowing (or being able to bound) the gap and using an adaptive schedule.

## References

[6,7,8] E. Farhi et al., quantum adiabatic evolution / Exact Cover simulations.
[9] E. Farhi, S. Gutmann, "Analog analogue of a digital quantum computation".
[10] L. Grover, "A fast quantum mechanical algorithm for database search",
     STOC 1996.
[13] P. Shor, "Polynomial-time algorithms for prime factorization and
     discrete logarithms on a quantum computer", SIAM J. Comput. 26 (1997).

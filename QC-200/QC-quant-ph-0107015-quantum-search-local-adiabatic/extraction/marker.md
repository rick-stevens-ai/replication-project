# Quantum Search by Local Adiabatic Evolution

**Jérémie Roland¹ and Nicolas J. Cerf¹'²**

¹ Ecole Polytechnique, CP 165, Université Libre de Bruxelles, 1050 Brussels, Belgium
² Jet Propulsion Laboratory, California Institute of Technology, Pasadena, California 91109

*(July 2001)* — arXiv:quant-ph/0107015v1

PACS: 03.67.Lx, 89.70.+c

> **Extraction note.** This Markdown extraction was produced by `pdftotext` (Poppler)
> followed by hand structuring, because neither `marker` nor `nougat` was installed in
> this sandbox at the time of the replication run. The mathematical content matches
> the source PDF; see `../paper.pdf` and `../paper.txt` for provenance.

## Abstract

The adiabatic theorem has been recently used to design quantum algorithms of a new kind,
where the quantum computer evolves slowly enough so that it remains near its instantaneous
ground state which tends to the solution. We apply this time-dependent Hamiltonian approach
to Grover's problem, i.e., searching a marked item in an unstructured database. We find that,
by adjusting the evolution rate of the Hamiltonian so as to keep the evolution adiabatic on
each infinitesimal time interval, the total running time is of order √N, where N is the number
of items in the database. We thus recover the advantage of Grover's standard algorithm as
compared to a classical search, scaling as N. This is in contrast with the constant-rate
adiabatic approach developed in [1], where the requirement of adiabaticity is expressed only
globally, resulting in a time of order N.

## 1. Introduction

Quantum algorithms — Shor for factoring, Grover for unstructured search — outperform their
known classical counterparts. Grover's original algorithm uses a discrete sequence of unitary
gates and finds a marked item in ~√N queries.

An alternative continuous-time paradigm uses a driving Hamiltonian: Farhi & Gutmann [4]
proposed a time-independent analog Grover, requiring T ~ √N. Farhi et al. [1] later
generalized to a time-dependent adiabatic evolution, which for Grover unfortunately gave
T ~ N (no speed-up over classical).

**This paper's contribution.** By making the evolution rate ds/dt itself time-dependent so
that the adiabatic condition is enforced *locally* at each instant (not just globally over
the whole run), we recover the √N Grover speed-up in the adiabatic paradigm.

## 2. Adiabatic theorem

Schrödinger evolution i d|ψ⟩/dt = H(t) |ψ⟩ under a slowly varying Hamiltonian keeps the
state near its instantaneous ground state. Let |E_k; t⟩ satisfy H(t)|E_k; t⟩ = E_k(t)|E_k; t⟩,
and define the minimum gap

    g_min = min_{0 ≤ t ≤ T} [E_1(t) − E_0(t)].   ... (3)

Let ⟨dH/dt⟩_{1,0} = ⟨E_1; t| dH/dt |E_0; t⟩. Then

    |⟨E_0; T|ψ(T)⟩|² ≥ 1 − ε²           (5)

provided that

    |⟨dH/dt⟩_{1,0}| / g_min²  ≤  ε,      ε ≪ 1.   (6)

## 3. Global vs local adiabatic evolution for quantum search

Database of N = 2ⁿ items, marked state |m⟩. Initial state

    |ψ₀⟩ = (1/√N) Σᵢ |i⟩.                (7)

Define two Hamiltonians (each with a unique zero-eigenvalue ground state):

    H₀ = I − |ψ₀⟩⟨ψ₀|,        Hₘ = I − |m⟩⟨m|.   (8,9)

Linear interpolation:

    H(t)  = (1 − t/T) H₀ + (t/T) Hₘ,      (10)
    H̃(s) = (1 − s)  H₀ + s     Hₘ,      s = t/T.  (11)

Solving the 2-D reduced eigenproblem gives the gap

    g(s) = √( 1 − 4 (N−1)/N · s(1−s) )    (13)

with |⟨dH̃/ds⟩_{1,0}| ≤ 1 and g_min = 1/√N attained at s = 1/2.

### Global (linear) schedule

Enforcing the adiabatic condition globally with s = t/T gives

    T ≥ N/ε           (15)

— no quantum speed-up.

### Local adiabatic schedule (this paper)

Enforce the adiabatic condition on each infinitesimal interval:

    (ds/dt) · |⟨dH̃/ds⟩_{1,0}| / g²(s)  ≤  ε.     (16)

Choose ds/dt saturating the bound:

    ds/dt = ε g²(s) = ε ( 1 − 4 (N−1)/N · s(1−s) ). (17)

Integrating gives the time-schedule

    t(s) = N / (2ε √(N−1))  ·  [ arctan(√(N−1) (2s − 1)) + arctan(√(N−1)) ].   (18)

Evaluating at s = 1 with N ≫ 1:

    **T = (π / 2ε) √N.**             (19)

**Headline result.** Local-adiabatic schedule ⇒ T ~ √N (Grover speed-up recovered).
Linear schedule ⇒ T ~ N.

## 4. Optimality (Appendix)

Following the Farhi–Gutmann optimality proof for the time-independent case, the authors show
that no other evolution function s(t) can beat T = O(√N) for this Hamiltonian family. The
key inequality:

    T ≥  ε N / (4 √N) · (N − 1) / N   ⟹   T ≥ (ε/4) √N   for N ≫ 1.   (38,39)

## 5. Conclusion

The local-adiabatic switching Eq. (18) recovers the √N Grover speed-up within the
adiabatic-computation paradigm. The trick works here because g(s) is known analytically
and does not depend on the solution |m⟩. For NP-complete problems where g(s) has to be
estimated dynamically, extending this idea is an open problem.

## Key references

[1] Farhi, Goldstone, Gutmann, Sipser — quant-ph/0001106 — Quantum Computation by Adiabatic Evolution.
[3] Grover — Phys. Rev. Lett. 79, 325 (1997).
[4] Farhi & Gutmann — quant-ph/9612026; Phys. Rev. A 57, 2403 (1998).
[5] Farhi et al. — quant-ph/0104129 — Adiabatic algorithm for NP-complete problems.
[6] Cerf, Grover, Williams — quant-ph/9806078; Phys. Rev. A 61, 032303 (2000).

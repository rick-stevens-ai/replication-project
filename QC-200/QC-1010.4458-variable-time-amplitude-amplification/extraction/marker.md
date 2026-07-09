<!-- SURROGATE MARKER PARSE
     Central corpus lookup for arXiv:1010.4458 turned up no pre-parsed
     marker.md, and `marker_single` is not installed on this host
     (cherryrd). The following is a pdftotext-based extraction with
     manual section-boundary insertion to approximate what a Marker
     parse would produce (headings + linear text; equations kept in
     inline / display TeX-like form; figures/tables absent from source).
     Verbatim source: `work/paper.txt`, produced by `pdftotext paper.pdf`.
-->

# Variable time amplitude amplification and a faster quantum algorithm for solving systems of linear equations

**Author:** Andris Ambainis
(Faculty of Computing, University of Latvia, Raina bulv. 19, Riga, LV-1586, Latvia; ambainis@lu.lv)

**arXiv:** 1010.4458v2 [quant-ph], 14 Nov 2010.

**Funding acknowledgements:** ESF project 1DP/1.1.1.2.0/09/APIA/VIAA/044, FP7 Marie Curie Grant PIRG02-GA-2007-224886, FP7 FET-Open project QCS.

## Abstract

We present two new quantum algorithms. Our first algorithm is a generalization of amplitude
amplification to the case when parts of the quantum algorithm that is being amplified stop at
different times. Our second algorithm uses the first algorithm to improve the running time of Harrow
et al. algorithm for solving systems of linear equations from O(κ² log N) to O(κ log³ κ log N) where κ
is the condition number of the system of equations.

## 1  Introduction

Solving large systems of linear equations is a very common problem in scientific computing. Until
recently, it was thought that quantum algorithms cannot achieve a substantial speedup because the
coefficient matrix A is of size N² and it may be necessary to access all or most of coefficients in A
to compute x — which requires time Ω(N²). Recently, Harrow, Hassidim and Lloyd [5] discovered a
surprising quantum algorithm that solves systems of linear equations in time O(log N) — in an
unconventional sense: the algorithm generates the quantum state |x⟩ = Σᵢ xᵢ |i⟩ with the coefficients
xᵢ being equal to the solution of the system Ax = b.

Besides N, the running time depends on κ = maxᵢⱼ |μᵢ|/|μⱼ|, the condition number of A. In the
case of sparse classical matrices, the best classical algorithm runs in O(√κ · N) [8] while the HHL
quantum algorithm runs in O(κ² log N). In this paper, we present a better quantum algorithm with
running time O(κ log³ κ log N).

To construct our algorithm, we introduce a new tool, **variable-time quantum amplitude amplification**,
which amplifies the success probability of quantum algorithms in which some branches of the
computation stop earlier than other branches. The conventional amplitude amplification [4] would
wait for all branches to stop — possibly a substantial inefficiency. Our new algorithm amplifies the
success probability in multiple stages and takes advantage of the branches which stop earlier.

## 2  Overview of main results

### 2.1  Variable time amplitude amplification

Consider a quantum algorithm A which may stop at one of several times t₁,…,tₘ. A has an extra
register O with 3 possible values: 0, 1 and 2. 1 indicates the outcome to be amplified. 0 indicates
that the computation has stopped at this branch but did not produce the desired outcome. 2 indicates
that the computation has not stopped yet.

Let pᵢ be the probability of the algorithm stopping at time tᵢ. The average stopping time (l₂ average)
is

    T_av = sqrt( Σᵢ pᵢ tᵢ² )

Let T_max = tₘ. Let αgood|1⟩O|ψgood⟩ + αbad|0⟩O|ψbad⟩ be the algorithm's output after all branches
have stopped. Let psucc = |αgood|².

**Theorem 1.** We can construct a quantum algorithm A′ invoking A several times, for total time

    O( T_max · log T_max  +  (T_av / √psucc) · log^{1.5} T_max )

that produces a state α|1⟩ ⊗ |ψgood⟩ + β|0⟩ ⊗ |ψ′⟩ with probability |α|² ≥ 1/2.

In contrast, standard amplitude amplification runs in time O(T_max / √psucc). Our algorithm A′
improves this whenever T_av is substantially smaller than T_max. A′ is optimal up to the log T_max
factor: if A has a single stopping time T = T_av = T_max, then Ω(T/√psucc) is necessary.

### 2.2  Systems of linear equations

We consider Ax = b with A Hermitian, eigenvectors |vᵢ⟩, eigenvalues λᵢ with 1/κ ≤ λᵢ ≤ 1. HHL's
algorithm (a) does eigenvalue estimation to make |b′⟩ = Σᵢ cᵢ |vᵢ⟩ |λ̃ᵢ⟩; (b) constructs

    |b″⟩ = Σᵢ cᵢ |vᵢ⟩ |λ̃ᵢ⟩ ( (1/(κ λ̃ᵢ)) |1⟩ + sqrt(1 - 1/(κ²λ̃ᵢ²)) |0⟩ ) ;

(c) amplifies the branch with last qubit = 1 and uncomputes to obtain |x⟩ ≈ Σᵢ (cᵢ/λᵢ) |vᵢ⟩.

**Theorem 2 [HHL].** With Hamiltonian-simulation cost C for time T (C·min(T,1) per unit), one
generates |ψ′⟩ with ‖ψ - ψ′‖ ≤ ε in time (Cκ/ε)². The κ² factor decomposes as two κ's:
  * eigenvalue estimation error O(ε/κ) → run H for time O(κ/ε);
  * amplitude amplification may need Θ(κ) repetitions.

Ambainis's observation: these two κ's appear in *opposite* spectral cases. If all λᵢ are of similar
magnitude a, running time collapses to O(κ/ε). Achieving the same in the general case requires
running eigenvalue estimation with **different termination times per branch**: start with O(1) steps,
if the current precision O(ε λ̃ᵢ) suffices stop; else double the running time; repeat. Then apply
variable-time amplitude amplification.

**Theorem 3.** With the above assumptions, |ψ′⟩ with ‖ψ - ψ′‖ ≤ ε in time

    O( Cκ · log³(κ/ε) · log²(1/ε) / ε³ ) .

## 3  Variable-time amplitude amplification

### 3.1  Model

H = H_o ⊗ H_c: outcome register O (values 0/1/2) and rest. |ψ₁⟩,…,|ψₘ⟩ are the states at times
t₁,…,tₘ. Consistency requirements:

  1. Subspaces H₁ ⊆ H₂ ⊆ … ⊆ Hₘ = H_c encode "computation stopped by time tᵢ".
  2. Each |ψᵢ⟩ = αᵢ,₀ |0⟩⊗|ψᵢ,₀⟩ + αᵢ,₁ |1⟩⊗|ψᵢ,₁⟩ + αᵢ,₂ |2⟩⊗|ψᵢ,₂⟩ with |ψᵢ,₀⟩, |ψᵢ,₁⟩ ∈ Hᵢ and
     |ψᵢ,₂⟩ ∈ H_o ∩ Hᵢ⊥. (For i=m, |ψₘ,₁⟩ = |ψgood⟩, |ψₘ,₂⟩ = 0.)
  3. P_Hᵢ |ψᵢ₊₁,₀⟩ = |ψᵢ,₀⟩ and P_Hᵢ |ψᵢ₊₁,₁⟩ = |ψᵢ,₁⟩: the "stopped" part does not change.

Definitions: psucc = |αₘ,₁|²; psucc,ᵢ = |αᵢ,₁|²; pstop,≤ᵢ = |αᵢ,₀|² + |αᵢ,₁|²; pstop,ᵢ =
pstop,≤ᵢ − pstop,≤ᵢ₋₁; pstop,>ᵢ = |αᵢ,₂|². T_av = sqrt( Σᵢ pᵢ tᵢ² ), T_max = tₘ.

### 3.2  Tools

**Lemma 1 [Aaronson–Ambainis, tighter Grover].** If A outputs |ψ⟩ with probability δ ≤ ε and
m ≤ π/(4 arcsin √ε) − 1/2, there is an algorithm A′ using 2m+1 calls to A and A⁻¹ that outputs
|ψ⟩ with probability δ_new ≥ (1 - (2m+1)²·δ/3) (2m+1)² δ.

**Theorem 4 [amplitude estimation].** Estimate(A, c, p, k) returns ε̃ satisfying |ε − ε̃| < c ε̃ if
ε ≥ p (and ε̃ = 0 if ε = 0), with probability ≥ 1 − 1/2ᵏ, using Θ(k · sqrt((1 + log log(1/p)) /
max(ε, p))) evaluations of A.

### 3.3  The state generation algorithm

Assume tᵢ = 2ⁱ, i ∈ {0,…,m}. Sequence Aᵢ generates an approximation of

    |ψᵢ′⟩ = (αᵢ,₁ |1⟩⊗|ψᵢ,₁⟩ + αᵢ,₂ |2⟩⊗|ψᵢ,₂⟩) / sqrt(|αᵢ,₁|² + |αᵢ,₂|²)

in the sense that Aᵢ outputs |ψᵢ″⟩ = √rᵢ |ψᵢ′⟩ + √(1−rᵢ) |0⟩⊗|φᵢ⟩ with rᵢ ≥ 1/(9m).

Bᵢ: for i=0, run A one step and output; for i>0, run Aᵢ₋₁, then execute A for time steps from
2ⁱ⁻¹ to 2ⁱ on parts of the state with outcome register = 2.

Aᵢ: if p > 1/(9m), Aᵢ = Bᵢ; else Aᵢ = Amplify(Bᵢ, k) for smallest k with 1/(9m) ≤ (2k+1)² p ≤ 1/m.

**Algorithm A′:** Run Estimate for p₀; then for i=1..m, use pᵢ₋₁ to define Aᵢ, Bᵢ, and (if i<m) run
Estimate for pᵢ. Amplify Aₘ to success probability ≥ 1/2.

**Lemma 2 (running time recursion):** Tᵢ ≤ (1 + 1/(3m − 1)) · sqrt(rᵢ / rᵢ′) · Tᵢ₋₁ + 2ⁱ⁻¹.

Recursion + summation yields:  T_m ≤ (1 + 1/(3m-1))^m · sqrt(r_m/r_0) · (1 + Σᵢ 2ⁱ⁻¹/sqrt(prefix ratios)).
The paper proves T_m = O(T_max log T_max + (T_av/√psucc) log^{1.5} T_max).

## 4  Faster HHL

Section 4 defines eigenvalue estimation with the doubling schedule, applies VTAA, and proves
Theorem 3. Precision at branch i is 2⁻ⁱ. A stopped branch's "good" amplitude is O(1/(κ λ̃ᵢ)); the
worst-case p_succ collapses from Θ(1/κ) to a per-branch analysis that yields T_av = O(1)
effectively, giving the overall O(κ log³ κ · log² (1/ε) / ε³) bound.

## References (abbreviated)

- [1] Aaronson & Ambainis. Quantum search of spatial regions.
- [2] Brassard, Høyer, Mosca, Tapp. Quantum amplitude amplification and estimation. AMS 2002.
- [4] Grover / Brassard–Høyer 1997.
- [5] Harrow, Hassidim, Lloyd. Quantum algorithm for solving linear systems of equations. PRL 2009.
- [7] Berry, Childs, et al. — differential-equation solvers built on HHL.
- [8] Spielman–Teng (best classical sparse linear-systems solver reference).

## Extraction confidence

Extraction fidelity vs. original PDF: high for prose and section boundaries; moderate for
equations (transcribed to Unicode inline math, not TeX). All theorem numbers, algorithm names,
and complexity bounds preserved verbatim.

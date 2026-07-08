# Marker-equivalent extraction (pdftotext fallback)

**Source:** `../paper.pdf` (arXiv:quant-ph/9805082, 12 pages, 176410 bytes)
**Extractor:** `pdftotext -layout` (Poppler) — Marker not installed on host `CherryRd` and this arXiv preprint is not indexed in the SCOUT/LUCID/OSTI central Marker corpus.

**Rationale for substitute:** For a text-native 12-page arXiv LaTeX preprint, `pdftotext -layout` produces a faithful text extraction; equations, tables and algorithm blocks render cleanly. Marker would improve Markdown structure but adds no information content for this paper. The full extracted text is below and also lives at `../work/paper.txt`.

---

                                                                    Quantum Counting

                                                       Gilles Brassard 1⋆ , Peter Høyer 2⋆⋆ , and Alain Tapp 1⋆ ⋆ ⋆
                                                   1
                                                       Université de Montréal, {brassard,tappa}@iro.umontreal.ca
                                                                  2
                                                                    Odense University, u2pi@imada.ou.dk




arXiv:quant-ph/9805082v1 27 May 1998
                                                Abstract. We study some extensions of Grover’s quantum searching
                                                algorithm. First, we generalize the Grover iteration in the light of
                                                a concept called amplitude amplification. Then, we show that the
                                                quadratic speedup obtained by the quantum searching algorithm over
                                                classical brute force can still be obtained for a large family of search
                                                problems for which good classical heuristics exist. Finally, as our main
                                                result, we combine ideas from Grover’s and Shor’s quantum algorithms
                                                to perform approximate counting, which can be seen as an amplitude
                                                estimation process.


                                         1    Introduction

                                         Quantum computing is a field at the junction of theoretical modern physics and
                                         theoretical computer science. Practical experiments involving a few quantum
                                         bits have been successfully performed, and much progress has been achieved
                                         in quantum information theory, quantum error correction and fault tolerant
                                         quantum computation. Although we are still far from having desktop quantum
                                         computers in our offices, the quantum computational paradigm could soon be
                                         more than mere theoretical exercise [6, and references therein].
                                             The discovery by Peter Shor [12] of a polynomial-time quantum algorithm for
                                         factoring and computing discrete logarithms was a major milestone in the his-
                                         tory of quantum computing. Another significant result is Lov Grover’s quantum
                                         search algorithm [10]. Grover’s algorithm does not solve NP–complete problems
                                         in polynomial time, but the wide range of its applications compensates for this.
                                             The search problem and Grover’s iteration are reviewed in Section 2. It was
                                         already implicit in [7] that the heart of Grover’s algorithm can be viewed as an
                                         amplitude amplification process. Here, we develop this viewpoint and obtain a
                                         more general algorithm.
                                             When the structure in a search problem cannot be exploited, any quantum
                                         algorithm requires a computation time at least proportional to the square root of
                                         the time taken by brute-force classical searching [3]. In practice, the structure of
                                         ⋆
                                           Supported in part by Canada’s nserc, Québec’s fcar and the Canada Council.
                                        ⋆⋆
                                           Supported in part by the esprit Long Term Research Programme of the EU under
                                           project number 20244 (alcom-it). Research carried out while this author was at the
                                           Université de Montréal.
                                       ⋆⋆⋆
                                           Supported in part by postgraduate fellowships from fcar and nserc.
the search problem can usually be exploited, yielding deterministic or heuristic
algorithms that are much more efficient than brute force would be. In Section 3,
we study a vast family of heuristics for which we show how to adapt the quantum
search algorithm to preserve quadratic speedup over classical techniques.
    In Section 4, we present, as our main result, a quantum algorithm to perform
counting. This is the problem of counting the number of elements that fulfill some
specific requirements, instead of merely finding such an element. Our algorithm
builds on both Grover’s iteration [10] as described in [4] and the quantum Fourier
transform as used in [12]. The accuracy of the algorithm depends on the amount
of time one is willing to invest. As Grover’s algorithm is a special case of the
amplitude amplification process, our counting algorithm can also be viewed as
a special case of the more general process of amplitude estimation.
    We assume in this paper that the reader is familiar with basic notions of
quantum computing [1,5].


2   Quantum Amplitude Amplification
Consider the following search problem: Given a Boolean function F : X → {0, 1}
defined on some finite domain X, find an input x ∈ X for which F (x) = 1,
provided such an x exists. We assume that F is given as a black box, so that it is
not possible to obtain knowledge about F by any other means than evaluating it
on points in its domain. The best classical strategy is to evaluate F on random
elements of X. If there is a unique x0 ∈ X on which F takes value 1, this strategy
evaluates F on roughly half the elements of the domain in order to determine x0 .
By contrast, Grover [10] discovered a quantum algorithm  √    that only requires an
expected number of evaluations of F in the order of N , where N = |X| denotes
the cardinality of X.
    It is useful for what follows to think of the above-mentioned classical strategy
in terms of an algorithm that keeps boosting the probability of finding x0 . The
algorithm evaluates F on new inputs, until it eventually finds the unique input x0
on which F takes value 1. The probability that the algorithm stops after exactly
j evaluations of F is 1/N (1 ≤ j ≤ N − 2), and thus we can consider that each
evaluation boosts the probability of success by an additive amount of 1/N .
    Intuitively, the quantum analog of boosting the probability of success would
be to boost the amplitude of being in a certain subspace of a Hilbert space, and
indeed the algorithm found by Grover can be seen as working by that latter
principle [10,4]. As discovered by Brassard and Høyer [7], the idea of amplifying
the amplitude of a subspace is a technique that applies in general. Following [7],
we refer to this as amplitude amplification, and describe the technique below.
For this, we require the following notion, which we shall use throughout the rest
of this section.
    Let |Υ i be any pure state of a joint quantum system H. Write |Υ i as a
superposition of orthonormal states according to the state of the first subsystem:
                                         X
                                  |Υ i =     xi |ii|Υi i
                                       i∈Z
so that only a finite number of the states |ii|Υi i have nonzero amplitude xi .
    Every Boolean function χ : Z → {0, 1} induces two orthogonal subspaces
of H, allowing us to rewrite |Υ i as follows:
                                     X                  X
            |Υ i = |Υ a i + |Υ b i =      xi |ii|Υi i +      xi |ii|Υi i.       (1)
                                   i∈χ−1 (1)            i∈χ−1 (0)


We say that a state |ii|·i is good if χ(i) = 1, and otherwise it is bad. Thus, we
have that |Υ a i denotes the projection of |Υ i onto the subspace spanned by the
good states, and similarly |Υ b i is the projection of |Υ i onto the subspace spanned
by the bad states. Let aΥ = hΥ a |Υ a i denote the probability that measuring |Υ i
produces a good state, and similarly let bΥ = hΥ b |Υ b i. Since |Υ a i and |Υ b i are
orthogonal, we have aΥ + bΥ = 1.
   Let A be any quantum algorithm that acts on H and uses no measurements.
The heart of amplitude amplification is the following operator [7]

                       Q = Q(A, χ, φ, ϕ) = −ASφ0 A−1 Sϕ
                                                      χ.                          (2)

Here, φ and ϕ are complex numbers of unit norm, and operator Sϕ
                                                              χ conditionally
changes the phase by a factor of ϕ:
                                  (
                                    ϕ|ii|·i if χ(i) = 1
                       |ii|·i 7−→
                                     |ii|·i if χ(i) = 0.

Further, Sφ0 changes the phase of a state by a factor of φ if and only if the first
register holds a zero. The operator Q is a generalization of the iteration applied
by Grover in his original quantum searching paper [10]. It was first used in [7] to
obtain an exact quantum polynomial-time algorithm for Simon’s problem. It is
well-defined since we assume that A uses no measurements and, therefore, A has
an inverse.
    Denote the complex conjugate of λ by λ∗ . It is easy to show the following
lemma by a few simple rewritings.
Lemma 1. Let |Υ i be any superposition. Then
                                                            ∗
                   ASφ0 A−1 |Υ i = |Υ i − (1 − φ)hΥ |A|0i A |0i.

   By factorizing Q as (ASφ0 A−1 )(−Sϕ
                                     χ ), the next lemma follows.

Lemma 2. Let |Υ i = |Υ a i + |Υ b i be any superposition. Then
                                                             ∗
                   Q |Υ a i = −ϕ|Υ a i + ϕ(1 − φ)hΥ a |A|0i A|0i                  (3)
                        b          b                b        ∗
                   Q |Υ i = −|Υ i + (1 − φ)hΥ |A|0i A|0i.                         (4)

   In particular, letting |Υ i be A|0i = |Ψ a i + |Ψ b i implies that the subspace
spanned by |Ψ a i and |Ψ b i is invariant under the action of Q.
Lemma 3. Let A|0i = |Ψ i = |Ψ a i + |Ψ b i. Then

               Q |Ψ a i = ϕ((1 − φ)a − 1)|Ψ a i +          ϕ(1 − φ)a|Ψ b i             (5)
                     b                          b                      a
               Q |Ψ i = −((1 − φ)a + φ)|Ψ i + (1 − φ)(1 − a)|Ψ i,                      (6)

where a = hΨ a |Ψ a i.

   From Lemmas 2 and 3 it follows that, for any vector |Υ i = |Υ a i + |Υ b i, the
subspace spanned by the set {|Υ a i, |Υ b i, |Ψ a i, |Ψ b i} is invariant under the action
of Q. By setting φ = ϕ = −1, we find the following much simpler expressions.

Lemma 4. Let A|0i = |Ψ i = |Ψ a i + |Ψ b i, and let Q = Q(A, χ, −1, −1). Then

                          Q |Ψ a i = (1 − 2a)|Ψ a i − 2a|Ψ b i                         (7)
                                b                   b        a
                          Q |Ψ i = (1 − 2a)|Ψ i + 2b|Ψ i,                              (8)

where a = hΨ a |Ψ a i and b = 1 − a = hΨ b |Ψ b i.

    The recursive formulae defined by Equations 7 and 8 were solved in [4],
and their solution is given in the following theorem. The general cases defined
by Equations 3 – 6 have similar solutions, but we shall not need them in what
follows.

Theorem 1 (Amplitude Amplification—simple case). Let A|0i = |Ψ i =
|Ψ a i + |Ψ b i, and let Q = Q(A, χ, −1, −1). Then, for all j ≥ 0,

                             Qj A |0i = kj |Ψ a i + ℓj |Ψ b i,

where
                1                                      1
          kj = √ sin((2j + 1)θ)         and     ℓj = √    cos((2j + 1)θ),
                 a                                    1−a

and where θ is defined so that sin2 θ = a = hΨ a |Ψ a i and 0 ≤ θ ≤ π/2.

    Theorem 1 yields a method for boosting the success probability a of a quan-
tum algorithm A. Consider what happens if we apply A on the initial state
|0i and then measure the system. The probability that the outcome is a good
state is a. If, instead of applying A, we apply operator Qm A for some inte-
ger m ≥ 1, then our success probability is given by akm    2
                                                             = sin2 ((2m + 1)θ).
Therefore, to obtain a high probability of success, we want to choose integer m
such that sin2 ((2m + 1)θ) is close to 1. Unfortunately, our ability to choose m
wisely depends on our knowledge about θ, which itself depends on a. The two
extreme cases are when we know the exact value of a, and when we have no
prior knowledge about a whatsoever.
    Suppose the value of a is known. If a > 0, then by letting m = ⌊π/4θ⌋, we
              2
have that akm    ≥ 1 − a, as shown in [4]. The next theorem is immediate.
Theorem 2 (Quadratic speedup). Let A be any quantum algorithm that uses
no measurements, and let χ : Z → {0, 1} be any Boolean function. Let the initial
success probability a and angle θ be defined as in Theorem 1. Suppose a > 0
and set m = ⌊π/4θ⌋. Then, if we compute Qm A|0i and measure the system, the
outcome is good with probability at least max(1 − a, a).
    This theorem is often referred to as a quadratic speedup, or the square-root
running-time result. The reason for this is that if an algorithm A has success
probability a > 0, then after an expected number of 1/a applications of A,
we will find a good solution. Applying the aboveptheorem reduces this to an
expected number of at most (2m + 1)/(1 − a) ∈ Θ( 1/a ) applications of A and
its inverse.
    Suppose the value of a is known and that 0 < a < 1. Theorem 2 allows us to
find a good solution with probability at least max(1 − a, a). A natural question
to ask is whether it is possible to improve this to certainty, still given the value
of a. It turns out that the answer is positive. This is unlike classical computers,
where no such general de-randomization technique is known. We now describe
two optimal methods for obtaining this, but other approaches are possible.
    The first method is by applying amplitude amplification, not on the origi-
nal algorithm A, but on a slightly modified version of it. If m̃ = π/4θ − 1/2 is
an integer, then we would have ℓm̃ = 0, and we would succeed with certainty.
In general, m0 = ⌈m̃⌉ iterations is a fraction of 1 iteration too many, but we
can compensate for that by choosing θ0 = π/(4m0 + 2), an angle slightly smaller
than θ. Any quantum algorithm that succeeds with probability a0 such that
sin2 θ0 = a0 , will succeed with certainty after m0 iterations of amplitude ampli-
fication. Given A and its initial success probability a, it is easy to construct a
new quantum algorithm that succeeds with probability a0 ≤ a: Let B denote the
quantum algorithm that p takes a singlepqubit in the initial state |0i and rotates it
to the superposition 1 − a0 /a |0i+ a0 /a |1i. Apply both A and B, and define
a good solution as one in which A produces a good solution, and the outcome
of B is the state |1i.
    The second method is to slow down the speed of the very last iteration. First,
apply m0 = ⌊m̃⌋ iterations of amplitude amplification with φ = ϕ = −1. Then,
if m0 < m̃, apply one more iteration with complex phase-shifts φ and ϕ satisfying
ℓ2m0 = 2a(1 − Re(φ)) and so that ϕ(1 − φ)akm0 − ((1 − φ)a + φ)ℓm0 vanishes.
Going through the algebra and applying Lemma 3 shows that this produces
a good solution with certainty. For the case m0 = 0, this second method was
independently discovered by Chi and Kim [8].
    Suppose now that the value of a is not known. In Section 4, we discuss
techniques for finding a good estimate of a, after which one then can apply a
weakened version of Theorem 2 to find a good solution. Another idea is to try
to find a good solution without prior computation of an estimate of a. Within
that approach, by adapting the ideas in Section 4 in [4] (Section 6 in its final
version), we can still obtain a quadratic speedup.
Theorem 3 (Quadratic speedup without knowing a). Let A be any quan-
tum algorithm that uses no measurements, and let χ : Z → {0, 1} be any Boolean
function. Let the initial success probability a of A be defined as in Theorem 1.
Then there exists a quantum
                      p        algorithm that finds a good solution using an ex-
pected number of Θ( 1/a ) applications of A and its inverse if a > 0, and
otherwise runs forever.
   By applying this theorem to the searching problem defined in the first para-
graph of this section, we obtain the following result from [4], which itself is a
generalization of the work by Grover [10].
Corollary 1. Let F : X → {0, 1} be any Boolean function defined on a finite
set X. Then there exists a quantum algorithm Search
                                                 p       that finds an x ∈ X such
that F (x) = 1 using an expected number of Θ( |X|/t ) evaluations of F , pro-
vided such an x exists, and otherwise runs forever. Here t = |{x ∈ X | F (x) = 1}|
denotes the cardinality of the preimage of 1.
Proof. Apply Theorem P
                     3 with χ = F and A being any unitary transformation
that maps |0i to √ 1   x∈X |xi, such as the Walsh–Hadamard transform.  ⊓
                                                                       ⊔
                    |X|


3   Quantum Heuristics
If function F has no useful structure, then quantum algorithm Search will
be more efficient than any classical (deterministic or probabilistic) algorithm.
In sharp contrast, if some useful information is known about the function, then
some classical algorithm might be very efficient. Useful information might be
clear mathematical statements or intuitive information stated as a probability
distribution of the likelihood of x being a solution. The information we have
about F might also be expressed as an efficient classical heuristic to find a
solution. In this section, we address the problem of heuristics.
    Search problems, and in particular NP problems, are often very difficult to
solve. For many NP–complete problems, practical algorithms are known that
are more efficient than brute force search on the average: they take advantage
of the problem’s structure and especially of the input distribution. Although in
general very few theoretical results exist about the efficiency of heuristics, they
are very efficient in practice.
    We concentrate on a large but simple family of heuristics that can be ap-
plied to search problems. Here, by heuristics, we mean a probabilistic algorithm
running in polynomial time that outputs what one is searching for with some
nonzero probability. Our goal is to apply Grover’s technique for heuristics in
order to speed them up, in the same way that Grover speeds up black-box
search, without making things too complicated.
    More formally, suppose we have a family F of functions such that each F ∈ F
is of the form F : X → {0, 1}. A heuristic is a function G : F × R → X, for
an appropriate finite set R. For every function F ∈ F, let tF = |F −1 (1)| and
hF = |{r ∈ R | F (G(F, r)) = 1}|. We say that the heuristic is efficient for a given
F if hF /|R| > tF /|X| and the heuristic is good in general if
                                                 
                                  hF             tF
                            EF          > EF          .
                                  |R|           |X|
Here EF denotes the expectation over all F according to some fixed distribution.
Note that for some F , hF might be small but repeated uses of the heuristic, with
seeds r uniformly chosen in R, will increase the probability of finding a solution.
Theorem 4. Let F be a search problem chosen in a family F according to some
probability distribution. If, using a heuristic G, a solution to F is found in
expected time T then,√ using a quantum computer, a solution can be found in
expected time in O( T ).
Proof. We simply combine the quantum algorithm Search with the heuris-
tic G. Let G′ (r) = F (G(F, r)) and x = G(F, Search(G′ )), so that F (x) = 1.
By Corollary p 1, for each function F ∈ F, we have an expected running
time
P      in Θ(   |R|/hF ). Let PF denote the probability that F occurs. Then
   F ∈F  PF = 1, and we have that the expected running time is in the order
   P       p
of F ∈F |R|/hF PF , which can be rewritten as
        s                            !1/2        !1/2                 !1/2
   X |R| p                X |R|           X                X |R|
              PF PF ≤             PF          PF      =           PF       ,
           hF                  hF                              hF
    F ∈F                  F ∈F               F ∈F              F ∈F

by Cauchy–Schwarz’s inequality.                                                  ⊓
                                                                                 ⊔

4     Approximate Counting
In this section, we do not concentrate on finding one solution, but rather on
counting them. For this, we complement Grover’s iteration [10] using techniques
inspired by Shor’s quantum factoring algorithm [12].
Counting Problem: Given a Boolean function F defined on some finite set
X = {0, . . . , N − 1}, find or approximate t = F −1 (1) .
    Before we proceed, here is the basic intuition. From Section 2 it follows that,
in Grover’s algorithm, the amplitude of the set F −1 (1), as well as the amplitude
of the set F −1 (0), varies with the number of iterations according to a periodic
function. We also note that the period (frequency) of this association is in direct
relation with the sizes of these sets. Thus, estimating their common period using
Fourier analysis will give us useful information on the sizes of those two sets.
Since the period will be the same if F −1 (1) has cardinality t or if F −1 (1) has
cardinality N − t, we will assume in the rest of this section that t ≤ N/2.
    The quantum algorithm Count we give to solve this problem has two param-
eters: the function F given as a black box and an integer P that will determine
the precision of our estimate, as well as the time taken by the algorithm. For
simplicity, we assume that P and N are powers of 2, but this is not essential.
Our algorithm is based on the following two unitary transformations:
                     CF : |mi ⊗ |Ψ i → |mi ⊗ (GF )m |Ψ i
                                            P −1
                                   1 X 2πıkl/P
                       FP : |ki → √      e     |li.
                                   P l=0
           √
Here ı = −1 and GF = Q(W, F, −1, −1) denotes the iteration originally used
by Grover [10], where W denotes the Walsh–Hadamard transform on n qubits
                         P2n −1
that maps |0i to 2−n/2 i=0 |ii.
    In order to apply CF even if its first argument is in a quantum superposi-
tion, it is necessary to have an upper bound on the value of m, which is the
purpose of parameter P . Thus, unitary transformation CF performs exactly P
Grover’s iterations so that P evaluations of F are required. The quantum Fourier
transform can be efficiently implemented (see [12] for example).

Count(F, P )
 1. |Ψ0 i ← W ⊗ W |0i|0i
 2. |Ψ1 i ← CF |Ψ0 i
 3. |Ψ2 i ← |Ψ1 i after the second register is measured (optional )
 4. |Ψ3 i ← FP ⊗ I |Ψ2 i
 5. f˜ ← measure |Ψ3 i          (if f˜ > P/2 then f˜ ← (P − f˜))
                  2 ˜
 6. output: N sin (f π/P )      (and f˜ if needed)
   The following theorem tells us how to make proper use of algorithm Count.

Theorem 5. Let F : {0, . . . , N − 1} → {0, 1} be a Boolean function,
t = |F −1 (1)| ≤ N/2 and t̃ be the output of Count(F, P ) with P ≥ 4, then

                                              2π √    π2
                               |t − t̃| <         tN + 2 N
                                              P       P
with probability at least 8/π 2 .

Proof. Let us follow the state through the algorithm using notation from
Section 2.
                            P −1 N −1
                        1   X    X
            |Ψ0 i = √                 |mi|xi
                        P N m=0 x=0
                        P −1
                                                                      !
                     1 X              X                   X
            |Ψ1 i = √        |mi km            |xi + ℓm            |xi .
                      P m=0         x∈F −1 (1)          x∈F −1 (0)

We introduced Step 3 to make it intuitively clear to the reader why the Fourier
transform in Step 4 gives us what we want. The result of this measurement is
not used in the algorithm and this is why it is optional: the final outcome would
be the same if Step 3 were not performed. Without loss of generality, assume
that the state x observed in the second register is such that F (x) = 1. Then by
replacing km by its definition we obtain
                                       P
                                       X −1
                           |Ψ2 i = α          sin((2m + 1)θ) |mi,            (9)
                                       m=0

where α is a normalization factor that depends on θ.
   Let

                                     f = P θ/π.                                  (10)

In Step 4, we apply the Fourier transform on a sine (cosine) of period f and
phase shift θ. From sin2 θ = t/N we conclude that θ ≤ π/2 and f ≤ P/2. After
we apply the Fourier transform, the state |Ψ3 i strongly depends on f (which
depends on t). If f were an integer, there would be two possibilities: either f = 0
(which happens if t = 0 or t = N ), in which case |Ψ3 i = |0i, or t > 0, in which
                                                                                √
case |Ψ3 i = a|f i + b|P − f i, where a and b are complex numbers of norm 1/ 2.
   In general f is not an integer and we will obtain something more complicated.
We define f − = ⌊f ⌋ and f + = ⌊f + 1⌋. We still have three cases. If 1 < f <
P/2 − 1, we obtain

              |Ψ3 i = a|f − i + b|f + i + c|P − f − i + d|P − f + i + |Ri

where |Ri is an un-normalized error term that may include some or all values
other than the desirable f − , f + , P − f − and P − f + . The two other possibilities
are 0 < f < 1, in which case we obtain

                        |Ψ3 i = a|0i + b|1i + c|P − 1i + |Ri

or P/2 − 1 < f < P/2, in which case we obtain

                 |Ψ3 i = a|P/2 − 1i + b|P/2i + c|P/2 + 1i + |Ri .

In all three cases, extensive algebraic manipulation shows that the square of the
norm of the error term |Ri can be upper bounded by 2/5,
                                               2
                                    hR|Ri <      .
                                               5
In order to bound the success probability by 8/π 2 (which is roughly 0.81 and
therefore larger than 1 − 2/5 = 0.6) as claimed in the statement of the Theorem,
we could perform a complicated case analysis depending on whether the value x
observed in Step 3 is such that F (x) = 0 or F (x) = 1. Fortunately, in the light
of some recent analysis of Michele Mosca [11], which itself is based on results
presented in [9], this analysis can be simplified. Since the information obtained
by measuring the second register is not used, measuring it in a different basis
would not change the behaviour of the algorithm. Measuring in the eigenvector
basis of GF , one obtains this bound in an elegant way. Details will be provided
in the final version of this paper.
    Assuming that f˜ phas been observed at Step 5 and applying Equation 10 and
the fact that sin θ = t/N , we obtain an estimate t̃ of t such that

                                         2π √     π2
                            |t − t̃| <        tN + 2 N .
                                         P        P
                                                                                    ⊓
                                                                                    ⊔
   Using a similar technique, it can be shown that the same quantum algorithm
can also be used to perform amplitude estimation: Grover’s algorithm [10] is to
amplitude amplification what approximate counting is to amplitude estimation.
Theorem 6. Replacing GF in CF of algorithm Count by Q = Q(A, χ, −1, −1)
and also modifying Step 6 so that the algorithm outputs ã = sin2 (f˜π/P ),
Count(F, P ) with P ≥ 4 will output ã such that
                                                 2π √  π2
                                |a − ã| <           a+ 2
                                                 P     P
with probability at least 8/π 2 .
    In Theorems 5 and 6, parameter P allows us to balance the desired accuracy
of the estimate with the running time required to achieve it. We will now look
at different choices for P and analyse the accuracy of the answer. To obtain t
up to a few standard deviations, apply the following corollary of Theorem 5.
Corollary 2. Given a Boolean
                         √    function F : {0, . . . , N − 1} → {0, 1} with t as
defined above, Count(F, c N ) outputs an estimate t̃ such that
                                                 2π √  π2
                                    |t − t̃| <       t+ 2
                                                  c    c
                                                      √
with probability at least 8/π 2 and requires exactly c N evaluations of F .
    The above corollary states that some accuracy can be achieved with proba-
bility 8/π 2 . This means that, as usual, the success probability can be boosted
exponentially close to 1 by repetition. We will denote by Maj(k, Count) an al-
gorithm that performs k evaluations of Count and outputs the majority answer.
To obtain an error probability smaller than 1/2n , one should choose k in Ω(n).
    If one is satisfied in counting uppto a constant relative error, it would be
natural to call Count with P = c N/t , but we need to use the following
strategy because t is precisely what we are looking for.
CountRel(F, c)
 1. P ← 2
 2. Repeat
    (a) P ← 2P
    (b) f˜ ←Maj(Ω(log log N ),Count(F, P ))
 3. Until f˜ > 1
 4. Output Count(F, cP )

   Note that in the main loop the algorithm calls Count to obtain f˜ and not t̃.
Corollary 3. Given F with N and t as defined above, CountRel(F, c) outputs
an estimate t̃ such that
                                         |t − t̃| < t/c
with probability at least 34 , using an expected number of Θ((c + log log N )
                                                                            p
                                                                             N/t )
evaluations of F .
Proof. Suppose for the moment that in Step 2(b) we always obtain f˜ such that
|f − f˜| < 1. Combining this with Equation 10 we seep       that to obtain f˜ > 1, we
                                     2
must have P θ/π > 1. Since sin θ = t/N , then P > 2 N/t, so, by Theorem 5,
|t − t̃| < t πc (1 + πc ). Thus, the core of the main loop will be performed at most
       p
log(2 N/t ) times before P is large enough. By using Ω(log log N ) repetitive
calls to Count in Step 2(b), we know that this will happen with sufficiently
high probability, ensuring an overall success probability of at least 3/4.
    The√ expected number of evaluations of F follows from the fact that
Plog(2 N/t)                                     p
                 (log log N )2i ∈ Θ (log log N ) N/t .
                                                     
   i=1                                                                              ⊓
                                                                                    ⊔

    Of course, to obtain a smaller relative error, the first estimate can be used
in order to call Count with P as large as one wishes. From Theorem 5, it is
clear that by letting P be large enough, one can make the absolute error smaller
than 1.

Corollary 4. Given F with N and        √ t as defined above, there is an algorithm
requiring an expected number of Θ( tN ) evaluations of F that outputs an esti-
mate t̃ such that t̃ = t with probability at least 43 using only space linear in log N .

                                        √ √
Proof. By Theorem 5, if P > π(2 + 6 ) tN , the error in the output of Count
is likely to be smaller than 1/2. Again we do not  √ know t, but we already know
how to estimate it. By calling first Count(F,√       N ) a few times, we obtain an
approximation t̃ such that |t − t̃| < 2π t + π 2 with good   √ probability. Now,
assuming the first estimate was good, calling Count(F, 20 t̃N ) we obtain t˜′ = t
with a probability of at least 8/π 2 . Thus, obtaining an overall success probability
of at least 3/4.                                                                    ⊓
                                                                                    ⊔

   It follows from a new result of Beals, Buhrman, Cleve, Moska and de Wolf [2]
that any quantum algorithm capable of deciding with high probability whether
or not a function F : {0, . . . , N − 1} → {0, 1} is such that F −1 (1) ≤ t, given
                                                √
some 0 < t < N/2, must query F at least Ω( N t ) times. Therefore, our exact
counting algorithm is optimal. Note also that successive applications of Grover’s
algorithm in which we strike out the solutions as they are found will also provide
an exact count with high probability, but at a high cost in terms of additional
quantum memory, that is Θ(t).


Acknowledgements

We are grateful to Joan Boyar, Harry Buhrman, Christoph Dürr, Michele Mosca,
Barbara Terhal and Ronald de Wolf for helpful comments. The third author
would like to thank Mélanie Doré Boulet for her encouragements throughout
the realization of this work.
References
 1. Barenco, Adriano, “Quantum physics and computers”, Contemporary Physics,
    Vol. 38, 1996, pp. 357 – 389.
 2. Beals, Robert, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de
    Wolf, “Quantum Lower Bounds by Polynomials”, 1998, Available on Los Alamos
    e-print archive as quant-ph/9802049.
 3. Bennett, Charles H., Ethan Bernstein, Gilles Brassard and Umesh Vazirani,
    “Strengths and weaknesses of quantum computing”, SIAM Journal on Computing,
    Vol. 26, no. 5, October 1997, pp. 1510 – 1523.
 4. Boyer, Michel, Gilles Brassard, Peter Høyer and Alain Tapp, “Tight bounds
    on quantum searching”, Proceedings of Fourth Workshop on Physics and Compu-
    tation — PhysComp ’96, November 1996, pp. 36 – 43. Final version to appear in
    Fortschritte Der Physik.
 5. Brassard, Gilles, “A quantum jump in computer science”, in Computer Science
    Today, Jan van Leeuwen (editor), Lecture Notes in Computer Science, Vol. 1000,
    Springer–Verlag, 1995, pp. 1 – 14.
 6. Brassard, Gilles, “New horizons in quantum information processing”, Proceedings
    of this ICALP Conference, 1998.
 7. Brassard, Gilles and Peter Høyer, “An exact quantum polynomial-time algo-
    rithm for Simon’s problem”, Proceedings of Fifth Israeli Symposium on Theory of
    Computing and Systems — ISTCS ’97, June 1997, IEEE Computer Society Press,
    pp. 12 – 23.
 8. Chi, Dong-Pyo and Jinsoo Kim, “Quantum database searching by a single query”,
    Lecture at First NASA International Conference on Quantum Computing and
    Quantum Communications, Palm Springs, February 1998.
 9. Cleve, Richard, Artur Ekert, Chiara Macchiavello and Michele Mosca,
    “Quantum algorithms revisited”, Proceedings of the Royal Society, London,
    Vol. A354, 1998, pp. 339 – 354.
10. Grover, Lov K., “Quantum mechanics helps in searching for a needle in a
    haystack”, Physical Review Letters, Vol. 79, no. 2, 14 July 1997, pp. 325 – 328.
11. Mosca, Michele, “Quantum computer algorithms and interferometry”, Lecture
    at BRICS Workshop on Algorithms in Quantum Information Processing, Aarhus,
    January 1998.
12. Shor, Peter W., “Polynomial-time algorithms for prime factorization and discrete
    logarithms on a quantum computer”, SIAM Journal on Computing, Vol. 26, no. 5,
    October 1997, pp. 1484 – 1509.

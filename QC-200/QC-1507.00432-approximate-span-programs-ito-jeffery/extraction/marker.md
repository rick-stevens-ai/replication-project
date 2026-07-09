# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:1507.00432 — Tsuyoshi Ito and Stacey Jeffery, 'Approximate Span Programs'
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

arXiv:1507.00432v1  [quant-ph]  2 Jul 2015
Approximate Span Programs
Tsuyoshi Ito and Stacey Jeﬀery∗
Abstract
Span programs are a model of computation that have been used to design quantum algo-
rithms, mainly in the query model. It is known that for any decision problem, there exists
a span program that leads to an algorithm with optimal quantum query complexity, however
ﬁnding such an algorithm is generally challenging.
In this work, we consider new ways of designing quantum algorithms using span programs.
We show how any span program that decides a problem f can also be used to decide “property
testing” versions of the function f, or more generally, approximate a quantity called the span
program witness size, which is some property of the input related to f. For example, using our
techniques, the span program for OR, which can be used to design an optimal algorithm for the
OR function, can also be used to design optimal algorithms for: threshold functions, in which
we want to decide if the Hamming weight of a string is above a threshold, or far below, given
the promise that one of these is true; and approximate counting, in which we want to estimate
the Hamming weight of the input up to some desired accuracy. We achieve these results by
relaxing the requirement that 1-inputs hit some target exactly in the span program, which could
potentially make design of span programs signiﬁcantly easier.
In addition, we give an exposition of span program structure, which increases the general
understanding of this important model. One implication of this is alternative algorithms for
estimating the witness size when the phase gap of a certain unitary can be lower bounded. We
show how to lower bound this phase gap in certain cases.
As an application, we give the ﬁrst upper bounds in the adjacency query model on the
quantum time complexity of estimating the eﬀective resistance between s and t, Rs,t(G). For
this problem we obtain eO(
1
ε3/2 n
p
Rs,t(G)), using O(log n) space.
In addition, when µ is a
lower bound on λ2(G), by our phase gap lower bound, we can obtain an upper bound of
eO

1
εn
p
Rs,t(G)/µ

for estimating eﬀective resistance, also using O(log n) space.
1
Introduction
Span programs are a model of computation ﬁrst used to study logspace complexity [KW93], and
more recently, introduced to the study of quantum algorithms in [RˇS12]. They are of immense the-
oretical importance, having been used to show that the general adversary bound gives a tight lower
bound on the quantum query complexity of any decision problem [Rei09, Rei11]. As a means of de-
signing quantum algorithms, it is known that for any decision problem, there exists a span-program-
based algorithm with asymptotically optimal quantum query complexity, but this fact alone gives
no indication of how to ﬁnd such an algorithm. Despite the relative diﬃculty in designing quantum
algorithms this way, there are many applications, including formula evaluation [RˇS12, Rei11], a
number of algorithms based on the learning graph framework [Bel12b], st-connectivity [BR12] and
k-distinctness [Bel12a]. Although generally quantum algorithms designed via span programs can
∗sjeﬀery@caltech.edu, Institute for Quantum Information and Matter, California Institute of Technology
1


---- page 2 ----

only be analyzed in terms of their query complexity, in some cases their time complexity can also be
analyzed, as is the case with the quantum algorithm for st-connectivity. In the case of the quantum
algorithm for k-distinctness, the ideas used in designing the span program could be turned into a
quantum algorithm for 3-distinctness with time complexity matching its query complexity up to
logarithmic factors [BCJ+13].
In this work, we consider new ways of designing quantum algorithms via span programs. Con-
sider Grover’s quantum search algorithm, which, on input x ∈{0, 1}n, decides if there is some
i ∈[n] such that xi = 1 using only O(√n) quantum operations [Gro96]. The ideas behind this
algorithm have been used in innumerable contexts, but in particular, a careful analysis of the ideas
behind Grover’s algorithm led to algorithms for similar problems, including a class of threshold
functions: given x ∈{0, 1}n, decide if |x| ≥t or |x| < εt, where |x| denotes the Hamming weight;
and approximate counting: given x ∈{0, 1}n, output an estimate of |x| to some desired accuracy.
The results in this paper oﬀer the possibility of obtaining analogous results for any span program.
That is, given a span program for some problem f, our results show that one can obtain, not only
an algorithm for f, but algorithms for a related class of threshold functions, as well as an algorithm
for estimating a quantity called the span program witness size, which is analogous to |x| in the above
example (and is in fact exactly 1/|x| in the span program for the OR function — see Section 2.3).
New Algorithms from Span Programs
We give several new means of constructing quantum
algorithms from span programs. Roughly speaking, a span program can be turned into a quantum
algorithm that decides between two types of inputs: those that “hit” a certain “target vector”, and
those that don’t. We show how to turn a span program into an algorithm that decides between
inputs that get “close to” the target vector, and those that don’t. Whereas as traditionally a span
program has been associated with some decision problem, this allows us to now associate, with one
span program, a whole class of threshold problems.
In addition, for any span program P, we can construct a quantum algorithm that estimates the
positive witness size, w+(x), to accuracy ε in
1
ε3/2
q
w+(x)f
W−queries, where f
W−is the approximate
negative witness complexity of P. This construction is useful whenever we can construct a span
program for which w+(x) corresponds to some function we care to estimate, as is the case with
the span program for OR, in which w+(x) =
1
|x|, or the span from for st-connectivity, in which
w+(G) = 1
2Rs,t(G), where G is a graph, and Rs,t(G) is the eﬀective resistance between s and t in
G. We show similar results for estimating the negative witness size as well.
Structural Results
Our analysis of the structure of span programs increases the theoretical
understanding of this important model. One implication of this is alternative algorithms for esti-
mating the witness size when the phase gap (or spectral gap) of a certain unitary associated with
the span program can be lower bounded. This is in contrast to previous span program algorithms,
including those mentioned in the previous paragraph, which have all relied on eﬀective spectral gap
analysis. We show how the phase gap can be lower bounded by
σmax(A)
σmin(A(x)), where A and A(x) are
linear operators associated with the span program and some input x, and σmin and σmax are the
smallest and largest nonzero singular values.
In addition, our exposition highlights the relationship between span programs and estimating
the size of the smallest solution to a linear system, which is a problem solved by [HHL09]. It is not
yet clear if this relationship can lead to new algorithms, but it is an interesting direction for future
work, which we discuss in Section 5.
2


---- page 3 ----

Application to Eﬀective Resistance
An immediate application of our results is a quantum
algorithm for estimating the eﬀective resistance between two vertices in a graph, Rs,t(G). This ex-
ample is immediate, because in [BR12], a span program for st-connectivity was presented, in which
the positive witness size corresponds to Rs,t(G). The results of [BR12], combined with our new
span program algorithms, immediately yield an upper bound of eO(
1
ε3/2n
p
Rs,t(G)) for estimating
the eﬀective resistance to relative accuracy ε. This upper bound also holds for time complexity,
due to the time complexity analysis of [BR12]. Using our new spectral analysis techniques, we
are also able to get an often better upper bound of eO
  1
εn
p
Rs,t(G)/µ

, on the time complexity of
estimating eﬀective resistance, where µ is a lower bound on λ2(G), the second smallest eigenvalue
of the Laplacian. Both algorithms use O(log n) space. We also show that a linear dependence on
n is necessary, so our results cannot be signiﬁcantly improved.
These are the ﬁrst quantum algorithms for this problem in the adjacency query model. Previous
results have studied the problem in the edge-list model [Wan13].
At the end of Section 4, we
compare the techniques used in [Wan13] to those of our algorithms. Classically, this quantity can
be computed exactly by inverting the Laplacian, which costs O(m) = O(n2), where m is the number
of edges in the input graph.
Outline
In Section 1.1, we describe the algorithmic subroutines and standard linear algebra that
will form the basis of our algorithms. In Section 2.1, we review the use of span programs in the
context of quantum query algorithms, followed in Section 2.2 by our new paradigm of approximate
span programs.
At this point we will be able to formally state our results about how to use
span programs to construct quantum algorithms. In Section 2.4, we describe the structure of span
programs, giving several results that will help us develop algorithms. The new algorithms from
span programs are developed in Section 3, and ﬁnally, in Section 4, we present our applications to
estimating eﬀective resistance. In Section 5, we discuss open problems.
1.1
Preliminaries
To begin, we ﬁx notation and review some concepts from linear algebra. By L(V, W) we denote
the set of linear operators from V to W. For any operator A ∈L(V, W), we denote by colA the
columnspace, rowA the rowspace, and ker A the kernel of A.
Deﬁnition 1.1 (Singular value decomposition). Any linear operator A ∈L(V, W) can be written as
A = Pr
i=1 σi|ψi⟩⟨φi| for positive real numbers σi, called the singular values, an orthonormal basis
for rowA, {|φi⟩}i, called the right singular vectors, and an orthonormal basis for colA, {|ψi⟩}i,
called the left singular vectors. We deﬁne σmin(A) := mini σi and σmax(A) := maxi σi.
Deﬁnition 1.2 (Pseudo-inverse). For any linear operator A with singular value decomposition
A = Pr
i=1 σi|ψi⟩⟨φi|, we deﬁne the pseudo-inverse of A as A+ := Pr
i=1
1
σi |φi⟩⟨ψi|. We note that
A+A is the orthogonal projector onto rowA, and AA+ is the orthogonal projector onto colA. For
any |v⟩∈rowA, the unique smallest vector |w⟩satisfying A|w⟩= |v⟩is A+|v⟩.
The algorithms in this paper solve either decision problems, or estimation problems.
Deﬁnition 1.3. Let f : X ⊆[q]n →{0, 1}. We say that an algorithm decides f with bounded
error if for any x ∈X, with probability at least 2/3, the algorithm outputs f(x) on input x.
Deﬁnition 1.4. Let f : X ⊆[q]n →R≥0.
We say that an algorithm estimates f to relative
accuracy ε with bounded error if for any x ∈X, with probability at least 2/3, on input x the
algorithm outputs ˜f such that |f(x) −˜f| ≤εf(x).
3


---- page 4 ----

We will generally omit the description “with bounded error”, since all of our algorithms will
have bounded error.
All algorithms presented in this paper are based on the following structure. We have some
initial state |φ0⟩, and some unitary operator U, and we want to estimate ∥Π0|φ0⟩∥, where Π0 is
the orthogonal projector onto the 1-eigenspace of U. The ﬁrst step in this process is a quantum
algorithm that estimates, in a new register, the phase of U applied to the input state.
Theorem 1.5 (Phase Estimation [Kit95, CEMM98]). Let U = Pm
j=1 eiθj|ψj⟩⟨ψj| be a unitary,
with θ1, . . . , θm ∈(−π, π]. For any Θ ∈(0, π) and ε ∈(0, 1), there exists a quantum algorithm
that makes O
  1
Θ log 1
ε

controlled calls to U and, on input |ψj⟩, outputs a state |ψj⟩|ω⟩such that
if θj = 0, then |ω⟩= |0⟩, and if |θj| ≥Θ, |⟨0|ω⟩|2 ≤ε. If U acts on s qubits, the algorithm uses
O(s + log 1
Θ) space.
The precision needed to isolate Π0|φ0⟩depends on the smallest nonzero phase of U, the phase gap.
Deﬁnition 1.6 (Phase Gap). Let {eiθj}j∈S be the eigenvalues of a unitary operator U, with
{θj}j∈S ⊂(−π, π]. Then the phase gap of U is ∆(U) := min{|θj| : θj ̸= 0}.
In order to estimate ∥Π0|φ0⟩∥2, given a state |0⟩Π0|φ0⟩+ |1⟩(I −Π0)|φ0⟩, we use the following.
Theorem 1.7 (Amplitude Estimation [BHMT02]). Let A be a quantum algorithm that outputs
p
p(x)|0⟩|Ψx(0)⟩+
p
1 −p(x)|1⟩|Ψx(1)⟩on input x. Then there exists a quantum algorithm that
estimates p(x) to precision ε using O

1
ε
1
√
p(x)

calls to A.
If we know that the amplitude is either ≤p0 or ≥p1 for some p0 < p1, then we can use
amplitude estimation to distinguish between these two cases.
Corollary 1.8 (Amplitude Gap). Let A be a quantum algorithm that outputs
p
p(x)|0⟩|Ψx(0)⟩+
p
1 −p(x)|1⟩|Ψx(1)⟩on input x. For any 0 ≤p1 < p0 ≤1, we can distinguish between the cases
p(x) ≥p0 and p(x) ≤p1 with bounded error using O
 √p0
p0−p1

calls to A.
Proof. By [BHMT02, Thm. 12], using M calls to A, we can obtain an estimate ˜p of p(x) such that
|˜p −p(x)| ≤2π
p
p(x)(1 −p(x))
M
+ π2
M2
with probability 3/4. Let M = 4π
√p0+p1
p0−p1 . Then note that for any x1 and x0 such that p(x1) ≤p1
and p(x0) ≥p0, we have, using √p0 + p1 ≥(√p0 + √p1)/
√
2,
M ≥2
√
2π
√p0 + √p1
p0 −p1
= 2
√
2π
1
√p0 −√p1
≥2
√
2π
1
p
p(x0) −
p
p(x1)
= 2
√
2π
p
p(x0) +
p
p(x1)
p(x0) −p(x1)
.
If ˜p1 is the estimate obtained on input x1, then we have, with probability 3/4:
˜p1 ≤p(x1) + 2π
p
p(x1)(1 −p(x1))
M
+ π2
M2 ≤p(x1) +
p
p(x1)(p(x0) −p(x1))
√
2(
p
p(x0) +
p
p(x1))
+ (p0 −p1)2
16(p0 + p1).
On the other hand, if ˜p0 is an estimate of p(x0), then with probability 3/4:
˜p0 ≥p(x0) −2π
p
p(x0)(1 −p(x0))
M
−π2
M2 ≥p(x0) −
p
p(x0)(p(x0) −p(x1))
√
2(
p
p(x0) +
p
p(x1))
−(p0 −p1)2
16(p0 + p1).
4


---- page 5 ----

We complete the proof by showing that ˜p1 < ˜p0, so we can distinguish these two events. We have:
˜p0 −˜p1
≥
p(x0) −p(x1) −
(p(x0) −p(x1))
√
2(
p
p(x0) +
p
p(x1))
(
p
p(x0) +
p
p(x1)) −(p0 −p1)2
8(p0 + p1)
≥

1 −1
√
2

(p0 −p1) −1
8(p0 −p1)
≥
1
6(p0 −p1)
>
0.
Thus, using 4π
√p0+p1
p0−p1 = O
 √p0
p0−p1

calls to A, we can distinguish between p(x) ≤p1 and p(x) ≥p0
with success probability 3/4.
In order to make use of phase estimation, we will need to analyze the spectrum of a particular
unitary, which, in our case, consists of a pair of reﬂections. The following lemma ﬁrst appeared in
this form in [LMR+11]:
Lemma 1.9 (Eﬀective Spectral Gap Lemma). Let U = (2ΠA −I)(2ΠB −I) be the product of two
reﬂections, and let ΠΘ be the orthogonal projector onto span{|u⟩: U|u⟩= eiθ|u⟩, |θ| ≤Θ}. Then if
ΠA|u⟩= 0, ∥ΠΘΠB|u⟩∥≤Θ
2 ∥|u⟩∥.
The following theorem was ﬁrst used in the context of quantum algorithms by Szegedy [Sze04]:
Theorem 1.10 ([Sze04]). Let U = (2ΠA −I)(2ΠB −I) be a unitary on a ﬁnite inner product space
H containing A = span{|ψ1⟩, . . . , |ψa⟩} and B = span{|φ1⟩, . . . , |φb⟩}. Let ΠA = Pa
i=1 |ψi⟩⟨ψi| and
ΠB = Pb
i=1 |φi⟩⟨φi|. Let D = ΠAΠB be the discriminant of U, and suppose it has singular value
decomposition Pr
j=1 cos θj|αj⟩⟨βj|, with θj ∈[0, π
2 ]. Then the spectrum of U is {e±2iθj}j. The
1-eigenspace of U is (A ∩B) ⊕(A⊥∩B⊥) and the −1-eigenspace is (A ∩B⊥) ⊕(A⊥∩B).
Let ΛA = Pa
j=1 |ψj⟩⟨j| and ΛB = Pb
j=1 |φj⟩⟨j|.
We note that in the original statement of
Theorem 1.10, the discriminant is deﬁned D′ = Λ†
AΛB. However it is easy to see that D′ and D
have the same singular values: if D′ = P
i σi|vi⟩⟨ui| is a singular value decomposition of D′, then
D = P
i σiΛA|vi⟩⟨ui|Λ†
B is a singular value decomposition of D, since ΛA acts as an isometry on
the columns of D′, and ΛB acts as an isometry on the rows of D′.
The following corollary to Theorem 1.10 will be useful in the analysis of several algorithms.
Corollary 1.11 (Phase gap and discriminant). Let D be the discriminant of a unitary U = (2ΠA−
I)(2ΠB −I). Then ∆(−U) ≥2σmin(D).
Proof. By Theorem 1.10, if {σ0 = cos θ0 < σ1 = cos θ1 < . . . σm = cos θm} are the singular
values of D, for θj ∈[0, π
2 ], then U has phases {±2θj}m
j=0 ⊂[−π, π], and so −U has phases
{±2θj ∓π}m
j=0 = {±(2θj −π)}m
j=0 ⊂[−π, π]. Thus
∆(−U) = min{|π −2θj| : θj ̸= π/2} = |π −2 cos−1 min{σj : σj ̸= 0}| = |π −2 cos−1 σmin(D)|.
We have θ ≥sin θ = cos(π/2 −θ), so σmin(D) ≥cos(π/2 −σmin(D)). Then since cos is decreasing
on the interval [0, π/2], we have cos−1(σmin(D)) ≤π/2 −σmin(D), and thus
∆(−U) ≥|π −2 (π/2 −σmin(D))| = 2σmin(D).
5


---- page 6 ----

2
Approximate Span Programs
2.1
Span Programs and Decision Problems
In this section, we review the concept of span programs, and their use in quantum algorithms.
Deﬁnition 2.1 (Span Program). A span program P = (H, V, τ, A) on [q]n consists of
1. ﬁnite-dimensional inner product spaces H = H1 ⊕· · · ⊕Hn ⊕Htrue ⊕Hfalse, and {Hj,a ⊆
Hj}j∈[n],a∈[q] such that Hj,1 + · · · + Hj,q = Hj,
2. a vector space V ,
3. a target vector τ ∈V , and
4. a linear operator A ∈L(H, V ).
To each string x ∈[q]n, we associate a subspace H(x) := H1,x1 ⊕· · · ⊕Hn,xn ⊕Htrue.
Although our notation in Deﬁnition 2.1 deviates from previous span program deﬁnitions, the
only diﬀerence in the substance of the deﬁnition is that the spaces Hj,a and Hj,b for a ̸= b need
not be orthogonal in our deﬁnition. This has the eﬀect of removing log q factors in the equivalence
between span programs and the dual adversary bound (for details see [Jef14, Sec. 7.1]). The spaces
Htrue and Hfalse can be useful for designing a span program, but are never required, since we can
always add an (n + 1)th variable, set xn+1 = 1, and let Hn+1,0 = Hfalse and Hn+1,1 = Htrue.
A span program on [q]n partitions [q]n into two sets: positive inputs, which we call P1, and
negative inputs, which we call P0. The importance of this partition stems from the fact that a span
program may be converted into a quantum algorithm for deciding this partition in the quantum
query model [Rei09, Rei11]. Thus, if one can construct a span program whose partition of [q]n
corresponds to a problem one wants to solve, an algorithm follows. In order to describe how a span
program partitions [q]n and the query complexity of the resulting algorithm, we need the concept
of positive and negative witnesses and witness size.
Deﬁnition 2.2 (Positive and Negative Witness). Fix a span program P on [q]n, and a string
x ∈[q]n. We say that |w⟩is a positive witness for x in P if |w⟩∈H(x), and A|w⟩= τ. We deﬁne
the positive witness size of x as:
w+(x, P) = w+(x) = min{∥|w⟩∥2 : |w⟩∈H(x) : A|w⟩= τ},
if there exists a positive witness for x, and w+(x) = ∞else. We say that ω ∈L(V, R) is a negative
witness for x in P if ωAΠH(x) = 0 and ωτ = 1. We deﬁne the negative witness size of x as:
w−(x, P) = w−(x) = min{∥ωA∥2 : ω ∈L(V, R) : ωAΠH(x) = 0, ωτ = 1},
if there exists a negative witness, and w−(x) = ∞otherwise. If w+(x) is ﬁnite, we say that x is
positive (wrt. P), and if w−(x) is ﬁnite, we say that x is negative. We let P1 denote the set of
positive inputs, and P0 the set of negative inputs for P. Note that for every x ∈[q]n, exactly one
of w−(x) and w+(x) is ﬁnite; that is, (P0, P1) partitions [q]n.
For a decision problem f : X ⊆[q]n →{0, 1}, we say that P decides f if f −1(0) ⊆P0 and
f −1(1) ⊆P1. In that case, we can use P to construct a quantum algorithm that decides f.
6


---- page 7 ----

Theorem 2.3 ([Rei09]). Fix f : X ⊆[q]n →{0, 1}, and let P be a span program on [q]n that
decides f. Let W+(f, P) = maxx∈f−1(1) w+(x, P) and W−(f, P) = maxx∈f−1(0) w−(x, P). Then
there exists a quantum algorithm that decides f using O(
p
W+(f, P)W−(f, P)) queries.
We call
p
W+(f, P)W−(f, P) the complexity of P. It is known that for any decision problem,
there exists a span program whose complexity is equal, up to constants, to its query complexity
[Rei09, Rei11] ([Jef14, Sec. 7.1] removes log factors in this statement), however, it is generally a
diﬃcult task to ﬁnd such an optimal span program.
2.2
Span Programs and Approximate Decision Problems
Consider a span program P and x ∈P0. Suppose there is some |w⟩∈H(x) such that A|w⟩comes
extremely close to τ. We might say that x is very close to being in P1. If all vectors in H(y)
for y ∈P0 \ {x} are very far from τ, it might be slightly more natural to consider the partition
(P0 \ {x}, P1 ∪{x}) rather than (P0, P1).
As further motivation, we mention a construction of Reichardt [Rei09, Sec. 3 of full version]
that takes any quantum query algorithm with one-sided error, and converts it into a span program
whose complexity matches the query complexity of the algorithm. The target of the span program
is the vector |1, ¯0⟩, which corresponds to a quantum state with a 1 in the answer register and 0s
elsewhere. If an algorithm has no error on 1-inputs, it can be modiﬁed so that it always ends in
exactly this state, by uncomputing all but the answer register. An algorithm with two-sided error
cannot be turned into a span program using this construction, because there is error in the ﬁnal
state. This is intuitively in opposition to the evidence that span programs characterize bounded
(two-sided) error quantum query complexity. The exactness required by span programs seems to
contrast the spirit of non-exact quantum algorithms.
This motivates us to consider the positive error of an input, or how close it comes to being
positive. Since there is no meaningful notion of distance in V , we consider closeness in H.
Deﬁnition 2.4 (Positive Error). For any span program P on [q]n, and x ∈[q]n, we deﬁne the
positive error of x in P as:
e+(x) = e+(x, P) := min
ΠH(x)⊥|w⟩

2
: A|w⟩= τ

.
Note that e+(x, P) = 0 if and only if x ∈P1. Any |w⟩such that
ΠH(x)⊥|w⟩

2
= e+(x) is called a
min-error positive witness for x in P. We deﬁne
˜w+(x) = ˜w+(x, P) := min

∥|w⟩∥2 : A|w⟩= τ,
ΠH(x)⊥|w⟩

2
= e+(x)

.
A min-error positive witness that also minimizes ∥|w⟩∥2 is called an optimal min-error positive
witness for x.
Note that if x ∈P1, then e+(x) = 0. In that case, a min-error positive witness for x is just a
positive witness, and ˜w+(x) = w+(x).
We can deﬁne a similar notion for positive inputs, to measure their closeness to being negative.
Deﬁnition 2.5 (Negative Error). For any span program P on [q]n and x ∈[q]n, we deﬁne the
negative error of x in P as:
e−(x) = e−(x, P) := min
nωAΠH(x)
2 : ω(τ) = 1
o
.
7


---- page 8 ----

Again, e−(x, P) = 0 if and only if x ∈P0. Any ω such that
ωAΠH(x)
2 = e−(x, P) is called a
min-error negative witness for x in P. We deﬁne
˜w−(x) = ˜w−(x, P) := min
n
∥ωA∥2 : ω(τ) = 1,
ωAΠH(x)
2 = e−(x, P)
o
.
A min-error negative witness that also minimizes ∥ωA∥2 is called an optimal min-error negative
witness for x.
It turns out that the notion of span program error has a very nice characterization as exactly
the reciprocal of the witness size:
∀x ∈P0, w−(x) =
1
e+(x),
and
∀x ∈P1, w+(x) =
1
e−(x),
which we prove shortly in Theorem 2.10 and Theorem 2.11. This is a very nice state of aﬀairs, for a
number of reasons. It allows us two ways of thinking about approximate span programs: in terms of
how small the error is, or how large the witness size is. That is, we can say that an input x ∈P0 is
almost positive either because its positive error is small, or equivalently, because its negative witness
size is large. In general, we can think of P as not only partitioning P into (P0, P1), but inducing an
ordering on [q]n from most negative — smallest negative witness, or equivalently, largest positive
error — to most positive — smallest positive witness, or equivalently, largest negative error. For
example, on the domain {x(1), . . . , x(6)} ⊂[q]n, P might induce the following ordering:
x(1)
x(2)
x(3)
x(4) x(5)
x(6)
increasing positive error/
decreasing negative witness size
increasing negative error/
decreasing positive witness size
The inputs {x(1), x(2), x(3)} are in P0, and w−(x(1)) < w−(x(2)) < w−(x(3)) (although it is gen-
erally possible for two inputs to have the same witness size).
The inputs {x(4), x(5), x(6)} are
in P1, and w+(x(4)) > w+(x(5)) > w+(x(6)).
The span program exactly decides the partition
({x(1), x(2), x(3)}, {x(4), x(5), x(6)}), but we say it approximates any partition that respects the
ordering.
If we obtain a partition by drawing a line somewhere on the left side, for example
({x(1), x(2)}, {x(3), x(4), x(5), x(6)}), we say P negatively approximates the function corresponding to
that partition, whereas if we obtain a partition by drawing a line on the right side, for example
({x(1), x(2), x(3), x(4), x(5)}, {x(6)}), we say P positively approximates the function.
Deﬁnition 2.6 (Functions Approximately Associated with P). Let P be a span program on [q]n,
and f : X ⊆[q]n →{0, 1} a decision problem. For any λ ∈(0, 1), we say that P positively λ-
approximates f if f −1(1) ⊆P1, and for all x ∈f −1(0), either x ∈P0, or w+(x, P) ≥1
λW+(f, P).
We say that P negatively λ-approximates f if f −1(0) ⊆P0, and for all x ∈f −1(1), either x ∈P1,
or w−(x, P) ≥1
λW−(f, P). If P decides f exactly, then both conditions hold for any value of λ,
and so we can say that P 0-approximates f.
This allows us to consider a much broader class of functions associated with a particular span
program. This association is useful, because as with the standard notion of association between a
function f and a span program, if a function is approximated by a span program, we can convert
the span program into a quantum algorithm that decides f using a number of queries related to
the witness sizes. Speciﬁcally, we get the following theorem, proven in Section 3.
8


---- page 9 ----

Theorem 2.7 (Approximate Span Program Decision Algorithms). Fix f : X ⊆[q]n →{0, 1}, and
let P be a span program that positively λ-approximates f. Deﬁne
W+ = W+(f, P) :=
max
x∈f−1(1) w+(x, P)
and
f
W−= f
W−(f, P) :=
max
x∈f−1(0) ˜w−(x, P).
There is a quantum algorithm that decides f with bounded error in O
√
W+f
W−
(1−λ)3/2 log
1
1−λ

queries.
Similarly, let P be a span program that negatively λ-approximates f. Deﬁne
W−= W−(f, P) :=
max
x∈f−1(0) w−(x, P)
and
f
W+ = f
W+(f, P) :=
max
x∈f−1(1) ˜w+(x, P).
There is a quantum algorithm that decides f with bounded error in O
√
W−f
W+
(1−λ)3/2 log
1
1−λ

queries.
With the ability to distinguish between diﬀerent witness sizes, we can obtain algorithms for
estimating the witness size.
Theorem 2.8 (Witness Size Estimation Algorithm). Fix f : X ⊆[q]n →R≥0. Let P be a span
program such that for all x ∈X, f(x) = w+(x, P) and deﬁne f
W−= f
W−(f, P) = maxx∈X ˜w−(x, P).
There exists a quantum algorithm that estimates f to accuracy ε in eO

1
ε3/2
q
w+(x)f
W−

queries.
Similarly, let P be a span program such that for all x ∈X, f(x) = w−(x, P) and deﬁne f
W+ =
f
W+(f, P) = maxx∈X ˜w+(x, P). Then there exists a quantum algorithm that estimates f to accuracy
ε in eO

1
ε3/2
q
w−(x)f
W+

queries.
The algorithms of Theorem 2.7 and 2.8 involve phase estimation of a particular unitary U, as
with previous span program algorithms, in order to distinguish the 1-eigenspace of U from its other
eigenspaces. In general, it may not be feasible to calculate the phase gap of U, so for the algorithms
of Theorem 2.7 and 2.8, as with previous algorithms, we use the eﬀective spectral gap lemma to
bound the overlap of a particular initial state with eigenspaces of U corresponding to small phases.
However, by relating the phase gap of U to the spectrum of A and A(x) := AΠH(x), we show how
to lower bound the phase gap in some cases, which may give better results. In particular, in our
application to eﬀective resistance, it is not diﬃcult to bound the phase gap in this way, which leads
to an improved upper bound. In general we have the following theorem.
Theorem 2.9 (Witness Size Estimation Algorithm Using Real Phase Gap). Fix f : X ⊆[q]n →
R≥0 and let P = (H, V, τ, A) be a normalized span program (see Deﬁnition 2.12) on [q]n such that
for all x ∈X, f(x) = w+(x, P) (resp. f(x) = w−(x)). If κ ≥
σmax(A)
σmin(AΠH(x)) for all x ∈X, then the
quantum query complexity of estimating f(x) to relative accuracy ε is at most eO
√
f(x)κ
ε

.
Theorem 2.7 is proven in Section 3.2, and Theorem 2.8 is proven in Section 3.3, and Theorem 2.9
is proven in Section 3.4.
2.3
Example
To illustrate how these ideas might be useful, we will give a brief example of how a span program
that leads to an algorithm for the OR function can be combined with our results to additionally
9


---- page 10 ----

give algorithms for threshold functions and approximate counting. We deﬁne a span program P on
{0, 1}n as follows:
V = R,
τ = 1,
Hi = Hi,1 = span{|i⟩},
Hi,0 = {0},
A =
n
X
i=1
⟨i|.
So we have H = span{|i⟩: i ∈[n]} and H(x) = span{|i⟩: xi = 1}. It’s not diﬃcult to see that P
decides OR. In particular, we can see that the optimal positive witness for any x such that |x| > 0
is |wx⟩= P
i:xi=1
1
|x||i⟩. The only linear function ω : R →R that maps τ to 1 is the identity, and
indeed, this is a negative witness for the string ¯0 = 0 . . . 0, since H(¯0) = {0}, and so ωAΠH(¯0) = 0.
Let λ ∈(0, 1), t ∈[n], and let f be a threshold function deﬁned by f(x) = 1 if |x| ≥t and
f(x) = 0 if |x| ≤λt, with the promise that one of these conditions holds. Note that if f(x) = 1,
then w+(x) = ∥|wx⟩∥2 =
1
|x| ≤
1
t , so W+(f, P) =
1
t .
On the other hand, if f(x) = 0, then
w+(x) =
1
|x| ≥1
λt = 1
λW+(f, P), so P positively λ-approximates f. The only approximate negative
witness is ω the identity, so we have f
W−= ∥ωA∥2 = ∥A∥2 = n.
By Theorem 2.7, there is a
quantum algorithm for f with query complexity
1
(1−λ)3/2
q
W+f
W−=
1
(1−λ)3/2
p
n/t.
Furthermore, since w+(x) =
1
|x|, by Theorem 2.8, we can estimate
1
|x| to relative accuracy ε, and
therefore we can estimate |x| to relative accuracy 2ε, in quantum query complexity
1
ε3/2
p
n/|x|.
These upper bounds do not have optimal scaling in ε, as the actual quantum query complexi-
ties of these problems are
1
1−λ
p
n/t and 1
ε
p
n/|x| [BBBV97, BHMT02, BBC+01], however, using
Theorem 2.9, the optimal query complexities can be recovered.
2.4
Span Program Structure and Scaling
In this section, we present some observations about the structure of span programs that will be
useful in the design and analysis of our algorithms, and for general intuition. We begin by formally
stating and proving Theorem 2.10 and Theorem 2.11, relating error to witness size.
Theorem 2.10. Let P be a span program on [q]n and x ∈P0. If | ˜w⟩is an optimal min-error
positive witness for x, and ω is an optimal exact negative witness for x, then
(ωA)† =
ΠH(x)⊥| ˜w⟩
ΠH(x)⊥| ˜w⟩

2 ,
and so
w−(x) =
1
e+(x).
Proof. Let | ˜w⟩be an optimal min-error positive witness for x, and ω an optimal zero-error neg-
ative witness for x. We have (ωA)| ˜w⟩= ωτ = 1 and furthermore, since ωAΠH(x) = 0, we have
(ωA)ΠH(x)⊥| ˜w⟩= 1. Thus, write (ωA)† =
ΠH(x)⊥| ˜w⟩
ΠH(x)⊥| ˜w⟩

2 + |u⟩such that ⟨u|ΠH(x)⊥| ˜w⟩= 0. Deﬁne
|werr⟩= ΠH(x)⊥| ˜w⟩. We have A(| ˜w⟩−Πker A|werr⟩) = A| ˜w⟩= τ, so by assumption that | ˜w⟩has
minimal error,
ΠH(x)⊥| ˜w⟩
 ≤
ΠH(x)⊥(| ˜w⟩−Πker A|werr⟩)
 ≤
ΠH(x)⊥| ˜w⟩−Πker A|werr⟩
 =
Π(ker A)⊥|werr⟩
 ,
so ∥|werr⟩∥≤
Π(ker A)⊥|werr⟩
, and so we must have |werr⟩∈(ker A)⊥. Thus, ker ⟨werr| ⊆ker A,
so by the fundamental homomorphism theorem, there exists a linear function ¯ω : colA →R such
10


---- page 11 ----

that ¯ωA = ⟨werr|. Furthermore, we have ¯ωτ = ¯ωA| ˜w⟩= ⟨˜w|ΠH(x)⊥| ˜w⟩=
ΠH(x)⊥| ˜w⟩

2
= e+(x),
so ω′ =
¯ω
e+(x) has ω′τ = 1. By the optimality of ω, we must have ∥ωA∥2 ≤∥ω′A∥2, so

ΠH(x)⊥| ˜w⟩
e+(x)
+ |u⟩

2
≤

ΠH(x)⊥| ˜w⟩
e+(x)

2
and so |u⟩= 0. Thus (ωA)† =
ΠH(x)⊥| ˜w⟩
e+(x)
and w−(x) = ∥ωA∥2 =
ΠH(x)⊥| ˜w⟩

2
e+(x)2
=
1
e+(x).
Theorem 2.11. Let P be a span program on [q]n and x ∈P1. If |w⟩is an optimal exact positive
witness for x, and ˜ω is an optimal min-error negative witness for x, then
|w⟩= ΠH(x)(˜ωA)†
˜ωAΠH(x)
2
and so
w+(x) =
1
e−(x).
Proof. Let ˜ω be an optimal min-error negative witness for x, and deﬁne |w′⟩=
ΠH(x)(˜ωA)†
∥˜ωAΠH(x)∥
2 . First
note that |w′⟩∈H(x). We will show that |w′⟩is a positive witness for x by showing A|w′⟩= τ.
Suppose τ and A|w′⟩are linearly independent, and let α ∈L(V, R) be such that α(A|w′⟩) = 0 and
α(τ) = 1. Then for any ε ∈[0, 1], we have (ε˜ω + (1 −ε)α)τ = 1, so by optimality of ˜ω,
˜ωAΠH(x)
2
≤
(ε˜ω + (1 −ε)α)AΠH(x)
2
=
ε2 ˜ωAΠH(x)
2 + (1 −ε)2 αAΠH(x)
2 since α(AΠH(x)(˜ωA)†) = 0
(1 −ε2)
˜ωAΠH(x)
2
≤
(1 −ε)2 αAΠH(x)
2 .
This implies
˜ωAΠH(x)
 ≤0, a contradiction, since
˜ωAΠH(x)
 > 0. Thus, we must have A|w′⟩=
rτ for some scalar r, so ˜ω(A|w′⟩) = r˜ω(τ). We then have ˜ω(A|w′⟩) = ˜ωA
ΠH(x)(˜ωA)†
∥˜ωAΠH(x)∥
2 = 1, and so we
have r = 1, and thus A|w′⟩= τ. So |w′⟩is a positive witness for x. Let |w⟩∈H(x) be an optimal
positive witness for x, so ∥|w⟩∥2 = w+(x). We have
⟨w′|w⟩= ˜ωAΠH(x)|w⟩
˜ωAΠH(x)
2 =
˜ωτ
˜ωAΠH(x)
2 =
1
˜ωAΠH(x)
2 =
|w′⟩
2 .
Thus ∥|w′⟩∥2 ≤∥|w′⟩∥∥|w⟩∥by the Cauchy-Schwarz inequality, so since |w⟩is optimal, we must
have ∥|w⟩∥= ∥|w′⟩∥. Since the the smallest |w⟩such that AΠH(x)|w⟩= τ is uniquely deﬁned as
(AΠH(x))+τ, we have |w⟩= |w′⟩. Thus w+(x) = ∥|w⟩∥2 = ∥|w′⟩∥2 =
1
∥˜ωAΠH(x)∥
2 =
1
e−(x).
Positive Witnesses
Fix a span program P = (H, V, τ, A) on [q]n. In general, a positive witness
is any |w⟩∈H such that A|w⟩= τ. Assume the set of all such vectors is non-empty, and let |w⟩
be any vector in H such that A|w⟩= τ. Then the set of positive witnesses is exactly
W := |w⟩+ ker A = {|w⟩+ |h⟩: |h⟩∈ker A}.
It is well known, and a simple exercise to prove, that the unique shortest vector in W is A+τ, and
it is the unique vector in W ∩(ker A)⊥. We can therefore talk about the unique smallest positive
witness, whenever W is non-empty.
11


---- page 12 ----

Deﬁnition 2.12. Fix a span program P, and suppose W = {|h⟩∈H : A|h⟩= τ} is non-empty. We
deﬁne the minimal positive witness of P to be |w0⟩∈W with smallest norm — that is, |w0⟩= A+τ.
We deﬁne N+(P) := ∥|w0⟩∥2.
Since |w0⟩∈(ker A)⊥, we can write any positive witness |w⟩as |w0⟩+|w⊥
0 ⟩for some |w⊥
0 ⟩∈ker A.
If we let T = A−1(τ), then we can write T = span{|w0⟩} ⊕ker A.
Negative Witnesses
Just as we can talk about a minimal positive witness, we can also talk
about a minimal negative witness of P: any ω0 ∈L(V, R) such that ω0(τ) = 1, that minimizes
∥ω0A∥. We deﬁne N−(P) = minω0:ω0(τ)=1 ∥ω0A∥2. Note that unlike |w0⟩, ω0 might not be unique.
There may be distinct ω0, ω′
0 ∈L(V, R) that map τ to 1 and have minimal complexity, however,
one can easily show that in that case, ω0A = ω′
0A, and that the unique globally optimal negative
witness in colA is
⟨τ|
∥τ∥2.
For any minimal negative witness, ω0, ω0A is conveniently related to the minimal positive
witness |w0⟩by (ω0A)† =
|w0⟩
N+(P ), and N+(P) =
1
N−(P ). (We leave this as an exercise, since it is
straightforward to prove, and not needed for our results).
Span Program Scaling and Normalization
By scaling τ to get a new target τ ′ = Bτ, we
can scale a span program by an arbitrary positive real number B, so that all positive witnesses are
scaled by B, and all negative witnesses are scaled by 1
B . Note that this leaves W+W−unchanged,
so we can in some sense consider the span program invariant under this scaling.
Deﬁnition 2.13. A span program P is normalized if N+(P) = N−(P) = 1.
Any span program can be converted to a normalized span program by replacing the target with
τ ′ =
τ
N+. However, it will turn out to be desirable to normalize a span program, and also scale it,
independently. We can accomplish this to some degree, as shown by the following theorem.
Theorem 2.14 (Span program scaling). Let P = (H, V, τ, A) be any span program on [q]n, and let
N = ∥|w0⟩∥2 for |w0⟩the minimal positive witness of P. For β ∈R>0, deﬁne P β = (Hβ, V β, τ β, Aβ)
as follows, for |ˆ0⟩and |ˆ1⟩two vectors orthogonal to H and V :
∀j ∈[n], a ∈[q], Hβ
j,a := Hj,a,
Hβ
true = Htrue ⊕span{|ˆ1⟩},
Hβ
false = Hfalse ⊕span{|ˆ0⟩}
V β = V ⊕span{|ˆ1⟩},
Aβ = βA + |τ⟩⟨ˆ0| +
p
β2 + N
β
|ˆ1⟩⟨ˆ1|,
τ β = |τ⟩+ |ˆ1⟩
Then we have the following:
• For all x ∈P1, w+(x, P β) =
1
β2w+(x, P) +
β2
N+β2 and ˜w−(x, P β) ≤β2 ˜w−(x, P) + 2;
• for all x ∈P0, w−(x, P β) = β2w−(x, P) + 1 and ˜w+(x, P β) ≤
1
β2 ˜w+(x, P) + 2;
• the minimal witness of P β is |wβ
0 ⟩=
β
β2+N |w0⟩+
N
β2+N |ˆ0⟩+
β
√
β2+N |ˆ1⟩, and
|wβ
0 ⟩

2
= 1.
Proof of Theorem 2.14 is postponed to Appendix A, as it consists of straightforward computation.
12


---- page 13 ----

3
Span Program Algorithms
In this section we describe several ways in which a span program can be turned into a quantum
algorithm. As in the case of algorithms previously constructed from span programs, our algorithms
will consist of many applications of a unitary on H, applied to some initial state. Unlike previous
applications, we will use |w0⟩, the minimal positive witness of P, as the initial state, assuming P is
normalized so that ∥|w0⟩∥= 1. This state is independent of the input, and so can be generated with
0 queries. For negative span program algorithms, where we want to decide a function negatively
approximated by P, we will use a unitary U(P, x), deﬁned as follows:
U(P, x) := (2Πker A −I)(2ΠH(x) −I) = (2Π(ker A)⊥−I)(2ΠH(x)⊥−I).
This is similar to the unitary used in previous span program algorithms. Note that (2Πker A −I) is
input-independent, and so can be implemented in 0 queries. However, in order to analyze the time
complexity of a span program algorithm, this reﬂection must be implemented (as we are able to do
for our applications, following [BR12]). The reﬂection (2ΠH(x) −I) depends on the input, but it is
not diﬃcult to see that it requires two queries to implement. Since our deﬁnition of span programs
varies slightly from previous deﬁnitions, we provide a proof of this fact.
Lemma 3.1. The reﬂection (2ΠH(x) −I) can be implemented using 2 queries to x.
Proof. For every i ∈[n] and a ∈[q], let Ri,a = (I −2ΠH⊥
i,a∩Hi), the operator that reﬂects every
vector in Hi that is orthogonal to Hi,a.
This operation is input independent, and so, can be
implemented in 0 queries. For every i ∈[n], let {|ψi,1⟩, . . . , |ψi,mi⟩} be an orthonormal basis for Hi.
Recall that the spaces Hi are orthogonal, so we can map |ψi,j⟩7→|i⟩|ψi,j⟩. Then using one query,
we can map |i⟩|ψi,j⟩7→|i⟩|xi⟩|ψi,j⟩. We then perform Ri,xi on the last register, conditioned on the
ﬁrst two registers, and then uncompute the ﬁrst two registers, using one additional query.
For positive span program algorithms, where we want to decide a function positively approxi-
mated by P, or estimate the positive witness size, we will use a slightly diﬀerent unitary:
U ′(P, x) = (2ΠH(x) −I)(2ΠT −I),
where T = ker A ⊕span{|w0⟩}, the span of positive witnesses. We have U ′ = U †(I −2|w0⟩⟨w0|).
We begin by analyzing the overlap of the initial state, |w0⟩, with the phase spaces of the
unitaries U and U ′ in Section 3.1. In particular, we show that the projections of |w0⟩onto the
0-phase spaces of U and U ′ are exactly related to the witness size. Using the eﬀective spectral
gap lemma (Lemma 1.9), we show that the overlap of |w0⟩with small nonzero phase spaces is
not too large.
Using this analysis, in Section 3.2, we describe how to convert a span program
into an algorithm for any decision problem that is approximated by the span program, proving
Theorem 2.7, and in Section 3.3, we describe how to convert a span program into an algorithm
that estimates the span program witness size, proving Theorem 2.8.
Finally, in Section 3.4, we give a lower bound on the phase gap of U in terms of the spectra
of A and A(x) = AΠH(x), giving an alternative analysis to the eﬀective spectral gap analysis of
Section 3.1 that may be better in some cases, and proving Theorem 2.9.
3.1
Analysis
Negative Span Programs
In this section we analyze the overlap of |w0⟩with the eigenspaces of
U(P, x). For any angle Θ ∈[0, π), we deﬁne Πx
Θ as the orthogonal projector onto the eiθ-eigenspaces
of U(P, x) for which |θ| ≤Θ.
13


---- page 14 ----

Lemma 3.2. Let P be a normalized span program on [q]n. For any x ∈[q]n,
∥Πx
Θ|w0⟩∥2 ≤Θ2
4 ˜w+(x) +
1
w−(x).
In particular, for any x ∈P1, ∥Πx
Θ|w0⟩∥2 ≤Θ2
4 w+(x).
Proof. Suppose x ∈P1, and let |wx⟩be an optimal exact positive witness for x, so Π(ker A)⊥|wx⟩=
|w0⟩. Then since ΠH(x)⊥|wx⟩= 0, we have by the eﬀective spectral gap lemma (Lemma 1.9):
∥Πx
Θ|w0⟩∥2 =
Πx
ΘΠ(ker A)⊥|wx⟩

2
≤Θ2
4 ∥|wx⟩∥2 = Θ2
4 w+(x).
Suppose x ∈P0 and let ωx be an optimal zero-error negative witness for x and | ˜wx⟩an optimal
min-error positive witness for x. First note that Π(ker A)⊥| ˜wx⟩= |w0⟩, so Π(ker A)⊥ΠH(x)| ˜wx⟩+
Π(ker A)⊥ΠH(x)⊥| ˜wx⟩= |w0⟩. Since ΠH(x)⊥
 ΠH(x)| ˜wx⟩

= 0, we have, by Lemma 1.9,
ΠΘΠ(ker A)⊥ΠH(x)| ˜wx⟩

2
≤
Θ2
4
ΠH(x)| ˜wx⟩
2
ΠΘ

|w0⟩−Π(ker A)⊥ΠH(x)⊥| ˜wx⟩

2
≤
Θ2
4 ∥| ˜wx⟩∥2
ΠΘ

|w0⟩−Π(ker A)⊥(ωxA)†
w−(x)

2
≤
Θ2
4 ∥| ˜wx⟩∥2 .
In the last step, we used the fact that (ωxA)†
w−(x) = ΠH(x)⊥| ˜wx⟩, by Theorem 2.10. Next note that
Π(ker A)⊥(ωxA)† = (ωxA)† and ΠH(x)⊥(ωxA)† = (ωxA)†, so U(ωxA)† = (ωxA)†, and therefore,
ΠΘ(ωxA)† = (ωxA)†. Thus:
ΠΘ|w0⟩−(ωxA)†
w−(x)

2
≤
Θ2
4 ∥| ˜wx⟩∥2
∥ΠΘ|w0⟩∥2 +
1
w−(x) −2
1
w−(x)⟨w0|ΠΘ(ωxA)†
≤
Θ2
4 ˜w+(x)
∥ΠΘ|w0⟩∥2 +
1
w−(x) −2
1
w−(x)(ωxA|w0⟩)†
≤
Θ2
4 ˜w+(x)
∥ΠΘ|w0⟩∥2 +
1
w−(x) −2
1
w−(x)(ωxτ)†
≤
Θ2
4 ˜w+(x)
∥ΠΘ|w0⟩∥2
≤
Θ2
4 ˜w+(x) +
1
w−(x),
where in the last line we used the fact that ωxτ = 1.
Lemma 3.3. Let P be a normalized span program on [q]n. For any x ∈[q]n,
∥Πx
0|w0⟩∥2 =
1
w−(x).
In particular, for any x ∈P1, ∥Πx
0|w0⟩∥= 0.
Proof. By Lemma 3.2, we have ∥Πx
0|w0⟩∥2 ≤
1
w−(x). To see the other direction, let ωx be an optimal
zero-error negative witness for x (if none exists, then w−(x) = ∞and the statement is vacuously
true). Deﬁne |u⟩= (ωxA)†. By the proof of Lemma 3.2, U|u⟩= |u⟩. We have ⟨u|w0⟩= ωxA|w0⟩=
ωxτ = 1 and ∥|u⟩∥2 = ∥ωxA∥2 = w−(x), so we have: ∥Πx
0|w0⟩∥2 ≥
 |u⟩⟨u|
∥|u⟩∥2 |w0⟩

2
=
1
w−(x).
14


---- page 15 ----

Positive Span Programs
We now prove results analogous to Lemma 3.2 and 3.3 for the unitary
U ′(P, x). For any angle Θ ∈[0, π), we deﬁne Π
x
Θ as the projector onto the θ-phase spaces of U ′(P, x)
for which |θ| ≤Θ.
Lemma 3.4. Let P be a normalized span program on [q]n. For any x ∈[q]n,
Π
x
Θ|w0⟩
2 ≤Θ2
4 ˜w−(x) +
1
w+(x).
In particular, if x ∈P0, then
Π
x
Θ|w0⟩
2 ≤Θ2
4 w−(x).
Proof. If x ∈P0, then let ωx be an optimal exact negative witness for x, so ωxAΠH(x) = 0, and we
thus have, by the eﬀective spectral gap lemma (Lemma 1.9),
Π
x
ΘΠT (ωxA)†
2
≤Θ2
4 ∥ωxA∥2 = Θ2
4 w−(x).
We have ωxAΠT = ωxA(Πker A + |w0⟩⟨w0|) = ωxA|w0⟩⟨w0| = ωxτ⟨w0| = ⟨w0|, so
Π
x
Θ|w0⟩
2 ≤
Θ2
4 w−(x).
Suppose x ∈P1, and let |wx⟩be an optimal zero-error positive witness for x, and ˜ωx an
optimal min-error negative witness for x. By Theorem 2.11, we have
|wx⟩
w+(x) = ΠH(x)(˜ωxA)†. Since
ΠH(x)(˜ωxAΠH(x)⊥)† = 0, we have, by Lemma 1.9,
Π
x
ΘΠT (˜ωxAΠH(x)⊥)†
2
≤
Θ2
4
˜ωxAΠH(x)⊥

2
Π
x
ΘΠT

(˜ωxA)† −|wx⟩
w+(x)

2
≤
Θ2
4 ∥˜ωxA∥2
Π
x
ΘΠT (˜ωxA)† −|wx⟩
w+(x)

2
≤
Θ2
4 ˜w−(x).
In the last line we used the fact that ΠT |wx⟩= ΠH(x)|wx⟩= |wx⟩, so U ′|wx⟩= |wx⟩, and thus
Π
x
Θ|wx⟩= |wx⟩.
Note that ˜ωxAΠT = ˜ωxA(Πker A + |w0⟩⟨w0|) = ˜ωxA|w0⟩⟨w0| = ˜ωxτ⟨w0| = ⟨w0|. Thus, we can
continue from above as:
Π
x
Θ|w0⟩−|wx⟩
w+(x)

2
≤
Θ2
4 ˜w−(x)
Π
x
Θ|w0⟩
2 +

|wx⟩
w+(x)

2
−
2
w+(x)⟨w0|Π
x
Θ|wx⟩
≤
Θ2
4 ˜w−(x)
Π
x
Θ|w0⟩
2 +
1
w+(x) −
2
w+(x)⟨w0|wx⟩
≤
Θ2
4 ˜w−(x)
Π
x
Θ|w0⟩
2
≤
Θ2
4 ˜w−(x) +
1
w+(x),
where in the last line we used the fact that ⟨w0|wx⟩= 1.
15


---- page 16 ----

Lemma 3.5. Let P be a normalized span program on [q]n. For any x ∈[q]n,
Π
x
0|w0⟩
2 =
1
w+(x).
In particular, if x ∈P0, then
Π
x
0|w0⟩
 = 0.
Proof. By Lemma 3.4,
Π
x
0|w0⟩
2 ≤
1
w+(x). Let |wx⟩= |w0⟩+|w⊥
0 ⟩be an optimal zero-error positive
witness for x. Since |wx⟩∈H(x) ∩T, U ′|wx⟩= |wx⟩, so
Π
x
0|w0⟩
2 ≥⟨wx|w0⟩
∥|wx⟩∥2 ≥
1
w+(x).
3.2
Algorithms for Approximate Span Programs
Using the spectral analysis from Section 3.1, we can design an algorithm that decides a function that
is approximated by a span program. We will give details for the negative case, using Lemma 3.2
and 3.3. A nearly identical argument proves the analogous statement for the positive case, using
Lemma 3.4 and 3.5 instead.
Throughout this section, ﬁx a decision problem f on [q]n, and let P be a normalized span
program that negatively λ-approximates f. By Lemma 3.3 and 3.2, it is possible to distinguish
between the cases f(x) = 0, in which
1
w−(x) ≥
1
W−, and f(x) = 1, in which
1
w−(x) ≤
λ
W−using phase
estimation to suﬃcient precision, and amplitude estimation on a 0 in the phase register. We give
details in the following theorem.
Lemma 3.6. Let P be a normalized λ-negative approximate span program for f. Then the quantum
query complexity of f is at most O

1
(1−λ)3/2 W−
q
f
W+ log W−
1−λ

.
Proof. Let U(P, x) = Pm
j=1 eiθj|ψj⟩⟨ψj|, and let |w0⟩= Pm
j=1 αj|ψj⟩. Then applying phase esti-
mation (Theorem 1.5) to precision Θ =
r
4(1−λ)
3W−f
W+ and error ε = 1
6
1−λ
W−produces a state |w′
0⟩=
Pm
j=1 αj|ψj⟩|ωj⟩such that if θj = 0, then |ωj⟩= |0⟩, and if |θj| > Θ then |⟨ωj|0⟩|2 ≤ε. Let Λ0 be
the projector onto states with 0 in the phase register. We have: ∥Λ0|w′
0⟩∥2 = Pm
j=1 |αj|2|⟨0|ωj⟩|2.
Suppose x ∈f −1(0), so ∥Πx
0|w0⟩∥2 = P
j:θj=0 |αj|2 ≥
1
w−(x), by Lemma 3.3, and thus we have:
Λ0|w′
0⟩
2 ≥
X
j:θj=0
|αj|2|⟨0|0⟩|2 = ∥Πx
0|w0⟩∥2 ≥
1
w−(x) ≥
1
W−
=: p0.
On the other hand, suppose x ∈f −1(1). Since P negatively λ-approximates f and x ∈f −1(1),
w−(x, P) ≥1
λW+(x, P). By Lemma 3.2, we have
∥Πx
Θ|w0⟩∥2 ≤
1
w−(x, P) + Θ2
4 ˜w+(x, P) ≤
λ
W−
+
1 −λ
3W−f
W+
f
W+ = 1
3
1 + 2λ
W−
and thus
Λ0|w′
0⟩
2 ≤
X
j:|θj|≤Θ
|αj|2 +
X
j:|θj|>Θ
|αj|2|⟨ωj|0⟩|2 = ∥Πx
Θ|w0⟩∥2 + ε
X
j:|θj|>Θ
|αj|2 ≤1 + 2λ
3W−
+ 1 −λ
6W−
=: p1.
By Corollary 1.8, we can distinguish between these cases using O
 √p0
p0−p1

calls to phase estimation,
which costs 1
Θ log 1
ε. In this case, we have
p0 −p1 = 1 −1
3 −2
3λ −1
6 + 1
6λ
W−
= 1
2
1 −λ
W−
.
16


---- page 17 ----

The total number of calls to U is:
√p0
p0 −p1
1
Θ log 1
ε =
W−
√W−(1 −λ)
s
W−f
W+
1 −λ log W−
1 −λ =
W−
q
f
W+
(1 −λ)3/2 log W−
1 −λ.
In addition to wanting to extend this to non-normalized span programs, we note that this
expression is not symmetric in the positive and negative error. Using Theorem 2.14, we can nor-
malize any span program, while also scaling the positive and negative witnesses. This gives us the
following.
Corollary 3.7. Let P be any span program that negatively λ-approximates f. Then the quantum
query complexity of f is at most O

1
(1−λ)3/2
q
W−(f, P)f
W+(f, P) log
1
1−λ

.
Proof. We will use the scaled span program described in Theorem 2.14. Let β =
1
√
W−(f,P ). Then
P β is a normalized span program with
W−(f, P β) =
max
x∈f−1(0) w−(x, P β) = β2
max
x∈f−1(0) w−(x, P) + 1 =
1
W−
W−+ 1 = 2,
and
f
W+(f, P β) =
max
x∈f−1(1) ˜w+(x, P β) ≤1
β2
max
x∈f−1(1) ˜w+(x, P) + 2 = W−(f, P)f
W+(f, P) + 2.
If we deﬁne λ(β) :=
maxx∈f−1(0) w−(x,P β)
minx∈f−1(1) w−(x,P β) =
β2W−(f,P )+1
β2 1
λ W−(f,P )+1 =
2
1
λ +1, then clearly P β negatively λ(β)-
approximates f, so we can apply Lemma 3.6. We have
1
1−λ(β) =
1
1−2λ
1+λ = 1+λ
1−λ so we can decide f
in query complexity (neglecting constants):
1 + λ
1 −λ
 3
2r
2

W−(f, P)f
W+(f, P) + 2

log 21 + λ
1 −λ =
1
(1 −λ)
3
2
q
W−(f, P)f
W+(f, P) log
1
1 −λ.
By computations analogous to Lemma 3.6 and Corollary 3.7 (using β = √W+), we can show
that if P positively λ-approximates f, then f has quantum query complexity O

1
(1−λ)3/2
q
W+f
W−log
1
1−λ

.
This and Corollary 3.7 imply Theorem 2.7.
3.3
Estimating the Witness Size
Using the algorithms for deciding approximate span programs (Theorem 2.7) as a black box, we
can construct a quantum algorithm that estimates the positive or negative witness size of an input
using standard algorithmic techniques. We give the full proof for the case of positive witness size,
as negative witness size is virtually identical. This proves Theorem 2.8.
Theorem 3.8 (Estimating the Witness Size). Fix f : X ⊆[q]n →R>0. Let P be a span program
on [q]n such that for all x ∈X, f(x) = w+(x, P). Then the quantum query complexity of estimating
f to accuracy ε is eO
√
w+(x)f
W−(P )
ε3/2

.
Proof. We will estimate e(x) =
1
w+(x). The basic idea is to use the algorithm from Theorem 2.7 to
narrow down the interval in which the value of e(x) may lie. Assuming that the span program is
17


---- page 18 ----

normalized (which is without loss of generality, since normalizing by scaling τ does not impact rel-
ative accuracy) we can begin with the interval [0, 1]. We stop when we reach an interval [emin, emax]
such that the midpoint ˜e = emax+emin
2
satisﬁes (1 −ε)emax ≤˜e ≤(1 + ε)emin.
Let Decide(P, w, λ) be the quantum algorithm from Theorem 2.7 that decides the (partial)
function g : P1 →{0, 1} deﬁned by g(x) = 1 if w+(x) ≤w and g(x) = 0 if w+(x) ≥w
λ . We
will amplify the success probability so that with high probability, Decide returns g(x) correctly
every time it is called by the algorithm, and we will assume that this is the case. The full witness
estimation algorithm consists of repeated calls to Decide as follows:
WitnessEstimate(P, ε):
1. e(1)
max = 1, e(1)
min = 0, e(1)
1
= 2
3, e(1)
0
= 1
3
2. For i = 1, 2, . . . repeat:
(a) Run Decide(P, w, λ) with w = 1/e(i)
1
and λ = e(i)
0 /e(i)
1 .
(b) If Decide outputs 1, indicating w+(x) ≤w, set e(i+1)
max = e(i)
max and e(i+1)
min
= e(i)
0 .
(c) Else, set e(i+1)
min
= e(i)
min and e(i+1)
max = e(i)
1 .
(d) If e(i+1)
max ≤(1 + ε)e(i+1)
min , return ˜e = e(i+1)
max +e(i+1)
min
2
.
(e) Else, set e(i+1)
1
= 2
3e(i+1)
max + 1
3e(i+1)
min
and e(i+1)
0
= 1
3e(i+1)
max + 2
3e(i+1)
min .
We can see by induction that for every i, e(i)
min ≤
1
w+(x) ≤e(i)
max. This is certainly true for i = 1,
since w+(x) ≥∥|w0⟩∥2 = 1. Suppose it’s true at step i. At step i we run Decide(P, wi, λi) with
wi = 1/e(i)
1
and wi
λi = 1/e(i)
0 . If
1
w+(x) ≥e(1)
1 , then Decide returns 1, so we have
1
w+(x) ∈[e(i)
0 , e(i)
max] =
[e(i+1)
min , e(i+1)
max ]. If
1
w+(x) ≤e(i)
0 , then Decide returns 0, so we have
1
w+(x) ∈[e(i)
min, e(i)
1 ] = [e(i+1)
min , e(i+1)
max ].
Otherwise,
1
w+(x) ∈[e(i)
0 , e(i)
1 ], which is a subset of both [e(i)
0 , e(i)
max] and [e(i)
min, e(i)
1 ], so in any case,
1
w+(x) ∈[e(i+1)
min , e(i+1)
max ].
To see that the algorithm terminates, let ∆i = e(i)
max −e(i)
min denote the length of the remaining
interval at round i.
We either have ∆i+1 = e(i)
max −e(i)
0
= e(i)
max −1
3e(i)
max −2
3e(i)
min =
2
3∆i, or
∆i+1 = e(i)
1 −e(i)
min = 2
3e(i)
max + 1
3e(i)
min −e(i)
min = 2
3∆i, so ∆i = (2/3)i−1. We terminate at the smallest
T such that (2/3)T−1 = ∆T = e(T)
max −e(T)
min ≤(1 + ε −1)e(T)
min ≤
ε
w+(x). Thus we terminate before
T = ⌈log3/2
w+(x)
ε
+ 1⌉.
Next, we show that, assuming Decide does not err, the estimate is correct to within ε. Let
˜e = 1
2(e(T)
max+e(T)
min) be the returned estimate. Recall that we only terminate when e(T)
max ≤(1+ε)e(T)
min.
We have
1
˜e =
2
e(T)
max + e(T)
min
≤
2
e(T)
max

1 +
1
1+ε
 ≤
2
1
w+(x)

2+ε
1+ε
 ≤(1 + ε) w+(x),
and
1
˜e ≥
2
emin(1 + 1 + ε) ≥
1
1
w+(x)(1 + ε/2) =

1 −
ε/2
1 + ε/2

w+(x) ≥

1 −ε
2

w+(x).
Thus, |1/˜e −w+(x)| ≤εw+(x).
18


---- page 19 ----

By Theorem 2.7, Decide(P, w, λ) runs in cost O
 √
wf
W−
(1−λ)3/2 log
1
1−λ

. Let wi = 1/e(i)
1
and λi =
e(i)
0 /e(i)
1
be the values used at the ith iteration. Since e(i)
1
≤e(i)
max ≤
1
w+(x) + ∆i, we have
1
1 −λi
=
e(i)
1
e(i)
1 −e(i)
0
≤
1
w+(x) + ∆i
2
3e(i)
max + 1
3e(i)
min −1
3e(i)
max −2
3e(i)
min
=
3
w+(x)∆i
+ 3 = O(1/ε),
since ∆i = (2/3)i−1 ≥(2/3)T−1 = Ω

ε
w+(x)

. Observe
√wi
(1−λi)3/2 =
e(i)
1
(e(i)
1 −e(i)
0 )3/2 ≤

1
w+(x) + ∆i

3
∆3/2
i
,
so, ignoring the log
1
1−λi = O(log 1
ε) factor, the cost of the ith iteration can be computed as:
Ci =
q
wif
W−
(1 −λi)3/2 ≤
q
f
W−

1
w+(x) + ∆i

3
∆3/2
i
= 3
q
f
W−
w+(x)
3
2
 3
2 (i−1)
+ 3
q
f
W−
3
2
 1
2(i−1)
.
We can thus compute the total cost (neglecting logarithmic factors):
T
X
i=1
Ci ≤
q
f
W−
w+(x)
T
X
i=1
3
2
 3
2(i−1)
+
q
f
W−
T
X
i=1
3
2
 1
2(i−1)
≤
q
f
W−
w+(x)
  3
2
 3
2T −1
  3
2
3/2 −1
+
q
f
W−
  3
2
 1
2T −1
  3
2
1/2 −1
≤O


q
f
W−
w+(x)
w+(x)
ε
3/2
+
q
f
W−
w+(x)
ε
1/2

= O


q
f
W−w+(x)
ε3/2

,
using the fact that (2/3)T = Θ

ε
w+(x)

.
Finally, we have been assuming that Decide returns the correct bit on every call. We now justify
this assumption. At round i, we will amplify the success probability of Decide to 1 −1
9(2/3)i−1,
incurring a factor of log(9(3/2)i−1) = O(log w+(x)
ε
) in the complexity. Then the total error is at
most:
T
X
i=1
1
9(2/3)i−1 = 1
9
1 −(2/3)T−1
1 −2
3
= 1
3

1 −
ε
w+(x)

≤1
3.
Thus, with probability at least 2/3, Decide never errs, and the algorithm is correct.
3.4
Span Program Phase Gap
The scaling in the error from Theorem 3.8, 1/ε3/2, is not ideal.
For instance, we showed in
Section 2.3 how to construct a quantum algorithm for approximate counting based on a simple
span program for the OR function with complexity that scales like 1/ε3/2 in the error, whereas
the best quantum algorithm for this task has complexity scaling as 1/ε in the error. However, the
following theorem, which is a corollary to Lemma 3.3 and Lemma 3.5, gives an alternative anal-
ysis of the complexity of the algorithm in Theorem 3.8 that may be better in some cases, and in
particular, has the more natural error dependence 1/ε.
Theorem 3.9. Fix f : X ⊆[q]n →R>0.
Let P be a normalized span program on [q]n such
that X ⊆P0, and for all x ∈X, w−(x, P) = f(x); and deﬁne ∆(f) = minx∈X ∆(U(P, x)).
Then there is a quantum algorithm that estimates f to relative accuracy ε using eO

1
ε
√
w−(x,P )
∆(f)

queries. Similarly, let P be a normalized span program such that X ⊆P1, and for all x ∈X,
19


---- page 20 ----

w+(x, P) = f(x); and deﬁne ∆′(f) = minx∈X ∆(U ′(P, x)). Then there is a quantum algorithm that
estimates f with relative accuracy ε using eO

1
ε
√
w+(x,P )
∆′(f)

queries.
Proof. To estimate w−(x), we can use phase estimation of U(P, x) applied to |w0⟩, with precision
∆= ∆(f) and accuracy ǫ = ε
8
1
W−(P,f), however, this results in log W−factors, and W−may be
signiﬁcantly larger than w−(x). Instead, we will start with ǫ = 1
2, and decrease it by 1/2 until
ǫ ≈
ε
w−(x,P ).
Let |w′
0⟩be the result of applying phase estimation to precision ∆= ∆(f) and accuracy ǫ, and
let Λ0 be the projector onto states with 0 in the phase register. We will then estimate ∥Λ0|w′
0⟩∥2
to relative accuracy ε/4 using amplitude estimation. Since ∆≤∆(U(P, x)), we have ∥Πx
0|w0⟩∥2 ≤
∥Λ0|w′
0⟩∥2 ≤∥Πx
∆|w0⟩∥2 + ǫ = ∥Πx
0|w0⟩∥2 + ǫ. By Lemma 3.3, we have ∥Πx
0|w0⟩∥2 =
1
w−(x), so we
will obtain an estimate ˜p of
1
w−(x) such that

1 −ε
4

1
w−(x) ≤˜p ≤

1 + ε
4
 
1
w−(x) + ǫ

.
If ˜p > 2(1 + ε
4)ǫ, then we know that
1
w−(x) ≥ǫ, so we perform one more estimate with accuracy
ǫ′ = ε
8ǫ ≤ε
8
1
w−(x) and return the resulting estimate. Otherwise, we let ǫ′ = ǫ/2 and repeat.
To see that we will eventually terminate, suppose ǫ ≤
1
4w−(x). Then we have
˜p ≥(1 −ε/4)
1
w−(x) ≥(3/4)4ǫ ≥(3/4)(4/5)(1 + ε/4)4ǫ ≥2(1 + ε/4)ǫ,
so the algorithm terminates. Upon termination, we have
˜p ≤(1 + ε/4)

1
w−(x) + ǫ

≤(1 + ε/4)

1
w−(x) + ε
8
1
w−(x)

≤

1 + ε
2

1
w−(x),
so |1/˜p −w−(x)| ≤εw−(x). By Theorem 1.5 and 1.7, the total number of calls to U is:
log 4w−(x)
X
i=0
1
∆
p
w−(x)
ε
log 2i +
p
w−(x)
∆ε
log w−(x)
ε
= 1
∆
p
w−(x)
ε


log 6w−(x)
X
i=0
i + log w−(x)
ε

,
which is at most
√
w−(x)
∆
ε log2 w−(x)
ε
= eO
√
w−(x)
∆ε

. Similarly, we can estimate w+(x) to relative
accuracy ε using eO
√
w+(x)
∆′ε

calls to U ′.
Theorem 3.9 is only useful if a lower bound on the phase gap of U(P, x) or U ′(P, x) can be
computed. This may not always be feasible, but the following two theorems shows it is suﬃcient
to compute the spectral norm of A, and the spectral gap, or speciﬁcally, smallest nonzero singular
value, of the matrix A(x) = AΠH(x). This may still not be an easy task, but in Section 4, we show
that we can get a better algorithm for estimating the eﬀective resistance by this analysis, which,
in the case of eﬀective resistance, is very simple.
Theorem 3.10. Let P be any span program on [q]n. For any x ∈[q]n, ∆(U(P, x)) ≥2σmin(A(x))
σmax(A) .
20


---- page 21 ----

Proof. Let U = U(P, x). Consider −U = (2Π(ker A)⊥−I)(2ΠH(x) −I). By Corollary 1.11, if D
is the discriminant of −U, then ∆(U) ≥2σmin(D), so we will lower bound σmin(D). Since the
orthogonal projector onto (ker A)⊥= rowA is A+A, we have D = A+AΠH(x) = A+A(x).
We have σmin(D) = min|u⟩∈rowD
∥D|u⟩∥
∥|u⟩∥, so let |u⟩∈rowD be a unit vector that minimizes
∥D|u⟩∥. Since |u⟩∈rowD ⊆rowA(x), we have ∥A(x)|u⟩∥≥σmin(A(x)). Since A(x)|u⟩∈colA(x) ⊆
colA = rowA+, we have
σmin(D) =
A+A(x)|u⟩
 ≥σmin(A+) ∥A(x)|u⟩∥≥σmin(A+)σmin(A(x)) = σmin(A(x))
σmax(A) ,
since σmin(A+) =
1
σmax(A). Thus ∆(U) ≥2σmin(A(x))
σmax(A) .
Theorem 3.11. Let P be any span program. For any x ∈P1, ∆(U ′(P, x)) ≥2σmin(A(x))
σmax(A) .
Proof. We have
−U ′(P, x)† = (2(I −Πker A⊕span{|w0⟩}) −I)(2ΠH(x) −I) = (2(I −Πker A −Π|w0⟩) −I)(2ΠH(x) −I),
since |w0⟩∈(ker A)⊥, so −U ′(P, x)† has discriminant:
D′ = (Π(ker A)⊥−Π|w0⟩)ΠH(x) = Π(ker A)⊥ΠH(x) −Π|w0⟩Π(ker A)⊥ΠH(x) = Π|w0⟩⊥D.
Since x ∈P1, let |wx⟩= A(x)+|τ⟩. Then D|wx⟩= A+A(x)|wx⟩= A+|τ⟩= |w0⟩, so |w0⟩∈colD.
Let {|φ0⟩= |w0⟩, |φ1⟩, . . . , |φr−1⟩} be an orthogonal basis for colD.
Then we can write D =
Pr−1
i=0 |φi⟩⟨vi| for |vi⟩= D†|φi⟩̸= 0 (not necessarily orthogonal). Then D′ = Pr−1
i=0 Π|w0⟩⊥|φi⟩⟨vi| =
Pr−1
i=1 |φi⟩⟨vi|, so colD′ = span{|φ1⟩, . . . , |φr−1⟩} = {|φ⟩∈colD : ⟨φ|w0⟩= 0}. Thus:
σmin(D′)
=
min
|u⟩∈colD′
∥⟨u|D′∥
∥|u⟩∥
=
min
|u⟩∈colD:⟨w0|u⟩=0
⟨u|Π|w0⟩⊥D

∥|u⟩∥
=
min
|u⟩∈colD:⟨w0|u⟩=0
∥⟨u|D∥
∥|u⟩∥
≥
min
|u⟩∈colD
∥⟨u|D∥
∥|u⟩∥
=
σmin(D).
By the proof of Theorem 3.10, we have σmin(D) ≥
σmin(A(x))
σmax(A)
and by Corollary 1.11, we have
∆(U ′(P, x)†) = ∆(U ′(P, x)) ≥2σmin(D′) ≥2σmin(D) ≥2σmin(A(x))
σmax(A) .
Combining the last three theorems, we get the following, which has Theorem 2.9 as a special case:
Theorem 3.12. Fix f : X ⊆[q]n →R>0, and deﬁne κ(f) = maxx∈X
σmax(A)
σmin(A(x)). Let P be any
span program on [q]n such that X ⊆P0 (resp. X ⊆P1), and for all x ∈X, f(x) = w−(x, P)
(resp. f(x) = w+(x, P)). Let N = ∥|w0⟩∥2. Then there is a quantum algorithm that estimates f
to relative accuracy ε using eO

κ(f)
ε
p
Nf(x)

(resp. eO

κ(f)
ε
q
f(x)
N

) queries.
Proof. Let P ′ be the span program that is the same as P, but with target τ ′ =
τ
√
N . Then it’s clear
that |w0⟩
√
N is the minimal positive witness of P ′, and furthermore, it has norm 1, so P ′ is normalized.
We can similarly see that for any x ∈P1, if |wx⟩is an optimal positive witness for x in P, then
1
√
N |wx⟩is an optimal positive witness for x in P ′, so w+(x, P ′) = w+(x,P )
N
. Similarly, for any x ∈P0,
if ωx is an optimal negative witness for x in P, then
√
Nωx is an optimal negative witness for x in
P ′, so w−(x, P ′) = Nw−(x, P). By Theorem 3.10 and 3.11, for all x ∈X,
1
∆(U(P ′,x)) ≤κ(f) (resp.
1
∆(U′(P ′,x)) ≤κ(f)). The result then follows from Theorem 3.9.
21


---- page 22 ----

4
Applications
In this section, we will demonstrate how to apply the ideas from Section 3 to get new quantum
algorithms. Speciﬁcally, we will give upper bounds of eO(n
p
Rs,t/ε3/2) and eO(n
p
Rs,t/λ2/ε) on
the time complexity of estimating the eﬀective resistance, Rs,t, between two vertices, s and t, in
a graph. Unlike previous upper bounds, we study this problem in the adjacency model, however,
there are similarities between the ideas of this upper bound and a previous quantum upper bound
in the edge-list model due to Wang [Wan13], which we discuss further at the end of this section.
A unit ﬂow from s to t in G is a real-valued function θ on the directed edges
→
E(G) = {(u, v) :
{u, v} ∈E(G)} such that:
1. for all (u, v) ∈
→
E, θ(u, v) = −θ(v, u);
2. for all u ∈[n] \ {s, t}, P
v∈Γ(u) θ(u, v) = 0, where Γ(u) = {v ∈[n] : {u, v} ∈E}; and
3. P
u∈Γ(s) θ(s, u) = P
u∈Γ(t) θ(u, t) = 1.
Let F be the set of unit ﬂows from s to t in G. The eﬀective resistance from s to t in G is deﬁned:
Rs,t(G) = min
θ∈F
X
{u,v}∈E(G)
θ(u, v)2.
In the adjacency model, we are given, as input, a string x ∈{0, 1}n×n, representing a graph
Gx = ([n], {{i, j} : xi,j = 1}) (we assume that xi,i = 0 for all i, and xi,j = xj,i for all i, j). The
problem of st-connectivity is the following. Given as input x ∈{0, 1}n×n and s, t ∈[n], decide if
there exists a path from s to t in Gx; that is, whether or not s and t are in the same component of
Gx. A span-program-based algorithm for this problem was given in [BR12], with time complexity
eO(n√p), under the promise that, if s and t are connected in Gx, they are connected by a path of
length ≤p. They use the following span program, deﬁned on {0, 1}n×n:
H(u,v),0 = {0}, H(u,v),1 = span{|u, v⟩}, V = Rn, A =
X
u,v∈[n]
(|u⟩−|v⟩)⟨u, v|, |τ⟩= |s⟩−|t⟩.
We have H = span{|u, v⟩: u, v ∈[n]}, and H(x) = span{|u, v⟩: {u, v} ∈E(Gx)}. Throughout this
section, P will denote the above span program. We will use this span program to deﬁne algorithms
for estimating the eﬀective resistance. Ref. [BR12] are even able to show how to eﬃciently imple-
ment a unitary similar to U(P, x), giving a time eﬃcient algorithm. In Appendix B, we adapt their
proof to our setting, showing how to eﬃciently implement U ′(P β, x) for any n−O(1) ≤β ≤nO(1)
and eﬃciently construct the initial state |w0⟩, making our algorithms time eﬃcient as well.
The eﬀective resistance between s and t is related to st-connectivity by the fact that if s and t
are not connected, then Rs,t is undeﬁned (there is no ﬂow from s to t) and if s and t are connected
then Rs,t is related to the number and length of paths from s to t. In particular, if s and t are
connected by a path of length p, then Rs,t(G) ≤p (take the unit ﬂow that simply travels along this
path). In general, if s and t are connected in G, then 2
n ≤Rs,t(G) ≤n −1. The span program for
st-connectivity is amenable to the task of estimating the eﬀective resistance due to the following.
Lemma 4.1 ([BR12]). For any graph Gx on [n], x ∈P1 if and only if s and t are connected, and
in that case, w+(x, P) = 1
2Rs,t(Gx).
A near immediate consequence of this, combined with Theorem 2.8, is the following.
22


---- page 23 ----

Theorem 4.2. There exists a quantum algorithm for estimating Rs,t(Gx) to accuracy ε with time
complexity eO

n√
Rs,t(Gx)
ε3/2

and space complexity O(log n).
Proof. We merely observe that if G is a connected graph, an approximate negative witness is ω :
[n] →R that minimizes
ωAΠH(x)
2 = P
{u,v}∈E(ω(u)−ω(v))2 and satisﬁes ω(s)−ω(t) = 1. That
is, ω is the voltage induced by a unit potential diﬀerence between s and t (see [DS84] for details).
This is not unique, but if we ﬁx ω(s) = 1 and ω(t) = 0, then the ω that minimizes
ωAΠH(x)
2 is
unique, and this is without loss of generality. In that case, for all u ∈[n], 0 ≤ω(u) ≤1, so
˜w−(x) = ∥ωA∥2 = P
u,v∈[n](ω(u) −ω(v)) ≤2n2
and thus
f
W−≤2n2.
By Theorem 2.8, we can estimate Rs,t to precision ε using eO
√
f
W−w+(x)
ε3/2

= eO

n√
Rs,t(Gx)
ε3/2

calls
to U ′(P β, x) for some β, which, by Theorem B.1, costs O(log n) time and space.
By analyzing the spectra of A and A(x), and applying Theorem 2.9, we can get an often better
algorithm (Theorem 4.3). The spectral gap of a graph G, denoted λ2(G), is the second largest
eigenvalue (including multiplicity) of the Laplacian of G, which is deﬁned LG = P
u∈[n] du|u⟩⟨u| −
P
u∈[n]
P
v∈Γ(u) |u⟩⟨v|, where du is the degree of u, and Γ(u) is the set of neighbours of u. The
smallest eigenvalue of LG is 0 for any graph G. A graph G is connected if and only if λ2(G) > 0.
A connected graph G has
2
n2 ≤λ2(G) ≤n.
The following theorem is an improvement over Theorem 4.2 when λ2(G) > ε. In particular, it
is an improvement for all ε when we know that λ2(G) > 1.
Theorem 4.3. Let G be a family of graphs such that for all x ∈G, λ2(Gx) ≥µ. Let f : G × [n] ×
[n] →R>0 be deﬁned by f(x, s, t) = Rs,t(Gx). There exists a quantum algorithm for estimating f
to relative accuracy ε that has time complexity eO
 1
εn
p
Rs,t(Gx)/µ

and space complexity O(log n).
Proof. We will apply Theorem 2.9. We ﬁrst compute ∥|w0⟩∥2, in order to normalize P.
Lemma 4.4. N = ∥|w0⟩∥2 = 1
n.
Proof. Since H(x) = H when Gx is the complete graph, by Lemma 4.1, we need only compute Rs,t
in the complete graph. It’s simple to verify that the optimal unit st-ﬂow in the complete graph has
1
n units of ﬂow on every path of the form (s, u, t) for u ∈[n]\{s, t}, and 2
n units of ﬂow on the edge
(s, t). Thus, Rs,t(Kn) = P
u∈[n]\{s,t} 2(1/n)2 + (2/n)2 = 2/n. Thus ∥|w0⟩∥2 = 1
2Rs,t(Kn) = 1
n.
Next, we compute the following:
Lemma 4.5. For any x ∈G,
σmax(A)
σmin(A(x)) =
q
n
λ2(Gx) ≤
q
n
µ, so κ(f) ≤
q
n
µ.
Proof. Let Lx denote the Laplacian of Gx. We have:
A(x)A(x)T =
X
u∈[n]
X
v∈Γ(u)
(|u⟩−|v⟩)(⟨u| −⟨v|) = 2
X
u∈[n]
du|u⟩⟨u| −2
X
u∈[n]
X
v∈Γ(u)
|u⟩⟨v| = 2Lx.
Thus, if L denotes the Laplacian of the complete graph, we also have AAT = 2L.
Letting J
denote the all ones matrix, we have L = (n −1)I −(J −I) = nI −J, and since J = n|u⟩⟨u| where
|u⟩=
1
√n
Pn
i=1 |i⟩, if |u1⟩, . . . , |un−1⟩, |u⟩is any orthonormal basis of Rn, then L = n Pn−1
i=1 |ui⟩⟨ui|+
n|u⟩⟨u| −n|u⟩⟨u| = Pn−1
i=1 n|ui⟩⟨ui|, so the spectrum of L is 0, with multiplicity 1, and n with
23


---- page 24 ----

s
t
Figure 1: The graphs in G0 contain only the solid edges. The graphs in G1 contain the solid edges
and one of the dashed edges. We can embed an instance of OR in the dashed edges. If one of the
dashed edges is included, the number of st-paths increases to 2, decreasing the eﬀective resistance.
multiplicity n−1. Thus, the only nonzero singular value of A is
√
2n = σmax(A). Furthermore, since
λ2(Gx) is the smallest nonzero eigenvalue of Lx, and A(x)A(x)T = 2Lx, σmin(A(x)) =
p
2λ2(Gx).
The result follows.
Finally, by Lemma 4.1, we have w+(x, P) = 1
2Rs,t(Gx), so, applying Theorem 3.12, we get an
algorithm that makes eO

κ(f)
ε
q
w+(x,P )
N

= eO

1
ε
p
n/µpRs,tn

calls to U ′(P, x). By Theorem B.1,
this algorithm has time complexity eO
  1
εn
p
Rs,t/µ

and space complexity O(log n).
Both of our upper bounds have linear dependence on n, and the following theorem shows that
this is optimal.
Theorem 4.6 (Lower Bound). There exists a family of graphs G such that estimating eﬀective
resistance on G costs at least Ω(n) queries.
Proof. Let G0 be the set of graphs consisting of two stars K1,n/2−1, centered at s and t, with an
edge connecting s and t (see Figure 1). Let G1 be the set of graphs consisting of graphs from G0
with a single edge added between two degree one vertices from diﬀerent stars. Let G = G0 ∪G1.
We ﬁrst note that we can distinguish between G0 and G1 by estimating eﬀective resistance on G
to accuracy
1
10: If G ∈G0, then there is a single st-path, consisting of one edge, so the eﬀective
resistance is 1. If G ∈G1, then there are two st-paths, one of length 1 and one of length 3. We
put a ﬂow of 1
4 on the length-3 path and 3
4 on the length-1 path to get eﬀective resistance at most
(3/4)2 + 3(1/4)2 = 3
4.
We now describe how to embed an instance y ∈{0, 1}(n/2−1)2 of OR(n/2−1)2 in a graph. We
let s = 1 be connected to every vertex in {2, . . . , n/2}, and t = n be connected to every vertex in
{n/2+ 1, . . . , n −1}. Let the values of {Gi,j : i ∈{2, . . . , n/2}, j ∈{n/2, . . . , n −1}} be determined
by y. Let all other values Gi,j be 0. Then clearly Rs,t(G) ≥1 if and only if y = 0 . . . 0 (in that case
G ∈G0) and otherwise, Rs,t(G) ≤3/4, since there is at least one extra path from s to t (in that case
G ∈G1). The result follows from the lower bound of Ω(
p
(n/2 −1)2) = Ω(n) on OR(n/2−1)2.
Discussion
The algorithms from Theorem 4.2 and 4.3 are the ﬁrst quantum algorithms for es-
timating the eﬀective resistance in the adjacency model, however, the problem has been studied
previously in the edge-list model [Wan13], where Wang obtains a quantum algorithm with com-
plexity eO

d3/2 log n
Φ(G)2ε

, where Φ(G) ≤1 is the conductance (or edge-expansion) of G. In the edge-list
model, the input x ∈[n][n]×[d] models a d-regular graph (or d-bounded degree graph) Gx by xu,i = v
for some i ∈[d] whenever {u, v} ∈E(Gx). Wang requires edge-list queries to simulate walking on
the graph, which requires constructing a superposition over all neighbours of a given vertex. This
type of edge-list query can be simulated by
p
n/d adjacency queries to a d-regular graph, using
quantum search, so Wang’s algorithm can be converted to an algorithm in the adjacency query
model with cost eO

d3/2
Φ(G)2ε
p n
d

. We can compare our results to this by noticing that Rs,t ≤
1
λ2(G)
24


---- page 25 ----

[CRR+96], implying that our algorithm always runs in time at most eO

1
ε
n
µ

.
If G is a con-
nected d-regular graph, then λ2(G) = dδ(G), where δ(G) is the spectral gap of a random walk
on G.
By Cheeger inequalities, we have Φ2
2
≤δ [LPW09], so the complexity of the algorithm
from Theorem 4.3 is at most eO
  1
ε
n
dδ

= eO
  1
ε
n
dΦ2

, which is an improvement over the bound of
eO

1
ε
d3/2
Φ2
p n
d

= eO
  1
ε
d
Φ2
√n

given by naively adapting Wang’s algorithm to the adjacency model
whenever d >
4√n. In general our upper bound may be much better than 1
ε
n
dΦ2 , since the Cheeger
inequality is not tight, and Rs,t can be much smaller than
1
λ2 .
It is worth further discussing Wang’s algorithms for estimating eﬀective resistance, due to
their relationship with the ideas presented here.
In order to get a time-eﬃcient algorithm for
st-connectivity, Belovs and Reichardt show how to eﬃciently reﬂect about the kernel of A (see
also Appendix B), A being related to the Laplacian of a complete graph, L, by AAT = 2L. This
implementation consists, in part, of a quantum walk on the complete graph. Wang’s algorithm
directly implements a reﬂection about the kernel of A(x) by instead using a quantum walk on the
graph G, which can be done eﬃciently in the edge-list model. For general span programs, when
a reﬂection about the kernel of A(x) can be implemented eﬃciently in such a direct way, this can
lead to an eﬃcient quantum algorithm for estimating the witness size.
We also remark on another quantum algorithm for estimating eﬀective resistance, also from
[Wan13]. This algorithm has the worse complexity eO

d8polylogn
Φ(G)10ε2

, and is obtained by using the HHL
algorithm [HHL09] to estimate ∥A(x)+|τ⟩∥2, which is the positive witness size of x, or in this case,
the eﬀective resistance. We remark that, for any span program, w+(x) = ∥|wx⟩∥2 = ∥A(x)+|τ⟩∥2,
so HHL may be another means of estimating the positive witness size. There are several caveats:
A(x) must be eﬃciently row-computable, and the complexity additionally depends on σmax(A(x))
σmin(A(x)) ,
the condition number of A(x) (We remark that this is upper bounded by
σmax(A)
σmin(A(x)), upon which
the complexity of some of our algorithms depends as well). However, if this approach yields an
eﬃcient algorithm, it is eﬃcient in time complexity, not only query complexity. We leave further
exploration of this idea for future research.
5
Conclusion and Open Problems
Summary
We have presented several new techniques for turning span programs into quantum
algorithms, which we hope will have future applications. Speciﬁcally, given a span program P, in
addition to algorithms for deciding any function f such that f −1(0) ⊆P0 and f −1(1) ⊆P1, we also
show how to get several diﬀerent algorithms for deciding a number of related threshold problems,
as well as estimating the witness size. In addition to algorithms based on the standard eﬀective
spectral gap lemma, we also show how to get algorithms by analyzing the real phase gap.
We hope that the importance of this work lies not only in its potential for applications, but
in the improved understanding of the structure and power of span programs. A number of very
important quantum algorithms rely on a similar structure, using phase estimation of a unitary
that depends on the input to distinguish between diﬀerent types of inputs. Span-program-based
algorithms represent a very general class of such algorithms, making them not only important to
the study of the quantum query model, but to quantum algorithms in general.
Further Applications
The main avenue for future work is in applications of our techniques to
obtain new quantum algorithms. We stress that any span program for a decision problem can now
be turned into an algorithm for estimating the positive or negative witness size, if these correspond
25


---- page 26 ----

to some meaningful function, or deciding threshold functions related to the witness size. A natural
source of potential future applications is in the rich area of property testing problems (for a survey,
see [MdW13]).
Span Programs and HHL
One ﬁnal open problem, brieﬂy discussed at the end of the previous
section, is the relationship between estimating the witness size and the HHL algorithm [HHL09].
The HHL algorithm can be used to estimate ∥M+|u⟩∥2, given the state |u⟩and access to a row-
computable linear operator M. When M = A(x), this quantity is exactly w+(x), so if A(x) is
row-computable — that is, there is an eﬃcient procedure for computing the ith nonzero entry of
the jth row of A(x), then HHL gives us yet another means of estimating the witness size, whose
time complexity is known, rather than only its query complexity. It may be interesting to explore
this connection further.
6
Acknowledgements
The authors would like to thank David Gosset, Shelby Kimmel, Ben Reichardt, and Guoming Wang
for useful discussions about span programs. We would especially like to thank Shelby Kimmel for
valuable feedback and suggestions on an earlier draft of this paper. Finally, S.J. would like to thank
Moritz Ernst for acting as a sounding board throughout the writing of this paper.
References
[BBBV97]
C. H. Bennett, E. Bernstein, G. Brassard, and U. Vazirani. Strengths and weaknesses of quantum
computing. SIAM Journal on Computing (special issue on quantum computing), 26:1510–1523,
1997. arXiv:quant-ph/9701001v1.
[BBC+01]
R. Beals, H. Buhrman, R. Cleve, M. Mosca, and R. de Wolf. Quantum lower bounds by poly-
nomials. Journal of the ACM, 48, 2001.
[BCJ+13]
A. Belovs, A. M. Childs, S. Jeﬀery, R. Kothari, and F. Magniez. Time eﬃcient quantum walks
for 3-distinctness. In Proceedings of the 40th International Colloquium on Automata, Languages
and Programming (ICALP 2013), pages 105–122, 2013.
[Bel12a]
A. Belovs. Learning-graph-based quantum algorithm for k-distinctness. In Prooceedings of the
53rd Annual IEEE Symposium on Foundations of Computer Science (FOCS 2012), pages 207–
216, 2012.
[Bel12b]
A. Belovs. Span programs for functions with constant-sized 1-certiﬁcates. In Proceedings of the
44th Symposium on Theory of Computing (STOC 2012), pages 77–84, 2012.
[BHMT02] G. Brassard, P. Høyer, M. Mosca, and A. Tapp. Quantum amplitude ampliﬁcation and esti-
mation. In S. J. Lomonaca and H. E. Brandt, editors, Quantum Computation and Quantum
Information: A Millennium Volume, volume 305 of AMS Contemporary Mathematics Series
Millennium Volume, pages 53–74. AMS, 2002. arXiv:quant-ph/0005055v1.
[BR12]
A. Belovs and B. Reichardt. Span programs and quantum algorithms for st-connectivity and
claw detection. In Proceedings of the 20th European Symposium on Algorithms (ESA 2012),
pages 193–204, 2012.
[CEMM98] R. Cleve, A. Ekert, C. Macchiavello, and M. Mosca. Quantum algorithms revisited. Proceedings
of the Royal Society A: Mathematical, Physical and Engineering Sciences, 454(1969):339–354,
1998.
[CRR+96]
A. K. Chandra, P. Raghavan, W. L. Ruzzo, R. Smolensky, and P. Tiwari. The electrical resistance
of a graph captures its commute and cover times. Computational Complexity, 6(4):312–340, 1996.
26


---- page 27 ----

[DS84]
P. G. Doyle and J. L. Snell. Random Walks and Electrical Networks, volume 22 of The Carus
Mathematical Monographs. The Mathematical Association of America, 1984.
[Gro96]
L. K. Grover. A fast quantum mechanical algorithm for database search. In Proceedings of the
28th ACM Symposium on Theory of Computing (STOC 1996), pages 212–219, 1996.
[HHL09]
A. W. Harrow, A. Hassidim, and S. Lloyd. Quantum algorithm for linear systems of equations.
Phys. Rev. Lett., 103:150502, Oct 2009.
[Jef14]
S. Jeﬀery. Frameworks for Quantum Algorithms. PhD thesis, University of Waterloo, 2014.
Available at http://uwspace.uwaterloo.ca/handle/10012/8710.
[Kit95]
A.
Kitaev.
Quantum
measurements
and
the
Abelian
stabilizer
problem,
1995.
arXiv:quant-ph/9511026.
[KW93]
M. Karchmer and A. Wigderson. On span programs. In Proceedings of the IEEE 8th Annual
Conference on Structure in Complexity Theory, pages 102–111, 1993.
[LMR+11]
T. Lee, R. Mittal, B. Reichardt, R. ˇSpalek, and M. Szegedy. Quantum query complexity of state
conversion. In Proceedings of the 52nd Annual IEEE Symposium on Foundations of Computer
Science (FOCS 2011), pages 344–353, 2011.
[LPW09]
D. A. Levin, Y. Peres, and E. L. Wilmer. Markov Chains and Mixing Times. American Mathe-
matical Society, 2009.
[MdW13]
A. Montanaro and R. de Wolf. A survey of quantum property testing, 2013. arXiv:1310.2035.
[Rei09]
B. Reichardt. Span programs and quantum query complexity: The general adversary bound is
nearly tight for every Boolean function. In Proceedings of the 50th IEEE Symposium on Foun-
dations of Computer Science (FOCS 2009), pages 544–551, 2009. arXiv:quant-ph/0904.2759.
[Rei11]
B. Reichardt. Reﬂections for quantum query algorithms. In Proceedings of the 22nd ACM-SIAM
Symposium on Discrete Algorithms (SODA 2011), pages 560–569, 2011.
[RˇS12]
B. Reichardt and R. ˇSpalek. Span-program-based quantum algorithm for evaluating formulas.
Theory of Computing, 8(13):291–319, 2012.
[Sze04]
M. Szegedy. Quantum speed-up of Markov chain based algorithms. In Proceedings of the 45th
Annual IEEE Symposium on Foundations of Computer Science (FOCS 2004), pages 32–41, 2004.
[Wan13]
G. Wang. Quantum algorithms for approximating the eﬀective resistances in electrical networks,
2013. arXiv:1311.1851.
A
Span Program Scaling
In this section we prove Theorem 2.14. Let P = (H, V, τ, A) be any span program on [q]n, and
let N = ∥|w0⟩∥2 for |w0⟩the optimal positive witness of P. We deﬁne P β = (Hβ, Aβ, τ β, V β) as
follows. Let |ˆ0⟩and |ˆ1⟩be two vectors orthogonal to H and V . We deﬁne:
∀j ∈[n], a ∈[q], Hβ
j,a = Hj,a,
Hβ
true = Htrue ⊕span{|ˆ1⟩},
Hβ
false = Hfalse ⊕span{|ˆ0⟩}
V β = V ⊕span{|ˆ1⟩},
Aβ = βA + τ|ˆ0⟩+
p
β2 + N
β
|ˆ1⟩⟨ˆ1|,
τ β = τ + |ˆ1⟩
We then have and Hβ = H ⊕span{|ˆ0⟩, |ˆ1⟩} and Hβ(x) = H(x) ⊕span{|ˆ1⟩}. In order to prove
Theorem 2.14, we will show that:
• For all x ∈P1, w+(x, P β) =
1
β2w+(x, P) +
β2
N+β2 and ˜w−(x, P β) ≤β2 ˜w−(x, P) + 2;
• for all x ∈P0, w−(x, P β) = β2w−(x, P) + 1 and ˜w+(x, P β) ≤
1
β2 ˜w+(x, P) + 2;
27


---- page 28 ----

• the smallest witness in P β is |wβ
0 ⟩=
β
β2+N |w0⟩+
N
β2+N |ˆ0⟩+
β
√
β2+N |ˆ1⟩, and
|wβ
0 ⟩

2
= 1.
Lemma A.1. The smallest witness in P β is |wβ
0 ⟩=
β
β2+N |w0⟩+
N
β2+N |ˆ0⟩+
β
√
β2+N |ˆ1⟩. It is easily
veriﬁed that
|wβ
0 ⟩

2
= 1.
Proof. Let |w′
0⟩= |h⟩+ b|ˆ0⟩+ c|ˆ1⟩be the smallest witness in P β, for some |h⟩∈H.
Since
Aβ|w′
0⟩= βA|h⟩+ bτ + c
√
β2+N
β
|ˆ1⟩= τ + |ˆ1⟩, we must have c =
β
√
β2+N and A|h⟩= 1−b
β τ, so
|h⟩= 1−b
β |w⟩for some positive witness |w⟩of P. We have:
|w′
0⟩
2 = (1 −b)2
β2
∥|w⟩∥2 + b2 +
β2
β2 + N .
This is minimized by taking |w⟩= |w0⟩, the smallest witness of P, and setting b =
N
β2+N , giving:
|wβ
0 ⟩=
β
β2 + N |w0⟩+
N
β2 + N |ˆ0⟩+
β
p
β2 + N
|ˆ1⟩.
Lemma A.2. For all x ∈P1, w+(x, P β) =
1
β2 w+(x, P) +
β2
N+β2 and ˜w−(x, P β) ≤β2 ˜w−(x, P) + 2.
Proof. The proof is similar to that of Lemma A.1, however, we have Hβ(x) = H(x) ⊕span{|ˆ1⟩},
so a positive witness for x has the form |w′
x⟩= |h⟩+
β
√
β2+N |ˆ1⟩with β|h⟩some witness for x in P.
Clearly ∥|w′
x⟩∥is minimized by setting |h⟩= 1
β|wx⟩for |wx⟩the minimal positive witness for x in
P, so we have w+(x, P β) =
1
β2 w+(x, P) +
β2
β2+N , as required.
Let ˜ω be an optimal min-error witness for x in P, and deﬁne
˜ω′ =
(β2 + N)w+(x, P)
β4 + (β2 + N)w+(x, P) ˜ω +
β4
β4 + (β2 + N)w+(x, P)⟨ˆ1|.
We have ˜ω′(τ + |ˆ1⟩) =
(β2 + N)w+(x, P)
β4 + (β2 + N)w+(x, P) ˜ω(τ) +
β4
β4 + (β2 + N)w+(x, P) = 1, and:
˜ω′AβΠHβ(x)

2
=

(β2 + N)w+(x, P)
β4 + (β2 + N)w+(x, P) ˜ωβAΠH(x)

2
+

β4
β4 + (β2 + N)w+(x, P)
p
β2 + N
β
⟨ˆ1|

2
=
(β2 + N)2w+(x, P)2β2
(β4 + (β2 + N)w+(x, P))2
1
w+(x, P) +
β8
(β4 + (β2 + N)w+(x, P))2
β2 + N
β2
= (β2 + N)2w+(x, P)β2 + β6(β2 + N)
(β4 + (β2 + N)w+(x, P))2
=
β2(β2 + N)
β4 + (β2 + N)w+(x, P) =
1
w+(x, P β)
so ˜ω′ is a min-error witness for x in P β. Thus, letting ε =
(β2+N)w+(x,P )
β4+(β2+N)w+(x,P ), we have
˜w−(x, P β)
≤
˜ω′Aβ
2
=
ε˜ωβA + ε˜ω(τ)⟨ˆ0| +
p
β2 + N
β
˜ω′(ˆ1)⟨ˆ1|

2
≤
β2 ∥˜ωA∥2 + 1 + β2 + N
β2
β8
(β4 + (β2 + N)w+(x, P))2
≤
β2 ˜w−(x, P) + 1 +
β6(β2 + N)
(β4 + β2w+(x, P))2 ≤β2 ˜w+(x, P) + 2,
where in the last line, we use the fact that w+(x, P) ≥N.
28


---- page 29 ----

Lemma A.3. For all x ∈P0, w−(x, P β) = β2w−(x, P) + 1, and ˜w+(x, P β) ≤
1
β2 ˜w+(x, P) + 2.
Proof. Let ω′
x be an optimal negative witness for x in P β. Since ω′
xΠHβ(x) = 0, ω′
x|ˆ1⟩= 0, so
ω′
x(τ β) = ω′
x(τ) + ω′
x(|ˆ1⟩) = ω′
x(τ) = 1. Furthermore, ω′
x minimizes
ω′
xAβ
2
=
βω′
xA + ω′
x(τ)|ˆ0⟩
2 = β2 ω′
xA
2 + 1.
This is minimized by taking ω′
x|V to be the minimal negative witness of x in P, so ∥ω′
xA∥2 =
w−(x, P), and thus w−(x, P β) = β2w−(x, P) + 1.
Next, let | ˜w⟩be an optimal min-error positive witness for x in P. Deﬁne:
| ˜w′⟩:=
βw−(x, P)
1 + β2w−(x, P)| ˜w⟩+
1
1 + β2w−(x, P)|ˆ0⟩+
β
p
β2 + N
|ˆ1⟩.
We have:
A| ˜w′⟩=
β2w−(x, P)
1 + β2w−(x, P)τ +
1
1 + β2w−(x, P)τ + |ˆ1⟩= τ + |ˆ1⟩= τ β,
and since Hβ(x)⊥= H(x)⊥⊕span{|ˆ0⟩}:
ΠHβ(x)⊥| ˜w′⟩

2
=
ΠH(x)⊥| ˜w′⟩

2
+
Π|ˆ0⟩| ˜w′⟩

2
=
β2w−(x, P)2
(1 + β2w−(x, P))2
ΠH(x)⊥| ˜w⟩

2
+
1
(1 + β2w−(x, P))2
=
β2w−(x, P)2
(1 + β2w−(x, P))2
1
w−(x, P) +
1
(1 + β2w−(x, P))2
=
1
1 + β2w−(x, P)
=
1
w−(x, P β),
so | ˜w′⟩has minimal error. Thus:
˜w+(x, P β)
≤
| ˜w′⟩
2
=
β2w−(x, P)2
(1 + β2w−(x, P))2 ∥| ˜w⟩∥2 +
1
(1 + β2w−(x, P))2 +
β2
β2 + N
≤
β2w−(x, P)2 ˜w+(x, P)
(1 + β2w−(x, P))2
+ 2
≤
β2w−(x, P)2 ˜w+(x, P)
β4w−(x, P)2
+ 2
=
˜w+(x, P)
β2
+ 2.
B
Time Complexity Analysis
In [BR12], the authors analyze the time complexity of the reﬂections needed to implement their
span program to give a time upper bound on st-connectivity. Since our algorithms look superﬁcially
diﬀerent from theirs, we reproduce their analysis here to show an upper bound on the quantum
time complexity of estimating eﬀective resistance.
Theorem B.1. Let P be the span program for st-connectivity given in Section 4. Then for any β
such that 1/nO(1) ≤β ≤nO(1), U ′(P β, x) can be implemented in quantum time complexity O(log n)
and space O(log n), and |wβ
0 ⟩can be constructed in quantum time complexity O(log n).
29


---- page 30 ----

Proof. In order to implement U ′(P β, x), we must implement the reﬂections Rx(β) = 2ΠHβ(x) −I
and R′
P (β) = 2Πker Aβ⊕span{|wβ
0 ⟩} −I. We remark that Rx(β) is easily implemented in a single query
and constant overhead. This proof deals with the implementation of R′
P (β), which can be easily
implemented given an implementation of RP = 2Πker A −I.
In order to implement RP, we describe a unitary W = (2ΠZ −I)(2ΠY −I) that can be eﬃciently
implemented, and such that W can be used to implement RP . In order to show that W implements
RP , we need to show that some isometry MY : H →Y maps ker A to the −1-eigenspace of W,
and (ker A)⊥to the 1-eigenspace of W. This allows us to implement RP by ﬁrst implementing the
isometry MY , applying W, and then uncomputing MY .
Deﬁne the spaces Z and Y as follows:
Z = span


|zu⟩:=
1
p
2(n −1)
X
v̸=u
|0, u, u, v⟩+
1
p
2(n −1)
X
v̸=u
|1, u, v, u⟩: u ∈[n]


;
and
Y = span
n
|yu,v⟩:= (|0, u, u, v⟩−|1, v, u, v⟩) /
√
2 : u, v ∈[n], u ̸= v
o
.
Deﬁne isometries
MZ =
X
u∈[n]
|zu⟩⟨u|
and
MY =
X
(u,v)∈[n]2:u̸=v
|yu,v⟩⟨u, v|.
Lemma B.2. Let S = {MY |ψ⟩: |ψ⟩∈ker A} and S′ = {MY |ψ⟩: |ψ⟩∈(ker A)⊥} be the images
of ker A and (ker A)⊥respectively under the isometry MY . Then S = Y ∩Z⊥, which is exactly the
intersection of Y and the −1-eigenspace of W, and S′ = Y ∩Z, which is exactly the intersection
of Y and the 1-eigenspace of W.
Proof. We have:
M†
ZMY
=
1
2√n −1
X
u∈[n]
X
v̸=u
|u⟩(⟨0, u, u, v| + ⟨1, u, v, u|)
X
a,b∈[n]:a̸=b
(|0, a, a, b⟩−|1, b, a, b⟩)⟨a, b|
=
1
2√n −1
X
u∈[n]
X
v̸=u
|u⟩⟨u, v| −
1
2√n −1
X
u∈[n]
X
v̸=u
|v⟩⟨u, v| =
1
2√n −1A.
Thus, for all |ψ⟩∈ker A, MY |ψ⟩∈Y ∩ker M†
Z = Y ∩Z⊥, so S ⊆Y ∩Z⊥. On the other hand, if
|ψ⟩∈(ker A)⊥, then MY |ψ⟩∈Y ∩(ker M†
Z)⊥= Y ∩Z. By Theorem 1.10, the −1-eigenspace of W
is exactly (Y ∩Z⊥) ⊕(Y ⊥∩Z) and the 1-eigenspace of W is exactly (Y ∩Z) ⊕(Y ⊥∩Z⊥).
Lemma B.3. MY , RZ = 2ΠZ −I and RY = 2ΠY −I can be implemented in time O(log n).
Proof. To implement RZ and RY , we need only show how to implement the unitary versions of MZ
and MY . We begin with MZ. For any u ∈[n], we can map |u⟩7→|0, u, u, 0⟩by initializing three
new registers and copying u into one of them. Then we map:
|0, u, u, 0⟩7→|0, u, u⟩
1
√n −1
X
v̸=u
|v⟩H⊗I⊗3
7→
1
p
2(n −1)

|0, u, u⟩
X
v̸=u
|v⟩+ |1, u, u⟩
X
v̸=u
|v⟩

7→|xu⟩,
where the last transformation is achieved by swapping the last two registers conditioned on the
ﬁrst. This can be implemented in O(log n) elementary gates.
30


---- page 31 ----

For MY , we start by mapping any edge |u, v⟩to |1, 0, u, v⟩, followed by:
|1, 0, u, v⟩H⊗I⊗3
7→
1
√
2
(|0, 0, u, v⟩−|1, 0, u, v⟩) 7→
1
√
2
(|0, u, u, v⟩−|1, v, u, v⟩) = |yu,v⟩,
where in the last step we copy either u or v into the second register depending on the value of the
ﬁrst register. This can be implemented in O(1) elementary gates.
Then in order to implement RZ, we simply apply M†
Z, reﬂect about span{|0, u, u, 0⟩: u ∈[n]},
and then apply MZ again. To implement RY , we apply M†
Y , reﬂect about span{|1, 0, u, v⟩: u, v ∈
[n], u ̸= v}, and then apply MY .
We now show how to eﬃciently implement the span program P β when 1/nO(1) ≤β ≤nO(1).
First, consider |w0⟩, the minimal positive witness for P. Since |w0⟩corresponds to an optimal
st-ﬂow in the complete graph, it is easy to compute that
|w0⟩= 1
n|s, t⟩+ 1
2n
X
u∈[n]\{s,t}
(|s, u⟩+ |u, t⟩) −1
n|t, s⟩−1
2n
X
u∈[n]
(|t, u⟩+ |u, s⟩),
and ∥|w0⟩∥2 = 1
n (see also Lemma 4.4). We can construct this state by mapping |s, 0⟩+ |0, t⟩7→
P
u̸=s |s, u⟩+ P
u̸=t |u, t⟩and then performing a swap controlled on an additional register in the
state
1
√
2(|0⟩+ |1⟩). The initial state of the scaled span program P β is (see Theorem 2.14):
|wβ
0 ⟩=
β
β2 + 1
n
|w0⟩+
1
n
β2 + 1
n
|ˆ0⟩+
β
q
β2 + 1
n
|ˆ1⟩,
which we can also construct eﬃciently, as follows:
|ˆ0⟩7→
β√n
β2 + 1
n
|ˆ2⟩+
1
nβ2 + 1|ˆ0⟩+
β
q
β2 + 1
n
|ˆ1⟩7→
β
β2 + 1
n
|w0⟩+
1
n
β2 + 1
n
|ˆ0⟩+
β
q
β2 + 1
n
|ˆ1⟩.
The ﬁrst step is accomplished by a pair of rotations using O(log n
β) elementary gates, and the
second is accomplished by mapping |ˆ2⟩to
|w0⟩
∥|w0⟩∥= √n|w0⟩, which can be accomplished in O(log n)
elementary gates.
Next, we have Aβ = βA + (|s⟩−|t⟩)⟨ˆ0| +
√
β2+ n
2
β
|ˆ1⟩⟨ˆ1|, so
ker Aβ ⊕span{|wβ
0 ⟩} = ker A ⊕span{|ˆ0⟩−1
β |w0⟩} ⊕span{|wβ
0 ⟩}.
We know how to reﬂect about ker A, and since we can eﬃciently construct |wβ
0 ⟩, we can reﬂect
about it, so we need only consider how to reﬂect about span{|ˆ0⟩−1
β|w0⟩}. Since we can compute
|w0⟩eﬃciently, we can compute:
|ˆ0⟩7→
β
p
β2 + 1
|ˆ0⟩+
1
p
β2 + 1
|ˆ1⟩7→
β
p
β2 + 1
|ˆ0⟩+
1
p
β2 + 1
| ¯w0⟩.
The ﬁrst step is a rotation, which can be performed in O(log 1
β) elementary gates, and the second
step is some mapping that maps |ˆ1⟩to |w0⟩, which we know can be done in O(log n) elementary
gates. Thus, the total cost to reﬂect about ker Aβ is O(log n).
31

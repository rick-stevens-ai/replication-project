# Extraction Provenance

This project's Marker/Nougat pipelines were not available on the current host
(no `marker_single`/`nougat` in $PATH; no central CORPUS-PARSED cache found).
As a substitute we use a `pdftotext`-based plain-text extraction of the same
paper.pdf. Sections below preserve the paper's structure to remain usable for
downstream corpus tooling. Original PDF: paper.pdf (arXiv:1509.02374, 23 pp,
480 KB, produced by pdfTeX-1.40.12, CreationDate 2016-01-04).

Provenance:
  tool     : Poppler pdftotext
  version  : (bundled with local Poppler on macOS)
  command  : pdftotext work/paper.pdf work/paper.txt
  fallback : Marker/Nougat unavailable at replication time

---

Quantum walk speedup of backtracking algorithms
Ashley Montanaro∗

arXiv:1509.02374v2 [quant-ph] 4 Jan 2016

January 5, 2016

Abstract
We describe a general method to obtain quantum speedups of classical algorithms which are
based on the technique of backtracking, a standard approach for solving constraint satisfaction
problems (CSPs). Backtracking algorithms explore a tree whose vertices are partial solutions
to a CSP in an attempt to find a complete solution. Assume there is a classical backtracking
algorithm which finds a solution to a CSP on n variables, or outputs that none exists, and
whose corresponding tree contains T vertices, each vertex corresponding to a test of a partial
solution. Then we show
√ that there is a bounded-error quantum algorithm which completes the
same task using O( T n3/2 log n) tests. In particular, this quantum algorithm can be used to
speed up the DPLL algorithm, which is the basis of many of the most efficient SAT solvers used
in practice. The quantum algorithm is based on the use of a quantum walk algorithm of Belovs
to search in the backtracking tree. We also discuss how, for certain distributions on the inputs,
the algorithm can lead to an exponential reduction in expected runtime.

1

Introduction

Grover’s quantum search algorithm [34] is one of the great success stories of quantum computation.
One important domain to which the algorithm can be applied is the solution of constraint satisfaction problems (CSPs). Consider a constraint satisfaction problem (CSP) expressed as a predicate
P : [d]n → {true, false}, where [d] = {0, . . . , d − 1}. We would like to find an assignment x to
the n variables such that P (x) is true, or output “not found” if no such x exists. This framework
encompasses many important problems√such as boolean satisfiability and graph colouring. Grover’s
algorithm solves such a CSP using O( dn ) evaluations of P , whereas with no further information
about P , finding an x such that P (x) is true requires Ω(dn ) evaluations classically in the worst
case. However, when we are faced with an instance of a CSP in practice, we usually have some
additional information about its structure. For example, P may be defined as the conjunction of
smaller constraints of a particular type, as in the case of graph colouring. This information often
allows classical algorithms to solve the CSP significantly more efficiently than the above bound
would suggest, throwing some doubt on whether straightforward use of Grover’s algorithm will
really be used to solve CSPs in practice.
One of the most important and most general classical tools to take advantage of problem
structure, both in theory and in practice, is backtracking [7]. This technique can be used when
we have the ability to recognise whether partial solutions to a problem can be extended to full
solutions. We assume that the predicate P allows us to pass it a partial assignment x of the form
x : S → [d], where S ⊆ {1, . . . , n}, which specifies the values assigned to the variables in the set
∗

School of Mathematics, University of Bristol, UK; ashley.montanaro@bristol.ac.uk.

1

Assume that we are given access to a predicate P : D → {true, false, indeterminate}, and a
heuristic h : D → {1, . . . , n} which returns the next index to branch on from a given partial
assignment.
Return bt(∗n ), where bt is the following recursive procedure:
bt(x):
1. If P (x) is true, output x and return.
2. If P (x) is false, or x is a complete assignment, return.
3. Set j = h(x).
4. For each w ∈ [d]:
(a) Set y to x with the j’th entry replaced with w.
(b) Call bt(y).
Algorithm 1: General classical backtracking algorithm

S. We can equivalently think of x as an element of D := ([d] ∪ {∗})n , where the ∗’s represent the
positions which are as yet unassigned values. We say that x is complete if it contains no ∗’s. Then
P returns “true” if x is a solution to P , “false” if it is clear that x cannot be extended to a solution
to P , and “indeterminate” otherwise. We say that a partial assignment x is valid if P (x) is true or
indeterminate, and invalid if P (x) is false.
Algorithm 1 above describes a generic way to use this information classically. The algorithm
assumes access to P and a heuristic h(x) which determines how to extend a given partial assignment
x. We think of P and h as black boxes (“oracles”). The basic idea is to fail early: if we know that a
partial assignment cannot be extended to a solution, we should give up on it and try a different one.
We can think of the algorithm as exploring a tree, whose internal vertices are partial solutions to
P , and whose leaves are solutions to P or certificates that the partial solution cannot be extended
to a complete solution. This tree is of size at most O(dn ), but for some problem instances could be
substantially smaller.
A canonical example of a powerful backtracking algorithm which fits into the framework of
Algorithm 1 is the DPLL (Davis-Putnam-Logemann-Loveland) algorithm [24, 23] for k-SAT. This
algorithm forms the basis of many of the most successful SAT solvers used in practice [25, 41, 32].
For many practically relevant problem instances, the algorithm runs more quickly than worst-case
upper bounds would suggest. Another appealing aspect of this algorithm is that, unlike “local
search” methods based on random walks or similar ideas, it can sometimes produce efficient proofs
of unsatisfiability, corresponding to small backtracking trees.
Algorithm 1 outputs all solutions x such that P (x) is true. While in practice the algorithm
might be modified to terminate when the first solution is found, here we will assume throughout
that the entire tree is explored. We assume that P and h can both be evaluated in time poly(n), so
the most important contribution to the complexity of Algorithm 1 is usually the number of vertices
in the tree, which can often be exponential in n. To simplify the complexity bounds, we also assume
throughout that d = O(1); this is effectively without loss of generality as any predicate with local
domain size d can be replaced with one which uses O(log d) bits to encode each variable.

2

1.1

Results

We show here that there is a quantum equivalent of Algorithm 1 which can be substantially faster:
Theorem 1. Let T be an upper bound on the number of vertices in the tree explored by Algorithm
1. √Then for any 0 < δ < 1 there is a quantum algorithm which, given T , evaluates P and h
O( T n log(1/δ)) times each, outputs true if there exists x such that P (x) is true, and outputs false
otherwise. The algorithm uses poly(n) space, O(1) auxiliary operations per use of P and h, and
fails with probability at most δ.
We usually think of T as being exponential in n; in this regime this complexity is a nearquadratic speedup over the classical algorithm. The algorithm can be modified to find a solution,
rather than just detect the existence of one, with a small runtime penalty:
Theorem 2. Let T be the number of vertices in the tree explored by√Algorithm 1. Then for any
0 < δ < 1 there is a quantum algorithm which evaluates P and h O( T n3/2 log n log(1/δ)) times
each, and outputs x such that P (x) is true, or “not found” if no such x exists. If we are promised
that there exists a √
unique x0 such that P (x0 ) is true, there is a quantum algorithm which outputs x0
using P and h O( T n log3 n log(1/δ)) times each. In both cases the algorithm uses poly(n) space,
O(1) auxiliary operations per use of P and h, and fails with probability at most δ.
We stress that these results can be applied to any backtracking algorithm which fits into the
framework of Algorithm 1, whatever the predicate P or the choice of the heuristic h. In particular,
they can be applied to the DPLL algorithm with the commonly used “unit clause” heuristic.
Theorems 1 and 2 can also be applied to backtracking algorithms which make use of randomness
in the heuristic h, by interpreting these algorithms as first fixing a random seed, then using this
seed as input to a deterministic heuristic h. Observe that the runtime bound of Theorem 2 is
instance-dependent and, to use it, we do not need to know an upper bound on the runtime T of the
underlying classical backtracking algorithm. For instances on which the classical algorithm runs
quickly, the quantum algorithm also runs quickly.
These algorithms can be leveraged to obtain an exponential separation between average quantum
and classical runtimes. The speedup for any given instance is approximately quadratic. However,
given the right distribution on the input instances, this can be amplified to an exponential separation. This is discussed further in Section 4.

1.2

Techniques

The algorithms which achieve the bounds of Theorems 1 and 2 are based on the use of a discretetime quantum walk to find a marked vertex within the tree produced by the classical backtracking
algorithm, corresponding to a partial solution x such that P (x) is true. Quantum walks have
become a basic tool in quantum algorithm design [16, 2, 51, 43]. In particular, they have been
applied in several contexts to solve search problems on graphs [49, 51, 43, 39], sometimes achieving
up to a quadratic speedup over classical algorithms. However, in prior work it is usually assumed
that the input graph is known in advance, and moreover that the initial state of the quantum
walk is the stationary distribution of the corresponding random walk. Aaronson and Ambainis [1]
described a different approach to spatial search on graphs; this does not use a quantum walk, but
also assumes the input graph is known in advance.
Here we would like to use quantum walks in a context where the input graph is defined implicitly
by the backtracking algorithm and hence is not known in advance, and where the walk starts at
3

the root of the tree. One of the few cases where such walks have been studied is beautiful work
of Belovs [8, 9]. The main result of that work relates the complexity of detecting a marked vertex
by quantum walk on a graph to the effective resistance of the graph. Informally, this quantity is
determined by thinking of the graph as an electrical circuit and calculating the resistance between
the initial vertex and the set of marked vertices. Belovs’ result can be seen as a quantum variant of
previous classical work characterising properties of random walks on graphs (such as the commute
time and cover time) in terms of effective resistance [15].
The main quantum subroutine used here is just the special case of Belovs’ result where the
underlying graph is a tree, for which we include a slightly more concise correctness proof. We are
also able to extend Belovs’ work to give an algorithm for finding a marked vertex in a tree, rather
than just detecting one. This can easily be achieved using binary search; in the case where there
is promised to be a unique marked element, we give a more efficient algorithm based on analysing
eigenvectors of the quantum walk.
Once we have the quantum search algorithm, all that remains is to check the claim that the P
and h functions can indeed be used to implement the required quantum walk operations, namely
mixing across the neighbours of a vertex in the tree, dependent on whether the vertex is marked.
To do this one has to be careful to ensure that the quantum walk steps are implemented efficiently.

1.3

Other prior work

Backtracking is a fundamental technique in computer science and has been studied since at least
the 1960s. The classical literature on this topic is too vast to summarise here; see [38, 29, 7] for
introductions to the topic and historical overviews. Cerf, Grover and Williams attempted to find
a direct quantum speedup of backtracking algorithms [14]. The algorithm of [14] is based on a
nested version of Grover search. The complete tree of partial assignments is expanded to a certain
depth, then quantum search is performed within the subspace of partial assignments which have
not yet been ruled out. The complexity of the algorithm depends on the number of valid partial
assignments at this depth. It is argued in [14] that, for some reasonable distributions on random
CSPs, the average complexity of the quantum algorithm (over the distribution on instances) will
be smaller than would be obtained from Grover search. By contrast, the bounds of Theorems 1
and 2 hold in the worst case and are applicable to arbitrary backtracking algorithms: if a faster
backtracking algorithm is found, we immediately obtain a faster quantum algorithm.
The algorithm used here can be seen as an extreme version of the nested search strategy of [14].
The diffusion operation used in the quantum walk can be viewed as applying Grover search within a
subspace spanned by a vertex in the tree and its children. The algorithm repeatedly performs these
searches across many vertices and levels simultaneously. On the other hand, the algorithm of [14]
can be seen as accelerating a restricted classical backtracking algorithm which uses a predicate P
which is only capable of detecting whether partial assignments at a particular level are false.
Similarly to the present work, Farhi and Gutmann [28] have studied the use of quantum walks
to speed up classical backtracking algorithms by searching within the backtracking tree. These
authors showed that there are some trees for which continuous-time quantum walks can be used
to find a marked vertex exponentially faster than a classical random walk. The special structure
of these trees leads to interference effects which enable the quantum walk to penetrate the tree
more quickly than the random walk. However, for the examples presented in [28] where there is an
exponential speedup of this form, the structure of the tree enables an alternative classical algorithm
to also find a marked vertex efficiently. Here, we seek to accelerate classical search in arbitrary
trees, with no prior assumptions about the structure of the tree.
4

A related, but different, approach towards quantum speedup of recursive classical algorithms
was proposed by Fürer [30]. Imagine we have a constraint satisfaction problem for which we can
put a non-trivial upper bound L on the number of leaves in the computation tree of a recursive
classical algorithm for solving the problem. The idea of [30]√was to apply Grover search over the
leaves of the computation tree to find a solution in time O( L poly(n)). This approach relies on
knowing, in advance, an efficiently computable mapping associating each integer between 1 and L
with a leaf. For many more complicated recursive algorithms we may not know such a mapping.
Indeed, there is some evidence that it may not be possible to compute such a mapping for general
backtracking algorithms in polynomial time [50]. The quantum algorithm presented here, on the
other hand, can be applied to any classical backtracking algorithm, even if we do not know a bound
on L in advance.
A somewhat similar idea to Fürer’s was previously used by Angelsmark, Dahllöf and Jonsson [5]
to obtain quantum speedups for CSPs. These authors observed that, for certain CSPs, one can
construct a set of dcn easily checked certificates, for some c < 1, such that the existence of a
solution to the CSP is certified by at least one certificate. Then Grover search can be used to find
a certificate, if one exists, in time O(dcn/2 poly(n)).
An alternative, and simpler, approach to find quantum speedups of classical algorithms for
CSPs is the use of amplitude amplification [12]. This can be applied to any classical algorithm
which can be expressed as repeatedly running a randomised subroutine which runs in time poly(n)
and finds a solution with probability p. The corresponding quantum algorithm has a runtime of
√
O((1/ p) poly(n)), a near-quadratic improvement on the classical O((1/p) poly(n)) if p is small.
For example, it was observed by Ambainis [2] that Schöning’s efficient randomised algorithm for
k-SAT [47] can be accelerated in this way; Dantsin, Kreinovich and Wolpert [22] gave several other
examples. Deterministic backtracking algorithms are, of course, not amenable to this approach.
Finally, a completely different technique for solving CSPs is the quantum adiabatic algorithm [27]. Although there is some numerical evidence that this algorithm may outperform classical
algorithms for CSPs [26], the adiabatic algorithm’s runtime is hard to analyse for large input sizes
and there is as yet no analytical proof of its superiority over classical algorithms.
Quantum walks on trees have been used previously in a quite different context, to obtain a
near-quadratic speedup for evaluation of AND-OR formulae [3]. In that algorithm the structure
of the formula (which is known in advance) defines the tree on which the walk takes place. It is
interesting to note that the quantum walk used in [3] is similar to the quantum walk used here, but
has apparently quite different properties. Another case in which the concept of effective resistance
was used in quantum computing is work by Wang, which gave an efficient quantum algorithm for
approximating effective resistances [53]. This uses some similar ideas to the present work but does
not seem directly applicable.

1.4

Organisation

We begin in Section 2 by describing the main underlying quantum ingredient, the use of a quantum
walk to detect a marked vertex in a tree. This algorithm is a special case of an algorithm described
by Belovs [8]. We then go on in Sections 2.1 and 2.2 to describe extensions to this algorithm to allow
finding a marked vertex, and a faster runtime in the case where we know there is a unique marked
vertex. Section 3 shows that the algorithm can be applied to accelerate backtracking algorithms for
CSPs. Section 4 discusses how to use the algorithm to obtain exponential reductions in expected
runtime, while Section 5 concludes with a discussion of some ways in which the algorithm could be
improved, and barriers to doing so.
5

1.5

Preliminaries

We will need the following tools, which have been used many times elsewhere in quantum algorithm
design:
Lemma 3 (Effective spectral gap lemma [40]). Let ΠA and ΠB be projectors on the same Hilbert
space, and set RA = 2ΠA − I, RB = 2ΠB − I. Let Pχ be the projector onto the span of the
eigenvectors of RB RA with eigenvalues e2iθ such that |θ| ≤ χ. Then, for any vector |ψi such that
ΠA |ψi = 0, we have
kPχ ΠB |ψik ≤ χk|ψik.
Theorem 4 (Phase estimation [17, 37]). For every integer s ≥ 1, and every unitary U on m qubits,
there exists a uniformly generated quantum circuit C such that C acts on m + s qubits and:
1. C uses the controlled-U operator O(2s ) times, and contains O(s2 ) other gates.
2. For every eigenvector |ψi of U with eigenvalue 1, C|ψi|0s i = |ψi|0s i.
3. If U |ψi = e2iθ |ψi, where θ ∈ (0, π), then C|ψi|0s i = |ψi|ωi, where |ωi satisfies |hω|0s i|2 =
sin2 (2s θ)/(22s sin2 θ).
P
4. For any |φi ∈ (C2 )⊗m , expanded as |φi = k λk |ψk i, where |ψk i is an eigenvector of U with
eigenvalue e2iθk , then
X
C|φi|0s i =
λk |ψk i|ωk i,
k

where

s 2
s
k:θk ≥ |hωk |0 i| = O(1/(2 )).

P

Call 2−s the precision of the circuit.
Phase estimation is normally used to estimate eigenvalues of U (hence its name); here, however,
similarly to [43] we will only need to apply it to distinguish the eigenvalue 1 from other eigenvalues.
If the smallest nonzero phase is , this can be done with O(1/) uses of controlled-U .
Fact 5 (Close states and measurement outcomes, e.g. [11]). Let |ψ1 i, |ψ2 i be quantum states
satisfying k|ψ1 i − |ψ2 ik = . Then the total variation distance between the two distributions on
measurement outcomes obtained by measuring each state in the computational basis is at most .
(This fact is usually presented with  replaced with 4 [11]; the tighter constant stated here can
easily be obtained by relating the fidelity of |ψ1 i and |ψ2 i to their trace distance, for example.)

2

Quantum walks on trees

We now describe a quantum algorithm for detecting a marked vertex in a tree. The algorithm
is a special case of a beautiful connection between quantum walks and electrical circuits due to
Belovs [8] (see also [9]), which is a quantum analogue of a similar connection between random
walks and electrical circuits [15]. This is conceptually elegant and leads to a very concise proof of
a previous result of Szegedy [51] on detecting marked elements using a quantum walk. Here we
only use these ideas for the special case of trees and a quantum walk starting at the root. This will
enable us to simplify some notation and, hopefully, make the algorithm more intuitive.

6

Input: Operators RA , RB , a failure probability δ, upper bounds on the depth n and the
number of vertices T . Let β, γ > 0 be universal constants to be determined.
1. Repeat the following subroutine K = dγ log(1/δ)e times:
√
(a) Apply phase estimation to the operator RB RA with precision β/ T n.
(b) If the eigenvalue is 1, accept; otherwise, reject.
2. If the number of acceptances is at least 3K/8, return “marked vertex exists”; otherwise,
return “no marked vertex”.
Algorithm 2: Detecting a marked vertex

Consider a rooted tree with T vertices, labelled r, 1, . . . , T − 1, with vertex r being the root,
where the distance from the root to any leaf is at most n. Assume for simplicity in what follows
that the root is promised not to be marked. For each vertex x, let `(x) be the distance of x from
the root. We assume throughout that, although we do not necessarily know the structure of T in
advance, we can determine `(x) for any x. Let A be the set of vertices an even distance from the
root (including the root itself), and let B be the set of vertices at an odd distance from the root.
We write x → y to mean that y is a child of x in the tree. For each x, let dx be the degree of x as a
vertex in an undirected graph. Thus, for all x 6= r, dx = |{y : x → y}| + 1; and dr = |{y : r → y}|.
The quantum walk operates on the Hilbert space H spanned by {|ri}∪{|xi : x ∈ {1, . . . , T −1}},
and starts in the state |ri. Unlike many discrete-time quantum walk algorithms, it does not use a
separate “coin” space. The walk is based on a set of diffusion operators Dx , where Dx acts on the
subspace Hx spanned by {|xi} ∪ {|yi : x → y}. The diffusion operators are defined as follows:
• If x is marked, then Dx is the identity.
• If x is not marked, and x 6= r, then Dx = I − 2|ψx ihψx |, where
!
X
1
|ψx i = √
|xi +
|yi .
dx
y,x→y
• Dr = I − 2|ψr ihψr |, where
1
|ψr i = √
1 + dr n

|ri +

√

!
n

X

|yi .

y,r→y

Observe that Dx can be implemented with only local knowledge, i.e. based only on whether x is
marked and the neighbourhood
structure of x. A step
L
L of the walk consists of applying the operator
RB RA , where RA = x∈A Dx and RB = |rihr| + x∈B Dx . An alternative way of viewing this
process is as a quantum walk on the graph given by the edges of the tree, where we identify each
vertex with the edge from its parent in the tree, and add an additional “input” edge into the root.
The algorithm for detecting a marked vertex is presented as Algorithm 2.
√
Lemma 6 (Special case of Belovs [8]). Algorithm 2 uses RA and RB O( T n log(1/δ)) times. There
exist universal constants β, γ such that it fails with probability at most δ.
7

Proof. The complexity bound is immediate from Theorem 4. For the correctness proof, we first
show that, if there is a marked vertex, then |ri is quite close to (a normalised version of) an
eigenvector |φi of RB RA with eigenvalue 1. Let x0 be a marked vertex and set
X
√
(−1)`(x) |xi.
(1)
|φi = n|ri +
x6=r,x x0

Here x
x0 denotes the vertices x on the unique path from the root to x0 , including x0 itself.
To see that |φi is invariant under RB RA , first note that |φi is orthogonal to all states |ψx i, where
x 6= r and x is not marked. Indeed, any such state |ψx i either has uniform support on exactly 2
consecutive vertices v in the path from r to x0 , or is not supported on any vertices in this path.
|φi is also orthogonal to |ψr i by direct calculation. We have
k|φik2 = n + `(x0 ) ≤ 2n.
Thus

hr|φi
1
≥√ .
k|φik
2

Therefore, phase estimation returns the eigenvalue 1 with probability at least 1/2. On the other
hand, if there are no marked vertices, we consider the vector
√ X
|ηi = |ri + n
|xi.
x6=r

Let ΠA and ΠB be projectors onto the invariant subspaces of RA and RB . These spaces are spanned
by vectors of the form |ψx⊥ i for x ∈ A, x ∈ B respectively, where |ψx⊥ i is orthogonal to |ψx i and has
support only on {|xi} ∪ {|yi : x → y}; in addition to |ri in the case of RB . On each subspace Hx ,
x ∈ A, |ηi is proportional to |ψx i, so ΠA |ηi = 0. Similarly √
ΠB |ηi = |ri. By the effective spectral
√ gap
lemma (Lemma 3), kPχ |rik = kPχ ΠB |ηik ≤ χk|ηik ≤ χ T n. For small enough χ = Ω(1/ T n),
this is upper-bounded by 1/2.
√ By Theorem 4, there exists β such that applying phase estimation
to RB RA with precision β/ T n returns the eigenvalue 1 with probability at most 1/4.
Using a Chernoff bound, by repeating the subroutine O(log 1/δ) times and returning “marked
vertex exists” if the fraction of acceptances is greater than 3/8, and “no marked vertex” otherwise,
we obtain that the overall algorithm fails with probability at most δ.

2.1

Finding a marked vertex

From now on, we assume that the degree of every vertex in the tree is O(1); this is not a significant
restriction for the application to backtracking. For trees obeying this restriction we can use the
detection algorithm as a subroutine to find a marked vertex efficiently, via binary search.
To find a marked vertex, we start by applying Algorithm 2 to the entire tree. If it outputs
“marked vertex exists”, we apply the algorithm to the subtrees rooted at each child of the root
in turn, to detect marked vertices within each subtree. Assuming the algorithm did not fail at
any point, there must be a marked vertex in at least one subtree. We pick the root of one such
subtree and check whether it is marked. If it is marked, we output its label and terminate; if it is
not marked, we apply Algorithm 2 to each of its children and repeat. This process continues until
we have found a marked vertex. As there are at most O(n) repetitions to reach a leaf and O(1)
subtrees are checked at each repetition, the time complexity of the algorithm is multiplied by a
factor of O(n). Note that, when we apply the algorithm to subtrees, we must leave the parameter
8

T unchanged; this is because the tree could be quite unbalanced, and a given subtree could contain
many vertices.
We have thus far assumed that we know an upper bound on T in advance. If we do not, we
can repeat the whole search algorithm O(log T ) = O(n) times, doubling a guess for T each time
(starting with T = 1) until we either find a marked vertex, or the algorithm returns “no marked
vertex”. This exponential doubling does not affect the asymptotic runtime. If our guess for T is
too low, the correctness proof of Algorithm 2 no longer holds, so the detection algorithm may claim
that there is a marked vertex in a situation where there is actually no marked vertex. This may
lead to the above binary search procedure returning an incorrect result. But we can deal with this
situation by checking the final vertex returned by the search algorithm, and only terminating if it
is marked; if it is not, we know that the search has failed, and continue doubling our guess for T .
On the other hand, one can see from inspecting the proof of Lemma 6 that, if there is a marked
vertex, the phase estimation subroutine in Algorithm 2 will accept with probability at least 1/2
whether or not our guess for T is large enough. Therefore, if there is a marked vertex, Algorithm
2 will output that a marked vertex exists with probability at least 1 − δ, for δ of our choice.
Using this procedure the total number of uses of Algorithm 2 (with differing values of T ) is
O(n2 ), so in order for the whole algorithm to succeed with probability, say, 2/3, it is sufficient to
reduce the failure probability of each use of Algorithm 2 to O(1/n2 ). This
an additional time
√ costs
3/2
factor of O(log n) per use of the algorithm, giving a total runtime of O( T n log n). This can in
turn be improved to an arbitrary
√ failure probability δ > 0 by taking O(log 1/δ) repetitions, leading
to an overall bound of time O( T n3/2 log n log(1/δ)).
Finally, we can find all marked vertices by simply repeating the algorithm, modifying the
underlying oracle operator to strike√out previously seen marked elements. If there are k marked
elements, the overall runtime is O(k T n3/2 log n log(k/δ)).

2.2

Search with a unique marked element

If we are promised that there exists a unique marked element in the tree, we can improve the above
bounds by a factor of almost n. In general this improvement is not particularly large, as we usually
have T  n; however, for some “tall and thin” trees it can be relatively significant. In particular,
following this improvement we see that the complexity of the quantum algorithm for the search
problem is never worse than the classical complexity O(T ), up to logarithmic factors.
We assume that there is a unique marked vertex x0 and that `(x0 ) = n. This second assumption
is without loss of generality. We can determine `(x0 ) at the start of the algorithm by applying
Algorithm 2 to the subtree rooted at r and of depth i, for differing values of i. That is, we only
expand the tree up to depth i, and use binary search on i ∈ {1, . . . , n} to find the minimal i such
that the tree
√ of depth i contains x0 . This needs O(log n) repetitions, so the complexity of this
part is O( T n log n log log n), where the log log term comes from reducing the failure probability
of Algorithm 2 to O(1/(log n)). Once `(x0 ) is determined, we henceforth only search within the
tree of depth `(x0 ).
Let |φ0 i = |φi/k|φik, where the eigenvector |φi is defined in (1), i.e.
X
1
1
|φ0 i = √ |ri + √
(−1)`(x) |xi.
2
2n x6=r,x x
0

The starting point for the search algorithm is the observation1 that |φ0 i encodes the entire path
1

A similar observation was used in [53] to approximate effective resistances.

9

from r to x0 . If we measure |φ0 i, and do not receive outcome r, we receive a measurement outcome
y which is uniformly distributed on the path from r to x0 . We can then repeat the algorithm on
the subtree rooted at y, obtaining a new state of the form of |φ0 i for a smaller value of n. The
expected number of measurements we would need to make to find x0 is logarithmic in n (rather
than the bound of O(n) which follows from the previous binary search algorithm).
We first bound the total number of quantum walk steps used to find x0 , given access to states
of the form of |φ0 i for various subtrees. Let C = O(1/
√log n) be chosen such that Algorithm 2 fails
with probability at most 1/(4n) and uses at most C T n steps. Given that `(x0 ) = n, measuring
a copy of |φ0 i will give a “good” outcome (which is not r) with probability 1/2. The distance from
the root of such an outcome is uniformly distributed. Considering only the good outcomes, the
expected total number of steps Sn to find x0 , given that `(x0 ) = n, therefore satisfies
n−1

Sn ≤

√
1X
Si + C T n.
n
i=0

√

We claim that Sn = O(C T√n). The proof is by induction. First, S0 = 0 as no quantum walk steps
are made. Assume Si ≤ 4C T i for all i < n. Then
v
u n−1
n−1
u1 X
X
√
√
√
√
√
4C
4C √ √
Sn ≤
T i + C T n ≤ 4C t
T i + C T n = √ T n − 1 + C T n ≤ 4C T n,
n
n
2
i=0
i=0
where the second inequality is Jensen’s inequality.
As on average half the outcomes are good, the
√
expected total number of steps is thus O( T n log n).
We can approximately produce |φ0 i by applying phase estimation to the operator RB RA , with
input state |ri. If we write
1
1
|ri = √ |φ0 i + √ |φ⊥ i,
2
2
where |φ⊥ i is normalised and orthogonal to |φi, the result of applying phase estimation on |ri with
s ancilla qubits is a state of the form
1
1 X
√ |φ0 i|0s i + √
λk |ψk i|ωk i,
2
2 k,θ >0
k

where |ψk i is an eigenvector of RB RA with eigenvalue e2iθk . Write each |ωk i as |ωk i = µk |0s i + |ωk0 i
for some subnormalised vectors |ωk0 i orthogonal to |0s i. If we obtain outcome |0s i when we measure
the second register, the first register collapses to


X
1
|φ0 i +
|φe0 i = q
λk µk |ψk i .
P
1 + k,θk >0 |λk µk |2
k,θk >0
To bound the distance between |φe0 i and the desired state |φ0 i, we split the sum into two parts. For
any  > 0, via Theorem 4 we have
X
X
|λk µk |2 ≤
|µk |2 = O(1/(2s )).
k,θk ≥

k,θk ≥

On the other hand, we prove the following technical claim in Appendix A. Recall that P is the
projector onto the span of the eigenvectors of RB RA with eigenvalues e2iθ such that |θ| ≤ .
10

√
Lemma 7. kP |φ⊥ ik = O( T n).
Given Lemma 7, we have
X
k,0<θk ≤

|λk µk |2 ≤

X

|λk |2 = kP |φ⊥ ik2 = O(2 T n).

k,0<θk ≤

√
√
Fixing an accuracy δ and taking  = Θ(δ/ T n), 2s = O( T n/δ 3 ), we have k|φe0 i−|φ0 ik = O(δ). By
Fact 5, measuring |φe0 i in the computational basis is indistinguishable from measuring |φ0 i, except
with probability O(δ). If we take δ = O(1/ log n), the algorithm does not notice the difference on
any of the O(log
√ n) states used, with probability Ω(1). The overall complexity of the algorithm
is therefore O( T n log3 n)2 . As before, the failure probability can be made arbitrarily small via
repetition.
In Section 5 we discuss some barriers to improving the complexity and applicability of these
algorithms.

3

From quantum walks on trees to accelerating backtracking

To complete the proofs of Theorems 1 and 2, we now verify that Algorithm 2 can be applied to
search in the tree defined by a backtracking algorithm. In order to do this, it is sufficient to define
a suitable efficient mapping between partial assignments and vertices in a tree, and to implement
the operators RA and RB appropriately and efficiently. As the quantum walk subroutines assume
that the root of the tree is not marked, the first step of the algorithm is to check whether P (∗n )
is true. If so, the algorithm immediately returns “true”; if not, it runs Algorithm 2 on a graph
defined as follows.
The current state of the backtracking algorithm is represented by a vertex in a rooted tree
labelled with a sequence of the form (i1 , v1 ), . . . , (i` , v` ), for 1 ≤ ` ≤ n. The sequence corresponds to
a partial assignment x ∈ D where we assign xik = vk for k = 1, . . . , `, and xj = ∗ for all other indices
j. The tree only contains vertices corresponding to valid partial assignments. Each vertex except for
the root (which is labelled with the empty sequence) is connected to its parent, the vertex labelled
with (i1 , v1 ), . . . , (i`−1 , v`−1 ). It is also connected to all vertices of the form (i1 , v1 ), . . . , (i` , v` ), (j, w),
where j = h((i1 , v1 ), . . . , (i` , v` )), w ∈ [d], and P ((i1 , v1 ), . . . , (i` , v` ), (j, w)) is not false. That is,
all vertices corresponding to valid partial assignments which extend the current partial assigment
by assigning a value to the variable whose index is given by h. It is convenient to assume that
the predicate P and the heuristic h take as input a string of (index, value) pairs which describe
value assignments to variables, rather than an element of D; if not, converting between these
representations can be done in time O(n). We will also assume that, for all complete assignments,
the predicate returns either true or false (as it should do).
The algorithm takes place within the Hilbert space H(n) = Cn+1 ⊗ (Cn+1 ⊗ Cd+1 )⊗n together
with an ancilla space. Each basis vector within H(n) represents a partial assignment described by
a sequence as above. The first register stores a level ` between 0 and n, representing the length
of the sequence (the number of non-∗’s in the assignment). Each of the next ` registers stores a
pair (ik , vk ) giving the index of a variable (an integer between 1 and n) and the assignment to that
variable (an integer between 0 and d − 1). Except during updates to the state, the remaining n − `
registers all contain the pair (0, ∗). The algorithm can easily be modified to use qubits if desired,
2

One way to improve the polylogarithmic factors in this complexity could be to reweight the tree such that the
eigenvector of RB RA with eigenvalue 1 has more weight on x0 (Alexander Belov, personal communication).

11

Input: A basis state |`i|(i1 , v1 )i . . . |(in , vn )i ∈ H(n) corresponding to a partial assignment
xi1 = v1 , . . . , xi` = v` . Ancilla registers Hanc , Hnext , Hchildren , storing a tuple (a, j, S), where
a ∈ {∗} ∪ [d], j ∈ {0, . . . , n}, S ⊆ [d], initialised to a = ∗, j = 0, S = ∅.
1. If P (x) is true, return.
2. If ` is odd, subtract h((i1 , v1 ), . . . , (i`−1 , v`−1 )) from i` and swap a with v` .
3. If a 6= ∗, subtract 1 from `. (Now ` is even and (i`+1 , v`+1 ) = (0, ∗).)
4. Add h((i1 , v1 ), . . . , (i` , v` )) to j.
5. For each w ∈ [d]:
(a) If P ((i1 , v1 ), . . . , (i` , v` ), (j, w)) is not false, set S = S ∪ {w}.
6. If ` = 0, perform the operation I − 2|φn,S ihφn,S | on Hanc . Otherwise, perform the
operation I − 2|φ1,S ihφ1,S | on Hanc .
7. Uncompute S and j by reversing steps 5 and 4.
8. If a 6= ∗, add 1 to `. If ` is now odd, add h((i1 , v1 ), . . . , (i`−1 , v`−1 )) to i` and swap v`
with a. (Now a = ∗ again.)
Algorithm 3: Implementation of the operator RA

rather than systems with dimension n + 1 and d + 1, by encoding each subsystem in O(log n + log d)
qubits.
Let Uα,S , for S ⊆ [d] and α ∈ R, act on Cd+1 with basis {|∗i, |0i, . . . , |d − 1i} by mapping
|∗i 7→ |φα,S i, where
!
√ X
1
|∗i + α
|ii .
|φα,S i := p
α|S| + 1
i∈S
We assume that, for any subset S ⊆ [d] and any fixed α ∈ R, we can perform Uα,S and its inverse
in time O(1) each. (Dependent on the gate set being used, we may not be able to implement Uα,S
exactly. However, for any universal gate set we can implement it up to accuracy 1 −  in time
poly log(1/); this will multiply the runtime of the overall algorithm by at most a polylogarithmic
factor.) By applying Uα,S and its inverse we can perform the operation I − 2|φα,S ihφα,S |.
In order to use Algorithm 2, we need to implement the operators RA and RB . The implementation of RA using I − 2|φα,S ihφα,S |, P and h is described in Algorithm 3 above. RB is similar,
except that: step 1 is replaced with the check “If P (x) is true or ` = 0, return”; “odd” is replaced
with “even” in steps 2 and 8; and the check “If ` = 0” is removed from step 6. The first of these
changes is because RB should leave the root of the tree invariant; and the last is because ` is always
odd at that point in the modified algorithm, so the check is unnecessary.
We now argue that Algorithm 3 correctly implements RA . Write x = (i1 , v1 ), . . . , (i` , v` ) for the
partial assignment passed to the algorithm, and write x0 = (i1 , v1 ), . . . , (i`−1 , v`−1 ) for the
L parent
partial assignment in the tree. The goal of the algorithm is to implement the operator x∈A Dx
defined in Section 2. For each x ∈ A, Dx only acts on the subspace corresponding to x and
its children. To implement Dx , it is therefore sufficient to map the basis state corresponding to
12

(i1 , v1 ), . . . , (i` , v` ), and all the basis states corresponding to (i1 , v1 ), . . . , (i` , v` ), (j, w) for w ∈ [d],
where j = h((i1 , v1 ), . . . , (i` , v` )) and ` is even, to a (d + 1)-dimensional subspace on which the
children of x can be mixed over using Uα,S , and then returning to the original subspace. This is
precisely what Algorithm 3 does.
In more detail, the algorithm performs the following steps. First, it does nothing when x is
marked, corresponding to the definition of Dx . If x is not marked, the behaviour depends on
whether ` is even (corresponding to x ∈ A) or ` is odd (corresponding to x ∈ B). Define y by
setting y = x if x ∈ A, and y = x0 if x ∈ B. Then the algorithm implements an inversion about
|ψy i, which is split into three subparts:
• Steps 2-3: Perform a map of the form |xi 7→ |yi|∗i for x ∈ A, and |xi 7→ |yi|wi for x ∈ B,
where w is the value of x at the h(x0 )’th position, i.e. the most recent variable assignment
that was made by the backtracking algorithm.
• Steps 4-5: Determine the children of y.
• Step 6: Perform the operation I − 2|ψy ihψy | using the knowledge of the children of y.
• Steps 7-8: Uncompute junk and reverse the first map.
It can be verified that the algorithm implements the desired behaviour for all basis state inputs
|`i|(i1 , v1 )i . . . |(in , vn )i such that (i1 , v1 ), . . . , (i` , v` ) is a valid path in the L
backtracking tree; we
omit the routine details. As the algorithm implements the operation RA = x∈A Dx unitarily for
all basis states |xi, it also implements RA correctly for all superpositions of basis states. Together
with the similar implementation of RB , this is enough to implement Algorithm 2. For each use of
RA and RB the algorithm uses O(1) auxiliary operations as claimed.

4

From quadratic speedups to exponential speedups

In this section we show that it is possible to leverage the speedup achieved by the quantum backtracking algorithm to obtain much more significant speedups over classical algorithms – but in a
non-standard, average-case setting.
For any (classical or quantum) algorithm A, let TA (X) denote the expected runtime of A on
input X. Let P be a distribution on inputs
pX. Imagine we have a quantum algorithm Q and
a classical algorithm C such that TQ (X) ≈ TC (X) for all X. This is the case p
for the quantum
algorithms presented here, where for CSPs on n variables we have TQ (X) ≤ TC (X) poly(n).
Then, by Jensen’s inequality, we have
p
p
EX∼P [TQ (X)] ≤ EX∼P [TQ (X)2 ] . EX∼P [TC (X)].
However, dependent on the distribution P, taking the average in this way can sometimes amplify
the separation to become much greater than quadratic, and even sometimes exponential or superexponential. This point was noted in the context of quantum query complexity by Ambainis and
de Wolf [4], who gave several examples of super-polynomial average-case quantum speedups for the
computation of total functions, and later by Montanaro [44], who showed that even the unstructured
search problem with a unique marked element, with power-law distributions on the position of this
marked element, can display this behaviour.
One very simple example of this phenomenon is the following separation. Let C be a classical
algorithm for Circuit SAT. Assume that, for each integer n, there exists an instance of Circuit SAT
13

on n variables such that C has runtime Ω(2n ) (this is the case for the best classical algorithms at
present [54]). Also let Q be a quantum algorithm which solves Circuit SAT using Grover’s algorithm,
using time O(2n/2 poly(n)) on an input of size n. Finally, let Pn be the following distribution on
instances with n variables: with probability p, return a hard instance of size n; with probability
1 − p, return a trivial instance. Then
EX∼Pn [TC (X)] = Ω(p2n ),

EX∼Pn [TQ (X)] = O(p2n/2 poly(n)).

If we take p = 2−n/2 , the separation between these two quantities is exponential.
However, this is clearly a rather contrived distribution on the inputs. One might hope to find
some problem, together with a more natural distribution on the inputs, which allows a similar
exponential separation to be proven. The quantum backtracking algorithm allows one to find
separations of this form, given a backtracking algorithm with a suitable distribution of runtimes.
Indeed, imagine we have a family of CSPs and a distribution Pn on problems of size n such that
with high probability the problem has O(1) solutions. Further imagine that we have a deterministic
classical backtracking algorithm whose backtracking tree contains T (X) vertices on input X, such
that PrPn [T (X) = t] ≤ Ctβ for all t and some constants C and β. In addition, assume that
PrPn [T (X) = t] ≥ Dtβ , for some constant D, for M different values t. Here M is some large integer
which we think of as being exponentially large in n. Then
EX∼Pn [T (X)] ≥

M
X

Dtβ · t = Ω(M β+2 ).

t=1

For β > −2, this quantity is exponentially large. However, if −2 < β < −3/2, the quantum
backtracking algorithm described above uses an average of
X √
p
EX∼Pn [O( T (X) poly(n))] ≤
O( t · tβ poly(n)) = poly(n)
t≥1

quantum walk steps. If each step requires time poly(n) (to evaluate the predicate P and the
heuristic h) we have obtained an exponential reduction in expected runtime.
We therefore see that a “power law” tail of the distribution Pn of the form pt = PrPn [T (X) =
t] ∼ tβ , for a suitable value of β, gives us an exponential separation. There is substantial empirical
evidence, and some analytical evidence, that such power law, or “heavy”, tails can occur in both
random and real-world instances of CSPs; for a survey, see [33]. For example, consider the case of
graph k-colouring on random graphs with n vertices, where each edge is present with probability
Θ(1/n). Hogg and Williams [35] observed that a natural backtracking algorithm seemed to have a
power-law distribution of its runtimes. Later work by Jia and Moore [36] provided some analytical
justification for this, and additional experiments, which together suggest that for 3-colouring the
distribution is of the form pt ∼ t−1 .
However, there are several reasons why it is unclear that this phenomenon could lead to exponential separations between quantum and classical expected runtimes. First, there is some evidence
that some apparently heavy-tailed behaviour may in fact be due to finite-size effects [20, 21]. Second, one reason for a skewed runtime distribution could be that, on satisfiable instances, the
backtracking algorithm sometimes gets lucky and happens to find a satisfying assignment early on,
after which it terminates. The runtime of the quantum algorithm described here depends on the
size of the whole tree and hence will not correspond to the square root of the classical runtime in
this case. Indeed, runtime distributions on unsatisfiable instances do not seem to display the same
heavy-tailed behaviour [46, 31].
14

Third, in many cases power-law behaviour is observed when a randomised backtracking algorithm is run on a single instance. That is, when the choices of branching variables made by the
algorithm are random and we consider the distribution of the runtimes T (r) over the choice of
random seed r. Algorithmic randomness of this form (as opposed to picking the input instance at
random) is not suitable for obtaining an exponential quantum-classical separation using the quantum backtracking algorithm. This is because, if the quantum
p backtracking algorithm’s expected
runtime over r is at most R, for some R, we have R = Ω(Er [ T (r)]). So, by Markov’s inequality,
T (r) = O(R2 ) with, say, 99% probability. Therefore, if we stop the classical algorithm after time
O(R2 ), it will succeed with probability Ω(1).
For these reasons, we consider random instances of CSPs produced not just by using a fixed
density of constraints, but by taking a distribution over different constraint densities. This enables
us to find relatively natural input distributions under which the expected runtime of the quantum
backtracking algorithm is exponentially faster.

4.1

Expected runtime bounds

There is now a substantial body of work proving bounds on the expected runtime of DPLL-type
algorithms for random k-SAT. For example, consider k = 3 and instances consisting of m = αn
uniformly random clauses. For α & 4.3, there is strong evidence that such instances very rarely
have a solution [48], so the task of the algorithm is usually to prove unsatisfiability. Beame et al. [6]
have shown that, for a simple DPLL variant (known as ordered DLL) the runtime is 2Θ(n/α) with
probability 1 − o(1). Cocco and Monasson [18, 19] have used statistical physics techniques to even
determine (non-rigorously) the constant in the exponent. In particular, they argue that, for large
α, the runtime is approximately 20.292n/α .
Sometimes one can prove such tight bounds rigorously. For example, consider the following very
simple backtracking algorithm, which fits within the framework of Algorithm 1. Fix an ordering
of the variables from 1 to n. Then the heuristic h returns the lowest index of a variable which has
not yet been assigned a value. Call this algorithm Naı̈veBt. Then the following result holds:
Proposition 8. The expected number of vertices E in the backtracking tree of the Naı̈veBt algorithm
when applied to a random k-SAT instance on n variables, with m = αn uniformly random clauses,
for 1 ≤ α ≤ nk−1 , satisfies
0
2C n ≤ E ≤ O(n2Cn ),
√
√
where C and C 0 depend only on α and k. For k = 3, C ≤ 0.907/ α, C 0 ≥ 0.906/ α − 0.142/α2 .
Proof. See Appendix B.
Similar analyses to Proposition 8 have been carried out many times in the literature, albeit
often for slightly different models (e.g. [13, 45]).
Let Cn denote the expected runtime of the Naı̈veBt algorithm applied to 3-SAT instances on n
variables, where the expectation is taken with respect to a distribution over numbers of constraints
m. If the probability that we have m constraints is pm , then by Proposition 8
√
X
2
Cn ≥
pm 2n(0.906 n/m−0.142(n/m) ) .
m

On the other hand, up to a poly(n) factor, on any instance the runtime of the quantum backtracking
algorithm is at most the square root of the classical one, multiplied by the number of solutions (if
15

there are any). We consider a distribution pm which is only supported on values of m such that
the probability that a random CSP with m constraints has a solution is O(2−n ). For such values
of m, we can ignore the additional cost for finding all the solutions. For 3-SAT, this is true for
m > 16n/(ln 2), for example (see Appendix B).
Letting Qn denote the expected runtime of the quantum algorithm applied to Naı̈veBt, we
therefore have
X
3/2 √
Qn ≤
pm 20.454n / m poly(n).
m
3/2

√

Consider the distribution pm ∝ 2−0.454n / m for 16n/(ln 2) < m ≤ n3 . Then
X
3/2 √
2
2(0.906−0.454)n / m−0.142(n/m) ) = Ω(20.094n ),
Qn = poly(n), Cn = Ω(
m>16n/(ln 2)

where the asymptotic bound follows from inserting m = d16n/(ln 2)e. We therefore have an averagecase exponential separation between the quantum and classical complexities of 3-SAT√under this
3/2
distribution; and, indeed, for various other distributions of the form pm ∝ 2−Cn / m . While
this family of distributions is arguably less contrived than the Circuit SAT example given above
(for example, the number of variables is fixed; only the number of clauses varies), it still appears
somewhat unnatural. It seems to be an interesting question to determine more natural input
distributions which also lead to exponential quantum speedups.

5

Improving the quantum walk algorithm?

We finish by addressing the question of how tight the bounds are which we have obtained on
quantum search
√ in trees. It is clear that, given a tree with T vertices, we must have a lower bound
of the form Ω( T ) for finding a marked vertex (otherwise,
we could use the algorithm to solve the
√
unstructured search problem on T elements using o( T ) quantum queries, which is impossible [10]).
There are several plausible ways in which the complexity of the algorithm presented here could be
improved to get closer to this bound. However, there appear to be some challenges to doing so in
each of these cases.
1. Reduction of the dependence on the depth n. It is easy to see that, if we would like to apply
the quantum backtracking algorithm to general trees, there must be some dependence on
the depth in the runtime. Indeed, consider a path on T vertices, which has depth T − 1.
Then, if the marked vertex is the last one in the path, we require Ω(T ) steps to find it. More
generally, it was shown by Aaronson and Ambainis [1] that for each pair T and n, there is
a tree containing T vertices
√ and with depth O(n) such that determining the existence of a
marked vertex requires Ω( T n) queries. This holds even if we know the tree in advance and
are allowed to perform arbitrary “local” operations to search within it.
2. Reduction of the overhead for searching with multiple marked vertices. It would be interesting
to determine whether the search algorithm in Section 2.2 could be generalised to work with a
similar efficiency for an arbitrary number of marked vertices. The question of when one can
convert a quantum walk speedup for detecting a marked element to a speedup for finding a
marked element has been studied previously. But while it was shown by Szegedy [51] that
the time to detect a marked element using a quantum walk is at most the square root of the
classical hitting time, it is not known whether the time to find a marked element has the
same scaling in general.
16

Indeed, Krovi et al. [39] have described a way (generalising previous results of [52, 42]) to
modify the original quantum walk approach of Szegedy to obtain a quadratic speedup for the
search problem in the case where there is a unique marked element. However, if there is more
than one marked element, the runtime of their algorithm scales with a quantity they call
the extended hitting time, which may be larger than the hitting time. In any case, all these
algorithms assume that the graph is known in advance and the initial state of the quantum
walk algorithm corresponds to the stationary distribution of the random walk. Neither of
these assumptions applies here.
3. Reduction of the dependence on k to find one, or all, of k marked vertices. For the unstructured search problem
p with k marked elements out of T , Grover’s algorithm can find a marked
element
using
O(
T /k) queries, which implies an algorithm which finds all marked elements
√
in O( T k) queries. It p
would be natural to hope for a bound of√a similar form for quantum
search on trees, e.g. O( T n/k) to find a marked vertex and O( T nk) to find all k of them.
Unfortunately, it is far from clear that this can be achieved.
Indeed, consider the following argument due to Alexander Belov.√Imagine we have access to
an algorithm A which finds one of k > 1 marked vertices using o( T n) queries, and consider
an arbitrary tree containing one marked leaf `0 . Modify the tree by attaching a subtree of
depth O(log k) below that leaf containing k vertices, all of which are marked and are labelled
such that `0 can√be determined from their labels. Then, using A, we can find one of these
vertices using o( T n) queries. Finding such a√vertex enables us to find `0 with no additional
queries, contradicting the aforementioned Ω( T n) lower bound [1]. However, this argument
does not rule out the
√ possibility that some other approach could find all k marked vertices
in, for example, O( T nk) time.
One other way in which it might be possible to improve the quantum backtracking algorithm is in
situations where the classical backtracking algorithm is lucky and finds a solution without exploring
the whole tree. For such instances the quantum algorithm, which is forced to explore the whole
tree, may not outperform the classical algorithm. It might be possible to improve the performance
of the quantum algorithm in this situation by biasing it to prefer to explore the parts of the tree
visited by the classical algorithm earlier on.

Acknowledgements
I would like to thank Alexander Belov and Aram Harrow for helpful comments on previous versions
of this paper. This work was supported by EPSRC Early Career Fellowship EP/L021005/1.

A

Proof of technical claim for search with one marked element

In this appendix, we prove the following claim from Section 2.2:
√
Lemma 7 (restated). kPχ |φ⊥ ik = O(χ T n).
Let x0 be the unique marked vertex, assuming for simplicity in the proof (as justified in Section

17

2.2) that `(x0 ) = n, and hence that x0 is a leaf in the tree. We can write


X
√
√
√
1
(−1)`(x) |xi
2|ri − |φ0 i = 2|ri − √  n|ri +
|φ⊥ i =
2n
x6=r,x x0
X
1
1
= √ |ri − √
(−1)`(x) |xi.
2
2n x6=r,x x
0

Recall that ΠA and ΠB are projectors onto the invariant subspaces of RA and RB . The invariant
subspace of RA is spanned by vectors of the form |ψx⊥ i for each vertex x ∈ A, and if x0 ∈ A, in
addition the vector |ψx0 i. The invariant subspace of RB is similar (replacing A with B) but also
contains |ri. Here hψx |ψx⊥ i = 0 and |ψx⊥ i has support only on {|xi} ∪ {|yi : x → y}. In order
to apply the effective spectral gap lemma, we determine a vector |ξi such that ΠA |ξi = 0 and
ΠB |ξi = |φ⊥ i.
First assume x0 ∈ B. We will take |ξi to be a linear combination of vectors |ψx i for x ∈ A.
Then the first of these two constraints is immediately satisfied. The second will be satisfied if, for
a set of vectors |ζi which span the invariant subspace of RB , i.e.
|ζi ∈ {|ri, |ψx0 i} ∪ {|ψx⊥ i : hψx⊥ |ψx i = 0, x ∈ B},
we have hζ|ξi = hζ|φ⊥ i. To compute the required inner products, first observe that |ψx⊥ i only has
support on x and its children, so for all x not on the path from r to x0 , hψx⊥ |φ⊥ i = 0. On the other
hand, for each x ∈ B such that x
x0 , define a basis for the space span{|ψx⊥ i : hψx⊥ |ψx i = 0} by
fixing the vectors
X
⊥
|ψx,i
i = −|xi + (dx − 1)|Ni (x)i −
|Nj (x)i,
j6=i

where Ni (x) denotes the i’th child of x, recalling that dx denotes the degree of x. We have
(
√
−dx / 2n if i = i0
⊥
⊥
hψx,i |φ i =
0
otherwise

(2)

where i0 denotes the unique child of x on the path to x0 .
P
We now find a vector
|ξi
=
First, we require αr =
x αx |xi satisfying
√
√ the above constraints.
⊥
0
⊥
hr|ξi = hr|φ i = 1/ 2 and αx0 = hx0 |φ i = 1/ 2n. For each x, let x denote the parent of x in
the tree. For |ξi to be a linear combination of vectors |ψx i, x ∈ A, it is necessary and sufficient
√
that αx = αx0 for all x ∈ B; except in the case `(x) = 1, where we require αx = n αr . We in
addition need αx = αx0 for all x 6= r ∈ A such that x0 is not on the path to x0 , in order that
hψx⊥0 |ξi = hψx⊥0 |φ⊥ i = 0. For each child y of x ∈ B, set αy = γ if y 6 x0 , and αy = δ if y
x0 .
Then from (2) we have the final constraints that
−αx + 2γ − δ = 0 if y 6

x0 ,

dx
if y
x0 .
−αx − (dx − 2)γ + (dx − 1)δ = − √
2n
p
√
These equations have unique solution γ = αx − 1/ 2n, δ = αx − 2/n. This now uniquely defines
all coefficients αx . In particular, observe that
r

r
n
n−1
2
1
α x0 =
−
=√
2
2
n
2n
18

as required.
This constructs |ξi in the case where x0 ∈ B. If instead x0 ∈ A, the procedure is similar.
Now |ψx0 i is not in the invariant subspace of RB (which only makes it easier to satisfy the inner
product constraints), but also |ξi must be a linear combination of vectors |ψx i corresponding only
to unmarked vertices x ∈ A. This new constraint implies that now αx0 = 0. But following the
above procedure now gives
r
r
n n 2
αx0 =
−
=0
2
2 n
p
√
as required. In either case, for all x, we have |αx | ≤ n/2.√So k|ξik = O( T n) and hence, by the
effective spectral gap lemma (Lemma 3), kPχ |φ⊥ ik = O(χ T n).

B

The runtime of the Naı̈veBt backtracking algorithm for k-SAT

Here we find simple, yet fairly precise, bounds on the expected number of vertices in the backtracking tree for the Naı̈veBt algorithm when applied to random k-SAT with k = O(1).
Assume we pick a random instance of k-SAT by choosing m = αn clauses, for some α such that
1 ≤ α ≤ nk−1 . Each clause contains k distinct variables, and each variable can be present negated
or unnegated.
Each clause is chosen uniformly at random, with replacement, from the set of all

2k nk allowed such clauses. Recall that the Naı̈veBt algorithm is a backtracking algorithm in the
framework of Algorithm 1 where the heuristic h simply picks the lowest index of a variable which
has not yet been assigned a value.
The probability that a given assignment to variables x1 , . . . , x` is consistent with all the clauses
in such a random instance is
(1 − Pr[clause only depends on first ` variables] Pr[assignment fails to satisfy clause])m
 !m
1−

=

`
k

.


2k nk

The expected number of solutions is
−k αn

2n (1 − 2−k )m ≤ 2n e−2

−k ln 2)α)n

= 2(1−(2

,

so for α  2k / ln 2, the probability that the instance is satisfiable is exponentially small in n. The
expected number of vertices in the backtracking tree is
 !m
n
`
X
E :=
2` 1 − k k n
.
2 k
`=0
We have
max 2

`

`

1−

`
k

 !m

≤ E ≤ (n + 1) max 2`
n

2k k

`

For the upper bound, using 1 − x ≤ e−x we obtain
 !m
max 2`
`

1−

`
k

2k nk



≤ max 2` e

`(`−1)...(`−k+1)

−α2−k n n(n−1)...(n−k+1)

`

1−

 !m

.
n

2k k

−k `k n1−k (1−k 2 /`)

≤ max 2` e−α2
`

19

`
k

.

(3)

By taking the derivative over ` we get that the maximum is achieved for ` such that

 k
1/(k−1)

2 ln 2
k(k − 1) 1/(k−1)
=n
.
` 1−
`
αk
The left-hand side is of the form `(1 − O(1/`)) = ` − O(1), so we can ignore the O(1/`) correction
term as it can only change the final bound by an O(1) factor. Rounding ` to the nearest integer
similarly does not change the asymptotic complexity. So, inserting the right-hand side in (3) and
simplifying, we obtain
Cn

E = O(n2

 k
1/(k−1) 

2 ln 2
1
), where C =
1−
.
αk
k

On the other hand, inserting this value of ` into the lower bound and using the inequality 1 − x ≥
2
e−x−x gives
−k k 1−k
−2k 2k 1−2k
0
E = Ω(2` e−α2 ` n −α2 ` n
) = Ω(2C n ),
where

1/(k−1)
 k
2 ln 2
C =
αk


1/(k−1) !
1
ln 2 2k ln 2
1− −
.
k αk 2
αk
√
√
For example, for k = 3, we have C ≤ 0.907/ α, C 0 ≥ 0.906/ α − 0.142/α2 .
0

References
[1] S. Aaronson and A. Ambainis. Quantum search of spatial regions. Theory of Computing,
1:47–79, 2005. quant-ph/0303041.
[2] A. Ambainis. Quantum walk algorithm for element distinctness. In Proc. 45th Annual Symp.
Foundations of Computer Science, pages 22–31, 2004. quant-ph/0311001.
[3] A. Ambainis, A. Childs, B. Reichardt, R. Špalek, and S. Zhang. Any AND-OR formula of size
n can be evaluated in time n1/2+o(1) on a quantum computer. SIAM J. Comput., 39(6):2513–
2530, 2010. quant-ph/0703015.
[4] A. Ambainis and R. de Wolf. Average-case quantum query complexity. J. Phys. A: Math.
Gen., 34:6741–6754, 2001. quant-ph/9904079.
[5] O. Angelsmark, V. Dahllöf, and P. Jonsson. Finite domain constraint satisfaction using quantum computation. In Proc. Mathematical Foundations of Computer Science 2002, pages 93–
103, 2002.
[6] P. Beame, R. Karp, T. Pitassi, and M. Saks. The efficiency of resolution and Davis–Putnam
procedures. SIAM J. Comput., 31(4):1048–1075, 2002.
[7] P. van Beek. Backtracking search algorithms. In Handbook of Constraint Programming. Elsevier, 2006.
[8] A. Belovs. Quantum walks and electric networks, 2013. arXiv:1302.3143.

20

[9] A. Belovs, A. Childs, S. Jeffery, R. Kothari, and F. Magniez. Time-efficient quantum walks
for 3-distinctness. In Proc. 40th International Conference on Automata, Languages and Programming (ICALP’13), pages 105–122, 2013.
[10] C. Bennett, E. Bernstein, G. Brassard, and U. Vazirani. Strengths and weaknesses of quantum
computing. SIAM J. Comput., 26(5):1510–1523, 1997. quant-ph/9701001.
[11] E. Bernstein and U. Vazirani. Quantum complexity theory. SIAM J. Comput., 26(5):1411–
1473, 1997.
[12] G. Brassard, P. Høyer, M. Mosca, and A. Tapp. Quantum amplitude amplification and estimation. Quantum Computation and Quantum Information: A Millennium Volume, pages
53–74, 2002. quant-ph/0005055.
[13] C. Brown and P. Purdom, Jr. An average time analysis of backtracking. SIAM J. Comput.,
10(3):583–593, 1981.
[14] N. Cerf, L. Grover, and C. Williams. Nested quantum search and structured problems. Phys.
Rev. A, 61(3):032303, 2000. quant-ph/9806078.
[15] A. Chandra, P. Raghavan, W. Ruzzo, R. Smolensky, and P. Tiwari. The electrical resistance
of a graph captures its commute and cover times. Computational Complexity, 6(4):312–340,
1996/1997.
[16] A. Childs, R. Cleve, E. Deotto, E. Farhi, S. Gutmann, and D. Spielman. Exponential algorithmic speedup by a quantum walk. In Proc. 35th Annual ACM Symp. Theory of Computing,
pages 59–68, 2003. quant-ph/0209131.
[17] R. Cleve, A. Ekert, C. Macchiavello, and M. Mosca. Quantum algorithms revisited. Proc. R.
Soc. Lond. A, 454(1969):339–354, 1998. quant-ph/9708016.
[18] S. Cocco and R. Monasson. Statistical physics analysis of the computational complexity of
solving random satisfiability problems using backtrack algorithms. Eur. J. Phys. B, 22:505–
531, 2001. cond-mat/0012191.
[19] S. Cocco and R. Monasson. Trajectories in phase diagrams, growth processes, and computational complexity: how search algorithms solve the 3-satisfiability problem. Phys. Rev. Lett.,
86(8), 2001. cond-mat/0009410.
[20] S. Cocco and R. Monasson. Exponentially hard problems are sometimes polynomial, a large
deviation analysis of search algorithms for the random satisfiability problem, and its application
to stop-and-restart solutions. Phys. Rev. E, 66(037101), 2002. cond-mat/0203012.
[21] S. Cocco and R. Monasson. Restarts and exponential acceleration of the Davis-PutnamLoveland-Logemann algorithm: A large deviation analysis of the generalized unit clause heuristic for random 3-SAT. Annals of Mathematics and Artificial Intelligence, 43(1–4):153–172,
2005. cond-mat/0206242.
[22] E. Dantsin, V. Kreinovich, and A. Wolpert. On quantum versions of record-breaking algorithms
for SAT. ACM SIGACT News, 36(4):103–108, 2005.
[23] M. Davis, G. Logemann, and D. Loveland. A machine program for theorem proving. C. ACM,
5(7):394–397, 1962.
21

[24] M. Davis and H. Putnam. A computing procedure for quantification theory. J. ACM, 7(3):201–
215, 1960.
[25] N. Eén and N. Sörensson. An extensible SAT-solver. In Proc. Theory and Applications of
Satisfiability Testing 2003, pages 502–518, 2003.
[26] E. Farhi, J. Goldstone, S. Gutmann, J. Lapan, A. Lundgren, and D. Preda. A quantum adiabatic evolution algorithm applied to random instances of an NP-complete problem. Science,
292(5516):472–475, 2001. quant-ph/0104129.
[27] E. Farhi, J. Goldstone, S. Gutmann, and M. Sipser. Quantum computation by adiabatic
evolution. Technical Report MIT-CTP-2936, MIT, 2000. quant-ph/0001106.
[28] E. Farhi and S. Gutmann. Quantum computation and decision trees. Phys. Rev. A, 58(2):915–
928, 1998. quant-ph/9706062.
[29] E. Freuder and A. Mackworth. Constraint satisfaction: an emerging paradigm. In Handbook
of Constraint Programming. Elsevier, 2006.
[30] M. Fürer. Solving NP-complete problems with quantum search. In Proc. LATIN’08, pages
784–792, 2008.
[31] C. Gomes, C. Fernández, B. Selman, and C. Bessiere. Statistical regimes across constrainedness
regions. In Principles and Practice of Constraint Programming – CP 2004, pages 32–46, 2004.
[32] C. Gomes, H. Krautz, A. Sabharwal, and B. Selman. Satisfiability solvers. In Handbook of
Knowledge Representation, volume 3 of Foundations of Artificial Intelligence, pages 89–134.
Elsevier, 2008.
[33] C. Gomes and T. Walsh. Randomness and structure. In Handbook of Constraint Programming.
Elsevier, 2006.
[34] L. Grover. Quantum mechanics helps in searching for a needle in a haystack. Phys. Rev. Lett.,
79(2):325–328, 1997. quant-ph/9706033.
[35] T. Hogg and C. Williams. The hardest constraint problems: A double phase transition.
Artificial Intelligence, 69:359–377, 1994.
[36] H. Jia and C. Moore. How much backtracking does it take to color random graphs? rigorous
results on heavy tails. In Principles and Practice of Constraint Programming – CP 2004, pages
742–746, 2004. cond-mat/0412489.
[37] A. Kitaev.
Quantum measurements and the abelian stabilizer problem,
quant-ph/9511026.

1995.

[38] D. Knuth. Estimating the efficiency of backtrack programs. Mathematics of Computation,
29(129), 1975.
[39] H. Krovi, F. Magniez, M. Ozols, and J. Roland. Quantum walks can find a marked element
on any graph. Algorithmica, pages 1–57, 2015. arXiv:1002.2419.
[40] T. Lee, R. Mittal, B. Reichardt, R. Špalek, and M. Szegedy. Quantum query complexity
of state conversion. In Proc. 52nd Annual Symp. Foundations of Computer Science, pages
344–353, 2011. arXiv:1011.3020.
22

[41] I. Lynce and J. P. Marques-Silva. An overview of backtrack search satisfiability algorithms.
Annals of Mathematics and Artificial Intelligence, 37:307–326, 2003.
[42] F. Magniez, A. Nayak, P. Richter, and M. Santha. On the hitting times of quantum versus
random walks. Algorithmica, 63(1–2):91–116, 2012. arXiv:0808.0084.
[43] F. Magniez, A. Nayak, J. Roland, and M. Santha. Search via quantum walk. SIAM J. Comput.,
40(1):142–164, 2011. quant-ph/0608026.
[44] A. Montanaro. Quantum search with advice. In Proc. 5th Conference on the Theory of Quantum Computation, Communication, and Cryptography (TQC’10), 2010. arXiv:0908.3066.
[45] P. Purdom. Backtracking and random constraint satisfaction. Annals of Mathematics and
Artificial Intelligence, 20:393–410, 1997.
[46] I. Rish and D. Frost. Statistical analysis of backtracking on inconsistent CSPs. In Principles
and Practice of Constraint Programming-CP97, pages 150–162, 1997.
[47] U. Schöning. A probabilistic algorithm for k-SAT and constraint satisfaction problems. In
Proc. 40th Annual Symp. Foundations of Computer Science, pages 410–414, 1999.
[48] B. Selman, D. Mitchell, and H. Levesque. Generating hard satisfiability problems. Artificial
Intelligence, 81(1–2):17–29, 1996.
[49] N. Shenvi, J. Kempe, and K. Whaley. Quantum random-walk search algorithm. Phys. Rev.
A, 67(5):052307, 2003. quant-ph/0210064.
[50] L. Stockmeyer. On approximation algorithms for #P. SIAM J. Comput., 14(4):849–861, 1985.
[51] M. Szegedy. Quantum speed-up of Markov chain based algorithms. In Proc. 45th Annual
Symp. Foundations of Computer Science, pages 32–41, 2004. quant-ph/0401053.
[52] A. Tulsi. Faster quantum walk algorithm for the two dimensional spatial search. Phys. Rev.
A, 78:012310, 2008. arXiv:0801.0497.
[53] G. Wang. Quantum algorithms for approximating the effective resistances in electrical networks, 2013. arXiv:1311.1851.
[54] R. Williams. Improving exhaustive search implies superpolynomial lower bounds. SIAM J.
Comput., 42(3):1218–1244, 2013.

23


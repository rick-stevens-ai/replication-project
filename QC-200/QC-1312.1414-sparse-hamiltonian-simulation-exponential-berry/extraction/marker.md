<!-- Fallback extraction: Marker not installed on this host (2026-07-05). Content is pdftotext(paper.pdf); markdown is minimally reformatted. Provenance: poppler pdftotext on paper.pdf, arXiv:1312.1414v2 -->

# Exponential improvement in precision for simulating sparse Hamiltonians

**Authors:** Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, Rolando D. Somma

**arXiv:** 1312.1414v2 (7 Oct 2014)

---

Exponential improvement in precision
for simulating sparse Hamiltonians

arXiv:1312.1414v2 [quant-ph] 7 Oct 2014

Dominic W. Berry∗ Andrew M. Childs†,‡ Richard Cleve§,‡ Robin Kothari§ Rolando D. Somma¶

Abstract
We provide a quantum algorithm for simulating the dynamics of sparse Hamiltonians with
complexity sublogarithmic in the inverse error, an exponential improvement over previous methods. Specifically, we show that a d-sparse Hamiltonian H acting on n qubits can be simulated

/ǫ) 
log2 (τ /ǫ)
for time t with precision ǫ using O τ loglog(τ
log(τ /ǫ) queries and O τ log log(τ /ǫ) n additional 2-qubit
gates, where τ = d2 kHkmax t. Unlike previous approaches based on product formulas, the query
complexity is independent of the number of qubits acted on, and for time-varying Hamiltonians,
the gate complexity is logarithmic in the norm of the derivative of the Hamiltonian. Our algorithm is based on a significantly improved simulation of the continuous- and fractional-query
models using discrete quantum queries, showing that the former models are not much more
powerful than the discrete model even for very small error. We also simplify the analysis of
this conversion, avoiding the need for a complex fault correction procedure. Our simplification
relies on a new form of “oblivious amplitude amplification” that can be applied even though
the reflection about the input state is unavailable. Finally, we prove new lower bounds showing
that our algorithms are optimal as a function of the error.

1

Introduction

Simulation of quantum mechanical systems is a major potential application of quantum computers.
Indeed, the problem of simulating Hamiltonian dynamics was the original motivation for the idea
of quantum computation [21]. Lloyd provided an explicit algorithm for simulating many realistic
quantum systems, namely those whose Hamiltonian is a sum of interactions acting nontrivially
on a small number of subsystems of limited dimension [26]. If the interactions act on at most k
subsystems, such a Hamiltonian is called k-local. Here we consider the more general problem of
simulating sparse Hamiltonians, a natural class of systems for which quantum simulation has been
widely studied. Note that k-local Hamiltonians are sparse, so algorithms for simulating sparse
Hamiltonians can be used to simulate many physical systems. Sparse Hamiltonian simulation is
also useful in quantum algorithms [1, 11, 16, 22].
A Hamiltonian is said to be d-sparse if it has at most d nonzero entries in any row or column.
In the sparse Hamiltonian simulation problem, we are given access to a d-sparse Hamiltonian H
acting on n qubits via a black box that accepts a row index i and a number j between 1 and d, and
returns the position and value of the jth nonzero entry of H in row i. Given such a black box for
H, a time t > 0 (without loss of generality), and an error parameter ǫ > 0, our task is to construct
∗

Department of Physics and Astronomy, Macquarie University
Department of Combinatorics & Optimization and Institute for Quantum Computing, University of Waterloo
‡
Canadian Institute for Advanced Research
§
Cheriton School of Computer Science and Institute for Quantum Computing, University of Waterloo
¶
Theory Division, Los Alamos National Laboratory
†

1

a circuit that performs the unitary operation e−iHt with error at most ǫ using as few queries to
H as possible. To develop practical algorithms, we would also like to upper bound the number of
additional 2-qubit gates. The time complexity of a simulation is the sum of the number of queries
and additional 2-qubit gates.
The first efficient algorithm for sparse Hamiltonian simulation was due to Aharonov and TaShma [1]. The key idea (also applied
Pη in [10]) is to use edge coloring to decompose the Hamiltonian
H into a sum of Hamiltonians j=1 Hj , where each Hj is easy to simulate. These terms are then
recombined using the Lie product formula, which states that e−iHt ≈ (e−iH1 t/r e−iH2 t/r · · · e−iHη t/r )r
for large r. This method gives query complexity O(poly(n, d)(kHkt)2 /ǫ), where k·k denotes the
spectral norm. This was later improved using high-order product formulas and more efficient
decompositions of the Hamiltonian [5, 8, 13, 14, 32]. The best algorithms of this type [13, 14] have
query complexity
 p

d2 (d + log∗ n)kHkt exp O log(dkHkt/ǫ) .
(1)
p
is asymptotThis complexity is only slightly superlinear in kHkt in that exp(O( log(dkHkt/ǫ)))
p
ically smaller than (dkHkt/ǫ)δ for any constant δ > 0; however, exp(O( log(dkHkt/ǫ))) is not
polylogarithmic in dkHkt/ǫ.
We show the following (where kHkmax denotes the largest entry of H in absolute value).
Theorem 1.1 (Sparse Hamiltonian simulation). A d-sparse Hamiltonian H acting on n qubits can
log2 (τ /ǫ) 
/ǫ) 
queries
and
O
τ
be simulated for time t within error ǫ with O τ loglog(τ
log(τ /ǫ)
log log(τ /ǫ) n additional
2
2-qubit gates, where τ := d kHkmax t ≥ 1.
Our algorithm has no query dependence on n, improved dependence on d and t, and exponentially
improved dependence on 1/ǫ. Our new approach to Hamiltonian simulation strictly improves all
previous approaches based on product formulas (e.g., [1, 5, 8, 13, 26]). An alternative Hamiltonian
simulation method based on a quantum walk [6, 9] is incomparable. That method has query com√
plexity O(dkHkmax t/ ǫ), so its performance is better in terms of kHkmax t and d but significantly
worse in terms of ǫ. Thus, while suboptimal for (say) constant-precision simulation, the results of
Theorem 1.1 currently give the best known Hamiltonian simulations as a function of ǫ.
Essentially the same approach used for Theorem 1.1 can be applied even when the Hamiltonian
is time dependent. The query complexity is unaffected by any such time dependence, except that we
take the largest max-norm of the Hamiltonian over all times (i.e., τ is redefined as τ := d2 ht with
log((τ +τ ′ )/ǫ) 
n ,
h := maxs∈[0,t] kH(s)kmax ). The number of additional 2-qubit gates is O τ log(τ /ǫ)
log log(τ /ǫ)
d
′
2
′
′
′
where τ := d h t with h := maxs∈[0,t] k ds H(s)k. This dependence on h is a dramatic improvement over previous methods for simulating time-dependent Hamiltonians using high-order product
formulas [35]. Another previous simulation method [31] also improved the dependence on h′ , but
at the cost of substantially worse dependence on t and ǫ.
While our approach applies to sparse Hamiltonians in general, it can sometimes be improved
using additional structure. In particular, consider the case of a k-local Hamiltonian acting on a
system of qubits. (A k-local Hamiltonian acting on subsystems of limited dimension is equivalent
to a k-local Hamiltonian acting on qubits with an increased value of k.) Since a term acting only
on k qubits is 2k -sparse, we can apply Theorem 1.1 with d = 2k M , where M is the total number
of local terms. However, by taking the structure of sparse Hamiltonians into account, we find an
improved simulation with τ replaced by τ̃ := 2k M kHkmax t.
The performance of our algorithm is optimal or nearly optimal as a function of some of its
parameters. A lower bound of Ω(kHkmax t) follows from the no-fast-forwarding theorem of [5],
showing that our algorithm’s dependence on kHkmax t is almost optimal. However, prior to our
2

work, there was no known ǫ-dependent lower bound, not even one ruling out algorithms with no
dependence on ǫ. We show that, surprisingly, our query dependence on ǫ in Theorem 1.1 is optimal.
Theorem 1.2 (ǫ-dependent lower bound for Hamiltonian simulation). For any ǫ > 0, there exists
a 2-sparse Hamiltonian H with kHkmax < 1 such that simulating H with precision ǫ for constant

time requires Ω loglog(1/ǫ)
log(1/ǫ) queries.

Our Hamiltonian simulation algorithm is based on a connection to the so-called fractional
quantum query model. A result of Cleve, Gottesman, Mosca, Somma, and Yonge-Mallo [17] shows
that this model can be simulated with only small overhead using standard, discrete quantum
queries. While this can be seen as a kind of Hamiltonian simulation, simulating the dynamics
of a sparse Hamiltonian appears a priori unrelated. Here we relate these tasks, giving a simple
reduction from Hamiltonian simulation to the problem of simulating (a slight generalization of) the
fractional-query model, so that improved simulations of the fractional-query model directly yield
improvements in Hamiltonian simulation.
To introduce the notion of fractional queries, recall that in the usual model of quantum query
complexity, we wish to solve a problem whose input x ∈ {0, 1}N is given by an oracle (or black box)
that can be queried to learn the bits of x. The measure of complexity, called the query complexity,
is the number of times we query the oracle. More precisely, we are given access to a unitary
gate Qx whose action on the basis states |ji|bi for all j ∈ [N ] := {1, 2, . . . , N } and b ∈ {0, 1} is
Qx |ji|bi = (−1)bxj |ji|bi. A quantum query algorithm is a quantum circuit consisting of arbitrary
x-independent unitaries and Qx gates. The query complexity of such an algorithm is the total
number of Qx gates used in the circuit.
The query model is often used to study the complexity of evaluating a classical function of x.
However, it is also natural to consider more general tasks. In order of increasing generality, such
tasks include state generation [3], state conversion [25], and implementing unitary operations [6].
Here we focus on the last of these tasks, where for each possible input x we must perform some
unitary operation Ux . Considering this task leads to a strong notion of simulation: to simulate
a given algorithm in the sense of unitary implementation, one must reproduce the entire correct
output state for every possible input state, rather than simply (say) evaluating some predicate in
one bit of the output with a fixed input state.
Since quantum mechanics is fundamentally described by the continuous dynamics of the Schrödinger equation, it is natural to ask if the query model can be made less discrete. In particular,
instead of using the gate Qx for unit cost, what if we can make half a query for half the cost? This
perspective is motivated by the idea that if Qx is performed by a Hamiltonian running for unit
time, we can stop the evolution after half the time to obtain half a query. In general we could run
this Hamiltonian for time α ∈ (0, 1] at cost α. This fractional-query model is at least as powerful
as the standard (discrete-query) model. More formally, we define the model as follows.
Definition 1 (Fractional-query model). For an n-bit string x, let Qαx act as Qαx |ji|bi = e−iπαbxj |ji|bi
for all j ∈ [N ] and b ∈ {0, 1}. An algorithm in the fractional-query model is a sequence of unitary
unitaries and αi ∈ (0, 1] for all i. The
gates Um Qαx m Um−1 · · · U1 Qαx 1 U0 , where Ui are arbitrary
P
fractional-query complexity of this algorithm is m
α
and
the total number of fractional-query
i=1 i
gates used is m.
This idea can be taken further by taking the limit as the sizes of the fractional queries approach
zero to obtain a continuous variant of the model, called the continuous-query model [20]. In this
model, we have access to a query Hamiltonian Hx acting as Hx |ji|bi = πbxj |ji|bi. Unlike the
fractional- and discrete-query models, this is not a circuit-based model of computation. In this
3

model we are allowed to evolve for time T according to the Hamiltonian given by Hx + HD (t) for
an arbitrary time-dependent driving Hamiltonian HD (t), at cost T . More precisely, the model is
defined as follows.
Definition 2 (Continuous-query model). Let Hx act as Hx |ji|bi = πbxj |ji|bi for all j ∈ [N ] and
b ∈ {0, 1}. An algorithm in the continuous-query model is specified by an arbitrary x-independent
driving Hamiltonian HD (t) for t ∈ [0, T ]. The algorithm implements the unitary operation U (T )
obtained by solving the Schrödinger equation
i


d
U (t) = Hx + HD (t) U (t)
dt

(2)

with U (0) = 1. The continuous-query complexity of this algorithm is the total evolution time, T .
Because e−iαHx = Qαx , running the Hamiltonian Hx with no driving Hamiltonian for time T = α
is equivalent to an α-fractional query. In the remainder of this work we omit the subscript x on Q
for brevity.
While initial work on the continuous-query model focused on finding analogues of known algorithms [20, 28], it has also been studied with the aim of proving lower bounds on the discrete-query
model [28]. Furthermore, the model has led to the discovery of new quantum algorithms. In
particular, Farhi, Goldstone, and Gutmann [18] discovered an algorithm with continuous-query
√
complexity O( n) for evaluating a balanced binary NAND tree with n leaves, which is optimal.
This result was later converted to the discrete-query model with the same query complexity [2, 11].
A similar conversion can be performed for any algorithm with a sufficiently well-behaved driving
Hamiltonian [9]. However, this leaves open the question of whether continuous-query algorithms
can be generically converted to discrete-query algorithms with the same query complexity. This was
that approximates a T -query continuous-query
almost resolved by [17], which gave an algorithm

algorithm to bounded error with O T logloglogT T discrete queries. This algorithm can be made time
efficient [7] (informally, the number of additional 2-qubit gates is close to the query complexity).
However,
to approximate a continuous-query algorithm to precision ǫ, the algorithm of [17] uses
T log T 
queries.
Ideally we would like the dependence on ǫ to be polylogarithmic, instead of
O 1ǫ log
log T
polynomial, in 1/ǫ. For example, such behavior would be desirable when using a fractional-query
algorithm as a subroutine. Here we present a significantly improved and simplified simulation of
the continuous- and fractional-query models. In particular, we show the following.
Theorem 1.3 (Continuous-query simulation). An algorithm with continuous- or fractional-query
/ǫ) 
complexity T ≥ 1 can be simulated with error at most ǫ with O T loglog(T
log(T /ǫ) queries. For continuousquery simulation, if there is a circuit using at most g gates that implements the time evolution due
to HD (t) between any two times t1 and t2 with precision ǫ/T , then the number of additional 2-qubit

R
/ǫ)
:= T1 0T kHD (t)kdt.
gates for the simulation is O T loglog(T
log(T /ǫ) [g + log(h̄T /ǫ)] , where h̄

Since the continuous-query model is at least as powerful as the discrete-query model, a discrete
simulation must use Ω(T ) queries, showing our dependence on T is close to optimal. However, as for
the problem of Hamiltonian simulation, there was previously no ǫ-dependent
lower bound. Along

queries
for
a continuous-query
the lines of Theorem 1.2, we show a lower bound of Ω loglog(1/ǫ)
log(1/ǫ)
algorithm with T = O(1) (Theorem 6.1), so the dependence of our simulation on ǫ is optimal.
For the problem of evaluating a classical function of a black-box input, an approach based on an
invariant called the γ2 norm shows that the continuous-query complexity is at most a constant factor
smaller than the discrete-query complexity for a bounded-error simulation [25]. However, it remains
unclear whether the algorithm can be made time efficient and whether the unitary dynamics of a
4

continuous-query algorithm can be simulated (even with bounded error) using O(T ) queries. Such a
result does hold for state conversion, but its dependence on error is quadratic [25]. More generally,
the optimal tradeoff between T and ǫ for simulation of continuous-query algorithms using discrete
queries—and for simulation of Hamiltonian dynamics—remains open (with or without conditions
on the time complexity).
The remainder of this article is organized as follows. In Section 2 we give a high-level overview
of the techniques used in our results. In Section 3 we describe our simulation of the continuous- and
fractional-query models using discrete queries. In Section 4 we apply these results to Hamiltonian
simulation. In Section 5 we analyze the time complexity of our algorithms, and in Section 6 we
prove ǫ-dependent lower bounds showing optimality of their error dependence. We conclude in
Section 7 with a brief discussion of some open questions. In Appendix A, we provide some proofs
of known results for the sake of completeness.

2

High-level overview of techniques

We begin by proving Theorem 1.3, our improved simulation of continuous- and fractional-query
algorithms. Then we prove Theorem 1.1 by reducing an instance of a sparse Hamiltonian simulation problem to an instance of a fractional-query algorithm, which can then be simulated via
Theorem 1.3. We prove Theorem 1.2 using ideas from the no-fast-forwarding theorem from [5] and
properties of the unbounded-error quantum query complexity of the parity function.
We now sketch the approach for each of the main theorems, highlighting the novel ideas.

2.1

Continuous-query simulation (Theorem 1.3)

First consider the simulation of fractional queries using discrete queries. We show that an algorithm with constant
fractional-query complexity can be simulated in the discrete-query model

queries
(Lemma 3.2). The claimed upper bound for simulating a fractionalusing O loglog(1/ǫ)
log(1/ǫ)
query algorithm with query complexity T follows easily by breaking the algorithm into pieces
with constant fractional-query complexity. Since the continuous- and fractional-query models are
equivalent (Theorem 3.1), the result for the continuous-query model (Theorem 1.3) follows.
We prove Lemma 3.2 in two steps. Let the unitary performed by the constant-query fractionalquery algorithm be V and let the (unknown) state it acts on be |ψi. We would like to create the state
√
V |ψi up to error ǫ. First we construct a circuit Ũ that performs V with amplitude p up to error ǫ,
√
√
in the sense that Ũ is within error ǫ of a unitary U that maps |0m i|ψi to p|0m iV |ψi + 1 − p|Φ⊥ i
for some constant p and some state |Φ⊥ i with (|0m ih0m | ⊗ 1)|Φ⊥ i = 0. The existence of such a Ũ

that makes O loglog(1/ǫ)
log(1/ǫ) queries was shown by [17]. Their strategy is to measure the first m qubits
and obtain V |ψi with constant probability. If the measurement fails, they recover the original state
|ψi from |Φ⊥ i using a fault-correction procedure, which is itself probabilistic and occasionally fails,
requiring a recursive correction algorithm to remove all faults. The time-efficient implementation
of this recursive fault-correction procedure [7] is cumbersome.
Our alternative approach uses Ũ to deterministically create V |ψi without measurements. We
show in general how to create V |ψi with a constant number of applications of Ũ when p is a
constant. To do this, we introduce a notion of “oblivious amplitude amplification” that can have
the same performance as standard amplitude amplification, but that can be applied even when the
reflection about the input state is unavailable. This idea, which is inspired by the in-place QMA
amplification procedure of Marriott and Watrous [27], is a general result that can potentially be
applied in other contexts.
5

Most of the algorithm is easily made time efficient, except the preparation of a certain quantum
state. However, this state can be prepared efficiently [7] and the result follows.

2.2

Hamiltonian simulation reduction (Theorem 1.1)

Next we describe the main ideas of our Hamiltonian simulation algorithm. We remove the dependence of the query cost on n with a simple trick involving local edge coloring of bipartite
graphs. This strategy is quite general and can be used to remove n-dependence from several known
Hamiltonian simulation algorithms. The improved dependence on ǫ results from our algorithm for
simulating the fractional-query model in the discrete-query model (Theorem 1.3).
As mentioned previously, we reduce Hamiltonian simulation to a generalization of the task
of simulating the fractional-query model. Examining the basic Lie product formula e−iHt ≈
(e−iH1 t/r e−iH2 t/r · · · e−iHη t/r )r , we see that if Qj := e−iHj were query oracles, this would be a
fractional-query algorithm using multiple oracles Qj for time t each. (Note that because the query
complexity of the simulation depends only on the total time over which fractional queries are applied rather than the total number of fractional queries, there is no advantage to using higher-order
product formulas.) We reduce a fractional-query algorithm that calls each of η different query
oracles for time t to a fractional-query algorithm that uses query time ηt with a single query oracle
that can perform any Qj . Thus it suffices to decompose the given Hamiltonian H into a sum of
Hamiltonians for which the matrices Qj can be viewed as query oracles in Theorem 1.3. We show
such a decomposition (Lemma 4.3) that yields that stated upper bound. This algorithm can be
made time efficient since it is essentially a reduction to continuous-query simulation.

2.3

Lower bounds (Theorem 1.2 and Theorem 6.1)

Finally, we prove lower bounds showing optimality of our algorithms as a function of ǫ (Theorem 1.2
and Theorem 6.1). The main idea behind both lower bounds is to show a Hamiltonian whose exact
simulation for any time t > 0 allows us to compute the parity of a string with unbounded error,
which is as hard as computing parity exactly, requiring Ω(n) queries [4, 19]. Because one must
apply the Hamiltonian Ω(n) times to have nonzero amplitude on a state that encodes the parity,
the evolution for constant time only produces the answer at nth order in the Taylor series, so
the parity is only successfully computed with probability Θ(1/n!). To obtain an unbounded-error
algorithm for parity, one must simulate this evolution accurately enough to resolve such asmall
success probability. Thus we must have ǫ = O(1/n!), giving the lower bound of Ω loglog(1/ǫ)
log(1/ǫ) .

3

From continuous to discrete queries

In this section we present our improved simulation of continuous or fractional queries in the conventional discrete query model. The main result of this section is Lemma 3.8, which establishes the
query complexity claimed in Theorem 1.3. The time-complexity part of Theorem 1.3 is established
in Section 5.
For concreteness, we quantify the distance between unitaries U and V with the function kU − V k
and the distance between states |ψi and |φi with the function k|ψi − |φik. As the error ultimately
appears inside a logarithm, the precise choice of distance measure is not significant.
We begin by recalling the equivalence of the continuous- and fractional-query models for any
error ǫ > 0. An explicit simulation of the continuous-query model by the fractional-query model
was provided by [17]; the proof is a straightforward application of a result of [23]. The other

6

direction is apparently folklore (e.g., both directions are implicitly assumed in [28]); we provide a
short proof in Appendix A.1 for completeness.
Theorem 3.1 (Equivalence of continuous- and fractional-query models). For any ǫ > 0, any
algorithm with continuous-query complexity T can be implemented with fractional-query
R T complexity
T with error at most ǫ and m = O(h̄T 2 /ǫ) fractional-query gates, where h̄ := T1 0 kHD (t)k dt
is the average norm of the driving Hamiltonian. Conversely, any algorithm with fractional-query
complexity T can be implemented with continuous-query complexity T with error at most ǫ.
Since the two models are equivalent, it suffices to convert a fractional-query algorithm to a
discrete-query algorithm. We start with a fractional-query algorithm that makes at most 1 query.
The result for multiple queries (Lemma 3.8) follows straightforwardly.
Lemma 3.2. Any algorithm in
 the fractional-query model with query complexity at most 1 can be
implemented with O loglog(1/ǫ)
log(1/ǫ) queries in the discrete-query model with error at most ǫ.

The construction of the algorithm in this main lemma can be viewed in two steps. First,
we show how to unitarily construct a superposition of the required state along with a label in
state 0m+1 and another state whose label is orthogonal. The construction is similar to that in
[7, 17]; the main difference is that we do not measure the state of the label. (This step is shown
in the sequence Lemma 3.3, Lemma 3.4, and Lemma 3.5.) Then, in the second step, rather than
performing a fault-correction procedure upon seeing a measurement outcome other than 0m+1 , we
perform the underlying unitary operation in the first step three times (one of which is backwards)
in conjunction with certain reflections to arrive at the required state. This step can be viewed as
applying a generalization of amplitude amplification that is shown in Lemma 3.6.
|0i Rα

•

..
.

Q

|ψi

P

Rα
..
.

Figure 1: The fractional-query gadget. After performing the controlled-Q operation on the target state |ψi,
the operation Qα is performed with amplitude depending on α.

The first step of the construction uses the fractional-query gadget [17, Section II.B] shown in
Figure 1. This gadget behaves as follows, as we show in Appendix A.2.
Lemma 3.3 (Gadget Lemma [17]). Let Q
be a√ unitary
matrix with eigenvalues ±1; let α ∈ [0, 1].

√
c
s
1
The circuit in Figure 1, with Rα := √c+s √s −√c and P := ( 10 0i ), performs the map
|0i|ψi 7→

√

qα |0ie−iπα/2 Qα |ψi +

p

1 − qα |1i|φi

(3)

for some state |φi, where c := cos(πα/2), s := sin(πα/2), qα := 1/(c + s)2 = 1/(1 + sin(πα)), and
Qα = 21 (1 + Q) + e−iπα 12 (1 − Q) = e−iπα/2 (c1 + isQ).
While the proof in Appendix A.2 shows that |φi = e−iπ/4 Q−1/2 |ψi, we do not use this fact in
our analysis, in contrast to previous approaches [7, 17].
Note that while we have defined the fractional-query model to use fractions α ∈ (0, 1], a similar
simulation could be applied if we allowed negative fractional-time evolutions with α ∈ [−1, 1]. In
7

|0i
|0i

Rα1

•

..
.
|0i
|ψi

Rαm
..
.

···

Υ

···

Rα1 P

..

..
.

.

···
U0

Q

···
..
.

U1

Um−1

•

Rαm P

Q

Um

···
Figure 2: A segment to implement the fractional-query algorithm. The segment consists of many concatneated applications of the fractional-query gadget, interspersed with x-independent unitaries Ui . The state
preparation is indicated in the dotted box, and the main operation is performed by the circuit in the dashed
box. The additional ancilla at the top is introduced to reduce the amplitude for performing the correct
operation to exactly 1/2.
0
particular, we could define s = sin(π|α|/2), P = ( 10 i sgn(α)
) and carry through an analogous analysis.
However, for simplicity, we restrict our attention to the model with only positive fractional time
evolutions.
We now collect the gadgets into segments as shown in Figure 2 and show that, with an appropriate choice of parameters, a segment implements a fractional-query algorithm with constant
query complexity with amplitude 1/2. This specific choice facilitates one-step exact oblivious amplitude amplification. Other than this choice of constant, this lemma is the same as in [17]. For
completeness, we provide a proof in Appendix A.2.

Lemma 3.4 (Segment Lemma). Let V be a unitary implementable by a fractional-query algorithm
α1
αm
with query complexity at most
Pm 1/5, i.e., there exists an m such that V = Um Q Um−1 · · · U1 Q U0
with αi ≥ 0 for all i and i=1 αi ≤ 1/5. Let P and Rα be as in Lemma 3.3. Then there exists a
unitary Υ on the additional ancilla such that the circuit in Figure 2 performs the map
√
3 ⊥
1 m+1 iϑ
m+1
ie V |ψi +
|Φ i
(4)
|0
i|ψi 7→ |0
2
2
for some state |Φ⊥ i satisfying (|0m+1 ih0m+1 | ⊗ 1)|Φ⊥ i = 0 and some ϑ ∈ [0, 2π).
Although the segment in Figure 2 makes m queries, it is possible to approximate this segment
within precision ǫ using only O( loglog(1/ǫ)
log(1/ǫ) ) queries. To get some intuition for why this is possible,
note that the state on the control registers decides how many queries are performed. For example,
if all the control registers were set to |0i when the controlled-Q gates act, then no queries would
be performed, even though the circuit contains m query gates. In general, the number of queries
performed when the control registers are set to |b1 , b2 , . . . , bm i is the Hamming weight of b. In
Figure 2, the state of the control registers has very little overlap with high-weight states, so we can
approximate that state with one that has no overlap with high-weight states. We then show how
to rearrange such a circuit to obtain a new circuit that uses very few query gates.
This lemma follows the same proof structure as Section II.C of [17], but is more general since
we do not restrict all the fractional queries to have the same value of α. This change requires us
to use a version of the Chernoff bound for independent (but not necessarily identically distributed)
random variables instead of the one used in [17]. The lemma is proved in Appendix A.2.
8

Lemma 3.5 (Approximate Segment Lemma). Let V be a unitary implementable by a fractionalquery algorithm with query complexity at most 1/5. Then for any ǫ > 0, there exists a unitary

quantum circuit that makes O loglog(1/ǫ)
log(1/ǫ) discrete queries and, within error ǫ, performs a unitary
U acting as
√
3 ⊥
1 m+1 iϑ
m+1
ie V |ψi +
|Φ i
(5)
U |0
i|ψi = |0
2
2
for some state |Φ⊥ i satisfying (|0m+1 ih0m+1 | ⊗ 1)|Φ⊥ i = 0 and some ϑ ∈ [0, 2π).
Up to this point our proof is similar to previous approaches [7, 17]. In those previous approaches,
the map of Lemma 3.5 was used to probabilistically create the desired state by measuring the first
m + 1 qubits. With constant probability we obtain the desired state, but in the other case we have
a fault and have to recover the original input state. This recovery stage required a fault-correction
procedure that is difficult to analyze and considerably harder to make time efficient.
We avoid these difficulties by introducing oblivious amplitude amplification. Given a unitary
U that implements another unitary V with some amplitude (in a certain precise sense), this idea
allows one to use a version of amplitude amplification to give a better implementation of V . In
particular, as in amplitude amplification, if the amplitude for implementing V is known, we can
exactly perform V .
In standard amplitude amplification, to amplify the “good” part of a state, we need to be able
to reflect about the state itself and the projector onto the good subspace. While the latter is easy
in our application, we cannot reflect about the unknown input state. Nevertheless, we show the
following.
Lemma 3.6 (Oblivious amplitude amplification). Let U and V be unitary matrices on µ + n qubits
and n qubits, respectively, and let θ ∈ (0, π/2). Suppose that for any n-qubit state |ψi,
U |0µ i|ψi = sin(θ)|0µ iV |ψi + cos(θ)|Φ⊥ i,

(6)

where |Φ⊥ i is an (µ + n)-qubit state that depends on |ψi and satisfies Π|Φ⊥ i = 0, where Π :=
|0µ ih0µ | ⊗ 1. Let R := 2Π − 1 and S := −U RU † R. Then for any ℓ ∈ Z,


S ℓ U |0µ i|ψi = sin (2ℓ + 1)θ |0µ iV |ψi + cos (2ℓ + 1)θ |Φ⊥ i.
(7)

Note that R is not the reflection about the initial state, so Lemma 3.6 does not follow from
amplitude amplification alone. However, in the context described in the lemma, it suffices to use a
different reflection.
The motivation for oblivious amplitude amplification comes from work of Marriott and Watrous
on in-place amplification of QMA [27] (see also related work on quantum rewinding for zeroknowledge proofs [33] and on using amplitude amplification to obtain a quadratic improvement
[30]). Specifically, the following technical lemma shows that amplitude amplification remains in a
certain 2-dimensional subspace in which it is possible to perform the appropriate reflections.

Lemma 3.7 (2D Subspace Lemma). Let U and V be unitary matrices on µ + n qubits and n qubits,
respectively, and let p ∈ (0, 1). Suppose that for any n-qubit state |ψi,
p
√
U |0µ i|ψi = p|0µ iV |ψi + 1 − p|Φ⊥ i,
(8)
where |Φ⊥ i is an (µ + n)-qubit state that depends on |ψi and satisfies Π|Φ⊥ i = 0, where Π :=
|0µ ih0µ | ⊗ 1. Then the state |Ψ⊥ i defined by the equation
p
√
U |Ψ⊥ i := 1 − p|0µ iV |ψi − p|Φ⊥ i
(9)
is orthogonal to |Ψi := |0µ i|ψi and satisfies Π|Ψ⊥ i = 0.
9

Proof. For any |ψi, let |Φi := |0µ iV |ψi. Then for all |ψi, we have
p
√
U |Ψi = p|Φi + 1 − p|Φ⊥ i
p
√
U |Ψ⊥ i = 1 − p|Φi − p|Φ⊥ i,

(10)
(11)

where Π|Φ⊥ i = 0. By taking the inner product of these two equations, we get hΨ|Ψ⊥ i = 0. The
lemma asserts that not only is |Ψ⊥ i orthogonal to |Ψi, but also Π|Ψ⊥ i = 0.
To show this, consider the operator
Q := (h0µ | ⊗ 1)U † ΠU (|0µ i ⊗ 1).

(12)

For any state |ψi,

p
√
√
hψ|Q|ψi = kΠU |0µ i|ψik2 = kΠ( p|Φi + 1 − p|Φ⊥ i)k2 = k p|Φik2 = p.

In particular, this holds for a basis of eigenvectors of Q, so Q = p1.
Thus for any |ψi, we have

p|ψi = Q|ψi = (h0µ | ⊗ 1)U † ΠU (|0µ i ⊗ 1)|ψi = (h0µ | ⊗ 1)U † ΠU |Ψi =
From (10) and (11) we get U † |Φi =
we get
p|ψi =
This gives us

p

√

√

p(h0µ | ⊗ 1)U † |Φi.

(13)

(14)

√
p|Ψi + 1 − p|Ψ⊥ i. Plugging this into the previous equation,

p
p
√
√
p(h0µ | ⊗ 1)( p|Ψi + 1 − p|Ψ⊥ i) = p|ψi + p(1 − p)(h0µ | ⊗ 1)|Ψ⊥ i.

(15)

p(1 − p)(h0µ | ⊗ 1)|Ψ⊥ i = 0. Since p ∈ (0, 1), this implies Π|Ψ⊥ i = 0.

Note that this fact can also be viewed as a consequence of Jordan’s Lemma [24], which decomposes the space into a direct sum of 1- and 2-dimensional subspaces that are invariant under
the projectors Π and U † ΠU . In this decomposition, Π and U † ΠU are rank-1 projectors within
each 2-dimensional subspace. Let |0i|ψi i denote the eigenvalue-1 eigenvector of Π within the ith 2√
dimensional subspace Si . Since Si is invariant under U † ΠU , the state U † ΠU |0i|ψi i = pU † |0iV |ψi i
√
√
⊥
belongs to Si . Let |Φ⊥
i be such that |0i|ψi i = U † ( p|0iV |ψi i + 1 − p|Φ⊥
i i). Then |Ψi i :=
√
√i
⊥
†
†
U ( 1 − p|0iV |ψi i − p|Φi i) is in Si , since it is a linear combination of |0i|ψi i and U ΠU |0i|ψi i.
However, |Ψ⊥
i i is orthogonal to |0i|ψi i and is therefore an eigenvalue-0 eigenvector of Π, since Π
is a rank-1 projector in Si . Thus for each i, |ψi i and |Ψ⊥
i i satisfy the conditions of the lemma.
We claim that the number of 2-dimensional subspaces (and hence the number of states |ψi i) is 2n .
There are at most 2n such subspaces since Π has rank 2n and is rank-1 in each subspace. There
also must be at least 2n 2-dimensional subspaces, since otherwise there would be a state |0i|ψi
that is in a 1-dimensional subspace, i.e., is invariant under both Π and U † ΠU . This is not possible
√
because U † ΠU acting on |0i|ψi yields pU † |0iV |ψi, which is a subnormalized state since p < 1.
Finally, since there are 2n linearly independent |ψi i, an arbitrary state |ψi can be written as a
linear combination of |ψi i, and the result follows.
With the help of Lemma 3.7 we can prove Lemma 3.6.
Proof of Lemma 3.6. Since Lemma 3.7 shows that the evolution occurs within a two-dimensional
subspace (or its image under U ), the remaining analysis is essentially the same as in standard
amplitude amplification. For any |ψi, we define |Ψi := |0µ i|ψi and |Φi := |0µ iV |ψi, so that
U |Ψi = sin(θ)|Φi + cos(θ)|Φ⊥ i,
10

(16)

where θ ∈ (0, π/2) is such that

√

p = sin(θ). We also define |Ψ⊥ i through the equation

U |Ψ⊥ i := cos(θ)|Φi − sin(θ)|Φ⊥ i.

(17)

By Lemma 3.7, we know that Π|Ψ⊥ i = 0. Using these two equations, we have
U † |Φi = sin(θ)|Ψi + cos(θ)|Ψ⊥ i

U † |Φ⊥ i = cos(θ)|Ψi − sin(θ)|Ψ⊥ i.

(18)
(19)

Then a straightforward calculation gives
S|Φi = −U RU † |Φi

= −U R(sin(θ)|Ψi + cos(θ)|Ψ⊥ i)

= −U (sin(θ)|Ψi − cos(θ)|Ψ⊥ i)

= cos2 (θ) − sin2 (θ) |Φi − 2 cos(θ) sin(θ)|Φ⊥ i
= cos(2θ)|Φi − sin(2θ)|Φ⊥ i.

(20)

Similarly,
S|Φ⊥ i = U RU † |Φ⊥ i

= U R(cos(θ)|Ψi − sin(θ)|Ψ⊥ i)

= U (cos(θ)|Ψi + sin(θ)|Ψ⊥ i)


= 2 cos(θ) sin(θ)|Φi + cos2 (θ) − sin2 (θ) |Φ⊥ i
= sin(2θ)|Φi + cos(2θ)|Φ⊥ i.

(21)

Thus we see that S acts as a rotation by 2θ in the subspace span{|Φi, |Φ⊥ i}, and the result
follows.
We are now ready to complete the proof of Lemma 3.2 using Lemma 3.5 and Lemma 3.6.
Proof of Lemma 3.2. We are given a fractional-query algorithm that makes at most 1 query. This
can be split into 5 steps that make at most 1/5 queries each in the fractional-query model. We
perform the analysis for these steps of size 1/5; the difference is only a constant factor that does not
affect the asymptotics. We convert this fractional-query algorithm into a discrete-query algorithm
with some error.
From Lemma 3.5, weknow that for any such fractional-query algorithm V , there is an algorithm
m+1 i|ψi to a state that is at most ǫ
that makes O loglog(1/ǫ)
log(1/ǫ) discrete queries and maps the state |0
√

far from 12 |0m+1 ieiϑ V |ψi + 23 |Φi, for some state |Φi that satisfies (|0m+1 ih0m+1 | ⊗ 1)|Φi = 0 and
some ϑ ∈ [0, 2π). We wish to perform the unitary V on the input state |ψi approximately. √
The unitary operation U defined in Lemma 3.5 maps |0m+1 i|ψi 7→ 21 |0m+1 ieiϑ V |ψi + 23 |Φi.
The operation U satisfies the conditions of Lemma 3.6 with µ = m + 1 and sin2 (θ) = 1/4. Thus a
single application of S (using three applications of U ) would produce the state V |ψi exactly.
While we cannot necessarily perform U , using Lemma 3.5 we can perform another unitary
operation Ũ that is within error ǫ/3 of U . Since we only perform the unitary three times, we obtain
a state ǫ-close to V |ψi when we use Ũ instead of U .

11

By straightforwardly concatenating such simulations with sufficiently small error, we obtain
simulations for longer times. This establishes the following lemma, which is the query-complexity
part of Theorem 1.3.
Lemma 3.8. An algorithm with continuousor fractional-query complexity T ≥ 1 can be simulated
log(T /ǫ) 
queries.
with error at most ǫ with O T log log(T /ǫ)

Proof. Given an algorithm that runs for time T in the continuous-query model, we can convert
it to an algorithm with fractional-query complexity T with error at most ǫ/2 using Theorem 3.1.
Given a fractional-query algorithm that makes T queries, we can divide it into ⌈T ⌉ pieces that
make at most 1 query each and invoke Lemma 3.2 with error ǫ/2⌈T ⌉ to obtain ⌈T ⌉ discrete-query
⌉/ǫ) 
algorithms, each of which makes O loglog(⌈T
log(⌈T ⌉/ǫ) queries. When run sequentially on the input state,
they yield an output that is ǫ/2-close to the correct output (by subadditivity of error). Thus the
final state has error at most ǫ.

4

Hamiltonian simulation

We now apply the results of the previous section to give improved algorithms for simulating sparse
Hamiltonians. The main result of this section is the reduction from an instance of the sparse
Hamiltonian simulation problem to a fractional-query algorithm, which establishes Lemma 4.5, the
query-complexity part of Theorem 1.1. The time-complexity part of Theorem 1.1 is established in
Section 5.
To see the connection between the fractional-query model and Hamiltonian simulation, consider
the example of a Hamiltonian H = H1 + H2 , where H1 and H2 have eigenvalues 0 and π, so that
e−iH1 and e−iH2 have eigenvalues ±1. From the Lie product formula, we have e−i(H1 +H2 )T ≈
(e−iH1 T /r e−iH2 T /r )r for large r. If we think of H1 and H2 as query Hamiltonians, this is a
fractional-query algorithm
that makes T queries to each Hamiltonian. We might therefore ex/ǫ) 
discrete
queries to e−iH1 and e−iH2 suffice to implement e−i(H1 +H2 )T to
pect that O T loglog(T
log(T /ǫ)
precision ǫ. Here we do this by generalizing the results of the previous section to allow multiple
fractional-query oracles.
For a set Q = {Q1 , . . . , Qη } of unitary matrices with eigenvalues ±1, we say U is a fractionalquery algorithm over Q with cost T if U can be written as Uλ Qαiλλ Uλ−1 · · · U1 Qαi11 U0 , where 0 <
P
αi ≤ 1, λi=1 αi = T , and ij ∈ [η] for all j ∈ [λ].
Theorem 4.1 (Multiple-query model). Let Q = {Q1 , . . . , Qη } be a set of unitaries
with eigenvalues
P
±1. Let U be a fractional-query algorithm over Q with cost T . Let Q := ηj=1 |jihj| ⊗ Qj . Then
/ǫ) 
U can be implemented by a circuit that makes O T loglog(T
log(T /ǫ) queries to Q with error at most ǫ.

Proof. We prove this by reduction to Theorem 1.3.
P We know that U can be written in the form
U = Uλ Qαiλλ Uλ−1 · · · U1 Qαi11 U0 , where 0 < αi ≤ 1, λi=1 αi = T , and ij ∈ [η] for all j ∈ [λ].
We first express U as a fractional-query algorithm over Q with cost T . To do this, we add an
extra control register to the original circuit for U . This register holds the index ij of the next query
to be performed. We start with this register initialized to |0i. Let V0 be any unitary that maps
|0i to |i1 i. The action of Qαi11 U0 on any state |ψi is the same as the action of Qα1 (V0 ⊗ U0 ) on the
second register of |0i|ψi. Similarly, for all j ∈ [λ], let Vj be any unitary that maps |ij i to |ij+1 i,
where iλ+1 := 0. Thus the circuit (Vλ ⊗ Uλ )Qαλ (Vλ−1 ⊗ Uλ−1 ) · · · (V1 ⊗ U1 )Qα1 (V0 ⊗ U0 ) maps |0i|ψi
to |0iU |ψi.
This construction gives a fractional-query algorithm with fractional-query complexity T given
oracle access to Q. Since Q has eigenvalues ±1, we can invoke Theorem 1.3 to give a discrete-query
12

/ǫ) 
algorithm that makes O T loglog(T
log(T /ǫ) queries to Q and performs U up to error ǫ. Theorem 1.3
assumes the queries are diagonal in the computational basis, whereas here we assume only that
Q has eigenvalues ±1. However, these two scenarios are equivalent since the target system can
be considered in a basis where Q is diagonal. Therefore Theorem 1.3 applies to the slightly more
general scenario considered here.

This theorem allows us to simulate a Hamiltonian H = H1 + · · · + Hη for time t using resources
that scale only slightly superlinearly in ηt, provided each Hj has eigenvalues 0 and π (or more
generally, by rescaling, provided each Hj has the same two eigenvalues). For any ǫ > 0, there is a
sufficiently large r so that e−iHt is ǫ-close to (e−iH1 t/r · · · e−iHη t/r )r , which is of the form required by
Theorem 4.1 if e−iHj has eigenvalues ±1. Since ke−iHt − (e−iH1 t/r · · · e−iHη t/r )r k = O((η h̄t)2 /r),
where h̄ := maxj kHj k [5], choosing r = Ω((η h̄t)2 /ǫ) is sufficient to achieve an ǫ-approximation.
Since our Hamiltonians Hj have constant norm, we have h̄ = O(1) and get the following corollary.
Pη
Corollary 4.2. For a Hamiltonian H =
j=1 Hj , where Hj has eigenvalues 0 and π for all
P
−iH
j . The unitary e−iHt can be implemented by a fractional-query
j ∈ [η], define Q := j |jihj| ⊗ e
algorithm over Q, up to error ǫ, with query complexity τ = ηt and O(η 3 t2 /ǫ) fractional-query gates.
/ǫ) 
Thus e−iHt can be implemented up to error ǫ by a circuit with O τ loglog(τ
log(τ /ǫ) invocations of Q.

To simulate arbitrary sparse Hamiltonians, we decompose them into Hamiltonians with this
property. To do this we first decompose the Hamiltonian into a sum of 1-sparse Hamiltonians (with
at most 1 nonzero entry in any row or column). Second, we decompose 1-sparse Hamiltonians into
Hamiltonians of the required form.
Lemma 4.3. For any 1-sparse Hamiltonian G and precision
γ > √
0, there exist O(kGkmax /γ)
P
Hamiltonians Gj with eigenvalues ±1 such that kG − γ j Gj kmax ≤ 2γ.

Proof. First we decompose the Hamiltonian G as G = GX + iGY + GZ , where GX contains the
off-diagonal real terms, iGY contains the off-diagonal imaginary terms, and GZ contains the ondiagonal real terms. Next, for each of Gξ for ξ ∈ {X, Y, Z}, we construct an approximation G̃ξ
with each entry rounded off to the closest multiple of 2γ. Since each entry of G̃ξ is at most γ away
from the corresponding entry
√ in Gξ , we have kGξ − G̃ξ kmax ≤ γ. Denoting G̃ = G̃X + iG̃Y + G̃Z ,
this implies kG − G̃kmax ≤ 2γ.
Next, we take C ξ := G̃ξ /γ, so kC ξ kmax = ⌈kGξ kmax /γ⌉ ≤ ⌈kGkmax /γ⌉. We can then decompose
each 1-sparse matrix C ξ into kC ξ kmax matrices, each of which is 1-sparse and has entries from
ξ
{−2, 0, 2}. If Cjk
is 2p, then the first |p| matrices in the decomposition have a 2 for p > 0 (or −2
if p < 0) at the (j, k) entry, and the rest have 0. More explicitly, we define

ξ
if Cjk
≥ 2ℓ > 0

2
ξ,ℓ
ξ
Cjk := −2 if Cjk ≤ −2ℓ < 0


0
otherwise

(22)

for ξ ∈ {X, Y, Z} and ℓ ∈ [kC ξ kmax ]. This gives a decomposition into at most 3⌈kGkmax /γ⌉ terms
with eigenvalues in {−2, 0, 2}.
To obtain matrices with eigenvalues ±1, we perform one more step to remove the 0 eigenvalues.
We divide each C ξ,ℓ into two copies, C ξ,ℓ,+ and C ξ,ℓ,−. For any column where C ξ,ℓ is all zero, the
corresponding diagonal element of C ξ,ℓ,+ is +1 (if ξ ∈ {X, Z}) or +i (if ξ = Y ) and the diagonal
ξ,ℓ,+
ξ,ℓ,−
ξ,ℓ
element of C ξ,ℓ,− is −1 (if ξ ∈ {X, Z}) or −i (if ξ = Y ). Otherwise, we let Cjk
= Cjk
= Cjk
/2.
13

Thus C ξ,ℓ = C ξ,ℓ,+ + C ξ,ℓ,−. Moreover, each column of C ξ,ℓ,± has exactly one nonzero entry, which
is ±1 (or ±i on the diagonal of C Y,ℓ,±). P
X,ℓ,± + iC Y,ℓ,± + C Z,ℓ,± ) in which each term has
This gives a decomposition G̃/γ =
ℓ,± (C
eigenvalues ±1. The decomposition contains at most 6⌈kGkmax /γ⌉ = O(kGkmax /γ) terms.
Lemma 4.3 gives a decomposition of the required form as the eigenvalues can be adjusted to 0
and π by adding the identity matrix and multiplying by π/2.
It remains to decompose a sparse Hamiltonian into 1-sparse Hamiltonians. Known results decompose a d-sparse Hamiltonian H into a sum of O(d2 ) 1-sparse Hamiltonians [5], but simulating
one query to a 1-sparse Hamiltonian requires O(log∗ n) queries to the oracle for H. We present a
simplified decomposition theorem that decomposes a d-sparse Hamiltonian into d2 1-sparse Hamiltonians. A query to the individual 1-sparse Hamiltonians can be performed using O(1) queries to
the original Hamiltonian, removing the log∗ n factor.
P2
Lemma 4.4. If H is a d-sparse Hamiltonian, there exists a decomposition H = dj=1 Hj where
each Hj is 1-sparse and a query to any Hj can be simulated with O(1) queries to H.
Proof. The new ingredient in our proof is to assume that the graph of H is bipartite. (Here the
graph of H has a vertex for each basis state and an edge between two vertices if the corresponding
entry of H is nonzero.) This is without loss of generality because we can simulate the Hamiltonian
σx ⊗ H instead, which is indeed bipartite and has the same sparsity as H. From a simulation of
σx ⊗ H, we can recover a simulation of H using the identity e−i(σx ⊗H)t |+i|ψi = |+ie−iHt |ψi.
Now we decompose a bipartite d-sparse Hamiltonian into a sum of d2 terms. To do this, we
give an edge coloring of the graph of H (i.e., an assignment of colors to the edges so that no two
edges incident on the same vertex have the same color). Given such a coloring with d2 colors, the
Hamiltonian Hj formed by only considering edges with color j is 1-sparse.
We use the following simple coloring. For any pair of adjacent vertices u and v, let r(u, v) denote
the rank of v in u’s neighbor list, i.e., the position occupied by v in a sorted list of u’s neighbors.
This is a number between 1 and d. Let the color of the edge (u, v), where u comes from the left
part of the bipartition and v comes from the right, be the ordered pair (r(u, v), r(v, u)). This is a
valid coloring since if (u, v) and (u, w) have the same color, then in particular the first component
of the ordered pair is the same, so r(u, v) = r(u, w) implies v = w. A similar argument handles the
case where the common vertex is on the right.
Given a color (a, b), it is easy to simulate queries to the Hamiltonian corresponding to that
color. To compute the nonzero entries of the jth row for this color, if j is in the left partition, then
we find the neighbor of j that has rank a; let us call this ℓ. Then we find the neighbor of ℓ that has
rank b. If this neighbor is j, then ℓ is the position of the nonzero entry in row j; otherwise there is
no nonzero entry. If j is in the right partition, the procedure is the same, except with the roles of
a and b reversed. This procedure uses two queries.
Observe that the simple trick of making the Hamiltonian bipartite suffices to remove the
O(log∗ n) term present in previous decompositions of this form. This trick is quite general and
can be applied to remove a factor of O(log∗ n) wherever such a factor appears in a known Hamiltonian simulation algorithm (e.g., [5, 13, 35]).
Lemma 4.4 decomposes our Hamiltonian H into d2 1-sparse Hamiltonians. We further de2
composePH using Lemma
√ 4.32 into a sum of η = O(d kHkmax /γ) Hamiltonians Gj such that
η
kH − γ j=1 Gj kmax ≤ 2γd , since each 1-sparse Hamiltonian is approximated with precision
√
2γ and therePare d2 approximations
in this sum.
√ To upper bound the simulation error, we have
P
ke−iHt − e−iγ j Gj t k ≤ k(H − γ ηj=1 Gj )tk ≤ 2γd3 t, where we used the fact that keiA − eiB k ≤
14

kA − Bk (as explained
√ 3 in the proof of Theorem 3.1) and kAk ≤ dkAkmax for a d-sparse matrix A.
Choosing γ = ǫ/ 2d t gives the required precision. We now invoke Corollary 4.2 with number of
Hamiltonians η = O(d2 kHkmax /γ) and simulation time γt to get τ = d2 kHkmax t. Plugging this
value of τ into Corollary 4.2 gives us the following lemma, which is the query-complexity part of
Theorem 1.1.
Lemma 4.5. A d-sparse Hamiltonian H can be simulated for time t with error at most ǫ using
/ǫ)
:= d2 kHkmax t ≥ 1.
O τ loglog(τ
log(τ /ǫ) queries, where τ

Note that above we have determined the values of r and γ to use, but these values do not
affect the query complexity (although they do affect the time complexity). This is because r
and γ affect the value of m, but the analysis in Section 3 is independent of m. This enables a
simple generalization to time-dependent Hamiltonians. We can approximate the true evolution by
a product of evolutions under time-independent Hamiltonians for each of the r time intervals of
length t/r. Provided the derivative of the Hamiltonian is bounded, this approximation can be made
arbitrarily accurate by choosing r large enough. As the query complexity does not depend on r, it
is independent of h′ , similar to [31].
Finally, consider simulating a k-local Hamiltonian. A term acting nontrivially on at most k
qubits is 2k -sparse: two states x, y ∈ {0, 1}n are adjacent if the only bits on which x and y differ are
among the k bits involved in the local term. Using this structure, we can give an explicit 2k -coloring,
improving over the 4k -coloring provided by Lemma 4.4: we simply color an edge between states x
and y by indicating which of the k bits are flipped. Thus we can decompose a k-local Hamiltonian
with M terms as a sum of 2k M 1-sparse Hamiltonians. Using this decomposition in place of
Lemma 4.4, we find a simulation as in Theorem 1.1 but with τ replaced by τ̃ := 2k M kHkmax t.

5

Time complexity

We now consider the time complexities of the algorithms described in Theorem 1.3 and Theorem 1.1
(recall that time complexity refers to the sum of the number of queries and additional 2-qubit gates
used in the algorithm). Our approach considerably simplifies this analysis over previous work and
gives improved upper bounds.
The basic algorithm as described in Section 3 is inefficient as it relies on creating a state of
m = poly(h, T, 1ǫ ) qubits. Instead, as in previous work [7], we create a compressed version of this
state that allows us to perform the necessary controlled operations and to reflect about the zero
state. Our simplified approach does not require measuring the control qubits, an operation that
accounts for much of the technical complexity of [7].
We now prove Theorem 1.3 from Section 1, which we restate for convenience.
Theorem 1.3 (Continuous-query simulation). An algorithm with continuous- or fractional-query
/ǫ) 
complexity T ≥ 1 can be simulated with error at most ǫ with O T loglog(T
log(T /ǫ) queries. For continuousquery simulation, if there is a circuit using at most g gates that implements the time evolution due
to HD (t) between any two times t1 and t2 with precision ǫ/T , then the number of additional 2-qubit

R
/ǫ)
:= T1 0T kHD (t)kdt.
gates for the simulation is O T loglog(T
log(T /ǫ) [g + log(h̄T /ǫ)] , where h̄
Proof. The query complexity of this theorem was established in Lemma 3.8. As in the analysis
of query complexity, it suffices to simulate a segment implementing evolution for time 1/5 with
precision ǫ/5T . To simulate the continuous-query model, we can assume without loss of generality
that query evolutions are approximated (as in Theorem 3.1) by m fractional evolutions of equal

15

length 1/5m. Thus we can assume that in each segment, as defined in Lemma 3.4, α := αi = 1/5m
for all i ∈ [m]. Let c := cos(π/10m) and s := sin(π/10m).
The idealized initial state of the ancilla qubits (i.e., the state in the dotted box of Figure 2) is
⊗m
√
√
X
c|0i + s|1i
√
=
κm−|b| σ |b| |bi,
(23)
c+s
m
b∈{0,1}

√
√
c
s
and σ := √c+s
. We truncate this state to the subspace of those b with Hamming
where κ := √c+s

weight |b| ≤ k. Specifically, we prepare the encoded state
X
κm−|ℓ| σ |ℓ| |ℓi + δ|⊥i,

(24)

ℓ∈L

where L := {(ℓ1 , . . . , ℓh ) : 1 ≤ h ≤ k, ℓ1 + · · · + ℓh ≤ m − h}, |⊥i is a special state orthogonal
to all terms in the first sum, and the coefficient δ was shown to be small in Lemma 3.5. Observe
that there is a natural bijection between L and the set of strings b with |b| ≤ k, given by b ↔
0ℓ1 10ℓ2 10ℓ3 . . . 0ℓh 10m−h−ℓ1 −···−ℓh .
It is straightforward to perform the operation (53) from the proof of Lemma 3.5, conditioning
on b as represented
by ℓ. RecallP
that Wi (b) represents the evolution under the driving Hamiltonian
P
from time ij=1 ℓj /5m to time i+1
j=1 ℓj /5m (where we define ℓk+1 = m). By assumption, any such
evolution can be performed with precision O(ǫ/T ) using g gates. Also, recall that Qi (b) is simply
Q if i ≤ |b| or 1 otherwise, so it can be applied in time O(log k). Thus the operation (53) can be
applied in time O(k(g + log k)).
At the end of the segment we must effectively apply the final P and R gates to the encoded
state before reflecting about the encoding of |0m i. (That is, we jointly reflect about this state and
|0i for the additional ancilla in Figure 2.) The P gates are straightforward to apply in the given
encoding. Rather than apply the encoded R gates directly, reflect about the encoding of |0m i, and
then apply the encoded R gates for the next segment, it suffices to reflect about the encoding of
Rα⊗m |0m i (note that Rα† = Rα ). This can be done by applying the inverse of the procedure for
preparing (24), reflecting about the initial state, and applying the preparation procedure. Overall,
we see that the segment can be applied to the encoded initial state with suitable accuracy using
O(k(g + log m)) gates, plus the cost of preparing the encoded ancillas.
The encoded initial state (24) can be prepared in time O(k(log m + log log(1/ǫ))) = O(k log m),
/ǫ) 
as described in Sections 4.2–4.4 of [7] (see in particular equation (22)). Since k = O loglog(T
log(T /ǫ)
(from the proof of Lemma 3.5 with error at most ǫ/5T ) and m = poly(T, h̄, 1ǫ ) (from Theorem 3.1),
/ǫ) log(h̄T /ǫ) 
the overall complexity of making the encoded ancilla state is O log(T
. Thus the cost of
log log(T /ǫ)
implementing a constant-query algorithm to precision ǫ/5T is


log(T /ǫ)
[g + log(h̄T /ǫ)] .
(25)
O(k(g + log m)) = O
log log(T /ǫ)
Implementing O(T ) segments, each with this complexity, gives the stated time complexity. With
error bounded by ǫ/5T for each segment, the overall error is at most ǫ.
Using this approach we can similarly prove Theorem 1.1 from Section 1, which we restate for
convenience.
Theorem 1.1 (Sparse Hamiltonian simulation). A d-sparse Hamiltonian H acting on n qubits can
log2 (τ /ǫ) 
/ǫ) 
be simulated for time t within error ǫ with O τ loglog(τ
log(τ /ǫ) queries and O τ log log(τ /ǫ) n additional
2-qubit gates, where τ := d2 kHkmax t ≥ 1.
16

Proof. The query complexity of this theorem was established in Lemma 4.5. Since the query
complexity of Theorem 1.1 is proved by reduction to Theorem 1.3, a time-efficient version of
Theorem 1.1 can be obtained by essentially the same procedure as the time-efficient version of
Theorem 1.3. In this reduction, τ plays the role of T . Note that the reduction ultimately uses a
fractional-query simulation, so we cannot directly use the result as stated in Theorem 1.3, where
the time-complexity is for the continuous-query case. Nevertheless, we can obtain a similar result
if g is taken to represent the cost of performing any sequence of consecutive non-query operations
in the fractional-query algorithm. The term log(h̄T /ǫ) in Theorem 1.3 results from discretizing a
continuous-query algorithm with a driving Hamiltonian and does not arise here.
The non-query operations Vj for j ∈ [m] described in the proof of Theorem 4.1 are straightforward to implement. In the application to Hamiltonian simulation, we simply cycle through all η
terms in order, so all the Vj s can simply add 1 modulo η, and a sequence Vj ′ · · · Vj adds j ′ −j mod η.
Without loss of generality, we can assume η is a power of 2, so addition modulo η can be performed
by standard binary addition, keeping only the log2 η least significant bits. Thus any operation to
be performed between queries can be applied using g = O(log η) = O(log(dkHkmax t/ǫ)) operations (where the value of η is discussed following the proof of Lemma 4.4). Next, observe that it
suffices to decompose the evolution into m = η 3 t2 /ǫ = poly(t, kHkmax , d, 1ǫ ) terms (as stated in
Corollary 4.2). In the proof of Theorem 1.3, the time complexity for a constant-query algorithm
is O(k(g + log m)). This upper bounds the number of additional gates required to perform the
non-query operations. Using g = O(log(dkHkmax t/ǫ)) and log m = O(log(dkHkmax t/ǫ)), we see
log2 (τ /ǫ) 
that this is O τ log
log(τ /ǫ) .
This only accounts for the operations performed
P between applications of the unitary Q defined
:= ηj=1 |jihj| ⊗ e−iHj using the oracle, where H =
Corollary
4.2.
It
remains
to
implement
Q
in
Pη
j=1 Hj and Hj are Hamiltonians with eigenvalues 0 and π. To implement Q we need to read
the first register to learn which 1-sparse Hamiltonian is to be simulated and then simulate the
1-sparse Hamiltonian Hj . The first part is straightforward; from j we can determine which 1sparse Hamiltonian is to be simulated and whether it is an X, Y , or Z term, in the notation of
Lemma 4.3. This can be done with O(log η) gates, which is linear in the size of the first register.
Now we need to implement the 1-sparse Hamiltonian on an n-qubit register. This can be done with
O(n) gates using the constructions in [1, 10]. For example, to implement an X Hamiltonian on a
state |vi, we can write down the index of v’s neighbor in another register, swap the two registers,
and uncompute the second register. Thus we can implement Q using O(log η + n) gates. Since the
number of uses of Q is the query complexity, the total number of gates used for all invocations of

log2 (τ /ǫ) 
/ǫ)
Q and the non-query operations is O τ loglog(τ
log(τ /ǫ) [log(τ /ǫ) + n] , which is O τ log log(τ /ǫ) n .
The same techniques can be straightforwardly applied to simulate time-dependent sparse Hamiltonians. We divide the evolution into intervals of length t/r, so the Hamiltonian can change by no
d
more than h′ t/r over such an interval, where h′ := maxs∈[0,t] k ds
H(s)k. Thus the error for each
interval is O(h′ t2 /r 2 ), and the error in the overall simulation is O(h′ t2 /r). Therefore it suffices to
log((τ +τ ′ )/ǫ) 
n as
take r = Ω(h′ t2 /ǫ). Then m = poly(t, h, h′ , d, 1ǫ ), and the complexity is O τ log(τ /ǫ)
log log(τ /ǫ)
stated.

6

Lower bounds


We now show that in general, any sparse Hamiltonian simulation method must use Ω loglog(1/ǫ)
log(1/ǫ)
discrete queries to obtain error at most ǫ, so dependence of the query complexity in Theorem 1.1
on ǫ is tight up to constant factors. To show this, we use ideas from the proof of the no-fast17

forwarding theorem [5, Theorem 3], which says that generic Hamiltonians cannot be simulated in
time sub-linear in the evolution time. The Hamiltonian used in the proof of that theorem has the
property that simulating it for time t = πn/2 determines the parity of n bits exactly. We observe
that simulating this Hamiltonian (with sufficiently high precision) for any time t > 0 gives an
unbounded-error algorithm for the parity of n bits, which also requires Ω(n) queries [4, 19].
We now prove Theorem 1.2 from Section 1, which we restate for convenience.
Theorem 1.2 (ǫ-dependent lower bound for Hamiltonian simulation). For any ǫ > 0, there exists
a 2-sparse Hamiltonian H with kHkmax < 1 such that simulating H with precision ǫ for constant

time requires Ω loglog(1/ǫ)
log(1/ǫ) queries.

Proof. To construct the Hamiltonian, we begin with a simpler Hamiltonian H ′ that acts on vectors
|ii with i ∈ {0, 1, . . . , N } [15]. The nonzero matrix entries of H ′ are hi |H ′ | i + 1i = hi + 1 |H ′ | ii =
p
(N − i)(i + 1)/N for i ∈ {0, 1, . . . , N −1}. We have kH ′ kmax < 1, and simulating H ′ for t = πN/2
′
starting with the state |0i gives the state |N i (i.e., e−iH πN/2 |0i = |N i). More generally, for
′
N.
t ∈ [0, πN/2], we claim that |hN |e−iH t |0i| = |sin(t/N
PN )| (j)
To see this, consider the Hamiltonian X̄ := j=1 X , where X := ( 01 10 ) and the superscript
(j) indicates that the operator acts nontrivially on the jth qubit. Since e−iXt = cos(t)1 − i sin(t)X,
−1/2 P
we have |h11 . . . 1|e−iX̄t |00 . . . 0i| = |sin(t)|N . Defining |wtk i := Nk
|x|=k |xi, we have
X̄|wtk i =

p

(N − k + 1)k|wtk−1 i +

p
(N − k)(k + 1)|wtk+1 i.

(26)

This is precisely the behavior of N H ′ with |ki playing the role of |wtk i, so the claim follows.
Now, as in [5], consider a Hamiltonian H generated from an N -bit string x1 x2 . . . xN . H acts
on vertices |i, ji with i ∈ {0, . . . , N } and j ∈ {0, 1}. The nonzero matrix entries of this Hamiltonian
are
p
(27)
hi, j |H| i − 1, j ⊕ xi i = hi − 1, j ⊕ xi |H| i, ji = (N − i + 1)i/N

for all i and j. By construction, |0, 0i is connected to either |i, 0i or |i, 1i (but not both) for
any i; it is connected to |i, ji if and only if j = x1 ⊕ x2 ⊕ · · · ⊕ xi . Thus |0, 0i is connected
to either |N, 0i or |N, 1i, and determining which is the case determines the parity of x. The
graph of this Hamiltonian contains two disjoint paths, one containing |0, 0i and |N, parity(x)i
and the other containing |0, 1i and |N, 1 ⊕ parity(x)i. Restricted to the connected component
of |0, 0i, this Hamiltonian is the same as H ′ . Thus, starting with the state |0, 0i and simulating
H for time t gives |hN, parity(x)|e−iHt |0, 0i| = |sin(t/N )|N . Furthermore, for any t, we have
hN, 1 ⊕ parity(x)|e−iHt |0, 0i = 0 since the two states lie in disconnected components.
Simulating this Hamiltonian exactly for any time t > 0 starting with |0, 0i yields an unboundederror algorithm for computing the parity of x, as follows. First we measure e−iHt |0, 0i in the
computational basis. We know that for any t > 0, the state e−iHt |0, 0i has some nonzero overlap
on |N, parity(x)i and zero overlap on |N, 1 ⊕ parity(x)i. If the first register is not N , we output
0 or 1 with equal probability. If the first register is N , we output the value of the second register.
This is an unbounded-error algorithm for the parity of x, and thus requires Ω(N ) queries.
Since the unbounded-error query complexity of parity is Ω(N ) [4, 19], this shows that exactly
simulating H for any time t > 0 needs Ω(N ) queries. However, even if we only have an approximate
simulation, the previous algorithm still works as long as the error in the output state is smaller
than the overlap |hN, parity(x)|e−iHt |0, 0i|. If we ensure that the overlap is larger than ǫ by a
constant factor, then even with error ǫ, the overlap on that state will be larger than ǫ. On the
other hand, the overlap on |N, 1 ⊕ parity(x)i is at most ǫ, since the output state is ǫ close to the
ideal output state which has no overlap.
18

To achieve an overlap much larger than ǫ, we need |sin(t/N )|N to be much larger than ǫ. There

is some value of N in Θ loglog(1/ǫ)
log(1/ǫ) that achieves this.

A similar construction
shows that any ǫ-error simulation of the continuous-query model must

discrete
queries,
so Lemma 3.2 is tight up to constant factors. Again we show
use Ω loglog(1/ǫ)
log(1/ǫ)
that a sufficiently high-precision simulation of a certain Hamiltonian could be used to compute
parity with unbounded error. However, in the fractional-query model, the form of the Hamiltonian
is restricted and it is unclear how to implement the weights that simplify the analysis of the
dynamics in Theorem 1.2. Instead, we consider a quantum walk on an infinite unweighted path
that also solves parity with unbounded error, and we show that this still holds if the path is long
but finite.

Theorem 6.1 (ǫ-dependent lower bound for continuous-query simulation). For any ǫ > 0, given a

query Hamiltonian Hx for a string of N = Θ loglog(1/ǫ)
log(1/ǫ) bits, simulating Hx + HD (t) for constant
time with precision ǫ requires Ω(N ) queries.
P
Proof. We prove a lower bound for simulating a Hamiltonian of the form H ′ = ηa=1 ca Ua† Hx Ua
with coefficients c1 , . . . , P
cη ∈ R. The Hamiltonian Hx can be used to simulate H ′ to any given
accuracy with overhead a |ca |, so this implies a lower bound for simulating Hx . In particular, by
taking r sufficiently large, the evolution under H ′ can be approximated arbitrarily closely as
!r
η
Y
′
Ua† e−iHx ca t/r Ua .
e−iH t ≈
(28)
a=1

P
This corresponds to a fractional-query algorithm with cost t ηa=1 |ca |. By Theorem 3.1, this
fractional-query algorithm can be simulated with arbitrarily small error by a continuous-query
algorithm with the same cost. This continuous-query algorithm uses the query Hamiltonian Hx ,
and its driving Hamiltonian HD (t) implements the unitaries {Ua , Ua† }ηa=1 at appropriate times.
Viewing the Hamiltonian in terms of the graph of its nonzero entries, the oracle Hamiltonian
Hx provides input-dependent self-loops. First we modify it to give input-dependent edges. Observe
that




1 1 1
1 0
Had
Had =
(29)
0 0
2 1 1
1 ) is the Hadamard gate. Thus we can include a term in the Hamiltonian
where Had := √12 ( 11 −1
that has an edge between two vertices associated with the input index i (and self-loops on those
vertices) if xi = 1, and is zero otherwise.
Now consider a space with basis states |i, j, ki where i ∈ Z and j, k ∈ {0, 1}. The label j plays
the same role as in Theorem 1.2, whereas the new label k indexes two positions for each value of
i. These new positions are needed because the pairs of vertices associated with each input index
must be disjoint.
To specify the Hamiltonian, we define unitaries U1 , U2 , U3 , U4 so that the nonzero matrix elements of Ua† Hx Ua for a ∈ {1, 2, 3, 4} are

hi, 0, k|U1† Hx U1 |i, 0, k̄i = hi, 0, k|U1† Hx U1 |i, 0, ki = xi /2

hi, 1, k|U2† Hx U2 |i, 1, k̄i = hi, 1, k|U2† Hx U2 |i, 1, ki = xi /2

hi, k, k|U3† Hx U3 |i, k̄, k̄i = hi, k, k|U3† Hx U3 |i, k, ki = xi /2
hi, k, k̄|U4† Hx U4 |i, k̄, ki = hi, k̄, k|U4† Hx U4 |i, k̄, ki = xi /2
19

(30)
(31)
(32)
(33)

for all i ∈ [N ] and k ∈ {0, 1}. Combining these four contributions to obtain a Hamiltonian
−U1† Hx U1 − U2† Hx U2 + U3† Hx U3 + U4† Hx U4 and observing that the self-loops cancel, these matrix
elements can be summarized in terms of the gadget shown in Figure 3.
(i, 0, 0)

(i, 0, 1)

(i, 1, 0)

(i, 1, 1)

Figure 3: The gadget for querying xi . If xi = 0, no edges are present. If xi = 1, the solid edges have weight
1/2 and the dashed edges have weight −1/2.

We add a driving Hamiltonian to connect these gadgets to form two paths encoding the parity
similarly as in Theorem 1.2, and we extend the paths infinitely in both directions. Specifically, the
driving Hamiltonian HD has nonzero matrix elements
hi, j, k|HD |i, j, k̄i = 1/2

(34)

for all i ∈ Z and j, k ∈ {0, 1} (corresponding to the dashed edges in Figure 3, but with positive
weight), and
hi + 1, j, 0|HD |i, j, 1i = hi, j, 1|HD |i + 1, j, 0i = 1/2

(35)

for all i ∈ Z and j ∈ {0, 1} (corresponding to edges that join sectors with adjacent values of i).
Then the total Hamiltonian
H = −U1† Hx U1 − U2† Hx U2 + U3† Hx U3 + U4† Hx U4 + HD

(36)

is 1/2 times the adjacency matrix of the disjoint union of two infinite paths, one with vertices
. . . ,(0, 0, 0), (0, 0, 1), (1, 0, 0), (1, x1 , 1), (2, x1 , 0), (2, x1 ⊕ x2 , 1), . . . ,

(N, x1 ⊕ · · · ⊕ xN , 1), (N + 1, x1 ⊕ · · · ⊕ xN , 0), (N + 1, x1 ⊕ · · · ⊕ xN , 1), . . .

(37)

and the other with vertices
. . . ,(0, 1, 0), (0, 1, 1), (1, 1, 0), (1, 1 ⊕ x1 , 1), (2, 1 ⊕ x1 , 0), (2, 1 ⊕ x1 ⊕ x2 , 1), . . . ,

(N, 1 ⊕ x1 ⊕ · · · ⊕ xN , 1), (N + 1, 1 ⊕ x1 ⊕ · · · ⊕ xN , 0), (N + 1, 1 ⊕ x1 ⊕ · · · ⊕ xN , 1), . . . .
(38)
Analogous to the Hamiltonian H in the proof of Theorem 1.2, (0, 0, 1) is in the same component
as (N, b, 1) if and only if b = parity(x).
To compute the probability of reaching (n, parity(x), 1) starting from (0, 0, 1) after evolving
with the Hamiltonian (36) for time t, we can use the expression for the propagator on an infinite
path in terms of a Bessel function (see for example [10]). Specifically, we have
|hN, parity(x), 1|e−iHt |0, 0, 1i| = |J2N (t)|.

(39)

For large N and for any fixed t 6= 0, we have |JN (t)| = e−Θ(N log N ) [34, Section 8.1]. Thus, as in
the proof of Theorem 1.2, even
a simulation with error ǫ gives the result with nonzero probability

.
provided N = Θ loglog(1/ǫ)
log(1/ǫ)
20

The preceding argument uses a Hamiltonian acting on an infinite-dimensional space. However,
we can truncate it to act on a finite space with essentially the same effect. Specifically, we apply
the Truncation Lemma of [12] with K = span{|i, j, ki : − N 3 − N 2 ≤ i ≤ N 3 + N 2 , j, k ∈ {0, 1}}
and W = H. Let P project onto K and let P ′ project onto span{|i, j, ki : − N 2 ≤ i ≤ N 2 , j, k ∈
{0, 1}}. Finally, let |γ(t)i = P ′ e−iHt |0, 0, 1i. Then δ2 := ke−iHt |0, 0, 1i − |γ(t)ik2 = |J2N 2 +1 (t)|2 +
P
2
−Ω(N 2 log N ) . Furthermore, (1 − P )H r |γ(t)i = 0 for all r ∈ {0, 1, . . . , N 3 }.
2 ∞
j=2 |J2N 2 +j (t)| ≤ e
Also observe that kHk = 1. Thus the Truncation Lemma shows that



4et
2
3
−iHt
−iP HP t
(40)
+ 2 δ + 2−N (1 + δ) ≤ e−Ω(N log N ) ,
k(e
−e
)|0, 0, 1ik ≤
3
N

so the error incurred by truncating H to the Hamiltonian P HP acting on the finite-dimensional
space K is asymptotically negligible compared to ǫ.

7

Open questions

While our algorithm for continuous-query simulation is optimal as a function of ǫ alone, it is
suboptimal as a function of T , and it is unclear what tradeoffs might exist between these two
parameters. The best known lower bound as a function of both ǫ and T is Ω T + loglog(1/ǫ)
log(1/ǫ) . It
would be surprising if this bound were achievable, but it remains open to find such an algorithm or
to prove a better lower bound. In general, any improvement to the tradeoff between ǫ and T could
be of interest.
In the context of time-independent sparse Hamiltonian simulation, the quantum walk-based
simulation of [6, 9] achieves linear dependence on t, whereas our upper bound is superlinear in
t. However, the dependence on ǫ is significantly worse in the walk-based approach. It would be
desirable to combine the benefits of these two approaches into a single algorithm.
Another open question is to better understand the dependence of our sparse Hamiltonian simulation method on the sparsity d. While we use d2+o(1) queries, the method of [6] uses only O(d)
queries. Could the performance of the simulation based on fractional queries be improved by a
different decomposition of the Hamiltonian?

Acknowledgements
We thank Sevag Gharibian and Nathan Wiebe for valuable discussions. This work was supported in
part by ARC grant FT100100761, Canada’s NSERC, CIFAR, the Ontario Ministry of Research and
Innovation, and the US ARO. RDS acknowledges support from the Laboratory Directed Research
and Development Program at Los Alamos National Laboratory.

References
[1] Dorit Aharonov and Amnon Ta-Shma, Adiabatic quantum state generation and statistical zero
knowledge, Proceedings of the 35th ACM Symposium on Theory of Computing, pp. 20–29,
2003, arXiv:quant-ph/0301023. [pp. 1, 2, 17]
[2] Andris Ambainis, Andrew M. Childs, Ben W. Reichardt, Robert Špalek, and Shengyu Zhang,
Any AND-OR formula of size N can be evaluated in time N 1/2+o(1) on a quantum computer, SIAM Journal on Computing 39 (2010), no. 6, 2513–2530, arXiv:quant-ph/0703015
and arXiv:0704.3628. [p. 4]
21

[3] Andris Ambainis, Loı̈ck Magnin, Martin Roetteler, and Jérémie Roland, Symmetry-assisted
adversaries for quantum state generation, Proceedings of the 26th IEEE Conference on Computational Complexity, pp. 167–177, 2011, arXiv:1012.2112. [p. 3]
[4] Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, and Ronald de Wolf,
Quantum lower bounds by polynomials, Journal of the ACM 48 (2001), no. 4, 778–797,
arXiv:quant-ph/9802049. [pp. 6, 18]
[5] Dominic W. Berry, Graeme Ahokas, Richard Cleve, and Barry C. Sanders, Efficient quantum
algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270
(2007), no. 2, 359–371, arXiv:quant-ph/0508139. [pp. 2, 5, 13, 14, 18]
[6] Dominic W. Berry and Andrew M. Childs, Black-box Hamiltonian simulation and unitary implementation, Quantum Information and Computation 12 (2012), no. 1–2, 29–62,
arXiv:0910.4157. [pp. 2, 3, 21]
[7] Dominic W. Berry, Richard Cleve, and Sevag Gharibian, Gate-efficient discrete simulations
of continuous-time quantum query algorithms, Quantum Information and Computation 14
(2014), no. 1–2, 1–30, arXiv:1211.4637. [pp. 4, 5, 6, 7, 9, 15, 16]
[8] Andrew M. Childs, Quantum information processing in continuous time, Ph.D. thesis, Massachusetts Institute of Technology, 2004. [p. 2]
[9]

, On the relationship between continuous- and discrete-time quantum walk, Communications in Mathematical Physics 294 (2010), no. 2, 581–603, arXiv:0810.0312. [pp. 2, 4,
21]

[10] Andrew M. Childs, Richard Cleve, Enrico Deotto, Edward Farhi, Sam Gutmann, and Daniel A.
Spielman, Exponential algorithmic speedup by quantum walk, Proceedings of the 35th ACM
Symposium on Theory of Computing, pp. 59–68, 2003, arXiv:quant-ph/0209131. [pp. 2, 17,
20]
[11] Andrew M. Childs, Richard Cleve, Stephen P. Jordan, and David Yonge-Mallo, Discretequery quantum algorithm for NAND trees, Theory of Computing 5 (2009), no. 5, 119–123,
arXiv:quant-ph/0702160. [pp. 1, 4]
[12] Andrew M. Childs, David Gosset, and Zak Webb, Universal computation by multi-particle
quantum walk, Science 339 (2013), no. 6121, 791–794, arXiv:1205.3782. [p. 21]
[13] Andrew M. Childs and Robin Kothari, Simulating sparse Hamiltonians with star decompositions, Theory of Quantum Computation, Communication, and Cryptography (TQC 2010),
Lecture Notes in Computer Science, vol. 6519, pp. 94–103, 2011, arXiv:1003.3683. [pp. 2, 14]
[14] Andrew M. Childs and Nathan Wiebe, Hamiltonian simulation using linear combinations of unitary operations, Quantum Information and Computation 12 (2012), 901–924,
arXiv:1202.5822. [p. 2]
[15] Matthias Christandl, Nilanjana Datta, Artur Ekert, and Andrew J. Landahl, Perfect state
transfer in quantum spin networks, Physical Review Letters 92 (2004), no. 18, 187902,
arXiv:quant-ph/0309131. [p. 18]
[16] B. David Clader, Bryan C. Jacobs, and Chad R. Sprouse, Preconditioned quantum linear
system algorithm, Physical Review Letters 110 (2013), no. 25, 250504, arXiv:1301.2340. [p. 1]
22

[17] Richard Cleve, Daniel Gottesman, Michele Mosca, Rolando D. Somma, and David YongeMallo, Efficient discrete-time simulations of continuous-time quantum query algorithms,
Proceedings of the 41st ACM Symposium on Theory of Computing, pp. 409–416, 2009,
arXiv:0811.4428. [pp. 3, 4, 5, 6, 7, 8, 9, 24, 25]
[18] Edward Farhi, Jeffrey Goldstone, and Sam Gutmann, A quantum algorithm for the Hamiltonian NAND tree, Theory of Computing 4 (2008), no. 8, 169–190, arXiv:quant-ph/0702144. [p.
4]
[19] Edward Farhi, Jeffrey Goldstone, Sam Gutmann, and Michael Sipser, Limit on the speed of
quantum computation in determining parity, Physical Review Letters 81 (1998), no. 24, 5442–
5444, arXiv:quant-ph/9802045. [pp. 6, 18]
[20] Edward Farhi and Sam Gutmann, Analog analogue of a digital quantum computation, Physical
Review A 57 (1998), no. 4, 2403–2406, arXiv:quant-ph/9612026. [pp. 3, 4]
[21] Richard P. Feynman, Simulating physics with computers, International Journal of Theoretical
Physics 21 (1982), no. 6–7, 467–488. [p. 1]
[22] Aram W. Harrow, Avinatan Hassidim, and Seth Lloyd, Quantum algorithm for linear systems
of equations, Physical Review Letters 103 (2009), no. 15, 150502, arXiv:0811.3171. [p. 1]
[23] Jacky Huyghebaert and Hans De Raedt, Product formula methods for time-dependent
Schrödinger problems, Journal of Physics A 23 (1990), no. 24, 5777. [pp. 6, 24]
[24] Camille Jordan, Essai sur la géométrie à n dimensions, Bulletin de la Société Mathématique
de France 3 (1875), 103–174. [p. 10]
[25] Troy Lee, Rajat Mittal, Ben W. Reichardt, Robert Špalek, and Mario Szegedy, Quantum query
complexity of state conversion, Proceedings of the 52nd IEEE Symposium on Foundations of
Computer Science, pp. 344–353, 2011, arXiv:1011.3020. [pp. 3, 4, 5]
[26] Seth Lloyd, Universal quantum simulators, Science 273 (1996), no. 5278, 1073–1078. [pp. 1,
2]
[27] Chris Marriott and John Watrous, Quantum Arthur–Merlin games, Computational Complexity 14 (2005), no. 2, 122–152, arXiv:cs/0506068. [pp. 5, 9]
[28] Carlos Mochon, Hamiltonian oracles, Physical Review A 75 (2007), no. 4, 042313,
arXiv:quant-ph/0602032. [pp. 4, 7]
[29] Rajeev Motwani and Prabhakar Raghavan, Randomized algorithms, Cambridge University
Press, 1995. [p. 27]
[30] Daniel Nagaj, Pawel Wocjan, and Yong Zhang, Fast amplification of QMA, Quantum Information and Computation 9 (2009), no. 11-12, 1053–1068, arXiv:0904.1549. [p. 9]
[31] David Poulin, Angie Qarry, Rolando D. Somma, and Frank Verstraete, Quantum simulation
of time-dependent Hamiltonians and the convenient illusion of Hilbert space, Physical Review
Letters 106 (2011), no. 17, 170501, arXiv:1102.1360. [pp. 2, 15]
[32] Masuo Suzuki, General theory of fractal path integrals with applications to many-body theories
and statistical physics, Journal of Mathematical Physics 32 (1991), no. 2, 400–407. [p. 2]
23

[33] John Watrous, Zero-knowledge against quantum attacks, SIAM Journal on Computing 39
(2009), no. 1, 296–305, arXiv:quant-ph/0511020. [p. 9]
[34] George N. Watson, A treatise on the theory of Bessel functions, Cambridge University Press,
1922. [p. 20]
[35] Nathan Wiebe, Dominic W. Berry, Peter Høyer, and Barry C. Sanders, Simulating quantum dynamics on a quantum computer, Journal of Physics A 44 (2011), no. 44, 445308,
arXiv:1011.3489. [pp. 2, 14]

A

Proofs of known results

In this appendix, for the sake of completeness we provide proofs of claims that are known or
essentially follow from known results.

A.1

Equivalence of continuous- and fractional-query models

Theorem 3.1 (Equivalence of continuous- and fractional-query models). For any ǫ > 0, any
algorithm with continuous-query complexity T can be implemented with fractional-query
R T complexity
T with error at most ǫ and m = O(h̄T 2 /ǫ) fractional-query gates, where h̄ := T1 0 kHD (t)k dt
is the average norm of the driving Hamiltonian. Conversely, any algorithm with fractional-query
complexity T can be implemented with continuous-query complexity T with error at most ǫ.
Proof. A simulation of the continuous-query model by the fractional-query model with the stated
properties appears in Section II.A of [17]. We present their proof for completeness.
We wish to implement the unitary U (T ) satisfying the Schrödinger equation (2) with U (0) = 1.
To refer to the solutions of this equation for arbitrary Hamiltonians and time intervals, we define
UH (t2 , t1 ) to be the solution of the Schrödinger equation with Hamiltonian H from time t1 to time
t2 where U (t1 ) = 1. In this notation, U (T ) = UHx +HD (T, 0).
Let m be an integer and θ = T /m. We have
UHx +HD (T, 0) = UHx +HD (mθ, (m − 1)θ) · · · UHx +HD (2θ, θ)UHx +HD (θ, 0).

(41)

If we can approximate each of these m terms, we can use the subadditivity of error in implementing unitaries (i.e., kU V − Ũ Ṽ k ≤ kU − Ũ k + kV − Ṽ k for unitaries U, Ũ , V, Ṽ ) to obtain an
approximation of U (T ).
Reference [23] shows that for small θ, the evolution according to Hamiltonians A and B over
an interval of length θ approximates the evolution according to A + B over the same interval.
Specifically, from [23, eq. A8b] we have
kUA+B ((j + 1)θ, jθ) − UA ((j + 1)θ, jθ)UB ((j + 1)θ, jθ)k ≤

Z (j+1)θ

dv

jθ

Z v
jθ

du k[A(u), B(v)]k. (42)

In our application, A(t) = HD (t) and B = Hx . Since kHx k = 1, the right-hand side is at most
2

Z (j+1)θ
jθ

dv

Z v
jθ

du kHD (u)k ≤ 2

Z (j+1)θ
jθ

dv

Z (j+1)θ
jθ

24

du kHD (u)k = 2θ

Z (j+1)θ
jθ

kHD (u)k du. (43)

By subadditivity, the error in implementing U (T ) is at most
2θ

m−1
X Z (j+1)θ
j=0

jθ

kHD (u)k du = 2θ

Z T
0

kHD (u)kdu = 2θ h̄T =

2h̄T 2
.
m

(44)

This error is smaller than ǫ when m ≥ 2h̄T 2 /ǫ, which proves this direction of the equivalence.
For the other direction, consider a fractional-query algorithm
Ufq := Um Qαm Um−1 · · · Qα2 U1 Qα1 U0

(45)

P
(recall that Q depends on x), where αi ∈ (0, 1] for all i ∈ [m], with complexity T = m
i=1 αi . Let
Pi
(j)
−iH
D for all j ∈ {0, 1, . . . , m}. Consider the piecewise
Ai := j=1 αj for all i ∈ [m] and let Uj =: e
constant Hamiltonian
!
m
X
1
(i)
(0)
(46)
δt∈[Ai −ǫ1 ,Ai ] HD ,
δt∈[0,ǫ1 ] HD +
H(t) = Hx +
ǫ1
i=1

where δB is 0 if B is false and 1 if B is true. Provided ǫ1 ≤ min{α1 /2, α2 , . . . , αm }, evolving with
H(t) from t = 0 to T implements a unitary close to our fractional-query algorithm. More precisely,
it implements
(m−1)

(m)

U (T ) = e−i(HD +ǫ1 Hx ) e−i(αm −ǫ1 )Hx e−i(HD
(1)
−i(HD +ǫ1 Hx )

e−i(α2 −ǫ1 )Hx e

+ǫ1 Hx )

···
0

e−i(α1 −2ǫ1 )Hx e−i(HD +ǫ1 Hx ) ,

(47)

which satisfies kU (T ) − Ufq k = O(mǫ1 ). This follows from the fact that each exponential in (47)
(m)

approximates the corresponding unitary of (45) within error ǫ1 (e.g., ke−i(HD +ǫ1 Hx ) − Um k = O(ǫ1 )
and ke−i(αm −ǫ1 )Hx − Qαm k = O(ǫ1 )) and the subadditivity of error when implementing unitaries.
The fact that each exponential has error O(ǫ1 ) follows from the inequality keiA − eiB k ≤ kA − Bk.
This can be proved by observing that keiA − eiB k = k(eiA/n )n − (eiB/n )n k ≤ nkeiA/n − eiB/n k ≤
kA − Bk + O(1/n), where the first inequality uses subadditivity of error and the second inequality
follows by Taylor expansion. Since the statement is true for all n, the claim follows.
This simulation has continuous-query complexity T . Its error can be made less than ǫ by
choosing ǫ1 sufficiently small (in particular, it suffices to take some ǫ1 = Θ(ǫ/m)).

A.2

The Approximate Segment Lemma

In this section, we establish the Approximate Segment Lemma (Lemma 3.5). This lemma essentially
follows from [17] with minor modification. We start by proving the following Gadget Lemma, which
follows from [17, Section II.B].
be a√ unitary
matrix with eigenvalues ±1; let α ∈ [0, 1].
Lemma 3.3 (Gadget Lemma [17]). Let Q
√

c
s
1
√
√
√
The circuit in Figure 1, with Rα := c+s
and P := ( 10 0i ), performs the map
s− c
|0i|ψi 7→

√

qα |0ie−iπα/2 Qα |ψi +

p

1 − qα |1i|φi

(3)

for some state |φi, where c := cos(πα/2), s := sin(πα/2), qα := 1/(c + s)2 = 1/(1 + sin(πα)), and
Qα = 21 (1 + Q) + e−iπα 12 (1 − Q) = e−iπα/2 (c1 + isQ).

25

Proof. The input state evolves as follows:
√
√
c|0i + s|1i
√
|ψi
|0i|ψi 7→
c+s
√
√
1
7→ √
( c|0i|ψi + s|1iQ|ψi)
c+s
√
1
[|0i(c|ψi + isQ|ψi) + cs|1i(|ψi − iQ|ψi)]
7→
c+s
p
√
= qα (|0ieiπα/2 Qα |ψi + sin(πα)|1ie−iπ/4 Q−1/2 |ψi).

(48)

Thus the output has the stated form.

We can now collect these gadgets into a segment, which implements a fractional-query algorithm
with constant query complexity with amplitude 1/2.
Lemma 3.4 (Segment Lemma). Let V be a unitary implementable by a fractional-query algorithm
α1
αm
with query complexity at most
Pm 1/5, i.e., there exists an m such that V = Um Q Um−1 · · · U1 Q U0
with αi ≥ 0 for all i and i=1 αi ≤ 1/5. Let P and Rα be as in Lemma 3.3. Then there exists a
unitary Υ on the additional ancilla such that the circuit in Figure 2 performs the map
√
3 ⊥
1 m+1 iϑ
m+1
|0
i|ψi 7→ |0
ie V |ψi +
|Φ i
(4)
2
2
for some state |Φ⊥ i satisfying (|0m+1 ih0m+1 | ⊗ 1)|Φ⊥ i = 0 and some ϑ ∈ [0, 2π).
Proof. We first analyze the subcircuit in the dashed box in Figure 2, which is the entire circuit
without the first qubit. The first qubit does not interact with the rest of the qubits and is only
used at the end of the proof.
This subcircuit is built by composing several fractional-query gadgets (as in Figure 1) with
a new control qubit for each gadget but with a common target. The m gadgets correspond to
making the fractional queries Qαi . The first register of a gadget indicates whether it has applied
the fractional query successfully, in which case the register is |0i, or not, in which case it is |1i. For
the ith gadget, the output state has amplitude qαi on the state |0i corresponding to the successful
outcome, as shown in Lemma 3.3.
The state of the control qubits on the output is |0m i only when all the gadgets have successfully
applied the fractional query. In this case, the target has been successfully transformed to V |ψi.
Thus the dashed subcircuit in Figure 2 performs the map
p
√
(49)
|0m i|ψi 7→ p|0m ieiϑ V |ψi + 1 − p|Φ⊥ i
Q
Pm
for some |Φ⊥ i satisfying (|0m ih0m | ⊗ 1)|Φ⊥ i = 0, where p = m
i=1 qαi and ϑ = −
i=1 παi /2 mod
2π.
This is similar to the desired statement, except that we want the amplitude in front of |0m i to
√
be 1/2 instead of p. We show that p > 1/4 and then use the first qubit to decrease its value to
exactly 1/4.
P
Since m
i=1 αi ≤ 1/5 by assumption, we can lower bound the value of p as follows. Since αi ≥ 0
for all i, using the inequalities sin x ≤ x (for x ≥ 0) and 1/(1 + x) ≥ 1 − x (for x ≥ −1) gives
p=

m
Y
i=1

qαi =

m
Y
i=1

m

m

m

X
Y
Y
π
1
1
1
αi ≥ 1 − > ,
(1 − παi ) ≥ 1 − π
≥
≥
1 + sin(παi )
1 + παi
5
4
i=1

i=1

26

i=1

(50)

Q
P
where the third inequality uses the fact that for xi ∈ [0, 1], i (1 − xi ) ≥ 1 − i xi .
√
1
1 1/2
|1i.
Thus we have p > 1/2. Now let Υ be any unitary that maps |0i to 2√
p |0i + (1 − 4p )
√
1
Since p > 1/2, we have 2√p < 1, so a unitary Υ exists. Then for the full circuit in Figure 2, the
√
1
amplitude corresponding to the state |0m i is p · 2√
p = 1/2.
Finally, we
 show that the map in the previous lemma can be performed to error ǫ using only
O loglog(1/ǫ)
log(1/ǫ) queries.

Lemma 3.5 (Approximate Segment Lemma). Let V be a unitary implementable by a fractionalquery algorithm with query complexity at most 1/5. Then for any ǫ > 0, there exists a unitary

quantum circuit that makes O loglog(1/ǫ)
log(1/ǫ) discrete queries and, within error ǫ, performs a unitary
U acting as
√
1 m+1 iϑ
3 ⊥
m+1
U |0
i|ψi = |0
ie V |ψi +
|Φ i
(5)
2
2
for some state |Φ⊥ i satisfying (|0m+1 ih0m+1 | ⊗ 1)|Φ⊥ i = 0 and some ϑ ∈ [0, 2π).

Proof. From Lemma 3.4 we know that the circuit in Figure 2 performs the claimed map with no
error. However, the circuit makes m discrete queries, which can be arbitrarily
large. We wish to
log(1/ǫ) 
construct a circuit with error at most ǫ that makes only O log log(1/ǫ) queries, independent of m.
WeNfirst analyze the
subcircuit in the dotted box in Figure 2. The output of this subcircuit is
Nm
√
√
√ 1
|ζi = m
R
|0i
=
i=1 αi
i=1 ci +si ( ci |0i + si |1i), where ci := cos(παi /2) and si := sin(παi /2).
P
We also define qi := qαi = 1/(ci + si )2 = 1/(1 + sin(παi )). We can write |ζi = x∈{0,1}m wx |xi
P
with x |wx |2 = 1.
P
Now consider the subnormalized state |ζk i := |x|≤k wx |xi, where |x| denotes the Hamming
weight of x and k ≤ m is a positive integer. In the circuit, we approximate the state |ζi with some
|ζk i. Clearly |ζm i = |ζi, and the approximation becomes worse as k decreases. To achieve a 1−ǫ2 /2

P
. Since 1 − hζ|ζk i = |x|>k |wx |2 , we
approximation, we claim it suffices to take k = Ω loglog(1/ǫ)
log(1/ǫ)
P
must upper bound |x|>k |wx |2 in terms of k.
ci
i
and Pr(Xi = 1) = ci s+s
.
Consider m independent random variables Xi with Pr(Xi = 0) = ci +s
i
i
P
P
2
2
The probability that i Xi > k is |x|>k |wx | , since |wx | is the probability of the event Xi = xi
for all i. For such events, the Chernoff bound (see for example [29, Theorem 4.1]) says that for any
δ > 0,
!
X
eδµ
,
(51)
Xi > (1 + δ)µ <
Pr
(1 + δ)(1+δ)µ
i
P
P si
P
wherePµ :=
1) =
αi ≥ 0 and
i = P
i Pr(X
i ci +si . Since
i αi ≤ 1/5, we have µ ≥ 0 and
P
P
si
µ = i ci +si ≤ i si = i sin(παi /2) ≤ i παi /2 ≤ π/10 ≤ 1, where we used the facts that
sin x ≤ x for all x > 0 and sin θ +P
cos θ ≥ 1 for all θ ∈P[0, π/2].
Setting k = (1 + δ)µ, we get |x|>k |wx |2 = Pr( i Xi > k) < ek−µ /(1 + δ)k = ek−µ µk /kk <

ek /kk . This is less than ǫ2 /2 when k = Ω loglog(1/ǫ)
log(1/ǫ) . For such a value of k, the state |ζk i has
inner product at least 1 − ǫ2 /2 with |ζi. Let |ζ̃i denote the normalized |ζk i for some choice of

2
k = Ω loglog(1/ǫ)
log(1/ǫ) . The state |ζ̃i also has inner product at least 1 − ǫ /2 with |ζi. We replace the

dotted box in Figure 2 with |ζ̃i, a fixed state that requires no queries to create.
With this modification, the control qubits are in a superposition over states with Hamming
weight at most k, suggesting that this circuit can be performed with at most k queries. We now
show that this is possible.
27

The control qubits are in a superposition over states |bi where b ∈ {0, 1}m . The value of bi
decides whether the ith query occurs or not. The string b therefore completely determines the
product of unitary matrices that is applied to |ψi when the control qubits are in the state |bi. This
product contains at most k query gates, and thus may be written as
W|b| (b) Q W|b|−1 (b) · · · Q W1 (b) Q W0 (b).

(52)

Note that the Wi operators are functions of b. We may also write this unitary as
Wk (b) Qk (b) Wk−1 (b) · · · Q2 (b) W1 (b) Q1 (b) W0 (b),

(53)

where for i ≤ |b| the Wi operators are as before and for i > |b|, we have Wi = 1. Here Qi (b) is
defined to be Q when i ≤ |b| and 1 when i > |b|. We can now construct a circuit that performs the
unitary in (53) controlled on the value of b. This circuit has at most k query gates and performs
the same unitary as the circuit in Figure 2 with |ζi replaced with |ζ̃i.
Finally, we show that the actual operation performed, denoted Ũ , is within error ǫ of the ideal
unitary U . The only difference between these operations is that Ũ prepares |ζ̃i rather than |ζi in
the initial step. Therefore the error between Ũ and U is at most the error between an operation
Nm that
prepares |ζ̃i and an operation that prepares |ζi. If we required U to prepare |ζi using i=1 Rαi ,
it would be difficult to design a nearby unitary that prepares |ζ̃i. However, the lemma does not
specify the action of U on states not of the form |0m+1 i|ψi, so we can make any convenient choice
of the operation
N preparing |ζi that is close to the operation preparing |ζ̃i.
Let R := m
i=1 Rαi and denote the unitary that prepares |ζ̃i by R̃. In the computational basis,
R has first column ζ and R̃ has first column ζ̃. We claim there is a unitary R′ that is within ǫ of
R̃ but that has the same first column as R.
To see this, let θ satisfy hζ̃|ζi = cos θ. Consider the 2-dimensional subspace spanned by |ζi
and |ζ̃i, and let E be the unitary that rotates by angle θ in this subspace, but acts as the identity
outside the subspace. In particular, E|ζ̃i = |ζi. Taking R′ := E R̃, we√see that R′ has the first
column ζ as required. The error is kR′ − R̃k = kE R̃ − R̃k = kE − 1k = 2 − 2 cos θ.
Since hζ̃|ζi ≥ 1 − ǫ2 /2, we find kR′ − R̃k ≤ ǫ. Because the remainder of the circuit is identical,
the overall error between Ũ and U is at most ǫ as claimed.

28


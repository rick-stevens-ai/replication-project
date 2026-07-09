# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:quant-ph/0509206 — Yuki Kelly Itakura, 'Quantum Algorithm for Commutativity Testing of a Matrix Set'
# MSc essay, University of Waterloo, 2005 (70 pages)
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).

---- page 1 ----
arXiv:quant-ph/0509206v1  29 Sep 2005
Quantum Algorithm for Commutativity Testing of
a Matrix Set
by
Yuki Kelly Itakura
An essay
presented to the University of Waterloo
in fulﬁlment of the
essay requirement for the degree of
Master of Mathematics
in
Computer Science
Waterloo, Ontario, Canada, 2018
c⃝Yuki Kelly Itakura 2018

---- page 2 ----
Author’s Declaration for Electronic Submission of an Essay
I hereby declare that I am the sole author of this essay. This is a true copy of the
essay, including any required ﬁnal revisions, as accepted by my examiners.
I understand that my essay may be made electronically available to the public.
ii

---- page 3 ----
Abstract
Suppose we have k matrices of size n × n. We are given an oracle that knows all
the entries of k matrices, that is, we can query the oracle an (i, j) entry of the l-th
matrix. The goal is to test if each pair of k matrices commute with each other or not
with as few queries to the oracle as possible. In order to solve this problem, we use a
theorem of Mario Szegedy [Sze04b, Sze04a] that relates a hitting time of a classical
random walk to that of a quantum walk. We also take a look at another method of
quantum walk by Andris Ambainis [Amb04a]. We apply both walks into triangle
ﬁnding problem [MSS05] and matrix veriﬁcation problem [BS05] to compare the
powers of the two diﬀerent walks. We also present Ambainis’s method of lower
bounding technique [Amb00] to obtain a lower bound for this problem. It turns
out Szegedy’s algorithm can be generalized to solve similar problems. Therefore
we use Szegedy’s theorem to analyze the problem of matrix set commutativity. We
give an O(k4/5n9/5) algorithm as well as a lower bound of Ω(k1/2n). We generalize
the technique used in coming up with the upper bound to solve a broader range of
similar problems. This is probably the ﬁrst problem to be studied on the quantum
query complexity using quantum walks that involves more than one parameter,
here, k and n.
iii

---- page 4 ----
Acknowledgements
The author would like to acknowledge Ashwin Nayak for supervion, Richard Cleve
for reading this essay, Andris Ambainis and Frederic Magniez for consultation on
lower bounds and the diﬀerences between the two quantum walks respectively, as
well as Mike Mosca for the operation of IQC and Mike and Ophelia Lizaridis for
the funding of IQC.
The author would also like to acknowledge both her quantum and classical
friends, especially; Pierre Philipps for “Tempest”, Pranab Sen for regular helps,
Alex Golynski for feeding her brownies, the Crazy Lebanese Exchange Students
(TM) for fun, and all the people she danced with, including Scott Aaronson.
iv

---- page 5 ----
Contents
1
Introduction
1
1.1
The Model, Motivation, and the Main Results . . . . . . . . . . . .
1
1.2
Mathematical Background . . . . . . . . . . . . . . . . . . . . . . .
3
1.2.1
Space and qubit . . . . . . . . . . . . . . . . . . . . . . . . .
3
1.2.2
Superposition and Measurement . . . . . . . . . . . . . . . .
4
1.2.3
Operators and Quantum Gates
. . . . . . . . . . . . . . . .
6
1.2.4
Quantum Algorithms and the Circuit Model . . . . . . . . .
7
1.2.5
Query Model and Quantum Query Complexity . . . . . . . .
8
1.2.6
Reducing Error Probability
. . . . . . . . . . . . . . . . . .
10
2
Related Work
13
2.1
Quantum Walk of Szegedy . . . . . . . . . . . . . . . . . . . . . . .
13
2.1.1
Element Distinctness . . . . . . . . . . . . . . . . . . . . . .
13
2.1.2
Classical Walk Based Algorithm . . . . . . . . . . . . . . . .
14
2.1.3
Hitting Time in Classical Walks . . . . . . . . . . . . . . . .
15
2.1.4
Quantization of the classical walk . . . . . . . . . . . . . . .
20
2.1.5
Hitting Time in Quantum Walks
. . . . . . . . . . . . . . .
24
2.2
Quantum Walk of Ambainis . . . . . . . . . . . . . . . . . . . . . .
32
2.3
Triangle Finding Problem
. . . . . . . . . . . . . . . . . . . . . . .
33
2.3.1
O(n1.3) Algorithm Using Ambainis Walk . . . . . . . . . . .
34
2.3.2
Szegedy Walk Does Not Perform Better . . . . . . . . . . . .
35
2.4
Adversary Method for Query Lower Bounds
. . . . . . . . . . . . .
36
2.4.1
Quantum Adversary Theorem . . . . . . . . . . . . . . . . .
36
2.4.2
The Graph Connectivity . . . . . . . . . . . . . . . . . . . .
41
2.4.3
Lower Bound for Unstructured Search
. . . . . . . . . . . .
43
2.5
Quantum Matrix Veriﬁcation Problem
. . . . . . . . . . . . . . . .
43
2.5.1
Upper Bound . . . . . . . . . . . . . . . . . . . . . . . . . .
44
2.5.2
Lower Bound
. . . . . . . . . . . . . . . . . . . . . . . . . .
45
v

---- page 6 ----
3
Testing Commutativity of Matrices
47
3.1
Commutativity Testing for a Single Pair
. . . . . . . . . . . . . . .
47
3.2
Commutativity Testing of k Matrices . . . . . . . . . . . . . . . . .
48
3.2.1
Two Straightforward Algorithms
. . . . . . . . . . . . . . .
48
3.2.2
Walk Over Separate Rows and Columns
. . . . . . . . . . .
49
3.2.3
Simultaneous Quantum Walk
. . . . . . . . . . . . . . . . .
51
3.3
Generalization of Simultaneous Quantum Walks . . . . . . . . . . .
54
3.3.1
Example Problem . . . . . . . . . . . . . . . . . . . . . . . .
54
3.3.2
Upper Bound . . . . . . . . . . . . . . . . . . . . . . . . . .
54
3.3.3
Lower Bound
. . . . . . . . . . . . . . . . . . . . . . . . . .
56
4
Summary and Future Work
57
Bibliography
59
vi

---- page 7 ----
List of Figures
1.1
Diagrammatic Representations of X, H, and control-NOT respectively.
6
1.2
A Circuit that Implements a Phase Flip
. . . . . . . . . . . . . . .
8
1.3
A Product of Two Reﬂections is a Rotation
. . . . . . . . . . . . .
11
2.1
The Probability of the Walk Stopping in Two Steps . . . . . . . . .
15
2.2
An Example of a Periodic Markov Chain . . . . . . . . . . . . . . .
16
2.3
Pij Moves from One State to Another With a Symmetric Diﬀerence
of Two . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
2.4
A Bipartite Walk . . . . . . . . . . . . . . . . . . . . . . . . . . . .
21
2.5
Transformations between G and G′ . . . . . . . . . . . . . . . . . .
42
vii

---- page 8 ----
List of Algorithms
1
A Classical Walk Algorithm for Element Distinctness . . . . . . . .
14
2
Szegedy’s Quantization of a Random Walk . . . . . . . . . . . . . .
23
3
A Classical Algorithm for Testing If AB = C . . . . . . . . . . . . .
45
4
A Classical Version of the Second Straightforward Algorithm . . . .
48
5
A Classical Walk Over Separate Rows and Columns . . . . . . . . .
50
6
A Classical Simultaneous Walk
. . . . . . . . . . . . . . . . . . . .
51
7
A Classical Algorithm for Solving Collisions with Three Parameters
55
viii

---- page 9 ----
Chapter 1
Introduction
1.1
The Model, Motivation, and the Main Re-
sults
Suppose we are given a set X of size n and we want to test if the set satisﬁes a given
property. We are also given an oracle that computes f(i) for some index i in the
set. For example, in element distinctness [Amb04a], X is a set of integer variables,
{x1, x2, . . . , xn} and the property to test is whether there are two diﬀerent indices
i and j such that xi = xj. In order to decide if X satisﬁes the property, we query
the oracle for values f(i) = xi at various indices i. In general, we are interested
in minimizing the classical or quantum query complexity, the number of queries
a classical or quantum algorithm make to the oracle. This notion will be deﬁned
formally in Section 1.2.5.
We are interested in studying classical and quantum query complexities because
an oracle sometimes gives a separation between them. For example, de Beaudrap,
Cleve and Watrous showed one problem where we need an exponentially many
queries in the bounded error classical case, but only a single query is needed in
the quantum case [dBCW]. Another occasion to study a query complexity is when
obtaining a time complexity is hard. In such a case, the number of queries we make
gives a lower bound for the time complexity. In fact, currently there is no lower
bound method for quantum time complexity that gives super-linear bounding, and
by studying quantum query complexity, we get lower bounds heuristic on quantum
time complexity.
One of the powers of quantum computation comes from the fact that we can
query in superposition. That is, if we are given a set of n elements from 1 to n
denoted [n], we can query an oracle in parallel once to obtain a superposition of
1

---- page 10 ----
CHAPTER 1. INTRODUCTION
2
f(1) through f(n). However, as we will see in Section 1.2.2, we can in a sense only
learn one of the f(i)’s from such a query. The real power of quantum computation
comes from interference. That is, the information in the states, e.g., f(i)’s, can
be combined by means of unitary quantum gates in a non-trivial way, and we can
extract a global property of the inputs. For example, in Deutsch’s algorithm, given
two input bits indexed by 0 and 1, we cannot obtain both f(0) and f(1) in one
oracle query. However, by making a suitable quantum query, we can obtain a global
property, f(0) ⊕f(1) [Deu85]. This interference is also used for quantum search
in an unstructured database, in an algorithm due to Grover [Gro98], to extract a
global property, i.e., if the set we are given contains an element we are looking for.
It turns out we can generalize Grover’s search to test if a set we have satisﬁes
a given property using a quantum version of a random walk, called a quantum
walk.
Using a quantum walk, for example, element distinctness can be solved
in O(n2/3) [Amb04a] queries with a matching lower bound of Ω(n2/3) [AS04]. A
quantum walk was ﬁrst studied on the line, both discrete [ABN+01] and contin-
uous [FG98], analogous to classical discrete and continuous random walks, except
that a quantum discrete walk uses a coin to decide which point to move to next,
whereas a quantum continuous walk does not. The discrete quantum walk on the
line showed that the probability distribution after certain number of steps of quan-
tum walk is diﬀerent from that of the classical probability distribution [ABN+01].
The continuous quantum walk was then applied to a graph that gave an exponential
speed up in a hitting time as compared to the classical counterpart [CFG02]. The
discrete quantum walk on the line was also extended to general graphs [AAKV01]
and later applied to a search on a hypercube [SKW03]. Both discrete [AKR05]
and continuous [CG04] walks were applied to search an item on a grid. Ambai-
nis [Amb04a] used a discrete quantum walk to solve element distinctness. This is
generalized in [MSS05] to ﬁnd a three clique in a graph (triangle ﬁnding). Szegedy
proposed a diﬀerent quantization of a classical Markov chain in [Sze04b, Sze04a].
He showed that there is a quadratic speedup for the hitting time of his quantization
of classical walk. Szegedy’s quantization was applied in [BS05] to verify a prod-
uct of two matrices (matrix veriﬁcation). For more details in the development of
quantum walk based algorithms, see [Amb04b].
The goal of this essay is to investigate the query complexity of testing the
commutativity of k matrices of size n × n. This essay is probably the ﬁrst to study
quantum query complexity that involves two variables, k, the number of matrices
in the set and n, their dimension. We show that there are three upper bounds for
this problem, O(kn5/3), O(k2/3n2) and O(k4/5n9/5), depending on the relationships
between the variables k and n. We also show a lower bound of Ω(k1/2n).
The organization of the essay is as follows. We ﬁrst introduce the mathematical

---- page 11 ----
CHAPTER 1. INTRODUCTION
3
background necessary to understand our quantum algorithms in Section 1.2. Then
we take a look at the details of Szegedy-Walk in Section 2.1 and Ambainis-Walk
in Section 2.2.
We use these two walks to analyze triangle ﬁnding problem in
Section 2.3 to see a case where Amabinis-Walk performs better. In Section 2.4.1,
we take a look at a quantum adversary method [Amb00] to obtain a lower bound
for our problems. We shift our focus to matrices next and in Section 2.5, we study
matrix veriﬁcation problem. In Chapter 3, we ﬁnally study the problem of testing
the commutativity of k matrices of size n × n.
We ﬁrst take a look at a case
where k = 2 by using a modiﬁcation of matrix veriﬁcation in Section 3.1. Next
we study four diﬀerent algorithms for a general k in Section 3.2. This problem is
generalized in Section 3.3. Finally we give a summary and directions for future
work in Chapter 4.
1.2
Mathematical Background
In this section, we will go over the mathematical background necessary to follow
the algorithms in this essay. Beyond the content in this section, [NC00] is a good
reference in general introductory material in quantum computation.
1.2.1
Space and qubit
Classically, information is encoded in a binary string using a sequence of bits 0 and
1. Quantumly, information is encoded in a ﬁnite-dimensional complex vector space,
endowed with the standard inner product, a Hilbert space using qubits. A qubit
may exist in states |0⟩and |1⟩, which are basis vectors for a two-dimensional space.
|0⟩=

1
0

and
|1⟩=

0
1

,
or in any linear combination of these basis states with unit norm. We call the two
vectors |0⟩and |1⟩computational basis for the two-dimensional Hilbert space since
they correspond to the conventional bit representation of information. There are
other pairs of basis states that span the two-dimensional Hilbert space but we focus
on the computational basis. The state of a sequence of n qubits is a unit vector in
the n-fold tensor product space C2 ⊗C2 ⊗. . . ⊗C2. This 2n-dimensional space is

---- page 12 ----
CHAPTER 1. INTRODUCTION
4
spanned by tensor products of states |0⟩, |1⟩. This is the computational basis for
the n-qubit memory. The tensor product of two vectors |φ⟩and |ψ⟩is denoted as
|φ⟩⊗|ψ⟩. When these are computational basis vectors given by bit strings x, y, we
may abbreviate the state |x⟩⊗|y⟩by |x, y⟩or simply |xy⟩. The latter two make
sense when x and y are bit-strings. Using a standard vector notation, a tensor
product of two vectors is obtained by multiplying each entry in the left vector with
the right vector.

a
b
 O


c
d
e

=








a


c
d
e


b


c
d
e










=








ac
ad
ae
bc
bd
be








.
For example, a two qubit state |10⟩is,
|1⟩|0⟩=

0
1

⊗

1
0

=




0
0
1
0



.
This extends in the natural way to tensor products of higher-dimensional vectors.
The dual of the vector |i⟩is denoted by ⟨i|, which is a row vector obtained by taking
a conjugate transpose of |i⟩. For |0⟩this is just a row vector (1 0).
1.2.2
Superposition and Measurement
A Hilbert space of dimension n is spanned by n orthonormal vectors, and we can
express a state in the space as a linear combination of these basis states. For a
two-dimensional Hilbert space with the basis states |0⟩and |1⟩, any state |φ1⟩can
be expressed as
|φ1⟩=
1
p
|α0|2 + |α1|2 (α0|0⟩+ α1|1⟩) ,
where αi is the amplitude of |i⟩. Similarly, a multiple qubit state is also expressed
as a linear combination of its basis states. For example, a two qubit state |φ2⟩can

---- page 13 ----
CHAPTER 1. INTRODUCTION
5
be expressed as a linear combination of four computational basis states,
|φ2⟩=
1
p
|α00|2 + |α01|2 + |α10|2 + |α11|2 (α00|00⟩+ α01|01⟩+ α10|10⟩+ α11|11⟩) .
Deﬁnition 1 (Measurement [NC00]) Given a set of n basis states {|mi⟩}, a
measurement in a basis |m⟩of a state |φn⟩= α1|m1⟩+ . . .+ αn|mn⟩is a projection
of |φn⟩onto one of the basis states by applying projective operators {|mi⟩⟨mi|} to
|φn⟩. The superposition collapses to one of the basis states and the probability of
obtaining |mi⟩is ⟨φn| (|mi⟩⟨mi|) |φn⟩= |αi|2. The state after measurement is then,
|mi⟩⟨mi|φn⟩
|αi|
.
The implication above is that before measuring |φn⟩, the state is in superposition
of its basis states, but measuring collapses the superposition and gives only one of
the basis states as an outcome with the probability according to the amplitude of
the basis states in |φn⟩. Since the probabilities must sum up to one, this means
that the sum of the squares of the amplitudes must also sum up to one,
n
X
i=1
|αi|2 = 1.
Also note that we normalize the collapsed state resulting from the measurement
so that the squares of the amplitudes in this new state also sums up to one.
For a multiple qubit system, we can also measure a small set of qubits only and
leave the rest alone. A measurement in the computational basis of the ﬁrst qubit
collapses the ﬁrst qubit into one outcome of the measurement, the remaining state
is unchanged. Formally, the state is projected onto a subspace consistent to the
measurement outcome. For example, if we have
|ψ⟩= 1
√
2(|00⟩+ |01⟩+ |10⟩+ |11⟩),
measuring the ﬁrst qubit gives 0 with probability 1
2 and 1 with probability 1
2. On
outcome 0, the new state is
|ψ′⟩= 1
√
2
(|00⟩+ |01⟩),

---- page 14 ----
CHAPTER 1. INTRODUCTION
6
X
H
Figure 1.1: Diagrammatic Representations of X, H, and control-NOT respectively.
and on outcome 1, the new state is
|ψ′′⟩= 1
√
2
(|10⟩+ |11⟩).
1.2.3
Operators and Quantum Gates
A quantum gate is a matrix that acts on the state vectors. In order for a matrix
to be a legal (physically realizable) operator, it must be unitary, that is U†U = I,
where U† is the conjugate transpose of a gate U. Some gates that are used for the
construction of the algorithms in this essay are X, Hadamard H, and control-NOT
gates.
X =
 0
1
1
0

, H = 1
√
2
 1
1
1
−1

, C-NOT =




1
0
0
0
0
1
0
0
0
0
0
1
0
0
1
0




The eﬀect of X on computational basis is a logical NOT operation, X|0⟩= |1⟩
and X|1⟩= |0⟩. A Hadamard, H transforms |0⟩into a uniform superposition of
|0⟩and |1⟩i.e.,
(|0⟩+|1⟩)
√
2
and |1⟩into
(|0⟩−|1⟩)
√
2
.
Applying H for each of n qubits
initialized to |0⟩, we can create a uniform superposition of 2n computational bases,

---- page 15 ----
CHAPTER 1. INTRODUCTION
7
i.e.,
1
√
2n
2n−1
X
x=0
|x⟩. C-NOT takes two qubits as inputs and conditioned on the ﬁrst
qubit, it performs a logical NOT operation to the second qubit, e.g., C-NOT|01⟩=
|01⟩because the ﬁrst qubit is 0, and C-NOT|11⟩= |10⟩because the ﬁrst qubit is
1. It is a unitary operation corresponding to a classical gate.
Recall that classically if we are given NOT and AND gates, we can construct a
classical circuit for any boolean function. Such a set of gates is called a universal
set of gates. Similarly, quantumly, we have universal sets of gates. This means that
any unitary transformation on n quantum bits maybe approximated to within a
speciﬁed ǫ > 1 (in the spectral norm, say) by composing a sequence of these gates.
One example involves the use of a C-NOT and a Hadamard with two additional
one-qubit gates called a phase gate S, and π/8 gate T.
S =

1
0
0
i

, T =
 1
0
0
eiπ/4

For the proof of the universality of this gate set, refer Section 4.5 in [NC00].
1.2.4
Quantum Algorithms and the Circuit Model
A quantum algorithm consists of quantum registers that hold qubits, and a series
of unitary operations described by a quantum circuit. The registers are initialized
to |0⟩except for the input register which is initialized to the bits of the problem
instance, as in a classical circuit. The circuit consists of a sequence of gates from a
universal set of quantum gates with the labels of the qubits the gates are applied to.
In Figure 1.2, the registers are represented by black lines. As we apply operators
we move from the left to the right of the circuit. At the end of the algorithm, i.e.,
at the right end of the circuit, a measurement is performed on one or more qubits
in the computational basis, which gives an outcome of the algorithm. An algorithm
is said to compute a boolean function with bounded error if when the input string
x is in the language, the algorithm accepts x (has outcome 1) with probability
more than 3/4, and when x is not in the language, the algorithm accepts (i.e., has
outcome 0) with probability less than 1/4.
For example, suppose we want to implement an algorithm that ﬂips the phase
if the registers both contain |0⟩, but not otherwise. Then Figure 1.2 performs such
algorithm. It ﬁrst applies an X gate to each register, and then applies a Hadamard
gate to the second qubit, followed by a C-NOT conditioned on the ﬁrst qubit,
followed by a Hadamard on the second qubit, and ﬁnally applies X gates to two of

---- page 16 ----
CHAPTER 1. INTRODUCTION
8
X
X
X
X
H
H
1x
2x
Figure 1.2: A Circuit that Implements a Phase Flip
the qubits. This operator can be written as
I −2|00⟩⟨00|.
It is straightforward to check that both the circuit and the above matrix ﬂips
the phase of the qubit if they are both 0.
The quantum time complexity of a (boolean) function is measured by the least
number of gates required to implement an algorithm that computes the function
with bounded error in terms of the size of the input. In Figure 1.2, the input size
is two and the number of gates is seven.
1.2.5
Query Model and Quantum Query Complexity
We ﬁrst formally deﬁne an oracle in terms of an operator.
Deﬁnition 2 (Oracle) [NC00] An oracle O for a function f : {1, . . . , n} →{0, 1}
is a unitary operator that acts on a computational basis such that
O|x⟩|q⟩= |x⟩|q ⊕f(x)⟩,
where |q⟩is an oracle qubit with q ∈{0, 1}, which is ﬂipped conditioned on x ∈
{1, . . . , n}, i.e., ﬂipped if f(x) = 1. An oracle for a function with a larger range,

---- page 17 ----
CHAPTER 1. INTRODUCTION
9
{1, . . . , n} is deﬁned similarly, with O(log n) qubits each for the query and the func-
tion value and ⊕representing a bit-wise XOR.
Using an oracle, we can perform a query algorithm,
Deﬁnition 3 (T-Query Quantum Algorithm)
[BBC+01a] A T-query quan-
tum algorithm A with an oracle O for function f is deﬁned as
A = UTOUT−1 . . . OU1OU0,
where all the transformation are deﬁned on a three register quantum memory con-
sisting of the query register, the oracle response register and workplace qubits for
the algorithms. The Ui’s are unitary transformations independent of the function
f, and the algorithm only depends on the function f through T applications of O.
The query complexity of an algorithm is measured by the number of oracle
operators we apply. The query complexity of computing a property P of the oracle
function f is given by the least query complexity algorithm that computes P(f).
For a search algorithm where an oracle outputs f(x) = 1 if x is a target of the
search and the property being if a given set contains a target element, we usually
prepare an oracle qubit as |0⟩−|1⟩
√
2 , so that we get
O 1
√
2n
2n−1
X
x=0
|x⟩
|0⟩−|1⟩
√
2

→(−1)f(x) 1
√
2n
2n−1
X
x=0
|x⟩
|0⟩−|1⟩
√
2

.
Since the oracle qubit does not change throughout the algorithm, we could
simply think of this oracle as ﬂipping a phase if f(x) = 1.
What would be the action of O in a search algorithm? Suppose we have an
initial state
|ψ⟩=
1
√
2n
2n−1
X
x=0
|x⟩,
and that |ψ⟩is a combination of two vectors, |α⟩and |β⟩, where the former is a
uniform superposition of elements x such that f(x) = 0, and the latter contains the
rest of elements. Then the act of applying the oracle is a reﬂection about the axis
|α⟩because
O(a|α⟩+ b|β⟩) = a|α⟩−b|β⟩.
Recall the phase ﬂip operator from the last section, which up to an overall sign
of −1 is a reﬂection operator. Thus we can create the following reﬂection operator

---- page 18 ----
CHAPTER 1. INTRODUCTION
10
by removing X gates in Figure 1.2.
2|0⟩⟨0| −I.
This construction extends in a straightforward manner to n qubits. In general,
in order to implement a phase ﬂip on qubits that represent n, O(log n) gates are
required.
We can create another reﬂection operator also called Grover diﬀusion operator
that reﬂects the state with the axis |ψ⟩by
H⊕n(2|0⟩⟨0| −I)H⊕n = 2|ψ⟩⟨ψ| −I.
Hence so far we have two reﬂection operators, O and 2|ψ⟩⟨ψ| −I.
Lemma 4 Applying
G = (2|ψ⟩⟨ψ| −I) O
is a rotation in a two-dimensional space spanned by |α⟩and |β⟩by 2θ, where θ is
the initial angle between |ψ⟩and |α⟩.
Lemma 4 also holds for the composition of reﬂections of any two vectors. We
will use this fact later in this essay. In Figure 1.3, the action of G is described
geometrically. It ﬁrst reﬂects |ψ⟩about the axis |α⟩, and then O|ψ⟩is reﬂected
against the original state |ψ⟩. In this one step of G, there is only one query O.
In Grover’s algorithm, this process is repeated O(
√
N) times for N = 2n so as to
rotate the state of the query register close to |β⟩: in the worst case when there is
only one x such that f(x) = 1, θ ≈
1
√n. This gives a query complexity of O(√n).
1.2.6
Reducing Error Probability
In many quantum algorithms, we encounter a problem of reducing the error prob-
ability from a constant such as 1/4 to polynomial close to 0. An algorithm is said
to compute a function f with one-sided error given an input x if the following two
conditions hold,
1. If x is not in the language, it rejects with probability 1.
2. if x is in the language, it accepts with probability at least ǫ > 0.
This means that we have a probability (1 −ǫ) of having a false negative. In order
to reduce the error probability to at most 1/2, we repeat this algorithm for k =

---- page 19 ----
CHAPTER 1. INTRODUCTION
11
\
E
D
\
O
T
T
2
\
G
Figure 1.3: A Product of Two Reﬂections is a Rotation

---- page 20 ----
CHAPTER 1. INTRODUCTION
12
⌈−
1
log (1−ǫ)⌉≈1
ǫ times, because
(1 −ǫ)−
1
log (1−ǫ) ≤1
2.
During any one time in the k repetition of the algorithms, if the algorithm accepts
x, we terminate and decide “yes”. Most of the algorithms in this essay have one-
sided error. For example, in element distinctness, if we ﬁnd two diﬀerent indices i
and j such that xi ̸= xj, we are sure it is in fact true.
In our algorithms, we will often compose bounded error quantum algorithms. In
such cases, a quantum algorithm is used as a subroutine in place of an oracle. We
would have to amplify, by repetition, the success probability of the subroutine so
that the overall algorithm succeeds. This results in an additional factor of O(log T)
in the query complexity where the complexity with an ideal oracle is O(T). Such a
scenario is studied in [HMdW03] as a quantum search with a bounded error oracle.
The main result in [HMdW03] is that we only need to invoke the oracle √n times
as opposed to the obvious approach that gives √n log n.
In this essay, whenever we have a one-sided error and we wish to amplify the
success probability, we assume the procedure is modiﬁed as above. Moreover, if we
have a case of imperfect oracle realized by a bounded error quantum algorithm, we
apply the theorem in [HMdW03].

---- page 21 ----
Chapter 2
Related Work
2.1
Quantum Walk of Szegedy
2.1.1
Element Distinctness
Recall from Chapter 1, the problem of Element Distinctness: given a function f :
[n] = {1, 2, . . . , n} 7→[m], m ≥n, as an oracle, we want to test if f is one-one or not.
If f is not one-one, we say there is a collision. That is, (i, j) collide if f(i) = f(j),
The function f can also be written as a list of numbers: f ≡(f1, f2, . . . , fn). The
goal of the algorithm is to answer this question with as few queries to the oracle as
possible.
The signiﬁcance of this problem is that it is one of the applications of quantum
walks that gives better bounds than classical counterparts. Underlying this quan-
tum algorithm is a random walk. Ambainis was the ﬁrst to adopt this classical walk
into a quantum algorithm [Amb04b]. Classically, the straightforward algorithm to
solve Element Distinctness is to go through the list one by one. Interestingly, this
straightforward algorithm performs better than a random walk based algorithm
classically which we will see in Section 2.1.2.
Fact 5 Classical query complexity of element distinctness is Θ(n).
Since it is optimal an unordered search may be reduced to element distinctness.
However, in quantum scenario, quantum walk based algorithm performs better
than the above bound. Quantum walk based algorithm is a quantum version of a
random walk based algorithm, which is described below.
13

---- page 22 ----
CHAPTER 2. RELATED WORK
14
2.1.2
Classical Walk Based Algorithm
The following is a classical algorithm based on random walk for ﬁnding a collision.
This walk is irreducible in the sense that there is a path between any pair of subsets.
Algorithm 1 A Classical Walk Algorithm for Element Distinctness
1: Pick a uniformly random set I of r elements out of [n] (call it an r-subset).
2: Query f at points in I.
3: if There is a collision within I then
4:
return “Collision found” and elements that collide
5: end if
{Walk on r-subsets of [n].}
{(idea) Pick an element in the set and one not in the set uniformly at random
(u.a.r.). Swap these elements. Note that we are maintaining the size of the
subset.}
6: for t ≤T do
7:
Pick i ∈I and j ∈[n] −I u.a.r.
8:
I ←(I −{i}) ∪{j}.
9:
Query fj.
10:
if There is a collision within I then
11:
Output the elements that collide.
12:
return
13:
end if
14: end for
15: print “No collision” {i.e., f is one-one.}
Let T be the ﬁrst time the walk “hits” an r-subset containing a collision (hitting
time).
Observation
Pr(walk stops in two steps | any state) ≥1 ·
2
n −r · r −1
r
·
1
n −r.
This is because in the worst case, there are exactly two elements that collide
with each other, and initially, we do not have any element that form a colliding
pair in the r-subset. Next we pick one of the two colliding elements from n −r
elements not in the set with probability
2
n−r. In the second step, we ﬁrst choose an
element in the r-subset that is not part of the colliding set with probability r−1
r ,
and then we pick the other colliding element not in the r-subset with probability

---- page 23 ----
CHAPTER 2. RELATED WORK
15
1
1
2
2
2
1
1
2
first step
second step
Figure 2.1: The Probability of the Walk Stopping in Two Steps
1
n−r and swap these. In Figure 2.1, 1 and 2 are colliding elements not in the subset
initially. It describes a sequence of transformation by which they are found by the
algorithm. The hitting time for the walk is
E(T ) ≤(n −r)2r
2(r −1) .
There are more sophisticated arguments that give a better bound on T . We
will analyze hitting times more precisely.
2.1.3
Hitting Time in Classical Walks
Consider a Markov Chain on the state space X, (|X| = N) given by the transition
matrix P, where P = (px,y), x, y ∈X and
px,y = Pr(making a transition to y | current state = x).
This corresponds to general Markov Chains, in the sense that if we are at x, we
move to any arbitrary state y in the state space with probability px,y. P is called
a stochastic matrix, i.e.,
X
y
px,y = 1 for all x. So all the rows sum up to 1.
We assume that the Markov Chain is
1. Symmetric: px,y = py,x. This makes the underlying graph of the walk undi-
rected.
2. Irreducible: There is a path between every pair of states.

---- page 24 ----
CHAPTER 2. RELATED WORK
16
1
1
Figure 2.2: An Example of a Periodic Markov Chain
3. Aperiodic: There exists x ∈X and tx ≥1 such that
Pr(We reach x in t steps starting from x) > 0
for all t ≥tx. Aperiodicity of the walk is equivalent to having an underlying
graph that is not bipartite. This implies the same property for all y ∈X if
the second property holds.
What are the properties of such Markov Chains?
1. Since P is symmetric, it is equal to its transpose, P = P T. So P is doubly
stochastic; both rows and columns sum up to 1.
2. Let s be any initial distribution, then sTP t 7−→πT = ( 1
N , 1
N , . . . , 1
N ) as t →∞
in the l1 metric. The distribution π is called stationary distribution, which is
a ﬁxed point in a Markov Chain. So we have uniform stationary distribution.
3. πTP = πT = ( 1
N , 1
N , . . . , 1
N ): π is an eigenvector of P with eigenvalue of 1.
Since P is symmetric, it is Hermitian, therefore it is diagonalizable and all
the eigenvalues are real. Moreover, the other eigenvalues are strictly less than
1: λ1 = 1 > λ2 ≥. . . ≥λn > −1. The eigenvalue of 1 is obtained from the
irreducibility property. Aperiodicity implies all the eigenvalues are > −1.
In general, a marked state M ⊆X is a subset. For element distinctness, M
contains two colliding elements. Since we stop at a marked state, the transition
matrix for this state is diﬀerent from others. Suppose we would like to search for
one of the marked states by simulating the walk and stopping when we see a state

---- page 25 ----
CHAPTER 2. RELATED WORK
17
x ∈M. The transition matrix now looks like
˜
PM =
 PM
P ′
0
I

,
(2.1)
where (PM P ′) are the rows of P corresponding to X −M, PM is P from which
rows and columns corresponding to M have been removed. The rows corresponding
to the states in M are (0 I) since once we reach M, we do not move to any other
state.
What is the hitting time of M? Let T be the hitting time for ﬁnding a marked
state starting in distribution s.
Fact 6
E(T) = sT
M(I −PM)−1 · 1,
where sM is the projection of s onto X −M, and 1T = (1, 1, . . . , 1). When M is
non-empty, and since the Markov Chain is ergodic all the eigenvalues of PM have
absolute value less than 1. Therefore the expression is well-deﬁned.
Proof :
For any non-negative integer-valued random variable T, E(T) =
∞
X
t=0
Pr(T >
t). In our case, Pr(T > t) is the probability we have not reached the marked state
after t steps. This is also the probability that we are still in one of the states in
X −M. Since the state distribution after t steps is sT ˜P t, where
˜P t =

P t
M
P ′(t)
0
I

.
Let 1X−M denote a vector that contains 1 for the ﬁrst |X −M| entries and 0
for the rest. Then we have
Pr(We are not in a marked state after t steps) = sT ˜P t1X−M = sT
M ˜P t
M1.
Then,
E(T)
=
∞
X
t=0
sT
MP t
M1
= sT
M(
∞
X
t=0
P t
M)1
= sT
M(I −PM)−11.

---- page 26 ----
CHAPTER 2. RELATED WORK
18
□
Stationary distribution for P is a uniform distribution over all elements. Thus
by judicially choosing initial state to be the stationary distribution, we get a good
bound on hitting time.
Corollary 7 a. If s = ( 1
N , 1
N , . . . , 1
N ), then hitting time E(T) is
E(T) = 1
N · 1 · (I −PM)−1 · 1.
b. Let 1M =
(1,...,1)
√
N . If the eigenvalues/vectors of PM are (λi, vi) and 1M =
N−m
X
i=1
νivi then,
E(T) =
N−m
X
i=1
ν2
i (
1
1 −λi
),
(2.2)
where N is the normalization factor, m = |M| is the size of marked subsets, and λi
is the i-th largest eigenvalue of PM in magnitude.
Note in the ﬁrst part of Corollary 7, the eigenvalues of (I −PM)−1 are
1
1−λi, for
each eigenvalue λi of PM. Also since we are working with real symmetric matrices,
all the numbers νi are real.
The matrix PM is real, all the absolute values of eigenvalues of PM are strictly
less than 1, and along with the symmetry of PM, it is orthogonally diagonalizable.
This means we can choose vi such that they form an orthonormal set. Note that
the spectral norm of a matrix is the largest singular value of the matrix. Since PM
is symmetric, it is equivalent to the largest eigenvalue. Hence ∥PM∥= λ1. Since
X
ν2
i is at most 1, we have, E(T) ≤
1
1−λ1 =
1
1−∥PM∥.
In order to bound the hitting time, then we need to bound the largest eigenvalue
of PM.
Lemma 8 ([Sze04b]) If the spectral gap(= 1−λ2(P)) of P is ≥δ, and if |M|
|X| ≥ǫ,
then ∥PM∥≤1 −δǫ
2 .
In the above lemma, we deﬁne λi(P) to be i-th largest eigenvalue of P in mag-
nitude. Note that since P has a uniform distribution, λ1 = 1. So the spectral
gap, which is formally, the diﬀerence between the largest and the second largest
eigenvalues in magnitude, is λ1(P) −λ2(P) = 1 −λ2(P).

---- page 27 ----
CHAPTER 2. RELATED WORK
19
   r-1 
elements
Figure 2.3: Pij Moves from One State to Another With a Symmetric Diﬀerence of
Two
To bound the hitting time of the walk , we would like an explicit formula for
the spectral gap of P to compute the upper bound of the spectra for PM. Recall
the state space of the walk is X = {r-subsets of [n]}. Given an r-subset, there
are r(n −r) other r-subsets to transition to by swapping one of the r elements in
the current subset with one of the n −r elements not in the subset. Each of these
r(n−r) subsets have equal probability of being moved to from the current r-subset.
Then
N = |X| =
n
r

,
and
pi,j
=

1
r(n−r)
if |i ∩j| = r −1
0
= Jn,r,r−1
r(n−r) ,
where Jn,r,r−1 is a boolean matrix with entry 1 iﬀi and j are subsets of size r,
whose intersection is of size r −1.
Theorem 9 ([Knu91]) There are r + 1 eigenspaces of Jn,r,r−1, eigenvalues corre-
sponding to
λj = (r −j)(n −r) −j(r −j + 1), 0 ≤j ≤r.
We have r ≤n
2, otherwise we have a high probability of solving the problem in
Line 3 in Algorithm 1. Also, λj is a decreasing function of j. The eigenvalues

---- page 28 ----
CHAPTER 2. RELATED WORK
20
are not all positive, e.g., for j = r, we have λr = −r.
However, we are only
interested in the ﬁrst and the second largest eigenvalues, which are, λ0 = r(n −r)
and λ1 = r(n −r) −n. Since these are eigenvalues for Jn,r,r−1 and P = Jn,r,r−1
r(n−r) ,
the second largest eigenvalue for P is r(n−r)−n
r(n−r) . From these, we can compute the
spectral gap: 1 −
λ1
r(n−r) =
n
r(n−r) > 1
r. Remembering that M is the set of r-subsets
that contain a colliding pair of elements, in order to lower bound the fraction of
marked elements, we need to consider the worst case scenario where we have exactly
one pair of colliding elements.
|M|
|X| ≥
  n
r−2

 n
r
 =
r(r −1)
(n −r −2)(n −r −1) ≥r2
2n2
for r = o(n) when approximation involved.
From this, we have
∥PM∥
≤1 −
r2
2n2
1
r
2
= 1 −
r
4n2.
So
E(T) ≤
1
1 −∥Pm∥≤4n2
r
= O
n2
r

.
This is a bound on the hitting time of the algorithm. The query complexity of
the algorithm is calculated as follows. We need to make r initial queries for the
values of each element in the initial r-subset. At each of the O( n2
r ) iteration of the
walk, we need to query the value of the new element we swapped into the subset.
Thus, we have O(r + n2
r ) query complexity. This is minimized when r = n and
gives O(n) query complexity. This is equivalent to checking every element in the
entire set, thus giving no speedup to the straightforward algorithm of sequentially
checking every element in the set.
Now we are interested in the quantization of the classical algorithm we have
discussed thus far.
2.1.4
Quantization of the classical walk
The ﬁrst quantization of random walk in Algorithm 1 was proposed by Ambai-
nis [Amb04b], which is described in Section 2.2. A new kind of quantization of
classical walks was proposed by Szegedy [Sze04b], which we present here in detail.
The walk is over a bipartite graph. Each side of the graph contains r-subsets as
vertices. A pair of vertices in the left and the right hand side of the graph are con-

---- page 29 ----
CHAPTER 2. RELATED WORK
21
1y
2y
3y
x
1
,y
xP
2
,y
xP
3
,y
xP
Figure 2.4: A Bipartite Walk
nected only if one can be changed into another on the opposite side by removing
one of the elements in the subset and adding one that is not in the current set. This
is equivalent to having two vertices connected if they diﬀer in exactly two elements.
The probability of moving from a subset x in the left side of the graph to a subset y
in the right side of the graph is given by px,y. For each side of the graph, we create
a state,
|φx⟩=
X
y
√px,y|x⟩|y⟩
for the transition from x on the left side to all of its neighbors y on the right side
of the graph, and
|ψy⟩=
X
x
√px,y|x⟩|y⟩
similarly. Note that,
a. {φx}x and {ψy}y are orthonormal sets because each |x⟩and |y⟩are distinct.
b. Let E1 = span{φx}x and E2 = span{ψy}y and π1, π2 to be orthonormal
projections onto E1, E2 respectively. We deﬁne two unitary operators R1 and R2
as R1 = 2Π1 −I and R2 = 2Π2 −I.
Then R1 is unitary because it can be implemented using the combination of
unitary gates similar to the reﬂection operator in Section 1.2.4. We can see that

---- page 30 ----
CHAPTER 2. RELATED WORK
22
R1 is actually a reﬂection operator about the space E1 because
R1|ϕ⟩
= (2π1 −I)|ϕ⟩
= (2
X
x
|φx⟩⟨φx| −I)|ϕ⟩
=
X
x
(2|φx⟩⟨φx| −I)|ϕ⟩
=

|ϕ⟩
if ϕ ∈E1
−|ϕ⟩
if ϕ ∈E⊥
1
Similarly R2 is unitary and is a reﬂection about the space E2.
Deﬁnition 10 (Quantitization of a M.C. P)
WP = R2R1
Why is this a natural deﬁnition? The straightforward way to deﬁne a step of
the walk is
|x⟩|0⟩
→|x⟩
X
y
√px,y|y⟩
→|x⟩
X
y
√px,y|y⟩
X
z
√py,z|z⟩
→|x⟩
X
y
√px,y|y⟩
X
z
√py,z|z⟩
X
a
√pz,a|a⟩
But this is just a simulation of a classical walk. Instead, we keep the memory
of the previous step only. To do so, we need an operator that diﬀuses x into all the
neighbors y and vice versa.
Another way to see that the deﬁnition of the quantized walk is natural is to
look at the Grover diﬀusion operator as an operator to move from a vertex in a
complete graph to one of the adjacent vertices with equal probability. This idea
was introduced in [Wat01]. Algorithm 2 describes Szegedy’s algorithm.
Szegedy deﬁnes the quantum hitting time as follows.
Deﬁnition 11 ([Sze04a]) T is an c-deviation-on-average time with respect to |φ⟩
if
1
T + 1
T
X
t=0
∥W t
p|φ⟩−|φ⟩∥2
2 ≥c.
This was deﬁned so that after T steps of the walk, the average deviation of
the initial state is very high. That is, the state is signiﬁcantly skewed towards the

---- page 31 ----
CHAPTER 2. RELATED WORK
23
Algorithm 2 Szegedy’s Quantization of a Random Walk
1: Let |φ0⟩=
1
√
N
X
x
|φx⟩=
1
√
N
X
x,y
√px,y|x⟩|y⟩=
1
√
N
X
y
|φy⟩
2: Measure if the ﬁrst register is marked or not.
3: if The ﬁrst register is marked then
4:
return ‘‘Found marked element.’’
5: end if
6: Apply H ⊗I to |0⟩|φ01⟩to get
1
√
2(|0⟩|φ01⟩+ |1⟩|φ01⟩)
7: Pick t u.a.r. from [0, . . . , T]
8: for i ≤T do
9:
Apply controlled-W ˜P conditioned on the ﬁrst register.
{The modiﬁed matrix ˜P in Equation 2.1 lets us remain in the same state
once we arrive at the marked state.}
10: end for
{ Now we have
1
√
2(|0⟩|φ01⟩+ |1⟩W t
˜P|φ01⟩)}
11: Apply H ⊗I to get 1
2|0⟩(|φ01⟩+ W t
˜P|φ01⟩) + 1
2|1⟩(|φ01⟩−W t
˜P|φ01⟩)
12: Measure the ﬁrst register.
13: if There is a ’1’ in the ﬁrst register then
14:
return ‘‘Detected marked element.’’
15: else
16:
return ‘‘No marked element.’’
17: end if

---- page 32 ----
CHAPTER 2. RELATED WORK
24
marked state and so the probability of observing the marked state is high. Since the
walk is realized by unitary evolution it cannot end up in a marked state. Instead,
it can cycle through states with high amplitude on marked states.
Next we compute the complexity of this algorithm. One step of the walk is R1
followed by R2. We show here that R1 can be implemented eﬃciently. R2 can be
implemented similarly. Recall that
R1
= (2Π1 −I)
=
 
2
X
x
|φx⟩⟨φx| −I
!
=
X
x
(2|φx⟩⟨φx| −Ix) ,
where Ix is identity on |x⟩⊗Cx. The last line follows from the fact that we are
working on
CX×X
∼= CX ⊗CX
∼= L
x |x⟩⊗CX,
so R1 which acts on CX ⊗CX can be decomposed into the direct sum of |X| diﬀusion
operators, 2|φx⟩⟨φx| −Ix. Since this is the reﬂection in |x⟩⊗CX about |φx⟩, this
can be written as
|x⟩⟨x| ⊗
 Ux(2|0⟩⟨0| −I)U†
x

,
and 2|0⟩⟨0| −I can be implemented using O(log |X|) gates similarly to the con-
struction of a circuit for 2|00⟩⟨00| −I in Section 1.2.4.
From the above argument, we see that if there is an eﬃcient procedure to
implement the transformation
(I ⊗Ux) |x⟩|0⟩= |x⟩
X
y
√px,y|y⟩,
then the algorithm can be implemented eﬃciently.
2.1.5
Hitting Time in Quantum Walks
In order to analyze the deviation time, it suﬃces to take a look at the eigenvalues
and eigenvectors of one step of the walk. This is because for a unitary operator
U =
X
j
eiθj|vj⟩⟨vj| with {|vj⟩} being the orthonormal eigenvectors of U, Ut =

---- page 33 ----
CHAPTER 2. RELATED WORK
25
X
j
eiθjt|vj⟩⟨vj| so it has the same set of eigenvectors.
Recall that WP = R2R1 = (2Π2 −I)(2Π1 −I), where Πi is an orthogonal
projection to Ei, and E1 is the space spanned by |φx⟩and similarly for E2. Let
A =
X
x
|φx⟩⟨x| and B =
X
y
|φy⟩⟨y|. Note that the dimension of the space in
which |φx⟩lies is N2 and that of ⟨x| is N. Then we can write WP = R2R1 as
(2AA† −I)(2BB† −I) because Π1 =
X
x
|φx⟩⟨φx| = AA†, and similarly for Π2.
Note that A and B are norm-preserving operations because A†A = I = B†B and
A maps a vector in Cx into its subspace E1 and similarly for B.
Suppose a vector v ∈(E1 + E2)⊥. Then v lies in the space orthogonal to both
E1 and E2. Since Ri reﬂects a vector orthogonal to Ei, then v is reﬂected by both
R1 and R2. Then applying a walk operator WP = R2R1 does not change v. Hence
WP|v⟩= |v⟩, and the subspace spanned by such v’s is an invariant subspace, an
eigenspace with eigenvalue 1. Thus we only need to analyze the behavior of WP in
E1 + E2. Suppose we have |w⟩, |v⟩∈CX, then we want to analyze the action of R2
on A|w⟩and the action of R1 on B|v⟩. (Since A|w⟩∈E1, the action of R1 on A|w⟩
is identity.) Since
R2A|w⟩
= 2Π2A|w⟩−A|w⟩
= 2B(B†A)|w⟩−A|w⟩,
where the ﬁrst term of the last line lies in E2 and the second term in E1, and
similarly,
R1B|v⟩= 2A(A†B)|v⟩−B|v⟩,
we deﬁne the discriminant of A and B as follows.
Deﬁnition 12 The discriminant matrix D of A and B is D = A†B.
Theorem 2.1.1 If D =
X
j
δj|wj⟩⟨vj| is the singular value decomposition of D,
then
a) 0 ≤δj ≤1.
b) The space generated by {Awj, Bvj}, for all j where (wj, vj) is a pair of singu-
lar vectors is invariant under WP. And WP restricted to this space is a composition
of a reﬂection about Awj followed by a reﬂection about Bvj.
Let the angle between Awj and Bvj be θj, that is the singular value correspond-
ing to Awj and Bvj be ⟨wj|A†B|vj⟩= ⟨wj|D|vj⟩= cos θj, for θj ∈[0, π/2]. Recall
from Lemma 4 that a product of two reﬂections about two reﬂectors |φ⟩and |ψ⟩

---- page 34 ----
CHAPTER 2. RELATED WORK
26
is a rotation by an angle 2θ, where θ is an angle between the vectors |φ⟩and |ψ⟩.
Similarly then WP is a rotation by 2θj in this subspace.
Proof : [Theorem 2.1.1-a] Singular values are taken to be real and non-negative
by convention, so δj ≥0.
Since A, B are norm-preserving ∥Aw∥= ∥w∥and
∥Bv∥= ∥v∥. Using these facts,
δj
≤max{|α⟩,|β⟩} |⟨β|D|α⟩|
= max{|α⟩,|β⟩} |⟨β|A†B|α⟩|
≤max{|α⟩,|β⟩} ∥A|β⟩∥· ∥B|α⟩∥
≤1.
Hence δj ≤1.
□
Proof : [Theorem 2.1.1-b] As we mentioned before, we only need to consider the
action of WP on Awj and Bvj and that Awj is invariant by R1 and Bvj is invariant
by R2.
WP|Awj⟩
= (2Π2 −I)A|wj⟩
= (2(BB†) −I)A|wj⟩
= 2B(B†A|wj⟩) −A|wj⟩
= 2BD†|wj⟩−A|wj⟩
= 2δjB|vj⟩−A|wj⟩
= (cos θjB|vj⟩) −(A|wj⟩−cos θjB|vj⟩).
The ﬁrst term in the last line is the component of A|wj⟩that is along B|vj⟩
and the second term is the component of A|wj⟩that is orthogonal to B|vj⟩. So, on
A|wj⟩, R1 is a reﬂection about A|wj⟩(identity in this case), and R2 is a reﬂection
about B|vj⟩(because of the orthogonal component) in the subspace. Similarly, on
B|vj⟩, R1 is a reﬂection about A|wj⟩(because of the orthogonal component), and
R2 is a reﬂection about B|vj⟩(identity) in the subspace.
□
Using Theorem 2.1.1, we are ready to estimate the deviation time with the
initial state,
|φ01⟩
=
1
√
N
X
x∈X−M
|x⟩
X
y∈X
√px,y|y⟩
=
1
√
N
X
x∈X−M
|φx⟩,
because |φ01⟩is the state that remains after the measurement in Step 3 of Algo-

---- page 35 ----
CHAPTER 2. RELATED WORK
27
rithm 2. We would like to bound T such that
1
T + 1
T
X
t=0
∥W t
˜P|φ01⟩−|φ01⟩∥2 ≥c(1 −ǫ)
for some small positive constant c and ǫ being the fraction of marked elements. This
is because by Szegedy’s deﬁnition in Deﬁnition 11, the hitting time is the time it
takes for the state to be signiﬁcantly diﬀerent from the initial state, greatly skewed
towards the marked state. That is, we want the L2 norm of the diﬀerence between
the ﬁnal and the initial state to be at least as large as the fraction of unmarked
elements. This ensures that when we measure the ﬁnal state, we detect a large
deviation from the initial state. The term in the summation is 2(1−ǫ−⟨φ01|W t
˜P|φ01⟩)
because |φ01⟩=
X
x∈X−M
1
√
N
|φx⟩and so ∥|φ01⟩∥2 = 1−ǫ, so we need to upper bound
1
T+1
T
X
t=0
⟨φ01|W t
˜P|φ01⟩.
Now
D(x, y)
= ⟨x|D|y⟩
= ⟨x|A†B|y⟩
= ⟨x|
 X
z
|z⟩⟨φz|
!  X
u
|φu⟩⟨u|
!
|y⟩
= ⟨φx|φy⟩
= ⟨x|
 X
y
√px,y⟨y|
!  X
x
√py,x|x⟩
!
|y⟩
= √px,y√py,x,
then for D ˜P, the (x, y) entry is p˜px,y
p˜py,x. Since if exactly one of x or y is marked,
p˜px,y or p˜py,x is 0, the entry of D ˜P is zero if exactly one of x or y is marked. Also
since PM, and I are symmetric, for (x, y) both being unmarked or marked, we have
PM or I respectively as diagonal blocks in D ˜P. So
D ˜P =
 PM
0
0
I

.
Now we are ready to use Theorem 2.1.1. Let the normalized eigenvectors of
PM be {v′
k}k with eigenvalues λk, and denote vk for v′
k padded with 0 to make
an eigenvector of D ˜P. Since PM is symmetric, all the eigenvectors are orthogonal.
The rest of the eigenvectors of D ˜P are {|x⟩}x for x ∈M. These vectors are also

---- page 36 ----
CHAPTER 2. RELATED WORK
28
orthogonal to each other, and all n eigenvectors of D ˜P are orthogonal to each other
as well. So its eigenvectors are the singular vectors and the absolute value of the
eigenvalues give the singular values because some eigenvalues may be negative.
Then from Theorem 2.1.1, the invariant subspaces of W ˜P are the subspaces Fk
spanned by the pairs (Avk, Bvk) with singular value |λk| for all k and the subspaces
Fx spanned by the pairs (A|x⟩, B|x⟩) with singular values 1 for all x ∈M. Since
the product of two reﬂections is a rotation as we have seen before, the action of
W ˜P is a rotation of the subspace Fk by 2θk, where θk is the angle between Avk and
Bvk:
⟨vk|A†B|vk⟩= cos θk,
This is also equal to the singular value of A†B = D corresponding to vk, θk =
cos−1 |λk|. Also θk ∈(0, π/2] cannot be zero because cos θk = |λk| < 1 and from
Theorem 8, ∥PM∥= λ1 = 1 −δǫ
2 < 1 assuming that ǫ ̸= 0. So W t
˜P rotates the
subspaces by 2θkt.
Observation
a)
|φ01⟩∈span{Avk}k
because
|φ01⟩
=
1
√
N
X
x∈X−M
|φx⟩
=
1
√
N
X
x∈X−M
 X
z
|φz⟩⟨z|
!
|x⟩
=
1
√
N
X
x∈X−M
A|x⟩
and |x⟩∈spank{vk} for n ∈X −M. So |φ01⟩is spanned by Avk for all k.
b)
∥|φ01⟩∥2 = 1 −ǫ
because
∥|φ01⟩∥2
= 1
N
X
x∈X−M
⟨φx|φx⟩
= |X−M|
N
= 1 −ǫ.
So we normalize the initial state and also write this as the linear combination
of the spanning set,
|φ01⟩
√1 −ǫ =
X
k
νkA|vk⟩.
(2.3)

---- page 37 ----
CHAPTER 2. RELATED WORK
29
Note that the square of the amplitudes sum up to 1 so
X
k
ν2
k = 1. Let |zk⟩=
A|vk⟩. Then |zk⟩are orthonormal to each other because |vk⟩are orthonormal to
each other. A preserves inner products:
⟨zk|zk′⟩
= A†A⟨vk|vk′⟩
= ⟨vk|A†A|vk′⟩
= ⟨vk|vk′⟩
= 0.
Claim 13 If T ≥100
X
k
ν2
k
θk
,
1
T+1
T
X
t=0
∥W t
˜P|φ01⟩−|φ01⟩∥2
= 2
 
(1 −ǫ) −
1
T+1
T
X
t=0
⟨φ01|W t
˜P|φ01⟩
!
≥c(1 −ǫ),
for some constant 2 ≥c > 0.
This means
1
T + 1
T
X
t=0
⟨φ01|W t
˜P|φ01⟩<

1 −c
2

(1 −ǫ) .
Proof :
From Equation 2.3
⟨φ01|W t
˜P|φ01⟩
=
1
1−ǫ
X
k1,k2
νk1νk2⟨zk1|W t
˜P|zk2⟩
=
1
1−ǫ
X
k
ν2
k⟨zk|W t
˜P|zk⟩
=
1
1−ǫ
X
k
ν2
k cos (2θkt),
because |zk⟩’s are orthonormal to each other and belong to orthogonal eigenspaces of
W ˜P. The last line is obtained from the fact that the angle between |zk⟩and W t
˜P|zk⟩
is 2θkt since one step of W ˜P rotates the subspace by 2θk, and so ⟨zk|W t
˜P|zk⟩=
cos (2θkt).

---- page 38 ----
CHAPTER 2. RELATED WORK
30
Now we use three mathematical identities to bound
T
X
t=0
cos (2θkt). First,
cos (ωt) = eiωt + e−iωt
2
.
So the sum of cosines is a sum of two geometric series. Using the formula for
the sum of geometric series we have,
1
T+1
T
X
t=0
⟨φ01|W t
˜P|φ01⟩
≤(1 −ǫ)
X
k
ν2
k
1
T + 1
cos (2θkT) −cos (2θk(T + 1)) + 1 −cos (2θk)
2(1 −cos (2θk))
.
Next, we use
| cos α −cos β| ≤|α −β|
to bound the numerator and use
cos α ≤1 −α2
8 for α ∈[−3.79, 3.79],
to bound the denominator. Note that here, α = 2θk and θk ∈(0, π
2] as mentioned
before, so the third inequality can be applied.
Using these, we get
1
T+1
T
X
t=0
⟨φ01|W t
˜P|φ01⟩
≤(1 −ǫ)
1
T+1
X
k
ν2
k
2θk + 2θk
2((2θk)2)/8
= (1 −ǫ)
4
T+1
X
k
ν2
k
θk
≤(1 −ǫ) 4
100.
The last line comes from the fact that we have chosen T ≥100
X
k
v2
k
θk
. So the
claim holds for
 1 −c
2

=
1
25 or c = 48
25.
□
We can relate the hitting time of the walk with the eigenvalues of PM.
Corollary 14 c-deviation on average time for W ˜P with respect to |φ01⟩
√1−ǫ is O

1
√
1−∥PM∥

.

---- page 39 ----
CHAPTER 2. RELATED WORK
31
Proof :
We know that T ≥100
X
k
ν2
k
θk
and that cos θk = |λk|. Then
θk ≥sin θk
= √1 −cos2 θk
=
p
1 −λ2
k
≥√1 −λk,
because λk ≤1.
So,
T ≤100
X
k
ν2
k
p
1 −λ2
k
≤
100
p
1 −∥PM∥
X
k
ν2
k
because
X
k
ν2
k = 1 and any eigenvalue in PM is at most the largest eigenvalue of
PM which is ∥PM∥. This means that the hitting time T ∈O

1
√
1−∥PM∥

.
□
Recall that the classical hitting time for a symmetric transition matrix is O

1
1−∥PM ∥

,
so using Szegedy’s walk we have quadratic speedup.
Theorem 15 ([Sze04a]) For the quantum walk based on a transition matrix P
with eigenvalue gap of δ, the fraction of marked elements |M|/|X| at least ǫ, in
time O

1/
√
δǫ

, Algorithm 2 detects a marked element with probability at least
1
1000 if it exists, in O(1/
√
δǫ) application of W ˜P.
Proof :
If a marked element exists, either a marked element is detected in
Step 2 with probability ǫ, or a deviation is detected in Step 11 with probability
≥
1
4(T+1)
T
X
t=0
∥W t
˜P|φ01⟩−|φ01⟩∥2 ≥12
25(1 −ǫ). Then the net probability of success is
ǫ + 12
25(1 −ǫ) ≥12
25 + 13ǫ
25 . Here, T = O(
1
√
1−∥PM∥) from Corrollary 14 and Lemma 8.
□
The consequence of Theorem 15 is that it suﬃces to analyze the classical version
of the walk in order to bound the quantum hitting time. Suppose we have three
diﬀerent costs, time or query, associated with a classical walk based algorithm. A
setup cost, s(r), an update cost u(r) and a checking cost c(r). A setup cost is the
cost required to set up the initial r-subset, an update cost is the cost to maintain
the data pertaining to the r-subset during the walk, and a checking cost is the cost

---- page 40 ----
CHAPTER 2. RELATED WORK
32
needed to see if we have a marked subset. Then the total quantum complexity of
this algorithm is
s(r) +
1
√
δǫ
(u(r) + c(r)) .
(2.4)
Throughout the rest of the essay, we will describe the classical versions of the
algorithms to obtain quantum upper bound.
As an application to element distinctness, using Theorem 15, we get O(n2/3)
bound. If we use the classical walk, however, we get a query complexity of O(n4/3),
which is worse than the straightforward algorithm that gives O(n). Because in
quantum case, we have a smaller hitting time, a walk based approach performs
better.
2.2
Quantum Walk of Ambainis
There is another quantum walk algorithm proposed by Ambainis [Amb04b] to solve
Element Distinctness, which came prior to [Sze04b, Sze04a]. This is generalized
in [MSS05, CE03] to solve any k-collision problem and is called Generic Algorithm.
Deﬁnition 16 (k-collision)
[CE03] Given a function f on a set S as an oracle
and a k-ary relation C ⊆Sk, ﬁnd a k-tuple of distinct elements (a1, a2, . . . , ak) ∈Sk
such that (f(a1), f(a2), . . . , f(ak)) ∈C if it exists. Otherwise, reject.
In the circuit for the generic algorithm, there are three main registers, a set
register, a data register and a coin register. The set register holds a subset I of
the set S, of size r or r + 1. The data register holds the data corresponding to
the set in the set register. The coin register holds an element of S −I. In element
distinctness, for example, the set register contains indices of elements i in r-subset,
the data register contains the actual value xi for each element in the set register,
and the coin register contains the indices j’s that are not in the set register.
The walk starts with a uniform superposition of r-subset in the set register and
sets up the corresponding data register as in Szegedy-walk. Unlike Szegedy-walk,
this algorithm also sets up a coin register C. At each step of the walk, if the subset
is marked, i.e., contains a k-tuple in C, then it ﬂips the phase by applying a phase
ﬂip operator similar to the one in Section 1.2.4. Then it enters quantum walks to
ﬂip the coin. It diﬀuses the coin register over indices in S −I by applying a Grover
diﬀusion operator similar to the one in Section 1.2.5 and adds the element from
the coin register to the set register. Now the size of the set register is augmented
to r + 1. Then it diﬀuses the set register over I, and removes one element from
the set register. Note that during this diﬀusion step, the data register is updated

---- page 41 ----
CHAPTER 2. RELATED WORK
33
correspondingly. This process is repeated for some time before checking the subset
for a marked state. When the size of r-subset is 1, this is analogous to what Grover’s
algorithm does.
Similarly to Equation 2.4, we can write the expression for the total cost of
Ambainis-walk using a setup cost, an update cost and a checking cost from the
classical walk,
s(r) +
n
r
k/2
(c(r) + √ru(r)).
One of the diﬀerences between Ambainis-Walk and Szegedy-Walk is that in the
former, checking takes after √r steps of the quantum walk, whereas in the latter,
checking takes after every step of the walk. Also, in the former, the walk is over a
graph, in which the vertices are a subset of size r or r +1 and they are connected iﬀ
the size of the vertex diﬀer by 1 and the symmetric diﬀerence is two, whereas in the
latter, the walk is over a bipartite graph, and each side of the vertices are subsets of
size r, and they are connected iﬀthe symmetric diﬀerence is two. We shall see later
how these diﬀerences aﬀect the performance of an algorithm for diﬀerent problems.
2.3
Triangle Finding Problem
Suppose we are given an oracle for the adjacency matrix of a graph. It takes two
vertices in a graph (i, j) as inputs and outputs 1 if the vertices are connected by
an edge and 0 otherwise. We are promised that there is exactly one clique of size
three, called triangle, or none at all. Our goal is to test which case holds for an
undirected graph G with as few queries to the oracle as possible.
For G with n vertices, classical lower bound is Ω(n4/3 log1/3 n) [CK01]. Quan-
tumly, the lower bound is Ω(n) [MSS05], by the following argument. Suppose there
is a graph G1, that is formed by adding an extra edge to one pair of the n leaves
in a star graph, G2. Then there are n2 possible triangles in G1. We are given an
oracle for the edges in G1; it answers “yes” in input (i, j) if it is part of the graph.
The goal is to ﬁnd an edge in G1 that is part of G1 −G2. Using a lower bound
for unordered search over n2 edges this takes Ω(n) quantumly as we prove later
in Section 2.4.3. Now such an edge forms a triangle in G1. So if we are given an
algorithm for triangle ﬁnding, we could also ﬁnd an edge in G1 −G2. Hence the
quantum lower bound for triangle ﬁnding problem is Ω(n).
A straightforward quantum upper bound is O(n1.5) by running Grover search
on n3 triplets of vertices, querying three times at each iteration. Here we present
an algorithm of Magniez, Santha, and Szegedy [MSS05] that uses Ambainis-based
quantum walk and queries the oracle O(n1.3) times. We also present an algorithm

---- page 42 ----
CHAPTER 2. RELATED WORK
34
that uses Szegedy-based quantum walk to compare its performance with Ambainis-
based quantum walk algorithm. We will also point out why there is a diﬀerence in
performance between the algorithms that use these two diﬀerent quantum walks.
2.3.1
O(n1.3) Algorithm Using Ambainis Walk
Recall from Section 2.2 that the query complexity for solving k-Collision for a set
of n elements by performing a quantum walk on r-subsets is,
s(r) +
n
r
k/2
(c(r) + √ru(r)).
The approach in [MSS05] consists of an outer algorithm Ao and a subroutine
As. The input of Ao is a set Vo of n vertices. The output of Ao is a pair of vertices
in Vo that is part of a triangle if there is one, “reject” otherwise. The input for As
is a set of r vertices, Vs and their adjacency matrix as well as a vertex v that is not
necessarily in Vs. The output of As is an edge called Golden Edge in the adjacency
matrix for vertices in Vs that together with v forms a triangle. Then in order to
ﬁnd a triangle edge in the subset in Ao, we only need to feed each of the n vertices
in Vo and an adjacency matrix for a subgraph induced by an r-subset into As. A
further modiﬁcation is that using Grover’s search algorithm, we search for a vertex
that forms a golden edge by repeating this algorithm √n times instead of n.
Next, we analyze the query cost of As and then Ao. Remember that in As, we
are given the adjacency matrix of a set of vertices Vs of size r. We perform a walk
on s-subsets of [n] to ﬁnd a golden edge in Vs. We create a subset of size s out
of r vertices, and query if each of s vertices is connected to the given vertex v,
because v might come from outside this set Vs. This setup cost is then O(s). At
each step of the walk, we get a new vertex from Vs into the subset of size s, but
in order to check if there is a golden edge in the subset, we only need to query if
the new vertex is connected to v. So the update cost is 1 and the checking cost is
0. The parameter k for this instance of k-collision is 2, because we are looking for
two vertices that form a triangle with v, giving the total query cost of the order of
s + r
s(√s).
This is minimized when s = r2/3 with O(r2/3) query cost.
The outer algorithm Ao performs a walk on r-subsets of vertices of Vo. The
data are the adjacency matrix of the subgraphs induced by the r-subset. Initially
we need to query r2 times to set up an adjacency matrix of the subset. At each

---- page 43 ----
CHAPTER 2. RELATED WORK
35
step of the walk, we insert a new vertex in the subset and remove one from it.
We update the adjacency matrix for the new vertex, which costs r queries. For
detecting a golden edge, we invoke √n times the subroutine As that costs r2/3.
Hence the checking cost is √nr2/3. The parameter k = 2 because we are looking
for two vertices that are part of a triangle. Hence the total cost is,
r2 +
n
r
  √nr2/3 + √rr

.
This is minimized when r = n3/5 giving O(n1.3) query complexity.
2.3.2
Szegedy Walk Does Not Perform Better
Does using Szegedy-Walk give any advantage in query complexity for this problem?
Suppose the goal of the outer algorithm Ao and the subroutine As are the same as
in [MSS05]. Then for As, the setup cost, update cost and the checking cost do not
change. Using s as the size of the subset and r as the number of vertices in As, δ is
1/s from Theorem 9, and ǫ is the probability that we have two vertices that form
a golden edge with v, so ǫ = (r−2
s−2)
(r
s) ≈s2
r2, for s ∈o(r). Then the total cost is,
s + r
√s(1),
minimizing this gives r2/3 when s = r2/3, which is exactly the same as in [MSS05]
described in Section 2.3.1.
For Ao, the setup cost, update cost and the checking cost are as same as
in [MSS05]. Using r as the size of the subset, δ is 1/r from Theorem 9, and ǫ
is the probability that we have two vertices that form a golden edge in the r-subset
Vs. So ǫ = (n−2
r−2)
(n
r) ≈r2
n2, for r ∈o(n). Then the total cost is of the order of,
r2 + n
√r(r + √nr2/3).
However, this gives O(n1.5) query complexity for r = O(1), the same as the
straightforward application of Grover’s search and worse than in [MSS05].
It turns out for the same setup, update and checking cost, we can easily see
which algorithm will perform better [Mag05]. Compare the formula for k-collision

---- page 44 ----
CHAPTER 2. RELATED WORK
36
using Ambainis-Walk
s(r) +
 n
r
k/2 (c(r) + √ru(r))
= s(r) + nk/2
rk/2 c(r) +
nk−2
r(k−1)/2u(r),
with the one for Szegedy-Walk, where δ = 1
r and ǫ = (n−k
r−k)
(n
r) ≈rk
nk ,
s(r) +
nk/2
r(k−1)/2(c(r) + u(r))
= s(r) +
nk/2
r(k−1)/2c(r) +
nk/2
r(k−1)/2u(r).
From these we see that Ambainis-Walk always performs better because the
second term is always better than Szegedy-Walk, while other terms are the same.
This allows us to have a higher query cost for checking, giving an improvement over
the straightforward O(n1.3) upper bound for triangle ﬁnding algorithm.
There are other algorithms that use Szegedy-Walk, such as an algorithm that
performs a walk based on edges. However, so far all these algorithms give the same
O(n1.5) query upper bound.
2.4
Adversary Method for Query Lower Bounds
In this section, we describe one of the popular methods to derive lower bounds for
quantum query complexity. Later in this essay we apply this technique to derive
lower bounds for the problems we are studying.
2.4.1
Quantum Adversary Theorem
Suppose an oracle takes an input i and produces xi to form a string x = (x1, x2, . . . , xN)N ∈
{0, 1}. Furthermore, suppose there is a boolean function that takes the string x
as an input and produces an output f(x). For example, in unordered search, the
oracle takes an index i and outputs xi. The boolean function f(x) is the logical
OR of all xi: f(x) = ∨ixi. We want to lower bound the number of queries needed
to decide f(x).
Theorem 2.4.1
[Amb00] Let A ⊆{0, 1}N be a set such that every string in the
set maps to 0 under f, and let B ⊆{0, 1}N be a set such that every string in the
set maps to 1. Suppose that
1. For all x ∈A, there exists m diﬀerent y ∈B such that yi ̸= xi for exactly one
i.

---- page 45 ----
CHAPTER 2. RELATED WORK
37
2. For all y ∈B, there exists m′ diﬀerent x ∈A such that xi ̸= yi for exactly
one i.
Then Ω(
√
mm′) queries are required to compute f.
Proof :
Suppose we have a t query bounded error algorithm for computing f. In
order to lower bound t, the number of queries needed, we take a look at Wt, the
sum of all the inner products at the end of t-th query over all pairs of x and y that
satisfy the relationships stated in parts 1 and 2 of the theorem:
Wt =
X
(x,y)∈R
⟨ψt
x|ψt
y⟩.
(2.5)
The proof estimates the diﬀerence |Wt −W0| and |Wj −Wj−1|, the diﬀerence made
after each query to the oracle in terms of |R|.
Let |ψj
x⟩be the state of the algorithm after the j-th query if queries were an-
swered according to the input x = (x1, x2, . . . , xN). We are interested in ⟨ψj
x|ψj
y⟩,
i.e., how much the states will diﬀer after j queries if x is taken from the set A and
y is taken from the set B. For this inner product, there are two simple things we
know about,
Property 1 ⟨ψ0
x|ψ0
y⟩= 1. This is because |ψ0
x⟩= |ψ0
y⟩= |ψstart⟩.
Property 2 At the end of the algorithm, the inner product must be small: After
t queries, |⟨ψt
x|ψt
y⟩| ≤c for a constant c < 1.
Proof :
The proof of Property 2 above follows from the lemma,
Lemma 17 ([AKN98]) If |⟨ψ1|ψ2⟩| ≥1 −ǫ, then for any measurement M and
any outcome i, the probability of ﬁnding i when measuring |ψ1⟩and |ψ2⟩diﬀers by
at most
√
2ǫ.
Suppose there is an algorithm with the probability of obtaining correct outcome
greater than or equal to 3
4. The probability of having an outcome 0 is at least 3
4
if we have an input x such that f(x) = 0. The probability of obtaining 0 is less
than 1
4 if we have y such that f(y) = 1. This means that if we have x ∈A and
y ∈B and measure the ﬁnal state |ψt
x⟩and |ψt
y⟩then the probability of measuring
0 diﬀers by at least 1/2. So
√
2ǫ ≥1
2
ǫ ≥1
8
1 −ǫ ≤7
8.
Therefore, the inner product |⟨ψt
x|ψt
y⟩| diﬀers by at most 7
8 < 1.
□

---- page 46 ----
CHAPTER 2. RELATED WORK
38
Property 3 From Property 1, we know W0 =
X
(x,y)∈R
⟨ψt
0|ψt
0⟩=
X
(x,y)∈R
1 = |R|,
where |R| ≥|A|m, |B|m′.
Property 4 From Property 2, we know that after the last, t-th query, each of the
inner product is at most 7
8 in absolute value, so |Wt| ≤7
8|R|.
Lemma 18 |Wj −Wj−1| ≤
2
√
mm′|R|.
We will provide a proof of Lemma 18 shortly. From Property 3 and Property
4, we get |Wt −W0| ≥1
8|R|, that is queries performed during the entire algorithm
decreases the inner products in Equation 2.5 at least one eighth the size of R.
Since at each step of the query, quantity Wj decreases by at most
2
√
mm′|R| from
Lemma 18, the total number of queries must be at least
t ≥|Wt −W0|
2
√
mm′|R| ≥
√
mm′
16
.
This proves the query lower bound of Ω(
√
mm′).
□
We are now left with the proof of Lemma 18.
Proof :
Let
|ψj−1
x
⟩=
n
X
i=1
αx,i|i⟩|φx,i⟩,
where |ψj−1
x
⟩is the state of the algorithm before j-th query on input x. After j-th
query, we get
|ψj
x⟩=
n
X
i=1
αx,i|i⟩|φ′
x,i⟩,
where |φ′
x,i⟩is obtained from applying a query operator Q to |i⟩|φx,i⟩. Now suppose
we have two input strings x = (x1, x2, . . . , xN) and y = (y1, y2, . . . , yN), where we
have exactly one i such that xi ̸= yi. For such i, we can rewrite |ψj−1
x
⟩as the part
that involves such i and the rest,
|ψj−1
x
⟩= αx,i|i⟩|φx,i⟩+ |ψ′
x⟩
and similarly for |ψj−1
y
⟩,
|ψj−1
y
⟩= αy,i|i⟩|φy,i⟩+ |ψ′
y⟩.

---- page 47 ----
CHAPTER 2. RELATED WORK
39
The inner product ⟨ψj−1
x
|ψj−1
y
⟩can also be decomposed into two parts, the one
that involves the i and the rest,
⟨ψj−1
x
|ψj−1
y
⟩= α∗
y,iαx,i⟨φy,i|φx,i⟩+ ⟨ψ′
y|ψ′
x⟩.
(2.6)
Similarly, we can rewrite |ψj
x⟩and |ψj
y⟩as
|ψj
x⟩= αx,i|i⟩Qxi|φx,i⟩+ Q|ψ′
x⟩
and
|ψj
y⟩= αy,i|i⟩Qyi|φy,i⟩+ Q|ψ′
y⟩.
The inner product of the ﬁnal state is,
⟨ψj
x|ψj
y⟩= α∗
y,iαx,iQ∗
yiQxi⟨φy,i|φx,i⟩+ ⟨ψ′
y|ψ′
x⟩.
(2.7)
Note that the query in Equation 2.7 does not change the second term because
we apply the same unitary transformation Q to the second registers for both |ψ′
x⟩
and |ψ′
y⟩. They contain the same data, and the unitary transformation preserves
inner products. So we only need to be careful about how much ⟨φy,i|φx,i⟩changes.
Since the inner product of |φy,i⟩and |ψx,i⟩is at most 1 and |α∗
y,iαx,i| ≤|αy,i||αx,i|,
|⟨ψj
x|ψj
y⟩−⟨ψj−1
x
|ψj−1
y
⟩| ≤2|αy,i||αx,i|.
However, we are interested in the diﬀerence above for all (x, y) ∈R, so
|Wj −Wj−1|
≤2
X
(x,y)∈R
|αy,i||αx,i|
≤
X
(x,y)∈R
 γ|αx,i|2 + γ−1|αy,i|2
.
For going from the second to the third line above, we used an inequality 2AB ≤
A2 + B2 with A = √γ|αx,i| and B = √γ−1|αy,i|.

---- page 48 ----
CHAPTER 2. RELATED WORK
40
Now we bound
X
(x,y)∈R
γ|αx,i|2 and
X
(x,y)∈R
γ−1|αy,i|2 separately.
X
(x,y)∈R
γ|αx,i|2
= γ
X
x∈A
X
y:(x,y)∈R
|αx,i|2
≤γ
X
x∈A
1
= γ|A|
≤γ |R|
m
Above, we used the fact that given x, we have at most N diﬀerent y’s that diﬀer
by exactly one position:
X
y:(x,y)∈R
|αx,i|2
=
N
X
i=1
|αx,i|2
X
y:(x,y)∈R,xi̸=yi
1
≤
X
i
|αx,i|2
= 1.
The last line comes from the fact that the squares of amplitudes sum up to 1. Also,
since for every x ∈A, we have at least m diﬀerent y ∈B that diﬀer by 1, so
|R| ≥m|A| and hence |A| ≤|R|
m .
Similarly
X
(x,y)∈R
γ−1|αy,i|2 ≤1
γ
|R|
m′ and we get
|Wj −Wj−1|
≤
X
(x,y)∈R
 γ|αx,i|2 + γ−1|αy,i|2
≤γ
m|R| + γ−1
m′ |R|
= m′γ+mγ−1
mm′
|R|.
The above expression is minimized when γ = p m
m′ to give
|Wj −Wj−1| ≤
2
√
mm′|R|.
□
The Quantum Adversary Theorem we have proven is of the simplest form in
that the yes and no instances only diﬀer in exactly one position. The stronger form

---- page 49 ----
CHAPTER 2. RELATED WORK
41
of the previous theorem relaxes the number of i at which x and y diﬀer to be more
than one. This gives a tighter bound for several problems of interest.
Theorem 2.4.2
[Amb00] For a boolean function f : {0, 1}n →{0, 1}, let A ⊆
f −1(0), B ⊆f −1(1) and R ⊆A × B.
1. For all x ∈A, |{y : (x, y) ∈R}| ≥m.
2. For all y ∈B, |{x : (x, y) ∈R}| ≥m′.
3. Deﬁne lx,i = |{y : (x, y) ∈R, xi ̸= yi}|, ly,i = |{x : (x, y) ∈R, xi ̸= yi}| and
l = max(x,y)∈R,i:xi̸=yi{lx,i, ly,i}
Then Ω
q
mm′
l

queries are required.
Unfortunately, it is proven by Szegedy [Sze03] and independently by Zhang [Zha03]
that this method cannot provide a tight lower bound for all the problems. Infor-
mally, a 1-certiﬁcate is the least number of bits of the input that determines the
value of the function to be 1. If the size of a 1-certiﬁcate is C1(f), and N is the
number of variables in the boolean function to the oracle, then the method can only
prove up to the lower bound of O(
p
C1(f)N) [Zha03]. For example, in element dis-
tinctness, C1(f) = 2, because we need to know the two elements that collide. Then
this quantity is O(√n), but the tight lower bound of this problem is Θ(n2/3) using
polynomial method [AS04].
The polynomial method [BBC+01b] is another powerful lower bound technique.
However, this method is also proven not to be tight by Ambainis [Amb03]. As
far as we know neither the adversary nor the polynomial method provides a tight
lower bound for all problems of interest. For some problem, the adversary method
provides a better bound than polynomial method [Amb03] and the opposite also
holds [AS04].
2.4.2
The Graph Connectivity
As an application of Theorem 2.4.2, we take a look at the Graph Connectivity
problem [DML03]. An undirected graph G is described by
 n
2

variables {Gi,j},
where Gi,j = 1 if (i, j) is an edge in G and 0 otherwise. The oracle gives the entries
of adjacency matrix Gi,j. We want to ﬁnd if G is connected by making as few
queries to Gi,j as possible. What would be the lower bound for quantum query
complexity?
Let A be the set of graphs on n vertices that consist of two cycles not connected
one to another, each cycle of length at least n/3. Let B be the set of graphs that

---- page 50 ----
CHAPTER 2. RELATED WORK
42
Figure 2.5: Transformations between G and G′
are one cycle of length n. In both cases each vertex belongs to one of the cycles.
We deﬁne the relationship as R = {(G, G′) : G′ has exactly two edges not in G}.
We can obtain G′ from G by deleting one edge from each cycle in G and inserting
two edges to make it a single cycle. When connecting cycles, there are two ways,
cross or parallel. So given G, the number of possible G′ you can make is
|{G′ : (G, G′) ∈R}|
= (length of ﬁrst cycle)(length of second cycle) × 2
≥2 n
3
n
3
= 2n2
9
because each cycle in G is of length at least n/3. Hence m = Ω(n2).
Creating G from G′ starts by picking one edge out of n edges in the cycle. Since
each cycle in G is of length at least n/3, the next one must be at distance at least
n/3 from the edge we just picked. This leads to n −2(n/3) = n/3 choices for the
second edge. After that there is only one way to connect the vertices to create the
two cycles. Hence m′ = Ω(n2).
For each instance in G, the number of instances in G′ that diﬀers at position
(i, j), i.e., lG,(i,j) is O(n) or O(1). If (i, j) is an edge in G, and (i, j) is not an edge
in G′, then there are ≤2n/3 graphs G′’s we can make by removing (i, j) and one of

---- page 51 ----
CHAPTER 2. RELATED WORK
43
at most 2n/3 edges in G, and we have lG,(i,j) = O(n). If (i, j) is not an edge in G,
but an edge in G′, then there are four ways to create G′ from G, e.g., by connecting
(i, j) and connecting a vertex to the left of i with the one left of j or connecting
a vertex right of i to the one to the right of j. Similarly, lG′,(i,j) = 1 if (i, j) is an
edge in G, and at most n otherwise. Overall then we have l ≤O(n), and the query
complexity is Ω
q
mm′
l

= Ω
q
n2n2
n

= Ω(n1.5).
2.4.3
Lower Bound for Unstructured Search
In this section, using Theorem 2.4.1, we prove a lower bound for a search on un-
structured database [Amb03]. Unordered search is deﬁned as follows. Given an
oracle for x = (x1, x2, . . . , xn) ∈{0, 1}n, is there i such that xi = 1? This lower
bound is useful in later sections when we reduce from this search problem to the
problems of our interest. This lower bound was ﬁrst proven in [BBBV97] using a
“hybrid argument”.
Theorem 2.4.3 [Amb03] The query complexity of a search on unstructured database
of size n is Ω(√n).
Proof :
Suppose we have n boolean elements, (x1, x2, . . . , xn). Let A be the set
that contains exactly one xi = 1 for some i ∈[n]. Let B be the set such that
xj = 0 for all j. Then for every a ∈A, there are m = 1 elements in B that diﬀer
by exactly one position. For every b ∈B, there are m′ = n diﬀerent elements in
A that diﬀer by exactly one position. Using Theorem 2.4.1, the number of queries
needed to search an element in unstructured database is Ω(√n).
□
2.5
Quantum Matrix Veriﬁcation Problem
Suppose we want to verify if AB = C for n×n matrices A, B, and C over some ring.
The oracle knows the entries of A, B, and C. What is the query and time complexity
for this problem? Classically, there is an O(n2) time algorithm by Freidvals using
random vectors [Fre79]. Classical query lower bound for this problem is Ω(n2), by a
reduction from unordered search; Let A and B be matrices having all entries being
1: Let C be a matrix with all entries being n. Then AB = C. If we set one of the
3n2 entries to be 0 then AB = C no longer holds. Hence we are searching for one
entry of 0 out of 3n2 entries. The classical lower bound for unordered search for n2
elements is Ω(n2), hence we have an Ω(n2) lower bound for matrix veriﬁcation.

---- page 52 ----
CHAPTER 2. RELATED WORK
44
2.5.1
Upper Bound
An O(n5/3) query upper bound can be obtained by using either Ambainis-Walk
or Szegedy-Walk. The idea behind this is to perform a walk over r-subsets from
the set of rows from A and another r-subsets of a set of columns from B, and the
corresponding entries from C. For an n × n matrix M and an r-subset S of [n],
let M|S denote a r × n sub-matrix of M corresponding to rows in S, M|S an n × r
sub-matrix of M corresponding to columns in S. Initially, we query r rows of A, r
columns of B and r2 entries of C corresponding to all these rows and columns. So
the setup cost is O(rn). When update, we swap in a new row for A, a new column
for B and 2r entries of C, giving the update cost of O(n). Checking is done by
performing A|S × B|T to see if it is equal to C|T
S for subsets S and T. Then the
checking cost is 0. Here, we are looking for k = 2 elements, an index for a row in
A and an index for a column in B that gives a wrong entry in C. The total cost if
we use Ambainis-Walk is of the order of
rn +
n
r
2/2
(√rn).
Since we are looking for two elements that collide, ǫ ≈r2
n2 for r ∈o(n) and the
spectral gap of the walk is 1
r. Then the query cost if we use Szegedy-Walk is of the
order of
rn + n
√r(n).
Here we see that both formulae give the same result, an O(n5/3) query upper
bound when r = n2/3.
Buhrman and Spalek [BS05] showed another Szegedy-Walk algorithm that uses
random vectors to speed up the running time of the algorithm, the query complexity
stays the same. In the original Szegedy-based algorithm described above, multiply-
ing A|S with B|T takes O(nr2) multiplications. This time can be reduced by using
Freivalds’ random vector technique on sub-matrices. At a setup stage, we multiply
A|S with a vector u of length r and B|T with another vector v of length r as well as
computing uC|T
Sv. During the walk stage we keep updating these three vectors. At
the checking stage, the product of uA|S and B|Tv is tested against uC|T
Sv. Then the
setup cost is 2rn + r2 = O(rn), the update cost is 2n + 4r = O(n) (a factor of two
came from erasing and rewriting data), and the checking cost is O(n). Note that we
still need to query the same number of entries, i.e., O(rn) entries, in the matrices
as the original algorithm, and so the query complexity stays the same. Thus we
focus on how much speed up there is in time complexity. The marked element is
a pair (i, j) of a row of A and a column of B such that when matrix A and B are

---- page 53 ----
CHAPTER 2. RELATED WORK
45
multiplied together via random vectors, it gives the incorrect entry of C at (i, j).
Note that since we are using random vectors, the fraction of marked elements and
the fraction of elements that actually contribute to the product inequality, call them
visible marked element are diﬀerent. It can be shown, however, that the fraction
of marked elements is close to the fraction of visible marked elements, and that we
can minimize the error probability by calling this algorithm for a constant number
of times, each time picking u and v randomly. Therefore, ǫ ≈r2
n2 for r ∈o(n). The
eigenvalue gap δ = 1
r as before, from Theorem 9. The time complexity of one run
of the algorithm is
rn + n
√r(n),
which is O(n5/3) when r = n2/3. This algorithm is invoked for a constant number
of times, hence the overall time complexity is also O(n5/3). Algorithm 3 describes
the classical version of their algorithm.
Algorithm 3 A Classical Algorithm for Testing If AB = C
1: Create a random r-subset S of rows of A and another random r-subset T of
columns of B.
2: Pick a random 1 × r row vector u and a random r × 1 column vector v.
3: Compute uA|S, B|Tv and uC|T
Sv.
4: while t ≤T0 do
5:
Swap one row of A and one column of B chosen u.a.r.
6:
Recompute uA|S, B|Tv and uC|T
Sv.
7:
Test if uA|S × B|Tv = uC|T
Sv.
8: end while
9: Answer “AB=C”
2.5.2
Lower Bound
We use quantum adversary theorem to prove an Ω(n1.5) lower bound [Amb05]. First
consider a problem to test if Au = v, where A is an n × n matrix, u is a vector
of length n with all the entries being 1, and v is a vector of length n with all the
entries being n/2. Let a matrix A be balanced if each of its rows contains exactly
n/2 entries that are 1 and exactly n/2 entries that are 0. Let unbalanced A to be
such that n −1 rows contain exactly n/2 entries of 1 but one row contains n/2 + 1
entries of 1. Then for a balanced A, we have Au = v, but for an unbalanced A,
we have Au ̸= v. There are m = n(n/2) ways to transform a balanced matrix A
into an unbalanced matrix by choosing one of n(n/2) entries that are 0. There are

---- page 54 ----
CHAPTER 2. RELATED WORK
46
m′ = n/2+1 ways to transform an unbalanced A into a balanced A by choosing one
of n/2+1 entries that are 1. The parameter l = 1 since balanced A and unbalanced
A diﬀers by exactly one position. Hence we obtain
q
n(n/2)(n/2+1)
1
= Ω(n1.5) query
lower bound for testing if Au = v. Let B consist of n entries of u in the columns
and C to consist of n entries of v in the columns, then the above argument still
holds, and so the lower bound for testing if AB = C is Ω(n1.5).

---- page 55 ----
Chapter 3
Testing Commutativity of
Matrices
Suppose we have k matrices of dimension n×n. The entries of the matrix are given
by an oracle with the input being a triplet (i, j, l) and the output being the (i, j)
entry of l-th matrix. We want to test if all the matrices in the set commute with
each other or not by making as few queries to the oracle as possible. Classically, we
need to query all the entries of the matrices by the following argument. Suppose
all the matrices in the set contained all 1 entries. Then AB = BA for every pair.
However, for every pair A, B, if we ﬂip one of the kn2 entries, say in matrix A, to
0 then AB ̸= BA for every other matrix B. Hence we have reduced the problem of
unordered search among kn2 items to testing commutativity, giving the lower bound
of Ω(kn2). Quantumly, an unordered search of n elements takes Ω(√n) queries
from Theorem 2.4.3 [Amb03], then by reduction, quantum query complexity of this
problem is Ω(
√
kn2). What would be the quantum query complexity of testing the
commutativity of k matrices of size n × n?
3.1
Commutativity Testing for a Single Pair
Suppose we only want to test a single pair of matrices, that is to see if AB = BA for
two n×n matrices A and B. The lower bound is obtained by the reduction from the
unordered search as in at the beginning of Section 3 with k = 1. So quantum query
lower bound is Ω(n). The upper bound is obtained from a modiﬁcation of matrix
veriﬁcation algorithm in [BS05]. When checking, instead of testing uA|S × B|Tv =
uC|T
Sv, we test uA|S ×B|Tv = uB|S ×A|Tv. This does not aﬀect the overall time or
query complexity of [BS05] in Section 2.5, and hence we have O(n5/3) upper bound
47

---- page 56 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
48
for testing AB = BA.
3.2
Commutativity Testing of k Matrices
Now let’s take a look at the cases where we have k matrices to test the commutativ-
ity. In presenting the quantum algorithms, we will describe the classical versions,
as from Theorem 15, we only need to know the classical algorithm to bound the
quantum complexity.
3.2.1
Two Straightforward Algorithms
The ﬁrst algorithm performs a Grover search over all O(k2) pairs of matrices, at
each step running a single pair commutativity testing algorithm that costs O(n5/3).
Recall that the single pair commutativity testing algorithm in Section 3.1 was
obtained from the modiﬁcation of the bounded error matrix veriﬁcation algorithm
in Section 2.5. Then we have a bounded-error oracle. However, using the Theorem
of [HMdW03] in Section 1.2.6, we can perform a quantum search with a bounded-
error oracle with the same complexity as that with a perfect oracle. Hence, the
query complexity of this algorithm is O(kn5/3).
In the second algorithm, Algorithm 4 presented in the table below, we query
fewer number of matrices by querying more entries per matrix. In order to estimate
Algorithm 4 A Classical Version of the Second Straightforward Algorithm
1: Create a random subset of r matrices.
2: Query all the entries of the matrices in the subset.
3: while t ≤T do
4:
Pick a matrix to be swapped u.a.r. from the subset and swap this with the
one not in the subset also picked u.a.r.
5:
For the new matrix in the subset, query all the entries.
6:
Check if all the matrices in the subset commute or not.
7:
if There is a non commutative pair in the subset then
8:
print ‘‘Non commutative.’’
9:
return
10:
end if
11: end while
12: Answer “Commutative”
the query, but not time complexity, we need to calculate the setup cost, update and

---- page 57 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
49
checking cost, and T the number of iterations as in Section 2.1.5. The setup cost
is rn2 by querying all the entries of r matrices in the subset. The update cost is n2
because we only need to query all the entries for the new matrix we swap into the
subset. The checking cost is 0. T =
k
√r because from Theorem 15, T =
1
√
δǫ and
δ = 1
r from Theorem 9 and ǫ = (
(k−2)
(r−2))
(k
r)
≈r2
k2 for r ∈o(n), because we are looking for
two matrices that does not commute. Applying these costs into Equation 2.4,
rn2 + k
√r(n2).
Optimizing this, we have r = k2/3 and hence the query complexity is O(k2/3n2).
Notice that we could also think of this problem as element distinctness. Suppose
that each element is a matrix, then we have a collision if two matrices do not
commute.
Since element distinctness can be solved in O(k2/3) and we need to
query each of O(n2) entries of the pair of matrices in question, this gives O(k2/3n2)
query complexity.
It is interesting to realize that although we could get the query upper bound
using Szegedy-Walk, we could simply apply a Grover’s search with a single pair
matrix veriﬁcation algorithm for the ﬁrst algorithm, and element distinctness for
the second algorithm. It seems we have not yet taken an advantage of Szegedy-walk.
3.2.2
Walk Over Separate Rows and Columns
The ﬁrst straightforward algorithm repeatedly performs a walk over a set of rows of
matrices. What if we walk over the rows and columns taken from all k matrices put
together? Algorithm 5 describes the classical version of the walk. This algorithm
keeps two diﬀerent r-subsets, one for rows and one for columns. An element of
r-subset for rows consists of (i, l), an i-th row of l-th matrix, also denoted Mi,l. An
element of r-subset for columns consists of (j, m), a j-th column of m-th matrix, also
denoted Mj,m. This is because we are looking for a pair of matrices (l, m) and pairs
of rows and columns (i, j) that do not commute i.e., Mi,l×Mj,m ̸= Mi,m×Mj,l, and
so we need to separate all the rows and columns in diﬀerent matrices. At each step
of the walk, we pick one row and one column in the r-subsets and those not in the
r-subsets u.a.r. and then swap these and update the data registers accordingly. At
the checking step, the algorithm checks to see if there are rows i and columns j from
two diﬀerent matrices A and B. If so, we check the commutativity by multiplying
the i-th row of A with j-th column of B, and see if it agrees with the product of
i-th row of B with j-th column of A.

---- page 58 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
50
Algorithm 5 A Classical Walk Over Separate Rows and Columns
1: Create an r-subset of rows by randomly choosing r rows among all the rows in
k matrices. Similarly create another r-subset of columns.
2: Query all the entries of the rows and columns in the subset.
3: while t ≤T do
4:
Pick a row and a column u.a.r. from the r-subsets, and another row and
column not in the r-subsets and swap these.
5:
For the new row and column in the subset, query all the entries.
6:
Check if there are rows i and columns j from two matrices A and B. If so,
check if the product of row i of matrix A with the column j of matrix B is
the same as that of row i of matrix B and the column j of matrix A.
7:
if There is a non commutative pair in the subset then
8:
print ‘‘Non commutative.’’
9:
return
10:
end if
11: end while
12: Answer “Commutative”
The setup cost is O(rn) because we have r rows and r columns in the subsets.
The update cost is O(n), because we need to query one row and one column.
The checking cost is 0. We have two walks going on over row indices and column
indices, each of a subset of size r.
Then each walk operator has an eigenvalue
gap of at least
1
r, with λ1 = 1, λ2 ≤1 −1
r.
Since the eigenvalues of a tensor
product of two matrices are the products of all the pairs of eigenvalues from the
matrices, the largest eigenvalue is still 1 · 1 = 1 and the second largest eigenvalue
is at most 1 · 1
r = 1
r. Hence the eigenvalue gap of the tensor product of the two
matrices is δ ≥1
r. The probability of having marked elements is the probability that
we have noncommutative rows from two noncommutative matrices in the subset
of rows times the probability that we have noncommutative columns from two
noncommutative matrices in the subset of columns. Hence ǫ =

(nk−2
r−2 )
(nk
r )
2
≈
r4
n4k4
for r ∈o(nk). Hence our query complexity is
rn + n2k2
r3/2 (n).
Optimizing this gives O(k4/5n9/5) for r = k4/5n4/5 when r = o(nk).
Note that when k = n, The ﬁrst two straightforward algorithms both give n8/3,

---- page 59 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
51
and Algorithm 5 gives O(n13/5), hence Algorithm 5 has a better query complex-
ity. However, when k < n2/3, the ﬁrst straightforward algorithm in Section 3.2.1
performs the best and when k > n3/2, Algorithm 4 performs the best.
3.2.3
Simultaneous Quantum Walk
Recall that in the ﬁrst straightforward algorithm we repeatedly performed a walk
over rows and columns of a ﬁxed pair of matrices but no walk was performed
over the matrices. In Algorithm 4, we performed a walk over matrices, but no
walk was performed over the rows. What if we perform a walk over matrices and
rows/columns at the same time? This is what Algorithm 6 does. The quantization
of Algorithm 6 gives us another O(k4/5n9/5) upper bound. Note that it has the
same query complexity as that of Algorithm 5 from the previous section.
Algorithm 6 A Classical Simultaneous Walk
1: Create an r-subset of matrices S, an s-subset of rows R, and another s-subset
C of columns.
2: Query all the entries of the rows and columns in R and C of the matrices in
the subset S.
3: while t ≤T do
4:
Swap one matrix in the subset S with the one not in the subset chosen u.a.r.
5:
For the new matrix in the subset, query the s rows and columns in R and C.
6:
Swap one row and column in the subsets R and C with the ones not in the
subsets both chosen u.a.r.
7:
For the new row and column in each of the matrices in the subset S, query
all the entries.
8:
Check if all the sub matrices given by the subset commute or not.
9:
if There is a non commutative pair in the subset then
10:
print ‘‘Non commutative.’’
11:
return
12:
end if
13: end while
14: Answer “Commutative”
In Algorithm 6, we maintain two diﬀerent s-subsets for rows and columns. We
keep all the rows and columns from all the matrices in the r-subset from the same
set of row indices and column indices as the data. So the idea behind the algorithm
is to keep updating the set of indices for matrices, rows, and columns. At each step
of the walk, we get a new matrix and query the entries of this new matrix. Then

---- page 60 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
52
for each matrix in the r-subset, we update a row and a column. Then the setup
cost is O(rsn) for querying each entry of an s × n submatrix for each matrix in
r-subset. The update cost is O(rn + sn), O(sn) for a new matrix we just swapped
in, and O(rn) for a new row and a column for each matrix in r-subset. The checking
cost is 0 because checking is done by computing the product of submatrices whose
entries we already know. We now calculate δ. Let P be the operator acting on
matrix indices and Q = Qr ⊗Qc be the operator acting on row and column indices.
The eigenvalue gap for P is 1/r and for Q is 1/s. Then δ = min{1/r, 1/s}. The
probability of having noncommutative submatrices is ǫ =

(k−2
r−2)
(k
r)
 
(n−1
s−1)
(n
s)
2
for
r ∈o(k) and s ∈o(n). Thus we have a total query cost of
rsn + kn
rs
p
max{r, s}(rn + sn).
Since r ∈o(k) and s ∈o(n), minimizing this gives O(k4/5n9/5) with r = s =
k2/5n2/5 when k2/3 ≤n ≤k3/2, O(kn2) with r = s = 1 otherwise.
Note that walking for multiple steps before checking mixes the elements of
subsets well without changing the eigenvalue gap. Then can we do better if the
underlying classical Markov Chain is P u ⊗Qv, that is, perform u steps of the walk
P over the matrices and then v steps of the walk Q over the rows/columns indices?
It turns out that the increased cost of updating diminishes any gain from having
the same eigenvalue gap.
Theorem 3.2.1 Having M = P u ⊗Qv for positive u and v as an underlying
classical Markov Chain does not give any better query complexity than having M′ =
P ⊗Q.
Proof :
We still have the same setup, the checking cost and ǫ as before. So
the setup cost is O(rsn), the checking cost is 0 and ǫ =

(k−2
r−2)
(k
r)
 
(n−1
s−1)
(n
s)
2
for
r ∈o(k) and s ∈o(n). The update cost this time is (usn + vrn). We need to
analyze the eigenvalue gap of M = P uQv. From Theorem 9, the upper bound of
the eigenvalue gap is 1/r, hence the second largest eigenvalue is at least 1 −1/r.
Then the largest eigenvalue of P u is still 1 and its second largest eigenvalue is at
least (1−1/r)u. Similarly, the second largest eigenvalue of Qv is at least (1−1/s)v.
Then the largest eigenvalues for P uQv is still 1 and the second largest is at most
max{(1 −1/r)u, (1 −1/s)v}. Then δ ≥min{1 −(1 −1/r)u, 1 −(1 −1/s)v}. Then

---- page 61 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
53
we have
T
=
1
√
δǫ
= kn
rs max

1
√
1−(1−1
r )u,
1
√
1−(1−1
s )v

.
Hence we have
rsn + (usn + vrn)kn
rs max



1
q
1 −(1 −1
r)u
,
1
q
1 −(1 −1
s)v


.
Next, we express r and s in terms of k and n that gives the optimal bound.
We ﬁrst note that (1 −1/r)u ≈1 + u(−1/r) = 1 −u/r for r = ω(1) by taking
the ﬁrst two terms of binomial expansion. Hence
q
1 −(1 −1
r)u ≈
p
u/r. Then
we get the following bound for the cost,
rsn + (usn + vrn)kn
rs max
√r
√u,
√s
√v

.
Suppose r/u ≥s/v, then r ≥su/v and vrn ≥usn. Then we get
rsn + vrnkn
rs
√r
√u.
Simplifying this, we get
rsn + kn2v√r
s√u
.
Both the ﬁrst and the second terms of the sum above is an increasing function
of r, so we want to set r to be the minimum. Since r ≥su/v, we set r = su/v. The
new simpliﬁed formula is then,
s2un
v
+ kn2√v
√s
.
Since the ﬁrst term of the sum above is an increasing function of s but the
second term is a decreasing function of s, we set the ﬁrst term to be equal to the
second term,
s2un
v
= kn2√v
√s
.
Solving this gives s = k2/5n2/5v3/5
u2/5
, and the query complexity is O(k4/5n9/5v1/5u1/5)

---- page 62 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
54
for k2/3
v
u2/3 ≤n ≤k3/2 v3/2
u . Otherwise, we get r = s = 1 with complexity O(kn2v).
Similar arguments holds for when r/u ≤s/v. We see that since u and v are pos-
itive, the best upper bound achieved by applying M = P uQv does not give any
better query bound than simply applying M′ = PQ.
□
3.3
Generalization of Simultaneous Quantum Walks
In the previous problem of testing the commutativity of k matrices in Section 3.2,
the marked state depended on two parameters, a set of matrix indices and the set
of row/column indices. The best upper bound was obtained by a simultaneous walk
over these two sets of indices. Suppose now the condition of being marked depends
on m parameters. Then we can obtain a better upper bound than straightforward
application of Grover’s search or that of quantum walk by having a walk in each
of m subsets in parallel, at each step of the walk, updating each of the parameters.
For example, for the commutativity testing of a matrix set, m = 2 and so at each
step, we updated a matrix set and a row/column set. The setup, the update and
the checking cost, as well as ǫ depends on how the data are stored. However, δ is
the minimum eigenvalue gap among all the walk operators. Hence if we have m
subsets of size r1, r2, . . . , rm, then δ = mini{ 1
ri}. Below is an example problem that
is reduced to testing the commutativity of k matrices problem by having only one
element in each set.
3.3.1
Example Problem
Suppose we have m sets of matrices, each containing k matrices of size n × n. We
are promised that within each set, the matrices commute. Are there two or more
sets, when combined, give a noncommutative set of matrices?
3.3.2
Upper Bound
The following is an O(m6/7k6/7n13/7) algorithm by a simultaneous quantum walk
over the sets, matrices and rows/columns.
The idea is to form subsets of the set of matrices, matrix, and row/column and
query all the entries corresponding to them at a setup stage. At each step of the
walk, we swap a new set, a new matrix, and a new row/column and update the
entries accordingly. The checking is done by computing the product of each pairs
of matrices without any further query. See Algorithm 7 for details. Then, the setup

---- page 63 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
55
Algorithm 7 A Classical Algorithm for Solving Collisions with Three Parameters
1: Create a t-subset S of sets, r-subset M of matrices and s-subsets R and C of
rows/columns.
2: Query all the entries of the rows and columns in R and C of matrices in M
that are in sets S.
3: while t ≤T do
4:
Swap one set in S with one not in S by choosing the elements u.a.r.
5:
Query s rows and columns in R and C for all the r matrices in M in the new
t-subset.
6:
Swap one matrix in M with the one not in M both chosen u.a.r.
7:
Query s rows and columns in R and C for the new matrix in each of t sets
in S.
8:
Swap one row and column in R and C with the ones not in R and C both
chosen u.a.r.
9:
Query a row and a column for the new row and column in each of r matrices
in M in t sets in S.
10:
Check if all the matrices in the subset commutes or not.
11:
if There is a non commutative pair in the subset then
12:
print ‘‘Non commutative.’’
13:
return
14:
end if
15: end while
16: Answer “Commutative”

---- page 64 ----
CHAPTER 3. TESTING COMMUTATIVITY OF MATRICES
56
cost is O(trsn), because we need to query s rows for each of r matrices in each of
t sets. The update cost is O(rsn + tsn + rtn), rsn for when swapping sets, tsn for
when swapping matrices, and O(rtn) for when swapping rows/columns, e.g., for a
new set, we need to query the entries of r matrices, and for each matrix, we keep
s rows and columns. The checking cost is 0 because we have already queried the
entries of submatrices at the setup and the updating stages. The eigenvalue gap,
δ = min{1/t, 1/r, 1/s}, and ǫ ≈
r2s2t2
k2n2m2 for t ∈o(m), r ∈o(k), and s ∈o(n). Then
our query complexity is
trsn +
1
√
δǫ
(rsn + tsn + rtn)
for δ, ǫ as stated above. By optimizing this, we get a cost of O(m6/7k6/7n13/7)
with t = r = s = m2/7k2/7n2/7 for k5/2n5/2 ≤m, m5/2n5/2 ≤k, and m5/2k5/2 ≤n.
O(kmn2) otherwise. On the other hand, if we perform a simple Grover’s search by
searching on a pair of sets and within each pair of set, a pair of noncommutative
matrices, then it costs O(mkn5/3). Applying element distinctness over pairs of sets
and within each pair, applying Grover’s search over O(k2) pairs of matrices, and
for each pair of matrices, applying a single pair commutativity testing algorithm in
Section 3.1 gives O(m2/3kn5/3) query complexity.
3.3.3
Lower Bound
Ω(m1/2k1/2n) lower bound is obtained by quantum adversary argument.
Let A be the set such that m/2 sets contain pseudo-identity matrices, i.e., for
1 ≤i ≤m/2, 1 ≤j ≤k, the j-th matrix in i-th set consists of diagonal entries
of all ij. The other m/2 sets contain matrices with all the entries being the same
and non-zero. For m/2 < i ≤m, the j-th matrix in i-th set contains all ij entries.
Then within each of the m sets, the matrices commute with each other. Also all of
mk matrices commute with each other.
Let B be the set such that one of k matrices in one of m/2 sets that contain
pseudo-identity matrices has one of oﬀdiagonal entries being ﬂipped from zero to
the same entry as in diagonal. Then within this set, the matrices still commute
with each other because the rest of the k −1 matrices are pseudo-identity. Within
each of the other sets, the matrices still commute, because they are not aﬀected.
However, a set consists of the matrices from the modiﬁed set and the matrices from
one of m/2 sets that contain all-same-entry matrices, gives non-commutative pairs.
m = m/2kn2, m′ = 1 and l = 1. So the lower bound is
p
m/2kn2 = Ω(m1/2k1/2n).

---- page 65 ----
Chapter 4
Summary and Future Work
We have seen two diﬀerent kinds of quantum walk; Ambainis-Walk and Szegedy-
Walk, which are tools for providing upper bounds for triangle ﬁnding problem and
other matrix related problems. Both of the walks give the same query upper bound
for matrix product veriﬁcation. However, for triangle ﬁnding problem, Ambainis-
Walk gives a better query upper bound. In fact, we have shown that with the same
setup, update and checking cost for time or query complexity, Ambainis-Walk gives
a better bound. On the other hand, Szegedy-Walk gives a better upper bound for
time complexity in matrix veriﬁcation problem. Moreover, there is an algorithm for
testing commutativity of a general group [MN05], where analysis of Szegedy-walk
is more powerful.
Both of these walks are discrete in the sense that each time step of the walk is
discrete. There is another kind of walk called continuous walk, where the walk is
performed with a time step ǫ where ǫ →0. There is an application of continuous
walk that gives an exponential separation in quantum query complexity [CCD+03]
from the classical counterpart. There is no exponential separation shown using
discrete time walk so far, however. For some problem such as a search on N × N
grid, discrete walk performs quadratically better than continuous walk without
ancilla [AKR05]. Whether discrete walk is more powerful than continuous walk
is an open question, although it is suspected that these give essentially the same
behaviour.
We have also seen Ambainis’s quantum adversary theorem for proving lower
bounds. This technique is used to prove a lower bound of Ω(√n) for a search on
unstructured database. From this problem, we may derive lower bounds for many
of the problems studied in this essay.
For testing the commutativity of k matrices of size n × n, we learned that there
are three query complexities O(kn5/3), O(k2/3n2) and O(k4/5n9/5) and depending
57

---- page 66 ----
CHAPTER 4. SUMMARY AND FUTURE WORK
58
on the relationship between k and n, one upper bound is better than the others.
The lower bound for this problem is Ω(k1/2n).
For future work, we would like to classify what kinds of problems are better
suited using Ambainis or Szegedy Walk. Also, we would like to come up with an
upper bound for the matrix commutativity testing problem, that either supersedes
or incorporates all the three upper bounds.
Since the gap between the current
upper bound and the lower bound is wide, we need to close the gap as well. We
are not sure if quantum adversary method can prove a tight lower bound for this
problem, and investigating other lower bound methods is also of interest.

---- page 67 ----
Bibliography
[AAKV01] Dorit Aharonov, Andris Ambainis, Julia Kempe, and Umesh Vazirani.
Quantum walks on graphs. In STOC ’01: Proceedings of the thirty-
third annual ACM symposium on Theory of computing, pages 50–59,
New York, NY, USA, 2001. ACM Press.
[ABN+01]
Andris Ambainis, Eric Bach, Ashwin Nayak, Ashvin Vishwanath, and
John Watrous. One-dimensional quantum walks. In STOC ’01: Pro-
ceedings of the thirty-third annual ACM symposium on Theory of com-
puting, pages 37–49, New York, NY, USA, 2001. ACM Press.
[AKN98]
Dorit Aharonov, Alexei Kitaev, and Noam Nisan. Quantum circuits
with mixed states. In STOC ’98: Proceedings of the thirtieth annual
ACM symposium on Theory of computing, pages 20–30, New York, NY,
USA, 1998. ACM Press.
[AKR05]
Andris Ambainis, Julia Kempe, and Alexander Rivosh. Coins make
quantum walks faster. In SODA ’05: Proceedings of the sixteenth an-
nual ACM-SIAM symposium on Discrete algorithms, pages 1099–1108,
Philadelphia, PA, USA, 2005. Society for Industrial and Applied Math-
ematics.
[Amb00]
Andris Ambainis.
Quantum lower bounds by quantum arguments.
2000. LANL preprint quant-ph/0002066.
[Amb03]
Andris Ambainis. Polynomial degree vs. quantum query complexity.
In Proceedings of the 44th Annual IEEE Symposium on Foundations
of Computer Science (FOCS’03), pages 230–239, 2003. LANL preprint
quant-ph/0305028.
[Amb04a]
Andris Ambainis. Quantum walk algorithm for element distinctness. In
FOCS ’04: Proceedings of the 45th Annual IEEE Symposium on Foun-
59

---- page 68 ----
BIBLIOGRAPHY
60
dations of Computer Science (FOCS’04), pages 22–31, Washington,
DC, USA, 2004. IEEE Computer Society.
[Amb04b]
Andris Ambainis. Quantum walks and their algorithmic applications.
LANL Quantum Physics preprint quant-ph/0403120, May 2004.
[Amb05]
Andris Ambainis. private communication, 2005.
[AS04]
Scott Aaronson and Yaoyun Shi. Quantum lower bounds for the col-
lision and the element distinctness problems. J. ACM, 51(4):595–605,
2004.
[BBBV97]
Charles H. Bennett, Ethan Bernstein, Gilles Brassard, and Umesh
Vazirani.
Strengths and weaknesses of quantum computing.
SIAM
J. Comput., 26(5):1510–1523, 1997.
[BBC+01a] Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, and
Ronald de Wolf. Quantum lower bounds by polynomials. J. ACM,
48(4):778–797, 2001.
[BBC+01b] Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, and
Ronald de Wolf. Quantum lower bounds by polynomials. J. ACM,
48(4):778–797, 2001.
[BS05]
Harry Buhrman and Robert Spalek. Quantum veriﬁcation of matrix
products. In The 32nd International Colloquium on Automata, Lan-
guages and Programming (ICALP2005), 2005.
[CCD+03]
Andrew M. Childs, Richard Cleve, Enrico Deotto, Edward Farhi, Sam
Gutmann, and Daniel A. Spielman. Exponential algorithmic speedup
by a quantum walk. In STOC ’03: Proceedings of the thirty-ﬁfth annual
ACM symposium on Theory of computing, pages 59–68, New York, NY,
USA, 2003. ACM Press.
[CE03]
A. M. Childs and J. M. Eisenberg. Quantum algorithms for subset
ﬁnding. 2003. LANL preprint quant-ph/0311038.
[CFG02]
Andrew M Childs, Edward Farhi, and Sam Gutmann. An example of
the diﬀerence between quantum and classical random walks. Quantum
Information Processing, 1:35, 2002.
[CG04]
Andrew M Childs and Jeﬀrey Goldstone. Spatial search by quantum
walk. Physical Review A, 70:022314, 2004.

---- page 69 ----
BIBLIOGRAPHY
61
[CK01]
Amit Chakrabarti and Subhash Khot. Improved lower bounds on the
randomized complexity of graph properties. ICALP 2001,the 28th In-
ternational Colloquium on Automata, Languages and Programming,
Lecture Notes in Computer Science 2076, pages 285–296, 2001.
[dBCW]
J. Niel de Beaudrap, Richard Cleve, and John Watrous. Sharp quantum
versus classical query complexity separations. Algorithmica, 34(4):449–
461.
[Deu85]
David Deutsch.
Quantum theory, the Church-Turing principle and
the universal quantum computer. Proceedings of the Royal Society of
London Ser. A, A400:97–117, 1985.
[DML03]
Christoph Durr, Mehdi Mhalla, and Yaohui Lei. Quantum query com-
plexity of graph connectivity. 2003. LANL preprint quant-ph/0303169.
[FG98]
Edward Farhi and Sam Gutmann. Quantum computation and decision
trees. Physical Review A, 58:915–928, 1998.
[Fre79]
R. Freivalds. Fast probabilistic algorithms. In the 8th Symposium on
Mathematical Foundations of Computer Science, pages 57–69. Springer
Verlag, 1979. LNCS 74.
[Gro98]
Lov K. Grover. Quantum search on structured problems. In QCQC
’98: Selected papers from the First NASA International Conference on
Quantum Computing and Quantum Communications, pages 126–139,
London, UK, 1998. Springer-Verlag.
[HMdW03] Peter Høyer, Michele Mosca, and Ronald de Wolf. Quantum search
on bounded-error inputs. In Proc. of 30th International Colloquium
on Automata, Languages, and Programming (ICALP’03),LNCS 2719,
pages 291–299, 2003.
[Knu91]
D. Knuth. Combinatorial matrices. 1991. Manuscript available at
http://www-cs-faculty.stanford.edu/~knuth/preprints.html\
#unpub.
[Mag05]
F. Magniez. private communication, 2005.
[MN05]
F. Magniez and A. Nayak. Quantum complexity of testing group com-
mutativity. In Proceedings of 32nd International Colloquium on Au-
tomata, Languages and Programming, Lecture Notes in Computer Sci-
ence, pages 1312–1324. Verlag, 2005.

---- page 70 ----
BIBLIOGRAPHY
62
[MSS05]
F. Magniez, M. Santha, and M. Szegedy. Quantum algorithms for the
triangle problem. In Proceedings of 16th ACM-SIAM Symposium on
Discrete Algorithms, pages 1109–1117, 2005.
[NC00]
Michael A. Nielsen and Isaac L. Chuang. Quantum computation and
quantum information. Cambridge University Press, New York, NY,
USA, 2000.
[SKW03]
Neil Shenvi, Julia Kempe, and K. Birgitta Whaley. Quantum random-
walk search algorithm. Physical Review A (Atomic, Molecular, and
Optical Physics), 67(5):052307, 2003.
[Sze03]
Mario Szegedy. On the quantum query complexity of detecting trian-
gles in graphs. 2003. LANL preprint quant-ph/0310107.
[Sze04a]
Mario Szegedy. Quantum speed-up of Markov chain based algorithms.
In Proceedings of the 45th Annual IEEE Symposium on Foundations of
Computer Science (FOCS’04), pages 32–41, 2004.
[Sze04b]
Mario Szegedy. Spectra of quantized walks and a
√
δǫ rule. 2004. LANL
preprint quant-ph/0401053.
[Wat01]
John Watrous. Quantum simulations of classical random walks and
undirected graph connectivity. Journal of Computer and System Sci-
ences, 62(2):376–391, 2001.
[Zha03]
Shengyu Zhang.
On the power of Ambainis’s lower bounds.
2003.
LANL preprint quant-ph/0311060.

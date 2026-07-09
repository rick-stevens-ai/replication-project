# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:0704.3628 — Andris Ambainis, 'A nearly optimal discrete query quantum algorithm for evaluating NAND formulas'
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

arXiv:0704.3628v1  [quant-ph]  26 Apr 2007
A nearly optimal discrete query quantum algorithm for evaluating
NAND formulas
Andris Ambainis∗
Abstract
We present an O(
√
N) discrete query quantum algorithm for evaluating balanced binary
NAND formulas and an O(N
1
2 +O(
1
√
log N )) discrete query quantum algorithm for evaluating ar-
bitrary binary NAND formulas.
1
Introduction
One of two most famous quantum algorithms is Grover’s search [15] which solves a generic
problem of exhaustive search among N possibilities in O(
√
N) steps. This provides a quadratic
speedup over the naive classical algorithm for a variety of search problems [3].
Grover’s algorithm can be re-cast as computing OR of N bits x1, . . . , xN, with O(
√
N)
queries to a black box storing the values x1, . . . , xN. Then, a natural generalization of this
problem is computing the value of an AND-OR formula of x1, . . . , xN.
This problem can be viewed as a black-box model for determining the winner in a 2-player
game (such as chess) if both players play their optimal strategies. In this case, the game can be
represented by a game tree consisting of possible positions. The leaves of a tree correspond to
the possible end positions of the game. Each of them contains a variable xi, with xi = 1 if the
ﬁrst player wins and xi = 0 otherwise. Internal nodes corresponding to positions which the ﬁrst
player makes the next move contain a value that is OR of the values of their children. (The ﬁrst
player wins if he has a move that leads to a position from which he can win.) Internal nodes
for which the second player makes the next move contain a value that is AND of the values of
their children. (The ﬁrst player wins if he wins for any possible move of the second player.)
The question is: assuming we have no further information about the game beyond the
position tree, how many of the variables xi do we have to examine to determine whether the
ﬁrst player has a winning strategy? This problem has been studied in both classical [20, 19, 21]
and quantum [2, 5, 8, 16] context.
Throughout this paper, we will assume that the formula is read-once (every leaf contains a
diﬀerent variable). There are two main cases that have been studied in the quantum case.
The ﬁrst case is when the formula is of a constant depth d. If the formula is balanced (which
is the most commonly studied case), then even levels contain ORs of N 1/d variables and odd
levels contain ANDs of N 1/d variables. In this case, Θ(
√
N) quantum queries are both suﬃcient
[8, 16] and necessary [2]. Since any randomized algorithm requires Ω(N) queries in this case,
we still achieve a quadratic speedup over the best classical algorithm. For arbitrary formulas of
depth d, O(
√
N logd−1 N) queries suﬃce [5]. This is almost tight, as Barnum and Saks [7] have
shown that Ω(
√
N) queries are necessary to evaluate any AND-OR formula of any depth.
∗Department
of
Combinatorics
and
Optimization
and
IQC,
University
of
Waterloo,
Canada,
ambainis@math.uwaterloo.ca. Supported by NSERC, CIAR, ARO/DTO, MITACS and IQC.
1


---- page 2 ----

The second case is when, instead of a constant depth, we have a constant fan-out. This
case has been much harder and, until a few months ago, there has been no progress on it at
all. If we restrict to binary AND-OR trees, the classical complexity of computing the value of
a balanced binary AND-OR tree is Θ(N .754...) [20, 19, 21] and there was no better quantum
algorithm known.
In a breakthrough result, Farhi et al.
[14] showed that the value of a balanced binary
NAND tree can be computed in O(
√
N) quantum time in an unconventional continuous-time
Hamiltonian query model of [13, 18]. (Because of De Morgan’s laws, computing the value of
an AND-OR tree is equivalent to computing the value of a NAND tree.) Using a standard
reduction between continuous time and discrete time quantum computation [10], this yields an
O(N 1/2+ǫ) query quantum algorithm in the standard discrete time quantum query model, for
any ǫ > 0. (The big-O constant deteriorates, as the ǫ decreases.)
Soon after, Childs et al. [11] extended the result of [14] to computing the value of an arbitrary
binary NAND tree of depth in time O(
√
Nd) in the continuous-time Hamiltonian query model
and with O(N 1/2+ǫ) queries in the discrete-time query model.
In this paper, we improve over [14] and [11] by giving a better discrete time quantum query
algorithms for both balanced and general NAND trees. Namely, we give
1. An O(
√
N) query quantum algorithm for evaluating balanced binary NAND formulas,
which is optimal up to a constant factor.
2. An O(
√
Nd) query quantum algorithm for evaluating arbitrary binary NAND formulas of
depth d.
3. An O(N
1
2 +O(
1
√
log N )) query quantum algorithm for evaluating arbitrary binary NAND
formulas of any depth.
All of our algorithms are designed directly in the discrete quantum query model and do not
incur the overhead from converting from continuous to discrete time.
Besides better running time, our algorithms provide a new perspective for understanding
the quantum algorithms for this problem. When the breakthrough algorithm of [14] appeared,
its ideas seemed to be very diﬀerent from anything known before. Our new algorithm and its
analysis show intricate connections to the previous work on quantum search.
Although its technical details are complex, the main intuition is the same as in Grover’s
search [15] and its ”two reﬂections” analysis [1] which views the Grover’s algorithm as a sequence
of reﬂections in two-dimensional space against two diﬀerent axes. The idea of ”two reﬂections”
has come up in quantum algorithms over and over.
For example, the element distinctness
algorithm of [4], designed by diﬀerent methods, was re-cast in the form of two reﬂections by
Szegedy [22]. In this paper, we show that the NAND-tree algorithms can be viewed as another
instance of ”two-reﬂections”, with the reﬂections designed, using the structure of the NAND
tree.
2
Preliminaries
2.1
Quantum query model
We work in the standard discrete time quantum query model [3, 9]. In this model, the input
bits can be accessed by queries to an oracle X and the complexity of f is the number of queries
needed to compute f. A quantum computation with T queries is just a sequence of unitary
transformations
V0 →O →V1 →O →. . . →VT −1 →O →VT .
The Vj’s can be arbitrary unitary transformations that do not depend on the input bits
x1, . . . , xN. The O’s are query (oracle) transformations which depend on x1, . . . , xN. To deﬁne
2


---- page 3 ----

O, we represent basis states as |i, z⟩where i ∈{0, 1, . . ., N}. The query transformation Ox
(where x = (x1, . . . , xN)) maps |0, z⟩to |0, z⟩and |i, z⟩to (−1)xi|i, z⟩for i ∈{1, ..., N} (i.e., we
change phase depending on xi, unless i = 0 in which case we do nothing).
The computation starts with a state |0⟩. Then, we apply V0, Ox, . . ., Ox, VT and measure the
ﬁnal state. The result of the computation is the rightmost bit of the result of the measurement.
A quantum algorithm computes a function f(x1, . . . , xN) if, for any x1, . . . , xN ∈{0, 1}, the
probability that the result of the measurement is equal to f(x1, . . . , xN) is at least 2/3.
We will describe our algorithm in a high level language but it can be translated into a
sequence of transformations of this form.
2.2
Phase estimation
In our algorithm, we use phase estimation [12]. Assume that we are given a black box performing
a unitary transformation U and a state |ψ⟩which is an eigenstate of U: U|ψ⟩= eiθ|ψ⟩. Our goal
is to obtain an estimate ˜θ such that |˜θ −θ| < δ with probability at least 1 −ǫ. The algorithm
for phase estimation by [12] solves this problem by invoking U O( 1
δǫ) times.
If the input to this algorithm is a state |ψ⟩that is a linear combination of diﬀerent eigen-
states: |ψ⟩= P
j αj|ψj⟩with Ui|ψj⟩= eiθj|ψj⟩, then the algorithm works as if the input was a
probabilistic combination of |ψj⟩with probabilities |αj|2.
3
Summary of results and methods
3.1
Results
Let T be a read-once binary NAND formula involving variables x1, x2, . . ., xN. We can represent
T by a tree that have variables x1, . . . , xN at the leaves and NAND gates at the internal nodes.
Let d be the depth of T . We have
Theorem 1
1. If T is the complete binary tree, then T (x1, . . . , xN) can be computed with
O(
√
N) quantum queries.
2. For any binary tree T , T (x1, . . . , xN) can be computed with O(
√
dN) quantum queries.
We refer to the ﬁrst part of the theorem as the balanced case and to the second part as the
general case.
Bshouty et al. [6] have shown
Theorem 2 [6] For any NAND formula T of size S, there exists a NAND formula T ′ of size
S′ = O(S
1+O(
1
√
log S )) and depth d = O(S
O(
1
√
log S )) such that T ′ = T .
This theorem follows by substituting k = 2
1
√
log S into Theorem 6 of [6].
By combining
Theorems 1 and 2, we have
Corollary 1 For any T , T (x1, . . . , xN) can be computed with O(N
1
2 +O(
1
√
log N )) quantum queries.
If the formula T is not read once, the number of variables N is replaced by the size of the
formula S. This gives us
Corollary 2 If T (x1, . . . , xN) is computable by a NAND formula of size S, T is computable by
a quantum query algorithm with O(S
1
2 +O(
1
√
log S )) queries.
3


---- page 4 ----

The link between quantum query complexity and formula size was ﬁrst noticed by Laplante
et al. [17] who observed that, whenever quantum adversary lower bound method of [2] gives
a lower bound of Ω(M) for quantum query algorithms, it also gives a lower bound of Ω(M 2)
for formula size. Based on that, they conjectured that any Boolean function with formula size
M 2 has a quantum query algorithm with O(
√
M) queries. The results in [11] and this paper
show that it is indeed possible to transform an arbitrary NAND formula into a quantum query
algorithm, with almost a quadratic relation between formula size and the number of queries.
3.2
The algorithm
Our algorithm is the same for both parts of Theorem 3. Without the loss of generality, assume
that all leafs are at an even distance from the root. (If there is a leaf l at an odd depth, create
two new vertices v1, v2 and connect them to l, making l an internal node. v1, v2 are now leaves
at an even depth. If xi is the variable that used to be at the leaf l, replace it by two new
variables at leaves v1, v2 and make both of those equal to NOT xi. Then, the NAND of those
two variables at the vertex l will evaluate to xi.)
Tail
Tree
t
t-1
1
0
2
...
Figure 1: A tree T, augmented by a tail.
We augment the tree T by a “tail” of an even length t where t = 2⌈
√
N⌉in the balanced
case and t = 2⌈
√
Nd⌉in the general case. The tail is a path that starts at the root of T and
then goes through t newly created vertices. T ′ denotes the tree T , augmented by the tail (see
Figure 1).
Our state space H will be spanned by basis states |v⟩corresponding to vertices of T ′. We
use |i⟩(for i = 0, . . . , t) to denote the basis state corresponding to the ith vertex in the tail of
T ′. |0⟩corresponds to the root of T .
We deﬁne a Hermitian matrix H as follows:
1. If pc is an edge in T from a parent p to a child c, then Hpc = Hcp =
4q
mp
2mc if p is at an odd
level and Hpc = Hcp =
4q
2mc
mp if p is at an even level. (When T is the complete balanced
tree, this becomes Hcp = Hpc = 1.)
2. If uv is an edge in the tail, then Huv = Hvu = 1.
3. If uv is not an edge, then Huv = Hvu = 0.
Then, H is a Hermitian operator acting on H. Let SH,0 be the 0-eigenspace of H, SH,1 =
(SH,0)⊥and let U1 be deﬁned by U1|ψ⟩= |ψ⟩for |ψ⟩∈SH,0 and U1|ψ⟩= −|ψ⟩for |ψ⟩∈SH,1.
Let U2 be deﬁned by U2|ψ⟩= −|ψ⟩if |ψ⟩belongs to the subspace Sx,1 spanned by basis
states |v⟩that correspond to leaves containing variables xi = 1 and U2|ψ⟩= |ψ⟩if |ψ⟩belongs
to the subspace Sx,0 spanned by all other basis states |v⟩.
4


---- page 5 ----

U2 can be implemented with one query O. (It is essentially the query transformation Ox,
with basis states labelled in a diﬀerent way.)
U1 is independent of x1, . . . , xN and can be
implemented without using the query transformation O.
Let |ψstart⟩= Pt/2
i=0 |2i⟩. (This is the starting state for the continuous time algorithm of
Childs et al. [11].) Let |ψ′
start⟩= PSH,0|ψstart⟩and let |ψ′′
start⟩= |ψ′
start⟩
∥ψ′
start∥.
Theorem 3
1. If T evaluates to 0, there is a state |ψ0⟩such that U2U1|ψ0⟩= |ψ0⟩and
|⟨ψ0|ψ′′
start⟩|2 ≥c for some constant c > 0.
2. If T evaluates to 1, then, for any eigenstate |ψ0⟩of U2U1 which is not orthogonal to |ψ′′
start⟩,
the corresponding eigenvalue of U2U1 is eiθ, with θ = Ω(
1
√
Nd) for any T and θ = Ω(
1
√
N )
when T is the complete balanced tree.
We can distinguish the two cases by running the eigenvalue estimation for U2U1, with |ψ′′
start⟩
as the starting state, precision δ = θmin
2
where θmin is the lower bound on θ from the second
part of Theorem 3 (θmin = Θ(
1
√
Nd) or θmin = Θ(
1
√
N )) and error probability ǫ ≤c
3. In the ﬁrst
case, with probability |⟨ψ0|ψ′′
start⟩|2 ≥c, we get the same answer as if the input to eigenvalue
estimation was |ψ0⟩. Since the correct eigenvalue is 0, this means that we get an answer ˜θ < θmin
2
with probability at least (1 −ǫ)c.
In the second case, if we write out |ψ′′
start⟩as a linear combination of eigenvectors of U2U1,
all of those eigenvectors have eigenvalues that are eiθ, θ > θmin. Therefore, the probability of
the eigenvalue estimation outputting an estimate ˜θ < θmin −δ = θmin
2
is at most ǫ.
By our choice of ǫ, we have (1 −ǫ)c > ǫ. We can distinguish the two cases with arbitrarily
high probability, by repeating the eigenvalue estimation C times, for a suﬃciently large constant
C.
3.3
Proof overview
The ﬁrst part of Theorem 3 is proven by constructing the state |ψ0⟩. For the second part, we
show that the entire state-space H can be expressed as a direct sum of one-dimensional and
two-dimensional subspaces, with each subspace being mapped to itself by U1 and U2. Each one-
dimensional subspace consists of all multiples of some state |ψ⟩, with U1|ψ⟩and U2|ψ⟩being
either |ψ⟩or −|ψ⟩. Therefore, we either have U2U1|ψ⟩= |ψ⟩or U2U1|ψ⟩= −|ψ⟩. We show
that, if U2U1|ψ⟩= |ψ⟩, then |ψ⟩is orthogonal to the starting state |ψ′′
start⟩and, therefore, has
no eﬀect on the algorithm.
For two-dimensional subspaces, we show that each of them has an orthonormal basis |ψ11⟩,
|ψ12⟩such that U1|ψ11⟩= |ψ11⟩and U1|ψ12⟩= −|ψ12⟩and another orthonormal basis |ψ21⟩, |ψ22⟩
such that U2|ψ21⟩= |ψ21⟩and U2|ψ22⟩= −|ψ22⟩. Then, on this two-dimensional subspace, U2U1
is a product of two reﬂections, one w.r.t. |ψ11⟩and one w.r.t. |ψ21⟩. As in ”two reﬂections”
analysis [1] of Grover’s search, a product of two reﬂections in a two-dimensional plane is a
rotation of plane by 2β, where β is the angle between |ψ11⟩and |ψ21⟩. A rotation of the plane
by 2β has eigenvalues e±iβ. Therefore, we need to lower-bound β.
Since |ψ21⟩and |ψ22⟩are orthogonal, the angle between |ψ11⟩and |ψ22⟩is π
2 −β. Therefore,
|⟨ψ22|ψ11⟩| = sin β. Since |ψ22⟩belongs to Sx,1 and |ψ11⟩belongs to SH,0, we have
|⟨ψ22|ψ11⟩| = ∥PSx,1|ψ11⟩∥≥
min
|ψ⟩∈SH,0 ∥PSx,1|ψ⟩∥.
Therefore, to lower-bound sin β and β, it suﬃces to lower-bound the minimum of ∥PSx,1|ψ⟩∥for
|ψ⟩∈SH,0. We do that by an induction over the depth of the tree.
5


---- page 6 ----

4
Notation
In this section, we summarize the main notation used in this paper:
Trees. T is the tree which we are evaluating. T ′ is the tree T with the tail attached to it.
Tv is the subtree of T rooted at v. We also use T (or Tv) to denote the Boolean function deﬁned
by evaluating the NAND tree T (or Tv).
mv and dv denote the number of leaves and the depth of Tv. r denotes the root of T . Thus,
Tr = T .
Matrices. H is the weighted version of the adjacency matrix of T ′, deﬁned in section 3.2.
Hv is the restriction of H to rows and columns in Tv.
Subspaces.
SH,0 is the eigenspace of H with the eigenvalue 0.
SH,1 is the orthogonal
complement of SH,0: SH,1 = (SH,0)⊥. Sv,0 denotes the 0-eigenspace of Hv. S′
H,0 and S′
v,0 are
subspaces of SH,0 and Sv,0, deﬁned in section 7.
Sx,1 is the subspace spanned by |v⟩, for all leaves v that correspond to a variable xi = 1.
Sx,0 is the subspace spanned by all other |v⟩(for v that are either leaves corresponding to xi = 0
or non-leaves).
Unitary transformations U1 is deﬁned by U1|ψ⟩= |ψ⟩for |ψ⟩∈SH,0 and U1|ψ⟩= −|ψ⟩
for |ψ⟩∈SH,1. U2 is the query transformation. It can be equivalently described by deﬁning
U2|ψ⟩= |ψ⟩for |ψ⟩∈Sx,0 and U2|ψ⟩= −|ψ⟩for |ψ⟩∈Sx,1.
5
Structure of minimal certiﬁcates of Tv
Let C be a minimal certiﬁcate of Tv = 0. We would like to determine the structure of C. Let
z1 and z2 be the two children of v and y1, y2 (y3, y4) be the children of z1 (z2, respectively).
For Tv = 0, we need to have Tz1 = Tz2 = 1 which is equivalent to at least one of Ty1 and Ty2
and at least one of Ty3 and Ty4 evaluates to 0. Thus, a minimal 0-certiﬁcate for Tv consists of
a minimal 0-certiﬁcate for one of Ty1 = 0 and Ty2 = 0 and a minimal 0-certiﬁcate for one of
Ty3 = 0 and Ty4 = 0. Each of those 0-certiﬁcates can be decomposed in a similar way.
0
0
0
1
1
1
0
0
1
1
1
1
0
1
1
0
1
0
1
1
0
1
1
0
0
1
1
0
0
0
1
Figure 2: An extended certiﬁcate for Tv = 0.
We now deﬁne an extended minimal certiﬁcate for Tv = 0 to consist of v, an extended
minimal certiﬁcate for one of Ty1 = 0 and Ty2 = 0 and an extended minimal 0-certiﬁcate for
one of Ty3 = 0 and Ty4 = 0. Intuitively, an extended minimal certiﬁcate is a minimal certiﬁcate,
augmented by non-leaf vertices that must evaluate to 0 on this certiﬁcate. We can show
Lemma 1 Let C be an extended minimal certiﬁcate. If a non-leaf vertex w belongs to C, z1
and z2 are the two children of w and y1, y2 (y3, y4) are the children of z1 (z2, respectively),
then exactly one of y1, y2 and exactly one of y3, y4 belongs to C.
6


---- page 7 ----

Proof: In appendix A.
We show an example of an extended certiﬁcate for Tv = 0 in ﬁgure 2. The vertices that
belong to the extended certiﬁcate are shown by squares.
For each extended minimal certiﬁcate C of Tv = 0, we can deﬁne a state |ψC⟩that has
non-zero amplitudes only in the vertices of C, in a following way:
1. Decompose C as C = Cyi ∪Cyj ∪{v}, where Cyi is an extended certiﬁcate for Tyi = 0,
i ∈{1, 2} and Cyj is an extended certiﬁcate for Tyj = 0, j ∈{3, 4}.
2. Construct |ψCyi ⟩and |ψCyj ⟩inductively and deﬁne
|ψC⟩= |v⟩−
4√mv
4p4myi
|ψCyi ⟩−
4√mv
4p4myj
|ψCyj ⟩.
(1)
Lemma 2 Let C be an extended minimal certiﬁcate for Tv = 0. Then,
Hv|ψC⟩= 0.
Proof: In appendix A.
Lemma 3
(a) If T is balanced, ∥ψCv∥2 ≤2√mv −1.
(b) For any T , ∥ψCv∥2 ≤2√mvdv.
Proof: In appendix A.
6
Proof of Theorem 1: T = 0 case
Let C be an extended minimal 0-certiﬁcate of Tr where r is the root of the tree and let |ψC⟩
be the corresponding state (deﬁned so that the amplitude αr of the root is 1).
We deﬁne
|ψ0⟩= |ψC⟩+ Pt/2
i=1(−1)i|2i⟩. Let |ψ′
0⟩be the corresponding normalized state: |ψ′
0⟩= |ψ0⟩
∥ψ0∥.
We claim that U2U1|ψ0⟩= |ψ0⟩. This follows from U2|ψ⟩= |ψ⟩(which is true, because |ψC⟩
and |ψ0⟩are only non-zero on the vertices that belong to the extended certiﬁcate C and xi = 0
for all variables xi at the leaves that belong to a certiﬁcate C) and U1|ψ0⟩= |ψ0⟩(which follows
from the next lemma).
Lemma 4
H|ψ0⟩= 0.
Proof: It suﬃces to show that, for every u, the amplitude of u in H|ψ0⟩is 0. For vertices in the
tree T , their amplitudes in H|ψ0⟩are the same as their amplitudes in Hr|ψC⟩and, by Lemma
2, Hr|ψC⟩= 0.
For vertices j in the tail, the amplitude of j in H|ψ0⟩is the sum of the amplitudes of its
two neighbors of j −1 and j + 1 in |ψ0⟩. If j = 2i is even, then both 2i −1 and 2i + 1 have
amplitudes 0 and their sum is 0. If j = 2i + 1 is odd, then one of 2i and 2i + 2 has amplitude 1
and the other has amplitude -1, resulting in the sum of amplitudes being 0.
To complete the proof of the ﬁrst part of Theorem 3, we show
Lemma 5 If t >
√
N (for the balanced case) or t >
√
Nd (for the unbalanced case), then
⟨ψ′
0|ψ′′
start⟩≥
1
√
5.
7


---- page 8 ----

Proof: We show the proof for the balanced case. (For the unbalanced case, just replace N by
Nd everywhere.)
Since |ψ′
0⟩∈SH,0 (by Lemma 4), we have
⟨ψ′
0|ψstart⟩= ⟨ψ′
0|PSH,0|ψstart⟩= ∥ψ′
start∥⟨ψ′
0|ψ′′
start⟩≤⟨ψ′
0|ψ′′
start⟩.
Therefore, it suﬃces to prove ⟨ψ′
0|ψstart⟩≥
1
√
5. We have
⟨ψ′
0|ψstart⟩= ⟨ψ0|ψstart⟩
∥ψ0∥
.
Since each of the basis states |2j⟩has amplitude 1 in |ψ0⟩and amplitude
1
√t
2 +1 in |ψstart⟩, we
have ⟨ψ0|ψstart⟩=
q
t
2 + 1. We also have
∥ψ0∥2 = ∥ψC∥2 + t
2 ≤2
√
N + t
2 ≤2.5t.
Therefore,
⟨ψ0|ψstart⟩
∥ψ0∥
≥
q
t
2 + 1
√
2.5t
=
1
√
5.
⟨ψ′
0|ψ′′
start⟩can be increased to 1 −ǫ by taking t ≥C
√
N for suﬃciently large constant C.
7
Proof of Theorem 1: T = 1 case
7.1
Overview
We ﬁrst describe a subset of the 1-eigenstates |ψ⟩of U2U1. Let v be a vertex of an odd depth 2j+1
and let v1 and v2 be the children of v. Assume that Tv1 = Tv2 = 0 and let C1, C2 be the extended
minimal certiﬁcates for Tv1 = 0 and Tv2 = 0. Deﬁne |ψC1,C2⟩=
4√mv1|ψC1⟩−
4√mv2|ψC2⟩.
Lemma 6 U2|ψC1,C2⟩= U1|ψC1,C2⟩= |ψC1,C2⟩.
Proof: In appendix A.
We deﬁne S′
H,0 to be the subspace spanned by all |ψC1,C2⟩, for all possible choices of v, C1
and C2. Observe that S′
H,0 is orthogonal to the starting state |ψstart⟩(since the state |ψstart⟩
only has non-zero amplitude on the root and in the tail and any of the states |ψC1,C2⟩always has
zero amplitudes there). Since S′
H,0 ⊆SH,0, S′
H,0 is also orthogonal to |ψ′
start⟩= PSH,0|ψstart⟩
and |ψ′′
start⟩= |ψ′
start⟩
∥ψ′
start∥.
Theorem 3 follows from the following two lemmas:
Lemma 7 Let S be a Hilbert space, let S1, S2 be two subspaces of S and let Ui (i ∈{1, 2})
be the unitary transformation on S deﬁned by Ui|ψ⟩= −|ψ⟩for |ψ⟩∈Si and Ui|ψ⟩= |ψ⟩for
|ψ⟩∈(Si)⊥. Assume that S1 ∩S2 = {−→0 } and, for any |ψ⟩∈S1, we have
∥P(S2)⊥|ψ⟩∥2 ≥ǫ.
Then, all eigenvalues of U2U1 are of the form eiθ with θ ∈[√ǫ, 2π −√ǫ].
Lemma 8 For any state |ψ⟩∈SH,0 ∩(S′
H,0)⊥, ∥PSx,1|ψ⟩∥2 ≥c∥ψ∥2 for a constant c, where
c = Ω( 1
N ) in the balanced case and c = Ω( 1
Nd) in the general case.
8


---- page 9 ----

Given the two lemmas, the proof of Theorem is completed as follows. Deﬁne S = (S′
H,0)⊥∩
(SH,1 ∩Sx,1)⊥. For both S′
H,0 and SH,1 ∩Sx,1, U1 and U2 map those subspaces to themselves.
Since U1 and U2 are unitary, this means that U1 and U2 map S to itself, as well. Combining
Lemma 7 and 8 implies that all eigenvalues of U2U1 on S are eiθ with θ ∈[δ, 2π −δ], with
δ = Ω(
1
√
N ) in the balanced case and δ = Ω(
1
√
Nd) in the general case.
Since S′
H,0 and SH,1 are both orthogonal to |ψ′′
start⟩, the state |ψ′′
start⟩belongs to S. Therefore,
all eigenvectors of U2U1 which are not orthogonal to |ψ′′
start⟩must lie in S and, therefore, have
eigenvalues eiθ of the required form. This completes the proof of the theorem.
Lemma 7 is fairly similar to previous work.
We give its proof in Appendix B.
In the
next section, we give the proof of Lemma 8, postponing some of the technical details till the
appendices.
7.2
Proof of Lemma 8
This lemma is equivalent to the next one.
Lemma 9 For any state |ψ⟩∈SH,0, there exists a state |ψ′⟩∈S′
H,0 such that
∥PSx,1(|ψ⟩+ |ψ′⟩)∥2 ≥c∥|ψ⟩+ |ψ′⟩∥2
for a constant c, where c = Ω( 1
N ) in the balanced case and c = Ω( 1
Nd) in the general case.
Proof: [of Lemma 8] By construction of S′
H,0, any state in S′
H,0 is orthogonal to Sx,1. Let
|ψ⟩∈SH0 ∩(S′
H,0)⊥. We use Lemma 9 to obtain |ψ′⟩∈S′
H,0. Then, we have
∥PSx,1|ψ⟩∥2 = ∥PSx,1(ψ + ψ′)∥2 ≥c∥ψ + ψ′∥2 = c∥ψ∥2 + c∥ψ′∥2 ≥c∥ψ∥2,
with the ﬁrst equality following from |ψ′⟩being orthogonal to Sx,1, the second inequality from
lemma 9 and the the third equality following from |ψ⟩being orthogonal to |ψ′⟩(which is true
because |ψ′⟩∈S′
H,0 but |ψ⟩∈(S′
H,0)⊥).
Proof: [of Lemma 9] We recall that Sv,0 is the 0-eigenspace of Hv. We deﬁne S′
v,0 to be the
subspace spanned by all |ψC1,C2⟩which only have non-zero amplitudes for |u⟩, u ∈Tv. Then,
we have S′
v,0 ⊆Sv,0.
For a state |ψ⟩, we deﬁne
Lv(ψ) = ∥ψ∥2 −K∥PSx,1ψ∥2
|αv|2
where αv is the amplitude of v of Tk in |ψ⟩and K will be deﬁned later.
The next lemma is slightly diﬀerent for balanced NAND trees and general NAND trees.
Below is the variant for balanced trees. The counterpart for general trees is described in appendix
D.
Lemma 10 Let K ≥20N and let v be a vertex at depth 2k. For any state |ψ⟩∈Sv,0, there
exists a state |ψ′⟩∈S′
v,0 such that, for |ψ′′⟩= |ψ⟩+ |ψ′⟩, we have
1. If Tk(x1, . . . , xN) = 0, then
Lv(ψ) ≤av,
av =

1 + 222k
K

(2k+1 −1).
2. If Tk(x1, . . . , xN) = 1, then
Lv(ψ) ≤−bv,
bv =

1 −222k
K
 K
2k .
9


---- page 10 ----

Given Lemma 10, the proof of Lemma 9 can be completed as follows. Let |ψ⟩be a 0-eigenstate
of H. Then, we can decompose |ψ⟩= |ψtree⟩+ |ψtail⟩, with |ψtree⟩being a superposition over
vertices in T (including the root) and |ψtail⟩being a superposition over vertices in the tail.
Let αr be the amplitude of the root in |ψ⟩. In both balanced and general case, we have
Lemma 11 Let |ψ⟩= P
u αu|u⟩be a 0-eigenstate of H (or Hv, for some v). Then, any vertex
u of an odd depth (or any u in the tail at an odd distance from the root) must have αu = 0.
Proof: In appendix A.
By this lemma, H|ψ⟩= 0 implies that the amplitudes of the vertices in the tail at an odd
distance from the root are 0. Also, to achieve H|ψ⟩= 0, the amplitudes at an even distance
from the root must be ±αr. Therefore, ∥ψtail∥2 = t
2|αr|2.
We have Hr|ψtree⟩= 0. Therefore, we can apply Lemma 10 with v = r and |ψtree⟩instead of
|ψ⟩, obtaining a state |ψ′⟩∈S′
r,0 ⊆S′
H,0. We let |ψ′′
tree⟩= |ψtree⟩+|ψ′⟩and |ψ′′
all⟩= |ψ⟩+|ψ′⟩=
|ψ′′
tree⟩+ |ψtail⟩. Then,
∥ψ′′
all∥2 = ∥ψ′′
tree∥2 + t
2|αr|2.
We have PSx,1|ψ′′
all⟩= PSx,1|ψ′′
tree⟩. From Lemma 10,
∥ψ′′
tree∥2 ≤K∥PSx,1|ψ′′
tree⟩∥−br|αr|2.
This means that
∥ψ′′
all∥2 +

br −t
2

|αr|2 ≤K∥PSx,1|ψ′′
all⟩∥.
If t = 2⌈
√
N⌉, we have br ≥
t
2 (this can be veriﬁed by substituting the deﬁnition of br).
Therefore, ∥PSx,1|ψ′′
all⟩∥≥∥ψ′′
all∥2
K
.
The balanced case is based on similar ideas but has some minor changes in the expressions
that appear in Lemma 10 (with the main change being K ≥20N replaced by K ≥30Nd, which
results in a bound of c = Ω( 1
Nd) instead of c = Ω( 1
N )). We discuss that in appendix D.
Acknowledgments. I thank Richard Cleve and John Watrous for the discussion that lead
me to discovering the main idea of the paper.
References
[1] D. Aharonov. Quantum computation - a review. Annual Review of Computational Physics,
World Scientiﬁc, volume VI. Also quant-ph/9812037.
[2] A. Ambainis. Quantum lower bounds by quantum arguments. Journal of Computer and
System Sciences, 64:750-767, 2002. Also quant-ph/0002066.
[3] A. Ambainis. Quantum search algorithms (a survey). SIGACT News, 35(2):22-35, 2004.
Also quant-ph/0504012.
[4] A. Ambainis. Quantum walk algorithm for element distinctness. Proceedings of FOCS’04,
pp. 22-31. Also quant-ph/0311001.
[5] A. Ambainis. Quantum search with variable times, quant-ph/0609188.
[6] N. Bshouty, R. Cleve, W. Eberly. Size-depth tradeoﬀs for algebraic formulas. SIAM J.
Comput. 24(4): 682-705 (1995)
[7] H. Barnum, M. Saks. A lower bound on the quantum query complexity of read-
once functions. Journal of Computer and System Sciences, 69(2): 244-258 (2004). Also
quant-ph/0201007.
10


---- page 11 ----

[8] H. Buhrman, R. Cleve, A. Wigderson. Quantum vs. Classical Communication and Com-
putation. Proceedings of STOC’98, pp. 63-68. Also quant-ph/9802040.
[9] H. Buhrman, R. de Wolf. Complexity measures and decision tree complexity: a survey.
Theoretical Computer Science, 288:21-43, 2002.
[10] A. Childs, R. Cleve, S. Jordan, D. Yeung. Discrete-query quantum algorithm for NAND
trees, quant-ph/0702160.
[11] A. Childs, B. Reichardt, R. Spalek, S. Zhang. Every NAND formula on N variables can be
evaluated in time O(N 1/2+ǫ), quant-ph/0703015.
[12] R. Cleve, A. Ekert, C. Machiavello, M. Mosca. On Quantum Algorithms. Complexity, 4:33-
42, 1998.
[13] E. Farhi, S. Gutmann, An analog analogue of a digital quantum computation. Physical
Review A, 57:2403, 1997, quant-ph/9612026.
[14] E. Farhi, J. Goldstone, S. Gutmann. A Quantum Algorithm for the Hamiltonian NAND
Tree, quant-ph/0702144.
[15] L. Grover. A fast quantum mechanical algorithm for database search. Proceedings of
STOC’96, pp. 212-219. Also quant-ph/9605043.
[16] P. Høyer, M. Mosca, R. de Wolf. Quantum Search on Bounded-Error Inputs. Proceedings
of ICALP’03, pp. 291-299. Also quant-ph/0304052.
[17] S. Laplante, T. Lee, M. Szegedy. The quantum adversary method and classical formula size
lower bounds. Computational Complexity, 15(2): 163-196, 2006. Also quant-ph/0501057.
[18] C. Mochon. Hamiltonian oracles, quant-ph/0602032.
[19] M. Saks, A. Wigderson. Probabilistic Boolean decision trees and the complexity of evalu-
ating game trees, Proceedings of FOCS’86, pp. 29-38.
[20] M. Santha. On the Monte Carlo Boolean Decision Tree Complexity of Read-Once Formulae.
Random Structures and Algorithms, 6(1): 75-88, 1995.
[21] M. Snir. Lower bounds on probabilistic linear decision trees. Theoretical Computer Science,
38: 69-82, 1985.
[22] M. Szegedy. Quantum speed-up of Markov chain based algorithms. Proceedings of FOCS
2004, pp. 32-41.
11


---- page 12 ----

Appendix
A
Lemmas on the structure of minimal certiﬁcates
Proof: [of Lemma 1] If w belongs to C, then C contains an extended minimal certiﬁcate for
Tw = 0 which, by the argument before the statement of lemma 1 in section 5 (with w instead of
v) must contain an extended minimal certiﬁcate for one of Ty1 = 0 and Ty2 = 0 and an extended
minimal certiﬁcate for one of Ty3 = 0 and Ty4 = 0. From the construction of extended minimal
certiﬁcates, a certiﬁcate for Tw = 0 contains yi if and only if it contains a certiﬁcate for Tyi = 0.
Proof: [of Lemma 2] Since Hv has non-zero entries only in the places corresponding to the
edges of T , the amplitude of each basis state |u⟩in Hv|ψ0⟩is just the sum of amplitudes of the
neighbors of u in |ψ0⟩, multiplied by the appropriate factors. We need to show that, for every
u, this sum is 0.
For vertices u in the subtree Tv, if u is at an even depth 2l, then its neighbors are at an
odd depth (2l −1 or 2l + 1) and their amplitudes are 0. If u is at an odd depth 2l + 1, let p
be the parent of u and let y1, y2 be the two children of u. If p does not belong to C, than none
of p’s descendants belongs to C as well, including y1 and y2. Then, all the neighbors of u have
amplitude 0 in |ψ0⟩. If p ∈C, then by Lemma 1, exactly one of y1 and y2 belongs to C. Assume
that y1 ∈C. Let α be the amplitude of p. By equation (1), the amplitude of y1 is −
4√mp
4√
4my1 α.
The amplitude of u in Hv|ψ⟩is
Hupα −Huy1
4√mp
4p4my1
α =
4
r mp
2mu
α −
4
r
2my1
mu
4√mp
4p4my1
α = 0.
Proof: [of Lemma 3]
Part (a). By induction on the depth of Tv. If Cv is a leaf, then mv = 1 and ∥ψCv∥≤2
√
1−1.
For the inductive case, decompose Cv = {v}∪Cy1∪Cy2. By eq. (1) and the inductive assumption,
we have
∥ψCv∥2 ≤1 +
√mv
2√my1
(2√my1 −1) +
√mv
2√my2
(2√my2 −1)
≤2√mv −√mv

1
2√my1
+
1
2√my2

+ 1 = 2√mv −1,
with the ﬁrst inequality following from the inductive assumption, the second inequality following
by rearranging terms and the third following from my1 = my2 = mv
2 (since the tree is balanced).
Part (b). By induction on the depth of Tv. If Cv is a leaf, then mv = dv = 1 and ∥ψCv∥=
1 ≤2
√
1.
For the inductive case, decompose Cv = {v} ∪Cy1 ∪Cy2. By eq. (1) and the inductive
assumption, we have
∥ψCv∥2 = 1 +
√mv
2√my1
∥ψCy1∥2 +
√mv
2√my2
∥ψCy2∥2
≤1 +
√mv
2√my1
2
p
my1dy1 +
√mv
2√my2
2
p
my2dy2 = 1 +
p
mvdy1 +
p
mvdy2
≤1 + 2
p
mv(dv −1) ≤mv
dv
+ 2
p
mv(dv −1) ≤2
p
mvdv,
12


---- page 13 ----

with the ﬁrst inequality following from the inductive assumption, the second inequality following
from dy1 ≤dv −1, dy2 ≤dv −1, the third inequality following from dv ≤mv (the depth
of a tree is always at most the number of leaves) and the fourth inequality following from
√
A −√A −1 =
1
√
A+√A−1 ≥
1
2
√
A.
Proof: [of Lemma 6] To prove U1|ψC1,C2⟩= |ψC1,C2⟩, we need to show H|ψC1,C2⟩= 0. Consider
the amplitude of |u⟩in H|ψC1,C2⟩. If u belongs to Tv1 or Tv2, its amplitude in H|ψC1,C2⟩are 0
by Lemma 2. If u = v, its amplitude in H|ψC1,C2⟩is
Huv1
4√mv1 −Huv2
4√mv2 =
4√mu
4√2mv1
4√mv1 −
4√mu
4√2mv2
4√mv2 = 0.
If u is outside Tv, then it has no neighbors in Tv, except for possibly v itself. That means that
all of u’s neighbors have amplitude 0 in |ψC1,C2⟩and the amplitude of |u⟩in H|ψC1,C2⟩is 0.
For U2, we have U2|ψC1,C2⟩= |ψC1,C2⟩because the only leaves v with |v⟩having a non-zero
amplitude in |ψC1,C2⟩are those for which the corresponding variable xi belongs to C1 or C2 and
all the variables xi in a certiﬁcate Cj have xi = 0 which means that U2|v⟩= |v⟩.
Proof: [of Lemma 11] We prove the lemma for the general case.
The proof is by induction. For the base case, let u be a vertex of depth 1 (i.e. at a distance
1 from a leaf). Then, u is connected to a leaf w. Since w is a leaf, u is the only neighbor of w.
This means that the amplitude of w in H|ψ⟩is equal to Huwαu. Since H|ψ⟩= 0 and Huw ̸= 0,
it must be the case that αu = 0.
For the inductive case, assume that αu = 0 for vertices u of depth 2i+1, for i ∈{0, . . . , l−1}.
Let u be a vertex at the depth 2l + 1. Let c be one of the two children of u. Let v1 and v2 be
the children of c. Then, the amplitude of c in H|ψ⟩is equal to Hucαu + Hcv1αv1 + Hcv2αv2 and
it must be equal to 0. By the inductive assumption, αv1 = αv2 = 0. Therefore, αu = 0.
The proof for the vertices in the tail is similar, starting with the vertex that is adjacent to
the end of the tail and proceeding inductively towards the root.
B
Proof of Lemma 7
Similar statements have been proven before (e.g. [22]) but none of them has the exact form that
we need. Therefore, we include the proof for completeness.
Let |ψ⟩be an eigenvector of U2U1 with an eigenvalue λ. We consider the following possibil-
ities:
1. U1|ψ⟩= |ψ⟩. Then, |ψ⟩is an eigenvector of U2U1 if and only if it is an eigenvector of U2.
We cannot have U2|ψ⟩= |ψ⟩because, by the conditions of the lemma, ∥P(S2)⊥|ψ⟩∥> 0.
Since all eigenvalues of U2 are ±1, this means that U2|ψ⟩= −|ψ⟩and U2U1|ψ⟩= −|ψ⟩.
2. U1|ψ⟩= −|ψ⟩. Again, |ψ⟩is an eigenvector of U2U1 if and only if it is an eigenvector of
U2. We cannot have U2|ψ⟩= −|ψ⟩because, then |ψ⟩would belong to S1 ∩S2 and the
lemma assumes that S1 ∩S2 = {−→0 }. Therefore, U2|ψ⟩= |ψ⟩and U2U1|ψ⟩= −|ψ⟩.
3. U1|ψ⟩̸= |ψ⟩and U1|ψ⟩̸= −|ψ⟩.
Then, |ψ⟩is not an eigenvector of U1. This means that |ψ⟩and |ψ′⟩= U1|ψ⟩span a two
dimensional subspace which we denote H2. Since U 2
1 = I, we also have |ψ⟩= U1|ψ′⟩.
This means that U1 maps H2 to itself. U2 also maps H2 to itself, because it maps |ψ′⟩to
U2|ψ′⟩= U2U1|ψ′⟩= λ|ψ⟩and, since U 2
2 = I, this means that U2|ψ⟩= λ−1|ψ′⟩.
Therefore, U2 and U1 both map H2 to itself. Let |ψi1⟩, |ψi2⟩be the eigenvectors of Ui
in H2. One of |ψ11⟩, |ψ12⟩must have an eigenvalue that is +1 and the other must have
an eigenvalue -1. (Otherwise, all of H2, including |ψ⟩, would be eigenvectors of U1 with
the same eigenvalue and then we would have one of the ﬁrst two cases.) Similarly, one of
|ψ21⟩, |ψ22⟩must have an eigenvalue +1 and the other must have an eigenvalue -1.
13


---- page 14 ----

For simplicity, assume that |ψ11⟩and |ψ21⟩are the eigenvectors with eigenvalue 1. Then,
U2U1 is a composition of reﬂections w.r.t. |ψ11⟩and |ψ21⟩. By the analysis in [1], the
eigenvalues of U2U1 on H2 are e±iβ, where β is the angle between |ψ11⟩and |ψ21⟩. We
have
∥P(S2)⊥|ψ11⟩∥2 = |⟨ψ11|ψ22⟩|2 = sin2 β.
By the conditions of the lemma, we have sin2 β ≥ǫ which implies β ∈[√ǫ, π
2 ].
C
Evaluating balanced trees: proof of Lemma 10
Since av and bv only depend on k, we will denote them ak and bk. We ﬁrst state some simple
bounds on ak and bk.
Claim 1
(a) ak ≤1.1 · 2k+1;
(b) bk ≥0.9 · K
2k ;
(c) ak ≤0.13bk;
Proof: The ﬁrst two parts follow from 2 22k
K ≤2 N
20N = 0.1. The third part follows by
ak ≤1.1 · 2k+1 ≤0.11 K
2k ≤0.13bk,
with the second inequality using K ≥20N ≥20 · 22k and the third inequality using part (b).
The proof of Lemma 10 is by an induction on k. The basis case is k = 0. Then, the tree
consists of the vertex v only. The only possible states |ψ⟩are multiples of |v⟩. v is also the
only leaf, carrying a variable x1 and T0(x1) = x1. If x1 = 0, then Sx,1 is empty, meaning that
L(ψ) = 1. If x1 = 1, then Sx,1 consists of all multiples of |v⟩, meaning that PSx,1|ψ⟩= |ψ⟩and
L(ψ) = −(K −1). In both cases, the lemma is true.
For the inductive case, let z1 and z2 be the children of v, y1 and y2 be the children of z1 and
y3, y4 be the children of z2. We can decompose the state |ψ⟩as
|ψ⟩= αv|v⟩+ |ψ1⟩+ |ψ2⟩
where |ψi⟩∈Szi,0. We claim
Claim 2 For every i ∈{1, 2}, there exists |ψ′
i⟩∈S′
zi,0 such that, for the state |ψ′′
i ⟩= |ψi⟩+|ψ′
i⟩,
we have
1. If Tz1(x1, . . . , xN) = 0, then
∥ψ′′
i ∥−∥Px,1|ψ′′
i ⟩∥≤−bk−1
2
|αv|2.
(2)
2. If Tz1(x1, . . . , xN) = 1, then
∥ψ′′
i ∥−∥Px,1|ψ′′
i ⟩∥≤ak −1
2
|αv|2.
(3)
Proof: For typographical convenience, let i = 1. For the ﬁrst part, Tz1 = 0 if and only if
Ty1 = Ty2 = 1.
By Lemma 11, the amplitude of |zi⟩in |ψ1⟩is 0. Therefore, we can decompose
|ψ1⟩= |ϕ1⟩+ |ϕ2⟩,
14


---- page 15 ----

with |ϕi⟩∈Syi,0. By the inductive assumption, there exist states |ϕ′
1⟩, |ϕ′
2⟩∈S′
yi,0 such that,
for the states |ϕ′′
i ⟩= |ϕi⟩+ |ϕ′
i⟩, we have
∥ϕ′′
i ∥2 −∥PSx,1|ϕ′′
i ⟩∥2 ≤−bk−1|αyi|2,
(4)
with αyi being the amplitude of yi in |ϕi⟩. We deﬁne |ψ′
1⟩= |ϕ′
1⟩+ |ϕ′
2⟩and |ψ′′
1 ⟩= |ψ1⟩+ |ψ′
1⟩.
By summing equations (4) for i = 1 and i = 2, we get
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤−bk−1
2
X
i=1
|αyi|2.
(5)
Because of αy1 + αy2 + αv = 0, we have |αy1|2 + |αy2|2 ≥|αv|2
2
. Therefore, (5) implies
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1 ⟩∥2 ≤−bk−1
2
|αv|2.
For the second part, we consider two cases:
1. y1 = y2 = 0.
Let C be a minimal 0-certiﬁcate for r = 1 and |ψC⟩be the state corresponding to this
certiﬁcate. Let |ψ1⟩= P
u αu|u⟩. We deﬁne
|φ1⟩= αy1 −αy2
2
|ψC⟩.
Let |ψ1⟩+ |φ1⟩= P
v βv|v⟩. Then, βy1 = βy2 = αy1 +αy2
2
. Because of αy1 + αy2 + αv = 0,
we have βy1 = βy2 = −αv
2 .
We decompose
|ψ1⟩+ |φ1⟩= |ϕ1⟩+ |ϕ2⟩,
with |ϕi⟩being a superposition over Tyi. By the inductive assumption, there exist states
|ϕ′
1⟩, |ϕ′
2⟩∈SH,0 such that, for the states |ϕ′′
i ⟩= |ϕi⟩+ |ϕ′
i⟩, we have
∥ϕ′′
i ∥2 −∥PSx,1|ϕ′′
i ⟩∥2 ≤ak−1|αyi|2.
(6)
We deﬁne |ψ′
1⟩= |φ1⟩+|ϕ′
1⟩+|ϕ′
2⟩and |ψ′′
1⟩= |ψ1⟩+|ψ′
1⟩. Summing up eq. (6) for i = 1, 2
gives
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1 ⟩∥2 ≤ak−1(|βy1|2 + |βy2|2) = ak−1
2
|αv|2.
The claim now follows from ak−1 ≤ak −1 which is easy to prove.
2. one of y1, y2 is 0 and the other is 1.
For typographical convenience, assume that y1 = 0, y2 = 1. Once again, we decompose
|ψ1⟩= |ϕ1⟩+ |ϕ2⟩,
with |ϕi⟩being a superposition over Tyi. By the inductive assumption, there exist states
|ϕ′
1⟩, |ϕ′
2⟩∈SH,0 such that, for the states |ϕ′′
i ⟩= |ϕi⟩+ |ϕ′
i⟩, we have (4) for i = 1 and (6)
for i = 2. We deﬁne |ψ′
1⟩= |ϕ′
1⟩+ |ϕ′
2⟩, |ψ′′
1⟩= |ψ1⟩+ |ψ′
1⟩and sum up the equations from
the inductive assumption. This gives us
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤ak−1|αy1|2 −bk−1|αy2|2.
(7)
Let |αy2| = δ|αv|. Then, because of αy1 + αy2 + αv = 0, we have |αy1| ≤(1 + δ)|αv|. We
now upper-bound the expression
ak−1|αy1|2 −bk−1|αy2|2 ≤ak−1(1 + δ)2|αv|2 −bk−1δ2|αv|2.
15


---- page 16 ----

Let f(δ) = ak−1(1 + δ)2 −bk−1δ2. Then, f ′(δ) = 2(1 + δ)ak−1 −2δbk−1. The maximum
of f(δ) is achieved when f ′(δ) = 0 which is equivalent to δ(ak−1 −bk−1) = −ak−1 and
δ =
ak−1
bk−1−ak−1 . Then,
f(δ) = ak−1

bk−1
bk−1 −ak−1
2
−bk−1

ak−1
bk−1 −ak−1
2
=
ak−1bk−1
bk−1 −ak−1
.
This means that
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤
ak−1bk−1
bk−1 −ak−1
|αv|2.
To complete the case, it suﬃces to show
2 ak−1bk−1
bk−1 −ak−1
+ 1 ≤ak.
(8)
We have
2 ak−1bk−1
bk−1 −ak−1
= 2

1 +
ak−1
bk−1 −ak−1

ak−1 ≤2

1 + 1.1 · 2k
0.87bk

ak−1
≤2
 
1 +
1.1 · 2k
0.87 · 0.9
K
2k−1
!
ak−1 ≤2

1 + 1.4122k−1
K

ak−1
≤2

1 + 2.8222k−2
K
 
1 + 222k−2
K

(2k −1) ≤

1 + 222k
K

(2k+1 −2),
(9)
with the ﬁrst inequality following from parts (a) and (c) of Claim 1, the second inequality
following from part (b) of Claim 1, the fourth inequality following by writing out ak−1 and
the last inequality following from (1+2δ)(1+2.82δ) ≤1+8δ (where δ = 22k−2
K
) being true
for suﬃciently small δ. The equation (8) now follows by adding 1 to both sides of eq. (9).
To deduce lemma 10 from claim 2, we deﬁne
|ψ′⟩= |ψ′
1⟩+ |ψ′
2⟩.
Let |ψ′′⟩= |ψ⟩+ |ψ′⟩. Then, we also have
|ψ′′⟩= αv|v⟩+ |ψ′′
1 ⟩+ |ψ′′
2 ⟩.
If Tr = 0, then Tz1 = Tz2 = 1. By summing up eq. (3) for i = 1, 2 and adding |αv|2 to both
sides, we get
∥ψ′′∥−∥Px,1|ψ′′⟩∥≤ak|αv|2.
If Tr = 1, then we again have two cases:
1. Tz1 = Tz2 = 1.
By summing up eq. (2) for i = 1, 2 and adding |αv|2 to both sides, we get
∥ψ′′∥−∥Px,1|ψ′′⟩∥≤−(bk−1 −1)|αv|2.
The lemma follows from bk−1 −1 ≥bk which is easy to prove.
2. one of z1, z2 is 0 and the other is 1.
For typographical convenience, assume that z1 = 0, z2 = 1. In this case, claim 2 gives us
∥ψ′′∥−∥Px,1|ψ′′⟩∥≤−bk−1 −ak −1
2
|αv|2.
To complete the proof, we need to show that bk−1−ak−1
2
≥bk. This follows by substituting
the expressions for ak, bk−1 and bk.
16


---- page 17 ----

D
General case
The counterpart of Lemma 10 is
Lemma 12 Let K = 30Nd. For v ∈T , deﬁne δv = 5mv
√dv
K
+
dv
√
K , where dv is the depth of
the subtree Tv. For any v of even depth and any state |ψ⟩∈Sv,0, there exists a state |ψ′⟩∈S′
v,0
such that, for |ψ′′⟩= |ψ⟩+ |ψ′⟩, we have
1. If Tv(x1, . . . , xN) = 0, then
Lv(ψ) ≤av,
av = 2(1 + δv)
p
dvmv.
2. If Tk(x1, . . . , xN) = 1, then
Lv(ψ) ≤−bv,
bv = (1 −δv) K
√mv
.
Observe that, because of mv ≤N and dv ≤d ≤N, we always have
δv ≤5N
√
d
30Nd +
d
30
√
dN
≤5
30 + 1
30 = 1
5.
Proof: By induction on the depth l of the subtree Tv. The basis case is l = 0. Then, the
tree consists of v only. The only possible states |ψ⟩are multiples of |v⟩. The root is also the
only leaf, carrying a variable xi and Tv(xi) = xi. If xi = 0, then Sx,1 is empty, meaning that
Lv(ψ) = 1. If xi = 1, then Sx,1 consists of all multiples of |r⟩, meaning that PSx,1|ψ⟩= |ψ⟩and
Lv(ψ) = −(K −1). In both cases, the lemma is true.
For the inductive case, let z1 and z2 be the children of v, y1 and y2 be the children of z1 and
y3, y4 be the children of z2. We can decompose the state |ψ⟩as
|ψ⟩= αv|v⟩+ |ψ1⟩+ |ψ2⟩
(10)
where |ψi⟩is a superposition over |u⟩, u ∈Tzi. We claim
Claim 3 For every i ∈{1, 2}, there exists |ψ′
i⟩∈S′
zi,0, such that, for the state |ψ′′
i ⟩= |ψi⟩+|ψ′
i⟩,
we have
1. If Tz1(x1, . . . , xN) = 0, then
∥ψ′′
i ∥2 −∥Px,1|ψ′′
i ⟩∥2 ≤−byi
√
2 |Hvyiαv|2.
(11)
2. If Tz1(x1, . . . , xN) = 1, then
∥ψ′′
i ∥2 −∥Px,1|ψ′′
i ⟩∥2 ≤ayi
√
2
|Hvyiαv|2.
(12)
Proof: For typographical convenience, let i = 1. By Lemma 11, the amplitude of z1 in |ψ1⟩is
0. Therefore, we can decompose
|ψ1⟩= |ϕ1⟩+ |ϕ2⟩,
with |ϕi⟩being a superposition over Tyi.
For the ﬁrst part, Tz1 = 0 if and only if Ty1 = Ty2 = 1. By the inductive assumption, there
exist states |ϕ′
1⟩∈S′
y1,0, |ϕ′
2⟩∈∈S′
y2,0 such that, for the states |ϕ′′
i ⟩= |ϕi⟩+ |ϕ′
i⟩, we have
∥ϕ′′
i ∥2 −∥PSx,1|ϕ′′
i ⟩∥2 ≤−byi|αyi|2,
(13)
17


---- page 18 ----

with αyi being the amplitude of yi in |ϕi⟩(which is the same as its amplitude in |ψ1⟩). We
deﬁne |ψ′
1⟩= |ϕ′
1⟩+ |ϕ′
2⟩and |ψ′′
1⟩= |ψ1⟩+ |ψ′
1⟩. By summing equations (13) for i = 1 and
i = 2, we get
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤−
2
X
i=1
byi|αyi|2.
(14)
We would like to upperbound the right-hand side of this equation. From H|ψ⟩= 0, we have
Hy1z1αy1 + Hy2z1αy2 + Hvz1αv = 0.
(15)
Deﬁne xi = −
Hyiz1αyi
Hvz1 αv . Then, by dividing both sides of (15) by −Hvz1αv, we have x1 + x2 = 1.
By expressing αyi in terms of xi, we get
−
2
X
i=1
byi|αyi|2 = −|Hvz1αv|2
2
X
i=1
byi
H2yiz1
|xi|2
≤−|Hvz1αv|2(1 −δz1)
2
X
i=1
K√mz1
√
2myi
|xi|2,
where the last inequality follows by writing out byi and Hyiz1 and applying δyi ≤δz1 (which is
true because both the size and the depth of Tyi are less than the size and the depth of Tz1). To
complete the proof, it suﬃces to show that
|x1|2
my1
+ |x2|2
my2
≥
1
mz1
,
(16)
subject to the constraint x1 + x2 = 1. The left hand side of (16) is minimized when x1 and x2
are both real. (Otherwise, one can replace x1 and x2 by x′
1 =
|x1|
|x1|+|x2| and x′
2 =
|x2|
|x1|+|x2| and
this does not increase the left hand side.) Therefore, we can ﬁnd the minimum of the left hand
side of (16) by substituting x2 = 1 −x1 and taking the derivative of the left hand side. That
shows that the left hand side is minimized by x1 =
my1
my1 +my2 , x2 =
my2
my1 +my2 . Then, it is equal
to
1
my1 +my2 =
1
mz1 .
For the second part, we consider two cases:
1. y1 = y2 = 0.
Let C1, C2 be extended minimal certiﬁcates for Ty1 = 0 and Ty2 = 0, respectively and
γ =
αy2 −αy1
4√my1 + 4√my2 . We deﬁne
| ˜ϕ1⟩= |ϕ1⟩+ γ 4√my1|ψC1⟩.
We deﬁne | ˜ϕ2⟩similarly, with - sign in the front of √my2|ψC2⟩. We then apply the inductive
assumption to the states | ˜ϕi⟩, obtaining |ϕ′
1⟩, |ϕ′
2⟩such that for |ϕ′′
i ⟩= | ˜ϕi⟩+|ϕ′
i⟩, we have
∥ϕ′′
i ∥2 −∥PSx,1|ϕ′′
i ⟩∥2 ≤ayi|βyi|2,
(17)
where βyi is the amplitude of yi in | ˜ϕi⟩. We deﬁne
|ψ′
1⟩= |ϕ′
1⟩+ |ϕ′
2⟩+ γ|ψC1,C2⟩
and let |ψ′′
1⟩= |ψ1⟩+ |ψ′
1⟩. Then, by summing equations (17), we get
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤ay1|βy1|2 + ay2|βy2|2.
(18)
18


---- page 19 ----

By our choice, we have βy1 = βy2. Since H|ψ⟩= 0 and H|ψ′⟩= 0, we have H|ψ′′⟩= 0.
By writing out the amplitude of |z1⟩in H|ψ′′⟩, we get
Hy1z1βy1 + Hy2z1βy2 + Hz1vαv = 0.
Therefore,
βy1 = βy2 = −
Hz1vαv
Hy1z1 + Hy2z1
.
By substituting that into (18), we get
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤
ay1 + ay2
(Hy1z1 + Hy2z1)2 |Hz1vαv|2.
We now expand the coeﬃcient of |Hz1vαv|2:
ay1 + ay2
(Hy1z1 + Hy2z1)2 ≤2(1 + δz1)
p
dy1my1 +
p
dy2my2

4√
2my1
4√mz1 +
4√
2my2
4√mz1
2
≤
1
√
22(1 + δz1)
p
dz1mz1
√my1 + √my2
( 4√my1 +
4√my2)2
≤
1
√
2
2(1 + δz1)
p
dz1mz1.
2. one of y1, y2 is 0 and the other is 1.
For typographical convenience, assume that y1 = 0, y2 = 1. By the inductive assumption,
there exist states |ϕ′
1⟩, |ϕ′
2⟩∈SH,0 such that, for the states |ϕ′′
i ⟩= |ϕi⟩+ |ϕ′
i⟩, we have
∥ϕ′′
i ∥2 −∥PSx,1|ϕ′′
i ⟩∥2 ≤c|αyi|2,
(19)
with c = ay1 for i = 1 and c = −by2 for i = 2.
We deﬁne |ψ′
1⟩= |ϕ′
1⟩+ |ϕ′
2⟩and
|ψ′′
1 ⟩= |ψ1⟩+ |ψ′
1⟩. By summing the equations (19), we get
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤ay1|αy1|2 −by2|αy2|2.
(20)
We switch to variables xi = −
Hyiz1αyi
Hvz1 αv , obtaining
∥ψ′′
1∥2 −∥PSx,1|ψ′′
1⟩∥2 ≤|Hvz1αv|2
 ay1
H2y1z1
|x1|2 −
by2
H2y2z1
|x2|2

.
Substituting the expressions for ay1, by2, Hy1z1, Hy2z1 gives
ay1
H2y1z1
|x1|2 −
by2
H2y2z1
|x2|2
=
1
√
2

(1 + δy1)2
p
dy1mz1|x1|2 −(1 −δy2)K√mz1
my2
|x2|2

≤
1
√
22(1 + δy1)
p
dy1mz1
 
|x1|2 −
K
3
p
dy1my2
|x2|2
!
,
(21)
with the second inequality following by rearranging terms and applying 1 −δy2 ≥4
5 ≥
4
6(1 + δy1) which is true because of δy1 ≤1
5 and δy2 ≤1
5.
19


---- page 20 ----

Let δ = |x2|. Then |x1| ≤1 + δ and the right hand side of (21) is at most
1
√
22(1 + δy1)
p
dy1mz1
 
(1 + δ)2 −
K
3
p
dy1my2
δ2
!
.
Taking the derivative w.r.t. δ shows that the expression in the brackets is maximized by
δ =
3
p
dy1my2
K −3
p
dy1my2
,
in which case it is equal to
K
K−3√
dy1 my2 . To complete the proof, we observe that
(1 + δy1)
K
K −3
p
dy1my2
= 1 + δy1 + (1 + δy1)3
p
dy1my2
K −3
p
dy1my2
≤1 + δy1 + 4
p
dy1my2
K
< 1 + δy1 + 4
p
dz1my2
K
< 1 + δz1,
with the ﬁrst inequality following from δy1 < 1
5 and K −3
p
dy2my2 ≥K −3N
√
d ≤27
30K.
To deduce lemma 12 from claim 3, we deﬁne
|ψ′⟩= |ψ′
1⟩+ |ψ′
2⟩.
Because of equation (10), we can also express |ψ′′⟩= |ψ⟩+ |ψ′⟩as
|ψ′′⟩= αv|v⟩+ |ψ′′
1 ⟩+ |ψ′′
2 ⟩.
If Tr = 0, then Tz1 = Tz2 = 1. By summing up eq. (12) for i = 1, 2 and adding |αv|2 to both
sides, we get
∥ψ′′∥2 −∥Px,1|ψ′′⟩∥2 ≤
az1
√
2H2
vz1 + az2
√
2H2
vz2 + 1

|αv|2.
(22)
By expanding azi and Hvzi, we get
az1
√
2H2
vz1 + az2
√
2H2
vz2 + 1 ≤(1 + δv)
 
mz1
p
dz1
√mv
+ mz2
p
dz2
√mv
+ 1
!
.
Since mv = mz1 +mz2, we have
mz1
√mv +
mz2
√mv =
mv
√mv = √mv. Together with dv = max(dz1, dz2)+
1, this implies
mz1
p
dz1
√mv
+ mz2
p
dz2
√mv
+ 1 ≤
p
mv(dv −1) + 1
≤
p
mv(dv −1) +
√mv
√dv
= √mv
2
p
dv(dv −1) + 1
√dv
≤√mv
2dv
√dv
= 2
p
mvdv,
with the second inequality following from dv ≤mv (the depth of any tree is at most the number
of leaves in it) and the last inequality following from
p
dv(dv −1) ≤dv −1
2.
If Tr = 1, then we again have two cases:
20


---- page 21 ----

1. Tz1 = Tz2 = 1.
By summing up eq. (11) for i = 1, 2 and adding |αv|2 to both sides, we get
∥ψ′′∥2 −∥Px,1|ψ′′⟩∥2 ≤−
 bz1
√
2H2
vz1 + bz2
√
2H2
vz2 −1

|αv|2.
By expanding bzi and Hvzi and simplifying, we get
bz1
√
2H2
vz1 + bz2
√
2H2
vz2 −1 ≥(1 −δz1) K
√mv
+ (1 −δz2) K
√mv
−1
≥2(1 −δv) K
√mv
−1 > (1 −δv) K
√mv
.
2. one of z1, z2 is 0 and the other is 1.
For typographical convenience, assume that z1 = 0, z2 = 1. In this case, claim 3 gives us
∥ψ′′∥2 −∥Px,1|ψ′′⟩∥2 ≤

−bz1
√
2H2
vz1 + az2
√
2H2
vz2 + 1

|αr|2.
We have
−bz1
√
2H2
vz1 + az2
√
2H2
vz2 + 1 ≤−(1 −δz1) K
√mv
+ 2(1 + δz2)mz2
p
dz2
√mv
+ 1.
To prove that this is at most −bv, we need to show that
2(1 + δz2)mz2
p
dz2
√mv
+ 1 ≤(δv −δz1) K
√mv
.
(23)
This follows from
(δv −δz1) K
√mv
=
 
5mv
√dv
K
+ dv
√
K
−5mz1
p
dz1
K
−dz1
√
K
!
K
√mv
≥
5mz2
√dv
K
+
1
√
K

K
√mv
≥5mz2
p
dz2
√mv
+
√
K
√mv
≥2(1 + δz2)mz2
p
dz2
√mv
+ 1.
The ﬁrst equality follows by writing out δv and δz1, the next inequality follows from mv =
mz1 + mz2 and dv > dz1 and the last inequality follows from δz2 < 1
5 and mv ≤N ≤K
30.
This completes the proof of Lemma 12.
The general case of Lemma 9 now follows from Lemma 12 in the same way as the balanced
case of Lemma 9 followed from Lemma 10.
Distinction between balanced and general case. There are two reasons why our bound
for the general case has O(
√
Nd) instead of O(
√
N) for the balanced case:
1. z1 = 0, z2 = 1 case of the proof of Lemma 12 which requires having √dvmv instead of
√mv. (The rest of the proof of Lemma 12 would still work with √mv.)
2. For the T = 0 case, lemma 3 has O(√mvdv) in the general case and O(√mv) in the
balanced case.
21

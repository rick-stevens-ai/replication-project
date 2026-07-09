# 0708.2584 -- surrogate Marker (PyMuPDF fitz v1.27.2.3). Marker not installed 2026-07-05.

---- page 1 ----
arXiv:0708.2584v2  [quant-ph]  3 Mar 2008
Claw Finding Algorithms Using Quantum Walk
Seiichiro Tani∗
Quantum Computation and Information Project, ERATO-SORST, JST.
NTT Communication Science Laboratories, NTT Corporation.
Abstract
The claw ﬁnding problem has been studied in terms of query complexity as one of the problems closely
connected to cryptography. For given two functions, f and g, as an oracle which have domains of size N
and M (N ≤M), respectively, and the same range, the goal of the problem is to ﬁnd x and y such that
f(x) = g(y). This problem has been considered in both quantum and classical settings in terms of query
complexity. This paper describes an optimal algorithm using quantum walk that solves this problem. Our
algorithm can be slightly modiﬁed to solve a more general problem of ﬁnding a tuple consisting of elements
in the two function domains that has prespeciﬁed property. Our algorithm can also be generalized to ﬁnd a
claw of k functions for any constant integer k > 1, where the domains of the functions may have diﬀerent
size. Keywords: quantum computing, query complexity, oracle computation
1
Introduction
The most signiﬁcant discovery in quantum computation would be Shor’s polynomial-time quantum algorithms
for factoring integers and computing discrete logarithms [15], both of which are believed to be hard to solve
in classical settings and are thus used in arguments for the security of the widely used cryptosystems. Another
signiﬁcant discovery is Grover’s quantum algorithm for the problem of searching an unstructured set [11], i.e,
the problem of searching for i ∈{0, 1, . . . , N −1} such that f(i) = 1 for a hidden Boolean function f; it has
yielded a variety of generalizations [4, 12, 2, 16, 13]. Grover’s algorithm and its generalizations assume the
oracle computation model, in which a problem instance is given as a black box (called an oracle) and any
algorithm needs to make queries to the black box to get suﬃcient information on the instance. In the case of
searching an unstructured set, any algorithm needs to make queries of the form “what is the value of function
f for input i ?” to the given oracle. In the oracle computation model, the eﬃciency of an algorithm is usually
measured by the number of queries the algorithm needs to make, i.e., the query complexity of the algorithm.
The query complexity of a problem means the query complexity of the algorithm that solves the problem with
fewest queries.
One of the earliest applications of Grover’s algorithm was the bounded-error algorithm of Brassard, Høyer
and Tapp [5]; it addressed the collision problem in a cryptographic context, i.e., ﬁnding pair (x, y) such that
f(x) = f(y), in a given 2-to-1 function f of domain size N. Their quantum algorithm requires O(N1/3) queries,
whereas any bounded-error classical algorithm needs Θ(N1/2) queries. Subsequently, Aaronson and Shi [1]
proved the matching lower bound. Brassard et al. [5] considered two more related problems: the element
distinctness problem and the claw ﬁnding problem. These problems are also important in a cryptographic sense.
Furthermore, studying these problems has deepened our understanding of the power of quantum computation.
The element distinctness problem is to decide whether or not N integers given as an oracle are all distinct.
Buhrman et al. [8] gave a bounded-error algorithm for the problem, which makes O(N3/4) queries (strictly
∗tani@theory.brl.ntt.co.jp
1

---- page 2 ----
speaking, they assumed a comparison oracle, which returns just the result of comparing function values for two
speciﬁed inputs, and, in this case, the query complexity is O(N3/4 log N)). Subsequently, Ambainis [2] gave an
improved upper bound O(N2/3) by introducing a new framework of quantum walk (his quantum walk algorithm
was reviewed from a slightly more general point of view in [14, 10], and a much more general framework was
given by Szegedy [16]). This upper bound matches the lower bound proved by Aaronson and Shi [1].
The claw ﬁnding problem is deﬁned as follows. Given two functions f : X →Z and g : Y →Z as an oracle,
decide whether or not there exists at least one pair (x, y) ∈X × Y, called a claw, such that f(x) = g(y), and ﬁnd
a claw if it exists, where X and Y are domains of size N and M (N ≤M), respectively. By clawﬁnding(N, M), we
mean this problem.
After Brassard et al. [5] considered a special case of the claw ﬁnding problem, Buhrman et al. [7] gave
a quantum algorithm that requires O(N1/2M1/4) queries for N ≤M < N2 and O(M1/2) queries for M ≥N2
(strictly speaking, they assumed a comparison oracle, and, in this case, the query complexity is multiplied by
log N). They also proved that any algorithm requires Ω(M1/2) queries by reducing the search problem over an
unstructured set to the claw ﬁnding problem. Thus, while their bounds of the query complexity are tight when
M ≥N2, there is still a big gap when N ≤M < N2. Furthermore, they considered the case of k functions,
i.e., the k-claw ﬁnding problem deﬁned as follows: given k functions fi : Xi := {1, . . . , Ni} →Z (i ∈{1, . . . , k})
as an oracle, where k > 1 is any constant integer, and Ni ≤N j if i < j, decide whether or not there exists
at least one k-claw, i.e., a tuple (x1, . . . , xk) ∈X1 × · · · × Xk such that fi(xi) = fj(xj) for any i, j ∈{1, . . . , k},
and ﬁnd a k-claw if it exists. A generalization of their algorithm works well for the k-claw ﬁnding problem;
its query complexity is O(N1−1/2k) if Ni = N for all i ∈{1, . . . , k}. It is shown in [14] that the quantum-walk
algorithm in [2] for the element distinctness problem is general enought to be applied with slight modiﬁcation
to the k-claw ﬁnding problem; this yields query complexity O((Pk
i=1 Ni)
k
k+1 ) if the promise is assumed that
there is at most one solution, and, with random reduction, query complexity ˜O((Pk
i=1 Ni)
k
k+1 ) for the problem
without the single-solution promise. Zhang [17] generalized the quantum-walk algorithm in [2] to solve the
claw ﬁnding problem with the single-solution promise by making O((NM)1/3) queries for N ≤M < N2 and
O(M1/2) for M ≥N2. This upper bound is optimal, since the matching lower bound Ω((NM)1/3) was proved in
the paper by reducing the collision problem to the claw ﬁnding problem. Zhang also showed that the algorithm
can be generalized to solve a more general problem of ﬁnding a tuple consisting of elements in the domains of
given k functions with the single-solution promise. To solve the problems without the promise, we usually use
a randomly reduction to the problem with the single-solution promise, which is known to increase the query
complexity by at most a log factor as pointed out in [14] (if the problem has certain robust properties, there is
a random reduction that increases the query complexity by a constant multiplicative factor, e.g., [2].)
This paper gives an optimal quantum algorithm that directly (i.e., without using such a random reduction)
solves the claw ﬁnding problem without the single-solution promise. The query complexity of our algorithm is
as follows:
Q(clawﬁnding(N, M)) =

O

(NM)1/3
(N ≤M < N2)
O

M1/2
(M ≥N2),
where Q(P) means the number of queries required to solve problem P with one-sided bounded error (i.e.,
with the one-sided error probability bounded by a certain constant, say, 1/3).
The optimality is guaran-
teed by the lower bounds given in [7, 17]. Our algorithm can be modiﬁed to solve a more general prob-
lem of ﬁnding a tuple (x1, . . . , xp, y1, . . . , yq) ∈Xp × Yq such that xi , xj and yi , yj for any i ,
j,
and ( f(x1), . . . , f(xp), g(y1), . . . , g(yq)) ∈R, for given R ⊆Z p+q, where p and q are positive constant inte-
gers. We call this problem (p, q)-subset ﬁnding problem and denote it by (p, q) −subsetﬁnding(N, M)). Thus,
clawﬁnding(N, M) is a special case of (p, q)−subsetﬁnding(N, M)) with p = q = 1 and equality relation R. The
query complexity is
Q((p, q)−subsetﬁnding(N, M)) =

O((N pMq)1/(p+q+1))
N ≤M < N1+1/q
O(Mq/(1+q))
M ≥N1+1/q.

---- page 3 ----
Our claw ﬁnding algorithm ﬁrst ﬁnds subsets ˜X ⊆X and ˜Y ⊆Y of size O(1) such that there is a claw in ˜X × ˜Y,
by using binary and 4-ary searches over X and Y; in order to decide which branch we should proceed at each
visited node in the search trees, we use a subroutine that decides, with one-sided bounded error, whether or not
there exists a claw of two functions f and g. The algorithm then searches ˜X × ˜Y for a claw by making classical
queries. If we na¨ıvely repeated the bounded-error subroutine O(log M) times at each visited node to guarantee
bounded error as a whole, a “log” factor would be multiplied to the total query complexity. Instead, at the
node of depth s in the search trees, we repeat the subroutine O(s) times to amplify success probability. This
achieves bounded error as a whole, while pushing up the query complexity by just a constant multiplicative
factor. This binary search technique can be used to solve other problems such as the search version of the
element distinctness problem, with the quantum walk algorithm for the problems in [16]. (Høyer et al. [12]
introduced an error reduction technique with a similar ﬂavor; however, their technique is used in an algorithmic
context diﬀerent from ours: their error reduction is performed at each recursion level while ours is sequentially
used at each step of the search tree.)
The subroutine is developed around the Szegedy’s quantum walk framework [16] over a Markov chain on
the graph categorical product of two Johnson graphs, which correspond to the two functions (with an idea
similar to the one used in [9]). The Johnson graph J(n, k) is a connected regular graph with
n
k

vertices
such that every vertex is a subset of size k of [n]; two vertices are adjacent if and only if the symmetric
diﬀerence of their corresponding subsets has size 2. For two functions f and g with domains X and Y such
that |X| ≤|Y|, the subroutine applies Szegedy’s quantum walk to the graph categorical product of two Johnson
graphs Jf = J(|X|, (|X||Y|)1/3) and Jg = J(|Y|, (|X||Y|)1/3) if |Y| ≤|X|2, and Jf = J(|X|, |X|) and Jg = J(|Y|, |X|)
otherwise.
Our algorithm can be generalized to the k-claw ﬁnding problem.
For the k-claw ﬁnding problem
k-clawﬁnding(N1, . . . , Nk) against the k functions with domain sizes Ni (i = 1, . . . , k), repectively,
Q(k-clawﬁnding(N1, . . . , Nk)) =

O
 Qk
i=1 Ni
 1
k+1
!
if Qk
i=2 Ni = O(Nk
1),
O
 qQk
i=2 Ni/Nk−2
1

otherwise.
Our algorithms can work with slight modiﬁcation even against a comparison oracle (i.e., against an oracle
that, for a given pair of inputs (xi, xj) ∈Xi × X j, only decides which is the larger of two function values fi(xi)
and fj(xj)); the query complexity increases by a multiplicative factor of log N1 for the k-function case (log N
for the two-function case).
Related works
Recently, Magniez et al. [13] developed a new quantum walk over a Markov chain. One of the advantages
of their quantum walk over Szegedy’s quantum walk is that their quantum walk can ﬁnd a marked vertex if
there is at least one marked vertex, which would simplify our algorithm. Interestingly, our algorithm shows
Szegedy’s quantum walk together with carefully adjusted binary search can ﬁnd a solution in some interesting
problems such as the claw ﬁnding problem and the element distinctness problem with the same order of query
complexity.
2
Preliminaries
This section deﬁnes problems and introduces some useful techniques. We denote the set of positive integers by
Z∗, the set of {i | j ≤i ≤k for i, j, k ∈Z∗} by [ j.k], and [1.k] by [k] for short.
Problem 1 (Claw Finding Problem) Given two functions f : X := [N] →Z and g : Y := [M] →Z as an
oracle for N ≤M, where Z = [|Z|], ﬁnd a pair (x, y) ∈X × Y such that f(x) = g(y) if such a pair exists.

---- page 4 ----
Actually, Z is allowed to be any totally ordered set, but we adopt the above deﬁnition for simplicity.
In a quantum setting, the two functions are given as quantum oracle O f,g which is deﬁned as O f,g :
|p, z, w⟩−→|p, z ⊕P(p) (mod |Z|), w⟩, where p ∈X ∪Y, z ∈Z, w is work space, P(p) is deﬁned as f(p)
if p ∈X and g(p) if p ∈Y (note that it easy to know whether p is in X or Y by using one more bit to represent
p). This kind of oracle, which returns the value of the function(s), is called a standard oracle.
Another type of oracle is called the comparison oracle, which, for given two inputs, only decides which
is the larger of the two function values corresponding to the inputs. More formally, comparison oracle O f,g is
deﬁned as O f,g : |p, q, b, w⟩−→|p, q, b ⊕[P(p) ≤Q(q)], w⟩, where p, q ∈X ∪Y, b ∈{0, 1}, w and P are deﬁned
as in the standard oracle, Q is deﬁned in the same way as P, and [P(p) ≤Q(q)] is the predicate such that its
value is 1 if and only if P(p) ≤Q(q).
It is obvious that, if we are given a standard oracle, we can realize a comparison oracle by issuing O(1)
queries to the standard oracle. Thus, upper bounds for a comparison oracle are those for a standard oracle,
and lower bounds for a standard oracle are those for a comparison oracle, if we ignore constant multiplicative
factors.
Buhrman et al. [7] generalized the claw ﬁnding problem to a k-function case.
Problem 2 (k-Claw Finding Problem) Given k functions fi : Xi := [Ni] →Z (i ∈[k]) as an oracle, where
Ni ≤N j if i < j, and Z := [|Z|], ﬁnd a k-claw, i.e., a k-tuple (x1, . . . , xk) ∈X1 × · · · × Xk such that fi(xi) = fj(xj)
for any i, j ∈[k], if it exists.
Standard and comparison oracles are deﬁned in almost the same way as in the two-function case, except that
inputs p and q belong to one of Xi’s, respectively, for i ∈[k].
The next theorem describes Szegedy’s framework, which we use to prove our upper bounds.
Theorem 1 ([16]) Let M be a symmetric Markov chain with state set V and transition matrix P and let δM
be the spectral gap of P, i.e., 1 −maxi |λi| for the eigenvalues λi’s of P. For a certain subset V′ ⊆V with the
promise that |V′| is either 0 or at least ǫ|V| for 0 < ǫ < 1, any element in V′ is marked. For T = O(1/ √ǫδM),
the next quantum algorithm decides whether |V′| is 0 (“false”) or at least ǫ|V| (“true”) with one-sided bounded
error with cost O(CU + (CF + CW)/ √δMǫ), where C = P
i |ci⟩⟨ci| for |ci⟩= P
j
pPi, j|i⟩| j⟩and R = P
j |rj⟩⟨rj|
for |rj⟩= P
i
pP j,i|i⟩| j⟩:
1. Prepare |0⟩in a one-qubit register R0, and prepare a uniform superposition |φ0⟩:=
1
√r|V|
P
i, j∈V,Pi,j,0 |i⟩| j⟩
in a register R1 with cost at most CU, where r is the number of adjacent states (of any state) in M.
2. Apply the Hadamard operator to R0.
3. For randomly and uniformly chosen 1 ≤t ≤T, apply the next operation W t times to R1 if the content of
R0 is “1.”
3.1 To any |i⟩| j⟩, perform the next steps: (i) Check if i ∈V′ with cost at most CF, (ii) If i < V′, apply
diﬀusion operator 2C −I with cost at most CW.
3.2 To any |i⟩| j⟩, perform the next steps: (i) Check if j ∈V′ with cost at most CF, (ii) If j < V′, apply
diﬀusion operator 2R −I with cost at most CW.
4. Apply the Hadamard operator to R0, and measure registers R0 and R1 with respect to the computational
basis.
5. If the result of measuring R0 is 1 or a marked element is found by measuring R1, output “true”; otherwise
output “false.”
3
Claw Detection
In this section, we describe “claw-detection” algorithms that detect the existence of a claw. The claw-detection
algorithms will be used as subroutines in the “claw-search” algorithms presented in the next section that ﬁnd a

---- page 5 ----
claw.
Before presenting the claw-detection algorithm, we introduce some notions. The Johnson graph J(n, k) is
a connected regular graph with
n
k

vertices such that every vertex is a subset of size k of [n]; two vertices are
adjacent if and only if the symmetric diﬀerence of their corresponding subsets has size 2. The graph categorical
product G = (VG, EG) of two graphs G1 = (VG1, EG1) and G2 = (VG2, EG2), denoted by G = G1 × G2, is a graph
having vertex set VG = VG1×VG2 such that ((v1, v2), (v′
1, v′
2)) ∈EG if and only if (v1, v′
1) ∈EG1 and (v2, v′
2) ∈EG2.
The next two propositions are useful in analyzing the claw-detection algorithms we will describe.
Proposition 2 For Markov chains M, M1, . . . , Mk, the spectral gap δ of M is the minimum of those δ1, . . . , δk
of M1, . . . , Mk, i.e., δ = mini{δi}, if the underlying graph of M is the graph categorical product of those of
M1, . . . , Mk.
The eigenvalues of the Markov chain on J(n, k) are (k−j)(n−k−j)−j
k(n−k)
for j ∈[0.k] [6, pages 255–256], from which
the next proposition follows.
Proposition 3 The Markov chain on Johnson graph J(n, k) has spectral gap δ = Ω(1
k), if 2 ≤k ≤n/2.
We will ﬁrst describe a claw-detection algorithm against a comparison oracle, from which we can almost
trivially obtain a claw-detection algorithm against a standard oracle. Let Claw Detect denote the algorithm.
To construct Claw Detect, we apply Theorem 1 on the graph categorical product of two Johnson graphs Jf =
J(|X|, l) and Jg = J(|Y|, m) for the domains X and Y of functions f and g, respectively, where l and m (l ≤m)
are integers ﬁxed later.
More precisely, let F and G be any vertices of Jf and Jg, respectively, i.e., any l-element subset and m-
element subset of X and Y, respectively. Then (F,G) is a vertex in Jf × Jg. Similarly, for any edges (F, F′) and
(G,G′) of Jf and Jg, respectively, ((F,G), (F′,G′)) is an edge connecting two vertices (F,G) and (F′,G′) in
Jf × Jg. We next deﬁne “marked vertices” as follows. Vertex (F,G) is marked if there is a pair of (x, y) ∈F ×G
such that f(x) = g(y). To check if (F,G) is marked or not, we just sort all elements in F ∪G on their function
values. Although we have to sort all elements in the initial vertex, we have only to change a small part of
the sorted list we have already had when moving to an adjacent vertex. For every vertex (F,G), we maintain a
representation LF,G of the sorted list of all elements in F∪G on their function values, and we identify (F,G, LF,G)
as a vertex of Jf × Jg. Here, we want to guarantee that LF,G is uniquely determined for any pair (F,G) in order
to avoid undesirable quantum interference; we have just to introduce some appropriate rules that break ties, i.e.,
the situation where there are multiple elements in F ∪G that have the same function value.
As the state |φ0⟩in Theorem 1, we prepare
|φ0⟩=
1
qN
l
M
m

l(N −l)m(M −m)
O
|F△F′|=|G△G′|=2
F,F′⊆X,|F|=|F′|=l
G,G′⊆Y,|G|=|G′|=m
|F,G, LF,G⟩|F′,G′, LF′,G′⟩,
in register R1. The number 1 ≤t ≤
c
√
δǫ of repeating W is chosen randomly and uniformly for some constant c,
δ := Ω(1/m) and ǫ := lm/(NM).
We next describe the implementation of operation W. Since diﬀusion operator 2C −I depends on LF,G’s,
it cannot be performed without queries to the oracle. We thus divide operator 2C −I into a few steps. For
every unmarked vertex (F,G, LF,G), we ﬁrst transform |F,G, LF,G⟩|F′,G′, LF′,G′⟩into |F,G, LF,G⟩|F′,G′, LF,G⟩
with queries to the oracle. We then perform a diﬀusion operator on the registers where the contents “F,G”
and “F′,G′” are stored, to obtain a superposition of |F,G, LF,G⟩|F′′,G′′, LF,G⟩over all (F′′,G′′) adjacent to
(F,G). Finally, we transform |F,G, LF,G⟩|F′′,G′′, LF,G⟩into |F,G, LF,G⟩|F′′,G′′, LF′′,G′′⟩. Operator 2R −I can
be implemented in a similar way.

---- page 6 ----
Lemma 4 Let Q2(clawdetect(N, M)) be the number of queries needed to decide whether there is a claw or not
for functions f : X := [N] →Z and g : Y := [M] →Z given as a comparison oracle. Then,
Q2(clawdetect(N, M)) =

O((NM)1/3 log N)
(N ≤M < N2)
O(M1/2 log N)
(M ≥N2).
Proof We will estimate CU, CF and CW for Claw Detect, and then apply Theorem 1.
To generate |φ0⟩, we ﬁrst prepare the uniform superposition of |F,G⟩|F′,G′⟩over all F, F′,G,G′ such
that (F, F′) and (G,G′) are edges of Jf and Jg, respectively. Obviously, this requires no queries. We then
compute LF,G and LF′,G′ for each basis state by issuing O((l + m) log(l + m)) queries to oracle O f,g. Thus,
CU = O((l + m) log(l + m)).
We can check if there is a pair of (x, y) ∈F × G such that f(x) = g(y) by looking through LF,G (without any
queries). Thus, CF = 0.
For every unmarked (F,G, LF,G), step (a).ii of operation W transforms |F,G, LF,G⟩|F′,G′, LF′,G′⟩into a su-
perposition over all |F,G, LF,G⟩|F′′,G′′, LF′′,G′′⟩such that |F△F′′| = |G△G′′| = 2. This is realized by insertion
and deletion of O(1) elements to/from the sorted list of O(l + m) elements, and diﬀusion operators without
queries. Each insertion or deletion can be performed with O(log(l + m)) queries by using binary search. Simi-
larly, step (b).ii of operation W needs O(log(l + m)) queries. Thus, we have CW = O(log(l + m)).
We set ǫ to
l
N × m
M, since the probability that a state is marked is minimized when only one claw exists
for f and g, in which case the probability is
l
N × m
M. Since, from Proposition 3, the spectral gaps of the
Markov chains on J(N, l) and J(M, m) are Ω(1
l ) and Ω( 1
m), respectively, the spectral gap of the Markov chain
on J(N, l) × J(M, m) is Ω(min{ 1
l , 1
m}) = Ω( 1
m) due to l ≤m and Proposition 2.
From Theorem 1, the total number of queries is Q2(clawdetect(N, M)) = O((l + m) log(l + m) + log(l +
m) √m(NM/(lm))) = O((l + m) log(l + m) + √NM/l log(l + m)).
When N ≤M < N2, we set l = m = Θ((NM)1/3), which satisﬁes condition l ≤N. The total number
of queries is Q2(clawdetect(N, M)) = O((NM)1/3 log N). When M ≥N2, we set l = m = N, implying that
Q2(clawdetect(N, M)) = O(M1/2 log N). □
□
The standard oracle case can be handled by using almost the same approach.
Corollary 5 Let Q2(clawdetect(N, M)) be the number of queries needed to decide whether there is a claw or not
for functions f : X = [N] →Z and g : Y = [M] →Z given as a standard oracle. Then,
Q2(clawdetect(N, M)) =

O((NM)1/3)
(N ≤M < N2)
O(M1/2)
(M > N2).
The claw-detection algorithm against a standard oracle can easily be modiﬁed in order to solve the more general
problem of detecting a tuple (x1, . . . , xp, y1, . . . , yq) ∈Xp × Yq such that xi , xj and yi , yj for any i , j, and
( f(x1), . . . , f(xp), g(y1), . . . , g(yq)) ∈R, for given R ⊆Z p+q, where p and q are any constant positive integers.
A modiﬁcation is made to the part of the algorithm that decides whether a vertex of the underlying graph is
marked or not; the modiﬁcation can be made without changing the number of queries. The query complexity
can be analyzed by using almost the same approach as used in claw detection with ǫ =
N−p
l−p

/
N
l

×
M−q
m−q

/
M
m

≥
lpmq(1 −o(1))/(N pMq); the query complexity is O((N pMq)1/(p+q+1)) for N ≤M < N1+1/q and O(Mq/(1+q)) for
M ≥N1+1/q. The problem of ﬁnding such a tuple can also be solved with the same order of complexity as
above by using the algorithm for detecting it as a subroutine.
Our algorithm for detecting a claw can easily be generalized to the case of k functions of domains of size
N1, . . . , Nk, respectively. More concretely, we apply Theorem 1 to the Markov chain on the graph categorical

---- page 7 ----
product of the k Johnson graphs, each of which corresponds to one of the k functions. We denote this “k-claw
detection” algorithm by k-Claw Detect in the next section.
Lemma 6 For any positive integer k > 1, let Q2(k-clawdetect(N1, . . . , Nk)) be the number of queries needed to
decide whether there is a k-claw or not for functions fi : Xi := [Ni] →Z (i ∈[k]) given as a comparison oracle,
where Ni ≤N j if i < j. If k is constant,
Q2(k-clawdetect(N1, . . . , Nk)) =

O
 Qk
i=1 Ni
 1
k+1 log N1
!
if Qk
i=2 Ni = O(Nk
1),
O
 qQk
i=2 Ni/Nk−2
1
log N1

otherwise.
Proof (Sketch).
In a way similar to the case of two functions, we apply Theorem 1 on the graph categorical
product of k Johnson graphs Jfi := J(|Xi|, li) (i ∈[k]) for the domains Xi’s of functions fi’s, where li’s are
integers ﬁxed later such that li ≤lj for i < j.
To generate |φ0⟩, we ﬁrst prepare the uniform superposition of |F1, . . . , Fk⟩|F′
1, . . . , F′
k⟩over all Fi and F′
i
such that (Fi, F′
i) is an edge of Jfi for every i. This requires no queries. As in the case of two functions, deﬁne
LF1,...,Fk for any F1, . . . , Fk as a representation of the sorted list of all elements in Sk
i=1 Fi so that it can be
uniquely determined for each tuple (F1, . . . , Fk). We then compute LF1,...,Fk and LF′
1,...,F′
k for each basis state by
issuing O  (l1 + · · · + lk) log(l1 + · · · + lk) queries to the oracle. Thus, CU = O  (l1 + · · · + lk) log(l1 + · · · + lk).
CF and CW can be estimated as 0 and O  log(l1 + · · · + lk), respectively, in a way similar to the case of two
functions. We set ǫ to Qk
i=1 li/Ni and δ to mini{1/li} = 1/lk.
When Qk
i=2 Ni = O(Nk
1), we set li := Θ
 Qk
i=1 Ni
 1
k+1
!
for every i ∈[k], which satisﬁes condition li ≤N1 ≤
Ni for every i ∈[k]. When Qk
i=2 Ni = Ω(Nk
1), we set li := Θ(N1) for every i ∈[k]. □Against a standard oracle,
we obtain a similar result.
Corollary 7 For any positive integer k > 1, let Q2(k-clawdetect(N1, . . . , Nk)) be the number of queries needed
to decide whether there is a k-claw or not for functions fi : Xi := [Ni] →Z (i ∈[k]) given as a standard oracle,
where Ni ≤N j if i < j. If k is constant,
Q2(k-clawdetect(N1, . . . , Nk)) =

O
 Qk
i=1 Ni
 1
k+1
!
if Qk
i=2 Ni = O(Nk
1),
O
 qQk
i=2 Ni/Nk−2
1

otherwise.
4
Claw Finding
We now describe an algorithm, Claw Search, that ﬁnds a claw. The algorithm consists of three stages. In the
ﬁrst stage, we ﬁnd an O(N)-sized subset Y′ of Y such that there is a claw in X ×Y′, by performing binary search
over Y with Claw Detect. In the second stage, we perform 4-ary search over X and Y′ with Claw Detect to ﬁnd
O(1)-sized subsets X′′ and Y′′ of X and Y′, respectively, such that there is a claw in X′′ × Y′′. In the ﬁnal stage,
we search X′′ × Y′′ for a claw by issuing classical queries. To keep the error rate moderate, say, at most 1/3,
Claw Detect is repeated O(s) times against the same pair of domains at the sth node of the search tree at each
stage. This pushes up the query complexity by only a constant multiplicative factor.
Figure 1 precisely describes Claw Search. Steps 2, 3 and 4 in the ﬁgure correspond to the ﬁrst, second and
ﬁnal stages, respectively.

---- page 8 ----
Algorithm Claw Search
Input: Integers M and N such that M ≥N; Comparison oracle O f,g for functions f : X →Z and g : Y →Z,
respectively, such that X := [N] and Y := [M].
Output: Claw pair (x, y) ∈X × Y such that f(x) = g(y) if such a pair exists; otherwise (−1, −1).
1. Set ˜X := X and ˜Y := Y.
2. Set s := 1, and repeat the next steps until u ˜Y −l ˜Y ≤| ˜X|, where u ˜Y and l ˜Y are the largest and smallest
values, respectively, in ˜Y.
2.1 Set ΞY := {[l ˜Y.m ˜Y −1], [m ˜Y.u ˜Y]}, where m ˜Y := ⌈(l ˜Y + u ˜Y)/2⌉.
2.2 For every ˜Y′ ∈ΞY, do the following.
If all ˜Y′ ∈ΞY are examined, output (−1, −1) and halt.
2.2.1 Apply Claw Detect (s + 2) times to f and g restricted to domains ˜X and ˜Y, respectively.
2.2.2 If at least one of the (s + 2) results is “true,” set ˜Y := ˜Y′, and break (leave (b)).
2.3 Set s := s + 1.
3. Set s := 1, and repeat the next steps until uD −lD ≤c for every D ∈{ ˜X, ˜Y} and some constant c, say, 100,
where uD and lD are the largest and smallest values, respectively, in D.
3.1 For every D ∈{ ˜X, ˜Y}, set ΞD := {[lD.uD]} if uD −lD ≤c, and
otherwise, set ΞD := {[lD.mD −1], [mD.uD]} where mD := ⌈(lD + uD)/2⌉.
3.2 For every pair ( ˜X′, ˜Y′) ∈Ξ ˜X × Ξ ˜Y, do the following.
If all the pairs are examined, output (−1, −1) and halt.
3.2.1 Apply Claw Detect (s + 3) times to f and g restricted to domains ˜X′ and ˜Y′, respectively.
3.2.2 If at least one of the (s + 3) results is “true,” set ˜X := ˜X′ and ˜Y := ˜Y′, and break (leave (b)).
3.3 Set s := s + 1.
4. Classically search ˜X × ˜Y for a claw.
5. Output claw (x, y) ∈˜X × ˜Y if it exists; otherwise output (−1, −1).
Figure 1: Algorithm Claw Search
Theorem 8 Let Q2(clawﬁnding(N, M)) be the number of queries needed to locate a claw if it exists for functions
f : X = [N] →Z and g : Y = [M] →Z given as a comparison oracle. Then,
Q2(clawﬁnding(N, M)) =

O

(NM)1/3 log N

N ≤M < N2
O(M1/2 log N)
M ≥N2.
Proof We will analyze Claw Search in Fig. 1.
When there is no claw, Claw Search always outputs the correct answer. Suppose that there is a claw. The
algorithm may output a wrong answer if at least one of the following two cases happens. In case (1), one of
O(log M/N) runs of step 2.(b) errs; in case (2), one of O(log N) runs of step 3.(b) errs.
Without loss of generality, the error probability of Claw Detect can be assumed to be at most 1/3. The error
probability of each single run of step 2.(b).i is at most
1
3s+2 . The error probability of each run of step 2.(b) is
at most
2
3s+2 <
1
3s+1 . The error probability of case (1) is thus at most P⌈log M/N⌉
s=1
1
3s+1 < 1
6. The error probability
of case (2) is also at most P⌈log N1⌉
s=1
1
3s+1 < 1
6 by similar calculation. Therefore, the overall error probability is at
most 1/6+1/6=1/3.

---- page 9 ----
We next estimate the number of queries. If N ≤M < N2, the size of ˜Y is always at most quadratically
diﬀerent from that of ˜X. Thus, the sth repetition of step 2 requires O(s(NM/2s)1/3 log N) queries by Lemma 4.
Similarly, the sth repetition of step 3 requires O(s(N/2s)2/3 log N) queries by Lemma 4.
The total number of queries is
O

⌈log(M/N)⌉
X
s=1
 
s

N M
2s
1/3
log N
!
+
⌈log N⌉
X
s=1

s(N/2s)2/3 log N
= O

(NM)1/3 log N

.
If M ≥N2, the sth repetition of step 2 requires O(s((NM/2s)1/3 + (M/2s)1/2) log N) by Lemma 4. Thus,
similar calculation gives O(M1/2 log N) queries. □
□
We can easily obtain the standard-oracle version of the above theorem by using Corollary 5 instead of Lemma 4.
Corollary 9 Let Q2(clawﬁnding(N, M)) be the number of queries needed to locate a claw if it exists for functions
f : X := [N] →Z and g : Y := [M] →Z given as a standard oracle. Then,
Q2(clawﬁnding(N, M)) =

O

(NM)1/3
N ≤M < N2
O(M1/2)
M ≥N2.
Similarly, we can ﬁnd a k-claw by using k-Claw Detect as a subroutine. First, we ﬁnd O(N1)-sized subset X′
i of
Xi for every i ∈[2.k] such that there is a k-claw in X1 × X′
2 × · · · × X′
k, by performing 2k−1-ary search over X′
i’s
for all i ∈[2.k] with k-Claw Detect. Let X′
1 := X1. We then perform 2k-ary search over X′
is for all i ∈[k] with
k-Claw Detect to ﬁnd O(1)-sized subset X′′
i of X′
i for every i ∈[k] such that there is a k-claw in X′′
1 × · · · × X′′
k .
Finally, we search X′′
1 × · · · × X′′
k for a k-claw by issuing classical queries. A more precise description of the
algorithm, k-Claw Search, is given in Fig. 2.
Theorem 10 For any positive integer k > 1, let Q2(k-clawﬁnding(N1, . . . , Nk)) be the number of queries needed
to locate a k-claw if it exists for k functions fi : Xi := [Ni] →Z (i ∈[k]) given as a comparison oracle, where
Ni ≤N j if i < j. If k is constant,
Q2(k-clawﬁnding(N1, · · · , Nk)) =

O
 Qk
i=1 Ni
 1
k+1 log N1
!
if Qk
i=2 Ni = O(Nk
1),
O
 qQk
i=2 Ni/Nk−2
1
log N1

otherwise.
We can easily obtain the standard-oracle version of the above theorem by using Corollary 7 instead of Lemma 6.
Corollary 11 For any positive integer k > 1, let Q2(k-clawﬁnding(N1, . . . , Nk)) be the number of queries needed
to locate a k-claw if it exists for k functions fi : Xi := [Ni] →Z (i ∈[k]) given as a standard oracle, where
Ni ≤N j if i < j. If k is constant,
Q2(k-clawﬁnding(N1, · · · , Nk)) =

O
 Qk
i=1 Ni
 1
k+1
!
if Qk
i=2 Ni = O(Nk
1),
O
 qQk
i=2 Ni/Nk−2
1

otherwise.

---- page 10 ----
References
[1] Scott Aaronson and Yaoyun Shi. Quantum lower bounds for the collision and the element distinctness
problems. Journal of the ACM, 51(4):595–605, 2004.
[2] Andoris Ambainis. Quantum walk algorithm for element distinctness. SIAM Journal on Computing,
37(1):21—239, 2007.
[3] Andris Ambainis. Quantum walk algorithm for element distinctness. In Proceedings of the Forty-Fifth
IEEE Symposium on Foundations of Computer Science, pages 22–31. IEEE Computer Society, 2004.
[4] Gilles Brassard, Peter Høyer, Michele Mosca, and Alain Tapp. Quantum amplitude ampliﬁcation and
estimation. In Quantum Computation and Quantum Information: A Millennium Volume, volume 305 of
AMS Contem. Math., pages 53–74. 2002.
[5] Gilles Brassard, Peter Høyer, and Alain Tapp. Quantum cryptanalysis of hash and claw-free functions. In
Claudio L. Lucchesi and Arnaldo V. Moura, editors, Proceedings of the Third Latin American Symposium
on Theoretical Informatics (LATIN ’98), volume 1380 of Lecture Notes in Computer Science, pages 163–
169. Springer, 1998.
[6] Andries E. Brouwer, Arjeh M. Cohen, and Arnold Neumaier. Distance-Regular Graphs. A series of
Modern Surveys in Mathematics. Springer-Verlag, 1989.
[7] Harry Buhrman, Christoph D¨urr, Mark Heiligman, Peter Høyer, Fr´ed´eric Magniez, Miklos Santha, and
Ronald de Wolf. Quantum algorithms for element distinctness. In Proceedngs of the Sixteenth Annual
IEEE Conference on Computational Complexity, pages 131–137, 2001.
[8] Harry Buhrman, Christoph D¨urr, Mark Heiligman, Peter Høyer, Fr´ed´eric Magniez, Miklos Santha, and
Ronald de Wolf. Quantum algorithms for element distinctness. SIAM Journal on Computing, 34(6):1324–
1330, 2005.
[9] Harry Buhrman and Robert ˇSpalek. Quantum veriﬁcation of matrix products. In Proceedings of the
Seventeenth Annual ACM/SIAM Symposium on Discrete Algorithms (SODA ’06), pages 880–889, 2006.
[10] Andrew M. Childs and Jason M. Eisenberg. Quantum algorithms for subset ﬁnding. Quantum Information
and Computation, 5(7):593–604, 2005.
[11] Lov K. Grover. A fast quantum mechanical algorithm for database search. In Proceedings of the Twenty-
Eighth Annual ACM Symposium on Theory of Computing, pages 212–219, 1996.
[12] P. Høyer, M. Mosca, and R. de Wolf. Quantum search on bounded-error inputs. In Proceedings of the
Thirtieth International Colloquium on Automata, Languages and Programming, volume 2719 of Lecture
Notes in Computer Science, pages 291–299. Springer, 2003.
[13] Fr´ed´eric Magniez, Ashwin Nayak, J´er´emie Roland, and Miklos Santha. Search via quantum walk. In
David S. Johnson and Uriel Feige, editors, Proceedings of the Thirty-Nineth Annual ACM Symposium on
Theory of Computing, pages 575–584. ACM, 2007.
[14] Fr´ed´eric Magniez, Miklos Santha, and Mario Szegedy. Quantum algorithms for the triangle problem. In
Proceedings of the Sixteenth Annual ACM/SIAM Symposium on Discrete Algorithms (SODA ’05), pages
1109–1117, 2005.
[15] Peter W. Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum
computer. SIAM Journal on Computing, 26(5):1484–1509, 1997.

---- page 11 ----
[16] Mario Szegedy. Quantum speed-up of markov chain based algorithms. In Proceedings of the Forty-Fifth
IEEE Symposium on Foundations of Computer Science, pages 32–41. IEEE Computer Society, 2004.
[17] Shengyu Zhang. Promised and distributed quantum search. In Proceedings of the Eleventh Annual Inter-
national Conference on Computing and Combinatorics (COCOON ’05), volume 3595 of Lecture Notes
in Computer Science, pages 430–439. springer, 2005.

---- page 12 ----
Algorithm k-Claw Search
Input: k integers N1, . . . , Nk such that Ni ≤N j if i < j.
Comparison oracle O f1,..., fk for functions fi : Xi →Z such that Xi := [Ni] for every i ∈[k].
Output: k-claw (x1, . . . , xk) ∈X1 × · · · × Xk such that fi(xi) = fj(xj) for every i, j ∈[k] if it exists; otherwise
(−1, . . . , −1).
1. Set ˜Xi := Xi for every i ∈[k].
2. Set s := 1, and repeat the next steps until ui −li ≤| ˜X1| for all i ∈[2.k], where ui and li are the largest and
smallest values, respectively, in ˜Xi.
2.1 For every i ∈[2.k], set Ξi := {[li.ui]} if ui −li ≤| ˜X1|, and
otherwise, set Ξi := {[li.mi −1], [mi.ui]} where mi := ⌈(li + ui)/2⌉.
2.2 For every tuple ( ˜X′
1, ˜X′
2, . . . , ˜X′
k) ∈{ ˜X1} × Ξ2 × · · · × Ξk, do the following.
If all the tuples are examined, output (−1, . . . , −1) and halt.
2.2.1 Apply k-Claw Detect (s + 1) + ⌈log3 2k−1⌉times to the k functions fi restricted to domains ˜X′
i,
respectively, for every i ∈[k].
2.2.2 If at least one of the (s + 1) + ⌈log3 2k−1⌉results is “true,” set ˜Xi := ˜X′
i for every i ∈[2.k], and
break (leave (b)).
2.3 Set s := s + 1.
3. Set s := 1, and repeat the next steps until ui −li ≤c for all i ∈[k] and some constant c, say, 100, where
ui and li are the largest and smallest values, respectively, in ˜Xi.
3.1 For every i ∈[k], set Ξi := {[li.ui]} if ui −li ≤c, and
otherwise, set Ξi := {[li.mi −1], [mi.ui]} where mi = ⌈(li + ui)/2⌉.
3.2 For every tuple ( ˜X′
1, ˜X′
2, . . . , ˜X′
k) ∈Ξ1 × · · · × Ξk, do the following.
If all the tuples are examined, output (−1, . . . , −1) and halt.
3.2.1 Apply k-Claw Detect (s + 1) + ⌈log3 2k⌉times to the k functions fi restricted to domains ˜X′
i for
every i ∈[k].
3.2.2 If at least one of the (s + 1) + ⌈log3 2k⌉results is “true,” set ˜Xi := ˜X′
i for every i ∈[k], and break
(leave (b)).
3.3 Set s := s + 1.
4. Classically search ˜X1 × · · · × ˜Xk for a k-claw.
5. Output k-claw (x1, . . . , xk) ∈X′
1 × · · · × X′
k if it exists; otherwise output (−1, . . . , −1).
Figure 2: Algorithm k-Claw Search

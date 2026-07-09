# Marker Extraction (Fallback via pdftotext)

*Note: Marker (VikParuchuri/marker) was not available in this environment.
This extraction was produced via `pdftotext -layout` from the arXiv PDF as a
faithful text fallback. The full plain-text extraction of the paper follows.*

**Source:** `paper.pdf` — arXiv:1704.06774v3 (Ambainis & Kokainis, 2017/2022)

---

                                            Quantum algorithm for tree size estimation, with applications to
                                                          backtracking and 2-player games
                                                                         Andris Ambainis†             Martins Kokainis†




arXiv:1704.06774v3 [quant-ph] 28 Dec 2022
                                                                                             Abstract
                                                  We study quantum algorithms on search trees of unknown structure, in a model where the tree
                                                  can be discovered by local exploration. That is, we are given the root of the tree and access to
                                                  a black box which, given a vertex v, outputs the children of v.
                                                      We construct a quantum algorithm which, given such access to a√search tree of depth at most
                                                  n, estimates the size of the tree T within a factor of 1 ± δ in Õ( nT ) steps. More generally,
                                                  the same algorithm can be used to estimate size of directed acyclic graphs (DAGs) in a similar
                                                  model.
                                                      We then show two applications of this result:
                                                     • We show how to transform a classical
                                                                                         √ backtracking search algorithm which examines T
                                                       nodes of a search tree into an Õ( T n3/2 ) time quantum algorithm, improving over an
                                                       earlier quantum backtracking algorithm of Montanaro [12].
                                                     • We give a quantum algorithm for evaluating AND-OR formulas in a model where the
                                                       formula can be discovered by local exploration (modeling position trees in 2-player games).
                                                       We show that, in this setting, formulas of size T and depth T o(1) can be evaluated in
                                                       quantum time O(T 1/2+o(1) ). Thus, the quantum speedup is essentially the same as in the
                                                       case when the formula is known in advance.

                                            †
                                                Faculty of Computing, University of Latvia
1     Introduction
Many search algorithms involve exploring search trees of an unknown structure. For example,
backtracking algorithms perform a depth-first search on a tree consisting of partial solutions to the
computational task (for example, partial assignments for SAT in the well known DPLL algorithm
[3, 4]), until a full solution is found. Typically, different branches of the tree stop at different depths
(e.g., when the corresponding partial assignment can no longer be extended) and the structure of
the tree can be only determined by exploring it.
     Quantum algorithms provide a quadratic speedup for many search problems, from simple ex-
haustive search (Grover’s algorithm [6]) to computing AND-OR formulas [1, 5, 14] (which corre-
sponds to determining the winner in a 2-player game, given a position tree). These algorithms,
however, assume that the structure of the search space is known. Grover’s algorithm assumes that
the possible solutions in the search space can be indexed by numbers 1, 2, . . . , T so that, given i,
one can efficiently (in constant or polylog time) find the ith possible solution. In the case of back-
tracking trees, the unknown structure of the tree prevents us from setting up such an addressing
scheme.
     In the case of AND-OR formulas, the quantum algorithms of [1, 14] work for formula of any
structure but the coefficients in algorithm’s transformations depend on the sizes of different subtrees
of the formula tree. Therefore, the algorithm can be only used if the whole AND-OR formula is
known in advance (and only the values of the variables are unknown) which is not the case if the
formula corresponds to a position tree in a game.
     Despite the importance of such algorithms classically, there has been little work on quantum
search on structures which can be only explored locally. The main algorithmic result of this type
is a recent algorithm by Montanaro for quantum backtracking. Given a search tree         √ of size T and
depth n, Montanaro’s algorithm   √ detects if the tree contains a marked vertex in O( T n) steps (and
finds a marked vertex in O( T n3/2 ) steps).
     In this paper, we show three new quantum algorithms for trees of an unknown structure,
including an improvement to Montanaro’s algorithm. We start with
     Quantum tree size estimation. We show that, given a tree T with a depth at most n, the
size T of the tree T can be estimated to a multiplicative
                                                   √            factor of 1 + δ, for an arbitrary constant
δ > 0, by a quantum algorithm that uses Õ( T n) steps1 . More generally, our algorithm is also
applicable to estimating size of directed acyclic graphs (DAGs) in a similar model.
     We then apply the quantum tree size estimation algorithm to obtain two more results.
     Improved quantum algorithm for backtracking. Montanaro’s algorithm has the following
drawback. Since classical search algorithms are optimized to search the most promising branches
first, a classical search algorithm may find a marked vertex after examining T ′ ≪ T nodes of the
tree. Since the running time of Montanaro’s algorithm depends on T , the quantum speedup that
it achieves can be much less than quadratic (or there might be no speedup at all).
     We fix this problem by using our tree size estimation√ algorithm. Namely, we construct a
quantum algorithm that searches a backtracking tree in Õ( T ′ n3/2 ) steps where T ′ is the number
of nodes actually visited by the classical algorithm.
     AND-OR formulas of unknown structure. We construct a quantum algorithm for comput-
   1
     In the statements of results in the abstract and the introduction, Õ hides log T and log n factors and the depen-
dence of the running time on the maximum degree d of vertices in a tree T (or a DAG G). More precise bounds are
given in Section 3.



                                                          1
ing AND-OR formulas in a model where the formula is accessible by local exploration, starting from
the root (which is given). More specifically, we assume query access to the following subroutines:
    • given a node v, we can obtain the type of the node (AND, OR or a leaf),

    • given a leaf v, we can obtain the value of the variable (true or false) at this leaf,

    • given an AND/OR node, we can obtain pointers to the inputs of the AND/OR gate.
This models a position tree in a 2-player game (often mentioned as a motivating example for
studying AND-OR trees) with OR gates corresponding to positions at which the 1st player makes
a move and AND gates corresponding to positions at which the 2nd player makes a move.
   We give an algorithm that evaluates AND-OR formulas of size T and depth T o(1) in this model
with O(T 1/2+o(1) ) queries. Thus, the quantum speedup is almost the same as in the case when the
formula is known in advance (and only values at the leaves need to be queried) [1, 14], as long as
the depth of the tree is not too large.


2     Preliminaries
2.1    Setting
We consider a tree T of an unknown structure given to us in the following way:
    • We are given the root r of T .

    • We are given a black box which, given a vertex v, returns the number of children d(v) for this
      vertex.

    • We are given a black box which, given a vertex v and i ∈ [d(v)], returns the ith child of v.
     Trees of unknown structure come up in several different settings.
     Backtracking. Let A be a backtracking algorithm that searches a solution space D in a depth-
first fashion. The space D consists of partial solutions where some of the relevant variables have
been set. (For example, D can be the space of all partial assignments for a SAT formula.) Then,
the corresponding tree T is defined as follows:
    • vertices vx correspond to partial solutions x ∈ D;

    • the root r corresponds to the empty solution where no variables have been set;

    • children of a vertex vx are the vertices vy corresponding to possible extensions y of the partial
      solution x that A might try (for example, a backtracking algorithm for SAT might choose
      one variable and try all possible values for this variable), in the order in which A would try
      them.
    Two-player games. T may also be a position tree in a 2-player game, with r corresponding
to the current position. Then, children of a node v are the positions to which one could go by
making a move at the position v. A vertex v is a leaf if we stop the evaluation at v and do not
evaluate children of v.
    DAGs of unknown structure. We also consider a generalization of this scenario to directed
acyclic graphs (DAGs). Let G be a directed acyclic graph. We assume that

                                                   2
   • Every vertex v is reachable from the root r via a directed path.

   • The vertices of G can be divided into layers so that all edges from layer i go to layer i + 1.

   • Given a vertex v, we can obtain the number d(v) of edges (u, v) and the number d′ (v) of edges
     (v, u).

   • Given a vertex v and a number i ∈ [d(v)], we can obtain the ith vertex u with an edge (u, v).

   • Given a vertex v and a number i ∈ [d′ (v)], we can obtain the ith vertex u with an edge (v, u).

2.2    Notation
By [a .. b], with a, b being integers, a ≤ b, we denote the set {a, a + 1, a + 2, . . . , b}. When a = 1,
notation [a .. b] is simplified to [b].
   We shall use the following notation for particular matrices:

   • Ik : the k × k identity matrix;

   • 0k1 ,k2 : the k1 × k2 all-zeros matrix.

We use the following notation for parameters describing a tree T or a DAG G:

   • T denotes the number of edges in T (or G) or an upper bound on the number of edges which
     is given to an algorithm.

   • n denotes the depth of T (or G) or an upper bound on the depth which is given to an
     algorithm.

   • d denotes the maximum possible total degree of a vertex v ∈ T (G).

   • For any vertex x ∈ T (where T is a tree), the subtree rooted at x will be denoted by T (x).

2.3    Eigenvalue estimation
Quantum eigenvalue estimation is an algorithm which, given a quantum circuit implementing a
unitary U and an eigenstate |ψi s.t. U |ψi = eiθ |ψi, produces an estimate for θ. It is known that
                                                                                   1        1
one can produce an estimate θ̂ such that P r[|θ − θ̂| ≤ δest ] ≥ 1 − ǫest with O( δest log ǫest ) repetitions
of a circuit for controlled-U .
    If eigenvalue estimation is applied to a quantum state |ψi that is a superposition of several
eigenstates                           X
                                |ψi =   αj |ψj i , U |ψj i = eiθj |ψj i ,
                                         j

the result is as if we are randomly choosing j with probability |αj |2 and estimating θj .
    In this paper, we use eigenvalue estimation to estimate the eigenvalue eiθmin that is closest to
1 (by that, here and later, we mean the eigenvalue which is closest to 1 among all eigenvalues that
are distinct from 1, i.e., the eigenvalue eiθmin with the smallest nonzero absolute value |θmin |). We
assume that we can produce a state |ψstart i such that |ψstart i is orthogonal to all 1-eigenvectors of
U and
                                   |hΨ+ |ψstart i|2 + |hΨ− |ψstart i|2 ≥ C

                                                     3
where |Ψ+ i and |Ψ− i are eigenstates with eigenvalues eiθmin and e−iθmin and C is a known constant.
(If U does not have an eigenvector with an eigenvalue e−iθmin , the condition should be replaced by
|hΨ+ |ψstart i|2 ≥ C.) We claim

Lemma 1. Under the conditions above, there is an algorithm which produces an estimate θ̂ such
that P r[|θmin − θ̂| ≤ δmin ] ≥ 1 − ǫmin with
                                                              
                                          1 1       1    2 1
                                      O          log log
                                          C δmin    C     ǫmin

repetitions of a circuit for controlled-U .

Proof. In Section 4.


3     Results and algorithms
3.1    Results on estimating sizes of trees and DAGs
In this subsection, we consider the following task:
    Tree size estimation. The input data consist of a tree T and a value T0 which is supposed to
be an upper bound on the number of vertices in the tree. The algorithm must output an estimate
for the size of the tree. The estimate can be either a number T̂ ∈ [T0 ] or a claim “T contains more
than T0 vertices”. We say that the estimate is δ-correct if:

    1. the estimate is T̂ ∈ [T0 ] and it satisfies |T − T̂ | ≤ δT where T is the actual number of vertices;

    2. the estimate is “T contains more than T0 vertices” and the actual number of vertices T
       satisfies (1 + δ)T > T0 .

We say that an algorithm solves the tree size estimation problem up to precision 1 ± δ with correct-
ness probability at least 1 − ǫ if, for any T and any T0 , the probability that it outputs a δ-correct
estimate is at least 1 − ǫ.
    More generally, we can consider a similar task for DAGs.
    DAG size estimation. The input data consist of a directed acyclic graph G and a value T0
which is supposed to be an upper bound on the number of edges in G. The algorithm must output
an estimate for the number of edges. The estimate can be either a number T̂ ∈ [T0 ] or a claim “G
contains more than T0 edges”. We say that the estimate is δ-correct if:

    1. the estimate is T̂ ∈ [T0 ] and it satisfies |T − T̂ | ≤ δT where T is the actual number of edges;

    2. the estimate is “G contains more than T0 edges” and the actual number of edges T satisfies
       (1 + δ)T > T0 .

We say that an algorithm solves the DAG size estimation problem up to precision 1 ± δ with
correctness probability at least 1 − ǫ if, for any G and any T0 , the probability that it outputs a
δ-correct estimate is at least 1 − ǫ.
    Tree size estimation is a particular case of this problem: since a tree with T edges has T + 1
vertices, estimating the number of vertices and the number of edges are essentially equivalent for
trees. We show

                                                     4
Theorem 2. DAG size estimation up to precision 1±δ can be solved with the correctness probability
at least 1 − ǫ by a quantum algorithm which makes
                                         √                
                                             nT0       2 1
                                       O         d log
                                            δ1.5         ǫ

queries to black boxes specifying G and O(log T0 ) non-query transformations per query.

   Note. If we use Õ-notation, the O(log T0 ) factor can be subsumed into the Õ and the time
complexity is similar to query complexity.

3.2    Algorithm for DAG size estimation
In this subsection, we describe the algorithm of Theorem 2. The basic framework of the algorithm
(the state space and the transformations that we use) is adapted from Montanaro [12].
    Let G = (V, E) be a directed acyclic graph, with |V| = V vertices and |E| = T edges. We assume
that the root is labeled as v1 .
    For each vertex vi ∈ V

   • ℓ(i) ≤ n stands for the distance from vi to the root,

   • di ≤ d stands for the total degree of the vertex vi . In notation in Section 2.1, we have
     di = d(vi ) + d′ (vi ).

For technical purposes we also introduce an additional vertex vV +1 and an additional edge eT +1 =
(vV +1 , v1 ) which connects vV +1 to the root. Let V′ = V ∪ {vV +1 }, E′ = E ∪ {eT +1 } and G ′ = (V′ , E′ ).
    For each vertex v by E(v) we denote the set of all edges in E incident to v (in particular, when
v = v1 is the root, the additional edge eT +1 ∈   / E is not included in E(v1 )).
    Let VA be the set of vertices at an even distance from the root (including the root itself) and VB
be the set of vertices at an odd distance from the root. Let A = |VA | and B = |VB |, then V = A+B.
Label the vertices in V so that VA = {v1 , v2 , . . . , vA } and VB = {vA+1 , vA+2 , . . . , vA+B }.
    Let α > 0 be fixed. Define a Hilbert space H spanned by {|ei e ∈ E′ } (one basis state per
edge, including the additional edge). For each vertex v ∈ V define a vector |sv i ∈ H as
                                       (               P
                                         |eT +1 i + α e∈E(v) |ei , v = v1
                                |sv i = P
                                            e∈E(v) |ei ,             v 6= v1 .

Define a subspace HA ⊂ H spanned by {|sv i v ∈ VA } and a subspace HB ⊂ H spanned by
{|sv i v ∈ VB }. Define a unitary operator RA which negates all vectors in HA (i.e., maps |ψi to
− |ψi for all |ψi ∈ HA ) and leaves HA  ⊥ invariant. Analogously, a unitary operator R negates all
                                                                                         B
vectors in HB and leaves HB   ⊥ invariant.

    Similarly as in [12], both RA and RB are implemented as the direct sum of diffusion operators Dv .
Let a subspace Hv , v ∈ V, be spanned by {|ei e ∈ E(v)} (or {|ei e ∈ E(v)}∪{|eT +1 i} when v = v1
is the root). Define the diffusion operator Dv , which acts on the subspace Hv , as I − ks2k2 |sv i hsv |.
                                                                                                 v
This way, each Dv can be implemented with only knowledge of v and its neighborhood. (A minor
difference from [12]: since we are concerned with tree size estimation problem now, we make no
assumptions about any vertices being marked at this point and therefore Dv is not the identity for
any v ∈ V.)

                                                      5
   Then,                           M                                            M
                          RA =            Dv   and RB = |eT +1 i heT +1 | +            Dv .
                                   v∈VA                                         v∈VB

In Section 5, we show

Lemma 3. Transformations RA and RB can be implemented using O(d) queries and O(d log V )
non-query gates.

    We note that RA and RB are defined with respect to a parameter α, to be specified in the
algorithm that uses the transformations RA and RB .
    The algorithm of Theorem 2 for estimating size of DAGs is as follows:

Algorithm 1 Algorithm for DAG size estimation
                                                                                                  √
  1. Apply the algorithm of Lemma 1 for the transformation RB RA (with α =                         2nδ−1 ) with the
                                                                           δ1.5
     state |ψstart i = |eT +1 i and parameters C = 94 , ǫmin = ǫ, δmin = 24√ 3nT              0

                       1
  2. Output T̂ =                 as the estimate for the number of edges.
                   α2 sin2 θ̂2




3.3    Analysis of Algorithm 1
We now sketch the main ideas of the analysis of Algorithm 1. From Lemma 13 in Section 6.2
it follows that RB RA has no 1-eigenvector |ψi with hψ|eT +1 i 6= 0. Let |Ψ+ i and |Ψ− i be the
two eigenvectors of RB RA with eigenvalues e±iθ closest to 1. Lemma 4 shows that the starting
state |eT +1 i has sufficient overlap with the subspace spanned by these two vectors for applying the
algorithm of Lemma 1.
                      √
Lemma 4. If α ≥ 2n, we have
                                                             2
                                              heT +1 |q2 i ≥
                                                             3
for a state |q2 i ∈ span {|Ψ+ i , |Ψ− i}.

Proof. In Section 6.4.

  Lemma 5 shows that the estimate θ̂ provides a good estimate T̂ for the size of the DAG.
                                          √
Lemma 5. Suppose that δ ∈ (0, 1). Let α = 2nδ−1 and θ̂ ∈ (0; π/2) satisfy

                                                              δ1.5
                                                θ̂ − θ ≤      √    .
                                                            24 3nT
Then
                                                        1
                                       (1 − δ)T ≤                 ≤ (1 + δ)T.
                                                    α2 sin2 θ̂2
Proof. In Section 6.4.


                                                         6
    Lemmas 1, 4 and 5 together imply that Algorithm 1 outputs a good estimate with probability
at least 1 − ǫ. According to Lemma 1, we need to invoke controlled versions of RA and RB
                                                      √               
                             1 1       1    2 1             nT0      2 1
                         O          log log         =O           log
                             C δmin    C     ǫmin          δ1.5        ǫ

times and because of Lemma 3, each of these transformations can be performed with O(d) queries
and O(d log V ) = O(d log T0 ) non-query transformations.
   Proof of Lemmas 4 and 5 consists of a number of steps:

  1. We first relate the eigenvalues of RA RB to singular values of an A × B matrix L. The matrix
     L is defined by L[v, w] = kshsv vk·ks
                                       |sw i
                                           wk
                                              . Because of a correspondence by Szegedy [15], a pair of
      eigenvalues e±iθ of RB RA corresponds to a singular value λ = cos 2θ of L.

  2. Instead of L, we consider K = (I − LL∗ )−1 (with both rows and columns indexed by elements
     of VA ). A singular value λ of L corresponds to an eigenvalue (1 − λ2 )−1 of K.

  3. We relate K to the fundamental matrix N of a certain classical random walk on the graph
     G. (The entries of the fundamental matrix N [i, j] are the expected number of visits to j that
     the random walk makes if it is started in the vertex i.)

  4. We relate N to the resistance between i and j if the graph G is viewed as an electric network.

  5. We bound the electric resistance, using the fact that the resistance only increases if an edge
     is removed form G. Thus, the maximum resistance is achieved if G is a tree.

    This analysis yields that the entries of K can be characterized by the inequalities

                               α2 a[i]a[j] ≤ K[i, j] ≤ α2 + n a[i]a[j]
                                                             

               √                      p
where a[1] = d1 + α−2 and a[j] = dj for j ∈ [2 .. A] (Lemma 14 in Section 6.3). From this we
derive bounds on the largest eigenvalue of K which imply bounds on the eigenvalue of RB RA that
is closest to 1.
    We describe the analysis in more detail in Section 6.

3.4   Better backtracking algorithm
Backtracking task. We are given a tree T and a black-box function

                             P : V (T ) → {true, f alse, indeterminate}

(with P (x) telling us whether x is a solution to the computational problem we are trying to solve),
where V (T ) stands for the set of vertices of T and P (v) ∈ {true, f alse} iff v is a leaf. A vertex
v ∈ V (T ) is called marked if P (v) = true. We have to determine whether T contains a marked
vertex.
    For this section, we assume that the tree is binary. (A vertex with d children can be replaced
by a binary tree of depth ⌈log d⌉. This increases the size of the tree by a constant factor, the depth
by a factor of at most ⌈log d⌉ and the complexity bounds by a polylogarithmic factor of d.)

Theorem 6. [12] There is a quantum algorithm which, given

                                                  7
   • a tree T (accessible through black boxes, as described in Section 2.1),

   • an access to the black-box function P , and

   • numbers T1 and n which are upper bounds on the size and the depth of T ,
                                                                                 √
determines if the tree contains a marked vertex with query and time complexity O( T1 n log 1ǫ ), with
the probability of a correct answer at least 1 − ǫ.

    The weakness of this theorem is that the complexity of the algorithm depends on T1 . On the
other hand, a classical backtracking algorithm A might find a solution in substantially less than T1
steps (either because the tree T contains multiple vertices x : P (x) = true or because the heuristics
that A uses to decide which branches to search first are likely to lead to x : P (x) = true).
    We improve on Montanaro’s algorithm by showing

Theorem 7. Let A be a classical backtracking algorithm. There is a quantum algorithm that, with
probability at least 1 − ǫ, outputs 1 if T contains a marked vertex and 0 if T does not contain a
marked vertex and uses
                                            √
                                                              
                                                    2 n log T1
                                       O n nT log
                                                          ǫ
queries and O(log T1 ) non-query transformations per query where

   • T1 is an upper bound on the size of T (which is given to the quantum algorithm),

   • n is an upper bound on the depth of the T (also given to the quantum algorithm),

   • T is the number of vertices of T actually explored by A.

Proof. The main idea of our search algorithm is to generate subtrees of T that consist of first
approximately 2i vertices visited by the classical backtracking strategy A, increasing i until a
marked vertex is found or until we have searched the whole tree T .
    Let Tm be the subtree of T consisting of the first m vertices visited by the classical backtracking
algorithm A. Then, we can describe Tm by giving a path

                                    r = u0 → u1 → u2 → . . . → ul = u                                       (1)

where u is the mth vertex visited by A. Then, Tm consists of all the subtrees T (u) rooted at u such
that u is a child of ui (for some i ∈ [0 .. l − 1]) that is visited before ui+1 and the vertices u0 , . . . , ul
on the path.
   Given access to T and the path (1), one can simulate Montanaro’s algorithm on Tm . Mon-
tanaro’s algorithm consists of performing the transformations similar to RA and RB described in
Section 3.2, except that Dv is identity if v is marked. To run Montanaro’s algorithm on Tm , we use
access to T but modify the transformations of the algorithm as follows:

   • when performing Dv for some v, we check if v is one of vertices ui on the path;

   • if v = ui for some i ∈ [0 .. l − 1] and ui+1 is the first child of ui , we change Dv as if ui+1 is the
     only child of ui ;

   • otherwise, we perform Dv as usually.

                                                       8
Lemma 8. There is a quantum algorithm that generates the path

                                  r = u0 → u1 → u2 → . . . → ul = u

corresponding to a subtree Tm̂ for m̂ : |m − m̂| ≤ δm with a probability at least 1 − ǫ and uses
                                            1.5 √            
                                            n       m     2 n
                                         O            log
                                               δ1.5         ǫ
queries and O(log T0 ) non-query transformations per query.

Proof. The algorithm Generate-path is described as Algorithm 2.

Algorithm 2 Procedure Generate-path(v, m)
Generate-path(v, m) returns a path (1) defining a subtree Tm̂ , with m̂ satisfying |m − m̂| ≤ δm
with a probability at least 1 − ǫ.

  1. If v is a leaf, return the empty path.

  2. Otherwise, let v1 , v2 be the children of v, in the order in which A visits them.

  3. Let m1 be an estimate for the size of T (v1 ), using the algorithm for the tree size estimation
     with the precision 1 ± δ, the probability of a correct answer at least 1 − nǫ and m−11−δ as the
     upper bound on the tree size.

  4. If m1 > m − 1, return the path obtained by concatenating the edge v → v1 with the path
     returned by Generate-path(v1 , m − 1).

  5. If m1 = m − 1, return the path obtained by concatenating the edge v → v1 with the path
     from vi to the last vertex of T (vi ) (that is, the path in which we start at vi and, at each
     vertex, choose the child that is the last in the order in which A visits the vertices).

  6. If m1 < m − 1, return the path obtained by concatenating the edge v → v2 with the path
     returned by Generate-path(v2 , m − 1 − m1 ).


    Correctness. Generate-path(v, m) invokes the tree size estimation once and may call itself
recursively once, with v1 or v2 instead of v. Since the depth of the tree is at most n, the depth
of the recursion is also at most n. On all levels of recursion together, there are at most n calls
to tree size estimation. If we make the probability of error for tree size estimation at most nǫ , the
probability that all tree size estimations return sufficiently precise estimates is at least 1 − ǫ. Under
this assumption, the number of vertices in each subtree added to T ′ is within a factor of 1 ± δ of
the estimate. This means that the total number of vertices in T ′ is within 1 ± δ of m (which is
equal to the sum of estimates).
    Query complexity. Tree size estimation is called at most n times, with the complexity of
                                             √              
                                                 nm      2 n
                                           O         log
                                                δ1.5       ǫ
each time, according to Theorem 2. Multiplying this complexity by n gives Lemma 8.

                                                   9
Algorithm 3 Main part of the quantum algorithm for speeding up backtracking
  1. Let i = 1.

  2. Repeat:

      (a) Run Generate-path(r, 2i ) with δ = 21 and error probability at most 2⌈logǫ T1 ⌉ , obtain a
          path defining a tree T ′ = Tm̂ .
      (b) Run Montanaro’s algorithm on T ′ , with the upper bound on the number of vertices 23 2i
          and the error probability at most 2⌈logǫ T1 ⌉ , stop if a marked vertex is found.
       (c) Let i = i + 1.

      until a marked vertex is found or T ′ contains the whole tree.

  3. If T ′ contains the whole tree and no marked vertex was found in the last run, stop.



    We now continue with the main algorithm for Theorem 7 (Algorithm 3).
    Correctness. Each of the two subroutines (Generate-path and Montanaro’s algorithm) is
invoked at most ⌈log T1 ⌉ times. Hence, the probability that all invocations are correct is at least
1 − ǫ.
    Query complexity. By Lemma 8, the number of queries performed by Generate-path in
the ith stage of the algorithm is           √                  
                                         1.5    i    2 n log T1
                                   O n         2 log
                                                           ǫ
and the complexity of Montanaro’s algorithm in the same stage of the algorithm is of a smaller
                                         T
order. Summing over i from 1 to ⌈log 1−δ     ⌉ (which is the maximum possible value of i if all the
subroutines are correct) gives the query complexity
                                              √
                                                                
                                          1.5         2 n log T1
                                    O n         T log              .
                                                            ǫ



    Note. If T is close to the size of the entire tree, the complexity of Algorithm 3 (given by
Theorem 7) may be larger than the complexity of Montanaro’s algorithm (given by Theorem 6).
To deal with this case, one can stop Algorithm 3 when the number of queries exceeds the expression
in Theorem 6 and then run Montanaro’s algorithm on the whole tree. Then, the complexity of the
resulting algorithm is the minimum of complexities in Theorems 6 and 7.

3.5   Evaluating AND-OR formulas of unknown structure
We now consider evaluating AND-OR formulas in a similar model where we are given the root of
the formula and can discover the formula by exploring it locally. This corresponds to position trees
in 2-player games where we know the starting position (the root of the tree) and, given a position,
we can generate all possible positions after one move. More precisely, we assume access to

   • a formula tree T (in the form described in Section 2.1);

                                                10
   • a black box which, given an internal node, answers whether AND or OR should be evaluated
     at this node;

   • a black box which, given a leaf, answers whether the variable at this leaf is 0 or 1.

Theorem 9. There is a quantum algorithm which evaluates an AND-OR tree of size at most T
and depth n = T o(1) in this model running in time O(T 1/2+δ ), for an arbitrary δ > 0.

Proof. We assume that the tree is binary. (An AND/OR node with k inputs can be replaced by a
binary tree of depth ⌈log k⌉ consisting of gates of the same type. This increases the size of the tree
by a constant factor and the depth by a factor of at most ⌈log k⌉.)
   We say that T ′ is an m-heavy element subtree of T if it satisfies the following properties:

   1. T ′ contains all x with |T (x)| ≥ m and all children of such x;

   2. all vertices in T ′ are either x with |T (x)| ≥ m
                                                      2 or children of such x.

Lemma 10. Let T be a tree and let T be an upper bound on the size of T . There is a
                                        1.5         
                                        n T      2 T
                                    O √ log
                                           m       ǫ

time quantum algorithm that generates T ′ such that, with probability at least 1−ǫ, T ′ is an m-heavy
element subtree of T .

Proof. The algorithm is as follows.

Algorithm 4 Algorithm Heavy-subtree(r, m, ǫ)
   1. Run the tree size estimation for T (r) with m as the upper bound on the number of vertices
                                       m
      and parameters δ = 14 and ǫ′ = 6nT  ǫ.

   2. If the estimate is smaller than 2m           ′
                                       3 , return T consisting of the root r only.

   3. Otherwise, let T ′ = {r}. Let v1 and v2 be the children of r. For each i, invoke Heavy-
      subtree(vi , m, ǫ) recursively and add all vertices from the subtree returned by Heavy-
      subtree(vi , m, ǫ) to T ′ . Return T ′ as the result.

   4. If, at some point, the number of vertices added to T ′ reaches 6T
                                                                     m n, stop and return the current
      T ′.


   The proof of correctness and the complexity bounds are given in Section 7.

    To evaluate an AND-OR formula with an unknown structure, let T be an upper bound on the
size of the formula F . Let c be an integer. For i = 1, . . . , c, we define Ti = T i/c . To evaluate F , we
identify an Tc−1 -heavy element subtree F ′ and then run the algorithm of [1] or [14] for evaluating
formulas with a known structure on it. The leaves of this F ′ are roots of subtrees of size at most
Tc−1 . To perform queries on them, we call the same algorithm recursively. That is, given a leaf
v, we identify a Tc−2 -heavy element subtree F ′ (v) and then run the algorithm of [1] or [14] for


                                                    11
Algorithm 5 Algorithm Unknown-evaluate(r, i, ǫ)
    1. If i = 1, determine the structure of the tree by exploring it recursively, let T ′ be the resulting
       tree.

    2. If i > 1, use Heavy-subtree(r, Ti−1 , ǫ/5) to obtain T ′ . Let s be the size of T ′ .

    3. Run the AND-OR formula evaluation algorithm for known formulas of [1] to evaluate the
       formula corresponding to T ′ , with a probability of a correct answer at least 1 − 5ǫ . If i > 1,
       use calls to Unknown-evaluate(v, i − 1, ǫ/s3 ) instead of queries at leaves v.

    4. If Unknown-evaluate is used as a query at a higher level (that is, if i < c), perform a phase
       flip to simulate the query and run the first three steps in reverse, erasing all the information
       that was obtained during this execution of Unknown-evaluate.



evaluating formulas with a known structure on it, with queries at the leaves replaced by another
recursive call of the same algorithm, now on a subtree of size at most Tc−2 .
    The algorithm that is being called recursively is described as Algorithm 5. To evaluate the
original formula F , we call Unknown-evaluate(r, c, ǫ).
    The proof of correctness and the complexity bounds are given in Section 7.


4     Proof of Lemma 1
We perform ordinary eigenvalue estimation t = ⌈ C1 ln ǫmin 2
                                                                ⌉ times, with parameters δest = δmin and
      ǫmin
ǫest = 2t . We then take
                                    θ̂ = min(|θˆ1 |, . . . , |θˆt |)
where θˆ1 , . . . , θˆt are the estimates that have been obtained.
   To see that P r[|θmin − θ̂| ≤ δmin ] ≥ 1 − ǫmin , we observe that:

    1. The probability that none of θˆj is an estimate for ±θmin is at most

                                                       − ln ǫ 2       ǫmin
                                         (1 − C)t ≤ e       min   =        .
                                                                       2

    2. The probability that one or more of θˆj differs from the corresponding θj by more than δest is
       at most tǫest = ǫmin
                        2 .

If none of these two “bad events” happens, we know that, among θˆj , there is an estimate for ±θmin
that differs from θmin or −θmin by at most δest . Moreover, any estimate θˆj for θj 6= ±θmin must
be at least |θj | − δest ≥ θmin − δest in absolute value. Therefore, even if θˆj with the smallest |θˆj | is
not an estimate for ±θmin , it must still be in the interval [θmin − δest , θmin + δest ].
    The number of repetitions of controlled-U is
                                                                            
                                1       1           1        1      1        1
                          O t      log        =O        log            log
                              δest     ǫest         C       ǫmin δmin       ǫest


                                                    12
                                     1
                 1
and we have log ǫest = log t + log ǫmin + O(1). Also, log t ≤ log C1 + log log ǫmin
                                                                                1
                                                                                    + O(1). Therefore,
                                                                            
                          1          1            1                 1       1
                     log      ≤ log + O log             = O log log              ,
                         ǫest        C          ǫmin                C    ǫmin
implying the lemma.


5     Implementing transformations RA and RB
We represent the basis states |ei as |u, wi where u ∈ VA and w ∈ VB ∪ {vV +1 }. Let H1 and H2 be
the registers holding u and w, respectively.
    Each |su i, u ∈ VA , can be expressed as |su i = |ui ⊗ |s′u i. We can view RA as a transformation
in which, for each u in H1 , we perform Du′ = I − ks′2k2 |s′u i hs′u | on the subspace |ui ⊗ H2 .
                                                          u
    The transformation Du′ can be performed as follows:
    1. Use queries to obtain the numbers of incoming and outgoing edges d(u) and d′ (u) (denoted
       by din and dout from now on). Use queries to obtain vertices w1 , . . . , wdin with edges (wj , u)
       and vertices w1′ , . . . , wd′ out with edges (u, wj ).

    2. Let H3 be a register with basis states |0i , . . . , |d + 1i. Use the information from the first step
       to perform a map on H2 ⊗ H3 that maps |w1 i |0i, . . ., |wdin i |0i, |w1′ i |0i, . . ., wd′ out |0i to
       |0i |1i, . . ., |0i |din + dout i and, if u = v1 , also maps |vV +1 i |0i to |0i |din + dout + 1i.

                   transformation D = I − 2 |ψi hψ| on H3 where
    3. Perform the P                                                   |ψi is the state obtained by
                                                                 Pdin +d
                     din +dout                                           out
       normalizing   i=1       |ii if u 6= v1 and by normalizing  i=1        |ii + α |din + dout + 1i if
       u = v1 .

    4. Perform steps 2 and 1 in reverse.
The first step consists of at most d + 2 queries (two queries to obtain d(u) and d′ (u) and at most
d queries to obtain the vertices wi and wi′ ) and some simple operations between queries, to keep
count of vertices wi or wi′ that are being queried.
    For the second step, let Hj be the register holding the value of wj obtained in the first step.
For each j ∈ {1, . . . , din }, we perform a unitary Uj on Hj ⊗ H2 ⊗ H3 that maps |wj i |wj i |0i to
|wj i |0i |ji. This can be done as follows:
    1. Perform |xi |yi → |xi |x ⊕ yi on Hj ⊗ H2 where ⊕ denotes bitwise XOR.

    2. Conditional on the second register being |0i, add j to the third register.

   3. Conditional on the third register not being |ji, perform |xi |yi → |xi |x ⊕ yi on Hj ⊗ H2 to
      reverse the first step.
                                                       E     E            E
We then perform similar unitaries Udin +j that map wj′ wj′ |0i to wj′ |0i |din + ji and, if u = v1 ,
we also perform a unitary Udin +dout +1 that maps |vV +1 i |0i to |0i |din + dout + 1i. Each of these
unitaries requires O(log V ) quantum gates and there are O(d) of them. Thus, the overall complexity
is O(d log V ).
    The third step is a unitary D on H3 that depends on din + dout and on whether we have u = v1 .
We can express D as D = Uψ (I − 2 |0i h0|)Uψ−1 where Uψ is any transformation with Uψ |0i = |ψi.

                                                     13
Both Uψ and I − 2 |0i h0| are simple transformations on a ⌈log(d + 2)⌉ qubit register H3 which can
be performed with O(log d) gates.
    Since there are d possible values for din + dout and 2 possibilities for whether u = v1 , we can
try all possibilities one after another, checking the conditions and then performing the required
unitary, if necessary, with O(d log d) gates. Checking u = v1 requires O(log V ) gates.
    The fourth step is the reverse of the first two steps and can be performed with the same
complexity.
    The overall complexity is O(d) queries and O(d log V ) quantum gates. The transformation RB
can be performed with a similar complexity in a similar way.


6     Analysis of algorithm for DAG size estimation
This section is devoted to the analysis of Algorithm 1.

6.1    Spectral theorem
Our bounds on eigenvalues of RB RA are based on the spectral theorem from [15].
   Suppose that X is a subspace of a Hilbert space H. Let ref X denote a reflection which leaves
X invariant and negates all vectors in X ⊥ .
   Let Gram(w1 , . . . , wk ) stand for the Gram matrix of vectors w1 , . . . , wk , i.e., the matrix formed
by the inner products hws , wt i.

Definition 11 ([15, Definition 5]). Let ({w1 , . . . , wk } , {w̃1 , . . . , w̃l }) be an ordered pair of orthonor-
mal systems. The discriminant matrix of this pair is

                                  M = Gram(w1 , . . . , wk , w̃1 , . . . , w̃l ) − I.

   Let A and B be two subspaces of the same Hilbert space H. Suppose that A is spanned by
an orthonormal basis w1 , . . . , wk and B is spanned by an orthonormal basis w̃1 , . . . , w̃l . Let M be
the discriminant matrix of ({w1 , . . . , wk } , {w̃1 , . . . , w̃l }). The spectral theorem from [15] provides
spectral decomposition for the operator ref B ref A restricted to A+B = (A⊥ ∩B ⊥ )⊥ ; on the subspace
A⊥ ∩ B ⊥ (called the idle subspace in [15]) ref B ref A acts as the identity.

Theorem 12 ([15, Spectral Theorem]). ref B ref A has the following eigenvalues on A + B:

    • eigenvalue 1, with eigenvectors being all vectors in A ∩ B; the space has the same dimension
      as the eigenspace of M associated to the eigenvalue 1.
                              √                                                  E √          E
    • eigenvalue 2λ2 −1∓2iλ 1 − λ2 , with corresponding eigenvectors |ãi − λ b̃ ±i 1 − λ2 b̃ ,
      where (a, b) is an eigenvector of M with eigenvalue λ ∈ (0, 1) and
                                                   k
                                                   X                 E   l
                                                                         X
                                         |ãi :=         ai wi ,   b̃ :=   bj w̃j .
                                                   i=1                   j=1

                                                                           E
    • eigenvalue −1, with eigenvectors being all vectors in form |ãi or b̃ , where (a, b) is an eigen-
      vector of M with eigenvalue 0.

                                                            14
    Since
                     ref A⊥ = −ref A ,        ref B⊥ = −ref B ,                  ref B⊥ ref A⊥ = ref B ref A ,
we can restrict the operator ref B⊥ ref A⊥ on A + B and obtain its spectral decomposition in terms
of the discriminant matrix of the pair ({w1 , . . . , wk } , {w̃1 , . . . , w̃l }) (instead of forming the discrim-
inant matrix of the orthogonal systems spanning A⊥ and B ⊥ ).

6.2    1-eigenvectors of RB RA
In our setting RB = ref H⊥ and RA = ref H⊥ .
                             B                        A
                                                                                           ⊥ ∩ H⊥
   From the spectral theorem it follows that all 1-eigenvectors of RB RA belong to either HA    B
or HA ∩ HB . We start with characterizing these 1-eigenspaces as follows:
Lemma 13.                                                                         ⊥ ∩ H⊥ .
                   1. The starting state |eT +1 i is orthogonal to each state in HA    B

   2. dim (HA ∩ HB ) = 0.
Proof. The first claim can be restated as
                                                 ⊥
                                           ⊥    ⊥
                               |eT +1 i ∈ HA ∩ HB    = HA + HB .

To show that, notice that the following equality holds:
                                   X X             X X
                                            |ei =       |ei ,                                                           (2)
                                           v∈VA e∈E(v)                v∈VB e∈E(v)

since for every edge e ∈ E the state |ei is added both in the LHS and RHS of (2) exactly once: if e
connects a vertex u ∈ VA and a vertex
                                   P v ∈ V′ B (no edge can connect two vertices       from VA or from
VB ), then |ei appears in the sum e′ ∈E(u) |e i in the LHS and in the sum e′ ∈E(v) |e′ i in the RHS
                                                                            P

                               / {u, v}, |ei is not contained in the sum e′ ∈E(w) |e′ i).
                                                                         P
(and, for any other vertex w ∈
    Now from (2) we conclude that
                             X X              X X                        X                X
     |eT +1 i = |eT +1 i + α         |ei − α            |ei = |sv1 i + α       |sv i − α     |sv i ,
                            v∈VA e∈E(v)                v∈VB e∈E(v)                            v∈VA \{v1 }        v∈VB

i.e., |eT +1 i ∈ HA + HB as claimed.
     To show the second claim, suppose a vector |xi is contained both in HA and HB . Then |xi can
be expressed in two ways via the vectors |sv i, i.e., there are scalars ηi , i ∈ [V ], such that
                            A+B
                            X            X                 A
                                                           X           X
                                   ηi              |ei =         ηi              |ei + η1 α−1 |eT +1 i .                (3)
                           i=A+1        e∈E(vi )           i=1        e∈E(vi )

    Clearly, for any adjacent vertices vi ∼ vj we must have ηi = ηj , since the corresponding basis
state |ei (where e is the unique edge between vi and vj ) has coefficient ηi in the LHS of (3) (supposing
that vi is in VA ) and coefficient ηj in the RHS of (3). However, G is connected, therefore we must
have η1 = η2 = . . . = ηV . It remains to notice that η1 = 0, since the LHS of (3) is orthogonal to
|eT +1 i. We conclude that only the null vector belongs to the subspace HA ∩ HB .

    An immediate consequence of this Lemma is that all 1-eigenvectors |ψi of RB RA are orthogonal
to the starting state |eT +1 i.

                                                                 15
6.3   Eigenvalue closest to 1
The spectral decomposition for RB RA (restricted to HA +HB ) will be obtained from the discriminant
matrix of two orthonormal systems spanning HA and HB ; in (HA + HB )⊥ = HA      ⊥ ∩ H⊥ the operator
                                                                                     B
RB RA acts as the identity.
    From Theorem 12 and Lemma 13 it follows that the discriminant matrix does not have the
eigenvalue 1. Let λ ∈ (0, 1) be the maximal eigenvalue of the discriminant matrix and θ = 2 arccos λ,
then e±iθ is the eigenvalue of RB RA which is closest to 1.
    To describe the discriminant matrix, we introduce the following notation. We define a (T +1)×A
matrix Ma as follows:

   • the elements of the first column are defined by
                                                
                                                1,
                                                     ei ∈ E(v1 ),
                                                   −1
                                     Ma [i, 1] = α , i = T + 1,
                                                
                                                 0,   otherwise;
                                                


   • the elements of the j th column, j = 2, 3, . . . , A, are defined by
                                                     (
                                                        1, ei ∈ E(vj ),
                                       Ma [i, j] =
                                                        0, otherwise.

A (T + 1) × B matrix Mb is defined by
                                 (
                                   1, ei ∈ E(vA+j ),
                     Mb [i, j] =                                i ∈ [T + 1], j ∈ [B].
                                   0, otherwise,

Then HA and HB can be identified with the column spaces of Ma and Mb , respectively. Let a ∈ RA
and and b ∈ RB be vectors defined by
                 p                  p                             p
           a[1] = d1 + α−2 , a[j] = dj , j ∈ [2 .. A] and b[j] = dA+j , j ∈ [B].             (4)

By MA we denote the matrix Ma diag(a)−1 and by MB we denote the matrix Mb diag(b)−1 . Notice
that columns of MA and MB are orthonormal vectors. The corresponding vectors
         X                           svj                       X                           svA+j
                   MA [i, j] |ii =         , j ∈ [A],   and              MB [i, j] |ii =           , j ∈ [B]   (5)
                                     svj                                                   svA+j
        i∈[T +1]                                              i∈[T +1]

form orthonormal bases of HA and HB , respectively.
   Let L = MA∗ MB . Then the discriminant matrix of the pair of orthonormal systems spanning
HA and HB has the following block structure:
                                                   
                                         0A,A    L
                                                      .
                                          L∗ 0B,B

   It is easy to check that ( uv ) is an eigenvector of the discriminant matrix with an eigenvalue
λ > 0 iff u is a left-singular vector and v is the right-singular vector of L with singular value λ.

                                                         16
Therefore, if λL = cos 2θ is the largest singular value of L, then e±iθ are the eigenvalues of RB RA
that are closest to 1.
   Let K = (I − LL∗ )−1 and λK be the maximal eigenvalue of K. Since λL = cos θ2 < 1 is the
                                                            −1
maximal singular value of L, it holds that λK = 1 − λ2L         = sin−2 2θ is the maximal eigenvalue
of K. We show the following characterization of the entries of K:

Lemma 14. For all i, j ∈ [A] the following inequalities hold:

                            α2 a[i]a[j] ≤ K[i, j] ≤ α2 + n a[i]a[j].
                                                           


Moreover, when i = 1 or j = 1, we have K[i, j] = α2 a[i]a[j].

   Proof in Sections 6.5 - 6.8.
   Lemma 14 now allows to estimate the maximal eigenvalue of K:

Lemma 15. The entries K[i, j], i, j ∈ [A], satisfy

                          α2 di dj ≤ K[i, j] ≤ di dj α2 + n .
                              p                    p       
                                                                                                 (6)

Furthermore, λK , the maximal eigenvalue of K, satisfies

                                       α2 T ≤ λK ≤ (α2 + n)T.                                    (7)
                   √
Proof. Since a[i] = di for all i ∈ [2 .. A], inequalities (6) immediately follow from Lemma 14 when
i, j ≥ 2. Suppose                                                                           2
             p that i = 1 (since K is symmetric), then, again by Lemma 14, K[1, j] = α a[1]a[j].
Since a[j] ≥ dj for all j ∈ [A], the first inequality in (6) is obvious. It remains to show

                              α2 a[1]a[j] ≤       d1 dj α2 + n ,
                                              p               
                                                                       j ∈ [A].                  (8)
                                                 p
However, from the definition
                     p       of a we have αa[j] ≤ α2 dj + 1 for all j ∈ [A]. Hence the LHS of (8)
is upper-bounded by (α2 d1 + 1)(α2 dj + 1), which, in turn, is upper bounded by the RHS of (8).
This proves (6).
    Let K ′ be a symmetric A × A matrix, defined by K ′ [i, j] = di dj . Then (6) can be restated as
                                                                p


                       α2 K ′ [i, j] ≤ K[i, j] ≤ (α2 + n)K ′ [i, j],       i, j ∈ [A].

Now, from [7, Theorem 8.1.18] we have that

                                  λ(α2 K ′ ) ≤ λK ≤ λ (α2 + n)K ′ ,
                                                                 


where by λ(M ) we denote the spectral radius of a matrix M (the maximum absolute value of an
eigenvalue of M ), P
                   since λ K = λ(K).    On the other hand, K ′ is a rank-1 matrix, thus its spectral
                     A              A
radius is λ(K ′ ) = j=1 ( dj )2 = j=1 dj = T (on each side of the last equality every edge in E is
                         p        P
counted exactly once), hence

                       α2 T = λ(α2 K ′ ) ≤ λK ≤ λ (α2 + n)K ′ = (α2 + n)T.
                                                              




                                                     17
6.4    Phase estimation for θ
We now show that Lemma 15 implies Lemmas 4 and 5.
    Let u be the left-singular vector and v be the right-singular vector of L corresponding to the
largest singular value λL . By Theorem 12, the corresponding eigenvectors of RB RA are
                                          1                         λL         E   i  E
                        |Ψ± i = q                    |ãi − q                b̃ ∓ √ b̃ ,
                                      2(1 − λ2L )                 2(1 − λ2 )        2
                                                                           L
                    E
where |ãi ∈ HA , b̃ ∈ HB are the unit vectors associated to MA u and MB v, i.e.,

                                       A                               B
                                                                      X svA+j
                                      X   svj                      E
                             |ãi =           u[j],              b̃ =           v[j].
                                      j=1
                                          svj                         j=1
                                                                          svA+j

   The two-dimensional plane Π = span {|Ψ+ i , |Ψ− i} is also spanned by
                                     E                       1                   λL          E
                           |q1 i = b̃ ,       |q2 i = q               |ãi − q             b̃ .    (9)
                                                            1 − λ2L              1 − λ2L

We claim that
                     √
Lemma 4. If α ≥       2n, we have
                                                                      2
                                                    heT +1 |q2 i ≥
                                                                      3
for the state |q2 i ∈ span {|Ψ+ i , |Ψ− i}, defined by (9).
                                                 E
Proof. Since |eT +1 i ⊥ HB , we have heT +1 b̃ = 0 and

                                                1                          p
                          heT +1 |q2 i = q                 heT +1 |ãi =       λK heT +1 |ãi .
                                               1 − λ2L

Since heT +1 svj = 0 unless j = 1, we have

                                              A
                                              X heT +1 svj                    u[1]
                            heT +1 |ãi =                           u[j] = √          .
                                              j=1
                                                           svj              1 + α2 d1

Consequently,                                                 √
                                                         u[1] λK
                                          heT +1 |q2 i = √           .                            (10)
                                                           1 + α2 d1
We now lower bound this expression. Since u is an eigenvector of K, we have
                                                    A
                                                    X
                                      λK u[i] =           u[j]K[i, j],     i ∈ [A].
                                                    j=1




                                                            18
From (6) it follows that
                                                             
                                             p     A
                                                   X
                           λK u[i] ≤ (α2 + n) di 
                                                     p
                                                       dj u[j] ,                      i ∈ [A].
                                                             j=1

             PA p
Denote µ =     j=1   dj u[j]; then the previous inequality can be rewritten as

                                                     α2 + n p
                                      u[i] ≤ µ ·              di ,        i ∈ [A].
                                                      λK
On the other hand, u is a unit vector, thus
                            A                                   A
                                                             2 X                              2
                                                    α2 + n                            α2 + n
                            X                                                    
                       1=         u2 [i] ≤ µ2                           di = µ2                     T.
                                                     λK                                λK
                            i=1                                   i=1

Now we conclude that
                                                           λK
                                                µ≥            √ .
                                                         2
                                                       (α + n) T
                                                            √
    From Lemma 14 it follows that K[1, j] = α2 a[1]a[j] ≥ α2 d1 + α−2 dj for all j ∈ [A]. That
                                                                     p

allows to estimate the RHS of the equation
                                                             A
                                                       1 X
                                            u[1] =         u[j]K[1, j]
                                                      λK
                                                           j=1

more precisely:
                      √         A               √                  √
                    α2 d1 + α−2 X p           α2 d1 + α−2     α2    α2 d1 + 1
             u[1] ≥                 dj u[j] =             µ≥ 2   ·    √       .
                        λK                        λK        α +n     α T
                                      j=1

                                             √      √
Combining this with (10) and the estimate λK ≥ α T (which follows from (7)) yields
                                         √
                                    u[1] λK        α2       n       2
                     heT +1 |q2 i = √          ≥  2
                                                      =1− 2     ≥ ,
                                           2
                                      1 + α d1   α +n    α +n       3

which completes the proof.
                                                       √
Lemma 5. Suppose that δ ∈ (0, 1). Let α =                  2nδ−1 and θ̂ ∈ (0; π/2) satisfy

                                                                   δ1.5
                                                θ̂ − θ ≤           √    .
                                                                 24 3nT
Then
                                                             1
                                      (1 − δ)T ≤                    ≤ (1 + δ)T.
                                                      α2 sin2 θ̂2
Proof. We start with


                                                            19
Lemma 16. Suppose that θ̂ ∈ (0; π/2) satisfies
                                                                  θ
                                                 θ − θ̂ ≤ ǫ sin
                                                                  2
for some ǫ ∈ (0, 1). Then
                                         1               1        6ǫ
                                                  −       2 θ
                                                              ≤         .
                                      sin2 2θ̂        sin 2     sin2 θ2

Proof. Let σ = sin θ2 , then θ − θ̂ ≤ ǫσ and we have to show that

                                             1             1     6ǫ
                                                    −       2 θ
                                                                ≤ 2.
                                         sin2 θ̂2       sin 2    σ

   Since the sin function is Lipschitz continuous with Lipschitz constant 1, we have

                                                  θ̂       θ   ǫσ
                                           sin       − sin   ≤
                                                  2        2    2

and σ 1 − 2ǫ ≤ sin 2θ̂ ≤ σ 1 + 2ǫ . On the other hand,
                                

                                                        (            )
        θ̂      θ      θ̂     θ    θ̂     θ   ǫσ            θ̂     θ        ǫ 2
    sin2 − sin2   = sin − sin   sin + sin   ≤    · 2 max sin , sin     ≤ǫ 1+   σ .
        2       2      2      2    2      2    2            2      2         2

We conclude that

                             sin2 2θ̂ − sin2 θ2     ǫ 1 + 2ǫ σ 2
                                                            
           1          1                                               ǫ(1 + ǫ/2)     6ǫ
                 −     2 θ
                           =                    ≤ 4           2
                                                                  ≤ 2          2
                                                                                    < 2,
            2 θ̂
         sin 2     sin 2         2  θ̂
                              sin 2 · sin 22 θ   σ (1 − ǫ + ǫ /4)  σ (1 − ǫ + ǫ /4)  σ

where the last inequality is due to 2x(1 + x)/(1 − x)2 < 12x, which is valid for all x ∈ (0, 1/2), and,
in particular, for x = ǫ/2.

   From Lemma 15 it follows that σ := sin 2θ satisfies

                                      α2 T ≤ σ −2 ≤ (α2 + n)T.                                          (11)

Notice that
                                     r                         r
                    δ1.5    δ            δ    1     δ               δ    1        δ
          θ − θ̂ ≤ √     =    ·            ·√    <    ·                ·√    = q       .
                  24 3nT   24            3    nT   24              2+δ    nT  24 2n
                                                                                    +n T
                                                                                     δ


Since 2n    2
       δ = α , the RHS of the last equality is upper-bounded by (11) as
                                                                                 √ δ2              ≤ δσ
                                                                                                     24 . An
                                                                                24       (α +n)T
application of Lemma 16 (with ǫ = δ/24 < 1) now gives

                                             1                    δσ −2
                                                      − σ −2 ≤
                                         sin2 2θ̂                   4

                                                        20
or                                                                  
                                            δ        1               δ
                                   σ −2 1 −     ≤         ≤ σ −2 1 +     .
                                            4     sin2 θ̂            4
                                                                    2
From (11) it follows that
                                                                                  
                                       δ                     1                   δ
                                  1−           α2 T ≤               ≤       1+           (α2 + n)T.
                                       4                 sin2 θ̂2                4

Consequently,
                                                                                 
                    δ                  1                   δ          n       δ       δ
                 1−         T ≤                 ≤       1+         1+ 2 T = 1+      1+     T.
                    4             α2 sin2 2θ̂              4         α         4       2

It remains to notice that
                                                                        δ2
                                                          
                                           δ             δ          3
                                      1+            1+           =1+ δ+    < 1 + δ.
                                           4             2          4   8
Hence                                            
                                              δ                     1
                                           1−         T ≤                   ≤ (1 + δ) T,
                                              4              α2 sin2 2θ̂
and the claim follows.


6.5     Harmonic functions and electric networks
The next five subsections are devoted to the proof of Lemma 15. We start with the concept of
harmonic functions which is linked to the connection between electric networks and random walks.
More details on the subject can be found in [10, Sec. 4] (in the case of a simple random walk which
is the framework we use below), [8, Lect. 9], [11, Chap. 2] and [9, Chap. 9] (in a more general
setting with weighted graphs).
    Throughout the rest of this subsection suppose that P is a transition matrix of an irreducible
Markov chain with a state space Ω.

Definition 17. Consider a function f : Ω → R. We say that f is harmonic for P at x ∈ Ω (or
simply “harmonic at x”) if [9, Eq. 1.28]
                                              X
                                      f (x) =   P[x, y]f (y),
                                                             y∈Ω

i.e., f has the averaging property at x. If f is harmonic for every x ∈ Ω′ ⊂ Ω, then f is said to be
harmonic on the subset Ω′ .

    It can be easily seen that a linear combination of harmonic functions is still harmonic. In
particular, all constant functions are harmonic on Ω.
    It is known that a harmonic (on Ω′ ) function attains its maximal and minimal values (in the
set Ω) on Ω \ Ω′ (it appears as an exercise in [9, Exercise 1.12]; in the context of weighted random
walks it can be found in [13, Lemma 3.1]).

                                                                 21
Lemma 18 (Maximum Principle). Let f be harmonic for P on Ω′ ⊂ Ω, with Ω \ Ω′ 6= ∅. Then
there exists x ∈ Ω \ Ω′ s.t. f (x) ≥ f (y) for all y ∈ Ω′ .

    By applying the Maximum Principle for −f , one obtains a similar statement for the minimal
values of f . In particular, if the function f is harmonic on Ω′ and constant on the set Ω \ Ω′ , then
f is constant. A consequence of this is the Uniqueness Principle: if f and g are harmonic on Ω′
and f ≡ g on Ω \ Ω′ , then f ≡ g on Ω. Moreover, when f is harmonic everywhere on Ω, it is a
constant function.
    Further, suppose that P is a simple random walk on a finite connected undirected graph G =
(Ω, E), in the sense that
                                       1{x∼y}
                           P[x, y] =            ,    d(x) := {y ∈ Ω x ∼ y} ,
                                        d(x)

where 1 stands for the indicator function. Then the Markov chain, corresponding to P, is time-
reversible; the graph G can be viewed as an electric network where each edge has unit conductance
(this approach can be further generalized to weighted graphs where the weight c(e) of an edge e ∈ E
is referred to as conductance in the electric network theory, whereas its reciprocal r(e) = c(e)−1 is
called resistance).
    For a subset Ω′ ⊂ Ω we call the set {x ∈ Ω \ Ω′ ∃y ∈ Ω′ : x ∼ y} the boundary of Ω′ and denote
by ∂Ω′ . The Maximum Principle can be strengthened as follows:

Lemma 18’. Let f be harmonic for P on Ω′ ⊂ Ω, with ∂Ω′ 6= ∅. Then there exists x ∈ ∂Ω′ s.t.
f (x) ≥ f (y) for all y ∈ Ω′ .

   Similarly,

   • if the function f is harmonic on Ω′ and constant on the boundary ∂Ω′ (for example, when
     the boundary is a singleton), then f is constant on Ω′ ∪ ∂Ω′ .

   • if f and g are harmonic on Ω′ and f ≡ g on ∂Ω′ , then f ≡ g on Ω′ ∪ ∂Ω′ .

   Let s, t ∈ Ω be two different vertices of the graph G and consider the unique function φst : Ω → R,
which

   • is harmonic on Ω \ {s, t},

   • satisfies boundary conditions φst (s) = 1, φst (t) = 0.

From the Maximum Principle it follows that values of φst are between 0 and 1. In the electric
network theory, the function φst (u), u ∈ Ω, is interpreted as the voltage of u, if we put current
through the electric network associated to G, where the voltage of s is 1 and the voltage of t is 0
(see [10, p. 22] or [8, p. 60]; in the latter φst is denoted by Ṽ ). For the random walk with the
transition matrix P, the value φst (u) is the probability that the random walk starting at u visits s
before t.
    Consider the quantity
                                                            !−1
                                                X
                                      Rst =          φst (u)    .
                                                    u:u∼t



                                                       22
The electrical connection is that this quantity, called the effective resistance (or simply resistance
between s and t in [10]), is the voltage difference that would result between s and t if one unit of
current was driven between them. On the other hand, it is linked to the “escape probabilities”,
because (d(t)Rst )−1 is the probability that a random walk, starting at t, visits s before returning
back to t [8, p. 61].
    An important result is the Rayleigh’s Monotonicity Law [9, Theorem 9.12], from which it
follows that adding edges in the graph cannot increase the effective resistance [10, Corollary 4.3],
[9, Corollary 9.13]. More precisely, if we add another edge in G, obtaining a graph G ′ = (Ω, E ′ ),
and denote by Rst  ′ the effective resistance between vertices s and t, then R ≥ R′ .
                                                                                  st      st
    More generally, if we consider the same graph G, but with different weights (or conductances)
c(x, y) and c′ (x, y), satisfying c(x, y) ≤ c′ (x, y) for all x, y ∈ Ω, then the Monotonicity Law says
that the effective resistances satisfy the opposite inequality Rst ≥ Rst   ′ for all distinct s, t ∈ Ω.

    We can view adding an edge as increasing its weight from 0 to 1, hence the claim about edge
adding.

6.6   Extended DAG and an absorbing random walk
Let G and G ′ be as defined in Section 3.2. In this Section, we define an absorbing random walk on
G ′′ , a slightly extended version of G ′ .                                                    −1
      Let Γ denote the adjacency matrix of the weighted graph G ′ . We denote β = d1 α2 + 1 .
      We introduce another vertex vV +2 and connect the vertex vV +1 with an edge eT +2 = (vV +2 , vV +1 ).
Let V′′ = V′ ∪ {vV +2 }, E′′ = E′ ∪ {eT +2 } and G ′′ = (V′′ , E′′ ).
      Finally, let all edges in the original DAG G have weight 1, but the two additional edges have
the following weights:

   • the edge eT +1 has weight α−2 ;

   • the edge eT +2 has weight d1 .

    For any two vertices vi , vj , i, j ∈ [V + 2], we denote vi ∼ vj if there is an edge between vi and vj
in the DAG G ′′ . For each i ∈ [V + 2] we denote by d′′ (i) the degree of the vertex vi in the weighted
graph G ′′ . Then

   • d′′ (1) = d′′ (V + 1) = d1 + α−2 ;

   • d′′ (i) for each i ∈ [2 .. V ] equals di , i.e., the degree of vi in the unweighted graph G;

   • d′′ (V + 2) = d1 .

Notice that                   p                                    p
                     a[i] =       d′′ (i), i ∈ [A],   and b[j] =       d′′ (A + j), j ∈ [B],
for vectors a and b defined with (4).
    Consider a random walk on the graph G ′′ with transition probabilities as follows:

   • when at the vertex vV +2 , with probability 1 stay at vV +2 ;

   • when at the vertex vV +1 , with probability 1 − β move to vV +2 and with probability β move
     to v1 ;


                                                        23
   • when at the vertex v1 , with probability β move to vV +1 and with probability 1−β  d1 = βα
                                                                                               2

     move to any v ∈ E(v1 ) (i.e., to any neighbor of the root, different from vV +1 );

   • at any vertex vi , i ∈ [2 .. V ], with probability d′′1(i) move to any neighbor of vi .
In other words, at any vertex we move to any its neighbors with probability proportional to the
weight of the edge, except for the vertex vV +2 , where we stay with probability 1. Moreover, this
random walk ignores edge direction, i.e., we can go from a vertex of depth l to a vertex of depth
l − 1.
    This way an absorbing random walk is defined; let {Yk }∞  k=0 be the corresponding sequence of
random variables, where Yk = j ∈ [V + 2] if after k steps the random walk is at the vertex vj (i.e.,
this sequence is the Markov chain, associated to the absorbing random walk).
    Let P be the transition matrix for this walk; it has the following block structure:
                                                                  
                                                               0
                                    
                                                              0  
                                            Q                 0 
                               P =                                  ,
                                                                  
                                                               .. 
                                    
                                                               . 
                                                            1 − β
                                      0 0 0 0 ... 0            1

where Q is a matrix of size (V + 1) × (V + 1) which describes the probability of moving from some
transient vertex to another.
   Define a (V + 1) × 1 vector d as follows:
                            p                                    p
              d[i] = a[i] = d′′ (i), i ∈ [A], d[A + j] = b[j] = d′′ (A + j), j ∈ [B],

and d[V + 1] = d′′ (V + 1) = d[1]. Then diag(d)2 Q is the adjacency matrix Γ for the graph G ′ .
                p

   Let
                           N = IV +1 + Q + Q2 + Q3 + . . . = (IV +1 − Q)−1
be the fundamental matrix of this walk. An entry of the fundamental matrix N [i, j], i, j ∈ [V + 1],
equals the expected expected number of visits to the vertex j starting from the vertex i, before
being absorbed, i.e.,                       "∞                #
                               N [i, j] = E    1{Yk =j} Y0 = i .
                                             X

                                                       k=0

   Notice that N Q = QN = Q + Q2 + Q3 + . . . = N − I                   V +1 . It follows that

                       VX
                        +1                             VX
                                                        +1
          N [i, j] =         N [i, l]Q[l, j] + δij =         Q[i, l]N [l, j] + δij   for all i, j ∈ [V + 1],   (12)
                       l=1                             l=1

where by δij we denote the Kronecker symbol.

6.7   Entries of the fundamental matrix
The purpose of this section is to obtain expressions for entries of the fundamental matrix N . In
the next subsection, we will relate those entries to entries of the matrix K from Lemma 15. This
will allow us to complete the proof of Lemma 15.

                                                             24
Lemma 19.
                                                                       1                          1
            N [1, V + 1] = N [V + 1, 1] = N [V + 1, V + 1] =              ,      N [1, 1] =            .
                                                                      1−β                     β(1 − β)
Proof. We have                                      "∞                                  #
                        N [V + 1, V + 1] = E               1{Yk =V +1} Y0 = V + 1 .
                                                     X

                                                     k=0
Notice that
                           ∞                       ∞
                                 1{Yk =V +1} =           1{Yk =V +1 and Yk+1 =1} + 1,
                           X                       X

                           k=0                     k=0
since from the vertex vV +1 one either moves to vV +2 and gets absorbed or moves to v1 and returns
back to vV +1 later. From the linearity of expectation it follows that
                                             ∞
                                                   E 1{Yk =V +1 and Yk+1 =1} Y0 = V + 1
                                             X                                                
                  N [V + 1, V + 1] = 1 +
                                             k=0
                                             ∞
                                                   P [Yk = V + 1, Yk+1 = 1 Y0 = V + 1] .
                                             X
                                      =1+
                                             k=0

Since

              P [Yk = V + 1, Yk+1 = 1 Y0 = V + 1]
              = P [Yk+1 = V + 1 Yk = V + 1, Y0 = V + 1] · P [Yk = V + 1 Y0 = V + 1]
              = P [Yk+1 = V + 1 Yk = V + 1] · P [Yk = V + 1 Y0 = V + 1]
              = Q[V + 1, 1] P [Yk = V + 1 Y0 = V + 1] ,

we obtain
                                                     ∞
                                                           P [Yk = V + 1 Y0 = V + 1] .
                                                     X
                      N [V + 1, V + 1] = 1 + β
                                                     k=0
On the other hand,
                                                                       ∞
                               "∞                                 #
        N [V + 1, V + 1] = E          1{Yk =V +1} Y0 = V + 1 =               P [Yk = V + 1 Y0 = V + 1] ,
                                X                                      X

                                k=0                                    k=0

hence
                                N [V + 1, V + 1] = 1 + βN [V + 1, V + 1],
from which the equality N [V + 1, V + 1] = (1 − β)−1 follows.
   From (12) it follows that
                               VX
                                +1                                     VX
                                                                        +1
         N [V + 1, V + 1] =          Q[V + 1, l]N [l, V + 1] + 1 =           N [V + 1, l]Q[l, V + 1] + 1.
                               l=1                                     l=1

Since Q[l, V + 1] and Q[V + 1, l] is nonzero only for l = 1, we have

                      N [V + 1, V + 1] = βN [1, V + 1] + 1 = βN [V + 1, 1] + 1.

                                                          25
From that we conclude
                                                                   1                           1
                         N [V + 1, 1] = N [1, V + 1] =               (N [V + 1, V + 1] − 1) =     .
                                                                   β                          1−β
   Finally, again from (12) we obtain
                                                        V
                                                        X +1
                                  N [V + 1, 1] =               Q[V + 1, l]N [l, 1] = βN [1, 1],
                                                        l=1

thus N [1, 1] = (β(1 − β))−1 .

   Define the matrix Ñ = N diag(d)−2 , then

                                                            N [i, j]
                                              Ñ [i, j] =            ,   i, j ∈ [V + 1].
                                                            d′′ (j)

We note that Ñ is a symmetric matrix, since
                                                                                                         −1
                           Ñ = (IV +1 − Q)−1 diag(d)−2 = diag(d)2 − diag(d)2 Q

and diag(d)2 Q is symmetric. Moreover, from the symmetry we also have d′′ (l)Q[l, j] = d′′ (j)Q[j, l]
for j, l ∈ [V + 1]. Then, since
                     V
                     X +1                         VX
                                                   +1                              V
                                                                                   X +1
                            N [i, l]Q[l, j] =           Ñ[i, l]d′′ (l)Q[l, j] =          Ñ [i, l]Q[j, l]d′′ (j),
                     l=1                          l=1                              l=1

we can rewrite (12) as
                   VX
                    +1                                      V +1
                                               δij    X                    δij
     Ñ [i, j] =         Ñ [i, l]Q[j, l] +    ′′
                                                    =   Q[i, l]Ñ [l, j] + ′′                    for all i, j ∈ [V + 1].   (13)
                                              d (j)                       d (j)
                   l=1                                      l=1

It follows that for all i ∈ [V + 1], the function fi : [V + 1] → R defined by

                                        fi (l) = Ñ [i, l] = Ñ [l, i],      l ∈ [V + 1],

is harmonic on the set [V ] \ {i} (the function is well defined, since Ñ [i, l] = Ñ [l, i] due to the
symmetry of Ñ).
    In particular, fV +1 is harmonic on the set [V ], whose boundary is the singleton {V + 1}. Hence
fV +1 is a constant function. Similarly, f1 is constant on [V ], because it is harmonic on [2 .. V ],
whose boundary is the singleton {1}.

Corollary 1. For all i ∈ [V + 1] we have
                                                                                      1
                                               Ñ [i, V + 1] = N [V + 1, i] =
                                                                                      d1
and for all i ∈ [V ] we have
                                                                                   1
                                                 Ñ [i, 1] = N [1, i] = α2 +          .
                                                                                   d1

                                                                   26
Proof. We already concluded that fV +1 is a constant function, i.e., the value

                                  fV +1 (j) = Ñ [V + 1, j] = Ñ [j, V + 1]

does not depend on j. By Lemma 19,

                                      1                            1      d1 α2 + 1  1
            Ñ [V + 1, V + 1] =    ′′
                                            N [V + 1, V + 1] =       −2
                                                                        ·       2
                                                                                    = ,
                                  d (V + 1)                    d1 + α       d1 α     d1
and the first claim follows.
   The other claim follows from the fact that f1 is constant on [V ] and
                                                                    2
                                1                   1      d1 α2 + 1         1
                   f1 (1) =       −2
                                     N [1, 1] =       −2
                                                         ·        2
                                                                       = α2 + .
                            d1 + α              d1 + α        d1 α           d1


   It remains to describe the values of Ñ [i, j] when 2 ≤ i, j ≤ V . For each i ∈ [2 .. V ] define φi to
be the unique function which
   • is harmonic on [2 .. V ] \ {i},

   • satisfies φ(1) = 1, φ(i) = 0.
Let R : [2 .. V ] → R be defined by
                                                                  −1
                                                     X
                                        R(i) =                φi (j)    .
                                                    j:vj ∼vi

Lemma 20. For all i ∈ [2 .. V ], j ∈ [V ], it holds that
                                                    1
                                  Ñ[i, j] = α2 +      + (1 − φi (j)) R(i).
                                                    d1
Proof. Fix i ∈ [2 .. V ]. Let m = fi (1) (we already have m = α2 + d1 −1 ) and M = fi (i) − m (M
to be described). Then fi is the unique function which is harmonic on [2 .. V ] \ {i} and satisfies
the boundary conditions fi (1) = m, fi (i) = m + M . Clearly, 0 6= M , since otherwise fi must be a
constant (and therefore harmonic) function, but from (13) it follows that fi is not harmonic at i.
   Define
                                          1
                                  g(j) =     (fi (j) − m) , j ∈ [V ].
                                          M
Then g is harmonic on [2 .. V ] \ {i} and satisfies the boundary conditions g(1) = 0, g(i) = 1. By
the Uniqueness Principle, g ≡ 1 − φi , since 1 − φi satisfies the same conditions. Hence

                                  fi (j) = m + M (1 − φi (j)) ,          j ∈ [V ].

From (13) we have
                                                                  
                      1       X                    1        X
            fi (i) = ′′     1+   fi (j) = m + M + ′′ 1 − M   φi (j) .
                    d (i)                         d (i)
                                  j:vj ∼vi                                           j:vj ∼vi


                                                       27
On the other hand, fi (i) = m + M . Taking into account the definition of R(i), we have
                                                                 
                                                    1         M
                              m + M = m + M + ′′          1−
                                                  d (i)      R(i)

or M = R(i), which concludes the proof.

Lemma 21. Suppose that the original graph G is a tree. For all vertices vi , vj ∈ V, let ℓ(i, j) be
the distance from the lowest common ancestor of vi , vj to the root v1 .
    Then for all i, j ∈ [V ] it holds that
                                                         1
                                      Ñ [i, j] = α2 +      + ℓ(i, j).
                                                         d1
Proof. For i = 1 the claim follows from Corollary 1. Let i ∈ [2 .. V ], then from Lemma 20 we have
                                            1
                            fi (j) = α2 +      + (1 − φi (j))R(i),         j ∈ [V ].
                                            d1
Let us show that
                                                   ℓ(i, j)
                                    φi (j) = 1 −           ,   j ∈ [V ].                           (14)
                                                    ℓ(i)
and
                                               R(i) = ℓ(i).                                        (15)
    In (14) the boundary conditions φi (1) = 1, φi (i) = 0 are satisfied. By the Uniqueness Principle
it remains to show that the right-hand side of (14) defines a harmonic function in j on [2 .. V ] \ {i}.
Equivalently, we must show that ℓ(i, ·) is harmonic on [2 .. V ] \ {i}.
    Fix any j ∈ [2 .. V ] \ {i}. There are two cases to consider:

   • The vertex vj is not on the path from the root to vi ; then the lowest common ancestor of vi
     and vj coincides with the lowest common ancestor of vi and the parent of vj or the lowest
     common ancestor of vi and any child of vj ; hence ℓ(i, j) = ℓ(i, k) for all vertices vk , adjacent
     to vj .

   • The vertex vj is on the path from the root to vi . Let vp be the parent of vj and vc be the
     unique child of vj which also is on the path from the root to vi . Then for each vertex vk ∼ vj
     we have                                
                                            ℓ(i, j),
                                                          k∈/ {p, c} ,
                                   ℓ(i, k) = ℓ(i, j) + 1, k = c,
                                            
                                              ℓ(i, j) − 1, k = p.
                                            

In both cases we obtain
                                            X ℓ(i, k)
                                                      = ℓ(i, j),
                                              d′′ (j)
                                        k:vk ∼vj

i.e., ℓ(i, ·) (and thus also 1 − ℓ(i,·)
                                  ℓ(i) ) is harmonic at every j ∈ [2 .. V ] \ {i}. We conclude that (14)
holds.



                                                    28
   It remains to show (15). From the definition of R,
                                  X                        1 X
                        R(i)−1 =       φi (j) = d′′ (i) −      ℓ(i, j).
                                                          ℓ(i)
                                         j:vj ∼vi                       j:vj ∼vi

On the other hand, for every vertex vj ∼ vi we have
                                     (
                                       ℓ(i) − 1, vj is the parent of vi ,
                           ℓ(i, j) =
                                       ℓ(i),     vj is a child of vi .
Thus                      X
                                    ℓ(i, j) = d′′ (i)ℓ(i) − 1 and   R(i)−1 = ℓ(i)−1 .
                         j:vj ∼vi

Now, by combining (14) and (15) with Lemma 20, we obtain the desired equality.
  Remark. For another argument why R(i) = ℓ(i), see [9, Exercise 9.7].
Corollary 2. Suppose that G is an arbitrary DAG satisfying the initial assumptions.
  Then for all i, j ∈ [V ] we have
                                                     
                                                2  1
                                   Ñ [i, j] − α +      ≤ ℓ(i).
                                                   d1
In particular,                                                     
                                                            21
                                         0 ≤ Ñ [i, j] − α +            ≤n
                                                             d1
for all i, j ∈ [V ]. Moreover, when i = 1 or j = 1, the equality Ñ [i, j] = α2 + d11 holds.
Proof. When i = 1 or j = 1, the assertion holds (Lemma 1). Suppose that i > 1. Since Ñ [i, ·]
is harmonic on [2 .. V ] \ {i}, it attains its extreme values on the boundary {1, i}, i.e., it suffices to
show the inequality for j = i. In view of Lemma 20, this becomes R(i) ≤ ℓ(i).
     Let T be any spanning tree of G s.t. the shortest path between vi and the root is preserved,
i.e., distance from vi to v1 is still ℓ(i). By replacing G with T , the value of R(i) can only increase,
since replacing G with T corresponds to deleting edges in G and this operation, by Rayleigh’s
Monotonicity Law, can only increase the effective resistance R(i). However, Lemma 21 ensures
that for the tree T the value of R(i) equals ℓ(i). Thus in the graph G the value R(i) is upper-
bounded by ℓ(i) ≤ n.

6.8    Entries of the matrix K
Now we shall describe the matrix K, where K, L, Ma , Mb , a and b are defined as in Section 6.1.
The adjacency matrix Γ of the graph G ′ has the following block structure:
                                        0A,A H        α−2 e
                                                            
                                                            
                                          ∗
                                Γ= H                        ,
                                                            
                                                   0B+1,B+1 
                                       α−2 e∗
where H is a matrix of size A × B and e stands for the column vector of length A, whose first entry
is 1 and the remaining entries are 0.
    We claim that

                                                       29
Lemma 22.
                                              H = Ma∗ Mb .

Proof. We have to show that for every i ∈ [A], j ∈ [A + 1 .. V ] it holds that
                                           X
                                Γ[i, j] =        Ma [e, i]Mb [e, j].                                    (16)
                                              e∈[T +1]

Notice that Γ[i, j] = 0 unless vi ∼ vj (in that case Γ[i, j] = 1 for i ∈ [A], j ∈ [A + 1 .. V ]). On the
other hand, both Ma [e, i] and Mb [e, j] are simultaneously nonzero iff the edge e is incident both to
vi and vj .
    There are two cases to consider:

  1. vi ∼ vj ; then Γ[i, j] = 1 and there is a unique edge e ∈ [T +1] s.t. Ma [e, i] 6= 0 and Mb [e, j] 6= 0.
     Since i ∈ [A], j ∈ [A + 1 .. V ], we have Ma [e, i] = Mb [e, j] = 1 and (16) holds.

  2. vi 6∼ vj ; then Γ[i, j] = 0 and for each edge e ∈ [T + 1] either Ma [e, i] = 0 or Mb [e, j] = 0.
     Again, (16) holds.



   Denote
                           D = diag(d)−1 Γ diag(d)−1 = diag(d)Q diag(d),
then D has the following block structure:
                                                        
                                           0A,A    L̃
                                       D=                  ,
                                            L̃∗ 0B+1,B+1
                                                                               
where L̃ is an A × (B + 1) matrix with the following block structure: L̃ = L βe . This follows
from the fact that d has the following block structure:
                                                     
                                                   a
                                           d =  b ,
                                                 a[1]

and from the equalities

          L = diag(a)−1 Ma∗ Mb diag(b)−1 = diag(a)−1 H diag(b)−1          and β = (αa[1])−2 .

   Now we can show the following characterization of the matrix K = (IA − LL∗ )−1 :

Lemma 23. Let N stand for the leading A × A principal submatrix of Ñ , i.e., for the submatrix
of Ñ , formed by the rows indexed by [A] and columns indexed by [A]. Then

                                 K = diag(a) N − d−1
                                                        
                                                    1 J diag(a),

where J is the A × A all-ones matrix.




                                                     30
Proof. Since Q = diag(d)−1 D diag(d) and N = (IV +1 − Q)−1 , we have

                       (IV +1 − D)−1 = diag(d)N diag(d)−1 = diag(d)Ñ diag(d).               (17)

   By the block-wise inversion formulas [2, Proposition 2.8.7], (IV +1 − D)−1 has the following
block structure:
                                                  −1                  −1 
                                      I   − L̃ L̃ ∗       −  I   − L̃L̃ ∗    L̃
                                        A                      A
                 (IV +1 − D)−1 =                    −1                 −1  .
                                   −L̃∗ IA − L̃L̃∗          IB+1 − L̃∗ L̃

From (17) we conclude that
                                                   −1
                                       IA − L̃L̃∗         = diag(a)N diag(a).                (18)

   From the Sherman-Morrison formula [2, Fact 2.16.3] we have that for an invertible matrix W
and a column vector w s.t. 1 + w∗ W −1 w 6= 0 the inverse of the updated matrix W + ww∗ can be
computed as
                                                      W −1 ww∗ W −1
                            (W + ww∗ )−1 = W −1 −                   .
                                                      1 + w∗ W −1 w
Take W = IA − L̃L̃∗ and w = βe; then

   • L̃L̃∗ = LL∗ + β 2 ee∗ ;

   • ee∗ is a matrix of size A × A, whose only nonzero entry is 1 in the first row and column;

   • w∗ W −1 w = β 2 W −1 [1, 1] = β 2 d′′ (1)Ñ [1, 1] = d11α2 (by (18));
                      1
   • 1 + w∗ W −1 w = 1−β 6= 0;

   • IA − LL∗ = W + ww∗ .

We obtain                                        −1
                   K = (IA − LL∗ )−1 = IA − L̃L̃∗     IA − β 2 (1 − β)ee∗ W −1 .
                                                                              

Applying (18) yields
                                           K = diag(a)NU diag(a),
where

                           U := diag(a) IA − β 2 (1 − β)ee∗ W −1 diag(a)−1
                                                                

                               = IA − β 2 (1 − β)ee∗ diag(a)W −1 diag(a)−1
                               = IA − β 2 (1 − β)ee∗ diag(a)N
                               = IA − β 2 (1 − β)d′′ (1)ee∗ N.

Here we have used the fact that ee∗ and diag(a) commute and ee∗ diag(a)2 = d′′ (1)ee∗ . It follows
that
                               NU = N − β 2 (1 − β)d′′ (1)Nee∗ N.

                                                           31
   Furthermore, the row vector e∗ N equals the first row of N (and N is a symmetric matrix). All
elements of the first row of N are equal to α2 + d−1
                                                  1 , hence
                                                                         2
                                      (Ne) (e∗ N) = α2 + d−1
                                                          1                    J.

It is straightforward to check that

                         β(1 − β)d′′ (1) α2 + d−1
                                                  
                                               1    = 1,
                                                 −1 2
                          2         ′′     2
                                                      = β α2 + d−1   = d−1
                                                                  
                         β (1 − β)d (1) α + d1                  1       1 ,

thus
                     NU = N − d−1            and K = diag(a) N − d−1
                                                                     
                               1 J                                1 J diag(a).



    We now continue with the proof of Lemma 14, restated here for convenience.

Lemma 14. For all i, j ∈ [A] the following inequalities hold:

                            α2 a[i]a[j] ≤ K[i, j] ≤ α2 + n a[i]a[j].
                                                           


Moreover, when i = 1 or j = 1, we have K[i, j] = α2 a[i]a[j].

Proof. From Lemma 23 we have
                                                            
                                                        1
                            K[i, j] =       Ñ [i, j] −          a[i]a[j],     i, j ∈ [A].
                                                        d1

On the other hand, from Corollary 2 we have
                                                   1
                               α2 ≤ Ñ [i, j] −       ≤ α2 + n,              i, j ∈ [A],
                                                   d1

and Ñ [i, j] = α2 + d11 whenever i = 1 or j = 1. This proves the claim.


7      Proofs for AND-OR tree evaluation
Proof of Lemma 10. Correctness. Children of a vertex v gets added to T ′ if the tree size estimate
for T (v) is at least 2m
                       3 . If the tree size estimation in step 1 is correct, we have the following:

    • if the actual size is at least m, the estimate is at least (1 − δ)m = 2m
                                                                             3 ;
                                                                           m    2m
    • if the actual size is less than m
                                      2 , the estimate is less than (1 + δ) 2 = 3 .

This means, if all the estimates are correct, then T ′ is a correct m-heavy element subtree.
   To show that all the estimates are correct with probability at least 1 − ǫ, we have to bound the
number of calls to tree size estimation. We show
Lemma 24. An m-heavy element subtree T ′ contains at most n 6T
                                                            m vertices.




                                                        32
                                                                      m
Proof. On each level, T ′ has at most 2T m vertices x with |T (x)| ≥ 2 . Since the depth of T (and,
hence, T ′ ) is at most n, the total number of such vertices is at most 2Tmn . For each such x, T ′ may
also contain its children with |T (x)| < m2 . Since each non-leaf x has two children, the number of
such vertices is at most 4Tmn and the total number of vertices is at most 6Tmn .

    Since the algorithm makes one call to tree size estimation for each x in T ′ and each call to tree
                                                                   m
size estimation is correct with probability at least 1 − ǫ′ = 1 − 6nT ǫ, we have that all the calls are
correct with probability at least 1 − ǫ.
Running time. Since the formula tree is binary, we have d = O(1). Also, δ = 31 is a constant, as
well. Therefore, each call to tree size estimation uses
                                               √
                                                          
                                                       2 1
                                           O     nm log ′
                                                         ǫ

queries. Since tree size estimation is performed only for vertices that get added to T ′ , it is performed
at most 6Tmn times. Multiplying the complexity of one call by 6Tmn and substituting ǫ′ = 6nT     m
                                                                                                   ǫ > 6Tǫ 2
gives the complexity of                       1.5          
                                              n T        T
                                          O √ log2            .
                                                 m        ǫ


   Analysis of the main algorithm: correctness.

Lemma 25. If Unknown-evaluate is used as a query, it performs a transformation |ψstart i → |ψi
where |ψi satisfies                                   √
                             kψ − (−1)T ψstart k ≤ 2 ǫ

Proof. We use induction over i ∈ {0, 1, . . . , c}, with i = 0 being queries to one variable (which are
invoked by Unknown-evaluate(r, 1, ǫ) in the 3rd step when i = 1) and i = 1, . . . , c being calls to
Unknown-evaluate with the respective value of i.
    For the base case (i = 0), a query to a variable produces the transformation |ii → (−1)xi |ii.
In this case, T = xi , so, this is exactly the correct transformation.
    For the inductive step (i ≥ 1), we first assume that, instead of calls to Unknown-evaluate
at the leaves, we have perfect queries with no error. Let |ψideal i be the final state under this
assumption. We first bound kψideal − (−1)T ψstart k and then bound the difference between |ψideal i
and the actual P final state |ψi.
    Let |ψ i = T ′ ,x αT ′ ,x |T ′ , xi ψT ′ ,x be the state after the first three steps, with T ′ being the
           ′

subtree obtained in the 1st or the 2nd step, x being the result obtained at the 3rd step and ψT ′ ,x
being all the other registers containing intermediate information. We express |ψ ′ i = |ψ1 i+|ψ2 i+|ψ3 i
where

   • |ψ1 i contains terms where T ′ is a valid m-heavy element subtree and x is the correct answer;

   • |ψ2 i contains terms where T ′ is a valid m-heavy element subtree but x is not the correct
     answer;

   • |ψ3 i contains all the other terms.



                                                    33
                                                                     p                       p
By the correctness guarantees for steps 2 and 3, we have kψ2 k ≤ ǫ/5 and kψ3 k ≤ ǫ/5.
    After the phase flip in step 4, the state becomes |ψ ′′ i = (−1)T |ψ1 i + |ψ2′ i + |ψ3′ i with |ψ2′ i and
  ′
|ψ3 i consisting of terms from |ψ2 i and |ψ3 i , with some of their phases flipped. Hence,
                                                                                              r
             ′′       T ′       ′     ′                     ′      ′                             ǫ
         kψ − (−1) ψ k ≤ kψ2 + ψ3 k + kψ2 + ψ3 k ≤ kψ2 k + kψ3 k + kψ2 k + kψ3 k ≤ 4               .
                                                                                                 5

Reversing the first three steps maps |ψ ′ i back to |ψstart i and |ψ ′′ i to |ψideal i. Hence, we have the
same estimate for kψideal − (−1)T ψstart k.
                                                                                            √
   We now replace queries by applications of Unknown-evaluate. Let t = O( sn) = O(s)
be the number of queries. Let |φi i be the final state of the algorithm if the first i queries use
the perfect query transformation and the remaining queries are implemented using Unknown-
evaluate. Then, |ψideal i = |φt i and |ψi = |φ0 i and we have
                                                   t−1                √
                                                   X               2s ǫ     √
                    kψ − ψideal k = kφ0 − φt k ≤     kφj − φj+1 k ≤ 3/2 = o( ǫ),
                                                 j=0
                                                                    s

with the second inequality following from the inductive assumption. (The only difference between
|φj i and |φj+1 i is that, in the first case, we apply a perfect query transformation in the (j + 1)st
query and, in the second case, we apply Unknown-evaluate(v, i − 1, ǫ/s3 ) instead.√
                                                                                        The distance
                                                                                 2 ǫ
between the states resulting from these two transformations can be bounded by s3/2 by the inductive
assumption.) Therefore,
                                                                         4 √    √      √
       kψ − (−1)T ψstart k ≤ kψideal − (−1)T ψstart k + kψ − ψideal k ≤ √ ǫ + o( ǫ) < 2 ǫ.
                                                                          5
This concludes the proof.

    For the case when Unknown-evaluate is used to obtain the final answer, let |ψ ′ i be the final
state if, instead of calls to Unknown-evaluate at the next level, we had perfect queries and let |ψi
be the actual final state of the algorithm. We express |ψi = |ψcor i+|ψinc i where |ψcor i (|ψinc i) is the
part of the state where the algorithm outputs correct (incorrect) answer. Let |ψ ′ i = |ψcor ′ i + |ψ ′ i
                                                                                                        inc
                                     ′          ′                       2 √
be a similar decomposition for |ψ i. Then, kψinc k ≤ kψ2 k + kψ3 k ≤ √5 ǫ and

                       ′                ′         ′                    2 √     √    √
           kψinc k ≤ kψinc k + kψinc − ψinc k ≤ kψinc k + kψ − ψ ′ k ≤ √ ǫ + o( ǫ) < ǫ.
                                                                        5

The probability of Unknown-evaluate outputting an incorrect answer is kψinc k2 < ǫ.
   Analysis of the main algorithm: running time.

Lemma 26. The number of queries made by Unknown-evaluate(r, i, ǫ) is of an order
                                                     i !
                                i
                                  p                 1
                          O n Ti T 1/c log Ti + log        .
                                                    ǫ

                                                         n Ti 1.5
Proof. Generating T ′ takes O(T1 ) steps if i = 1 and O( √     log2 Tǫi ) steps if i > 1. Since √Ti =
                                                          Ti−1                                   Ti−1
p
      1/c
  Ti T , this is at most the bound in the statement of the lemma.

                                                     34
                                                                      √       1
   In the next step, the algorithm calls Unknown-evaluate
                                                     √      for   ns log ǫ ) subtrees where s is
                                                                    O(
the size of T ′ . Since s = O n TTi−1
                                   i
                                        , this means O n √ Ti log 1ǫ calls of Unknown-evaluate.
                                                                          Ti−1
For each of them, the number of queries is
                                                         i−1 !                                                     i−1 !
                                                      1                                                           1
                  q                                                             q
            i−1                                                           i−1
      O n             Ti−1 T 1/c       log Ti−1 + log ′            =O n             Ti−1 T 1/c       log Ti + log              .
                                                     ǫ                                                            ǫ

Multiplying the number of calls to Unknown-evaluate with the complexity of each call gives the
claim.

     We now show how Lemma 26 implies Theorem 9. If i = c, the expression of Lemma 26 is equal
to
                                             1 c
                       p                               1 1        
                    O nc T 1+1/c log T + log         = O T 2 + 2c +o(1) .
                                              ǫ
Since c can be chosen arbitrarily large, we can achieve O(T 1/2+δ ) for arbitrarily small δ > 0. The
total running time is O(log T ) = O(T o(1) ) times the number of queries.


8      Conclusion
Search trees of unknown structure (which can be discovered by local exploration) are commonly
used in classical computer science. In this paper, we constructed three quantum algorithms for such
trees: for estimating size of a tree, for finding whether a tree contains a marked vertex (improving
over an earlier algorithm by Montanaro) and for evaluating an AND-OR formula described by a
tree of unknown structure.
    Some of possible directions for future study are:

     1. Space-efficient algorithm for AND-OR formula evaluation? Our algorithm for eval-
        uating AND-OR formulas in Section 3.5 uses a substantial amount of memory to store the
        heavy element subtrees. In contrast, the algorithm of [1] for evaluating formulas of known
        structure only uses O(log T ) qubits of memory. Can one construct an algorithm for evaluat-
        ing formulas of unknown structure with time complexity similar to our algorithm but smaller
        space requirements?

     2. Speeding up other methods for solving NP-complete problems. Backtracking is used
        by SAT solvers and other algorithms for NP-complete problems. Our quantum algorithm
        for backtracking provides an almost quadratic quantum improvement over those algorithms.
        What other methods for solving NP-complete problems have faster quantum counterparts?

     3. Other parameter estimation problems. The tree size estimation problem can be viewed
        as a counterpart of quantum counting, in a more difficult setting. What other problems about
        estimating size (or other parameters) of combinatorial structures would be interesting and
        what would they be useful for?




                                                               35
Acknowledgements
The authors would like to thank Mark Goh for his valuable comments on a previous version of
the paper, in particular, for pointing out a mistake in the proof of Lemma 16. The corrected
version requires adjusting the bound on θ̂ − θ in Lemma 5 and choosing the parameter value
          1.5                        1.5
         δ
δmin = 24√ 3nT0
                (instead of δmin = 4√δ3nT ) in Algorithm 1.
                                         0
   This work has been supported by the ERC Advanced Grant MQC and Latvian State Research
programme NexIT project No.1.


References
 [1] A. Ambainis, A. Childs, B. Reichardt, R. Špalek, S. Zhang. Any AND-OR formula of size N
     can be evaluated in time N 1/2+o(1) on a quantum computer. SIAM Journal on Computing,
     39(6): 2513-2530, 2010. DOI:10.1137/080712167. Also arXiv:quant-ph/0703015.

 [2] D. S. Bernstein. Matrix mathematics. Theory, facts, and formulas, 2nd edition. Princeton
     University Press, Princeton, 2009.

 [3] M. Davis, G. Logemann, and D. Loveland. A machine program for theorem proving. Commu-
     nications of the ACM, 5(7):394-397, 1962. DOI:10.1145/368273.368557.

 [4] M. Davis and H. Putnam. A computing procedure for quantification theory. Journal of the
     ACM, 7(3):201-215, 1960. DOI:10.1145/321033.321034.

 [5] E. Farhi, J. Goldstone, S. Gutman, A quantum algorithm for the Hamilto-
     nian NAND tree. Theory of Computing, 4(1):          169-190, 2008. Available at
     http://theoryofcomputing.org/articles/v004a008. Also arXiv:quant-ph/0702144.

 [6] L. K. Grover. A fast quantum mechanical algorithm for database search. Proceed-
     ings of the ACM Symposium on the Theory of Computing (STOC’1996), pp. 212-219.
     DOI:10.1145/237814.237866. Also arXiv:quant-ph/9605043.

 [7] R. A. Horn, C. R. Johnson. Matrix analysis, 2nd edition. Cambridge University Press, Cam-
     bridge, 2012. DOI:10.1017/CBO9781139020411.

 [8] G. F. Lawler, L. N. Coyle. Lectures on contemporary probability, volume 2 of Student Math-
     ematical Library / IAS/Park City Mathematical Subseries. American Mathematical Society,
     Providence, 1999. DOI:10.1090/stml/002

 [9] D. A. Levin, Y. Peres, E. L. Wilmer.      Markov chains and mixing times. With
     a chapter by James G. Propp and David B. Wilson.          American Mathematical
     Society, Providence, 2009. Available at http://www.ams.org/books/mbk/058/. Also
     http://pages.uoregon.edu/dlevin/MARKOV/markovmixing.pdf.

[10] L. Lovász. Random walks on graphs: A survey. In Combinatorics, Paul Erdös is eighty
     (D. Miklós, V. T. Sós, T. Szőnyi, eds.), volume 2, pp. 353–397, János Bolyai Mathematical
     Society, Budapest, 1996.



                                               36
[11] R. Lyons, Y. Peres.    Probability on trees and networks.   Cambridge University
     Press, New York, 2016. Available at http://www.cambridge.org/9781107160156. Also
     http://pages.iu.edu/~rdlyons/.

[12] A. Montanaro. Quantum walk speedup of backtracking algorithms. arXiv:1509.02374.

[13] R. Pemantle. Uniform random spanning trees. In Topics in contemporary probability and its ap-
     plications (J.L. Snell, ed.), pp. 1–54, CRC Press, Boca Raton, 1995. Also arXiv:math/0404099.

[14] B. Reichardt. Faster quantum algorithm for evaluating game trees. Proceedings of
     SODA’2011, pp. 546-559. Available at http://dl.acm.org/citation.cfm?id=2133079. Also
     arXiv:0907.1623.

[15] M. Szegedy. Quantum speed-up of Markov chain based algorithms. Proceedings of FOCS’2004,
     pp. 32-41. DOI:10.1109/FOCS.2004.53




                                               37

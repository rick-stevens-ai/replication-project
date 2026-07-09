                                                                           Element Distinctness Revisited
                                                                                          Renato Portugal∗




arXiv:1711.11336v3 [quant-ph] 13 Jun 2018
                                                                        National Laboratory of Scientific Computing - LNCC
                                                                       Av. Getúlio Vargas 333, Petrópolis, RJ, 25651-075, Brazil

                                                                                            June 15, 2018



                                                                                               Abstract
                                                          The element distinctness problem is the problem of determining whether the ele-
                                                      ments of a list are distinct, that is, if x = (x1 , ..., xN ) is a list with N elements, we ask
                                                      whether the elements of x are distinct or not. The solution in a classical computer
                                                      requires N queries because it uses sorting to check whether there are equal elements.
                                                      In the quantum case, it is possible to solve the problem in O(N 2/3 ) queries. There
                                                      is an extension which asks whether there are k colliding elements, known as element
                                                      k-distinctness problem.
                                                          This work obtains optimal values of two critical parameters of Ambainis’ seminal
                                                      quantum algorithm [SIAM J. Comput., 37, 210-239, 2007]. The first critical param-
                                                      eter is the number of repetitions of the algorithm’s main block, which inverts the
                                                      phase of the marked elements and calls a subroutine. The second parameter is the
                                                      number of quantum walk steps interlaced by oracle queries. We show that, when
                                                      the optimal values of the parameters are used, the algorithm’s success probability is
                                                      1 − O(N 1/(k+1) ), quickly approaching 1. The specification of the exact running time
                                                      and success probability is important in practical applications of this algorithm.


                                            1        Introduction
                                            The element distinctness problem has a long history. In classical computing, the opti-
                                            mal lower bound for the model of comparison-based branching programs was obtained by
                                            Yao [1] and classical lower bounds have been obtained in general models in Refs. [2, 3].
                                            Quantum lower bounds for the number of queries were obtained by Aaronson and Shi [4]
                                            and Ambainis [5]. Buhrman et al. [6] described a quantum algorithm that uses O(N 3/4 )
                                            queries. Ambainis’ optimal algorithm for the element distinctness problem in O(N 2/3 )
                                            queries firstly appeared in [7] and later in [8]. Ambainis also addressed the element k-
                                            distinctness problem describing an algorithm in O(N k/(k+1) ) queries. This algorithm used
                                            a new quantum walk framework on a bipartite graph, which was generalized by Szegedy [9].
                                            The algorithm was also used to build a quantum algorithm for triangle finding by Mag-
                                            niez et al. [10] and to subset finding by Childs and Eisenberg [11].
                                                ∗
                                                    portugal@lncc.br



                                                                                                    1
     A related problem is the collision problem, where a one-to-one or a two-to-one function
f : {1, ..., N } → {1, ..., N } is given and we have to decide which the function type is.
Quantum lower bounds for the collision problem were obtained by Aaronson and Shi [4]
and by Kutin [12]. Brassard et al. [13] solved the collision problem in O(N 1/3 ) quantum
steps achieving the lower bound. If the element distinctness√problem can be solved with
N queries, then the collision problem can be solved with O( N) queries [4].
     Many important results were obtained after Ambainis’ seminal paper. Santha [14]
surveyed the application of Szegedy’s quantum walk to the element distinctness problem
and for other related search problems, such as matrix product verification and group
commutativity. Childs [15] described the element distinctness algorithm in terms of the
continuous-time quantum walk model [16]. Belovs [17] used learning graphs to present a
                                                               k−2  k
quantum algorithm for the k-distinctness problem in O N 1−2 /(2 −1) queries, improving
                                                                        

Ambainis’ result for k ≥ 3 and Belovs et al. [18] presented quantum walk algorithms for
the element 3-distinctness problem with time complexity Õ(N 5/7 ) improving the time
complexity of Õ(N 3/4 ) by Ambainis. Rosmanis [19] addressed quantum adversary lower
bounds for the element distinctness problem. Kaplan [20] used the element distinctness
algorithm in the context of quantum attacks against iterated block ciphers. Jeffery et
al. [21] analyzed parallel quantum queries for the element distinctness problem.
     Ambainis’ algorithm consists of a main block that is repeated t1 =
O((N/r)k/2 ) times. The block alternates the action of a conditional phase-flip operator
                                                           √
and a subroutine call. The subroutine executes t2 = O( r) steps of a bipartite quantum
walk interlaced with oracle calls. The value of r is chosen so that the number of queries
is minimized. Ambainis showed that the best value is r = N k/(k+1) , which implies that
            √
t1 = O( r) and the number of queries is O(r), which is optimal for k = 2.
     In this work, we determine the optimal values of constants c1 and c2 that maximize the
                                                      √               √
success probability of the algorithm, where  √ t1 = c1 r and t2 = c2 r. We show that√the
optimal values are c1 = π/4 and c2 = π/(2 k) and the success probability is 1− O(1/ k r).
In order to do so, we use an instance of the staggered quantum walk [22, 23, 24], which helps
to simplify the analysis of the algorithm. The algorithm can be described as a quantum-
walk-based search algorithm with multiple marked vertices. At the end, we measure the
position of the walker outputting a vertex label, which is a r-subset of indices {i1 , ..., ir }
that has a k-collision with high probability, that is, xj1 = · · · = xjk for {j1 , ..., jk } ⊂
{i1 , ..., ir }. The algorithm can be analyzed in full details because the dynamics can be
obtained from a reduced (2k + 1)-dimensional Hilbert space, which simplifies the analysis
of the quantum-walk-based search algorithm. This work was motivated by Abreu’s master
thesis [25], who analyzed Ambainis’ algorithm in terms of the staggered model.
     In Section 2, we describe the staggered quantum walk and the graph on which the
quantum walk takes place. Then, we describe the algorithm. In Section 3, we formulate
a theorem about the optimality of t1 , t2 , and the algorithm’s success probability, and we
give a proof of this theorem. In Section 4, we draw our conclusions. The appendix includes
a formal definition of the staggered quantum walk and contains a glossary of graph theory
terms used in this work.




                                               2
2     Description of the Algorithm
This section describes a quantum algorithm for the element k-distinctness problem, which
is the following problem. Suppose we have a list x = (x1 , ..., xN ) of N elements, is there
a set K = {i1 , ..., ik } with k distinct marked indices such that xi1 = · · · = xik ?

2.1    Quantum Walk Evolution Operator
Before describing the algorithm, let us give a list of definitions. [N ] is the set {1, ..., N }, r is
                            k
the integer nearest to N k+1 , Sr is the set of all r-subsets of [N ], V= {(S, y) : S ∈ Sr , y ∈
[N ] \ S}, and H = span {|S, yi : (S, y) ∈ V}. Note that |Sr | = Nr and |V| = Nr (N − r),
where Nr is the binomial coefficient. Let Γ be a graph with vertex set V (the vertices are
           

labeled by (S, y) ∈ V) such that vertices (S, y) and (S ′ , y ′ ) are adjacent if and only if S = S ′
or S ∪ {y} = S ′ ∪ {y ′ }. Since the clique graph of Γ is 2-colorable, Γ is 2-tessellable [24].
    The appendix contains definitions of some key concepts of graph theory and, in par-
ticular, the definitions of graph tessellation and the staggered model, which are required
in the rest of this work. Note that from now on, the description given here moves away
from Ambainis’ description, which uses a bipartite graph defined formally in the appendix.
Graph Γ, on which the staggered quantum walk is defined, is the line graph of Ambai-
nis’ graph. The results obtained in this paper regarding the optimality of t1 and t2 do
apply to Ambainis’ algorithm. Note that there is an alternate description of the element
distinctness algorithm given by Santha [14], who uses Szegedy’s quantum walk on a sym-
metric bipartite graph obtained from the Johnson graph through a duplication process.
In principle, the results obtained here do not apply to Santha’s version.
    A staggered quantum walk on graph Γ is defined after describing two tessellations Tα
and Tβ induced by a coloring of the clique graph K(Γ). Let us start by defining Tα . For
each S ∈ Sr define set αS = {(S, y) ∈ V : y ∈ [N ] \ S}. We state that αS is a clique of
size (N −r). In fact, a subset of vertices is a clique if all vertices in the subset are adjacent.
By definition, αS is a subset of vertices and all vertices in αS are adjacent because they
share the same S. The size of the clique is (N − r) because the cardinality of set [N ] \ S
is (N − r). It is straightforward to check that the union of αS for all S in Sr is the vertex
set V, that is,                                 [
                                          V=         αS .
                                                 S∈Sr
                                  ′
                   ′ = ∅ if S 6= S . Then, the set T
Besides, αS ∩ αS                                 α = {αS : S ∈ Sr } is a tessellation of Γ,
whose size is |Tα | = Nr .
                        

   For each S ∈ Sr , define the α-polygon vector
                                           1      X
                                 |αS i = √               |S, yi .                                 (1)
                                          N − r y∈[N ]\S

Note that αS αS ′ = δSS ′ . Now define
                                             X
                                   Uα = 2           |αS i hαS | − I,                              (2)
                                             S∈Sr



                                                    3
which is the unitary and Hermitian operator associated with tessellation α.
      Let us define tessellation Tβ . Define a partition of the vertex set V induced by the
equivalence relation ∼, where (S, y) ∼(S ′ , y ′ ) if and only if S ∪ {y} = S ′ ∪ {y ′ }. An
equivalence class is defined by [S, y] = (S ′ , y ′ ) ∈ V : (S ′ , y ′ ) ∼ (S, y) and the quotient
set by V/∼ = {[S, y] : (S, y) ∈ V}. Note            that the cardinality of each equivalence class is
                                             N 
(r + 1) and of the quotient set is r+1           . For each element [S, y] in the quotient set, define
β[S,y] = {(S ′ , y ′ ) ∈ V : (S ′ , y ′ ) ∼ (S, y)}. Set β[S,y] is obtained from a cyclic rotation of
the elements of S ∪ {y}. We state that β[S,y] is a clique of size (r + 1). In fact, all vertices
(S ′ , y ′ ) in β[S,y] are adjacent because S ′ ∪ {y ′ } = S ∪ {y}. The size of β[S,y] is (r + 1)
because the cardinality of set S ∪ {y} is (r + 1).
      It is straightforward to check that the union of β[S,y] for all [S, y] in quotient set V/∼
is the vertex set V, that is,                        [
                                             V=            β[S,y] .
                                              [S,y]∈V/∼

                          = ∅ if [S, y] 6= [S ′ , y ′ ]. Then, the set T
Besides, β[S,y] ∩ β[S ′ ,y′ ]                                              β = {β[S,y] : [S, y] ∈ V/∼} is
                                            N 
a tessellation of Γ, whose size is |Tβ | = r+1 .
    For each [S, y] ∈ V/∼, define the β-polygon vector
                                         1    X
                         β[S,y] = √                       S ∪ {y} \ {y ′ }, y ′ .                    (3)
                                        r+1 ′
                                               y ∈S∪{y}


Note that β[S,y] is the uniform superposition of the equivalence class that contains (S, y)
and that β[S,y] β[S ′ ,y′ ] = δ[S,y],[S ′,y′ ] . Define
                                           X
                              Uβ = 2                β[S,y]   β[S,y] − I,                             (4)
                                        [S,y]∈V/∼

which is the unitary and Hermitian operator associated with tessellation β.
    Uα and Uβ are local operators in the sense that they move the walker only to adjacent
vertices. The evolution operator of a staggered quantum walk on graph Γ with unmarked
vertices is driven by the unitary operator U = Uβ Uα . The evolution operator must be
modified if there are marked vertices. A vertex (S, y) is marked if and only if K ⊆ S.
The usual recipe to obtain quantum walk search algorithms is to define a new evolution
operator U ′ = U R, where R inverts the sign of the marked vertices and acts as the identity
on unmarked ones. This recipe does not work in the present case because the argument
of the principal eigenvalue of U goes to zero too quickly when N increases. To solve this
problem, we have to use the recipe U ′ = U t2 R, where t2 must counteract the decrease of
the argument of the principal eigenvalue.
    In the next section, we give the full description of the element k-distinctness algorithm,
which employs two registers. Here we move closer to Ambainis’ description but from two
key differences: First, the unitary operator Uβ , which acts on the first register only, is
               EXT
extended to Uβ , which acts on both registers; and second, the oracle is simpler and acts
only on the last ket of the second register. In Ambainis’ algorithm, the operator that is
equivalent to Uβ acts only on the first register and the oracle must perform some highly
non-trivial tasks.

                                                    4
2.2   The Algorithm
The algorithm uses two registers. A vector of the computation basis has the form

                                       |S, yi ⊗ x′1 , ..., x′r+1 ,

where (S, y) is a vertex label, x′ ∈ [M], and M is an upper bound for the list elements.
                                      N
The Hilbert space has   dimension r (N      − r)M r+1 and the memory in qubits is then
                                         ′
O r(log2 N + log2 M ) . The notation xi denotes a generic value in [M ] and xi denotes the
list element in the ith position, such as xi1 or xy .

Initial Setup
The initial state is
                                      1           X
                               q                        |S, yi |0, ..., 0i .
                                   N
                                   r (N − r) (S,y)∈V

The first step is to query each xi for i ∈ S. Suppose that S = {i1 , ..., ir }, then the next
state is
                               1          X
                         q                     |S, yi |xi1 , ..., xir , 0i .             (5)
                            N
                             r (N −  r) (S,y)∈V


Main Block
                                                                               j √ m
                                                                                π
   1. Repeat this step the following number of times: t1 =                      4 r , where ⌊ ⌉ is the
      notation for the nearest integer.

       (a) Apply a conditional phase-flip operator R that inverts the phase of |S, yi
            x′1 , ..., x′r+1 if and only if there is a k-collision for distinct indices K = {i1 ,...,ik }
           in S, that is,
                                              (
                                               − |S, yi x′1 , ..., x′r+1 , k-collision for K ⊆ S,
                 R |S, yi x′1 , ..., x′r+1 =
                                                 |S, yi x′1 , ..., x′r+1 , otherwise.
                                                                                   j √ m
                                                                                    π√ r
       (b) Repeat Subroutine 1 the following number of times: t2 =                  2 k
                                                                                           .

   2. Measure the first register and check whether S has a k-collision using a classical
      algorithm.

Subroutine 1
   1. Apply operator Uα given by (2) on the first register.

   2. Apply oracle O defined by

                           O |S, yi x′1 , ..., x′r+1 = |S, yi x′1 , ..., x′r+1 ⊕ xy ,

      which queries element xy and adds xy to x′r+1 in the last slot of the second register.

                                                   5
                               EXT
    3. Apply operator Uβ             , which is an extension of (4), defined by

                        EXT
                                            X           X            x′ ,...,x′r+1
                                                                                     E D x′ ,...,x′
                                                                       1                   1      r+1
                       Uβ          = 2                              β[S,y]              β[S,y]        − I,
                                         x′1 ,...,x′r+1 [S,y]∈V/∼

      where
               x′ ,...,x′r+1
                               E           1    X
                 1
              β[S,y]               = √                           S ∪ {y} \ {y ′ }, y ′      π(x′1 ), ..., π(x′r+1 )   (6)
                                          r+1 ′
                                                  y ∈S∪{y}

      and π is a permutation of the slots of the second register induced by the permutation
      of the indices of the first register.

    4. Apply oracle O.

Notes. (i ) In Eq. (5), the elements of S and the first r slots of the second register are
in one-to-one correspondence. The number of queries in this step is r and it is performed
only once. (ii ) When the input is state (5), the output of step 2 of Subroutine 1 has the
elements of S and the first r slots of the second register in one-to-one correspondence and
the last slot of the second register is xy . This one-to-one correspondence is maintained
for each term in sum (6) and π(x′r+1 ) = xy′ . (iii ) The total number of quantum queries
               √
is r + π 2 r/(4 k) approximately considering the Initial Setup and the Main Block. After
the measurement, r classical queries are necessary.


3     Main Result
                                             √     √
The next theorem improves the value t2 = π r/(3 k) given by Ambainis [8], which yields
a success probability of 75% asymptotically.
                                    √                √      √
Theorem 3.1. The values t1 = π r/4 and t2 = π r/(2 k) are asymptotically optimal
and the success probability of the algorithm is 1 − O(1/r 1/k ).

Proof. Define (2k + 1) nonempty sets ηℓj = {(S, y) ∈ V : |S ∩ K| = ℓ, |{y} ∩ K| = j}.
Set ηℓj is the set of vertices (S, y) such that S has exactly ℓ marked indices and y 6∈
K if j = 0 and y ∈ K if j = 1. Set ηk1 is the empty set. The cardinality of ηℓj is
 k  N −k                                k  N −k                                    j
 ℓ   r−ℓ (N − r − k + ℓ) if j = 0 and ℓ         r−ℓ (k − ℓ) if j = 1. The set of sets ηℓ is a
partition of V. The range of ℓ is 0 ≤ ℓ ≤ k and of j is 0 ≤ j ≤ 1 but must exclude the
case ℓ = k and j = 1. Assume that k < N − r so that sets ηℓj are nonempty.
    Define the corresponding unit vectors
                                    E      1
                                 ηℓj = r
                                                   X
                                                         |S, yi ,                         (7)
                                              j
                                             ηℓ (S,y)∈ηℓ
                                                       j




which span a (2k + 1)-dimensional subspace of the Hilbert space that can be used to
analyze the algorithm and to obtain the success probability. In order to do so, we show
that the (2k + 1)-subspace is invariant under the action of Uα and Uβ . Let us obtain

                                                             6
matrices uE
          α and uβ of dimension (2k + 1) that reproduce the action of Uα and Uβ on
vectors ηℓj , that is,
                                                                                ′
                                        E                                         E
                               Uα ηℓj                                        ηℓj′ ,
                                                X
                                            =             ℓ′ , j ′ uα ℓ, j
                                                ℓ′ j ′

and the equivalent one for uβ , where the set of kets |ℓ, ji is the computational basis of a
Hilbert space of dimension (2k + 1).
   Using (1) and (7), we obtain
                     D         E (1 − j)(N − r) + (2j − 1)(k − ℓ)
                         αS ηℓj =                                 δ|S∩K|,ℓ
                                              j √
                                          r
                                            ηℓ N − r

and                                             q                                            
                                       1
                  X                                                              q
                          |αS i = √                      ηℓ0     ηℓ0 + (1 − δkℓ ) ηℓ1   ηℓ1       .
                  S∈Sr
                                      N −r
                |S∩K|=ℓ

Using those results and (2), we find the entries of uα , which are
                                                          
                      ′ ′                 j      2 (k − l)
                     ℓ , j uα ℓ, j = (−1) 1 −                δℓℓ′ δjj ′ +
                                                   N −r
                                       r        r
                                         k−ℓ            k−ℓ
                                     2            1−           δℓℓ′ δj⊕1,j ′ .                                (8)
                                         N −r          N −r
Analogously, using (3) and (7), we obtain
                    D          E (1 − j) r + (2j − 1) ℓ + 1
                     β[S,y] ηℓj =                           δ|(S∪{y})∩K|,ℓ+j
                                            j √
                                       r
                                           ηℓ r + 1

and                                             q                                                    
                                         1
               X                                                                  q
                           β[S,y] = √                      ηℓ0    ηℓ0 + (1 − δℓ0 ) ηℓ−1
                                                                                    1          1
                                                                                              ηℓ−1        .
                                        r+1
               (S,y)
          |(S∪{y})∩K|=ℓ

Using those results and (4), we find the entries of uβ , which are
                                                        
                   ′ ′                 j       2 (ℓ + j)
                  ℓ , j uβ ℓ, j = (−1) 1 −                 δℓℓ′ δjj ′ +
                                                 r+1
                                     r      r
                                       ℓ+j          ℓ+j
                                   2           1−          δ          j ′ δ1⊕j,j ′ .                          (9)
                                       r+1          r + 1 ℓ−(−1) ,ℓ
    Next step is to show that the conditional phase flip operator R leaves the (2k + 1)-
subspace invariant too. R inverts the phase of |S, yi if and only if |S ∩ K| = k, that is
(S, y) ∈ ηk0 . Define a reduced version of R, denoted by R, in the (2k + 1)-dimensional
Hilbert space as
                                  R = I − 2 |k, 0i hk, 0| .                         (10)


                                                           7
                                                                                                  E
   State (5) at the beginning of the algorithm is a linear combination of ηℓj                         and can be
written in the Hilbert space of dimension (2k + 1) as
                                                    r
                                        1
                                                        ηℓj |ℓ, ji .
                                                X
                          |ψ0 i = q                                                                        (11)
                                     N
                                     r (N − r) ℓ,j

Since all steps of the algorithm can be obtained from the reduced Hilbert space, the final
state of the algorithm right before the measurement can be obtained from
                                                    t
                                |ψf i = (uβ uα )t2 R 1 |ψ0 i .

Note that the oracle changes only the second register and is therefore omitted. Our goal
now is to show that the choices for t1 and t2 described in the algorithm are optimal with
maximal success probability.
   The probability of finding a marked vertex as a function of t is
                                            D          t  E2
                                   p(t) =    k, 0 ut2 R ψ0    ,                                             (12)

where u = uα uβ . Let e±iλ be the eigenvalues of ut2 R that are nearest to 1 and let |λi
                                                       

and its complex-conjugate |λi∗ be the corresponding eigenvectors. Assume for now that
the contribution of the other eigenvalues and eigenvectors to the calculation of p(t) goes
to zero when N increases. In this case
                                                                      ∗          ∗        2
                p(t) = eiλ t k, 0 λ        λ ψ0 + e−iλ t k, 0 λ           λ ψ0       +ǫ       ,             (13)

where limN →∞ |ǫ| = 0. Suppose that vectors |ψ±n i for 0 ≤ n ≤ k are unit eigenvectors of
u with eigenvalues eiφ±n , where |ψ−n i = |ψn i∗ , φ−n = −φn , and k, 0 ψ±n > 0. |ψ0 i is
given by (11) and has positive entries.
    Using ψn ut2 R λ = eiλ ψn λ , we obtain

                                                  2 k, 0 λ k, 0 ψn
                                   ψn λ =                            ,                                      (14)
                                                    1 − ei(λ−t2 φn )
which is valid if λ 6= t2 φn . Substituting this result in
                                               k
                                               X
                                  k, 0 λ =               k, 0 ψn   ψn λ ,                                   (15)
                                              n=−k

we obtain
                                      X 2 k, 0 ψn 2
                                                               = 1.
                                       n
                                            1 − ei(λ−t2 φn )

Using that 2/(1 − eia ) = 1 + i sin a/(1 − cos a), the imaginary part of the above equation is
                             X                2     sin(λ − t2 φn )
                                    k, 0 ψn                           = 0.                                  (16)
                              n
                                                  1 − cos(λ − t2 φn )

                                                     8
Suppose that λ ≪ t2 φn for n > 0 when N ≫ 1. We will check the validity of this
assumption later. Expanding in Taylor series and discarding terms O(λ2 ), we obtain

                                                  k, 0 ψ0
                                         λ=         √     ,                                       (17)
                                                      b
where
                                        k                    2
                                        X        k, 0 ψn
                                  b=                          .                                   (18)
                                              1 − cos(t2 φn )
                                        n=1

   Now let us find φn and k, 0 ψn . Using the entries of uα and uβ , we obtain the
characteristic polynomial of u = uβ uα , which is

                                               k
                        |λI − u|               Y
                                                 λ2 − 2 λ cos φn + 1 ,
                                                                    
                           k       k
                                     = (λ − 1)
                    (r + 1) (N − r)
                                                       n=1

where
                                                  2 n (N − n + 1)
                                 cos φn = 1 −                     .                               (19)
                                                  (r + 1) (N − r)
The eigenvectors of u can be found explicitly, but it is easier to calculate directly k, 0 ψn ,
which for n = 0 is
                                               k−1 r
                                               Y       r−i
                                 k, 0 ψ0 =                   ,                             (20)
                                                      N −i
                                                    i=0

for 0 < n < k is
                                  s  v
                                       u Qn−1              Qk−1
                               1
                               √
                                    k u    i=0 (N − r − i)   i=n (r − i)
                   k, 0 ψn   =         t Q2 n−2         Qk+n−1           ,                        (21)
                                2   n     i=n−1 (N − i)   i=2 n (N − i)

and for n = k is                              v
                                              u Qk−1
                                           1 u       (N − r − i)
                              k, 0 ψk   = √ t Qi=02 k−2
                                                                 .                                (22)
                                            2     i=k−1 (N − i)

     Next step in the calculation of p(t) is the term              k, 0 λ .     Substituting (14) into
P            2
    n ψn λ     = 1, we have

                                                 k                     2
                                 1               X           k, 0 ψn
                                        2 =4                               2.
                               k, 0 λ           n=−k    1 − ei(λ−t2 φn )

                         2
Using identity 1 − eia = 2 (1 − cos a), redefining |λi by choosing a multiplicative unit
constant such that k, 0 λ > 0, expanding in Taylor series, and keeping the dominant
term, we obtain
                                               ∗      1
                            k, 0 λ = k, 0 λ = √ √ .                                 (23)
                                                   2 2 b

                                                   9
Next term is λ ψ0 . Substituting n = 0 into (14), using (23), (20), and (17), we obtain

                                          i      √ 
                                  ψ0 λ = √ + O 1/ r .                                 (24)
                                           2
                                                                      √
In fact, the next term in the asymptotic expansion of ψ0 λ would be λ/ 8, which is
     √
O (1/ r). Substituting (23) and (24) into p(t), we obtain
                                                     1
                                            p(t) =      sin2 λt.                      (25)
                                                     4b
   The maximal value of the success probability is obtained by taking t = π/(2λ), which
implies that psucc = 1/(4b). To maximize the success probability, we have to minimize
b. Using Eq. (18), we see that the only free parameter in b is t2 . So, we choose t2 that
                                                       2
minimizes b. Eqs. (20) to (22) show that k, 0 ψn = O (r/N )k−n , which goes to 0
                                                                       
                          2
when n < k, and k, 0 ψk = O(1). The expression of b given by (18) is a sum of terms
which is dominated by the term
                                                 2
                                        k, 0 ψk
                                                     .
                                     1 − cos(t2 φk )
The optimal value of t2 is the one that minimizes this term, that is, maximizes (1 −
cos(t2 φk )), which implies t2 = π/φk . Using (19), the asymptotic expansion of π/φk yields
                                                √
                                         π    π r
                                   t2 =     = √ + O(1),                                (26)
                                        φk    2 k
and then the success probability is
                                                         r         !
                                        k            π       k−1           2
                      psucc = 1 −       1 cot
                                                2
                                                                       + O r− k .     (27)
                                    rk               2        k

Now let us find the running time. Eq. (25) shows that the probability as a function of
time is the square of a sinusoidal function. The optimal running time is the first value of
t that maximizes sin(λt), which is t1 = π/(2λ). Using the value of t2 given by (26), the
expression (17) for λ, and the dominant term of b, the asymptotic expansion of π/(2λ)
yields
                                      π     π√         k−2 
                                t1 =     =      r + O r 2k .                           (28)
                                     2λ     4
    It is still missing to check that λ ≪ t2 φn and limN →∞ |ǫ| = 0 (see (13)). Using (19),
                      √
we have φn = O(1/ r). Using (26), we obtain t2 φn = O(1). Then, λ ≪ t2 φn when N is
large. On the other hand, (24) implies that
                                    2                 ∗ 2              √ 
                           ψ0 λ         +     ψ0 λ           = 1 + O 1/ r .

This means that the initial state |ψ0 i lies in the subspace spanned by |λi and |λi∗ in the
limit N → ∞, that is, limN →∞ |ǫ| = 0. This completes the proof of the theorem.




                                                     10
4    Conclusions
In this work, we have obtained the optimal values of the two critical parameters of Am-
bainis’ algorithm [8]. The first parameter is the number of repetitions of the steps of
the main block, which includes the conditional phase-flip inversion and the subroutine
call. The second parameter is the number of quantum walk steps interlaced by ora-
cle queries. After obtaining the √ optimal values of the critical parameters, which are
        √                 √
t1 = π r/4 and t2 = π r/(2 k), we have shown that the success probability of the
algorithm is 1 − O(1/r 1/k ) improving Ambainis’ result, which attains a success proba-
bility of 3/4 − O(1/r 1/k ), due to a non-optimal choice of the second critical parame-
ter. The√ total number of quantum     queries with optimal values for the parameters is
 π 2 /(4 k) + 1 r + O r (k−1)/k and, at the end, r classical queries are necessary.
                                

     The dynamics of the algorithm can be described in a reduced (2k + 1)-dimensional
Hilbert space. Using the staggered quantum walk model, we were able to obtain the
reduced version of the quantum-walk evolution operator and to calculate the spectral
decomposition. The analysis of quantum-walk-based search algorithms using a reduced
version of the evolution operator has been widely used in literature, such as Refs. [26, 27,
28], which developed many calculation tools that were used in this work and were reviewed
in Ref. [29].
     As a follow-up, we are interested in describing quantum circuits for the element dis-
tinctness algorithm and in determining precisely the number of gates in order to find a
prefactor for the known time complexity bound of O(N 2/3 ln N ) [8].


Appendix
In this appendix, we define the graph theory terms used in this work [30, 31, 32] and the
staggered quantum walk [22, 23, 24].
    A simple and undirected graph (simply graph) Γ(V, E) is defined by a set V (Γ) of
vertices or nodes and a set E(Γ) of edges so that each edge links two vertices and two
vertices are linked by at most one edge. Two vertices linked by an edge are called adjacent.
Two edges that share a common vertex are also called adjacent. A subgraph Γ′ (V ′ , E ′ ),
where V ′ (Γ′ ) ⊂ V (Γ) and E ′ (Γ′ ) ⊂ E(Γ), is an induced subgraph of Γ(V, E) if it has exactly
the edges that appear in Γ over the same vertex set. If two vertices are adjacent in Γ they
are also adjacent in the induced subgraph. A bipartite graph is a graph whose vertex set
V is the union of two disjoint sets X and X ′ so that no two vertices in X are adjacent and
no two vertices in X ′ are adjacent. A clique is a subset of vertices of a graph such that its
induced subgraph is complete. A maximal clique is a clique that cannot be extended by
including one more adjacent vertex, that is, it is not contained in a larger clique. A clique
of size d is called a d-clique. A clique can have one vertex. A partition of the vertex set
into cliques is a collection of vertex-disjoint cliques, whose union is the vertex set. Some
references in graph theory use the term “clique” as a synonym of maximal clique. We
avoid this notation here. A clique graph K(Γ) of a graph Γ is a graph such that every
vertex represents a maximal clique of Γ and two vertices of K(Γ) are adjacent if and only
if the underlying maximal cliques in Γ share at least one vertex in common. A line graph
(or derived graph or interchange graph) of a graph Γ (called root graph) is another graph


                                               11
L(Γ) so that each vertex of L(Γ) represents an edge of Γ and two vertices of L(Γ) are
adjacent if and only if their corresponding edges share a common vertex in Γ. A proper
coloring or simply coloring of a loopless graph is a labeling of the vertices with colors such
that no two vertices sharing the same edge have the same color. A n-colorable graph is the
one whose vertices can be colored with at most n colors so that no two adjacent vertices
share the same color. This concept can be used for edges and other graph structures.
    A graph tessellation T is a partition of the vertex set into cliques, that is, there
                                             |T |
are disjoint cliques c1 , ..., c|T | such ∪ℓ=1 cℓ = V (Γ), where |T | is the tessellation size.
An element cℓ of the tessellation is called a polygon (or tile). An edge belongs to the
tessellation T if and only if its endpoints belong to the same polygon in T . The set of
edges belonging to T is denoted by E(T ). A graph tessellation cover of size n is a set of
n tessellations T1 , ..., Tn , whose union is the edge set, that is, ∪nj=1 E(Tj ) = E(Γ). A graph
is called n-tessellable if there is a tessellation cover of size at most n. The tessellation cover
number is the size of a smallest tessellation cover of Γ. A graph Γ is 2-tessellable if and
only if K(Γ) is 2-colorable [24]. The definition of graph tessellation cover was introduced
by Portugal et al. [22].
    In its simplest form, a staggered quantum walk on a graph Γ(V, E) with a graph
tessellation cover C = {T1 , ..., Tn } is a quantum walk driven by the unitary operator
UC = Un · · · U2 · U1 , where Uj is associated with tessellation Tj and is defined by
                                              |Tj |          ED
                                                       (j)      (j)
                                              X
                                 Uj = 2               cℓ       cℓ − I,
                                              ℓ=1

where
                                    (j)
                                          E           1        X
                                   cℓ         = r                  |vi .
                                                        (j)
                                                       cℓ v∈c(j)
                                                             ℓ


The dimension of Hilbert space is |V | and the computational basis is indexed by the
vertices of Γ.
     Ambainis’ graph [8] is a bipartite graph with Nr + r+1  N 
                                                       
                                                                 vertices. The vertices of the
first set are r-subsets of [N ] and of the second set are (r + 1)-subsets. A vertex v1 in the
first set is adjacent to a vertex v2 in the second set if and only if |v1 ∩ v2 | = r. The graph
Γ defined in Section 2, on which the 2-tessellable staggered quantum walk takes place, is
the line graph of Ambainis’ graph, which on the other hand is the clique graph of Γ. K(Γ)
is 2-colorable because Ambainis’ graph is bipartite.


Acknowledgements
The author acknowledges financial support from CNPq and thanks Raqueline Santos for
useful comments.


References
[1] A. C. C. Yao. Near-optimal time-space tradeoff for element distinctness. In Proc. of
    29th Annual Symposium on Foundations of Computer Science, pages 91–97, 1988.

                                                      12
[2] D. Grigoriev, M. Karpinski, F. M. Heide, and R. Smolensky. A lower bound for
    randomized algebraic decision trees. Computational Complexity, 6(4):357–375, 1996.

[3] P. Beame, M. Saks, X. Sun, and E. Vee. Time-space trade-off lower bounds for ran-
    domized computation of decision problems. J. ACM, 50(2):154–195, 2003.

[4] S. Aaronson and Y. Shi. Quantum lower bounds for the collision and the element
    distinctness problems. J. ACM, 51(4):595–605, 2004.

[5] A. Ambainis. Polynomial degree and lower bounds in quantum complexity: Collision
    and element distinctness with small range. Theory of Computing, 1:37–46, 2005.

[6] H. Buhrman, C. Dürr, M. Heiligman, P. Høyer, F. Magniez, M. Santha, and R. de
    Wolf. Quantum algorithms for element distinctness. SIAM Journal on Computing,
    34(6):1324–1330, 2005.

[7] A. Ambainis. Quantum walk algorithm for element distinctness. In FOCS ’04: Proc. of
    the 45th Annual IEEE Symposium on Foundations of Computer Science, pages 22–31,
    Washington, DC, 2004.

[8] A. Ambainis. Quantum walk algorithm for element distinctness. SIAM Journal on
    Computing, 37(1):210–239, 2007.

[9] M. Szegedy. Quantum speed-up of markov chain based algorithms. In Proc. of the
    45th Annual IEEE Symposium on Foundations of Computer Science, FOCS ’04, pages
    32–41, Washington, DC, 2004.

[10] F. Magniez, M. Santha, and M. Szegedy. Quantum algorithms for the triangle prob-
    lem. SIAM Journal on Computing, 37(2):413–424, 2007.

[11] A. M. Childs and J. M. Eisenberg. Quantum algorithms for subset finding. Quantum
    Info. Comput., 5(7):593–604, 2005.

[12] S. Kutin. Quantum lower bound for the collision problem with small range. Theory
    of Computing, 1:29–36, 2005.

[13] G. Brassard, P. Høyer, and A. Tapp. Quantum cryptanalysis of hash and claw-free
    functions. In Proc. of LATIN’98: Theoretical Informatics: Third Latin American
    Symposium, Campinas, pages 163–169, 1998.

[14] M. Santha. Quantum walk based search algorithms. In Proc. of Theory and Appli-
    cations of Models of Computation: 5th International Conference, TAMC 2008, Xi’an,
    pages 31–46, 2008.

[15] A. M. Childs. On the relationship between continuous- and discrete-time quantum
    walk. Communications in Mathematical Physics, 294(2):581–603, 2010.

[16] E. Farhi and S. Gutmann. Quantum computation and decision trees. Phys. Rev. A,
    58:915–928, 1998.



                                          13
[17] A. Belovs. Learning-graph-based quantum algorithm for k-distinctness. In Proc.
    of 2012 IEEE 53rd Annual Symposium on Foundations of Computer Science, pages
    207–216, 2012.

[18] A. Belovs, A. M. Childs, S. Jeffery, R. Kothari, and F. Magniez. Time-efficient
    quantum walks for 3-distinctness. In Proc. of Automata, Languages, and Programming:
    40th International Colloquium, ICALP 2013, Riga, pages 105–122, 2013.

[19] A. Rosmanis. Quantum adversary lower bound for element distinctness with small
    range. Chicago Journal of Theoretical Computer Science, 2014(4), 2014.

[20] M. Kaplan. Quantum attacks against iterated block ciphers. Mat. Vopr. Kriptogr.,
    7:71–90, 2016.

[21] S. Jeffery, F. Magniez, and R. de Wolf. Optimal parallel quantum query algorithms.
    Algorithmica, 79(2):509–529, 2017.

[22] R. Portugal, R. A. M. Santos, T. D. Fernandes, and D. N. Gonçalves. The staggered
    quantum walk model. Quantum Information Processing, 15(1):85–101, 2016.

[23] R. Portugal. Establishing the equivalence between Szegedy’s and coined quantum
    walks using the staggered model. Quantum Information Processing, 15(4):1387–1409,
    2016.

[24] R. Portugal. Staggered quantum walks on graphs. Phys. Rev. A, 93:062335, 2016.

[25] Alexandre S. Abreu. Tesselações em grafos e suas aplicações em computação quântica.
    Master’s thesis, UFRJ, 2017.

[26] N. Shenvi, J. Kempe, and K. B. Whaley. A quantum random walk search algorithm.
    Phys. Rev. A, 67(5):052307, 2003.

[27] A. Ambainis, J. Kempe, and A. Rivosh. Coins make quantum walks faster. In Proc.
    Sixteenth Annual ACM-SIAM Symposium on Discrete Algorithms, SODA, pages 1099–
    1108, 2005.

[28] A. Tulsi. General framework for quantum search algorithms. Phys. Rev. A, 86:042331,
    2012.

[29] Renato Portugal. Quantum Walks and Search Algorithms. Springer, New York, 2013.

[30] Douglas B. West. Introduction to Graph Theory. Prentice Hall, 2000.

[31] A. Brandstädt, V. B. Le, and J. P. Spinrad. Graph Classes: A Survey. SIAM,
    Philadelphia, 1999.

[32] Frank Harary. Graph Theory. Addison-Wesley, Massachusetts, 1969.




                                              14

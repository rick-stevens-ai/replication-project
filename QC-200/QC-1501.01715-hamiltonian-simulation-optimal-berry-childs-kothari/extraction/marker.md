<!--
NOTE: Marker is not installed on this host (CherryRd) and the paper is not
present in the central _LUCID100_ADMIN/marker_md_uicgpu_20260622/ corpus.
This file is a pdftotext-derived proxy fallback per the QC wave brief's
"else run Marker" clause; the run was not launched here because Marker
requires a GPU box (uicgpu) that was not tasked for a single-paper
extraction (per the "small OCR -> uicgpu / large OCR -> Polaris" rule).
Content below is `pdftotext -layout paper.pdf` output, header/footer
noise preserved to keep parity with a real Marker run's raw fidelity.
Source: arXiv:1501.01715v3 (Berry, Childs, Kothari 2015).
-->

# Hamiltonian simulation with nearly optimal dependence on all parameters

**Authors:** Dominic W. Berry (Macquarie), Andrew M. Childs (Waterloo/UMD), Robin Kothari (Waterloo/MIT)
**arXiv:** 1501.01715v3 (7 Dec 2015)
**Extraction:** pdftotext -layout fallback (Marker unavailable on this host)

</br>

<!-- content: full pdftotext dump -->
                                                                     Hamiltonian simulation with nearly
                                                                    optimal dependence on all parameters
                                                          Dominic W. Berry ∗            Andrew M. Childs †‡            Robin Kothari §¶




arXiv:1501.01715v3 [quant-ph] 7 Dec 2015
                                                                                             Abstract
                                                       We present an algorithm for sparse Hamiltonian simulation whose complexity is optimal (up
                                                   to log factors) as a function of all parameters of interest. Previous algorithms had optimal or
                                                   near-optimal scaling in some parameters at the cost of poor scaling in others. Hamiltonian
                                                   simulation via a quantum walk has optimal dependence on the sparsity at the expense of poor
                                                   scaling in the allowed error. In contrast, an approach based on fractional-query simulation
                                                   provides optimal scaling in the error at the expense of poor scaling in the sparsity. Here we
                                                   combine the two approaches, achieving the best features of both. By implementing a linear
                                                   combination of quantum walk steps with coefficients given by Bessel functions, our algorithm’s
                                                   complexity (as measured by the number of queries and 2-qubit gates) is logarithmic in the
                                                   inverse error, and nearly linear in the product τ of the evolution time, the sparsity, and the
                                                   magnitude of the largest entry of the Hamiltonian. Our dependence on the error is optimal, and
                                                   we prove a new lower bound showing that no algorithm can have sublinear dependence on τ .


                                           1       Introduction
                                           The problem of simulating the dynamics of quantum systems was the original motivation for quan-
                                           tum computers [19] and remains one of their major potential applications. Although classical
                                           algorithms for this problem are inefficient, a significant fraction of the world’s computing power
                                           today is spent in solving instances of this problem that arise in, e.g., quantum chemistry and ma-
                                           terials science [25, 26]. Furthermore, efficient classical algorithms for this problem are unlikely
                                           to exist: since the simulation problem is BQP-complete [20], an efficient classical algorithm for
                                           quantum simulation would imply an efficient classical algorithm for any problem with an efficient
                                           quantum algorithm (e.g., integer factorization [29]).
                                               The first explicit quantum simulation algorithm, due to Lloyd [24], gave a method for simulating
                                           Hamiltonians that are sums of local interaction terms. Aharonov and Ta-Shma gave an efficient
                                           simulation algorithm for the more general class of sparse Hamiltonians [2], and much subsequent
                                           work has given improved simulations [5, 6, 7, 8, 11, 12, 16, 28, 30]. Sparse Hamiltonians include
                                           most physically realistic Hamiltonians as a special case (making these algorithms potentially useful
                                           for simulating real-world systems). In addition, sparse Hamiltonian simulation can be used to
                                               ∗
                                                Department of Physics and Astronomy, Macquarie University, Sydney, Australia. dominic.berry@mq.edu.au
                                               †
                                                Department of Combinatorics & Optimization and Institute for Quantum Computing, University of Waterloo,
                                           Waterloo, Ontario, Canada.
                                              ‡
                                                Department of Computer Science, Institute for Advanced Computer Studies, and Joint Center for Quantum
                                           Information and Computer Science, University of Maryland, College Park, Maryland, USA. amchilds@umd.edu
                                              §
                                                David R. Cheriton School of Computer Science and Institute for Quantum Computing, University of Waterloo,
                                           Waterloo, Ontario, Canada.
                                              ¶
                                                Center for Theoretical Physics, Massachusetts Institute of Technology, Cambridge, Massachusetts, USA.
                                           rkothari@mit.edu


                                                                                                 1
design other quantum algorithms [13, 14, 21]. For example, it was used to convert the algorithm
for evaluating a balanced binary NAND tree with n leaves [17] to the discrete-query model [14].
     In the Hamiltonian simulation problem, we are given an n-qubit Hamiltonian H (a Hermitian
matrix of size 2n × 2n ), an evolution time t, and a precision ǫ > 0, and are asked to implement
the unitary operation e−iHt up to error at most ǫ (as quantified by the diamond norm distance).
That is, the task is to implement a unitary operation, rather than simply to generate [3] or convert
[23] a quantum state. We say that H is d-sparse if it has at most d nonzero entries in any row.
In the sparse Hamiltonian simulation problem, H is specified by a black box that takes input
(j, ℓ) ∈ [2n ] × [d] (where [d] := {1, . . . , d}) and outputs the location and value of the ℓth nonzero
entry in the jth row of H. Specifically, as in [6], we assume access to an oracle OH acting as

                                       OH |j, k, zi = |j, k, z ⊕ Hjk i                              (1)

for j, k ∈ [2n ] and bit strings z representing entries of H, and another oracle OF acting as

                                          OF |j, ℓi = |j, f (j, ℓ)i,                                (2)

where f (j, ℓ) : [2n ] × [d] → [2n ] is a function giving the column index of the ℓth nonzero element
in row j. Note that the form of OF assumes that the locations of the nonzero entries of H can
be computed in place. This is possible if we can efficiently compute both (j, ℓ) 7→ f (j, ℓ) and the
reverse map (j, f (j, ℓ)) 7→ ℓ, which holds in typical applications of sparse Hamiltonian simulation.
Alternatively, if f provides the nonzero elements in order, we can compute the reverse map with
only a log d overhead by binary search.
     At present, the best algorithms for sparse Hamiltonian simulation, in terms of query complexity
(i.e., the number of queries made to the oracles) and number of 2-qubit gates used, are one based
on a Szegedy quantum walk [6, 12] and another based on simulating an unconventional model of
query complexity called the fractional-query model [7]. An algorithm with similar complexity to [7]
is based on implementing a Taylor series of the exponential [8]. The quantum walk approach has
                                    √
query complexity O(dkHkmax t/ ǫ), which is linear in both the sparsity d and the evolution time t.
(Here kHkmax denotes the largest entry of H in absolute value.) However, this approach has poor
dependence on the allowed error ǫ. In contrast, the fractional-query approach has query complexity
O dτ loglog(τ /ǫ)
          log(τ /ǫ) , where τ
                              := dkHkmax t. This approach gives exponentially better dependence on the
error at the expense of quadratically worse dependence on the sparsity. Considering the fundamental
importance of quantum simulation, it is desirable to have a method that achieves the best features
of both approaches. In this work, we combine the two approaches, giving the following.

Theorem 1. A d-sparse Hamiltonian H acting on n qubits can be simulated for time t within error
ǫ with                                               
                                          log(τ /ǫ)
                                   O τ                                                      (3)
                                        log log(τ /ǫ)
queries and                                                                   
                                                 5/2             log(τ /ǫ)
                                 O τ [n + log          (τ /ǫ)]                                      (4)
                                                               log log(τ /ǫ)
additional 2-qubit gates, where τ := dkHkmax t.

    This result provides a strict improvement over the query complexity of [7, 8], removing a factor
of d in τ , and thus providing near-linear instead of superquadratic dependence on d.
    We also prove a lower bound showing that any algorithm must use Ω(τ ) queries. While a lower
bound of Ω(t) was known previously [5], our new lower bound shows that the complexity must

                                                        2
be at least linear in the product of the sparsity and the evolution time. Our proof is similar to a
previous limitation on the ability of quantum computers to simulate non-sparse Hamiltonians [15]:
by replacing each edge in the graph of the Hamiltonian by a complete bipartite graph Kd,d , we
effectively boost the strength of the Hamiltonian by a factor of d at the cost of making the matrix
less sparse by a factor of d. Combining this result with the error-dependent lower bound of [7], we
find a lower bound as follows.

Theorem 2. For any ǫ, t > 0, integer d ≥ 2, and fixed value of kHkmax , there exists a d-sparse
Hamiltonian H such that simulating H for time t with precision ǫ has query complexity
                                                       
                                             log(1/ǫ)
                                   Ω τ+                   .                                 (5)
                                           log log(1/ǫ)

    Thus our result is near-optimal for the scaling in either τ or ǫ on its own. However, our upper
bound (3) has a product, whereas the lower bound (5) has a sum. It remains an open question how
to close the gap between these bounds. Intriguingly, a slight modification of our technique gives
another algorithm with the following complexity.

Theorem 3. For any α ∈ (0, 1], a d-sparse Hamiltonian H acting on n qubits can be simulated for
time t within error ǫ with query complexity

                                   O τ 1+α/2 + τ 1−α/2 log(1/ǫ) .
                                                               
                                                                                            (6)

    This result provides a nontrivial tradeoff between the parameters t, d, and ǫ, and suggests that
further improvements to such tradeoffs may be possible.
    We now informally describe the key idea behind our algorithms. For simplicity, suppose that the
entries of the Hamiltonian are small, satisfying kHkmax ≤ 1/d, and t = 1. Previous work on Hamil-
tonian simulation [6, 12] has shown that using a constant number of queries, we can construct a
unitary U whose top-left block (in some basis) is exactly e−i arcsin(H) . Technical difficulties aside, the
essential problem is to implement the unitary e−iH given the ability to perform e−i arcsin(H) . While it
is not clear how to express e−iH as a product of easy-to-implement unitaries and e−i arcsin(H) , it can
be approximated by a linear combination of powers of e−i arcsin(H) . Although such a decomposition
may not seem natural, we show that nevertheless it leads to an efficient implementation.
    In the next section we present a more technical overview of this high-level idea. In Section 3 we
analyze and prove the correctness of our algorithms. Section 4 proves the lower bound presented
in Theorem 2 and we conclude with some discussion in Section 5.


2    Overview of algorithms
Our algorithm uses a Szegedy quantum walk as in [6, 12], but with a linear combination of dif-
ferent numbers of steps. Such an operation can be implemented using the techniques that were
developed to simulate the fractional-query model [7]. This allows us to introduce a desired phase
more accurately than with the phase estimation approach of [6, 12]. As in [7], we first implement
the approximated evolution for some time interval with some amplitude and then use oblivious am-
plitude amplification to make the implementation deterministic, facilitating simulations for longer
times. In the rest of this section, we describe the approach in more detail.
    References [6, 12] define a quantum walk step U that depends on the Hamiltonian H to be
simulated. In turn, this quantum walk step is based on a state preparation procedure that only
requires one call to the sparse Hamiltonian oracle, avoiding the need to decompose H into a sum of


                                                    3
terms as in product-formula approaches. Two copies of the Hilbert space acted on by H are used.
First, the initial state is in one of these Hilbert spaces. Then, the state preparation procedure is
used to map the initial state onto the joint Hilbert space. This state preparation acts on the second
copy of the Hilbert space, controlled by the state in the first Hilbert space. The quantum walk
steps take place in this joint Hilbert space. Finally, the controlled state preparation is inverted to
map the final state back to the first Hilbert space.
    In the controlled state preparation, each eigenstate of H is mapped onto a superposition of two
eigenstates |µ± i of the quantum walk step U . The precise definition of U is not needed here; for
our application, it suffices to observe that the eigenvalues µ± of U are related to the eigenvalues λ
of H via
                                         µ± = ±e±i arcsin(λ/Xd) ,                                  (7)
where X ≥ kHkmax is a parameter that can be increased to make the steps of the quantum walk
closer to the identity. For small λ/Xd, the steps of the quantum walk yield a phase factor that
is nearly proportional to that for the Hamiltonian evolution. However, the phase deviates from
the desired value since the function arcsin ν is not precisely linear about ν = 0. Also, there are
two eigenvalues µ± , and in previous approaches it was necessary to distinguish between these to
approximate Hamiltonian evolution [6, 12]. In contrast, for the new technique we present here it is
not necessary to distinguish the eigenspaces.
     An obvious way to increase the accuracy is to increase X above its minimum value of kHkmax .
However, the number of steps of the quantum walk is O(tXd), so increasing X results in a less
efficient simulation. Another approach is to use phase estimation to correct the phase factor [6, 12],
but this approach still gives polynomial dependence on 1/ǫ.
     Instead, we propose using a superposition of steps of the quantum walk to effectively linearize
the arcsin function. Specifically, rather than applying U , we apply
                                                 k
                                                 X
                                         Vk :=          am U m                                     (8)
                                                 m=−k

for some coefficients a−k , . . . , ak . We show that the coefficients can be chosen by considering the
generating function for the Bessel function [1, 9.1.41],
                          ∞                                
                          X                       z        1
                                Jm (z)µm
                                       ± = exp       µ± −       = eiλz/Xd ,                        (9)
                         m=−∞
                                                  2       µ±

where the second equality follows from (7). Because the right-hand-side does not depend on whether
the eigenvalue of U is µ+ or µ− , there is no need to distinguish the eigenspaces. Thus the ability
to perform the operation
                                            ∞
                                            X
                                                 Jm (z)U m                                    (10)
                                           m=−∞

would allow us to exactly implement the evolution under H for time −z/Xd. Because of the minus
sign, we will take z to be negative to obtain positive time. By truncating the sum in (10) to some
finite range {−k, . . . , k}, we obtain an expression in which each term can be performed using at
most k queries. Because the Bessel function falls off exponentially for large |m|, we can obtain error
at most ǫ with a cutoff k that is only logarithmic in 1/ǫ.
    A linear combination of unitaries (LCU) such as (8) can be implemented using the LCU Lemma
(Lemma 4) described in the next section. The high-level intuition for the procedure is as follows.
We prepare ancilla qubits in a superposition encoding the coefficients of the linear combination

                                                  4
and then perform the unitary operations of the linear combination in superposition, controlled by
the ancilla. One could then obtain Vk by postselecting on an appropriate ancilla state. Instead, to
obtain Vk deterministically, we apply the oblivious amplitude amplification procedure introduced
in [7]. Rather than using Vk to implement evolution over the entire time, we break the time up
into shorter time steps we call “segments” (named by analogy to the segments used in [7]) and use
Vk to achieve the time evolution for each segment.
    The complexity of our algorithm is the number of segments (tXd/|z|) times the complexity for
each segment (k) times the number of steps needed for oblivious amplitude amplification (a). We
have some freedom in choosing z, which controls the amount of evolution time simulated by each
segment. To obtain near-linear dependence on the evolution time t, we choose z = O(1). Then
amplitude amplification requires O(1) steps, and the number of segments needed is O(τ ), giving
the linear factor in (3). The value of k needed to achieve overall error at most ǫ is logarithmic in
τ /ǫ, yielding the logarithmic factor in (3).
    An alternative approach is to use a larger segment that scales with τ . Choosing z = −τ α for
α ∈ (0, 1], we need k = O(τ α + log(1/ǫ)). Then we require O(τ 1−α ) segments and O(τ α/2 ) steps of
amplitude amplification, giving the scaling presented in Theorem 3.


3     Analysis of algorithms
3.1    A quantum walk for any Hamiltonian
We begin by reviewing the quantum walk defined in [7, 12]. Given a Hamiltonian H acting on
CN (where N := 2n ), the Hilbert space is expanded to C2N ⊗ C2N . First, an ancilla qubit in the
state |0i is appended, which expands the space from CN to C2N . Then the entire Hilbert space is
duplicated, giving C2N ⊗ C2N . This is achieved using the isometry
                                          N
                                          X −1       X
                                   T :=                  (|jihj| ⊗ |bihb|) ⊗ |ϕjb i                             (11)
                                          j=0 b∈{0,1}

with |ϕj1 i = |0i|1i and
                                                         s                 s                 !
                                                              ∗
                                                             Hjℓ                      ∗|
                                                                                    |Hjℓ
                                        1 X
                             |ϕj0 i := √       |ℓi                 |0i +       1−          |1i ,                (12)
                                         d ℓ∈F               X                       X
                                                 j


where X ≥ kHkmax and Fj is the set of indices of nonzero elements in column j of H. Here we use
the convention that the first subsystem is the original space, the next is the ancilla qubit, and the
third and fourth subsystems are the duplicated space and duplicated ancilla qubit, respectively.
This operation can be viewed as a controlled state preparation, creating state |ϕj0 i on input |ji|0i.
If the ancilla qubit is in the state |1i, then |0i|1i is prepared. Starting with the initial space, the
controlled state preparation is performed, and then steps of the quantum walk are applied using
the unitary
                                           U := iS(2T T † − I),                                    (13)
where S swaps the two registers (i.e., S|j1 i|j2 i|ℓ1 i|ℓ2 i = |ℓ1 i|ℓ2 i|j1 i|j2 i for all j1 , ℓ1 ∈ [N ], j2 , ℓ2 ∈
{0, 1}). Finally, the inverse state preparation T † is performed. For a successful simulation, the
output should lie in the original space, and the ancilla should be returned to the state |0i.
    Let λ be the eigenvalue of H with eigenstate |λi, and let ν := λ/Xd be the corresponding scaled
eigenvalue for the quantum walk. The steps of the quantum walk U satisfy U |µ± i = µ± |µ± i [12]

                                                             5
with

                                  |µ± i := (T + iµ± ST )|λi,                                        (14)
                                             p
                                    µ± := ± 1 − ν 2 + iν = ±e±i arcsin ν .                          (15)

To apply the steps of the quantum walk to approximate Hamiltonian evolution, there are two
challenges: we must handle both the |µ+ i and |µ− i sectors, and correct the applied phase. In this
work we are able to solve both these challenges at once by using a superposition of steps of the
quantum walk.

3.2    Linear combination of unitaries
We now describe how to perform a linear combination of unitary operations. Given an M -tuple
                      ~ = (U1 , . . . , UM ), we quantify the complexity of implementing a linear
of unitary operations U
combination of the Um s in terms of the number of invocations of
                                                       M
                                             ~ ) :=
                                                       X
                                      select(U               |mihm| ⊗ Um .                          (16)
                                                       m=1

Such a result was previously given in [8, 22]. Here we formalize that result and generalize to allow
more steps of oblivious amplitude amplification. The overall result is as given in the following
lemma.
                                ~ = (U1 , . . . , UM ) be unitary operations and let Ṽ = M am Um
                                                                                           P
Lemma 4 (LCU Lemma). Let U                                                                   m=1
be δ-close to a unitary. We can approximate Ṽ to within O(δ)      using O(a) select(U~ ) and select(U
                                                                                                     ~ †)
                                                                PM
operations and O(M a) additional 2-qubit gates, where a := m=1 |am |.

    To prove this result, we first consider an operation that would give Ṽ with postselection, then
apply oblivious amplitude amplification to achieve it deterministically. The operation that provides
Ṽ with postselection is described in the following lemma.

Lemma
PM        5. Let ~
                 U = (U1 , P
                           . . . , UM ) be unitary operations acting on a Hilbert space H2 , let Ṽ =
                               M
  m=1 am Um , and let s ≥      m=1 |am | be a real number. Define a Hilbert space H1 to be a tensor
product of a qubit and a subspace of dimension M , and let |ςi := |0i|0i ∈ H1 . Then there exists a
unitary operation W acting on H1 ⊗H2 such that Z = 1s (|ςihς|⊗ Ṽ ), with Z := P W P , P := |ςihς|⊗I.
The operation W can be applied with O(1) select(U   ~ ) and select(U
                                                                   ~ † ) operations and O(M ) additional
2-qubit gates.

Proof. To perform W , we perform an operation that rotates the ancilla qubits from |ςi to the state
                                  r             r                M
                                       a                a       1 X√
                          |χi =          |0i +       1 − |1i ⊗ √     am |mi,                        (17)
                                       s                s        a    m=1

where a := M
             P
               m=1 |am |. This state is of dimension 2M and can be prepared from state |ςi using
O(M ) operations (which is trivial for |mi encoded in unary). Next we perform the controlled oper-
             ~ ). Finally, inverting the preparation of |χi and projecting onto |ςi would effectively
ation select(U
project the ancilla onto |χi. Then the unnormalized operation on H2 is Ṽ /s, corresponding to Z.
The action of applying the unitary operation to prepare |χi, the controlled operation select(U    ~ ),
and the inverse preparation gives the desired operation W .

                                                        6
    Next we provide a multi-step version of robust amplitude amplification, generalizing the single-
step version presented in [8]. In this lemma, and throughout this paper, k·k denotes the spectral
norm.

Lemma 6 (Robust oblivious amplitude amplification). Let W be a unitary matrix acting on H1 ⊗H2
and let P be the projector onto the subspace whose first register is |ςi := |0i|0i ∈ H1 , i.e., P :=
|ςihς| ⊗ I. Furthermore let Z := P W P satisfy Z = 1s (|ςihς| ⊗ Ṽ ), where Ṽ is δ-close to a unitary
                   π
matrix and sin 2(2ℓ+1)   = 1s for some ℓ ∈ N, and let R := −W (I − 2P )W † (I − 2P ). Then

                                    kP Rℓ W P − (|ςihς| ⊗ Ṽ )k = O(δ).                                 (18)

Proof. We start by considering a single iteration, as in [8]. Then we have

                          RW P = −W (I − 2P )W † (I − 2P )W P
                                 = −W P + 2W P + 2P W P − 4W P W † P W P
                                 = W P + 2Z − 4W Z † Z.                                                 (19)

Multiplying by P on the left gives

                      P RW P = −P W (I − 2P )W † (I − 2P )W P = 3Z − 4ZZ † Z,                           (20)

which matches the expression in [8].
   The general solution after m iterations is
                                             √                           √
                 m                   T2m+1 ( 1 − Z † Z)    (−1)m T2m+1 ( Z † Z)
               R W P = (W P − Z)         √              +Z        √             ,                       (21)
                                           1 − Z †Z                 Z †Z
where T2m+1 are Chebyshev polynomials of the first kind. (Because Chebyshev polynomials for
odd order only include odd powers, no square roots appear when (21) is expanded.)
    We establish (21) by induction. First note that it holds for m = 0, because T1 (x) = x, so the
right-hand side evaluates to W P . Next assume that it holds for a given m. It is straightforward to
show that

                      R(W P − Z) = (W P − Z)(1 − 2Z † Z) + 2Z(1 − Z † Z) and
                               RZ = (W P − Z)(−2Z † Z) + Z(1 − 2Z † Z).                                 (22)

Hence, multiplying both sides of (21) by R, we get
                   "                  √                                  √        #
                               T     (  1 −  Z † Z)       (−1)  mT      (  Z † Z)
                                2m+1                              2m+1
   Rm+1 W P = R (W P − Z)          √                 +Z           √
                                     1 − Z †Z                       Z †Z
                           "                      √                                       √         #
                                         T       (   1 − Z † Z)          (−1) mT         (  Z  † Z)
                                          2m+1                                    2m+1
              = (W P − Z) (1 − 2Z † Z)       √                  − 2Z † Z         √
                                                1 − Z †Z                            Z †Z
                     "                   √                                              √         #
                                  T     (  1 −   Z † Z)                 (−1)mT         (   Z † Z)
                                   2m+1                                         2m+1
                + Z 2(1 − Z † Z)      √                 + (1 − 2Z † Z)          √                   .   (23)
                                        1 − Z †Z                                  Z †Z

To progress further, we use the relation [1, 22.3.15]

                  T2m+1 (x) = cos[(2m + 1) arccos x] = (−1)m sin[(2m + 1) arcsin x].                    (24)

                                                      7
Using this we find that, with x = sin θ,
                                      √
                            2 T2m+1 ( 1 − x )
                                              2        (−1)m T2m+1 (x)
                    (1 − 2x )      √             − 2x2
                                     1 − x2                   x
                                           cos[(2m + 1)θ]
                       = (cos2 θ − sin2 θ)                − 2 sin θ sin[(2m + 1)θ]
                                                cos θ
                          cos(2θ) cos[(2m + 1)θ] − sin(2θ) sin[(2m + 1)θ]
                       =
                                                 cos θ
                          cos[(2m + 3)θ]
                       =
                               cos√θ
                          T2m+3 ( 1 − x2 )
                       =      √             .                                                  (25)
                                1 − x2
Next put x = cos φ to obtain
                           √
                  2 T2m+1 ( 1 − x )
                                    2               (−1)m T2m+1 (x)
          2(1 − x )     √              + (1 − 2x2 )
                          1 − x2                           x
                              m
                         (−1) sin[(2m + 1)φ]                        (−1)m cos[(2m + 1)φ]
             = 2(sin2 φ)                        − (cos2 φ − sin2 φ)
                                  sin φ                                    cos φ
                      sin(2φ)  sin[(2m  + 1)φ] − cos(2φ) cos[(2m  +  1)φ]
             = (−1)m
                                             cos φ
                         cos[(2m + 3)φ]
             = (−1)m+1
                              cos φ
                         T2m+3 (x)
             = (−1)m+1              .                                                          (26)
                             x
Using these relations, (23) simplifies to
                                          √                               √
                                   T     (  1 − Z † Z)    (−1)m+1 T      (  Z † Z)
                                    2m+3                           2m+3
              Rm+1 W P = (W P − Z)    √                +Z        √                 .           (27)
                                        1 − Z †Z                    Z †Z
Hence we find that, if (21) is correct for non-negative integer m, it is correct for m + 1. Hence it
is correct for all non-negative integers m by induction.
    Thus we find that by multiplying on the left by P , we obtain
                                                              √
                                     m         (−1)m T2m+1 ( Z † Z)
                                 PR WP = Z            √             .                          (28)
                                                         Z †Z

Then, in the case that δ = 0, i.e., if Ṽ is equal to a unitary V , we would have
                                                 1
                                            Z=     (|ςihς| ⊗ V ).                              (29)
                                                 s
Then Z † Z = (|ςihς| ⊗ I)/s2 , and we get
                                    √
                     (−1)m T2m+1 ( Z † Z)   1              (−1)m T2m+1 (1/s)
                  Z         √             = (|ςihς| ⊗ V )
                               Z †Z         s                     1/s
                                                             m
                                          = (|ςihς| ⊗ V )(−1) T2m+1 (1/s)
                                            = (|ςihς| ⊗ V ) sin[(2m + 1) arcsin(1/s)].         (30)


                                                     8
                                     π
                                           1
In the case m = ℓ, we can use sin 2(2ℓ+1)  = s to obtain sin[(2ℓ + 1) arcsin(1/s)] = 1, which implies

                                       P Rℓ W P = |ςihς| ⊗ V.                                    (31)

   Next, consider the case where Ṽ is only δ-close to being unitary. Let us define
                                              p
                                        ∆ := Ṽ † Ṽ − I.                                        (32)

We immediately obtain k∆k = O(δ), and
                               1               √       1
                                 (|ςihς| ⊗ ∆) = Z † Z − (|ςihς| ⊗ I).                            (33)
                               s                       s
We then get
                                  √
                     (−1)ℓ T2ℓ+1 ( Z † Z)   1               (−1)ℓ T2ℓ+1 ((I + ∆)/s)
                   Z        √             = (|ςihς| ⊗ Ṽ )
                              Z †Z          s                      (I + ∆)/s
                                                               ℓ
                                                           (−1) T2ℓ+1 ((I + ∆)/s)
                                          = (|ςihς| ⊗ Ṽ )                        .              (34)
                                                                   I+∆

Using (−1)ℓ T2ℓ+1 (x) = sin[(2ℓ + 1) arcsin x] and (−1)ℓ T2ℓ+1 (1/s) = 1, we obtain

                            k(−1)ℓ T2ℓ+1 ((I + ∆)/s) − Ik = O(ℓ2 δ2 /s2 ).                       (35)

Since ℓ = Θ(s), ℓ2 /s2 = O(1), which implies

                               k(−1)ℓ T2ℓ+1 ((I + ∆)/s) − Ik = O(δ2 ).                           (36)

The contribution to the error from I + ∆ is O(δ), so we have
                                           √
                              (−1)ℓ T2ℓ+1 ( Z † Z)
                            Z        √             − (|ςihς| ⊗ Ṽ ) = O(δ).                      (37)
                                       Z †Z

Using (28) we then get (18) as required.

    Lemma 6 is in terms of the spectral norm distance, but the diamond norm distance is at most
a constant factor larger. The specific result, proven in the Appendix, is as follows.

Lemma 7. Let U , V be operators satisfying kU k ≤ 1 and kV k ≤ 1, and let k · k⋄ denote the
diamond norm. Then kU − V k⋄ ≤ 2kU − V k. Furthermore, if V is a quantum channel with Kraus
decomposition V(ρ) = V ρV † + j Vj ρVj† and U (ρ) = U ρU † , then kU − Vk⋄ ≤ 4kU − V k.
                             P

   The LCU Lemma follows by combining Lemma 5 and Lemma 6.

Proof of Lemma 4. Using Lemma 5 we can implement the operation W required for Lemma 6 using
            ~ ) and select(U
O(1) select(U               ~ † ) operations and O(M ) additional 2-qubit gates. We can choose s ≥ a
                 π
                        = 1s for some ℓ ∈ N. Then Lemma 6 shows that Ṽ can be approximated to
                      
such that sin 2(2ℓ+1)
within O(δ) using O(ℓ) applications of W and the projection P . Since ℓ = O(s) = O(a), the total
number of select(U~ ) and select(U ~ † ) operations is O(a) and the number of additional 2-qubit gates
is O(M a).



                                                  9
3.3   Main algorithm
The main problem with applying the quantum walk as presented in [6, 12] is that arcsin ν is a
nonlinear function of ν, so an imprecise phase is introduced. To solve this, we use a superposition
of different numbers of applications of U . Define Vk as in (8), where the choice of {am }km=−k is
considered below. The eigenvalues of Vk corresponding to the eigenvalues µ± of U are
                                                      k
                                                      X
                                            µ±,k :=          am µ m
                                                                  ±.                               (38)
                                                      m=−k

In general µ±,k can depend on ±. However, we will choose am satisfying a−m = (−1)m am , which
yields µ±,k independent of ±.
    To see how to choose the coefficients am , solve (15) for ν to give
                                                           
                                              i          1
                                       ν=−        µ± −        .                          (39)
                                              2         µ±

This implies that, for any z,                               
                                      iνz          z        1
                                    e       = exp     µ± −       .                                 (40)
                                                   2       µ±
This corresponds to the standard generating function for the Bessel function [1, 9.1.41], so
                                                      ∞
                                         z        1       X
                           eiνz = exp       µ± −       =      Jm (z)µm
                                                                     ±.                            (41)
                                         2       µ±      m=−∞

Thus we can take am ≈ Jm (z). Because there are efficient classical algorithms to calculate Bessel
functions, the circuit to prepare |χk i can be designed efficiently. Note that for large m, we have
           1
|Jm (z)| ∼ m! |z/2|m [1, 9.3.1], so the values of am are similar to the coefficients in the expansion of
the exponential function. Thus the segments used here are analogous to the segments used in [8].
    To determine the complexity of this approach, we primarily need to bound the error in approx-
imating eiνz . To optimize the result, we use the coefficients

                                                       Jm (z)
                                            am := Pk                .                              (42)
                                                      j=−k Jj (z)

We make this choice because the most accurate results are obtained when the values of am sum to
1. Note also that this yields the symmetry a−m = (−1)m am , because J−m (z) = (−1)m Jm (z) [1,
9.1.5]. The sum of Jm (z) over all integers m is equal to 1 (which can be shown by putting t = 1 in
[1, 9.1.41]), but because k is finite, we normalize the values as in (42). With this choice, we have
the following error bound, proved in the Appendix.

Lemma 8. With the values am as in (42), for |z| ≤ k we have

                                               kHk (z/2)k+1
                                                           
                           kVk − V∞ k = O                     .                                    (43)
                                               Xd     k!

    Note that V∞ is the exact unitary operation desired. We now determine the query complexity
of this approach. In fact, we prove a result that is slightly tighter than the query complexity stated
in Theorem 1.


                                                      10
Lemma 9. A d-sparse Hamiltonian H acting on n qubits can be simulated for time t within error ǫ
with complexity (quantified by the number of 2-qubit operations and controlled-U and controlled-U †
operations)                                               
                                            log(kHkt/ǫ)
                                     O τ                     .                                 (44)
                                          log log(kHkt/ǫ)
Proof. Our main goal is to determine the value of k needed to bound the error by ǫ. This depends
on the length of time for the segments, which we can adjust by choosing the value of z. We wish
to perform each step deterministically with one step of oblivious amplitude amplification, so we
should have s = 2 in Lemma 6. Using the values of am given in (42), this means that we should
take z = O(1), and for concreteness z = −1/2 yields a < 2, so we can take s = 2. Then, using
Lemma 4 with Um = U m and Ṽ = Vk , we can approximate the operation Vk to within O(δ).
   Given an allowable error in a segment of δ > 0, let us take
                                                            
                                            log(kHk/Xdδ)
                                  k=O                          .                             (45)
                                          log log(kHk/Xdδ)

Then, using Lemma 8 and the inequality k! > (k/e)k , it is straightforward to show that the error in
each segment is no more than δ. Using Lemma 7, this bound on the error in terms of the spectral
norm distance implies a bound on the diamond norm distance that is at most a constant factor
larger. For the total error to be no more than ǫ, the value of δ can be no more than ǫ divided by
the number of segments. The number of segments is O(tXd), which gives
                                                            
                                              log(kHkt/ǫ)
                                     k=O                       .                               (46)
                                            log log(kHkt/ǫ)

   Using Lemma 4, the complexity of each segment is O(k) since a select(U      ~ ) operation can be
implemented with complexity O(M ), and M = 2k+1. It is straightforward to apply select(U    ~ ) using
                                    †
O(k) controlled-U and controlled-U operations. If |mi is encoded in unary, then each controlled
operation may be just controlled on one qubit of |mi.
   The number of segments required is O(tXd). It is most efficient to take the minimum value of
X, which is kHkmax . Because each segment uses O(k) controlled-U and controlled-U † operations,
as well as O(M ) = O(k) additional 2-qubit gates, the complexity for the simulation over time t is
O(τ k), Using the value of k from (46) gives the overall complexity stated in (44).

   Next we determine the gate complexity of this approach. Again we give a slightly tighter result
than presented in Theorem 1.

Lemma 10. A d-sparse Hamiltonian H acting on n qubits can be simulated for time t within error
ǫ using                                                         
                                                   log(kHkt/ǫ)
                       O τ [n + F (log(kHkt/ǫ))]                                          (47)
                                                 log log(kHkt/ǫ)
2-qubit gates, where F (m) is the complexity of performing elementary functions with m bits.

Proof. To obtain the gate complexity, we need to consider the procedure for performing the step U
in detail. We can perform T by first performing log d Hadamard gates to prepare the superposition
state
                                               d−1
                                            1 X
                                           √       |ℓi|0i.                                    (48)
                                             d ℓ=0


                                                 11
Here we take d to be a power of 2 without loss of generality. (The value of d can always be rounded
up to the nearest power of two.) Then the oracle OF (from (2)) can be used to produce the state
                                             1 X
                                            √       |ℓi|0i.                                        (49)
                                              d ℓ∈F
                                                    j


A call to the oracle OH for the value of an element of the Hamiltonian (from (1)) then gives the
value of Hjℓ in an ancilla space. Another ancilla qubit is rotated from |0i to
                                    s            s
                                         ∗
                                       Hjℓ                ∗|
                                                       |Hjℓ
                                           |0i + 1 −         |1i                            (50)
                                       X                 X
based on the value of Hjℓ . Then inverting the oracle OH erases the value of Hjℓ from the ancilla
space. Note that there is a sign ambiguity for the square root when Hjℓ takes negative real values.
This is addressed in [6] and does not affect the complexity.
    To perform the step U , we also require the swap operation S, which has complexity O(n) due
to the number of qubits. The gate complexity is O(n) from S, plus O(log d) = O(n) from the
Hadamard gates, plus the complexity of performing the rotations to obtain the state (50). The
complexity of the rotations depends on the number of bits of precision used for the entries of H.
To obtain overall error O(ǫ), the number of bits must be log(kHkt/ǫ). To determine the rotations
needed, we must also compute a square root and trigonometric functions on the output of the oracle.
If these functions can be computed with complexity F (m) for m-bit inputs, the contribution to the
overall complexity is F (log(kHkt/ǫ)).
    In Lemma 9 the complexity is quantified in terms of the number of controlled-U and controlled-
U † operations, so to obtain the overall gate complexity we just need to multiply that complexity
by the cost of U . There is also a cost in terms of additional 2-qubit gates in Lemma 9, but
that is smaller than the gate cost of performing U . Therefore, the gate complexity is equal to
the complexity from Lemma 9 times O(n + F (log(kHkt/ǫ))), which gives a gate complexity as in
(47).

    This result depends on the complexity of elementary functions, F (m), needed to calculate
the rotations. Using advanced techniques, F (m) may be made close to linear in m [10], though
such advanced techniques only give an improvement for extremely high precision. Using simple
techniques based on Taylor series and long multiplication, F (m) = O(m5/2 ).
    The classical complexity of determining the coefficients {am }km=−k is also potentially significant.
A set of values of the Bessel function can be efficiently computed using Miller’s recurrence algorithm
[9, 27]. The complexity scales as k (the number of entries) times log(kHkt/ǫ) (the bits of precision
needed for each Jm (z)). This is no larger than the quantum gate complexity.
    Note that the gate complexity in Lemma 10 depends linearly on n, whereas the query complexity
in Theorem 1 does not. This is because performing an operation on a target state with n qubits
must require at least Ω(n) gates. In contrast, the number of queries need not scale with n, because
the queries are used to determine which gates to perform. There is an implicit complexity of Ω(n)
for the queries, because the input to a query is of size at least n.
    The proof of Theorem 1 then follows immediately.

Proof of Theorem 1. The implementation of U uses O(1) oracle calls, which means that the query
complexity is the same as the number of controlled applications of U . Noting that kHk ≤ dkHkmax ,
Lemma 9 implies the query complexity in Theorem 1, and Lemma 10 with F (m) = O(m5/2 ) implies
the gate complexity in Theorem 1.

                                                  12
3.4   A tradeoff between τ and ǫ
The alternative algorithm characterized by Theorem 3 uses larger segments with z ∝ −τ α for
α ∈ (0, 1]. The case α = 0 corresponds to the case considered above, whereas α = 1 corresponds to
a single segment. The analysis of this section assumes α > 0.
    To analyze this algorithm, we first need to bound the absolute sum of Bessel functions.

Lemma 11. The quantity
                                                   ∞
                                                   X
                                         S(z) :=          |Jm (z)|                               (51)
                                                   m=−∞
     p
is O( |z|).

   We prove this in the Appendix. Using the robust version of amplitude amplification given in
Lemma 6, we obtain the bound in Theorem 3.

Proof of Theorem 3. Using Lemma 8, Stirling’s formula, and the fact that kHk ≤ dkHkmax ≤ Xd,
we find that for |z| ≤ k the error is bounded as

                                  kVk − V∞ k = O (e/k)k (z/2)k+1 .
                                                                
                                                                                         (52)

By Lemma 6, the error in a segment after amplitude amplification is of the same order. Therefore,
to ensure that the error in a segment is at most δ, it suffices to take

                            k = O(|z| + log(1/δ)) = O(τ α + log(1/δ)).                           (53)

With this value of k, we have km=−k Jm (z) = 1 + O(δ), so Lemma 11 gives
                              P

                                   k
                                   X                         p
                                         |am | = O(S(z)) = O( |z|).                              (54)
                                  m=−k

This corresponds to thepnumber of steps of oblivious amplitude amplification. The overall com-
plexity is therefore O(k |z|) = O(kτ α/2 ) for a single segment.
    The number of segments is τ /|z| ∝ τ 1−α . This means that the complexity is O(kτ 1−α/2 ).
The value of k also depends on the number of segments. We can take δ = ǫ/τ 1−α , which gives
k = O(τ α + log(1/ǫ)), implying the result in Theorem 3.

    In this proof we have ignored log τ in comparison to τ α , which would not be valid for α = 0. For
the gate complexity, we again have a multiplying factor of n + F (log(kHkt/ǫ)), yielding a number
of gates scaling as
                        O [n + F (log(kHkt/ǫ))] τ 1+α/2 + τ 1−α/2 log(1/ǫ) .
                                                                          
                                                                                                  (55)


4     Lower bound
We now present a lower bound showing that the dependence of our algorithm on τ := dkHkmax t
is nearly optimal (and that the dependence of [6] on τ is optimal). The main idea of the proof is
the same as in Theorem 3 of [15], but we slightly adapt that argument to let t vary independently
of d. Note that this is stronger than proving separate lower bounds of Ω(t) and Ω(d), since that
would only show a lower bound of Ω(d + t), which is weaker than our Ω(td) lower bound.



                                                    13
Lemma 12. For any positive integer d and any t > 0, there exists a 2d-sparse Hamiltonian H with
kHkmax = Θ(1) such that simulating H with constant precision for time t requires Ω(td) queries.

Proof. Similarly to the Ω(t) lower bound from [5], we construct a sparse Hamiltonian whose dy-
namics compute the parity of a bit string, and we use the fact that at least N/2 quantum queries
are needed to compute the parity of N bits [4, 18].
    First consider a Hamiltonian H1 whose graph is a path with N + 1 vertices. (Here the graph
of H has a vertex for each basis state and an edge between two vertices if the corresponding entry
of H is nonzero.) The Hamiltonian acts on vectors |ii with i ∈ {0, . . . , N } and has nonzero matrix
elements
                                                          p
                           hi − 1|H1 |ii = hi|H1 |i − 1i = i(N − i + 1)                          (56)

for i ∈ [N ]. Simulating H1 for time π/2 starting with the state |0i gives the state |N i (i.e.,
e−iH1 π/2 |0i = |N i).
    Next, consider a Hamiltonian H2 generated from a string x ∈ {0, 1}N as in [5]. H2 acts on
vertices |i, ji with i ∈ {0, . . . , N } and j ∈ {0, 1} and has nonzero matrix elements
                                                                            p
                     hi − 1, j|H2 |i, j ⊕ xi i = hi, j ⊕ xi |H2 |i − 1, ji = i(N − i + 1) (57)

for all i ∈ [N ] and j ∈ {0, 1}. By construction, |0, 0i is connected to |i, ji if and only if j = x1 ⊕· · ·⊕
xi . In particular, |0, 0i is connected to |N, x1 ⊕ · · · ⊕ xN i, and determining whether it is connected
to |N, 0i or |N, 1i determines the parity of x. The graph of H2 consists of two disjoint paths,
one containing |0, 0i and |N, x1 ⊕ · · · ⊕ xN i. Thus we have e−iH2 π/2 |0, 0i = |N, x1 ⊕ · · · ⊕ xN i, so
evolution for time π/2 computes the parity of x.
     Finally, we construct the Hamiltonian H claimed in the lemma. As before, H is generated from
a string x ∈ {0, 1}N . H acts on vertices |i, j, ℓi with i ∈ {0, . . . , N }, j ∈ {0, 1}, and ℓ ∈ [d]. The
nonzero entries of H are

                hi − 1, j, ℓ|H|i, j ⊕ xi , ℓ′ i = hi, j ⊕ xi , ℓ′ |H|i − 1, j, ℓi = i(N − i + 1)/N
                                                                                   p
                                                                                                        (58)

for all i ∈ [N ], j ∈ {0, 1}, and ℓ, ℓ′ ∈ [d]. The graph of H is similar to that of H2 , except that for
each vertex in H2 , there are now d copies of it in H. Each vertex is connected to all d copies of
its neighboring vertices, so the graph has maximum degree 2d. Observe that, having divided the
matrix elements by N , we have kHkmax = Θ(1).
    Now we simulate the Hamiltonian starting from the state |0, 0, ∗i, where |i, j, ∗i := √1
                                                                                                  P
                                                                                                d   ℓ |i, j, ℓi
denotes a uniform superposition over the third register. The subspace span{|i, j, ∗i : i ∈ {0, . . . , N },
j ∈ {0, 1}} is an invariant subspace of H. Since the initial state lies in this subspace, the quantum
walk remains in this subspace. The nonzero matrix elements of H in this invariant subspace are
                                                                               p
              hi − 1, j, ∗|H|i, j ⊕ xi , ∗i = hi, j ⊕ xi , ∗|H|i − 1, j, ∗i = d i(N − i + 1)/N,          (59)

so we have e−iHt |0, 0, ∗i = |N, x1 ⊕ · · · ⊕ xN , ∗i for t = N π/2d. Since this determines the parity of
x, we find a lower bound of Ω(N ) = Ω(td) as claimed.

    It is now straightforward to use this result to prove Theorem 2.

Proof of Theorem 2. We choose one of two Hamiltonians depending on whether the first or second
term in (5) is larger. If τ is larger, then we use Lemma 12. The value of d used in Lemma 12 is
denoted d′ here, to distinguish it from the d given in Theorem 2. Taking d′ = ⌊d/2⌋, we ensure


                                                      14
that d′ is a positive integer, because d ≥ 2. Then Lemma 12 shows that there is a 2d′ -sparse
Hamiltonian; given this value of d′ , this Hamiltonian is also d-sparse, as required for Theorem 2.
    For Theorem 2, we are also given a required value for kHkmax . The Hamiltonian used in
Lemma 12 has kHkmax = Θ(1). By multiplying that Hamiltonian by a scaling factor, we obtain a
Hamiltonian with the required value of kHkmax . Dividing the time used in Lemma 12 by the same
factor, the simulation requires time Ω(τ ) for constant precision. In Theorem 2 we require precision
ǫ, which can only increase the complexity.
    In the case where the second term is larger, we use Theorem 6.1 of [7]. There it is shown that
performing a simulation of a 2-sparse Hamiltonian with precision ǫ and kHkmax t = O(1) requires
                                                           
                                                 log(1/ǫ)
                                           Ω                                                    (60)
                                               log log(1/ǫ)

queries. Because d ≥ 2, this Hamiltonian is also d-sparse. As using larger values of kHkmax t can
only increase the complexity, we also have this lower bound in the more general case. Therefore,
regardless of whether the first or second term in (5) is larger, this expression provides a lower bound
on the complexity.

   It is also possible to combine our lower bound with the lower bound of [7] to obtain a combined
lower bound in terms of d, t, and ǫ, that is stronger than Theorem 2. This yields a lower bound
of Ω(N ) for any N that satisfies ǫ < 12 |sin(td/N )|N . Note that when ǫ is a constant, we recover
Lemma 12 and when td is constant, we recover (60). However, for intermediate values this lower
bound can be strictly larger than the expression in Theorem 2.


5    Conclusion
Our technique for Hamiltonian simulation combines ideas from quantum walks and fractional-
query simulation to provide improved performance over both previous techniques. As a result, it
provides near-optimal scaling with respect to all parameters of interest. In particular, the scaling
is only slightly superlinear in τ = dkHkmax t, whereas we have proven that linear scaling is optimal.
Furthermore, the method has query complexity sublogarithmic in the allowed error, which was
proven to be optimal in [7].
    Nevertheless, there is still a gap between the complexity of our algorithm and the lower bound
in (5), as they involve different tradeoffs between the parameters τ and ǫ. It remains open whether
the performance can be further improved, perhaps to give performance similar to (5), although as
observed at the end of Section 4, we can rule out scaling strictly as in (5).
    Our technique can potentially be used for the more general task of operation conversion, in
which we use one quantum operation to implement another. In our work, we convert a step of
a quantum walk to Hamiltonian evolution, whereas in [21] the task is to convert Hamiltonian
evolution to an inverse. One approach to operation conversion is to use phase estimation. Here we
have shown that a superposition of operations can provide far better performance.


Acknowledgment
D.W.B. is funded by an ARC Future Fellowship (FT100100761). This work was also supported
in part by CIFAR, NSERC, the Ontario Ministry of Research and Innovation, and the US ARO
under ARO grant Contract Numbers W911NF-12-1-0482 and W911NF-12-1-0486. This preprint is
MIT-CTP #4631.

                                                  15
References
 [1] Milton Abramowitz and Irene A. Stegun, Handbook of mathematical functions, National Bu-
     reau of Standards, 1964.

 [2] Dorit Aharonov and Amnon Ta-Shma, Adiabatic quantum state generation and statistical zero
     knowledge, Proceedings of the 35th Annual ACM Symposium on Theory of Computing, pp. 20–
     29, June 2003.

 [3] Andris Ambainis, Loı̈ck Magnin, Martin Roetteler, and Jérémie Roland, Symmetry-assisted
     adversaries for quantum state generation, Proceedings of the 26th IEEE Conference on Com-
     putational Complexity, pp. 167–177, June 2011, arXiv:1012.2112.

 [4] Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca, and Ronald de Wolf,
     Quantum lower bounds by polynomials, Journal of the ACM 48 (2001), no. 4, 778–797,
     arXiv:quant-ph/9802049.

 [5] Dominic W. Berry, Graeme Ahokas, Richard Cleve, and Barry C. Sanders, Efficient quantum
     algorithms for simulating sparse Hamiltonians, Communications in Mathematical Physics 270
     (2007), no. 2, 359–371, arXiv:quant-ph/0508139.

 [6] Dominic W. Berry and Andrew M. Childs, Black-box Hamiltonian simulation and uni-
     tary implementation, Quantum Information and Computation 12 (2012), no. 1–2, 29–62,
     arXiv:0910.4157.

 [7] Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and Rolando D.
     Somma, Exponential improvement in precision for simulating sparse Hamiltonians, Proceed-
     ings of the 46th Annual ACM Symposium on Theory of Computing, pp. 283–292, May 2014,
     arXiv:1312.1414.

 [8]          , Simulating Hamiltonian dynamics with a truncated Taylor series, Physical Review
       Letters 114 (2015), no. 9, 090502, arXiv:1412.4687.

 [9] William G. Bickley, Leslie J. Comrie, Jeffrey C. P. Miller, Donald H. Sadler, and Alexander J.
     Thompson, Bessel functions, part II, Functions of positive integer order, Cambridge University
     Press, 1952.

[10] Richard P. Brent, Fast multiple-precision evaluation of elementary functions, Journal of the
     Association for Computing Machinery 23 (1976), no. 2, 242–251.

[11] Andrew M. Childs, Quantum information processing in continuous time, Ph.D. thesis, Mas-
     sachusetts Institute of Technology, 2004.

[12]          , On the relationship between continuous- and discrete-time quantum walk, Communi-
       cations in Mathematical Physics 294 (2010), no. 2, 581–603, arXiv:0810.0312.

[13] Andrew M. Childs, Richard Cleve, Enrico Deotto, Edward Farhi, Sam Gutmann, and Daniel A.
     Spielman, Exponential algorithmic speedup by quantum walk, Proceedings of the 35th ACM
     Symposium on Theory of Computing, pp. 59–68, June 2003, arXiv:quant-ph/0209131.

[14] Andrew M. Childs, Richard Cleve, Stephen P. Jordan, and David Yonge-Mallo, Discrete-
     query quantum algorithm for NAND trees, Theory of Computing 5 (2009), no. 5, 119–123,
     arXiv:quant-ph/0702160.

                                                16
[15] Andrew M. Childs and Robin Kothari, Limitations on the simulation of non-sparse Hamilto-
     nians, Quantum Information and Computation 10 (2010), no. 7–8, 669–684, arXiv:0908.4398.

[16] Andrew M. Childs and Nathan Wiebe, Hamiltonian simulation using linear combinations of
     unitary operations, Quantum Information and Computation 12 (2012), no. 11–12, 901–924,
     arXiv:1202.5822.

[17] Edward Farhi, Jeffrey Goldstone, and Sam Gutmann, A quantum algorithm for the Hamilto-
     nian NAND tree, Theory of Computing 4 (2008), no. 8, 169–190, arXiv:quant-ph/0702144.

[18] Edward Farhi, Jeffrey Goldstone, Sam Gutmann, and Michael Sipser, Limit on the speed of
     quantum computation in determining parity, Physical Review Letters 81 (1998), no. 24, 5442–
     5444, arXiv:quant-ph/9802045.

[19] Richard P. Feynman, Simulating physics with computers, International Journal of Theoretical
     Physics 21 (1982), no. 6–7, 467–488.

[20]       , Quantum mechanical computers, Optics News 11 (1985), no. 2, 11–20.

[21] Aram W. Harrow, Avinatan Hassidim, and Seth Lloyd, Quantum algorithm for linear systems
     of equations, Physical Review Letters 103 (2009), no. 15, 150502, arXiv:0811.3171.

[22] Robin Kothari, Efficient algorithms in quantum query complexity, Ph.D. thesis, University of
     Waterloo, 2014.

[23] Troy Lee, Rajat Mittal, Ben W. Reichardt, Robert Špalek, and Mario Szegedy, Quantum query
     complexity of state conversion, Proceedings of the 52nd IEEE Symposium on Foundations of
     Computer Science, pp. 344–353, October 2011, arXiv:1011.3020.

[24] Seth Lloyd, Universal quantum simulators, Science 273 (1996), no. 5278, 1073–1078.

[25] National Energy Research Scientific Computing Center, NERSC Annual Report 2013,
     https://www.nersc.gov/news-publications/publications-reports/nersc-annual-reports/.

[26] Oak Ridge Leadership Computing Facility, OLCF                 Annual   Report    2012–2013,
     https://www.olcf.ornl.gov/media-center/center-reports/.

[27] Frank W. J. Olver, Error analysis of Miller’s recurrence algorithm, Mathematics of Computa-
     tion 18 (1964), 65–74.

[28] David Poulin, Angie Qarry, Rolando D. Somma, and Frank Verstraete, Quantum simulation
     of time-dependent Hamiltonians and the convenient illusion of Hilbert space, Physical Review
     Letters 106 (2011), no. 17, 170501, arXiv:1102.1360.

[29] Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms
     on a quantum computer, SIAM Journal on Computing 26 (1997), no. 5, 1484–1509,
     arXiv:quant-ph/9508027.

[30] Nathan Wiebe, Dominic W. Berry, Peter Høyer, and Barry C. Sanders, Simulating quan-
     tum dynamics on a quantum computer, Journal of Physics A 44 (2011), no. 44, 445308,
     arXiv:1011.3489.




                                               17
A      Proofs of technical lemmas
We now present proofs of some of the more technical results.

Proof of Lemma 7. Consider two operators U and V acting on a pure state |ψi. For the following
analysis we define

                                    φ := arg hψ|V † U |ψi,                                                (61)
                                           q
                                   NU := 1/ hψ|U † U |ψi,                                                 (62)
                                           q
                                   NV := 1/ hψ|V † V |ψi,                                                 (63)
                                         q
                                   N± := 2 ± 2NU NV |hψ|V † U |ψi|.                                       (64)

Then we define a basis
                                                  NU U |ψi ± eiφ NV V |ψi
                                       |χ± i :=                           .                               (65)
                                                           N±
In terms of this basis, we have
                                            1
                                   U |ψi =      (N+ |χ+ i + N− |χ− i),                                    (66)
                                           2NU
                                           e−iφ
                                   V |ψi =      (N+ |χ+ i − N− |χ− i),                                    (67)
                                           2NV
so
                                               N+2                  N+2
                                                                              
                                          1         N+ N−      1          −N+ N−
         U |ψihψ|U † − V |ψihψ|V † =                        −                      .                      (68)
                                         4NU2 N+ N−  N−2      4NV2 −N+ N−  N−2

     The eigenvalues of this matrix are
                                                                                    
            1
                                         q
                    †            †             †            †      2        †      2
      λ± =      hψ|U U |ψi − hψ|V V |ψi ± (hψ|U U |ψi + hψ|V V |ψi) − 4|hψ|V U |ψi| .                     (69)
            2

The square root in this expression must be at least as large as |hψ|U † U |ψi − hψ|V † V |ψi|, so λ− ≤ 0
and λ+ ≥ 0. Thus the trace norm (i.e., the Schatten 1-norm, denoted k·k1 ) is

           kU |ψihψ|U † − V |ψihψ|V † k1 = |λ+ | + |λ− |
                                           q
                                         = (hψ|U † U |ψi + hψ|V † V |ψi)2 − 4|hψ|V † U |ψi|2 .            (70)

Next, from the definition of the spectral norm,

                   kU − V k2 ≥ hψ|(U − V )† (U − V )|ψi
                              = hψ|U † U |ψi + hψ|V † V |ψi − hψ|V † U |ψi − hψ|U † V |ψi
                              ≥ hψ|U † U |ψi + hψ|V † V |ψi − 2|hψ|V † U |ψi|.                            (71)

Using this inequality with the expression for the trace norm gives

      kU |ψihψ|U † − V |ψihψ|V † k21
       = (hψ|U † U |ψi + hψ|V † V |ψi − 2|hψ|V † U |ψi|)(hψ|U † U |ψi + hψ|V † V |ψi + 2|hψ|V † U |ψi|)
       ≤ kU − V k2 (hψ|U † U |ψi + hψ|V † V |ψi + 2|hψ|V † U |ψi|).                                       (72)


                                                        18
Provided kU k ≤ 1 and kV k ≤ 1, this yields

                               kU |ψihψ|U † − V |ψihψ|V † k21 ≤ 4kU − V k2 ,                       (73)

so

                            kU |ψihψ|U † − V |ψihψ|V † k1 ≤ 2kU − V k.                             (74)
                            P
     Given a mixed state ρ = j pj |ψj ihψj |, strong convexity implies that
                                               X
                       kU ρU † − V ρV † k1 ≤            pj kU |ψj ihψj |U † − V |ψj ihψj |V † k1
                                                j
                                                 X
                                           ≤2            pj kU − V k
                                                    j

                                           = 2kU − V k.                                            (75)

Similarly, tensoring with the identity gives

                      k(U ⊗ I)ρ(U † ⊗ I) − (V ⊗ I)ρ(V † ⊗ I)k1 ≤ 2kU ⊗ I − V ⊗ Ik
                                                                         = 2kU − V k.              (76)

Hence, maximizing over ρ, the diamond norm satisfies

                                          kU − V k⋄ ≤ 2kU − V k.                                   (77)

    Now consider the case where U is some desired unitary, and V = V0 is an operation that happens
if a measurement succeeds, with other operations Vj occurring for other measurement outcomes.
That is, the overall channel is
                                                        Vj ρVj†
                                                    X
                                    C(ρ) = V ρV † +                                           (78)
                                                                   j
                        †
where V † V +
                P
                    j Vj Vj = I. The trace is bounded by

                              Tr(V ρV † ) = Tr(U ρU † ) − Tr(U ρU † − V ρV † )
                                          ≥ 1 − kU ρU † − V ρV † k1
                                          ≥ 1 − 2kU − V k.                                         (79)

Hence the trace of the remaining part is bounded as
                                           

                                    Vj ρVj†  = Tr(C(ρ)) − Tr(V ρV † )
                                 X
                            Tr 
                                      j

                                                         ≤ 1 − (1 − 2kU − V k)
                                                         ≤ 2kU − V k.                              (80)

For non-negative Hermitian operators, the trace norm is equal to the trace, so


                                               Vj ρVj†
                                          X
                                                                ≤ 2kU − V k.                       (81)
                                          j
                                                            1


                                                           19
Since the trace is unchanged by tensoring with the identity, we have

                                       X
                                        (Vj ⊗ I)ρ(Vj ⊗ I)†           ≤ 2kU − V k.                                       (82)
                                        j
                                                                 1

Hence

                                                      X
     kC − U k⋄ = max (V ⊗ I)ρ(V ⊗ I)† +                    (Vj ⊗ I)ρ(Vj ⊗ I)† − (U ⊗ I)ρ(U ⊗ I)†
                        ρ
                                                       j
                                                                                                         1
                                                                                                                   
                                                                                       X
                   ≤ max k(V ⊗ I)ρ(V ⊗ I)† − (U ⊗ I)ρ(U ⊗ I)† k1 +                        (Vj ⊗ I)ρ(Vj ⊗ I)†       
                        ρ
                                                                                       j
                                                                                                                1
                   ≤ 4kU − V k                                                                                          (83)

as claimed.

Proof of Lemma 8. For |m| ≤ k, the values of am differ from Jm (z) only due to the normalization
factor in (42). The Bessel function Jm (z) is bounded, for real z and integer m, by [1, 9.1.62]

                                                              1 z |m|
                                              |Jm (z)| ≤                                                                (84)
                                                             |m|! 2

(here we use the fact that J−m (z) = (−1)m Jm (z) [1, 9.1.5]). Using this bound, together with the
condition that |z| ≤ k,
               ∞                   ∞                    ∞
               X                   X |z/2|m    |z/2|k+1 X                  |z/2|k+1
          2           |Jm (z)| ≤ 2          <2            (1/2)m−(k+1) = 4          .                                   (85)
                                       m!      (k + 1)!                    (k + 1)!
              m=k+1                  m=k+1                            m=k+1

As a result, the normalization factor in (42) satisfies
                                             k
                                             X                       |z/2|k+1
                                                   Jm (z) ≥ 1 − 4             .                                         (86)
                                                                     (k + 1)!
                                            m=−k

This means that am closely approximates Jm (z), in the sense that

                                                    (z/2)k+1
                                                            
                              am = Jm (z) 1 + O                  .                                                      (87)
                                                     (k + 1)!

   Similarly, using |µm
                      ± − 1| ≤ |νm| and |z| ≤ k gives

                            ∞                                   ∞
                            X                                   X         |z/2|m
                       2           Jm (z)(µm
                                           ± − 1) ≤ 2|ν|              m
                                                                            m!
                           m=k+1                             m=k+1
                                                                     ∞
                                                            |z/2|k+1 X
                                                     < 2|ν|            m(1/2)m−(k+1)
                                                            (k + 1)!
                                                                         m=k+1
                                                                       |z/2|k+1
                                                     = 4|ν|(k + 2)                 .                                    (88)
                                                                       (k + 1)!


                                                           20
Using (41) gives
                                                      ∞
                                                      X
                                    e   iνz
                                              −1=           Jm (z)(µm
                                                                    ± − 1).                       (89)
                                                     m=−∞
Therefore, with (88), we obtain
                          k
                                                                              (z/2)k+1
                          X                                                             
                                Jm (z)(µm
                                        ± − 1) = e
                                                  iνz
                                                      −1+O                  ν                 .   (90)
                                                                                 k!
                         m=−k

Using this expression together with (87) then gives
               k
                                                   (z/2)k+1            (z/2)k+1
              X                                                            
                        m           iνz
                   am (µ± − 1) = e − 1 + O ν                     1+O                .             (91)
                                                      k!                (k + 1)!
                m=−k

Using |eiνz − 1| ≤ |νz| and |z| ≤ k gives
                            k
                                                                           (z/2)k+1
                            X                                                        
                                  am (µm
                                       ± − 1) = e
                                                 iνz
                                                     −1+O                ν                .       (92)
                                                                              k!
                           m=−k
          P
Because       m am = 1, we obtain
                                  k
                                                                (z/2)k+1
                                  X                                     
                                          am µ m
                                               ± − eiνz
                                                        = O   ν            .                      (93)
                                                                   k!
                                m=−k
     Pk
Now m=−k am µm   ± are the eigenvalues of Vk , and e
                                                    iνz are the eigenvalues of the desired unitary

operation V∞ . Using ν = λ/Xd, we have |ν| ≤ kHk/Xd. Hence the norm of the difference of these
operators is bounded as in (43).
Proof of Lemma 11. First we bound the sum over small values of m. The Bessel functions satisfy
[1, 9.1.76]
                                      X∞
                                          [Jm (z)]2 = 1.                                 (94)
                                                m=−∞
For any positive integer k we have
                                                k
                                                X
                                                       |Jm (z)|2 < 1.                             (95)
                                                m=−k
Using the Cauchy-Schwarz inequality, we find
                                     v        v
                      k              u k
                                     u X u k                 √
                                              u
                     X                          X
                          |Jm (z)| ≤ t       1t   |Jm (z)|2 < 2k + 1.                             (96)
                        m=−k                    m=−k        m=−k

   Provided |z| ≤ k, using (85), together with ℓ! > (ℓ/e)ℓ , we obtain
                                         ∞                               k+1
                                         X                         ez
                                    2           |Jm (z)| < 4                 .                    (97)
                                                                2(k + 1)
                                        m=k+1

Combining (96) and (97), we find
                                               √                         k+1
                                                                   ez
                                    S(z) <         2k + 1 + 4                .                    (98)
                                                                2(k + 1)
                                                                          p
Finally, taking k = ⌈ez/2⌉, the second term is O(1), which gives S(z) = O( |z|) as claimed.


                                                         21

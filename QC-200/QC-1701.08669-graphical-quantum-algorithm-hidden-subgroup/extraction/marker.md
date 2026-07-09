# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3:
# Paper: arXiv:1701.08669 — Stefano Gogioso and Aleks Kissinger, 'Fully Graphical Treatment of the Quantum Algorithm for the Hidden Subgroup Problem'
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM
FOR THE HIDDEN SUBGROUP PROBLEM
STEFANO GOGIOSO AND ALEKS KISSINGER
Quantum Group, University of Oxford, UK
iCIS, Radboud University. Nijmegen, Netherlands
Abstract. The abelian Hidden Subgroup Problem (HSP) is extremely general, and many
problems with known quantum exponential speed-up (such as integers factorisation, the
discrete logarithm and Simon’s problem) can be seen as speciﬁc instances of it. The
traditional presentation of the quantum protocol for the abelian HSP is low-level, and relies
heavily on the the interplay between classical group theory and complex vector spaces.
Instead, we give a high-level diagrammatic presentation which showcases the quantum
structures truly at play. Speciﬁcally, we provide the ﬁrst fully diagrammatic proof of
correctness for the abelian HSP protocol, showing that strongly complementary observables
are the key ingredient to its success. Being fully diagrammatic, our proof extends beyond
the traditional case of ﬁnite-dimensional quantum theory: for example, we can use it to
show that Simon’s problem can be eﬃciently solved in real quantum theory, and to obtain
a protocol that solves the HSP for certain inﬁnite abelian groups.
1. Introduction
The advent of quantum computing promises to solve a number number of problems which
have until now proven intractable for classical computers. Amongst these, one of the most
famous is Shor’s algorithm [Sho95,EJ96]: it allows for an eﬃcient solution of the integer
factorisation problem and the discrete logarithm problem, the hardness of which underlies
many of the cryptographic algorithms which we currently entrust with our digital security
(such as RSA and DHKE). Integer factorisation and the discrete logarithm, together with
Simon’s problem [Sim97], Deutsch original algorithm and a number of other number-theoretic
questions, turn out to be special cases of the much more general abelian Hidden Subgroup
Problem (HSP) [Joz01], and can be tackled by quantum computers using a uniform strategy.
The reformulation of Shor’s algorithm as a special case of the abelian HSP [Joz01]
makes the core issue of order-ﬁnding pop out as a group-theoretic question, and highlights
the role played by the quantum Fourier transform in solving it [Joz97]. However, it is only
with the compelling diagrammatic work of [Vic12] that the structures and information ﬂow
behind the quantum solution to the HSP become fully apparent: the unitary oracle used in
Key words and phrases: Hidden subgroup problem, quantum computation, categorical quantum mechanics,
quantum Fourier transform, strongly complementary observables.
LOGICAL METHODS
IN COMPUTER SCIENCE
DOI:10.2168/LMCS-???
c
⃝
S. Gogioso and A. Kissinger
Creative Commons
1
arXiv:1701.08669v1  [quant-ph]  30 Jan 2017


---- page 2 ----
2
S. GOGIOSO AND A. KISSINGER
the algorithm is decomposed into its algebraic building blocks, namely certain †-Frobenius
algebras, providing a clear topological account of why the procedure works.
Strong complementarity [CD11], a diagrammatic property of †-Frobenius algebras
related to the quantum Fourier transform, seems to play a fundamental role in the procedure.
However, the diagrammatics in the proof of [Vic12] are nothing but straightforward graphical
transcriptions of results obtained via traditional representation theory: this approach makes
it hard to tell whether strong complementarity is truly fundamental at the topological level
of information ﬂow, or whether its presence is merely accidental. In this work, we provide
the ﬁrst fully diagrammatic proof of correctness for the quantum algorithm solving the
abelian HSP, showing beyond any shadow of doubt that the feature providing the quantum
advantage is indeed strong complementarity. Furthermore, our fully diagrammatic approach
means that our results can be immediately generalised from traditional quantum mechanics
to other theories featuring the necessary algebraic structures.
Both the original [Vic12] and this work use the graphical language of string diagrams
and dagger symmetric monoidal categories [JS91,JSV96,Sel09,Coe09,Kis12,CK16], where
processes between quantum systems are represented by means of boxes and decorations (the
processes) connected by wires (the input/output systems of sequentially composed processes)
and/or stacked side by side (for parallel composition). This work adopts a left-to-right
convention for sequential composition: this is in line with several other formalisms used in
quantum information and computation, but is diﬀerent from the bottom-to-top convention
of [Vic12] and other works in string diagrams.
2. The Hidden Subgroup Problem
The Hidden Subgroup Problem (HSP) can be phrased as follows:
(i) a ﬁnite group G is ﬁxed;
(ii) we are given an oracle implementing a subgroup hiding function f : G →ZN
2 ,
which associates to each element of G a label in the form of an N-bit string;
(iii) we are promised that the function is constant on (left) cosets of some subgroup
H ≤G, and associates diﬀerent labels to diﬀerent cosets; equivalently, we are
promised that f factorizes as follows for some injective function s and the quotient
group homomorphism q (we refer to this as the factorisation promise):
G
G/H
ZN
2
f
q
s
(2.1)
(iv) we are asked to ﬁnd the hidden subgroup H.
In the abelian HSP we are also promised that G is abelian, while in the more general
normal HSP we are promised that H is a normal subgroup (a fact which always holds
in the abelian HSP). In order for a quantum treatment to be possible at all, one imposes
additional requirement on the oracle encoding the subgroup hiding function:
(e) the oracle is given coherently, as the following unitary Uf ∈U

C[G] ⊗C[ZN
2 ]

:
Uf := |g⟩⊗|t⟩7→|g⟩⊗|f(g) ⊕t⟩
(2.2)
where by ⊕we denoted the bit-wise XOR operation on N-bit strings.


---- page 3 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
3
A number of important problems arise as special instances of the abelian HSP. In the Discrete
Logarithm problem, one is given a prime number p, a primitive root g mod p, and a number
a such that a = gb (mod p) for some unknown b to be found. This is an instance of the
abelian HSP with group G = Zp−1 × Zp−1, hidden subgroup H = Zp−1 · (b, 1) ⊴G and
subgroup hiding function f(x, y) := gxa−y (mod p) = gx−by (mod p).
In the Integer Factorisation problem, one is given a composite number N and is asked
to provide a non-trivial factorisation for it. Shor’s algorithm solves the problem eﬃciently
on quantum computers: its core is the order-ﬁnding subroutine, which considers an integer
a coprime1 with N, and asks for the order of a as a multiplicative unit modulo N. The
order-ﬁnding subroutine is an instance of the abelian HSP with group G = Z×
N (the abelian
group of multiplicative units modulo N)2, hidden subgroup H = ⟨a⟩∼= Zord(a) and subgroup
hiding function f(x) = ax (mod N).
In Simon’s problem, one is given a function f : ZN
2 →ZN
2 with the promise that the
stabilizer subgroup for f has order 2: there is a unique non-zero string z ∈ZN
2 , which we
are asked to ﬁnd, such that for any two N-bit strings x, y ∈ZN
2 we have that f(x) = f(y) if
and only if x = y or x = y ⊕z. The importance of Simon’s problem in the complexity of
quantum computing lies in a result [BV97] stating that, relative to oracles with the promise
above, Simon’s problem separates BQP (the class of bounded-error quantum polynomial
time problems) from BPP (the class of bounded-error classical polynomial time problems).
Simon’s problem is clearly an instance of the abelian HSP, with G = ZN
2 , hidden subgroup
H = ⟨z⟩= {0, z} and subgroup hiding function f.
Quantum algorithms to solve the HSP have been studied beyond the abelian case. An
extension of the eﬃcient quantum solution to the case of normal subgroups of non-abelian
groups is given by [HRTS00], while [MRS08,HRS10] provide a no-go theorem showing that
the same techniques cannot be used to formulate an eﬃcient quantum solution to the general
non-abelian case. The general non-abelian case is important because two interesting problems
of classical computational complexity arise as special cases: the Graph Isomorphism Problem
arises as a special case of the HSP on symmetric groups [HRTS00], while the Unique Shortest
Vector Problem (uSVP) arises as a special case of the HSP on dihedral groups [Reg04b].
The latter forms the basis of a public key cryptosystem [Reg04a] which, subject to quantum
intractability of the HSP on dihedral groups, is a candidate to replace RSA in post-quantum
cryptography (as are many other lattice-based cryptographic algorithms).
3. Coherent Data Manipulation
At the basis of the diagrammatic treatment of the HSP is the observation that the unitary
oracle of Equation 2.2 has certain Frobenius algebras as its constituent parts [Vic12].
Frobenius algebras, or more precisely †-Frobenius algebras, are a fundamental structure
in the categorical and diagrammatic treatment of quantum information and computation:
they provide the coherent versions of several classical data manipulation primitives, such as
copy, deletion, matching and group operations (e.g. bit-wise XOR, modular addition, etc),
they obey simple graphical rules, and they can be composed together to form more complex
quantum processes taking place during quantum computation. Our main contribution will
1If a ∈{2, ..., N −1} is not coprime with N, then we already have a non-trivial factorisation of N.
2In practice one uses Z2M : if M ≫log2 N, the errors due to the inexact period of a will be small.


---- page 4 ----
4
S. GOGIOSO AND A. KISSINGER
be to show that those abstract graphical rules are in fact suﬃcient to prove correctness of
the quantum subroutine for the HSP.
We begin our journey by observing that there are four distinct group structures playing
a role in the deﬁnition of the Hidden Subgroup Problem, and/or intervening in some capacity
in the formulation of the quantum algorithm aiming to solve it:
(a) the main group G;
(b) the hidden subgroup H;
(c) the quotient group G/H appearing in the factorisation promise;
(d) the group ZN
2 of N-bit strings under the bit-wise XOR operation.
Two distinct algebraic structures intervene when we wish to encode a ﬁnite group K (such
as K = G, H, G/H, ZN
2 above) into a quantum system H:
(a) a copy/delete coalgebra (
K,
K) on H, deﬁning a coherent encoding of the
elements (or points) of the group as an orthonormal basis of the quantum system;
(b) a group algebra (
K,
K) on H, deﬁning the group multiplication and unit
on the coherently encoded points.
Both structures will turn out to deﬁne certain †-Frobenius algebras, corresponding in turn
to various quantum observables intervening in algorithm itself.
3.1. The copy/delete coalgebra. The copy/delete coalgebra (
K,
K) deﬁnes the
coherent copy and delete operations on the encoded points:
coherent copy
coherent delete
|k⟩⊗|k⟩
7→
|k⟩
=
=
|k⟩
7→
1
K
K
(3.1)
The adjoints of the linear maps in 3.1 form an algebra (
K,
K) on H, deﬁning the
coherent match operation and the superposition of the encoded classical data:
coherent match
coherent superposition
=
|k⟩⊗|h⟩
7→δk,h|k⟩
P
k∈K
|k⟩
=
K
K
(3.2)
The algebra and coalgebra are not unrelated, but instead interact via the following Frobenius
law, which can be interpreted as encoding a basic topological property of the ﬂow of classical
information:
=
=
Frobenius Law
K
K
K
K
K
K
(3.3)
As a consequence, the four coherent operations deﬁned above form a †-Frobenius algebra,
which we will refer to as the point structure and denote by
K for short. In fact, they
satisfy the additional requirements of commutativity and speciality below, and hence form a
special commutative †-Frobenius algebra (†-SCFA for short):
=
Speciality
Commutativity
=
K
K
K
K
(3.4)


---- page 5 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
5
A key result of categorical quantum mechanics [CPV13] states that there is an exact
correspondence between †-SCFAs on a ﬁnite-dimensional quantum system H and orthonormal
bases (i.e. non-degenerate quantum observables) of H: all †-SCFAs take the form of a coherent
copy/delete coalgebra and a match/superimpose algebra for some orthonormal basis. When
we said that the copy/delete coalgebra deﬁnes the coherent encoding of points, we meant
this: the coalgebra deﬁnes its adjoint, and together they form a †-SCFA, which in turns
identiﬁes a unique orthonormal basis.
If
A and
B are two †-SCFAs, encoding classical input and output data respectively,
the following diagrammatic equations [CPP10] provide an exact characterisation of those
complex linear maps arising as coherent versions (i.e. linear extensions) of classical maps3:
F
F
F
F
=
=
F
F †
=
(adjoin)
(delete)
(copy)
B
A
B
B
B
A
A
A
(3.5)
If F satisﬁes the three equations above, we will say that F is
A-to- B classical. As a
special case, we say that a state |ψ⟩: C →H is
-classical if it is coherently copied, deleted
and transposed by the †-SCFA
in the following sense:
ψ
ψ
ψ
ψ
=
=
ψ
ψ†
=
(copy)
(delete)
(transpose)
(3.6)
In the case of ﬁnite-dimensional Hilbert spaces, classical states for a †-SCFA
are exactly
the states in the associated orthonormal basis.
The graphical deﬁnitions of classical states (Equations 3.6) and classical maps (Equations
3.5) make sense for arbitrary †-Frobenius algebras in arbitrary dagger symmetric monoidal
categories, and we extend them accordingly. Even though the exact correspondence with
encoded classical data is lost, the classical states K( ) for a †-Frobenius algebra
can still
be copied and deleted as if they were classical information, and the
A-to- B classical maps
always restrict to functions K( A) →K( B) on the sets of classical states. We can also
recover the notion of basis in this more general setting, by saying that a †-Frobenius algebra
has enough classical states if any two parallel maps coincide whenever they agree on
all
-classical states.
3If the †-SCFA
A is associated with an orthonormal basis
 |a⟩

a∈A of some space H and the †-SCFA
B
is associated with an orthonormal basis
 |b⟩

b∈B of some space K, then a linear map F : H →K satisfy the
two equations above if and only if we have F|a⟩= |f(a)⟩for some classical map f : X →Y .


---- page 6 ----
6
S. GOGIOSO AND A. KISSINGER
3.2. The group algebra. The group algebra (
K,
K) deﬁnes the coherent group
multiplication on the encoded points, and labels one of them as the group unit4:
=
=
|1K⟩
|g⟩⊗|h⟩
|gh⟩
7→
K
K
coherent group multipication
group unit
(3.7)
The explicit presentation given above is easy to understand in the traditional Hilbert space
formalism, but unsatisfactory from our more abstract point of view. We would like to replace
it with a series of diagrammatic laws, capturing the same structure while highlighting the
interactions between the group algebra and the point structure. As we shall shortly see, the
notion of strong complementarity is exactly what we are looking for.
Just like we did with the copy/delete coalgebra, we can take the adjoints of the maps in
the group algebra to obtain a coalgebra (
K,
K):
7→
δk,1K
7→
=
|k⟩
|k⟩
P
gh=k
|g⟩⊗|h⟩
K
=
K
(3.8)
Somewhat surprisingly, the four maps (
K,
K,
K,
K) also deﬁne a †-Frobenius
algebra, which we shall refer to as the group structure and denote by
K.
Contrary to the point structure, the group structure does not in general satisfy the
speciality law, and it is commutative if and only if the group K is. However, it is always
quasi-special and balanced-symmetric, i.e. it satisﬁes the following laws, where ξ is some
invertible scalar (we refer to it as the normalisation scalar):
=
Quasi-speciality
Balanced-symmetry
=
K
K
K
K
K
K
ξ†ξ
(3.9)
In the Hilbert space case explicitly deﬁned by 3.7, the scalar occurring in the quasi-speciality
law is ξ :=
p
|K|. The result of [CPV13] on orthonormal bases straightforwardly extends
to quasi-special commutative †-Frobenius algebras (†-qSCFA for short), which correspond
exactly to orthogonal bases where all elements have the same square norm (equal to ξ†ξ).
Also, by the deﬁnition of the quasi-special law we have that every quasi-special †-Frobenius
algebra can be normalised to obtain a unique corresponding special †-Frobenius algebra,
and hence quasi-speciality is merely a diagrammatic convenience. An extension of the
result of [CPV13] to arbitrary balanced-symmetric special5 †-Frobenius algebra (balanced-
symmetric †-SFAs, for short) is obtained straightforwardly from [Vic11], and it states that
balanced-symmetric †-Frobenius algebras on ﬁnite-dimensional quantum system are in exact
correspondence with complete families of orthogonal projectors (i.e. quantum observables).
4We use multiplicative notation for the groups operations, to accommodate the general case where the
group in consideration might not be abelian. As a special exception, we will use additive notation (ZN
2 , ⊕, 0)
for the bit-wise XOR group operation on N-bit strings, with the zero string as its unit.
5And hence also to balanced-symmetric quasi-special †-Frobenius algebras.


---- page 7 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
7
3.3. Strong complementarity. With these observations at hand, we are now ready to
deﬁne the diagrammatic property of strong complementarity, and to show that it captures
exactly the abstract relationship between the point and group structures deﬁned explicitly
above. We will state it in arbitrary dagger symmetric monoidal categories (†-SMC for short).
Deﬁnition 3.1. Two balanced-symmetric †-qSFAs
and
on the same object H are said
to be complementary (or a complementary pair) if they satisfy the Hopf Law:
=
=
(3.10)
where the antipode
: H →H satisﬁes the following equation:
:=
=
(3.11)
Note that the antipode is unitary (by deﬁnition) and self-adjoint (by Equation 3.11).
Remark 3.2. Because of balanced-symmetry and the self-adjointness requirement, the
antipode can be equivalently written in two additional ways:
=
=
(3.12)
Deﬁnition 3.3. Two balanced-symmetric †-qSFAs
and
on the same object of a †-SMC
are said to be strongly complementary (or a strongly complementary pair) if they
are complementary and furthermore satisfy the following four equations:
=
=
=
=
(3.13)
The empty diagram on the right hand side of the top-right equation corresponds to the
scalar 1, i.e. the identity morphism 1I on the monoidal unit I.
Theorem 3.4. Let ( , ) be a pair of balanced-symmetric †-qSFAs. If ( , ) is a strongly
complementary pair then the algebraic fragment of
endows the
-classical states with the
structure of a group (K( ),
,
), which has the antipode
as group inverse and is
abelian if and only if
is commutative. A converse holds when
has enough classical states
and
is a
-classical state6: in that case, if (K( ),
,
) is a group then ( , ) is a
strongly complementary pair.
Proof. A ﬁrst version of this result was proven in [CD11,Kis12] for the ﬁnite abelian group
case of †-SCFAs on ﬁnite-dimensional Hilbert spaces (which always have enough points).
Here we present a simpler proof of much broader scope, valid for all balanced-symmetric
†-qSFAs in arbitrary †-SMCs.
6In fact it is suﬃcient for
to satisfy the
transpose condition. The reasons behind this somewhat
bizarre requirement are explained after the proof.


---- page 8 ----
8
S. GOGIOSO AND A. KISSINGER
To begin with, assume that ( , ) is a strongly complementary pair. The deﬁning Equations
3.13 of strong complementarity state that the unit
and multiplication
satisfy the
copy and delete conditions for
-classical states and ( ⊗)-to-
classical maps. In order to
prove that they are indeed classical (so that (K( ),
,
) is a monoid) we need to show
the transpose condition for both:
=
=
(3.14)
Both equations can be shown to follow from Hopf’s law, the self-adjointness requirement for
the antipode, and the four deﬁning equations of strong complementarity:
=
=
=
=
=
=
(3.15)
=
=
=
=
=
(3.16)
Finally, applying Hopf’s law to any
-classical state (which is copied by
and deleted
by
) shows that the antipode
acts as an inverse for elements of the the monoid
(K( ),
,
), which is therefore a group. As a side note, a proof on the same lines of that
in 3.15, but with colours swapped, shows that
satisﬁes the transpose condition with
respect to
, and hence is always a
-classical state.
Conversely, assume that
has enough classical states, and that (K( ),
,
) is a
group. In particular,
is a
-classical state and
is ( ⊗)-to- -classical map: because
has enough classical states, the four deﬁning Equations 3.13 of strong complementarity and
the two Equations 3.14 all hold. All that remains to show is that ( , ) are complementary.
The proof of Hopf’s law goes as follows, and requires one to use the fact that
is transposed
by
:
=
=
=
=
=
(3.17)
The proof for the other equation is similar (using balanced-symmetry at one point). Finally,
Hopf’s law proves that the antipode acts as the group inverse on the
-classical states:
because
has enough classical states, the antipode must be self-inverse, or equivalently
self-adjoint, completing the proof of complementarity.
The requirement in Theorem 3.4 that
be
-classical7 seems to come somewhat
out of the blue, but is instead an inkling of a deeper result. Theorem 3.4 was stated
asymmetrically and with a minimal set of requirements and conclusions, which are relevant
when
and
are the point and group structures for some group K. However, the deﬁnitions
of complementarity and strong complementarity are fully symmetric in the two †-Frobenius
algebras involved, and Theorem 3.4 can be re-formulated in a fully symmetric way.
7Or at least transposed by
, since the copy and delete conditions for
to be
-classical can already be
obtained as the adjoints of the delete conditions for
and
.


---- page 9 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
9
Corollary 3.5. Let ( , ) be a pair of balanced-symmetric †-qSFAs. If ( , ) is a strongly
complementary pair then both (K( ),
,
) and (K( ),
,
) are groups, both with the
antipode as group inverse. A converse holds when at least one of ( , ) has enough classical
states: in that case, if (K( ),
,
) and (K( ),
,
) are both groups then ( , ) is a
strongly complementary pair.
Having just seen the correspondence between groups and strongly complementary pairs,
it is natural to ask how group homomorphisms could be characterised diagrammatically.
Deﬁnition 3.6. If ( H,
H) and ( K,
K) are strongly complementary pairs on two ob-
jects H and K respectively, we say that a process F : H →K is a ( H,
H)-to-( K,
K)
homomorphism if it is
H-to- K classical and furthermore satisﬁes the following8:
=
F
F
F
F
=
(multiplication)
(unit)
F
=
F
(inverse)
H
K
H
K
K
H
(3.18)
Lemma 3.7. Let ( H,
H) and ( K,
K) be two strongly complementary pairs on two objects
H and K respectively.
If F : H →K is a ( H,
H)-to-( K,
K) homomorphism, then
restricting F to the
H-classical states gives rise to a well-deﬁned group homomorphism
(K( H),
H,
H) →(K( K),
K,
K). A converse to this statement holds if
H has
enough classical states: in that case, any F : H →K which gives rise to a well-deﬁned
group homomorphism (K( H),
H,
H) →(K( K),
K,
K) when restricted to the
H-classical states is in fact a ( H,
H)-to-( K,
K) homomorphism.
Proof. If F is a ( H,
H)-to-( K,
K) homomorphism, then in particular it restricts to a
function K( H) →K( K); then the two Equations 3.18 state applied to
H-classical states
simply state that the function respects the group multiplication and unit, i.e. that it is a
group homomorphism. Conversely, we have already seen that if F restricts to a function
then it is
H-to- K classical, since
H has enough classical states. Furthermore, Equations
3.18 hold when applied to
H-classical states because F gives rise to a group homomorphism,
and hence hold in full generality because
H has enough classical states. We conclude that
F is a ( H,
H)-to-( K,
K) homomorphism.
Lemma 3.8. Let ( H,
H) and ( K,
K) be two strongly complementary pairs on two objects
H and K respectively. Then a process F : H →K is a ( H,
H)-to-( K,
K) homomorphism
if and only if its adjoint F † : K →H is a ( K,
K)-to-( H,
H) homomorphism9.
Proof. Being a homomorphism is a statement comprised of six conditions: the copy,delete
and transpose conditions from Equations 3.5 and the multiplication, unit and inverse
conditions from Equations 3.18. Taking the dagger of the copy/delete conditions from F
being a ( H,
H)-to-( K,
K) homomorphism are exactly the multiplication/unit conditions
for F † being a ( K,
K)-to-( H,
H) homomorphism; conversely, taking the dagger of the
copy/delete conditions for F † yields the multiplication/unit conditions for F. Also, taking
8Note that the inverse condition follows from the other two when
H has enough classical states.
9Note that not only H and K were swapped, but that colours were swapped as well.


---- page 10 ----
10
S. GOGIOSO AND A. KISSINGER
the dagger of the inverse condition for F yields the inverse condition for F †, as the antipodes
are self-adjoint. Finally, we need to show that the transpose condition for F implies the
transpose condition for F †. To obtain the desired implication, we pre/post compose the
transpose condition for F with the symmetric cup and cap for
H and
K respectively (we
used balanced-symmetry to keep our diagrams tidy):
⇒
F
F †
=
F
=
F †
K
H
H
K
H
H
K
K
(3.19)
We then use the inverse condition for F together with the fact that the antipode is self-inverse
to obtain the transpose condition for F †.
Before proceeding to our main result, we wish to highlight the connection between
strong complementarity, the key ingredient in our proof, and the quantum Fourier transform,
the key ingredient in the traditional proof [Joz97,Joz01].
Lemma 3.9. Let ( , ) be a strongly complementary pair on some object H of some †-SMC.
Then the adjoints of the
-classical states satisfy the following equations:
=
χ
χ
χ
χ
=
χ
=
χ†
(3.20)
We will refer to them as the ( , )-multiplicative characters.
Proof. The ﬁrst two equations are the daggers of the copy and delete conditions for -classical
states. The last equation follows by post-composing the dagger of the transpose condition
with the symmetric cap for
.
Corollary 3.10. Let ( , ) be a strongly complementary pair on a ﬁnite-dimensional quantum
system H, with
a †-SCFA and
a †-qSCFA. Let G := (K( ),
,
) be the ﬁnite abelian
group corresponding to the pair, and G∧be its Pontryagin dual, i.e. the ﬁnite abelian group
of multiplicative characters for G. If the non-degenerate observable corresponding to
is
taken as the computational basis (|g⟩)g∈G, then the non-degenerate observable corresponding
to
is the Fourier basis (|χ⟩)χ∈G∧corresponding to the group G, i.e. the basis given by the
following states:
|χ⟩=
X
g∈G
χ(g)|g⟩
(3.21)
Proof. Applying Equations 3.20 to the
-classical states (|g⟩)g∈G yields maps χ : G →C
for all
-classical states ⟨χ| ∈K( ). These maps satisfy χ(gh) = χ(g)χ(h), χ(1) = 1 and
χ(g−1) = χ(g)†, and hence are multiplicative characters. Conversely, the adjoint of any
state |χ⟩deﬁne as in Equation 3.21 for a multiplicative character χ satisﬁes Equations 3.20
when applied to the
-classical states, and hence satisﬁes them altogether because
has
enough classical states. Hence the
-classical states are in bijection with the multiplicative
characters of G.


---- page 11 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
11
4. The Quantum Algorithm – Traditional Presentation
The quantum subroutine of the algorithm solving the abelian HSP proceeds as follows:
(i) an initial state P
g∈G |g⟩⊗|0⟩of the joint quantum system C[G] ⊗C[ZN
2 ] is prepared;
(ii) the unitary oracle Uf is applied to this initial state;
(iii) the subsystem C[ZN
2 ] is measured in the standard orthonormal basis, resulting in a
classical measurement outcome b ∈ZN
2 ;
(iv) the subsystem C[G] is measured in the orthonormal basis
 1
√
|G|
P
g∈G χ(g)|g⟩

χ∈G∧,
where G∧is the set of multiplicative characters10 of the ﬁnite abelian11 group G.
Now assume that the measurement on C[ZN
2 ] has yielded a string b, associated with a coset
gbH of the hidden subgroup H (i.e. an element of the quotient group G/H). Then we can
compute the probability of an outcome χ ∈G∧(where G∧denotes the abelian group of
multiplicative characters of G): they main observation behind the algorithm is that this
results in a uniform distribution over the annihilator of H, the subgroup Ann[H] ≤G
containing those multiplicative characters such that χ(h) = 1 for all h ∈H (independently
of which b we had obtained). Therefore, the quantum subroutine of the algorithm provides
a way to uniformly sample the annihilator of the hidden subgroup H.
The classical part of the algorithm identiﬁes H by sampling its annihilator a number of
times logarithmic in the size of H. Because G is abelian, the Fundamental Theorem for ﬁnite
abelian groups [FS78] implies that it admits a description in terms of O(log |G|) generators,
i.e. that there are k ∝log |G| generators g1, ..., gk such that every g ∈G can be written
uniquely as gn1
1 ·...·gnk
k , for coeﬃcients nj ∈Zord(gj). In terms of generators, the multiplicative
characters take the following form, for all possible p := (p1, ..., pk) ∈Qk
j=1 Zord(gj):
χp
 gn1
1 · ... · gnk
k

= e
i2π
  p1·n1
ord(g1)+...+ pk·nk
ord(gk)

(4.1)
Each sampled χp ∈Ann[H] then results in the following equation (coming from χp(h) = 1),
which all elements h := gm1
i
· ... · gmk
k
of the hidden subgroup H must satisfy:
p1 · m1
ord(g1) + ... + pk · mk
ord(gk) = 0 (mod 1)
(4.2)
Because H is an abelian subgroup, it also admits a logarithmic description in terms of the
generators, which can be identiﬁed by simultaneously solving O(log |H|) such equations.
5. The Quantum Algorithm – Diagrammatic Presentation
For the fully diagrammatic version of the proof, we replace the concrete Hilbert space setting
with four assumptions about the †-SMC we want to implement the protocol in, and the
strongly complementary pairs that it possesses.
(a) There exist strongly complementary pairs encoding the four relevant ﬁnite abelian
groups: the group G, the hidden subgroup H, the quotient group G/H and the group
of N-bit strings ZN
2 . That is, there exists a strongly complementary pair ( K,
K)
on object HK such that K ∼= (K( K),
K,
K), for each K = G, H, G/H, ZN
2 .
10In fact, multiplicative characters χ : G →S1 form a ﬁnite abelian group with pointwise multiplication.
11The requirement that G be abelian is important here: the linear extensions of multiplicative characters
form a basis of the group algebra C[G] if and only if G is abelian.


---- page 12 ----
12
S. GOGIOSO AND A. KISSINGER
(b) The †-SMC we are working with has an absorbing scalar 0, i.e. we can deﬁne a
sensible notion of impossibility in it.
(c)
H and
G/H have enough classical states.
(d)
G and
ZN
2 have enough classical states, and that their classical states are orthogonal,
so that measurement in either observable can be properly interpreted as a process
with classical output.
As a matter of convenience, we also assume the point structures
K to be special, though
this is not crucial to the proof. We denote by ξK the normalisation scalars of the groups
structures
K (which are quasi-special).
Remark 5.1. When working in the †-SMC fdHilb of ﬁnite-dimensional Hilbert spaces (which
obviously satisﬁes condition (b)), condition (a) is guaranteed by the classiﬁcation theorem for
strongly complementary pairs of †-SCFAs in fdHilb [Kis12] (because the groups we consider
are ﬁnite abelian). Conditions (c) and (d) hold automatically if we pick the
K algebras to
be commutative [CPV13].
5.1. Constructing the oracle. We begin by constructing an abstract version of the unitary
oracle Uf given in Equation 2.2. We replace the subgroup hiding function f : G →ZN
2
(or, to be precise, its linear extension f : C[G] →C[ZN
2 ]) with a
G-to- ZN
2 -classical map
f : HG →HZN
2 , which is required to satisfy an appropriate factorisation promise (detailed
later on). The unitary oracle Uf can then be decomposed as follows, in terms of a coherent
copy operations for G, a coherent multiplication operations for ZN
2 , and the coherent
subgroup hiding function f:
Uf
f
HG
HZN
2
HZN
2
HG
HG
HZN
2
HG
HZN
2
=
G
ZN
2
(5.1)
The process Uf deﬁned above is always unitary, and on ﬁnite-dimensional quantum systems
it coincides with the oracle we explicitly deﬁned in the previous Section [Vic12].
5.2. What we want to show. The following diagram presents the quantum subroutine in
its entirety: the initial state is prepared, the unitary oracle is applied, and two outcomes
b ∈ZN
2 and χ ∈G∧are obtained from the measurements performed on the two parts of the
resulting state:
f
χ
b
G
ZN
2
G
ZN
2
1
ξG
1
ξ†
G
(5.2)
The diagram given above is a scalar cb,χ, and we interpret its square absolute value as the
probability P(b, χ) = c†
b,χcb,χ of obtaining the joint measurement outcome (b, χ). In the
remainder of this Section, we will provide a fully diagrammatic proof that the probability
must be zero if b /∈im s or if χ /∈Ann[H], and it must otherwise be non-zero and independent


---- page 13 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
13
of b and χ. In other words, we wish to show that the procedure produces a uniformly random
sampling of the annihilator of H:
f
χ
b
G
ZN
2
G
ZN
2
1
ξG
1
ξ†
G
2
=
(ξ†
HξH)2
(ξ†
GξG)2
0
if b ∈im s,
otherwise
χ ∈Ann[H] (5.3)
In the case of ﬁnite-dimensional quantum systems, we have ξ†
KξK = |K| for any ﬁnite group
K, and hence the scalar appearing on the RHS is |H|2/|G|2. This is what we expect: there
are |G/H| = |G|/|H| distinct b in the image of s : G/H →ZN
2 (because s is injective), and
the annihilator of H itself has size |G|/|H|, leading to a total of |G|2/|H|2 possible joint
measurement outcomes (b, χ).
5.3. Using the Factorisation Promise. We begin by decomposing f according to the
promise of factorisation through the quotient group G/H. Directly translated, Diagram 2.1
says that the coherent subgroup hiding function f : HG →HZN
2 must factor through two
maps q : HG →HG/H and s : HG/H →HZN
2
q
s
=
f
(5.4)
The map q corresponds to the quotient group homomorphism, and hence must be a ( G,
G)-
to-( G/H,
G/H) homomorphism (satisfying three additional properties detailed later on),
while the map s must correspond to an injection, and hence must be a
G/H-to- ZN
2 -classical
map and an isometry12. As our ﬁrst manipulation step, we can substitute the promised
factorisation of f into s ◦q, and use the unit law to remove the †-qSCFA
ZN
2 from the
diagram:
q
χ
b
G
G
1
ξG
1
ξ†
G
s
G
ZN
2
G
χ
b
f
ZN
2
=
1
ξG
1
ξ†
G
(5.5)
5.4. Eliminating the ZN
2
labels. The property of process s : HG/H →HZN
2 being an
isometry can be readily formulated diagrammatically as follows:
=
F
F †
(5.6)
Because s is a
G/H-to- ZN
2 classical map, and because
G/H has enough classical states
and the classical states of
ZN
2 are orthogonal, then we have the following: a
ZN
2 -classical
state b is either in the image of s, i.e. b = s ◦(gbH) for some classical state gbH, or we have
that b† ◦s = 0 is the impossible process, i.e. b is never observed as outcome. Our second
12When classical data is encoded on orthonormal bases, the coherent versions of injections are isometries.


---- page 14 ----
14
S. GOGIOSO AND A. KISSINGER
manipulation step then assumes that the outcome b ∈ZN
2 is in the image of s, and uses the
isometry property to remove s from the diagram altogether:
q
χ
b
G
G
1
ξG
1
ξ†
G
s
=
χ
1
ξ†
G
G
q
G
gbH
1
ξG
s
b
=
s
gbH
s†
=
gbH
(5.7)
5.5. Formalising the Quotient Map. The manipulation of q in the diagram is more
complicated than that of s, since much of the proof relies on the fact that it is the co-
herent version of a very speciﬁc group homomorphism. Operationally, the quotient group
homomorphism q : G →G/H can be characterised as one satisfying the following three
properties:
(a) q identiﬁes enough elements of G to send all of H to the group unit;
(b) q does not send any elements other than those in H to the group unit;
(c) q is surjective.
These three properties can be captured graphically as follows, where r : HG/H →HG is
some isometry (a section for q, witnessing its surjectivity), and iH : HH →HG is a
H-to- G
classical isometry, corresponding to the group homomorphism injecting H as a subgroup of
G:
=
r
q
=
iH
q
H
G/H
=
q†
G/H
H
iH
(5.8)
As a matter of notational convenience, we will henceforth choose representatives gbH in the
quotient group so that r|gbH⟩:= |gb⟩holds.
5.6. Excluding the Non-Annihilator Outcomes. As our next step, we want to show
that the diagram evaluates to 0 whenever χ is not in the annihilator of H. To do so, we
ﬁrst need a graphical deﬁnition of what it means for a character χ to annihilate H:
=
iH
χ
H
(5.9)
We begin by moving q from the lower to the upper branch, by using the fact that it is
G-to- G/H classical:
=
G
χ
1
ξG
1
ξ†
G
q
gbH
G
1
ξ†
G
1
ξG
G/H
G/H
q†
χ
gbH
(5.10)


---- page 15 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
15
We then proceed to show that either χ† ◦q† = 0, and hence that the entire diagram vanishes,
or that the character χ is in the annihilator of H (according to the graphical deﬁnition of
Equation 5.9):
q†
χ
=
H
G
χ
iH
q†
q†
χ
=
iH
χ
⇒
either
q†
χ
=
0
H
=
iH
χ
enough classical states
(5.11)
The ﬁrst equality is a consequence of the following equivalent reformulation of a deﬁning
property of the quotient map q:
=
iH
q
H
G/H
=
⇔
G
iH
q†
H
q†
(5.12)
The equivalence between the two versions can be proven by using the same general technique
which is used in Equation 5.16 below.
5.7. Introducing the Coset States. Having excluded the case where χ /∈Ann[H] (which
won’t really be needed until the next subsection), our third manipulation step goes as follows:
=
χ
1
ξ†
G
G
G
gb
1
ξG
G
q
gbH
1
ξ†
G
1
ξG
χ
G
H
G
i†
H
(5.13)
We removed both q† and the state gbH of HG/H from the diagram, and replaced them with
an abstract version of the coset state P
h∈H |gb · h⟩of HG, by using the following result:
=
q†
iH
r
G
H
(5.14)
The equality above can be proven diagrammatically using the deﬁning properties of q:
=
iH
r
G
H
q†
G
r
G/H
=
q
G/H
G/H
q†
r
q†
=
(5.15)


---- page 16 ----
16
S. GOGIOSO AND A. KISSINGER
More in detail, the second equation in the chain is proven by using the fact that q is a
( G,
G)-to-( G/H,
G/H) homomorphism, by replacing the antipode with its deﬁnition, and
by appealing to the fact that the antipode is self-inverse:
=
G
q†
G
q
G/H
G
G
G
G
q
q
=
q
G/H
G/H
G/H
q
q†
=
q
G/H
=
(5.16)
5.8. Annihilating the Coset States. We are now in the situation where χ is in the
annihilator of H, and we have rewritten our diagram explicitly in terms of coset states. As
our fourth manipulation step, we turn the character around to obtain (the adjoint of) a
diagram involving a character evaluated on a coset state:
=
χ
1
ξ†
G
G
G
gb
1
ξG
H
G
i†
H
gb
G
H
i†
H
χ†
=
=
i†
H
gb
H
=
χ†
G
H
χ†
i†
H
G
g−1
b
1
ξ†
GξG
1
ξ†
GξG
1
ξ†
GξG
G
G
G
G
(5.17)
Because the character is multiplicative (its adjoint is a
G-classical state), we can copy
it through
G. Evaluating against g−1
b
removes the ﬁrst copy to give some phase χ(g),
satisfying χ(g)†χ(g) = 1, while the deﬁnition of the annihilator removes the second copy
together with i†
H:
χ†
H
=
=
i†
H
g−1
b
H
χ†
1
ξ†
GξG
=
1
ξ†
GξG
H
H
χ(g)
H
χ(g)
1
ξ†
GξG
H
H
1
ξ†
GξG
i†
H
g−1
b
H
G
χ†
G
(5.18)
We are left with a bunch of explicit scalars, and we can ﬁnally evaluate the square absolute
value of Diagram 5.2 to obtain our desired result:
f
χ
b
G
ZN
2
G
ZN
2
1
ξG
1
ξ†
G
2
=
χ(g)
1
ξ†
GξG
H
H
2
=
χ(g)ξ†
HξH
ξ†
GξG

2
(ξ†
HξH)2
(ξ†
GξG)2
=
(5.19)
The evaluation of the square norm
†
H ◦
H to ξ†
HξH comes from the fact that
H is
H-classical, and the latter has ξH as normalisation factor.


---- page 17 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
17
6. Non-abelian HSP
Nowhere in the proof above we have explicitly used commutativity of the †-qSCFAs (equiva-
lently, the fact that G and H are abelian), and our approach naturally generalises to the
case where G is a ﬁnite group and H a normal subgroup (a necessary requirement in this
approach, which explicitly uses a group structure on G/H). For the sake of simplicity, and
because no hard result will be proven, we will stick to the case of ﬁnite-dimensional Hilbert
spaces for the remainder of this Section.
Going from commutative to general quasi-special †-Frobenius algebras (†-qSFA) has the
following implication: the classical states are still the multiplicative characters, and they
are still orthogonal, but they no longer form a basis. Instead, the †-qSFA is now associated
with a potentially degenerate observable: sampling it will produce, as classical output, the
character χρ of an irreducible representation ρ of G, with the following probability (where
dρ is the dimension of representation ρ):
P[b, χρ] =
(|H|2
|G|2 d2
ρ
if ρ(h) = 0 for all h ∈H
0
otherwise
(6.1)
For our graphical proof to go through, Diagram 5.2 needs to be modiﬁed as follows:
f
ρ
b
G
ZN
2
G
ZN
2
1
√
|G|
dρ
√
|G|
(6.2)
where we used the dagger-compact structure to take the trace of the irreducible representation
ρ : C[G] →V ∗
ρ ⊗Vρ (technically, its linear extension from G to C[G]). The deﬁning properties
of multiplicative characters generalise to representations [Vic12]:
=
ρ
ρ
ρ
ρ
=
G
G
G
ρ
=
ρ†
(6.3)
However, the generalisation from the abelian to the non-abelian case encounters a much
bigger hurdle in the classical post-processing: the logarithmic dependency of the number of
generators on the size of the group only need to hold in the abelian case, and the number of
samples required is in general linear in the size of the group (and hence exponential in the
size of its description) [HRS10]. This is a separate problem, interesting in its own right, and
is beyond the scope of this work.
7. Further Applications
The fully diagrammatic, abstract character of our approach means that our results can be
directly applied to theories other than quantum theory, as long as they feature the relevant
algebraic structure. We give three short examples, to corroborate our point: Real Quantum
Theory; more general toy models of quantum theory based on semirings other than C and R;
and treatment of inﬁnite-dimensional HSP using non-standard analysis.


---- page 18 ----
18
S. GOGIOSO AND A. KISSINGER
7.1. Simon’s Problem in Real Quantum Theory. While the quantum subroutine for
the HSP can be formulated with any theory satisfying the few technical requirements we
have imposed, the multiplicative characters appearing in the theory may be very diﬀerent
from the complex-valued ones appearing in the traditional implementation, and this may
give rise to issues in the classical post-processing part of the algorithm (e.g. it might be
hard/impossible to reconstruct the hidden subgroup from the characters sampled by the
routine). As a concrete example, we consider the case of Real Quantum Theory [BDP12],
where wavefunctions are restricted to take real-valued amplitudes only. Real quantum theory
is modelled by ﬁnite-dimensional real Hilbert spaces, and satisﬁes all the requirements for
the quantum subroutine to be implemented (for all ﬁnite abelian groups G and all subgroup
hiding functions). However, the multiplicative characters arising in Real Quantum Theory
are only the real-valued characters of G: this means that, except in the case G = ZM
2 ,
the classical post-processing part of the algorithm will fail in most cases. Thus said, it is
interesting to note that both the quantum subroutine and the classical post-processing will
work out when G = ZM
2 . As a consequence, Simon’s problem can be eﬃciently solved in
Real Quantum Theory, and the class BQPR (by which we mean BQP for Real Quantum
Theory) is separated from BPP relative to oracles with the appropriate promise.
7.2. Categories of modules over semirings. Spekkens’ toy model [Spe07,CB17] is a toy
theory, based on sets and relations, which shares many of the iconic operational features of
quantum theory while at the same time being fully local. The toy model has been formulated
categorically and diagrammatically [CE12, BD15], and it has been used, in comparison
with the ZX calculus for qubit stabiliser quantum theory, to investigate the relationship
between non-locality and phase groups [CES10]. More recently, formulations of several
quantum algorithms and protocols have been studied in terms of ﬁnite sets and relations,
as opposed to ﬁnite-dimensional Hilbert spaces, and more speciﬁcally within Spekkens’ toy
model [Zen15,DM16]. In particular, a ﬁrst translation of the HSP quantum algorithm to
the category of sets and relation was given in [Zen15].
We take here a broader outlook on things, and consider the extremely general case of
categories of modules over involutive commutative semirings, of which real/complex quantum
theory and the category of sets and relations are all special cases (for the semirings of the
real/complex numbers and the semiring of the booleans respectively). Our approach, using
strong complementarity and diagrammatic methods, will give us control over the HSP in
this broader context, where the Fourier transform itself has not yet been studied. To be
precise, we will ﬁx an arbitrary commutative semiring R with a (possibly trivial) involution
† (that is, a self-inverse semiring homomorphism † : R →R), and we deﬁne the †-SMC
R -Mat of free, ﬁnite-dimensional modules over R:
(i) the objects of R -Mat are labelled by ﬁnite sets;
(ii) the morphisms X →Y in R -Mat are the R-valued matrices indexed by Y × X, i.e.
the free, ﬁnite-dimensional R-module RY ⊗X;
(iii) composition and tensor product are the usual ones for matrices, while the dagger
f† : Y →X of a morphism f : X →Y is given by taking the transpose of the matrix
and then applying the involution to all elements (i.e. (f†)yx := (fxy)†).
The category R -Mat is enriched over itself, and in particular we have a summation operation
+ (matrix addition) and zero morphisms 0 (the zero matrix).


---- page 19 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
19
Our reason to consider R -Mat is the following: on each object X we can deﬁne a canonical
copy/delete coalgebra by Equations 3.1 (with associated †-SCFA), which has the points of the
ﬁnite set X as classical states. Furthermore, for any choice of group structure G := (X, ·, 1)
on X we can deﬁne a group algebra by Equations 3.7: as long as the scalar |G| (which is
well deﬁned in any semiring) can be factored as |G| = ξ†
GξG, the group algebra always gives
rise to a †-qSFA with normalisation factor ξG. If we are willing to weaken the deﬁnition
of quasi-special †-Frobenius algebra to include any scalar Ξ, instead of only positive ones
Ξ := ξ†ξ, then the group algebra always gives rise to a †-qSFA this way: our proof does
not require positivity, and goes through with minor modiﬁcation under this more general
deﬁnition (but we lost the equivalence between quasi-special and special †-Frobenius algebras
in the process, which creates problems with our operational interpretation).
The change from the complex numbers to an arbitrary semiring aﬀects the structure of
characters and representations of groups, with consequent impact on the measurement in
G and on the classical post-processing. Firstly, even in the abelian case there may not be
enough multiplicative characters G →(R×, ·, 1) to distinguish the elements of G themselves,
so that
G fails to have enough classical states: this is usually the case in the category
of sets and relations, because when R is the semiring of the booleans the only character
available is the trivial character. Secondly, even if there are enough multiplicative characters
to distinguish group elements, the classical post-processing step is not guaranteed to go
through on the nose. A detailed study of the structure of characters (i.e. of Fourier theory
over involutive commutative semirings) and of the required generalisation of the classical
post-processing is left to future work.
7.3. Inﬁnite-dimensional HSP. The category Hilb of inﬁnite-dimensional Hilbert spaces
and bounded linear maps does not admit Frobenius algebras, and as a consequence it
cannot be used to extend our abstract setup to inﬁnite abelian groups. However, tools from
non-standard analysis can be used to construct a well-deﬁned category ⋆Hilb of inﬁnite-
dimensional separable Hilbert spaces, including both bounded and unbounded linear maps,
as well as a number of commonplace features of quantum mechanics (such as Dirac deltas
and plane-waves) [GG17].
It has been shown that the category ⋆Hilb possesses suitable strongly complementary
pairs corresponding to the discrete groups ZN of translations of lattices and the compact
groups T N of translations of tori; all the observables concerned are quasi-special or special,
commutative, and have enough classical states. These observables have direct physical
relevance, as they correspond to the momentum/position observable pairs for particles in
N-dimensional boxes with periodic boundary conditions. As a consequence, our scheme
straightforwardly extends to a quantum subroutine for the HSP on the inﬁnite abelian
groups G = ZN (the translation groups of lattices) or their Pontryagin duals G = T N (the
translation groups of tori).
The classical subroutine requires no adjustment for the G = ZN cases: all the possible
quotients G/H, and hence all the possible annihilators Ann[H] ≤T N, are ﬁnite. For the
sake of physical implementation, this corresponds to ﬁxing the computational basis
G in the
momentum eigenstates (valued in ZN) of a particle in an N-dimensional box with periodic
boundary conditions, and performing the
G measurement corresponding to its position
observable (valued in T N). A similar physical setup, with position and momentum swapped,
can be used to tackle the G = T N case, but some minor adjustment will be required in the
classical subroutine (because the annihilators Ann[H] ≤ZN are all inﬁnite).


---- page 20 ----
20
S. GOGIOSO AND A. KISSINGER
8. Conclusions
The abelian Hidden Subgroup Problem comprises many of the problems successfully tackled
by quantum algorithms as special instances, but the traditional presentation of the quantum
solution is too heavily algebraic to clearly show the key structures at work. We improved
upon previous work by presenting the ﬁrst fully graphical proof of correctness for the
algorithm, showing that strong complementarity is the key algebraic feature behind the
quantum advantage in the abelian HSP.
We have remarked that our diagrammatic treatment naturally extends to the non-
abelian case, and that the known intractability of the problem is more a matter of classical
post-processing than an issue with the quantum part itself. We have also shown that our
approach immediately applies to theories other than ﬁnite-dimensional quantum theory, as
long as they possess the required algebraic structures. We have shown that Simon’s Problem
can be eﬃciently solved in Real Quantum Theory, and we have highlighted the issues and
opportunities associated with choices of semirings of scalars other than the traditional
C (Quantum Theory) and R (Real Quantum Theory). We have also seen that our fully
diagrammatic approach immediately applies to the inﬁnite-dimensional case of wavefunctions
in a box with periodic boundary conditions, where it yields an algorithm to solve the HSP
for the inﬁnite abelian groups ZN and T N (translations of N-dimensional lattices and tori,
respectively).
A number of questions remain open. Firstly, the group theoretic nature of the Hidden
Subgroup Problem begs the question of whether strong complementarity is somehow also a
necessary condition for the implementation of a suitable quantum subroutine. Secondly, it
would be interesting to look at more explicit implementations of our results in other suitable
theories, such as Fermionic Quantum Theory [DMPT14], Spekkens’ Toy Model, and inﬁnite-
dimensional quantum theory. Finally, the relationship between strong complementarity and
the quantum Fourier transform prompts further investigation of the role that these algebraic
structures might be playing in a number of other quantum algorithms and protocols.
Acknowledgements.
The authors would like to thank Bob Coecke for comments and suggestions, as well as Sukrita
Chatterji and Nicol`o Chiappori for support. The ﬁrst author would like to acknowledge
support from EPSRC (OUCL/2013/SG) and Trinity College (Williams Scholarship). The
second author would like to acknowledge support from the ERC under the European Union’s
Seventh Framework Programme (FP7/2007-2013) / ERC grant no 320571.
References
[BD15]
Miriam Backens and Ali Nabi Duman. A Complete Graphical Calculus for Spekkens’ Toy Bit
Theory. Foundations of Physics, 46(1):70–103, 2015.
[BDP12]
Alessio Belenchia, Giacomo Mauro D’Ariano, and Paolo Perinotti. Universality of Computation in
Real Quantum Theory. EPL, 104(2):20006, 2013.
[BV97]
Ethan Bernstein and Umesh Vazirani. Quantum Complexity Theory. SIAM Journal on Computing,
26(5):1411–1473, 1997.
[CB17]
Lorenzo Catani and Dan E. Browne. Spekkens’ toy model in all dimensions and its relationship
with stabilizer quantum mechanics. arXiv preprint, 2017.
[CD11]
Bob Coecke and Ross Duncan. Interacting quantum observables: Categorical algebra and diagram-
matics. New Journal of Physics, 13, 2011.


---- page 21 ----
FULLY GRAPHICAL TREATMENT OF THE QUANTUM ALGORITHM FOR THE HSP
21
[CES10]
Bob Coecke, Bill Edwards, and Robert W. Spekkens. Phase groups and the origin of non-locality
for qubits. Electronic Notes in Theoretical Computer Science, 270(2):15–36, 2010.
[CK16]
Bob Coecke and Aleks Kissinger. Picturing Quantum Processes. CUP, 2016.
[Coe09]
Bob Coecke. Quantum Picturalism. Contemporary Physics, pages 1–32, 2009.
[CPP10]
Bob Coecke, Eric Oliver Paquette, and Dusko Pavlovic. Classical and quantum structuralism.
Semantic Techniques in Quantum Computation, pages 29–69, 2010.
[CE12]
Bob Coecke and Bill Edwards. Spekkens’s toy theory as a category of processes. Proceedings of
Symposia in Applied Mathematics, 71:28, 2012.
[CPV13]
Bob Coecke, Dusko Pavlovic, and Jamie Vicary. A new description of orthogonal bases. Mathe-
matical Structures in Computer Science, 23(03), 2013.
[DD16]
Ross Duncan and Kevin Dunne. Interacting Frobenius Algebras are Hopf. Logic in Computer
Science, 2016.
[DM16]
Leonardo Disilvestro and Damian Markham. Quantum Protocols within Spekkens’ Toy Model.
Quantum Physics and Logic, 2016.
[DMPT14] Giacomo Mauro D’Ariano, Franco Manessi, Paolo Perinotti, and Alessandro Tosini. The Feynman
problem and Fermionic entanglement: Fermionic theory versus qubit theory. International Journal
of Modern Physics A, 29(17), 2014.
[EJ96]
Artur Ekert and Richard Jozsa. Quantum computation and Shor’s factoring algorithm. Reviews of
Modern Physics, 68(3):733–753, 1996.
[FS78]
Ferdinand Georg Frobenius and Ludwig Stickelberger. Ueber Gruppen von vertauschbaren Ele-
menten. Journal f¨ur die reine und angewandte Mathematik, 86:217–272, 1878.
[GG17]
Stefano Gogioso and Fabrizio Genovese. Inﬁnite-dimensional Categorical Quantum Mechanics.
Electronic Proceedings in Theoretical Computer Science, 236:51–69, 2017.
[HRS10]
Sean Hallgren, Martin Roetteler, and Pranab Sen. Limitations of Quantum Coset States for Graph
Isomorphism. Journal of the ACM, 57(6), 2010.
[HRTS00] Sean Hallgren, Alexander Russell, and Amnon Ta-Shma. Normal subgroup reconstruction and
quantum computation using group representations. Proceedings of the Thirty Second Annual ACM
Symposium on Theory of Computing, pages 627–635, 2000.
[Joz97]
Richard Jozsa. Quantum Algorithms and the Fourier Transform. 1997.
[Joz01]
Richard Jozsa. Quantum factoring, discrete logarithms, and the hidden subgroup problem. Com-
puting in Science & Engineering, 3(2):1–15, 2001.
[JS91]
Andr´e Joyal and Ross Street. The Geometry of Tensor Calculus I. Advances in Mathematics,
88:55–112, 1991.
[JSV96]
Andr´e Joyal, Ross Street, and Dominic Verity. Traced Monoidal Categories. Mathematical Pro-
ceedings of the Cambridge Philosophical Society, 119(03):447–468, 1996.
[Kis12]
Aleks Kissinger. Pictures of Processes: Automated Graph Rewriting for Monoidal Categories and
Applications to Quantum Computing. PhD thesis, 2012.
[MRS08]
Cristopher Moore, Alexander Russell, and Leonard J. Schulman. The Symmetric Group Deﬁes
Strong Fourier Sampling. SIAM Journal on Computing, 37(6):1842–1864, 2008.
[Reg04a]
Oded Regev. New lattice based cryptographic constructions. J. of the ACM, 51(6):899–942, 2004.
[Reg04b]
Oded Regev. Quantum Computation and Lattice Problems. SIAM Journal on Computing,
33(3):738–760, 2004.
[Sel09]
Peter Selinger. A survey of graphical languages for monoidal categories. Lecture Notes in Physics,
813:289–355, 2009.
[Sho95]
Peter W. Shor. Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on
a Quantum Computer. SIAM Journal on Computing, 26(5):1484–1509, 1997.
[Sim97]
Daniel R. Simon. On the Power of Quantum Computation. SIAM Journal on Computing, 26(5):1474–
1483, 1997.
[Spe07]
Robert W. Spekkens. Evidence for the epistemic view of quantum states: A toy theory. Physical
Review A, 75(3):032110, 2007.
[Vic11]
Jamie Vicary. Categorical Formulation of Finite-Dimensional Quantum Algebras. Communications
in Mathematical Physics, 304(3):765–796, 2011.
[Vic12]
Jamie Vicary. Topological structure of quantum algorithms. In Proceedings of the 2013 28th Annual
ACM/IEEE Symposium on Logic in Computer Science, 2012.
[Zen15]
William Zeng. Models of Quantum Algorithms in Sets and Relations. arXiv preprint, 2015.

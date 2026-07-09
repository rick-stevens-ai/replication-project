<!--
FALLBACK PARSE — Marker was not available in this environment (marker-pdf install
gate on this Python/numpy combo; matches convention used by the sibling
QC-quant-ph-0102014 replication in QC-200).  This file contains the pdftotext
(Poppler) rendering of the paper preserved verbatim so downstream tooling that
expects extraction/marker.md still has structured text to consume.  Layout is
per-column reflow (no `-layout` flag) which is closer in shape to what Marker
would emit than the raw layout dump we save as extraction/nougat.mmd.
-->

arXiv:quant-ph/0603140v1 15 Mar 2006

IS GROVER’S ALGORITHM A QUANTUM HIDDEN
SUBGROUP ALGORITHM ?
SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN
Abstract. The arguments given in this paper suggest that Grover’s and
Shor’s algorithms are more closely related than one might at first expect.
Specifically, we show that Grover’s algorithm can be viewed as a quantum algorithm which solves a non-abelian hidden subgroup problem (HSP). But we
then go on to show that the standard non-abelian quantum hidden subgroup
(QHS) algorithm can not find a solution to this particular HSP.
This leaves open the question as to whether or not there is some modification of the standard non-abelian QHS algorithm which is equivalent to
Grover’s algorithm.

Contents
1. Introduction
1
2. Definition of the hidden subgroup problem (HSP) and hidden subgroup algorithms
3. The generic QHS algorithm QRand
3
4. Pushing HSPs for the generic QHS algorithm QRand
4
5. Shor’s algorithm
5
6. Description of Grover’s algorithm
6
7. The symmetry hidden within Grover’s algorithm
7
8. A comparison of Grover’s and Shor’s algorithms
9
9. However
10
10. Conclusions and Open Questions
11
References
12

1. Introduction
Is Grover’s algorithm a quantum hidden subgroup (QHS) algorithm ?
We do not completely answer this question. Instead, we show that Grover’s
algorithm is a QHS algorithm in the sense that it can be rephrased as a quantum
algorithm which solves a non-abelian hidden subgroup problem (HSP) on the symmetric group SN . But we then go on to show that the standard non-abelian QHS
algorithm cannot solve the Grover HSP.
This leaves unanswered an intriguing question:
Date: March 12, 2006.
1991 Mathematics Subject Classification. [2000]Primary 81P68; Secondary 81P99.
1

2

2

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

Question. Is there an extension or modification of the standard non-abelian QHS
on the symmetric group SN which solves the non-abelian HSP associated with
Grover’s algorithm?
It should be mentioned that, because of a result of Zalka [31], such an algorithm,
if it exists, could not be asymptotically faster than Grover’s algorithm.
We hope that the results found in this paper will lead to a better understanding
of quantum algorithms.
2. Definition of the hidden subgroup problem (HSP) and hidden
subgroup algorithms
What is a hidden subgroup problem ? What is a hidden subgroup algorithm ?
Definition 1. A map ϕ : G −→ S from a group G into a set S is said to have
hidden subgroup structure if there exists a subgroup Kϕ of G, called a hidden
subgroup, and an injection ιϕ : G/Kϕ −→ S, called a hidden injection, such
that the diagram
ϕ
G
−→
S
νց
ր ιϕ
G/Kϕ
is commutative1, where G/Kϕ denotes the collection of right cosets of Kϕ in G,
and where ν : G −→ G/Kϕ is the natural surjection of G onto G/Kϕ . We refer
to the group G as the ambient group and to the set S as the target set. If
Kϕ is a normal subgroup of G, then Hϕ = G/Kϕ is a group, called the hidden
quotient group, and ν : G −→ G/Kϕ is an epimorphism, called the hidden
epimorphism. We will call the above diagram the hidden subgroup structure
of the map ϕ : G −→ S.
Remark 1. The underlying intuition motivating this formal definition is as follows:
Given a natural surjection (or epimorphism) ν : G −→ G/Kϕ , an ”archvillain with
malice of forethought” hides the algebraic structure of ν by intentionally renaming
all the elements of G/Kϕ , and ”tossing in for good measure” some extra elements
to form a set S and a map ϕ : G −→ S.
The hidden subgroup problem can be stated as follows:
Problem 1 (Hidden Subgroup Problem (HSP)). Given a map
ϕ : G −→ S

with hidden subgroup structure, determine a hidden subgroup Kϕ of G. An algorithm solving this problem is called a hidden subgroup algorithm. We will call
a map with hidden subgroup structure a hidden subgroup problem (HSP).
1By saying that this diagram is commutative, we mean ϕ = ι ◦ ν. This concept generalizes
ϕ
in an obvious way to more complicated diagrams.

IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

3

The corresponding quantum form of this HSP is stated as follows:
Problem 2 (Hidden Subgroup Problem: Quantum Version). Let
ϕ : G −→ S
be a map with hidden subgroup structure. Construct a quantum implementation of
the map ϕ as follows:
Let HG and HS be Hilbert spaces defined respectively by the orthonormal bases
{ |gi | g ∈ G } and { |si | s ∈ S } ,
and let s0 = ϕ (1), where 1 denotes the identity of the ambient group G. Finally,
let Uϕ be a unitary transformation such that
Uϕ : HG ⊗ HS
|gi |s0 i

−→ HG ⊗ HS
7−→

,

|gi |ϕ (g)i

Determine the hidden subgroup Kϕ with bounded probability of error by making
as few queries as possible of the blackbox Uϕ . A quantum algorithm solving this
problem is called a quantum hidden subgroup (QHS) algorithm.

3. The generic QHS algorithm QRand
Let ϕ : G −→ S be a map from a group G to a set S with hidden subgroup
structure. We assume that all representations of G are equivalent to unitary
b denote a complete set of distinct irreducible unitary
representations2. Let G
representations of G. Using multiplicative notation for G, we let 1 denote the
b denote the trivial
identity of G, and let s0 denote its image in S. Finally, let 1
representation of G.
b becomes the dual group of characters.
Remark 2. If G is abelian, then G
The generic QHS algorithm is given below:

Quantum Subroutine QRand(ϕ)
Step 0. Initialization

E
b |s0 i ∈ H b ⊗ HS
|ψ0 i = 1
G

−1
Step 1. Application of the inverse Fourier transform FG
of G to the left register
X
1
|ψ1 i = p
|gi |s0 i ∈ HG ⊗ HS ,
|G| g∈G

where |G| denotes the cardinality of the group G.

2This is true for all finite groups as well as a large class of infinite groups.

4

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

Step 2. Application of the unitary transformation Uϕ
1 X
|gi |ϕ (g)i ∈ HG ⊗ HS
|ψ2 i = p
|G| g∈G
Step 3. Application of the Fourier transform FG of G to the left register


X
 
1 X
1 X
†
|ψ3 i =
|γ|
|γ| T race |γi Φ γ †
∈ HGb ⊗HS ,
T race γ (g) |γi |ϕ (g)i =
|G|
|G|
b
γ∈G

g∈G

b
γ∈G

where |γ| denotes the degree of the representation γ, where γ † denotes
T
T
the contragradient representation (i.e., γ † (g) = γ g −1 =γ (g)
E), where

P
P
P
|γ|
|γ|
†
T race γ † (g) |γi = i=1 j=1 γ (g)ji |γij i, and where Φ γij
= g∈G γ ji (g) |ϕ (g)i.
Step 4. Measurement of the left quantum register with respect to the orthonormal
basis
n
o
b 1 ≤ i, j ≤ |γ| .
|γij i : γ ∈ G,
Thus, with probability

P robϕ (γij ) =

|γ|

2

D    E
†
†
|Φ γij
Φ γij
|G|2

,

γij is the measured result, and the quantum system ”collapses” to the state
 E
†
|γij i Φ γij
|ψ4 i = r D    E ∈ HGb ⊗ HS
†
†
|Φ γij
Φ γij
Step 5. Output γij and stop.
4. Pushing HSPs for the generic QHS algorithm QRand
For certain hidden subgroup problems (HSPs) ϕ : G −→ S, the corresponding
generic QHS algorithm QRand either is not physically implementable or is too expensive to implement physically. For example, the HSP ϕ is usually not physically
implementable if the ambient group is infinite (e.g., G is the infinite cyclic group
Z), and is too expensive to implement if the ambient group is too large (e.g., G
is the symmetric group S10100 ). In this case, there is a standard generic way of
”tweaking” the HSP to get around this problem, which we will call pushing.
Definition 2. Let ϕ : G −→ S be a map from a group G to a set S. A map
e −→ S from a group G
e to the set S is said to be a push of ϕ, written
ϕ
e:G
ϕ
e = P ush (ϕ) ,

e from G onto G,
e and a transversal
provided there exists an epimorphism µ : G −→ G
e
τ : G −→ G of µ such that ϕ
e = ϕ ◦ τ.

IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

5

If the epimorphism µ and the transversal τ are chosen in an appropriate way,
then execution of the generic QHS subroutine with input ϕ
e = P ush (ϕ) , i.e.,
execution of
QRand ( e
ϕ) ,
e
will with high probability produce an irreducible representation γ
e of the group G
which is sufficiently close to an irreducible representation γ of the group G. If this
is the case, then there is a polynomial time classical algorithm which upon input γ
e
produces the representation γ.
Obviously, much more can be said about pushing. But unfortunately that
would take us far afield from the objectives of this paper. For more information
on pushing, we refer the reader to [24].

5. Shor’s algorithm
Shor’s factoring algorithm is a classic example of a QHS algorithm created from
the push of an HSP.
Let N be the integer to be factored. Let Z denote the additive group of integers,
and Z×
N denote the monoid of integers under multiplication modulo N (i.e., the
ring of integers modulo N ignoring addition.)
Shor’s algorithm is a QHS algorithm that solves the following HSP
ϕ:Z
m

−→
Z×
N
m
7−→ a mod N

with unknown hidden subgroup structure given by the following commutative diagram
Z
νց

ϕ

−→
Z/P Z

Z×
N
րι

,

where a is an integer relatively prime to N , where P is the hidden integer period of
the map ϕ : Z −→ Z×
N , where P Z is the additive subgroup all integer multiples of
P (i.e., the hidden subgroup), where ν : Z −→ Z/P Z is the natural epimorpism of
of the integers onto the quotient group Z/P Z (i.e., the hidden epimorphism), and
where ι : Z/P Z −→ Z×
N is the hidden monomorphism.
An obstacle to creating a physically implementable algorithm for this HSP is
that the domain Z of ϕ is infinite. As observed by Shor, a way to work around
this difficulty is to push the HSP.
In particular, as illustrated by the following commutative diagram
Z
µ ցտ τ

ϕ

−→
ZQ

Z×
N
ր ϕ = P ush (ϕ) = ϕ ◦ τ

,

6

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

a push ϕ
e = P ush (ϕ) is constructed by selecting the epimorphism µ : Z −→ ZQ of
Z onto the finite cyclic group ZQ of order Q, where the integer Q is the unique
power of 2 such that N 2 ≤ Q < 2N 2 , and choosing the transversal3
τ : ZQ
m mod Q

−→ Z
7−→ m

,

where 0 ≤ m < Q. This push ϕ
e = P ush (ϕ) is called Shor’s oracle.

Shor’s algorithm consists in first executing the quantum subroutine QRand( e
ϕ),
thereby producing a random character
my
γy/Q : m mod Q 7→
mod 1
Q
of the finite cyclic group ZQ . The transversal τ used in pushing has been engineered
to assure that the character γy/Q is sufficiently close to a character
kd
mod 1
P
of the hidden quotient group Z/P Z = ZP . In this case ”sufficiently close” means
that
1
d
y
≤
,
−
Q P
2P 2
which that d/P is a continued fraction convergent of y/Q, and thus can be found
found by the classical polynomial time continued fraction algorithm.
γd/P : k mod P 7→

6. Description of Grover’s algorithm
Now let us turn to Grover’s algorithm. We begin with a brief description.
Consider an unstructured database of N = 2n records labeled without repetitions
with the labels
0, 1, 2, . . . , N − 1.
n
We are given the oracle f : {0, 1} −→ {0, 1}, where

(“Yes”)
 1 if j = j0
f (x) =

0 otherwise (“No”) ,

called Grover’s oracle, and asked to solve the following search problem:

Search Problem for an Unstructured Database. Find the unknown record
labeled as j0 with the minimum amount of computational work, i.e., with the minimum number of queries of the oracle f , and with bounded probability of error.
Let H be the Hilbert space with orthonormal basis

|0i , |1i , |2i , . . . , |N − 1i ,

3A transversal for an epimorphism α : Z −→ Z is an injection τ : Z −→ Z such that
ϕ
ϕ
Q
Q
αϕ ◦ τϕ is the identity map on ZQ , i.e., a map that takes each element of ZQ onto a coset
representative of the element in Z .

IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

7

where N = 2n . Then Grover’s oracle is essentially given as the unitary transformation
I|j0 i : H −→ H
f (j)
|ji 7−→ (−1)
|ji
where
I|j0 i = I − 2 |j0 i hj0 |
is inversion in the hyperplane orthogonal to |j0 i.
Let H denote the Hadamard transform on the Hilbert space H. Then Grover’s
algorithm is given as:
Grover’s Algorithm
STEP 0.

(Initialization)
|ψi ←− H |0i = √1N
k

STEP 1.

←− 0

Loop until k =



N
−1
X
j=0

|ji

π √
4 sin−1 (1/ N )



≈

j √ k
π
4 N

|ψi ←− Q |ψi = −HI|0i HI|j0 i |ψi
k
STEP 2.

←− k + 1

Measure |ψi with respect to the standard basis
|0i , |1i , . . . , |N − 1i to obtain the unknown
state |j0 i with probability ≥ 1 − N1 .

7. The symmetry hidden within Grover’s algorithm
But where is the hidden symmetry in Grover’s algorithm ?
Let SN be the symmetric group on the symbols
0, 1, 2, 3, . . . , N − 1 .

Then Grover’s algorithm is invariant under the hidden subgroup
Stabj0 = {g ∈ SN : g (j0 ) = j0 } ⊂ SN ,

called the stabilizer subgroup for j0 , i.e., Grover’s algorithm is invariant under
the group action
Stabj0 × H

 P

−1
a
|ji
g, N
j
j=0

−→
7−→

H
PN −1
j=0

aj |g(j)i

Moreover, if the hidden subgroup Stabj0 is known, then so is the integer j0 , and
vice versa.

8

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

Thus, Grover’s algorithm is an algorithm that solves the following hidden subgroup problem, which we will henceforth refer to as Grover’s hidden subgroup
problem:

Grover’s Hidden Subgroup Problem. Given a map
ϕ

SN −→ S
from the the symmetric group SN into a target set S = {0, 1, 2, . . . , N − 1} with
hidden subgroup structure given by the commutative diagram
SN
νj0 ց

ϕ

−→
SN /Stabj0

S
րι

,

where νj0 : SN −→ S/Stabj0 is the natural surjection of SN onto the coset space
S/Stabj0 , and where
ι : SN
(j j0 ) Stabj0

ϕ

−→ S
7−→ j

is the unknown relabeling (bijection) of the coset space SN /Stabj0 onto the set
S. Find the hidden subgroup Stabj0 with bounded probability of error.

Let (ij) ∈ SN denote the permutation that interchanges integers i and j, and
leaves all other integers fixed. Thus, (ij) is a transposition if i 6= j, and the identity
permutation 1 if i = j.
Proposition 1. The set
{(0j0 ) , (1j0 ) , (2j0 ) , . . . , ((N − 1) j0 )}
is a complete set of distinct coset representatives for the hidden subgroup Stabj0
of SN , i.e., the coset space SN /Stabj0 is given by the following complete set of
mutually distinct cosets.
SN /Stabj0 = {(0j0 ) Stabj0 , (1j0 ) Stabj0 , (2j0 ) Stabj0 , . . . , ((N − 1) j0 ) Stabj0 }
Proof. Since
−1

(kj0 ) Stabj0 = (ℓj0 ) Stabj0 ⇐⇒ (ℓj0 )

(kj0 ) ∈ Stabj0 ⇐⇒ k = l ,

it follows that
(0j0 ) Stabj0 , (1j0 ) Stabj0 , (2j0 ) Stabj0 , . . . , ((N − 1) j0 ) Stabj0
are mutually distinct cosets of Stabj0 in SN . It now follows from Lagrange’s
theorem that the above collection of mutually distinct cosets is complete.


IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

9

8. A comparison of Grover’s and Shor’s algorithms
Now let us compare Shor’s algorithm with Grover’s.
Let S be the set of integers
n

S = {0, 1, 2, . . . , N − 1} ,

where N = 2 , and let j0 ∈ S denote the unknown label to be found by Grover’s
algorithm.
Shor’s algorithm solves the HSP ϕ : Z −→ Z×
N with hidden subgroup structure
Z
νց

ϕ

−→
Z/P Z

Z×
N
րι

,

where Z×
N can be thought of as the result of the unknown (”malicious”) relabeling
ι : k + P Z 7−→ ak mod N
of Z/P Z.
In like manner, Grover’s algorithm solves an HSP, namely, the HSP ϕ : SN −→ S
with hidden subgroup structure
SN
νց

ϕ

−→
SN /Stabj0

S
րι

,

where S = {0, 1, 2, . . . , N − 1} denotes the set resulting from the unknown (”malicious”) relabeling (bijection)
ι : (j j0 ) Stabj0 7−→ j
of SN /Stabj0 .
For Shor’s algorithm, Shor’s oracle ϕ
e : ZQ −→ Z×
N is created by pushing the
HSP ϕ : Z −→ Z×
N using
Z
µ ցտ τ

ϕ

−→
Z/QZ

Z×
N
րϕ
e

,

thereby producing ϕ
e = P ush(ϕ) = ϕ ◦ τ with the transversal τ : k mod Q 7−→ k.

In like manner, for Grover’s algorithm, Grover’s oracle can be created by pushing
the HSP ϕ : SN −→ S using
SN
µ ցտ τ

ϕ

−→
SN /Stab0

S
րϕ
e

,

thereby producing ϕ
e = P ush(ϕ) = ϕ ◦ τ with the transversal τ : (0 j) Stab0 7−→ SN
of the natural surjection µ.

10

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

Although it is not immediately apparent, the resulting push ϕ
e (for j0 6= 0) is
actually Grover’s oracle relabelled by the injection ι : SN /Stabj0 −→ S. For
ϕ
e = ϕ ◦ τ = (ι ◦ ν) ◦ τ = ι ◦ (ν ◦ τ ) and
(ν ◦ τ ) [(0 j) Stab0 ] =


 (0 j0 ) Stabj0


Stabj0

if j = j0

otherwise

which is informationally the same as Grover’s oracle

f (j) =


 1


0

if j = j0
otherwise

Hence, we can conclude that Grover’s algorithm is an quantum algorithm very
much like Shor’s algorithm, in that it is a quantum algorithm that solves the Grover
hidden subgroup problem.

9. However

However, ... this appears to be where the similarity between these two algorithms
ends. For, the standard non-abelian QHS algorithm on SN for the HSP ϕ (or e
ϕ)
can not find the hidden subgroup Stabj0 for each of the following two reasons:

• Since the subgroups Stabj are not normal subgroups of SN , it follows from
the work of Hallgren et al [11] that the standard non-abelian hidden subgroup algorithm will find the largest normal subgroup of SN lying in Stabj .
But unfortunately, the largest normal subgroup of SN lying in Stabj . is the
trivial subgroup of SN .

• The subgroups Stab0 , Stab1 , ... , StabN −1 are mutually conjugate subgroups of SN .

We should also mention that this hidden subgroup approach can not possibly
lead to a quantum algorithm that is faster than Grover’s.. For Zalka[31] has shown
that Grover’s algorithm is asymptotically optimal.

IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

11

A Comparison of Two Quantum Algorithms
Shor’s Algorithm
Grover’s Algorithm
Similarities
Shor’s algorithm solves
Grover’s algorithm solves
an HSP, namely:
an HSP, namely:
ϕ
ϕ
−→
S
Z
−→
Z×
SN
N
νց
րι
νց
րι
SN /Stabj0
Z/P Z
Pushing ϕ using
Pushing ϕ using
ϕ
ϕ
−→
S
Z
−→
Z×
SN
N
µ ցտ τ
րϕ
e
µ ցտ τ
րϕ
e
Z/QZ
SN /Stab0
produces ϕ
e = P ush(ϕ) = ϕ ◦ τ
produces ϕ
e = P ush(ϕ) = ϕ ◦ τ
which is Shor’s oracle
which is Grover’s oracle (j0 6= 0)
Differences
Repeated calling of the quantum
Repeated calling of the quantum
subroutine QRand( e
ϕ) provides
subroutine QRand( e
ϕ) provides
enough information to solve the
no information whatsoever about
HSP ϕ
the HSP ϕ

10. Conclusions and Open Questions
The arguments made in this paper suggest that Grover’s and Shor’s algorithms
are more closely related quantum algorithms than one might at first expect. Although the standard non-abelian QHS algorithm on SN can not solve the Grover
hidden subgroup problem, there still remains an intriguing question:
Question. Is there some modification or extension of the stantard non-abelian
QHS algorithm on the symmetric group SN that actually solves Grover’s hidden
subgroup problem?
An answer to the above question could lead to a greater insight into how to
create new quantum algorithms.
The methods of this paper can also be applied to Grover’s algorithm for multiple
marked label search. But can they also be applied to other extensions of Grover’s
algorithm such as those found in [2], [3]?
Acknowledgement 1. This work is partially supported by the Defense Advanced
Research Projects Agency (DARPA) and Air Forche Research Laboratory, Air Force
Materiel Command, USAF, under agreement number F30602-01-2-0522. The U.S.
Government is authorized to reproduce and distribute reprints for Governmental
purposes notwithstanding any copyright annotation thereon. This work also partially supported by the Institute for Scientific Interchange (ISI), Torino, the National Institute of Standards and Technology (NIST), the Mathematical Sciences

12

SAMUEL J. LOMONACO, JR. AND LOUIS H. KAUFFMAN

Research Institute (MSRI), the Isaac Newton Institute for Mathematical Sciences,
and the L-O-O-P fund.

References
[1] Bernstein, Ethan, and Umesh Vazirani, Quantum Complexity Theory, SIAM J. of Computing, Vol. 26, No. 5, (1997), pp 1411-1473.
[2] Biham, Eli, Ofer Biham, David Biron, Markus Grassl, and Daniel A. Lidar, Grover’s quantum search algorithm for an arbitrary ininitial amplitude distribution, Phys Rev
A 60, (1999), 2742-2745.
[3] Biham, Eli, Ofer Biham, David Biron, Markus Grassl, Daniel A. Lidar, and Daniel Shapira,
Analysis of generalized Grover’s quantum search algorithm using recursion equations, Phys Rev A 63, 012310 (2001).
[4] Cleve, Richard, Artur Ekert, Chiara Macchiavello, and Michele Mosca, Quantum
Algorithms
Revisited,
Phil. Trans. Roy. Soc. Lond.,
A, (1997).
http://xxx.lanl.gov/abs/quant-ph/9708016
[5] Ekert, Artur K.and Richard Jozsa, Quantum computation and Shor’s factoring algorithm, Rev. Mod. Phys., 68,(1996), pp 733-753.
[6] Ettinger, Mark, and Peter Hoyer, On Quantum Algorithms for Noncommutative Hidden Subgroups, (1998). http://xxx.lanl.gov/abs/quant-ph/9807029
[7] Ettinger, Mark, Peter Hoyer, Emanuel Knill, Hidden Subgroup States Are Almost
Orthogonal, http://xxx.lanl.gov/abs/quant-ph/9901034.
[8] Grover, Lov K., in Proc. 28th Annual ACM Symposium on the Theory of Computation, ACM
Press, new York, (1996), 212-219.
[9] Grover, Lov K., Quantum mechanics helps in searching for a needle in a haystack,
Phys. Rev. Lett., 79(2),(1997). (http://xxx.lanl.gov/abs/quant-ph/9706033)
[10] Grover, Lov K., A framework for fast quantum mechanical algorithms,
http://xxx.lanl.gov/abs/quant-ph/9711043
[11] Hallgren, Sean, Alexander Russell, Amnon Ta-Shma, The Hidden subgroup problem
and quantum computation using group representations, Proceedings of the ThirtySecond Annual ACM Symposium on Theory of Computing, Portland, Oregon, May 2000,
627-635.
[12] Hallgren, Sean, Alexander Russell, Amnon Ta-Shma, The Hidden subgroup problem
and quantum computation using group representations, SIAM J. Comput., Vol. 32,
No. 4, (2003), 916-934.
[13] Ivanyos, Gabor, Frederic Magniez, and Miklos Santha, Efficient quantum algorithms
for some instances of the non-Abelian hidden subgroup problem, (2001).
http://xxx.lanl.gov/abs/quant-ph/0102014
[14] Jozsa, Richard, Quantum algorithms and the Fourier transform, quant-ph preprint
archive 9707033 17 Jul 1997.
[15] Jozsa, Richard, Proc. Roy. Soc. London Soc., Ser. A, 454, (1998), 323 - 337.
[16] Jozsa, Richard, Quantum factoring, discrete logarithms and the hidden
subgroup problem, IEEE Computing in Science and Engineering, (to appear).
http://xxx.lanl.gov/abs/quant-ph/0012084
[17] Kitaev, A., Quantum measurement and the abelian stabiliser problem, (1995),
quant-ph preprint archive 9511026.
[18] Lomonaco, Samuel J., Jr., A Rosetta Stone for quantum mechanics with
an introduction to quantum computation, in “Quantum Computation: A
Grand Mathematical Challenge for the Twenty-First Century and the
Millennium” PSAPM/58, American Mathematical Society, Providence, RI, (2002).
(http://xxx.lanl.gov/abs/quant-ph/0007045 )
[19] Lomonaco,
Samuel
J.,
Jr.,
Shor’s
quantum
factoring
algorithm,
PSAPM/58, American Mathematical Society, Providence, RI, (2002), 161-179.
(http://xxx.lanl.gov/abs/quant-ph/0010034 )
[20] Lomonaco,
Samuel
J.,
Jr.,
Grover’s
quantum
search
algorithm,
PSAPM/58, American Mathematical Society, Providence, RI, (2002), 181-192.
(http://arxiv.org/abs/quant-ph/0010040)

IS GROVER’S ALGORITHM A QUANTUM HIDDEN SUBGROUP ALGORITHM ?

13

[21] Lomonaco, Samuel J., Jr., and Howard E. Brandt, ”Quantum Computation and Information,” Contemporary Mathematics, Vo. 305, American Mathematical Society, Providence, Rhode Island, (2000).
[22] Lomonaco, Samuel J., Jr., and Louis H. Kauffman, Quantum hidden subgroup algorithms: A mathematical perspective, CONM/305, (2000), 139-202.
(http://arxiv.org/abs/quant-ph/0201095)
[23] Lomonaco,
Samuel
J.,
Jr.,
The
non-abelian
Fourier
transform
and
quantum
computation,
MSRI
Streaming
Video,
(2000),
http://www.msri.org/publications/ln/msri/2000/qcomputing/lomonaco/1/index.html
[24] Lomonaco, Samuel J., Jr., and Louis H. Kauffman, Quantum hidden subgroup algorithms on free groups, (in preparation.)
[25] Mosca, Michelle, and Artur Ekert, The Hidden Subgroup Problem and Eigenvalue
Estimation on a Quantum Computer, Proceedings of the 1st NASA International Conference on Quantum Computing and Quantum Communication, Springer-Verlag, (to appear).
(http://xxx.lanl.gov/abs/quant-ph/9903071 )
[26] Russell, Alexander, and Amnon Ta-Shma, Normal Subgroup Reconstruction and
Quantum Computation Using Group Representations, STOC, (2000).
[27] Shor, Peter W., Polynomial time algorithms for prime factorization and discrete
logarithms on a quantum computer, SIAM J. on Computing, 26(5) (1997), pp 1484 1509. (http://xxx.lanl.gov/abs/quant-ph/9508027)
[28] Shor, Peter W., Introduction to quantum algorithms, in “Quantum Computation: A Grand Mathematical Challenge for the Twenty-First Century and
the Millennium,” PSAPM/58, American Mathematical Society, Providence, RI, (2002).
(http://xxx.lanl.gov/abs/quant-ph/0005003 )
[29] van Dam, Wim, and Lawrence Ip, Quantum Algorithms, for Hidden Coset Problems,
manuscript, http://www.cs.caltech.edu/˜hallgren/hcp.pdf
[30] Vazirani, Umesh, On the power of quantum computation, Philosophical Tranactions of
the Royal Society of London, Series A, 354:1759-1768, August 1998.
[31] Zalka, Christof, Grover’s quantum searching algorithm is optimal, Phys. Rev. A, Vol.
60, No. 4, (1999), 2746-2751. (http://xxx.lanl.gov/abs/quant-ph/9711070)
University of Maryland Baltimore County (UMBC), Baltimore, MD 21250
E-mail address: Lomonaco@umbc.edu
URL: http://www.csee.umbc.edu/~lomonaco
Current address: University of Illinois at Chicago, Chicago, IL 60607-7045
E-mail address: kauffman@uic.edu
URL: http://www.math.uic.edu/~kauffman

USA

USA


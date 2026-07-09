# The Hidden Subgroup Problem in Affine Groups: Basis Selection in Fourier Sampling

**Authors:** Cristopher Moore, Daniel Rockmore, Alexander Russell, Leonard J. Schulman

**arXiv:** quant-ph/0211124v3 (24 Feb 2003)

**NOTE:** This is a `pdftotext`-derived Markdown substitute for a native Marker parse. Neither `marker-pdf` nor `nougat-ocr` is installed in this environment; the raw text is preserved verbatim below with light structural annotation.

---

The Hidden Subgroup Problem in Affine
Groups: Basis Selection in Fourier Sampling

arXiv:quant-ph/0211124v3 24 Feb 2003

Cristopher Moore1 , Daniel Rockmore2 , Alexander Russell3 , and Leonard J.
Schulman4
1

University of New Mexico, moore@cs.unm.edu
Dartmouth College, rockmore@cs.dartmouth.edu
3
University of Connecticut, acr@cse.uconn.edu
4
California Institute of Technology, schulman@caltech.edu
2

Abstract. Many quantum algorithms, including Shor’s celebrated factoring and discrete log algorithms, proceed by reduction to a hidden
subgroup problem, in which a subgroup H of a group G must be determined from a quantum state ψ uniformly supported on a left coset of
H. These hidden subgroup problems are then solved by Fourier sampling: the quantum Fourier transform of ψ is computed and measured.
When the underlying group is non-Abelian, two important variants of
the Fourier sampling paradigm have been identified: the weak standard
method, where only representation names are measured, and the strong
standard method, where full measurement occurs. It has remained open
whether the strong standard method is indeed stronger, that is, whether
there are hidden subgroups that can be reconstructed via the strong
method but not by the weak, or any other known, method.
In this article, we settle this question in the affirmative. We show that
hidden subgroups of semidirect products of the form Zq ⋉ Zp , where
q | (p − 1) and q = p/polylog(p), can be efficiently determined by the
strong standard method. Furthermore, the weak standard method and
the “forgetful” Abelian method are insufficient for these groups. We extend this to an information-theoretic solution for the hidden subgroup
problem over the groups Zq ⋉ Zp where q | (p − 1) and, in particular, the
Affine groups Ap . Finally, we prove a closure property for the class of
groups over which the hidden subgroup problem can be solved efficiently.
Submission Track: A

1

The Hidden Subgroup Problem

Simon’s algorithm for the “XOR-mask” oracle problem [19] and Shor’s factoring
algorithm [18] determine an unknown (“hidden”) subgroup H of a given group
G in the following way.
Step 1. Prepare two registers, the first in a uniform superposition over the
elements P
of a group G and the second with
p the value zero, yielding the state
ψ = cG · g∈G |gi ⊗ |0i, where cG = 1/ |G|.

Step 2. Calculate a (classical polynomial-time) function F defined on G and
XOR it with the second
P register. This entangles the two registers and results
in the state ψ = cG · g∈G |gi ⊗ |F (g)i.
Step 3. Measure the second register. This produces a uniform superposition
over one of F ’s level sets, i.e., the set of group elements g for which F (g)
takes a particular value F0 . If the level sets of F are the cosets of H, this
puts the first register in a uniform distribution over superpositions on one
of those cosets, namely cH where F (c) = Fp
it disentangles the
0 . Moreover,
P
two registers, resulting in the state ψ = (1/ |H|)
h∈H |cHi ⊗ |F0 i.

Write the amplitudes of the basis states in the first register as the function
( p
1/ |H| if g ∈ cH,
f (g) =
(1)
0
otherwise.

The approach taken by Simon and Shor is to perform Fourier Sampling [1]: carry
out a quantum Fourier transform on f , and measure the result.
In Simon’s case, the “ambient” group G, over which the Fourier transform is
performed, is Zn2 and H is a subgroup of index 2. In Shor’s case (factoring), G is
the cyclic group Z∗n where n is the number we wish to factor, F (x) = rx mod n
for a random r < n, H is the subgroup of Z∗n of index order(r), and the Fourier
transform is the familiar Abelian one. (However since |Z∗n | is unknown, the above
algorithm is actually performed over Zq where q is polynomially bounded by n;
see [18] or [7,8].) To solve the elusive Graph Automorphism problem, on the
other hand, it would be sufficient to solve the HSP over the permutation group
Sn ; see, e.g., Jozsa [12] for a review. It is partly for this reason that the nonAbelian HSP has remained such an active area of quantum algorithms research.
In general, we will say that the HSP for a family of groups has a Fourier sampling algorithm if a procedure similar to that outlined above works. Specifically,
the algorithm prepares a superposition of the form (1), computes its (quantum)
Fourier transform, and measures the result in a basis of its choice. After a polynomial number of such trials, a polynomial amount of classical computation,
and, perhaps, a polynomial number of classical queries to the function F to confirm the result, the algorithm produces a set of generators for the subgroup H
with high probability.
Since we are typically interested in exponentially large groups, we will take
the size of our input to be n = log |G|. Thus “polynomial” means polylogarithmic
in the size of the group.
History and Context. Though a number of interesting results have been obtained
on the non-Abelian HSP, the groups for which efficient solutions are known remain woefully few and sporadic. On the positive side, Roetteler and Beth [15]
give an algorithm for the wreath product Zk2 ≀ Z2 . Ivanyos, Magniez, and Santha [11] extend this to the more general case of semidirect products K ⋉Zk2 where
K is of polynomial size, and also give an algorithm for groups whose commutator subgroup is of polynomial size. Friedl, Ivanyos, Magniez, Santha and Sen

solve a problem they call Hidden Translation, and thus generalize this further
to what they call “smoothly solvable” groups: these are solvable groups whose
derived series is of constant length and whose Abelian factor groups are each the
direct product of an Abelian group of bounded exponent and one of polynomial
size [4].
In another vein, Ettinger and Høyer [2] show that the HSP is solvable for
the dihedral groups in an information-theoretic sense; namely, a finite number of
quantum queries to the function oracle gives enough information to reconstruct
the subgroup, but the best known reconstruction algorithm takes exponential
time. More generally, Ettinger, Høyer and Knill [3] show that for arbitrary groups
the HSP can be solved information-theoretically with a finite number of quantum
queries, but do not give an explicit set of measurements to do so.
Our current understanding, then, divides groups in three classes
I. Fully Reconstructible. Subgroups of a family of groups G = {Gi } are fully
reconstructible if the HSP can be solved with high probability by a quantum
circuit of size polynomial in log |Gi |.
II. Measurement Reconstructible. Subgroups of a family of groups G =
{Gi } are measurement reconstructible if the solution to the HSP for Gi is
determined information-theoretically by the fully measured result of a quantum circuit of size polynomial in log |Gi |.
III. Query Reconstructible. Subgroups of a family of groups G = {Gi } are
query reconstructible if the solution to the HSP for Gi is determined by
the quantum state resulting from a quantum circuit of polynomial size in
log |Gi |, in the sense that there is a POVM that yields the subgroup H with
constant probability. (Note that there is no guarantee that this POVM can
be implemented by a small quantum circuit.)
In each case, the quantum circuit has oracle access to a function f : G → S, for
some set S, with the property that f is constant on each left coset of a subgroup
H, and distinct on distinct cosets.
In this language, then, the result of [3] shows that subgroups of arbitrary
groups are query reconstructible, whereas it is known that subgroups of Abelian
groups are in fact fully reconstructible. The other work cited above has labored
to place specific families of (non-Abelian) groups into the more algorithmically
meaningful classes I and II above.
All the above results use Abelian Fourier analysis, even in the cases in which
the groups of interest are non-Abelian; it turns out that each of these groups
are “close enough” to Abelian that a “forgetful” Abelian Fourier analysis, which
treats the groups as though their multiplication rule was commutative, suffices
to detect subgroups. Nevertheless, as we shall see, there are situations in which
Abelian Fourier analysis will not suffice and, instead, the full power of the nonAbelian Fourier analysis associated with the group is required.
Fourier analysis over a finite Abelian group A proceeds by expressing a function f : A → C as a linear combination of special functions χ : A → C which
are homomorphisms of A into C. If A = Zp , for example, the homomorphisms
from A to C are exactly the familiar functions χt : z 7→ e2πitz/p ≡ ωptz and

any function f : A → C can be uniquely expressed as a linear combination of
these χt ; this change of basis is precisely the Fourier transform. When G is a
non-Abelian group, however, this same procedure cannot work: in particular,
there are not enough homomorphisms of G into C to even span the space of all
C-valued functions on G. The representation theory of finite groups constructs
the objects which can be used in place of the C-valued homomorphisms above to
develop a satisfactory theory of Fourier analysis over general groups. See [17,5]
for treatments of non-Abelian Fourier analysis and representation theory. In this
general setting Fourier transforms are matrix-valued and our Fourier sampling
algorithm might measure not just which representation we are in, but also the
row and column. See Appendix A for more discussion.
Along these lines, Hallgren, Russell, and Ta-Shma [9] showed that measuring
the names of representations alone — the weak standard method in the terminology of [6] — can reconstruct normal subgroups (and thus solve the HSP for
Hamiltonian groups, all of whose subgroups are normal). More generally, they
show how to reconstruct the normal core of a subgroup, i.e. the intersection of
all its conjugates. On the other hand, they show that this is insufficient to solve
the Graph Automorphism problem, since even in an information-theoretic sense
this method cannot distinguish between the trivial subgroup of Sn and most
subgroups of order 2.
Grigni, Schulman, Vazirani and Vazirani [6] showed that trivial and nontrivial subgroups are still information-theoretically indistinguishable, even if we
do measure the rows and columns of the representation, under the assumption
that a random basis is used for each representation. In other words, even the
strong standard method, in which rows and columns are measured, cannot solve
Graph Automorphism unless there exist bases for the representations of Sn with
very special computational properties. (They also point out that since we can
reconstruct normal subgroups, we can also solve the HSP for groups where the
intersection of all normalizers (the Baer norm) has small index.)
Contributions of this paper. An important open question, then, is whether there
are cases in which the strong standard method offers any advantage over a simple
Abelian transform or the weak standard method. In this paper, we settle this
question in the affirmative. Our results deal primarily with semidirect products
of the form Zq ⋉ Zp , the so-called q-hedral groups, including the affine group
Ap ∼
= Z∗p ⋉ Zp . We show the following:
Theorem 1. Let p and q be prime with q = (p − 1)/polylog(p). Then subgroups
of Zq ⋉ Zp are fully reconstructible.
More generally, we define the Hidden Conjugate Problem as follows: given a
group G, a non-normal subgroup H, and a function which is promised to be
constant on the cosets of some conjugate bHb−1 of H, identify b. We adopt the
above classification (fully/ measurement/ query) for this problem in the natural
way. Then we also show that
Theorem 2. Let p be prime and q a divisor of p−1. Then the hidden conjugates
of H in G = Zq ⋉ Zp are fully reconstructible if H has index polylog(p).

Moreover, our algorithms in Theorems 1 and 2 rely crucially on the highdimensional representations of Zq ⋉ Zp , and we show that Abelian methods (in
other words, treating the group as a direct product rather than a semidirect one)
do not suffice.
We also generalize the results of Ettinger and Høyer on the dihedral group
to the q-hedral groups:
Theorem 3. Let p be prime and q a divisor of p − 1. Then hidden conjugates
in Zq ⋉ Zp are measurement reconstructible.
We then reduce the general problem of hidden subgroup reconstruction in Zq ⋉Zp
(and Ap ) to Theorem 3:
Theorem 4. Let p be prime and q a divisor of p − 1. The subgroups of the
q-hedral groups Zq ⋉ Zp are measurement reconstructible. In particular, the subgroups of the affine groups Ap = Z∗p−1 ⋉ Zp are measurement reconstructible.
In Theorems 3 and 4 we give an explicit set of efficiently computable measurements from which the subgroup can be reconstructed, with a (possibly exponential) amount of classical computation.
Finally, we show that the set of groups for which the HSP can be solved in
polynomial time has the following closure property:
Theorem 5. Let H be a group for which hidden subgroups are fully reconstructible, and K a group of polynomial size in log |H|. Then hidden subgroups
in any extension of K by H, i.e. any group G with K ⊳ G and G/K ∼
= H, are
fully reconstructible.
This subsumes the results of [9] on Hamiltonian groups, and also those of [11]
on groups with commutator subgroups of polynomial size.
The Non-Abelian Fourier Transform. To solve the HSP for the non-Abelian
groups discussed above, we shall consider the more general setting of non-Abelian
Fourier analysis. Briefly, we treat a representation as a homomorphism ρ : G →
U(d), where U(d) denotes the group of unitary operators on Cd . We call dρ = d
the dimension of ρ. For a function f : G → C and an irreducible representation
ρ, we let fˆ(ρ) denote the Fourier transform of f at ρ, given by
s
dρ X
ˆ
f (ρ) =
f (g)ρ(g).
|G| g
A more complete description of the representations of a group G and the associated transform appear in Appendix A. The Fourier transform of a function of
the form (1) is then
s
X
dρ
ˆ
ρ(c) ·
ρ(h).
f (ρ) =
|G||H|
h∈H

P
As H is aPsubgroup, h ρ(h) is |H| times a projection operator (see, e.g., [9]);
we write h ρ(h) = |H| πH . (Its rank is determined by the number of copies of
the trivial representation in the representation IndG
H 1.) With this notation, we
√
ˆ
write f (ρ) = nρ ρ(c) · πH where nρ = dρ |H|/|G|. For a d × d matrix M , we let
P
2
2
kM k denote the matrix norm given by kM k = ij |Mij | . Then the probability
that we observe the representation ρ is
fˆ(ρ)

2

=

√

nρ ρ(c)πH

2

2

2

= nρ kρ(c)k kπH k = nρ rk πH ,

where rk πH is the rank of the projection operator πH . See [9] for discussion.

2

The Affine Group Ap

Let Ap be the affine group of size p(p − 1) for p prime, consisting of functions
(a, b) : x 7→ ax + b on Zp acting by composition, where a ∈ Z∗p and b ∈ Zp . Thus
Ap is a semidirect product Z∗p ⋉ Zp where (a1 , b1 ) · (a2 , b2 ) = (a1 a2 , b1 + a1 b2 )
(we adopt the convention that functions compose on the right). We enumerate
the subgroups below:
– Let N ∼
= Zp be the normal subgroup of size p consisting of elements of the
form (1, b).
– Let H be the non-normal subgroup of size p − 1 consisting of the elements
of the form (a, 0). Its conjugates H b = (1, b) · H · (1, −b) consist of elements
of the form (a, (1 − a)b). (In the action on Zp , H b is the stabilizer of b).
– More generally, if a ∈ Z∗p has order q, let Na ∼
= Zq ⋉ Zp be the normal
subgroup consisting of all elements of the form (at , b), and let Ha be the nonnormal subgroup Ha = h(a, 0)i of size q. Then Ha consists of the elements
of the form (at , 0) and its conjugates Hab = (1, b) · Ha · (1, −b) consist of the
elements of the form (at , (1 − at )b).

To discuss Ap ’s representations, fix a generator γ of Z∗p and let φ : Z∗p → Zp−1
be the isomorphism φ(γ t ) = t. Let ωp denote the p’th root of unity e2πi/p . Then
G has p − 1 one-dimensional representations σs which are simply the representφ(a)
tations of Z∗p ∼
= Zp−1 given by σt ((a, b)) = ωp−1 and one (p − 1)-dimensional
representation ρ. In the multiplicative basis whose indices j, k are elements of
Z∗p , we have:
 bj
ωp k = aj mod p
ρ((a, b))j,k =
, 1 ≤ j, k < p .
0 otherwise
We review the construction of these representations in Appendix B.
The affine group — and more generally, the q-hedral groups we discuss below
— are metacyclic groups, i.e. extensions of a cyclic group Zp by a cyclic group Zq .
In [10], Høyer showed how to perform the non-Abelian Fourier transform over
such groups in a polynomial (i.e. polylog(p)) number of elementary quantum
operations. (In fact, he does this only up to an overall phase factor, but this is
sufficient for our purposes.)

Conjugates of the Largest Non-Normal Subgroup. In this section we solve the
Hidden Conjugate Problem, in which we are promised that f is a superposition
over some coset of one of the conjugates H b of the largest non-normal subgroup
H, and our job is to identify which conjugate, i.e. to identify b. First note that
nρ = dρ |H|/|G| = (p − 1)/p = 1 − 1/p. Then a little calculation shows that,
b(j−k)
in the multiplicative basis, π(H b )j,k = (1/p − 1) ωp
, 1 ≤ j, k < p. This
is a circulant matrix of rank 1. More specifically, every column is some root
of unity times the vector (ub )j = (1/p − 1) ωpbj , 1 ≤ j < p. This is also true
of ρ(c) · π(H b ); since ρ(c) has one nonzero entry per column, left multiplying
by ρ(c) simply multiplies each column of π(H b ) by a phase. Therefore, we can
first carry out a partial measurement on the columns, and then transform the
rows by left-multiplying ρ(cH) by the quantum Fourier transform over Zp−1 ,
−ℓj
Qℓ,j = (1/p − 1) ωp−1
. We can now infer b by measuring the frequency ℓ. We
observe a given value of ℓ with probability
p−1
1 X bj −ℓj
P (ℓ) =
ω ω
p − 1 j=1 p p−1

where θ =



b
ℓ
p − p−1



2

p−1
X
1
e2iθj
=
(p − 1)2 j=1

2

=

1
sin2 (p − 1)θ
2
(p − 1)
sin2 θ

π. Now note that for any b there is an ℓ such that |θ| ≤

π/(2(p−1)). Since (2x/π)2 ≤ sin2 x ≤ x2 for |x| ≤ π/2, this gives P (ℓ) ≥ (2/π)2 .
Finally, the probability that we observed the (p − 1)-dimensional representation ρ in the first place is nρ = 1 − 1/p. Thus if we measure ρ, the column, and
then ℓ and then guess that b minimizes |θ|, we will be right Ω(1) of the time.
We boost this to high probability by repeating a polynomial number of times.
Subgroups with Large Index. We focus next on the Hidden Conjugate Problem
for the subgroups Ha where a’s order q is a proper divisor of p − 1. Recall that a
given conjugate of Ha consists of the elements of the form (at , (1 − at )b). Then
in the multiplicative basis we have

1 ωpb(j−k) k = at j mod p for some t
b
, 1 ≤ j, k < p .
π(Ha )j,k =
q 0
otherwise
In other words, the nonzero entries are those for which j and k are in the same
coset of hai ⊂ Z∗p . The rank of this projection operator is thus the number of
cosets, which is the index (p − 1)/q of hai in Z∗p . Since nρ is now q/p, we again
observe ρ with probability nρ rk π(H) = (p − 1)/p = 1 − 1/p.
We will show that we can reconstruct the conjugates of Ha in polynomial
time if a has large order, in particular when the index of hai is polylog(p). If
q is prime then Ha is the only non-normal subgroup of Zq ⋉ Zp , so we can
completely solve the Hidden Subgroup Problem for these groups. For instance,
if q is a Sophie Germain prime, i.e. one for which 2q + 1 is also a prime, we can
solve the HSP for Zq ⋉ Z2q+1 . This establishes Theorem 1.
Following the same procedure as before, we do a partial measurement on the
columns of ρ, and then Fourier transform the rows. After changing the variable

of summation from t to −t and adding a phase shift of e−iθ(p−1) inside the | · |2 ,
the probability we observe a frequency ℓ, assuming we find ourselves in the k’th
column, is
q−1
X
t
1
−ℓat k
P (ℓ) = p
ωpbka ωp−1
q(p − 1) t=0

2

q−1
X
t
1
eiθ(2a k−(p−1))
=
q(p − 1) t=0

2

.

(2)

Now note that the terms in the sum are of the form eiφ where (assuming w.l.o.g.
that θ is positive) φ ∈ [−θ(p − 1), θ(p − 1)]. If we again take ℓ so that |θ| ≤
π/(2(p−1)), then φ ∈ [−π/2, π/2] and all the terms in the sum have nonnegative
real parts. We will lower bound the real part of the sum by showing that a
constant fraction of the terms have φ ∈ (−π/3, π/3), and thus have real part
more than 1/2. This is the case whenever at k ∈ (p/6, 5p/6), so it is sufficient to
prove the following lemma:
Lemma 1. Let a have order q = p/polylog(p). Then for any ǫ > 0 at least
(1/3 − ǫ)q of the elements in the coset haik are in the interval (p/6, 5p/6).
Proof. We will prove this using Gauss sums, which quantify the interplay between the additive and multiplicative behavior of Zp and thus establish bounds
on the distribution of powers of a. Specifically, if a has order q in Z∗p then for any
Pq−1 t
integer k 6≡ 0 (modp) we have t=0 ωpa k = O(p1/2 ) = o(p). (See Appendix C.)
Now suppose s of the elements x in haik are in the set (p/6, 5p/6), for which
Re ωpx ≥ −1, and the other q − s elements are in [0, p/6] ∪ [5p/6, p), for which
Pq−1 at k
Re ωpx ≥ 1/2. Thus we have Re t=0
ωp ≥ (q/2) − (3s/2). If s ≤ (1/3 − ǫ)q
for any ǫ > 0 this is Θ(q), a contradiction.

Now that we know that a fraction 1/3 − ǫ of the terms in (2) have real part
at least 1/2 and the others have real part at least 0, we can take ǫ = 1/12 (say)
and write
 q 2
1 q
1
1
=
=
.
P (ℓ) ≥
q(p − 1) 8
8p−1
polylog(p)
Thus we observe the correct frequency with polynomially small probability, and
we again boost this to high probability by repeating a polynomial number of
times. This establishes Theorem 2.

3

The q-hedral Groups

In general, if a has multiplicative order q, then we are in the subgroup Zq ⋉ Zp ⊂
Ap , the q-hedral group. In this section we show that the conjugates of Ha are then
measurement reconstructible — i.e. are information-theoretically reconstructible
from a polynomial number of quantum queries given by a polynomial size quantum circuit, followed by a possibly exponential amount of classical computation.
It follows that subgroups of the q-hedral groups are measurement reconstructible
whenever q has polylog(p) divisors — for instance, Ap (where q = p − 1) if p is a
Fermat prime 2k +1. (Note also that for a prime selected at random in {1, . . . , n}

for large n, p − 1 has no more than polylog(p) divisors with high probability.)
This generalizes the results of Ettinger and Høyer [2] who showed this for the
case q = 2, i.e. the dihedral groups.
The representations of Zq ⋉ Zp include the q one-dimensional representations
of Zq given by σℓ ((at , b)) = ωqℓt , ℓ ∈ Zq and (p − 1)/q q-dimensional representations ρk ,
 kas b
ωp
t = s + u mod q
u
, 0 ≤ s, t < q .
ρk (a , b))s,t =
0
otherwise
Here k ranges over the elements of Z∗p /Zq , or, to put it differently, k takes values
in Z∗p but ρk and ρk′ are isomorphic if k and k ′ are in the same coset of hai.
These ρk are simply the (p − 1)/q diagonal blocks of the (p − 1)-dimensional
representation ρ of Ap (this is perhaps a little easier to see in the additive basis).
Then summing ρk over the elements (at , (1 − at )b) gives πk (Hab )s,t =
k(as −at )b

(1/q) ωp
, 0 ≤ s, t < q. This is again a matrix of rank 1, where each
column (even after left multiplication by ρk (c)) is some root of unity times the
s
vector (uk )s = (1/q) ωpka b . Note that nρ = q/p.
We now wish to show that there is a measurement whose outcomes given
two distinct values of b have polynomial total variation distance. First, we perform a series of partial measurements as follows: (i.) measure the name of the
representation; (ii.) measure the column of the representation; (iii.) perform a
POVM with q outcomes, in each of which s is u or u + 1 mod q for some u ∈ Zq .
The total probability we observe one of the q-dimensional representations, since
there are (p − 1)/q of them, is nρ (p − 1)/q = 1 − 1/p. Then these three partial
measurements determine k, remove the effect of the coset, and determine that s
has one of two values, u or u + 1. Up to an overall phase we can write this as a
two-dimensional vector
 kau b 
ωp
1
√
kau+1 b
ω
2
p
√  
We now apply the Hadamard transform (1/ 2) 11−11 and measure s. The prob-

ability we observe u and u + 1 is then cos2 θ and sin2 θ respectively, where
θ = (πkau (a − 1)b)/p. Now when we observe a q-dimensional representation,
the k we observe is uniformly distributed over Z∗p /Zq , and when we perform the
POVM, the u we observe is uniformly distributed over Zq . It follows that the
coefficient m = kau (u − 1) is uniformly distributed over Z∗p . For any two distinct
b, b′ , the total variation distance is then

X 
1
πmb
πmb′
πmb′
πmb
+ sin2
− cos2
− sin2
cos2
2(p − 1)
p
p
p
p
∗
m∈Zp

X
πmb′
2πmb′
1
πmb
2πmb
1 X
− cos2
− cos
=
cos2
cos
p−1
p
p
2(p − 1)
p
p
m∈Zp
m∈Zp


2
X
p
2πmb
2πmb′
1
1
=
cos
− cos
>
.
≥
4(p − 1)
p
p
4(p − 1)
4
=

m∈Zp

(Adding the m = 0 term contributes zero to the sum in the second line. In the
third line we use the facts that |x| ≤ x2 /2 for all |x| ≤ 2, the average of cos2 is
1/2, and the two cosines have zero inner product.)
Since the total variation distance between any two distinct conjugates is
bounded below by a constant, by standard results in probability theory we can
distinguish between the p different conjugates with only O(log p) = poly(n)
queries. Thus hidden conjugates in q-hedral groups are measurement reconstructible, completing the proof of Theorem 3.
What remains to be seen is that in a group of form Zq ⋉ Zp , where q | p − 1, it
is possible to determine the order of a hidden subgroup. Were this possible, based
on Theorem 3, we could (measurement) reconstruct arbitrary hidden subgroups
of Zq ⋉ Zp . Let H be a hidden subgroup of Zq ⋉ Zp given by the oracle f :
αk
1
Zq ⋉ P
Zp → S, and let pα
1 . . . pk be the prime factorization of q, in which case
i
| |H|. This
k ≤ i αi = O(log q). For each i ∈ [k], we will determine if pα
i
suffices to determine |H|, at which point the subgroup H can be determined by
Theorem 3.
By initially applying the techniques of [9] (the weak standard method), we
may (fully) reconstruct H if H is a non-trivial normal subgroup. (This follows
because these particular semidirect product groups have the special property
that if A is a non-trivial normal subgroup and A ⊂ B, then B is normal; in
particular, the normal core
\
γCγ −1
γ∈G

of any non-normal subgroup C is the identity group.) It remains to consider
non-normal subgroups H. Recall that in this case, H is cyclic and |H| is equal
to the order of a, where H = h(a, b)i. Now, for each i ∈ [k] and 1 ≤ α ≤ αi , let
Υiα : Zq ⋉ Zp → Zq/pαi be the homomorphism given by
α

Υiα : (a, b) 7→ api .
αi

α
pi
i
= 1}, where 1 denotes the identity
Then let Aα
i = ker Υi = {γ ∈ Zq ⋉ Zp | γ
αi
element of Zq ⋉ Zp . Ai is the subgroup of Zq ⋉ Zp consisting of all elements
whose orders are a multiple of pα
i . Consider now the function

(f, Υiα ) : Zq ⋉ Zp → S × Zq/pαi
given by (f, Υiα )(γ) = (f (γ), Υiα (γ)). Observe that (f, Υiα ) is constant (and disα
tinct) on the left cosets of H ∩ Aα
i and, furthermore, the subgroup H ∩ Ai has
α
α
order p if and only if p divides the order of a. We may then determine if
α
H ∩ Aα
i has order p by assuming that it does, applying the result of Theorem 3,
and checking the result against the original oracle f . This allows us to determine the prime factorization of |H|, as desired. Therefore, all subgroups of the
q-hedral groups Zq ⋉ Zp are measurement reconstructible, completing the proof
of Theorem 4.
However, as in the dihedral case [2], we know of no polynomial-time algorithm
which can reconstruct the most likely b from these queries.

4

Failure of the Abelian Fourier Transform

Suppose we try to reconstruct subgroups of Ap using the Abelian Fourier transform over the direct product Z∗p × Zp instead of using Ap ’s non-Abelian structure
as a semidirect product. We first consider trying to solve the hidden conjugate
problem for Ha where a has order p − 1.
kt
If a is a generator, the characters of Z∗p × Zp are simply ρk,ℓ (at , b) = ωp−1
ωpℓb .
t
t
Summing these over Ha = {(a , (1 − a )b} shows that we observe the character
(k, ℓ) with probability
2

1
P (k, ℓ) =
p (p − 1)2

X

t∈Z/(p−1)

t
kt
ωp−1
ωpℓ(1−a )b

2

X k log x
1
=
ωp−1 a ωp−ℓxb
2
p (p − 1)
∗
x∈Zp

This is the inner product of a multiplicative character with an additive one,
which is another Gauss sum. In particular, assuming b 6= 0, we have P (0, 0) =
1/p, P (0, ℓ 6= 0) = 1/(p (p − 1)2 ), P (k 6= 0, 0) = 0, and P (k 6= 0, ℓ 6= 0) =
1/(p − 1)2 . (See Appendix C.) Since these probabilities don’t depend on b, the
different conjugates Hab with b 6= 0 are indistinguishable from each other. Thus
it appears essential that we use the use non-Abelian Fourier transform and the
high-dimensional representations of Ap .
(For the q-hedral groups, when q is small enough it is information-theoretically
possible to reconstruct the subgroup from the Abelian Fourier transform. In fact,
Ettinger and Høyer [2] use the Abelian Fourier transform over Z2 × Zp in their
reconstruction algorithm for the dihedral groups.)

5

Closure Under Extending Small Groups

In this section we prove Theorem 5, that for any polynomial-size group K and
any H for which we can solve the HSP, we can also solve the HSP for any
extension of K by H, i.e. any group G with K ⊳ G and G/K ∼
= H. (Note that
this is more general than split extensions, i.e. semidirect products H ⋉ K.) This
includes the case discussed in [9] of Hamiltonian groups, since all such groups
are direct products (and hence extensions) by Abelian groups of the quaternion
group Q8 [16]. It also includes the case discussed in [4] of groups with commutator
subgroups of polynomial size, such as extra-special p-groups, since in that case
K = G′ and H ∼
= G/G′ is Abelian. Indeed, our proof is an easy generalization
of that in [4].
We assume that G and K are encoded in such a way that multiplication can
be carried out in classical polynomial time. We fix some transversal t(h) of the
left cosets of K. First, note that any subgroup L ⊆ G can be described in terms
of i) its intersection L ∩ K, ii) its projection LH = L/(L ∩ K) ⊆ H, and iii)
a representative η(h) ∈ L ∩ (t(h) · K) for each h ∈ LH . S
Then each element of
LH is associated with some left coset of L ∩ K, i.e. L = h∈LH η(h) · (L ∩ K).
Moreover, if S is a set of generators for L ∩ K and T is a set of generators for
LH , then S ∪ η(T ) is a set of generators for L.

.

We can reconstruct S in classical polynomial time simply by querying F on
all of K. Then L ∩ K is the set of all k such that F (k) = F (1), and we construct
S by adding elements of L ∩ K to it one at a time until they generate all of
L ∩ K.
To identify LH , as in [4] we define a new function F ′ on H consisting of the
unordered collection of the values of F on the corresponding left coset of K:
F ′ (h) = {F (g) | g ∈ t(h) · K}. Each query to F ′ consists of |K| = poly(n) queries
to K. The level sets of F ′ are clearly the cosets of LH , so we reconstruct LH by
solving the HSP on H. This yields a set T of generators for LH .
It remains to find a representative η(h) in L ∩ (t(h) · K) for each h ∈ T .
We simply query F (g) for all g ∈ t(h) · K, and set η(h) to any g such that
F (g) = F (1). Since |T | = O(log |H|) = poly(n) this can be done in polynomial
time, and we are done.
Unfortunately, we cannot iterate this construction more than a constant number of times, since doing so would require a superpolynomial number of queries
to F for each query of F ′ . If K has superpolynomial size it is not clear how to
obtain η(h), even when H has only two elements: this is precisely the difficulty
with the dihedral group. This completes the proof of Theorem 5.

References
1. Ethan Bernstein and Umesh Vazirani. Quantum complexity theory (preliminary
abstract). In Proceedings of the Twenty-Fifth Annual ACM Symposium on the
Theory of Computing, pages 11–20, San Diego, California, 16–18 May 1993.
2. Mark Ettinger and Peter Høyer. On quantum algorithms for noncommutative
hidden subgroups. Technical Report quant-ph/9807029, Quantum Physics e-Print
Archive, 1998.
3. Mark Ettinger and Peter Høyer and Emmanuel Knill. Hidden subgroup states are
almost orthogonal. Technical Report quant-ph/9901034, Quantum Physics e-Print
Archive, 1999.
4. Katalin Friedl, Gábor Ivanyos, Frédéric Magniez, Miklos Santha, and Pranab Sen.
Hidden translation and orbit coset in quantum computing. Technical Report
quant-ph/0211091, Quantum Physics e-Print Archive, 2002.
5. William Fulton and Joe Harris. Representation Theory: A First Course. Number
129 in Graduate Texts in Mathematics. Springer-Verlag, 1991.
6. Michelangelo Grigni, Leonard J. Schulman, Monica Vazirani, and Umesh Vazirani.
Quantum mechanical algorithms for the nonabelian hidden subgroup problem. In
Proceedings of the 33rd ACM Symposium on Theory of Computing, pages 68–74,
2001.
7. Lisa Hales and Sean Hallgren. Quantum fourier sampling simplified. In Proceedings
of the Thirty-First Annual ACM Symposium on Theory of Computing, Atlanta,
Georgia, 1–4 May 1999.
8. Lisa Hales and Sean Hallgren. An improved quantum fourier transform algorithm
and applications. In 41st Annual Symposium on Foundations of Computer Science.
IEEE, 2000.
9. Sean Hallgren, Alexander Russell, and Amnon Ta-Shma. Normal subgroup reconstruction and quantum computation using group representations. In Proceedings
of the 32nd ACM Symposium on Theory of Computing, pages 627–635, 2000.

10. Peter Høyer. Efficient quantum transforms. Technical Report quant-ph/9702028,
Quantum Physics e-Print Archive, 1997.
11. Gábor Ivanyos, Frédéric Magniez, and Miklos Santha. Efficient quantum algorithms
for some instances of the non-Abelian hidden subgroup problem. Technical Report
quant-ph/0102014, Quantum Physics e-Print Archive, 2001.
12. Richard Jozsa. Quantum factoring, discrete logarithms and the hidden subgroup
problem. Technical Report quant-ph/0012084, Quantum Physics e-Print Archive,
2000.
13. Sergei V. Konyagin and Igor E. Shparlinski. Character sums with exponential
functions and their applications. Number 136 in Cambridge Tracts in Mathematics.
Cambridge University Press, Cambridge, 1999.
14. Rudolf Lidl and Harald Niederreiter. Finite Fields. Number 20 in Encyclopedia of
Mathematics and its Applications. Cambridge University Press, 1997.
15. Martin Roetteler and Thomas Beth. Polynomial-time solution to the hidden subgroup problem for a class of non-abelian groups. Technical Report
quant-ph/9812070, Quantum Physics e-Print Archive, 1998.
16. Joseph Rotman. An Introduction to the Theory of Groups. Number 148 in Graduate
Texts in Mathematics. Springer-Verlag, 1994.
17. Jean-Pierre Serre. Linear Representations of Finite Groups. Number 42 in Graduate Texts in Mathematics. Springer-Verlag, 1977.
18. Peter W. Shor. Polynomial-time algorithms for prime factorization and discrete
logarithms on a quantum computer. SIAM Journal on Computing, 26(5):1484–
1509, October 1997.
19. Daniel R. Simon. On the power of quantum computation. SIAM Journal on
Computing, 26(5):1474–1483, October 1997.

Acknowledgements. We are grateful to Wim van Dam, Frederic Magniez,
Martin Rötteler, and Miklos Santha for helpful conversations, and to Sally Milius
and Tracy Conrad for their support. Support for this work was provided by the
California Institute of Technology’s Institute for Quantum Information (IQI), the
Mathematical Sciences Research Institute (MSRI), the Institute for Advanced
Study (IAS), NSF grants ITR-0220070 and QuBIC-0218563, the Charles Lee
Powell Foundation, and the Bell Fund.

A

The Non-Abelian Fourier Transform

To solve the HSP for the non-Abelian groups discussed above, we shall have to
consider the more general setting of non-Abelian Fourier analysis. Here, instead
of the familiar basis functions hk (x) = ωpkx , which are homomorphisms from
Zp into C, we have representations ρ which are homomorphisms from G into
U(d), the group of unitary d × d matrices with entries in C. We call dρ = d the
dimension of ρ.
We say that two representations ρ : G → U(d) and σ : G → U(d) are
isomorphic if there is a non-singular linear map ι : Cd → Cd for which ρ(g) ◦ ι =
ι ◦ σ(g) for every g ∈ G. Though there are an infinite number of non-isomorphic
representations of a given group G, there is a natural notion of “decomposition”

that applies to such representations; with respect to this notion, a finite group G
has a finite number of “irreducible” representations up to isomorphism, and every
other representation may be expressed in terms of these basic building blocks.
Specifically, we say that a representation ρ : G → U(d) is reducible if there is a
nontrivial subspace {0} ( W ( Cd with the property that ρ(g)(W ) ⊂ W for all
g ∈ G. A representation is irreducible if no such subspace exists.
For a given group G, there are only a finite number of irreducible representations upto isomorphism; we let Ĝ denote a set of irreducible representations
of G containing one from each isomorphism class.
Let f : G → C be a function and ρ an irreducible representation of G. Then
the Fourier transform of f at ρ, written fˆ(ρ), is the operator
s
dρ X
ˆ
f (ρ) =
f (g)ρ(g).
|G| g
The functional notation fˆ(ρ) is somewhat misleading, as fˆ(ρ) is a dρ ×dρ matrix,
the dimension dρ being determined by the representation ρ. By selecting an
orthonormal basis for Cdρ for each ρ, we may associate with f p
the family of
complex numbers fˆ(ρ)ij , where 1 ≤ i, j ≤ dρ ; With the constants dρ /|G|, the
linear transformation
f 7→ hfˆ(ρ)i,j iρ∈Ĝ,1≤i,j≤dρ
is in fact unitary.
The Fourier transform of a function of the form (1) is then
s
X
dρ
ρ(c) ·
ρ(h).
fˆ(ρ) =
|G||H|
h∈H
P
As H is aPsubgroup, h ρ(h) is |H| times a projection operator (see, e.g., [9]);
we write h ρ(h) = |H| πH . (Its rank is determined by the number of copies of
the trivial representation in the representation IndG
H 1.) With this notation, we
√
write fˆ(ρ) = nρ ρ(c) · πH where nρ = dρ |H|/|G|. For a d × d matrix M , we let
P
2
2
kM k denote the matrix norm given by kM k = ij |Mij | . Then the probability
that we observe the representation ρ is
fˆ(ρ)

2

=

√

nρ ρ(c)πH

2

2

2

= nρ kρ(c)k kπH k = nρ rk πH ,

where rk πH is the rank of the projection operator πH . See [9] for more discussion.

B

Constructing Ap’s Representations; Induced
Representations

In this Appendix we construct the (p − 1)-dimensional representation of Ap by
inducing upward from a one-dimensional representation of the normal subgroup
N∼
= Zp . We begin with a short discussion of induced representations.

Let G be a group, H a subgroup of G, and σ : H → U(d) a representation of
H. We shall define a representation IndG
H σ of G, the induced representation. Let
Γ = {γ1 , . . . , γt } ⊂ G be a left transversal of H in G, so that G = ∪γ∈Γ γH, this
union being disjoint. The representation IndG
H σ is defined
P on the vector space
of dimension d|G|/|H| whose elements are formal sums γ∈Γ γ · vγ , where each
P
vγ ∈ Cd . Addition and scalar multiplication are given by the rule
γ · uγ +
P
P
P
P
γ · vγ = γ · (uγ + vγ ) and c γ · vγ = γ · cvγ . Then IndG
σ
is
defined
by
H
linearly extending the rule
h
i
′
IndG
H σ(g) γ · vγ 7→ γ · σ(h)vγ

where (γ ′ , h) is the unique pair in Γ × H so that gγ = γ ′ h.
Returning now to the affine group, let τt (1, b) 7→ ωptb for 0 ≤ t < p be
the p distinct one-dimensional characters of the normal subgroup N = Zp . Let
H = Ap /N ∼
= Z∗p . Consider the conjugation action of H on these characters:
that is, define (a, 0) ⊙ τt (1, b) = τt [(a, 0)(1, b)(a, 0)−1 ] = τt (1, ab) = τat (1, b).
Note that this action has two orbits, one consisting of the trivial character τ0
and the other consisting of all non-trivial character.
Now, considering the first orbit, consisting of τ0 alone, we see that the isotropy
subgroup is all of H. Now, let ρ0 be the extension of σ0 to all of H (which
makes sense, since it was stable under the H-action). Then for each irreducible
Ap
(ρ0 ⊗ σ̌).
representation σ̌ of H, we get an irreducible representation σ = IndHN
(Note that this gives rise to the representations σs above.)
Focusing on the other orbit, for simplicity consider σ̌1 . Since H is cyclic,
the isotropy subgroup of σ1 is the identity subgroup and this gives rise to the
A
A
representation ρ = IndNp σ̌1 . Now IndNp operates on the vector space W =
(1, 0)C ⊕ . . . ⊕ (p − 1, 0)C. The action is
A

[IndNp (a, b)] · (i, 0) 7→ σ̌1 ((ai)−1 b)(ai, 0).
so that
A

[IndNp (a, b)]j,k =



ωpbj k = aj mod p
, 1 ≤ j, k < p
0 otherwise

which is precisely the (p − 1)-dimensional representation ρ in the multiplicative
basis. We can construct the q-dimensional representations of the q-hedral groups
in a similar way.

C

Notes on Exponential Sums

The basic Gauss sum bounds the inner products of additive and multiplicative
characters of Fp , the finite field with p elements. Definitive treatments appear
in [14, §5] and [13]. Considering Fp as an additive group with p elements, we
have p additive characters χs : Fp → C, for s ∈ Fp , given by
χs : z 7→ ωpsz ,

where ωp = e2πi/p is a primitive pth root of unity. Likewise considering the
elements of F∗p = Fp \ {0} as a multiplicative group, we have p − 1 characters
ψt : F∗p → C, for t ∈ F∗p , given by
tz
ψt : g z 7→ ωp−1
,

where ωp−1 = e2πi/(p−1) is a primitive p − 1st root of unity and g is a multiplicative generator for the (cyclic) group F∗p .
With this notation the basic Gauss sum is the following:
Theorem 6. Let χs be a multiplicative character and ψt an additive character
of Fp . If s 6= 0 and t 6= 1 then
X

χs (z)ψt (z) =

√
p.

z∈F∗
p

Otherwise



p − 1
χs (z)ψt (z) = −1


z∈F∗
p
0
X

if s = 0, t = 1,
if s = 0, t 6= 1,
if s 6= 0, t = 1.

See [14, §5.11] for a proof.
This basic result has been spectacularly generalized. In the body of the paper
we require bounds on additive characters taken over multiplicative subgroups of
F∗p . Such sums are discussed in detail in [13]. The specific bound we require is
the following.
Theorem 7. Let χt be a nontrivial additive character of Fp and a ∈ F∗p an
element of multiplicative order q. Then

1/2

if q ≥ p2/3 ,
q−1
O(p ),
X
z
χt (a ) = O(p1/4 q 3/8 ), if p1/2 ≤ q ≤ p2/3 ,


z=0
O(p1/8 q 5/8 ), if p1/3 ≤ q ≤ p1/2 .

See [13, §2] for a proof.
Note that in the body of the paper, we use Zp to denote the additive group of
integers modulo p and Z∗p to denote the multiplicative group of integers modulo
p.


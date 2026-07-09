# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:0707.2831 — Shor & Jordan, 'Estimating Jones Polynomials is a Complete Problem for One Clean Qubit'

## Page 1

arXiv:0707.2831v3  [quant-ph]  1 Feb 2008
Estimating Jones Polynomials is a Complete Problem for One
Clean Qubit
Peter W. Shor∗and Stephen P. Jordan†
Abstract
It is known that evaluating a certain approximation to the Jones polynomial for the plat closure of
a braid is a BQP-complete problem. That is, this problem exactly captures the power of the quantum
circuit model[13, 3, 1]. The one clean qubit model is a model of quantum computation in which all but one
qubit starts in the maximally mixed state. One clean qubit computers are believed to be strictly weaker
than standard quantum computers, but still capable of solving some classically intractable problems [21].
Here we show that evaluating a certain approximation to the Jones polynomial at a ﬁfth root of unity
for the trace closure of a braid is a complete problem for the one clean qubit complexity class. That is,
a one clean qubit computer can approximate these Jones polynomials in time polynomial in both the
number of strands and number of crossings, and the problem of simulating a one clean qubit computer
is reducible to approximating the Jones polynomial of the trace closure of a braid.
1
One Clean Qubit
The one clean qubit model of quantum computation originated as an idealized model of quantum computation
on highly mixed initial states, such as appear in NMR implementations[21, 4]. In this model, one is given an
initial quantum state consisting of a single qubit in the pure state |0⟩, and n qubits in the maximally mixed
state. This is described by the density matrix
ρ = |0⟩⟨0| ⊗I
2n .
One can apply any polynomial-size quantum circuit to ρ, and then measure the ﬁrst qubit in the com-
putational basis. Thus, if the quantum circuit implements the unitary transformation U, the probability of
measuring |0⟩will be
p0 = Tr[(|0⟩⟨0| ⊗I)UρU †] = 2−nTr[(|0⟩⟨0| ⊗I)U(|0⟩⟨0| ⊗I)U †].
(1)
Computational complexity classes are typically described using decision problems, that is, problems
which admit yes/no answers. This is mathematically convenient, and the implications for the complexity of
non-decision problems are usually straightforward to obtain (cf. [24]). The one clean qubit complexity class
consists of the decision problems which can be solved in polynomial time by a one clean qubit machine with
correctness probability of at least 2/3. The experiment described in equation 1 can be repeated polynomially
many times. Thus, if p1 ≥1/2 + ǫ for instances to which the answer is yes, and p1 ≤1/2 −ǫ otherwise, then
by repeating the experiment poly(1/ǫ) times and taking the majority vote one can achieve 2/3 probability of
correctness. Thus, as long as ǫ is at least an inverse polynomial in the problem size, the problem is contained
in the one clean qubit complexity class. Following [21], we will refer to this complexity class as DQC1.
A number of equivalent deﬁnitions of the one clean qubit complexity class can be made. For example,
changing the pure part of the initial state and the basis in which the ﬁnal measurement is performed does
∗Mathematics Department, Massachusetts Institute of Technology, Cambridge, Massachusetts 02139. shor@math.mit.edu
†Center for Theoretical Physics, Massachusetts Institute of Technology, Cambridge, Massachusetts 02139. sjordan@mit.edu
1


---

## Page 2

1
√
2(|0⟩+ |1⟩)
•
H
FE

|ψ⟩
/
U
/
p0 = 1+Re(⟨ψ|U|ψ⟩)
2
Figure 1: This circuit implements the Hadamard test. A horizontal line represents a qubit. A horizontal line with
a slash through it represents a register of multiple qubits. The probability p0 of measuring |0⟩is as shown above.
Thus, one can obtain the real part of ⟨ψ| U |ψ⟩to precision ǫ by making O(1/ǫ2) measurements and counting what
fraction of the measurement outcomes are |0⟩. Similarly, if the control bit is instead initialized to
1
√
2(|0⟩−i |1⟩), one
can estimate the imaginary part of ⟨ψ| U |ψ⟩.
not change the resulting complexity class. Less trivially, allowing logarithmically many clean qubits results
in the same class, as discussed below. It is essential that on a given copy of ρ, measurements are performed
only at the end of the computation. Otherwise, one could obtain a pure state by measuring ρ thus making
all the qubits “clean” and re-obtaining BQP. Remarkably, it is not necessary to have even one fully polarized
qubit to obtain the class DQC1. As shown in [21], a single partially polarized qubit suﬃces.
In the original deﬁnition[21] of DQC1 it is assumed that a classical computer generates the quantum
circuits to be applied to the initial state ρ. By this deﬁnition DQC1 automatically contains the complexity
class P. However, it is also interesting to consider a slightly weaker one clean qubit model, in which the
classical computer controlling the quantum circuits has only the power of NC1. The resulting complexity
class appears to have the interesting property that it is incomparable to P. That is, it is not contained in
P nor does P contain it. We suspect that our algorithm and hardness proof for the Jones polynomial carry
over straightforwardly to this NC1-controlled one clean qubit model. However, we have not pursued this
point.
Any 2n × 2n unitary matrix can be decomposed as a linear combination of n-fold tensor products of
Pauli matrices. As discussed in [21], the problem of estimating a coeﬃcient in the Pauli decomposition of a
quantum circuit to polynomial accuracy is a DQC1-complete problem. Estimating the normalized trace of
a quantum circuit is a special case of this, and it is also DQC1-complete. This point is discussed in [27]. To
make our presentation self-contained, we will sketch here a proof that trace estimation is DQC1-complete.
Technically, we should consider the decision problem of determining whether the trace is greater than a given
threshold. However, the trace estimation problem is easily reduced to its decision version by the method of
binary search, so we will henceforth ignore this point.
First we’ll show that trace estimation is contained in DQC1. Suppose we are given a quantum circuit on
n qubits which consists of polynomially many gates from some ﬁnite universal gate set. Given a state |ψ⟩
of n qubits, there is a standard technique for estimating ⟨ψ| U |ψ⟩, called the Hadamard test[3], as shown in
ﬁgure 1. Now suppose that we use the circuit from ﬁgure 1, but choose |ψ⟩uniformly at random from the
2n computational basis states. Then the probability of getting outcome |0⟩for a given measurement will be
p0 = 1
2n
X
x∈{0,1}n
1 + Re(⟨x| U |x⟩)
2
= 1
2 + Re(Tr U)
2n+1
.
Choosing |ψ⟩uniformly at random from the 2n computational basis states is exactly the same as inputting
the density matrix I/2n to this register. Thus, the only clean qubit is the control qubit. Trace estimation
is therefore achieved in the one clean qubit model by converting the given circuit for U into a circuit for
controlled-U and adding Hadamard gates on the control bit. One can convert a circuit for U into a circuit
for controlled-U by replacing each gate G with a circuit for controlled-G. The overhead incurred is thus
bounded by a constant factor [23].
Next we’ll show that trace estimation is hard for DQC1. Suppose we are given a classical description of
a quantum circuit implementing some unitary transformation U on n qubits. As shown in equation 1, the
probability of obtaining outcome |0⟩from the one clean qubit computation of this circuit is proportional to
2


---

## Page 3

•
U
•
•
/
/




Figure 2: Here CNOT gates are used to simulate 3 clean ancilla qubits.
the trace of the non-unitary operator (|0⟩⟨0| ⊗I)U(|0⟩⟨0| ⊗I)U †, which acts on n qubits. Estimating this
can be achieved by estimating the trace of
U ′ =
U †
•
U
•
/
/


which is a unitary operator on n + 2 qubits. This suﬃces because
Tr[(|0⟩⟨0| ⊗I)U(|0⟩⟨0| ⊗I)U †] = 1
4Tr[U ′].
(2)
To see this, we can think in terms of the computational basis:
Tr[U ′] =
X
x∈{0,1}n
⟨x| U ′ |x⟩.
If the ﬁrst qubit of |x⟩is |1⟩, then the rightmost CNOT in U ′ will ﬂip the lowermost qubit. The resulting
state will be orthogonal to |x⟩and the corresponding matrix element will not contribute to the trace. Thus
this CNOT gate simulates the initial projector |0⟩⟨0| ⊗I in equation 2. Similarly, the other CNOT in U ′
simulates the other projector in equation 2.
The preceding analysis shows that, given a description of a quantum circuit implementing a unitary
transformation U on n-qubits, the problem of approximating
1
2n Tr U to within ±
1
poly(n) precision is DQC1-
complete.
Some unitaries may only be eﬃciently implementable using ancilla bits. That is, to implement U on
n-qubits using a quantum circuit, it may be most eﬃcient to construct a circuit on n + m qubits which acts
as U ⊗I, provided that the m ancilla qubits are all initialized to |0⟩. These ancilla qubits are used as work
bits in intermediate steps of the computation. To estimate the trace of U, one can construct a circuit Ua on
n + 2m qubits by adding CNOT gates controlled by the m ancilla qubits and acting on m extra qubits, as
shown in ﬁgure 2. This simulates the presence of m clean ancilla qubits, because if any of the ancilla qubits
is in the |1⟩state then the CNOT gate will ﬂip the corresponding extra qubit, resulting in an orthogonal
state which will not contribute to the trace.
With one clean qubit, one can estimate the trace of Ua to a precision of
2n+2m
poly(n,m). By construction,
Tr[Ua] = 2mTr[U]. Thus, if m is logarithmic in n, then one can obtain Tr[U] to precision
2n
poly(n), just as can
be obtained for circuits not requiring ancilla qubits. This line of reasoning also shows that the k-clean qubit
model gives rise to the same complexity class as the one clean qubit model, for any constant k, and even for
k growing logarithmically with n.
It seems unlikely that the trace of these exponentially large unitary matrices can be estimated to this
precision on a classical computer in polynomial time. Thus it seems unlikely that DQC1 is contained in
3


---

## Page 4

Figure 3: Shown from left to right are the unknot, another representation of the unknot, an oriented trefoil knot,
and the Hopf link. Broken lines indicate undercrossings.
I.
III.
II.
Figure 4: Two knots are the same if and only if one can be deformed into the other by some sequence of the three
Reidemeister moves shown above.
P. (For more detailed analysis of this point see [10].) However, it also seems unlikely that DQC1 contains
all of BQP. In other words, one clean qubit computers seem to provide exponential speedup over classical
computation for some problems despite being strictly weaker than standard quantum computers.
2
Jones Polynomials
A knot is deﬁned to be an embedding of the circle in R3 considered up to continuous transformation (isotopy).
More generally, a link is an embedding of one or more circles in R3 up to isotopy. In an oriented knot or
link, one of the two possible traversal directions is chosen for each circle. Some examples of knots and links
are shown in ﬁgure 3. One of the fundamental tasks in knot theory is, given two representations of knots,
which may appear superﬁcially diﬀerent, determine whether these both represent the same knot. In other
words, determine whether one knot can be deformed into the other without ever cutting the strand.
Reidemeister showed in 1927 that two knots are the same if and only if one can be deformed into the
other by some sequence constructed from three elementary moves, known as the Reidemeister moves, shown
in ﬁgure 4. This reduces the problem of distinguishing knots to a combinatorial problem, although one for
which no eﬃcient solution is known. In some cases, the sequence of Reidemeister moves needed to show
equivalence of two knots involves intermediate steps that increase the number of crossings.
Thus, it is
very diﬃcult to show upper bounds on the number of moves necessary. The most thoroughly studied knot
equivalence problem is the problem of deciding whether a given knot is equivalent to the unknot. Even
showing the decidability of this problem is highly nontrivial. This was achieved by Haken in 1961[14]. In
1998 it was shown by Hass, Lagarias, and Pippenger that the problem of recognizing the unknot is contained
in NP[15].
A knot invariant is any function on knots which is invariant under the Reidemeister moves. Thus, a
knot invariant always takes the same value for diﬀerent representations of the same knot, such as the two
representations of the unknot shown in ﬁgure 3. In general, there can be distinct knots which a knot invariant
fails to distinguish.
One of the best known knot invariants is the Jones polynomial, discovered in 1985 by Vaughan Jones[18].
To any oriented knot or link, it associates a Laurent polynomial in the variable t1/2. The Jones polynomial
has a degree in t which grows at most linearly with the number of crossings in the link. The coeﬃcients
are all integers, but they may be exponentially large. Exact evaluation of Jones polynomials at all but a
few special values of t is #P-hard[16]. The Jones polynomial can be deﬁned recursively by a simple “skein”
relation. However, for our purposes it will be more convenient to use a deﬁnition in terms of a representation
of the braid group, as discussed below.
To describe in more detail the computation of Jones polynomials we must specify how the knot will
4


---

## Page 5

Figure 5: Shown from left to right are a braid, its plat closure, and its trace closure.
be represented on the computer. Although an embedding of a circle in R3 is a continuous object, all the
topologically relevant information about a knot can be described in the discrete language of the braid group.
Links can be constructed from braids by joining the free ends.
Two ways of doing this are taking the
plat closure and the trace closure, as shown in ﬁgure 5. Alexander’s theorem states that any link can be
constructed as the trace closure of some braid. Any link can also be constructed as the plat closure of some
braid. This can be easily proven as a corollary to Alexander’s theorem, as shown in ﬁgure 6.
Figure 6: A trace closure of a braid on n strands can be converted to a plat closure of a braid on 2n strands by
moving the “return” strands into the braid.
B
A
A
B
I.
II.
Figure 7: Shown are the two Markov moves. Here the boxes represent arbitrary braids. If a function on braids is
invariant under these two moves, then the corresponding function on links induced by the trace closure is a link
invariant.
Given that the trace closure provides a correspondence between links and braids, one may attempt to
ﬁnd functions on braids which yield link invariants via this correspondence. Markov’s theorem shows that
a function on braids will yield a knot invariant provided it is invariant under the two Markov moves, shown
in ﬁgure 7. Thus the Markov moves provide an analogue for braids of the Reidemeister moves on links. The
constraints imposed by invariance under the Reidemeister moves are enforced in the braid picture jointly by
invariance under Markov moves and by the deﬁning relations of the braid group.
5


---

## Page 6

A linear function f satisfying f(AB) = f(BA) is called a trace. The ordinary trace on matrices is one
such function. Taking a trace of a representation of the braid group yields a function on braids which is
invariant under Markov move I. If the trace and representation are such that the resulting function is also
invariant under Markov move II, then a link invariant will result. The Jones polynomial can be obtained in
this way.
In [3], Aharonov, et al. show that an additive approximation to the Jones polynomial of the plat or trace
closure of a braid at t = ei2π/k can be computed on a quantum computer in time which scales polynomially
in the number of strands and crossings in the braid and in k. In [1, 31], it is shown that for plat closures,
this problem is BQP-complete. The complexity of approximating the Jones polynomial for trace closures
was left open, other than showing that it is contained in BQP.
The results of [3, 1, 31] reformulate and generalize the previous results of Freedman et al.
[13, 12],
which show that certain approximations of Jones polynomials are BQP-complete. The work of Freedman
et al. in turn builds upon Witten’s discovery of a connection between Jones polynomials and topological
quantum ﬁeld theory [30]. Recently, Aharonov et al. have generalized further, obtaining an eﬃcient quantum
algorithm for approximating the Tutte polynomial for any planar graph, at any point in the complex plane,
and also showing BQP-hardness at some points [2]. As special cases, the Tutte polynomial includes the
Jones polynomial, other knot invariants such as the HOMFLY polynomial, and partition functions for some
physical models such as the Potts model.
The algorithm of Aharonov et al. works by obtaining the Jones polynomial as a trace of the path model
representation of the braid group. The path model representation is unitary for t = ei2π/k and, as shown
in [3], can be eﬃciently implemented by quantum circuits. For computing the trace closure of a braid the
necessary trace is similar to the ordinary matrix trace except that only a subset of the diagonal elements of
the unitary implemented by the quantum circuit are summed, and there is an additional weighting factor. For
the plat closure of a braid the computation instead reduces to evaluating a particular matrix element of the
quantum circuit. Aharonov et al. also use the path model representation in their proof of BQP-completeness.
Given a braid b, we know that the problem of approximating the Jones polynomial of its plat closure
is BQP-hard. By Alexander’s theorem, one can obtain a braid b′ whose trace closure is the same link as
the plat closure of b. The Jones polynomial depends only on the link, and not on the braid it was derived
from. Thus, one may ask why this doesn’t immediately imply that estimating the Jones polynomial of the
trace closure is a BQP-hard problem. The answer lies in the degree of approximation. As discussed in
section 6, the BQP-complete problem for plat closures is to approximate the Jones polynomial to a certain
precision which depends exponentially on the number of strands in the braid. The number of strands in b′
can be larger than the number of strands in b, hence the degree of approximation obtained after applying
Alexander’s theorem may be too poor to solve the original BQP-hard problem.
The fact that computing the Jones polynomial of the trace closure of a braid can be reduced to estimating
a generalized trace of a unitary operator and the fact that trace estimation is DQC1-complete suggest a
connection between Jones polynomials and the one clean qubit model. Here we ﬁnd such a connection by
showing that evaluating a certain approximation to the Jones polynomial of the trace closure of a braid
at a ﬁfth root of unity is DQC1-complete. The main technical diﬃculty is obtaining the Jones polynomial
as a trace over the entire Hilbert space rather than as a summation of some subset of the diagonal matrix
elements.
To do this we will not use the path model representation of the braid group, but rather the
Fibonacci representation, as described in the next section.
3
Fibonacci Representation
The Fibonacci representation ρ(n)
F
of the braid group Bn is described in [19] in the context of Temperley-Lieb
recoupling theory. Temperley-Lieb recoupling theory describes two species of idealized “particles” denoted
by p and ∗.
We will not delve into the conceptual and mathematical underpinnings of Temperley-Lieb
recoupling theory. For present purposes, it will be suﬃcient to regard it as a formal procedure for obtaining
a particular unitary representation of the braid group whose trace yields the Jones polynomial at t = ei2π/5.
6


---

## Page 7

p
p
p
p
*
*
*
Figure 8: For an n-strand braid we can write a length n + 1 string of p and ∗symbols across the base. The string
may have no two ∗symbols in a row, but can be otherwise arbitrary.
σi =
σ−1
i
=
i
1
i+1
n
...
...
i
i+1
n
1
...
...
Figure 9: σi denotes the elementary crossing of strands i and i + 1. The braid group on n strands Bn is generated
by σ1 . . . σn−1, which satisfy the relations σiσj = σjσ for |i −j| > 1 and σi+1σiσi+1 = σiσi+1σi for all i. The group
operation corresponds to concatenation of braids.
Throughout most of this paper it will be more convenient to express the Jones polynomial in terms of
A = e−i3π/5, with t deﬁned by t = A−4.
It is worth noting that the Fibonacci representation is a special case of the path model representation
used in [3]. The path model representation applies when t = ei2π/k for any integer k, whereas the Fibonacci
representation is for k = 5.
The relationship between these two representations is brieﬂy discussed in
appendix C. However, for the sake of making our discussion self contained, we will derive all of our results
directly within the Fibonacci representation.
Given an n-strand braid b ∈Bn, we can write a length n + 1 string of p and ∗symbols across the base
as shown in ﬁgure 8. These strings have the restriction that no two ∗symbols can be adjacent. The number
of such strings is fn+3, where fn is the nth Fibonacci number, deﬁned so that f1 = 1, f2 = 1, f3 = 2, . . .
Thus the formal linear combinations of such strings form an fn+3-dimensional vector space. For each n, the
Fibonacci representation ρ(n)
F
is a homomorphism from Bn to the group of unitary linear transformations on
this space. We will describe the Fibonacci representation in terms of its action on the elementary crossings
which generate the braid group, as shown in ﬁgure 9.
The elementary crossings correspond to linear operations which mix only those strings which diﬀer by
the symbol beneath the crossing. The linear transformations have a local structure, so that the coeﬃcients
for the symbol beneath the crossing to be changed or unchanged depend only on that symbol and its two
neighbors. For example, using the notation of [19],
p
*
p
p
p
p
p
*
p
= c
d
+
(3)
which means that the elementary crossing σi corresponds to a linear transformation which takes any string
whose ith through (i + 2)th symbols are p ∗p to the coeﬃcient c times the same string plus the coeﬃcient
d times the same string with the ∗at the (i + 1)th position replaced by p. (As shown in ﬁgure 9, the ith
crossing is over the (i + 1)th symbol.) To compute the linear transformation that the representation of a
given braid applies to a given string of symbols, one can write the symbols across the base of the braid, and
then apply rules of the form 3 until all the crossings are removed, and all that remains are various coeﬃcients
for diﬀerent strings to be written across the base of a set of straight strands.
For compactness, we will use (pb∗p) = c(p ∗p) + d(ppp) as a shorthand for equation 3. In this notation,
7


---

## Page 8

the complete set of rules is as follows.
(∗bpp)
=
a(∗pp)
(∗bp∗)
=
b(∗p∗)
(pb∗p)
=
c(p ∗p) + d(ppp)
(pbp∗)
=
a(pp∗)
(pbpp)
=
d(p ∗p) + e(ppp),
(4)
where
a
=
−A4
b
=
A8
c
=
A8τ 2 −A4τ
d
=
A8τ 3/2 + A4τ 3/2
e
=
A8τ −A4τ 2
A
=
e−i3π/5
τ
=
2/(1 +
√
5).
(5)
Using these rules we can calculate any matrix from the Fibonacci representation of the braid group.
Notice that this is a reducible representation. These rules do not allow the rightmost symbol or leftmost
symbol of the string to change. Thus the vector space decomposes into four invariant subspaces, namely the
subspace spanned by strings which begin and end with p, and the ∗. . . ∗, p . . . ∗, and ∗. . . p subspaces. As
an example, we can use the above rules to compute the action of B3 on the ∗. . . p subspace.
ρ(3)
∗p (σ1) =

b
0
0
a

∗p∗p
∗ppp
ρ(3)
∗p (σ2) =

c
d
d
e

∗p∗p
∗ppp
(6)
In appendix A we prove that the Jones polynomial evaluated at t = ei2π/5 can be obtained as a weighted
trace of the Fibonacci representation over the ∗. . . ∗and ∗. . . p subspaces.
4
Computing the Jones Polynomial in DQC1
As mentioned previously, the Fibonacci representation acts on the vector space of formal linear combinations
of strings of p and ∗symbols in which no two ∗symbols are adjacent. The set of length n strings of this
type, Pn, has fn+2 elements, where fn is the nth Fibonacci number: f1 = 1, f2 = 1, f3 = 2, and so on. As
shown in appendix E, one can construct a bijective correspondence between these strings and the integers
from 0 to fn+2 −1 as follows. If we think of ∗as 1 and p as 0, then with a string snsn−1 . . . s1 we associate
the integer
z(s) =
n
X
i=1
sifi+1.
(7)
This is known as the Zeckendorf representation.
Representing integers as bitstrings by the usual method of place value, we thus have a correspondence
between the elements of Pn and the bitstrings of length b = ⌈log2(fn+2)⌉. This correspondence will be a
key element in computing the Jones polynomial with a one clean qubit machine. Using a one clean qubit
machine, one can compute the trace of a unitary over the entire Hilbert space of 2n bitstrings. Using CNOT
gates as above, one can also compute with polynomial overhead the trace over a subspace whose dimension
is a polynomially large fraction of the dimension of the entire Hilbert space. However, it is probably not
possible in general for a one clean qubit computer to compute the trace over subspaces whose dimension is
8


---

## Page 9

an exponentially small fraction of the dimension of the total Hilbert space. For this reason, directly mapping
the strings of p and ∗symbols to strings of 1 and 0 will not work. In contrast, the correspondence described
in equation 7 maps Pn to a subspace whose dimension is at least half the dimension of the full 2b-dimensional
Hilbert space.
In outline, the DQC1 algorithm for computing the Jones polynomial works as follows. Using the results
described in section 1, we will think of the quantum circuit as acting on b maximally mixed qubits plus
O(1) clean qubits. Thinking in terms of the computational basis, we can say that the ﬁrst b qubits are in
a uniform probabilistic mixture of the 2b classical bitstring states. By equation 7, most of these bitstrings
correspond to elements of Pn. In the Fibonacci representation, an elementary crossing on strands i and i−1
corresponds to a linear transformation which can only change the value of the ith symbol in the string of p’s
and ∗’s. The coeﬃcients for changing this symbol or leaving it ﬁxed depend only on the two neighboring
symbols. Thus, to simulate this linear transformation, we will use a quantum circuit which extracts the
(i −1)th, ith, and (i + 1)th symbols from their bitstring encoding, writes them into an ancilla register while
erasing them from the bitstring encoding, performs the unitary transformation prescribed by equation 4 on
the ancillas, and then transfers this symbol back into the bitstring encoding while erasing it from the ancilla
register. Constructing one such circuit for each crossing, multiplying them together, and performing DQC1
trace-estimation yields an approximation to the Jones polynomial.
Performing the linear transformation demanded by equation 4 on the ancilla register can be done easily
by invoking gate set universality (cf. Solovay-Kitaev theorem [23]) since it is just a three-qubit unitary
operation. The harder steps are transferring the symbol values from the bitstring encoding to the ancilla
register and back.
It may be diﬃcult to extract an arbitrary symbol from the bitstring encoding. However, it is relatively
easy to extract the leftmost “most signiﬁcant” symbol, which determines whether the Fibonacci number fn
is present in the sum shown in equation 7. This is because, for a string s of length n, z(s) ≥fn−1 if and
only if the leftmost symbol is ∗. Thus, starting with a clean |0⟩ancilla qubit, one can transfer the value
of the leftmost symbol into the ancilla as follows. First, check whether z(s) (as represented by a bitstring
using place value) is ≥fn−1. If so ﬂip the ancilla qubit. Then, conditioned on the value of the ancilla qubit,
subtract fn−1 from the bitstring. (The subtraction will be done modulo 2b for reversibility.)
Any classical circuit can be made reversible with only constant overhead.
It thus corresponds to a
unitary matrix which permutes the computational basis. This is the standard way of implementing classical
algorithms on a quantum computer[23]. However, the resulting reversible circuit may require clean ancilla
qubits as work space in order to be implemented eﬃciently. For a reversible circuit to be implementable
on a one clean qubit computer, it must be eﬃciently implementable using at most logarithmically many
clean ancillas. Fortunately, the basic operations of arithmetic and comparison for integers can all be done
classically by NC1 circuits [29]. NC1 is the complexity class for problems solvable by classical circuits of
logarithmic depth. As shown in [4], any classical NC1 circuit can be converted into a reversible circuit using
only three clean ancillas. This is a consequence of Barrington’s theorem. Thus, the process described above
for extracting the leftmost symbol can be done eﬃciently in DQC1.
More speciﬁcally, Krapchenko’s algorithm for adding two n-bit numbers has depth ⌈log n⌉+ O(√log n)
[29]. A lower bound of depth log n is also known, so this is essentially optimal [29]. Barrington’s construction
[7] yields a sequence of 22d gates on 3 clean ancilla qubits [4] to simulate a circuit of depth d. Thus we obtain
an addition circuit which has quadratic size (up to a subpolynomial factor). Subtraction can be obtained
analogously, and one can determine whether a ≥b can be done by subtracting a from b and looking at
whether the result is negative.
Although the construction based on Barrington’s theorem has polynomial overhead and is thus suﬃcient
for our purposes, it seems worth noting that it is possible to achieve better eﬃciency. As shown by Draper
[11], there exist ancilla-free quantum circuits for performing addition and subtraction, which succeed with
high probability and have nearly linear size. Speciﬁcally, one can add or subtract a hardcoded number
a into an n-qubit register |x⟩modulo 2n by performing quantum Fourier transform, followed by O(n2)
controlled-rotations, followed by an inverse quantum Fourier transform. Furthermore, using approximate
quantum Fourier transforms[8, 6], [11] describes an approximate version of the circuit, which, for any value
9


---

## Page 10

1
2
3
5
13
8
5
3
2
1
∗
p
p
∗
p
p
∗
p
p
p
↔
(6, 5)
Figure 10: Here we make a correspondence between strings of p and ∗symbols and ordered pairs of integers. The
string of 9 symbols is split into substrings of length 4 and 5, and each one is used to compute an integer by adding
the (i + 1)th Fibonacci number if ∗appears in the ith place. Note the two strings are read in diﬀerent directions.
of parameter m, uses a total of only O(mn log n) gates1 to produce an output having an inner product with
|x + a mod 2n⟩of 1 −O(2−m).
Because they operate modulo 2n, Draper’s quantum circuits for addition and subtraction do not imme-
diately yield fast ancilla-free quantum circuits for comparison, unlike the classical case. Instead, start with
an n-bit number x and then introduce a single clean ancilla qubit initialized to |0⟩. Then subtract an n-bit
hardcoded number a from this register modulo 2n+1. If a > x then the result will wrap around into the
range [2n, 2n+1 −1], in which case the leading bit will be 1. If a ≤x then the result will be in the range
[0, 2n −1]. After copying the result of this leading qubit and uncomputing the subtraction, the comparison
is complete. Alternatively, one could use the linear size quantum comparison circuit devised by Takahashi
and Kunihiro, which uses n uninitialized ancillas but no clean ancillas[28].
Unfortunately, most crossings in a given braid will not be acting on the leftmost strand. However, we
can reduce the problem of extracting a general symbol to the problem of extracting the leftmost symbol.
Rather than using equation 7 to make a correspondence between a string from Pn and a single integer,
we can split the string at some chosen point, and use equation 7 on each piece to make a correspondence
between elements of Pn and ordered pairs of integers, as shown in ﬁgure 10. To extract the ith symbol, we
thus convert encoding 7 to the encoding where the string is split between the ith and (i −1)th symbols, so
that one only needs to extract the leftmost symbol of the second string. Like equation 7, this is also an
eﬃcient encoding, in which the encoded bitstrings form a large fraction of all possible bitstrings.
To convert encoding 7 to a split encoding with the split at an arbitrary point, we can move the split
rightward by one symbol at a time. To introduce a split between the leftmost and second-to-leftmost symbols,
one must extract the leftmost symbol as described above. To move the split one symbol to the right, one
must extract the leftmost symbol from the right string, and if it is ∗then add the corresponding Fibonacci
number to the left string. This is again a procedure of addition, subtraction, and comparison of integers.
Note that the computation of Fibonacci numbers in NC1 is not necessary, as these can be hardcoded into
the circuits. Moving the split back to the left works analogously. As crossings of diﬀerent pairs of strands
are being simulated, the split is moved to the place that it is needed. At the end it is moved all the way
leftward and eliminated, leaving a superposition of bitstrings in the original encoding, which have the correct
coeﬃcients determined by the Fibonacci representation of the given braid.
Lastly, we must consider the weighting in the trace, as described by equation 10. Instead of weight Ws,
we will use Ws/φ so that the possible weights are 1 and 1/φ both of which are ≤1. We can impose any
weight ≤1 by doing a controlled rotation on an extra qubit. The CNOT trick for simulating a clean qubit
which was described in section 1 can be viewed as a special case of this. All strings in which that qubit takes
the value |1⟩have weight zero, as imposed by a π/2 rotation on the extra qubit. Because none of the weights
are smaller than 1/φ, the weighting will cause only a constant overhead in the number of measurements
needed to get a given precision.
5
DQC1-hardness of Jones Polynomials
We will prove DQC1-hardness of the problem of estimating the Jones polynomial of the trace closure of a
braid by a reduction from the problem of estimating the trace of a quantum circuit. To do this, we will
specify an encoding, that is, a map η : Qn →Sm from the set Qn of strings of p and ∗symbols which
1A linear-size quantum circuit for exact ancilla-free addition is known, but it does not generalize easily to the case of
hardcoded summands [9].
10


---

## Page 11

start with ∗and have no two ∗symbols in a row, to Sm, the set of bitstrings of length m. For a given
quantum circuit, we will construct a braid whose Fibonacci representation implements the corresponding
unitary transformation on the encoded bits. The Jones polynomial of the trace closure of this braid, which
is the trace of this representation, will equal the trace of the encoded quantum circuit.
Unlike in section 4, we will not use a one to one encoding between bit strings and strings of p and ∗
symbols. All we require is that a sum over all strings of p and ∗symbols corresponds to a sum over bitstrings
in which each bitstring appears an equal number of times. Equivalently, all bitstrings b ∈Sm must have a
preimage η−1(b) of the same size. This insures an unbiased trace in which no bitstrings are overweighted.
To achieve this we can divide the symbol string into blocks of three symbols and use the encoding
ppp
→
0
p∗p
→
1
(8)
The strings other than ppp and p∗p do not correspond to any bit value. Since both the encoded 1 and the
encoded 0 begin and end with p, they can be preceded and followed by any allowable string. Thus, changing
an encoded 1 to an encoded zero does not change the number of allowed strings of p and ∗consistent with
that encoded bitstring. Thus the condition that |η−1(b)| be independent of b is satisﬁed.
We would also like to know a priori where in the string of p and ∗symbols a given bit is encoded. This
way, when we need to simulate a gate acting on a given bit, we would know which strands the corresponding
braid should act on. If we were to simply divide our string of symbols into blocks of three and write down
the corresponding bit string (skipping every block which is not in one of the two coding states ppp and p∗p)
then this would not be the case. Thus, to encode n bits, we will instead divide the string of symbols into
n superblocks, each consisting of c log n blocks of three for some constant c. To decode a superblock, scan
it from left to right until you reach either a ppp block or a p∗p block. The ﬁrst such block encountered
determines whether the superblock encodes a 1 or a 0, according to equation 8. Now imagine we choose a
string randomly from Q3cn log n. By choosing the constant prefactor c in our superblock size we can ensure
that in the entire string of 3cn log n symbols, the probability of there being any noncoding superblock which
contains neither a ppp block nor a p∗p block is polynomially small. If this is the case, then these noncoding
strings will contribute only a polynomially small additive error to the estimate of the circuit trace, on par
with the other sources of error.
The gate set consisting of the CNOT, Hadamard, and π/8 gates is known to be universal for BQP [23].
Thus, it suﬃces to consider the simulation of 1-qubit and 2-qubit gates. Furthermore, it is suﬃcient to
imagine the qubits arranged on a line and to allow 2-qubit gates to act only on neighboring qubits. This
is because qubits can always be brought into neighboring positions by applying a series of SWAP gates to
nearest neighbors. By our encoding a unitary gate applied to qubits i and i + 1 will correspond to a unitary
transformation on symbols i3c log n through (i + 2)3c log n −1. The essence of our reduction is to take each
quantum gate and represent it by a corresponding braid on logarithmically many symbols whose Fibonacci
representation performs that gate on the encoded qubits.
Let’s ﬁrst consider the problem of simulating a gate on the ﬁrst pair of qubits, which are encoded in
the leftmost two superblocks of the symbol string. We’ll subsequently consider the more diﬃcult case of
operating on an arbitrary pair of neighboring encoded qubits. As mentioned in section 3, the Fibonacci
representation ρ(n)
F
is reducible. Let ρ(n)
∗∗denote the representation of the braid group Bn deﬁned by the
action of ρ(n)
F
on the vector space spanned by strings which begin and end with ∗. As shown in appendix
B, ρ(n)
∗∗(Bn) taken modulo phase is a dense subgroup of SU(fn−1), and ρ(n)
∗p (Bn) modulo phase is a dense
subgroup of SU(fn).
In addition to being dense, the ∗∗and ∗p blocks of the Fibonacci representation can be controlled
independently. This is a consequence of the decoupling lemma, as discussed in appendix B. Thus, given
a string of symbols beginning with ∗, and any desired pair of unitaries on the corresponding ∗p and ∗∗
vector spaces, a braid can be constructed whose Fibonacci representation approximates these unitaries to
any desired level of precision. However, the number of crossings necessary may in general be large. The
space spanned by strings of logarithmically many symbols has only polynomial dimension. Thus, one might
guess that the braid needed to approximate a given pair of unitaries on the ∗p and ∗∗vector spaces for
11


---

## Page 12

Figure 11: This sequence of unitary steps is used to bring a ∗symbol where it is needed in the symbol string to
ensure density of the braid group representation. The presence of the left ∗ensures density to allow the movement
of the right ∗by proposition 1. Similarly, the presence of the right ∗allows the left ∗to be moved.
logarithmically many symbols will have only polynomially many crossings. It turns out that this guess is
correct, as we state formally below.
Proposition 1. Given any pair of elements U∗p ∈SU(fk+1) and U∗∗∈SU(fk), and any real parameter ǫ,
one can in polynomial time ﬁnd a braid b ∈Bk with poly(n, log(1/ǫ)) crossings whose Fibonacci representa-
tion satisﬁes ∥ρ∗p(b) −U∗p∥≤ǫ and ∥ρ∗∗(b) −U∗∗∥≤ǫ, provided that k = O(log n). By symmetry, the same
holds when considering ρp∗rather than ρ∗p.
Note that proposition 1 is a property of the Fibonacci representation, not a generic consequence of
density, since it is in principle possible for the images of group generators in a dense representation to lie
exponentially close to some subgroup of the corresponding unitary group. We prove this proposition in
appendix D.
With proposition 1 in hand, it is apparent that any unitary gate on the ﬁrst two encoded bits can be
eﬃciently performed. To similarly simulate gates on arbitrary pairs of neighboring encoded qubits, we will
need some way to unitarily bring a ∗symbol to a known location within logarithmic distance of the relevant
encoded qubits. This way, we ensure that we are acting in the ∗p or ∗∗subspaces.
To move ∗symbols to known locations we’ll use an “inchworm” structure which brings a pair of ∗symbols
rightward to where they are needed. Speciﬁcally, suppose we have a pair of superblocks which each have a
∗in their exact center. The presence of the left ∗and the density of ρ∗p allow us to use proposition 1 to
unitarily move the right ∗one superblock to the right by adding polynomially many crossings to the braid.
Then, the presence of the right ∗and the density of ρp∗allow us to similarly move the left ∗one superblock
to the right, thus bringing it into the superblock adjacent to the one which contains the right ∗. This is
illustrated in ﬁgure 11. To move the inchworm to the left we use the inverse operation.
To simulate a given gate, one ﬁrst uses the previously described procedure to make the inchworm crawl
to the superblocks just to the left of the superblocks which encode the qubits on which the gate acts. Then,
by the density of ρ∗p and proposition 1, the desired gate can be simulated using polynomially many braid
crossings.
To get this process started, the leftmost two superblocks must each contain a ∗at their center. This occurs
with constant probability. The strings in which this is not the case can be prevented from contributing to
the trace by a technique analogous to that used in section 1 to simulate logarithmically many clean ancillas.
Namely, an extra encoded qubit can be conditionally ﬂipped if the ﬁrst two superblocks do not both have
∗symbols at their center. This can always be done using proposition 1, since the leftmost symbol in the
string is always ∗, and the ρ∗p and ρ∗∗representations are both dense.
12


---

## Page 13

p
p
p p
p p
*
p * p *
*
*
p
* p
p *
swap
Figure 12: This unitary procedure starts with a ∗in the current superblock and brings it to the center of the target
superblock.
It remains to specify the exact unitary operations which move the inchworm. Suppose we have a current
superblock and a target superblock.
The current superblock contains a ∗in its center, and the target
superblock is the next superblock to the right or left. We wish to move the ∗to the center of the target
superblock. To do this, we can select the smallest segment around the center such that in each of these
superblocks, the segment is bordered on its left and right by p symbols. This segment can then be swapped,
as shown in ﬁgure 12.
For some possible strings this procedure will not be well deﬁned. Speciﬁcally there may not be any
segment which contains the center and which is bordered by p symbols in both superblocks.
On such
strings we deﬁne the operation to act as the identity. For random strings, the probability of this decreases
exponentially with the superblock size. Thus, by choosing c suﬃciently large we can make this negligible for
the entire computation.
As the inchworm moves rightward, it leaves behind a trail. Due to the swapping, the superblocks are not
in their original state after the inchworm has passed. However, because the operations are unitary, when the
inchworm moves back to the left, the modiﬁcations to the superblocks get undone. Thus the inchworm can
shuttle back and forth, moving where it is needed to simulate each gate, always stopping just to the left of
the superblocks corresponding to the encoded qubits.
The only remaining detail to consider is that the trace appearing in the Jones polynomial is weighted
depending on whether the last symbol is p or ∗, whereas the DQC1-complete trace estimation problem is
for completely unweighted traces. This problem is easily solved. Just introduce a single extra superblock at
the end of the string. After bringing the inchworm adjacent to the last superblock, apply a unitary which
performs a conditional rotation on the qubit encoded by this superblock. The rotation will be by an angle
so that the inner product of the rotated qubit with its original state is 1/φ where φ is the golden ratio. This
will be done only if the last symbol is p. This exactly cancels out the weighting which appears in the formula
for the Jones polynomial, as described in appendix A.
Thus, for appropriate ǫ, approximating the Jones polynomial of the trace closure of a braid to within ±ǫ
is DQC1-hard.
6
Conclusion
The preceding sections show that the problem of approximating the Jones polynomial of the trace closure of a
braid with n strands and m crossings to within ±ǫ at t = ei2π/5 is a DQC1-complete problem for appropriate
ǫ. The proofs are based on the problem of evaluating the Markov trace of the Fibonacci representation
of a braid to
1
poly(n,m) precision. By equation 11, we see that this corresponds to evaluating the Jones
polynomial with ±
|Dn−1|
poly(n,m) precision, where D = −A2 −A−2 = 2 cos(6π/5). Whereas approximating the
Jones polynomial of the plat closure of a braid was known[1] to be BQP-complete, it was previously only
known that the problem of approximating the Jones polynomial of the trace closure of a braid was in BQP.
Understanding the complexity of approximating the Jones polynomial of the trace closure of a braid to
precision ±
|Dn−1|
poly(n,m) was posed as an open problem in [3]. This paper shows that for A = e−i3π/5, this
problem is DQC1-complete. Such a completeness result improves our understanding of both the diﬃculty of
the Jones polynomial problem and the power one clean qubit computers by ﬁnding an equivalence between
13


---

## Page 14

the two.
It is generally believed that DQC1 is not contained in P and does not contain all of BQP. The DQC1-
completeness result shows that if this belief is true, it implies that approximating the Jones polynomial of
the trace closure of a braid is not so easy that it can be done classically in polynomial time, but is not so
diﬃcult as to be BQP-hard.
To our knowledge, the problem of approximating the Jones polynomial of the trace closure of a braid is
one of only four known candidates for classically intractable problems solvable on a one clean qubit computer.
The others are estimating the Pauli decomposition of the unitary matrix corresponding to a polynomial-size
quantum circuit2, [21, 27], estimating quadratically signed weight enumerators[22], and estimating average
ﬁdelity decay of quantum maps[25, 26].
7
Acknowledgements
The authors thank David Vogan, Pavel Etingof, Raymond Laﬂamme, Pawel Wocjan, Sergei Bravyi, Wim
van Dam, Aram Harrow, and Daniel Nagaj for useful discussions, and an anonymous reviewer for helpful
comments. PS gratefully acknowledges support from the W. M. Keck foundation and from the NSF under
grant number CCF-0431787. SJ gratefully acknowledges support from ARO/DTO’s QuaCGR program and
the use of MIT Center for Theoretical Physics facilities as supported by the US Department of Energy. Part
of this work was completed while SJ was a short term visitor at Perimeter Institute.
A
Jones Polynomials by Fibonacci Representation
For any braid b ∈Bn we will deﬁne f
Tr(b) by:
f
Tr(b) =
1
φfn + fn−1
X
s∈Qn+1
Ws
s
s
b
(9)
We will use | to denote a strand and ∤to denote multiple strands of a braid (in this case n). Qn+1 is the
set of all strings of n + 1 p and ∗symbols which start with ∗and contain no two ∗symbols in a row. The
symbol
s
s
b
denotes the s, s matrix element of the Fibonacci representation of braid b. The weight Ws is
Ws =

φ
if s ends with p
1
if s ends with ∗.
(10)
φ is the golden ratio (1 +
√
5)/
√
2.
As discussed in [3], the Jones polynomial of the trace closure of a braid b is given by
Vbtr(A−4) = (−A)3w(btr)Dn−1Tr(ρA(btr)).
(11)
btr is the link obtained by taking the trace closure of braid b. w(btr) is denotes the writhe of the link btr. For
an oriented link, one assigns a value of +1 to each crossing of the form
, and the value −1 to each crossing
of the form
. The writhe of a link is deﬁned to be the sum of these values over all crossings. D is deﬁned
2This includes estimating the trace of the unitary as a special case.
14


---

## Page 15

by D = −A2 −A−2. ρA : Bn →TLn(D) is a representation from the braid group to the Temperley-Lieb
algebra with parameter D. Speciﬁcally,
ρA(σi) = AEi + A−11
(12)
where E1 . . . En are the generators of TLn(D), which satisfy the following relations.
EiEj
=
EjEi
for |i −j| > 1
(13)
EiEi±1Ei
=
Ei
(14)
E2
i
=
DEi
(15)
The Markov trace on TLn(D) is a linear map Tr : TLn(D) →C which satisﬁes
Tr(1)
=
1
(16)
Tr(XY )
=
Tr(Y X)
(17)
Tr(XEn−1)
=
1
DTr(X′)
(18)
On the left hand side of equation 18, the trace is on TLn(D), and X is an element of TLn(D) not containing
En−1. On the right hand side of equation 18, the trace is on TLn−1(D), and X′ is the element of TLn−1(D)
which corresponds to X in the obvious way since X does not contain En−1.
We’ll show that the Fibonacci representation satisﬁes the properties implied by equations 12, 13, 14, and
15. We’ll also show that f
Tr on the Fibonacci representation satisﬁes the properties corresponding to 16, 17,
and 18. It was shown in [3] that properties 16, 17, and 18, along with linearity, uniquely determine the map
Tr. It will thus follow that f
Tr(ρ(n)
F (b)) = Tr(ρA(b)), which proves that the Jones polynomial is obtained from
the trace f
Tr of the Fibonacci representation after multiplying by the appropriate powers of D and (−A) as
shown in equation 11. Since these powers are trivial to compute, the problem of approximating the Jones
polynomial at A = e−i3π/5 reduces to the problem of computing this trace.
f
Tr is equal to the ordinary matrix trace on the subspace of strings ending in ∗plus φ times the matrix
trace on the subspace of strings ending in p.
Thus the fact that the matrix trace satisﬁes property 17
immediately implies that f
Tr does too. Furthermore, since the dimensions of these subspaces are fn−1 and
fn respectively, we see from equation 9 that f
Tr(1) = 1. To address property 18, we’ll ﬁrst show that
f
Tr




b



= 1
δ
f
Tr



b



(19)
for some constant δ which we will calculate. We will then use equation 12 to relate δ to D.
Using the deﬁnition of f
Tr we obtain
f
Tr




b




=
1
fnφ + fn−1

φ
X
s∈Qn−2
*
p
s p
*
p
s p
b
+ φ
X
s∈Qn−2
p
s p
p
p
s p
p
b
+
X
s∈Qn−2
s p
p *
s p
p *
b
+
X
s∈Q′
n−2
s
p
*
*
s
p
*
*
b
+ φ
X
s∈Q′
n−2
s
p
*
p
s
p
*
p
b


where Q′
n−2 is the set of length n −2 strings of ∗and p symbols which begin with ∗, end with p, and have
no two ∗symbols in a row.
15


---

## Page 16

Next we expand according to the braiding rules described in equations 3 and 4.
=
1
fnφ + fn−1


X
s∈Qn−2




φc
*
p
s p
*
p
s p
b
+ φe
p
s p
p
p
s p
p
b
+ a
s p
p *
s p
p *
b





+
X
s∈Q′
n−2




b
s
p
*
*
s
p
*
*
b
+ φa
s
p
*
p
s
p
*
p
b







We know that matrix elements in which diﬀering string symbols are separated by unbraided strands will be
zero. To obtain the preceding expression we have omitted such terms. Simplifying yields
=
1
fn + φfn−1


X
s∈Qn−2




φc
b
*
s p
*
s p
+ (φe + a)
b
s p
p
s p
p




+
X
s∈Q′
n−2
(b + φa)
b
s
p
*
s
p
*

.
By the deﬁnitions of A, a, b, and e, given in equation 5, we see that φe + a = b + φa. Thus the above
expression simpliﬁes to
=
1
fnφ + fn−1


X
s∈Q′
n−1
φc
s*
s*
b
+
X
s∈Qn−1
(φe + a)
b
sp
sp


Now we just need to show that
φc
fnφ + fn−1
= 1
δ
1
fn−1φ + fn−2
(20)
and
φe + a
fnφ + fn−1
= 1
δ
φ
fn−1φ + fn−2
.
(21)
The Fibonacci numbers have the property
fnφ + fn−1
fn−1φ + fn−2
= φ
for all n. Thus equations 20 and 21 are equivalent to
φc = 1
δ φ
(22)
and
φe + a = 1
δ φ2
(23)
respectively. For A = e−i3π/5 these both yield δ = A −1. Hence
f
Tr




b



= 1
δ
1
fn−1φ + fn−2


X
s∈Q′
n−1
s*
s*
b
+
X
s∈Qn−1
φ
b
sp
sp


16


---

## Page 17

= 1
δ
f
Tr(b),
thus conﬁrming equation 19.
Now we calculate D from δ. Solving 12 for Ei yields
Ei = A−1ρA(σi) −A−21
(24)
Substituting this into 18 yields
Tr(X(A−1ρA(σi) −A−21)) = 1
DTr(X)
⇒A−1Tr(XρA(σi)) −A−2Tr(X) = 1
DTr(X).
Comparison to our relation Tr(XρA(σi)) = 1
δ Tr(X) yields
A−1 1
δ −A−2 = 1
D.
Solving for D and substituting in A = e−i3π/5 yields
D = φ.
This is also equal to −A2 −A−2 consistent with the usage elsewhere.
Thus we have shown that f
Tr has all the necessary properties. We will next show that the image of the
representation ρF of the braid group Bn also forms a representation of the Temperley-Lieb algebra T Ln(D).
Speciﬁcally, Ei is represented by
Ei →A−1ρ(n)
F (σi) −A−21.
(25)
To show that this is a representation of T Ln(D) we must show that the matrices described in equation
25 satisfy the properties 13, 14, and 15. By the theorem of [3] which shows that a Markov trace on any
representation of the Temperley-Lieb algebra yields the Jones polynomial, it will follow that the trace of the
Fibonacci representation yields the Jones polynomial.
Since ρF is a representation of the braid group and σiσj = σjσi for |i−j| > 1, it immediately follows that
the matrices described in equation 25 satisfy condition 13. Next, we’ll consider condition 15. By inspection
of the Fibonacci representation as given by equation 4, we see that by appropriately ordering the basis3 we
can bring ρA(σi) into block diagonal form, where each block is one of the following 1×1 or 2×2 possibilities.
[a]
[b]
 c
d
d
e

Thus, by equation 25, it suﬃces to show that

A−1

c
d
d
e

−A−2

1
0
0
1
2
= D

A−1

c
d
d
e

−A−2

1
0
0
1

,
(A−1a −A−2)2 = D(A−1a −A−2),
and
(A−1b −A−2)2 = D(A−1b −A−2),
i.e. each of the blocks square to D times themselves. These properties are conﬁrmed by direct calculation.
3We will have to choose diﬀerent orderings for diﬀerent σi’s.
17


---

## Page 18

Now all that remains is to check that the correspondence 25 satisﬁes property 14.
Using the rules
described in equation 4 we have
ρ(3)
F (σ1) =


b
0
0
a
a
e
0
d
0
a
0
d
0
c
e
d
d
c


∗p∗p
∗ppp
∗pp∗
pppp
pp∗p
p∗pp
ppp∗
p∗p∗
ρ(3)
F (σ2) =


c
d
d
e
a
e
d
0
d
c
0
0
0
a
a
0
0
b


∗p∗p
∗ppp
∗pp∗
pppp
pp∗p
p∗pp
ppp∗
p∗p∗
(Here we have considered all four subspaces unlike in equation 6.) Substituting this into equation 25 yields
matrices which satisfy condition 15. It follows that equation 25 yields a representation of the Temperley-Lieb
algebra. This completes the proof that
Vbtr(A−4) = (−A)3w(btr)Dn−1f
Tr(ρ(n)
F (btr))
for A = e−i3π/5.
B
Density of the Fibonacci representation
In this appendix we will show that ρ(n)
∗∗(Bn) is a dense subgroup of SU(fn−1) modulo phase, and that
ρ(n)
∗p (Bn) and ρ(n)
p∗(Bn) are dense subgroups of SU(fn) modulo phase. Similar results regarding the path
model representation of the braid group were proven in [1]. Our proofs will use many of the techniques
introduced there.
We’ll ﬁrst show that ρ(4)
∗∗(B4) modulo phase is a dense subgroup of SU(2). We can then use the bridge
lemma from [1] to extend the result to arbitrary n.
Proposition 2. ρ(4)
∗∗(B4) modulo phase is a dense subgroup of SU(2).
Proof: Using equation 4 we have:
ρ(4)
∗∗(σ1) = ρ(4)
∗∗(σ3) =

b
0
0
a

∗p∗p∗
∗ppp∗
ρ(4)
∗∗(σ2) =

c
d
d
e

∗p∗p∗
∗ppp∗
We do not care about global phase so we will take
ρ(n)
∗∗(σi)
→
1

det ρ(n)
∗∗(σi)
1/fn−1 ρ(n)
∗∗(σi)
to project into SU(fn−1). Thus we must show the group ⟨A, B⟩generated by
A =
1
√
ab
 b
0
0
a

B =
1
√
ce −d2
 c
d
d
e

(26)
is a dense subgroup of SU(2). To do this we will use the well known surjective homomorphism φ : SU(2) →
SO(3) whose kernel is {±1} (cf. [5], pg. 276). A general element of SU(2) can be written as
cos
θ
2

1 + i sin
θ
2

[xσx + yσy + zσz]
18


---

## Page 19

where σx, σy, σz are the Pauli matrices, and x, y, z are real numbers satisfying x2 + y2 + z2 = 1. φ maps
this element to the rotation by angle θ about the axis
⃗x =


x
y
z

.
Using equations 26 and 5, one ﬁnds that φ(A) and φ(B) are both rotations by 7π/5. These rotations are
about diﬀerent axes which are separated by angle
θ12 = cos−1(2 −
√
5) ≃1.8091137886 . . .
To show that ρ(4)
∗∗(B4) modulo phase is a dense subgroup of SU(2) it suﬃces to show that φ(A) and φ(B)
generate a dense subgroup of SO(3). To do this we take advantage of the fact that the ﬁnite subgroups of
SO(3) are completely known.
Theorem 1. ([5] pg. 184) Every ﬁnite subgroup of SO(3) is one of the following:
Ck: the cyclic group of order k
Dk: the dihedral group of order k
T : the tetrahedral group (order 12)
O: the octahedral group (order 24)
I: the icosahedral group (order 60)
The inﬁnite proper subgroups of SO(3) are all isomorphic to O(2) or SO(2). Thus, since φ(A) and φ(B)
are rotations about diﬀerent axes, ⟨φ(A), φ(B)⟩can only be SO(3) or a ﬁnite subgroup of SO(3). If we can
show that ⟨φ(A), φ(B)⟩is not contained in any of the ﬁnite subgroups of SO(3) then we are done.
Since φ(A) and φ(B) are rotations about diﬀerent axes we know that ⟨φ(A), φ(B)⟩is not Ck or Dk. Next,
we note that R = φ(A)5φ(B)5 is a rotation by 2θ12. By direct calculation, 2θ12 is not an integer multiple of
2π/k for k = 1, 2, 3, 4, or 5. Thus R has order greater than 5. As mentioned on pg. 262 of [17], T , O, and I
do not have any elements of order greater than 5. Thus, ⟨φ(A), φ(B)⟩is not contained in C, O, or I, which
completes the proof. Alternatively, using more arithmetic and less group theory, we can see that 2θ12 is not
any integer multiple of 2π/k for any k ≤30, thus R cannot be in T , O, or I since its order does not divide
the order of any of these groups. □
Next we’ll consider ρ(n)
∗∗for larger n. These will be matrices acting on the strings of length n + 1. These
can be divided into those which end in pp∗and those which end in ∗p∗. The space upon which ρ(n)
∗∗acts
can correspondingly be divided into two subspaces which are the span of these two sets of strings. From
equation 4 we can see that ρ(n)
∗∗(σ1) . . . ρ(n)
∗∗(σn−3) will leave these subspaces invariant. Thus if we order
our basis to respect this grouping of strings, ρ(n)
∗∗(σ1) . . . ρ(n)
∗∗(σn−3) will appear block-diagonal with a block
corresponding to each of these subspaces.
The possible preﬁxes of ∗p∗are all strings of length n−2 that start with ∗and end with p. Now consider
the strings acted upon by ρ(n−2)
∗∗
. These have length n −1 and must end in ∗. The possible preﬁxes of this ∗
are all strings of length n−2 that begin with ∗and end with p. Thus these are in one to one correspondence
with the strings acted upon by ρ(n)
∗∗that end in ∗p∗. Furthermore, since the rules 4 depend only on the three
symbols neighboring a given crossing, the block of ρ(n)
∗∗(σ1) . . . ρ(n)
∗∗(σn−3) corresponding to the ∗p∗subspace
is exactly the same as ρ(n−2)
∗∗
(σ1) . . . ρ(n−2)
∗∗
(σn−3). By a similar argument, the block of ρ(n)
∗∗(σ1) . . . ρ(n)
∗∗(σn−3)
corresponding to the pp∗is exactly the same as ρ(n−1)
∗∗
(σ1) . . . ρ(n−1)
∗∗
(σn−3).
For any n > 3, ρ(n)
∗∗(σn−2) will not leave these subspaces invariant. This is because the crossing σn−2
spans the (n −1)th symbol. Thus if the (n −2)th and nth symbols are p, then by equation 4, ρ(n)
∗∗can ﬂip
19


---

## Page 20

the value of the (n −1)th symbol. The nth symbol is guaranteed to be p, since the (n + 1)th symbol is the
last one and is therefore ∗by deﬁnition. For any n > 3, the space acted upon by ρ(n)
∗∗(σn−1) will include
some strings in which the (n −2)th symbol is p.
As an example, for ﬁve strands:
ρ(5)
∗∗(σ1) =


b
0
0
0
a
0
0
0
a


∗p∗pp∗
∗pppp∗
∗pp∗p∗
ρ(5)
∗∗(σ2) =


c
d
0
d
e
0
0
0
a


∗p∗pp∗
∗pppp∗
∗pp∗p∗
ρ(5)
∗∗(σ3) =


a
0
0
0
e
d
0
d
c


∗p∗pp∗
∗pppp∗
∗pp∗p∗
ρ(5)
∗∗(σ4) =


a
0
0
0
a
0
0
0
b


∗p∗pp∗
∗pppp∗
∗pp∗p∗
We recognize the upper 2×2 blocks of ρ(5)
∗∗(σ1), and ρ(5)
∗∗(σ2) from equation 6. The lower 1×1 block matches
ρ(3)
∗∗(σ1) and ρ(3)
∗∗(σ2), which are both easily calculated to be [a]. ρ(5)
∗∗(σ3) mixes these two subspaces.
We can now use the preceding observations about the recursive structure of {ρ(n)
∗∗|n = 4, 5, 6, 7 . . .} to
show inductively that ρ(n)
∗∗(Bn) forms a dense subgroup of SU(fn−1) for all n. To perform the induction step
we use the bridge lemma and decoupling lemma from [1].
Lemma 1 (Bridge Lemma). Let C = A ⊕B where A and B are vector spaces with dim B > dim A ≥1. Let
W ∈SU(C) be a linear transformation which mixes the subspaces A and B. Then the group generated by
SU(A), SU(B), and W is dense in SU(C).
Lemma 2 (Decoupling Lemma). Let G be an inﬁnite discrete group, and let A and B be two vector spaces
with dim(A) ̸= dim(B). Let ρa : G →SU(A) and ρb : G →SU(B) be homomorphisms such that ρa(G) is
dense in SU(A) and ρb(G) is dense in SU(B). Then for any Ua ∈SU(A) there exist a series of G-elements
αn such that limn→∞ρa(αn) = Ua and limn→∞ρb(αn) = 1. Similarly, for any Ub ∈SU(B), there exists a
series βn ∈G such that limn→∞ρa(βn) = 1 and limn→∞ρa(βn) = Ub.
With these in hand we can prove the main proposition of this appendix.
Proposition 3. For any n ≥3, ρ(n)
∗∗(Bn) modulo phase is a dense subgroup of SU(fn−1).
Proof: As mentioned previously, the proof will be inductive. The base cases are n = 3 and n = 4. As
mentioned previously, ρ(3)
∗∗(σ1) = ρ(3)
∗∗(σ2) = [a]. Trivially, these generate a dense subgroup of (indeed, all
of) SU(1) = {1} modulo phase. By proposition 2, ρ(4)
∗∗(σ1), and ρ(4)
∗∗(σ2) generate a dense subgroup of
SU(2) modulo phase. Now for induction assume that ρ(n−1)
∗∗
(Bn−1) is a dense subgroup of SU(fn−2) and
ρ(n−2)
∗∗
(Bn−2) is a dense subgroup of SU(fn−3). As noted above, these correspond to the upper and lower
blocks of ρ(n)
∗∗(σ1) . . . ρ(n)
∗∗(σn−2). Thus, by the decoupling lemma, ρ(n)
∗∗(Bn) contains an element arbitrarily
close to U ⊕1 for any U ∈SU(fn−2) and an element arbitrarily close to 1⊕U for any U ∈SU(fn−3). Since,
as observed above, ρ(n)
∗∗(σn−1) mixes these two subspaces, the bridge lemma shows that ρ(n)
∗∗(Bn) is dense in
SU(fn−1). □
From this, the density of ρ(n)
∗p and ρ(n)
p∗easily follow.
Corollary 1. ρ(n)
∗p (Bn) and ρ(n)
p∗(Bn) are dense subgroups of SU(fn) modulo phase.
Proof: It is not hard to see that
ρ(n)
∗p (σ1)
=
ρ(n+1)
∗∗
(σ1)
...
ρ(n)
∗p (σn−1)
=
ρ(n+1)
∗∗
(σn−1)
.
20


---

## Page 21

As we saw in the proof of proposition 3, ρ(n+1)
∗∗
(σn) is not necessary to obtain density in SU(fn), that
is, ⟨ρ(n+1)
∗∗
(σ1), . . . , ρ(n+1)
∗∗
(σn−1)⟩is a dense subgroup of SU(fn) modulo phase. Thus, the density of ρ(n)
∗p
in SU(fn) follows immediately from the proof of proposition 3. By symmetry, ρ(n)
p∗(Bn) is isomorphic to
ρ(n)
∗p (Bn), thus this is a dense subgroup of SU(fn) modulo phase as well. □
C
Fibonacci and Path Model Representations
For any braid group Bn, and any root of unity ei2π/k, the path model representation is a homomorphism
from Bn to to a set of linear operators. The vector space that these linear operators act is the space of
formal linear combinations of n step paths on the rungs of a ladder of height k −1 that start on the bottom
rung. As an example, all the paths for n = 4, k = 5 are shown in below.
Thus, the n = 4, k = 5 path model representation is on a ﬁve dimensional vector space. For k = 5 we
can make a bijective correspondence between the allowed paths of n steps and the set of strings of p and ∗
symbols of length n + 1 which start with ∗and have no to ∗symbols in a row. To do this, simply label the
rungs from top to bottom as ∗, p, p, ∗, and directly read oﬀthe symbol string for each path as shown below.
p
p
*
*
p
p
*
*
p
p
*
*
p
p
*
*
p
p
*
*
* p * p *
* p p p *
* p p *p
* p *p p
* p p p p
In [3], it is explained in detail for any given braid how to calculate the corresponding linear transformation
on paths. Using the correspondence described above, one ﬁnds that the path model representation for k = 5
is equal to the −1 times Fibonacci representation described in this paper. This sign diﬀerence is a minor
detail which arises only because [3] chooses a diﬀerent fourth root of t for A than we do. This sign diﬀerence
is automatically compensated for in the factor of (−A)3·writhe, so that both methods yield the correct Jones
polynomial.
D
Unitaries on Logarithmically Many Strands
In this appendix we’ll prove the following proposition.
Proposition 1. Given any pair of elements U∗p ∈SU(fk+1) and U∗∗∈SU(fk), and any real parameter ǫ,
one can in polynomial time ﬁnd a braid b ∈Bk with poly(n, log(1/ǫ)) crossings whose Fibonacci representa-
tion satisﬁes ∥ρ∗p(b) −U∗p∥≤ǫ and ∥ρ∗∗(b) −U∗∗∥≤ǫ, provided that k = O(log n). By symmetry, the same
holds when considering ρp∗rather than ρ∗p.
To do so, we’ll use a recursive construction. Suppose that we already know how to achieve proposition 1
on n symbols, and we wish to extend this to n + 1 symbols. Using the construction for n symbols we can
eﬃciently obtain a unitary of the form
Mn−1(A, B) =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
A
A
B
(27)
21


---

## Page 22

where A and B are arbitrary unitaries of the appropriate dimension. The elementary crossing σn on the last
two strands has the representation4
Mn =


b
a
a
e
d
d
c


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
As a special case of equation 27, we can obtain
Mdiag(α) =


eiα/2
eiα/2
eiα/2
eiα/2
e−iα/2


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
Where 0 ≤α < 2π. We’ll now show the following.
Lemma 3. For any element

V11
V12
V21
V22

∈SU(2),
one can ﬁnd some product P of O(1) Mdiag matrices and Mn matrices such that for some phases φ1 and φ2,
P =


φ1
φ2
φ2
V11
V12
V21
V22


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
Proof: Let Bdiag(α) and Bn be the following 2 × 2 matrices
Bdiag(α) =
 eiα/2
0
0
e−iα/2

and
Bn =
 e
d
d
c

We wish to show that we can approximate an arbitrary element of SU(2) as a product of O(1) Bdiag and Bn
matrices. To do this, we will use the well known homomorphism φ : SU(2) →SO(3) whose kernel is {±1}
(see appendix B). To obtain an arbitrary element V of SU(2) modulo phase it suﬃces to show that the we
can use φ(Bn) and φ(Bdiag(α)) to obtain an arbitrary SO(3) rotation. In appendix B we showed that

a
0
0
b

and

e
d
d
c

correspond to two rotations of 7π/5 about axes which are separated by an angle of θ12 ≃1.8091137886 . . .
By the deﬁnition of φ, φ(Bdiag(α)) is a rotation by angle α about the same axis that φ
 a
0
0
b

rotates
about. φ(B5
n) is a π rotation. Hence, R(α) ≡φ(B5
nBdiag(α)B5
n) is a rotation by angle α about an axis which
is separated by angle5 2θ12 −π from the axis that φ(Bdiag(α)) rotates about. Q ≡R(π)φ(Bdiag(α))R(π) is a
rotation by angle α about some axis whose angle of separation from the axis that φ(Bdiag(α)) rotates about
is 2(2θ12 −π) ≃0.9532. Similarly, by geometric visualization, φ(Bdiag(α′))Qφ(Bdiag(−α′)) is a rotation by α
4Here and throughout this appendix when we write a scalar α in a block of the matrix we really mean αI where I is the
identity operator of appropriate dimension.
5We subtract π because the angle between axes of rotation is only deﬁned modulo π. Our convention is that these angles
are in [0, π).
22


---

## Page 23

about an axis whose angle of separation from the axis that Q rotates about is anywhere from 0 to 2×0.9532
depending on the value of α′. Since 2 × 0.9532 > π/2, there exists some choice of α′ such that this angle of
separation is π/2. Thus, using the rotations we have constructed we can perform Euler rotations to obtain
an arbitrary rotation. □
As a special case of lemma 3, we can obtain, up to global phase,
Mswap =


φ1
φ2
φ2
0
1
1
0


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
Similarly, we can produce M −1
swap. Using Mswap, M −1
swap, and equation 27 we can produce the matrix
MC =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
I
I
C
for any unitary C. We do it as follows. Since C is a normal operator, it can be unitarily diagonalized. That
is, there exists some unitary U such that UCU −1 = D for some diagonal unitary D. Next, note that in
equation 27 the dimension of B is more than half that of A. Let d = dim(A) −dim(B), and let Id be the
identity operator of dimension d. We can easily construct two diagonal unitaries D1 and D2 of dimension
dim(B) such that (D1 ⊕Id)(Id ⊕D2) = D. As special cases of equation 27 we can obtain
MD1 =


1
1
1
1
D1


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
and
MD2 =


1
1
1
1
D2


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
and
MP =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
P
P
I
where P is a permutation matrix that shifts the lowest dim(B) basis states from the bottom of the block to
the top of the block. Thus we obtain
M2 ≡MswapMD2M −1
swap =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
I
I
Id ⊕D2
23


---

## Page 24

and
M1 ≡MP MswapMD1M −1
swapM −1
P
=




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
I
I
D1 ⊕Id
.
Thus
M1M2 =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
I
D
I
.
As a special case of equation 27 we can obtain
MU =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
I
U
U
.
Thus we obtain MC by the construction MC = MUM1M2M −1
U . By multiplying together MC and Mn−1 we
can control the three blocks independently. For arbitrary unitaries A, B, C of appropriate dimension we can
obtain
MACB =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
A
C
B
.
(28)
As a special case of equation 28 we can obtain
Munphase =


φ∗
1
φ∗
2
φ∗
2
1
1


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
Thus, we obtain a clean swap
Mclean = MunphaseMswap =


1
1
1
0
1
1
0


∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
.
(29)
We’ll now use Mclean and MACB as our building blocks to create the maximally general unitary
Mgen(V, W) =




∗. . . ∗p∗
∗. . . pp∗
∗. . . ∗pp
∗. . . ppp
∗. . . p∗p
V
W
.
(30)
24


---

## Page 25

For n + 1 symbols, the ∗. . . ∗pp subspace has dimension fn−3, and the ∗. . . p ∗p and ∗. . . ppp subspaces
each have dimension fn−2. Thus, in equation 28, the block C has dimension fn−2 + fn−3 = fn−1, and the
block B has dimension fn−2. To construct Mgen(V, W) we will choose a subset of the fn basis states acted
upon by the B and C blocks and permute them into the C block. Then using MACB, we’ll perform an
arbitrary unitary on these basis states. At each such step we can act upon a subspace whose dimension is a
constant fraction of the dimension of the entire fn dimensional space on which we wish to apply an arbitrary
unitary. Furthermore, this constant fraction is more than half. Speciﬁcally, fn/fn−1 ≃1/φ ≃0.62 for large
n. We’ll show that an arbitrary unitary can be built up as a product of a constant number of unitaries each
of which act only on half the basis states. Thus our ability to act on approximately 62% of the basis states
at each step is more than suﬃcient.
Before proving this, we’ll show how to permute an arbitrary set of basis states into the C block of MACB.
Just use Mclean to swap the B block into the ∗. . . ppp subspace of the C block. Then, as a special case of
equation 28, choose A and B to be the identity, and C to be a permutation which swaps some states between
the ∗. . .∗pp and ∗. . . ppp subspaces of the C block. The states which we swap up from the ∗. . . ppp subspace
are the ones from B which we wish to move into C. The ones which we swap down from the ∗. . . ∗pp
subspace are the ones from C which we wish to move into B. This process allows us to swap a maximum
of fn−3 states between the B block and the C block. Since fn−3 is more than half the dimension of the B
block, it follows that any desired permutation of states between the B and C blocks can be achieved using
two repetitions of this process.
We’ll now show the following.
Lemma 4. Let m by divisible by 4. Any m × m unitary can be obtained as a product of seven unitaries,
each of which act only on the space spanned by m/2 of the basis states, and leave the rest of the basis states
undisturbed.
It will be obvious from the proof that even if the dimension of the matrix is not divisible by four, and
the fraction of the basis states on which the individual unitaries act is not exactly 1/2 it will still be possible
to obtain an arbitrary unitary using a constant number of steps independent of m. Therefore, we will not
explicitly work out this straightforward generalization.
Proof: In [23] it is shown that for any unitary U, one can always ﬁnd a series of unitaries Ln, . . . , L1 which
each act on only two basis states such that Ln . . . L1U is the identity. Thus Ln . . . L1 = U −1. It follows that
any unitary can be obtained as a product of such two level unitaries. The individual matrices L1, . . . , Ln
each perform a (unitary) row operation on U. The sequence Ln . . . L1 reduces U to the identity by a method
very similar to Gaussian elimination. We will use a very similar construction to prove the present lemma.
The essential diﬀerence is that we must perform the two level unitaries in groups. That is, we choose some
set of m/2 basis states, perform a series of two level unitaries on them, then choose another set of m/2 basis
states, perform a series of two level unitaries on them, and so on. After a ﬁnite number of such steps (it
turns out that seven will suﬃce) we will reduce U to the identity.
Our two-level unitaries will all be of the same type. We’ll ﬁx our attention on two entries in U taken
from a particular column: Uik and Ujk. We wish to perform a unitary row operation, i.e. left multiply by a
two level unitary, to set Ujk = 0. If Uik and Ujk are not both zero, then the two-level unitary which acts on
the rows i and j according to
1
p
|Uik|2 + |Ujk|2
 U ∗
ik
U ∗
jk
Ujk
−Uik

(31)
will achieve this. If Uik and Ujk are both zero there is nothing to be done.
We can now use this two level operation within groups of basis states to eliminate matrix elements of U
one by one. As in Gaussian elimination, the key is that once you’ve obtained some zero matrix elements,
your subsequent row operations must be chosen so that they do not make these nonzero again, undoing your
previous work.
As the ﬁrst step, we’ll act on the top m/2 rows in order to reduce the upper-left quadrant of U to upper
triangular form. We can do this as follows. Consider the ﬁrst and second entries in the ﬁrst column. Using
the operation 31 we can make the second entry zero. Next consider the ﬁrst and third entries in the ﬁrst
25


---

## Page 26

column. By operation 31 we can similarly make the third entry zero. Repeating this procedure, we get all
of the entries in the top half of the ﬁrst column to be zero other than the top entry. Next, we perform the
same procedure on the second column except leaving out the top row. These row operations will not alter
the ﬁrst column since the rows being acted upon all have zero in the ﬁrst column. We can then repeat this
procedure for each column in the left half of U until the upper-left block is upper triangular.
We’ll now think of U in terms of 16 blocks of size (m/4) × (m/4). In the second step we’ll eliminate the
matrix elements in the third block of the ﬁrst column. The second step is shown schematically as
{
{
The curly braces indicate the rows to be acted upon, and the unshaded areas represent zero matrix elements.
This step can be performed very similarly to the ﬁrst step. The nonzero matrix elements in the bottom part
of the ﬁrst column can be eliminated one by one by interacting with the ﬁrst row. The nonzero matrix
elements in the bottom part of the second column can then be eliminated one by one by interacting with
the second row. The ﬁrst column will be undisturbed by this because the rows being acted upon in this step
have zero matrix elements in the ﬁrst column. Similarly acting on the remaining columns yields the desired
result.
The next step, as shown below, is nearly identical and can be done the same way.
{
{
(32)
The matrix on the right hand side of 32 is unitary. It follows that it must be of the form
where the upper-leftmost block is a diagonal unitary. We can next apply the same sorts of steps to the lower
3 × 3 blocks, as illustrated below.
{
{
{
{
By unitarity the resulting matrix is actually of the form
where the lower-right quadrant is an (m/2) × (m/2) unitary matrix, and the upper-left quadrant is an
(m/2) × (m/2) diagonal unitary matrix. We can now apply the inverse of the upper-left quadrant to the top
26


---

## Page 27

m/2 rows and then apply the inverse of the lower-right quadrant to the bottom m/2 rows. This results in
the identity matrix, and we are done. In total we have used seven steps. □
Examining the preceding construction, we can see the recursive step uses a constant number of the Mn−1
operators from the next lower level of recursion, plus a constant number of Mn operators. Thus, the number
of crossings in the braid grows only exponentially in the recursion depth. Since each recursion adds one more
symbol, we see that to construct Mgen(V, W) on logarithmically many symbols requires only polynomially
many crossings in the corresponding braid.
The main remaining task is to work out the base case on which the recursion rests. Since the base case is
for a ﬁxed set of generators on a ﬁxed number of symbols, we can simply use the Solovay-Kitaev theorem[20].
Theorem 2 (Solovay-Kitaev). Suppose matrices U1, . . . , Ur generate a dense subgroup in SU(d). Then,
given a desired unitary U ∈SU(d), and a precision parameter δ > 0, there is an algorithm to ﬁnd a product
V of U1, . . . , Ur and their inverses such that ∥V −U∥≤δ. The length of the product and the runtime of the
algorithm are both polynomial in log(1/δ).
Because the total complexity of the process is polynomial, it is only necessary to implement the base case
to polynomially small δ in order for the ﬁnal unitary Mgen(V, W) to have polynomial precision. This follows
from simple error propagation. An analogous statement about the precision of gates needed in quantum
circuits is worked out in [23]. This completes the proof of proposition 1.
E
Zeckendorf Representation
Following [19], to construct the Fibonacci representation of the braid group, we use strings of p and ∗symbols
such that no two ∗symbols are adjacent. There exists a bijection z between such strings and the integers,
known as the Zeckendorf representation. Let Pn be the set of all such strings of length n. To construct the
map z : Pn →{0, 1, . . ., fn+2} we think of ∗as one and p as zero. Then, for a given string s = snsn−1 . . . s1
we associate the integer
z(s) =
n
X
i=1
sifi+1,
(33)
where fi is the ith Fibonacci number: f1 = 1, f2 = 1, f3 = 2, and so on. In this appendix we’ll show the
following.
Proposition 4. For any n, the map z : Pn →{0, . . ., fn+2} deﬁned by z(s) = Pn
i=1 sifi+1 is bijective.
Proof: We’ll inductively show that the following two statements are true for every n ≥2.
An :
z maps strings of length n starting with p bijectively to {0, . . ., fn+1 −1}.
Bn :
z maps strings of length n starting with ∗bijectively to {fn+1, . . . , fn+2 −1}.
Together, An and Bn imply that z maps Pn bijectively to {0, . . ., fn+2 −1}.
As a base case, we can
look at n = 2.
pp
↔
0
p∗
↔
1
∗p
↔
2
Thus A2 and B2 are true. Now for the induction. Let sn−1 ∈Pn−1. By equation 33,
z(psn−1) = z(sn−1).
27


---

## Page 28

Since sn−1 follows a p symbol, it can be any element of Pn−1. By induction, z is bijective on Pn−1, thus An
is true. Similarly, by equation 33
z(∗sn−1) = fn+1 + z(sn−1).
Since sn−1 here follows a ∗, its allowed values are exactly those strings which start with p. By induction,
An−1 tells us that z maps these bijectively to {0, . . ., fn −1}. Since fn+1 + fn = fn+2, this implies Bn is
true. Together, An and Bn for all n ≥2, along with the trivial n = 1 case, imply proposition 4. □
References
[1] Dorit Aharonov and Itai Arad.
The BQP-hardness of approximating the Jones polynomial.
2006.
arXiv:quant-ph/0605181.
[2] Dorit Aharonov, Itai Arad, Elad Eban, and Zeph Landau. Polynomial quantum algorithms for additive
approximations of the Potts model and other points of the Tutte plane. arXiv:quant-ph/0702008, 2007.
[3] Dorit Aharonov, Vaughan Jones, and Zeph Landau. A polynomial quantum algorithm for approximating
the Jones polynomial. STOC 06, 2006. arXiv:quant-ph/0511096.
[4] Andris Ambainis, Leonard Schulman, and Umesh Vazirani. Computing with highly mixed states. Jour-
nal of the ACM, 53(3):507–531, May 2006. arXiv:quant-ph/0003136.
[5] Michael Artin. Algebra. Prentice Hall, 1991.
[6] Adriano Barenco, Artur Ekert, Kalle-Antti Suominen, and P¨aivi T¨orm¨a. Approximate quantum Fourier
transform and decoherence. Phyical Review A, 54(1):139–146, 1996. arXiv:quant-ph/9601018.
[7] David A. Barrington. Bounded-width polynomial-size brancing programs recognize exactly those lan-
guages in NC1. Journal of Computer and System Sciences, 38:150–164, 1989.
[8] D. Coppersmith. An approximate fourier transform useful in quantum factoring. Technical report, IBM,
1994. arXiv:quant-ph/0201067.
[9] Steven A. Cuccaro, Thomas G. Draper, Samuel A. Kutin, and David Petrie Moulton. A new quantum
ripple-carry addition circuit. arXiv:quant-ph/0410184, 2004.
[10] Animesh Datta, Steven T. Flammia, and Carlton M. Caves. Entanglement and the power of one qubit.
Physical Review A, 72(042316), 2005. arXiv:quant-ph/0505213.
[11] Thomas Draper. Addition on a quantum computer. arXiv:quant-ph/0008033, 2000.
[12] Michael Freedman, Alexei Kitaev, and Zhenghan Wang. Simulation of topological ﬁeld theories by
quantum computers. Communications in Mathematical Physics, 227:587–603, 2002.
[13] Michael Freedman, Michael Larsen, and Zhenghan Wang. A modular functor which is universal for
quantum computation. 2000. arXiv:quant-ph/0001108.
[14] W. Haken. Theorie der normalﬂachen, ein isotopiekriterium f¨ur den kreisknoten. Acta Mathematica,
(105):245–375, 1961.
[15] Joel Hass, Jeﬀrey Lagarias, and Nicholas Pippenger. The computational complexity of knot and link
problems. Journal of the ACM, 46(2):185–211, 1999. arXiv:math.GT/9807016.
[16] F. Jaeger, D. L. Vertigan, and D. J. A. Welsh. On the computational complexity of the Jones and Tutte
polynomials. Mathematical Proceedings of the Cambridge Philosophical Society, (108):35–53, 1990.
[17] Vaughan F. R. Jones. Braid groups, Hecke algebras and type II1 factors. In Geometric methods in
operator algebras, US-Japan Seminar, pages 242–273, Kyoto, July 1983.
28


---

## Page 29

[18] Vaughan F. R. Jones. A polynomial invariant for knots via von Neumann algebras. Bulletin of the
American Mathematical Society, 12:103–111, 1985.
[19] Louis H. Kauﬀman and Samuel J. Lomonaco Jr. q-deformed spin networks knot polynomials and anyonic
topological quantum computation. arXiv:quant-ph/0606114, 2006.
[20] Alexei Yu. Kitaev. Quantum computations: algorithms and error correction. Russian Mathematical
Surveys, 52(6):1191–1249, 1997.
[21] E. Knill and R. Laﬂamme.
Power of one bit of quantum information.
Physical Review Letters,
81(25):5672–5675, 1998. arXiv:quant-ph/9802037.
[22] E. Knill and R. Laﬂamme. Quantum computating and quadratically signed weight enumerators. Infor-
mation Processing Letters, 79(4):173–179, 2001. arXiv:quant-ph/9909094.
[23] Michael A. Nielsen and Isaac L. Chuang. Quantum Computation and Quantum Information. Cambridge
University Press, 2000.
[24] Christos Papadimitriou. Computational Complexity. Addison Wesley, 1994.
[25] David Poulin, Robin Blume-Kohout, Raymond Laﬂamme, and Harold Ollivier. Exponential speedup
with a single bit of quantum information: Measuring the average ﬁdelity decay. Physical Review Letters,
92(17):177906, 2004. arXiv:quant-ph/0310038.
[26] C. A. Ryan, J. Emerson, D. Poulin, C. Negrevergne, and R. Laﬂamme. Characterization of complex
quantum dynamics with a scalable NMR information processor. Physical Review Letters, 95:250502,
2005. arXiv:quant-ph/0506085.
[27] Dan Shepherd. Computation with unitaries and one pure qubit. 2006. arXiv:quant-ph/0608132.
[28] Yasuhiro Takahashi and Noburu Kunihiro. A quantum circuit for Shor’s factoring algorithm using 2n+2
qubits. Quantum Information and Computation, 6(2):184–192, 2006.
[29] Ingo Wegener. The Complexity of Boolean Functions. Wiley, 1987.
[30] Edward Witten. Quantum ﬁeld theory and the Jones polynomial. Communications in Mathematical
Physics, 121(3):351–399, 1989.
[31] Pawel Wocjan and Jon Yard. The Jones polynomial: quantum algorithms and applications in quantum
complexity theory. arXiv:quant-ph/0603069, 2006.
29


---

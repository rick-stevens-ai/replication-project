# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:quant-ph/0406180 — Julia Kempe, Alexei Kitaev, Oded Regev,
# 'The Complexity of the Local Hamiltonian Problem' (2004; v2 2005-10-02)
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

arXiv:quant-ph/0406180v2  2 Oct 2005
The Complexity of the Local Hamiltonian Problem
Julia Kempe
CNRS & LRI, Universit´e de Paris-Sud,
91405 Orsay, France, and
UC Berkeley, Berkeley, CA94720
Alexei Kitaev
Departments of Physics and Computer Science,
California Institute of Technology,
Pasadena, CA 91125
Oded Regev
Department of Computer Science,
Tel-Aviv University,
Tel-Aviv 69978, Israel
November 26, 2024
Abstract
The k-LOCAL HAMILTONIAN problem is a natural complete problem for the complexity
class QMA, the quantum analog of NP. It is similar in spirit to MAX-k-SAT, which is NP-
complete for k ≥2. It was known that the problem is QMA-complete for any k ≥3. On
the other hand 1-LOCAL HAMILTONIAN is in P, and hence not believed to be QMA-complete.
The complexity of the 2-LOCAL HAMILTONIAN problem has long been outstanding. Here we
settle the question and show that it is QMA-complete. We provide two independent proofs; our
ﬁrst proof uses only elementary linear algebra. Our second proof uses a powerful technique
for analyzing the sum of two Hamiltonians; this technique is based on perturbation theory
and we believe that it might prove useful elsewhere. Using our techniques we also show that
adiabatic computation with two-local interactions on qubits is equivalent to standard quantum
computation.
1
Introduction
Quantum complexity theory has emerged alongside the ﬁrst efﬁcient quantum algorithms in an
attempt to formalize the notion of an efﬁcient algorithm. In analogy to classical complexity theory,
several new quantum complexity classes have appeared. A major challenge today consists in
understanding their structure and the interrelation between classical and quantum classes.
One of the most important classical complexity classes is NP - nondeterministic polynomial
time. This class comprises languages that can be veriﬁed in polynomial time by a deterministic
veriﬁer. The celebrated Cook-Levin theorem (see, e.g., [Pap94]) shows that this class has complete
problems. More formally, it states that SAT is NP-complete, i.e., it is in NP and any other lan-
guage in NP can be reduced to it with polynomial overhead. In SAT we are given a set of clauses
(disjunctions) over n variables and asked whether there is an assignment that satisﬁes all clauses.
One can consider the restriction of SAT in which each clause consists of at most k literals. This
is known as the k-SAT problem. It is known that 3-SAT is still NP-complete while 2-SAT is in P,
1

---- page 2 ----

i.e., has a polynomial time solution. We can also consider the MAX-k-SAT problem: here, given a
k-SAT formula and a number m we are asked whether there exists an assignment that satisﬁes at
least m clauses. It turns out that MAX-2-SAT is already NP-complete; MAX-1-SAT is clearly in P.
The class QMA is the quantum analogue of NP in a probabilistic setting, i.e., the class of all
languages that can be probabilistically veriﬁed by a quantum veriﬁer in polynomial time (the
name is derived from the classical class MA, which is the randomized analogue of NP). This class,
which is also called BQNP, was ﬁrst studied in [Kni96, KSV02]; the name QMA was given to it
by Watrous [Wat00]. Several problems in QMA have been identiﬁed [Wat00, KSV02, JWB03]. For
a good introduction to the class QMA, see the book by Kitaev et al. [KSV02] and the paper by
Watrous [Wat00].
Kitaev, inspired by ideas due to Feynman, deﬁned the quantum analogue of the classical SAT
problem, the LOCAL HAMILTONIAN problem [KSV02].1 An instance of k-LOCAL HAMILTONIAN
can be viewed as a set of local constraints on n qubits, each involving at most k of them. We are
asked whether there is a state of the n qubits such that the expected number of violated constraints
is either below a certain threshold or above another, with a promise that one of the two cases holds
and both thresholds are at least a constant apart. More formally, we are to determine whether the
groundstate energy of a given k-local Hamiltonian is below one threshold or above another.
Kitaev proved [KSV02] that the 5-LOCAL HAMILTONIAN problem is QMA-complete. Later,
Kempe and Regev showed that already 3-LOCAL HAMILTONIAN is complete for QMA [KR03]. In
addition, it is easy to see that 1-LOCAL HAMILTONIAN is in P. The complexity of the 2-LOCAL
HAMILTONIAN problem was left as an open question in [AN02, WB03, KR03, BV05]. It is not hard
to see that the k-LOCAL HAMILTONIAN problem contains the MAX-K-SAT problem as a special
case.2 Using the known NP-completeness of MAX-2-SAT, we obtain that 2-LOCAL HAMILTONIAN
is NP-hard, i.e., any problem in NP can be reduced to it with polynomial overhead. But is it
also QMA-complete? Or perhaps it lies in some intermediate class between NP and QMA? Some
special cases of the problem were considered by Bravyi and Vyalyi [BV05]; however, the question
still remained open.
In this paper we settle the question of the complexity of 2-LOCAL HAMILTONIAN and show
Theorem 1 The 2-LOCAL HAMILTONIAN problem is QMA-complete.
In [KSV02] it was shown that the k-LOCAL HAMILTONIAN problem is in QMA for any constant
k (and in fact even for k = O(log n) where n is the total number of qubits). Hence, our task in
this paper is to show that any problem in QMA can be reduced to the 2-LOCAL HAMILTONIAN
problem with a polynomial overhead. We give two self-contained proofs for this.
Our ﬁrst proof is based on a careful selection of gates in a quantum circuit and several appli-
cations of a lemma called the projection lemma. The proof is quite involved; however, it uses only
elementary linear algebra and hence might appeal to some readers.
Our second proof is based on perturbation theory – a collection of techniques that are used
to analyze sums of Hamiltonians. This proof is more mathematically involved. Nevertheless,
1For a good survey of the LOCAL HAMILTONIAN problem see [AN02].
2The idea is to represent the n variables by n qubits and represent each clause by a Hamiltonian. Each Hamiltonian
is diagonal and acts on the k variables that appear in its clause. It ‘penalizes’ the assignment that violates the clause
by increasing its eigenvalue. Therefore, the lowest eigenvalue of the sum of the Hamiltonians corresponds to the
maximum number of clauses that can be satisﬁed simultaneously.
2

---- page 3 ----

it might give more intuition as to why the 2-LOCAL HAMILTONIAN problem is QMA-complete.
Unlike the ﬁrst proof which shows how to represent any QMA circuit by a 2-local Hamiltonian,
the second proof shows a reduction from the 3-LOCAL HAMILTONIAN problem (which is already
known to be QMA-complete [KR03]) to the 2-LOCAL HAMILTONIAN problem. To the best of our
knowledge, this is the ﬁrst reduction inside QMA (i.e., not from the circuit problem). This proof
involves what is known as third order perturbation theory (interestingly, the projection lemma used
in our ﬁrst proof can be viewed as an instance of ﬁrst order perturbation theory). We are not aware
of any similar application of perturbation theory in the literature and we hope that our techniques
will be useful elsewhere.
Adiabatic computation:
It has been shown in [AvK+04] that the model of adiabatic computation
with 3-local interactions is equivalent to the standard model of quantum computation (i.e., the
quantum circuit model).3 We strengthen this result by showing that 2-local interactions sufﬁce.4
Namely, the model of adiabatic computation with 2-local interactions is equivalent to the standard
model of quantum computation. We obtain this result by applying the technique of perturbation
theory, which we develop in the second proof of the main theorem.
Recent work:
After a preliminary version of our paper has appeared [KKR04], Oliveira and
Terhal [OT05] have generalized our results and have shown that the 2-LOCAL HAMILTONIAN
problem remains QMA-complete even if the Hamiltonians are restricted to nearest neighbor inter-
actions between qubits on a 2-dimensional grid. Similarly, they show that the model of adiabatic
computation with 2-local Hamiltonians between nearest neighbor qubits on a 2-dimensional grid
is equivalent to standard quantum computation. Their proof applies the perturbation theory tech-
niques that we develop in this paper and introduces several novel “perturbation gadgets” akin to
our three-qubit gadget in Section 6.2.
Structure:
We start by describing our notation and some basics in Section 2. Our ﬁrst proof
is developed in Sections 3, 4 and 5. The main tool in this proof, which we name the projection
lemma, appears in Section 3. Using this lemma, we rederive in Section 4 some of the previously
known results. Then we give the ﬁrst proof of our main theorem in Section 5. In Section 6 we give
the second proof of our main theorem. This proof does not require the projection lemma and is in
fact independent of the ﬁrst proof. Hence, some readers might choose to skip Sections 3, 4 and 5
and go directly to Section 6. In Section 7 we show how to use our techniques to prove that 2-local
adiabatic computation is equivalent to standard quantum computation. Some open questions are
mentioned in Section 8.
3 Interestingly, their proof uses ideas from the proof of QMA-completeness of the LOCAL HAMILTONIAN problem.
4The main result of [AvK+04] is that 2-local adiabatic computation on six-dimensional particles is equivalent to stan-
dard quantum computation. This result is incomparable to ours since their particles are set on a two-dimensional grid
and all two-local interactions are between closest neighbors.
3

---- page 4 ----

2
Preliminaries
QMA is naturally deﬁned as a class of promise problems: A promise problem L is a pair (Lyes, Lno)
of disjoint sets of strings corresponding to YES and NO instances of the problem. The problem is
to determine, given a string x ∈Lyes ∪Lno, whether x ∈Lyes or x ∈Lno. Let B be the Hilbert
space of a qubit.
Deﬁnition 1 (QMA) Fix ε = ε(|x|) such that ε = 2−Ω(|x|). Then, a promise problem L is in QMA if there
exists a quantum polynomial time veriﬁer V and a polynomial p such that:
- ∀x ∈Lyes
∃|ξ⟩∈B⊗p(|x|)
Pr (V (|x⟩, |ξ⟩) = 1) ≥1 −ε
- ∀x ∈Lno
∀|ξ⟩∈B⊗p(|x|)
Pr (V (|x⟩, |ξ⟩) = 1) ≤ε
where Pr (V (|x⟩, |ξ⟩) = 1) denotes the probability that V outputs 1 given |x⟩and |ξ⟩.
We note that in the original deﬁnition ε was deﬁned to be 2−Ω(|x|) ≤ε ≤1/3. By using ampliﬁca-
tion methods, it was shown in [KSV02] that for any choice of ε in this range the resulting classes
are equivalent. Hence our deﬁnition is equivalent to the original one. In a related result, Marriott
and Watrous [MW04] showed that exponentially small ε can be achieved without ampliﬁcation
with a polynomial overhead in the veriﬁer’s computation.
A natural choice for the quantum analogue of SAT is the LOCAL HAMILTONIAN problem. As
we will see later, this problem is indeed a complete problem for QMA.
Deﬁnition 2 We say that an operator H : B⊗n →B⊗n on n qubits is a k-local Hamiltonian if H is
expressible as H = Pr
j=1 Hj where each term is a Hermitian operator acting on at most k qubits.
Deﬁnition 3 The (promise) problem k-LOCAL HAMILTONIAN is deﬁned as follows. We are given a k-
local Hamiltonian on n-qubits H = Pr
j=1 Hj with r = poly(n). Each Hj has a bounded operator norm
∥Hj∥≤poly(n) and its entries are speciﬁed by poly(n) bits. In addition, we are given two constants a
and b with a < b. In YES instances, the smallest eigenvalue of H is at most a. In NO instances, it is larger
than b. We should decide which one is the case.
We will frequently refer to the lowest eigenvalue of some Hamiltonian H.
Deﬁnition 4 Let λ(H) denote the lowest eigenvalue of the Hamiltonian H.
Another important notion that will be used in this paper is that of a restriction of a Hamiltonian.
Deﬁnition 5 Let H be a Hamiltonian and let Π be a projection on some subspace S. Then we say that the
Hamiltonian ΠHΠ on S is the restriction of H to S. We denote this restriction by H|S.
3
Projection Lemma
Our main technical tool is the projection lemma. This lemma (in a slightly different form) was
already used in [KR03] and [AvK+04] but not as extensively as it is used in this paper (in fact, we
apply it four times in the ﬁrst proof of our main theorem). The lemma allows us to successively
4

---- page 5 ----

cut out parts of the Hilbert space by giving them a large penalty. More precisely, assume we work
in some Hilbert space H and let H1 be some Hamiltonian. For some subspace S ⊆H, let H2 be
a Hamiltonian with the property that S is an eigenspace of eigenvalue 0 and S⊥has eigenvalues
at least J for some large J ≫∥H1∥. In other words, H2 gives a very high penalty to states in S⊥.
Now consider the Hamiltonian H = H1 + H2. The projection lemma says that λ(H), the lowest
eigenvalue of H, is very close to λ(H1|S), the lowest eigenvalue of the restriction of H1 to S. The
intuitive reason for this is the following. By adding H2 we give a very high penalty to any vector
that has even a small projection in the S⊥direction. Hence, all eigenvectors with low eigenvalue
(and in particular the one corresponding to λ(H)) have to lie very close to S. From this it follows
that these eigenvectors correspond to the eigenvectors of H1|S.
The strength of this lemma comes from the following fact. Even though H1 and H2 are lo-
cal Hamiltonians, H1|S is not necessarily so. In other words, the projection lemma allows us to
approximate a non-local Hamiltonian by a local Hamiltonian.
Lemma 1 Let H = H1+H2 be the sum of two Hamiltonians operating on some Hilbert space H = S+S⊥.
The Hamiltonian H2 is such that S is a zero eigenspace and the eigenvectors in S⊥have eigenvalue at least
J > 2∥H1∥. Then,
λ(H1|S) −
∥H1∥2
J −2∥H1∥≤λ(H) ≤λ(H1|S).
Notice that with, say, J ≥8∥H1∥2 + 2∥H1∥= poly(∥H1∥) we have λ(H1|S) −1/8 ≤λ(H) ≤
λ(H1|S).
Proof: First, we show that λ(H) ≤λ(H1|S). Let |η⟩∈S be the eigenvector of H1|S corresponding
to λ(H1|S). Using H2|η⟩= 0,
⟨η|H|η⟩= ⟨η|H1|η⟩+ ⟨η|H2|η⟩= λ(H1|S)
and hence H must have an eigenvector of eigenvalue at most λ(H1|S).
We now show the lower bound on λ(H). We can write any unit vector |v⟩∈H as |v⟩=
α1|v1⟩+ α2|v2⟩where |v1⟩∈S and |v2⟩∈S⊥are two unit vectors, α1, α2 ∈R, α1, α2 ≥0 and
α2
1 + α2
2 = 1. Let K = ∥H1∥. Then we have,
⟨v|H|v⟩
≥
⟨v|H1|v⟩+ Jα2
2
=
(1 −α2
2)⟨v1|H1|v1⟩+ 2α1α2Re⟨v1|H1|v2⟩+ α2
2⟨v2|H1|v2⟩+ Jα2
2
≥
⟨v1|H1|v1⟩−Kα2
2 −2Kα2 −Kα2
2 + Jα2
2
=
⟨v1|H1|v1⟩+ (J −2K)α2
2 −2Kα2
≥
λ(H1|S) + (J −2K)α2
2 −2Kα2
where we used α2
1 = 1−α2
2 and α1 ≤1. Since (J−2K)α2
2−2Kα2 is minimized for α2 = K/(J−2K),
we have
⟨v|H|v⟩≥λ(H1|S) −
K2
J −2K .
5

---- page 6 ----

4
Kitaev’s Construction
In this section we reprove Kitaev’s result that O(log n)-LOCAL HAMILTONIAN is QMA-complete.
The difference between our version of the proof and the original one in [KSV02] is that we do not
use their geometrical lemma to obtain the result, but rather apply our Lemma 1. This paves the
way to the later proof that 2-LOCAL HAMILTONIAN is QMA-complete.
As mentioned before, the proof that O(log n)-LOCAL HAMILTONIAN is in QMA appears in
[KSV02]. Hence, our goal is to show that any problem in QMA can be reduced to O(log n)-LOCAL
HAMILTONIAN. Let Vx = V (|x⟩, ·) = UT · · · U1 be a quantum veriﬁer circuit of size T = poly(|x|)
operating on N = poly(|x|) qubits.5 Here and in what follows later we assume without loss of
generality that each Ui is either a one-qubit gate or a two-qubit gate. We further assume that
T ≥N and that initially, the ﬁrst m = p(|x|) qubits contain the proof and the remaining ancillary
N −m qubits are zero (see Deﬁnition 1). Finally, we assume that the output of the circuit is written
into the ﬁrst qubit (i.e., it is |1⟩if the circuit accepts). See Figure 1.
|0⟩
|0⟩
0
1
2
9
3
4
5
6
7
8
1
10
11
Figure 1: A circuit with T = 11, N = 4 and m = 2.
The constructed Hamiltonian H operates on a space of n = N + log(T + 1) qubits. The ﬁrst
N qubits represent the computation and the last log(T + 1) qubits represent the possible values
0, . . . , T for the clock:
H = Hout + JinHin + JpropHprop.
The coefﬁcients Jin and Jprop will be chosen later to be some large polynomials in N. The terms
are given by
Hin =
N
X
i=m+1
|1⟩⟨1|i ⊗|0⟩⟨0|
Hout = (T + 1)|0⟩⟨0|1 ⊗|T⟩⟨T|
Hprop =
T
X
t=1
Hprop,t
(1)
and
Hprop,t = 1
2

I ⊗|t⟩⟨t| + I ⊗|t-1⟩⟨t-1| −Ut ⊗|t⟩⟨t-1| −U†
t ⊗|t-1⟩⟨t|

(2)
for 1 ≤t ≤T where |α⟩⟨α|i denotes the projection on the subspace in which the i’th qubit is
|α⟩. It is understood that the ﬁrst part of each tensor product acts on the space of the N compu-
tation qubits and the second part acts on the clock qubits. Ut and U†
t in Hprop,t act on the same
computational qubits as Ut does when it is employed in the veriﬁer’s circuit Vx. Intuitively, each
5For ease of notation we hardwire the dependence on the input x into the circuit.
6

---- page 7 ----

Hamiltonian ‘checks’ a certain property by increasing the eigenvalue if the property doesn’t hold:
The Hamiltonian Hin checks that the input of the circuit is correct (i.e., none of the last N −m
computation qubits is 1), Hout checks that the output bit indicates acceptance and Hprop checks
that the propagation is according to the circuit. Notice that these Hamiltonians are O(log n)-local
since there are log(T + 1) = O(log n) clock qubits.
To show that a problem in QMA reduces to the O(log n)-LOCAL HAMILTONIAN problem with
H chosen as above, we prove the following lemma.
Lemma 2 If the circuit Vx accepts with probability more than 1−ε on some input |ξ, 0⟩, then the Hamilto-
nian H has an eigenvalue smaller than ε. If the circuit Vx accepts with probability less than ε on all inputs
|ξ, 0⟩, then all eigenvalues of H are larger than 3
4 −ε.
Proof: Assume the circuit Vx accepts with probability more than 1 −ε on some |ξ, 0⟩. Deﬁne
|η⟩=
1
√
T + 1
T
X
t=0
Ut · · · U1|ξ, 0⟩⊗|t⟩.
It can be seen that ⟨η|Hprop|η⟩= ⟨η|Hin|η⟩= 0 and that ⟨η|Hout|η⟩< ε. Hence, the smallest
eigenvalue of H is less than ε. It remains to prove the second part of the lemma. So now assume
the circuit Vx accepts with probability less than ε on all inputs |ξ, 0⟩.
Let Sprop be the groundspace of the Hamiltonian Hprop. It is easy to see that Sprop is a 2N-
dimensional space whose basis is given by the states
|ηi⟩=
1
√
T + 1
T
X
t=0
Ut · · · U1|i⟩⊗|t⟩
(3)
where i ∈{0, . . . , 2N −1} and |i⟩represents the ith vector in the computational basis on the
N computation qubits. These states have eigenvalue 0. The states in Sprop represent the correct
propagation from an initial state on the N computation qubits according to the veriﬁer’s circuit
Vx.
We would like to apply Lemma 1 with the space Sprop. For that, we need to establish that
JpropHprop gives a sufﬁciently large (poly(N)) penalty to states in S⊥
prop. In other words, the small-
est non-zero eigenvalue of Hprop has to be lower bounded by some inverse polynomial in N. This
has been shown in [KSV02], but we wish to brieﬂy recall it here, as it will apply in several instances
throughout this paper.
Claim 2 ([KSV02]) The smallest non-zero eigenvalue of Hprop is at least c/T 2 for some constant c > 0.
Proof: We ﬁrst apply the change of basis
W =
T
X
t=0
Ut · · · U1 ⊗|t⟩⟨t|
which transforms Hprop to
W †HpropW =
T
X
t=1
I ⊗1
2 (|t⟩⟨t| + |t-1⟩⟨t-1| −|t⟩⟨t-1| −|t-1⟩⟨t|) .
7

---- page 8 ----

The eigenspectrum of Hprop is unchanged by this transformation. The resulting Hamiltonian is
block-diagonal with 2N blocks of size T + 1.
W †HpropW
=
I ⊗















1
2
−1
2
0
· · ·
0
−1
2
1
−1
2
0
...
...
0
−1
2
1
−1
2
0
...
...
...
...
...
...
...
...
0
−1
2
1
−1
2
0
0
−1
2
1
−1
2
0
· · ·
0
−1
2
1
2















.
(4)
Using standard techniques, one can show that the smallest non-zero eigenvalue of each (T + 1) ×
(T + 1) block matrix is bounded from below by c/T 2, for some constant c > 0.
Hence any eigenvector of JpropHprop orthogonal to Sprop has eigenvalue at least J = cJprop/T 2.
Let us apply Lemma 1 with
H1 = Hout + JinHin
H2 = JpropHprop.
Note that ∥H1∥≤∥Hout∥+ Jin∥Hin∥≤T + 1 + JinN ≤poly(N) since Hin and Hout are sums of
orthogonal projectors and Jin = poly(N). Lemma 1 implies that we can choose Jprop = JT 2/c =
poly(N), such that λ(H) is lower bounded by λ(H1|Sprop) −1
8. With this in mind, let us now
consider the Hamiltonian H1|Sprop on Sprop.
Let Sin ⊂Sprop be the groundspace of Hin|Sprop. Then Sin is a 2m-dimensional space whose
basis is given by states as in Eq. (3) with |i⟩= |j, 0⟩, where |j⟩is a computational basis state on the
ﬁrst m computation qubits. We apply Lemma 1 again inside Sprop with
H1 = Hout|Sprop
H2 = JinHin|Sprop.
This time, ∥H1∥≤∥Hout∥= T + 1 = poly(N). Any eigenvector of H2 orthogonal to Sin inside
Sprop has eigenvalue at least Jin/(T + 1). Hence, there is a Jin = poly(N) such that λ(H1 + H2) is
lower bounded by λ(Hout|Sin) −1
8.
Since the circuit Vx accepts with probability less than ε on all inputs |ξ, 0⟩, we have that all
eigenvalues of Hout|Sin are larger than 1 −ε. Hence the smallest eigenvalue of H is larger than
1 −ε −2
8 = 3
4 −ε, proving the second part of the lemma.
5
The 2-local Construction
Previous constructions:
Let us give an informal description of ideas used in previous improve-
ments on Kitaev’s construction; these ideas will also appear in our proof. The ﬁrst idea is to
represent the clock register in unary notation. Then, the clock register consists of T qubits and time
step t ∈{0, . . . , T} is represented by |1t0T−t⟩. The crucial observation is that clock terms that used
to involve log(T + 1) qubits, can now be replaced by 3-local terms that are essentially equivalent.
For example, a term like |t-1⟩⟨t| can be replaced by the term |100⟩⟨110|t−1,t,t+1. Since the gates Ut
8

---- page 9 ----

involve at most two qubits, we obtain a 5-local Hamiltonian. This is essentially the way 5-LOCAL
HAMILTONIAN was shown to be QMA-complete in [KSV02]. The only minor complication is that
we need to get rid of illegal clock states (i.e., ones that are not a unary representation). This is done
by the addition of a (2-local) Hamiltonian Hclock that penalizes a clock state whenever 1 appears
after 0.
This result was further improved to 3-LOCAL HAMILTONIAN in [KR03]. The main idea there
is to replace a 3-local clock term like |100⟩⟨110|t−1,t,t+1 by the 1-local term |0⟩⟨1|t. These one-qubit
terms are no longer equivalent to the original clock terms. Indeed, it can be seen that they have
unwanted transitions into illegal clock states. The main idea in [KR03] was that by giving a large
penalty to illegal clock states (i.e., by multiplying Hclock by some large number) and applying the
projection lemma, we can essentially project these one-qubit terms to the subspace of legal clock
states. Inside this subspace, these terms become the required clock terms.
The 2-local construction:
Most of the terms that appear in the construction of [KR03] are already
2-local. The only 3-local terms are terms as in Eq. (2) that correspond to two-qubit gates (those
corresponding to one-qubit gates are already 2-local). Hence, in order to prove our main theorem,
it is enough to ﬁnd a 2-local Hamiltonian that checks for the correct propagation of 2-qubit gates.
This seems difﬁcult because the Hamiltonian must somehow couple two computation qubits to
a clock qubit. We circumvent this problem in the following manner. First, we isolate from the
propagation Hamiltonian those terms that correspond to one-qubit gates and we multiply these
terms by some large factor. Using the projection lemma, we can project the remaining Hamilto-
nians into a space where the 1-qubit-gate propagation is correct. In other words, at this stage we
can assume that our space is spanned by states that correspond to legal propagation according
to the 1-qubit gates. This allows us to couple clock qubits instead of computation qubits. To see
this, consider the circuit in Fig. 2 at time t and at time t + 2. A Z gate ﬂips the phase of a qubit
if its state is |1⟩and leaves it unchanged otherwise. Hence, the phase difference between time t
and time t + 2 corresponds to the parity of the two qubits. This phase difference can be detected
by a 2-local term such as |00⟩⟨11|t+1,t+2. The crucial point here is that by using a term involving
only two clock qubits, we are able to check the state of two computation qubits (in this case, their
parity) at a certain time. This is the main idea in our proof.
We now present the proof of the main theorem in detail. We start by making some further
assumptions on the circuit Vx, all without loss of generality. First, we assume that in addition
to one-qubit gates, the circuit contains only the controlled phase gate, Cφ. This two-qubit gate is
diagonal in the computational basis and ﬂips the sign of the state |11⟩,
Cφ = Cφ† = |00⟩⟨00| + |01⟩⟨01| + |10⟩⟨10| −|11⟩⟨11|.
It is known [BBC+95, NC00] that quantum circuits consisting of one-qubit gates and Cφ gates are
universal6 and can simulate any other quantum circuit with only polynomial overhead. Second,
we assume that each Cφ gate is both preceded and followed by two Z gates, one on each qubit, as
in Figure 2. The Z gate is deﬁned by |0⟩⟨0| −|1⟩⟨1|; i.e., it is a diagonal one-qubit gate that ﬂips
6The original universal gate set in [BBC+95] consists of one-qubit gates and CNOT gates. It is, however, easy to see
that a CNOT gate can be obtained from a Cφ gate by conjugating the second qubit with Hadamard gates (see [NC00]).
9

---- page 10 ----

the sign of |1⟩. Since both the Z gate and the Cφ gate are diagonal, they commute and the effect of
the Z-gates cancels out. This assumption makes the circuit at most ﬁve times bigger. Finally, we
assume that the Cφ gates are applied at regular intervals. In other words, if T2 is the number of Cφ
gates and L is the interval length, then a Cφ gate is applied at steps L, 2L, . . . , T2L. Before the ﬁrst
Cφ gate, after the last Cφ gate and between any two consecutive Cφ gates we have L −1 one-qubit
gates. This makes the total number of gates in the resulting circuit T = (T2 + 1)L −1.
Cφ
Z
Z
Z
Z
t-2
t-3
t-1
t
t+1
t+2
Figure 2: A modiﬁed Cφ gate applied at step t
We construct a Hamiltonian H that operates on a space of N + T qubits. The ﬁrst N qubits
represent the computation and the last T qubits represent the clock. We think of the clock as
represented in unary,
|bt⟩
def
= |1 . . . 1
| {z }
t
0 . . . 0
| {z }
T−t
⟩.
(5)
Let T1 be the time steps in which a one-qubit gate is applied. Namely, T1 = {1, . . . , T}\{L, 2L, . . . , T2L}.
Then
H = Hout + JinHin + J2Hprop2 + J1Hprop1 + JclockHclock,
where
Hin =
N
X
i=m+1
|1⟩⟨1|i ⊗|0⟩⟨0|1
Hout = (T + 1)|0⟩⟨0|1 ⊗|1⟩⟨1|T
Hclock =
X
1≤i<j≤T
I ⊗|01⟩⟨01|ij.
The terms Hprop1 and Hprop2, which represent the correct propagation according to the 1-qubit
gates and 2-qubit gates respectively, are deﬁned as:
Hprop1 =
X
t∈T1
Hprop,t
Hprop2 =
T2
X
l=1
(Hqubit,lL + Htime,lL)
with
Hprop,t
=
1
2

I ⊗|10⟩⟨10|t,t+1 + I ⊗|10⟩⟨10|t−1,t −Ut ⊗|1⟩⟨0|t −U†
t ⊗|0⟩⟨1|t

for t ∈T1 ∩{2, . . . , T −1} and
Hprop,1
=
1
2

I ⊗|10⟩⟨10|1,2 + I ⊗|0⟩⟨0|1 −U1 ⊗|1⟩⟨0|1 −U†
1 ⊗|0⟩⟨1|1

Hprop,T
=
1
2

I ⊗|1⟩⟨1|T + I ⊗|10⟩⟨10|T−1,T −UT ⊗|1⟩⟨0|T −U†
T ⊗|0⟩⟨1|T

10

---- page 11 ----

and, with ft and st being the ﬁrst and second qubit of the Cφ gate at time t,
Hqubit,t = 1
2

−2|0⟩⟨0|ft −2|0⟩⟨0|st + |1⟩⟨1|ft + |1⟩⟨1|st

⊗(|1⟩⟨0|t + |0⟩⟨1|t)
Htime,t = 1
8I ⊗

|10⟩⟨10|t,t+1 + 6|10⟩⟨10|t+1,t+2 + |10⟩⟨10|t+2,t+3
+ 2|11⟩⟨00|t+1,t+2 + 2|00⟩⟨11|t+1,t+2
+ |1⟩⟨0|t+1 + |0⟩⟨1|t+1 + |1⟩⟨0|t+2 + |0⟩⟨1|t+2
+ |10⟩⟨10|t−3,t−2 + 6|10⟩⟨10|t−2,t−1 + |10⟩⟨10|t−1,t
+ 2|11⟩⟨00|t−2,t−1 + 2|00⟩⟨11|t−2,t−1
+ |1⟩⟨0|t−2 + |0⟩⟨1|t−2 + |1⟩⟨0|t−1 + |0⟩⟨1|t−1

.
At this point, these last two expressions might look strange. Let us say that later, when we consider
their restriction to a smaller space, the reason for this deﬁnition should become clear. Note that all
the above terms are at most 2-local. We will later choose Jin ≪J2 ≪J1 ≪Jclock ≤poly(N). As in
Section 4, we have to prove the following lemma:
Lemma 3 Assume that the circuit Vx accepts with probability more than 1 −ε on some input |ξ, 0⟩. Then
H has an eigenvalue smaller than ε. If the circuit Vx accepts with probability less than ε on all inputs |ξ, 0⟩,
then all eigenvalues of H are larger than 1
2 −ε.
Proof: If the circuit Vx accepts with probability more than 1 −ε on some input |ξ, 0⟩then the state
|η⟩=
1
√
T + 1
T
X
t=0
Ut · · · U1|ξ, 0⟩⊗|bt⟩
satisﬁes ⟨η|H|η⟩≤ε. In order to see this, one can check that
⟨η|Hclock|η⟩= ⟨η|Hprop1|η⟩= ⟨η|Hprop2|η⟩= ⟨η|Hin|η⟩= 0
and ⟨η|Hout|η⟩≤ε. However, verifying that ⟨η|Hprop2|η⟩= 0 can be quite tedious. Later in the
proof, we will mention an easier way to see this.
In the following, we will show that if the circuit Vx accepts with probability less than ε on all
inputs |ξ, 0⟩, then all eigenvalues of H are larger than 1
2 −ε. The proof of this is based on four
applications of Lemma 1. Schematically, we proceed as follows:
H ⊃Slegal ⊃Sprop1 ⊃Sprop ⊃Sin
where Slegal corresponds to states with legal clock states written in unary, and Sprop1 is spanned
by states in the legal clock space whose propagation at time steps corresponding to one-qubit gates
(that is, in T1) is correct. Finally, Sprop and Sin are deﬁned in almost the same way as in Section 4.
These spaces will be described in more detail later.
Norms:
Note that all relevant norms, as needed in Lemma 1, are polynomial in N. Indeed, we
have ∥Hout∥= T + 1 and ∥Hin∥≤N as in Section 4, ∥Hprop1∥≤P
t∈T1 ∥Hprop,t∥≤2T (each term
in Hprop1 has norm at most 2) and ∥Hprop2∥≤PT2
t=1(∥Hqubit,lL∥+ ∥Htime,lL∥) ≤O(T2) ≤O(T).
11

---- page 12 ----

1.
Restriction to legal clock states in Slegal:
Let Slegal be the (T + 1)2N-dimensional space
spanned by states with a legal unary representation on the T clock qubits, i.e., by states of the
form |eξ⟩⊗|bt⟩with |bt⟩as in Eq. (5). In this ﬁrst stage we apply Lemma 1 with
H1 = Hout + JinHin + J2Hprop2 + J1Hprop1
H2 = JclockHclock.
Notice that Slegal is an eigenspace of H2 of eigenvalue 0 and that states orthogonal to Slegal have
eigenvalue at least Jclock. Lemma 1 implies that we can choose Jclock = poly(∥H1∥) = poly(N)
such that λ(H) can be lower bounded by λ(H1|Slegal) −1
8. Hence, in the remainder of the proof, it
is enough to study H1|Slegal inside the space Slegal. This can be written as:
Hout|Slegal + JinHin|Slegal + J2Hprop2|Slegal + J1Hprop1|Slegal
with
Hin|Slegal =
N
X
i=m+1
|1⟩⟨1|i ⊗|b0⟩⟨b0|
Hout|Slegal = (T + 1)|0⟩⟨0|1 ⊗| bT⟩⟨bT|
Hprop,t|Slegal = 1
2

I ⊗|bt⟩⟨bt| + I ⊗|c
t-1⟩⟨c
t-1| −Ut ⊗|bt⟩⟨c
t-1| −U†
t ⊗|c
t-1⟩⟨bt|

Hqubit,t|Slegal = 1
2

−2|0⟩⟨0|ft −2|0⟩⟨0|st + |1⟩⟨1|ft + |1⟩⟨1|st

⊗

|bt⟩⟨c
t-1| + |c
t-1⟩⟨bt|

Htime,t|Slegal = 1
8I ⊗

|bt⟩⟨bt| + 6|d
t+1⟩⟨d
t+1| + |d
t+2⟩⟨d
t+2|
+ 2|d
t+2⟩⟨bt| + 2|bt⟩⟨d
t+2| + |d
t+1⟩⟨bt| + |bt⟩⟨d
t+1| + |d
t+2⟩⟨d
t+1| + |d
t+1⟩⟨d
t+2|
+ |c
t-3⟩⟨c
t-3| + 6|c
t-2⟩⟨c
t-2| + |c
t-1⟩⟨c
t-1|
+2|c
t-1⟩⟨c
t-3| + 2|c
t-3⟩⟨c
t-1| + |c
t-2⟩⟨c
t-3| + |c
t-3⟩⟨c
t-2| + |c
t-1⟩⟨c
t-2| + |c
t-2⟩⟨c
t-1|

.
The above was obtained by noting that the projection of a term like, say, |10⟩⟨10|t,t+1 on Slegal is
exactly |ˆt⟩⟨ˆt|. Similarly, the projection of the term |1⟩⟨0|t+1 is |d
t+1⟩⟨ˆt|.7 By rearranging terms, the
above expression can be written as a sum of projectors:
Htime,t|Slegal = 1
8I ⊗
n
2

|bt⟩+ |d
t+1⟩
 
⟨bt| + ⟨d
t+1|

+ 2

|d
t+1⟩+ |d
t+2⟩
 
⟨d
t+1| + ⟨d
t+2|

+

|bt⟩−|d
t+1⟩
 
⟨bt| −⟨d
t+1|

+

|d
t+1⟩−|d
t+2⟩
 
⟨d
t+1| −⟨d
t+2|

−2

|bt⟩−|d
t+2⟩
 
⟨bt| −⟨d
t+2|

+ 2

|c
t-3⟩+ |c
t-2⟩
 
⟨c
t-3| + ⟨c
t-2|

+ 2

|c
t-2⟩+ |c
t-1⟩
 
⟨c
t-2| + ⟨c
t-1|

+

|c
t-3⟩−|c
t-2⟩
 
⟨c
t-3| −⟨c
t-2|

+

|c
t-2⟩−|c
t-1⟩
 
⟨c
t-2| −⟨c
t-1|

−2

|c
t-3⟩−|c
t-1⟩
 
⟨c
t-3| −⟨c
t-1|
o
.
(6)
Notice that the above expression is symmetric around t −1
2 (i.e., switching t −1 with t, t −2 with
t + 1, and t −3 with t + 2 does not change the expression). Let us also mention that the fact that
we have terms like |bt⟩−|d
t+2⟩is crucial in our proof. They allow us to compare the state at time t
to the state at time t + 2.
7Notice that we do not have terms like |1⟩⟨1|t; its projection on Slegal is not |ˆt⟩⟨ˆt| but rather |ˆt⟩⟨ˆt| + · · · + | bT⟩⟨bT|.
12

---- page 13 ----

2. Restriction to Sprop1:
We now apply Lemma 1 inside Slegal with
H1 = (Hout + JinHin + J2Hprop2) |Slegal
H2 = J1Hprop1|Slegal.
Let Sprop1 be the 2N(T2+1)-dimensional space given by all states that represent correct propagation
on all one-qubit gates. More precisely, let
|ηl,i⟩
def
=
1
√
L
(l+1)L−1
X
t=lL
Ut · · · U1|i⟩⊗|bt⟩,
(7)
where l ∈{0, . . . , T2}, i ∈{0, . . . , 2N −1} and |i⟩represents the ith vector in the computational
basis. Then these states form a basis of Sprop1. It is easy to see that each |ηl,i⟩is an eigenvector of
Hprop1 of eigenvalue 0. Hence, Sprop1 is an eigenspace of eigenvalue 0 of Hprop1|Slegal. Furthermore,
Hprop1|Slegal decomposes into T2 + 1 invariant blocks, with the lth block spanned by states of the
form Ut · · · U1|i⟩⊗|bt⟩for t = lL, . . . , (l+1)L−1. Inside such a block Hprop1|Slegal corresponds exactly
to Hprop of Section 4, Eqs. (1,2). By Claim 2, its non-zero eigenvalues are at least c/L2 ≥c/T 2 for
some constant c > 0 and hence the smallest non-zero eigenvalue of Hprop1|Slegal is also at least
c/T 2. Therefore, all eigenvectors of H2 orthogonal to Sprop1 have eigenvalue at least J = J1c/T 2
and Lemma 1 implies that for J1 ≥poly(N), λ(H1+H2) can be lower bounded by λ(H1|Sprop1)−1
8.
Hence, in the remainder of the proof, it is enough to study
Hout|Sprop1 + JinHin|Sprop1 + J2Hprop2|Sprop1.
Let us ﬁnd Hprop2|Sprop1. Let t = lL be the time at which the lth Cφ gate is applied and consider the
projection of a state |ηl,i⟩onto the space spanned by the computation qubits and |bt⟩, |d
t+1⟩, |d
t+2⟩.
Since at time t + 1 (resp., t + 2) a Z gate is applied to qubit ft (resp., st), this projection is a linear
combination of the following four states:
|00⟩ft,st|ξ00⟩⊗

|bt⟩+ |d
t+1⟩+ |d
t+2⟩

|01⟩ft,st|ξ01⟩⊗

|bt⟩+ |d
t+1⟩−|d
t+2⟩

|10⟩ft,st|ξ10⟩⊗

|bt⟩−|d
t+1⟩−|d
t+2⟩

|11⟩ft,st|ξ11⟩⊗

|bt⟩−|d
t+1⟩+ |d
t+2⟩

,
where |ξb1b2⟩is an arbitrary state on the remaining N −2 computation qubits. This implies that
the restriction to Sprop1 of the projector on, say, |bt⟩+ |d
t+1⟩from Eq. (6) is essentially the same as
the restriction to Sprop1 of the projector on |0⟩ft|bt⟩. More precisely, for all l1, l2, i1, i2 we have
1
4⟨ηl1,i1|

I ⊗
 |bt⟩+ |d
t+1⟩
 ⟨bt| + ⟨d
t+1|

|ηl2,i2⟩= ⟨ηl1,i1|

|0⟩⟨0|ft ⊗|bt⟩⟨bt|

|ηl2,i2⟩.
Similarly, the term involving |bt⟩−|d
t+2⟩satisﬁes
1
4⟨ηl1,i1|

I ⊗
 |bt⟩−|d
t+2⟩
 ⟨bt|−⟨d
t+2|

|ηl2,i2⟩= ⟨ηl1,i1|
 |01⟩⟨01|ft,st + |10⟩⟨10|ft,st

⊗|bt⟩⟨bt|

|ηl2,i2⟩.
Observe that the right-hand side involves two computation qubits and the clock register. Being
able to obtain such a term from two-local terms is a crucial ingredient in this proof.
13

---- page 14 ----

Following a similar calculation, we see that from the terms involving |c
t-1⟩, |c
t-2⟩, |c
t-3⟩we obtain
projectors involving |c
t-1⟩. To summarize, instead of considering Htime,t|Sprop1 we can equivalently
consider the restriction to Sprop1 of
1
2

2|0⟩⟨0|ft + 2|0⟩⟨0|st + |1⟩⟨1|ft + |1⟩⟨1|st −2 |01⟩⟨01|ft,st −2|10⟩⟨10|ft,st

⊗

|c
t-1⟩⟨c
t-1| + |bt⟩⟨bt|

.
We now add the terms in Hqubit,t. A short calculation shows that (Htime,t + Hqubit,t) |Sprop1 is the
same as the restriction to Sprop1 of
|00⟩⟨00|ft,st
⊗
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|01⟩⟨01|ft,st
⊗
1
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|10⟩⟨10|ft,st
⊗
1
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|11⟩⟨11|ft,st
⊗

|c
t-1⟩+ |bt⟩
 
⟨c
t-1| + ⟨bt|

.
At this point, let us mention how one can show that for the state |η⟩described in the beginning
of this proof, ⟨η|Hprop2|η⟩= 0. First, observe that |η⟩∈Sprop1 (its propagation is correct at all
time steps). Next, since |η⟩has a Cφ propagation at time t, the above Hamiltonian shows that
⟨η|Hprop2|η⟩= 0.
Let us return now to the main proof. Recall that we wish to show a lower bound on the lowest
eigenvalue of
Hout|Sprop1 + JinHin|Sprop1 + J2Hprop2|Sprop1.
(8)
In the following, we show a lower bound on the lowest eigenvalue of the Hamiltonian
Hout|Sprop1 + JinHin|Sprop1 + J2H′
(9)
on Sprop1 where H′ satisﬁes that H′ ≤Hprop2|Sprop1, i.e., Hprop2|Sprop1 −H′ is positive semideﬁnite.
Hence, any lower bound on the lowest eigenvalue of the Hamiltonian in (9) implies the same
lower bound on the lowest eigenvalue of the Hamiltonian in (8). We deﬁne H′ as the sum over
t ∈{L, 2L, . . . , T2L} of the restriction to Sprop1 of
|00⟩⟨00|ft,st
⊗
1
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|01⟩⟨01|ft,st
⊗
1
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|10⟩⟨10|ft,st
⊗
1
2

|c
t-1⟩−|bt⟩
 
⟨c
t-1| −⟨bt|

+
|11⟩⟨11|ft,st
⊗
1
2

|c
t-1⟩+ |bt⟩
 
⟨c
t-1| + ⟨bt|

.
Equivalently, H′ is the sum over t ∈{L, 2L, . . . , T2L} of
1
2

I ⊗|bt⟩⟨bt| + I ⊗|c
t-1⟩⟨c
t-1| −Cφ ⊗|bt⟩⟨c
t-1| −C†
φ ⊗|c
t-1⟩⟨bt|

Sprop1 ,
14

---- page 15 ----

which resembles Eq. (2). Note that this term enforces correct propagation at time step t = lL. We
claim that
H′ = 1
2L
2N−1
X
i=0
T2
X
l=1
(|ηl−1,i⟩−|ηl,i⟩) (⟨ηl−1,i| −⟨ηl,i|) .
(10)
The intuitive reason for this is the following. For any i, |ηl−1,i⟩+ |ηl,i⟩can be seen as a correct
propagation at time t = lL. In other words, consider the projection of |ηl,i⟩on clock |bt⟩and the
projection of |ηl−1,i⟩on clock |c
t-1⟩. Then the ﬁrst state is exactly the second state after applying the
lth Cφ gate. This means that inside Sprop1, checking correct propagation from time t −1 to time t
is equivalent to checking correct propagation from |ηl−1,i⟩to |ηl,i⟩.
More precisely, ﬁx some l and t = lL. Then, using Eq. (7), we get that for all l1, l2, i1, i2 such
that either l1 ̸= l, l2 ̸= l, or i1 ̸= i2,
⟨ηl1,i1|
 I ⊗|bt⟩⟨bt|

|ηl2,i2⟩= 0.
Otherwise, l1 = l2 = l and i1 = i2 = i for some i and we have
⟨ηl,i|
 I ⊗|bt⟩⟨bt|

|ηl,i⟩= 1
L.
Hence we obtain
I ⊗|bt⟩⟨bt||Sprop1 = 1
L
2N−1
X
i=0
|ηl,i⟩⟨ηl,i|
and similarly,
I ⊗|c
t-1⟩⟨c
t-1||Sprop1 = 1
L
2N−1
X
i=0
|ηl−1,i⟩⟨ηl−1,i|.
For the off-diagonal terms we see that
⟨ηl1,i1|

Cφ ⊗|bt⟩⟨c
t-1|

|ηl2,i2⟩= 0
if l1 ̸= l or l2 ̸= l −1. If l1 = l and l2 = l −1 then using Cφ = UlL, we get
⟨ηl,i1|

Cφ ⊗|bt⟩⟨c
t-1|

|ηl−1,i2⟩= 1
L⟨i1| (UlL · · · U1)† CφUlL−1 · · · U1|i2⟩= 1
L⟨i1|i2⟩
which is 0 if i1 ̸= i2 and 1
L otherwise. Hence Cφ ⊗|bt⟩⟨c
t-1||Sprop1 =
1
L
P2N−1
i=0
|ηl,i⟩⟨ηl−1,i| and
similarly for its Hermitian adjoint. This establishes Eq. (10).
3. Restriction to Sprop:
Let Sprop be the 2N-dimensional space whose basis is given by the states
|ηi⟩=
1
√
T + 1
T
X
t=0
Ut · · · U1|i⟩⊗|bt⟩=
1
√T2 + 1
T2
X
l=0
|ηl,i⟩,
for i ∈{0, . . . , 2N −1}. Eq. (10) shows that Sprop is an eigenspace of H′ of eigenvalue 0. Moreover,
H′ is block-diagonal with 2N blocks of size T2 + 1. Each block is a matrix as in Eq. (4), multiplied
15

---- page 16 ----

by 1/L. As in Claim 2 we see that the smallest non-zero eigenvalue of this Hamiltonian is c/LT 2
2 ≥
c/T 2 for some constant c. Now we can apply Lemma 1. This time, we apply it inside Sprop1 with
H1 = (Hout + JinHin) |Sprop1
H2 = J2H′.
Eigenvectors of H2 orthogonal to Sprop have eigenvalue at least J = J2c/T 2. As before, we can
choose J2 = poly(N) such that λ(H1 + H2) is lower bounded by λ(H1|Sprop) −1
8. Hence, in the
remainder we consider
Hout|Sprop + JinHin|Sprop.
4. Restriction to Sin:
The rest of the proof proceeds in the same way as in Section 4. Indeed,
the subspace Sprop is isomorphic to the one in Section 4 and both Hout|Sprop and Hin|Sprop are the
same Hamiltonians. So by another application of Lemma 1 we get that the lowest eigenvalue
of Hout|Sprop + JinHin|Sprop is lower bounded by λ(Hout|Sin) −1
8. As in Section 4, we have that
λ(Hout|Sin) > 1 −ε if the circuit accepts with probability less than ε. Hence λ(H), the lowest
eigenvalue of the original Hamiltonian H, is larger than 1 −ε −4
8 = 1
2 −ε.
6
Perturbation Theory Proof
In this section we give an alternative proof of our main theorem. In Section 6.1, we develop
our perturbation theory technique. Since this technique might constitute a useful tool in other
Hamiltonian constructions, we keep the presentation as general as possible. Then, in Section 6.2,
we present a speciﬁc application of our technique, the three-qubit gadget. Finally, in Section 6.3,
we use this gadget to complete the proof of the main theorem.
6.1
Perturbation theory
The goal in perturbation theory is to analyze the spectrum of the sum of two Hamiltonians eH =
H + V in the case that V has a small norm compared to the spectral gap of H. One setting was
described in the projection lemma. Speciﬁcally, assume H has a zero eigenvalue with the asso-
ciated eigenspace S, whereas all other eigenvalues are greater than ∆≫∥V ∥. The projection
lemma shows that in this case, the lowest eigenvalue of eH is close to that of V |S. In this section we
ﬁnd a better approximation to Spec eH by considering certain correction terms that involve higher
powers of V . It turns out that these higher order correction terms include interesting interactions,
which will allow us to create an effective 3-local Hamiltonian from 2-local terms. We remark that
the projection lemma (for the entire lower part of the spectrum) can be obtained by following the
development done in this section up to the ﬁrst order.
Before giving a more detailed description of the technique, we need to introduce a certain
amount of notation. For two Hermitian operators H and V , let eH = H + V . We refer to H as the
unperturbed Hamiltonian and to V as the perturbation Hamiltonian. Let λj, |ψj⟩be the eigenvalues
and eigenvectors of H, whereas the eigenvalues and eigenvectors of eH are denoted by eλj, | eψj⟩. In
case of multiplicities, some eigenvalues might appear more than once. We order the eigenvalues
16

---- page 17 ----

in a non-decreasing order
λ1 ≤λ2 ≤· · · ≤λdim H,
eλ1 ≤eλ2 ≤· · · ≤eλdim H.
In general, everything related to the perturbed Hamiltonian is marked with a tilde.
An important component in our proof is the resolvent of eH, deﬁned as
eG(z) =
 zI −eH
−1 =
X
j
 z −eλj
−1 eψj

 eψj
.
(11)
It is a meromorphic8 operator-valued function of the complex variable z with poles at z = eλj. In
fact, for our purposes, it is sufﬁcient to consider real z.9 Its usefulness comes from the fact that
poles can be preserved under projections (while eigenvalues are usually lost). Similarly, we deﬁne
the resolvent of H as G(z) = (zI −H)−1.10
Let λ∗∈R be some cutoff on the spectrum of H.
Deﬁnition 6 Let H = L+ ⊕L−, where L+ is the space spanned by eigenvectors of H with eigenvalues
λ ≥λ∗and L−is spanned by eigenvectors of H of eigenvalue λ < λ∗. Let Π± be the corresponding
projection onto L±. For an operator X on H deﬁne the operator X++ = X|L+ = Π+XΠ+ on L+ and
similarly X−−= X|L−. We also deﬁne X+−= Π+XΠ−as an operator from L−to L+, and similarly
X−+.
With these deﬁnitions, in a representation of H = L+ ⊕L−both H and G are block diagonal
and we will omit one index for their blocks, i.e., H+
def
= H++, G+
def
= G++ and so on. Note that
G−1
± = zI± −H±. To summarize, we have:
eH =
 
eH++
eH+−
eH−+
eH−−
!
V =
 
V++
V+−
V−+
V−−
!
H =
 
H+
0
0
H−
!
eG =
 
eG++
eG+−
eG−+
eG−−
!
G =
 
G+
0
0
G−
!
We similarly write H = eL+ ⊕eL−according to the spectrum of eH and the cutoff λ∗. Finally, we
deﬁne
Σ−(z) = zI−−eG−1
−−(z).
This operator-valued function is called self-energy.11
8A meromorphic function is analytic in all but a discrete subset of C, and these singularities must be poles and not
essential singularities.
9 The resolvent is the main tool in abstract spectral theory [Rud91]. In physics, it is known as the Green’s function.
Physicists actually use slightly different Green’s functions that are suited for speciﬁc problems.
10 We can express eG in terms of G (where we omit the variable z):
eG =
 G−1 −V
−1 = G
 I −V G
−1 = G + GV G + GV GV G + GV GV GV G + · · · .
This expansion of eG in powers of V may be represented by Feynman diagrams [AGD75].
11As we will see later, this deﬁntion includes an H−term. This term is usually not considered part of self-energy, but
we have included it for notational convenience.
17

---- page 18 ----

With these notations in place, we can now give an overview of what follows. Our goal is to
approximate the spectrum of eH| eL−. We will do this by showing that in some sense, the spectrum
of Σ−(z) gives such an approximation. To see why this arises, notice that by deﬁnition of Σ−(z),
we have eG−−(z) =
 zI−−Σ−(z)
−1. In some sense, this equation is the analogue of Eq. (11) where
Σ−(z) plays the role of a Hamiltonian for the projected resolvent eG−−(z). However, Σ−(z) is in
general z-dependent and not a ﬁxed Hamiltonian. Nonetheless, for certain choices of H and V ,
Σ−(z) is nearly constant in a certain range of z so we can choose an effective Hamiltonian Heﬀthat
approximates Σ−(z) in this range. Our main theorem relates the spectrum of Heﬀto that of eH| eL−.
Theorem 3 Assume H has a spectral gap ∆around the cutoff λ∗, i.e., all its eigenvalues are in (−∞, λ−]∪
[λ+, +∞), where λ+ = λ∗+ ∆/2 and λ−= λ∗−∆/2. Assume moreover that ∥V ∥< ∆/2. Let ε > 0 be
arbitrary. Assume there exists an operator Heﬀsuch that SpecHeﬀ⊆[c, d] for some c < d < λ∗−ε and
moreover, the inequality
∥Σ−(z) −Heﬀ∥≤ε
holds for all z ∈[c −ε, d + ε]. Then each eigenvalue eλj of eH| eL−is ε-close to the jth eigenvalue of Heﬀ.
The usefulness of the theorem comes from the fact that Σ−(z) has a natural series expansion,
which can be truncated to obtain Heﬀ. This series may give rise to interesting terms; for example,
in our application, 2-local terms in H and V lead to 3-local terms in Heﬀ. To obtain this expansion,
we start by expressing eG in terms of G as
eG =
 G−1 −V
−1 =
 
G−1
+ −V++
−V+−
−V−+
G−1
−−V−−
!−1
.
Then, using the block matrix identity
 
A
B
C
D
!−1
=
 
 A −BD−1C
−1
−A−1B
 D −CA−1B
−1
−D−1C
 A −BD−1C
−1
 D −CA−1B
−1
!
we conclude that
eG−−=

G−1
−−V−−−V−+
 G−1
+ −V++
−1V+−
−1
.
Finally, we can represent Σ−(z) using the series expansion (I −X)−1 = I + X + X2 + · · · ,
Σ−(z) = H−+ V−−+ V−+
 G−1
+ −V++
−1V+−
= H−+ V−−+ V−+G+
 I+ −V++G+
−1V+−
= H−+ V−−+ V−+G+V+−+ V−+G+V++G+V+−+ V−+G+V++G+V++G+V+−+ · · · .
(12)
Proof of Theorem 3: We start with an overview of the proof. We ﬁrst notice that, by deﬁnition,
the eigenvalues of eH| eL−appear as poles in eG. In Lemma 5, we show that these poles also appear
as poles of eG−−. As mentioned before, this is the reason we work with resolvents. In Lemmas 6
18

---- page 19 ----

and 7 we relate these poles to the eigenvalues of Σ−by showing that z is a pole of eG−−if and only
if it is an eigenvalue of Σ−(z). In other words, these are values of z for which Σ−(z) has z as an
eigenvalue. Finally, we complete the proof of the theorem by using the assumption that Σ−(z) is
close to Heﬀ, so any eigenvalue of Σ−(z) must be close to an eigenvalue of Heﬀ. This situation is
illustrated in Figure 3.
c −ε
d + ε
d + ε
c −ε
z
e.v.
Figure 3: The spectrum of Σ−(z) as a function of z is indicated with solid curves. The boxes
correspond to the spectrum of eH| eL−; they are those eigenvalues of Σ−(z) that lie on the dashed
line z = e.v. The dots indicate the spectrum of Heﬀ, which approximates the spectrum of eH| eL−.
We start with a simple lemma that says that if two Hamiltonians H1, H2 are close, their spectra
must also be close. It is a special case of Weyl’s inequalities (see, e.g., Section III.2 in [Bha97]).
Lemma 4 Let H1, H2 be two Hamiltonians with eigenvalues µ1 ≤µ2 ≤. . . and σ1 ≤σ2 ≤. . . . Then,
for all j, |µj −σj| ≤∥H1 −H2∥.
Proof: We will use a fact from the theory of Hermitian forms: if X ≤Y (i.e., if Y −X is positive
semideﬁnite), then the operator Y has at least as many positive and nonnegative eigenvalues as
X. Let ε = ∥H1 −H2∥; then
(µj −ε)I −H2 ≤µjI −H1 ≤(µj + ε)I −H2.
The operator µjI −H1 has at most j −1 positive and at least j nonnegative eigenvalues. Hence
(µj −ε)I −H2 has at most j −1 positive eigenvalues, and (µj +ε)I −H2 has at least j nonnegative
eigenvalues. It follows that σj ∈[µj −ε, µj + ε].
The next lemma asserts that the poles of eG−−in the range (−∞, λ∗) are in one-to-one corre-
spondence with the eigenvalues of eH| eL−. Hence we can recover the eigenvalues of eH| eL−from the
poles of eG−−.
Lemma 5 Let ˜λ be in (−∞, λ∗) and let m ≥0 be its multiplicity as an eigenvalue of eH| eL−. Then around
˜λ, eG−−is of the form (z −˜λ)−1A + O(1) where A is a rank m operator.
Proof: We ﬁrst show that eL−∩L+ = {0}. Suppose the contrary, i.e., there is a nonzero vector
|ξ⟩∈eL−∩L+. W.l.o.g. ⟨ξ|ξ⟩= 1. Then we have ⟨ξ|(H + V )|ξ⟩≤λ∗(since |ξ⟩∈eL−) and
19

---- page 20 ----

⟨ξ|H|ξ⟩≥λ+ (since |ξ⟩∈L+). Hence ⟨ξ|V |ξ⟩≤λ∗−λ+ = −∆/2. But this is impossible because
∥V ∥< ∆/2.
Now, since eL−∩L+ = {0}, we have that Π−|ξ⟩̸= 0 for all nonzero vectors |ξ⟩∈eL−. From Eq.
(11) we obtain
eG−−= Π−eGΠ−=
X
j
(z −eλj)−1Π−| eψj⟩⟨eψj|Π−.
If the multiplicity of ˜λ is m then the matrix P | eψj⟩⟨eψj| of the corresponding eigenvectors has rank
m. This implies that the matrix P Π−| eψj⟩⟨eψj|Π−also has rank m. Indeed, if there is some linear
combination of Π−| eψj⟩that sums to zero then taking the same linear combination of | eψj⟩must
also sum to zero.
The next two lemmas relate the spectrum of eH| eL−to the operator Σ−(z).
Lemma 6 For any z < λ∗, the multiplicity of z as an eigenvalue of eH| eL−is equal to the multiplicity of z
as an eigenvalue of Σ−(z).
Proof: Fix some z < λ∗and let m be its multiplicity as an eigenvalue of eH (in particular, m = 0 if
z is not an eigenvalue of eH). In the neighborhood of z the function eG−−(w) has the form
eG−−(w) = (w −z)−1A + B + O
 |w −z|

,
where by Lemma 5, A is an operator of rank m. We now consider eG−1
−−(w). For any w < λ+ −∥V ∥
the norm of G+(w) is strictly less than 1/∥V ∥. Hence, by Eq. (12) we see that all the poles of
Σ−(w) lie on the interval

λ+ −∥V ∥, +∞

; in particular eG−1
−−(w) = wI−−Σ−(w) is analytic for
w ∈(−∞, λ∗]. Hence we can write
eG−1
−−(w) = wI−−Σ−(w) = C + D(w −z) + O
 |w −z|2
.
We claim that the dimension of the null-space of C is exactly m. Notice that this implies that z is
an m-fold eigenvalue of Σ−(z) = zI−−C. By multiplying the two equations above, we obtain
I−= eG−1
−−(w) eG−−(w) = (w −z)−1CA + (DA + CB) + O(|w −z|).
By equating coefﬁcients, we obtain CA = 0 and DA + CB = I−. On one hand, CA = 0 implies
that the null-space of C has dimension at least m. On the other hand, the rank of DA is at most
rank(A) = m. Since I−has full rank, the dimension of the null-space of CB must be at most m.
This implies that the dimension of the null-space of C must also be at most m.
We observe that the function Σ−(z) is monotone decreasing in the operator sense (i.e., if z1 ≤z2
then Σ−(z1) −Σ−(z2) is positive semideﬁnite):
dΣ−(z)
dz
=
d
dz

H−+ V−−+ V−+(zI+ −H+ −V++)−1V+−

= −V−+(zI+ −H+ −V++)−2V+−≤0.
Lemma 7 Let eλj be the jth eigenvalue of eH| eL−. Then it is also the jth eigenvalue of Σ−(eλj).
20

---- page 21 ----

Proof: For any z ∈R, let f1(z) (resp., f2(z)) be the number of eigenvalues not greater than z of
eH| eL−(resp., Σ−(z)). When z →−∞, f1(z) is clearly 0. By the monotonicity of Σ−we see that
f2(z) is also 0. Using Lemma 6 we see that as z increases, both numbers increase together by the
same amount m whenever z hits an eigenvalue of eH| eL−of multiplicity m (here we used again the
monotonicity of Σ−). Hence, for all z, f1(z) = f2(z) and the lemma is proven.
We can now complete the proof of the theorem. By Lemma 4 and our assumption on Heﬀ,
we have that for any z ∈[c −ε, d + ε], SpecΣ−(z) is contained in [c −ε, d + ε]. From this and
the monotonicity of Σ−, we obtain that there is no z ∈(d + ε, λ∗] that is an eigenvalue of Σ−(z).
Similarly, there is no z < c −ε that is an eigenvalue of Σ−(z). Hence, using Lemma 6 we see that
Spec eH| eL−is contained in [c −ε, d + ε]. Now let eλj ∈[c −ε, d + ε] be the jth eigenvalue of eH| eL−.
By Lemma 7 it is also the jth eigenvalue of Σ−(eλj). By Lemma 4 it is ε-close to the jth eigenvalue
of Heﬀ.
6.2
The Three-Qubit Gadget
In this section we demonstrate how Theorem 3 can be used to transform a 3-local Hamiltonian into
a 2-local one. The complete reduction will be shown in the next section. From now we try to keep
the discussion more specialized to our QMA problem rather than presenting it in full generality as
was done in Section 6.1.
Let Y be some arbitrary 2-local Hamiltonian acting on a space M of N qubits.
Also, let
B1, B2, B3 be positive semideﬁnite Hamiltonians each acting on a different qubit (so they com-
mute). We think of these four operators as having constant norm. Assume we have the 3-local
Hamiltonian
Y −6B1B2B3.
(13)
The factor 6 is added for convenience. Recall that in the LOCAL HAMILTONIAN problem we are
interested in the lowest eigenvalue of a Hamiltonian. Hence, our goal is to ﬁnd a 2-local Hamilto-
nian whose lowest eigenvalue is very close to the lowest eigenvalue of (13).
We start by adding three qubits to our system. For j = 1, 2, 3, we denote the Pauli operators
acting on the jth qubit by σα
j . Let δ > 0 be a sufﬁciently small constant. Our 2-local Hamiltonian
is eH = H + V , where
H = −δ−3
4 I ⊗
 σz
1σz
2 + σz
1σz
3 + σz
2σz
3 −3I

V = X ⊗I −δ−2 B1 ⊗σx
1 + B2 ⊗σx
2 + B3 ⊗σx
3

X = Y + δ−1(B2
1 + B2
2 + B2
3)
The unperturbed Hamiltonian H has eigenvalues 0 and ∆
def
= δ−3. Associated with the zero
eigenvalue is the subspace
L−= M ⊗C,
where
C =
 |000⟩, |111⟩

.
21

---- page 22 ----

In the orthogonal subspace C⊥we have the states |001⟩, |010⟩, etc. We may think of the subspace C
as an effective qubit (as opposed to the three physical qubits); the corresponding Pauli operators
are denoted by σα
eﬀ.
To obtain Heﬀ, we now compute the self-energy Σ−(z) using the power expansion in Eq. (12)
up to the third order. There is no zeroth order term, i.e., H−= 0. For the remaining terms, notice
that G+ = (z −∆)−1IL+. Hence, we have
Σ−(z) = V−−+ (z −∆)−1V−+V+−+ (z −∆)−2V−+V++V+−+ (z −∆)−3V−+V++V++V+−+ · · · .
The ﬁrst term is V−−= X ⊗IC because a σx term takes any state in C to C⊥. The expressions in the
following terms are of the form
V−+ = −δ−2
B1 ⊗|000⟩⟨100| + B2 ⊗|000⟩⟨010| + B3 ⊗|000⟩⟨001| +
B1 ⊗|111⟩⟨011| + B2 ⊗|111⟩⟨101| + B3 ⊗|111⟩⟨110|

V++ = X ⊗IC⊥−δ−2
B1 ⊗(|001⟩⟨101| + |010⟩⟨110| + |101⟩⟨001| + |110⟩⟨010|) +
B2 ⊗(. . . ) + B3 ⊗(. . . )

,
where the dots denote similar terms for B2 and B3. Now, in the second term of Σ−(z), V+−ﬂips
one of the physical qubits, and V−+ must return it to its original state in order to return to the space
C. Hence we have V−+V+−= δ−4(B2
1 + B2
2 + B2
3) ⊗IC. The third term is slightly more involved.
Here we have two possible processes. In the ﬁrst process, V+−ﬂips a qubit, V++ acts with X ⊗IC⊥,
and ﬁnally V−+ ﬂips the qubit back. In the second process, V+−, V++, and V−+ ﬂip all three qubits
in succession. Thus,
Σ−(z) = X ⊗IC + (z −∆)−1δ−4(B2
1 + B2
2 + B2
3) ⊗IC
+ (z −∆)−2δ−4(B1XB1 + B2XB2 + B3XB3) ⊗IC
−(z −∆)−2δ−6 B3B2B1 + B2B3B1 + B3B1B2 + B1B3B2 + B2B1B3 + B1B2B3

⊗σx
eﬀ
+ O
 ∥V ∥4(z −∆)−3
.
(14)
We now focus on the range z = O(1) ≪∆. In this range we have
(z −∆)−1 = −1
∆

1 −z
∆
−1
= −1
∆+ O(z/∆2) = −δ3 + O(δ6).
Simplifying, we obtain
Σ−(z) = Y ⊗IC −6B1B2B3 ⊗σx
eﬀ
|
{z
}
Heﬀ
+ O(δ).
Notice that ∥Heﬀ∥= O(1) and hence we obtain that for all z in, say, [−2∥Heﬀ∥, 2∥Heﬀ∥] we have
∥Σ−(z) −Heﬀ∥= O(δ).
We may now apply Theorem 3 with c = −∥Heﬀ∥, d = ∥Heﬀ∥, and λ∗= ∆/2 to obtain the following
result: Each eigenvalue eλj from the lower part of Spec eH is O(δ)-close to the j-th eigenvalue of
22

---- page 23 ----

Heﬀ. In fact, for our purposes, it is enough that the lowest eigenvalue of eH is O(δ)-close to the
lowest eigenvalue of Heﬀ. It remains to notice that the spectrum of Heﬀconsists of two parts that
correspond to the effective spin states |+⟩=
1
√
2
 |0⟩+|1⟩

and |−⟩=
1
√
2
 |0⟩−|1⟩

. Since B1B2B3 is
positive semideﬁnite, the smallest eigenvalue is associated with |+⟩. Hence, the lowest eigenvalue
of eH is equal to the lowest eigenvalue of (13), as required.
6.3
Reduction from 3-LOCAL HAMILTONIAN to 2-LOCAL HAMILTONIAN
In this section we reduce the 3-LOCAL HAMILTONIAN problem to the 2-LOCAL HAMILTONIAN
problem. By the QMA-completeness of the 3-LOCAL HAMILTONIAN problem [KR03], this estab-
lishes Theorem 1.
Theorem 4 There is a polynomial time reduction from the 3-LOCAL HAMILTONIAN problem to the 2-
LOCAL HAMILTONIAN problem.
Proof: Recall that in the 3-LOCAL HAMILTONIAN problem (see Def. 3) we are given two constants
a and b and a local Hamiltonian H(3) = P
j Hj such that each Hj is a 3-qubit term whose norm is
at most poly(n). Our goal in this proof is to transform H(3) into a 2-local Hamiltonian H(2) whose
lowest eigenvalue is close to that of H(3). We do this in two steps. The ﬁrst is a somewhat technical
step where we bring H(3) into a convenient form. In the second step, we replace each 3-local term
with 2-local terms by using the gadget construction of the previous section. Before we continue
with the proof, let us mention that it is crucial that we apply the gadget construction to all 3-local
terms simultaneously. If instead we tried to apply the gadget construction sequentially, we would
end up with an exponential blowup in the norms (since each application of the three-qubit gadget
increases the norm by a multiplicative factor).
Lemma 8 The 3-local Hamiltonian H(3) can be represented as
H(3) = cr
 
Y −6
M
X
m=1
Bm1Bm2Bm3
!
where Y is a 2-local Hamiltonian with ∥Y ∥= O(1/n6), M = O(n3), each Bmi is a one-qubit term of norm
O(1/n3) that satisﬁes Bmi ≥
1
n3I, and cr is a rescaling factor satisfying 1 ≤cr ≤poly(n).12
Proof: First, we can assume without loss of generality that each Hj acts on a different triple of
qubits, and hence there are at most n3 such terms. Recall that any 3-qubit Hermitian operator
can be written as a linear combination with real coefﬁcients of the basis elements σα ⊗σβ ⊗σγ
where each of σα, σβ, σγ ranges over the four possible Pauli matrices {I, σx, σy, σz}. Hence, for
M = O(n3), we can write
H(3) = cr
 
−6
M
X
m=1
cm · σm,α ⊗σm,β ⊗σm,γ
!
,
12 For the proof of Thm. 4 we only need the property Bmi ≥0. The stronger property Bmi ≥
1
n3 I will be used in Sec.
7.
23

---- page 24 ----

where each σm,α is a Pauli matrix acting on one of the qubits, and cr ≤poly(n) is chosen to be
large enough so that |cm| ≤
1
n9 for all m = 1, . . . , M.
We can now write
cm σm,α ⊗σm,β ⊗σm,γ =
 2
n3 I + n6cmσm,α

|
{z
}
Bm1
⊗
 2
n3 I + 1
n3 σm,β

|
{z
}
Bm2
⊗
 2
n3 I + 1
n3 σm,γ

|
{z
}
Bm3
+ Dm
where Dm is 2-local. Since |cm| ≤1/n9 we have that Bmi ≥
1
n3 I and ∥Dm∥= O(1/n9).
We now replace each term −6Bm1Bm2Bm3 by a three-qubit gadget. More speciﬁcally, let δ be a
sufﬁciently small inverse polynomial in n to be chosen later. We consider the Hamiltonian H(2) =
cr eH, eH = H + V , acting on a system of n + 3M qubits, where
H = −δ−3
4
M
X
m=1
I ⊗
 σz
m1σz
m2 + σz
m1σz
m3 + σz
m2σz
m3 −3I

,
V = Y ⊗I + δ−1
M
X
m=1
(B2
m1 + B2
m2 + B2
m3) ⊗I
−δ−2
M
X
m=1
 Bm1 ⊗σx
m1 + Bm2 ⊗σx
m2 + Bm3 ⊗σx
m3

.
(15)
As before, let ∆= δ−3 be the spectral gap of H. Notice that the spectrum of H includes not
only 0 and ∆, but also 2∆, 3∆, . . . , M∆. Associated with the zero eigenvalue is the subspace
spanned by all the zero-subspaces of the gadgets. Using ∥Bmi∥≤O(1/n3) and M = O(n3) we get
∥V ∥= O(δ−2) < ∆/2.
The calculation of Σ−is quite similar to the one-gadget case (cf. Eq. (14)). Each gadget con-
tributes an independent term. Terms up to the third order can only include processes that involve
one gadget. Indeed, in order to involve two gadgets, one has to ﬂip a qubit from one gadget and
from another gadget, and then ﬂip both qubits back. Moreover, since only one gadget is involved,
G+ can be replaced by (z −∆)−1IL+ as before. From the fourth order onwards, processes start to
include cross-terms between different gadgets. However, we claim that their contribution is only
O(δ), as long as |z| = O(1). Indeed, in this range, the eigenvalues of G+, which are (z −∆)−1,
(z −2∆)−1, . . . , are all at most O(δ3) in absolute value while the norm of each of the V terms is at
most O(δ−2). To summarize, for |z| = O(1),
Σ−(z) = Y ⊗IC −6
M
X
m=1
Bm1Bm2Bm3 ⊗
 σx
m

eﬀ
|
{z
}
Heﬀ
+ O(δ).
(16)
Since ∥Heﬀ∥≤O(1), we can apply Theorem 3 with c = −∥Heﬀ∥, d = ∥Heﬀ∥and λ∗= ∆/2. We
obtain that the smallest eigenvalue of eH is O(δ)-close to that of Heﬀ. The spectrum of Heﬀconsists
of 2M parts, corresponding to subspaces spanned by setting each effective spin state to either |+⟩
or |−⟩. Since Bm1Bm2Bm3 ≥0, the smallest eigenvalue of Heﬀis achieved in the subspace where
all effective spin states are in the |+⟩state. In this subspace, Heﬀis identical to H(3)/cr. Hence,
the smallest eigenvalue of H(2) = cr eH is O(crδ)-close to that of H(3). We complete the proof by
choosing δ = c′/cr for some small enough constant c′.
24

---- page 25 ----

7
2-local Universal Adiabatic Computation
In this section we show that adiabatic computation with 2-local Hamiltonians is equivalent to
“standard” quantum computation in the circuit model. In order to prove such an equivalence,
one has to show that each model can simulate the other. One direction is already known: it is not
too hard to show that any polynomial time adiabatic computation can be efﬁciently simulated by
a quantum circuit [FGGS00]. Hence, it remains to show that adiabatic computation with 2-local
Hamiltonians can efﬁciently simulate any quantum circuit. In [AvK+04] it is shown that adiabatic
computation with 3-local Hamiltonians can efﬁciently simulate any quantum circuit. We obtain
our result by combining their result with the techniques in our second proof.
Let us brieﬂy mention the main ideas behind adiabatic computation. For more details see
[AvK+04] and references therein. In adiabatic computation, we consider a time-dependent Hamil-
tonian H(s) for s ∈[0, 1] acting on a quantum system. We initialize the system in the groundstate
of the initial Hamiltonian H(0). This groundstate is required to be some simple quantum state
that is easy to create. We then slowly modify the Hamiltonian from s = 0 to s = 1. We say that
the adiabatic computation is successful if the ﬁnal state of the system is close to the groundstate
of H(1). The adiabatic theorem (see, e.g., [Rei04, AR04]) says that if the Hamiltonian is modiﬁed
slowly enough, the adiabatic computation is successful. In other words, it gives an upper bound
on the running time of an adiabatic computation. For our purposes, it is enough to know that this
bound is polynomial if for any s ∈[0, 1], the norm of H(s), as well as that of its ﬁrst and second
derivatives, is bounded by a polynomial, and the spectral gap of H(s) is larger than some inverse
polynomial.
In [AvK+04] it is shown how to transform an arbitrary quantum circuit into an efﬁcient 3-
local adiabatic computation. To establish this, they deﬁne a 3-local time-dependent Hamiltonian
H(3)(s) with the following properties. First, the Hamiltonian acts on a system of n qubits, where
n is some constant times the number of gates in the circuit. Second, the groundstate of H(3)(0)
is very easy to create (namely, it is the all zero state), and the groundstate of H(3)(1) is some
state that encodes the result of the quantum circuit. Third, for all s ∈[0, 1], the spectral gap of
H(3)(s) is bounded from below by an inverse polynomial in n and the norm of H(3)(s), as well
as that of its ﬁrst and second derivatives, is bounded by some polynomial in n. Together with
the adiabatic theorem, these properties imply that adiabatic computation according to H(3)(s)
is efﬁcient. Finally, let us mention that H(3)(s), as deﬁned in [AvK+04], is linear in s, that is,
H(3)(s) = (1 −s)H(3)(0) + sH(3)(1). This property will be useful in our proof.
The following is the main theorem of this section.
Theorem 5 Any quantum computation can be efﬁciently simulated by an adiabatic computation with 2-
local Hamiltonians.
Proof: Given a quantum circuit, let H(3)(s) be the time-dependent Hamiltonian of [AvK+04] as
described above. The idea of the proof is to apply the gadget construction of Sec. 6.3 to H(3)(s) for
any s ∈[0, 1], thereby creating a 2-local time-dependent Hamiltonian H(2)(s). Some care needs to
be taken to ensure that the resulting time-dependent Hamiltonian is smooth enough as a function
of s. We therefore describe how this is done in more detail.
We start by writing H(3)(s) in a form similar to that given by Lemma 8. Since H(3)(s) is linear
25

---- page 26 ----

in s, we can write
H(3)(s) = cr
 
−6
M
X
m=1
cm(s) · σm,α ⊗σm,β ⊗σm,γ
!
,
where M = O(n3), each cm(s) is a linear function of s, and cr ≤poly(n) is chosen to be large
enough so that |cm(s)| ≤
1
n9 for all m and all s ∈[0, 1]. Notice that cr is a ﬁxed scaling factor, used
for all s ∈[0, 1]. Following the proof of Lemma 8, we write
H(3)(s) = cr
 
Y (s) −6
M
X
m=1
Bm1(s)Bm2Bm3
!
where by our construction, Y (s) and Bm1(s) are linear in s, whereas Bm2 and Bm3 are independent
of s. Finally, we deﬁne H(2)(s) = cr ˜H(s), where ˜H(s) = H + V (s) and the Hamiltonians H and
V (s) are deﬁned as in Eq. (15). The parameter δ will be chosen later to be some small enough
inverse polynomial in n.
In the rest of the proof, we show that adiabatic computation according to H(2)(s) can be used
to simulate the given quantum circuit. We start by proving two lemmas that, together with the
adiabatic theorem, imply that the running time of the adiabatic computation is polynomial in n.
Lemma 9 For any s ∈[0, 1], ∥H(2)(s)∥, ∥d
dsH(2)(s)∥, and ∥d2
ds2H(2)(s)∥are upper bounded by a polyno-
mial in n.
Proof: Recall that Y (s) and Bm1(s) are linear in s. Together with the deﬁnition of H(2), this implies
that H(2)(s) is a degree two polynomial in s, i.e., we can write H(2)(s) = A + sB + s2C for some
Hermitian matrices A, B, C. It is not hard to see that the norm of each of these matrices is bounded
by some polynomial in n. This implies that the norm of H(2)(s), of its ﬁrst derivative B +2sC, and
of its second derivative 2C are bounded by some polynomial in n.
Lemma 10 For any s ∈[0, 1], the spectral gap of H(2)(s) is lower bounded by an inverse polynomial in n.
Proof: As shown in Sec. 6.3, the lower part of the spectrum of H(2)(s) is O(crδ)-close to the
spectrum of crHeﬀ(s). Hence, by choosing δ to be a small enough inverse polynomial in n, we see
that it is enough to show that the spectral gap of crHeﬀ(s) is at least some inverse polynomial in n.
The spectrum of crHeﬀ(s) consists of 2M parts, corresponding to all possible settings for the
effective qubits. The part corresponding to the subspace in which all effective qubits are in the |+⟩
state is identical to the spectrum of H(3)(s). Hence, we know that in this subspace the spectral gap
is at least some inverse polynomial in n. We now claim that the lowest eigenvalue in all other 2M −
1 subspaces is greater than that in the all |+⟩subspace by at least some inverse polynomial in n.
Indeed, the restriction of crHeﬀ(s) to any such subspace is given by H(3)(s) plus a nonzero number
of terms of the form 12crBm1(s)Bm2Bm3. The claim follows from the fact that Bm1(s)Bm2Bm3 ≥
1
n9I.
To complete the proof, we need to argue about the groundstate of H(2)(0) and that of H(2)(1).
To this end, we use the following lemma, which essentially says that if Heﬀhas a spectral gap,
then Theorem 3 not only implies closeness in spectra but also in the groundstates.
26

---- page 27 ----

Lemma 11 Assume that H, V, Heﬀsatisfy the conditions of Theorem 3 with some ε > 0. Let λeﬀ,i denote
the ith eigenvalue of Heﬀand |ev⟩(resp., |veﬀ⟩) denote the groundstate of eH (resp., Heﬀ). Then, under the
assumption λeﬀ,2 > λeﬀ,1,
|⟨ev|veﬀ⟩| ≥1 −
2∥V ∥2
(λ+ −λeﬀ,1 −ε)2 −
4ε
λeﬀ,2 −λeﬀ,1
.
Before we prove the lemma, let us complete the proof of the theorem. Recall that in our case
ε = O(δ), ∥V ∥= O(δ−2), λ+ = δ−3, |λeﬀ,1| ≤O(1) and λeﬀ,2 −λeﬀ,1 = 1/poly(n). Hence, the ﬁrst
error term in the above bound is O(δ2) while the second is O(δ ·poly(n)). Therefore, by choosing δ
to be a small enough inverse polynomial in n, we can guarantee that the groundstate of H(2)(s) is
close to the groundstate of Heﬀ(s). In particular, the groundstate of H(2)(1), which is the output of
the adiabatic computation, is close to the groundstate of Heﬀ(1). The latter is |v1⟩⊗|+⟩⊗M, where
|v1⟩is the groundstate of H(3)(1). By simply tracing out the 3M gadget qubits, we can recover
|v1⟩from this groundstate, and therefore obtain the output of the quantum circuit. Similarly, the
groundstate of H(2)(0), which is the state to which the system should be initialized, is close to
the groundstate of Heﬀ(0). The latter is |v0⟩⊗|+⟩⊗M, where |v0⟩is the groundstate of H(3)(0).
We therefore initialize the system by setting the original n qubits to |v0⟩and the M gadgets to
the effective |+⟩state. This state is close to the groundstate of H(2)(0), and since the adiabatic
computation is unitary, this approximation does not affect the output by much.
It remains to prove the lemma.
Proof of Lemma 11: Let |ev−⟩= Π−|ev⟩/∥Π−|ev⟩∥be the normalized projection of |ev⟩on the space
L−. We ﬁrst show that |ev−⟩is close to |ev⟩. By Theorem 3, we know that eλ1 ≤λeﬀ,1 + ε. Hence,
∥Π+ eH|ev⟩∥= eλ1∥Π+|ev⟩∥≤(λeﬀ,1 + ε)∥Π+|ev⟩∥
and
∥Π+ eH|ev⟩∥= ∥Π+H|ev⟩+ Π+V |ev⟩∥≥∥Π+H|ev⟩∥−∥V ∥≥λ+∥Π+|ev⟩∥−∥V ∥.
By combining the two inequalities we obtain
∥Π+|ev⟩∥≤
∥V ∥
λ+ −λeﬀ,1 −ε,
from which we see that
α
def
= |⟨ev|ev−⟩| = ∥Π−|ev⟩∥≥∥Π−|ev⟩∥2 ≥1 −
∥V ∥2
(λ+ −λeﬀ,1 −ε)2 .
Our next step is to show that |ev−⟩is close to |veﬀ⟩. For this we need to consider the proof of
Theorem 3. We start by taking Lemma 5 with eλ = eλ1. The lemma says that A is a matrix of rank
1. By looking at the proof, it is easy to see that A is in fact Π−|ev⟩⟨ev|Π−. Next, Lemma 6 implies
that eλ1 is an eigenvalue of multiplicity 1 of Σ−(eλ1). In fact, from the proof it follows that the
corresponding eigenvector is exactly Π−|ev⟩(since the null space of C is equal to the span of A). By
normalizing, this is exactly |ev−⟩. But by our assumption, ∥Σ−(z)−Heﬀ∥≤ε for all z ∈[c−ε, d+ε]
and in particular
∥Σ−(eλ1) −Heﬀ∥≤ε.
27

---- page 28 ----

From this we obtain that
⟨ev−|(Σ−(eλ1) −Heﬀ)|ev−⟩
 ≤ε
and hence
⟨ev−|Heﬀ|ev−⟩≤eλ1 + ε ≤λeﬀ,1 + 2ε
where we again used that eλ1 ≤λeﬀ,1 +ε. Since Heﬀhas a spectral gap, this indicates that |ev−⟩must
be close to |veﬀ⟩. Indeed, let β = |⟨ev−|veﬀ⟩|. Then,
⟨ev−|Heﬀ|ev−⟩≥β2λeﬀ,1 + (1 −β2)λeﬀ,2 = λeﬀ,1 + (1 −β2)(λeﬀ,2 −λeﬀ,1).
By combining the two inequalities we obtain
1 −β2 ≤
2ε
λeﬀ,2 −λeﬀ,1
.
Summarizing,
|⟨ev|veﬀ⟩| = |⟨ev|ev−⟩⟨ev−|veﬀ⟩+ ⟨ev|(I −|ev−⟩⟨ev−|)|veﬀ⟩|
≥α · β −
p
(1 −α2)(1 −β2) ≥α · β −1
2
 (1 −α2) + (1 −β2)

≥
 1 −(1 −α) −(1 −β)

−
 (1 −α) + (1 −β)

= 1 −2(1 −α) −2(1 −β)
≥1 −
2∥V ∥2
(λ+ −λeﬀ,1 −ε)2 −
4ε
λeﬀ,2 −λeﬀ,1
.
8
Conclusion
Some interesting open questions remain. First, perturbation theory has allowed us to perform
the ﬁrst reduction inside QMA. What other problems can be solved using this technique? Second,
there exists an intriguing class between NP (in fact, MA) and QMA known as QCMA. It is the class
of problems that can be veriﬁed by a quantum veriﬁer with a classical proof. Can one show a
separation between QCMA and QMA? or perhaps show they are equal? Third, Kitaev’s original 5-
local proof has the following desirable property. For any YES instance produced by the reduction
there exists a state such that each individual 5-local term is very close to its groundstate. Note that
this is a stronger property than the one required in the LOCAL HAMILTONIAN problem. Using
a slight modiﬁcation of Kitaev’s original construction, one can show a reduction to the 4-LOCAL
HAMILTONIAN problem that has the same property. However, we do not know if this property
can be achieved for the 3-local or the 2-local problem.
Acknowledgments
Discussions with Sergey Bravyi and Frank Verstraete are gratefully acknowledged. JK is sup-
ported by ACI S´ecurit´e Informatique, 2003-n24, projet “R´eseaux Quantiques”, ACI-CR 2002-40
28

---- page 29 ----

and EU 5th framework program RESQ IST-2001-37559, and by DARPA and Air Force Laboratory,
Air Force Materiel Command, USAF, under agreement number F30602-01-2-0524, and by DARPA
and the Ofﬁce of Naval Research under grant number FDN-00014-01-1-0826 and during a visit
supported in part by the National Science Foundation under grant EIA-0086038 through the Insti-
tute for Quantum Information at the California Institute of Technology. AK is supported in part by
the National Science Foundation under grant EIA-0086038. OR is supported by an Alon Fellow-
ship, the Binational Science Foundation, the Israel Science Foundation, and the Army Research
Ofﬁce grant DAAD19-03-1-0082. Part of this work was carried out during a visit of OR at LRI,
Universit´e de Paris-Sud and he thanks his hosts for their hospitality and acknowledges partial
support by ACI S´ecurit´e Informatique, 2003-n24, projet “R´eseaux Quantiques”.
References
[AGD75] A. A. Abrikosov, L. P. Gorkov, and I. E. Dzyaloshinski. Methods of quantum ﬁeld theory
in statistical physics. Dover Publications Inc., New York, 1975.
[AN02]
D. Aharonov and T. Naveh. Quantum NP - a survey, 2002. quant-ph/0210077.
[AR04]
A. Ambainis and O. Regev.
An elementary proof of the adiabatic theorem, 2004.
quant-ph/0411152.
[AvK+04] D. Aharonov, W. van Dam, J. Kempe, Z. Landau, S. Lloyd, and O. Regev. Adiabatic
quantum computation is equivalent to standard quantum computation. In Proc. 45th
FOCS, pages 42–51, 2004.
[BBC+95] D. Barenco, C. H. Bennett, R. Cleve, D. P. DiVincenzo, N. Margolus, P. Shor, T. Sleator,
J. Smolin, and H. Weinfurter. Elementary gates for quantum computation. Phys. Rev.
A, 52:3457–3467, 1995.
[Bha97]
R. Bhatia. Matrix Analysis. Number 169 in Graduate Texts in Mathematics. Springer-
Verlag, New York, 1997.
[BV05]
S. Bravyi and M. Vyalyi. Commutative version of the k-local Hamiltonian problem and
non-triviality check for quantum codes. Quantum Information & Computation, 5(3):187–
215, 2005.
[FGGS00] E. Farhi, J. Goldstone, S. Gutmann, and M. Sipser. Quantum computation by adiabatic
evolution, 2000. quant-ph/0001106.
[JWB03]
D. Janzing, P. Wocjan, and T. Beth.
Identity check is QMA-complete, 2003.
quant-ph/0305050.
[KKR04]
J. Kempe, A. Kitaev, and O. Regev. The complexity of the local hamiltonian problem.
In Proc. of 24th FSTTCS, pages 372–383, 2004. quant-ph/0406180.
[Kni96]
E. Knill. Quantum randomness and nondeterminism, 1996. quant-ph/9610012.
29

---- page 30 ----

[KR03]
J. Kempe and O. Regev. 3-local Hamiltonian is QMA-complete. Quantum Information &
Computation, 3(3):258–264, 2003.
[KSV02]
A. Yu. Kitaev, A. H. Shen, and M. N. Vyalyi. Classical and quantum computation, vol-
ume 47 of Graduate Studies in Mathematics. AMS, Providence, RI, 2002.
[MW04]
C. Marriott and J. Watrous. Quantum Arthur-Merlin games. In Proc. of 19th IEEE Annual
Conference on Computational Complexity (CCC), 2004.
[NC00]
M.A. Nielsen and I.L. Chuang. Quantum Computation and Quantum Information. Cam-
bridge University Press, Cambridge, UK, 2000.
[OT05]
R. Oliveira and B. Terhal.
The complexity of quantum spin systems on a two-
dimensional square lattice, 2005. quant-ph/0504050.
[Pap94]
C. Papadimitriou. Computational Complexity. Addison Wesley, Reading, Massachusetts,
1994.
[Rei04]
B. Reichardt. The quantum adiabatic optimization algorithm and local minima. In Proc.
of 36th STOC, pages 502–510, 2004.
[Rud91]
W. Rudin. Functional analysis. International Series in Pure and Applied Mathematics.
McGraw-Hill Inc., New York, second edition, 1991.
[Wat00]
J. Watrous. Succinct quantum proofs for properties of ﬁnite groups. In Proc. 41st FOCS,
pages 537–546, 2000.
[WB03]
P. Wocjan and T. Beth. The 2-local Hamiltonian problem encompasses NP. International
J. of Quantum Info., 1(3):349–357, 2003.
30

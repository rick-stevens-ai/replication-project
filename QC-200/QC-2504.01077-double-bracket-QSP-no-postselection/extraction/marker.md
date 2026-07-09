# Double-bracket algorithm for quantum signal processing without post-selection

**arXiv:2504.01077v3 [quant-ph]** — Suzuki, Tiang, Son, Ng, Holmes, Gluza — Quantum 2025-12-16

> **NOTE — Extraction substitution:** Marker was unavailable in this environment (Python 3.14; `marker-pdf` failed to build numpy from source in a wheel-less environment). The content below is the pdftotext `-raw` output preserved as pseudo-markdown — text fidelity is very high but LaTeX equations, tables, and figures are NOT reconstructed as they would be by real Marker. Use `extraction/nougat.mmd` for the layout-preserving variant and the original `paper.pdf` as ground truth for equations. See `report/failure_analysis.md`.

---

Double-bracket algorithm for quantum signal processing
without post-selection
Yudai Suzuki1,2
, Bi Hong Tiang3
, Jeongrak Son3
, Nelly H. Y. Ng 3,4
, Zoë Holmes1
, and
Marek Gluza3
1
Institute of Physics, École Polytechnique Fédérale de Lausanne (EPFL), Lausanne, Switzerland
2
Quantum Computing Center, Keio University, Hiyoshi 3-14-1, Kohoku-ku, Yokohama 223-8522, Japan
3
School of Physical and Mathematical Sciences, Nanyang Technological University, 637371, Singapore
4
Centre for Quantum Technologies, Nanyang Technological University, 637371, Singapore
Quantum Signal Processing (QSP),
a framework for implementing matrix-
valued polynomials, is a fundamental
primitive in various quantum algorithms.
Despite its versatility, a potentially under-
appreciated challenge is that all system-
atic protocols for implementing QSP rely
on post-selection. This can impose pro-
hibitive costs for tasks when amplitude
amplification cannot sufficiently improve
the success probability. For example, in
the context of ground-state preparation,
this occurs when using a too poor initial
state. In this work, we introduce a new
formula for implementing QSP transfor-
mations of Hermitian matrices, which re-
quires neither auxiliary qubits nor post-
selection. Rather, using approximation to
the exact unitary synthesis, we leverage
the theory of the double-bracket quantum
algorithms to provide a new quantum al-
gorithm for QSP, termed Double-Bracket
QSP (DB-QSP). The algorithm requires
the energy and energetic variance of the
state to be measured at each step and has a
recursive structure, which leads to circuit
depths that can grow super exponentially
with the degree of the polynomial. With
these strengths and caveats in mind, DB-
QSP should be viewed as complementing
the established QSP toolkit. In particular,
DB-QSP can deterministically implement
low-degree polynomials to “warm start”
QSP methods involving post-selection.
Marek Gluza: marekludwik.gluza@ntu.edu.sg
1 Introduction
The efficient implementation of matrix-valued
functions plays a central role in the design of
modern quantum algorithms [1]. That is, the
essence of many quantum algorithms boils down
to constructing a polynomial function p(H) of a
given Hermitian matrix H and applying it to an
input state |Ψ⟩ to obtain a normalized state
|Ψ′
⟩ =
p(H)|Ψ⟩
∥p(H)|Ψ⟩∥
(1)
with ∥|ψ⟩∥ =
p
⟨ψ|ψ⟩ for any vector |ψ⟩. For
example, real and imaginary time evolution cor-
respond to the transformations p(H) ≈ exp(iHt)
and p(H) ≈ exp(−τH), while matrix inversion
implements the transformation p(H) ≈ H−1.
Quantum Signal Processing (QSP) is an algo-
rithmic framework for realizing such polynomial
transformations on quantum computers. QSP
has enabled the development of advanced quan-
tum algorithms for solving linear systems of
equations [2, 3, 4], Hamiltonian simulation [5, 6,
7], and ground state preparation [8, 9].
Despite its versatility, an underappreciated
challenge in QSP is the cost of post-selection [10].
For QSP implementation methods such as qubiti-
zation [5] and Linear Combination of Unitaries
(LCU) [11, 12, 13] to be practically viable, the
success probability for post-selection must be suf-
ficiently high to avoid excessive resource over-
head. While amplitude amplification techniques
can improve success probabilities [14, 15], they
may be insufficient when the success proba-
bility is exponentially small in the number of
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 1
arXiv:2504.01077v3 [quant-ph] 18 Dec 2025qubits [16]. For instance, ground-state prepara-
tion algorithms with nearly optimal resource scal-
ing may still incur exponential costs if the initial
overlap between the input state and ground state
is exponentially small [16, 9].
In this work, we propose a new QSP imple-
mentation that eliminates the need for auxiliary
qubits and post-selection. Since the state after
normalization in Eq. (1) is a genuine quantum
state, there must exist a unitary operator UΨ
such that UΨ |Ψ⟩ = p(H)|Ψ⟩/∥p(H)|Ψ⟩∥. This
work identifies how to systematically perform the
unitary synthesis of UΨ. The key insight is that
any linear polynomial, aI + bH with real coeffi-
cients a,b ∈ R and the identity operator I, can
be exactly represented by a unitary operator in
form of
(aI + bH)|Ψ⟩
∥(aI + bH)|Ψ⟩∥
= es[|Ψ⟩⟨Ψ|,H]
|Ψ⟩ , (2)
where s is determined by the energy mean and
variance. Using this building block, we prove
that a recursion involving unitaries in Eq. (2)
together with state-dependent reflection gates
can realize arbitrary polynomial functions (see
Fig. 1). We then utilize the recently-established
theory of Double-Bracket Quantum Algorithms
(DBQA) [17, 18] to derive a unitary synthesis
that can be compiled into primitive gates us-
ing standard quantum computing methods. This
leads to a new quantum algorithm which we call
the Double-Bracket QSP (DB-QSP).
The advantages of DB-QSP come with two
challenges. First, its recursive form means
the depth of circuit required to converge with
arbitrary precision grows super exponentially
with the degree of the target polynomial func-
tions. However, low-degree approximation tech-
niques [3, 2] can be applied to keep the circuits
depths efficient in certain cases. The second lim-
itation is the need to estimate the energy and
variance in energy of the state at each iteration in
order to compute the step size used in the circuit
at the next iteration. However, when the degree
of polynomials scales logarithmically in the in-
verse of the desired precision, the corresponding
sampling overhead should only be polynomial.
DB-QSP can be used both as a standalone
method and as a tool in conjunction with other
QSP methods [5, 12, 13]. In particular, it can
be viewed as a (partial) alternative when the
post-selection overhead of other QSP methods
are prohibitively large. Namely, DB-QSP pro-
vides a deterministic approach to drive a state
closer to a target state, such as an approximate
ground state, regardless of the quality of the ini-
tial state. Conversely, in conventional QSP meth-
ods [5, 12, 13], a low post-selection success prob-
ability could prevent systematic improvements.
Thus DB-QSP can provide a warm-starting pro-
cedure, i.e., a means of preparing approximate
initial states, for existing methods.
2 Preliminaries
2.1 Overview of Quantum Signal Processing
(QSP)
QSP is a framework for systematically construct-
ing matrix-valued functions on quantum comput-
ers. The goal of QSP is to perform degree-K
polynomial transformation p(H) of a Hermitian
matrix H to a n-qubit input state |Ψ⟩ up to
normalization (Eq. (1)). Sometimes, the imple-
mentation methodology proposed in Ref. [1] itself
is referred to as “QSP”. However, Eq. (1) can
be achieved also via alternative techniques, e.g.,
Linear Combination of Unitaries (LCU) [12, 13];
see App. A for a detailed overview. In this
manuscript, we use “QSP” to refer to the concept
of implementing the polynomial functions, and
distinguish it from the methodology in Ref. [1, 5]
by referring to the latter as “qubitization”.
Qubitization uses a circuit UQ comprised of
two types of operators: signal operators W and
signal processing operators S(ϕ), where the phase
ϕ is drawn from a set {ϕk}. The desired poly-
nomial transformation is obtained by perform-
ing a measurement in the so-called signal basis.
Concretely, given the signal operator W(H) of
a Hermitian matrix H with ∥H∥ ≤ 1 and the
signal processing operator Sz(ϕ), there exists a
sequence of QSP phase {ϕk} such that the fol-
lowing circuit
UQ = Sz(ϕ0)
K Y
k=1
W(H)Sz(ϕk) , (3)
followed by measurement in the basis M =
{|+⟩,|−⟩} can realize a degree-K real polyno-
mial p(H). The signal operator W(H) can be
constructed using block-encoding [19], which em-
beds a Hermitian matrix H into the top-left block
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 2(a) Original QSP with Post-Selection [1]
repeat until
success
(b) Our Proposal without Post-Selection (Thm. 2)
Figure 1: Quantum Signal Processing (QSP) without auxiliary qubits and post-selection. We introduce
a new formula for implementing QSP of Hermitian matrices (Thm. 2). (a) To realize a degree-K polynomial of
a Hermitian matrix H, original QSP performs measurement on auxiliary qubits so that the desired transforma-
tion is realized, as shown in Eq. (3). (b) In contrast, our formula does not require auxiliary qubits and accord-
ingly the post-selection. Instead, we recursively apply the state-dependent unitary operators eiθkΨk
esk[Ψk,H]
with
|Ψk+1⟩ = eiθkΨk
esk[Ψk,H]
|Ψk⟩, resulting in the circuit depth that grow significantly in the degree of polynomials
K. Furthermore, to determine the time duration sk and phase θk, energy Ek = ⟨Ψk|H|Ψk⟩ and variance in energy
Vk = ⟨Ψk|H2
|Ψk⟩ − E2
k must be known at each step.
of a larger unitary matrix as
W(H) =
"
H i
√
I − H2
i
√
I − H2 H
#
.
The signal processing operator Sz(ϕ),
Sz(ϕ) = eiϕZ
=
"
eiϕ 0
0 e−iϕ
#
,
then acts on an auxiliary qubit. We provide de-
tails of the achievable functions via this technique
in App. A.
QSP has led to asymptotically optimal Hamil-
tonian simulation algorithms [5] and a near-
optimal method for ground-state preparation [9].
Furthermore, it serves as a fundamental tool for
constructing primitive quantum algorithms that
exhibit quantum advantages [2, 3]. Therefore, its
efficiency in implementing linear algebraic oper-
ations and its role as a key building block for
quantum algorithms have made QSP a subject
of significant interest.
2.2 The Role of Post-Selection in Existing
QSP Methods
Despite their versatility, existing QSP implemen-
tations face several challenges such as difficulty
in finding angles [20] and demanding implemen-
tation costs for block-encodings [21]. As shown
above, qubitization performs the measurement
in the signal basis to post-select for the de-
sired transformation. When this post-selection
in qubitization is unsuccessful, it is possible to
simply repeat the experiment until a success-
ful implementation eventually appears. Ampli-
tude amplification techniques [14] can often en-
hance success probabilities. For instance, Hamil-
tonian simulation benefits from this combination
of techniques [15]. However, in some cases, the
success probability for QSP could be exponen-
tially small in the number of qubits [16]. For ex-
ample, the successful probability of ground-state
preparation can be prohibitively small if not ini-
tialized with a sufficiently good input state.
We illustrate the issue using an example of gen-
eral qubitization. Given an input state |Ψ⟩, the
number of auxiliary qubits na and α ∈ R, apply-
ing UQ in Eq. (3) to |Ψ⟩ yields
|0⟩⊗na
⊗ p(H/α)|Ψ⟩ + |garbage⊥
⟩, (4)
where |garbage⊥
⟩ is an orthogonal state, i.e.,
|garbage⊥
⟩ ⊥ |0⟩⊗na
⊗ H
α |Ψ⟩. The probability
of projecting onto |0⟩⊗na
is given by
psucc = ∥p(H/α)|Ψ⟩∥2
, (5)
which can be exponentially small. For exam-
ple, in the case of Imaginary-Time Evolution
(ITE), where p(H) ≈ e−τH, the success proba-
bility scales with the overlap of the initial state
and the corresponding thermal state, which can
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 3decay exponentially [22, 16, 23]. More gener-
ally, this dependence on state fidelity persists
across various scenarios. For instance, the block-
encoding query complexity for nearly-optimal
ground-state preparation algorithm in Ref. [9]
scales as O(α/γ), where γ = |⟨λ0|Ψ⟩|2 is the
fidelity of the input state |Ψ⟩ with the ground
state |λ0⟩ of H. The query scaling O(α/γ) cor-
responds to the inverse success probability and
thus requires repeated trials for obtaining a suc-
cessful outcome. This indicates that the success
of the block-encoding depends on the input state.
Additionally, since the number of queries to the
block-encoding unitary scales with the degree of
polynomials as shown in Eq. (3), the degree K
needs to be sufficiently low to ensure successful
post-selection each time. For more details and a
discussion of similar challenges when using LCU
for implementing QSP, see App. A.
3 Main Results
3.1 Overview of Analysis
In this section, we present an algorithm for QSP
that requires neither auxiliary qubits nor post-
selection. Our key insight, captured in Lem. 1 in
Sec. 3.2, is that there exists a unitary that exactly
implements the normalized action of the linear
polynomial H −αI on an input state |Ψ⟩ for any
real α. We then show how repeated applications
of this circuit to apply the linear polynomial can
be used to implement any polynomial with real
roots.
Sec. 3.3 tackles the extension to polynomials
with complex roots. This leads to our main re-
sult, Thm. 2, which demonstrates that interleav-
ing the unitary sequence UΨ from Lem. 1 with
state-dependent reflection gates enables the real-
ization of arbitrary polynomials.
Sec. 3.4 introduces a method to implement
the unitary sequence in Thm. 2 called Double-
Bracket QSP (DB-QSP), which performs gen-
eral QSP without post-selection. Namely, we
show that the recently-developed DBQA frame-
work provides a means to efficiently implement
the exponentials of commutators that appear in
Thm. 2. Leveraging DBQA, we formulate DB-
QSP outlined in Alg. 1. We analyze the errors
introduced by this implementation compared to
the idealized scenario in Thm. 2 and show that
circuit depths of DB-QSP scale super exponen-
tially with the degree of the polynomial to be
implemented.
The DB-QSP algorithm (Alg. 1) also requires
the energy and energy variance of the state at
each iteration to be estimated in order to com-
pute the step size for the next iteration. On
quantum hardware, statistical noise is inevitable
due to the finite number of measurement shots.
In Sec. 3.5, we analyze how this noise affects the
accuracy of the constructed state.
To further examine the practical implications
of these challenges, Sec. 3.6 investigates the im-
pact of circuit depth on applicability. Since the
required depth depends on the polynomial de-
gree, DB-QSP is limited to low-degree polyno-
mials. We identify approximate ground-state
preparation as a use case where DB-QSP can be
practically useful.
Finally, Sec. 3.7 discusses a hybrid strategy
that integrates DB-QSP with existing methods
such as variational quantum algorithms, quan-
tum dynamic programming, qubitization and
LCU. The circuit depth scaling of DB-QSP sug-
gests that available experimental resources may
be insufficient for certain tasks. However, even
qubitization with amplitude amplification some-
times demands exponential costs. In such diffi-
cult cases, combining qubitization or LCUs with
DB-QSP could reduce resource requirements.
3.2 Main Tool: Unitary Synthesis for Polyno-
mials with Real Roots without Post-Selection
In Sec. 2, we reviewed a QSP implementation
relying on post-selection. An alternative is to
find a unitary UΨ satisfying
UΨ |Ψ⟩ =
p(H)|Ψ⟩
∥p(H)|Ψ⟩∥
. (6)
The following Lemma constructs a new tool that
provides an explicit and exact construction of UΨ
through an exponential of a specific commutator
for linear polynomials. For simplicity, we here-
after use Ψ as a shorthand for the density matrix
representation of a pure state, i.e., Ψ = |Ψ⟩⟨Ψ|.
Lemma 1 (Unitary synthesis for linear polyno-
mials without post-selection). Suppose p(H) =
H − αI is any linear polynomial of a Hermitian
matrix H with α ∈ R. Given an input state |Ψ⟩
with energy mean EΨ = ⟨Ψ|H |Ψ⟩ and variance
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 4VΨ = ⟨Ψ|H2 |Ψ⟩ − E2
Ψ, the unitary synthesis for
p(H) in Eq. (6) can be achieved by
UΨ = esΨ[Ψ,H]
, (7)
with
sΨ =
−1
√
VΨ
arccos


EΨ − α
q
VΨ + (EΨ − α)2

 . (8)
A rigorous proof of Lem. 1 is provided in
App. B. Here, we present a proof sketch to clarify
the derivation of the unitary operator in Eq. (7).
First, we can see immediately that UΨ is in-
deed unitary as claimed because the commuta-
tor [Ψ,H] in its exponent is anti-Hermitian, i.e.,
[Ψ,H] = −([Ψ,H])†.
Next, we derive Eq. (7), which establishes the
equivalence between esWH with WH = [Ψ,H] and
a linear polynomial applied to |Ψ⟩ for s ∈ R. By
definition, the unitary operator can be expressed
as esWH =
P∞
k=0
sk
k! Wk
H using all powers of WH.
However, when acting on |Ψ⟩, we get
WH |Ψ⟩ = −(H − EΨI)|Ψ⟩ , (9)
while for the second power
W2
H |Ψ⟩ = −(⟨Ψ|H2
|Ψ⟩ − E2
Ψ)|Ψ⟩ = −VΨ |Ψ⟩ .
(10)
This shows that the square of WH leaves |Ψ⟩ un-
changed up to a rescaling prefactor. Thus, by
substituting Eqs. (9), (10) into the series expan-
sion, the resulting state can be simplified to
esΨWH
|Ψ⟩ = (a(sΨ)I + b(sΨ)H)|Ψ⟩, (11)
with real-valued coefficients a(sΨ),b(sΨ) corre-
sponding to any duration sΨ ∈ R given by
a(sΨ) =
EΨ
√
VΨ
sin

sΨ
p
VΨ

+ cos

sΨ
p
VΨ

,
(12)
b(sΨ) = −
1
√
VΨ
sin

sΨ
p
VΨ

. (13)
Here, the derivation exploits the Taylor series of
trigonometric functions. Finally, by solving the
equations a(sΨ) = −α/∥p(H)|Ψ⟩∥ and b(sΨ) =
1/∥p(H)|Ψ⟩∥, we obtain Eq. (8), the time dura-
tion sΨ to realize Eq. (6) for any linear polyno-
mial.
Lem. 1 indicates that there exists a duration
s such that the exponential of the commutator
esWH with WH = [Ψ,H] can realize any linear
real polynomial. Importantly, the duration s can
be found by precise measurements of the energy
and variance of the state Ψ.
Higher order polynomials can then be realised
by repeated applications of Lem. 1. The fun-
damental theorem of algebra shows that a poly-
nomial of degree K with real roots can be rep-
resented as p(H) = aK
QK
k=1(H − αkI) with
αk ∈ R. This implies that such polynomials can
be obtained by implementing Eq. (7) with the
corresponding factors K times,
p(H)|Ψ0⟩
∥p(H)|Ψ0⟩∥
=
K−1 Y
k=0
esk[Ψk,H]
|Ψ0⟩ , (14)
where we start with an input state |Ψ0⟩ and de-
fine |Ψk+1⟩ = esk[Ψk,H] |Ψk⟩ using sk in Eq. (8).
We stress that Eq. (14) only implements func-
tions with real roots. Nonetheless, many func-
tions, such as Chebyshev polynomials, have only
real roots. Hence Eq. (14) can be used for ap-
plications including approximations of ITE; see
App. D for the detail. However, Eq. (14) alone
cannot construct arbitrary polynomial functions,
as the roots can be complex in general. We will
now proceed to discuss how to extend Eq. (14)
to implement polynomials with complex roots.
3.3 Main Result: Unitary Synthesis for Arbi-
trary Polynomials without Post-Selection
In this section we show how Eq. (14) can be gen-
eralized to implement any arbitrary polynomial
of the form
p(H) = aK
K Y
k=1
(H − zkI) , (15)
where the roots can be complex, i.e., zk ∈ C. A
core idea is that introducing a state-dependent
reflection gate eiθΨΨ right after UΨ in Eq. (7) can
realize any complex number z. That is, for any
z ∈ C, we obtain
(H − zI)|Ψ⟩
∥(H − zI)|Ψ⟩∥
= eiθΨΨ
esΨ[Ψ,H]
|Ψ⟩. (16)
Using this technique, we derive a unitary syn-
thesis formula for QSP without the need for the
auxiliary qubits and post-selection, which is the
main result of this work. The proof is provided
in App. B.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 5Theorem 2 (Unitary synthesis for QSP with-
out post-selection). Consider an input state |Ψ0⟩
and any polynomial p(H) of degree K for a given
Hermitian matrix H in the form of Eq. (15).
Given energy mean Ek = ⟨Ψk|H |Ψk⟩ and vari-
ance Vk = ⟨Ψk|H2 |Ψk⟩−E2
k, the unitary synthe-
sis in Eq. (6) can be achieved by
p(H)|Ψ0⟩
∥p(H)|Ψ0⟩∥
=
K−1 Y
k=0
eiθkΨk
esk[Ψk,H]
|Ψ0⟩, (17)
with sk = −1 √
Vk
arccos

|Ek−zk|
√
Vk+|Ek−zk|2

and θk =
arg

Ek−zk
|Ek−zk|

. Here, we recursively define the
state |Ψk⟩ by
|Ψk+1⟩ = eiθkΨk
esk[Ψk,H]
|Ψk⟩ . (18)
Thm. 2 establishes a recursive method for con-
structing any QSP polynomial through a se-
quence of unitary operators. Next, we explicitly
demonstrate how this formulation can be imple-
mented as a quantum algorithm.
3.4 Implementation: Double-Bracket QSP al-
gorithm (DB-QSP)
Building upon Thm. 2, we present a unitary syn-
thesis approach termed the Double-Bracket QSP
algorithm (DB-QSP). A key challenge in imple-
menting Eq. (17) lies in realizing the unitary op-
erator esΨ[Ψ,H]. Here, we adopt the approach of
DBQAs and utilize the group commutator for-
mula [17, 18, 24, 25] given by [26, 17, 27]:
esΨ[Ψ,H]
=

eis
(N)
Ψ Ψ
eis
(N)
Ψ H
e−is
(N)
Ψ Ψ
e−is
(N)
Ψ H
N
+ O(s
3/2
Ψ /
√
N) , (19)
where s(N)
Ψ =
p
|sΨ|/N for sΨ ≤ 0. Note that,
since the range of the arccos function is [0,π],
the time duration sk in Thm. 2 always takes a
non-positive value. Based on this approxima-
tion, DB-QSP implements QSP using the Hamil-
tonian evolution eis
(N)
Ψ H
and the state-dependent
reflection gates eis
(N)
Ψ Ψ
. Specifically, the state-
dependent reflection gate is implemented using
the reflection about the initial state |Ψ0⟩ and a
unitary operator U satisfying |Ψ⟩ = U |Ψ0⟩, i.e.,
eis
(N)
Ψ Ψ
= Ueis
(N)
Ψ Ψ0
U†
. (20)
Algorithm 1: DB-QSP
1: Input: Hermitian operator H, initial state
|Ψ0⟩, degree K, parameters {zk}K−1
k=0 ,
number of group commutator repetitions N.
2: Output: State |ΨK⟩ = p(H)|Ψ0⟩
∥p(H)|Ψ0⟩∥.
3: Initialize: |Ψ⟩ ← |Ψ0⟩.
4: for k = 0 to K − 1 do
5: Compute energy moment Ek and variance
Vk for |Ψ⟩.
6: Use Thm. 2 to determine parameters sk
and θk for
eiθkΨ
esk[Ψ,H]
|Ψ⟩ =
(H − zkI)|Ψ⟩
∥(H − zkI)|Ψ⟩∥
.
7: Set s(N)
k =
p
|sk|/N and the group
commutator unitary
Gk = eis
(N)
k
Ψ
eis
(N)
k
H
e−is
(N)
k
Ψ
e−is
(N)
k
H
.
8: Update state by applying
|Ψ⟩ ← eiθkΨGN
k |Ψ⟩ .
9: end for
10: Return: |Ψ⟩.
Alg. 1 summarizes the procedure of DB-QSP al-
gorithm.
We note that DB-QSP assumes that both the
state-dependent reflection gate with respect to
the initial state and Hamiltonian evolution can
be generated efficiently. Nevertheless, this as-
sumption is not particularly restrictive. For the
reflection gates, a straightforward approach is to
perform the density matrix exponentiation of the
initial state [28, 29]. Yet, if the input state |Ψ0⟩
is a computational basis state, the operation re-
duces to a multi-qubit controlled unitary, which
can be implemented efficiently with cost scaling
linearly in the number of qubits [30, 31, 32]. More
concretely, when |Ψ0⟩ = |0⟩, the reflection gate
takes the form of
eiθ|0⟩⟨0|
= I +(eiθ
−1)|0⟩⟨0| =






eiθ 0 0 0
0 1 0 0
0 0
... 0
0 0 0 1






,
(21)
which corresponds to a multi-qubit controlled pa-
rameterized phase gate. Even when |Ψ0⟩ is not
a computational basis state, if a unitary U exists
such that |Ψ0⟩ can be efficiently prepared from
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 6a basis state, e.g., |0⟩, the reflection gate can be
realized as eiθΨ0 = Ueiθ|0⟩⟨0|U†. Similarly, when
H is a local Hamiltonian, efficient compilation
is feasible using established Hamiltonian simula-
tion methods [33, 34, 12, 35, 36]. Thus, in many
practical scenarios where such compilation sub-
routines are available, Eq. (7) serves as a unitary
synthesis method of QSP without post-selection.
A key question is how efficiently DB-QSP
can implement polynomials with small error.
Eq. (19) indicates that the approximation error is
governed by |sΨ|3/2/
√
N, suggesting that the to-
tal number of group commutator repetiotions N
may need to increase for higher precision. Thus,
elucidating how N (or equivalently, the circuit
depth) scales to achieve a fixed precision is cru-
cial for evaluating the practicality of DB-QSP. In
the following, we analytically estimate the circuit
depth needed to accurately realize a polynomial
p(H) of degree K using DB-QSP. Before diving
into this, we begin by analyzing the potential cost
for implementing one step of DB-QSP with re-
spect to the total discretization steps N.
Implementation cost for a single step of
DB-QSP. We begin by analyzing the total
number of group commutator repetitions N nec-
essary to approximate esΨ[Ψ,H] to ϵ0-precision via
the group commutator formula. That is, we com-
pute the required N such that
∥esΨ[Ψ,H]
− (eis
(N)
Ψ
Ψ
eis
(N)
Ψ
H
e−is
(N)
Ψ
Ψ
e−is
(N)
Ψ
H
)N
∥ ≤ ϵ0.
(22)
From Eq. (19), we can immediately see that the
relative size of sΨ and N determines the error ϵ0.
We further recall that from Thm. 2 we have
|sΨ| =
1
√
VΨ
arccos
|EΨ − z|
p
VΨ + |EΨ − z|2
!
≤
1
|EΨ − z|
, (23)
where the inequality is obtained by exploiting the
fact that sΨ is monotonically decreasing in VΨ (as
shown explicitly in App. B). Combining Eq. (19)
and Eq. (23), we want 1/(|EΨ − z|)3/2
√
N ≤ ϵ0,
and so we find that there exists an N such that
N ∈ O

1
|EΨ − z|3ϵ2
0

(24)
suffices to ensure Eq. (22) holds.
We thus see that a large gap |EΨ − z| reduces
the required number of steps N. Conversely, N
diverges when Vk = 0 and zk = Ek. This can
intuitively be understood as arising from the fact
that the operation H − EkI acts as an “annihi-
lation operator”. If Vk = 0, then the state is an
eigenstate and Ek corresponds to its eigenvalue,
meaning (H − EkI)|Ψ⟩ = 0 and so the method
breaks down. We note that a similar breakdown
for eigenstates was observed for a quantum algo-
rithm for ITE using the group commutator uni-
tary in Ref. [18].
Circuit Depth of DB-QSP. We now proceed
to analyze the circuit depth to realize a DB-QSP
state that is ϵ-close to the ideal state for a degree-
K polynomial. We define the circuit depth as
the number of Hamiltonian evolution gates and
reflection gates to construct quantum circuits for
DB-QSP. For the analysis, consider the following
state constructed by DB-QSP:
|ωK⟩
=
K−1 Y
k=0
eiθkωk

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
|ω0⟩
(25)
where the intermediate state is recursively con-
structed as
|ωk+1⟩
= eiθkωk

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
|ωk⟩
(26)
with s(N)
k =
p
|sk|/N. We also define the exact
QSP state derived from Thm. 2 as
|Ψ(θ,s)⟩ =
K−1 Y
k=0
eiθkΨk
esk[Ψk,H]
|Ψ0⟩ (27)
with θ = (θ0,...,θK−1) and s =
(|s0|,...,|sK−1|). The following Theorem
captures the circuit depths required to ensure
that the DB-QSP state in Eq. (25), agrees with
the true circuit up to ϵ precision. The key
assumption here is that the parameters (θk,sk)
are known exactly. In practice, the parameters
will be computed with a finite number of mea-
surement shots, requiring an additional sampling
overhead and introducing additional errors. We
will address this aspect in Section 3.5.
Theorem 3 (DB-QSP circuit depth). Suppose
H is a Hermitian matrix whose spectral radius
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 7does not exceed unity, i.e., ∥H∥ ≤ 1. Let
ζ = max(θ,s) be the maximum value of all el-
ements in θ and s. Also, consider |ωK⟩ given by
DB-QSP from Alg. 1 in Eq. (25) and the state
|Ψ(θ,s)⟩ from Thm. 2 in Eq. (27) for degree-K
polynomials. Then there exists a circuit depth
NK such that
NK ∈ O

8
3
2
ζ(1 + 6ζ)2K
/ϵ2
+ 3
!K
(28)
suffices to ensure that ∥|Ψ(θ,s)⟩ − |ωK⟩∥ ≤ ϵ.
To prove this, we first utilize a result proven in
App. C that the DB-QSP error can be bounded
as
∥|Ψ(θ,s)⟩ − |ωK⟩∥ ≤
4
3
ζ1/2
(1 + 6ζ)K
/
√
N .
(29)
Next, we compute the circuit depth, which is de-
fined as the total number of Hamiltonian evolu-
tion gates and the reflection gates. Given that
the state is |ωk⟩ = Uk |0⟩, we can write the recur-
sive unitary synthesis formula as
Uk+1 =Ukeiθk|0⟩⟨0|
U†
k × GN
× Uk (30)
with
G = Ukeis
(N)
k
|0⟩⟨0|
U†
keis
(N)
k
H
× Uke−is
(N)
k
|0⟩⟨0|
U†
ke−is
(N)
k
H
.
This implies that each step involves 4N+3 repeti-
tions of the unitary operators Uk at the previous
step. Therefore, since an additional 4N +1 gates
(2N gates for Hamiltonian evolution and 2N +1
for the reflection gates on the initial state |0⟩⟨0|)
are required, the circuit depth Nk+1 at step k+1
is given by Nk+1 = (4N +3)Nk +4N +1. Thus,
the total circuit depth required for a polynomial
of degree K can be represented as
NK =
(4N + 1)((4N + 3)K − 1)
4N + 2
≤ (4N + 3)K
(31)
Thus, by substituting Eq. (31) into the right-
hand side of Eq. (29), Eq. (28) satisfies to ensure
the ϵ-precision as claimed in the theorem.
Thm. 3 indicates that the circuit depth scaling
can be prohibitive for high degree polynomials.
Namely, although the depth scales polynomially
in the precision 1/ϵ, it grows super-exponentially
with the degree of the polynomials K. Conse-
quently, DB-QSP is not practically applicable to
polynomials of arbitrary degrees, but should tar-
get low-degree polynomials.
3.5 Performance Analysis of Perturbations in
Parameters
In this section, we analyze the effect of statistical
noise. As shown in Alg. 1, DB-QSP requires the
estimation of energy and variance to determine
the parameters sk and θk at each time step. How-
ever, due to the finite number of measurement
shots in practice, precise estimation is not feasi-
ble on quantum hardware. Consequently, param-
eters deviate from their true values at each time
step, with perturbations satisfying |sk − s̃k| ≤ δs
and |θk − θ̃k| ≤ δθ. In other words, even if the
quantum hardware performs the operations per-
fectly, statistical errors from the measurements
lead to erroneous parameters.
Under this setting, we provide an error bound
for implementing a polynomial of degree K. We
introduce a noisy state to handle the erroneous
parameters:
|Ψ̃H(θ̃,s̃)⟩ =
K Y
k=1
eiθ̃kΨ̃k
es̃k[Ψ̃k,H]
|Ψ0⟩, (32)
where we define |Ψ̃k+1⟩ = eiθ̃kΨ̃kes̃k[Ψ̃k,H] |Ψ̃k⟩,
with |Ψ̃0⟩ = |Ψ0⟩. Here, we also introduce
θ̃ = (θ̃0,...,θ̃K−1) and s̃ = (|s̃0|,...,|s̃K−1|).
Again, we assume ∥H∥ ≤ 1. We can then de-
rive the following result on the circuit error with
the detailed proof provided in App. C.
Proposition 4 (Stability of Thm. 2 under erro-
neous estimation). Let H be a Hermitian matrix
such that ∥H∥ ≤ 1, and assume that the esti-
mated parameters s̃k and θ̃k satisfy |sk −s̃k| ≤ δs
and |θk − θ̃k| ≤ δθ with ideal parameters sk and
θk for all k. By setting ζ = max(θ,s), the per-
turbed state |Ψ̃H(θ̃,s̃)⟩ in Eq. (32) and the state
|ΨH(θ,s)⟩ from Thm. 2 satisfies
∥|ΨH(θ,s)⟩ − |Ψ̃H(θ̃,s̃)⟩∥
≤
1
3ζ
(1 + 6ζ)K
max(δs,δθ) . (33)
Prop. 4 indicates that the parameter deviation
max(δs,δθ) scales linearly with the accumulated
error and hence its suppression is critical. On the
other hand, since these parameters are nonlinear
functions of energy and variance, analyzing the
impact of statistical estimates from Prop. 4 is
non-trivial. To address this, we extend our anal-
ysis to explicitly account for statistical noise in
energy and variance estimation.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 8The recursive structure of Eq. (27) and
Eq. (32) implies that, even in the limit of in-
finite measurement shots, the estimated energy
and variance may still differ from their ideal val-
ues. This discrepancy arises because these quan-
tities are measured on a potentially different state
at each iteration. Specifically, the statistical esti-
mate Ek (V k) converges to Ẽk (Ṽk) obtained from
the noisy state |Ψ̃k⟩, rather than the ideal values
Ek and Vk. To account for this, we extend Prop. 4
and demonstrate that the statistical noise, δE =
|Ek − Ẽk| and δV = |V k − Ṽk|, exhibits a linear
dependence on the accumulated error in Eq. (33),
but keeps the exponential scaling with K. That
is, ∥|ΨH(θ,s)⟩−|Ψ̃H(θ̃,s̃)⟩∥ ≤ CK max(δE,δV )
for a constant C ≥ 1. See App. C for further
technical details.
Using the results, we also estimate the num-
ber of measurement shots needed to achieve the
state ϵ-close to the ideal state at K step. With-
out loss of generality, we express the Hermitian
matrix as a weighted sum of Pauli terms, i.e.,
H =
PJ
i=1 wiPi. Then, the number of samples
NE (NV ) required to estimate the energy (vari-
ance) within an error ϵ̃ with probability at least
1 − δ, δ ∈ (0,1], scales as NE ∈ O(J∥w∥2
1/ϵ̃δ)
(NV ∈ O(J2∥w∥4
1/ϵ̃δ)), where ∥w∥1 =
PJ
i=1 |wi|.
See App. F for further details. Thus, the num-
ber of measurement shots needed to achieve the
ϵ-precision grows exponentially with the polyno-
mial degree K, since the estimation error must be
sufficiently small to cancel a term that scales ex-
ponentially with K. However, when K scales log-
arithmically with 1/ϵ, the required measurement
shots reduce to polynomial resources in 1/ϵ.
Lastly, in App. E and App. F, we explore two
different aspects to alleviate statistical errors: (1)
the potential of classical computations to reduce
the impact of imprecise estimation, and (2) an
analysis of the estimator for variance operators.
3.6 Application Examples: Ground-State Ap-
proximation and Matrix Inversions
A significant limitation of DB-QSP is its scal-
ing with polynomial order K in Thm. 3. Yet,
Thm. 3 implies that when the degree of poly-
nomials K scales logarithmically in the inverse
of the precision, 1/ϵ, then the circuit depths
follow a quasi-polynomial scaling, i.e., NK =
2polylog(1/ϵ). Thus, DB-QSP is potentially ap-
plicable to polynomial functions of degree at
most K = O(log(1/ϵ)). Indeed, low-degree ap-
proximations, such as those using Chebyshev
polynomials, allow efficient representations of
certain functions using logarithmically-small de-
grees. For specific examples of such approxima-
tions, see App. D. In the following, we present
two representative tasks that illustrate the util-
ity and limitations of low-degree approximations:
ground-state preparation and matrix inversion.
We discuss DB-QSP’s applicability to other tasks
in App. D.
Ground-State Approximation. Given a
Hermitian matrix H, the objective here is to
prepare its ground state |λ0⟩. To achieve this,
some quantum algorithms employ a variety of
filtering techniques that apply suitable functions
of the Hamiltonian. In what follows, we focus on
two representative examples: Imaginary-Time
Evolution (ITE), which employs the exponential
filter, and the approach proposed in Ref. [9],
which makes use of a sign-function filter.
As a first example of a method that can
be implemented using DB-QSP, we consider
Imaginary-Time Evolution (ITE), where the non-
unitary operator p(H) = e−τH is applied to an
initial state |Ψ0⟩:
|Ψτ⟩ =
e−τH |Ψ0⟩
∥e−τH |Ψ0⟩∥
. (34)
A key feature of ITE is that it guarantees con-
vergence as long as the initial state has a nonzero
overlap with the ground state. Refs. [18, 37] es-
tablished that Eq. (7) serves as a first-order ap-
proximation of ITE and further extends this re-
sult by employing group commutator iterations
in Eq. (19) to construct a unitary realization of
ITE: See App. D for more details. In addition
to the methods proposed in Refs. [18, 37], DB-
QSP can be used to directly construct a poly-
nomial approximation of the exponential func-
tion. Specifically, such an approximation requires
a polynomial of degree K = O(
p
2τ̃ log(4/ϵ))
with τ̃ = ⌈max(e2τ,log(2/ϵ))⌉ [38]. This implies
that a polynomial approximation of ITE can be
implemented with a complexity that scales quasi-
polynomially in the error precision ϵ. However,
the scaling with respect to the evolution time τ
remains unfavorable.
Beyond ITE, DB-QSP can also construct al-
ternative filtering functions. Ref. [9] presents a
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 9nearly optimal algorithm for ground-state prepa-
ration using QSVT. The core idea is to use a low-
degree approximation of the sign function, whose
degree scales logarithmically with 1/ϵ, i.e., K =
O(log(1/ϵ)/δ), for an input x ∈ [−2,2]\(−δ,δ)
with δ > 0. Hence, with the same approximation
technique, similar filtering strategies could po-
tentially be realized via DB-QSP with favorable
scaling in the error precision ϵ.
We recall that the success probability of exist-
ing QSP implementations depends on the overlap
between the initial state and ground state, mean-
ing that these methods may fail entirely if the
initial state is not well-prepared [9]. In contrast,
our approach is applicable to any state, as long
as there is a non-zero overlap. Therefore, even
if DB-QSP cannot fully implement the desired
polynomial functions due to resource constraints,
it can still systematically improve the quality of
the state.
Matrix Inversion. The goal of “matrix inver-
sion” is to apply A−1 to an input state, where
A is a square matrix. This is a core subrou-
tine for solving linear systems A|x⟩ = |b⟩ for
|x⟩ [4, 2, 3]. As shown in App. D, a polynomial of
degree K = O(κlog(κ/ϵ)) can approximate the
inverse function 1/x with the precision ϵ for an
input x ∈ [−1,1]\(−1
κ, 1
κ) where κ ≥ 1 is the
condition number of the matrix. While our re-
sults so far apply to Hermitian matrices, we can
construct a Hermitian matrix from any square
matrix A by the extension:
H =
"
0 A
A† 0
#
, (35)
This indicates that DB-QSP has the potential to
efficiently perform matrix inversion in terms of
the inverse precision 1/ϵ. However, the circuit
depth required for DB-QSP scales super expo-
nentially with the condition number, a key factor
in assessing the algorithm’s efficiency. Thus, this
example also highlights a fundamental challenge
for DB-QSP in certain computational tasks.
3.7 Hybrid Strategy: DB-QSP with Existing
Methods
The performance analysis has highlighted that,
while DB-QSP holds promise for certain tasks,
its circuit depth and the requirement for precise
estimation of the energy and variance pose sig-
nificant challenges. However, DB-QSP does not
have to be used as a standalone approach. By
integrating it with existing methods, these limi-
tation can be alleviated and a hybrid approach
may further enhance its feasibility.
In the following, we explore how combining
DB-QSP with established techniques can im-
prove performance. Specifically, we examine
three approaches: (1) Variational Quantum Al-
gorithms (VQA) [39] and classical computation,
(2) Quantum Dynamic Programming (QDP)[40],
(3) qubitization and LCU.
VQA & Classical pre-computations. A po-
tential strategy to circumvent the challenges in
DB-QSP is to employ a preconditioner that by-
passes the initial steps. In this regard, classi-
cal computational methods can serve as effective
preconditioners. Our target operation in Eq. (11)
consists of a weighted sum of I and H with appro-
priate coefficients. Consequently, the feasibility
of classical computation relies on the efficiency
of evaluating ⟨Ψ0|H2k+2|Ψ0⟩ for degree-k poly-
nomials. We show that, if the initial state |Ψ0⟩
is sparse and a Hermitian matrix contains a lim-
ited number of Pauli terms, then classical com-
putation is feasible. Moreover, advanced classical
techniques, e.g., tensor networks, could further
improve the efficiency, see Sec. E for details.
Another approach might be to first use a Vari-
ational Quantum Algorithm (VQA) where a pa-
rameterized quantum circuit Uθ is trained to
approximate the target state. By leveraging a
VQA, a relatively shallow-depth circuit might be
found to replicate the operations of a few DB-
QSP steps, allowing the trained circuit to serve
as a warm start for DB-QSP; i.e. |Ψk⟩ ≈ Uθ |Ψ0⟩
for a small k. However, this strategy has sev-
eral challenges. First, there are no theoretical
guarantees of convergence for VQAs in practi-
cal regimes. Secondly, as highlighted in Thm. 3
and Prop. 4, small errors at each step can ac-
cumulate significantly as the polynomial degree
increases. Consequently, errors introduced by the
VQA may degrade the final result. Another is-
sue is the barren plateau phenomenon [41, 42],
where gradient magnitudes vanish exponentially
with system size, making parameter training im-
practical. Indeed, it has been suggested that
VQAs themselves may need warm starting strate-
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 10gies [43, 44], or else they are classically simula-
ble [45, 46, 47, 48]. In such cases, the direct use
of DB-QSP may be a better option.
Quantum Dynamic Programming (QDP).
We recall that the significant increase in cir-
cuit depth arises from a recursive circuit struc-
ture. Specifically, the implementation of the
state-dependent reflection through eiskΨk =
Ukeisk|0⟩⟨0|U†
k leads to a prohibitive number of
queries to the quantum gates. Therefore, incor-
porating a subroutine that reduces the imple-
mentation cost would enhance the efficiency of
DB-QSP. The operation eisΨk is a special case
of Density-Matrix Exponentiation (DME), for
which some quantum algorithms have been pro-
posed [28, 49, 29]. DME leverages coherent swap
operations between multiple copies of |Ψ⟩ to re-
alize exponentiation. Note that, since the swap
operations are independent of previous runtime,
the circuit depth scales only polynomially.
Recently, Quantum Dynamic Programming
(QDP) has been proposed to study the use of rou-
tines such as DME for speeding up quantum re-
cursions. QDP is powerful in that utilizing mem-
ory leads to an exponential reduction in circuit
depth [40]. This characteristic makes it a viable
subroutine for DB-QSP. However, due to the no-
cloning theorem, QDP has the disadvantage that
one must extend the width when implementing
recursion steps, meaning that multiple copies of
the state must be prepared [40]. Hence, when
combining DB-QSP with QDP, it becomes cru-
cial to balance the trade-off between width and
depth for practical feasibility.
Qubitization & LCU. One may envision
integrating DB-QSP with QSP implementations
that involve post-selection (e.g. qubitization and
LCU). While these methods supplemented with
amplitude amplification are highly sophisticated
and can function as standalone methods, their
practicality can be hindered in certain scenarios.
As discussed in Sec. 2, an exponentially small
success probability can limit the practicality of
these methods for some tasks such as ground-
state preparation. Thus, by leveraging DB-QSP
as a preconditioner, we can potentially mitigate
this issue and enhance the overall feasibility of
these advanced algorithms.
4 Discussion
Quantum signal processing (QSP) is a funda-
mental framework for designing quantum algo-
rithms. Existing implementation methods, such
as qubitization and linear combinations of uni-
taries (LCU), are powerful but rely on post-
selection of auxiliary qubits, which could limit
their celebrated efficiency in certain cases. In
this work, we propose a unitary synthesis for-
mula for QSP without auxiliary qubits and post-
selection. Our method, termed DB-QSP, re-
lies on Thm. 2 together with the recently es-
tablished Double-Bracket Quantum Algorithm
(DBQA) framework [17, 18]. While our ap-
proach comes at the cost of circuit depth and
requires precise estimation of energy and vari-
ance, it can be used to efficiently implement low-
degree polynomial approximations. We further
note that our method requires fewer multi-qubit
controlled gates than qubitization, as no ancil-
lary qubits are used. Namely, DB-QSP may be
more advantageous under hardware constraints,
which are likely to occur in near-term or up-
coming quantum devices. Thus our proposal
broadens the range of options for implementing
the QSP framework on quantum hardware, with
hybrid approaches that combines both DB-QSP
and prior methods looking particularly appeal-
ing.
Further investigations of the fundamental lim-
its of our algorithm’s performance could be inter-
esting. Thm. 2 clarifies that the time duration s
and the angle θ are determined by the energy
mean and fluctuation (i.e., variance). This sug-
gests that thermodynamic quantities alone pro-
vide sufficient information to guide the imple-
mentation of the target transformation. More-
over, these quantities are key to the algorithm’s
efficiency, as the complexity is determined by the
time duration and angles defined using them.
Given that this unitary process originates from
an unphysical polynomial function, the link
between unphysical operations and underlying
physical principles will provide an intriguing per-
spective.
Let us highlight a geometrical view of our
algorithm. As shown in Eq. (3), the core of
qubitization is that an auxiliary two-level system
enables the construction of specific polynomials
through a sequence of unitary operators inter-
leaved with phase gates. Interestingly, Thm. 2
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 11reveals that QSP implementations without aux-
iliary qubits exhibit a similar structure (i.e.,
Eq. (17)). This structural similarity suggests
that both approaches can be analyzed from a ge-
ometrical perspective. More specifically, through
the lens of DBQA [17, 18], it is known that the ex-
ponential of commutators, e[Ψ,H], approximates
the steepest descent direction on the Riemannian
manifold of quantum states with respect to the
cost function −∥H − Ψ∥2
2/2 [50, 51, 52, 53, 54,
55, 56, 57, 58]. While our formulation introduces
additional state-dependent reflection gates, poly-
nomials with real roots, such as Chebyshev poly-
nomials, can be constructed without these addi-
tional gates. This observation suggests a promis-
ing direction for exploring a geometric interpre-
tation of QSP, and possibly of qubitization itself,
within our framework.
Finally, a natural direction for future work
is to compare the runtime of the proposed ap-
proach with that of alternative methods. In par-
ticular, recent studies have introduced Lindbla-
dian approaches requiring only a single ancilla
qubit [59]. Such dissipative schemes potentially
offer an advantages over DBQA and standard
QSP, as the convergence to the ground state is
possible even when the initial state has zero over-
lap with the ground state [59, 60, 61]. Inter-
estingly, it is known that Lindbladian dynamics
can be formulated as a gradient flow with respect
to the quantum relative entropy [62]. This sug-
gests that, despite being seemingly distinct ap-
proaches, DBQAs, QSP and Lindbladian simula-
tions may have a shared foundation in gradient
flow dynamics defined for appropriate cost func-
tions and underlying Riemannian manifolds. A
detailed analysis of the role of Riemannian gradi-
ents in the procedures of Refs. [59, 60, 61] is left
for future investigation.
Acknowledgments. Insightful discussions with
Thais Silva and Andrew Wright are acknowl-
edged. MG, JS, BHT and NN are supported
by the start-up grant of the Nanyang Assistant
Professorship at the Nanyang Technological Uni-
versity in Singapore. ZH was supported by the
Sandoz Family Foundation-Monique de Meuron
program for Academic Promotion. MG was also
supported by the Presidential Postdoctoral Fel-
lowship of the Nanyang Technological University
in Singapore.
References
[1] Guang Hao Low, Theodore J. Yoder,
and Isaac L. Chuang. “Methodology of
resonant equiangular composite quantum
gates”. Phys. Rev. X 6, 041067 (2016).
[2] John M. Martyn, Zane M. Rossi, Andrew K.
Tan, and Isaac L. Chuang. “Grand unifica-
tion of quantum algorithms”. PRX Quan-
tum 2, 040203 (2021).
[3] András Gilyén, Yuan Su, Guang Hao Low,
and Nathan Wiebe. “Quantum singular
value transformation and beyond: exponen-
tial improvements for quantum matrix arith-
metics”. In Proceedings of the 51st An-
nual ACM SIGACT Symposium on Theory
of Computing. Pages 193–204. (2019).
[4] Aram W Harrow, Avinatan Hassidim, and
Seth Lloyd. “Quantum algorithm for linear
systems of equations”. Physical Review Let-
ters 103, 150502 (2009).
[5] Guang Hao Low and Isaac L. Chuang.
“Hamiltonian Simulation by Qubitization”.
Quantum 3, 163 (2019).
[6] Guang Hao Low and Isaac L Chuang. “Op-
timal Hamiltonian simulation by quantum
signal processing”. Physical Review Letters
118, 010501 (2017).
[7] Guang Hao Low. “Quantum signal pro-
cessing by single-qubit dynamics”. PhD
thesis. Massachusetts Institute of Technol-
ogy. (2017). url: http://hdl.handle.net/
1721.1/115025.
[8] Yimin Ge, Jordi Tura, and J Ignacio Cirac.
“Faster ground state preparation and high-
precision ground energy estimation with
fewer qubits”. Journal of Mathematical
Physics60 (2019).
[9] Lin Lin and Yu Tong. “Near-optimal ground
state preparation”. Quantum 4, 372 (2020).
[10] Lei Zhang, Jizhe Lai, Xian Wu, and Xin
Wang. “Quantum imaginary-time evolution
with polynomial resources in time” (2025).
arXiv:2507.00908.
[11] Long Gui-Lu and Liu Yang. “Duality
computing in quantum computers”. Com-
munications in Theoretical Physics 50,
1303 (2008).
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 12[12] Andrew M. Childs and Nathan Wiebe.
“Hamiltonian simulation using linear com-
binations of unitary operations”. Quantum
Inf. Comput. 12, 901–924 (2012).
[13] Shantanav Chakraborty. “Implement-
ing any linear combination of unitaries
on intermediate-term quantum computers”.
Quantum 8, 1496 (2024).
[14] Gilles Brassard, Peter Hø yer, Michele
Mosca, and Alain Tapp. “Quantum
amplitude amplification and estimation”.
In Quantum computation and information
(Washington, DC, 2000). Volume 305 of
Contemp. Math., pages 53–74. Amer. Math.
Soc., Providence, RI (2002).
[15] Dominic W Berry, Andrew M Childs,
Richard Cleve, Robin Kothari, and
Rolando D Somma. “Exponential im-
provement in precision for simulating sparse
Hamiltonians”. In Proceedings of the forty-
sixth annual ACM symposium on Theory
of computing. Pages 283–292. (2014).
[16] Michelle Wynne Sze, Yao Tang, Silas Dilkes,
David Muñoz Ramo, Ross Duncan, and
Nathan Fitzpatrick. “Hamiltonian dynam-
ics simulation using linear combination of
unitaries on an ion trap quantum com-
puter” (2025). arXiv:2501.18515.
[17] Marek Gluza. “Double-bracket quantum al-
gorithms for diagonalization”. Quantum 8,
1316 (2024).
[18] Marek Gluza, Jeongrak Son, Bi Hong
Tiang, Yudai Suzuki, Zoë Holmes, and Nelly
H. Y. Ng. “Double-bracket quantum algo-
rithms for quantum imaginary-time evolu-
tion” (2024). arXiv:2412.04554.
[19] Shantanav Chakraborty, András Gilyén,
and Stacey Jeffery. “The Power of Block-
Encoded Matrix Powers: Improved Re-
gression Techniques via Faster Hamiltonian
Simulation”. In Christel Baier, Ioannis
Chatzigiannakis, Paola Flocchini, and Ste-
fano Leonardi, editors, 46th International
Colloquium on Automata, Languages, and
Programming (ICALP 2019). Volume 132 of
Leibniz International Proceedings in Infor-
matics (LIPIcs), pages 33:1–33:14. (2019).
[20] Abhijeet Alase. “Quantum signal pro-
cessing without angle finding” (2025).
arXiv:2501.07002.
[21] Yuta Kikuchi, Conor Mc Keever, Luuk
Coopmans, Michael Lubasch, and Marcello
Benedetti. “Realization of quantum signal
processing on a noisy quantum computer”.
npj Quantum Information 9, 93 (2023).
[22] Hans Hon Sang Chan, David Muñoz Ramo,
and Nathan Fitzpatrick. “Simulating non-
unitary dynamics using quantum signal pro-
cessing with unitary block encoding” (2023).
arXiv:2303.06161.
[23] Thais L. Silva, Márcio M. Taddei, Ste-
fano Carrazza, and Leandro Aolita. “Frag-
mented imaginary-time evolution for early-
stage quantum signal processors”. Scientific
Reports 13, 18258 (2023).
[24] Matteo Robbiati, Edoardo Pedicillo, An-
drea Pasquale, Xiaoyue Li, Andrew Wright,
Renato Farias, Khanh Uyen Giang, Jeon-
grak Son, Johannes Knörzer, Siong Thye
Goh, et al. “Double-bracket quantum algo-
rithms for high-fidelity ground state prepa-
ration” (2024). arXiv:2408.03987.
[25] Li Xiaoyue, Matteo Robbiati, Andrea
Pasquale, Edoardo Pedicillo, Andrew
Wright, Stefano Carrazza, and Marek
Gluza. “Strategies for optimizing double-
bracket quantum algorithms” (2024).
arXiv:2408.07431.
[26] Christopher M Dawson and Michael A
Nielsen. “The Solovay-Kitaev algorithm”.
Quantum Information & Computation 6,
81–95 (2006).
[27] Yu-An Chen et al. “Efficient product for-
mulas for commutators and applications to
quantum simulation”. Phys. Rev. Res. 4,
013191 (2022).
[28] Seth Lloyd, Masoud Mohseni, and Patrick
Rebentrost. “Quantum principal compo-
nent analysis”. Nature Physics 10, 631–
633 (2014).
[29] M Kjaergaard, ME Schwartz, A Greene,
GO Samach, A Bengtsson, M O’Keeffe,
CM McNally, J Braumüller, DK Kim,
P Krantz, et al. “Demonstration of den-
sity matrix exponentiation using a supercon-
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 13ducting quantum processor”. Physical Re-
view X 12, 011005 (2022).
[30] Adriano Barenco, Charles H. Bennett,
Richard Cleve, David P. DiVincenzo, Nor-
man Margolus, Peter Shor, Tycho Sleator,
John A. Smolin, and Harald Weinfurter.
“Elementary gates for quantum computa-
tion”. Physical Review A 52, 3457 (1995).
[31] Ben Zindorf and Sougato Bose. “Efficient
Implementation of Multi-Controlled Quan-
tum Gates” (2024). arXiv:2404.02279.
[32] Ben Zindorf and Sougato Bose. “Multi-
controlled quantum gates in linear nearest
neighbor” (2025). arXiv:2506.00695.
[33] Andrew M Childs and Robin Kothari. “Lim-
itations on the simulation of non-sparse
Hamiltonians”. Quantum Information &
Computation 10, 669–684 (2010).
[34] Dominic W. Berry, Andrew M. Childs,
Richard Cleve, Robin Kothari, and
Rolando D. Somma. “Simulating Hamilto-
nian Dynamics with a Truncated Taylor Se-
ries”. Phys. Rev. Lett. 114, 090502 (2015).
[35] Andrew M. Childs, Yuan Su, Minh C. Tran,
Nathan Wiebe, and Shuchen Zhu. “Theory
of Trotter Error with Commutator Scaling”.
Phys. Rev. X 11, 011020 (2021).
[36] Andrew M. Childs and Yuan Su. “Nearly
optimal lattice simulation by product formu-
las”. Phys. Rev. Lett. 123, 050503 (2019).
[37] Nathan A McMahon, Mahum Pervez, and
Christian Arenz. “Equating quantum
imaginary time evolution, riemannian gra-
dient flows, and stochastic implementa-
tions” (2025). arXiv:2504.06123.
[38] Sushant Sachdeva, Nisheeth K Vishnoi,
et al. “Faster algorithms via approxima-
tion theory”. Foundations and Trends®
in Theoretical Computer Science 9, 125–
210 (2014).
[39] Marco Cerezo, Andrew Arrasmith, Ryan
Babbush, Simon C Benjamin, Suguru Endo,
Keisuke Fujii, Jarrod R McClean, Kosuke
Mitarai, Xiao Yuan, Lukasz Cincio, et al.
“Variational quantum algorithms”. Nature
Reviews Physics 3, 625–644 (2021).
[40] Jeongrak Son, Marek Gluza, Ryuji Tak-
agi, and Nelly H. Y. Ng. “Quantum dy-
namic programming”. Phys. Rev. Lett. 134,
180602 (2025).
[41] Jarrod R McClean, Sergio Boixo, Vadim N
Smelyanskiy, Ryan Babbush, and Hartmut
Neven. “Barren plateaus in quantum neural
network training landscapes”. Nature Com-
munications 9, 1–6 (2018).
[42] M. Cerezo, Akira Sone, Tyler Volkoff,
Lukasz Cincio, and Patrick J Coles. “Cost
function dependent barren plateaus in shal-
low parametrized quantum circuits”. Nature
Communications 12, 1–12 (2021).
[43] Ricard Puig, Marc Drudis, Supanut
Thanasilp, and Zoë Holmes. “Variational
quantum simulation: a case study for un-
derstanding warm starts”. PRX Quantum
6, 010317 (2025).
[44] Hela Mhiri, Ricard Puig, Sacha Lerch,
Manuel S Rudolph, Thiparat Chotibut, Su-
panut Thanasilp, and Zoë Holmes. “A
unifying account of warm start guarantees
for patches of quantum landscapes” (2025).
arXiv:2502.07889.
[45] Marco Cerezo, Martin Larocca, Diego
Garcı́a-Martı́n, Nelson L Diaz, Paolo Brac-
cia, Enrico Fontana, Manuel S Rudolph,
Pablo Bermejo, Aroosa Ijaz, Supanut
Thanasilp, et al. “Does provable absence
of barren plateaus imply classical simu-
lability?”. Nature Communications 16,
7907 (2025).
[46] Armando Angrisani, Alexander Schmidhu-
ber, Manuel S Rudolph, M Cerezo, Zoë
Holmes, and Hsin-Yuan Huang. “Classically
estimating observables of noiseless quantum
circuits” (2024). arXiv:2409.01706.
[47] Pablo Bermejo, Paolo Braccia, Manuel S
Rudolph, Zoë Holmes, Lukasz Cincio, and
M Cerezo. “Quantum convolutional neural
networks are (effectively) classically simula-
ble” (2024). arXiv:2408.12739.
[48] Sacha Lerch, Ricard Puig, Manuel S
Rudolph, Armando Angrisani, Tyson Jones,
M Cerezo, Supanut Thanasilp, and Zoë
Holmes. “Efficient quantum-enhanced clas-
sical simulation for patches of quantum
landscapes” (2024). arXiv:2411.19896.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 14[49] Shelby Kimmel, Cedric Yen-Yu Lin,
Guang Hao Low, Maris Ozols, and
Theodore J. Yoder. “Hamiltonian sim-
ulation with optimal sample complexity”.
npj Quantum Inf. 3, 13 (2017).
[50] Uwe Helmke and John B. Moore. “Opti-
mization and dynamical systems”. Springer
London. (1994).
[51] JB Moore, RE Mahony, and U Helmke. “Nu-
merical gradient algorithms for eigenvalue
and singular value calculations”. SIAM
Journal on Matrix Analysis and Applica-
tions 15, 881–902 (1994).
[52] Anthony M Bloch. “Steepest descent, linear
programming and Hamiltonian flows”. Con-
temp. Math. AMS 114, 77–88 (1990).
[53] Steven Thomas Smith. “Geometric opti-
mization methods for adaptive filtering”.
Harvard University. (1993).
[54] G Dirr and U Helmke. “Lie theory for quan-
tum control”. GAMM-Mitteilungen 31, 59–
93 (2008).
[55] Indra Kurniawan, Gunther Dirr, and Uwe
Helmke. “Controllability aspects of quan-
tum dynamics: a unified approach for closed
and open systems”. IEEE transactions on
automatic control 57, 1984–1996 (2012).
[56] T Schulte-Herbrüggen, A Spörl, N Khaneja,
and SJ Glaser. “Optimal control for gener-
ating quantum gates in open dissipative sys-
tems”. Journal of Physics B: Atomic, Molec-
ular and Optical Physics 44, 154013 (2011).
[57] Thomas Schulte-Herbrüggen, Steffen J.
Glaser, Gunther Dirr, and Uwe Helmke.
“Gradient flows for optimization in quantum
information and quantum dynamics: Foun-
dations and applications”. Reviews in Math-
ematical Physics 22, 597–667 (2010).
[58] Roeland Wiersema and Nathan Killoran.
“Optimizing quantum circuits with Rieman-
nian gradient flow”. Phys. Rev. A 107,
062421 (2023).
[59] Zhiyan Ding, Chi-Fang Chen, and Lin Lin.
“Single-ancilla ground state preparation via
Lindbladians”. Physical Review Research 6,
033147 (2024).
[60] Chi-Fang Chen, Michael Kastoryano, Fer-
nando GSL Brandão, and András Gilyén.
“Efficient quantum thermal simulation”.
Nature 646, 561–566 (2025).
[61] Chi-Fang Chen, Hsin-Yuan Huang, John
Preskill, and Leo Zhou. “Local minima in
quantum systems”. In Proceedings of the
56th Annual ACM Symposium on Theory
of Computing. Pages 1323–1330. (2024).
[62] Markus Mittnenzweig and Alexander
Mielke. “An entropic gradient structure
for Lindblad equations and couplings of
quantum systems to macroscopic mod-
els”. Journal of Statistical Physics 167,
205–233 (2017).
[63] Danial Motlagh and Nathan Wiebe. “Gen-
eralized quantum signal processing”. PRX
Quantum 5, 020368 (2024).
[64] David Poulin and Pawel Wocjan. “Prepar-
ing ground states of quantum many-body
systems on a quantum computer”. Physical
Review Letters 102, 130503 (2009).
[65] Oumarou Oumarou, Pauline J Ollitrault,
Cristian L Cortes, Maximilian Scheurer,
Robert M Parrish, and Christian Gogolin.
“Molecular Properties from Quantum
Krylov Subspace Diagonalization” (2025).
arXiv:2501.05286.
[66] Long Gui-Lu. “General quantum inter-
ference principle and duality computer”.
Communications in Theoretical Physics 45,
825 (2006).
[67] Andrew M Childs, Robin Kothari, and
Rolando D Somma. “Quantum algorithm
for systems of linear equations with ex-
ponentially improved dependence on preci-
sion”. SIAM Journal on Computing 46,
1920–1950 (2017).
[68] Yulong Dong, Lin Lin, and Yu Tong.
“Ground-state preparation and energy es-
timation on early fault-tolerant quantum
computers via quantum eigenvalue transfor-
mation of unitary matrices”. PRX Quantum
3, 040305 (2022).
[69] Ruizhe Zhang, Guoming Wang, and Peter
Johnson. “Computing ground state proper-
ties with early fault-tolerant quantum com-
puters”. Quantum 6, 761 (2022).
[70] Lin Lin and Yu Tong. “Heisenberg-Limited
Ground-State Energy Estimation for Early
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 15Fault-Tolerant Quantum Computers”. PRX
Quantum 3, 010318 (2022).
[71] Seth Lloyd. “Almost any quantum logic gate
is universal”. Physical Review Letters 75,
346 (1995).
[72] Nicholas C Rubin, Ryan Babbush, and Jar-
rod McClean. “Application of fermionic
marginal constraints to hybrid quantum al-
gorithms”. New Journal of Physics 20,
053020 (2018).
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 16Appendix
Table of Contents
A Overview of Methods for QSP Involving Post-Selection 18
A.1 Overview of QSP Using Qubitization . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
A.2 Overview of QSP Using Linear Combination of Unitaries (LCU) . . . . . . . . . . . . 19
B Proofs of Lem. 1 and Thm. 2 21
B.1 Proof of Lem. 1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 21
B.2 Useful Preliminary Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
B.3 Proof of Thm. 2 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
C Notions of Stability for Unitary Synthesis of Exact Formula in Thm. 2 27
C.1 Convergence of DB-QSP . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
C.2 Perturbation of the Hamiltonian . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
C.3 Perturbation of Angles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31
C.4 Statistical Error Propagation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
D Applications of DB-QSP 39
D.1 Examples of Low-Degree Polynomial Approximations . . . . . . . . . . . . . . . . . . 39
D.2 Derivation of DB-QITE Using DB-QSP . . . . . . . . . . . . . . . . . . . . . . . . . . 41
D.3 Hamiltonian Simulation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 41
D.4 Evolution under a Polynomial Function of Hamiltonian . . . . . . . . . . . . . . . . . 41
D.5 Laurent Polynomials . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
E Classically-Aided DB-QSP Synthesis 42
F Unbiased Estimator of the Operator Variance for Hamiltonians 43
F.1 Measurement Procedure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 43
F.2 Biased and Unbiased Estimator of the Operator Variance . . . . . . . . . . . . . . . . 44
F.3 Total Variance of the Unbiased Estimator of the Operator Variance . . . . . . . . . . 46
F.4 Alternative Unbiased Method of Estimating Operator Variance . . . . . . . . . . . . . 53
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 17A Overview of Methods for QSP Involving Post-Selection
We start with a brief overview of Quantum Signal Processing (QSP) through its unitary synthesis
method known as qubitization. Then, we also introduce the Linear Combination of Unitaries (LCU)
as a unitary synthesis technique for implementing QSP.
A.1 Overview of QSP Using Qubitization
QSP is a framework for systematically constructing matrix-valued functions. The concept of QSP
originated from a series of works which aimed at characterizing the achievable polynomial functions
of a scalar value embedded in a single-qubit rotation [1]. The QSP methodology introduced in Ref. [1]
was later extended to Hermitian matrices through a technique known as qubitization [5], using the
framework of block-encodings. Subsequently, QSP was generalized to all polynomials [63] and extended
to non-square matrices through Quantum Singular Value Transformation (QSVT) [3]. Notably, this
has led to asymptotically optimal Hamiltonian simulation algorithms [5] and a near-optimal method
for ground-state preparation [9]. Furthermore, QSP serves as a fundamental tool for constructing
primitive quantum algorithms that exhibit quantum advantages [2, 3]. Therefore, its efficiency in
implementing linear algebraic operations and its role as a key building block for quantum algorithms
with potential advantages have made QSP a subject of significant interest.
Here, we focus on the qubitization technique [1]. Specifically, following the approach in Ref. [1],
we begin with a degree-K polynomial of a scalar input x ∈ [−1,1]. In the original work, a quantum
circuit UY LC was introduced with a sequential structure comprising of two types of operators: signal
operators W and signal processing operators S(ϕ), where the phase ϕ is drawn from a set ϕk. The
desired polynomial transformation is then obtained by performing a measurement in the so-called
signal basis. Concretely, it was demonstrated that there exists a sequence of QSP phase {ϕk} such
that the following circuit
UY LC = Sz(ϕ0)
K Y
k=1
W(x)Sz(ϕk) (36)
with the operators
W(x) = eixX/2
=
"
x i
√
1 − x2
i
√
1 − x2 x
#
, Sz(ϕ) = eiϕZ
=
"
eiϕ 0
0 e−iϕ
#
,
followed by measurement in the basis M = {|+⟩,|−⟩} can realize a degree-K real polynomial p(x),
provided that
1. Degree of p(x) is equal to or less than K,
2. p(x) has a parity K mod 2,
3. ∀x ∈ [−1,1], |p(x)| ≤ 1.
This setting is referred to as the Wx convention, as the signal operator is implemented using the
rotation-x gate. Alternatively, the rotation-z gate can be used, which is known as the Wz convention.
For further details, see Ref. [2].
The core idea of the synthesis approach is that single-qubit rotations can implement arbitrary
polynomial transformations, provided the conditions mentioned earlier are met. Similarly, this single-
qubit-like structure used in Eq. (36) to synthesize polynomial functions can be extended to Hermitian
matrices by employing the block-encoding technique [19], which embeds a Hermitian matrix H in the
top-left block of a larger unitary matrix. More precisely, UH is called a (α,na,ϵ) block-encoding of H,
if it satisfies
∥H − α(⟨0|⊗na
⊗ I)UH(|0⟩⊗na
⊗ I)∥ ≤ ϵ (37)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 18with α,ϵ ∈ R+ and the number of auxiliary qubits na. An example of the matrix form is given by
W(H) =
"
H i
√
I − H2
i
√
I − H2 H
#
. (38)
By substituting the signal operator W(x) in the unitary UY LC of Eq. (36) with the block-encoded
unitary in Eq. (38), we can perform polynomial transformations of Hermitian matrices. Furthermore,
QSP has been extended to non-square matrices via QSVT, which enables the manipulation of singular
values for broader applications in quantum linear algebra.
We note that, given an input state |Ψ⟩, the state after applying the block-encoding unitary UH in
Eq. (37) is expressed as
|0⟩⊗na
⊗
H
α
|Ω⟩ + |garbage⊥
⟩. (39)
Here, |garbage⊥
⟩ is a state orthogonal to |0⟩⊗na
⊗H/α|Ω⟩. Due to the normalization, the probability
of getting |0⟩⊗na
is given by psucc = ∥H |Ω⟩∥2/α2. By extending Eq. (36) to controlled-unitary
operations, we obtain the state
|0⟩⊗na
⊗ p(H/α)|Ω⟩ + |garbage⊥
⟩, (40)
which succeeds with probability
psucc = ∥p(H/α)|Ω⟩∥2
. (41)
As shown in the main text, a core insight is that this probability can be exponentially small in case of
Imaginary-Time Evolution (ITE) where p(H) ≈ e−τH. In such cases, Eq. (41) is inversely proportional
to the fidelity of the initial state with a thermal state, which can decay exponentially [22, 16]. More
generally, this fidelity dependence holds across different scenarios. For instance, the block-encoding
query complexity for nearly-optimal ground-state preparation algorithm in Ref. [9] scales as O(α/γ),
where γ = |⟨λ0|Ψ⟩|2 is the fidelity of the input state |Ψ⟩ with the ground state |λ0⟩ of H. The
query scaling O(α/γ) corresponds to the inverse success probability and thus requires repeated trials
for obtaining a successful outcome. Other probabilistic methods exhibit similar sensitivity [9, 8, 64];
see, for example, Ref. [65] for a discussion focused on computing expectation values rather than
preparing quantum states and Ref. [10] for modifications of the filter functions which aim to alleviate
this problem. This indicates that the success of the block-encoding depends on the input state.
Additionally, since the number of queries to the block-encoding unitary scales with the degree of
polynomials as shown in Eq. (36), the degree K needs to be sufficiently low to ensure successful
post-selection each time.
A.2 Overview of QSP Using Linear Combination of Unitaries (LCU)
Another straightforward approach to implementing QSP is the Linear Combination of Unitaries (LCU)
technique [66, 12, 12, 34, 13]. More broadly, LCU is a fundamental method for realizing general
matrix functions using unitary operations. The key idea is that, a given matrix H =
PJ
j=1 wjUj,
which can be expressed as a weighted sum of unitary operators {Uj}, can be efficiently implemented
with additional auxiliary qubits whose number grows logarithmically with the number of decomposed
terms J in the matrix. The desired transformation is then realized by measuring the auxiliary qubits,
which corresponds to successfully projecting the system onto a subspace where the target operation
is encoded. In this sense, LCU serves as one way to implement the block-encoding framework in
Eq. (38); that is, LCU can be used as a subroutine of qubitization. However, in this section, we focus
on LCU as a standalone approach for realizing QSP.
We begin by outlining the LCU technique in detail. The framework is built upon two essential
subroutines: PREP and SEL. The PREP encodes the J coefficients {wj} of the target matrix H on
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 19auxiliary register states |0⟩a = |0⟩⊗na
as follows:
PREP : PREP |0⟩a =
J X
j=1
s
wj
∥w∥1
|j⟩, (42)
where ∥w∥1 =
PJ
j=1 |wj| is the 1-norm of the matrix H. The SEL subroutine applies the unitary Uj to
an input state |Ω⟩, conditioned on the control register being in state j. Combining these operations,
we construct the unitary ULCU = PREP†
· SEL · PREP, which gives
ULCU |0⟩a ⊗ |Ω⟩ =
1
∥w∥1
|0⟩a ⊗ H |Ω⟩ + |garbage⊥
⟩. (43)
If a measurement of the auxiliary register yields |0⟩a, the remaining quantum state is the normalized
state given by H |Ω⟩/∥H |Ω⟩∥. The probability of this successful projection is given by
psucc = ∥H |Ω⟩∥2
/∥w∥2
1 . (44)
This procedure extends naturally to QSP. We exploit the fundamental theorem of algebra, which
states that any univariate polynomial with complex coefficients p(z) =
PK
k=0 akzk can be factorized
in terms of its roots zk to take the form p(z) = aK
QK
k=0(z − zk). This directly generalizes to matrix
functions and we get
p(H) = aK
K Y
k=0
(H − zkI) . (45)
Setting H as a Hermitian matrix, we proceed inductively by applying a sequence of the operators
Fk = H − zkI using LCU. This results in the transformation
|Ψk+1⟩ =
Fk |Ψk⟩
∥Fk |Ψk⟩∥
. (46)
Since the leading coefficient aK of the polynomial p(H) = aK
QK
k=1 Fk cancels out by normalization,
we obtain
|ΨK⟩ =
p(H)|Ψ0⟩
∥p(H)|Ψ0⟩∥
. (47)
Let us next discuss the success probability of this procedure assuming that the Hamiltonian is decom-
posed into Pauli operators as H =
PJ
i=1 wiPi. From Eq. (44), the success probability of post-selection
for k step is equal to the conditional probability given that the state |Ψk−1⟩ at (k−1) step is successfully
generated: that is, we have
Pr(k-th step success |Ψk) =
∥Fk−1 |Ψk−1⟩∥2
(|zk−1| + ∥w∥1)2
. (48)
Thus, the success probability at K step is given by
Pr(QSP success) =
K Y
k=1
Pr(k-th step success | Ψk−1) =
∥
QK
k=1 Fk−1 |Ψ0⟩∥2
QK
k=1(|zk−1| + ∥w∥1)2K
. (49)
Suppose that the probability in Eq. (48) can be bounded by 1 − q with q ∈ (0,1], then we have
Pr(QSP success) ≤ (1 − q)2K, indicating an exponential hardness of successful post-selection.
To address these limitations, we turn to our proposal, DB-QSP. Unlike LCU, DB-QSP constructs
deterministic unitary operations that implement the desired state transformations without requiring
post-selection and auxiliary qubits. This approach could improve the preprocessing initialization for
QSP, reducing the overall hardware runtime by eliminating the need for post-selection.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 20B Proofs of Lem. 1 and Thm. 2
B.1 Proof of Lem. 1
For completeness, we restate the statement from the main text.
Lemma B.1 (Unitary synthesis for linear polynomials without post-selection). Suppose p(H) =
H − αI is any linear polynomial of a Hermitian matrix H with α ∈ R. Given a state vector |Ψ⟩ with
energy mean EΨ = ⟨Ψ|H |Ψ⟩ and variance VΨ = ⟨Ψ|H2 |Ψ⟩−E2
Ψ, the unitary synthesis for the action
of p(H) can be achieved by
UΨ = esΨ[Ψ,H]
, (50)
with
sΨ =
−1
√
VΨ
arccos


EΨ − α
q
VΨ + (EΨ − α)2

. (51)
Proof of Lem. B.1. Firstly, let us verify that UΨ is indeed a unitary operator. For a matrix of the
form eW to be unitary, W must be anti-Hermitian, i.e., W = −W†. Since [Ψ,H] = −([Ψ,H])†, the
operator in Eq. (50) is therefore unitary.
Next, we demonstrate that the unitary operator eWH with WH = [Ψ,H] can be exactly represented
by a linear polynomial when applied to the input state |Ψ⟩. By definition, the unitary operator can
be expressed as
esWH
=
∞ X
k=0
sk
k!
Wk
H . (52)
Now, we observe that
WH |Ψ⟩ = EΨ |Ψ⟩ − H |Ψ⟩, (53)
and
W2
H |Ψ⟩ = EΨWH |Ψ⟩ − WHH |Ψ⟩ = E2
Ψ |Ψ⟩ − EΨH |Ψ⟩ − ⟨Ψ|H2
|Ψ⟩|Ψ⟩ + EΨH |Ψ⟩ = −VΨ |Ψ⟩.
This indicates that any even power of the commutator WH acting on the state |Ψ⟩ gives
W2k
H |Ψ⟩ = (−VΨ)k
|Ψ⟩ . (54)
Similarly, we have W2k+1
H |Ψ⟩ = (−VΨ)kWH |Ψ⟩ for the cases of odd powers. Thus, by separating the
odd and even terms, we obtain a weighted sum of |Ψ⟩ and WH |Ψ⟩ with coefficients expressed by sine
and cosine functions as
esWH
|Ψ⟩ = cos

s
p
VΨ

|Ψ⟩ +
sin s
√
VΨ

√
VΨ
WH |Ψ⟩ . (55)
Using Eq. (53), this simplifies to esWH |Ψ⟩ = (a(s)I + b(s)H)|Ψ⟩, where a(s),b(s) are real-valued
coefficients for any s ∈ R:
a(s) =
EΨ
√
VΨ
sin

s
p
VΨ

+ cos

s
p
VΨ

, b(s) = −
1
√
VΨ
sin

s
p
VΨ

. (56)
Finally, an explicit calculation reveals that the ansatz for the duration Eq. (51) solves the equations
a(sΨ) = −α/∥p(H)|Ψ⟩∥ and b(sΨ) = 1/∥p(H)|Ψ⟩∥ where we utilize the equality
∥p(H)|Ψ⟩∥ =
q
VΨ + (EΨ − α)2
. (57)
The proof is concluded by noting that this means that
esΨWH
|Ψ⟩ =
(H − αI))|Ψ⟩
∥(H − αI))|Ψ⟩∥
. (58)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 21B.2 Useful Preliminary Results
In this section, we derive an exact formula for implementing an exponential of commutators, es[Ψ,H],
without any approximation or truncation error.
B.2.1 Effective Idempotence of Exponentials of [Ω,H]
We derive an equivalent expression of the unitaries es[Ω,H] found in Eq. (50), involving pure states Ψ
and the problem Hamiltonian H. We start with the general Taylor series of the exponential of an
operator
es[Ψ,H]
=
∞ X
k=0
sk
k!
([Ψ,H])k
, (59)
where all k-th powers of s[Ψ,H] contribute to the unitary. In general, one may approximate this
infinite series expansion by truncating it to a degree-K polynomial,
es[Ψ,H]
≈
K X
k=0
sk
k!
([Ψ,H])k
. (60)
However, the error O(sK+1) requires additional care and investment of resources to control. Interest-
ingly, we prove in Prop. B.2 that when Ψ is a pure state, an exact polynomial representation can be
obtained with K = 2, rather than an approximation.
Proposition B.2 (Effective idempotence). Let Ψ = |Ψ⟩⟨Ψ| be a pure density matrix associated to
state vector |Ψ⟩ with energy fluctuation VΨ = ⟨Ψ|H2 |Ψ⟩ − ⟨Ψ|H |Ψ⟩2
. Then for any duration s ∈ R
we have
es[Ψ,H]
= I + A(s)[Ψ,H] + B(s)([Ψ,H])2
(61)
where
A(s) =
sin s
√
VΨ

√
VΨ
, B(s) =
1 − cos s
√
VΨ

VΨ
. (62)
Proof. We will make a technical calculation showing that third power of the commutator is, in fact,
directly proportional to the first power of the commutator, with a scaling factor that depends on
energy fluctuation:
([Ψ,H])3
= −VΨ [Ψ,H] . (63)
We call this effective idempotence. Indeed, in general an operator W is indempotent if W2 = 1 which
implies that esW = cos(s)I + sin(s)W. Here we have the form A3 = αA with α ∈ R, similar to
idempotence. Effective idempotence has analogous consequences for the solution to the exponential
series. It implies that the (2k+1)-th power and the 2k-th power of the commutator can be written as
([Ψ,H])2k+1
= (−VΨ)k
[Ψ,H] , ([Ψ,H])2k
= (−VΨ)k−1
([Ψ,H])2
. (64)
Thus we find for the series of representation of the unitary
es[Ψ,H]
= I +
X
k=0
(−1)k s2k+1 (VΨ [H])k
(2k + 1)!
!
[Ψ,H] +
X
k=1
(−1)k−1 s2k (VΨ [H])k−1
(2k)!
!
([Ψ,H])2
= I + A(s)[Ψ,H] + B(s)([Ψ,H])2
,
(65)
where A(s),B(s) defined in Eq. (62), and we have utilized the Taylor series for sine and cosine in the
last equality. We complete the proof by deriving the effective idempotence namely
([Ψ,H])3
= (ΨH − HΨ)3
=

ΨHΨH − ΨH2
Ψ − HΨH + HΨHΨ

(ΨH − HΨ) (66)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 22where we have used the assumption that the quantum state is pure, i.e., Ψ2 = Ψ. Next, we switch
from density matrix representation to state vector representation, i.e. we substitute back Ψ = |Ψ⟩⟨Ψ|.
Thus, it becomes
([Ψ,H])3
=

⟨H⟩(ΨH + HΨ) − HΨH − ⟨H2
⟩Ψ

(ΨH − HΨ)
= ⟨H⟩(ΨHΨH + HΨH) − HΨHΨH − ⟨H2
⟩ΨH
− ⟨H⟩

ΨH2
Ψ + HΨHΨ

+ HΨH2
Ψ + ⟨H2
⟩ΨHΨ ,
where we introduce the notation ⟨H⟩ = ⟨Ψ|H |Ψ⟩ and ⟨H2⟩ = ⟨Ψ|H2 |Ψ⟩ in the first line, and the
second equality is a direct expansion. Finally, we repeat the same procedure and the result is given
by
([Ψ,H])3
= ⟨H⟩(⟨H⟩ΨH + HΨH) − ⟨H⟩HΨH − ⟨H2
⟩ΨH
− ⟨H⟩

⟨H2
⟩Ψ + ⟨H⟩HΨ

+ ⟨H2
⟩HΨ + ⟨H2
⟩⟨H⟩Ψ (67)
= ⟨H⟩2
ΨH − ⟨H2
⟩ΨH − ⟨H⟩2
HΨ + ⟨H2
⟩HΨ (68)
= −

⟨H2
⟩ − ⟨H⟩2

[Ψ,H] = −(VΨ [H])[Ψ,H], (69)
where we again use the pure state assumption in the first equality and the definition of VΨ in the last
equality.
B.2.2 Exponentials of [Ψ,H] Can Express the Normalized Action of Any Real-Valued Linear Polynomial
in H
We next extend Lem. 1 to operators of the form xI + yH, where x,y ∈ R are not both zero.
Lemma B.3. Let x,y ∈ R and (x,y) ̸= (0,0). Define the parameter
sΨ = −
sgn(y)
√
VΨ
arccos

x + yEΨ
∥(xI + yH)|Ψ⟩∥

. (70)
Then,
(xI + yH)|Ψ⟩
∥(xI + yH)|Ψ⟩∥
= (a(sΨ)I + b(sΨ)H)|Ψ⟩ , (71)
where a(sΨ),b(sΨ) are real-valued coefficients given by
a(sΨ) =
EΨ
√
VΨ
sin

sΨ
p
VΨ

+ cos

sΨ
p
VΨ

, (72)
b(sΨ) = −
1
√
VΨ
sin

sΨ
p
VΨ

. (73)
Proof. We here consider to match the weights of I and H between the polynomial operation and
exponentials of [Ψ,H]. Specifically, we solve the following two equations;
x
∥(xI + yH)|Ψ⟩∥
=
EΨ
√
VΨ
sin

s
p
VΨ

+ cos

s
p
VΨ

, (74)
y
∥(xI + yH)|Ψ⟩∥
= −
1
√
VΨ
sin

s
p
VΨ

. (75)
By computing Eq. (74)+EΨ×Eq. (75), we get
x + yEΨ
∥(xI + yH)|Ψ⟩∥
= cos

sΨ
p
VΨ

. (76)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 23Thus, computing the inverse of the cosine function yields the desired solution. However, since both
sΨ and −sΨ satisfy the equation, the sign must be determined explicitly. Eq. (75) indicates that the
sign of sin(sΨ
√
VΨ) is given by −sgn(y). This leads to the expression for the duration sΨ shown in
Eq. (70).
We lastly verify that this solution is consistent. By substituting Eq. (70) into Eq. (73), we find
b(sΨ) =
sgn(y)
√
VΨ
sin

arccos

x + yEΨ
∥(xI + yH)|Ψ⟩∥

. (77)
Applying sin(x) =
p
1 − cos2(x) further reveals that
b(sΨ) =
sgn(y)
√
VΨ
s
1 −
(x + yEΨ)2
∥(xI + yH)|Ψ⟩∥2
. (78)
With the identity ∥(xI + yH)|Ψ⟩∥2 = (x + yEΨ)2 + y2VΨ, this simplifies to
b(sΨ) =
sgn(y)
√
VΨ
|y|
√
VΨ
∥(xI + yH)|Ψ⟩∥
(79)
=
y
∥(xI + yH)|Ψ⟩∥
. (80)
Similarly, we use the relation a(sΨ) = −EΨb(sΨ) + cos sΨ
√
VΨ

, which gives
a(sΨ) =
−yEΨ
∥(xI + yH)|Ψ⟩∥
+
x + yEΨ
∥(xI + yH)|Ψ⟩∥
(81)
=
x
∥(xI + yH)|Ψ⟩∥
. (82)
B.3 Proof of Thm. 2
We again restate Thm. 2 in the main text.
Theorem B.4 (Unitary synthesis for QSP without post-selection). Suppose an input state |Ψ0⟩ and
any polynomial p(H) of degree K for a given Hermitian matrix H in the form of Eq. (15). Given
energy mean Ek = ⟨Ψk|H |Ψk⟩ and variance Vk = ⟨Ψk|H2 |Ψk⟩ − E2
k, the unitary synthesis for p(H)
can be achieved by
p(H)|Ψ0⟩
∥p(H)|Ψ0⟩∥
=
K−1 Y
k=0
eiθkΨk
esk[Ψk,H]
|Ψ0⟩, (83)
with
sk =
−1
√
Vk
arccos
|Ek − zk|
p
Vk + |Ek − zk|2
!
, and θk = arg

Ek − zk
|Ek − zk|

. (84)
Here, we recursively define the state |Ψk⟩ as |Ψk+1⟩ = eiθkΨkesk[Ψk,H] |Ψk⟩.
Proof. Let zk be the roots of p(H) as in Eq. (15). We iterate over the roots and at each step k, we
will find θk and sk such that the unitary Uk = eiθkΨkesk[Ψk,H] will implement the state
|Ψk+1⟩ =
(H − zkI)|Ψk⟩
∥(H − zkI)|Ψk⟩∥
(85)
as |Ψk+1⟩ = Uk |Ψk⟩. Let us comment that, if we apply the k-th filter fragment Fk = H − zkI, the
normalization is given by
∥(H − zkI)|Ψ⟩∥ = VΨ + |EΨ − zk|2
. (86)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 24We cannot use Lem. 1 directly because in general zk ∈ C, while polynomials with only real roots
such as Chebyshev polynomials can be realized by directly applying Lem. 1. Instead, in general cases,
we associate to zk the real number
uk = Ek − |Ek − zk| (87)
which is real and using Lem. 1 we set sk such that
esk[Ψk,H]
|Ψk⟩ =
(H − ukI)|Ψk⟩
∥(H − ukI)|Ψk⟩∥
. (88)
We define θk to be within [0,2π) and satisfy eiθk = Ek−zk
|Ek−zk|. We next observe that using that Ψk is
pure we have the form eiθkΨk = I + (eiθk − 1)Ψk, we get the following expression
|Ψk+1⟩ =
(I + (eiθk − 1)Ψk)(H − ukI)|Ψk⟩
∥(H − ukI)|Ψk⟩∥
=
(H + eiθk(Ek − uk)I − EkI)|Ψk⟩
∥(H − ukI)|Ψk⟩∥
. (89)
The definitions above were such that eiθk(Ek − wk) = Ek − zk which leads to a cancellation and
|Ψk+1⟩ =
(H − zkI)|Ψk⟩
∥(H − ukI)|Ψk⟩∥
. (90)
Here the numerator involves zk as desired but the norm is an expression involving wk. We have
∥(H − ukI)|Ψk⟩∥ = Vk + E2
k − 2ukEk + u2
k = Vk + (Ek − uk)2
, (91)
which means that, using Eq. (87), we arrive at the form in Eq. (86)
∥(H − ukI)|Ψk⟩∥ = Vk + |Ek − zk|2
= ∥(H − zkI)|Ψk⟩∥ . (92)
Thus the norms match and we conclude that the unitaries implement the desired action of Fk =
H − zkI.
We conclude this section by discussing the range of sk, which is relevant for analyzing implementation
costs and circuit depth. As shown in Eq. (84), the duration sk is given by
sk =
−1
√
Vk
arccos
|Ek − zk|
p
Vk + |Ek − zk|2
!
. (93)
First, to see if |sk| is a decreasing function with respect to Vk we differentiate the two components
g(Vk) =
√
Vk and f(Vk) = arccos

|Ek−zk|
√
Vk+|Ek−zk|2

;
g′
(Vk) =
1
2
√
Vk
(94)
f′
(Vk) = −
1
s
1 −

|Ek−zk|
√
Vk+|Ek−zk|2
2
·
|Ek − zk|
p
Vk + |Ek − zk|2
!′
=
|Ek − zk|
2
√
Vk(Vk + |Ek − zk|2)
(95)
where we used (arccos(y))′ = −1/
p
1 − y2. Thus, using quotient rule, we have
(|sk|)′
=
f′(Vk)g(Vk) − g′(Vk)f(Vk)
g2(Vk)
=
1
Vk
1
2
|Ek − zk|
Vk + |Ek − zk|2
−
1
2
1
√
Vk
arccos
|Ek − zk|
p
Vk + |Ek − zk|2
!!
.
(96)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 25Next we define x =
|Ek − zk|
p
Vk + |Ek − zk|2
= cos(α) which implies that
1
√
Vk
=
x
|Ek − zk|
1
√
1 − x2
and so
we find
(|sk|)′
=
x
2Vk|Ek − zk|

x −
1
√
1 − x2
arccos(x)

(97)
=
x
2Vk|Ek − zk|

cos(α) −
α
sin(α)

(98)
=
x
2Vk|Ek − zk|
1
2 sin(2α) − α
sin(α)
(99)
=
x
4Vk|Ek − zk|
sin(2α) − 2α
sin(α)
≤ 0 , (100)
where we use the fact sinx ≤ x in the last line. Then, the maximum value of sk arises when Vk = 0.
However, since Vk appears in the denominator, we cannot simply compute the value of sk at Vk = 0.
Thus, we apply the L’Hôpital’s rule, we get
lim
Vk→0
|sk| = lim
Vk→0
f′(Vk)
g′(Vk)
=
|Ek − zk|
Vk + |Ek − zk|2
Vk=0
=
1
|Ek − zk|
. (101)
Thus, the duration |sk| is upper-bounded by 1/|Ek − zk|.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 26C Notions of Stability for Unitary Synthesis of Exact Formula in Thm. 2
In this section we explore the unitary synthesis of Thm. 2 in more detail. in Sec. C.1 we prove that
discretizations using group commutator approximation can converge to the desired QSP.
We then analyze the sensitivity of the exact formula in Thm. 2 to perturbations in the input
parameters. We begin by studying a question similar to an existing stability result for QSP using
block-encodings. Concretely, the output of QSP synthesis using qubitization will depend on any errors
in the block-encoding of the input operator H. This enjoys a certain degree of stability; namely, given
block-encodings of H and H′ for ∥H∥ ≤ 1, ∥H′∥ ≤ 1, their transformed block-encodings are also close,
∥p(H) − p(H′)∥ ≤ 4K∥H − H′∥ [3]. In Sec. C.2, we derive a bound in this scenario.
We then focus on the impact of imperfect parameters θ and s on the performance. In Sec. C.3,
we first analyze the impact of deviations in the parameters from their ideal values. However, this
analysis alone is insufficient for practical scenarios, as statistical errors arise when estimating energy
and variance from a noisy state. To address limitation, we extend the results to the situation where
the estimated energy and variance may still differ from their ideal values even in the limit of finite
measurement shots. Sec. C.4 explores this extension, beginning with the single-step case before gen-
eralizing to arbitrary steps. These results provide insight into the statistical estimation requirements
necessary for achieving a converging QSP synthesis.
Hence, we further extend the result to the case where the statistical noise happens when the energy
and variance is different from the ideal situation even if we have the infinite number of measure-
ment shots. To address this, Sec. C.4 starts with a single-step case, followed by the arbitrary steps.
This result sheds light on the demands of statistical estimation required to obtain a converging QSP
synthesis.
C.1 Convergence of DB-QSP
Proposition C.1 (DB-QSP convergence). Suppose H is a Hermitian matrix whose spectral radius
does not exceed unity, i.e., ∥H∥ ≤ 1. Let ζ = max(θ,s) be the maximum value across all elements
in θ = (θ0,...,θK−1) and s = (|s0|,...,|sK−1|). For the analysis, we define the state constructed by
DB-QSP with s(N)
k =
p
|sk|/N
|ωK⟩ =
K−1 Y
k=0
eiθkωk

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
|ω0⟩ (102)
We also define the exact QSP state derived from Thm. 2
|Ψ(θ,s)⟩ =
K−1 Y
k=0
eiθkΨk
esk[Ψk,H]
|Ψ0⟩ . (103)
Then we have
∥|Ψ(θ,s)⟩ − |ωK⟩∥ ≤
4
3
s
ζ
N
(1 + 6ξ)K
. (104)
Proof. Let us define the intermediate QSP states as
|Ψk⟩ =
k−1 Y
k′=0
eiθk′Ψk′
esk′[Ψk′,H]
|Ψ0⟩ (105)
and the intermediate DB-QSP states as
|ωk+1⟩ = eiθkωk

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
|ωk⟩ . (106)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 27Section Main Focus Proof Final Results
Sec. C.1 Difference between
the exact formula in
Thm. 2 and DB-QSP
Prop. C.1
∥|Ψ(θ,s)⟩ − |ωK⟩∥ ≤
4
3
s
ζ
N
(1 + 6ξ)K
.
Sec. C.2 Stability with
respect to the differ-
ence in Hamiltonians
Prop. C.2
|Ψθ,s(H)⟩ − |Ψθ,s(H̃)⟩ ≤
1
3
(1 + 6ζ)K
∥H − H̃∥ .
Sec. C.3 Sensitivity to
changes from the
exact angles θ and s
Prop. C.3
∥|ΨH(θ,s)⟩ − |Ψ̃H(θ̃,s̃)⟩∥ ≤
max(δs,δθ)
3ζ
(1 + 6ζ)K
.
Sec. C.4 Error in a single step
caused by erroneous
estimation of energy
and variance
Prop. C.4
eiθΨΨ
esΨ[Ψ,H]
|Ψ⟩ − eiθΨ
esΨ[Ψ,H]
|Ψ⟩ ≤ 20η4
max(δV ′,δE′)
Sec. C.4 Error in K steps
using the estimated
QSP parametriza-
tion (θ,s)
Prop. C.5
∥|ΨH(θ,s)⟩ − |ΨH(θ,s)⟩∥ ≤ (14 + 120η4
)K
max(δV ,δE) .
Table 1: Summary of the results explored in this section. Props. C.1 and C.5 are the key results, but the other
derivations should be helpful in understanding their proof. For notation, please refer to the corresponding sections.
In addition, we introduce the shorthand δE′ = |EΨ − E′
| and δV ′ = |VΨ − V ′
| in this table.
First, we decompose the difference between the updated QSP states and the DB-QSP states as follows:
∥|Ψk+1⟩ − |ωk+1⟩∥ =∥eiθkΨk
esk[Ψk,H]
|Ψk⟩ − eiθkωk

eis̃kωk
eis̃kH
e−is̃kωk
e−is̃kH
N
|ωk⟩∥ (107)
=

eiθkΨk
esk[Ψk,H]
|Ψk⟩ − eiθkωk
esk[Ψk,H]
|Ψk⟩

+

eiθkωk
esk[Ψk,H]
|Ψk⟩ − eiθkωk
esk[ωk,H]
|Ψk⟩

+

eiθkωk
esk[ωk,H]
|Ψk⟩ − eiθkωk
esk[ωk,H]
|ωk⟩

+ eiθkωk
esk[ωk,H]
|ωk⟩ − eiθkωk

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
|ωk⟩
!
(108)
≤∥

eiθkΨk
− eiθkωk

esk[Ψk,H]
|Ψk⟩∥
+ ∥eiθkωk

esk[Ψk,H]
− esk[ωk,H]

|Ψk⟩∥
+ ∥eiθkωk
esk[ωk,H]
(|Ψk⟩ − |ωk⟩)∥
+ ∥eiθkωk
esk[ωk,H]
−

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
!
|ωk⟩∥ (109)
where we use triangle inequality to obtain the last inequality. Next, we evaluate these terms separately.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 281. Using the definition of the operator norm
∥

eiθkΨk
− eiθkωk

esk[Ψk,H]
|Ψk⟩∥ ≤ ∥eiθkωk
− eiθkΨk
∥ ≤ |θk|∥Ψk − ωk∥ (110)
where we utilize the inequality ∥eA − eB∥ ≤ ∥A − B∥ for unitary operator and the fact ∥AB∥ ≤
∥A∥∥B∥. Moreover, note that ∥Ψk − ωk∥ ≤ 2∥|Ψk⟩ − |ωk⟩∥ and thus we obtain
∥

eiθkΨk
− eiθkωk

esk[Ψk,H]
|Ψk⟩∥ ≤ 2|θk|∥|Ψk⟩ − |ωk⟩∥ (111)
2. For the second term, we have
∥eiθkωk

esk[Ψk,H]
− eiθkωk

esk[ωk,H]
|Ψk⟩∥ ≤ ∥eiθkωk
∥ · ∥

esk[Ψk,H]
− esk[ωk,H]

|Ψk⟩∥ (112)
≤ ∥esk[Ψk,H]
− esk[ωk,H]
∥ (113)
≤ |sk|∥[Ψk − ωk,H]∥ (114)
where we again employ the unitary invariance and normalised state assumption in the second line;
and the property ∥eA−eB∥ ≤ ∥A−B∥ in the last line. Next, using the bound ∥[A,B]∥ ≤ 2∥A∥∥B∥,
it can be further simplified to
∥eiθkωk

esk[Ψk,H]
− eiθkωk

esk[ωk,H]
|Ψk⟩∥ ≤ 2|sk|∥Ψk − ωk∥ · ∥H∥ (115)
Similar to the first term, employing the bound ∥Ψk − ωk∥ ≤ 2∥|Ψk⟩ − |ωk⟩∥ and the assumption
that ∥H∥ ≤ 1, we get
∥eiθkωk

esk[Ψk,H]
− eiθkωk

esk[ωk,H]
|Ψk⟩∥ ≤ 4|sk|∥|Ψk⟩ − |ωk⟩∥ (116)
3. For the third term, since eiθkωk esk[ωk,H] is unitary operator, the third term can be simplified to
∥eiθkωk
esk[ωk,H]
(|Ψk⟩ − |ωk⟩)∥ ≤ ∥|Ψk⟩ − |ωk⟩∥ (117)
where we use the unitary invariance property of norm.
4. Finally, for the fourth term, it becomes
∥eiθkωk
esk[ωk,H]
−

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
!
|ωk⟩∥
≤ ∥esk[ωk,H]
−

eis̃kωk
eis̃kH
e−is̃kωk
e−is̃kH
N
∥ (118)
Using upper bound in Lemma. (9) from [17] by replacing sk → s(N)
k , we have
eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
− es
(N)
k
[ωk,H]
≤ |sk|3/2
N−3/2

∥[H,[H,ωk]]∥ + ∥[ωk,[ωk,H]]∥

,
(119)
By the definition of s(N)
k and telescoping, we have
∥esk[ωk,H]
−

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
∥
≤ |sk|3/2
/
√
N × (∥[H,[H,ωk]]∥ + ∥[ωk,[ωk,H]]∥) (120)
≤ 2|sk|3/2
/
√
N × (∥[H,ωk]∥ × ∥H∥ + ∥[ωk,H]∥ × ∥ωk∥) (121)
≤ 4|sk|3/2
/
√
N ×

∥ωk∥ × ∥H∥2
+ ∥H∥ × ∥ωk∥2

(122)
where we recall the bound ∥[A,B]∥ ≤ 2∥A∥∥B∥ in the second and third line. Since we assume
that ∥H∥ ≤ 1 and ∥ωk = 1∥, we achieve
∥esk[ωk,H]
−

eis
(N)
k
ωk
eis
(N)
k
H
e−is
(N)
k
ωk
e−is
(N)
k
H
N
∥ ≤ 8|sk|3/2
/
√
N . (123)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 29Collecting all terms, Eq. (109) becomes
∥|Ψk+1⟩ − |ωk+1⟩∥ ≤ (1 + 2|θk| + 4|sk|)∥|Ψk⟩ − |ωk⟩∥ + 8|sk|3/2
/
√
N (124)
≤ (1 + 6ζ)∥|Ψk⟩ − |ωk⟩∥ + 8ζ3/2
/
√
N . (125)
where we use the definition ζ = maxk=1,...,K(θk,sk) to obtain last line. Iterating this recursive bound,
we get
∥|Ψk+1⟩ − |ωk+1⟩∥ ≤
8ζ3/2
√
N
k X
i=0
(1 + 6ζ)i
=
8ζ3/2
√
N
×
(1 + 6ξ)k+1 − 1
(1 + 6ξ) − 1
(126)
≤
4
3
s
ξ
N
(1 + 6ξ)k+1
. (127)
Setting K = k + 1, the proposition statement is justified.
C.2 Perturbation of the Hamiltonian
Using Thm. 2 we define |Ψθ,s(H)⟩ =
QK
k=1 eiθΨkesk[Ψk,H] |Ψ0⟩. This definition indicates that we will
hold the angles θk and sk fixed but consider what happens if the Hamiltonian is perturbed.
Proposition C.2 (QSP task stability). Suppose H is a Hermitian matrix whose spectral radius does
not exceed unity, i.e., ∥H∥ ≤ 1. Let ζ = max(θ,s) be the maximum value across all elements in
θ = (θ0,...,θK−1) and s = (|s0|,...,|sK−1|). Then, we have
|Ψθ,s(H)⟩ − |Ψθ,s(H̃)⟩ ≤
1
3
(1 + 6ζ)K
∥H − H̃∥ . (128)
Proof. Let us define the intermediate QSP states
|Ψk⟩ =
k−1 Y
k′=0
eiθk′Ψk′
esk′[Ψk′,H]
|Ψ0⟩ (129)
and analogously |Ψ̃k⟩ are the intermediate states of QSP with H̃. Thus, the difference between |Ψk+1⟩
and |Ψ̃k+1⟩ is given by
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ = ∥eiθkΨk
esk[Ψk,H]
|Ψk⟩ − eiθkΨ̃k
esk[Ψ̃k,H̃]
|Ψ̃k⟩∥ . (130)
Next, following the same procedure in Eq. (109) from Subsec. C.1, we add and subtract the term
{eiθkΨkesk[Ψk,H] |Ψ̃k⟩, eiθkΨ̃kesk[Ψk,H] |Ψ̃k⟩} to split them into multiple norm calculations via triangle
inequality.
Consequently, the result is
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤ ∥|Ψk⟩ − |Ψ̃k⟩∥ + ∥eiθkΨk
− eiθkΨ̃k
∥ + ∥esk[Ψk,H]
− esk[Ψ̃k,H̃]
∥ (131)
≤ ∥|Ψk⟩ − |Ψ̃k⟩∥ + |θk| · ∥Ψk − Ψ̃k∥ + |sk| · ∥[Ψk,H] − [Ψ̃k,H̃]∥ , (132)
where we recall the unitary invariance property of norm in the first inequality and we utilize the
formula ∥eA −eB∥ ≤ ∥A−B∥ in the second inequality. We then simplify these three terms separately.
1. For the first term ∥|Ψk⟩ − |Ψ̃k⟩∥, it remains unchanged.
2. For the second term, it becomes
|θk| · ∥Ψk − Ψ̃k∥ ≤ 2|θk| · ∥|Ψk⟩ − |Ψ̃k⟩∥ , (133)
where we use the relation ∥Ψk − Ψ̃k∥ ≤ 2∥|Ψk⟩ − |Ψ̃k⟩∥.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 303. For the third term, we rewrite it as
|sk| · ∥[Ψk,H] − [Ψ̃k,H̃]∥ = |sk| · ∥ΨkH − HΨk −

Ψ̃kH̃ − H̃Ψ̃k

∥ (134)
= |sk| · ∥ΨkH − ΨkH̃ + ΨkH̃ − Ψ̃kH̃ − HΨk + HΨ̃k − HΨ̃k + H̃Ψ̃k∥
(135)
= |sk| · ∥Ψk (H − H̃) +

Ψk − Ψ̃k

H̃ − H

Ψk − Ψ̃k

− (H − H̃)Ψ̃k∥ .
(136)
By triangle inequality and operator norm’s definition, we obtain
|sk| · ∥[Ψk,H] − [Ψ̃k,H̃]∥ ≤ 2|sk| · ∥Ψk − Ψ̃k∥ · ∥H∥ + 2|sk| · ∥H − H̃∥ . (137)
Similarly, using ∥Ψk − Ψ̃k∥ ≤ 2∥|Ψk⟩ − |Ψ̃k⟩∥, it becomes
∥[Ψk,H] − [Ψ̃k,H̃]∥ ≤ 4|sk| · ∥|Ψk⟩ − |Ψ̃k⟩∥ + 2|sk| · ∥H − H̃∥ . (138)
Collecting all the terms, Eq. (132) reduces to
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤ (1 + 2|θk| + 4|sk|)∥|Ψk⟩ − |Ψ̃k⟩∥ + 2|sk| · ∥H − H̃∥ (139)
≤ (1 + 6ζ)∥|Ψk⟩ − |Ψ̃k⟩∥ + 2|sk| · ∥H − H̃∥ , (140)
where we use the definition ζ = max(θ,s) in the last line. Finally, iterating this recursive bound and
it yields
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤
|sk| · ∥H − H̃∥
3ζ
(1 + 6ζ)k+1
≤
1
3
∥H − H̃∥(1 + 6ζ)k+1
, (141)
where we again used the definition ζ = max(θ,s) , i.e.
|sk|
ζ
≤ 1. Setting K = k +1, the proposition’s
statement is justified.
C.3 Perturbation of Angles
In order to study sensitivity of the parametrization in Thm. 2 we define
|ΨH(θ,s)⟩ =
K−1 Y
k=0
eiθΨk
esk[Ψk,H]
|Ψ0⟩ . (142)
In practice, we first measure the energy and variance, then compute and then compute sk and θk to
implement the operation. From this perspective, the time duration sk and phase θk vary at each step;
that is, the perturbations satisfy |sk − s̃k| ≤ δs and |θk − θ̃k| ≤ δθ. In other words, even if the unitary
implementation is perfect, the determined values for time duration and phase can cause errors.
Under this setting, we establish an error bound for implementing a non-unitary polynomial of degree
K. For simplicity, we assume the errors in time duration and phase remain constant across all steps. In
what follows, we denote the ideal state and operations as |Ψk+1⟩ and eiθkΨkesk[Ψk,H], whereas erroneous
counterparts are given by eiθ̃kΨ̃kes̃k[Ψ̃k,H]. Finally, we note that no group commutator approximation
is performed in this analysis.
Proposition C.3 (QSP parametrization stability). Let H be a Hermitian matrix such that ∥H∥ ≤ 1,
and assume that the estimated parameters s̃k and θ̃k satisfy |sk −s̃k| ≤ δs and |θk −θ̃k| ≤ δθ with ideal
parameters sk and θk for all k. By setting ζ = max(θ,s), the perturbed state |Ψ̃H(θ̃,s̃)⟩ in Eq. (32)
and the state |ΨH(θ,s)⟩ from Thm. 2 satisfies
∥|ΨH(θ,s)⟩ − |Ψ̃H(θ̃,s̃)⟩∥ ≤
1
3ζ
(1 + 6ζ)K
max(δs,δθ) . (143)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 31Proof. Let us define the intermediate QSP states
|Ψk⟩ =
k−1 Y
k′=0
eiθk′Ψk′
esk′[Ψk′,H]
|Ψ0⟩ (144)
and analogously |Ψ̃k⟩ are the intermediate states of QSP with θ̃k and s̃k. The difference between
|Ψk+1⟩ and |Ψ̃k+1⟩ is given by
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ = ∥eiθkΨk
esk[Ψk,H]
|Ψk⟩ − eiθ̃kΨ̃k
es̃k[Ψ̃k,H]
|Ψ̃k⟩∥ . (145)
Again, following the same procedure in Eq. (109) from Subsec. C.1, we add and subtract the term
{eiθkΨkesk[Ψk,H] |Ψ̃k⟩, eiθkΨ̃kesk[Ψk,H] |Ψ̃k⟩, eiθkΨ̃kesk[Ψ̃k,H] |Ψ̃k⟩}, eiθ̃kΨ̃kesk[Ψ̃k,H] |Ψ̃k⟩} to split them
into multiple norm calculation via triangle inequality. Therefore, the result is
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤ ∥|Ψk⟩ − |Ψ̃k⟩∥ + ∥eiθkΨk
− eiθkΨ̃k
∥ + ∥esk[Ψk,H]
− esk[Ψ̃k,H]
∥
+ ∥eiθkΨ̃k
− eiθ̃kΨ̃k
∥ + ∥esk[Ψ̃k,H]
|Ψ̃k⟩ − es̃k[Ψ̃k,H]
|Ψ̃k⟩∥ (146)
≤ ∥|Ψk⟩ − |Ψ̃k⟩∥
+ |θk| · ∥Ψk − Ψ̃k∥
+ |sk| · ∥[Ψk − Ψ̃k,H]∥
+ |θk − θ̃k|
+ ∥

esk[Ψ̃,H]
− es̃k[Ψ̃,H]

|Ψ̃k⟩∥ , (147)
where we use the formula ∥eA −eB∥ ≤ ∥A−B∥ in the second inequality. Next, we proceed to evaluate
these terms separately.
1. For the first term ∥|Ψk⟩ − |Ψ̃k⟩∥, it remains unchanged.
2. For the second term, it becomes
|θk| · ∥Ψk − Ψ̃k∥ ≤ 2|θk| · ∥|Ψk⟩ − |Ψ̃k⟩∥ , (148)
where we use the relation ∥Ψk − Ψ̃k∥ ≤ 2∥|Ψk⟩ − |Ψ̃k⟩∥.
3. For the third term, it is
|sk| · ∥[Ψk − Ψ̃k,H]∥ ≤ 2|sk| · ∥Ψk − Ψ̃k∥ · ∥H∥ (149)
≤ 4|sk| · ∥|Ψk⟩ − |Ψ̃k⟩∥ , (150)
where we use the bound ∥[A,B]∥ ≤ 2∥A∥∥B∥ in the first line and the relation ∥Ψk − Ψ̃k∥ ≤
2∥|Ψk⟩ − |Ψ̃k⟩∥. Note that we also exploited the assumption that ∥H∥ ≤ 1 in the second line.
4. For the fourth term, we recall the definition of δθ, i.e. |θk − θ̃k| ≤ δθ.
5. For the fifth term, we observe that
es̃[Ψ,H]
|Ψ̃k⟩ =

EΩ
√
VΩ
sin(s̃
p
VΩ) + cos(s̃
p
VΩ)

I −
1
√
VΩ
sin(s̃
p
VΩ)H

|Ψ̃k⟩
= cos(δs
p
VΩ)

es[Ψ,H]
|Ψ̃k⟩

+ sin(δs
√
V Ω)

e(s+π/2
√
VΩ)[Ψ,H]
|Ψ̃k⟩

.
(151)
Using this expression, the fifth term can be simplified to
∥es̃[Ψ,H]
|Ψ⟩ − es[Ψ,H]
|Ψ⟩∥ =
q
2 − 2|⟨Ψ|es̃[Ψ,H]e−s[Ψ,H]|Ψ⟩|
=
q
2 − 2|cos(δs
p
VΩ)|
=
r
4 − 4|cos2(δs
q
VΩ/2)| = 2|sin(δs
p
VΩ/2)| ≤ δs
p
VΩ,
(152)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 32Using the fact that
p
VΨk
≤ ∥H∥ and the assumption that ∥H∥ ≤ 1 , we have
∥es̃[Ψ,H]
|Ψ⟩ − es[Ψ,H]
|Ψ⟩∥ ≤ δs . (153)
Collecting all the terms, Eq. (147) reduces to
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤ (1 + 2|θk| + 4|sk|)∥|Ψk⟩ − |Ψ̃k⟩∥ + δθ + δs (154)
≤ (1 + 6ζ)∥|Ψk⟩ − |Ψ̃k⟩∥ + 2γ. (155)
where we utilize the definition of γ in the last line, i.e. γ = max(δs,δθ). Now, solving the iterative
sequence, we get
∥|Ψk+1⟩ − |Ψ̃k+1⟩∥ ≤ 2γ
k X
i=0
(1 + 6ζ)i
= 2γ
1 − (1 + 6ζ)k+1
1 − (1 + 6ζ)
≤
γ
3ζ
(1 + 6ζ)k+1
. (156)
Setting K = k + 1, the proposition statement is justified.
C.4 Statistical Error Propagation
In this section, we study sensitivity of the parametrization in Thm. 2 to estimation errors of the energy
and variance. More precisely, for k = 0,...K − 1, we define the energy Ek and the variance V k for
states |Ψk⟩, which is recursively determined by
|Ψk+1⟩ = eiθkΨk
esk[Ψk,H]
|Ψk⟩ , (157)
with
sk =
−1
q
V k
arccos


Ek − u
q
V k + (Ek − u)2

 (158)
and
θk = arg
Ek − zk
|Ek − zk|
!
. (159)
With this, the final state reads
|ΨH(θ,s)⟩ =
K−1 Y
k=0
eiθkΨk
esk[Ψk,H]
|Ψ0⟩ . (160)
Note that, while Prop. C.3 characterizes the sensitivity to differences in parameters sk and θk, its
direct application to analyzing the impact of statistical estimates is non-trivial. To address this, we
establish a lemma that circumvents this challenge by directly considering the relevant quantum states.
In the analysis, we define
s(E,V ) =
−1
√
V
arccos
|E − z|
p
V + |E − z|2
!
(161)
and
θ(E,V ) = arg

E − z
|E − z|

. (162)
for any E ∈ R and V ≥ 0.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 33Proposition C.4 (Statistical error propagation). Suppose H is a Hermitian matrix whose spectral
radius does not exceed unity, i.e., ∥H∥ ≤ 1. Consider the linear polynomial p(H) = H −zI, which we
implement using Thm. 2 for some z ∈ C. Let |Ψ⟩ be a state with energy EΨ and variance VΨ. Then,
for any E′ ∈ R and V ′ ≥ 0, we have
∥

eiθ(EΨ,VΨ)Ψ
es(EΨ,VΨ)[Ψ,H]
− eiθ(E′,V ′)Ψ
es(E′,V ′)[Ψ,H]

|Ψ⟩∥ ≤ 20η4
max(|EΨ − E′
|,|VΨ − V ′
|) ,
(163)
where η = max(
1
√
VΨ
,
1
√
V ′
,
1
|EΨ − z|
,
1
|E′ − z|
,1 + |z|) is the maximal characteristic instability scale.
Proof. For brevity, we define θ = θ(EΨ,VΨ), and θ = θ(E′,V ′), as well as s = s(E,V ) and s =
s(E′,V ′).
First we reduce the problem into two separate bounds
eiθΨ
es[Ψ,H]
|Ψ⟩ − eiθΨ
es[Ψ,H]
|Ψ⟩ ≤ eiθΨ
es[Ψ,H]
|Ψ⟩ − eiθΨ
es[Ψ,H]
|Ψ⟩
+ eiθΨ
es[Ψ,H]
|Ψ⟩ − eiθΨ
es[Ψ,H]
|Ψ⟩ (164)
= eiθΨ
− eiθΨ
+ es[Ψ,H]
|Ψ⟩ − es[Ψ,H]
|Ψ⟩ , (165)
where we use the unitary invariance in the second inequality. Next, we evaluate these two terms
individually.
1. First, by utilizing the fact that Ψ is a pure state, we have
eiθΨ
− eiθΨ
= ∥I + (eiθ
− 1)Ψ −

I + (eiθ
− 1)Ψ

∥ (166)
= |eiθ
− eiθ
| (167)
=
E′ − z
|E′ − z|
−
EΨ − z
|EΨ − z|
(168)
≤ |E′
− z|
1
|E′ − z|
−
1
|EΨ − z|
+
|E′ − EΨ|
|EΨ − z|
(169)
≤ η |EΨ − z| − |E′
− z| + η|E′
− EΨ| (170)
≤ 2η|E′
− EΨ|, (171)
where we utilize the triangle inequality for the forth line, while we use reverse triangle inequality
in the last line.
2. The implementation with s results in es[Ψ,H] |Ψ⟩ = (a(s)I + b(s)H)|Ψ⟩ with
a(s) =
EΨ
√
VΨ
sin

s
p
VΨ

+ cos

s
p
VΨ

, (172)
b(s) = −
1
√
VΨ
sin

s
p
VΨ

. (173)
Recall that the equalities are derived in Lem. 1; see Sec. B for more details. We stress that EΨ
and VΨ could be different from the estimated ones used for determining s. This stands in contrast
to implementing the polynomial which we wanted es[Ψ,H] |Ψ⟩ = (a(s)I + b(s)H)|Ψ⟩ with
a(s) =
EΨ
√
VΨ
sin

s
p
VΨ

+ cos

s
p
VΨ

, (174)
b(s) = −
1
√
VΨ
sin

s
p
VΨ

. (175)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 34With these expressions, we have
es[Ψ,H]
|Ψ⟩ − es[Ψ,H]
|Ψ⟩ = ∥(a(s)I + b(s)H)|Ψ⟩ − (a(s)I + b(s)H)|Ψ⟩∥ (176)
≤ |a(s) − a(s)| + |b(s) − b(s)|∥H∥ (177)
≤ |a(s) − a(s)| + |b(s) − b(s)| . (178)
In the last line, we used the spectral assumption ∥H∥ ≤ 1.
(a) We begin by bounding |b(s) − b(s)| because this will help with the bound for a(s). First,
for ease of notation, we introduce α =
√
VΨs = arccos

|EΨ−z|
√
VΨ+|EΨ−z|2

to denote b(s) =
−sin(α)/
√
VΨ. Similarly, b(s) with the estimated s is expressed using α =
√
V ′s as
b(s) = −
1
√
VΨ
sin
q
VΨ/V ′α

. (179)
Thus, we have
|b(s) − b(s)| =
1
√
VΨ
|sin(
q
VΨ/V ′α) − sin(α)| (180)
≤
1
√
VΨ
|sin(
q
VΨ/V ′α) − sin(α)| +
1
√
VΨ
|sin(α) − sin(α)| . (181)
i. For the first part, using sin(a) − sin(b) = 2sin(a−b
2 )cos(a+b
2 ), we get
1
√
VΨ
|sin(
q
VΨ/V ′α) − sin(α)|
≤
1
√
VΨ
2sin

(
q
VΨ/V ′ − 1)α/2

cos

(
q
VΨ/V ′ + 1)α/2

(182)
≤
π
2
√
VΨ
q
VΨ/V ′ − 1 (183)
≤
π
2
1
√
VΨ
−
1
√
V ′
(184)
≤
π
2
|VΨ − V ′|
√
VΨ
√
V ′(
√
VΨ +
√
V ′)
(185)
≤
π
2
|VΨ − V ′|
VΨ
√
V ′
(186)
≤ 2η3
|VΨ − V ′
|, (187)
where we use cos(x) ≤ 1, sin(x) ≤ x and α ≤ π/2 in the second inequality. As for the
third equality, we utilize
1
√
A
−
1
√
B
=
B − A
√
AB(
√
A +
√
B)
,
while we use 1/(x + y) ≤ 1/x for x > 0 and y > 0 in the fourth inequality.
ii. For the second part, we notice that
sin(α) =
q
1 − |EΨ − z|2/(VΨ + |EΨ − z|2) =
q
VΨ/(VΨ + |EΨ − z|2). (188)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 35with cosα = |EΨ−z|
√
VΨ+|EΨ−z|2
. Hence, we have
1
√
VΨ
|sin(α) − sin(α)|
≤
1
√
VΨ
s
VΨ
VΨ + |EΨ − z|2
−
s
V ′
V ′ + |E′ − z|2
(189)
≤
1
p
VΨ + |E − z|2
−
1
p
V ′ + |E′ − z|2
+
1
√
VΨ
p
V ′ + |E′ − z|2
p
VΨ −
√
V ′ . (190)
The first component is further upper bounded by
1
p
VΨ + |EΨ − z|2
−
1
p
V ′ + |E′ − z|2
≤
|VΨ + |E − z|2 − (V ′ + |E′ − z|2)|
p
VΨ + |E − z|2
p
V ′ + |E′ − z|2(
p
VΨ + |E − z|2 +
p
V ′ + |E′ − z|2)
(191)
≤
|VΨ − V ′| + ||EΨ − z|2 − |E′ − z|2|
|EΨ − z|2|E′ − z|
(192)
≤
|VΨ − V ′|
|EΨ − z|2|E′ − z|
+
2(1 + |z|)|EΨ − E′|
|EΨ − z|2|E′ − z|
(193)
≤ η3
|VΨ − V ′
| + 2η4
|EΨ − E′
| , (194)
where we exploit EΨ+E′ ≤ 2, and |EΨ−z|2−|E′−z|2 ≤ 2(1+|z|)|EΨ−E′| ≤ 2η|EΨ−E′|
because of the assumption ∥H∥ ≤ 1.
Also, the second component is given by
1
√
VΨ
p
V ′ + |E′ − z|2
p
VΨ −
√
V ′ ≤
|VΨ − V ′|
√
VΨ
p
V ′ + |E′ − z|2(
√
V ′ +
√
VΨ)
(195)
≤
|VΨ − V ′|
VΨ|E′ − z|
(196)
≤ η3
|VΨ − V ′
|. (197)
Consequently, we have
1
√
VΨ
|sin(α) − sin(α)| ≤ η3
|VΨ − V ′
| + 2η4
|EΨ − E′
| + η3
|VΨ − V ′
| (198)
≤ 2η3
|VΨ − V ′
| + 2η4
|EΨ − E′
|. (199)
Therefore, the upper bound of |b(s) − b(s)| is expressed as
|b(s) − b(s)| ≤ 2η3
|VΨ − V ′
| + 2η4
|EΨ − E′
| + 2η3
|VΨ − V ′
| (200)
= 4η3
|VΨ − V ′
| + 2η4
|EΨ − E′
|. (201)
(b) Using similar procedure, we arrive at
|a(s) − a(s)| ≤ EΨ|b(s) − b(s)| + |cos(
q
VΨ/V ′α) − cos(α)| + |cos(α) − cos(α)| (202)
≤ |b(s) − b(s)| + |2sin((
q
VΨ/V ′ − 1)α/2)sin((
q
VΨ/V ′ + 1)α/2)|
+ |cos(α) − cos(α)| (203)
≤ |b(s) − b(s)| +
π
2
1
√
VΨ
−
1
√
V ′
|cos(α) − cos(α)| . (204)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 36For the last component, recalling cosα =
|EΨ − z|
p
VΨ + |EΨ − z|2
, we have
|cos(α) − cos(α)|
≤
|EΨ − z|
p
VΨ + |EΨ − z|2
−
|E′ − z|
p
V ′ + |E′ − z|2
(205)
≤ |EΨ − z|
1
p
VΨ + |EΨ − z|2
−
1
p
V ′ + |E′ − z|2
+
||EΨ − z| − |E′ − z||
p
V ′ + |E′ − z|2
(206)
≤ |EΨ − z|
|VΨ − V ′|
|EΨ − z|2|E′ − z|
+
2(1 + |z|)|EΨ − E′|
|EΨ − z|2|E′ − z|
+
|EΨ − E′|
√
V ′
(207)
≤ η2
|VΨ − V ′
| + 2η3
|EΨ − E′
| + η|EΨ − E′
| (208)
= η2
|VΨ − V ′
| + (2η3
+ η)|EΨ − E′
| , (209)
where we use the result Eq. (193) in the third inequality. Hence, we obtain
|a(s) − a(s)| ≤ 4η3
|VΨ − V ′
| + 2η4
|EΨ − E′
| +
π
2
η3
|VΨ − V ′
| + η2
|VΨ − V ′
|
+ (2η3
+ η)|EΨ − E′
| (210)
≤ (6η3
+ η2
)|VΨ − V ′
| + (2η4
+ 2η3
+ η)|EΨ − E′
|. (211)
By substituting Eq. (201) and Eq. (211) into Eq. (178), we have
es[Ψ,H]
|Ψ⟩ − es[Ψ,H]
|Ψ⟩ ≤ (6η3
+ η2
)|VΨ − V ′
| + (2η4
+ 2η3
+ η)|EΨ − E′
| + 4η3
|VΨ − V ′
|
+ 2η4
|EΨ − E′
| (212)
= (10η3
+ η2
)|VΨ − V ′
| + (4η4
+ 2η3
+ η)|EΨ − E′
| (213)
≤ 18η4
max(|VΨ − V ′
|,|EΨ − E′
|) . (214)
where we use 10η3 +η2 ≤ 11η4 and 2η3 +η ≤ 3η4 in the last line since η ≥ 1 by definition. Lastly,
combining Eq. (171) and Eq. (214) leads to the constants claimed above.
Finally, leveraging the techniques developed thus far, we establish a bound on the deviation between
the ideal state and the state affected by noisy estimations of energy and variance in terms of their
statistical errors.
Proposition C.5 (QSP estimation stability). Suppose H is a Hermitian matrix whose spectral ra-
dius does not exceed unity, i.e., ∥H∥ ≤ 1 and consider the polynomial p(H) of degree K with
roots zk satisfying |zk| ≤ |z|. We denote the ideal parameter sequences as θ = (θ0,...,θK−1) and
s = (|s0|,...,|sK−1|), which yield the exact state |ΨH(θ,s)⟩. Similarly, let θ = (θ0,...,θK−1) and
s = (|s0|,...,|sK−1|) be the parameters obtained from statistical estimates of the energy mean and
variance, as used in the states defined in Eq. (157). Also, we define the maximal instability scale
across all states as η = max(
1
√
VΨ
,
1
√
V ′
,
1
|EΨ − z|
,
1
|E′ − z|
,1 + |z|). Then, we have
∥|ΨH(θ,s)⟩ − |ΨH(θ,s)⟩∥ ≤ (14 + 120η4
)K
· max(δV ,δE) = O(max(δV ,δE)) . (215)
where δE ≥ |Ek − Ek| and δV ≥ |Vk − V k| is the statistical errors of energy and variance.
Proof. Let us define the intermediate QSP states
|Ψk⟩ =
k−1 Y
k′=0
eiθk′Ψk′
esk′[Ψk′,H]
|Ψ0⟩ (216)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 37and analogously |Ψk⟩ will be the intermediate states of QSP with θk and sk. Thus, the difference
between |Ψk+1⟩ and |Ψk+1⟩ is given by
∥|Ψk+1⟩ − |Ψk+1⟩∥ = ∥eiθkΨk
esk[Ψk,H]
|Ψk⟩ − eiθkΨk
esk[Ψk,H]
|Ψk⟩∥ (217)
Again, following the same procedure in Eq. (109) from Sec. C.1, we add and subtract the term
{eiθkΨkesk[Ψk,H] |Ψk⟩, eiθkΨkesk[Ψk,H] |Ψk⟩, eiθkΨkesk[Ψk,H] |Ψk⟩}, eiθkΨkesk[Ψk,H] |Ψk⟩} to split them
into multiple norm calculation via triangle inequality. Therefore, the result is
∥|Ψk+1⟩ − |Ψk+1⟩∥ ≤ ∥|Ψk⟩ − |Ψk⟩∥ + ∥eiθkΨk
− eiθkΨk
∥ + ∥esk[Ψk,H]
− esk[Ψk,H]
∥
+ ∥eiθkΨk
− eiθkΨk
∥ + ∥esk[Ψk,H]
|Ψk⟩ − esk[Ψk,H]
|Ψk⟩∥ (218)
≤ ∥|Ψk⟩ − |Ψk⟩∥
+ |θk| · ∥Ψk − Ψk∥
+ |sk| · ∥[Ψk − Ψk,H]∥
+ ∥eiθkΨk
− eiθkΨk
∥
+ ∥

esk[Ψ,H]
− esk[Ψ,H]

|Ψk⟩∥ . (219)
1. For the second term, we recall that ∥Ψk − Ψk∥ ≤ 2∥|Ψk⟩ − |Ψk⟩∥. Thus, we get
|θk| · ∥Ψk − Ψk∥ ≤ 2π · 2∥|Ψk⟩ − |Ψk⟩∥ ≤ 13∥|Ψk⟩ − |Ψk⟩∥. (220)
2. For the third term, since |sk| ≤ π/2
√
Vk ≤ 2η, we have
|sk| · ∥[Ψk − Ψk,H]∥ ≤ 2η · 2∥Ψk − Ψk∥ · ∥H∥ ≤ 8η ∥|Ψk⟩ − |Ψk⟩∥. (221)
3. By a similar consideration as in Eq. (171), we arrive at
∥eiθkΨk
− eiθkΨk
∥ ≤ ∥eiθkΨk
− eiθ̃kΨk
∥ + ∥eiθ̃kΨk
− eiθkΨk
∥ (222)
≤ 4η∥|Ψk⟩ − |Ψk⟩∥ + 2ηδE , (223)
where we used |Ek − Ẽk| ≤ 2∥|Ψk⟩ − |Ψk⟩∥ to bound |θk − θ̃k|.
4. Here, most steps proceeded as in the Prop. C.3, but the last remaining term needs a separate
treatment as we do not a-priori have a bound on |sk − sk|. To proceed with the bound, we use
the exact expectation values Ẽk and Ṽk of the states |Ψk⟩ in Eq. (157) to introduce
s̃k = s(Ẽk,Ṽk) =
1
q
Ṽk
arccos


Ẽk − u
q
Ṽk + (Ẽk − u)2

 . (224)
Next, Prop. C.4 is used twice. Indeed, we use sk, s̃k and sk to denote different durations:
• sk: a time duration computed using the exact expectation values of the exact states |Ψk⟩
• s̃k: a time duration computed using exact expectation values for states |Ψk⟩
• sk: a time duration computed using the estimated expectation values of the states |Ψk⟩.
Then, we have

esk[Ψ,H]
− esk[Ψ,H]

|Ψk⟩ ≤

esk[Ψ,H]
− es̃k[Ψ,H]

|Ψk⟩ +

es̃k[Ψ,H]
− esk[Ψ,H]

|Ψk⟩ .
(225)
We remark that both terms are already computed in Eq. (214) for the proof of Prop. C.4. Hence,
we can compute them as follows.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 38(a) The first term is equal to Eq. (214) when V ′ (E′) is replaced with ˜ Vk (Ẽk), i.e.,

esk[Ψ,H]
− es̃k[Ψ,H]

|Ψk⟩ ≤ 18η4
·

max(|Vk − Ṽk|,|Ek − Ẽk|)

. (226)
Thus, the remaining task is to account the differences of the exact expectation values and
variances, which are given by
|Ek − Ẽk| ≤ 2∥|Ψk⟩ − |Ψk⟩∥, (227)
|Vk − Ṽk| ≤ |⟨Ψk|H2
|Ψk⟩ − ⟨Ψk|H2
|Ψk⟩| + |E2
k − Ẽ2
k| ≤ 6∥|Ψk⟩ − |Ψk⟩∥. (228)
Using this observation, we have

esk[Ψ,H]
− es̃k[Ψ,H]

|Ψk⟩ ≤ 18η4
·

6∥|Ψk⟩ − |Ψk⟩∥

= 108η4
∥|Ψk⟩ − |Ψk⟩∥ . (229)
(b) For the second term, the gaps in the energy and variance arise from the inaccurate estimation
caused by statistical noise. Thus we have

es̃k[Ψ,H]
− es̃k[Ψ,H]

|Ψk⟩ ≤ 18η4
max(δV ,δE) . (230)
Overall, by substituting the above calculations into Eq. (219), we have
∥|Ψk+1⟩ − |Ψk+1⟩∥ ≤ (14 + 120η4
)∥|Ψk⟩ − |Ψk⟩∥ + 20η4
max(δV ,δE) . (231)
Thus, using these bounds inductively, we get
∥|Ψk⟩ − |Ψk⟩∥ ≤ 20η4
max(δV ,δE)
k−1 X
i=0
(14 + 120η4
)i
(232)
= 20η4
max(δV ,δE)
1 − (14 + 120η4)k
1 − (14 + 120η4)
(233)
≤ (14 + 120η4
)k
max(δV ,δE) . (234)
By setting k = K, we get the claimed scaling.
D Applications of DB-QSP
In this section, we explore the potential applications of DB-QSP. As noted in the main text, a limi-
tation of DB-QSP is that only low-degree polynomials is feasible. Therefore, we first provide useful
approximation techniques that can expand its applicability. We then discuss applicability of DB-QSP
for other tasks.
D.1 Examples of Low-Degree Polynomial Approximations
To assess the effectiveness of DB-QSP, it is crucial to understand what kind of functions can be
realized using low-degree polynomials. In QSP with post-selection, this issue is directly linked to
the success probability of post-selection, as it depends on the degree of polynomials as well as an
input state |Ψ0⟩. Importantly, several polynomial approximation techniques have been explored in the
literature [2, 3]. To illustrate that DB-QSP can achieve ϵ-precision while maintaining a logarithmically
small polynomial degree, we present three representative examples below.
We first show an approximation of the sign function, which can be used for the ground-state prepa-
ration task [9].
Example D.1 (Approximation of the sign function sgn(x) [9, 2]). Suppose δ > 0, x ∈ R and ϵ ∈
(0,1/2). Given a degree K = O(log(1/ϵ)/δ), there exists an odd polynomial p(x), such that
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 39• for all x ∈ [−2,2]: |p(x)| ≤ 1 and
• for all x ∈ [−2,2]\(−δ,δ): |p(x) − sgn(x)| ≤ ϵ
where
sgn(x) =

  
  
1 if x > 0,
−1 if x < 0,
0 if x = 0.
(235)
As another polynomial function for filtering in the ground-state preparation task, we also demon-
strate the approximation of trigonometric functions.
Example D.2 (Polynomial approximation of trigonometric functions by Jacobi-Anger expansion [3,
2]). Suppose s ∈ R and ϵ ∈ (0, 1
e). Given a degree K = ⌊1
2r

e|s|
2 , 5
4ϵ

⌋, trigonometric functions can be
approximated as follows;
∥cos(sx) − J0(s) + 2
K X
l=1
(−1)l
J2l(t)T2l(x)∥[−1,1] ≤ ϵ, (236)
∥sin(sx) − 2
K X
l=1
(−1)l
J2l+1(t)T2l+1(x)∥[−1,1] ≤ ϵ, (237)
where Jm(s) is the Bessel functions of the first kind and Tm(x) is the Chebyshev polynomials of the
first kind. Also, r(t,ϵ) is a function that asymptotically scales as
r(t,ϵ) = Θ

|t| +
log(1/ϵ)
log(e + log(1/ϵ)
|t| )

. (238)
This indicates that trigonometric functions can be approximated using a polynomials of degree
d = ⌊1
2r

e|s|
2 , 5
4ϵ

⌋ to achieve ϵ-precision.
Next, we move to an polynomial approximation for matrix inversion used for, e.g., solving linear
system of equations.
Example D.3 (Polynomial approximation of the inverse [67, 3]). Suppose κ > 1, ϵ ∈ (0, 1
2) and
x ∈ [−1,1]\(−1
κ), 1
κ. Then
f(x) =
1 − (1 − x2)a
x
(239)
is an odd function with a = ⌈κ2 log(κ/ϵ)⌉ is ϵ-close to the inverse 1/x. Given a degree K =
⌈
p
alog(4a/ϵ)⌉ = O(κlog(κ/ϵ)), the odd real function
g(x) = 4
K X
l=1
(−1)l


Pa
j=l+1
2a
a+j

22a

T2l+1(x) (240)
is ϵ-close to f(x) on the domain [−1,1].
This indicates that DB-QSP has the potential to efficiently perform matrix inversion in terms of
the inverse precision 1/ϵ. However, the circuit depth required for DB-QSP scales super exponentially
with the condition number, a key factor in assessing the algorithm’s efficiency. Thus, this example
also highlights a fundamental challenge for DB-QSP in certain computational tasks.
With these approximations, our approach could circumvent the exponential costs for some cases.
Furthermore, approximations for other functions have been provided, e.g., in Ref. [7]. This suggests
that certain tasks benefiting from these polynomials can also be performed using DB-QSP. Thus,
DB-QSP remains practically viable in some cases.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 40D.2 Derivation of DB-QITE Using DB-QSP
As discussed in the main text, DB-QSP can be utilized to implement Imaginary-Time Evolution
(ITE), which is a key technique for ground-state preparation. The non-unitary operator in imaginary
time evolution, e−τH, can be approximated up to the first order as p(H) = I − τH. Thus, Lem. 1
immediately suggests that DB-QSP can be used to approximate the imaginary time evolution. Then,
by using the group commutator
es0[Ψ,H]
= ei
√
s0H
ei
√
s0Ψ
e−i
√
s0H
e−i
√
s0Ψ
+ O(s
3/2
0 ) (241)
and noticing that the last unitary has a trivial action on |Ψ⟩, we arrive at the proposal in Ref. [18]
|ωk+1⟩ = ei
√
s0H
ei
√
s0ωk
e−i
√
s0H
|ωk⟩ . (242)
This is essentially the same as choosing N = 1 in DB-QSP with θk = 0.
One subtlety is that DB-QSP suggests to use state-dependent scheduling sk. Ref. [18] proved that
using a sufficiently small constant s0 allows to converge to the ground state and in every step have a
cooling rate matching imaginary time evolution. The iterative use of Thm. 1 shows that this quantum
algorithm can be devised based on QSP as the design approach.
D.3 Hamiltonian Simulation
Next, we move onto the Hamiltonian simulation task, where the goal is to implement the real-time
evolution e−itH. To perform this task, a common assumption in QSP implementation is direct access
to a subroutine which applies the input Hermitian matrix H to an input state; see App. A. One
approach to Hamiltonian simulation is to approximate the evolution operator using a Taylor series
expansion
pHS(H) =
K X
k=0
(−it)n
n!
Hn
, (243)
which allows the Hamiltonian evolution to be approximated via polynomial transformations.
At first glance, this polynomial decomposition suggests that DB-QSP might also be applicable to
Hamiltonian simulation. However, DB-QSP is not designed for this task. Since Alg. 1 assumes direct
access to eitH, using DB-QSP for Hamiltonian simulation would be vacuous. This query model is also
known as the Hamiltonian evolution model and has been widely used in tasks such as ground-state
energy estimation with early fault-tolerant quantum computers [68, 69, 70]. From this perspective, the
fact that DB-QSP does not target Hamiltonian simulation is not a limitation but rather an inherent
feature of the query model.
D.4 Evolution under a Polynomial Function of Hamiltonian
Interestingly, though, DB-QSP can be used to effectively transform Hamiltonians, while working in
the Hamiltonian evolution model. In its simplest variant, we aim to implement the Hamiltonian
simulation of H2, the second power of the input matrix. Strikingly, DB-QSP can be applied to this
scenario by interpreting pHS(H2) as a polynomial of doubled degree in the variable H, which leads to
the factorization
pHS(H2
) = a2K
2K Y
k=1
(H −
√
zkI)(H +
√
zkI) (244)
in contrast to the alternative formulation
pHS(H2
) = aK
K Y
k=1
(H2
− zkI), (245)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 41which treats H2 as the primary variable. More generally, for evolution under eitg(H) where g is a
polynomial, we observe that if h = p ◦ g is also a polynomial, then pHS(g(H)) can be factorized
accordingly, allowing us to proceed in an analogous manner.
The possibility to systematically use the Hamiltonian simulation e−itH to simulate e−itH2
is implied
by classic results in Lie group theory [71], but an explicit construction of the type provided by DB-QSP
is new to our knowledge. In particular, DB-QSP could provide a convergence rate and a circuit lower
bound to a large class of instances of this classic question. Finally, we remark that Thm. 2 is required
in this case, because pHS(H) = I − iH − H2/2 has complex roots z± = ±1 − i for K = 2 and t = 1.
D.5 Laurent Polynomials
Another application is the Laurent polynomials, which include terms with negative powers, i.e.,
pL(H) =
K X
k=−K
akHk
. (246)
While it is useful for QSP to consider “polynomials” involving inverse powers, Thm. 2 does not directly
provide unitary synthesis for this type. Yet, assuming the matrix H satisfies ∥I − H∥ < 1, we can
consider H−K ≈ pINV(H)K and thus write
pDBL(H) = pINV(H)K
K X
k=0
ak−KHk
. (247)
This gives the approximation pDBL(H) ≈ pL(H) and provides an example how one can implement Lau-
rent polynomials using DB-QITE. The general case for Laurent polynomials with arbitrary Hermitian
matrices is left for future work.
E Classically-Aided DB-QSP Synthesis
Statistical error is unavoidable when estimating energy mean and variance on quantum hardware,
because of the finite number of measurement shots. Error analysis in Eq. (33) further suggests that
this issue becomes more pronounced as the polynomial degree increases. This suggests the need for
an approach to circumvent this challenge. One potential solution is to leverage classical computation
in initial steps. Motivated by this, we explore conditions under which energy and variance can be
efficiently computed using classical resources.
Assume that the initial state |Ψ0⟩ is expressed in a basis where only m of its components are nonzero.
For instance, if the initial state is a tensor-product of zero states, i.e., |0⟩⊗L
with L-qubits, then m = 1.
Additionally, suppose the target Hermitian matrix is given by H =
PJ
i=1 wiPi with Pauli operators
{Pi}. Using Eq. (11) together with the effect of state-dependent phase gate, the resultant state can
always be written as
|Ψk⟩ =


k Y
j=1
(a′
(sj)I + b(sj)H)

|Ψ0⟩ (248)
with a′(sj) ∈ C and b(sj) ∈ R. Note that the coefficients a′(sj) and b(sj) are determined by the
energy and variance of the state at (k−1)-th step. Our goal is to estimate the energy O = H and the
variance O = (H −⟨H⟩)2. By substituting Eq. (248) into the expectation value ⟨Ψk|O|Ψk⟩, we obtain
⟨Ψk|H|Ψk⟩ =
2k+1 X
l=1
ξl ⟨Ψ0|Hl
|Ψ0⟩, (249)
⟨Ψk|(H − ⟨H⟩)2
|Ψk⟩ =
2k+2 X
l=0
ξ′
l ⟨Ψ0|Hl
|Ψ0⟩. (250)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 42where coefficients {ξl} and {ξ′
l} are determined by computing Eq. (248). Implication of
Eqs. (249), (250) is that, if we can compute ⟨Ψ0|Hl|Ψ0⟩ up to l = 2k + 2 classically, the energy
and variance at k step is tractable using classical computers.
With these criteria in mind, we analyze the conditions under which the classical computation of
energy and variance is feasible. First, the number of Pauli operators in H2k+2 is at most J2k+2 + 1.
Furthermore, since each Pauli operator has exactly one nonzero entry per row and column, the total
number of nonzero elements that need to be stored scales as O(mJ2k+2). To ensure classical tractability
in terms of memory and computational cost, we require this scaling to remain within O(poly(n)). Thus,
the condition on k for energy and variance to be classically computable is given by
m2
J2k+2
≤ poly(n)
⇔k ≤
log(poly(n))/2 − log(m)
log(J)
− 1
⇔k = O

log(poly(n))/2 − log(m)
log(J)

.
This indicates that, if m,J = O(1), we can classically compute up to k = O(log(n)). On the other
hand, computing only constant step k is possible if m,J = O(poly(n)) This clearly captures the
classical difficulty: if the initial state contains many non-zero elements and the number of Pauli
terms becomes prohibitively large, it becomes infeasible to compute the energy even for a single
step. However, for instance, the Pauli terms for Ising models scale linearly in the number of qubits.
Furthermore, some situations involve easy-to-prepare initial states like the tensor product of zero
states, where m = 1. Thus, this result suggests that a few steps of classical computation may be
feasible in some cases. We also note that this estimation is straightforward, and advanced classical
techniques could further improve the efficiency, which we will leave for future work.
F Unbiased Estimator of the Operator Variance for Hamiltonians
In this section, we derive an unbiased estimator for the variance of an observable expressed as a
weighted sum of Pauli operators. We first describe the measurement procedure used to estimate the
expectation values of individual Pauli operators and their products. Next, we construct a straightfor-
ward variance estimator and demonstrate its bias arising from finite-sample effects. To address this,
we derive a corrected formula that provides an unbiased estimate of the operator variance.
F.1 Measurement Procedure
Here, we focus on the observables Ô that can be decomposed as the weighted sum of Pauli operators,
i.e., the observable can be expressed in the form
Ô =
L X
i=1
wiPi , (251)
where Pi ∈ {I,X,Y,Z}⊗n denotes the Pauli operators for n qubits and wi represents its corresponding
weights.
Then, the variance of the observable Ô is defined as V = ⟨Ô2⟩ − ⟨Ô⟩
2
, where ⟨·⟩ = ⟨ψ| · |ψ⟩ for a
pure quantum state |ψ⟩. Thus, the square of the observable is given by
Ô2
=
L X
i=1
wiPi
!

L X
j=1
wjPj

 =
L X
i=1
w2
i I +
L X
i,j=1
i̸=j
wiwjPij , (252)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 43where we use the Pauli operators’s identity P2
i = I and we introduce the notation Pij = PiPj. Using
the expression of Ô and Ô2, the variance of the observable is given by
V = ⟨Ô2
⟩ − ⟨Ô⟩
2
=
L X
i=1
w2
i ⟨I⟩ +
L X
i,j=1
i̸=j
wiwj ⟨Pij⟩ −
L X
i=1
wi ⟨Pi⟩
!2
. (253)
To estimate the variance, we measure each Pauli component multiple times. Using the measurement
outcomes, we can then estimate the expectation value of each term in Eq. (253). The procedure is:
1. ⟨I⟩ = 1 by the assumption of normalised state.
2. Suppose we measure Pi a total of Ni times, yielding outcomes (a set of measured bit-strings)
{b
(Pi)
1 , b
(Pi)
2 , ..., b
(Pi)
Ni
} with each bk ∈ {−1,+1} for 1 ≤ k ≤ Ni . (254)
Then the estimation of a single Pauli operator Pi is ⟨Pi⟩ =
1
Ni
Ni X
k=1
b
(Pi)
k .
3. Similarly, if we measure the product operator Pij = PiPj (for i ̸= j) Nij times, we obtain the
estimator
⟨PiPj⟩ =
1
Nij
Nij
X
k=1
b
(Pij)
k . (255)
F.2 Biased and Unbiased Estimator of the Operator Variance
F.2.1 Biased and Unbiased Estimator
First, we mention the definition of biased and unbiased estimator.
Definition F.1 (Estimator). Let A be an estimator of the parameter A. The estimator is said to be:
• unbiased if E[A] = A,
• biased if E[A] ̸= A ,
where we use E to denote the expected value over the sampling process in this section.
Using the statistics, a natural choice of the estimator of Eq. (253) would be
Ṽ =
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj ⟨PiPj⟩ −
L X
i=1
wi ⟨Pi⟩
!2
(256)
=
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k

 −


L X
i=1
wi


1
Ni
Ni X
k=1
b
(Pi)
k




2
. (257)
However, we demonstrate a simple example where the last term of this estimator introduces bias
into the estimator.
Example F.1. Let P ∈ {I,X,Y,Z}⊗n be a Pauli operator and suppose that we estimate its expec-
tation value by performing N independent and identically distributed (i.i.d.) measurements, yielding
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 44outcomes {bi}N
i=1 (with bi ∈ {−1,+1}). Using our construction, the natural estimator for ⟨P⟩2 is
˜ ⟨P⟩2 :=

1
N
PN
i=1 bi
2
, and its expectation value yields
E


1
N
N X
i=1
bi
!2

 =
1
N2




N X
i=1
E[b2
i ] +
N X
i,j=1
i̸=j
E[bibj]



 =
1
N2




N X
i=1
1 +
N X
i,j=1
i̸=j
⟨Pi⟩2



 (258)
=
1
N2

N + N(N − 1)⟨P⟩2

= ⟨P⟩2
+
1 − ⟨P⟩2
N
.
(259)
where we use the i.i.d. assumption (E[bibj] = E[bi]E[bj] for i ̸= j) and the relation b2
i = 1 in the second
line. Clearly, E
"z}|{
⟨P⟩2
#
̸= ⟨P⟩2 for any finite sample size N, and hence it is a biased estimator by the
definition. To remove this bias, we introduce a correction factor and define the unbiased estimator as
⟨P⟩2 :=
N
N − 1


1
N
N X
i=1
bi
!2
−
1
N

 . (260)
Directly evaluating the expectation value of new estimator of ⟨P⟩2 yields
E


N
N − 1


1
N
N X
i=1
bi
!2
−
1
N



 =
N
N − 1
"
⟨P⟩2
+
1 − ⟨P⟩2
N
−
1
N
#
= ⟨P⟩2
. (261)
Thus, this is indeed an unbiased estimator for ⟨P⟩2 as the expectation value of the estimator is con-
sistent with the true value.
Proposition F.2 (Unbiased estimator for the variance of an observable). Consider an observable Ô
which can be written as Ô =
PL
i=1 wiPi, where Pi ∈ {I,X,Y,Z}⊗n denotes the Pauli operators for
n qubits and wi represents its corresponding weights. The unbiased estimator for the variance of this
observable is then given by
V =
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k


−
L X
i=1
w2
i Ni
Ni − 1





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni


 −
L X
i,j=1
i̸=j
wiwj


1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k

 , (262)
where we measure the operator Pi a total of Ni times and the product operator Pij = PiPj (for i ̸= j)
a total of Nij times.
Proof. The expected value of V is
E
h
V
i
=
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj E




1
Nij
Nij
X
k=1
b
(Pij)
k




−
L X
i=1
w2
i Ni
Ni − 1
E





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni


 −
L X
i,j=1
i̸=j
wiwj E




1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k



 ,
(263)
where we use the fact that the expected value of a constant is the same constant for the first term.
Next, we address the remaining terms separately.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 451. Since the term
1
Nij
Nij
X
k=1
b
(Pij)
k is unbiased estimator for ⟨Pij⟩, we have
L X
i,j=1
i̸=j
wiwj E




1
Nij
Nij
X
k=1
b
(Pij)
k



 =
L X
i,j=1
i̸=j
wiwj ⟨Pij⟩ . (264)
2. For the third term, we have
L X
i=1
w2
i Ni
Ni − 1
E





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni


 =
L X
i=1
w2
i Ni
Ni − 1

 
 
E





1
Ni
Ni X
k=1
b
(Pi)
k


2


 −
1
Ni

 
 
(265)
=
L X
i=1
w2
i Ni
Ni − 1
(
⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
−
1
Ni
)
=
L X
i=1
w2
i ⟨Pi⟩2
,
(266)
where we use Eq. (279) of Lem. F.4 in the second line.
3. For the last term, since the samples for different indices (i ̸= j) are i.i.d., we have
L X
i,j=1
i̸=j
wiwj E




1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k



 =
L X
i,j=1
i̸=j
wiwj E




1
Ni
Ni X
k=1
b
(Pi)
k



E




1
Nj
Nj
X
k=1
b
(Pj)
k




(267)
=
L X
i,j=1
i̸=j
wiwj ⟨Pi⟩⟨Pj⟩ . (268)
Collecting all the terms, the expected value of V becomes
E
h
V
i
=
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj ⟨PiPj⟩ −
L X
i=1
w2
i ⟨Pi⟩2
−
L X
i,j=1
i̸=j
wiwj ⟨Pi⟩⟨Pj⟩ (269)
=
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj ⟨Pij⟩ −
L X
i=1
wi ⟨Pi⟩
!2
(270)
Since E
h
V
i
= V by using Eq. (253), V is indeed an unbiased estimator.
F.3 Total Variance of the Unbiased Estimator of the Operator Variance
Next, with the motivation to assess the query complexity in DB-QSP, we compute the uncertainty of
the unbiased estimator of the operator variance. Here, we consider variance as the uncertainty metric,
which is given by:
Var[V ] = Var

⟨Ô2⟩ − ⟨Ô⟩
2

= Var
h
⟨Ô2⟩
i
+ Var

⟨Ô⟩
2

− 2 Cov

⟨Ô2⟩,⟨Ô⟩
2

, (271)
where we use the identity Var[A+B] = Var[A]+Var[B]+2Cov(A,B). The estimator for ⟨Ô2⟩ and ⟨Ô⟩
2
are determined by the measurement on the Pauli operators Pij and Pk respectively. Assuming that
the measurements on Pij and Pk are independent, their covariance is zero, i.e., Cov

⟨Ô2⟩,⟨Ô⟩
2

= 0.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 46Therefore, the remaining task is to evaluate Var
h
⟨Ô2⟩
i
and Var

⟨Ô⟩
2

. We address these two terms
in Lem. F.3 and Lem. F.5.
Lemma F.3. Suppose we have an observable Ô which is of the form Ô =
PL
i=1 wiPi, where Pi ∈
{I,X,Y,Z}⊗n denotes the Pauli operators for n qubits and wi represents its corresponding weights.
Assuming that measurements performed for all operators are i.i.d., then the uncertainty (variance) of
the estimation of Ô2 can be expressed as
Var
h
⟨Ô2⟩
i
=
L X
i,j=1
i̸=j
w2
i w2
j
Nij

1 − ⟨Pij⟩2

, (272)
where we define ⟨Pij⟩ = ⟨Pi⟩⟨Pj⟩ and Nij is the number of sample used to estimate ⟨Pij⟩.
Proof. We start with the expression
Var
h
⟨Ô2⟩
i
= Var




L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k





. (273)
Since the first term
PL
i=1 w2
i is a constant, its variance is zero. Therefore, we have
Var
h
⟨Ô2⟩
i
= Var




L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k





. (274)
Assuming that the contributions from different pairs of Pauli operators (i,j) are independent, it
reduces to
Var
h
⟨Ô2⟩
i
=
L X
i,j=1
i̸=j
Var


wiwj
Nij
Nij
X
k=1
b(Pij)

 =
L X
i,j=1
i̸=j
w2
i w2
j
N2
ij
Var


Nij
X
i=1
b
(Pij)
i

 , (275)
where we use the property Var[aX] = a2 Var[X] (for any nonnegative constant a) in the last line.
Furthermore, assuming that the b
(Pij)
i are i.i.d., it can be further simplified to
Var
h
⟨Ô2⟩
i
=
L X
i,j=1
i̸=j
w2
i w2
j
N2
ij

Nij Var
h
b
(Pij)
i
i
. (276)
Next, recall that each bi satisfies b2
i = 1, and hence we obtain the following relation
Var
h
b
(Pij)
i
i
= ⟨b
(Pij)
i × b
(Pij)
i ⟩ − ⟨b
(Pij)
i ⟩
2
= 1 − ⟨b
(Pij)
i ⟩
2
= 1 − ⟨Pij⟩2
. (277)
Combining Eq. (276) and Eq. (277) yields Eq. (272).
Before proceeding to Lem. F.5, let us first show a technical Lem. F.4, which will be useful in the
proof of Lem. F.5.
Lemma F.4. Given a single Pauli operator of n qubits Pi ∈ {I,X,Y,Z}⊗n, we estimate the expecta-
tion value of Pi as
Xi = ⟨Pi⟩ =
1
Ni
Ni X
k=1
b
(Pi)
k . (278)
where b
(Pi)
k denotes the outcome of k-th measurement for the Pauli operator Pi. Assuming the mea-
surements are i.i.d., we obtain
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 471. the first moment of Xi as E[Xi] = ⟨Pi⟩.
2. the second moment of Xi as
E
h
X2
i
i
= ⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
. (279)
3. the third moment of Xi as
E
h
X3
i
i
= ⟨Pi⟩3
1 −
3
Ni
+
2
N2
i
!
+ ⟨Pi⟩
3
Ni
−
2
N2
i
!
. (280)
4. the fourth moment of Xi as
E
h
X4
i
i
= ⟨Pi⟩4
+
6⟨Pi⟩2 1 − ⟨Pi⟩2

Ni
+
11⟨Pi⟩2 − 3

⟨Pi⟩2 − 1

N2
i
+
2(3⟨Pi⟩2 − 1)(1 − ⟨Pi⟩2)
N3
i
.
(281)
where ⟨Pi⟩ denotes the true expectation value of Pi.
Proof. To simplify the notation, we use bi to represent b
(Pi)
i throughout this proof.
1. First moment of Xi:
Since the expectation value of a scalar is just the scalar itself, we obtain E[Xi] = E
h
⟨Pi⟩
i
= ⟨Pi⟩.
2. Second moment of Xi:
Taking the expectation value of it yields
E
h
X2
i
i
= E





1
Ni
Ni X
i=1
bi


2


 =
1
N2
i




Ni X
i=1
E[b2
i ] +
Ni X
i,j=1
i̸=j
E[bibj]



 . (282)
Since each bi satisfies b2
i = 1, we have E[b2
i ] = 1 for all i. Furthermore, assuming the samples are
i.i.d., we obtain E[bibj] = E[bi]E[bj] for i ̸= j. Thus, it becomes
E
h
X2
i
i
=
1
N2
i




Ni X
i=1
1 +
Ni X
i,j=1
i̸=j
E[bi]2



 =
1
N2
i




Ni X
i=1
1 +
Ni X
i,j=1
i̸=j
⟨Pi⟩2



 =
1
N2
i

Ni + Ni(Ni − 1)⟨Pi⟩2

(283)
= ⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
. (284)
where we recall the definition of the true expectation value E[bi] = ⟨Pi⟩ in the second equality.
3. Third moment of Xi:
Similarly, for the third moment, we split the summation into multiple parts, i.e. we classify the
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 483–tuple (i,j,k) according to the “equivalence class” of the three indices. Thus, we have
E
h
X3
i
i
=
1
N3
i




Ni X
i=1
E[b3
i ] +
Ni X
i,j=1
i̸=j
E[b2
i bj] +
Ni X
i,j,k=1
i̸=j̸=k
E[bibjbk]



 (285)
=
1
N3
i




Ni X
i=1
E[bi] +
Ni X
i,j=1
i̸=j
E[bj] +
Ni X
i,j,k=1
i̸=j̸=k
E[bi]E[bj]E[bk]



 (286)
=
1
N3
i




Ni X
i=1
⟨Pi⟩ +
Ni X
i,j=1
i̸=j
⟨Pi⟩ +
Ni X
i,j,k=1
i̸=j̸=k
⟨Pi⟩⟨Pi⟩⟨Pi⟩



 , (287)
where we again use the identity b2
i = 1 and the i.i.d. assumption in the second line. By counting
the possible configurations of each summation, we arrive at
E
h
X3
i
i
=
1
N3
i

Ni ⟨Pi⟩ + 3Ni(Ni − 1)⟨Pi⟩ + Ni(Ni − 1)(Ni − 2)⟨Pi⟩3

(288)
= ⟨Pi⟩3
1 −
3
Ni
+
2
N2
i
!
+ ⟨Pi⟩
3
Ni
−
2
N2
i
!
. (289)
4. Fourth moment of Xi:
Lastly, for the fourth moment E

X4
i

, we again split the summation into multiple parts in the
last line, i.e., we classify the 4–tuple (i,j,k,l) according to the “equivalence class” of the four
indices.
E
h
X4
i
i
=
1
N4
i




Ni X
i=1
E[b4
i ] +
Ni X
i,j=1
i̸=j
E[b3
i bj] +
Ni X
i,j=1
i̸=j
E[b2
i b2
j] +
Ni X
i,j,k=1
i̸=j̸=k
E[b2
i bjbk] +
Ni X
i,j,k,l=1
i̸=j̸=k̸=l
E[bibjbkbl]




(290)
=
1
N4
i




Ni X
i=1
1 +
Ni X
i,j=1
i̸=j
E[bi]E[bj] +
Ni X
i,j=1
i̸=j
1 +
Ni X
i,j,k=1
i̸=j̸=k
E[bj]E[bk] +
Ni X
i,j,k,l=1
i̸=j̸=k̸=l
E[bi]E[bj]E[bk]E[bl]




(291)
=
1
N4
i




Ni X
i=1
1 +
Ni X
i,j=1
i̸=j
⟨Pi⟩2
+
Ni X
i,j=1
i̸=j
1 +
Ni X
i,j,k=1
i̸=j̸=k
⟨Pi⟩2
+
Ni X
i,j,k,l=1
i̸=j̸=k̸=l
⟨Pi⟩4



 . (292)
where we also employ the identity b2
i = 1 and the i.i.d. assumption in the second line. By
accounting for all possible arrangements in each summation, we derive
E
h
X4
i
i
=
1
N4
i
(Ni + 4Ni(Ni − 1)⟨Pi⟩2
+ 3Ni(Ni − 1)
+ 6Ni(Ni − 1)(Ni − 2)⟨Pi⟩2
+ Ni(Ni − 1)(Ni − 2)(Ni − 3)⟨Pi⟩4
) (293)
= ⟨Pi⟩4
+
6⟨Pi⟩2 1 − ⟨Pi⟩2

Ni
+
11⟨Pi⟩2 − 3

⟨Pi⟩2 − 1

N2
i
+
2(3⟨Pi⟩2 − 1)(1 − ⟨Pi⟩2)
N3
i
.
(294)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 49Now, we are ready to present Lem. F.5, which is the second term of Eq. (271).
Lemma F.5. Suppose we have an observable Ô which can be decomposed to Ô =
PL
i=1 wiPi, where
Pi ∈ {I,X,Y,Z}⊗n denotes the Pauli operators for n qubits and wi represents its corresponding
weights. Assuming that measurements performed for all operators are i.i.d., then the uncertainty
(variance) of the square of the estimation of Ô can be expressed as
Var

⟨Ô⟩
2

=
L X
i=1
"
w4
i 1 − ⟨Pi⟩2

(Ni − 1)2
×

4⟨Pi⟩2
Ni + 2(1 − ⟨Pi⟩2
)

#
+
L X
i,j=1
i̸=j
"
w2
i w2
j
⟨Pi⟩2 1 − ⟨Pj⟩2

Nj
+
⟨Pj⟩2 1 − ⟨Pi⟩2

Ni
+
1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

NiNj
!#
+ 4
L X
i,j=1
i̸=j
w3
i wj
Ni
⟨Pi⟩⟨Pj⟩(1 − ⟨Pi⟩2
)
!
, (295)
where Ni is the number of sample used to estimate ⟨Pi⟩ for each 1 ≤ i ≤ L.
Proof. We start with the expression
Var

⟨Ô⟩
2

= Var




L X
i=1
w2
i Ni
Ni − 1





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni


 +
L X
i,j=1
i̸=j
wiwj


1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k





 (296)
= Var



L X
i=1
w2
i Ni
Ni − 1





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni





 + Var




L X
i,j=1
i̸=j
wiwj


1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k






+ 2 Cov




L X
i=1
w2
i Ni
Ni − 1





1
Ni
Ni X
k=1
b
(Pi)
k


2
−
1
Ni


,
L X
i,j=1
i̸=j
wiwj


1
Ni
Ni X
k=1
b
(Pi)
k




1
Nj
Nj
X
k=1
b
(Pj)
k





 ,
(297)
where we use the identity Var[A+B] = Var[A]+Var[B]+2 Cov(A,B) (for any variable A,B). Before
we proceed to evaluate these three terms, let us define the shorthand notation Xi = 1
Ni
PNi
k=1 b
(Pi)
k .
The final expression of these three terms are:
1. For the first term, we have
Var
" L X
i=1
w2
i Ni
Ni − 1

X2
i −
1
Ni
#
=
L X
i=1
Var
"
w2
i Ni
Ni − 1

X2
i −
1
Ni
#
=
L X
i=1
Var
"
w2
i Ni
Ni − 1
X2
i
#
(298)
=
L X
i=1
w4
i N2
i
(Ni − 1)2
Var
h
X2
i
i
, (299)
where we assume that Pi and Pj are independent measurement for i ̸= j in the first equality and
the property Var[X + c] = Var[X] (for arbitrary constant c) in the second equality. Next, by
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 50definition we have Var

X2
i

= E

X4
i

− E

X2
i
2
, where using Lem. F.4 further gives
Var
h
X2
i
i
= ⟨Pi⟩4
+
6⟨Pi⟩2 1 − ⟨Pi⟩2

Ni
+
11⟨Pi⟩2 − 3

⟨Pi⟩2 − 1

N2
i
+
2(3⟨Pi⟩2 − 1)(1 − ⟨Pi⟩2)
N3
i
(300)
− ⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
!2
(301)
=
4⟨Pi⟩2 1 − ⟨Pi⟩2

Ni
+
2 5⟨Pi⟩2 − 1

⟨Pi⟩2 − 1

N2
i
+
2(3⟨Pi⟩2 − 1)(1 − ⟨Pi⟩2)
N3
i
. (302)
Using this result, Eq. (299) simplifies to
Var
" L X
i=1
w2
i Ni
Ni − 1

X2
i −
1
Ni
#
=
L X
i=1
w4
i N2
i
(Ni − 1)2
×
4⟨Pi⟩2 1 − ⟨Pi⟩2

Ni
+
2 5⟨Pi⟩2 − 1

⟨Pi⟩2 − 1

N2
i
+
2(3⟨Pi⟩2 − 1)(1 − ⟨Pi⟩2)
N3
i
!
(303)
=
L X
i=1
w4
i (1 − ⟨Pi⟩2)
(Ni − 1)2
"
4Ni⟨Pi⟩2
− 2

5⟨Pi⟩2
− 1

+
2(3⟨Pi⟩2 − 1)
Ni
#
(304)
=
L X
i=1
w4
i (1 − ⟨Pi⟩2)
Ni(Ni − 1)2
h
4N2
i ⟨Pi⟩2
− 10Ni⟨Pi⟩2
+ 2Ni + 6⟨Pi⟩2
− 2
i
(305)
=
L X
i=1
w4
i (1 − ⟨Pi⟩2)
Ni(Ni − 1)2
h
2⟨Pi⟩2
(2Ni − 3)(Ni − 1) + 2(Ni − 1)
i
(306)
=
L X
i=1
"
2w4
i
Ni(Ni − 1)

1 + 2(Ni − 2)⟨Pi⟩2
− (2Ni − 3)⟨Pi⟩4

#
. (307)
2. For the second term, we have
Var




L X
i,j=1
i̸=j
wiwjXiXj



 = Var


L X
i<j
2wiwjXiXj

 =
L X
i<j
4w2
i w2
j Var[XiXj] , (308)
where we use the property Var[aX] = a2 Var[X]. Next, by definition of variance, we obtain
Var[XiXj] = E
h
X2
i X2
j
i
− E[XiXj]2
= E
h
X2
i
i
E
h
X2
j
i
− E[Xi]2
E[Xj]2
. (309)
Using Lem. F.4, we have
Var[XiXj] = ⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
!
⟨Pj⟩2
+
1 − ⟨Pj⟩2
Ni
!
− ⟨Pi⟩2
⟨Pj⟩2
(310)
=
⟨Pi⟩2 1 − ⟨Pj⟩2

Nj
+
⟨Pj⟩2 1 − ⟨Pi⟩2

Ni
+
1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

NiNj
. (311)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 51Consequently, Eq. (308) is
Var




L X
i,j=1
i̸=j
wiwjXiXj




= 4
L X
i<j
"
w2
i w2
j
NiNj

1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

+ Ni⟨Pi⟩2

1 − ⟨Pj⟩2

+ Nj⟨Pj⟩2

1 − ⟨Pi⟩2

#
.
(312)
3. For the third term, it is
Cov




L X
i=1
w2
i Ni
Ni − 1

X2
i −
1
Ni

,
L X
i,j=1
i̸=j
wiwjXiXj




=
L X
i,j=1
i̸=j
Cov
"
w2
i Ni
Ni − 1

X2
i −
1
Ni

,wiwjXiXj
#
+ Cov
"
w2
i Ni
Ni − 1

X2
i −
1
Ni

,wiwjXjXi
#!
,
(313)
where we use the bilinear property of the covariance. By symmetry, the two covariance contribu-
tions are equal and hence we have
Cov




L X
i=1
w2
i Ni
Ni − 1

X2
i −
1
Ni

,
L X
i,j=1
i̸=j
wiwjXiXj



 = 2
L X
i,j=1
i̸=j
Cov
"
w2
i Ni
Ni − 1

X2
i −
1
Ni

,wiwjXiXj
#!
,
(314)
Since Cov[A,B] = E[AB] − E[A] E[B], we have
Cov
"
w2
i Ni
Ni − 1

X2
i −
1
Ni

,wiwjXiXj
#
= E
"
w2
i Ni
Ni − 1

X2
i −
1
Ni
!
(wiwjXiXj)
#
− E
"
w2
i Ni
Ni − 1

X2
i −
1
Ni
#
E[wiwjXiXj] (315)
=
w3
i wjNi
Ni − 1
E[Xj] ×
n
E[X3
i ] − E[X2
i ] E[Xi]
o
, (316)
Using Lem. F.4, Eq. (316) reduces to
Cov
"
w2
i Ni
Ni − 1

X2
i −
1
Ni

,wiwjXiXj
#
=
w3
i wjNi
Ni − 1
⟨Pj⟩ ×
(
⟨Pi⟩3
1 −
3
Ni
+
2
N2
i
!
+ ⟨Pi⟩
3
Ni
−
2
N2
i
!
− ⟨Pi⟩2
+
1 − ⟨Pi⟩2
Ni
!
⟨Pi⟩
)
(317)
=
w3
i wjNi
Ni − 1
⟨Pj⟩ ×
(
⟨Pi⟩3(2 − 2Ni) + 2⟨Pi⟩(Ni − 1)
N2
i
)
=
2w3
i wj
Ni
⟨Pj⟩⟨Pi⟩(1 − ⟨Pi⟩2
) . (318)
Therefore, Eq. (314) is given by
Cov




L X
i=1
w2
i Ni
Ni − 1

X2
i −
1
Ni

,
L X
i,j=1
i̸=j
wiwjXiXj



 = 4
L X
i,j=1
i̸=j
w3
i wj
Ni
⟨Pj⟩⟨Pi⟩(1 − ⟨Pi⟩2
)
!
. (319)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 52Collecting Eq. (307), Eq. (312) and Eq. (319), we arrive at the final expression:
Var

⟨Ô⟩
2

= 2
L X
i=1
"
w4
i
Ni(Ni − 1)

1 + 2(Ni − 2)⟨Pi⟩2
− (2Ni − 3)⟨Pi⟩4

#
+ 4
L X
i<j
"
w2
i w2
j
NiNj

1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

+ Ni⟨Pi⟩2

1 − ⟨Pj⟩2

+ Nj⟨Pj⟩2

1 − ⟨Pi⟩2

#
+ 4
L X
i<j
w3
i wj
Ni
⟨Pi⟩⟨Pj⟩(1 − ⟨Pi⟩2
)
!
. (320)
Theorem F.6 (Uncertainty of the estimated variance of an observable). Suppose we have an observ-
able Ô which is of the form Ô =
PL
i=1 wiPi, where Pi ∈ {I,X,Y,Z}⊗n denotes the Pauli operators for
n qubits and wi represents its corresponding weights. Assuming that measurements performed for all
operators including Pij = PiPj are i.i.d., then the uncertainty (variance) of the estimated variance of
Ô can be expressed as
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j
Nij

1 − ⟨Pij⟩2

+ 2
L X
i=1
"
w4
i
Ni(Ni − 1)

1 + 2(Ni − 2)⟨Pi⟩2
− (2Ni − 3)⟨Pi⟩4

#
+ 4
L X
i<j
"
w2
i w2
j
NiNj

1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

+ Ni⟨Pi⟩2

1 − ⟨Pj⟩2

+ Nj⟨Pj⟩2

1 − ⟨Pi⟩2

#
+ 4
L X
i<j
w3
i wj
Ni
⟨Pi⟩⟨Pj⟩(1 − ⟨Pi⟩2
)
!
. (321)
Proof. Since the set of Pauli operators {Pi} and Pij = PiPj are i.i.d. and mutually independent, we
obtain Var[V ] = Var
h
⟨Ô2⟩
i
−Var

⟨Ô⟩
2

, where the first and second terms are given by Lem. F.3 and
Lem. F.5 respectively:
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j
Nij

1 − ⟨Pij⟩2

+ 2
L X
i=1
"
w4
i
Ni(Ni − 1)

1 + 2(Ni − 2)⟨Pi⟩2
− (2Ni − 3)⟨Pi⟩4

#
+ 4
L X
i<j
"
w2
i w2
j
NiNj

1 − ⟨Pi⟩2

1 − ⟨Pj⟩2

+ Ni⟨Pi⟩2

1 − ⟨Pj⟩2

+ Nj⟨Pj⟩2

1 − ⟨Pi⟩2

#
+ 4
L X
i<j
w3
i wj
Ni
⟨Pi⟩⟨Pj⟩(1 − ⟨Pi⟩2
)
!
. (322)
F.4 Alternative Unbiased Method of Estimating Operator Variance
Here, we provide another way of computing an unbiased estimator of the variance operator.
Lemma F.7. Suppose we have an observable Ô of the form Ô =
PL
i=1 wiPi, where Pi ∈ {I,X,Y,Z}⊗n
denotes the Pauli operators for n qubits and wi represents its corresponding weights. Assuming mea-
surements performed for all operators including Pij = PiPj are i.i.d., then the unbiased estimator of
the variance operator can be alternatively written as
V =
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k

 −
L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 , (323)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 53where we perform Nij times measurement on the operator Pij = PiPj and N(i⊗j) times joint measure-
ment on Pi ⊗ Pj.
Proof. Recall that the variance for an observable Ô is given by
V = ⟨Ô2
⟩ − ⟨Ô⟩
2
=
L X
i=1
w2
i ⟨I⟩ +
L X
i,j=1
i̸=j
wiwj ⟨Pij⟩ −
L X
i=1
wi ⟨Pi⟩
!2
. (324)
To estimate the second term ⟨Ô⟩
2
, we now perform joint measurements on two copies of quantum
states. For each independent measurement {Pi ⊗ Pj}, we collects the results of measured bit string
{b
(Pi⊗j)
i }. Thus, the unbiased estimator of the product ⟨Pi⟩⟨Pj⟩ is given by
⟨Pi⟩⟨Pj⟩ =
1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i , (325)
where N(i⊗j) denotes the number of samples for the measurement (Pi ⊗ Pj). Hence, the term ⟨Ô⟩
2
can be estimated as
⟨Ô⟩
2
=
L X
i,j=1
wiwj ⟨Pi⟩⟨Pj⟩ =
L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 . (326)
Thus, the unbiased estimator of the variance is
V =
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k

 −
L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 . (327)
Next, we derive the uncertainty of this estimated variance based on this alternative measurement
protocol.
Lemma F.8. Let Ô be an observable of the form Ô =
PL
i=1 wiPi, where Pi ∈ {I,X,Y,Z}⊗n denotes
the Pauli operators for n qubits and wi represents its corresponding weights. Assuming the measure-
ments {Pi⊗j} and {Pij = PiPj} are i.i.d. and they are mutually independent to each other, then the
uncertainty (variance) of the estimated variance V of the observable is
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j

1 − ⟨Pij⟩2

Nij
+
L X
i,j=1
w2
i w2
j

1 − ⟨Pi⟩2
⟨Pj⟩2

N(i⊗j)
, (328)
where we perform Nij times measurement on the operator Pij = PiPj and N(i⊗j) times joint measure-
ment on Pi ⊗ Pj.
Proof. First, since the measurements {Pi⊗j} and {Pij} are i.i.d. and mutually independent, the
variance of the operator is
V =
L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k

 −
L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 . (329)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 54where we use Lem. F.7. Expanding the uncertainty (variance) of this estimation gives
Var[V ] = Var




L X
i=1
w2
i +
L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k

 −
L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i





 (330)
= Var




L X
i,j=1
i̸=j
wiwj


1
Nij
Nij
X
k=1
b
(Pij)
k





 + Var


L X
i,j=1
wiwj


1
N(i⊗j)
N(i⊗j)
X
i=1
b
(Pi⊗j)
i



 , (331)
where we use the fact that the first term
PL
i=1 w2
i has zero variance in the last line. Next, as Var[aX] =
a2 Var[X] for any scalar factor a, it can be simplified to
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j
N2
ij
Var


Nij
X
k=1
b
(Pij)
k

 +
L X
i,j=1
w2
i w2
j
N2
(i⊗j)
Var


N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 . (332)
Since the bit string bi satisfies b2
i = 1, we have the following identity:
Var


Nij
X
k=1
b
(Pij)
k

 =
Nij
X
k=1
Var
h
b
(Pij)
k
i
=
Nij
X
k=1

1 − ⟨Pij⟩2

= Nij

1 − ⟨Pij⟩2

. (333)
Similarly, for the joint measurements, it becomes
Var


N(i⊗j)
X
i=1
b
(Pi⊗j)
i

 =
N(i⊗j)
X
i=1
Var
h
b
(Pi⊗j)
i
i
=
N(i⊗j)
X
i=1

1 − ⟨Pi⟩2
⟨Pj⟩2

= N(i⊗j)

1 − ⟨Pi⟩2
⟨Pj⟩2

. (334)
Therefore, Eq. (332) becomes
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j

1 − ⟨Pij⟩2

Nij
+
L X
i,j=1
w2
i w2
j

1 − ⟨Pi⟩2
⟨Pj⟩2

N(i⊗j)
. (335)
Using this result, we now present a proposition that tells us how many samples we need to achieve
precision ϵ when estimating the variance of the observable Ô.
Proposition F.9. Suppose we have an observable Ô of the form Ô =
PL
i=1 wiPi, where Pi ∈
{I,X,Y,Z}⊗n denotes the Pauli operators for n qubits and wi represents its corresponding weights.
Let us denote V as the estimated variance of the observable. Assume that the measurements {Pi⊗j}
and {Pij} are i.i.d. and mutually independent, the number of samples required to achieve a target
precision ϵ for V scales as the fourth power of the Hamiltonian’s L1 norm and quadratically in the
inverse of ϵ.
Proof. First, note that the total number of the measurements are given by
N =
L X
i,j=1
i̸=j
Nij +
L X
i,j=1
N(i⊗j) . (336)
In this setting, the optimal allocation of measurement shots can be determined via Lagrange multipli-
ers. Our objective is to minimize the total number of shots while ensuring that the uncertainty of V
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 55remains below the desired precision ϵ2. We follow the approach outlined in Ref. [72], which provides
the optimal allocation of measurement shots for estimating each term of the Hamiltonian. Note that
Ref. [72] demonstrates that the number of measurements required to achieve ϵ-precision is given by
O(|w|2/ϵ2) with |w| =
PL
i |wi|. First, the corresponding Lagrangian L can be expressed as
L =
L X
i,j=1
i̸=j
Nij +
L X
i,j=1
N(i⊗j) + λ

Var
h
VN
i
− ϵ2

. (337)
According to Lem. F.8, we have
Var[V ] =
L X
i,j=1
i̸=j
w2
i w2
j

1 − ⟨Pij⟩2

Nij
+
L X
i,j=1
w2
i w2
j

1 − ⟨Pi⟩2
⟨Pj⟩2

N(i⊗j)
. (338)
Using this result, we can proceed to evaluate L. By taking the derivative of L, Eq. (337) yields
∂L
∂Nij
= 1 − λ
w2
i w2
j

1 − ⟨P(i,j)⟩2

N2
ij
,
∂L
∂N(i⊗j)
= 1 − λ
w2
i w2
j

1 − ⟨Pi⟩2
⟨Pj⟩2

N2
(i⊗j)
. (339)
To obtain zero derivatives, we require
Nij = |wi||wj|
r
λ

1 − ⟨P(i,j)⟩2

, N(i⊗j) = |wi||wj|
r
λ

1 − ⟨Pi⟩2
⟨Pj⟩2

. (340)
Recall that we set the target precision to be ϵ, i.e. we would like to achieve Var
h
VN
i
= ϵ2 and hence
Eq. (328) yields
ϵ2
=
L X
i,j=1
i̸=j
w2
i w2
j

1 − ⟨Pij⟩2

Nij
+
L X
i,j=1
w2
i w2
j

1 − ⟨Pi⟩2
⟨Pj⟩2

N(i⊗j)
(341)
=
1
√
λ




L X
i,j=1
i̸=j
|wi||wj|
r
1 − ⟨Pij⟩2

+
L X
i,j=1
|wi||wj|
r
1 − ⟨Pi⟩2
⟨Pj⟩2




 . (342)
where we substitute back Eq. (340) to obtain last line. Thus, we have
√
λ =
1
ϵ2




L X
i,j=1
i̸=j
|wi||wj|
r
1 − ⟨P(i,j)⟩2

+
L X
i,j=1
|wi||wj|
r
1 − ⟨Pi⟩2
⟨Pj⟩2




 . (343)
Finally, the optimal number of total measurements are
N =
L X
i,j=1
i̸=j
Nij +
L X
i,j=1
N(i⊗j) =
√
λ




L X
i,j=1
i̸=j
|wi||wj|
r
1 − ⟨P(i,j)⟩2

+
L X
i,j=1
|wi||wj|
r
1 − ⟨Pi⟩2
⟨Pj⟩2





=
1
ϵ2




L X
i,j=1
i̸=j
|wi||wj|
r
1 − ⟨P(i,j)⟩2

+
L X
i,j=1
|wi||wj|
r
1 − ⟨Pi⟩2
⟨Pj⟩2





2
.
(344)
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 56Since bi ∈ {±1}, ⟨Pi⟩ ≤ 1 for all i. The total number of measurements is then upper bounded by
N ≤
1
ϵ2




L X
i,j=1
i̸=j
|wi||wj| +
L X
i,j=1
|wi||wj|




2
≤
1
ϵ2

2
L X
i,j=1
|wi||wj|


2
(345)
=
4
ϵ2
L X
i=1
|wi|
!2


L X
j=1
|wj|


2
=
4
ϵ2
L X
i=1
|wi|
!4
. (346)
So, the proposition’s statement is justified.
Accepted in Quantum 2025-12-16, click title to verify. Published under CC-BY 4.0. 57
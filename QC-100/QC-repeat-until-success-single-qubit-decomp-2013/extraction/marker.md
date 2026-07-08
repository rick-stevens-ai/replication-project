## Repeat-Until-Success: Non-deterministic decomposition of single-qubit unitaries

Adam Paetznick
David R. Cheriton School of Computer Science and

Institute for Quantum Computing,

University of Waterloo


Krysta M. Svore
Quantum Architectures and Computation Group,

Microsoft Research


October 21, 2014


**Abstract**


We present a decomposition technique that uses non-deterministic circuits to approximate
an arbitrary single-qubit unitary to within distance _ϵ_ and requires significantly fewer nonClifford gates than existing techniques. We develop “Repeat-Until-Success” (RUS) circuits and
characterize unitaries that can be exactly represented as an RUS circuit. Our RUS circuits
operate by conditioning on a given measurement outcome and using only a small number of
non-Clifford gates and ancilla qubits. We construct an algorithm based on RUS circuits that
approximates an arbitrary single-qubit _Z_ -axis rotation to within distance _ϵ_, where the number of
_T_ gates scales as 1 _._ 26 log2(1 _/ϵ_ ) 3 _._ 53, an improvement of roughly three-fold over state-of-the-art
_−_
techniques. We then extend our algorithm and show that a scaling of 2 _._ 4 log2(1 _/ϵ_ ) 3 _._ 28 can be
_−_
achieved for arbitrary unitaries and a small range of _ϵ_, which is roughly twice as good as optimal
deterministic decomposition methods.

### **1 Introduction**



As quantum devices continue to mature, there is an emerging need for algorithms that can efficiently
and accurately map a high-level quantum algorithm into a low-level fault-tolerant circuit representation. The mapping of a quantum algorithm into its equivalent fault-tolerant circuit representation
requires first the choice of a universal basis or gate set, and second a decomposition algorithm
that can translate a quantum circuit into a sequence of gates drawn from that basis. The choice
of basis is predominantly dictated by the existence of resource-efficient, fault-tolerant quantum
error correction protocols for each gate; a common set is CNOT plus the universal single-qubit
basis _{H, T_ _}_, where _H_ = ~~_√_~~ 12 - 11 _−_ 11 - and _T_ = - 10 _e_ _[iπ/]_ 0 [4] �. For many quantum error-correcting codes,



basis _{H, T_ _}_, where _H_ = ~~_√_~~ 12 - 11 _−_ 11 - and _T_ = - 10 _e_ _[iπ/]_ 0 [4] �. For many quantum error-correcting codes,

a fault-tolerant _H_ requires transversal application of the gate, and a fault-tolerant _T_ requires magic
state distillation. The cost of a _{H, T_ _}_ circuit is defined to be the number of _T_ gates, given that
the resource cost of a fault-tolerant _T_ gate is up to an order of magnitude larger than the resource
cost of a fault-tolerant _H_ gate [RHG07, FDJ13].



2 - 11 _−_ 11 - and _T_ =



1


The decomposition algorithm should minimize the desired cost function, such as the _T_ count
of the _ϵ_ -approximate gate sequence. The Solovay-Kitaev theorem [Kit97, KSV02], guarantees
that a single-qubit unitary operation can be efficiently approximated to within error _ϵ_ by a
sequence of _O_ (log _[c]_ (1 _/ϵ_ )) gates from a discrete universal basis, where _c_ = 1 is the theoretical lower
bound [Kni95]. Fowler gave an exponential-time algorithm that achieves the lower bound, resulting
in an approximating sequence containing 2 _._ 95 log2(1 _/ϵ_ )+3 _._ 75 _T_ gates, on average [Fow11]. However,
the exponential time complexity limits the achievable accuracy. A database search algorithm based
on canonical forms for _{H, T_ _}_ circuits was given by Bocharov and Svore [BS12] that also achieves
the lower bound and enables search to slightly better accuracy. Recently, efficient algorithms that
achieve the lower bound have been developed. Kliuchnikov, Maslov and Mosca (KMM) developed an
algorithm which yields 3 _._ 21 log2(1 _/ϵ_ ) 6 _._ 93 _T_ gates for the rotation _RZ_ (1 _/_ 10) [KMM12b]. Selinger’s
algorithm _ϵ_ -approximates a single-qubit _−_ _Z_ -axis rotation, _RZ_ ( _θ_ ) = - 10 _e_ 0 _[iθ]_ �, using 4 log2(1 _/ϵ_ ) + 11 _T_

gates in the worst case [Sel12]. Subsequent improvement by Ross and Selinger yields a scaling of
3 log(1 _/ϵ_ ) + _O_ (log log(1 _/ϵ_ )) in typical cases [RS14].
For a given single-qubit unitary _U_ and error _ϵ_, the above algorithms output a fixed sequence
of single-qubit gates from the set _{H, T_ _}_, without the use of ancillary qubits or measurements.
In this paper, we present a circuit framework and algorithm to minimize the _T_ gates required
to approximate a given single-qubit unitary. We show that by incorporating ancilla qubits and
measurements, the expected number of _T_ gates required to approximate a random _Z_ -axis rotation
can be significantly reduced to


Exp _Z_ [ _T_ ] = 1 _._ 26 log2(1 _/ϵ_ ) 3 _._ 53 _,_ (1)
_−_


an improvement of roughly three-fold over [Sel12] and more than two-fold over [Fow11], [KMM12b]
and [RS14]. For arbitrary single-qubit unitaries, our results indicate a significantly reduced _T_ -count
scaling of

Exp _U_ [ _T_ ] = 2 _._ 4 log2(1 _/ϵ_ ) 3 _._ 28 _,_ (2)
_−_

roughly 50 percent better than using (1) for each _Z_ rotation (three are required in general) and up
to four-fold better than traditional ancilla-free decomposition.

Our circuits are distinct from those output by Fowler, KMM and Selinger in that they are
_non-deterministic_ . Each circuit, when conditioned on a particular measurement outcome, exactly
implements a desired unitary, and otherwise implements a unitary that can be reversed at little
or no cost; it can then be repeated until the desired unitary is obtained. We call our circuits
“Repeat-Until-Success” (RUS) circuits. A significant advantage of RUS circuits is the extremely low

resource cost, in non-Clifford gates and ancillary qubits.

Our paper is structured as follows. We begin in Section 2 by discussing existing single-qubit
unitary decomposition techniques, and the presence of RUS circuits in previous work. We then
characterize unitaries that can be exactly implemented ( _ϵ_ = 0) as an RUS circuit in Section 3.
In Section 4, we present an optimized direct search algorithm for synthesizing RUS circuits with
extremely low _T_ count and in Section 5, we construct a corresponding database of RUS circuits.
Leveraging our database, we develop a decomposition algorithm to approximate a given unitary
using compositions of RUS circuits in Section 6. We then present a variety of applications of RUS
circuits, including a circuit for the _V_ 3 gate that results in state-of-the-art single-qubit decomposition.
Finally, we discuss future directions and open problems in Section 7.


2


### **2 Existing methods for single-qubit unitary decomposition**

In addition to the techniques discussed above [DN05, Fow11, KMM12b, Sel12, RS14], a variety of
other methods for single-qubit unitary decomposition have been developed. So-called “phase kickback”
involves preparing a special ancilla state based on the quantum Fourier transform and then using
phase estimation [KSV02]. Non-deterministic circuits called “programmable ancilla rotations”(PAR)
use a cascading set of prepared ancilla states along with gate teleportation [JWM [+] 12]. Similar use of
non-deterministic circuits to produce a “ladder” of non-stabilizer states, and in turn to approximate
an arbitrary single-qubit unitary, has also been proposed [DS12]. The number of _T_ gates required
for these ancilla-based methods is larger than for ancilla-free methods, but the total resources are
comparable in some architectures [Jon13a]. For this reason, we compare our results to the Fowler,
KMM, Selinger, and Ross-Selinger methods.

Non-deterministic circuits have also been proposed for decomposition into alternate gate sets.
Bocharov, Gurevich and Svore (BGS) showed that arbitrary single-qubit unitaries can be approximated using the gate set _H, S_ = _T_ [2] _, V_ 3, where _V_ 3 = ( _I_ + 2 _iZ_ ) _/√_ 5, with a typical scaling of
_{_ _}_



_√_



imated using the gate set _H, S_ = _T_ _, V_ 3, where _V_ 3 = ( _I_ + 2 _iZ_ ) _/_ 5, with a typical scaling of
_{_ _}_

3 log5(1 _/ϵ_ ) in the number of _V_ 3 gates [BGS13]. They suggest a fault-tolerant implementation of
the _V_ 3 gate (see Fig. 1a) using an RUS circuit which requires eight _T_ gates, four for each Toffoli
(see [Jon13b]). Later, Jones improved this circuit, using only a single Toffoli gate [Jon13a]. Using

our optimized direct search algorithm, we find an improved RUS circuit for _V_ 3 that uses only four _T_
gates, as shown in Fig. 1c, and is exact ( _ϵ_ = 0). By contrast, an approximation to within _ϵ_ = 10 _[−]_ [6]

using the KMM algorithm requires 67 _T_ gates. Furthermore, when used to implement _V_ 3, our
circuit results in _H, S, V_ 3 -decomposition achieving substantially lower _T_ count (on average) than
_{_ _}_
_{H, T_ _}_ -decomposition methods.

Repeat-until-success circuits have also been used by Wiebe and Kliuchnikov [WK13], who
proposed a family of tree-like, hierarchical RUS circuits that yield _T_ counts superior to Selinger and
KMM for small-angle _Z_ -axis rotations. In contrast, our results show that RUS circuits can be used
for large- and small-angle _Z_ -axis rotations, as well as rotations about an arbitrary axis. We also
provide a general characterization of RUS circuits, and a general framework for their construction.

A summary of the _T_ count costs of our method, labeled RUS, and the above algorithms is given
in Tables 1 and 2 for non-axial and axial rotations, respectively.

RUS circuits have been considered in other contexts, as well. The term was first used by [LBK04]
to describe the implementation of a CZ gate by repeated operations in linear optics. More
recently, [SO13] adapted deterministic ancilla-driven methods [AOK [+] 10, KOB [+] 09] to allow for
non-determinism. Our use of repetition is similar to [LBK04] and [SO13], but we generate a family
of circuits each of which are intended for use in conjunction with a fault-tolerant gate set, rather
than at the physical level.

### **3 Repeat-Until-Success circuits**



To describe RUS circuits, we begin with an example. Consider the circuit shown in Fig. 1a, which
performs the single-qubit unitary _V_ 3 = ( _I_ + 2 _iZ_ ) _/√_ 5. This circuit involves two measurements in the



_√_



performs the single-qubit unitary _V_ 3 = ( _I_ + 2 _iZ_ ) _/_ 5. This circuit involves two measurements in the

Pauli _X_ -basis. If both measurement outcomes are zero, then the output is equivalent to _V_ 3 _ψ_ . If
_|_ _⟩_
any other outcome occurs, then the output is _I |ψ⟩_ = _|ψ⟩_ . Thus, the circuit may be repeated until
obtaining the all zeros outcome, and the number of repetitions will vary according to a geometric
probability distribution. (In this case the probability of getting both zeros is 5 _/_ 8.) Upon measuring



3


|Method|Description|T count|Comments|
|---|---|---|---|
|Solovay-Kitaev<br>[DN05]|Converging _ϵ_-net<br>based on group<br>commutators.|_O_(log3_._97 1_/ϵ_)|Computationally<br>eﬃcient, but sub-optimal<br>_T_ count.|
|Ladder states<br>[DS12]|Hierarchical distillation<br>based _|H⟩_states.|_O_(log1_._75 1_/ϵ_)|Some of the cost can be<br>shifted “oﬄine”.|
|Direct search<br>[Fow11, BS12]|<br>Optimized<br>exponential-time search.|2_._95 log2(1_/ϵ_) + 3_._75|Optimal ancilla-free _T_<br>count.|
|BGS [BGS13]|Direct search<br>decomposition with _V_3.|_TV_ (3 log5 1_/ϵ_)|_TV_ is the _T_ count for<br>choice of fault-tolerant<br>implementation of _V_3.|
|**RUS**<br>(non-axial)|Database lookup.|2_._4 log2(1_/ϵ_)_ −_3_._28|Limited approximation<br>accuracy.|


Table 1: Decomposition methods for arbitrary single-qubit unitaries using the gate set _{H, S, T_ _}_ .































|Method|Description|T count|Comments|
|---|---|---|---|
|Phase kickback<br>[KSV02]|Uses Fourier states and<br>phase estimation.|_O_(log 1_/ϵ_)<br>(implementation<br>dependent)|_O_(log 1_/ϵ_) ancillas.<br>Optimizations make it<br>cost competitive with<br>Selinger and KMM.|
|PAR [JWM+12]|Cascading gate<br>teleportation.|_O_(log 1_/ϵ_)|Constant depth (on<br>average), higher _T_ count<br>than phase kickback.|
|Selinger [Sel12]|Round-oﬀfollowed by<br>exact decomposition.|4 log(1_/ϵ_) + 11|_T_ count is optimal for<br>worst-case rotations.|
|Ross-Selinger<br>[RS14]|Round-oﬀfollowed by<br>exact decomposition.|3 log(1_/ϵ_) +<br>_O_(log log 1_/ϵ_)|_T_ count is near-optimal<br>for typical rotations.|
|KMM<br>[KMM12b]|Round-oﬀfollowed by<br>exact decomposition.|3_._21 log2(1_/ϵ_)_ −_6_._93|_T_ count based on scaling<br>for _RZ_(1_/_10).|
|Floating-point<br>[WK13]|A family of tree-like RUS<br>circuits|1_._14 log2(10_γ_) +<br>8 log2(10_−γ/ϵ_)|For small angle<br>_θ_ =_ a ×_ 10_−γ_, _T_ count is<br>roughly 1_._14 log2(1_/θ_).|
|**RUS** (axial)|Database lookup.|1_._26 log2(1_/ϵ_)_ −_3_._53|Approximation to within<br>_ϵ_ = 10_−_6.|


Table 2: Decomposition methods for _Z_ -axis rotations using the gate set _{H, S, T_ _}_ . Approximation
of an arbitrary single-qubit unitary is possible by using the relation _U_ = _RZ_ ( _θ_ 1) _HRZ_ ( _θ_ 2) _HRZ_ ( _θ_ 3).


4


(c) Exp[T] _<_ 5 _._ 26



(a) Exp[T] = 12 _._ 8



|Col1|Col2|Col3|
|---|---|---|
||||
||||


(b) Exp[T] = 6 _._ 4



_√_



Figure 1: Repeat-Until-Success circuits for _V_ 3 = ( _I_ +2 _iZ_ ) _/_ 5. Each of the circuits above implements

_V_ 3 conditioned on an _X_ -basis measurement outcome of zero on each of the top two ancilla qubits. If
any other measurement outcome occurs, then each circuit implements the identity. The probability
of measuring 00 is 5 _/_ 8 for each circuit. Repeating the circuit until success yields an expectation
value for the number of _T_ gates, as indicated. (a) A slight modification of the circuit presented
in [NC00] pp. 198. Each Toffoli gate can be implemented with four _T_ gates (see [Jon13b]). (b) A
circuit proposed by Jones that requires just a single Toffoli gate [Jon13a]. (c) An alternative circuit
found by direct search. Measurement of the first qubit can be performed before interaction with
the data qubit. Thus the top-left part of the circuit can be repeated until measuring zero. The
probability of measuring zero on the first qubit is 3 _/_ 4. The probability of measuring zero on the
second qubit, conditioned on zero outcome of the first qubit, is 5 _/_ 6. The _T_ gate applied directly to
_|ψ⟩_ can be freely commuted through the CNOT. In the case that an even number of attempts are
required, the _T_ gates can be combined into the Clifford gate _T_ [2] = _S_ .



Figure 1: Repeat-Until-Success circuits for _V_ 3 = ( _I_ +2 _iZ_ ) _/_



all zeros, the unitary _V_ 3 is implemented _exactly_, even though the overall circuit is non-deterministic.

We define a Repeat-Until-Success (RUS) circuit over a gate set _G_ to be of the following general
structure:

1. Prepare _m_ ancilla qubits in the state _|_ 0 _[m]_ _⟩_ .
2. Given an input state _|ψ⟩_ on _n_ qubits, apply a unitary _W_ to all of the _n_ + _m_ qubits using gates
from _G_ .
3. Measure each ancilla qubit in the computational basis. The output is given by Φ _i_ _ψ_, where
_|_ _⟩_
Φ _i_ is a quantum channel on _n_ qubits that depends on the measurement outcome _i_ 0 _,_ 1 .
_∈{_ _}_ _[m]_
4. If the measurement outcome indicates “failure”, apply a recovery operation and repeat.


The measurement outcomes are partitioned into two sets: “success” and “failure”. Success
corresponds to some set of desired operations Φ _i_ : _i_ success ; failure corresponds to some set
_{_ _∈_ _}_
of undesired operations Φ _i_ : _i_ failure . In the case of success, no further action is required. In
_{_ _∈_ _}_
the case of failure _i_, a recovery operation Φ _[−]_ _i_ [1] is applied, and the circuit is repeated. For practical

purposes, the recovery operations should be implementable for relatively low cost compared to _W_ .

We restrict to the case in which _ψ_ is a single qubit and the Φ _i_ are unitary. We also limit
_|_ _⟩_ _{_ _}_
to a single “success” output _U |ψ⟩_, for some unitary _U_, though _U_ may correspond to multiple
measurement outcomes. The operation _W_ is then given by a 2 _[m]_ [+1] _×_ 2 _[m]_ [+1] unitary matrix of the


5


|Col1|W|Col3|
|---|---|---|
||||
||||


||0⟩|Col2|
|---|---|
|_|_0_⟩_<br>_W_<br>...<br>...<br>_|_0_⟩_<br>_{R†_<br>_i}_||
|_|_0_⟩_<br>_W_<br>...<br>...<br>_|_0_⟩_<br>_{R†_<br>_i}_||



Figure 2: A Repeat-Until-Success circuit that implements the unitary _U_ . Ancilla qubits are
prepared in _|_ 0 _⟩_, then the unitary _W_ is performed on both the ancillas and _|ψ⟩_ . Upon measuring the
ancillas, a unitary operation is effected on _ψ_ which is either _U_ or one of _Ri_, depending on the
_|_ _⟩_ _{_ _}_
measurement outcome. If the measurement outcome indicates _Ri_, then the recovery operation _Ri_ _[†]_ [is]

performed, and the process can be repeated.



form







_α_ 0 _U_ _. . ._ 







1
_W_ =
��
_i_

_[|][α][i][|]_ [2]




 _α_ 1 _R_ 1 ...


 ...

_αlRl_











_,_ (3)



where _U, R_ 1 _, . . ., Rl_ are 2 2 unitary matrices, and _α_ 0 _, . . ., αl_ C are scalars. Since the ancillas are
_×_ _∈_
prepared in _|_ 0 _[m]_ _⟩_, only the first two columns of _W_ are of consequence. Contents of the remaining
columns are essentially unrestricted, except that _W_ must be unitary. Each of the _l_ + 1 = 2 _[m]_

measurement outcomes corresponds to application of a unitary from _U_ _Ri_ on the input qubit
_∪{_ _}_
_|ψ⟩_ . Without loss of generality, we select the all zeros outcome to correspond with application of _U_,
since outcomes can be freely permuted. The entire protocol is illustrated in Fig. 2.

To ensure compatibility with existing fault-tolerance schemes, we require that _W_ can be
synthesized using the gate set _G_ = _{_ Clifford _, T_ _}_, where Clifford denotes the Clifford group generated
by _{H, S,_ CNOT _}_ ; note that our framework and algorithms can be extended to other gates sets with
little difficulty.contained in the ring extensionA unitary matrix is exactly implementable by Z[ _i,_ 1 [Thus, we require that] _{_ Clifford _[ α]_ _, T_ [0] _[U, α]_ _}_ if and only if its entries are [1] _[R]_ [1] _[, . . ., α][l][R][l]_ 1
~~_√_~~ ~~�~~ 2 [] [][GS12][].] _[∈]_ [Z][[] _[i,]_ ~~_√_~~ 2 [].]

Furthermore, the normalization 1 _/_ - _i_ [must] [also] [be] [in] [the] [ring.] [The] [unitarity] [condition] [on]

_W_ then requires that _[|][α][i][|]_ [2]

       - [2] _[k]_




[Thus, we require that] _[ α]_ [0] _[U, α]_ [1] _[R]_ [1] _[, . . ., α][l][R][l]_ 1
2 [] [][GS12][].] _[∈]_ [Z][[] _[i,]_ ~~_√_~~



2 [].]



Furthermore, the normalization 1 _/_



_i_



_αi_ = 2 _[k]_ (4)
_|_ _|_ [2]



for some integer _k_ .

If all of the recovery operations _R_ 1 _, . . ., Rl_ are exactly implementable by Clifford _, T_, then we
may assume that _α_ 1 _, . . ., αl_ _∈_ Z[ _i,_ ~~_√_~~ 12 [].] [If] _[α]_ [0] [is] [an] [integer,] [then] [Lagrange’s] _{_ [four-square] _}_ [theorem]

implies that (4) can be satisfied using at most _m_ = 2 ancilla qubits.


**3.1** **Characterization**


Consider a 2 _×_ 2 unitary matrix _U_ such that




- 1
= ~~_√_~~ 2 _[k]_ _α_


6




- _β_ 00 _β_ 01� _,_ (5)
_β_ 10 _β_ 11



_U_ =




- _u_ 00 _u_ 01
_u_ 10 _u_ 11


for _α_ R, _β_ 00 _, . . ., β_ 11 Z[ _i,_
_∈_ _∈_



for _α_ R, _β_ 00 _, . . ., β_ 11 Z[ _i,_ 2] and integer _k_ 0. We are concerned with exactly implementing
_∈_ _∈_ _≥_

_U_ only up to a global unit phase _e_ _[iφ]_ for some _φ_ _∈_ [0 _,_ 2 _π_ ). Accordingly, we may assume without
loss of generality that _α_ is real and non-negative since for any _β_ C, _[ββ][∗]_ [The] [restriction] [to]

_β_

_∈_ _|_ _|_ _[≥]_ [0.]



_√_



2] rather than Z[ _i,_ ~~_√_~~ 1




[is] [also] [without] [loss] [of] [generality,] [since] _[k]_ [can] [be] [chosen] [to] [eliminate]
2 []]




[The] [restriction] [to]
_|β|_ _[≥]_ [0.]



Z[ _i,_



_√_



2 _[k]_ _α_ we have



any denominators. Then choosing _α_ 0 =



_√_



2 _,_ (6)



~~_√_~~




~~�~~
_x_ + _y_



_α_ 0 =




~~�~~
_β_ 00 + _β_ 10 =
_|_ _|_ [2] _|_ _|_ [2]



where _x_ = _a_ [2] 00 [+] _[ c]_ 00 [2] [+] _[ a]_ 10 [2] [+] _[ c]_ 10 [2] [+ 2(] _[b]_ 00 [2] [+] _[ d]_ 00 [2] [+] _[ b]_ 10 [2] [+] _[ d]_ 10 [2] [),] _[y]_ [=] _[ a]_ [00] _[b]_ [00][ +] _[ c]_ [00] _[d]_ [00][ +] _[ a]_ [10] _[b]_ [10][ +] _[ c]_ [10] _[d]_ [10] [for]

integers _a_ 00, _b_ 00, _c_ 00, _d_ 00, _a_ 10, _b_ 10, _c_ 10, _d_ 10.



Any target unitary _U_ must have this form due to (3). In other words, the _only_ unitaries that
can be obtained by _{_ Clifford _, T_ _}_ circuits of the form shown in Fig. 2 are those that can be expressed
by entries in Z[ _i,_ _√_ 2] after multiplying by a scalar. Nonetheless, this restricted class can be used



_√_



by entries in Z[ _i,_ 2] after multiplying by a scalar. Nonetheless, this restricted class can be used

to approximate arbitrary unitaries more efficiently than unitaries limited to Z[ _i,_ ~~_√_~~ 12 [],] [as] [we] [show]



to approximate arbitrary unitaries more efficiently than unitaries limited to Z[ _i,_ ~~_√_~~ 2 [],] [as] [we] [show]

in Section 5 and Section 6.



**3.2** **Success** **probability** **and** **expected** **cost**


The success probability, i.e., the probability of obtaining the zero outcome for all ancilla measurements, can be computed from (4) and is given by



Pr[success] = _[α]_ 0 [2]



0 _α_ 0 [2]

_[α]_ [2]

2 _[k]_ 2 _[⌈]_ [2 log]

_[≤]_



0 (7)
2 _[⌈]_ [2 log][2] _[ α]_ [0] _[⌉]_ _[,]_



where since _α_ [2]



_√_



where since _α_ 0 [2] _[<]_ [2] _[k]_ [,] [we] [may] [use] _[k]_ _[≥⌈]_ [2][ log] 2 _[α]_ [0] _[⌉]_ [.] [The] [circuits] [in] [Fig.] [1][,] [for] [example,] [each] [yield]

a value of _α_ 0 = _√_ 5 and therefore a success probability of 5 _/_ 8. If _U_ appears multiple times in (3),



a value of _α_ 0 = 5 and therefore a success probability of 5 _/_ 8. If _U_ appears multiple times in (3),

then we have



Pr[success] = _[tα]_ 0 [2]



0 _tα_ 0 [2]

_[tα]_ [2]

2 _[k]_ _[≤]_ 2 _[⌈]_ [log][2]



0 (8)
2 _[⌈]_ [log][2] _[ tα]_ 0 [2] _[⌉]_ _[,]_



where _t_ is the number of times that _U_ appears. This upper bound can be made arbitrarily close to
one for large enough _t_ .

The expected number of repetitions required in order to achieve success is given by a geometric
distribution with expectation value 1 _/p_, and variance (1 _−_ _p_ ) _/p_ [2], where _p_ = Pr[success]. If _C_ ( _W_ )
is the cost of implementing the unitary _W_, then the expected cost of the RUS circuit is given by
_C_ ( _W_ ) _/p_ with a variance of _C_ ( _W_ )(1 _−_ _p_ ) _/p_ [2] . The resources required to implement a _{_ Clifford _, T_ _}_
fault-tolerant circuit are often dominated by the cost of implementing the _T_ gate. We therefore
define _C_ ( _W_ ) as the number of _T_ gates in the circuit used to implement _W_ .

The _T_ -gate count is not the only reasonable cost function. Other possibilities include circuit
size, width, area or volume, or the total number of measurements. The utility of a particular
cost function varies depending on the target quantum computing architecture. For architectures
that use the surface code, for example, total volume can be a more complete metric than _T_
count [FDJ13, Jon13a].

Here we choose to use _T_ -gate count as the cost function because it is simple, and is consistent
with other _{_ Clifford _, T_ _}_ -decomposition algorithms [KMM12a, AMMR12, Sel12, KMM12b, WK13,
GKMR13, RS14]. However, RUS circuits require techniques not present in the circuits produced
by previous decomposition methods, such as rapid classical feedback and control, and active


7


synchronization due to variable time scales per RUS circuit. Thus, while _T_ count allows for direct
comparison of RUS circuits with other methods, a more complete metric may be required in the
future for resource calculations on a particular hardware architecture.


**3.3** **Amplifying** **the** **success** **probability**


The action of the multi-qubit unitary _W_ may be described by



_W_ _|_ 0 _[m]_ _⟩|ψ⟩_ = _[√]_ _p_ _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ +




~~�~~ 1 _p_ ���Φ _⊥_ - _,_ (9)
_−_



where ��Φ _⊥_ - is a state that depends on _|ψ⟩_ and satisfies ( _|_ 0 _[m]_ _⟩⟨_ 0 _[m]_ _|⊗_ _I_ ) ��Φ _⊥_ - = 0. That is, _W_ outputs

a state which has amplitude _p_ on the “success” subspace, and amplitude 1 _p_ on the “failure”

_[√]_ _[√]_ _−_
subspace. We show that in some cases we may apply amplitude amplification to boost the success
probability and reduce the expected _T_ count of an RUS circuit.



where



��Φ _⊥_ - is a state that depends on _|ψ⟩_ and satisfies ( _|_ 0 _[m]_ _⟩⟨_ 0 _[m]_ _|⊗_ _I_ )



Traditional amplitude amplification [BHMT00] proceeds by applying the operator ( _RS_ ) _[j]_ on the
initial state _W_ _|_ 0 _[m]_ _⟩|ψ⟩_ for some integer _j_ _>_ 0 and reflections



_S_ = _I_ _−_ 2 _|_ 0 _[m]_ _⟩|ψ⟩⟨_ 0 _[m]_ _| ⟨ψ|,_



_R_ = _WSW_ _[†]_ = _I_ _−_ 2 _W_ _|_ 0 _[m]_ _⟩|ψ⟩⟨_ 0 _[m]_ _| ⟨ψ| W_ _[†]_ _._



(10)



Insinthe( _θ_ ) =two-dimensional _p_ . Thereforesubspace( _RS_ ) _[j]_ ( _W_ spanned0 _[m]_ _ψ_ by) = _{|_ sin0 _[m]_ ((2 _⟩_ _Uj |_ + 1) _ψ⟩_ _,_ �� _θ_ Φ) _⊥_ 0� _[m]_ _}_, _RSU_ _ψ_ acts+ cosas a((2rotation _j_ + 1) _θ_ )by��Φ2 _⊥θ_ �where. The

_[√]_ _|_ _⟩|_ _⟩_ _|_ _⟩_ _|_ _⟩_



In the two-dimensional subspace spanned by _{|_ 0 _[m]_ _⟩_ _U |ψ⟩_ _,_

_[j]_ _[m]_



sin( _θ_ ) = _p_ . Therefore ( _RS_ ) _[j]_ ( _W_ _|_ 0 _[m]_ _⟩|ψ⟩_ ) = sin((2 _j_ + 1) _θ_ ) _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ + cos((2 _j_ + 1) _θ_ ) ��Φ _⊥_ �. The

goal then is to choose _j_ appropriately so as to minimize the expected number of _T_ gates.

The problem in this case is that _|ψ⟩_ is unknown, and therefore we cannot directly implement _S_ .
We can, however, implement



_S_ _[′]_ = CZ( _m_ ) _⊗_ _I_ _,_ (11)



where CZ( _m_ ) = _X_ _[⊗][m]_ CZ( _m_ ) _X_ _[⊗][m]_ and CZ( _m_ ) is the generalized controlled- _Z_ gate on _m_ qubits
defined by



CZ( _m_ ) _x_ 1 _, x_ 2 _, . . ., xm_ = ( 1) _[x]_ [1] _[x]_ [2] _[...x][m]_ _x_ 1 _, x_ 2 _, . . ., xm_ _._ (12)
_|_ _⟩_ _−_ _|_ _⟩_



We could, therefore, apply ( _WS_ _[′]_ _W_ _[†]_ _S_ _[′]_ ) _[j]_ instead of ( _RS_ ) _[j]_ .



In the case _m_ = 1 (one ancilla qubit) this procedure corresponds to so-called “oblivious”
amplitude amplification.


**Lemma** **3.1** (Oblivious amplitude amplification on _n_ + 1 qubits [BCC [+] 13]) **.** _Consider_ _a_ _unitary_
_W_ _that_ _satisfies_ _(9)_ _for_ _m_ = 1 _._ _Let_ _S_ 1 := _Z_ _I._ _Then_ _for_ _any_ _j_ Z _,_
_⊗_ _∈_



( _WS_ 1 _WS_ 1) _[j]_ _W_ 0 _ψ_ = sin((2 _j_ + 1) _θ_ ) 0 _U_ _ψ_ + cos((2 _j_ + 1) _θ_ ) 1 _φ_ _,_ (13)

_−_ _|_ _⟩|_ _⟩_ _|_ _⟩_ _|_ _⟩_ _|_ _⟩|_ _⟩_



_where_ sin( _θ_ ) = _p._

_[√]_



In fact, oblivious amplitude amplification can be generalized to accommodate any number of
ancilla qubits.


**Corollary** **3.2** (Oblivious amplitude amplification on _n_ + _m_ qubits) **.** _Consider_ _a_ _unitary_ _W_ _that_
_satisfies_ _(9)._ _Oblivious_ _amplitude_ _amplification_ _on_ _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ _can_ _be_ _performed_ _using_ _the_ _operator_
_WS_ _[′]_ _W_ _[†]_ _S_ _[′]_ _,_ _where_ _S_ _[′]_ = _CZ_ ( _m_ ) _⊗_ _I._ _More_ _precisely,_ _for_ _any_ _j_ _∈_ Z



( _−WS_ _[′]_ _W_ _[†]_ _S_ _[′]_ ) _[j]_ ( _W_ _|_ 0 _[m]_ _⟩|ψ⟩_ ) = sin((2 _j_ + 1) _θ_ ) _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ + cos((2 _j_ + 1) _θ_ )

_where_ sin( _θ_ ) = _p._

_[√]_


8




  ���Φ _⊥_ _,_ (14)


_Proof._ The main technical part the proof of Lemma 3.1 in [BCC [+] 13] is accomplished by another
Lemma called the 2D Subspace Lemma (see Lemma 3 _._ 6 of [BCC [+] 13]). Like Lemma 3.1, the 2D
Subspace Lemma is stated specifically for the _m_ = 1 case. However, the proof still holds if _|_ 0 _⟩_ is
replaced by _|_ 0 _[m]_ _⟩_ . In that case, we find that the state


           - ��
���Ψ _⊥_ := _W_ _[†]_ [ �] ~~[�]~~ 1 _−_ _p |_ 0 _[m]_ _⟩_ _U |ψ⟩−_ _[√]_ _p_ ���Φ _⊥_ (15)



isbehaviorboth orthogonalof _W_ _[†]_ withinto _|_ 0 _[m]_ the _⟩|ψ_ two-dimensional _⟩_ and satisfies ( _|_ 0subspace _[m]_ _⟩⟨_ 0 _[m]_ _| ⊗_ spanned _I_ ) ��Ψ _⊥_ �by= 0. _|_ 0 _[m]_ This _⟩_ _U |ψ_ allows _⟩_ andus��Φto _⊥_ �calculate. We havethe



is both orthogonal to _|_ 0 _[m]_ _⟩|ψ⟩_ and satisfies ( _|_ 0 _[m]_ _⟩⟨_ 0 _[m]_ _| ⊗_ _I_ )



��Φ _⊥_ �. We have



_W_ _[†]_ ( _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ ) = _[√]_ _p |_ 0 _[m]_ _⟩_ _|ψ⟩_ +



�1 _p_ ���Ψ _⊥_ _−_



_W_ Φ _[⊥]_ [�]

_[†]_ [ ��]     


=



_._ (16)

~~�~~ 1 _p_ 0 _[m]_ _ψ_ _p_ ���Ψ _⊥_ _−_ _|_ _⟩|_ _⟩−_ _[√]_



Just as in [BCC [+] 13], this permits simple calculations yielding


_−_ _WS_ _[′]_ _W_ _[†]_ _S_ _[′]_ ( _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ ) = cos(2 _θ_ ) _|_ 0 _[m]_ _⟩_ _U |ψ⟩_ + sin(2 _θ_ )




  ���Φ _⊥_ (17)



and




  ���Φ _⊥_ _._ (18)




_−_ _WS_ _[′]_ _W_ _[†]_ _S_




  ���Ψ _⊥_ = sin(2 _θ_ ) 0 _[m]_ _U_ _ψ_ + cos(2 _θ_ )
_|_ _⟩_ _|_ _⟩_



The conclusion is that _−WS_ _[′]_ _W_ _[†]_ _S_ _[′]_ acts as a rotation by 2 _θ_ in the two-dimensional subspace of
interest.

If _m ≤_ 2, then _S_ _[′]_ can be implemented with only Clifford gates, i.e., _X_ and either _Z_ or CZ. Then,
for a fixed value of _j_, the total number of _T_ gates in the corresponding amplified circuit is given by
(2 _j_ + 1) _T_ 0. In order for amplitude amplification to yield an improvement in the expected number of

_T_ gates, we therefore require that


(2 _j_ + 1) sin [2] ( _θ_ ) _<_ sin [2] ((2 _j_ + 1) _θ_ ) _,_ (19)


a condition that holds if and only if 0 _≤_ _p_ _<_ 1 _/_ 3. Thus a sensible course of action is to apply
amplitude amplification for all RUS circuits for which _p <_ 1 _/_ 3, and leave higher probability circuits
unchanged.

Consider, for example, an RUS circuit that contains 15 _T_ gates and has a success probability
of 0 _._ 1. In this case, using amplitude amplification with a value of _j_ = 1 yields a new circuit with
success probability 0 _._ 676 and 45 _T_ gates, an improvement in the expected number of _T_ gates by a
factor of 2 _._ 25. The effects of amplitude amplification on our database of RUS circuits are discussed
in Section 5.

Cost analysis of amplitude amplification for circuits with more than two ancilla qubits is more
complicated because the reflection operator _S_ _[′]_ = CZ( _m_ ) is not a Clifford gate. For three ancilla
qubits, for example, _S_ _[′]_ requires the controlled-controlled- _Z_ gate, which can be implemented with 4
_T_ gates [Jon13b]. Larger versions of CZ( _m_ ) could be synthesized directly [Kli13, WGMAG13], or
by using a recursive procedure [NC00]. The circuits presented in Section 5 use at most two ancilla
qubits, however, so more complicated amplification circuits are not an issue in our analysis.


9


### **4 Direct search algorithm**

While equations (3) and (6) restrict the kinds of unitaries that can be exactly obtained with RUS

circuits, they indicate very little about how to implement the multi-qubit unitary _W_ . Given _W_
explicitly, it is possible to synthesize a corresponding _{_ Clifford _, T_ _}_ circuit with a minimum number
of _T_ gates [GKMR13], at least for _W_ with small _T_ count. However, given a unitary _U_ of the
form (5), there are potentially many choices of _W_, and an efficient way to find the _W_ that will
result in the minimum number of _T_ gates is unknown (and a direction for future research).

As a step towards synthesizing RUS circuits and understanding their scope, we design an
optimized direct search algorithm that synthesizes RUS circuits up to a given _T_ -gate count. Our
direct search algorithm is as follows:


1. Select the number of ancilla qubits and the number of gates.
2. Construct a _{_ Clifford _, T_ _}_ circuit and compute the resulting unitary matrix _W_ .
3. Partition the first two columns of _W_ into 2 _×_ 2 matrices.
4. Identify and remove matrices that are proportional to Clifford gates.
5. If the remaining matrices are all proportional to the same unitary matrix, then keep the
corresponding circuit.


We restrict the recovery operations _Ri_ of the circuits in our direct search to the set of single-qubit
Cliffords. This choice is motivated by our use of the _T_ count as a cost function; Clifford gates, and
therefore the recovery operations are assigned a cost of zero, therefore such recovery operations are
inexpensive.

In order to identify relevant search parameters for step 1 and circuit constructions for step 2, we
initially performed a random search over a wide range of circuit widths (number of qubits) and sizes
(number of gates). Our search produced ample results for small numbers of ancilla qubits, large

numbers of _T_ gates, and just one or two entangling gates. We therefore focus our current study on
circuits of the form shown in Fig. 3, which contain one ancilla qubit and two CZ gates, interleaved
with single-qubit Clifford gates.

Naively, the number of circuits of the form given in Fig. 3 is _O_ (3 _[n]_ ), where _n_ is the maximum
number of (non-CZ) gates in the circuit, and the base of three is the size of the set _{H, S, T_ _}_ . In
order to reduce the time complexity of direct search, we constructed each single-qubit gate sequence
using the canonical form proposed in [BS12]. A canonical form sequence is the product of three 2 _×_ 2
unitary matrices _g_ 2 _Cg_ 1 where _g_ 1 _, g_ 2 belong to the single-qubit Clifford group, and _C_ is the product
of some number of “syllables” _TH_ and _SHTH_ . The canonical form yields a unique representation of
all single-qubit circuits over _{H, T_ _}_ ; there are 2 _[t][−]_ [3] + 4 canonical circuits of _T_ -count at most _t_ . The
canonical representation yields more than a quadratic improvement in time complexity compared to
naive search, since the number of _T_ gates is roughly one-half the total number of gates.

In general, the canonical form requires conjugation by the full single-qubit Clifford group, which
contains 24 elements. Given a product of syllables _C_, each of the 24 [2] = 576 circuits _g_ 2 _Cg_ 1 are
unique. However, when multiple canonical form circuits are composed in a larger circuit, as in Fig. 3,
some combinations of Clifford gates can be eliminated. For example, when _g_ 2 _Cg_ 1 is applied to
the state 0, _g_ 1 need only be an element of _I, X, SH, SHX, HSH, HSHX_ since diagonal gates
_|_ _⟩_ _{_ _}_
act trivially on _|_ 0 _⟩_ . Similar simplifications for Fig. 3 are shown in Fig. 4. In total, these Clifford
optimizations further reduce the search space by a factor of more than 10 [5] .

Despite these optimizations, our direct search algorithm still requires time exponential in the
number of _T_ gates. To further reduce the time complexity, we partitioned the search into thousands


10


Figure 3: The general form of most RUS circuits in our database. Each of the gates labeled _g_
represents an element of the single-qubit Clifford group. Each of the gates labeled _C_ represents a
single-qubit canonical circuit as defined in [BS12].



_|_ 0 _⟩_ _{I, X}_ _{I, SH, HSH}_ _C_ _. . ._

(a)

|{I, SH, HSH}|Col2|C|Col4|
|---|---|---|---|
|_{I, SH, HSH}_|_{I, SH, HSH}_|_C_|_C_|
|_{I, SH, HSH}_||||



(c)



(b)

|Col1|C|Col3|{H, HS, HSH}|
|---|---|---|---|
||_C_|_C_|_{H, HS, HSH}_|
|||||



(d)



Figure 4: Some gates _g_ in Fig. 3 can be restricted to a subset of the single-qubit Clifford group.
(a) Circuits that begin with diagonal gates can be eliminated since they add a trivial phase to _|_ 0 _⟩_ .
(b) Similarly, diagonal gates have no impact on the _Z_ -basis measurement. (c) Pauli gates and _S_

gates can be commuted through the CZ and absorbed into either _|ψ⟩_ or the preceding _g_ gate. (d)
Analogously, Pauli and _S_ gates occurring before the CZ can be absorbed by the trailing _g_ gate or
by the output.


11


of small computations running in parallel on a large cluster and collected the results in a central
database. We were able to exhaustively synthesize circuits of the form given in Fig. 3 up to a total
(raw) _T_ count of 15 in roughly one week running on hundreds of cores. The results of our direct

search algorithm are presented in the next section.

### **5 Direct search results**


Our search yielded many RUS circuits that implement the same unitary _U_, but with different _T_ -gate
counts and success probabilities. To eliminate redundancy we construct a database containing only
the circuit with the minimum expected _T_ count for a given unitary _U_ . The resulting database
contains 2194 RUS circuits each of which contains at most 15 _T_ gates. Upon success, each circuit
exactly implements a unique non-Clifford single-qubit unitary _U_, and otherwise implements a
single-qubit Clifford operation. The database statistics are shown in Fig. 5. For circuits with success
probability less than 1 _/_ 3, we used amplitude amplification to improve performance (see Section 3.3).
Most RUS circuits result in high success probability and low expected _T_ count. Fig. 5b illustrates the
impact of amplitude amplification on the expected _T_ count. Amplification improved the performance
of circuits with relatively high expected _T_ count, but did not improve circuits with expected _T_
count of 30 or less. In general, RUS circuits exhibit very low expected _T_ counts around 15–20. Note
that the database also includes some circuits that were found by preliminary searches not of the
form of Fig. 3.

Of the 2194 RUS circuits, 1659 are axial rotations, i.e., unitaries which, modulo conjugation by
Cliffords, are rotations about the _Z_ -axis of the Bloch sphere, and 535 are non-axial rotations. The
number of axial rotations is noteworthy since, modulo Clifford conjugation, only one non-trivial
single-qubit rotation can be exactly synthesized with _{_ Clifford _, T_ _}_ and without measurement, namely
_T_ [KMM12a]. Our results show that _many_ axial rotations can be implemented exactly (conditioned
on success) when measurement is allowed.

Remarkably, the non-axial rotations in our database offer an expected _T_ count that is dramatically
better than the _T_ count obtained by approximation algorithms [Sel12, KMM12b, RS14]. For each
RUS circuit in the database we computed the number of _T_ gates required to approximate the
corresponding unitary to within a distance of 10 _[−]_ [6] using the algorithm of KMM. Fig. 6 shows
the ratio of the _T_ count given by KMM vs. the expected _T_ count for the RUS circuit. (KMM
and Ross-Selinger achieve similar _T_ count scaling so we expect similar ratios when comparing
to Ross-Selinger.) Our results show a typical improvement of about a factor of three for axial
rotations and a typical improvement of about a factor of about 12 for non-axial rotations. The larger
improvement for non-axial rotations is expected since the KMM algorithm requires the unitary to
be first decomposed into a sequence of three axial rotations.

As an example, the RUS circuit shown in Fig. 7 implements the non-axial single-qubit rotation
_U_ = (2 _X_ + _√_ 2 _Y_ + _Z_ ) _/√_ 7 with four _T_ gates and a probability of success of 7 _/_ 8. By contrast,



_√_



2 _Y_ + _Z_ ) _/√_



_U_ = (2 _X_ + 2 _Y_ + _Z_ ) _/_ 7 with four _T_ gates and a probability of success of 7 _/_ 8. By contrast,

approximating _U_ to within _ϵ_ = 10 _[−]_ [6] using the KMM algorithm requires a total of 182 _T_ gates.
Thus the circuit in Fig. 7 not only implements the intended unitary exactly, but does so at a cost
over 40 times less than the best approximation methods.

Our database is too large to offer an analysis of each circuit in detail. However, we highlight
some particularly important examples. The smallest circuit in our database contains two _T_ gates
and is shown in Fig. 8. Upon measuring zero, which occurs with probability 3 _/_ 4, the circuit
implements ( _I_ + _i√_ 2 _X_ ) _/√_ 3 and upon measuring one implements _I_ . This circuit was predicted to



_√_



2 _X_ ) _/√_



3 and upon measuring one implements _I_ . This circuit was predicted to



12


1000


800


600


400


200





400


350


300


250


200


150


100


50



|amplified<br>unamplified|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|
|---|---|---|---|---|---|---|---|---|---|
|amplified<br>unamplified|amplified<br>unamplified|amplified<br>unamplified||||||||
|amplified<br>unamplified|amplified<br>unamplified|amplified<br>unamplified||||||||
|amplified<br>unamplified|amplified<br>unamplified|||||||||
|||||||||||


10 20 30 40 50 60 70 80 90 100


Expected T count


(b)



10

2 3 4 5 6 7 8 9 10 11 12 13 14 15


Raw T count


(a)



Figure 5: Statistics for the database of repeat-until-success circuits, including all circuits of the
form of Fig. 3 up to a _T_ count of 15. (a) The total number of circuits grouped by (raw) _T_ gate
count and success probability. (b) The total number of circuits grouped by expected _T_ count, both
before amplitude amplification and after amplitude amplification. The two histograms (before
amplification and after amplification) are overlayed, where the darker hatched bars indicate circuits
that are unaffected by amplification. Only circuits with an expected _T_ count of at most 100 are
shown.



exist by Gosset and Nagaj [GN13]. They required a _{_ Clifford _, T_ _}_ circuit that exactly implemented
_R_ = ( _√_ 2 _I_ _iY_ ) _/√_ 3 with a constant probability of success. The unitary implemented by Fig. 8 is



_√_



2 _I_ _−_ _iY_ ) _/√_



_R_ = ( 2 _I_ _−_ _iY_ ) _/_ 3 with a constant probability of success. The unitary implemented by Fig. 8 is

equivalent to _R_ up to conjugation by Clifford gates.

As discussed in Section 1, our database contains a circuit that implements _V_ 3. In addition to the
circuit shown in Fig. 1c, our search also found a circuit that implements _V_ 3 with the same number
of _T_ gates, but with just a single ancilla qubit, as shown in Fig. 9. The expected _T_ count of the
single-ancilla circuit is slightly worse than that of Fig. 1c, though, since all four of the _T_ gates on
the ancilla must be performed “online”.

The _V_ 3 gate is one of a family of _V_ -basis gates for which the normalization factor is 1 _/√_ 5. In

addition to single-qubit unitary decomposition based on _V_ 3, [BGS13] also offers the possibility of
decomposing single-qubit unitaries using _V_ -basis gates with normalization factors 1 _/_ _[√]_ _p_ where _p_
is a prime. These “higher-order” _V_ gates cover _SU_ (2) more rapidly than _V_ 3 and therefore offer
potentially more efficient decomposition algorithms. A number of such _V_ -basis gates can be found
in our database, including axial versions for _p ∈{_ 13 _,_ 17 _,_ 29 _}_, as shown in Fig. 10, offering the first
fault-tolerant implementations of these gates. The prospect of decomposition algorithms with these
circuits is discussed in Section 6.1.



The _V_ 3 gate is one of a family of _V_ -basis gates for which the normalization factor is 1 _/_



_√_



13


500


400


300


200


100
50



|axial<br>non-axial|Col2|Col3|
|---|---|---|
|axial<br>non-axial|axial<br>non-axial||
||||


0 5 10 20 30 40


T count ratio KMM:RUS



Figure 6: RUS circuits database split into axial and non-axial single-qubit rotations. For each
circuit, the number of _T_ gates required to approximate the corresponding “success” unitary _U_ to
within 10 _[−]_ [6] was calculated using the algorithm of [KMM12b]. The _x_ -axis represents the ratio of
the KMM _T_ count vs. the expected number of _T_ gates for the RUS circuit.


_|_ 0 _⟩_ _H_ _T_ _[†]_ _H_ ~~_•_~~ ~~_•_~~ _H_ _T_ _[†]_ _H_





_ψ_
7
_|_ _⟩_



~~_√_~~ 27 _Y_ + _Z_


|Col1|H|Col3|T|Col5|H|Col7|T †|
|---|---|---|---|---|---|---|---|
|||||||||


|H|Col2|
|---|---|
|_H_||



Figure 7: An RUS circuit to implement the unitary _U_ = (2 _X_ + 2 _Y_ + _Z_ ) _/_ 7 with probability

7 _/_ 8, and _Z_ otherwise. Approximation of _U_ without ancillas requires 182 _T_ gates (roughly 40 times
more) for _ϵ_ = 10 _[−]_ [6] .



Figure 7: An RUS circuit to implement the unitary _U_ = (2 _X_ +



_√_



2 _Y_ + _Z_ ) _/√_


### **6 Applications**

One application of RUS circuits is in the construction of universal sets of gates. Our RUS circuits
offer exact, fault-tolerant implementations of a large set of single-qubit unitary gates. The Clifford
group plus any one non-Clifford gate is universal for quantum computation (see, e.g., [CAB12]
Appendix D). Thus any of our RUS circuits can be used to construct a new universal gate set. The
question, though, is whether or not RUS circuits can be used to decrease resource costs of unitary
approximation methods.

In this section, we show that RUS circuits can be used to significantly improve upon approximate
decomposition of single-qubit unitaries. First we discuss the use of our improved _V_ 3 circuit for





_√_





~~_√_~~ _i_ 32 _X_



_ψ_
3
_|_ _⟩_



Figure 8: The smallest circuit in our database. Upon measuring zero, with probability 3 _/_ 4, it
implements ( _I_ + _i√_ 2 _X_ ) _/√_ 3 on the input state _ψ_ . Upon measuring one, it implements the identity.



_√_



2 _X_ ) _/√_



3 on the input state _|ψ⟩_ . Upon measuring one, it implements the identity.



14


Figure 9: A circuit, like the circuits in Fig. 1, to implement _V_ 3 with probability 5 _/_ 8 and identity
with probability 3 _/_ 8, using only one ancilla qubit and one measurement.


_|_ 0 _⟩_ _H_ _T_ _H_ _T_ _[†]_ _H_ ~~_•_~~ _S_ _H_ _T_ _H_ _T_ _[†]_ _H_ _S_ ~~_•_~~ _H_ _T_ _H_ _T_ _[†]_ _H_



_|ψ⟩_ ~~_•_~~ ~~_•_~~ _Z_



_√_



(a) (3 _I_ + 2 _iZ_ ) _/_



13, Pr = 13 _/_ 16



_|_ 0 _⟩_ _H_ _S_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _S_ _[†]_ _H_ ~~_[•]_~~ _H_ _S_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ ~~_•_~~ _H_ _S_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _S_ _H_



_|ψ⟩_ ~~_•_~~ _X_ ~~_•_~~ _X_



_√_



(b) (4 _I_ + _iZ_ ) _/_



17, Pr _≈_ 0 _._ 985



_|_ 0 _⟩_ _H_ _T_ _H_ _T_ _H_ ~~_•_~~ _H_ _S_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _T_ _H_ _S_ _H_ ~~_•_~~ _H_ _T_ _H_ _T_ _H_



_|ψ⟩_ ~~_•_~~ _X_ ~~_•_~~ _X_



_√_



(c) (5 _I_ + 2 _iZ_ ) _/_



29, Pr _≈_ 0 _._ 774



Figure 10: RUS circuits for _V_ -basis gates with prime normalization factors (a) _p_ = 13 (b) _p_ = 17
and (c) _p_ = 29. The values under each circuit indicate the unitary effected upon success and the
success probability, respectively. Each circuit implements the identity upon failure.


15


decomposition into Clifford _, V_ 3 . Then we show how to compose RUS circuits in series in order to
_{_ _}_
expand the size and density of the database. The expanded database can be used to approximate
single-qubit unitaries up to an accuracy that is sufficient for a number of important quantum
algorithms. In particular, in Section 6.3, we show how to use circuits in our database for applications
using the quantum phase estimation algorithm.


**6.1** **Decomposition** **with** _V_ 3


The RUS circuit for _V_ 3, shown in Fig. 1c, can be used directly in the decomposition algorithm
of [BGS13]. The BGS algorithm produces an _ϵ_ -approximation of a given single-qubit unitary with
3 log5(1 _/ϵ_ ) _V_ 3 gates in most cases. Multiplying by an expected _T_ -cost of 5 _._ 26, using the circuit
in Fig. 1c, yields an algorithm with an expected _T_ count of


15 _._ 78 log5(1 _/ϵ_ ) _._ (20)


This is an improvement over the estimated _T_ count of 3(3 _._ 21 log2(3 _/ϵ_ ) 6 _._ 93) [KMM12b] for all
_−_
_ϵ <_ 0 _._ 25.

The database also contains _V_ -basis gates with prime normalization factors larger than 5.
In [BGS13], the authors conjecture that the decomposition algorithm for _p_ = 5 extends to other
primes with a _T_ -count scaling of 4 log _p_ (1 _/ϵ_ ). However, whereas _p_ = 5 requires only the single _V_ 3
gate, higher prime values require implementation of multiple _V_ gates. For simplicity, assume that
each of the required _V_ gates can be implemented with _T_ -count _Tp_ . Then the decomposition achieved
for prime _p_ will be better than that obtained with _V_ 3 if



1 _<_ [5] _[.]_ [26]
_Tp_



log5( _p_ ) _._ (21)



Unfortunately, our database contains only a single _V_ -basis gate for each of _p_ = _{_ 13 _,_ 17 _,_ 29 _}_ .
For the sake of argument, we calculate (21) under the optimistic assumption that for each _p_, the
remaining _V_ gates can someday be implemented at the same cost _Tp_ . Using the circuits in Fig. 10
we obtain


5 _._ 26 _/_ 7 _._ 38 log5 13 _≈_ 1 _._ 13 _,_ (22a)

5 _._ 26 _/_ 11 _._ 17 log5 17 _≈_ 0 _._ 83 _,_ (22b)

5 _._ 26 _/_ 14 _._ 22 log5 17 _≈_ 0 _._ 77 _._ (22c)

Based on these calculations we conclude that, while improved decomposition may be possible using
_p_ = 13, higher values of _p_ are unlikely to yield cost benefits on their own.

On the other hand, given implementations of multiple _V_ gates, there is no reason to limit to a
single value of _p_ . One could imagine an algorithm that combined multiple classes of _V_ gates, using
largely _V_ 3 and using more expensive high-order _V_ gates selectively. We do not consider such an
algorithm directly. In the next section, however, we study the effect of optimally combining all of
the RUS circuits in our database, not just _V_ gates.


**6.2** **Decomposition** **by** **composition** **of** **RUS** **circuits**


It is possible to approximate a given single-qubit unitary _U_ to within any _ϵ_ by composing Clifford
gates and circuits from our database. But finding the optimal composition sequence among all


16


possible compositions of circuits is a challenging task. Ideally, we could construct an efficient
decomposition algorithm based on algebraic characterization of the set of RUS circuits, similar
to algorithms for other gate sets [Sel12, KMM12b, BGS13, RS14]. But the current theoretical
characterization of RUS circuits remains open is a direction for future work. Here, we develop
decomposition algorithm based on exhaustive composition of RUS circuits, which is similar in nature
to the methods of [Fow11] and [BS12].

Starting with the set of RUS circuits found by our direct search algorithm, we compute all
products of pairs of circuits, keeping those that produce a unitary which is not yet in the database.
Composite circuits of arbitrary size can be constructed in this manner: triples of circuits can be
constructed from singles and pairs, and so on. Call a circuit a class- _k_ circuit if it is composed of
a _k_ -tuple of RUS circuits from the original database. Then the number _Nk_ of class- _k_ circuits is
bounded by



_Nk_ _≤_ _N_ 1 _· Nk−_ 1 _≤_ _N_ 1 _[k]_



1 _[,]_ (23)



where _N_ 1 is the number of circuits in the original database.



To manage the database expansion, we keep only those circuits that yield an expected _T_ count of
at most some fixed value _T_ 0. This has the simultaneous effect of discarding poorly performing circuits
and reducing the value of _Nk_ so that construction of class-( _k_ + 1) circuits is less computationally
expensive. Furthermore, circuits can be partitioned into equivalence classes by Clifford conjugation.
The unitaries of the initial set of circuits are of the form _g_ 0 _Ug_ 1, where _U_ is the unitary obtained
from the RUS circuit, and _g_ 0 _, g_ 1 are single-qubit Cliffords. Thus, the product of _k_ such circuits has
the form

_g_ 0 _U_ 1 _g_ 1 _U_ 2 _g_ 2 _. . . Ukgk_ _._ (24)


The set of class-( _k_ + 1) circuits can then be constructed by using


_g_ 0 _U_ 1 _g_ 1 _U_ 2 _g_ 2 _. . . Ukgk_ ( _gk′Uk_ +1 _gk_ +1) = _g_ 0 _U_ 1 _g_ 1 _U_ 2 _g_ 2 _. . . Ukgk′′Uk_ +1 _gk_ +1 _,_ (25)


so that the Clifford _gk_ is unnecessary. Furthermore, _g_ 0 can always be prepended later, and so we
instead express each class- _k_ unitary as


_U_ 1 _g_ 1 _U_ 2 _g_ 2 _. . . Uk_ _._ (26)


To find an equivalence class representative of _U_, we first remove the global phase by multiplying
by _u_ _[∗]_ _/_ - _|u|_ [2], where _u_ is the first non-zero entry in the first row of _U_ . Next, we conjugate _U_ by all

possible pairs of single-qubit Cliffords. The first element of a lexicographical sort then yields the
representative _g_ 1 _Ug_ 2 for some Cliffords _g_ 1 _, g_ 2.

Once the expanded database has been constructed up to a desired size, the decomposition
algorithm is straightforward. Given a single-qubit unitary _U_ and _ϵ ∈_ [0 _,_ 1], select all database entries
_V_ such that _D_ ( _U, V_ ) _≤_ _ϵ_, where



_D_ ( _U, V_ ) =




~~�~~ 2 Tr( _U_ _[†]_ _V_ )
_−|_ _|_ (27)
2



is the distance metric defined by [Fow11] and also used by [Sel12, KMM12b, BGS13, WK13, RS14].
Then, among the selected entries, find and output the circuit with the lowest expected _T_ count.


17


**6.2.1** **Results:** **decomposition** **with** **axial** **rotations**


An arbitrary single-qubit unitary can be decomposed into a sequence of three _Z_ -axis rotations and
two Hadamard gates [NC00]. Therefore, approximate decomposition of _Z_ -axis rotations suffices to
approximate any single-qubit unitary. If we limit to _Z_ -axis, i.e, diagonal, rotations only, then a few
additional simplifications are possible. In particular, each unitary can be represented by a single real
number corresponding to the rotation angle in radians. The result of a sequence of such rotations is
then given by the sum of the angles. Furthermore, up to conjugation by _{X, S}_, all _Z_ -axis rotations
can be represented by an angle in the range [0 _, π/_ 4]. This allows for construction of a database of
_Z_ -axis rotations which is much larger than a database of arbitrary (non-axial) unitaries.

Using the database expansion procedure described above, we construct a database containing all
combinations of RUS circuits with expected _T_ count at most 30. The maximum distance (according
to (27)) between any two neighboring rotations is less than 2 _._ 8 _×_ 10 _[−]_ [6], and can be improved to
2 _×_ 10 _[−]_ [6] by selectively filling the largest gaps. So the resulting database permits approximation of
any _Z_ -axis rotation to within _ϵ_ = 10 _[−]_ [6] .

To approximate a _Z_ -axis rotation by an angle _θ_, we select all entries that are within the prescribed
distance _ϵ_, and then choose the one with the smallest expected _T_ count. This procedure is efficient
since the database can be sorted according to rotation angle. Then the subset of entries that are
within _ϵ_ can be identified by binary search.

In order to assess the performance of this method, we approximate, for various values of _ϵ_,
a sample of 10 [5] randomly generated angles in the range [0 _, π/_ 4]. Results are shown in Fig. 11
and Table 3. A fit of the mean expected _T_ count for each _ϵ_ yields a scaling given by (1), with a
slope roughly 2 _._ 4 times smaller than that reported by [KMM12b] for the rotation _RZ_ (1 _/_ 10).

By way of comparison, Wiebe and Kliuchnikov report a scaling of 1 _._ 14 log2(1 _/θ_ ) for small angles
_θ_ . However, their RUS circuits are specially designed for small angles. For arbitrary angles they
report an expected _T_ count of about


1 _._ 14 log2(10 _[γ]_ ) + 8 log2(10 _[−][γ]_ _/ϵ_ ) _,_ (28)

where _θ_ = _a ×_ 10 _[−][γ]_ for some _a ∈_ (0 _,_ 1) and integer _γ_ _>_ 0. Using (28) to calculate costs for the same
10 [5] random angles as above, we obtain a fit function of


6 log2(1 _/ϵ_ ) 2 _._ 2 _._ (29)
_−_


Equation (29) indicates that the efficiency of the circuits in [WK13] does not extend to coarse angles.
Nevertheless, in Section 6.2.2 we show how to combine the circuits of Wiebe and Kliuchnikov with
our RUS circuits to achieve good cost scaling for relatively high accuracies.

Equation (1) also implies that RUS _Z_ -axis rotations can be used to approximate _arbitrary_
single-qubit unitaries with a scaling approaching that of optimal ancilla-free decomposition. Since
an arbitrary unitary can be expressed as a product of three axial rotations, the expected _T_ count
for approximating an arbitrary single-qubit unitary is given by 3 _._ 9 log2(3 _/ϵ_ ) 8 _._ 37. On the other
_−_
hand, Fowler calculates an optimal _T_ -count of 2 _._ 95 log2(1 _/ϵ_ ) + 3 _._ 75 (on average) without using
ancillas [Fow11].

Since our circuits are non-deterministic, we are also concerned with the probability distribution
of the number of _T_ gates. For each composite circuit in the database, we calculate the variance
_σ_ [2] of the _T_ count based on the variance of each individual circuit. We then obtain a confidence


18


RUS KMM Selinger































10 [�][2] 10 [�][3] 10 [�][4] 10 [�][5] 10 [�][6] 10 [�][7] 10 [�][8] 10 [�][9]





Approximation error Ε


number of _T_

               -               


Figure 11: The expected number of _T_ gates required
to approximate a single-qubit _Z_ -axis rotation to within
a distance _ϵ_ over 10 [5] real numbers selected in the
range [0 _, π/_ 4] uniformly at random. For each value
_θ_, the RUS circuit with the smallest expected _T_ count
within _ϵ_ of the unitary _RZ_ ( _θ_ ) was selected. The mean
for each value of _ϵ_ is plotted, yielding a fit-curve of
1 _._ 26 log2(1 _/ϵ_ ) 3 _._ 53. The gray region is an estimate

_−_
of the interval containing the actual number of _T_ gates
with probability 95%. The other curves are included
for reference: KMM = 3 _._ 21 log2(1 _/ϵ_ ) 6 _._ 93 [KMM12b],
_−_
Selinger = 4 log2(1 _/ϵ_ ) + 11 [Sel12].



log10(1 _/ϵ_ ) Exp _T_ ( _σ_ [2] ) 95% ( _σ_ [2] )
_±_
1 1 _._ 1 (1 _._ 1) 1 _._ 2 (3 _._ 6)
1 _._ 5 2 _._ 9 (2 _._ 2) 2 _._ 5 (2 _._ 9)
2 4 _._ 8 (3 _._ 4) 3 _._ 1 (2 _._ 9)
2 _._ 5 6 _._ 8 (3 _._ 9) 4 _._ 0 (3 _._ 8)
3 8 _._ 8 (4 _._ 3) 4 _._ 5 (4 _._ 7)
3 _._ 5 10 _._ 9 (4 _._ 6) 4 _._ 9 (5 _._ 2)
4 12 _._ 9 (4 _._ 8) 5 _._ 4 (5 _._ 5)
4 _._ 5 15 _._ 1 (5 _._ 3) 5 _._ 9 (5 _._ 7)
5 17 _._ 4 (5 _._ 7) 6 _._ 3 (5 _._ 8)
5 _._ 5 19 _._ 6 (6 _._ 0) 6 _._ 7 (6 _._ 1)
6 22 _._ 0 (6 _._ 4) 7 _._ 1 (6 _._ 5)


Table 3: Expected _T_ count required to
approximate a random single-qubit _Z_ axis rotation with an RUS circuit. The
middle column indicates the expected _T_
count based on a sample of 10 [5] random
angles. The right-hand column indicates
the expected 95 percent confidence interval of the _T_ count for the best RUS
circuit, given a random angle _θ_ . The
variance of each expected value is indicated in parenthesis.



interval using Chevyshev’s inequality


Pr( Actual[ _T_ ] Exp[ _T_ ] _kσ_ ) _[.]_ (30)
_|_ _−_ _| ≥_ _≤_ _k_ [1][2]


Table 3 shows the mean expected _T_ count for each _ϵ_ . By also calculating the mean variance _σ_ [2], we
obtain an estimate of the corresponding 95% confidence interval, shown by the gray region in Fig. 11.
That is, for a randomly chosen angle _θ_, the actual number of _T_ gates required to implement _RZ_ ( _θ_ )
is within the given interval around 1 _._ 26 log2(1 _/ϵ_ ) 3 _._ 53, with probability 0 _._ 95.
_−_

The approximation accuracy permitted by our database is limited by computation time and
memory. To maximize efficiency, we used floating-point (accurate to 14 digits) rather than symbolic
arithmetic. Construction of all RUS circuit combinations up to expected _T_ count of 30 took
roughly 20 hours and 41 GB of memory using Mathematica. Table 4 shows the number of circuit
combinations and corresponding rotation angle densities for increasing values of the expected _T_
count. The size and density of the database increases by roughly one order of magnitude for every
five _T_ gates. We expect that with a more efficient implementation—in C/C++ for example—the
worst-case approximation accuracy could be improved.


19


Max. exp.
_T_ count Size Mean _D_ Max _D_
5 7 0 _._ 04 0 _._ 08
10 134 0 _._ 0021 0 _._ 0066
15 2079 0 _._ 00013 0 _._ 0014
20 27420 0 _._ 00001 0 _._ 00017
25 320736 0 _._ 0000009 0 _._ 000016
30 3446708 0 _._ 00000008 0 _._ 0000028


Table 4: Size and density of the _Z_ -axis rotation database according to the maximum expected
number of _T_ gates. The mean and the maximum distances between nearest neighbors is given in
columns three and four, respectively.


**6.2.2** **More** **accurate** **axial** **rotations** **using** **gearbox** **circuits**


The approximation accuracy of _Z_ -axis rotations can be improved indirectly by combining our
database of axial rotations with the floating-point approach of Wiebe and Kliuchnikov [WK13]. In
their approach, a _Z_ -axis rotation by angle _φ_ = _a ×_ 10 _[−][γ]_ is approximated with a “gearbox” circuit
that multiplies the mantissa _a ∈_ (0 _,_ 1) by the value 10 _[−][γ]_ . The _T_ count of the gearbox circuit scales
as

Exp [WK] _Z_ [ _T_ ] = 2 _T_ ( _a,_ 10 _[γ]_ _ϵ_ ) + 1 _._ 14 log2(10 _[γ]_ ) + 12 _._ 2 _,_ (31)

where _T_ ( _a, ϵ_ ) is the number of _T_ gates required to approximate _RZ_ ( _a_ ) to within a distance _ϵ_ .
In [WK13], Selinger’s algorithm is used to approximate the mantissa _a_ . However, any approximation
method may be used.

The gearbox circuits are most useful when the angle _φ_ is very small, and the number of significant
digits _m_ = log10(10 _[−][γ]_ _/ϵ_ ) is also small. In that case, (31) is largely determined by the 1 _._ 14 log2(10 _[γ]_ )
term, which scales better than any other known methods. The scaling is maintained even for very
high accuracy, so long as the required relative precision is low.

If our decomposition method based on RUS circuits is used to approximate _RZ_ ( _a_ ) (instead of
Selinger’s method), then we obtain


Exp [WK] _Z_ [ _T_ ] = 2 _._ 52 log2(10 _[−][γ]_ _/ϵ_ ) + 1 _._ 14 log2(10 _[γ]_ ) + 5 _._ 14 _,_ (32)


which is an improvement over the direct methods due to Selinger and KMM, even for large angles.
The density of the database presented in Section 6.2.1 permits a maximum of _m_ = 6 significant
digits; a larger database would permit higher precision.

If full precision is required (i.e., _γ_ = 0), then a slightly different method can be used. Given an
angle _θ_ and error 10 _[−]_ [6] _> ϵ_ 10 _[−]_ [11], an approximation of _RZ_ ( _θ_ ) can be obtained by first using the
_≥_
RUS axial rotation database to get _RZ_ ( _θ_ [˜] ) such that _θ_ _θ_ = _φ_ 10 _[−]_ [6] . Then, a gearbox circuit can
_|_ [˜] _−_ _|_ _≤_
be used to approximate _φ_ = _a_ 10 _[−][γ]_ to within the prescribed distance _ϵ_, where _RZ_ ( _a_ ) is obtained
_×_
by again using the RUS database. The expected _T_ count is estimated by



Exp [hybrid]




[hybrid] _Z_ [ _T_ ] = 1 _._ 26 log2(1 _/δ_ ) + 2 1 _._ 26 log2(10 _[−][γ]_ _/ϵ_ ) + 1 _._ 14 log2(10 _[γ]_ ) + 1 _._ 61 _,_ (33)

_·_



where _δ_ is the selected accuracy of the approximation _θ_ [˜] . Assuming _φ ≈_ _δ_ and therefore 10 _[γ]_ _≈_ 10 _/δ_,
we obtain



Exp [hybrid]



_Z_ [ _T_ ] 2 _._ 52 log2(1 _/ϵ_ ) 0 _._ 12 log2(1 _/δ_ ) 2 _._ 97 _._ (34)
_≈_ _−_ _−_



20


Thus, an effective strategy is to approximate _θ_ to the maximum accuracy permitted by the axial
RUS database ( _δ_ = 10 _[−]_ [6] ) and then approximate the remaining angle _φ_ with a gearbox circuit.

The coarse approximation _θ_ [˜] will often be better than 10 _[−]_ [6] so the actual scaling may vary
from (34). To check, we calculated for _ϵ_ _≥_ 10 _[−]_ [11], the cost of the hybrid approach for the same
100k angles used in Section 6.2.1. The results yield an empirical fit of 2 _._ 62 log2(1 _/ϵ_ ) 3 _._ 1, which is
_−_
slightly higher than (34), but still lower than that reported by KMM.

Even higher accuracy can be obtained by recursively applying the hybrid procedure. If the
mantissa _a_ of _φ_ requires more accuracy than the RUS database can provide, then _RZ_ ( _a_ ) can be
coarsely approximated using the database and the remainder can be obtained using another gearbox.
Asymptotically, such an approach has scaling Θ((1 _/ϵ_ ) [1] _[/]_ [ log][2][(1] _[/δ]_ [)] ), making it practical only for a
limited range of _ϵ >_ 10 _δ_ [2] .


**6.2.3** **Results:** **Decomposition** **with** **non-axial** **rotations**


While it suffices to use three _Z_ -axis rotations and two Hadamard gates to decompose an arbitrary

single-qubit non-axial rotation, this process, used by [KMM12b], [Sel12] and [RS14], incurs a factor of
three increase in cost, since each axial rotation must in turn be decomposed. This effect is illustrated
in Fig. 6 by the larger ratios for non-axial unitaries. Using just our axial database for non-axial
unitary decomposition results in a similar increase in cost. Although Fowler’s method [Fow11] does
not incur the additional cost for arbitrary unitaries, maintaining a scaling of 2 _._ 95 log2(1 _/ϵ_ ) + 3 _._ 75,
the method is exponential and does not achieve exact implementation for many unitaries. RUS
circuits, on the other hand, offer a large domain of exactly implementable unitaries. As Fig. 6
suggests, composing both axial and non-axial RUS circuits could yield better approximations than
using _Z_ -axis rotations alone.

Construction of the database in the non-axial case is significantly more challenging than in the
axial case. First, unitaries must be represented by three rotation angles instead of one. Second,
composition of circuits requires multiplication in the non-axial case, which is less efficient than
for the _Z_ -axis case which only requires addition. Third, organization of the database to enable
efficient lookup is more complicated; _Z_ -axis rotations can be sorted by rotation angle, while arbitrary
unitaries require a more complicated data structure such as a _k_ -d tree [DN05, Amy13].

However, we can express each unitary by its Clifford equivalence class representative (26), and
also avoid conjugating by all 576 pairs of Clifford gates. Since any single-qubit Clifford can be
written as a product _g_ 1 _g_ 2 where _g_ 1 _G_ 1, _g_ 2 _G_ 2 and
_∈_ _∈_



_G_ 1 = _I, Z, S, S_ _[†]_
_{_ _}_



(35)
_G_ 2 = _I, H, X, XH, HS, XHS, HSH, XHSH_ _,_
_{_ _}_



then we need only conjugate by _G_ 2. Each resulting unitary can then be decomposed into three
rotations

_g_ 2 _Ug_ 2 _[′]_ [=] _[ R][Z]_ [(] _[θ]_ [1][)] _[R][X]_ [(] _[θ]_ [2][)] _[R][Z]_ [(] _[θ]_ [3][)] _[.]_ (36)

The Clifford gates in _G_ 1 are diagonal and only modify _θ_ 1 and _θ_ 3. Up to conjugation by elements of
_G_ 1, we have


_RZ_ ( _θ_ 1) _RX_ ( _θ_ 2) _RZ_ ( _θ_ 3) _RZ_ ( _θ_ 1 mod _π/_ 2) _RX_ ( _θ_ 2) _RZ_ ( _θ_ 3 mod _π/_ 2) _._ (37)
_≡_

Choosing 0 _θ_ 1 _, θ_ 2 _<_ _π/_ 2, we can find an equivalence class representative without actually
_≤_
conjugating by _G_ 1, saving a factor of 576 _/_ 64 = 9.


21


50


20


10


5


2



RUS U RUS Z Fowler BGS



1
10 [�][1] 10 [�][1.5] 10 [�][2] 10 [�][2.5]



Approximation error Ε


gates required to

               -               


Figure 12: The expected number of _T_ gates required to approximate an arbitrary single-qubit
unitary to within distance _ϵ_ . Each point indicates the mean of 100 random unitaries approximated to
the corresponding accuracy with our full database of RUS circuits. With 95 percent confidence, the
solid black line has slope in the range [2 _._ 29 _,_ 2 _._ 51]. The dashed black line indicates the estimated cost
of first expressing the unitary as a product of axial rotations, and then decomposing each rotation
using the _Z_ -axis RUS database from Section 6.2.1. The solid red line indicates the scaling obtained
by using the circuit in Fig. 1c for _V_ 3 decomposition [BGS13]. The scaling is worse than the others,
but is valid for _ϵ ≥_ 10 _[−]_ [10] . The estimated scaling using exponential direct search (Fowler [Fow11]) is
shown for reference.



Using these optimizations, we construct a database of size 45526 containing all RUS circuits with
expected _T_ count at most 18. We calculated the best circuit for 100 random single-qubit unitaries
for a range of _ϵ_ 8 10 _[−]_ [3] . A fit-curve of the data yields a scaling of Exp _U_ [ _T_ ] = 2 _._ 4 log2(1 _/ϵ_ ) 3 _._ 28.
_≥_ _×_ _−_
Based on the slope, the savings is roughly 18 percent over Fowler; in absolute terms, the savings is
roughly a factor of two for modest approximation accuracy. See Fig. 12. Given the relatively large
ratios for non-axial unitaries in Fig. 6 and the fact that our database contains only a limited subset
of possible RUS circuits, by incorporating a larger set of circuits, we expect the scaling to further
improve.


**6.3** **Quantum** **algorithms** **using** **coarse** **angles**


The accuracy of our decomposition method is limited by the size of the database. Our _Z_ -axis
rotation database is capable of approximating arbitrary rotations up to an accuracy of 10 _[−]_ [6] . To
achieve higher accuracy, either the database must be expanded, or an algorithmic decomposition
such as that of Section 6.1 must be used. However, a variety of important quantum algorithms
require only limited rotation accuracies. Fowler, for example, used numerical analysis to argue
that Shor’s algorithm requires rotation angles no smaller than _θ_ = _π/_ 64 _≈_ 0 _._ 05 with an with an
approximation error of _ϵ_ = _π/_ 256 _≈_ 0 _._ 012 [FH04].

Another application of coarse angles is in quantum chemistry. Consider a Hamiltonian for a


22


molecule expressed in second quantized form, where the objective is to determine the ground state
energy of the molecule. Wecker et al. [WBCT13] have developed a technique to obtain an estimate
of the energy using only angles at most 10 _[−]_ [6] accuracy in the phase estimation algorithm. Similarly,
Jones et al. show how to optimize quantum chemistry simulations by ignoring terms with small
norm [JWM [+] 12]. They use _Z_ -axis rotations with approximation accuracies in the range _ϵ_ = 10 _[−]_ [5] .
For such algorithms, our method produces rotations at the desired accuracy using extremely few _T_
gates.

### **7 Conclusions and future work**


We have presented a general framework of non-deterministic circuits called “Repeat-Until-Success”
(RUS) circuits, and characterize unitaries which can be exactly represented by a RUS circuit.

Traditional methods decompose single-qubit unitaries into deterministic sequences of gates. Wiebe
and Kliuchnikov showed that by adding measurements and allowing non-deterministic circuits,
decompositions with fewer _T_ gates are possible (in expectation) for very small _Z_ -axis rotations

[WK13]. Our results extend that conclusion to arbitrary single-qubit unitaries. By synthesizing
RUS circuits and then composing them, we can approximate arbitrary single-qubit unitaries to
within a distance of 10 _[−]_ [6], which is sufficient for many quantum algorithms. Approximation accuracy
can be improved by combining our circuits with those of [WK13]. For a random _Z_ -axis rotation, our
technique yields an approximation which requires as little as one-third as many _T_ gates as [Sel12],

[KMM12b], [RS14], and [Fow11]. Composing axial and non-axial RUS circuits yields even larger
improvements in _T_ count costs, where the approximation accuracy is limited by the size of the
database.

Our results suggest a number of possible areas for further research. First, circuits of the form
shown in Fig. 3 make up only a subset of possible RUS circuits. Expanding the search to include
additional types of circuits could improve database density. Second, a formal number-theoretic
characterization of RUS circuits needs to be made. A theoretical understanding could lead to
efficient decomposition algorithms based on RUS circuits and allow for approximation to much
smaller values of _ϵ_ .

Extensions of the RUS circuit framework to multi-qubit unitaries or non-unitary channels should
also be considered. In addition, we have restricted the setting to recovery operations that are
Clifford operators. That restriction could be modified to allow for larger or alternative classes
of operations. On the other hand, fault-tolerance schemes based on stabilizer codes often permit
the application of Pauli operators [Kni05] at no cost. Thus, it might be sensible to limit recovery
operations to only tensor products of Paulis.

Finally, the non-deterministic nature of RUS circuits imposes some additional constraints on
the overall architecture of the quantum computer. Many fault-tolerance schemes already use
non-deterministic methods to implement certain gates. But most of the non-determinism occurs
“offline”, without impacting the computational data qubits. Since RUS circuits are “online”, the time

required to implement a given unitary cannot be determined in advance. Such asynchronicity will
require extensive placement and routing techniques and classical control logic. Architecture-specific
analysis will be required in order to concretely assess the benefits of using RUS circuits.


23


### **Acknowledgements**

The authors extend thanks to Vadym Kliuchnikov, Alex Bocharov, Nathan Wiebe, Yuri Gurevich,
Andreas Blas, David Gosset and Cody Jones for helpful discussions, and to Dave Wecker for
assistance with the implementation of the direct search. Thanks also to Robin Kothari for suggesting
the amplitude amplification technique. AEP would like to thank Microsoft Research and the entire
QuArC group for their hospitality.

### **References**


[AMMR12] Matthew Amy, Dmitri Maslov, Michele Mosca, and Martin Roetteler. A meet-inthe-middle algorithm for fast synthesis of depth-optimal quantum circuits. 2012,
`[arXiv:1206.0758](http://www.arxiv.org/abs/1206.0758)` .


[Amy13] Matthew Amy. _Algorithms_ _for_ _the_ _Optimization_ _of_ _Quantum_ _Circuits_ . Master’s thesis,
University of Waterloo, 2013.


[AOK [+] 10] Janet Anders, Daniel Kuan Li Oi, Elham Kashefi, Dan E. Browne, and Erika Andersson. Ancilla-Driven Universal Quantum Computation. _Physical_ _Review_ _A_, 82:020301,
2010, `[arXiv:0911.3783](http://www.arxiv.org/abs/0911.3783)` .


[BCC [+] 13] Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and Rolando D.
Somma. Exponential improvement in precision for simulating sparse Hamiltonians.
2013, `[arXiv:1312.1414](http://www.arxiv.org/abs/1312.1414)` .


[BGS13] Alex Bocharov, Yuri Gurevich, and Krysta M. Svore. Efficient Decomposition of
Single-Qubit Gates into V Basis Circuits. _Physical_ _Review_ _A_, 88:012313, 2013,
`[arXiv:1303.1411](http://www.arxiv.org/abs/1303.1411)` .


[BHMT00] Gilles Brassard, Peter Høyer, Michele Mosca, and Alain Tapp. Quantum Amplitude
Amplification and Estimation. 2000, `[arXiv:0005055](http://www.arxiv.org/abs/0005055)` .


[BS12] Alex Bocharov and Krysta M. Svore. A Depth-Optimal Canonical Form for Singlequbit Quantum Circuits. _Physical_ _Review_ _Letters_, 109:19050, 2012, `[arXiv:1206.3223](http://www.arxiv.org/abs/1206.3223)` .


[CAB12] Earl T. Campbell, Hussain Anwar, and Dan E. Browne. Magic state distillation in all
prime dimensions using quantum Reed-Muller codes. _Physical_ _Review_ _X_, 2:041021,
2012, `[arXiv:1205.3104](http://www.arxiv.org/abs/1205.3104)` .


[DN05] Christopher M. Dawson and Michael A. Nielsen. The Solovay-Kitaev algorithm.
_Quantum_ _Information_ _and_ _Computation_, 6(1):81–95, 2005, `[arXiv:0505030](http://www.arxiv.org/abs/0505030)` .


[DS12] Guillaume Duclos-Cianci and Krysta M. Svore. A State Distillation Protocol to
Implement Arbitrary Single-qubit Rotations. _Physical_ _Review_ _A_, 88:042325, 2012,
`[arXiv:1210.1980](http://www.arxiv.org/abs/1210.1980)` .


[FDJ13] Austin G. Fowler, Simon J. Devitt, and Cody Jones. Surface code implementation of
block code state distillation. _Scientific_ _reports_, 3(1939), 2013, `[arXiv:1301.7107](http://www.arxiv.org/abs/1301.7107)` .


24


[FH04] Austin G. Fowler and Lloyd C. L. Hollenberg. Scalability of Shor’s algorithm with a
limited set of rotation gates. _Physical_ _Review_ _A_, 70:32329, 2004, `[arXiv:0306018](http://www.arxiv.org/abs/0306018)` .


[Fow11] Austin G. Fowler. Constructing arbitrary Steane code single logical qubit fault-tolerant
gates. _Quantum_ _Information_ _and_ _Computation_, 11:867–873, 2011, `[arXiv:0411206](http://www.arxiv.org/abs/0411206)` .


[GKMR13] David Gosset, Vadym Kliuchnikov, Michele Mosca, and Vincent Russo. An algorithm
for the T-count. 2013, `[arXiv:1308.4134](http://www.arxiv.org/abs/1308.4134)` .


[GN13] David Gosset and Daniel Nagaj. Quantum 3-SAT is QMA1-complete. 2013,
`[arXiv:1302.0290](http://www.arxiv.org/abs/1302.0290)` .


[GS12] Brett Giles and Peter Selinger. Exact synthesis of multi-qubit Clifford+T circuits.
_Physical_ _Review_ _A_, 87, 032332, 2012, `[arXiv:1212.0506](http://www.arxiv.org/abs/1212.0506)` .


[Jon13a] Cody Jones. _Logic_ _synthesis_ _for_ _fault-tolerant_ _quantum_ _computers_ . PhD thesis,
Stanford University, 2013, `[arXiv:1310.7290](http://www.arxiv.org/abs/1310.7290)` .


[Jon13b] Cody Jones. Low-overhead constructions for the fault-tolerant Toffoli gate. _Physical_
_Review_ _A_, 87, 022328, 2013, `[arXiv:1212.5069](http://www.arxiv.org/abs/1212.5069)` .


[JWM [+] 12] Cody Jones, James D. Whitfield, Peter L. McMahon, Man-Hong Yung, Rodney Van
Meter, Al´an Aspuru-Guzik, and Yoshihisa Yamamoto. Simulating chemistry efficiently
on fault-tolerant quantum computers. _New_ _Journal_ _of_ _Physics_, 14, 115023, 2012,
`[arXiv:1204.0567](http://www.arxiv.org/abs/1204.0567)` .


[Kit97] Alexei Y. Kitaev. Quantum computations: algorithms and error correction. _Russian_
_Mathematical_ _Surveys_, 52(6):1191–1249, 1997.


[Kli13] Vadym Kliuchnikov. Synthesis of unitaries with Clifford+T circuits. 2013,
`[arXiv:1306.3200](http://www.arxiv.org/abs/1306.3200)` .


[KMM12a] Vadym Kliuchnikov, Dmitri Maslov, and Michele Mosca. Fast and efficient exact
synthesis of single qubit unitaries generated by Clifford and T gates. _Quantum_
_Information_ _and_ _Computation_, 13(7&8):607–630, 2012, `[arXiv:1206.5236](http://www.arxiv.org/abs/1206.5236)` .


[KMM12b] Vadym Kliuchnikov, Dmitri Maslov, and Michele Mosca. Practical approximation
of single-qubit unitaries by single-qubit quantum Clifford and T circuits. 2012,
`[arXiv:1212.6964](http://www.arxiv.org/abs/1212.6964)` .


[Kni95] Emanuel Knill. Approximation by Quantum Circuits. Technical Report LAUR-952225, Los Alamos National Laboratory, 1995, `[arXiv:9508006](http://www.arxiv.org/abs/9508006)` .


[Kni05] Emanuel Knill. Quantum Computing with Very Noisy Devices. _Nature_, 434(7029):39–
44, 2005, `[arXiv:0410199](http://www.arxiv.org/abs/0410199)` .


[KOB [+] 09] Elham Kashefi, Daniel Kuan Li Oi, Daniel E. Browne, Janet Anders, and Erika
Andersson. Twisted graph states for ancilla-driven quantum computation. _Proc._ _25th_
_Conference_ _on_ _the_ _Mathematical_ _Foundations_ _of_ _Programming_ _Semantics_ _(MFPS_ _25),_
_ENTCS_, 249:307–331, 2009, `[arXiv:0905.3354](http://www.arxiv.org/abs/0905.3354)` .


25


[KSV02] Alexei Y. Kitaev, Alexander H. Shen, and Mikhail N. Vyalyi. _Classical_ _and_ _Quantum_
_Computation_ . American Mathematical Society, Providence, RI, 2002.


[LBK04] Yuan Liang Lim, Almut Beige, and Leong Chuan Kwek. Repeat-Until-Success
Quantum Computing. _Physical_ _Review_ _Letters_, 95, 030505, 2004, `[arXiv:0408043](http://www.arxiv.org/abs/0408043)` .


[NC00] Michael A. Nielsen and Isaac L. Chuang. _Quantum_ _Computation_ _and_ _Quantum_
_Information_ . Cambridge University Press, 2000.


[RHG07] Robert Raussendorf, Jim Harrington, and Kovid Goyal. Topological fault-tolerance
in cluster state quantum computation. _New_ _Journal_ _of_ _Physics_, 9(6):199–199, 2007,
`[arXiv:0703143](http://www.arxiv.org/abs/0703143)` .


[RS14] Neil J. Ross and Peter Selinger. Optimal ancilla-free Clifford+T approximation of
z-rotations. 2014, `[arXiv:1403.2975](http://www.arxiv.org/abs/1403.2975)` .


[Sel12] Peter Selinger. Efficient Clifford+T approximation of single-qubit operators. 2012,
`[arXiv:1212.6253](http://www.arxiv.org/abs/1212.6253)` .


[SO13] Kerem Halil Shah and Daniel Kuan Li Oi. Ancilla Driven Quantum Computation with arbitrary entangling strength. In _Proc._ _8th_ _Conference_ _on_ _the_ _Theory_
_of_ _Quantum_ _Computation,_ _Communication_ _and_ _Cryptography_ _(TQC_ _2013)_, 2013,
`[arXiv:1303.2066](http://www.arxiv.org/abs/1303.2066)` .


[WBCT13] Dave Wecker, Bela Bauer, Bryan Clark, and Matthias Troyer. In preparation. 2013.


[WGMAG13] Jonathan Welch, Daniel Greenbaum, Sarah Mostame, and Al´an Aspuru-Guzik.

Efficient Quantum Circuits for Diagonal Unitaries Without Ancillas. 2013,
`[arXiv:1306.3991](http://www.arxiv.org/abs/1306.3991)` .


[WK13] Nathan Wiebe and Vadym Kliuchnikov. Floating point representations in quantum
circuit synthesis. _New_ _Journal_ _of_ _Physics_, 15:093041, 2013, `[arXiv:1305.5528](http://www.arxiv.org/abs/1305.5528)` .


26



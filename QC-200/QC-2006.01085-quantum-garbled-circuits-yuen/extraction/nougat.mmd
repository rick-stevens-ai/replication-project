Quantum Garbled Circuits
Henry Yuen †

arXiv:2006.01085v2 [quant-ph] 9 Nov 2020

Zvika Brakerski *

Abstract
We present a garbling scheme for quantum circuits, thus achieving a decomposable randomized encoding scheme for quantum computation. Specifically, we show how to compute
an encoding of a given quantum circuit and quantum input, from which it is possible to derive
the output of the computation and nothing else.
In the classical setting, garbled circuits (and randomized encodings in general) are a versatile cryptographic tool with many applications such as secure multiparty computation, delegated computation, depth-reduction of cryptographic primitives, complexity lower-bounds,
and more. However, a quantum analogue for garbling general circuits was not known prior
to this work. We hope that our quantum randomized encoding scheme can similarly be useful
for applications in quantum computing and cryptography.
The properties of our scheme are as follows:
• Our scheme has perfect correctness, and has perfect information-theoretic security if we
allow the encoding size to blow-up considerably (double-exponentially in the depth of
the circuit in the worst-case). This blowup can be avoided via computational assumptions (specifically, the existence of quantum-secure pseudorandom generators). In the
computational case, the size of the encoding is proportional to the size of the circuit being
garbled, up to a polynomial in the security parameter.
• The encoding process is decomposable: each input qubit can be encoded independently,
when given access to classical randomness and EPR pairs.
• The complexity of encoding essentially matches the size of its output and furthermore it
can be computed via a constant-depth quantum circuit with bounded-arity gates as well
as quantum fan-out gates (which come “for free” in the classical setting). Formally this is
captured by the complexity class QNC0f .
To illustrate the usefulness of quantum randomized encoding, we use it to design a
conceptually-simple zero-knowledge (ZK) proof system for the complexity class QMA. Our
protocol has the so-called Σ format with a single-bit challenge, and allows the inputs to be
delayed to the last round. The only previously-known ZK Σ-protocol for QMA is due to
Broadbent and Grilo (FOCS 2020), which does not have the aforementioned properties.

* Weizmann Institute of Science, zvika.brakerski@weizmann.ac.il.

Supported by the Binational Science Foundation (Grant No. 2016726), and by the European Union Horizon 2020 Research and Innovation Program via ERC Project
REACT (Grant 756482) and via Project PROMETHEUS (Grant 780701).
†
University of Toronto. hyuen@cs.toronto.edu. Supported by a NSERC Discovery Grant.

1

Contents
1 Introduction
1.1 Quantum Randomized Encodings . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.2 Other Related Work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.3 Application: A New Zero-Knowlege Σ-Protocol for QMA . . . . . . . . . . . . . . .
1.4 Future Directions and Open Problems . . . . . . . . . . . . . . . . . . . . . . . . . . .
1.5 Paper Organization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

3
4
7
7
8
9

2 Overview of Our Construction
2.1 Our Approach: Quantum Computation via Teleportation . . . . . . . . . . . . . . . .
2.2 The Challenge: Going Beyond Clifford Gates . . . . . . . . . . . . . . . . . . . . . . .
2.3 Putting it Together . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.4 Privacy of Our Scheme . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
2.5 Another Simple QRE Using Group-Randomizing QRE . . . . . . . . . . . . . . . . .

9
9
11
14
15
15

3 Preliminaries
3.1 Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.2 Quantum Gates and Circuits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.2.1 Pauli, Clifford, and PX Groups . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.2.2 Universal Gate Set . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.2.3 Classical Circuits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3.2.4 Quantum Circuits and Their Topology . . . . . . . . . . . . . . . . . . . . . . .
3.3 Classical Randomized Encoding . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

17
17
18
18
19
19
19
21

4 Quantum Randomized Encoding – Definition and Existence
23
4.1 Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 23
4.2 Our Main Result: Existence of Decomposable Quantum Randomized Encodings . . 25
5 A New Zero-Knowledge Σ-Protocol for QMA
5.1 Building Blocks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5.2 Delayed-Input Zero-Knowledge Σ-Protocols . . . . . . . . . . . . . . . . . . . . . . .
5.3 Our Proof System . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

26
27
28
29

6 Quantum Garbled Circuits – Construction
6.1 Gadgets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.1.1 Teleportation Gadget . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.1.2 Correction Gadget . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.2 Encoding a Single Gate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.2.1 Correction Functions and Their Randomized Encoding . . . . . . . . . . . . .
6.2.2 The Gate Encoding Unitary . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.3 Encoding a Circuit and Input . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.4 Circuit Evaluation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6.5 The Simulator . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

35
35
35
36
39
40
40
41
44
46

7 Correctness and Privacy Analysis
46
7.1 Analysis of the Decoding Procedure . . . . . . . . . . . . . . . . . . . . . . . . . . . . 47
7.2 Proof of Lemma 7.1 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 50
2

A Comparison with Related Cryptographic Notions

54

B Potential Applications of QRE

55

C Proof of Proposition 6.3

57

1 Introduction
A randomized encoding (RE) of a function f is another function fˆ, computed probabilistically, such
that on every input x, the output f (x) can be recovered from fˆ(x), and no other information about f
or x is conveyed by fˆ(x). A trivial example of a RE of a function f is f itself. Things become much
more interesting when computing fˆ(x) is simpler in some way than computing f (x); for example,
fˆ(x) could be computed via a highly parallel process even if evaluating f (x) itself requires a long
sequential computation.
REs are central objects in cryptographic research and have proven useful in a multitude of
settings: the most famous example of a RE is Yao’s garbled circuits construction [Yao86], but it
was only until the work of Applebaum, Ishai and Kushilevitz in [AIK04, AIK06] that the formal
notion of randomized encodings was presented. Applications of RE range from secure multiparty computation, parallel cryptography, verifiable computation, software protection, functional
encryption, key-dependent message security, program obfuscation and more. We refer the readers
to an extensive survey by Applebaum [App17] for additional details and references. Interestingly,
REs have also proved useful in recent circuit lower bounds [CR20].
A useful feature of many randomized encodings is decomposability: this is where a function f
and a sequence of inputs (x1 , . . . , xn ) can be encoded in such a way that fˆ(x1 , . . . , xn ) = ( fˆoff , fˆ1 , . . . , fˆn )
where fˆoff (called the “offline” part of the encoding) depends only on f and the randomness r of the
encoding, and fˆi (the “online” part) only depends on xi and the randomness r. Such randomized
encodings are called decomposable.
A good illustration of the usefulness of decomposable REs (DREs) is the task of “private
simultaneous messages” (PSM) introduced by Feige, Kilian and Naor [FKN94]. In a PSM protocol
for computing a function f , a set of n separated players each have an input xi and send a message mi
to a referee, who then computes the output value y = f (x1 , . . . , xn ). The messages mi cannot reveal
any information about the xi ’s aside from the fact that f (x1 , . . . , xn ) = y (formally, the messages ei
can be simulated given y). The parties share a common random string r that is independent of
their inputs and unknown to the referee, and the goal is to accomplish this task using minimal
communication.
Using a DRE such as garbled circuits, the parties can simply send an encoding of the function f
and their respective inputs respectively to the referee. In particular, using the point-and-permute
garbled circuits scheme of Beaver, Micali and Rogaway [BMR90, Rog91], it is possible to construct
DREs with perfect decoding correctness and perfect simulation security for any function f with
complexity that scales with the formula size of f . Assuming the adversaries are computationally
bounded, it is possible to reduce this complexity to scale polynomially with the circuit size of f .
Thus, the PSM task can be performed efficiently using DREs.
In some cases, even non-decomposable REs can be useful. However, some other non-degeneracy
condition should be imposed, since (as mentioned before) every function f is trivially a nondecomposable RE of itself. For example, if for some measure of complexity, the complexity of
computing the encoding fˆ is lower than the complexity of computing f , then this can be leveraged

3

for blind delegated computation: a verifier who wishes to compute f (x) can first compute the
encoding of a function 1(x) that outputs a random string r0 if f (x) = 0, and otherwise outputs r1 .
The server can evaluate the encoding 1̂(x) to obtain either r0 or r1 , which the verifier decodes to
determine f (x). As long as the complexity of encoding 1(x) is less than f (x), this yields a non-trivial
delegation scheme.
Given the richness and utility of randomized encodings in cryptography and theoretical computer science, it is very natural to ask whether there exists a quantum analogue of randomized
encodings. Despite its appeal, this question has remained open, and as far as we know the notion
was not even formally defined in the literature before.

1.1 Quantum Randomized Encodings
In this paper we introduce the notion of randomized encodings in the quantum setting, propose
a construction, and analyze it. Our definition is an adaptation of the classical one: the quantum
randomized encoding (QRE) of a quantum operation F (represented as a quantum circuit) and a
quantum state x is another quantum state F̂(x) satisfying two properties:
1. (Correctness). The quantum state F(x) can be decoded from F̂(x).
2. (Privacy). The encoding F̂(x) reveals no information about F or x apart from the output F(x).
The privacy property is formalized by saying there is a simulator that, given F(x), can compute the
encoding F̂(x). We also refer to F̂ as the encoding of F.
Furthermore, we also define what it means for a QRE to be decomposable: the encoding F̂(x) can
be computed in a way that each qubit of the input x is encoded independently, and the encoding
takes in as input x, a classical random string r, and a sequence of EPR pairs e. 1 (See Section 4.1 for
a formal definition of (decomposable) QRE.)
For comparison of the notion of QRE with other cryptographic notions such as MPC, FHE and
program obfuscation see Appendix A.
We then present a construction of a decomposable QRE, which we call the Quantum Garbled
Circuits scheme:
Theorem 1.1 (Main result, informal). Suppose CRE is a classical DRE scheme with perfect correctness,
information-theoretic (resp. computational) privacy, and polynomial time decoding. Then there exists a
decomposable QRE scheme QGC with the following properties:
1. QGC has perfect correctness and polynomial-time decoding.
2. QGC uses CRE as a black box, and has information-theoretic (resp. computational) privacy.
3. If the encoding procedure of CRE can be computed in NC0 , then the encoding procedure of QGC can
be computed in QNC0f (i.e. the class of constant-depth quantum circuits with unbounded fan-out
gates).
(See Section 4.2 for a formal statement of our main result). We elaborate on the properties
of the QRE scheme below. It assumes the existence of a classical DRE scheme CRE with specific
correctness, privacy, and complexity properties; examples of such schemes can be found in [BMR90,
Rog91] (also see the survey in [App17]). In the case of computational privacy, we assume the
existence of quantum-secure one-way functions.


We recall that an EPR pair is the maximally entangled state √12 |00i + |11i , the quantum analogue of a pair of
classically correlated bits.
1

4

Correctness. The correctness property asserts that from an encoding F̂(x), it is possible to decode
the output state F(x) with probability 1. This is inherited from the perfect correctness property of
CRE. Furthermore, the decoding procedure preserves quantum correlations with side information:
if (x, y) denotes the joint state of the input x and some auxiliary quantum state y which may be
entangled with x, then the joint state of the output and side information after decoding is (F(x), y).
The decoding procedure also takes polynomial time in the size of encoding. This inherits the
polynomial-time decoding complexity of CRE.
Privacy. The privacy property implies that there exists a quantum algorithm Sim such that
Sim(F(x)) is indistinguishable from the encoding F̂(x), and furthermore Sim runs in time polynomial
in the size of the encoding F̂(x). The quantum scheme inherits its privacy from the classical scheme
in a black box way: if CRE is secure against all (quantum) distinguishers of size S, then QGC is
secure against distinguishers of size at most S−Λ where Λ is the complexity of decoding F̂(x) (which
is polynomial in the size of F̂(x)). Note that perfect information-theoretic privacy corresponds to
privacy against distinguishers of all sizes.
The privacy property also holds even when considering entangled side information: the joint
state (Sim(F(x)), y) (which is computed by applying F, then Sim to the input x) is indistinguishable
from (F̂(x), y).
Size of the Encoding. The size of the encoding of QGC is the number of qubits in F̂(x), which
depends on the circuit size and depth of F, and also on the size of the classical encodings computed
in the scheme CRE. For example, the classical DRE schemes from [BMR90, Rog91] with computational privacy have encoding size that scales polynomially with the circuit size of f . This translates
to the size of F̂ being polynomial in the circuit size of F. On the other hand, the known classical
decomposable RE schemes with information-theoretic privacy all have encodings fˆ that grow exponentially with the circuit depth of the function f . Using such a scheme as our CRE, the size of the
corresponding quantum encoding F̂ in our construction might grow even doubly-exponentially
with the circuit depth of the quantum operation F. Note that this is the worst-case, the exact
growth depends on the composition of gates in the circuit (see technical overview).2 However we
note that even in this case, the number of EPR pairs used in the encoding F̂(x) remains linear in
the circuit size of F.
Complexity and Locality of Encoding. The decomposability of the encoding F̂(x) is analogous
to the decomposability property of classical DRE schemes, where the encoding can be expressed
as the following concatenation:
F̂(x; r, e) = (F̂off (r, e), F̂1 (x1 ; r, e), . . . , F̂n (xn ; r, e))
where we indicate the dependency of the encoding on randomness string r and a sequence of EPR
pairs e. The state F̂off (r, e) is called the “offline” part of the encoding that depends on F but not x,
and {F̂ j (x j ; r, e)} j forms the “online” part of the encoding where x j is the j-th qubit of the n-qubit
state x.
The encoding procedure of QGC is highly parallelizable. Suppose that the encoding procedure
of CRE is computable in NC0 (which is the case for the randomized encoding schemes of [BMR90,
2
We note that an earlier version of this work claimed that the growth in the information-theoretic setting is only
(single) exponential. However we discovered an error in our original proof, and the correct analysis turns out to imply
the aforementioned parameters. We discuss the causes for this in our technical overview below.

5

Rog91]). Then the offline part F̂off (r; e) can be computed by a QNC0f circuit acting on (r, e); a
QNC0f circuit is a constant-depth circuit composed of single- and two-qubit gates, as well as fan-out
gates with unbounded arity, which implements the unitary |x, y1 , . . . , yn i → |x, x ⊕ y1 , . . . , x ⊕ yn i.
Similarly, F̂ j (x j ; r, e) can be computed by a QNC0f circuit acting on r, a constant number of qubits
of e, and the qubit x j (but does not depend on the gates of F).
We note that in the quantum setting it is not so clear what is the “correct” analogue for the
complexity class NC0 , which is the class of functions that can be computed in constant-depth, or
equivalently, functions where each output bit depends only on a constant number of input bits.
This implicitly assumes that input bits can be replicated an arbitrary number of times (for example,
all of the output bits may depend on one input bit). However, due to the No-Cloning Theorem
we cannot assume that input qubits can be copied, and thus it seems reasonable to consider
constant-depth quantum circuits augmented with fan-out gates. However, the fan-out gate does
appear to yield unexpected power in the quantum setting: for example, the parity gate can be
computed in QNC0f , while classically it is even outside AC0 (see e.g. [Moo99, HS05]). Nevertheless,
QNC0f circuits appear to be weaker than general polynomial-size quantum circuits and it may be
reasonable to assume that it will be possible to implement the fan-out gate in “constant depth” in
some quantum computing architectures (see [HS05] for discussion).
Classical Encoding for Classical Inputs. A desirable property that comes up in the quantum
setting is to allow some of the parties to remain classical, even when performing a quantum task.
In the RE setting, we would like to allow parties with a classical inputs to compute their encoding
in a classical manner (and in particular with access only to the classical part of the randomness/EPR
string). Our scheme indeed allows this type of functionality, and therefore allows applications such
as quantum PSM (as discussed above) even when some of the parties are classical. Nevertheless,
the encoding (and in particular the offline part that depends on the circuit) requires quantum
computation.
Could the encoding of a quantum circuit and classical input be made entirely classical? As we
will discuss later, this could be used to achieve general indistinguishability obfuscation for quantum circuits. However, there are certain complexity-theoretic constraints on this possibility: Applebaum showed that any language decidable by circuits that admit efficient RE with informationtheoretic security falls into the class SZK ⊆ PH [App14b]. Therefore, if we could achieve QRE with
statistical security for polynomial size quantum circuits, this would imply BQP ⊆ SZK. On the
other hand, the oracle separation between BQP and PH by Raz and Tal [RT19] suggests that this
inclusion is unlikely.3 As presented, our Quantum Garbled Circuits scheme achieves statistical
security for all quantum circuits of depth O(log log n), but with small modifications can handle an
interesting subclass of quantum circuits of depth O(log n) that is not obviously classically simulable, and thus languages computed by this subclass are not obviously contained in SZK.4 This
suggests that obtaining entirely classical encoding of quantum circuits cannot be achieved with
statistical security; whether it can be achieved with computational security remains an intriguing
open problem.
3

We thank Vinod Vaikuntanathan for pointing this out to us.
This subclass includes circuits such that the first O(log log n) layers can have arbitrary 2-qubit gates, and the
remaining layers are all Clifford gates.
4

6

1.2 Other Related Work
We mention some related work on adapting the notion of randomized encodings/garbled circuits to
the quantum setting. In [KW17], Kashefi and Wallden present an interactive, multi-round protocol
for verifiable, blind quantum computing, that is inspired by Yao’s garbled circuits. The motivation
for their protocol comes from wanting a protocol where a weak quantum client delegates a quantum
computation to a powerful quantum server, while still maintaining verifiability.
In a recent paper [Zha20] (which builds on prior work [Zha19]), Zhang presents a blind delegated quantum computation protocol that is (partially) “succinct”: it is an interactive protocol with
an initial quantum phase whose complexity is independent of the computation being delegated,
and the second phase is completely classical (with communication and round complexity that
depends on the size of the computation). The security of the protocol is proved in the random
oracle model. The construction and analysis appear to use ideas from classical garbled circuits.
Both the work of [KW17] and [Zha20] focus on protocols for delegated quantum computation,
and both protocols involve a large number of rounds of interaction that grow with the size of
the computation being delegated. In contrast, the focus of our work is on studying the notion of
quantum randomized encodings (in which the number of rounds of interaction is constant).
Finally, we mention that while our notion of quantum randomized encoding has many similarities with other commonly studied cryptographic notions such as secure multiparty computation
(MPC) and homomorphic encryption, QRE is a distinct notion with different goals. We provide a
more detailed comparison in Appendix A.

1.3 Application: A New Zero-Knowlege Σ-Protocol for QMA
To highlight the usefulness of the notion of QRE, we present an application to designing zeroknowledge (ZK) protocols for the complexity class QMA. Specifically we show how to easily
obtain 3-round “sigma” (abbreviated by Σ) protocols for QMA using QRE as a black box, and in
fact our construction achieves features that were not known before in the literature. We elaborate
more below.
Zero-knowledge proofs [GMR89] is one of the most basic and useful notions in cryptography.
Essentially, it is an interactive proof system where the verifier is guaranteed to learn nothing beyond
the validity of the statement being proven. This is formalized by showing that for any accepting
instance and any (possibly malicious) verifier, there exists a simulator which can generate a view
which is indistinguishable from the actual view of the verifier in an interaction with an honest
prover. The notion of indistinguishability depends on whether we are considering computational
or statistical zero-knowledge.
In the classical setting, the canonical ZK protocol for NP was presented by Goldreich, Micali,
and Wigderson [GMW91]. The protocol has a simple 3-message structure (known as the Σ format):
the prover sends a message, the verifier sends a uniformly random challenge, the prover responds,
and the verifier decides to accept or reject based on the transcript of the communication. Aside
from their simplicity, Σ-protocols are also desirable because it one can then use the Fiat-Shamir
heuristic [FS86] to make the protocol non-interactive, for example. In some cases, it is useful to
have a Σ-protocol with a single challenge bit. In the classical case this implies a notion known as
“special soundness” which is useful, for example, for constructing non-interactive zero-knowledge
(NIZK) protocols [BFM88, FLS90]. Another useful feature is “delayed input”, where the prover
can produce the first message without any knowledge of the instance or the witness. This is useful
for confirming well-formedness of the execution of a protocol while minimizing the number of
7

extra rounds of communication. In the classical setting Blum’s Graph-Hamiltonicity protocol
[Blu86, FLS90] has these properties and is thus often used.
Zero-knowledge proof systems for QMA, the quantum analogue of NP, have only been studied fairly recently, and known results are still few [BJSW16, VZ20, CVZ20, BG19, BS20]. Recently,
Broadbent and Grilo [BG19] presented the first ZK Σ-protocol for QMA, achieving constant soundness error. Their protocol relies on a reduction to a special variant of the local Hamiltonians
problem. It requires multi-bit challenges and does not seem to support delayed inputs.
In this work, we show a simple approach for obtaining a Σ-protocol with a single-bit challenge
and delayed-input functionality, using quantum randomized encodings. Like [BG19], our protocol
also has constant soundness error. In contrast to [BG19], we do not require a reduction to a
specific QMA-complete problem. Our approach is similar to constructions of ZK protocols from
randomized encoding in the classical setting [HV16].
Conceptually, the protocol is simple. Recall that a QMA problem L is defined by a (quantum
polynomial time) verifier circuit V, which takes a classical instance x and a quantum witness w
and decides (with all but negligible probability) whether x is a yes or no instance. We generically
create a zero-knowledge protocol, where the basic idea is as follows. The prover creates a QRE of
V, and sends it to the verifier, together with commitments to the labels and the randomness used to
generate the QRE. The verifier sends a challenge bit b. Now for b = 0 simply all the commitments
are opened and the verifier checks that indeed the proper circuit was encoded, if b = 1 then only the
labels corresponding to the actual x, w, and the verifier can thus check the value of V on them. The
actual protocol is slightly more complicated since the QRE only has “labels” for classical inputs,
and w needs to be hidden even given the labels. Therefore w is treated slightly differently than
described above (essentially “teleported” into the circuit).

1.4 Future Directions and Open Problems
We end this section with several examples of future directions and open problems.
1. Applications of QRE. We presented one application in the form of a simple zero-knowledge
protocol for QMA. Given the variety of applications of RE in classical cryptography, we
anticipate that there is similarly many analogous applications in the quantum setting. We
elaborate on several potential applications in Appendix B.
2. Obtain statistically-private QRE for all log-depth circuits. Our information-theoretic QRE
has overhead that is doubly-exponential in the depth of the circuit being encoded (although
as mentioned it should be possible to encode certain classes of circuits with “only” an
exponential overhead). Thus there is a gap between what is achievable with classical RE
(where it is possible to encode all log-depth circuits with statistical privacy). Can informationtheoretic QRE be achieved for all log-depth circuits, or is the gap inherent? We note that it is
not known whether statistically secure RE can be performed for all polynomial-size classical
circuits.
3. Completely classical encoding for quantum circuits. Can the encoding of a quantum
circuit be made completely classical? This would be very useful for obtaining obfuscation
for quantum circuits, assuming classical obfuscation.

8

1.5 Paper Organization
Section 2 contains a technical overview of our contribution. Section 3 contains notation and
preliminaries about quantum computation and classical randomized encoding. In Section 4 we
define the notion of quantum randomized encoding, state some of its basic properties and state
our main result. The details of our new zero-knowledge Σ-protocol appear in Section 5. Section 6
contains our Quantum Garbled Circuits construction and Section 7 contains proofs of correctness
and privacy. We note that there is no dependence at all (or vice versa) between the last two sections
and Section 5, and the order of reading them should be up to the reader’s preference.

Acknowledgments
We thank Sanjam Garg and Vinod Vaikuntanathan for insightful discussions. We thank Chinmay
Nirkhe for lengthy discussions about quantum garbled circuits. We thank Nir Bitansky and Omri
Shmueli for discussions on quantum zero-knowledge. We thank anonymous conference reviewers
for their helpful feedback. We thank the Simons Institute for the Theory of Computing – much
of this work was performed while the authors were visiting the Institute as a part of the Summer
Cluster on Quantum Computing (2018) and the Semester Programs on Quantum Computing and
Lattice Cryptography (2020).

2 Overview of Our Construction
We provide an overview of our techniques, we refer to the technical sections for the formal
presentation and proofs. In what follows, we use bolded variables such as q to denote density
matrices, and for a unitary U we write U(q) to denote the state UqU† (see Section 3 for more details
about notation).

2.1 Our Approach: Quantum Computation via Teleportation
The basis of our approach to quantum RE is computation by teleportation, an idea that is common to
many prior results on protocols for delegated quantum computation and computing on encrypted
data [BFK09, BJ15, DSS16]. We briefly review this concept.
Recall that quantum teleportation allows one party to transmit a qubit q to another party
using only classical communication and a preshared EPR pair e = (e1 , e2 ). Specifically, the sender
performs a measurement on the qubit q and e1 to obtain two (uniformly distributed) classical bits
a, b (often called “teleportation keys”). The receiver’s qubit e2 collapses to Xa Zb (q) where X, Z
are the bit-flip and phase-flip Pauli matrices respectively. Using the teleportation keys (a, b) the
original qubit q can be recovered.
Teleportation can be used to apply gates: let G be a single-qubit unitary (the generalization
to multi-qubit unitaries is straightforward), and suppose that the sender and receiver share the
state (e1 , G(e2 )) instead, in which G is applied to the second half of an EPR pair. When the sender
teleports the qubit q and obtains teleportation keys (a, b), the resulting state on the receiver’s side
is G(Xa Zb (q)). If G is a Clifford gate (i.e. a unitary that normalizes the Pauli group), then this is
′
′
equal to Xa Zb (G(q)) for some updated keys (a′ , b′ ) that are a deterministic function of (a, b) and G.
′
′
We call Xa Zb the Pauli error on the state.
This already suggests a method of quantum randomized encoding for the class of Clifford
circuits. Let C be a circuit consisting of gates G1 , . . . , Gm . The encoding of the circuit C and an
9

n-qubit quantum input x can be computed in the following way:
1. Generate EPR pairs ew = (ew
, ew ) for each wire w of the circuit C.5
1 2
2. For each gate Gi , if the input wires as specified by circuit C are v1 , v2 (if Gi is a two-qubit gate,
for example), then apply Gi to the “second halves” (ev21 , ev22 ) of the corresponding EPR pairs.
Note that after this operation the qubits (ev21 , ev22 ) now store the output of Gi .
3. If wire v is connected to wire w via some gate, perform the teleportation measurement on
the qubits (ev2 , ew
) to obtain classical teleportation keys (avw , bvw ).
1
4. If wire w is the i-th input wire to circuit C, then perform the teleportation measurement on
qubits (xi , ew
) to obtain classical teleportation keys (ai , bi ).
1
5. Compute from all the intermediate teleportation keys (ai , bi )i and (avw , bvw )v,w the final teleportation keys (a′j , b′j ) corresponding to the j-th output qubit, for each j. The final teleportation
keys are a deterministic function fcorr of all the intermediate teleportation keys, as well as
the gates G1 , . . . , Gm .
Each of the teleportation operations will yield uniformly random teleportation keys for each pair
of connected wires, inducing Pauli errors that accumulate as the teleported state “moves” through
the circuit. Since all gates are Clifford, the Pauli errors get adjusted in a deterministic way, and
′
′
′
′
) for output wires w will be Xa1 Zb1 ⊗ · · · ⊗ Xan Zbn (C(x)). This
the resulting state in the qubits (ew
2
output state, along with the final teleportation keys (a′j , b′j ) j , yields a QRE of circuit C and input
x, because the final state C(x) can be recovered from this, and it yields no information about the
gates or the original input x (as long as the intermediate teleportation keys are not revealed).
The quantum complexity of this encoding is quite low: preparing the EPR pairs, applying the
gates, and applying the teleportation measurements can be parallelized and thus performed in
constant-depth. However the classical complexity of this encoding is dominated by the complexity
of computing the final teleportation keys (a′j , b′j ) j , which takes time that is linear in the size of the
circuit C.
This complexity issue can be solved by leveraging classical randomized encodings (CREs): the
encoder, instead of computing (a′j , b′j ) j itself, computes a randomized encoding fˆcorr (~k) of the
function fcorr and intermediate teleportation keys ~k. Using a decomposable RE scheme such
as (classical) garbled circuits, it is possible to compute fˆcorr using a constant-depth circuit; this
encoding corresponds of an offline part fˆcorr,off and an online part that consists of labels for each bit
of the teleportation keys ~k. Thus the overall quantum encoding of C(x) will be the quantum state
′
′
′
′
Xa1 Zb1 ⊗ · · · ⊗ Xan Zbn (C(x)), along with the CRE fˆcorr (~k). The decoder can compute from the CRE
the final teleportation keys, and then recover C(x).
We see that this yields a simple QRE for Clifford circuits. If the CRE used is decomposable,
the QRE is decomposable as well: observe that the input qubits x are encoded separately from the
encoding of the circuit (the input teleportation measurements and the computation of the input
labels for fˆcorr can be done independently). Furthermore, the QRE has information-theoretic (resp.
computational) privacy if the CRE has information-theoretic privacy (resp. computational).
5

One can think of a wire as a line segment in a circuit diagram in between the gates, as well as the segments for the
inputs/output qubits.

10

2.2 The Challenge: Going Beyond Clifford Gates
The real challenge comes from dealing with the case of non-Clifford gates in the circuit (such as the
!
1
0
gate).6 The QRE described above does not work when one of the gates is a T gate; this
T=
0 eiπ/4
′
′
′
is because the gate teleportation protocol induces a non-Pauli error: T(Xa Zb (q)) = Xa Zb Pa (T(q)),
!
1 0
is the phase gate (a Clifford gate). Thus we no longer have the invariant that
where P =
0 i
the intermediate states of the teleportations are the masked by Pauli errors. This is problematic
because the errors that are induced via the sequence of teleportations will no longer be simple to
compute classically.
Instead, a phase error induced by a gate teleportation should be removed before the next
teleportation. However, there appears to be a catch-22: in order to know whether there is a phase
error, a teleportation measurement needs to be performed to get the keys (a, b). On the other
hand, the teleportation can only be performed if one was certain that there was no phase error
from previous teleportations! If the encoder wants to avoid performing a sequential computation,
it appears that both the teleportation measurements and the corresponding Pauli/phase error
corrections have to be performed by the evaluator – and this must be done in a way that does not
violate the privacy of the encoding.
We now describe the key ideas used in our Quantum Garbled Circuits scheme to handle these
issues.
Encrypted Teleportation Gadgets. First, to allow the teleportation measurements to be performed by the evaluator in a manner that maintains the privacy of the encoding, the encoder will
apply encrypted teleportation gadgets between the connected EPR pairs. For simplicitly assume that
G is a single-qubit gate in the circuit that connects wire v to wire w. The encoder applies gate
G to the EPR qubit ev2 as in the Clifford encoding, but instead of performing the teleportation
), the encoder applies the following circuit to the two qubits as
measurements on the pair (ev2 , ew
1
well as additional ancilla:7
ev2

•

•

H

|0 · · · 0i /

X(ℓz,0 )

X(ℓz,0 ⊕ ℓz,1 )

|0 · · · 0i /

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

ew
1

•

X sx

Z sz

Xtx

Ztz

Figure 1: Encrypted teleportation gadget.

Here, (ℓz,0 , ℓz,1 , ℓx,0 , ℓx,1 ) are random strings in {0, 1}κ (we will say in a moment where they come
from), and sx , sz , tx , tz are uniformly random bits. For a string r ∈ {0, 1}κ , the gate X(r) denotes the
κ-qubit gate that applies a bit-flip gate X to qubit i if ri = 1.
), but
The functionality of this circuit is to perform the teleportation measurement on (ev2 , ew
1
2
instead of obtaining teleportation keys (a, b) ∈ {0, 1} as usual, the middle two wire-bundles yield
6
Recall that when augmenting the Clifford group with any non-Clifford such as the T gate, the resulting set of gates
is universal for quantum computation.
vp
v
7
If G is a multiqubit gate, then the encoder will apply G to qubits (e21 , . . . , e2 ) before applying the teleportation
v i wi
gadget to each (e2 , e1 ).

11

teleportation labels (ℓz,a , ℓx,b ) which indicate the Pauli error Xb Za on the teleported qubit.8 As long
as the randomness used to choose (ℓz,0 , ℓz,1 , ℓx,0 , ℓx,1 ) and the bits sx , sz , tx , tz are kept secret from the
evaluator, then this circuit completely hides all information about the teleportation keys (a, b), and
thus the teleported qubit is completely randomized (from the evaluator’s point of view).
Switching The Order of Correction and Teleportation. There still is the issue that before ap), the input qubit may have a
plying the encrypted teleportation gadget to a specific pair (ev2 , ew
1
Pauli/phase error that needs correcting. For example, imagine that the qubit ev2 , originally the
second half of an EPR pair, now stores a qubit Xa Zb (q) due to a previous teleportation. When we
apply the gate G (which we again assume is a single-qubit gate for simplicity) to ev2 , we obtain
the following correction: G(Xa Zb (q)) = R(G(q)) where R is a Pauli or phase correction. We need to
avoid having the correction R before applying the teleportation gadget.
We show that we can essentially switch the order of the two operations: instead of performing
the Pauli/phase correction and then applying the encrypted teleportation gadget, we show that
a circuit similar to the teleportation gadget can be applied first by the encoder (obliviously to
whether the correction R was needed or not), and then the consequences of this bold move can
be dealt with by the encoder. More precisely, if we let TPℓ,s,t denote the encrypted teleportation
gadget, then there exist unitaries Λ1 , Λ2 , Λ3 such that the following circuit identity holds:
G
/
/
|0i

/

R

G
TPℓ,s,t

/
=

/

Λ1 (ℓ)

Λ2 (R, ℓ, s, t)

Λ3

/

|0i

Figure 2: Switching the order of correction and teleportation.

Here, Λ1 is a circuit that only depends on the labels ℓ. The circuit Λ2 depends on all parameters
R, ℓ, s, t. The circuit Λ3 does not depend on any parameters. The circuits on the right-hand side
use additional ancilla.
Thus, the encoder can first apply the gate G and then the circuit Λ1 (ℓ) to the connecting EPR
pairs and ancilla qubits, because it knows the random labels ℓ. The idea is then to offload the task
of applying the remaining circuits Λ2 (R, ℓ, s, t) and Λ3 – which we call correction gadgets – to the
evaluator in a way that hides the values of R, ℓ, s, t (and thus maintains the privacy of the encoding).
Since Λ3 doesn’t depend on any parameters, the decoder can always automatically apply this. For
Λ2 , the encoder computes a quantum randomized encoding of Λ2 (R, ℓ, s, t) — but this time we
have an easier task because Λ2 (R, ℓ, s, t) is a Clifford circuit (in fact, it comes from a special subset
of depth-1 Clifford circuits). In principle one could then recursively compute the QRE of Λ2 using
the Clifford scheme described above, but for our Quantum Garbled Circuits scheme we employ a
different method called group-randomizing QRE.
Group-Randomizing QRE. In this section we explain group-randomizing QRE in greater generality than is needed for our Quantum Garbled Circuits scheme, because we believe that it is a
8
The “label” terminology is inspired by how random labels are used to encrypt the contents of each wire in classical
garbled circuits.

12

useful conceptual framework for thinking about randomizing computations and may be useful
for other applications of QRE.
Let G denote a subgroup of the n-qubit unitary group. Let C denote a circuit computing a
unitary in G, and let x denote an input. The encoding of C(x) is a pair Ĉ(x) = (R(x), CR† ), where R
is a uniformly random9 element of G, and we assume that CR† is described using some canonical
circuit representation for elements of G. Clearly, the output C(x) can be decoded from this encoding:
the decoder simply applies CR† to R(x). This encoding is also perfectly private: for a uniformly
random R ∈ G, the unitary CR† is also uniformly distributed in G. Thus, a simulator on input
y can output (E† (y), E) for a uniformly random element E ∈ G. When y = C(x) this yields the
same distribution as the encoding Ĉ(x). We note that this method is conceptually similar to the
well-known classical RE techniques for branching programs using matrix randomization [Kil88].
For general unitaries, group-randomizing QRE is exorbitantly inefficient, because a general
unitary (even after discretization) requires exponentially many random bits to describe. However
when the group G is the Clifford group, for example, then this encoding is efficient: the n-qubit
2
Clifford group is a finite group of order 2Θ(n ) , and a uniformly random element can be sampled
in poly(n) time. Furthermore, there are efficient algorithms to compute canonical representations
of Clifford circuits [Got98, AG04]. In particular, an n-qubit Clifford unitary can always be written
as a Clifford circuit with O(n2 ) gates, and this is tight.
We now apply this group-randomizing framework to encoding the correction circuits Λ2 described above. Let G denote a unitary subgroup that contains Λ2 ; this will be a group of a special
class of depth-1 Clifford circuits. The circuits Λ2 depends on parameters R, ℓ, s, t. The parameters
(ℓ, s, t) are randomness that is known to the encoder, so this can be be fixed. However, as discussed
the correction unitary R is not known ahead of time to the encoder – it depends on the teleportation keys (a, b) of a previous gate teleportation, as well as the gate G that was involved. In fact R
is a deterministic function of (a, b), and therefore the description of Λ2 (R, ℓ, s, t) is a deterministic
function of (a, b).
To encode the circuit Λ2 (R, ℓ, s, t) with quantum input x, the encoder first samples a uniformly
random element A ∈ R. Then it applies the unitary A to the input x. This constitutes the quantum
part of the encoding.
For the classical part: let fcorr,A,ℓ,s,t(a, b) denote the function that computes a canonical description of the unitary Λ2 (R, ℓ, s, t) · A† ∈ G. Since Λ2 is a Clifford unitary on O(κ2 ) qubits (the
ancillas at the bottom of Figure 2 consist of O(κ2 ) qubits), the function fcorr,A,ℓ,s,t can be computed
by a poly(κ)-sized circuit. The encoder can then efficiently compute a classical decomposable RE
fˆcorr,A,ℓ,s,t of fcorr,A,ℓ,s,t . Since the input (a, b) is not known yet, the encoding consists of an offline
′ , ℓ′ , ℓ′ , ℓ′ ) for the 4 possible values of (a, b). The classical part of
part fˆoff and online labels (ℓz,0
z,1 x,0 x,1
the encoding of Λ2 is simply the offline part fˆoff .
Thus, the decoder has the encoding (A(x), fˆoff ). Suppose for the moment that the decoder had
two out of the four labels (ℓ′ , ℓ′ ) for some (a, b) ∈ {0, 1}2 . Then the tuple ( fˆoff , ℓ′ , ℓ′ ) denotes the
z,a

z,a

x,b

x,b

RE fˆcorr,A,ℓ,s,t(a, b), from which the value fcorr,A,ℓ,s,t (a, b) = Λ2 (R, ℓ, s, t) · A† can be efficiently decoded.
Given this, the decoder can then decode Λ2 (R, ℓ, s, t)(x), as desired. The privacy of this encoding
follows from the group-randomizing property described above.
9

For the purpose of this discussion we can always assume that G is finite.

13

2.3 Putting it Together
We now put everything together. For every pair v, w of wires in the circuit connected by a gate G,
the encoder applies the circuit Λ1 (ℓvw ) to the EPR pairs corresponding to v, w. Then, it computes
the encoding of Λ2 (·, ℓvw , svw , tvw ) as described. Here, svw , tvw are uniform randomness sampled for
every connected pair (v, w). The random labels ℓvw are generated from the classical RE fˆcorr of a Λ2
circuit corresponding to a subsequent pair (v′ , w′ ) of connected wires.
Thus, the decoder can sequentially decode each wire10 of the circuit in the following manner:
′ , ℓ′ ) resulting from a previous
inductively assume that the decoder has two-of-four labels (ℓz,a
x,b
encrypted teleportation measurement. Then the decoder can decode the group-randomizing QRE
of the Λ2 circuits, and then apply the Λ3 circuits. For each pair (v, w) of wires, the resulting state on
) will be Λ3 ·Λ2 (R, ℓ, s, t)·Λ1 (ℓ)·G, which by Figure 2 is equivalent to TPℓ,s,t ·R·G, the
the qubits (ev2 , ew
1
desired gate followed by “correct-then-teleport” operation11 Measuring the middle wire-bundles
of the teleportation gadget to obtain labels (ℓz,d , ℓx,e ) sets the decoder up for decoding a subsequent
wire pair (v′ , w′ ).
The encoder also provides a “dictionary” of labels for the output qubits, so that the decoder
can undo any final Pauli/phase errors. All together, the decoding is equivalent to a sequence
of correct-then-teleport operations, followed by a final correction, which allows the decoder to
recover the value C(x).
The encoding is constant-depth. The classical RE used in the encoding of each Λ2 circuit
can be done all in parallel and in constant-depth (assuming the CRE scheme has constant-depth
encoding). Then the quantum part of the encoding for each pair of wires (v, w) can be computed in
constant-depth, because the Λ1 circuits are constant-depth and the group G consists of constantdepth circuits.
In the setting of information-theoretic privacy, the size of the encoding grows doubly-exponentially
with the depth of the circuit. This is because if the labels ℓ for a pair of wires is κ bits, then the
corresponding teleportation gadget TPℓ,s,t has size Θ(κ), and thus the corresponding Λ2 circuit
has size Θ(κ2 ), which means that the complexity of computing the correction function fcorr is at
least Θ(κ2 ). This means that the labels for statistically-secure classical RE of fcorr are at least Ω(κ2 )
bits long. Thus the label sizes square with each layer. In the worst-case, this means that we can
only achieve efficient statistically-private encodings of O(log log n)-depth circuits.12 With some
simple modifications to this scheme, it is possible to handle certain circuits of larger depth, e.g.,
O(log n)-depth circuits where all layers except for the first O(log log n) layers consist of Clifford
gates.
In the setting of computational privacy (e.g., where we assume the existence of pseudorandom
generators), the size of the encoding is polynomial in the size of the circuit. This is because the
label sizes of computationally-secure classical RE are independent of the complexity of the function
being encoded; they only depend on the security parameter.
10

This should be viewed as analogous to the decoding in classical garbled circuits.
Again we assume that the gate G is a single-qubit gate; in the multiqubit case the gate G is “spread” across multiple
ev2 qubits.
12
In a previous version of this paper, we erroneously claimed that the label sizes grow linearly with each layer in the
information-theoretic setting, and concluded that the encoding size grows exponentially with the depth (which would
match the encoding complexity of known information-theoretic classical RE schemes). We find it an interesting problem
to determine whether we can avoid the doubly-exponential complexity blow-up for information-theoretic QRE.
11

14

2.4 Privacy of Our Scheme
The privacy properties of our randomized encoding scheme is established via the existence of a
simulator, which is an efficient procedure Sim that takes as input a quantum state F(x) for some
quantum circuit F and state x, and produces another quantum state that is indistinguishable from
the randomized encoding F̂(x). This formalizes the idea that the only thing that can be learned
from the randomized encoding F̂(x) is the value F(x).
An important feature of the randomized encoding F̂(x) is that it hides the specific names of
the gates being applied in a circuit F, and only reveals the topology of the circuit F. This feature
automatically implies the privacy of the randomized encoding: this means that it is not possible
to distinguish between the encoding of F on input x, or the encoding of a circuit E with the
same topology as F, but with all identity gates, with input F(x). In both cases, the decoding
process (which is a public procedure which does not require any secrets) produces the output F(x).
Thus, there is a canonical choice of simulator for such a randomized encoding: given input F(x),
it computes the randomized encoding Ê(F(x)), which is indistinguishable from the randomized
encoding F̂(x) via the circuit hiding property.
We now discuss a subtle point. We have described the decoding/evaluation procedure as
involving measurements: the decoder is supposed to measure the middle wire-bundles of the
teleportation gadgets to obtain the labels needed to decode the group-randomizing QRE in a
subsequent teleportation. However, there is no guarantee that a malicious evaluator (who is trying
to learn extra information from the encoding) will perform these measurements. The encoding
of a gate technically gives a superposition over all possible labels of a teleportation gadget, and
a malicious evaluator could try to perform some coherent operation to extract information about
labels for different teleportation keys simultaneously (which would in turn compromise the privacy
of the classical RE).
In our scheme, we in fact define the honest decoding procedure Dec to be unitary. The
randomization bits sx , sz , tx , tz in the teleportation gadgets, which are never revealed to the decoder,
effectively force a measurement of the teleportation gadget labels. In particular, randomizing over
the sz , tz bits destroy any coherence between the different labels in the superposition, which means
that the decoder (even a malicious one) can only get labels for a single teleportation key per
teleportation gadget at a time.
The unitarity of Dec is used in the privacy analysis in the following way: we show that
given the randomized encoding of F(x) and E(F(x)), applying a unitary decoder Dec to both states
yields outputs that are indistinguishable (statistical or computational, depending on the privacy
properties of the classical RE scheme). Thus, applying the inverse unitary Dec−1 to the outputs
preserves the indistinguishability (up to a loss related to the complexity of Dec), and shows that
the encodings of F(x) and E(F(x)) are indistinguishable.

2.5 Another Simple QRE Using Group-Randomizing QRE
We note that it is possible to construct a simpler QRE scheme for circuits using the grouprandomizing QRE in different and arguably more straightforward manner. This construction
does not have the low complexity property, or the gate-by-gate encoding property as our main
construction presented above, but it is simpler and carries conceptual resemblance to classical
branching program RE via matrix randomization as the well known Kilian RE [Kil88].
The idea is to use the “magic state” representation of quantum circuits [BK05]. At a high level
and using the terminology of this work, [BK05] shows that any quantum circuit can be represented
15

(without much loss in size and depth) by a layered circuit as follows. Each layer consists of a
unitary Clifford circuit with two types of outputs. Some of the output qubits are passed to the
next layer as inputs (hence each layer has fewer inputs than its predecessor), and some of them
are measured and the resulting classical string determines the gates that will be applied in the
next layer (the last layer of course contains no measured qubits).13 The inputs to the first layer
consist of the input to the original circuit, and in addition some auxiliary qubits, each of which
is independently sampled from an efficiently samplable distribution over single-qubit quantum
states (called “magic state”).
Given our methodology above, one can straightforwardly come up with a QRE for such circuits.
Given a circuit in the aforementioned layered form, and an input, the encoding is computed as
follows.
1. Generate the required number of magic states and concatenate them with the given input.
2. If the circuit contains only one layer, i.e. is simply a Clifford circuit, use group-randomizing
encoding (there is no need for classical RE in this case).
3. If the circuit contains more than one layer, consider the last layer (that produces the output),
we refer to the layer before last as the “predecessor layer”.
(a) Generate (classical) randomness that will allow to apply group-randomizing QRE on
the last layer (including decomposable classical RE of the classical part of the encoding).
This includes a randomizing Clifford R and randomness for classical RE.
(b) Modify the description of the predecessor layer so that instead of outputting its designated output, it essentially outputs the QRE of the last layer. Specifically, modify the
predecessor layer as follows. For the outputs that are passed to the next layer, add
an application of R before the values are actually output (since R is Clifford, the layer
remains a Clifford layer).
For the outputs that are to be measured, add a Z-twirl (i.e. Zs for a random s)14 followed
by a Clifford circuit that selects between the two labels of the classical RE of the following
(i.e. last) layer description. Also always output the (fixed classical) offline part of the
classical RE.
This transformation maintains the invariant that the new last layer (which is the augmented predecessor layer) is a Clifford circuit where the identity of the gates is determined by a classical value that comes from predecessor layers.
(c) Remove the last layer from the circuit and continue recursively.
Correctness and security follow from those of the group-randomizing QRE and the Z-twirl.
While this QRE is not natively decomposable, it can be made decomposable by adding a single
layer of teleportation-based encoding (as in our full-fledged scheme) at the input. Interestingly, the
only quantum operation required in this QRE is an application of a random Clifford on the input
(more accurately, extended input containing the actual input and a number of auxiliary qubits in
a given fixed state).
13

In fact, the [BK05] characterization is much more specific about what the layers look like and only uses very specific
classical characterization, in particular each measured bit controls one gate, but for our purposes even the above suffices.
14
Applying Zs for a randomly chosen bit s removes all information except the information that is recoverable via
measurement (in the computational basis). Therefore one can think of Z-twirl as equivalent to measurement (or as a
randomized encoding of the measurement operation).

16

Carefully keeping track of the lengths of the labels of the classical RE would imply again that
for perfect security we may incur up to a double-exponential blowup of the label length as a
function of the depth.15 In the computational setting, the blowup is only polynomial.
In terms of efficiency of encoding, we tried to present the scheme in a way that would make
it easiest to verify its correctness and security, but an efficiency-oriented description would allow
to encode all layers in parallel. This is because the modification to each layer only depends on the
randomness of the QRE of the next layer, which can be sampled ahead of time.

3 Preliminaries
3.1 Notation
Registers. A register is a named Hilbert space Cd for some dimension d. We denote registers
using sans-serif font such as a, b, c, etc. Let w1 , w2 , . . . , wn be a collection of registers. For a subset
S
S = {i1 , . . . , ik } ⊆ [n], we write wS to denote the union of registers i∈S wi . We write dim(a) to
denote the dimension of register a.
We also use underbrackets to denote the registers associated with a state, e.g.,
|ψi ,

1 X
|e, ei .
√
2 e vu

and

a

The first denotes a pure state |ψi in the register a, and the second denotes an EPR pair on registers
vu, respectively.
Quantum Random Variables. A quantum random variable (QRV) a on a register a is a density
matrix on register a. Note that we denote QRVs using bolded font. When referring to a collection
(a, b, c) of QRVs simultaneously, we are referring to the reduced density matrix of a global state on
the registers abc – we say that (a, b, c) is a joint QRV, which is also a QRV itself. We say that a QRV
a is independent of a collection of QRVs (b, c) if the density matrix corresponding to a is in tensor
product with the density matrix corresponding to (b, c). We denote this by a ⊗ (b, c).
Quantum Operations. Given a quantum operation F mapping register a to register a′ and a
collection of QRVs (a, b), we write (F(a), b) to denote the a density matrix on registers a′ b that is
the result of applying F to the density matrix (a, b). Given quantum operations F and G that act
on disjoint qubits, we write (F, G) to denote the product operation F ⊗ G. For a unitary U, we also
write U(x) as shorthand for U xU† .
Quantum Circuits and Their Descriptions. Throughout this paper we will talk about quantum
circuits both as quantum operations (e.g. a unitary), and as classical descriptions of a sequence of
gates. Formally, one is an algebraic object and the other is a classical string (using some reasonable
d
encoding format for quantum circuits). To distinguish between the two presentations we write Ckt
to denote a classical description of a circuit (i.e. a sequence of gates on some number of qubits),
and use sans-serif font such as Ckt to denote the corresponding unitary.
15
While the description above was completely sequential, one can notice that a blowup in labels of a certain gates
does not effect other gates that are in the same level in the circuit, even though the encoding is described sequentially.

17

EPR Pair.

We let |EPRi denote the maximally entangled state on two qubits, i.e. √1 (|00i + |11i).
2

Distinguishability of Quantum States. We say that two quantum states a, b on the same number
of qubits are (t, ǫ)-indistinguishable if for all auxiliary quantum states q that are unentangled with
either a or b, for all quantum circuits D of size t,
P[D(a ⊗ q) = 1] − P[D(b ⊗ q) = 1] ≤ ǫ.
We often write a ≈(t,ǫ) b to denote this. This notion of indistinguishability satisfies the triangle inequality: if a, b, c are quantum states such that a ≈(t1 ,ǫ1 ) b, and b ≈(t2 ,ǫ2 ) c, then we have
a ≈(min(t1 ,t2 ),ǫ1 +ǫ2 ) c.
Furthermore, if a ≈(t,ǫ) b and U is a size-s quantum circuit, then U(a) ≈(t−s,ǫ) U(b)). This is
because if there was a size-(t − s) circuit D that could distinguish between the two with advantage
more than ǫ, then there exists a circuit D′ = D ◦ U of size t that could distinguish between a and b
with advantage more than ǫ.

3.2 Quantum Gates and Circuits
3.2.1

Pauli, Clifford, and PX Groups

Pauli Group. The single-qubit Pauli group P consists of the group generated by the following
Pauli matrices:
!
!
!
!
1 0
0 i
0 1
1 0
Z=
Y=
X=
I=
0 −1
−i 0
1 0
0 1

The n-qubit Pauli group Pn is the n-fold tensor product of P.

Clifford Group. The n-qubit Clifford group Cn is defined to be the set of unitaries C such that
CPn C† = Pn .
√1
2

!
1 1
), and Phase
1 −1

Elements of the Clifford group are generated by CNOT, Hadamard (H =
!
1 0
) gates.
(P =
0 i
The third level of the n-qubit Clifford hierarchy (Pauli and Clifford groups being the first and
second, respectively) are unitaries U where
UPn U† = Cn .
In other words, conjugating Paulis by U yield a Clifford element.

PX Group. The following subgroup of the Clifford group, which we call the PX-group, will be
of particular interest to us. The group is defined as a group of single-qubit unitaries, and can be
extended to multiple qubits by tensoring as usual. We define the single-qubit PX-group to be the
group generated by the Pauli X gate and Phase P gate.
The aforementioned P operation is the “square root” of the Pauli Z, so P2 = Z (and therefore
the Pauli group is a subgroup of the PX-group). The Pauli group is a strict subset of the PX-group
(since the Pauli group does not contain P), and the PX-group itself is a strict subgroup of the
single-qubit Clifford group (since the PX group does not contain the Hadamard gate).
18

Calculation shows that PX = iXP3 , which implies that any element in the PX-group can be
written as ic Xa Pb , where a ∈ {0, 1} and b, c ∈ {0, 1, 2, 3}. This immediately implies that given a
circuit that contains only I, X, P gates (and of course also Z = P2 gates which are equivalent to two
consecutive applications of P), it is possible to efficiently find its canonical representation as ic Xa Pb .
We refer to such a circuit as a “PX circuit”. Given the canonical representation of a PX element, it
is possible to find a canonical PX circuit that implements the operation of the PX circuit. Since the
PX group is a group, applying a random PX operation on an arbitrary PX operation results in a
random PX operation.
3.2.2

Universal Gate Set

A universal set of gates is C2 ∪ {T}, i.e. the set of two-qubit Clifford gates along with
!
1
0
T=
.
0 eiπ/4
The T gate is an example of a unitary from the third level of the Clifford hierarchy, as formalized
in the following fact.
Fact 3.1. For all a, b ∈ {0, 1} it holds that TXa Zb = Pa Xa Zb T.
3.2.3

Classical Circuits

Here we briefly review classical circuits. A classical circuit topology T consists of a directed acyclic
graph (DAG) where the nodes are divided into input terminals, placeholder gates, and output terminals.
Input terminals have in-degree 0 and arbitrary out-degree (i.e. they are source nodes). Output
terminals have in-degree 1 and out-degree 0 (i.e. they are sink nodes). Placeholder gates have
constant in-degree and out-degree (without loss of generality this constant can be 2 while incurring
only a constant blowup in size and depth compared to any other constant). A classical circuit C
with topology T is simply an assignment of boolean functionalities to the placeholder gates.
The depth of a circuit is simply the length of the longest path from an input terminal to an
output terminal. The size of a circuit is the number of wires (i.e. edges) in the circuit topology.
An important class of circuits are constant-depth circuits. These are captured by the complexity
class NC0 , which technically consists of function families { fn } that can be computed by a family of
polynomial-size circuits whose depth is bounded by a constant (i.e. does not grow with n). As we
shall see in Section 3.3, the class NC0 captures the complexity of encoding in classical randomized
encoding schemes.
3.2.4

Quantum Circuits and Their Topology

Circuit Topology. A quantum circuit topology T is a tuple (B, I, O, W, inwire, outwire, Z, T )
where
1. GT = (B ∪ I ∪ O, W) forms a directed acyclic graph (DAG) where the vertex set consists of
the union of disjoint sets B, I, O, and the edge set is W.
2. The set of edges W are called wires of the circuit topology T .
3. The set I is ordered, and consist of input terminals, and have in-degree 0, and out-degree 1.
Throughout this paper we will overload notation and let I denote the subset of wires W
that are incident to the input terminals.
19

4. The set O is ordered, and consist of output terminals, and have in-degree 1, and out-degree
0. Throughout this paper we will overload notation and let O denote the subset of wires W
that are incident to the output terminals.
5. The vertices B are called placeholder gates, and for every 1 ∈ B, the in-degree and out-degree
of 1 are equal. We let p1 denote the degree, which we call the arity of the placeholder gate 1.
6. For every 1 ∈ B, we let inwire(1) denote an ordering of the wires w ∈ W that enter 1, and
let outwire(1) denote an ordering of the wires that exit 1.
7. The set Z is a subset of I that denotes zero qubits (i.e. qubits to initialize in the state |0i).
8. T ⊆ O denotes the set of discarded qubits (i.e. output qubits to trace out).
A topology thus specifies a quantum circuit in a natural way, except only “placeholder gates”
are specified. Note that the number of input terminals must be equal to the number of output
terminals; these correspond to the input and output wires of the circuit topology. We often let
n denote the number of input (and therefore output) terminals. Furthermore, a circuit topology
allows some input qubits to be initialized in the |0i state, and some output qubits to be traced out.
Given a topology T , we define an evaluation order π : B → |B| to be a topological ordering of
the “blank gates”.
Quantum Circuits.

A general quantum circuit F is a pair (T , G) where

T = (B, I, O, W, inwire, outwire, Z, T )
is a circuit topology and G is a set of unitaries such that for every 1 ∈ B, there is a corresponding
p1 -qubit unitary U1 ∈ G. We often write 1 ∈ G to denote the unitary itself. The size of a unitary
circuit C is the number of wires |W|. For an (n − |Z|)-qubit state w supported on the qubits not
indexed by Z, we write F(w) to denote the density matrix resulting from applying the gates 1 ∈ G
to (w, 0) where the qubits indexed by Z are set to |0i, and at the end the qubits indexed by T are
traced out.
A unitary quantum circuit C is a circuit where the set Z = T = ∅. In other words, it maps n
qubits to n qubits, and no qubits are discarded at the end.
By the Stinespring dilation theorem, every quantum operation can be realized as a general
quantum circuit. We associate the complexity of a quantum operation with the size of the quantum
circuit that implements it, with respect to a universal set of gates. For this work, we choose to
work with the universal set C2 ∪ {T} as described in Section 3.2.2.
Constant-Depth Quantum Circuits. The main model of constant-depth quantum circuits that
we consider in this paper are QNC0f circuits, which are constant-depth circuits consisting of oneor two-qubit gates, as well as fan-out gates of arbitrary arity, which copy a control qubit to a
number of target qubits (i.e., a fan-out gate with fan-out k performs the following transformation:
|x, y1 , . . . , yk i 7→ |x, y1 ⊕x, y2 ⊕x, . . . , yk ⊕xi). This is a natural analogue of classical NC0 circuits, yet is
surprisingly powerful: functions such as PARITY can be computed in this model [Moo99, HS05].
We will show that QNC0f captures the complexity of the encoding procedures of our quantum
randomized encoding scheme.

20

3.3 Classical Randomized Encoding
We define classical randomized encoding schemes and their properties. See survey by Applebaum [App17] for details and references.
Definition 3.2 (Classical Randomized Encoding). Let f ∈ {0, 1}n → {0, 1}m be some function. The
′
function fˆ : {0, 1}n ×{0, 1}ℓ → {0, 1}m is a (t, ǫ)-private classical randomized encoding (CRE) of f if there
exist a deterministic function CDec (called a decoder) and a randomized function CSim (called a
simulator) with the following properties.
• Correctness. For all x, r it holds that f (x) = CDec( fˆ(x; r)).16
• (t, ǫ)-Privacy. For all x and for all circuits D of size t it holds that
P[D( fˆ(x; r)) = 1] − P[D(CSim( f (x)) = 1] ≤ ǫ
r

where the second probability is over the randomness of the simulator CSim. The case of
ǫ = 0 is called perfect privacy.
The encoding fˆ is a decomposable CRE (DCRE) of f if there exist functions fˆoff (r) (called the offline
part of the encoding) and labi,b (r) (called the label functions) for all i ∈ [n], b ∈ {0, 1}, such that for all
(x, r),


fˆ(x; r) = fˆoff (r) , (labi,xi (r))i∈[n] .

Remark 3.3. We refer to the second input r of fˆ as the randomness of the encoding, and we use a
semicolon to distinguish it from the deterministic input x. We will sometimes write fˆ(x) to denote
the random variable f (x; r) induced by sampling r from the uniform distribution. Furthermore,
we say that the value fˆ(x) is the randomized encoding of a function f and a deterministic input x.
Note that as presented in Definition 3.2, there is no requirement that the randomized encoding
ˆ
f can be efficiently computed from the original function f . Furthermore, the decoder CDec
and simulator CSim are technically allowed to depend arbitrarily on the function f be encoded.
However, it is a highly desirable feature that randomized encodings be efficiently computable
given a description of f , and also have a universality property (see, e.g., Section 7.6.2 of [App14b]),
where the encoding fˆ(x) hides information not just about the input x, but also about the function f .
This is formalized by requiring that the decoding and simulation procedures depend only partially
on f . In many cases, including in this work, they should only depend on the topology of the circuit
computing f (see Section 3.2.3 for an overview of classical circuit topology). This motivates the
following general definition.
Definition 3.4 (Universal RE Schemes for Circuits). Let C denote a class of circuits and let R denote
an equivalence relation over C. An (t, ǫ)-private and efficient R-universal RE scheme for the class C is a
tuple of polynomial-time algorithms (CEnc, CDec, CSim) such that for all circuits f ∈ C (here we
identify the circuit with the function it computes),
• Efficient Encoding. For all x, r, CEnc( f, x; r) computes a randomized encoding fˆ(x, r).
• Correctness. For all x and r it holds that f (x) = CDec(c, fˆ(x; r)) where c denotes the equivalence class of f in R.
16

This is known as perfect correctness and is the only notion of correctness considered in this work.

21

• (t, ǫ)-Privacy. For all x and circuits D of size t it holds that
P[D( fˆ(x; r)) = 1] − P[D(CSim(c, f (x)) = 1] ≤ ǫ .
r

where c denotes the equivalence class of f in R.
Furthermore, we say that the R-universal RE scheme (CEnc, CDec, CSim) is decomposable if the
randomized encoding fˆ(x; r) is decomposable, and furthermore we say that it is label-universal if
the label functions labi,b (r) only depend on the equivalence class of f in R.
Remark 3.5 (Universal RE and Universal Circuits). For many classes of functions it is possible
to achieve universality for RE using the notion of a universal circuit (or machine). If the class of
functions admits a universal circuit (which depends on a property such as the topology but takes
the remainder of the description as input), and this universal circuit itself belongs to the class
that can be encoded using the RE scheme, then one can apply the RE to the universal circuit and
consider the description of f as additional input to the circuit. This will result in a universal RE
scheme, and if the original RE was decomposable then the resulting scheme will be decomposable
with respect to both the input and the description of the function.
For the remainder of this paper, when we speak of encoding a function f , we are referring to
encoding a specific circuit implementation of f (see Section 3.2.3). Furthermore, in this paper we will
be focused on topologically-universal RE schemes – in other words, the equivalence relation R is such
that two circuits f, f ′ are equivalent if they have the same topology (i.e. the same interconnection
between gates, but possibly different gate functionality). Randomized encoding schemes in the
literature are typically topologically-universal (for example Yao’s garbled circuits scheme).
We note that label universality can be derived from R-universality in a generic way (essentially by using a straightforward label-universal encoding of the multiplexer functions), but the
constructions we cite from the literature will have this property even without this transformation.
Existing Decomposable Classical RE Schemes. We use decomposable CRE (DCRE) as a building
block for our construction of quantum RE. In particular we rely on the following information
theoretical and computational schemes [BMR90, Rog91, App17].
Theorem 3.6 (Information Theoretic DRE). There exists an efficient topologically-universal and labeluniversal DRE scheme CRE = (CEnc, CDec, CSim) with the following properties:
• Efficiency. For every function f computable by a size-s and depth-d classical circuit and for every
input x, the encoding CEnc( f, x; r) is computable in time poly(2d )·s. Furthermore, the label functions
labi,b (r) are computable in time poly(2d ). The decoding and simulation algorithms CDec and CSim
are also computable in time poly(2d ) · s.
• Perfect Information-Theoretic Privacy. The scheme has perfect privacy against the class of all
distinguishers.
• Locality. Every output bit of fˆ(x; r) = CEnc( f, x; r) depends on at most 4 bits of (x, r).
We note that the locality and efficiency properties of the DRE scheme specified by Theorem 3.6
implies that the randomized encodings fˆ(x; r) are computable by NC0 circuits that take as input x
and the randomness r.

22

Theorem 3.7 (Computational DRE). Assume there exists a length doubling pseudorandom generator
(PRG) G that is secure against polynomial time classical (resp. quantum) adversaries. There exists an
efficient topologically-universal and label-universal DRE scheme CRE = (CEnc, CDec, CSim), which
implicitly depends on a security parameter λ, and has the following properties:
• Efficiency. For every function f computable by a size-s classical circuit and for every input x, the
encoding CEnc( f, x; r) is computable in time poly(λ) · s. Furthermore, the label functions labi,b (r)
are computable in time poly(λ). The decoding and simulation algorithms CDec and CSim are also
computable in time poly(λ) · s.
• Computational Privacy. For every polynomial t(λ), there exists a negligible function ǫ(λ) such that
the scheme is (t(λ), ǫ(λ))-private against the class of size-t(λ) classical (resp. quantum) distinguishers.
• Locality. Every output bit of fˆ(x; r) = CEnc( f, x; r) depends on at most 4 bits of (x, r, G(r)). If the
PRG G can be computed by a O(log(λ))-depth circuit, then every output bit of fˆ(x; r) can be made to
depend on at most 4 bits of (x, r), via non-black-box use of the PRG.
We note that the locality and efficiency properties of the DRE scheme specified by Theorem 3.7
implies that the randomized encodings fˆ(x; r) are computable by NC0 circuits that take as input x,
the randomness r, and the output of the PRG G.
Remark 3.8. In the case of computational security, the RE scheme (CEnc, CDec, CSim) may also
depend on a security parameter λ. Since the security parameter will always be set and fixed in
application, we do not explicitly point it out in our notation.

4 Quantum Randomized Encoding – Definition and Existence
4.1 Definition
We propose the following quantum analogue of randomized encoding.
Definition 4.1 (Quantum Randomized Encoding). Let F(x) be a quantum operation that maps n
qubits to m qubits. The quantum operation F̂(x; r) where r is classical randomness is a (t, ǫ)-private
quantum randomized encoding (QRE) of F if there exist quantum operations Dec (called the decoder)
and Sim (called the simulator) with the following properties.
• Correctness. For all quantum states (x, q) and all randomness r, it holds that (Dec(F̂(x; r)), q) =
(F(x), q).
• (t, ǫ)-Privacy. For all quantum states (x, q), we have




F̂(x; r) , q ≈(t,ǫ) Sim(F(x)) , q

where the state on the left-hand side is averaged over r. The case of ǫ = 0 is called perfect
privacy.

The encoding F̂ is a decomposable QRE (DQRE) if there exists a quantum state e (called the resource
state of the encoding), an operation F̂off (called the offline part of the encoding) and a collection of input
encoding operations F̂1 , . . . , F̂n such that for all inputs x = (x1 , . . . , xn ),


F̂(x; r) = F̂off , F̂1 , F̂2 , . . . , F̂n (x, r, e)
23

where the functions F̂off , F̂1 , . . . , F̂n act on disjoint subsets of qubits from e, x (but can depend on all
bits of r), each F̂i acts on a single qubit xi , and F̂off does not act on any of the qubits of x.
Similarly to the classical case, we refer to the second input r of F̂ as the randomness of the
encoding. We will often write F̂(x) to denote the quantum state F̂(x; r) when r is sampled from the
uniform distribution. Furthermore, we say that the quantum state F̂(x) is the randomized encoding
of the operation F and an input x.
One can see that this definition of quantum randomized encoding is syntactically similar to
Definition 3.2, with a couple differences. First, the correctness and privacy properties involves
the pair (x, q). We refer the reader to Section 3.1 for the full explanation of the quantum random
variable notation; but in short (x, q) represents a bipartite density matrix with an x part, and a q
part, and these parts may be entangled. The q part is never acted upon by the decoder or simulator,
but distinguishability is measured with respect to the encoding of x as well as q, which we think
of as quantum side information. In other words, correlations between the input and an external
system are preserved through the encoding, decoding, and simulation.
A second difference involves the definition of decomposable QRE. In addition to receiving
a random string r, the randomized encoding also receives a auxiliary quantum state e (that is
independent of the input x). The definition allows for any resource state e, but in this paper we
focus on decomposable QREs where the resource state e is a collection of EPR pairs, which is
perhaps the most natural quantum analogue of a randomness string.
Furthermore, similar to the classical setting, it is highly desirable to have efficient QRE schemes
that are universal with respect to some property of the quantum operations being encoded, say
the topology of some circuit implementation of them. This motivates the following definition of
universal QRE scheme, in analogy to Definition 3.4.
Definition 4.2 (Universal QRE Schemes for Circuits). Let C denote a class of general quantum
circuits17 and let R denote an equivalence relation over C. An (t, ǫ)-private and efficient R-universal
QRE scheme for the class C is a tuple of polynomial-time quantum algorithms (Enc, Dec, Sim) such
that given a circuit F ∈ C (here we identify the circuit with the function it computes),
• Efficient Encoding. For all quantum inputs x and randomness r, Enc(F, x; r) computes a
quantum randomized encoding F̂(x; r).
• Correctness. For all quantum states (x, q) and randomness r it holds that (F(x), q) =
(Dec(c, F̂(x); r), q) where c denotes the equivalence class of F in R.
• (t, ǫ)-Privacy. For all quantum states (x, q), we have





F̂(x; r) , q ≈(t,ǫ) Sim(c, F(x)) , q

where the state on the left-hand side is averaged over the randomness r, and c denotes the
equivalence class of F in R.
Furthermore, we say that the R-universal QRE scheme (Enc, Dec, Sim) is decomposable if the randomized encoding F̂(x) is decomposable and if the input encoding operations F̂i only depend on
the equivalence class of F in R.
17

See Section 3.2.4 for the definition of general quantum circuits.

24

For the remainder of this paper, when we speak of encoding a quantum operation F, we are
referring to encoding a specific circuit implementation of F. Furthermore, in this paper we will
be focused on topologically-universal QRE schemes – in other words, the equivalence relation R is
such that two circuits F, F′ are equivalent if they have the same topology (see Section 3.2.4 for the
definition of quantum circuit topology).

4.2 Our Main Result: Existence of Decomposable Quantum Randomized Encodings
Our main result is an efficient topologically-universal decomposable QRE scheme, which we call
Quantum Garbled Circuits. We use classical decomposable RE as a building block.
Lemma 4.3 (Quantum Garbled Circuits Scheme). Let CRE be an efficient topologically-universal and
label-universal classical DRE scheme such that for classical circuits f of size s and depth d, the time
complexity of encoding f is c(d, s) and the length of the labels is κ(d, s). Furthermore, suppose that the
encoding of CRE can be computed by NC0 circuits, and that the scheme is (t, ǫ)-private with respect to
quantum adversaries.
Recursively define κ0 = O(1), κi = κ(O(1), O(κ2i−1 )), and define ci = c(O(1), O(κ2i−1 )). (All the O(·)’s
refer to universal constants.)
Then there exists an efficient topologically-universal decomposable QRE scheme QRE = (Enc, Dec, Sim)
that satisfies the following properties:
• Efficiency. For every operation F computable by a size-s and depth-d quantum circuit and for every
quantum input x, the encoding Enc(F, x; r) is computable by a QNC0f circuit of size O(cd · s). The
QNC0f encoding circuit takes as input a string of random bits r, the quantum input x, and a collection
of EPR pairs. Furthermore, the input encoding operations F̂i can be computed by QNC0f circuits of
size O(κd ). The running time of Dec and Sim is O(cd · s).
• Classical Inputs. If an input qubit xi is classical, then the input encoding operation F̂i is computable
by a classical circuit.
• Privacy. The scheme QRE is (t′ , ǫ′ )-private where t′ = t − poly(cd ) · s and s′ = ǫ · s. Here, s and d
refer to the size and depth of the circuit being encoded.
Remark 4.4. As mentioned in Remark 3.5, we can apply our encoding scheme to a universal
circuit rather than to F itself, and consider the classical description of F as an additional input. This
would incur some overhead due to the use of the universal circuit but will have properties that
may be useful in some settings. In particular, the dependence of the encoding on the description
of F becomes very simple and since the description is classical, the encoding of the input F also
becomes classical. Furthermore, if the input x is classical as well, then the quantum part of the
encoding F̂(x) is independent of both F, x and can be generated beforehand as a “resource state”
that is given to the encoder.
The proof of Lemma 4.3 is presented in Sections 6 and 7. Specifically, Section 6 describes the
encoding, decoding, and simulation procedures of our Quantum Garbled Circuits scheme. The
correctness and privacy properties of the scheme are then analyzed in Section 7.
By instantiating CRE in Lemma 4.3 with the classical RE schemes from Theorem 3.6 and
Theorem 3.7, respectively, the following theorems immediately follow.
Theorem 4.5 (Information Theoretic DQRE). There exists an efficient topologically-universal decomposable QRE scheme QRE = (Enc, Dec, Sim) with the following properties:
25

• Efficiency. For every operation F computable by a size-s and depth-d quantum circuit and for every
d
quantum input x, the encoding Enc(F, x; r) is computable by a QNC0f circuit of size poly(22 ) · s. The
QNC0f encoding circuit takes as input a string of random bits r, the quantum input x, and a collection
of EPR pairs. Furthermore, the input encoding operations F̂i can be computed by QNC0f circuits of
d
d
size poly(22 ). The running time of Dec and Sim is poly(22 ) · s.
• Classical Inputs. If an input qubit xi is classical, then the input encoding operation F̂i is computable
by a classical circuit.
• Perfect Information-Theoretic Privacy. The scheme has perfect privacy against the class of all
distinguishers.
Proof. Plugging the properties of the DCRE scheme from Theorem 3.6 into the conditions of
i
i
Lemma 4.3, we get κi = poly(22 ), ci = poly(22 ) and (t, ǫ = 0)-privacy. The result thus follows. 
Theorem 4.6 (Computational DQRE). Assume there exists a length doubling pseudorandom generator
(PRG) G that is secure against polynomial-time quantum adversaries. There exists an efficient topologicallyuniversal decomposable QRE scheme QRE = (Enc, Dec, Sim), which implicitly depends on a security
parameter λ, and has the following properties:
• Efficiency. For every operation F computable by a size-s and depth-d quantum circuit and for every
quantum input x, the encoding Enc(F, x; r) is computable by a QNC0f circuit of size poly(λ) · s. The
QNC0f encoding circuit takes as input a string of random bits r, the output G(r) of the PRG, the
quantum input x, and a collection of EPR pairs.18 Furthermore, the input encoding operations F̂i can
be computed by QNC0f circuits of size poly(λ). The running time of Dec and Sim is poly(λ) · s.
• Classical Inputs. If an input qubit xi is classical, then the input encoding operation F̂i is computable
by a classical circuit.
• Computational Privacy. For every polynomial t(λ), there exists a negligible function ǫ(λ) such
that the scheme is (t′ (λ, s), ǫ′ (λ, s))-private with respect to quantum adversaries, where t′ (λ, s) =
t(λ) − poly(λ, s) and ǫ′ (λ, s) = ǫ(λ) · s with s being the size of the circuit being encoded.
Proof. Plugging the properties of the DCRE scheme from Theorem 3.7 into the conditions of
Lemma 4.3, we get κi = poly(λ), ci = poly(λ) · s. Since poly(cd ) · s = poly(λ, s), we get that the
scheme is (t′ , ǫ′ )-private for the functions t′ (λ, s) and ǫ′ (λ, s) specified in the Theorem statement.


5 A New Zero-Knowledge Σ-Protocol for QMA
We present a 3-message zero-knowledge Σ-protocol for any QMA problem. Our construction
generically uses QRE with certain properties, as well as quantum-secure classical commitment
schemes. Both are instantiable under (flavors of) quantum-secure one-way functions (QRE only
requires general one-way functions, and the commitment schemes we use can be achieved with
injective one-way functions or from arbitrary one-way functions in the presence of a common
random string).
18
As in the classical case, the PRG is used in a black-box manner. If we allow non-black-box use of the PRG and if it
can be computed by a O(log λ)-depth circuit, then the encoding circuit can be made fully in QNC0f that takes as input
only x, the randomness r, and EPR pairs.

26

5.1 Building Blocks
We start by going over the building blocks that are used in our protocol.
A QMA Problem with Almost-Perfect Soundness. Let L = (L yes , Lno ) be a promise problem in
QMA. Let VL = {VL,n } denote the corresponding QMA verifier, specified as a (uniform) family of
polynomial-size circuits that takes as input (x, w) where x is an instance of the language and w is a
poly(|x|)-sized quantum witness. If x ∈ L yes , then VL (x, w) accepts with probability at least 1 − µ(|x|)
and if x ∈ Lno , VL (x, w) accepts with probability at most µ(|x|) where µ(·) is a negligible function.
We let RL (x) denote the set of witnesses w on which VL accepts with probability at least 1 − µ(|x|).
A Quantum Randomized Encoding Scheme. Let QRE denote an efficient, computationallysecure quantum randomized encoding scheme satisfying the properties of Theorem 4.6. Since
the QRE is decomposable and has classical encoding for classical inputs, we can assume that
the scheme has the following structure: given a circuit F and input (q, c) where q is an n1 -qubit
quantum state and c is an n2 -bit classical string, the encoding F̂(q, c) can be written as


F̂off , F̂1 , . . . , F̂n1 +n2 (q, c, r, e)
where r is a uniformly random string, e is a collection of EPR pairs, F̂off acts on (r, e) only, and
F̂n1 +1 (c1 ; r), . . . , F̂n1 +n2 (cn2 ; r) are classical circuits that encode each bit of c separately. Thus for each
i ∈ [n2 ] and r, we can define classical labels for each ci :
labi,b (r) = F̂n1 +i (b; r) .
Furthermore, we assume that for a fixed value of r, the operations F̂off and F̂i can be implemented
via polynomial-size unitary circuits, possibly using some additional zero ancillas.19
We now consider the quantum functionality that, for a fixed value of r, takes as input the
quantum input q and a sequence of zero ancilla bits, and outputs the quantum state


F̂ 0 , {labi,b }i∈[n2 ],b∈{0,1} , 0 ,
where F̂ 0 denotes the part output by (F̂off , F̂1 , . . . , F̂n1 ), and where 0 represents a sequence of zero
qubits.
Since the encoding is unitary as we explained above, this functionality can be implemented by
a unitary circuit Ur that first creates a number of EPR pairs e from the zero qubits, and then applies
the encoding functions to compute F̂ 0 and {labi,b }i,b . In other words, Ur (q, 0) is almost the same
as the QRE encoding of F(q, c), except for the classical input it outputs all labels, and uses zero
ancillas for scratch space. We note that for a fixed c ∈ {0, 1}n2 , the state (F̂ 0 , {labi,ci }i∈[n2 ] ) constitutes
the encoding of F(q, c).
A Quantum-Secure Classical Commitment Scheme. We require a perfectly-binding non-interactive
commitment scheme secure against quantum adversaries. Such a commitment scheme is defined
as a polynomial-time function Com that takes as input a security parameter λ, an input message
m and randomness s and outputs a string c = Com(1λ , x; s) with the following properties:
19
This is true for our QGC scheme and can be assumed without loss of generality. The reason, briefly, is that we can
always consider purified versions of the F̂ functions, and then instead of tracing out a part of the output, just encrypt it
with a quantum one-time pad, using classical bits from a (possibly extended) r.

27

• (Perfect Binding). For all λ there does not exist x1 , x2 and s1 , s2 such that Com(1λ , x1 ; s1 ) =
Com(1λ , x2 ; s2 ).
• (Computational Hiding Against Quantum Adversaries). For any sequence of {x1,λ , x2,λ }λ , where
|x1,λ | = |x2,λ | = poly(λ), it holds that the distributions Com(1λ , x1,λ ; s1 ) and Com(1λ , x2,λ ; s2 )
where s1 , s2 are sampled uniformly cannot be distinguished by any polynomial-time quantum
circuit with non-negligible advantage.
Such a commitment scheme follows from the existence of quantum-secure injective one-way
functions, or in the common-random-string model from any one-way function. There are also
explicit constructions from post-quantum assumptions (see, e.g., [JKPT12]).
Commitment schemes like this can be used in the following manner: to commit to a message
x, the sender samples a randomness s and computes c = Com(1λ , x; s), and sends c to the receiver.
To reveal the message x, the sender sends (x, s) to the receiver. The receiver can verify that this is a
valid commitment by checking that c = Com(1λ , x; s).
For more background on commitment schemes see, e.g., [Gol06].
Quantum Teleportation. We recall the functionality of quantum teleportation. Let e = (e1 , e2 )
denote m EPR pairs, where e1 denotes all “first-halves” of the EPR pairs, and e2 denotes all
the “second halves”. Suppose that Alice has e1 along with an m-qubit quantum state w, and
Bob has e2 . Alice can teleport w to Bob by performing a measurement on (w, e1 ) to obtain
measurement outcomes (u, v) ∈ ({0, 1}m )2 . The post-measurement outcome on Bob’s side is Xu1 Zv1 ⊗
· · · ⊗ Xum Zvm (w). Alice can then send (u, v) to Bob so he can undo the Pauli corrections.

5.2 Delayed-Input Zero-Knowledge Σ-Protocols
We now recall the definition of zero-knowledge Σ-protocols with the delayed-input property. We
will use the following notation. Let P, V be a pair of interactive machines (interpreted as prover and
verifier respectively). We let hP(yp ), V(yv )i(x) denote the output of the verifier V after completing
an interaction with P, in which P has private input yp , V has private input yv and they also have a
common input x (the inputs yp , yv can be classical or quantum).
A pair (P, V) of a quantum polynomial-time “honest” prover P and an “honest” verifier V is a
quantum interactive proof system for L if there exist numbers α (called the completeness) and β (called
the soundness) such that α > β such that
• (Completeness.) If x ∈ L yes and w ∈ RL (x), then P[hP(w), Vi(x) accepts] ≥ α.
• ((Statistical) Soundness.) If x ∈ Lno , then for any prover P∗ (possibly computationallyunbounded) it holds that P[hP∗ , Vi(x) accepts] ≤ β.
Adaptive Soundness. For public-coin protocols (and in particular in our protocol) we can consider a stronger notion of adaptive soundness, in which the instance x is not specified ahead of time,
but rather is produced by P∗ in the end of the interaction. In this case it will be convenient for us to
specify that the output of the verifier includes the accept/reject bit also the instance x produced by
P∗ . Under this convention, adaptive soundness is the requirement that for any adaptive adversary
P∗ it holds that
P[hP∗ , Vi = (accept, x) ∧ x ∈ Lno ] ≤ β .
Note that the winning event in this case is not necessarily efficiently recognizable.
28

Zero-Knowledge The proof system is furthermore (computational) zero-knowledge if there exists
a a quantum polynomial-time simulator ZKSim such that for any malicious verifier V ∗ and for
any asymptotic sequence of instances x ∈ L yes , w ∈ RL (x) and quantum poly(|x|)-qubit auxiliary
input y it holds that the output state of ZKSim(V ∗ , x, y) and hP(w), V ∗ (y)i(x) are computationally
indistinguishable. We recall that the latter expression refers to the quantum output produced by
V ∗ at the end of the interaction.
An interactive protocol is a Σ-protocol if it consists of a prover sending the first message m1 ,
the verifier sending a uniformly random (classical) challenge m2 , the prover sending a response
m3 , and the verifier decides whether to accept or reject based on the transcript. We note that for
an honest verifier the transcript is well defined even if the messages are quantum, since m2 is a
classical random string independent of m1 .
Finally, we say that a zero-knowledge Σ-protocol has the delayed-input property if the prover
only receives the instance x and a quantum witness w after it has sent the first message. In other
words, the prover’s first message m1 is computed independently of the instance x and witness w.

5.3 Our Proof System
We present a zero-knowledge Σ-protocol hP, Vi for L in Protocol 1. Note that the prover only gets
the instance x and witness w right before generating the third message.
Parameters and Definitions. We assume that at the beginning all parties know the instance
length n. To avoid clutter we set the security parameter λ to be equal to n. We let m = m(n) denote
the length of the witness required for instances of length n of L. We let F denote the following
quantum circuit, that takes n + 2m classical bits (partitioned into strings x, u, v of length n, m, m
respectively) and m quantum bits as inputs. On input (x, u, v, w̃) the circuit does the following. It
first computes w = (Xu1 Zv1 ⊗ · · · ⊗ Xum Zvm )(w̃), i.e. applies a quantum one-time pad, indicated by
the vectors u, v to the quantum input. It then executes VL (x, w) and outputs the single-bit outcome
of this computation.

Lemma 5.1 (Completeness). There exists a negligible function µ such that for all x ∈ L yes and w ∈ RL (x),
the honest prover described in Protocol 1 runs in polynomial time given the input (x, w), and is accepted by
the verifier with probability at least 1 − µ(|x|).
Proof. If the prover behaves honestly, then with challenge b = 0, the verifier will be able to verify
that the state (F̂ 0 , {labi,b }i∈[n+2m],b∈{0,1} ) is indeed equal to U(e2 , 0); and with challenge b = 1, the
verifier obtains the output qubit of the circuit VL (x, w) by applying the QRE decoding procedure
(which we assume has perfect correctness). Thus if the maximum acceptance probability of VL (x, w)
over all choices of w is 1 − µ(|x|), then the acceptance probability of the verifier is 1 − µ(|x|). This
establishes the completeness property.

We now prove statistical adaptive soundness for our protocol as stated in the next Lemma.
Lemma 5.2 (Statistical Adaptive Soundness). There exists a negligible function µ′ such that for any
adaptive prover P∗ , it holds that
P[W] ≤ 1/2 + µ′ (|x|) ,
where W is the event where hP∗ , Vi = (accept, x) ∧ x ∈ Lno .
29

1 Global Parameters: Instance length n, witness length m = m(n).
2 Prover:
3
4

5

6

Generate m EPR pairs e = (e1 , e2 ) for the purpose of quantum teleportation.
Sample a random string r and execute the circuit Ur on input (e2 , 0), where the 0


represents a sufficient number of ancilla zeroes. Let F̂0 , {labi,b }i∈[n+2m],b∈{0,1} denote
the outcome of this computation.
Sample random strings si,b for all i ∈ [n + 2m], b ∈ {0, 1} and compute the
commitment ci,b = Com(1λ , labi,b ; si,b ). Then, sample a random string s0 and
compute the commitment c0 = Com(1λ , r; s0 ).


Send F̂ 0 , c0 , (ci,b )i∈[n+2m],b∈{0,1} to the verifier.

7 Verifier:
8

Send random bit b.

9 Prover (given x, w):
10
11
12
13

14

If b = 0:
Open all commitments, i.e. send (r, s0 ) and (labi,b , si,b )i∈[n+2m],b∈{0,1} to the verifier.
If b = 1:
Teleport the witness w into the “first halves” e1 of the EPR pairs e to obtain
classical strings (u, v) ∈ {0, 1}m .
Consider the concatenated string z = (x, u, v). Open the commitments
corresponding to z, i.e. send (zi , labi,zi , si,zi )i∈[n+2m] to the verifier.

15 Verifier (given x):
16
17
18

19
20
21

22

If b = 0:
Check that all commitments are valid. If any of them are invalid, then reject.
Apply the inverse circuit Ur−1 to (F̂ 0 , {labi,b }i∈[n+2m],b∈{0,1} ), and let (e′2 , q) denote the
output. Check that q is the all zeroes state. If so, then accept. Otherwise, reject.
If b = 1:
Check that z = (x, u, v) for the instance x and some u, v. If not then reject.
Check that all commitment openings are valid. If any of them are invalid, then
reject.
Decode the QRE (F̂ 0 , {labi,zi }i∈[n+2m] ) to obtain a single-qubit output; return the
output of this evaluation.
Protocol 1: A zero-knowledge Σ-protocol for QMA problem L

30

In order to prove the lemma, we require the following two claims.
Claim 5.3. Let |φi, |φ0 i, |φ1 i be unit vectors over some Hilbert space representing states of a quantum
system. Assume there exist non-negative real values α1 , α2 so that |φi = α1 |φ0 i + α2 |φ1 i (note that
|φ0 i, |φ1 i are not necessarily orthogonal, so α21 + α22 is not necessarily 1).
Let M be some measurement operator defined over this Hilbert space. Let p, p1 , p2 be the probability
that the measurement M succeeds when the system is in state |φi, |φ0 i, |φ1 i respectively. Then p ≤
√
√
(α1 p1 + α2 p2 )2 .
Proof. The proof follows by triangle inequality. We define |φ̃i i = M|φi i for i ∈ {0, 1} and note that
by definition pi = hφ̃i |φ̃i i.
p = hφ|M† M|φi

= α21 hφ̃0 |φ̃0 i + α22 hφ̃1 |φ̃1 i + α1 α2 (hφ̃0 |φ̃1 i + hφ̃1 |φ̃0 i)
√
≤ α21 p1 + α22 p2 + 2α1 α2 p1 p2
√
√
= (α1 p1 + α2 p2 )2 .

The claim thus follows.



The following claim establishes a very weak form of soundness, namely it asserts that soundness 1/2 + negl(n) holds when the b = 0 test is guaranteed to pass.
Claim 5.4. For any adversarial strategy P∗ for which P[W|b = 0] = 1 it holds that P[W|b = 1] = negl(n).
Proof. Assume that P∗ is such that P[W|b = 0] = 1. Then the message m1 is guaranteed to be a
properly generated QRE of the correct functionality F. It follows by the correctness of the QRE
that such a circuit cannot accept an instance x ∈ Lno except with negligible probability. The claim
thus follows.

We can now prove the soundness lemma.
Proof of Lemma 5.2. Let P∗ be an adaptive possibly-cheating prover. Consider the point in time
after P∗ sent its first message m1 and let us consider the joint quantum state of P∗ and m1 , denote
this state by |φi. Assume without loss of generality that this state is pure (we can always add
the purification of the state into the internal state of P∗ . Assume without loss of generality that if
P∗ sends valid commitments (i.e. ones that can be opened), then it indeed opens them correctly
upon challenge b = 0 (this can only increase the advantage of P∗ and since it is computationally
unbounded it can always find the openings).
We consider the (inefficient) measurement operator defined on this joint state in the following
way.
1. Check (via brute force search) that all commitments in m1 are valid. If they are valid, let
r, labi,b be their openings. If not then reject. Note that this is a projection since it simply
accepts a subset of the possible commitments (in the computational basis).


2. Apply Ur−1 on F̂ 0 , {labi,b }i,b , where F̂ 0 comes from m1 and r, labi,b are the openings of the
commitments (which at this point are well defined). The outcome is a pair (q, e2 ). Accept if
q = 0 and reject otherwise. Note that this part is a projection as well since it only involves
applying a unitary followed by accepting a value in the computational basis.
31

We conclude that this measurement operator is a projection Π, and notice that this measurement
corresponds to the event W|b = 0. Therefore
P[W|b = 0] = hφ|Π|φi ,
and denote this value by ǫ. If ǫ = 0 then the proof is complete because the overall acceptance
probability is at most 1/2. From now on assume ǫ > 0. Note that since Π is a projection it holds
that
hφ|(I − Π)|φi = 1 − ǫ .
Let M denote the (not necessarily projective and inefficient) measurement that acts on the joint
state of P∗ and m1 as follows. It acts on the state of P∗ to generate the third message m3 and instance
x, and then checks whether x ∈ Lno and if so whether the verifier V accepts. Again by definition it
holds that
P[W|b = 1] = hφ|M† M|φi .
√
√
Let us√now define |φ0 i = Π|φi/ ǫ and |φ1 i = (I − Π)|φi/ 1 − ǫ, so we can write |φi =
√
ǫ|φ0 i + 1 − ǫ|φ1 i. By Claim 5.3 (triangle inequality) we have
q
2
q
ǫhφ0 |M† M|φ0 i + (1 − ǫ)hφ1 |M† M|φ1 i
q
2
√
†
≤
ǫhφ0 |M M|φ0 i + 1 − ǫ .

P[W|b = 1] ≤

(5.1)
(5.2)

However, suppose that instead of starting with the joint prover-message state |φi, we consider
a different prover P̃∗ which starts with the state |φ0 i instead. By construction this prover will pass
the challenge b = 0 with probability 1, because Π|φ0 i = |φ0 i. Therefore, by Claim 5.4 it follows that
P[WP̃∗ |b = 1] = hφ0 |M† M|φ0 i ≤ µ(n) ,
for some negligible function µ, because M corresponds to the test performed on challenge b = 1.
Finally we can plug hφ0 |M† M|φ0 i ≤ µ(n) into Eq. (5.2) to obtain
P[W|b = 1] ≤
≤

p
for some µ′ (n) = O( µ(n)).
Finally we can conclude that

q

ǫhφ0 |M† M|φ0 i +

2
√
1−ǫ

p
2
√
ǫ · µ(n) + 1 − ǫ

= 1 − ǫ + 2µ′ (n) ,

 1
1
1
P[W] ≤ ǫ + 1 − ǫ + 2µ′ (n) ≤ + µ′ (n)
2
2
2

which completes the proof of the Lemma.



Lemma 5.5 (Computational zero-knowledge). There exists a quantum polynomial-time simulator
ZKSim satisfying the following: for all cheating verifiers V ∗ , for all asymptotic sequences of (x, y, w)
where x ∈ L yes , the state y is an arbitrary quantum state, and w ∈ RL (x) is a witness for x, we have that the
output of ZKSim(V ∗ , x, y) is computationally indistinguishable from hP(w), V ∗ (y)i(x).
32

Let V ∗ denote the malicious verifier. In order to prove Lemma 5.5 we first analyze a “conditional” simulator ZKSim0 that takes as input (V ∗ , x, y), and outputs a quantum state as well as a flag
indicating whether the simulator aborted. We show that the output of ZKSim0 is, conditioned on
not aborting, computationally indistinguishable from the view of the interaction hP(w), V ∗ (y)i(x).
The probability of aborting in the conditional simulator ZKSim0 is (negligibly close to) 1/2, but we
can use Watrous’s Rewinding Lemma [Wat09] to argue the existence of a quantum polynomial-time
algorithm ZKSim that satisfies the conclusions of Lemma 5.5. In particular, we use the formulation of the Rewinding Lemma as presented in [BS20, Lemma 2.1]; the resulting algorithm ZKSim
queries ZKSim0 as a blackbox polynomially many times to amplify the success probability. The
reason we need to use the Rewinding Lemma instead of simply just repeating ZKSim0 until it
doesn’t abort is because of the quantum auxiliary input y; running ZKSim0 once and aborting may
alter the state y significantly. Watrous’s Rewinding Lemma gets around this issue.

1 Input: cheating verifier V ∗ , instance x ∈ {0, 1}n , auxiliary quantum state y
2 Sample t ∈ {0, 1} uniformly at random.

3 if t = 0 then

Execute the honest prover P to generate the first message m1 (note P needs no input
for this).
5
Run the cheating verifier V ∗ (x, y) on the first message m1 to generate the challenge
bit b. If b , 0, abort (i.e., output (a, 0) where a = 1).
6
Otherwise, continue simulating the honest prover P on challenge b = 0 to generate
the third message m3 .
7 end
8 else
9
Generate m EPR pairs e = (e1 , e2 ).
10
Sample uniformly random u, v ∈ {0, 1}m .
11
Run the simulator Sim of the QRE on input |1ih1|, with respect to the same circuit


topology as F, to obtain an output F̂0 , {labi }i∈[n+2m] .
4

For all i ∈ [n + 2m],b ∈ {0, 1}, define labi,b = labi . Set r = 0.
13
Execute the honest prover P, starting at Step 5 of Protocol 1, where the prover
computes the commitments to r and (labi,b )i,b . Let m1 denote the prover’s first
message.
14
Run the cheating verifier V ∗ (x, y) on the first message m1 to generate the challenge
bit b. If b , 1, abort (i.e., output (a, 0) where a = 1).
15
Otherwise, execute Step 14 of the honest prover P in Protocol 1 to open the relevant
commitments, which forms message m3 . Note that w is note used by P in this step,
therefore the simulator can perform it.
16 end
17 Continue simulating the cheating verifier V ∗ on the third message m3 to obtain a state o,
and output (a, o) where a = 0.
12

Algorithm 2: The simulator ZKSim0 for the zero-knowledge protocol

33

Lemma 5.6. There exists a quantum polynomial-time conditional simulator ZKSim0 satisfying the following: for all cheating verifiers V ∗ , for all asymptotic sequences of (x, y, w) where x ∈ L yes , the state y is an
arbitrary quantum state, and w ∈ RL (x) is a witness for x, we have that the output of ZKSim0 (V ∗ , x, y),
conditioned on not aborting, is computationally indistinguishable from hP(w), V ∗ (y)i(x).
Proof. The proof proceeds by a sequence of experiments (or hybrids). We keep track of the output
distribution of the simulator and the rejection probability across experiments. Fix V ∗ , y, x, w as in
the Lemma statement.
• Experiment 0. This is the experiment of running the conditional simulator ZKSim0 on input
(V ∗ , x, y) as presented in Protocol 2.
• Experiment 1. Modify the previous experiment by replacing Step 10 with the following:
teleport w into e1 and let u, v be the (classical) outcome of the teleportation. By the properties
of the teleportation the strings u, v are uniformly random and therefore this experiment
produces an identical distribution to the previous one.
• Experiment 2. Now, consider Experiment 1 except we modify Step 11 of ZKSim0 . Instead
of using the QRE simulator Sim, do the following: sample randomness r∗ and evaluate the


unitary Ur∗ on input (e2 , 0) to generate the state F̂ 0 , (lab∗i,b )i∈[n+2m],b∈{0,1} . Set labi to be lab∗i,zi
for z = (x, u, v). By definition F(x, u, v, e2 ) computes VL (x, w), which by the completeness of
the QMA verifier outputs |1ih1| with probability 1 − negl(n).
By the privacy of QRE, the QRE encoding of circuit F(x, u, v, e2 ) is computationally indistinguishable from Sim(|1ih1|) when we marginalize over the randomness r∗ and the labels
(labi,b : b , zi ). Since the randomness r∗ and the unused labels are not used anywhere else in
the experiment, the output distribution of this experiment is computationally indistinguishable from that of the previous one.
• Experiment 3. Change Step 12 of ZKSim0 so that r = r∗ and labi,b = lab∗i,b . Since this only
changes locations of the commitment that are never opened by the prover P, the hiding
property of the commitment scheme guarantees that the views of V ∗ between Experiment 2
and Experiment 3 remain computationally indistinguishable.
• Experiment 4. Move the modified Step 10 (i.e. the teleportation of w into the EPR pairs) to
be right before Step 15. This does not change anything in the simulation because none of the
steps until Step 15 in Experiment 3 depend on teleportation outcomes (u, v).
• Experiment 5. Note that in Experiment 4, the steps up to and including receiving the bit b
from V ∗ are identical between t = 0 and t = 1. Thus we can move these steps outside of the
“if” statement, and before the sampling of t. The output of the Experiment is unchanged
from Experiment 4.
We see that the output in Experiment 5 is computationally indistinguishable from that of
ZKSim0 (x). Furthermore, in Experiment 5 the bit t is sampled after receiving the bit b and abort
occurs if and only if t , b. It follows that the abort probability is 1/2 in Experiment 5. Furthermore,
conditioned on not aborting, the experiment is identical to that of the execution of V ∗ with P(x, w).
It follows that Experiment 0 (which is to run ZKSim0 on input (V ∗ , x, y)), the probability of
abort is negligibly close to 1/2 and the output conditioned on not aborting is indistinguishable
from hP(w), V ∗ (y)i(x).

34

6 Quantum Garbled Circuits – Construction
In this section we present topologically-universal QRE scheme of Lemma 4.3, called the Quantum
Garbled Circuits scheme and denoted by QGC. In particular, given a circuit that computes a
quantum operation F, we show how to compute the encoding F̂ in Section 6.3, how to decode the
encoded value in Section 6.4, and how to simulate the randomized encoding in Section 6.5. We
then prove the correctness and security of the scheme in Section 7.
In this paper we assume that quantum circuits F being encoded use the universal gate set
C2 ∪ {T}. The only property of this gate set we use (other that the arity of the gates being bounded
by a global constant) is the following: each p-qubit gate U1 of circuit F has the property that for any
single-qubit Pauli unitaries P1 , . . . , Pp , there exist single-qubit gates R1 , . . . , Rp from the PX group
such that
U1 (P1 ⊗ P2 ⊗ · · · ⊗ Pp ) = (R1 ⊗ R2 ⊗ · · · ⊗ Rp )U1 .
(6.1)
This property indeed holds for the C2 ∪ {T} universal set as described in Sections 3.2.1 and 3.2.2.
A Building Block: Topologically-Universal Decomposable RE for Classical Circuits. As stated
in Lemma 4.3, we assume the existence of an efficient topologically-universal and label-universal
DCRE for classical circuits. We refer to this DCRE scheme as CRE = (CEnc, CDec, CSim). In
our construction we use CRE as a generic building block, and different instantiations of CRE will
result in quantum encoding scheme with different properties. As in the Lemma statement, we let
κ(·, ·) and c(·, ·) be such that for functions f computable by size-s and depth-d classical circuits, the
complexity of encoding f is c(d, s) and the length of the labels is κ(d, s). We let CSimT and CDecT
denote the polynomial-time simulator and decoding procedures of CRE, respectively, for classical
circuits with topology T.

6.1 Gadgets
In this section we introduce various gadgets that are used in our QGC scheme.
6.1.1

Teleportation Gadget

Let ℓ = (ℓb,a )a∈{0,1},b∈{x,z} be a vector of strings of length κ, and let s = (sz , sx ), t = (tz , tx ) ∈ {0, 1}2 .
Define TPℓ,s,t to be the unitary computed by the following circuit:
u

•

•

H

z /

X(ℓz,0 )

X(ℓz,0 ⊕ ℓz,1 )

x /

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )
•

v

X sx

Z sz

Xtx

Ztz

Figure 3: Teleportation gadget

Here, for a string r ∈ {0, 1}κ the notation X(r) denotes applying the tensor product of X gates
acting on the i-th qubit whenever ri = 1, and identity otherwise. The controlled X(ℓz,0 ⊕ ℓz,1 ) and
X(ℓx,0 ⊕ ℓx,1 ) gates can also be seen as fan-out gates that are applied to the qubits indexed by ℓz,0 ⊕ ℓz,1
and ℓx,0 ⊕ ℓx,1 , respectively, because it copies the control qubit into the target qubits simultaneously.
35

Thus the teleportation gadget is a QNC0f circuit. We refer to ℓ as the teleportation labels and s, t as
the randomization bits of the teleportation gadget TPℓ,s,t .
Lemma 6.1. Let u, v, u′ denote qubit registers, and let z, x denote ancilla registers. For all ℓ, s, t and for all
qubit states |ψi we have
TPℓ,s,t |ψi ⊗ |0, 0i ⊗ |EPRi =
u

vu′

zx

1 X sz sx
Z X |di ⊗ Ztz Xtx |ei ⊗ |ℓz,d , ℓx,e i ⊗ Xe Zd |ψi
2
d,e∈{0,1}

u

v

zx

u′

Proof. Since TPℓ,s,t is unitary, it suffices to prove the Lemma when |ψi = |ci is a standard basis state.
After the first CNOT, Hadamard, and X(ℓz,0 ) and X(ℓx,0 ) we have
1 X
(−1)dc |di ⊗ |ℓz,0 i ⊗ |ℓx,0 i ⊗ |a ⊕ c, ai .
2
′
d,a∈{0,1}

After the controlled X’s we have
1 X
2

d,a∈{0,1}

u

z

vu

x

(−1)dc |di ⊗ |ℓz,d i ⊗ |ℓx,a⊕c i ⊗ |a ⊕ c, ai .
u

vu′

x

z

Relabeling e = a ⊕ c and re-arranging, we get

1 X
|di ⊗ |ei ⊗ |ℓz,d , ℓx,e i ⊗ Xe Zd |ci .
2
′
d,e∈{0,1} u

v

zx

u

Applying the Xsx , Xtx , Zsz , Ztz gates, we obtain the desired Lemma statement.

6.1.2

Correction Gadget

In our QGC scheme, the encoding consists of a collection of EPR pairs that are connected via gates
of the circuit F and teleportation gadgets as described above. However, the teleportation gadget
induces a correction on the output (as demonstrated by Lemma 6.1) that, ostensibly, needs to be fixed
before applying the next gate and teleportation operation – but since the encoding is performed
in parallel, it is up to the evaluator to perform the corrections after the gates and teleportation
gadgets are appled. The next Lemma demonstrates that the desired operation (correction, then
teleportation) is equivalent a sequence of circuits Λ1 , Λ2 , Λ3 where the encoder can apply Λ1 ,
and the decoder can apply Λ2 and Λ3 . Before stating the Lemma, we first have to describe the
randomization group.
Randomization Group. In the following Lemma, the circuits Λ1 , Λ2 , Λ3 will act on the same
registers that the teleportation gadget acts on (single-qubit registers u, v and κ-qubit registers z, x),
as well as ancilla registers b that is (κ + 1)2 qubits wide. The individual qubits of registers b
are indexed by (i, j) ∈ {0, 1, . . . , κ}2 . An important conclusion of the Lemma is that the circuit Λ2
computes a unitary belonging to the randomization group Rκ , which consists of depth-one circuits
that are tensor products of
• Two-qubit Clifford gates acting on the pair of qubits (bij , b ji ) for all i < j, and
• Single-qubit Clifford gates acting on all other qubits.
36

The set Rκ indeed forms a group under the natural gate multiplication operation. It has finite
order with exp(O(κ2 )) elements, and a uniformly random element of Rκ can be sampled via an NC0
circuit that is given a uniformly random bitstring as input (essentially, the single- and two-qubit
Clifford gates are chosen independently in parallel).
Lemma 6.2. Let ℓ be κ-bit teleportation labels, and let s, t ∈ {0, 1}2 be randomization bits. Let R be an
element from the single-qubit PX group. Then there exist
• QNC0f circuits Λ1 (ℓ), Λ3 and
• A depth-one Clifford circuit Λ2 (R, ℓ, s, t) that computes a unitary in Rκ
all acting on registers u, z, x, v, b such that the following circuit identity holds:
u

R

z

/

x

/

u
TPℓ,s,t

=

v

(6.2)

z

/

x

/ Λ1 (ℓ)

Λ2 (R, ℓ, s, t)

Λ3

v
/

b |0i

b |0i /

Furthermore, the description of Λ2 (R, ℓ, s, t) can be computed by a NC0 circuit of size O(κ2 ).
Proof. We can write the left-hand side of (6.2) (omitting the ancilla registers b) as
H

•

/

X(ℓz,0 )

X(ℓz,0 ⊕ ℓz,1 )

/

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

u

R

z
x

•

X sx

Z sz

Xtx

Ztz

•

v

Since R is a PX group element, we can propagate it past the first CNOT gate to get the equivalent
circuit
•
•
R1 H
u
X sz Z sz
z /

X(ℓz,0 )

X(ℓz,0 ⊕ ℓz,1 )

x /

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

v

R2

•

Xtx

Ztz

for some single-qubit gates R1 and R2 that are PX group elements. Propagating R2 past the bottom
fan-out operation yields another equivalent circuit
u

•

R1

•

H

z /

X(ℓz,0 )

X(ℓz,0 ⊕ ℓz,1 )

x /

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

R3

•

R4

v
37

X sx

Z sz

Xtx

Ztz

(6.3)

where R3 is a single-qubit PX group element, and R4 is a tensor product of single-qubit PX group
elements.
Next, we use the following Proposition in order to “push” the R1 gate through the circuit as far
to the right as possible:
Proposition 6.3. For all single-qubit PX gates R, s = (sz , sx ) ∈ {0, 1}2 , and strings r ∈ {0, 1}κ there exist
QNC0f circuits C1 (r) and C3 and a depth-one Clifford circuit C2 (R, r, s) in the randomization group Rκ such
that the following circuit identity holds:
u

R

z

/

b |0i

/

H

X sx

•

Z sz
C1 (r)

=

X(r)

C2 (R, r, s)

C3

|0i

Here, the register b consists of (κ + 1)2 qubits. Furthermore, descriptions of the circuits C1 (r) and C2 (R, r, s)
can be computed by NC0 circuits of size O(κ2 ).
The proof of this Proposition is deferred to Appendix C. Letting r = ℓz,0 ⊕ ℓz,1 , we thus get that
Circuit (6.3) is equivalent to
•

u
z

/

(6.4)
X(ℓz,0 )

C1 (r)

C2 (R1 , r, s)

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

R3

•

R4

X(ℓz,0 )

C1 (r)

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )

C3

b |0i /
x

/

v

Xtx

Ztz

Define Λ1 (ℓ) to be the circuit
u

•

z /
b /
x /

•

v
Since C1 (r) is a QNC0f circuit, so is Λ1 (ℓ).
Define Λ2 (R, ℓ, s, t) to be the circuit
u
z / C2 (R1 , r, s)
b /
x /

R3

v

R4

Xtx

Ztz

Since C2 (R1 , r, s) is a depth-one Clifford circuit in the randomization group Rκ , R3 is a tensor product
of single-qubit Clifford gates, and R4 is a single-qubit Clifford gate, it follows that Λ2 (R, ℓ, s, t) is
38

also a member of Rκ . The fact that a description of Λ2 (R, ℓ, s, t) can be computed by an NC0 circuit
follows from the fact that C2 (R1 , r, s) and R1 , R2 , R3 , R4 can all be computed via NC0 circuits (given
R, ℓ, s, t as input).
Finally, define Λ3 to be the circuit C3 , which is a QNC0f circuit. This establishes the Lemma. 
Remark 6.4. Henceforth we will abbreviate the tuple of registers (z, x, b) as register a. We call the
qubits in this register “ancilla qubits”.
The Correction Gadget. Let κ be a positive integer and let A be a unitary from the randomization
group Rκ , let R be a single-qubit PX unitary, let ℓ be κ-bit teleportation labels, and let s = (sx , sz ), t =
(tx , tz ) ∈ {0, 1}2 be randomization bits. Define the κ-correction gadget unitary CorrA,R,ℓ,s,t to be the
unitary computed by the following circuit:
u
a / A†

Λ2 (R, ℓ, s, t)

v
Note that since A ∈ Rκ , it follows that the unitary CorrA,R,ℓ,s,t ∈ Rκ . Thus a canonical representation
d A,R,ℓ,s,t , is an ordered list of single- and two-qubit
of a correction gadget CorrA,R,ℓ,s,t , denoted by Corr
Clifford gates on the respective qubits.
Furthermore, then for every κ-bit teleportation labels ℓ, randomization bits s, t ∈ {0, 1}2 , and
single-qubit R from the PX group, for a uniformly random A drawn from Rκ , the correction gadget
d A,R,ℓ,s,t is uniformly distributed over the set of all κ-correction gadgets.
is Corr

6.2 Encoding a Single Gate

We now present the gate encoding unitary GateEnc1,r,A,ℓ,s,t in Algorithm 3. This is used by QGC to
encode each gate of the circuit. In what follows, we let 1 ∈ B denote a “placeholder gate” in the
circuit topology T , and let U1 denote a specific unitary for the gate.
The unitary GateEnc1,r,A,ℓ,s,t is a function of a p-qubit gate U1 , a string r (which represents the
randomness used by CRE), randomization unitaries A = (A j ) j∈[p] with A j ∈ Rκ j for some integer
κ j , strings ℓ = (ℓ j,b,a ) j∈[p],b∈{x,z},a∈{0,1} with ℓ j,b,a ∈ {0, 1}κ j (which represents the teleportation labels),
and randomization bits s = (s j,b ) j∈[p],b∈{0,1} , t = (t j,b ) j∈[p],b∈{0,1} . As described at the beginning of this
section, we assume that the gate U1 satisfes the property described in Equation (6.1).
At a high level, the gate encoding produces a quantum and a classical part. The quantum part
is comprised of input qubits in registers u1 , . . . , up , ancillas in registers a1 , . . . , ap , and target qubits
in registers v1 , . . . , vp . These target qubits are each initialized as part of an EPR pair. The gate U1
is first applied to the input registers u. Then the the circuit Λ1 (ℓ j ) from Lemma 6.2 are applied
to registers (u j , a j , v j ) for j ∈ [p], and then the randomization unitaries A j are applied to registers
(u j , a j , v j ) for j ∈ [p].
Since we think of the input qubits as having been previously teleported, the input qubits will
have X and Z corrections on them, and applying the gate U1 will incur further corrections. The
evaluator will have to fix these corrections; they will use the classical part of the gate encoding to
do this, which is a classical randomized encoding of a correction function, which we describe next.

39

6.2.1

Correction Functions and Their Randomized Encoding

Consider a vector κ = (κ j ) j∈[p] of label lengths. Define the classical correction function fκ , which on
input
d 1 , Corr
d 2 , . . . , Corr
d p ) where
(z1 , x1 , . . . , zp , xp , U1 , A, ℓ, s, t) outputs a tuple of quantum circuits (Corr
d j = Corr
d A ,R ,ℓ ,s ,t for j ∈ [p] are the correction gadgets defined in Section 6.1.2. The unitaries
Corr
j

j

j

j j

R1 , R2 , . . . , Rp are the single-qubit PX unitaries satisfying

U1 (Zz1 Xx1 ⊗ · · · ⊗ Zzp Xxp ) = (R†1 ⊗ · · · ⊗ R†p )U1 .
The unitaries R1 , . . . , Rp are well-defined because U1 comes from our universal set of gates (twod j are specified using their canonical
qubit Clifford and T gates). The correction gadgets Corr

representation (i.e., a tensor product of single- and two-qubit Clifford gates).
We now describe a classical circuit to compute fκ , by first describing the circuit to compute
d
Corr j for a single j. As discused in Section 6.1.2, there is a constant-depth circuit of size O(κ2j ) to
d j , and this circuit is a function of R j , A j , ℓ j , s j , t j . The unitary R j is itself a function of
compute Corr

U1 and the tuple (z1 , x1 , . . . , zp , xp ). Since the universal gate set used in this paper has arity bounded
by 2 and has a constant number of elements, there is a constant-sized circuit that computes R j .
d j , we get a constant-depth circuit of size O(κ2 ) that
Composing this circuit with the circuit for Corr
j

takes input 1, z1 , x1 , . . . , zp , xp , A j , ℓ j , s j , t j .
Putting everything together, we have a classical NC0 circuit, whose depth will be denoted a
P
universal constant dcorr and whose size is cκ = O( j κ2j ) that computes fκ . Note that the topology
of this circuit only depends on the vector κ; call this topology Tκ .
Now, consider the encoding fˆκ of fκ with respect to CRE, the DCRE scheme for classical circuits
that we use as a blackbox. Since the scheme is decomposable, we have that fˆκ(z1 , x1 , . . . , zp , xp , U1 , A, ℓ, s, t; r)
consists of an offline part fˆκ,off (r) that only depends on fκ , and an online part which are labels for
each input z1 , x1 , . . . , zp , xp , U1 , A, ℓ, s, t. Let labκ (U1 , A, ℓ, s, t; r) denote the set of labels encoding the
inputs U1 , A, ℓ, s, t.
Thus one can consider, for a fixed 1, A, ℓ, s, t the correction function f1,A,ℓ,s,t(z1 , x1 , . . . , zp , xp ) =
fκ (z1 , x1 , . . . , zp , xp , U1 , A, ℓ, s, t). The randomized encoding fˆκ is also a randomized encoding of
fˆ1,A,ℓ,s,t , where now the offline part fˆ1,A,ℓ,s,t,off(r) consists of both fˆκ,off (r) and labκ (U1 , A, ℓ, s, t; r). The
online part are labels for z1 , x1 , . . . , zp , xp ; for each j ∈ [p], b ∈ {x, z}, and a ∈ {0, 1}, let labκ (j, b, a; r)
denote the label of the input variable b j when it takes value a, when the DCRE randomness is r
and the topology of the circuit is Tκ .
6.2.2

The Gate Encoding Unitary

We now present the gate encoding unitary GateEnc1,r,A,ℓ,s,t. It acts on registers u = (u1 , . . . , up )
(which represents the input qubits to the gate U1 ), a = (a1 , . . . , ap ) (which represent the ancillas
qubits for the teleportation and correction gadgets), v = (v1 , . . . , vp ) (which represents the entrance
of connecting EPR pairs), and c (which represents a register to hold the classical randomized
encoding of the correction gadget). In the description of the protocol, the unitary Λ1 (ℓ j ) is given
by Lemma 6.2.

40

// Compute the quantum part of the QRE
1
Apply U1 to registers (u1 , . . . , up )
2
Apply Λ1 (ℓ j ) to registers (u j , a j, v j ) for all j ∈ [p]
3
Apply A j to registers (u j , a j , v j ) for all j ∈ [p]
// Compute the classical part of the QRE
4
Compute classical randomized encoding of the correction function f1,A,ℓ,s,t as defined
in Section 6.2.1, and let fˆ1,A,ℓ,s,t,off(r) denote the offline part of the randomized
encoding using randomness r. Store the string fˆ1,A,ℓ,s,t,off(r) in the register c.
Protocol 3: Gate encoding operation GateEnc1,r,A,ℓ,s,t

The quantum part of the gate encoding is illustrated in Figure 4. There, Λ1 denotes the tensor
product of Λ1 (ℓ1 ), . . . , Λp (ℓp ), and A denotes the tensor product of A1 , . . . , Ap .
u 1 , . . . , u p / U1
a1 , . . . , ap /

Λ1

A

v1 , . . . , vp /
Figure 4: The quantum part of the gate encoding GateEnc

Complexity of the Gate Encoding. The gate encoding consists of a quantum part and a classical
part. The quantum part is applying the gate U1 , applying the Λ1 circuits, and then applying the
randomizers A j . Since the Λ1 are QNC0f circuits, and the randomizers is just a single layer of
single- and two-qubit Clifford gates, the quantum encoding can be computed in QNC0f .
The classical part is computing the classical randomized encoding of the correction function
f1,A,ℓ,s,t , which has topology Tκ1 . The complexity of encoding f1,A,ℓ,s,t is inherited from the classical
RE used – if the encoding of CRE can be computed via a NC0 circuit, then the entire gate encoding
procedure can be computed in QNC0f .

6.3 Encoding a Circuit and Input
We now describe the encoding algorithm Enc of the QGC scheme. It takes as input a quantum
circuit F = (T , G) and quantum input y, and outputs the encoding F̂(y; J) where J is a uniform
random string.20 We let n denote the number of qubits of y. The encoding is decomposable, so the
encoding consists of
F̂(y; J) = (F̂off , ŷ1 , . . . , ŷn )
where F̂off is the offline encoding of F̂ and ŷi = F̂i (yi ) is the encoding of the i-th qubit of y.
Let Z and T be the zero input qubits and discarded output qubits of topology T , respectively.
For simplicity we assume that Z is empty (the zero inputs can be incorporated into y).
The offline encoding is presented in Algorithm 4 and the input encoding is presented in
Algorithm 5. First, we discuss details about the label lengths, the ancillary randomness and
quantum random variables used in the encoding.
20

We henceforth use y instead of x to denote the input to the function F being encoded; this is to disambiguate it from
the qubits in register x used by the teleportation and correction gadgets.

41

Label Lengths. Our quantum randomized encoding contains a classical encoding of a correction
function for every gate 1 in the circuit F. To keep track of the lengths of the labels and randomness
required, for every wire w ∈ W we let κw denote the label lengths for encoding each wire w,
and for every gate 1 ∈ G we let c1 denote the size of the CRE encoding of the correction function
associated with 1.
We recursively specify the label lengths κw and encoding sizes c1 , starting from the end of the
circuit. For all output wires w ∈ O, define κw = 1. Then, for every gate 1 ∈ G whose output wires
have label lengths defined so far, let κ1 denote the vector κ1 = (κw′ : w′ ∈ outwire(1)), which has
the label lengths for all the output wires of 1. Recall from Section 6.2.1 that classical circuits with
P
topology Tκ1 have depth dcorr (which is a universal constant) and size σ1 = O( j κ2j ) where κ j is
the label length of the j-th output wire. Thus the CRE encoding of a correction function f1,A,ℓ,s,t
has complexity c1 = c(dcorr , σ1 ) and label lengths κ1 = κ(dcorr , σ1 ), where c(·, ·) and κ(·, ·) are given in
the statement of Lemma 4.3. For every incoming wire w ∈ inwire(1), let κw = κ1 . We then recurse
on the next layer of gates.
The following observations will be useful for our analysis down the line. First, we note that
the encoding complexities c1 and the label lengths κw only depend on the topology T of F, and not
on the specific unitaries of the gates. Second, as a recursive argument shows, if d is the depth of
the quantum circuit F then it holds that c1 ≤ cd and κ1 ≤ κd , where κd , cd are given in the statement
of Lemma 4.3.
Quantum Registers.

We now specify the registers in the encoding.

• y = (y1 , . . . , yn ) is an n-qubit register that initially stores the input state y.
• ew = (ew
, ew
) is a two-qubit register for every wire w ∈ W, initialized with |EPRi.
2
1
• aw = (zw , xw , bw ) is a 2κw + (κw + 1)2 qubit register for every wire w ∈ W, initialized with
zeroes. Some of these qubits are used to store teleportation labels, and others are used as
part of the correction gadget (see Section 6.1.2 for details).
• c1 is a c1 -qubit register for every gate 1 ∈ G, initialized with zeroes. These are used to store
the description of the CRE encoding of the correction functions (see Section 6.2 for details).
• dw is a 4κw -qubit register for every non-traced-out wire w ∈ O \ T , initialized with zeroes.
These qubits store the “label dictionary” for the output wires (i.e. they store all possible
labels for the output wires), so the evaluator can decode the output.
Each part of the encoding F̂off , F̂1 , . . . , F̂n access disjoint subsets of registers.
Classical Randomness. We now specify the classical randomness J that is used by the encoding.
It consists of the following random strings:
• For every gate 1 ∈ G, the random string r1 is a uniformly random string of length c1 . The
randomness is used for the CRE encodings of the correction functions.
• For every gate 1 ∈ G, the random string A1 is a sequence (Aw )w∈outwire(1) where for each
output wire w of 1, the string Aw is a uniformly random element of the randomization group
Rκw . These randomizers are used in the encoding of each gate of the circuit.

42

2
w
w
• For every wire w ∈ W, sw is a random pair of bits (sw
z , sx ) ∈ {0, 1} , and t is a random pair
2
w
of bits (tw
z , tx ) ∈ {0, 1} . These values are used to randomize the teleportation measurements
(see Section 6.1.2).
w
• For every output wire w ∈ O, ow is a random pair of bits (ow
z , ox ). These values are used as
labels for the output wires.

Because the randomness is classical, it can be copied and thus each part of the encoding F̂off, F̂1 , . . . , F̂n
has access to the entire randomness J.
// Set up the labels
1 for w ∈ W do
2

3
4

5
6
7

if w < O then
Let 1, j be such that wire w is the j-th input wire of gate 1.

1
w
w )
Compute the labels ℓw = (ℓb,a
b∈{x,z},a∈{0,1} where ℓb,a = labκ1 (j, b, a; r ) and labκ1 is
the label function corresponding to the CRE encoding of a circuit with topology
Tκ1 .
end
else if w ∈ O then
w = ow and ℓw = ow ⊕ 1 for b ∈ {x, z}.
Let ℓb,0
b
b,1
b

end
9 end
8

// Store the “label dictionary” for output wires (ones not traced out)
10 for w ∈ O \ T do
w , ℓw , ℓw , ℓw ) into the register dw .
11
Write the labels (ℓz,0
z,1 x,0 x,1
12 end

// Encode each gate
13 for 1 ∈ G do
)
, and a1 = (aw )w∈outwire(1) .
14
Let u1 = (ev2 )v∈inwire(1) , v1 = (ew
1 w∈outwire(1)
15

Let ℓ1 = (ℓw )w∈outwire(1) , s1 = (sw )w∈outwire(1) , and t1 = (tw )w∈outwire(1) .

Apply GateEnc1,r1 ,A1 ,ℓ1 ,s1 ,t1 to registers (u 1 , a 1 , v 1 , c 1 ).
17 end
16

Protocol 4: The encoding of the offline part F̂off of F̂.

// Set up the labels
1 Let w denote the i-th input wire of F, and let yi denote the i-th input qubit, and let 1, j be
such that wire w is the j-th input wire of gate 1.
2 Compute the labels ℓw = (ℓw )b∈{x,z},a∈{0,1} where ℓw = labκ1 (j, b, a; r1 ).
b,a
b,a

// Teleport the input qubit into the encoding
3 Apply TPℓw ,sw ,tw to registers (yi , zw , xw , ew ).
1

Protocol 5: The encoding F̂i (yi ) of the i-th input qubit yi .

43

Complexity and Locality of the Encoding. We now argue that QGC has the claimed complexity
properties. First, the QRE is decomposable. The offline part F̂off only depends on the circuit F, the


classical randomness J = r, A, s, t, o , and the EPR pairs (ew ) (except for the qubits ew
for the input
1

wires w). The online part ŷi = F̂i (yi ) only depends on the classical randomness J, the i-th input
qubit yi and the qubit ew
for the i-th input wire w. Thus, the offline encoding and input encoding
1
act on disjoint qubits of the EPR pairs (ew ).
The offline encoding F̂off can be computed using a QNC0f circuit. The label setup procedure can
be parallelized over all wires, and its complexity is inherited from the complexity of computing
labels of CRE (which we are assuming can be done using an NC0 circuit). Since the complexity of
computing the label function labκ1 is at most cd where d is the depth of F, then the time complexity
of the label setup is at most O(cd · |W|).
The gate encoding can be parallelized over all gates, and as discussed in Section 6.2.2, the
complexity of encoding a single gate is O(cd ), which includes the complexity of computing the
classical encoding of the correction functions. Therefore encoding all gates has time complexity
O(cd · |G|). The gate encoding can be implemented by a QNC0f circuit.
Similarly, the encoding of the input qubits can be done in parallel. The complexity of the input
encoding comes from setting up the labels and applying the teleportation gadget. This is O(κd )
complexity for encoding each input qubit, and can be done using a QNC0f circuit.
The Case of Classical Inputs. We observe here that when the input y is classical, the input
encoding process can also be taken to be entirely classical. Although applying the teleportation
gadget TP on the input bits appears to be a fully quantum operation since it involves both a bit
of the input y as well as half of an EPR pair, we note that the EPR pair can in this case be “premeasured” in the standard (computational) basis (so that it collapses to a pair of correlated bits),
and then one can apply a “classical” teleportation gadget:
X sx

•

u
z /

X(ℓz,0 )

x /

X(ℓx,0 )

X(ℓx,0 ⊕ ℓx,1 )
•

v

Xtx

Figure 5: “Classical” teleportation gadget

Note that this circuit simply consists of CNOTs and bit flips, which are classically implementable. If the input state at the beginning of the classical teleportation gagdet is |y, 0, 0, r, ri, then
uzxvu′

the result of applying the gadget is |y ⊕ sx , ℓz,0 , ℓx,e , e ⊕ tx , e ⊕ yi where e = r ⊕ y. Thus the effect of
this circuit is to transfer the bit y to register u′ , and then encrypting it using a random bit e that is
encoded in the label ℓx,e .

6.4 Circuit Evaluation
We now describe the decoding procedure Dec, which takes a quantum randomized encoding F̂(y)
and computes F(y). The decoding procedure depends on the topology T of the circuit F, but does
not depend on the specific gates themselves. The decoder picks an evaluation order π based on
44

the topology T , and sequentially evaluates each gate 1 of the circuit F. Let B denote the set of
“gate placeholders” in the topology T . Let T ⊆ O denote the set of output qubits to be traced out.
1 Compute an evaluation order π for the topology T .

// Evaluate the gates according to π
2 for 1 ∈ B ordered according to π do

Apply the unitary GateEval(1).
4 end
// Decode the output
5 for w ∈ O \ T do
w , ℓw , ℓw , ℓw ) in the register dw , coherently decode
6
Given the set of labels ℓw = (ℓz,0
z,1 x,0 x,1
.
the labels (zw , xw ) in registers (zw , xw ) to bits (d, e) ∈ {0, 1}2 , and apply Zd Xe to ew
2
7 end
3

Protocol 6: The decoding procedure Dec of QGC.

For a p-qubit gate 1, the gate evaluation unitary GateEval(1) is defined as follows. Let
(v1 , . . . , vp ) = inwire(1) and (w1 , . . . , wp ) = outwire(1) denote the input and output wires of 1,
respectively. Let
1. (av1 , . . . , avp ) denote the ancilla registers for the input wires. Each register avi is composed of
subregisters (zvi , xvi , bvi ).
2. (aw1 , . . . , awp ) denote the ancilla registers for the output wires.
vp

3. (ev21 , . . . , e2 ) denote the input wire registers for 1.
w

1
, . . . , e1 p ) denote the output wire registers for 1.
4. (ew
1

5. c1 denote the register storing the (offline portion of the) classical randomized encoding of
d 1, . . . , d
the function f (z1 , x1 , . . . , zp , xp ) that computes a tuple of correction gadgets (Corr
Corrp ).
vj

vj

We note that it may seem strange that the input registers are denoted by e2 , but this is because e2
represents the output end of the EPR pair from a previous gate teleportation.
// Compute the correction circuits
1 Controlled on the values (zv1 , xv1 , . . . , zvp , xvp ) of registers (zv1 , xv1 , . . . , zvp , xvp ), and
controlled on the value fˆoff in register c1 , coherently run CDecT1 ( fˆoff , zv1 , xv1 , . . . , zvp , xvp )
d 1 , Corr
d 2 , . . . , Corr
d p ).
to obtain descriptions of correction circuits (Corr
// Apply the correction circuits

2 for j ∈ [p] do

v

w

Apply Corr j to registers (e2 j , aw j , e1 j ).
wj
vj
4
Apply Λ3 to registers (e2 , aw j , e1 ).
5 end
3

Protocol 7: The gate evaluation operation, GateEval(1), for a p-qubit gate 1.

In the gate evaluation, the map Λ3 is the QNC0f circuit given by Lemma 6.2. Furthermore,
the CRE decoding procedure CDec only depends on the topology T1 of the correction function
45

f , which only depends on the label lengths (κw1 , . . . , κwp ) of the output wires. The complexity
of gate evaluation is dominated by the complexity of running the decoding procedure CDec,
which is polynomial in the size c1 of fˆoff . Thus the complexity of the decoding procedure Dec is
P
O( 1∈B poly(c1 ) + n), which is polynomial in the complexity of the encoding procedure.

6.5 The Simulator
We now present the simulator Sim for QGC. It depends on the topology T of the circuit being
simulated, and takes as input a register s that is supposed to store the output of a quantum
operation F that has topology T . We assume that T has n input wires, and that the input register
s is |O \ T | qubits wide (i.e. the number of output qubits of T that aren’t traced out).
Intuitively the simulator computes the encoding of the identity circuit E with input s padded
with zeroes (so the output should be the quantum state stored in register s). However the topology
T could permute the ordering of qubits, so placing identity gates for all the placeholder gates of
T may still result in a nontrivial operation on the input qubits. Furthermore, the topology T may
trace out some qubits. Thus the simulator pads the input with some zeroes, shuffles the qubits
according to the inverse of the permutation effected by the topology T , and then computes the
randomized encoding of E and the shuffled input.

1 Let E denote the general quantum circuit with topology T and gate set G consisting only

of identity gates.
2 Let n = |I| = |O| denote the number of input and output wires of topology T .
3 Compute the bijection ξ : I → O that is the result of the (unitary part of) E.
4 Let Pξ denote the unitary that swaps n qubits according to the bijection ξ.
5 Let y denote an n-qubit register consisting of s, padded by zeroes.
6 Permute the qubits of y according to the permutation P−1 .
ξ
7 Compute the encoding Ê(y) of circuit E and input in register y.

Protocol 8: The simulator Sim for QGC.

Clearly the complexity of the simulation procedure is polynomial in the complexity of the
encoding procedure.

7 Correctness and Privacy Analysis
We now analyze the correctness and privacy of the QGC scheme. We argue that applying the
decoding procedure Dec to a QRE F̂(y) of a circuit F and input y yields the state F(y) ⊗ ρ, where ρ is
indistinguishable from a density matrix that only depends on the topology T of F, and nothing else
about F. This clearly implies the correctness of the decoding procedure, but also shows the privacy
of the QGC scheme: let E denote the “empty” circuit with the same topology T . As discussed
in Section 6.5, the empty circuit E may effect a permutation P on the qubits of F(y), along with

additional zero qubits. Applying the decoding procedure Dec to QRE Ê P (F(y) ) yields a state
that is indistinguishable from F(y) ⊗ ρ. Since the decoding procedure Dec is unitary, this implies
that



Ê P (F(y) ) ≈ Dec−1 F(y) ⊗ ρ ≈ F̂(y).
46

where “≈” denotes indistinguishability either in the computational or information-theoretic sense,
depending on the security properties of the classical randomized encoding scheme CRE used.
This shows that the simulator Sim, on input F(y), produces a state indistinguishable from F̂(y).
Some Notation. Let QGC denote the quantum randomized encoding scheme described in Section 6, where we use a classical randomized encoding scheme CRE that has perfect correctness
and has polynomial-time encoding, decoding and simulation procedures. We assume that CRE
has (t, ǫ)-privacy with respect to quantum adversaries. In the setting of computational security, t
and ǫ are implicitly functions of a security parameter λ. For a topology T of a classical circuit, let
CDecT and CSimT denote the decoder and simulator for CRE for classical circuits with topology
T, respfectively.
Fix an n-qubit input y, quantum side information q (which may be entangled with y), and
a general quantum circuit F = (T , G) with m = poly(n) gates. Let B denote the set of “gate
placeholders” in the topology T . As described in Section 6.4, the circuit evaluation only depends
on the topology T ; it sequentially evaluates each gate in B according to some evaluation order
π, and then decodes the output wires using the labels in the set O \ T . Let 11 , . . . , 1m ∈ B
denote the placeholder gates of topology T ordered according to π, and let U1 , . . . , Um denote the
corresponding unitaries in circuit F. Let W denote the set of wires in the topology T , with I, O
denoting the input/output wires respectively.
Let F≤i denote the part of circuit F up to (and including) gate 1i . (We define F≤0 to denote the
identity circuit with no gates). Thus, F≤i represents the unitary operation Ui · · · U1 .
Similarly, define F>i to denote the part of circuit F that starts after 1i . (We define F>0 to denote
F). As a quantum operation it first applies the unitaries Ui+1 , . . . , Um , and then traces out the qubits
specified by set T ⊆ O. As we will be considering randomized encodings of the partial circuit F>i ,
we define the randomness used by the encodings. As described in Section 6.3, the randomness
used to encode F = F>0 is the sequence J = (r, A, s, t, o). The randomness used to encode F>i is the
sequence J>i = (r>i , A>i , s>i , t>i , o), where
• r>i = (r1 : 1 comes after 1i )
• A>i = (A1 : 1 comes after 1i )
• s>i = (sw : wire w comes after gates 11 , . . . , 1i )
• t>i = (tw : wire w comes after gates 11 , . . . , 1i )
• o = (ow )w∈O is the same as before.
We define J>0 = J. We define J≤i = J \ J>i . This is all the randomness that is “used up” in evaluating
the first i gates.
Given a classical value c, we write JcK to denote the density matrix |cihc|.

7.1 Analysis of the Decoding Procedure
The decoding procedure Dec evaluates each of the gates of F in sequence (according to some evaluation order), and then traces out a subset of qubits. The following Lemma gives a characterization
of the result of each gate evaluation:

47

Lemma 7.1. Let i ∈ {0, 1, . . . , m−1}. Let GateEvali+1 denote the gate evaluation procedure from Section 6.4
corresponding to the gate 1i+1 of topology T . Let q denote quantum side information that is possibly entangled
with y, but uncorrelated with the classical randomness used by the encoding F̂(y). Then




E GateEvali+1 ( F̂>i ( F≤i (y ; J>i ) ), q = E F̂>i+1 ( F≤i+1 (y ; J>i+1 ) ), q ⊗ t
(7.1)
J>i

J>i+1

where for j ∈ {i, i + 1},
• F̂>j (F̂≤j (y ; J>j )) denotes the quantum randomized encoding of the circuit F>j and input F̂≤j (y), where
the randomness used for the encoding is J>j .
• The density matrix F≤j (y) is stored in registers
(ev2 : v is the predecessor wire to some w ∈ inwire(1 j+1 ))
where v is a predecessor wire to w if v, w are the k-th input and output wires respectively of the same
gate 1, for some k. If w is the k-th input wire of topology T , then there is no predecessor wire, but in
that case we define ev2 to be the register yk .
Furthermore, the density matrix t satisfies the following:
)
.
1. It is on registers (ev2 : v is the predecessor wire to w ∈ inwire(1i+1 )) and (aw , ew
1 w∈inwire(1i+1 )
2. t is (t, ǫ)-indistinguishable from a density matrix t̃ that only depends on topology T .
3. t is unentangled with F̂>i+1 ( F≤i+1 (y) ) and q.
4. The state t is independent of the randomness J>i+1 .
We first show how Lemma 7.1 implies the correctness and privacy of QGC. Using Lemma 7.1
repeatedly, we get


E GateEvalm · GateEvalm−1 · · · GateEval1 ( F̂(y) ; J), q
(7.2)
J

is equal to



E F̂>m ( F≤m (y ; J>m ) ), q ⊗ t1 ⊗ · · · ⊗ tm

J>m

(7.3)

where each ti satisfies the conclusions of the statement of the Lemma. Note that F≤m is the unitary
part of the circuit F (without the tracing out of the output wires T ), and F̂>m is the quantum
randomized encoding of the partial trace operation TrT (·). Let y(m) = F≤m (y) denote the state of the
circuit before tracing out. Since the circuit F>m has no gates, the randomized encoding F̂>m (y(m) )
 (m)

(m)
(m)
is the state ŷ1 , . . . , ŷn , (dw )w∈O\T where ŷ j is the encoding of the j-th qubit of y(m) and dw is
w , ℓw , ℓw , ℓw ) for output wire w ∈ O \ T .
the label dictionary ℓw = (ℓz,0
z,1 x,0 x,1
First we note that the randomness J>m used in the encoding F̂>m (F≤m (y ; J>m )) is the collection
w
w
of random values (ow , sw , tw )w∈O , where ow = (ow
x , oz ) are bits used to generate the labels (ℓ )w∈O
for the output wires, and (sw , tw ) are randomization bits used for the teleportation gadget (see
Section 6.3 for details on the randomness used in the encoding).
(m)
Fix an index j ∈ [n]. The state ŷ j is on the following registers. Let w ∈ O denote the j-th
output wire. Let v ∈ W denote the predecessor wire to w.
(m)

• ev2 . This register initially stores the j-th qubit of y j .
48

• (ew
, ew
). These initially store the EPR pair corresponding to wire w.
2
1
• aw = (zw , xw , bw ). This is the ancilla register for wire w.
(m)

The joint state of ŷ j and the register ew
in (7.3), when averaged over the randomness (ow, sw , tw )w∈O ,
2
is equal to
r
z


(m)
w
e d (m)
w
w
w
w
w
w
J0K
J0K
J0K
J0K
)
,
e
,
(7.4)
=
E
τ
⊗
E
,
ℓ
ℓ
TP
(y
,
,
,
e
E
ℓ ,s ,t
2
1
z,d x,e ⊗ τ ⊗ X Z (y j ) ⊗
j
w
w w w
o ,s ,t

ev2 zw xw ew
1

bw

ew
2

o

d,e

ew
2

ev2 zw xw ew
1

bw

where the density matrix τ denotes the maximally mixed qubit, and J0K denotes the pure state
|0 · · · 0ih0 · · · 0| for the appropriate number of zero bits. Equation (7.4) follows from the following
lemma.
Lemma 7.2. Let u denote a qubit density matrix and let q denote quantum side information that is
possibly entangled with u. Let s = (sz , sx ) and t = (tz , tx ) denote randomization bits. Then for all labels
ℓ = (ℓz,0 , ℓz,1 , ℓx,0 , ℓx,1 ), we have






q
y
E TPℓ,s,t u, J0 · · · 0K , e1 , e2 , q = τ ⊗ E ℓz,d , ℓx,e ⊗ τ ⊗ Xe Zd (u), q
(7.5)
s,t

d,e

where (e1 , e2 ) is initialized in the state |EPRi.
Proof. We prove this by showing that Equation (7.5) holds when u is the outer product |aiha′ | and
there is no quantum side information q; the Lemma follows by linearity of the TP operation.
By Lemma 6.1, we have that

 1X
TPℓ,s,t |ai ⊗ |0 · · · 0i ⊗ |EPRi =
Zsz Xsx |di ⊗ |ℓz,d , ℓx,e i ⊗ Ztz Xtx |ei ⊗ Xe Zd |ai .
2
d,e

Thus


 
E TPℓ,s,t |aiha′ |, J0 · · · 0K , e1 , e2
s,t

′
′
1 X
(−1)sz ·(d⊕d ) · (−1)tz ·(e⊕e ) |d ⊕ sx ihd′ ⊕ sx | ⊗ |ℓz,d , ℓx,e ihℓz,d′ , ℓx,e′ | ⊗ |e ⊕ tx ihe′ ⊕ tx | ⊗ Xe Zd (|aiha′ |)
s,t 4
d,e,d′ ,e′
y
q
1X
Jd ⊕ sx K ⊗ ℓz,d , ℓx,e ⊗ Je ⊕ tx K ⊗ Xe Zd (|aiha′ |)
= E
sx ,tx 4
d,e
y
q
= E τ ⊗ ℓz,d , ℓx,e ⊗ τ ⊗ Xe Zd (|aiha′ |).

=E

d,e


The first observation is that for each w ∈ O, the maximally mixed qubits τ in registers (ev2 , ew
)
1
in Equation (7.4) are completely unentangled from the rest of the state described in (7.3), because
), and is uncorrelated with the
the Pauli twirl bits sw , tw are only used to twirl the registers (ev2 , ew
1
side information q.
)
The next observation is that for each w ∈ T (i.e. the traced-out wires), the registers (zw , xw , ew
2
of (7.3) are in the state
(m)

(m)

e d
w
e d
w w
E E Jow
z ⊕ d, ox ⊕ eK ⊗ X Z (y j ) = wE w Joz , ox K ⊗ E X Z (y j ) = τ ⊗ τ ⊗ τ

w
ow
z ,ox d,e

oz ,ox

49

d,e

w
where w is the j-th output wire. Furthermore, the randomness (ow
z , ox ) is uncorrelated with the rest
w
w
w
of the state described in (7.3), so the registers (z , x , e2 ) are unentangled with the rest of the state.
Finally, for each w ∈ O \ T (i.e. the non-traced-out wires), the registers (dw , zw , xw , ew
) are in the
2
state
w
w w
w
w
e d (m)
E Jow
z , oz ⊕ 1, ox , ox ⊕ 1K ⊗ E Joz ⊕ d, ox ⊕ eK ⊗ X Z (y j )
w w
oz ,ox

d,e

Now consider the decoding procedure Dec, when applied to the encoding F̂(y). It evaluates
each gate by applying GateEval1 , GateEval2 , . . ., and then finally at the end decodes each wire
w ∈ O \ T by undoing the Pauli twirl. The resulting state in registers (dw , zw , xw , ew
) is then
2
indistinguishable from
(m)

w
w w
w
w
E Jow
z , oz ⊕ 1, ox , ox ⊕ 1K ⊗ E Joz ⊕ d, ox ⊕ eK ⊗ y j
w w

oz ,ox

d,e


⊗2
(m)
= E Ja, a ⊕ 1K
⊗ τ⊗2 ⊗ y j .
a

Let σ denote the density matrix Ea Ja, a ⊕ 1K. Putting everything together, the result of applying
the decoding procedure Dec to (F̂(y), q) results in the following state:


 
⊗|O\T |  ⊗|T |
⊗ t 1 ⊗ · · · ⊗ tm .
⊗ τ⊗3
TrT (y(m) ), q ⊗ σ⊗2 ⊗ τ
|
{z
}
ρ

Since F(y) = TrT (y(m) ), this proves the correctness of the decoding procedure. Note that ρ is
(t, ǫ · m)-indistinguishable from the density matrix

⊗|O\T |  ⊗|T |
⊗ τ⊗3
⊗ t̃1 ⊗ · · · ⊗ t̃m
ρ̃ = σ⊗2 ⊗ τ

where each t̃i only depends on T , as given by Lemma 7.1. Thus ρ̃ only depends on the topology

T.
Similarly, since E(P(F(y))) = F(y), it must be that
 


Ê(P(F(y))), q = F(y), q ⊗ ρ′

where ρ′ is (t, ǫ · m)-indistinguishable from ρ̃.
This in turn implies that (F̂(y), q) is (t′ , ǫ′ )-indistinguishable from (Ê(P(F(y))), q) = (Sim(F(y)), q),
where t′ = t − poly(s) where poly(s) is the complexity of Dec, and ǫ′ = ǫ · m. This establishes the
privacy property of QGC.

7.2 Proof of Lemma 7.1
We prove Lemma 7.1 for the case that i = 0; the argument is identical for i > 0. In particular, we
will show that




E GateEval1 ( F̂(y) ; J), q = E F̂>1 ( U1 (y) ; J>1 ), q ⊗ t
(7.6)
J

J>1

where t, q satisfy the conditions in the statement of Lemma 7.1.
Let 11 denote a p-qubit gate, with U1 being the corresponding unitary operator. For simplicity
we drop the subscript and just write 1, U from now on.
In encoding procedure presented in Section 6.3, each gate of F and each input qubit of y is
encoded independently. Thus we can treat F̂ as the following process:
1. Sample classical randomness J = (r, A, s, t, o);
50

2. Compute the labels (ℓw )w∈W ;
3. Apply M ⊗ GateEnc1 ⊗ TP1 where GateEnc1 is the gate encoding unitary for gate 1; the map
TP1 is the unitary to encode the p input qubits of y that are acted upon by U, and M is the
concatenation of all the other gate encoding and input encoding unitaries.
In more detail:
• The map TP1 is equal to

O

TP1 =

TPℓv ,sv ,tv

v∈inwire(1)

where TPℓv ,sv ,tv acts on the registers (yv , av , ev1 ). Here, yv denotes the input qubit that is
encoded into input wire v. The register av can be decomposed as (zv , xv , bv ).
• The map GateEnc1 is equal to
GateEnc1 = GateEnc1,r1 ,A1 ,ℓ1 ,s1 ,t1
where s1 = (sw )w∈outwire(1) , t1 = (tw )w∈outwire(1) , and ℓ1 = (ℓw )w∈outwire(1) . The map GateEnc1
acts on registers (ev2 )v∈inwire(1) , (aw )w∈outwire(1) , (ew
)
, and c1 .
1 w∈outwire(1)
• The map M acts on a disjoint set of registers from TP1 and GateEnc1 .
(yv )
(ev1 )

TP1

(av )
(ev2 )
(aw )
(ew
)
1
(c1 )

GateEval1

GateEnc1

Figure 6: A circuit diagram of the encoding of gate 1 and its inputs, proceeded by its evaluation. The indices v, w range
over inwire(1) and outwire(1) respectively.



We compute the state GateEval1 ( F̂(y ; J) ), q , which is correlated with the randomness J and
labels (ℓw )w∈W . We focus specifically on the registers depicted in Figure 6, which are the ones acted
upon by TP1 , GateEnc1 , and GateEval1 . In what follows, all randomness J and labels (ℓw ) are fixed
unless we explicitly average over certain random variables. Furthermore, the indices v, w range
over inwire(1) and outwire(1) respectively.
Computing the Input Teleportation. Fix v ∈ inwire(1). We compute the result of applying
TPℓv ,sv ,tv to registers (yv , zv , xv , ev1 , ev2 ), after averaging over the randomization bits (sv , tv ):
z
r


 
v
v
v
v
v
v ,sv ,tv y , J0 · · · 0K , e , e
E
TP
⊗ J0K ⊗ τ ⊗ Xev Zdv (yv )
,
ℓ
ℓ
=
τ
⊗
E
ℓ
x,e
2
1
v
z,dv
v v
s ,t

yv zv xv bv ev1

ev2

dv ,ev

where on the right-hand side, the J0K state is on the bv register (the teleportation gadget acts as the
identity on register bv ). This follows from Lemma 7.2.
51

Computing the Gate Encoding. Now we compute the result of applying GateEnc1 , where we’ve
conditioned on specific values of dv , ev :
O

Xev Zdv (yv ), J0 · · · 0K, (ew
GateEnc1
1 )w , J0K
v

ev2

(aw )w

(ew
)
1 w

c1

z
 r


 O
ˆ1,off
f
⊗
Xev Zdv (yv ) , J0 · · · 0K , (ew
)
= A1 · Λ1 · U
w
1

(7.7)

v

The unitary Λ1 is the tensor product
Λ1 =

O

Λ1 (ℓw )

w∈outwire(1)

where Λ1 (ℓw ) are the QNC0f circuits specified by Lemma 6.2. The value fˆ1,off is the (offline part of
the) classical randomized encoding of the correction function f (d1 , e1 , . . . , dp , ep ) (see Section 6.2.1
for the definition of correction functions and their encoding).
By our assumption on the gate set of the circuit F, we use Equation (6.1) to argue that
O
 O

U·
Xev Zdv =
R†dv ,ev · U
v∈inwire(1)

v∈inwire(1)

for single-qubit PX group elements (Rdv ,ev ). Thus, the right-hand side of Equation (7.7) can be
written as
z
 r


O
ˆ1,off
R†dv ,ev U(yv )v , J0 · · · 0K , (ew
f
⊗
)
A1 · Λ1 ·
w
1
v

Computing the Gate Evaluation. Next, we compute the effect of applying the gate evaluation
unitary GateEval1 , which is described in Section 6.4. Controlled on the registers (zv , xv )v , which
v , ℓv ) encoding the Pauli twirl Xev Zdv , the map GateEval uses the encoding
store the labels (ℓz,d
1
x,ev
v
ˆ
f1,off to compute the correction function f (d1 , e1 , . . . , dp , ep ). This yields (descriptions of) correction
gadgets ( d
Corrv )v such that

Corrv = Λ2 (Rdv ,ev , ℓw , sw , tw ) · (Aw )†

where w is the “successor wire” to v (i.e. v, w are the k-th input and output wires of 1, respectively),
and Λ2 (R, ℓ, s, t) are the unitaries specified by Lemma 6.2. Here, we assume that CRE has perfect
correctness, which means that the correction gadgets are computed without error. Furthermore,
for the rest of the section we will interchangeably index the input wires by either v ∈ inwire(1) or
integers 1, . . . , p.
), followed by
The unitary GateEval1 then applies the unitaries Corrv to registers (ev2 , aw , ew
1
applying the QNC0f circuit Λ3 (specified again by Lemma 6.2) to the same registers. Put together,
the state of registers (ev2 , aw , ew
) looks like the following:
1 v,w
(ev2 ) /
(aw ) /

U

R†
Λ1

A1

(ew
) /
1

52

(A1 )†

Λ2

Λ3

N
N
w w w
R
,
Λ
denotes
Here, R denotes
2
d
,e
v v
v Λ2 (Rdv ,ev , ℓ , s , t ), and Λ3 is applied transversally
v
1
in the circuit. The A unitaries cancel out, and we are left with

 
O
R†dv ,ev · U(yv )v , J0 · · · 0K , (ew
)
Λ3 · Λ2 · Λ1 ·
w
1
v

By Lemma 6.2, this is equal to


 O
 O
O
R†dv ,ev U(yv )v , J0 · · · 0K , (ew
Rdv ,ev ·
)
TPℓw ,sw ,tw ·
w
1
v

v

w

The PX unitaries (Rdv ,ev ) cancel out, and we are left with


O
TPℓw ,sw ,tw U(yv )v , J0 · · · 0K , (ew
1 )w
w

) of the “global”
Finishing the Proof. Consider the registers (yv , ev1 , av , ev2 )v , c1 , and (aw , ew
1 w


state GateEval1 ( F̂(y ; J) ), q , where all randomness J is fixed except for the randomization bits
(sv , tv )v∈inwire(1) , which we’ve averaged over. The density matrix in this registers can be written as
O
v

τ⊗2 ⊗ E

yv ev1

dv ,ev

r
z O
z

 r

v
v
ˆ1,off ⊗
w
w
w
J0K
TP
U(yv )v , J0 · · · 0K, (ew
⊗
,
ℓ
f
ℓz,d
⊗
ℓ ,s ,t
x,ev
1 )w
v
bv

zv xv

w

c1

(ev2 )v

(aw )w

(7.8)

(ew
)
1 w

where as usual the indices v, w range over inwire(1), outwire(1) respectively.
We now average over r1 and A1 . Consider the density matrix on registers (yv , ev1 , zv , xv , bv )v and
c1 , which can be written as
z
r
r
z
O
v
v
ˆ1,off
J0K
τ⊗2 ⊗ E ℓz,d
t = 1E 1
f
⊗
⊗
(7.9)
,
ℓ
x,ev
v
r ,A

v

yv ev1

dv ,ev

zv xv

bv

c1

Observe that the density matrix t does not depend on any other randomness of J. The remainder
of the global state can be seen to be equal to the encoding of the partial circuit F>1 with input
F≤1 (y) = U(y), and furthermore does not depend on the randomness J≤1 = (r1 , A1 , (sv , tv )v∈inwire(1) ).
Thus, averaging the global state over J, we get


E GateEval1 ( F̂(y ; J) ), q = E (F̂>1 (F≤1 (y ; J>1 ) , q) ⊗ t .
J

J>1

We are almost done – we just need to argue that t is indistinguishable from a state t̃ that only
depends on the topology T . Note that for fixed (dv , ev )v and A1 , the density matrix
r
z
z r
v
v
ˆ1,off
E1 ℓz,d
,
ℓ
f
(7.10)
⊗
x,ev
v
r

is precisely the output distribution of the CREencoding of the correction function f (d1, e1 , . . . , dp , ep ).
v , ℓv correspond to the
The value fˆ1,off corresponds to the offline part of the encoding, and the ℓz,d
x,ev
v
labels of the input bits dv , ev . The privacy guarantee of CRE is that the density matrix in (7.10) is
(t, ǫ)-indistinguishable from
z

q
y r
d 1 , . . . , Corr
dp
CSimT ( f (d1 , e1 , . . . , dp , ep )) = CSimT Corr
53

where T is the topology of the circuit computing f , and the topology T depends only on the
topology T of F. Thus the density matrix t is (t, ǫ)-indistinguishable from a density matrix t̃,
defined as follows:
r

z
⊗2p
d
d
CSimT Corr1 , . . . , Corrp ⊗ J0K .
t̃ = τ ⊗ 1 E
A ,(dv ,ev )v

d j only depends on A j . Since the A j’s are chosen indeLet A1 = (A1 , . . . , Ap ), and note that Corr
pendently from the randomization group Rκ j for some label length κ j , the distribution of the
d j when averaged over A j is going to be uniform over all correction gadgets corregadget Corr

the discussion at the end of Section 6.1.2 for more details). Thus,
sponding
to label length κ j (see
r
z

d
d
EA1 CSimT Corr1 , . . . , Corrp is a density matrix that only depends on the topology T of F (and
is independent of all other randomness). Thus the density matrix in (7.9) is (t, ǫ)-indistinguishable
from t, which only depends on the topology T .
This completes the proof of Lemma 7.1.

A

Comparison with Related Cryptographic Notions

We now compare quantum randomized encoding with other cryptographic primitives of a similar
nature. While we focus on the quantum variants of these primitives, the distinctions are the same
as in the classical versions.
Secure Multiparty Computation. The goal of secure multiparty computation (MPC) is to allow a
number of parties, each with their own private input xi , to jointly compute a function f (x1 , . . . , xn )
such that no party can learn about others’ inputs. There is a close connection between MPC
and REs, in that REs can often be used to accomplish secure MPC. Indeed, Yao’s garbled circuits
scheme from the 80’s was presented as a technique for achieving secure 2-party computation, and
its distillation into a separate primitive with concrete properties occurred later. Many protocols for
secure quantum MPC have been constructed over the years (see, e.g., [BOCG+ 06, Unr10, DNS10,
DNS12, DGJ+ 19]).
While RE is useful for constructing MPC (and sometimes the other way around), and while
the security in both notions is defined using the simulation paradigm, inherently they are very
different. While MPC is a communication protocol between multiple parties with inputs, RE is not
a protocol and it only considers a single input (one could imagine RE as a single-message protocol
where an encoder with an input sends a message to a decoder without an input). Since in the
context of RE there is only a single party, there is always a trivial solution of computing the function
locally. Therefore usually in RE we are concerned with other properties of the construction beyond
its security, such as the complexity of encoding.
Homomorphic Encryption. Fully homomorphic encryption (FHE) is a method to compute functions on inputs that are encrypted, without having to ever decrypt the information. FHE and RE
also share some commonalities, and there are contexts where both techniques are used to accomplish secure computation and delegation of computation. However there are intrinsic differences
between these two concepts. (See also [App17, Remark 1.4].)
In FHE, a client encrypts an input x and sends Enc(x) to a remote evaluator. The evaluator
can then compute Enc( f (x)) – for any function f – from the given ciphertext, without learning
54

anything about x or f (x). It sends Enc( f (x)) back to the client, who can use its secret decryption
key to recover f (x). It is important that the evaluator does not have access to the decryption key,
because otherwise it will be able to learn the original input x.
With REs, the client sends an encoding of both a function f and an input x, from which
the evaluator can compute the value f (x) in the clear. The evaluator doesn’t have to send any
messages back to the client, and furthermore the evaluator cannot derive an encoding of 1(x) for
some unrelated function 1.
If all we require is decomposable RE, then one can achieve this under minimal assumptions
such as the existence of one-way functions (or even unconditionally in some cases, depending on
the desired complexity properties). FHE (and homomorphic encryption in general) is only known
under stronger assumptions (and cannot be achieved with unconditional security). In particular,
candidates for classical and quantum FHE often rely on the hardness of the learning with errors
problem (or related problems). Quantum FHE was considered recently in [BJ15, DSS16, Mah18,
Bra18].
Program Obfuscation. In program obfuscation, an obfuscator encodes a function f into an
obfuscated program Enc( f ), which is sent to an evaluator. Using the obfuscated program, the
evaluator can compute f (x) for any choice of input x. The security requirement, intuitively, is that
nothing about f is revealed beyond its input-output functionality. The most commonly studied
notions of obfuscation are virtual black-box (VBB) obfuscation and indistinguishability obfuscation (iO),
which differ in how they hide the function f .
While an obfuscated program can be evaluated on multiple inputs (as mant as the user wishes),
in RE the encoding fixes both the function and an input, so it can be thought of as a “one-time
obfuscation”. As explained in [App17, Section 4.4], the obfuscation of the program which has x
hardwired and evaluates f on it, constitutes a RE of f (x). On the other hand, REs can be used to
“bootstrap” obfuscators to have superior complexity properties.
There has been a formalization of quantum program obfuscation [AF16], but it is not yet
known whether general quantum obfuscation can be achieved assuming only classical obfuscation.
Broadbent and Kazmi have recently showed how to achieve indistinguishability obfuscation for
quantum circuits with low T-gate count (at most logarithmically many) [BK20]. As we mention in
Appendix B, a classical RE scheme for quantum circuits can be combined with a classical obfuscator
to imply a quantum obfuscator.

B Potential Applications of QRE
Many of the applications of RE in the classical setting seem to carry over to the quantum setting,
possibly with some necessary adjustments. As the variety of applications of RE is so vast, we
view it as outside the scope of this paper to go over and attempt to re-prove them. We therefore
highlight the most immediate ones here.
PSM and Delegation. Two immediate applications that were mentioned above are private simultaneous messages (PSM) and delegation. Indeed, PSM is almost equivalent to decomposable
RE, and therefore our results show how to achieve PSM in the quantum setting, using quantum
messages and a quantum shared string (or even a classical shared string in the case where the

55

input is completely classical). In terms of delegation, QRE implies that any quantum computation
can be delegated (in 2 messages) using, essentially, a QNC0f verifier.21
Two-Party Secure Computation. Applications to MPC in the context of round reduction also
seem to follow. In particular, one can use our construction to obtain an analogue of Yao’s original
2-message two-party MPC protocol using (classical) oblivious transfer (OT) as a building block.
We recall that in OT, we have a receiver with a bit b, and a sender with two strings r0 , r1 , and in the
end of the execution the receiver learns rb and the sender learns nothing about b.
We can consider two parties A, B, each of which holding a quantum input, x, y respectively,
and they wish to jointly compute a quantum operation F on their inputs whose output is delivered
to A.22 This can be done as follows. Party A encrypts its input with a classical key using a
quantum one-time pad (QOTP, [AMTdW00]), it sends the encrypted input to B and conducts an
OT protocol as a receiver, for each bit of the classical pad for the QOTP. Party B considers a quantum
functionality F′ that takes as input an encrypted x, (unencrypted) y, and classical QOTP key. On
this input, F′ first decrypts x and then applies the original F on x, y. Party B creates a decomposable
QRE of F′ , plugging in the encrypted x that was received from A, and its own unencrypted input
y. We recall that for classical input bits, our QRE is classical and decomposable, which means that
for each classical input bit we can generate two labels r0 , r1 , such that if the value of the bit is b
then the part of the encoding that depends on this bit is rb . This means that party B can send the
parts of the encoding that it can compute, and complete the OT protocol as a sender with values
r0 , r1 for each bit of classical input. This will allow party A to obtain the encoding of F, apply the
decoding procedure and learn the intended output.
It appears that one should be able to prove security of such a protocol in the specious model
[DNS10], which is the mildest model of security in the quantum setting, if the underlying classical
OT primitive is also specious secure.23 However, a formal proof is tangent to the scope of this work
and one should only treat this as a candidate until a formal proof is presented. We also note that
protocols with comparable round complexity can be achieved using quantum fully homomorphic
encryption [BJ15, DSS16, Mah18, Bra18].
One could consider further applications in the context of MPC such as improved quantum
MPC in the multi-party setting and in the malicious setting [DNS12, DGJ+ 19].
Functional Encryption. It was noticed in [SS10] that decomposable RE schemes imply a limited
form of functional encryption (FE). An encryption scheme where there are multiple secret keys,
associated with functions, so that when sk f decrypts Enc(x) the output is f (x). In the classical
setting RE implies FE without “collusion resistance” (i.e. an adversary should not be allowed
to obtain more than a single functional key). It was then showed [GVW12] how to extend this
technique to FE with “bounded collusion”. This construction seem to carry over to the quantum
setting using our QRE scheme, under the appropriate definition of FE. However, some definitional
work is required in order to formally substantiate the definition and show the connection in the
quantum setting.
21

One should be careful since the final step of verification requires comparing two long classical strings, which can
be done in QNC0f with bounded error [HS05].
22
Interestingly, contrary to the classical setting, this does not seem to immediately imply a protocol for the setting
where both parties receive an output with the same round complexity (if we consider a general quantum operation).
One additional round message seems to be needed in this case.
23
At a high level, we believe that a proof goes through by requiring all parties to run all functions of the protocol in a
purified manner.

56

A more ambitious goal is to construct succinct FE schemes (even with bounded collusion) and
so-called “reusable” garbled circuits which are function-private symmetric-key FE, analogously
to the classical constructions in [GKP+ 13] (but possibly using different technique). One obstacle
that seems to prevent direct application is the absence of a quantum attribute-based encryption
schemes that are a central building block in that construction.
Classical Garbling and Quantum Obfuscation. If it is possible to construct a QRE with classical
encoding for classical inputs and function descriptions, then it would allow to construct quantum
indistinguishability obfuscation (iO) from the classical variant, similarly to how classical RE is
leveraged to obtain classical iO [App14a, BCG+ 18]. Constructing iO for quantum circuits is one of
the intriguing open problems in the context of quantum cryptography, and with the connections
between iO and RE in the classical setting, one would hope that QRE could be a useful tool in
establishing it.

C

Proof of Proposition 6.3

Here we give a proof of Proposition 6.3, restated here for convenience:
Proposition C.1. For all single-qubit PX gates R, s = (sz , sx ) ∈ {0, 1}2 , and strings r ∈ {0, 1}κ there exist
QNC0f circuits C1 (r) and C3 and a depth-one Clifford circuit C2 (R, r, s) in the randomization group Rκ such
that the following circuit identity holds:
u

R

z

/

b |0i

/

•

H

X sx

Z sz

(C.1)
C1 (r)

=

X(r)

C2 (R, r, s)

C3

|0i

Here, the register b consists of (κ + 1)2 qubits. Furthermore, descriptions of the circuits C1 (r) and C2 (R, r, s)
can be computed by NC0 circuits of size O(κ2 ).
A general PX group element R can be written (up to a global phase) as Xx Zz Pp for some
x, z, p ∈ {0, 1}. We will perform the analysis for the case of R = X, R = Z, and R = P separately, and
then put everything together to deduce the Proposition.
Before doing so, we will transform the right hand side of (C.1) via sequence of circuit equivalences. First, we observe that the fan-out gate CX(r) which maps |u, z1, . . . , zκ i to |u, z1 ⊕(u·r1 ), . . . , zκ ⊕
(u · rκ )i, when conjugated by Hadamards, becomes a parity gate ⊕(r) that maps |u, z1 , . . . , zκ i to
P
|u ⊕ (z · r), z1 , . . . , zκ i where z · r = i zi · ri . Next, we observe that we can move the Xsx and Zsz gates
before the Hadamard on register u, which changes them to Zsx and Xsz . Thus we get that the right
hand side of (C.1) is equivalent to
u
z1
..
.
zκ

Z sx

R

H
..
.
H
b |0i /

X sz

H
H
..
.
H

⊕(r)

Circuit 7

57

Next, we apply a series of fan-out gates to copy the contents of the registers u, z1 , . . . , zκ to
the ancilla register b. We label the individual qubits of register b as bij where i, j ∈ {0, 1, . . . , κ}.
We first apply a fan-out gate controlled on register u, with targets on {b00 , . . . , b0κ }. Then for each
j ∈ [κ], we apply a fan-out gate controlled on register z j with targets {b j0 , . . . , b jκ }. We call these
the “descending fan-outs”. Then, we apply the same series of fan-out gates in reverse, to undo
the copying procedure. We call these the “ascending fan-outs”. Thus Circuit 7 is equivalent to
Circuit 8.
u

R

z1
..
.
zκ

H
..
.
H

b0 |0i

/

b1 |0i
..
.

/

bκ |0i

/

•

•
•

⊕(r)

Z sx

X sz

•

H
H
..
.
H

• •

..
.

Circuit 8

Next, we move the Zsx and Xsz gates left, before the ascending fan-outs. When moving the Xsz
gate past the fan-out controlled on register u, however, this incurs an Xsz correction on each target
of the fan-out, which are the {b00 , . . . , b0κ } registers. Thus Circuit 8 is equivalent to Circuit 9.
u

R

z1
..
.
zκ

H
..
.
H

b0 |0i

/

b1 |0i
..
.

/

bκ |0i

/

Z sx

•
⊕(r)

X sz

•

•

•
•

•

H
H
..
.
H

(Xsz )⊗κ
..
.

Circuit 9

For now we focus on the part of the circuit depicted in Circuit 10 – we omit the first layer of
Hadamard gates, and everything past the descending fan-out gates. We show, for different gates
R, how to “push” the R correction past the descending fan-out gates.

58

u

•

R

z1
..
.
zκ
b0 |0i

•

⊕(r)

•

/

b1 |0i
..
.

/

bκ |0i

/

..
.

Circuit 10

Case 1. Suppose that R = Xx . First, the Xx gate commutes with the parity gate. Moving it past
the first fan-out gate that is controlled on the register u incurs a Xx correction on each of the {b0 j } j
registers. Thus Circuit 10 is equivalent to Circuit 11.

z1
..
.
zκ

Xx

•

u

•

⊕(r)

•
(Xx )⊗κ

b0 |0i /
b1 |0i /
..
.

..
.

bκ |0i /
Circuit 11

Case 2. Suppose now that R = Zz . Moving the Zz gate past the parity gate incurs a Zz·r j correction
on the register z j . This can be seen by repeatedly applying the identity CNOTa,b · (Ia ⊗ Zb ) =
(Za ⊗ Zb )CNOTa,b , where CNOTa,b denotes a CNOT with control a and target b. Furthermore, the
Z gates all commute with the fan-out gates. Thus Circuit 10 is equivalent to Circuit 12.

z1
..
.
zκ

Zz

•

u

•

⊕(r)

•

b0 |0i /
b1 |0i /
..
.

..
.

bκ |0i /
Circuit 12

59

Zz·r1
..
.
z·r
Z κ

Case 3. Suppose now that R = Pp . Then we claim that Circuit 10 is equivalent to Circuit 13.
Here, if p = 0, then the gate Γp,r is the identity. Otherwise, the gate Γp,r stands for the following
tensor-product of CZ gates:24
1. CZ(b0 j , b j0 ) for all j such that r j = 1, and
2. CZ(bij , b ji ) for all i < j such that ri = r j = 1.
Notice that all of these CZ gates are disjoint, and thus can be implemented in a single layer.
Pp

•

u
z1
..
.
zκ

•

⊕(r)

•

Pp·r1
..
.
p·r
P κ

b0 |0i /

b1 |0i /
..
.
bκ |0i /

Γp,r

..
.
Circuit 13

This can be verified by calculating the behavior of both circuits. For simplicity assume that
p = 1. Circuit 10 on input |u, z1 , . . . , zκ i produces an output state that has the following structure:
• It is pre-multiplied by a phase factor iu
• Registers u0 and b0 j are in the state |u ⊕ (z · r)i for all j.
• Registers zi and bij are in the state |zi i for all i > 0 and all j.
On the other hand, the state of Circuit 13 is exactly the same except the phase factor in front is the
product of
• i raised to the power u + (z · r) mod 2 (this comes from the P gate on register u).
P
• i raised to the power i zi (this comes from the P gates on registers {zi }).
P
• −1 raised to the power (u + 1) j:r j =1 z j (this comes from the CZ gates applied to (b0 j , b j0 ) for
all j such that r j = 1).
P
• −1 raised to the power i<j:ri =r j =1 zi z j (this comes from the CZ gates applied to (bij , b ji ) for all
i < j such that ri = r j = 1).
Using the identity that for bits c1 , . . . , cn ,
c1 + · · · + cn

mod 2 =

X
i

ci − 2

X

ci c j

i<j

we get that these phase factors are equivalently
24

Recall that a CZ gate is a controlled-Z gate; it maps |a, bi to (−1)ab |a, bi.

60

mod 4,

P
P
P
• i raised to the power u + i:ri =1 zi − 2u j:r j =1 z j − 2 i<j:ri =r j =1 zi z j
P
• i raised to the power i:ri =1 zi
P
• i raised to the power 2(u + 1) j:r j =1 z j
P
• i raised to the power 2( i<j:ri =r j =1 zi z j )

Summing all of these exponents modulo 4, we get that the phase factor is iu , as desired.
General case. Suppose that R is a general PX group element, so it can be written (up to a global
phase) as R = Xx Zz Pp for x, z, p ∈ {0, 1}. Then by combining Cases 1, 2 and 3 we determine that
Circuit 7 is equivalent to Circuit 14.
•

u
z1

H

..
.
zκ

..
.
H

b0 |0i

/

b1 |0i
..
.

/

bκ |0i

/

•
⊕(r)
•

Pp

Zz

Pp·r1

Zz·r1

..
.

..
.

Pp·rκ

Zz·rκ
(Xx )⊗κ

Xx

Z sx

X sz

•
•
•

H
H
..
.
H

(Xsz )⊗κ

Γp,r

Circuit 14

Note that Circuit 14 has the desired structure:
• Letting C1 (r) denote the the subcircuit up to and including the descending fan-out gates, we
see that C1 only depends on r and is independent of R and s. Furthermore, C1 (r) can be
implemented as a QNC0f circuit.
• Letting C2 (R, r, s) denote the subcircuit in between the descending and ascending fan-out
gates, we see that C2 depends on R, r, s, and can be implemented as a tensor product of
single-qubit Clifford unitaries on all registers except for the pairs (b0 j , b j0 ) for j > 0, which
have two-qubit Clifford unitaries acting on them (namely, products of X and CZ gates).
• Letting C3 denote the subcircuit that includes the ascending fan-out gates as well as the final
layer of Hadamard gates, we see that C3 is independent of R, r, s, and can be implemented as
a QNC0f circuit.
Furthermore, the description of the circuit C2 (R, r, s) in Lines 7 through 12 shows that each of
the single- and two-qubit gates are simple functions of the inputs (R, r, s), so this description can
be computed by a classical NC0 circuit of size O(κ2 ).
This concludes the proof of the Proposition.

61

References
On quantum obfuscation.

arXiv preprint

[AF16]

Gorjan Alagic and Bill Fefferman.
arXiv:1602.01771, 2016.

[AG04]

Scott Aaronson and Daniel Gottesman. Improved simulation of stabilizer circuits.
CoRR, quant-ph/0406196, 2004.

[AIK04]

Benny Applebaum, Yuval Ishai, and Eyal Kushilevitz. Cryptography in NC0 . In
45th Symposium on Foundations of Computer Science (FOCS 2004), 17-19 October 2004,
Rome, Italy, Proceedings, pages 166–175, 2004.

[AIK06]

Benny Applebaum, Yuval Ishai, and Eyal Kushilevitz. Computationally private randomizing polynomials and their applications. Computational Complexity, 15(2):115–
162, 2006.

[AMTdW00] Andris Ambainis, Michele Mosca, Alain Tapp, and Ronald de Wolf. Private quantum
channels. In 41st Annual Symposium on Foundations of Computer Science, FOCS 2000,
12-14 November 2000, Redondo Beach, California, USA, pages 547–553, 2000.
[App14a]

Benny Applebaum. Bootstrapping obfuscators via fast pseudorandom functions. In
Palash Sarkar and Tetsu Iwata, editors, Advances in Cryptology - ASIACRYPT 2014 20th International Conference on the Theory and Application of Cryptology and Information
Security, Kaoshiung, Taiwan, R.O.C., December 7-11, 2014, Proceedings, Part II, volume
8874 of Lecture Notes in Computer Science, pages 162–172. Springer, 2014.

[App14b]

Benny Applebaum. Cryptography in Constant Parallel Time. Information Security and
Cryptography. Springer, 2014.

[App17]

Benny Applebaum. Garbled circuits as randomized encodings of functions: a primer.
In Yehuda Lindell, editor, Tutorials on the Foundations of Cryptography, pages 1–44.
Springer International Publishing, 2017.

[BCG+ 18]

Nir Bitansky, Ran Canetti, Sanjam Garg, Justin Holmgren, Abhishek Jain, Huijia Lin,
Rafael Pass, Sidharth Telang, and Vinod Vaikuntanathan. Indistinguishability obfuscation for RAM programs and succinct randomized encodings. SIAM J. Comput.,
47(3):1123–1210, 2018.

[BFK09]

Anne Broadbent, Joseph Fitzsimons, and Elham Kashefi. Universal blind quantum
computation. In 2009 50th Annual IEEE Symposium on Foundations of Computer Science,
pages 517–526. IEEE, 2009.

[BFM88]

Manuel Blum, Paul Feldman, and Silvio Micali. Non-interactive zero-knowledge
and its applications (extended abstract). In Janos Simon, editor, Proceedings of the
20th Annual ACM Symposium on Theory of Computing, May 2-4, 1988, Chicago, Illinois,
USA, pages 103–112. ACM, 1988.

[BG19]

Anne Broadbent and Alex B Grilo. Zero-knowledge for qma from locally simulatable
proofs. arXiv preprint arXiv:1911.07782, 2019.

62

[BJ15]

Anne Broadbent and Stacey Jeffery. Quantum homomorphic encryption for circuits
of low t-gate complexity. In Advances in Cryptology - CRYPTO 2015 - 35th Annual
Cryptology Conference, Santa Barbara, CA, USA, August 16-20, 2015, Proceedings, Part
II, pages 609–629, 2015.

[BJSW16]

Anne Broadbent, Zhengfeng Ji, Fang Song, and John Watrous. Zero-knowledge proof
systems for qma. In 2016 IEEE 57th Annual Symposium on Foundations of Computer
Science (FOCS), pages 31–40. IEEE, 2016.

[BK05]

Sergey Bravyi and Alexei Kitaev. Universal quantum computation with ideal Clifford
gates and noisy ancillas. Physical Review A, 71(2):022316, February 2005.

[BK20]

Anne Broadbent and Raza Ali Kazmi. Indistinguishability obfuscation for quantum
circuits of low t-count. arXiv preprint arXiv:2005.14699, 2020.

[Blu86]

Manuel Blum. How to prove a theorem so no one else can claim it, August 1986.
Invited 45 minute address to the International Congress of Mathematicians, 1986. To
appear in the Proceedings of ICM 86.

[BMR90]

Donald Beaver, Silvio Micali, and Phillip Rogaway. The round complexity of secure
protocols (extended abstract). In Proceedings of the 22nd Annual ACM Symposium on
Theory of Computing, May 13-17, 1990, Baltimore, Maryland, USA, pages 503–513, 1990.

[BOCG+ 06]

Michael Ben-Or, Claude Crépeau, Daniel Gottesman, Avinatan Hassidim, and Adam
Smith. Secure multiparty quantum computation with (only) a strict honest majority.
In 2006 47th Annual IEEE Symposium on Foundations of Computer Science (FOCS’06),
pages 249–260. IEEE, 2006.

[Bra18]

Zvika Brakerski. Quantum FHE (almost) as secure as classical. In Hovav Shacham
and Alexandra Boldyreva, editors, Advances in Cryptology - CRYPTO 2018 - 38th
Annual International Cryptology Conference, Santa Barbara, CA, USA, August 19-23,
2018, Proceedings, Part III, volume 10993 of Lecture Notes in Computer Science, pages
67–95. Springer, 2018.

[BS20]

Nir Bitansky and Omri Shmueli. Post-quantum zero knowledge in constant rounds.
In Proceedings of the 52nd Annual ACM SIGACT Symposium on Theory of Computing,
pages 269–279, 2020.

[CR20]

Lijie Chen and Hanlin Ren. Strong average-case circuit lower bounds from nontrivial derandomization. Electronic Colloquium on Computational Complexity (ECCC),
27:10, 2020. To appear in STOC 2020.

[CVZ20]

Andrea Coladangelo, Thomas Vidick, and Tina Zhang. Non-interactive zeroknowledge arguments for qma, with preprocessing. In Annual International Cryptology Conference, pages 799–828. Springer, 2020.

[DGJ+ 19]

Yfke Dulek, Alex B. Grilo, Stacey Jeffery, Christian Majenz, and Christian Schaffner.
Secure multi-party quantum computation with a dishonest majority. CoRR,
abs/1909.13770, 2019.

63

[DNS10]

Frédéric Dupuis, Jesper Buus Nielsen, and Louis Salvail. Secure two-party quantum
evaluation of unitaries against specious adversaries. In Tal Rabin, editor, Advances
in Cryptology - CRYPTO 2010, 30th Annual Cryptology Conference, Santa Barbara, CA,
USA, August 15-19, 2010. Proceedings, volume 6223 of Lecture Notes in Computer
Science, pages 685–706. Springer, 2010.

[DNS12]

Frédéric Dupuis, Jesper Buus Nielsen, and Louis Salvail. Actively secure two-party
evaluation of any quantum operation. In Reihaneh Safavi-Naini and Ran Canetti,
editors, Advances in Cryptology - CRYPTO 2012 - 32nd Annual Cryptology Conference,
Santa Barbara, CA, USA, August 19-23, 2012. Proceedings, volume 7417 of Lecture Notes
in Computer Science, pages 794–811. Springer, 2012.

[DSS16]

Yfke Dulek, Christian Schaffner, and Florian Speelman. Quantum homomorphic
encryption for polynomial-sized circuits. In Advances in Cryptology - CRYPTO 2016 36th Annual International Cryptology Conference, Santa Barbara, CA, USA, August 14-18,
2016, Proceedings, Part III, pages 3–32, 2016.

[FKN94]

Uriel Feige, Joe Kilian, and Moni Naor. A minimal model for secure computation
(extended abstract). In Frank Thomson Leighton and Michael T. Goodrich, editors,
Proceedings of the Twenty-Sixth Annual ACM Symposium on Theory of Computing, 23-25
May 1994, Montréal, Québec, Canada, pages 554–563. ACM, 1994.

[FLS90]

Uriel Feige, Dror Lapidot, and Adi Shamir. Multiple non-interactive zero knowledge
proofs based on a single random string (extended abstract). In 31st Annual Symposium
on Foundations of Computer Science, St. Louis, Missouri, USA, October 22-24, 1990,
Volume I, pages 308–317. IEEE Computer Society, 1990.

[FS86]

Amos Fiat and Adi Shamir. How to prove yourself: Practical solutions to identification and signature problems. In Conference on the theory and application of cryptographic
techniques, pages 186–194. Springer, 1986.

[GKP+ 13]

Shafi Goldwasser, Yael Kalai, Raluca Ada Popa, Vinod Vaikuntanathan, and Nickolai
Zeldovich. Reusable garbled circuits and succinct functional encryption. In Proceedings of the forty-fifth annual ACM symposium on Theory of computing, pages 555–564,
2013.

[GMR89]

Shafi Goldwasser, Silvio Micali, and Charles Rackoff. The knowledge complexity of
interactive proof systems. SIAM Journal on computing, 18(1):186–208, 1989.

[GMW91]

Oded Goldreich, Silvio Micali, and Avi Wigderson. Proofs that yield nothing but
their validity or all languages in np have zero-knowledge proof systems. Journal of
the ACM (JACM), 38(3):690–728, 1991.

[Gol06]

Oded Goldreich. Foundations of Cryptography: Volume 1. Cambridge University Press,
USA, 2006.

[Got98]

Daniel Gottesman. The Heisenberg Representation of Quantum Computers.
arXiv:quant-ph/9807006, July 1998. arXiv: quant-ph/9807006.

[GVW12]

Sergey Gorbunov, Vinod Vaikuntanathan, and Hoeteck Wee. Functional encryption
with bounded collusions via multi-party computation. In Reihaneh Safavi-Naini and
64

Ran Canetti, editors, Advances in Cryptology - CRYPTO 2012 - 32nd Annual Cryptology
Conference, Santa Barbara, CA, USA, August 19-23, 2012. Proceedings, volume 7417 of
Lecture Notes in Computer Science, pages 162–179. Springer, 2012.
[HS05]

Peter Høyer and Robert Spalek. Quantum fan-out is powerful. Theory of Computing,
1(1):81–103, 2005.

[HV16]

Carmit Hazay and Muthuramakrishnan Venkitasubramaniam. On the power of
secure two-party computation. In Matthew Robshaw and Jonathan Katz, editors,
Advances in Cryptology - CRYPTO 2016 - 36th Annual International Cryptology Conference, Santa Barbara, CA, USA, August 14-18, 2016, Proceedings, Part II, volume 9815 of
Lecture Notes in Computer Science, pages 397–429. Springer, 2016.

[JKPT12]

Abhishek Jain, Stephan Krenn, Krzysztof Pietrzak, and Aris Tentes. Commitments
and efficient zero-knowledge proofs from learning parity with noise. In International
Conference on the Theory and Application of Cryptology and Information Security, pages
663–680. Springer, 2012.

[Kil88]

Joe Kilian. Founding cryptography on oblivious transfer. In Proceedings of the 20th
Annual ACM Symposium on Theory of Computing, May 2-4, 1988, Chicago, Illinois, USA,
pages 20–31, 1988.

[KW17]

Elham Kashefi and Petros Wallden. Garbled quantum computation. Cryptography,
1(1):6, 2017.

[Mah18]

Urmila Mahadev. Classical homomorphic encryption for quantum circuits. In 59th
IEEE Annual Symposium on Foundations of Computer Science, FOCS 2018, Paris, France,
October 7-9, 2018, pages 332–338, 2018.

[Moo99]

Cristopher Moore. Quantum circuits: Fanout, parity, and counting. Electronic Colloquium on Computational Complexity (ECCC), 6(32), 1999.

[Rog91]

Philip Rogaway. The Round-Complexity of Secure Protocols. PhD thesis, MIT, 1991.

[RT19]

Ran Raz and Avishay Tal. Oracle separation of BQP and PH. In Proceedings of the
51st Annual ACM SIGACT Symposium on Theory of Computing, STOC 2019, Phoenix,
AZ, USA, June 23-26, 2019, pages 13–23, 2019.

[SS10]

Amit Sahai and Hakan Seyalioglu. Worry-free encryption: functional encryption
with public keys. In Ehab Al-Shaer, Angelos D. Keromytis, and Vitaly Shmatikov,
editors, Proceedings of the 17th ACM Conference on Computer and Communications Security, CCS 2010, Chicago, Illinois, USA, October 4-8, 2010, pages 463–472. ACM, 2010.

[Unr10]

Dominique Unruh. Universally composable quantum multi-party computation. In
Annual International Conference on the Theory and Applications of Cryptographic Techniques, pages 486–505. Springer, 2010.

[VZ20]

Thomas Vidick and Tina Zhang. Classical zero-knowledge arguments for quantum
computations. Quantum, 4:266, 2020.

[Wat09]

John Watrous. Zero-knowledge against quantum attacks. SIAM Journal on Computing,
39(1):25–58, 2009.
65

[Yao86]

Andrew Chi-Chih Yao. How to generate and exchange secrets (extended abstract).
In FOCS, pages 162–167, 1986.

[Zha19]

Jiayu Zhang. Delegating quantum computation in the quantum random oracle
model. In Dennis Hofheinz and Alon Rosen, editors, Theory of Cryptography - 17th
International Conference, TCC 2019, Nuremberg, Germany, December 1-5, 2019, Proceedings, Part II, volume 11892 of Lecture Notes in Computer Science, pages 30–60. Springer,
2019.

[Zha20]

Jiayu Zhang. Succinct Blind Quantum Computation Using a Random Oracle, 2020.
arXiv:2004.12621v2.

66


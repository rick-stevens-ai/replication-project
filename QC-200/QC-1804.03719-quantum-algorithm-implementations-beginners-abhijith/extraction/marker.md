<!--
SURROGATE marker.md for arXiv:1804.03719 (Abhijith et al., "Quantum Algorithm
Implementations for Beginners", LANL, 2018/2022).

Provenance: Marker (`marker-pdf`, VikParuchuri) was installed in
`venv/` and invoked with `marker_single work/paper.pdf extraction/marker_out`.
The tool loaded its surya + texify + reading-order models successfully on
MPS, then aborted mid-parse with
    TypeError: Invalid input type 'PdfDocument'
raised from `pypdfium2._helpers.document._open_pdf`. This is a version
skew between `marker-pdf` 0.2.x and the current `pypdfium2` API (pdftext
wraps the PDF twice; the newer pypdfium2 rejects a nested PdfDocument
input). Full trace is preserved in `extraction/marker.log`.

Rather than downgrade pypdfium2 and iterate, we ship the documented
`pdftotext -layout` surrogate below with this provenance header, matching
the convention used by the sibling replication
`QC-quant-ph-9709029-entanglement-formation-two-qubits-wootters`. Downstream
tools that look for `extraction/marker.md` will find valid Markdown-shaped
text (headings/paragraphs preserved by pdftotext's layout mode).

If regenerated with a pinned older pypdfium2, the real command would be:
    marker_single work/paper.pdf extraction/marker_out
producing `extraction/marker_out/paper/paper.md`.
-->

                                         Quantum Algorithm Implementations for Beginners

                                         ABHIJITH J.∗ , ADETOKUNBO ADEDOYIN, JOHN AMBROSIANO, PETR ANISIMOV,
                                         WILLIAM CASPER, GOPINATH CHENNUPATI, CARLETON COFFRIN, HRISTO DJIDJEV,
                                         DAVID GUNTER, SATISH KARRA, NATHAN LEMONS, SHIZENG LIN, ALEXANDER MA-




arXiv:1804.03719v3 [cs.ET] 27 Jun 2022
                                         LYZHENKOV, DAVID MASCARENAS, SUSAN MNISZEWSKI, BALU NADIGA, DANIEL
                                         O’MALLEY, DIANE OYEN, SCOTT PAKIN, LAKSHMAN PRASAD, RANDY ROBERTS,
                                         PHILLIP ROMERO, NANDAKISHORE SANTHI, NIKOLAI SINITSYN, PIETER J. SWART,
                                         JAMES G. WENDELBERGER, BORAM YOON, RICHARD ZAMORA, WEI ZHU, STEPHAN
                                         EIDENBENZ∗ , ANDREAS BÄRTSCHI∗ , PATRICK J. COLES∗ , MARC VUFFRAY∗ , and AN-
                                         DREY Y. LOKHOV∗ ,
                                         Los Alamos National Laboratory, Los Alamos, New Mexico 87545, USA
                                         As quantum computers become available to the general public, the need has arisen to train a cohort of
                                         quantum programmers, many of whom have been developing classical computer programs for most of
                                         their careers. While currently available quantum computers have less than 100 qubits, quantum computing
                                         hardware is widely expected to grow in terms of qubit count, quality, and connectivity. This review aims
                                         to explain the principles of quantum programming, which are quite different from classical programming,
                                         with straightforward algebra that makes understanding of the underlying fascinating quantum mechanical
                                         principles optional. We give an introduction to quantum computing algorithms and their implementation on
                                         real quantum hardware. We survey 20 different quantum algorithms, attempting to describe each in a succinct
                                         and self-contained fashion. We show how these algorithms can be implemented on IBM’s quantum computer,
                                         and in each case, we discuss the results of the implementation with respect to differences between the simulator
                                         and the actual hardware runs. This article introduces computer scientists, physicists, and engineers to quantum
                                         algorithms and provides a blueprint for their implementations.

                                                                                             Contents
                                            Abstract                                                                                                         1
                                            Contents                                                                                                         1
                                            1     Introduction                                                                                               3
                                            1.1      The quantum computing programming model                                                                 4
                                            1.1.1          The qubit                                                                                         4
                                            1.1.2          System of qubits                                                                                  5
                                            1.1.3          Superposition and entanglement                                                                    5
                                            1.1.4          Inner and outer products                                                                          6
                                            1.1.5          Measurements                                                                                      7
                                            1.1.6          Unitary transformations and gates                                                                 7
                                            1.1.7          Observables and expectation values                                                                8
                                            1.1.8          Quantum circuits                                                                                 11
                                            1.1.9          Quantum algorithms                                                                               11
                                            1.2      Implementations on a real quantum computer                                                             12
                                            1.2.1          The IBM quantum computer                                                                         12
                                            1.2.2          Programming the IBM quantum computer: Qiskit library                                             13
                                            1.3      Classes of quantum algorithms                                                                          16
                                            2     Grover’s Algorithm                                                                                        17
                                         ∗ abhijithj@lanl.gov; eidenben@lanl.gov; baertschi@lanl.gov; pcoles@lanl.gov; vuffray@lanl.gov; lokhov@lanl.gov. LA-UR-

                                         20-22353
2                                                                             Abhijith J., et al.


    2.1       Problem definition and background                                              17
    2.2       Algorithm description                                                          18
    2.3       Algorithm implemented on IBM’s 5-qubit computer                                19
    3      Bernstein-Vazirani Algorithm                                                      19
    3.1       Problem definition and background                                              19
    3.2       Algorithm description                                                          20
    3.3       Algorithm implemented on IBM’s 5-qubit and 16-qubit computers                  21
    4      Linear Systems                                                                    23
    4.1       Problem definition and background                                              23
    4.2       Algorithm description                                                          24
    4.3       Phase estimation                                                               24
    4.4       Algorithm implemented on IBM’s 5 qubit computer                                27
    5      Shor’s Algorithm for Integer Factorization                                        29
    5.1       Problem definition and background                                              29
    5.2       Algorithm description                                                          30
    5.3       Algorithm implemented on IBM’s 5-qubit computer                                32
    6      Matrix Elements of Group Representations                                          32
    6.1       Problem definition and background                                              32
    6.2       Algorithm description                                                          36
    6.3       Algorithm implemented on IBM’s 5-qubit computer                                37
    7      Quantum Verification of Matrix Products                                           38
    7.1       Problem definition and background                                              38
    7.2       Algorithm description                                                          39
    8      Group Isomorphism                                                                 40
    8.1       Problem definition and background                                              40
    8.2       Algorithm description                                                          41
    8.3       Algorithm implemented using Qiskit                                             42
    9      Quantum Random Walks                                                              44
    9.1       Problem definition and background                                              44
    9.2       Example of a quantum random walk                                               44
    9.3       Algorithm implementation using Qiskit on IBM Q                                 45
    10     Quantum Minimal Spanning Tree                                                     46
    10.1      Problem definition and background                                              46
    10.2      Algorithm description                                                          47
    11     Quantum Maximum Flow Analysis                                                     51
    11.1      Problem definition and background                                              51
    11.2      Algorithm description                                                          52
    12     Quantum Approximate Optimization Algorithm                                        53
    12.1      Problem definition and background                                              53
    12.2      Algorithm description                                                          55
    12.3      QAOA MaxCut on ibmqx2                                                          58
    12.4      A proof-of-concept experiment                                                  60
    13     Quantum Principal Component Analysis                                              62
    13.1      Problem definition and background                                              62
    13.2      Algorithm description                                                          63
    13.3      Algorithm implemented on IBM’s 5-qubit computer                                65
    14     Quantum Support Vector Machine                                                    66
    15     Quantum Simulation of the Schrödinger Equation                                    67
Quantum Algorithm Implementations for Beginners                                                  3


    15.1    Problem definition and background                                                   67
    15.2    Algorithm description                                                               68
    15.3    Algorithm implemented on IBM’s 5-qubit computer                                     69
    16 Ground State of the Transverse Ising Model                                               70
    16.1    Variational quantum eigenvalue solver                                               70
    16.2    Simulation and results                                                              72
    17 Quantum Partition Function                                                               74
    17.1    Background on the partition function                                                74
    17.2    A simple example                                                                    76
    17.3    Calculating the quantum partition function                                          77
    17.4    Implementation of a quantum algorithm on the IBM Quantum Experience                 77
    18 Quantum State Preparation                                                                78
    18.1    Single qubit state preparation                                                      78
    18.2    Schmidt decomposition                                                               79
    18.3    Two-qubit state preparation                                                         81
    18.4    Two-qubit gate preparation                                                          81
    18.5    Four qubit state preparation                                                        82
    19 Quantum Tomography                                                                       82
    19.1    Problem definition and background                                                   82
    19.2    Short survey of existing methods                                                    85
    19.3    Implementation of the Maximum Likelihood method on 5-qubit IBM QX                   86
    19.3.1        Warm-up: Hadamard gate                                                        86
    19.3.2        Maximally entangled state for two qubits                                      87
    20 Tests of Quantum Error Correction in IBM Q                                               88
    20.1    Problem definition and background                                                   88
    20.2    Test 1: errors in single qubit control                                              89
    20.3    Test 2: errors in entangled 3 qubits control                                        90
    20.4    Discussion                                                                          90
    Acknowledgments                                                                             91
    References                                                                                  91




1   INTRODUCTION
Quantum computing exploits quantum-mechanical effects—in particular superposition, entangle-
ment, and quantum tunneling—to more efficiently execute a computation. Compared to traditional,
digital computing, quantum computing offers the potential to dramatically reduce both execution
time and energy consumption. These potential advantages, steady advances in nano-manufacturing,
and the slow-down of traditional hardware scaling laws (such as Moore’s Law) have led to a substan-
tial commercial and national-security interest and investment in quantum computing technology
in the 2010s. Recently, Google announced that it has reached a major milestone known as quan-
tum supremacy–the demonstration that a quantum computer can perform a calculation that is
intractable on a classical supercomputer [9]. The problem tackled here by the quantum computer
is not one with any direct real-world application. Nonetheless, this is a watershed moment for
quantum computing and is widely seen as an important step on the road towards building quantum
computers that will offer practical speedups when solving real-world problems [100]. (See [3] for a
precise technical definition of quantum supremacy.)
4                                                                                             Abhijith J., et al.


   While the mathematical basis of quantum computing, the programming model, and most quantum
algorithms have been published decades ago (starting in the 1990s), they have been of interest only
to a small dedicated community. We believe the time has come to make quantum algorithms and
their implementations accessible to a broad swath of researchers and developers across computer
science, software engineering, and other fields. The quantum programming model is fundamentally
different from traditional computer programming. It is also dominated by physics and algebraic
notations that at times present unnecessary entry barriers for mainstream computer scientists and
other more mathematically trained scientists.
   In this review, we provide a self-contained, succinct description of quantum computing and of
the basic quantum algorithms with a focus on implementation. Since real quantum computers, such
as IBM Q [69], are now available as a cloud service, we present results from simulator and actual
hardware experiments for smaller input data sets. Other surveys of quantum algorithms with a
different target audience and also without actual implementations include [11, 30, 72, 90, 91, 106].
Other cloud service based quantum computers are also available from Rigetti and IonQ, but in this
review we will focus solely on IBM’s quantum computing ecosystem. The code and implementations
accompanying the paper can be found at https://github.com/lanl/quantum_algorithms.

1.1   The quantum computing programming model
Here we provide a self-contained description of the quantum computing programming model. We
will define the common terms and concepts used in quantum algorithms literature. We will not
discuss how the constructs explained here are related to the foundations of quantum mechanics.
Interested readers are encouraged to take a look at Ref. [92] for a more detailed account along those
lines. Readers with a computer science background are referred to Refs. [82, 103, 136], for a more
comprehensive introduction to quantum computing from a computer science perspective.
   Quantum computing basically deals with the manipulation of quantum systems. The physical
details of this is dependent on the quantum computer’s hardware design. Here we will only talk
about the higher level abstractions used in quantum computing: a typical programmer will only
be exposed to these abstractions. The state of any quantum system is always represented by a
vector in a complex vector space (usually called a Hilbert space). Quantum algorithms are always
expressible as transformations acting on this vector space. These basic facts follow from the axioms
of quantum mechanics. Now we will explain some of the basic concepts and terminology used in
quantum computing.

1.1.1 The qubit. The qubit (short for ’quantum bit’) is the fundamental information carrying unit
used in quantum computers. It can be seen as the quantum mechanical generalization of a bit used
in classical computers. More precisely, a qubit is a two dimensional quantum system. The state of a
qubit can be expressed as,

                                           |𝜙⟩ = 𝛼 |0⟩ + 𝛽 |1⟩ .                                             (1)

Here 𝛼 and 𝛽                 numbers such that, |𝛼 | 2 + |𝛽 | 2 = 1. In the ket-notation or the Dirac
                are complex  
                 1               0
notation, |0⟩ =      and |1⟩ =      are shorthands for the vectors encoding the two basis states of a
                 0               1
two dimensional vector space. So according to this notation,
                                                                Eq. (1) expresses the fact that the state
                                                         𝛼
of the qubit is the two dimensional complex vector          . Unlike a classical bit the state of a qubit
                                                         𝛽
cannot be measured without changing it. Measuring a qubit, whose state given by Eq. (1), will yield
the classical value of either zero (|0⟩) with probability |𝛼 | 2 or one (|1⟩) with probability |𝛽 | 2 . Qubit
Quantum Algorithm Implementations for Beginners                                                             5


implementations and technologies are a very active area of research that is not the focus of our
review, an interested reader is referred to [80] for a survey.
1.1.2 System of qubits. The mathematical structure of a qubit generalizes to higher dimensional
quantum systems as well. The state of any quantum system is a normalized vector (a vector of norm
one) in a complex vector space. The normalization is necessary to ensure that the total probability
of all the outcomes of a measurement sum to one.
   A quantum computer contains many number of qubits. So it is necessary to know how to
construct the combined state of a system of qubits given the states of the individual qubits. The
joint state of a system of qubits is described using an operation known as the tensor product, ⊗.
Mathematically, taking the tensor product of two states is the same as taking
                                                                            the Kronecker
                                                                                          ′product
                                                                                            
                                                                            𝛼        ′    𝛼
of their corresponding vectors. Say we have two single qubit states |𝜙⟩ =      and |𝜙 ⟩ = ′ . Then
                                                                            𝛽             𝛽
the full state of a system composed of two independent qubits is given by,
                                                                    ′
                                                    ′  ©𝛼𝛼 ′ ª
                                                  𝛼      𝛼    ­𝛼𝛽 ®
                                  |𝜙⟩ ⊗ |𝜙 ′⟩ =      ⊗ ′ = ­ ′®                                           (2)
                                                  𝛽      𝛽    ­𝛽𝛼 ®
                                                                    ′
                                                              « 𝛽𝛽 ¬
Sometimes the ⊗ symbol is dropped all together while denoting the tensor product to reduce clutter.
Instead the states are written inside a single ket. For example, |𝜙⟩ ⊗ |𝜙 ′⟩ is shortened to |𝜙𝜙 ′⟩, and
|0⟩ ⊗ |0⟩ ⊗ |0⟩ is shortened to |000⟩ . For larger systems the Dirac notation gives a more succinct
way to compute the tensor product using the distributive property of the Kronecker product. For a
system of, say, three qubits with each qubit in the state 𝛾 𝑗 = 𝛼 𝑗 |0⟩ + 𝛽 𝑗 |1⟩, for 𝑗 = 1, 2, 3, the joint
state is,
                |𝛾 1𝛾 2𝛾 3 ⟩ = |𝛾 1 ⟩ ⊗ |𝛾 2 ⟩ ⊗ |𝛾 3 ⟩                                                    (3)
                           = 𝛼 1𝛼 2𝛼 3 |000⟩ + 𝛼 1𝛼 2 𝛽 3 |001⟩ + 𝛼 1 𝛽 2𝛼 3 |010⟩ + 𝛼 1 𝛽 2 𝛽 3 |011⟩
                             + 𝛽 1𝛼 2𝛼 3 |100⟩ + 𝛽 1𝛼 2 𝛽 3 |101⟩ + 𝛽 1 𝛽 2𝛼 3 |110⟩ + 𝛽 1 𝛽 2 𝛽 3 |111⟩   (4)
A measurement of all three qubits could result in any of the eight (23 ) possible bit-strings associated
with the eight basis vectors. One can see from these examples that the dimension of the state space
grows exponentially in the number of qubits 𝑛 and that the number of basis vectors is 2𝑛 .
1.1.3 Superposition and entanglement. Superposition refers to the fact that any linear combination
of two quantum states, once normalized, will also be a valid quantum state. The upshot to this is
that any quantum state can be expressed as a linear combination of a few basis states. For example,
we saw in Eq. (1) that any state of a qubit can be expressed as a linear combination of |0⟩ and |1⟩.
Similarly, the state of any 𝑛 qubit system can be written as a normalized linear combination of the
2𝑛 bit-string states (states formed by the tensor products of |0⟩’s and |1⟩’s). The orthonormal basis
formed by the 2𝑛 bit-string states is called the computational basis.
   Notice that Eq. (3) described a system of three qubits whose complete state was the tensor product
of three different single qubit states. But it is possible for three qubits to be in a state that cannot
be written as the tensor product of three single qubit states. An example of such a state is,
                                               1
                                       |𝜓 ⟩ = √ (|000⟩ + |111⟩).                                      (5)
                                                2
States of a system of which cannot be expressed as a tensor product of states of its individual
subsystems are called entangled states. For a system of 𝑛 qubits, this means that an entalged state
cannot be written a tensor product of 𝑛 single qubit states. The existence of entangled states is a
6                                                                                          Abhijith J., et al.


physical fact that has important consequences for quantum computing, and quantum information
processing in general. In fact, without the existence of such states quantum computers would be
no more powerful than their classical counterparts [128]. Entanglement makes it possible to create
a complete 2𝑛 dimensional complex vector space to do our computations in, using just 𝑛 physical
qubits.
1.1.4 Inner and outer products. We will now discuss some linear algebraic notions necessary for
understanding quantum algorithms. First of these is the inner product or overlap between two
quantum states. As we have seen before, quantum states are vectors in complex vectors spaces. The
overlap between two states is just the inner product between these complex vectors. For example,
take two single qubit states, |𝜙⟩ = 𝛼 |0⟩ + 𝛽 |1⟩ and |𝜓 ⟩ = 𝛾 |0⟩ + 𝛿 |1⟩ . The overlap between these
states is denoted in the ket notation as ⟨𝜓 |𝜙⟩. And this is given by,
                                           ⟨𝜓 |𝜙⟩ = 𝛾 ∗𝛼 + 𝛿 ∗ 𝛽,                                         (6)
where ∗ denotes the complex conjugate. Notice that,⟨𝜓 |𝜙⟩ = ⟨𝜙 |𝜓 ⟩ ∗ . The overlap of two states
is in general a complex number. The overlap of a state with a bit-string state will produce the
corresponding coefficient. For instance from Eq. (1), ⟨0|𝜙⟩ = 𝛼 and ⟨1|𝜙⟩ = 𝛽. And from Eq. (3),
⟨001|𝛾 1𝛾 2𝛾 3 ⟩ = 𝛼 1𝛼 2 𝛽 3 . Another way to look at overlaps between quantum states is by defining
what is called a bra state. The states we have seen so far are ket states, like |𝜙⟩, which represented
column vectors. A bra state corresponding to this ketstate,   written as ⟨𝜙 |, represents a row vector
                                                            𝛼
                                                                implies that ⟨𝜙 | = 𝛼 ∗ 𝛽 ∗ . The overlap
                                                                                           
with complex conjugated entries. For instance |𝜙⟩ =
                                                            𝛽
of two states is then the matrix product of a row vector with a column vector, yielding a single
number. The reader must have already noticed the wordplay here. The overlap, with its closing
angled parenthesis, form a ‘bra-ket’!
   The outer product of two states is an important operation that outputs a matrix given two states.
The outer product of the two states we defined above will be denoted by, |𝜓 ⟩⟨𝜙 |. Mathematically
the outer product of two states is a matrix obtained by multiplying the column vector of the first
state with the complex conjugated row vector of the second state (notice how the ket is written
before the bra to signify this). For example,
                                                                ∗
                                                                𝛼𝛾 𝛼𝛿 ∗
                                                                        
                                                  𝛼
                                                     𝛾∗ 𝛿∗ =
                                                          
                                     |𝜓 ⟩ ⟨𝜙 | =                                                       (7)
                                                  𝛽             𝛽𝛾 ∗ 𝛽𝛿 ∗
In this notation any matrix can be written as a linear combination of outer products between
bit-string states. For a 2 × 2 matrix,
                               
                      𝐴00 𝐴01
                𝐴=                = 𝐴00 |0⟩ ⟨0| + 𝐴01 |0⟩ ⟨1| + 𝐴10 |1⟩ ⟨0| + 𝐴11 |1⟩ ⟨1| . (8)
                      𝐴10 𝐴11
Acting on a state with a matrix then becomes just an exercise in computing overlaps between states.
Let us demonstrate this process:
                𝐴 |𝜙⟩ = 𝐴00 |0⟩ ⟨0|𝜙⟩ + 𝐴01 |0⟩ ⟨1|𝜙⟩ + 𝐴10 |1⟩ ⟨0|𝜙⟩ + 𝐴11 |1⟩ ⟨1|𝜙⟩ ,
                                                                                  
                                                                      𝐴00𝛼 + 𝐴01 𝛽
                      = (𝐴00𝛼 + 𝐴01 𝛽) |0⟩ + (𝐴10𝛼 + 𝐴11 𝛽) |1⟩ =                    .                    (9)
                                                                      𝐴10𝛼 + 𝐴11 𝛽
This notation might look tedious at first glance but it makes algebraic manipulations of quantum
states easily understandable. This is especially true when we are dealing with large number of
qubits as otherwise we would have to explicitly write down exponentially large matrices.
   The outer product notation for matrices also gives an intuitive input-output relation for them.
For instance, the matrix |0⟩ ⟨1| + |1⟩ ⟨0| can be read as "output 0 when given a 1 and output 1 when
Quantum Algorithm Implementations for Beginners                                                        7


given a 0". Likewise,the matrix, |00⟩ ⟨00| + |01⟩ ⟨01| + |10⟩ ⟨11| + |11⟩ ⟨10| can be interpreted as the
mapping {"00" –> "00", "01" –> "01", "11" –> "10", "10" –> "11" }. But notice that this picture becomes
a bit tedious when the input is in a superposition. In that case the correct output can be computed
like in Eq. (9).
1.1.5 Measurements. Measurement corresponds to transforming the quantum information (stored
in a quantum system) into classical information. For example, measuring a qubit typically corre-
sponds to reading out a classical bit, i.e., whether the qubit is 0 or 1. A central principle of quantum
mechanics is that measurement outcomes are probabilistic.
   Using the aforementioned notation for inner products, for the single qubit state in Eq. (1), the
probability of obtaining |0⟩ after measurement is | ⟨0|𝜙⟩ | 2 and the probability of obtaining |1⟩
after measurement is | ⟨1|𝜙⟩ | 2 . So measurement probabilities can be represented as the squared
absolute values of overlaps. Generalizing this, the probability of getting the bit string |𝑥 1 . . . 𝑥𝑛 ⟩
after measuring an 𝑛 qubit state, |𝜙⟩, is then | ⟨𝑥 1 . . . 𝑥𝑛 |𝜙⟩ | 2 .
   Now consider a slightly more complex case of measurement. Suppose we have a three qubit
state, |𝜓 ⟩ but we only measure the first qubit and leave the other two qubits undisturbed. What is
the probability of observing a |0⟩ in the first qubit? This probability will be given by,
                                             ∑︁
                                                    | ⟨0𝑥 2𝑥 3 |𝜙⟩ | 2 .                             (10)
                                          (𝑥 2 𝑥 3 ) ∈ {0,1}2

The state of the system after this measurement will be obtained by normalizing the state,
                                      ∑︁
                                            ⟨0𝑥 2𝑥 3 |𝜙⟩ |0𝑥 2𝑥 3 ⟩ .                               (11)
                                      (𝑥 2 𝑥 3 ) ∈ {0,1}2

Applying this paradigm to the state in Eq. (5) we see that the probability of getting |0⟩ in the first
qubit will be 0.5, and if this result is obtained, the final state of the system would change to |000⟩ .
On the other hand, if we were to measure |1⟩ in the first qubit we would end up with a state |111⟩ .
Similarly we can compute the effect of subsystem measurements on any 𝑛 qubit state.
  In some cases we will need to do measurements on a basis different from the computational
basis. This can be achieved by doing an appropriate transformation on the qubit register before
measurement. Details of how to do this is given in a subsequent section discussing observables and
expectation values.
  The formalism discussed so far is sufficient to understand all measurement scenarios in this paper.
We refer the reader to Ref. [92] for a more detailed and more general treatment of measurement.
1.1.6 Unitary transformations and gates. A qubit or a system of qubits changes its state by going
through a series of unitary transformations. A unitary transformation is described by a matrix 𝑈
with complex entries. The matrix 𝑈 is called unitary if
                                                𝑈 𝑈 † = 𝑈 †𝑈 = 𝐼,                                   (12)
where 𝑈 † is the transposed, complex conjugate of 𝑈 (called its Hermitian conjugate) and 𝐼 is the
identity matrix. A qubit state |𝜙⟩ = 𝛼 |0⟩ + 𝛽 |1⟩ evolves under the action of the 2 × 2 matrix 𝑈
according to
                                                                      
                                         𝑈 00 𝑈 01 𝛼        𝑈 00𝛼 + 𝑈 01 𝛽
                        |𝜙⟩ → 𝑈 |𝜙⟩ =                   =                    .                (13)
                                         𝑈 10 𝑈 11 𝛽        𝑈 10𝛼 + 𝑈 11 𝛽
Operators acting on different qubits can be combined using the Kronecker product. For example, if
𝑈 1 and 𝑈 2 are operators acting on two different qubits then the full operator acting on the combined
two qubit system will be given by 𝑈 1 ⊗ 𝑈 2 .
8                                                                                             Abhijith J., et al.


   For an 𝑛 qubit system the set of physically allowed transformations, excluding measurements,
consists of all 2𝑛 × 2𝑛 unitary matrices. Notice that the size of a general transformation increases
exponentially with the number of qubits. In practice a transformation on 𝑛 qubits is effected by
using a combination of unitary transformations that act only on one or two qubits at a time. By
analogy to classical logic gates like NOT and AND, such basic unitary transformations, which
are used to build up more complicated 𝑛 qubit transformations, are called gates. Gates are unitary
transformations themselves and from Eq. (12) it is clear that unitarity can only be satisfied if the
number of input qubits is equal to the number of output qubits. Also, for every gate 𝑈 it is always
possible to have another gate 𝑈 † that undoes the transformation. So unlike classical gates quantum
gates have to be reversible. Reversible means that the gate’s inputs can always be reconstructed
from the gate’s outputs. For instance, a classical NOT gate, which maps 0 to 1 and 1 to 0 is reversible
because an output of 1 implies the input was 0 and vice versa. However, a classical AND gate,
which returns 1 if and only if both of its inputs are 1, is not reversible. An output of 1 implies that
both inputs were 1, but an output of 0 provides insufficient information to determine if the inputs
were 00, 01, or 10.
   But this extra restriction of reversibility does not mean that quantum gates are ‘less powerful’
than classical gates. Even classical gates can be made reversible with minimal overhead. Reversibility
does not restrict their expressive power [105]. Quantum gates can then be seen as a generalization
of classical reversible gates.
   The most common gates are described in Table 1. The 𝑋 gate is the quantum version of the NOT
gate. The CNOT or “controlled NOT” negates a target bit if and only if the control bit is 1. We will
use the notation CNOT𝑖 𝑗 for a CNOT gate controlled by qubit 𝑖 acting on qubit 𝑗. The CNOT gate
can be expressed using the outer product notation as,
           CNOT = |0⟩ ⟨0| ⊗ 𝐼 + |1⟩ ⟨1| ⊗ 𝑋 = |00⟩ ⟨00| + |01⟩ ⟨01| + |10⟩ ⟨11| + |11⟩ ⟨10| .              (14)
   The Toffoli gate or “controlled-controlled NOT” or CCNOT, is a three qubit gate that is essentially
the quantum (reversible) version of the AND gate. It negates a target bit if and only if both control
bits are 1. In the outer product notation,
                             CCNOT = |11⟩ ⟨11| ⊗ 𝑋 + (𝐼 − |11⟩ ⟨11|) ⊗ 𝐼 .                                 (15)
    Another way to look at the CCNOT gate is as a CNOT gate with an additional control qubit,

                               CCNOT = |0⟩ ⟨0| ⊗ 𝐼 + |1⟩ ⟨1| ⊗ CNOT.                                       (16)
    In general, one can define controlled versions of any unitary gate 𝑈 as,
                                     𝐶𝑈 = |0⟩ ⟨0| ⊗ 𝐼 + |1⟩ ⟨1| ⊗ 𝑈 .                                      (17)
𝐶𝑈 applies 𝑈 to a set of qubits only if the first qubit (called the control qubit) is |1⟩.
  A set of gates that together can execute all possible quantum computations is called a universal
gate set. Taken together, the set of all unary (i.e., acting on one qubit) gates and the binary (i.e., acting
on two qubits) CNOT gate form a universal gate set. More economically, the set {𝐻,𝑇 , CNOT}
(Refer Table 1 for definitions of these gates) forms a universal set. Also, the Toffoli gate by itself is
universal [92].
1.1.7 Observables and expectation values. We have seen that experiments in quantum mechanics
are probabilistic. Often in experiments we will need to associate a real number with a measurement
outcome. And quantities that we measure in quantum mechanics will always be statistical averages
of these numbers. For instance, suppose we do the following experiment on many copies of the
single qubit state in Eq. (1): We measure a copy of the state and if we get |0⟩ we record 1 in our lab
notebook , otherwise we record −1. While doing this experiment we can never predict the outcome
Quantum Algorithm Implementations for Beginners                                                                                                             9


                               One-qubit gates                                                         Multi-qubit gates


                                                                                                          1              0       0       0
                                                            1           1                                 ­ 0              1       0       0 ®
                                                                                                          ©                                  ª
                Hadamard = 𝐻 = √1                                                             CNOT = 𝐶𝑋 = ­
                                                            1           −1                                ­ 0              0       0       1 ®
                                                                                                                                             ®
                                                2
                                                                                                          « 0              0       1       0 ¬



                                                                                                     1     0       0        0
                           1      0                         1           0                              ­ 0     1       0        0 ®
                                                                                                       ©                          ª
                 𝐼=                       , 𝑆=                                                    𝐶𝑍 = ­
                           0      1                         0                                          ­ 0     0       1        0 ®
                                                                                                                                  ®
                                                                        𝑖
                                                                                                       « 0     0       0       −1 ¬



                                                                                                           1             0        0            0
                                      1         0                                                          ­ 0             1        0            0 ®
                                                                                                           ©                                         ª
                           𝑇 =                                                         Controlled-𝑈 = 𝐶𝑈 = ­
                                      0     𝑒 𝑖𝜋 /4                                                        ­ 0             0
                                                                                                                                                     ®
                                                                                                                                   𝑈 00         𝑈 01 ®
                                                                                                           « 0             0       𝑈 10         𝑈 11 ¬



                                                                                                         1       0       0       0
                                                0           1                                            ­ 0       0       1       0 ®
                                                                                                         ©                           ª
                          NOT = 𝑋 =                                                               SWAP = ­
                                                1           0                                            ­ 0       1       0       0 ®
                                                                                                                                     ®

                                                                                                         « 0       0       0       1 ¬


                                                                                                    1     0    0       0       0       0    0     0
                                                                                                  © 0     1    0       0       0       0    0     0 ª®
                                                                                                  ­
                                                                                                  ­ 0     0    1       0       0       0    0     0 ®®
                                                                                              ­
                           0     −𝑖                         1            0                        ­ 0     0    0       1       0       0    0     0 ®
                                                                                                  ­                                                  ®
                𝑌 =                       ,𝑍 =                                          Toffoli = ­
                                 0                          0           −1                        ­ 0     0    0       0       1       0    0     0 ®
                                                                                                                                                     ®
                           𝑖                                                           (CCNOT)
                                                                                                  ­ 0     0    0       0       0       1    0     0 ®
                                                                                                  ­                                                  ®
                                                                                                  ­                                                  ®
                                                                                                  ­ 0     0    0       0       0       0    0     1 ®
                                                                                                  « 0     0    0       0       0       0    1     0 ¬


                                                                        
                                                    1           0
                  𝑅 (𝜃 ) = 𝑃 (𝜃 ) =
                                                    0       𝑒 𝑖𝜃

                                            Table 1. Commonly used quantum gates.



of a specific measurement. But we can ask statistical questions like: “What will be the average
value of the numbers in the notebook?” From our earlier discussion on measurement we know that
the probability of measuring |0⟩ is |𝛼 | 2 and the probability of measuring |1⟩ is |𝛽 | 2 . So the average
value of the numbers in the notebook will be,
                                                                                     |𝛼 | 2 − |𝛽 | 2                                                     (18)
In quantum formalism, there is neat way to express such experiments and their average outcomes,
without all the verbiage, using certain operators. For the experiment described above the associated
operator would be the 𝑍 gate,
                                                                 
                                                            1 0
                                  𝑍 = |0⟩ ⟨0| − |1⟩ ⟨1| =                                       (19)
                                                            0 −1
10                                                                                     Abhijith J., et al.


By associating this operator with the experiment we can write the average outcome of the experi-
ment, on |𝜙⟩, as the overlap between |𝜙⟩ and 𝑍 |𝜙⟩,
                         ⟨𝜙 |𝑍 |𝜙⟩ = ⟨𝜙 |0⟩ ⟨0|𝜙⟩ − ⟨𝜙 |1⟩ ⟨1|𝜙⟩ = |𝛼 | 2 − |𝛽 | 2 .                (20)
The operator 𝑍 is called the observable associated with this experiment. And the quantity ⟨𝜙 |𝑍 |𝜙⟩
is called its expectation value. The expectation value is sometimes denoted by ⟨𝑍 ⟩, when there is no
ambiguity about the state on which the experiment is performed.
   Here we saw an experiment done in the computational basis. But this need not always be the
case. Experiments can be designed by associating real numbers to measurement outcomes in any
basis. What would be the observable for such an experiment? For an experiment that associates
the real numbers {𝑎𝑖 } to a measurement onto a basis set {|Φ𝑖 ⟩}, the observable will be,
                                               ∑︁
                                         𝑂≡       𝑎𝑖 |Φ𝑖 ⟩ ⟨Φ𝑖 | .                               (21)
                                                   𝑖

This observable will reproduce the correct expectation value for this experiment done on any state
|𝜓 ⟩,
                                      ∑︁                        ∑︁
                         ⟨𝜓 |𝑂 |𝜓 ⟩ =    𝑎𝑖 ⟨𝜓 |Φ𝑖 ⟩ ⟨Φ𝑖 |𝜓 ⟩ =    𝑎𝑖 | ⟨Φ𝑖 |𝜓 ⟩ | 2 .        (22)
                                       𝑖                          𝑖

Because the states {|Φ𝑖 ⟩} are orthonormal, we can see that 𝑂 obeys the following eigenvalue
equation,
                                      ∑︁
                              𝑂 Φ𝑗 =     𝑎𝑖 |Φ𝑖 ⟩ Φ𝑖 |Φ 𝑗 = 𝑎 𝑗 Φ 𝑗 .                   (23)
                                           𝑖
So 𝑂 is an operator that has complete set of orthogonal eigenvectors and real eigenvalues. Such
operators are called Hermitian operators. Equivalently, these operators are equal to their Hermitian
conjugates (𝑂 = 𝑂 † ). In quantum mechanics, any Hermitian operator is a valid observable. The
eigenvectors of the operator give the possible outcomes of the experiment and the corresponding
eigenvalues are the real numbers associated with that outcome.
   But can all valid observables be measured in practice? The answer to this depends on the quantum
system under consideration. In this tutorial, the system under consideration is an IBM quantum
processor. And in these processors only measurements onto the computational basis are supported
natively. Measurements to other basis states can be performed by applying an appropriate unitary
transformation before measurement. Suppose that the hardware only lets us do measurements onto
the computational basis {|𝑖⟩} but we want to perform a measurement onto the basis set {|Φ𝑖 ⟩}.
This problem can be solved if we can implement the following unitary transformation,
                                               ∑︁
                                          𝑈 =      |𝑖⟩ ⟨Φ𝑖 | .                                  (24)
                                                       𝑖

Now measuring 𝑈 |𝜓 ⟩ in the computational basis is the same as measuring |𝜓 ⟩ in the {|Φ𝑖 ⟩} basis.
This can be seen by computing the outcome probabilities on 𝑈 |𝜓 ⟩,
                                              ∑︁
                         | ⟨𝑗 |𝑈 |𝜓 ⟩ | 2 = |    ⟨𝑗 |𝑖⟩ ⟨Φ𝑖 |𝜓 ⟩ | 2 = | Φ 𝑗 |𝜓 | 2 .         (25)
                                               𝑖

So once 𝑈 is applied, the outcome | 𝑗⟩ becomes equivalent to the outcome Φ 𝑗 in the original
measurement scenario. Now, not all such unitary transformations are easy to implement. So if
a quantum algorithm requires us to perform a measurement onto some complicated set of basis
states, then the cost of implementing the corresponding 𝑈 has be taken into account.
Quantum Algorithm Implementations for Beginners                                                     11


1.1.8 Quantum circuits. Quantum algorithms are often diagrammatically represented as circuits
in literature. Here we will describe how to construct and read quantum circuits. In the circuit
representation, qubits are represented by horizontal lines. Gates are then drawn on the qubits they
act on. This is done in sequence from left to right. The initial state of the qubit is denoted at the
beginning of each of the qubit lines. Notice that when we write down a mathematical expression
for the circuit, the gates are written down from right to left in the order of their application.
   These principles are best illustrated by an example. Given in Fig. 1 is a circuit to preparing an
entangled two qubit state called a Bell state from |00⟩.


                                      |0⟩         𝐻      •


                                      |0⟩

                             Fig. 1. Quantum circuit for preparing a Bell state


  The circuit encodes the equation,
                                                         1
                               CNOT12 (𝐻 ⊗ 𝐼 ) |00⟩ = √ (|00⟩ + |11⟩).
                                                          2
Let us now carefully go over how the circuit produces the Bell state. We read the circuit from left
to right. The qubits are numerically labelled starting from the top. First the 𝐻 gate acts on the top
most qubit changing the state of the system to,
                                                            
                                                   |0⟩ + |1⟩            1
                𝐻 ⊗ 𝐼 |00⟩ = (𝐻 |0⟩) ⊗ (𝐼 |0⟩) =      √        ⊗ |0⟩ = √ (|00⟩ + |10⟩).
                                                        2                2
Then CNOT12 acts on both of these qubits. The blackened dot on the first qubit implies that this
qubit is the control qubit for the CNOT. The ⊕ symbol on the second qubit implies that this qubit is
the target of the NOT gate (controlled by the state of the first qubit). The action of the CNOT then
gives,
                                   
                    1                   1                                      1
        CNOT12 √ (|00⟩ + |10⟩) = √ (CNOT12 |00⟩ + CNOT12 |10⟩) = √ (|00⟩ + |11⟩).
                     2                   2                                      2
The measurement of a qubit is also denoted by a special gate with a meter symbol on it, given in Fig 2.
The presence of this gate on a qubit means that the qubit must be measured in the computational
basis.




                                       Fig. 2. The measurement gate


1.1.9 Quantum algorithms. We have now introduced all the basic elements needed for the discus-
sion of practical quantum algorithms. A quantum algorithm consists of three basic steps:
     • Encoding of the data, which could be classical or quantum, into the state of a set of input
       qubits.
     • A sequence of quantum gates applied to this set of input qubits.
12                                                                                                 Abhijith J., et al.


    • Measurements of one or more of the qubits at the end to obtain a classically interpretable
       result.
   In this review, we will describe the implementation of these three steps for a variety of quantum
algorithms.

1.2   Implementations on a real quantum computer
1.2.1 The IBM quantum computer. In this article, we consider IBM’s publicly available quantum
computers. In most cases, we specifically consider the ibmqx4, which is a 5-qubit computer, although
in some cases we also consider other quantum processors freely accessible through the IBM
Quantum Experience platform. These processors can be accessed by visiting the IBM Quantum
Experience website (https://quantum-computing.ibm.com/)
   There are several issues to consider when implementing an algorithm on real quantum computers,
for example:
   (1) What is the available gate set with which the user can state their algorithm?
   (2) What physical gates are actually implemented?
   (3) What is the qubit connectivity (i.e., which pairs of qubits can two-qubit gates be applied to)?
   (4) What are the sources of noise (i.e., errors)?
   We first discuss the available gate set. In IBM’s graphical interface to the ibmqx4, the available
gates include:
                     {𝐼, 𝑋, 𝑌 , 𝑍, 𝐻, 𝑆, 𝑆 †,𝑇 ,𝑇 †, 𝑈 1 (𝜆), 𝑈 2 (𝜆, 𝜙), 𝑈 3 (𝜆, 𝜙, 𝜃 ), CNOT}.                (26)
The Graphical User Interface (GUI) also provides other controlled gates and operations like measure-
ment and reset. Most of these gates appear in our Table 1. The gates 𝑈 1 (𝜆), 𝑈 2 (𝜆, 𝜙), and 𝑈 3 (𝜆, 𝜙, 𝜃 )
are continuously parameterized gates, defined as follows:
                                                                                                           
            1 0                      1 1       −𝑒 𝑖𝜆                            cos(𝜃 /2)     −𝑒 𝑖𝜆 sin(𝜃 /2)
𝑈 1 (𝜆) =            , 𝑈 2 (𝜆, 𝜙) = √     𝑖𝜙 𝑒 𝑖 (𝜆+𝜙)   , 𝑈 3 (𝜆, 𝜙, 𝜃 ) =                                       .
            0 𝑒 𝑖𝜆                    2 𝑒                                    𝑒 𝑖𝜙 sin(𝜃 /2) 𝑒 𝑖 (𝜆+𝜙) cos(𝜃 /2)
                                                                                                          (27)
Note that 𝑈 3 (𝜆, 𝜙, 𝜃 ) is essentially an arbitrary one-qubit gate.
   The gates listed in Eq. (26) are provided by IBM for the user’s convenience. However these are
not the gates that are physically implemented by their quantum computer. IBM has a compiler that
translates the gates in (26) into products of gates from a physical gate set. The physical gate set
employed by IBM is essentially composed of three gates [1]:
                                          {𝑈 1 (𝜆), 𝑅𝑋 (𝜋/2), CNOT} .                                           (28)
Here, 𝑅𝑋 (𝜋/2) is a rotation by angle 𝜋/2 of the qubit about it’s 𝑋 -axis, corresponding to a matrix
similar to the Hadamard:
                                                             
                                                   1 1 −𝑖
                                    𝑅𝑋 (𝜋/2) = √                .                                (29)
                                                    2 −𝑖 1
The reason why it could be important to know the physical gate set is that some user-programmed
gates may need to be decomposed into multiple physical gates, and hence could lead to a longer
physical algorithm. For example, the 𝑋 gate gets decomposed into three gates: two 𝑅𝑋 (𝜋/2) gates
sandwiching one 𝑈 1 (𝜆) gate.
  The connectivity of the computer is another important issue. Textbook algorithms are typically
written for a fully-connected hardware, which means that one can apply a two-qubit gate to any
two qubits. In practice, real quantum computers may not have full connectivity. In the ibmqx4,
which has 5 qubits, there are 6 connections, i.e., there are only 6 pairs of qubits to which a CNOT
Quantum Algorithm Implementations for Beginners                                                           13


                                                     1


                                           0         2          3


                                                     4

Fig. 3. The connectivity diagram of ibmqx4. The circles represent qubits and the arrows represent the ability
to apply a physical CNOT gate between the qubits.


gate can be applied (Fig.3). In contrast a fully connected 5-qubit system would allow a CNOT to be
applied to 20 different qubit pairs. In this sense, there are 14 “missing connections”. Fortunately,
there are ways to effectively generate connections through clever gate sequences. For example, a
CNOT gate with qubit 𝑗 as the control and qubit 𝑘 as the target can be reversed (such that 𝑗 is the
target and 𝑘 is the control) by applying Hadamard gates on each qubit both before and after the
CNOT, i.e.,
                                 CNOT𝑘 𝑗 = (𝐻 ⊗ 𝐻 )CNOT 𝑗𝑘 (𝐻 ⊗ 𝐻 ) .                                   (30)
Similarly, there exists a gate sequence to make a CNOT between qubits 𝑗 and 𝑙 if one has connections
between 𝑗 and 𝑘, and 𝑘 and 𝑙, as follows:
                             CNOT 𝑗𝑙 = CNOT𝑘𝑙 CNOT 𝑗𝑘 CNOT𝑘𝑙 CNOT 𝑗𝑘 .                                  (31)
Hence, using (30) and (31), one can make up for lack of connectivity at the expense of using extra
gates.
   Finally, when implementing a quantum algorithm it is important to consider the sources of noise
in the computer. The two main sources of noise are typically gate infidelity and decoherence. Gate
infidelity refers to the fact that the user-specified gates do not precisely correspond to the physically
implemented gates. Gate infidelity is usually worse for multi-qubit gates than for one-qubit gates, so
typically one wants to minimize the number of multi-qubit gates in one’s algorithm. Decoherence
refers to the fact that gradually over time the quantum computer loses its “quantumness” and
behaves more like a classical object. After decoherence has fully occurred, the computer can
no longer take advantage of quantum effects. This introduces progressively more noise as the
quantum algorithm proceeds in time. Ultimately this limits the depth of quantum algorithms that
can be implemented on quantum computers. It is worth noting that different qubits decohere at
different rates, and one can use this information to better design one’s algorithm. The error rates
for individual qubits in the IBM processors are listed in the IBM Quantum Experience website.
In this tutorial, we will show in many cases how infidelity and decoherence affect the algorithm
performance in practice.
   A simple example of programming the IBM quantum computer is given in Fig. 4, which shows
the Bell state preparation circuit Fig.1 compiled using the IBM quantum experience GUI. Extra
measurement operations at the end serve to verify the fidelity of the implementation.
1.2.2 Programming the IBM quantum computer: Qiskit library. Qiskit [4] is an open-source quantum
computing library developed under the aegis of IBM. Qiskit allows users to write and run programs
on either IBM’s quantum processors or on a local simulator, without the use of the graphical
interface. This is an important feature because the graphical interface becomes impractical as
the number qubits become large. At the time of writing, users can use Qiskit to access quantum
14                                                                                           Abhijith J., et al.




     Fig. 4. The quantum circuit to prepare a Bell state and measure it in the IBM quantum experience GUI




processors with up to 16 qubits. Smaller processors are also accessible. Qiskit is a very powerful
software development kit (SDK) which has multiple elements in it that tackle a variety of problems
associated with practical quantum computing. Qiskit is further split into four modules called:
Terra, Aer, Aqua, and Ignis. Each of these modules deal with a specific part of quantum software
development. In this section we will only give a brief overview of programming simple quantum
circuits with Qiskit. For a comprehensive overview of Qiskit and its various capabilities, the reader
is encouraged to visit the official website ( www.qiskit.org ) [4].
   For our purposes, Qiskit can be viewed as a Python library for quantum circuit execution. A
basic Qiskit code has two parts, designing the circuit and running it. In the circuit design phase, we
create an instance of QuantumCircuit with the required number of qubits and classical bits. Then
gates and measurements are added to this blank circuit. Gates and measurements are implemented
in Qiskit as methods of the QuantumCircuit class. After the circuit has been designed we need to
choose a backend to run the circuit. This can be either be a simulator called the qasm_simulator
or it can be one of IBM’s quantum processors. To use a quantum processor, you will need to load
your IBM Q account information into Qiskit. Given in Fig. 5 is a simple code to construct the Bell
state. This is the Qiskit version of the circuit in Fig. 1 with measurement added at the end to verify
our results.
Quantum Algorithm Implementations for Beginners                                                   15


### Quantum circuit for preparing the Bell state ####

import numpy as np
from qiskit import QuantumCircuit, execute, Aer

# Create a Quantum Circuit with two qbits and 2 classical bits
circuit = QuantumCircuit(2,2)

# Add a H gate on qubit 0
circuit.h(0)

# Add a CX (CNOT) gate on control qubit 0 and target qubit 1
circuit.cx(0,1)

# Map the quantum measurement to the classical bits
circuit.measure([0,1],[0,1])


# Use Aer's qasm_simulator
simulator = Aer.get_backend('qasm_simulator')

# Execute the circuit on the qasm simulator
job = execute(circuit, simulator, shots=1000)

# Grab results from the job
result = job.result()

# Returns counts
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:",counts)

               Fig. 5. Qiskit code to create and measure a Bell state. Source: www.qiskit.org




   In Fig.5 we are running the circuit on the simulator for 1000 independent runs. The final output
was {'11': 493, '00': 507}. This is what we expect from measuring the Bell state ( |00⟩+|11⟩
                                                                                        √    ), up to
                                                                                         2
statistical fluctuations. While running the same code on the 14 qubit ibmq_16_melbourne processor
for 1024 runs gave |11⟩ with probability 0.358 and |00⟩ with probability 0.54. The remaining
probability was distributed over 01 and 10, which should not be a part of the Bell state. As we
discussed before, this phenomenon is due to errors inherent to the quantum processor. As the
backend technology improves we expect to get better results from these trials. Often, we will also
present a circuit using OpenQASM (Open Quantum Assembly Language). OpenQASM provides
an intermediate representation of a program in the form of a quantum circuit, that is neither the
actual program written by the programmer nor the machine instructions seen by the processor.
OpenQASM ‘scores’ we show in this paper will be simple sequence of gates and measurements, with
the corresponding registers that they act on. The syntax of these scores will be self explanatory.
16                                                                                                        Abhijith J., et al.


 Class                           Problem/Algorithm                            Paradigms used   Hardware   Simulation Match
 Inverse Function Computation    Grover’s Algorithm                           GO               QX4        med
                                 Bernstein-Vazirani                           n.a.             QX4, QX5   high
 Number-theoretic Applications   Shor’s Factoring Algorithm                   QFT              QX4        med
 Algebraic Applications          Linear Systems                               HHL              QX4        low
                                 Matrix Element Group Representations         QFT              ESSEX      low
                                 Matrix Product Verification                  GO               n.a.       n.a.
                                 Subgroup Isomorphism                         QFT              none       n.a.
 Graph Applications              Quantum Random Walk                          n.a.             VIGO       med-low
                                 Minimum Spanning Tree                        GO               QX4        med-low
                                 Maximum Flow                                 GO               QX4        med-low
                                 Approximate Quantum Algorithms               SIM              QX4        high
 Learning Applications           Quantum Principal Component Analysis (PCA)   QFT              QX4        med
                                 Quantum Support Vector Machines (SVM)        QFT              none       n.a.
                                 Partition Function                           QFT              QX4        med-low
 Quantum Simulation              Schrödinger Equation Simulation              SIM              QX4        low
                                 Transverse Ising Model Simulation            VQE              none       n.a.
 Quantum Utilities               State Preparation                            n.a.             QX4        med
                                 Quantum Tomography                           n.a.             QX4        med
                                 Quantum Error Correction                     n.a.             QX4        med
Table 2. Overview of studied quantum algorithms. Paradigms include Grover Operator (GO), Quantum
Fourier Transform (QFT), Harrow-Hassidim-Lloyd (HHL), Variational Quantum Eigenvalue solver (VQE),
and direct Hamiltonian simulation (SIM). The simulation match column indicates how well the hardware
quantum results matched the simulator results



1.3      Classes of quantum algorithms
In this review, we broadly classify quantum algorithms according to their area of application. We
will discuss quantum algorithms for graph theory, number theory, machine learning and so on. The
complete list of algorithms discussed in this paper, classified according to their application areas,
can be found in Table 2. The reader is also encouraged to take a look at the excellent Quantum
Algorithm Zoo website [72] for a concise and comprehensive list of quantum algorithms.
   In classical computing, algorithms are often designed by making use of one or more algorithmic
paradigms like dynamic programming or local search, to name a few. Most known quantum
algorithms also use a combination of algorithmic paradigms specific to quantum computing. These
paradigms are the Quantum Fourier Transform (QFT), the Grover Operator (GO), the Harrow-
Hassidim-Lloyd (HHL) method for linear systems, variational quantum eigenvalue solver (VQE),
and direct Hamiltonian simulation (SIM). The number of known quantum algorithmic paradigms is
much smaller compared to the number of known classical paradigms. The constraint of unitarity on
quantum operations and the impossibility of non-intrusive measurement make it difficult to design
quantum paradigms from existing classical paradigms. But researchers are constantly in search
for new paradigms and we can expect this list to get longer in the future. Table 2 also contains
information about the paradigms used by the algorithms in this article.
   The rest of the paper presents each of the algorithms shown in Table 2, one after the other. In
each case, we first discuss the goal of the algorithm (the problem it attempts to solve). Then we
describe the gate sequence required to implement this algorithm. Finally, we show the results from
implementing this algorithm on IBM’s quantum computer1 .
   The list of algorithms in Table 2 is by no means exhaustive. These algorithms have been chosen
due to their relative importance and to provide an overview of the field. Many interesting quantum
1 The code and implementations for most of the algorithms can be found at https://github.com/lanl/quantum_algorithms.
Quantum Algorithm Implementations for Beginners                                                          17


algorithms like those for topological data analysis [83], spatial search [123], supervised learning
[108], etc., have not been covered in this review. Nevertheless the tools and ideas elucidated in
this paper will help the reader understand and implement many quantum algorithms that are not
included here.

2   GROVER’S ALGORITHM
2.1 Problem definition and background
Grover’s algorithm as initially described [63] enables one to find (with√ probability > 1/2) a specific
item within a randomly ordered database of 𝑁 items using 𝑂 ( 𝑁 ) operations. By contrast, a
classical computer would require 𝑂 (𝑁 ) operations to achieve this. Therefore, Grover’s algorithm
provides a quadratic speedup over an optimal classical algorithm. It has also been shown [15] that
Grover’s
    √     algorithm is optimal in the sense that no quantum Turing machine can do this in less than
𝑂 ( 𝑁 ) operations.
   While Grover’s algorithm is commonly thought of as being useful for searching a database, the
basic ideas that comprise this algorithm are applicable in a much broader context. This approach
can be used to accelerate search algorithms where one could construct a “quantum oracle” that
distinguishes the needle from the haystack. The needle and hay need not be part of a database. For
example, it could be used to search for two integers 1 < 𝑎 < 𝑏 such that 𝑎𝑏 = 𝑛 for some number 𝑛,
resulting in a factoring algorithm. Grover’s search in this case would have worse performance than
Shor’s algorithm [113, 114] described below, which is a specialised algorithm to solve the factoring
problem. Implementing the quantum oracle can be reduced to constructing a quantum circuit that
flips an ancillary qubit, 𝑞, if a function, 𝑓 (x), evaluates to 1 for an input x. We use the term ancilla
or ancillary qubit to refer to some extra qubits that are used by the algorithm.
   The function 𝑓 (x) is defined by
                                                    (
                                                      1 if x = x∗
                                          𝑓 (x) =                                                   (32)
                                                      0 if x ≠ x∗
where x = 𝑥 1𝑥 2 . . . 𝑥𝑛 are binary strings and x∗ is the specific string that is being sought. It may seem
paradoxical at first that an algorithm for finding x∗ is needed if such a function can be constructed.
The key here is that 𝑓 (x) need only recognize x∗ – it is similar to the difference between writing
down an equation and solving an equation. For example, it is easy to check if the product of 𝑎
and 𝑏 is equal to 𝑛, but harder to factor 𝑛. In essence, Grover’s algorithm can invert an arbitrary
function with binary outputs, provided we have a quantum oracle that implements the function.
Grover’s algorithm has been used, with appropriate oracles, to solve problems like finding triangles
in a graph [87], finding cycles [32], and finding maximal cliques [131]. For the analysis of Grover’s
algorithm, the internals of the oracle is typically considered a black-box. Often, the oracle operator
for the problem at hand has to be constructed as a quantum circuit. But, keep in mind that an
inefficient oracle construction can nullify any practical advantages gained by using Grover’s search.
   Here we implement a simple instance of Grover’s algorithm. That is, the quantum oracle we
utilize is a very simple one. Let x = 𝑥 1𝑥 2 and we wish to find x∗ such that 𝑥 1∗ = 1 and 𝑥 2∗ = 1. While
finding such an 𝑥 ∗ is trivial, we don a veil of ignorance and proceed as if it were not. This essentially
means that our function 𝑓 (x) is an AND gate. But AND gate is not reversible and cannot be a
quantum gate. However the Toffoli gate, that was introduced in the previous section, is a reversible
version of the classical AND gate. The Toffoli gate takes three bits as input and outputs three bits.
The first two bits are unmodified. The third bit is flipped if the first two bits are 1. The unitary
matrix corresponding to the Toffoli gate can be found in Table 1. In other words, the Toffoli gate
implements our desired quantum oracle where the first two inputs are 𝑥 1 and 𝑥 2 and the third bit is
18                                                                                            Abhijith J., et al.




Fig. 6. A schematic diagram of Grover’s algorithm is shown. Note that in this case, one application of the
Grover operator is performed. This is all that is necessary when there are only two bits in x, but the Grover
operator should be applied repeatedly for larger problems.

                                                                                   É           É
the ancillary bit, 𝑞. The behavior of the oracle in general is |x⟩ |𝑞⟩ → |x⟩ 𝑓 (x)   𝑞 , where   is
the XOR operation . Here we will only discuss the case where x∗ is unique. Grover’s algorithm can
also be used to search for multiple items in a database.

2.2   Algorithm description
Here we present a brief introduction to Grover’s algorithm. A more detailed account can be found
in Nielsen and Chuang [92]. Let 𝑁 be the number of items (represented as bit strings) amongst
which we are performing the search. This number will also be equal to the dimension of the vector
space we are working with. An operator, called the Grover operator or the diffusion operator, is
the key piece of machinery in Grover’s algorithm. This operator is defined by
                                           𝐺 = (2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 )𝑂                                         (33)
where |𝜓 ⟩ = √1 𝑖 |𝑖⟩ is the uniform superposition over all the basis states and 𝑂 is the oracle
                Í
              𝑁
operator (see Fig. 6 for a representation of this operator in the case where x consists of 2 bits). The
                                                                 Í
action of (2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 ) on an arbitrary state, given by 𝑖 𝑎𝑖 |𝑖⟩, when decomposed over the basis
states is,                                         ∑︁          ∑︁
                                (2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 )    𝑎𝑖 |𝑖⟩ =    (2 ⟨𝑎⟩ − 𝑎𝑖 ) |𝑖⟩                 (34)
                                               𝑖            𝑖
              Í
                𝑖 𝑎𝑖
where ⟨𝑎⟩ = 𝑁 is the average amplitude in the basis states. From Eq. (34) one can see that the
amplitude of each |𝑖⟩-state (𝑎𝑖 ) is flipped about the mean amplitude.
   In order to use the Grover operator to successfully perform a search, the qubit register must
be appropriately initialized. The initialization is carried out by applying a Hadamard transform
to each of the the main qubits (𝐻 ⊗𝑛 ) and applying a Pauli X transform followed by a Hadamard
transform (𝐻𝑋 ) to the ancilla. This leaves the main register in the uniform superposition of all
states, |𝜓 ⟩, and the ancilla in the state |0⟩−
                                             √
                                                |1⟩
                                                    . After performing these operations, the system is in
                                              2
the state |𝜓 ⟩ |0⟩−
                 √
                    |1⟩
                        . Using Eq. (34), we can now understand how the Grover operator works. The
                  2
action of the oracle operator on |x∗ ⟩ |0⟩−
                                         √
                                            |1⟩
                                                reverses the amplitude of that state
                                           2

                             𝑓 (x∗ )    0 − 𝑓 (x∗ )
                                     É               É
        ∗ |0⟩ − |1⟩        ∗
                                                         1 )        |1⟩ − |0⟩          |0⟩ − |1⟩
    𝑂 |x ⟩ √         → |x ⟩                √                 = |x∗ ⟩ √        = − |x∗ ⟩ √        (35)
                2                             2                          2                  2
A similar argument shows that all other states are unmodified by the oracle operator. Combining
this with Eq. (34) reveals why the Grover operator is able to successfully perform a search. Consider
Quantum Algorithm Implementations for Beginners                                                        19


what happens on the first iteration: The oracle operator makes it so that the amplitude of |x∗ ⟩ is
below ⟨𝑎⟩ (using the notation of Eq. (34)) while all the other states have an amplitude that is slightly
above ⟨𝑎⟩. The effect of applying 2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 is then to make |x∗ ⟩ have an amplitude above the
mean while all other states have an amplitude below the mean. The desired behavior of the Grover
operator is to increase the amplitude of |x∗ ⟩ while decreasing the amplitude of the other states. If
the Grover operator is applied too manyl √ mtimes, this will eventually stop happening. The Grover
operator should be applied exactly 𝜋 4𝑁 times after which a measurement will reveal x∗ with
probability close to 1. In the case where x has two bits, a single application of Grover’s operator is
sufficient to find x∗ with certainty (in theory). Below is a high level pseudocode for the algorithm.

Algorithm 1 Grover’s algorithm
    Input:
        • An Oracle operator effecting the transformation |𝑥⟩ |𝑞⟩ → |𝑥⟩ |𝑞 ⊕ 𝑓 (𝑥)⟩.
    Output:
        • The unique bit string x∗ satisfying Eq. (32)
    Procedure:
        Step 1. Perform state initialization |0 . . . 0⟩ → |𝜓 ⟩ ( |0⟩−
                                                                    √
                                                                       |1⟩
                                                                           )
                                         l √ m                        2
                                          𝜋 𝑁
        Step 2. Apply Grover operator 4 times
        Step 3. Perform measurement on all qubit except the ancillary qubit.


2.3    Algorithm implemented on IBM’s 5-qubit computer
Fig. 7 shows the circuit that was designed to fit the ibmqx4 quantum computer. The Toffoli gate is
not available directly in ibmqx4 so it has to be constructed from the available set of gates given in
Eq. 26.
    The circuit consists of state preparation (first two time slots), a Toffoli gate (the next 13 time
slots), followed by the 2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 operator (7 time slots), and measurement (the final 2 time slots).
We use 𝑞 [0] (in the register notation from Fig. 7) as the ancillary qubit, and 𝑞 [1] and 𝑞[2] as 𝑥 1 and
𝑥 2 respectively. Note that the quantum computer imposes constraints on the possible source and
target of CNOT gates.
    Using the simulator, this circuit produces the correct answer x = (1, 1) every time. We executed
1,024 shots using the ibmqx4 and x = (1, 1) was obtained 662 times with (0, 0), (0, 1), and (1, 0)
occurring 119, 101, and 142 times respectively. This indicates that the probability of obtaining
the correct answer is approximately 65%. The deviation between the simulator and the quantum
computer is due to the inherent errors in ibmqx4. This deviation will get worse for circuits of larger
size.
    We also ran another test using CNOT gates that did not respect the underlying connectivity of
the computer. This resulted in a significantly deeper circuit and the results were inferior to the
results with the circuit in Fig. 7.
    This implementation used a Toffoli gate with a depth of 23 (compared to a depth of 13 here) and
obtained the correct answer 48% of the time.

3     BERNSTEIN-VAZIRANI ALGORITHM
3.1    Problem definition and background
Suppose we are given a classical Boolean function, 𝑓 : {0,É
                                                          1}𝑛 ↦→ {0, 1}. It is guaranteed that this
function can always be represented in the form, 𝑓s (x) =    𝑖 𝑠𝑖 𝑥𝑖 ≡ ⟨s, x⟩. Here, s is an unknown
20                                                                                             Abhijith J., et al.




Fig. 7. The circuit that was executed on IBM’s 5-qubit quantum computer. The first two time slots correspond
to the state preparation. The next 13 time slots implement a Toffoli gate. The next 7 time slots implement the
2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 operator, and the final two time slots are used for observing 𝑥 1 and 𝑥 2 .



bit string, which we shall call a hidden string. Just like in Grover’s algorithm we assume that we
have a quantum oracle that can compute this function.
   The Bernstein-Vazirani (BV) algorithm then finds the hidden string with just a single application
of the oracle. The number of times the oracle is applied during an algorithm algorithm is known as
its query complexity. The BV algorithm has a query complexity√of one. From our earlier discussions
we saw that Grover’s algorithm has a query complexity of 𝑂 ( 𝑁 ).
   In the classical case each call to 𝑓s (x) produces just 1 bit of information, and since an arbitrary
hidden string s has 𝑛-bits of information, the classical query complexity is seen to be 𝑛. Even with
bounded error, there is no way that this classical complexity can be brought down, as can be seen
using slightly more rigorous information-theoretic arguments.
   The quantum algorithm to solve this problem was developed by Bernstein and Vazirani [16]
building upon the earlier work of Deutsch and Jozsa [41]. Their contribution was a quantum
algorithm for the hidden string problem, which has a non-recursive quantum query complexity
of just 1. This constitutes a polynomial O (𝑛) query-complexity separation between classical and
quantum computation. They also discovered a less widely known recursive hidden-string query
algorithm, which shows a O (𝑛 log 𝑛 ) separation between classical and quantum query-complexities.
These developments preceded the more famous results of Shor and Grover, and kindled a lot of
early academic interest in the inherent computational power of quantum computers.
   One thing to note about the BV algorithm is that the black-box function 𝑓s (·) can be very complex
to implement using reversible quantum gates. For an 𝑛-bit hidden string, the number of simple
gates needed to implement 𝑓s (·) scales typically as O (4𝑛 )[92]. Since the black box is a step in
the algorithm, its serial execution time could in the worst-case even scale exponentially. The real
breakthrough of this quantum algorithm lies in speeding up the query complexity and not the
execution time per se.

3.2     Algorithm description
Let us explore the BV algorithm in more detail. Let 𝑈𝑠 be the oracle for the function 𝑓s (x). It acts in
the usual way and computes the value of the function onto an ancilla qubit,


                                     𝑈𝑠 |x⟩ |𝑞⟩ = |x⟩ |𝑞 ⊕ ⟨s, x⟩⟩                                          (36)
                                √
     Denoting |−⟩ = (|0⟩ − |1⟩)/ 2, we can easily verify from Eq. (35) that,

                                      𝑈𝑠 |x⟩ |−⟩ = (−1) ⟨s,x⟩ |x⟩ |−⟩ .                                     (37)
Quantum Algorithm Implementations for Beginners                                                         21


   Also, note that the 𝑛-qubit Hadamard operator, which is just 𝑛 single qubit 𝐻 operators applied
in parallel, can be expanded as,
                                        1      ∑︁
                                𝐻 ⊗𝑛 = √                (−1) ⟨x,y⟩ |y⟩ ⟨x|                    (38)
                                         2𝑛 x,y∈ {0,1}𝑛
   The reader may verify this identity by applying 𝐻 ⊗𝑛 to the computational basis states.
  𝑈𝑠 and 𝐻 ⊗𝑛 are the only two operators needed for the BV algorithm. The pseudocode for the
algorithm is given in Algorithm 2. Notice that the initialization part is identical to that of Grover’s
algorithm. This kind of initialization is a very common strategy in quantum algorithms.

Algorithm 2 Bernstein-Vazirani algorithm
  Input:
      • An oracle operator, 𝑈𝑠 , effecting the transformation |𝑥⟩ |𝑞⟩ → |𝑥⟩ |𝑞 ⊕ ⟨s, x⟩⟩.
  Output:
      • The hidden string s.
  Procedure:
      Step 1. Perform state initialization on 𝑛 + 1 qubits, |0 . . . 0⟩ → |𝜓 ⟩ |−⟩
      Step 2. Apply 𝑈𝑠 .
      Step 3. Apply 𝐻 ⊗𝑛 to the first 𝑛 qubits.
      Step 4. Measure all qubits except the ancillary qubit.


   The final measurement will reveal the hidden string, s, with probability 1. Let us now delve
into the algorithm to see how this result is achieved. The entire circuit for the BV algorithm is
represented in Figure 8. This circuit can be analyzed as follows,
                                        2𝑛 −1                            2𝑛 −1
                      𝐻 ⊗ (𝑛) ⊗𝐻    1 ∑︁                    𝑈𝑠       1 ∑︁
           |0⟩𝑛 |1⟩   −−−−−−−→     √          |x⟩ ⊗ |−⟩     −−→     √          (−1) ⟨s,x⟩ |x⟩ ⊗ |−⟩
                                     2𝑛 x=0                           2𝑛 x=0
                                        2𝑛 −1
                         𝐻 ⊗𝑛       1 ∑︁
                        −−−→       √          (−1) ⟨s,x⟩ ⊕ ⟨x,y⟩ |y⟩ ⊗ |−⟩   ≡    |s⟩ ⊗ |−⟩ .         (39)
                                     2𝑛 x,y=0
  Here we have crucially used the identity for 𝐻 ⊗𝑛 given in Eq.(38).

3.3   Algorithm implemented on IBM’s 5-qubit and 16-qubit computers
From the BV algorithm description in the previous section, we see that in any practical implementa-
tion of this algorithm, the main ingredient is the construction of the oracle 𝑈 s given a binary hidden
string s. Let us see how this is done using an example binary hidden string “01”. Equation (40)
below shows how the 3-qubit operator maps the 23 = 8 basis vectors onto themselves. The first line
is the input binary vector (in the order 𝑥 1, 𝑥 0, 𝑞), and the second line is the output binary vector.
                                                                                
                                 000 010 100 110 001 011 101 111
                        𝑈 01 =                                                                      (40)
                                 000 011 100 111 001 010 101 110
This mapping, 𝑈 01 : |x⟩ |𝑞⟩ ↦→ |x⟩ |⟨01, x⟩ ⊕ 𝑞⟩, is unitary. The next task in implementation is to
lower the unitary matrix operator 𝑈 01 to primitive gates available in the quantum computer’s
architecture given in Eq (26). The time cost of applying these gates can be accessed from IBM’s
published calibration models [125] for the primitive hardware gates.
  In order to decompose arbitrary unitary matrices to the primitive gates, we need to first perform
a unitary diagonalization of the 2 (𝑛+1) × 2 (𝑛+1) matrix using multi-qubit-controlled single-qubit
22                                                                                                   Abhijith J., et al.




Fig. 8. Bernstein-Vazirani hidden string discovery quantum algorithm. The hidden string s is discovered with
just a single query. The measurement result s e gives the hidden string.


unitary Given’s rotation operations. Such multi-qubit-controlled single-qubit operations can be
decomposed further to primitive gates using standard techniques [92] to the hardware primitive
gates. Even after this step we will be left with arbitrary CNOT gates that do not respect the topology
of the underlying quantum processor. Since both ibmqx4, ibmqx5 computers have restricted CNOT
connectivity between qubits, we will need to decompose the CNOT gates further into available
CNOT gates using the method discussed in the introductory section. As we saw in the Grover’s
algorithm section, such decompositions will further degrade the quality of our results. As the overall
primitive gate counts scale as O (4𝑛 ) for arbitrary 𝑛-qubit unitary operators, these decompositions
quickly becomes hard to do by hand. To address this we wrote a piece of software called Quantum
Netlist Compiler (QNC) [107] for performing these transformations automatically. QNC can do
much more than convert arbitrary unitary operators to OpenQASM-2.0 circuits—it has specialized
routines implemented to generate circuits to do state-preparations, permutation operators, Gray
coding to reduce gate counts, mapping to physical machine-topologies, as wells as gate-merging
optimizations. Applying QNC tool to the unitary matrix 𝑈 s gives us a corresponding quantum gate
circuit 𝐺 s as shown in Figure 8 for a specific bit-string s.
   QNC generated black-box circuits with following gate-counts for the non-trivial 2-bit hidden-
strings: “01”: 36, “11”: 38, “10”: 37, with estimated execution time2 for critical path ∼17𝜇𝑠 on an ideal
machine with all-to-all connection topology. For the 5-qubit ibmqx4 machine the corresponding
gate-counts where: “01”: 42, “11”: 43, “10”: 41, with estimated execution time for critical path ∼15𝜇𝑠,
and for the 16-qubit ibmqx5, they were: “01”: 66, “11”: 67, “10”: 67, with estimated execution time for
critical path ∼28𝜇𝑠. In all these cases, QNC used a specialized decomposition of 𝑈 01 , considering its
permutation matrix nature, and therefore was able to reduce gate-counts by 5× over the case when
this special structure was ignored. Considering that the machines’ observed coherence times are of
the order of ∼60𝜇𝑠, these QNC optimizations were crucial to the feasibility of the resulting score.
The quantum score (circuit) generated by QNC for 𝑈 01 for ibmqx4 is shown in Figure 9. A similarly
prepared score for 3-bit hidden-string “111” had a gate-count of 428 in the ibmqx4 architecture
with an estimated execution time of 153𝜇𝑠 which was well above the machines’ coherence times.
2 These times are estimated using the data available from IBM at the time of writing. These values will change as the

hardware improves.
Quantum Algorithm Implementations for Beginners                                                              23


    We tested the QNC generated quantum scores for all non-trivial 1-qubit, 2-bit and 3-bit strings
using the IBM-Qiskit based local simulator. In all cases, the simulator produced the exact hidden-
string as the measurement result, 100% of the trials. We then tested all 1-bit and 2-bit strings on
both the 5-qubit ibmqx4 and the 16-qubit ibmqx5 machines. The results are shown in Figure 10.
For 2-bit strings, the worst case noise was observed for the string “01” on ibmqx4 when the qubits
𝑞 0, 𝑞 1, 𝑞 2 where used for 𝑥 0, 𝑥 1, 𝑦 respectively. Since the estimated critical path times exceeded the
machines’ coherence times for 3-bit strings, we did not run those scores on the physical machines.
Even for 2-bit strings, the scores were quite long, and the results were quite noisy even with 8192
machine-shots.




Fig. 10. Results from running the BV algorithm for 8192 shots on 2-bit hidden-strings “01”, “10” and “11”
respectively (left to right) on ibmqx4. The y-axis here is the probability of obtaining the hidden string, which
theoretically should be 1.


4     LINEAR SYSTEMS
4.1     Problem definition and background
Solving linear systems is central to a majority of science, engineering, finance and economics
applications. For example, one comes across such systems while solving differential or partial
differential equations or while performing regression. The problem of solving a system of linear
equations is the following: Given a system 𝐴𝑥® = 𝑏,  ® find 𝑥® for a given matrix 𝐴® and vector 𝑏.    ® Here
we assume that 𝐴 is a Hermitian matrix, in that it is self-adjoint. To represent ®       𝑥, 𝑏® as quantum
states |𝑥⟩, |𝑏⟩, respectively, one has to rescale them as unit vectors, such that ||𝑥® || = ||𝑏®|| = 1. Thus,
one can pose the problem as finding |𝑥⟩ such that

                                                  𝐴 |𝑥⟩ = |𝑏⟩ ,                                            (41)

with the solution |𝑥⟩ being

                                                        𝐴−1 |𝑏⟩
                                              |𝑥⟩ =                .                                       (42)
                                                      ||𝐴−1 |𝑏⟩ ||




      Fig. 9. Quantum circuit for BV algorithm with hidden string “01” targeting the ibmqx4 architecture.
24                                                                                      Abhijith J., et al.


4.2   Algorithm description
The quantum algorithm for the linear system was first proposed by Harrow, Hassidim, and Lloyd
(HHL) [66]. The HHL algorithm has been implemented on various quantum computers in [12, 27,
137]. The problem of solving for 𝑥® in the system 𝐴𝑥® = 𝑏® is posed as obtaining expectation value of
some operator 𝑀 with ®   𝑥, 𝑥®† 𝑀 ®
                                 𝑥, instead of directly obtaining the value of ®
                                                                               𝑥. This is particularly
useful when solving on a quantum computer, since one usually obtains probabilities with respect
to some measurement, typically, these operators are Pauli’s operators 𝑋 , 𝑌 , 𝑍 . These probabilities
can then be translated to expectation values with respect to these operators.
   The user has to keep in mind certain caveats while using the HHL algorithm. The algorithm
requires that the elements of 𝑏® be accessible in superposition. Also, the solution vector is given as
a quantum state which collapses after every measurement. This means that the HHL algorithm
involves additional overheads for loading and reading data from a quantum computer [2]. Recently,
classical algorithms inspired by HHL have been developed that, while having assumptions similar
to HHL, considerably reduce the complexity of solving linear systems on classical computers [29]
   The main idea of the HHL algorithm is as follows. Let { 𝑢 𝑗 } and {𝜆 𝑗 } be the eigenvectors and
eigenvalues of 𝐴, respectively, with the eigenvalues rescaled such that 0 < 𝜆 𝑗 < 1. Then the state
                                                                               Í
|𝑏⟩, can be written as a linear combination of the eigenvectors { 𝑢 𝑗 }, |𝑏⟩ = 𝑁𝑗=1 𝛽 𝑗 𝑢 𝑗 . The goal
of the HHL algorithm is to obtain |𝑥⟩ in the form |𝑥⟩ = 𝑗=1 𝛽 𝑗 𝜆1𝑗 𝑢 𝑗 . By decomposing 𝐴 = 𝑅 † Λ𝑅,
                                                          Í𝑁

the HHL algorithms in a nutshell involves performing a set of operations that essentially performs
the three steps:
                         Step1                Step2                   Step3
        𝑅 † Λ𝑅 |𝑥⟩ = |𝑏⟩ =⇒ Λ𝑅 |𝑥⟩ = 𝑅 |𝑏⟩ =⇒ 𝑅 |𝑥⟩ = Λ−1 𝑅 |𝑏⟩ =⇒ |𝑥⟩ = 𝑅 † Λ−1𝑅 |𝑏⟩                (43)
  This procedure requires us to find the eigenvalues of 𝐴. This can be done using a quantum
subroutine called phase estimation. We will discuss this subroutine in some detail as it is a common
ingredient in many quantum algorithms.

4.3   Phase estimation
Phase estimation is a quantum subroutine that lets us find the eigenvalues of a unitary matrix 𝑈
given the ability to apply it to a quantum register as a controlled gate. Let |𝑢⟩ be an eigenvector
of 𝑈 such that, 𝑈 |𝑢⟩ = 𝑒 2𝜋𝑖𝜆𝑢 |𝑢⟩. Then the phase estimation subroutine effects the following
transformation,                                       E
                                                 → 𝜆˜𝑢 |𝑢⟩ .
                                         |0⟩ |𝑢⟩ −                                             (44)
  Here 𝜆˜𝑢 is an estimate for 𝜆𝑢 . This subroutine makes use of an important transformation called
the Quantum Fourier Transform (QFT)
   Quantum Fourier Transform. The Discrete Fourier Transform (DFT) takes as an input a vector 𝑋
of size 𝑁 and outputs vector 𝑌 = 𝑊 𝑋 where the Fourier matrix 𝑊 is defined by
                                 1     1         1     ...        1        
                                                    2              𝑁 −1
                                                                           
                                 1     𝜔        𝜔      . . .    𝜔          
                              1 1
                                 
                                       𝜔   2     𝜔  4   . . .  𝜔 2(𝑁 −1)
                                                                            
                      𝑊 =√ 
                                                                            
                                                                            ,
                              𝑁 .
                                  .     .
                                         .        .
                                                  .     . .         .
                                                                    .       
                                 .      .        .         .       .       
                                                                            
                                 1 𝜔 𝑁 −1 𝜔 2(𝑁 −1) . . . 𝜔 (𝑁 −1) (𝑁 −1) 
                                                                           
where the 𝑖 𝑗-th element of the matrix is 𝑊𝑖 𝑗 = 𝜔 and 𝜔 is a primitive 𝑁 -th root of one(𝜔 𝑁 = 1). A
                                                  𝑖 𝑗

straightforward implementation of the matrix-vector multiplication takes 𝑂 (𝑁 2 ) operations, but, by
using the special structure of the matrix, the Fast Fourier Transform (FFT) does the multiplication
 asgupta, C.H. Papadimitriou, and U.V. Vazirani                                                                        323

5.3     The quantum Fourier transform circuit
e we haveQuantum
           reproduced     the
                  Algorithm    diagram (from
                            Implementations          Section 2.6.4) showing how the classical FFT cir-
                                            for Beginners                                                  25

 for M -vectors is composed of two FFT circuits for (M/2)-vectors followed by some simple
s.        in only 𝑂 (𝑁 log 𝑁 ) time. The algorithm is recursive and is illustrated on Figure 11. The Quantum

                                   FFTM (input: α0 , . . . , αM −1 , output: β0 , . . . , βM −1 )

                                                   x0
                                                   x2
                                                   ..     FFTN/2                     yj
                                                    .                          +
                                                xN−2
                                                   x1
                                                   x3
                                                    ..    FFTN/2
                                                                     ωj        -     yj+N/2
                                                     .
                                                xN−1


s see howFig.
            to 11. Fast
                simulate     this
                        Fourier     on a circuit,
                                Transform   quantumwhere 𝑗system.       The
                                                             denotes a row  frominput
                                                                                  the opishalf
                                                                                            now      ncoded
                                                                                               of the circuit andin
                                                                                                                  𝜔 𝑗 the  2m
                                                                                                                      denotes
 litudes ofthat
            m the  log M qubits.
                = corresponding   valueThus    the decomposition
                                        is multiplied                       of the
                                                      by 𝜔 . The plus and minus        inputs
                                                                                   symbols      intothat
                                                                                            indicate    evens    and odds,
                                                                                                           the corresponding
                                                           𝑗
           values have to be added or subtracted, respectively.
hown in the preceding figure, is clearly determined by one of the qubits—the least sig-
 ant qubit. How do we separate the even and odd inputs and apply the recursive circuits
ompute F F          on each half?
             TM/2 Transform
           Fourier               (QFT) The    answer
                                         is defined   as aistransformation
                                                               remarkable:between just apply      the quantum
                                                                                          two quantum                 circuit
                                                                                                             states that  are
TM/2 to thedetermined
             remaining      m   −  1 qubits.     The   effect    of this   is  to  apply
                        using the values of DFT (FFT). If 𝑊 is a Fourier matrix and 𝑋 =M/2 QF    T       to   the  superpo-
                                                                                                    {𝑥𝑖 } and 𝑌 = {𝑦𝑖 } are
 n of all the  m-bit
           vectors suchstrings
                         that 𝑌 =of𝑊the    form
                                      𝑋 , then  thex0
                                                    QFT(ofiswhich
                                                              defined there     are M/2), and separately to the
                                                                       as the transformation
erposition of all the m-bit strings of the form x1. Thus            ! 𝑁 −1the two recursive classical circuits
 be emulated by a single quantum circuit—an                     exponential        speedup when we unwind the
                                                        𝑁
                                                        ∑︁−1             ∑︁
                                                 Q𝐹𝑇          𝑥𝑘 |𝑘⟩ =        𝑦𝑘 |𝑘⟩ .                                   (45)
 rsion!                                                 𝑘=0              𝑘=0

             The implementation of the QFT mimics the stages (recursive calls) of the FFT, but implements
                   qubits
              − 1 stage
          meach          using only 𝑛QFT                                   QFT
                                     + 1 additional gates per stage. A single
                                          M/2
                                                                              Hadamard gate on the last (least
                                                                                M/2
             significant) bit implements the additions/subtractions of the outputs from the recursive call and
             the multiplications by 𝜔 are done using 𝑛 controlled phase gates. The circuit for 𝑛 = 5 is shown
                                      𝑗

       least on Figure
              significant
                       12. bit                                                             H

Let us now consider the gates in the classical FFT circuit after the recursive calls to
TM/2 : the wires
             𝐻 𝑃 ( 2pair
                     ) up𝑃j( 𝜋4with                 and
                                                 𝑃 ( 𝜋8 ) ignoring for now           the) phase that is applied
                   𝜋                                                                 𝜋
                                  )     M/2 + j,                                 𝑃 ( 16
he contents of the                    wire,
                      (M/2 + j)th 𝑃 ( 𝜋      we must add  𝑃 ( 𝜋4 )and subtract these𝑃two    ( 𝜋8 ) quantities to ob-
                  •                      2)
  the jth and the (M/2 + j)th outputs, respectively. How would a quantum circuit achieve
                        𝐻

result of these M classical    • gates? •   Simple: just perform
                                             𝐻                      𝑃 ( 𝜋2 ) the Hadamard gate      𝑃 ( 𝜋4 )on the first
 t! Recall from the preceding discussion (Section               10.5.1)     that for every possible 𝑃 ( 𝜋    configura-
                                                    •        •         •                                         2)
  of the remaining m − 1 qubits x, this pairs up the strings 0x and 1x. Translating                                 from
                                                                              𝐻

 ry, this means we are pairing up x and M/2+x. Moreover the result                  •     of •the Hadamard
                                                                                                       •        • gate𝐻
 at√ for each such pair, the    amplitudes are replaced by the sum and difference (normalized
                             Fig. 12. A Quantum Fourier Transform circuit for five qubits (𝑛 = 5).
 / 2) , respectively. So far the QFT requires almost no gates at all!
The phase that must be applied to the (M/2 + j)th wire for each j requires a little more
k. Notice thatThe the
                  phasephase    of ωprocedure
                         estimation
                                      j must be applied only if the first qubit is 1. Now if j is
                                               cleverly uses the QFT operator to estimate the eigenphases of
              the operator 𝑈 . The circuit for performing phase estimation given in Fig. 13. Notice that the QFT is
              applied in reverse.
26                                                                                      Abhijith J., et al.



            |0⟩         𝐻                        ···         •

                  ...
                                                                       QF T †
            |0⟩         𝐻               •        ···


            |0⟩         𝐻      •                 ···


            |𝑢⟩         /     𝑈        𝑈2        ···       𝑈2
                                                                 𝑡




                              Fig. 13. Quantum circuit for phase estimation.


  The pseudocode for phase estimation is given in Algorithm 3. Notice that the algorithm also
works if the input state is not an eigenstate. The output in this case can be determined by expanding
the input state in terms of the eigenstates and then applying the linearity of quantum operations.
In the code, we have numbered the ancillary qubits from the top and 𝐶𝑖 𝑈 denotes the unitary
controlled by the 𝑖 th ancilla qubit acting on the main 𝑛 qubit register.

Algorithm 3 Phase estimation subroutine
     Input:
          • Controlled unitaries 𝐶𝑖 𝑈
          • An 𝑛 qubit input state |𝜓 ⟩ = 𝑢 𝜓𝑢 |𝑢⟩, where 𝑈 |𝑢⟩ = 𝑒 2𝜋𝑖𝜆𝑢 |𝑢⟩ .
                                         Í
     Output:         E
          • 𝑢 𝜓𝑢 𝜆˜𝑢 |𝑢⟩
            Í

     Procedure:
          Step 1. Take 𝑡 ancillary qubits initialized to zero and perform 𝐻 ⊗𝑡 on them to produce the
     uniform superposition state over them.
          for 0 ≤ 𝑖 < 𝑡 do
                 Step 2. Apply 𝐶𝑡 −𝑖−1𝑈 2
                                          𝑖


          end for
          Step 3. Apply QF T † .                              E
          Optional Measure the ancillary qubits to get 𝜆˜𝑢 |𝑢⟩ with probability |𝜓𝑢 | 2


   The number of ancillary qubits used in the phase estimation algorithm will determine both its
run-time and its accuracy. On the accuracy front, the number of ancillary qubits used is equal to the
bit precision of 𝜆˜𝑢 as the answer is stored in this register. The exact complexity of this subroutine
is discussed in Ref. [92].
   Now we can discuss the HHL algorithm which makes use of the phase estimation procedure to
perform a matrix inversion. The HHL algorithm requires three sets of qubits: a single ancilla qubit,
a register of 𝑛 qubits used to store the eigenvalues of 𝐴 in binary format with precision up to 𝑛 bits,
and a memory of 𝑂 (log(𝑁 )) that initially stores |𝑏⟩ and eventually stores |𝑥⟩. Start with a state
|0⟩𝑎 |0⟩𝑟 |𝑏⟩𝑚 , where the subscripts 𝑎, 𝑟 , 𝑚, denote the sets of ancilla, register and memory qubits,
                                                               FIG. 1:                                                                                                                              FIG. 1:

                                                                             Thisalgorithm
                                                                                     algorithm        wasdiscussed
                                                                                                             discussed                                         FIG.XX.1:
 s discussed in Ref. XXX Need citation          FIG. XX.
                                                      1: It is then         This
                                                                        straightforward        to wascalculate    the ininRef. Ref.XXX
                                                                                                                         eigenvalues XXXNeed   Needcitation
                                                                                                                                                        citation      XX.ItItisisth  th
  lows:                                                                      of
                                                                            of  ⌃⌃  from
                                                                                   from    PP, ,asas    follows:
                                                                                                      follows:                                                   FIG.1:1:
                                                                                                                                                                FIG.
s discussed in Ref. XXX Need citation            FIG.XX.
                                                FIG.  1:1: It is then       This    algorithm
                                                                        straightforward        to was       discussed
                                                                                                    calculate     the in      Ref. XXX Need citation XX. It is th
                                                                                                                        eigenvalues
                                                     p                                                                                                              pp
 lows:                                                                      of  ⌃  from    P ,   as   follows:                         ee11==    Tr(⌃)
                                                                                                                                                Tr(⌃)     ⇤⇤(1 (1++ XX.11 2(1 2(1 P
                                                                            This   algorithm        was     discussed     in  Ref.  (6)
                                                                                                                                    XXX        Need    citation      p It is th
                           e    =   Tr(⌃)
   discussed in Ref. XXX Need citation p
                Quantum    Algorithm
                             1               ⇤ (1 +     1    2(1    P ))/2
                                                     XX. It is then straightforward to calculate the eigenvalues
                                         Implementations     for Beginners                                                                                        27p
                                                                                                                                                                    p
 lows:                                                                      of  ⌃  from    P ,   as   follows:                         eee212= = Tr(⌃)    ⇤⇤⇤(1(1+ XX. 111 It2(1
ssdiscussed             XXX
                   Ref.XXX
    discussedininRef.
                           e12 = Tr(⌃) ⇤ (1 + 1 2(1 P ))/2 .This
                                  Need     citation p
                                  Needcitation        XX.                    Thisalgorithm
                                                                                     algorithm
                                                                         straightforward
                                                                   thenstraightforward
                                                      XX.ItItisisthen                          to   waswasdiscussed
                                                                                                      calculate
                                                                                                 tocalculate discussed
                                                                                                                   theeigenvalues
                                                                                                                  the          Ref.(6)
                                                                                                                          ininRef.  (7)
                                                                                                                                     XXX
                                                                                                                                    XXX
                                                                                                                          eigenvalues
                                                                                                                                              = Tr(⌃)
                                                                                                                                                 Tr(⌃)
                                                                                                                                                Need
                                                                                                                                               Need           (1
                                                                                                                                                        citation
                                                                                                                                                       citation       XX.    It2(1
                                                                                                                                                                             2(1     thP
                                                                                                                                                                                isisth
                                                     p                       of      from      ,  as    follows:                                                    p
  llows:
 lows:          respectively.                                               of  ⌃⌃ from    PP,   as   follows:
Fig.  ??, this simple     ee12  = This
                        algorithm
                                =  Tr(⌃)
                                   Tr(⌃)issubscript
                                            ⇤⇤ (1
                                               (1 +    notation
                                            schematically   2(1
                                                       11 2(1       was
                                                                    P ))/2
                                                              divided
                                                                    P    used
                                                                      ))/2
                                                                        up .intoin
                                                                                As  [137],
                                                                                Asfourdepicted
                                                                                    depicted andininwe
                                                                                          steps:            found
                                                                                                          Fig.
                                                                                                         Fig.   ??,this
                                                                                                               ??,
                                                                                                       classical             be
                                                                                                                        tosimple
                                                                                                                    itthis      most
                                                                                                                             simple
                                                                                                                   pre-processing,  (7)e1
                                                                                                                                      algorithm
                                                                                                                                     algorithm
                                                                                                                                    (6) useful
                                                                                                                                           2            keeping
                                                                                                                                                   inisisschematically
                                                                                                                                              = Tr(⌃)      ⇤schematically
                                                                                                                                                              (1 + 1 2(1        divid
                                                                                                                                                                               divid
                                                     p                       state    preparation,         quantifying       the  purity,     and  classical        pp
                                                                                                                                                                  post-processing
                things
 quantifying the purity,clear. and The   HHL
                                     classical        p
                                                  algorithm    requires
                                                  post-processing.        usstate
                                                                               to   preparation,
                                                                                  run    the   phase      quantifying
                                                                                                            estimation     the  purity,
                                                                                                                             procedure  e e and
                                                                                                                                              on
                                                                                                                                              ==  classical
                                                                                                                                                  the
                                                                                                                                                Tr(⌃)
                                                                                                                                                  Tr(⌃) unitary
                                                                                                                                                           ⇤ ⇤(1
                                                                                                                                                               (1post-processing
                                                                                                                                                                 + +    11   2(1
                                                                                                                                                                               2(1
                                                                                Asfour
                                                                                    depicted
                                                                                          steps:in Fig.        ??, this simple(7)    algorithm is schematically divid
                                                                                                                                     (6)1
                                                                                                                   eigenvalues(6)
  ig. ??, this simple     e
                       algorithm==Tr(⌃)     ⇤⇤(1(1++
                                        isphases       11 2(1
                                            schematically           PP))/2
                                                              divided  ))/2.into
                                                                        up                             classical                           2
                                                                                                           to thepre-processing,
                                                                                                                                            1
                operator e𝑒211𝑖𝐴     Tr(⌃)
                                  . The              estimated
                                                     pp
                                                              2(1
                                                                  would    be approximations                                          of 𝐴. The problemp             p
 quantifying the purity,       and   classical    post-processing.          state preparation, quantifying the purity,                  ee22and   classical
                                                                                                                                              ==Tr(⌃)
                                                                                                                                                  Tr(⌃)    ⇤ ⇤ (1
                                                                                                                                                              (1 post-processing
                                                                                                                                                                        11 2(1 2(1
                of applyingee22 = = Tr(⌃)
                                  theTr(⌃)   ⇤
                                       unitary⇤ (1
                                               (1       11
                                                    operation 2(1
                                                             2(1 𝑒  P
                                                                   𝑖𝐴P ))/2
                                                                      ))/2
                                                                      given. .  As
                                                                               the  depicted
                                                                                    matrix
  ig. ??, this simple algorithm is schematically divided up into four steps: classical pre-processing,
                                                                                                𝐴  inis  Fig.
                                                                                                         called??,  this
                                                                                                                  quantum   simple   (7)
                                                                                                                                    (7)
                                                                                                                                     algorithm
                                                                                                                                  simulation.        is
                                                                                                                                                    There schematically
                                                                                                                                                                are            divid
                                      Classical Pre-processing                                                                                      ClassicalPre-processing
                                                                                                                                                   Classical       Pre-processing
 quantifying themanypurity,   and classical
                       algorithms                 post-processing.
                                          in literature                     state
                                                           that tackle the problem  preparation,
                                                                                           of   quantum   quantifying
                                                                                                                simulation the   purity,
                                                                                                                                 [17]   [56] and  classical
                                                                                                                                                and    that      post-processing
                                                                                                                                                               will
Fig.   ??,this
 Fig.??,   thissimple                                          dividedup
                                             schematicallydivided
                         algorithmisisschematically
                 simplealgorithm                                                 Asfour
                                                                              into
                                                                         upinto As    depicted
                                                                                    depicted
                                                                                    four   steps:
                                                                                          steps:          Fig.??,
                                                                                                   ininclassical
                                                                                                         Fig.   ??,pre-processing,
                                                                                                        classical   this                                    schematicallydivid
                                                                                                                                      algorithmisisschematically
                                                                                                                             simplealgorithm
                                                                                                                     thissimple
                                                                                                                    pre-processing,                                             divid
                not  be our and  focus   in   thispost-processing.
                                      Classical     section.
                                                   Pre-processing            state the
                                                               We will explain
                                                                            state     preparation,
                                                                                           steps of the
                                                                                    preparation,           quantifying
                                                                                                                HHL the
                                                                                                          quantifying        the
                                                                                                                         algorithmpurity,and
                                                                                                                                 purity,  below     Classical
                                                                                                                                                   classical
                                                                                                                                              andclassical
                                                                                                                                                    assuming      Pre-processing
                                                                                                                                                                  post-processin
   quantifyingthe
 quantifying    thepurity,
                     purity,and       classical
                                     classical     post-processing.
                                                         State preparation                                                                                Statepost-processing
                                                                                                                                                         State     preparation
                                                                                                                                                                  preparation
                       that the quantum simulation part is taken care of. We will also include some mathematical  details
                                                                                                             Classical Pre-processing
                                      Classical Pre-processing                                                   State preparation
                       in the pseudocode State
                                          given preparation
                                                  in Algorithm 4 .                                            Quantifying
                                                                                                             Quantifying    thepurity
                                                                                                                           the  purity
                                       Quantifying the purity                                                                                                                      ClassicalPre-processing
                                                                                                                                                                                  Classical  Pre-processing
                                                    ClassicalPre-processing
                                                   Classical    Pre-processing                                                                                                       State preparation
                                                      State preparation                                                                                                            Quantifying the purity
                                                    Quantifying the purity                                                                                                        ClassicalPost-processing
                                                                                                                                                                                 Classical  Post-processing
                                                   Classical Post-processing                                                                                                          Statepreparation
                                                                                                                                                                                     State   preparation
                                                              Phase
                                                        Statepreparation
                                                       State   preparation                           Controlled                          Inverse phase
                                                    Quantifying the purity                                                                                                         Quantifying the purity
                                                   Classicalestimation
                                                              Post-processing                         rotation                             estimation                         Post-processing
                                                                                                                                                                                 Classical Post-processing
                                                     Quantifyingthe
                                                    Quantifying    thepurity
                                                                       purity                                                                                                       Quantifyingthe
                                                                                                                                                                                   Quantifying   thepurity
                                                                                                                                                                                                     purity
                                                   Classical Post-processing                                                                                                     Classical Post-processing
                                                                    !(#)                                                                                                       QST
                                                                                                                                                                          |0iData
                                                                                                                                                                         |0iData
                                                                                                                                                                           1         on the!
                                                                                                                                                                                   vectors
                                                                                                                                                                                 vectors    !⌃⌃! !⇢⇢!  !| | i
                         ancilla |0iData vectors ! ⌃ ! ⇢ ! | i vector                                          !(#/&)
                                                                                                                                                                                  Classical
                                                                                                                                                                                 Classical   Post-processing
                                          ClassicalPost-processing
                                         Classical  Post-processing                                                                                                           memory   qubitPost-processing
                        register |0iData vectors ! ⌃ ! ⇢ ! | Xi vector                                                         X                                          |0iData vectors ! ⌃ ! ⇢ ! |
                                                                                                            Algorithmimplementedimplementedon
              Algorithm implemented on IBM’s               5-qubit computer
                register |0iData vectors ! ⌃ ! ⇢X! | Xi vector                       X X
                                                                                                           Algorithm
                                                                                                                          |0iData    vectors ! on    IBM’s5-q
                                                                                                                                                       ⇢ ! |5-
                                                                                                                                                 ⌃ IBM’s
                                                                                                                                                    !
                                                                                                                                   Expectation
              Algorithm      implemented on IBM’s 5-qubit computer                                          Algorithm          implemented
                                                                                                                           |0iData
                                                                                                                          |0iData
                                                                                                                            x         vectors
                                                                                                                                     vectors
                                                                                                                                   values with!!on
                                                                                                                                                 ⌃⌃!IBM’s
                                                                                                                                                     ! ⇢⇢!  5-q
                                                                                                                                                          !| |
               memory b   |0iData
                         |0iData   vectors!
                                  vectors
                                     H
                                  Classical !  ⌃⌃! !⇢⇢!          vector
                                                         !| | iivector
                                            Post-processing                                                     H                    Classical
                                                                                                                                    Classical   Post-processing
                                                                                                                                               Post-processing
                                                                                                                                  Pauli X, Y, Z
              Algorithm implemented on IBM’s 5-qubit computer                                               Algorithm implemented on IBM’s 5-q
                                  Classical Post-processing                                                                         Classical Post-processing
                                        Conclusions                                                                                        Conclusions
                                                                                                                                          Conclusions
               Algorithm
              Algorithm       implemented
                             implemented       on
                                              on   IBM’s
                                                  IBM’s     5-qubit
                                                          5-qubit     computer
                                                                     computer                                Algorithm
                                                                                                            Algorithm           implemented
                                                                                                                               implemented       onIBM’s
                                                                                                                                                on   IBM’s5-q5-
               Fig. 14.   Schematic  of the  circuit for the
                                  Classical Post-processing   quantum   algorithm   for solving   a   2 × 2 linear      system.   The  first
                                                                                                                                    Classicalstep
                                                                                                                                               Post-processing
                                        Conclusions                                                                                        Conclusions
  f RB it that involves    phase estimation,
               it is insensitive               which maps
                                  to state-preparation    andthe   eigenvalues
                                                                        The
                                                                measurement   advantage
                                                                        The errors
                                                                                𝜆   of A
                                                                             advantage   ofof
                                                                                          into
                                                                                       (SPAM),RB
                                                                                             RB   ititand
                                                                                                the     thatititisisit
                                                                                                       register
                                                                                                       that
                                                                                                          that         insensitive
                                                                                                                        the
                                                                                                                   in can     binaryto
                                                                                                                     insensitive     to state-preparation
                                                                                                                                      form. The
                                                                                                                                       state-preparation
                                                                                                                                     Classical
                                                                                                                                                             an
                                                                                                                                                            and
                                                                                                                                                Post-processing
                                   ClassicalPost-processing
                                  Classical  Post-processing
                                                                                  𝑗                                                 Classical  Post-processing
               second
  ore eﬃciently on   logical  involves
                         step qubits than   processrotation
                                       controlled
                                        Conclusions   tomography.     be
                                                              of the be  implemented
                                                                        implemented
                                                                     ancilla qubit,      more
                                                                                        more
                                                                                    so that      eﬃcientlyofon
                                                                                                eﬃciently
                                                                                              the inverse       onthe  logical
                                                                                                                     logical     qubitsthan
                                                                                                                                qubits
                                                                                                                         eigenvalues     than  processtomogr
                                                                                                                                              process
                                                                                                                                          Conclusions
                                                                                                                                         1 show         tomog
    f RB it that it is insensitive to state-preparation and measurement                                 The
                                                                                                          The
                                                                                                        The      advantage
                                                                                                                  RB
                                                                                                                 RB  errors
                                                                                                                       protocol    of goes
                                                                                                                               (SPAM),
                                                                                                                         protocol      RB
                                                                                                                                        goesitas that
                                                                                                                                               and
                                                                                                                                                as        it isitinsensitive
                                                                                                                                                       that
                                                                                                                                                     follows.
                                                                                                                                                    follows.          can                  to 𝜆 𝑗state-preparation and
    l goes as follows.up in the state. The third                     step is tomography.
                                                                                the inverse phase            estimation
                                                                                                     be implemented            tomore
                                                                                                                                   disentangle
                                                                                                                                           eﬃciently    theonsystem,
                                                                                                                                                                   logicaland    qubits  restores         the
                                                                                                                                                                                                      Conclusions
                                                                                                                                                                                                     Conclusions
                                                                                                                                                                                                  than     process tomogr
 ore eﬃciently on logical qubits than                             process
                                                            Conclusions
                                                           Conclusions                                  The      advantage         of RB itand   thatthat it get
                                                                                                                                                              isitinsensitive              to state-preparation              and
       RB itasthat
  fl goes             registers
                       it
                  follows.is         to
                              insensitive
                                        |0⟩.   The
                                                to       memory
                                                       state-preparation qubit    nowandstores
                                                                                             measurement
                                                                                                   |𝑥⟩, which
                                                                                                        The1. RB
                                                                                                          1.        is  then
                                                                                                                    errors
                                                                                                                Randomly
                                                                                                               Randomly        (SPAM),
                                                                                                                        protocolpost-processed
                                                                                                                                       goesaaas
                                                                                                                                  choose
                                                                                                                                 choose             follows.
                                                                                                                                                 setofof
                                                                                                                                                set      tom          the
                                                                                                                                                                      can    expectation
                                                                                                                                                                  elementsfrom
                                                                                                                                                             melements               fromG,          values
                                                                                                                                                                                                       denotedGG=={G
                                                                                                                                                                                                  G,denoted                  {G11
     oose a et of       m elements from G, denoted G = {G1 , ..., Gm                                  }.
                                                                                                     be   implemented            more      eﬃciently         on    logical       qubits           than     process      tomogr
 ore eﬃcientlywith       on logical
                               respect toqubitsthe than Pauli process           tomography.
                                                                  operators 𝑋 , 𝑌         and 𝑍 . The     Theadvantage
                                                                                                                  advantage        ofofRBRBitit    that
                                                                                                                                                 that     ititisis    insensitive            tostate-preparation
                                                                                                                                                                                                   state-preparationand        an
 fofRB  RBititthat
                 thatititisisinsensitive
                                insensitiveto      tostate-preparation
                                                         state-preparationand          andmeasurement
                                                                                               measurement
                                                                                                        The
                                                                                                          1.
                                                                                                           2.    RB   errors
                                                                                                                     errors
                                                                                                               Randomly
                                                                                                                Prepare protocol (SPAM),
                                                                                                                               (SPAM),
                                                                                                                                 choose
                                                                                                                              qudit    goesa
                                                                                                                                       inin      and
                                                                                                                                               and
                                                                                                                                               as
                                                                                                                                                set
                                                                                                                                             state      that
                                                                                                                                                       that
                                                                                                                                                    follows.
                                                                                                                                                      of        ititinsensitive
                                                                                                                                                                        can from
                                                                                                                                                                      can
                                                                                                                                                                 elements
                                                                                                                                                                                           to
                                                                                                                                                                                                 G,   denoted
    oose
    t goes
       in     aset|0i.
            atate follows.
                    of  m elements from G, denoted G = {G1 , ..., Gmbe                                }.2.
                                                                                                      be       Prepare
                                                                                                           implemented
                                                                                                          implemented        quditmore
                                                                                                                                 more       state
                                                                                                                                            eﬃciently
                                                                                                                                           eﬃciently  |0i.
                                                                                                                                                     |0i.   m on
                                                                                                                                                             on       logical
                                                                                                                                                                   logical         qubits
                                                                                                                                                                                 qubits            than
                                                                                                                                                                                                  than       process
                                                                                                                                                                                                           process   Gtomogr
                                                                                                                                                                                                                         =  {G1
                                                                                                                                                                                                                         tomog
more       eﬃcientlyon
 ore eﬃciently            onlogical
                                logicalqubits
                                           qubitsthan    thanprocess processtomography.
                                                                                 tomography.
lol     goes
       goes   as   follows.
               asfollows.                                                                                 TheRB
                                                                                                        The
                                                                                                          1.
                                                                                                          2.   Randomly
                                                                                                               Prepare   protocol
                                                                                                                   RBprotocol    choose
                                                                                                                             qudit      goesa
                                                                                                                                       goes
                                                                                                                                       in       as
                                                                                                                                               as   follows.
                                                                                                                                                setunitary
                                                                                                                                            state    follows.
                                                                                                                                                      of   m elements            ††from G, denoted G = {G1
    oose
 tudit in   a  set
           state
            with    of
                   |0i. mThese
                   unitary  elements
                                G       G †from G, denoted G = {G1 , ..., Gm }.3.
                                      three
                                   j+1 j     for
                                               steps  j  =  0,
                                                           are   ..,   m,   with
                                                                   equivalent      Gto0 =the    m+1 = 11.
                                                                                             Gthree        3.
                                                                                                          steps Acton
                                                                                                               Act     on
                                                                                                                    shown   the
                                                                                                                           the     qudit
                                                                                                                                inqudit
                                                                                                                                     Eq.     with
                                                                                                                                            with
                                                                                                                                           (43).     |0i.
                                                                                                                                                   Theunitary
                                                                                                                                                           algorithm GGj+1 j+1G        forjj=
                                                                                                                                                                                isjj for
                                                                                                                                                                                G    probabilistic,            m,with
                                                                                                                                                                                                    =0,0,..,..,m,    withGG00==
 hoosea
    oose       set   of
                set|0i.
                    ofwe     elements
                            elements
                             get    |𝑥⟩     from
                                         onlyfrom      G,
                                                      if G,0, ..,
                                                            denoted
                                                          thedenoted
                                                                  final      measurement             gives 1.
                                                                                                          1.
                                                                                                          2.
                                                                                                          3.    Randomly
                                                                                                               Randomly
                                                                                                               Prepare
                                                                                                                |1⟩.
                                                                                                               Act     But
                                                                                                                      on the      choose
                                                                                                                                 choose
                                                                                                                             qudit
                                                                                                                               this
                                                                                                                                  quditin    a aset
                                                                                                                                            state
                                                                                                                                       probability
                                                                                                                                            with  set ofof
                                                                                                                                                     |0i.
                                                                                                                                                     unitarymm
                                                                                                                                                             can   elements
                                                                                                                                                                 elements
                                                                                                                                                                       be         †   from
                                                                                                                                                                                    from
                                                                                                                                                                              boosted for        G,G,
                                                                                                                                                                                                  usingdenoted
                                                                                                                                                                                                      denoted a      GG=we
                                                                                                                                                                                                                    with  ={G{G1=
tudit  in
    qudit  state
           with
              with      m
                   unitary
                     POVM m G     Qj+1=Gj
                                          †
                                         {Qfor0 , 11j =Q       0 }, m, where G G=
                                                                            with  =G
                                                                                 we  {G
                                                                                    {G
                                                                                     0  =1, ,G
                                                                                        1     ...,
                                                                                            ...,
                                                                                     typically    GGmtake
                                                                                                m+1  m}.
                                                                                                       =   4.
                                                                                                        }.4.11.QMeasure
                                                                                                               Measure
                                                                                                                 0 = |0ih0|.
                                                                                                                               the
                                                                                                                              the     qudit
                                                                                                                                    qudit       with
                                                                                                                                              with       POVM
                                                                                                                                                       POVM          GQQ  j+1==G{Q{Q
                                                                                                                                                                                  j 0          j1 =QQ
                                                                                                                                                                                         0, ,111           },m,
                                                                                                                                                                                                          ..,
                                                                                                                                                                                                      0,00},    where
                                                                                                                                                                                                               where     weG0 ty
                                                                                                                                                                                                                             typ
                      technique called                 amplitude            amplification          [23].   This
                                                                                                           2.
                                                                                                          2.        technique
                                                                                                                Prepare
                                                                                                               Prepare        qudit
                                                                                                                             qudit     is
                                                                                                                                       ininexplained
                                                                                                                                             state
                                                                                                                                            state     |0i.
                                                                                                                                                     |0i.     in     detail      in
                                                                                                                                                                                  †    Section           VII.
   tit2-4
udit   ininstate
    qudit   state
           with
           many     |0i.
                   |0i.
              withunitary
                     POVMG
                    times    into
                                          †
                                      order  for,to11j =Q
                                                      estimate         wherewith
                                                                             :=weG   typically  m+1take
                                                                                             Gthe      =5.3.
                                                                                                          4.
                                                                                                           5.
                                                                                                           11. Act
                                                                                                               Measure
                                                                                                               Repeat
                                                                                                     probabilityRepeaton   thethe
                                                                                                                             steps
                                                                                                                           steps  qudit2-4 with
                                                                                                                                     qudit
                                                                                                                                      2-4      with
                                                                                                                                             many
                                                                                                                                            many     unitary
                                                                                                                                                       POVM
                                                                                                                                                       times
                                                                                                                                                      times    Qinto G
                                                                                                                                                                    intoQ    =G
                                                                                                                                                                            order
                                                                                                                                                                                {Qj for
                                                                                                                                                                              order    0to,to11j =Q   0,
                                                                                                                                                                                                 estimate
                                                                                                                                                                                                estimate  .., m,
                                                                                                                                                                                                        0 },   where
                                                                                                                                                                                                               pp   with
                                                                                                                                                                                                                 GG:= :=weG  typ
                                                                                                                                                                                                                           Pr(Q
                                                                                                                                                                                                                         Pr(Q    =
                                  Q   =G {Q0               0,0 },.., m,              0 =                      Q  0 = of       obtaining
                                                                                                                        |0ih0|.                outcome             0.
                                                                        pG        Pr(Q                                                                                    j+1                                                 0
                                  j+1     j                                              0 ),                                                                                                                                    0
                                                                                                                                                                                  ††
     udit   with      4.4
                    unitary      Algorithm††
                                              for11jj==Qimplemented          with   on    IBM’s       5    3.
                                                                                                          3.
                                                                                                          4.
                                                                                                          qubit
                                                                                                          5.
                                                                                                           6.  Act
                                                                                                              1.Act
                                                                                                               Measure
                                                                                                                Repeat on
                                                                                                                      on     the
                                                                                                                           the
                                                                                                                      computerthe
                                                                                                                             steps qudit
                                                                                                                                  qudit
                                                                                                                                     qudit
                                                                                                                                      2-4    with
                                                                                                                                            with
                                                                                                                                             many
                                                                                                                                       1-5many with   unitary
                                                                                                                                                     unitary
                                                                                                                                                       POVM
                                                                                                                                                       times         G GQ
                                                                                                                                                                    intoorder= GG
                                                                                                                                                                                {Q
                                                                                                                                                                              order     for
                                                                                                                                                                                      for ,  11j j= =Q 0,
                                                                                                                                                                                                      0,   ..,
                                                                                                                                                                                                          ..,
                                                                                                                                                                                                          },    m,
                                                                                                                                                                                                               m,
                                                                                                                                                                                                               where with
                                                                                                                                                                                                                    with weGGtyp =
udit
  quditwith        unitary
                     POVM
              with times                     for                       wherewith we  typically       take 6.11.
                                                                                                             1 Repeat      steps      1-5             times       into           0totoestimate  estimate                 the
                                                                                                                                                                                                                      i,the     ex0
                                                                                                                                                                                                                              exp
                                                                                                                                                                           j+1                                                 0
                               GG       Gj                  0,00,},
                                                                 ..,..,m,
                                                                       m,           G00 0
                                                                                        ==   GG        ==                                                                                            0 p        hp  :=  Pr(Q
                                                                                                                                                                          j+1                                                 0
     2-4
     1-5   many              intoQ   order
                                     =G
                                    j+1
                                   j+1   {Q j 0to
                                                ,     estimate         phpG  :=
                                                                            G i,
                                                                                   G
                                                                                 the
                                                                                  Pr(Qexpectation
                                                                                           ),  them+1
                                                                                                m+1  probability
                                                                                                           value
                                                                                                              Q  0 = of pofGobtaining
                                                                                                                       |0ih0|.  (averaged      outcome
                                                                                                                                                 over    all   Q
                                                                                                                                                               G). 0
                                                                                                                                                                                  j j                          hp GGGi,

                                                                                                           4.
                                                                                                          4.    Measure
                                                                                                               Measure         the
                                                                                                                              the     qudit
                                                                                                                                     qudit      with
                                                                                                                                               with      POVM
                                                                                                                                                       POVM             Q  Q ==  1.5
                                                                                                                                                                                {Q{Q      ,  ,1
                                                                                                                                                                                              110.5
                                                                                                                                                                                                1    QQ    },
                                                                                                                                                                                                          },    where
                                                                                                                                                                                                               where      we
                                                                                                                                                                                                                         we    ty
                                                                                                                                                                                                                             typ
      qudit
    qudit
     2-4
     1-5      with
           many       POVM
               withtimes
                     POVM
                      Now    into    order
                                  QQ==
                                 we       {Q0
                                         {Q   to
                                      implement0, ,1111 Q
                                                      estimate
                                                            Q0
                                                            the 0},    where
                                                                  }, phpwhere
                                                                      HHL    := we
                                                                          GG i,   we
                                                                                 the typically
                                                                                algorithm
                                                                                  Pr(Qtypically
                                                                                         0 ),  the
                                                                                      expectationon a    25.
                                                                                                      take
                                                                                                     take 6.×  Repeat
                                                                                                     probability
                                                                                                               Q020
                                                                                                           value
                                                                                                              Q    ==    of
                                                                                                                         |0ih0|.
                                                                                                                        |0ih0|.
                                                                                                                     of p
                                                                                                                    system.G
                                                                                                                            stepsFor  2-4
                                                                                                                                      1-5this,
                                                                                                                              obtaining
                                                                                                                               (averaged    many
                                                                                                                                              outcome
                                                                                                                                                 over
                                                                                                                                                  we  times
                                                                                                                                                         all
                                                                                                                                                         choseQG).into
                                                                                                                                                                   0 𝐴 =
                                                                                                                                                                             order 00   to estimate   .00We phpGG i, := the
                                                                                                                                                                                                                         Pr(Q ex0
                                                                                                                                                                                 0.5 1.5
 s1-5       manytimes
       2-4many       times             orderto
                               intoorder          to    estimate                                 the      5.5.
                                                                                                          6.    Repeat
                                                                                                               Repeat
                                                                                                      probability            steps
                                                                                                                            steps     2-4
                                                                                                                                      1-5    many
                                                                                                                                       2-4many          times
                                                                                                                                                      times          intoorder
                                                                                                                                                                  into        order     to       estimatep
                                                                                                                                                                                           toestimate                 :=the
                                                                                                                                                                                                                     :=
                                                                                                                                                                                                                hpGG i,    Pr(Q
                                                                                                                                                                                                                         Pr(Q ex0
     2-4                     into
                      use four        qubits       forestimate
                                                          solvinghp     ppGG
                                                                           the
                                                                           G i,:=the
                                                                             :=   Pr(Qexpectation
                                                                                   Pr(Q00),),–
                                                                                 system        the   probability
                                                                                                           value
                                                                                                 one ancilla,        of
                                                                                                                      onepof
                                                                                                                         of    obtaining
                                                                                                                              obtaining
                                                                                                                               (averaged
                                                                                                                           Gmemory              outcome
                                                                                                                                               outcome
                                                                                                                                                over
                                                                                                                                              and    two all Q   Q00
                                                                                                                                                              register
                                                                                                                                                               G).    . .
                                                                                                                                                                               qubits. For this G
                                                                                       expectation6.value  6.value
                                                                                                                Repeat
                                                                                                               Repeat        steps     1-5many
                                                                                                                                             many       times        into         1 to estimate hp i, the ex
                                                                                                                                                                              order
 s1-5  1-5many
            manytimestimesinto intoorder
                                       orderto
                       case, the eigenvalues of A GG    estimatehp
                                                  toestimate                      theexpectation
                                                                         hp i,i,the
                                                       are 𝜆1 = 1 and 𝜆2 = 2 with G G eigenvectors being
                                                                                   the                               ofofppsteps
                                                                                                                    ≡ |−⟩ and         1-5
                                                                                                                                 (averaged
                                                                                                                               (averaged          over
                                                                                                                                                 over timesallG).
                                                                                                                                                         all      into
                                                                                                                                                                 G).      √1 order to estimate hpGGi, the ex
                                                                                                             2 −1
                           
                           1
                       √1      ≡ |+⟩, respectively. For this system, the three steps of the HHL algorithm, can be performed
                         2 1
                       by the operations shown in Fig. 14. For the controlled rotation, we use a controlled 𝑈 rotation
                       with 𝜃 = 𝜋 for 𝜆1 and 𝜃 = 𝜋/3 for 𝜆2 . This is done by setting 𝐶 = 1 in the Eq. (47). Both 𝜆 and 𝜙
                       are set to zero in these controlled 𝑈 rotations. Although the composer on Quantum Experience
                       does not have this
                                          gate, in IBM Qiskit-sdk-py,
                                                                         we use cu3 function for this purpose. Three cases
                                         1 1 1                1  1
                       are used for b:     ,√            and √      . We post selected the states with |1⟩ in the ancilla qubit.
                                         0     2 −1            2 1
                       The probabilities of these states are normalized such that their sum is one. Measurements with
                       respect to ⟨𝑋 ⟩, ⟨𝑌 ⟩, ⟨𝑍 ⟩ can then be performed to obtain the expectation values. QASM code is
                       output from Qiskit-sdk-py and then uploaded on to IBM Quantum Experience. Figure 15 shows
28                                                                                                Abhijith J., et al.


Algorithm 4 HHL algorithm
     Input:
                            Í
          • The state |𝑏⟩ = 𝑗 𝛽 𝑗 𝑢 𝑗
          • The ability to perform controlled operations with unitaries of the form 𝑒 𝑖𝐴𝑡
     Output:
          • The quantum state |𝑥⟩ such that 𝐴𝑥® = 𝑏. ®
     Procedure:
          Step 1. Perform quantum phase estimation using the unitary transformation 𝑒 𝑖𝐴 . This maps
     the eigenvalues 𝜆 𝑗 into the register in the binary form to transform the system,
                                                     𝑁
                                                    ∑︁
                                |0⟩𝑎 |0⟩𝑟 |𝑏⟩𝑚 →           𝛽 𝑗 |0⟩𝑎 𝜆 𝑗 𝑟 𝑢 𝑗 𝑚 .                              (46)
                                                    𝑗=1
                                                    √︂
                                                               2
         Step 2. Rotate the ancilla qubit |0⟩𝑎 to        1 − 𝐶𝜆2 |0⟩𝑎 + 𝜆𝐶𝑗 |1⟩𝑎 for each 𝜆 𝑗 . This is performed
                                                              𝑗

     through controlled rotation on the |0⟩𝑎 ancilla qubit. The system will evolve to
                               𝑁
                                     √︄                      !
                             ∑︁            𝐶2         𝐶
                                  𝛽𝑗    1 − 2 |0⟩𝑎 +     |1⟩𝑎 𝜆 𝑗 𝑟 𝑢 𝑗 𝑚 .                                    (47)
                              𝑗=1
                                           𝜆𝑗         𝜆𝑗
         Step 3. Perform the reverse of Step 1. This will lead the system to
                              𝑁
                                    √︄                       !
                            ∑︁             𝐶2        𝐶
                                 𝛽𝑗   1 − 2 |0⟩𝑎 +      |1⟩𝑎 |0⟩𝑟 𝑢 𝑗 𝑚 .                                      (48)
                             𝑗=1
                                           𝜆𝑗        𝜆𝑗
         Step 4. Measuring the ancilla qubit will give ,
                                              𝑁      
                                             ∑︁      𝛽𝑗
                                       |𝑥⟩ ≈     𝐶       𝑢𝑗 ,                                                  (49)
                                             𝑗=1
                                                     𝜆𝑗
     if the measurement outcome is |1⟩




the equivalent composer circuit generated from QASM for the measurement in the computational
basis (Z measurement).
    To first test our implementation of the algorithm, we ran nine cases on the local simulator
provided by Qiskit-sdk-py – three b cases and three measurements with respect to the operators 𝑋 ,
𝑌 , 𝑍 , for each b case. The comparison between the theoretical expectation values ⟨𝑋 ⟩, ⟨𝑌 ⟩, ⟨𝑍 ⟩
and the simulator values are shown in Table 3. The simulator expectation values and the theoretical
values match well. This shows that the implementation of the algorithm gives expected results.
Similar expectation values were also seen using the simulator on IBM Quantum Experience instead
of the local simulator. We then ran the circuit on the quantum computer ibmqx4. Fig. 16 shows a
comparison between the simulator results and the results from the ibmqx4 with Z measurement on
the circuit. As can be seen from Fig. 16, the results from the actual run do not give the expected
answer as seen in the simulator results. We remark that recent modifications to the algorithm [24,
121] can in some cases allow for larger scale and more accurate implementations on noisy quantum
computers.
Quantum Algorithm Implementations for Beginners                                                                            29




Fig. 15. Circuit implemented on IBM’s 5-qubit ibmqx4 quantum computer for the case with |𝑏⟩ set to |0⟩ and
with ⟨𝑍 ⟩ measurement. After implementing the circuit in Fig. 14 and setting the coupling map of the ibmqx4
architecture, Qiskit-sdk-py re-arranges the qubits to fit the mapping. This circuit represents the outcome of
the re-arrangement which was implemented on the ibmqx4 quantum computer.


Table 3. Comparison between theoretical and simulator values for the expectation values ⟨𝑋 ⟩, ⟨𝑌 ⟩, ⟨𝑍 ⟩. T
stands for theoretical and S stands for simulator.

                                      |𝑏⟩        T ⟨𝑋 ⟩     S ⟨𝑋 ⟩     T ⟨𝑌 ⟩                   S ⟨𝑌 ⟩   T ⟨𝑍 ⟩   S ⟨𝑍 ⟩
                                      |0⟩        -0.60      -0.60      0.00                     -0.027   0.80     0.81
                                      |+⟩        1.00       1.00       0.00                     -0.06    0.00     0.02
                                      |−⟩        -1.00      -1.00      0.0060                   0.000    -0.02    0.00

                                        IBM QX Simulator                                                     ibmqx4 Run
                         1.0                                                              1.0


                         0.8                                                              0.8




           Probability                                                      Probability
                         0.6                                                              0.6


                         0.4                                                              0.4


                         0.2                                                              0.2


                         0.0                                                              0.0
                                 01         00         00         01                       00 0
                                                                                           00 00
                                                                                              0
                                                                                           00 01
                                                                                              0
                                                                                           00 10
                                                                                              0
                                                                                           00 11
                                                                                              1
                                                                                           00 00
                                                                                              1
                                                                                           00 01
                                                                                              1
                               00 0    00 0          01 0       01 0
                                                                                           00 10
                                                                                              1
                                                                                           10 11
                                                                                              0
                                                                                           10 00
                                                                                              0
                                                                                           10 01
                                                                                              0
                                                                                           10 10
                                                                                              0
                                                                                           10 11
                                                                                              1
                                                                                           10 00
                                                                                              1
                                                                                           10 01
                                                                                              1
                                                                                           10 10
                                                                                              11 1



Fig. 16. Results of the circuit with Z measurement (computational basis measurement) from the actual run
and the simulator on a ibmqx4. 4096 shots were used for both the cases.


5     SHOR’S ALGORITHM FOR INTEGER FACTORIZATION
5.1    Problem definition and background
The integer factorization problem asks, given an integer 𝑁 as an input, to find integers 1 < 𝑁 1, 𝑁 2 <
𝑁 such that 𝑁 = 𝑁 1 𝑁 2 . This problem is hardest when 𝑁 1 and 𝑁 2 are primes with roughly the
same number of bits. If 𝑛 denotes the number of bits of 𝑁 , no algorithm with polynomial
                                                                                       √     in 𝑛 time
complexity is known. The straightforward algorithm that tries all factors from 2 to 𝑁 takes time
polynomial
         in √︃𝑁 , but exponential
                                    in 𝑛. The most efficient known classical algorithm has running
               3 64         2
time 𝑂 exp       9 𝑛(log 𝑛)      [99]. In practice, integers with 1000 or more bits are impossible to
factor using known algorithms and classical hardware. The difficulty of factoring big numbers is
the basis for the security of the RSA cryptosystem [104], one of the most widely used public-key
cryptosystems.
   One of the most celebrated results in quantum computing is the development of a quantum
algorithm for factorization that works in time polynomial in 𝑛. This algorithm, due to Peter Shor
and known as Shor’s algorithm [113], runs in 𝑂 (𝑛 3 log 𝑛) time and uses 𝑂 (𝑛 2 log 𝑛 log log 𝑛) gates.
30                                                                                           Abhijith J., et al.


The first experimental implementation of this algorithm on a quantum computer was reported in
2001, when the number 15 was factored [127]. The largest integer factored by Shor’s algorithm so
far is 21 [88].
   In this section we describe Shor’s algorithm and its implementation on ibmqx4

5.2    Algorithm description
   Reducing factorization to period finding. One way to factor an integer is by using modular
exponentiation. Specifically, let an odd integer 𝑁 = 𝑁 1 𝑁 2 be given, where 1 < 𝑁 1, 𝑁 2 < 𝑁 . Pick
any integer 𝑘 < 𝑁 such that gcd(𝑘, 𝑁 ) = 1, where gcd denotes the greatest common divisor. One
can show that there exists an exponent 𝑝 > 0 such that 𝑘 𝑝 ≡ 1 (mod 𝑁 ). Recall that, by definition,
𝑥 ≡ 𝑦 (mod 𝑚) if and only if 𝑚 divides 𝑥 − 𝑦. Assume that 𝑝 is the smallest such number. If we
find such 𝑝 and 𝑝 is even, then, by the definition of the modulo operation, 𝑁 divides
                                     𝑘 𝑝 − 1 = (𝑘 𝑝/2 − 1) (𝑘 𝑝/2 + 1).
But since the difference between 𝑛 1 = 𝑘 𝑝/2 + 1 and 𝑛 2 = 𝑘 𝑝/2 − 1 is 2, 𝑛 1 and 𝑛 2 have no common
factor greater than 2. Moreover, both numbers are nonzeros by the minimality of 𝑝. Since 𝑁 = 𝑁 1 𝑁 2
was assumed to be odd, then 𝑁 1 is a factor of either 𝑛 1 or 𝑛 2 . Assume 𝑁 1 is a factor of 𝑛 1 . Since 𝑁 1
is also a factor of 𝑁 , then 𝑁 1 divides both 𝑛 1 and 𝑁 and one can find 𝑁 1 by computing gcd(𝑛 1, 𝑁 ).
Hence, if one can compute such a 𝑝, one can find the factors of 𝑁 efficiently as gcd can be computed
in polynomial time.
   In order to find 𝑝, consider the modular exponentiation sequence 𝐴 = 𝑎 0, 𝑎 1, . . . , where 𝑎𝑖 = 𝑘 𝑖
(mod 𝑁 ). Each 𝑎𝑖 is a number from the finite set {0, . . . , 𝑁 − 1}, and hence there exists indices 𝑞
and 𝑟 such that 𝑎𝑞 = 𝑎𝑟 . If 𝑞 and 𝑟 are the smallest such indices, one can show that 𝑞 = 0 and 𝐴 is
periodic with period 𝑟 . For instance, for 𝑁 = 15 and 𝑘 = 7, the modular exponentiation sequence
is 1, 7, 4, 13, 1, 7, 4, 13, 1, . . . with period 4. Since the period 4 is an even number, we can apply the
above idea to find
      74 mod 15 ≡ 1 ⇒ 74 − 1 mod 15 ≡ 0 ⇒ (72 − 1) (72 + 1) mod 15 ≡ 0 ⇒ 15 divides 48 · 50,
which can be used to compute the factors of 15 as gcd(48, 15) = 3 and gcd(50, 15) = 5.
   Finding the period of the sequence 𝐴 is, however, not √ classically easier than directly searching for
factors of 𝑁 , since one may need to check as many as 𝑁 different values of 𝐴 before encountering
a repetition. However, with quantum computing, the period can be found in polynomial time using
the Quantum Fourier Transform (QFT). The QFT operation was introduced earlier during our
discussion of phase estimation.
   The property of the QFT that is essential for the factorization algorithm is that it can “compute”
the period of a periodic input. Specifically, if the input vector 𝑋 is of length 𝑀 and period 𝑟 , where
𝑟 divides 𝑀, and its elements are of the form
                                          (√︁
                                              𝑟 /𝑀 if 𝑖 mod 𝑟 ≡ 𝑠
                                    𝑥𝑖 =
                                            0         otherwise
                                 Í            Í
                                    𝑀                𝑀
for some offset 𝑠 < 𝑟 , and Q𝐹𝑇     𝑖=0 𝑥𝑖 |𝑖⟩ = 𝑖=0 𝑦𝑖 |𝑖⟩, then
                                         ( √
                                          1/ 𝑟 if 𝑖 mod 𝑀/𝑟 ≡ 0
                                  𝑦𝑖 =
                                          0        otherwise
                                                                          √︁            √
i.e., the output has nonzero values at multiples of 𝑀/𝑟 (the values 𝑟 /𝑀 and 1/ 𝑟 are used for
normalization). Then, in order to factor an integer, one can find the period of the corresponding
Period-finding algorithm
Quantum Algorithm Implementations for Beginners                                                                          31



•
modular exponentiation sequence using QFT, if one is able to encode
       Givenstate
of a quantum     a (the
                    coprime        𝑘 of 𝑁, find 𝑝 s.t. 𝑘 : ≡ 1 mod 𝑁
                         input to QFT).
                                                                        its period in the amplitudes
   S. period-finding
   A  Dasgupta, C.H.     Papadimitriou,
                     circuit               and
                             for solving the    U.V. Vazirani
                                             integer factorization problem is shown in Fig 17 [39].                                327
•      Period-finding
The first QFT on               circuitan equal superposition of the qubits from 𝐴, i.e., the resulting
                  register 𝐴 produces
   Figure 10.6 Quantum factoring.
                                                                                                                          𝑘"𝑀/𝑝

     register 𝐴
                                                                                                               measure
                                                                                                                          𝑘&𝑀/𝑝 GCD
            0                0             QFTM                                              QFTM                        measure
      𝑚 qubits
                                                                                                                            .. .

                                                                                                                          𝑘k 𝑀/𝑝
                                                                     f(i) =
                                                                   i
                                                                  x mod N

     register 𝐵
                  𝑛 qubits
            0                0




                             Fig. 17. Illustration of the period-finding
                                                              "          circuit, where 𝑚 ="2𝑛 and 𝑀 #= 2𝑚 .
                                                !M−1 "            #            !M−1 "
                                             √1
                                                 a=0 B,0
                                                                            √1
                                                                                a=0
                                                                                      B,G B
                                              M                              M
state is
                                                                  𝑀
                                              1 ∑︁
                                             √       |𝑖, 0⟩ .
       Let n = log N be the number of bits    𝑀 𝑖=0of the input N . The running time of the algorithm
   is is a
Next  dominated
           modularby the 2    log N =circuit
                     exponentiation          repetitions
                                       O(n) that computes   of the
                                                                step 3. Since
                                                                   function    modular
                                                                            𝑓 (𝑖) =      exponentiation
                                                                                    𝑥 𝑖 (mod 𝑁 ) on the takes
   O(n )
second  3  steps (as
         register. Thewe  saw instate
                       resulting  Section
                                      is 1.2.2) and the quantum Fourier transform takes O(n 2 ) steps,
   the total running time for the quantum𝑀factoring algorithm is O(n 3 log n).
                                             1 ∑︁
                                           √       |𝑖, 𝑓 (𝑖)⟩ .
                                             𝑀 𝑖=0
Before we apply the next QFT transform, we do a measurement of register 𝐵. (By the principle of
                                                            UNCLASSIFIED
deferred measurement [92] and due to the fact that register 𝐴 and 𝐵 don’t interact from that point
on, we don’t have to actually implement the measurement, but it will help to understand the final
output.) If the value measured is 𝑠, then the resulting state becomes
                                                                 𝑀
                                                             1  ∑︁
                                                          √︁        |𝑖, 𝑠⟩ ,
                                                            𝑀/𝑟 𝑖=0
                                                                  𝑓 (𝑖)=𝑠

where 𝑟 is the period of 𝑓 (𝑖). In particular, register 𝐴 is a superposition with equal non-zero
amplitudes only of |𝑖⟩ for which 𝑓 (𝑖) = 𝑠, i.e., it is a periodic superposition with period 𝑟 . Given the
property of QFT, the result of the transformation is the state
                                                𝑟
                                           1 ∑︁
                                         √          |𝑖 (𝑀/𝑟 ), 𝑠⟩ .
                                            𝑟 𝑖=0
Hence, the measurement of register 𝐴 will output a multiple of 𝑀/𝑟 . If the simplifying assumption
that 𝑟 divides 𝑀 is not made, then the circuit is the same, but the classical postprocessing is a bit
more involved [92].
  Period finding can also be viewed as a special case of phase estimation. The reader may refer
Nielsen and Chuang [92] for this perspective on period finding.
32                                                                                            Abhijith J., et al.


5.3    Algorithm implemented on IBM’s 5-qubit computer
We implemented the algorithm on ibmqx4, a 5-qubit quantum processor from the IBM Quantum
Experience, in order to factor number 15 with 𝑥 = 11. The circuit as described on Figure 17
requires 12 qubits and 196 gates, too large to be implemented on ibmqx4. Hence, we used an
optimized/compiled version from [127] that uses 5 qubit and 11 gates (Fig 18).

                   |0⟩ 𝐻                       𝑃 ( 𝜋2 )   𝐻                   •

                   |0⟩ 𝐻                 𝐻        •                •

                   |0⟩ 𝐻       •    •                           𝑃 ( 𝜋4 )   𝑃 ( 𝜋2 )

                   |0⟩
                   |0⟩

                         Fig. 18. Circuit for Shor’s algorithm for 𝑁 = 15 and 𝑥 = 11.

  The results from the measurements are shown on Figure 19.
  The periods found by the simulator are 𝑝 = 0, which is ignored as a trivial period, and 𝑝 = 4,
which is a good one. Since 𝑀 = 8, we can conclude that 𝑟 divides 𝑀/𝑝 = 8/4 = 2, hence 𝑟 = 2. Then
15 divides
                         (𝑥 𝑟 − 1) = (112 − 1) = (11 − 1) (11 + 1) = 10 · 12.
By computing gcd(15, 10) = 5 and gcd(15, 12) = 3, we find the factors of 15.
  The output from ibmqx4 finds the same periods 0 and 4 with the highest probabilities, but
contains much more noise.

6     MATRIX ELEMENTS OF GROUP REPRESENTATIONS
6.1    Problem definition and background
In this section we will discuss another quantum algorithm that makes use of the QFT operation. In
this section we will also introduce a subroutine called the Hadamard test, which lets us compute
matrix elements of unitary operators. But first, we will require some knowledge of group theory to
understand the problem being tackled here. This section follows the work of Jordan in Ref. [73].
   A Group (𝐺, ·) or (𝐺) is a mathematical object defined by its elements (𝑔1 , 𝑔2 , . . . ) and an operation
between elements (·), such that these four properties are satisfied.
   (1) Closure: for any two group elements, the defined group operation produces another element,
       which belongs to the group (for ∀ 𝑔𝑖 ,𝑔 𝑗 ∈ 𝐺, 𝑔𝑖 · 𝑔 𝑗 = 𝑔𝑘 ∈ 𝐺).
   (2) Associativity: for ∀ 𝑔𝑖 , 𝑔 𝑗 , 𝑔𝑚 ∈ 𝐺, 𝑔𝑖 · 𝑔 𝑗 · 𝑔𝑚 = 𝑔𝑖 · 𝑔 𝑗 · 𝑔𝑚 .
   (3) Identity element: 𝑒 ∈ 𝐺, such that 𝑒 · 𝑔𝑖 = 𝑔𝑖 · 𝑒 = 𝑔𝑖 .
   (4) Inverse element: for ∀ 𝑔𝑖 ∈ 𝐺, there exists 𝑔𝑝 , such that 𝑔𝑖 · 𝑔𝑝 = 𝑔𝑝 · 𝑔𝑖 = 𝑒.
   A group with a finite amount of elements 𝑛 is called a finite group with order 𝑛, while a group
with an infinite amount of elements is an infinite group. In this section, we will discuss quantum
algorithms to solve certain problems related to finite groups. As before, we will also implement
them on the IBM machines. Some examples of groups are given below.
   Example 1A. Abelian group 𝐴𝑛 with 𝑛 elements: 0, 1, . . . , 𝑛 − 1, and the group operation addition
modulo 𝑛: 𝑔𝑖 · 𝑔 𝑗 = (𝑖 + 𝑗)mod(𝑛). For instance, for 𝑛 = 3: 𝑎 0 = 0, 𝑎 1 = 1, 𝑎 2 = 2. Then, 𝑎 2 · 𝑎 2 = 4
mod(3) = 1 = 𝑎 1 , 𝑎 2 · 𝑎 1 = 3 mod(3) = 0 = 𝑎 0 , etc. The identity element is 𝑎 0 = 0 and its inverse
is itself. For all other elements the inverse element is, 𝑎𝑖−1 = 𝑎𝑛−𝑖 . This group is called Abelian or
Quantum Algorithm Implementations for Beginners                                                         33




  Fig. 19. Output from the circuit from Figure 18 implemented on the simulator (left) and ibmqx4 (right).



commutative, because in addition to the four group properties, it has a property of commutativity:
𝑎𝑖 · 𝑎 𝑗 = 𝑎 𝑗 · 𝑎𝑖 for ∀ 𝑎𝑖 , 𝑎 𝑗 ∈ 𝐴𝑛 .
   Example 1S. Symmetry group 𝑆𝑛 with 𝑛! group elements, each is a permutation of 𝑛 objects:
[1, 2.., 𝑛], [2, 1.., 𝑛], . . . , [𝑛, 𝑛 − 1.., 2, 1]. Consequent application of two permutations is a group
operation. For instance, for group 𝑆 2 : (𝑒,𝑝) we have two objects 𝑎 and 𝑏. The identity element 𝑒 is
no permutation: 𝑎𝑏 → 𝑎𝑏, while one permutation 𝑝 is the second group element: 𝑎𝑏 → 𝑏𝑎. Then,
𝑝 · 𝑝 = 𝑒, and 𝑝 −1 = 𝑝. Only 𝑆 1 and 𝑆 2 are Abelian groups. For 𝑛 ≥ 3, 𝑆𝑛 are not commutative. Let
us write elements of group 𝑆 3 as a permutation of elements 123 in the next order: [123] → [123],
[231], [312], [213], [132], [321]. Then 𝑠 4 · 𝑠 2 = 𝑠 6 , while 𝑠 2 · 𝑠 4 = 𝑠 5 .
   While group definition is quite simple, it is not straightforward how to operate with group
elements in general, especially when defined operations between them is not trivial and/or the
group order, 𝑛, is large. In this case, it is helpful to apply the representation theory to the group.
The idea is simple: if we can map a group of unknown objects with nontrivial operations to the
group of known objects with some trivial operations, we can gain some information about the
unknown group. In general, we introduce a function applied to a group element: 𝜌 (𝑔𝑖 ), which does
34                                                                                            Abhijith J., et al.


this mapping between two groups. Such function defines the group representation of 𝐺 if for ∀ 𝑔𝑖 ,
𝑔 𝑗 ∈ 𝐺, 𝜌 (𝑔𝑖 ) ∗ 𝜌 (𝑔𝑖 ) = 𝜌 (𝑔𝑖 · 𝑔 𝑗 ), where (∗) can be a different operation from (·).
    Example 2A. Representation of Abelian group 𝐴𝑛 : 𝑎 𝑗 → 𝜌 (𝑎 𝑗 ) = 𝑒 𝑖2𝜋 𝑗/𝑁 , where the original
operation (+mod(𝑛)) is substituted by the new operation of multiplication. Note that the group 𝑆 2
can be represented in the same way as 𝐴2 .
    Example 2S. Representation of group 𝑆 3 : 𝑠 𝑗 → 𝜌 (𝑠 𝑗 ) = 1, where the original operation is again
substituted by the new operation of multiplication. Such representation of the group 𝑆 3 is trivial,
since it does not carry any information about the group, however it satisfies the definition of
the group representation. Moreover, [1,1, . . . ] is a trivial representation for any group. Another
representation of group 𝑆 3 is, [1, 1, 1, −1, −1, −1] → [𝑠 1, 𝑠 2, . . . , 𝑠𝑛 ], where we map odd permutations
to −1 and even permutations to 1 . While it carries more information about the initial group than
the trivial representation, it does not imply that the group 𝑆 3 is not Abelian. One cannot construct
a one-dimensional representation for group 𝑆 3 which would retains all its properties. The smallest
equivalent representation for 𝑆 3 is two-dimensional. The multidimensional representations can be
easy understood when represented by matrices.
    Most useful representations are often ones which map a group to a set of matrices. When 𝜌 (𝑔) is
a 𝑑 𝜌 × 𝑑 𝜌 matrix, the representation is referenced as a matrix representation of the order 𝑑 𝜌 , while
(∗) is the operation of matrix multiplication. All representations of finite group can be expressed
as unitary matrices given an appropriate choice of basis. To prove the last fact, we introduce a
particular representation called the regular representation.
    The regular representation of a group of 𝑁 elements is a matrix representation of order 𝑁 .
We will explain the construction of the regular representation using the Dirac notation. First, we
associate with each element of the group 𝑔𝑖 a ket |𝑔𝑖 ⟩. This ket could simply be the basis state |𝑖⟩,
since the elements of the group are numbered. This ensures that the kets associated with different
group elements are orthonormal by construction, 𝑔𝑖 |𝑔 𝑗 = 𝛿𝑖 𝑗 . This also ensures that the identity
                                     Í𝑁
operator can be expressed as 𝑖=1             |𝑔𝑖 ⟩ ⟨𝑔𝑖 | . The regular representation of 𝑔𝑘 is then given by,


                                                      𝑁
                                                     ∑︁
                                        𝑅(𝑔𝑘 ) =           𝑔𝑘 · 𝑔 𝑗 𝑔 𝑗 .                                  (50)
                                                     𝑗=1


   The matrix elements of this representation are, 𝑅𝑖 𝑗 (𝑔𝑘 ) ≡ 𝑔𝑖 |𝑅(𝑔𝑘 )|𝑔 𝑗 = ⟨𝑔𝑖 |𝑔𝑘 · 𝑔 𝑗 ⟩. From the
defining properties of a group it can be easily seen that multiplying every element in the group
by the same element just permutes the elements of the group. This means that 𝑅(𝑔𝑘 ) matrices are
always permutation matrices and are hence unitary. We can prove that the regular representation
is a representation using simple algebra,


                                             ∑︁ 𝑁
                                              𝑁 ∑︁
                         𝑅(𝑔𝑘 ) · 𝑅(𝑔𝑚 ) =             |𝑔𝑘 · 𝑔𝑖 ⟩ ⟨𝑔𝑖 |𝑔𝑚 · 𝑔 𝑗 ⟩ 𝑔 𝑗 ,
                                             𝑖=1 𝑗=1
                                             ∑︁ 𝑁
                                              𝑁 ∑︁
                                         =             𝑔𝑘 · 𝑔𝑚 · 𝑔 𝑗 ⟨𝑔𝑖 |𝑔𝑚 · 𝑔 𝑗 ⟩ 𝑔 𝑗 ,
                                             𝑖=1 𝑗=1
                                              𝑁
                                             ∑︁
                                         =         𝑔𝑘 · 𝑔𝑚 · 𝑔 𝑗 𝑔 𝑗 = 𝑅(𝑔𝑘 · 𝑔𝑚 ).                        (51)
                                             𝑗=1
Quantum Algorithm Implementations for Beginners                                                                                  35


   Here we used orthogonality: ⟨𝑔𝑖 |𝑔𝑚 · 𝑔 𝑗 ⟩ = 1 only if |𝑔𝑖 ⟩ = 𝑔𝑚 · 𝑔 𝑗 and 0 otherwise, which
allowed us to swap these two states. Then, we used the same fact to calculate the sum over 𝑖. Below
we give some explicit examples of regular representations.
   Example 3A. Regular representation of the Abelian group 𝐴4 , where each matrix element is
calculated using the result derived above 𝑅𝑖 𝑗 (𝑎𝑘 ) = ⟨𝑎𝑖 |𝑎𝑘 · 𝑎 𝑗 ⟩:

           1     0       0       0               0   0    0    1                0      0   1    0                0     1    0     0
          ­0     1       0       0®             ­1   0    0    0®              ­0      0   0    1®             ­0      0    1     0®
          ©                       ª             ©                ª             ©                 ª             ©                   ª
𝑅(𝑎 0 ) = ­                       ® , 𝑅(𝑎 1 ) = ­                ® , 𝑅(𝑎 2 ) = ­                 ® , 𝑅(𝑎 3 ) = ­                   ®.
          ­0     0       1       0®             ­0   1    0    0®              ­1      0   0    0®             ­0      0    0     1®
          «0     0       0       1¬             «0   0    1    0¬              «0      1   0    0¬             «1      0    0     0¬
                                                                                                                                (52)
Commutative property is conserved: 𝑅(𝑎𝑖 ) · 𝑅(𝑎 𝑗 ) = 𝑅(𝑎 𝑗 ) · 𝑅(𝑎𝑖 ).
   Example 3S. Regular representation of the group 𝑆 3 , where we use the same order of permutations
introduced above ([123] → [123], [231], [312], [213], [132], [321])

             1       0       0    0   0   0                0    0   1   0    0      0                 0   1   0    0    0    0
            ­0       1       0    0   0   0®              ­1    0   0   0    0      0®              ­0    0   1    0    0    0®
            ©                               ª             ©                           ª             ©                          ª
            ­0       0       1    0   0   0®              ­0    1   0   0    0      0®              ­1    0   0    0    0    0®
            ­                               ®             ­                           ®             ­                          ®
  𝑅(𝑠 1 ) = ­                               ® , 𝑅(𝑠 2 ) = ­                           ® , 𝑅(𝑠 3 ) = ­                          ®,
            ­0       0       0    1   0   0®              ­0    0   0   0    0      1®              ­0    0   0    0    1    0®
            ­0       0       0    0   1   0®              ­0    0   0   1    0      0®              ­0    0   0    0    0    1®
            ­                               ®             ­                           ®             ­                          ®

            «0       0       0    0   0   1¬              «0    0   0   0    1      0¬              «0    0   0    1    0    0¬
                                                                                                                               (53)

            0     0      0       1    0   0                0   0    0   0   1    0                0       0   0   0    0    1
           ­0     0      0       0    0   1®              ­0   0    0   1   0    0®              ­0       0   0   0    1    0®
           ©                                ª             ©                        ª             ©                            ª
           ­0     0      0       0    1   0®              ­0   0    0   0   0    1®              ­0       0   0   1    0    0®
           ­                                ®             ­                        ®             ­                            ®
 𝑅(𝑠 4 ) = ­                                ® , 𝑅(𝑠 5 ) = ­                        ® , 𝑅(𝑠 6 ) = ­                            ®.
           ­1     0      0       0    0   0®              ­0   1    0   0   0    0®              ­0       0   1   0    0    0®
           ­0     0      1       0    0   0®              ­1   0    0   0   0    0®              ­0       1   0   0    0    0®
           ­                                ®             ­                        ®             ­                            ®

           «0     1      0       0    0   0¬              «0   0    1   0   0    0¬              «1       0   0   0    0    0¬
                                                                                                                               (54)
   Now we can finally explain the problem of calculating matrix elements of the group representa-
tions, which is equivalent to the problem of calculating an expectation value of an operator A in
respect to the state |𝜓 ⟩ in quantum mechanics: ⟨A⟩ = ⟨𝜓 | A |𝜓 ⟩.
   Example 4A. Calculating matrix elements of the regular representation of the element 𝑎 2 from
the Abelian group 𝐴4 with respect to the state 𝜓 13 which is the equal superposition of |𝑎 1 ⟩ and |𝑎 3 ⟩.
In operator form we find:
                                     𝑁 −1
                                                           !
                     ⟨𝑎 1 | + ⟨𝑎 3 | ∑︁                      |𝑎 1 ⟩ + |𝑎 3 ⟩ ⟨𝑎 3 |𝑎 2 · 𝑎 1 ⟩⟨𝑎 1 |𝑎 1 ⟩ ⟨𝑎 1 |𝑎 2 · 𝑎 3 ⟩⟨𝑎 3 |𝑎 3 ⟩
⟨𝜓 12 | a2 |𝜓 12 ⟩ =       √              |𝑎 2 · 𝑎𝑖 ⟩⟨𝑎𝑖 |         √        =                            +                             = 1.
                             2       𝑖=0                             2                    2                            2
                                                                                                                                (55)
    It is quite obvious that if a quantum computer is capable of finding expectation values of a
unitary operator, it will be able to solve the problem of finding the matrix elements of the regular
representation of a group element. This will consist of, at least, two stages: the first stage is the
state preparation, and the second is applying the unitary operator of the regular representation to
that state. The unitary operator of the regular representation of an element of any group 𝐺𝑛 can be
created using a combination of only two type of operations: qubit flip (|0⟩ → |1⟩) and qubit swap
( 𝑞 𝑗 𝑞𝑖 → 𝑞𝑖 𝑞 𝑗 ).
36                                                                                         Abhijith J., et al.




                         Fig. 20. Schematic diagram for the quantum algorithm


   Up to this point, we have only talked about the regular representation. The regular representation
is quite convenient, it is straightforward to find for any group, it carries all the information about the
group, and a corresponding unitary operator is easy to construct using standard quantum circuits.
However, for groups with a large number of elements, it requires matrix multiplication between large
matrices. So for many applications, instead of regular representations one is interested in what are
known as irreducible representations, which are matrix representations that cannot be decomposed
into smaller representations. Or in other words, every matrix representation (including the regular
representation) can be shown to be equivalent to a direct sum of irreducible representations, up to
a change of basis. This lets us reduce the representation theory of finite groups into the study of
irreducible representations. The importance of irreducible representations in group theory cannot
be overstated. The curious reader may refer these notes by Kaski [74].
   A result from group theory ensures that the direct sum of all irreducible representations (each
has different dimensions 𝑑 𝜌 in general) where each irreducible representation appears exactly 𝑑 𝜌
times is a block diagonal 𝑁 × 𝑁 matrix (the group has 𝑁 elements). The Fourier transform pair
over this group representation can be introduced by decomposing each irreducible representation
over the group elements and vice versa. Moreover, the above defined direct sum of all irreducible
representations can be decomposed as a regular representation conjugated by the direct and inverse
Fourier transform operators [73]. This result lets us find the the matrix elements of the irreducible
representations given the ability to implement the regular representation.

6.2   Algorithm description
In this section we will describe an algorithm to find the matrix elements of irreducible represen-
tations of a group given the ability to apply its regular representations to a quantum register in
a controlled fashion. The quantum algorithm calculating matrix elements ⟨𝜓 | U1 |𝜓 ⟩ of a unitary
operator U1 is known as the Hadamard test, which is illustrated on Fig. 20.
   The ancilla qubit should be prepared as |0⟩−𝑖
                                              √
                                                 |1⟩
                                                     to calculate the imaginary parts of the matrix ele-
                                                 2
                                                                                            |𝜓 ⟩+𝑈 |𝜓 ⟩ 2
ment. From the pseudocode, we can see that the probability of measuring |0⟩ is 𝑃0 = ||          √      || =
                                                                                                  2
1+𝑅𝑒 ⟨𝜓 |𝑈 |𝜓 ⟩
      2         . Hence, we find: 𝑅𝑒 ⟨𝜓 | 𝑈 |𝜓 ⟩ = 2𝑃0 − 1. The reader is encouraged to work out the same
steps for the imaginary part as well.
   With the Hadamard test algorithm, the problem of calculating matrix elements of an arbitrary
unitary operator is reduced to the problem of effectively implementing it as a controlled gate. For
the regular representation of any group 𝑈 0 , where unitary operator is an 𝑁 x 𝑁 square matrix with
only one non-zero element equal to 1 in each row, this implementation can be done for any group
as a combination of 𝐶𝑁𝑂𝑇 and 𝑍 gates.
Quantum Algorithm Implementations for Beginners                                                      37


Algorithm 5 Hadamard test
  Input:
      • The controlled unitary 𝐶𝑈 .
      • Input state |0⟩|𝜓 ⟩.
  Output:
      • An estimate for the real part of ⟨𝜓 |𝑈 |𝜓 ⟩
  Procedure:
      Step 1. Apply 𝐻 to the ancilla. This produces the state,
                                           |0⟩ + |1⟩
                                              √      |𝜓 ⟩
                                                2
      Step 2. Apply 𝐶𝑈 controlled on the ancilla. This produces the state,

                                            |0⟩ |𝜓 ⟩ + |1⟩ 𝑈 |𝜓 ⟩
                                                     √
                                                       2
          Step 3. Apply 𝐻 to the ancilla again. This gives,

                                 |0⟩ (|𝜓 ⟩ + 𝑈 |𝜓 ⟩) + |1⟩ (|𝜓 ⟩ − 𝑈 |𝜓 ⟩)
                                                    √
                                                      2
          Step 4. Measure the ancillary qubit. Repeat to estimate the probability of obtaining |0⟩ and
  |1⟩ .


   At the same time solutions for the direct sum of all irreducible representations 𝑈 1 , which can
be decomposed as 𝑈 1 (𝑔) = 𝐹 1𝑈 0 (𝑔−1 )𝐹 1−1 , exists for any group whose Fourier transform over that
group can be effectively implemented using quantum circuits. Quantum circuits for the Fourier
transform are already known for the symmetric group 𝑆 (𝑛) [13], the alternating group 𝐴𝑛 , and some
Lie groups: 𝑆𝑈 (𝑛), 𝑆𝑂 (𝑛) [10], while solutions for other groups, hopefully, will be found in the
future. For Abelian groups this Fourier transform implementation can be efficiently done using the
QFT circuit that was discussed in the earlier sections. For non-Abelian groups the implementation
is trickier and efficient implementations are not universally known.

6.3   Algorithm implemented on IBM’s 5-qubit computer
The actual gate sequence that we implemented on IBM’s 5-qubit computer (ibmq_essex) and IBM’s
quantum simulator to find matrix elements of the regular representation of the second element of
the group 𝑆 2 is shown in Fig. 21. The matrix for this representation is simply a 𝑋 gate. Hence, we
have to use one CNOT gate and two Hadamard gates, plus some gates to prepare state |𝜓 ⟩ from
the state |00⟩. We mapped the ancilla qubit to the actual machine 𝑞 1 qubit instead of 𝑞 0 , because of
the machine architecture, where the first qubit can control the zero qubit but not vice versa. We
could have used the original qubit sequence as in Fig. 20, by realizing the CNOT gate as a swapped
CNOT and four Hadamard gates, but this would add more gates to the circuit and potentially more
computational errors rather than just a virtual swap of the qubits.
   For the irreducible representation of the same element of the group 𝐴2 , the element is represented
by the 𝑍 gate. Hence the Hadamard test requires implementing a controlled-𝑍 gate, which is not
available as an actual gate on the IBM Quantum Experience. However, it can be constructed
using two Hadamard and one 𝐶𝑁𝑂𝑇 gates as shown in Fig. 22. Notice that the Hadamard gate
is actually the Fourier transform operator over group 𝑆 2 and 𝐴2 , while the 𝑋 gate is a regular
representation operator, as we mentioned earlier. Hence, such controlled-𝑍 gate representation
38                                                                                                  Abhijith J., et al.




Fig. 21. Actual circuit implemented on IBM’s 5-qubit computer for calculating matrix elements of the regular
representation for the second element of the group 𝑆 2 and 𝐴2 in respect to the state |0⟩ on the left and
 |0⟩+ |1⟩
   √      on the right. The expected probabilities to find a final state in the ground state are (1 + 0)/2 = 0.5 and
      2
(1 + 1)/2 = 1 respectively. The results of the 1024 runs on the actual chip (on the top) and the simulator (on
the bottom) are presented on the right side of each circuit.




Fig. 22. Actual circuit implemented on IBM’s 5-qubit computer for calculating matrix elements of the direct
sum of the irreducible representations for the second element of the group 𝑆 2 and 𝐴2 with respect to the
state |0⟩ on the left and |1⟩ on the right. The expected probabilities to find a final state in the ground state
are (1 + 1)/2 = 1 and (1 − 1)/2 = 0 respectively. The results of the 1024 runs on the actual chip (on the top)
and the simulator (on the bottom) are presented on the right side of each circuit.



is in fact the decomposition of the irreducible representation to the regular representation using
Fourier transform over that group.

7     QUANTUM VERIFICATION OF MATRIX PRODUCTS
7.1       Problem definition and background
Matrix multiplication is one of the most important linear algebra subroutines. Most scientific
computing algorithms use matrix multiplication in one form or another. Therefore, the compu-
tational complexity of matrix multiplication is a subject of intense study. For two 𝑛 × 𝑛 matrices
the computational complexity of the naive matrix multiplication algorithm is 𝑂 (𝑛 3 ) A faster algo-
rithm for matrix multiplication implies a considerable performance improvement for a variety of
computational tasks. Strassen [120] first showed that two 𝑛 × 𝑛 matrices can be multiplied in time
𝑂 (𝑛 2+𝛼 ) (𝛼 < 1). The best known algorithm to date with 𝛼 ≈ 0.376 was found by Coppersmith and
Winnograd [37]. Despite that, it remains an open problem to determine the optimal value of 𝛼. The
so-called problem of matrix verification is defined as, verifying whether the product of two 𝑛 × 𝑛
Quantum Algorithm Implementations for Beginners                                                            39


matrices is equal to a third one. So far the best classical algorithm can do this with high probability
in time proportional to 𝑛 2 [53].
   Ref. [5] was the first to study matrix verification for quantum computation. The authors use a
quantum algorithm based on Grover’s algorithm to verify whether two 𝑛 × 𝑛 matrices equal a third
in time 𝑂 (𝑛 7/4 ), thereby improving the optimal classical bound of Ref. [53]. Ref. [26] presents a
quantum algorithm that verifies a product of two 𝑛 × 𝑛 matrices over any integral  √      domain with
bounded error in worst-case time 𝑂 (𝑛 5/3 ) and expected time 𝑂 (𝑛 5/3 /𝑚𝑖𝑛(𝑤, 𝑛) 1/3 ), where 𝑤 is
the number of wrong entries. This further improves the time performance 𝑂 (𝑛 7/4 ) from Ref. [5].

7.2   Algorithm description
We briefly sketch the quantum algorithm from Ref. [5]. The presentation here follows from Ref. [119].
Before we discuss this algorithm we introduce the concept of amplitude amplification.
   Many real world algorithms are probabilistic, i.e., independent runs of the algorithm on the same
input will not necessarily give the same output. This is because the algorithm uses some source of
randomness during its execution. Most quantum algorithms are probabilistic owing to the inherent
randomness present in quantum mechanics.
   Suppose that the job of our probabilistic classical/quantum algorithm is to return one of a specific
set of states. Assume that we also have at our disposal an oracle that can identify the members of
this set from other states. An example of this would be polynomial root finding. The set of states in
this case would correspond to the roots of the polynomial. Our algorithm should return one of the
roots of the polynomial and we can verify if an output is a root by plugging it in to the polynomial.
   Obviously the algorithm is good only if it can return a state that is a member of this set with
high probability. But how high of a success probability is good enough? For practical reasons we
would like the probability of success to be a constant. That is, it should be a value independent of
the problem size and other parameters in the problem. Any constant value between 0 and 1 would
work here. The value 23 is usually used in literature.
   But often algorithms won’t succeed with constant probability and their success provability will
diminish with growing input size. In that case, how can we boost the success probability to the
desired level? The classical answer to this question is to repeatedly run the algorithm until we
succeed, i.e., till the algorithm outputs a state from the specific set of states that we want. If the
algorithm initially had a success probability of 𝑝, after 𝑂 ( 𝑝1 ) repetitions we are guaranteed to find
the desired state with constant probability.
   For quantum algorithms we can do something better. Let 𝑈 be a quantum algorithm and suppose
that we want this algorithm to return a state from the subspaceÍ        spanned by the orthogonal states,
{|𝑢𝑖 ⟩}. Let 𝑃 be the projection operator onto this subspace, 𝑃 = 𝑖 |𝑢𝑖 ⟩ ⟨𝑢𝑖 | . The oracle we have is
then, 𝑂 = 𝐼 − 2𝑃. This oracle will mark the states in the desired subspace. The success probability of
our algorithm is 𝑝 = 0 . . . 0|𝑈 † 𝑃𝑈 |0 . . . 0 . In this scenario we can use amplitude amplification to
boost the success probability to a constant with only 𝑂 ( √1𝑝 ) repetitions. This is a quadratic speedup
over the classical strategy.
   Essentially, amplitude amplification is a generalization of Grover search described in Section II .
In Grover search we repeatedly apply the Grover operator, 𝐺 = (2 |𝜓 ⟩ ⟨𝜓 | − 𝐼 )𝑂, where |𝜓 ⟩ is the
uniform superposition state. Amplitude amplification uses a more general operator,

                                        𝐺𝑈 = 𝑈 (2 |0⟩ ⟨0| − 𝐼 )𝑈 †𝑂.                                     (56)
  To get the desired result we apply this to the 𝑈 |0 . . . 0⟩ state 𝑂 ( √1𝑝 ) times. Notice that the original
Grover search is a specific case of amplitude amplification with 𝑈 = 𝐻 ⊗ . . . ⊗ 𝐻 . In that case, the
40                                                                                        Abhijith J., et al.

                                                                                        √
probability of getting the marked state in |𝜓 ⟩ is 𝑁1 so we run the algorithm for 𝑂 ( 𝑁 ) steps. The
reader is referred to Ref. [23] for more details on amplitude amplification.
   The matrix product verification procedure uses amplitude amplification as its outer loop. The
algorithm first splits the full matrix verification problem into smaller matrix verification problems.
Then it uses amplitude amplification to search if one of these verifications fail. Each of these smaller
verification steps also use a Grover search to look for disagreements. So the complete algorithm
uses one quantum search routine nested inside another quantum search routine. This is a common
strategy used while designing quantum algorithms to improve query complexity. The full algorithm
is sketched below.

Algorithm 6 Matrix product verification [5] [119]
     Input:
         • 𝑛 × 𝑛 matrices 𝐴, 𝐵, 𝐶.
     Output:
         • Verifies if 𝐴𝐵 = 𝐶
     Procedure:                        √                         √
         Step 1. Partition 𝐵 and 𝐶 into 𝑛 submatrices of size 𝑛 × 𝑛. Call these 𝐵𝑖 and 𝐶𝑖 respectively.
     𝐴𝐵 = 𝐶 if and only if 𝐴𝐵𝑖 = 𝐶𝑖 for all 𝑖.
         Step 2. Use amplitude amplification over 𝑖 on these steps:√
                  Step 2a. Choose a random vector 𝑥 of dimension 𝑛.
                  Step 2b. Compute 𝑦 = 𝐵𝑖 𝑥 and 𝑧 = 𝐶𝑖 𝑥 classically
                   Step 2c. Verify equation 𝐴𝑦 = 𝑧 by Grover search. Search for a row 𝑗 such that
     (𝐴𝑦 − 𝑧) 𝑗 ≠ 0


  The number of qubits and the circuit depth required for this algorithm is too large for it to be
successfully implemented on the IBM machines. But at the heart of this algorithm is the Grover
search procedure, which we have already discussed and implemented in Section II

8     GROUP ISOMORPHISM
8.1     Problem definition and background
The group isomorphism problem, originally identified by Max Dehn in 1911 [40], is a well-known
decision problem in abstract algebra. Simply stated, it asks whether there exists an isomorphism
between two finite groups, 𝐺 and 𝐺 ′. Which, according to the standpoint of group theory, means
that they are equivalent (and need not be distinguished). At the end of Section 5 we saw an example
of two isomorphic groups, 𝑆 2 and 𝐴2 . These two are the same group in terms of how the group
operation works on the group elements, but are defined in different ways. More precisely, two
groups, (𝐺 1, ·) and (𝐺 2, ∗) are called isomorphic if there is a bijection, 𝑓 : 𝐺 1 → 𝐺 2 , between them
such that, 𝑓 (𝑔1 · 𝑔2 ) = 𝑓 (𝑔1 ) ∗ 𝑓 (𝑔2 ).
   To solve this problem using a quantum algorithm, we assume that each element can be uniquely
identified by an arbitrary bit-string label. We also assume that a so-called group oracle can be used
to return the product of multiple elements. That is, given an ordered list of group-element labels,
the oracle will return the product label. In practice, this means that we must be able to construct a
quantum circuit to implement 𝑈𝑎 : |𝑦⟩ → |𝑎𝑦⟩, for any 𝑎 ∈ 𝐺.
   In this section, we will focus our attention on the abelian group isomorphism problem, because
it can be solved using a generalization of Shor’s algorithm [114]. As we saw before, abelian simply
means that the operation (·) used to define the group is commutative, such that 𝑎 · 𝑏 = 𝑏 · 𝑎, for
𝑎, 𝑏 ∈ 𝐺. Although Shor’s approach is specifically intended to leverage a quantum period-finding
Quantum Algorithm Implementations for Beginners                                                       41


algorithm to reduce the time-complexity of factoring, the procedure effectively solves the group
isomorphism problem over cyclic groups. Using this relationship, Cheung and Mosca [28] have
developed a theoretical quantum algorithm to solve the abelian group isomorphism problem by
computing the decomposition of a given group into a direct product of cyclic subgroups.

8.2   Algorithm description
The procedure presented in Algorithm 7 assumes the fundamental theorem of finite abelian groups,
that they can be decomposed as a direct sum of cyclic subgroups of prime power order. This
decomposition can then be used to test if an isomorphism exists between two groups.

Algorithm 7 Decompose(𝑎 1, . . . , 𝑎𝑘 , 𝑞), of Cheung and Mosca [28]
  Input:
      • A generating set {𝑎 1, . . . , 𝑎𝑘 } of 𝐺.
      • The maximum order, 𝑞, of the generating set.
  Output:
      • The set of elements 𝑔1, . . . , 𝑔𝑙 from group 𝐺, with 𝑙 ≤ 𝑘.
  Procedure:
      Step 1. Define 𝑔 : Z𝑞𝑘 → 𝐺 by mapping (𝑥 1, . . . , 𝑥𝑘 ) → 𝑔(𝑥) = 𝑎𝑥1 1 · · · 𝑎𝑘𝑥𝑘 .
      Find generators for the hidden subgroup 𝐾 of Z𝑞𝑘 as defined by function 𝑔.
      Step 2. Compute a set 𝑦1, . . . , 𝑦𝑙 ∈ Z𝑞𝑘 /𝐾 of generators for Z𝑞𝑘 /𝐾.
      Step 3. Output the set {𝑔(𝑦1 ), . . . , 𝑔(𝑦𝑙 )}.

   Since the procedure in Algorithm 7 is mostly classical, we shall treat the task of finding the
generators of the hidden subgroup in Step 1 as the most critical for us to explore. This task is
commonly referred to as the hidden subgroup problem (HSP). This means that, given a function
𝑔 that maps a finite group 𝐴 onto a finite set 𝑋 , we are asked to find a generating set for the
subgroup 𝐾. For 𝐾 to be the so-called hidden subgroup of 𝐴, we require that 𝑔 is both constant
and distinct on the cosets of 𝐾. On a quantum computer, this problem can be solved using a
number of operations that is polynomial in log|𝐴|, in addition to one oracle evaluation of the
unitary transform 𝑈 |𝑎⟩ |ℎ⟩ = |𝑎⟩ |ℎ ⊕ 𝑔(𝑎)⟩. The general procedure needed to complete Step 1 of
algorithm 7 is described in algorithm 8.
   Like the period-finding approach used in quantum factorization in Section V, Algorithm 8
is heavily based on the concept of phase estimation. Note that the Fourier transform in Eq. 58
represents 𝑎 ∈ 𝐴 indexed by 𝑙. The key concept of the procedure is that | ˆ𝑔(𝑙)⟩ has nearly zero
amplitude for all values of 𝑙, except those which satisfy
                                                    ∑︁
                                           |𝐾 | =          𝑒 −2𝜋𝑖𝑙ℎ/|𝐴 | ,                         (60)
                                                    ℎ ∈𝐾
and that knowledge of 𝑙 can be used to determine both the elements and generating set of 𝐾.
As discussed by Nielsen and Chuang [92], the final step in algorithm 8 can be accomplished by
expressing the phase as

                                                             𝑀
                                                             Ö
                                           2𝜋𝑖𝑙𝑎/ |𝐴 |
                                      →𝑒                 =         𝑒 2𝜋𝑖𝑙𝑖 𝑎𝑖 /𝑝𝑖 .                (61)
                                                             𝑖=1
for 𝑎𝑖 ∈ Z𝑝𝑖 , where 𝑝𝑖 are primes, and Z𝑝𝑖 is the group containing integers {0, 1, . . . , 𝑝𝑖 − 1} with
the operator being addition modulo 𝑝𝑖 .
42                                                                                      Abhijith J., et al.


Algorithm 8 Solution to the hidden subgroup problem (for finite abelian groups). Based on Ref. [92]
     Input:
         • Two quantum registers.
         • Elements of the finite abelian group 𝐴 (or the generating set).
         • A function 𝑔, such that 𝑔 : 𝐴 → 𝑋 , with 𝑎 ∈ 𝐴 and ℎ ∈ 𝑋 .
     Output:
         • The generating set for the hidden subgroup 𝐾.
     Procedure:
         Step 1. Create initial state.
         Step 2. Create superposition between resisters.
         Step 3. Apply unitary operation (𝑈 ) for function 𝑔(𝑎).
                                             1 ∑︁
                                        → √︁          |𝑎⟩ |𝑔(𝑎)⟩                                     (57)
                                             |𝐴| 𝑎 ∈𝐴
         Step 4. Apply inverse Fourier transform.
                                                |𝐴 |−1
                                            1    ∑︁
                                     → √︁                𝑒 2𝜋𝑖𝑙𝑎/|𝐴 | | ˆ
                                                                       𝑔(𝑙)⟩                         (58)
                                            |𝐴| 𝑙=0
         Step 5. Measure the phase from first register.
                                                 → 𝑙/|𝐴|                                             (59)
         Step 6. Sample 𝐾 from l / | A |.




Fig. 23. Basic phase-estimation quantum circuit needed to solve the general hidden subgroup problem in
algorithm 8. Here, |𝑢⟩ is an eigenstate of the unitary operator 𝑈 .


   The quantum circuit needed to solve the HSP is schematically illustrated in Fig. 23. This simplified
circuit includes steps 1-5 of algorithm 8, and makes it clear that all forms of the HSP (order-finding,
period-finding, discrete logarithm, etc.) are extensions of quantum phase estimation.

8.3     Algorithm implemented using Qiskit
Since the generalized group isomorphism problem is somewhat complex, we will focus here on the
implementation of the HSP circuit fragment illustrated in Fig. 23. We also chose a specific instance
of the HSP: the problem of finding the period of 𝑎 mod 𝑛. In Fig. 24, the basic outline of the code
needed for this specific problem is illustrated using the python-based Qiskit interface.
Quantum Algorithm Implementations for Beginners                                                     43


#======================================================================#
#---------- Finding period (r) of a % N, with N=15 ------------------#
#======================================================================#
def findperiod(a, N=15, nqubits1, nqubits2):

     # Create QuantumProgram object, and define registers and circuit
     Q_program = QuantumProgram()
     qr1 = Q_program.create_quantum_register("qr1", nqubits1)
     qr2 = Q_program.create_quantum_register("qr2", nqubits2)
     cr1 = Q_program.create_classical_register("cr1", nqubits1)
     cmod15 = Q_program.create_circuit("cmod15", [qr1, qr2], [cr1])

     # Apply a hadamard to each qubit in register 1
     # and prepare state |1> in regsiter 2
     for j in range(nqubits1): cmod15.h(qr1[j])
     cmod15.x(qr2[nqubits2-1])

     # Loop over qubits in register 1
     for p in range(nqubits1):

          # Calculate next 'b' in the Ub to apply
          # ( Note: b = a^(2^p) % N ).
          # Then apply Ub
          b = pow(a,pow(2,p),N)
          CxModM(cmod15, qr1, qr2, p, b, N, nqubits1, nqubits2)

     # Perform inverse QFT on first register
     qft_inv(cmod15, qr1, nqubits1)

     # Measure each qubit, storing the result in the classical register
     for i in range(n_qr1): cmod15.measure(qr1[i], cr1[i])


            Fig. 24. Simple implementation of the quantum period-finding algorithm in Qiskit




   Like most instances of the HSP, one of the most challenging practical tasks of finding the period
of 𝑎 mod 𝑛 on a quantum computer is the implementation of the oracle. The details of the oracle
are not explicitly shown in the Qiskit snippet, but for the required 𝐶𝑎 mod 15 operations, one can
simply used the circuits developed by Markov and Saeedi [105]. The code in Fig. 24 also assumes
that a function 𝑞𝑓 𝑡_𝑖𝑛𝑣 () will return the gates for an inverse quantum Fourier transform, and that a
classical continued fractions algorithm can be used to convert the end result (a phase) to the desired
integer period.
   Although the specific procedure outlined in Fig. 24 can be directly implemented using the IBM
Qiskit interface, the resulting QASM code is not expected to lead to accurate results on the IBMX4
(or IBMX5). This is because the generated circuit is long enough for decoherence error and noise to
ultimately dominate the measured state. In other words, the physical hardware requires further
44                                                                                        Abhijith J., et al.


optimization to reduce the number of gates used between the initial state preparation and the final
measurement.

9     QUANTUM RANDOM WALKS
9.1    Problem definition and background
Quantum algorithms for graph properties using the adjacency matrix (as part of an oracle) have
been published for minimum spanning tree, shortest path, deciding if a graph is bipartite, detecting
cycles, finding subgraphs (such as a triangle), maximal clique, and many more. Each typically
involves the use of Grover’s search [63] with an oracle constructed from the adjacency matrix.
   But for some problems Grover’s algorithm is insufficient to achieve optimal query complexity. In
such cases, a quantum random walk can sometimes be useful in reducing the query complexity
of an algorithm further. An example of this is the quantum algorithm for element distinctness by
Ambainis [6]. Additionally, quantum walk algorithms can also be used to search and find graph
properties [33, 43, 48, 75, 76, 86]. Quantum random walks can be seen as a quantum mechanical
generalization of classical random walks. Quantum random walk algorithms come in two forms,
discrete time quantum walks and continuous time quantum walks [75]. The discrete form operates
in a step-wise fashion, requiring multiple copies of a set of gates per step. The continuous form
uses a transition matrix that is expressed as a Hamiltonian, whose time evolution is then simulated.
Quantum random walks can be used to walk a graph [43, 76], search for marked vertices [48], and
to solve s-t connectivity [76]. An excellent survey of this approach to quantum search can be found
in Ref. [106].
   Most quantum algorithms that solve graph problems requires an oracle that knows the properties
of the underlying graph. A graph properties oracle can be assembled as a circuit based on the
adjacency matrix of the graph and linear algebra transformations. For example, a quantum circuit
for finding maximal cliques in a graph with 𝑛 nodes, requires an oracle workspace of 𝑛 2 data qubits
and 𝑛 2 ancilla qubits (see [131]). Each oracle call requires execution of 6𝑛 2 Toffoli gates and 2𝑛
CNOT gates. An oracle such as this can be run on a simulator, but requires too many qubits to run
on actual qubit hardware. Quantum algorithms for finding a triangle, quadrilateral, longer cycles,
and arbitrary subgraphs [32] typically use the adjacency matrix to create the oracles. Here we will
not get into using quantum random walks to solve such problems. Instead we will demonstrate
how to implement a simple quantum random walk on a quantum computer.

9.2    Example of a quantum random walk
Quantum random walks or simply quantum walks are quantum analogues of classical random
walks and Markov chains. Unlike the continuous time quantum walk, the discrete time quantum
walk algorithm requires the use of one or more coin qubits representing the number of movement
choices from each graph vertex. These extra coin degrees of freedom are necessary to ensure
unitarity of the quantum walk. An appropriate unitary transformation on these coin qubits then
acts like the quantum version of a random coin toss, to decide the next vertex for the walker.
   Intuitively, the quantum walk is very similar to its classical cousin. In a classical walk, the walker
observes some random process, say a coin toss, and decides on his next step conditioned on the
output of this random process. So for a classical random walk, the walker is given a probability
to make a transition. In a quantum walk, on the other hand, the random process is replaced by a
quantum process. This quantum process is the application of the coin operator, which is a unitary
matrix. So the next step of the walker is controlled by a complex amplitude rather than a probability.
This generalization, from positive numbers to complex numbers, makes quantum walks more
powerful than classical random walks.
Quantum Algorithm Implementations for Beginners                                                     45


   The full Hilbert space for the discrete quantum walk on a cycle with 𝑁 = 2𝑛 nodes can then be
constructed as follows. We use an 𝑛 qubit register to represent the nodes of the graph as bit strings.
For the cycle every node has only two neighbours, so the coin space only needs a dimension of 2.
Hence, only one extra coin qubit is required. The basis vectors of the coin (|0⟩ and |1⟩) will denote
the right and left neighbours. So a basis state in the full Hilbert space will have the form |𝑘, 𝑞⟩,
where 𝑘 is represents a node on the cycle and 𝑞 is a single bit representing the coin state.
   The quantum walk is then a product of two operators, the shift operator (𝑆) and the coin operator
(𝐶). As we mentioned before the coin operator only acts on the coin qubit. The coin operator can be
in principle any unitary that mixes the coin states, but here we will use the Hadamard coin which
is just the 𝐻 gate on the coin qubit,

                                                     |𝑘, 0⟩ + (−1)𝑞 |𝑘, 1⟩
                             𝐶 |𝑘, 𝑞⟩ = 𝐼 ⊗ 𝐻 |𝑘, 𝑞⟩ =        √            .                    (62)
                                                                2
  The shift operator acts on both the registers. It moves the walker to the left or right depending
on the coin state and then flips the coin state,
                                       𝑆 |𝑘, 𝑞⟩ = |𝑘 + (−1)𝑞 , 𝑞 ⊕ 1⟩                             (63)
   The quantum walk then proceeds by applying these two operators in alternation. A 𝑝 step
quantum walk is just the operator (𝑆𝐶) 𝑝 . This type of a walk was first introduced in Ref. [112] and
is sometimes referred to as a ‘flip-flop’ quantum walk.
   The definition of these operators can change for different types of quantum walk. The coin
operator can be a Hadamard gate or a sub-circuit that results in mixing the coin states. The shift
operator can be simple as described above or can be a more complicated circuit that selects the
next vertex in the path based on the state of the coin. A simple pseudo-code for implementing the
quantum walk is given in Algorithm 9.

Algorithm 9 Discrete time quantum walk
  Input:
      • Two quantum registers. The coin register and the position register.
      • Number of steps, 𝑇 .
  Output:
      • State of the quantum walk after 𝑇 steps.
  Procedure:
      Step 1. Create the initial state. The initial state depends on the application. For instance, in
  quantum search algorithms, the initial state is the uniform superposition state.

        for 0 ≤ 𝑘 < 𝑇 do
               Step 2a. Apply the coin operator, 𝐶, to the coin register.
               Step 2b. Apply the shift operator, 𝑆. This shifts the position of the walker controlled
          on the coin state.
        end for
        Step 3. (Optional) Measure the final state.


9.3   Algorithm implementation using Qiskit on IBM Q
In this section we will implement a simple quantum walk on Qiskit and execute it on both the
simulator and ibmq_vigo, which is a 5 qubit machine available on IBM Q. We will test the quantum
walk on a simple 4 vertex cycle with the vertices labels as given in Fig. 25.
46                                                                                               Abhijith J., et al.


                                                   0           3




                                                   1           2



Fig. 25. A graph of 4 nodes in the form of a square is used for the random walk algorithm. The starting vertex
is labeled 0. The vertex labels are converted to binary for input into the quantum circuit. The quantum walk
algorithm will walk around the graph.


   The coin operator in Eq. (62) is just the 𝐻 gate acting on the coin qubit. The shift operator defined
in Eq. (63) is more non-trivial. We can implement it by the circuit given in Fig. 26.


                                     •      •      𝑋       •               •

                                     •             𝑋       •       𝑋



     Fig. 26. Quantum circuit for the shift operation on the 4 vertex cycle. The top qubit is the coin qubit.


   Running the walk for multiple steps requires us to apply the shift operator circuit many times.
So it would be tedious to implement the quantum walk on the IBM Q graphical interface. Instead
we can use Qiskit to design the shift operator as a user defined gate and then run the walk for
multiple steps using a simple for loop. The Qiskit code for this is given in Fig. 27.
   We ran this Qiskit code for 4 steps of the quantum walk. We chose 4 steps since, a simple
calculation shows that, starting from |000⟩ and applying (𝑆𝐶) 4 will concentrate all the probability
to the state |100⟩ . This is confirmed by running the Qiskit code on the simulator. But running the
same code on ibm_vigo gave |100⟩ with only 21.7% probability. The rest of the probability was
distributed among the other basis states, but |100⟩ was still the state with the largest probability.
This poor performance is due to the circuit having large depth. We can expect to get better results
by running the quantum walk for a single step. After a single step, starting from |000⟩, the state of
the system is |111⟩+|010⟩
                   √      . This is again confirmed by the simulator. Running on ibm_vigo, we got
                     2
|111⟩ with 33.5% probability and |010⟩ with 28.5% probability.

10     QUANTUM MINIMAL SPANNING TREE
10.1     Problem definition and background
A common problem in network design is to find a minimum spanning tree. Suppose we are
responsible for maintaining a simple network of roads. Unfortunately, each segment needs repair
and our budget is limited. What combination of repairs will guarantee the network remains
connected? Fig 28 shows a model of a simple road network as a graph, together with a minimal
spanning tree.
    Formally, a graph 𝐺 = (𝑉 , 𝐸) consists of a set 𝑉 (the nodes) and a set 𝐸 consisting of pairs of
nodes. A graph is connected if between any two nodes there exists a path. A spanning tree of
a connected graph 𝐺 = (𝑉 , 𝐸) is the graph 𝑇 = (𝑉 , 𝐸𝑇 ) where 𝐸𝑇 ⊂ 𝐸 and 𝑇 contains no cycles
(i.e., there is exactly one path between any two vertices). It is not hard to see that a graph 𝑇 is a
Quantum Algorithm Implementations for Beginners                                                   47


from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute

n_steps =      4               #Number of steps

#Defining the shift gate

shift_q = QuantumRegister(3)                                                     #3 qubit register
shift_circ = QuantumCircuit (shift_q, name='shift_circ')                         #Circuit for shift operator
shift_circ.ccx (shift_q[0], shift_q[1], shift_q[2])                              #Toffoli gate
shift_circ.cx ( shift_q[0], shift_q[1] )                                         #CNOT gate
shift_circ.x ( shift_q[0] )
shift_circ.x ( shift_q[1] )
shift_circ.ccx (shift_q[0], shift_q[1], shift_q[2])
shift_circ.x ( shift_q[1] )
shift_circ.cx ( shift_q[0], shift_q[1] )

shift_gate = shift_circ.to_instruction()                            #Convert the circuit to a gate

q = QuantumRegister (3, name='q')                                   #3 qubit register
c = ClassicalRegister (3, name='c')                                 #3 bit classical register
circ = QuantumCircuit (q,c)                                         #Main circuit
for i in range(n_steps):
    circ.h (q[0])                                                   #Coin step
    circ.append (shift_gate, [q[0],q[1],q[2]])                      #Shift step

circ.measure ([q[0],q[1],q[2]], [c[0],c[1],c[2]])




                   Fig. 27. Qiskit code to implement the quantum walk on a 4 vertex cycle.


spanning tree if and only if 𝑇 is connected and has 𝑛 nodes and 𝑛 − 1 edges. A weighted graph is
a graph 𝐺 = (𝑉 , 𝐸, 𝑤) where 𝑤 is a map on the edges 𝑤 : 𝐸 → R. A minimal spanning tree of a
graph 𝐺 is then a spanning tree 𝑇 = (𝑉 , 𝐸𝑇 ) which minimizes
                                              ∑︁
                                                 𝑤 (𝑒).                                     (64)
                                                  𝑒 ∈𝐸𝑇



10.2   Algorithm description
Algorithmically, a graph is usually presented in one of two ways: either as a list of edges or as
an adjacency matrix. We consider the case where 𝐺 is presented as a list of edges. A quantum
48                                                                                               Abhijith J., et al.



                                                                          10
                                           3                  6                1


                                                                                   1
                                                          8
                                    2
                                                                  5
                                2
                                          2
                                                                      1



                                        (a) The weighted graph model.

                                                                          10
                                           3                  6                1


                                                                               1
                                                          8
                                    2
                                                              5
                                2
                                          2
                                                                      1



                                         (b) A minimal spanning tree.

Fig. 28. A graph modeling repair costs of a simple transportation network (a) together with (b) its minimal
spanning tree (the solid edges). The sum of the weights of the edges in the minimal spanning tree is 21.

                                                                          10
                                           3                  6                1


                                                                                   1
                                                          8
                                    2
                                                                  5
                                2
                                          2
                                                                      1




Fig. 29. The first two steps of Borůvka’s algorithm. Starting with each node as a distinct tree, find the minimal
weighed edge between each tree and the rest of the trees. The direction of the solid edges indicates the edge
is the minimal weighted edge for the source node. The components connected by solid edges (disregarding
the directions) will form the trees at the start of the second run of step (2) of Borůvka’s algorithm


algorithm for finding
                 √ a minimal spanning tree of an input graph is given in [45]. This algorithm
requires only 𝑂 ( 𝑛𝑚) queries where 𝑛 is the number of nodes and 𝑚 the number of edges in
the graph. Classically, the best algorithms run in time 𝑂 (𝑚 log 𝑛). In particular, this is the time
complexity of Borůvka’s algorithm [20]. The quantum algorithm combines Borůvka’s algorithm
together with the quantum search algorithm of Grover [63].
Quantum Algorithm Implementations for Beginners                                                      49


   Borůvka’s algorithm builds a collection of disjoint trees (i.e., a forest) and successively merges by
adding minimal weight edges. The first two steps of the algorithm are shown in Fig 29. Formally,
we have
   (1) Let T be the collection of 𝑛 disjoint trees, each consisting of exactly one node from the graph
       𝐺.
   (2) Repeat:
     (a) For each tree 𝑇𝑖 in T find the minimal weighted edge, 𝑒𝑖 , of 𝐺 between 𝑇𝑖 and the other
         trees of T .
     (b) Merge the trees {𝑇𝑖 ∪ {𝑒𝑖 }} so that they are disjoint: set this new collection to T .
If there are 𝑘 trees in T at a given iteration of Step (2), then the algorithm performs 𝑘 searches for
the respective minimal weighted edges. As the trees are disjoint, we can perform the 𝑘 searches in
one sweep by inspecting each of the 𝑚 edges of 𝐺 once. As there will be at most log 𝑛 iterations of
Step (2), this results in a running time of 𝑂 (𝑚 log 𝑛). The quantum algorithm takes advantage of
the Grover search algorithm, to speed up the searches in Step (2).
   In the previous sections we used Grover search to look for a single item in a list of 𝑁 elements.
But the search algorithm will work even if there are 𝑀 elements in√︃the list that are marked by the
                                                                     𝑁
oracle. One of these marked elements can then be found using 𝑂 ( 𝑀     ) queries to the oracle.
  In the algorithm above, we need to find the minimal element of an appropriate list. Clearly this
can not be implemented directly as an oracle without actually inspecting each of the list elements.
Luckily, there is a simple work around given by Durr et al [45] which involves multiple calls to the
Grover algorithm as described in Algorithm 10.

Algorithm 10 Minima finding algorithm
  Input:
      • A unitary implementation a function 𝐹 on a list of 𝑁 elements,
                                       𝑈 𝐹 |𝑥⟩ |𝑦⟩ = |𝑥⟩ |𝑦 ⊕ 𝐹 (𝑥)⟩ .

  Output:
      • |𝑥 ∗ ⟩ such that 𝐹 (𝑥 ∗ ) is the minimum of the function over the list.
  Procedure:
      Step 1. Pick a random 𝑗 from the list.

        for 0 ≤ 𝑘 < 𝑇 do
               Step 2a. Do Grover search [21] with the oracle for function 𝑓 𝑗 such that,
                                            (
                                              1 if 𝐹 (𝑖) ≤ 𝐹 ( 𝑗)
                                  𝑓 𝑗 (𝑖) =
                                              0 if 𝐹 (𝑖) > 𝐹 ( 𝑗)

              Step 2b. Update 𝑗 with the result of Grover search.
        end for

                                              √
  A probabilistic analysis shows that 𝑇 = 22.5 𝑁 +1.4 log22 (𝑁 ) suffices to find the minimal element
with high probability [46] . The inner loop of the algorithm uses a Grover search routine with
potentially multiple marked items. But the number of marked items is not known beforehand. This
poses problem as Grover search being a unitary algorithm needs to be stopped exactly at the right
number of iterations to give the correct answer. Running the procedure for longer deteriorates
50                                                                                               Abhijith J., et al.


the quality of the answer. If the number of marked items is unknown the stopping criterion of the
algorithm is also unknown. This problem can be rectified using some extra steps by a technique
given in Boyer et al [21]. We have to use this modified version of Grover search in the inner loop.
   We did not implement the full algorithm due to space constraints on the IBM computer. Even
to successfully implement a minima finding algorithm, at least 6 qubits would be necessary to
compare two 3-bit numbers. Therefore we implemented the minima finding algorithm by hard
coding the oracle for each of eight possible functions 𝑓𝑥 : {𝑓𝑥 (𝑖) = 1 if 𝐹 (𝑖) ≤ 𝐹 (𝑥)}. The results are
shown in Figure 30. The QASM code for implementing 𝑓2 (𝑖) = 1 if 𝐹 (𝑖) ≤ 𝐹 (2) required just under
100 lines of code (more than 100 individual gates.) The results, even when using the simulator
are not good when 𝑘 ≥ 𝑁 /4 elements are marked. A typical way to get around this is to double
the length of the list by adding 𝑁 extra items which will evaluate to 0 under 𝑓𝑥 , which however
requires an extra qubit.

                                        x=1          x=2         x=3            x=4

                                0.3
                                0.2
                                                                                             1
                                0.1                                                          2
                                                                                             3

                    Frequency
                                                                                             4
                                        x=5          x=6         x=7            x=8          5
                                                                                             6
                                                                                             7
                                0.3                                                          8
                                0.2
                                0.1
                                000
                                      12345678    12345678 12345678       1 2 3 4 5 6 7 81
                                                       Resulting Value

                                                  (a) IBM Q Implementation

                                        x=1          x=2         x=3            x=4
                                0.9


                                0.5
                                                                                             1
                                                                                             2
                                0.1                                                          3

                    Frequency
                                                                                             4
                                        x=5          x=6         x=7            x=8          5
                                0.9                                                          6
                                                                                             7
                                                                                             8
                                0.5


                                0.1
                                000
                                      12345678    12345678 12345678       1 2 3 4 5 6 7 81
                                                       Resulting Value

                                                 (b) Simulator Implementation

Fig. 30. The results of running 1000 trials of the minima finding algorithm on both (a) the ibmqx4 chip and
(b) the IBM simulator to find values less than or equal to the input 𝑥.
Quantum Algorithm Implementations for Beginners                                                            51




Fig. 31. A simple directed graph representing flows and capacities. Conventionally, the state of the flow
problem is indicated by the current flow relative to the capacity on any directed link using the notation f/c.




Fig. 32. The Ford-Fulkerson solution to the max-flow problem in three steps. Each step represents the
application of an augmenting path to the previous flow state.


11     QUANTUM MAXIMUM FLOW ANALYSIS
11.1    Problem definition and background
Network flow problems play a major role in computational graph theory and operations research
(OR). Solving the max-flow problem is the key to solving many important graph problems, such
as finding a minimum cut set, and finding a maximal graph matching. The Ford-Fulkerson algo-
rithm [52] is a landmark method that defines key heuristics for solving the max flow problem. The
most important of these heuristics include the construction of a residual graph, and the notion of
augmenting paths. For integer-capacity flows, Ford-Fulkerson has complexity 𝑂 (𝑓 𝑚) for 𝑚 edges
and max flow 𝑓 . The Edmonds-Karp variant has complexity 𝑂 (𝑛𝑚 2 ) for 𝑛 vertices and 𝑚√ edges.
The quantum-accelerated classical algorithm discussed here [7] claims complexity 𝑂 (𝑛 7/6 𝑚).
   The best classical implementations of the max-flow solver involve several important improve-
ments [47], especially that of using breadth-first search to find the shortest augmenting path on
each iteration. This is equivalent to constructing layered subgraphs for finding augmenting paths.
   An illustration of the essential method introduced by Ford and Fulkerson can be described using
Figures 31 and 32. At each link in the network, the current flow 𝑓 and the capacity 𝑐 are shown.
Typically, the state of flow on the graph is designated by 𝑓 /𝑐, with the residual capacity implicitly
given by 𝑐 − 𝑓 . In Figure 31, the initial flow has been set to zero.
   The basic steps in the solution to the max-flow problem are illustrated by Figure 32. The algorithm
begins on the left by considering the path [s,v,t]. Since 2 is the maximum capacity allowed along
that path, all the flows on the path are tacitly set to that value. Implicitly, a reverse flow of -2 is
also assigned to each edge so that the tacit flow may be “undone” if necessary. Next, the middle of
52                                                                                       Abhijith J., et al.


the figure examines the lower path [s,w,t]. This path is constrained by a maximum capacity on
the edge [s,w] of again 2. Finally, the path [s,v,w,t] is the only remaining path. It can only support
the residual capacity of 1 on edge [s,v]. We can then read off the maximum flow result at the sink
vertex 𝑡 since the total flow must end there. The maximum flow is seen to be 5.
    While this method seems straightforward, without the efficiencies provided by the improvements
of Edmonds and Karp, convergence might be slow for integer flows on large graphs, and may not
converge at all for real-valued flows. The modification of always choosing the shortest next path in
the residual network to augment, is what makes the algorithm practical. To see this, consider what
would have happened if the path [s,v,w,t] had been chosen first. Since augmenting that path blocks
the remaining paths, flows would have to be reversed before the algorithm could proceed.
    Choosing the shortest path requires performing a breadth-first search whenever new flow values
have been assigned to the residual graph. This is equivalent to building a layered set of subgraphs to
partition the residual graph. This is the step that leads to the 𝑚 2 complexity of Edmonds-Karp, and
it is this √
           step that is speeded up in the “quantized” version of the algorithm, leading to a complexity
term of 𝑚 instead of 𝑚 2 .

11.2     Algorithm description
The Quantum algorithm described by Ambainis and Spalek is a “quantized” version of the Edmonds-
Karp algorithm, that is, the classical algorithm with quantum acceleration. The key quantum
component is a generalized version of Grover’s search algorithm that finds 𝑘 items in an unsorted
list of length 𝐿 [21]. The algorithm is used in creating a layered subgraph data structure that is
subsequently used to find the shortest augmenting path at a given iteration. Like in Section XI, we
will be oblivious to the number of marked items Grover’s algorithm is searching for. So once again
we have to use techniques from Ref.[21] while performing the search.
   Here we will describe how to build a layered graph partition. In a layered graph partition each
vertex in the graph is assigned to thew 𝑖-th layer such that edges of the graph only connect between
𝑖-th and (𝑖 + 1)-th layers. The key to “quantization” lies in using Grover’s search to build a layered
graph partition by computing layer numbers for all vertices. The layers are represented by an array
L indexing the vertices of the graph, and assigning to each element a subgraph layer number. The
sink vertex at vertex zero is set to zero. The the algorithm proceeds according to the following
pseudo-code described in Algorithm 11.


Algorithm 11 Layered graph partitioning
     Input:
         • Adjacency information of the graph (Adjacency matrix, list of edges,etc.)
         • Source vertex 𝑠.
     Output:
         • L such that L [𝑖] is the layer number of the 𝑖-th vertex.
     Procedure:
         Step 1. Set L [𝑠] = 0 and L [𝑥] = ∞ for 𝑥 ≠ 0
         Step 2. Create a one-entry queue 𝑊 = {𝑠} (𝑥 = 0)
         while 𝑊 ≠ 𝜙 do
                Step 3a. Take the first vertex 𝑥 from 𝑊 .
                Step 3b. Find by Grover search all its neighbors 𝑦 with L [𝑦] = ∞.
                Step 3c. Set L (𝑦) = L [𝑥] + 1, append 𝑦 into 𝑊 , and remove 𝑥 from 𝑊
         end while
Quantum Algorithm Implementations for Beginners                                                          53


  Notice that the oracle for Grover search required for this algorithm is one that marks all the
neighbours of 𝑥 whose layer number is currently set to ∞. Grover’s search speeds up the layers
assignment of the vertices by quickly finding all the entries in the layer array L that contain the
value ∞. In practical terms, ∞ might simply be the largest value reachable in an n-qubit machine.
The generalized Grover search would look for all such values without a priori knowing the number
of such values. The size of a circuit required to do a full layered graph partitioning makes it
impractical to implement it on the IBM machine. But the heart of the algorithm is Grover search,
which we have already implemented earlier.

12     QUANTUM APPROXIMATE OPTIMIZATION ALGORITHM
12.1    Problem definition and background
Combinatorial optimization problems are pervasive and appear in applications such as hardware
verification, artificial intelligence and compiler design, just to name a few. Some examples of
combinatorial optimization problems include Knapsack, Traveling Saleman, Vehicle Routing, and
Graph Coloring problems. A variety of combinatorial optimization problems including MaxSat,
MaxCut, and MaxClique can be characterized by the following generic unconstrained discrete
maximization problem,
                                                  𝑚
                                                 ∑︁
                                       maximize:     𝐶𝛼 (𝑥)
                                                 𝛼=1                                       (65)
                                          𝑥𝑖 ∈ {0, 1} ∀𝑖 ∈ {1, . . . , 𝑛}
In this generic formulation, there are 𝑛 binary variables, 𝑥, and 𝑚 binary functions of those
variables, 𝐶 (𝑥), called clauses. The challenge is to find the assignment of 𝑥 that maximizes the
number of clauses that can be satisfied, i.e. that can be evaluated to 1. In case each clause is an OR
of literals (positive or negated variables), this is the so-called MaxSat problem, which is NP-Hard
in general [79], and is an optimization variant of the well-known satisfiability problem, which
is NP-Complete [36]. Hence, solving an instance of Eq. (65) in practice can be computationally
challenging, meaning that there is no algorithm which can solve all instances of the problem in
time polynomial in their input size (𝑛, 𝑚), unless P=NP.

The Maximum Cut Problem. To provide another concrete example of Eq. (65), let us consider the
MaxCut problem. As input, the MaxCut problem takes a graph G = (V, E), which is characterized
by a set of 𝑛 nodes V and a set of 𝑚 undirected edges E. The task is to partition the nodes into
two sets, such that the number of edges crossing these sets is maximized. Figure 33 provides an
illustrative example, in which a graph with five nodes and six edges is partitioned into two sets
that result in a cut of size five. In general, the MaxCut problem is characterized by the following
unconstrained discrete maximization problem,
                                      ∑︁                               ∑︁
                      maximize:                 XOR(𝑥𝑢 , 𝑥 𝑣 )   =               𝑥𝑢 + 𝑥 𝑣 − 2𝑥𝑢 𝑥 𝑣
                                    {𝑢,𝑣 } ∈E                        {𝑢,𝑣 } ∈E                         (66)
                      𝑥𝑖 ∈ {0, 1}     ∀𝑖 ∈ n
   It is clear that Eq. (66) conforms to the structure of Eq. (65): There is one binary variable 𝑥𝑖 ∈ {0, 1}
for each node in the graph, indicating which set it belongs to. The objective function consists of
one term for each edge in the graph. This term is 0 if the the nodes of that edge take the same value
and 1 otherwise. Consequently, the optimal solution of (66) will be a maximal cut of the graph G. In
                                                                                                 Í
foresight, we also reformulate Eq. (66) in terms of spin variables 𝑧𝑖 ∈ {−1, +1} as a sum 𝛼 𝐶𝛼 (𝑧),
54                                                                                                  Abhijith J., et al.


                                                                                 𝑥 1 .. 𝑥 5   Val   𝑥 1 .. 𝑥 5   Val
                                                  4                              00000         0    01000         3
             2               4                                    2              00001         2    01001         5
                                                                                 00010         2    01010         3
 1                                                1                              00011         2    01011         3
                                                                                 00100         3    01100         4
                                                                  5              00101         3    01101         4
             3               5
                                                  3                              00110         5    01110         4
                                                      5 Cut                      00111         3    01111         3

Fig. 33. An illustration of the MaxCut problem: (left) input Graph 𝐺, (middle) a solution of maximum value 5,
(right) values of all possible cuts; note that swapping 0/1 for all variables would result in the same cut sizes.



using the linear transformation 𝑥𝑖 = (𝑧𝑖 + 1)/2:
                                        ∑︁ 1                       𝑚           ∑︁ 𝑧𝑢 𝑧 𝑣
                         maximize:           (1 − 𝑧𝑢 𝑧 𝑣 )    =          −
                                           2                       2                2                            (67)
                                      {𝑢,𝑣 } ∈E                              {𝑢,𝑣 } ∈E
                       𝑧𝑖 ∈ {−1, 1}     ∀𝑖 ∈ n

   Interestingly, the form of Eq. (67) also highlights that finding a maximal cut of G is equivalent to
finding a ground state of the antiferromagnet of G in an Ising model interpretation. We will use
Eq. (67) later in the next subsection to formulate a quantum problem Hamiltonian by replacing spin
variables 𝑧𝑖 with Pauli 𝑍 -operators acting on qubit 𝑖, 𝑍𝑖 = Id ⊗ . . . ⊗ Id ⊗ ( 10 −1
                                                                                    0 ) ⊗ Id ⊗ . . . ⊗ Id .
                                                               | {z }                     | {z }
                                                                        𝑖−1                             𝑛−𝑖

Heuristics and approximation algorithms. Given that the decision version of the Maximum Cut
problem is NP-hard [54], the Maximum Cut optimization problem is often approached by heuristic
algorithms [44]. These are algorithms for which one cannot provide guarantees on their performance,
but which are often observed to perform well on typical instances. A simple example would be the
search for local improvements, where nodes are moved from one set of the cut to the other, if this
strictly (or monotonically) increased the cut size. While heuristics may perform very well on most
instances, it is generally difficult to tell when they get stuck in a local optimum (or end up in a
loop, respectively). As heuristics do not always achieve the perfect solution, one can measure their
performance on an individual instance 𝐼 via an approximation ratio, defined as the algorithm’s
                                                         𝐴(𝐼 )
solution value 𝐴(𝐼 ) versus the optimal value OPT(𝐼 ), OPT(𝐼   ).
   A different approach is the design of a polynomial-time 𝑟 -approximation algorithm 𝐴, for which
                                                                                         𝐴(𝐼 )
one proves an approximation ratio 𝑟 over all possible input instances 𝐼 : 𝑟 = min𝐼 OPT(𝐼       ) < 1
                                             𝐴(𝐼 )
for maximization problems (or 𝑟 = max𝐼 OPT(𝐼       ) > 1 for minimization problems). In the case of
randomized (classical or quantum) algorithms, the deterministic value 𝐴(𝐼 ) in the definition of the
approximation ratio is replaced by the expected value E[𝐴(𝐼 )] of the solution given by the algorithm.
A prominent example for the Maximum Cut problem is the 0.878..-approximation algorithm by
Goemans and Williamson [61], which first solves a semi-definite programming relaxation of the
problem followed by a randomized hyperplane rounding of the SDP solution. Assuming the unique
games conjecture, this is the best possible polynomial-time approximation ratio [77] for MaxCut,
which on the other hand is only known to be NP-hard to approximate within 0.941.. + 𝜀 [68].
Interestingly, for graphs of maximum degree 3, it is possible to improve on Goemans-Williamson
Quantum Algorithm Implementations for Beginners                                                                                 55



                                                                                            classically
                                                                                           optimize β, γ

|0i       H                       e−iβ[1]X                                      e−iβ[r]X



                                                                                                       multiple samples
                                                                                                                          ⇒ hβ, γ| C |β, γi
|0i       H                       e−iβ[1]X                                      e−iβ[r]X
                   e   −iγ[1]C                      ...         e   −iγ[r]C
|0i       H                       e−iβ[1]X                                      e−iβ[r]X

|0i     H                         e−iβ[1]X                                      e−iβ[r]X
       P
 √1        |xi |                                     {z                                    }
  2n
    x∈{0,1}n                                      r rounds


Fig. 34. A high-level view of the hybrid quantum-classical Quantum Approximate Optimization Algorithm:
Starting from a uniform superposition over all computational basis states, the quantum subroutine alternat-
ingly applies the quantum problem Hamiltonian C and a transverse field B = 𝑗 𝑋 𝑗 for times 𝛾 [1 : 𝑟 ] and
                                                                                    Í
𝛽 [1 : 𝑟 ], respectively, to prepare the state |𝛽, 𝛾⟩. Collecting multiple samples from |𝛽, 𝛾⟩, one can estimate
the expectation ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ and use a classical optimizer to adjust the the parameters 𝛽, 𝛾. This eventually
results in a state |𝛽, 𝛾⟩ of high expectation value, from which one can sample solutions of high objective value.



by combining SDP relaxation & rounding with the aforementioned local improvement heuristic,
taylored to low-degree nodes, achieving a polynomial-time approximation ratio of 0.932.. [64].
  When we assume – as is commonly believed – that quantum computers cannot solve NP-
hard problems in polynomial time (i.e. NP ⊄ BQP), then there are two routes for the design of
quantum algorithms for combinatorial optimization problems: polynomial speedups for existing
approximation algorithms or new quantum heuristics. The Quantum Approximate Optimization
Algorithm (QAOA) studied in this section is such a quantum heuristic. Only in rare cases an
approximation ratio was shown for QAOA, among them a 0.692..-approximation for the MaxCut
problem on 3-regular graphs (where all nodes have degree 3) [50].

12.2   Algorithm description
The Quantum Approximate Optimization Algorithm (QAOA) as proposed in [50] is a hybrid
quantum-classical heuristic algorithm. It leverages gate-based quantum computing for finding
candidate solutions to combinatorial optimization problems that have the form of Eq. (65), using a
variational circuit with parameters tuned in a classical outer loop (Fig. 34).
   To apply the quantum subroutine, the user first translates the clause functions 𝐶𝛼 (𝑧) into
equivalent
     Í       quantum clause Hamiltonians C𝛼 , which give rise to the quantum problem Í Hamiltonian
C = 𝛼 C𝛼 . Additionally, one defines a transverse field mixing Hamiltonian B = 𝑖 𝑋 𝑗 with Pauli
𝑋 -operators ( 01 10 ) acting on qubits 𝑗. Finally, the user defines a number of rounds 𝑟 ≥ 1 and two
angles per round, 0 ≤ 𝛽 [𝑘] ≤ 𝜋 and 0 ≤ 𝛾 [𝑘] ≤ 2𝜋 for the 𝑘-th round. Starting in a uniform
superposition |+⟩ ⊗𝑛 of all 𝑛-bit computational basis states, the quantum subroutine then prepares a
state |𝛽, 𝛾⟩ by alternatingly applying the Hamiltonians C and B for times 𝛾 [𝑘], 𝛽 [𝑘]. The former
operation corresponds to a unitary 𝑒 −𝑖𝛾 [𝑘 ]C which phases each basis state by an angle proportional
to its objective value and proportional to 𝛾 [𝑘]. It can be implemented by applying each clause
Hamiltonian C𝛼 on its own. The second operation corresponds to unitaries 𝑒 −𝑖𝛽 [𝑘 ]𝑋 𝑗 applied to
each qubit 𝑗 (see pseudocode in Algorithm 12). The goal is to prepare a state |𝛽, 𝛾⟩ such that one
56                                                                                           Abhijith J., et al.


Algorithm 12 Quantum subroutine of the Quantum Approximate Optimization Algorithm
     Input:
           • Number of rounds of optimization 𝑟
           • Two size 𝑟 array of angles, 𝛾 and 𝛽.
           • Hamiltonians C𝛼 corresponding to the clauses of the optimization problem.
     Output:
           • An approximation to the solution of problem in Eq. (65).
     Procedure:
           Step 1. Construct the 𝑛-qubit uniform superposition state by applying 𝐻 ⊗𝑛 to |0 . . . 0⟩
           for 1 ≤ 𝑘 ≤ 𝑟 do
                                           𝑒 −𝑖𝛾 [𝑘 ]C𝛼
                                      Î
                   Step 2a. Apply 𝑚
                                      Î𝛼=1
                   Step 2b. Apply 𝑗=1 𝑒 −𝑖𝛽 [𝑘 ]𝑋 𝑗
                                        𝑛

           end for
           Step 3. We call the state so constructed |𝛽, 𝛾⟩.
     Preparing and measuring |𝛽, 𝛾⟩ multiple times allows to both estimate the expectation value
     Í𝑚
       𝛼=1 ⟨𝛽, 𝛾 |C𝛼 |𝛽, 𝛾⟩ , and to sample an approximate solution to the problem of objective value of
     at least the expectation minus 1 (with high probability).


can indeed sample candidate solutions of objective value as close to the optimum value as possible.
This, however, heavily depends on the choice of the parameters 𝑟, 𝛽, 𝛾.
Parameter finding and relation to the adiabatic theorem. To find parameters 𝛽, 𝛾 that enable sampling
of good candidate solutions to Eq. (65) (for a given round 𝑟 ), one usually resorts to optimize 𝛽, 𝛾
for a large expectation value ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩, where the optimization is done through a classical
optimizer outer loop, see Fig. 34. The reason for this is two-fold: Assuming every solution has
an objective value in the range 0, . . . , 𝑚, with high probability ≥ 1 − 𝑚1 the number of samples
sufficient to (i) sample at least one solution of value at least (⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ − 1) is 𝑚 log 𝑚 [50], and
to (ii) precisely estimate ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ is 𝑚 3 [35], which can be further reduced if the distribution
of C is concentrated around the expectation, e.g. to 𝑚 2 for MaxCut on bounded-degree graphs with
a small number 𝑟 of QAOA rounds [50].
   On an ideal noise-free quantum computer, an increase in the number of rounds 𝑟 should lead
to a monotonic increase in the quality of the expectation value ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩, provided that the
chosen angles 𝛽, 𝛾 are optimal. In fact, any 𝑟 -round QAOA with 𝛽 [𝑟 ] = 𝛾 [𝑟 ] = 0 corresponds
simply to a (𝑟 − 1)-round QAOA with parameters 𝛽 [1 : 𝑟 − 1], 𝛾 [1 : 𝑟 − 1], hence the optimal
expectation value is non-decreasing in the number of rounds. One can also show that with an
increasing number of rounds, in the limit 𝑟 → ∞ with suitably chosen angles 𝛽, 𝛾, the expectation
value will converge to the optimum value: lim𝑟 →∞ max𝛽,𝛾 ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ = max 𝐶 (𝑧). To this end, we
consider a quantum adiabatic algorithm [51] running for time 𝑇 with time-dependent Hamiltonian
𝐻 (𝑡) = (1 − 𝑡/𝑇 )B + (𝑡/𝑇 )C. The starting state of QAOA, |+⟩ ⊗𝑛 , is also the starting state and unique
highest energy eigenstate of 𝐻 (0) = B. Running the quantum adiabatic algorithm sufficiently
slow (𝑇 ≫ poly(𝑛)) thus results in a highest energy eigenstate of 𝐻 (𝑇 ) = C, provided the energy
difference between the highest and the second highest eigenstate of 𝐻 (𝑇 ) is strictly positive for all
𝑡 < 𝑇 . This is the case by the Perron-Frobenius theorem whenever C has only non-negative entries
since B is non-negative irreducible matrix, in particular for combinatorial      Í optimization problems.
Quickly alternating between B and C with suitable angles 𝛽, 𝛾 such that 𝑟 𝛽 [𝑟 ] + 𝛾 [𝑟 ] = 𝑇 gives a
discretization (or so-called Trotterization) of the adiabatic algorithm, with improving precision and
improving expectation value max𝛽,𝛾 ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ for increasing 𝑟 .
Quantum Algorithm Implementations for Beginners                                                                             57


   However, while QOAO may certainly be looked at as inspired by the quantum adiabatic algorithm,
there are problems for which the latter fails for subexponential runtimes while QAOA succeeds
even in a single round [50]. Furthermore, for MaxCut on 3-regular graphs, 1-round QAOA was
shown to give a 0.692..-approximation. No approximation ratios have been shown for more than 1
round and thus in this regime QAOA is purely heuristic. However, there are known limitations for
small/constant-round QAOA approaches: for larger node degrees and sublogarithmic number of
rounds 𝑟 ∈ 𝑜 (log 𝑛) the approximation ratio is limited by ≈ 0.834 [25].
   So, what strategies of classical optimizers are there to tune the angles 𝛽, 𝛾 for a given 𝑟 -round
QAOA subroutine? In the original QAOA proposal, an exhaustive search over a fine cartesian grid is
suggested for small constant 𝑟 [50], where the number of grid points is polynomial in 𝑛. This works
because ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ does not have narrow peaks that fall between grid points. Other approaches
are necessary for larger 𝑟 , but we have to be aware that the parameter landscape is non-convex and
thus most classical optimization techniques cannot provide a guarantee for confergence to optimum
parameters. Possible optimizers for angle-finding have been extensively studied and are based on
techniques such as gradient descent [59, 129], optimal control [22, 135], interpolation of angles
for a 𝑟 -round QAOA based on good angles for a (𝑟 − 1) rounds [138], and basin-hopping [94, 130].
For example, basin-hopping starts with random angles, locally optimizes the solution and then
randomly perturbs the found angles more significantly to explore a new basin to try to find a better
local optima. The use of a quantum-variational-eigensolver is also possible [89, 96].


A closer look at the quantum Hamiltonians. We discuss the translation of the clauses of a combi-
natorial problem in the form of Equation (65) to quantum clause Hamiltonians by the MaxCut
and note generalizations along Í the way. Recall that we have already discussed how to transform a
combinatorial problem max 𝛼 𝐶𝛼 (𝑥) with binary variables 𝑥𝑖 ∈ {0, 1} (see Eq. (66)) into a com-
                           Í
binatorial problem max 𝛼 𝐶𝛼 (𝑧) with spin variables 𝑧𝑖 ∈ {−1, 1} (see Eq. (67)) using the linear
transformation 𝑥𝑖 = (𝑧𝑖 + 1)/2. To formulate a quantum clause Hamiltonian C𝛼 , we replace in the
clause 𝐶𝛼 (𝑧) each constant 1 with the identity Id ⊗𝑛 = ( 10 01 ) ⊗𝑛 and each spin variable 𝑧𝑖 with Pauli
                  0 ) acting on qubit 𝑖, 𝑍 = Id ⊗𝑖−1 ⊗ 𝑍 ⊗ Id ⊗𝑛−𝑖 .
𝑍 -operators ( 10 −1                      𝑖
   We note that the MaxCut problem is particularly advantageous for QAOA for the following
reasons: (1) all of the clauses in the objective function have the same structure, hence a circuit
implementation has only to be found for one unitary 𝑒 −𝑖𝛾 C𝛼 ; (2) each clause only involves two
decision variables, which keeps the structure of C𝛼 relativity simple. We note that we have 𝑍𝑖 · 𝑍 𝑗 =
Id ⊗𝑖−1 ⊗ 𝑍 ⊗ Id ⊗ 𝑗−𝑖 ⊗ 𝑍 ⊗ Id ⊗𝑛−𝑗 . As an example, for the MaxCut problem on the 2-edge path
○— 2
 1   ○— 3○, we get a maximization function 𝐶 (𝑧) and a quantum problem Hamiltonian C:




        1                1
   𝐶 (𝑧) =(1 − 𝑧 1𝑧 2 ) + (1 − 𝑧 2𝑧 3 ) = 𝐶 12 (𝑧) + 𝐶 23 (𝑧)
        2                2
        1                  1
   ⇒ C = (Id − 𝑍 1𝑍 2 ) + (Id − 𝑍 2𝑍 3 ) = C12 + C23                                                                    (68)
        2                  2
                  10000000              10 0    0   0   0 00              10000000              1 0   0 00 0     0 0
            ©© 0 1 0 0 0 0 0 0            © 0 1 0 00 00 00 00 00 ªª   ©© 0 1 0 0 0 0 0 0 ª © 0 −1 0 00 00 00 00 00 ªª
          1 ­­ 00 00 10 01 00 00 00 00 ª® ­ 00 00 −1 −1          ®® 1 ­­ 00 00 10 01 00 00 00 00 ® ­ 00 00 −1
         = ­­ 0 0 0 0 1 0 0 0 ® − ­ 0 0 0 0 −1 0 0 0 ®® + ­­ 0 0 0 0 1 0 0 0 ® − ­ 0 0 00 10 01 00 00 00 ®®
                                                   0    0 0 0  0                                                       ®®
          2 ­­ 0 0 0 0 0 1 0 0 ® ­ 0 0 0 0 0 −1 0 0 ®® 2 ­­ 0 0 0 0 0 1 0 0 ® ­ 0 0 0 0 0 −1 0 0 ®®
                00000010                     00 0 0 0 0 10                00000010                    0 0 0 0 0 0 −1 0
            «« 0 0 0 0 0 0 0 1 ¬ « 0 0 0 0 0 0 0 1 ¬¬                 «« 0 0 0 0 0 0 0 1 ¬ « 0 0 0 0 0 0 0 1 ¬¬
58                                                                                               Abhijith J., et al.




                      |000⟩   |001⟩   |010⟩   |011⟩   |100⟩    |101⟩     |110⟩    |111⟩
                        0       0       0       0       0        0         0        0      |000⟩
                    © 0
                    ­           1       0       0       0        0         0        0 ª®   |001⟩
                    ­ 0
                    ­           0       2       0       0        0         0        0 ®®   |010⟩
              C =
                    ­ 0
                    ­           0       0       1       0        0         0        0 ®®   |011⟩              (69)
                    ­ 0
                    ­           0       0       0       1        0         0        0 ®®   |100⟩
                    ­ 0
                    ­           0       0       0       0        2         0        0 ®®   |101⟩
                    ­ 0         0       0       0       0        0         1        0 ®    |110⟩
                    « 0         0       0       0       0        0         0        0 ¬    |111⟩


   Above, Eq. (68) shows the transformation of the maximization function 𝐶 (𝑧) into the quantum
Hamiltonian C, and Eq. (69) illustrate how the quantum Hamiltonian encodes the inputs and outputs
of the different cuts. We note that both clause terms C12 = 21 (Id − 𝑍 1𝑍 2 ) and C23 = 12 (Id − 𝑍 2𝑍 3 )
are diagonal matrices, hence they commute and we have 𝑒 −𝑖𝛾 (C12 +C23 ) = 𝑒 −𝑖𝛾 C12 · 𝑒 −𝑖𝛾 C23 . Similarly,
for the mixing Hamiltonian B = 𝑗 𝑋 𝑗 the 𝑋 𝑗 pairwise commute, and we have 𝑒 −𝑖𝛽B = 𝑗 𝑒 −𝑖𝛽𝑋 𝑗
                                      Í                                                          Î
as used in Algorithm 12.
   Finally, we discuss the influence of the forms of C and B on the bounds on the angles 𝛾, 𝛽. Since
C is a diagonal matrix with integer eigenvalues, we get that 𝑒 −𝑖𝛾 C is 2𝜋-periodic in 𝛾 and we get
0 ≤ 𝛾 ≤ 2𝜋. For B we have 𝑒 −𝑖 (𝜋 +𝛽)𝑋 = 𝑒 −𝑖𝜋𝑋 · 𝑒 −𝑖𝛽𝑋 = −Id · 𝑒 −𝑖𝛽𝑋 , hence 𝑒 −𝑖𝛽B is (up to a global
phase) 𝜋-periodic in 𝛽 and we get 0 ≤ 𝛽 ≤ 𝜋.
   By looking specifically at MaxCut, we can further narrow the angle bounds: we have 𝑒 −𝑖𝜋 /2𝑋 =
( −𝑖 −𝑖0 ), i.e. increasing 𝛽 in 𝑒 −𝑖𝛽B by 𝜋/2 only adds a global phase and swaps 0/1 values of all
  0

variables and thus the two cut sets. Hence ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ is even only 𝜋2 -periodic in 𝛽. Using these
periodicities, we observe

                𝜋               𝜋
                2 − 𝛽, 2𝜋 − 𝛾 C 2 − 𝛽, 2𝜋 − 𝛾      = ⟨−𝛽, −𝛾 | C |−𝛽, −𝛾⟩ = ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ ,                (70)

where the last equality comes from the fact that C and B are real valued and satisfy time reversal
symmetry. This cuts our angle search space further in halfs, and we can restrict our angle search
space to 0 ≤ 𝛽 [𝑘] ≤ 𝜋2 and 0 ≤ 𝛾 [𝑘] ≤ 𝜋.

12.3   QAOA MaxCut on ibmqx2
This section investigates the implementation of the QAOA MaxCut algorithm on the ibmqx2
quantum computer (Figure 35). The first challenge is to transform the QAOA algorithm from its
mathematical form into a sequence of operations that are available in the IBM Quantum Experience
platform. For the sake of convenience we will mention here the gates we will use in the ensuing
discussion,


                                                                                      1        0   0     0
          1 0                            cos(𝜃 /2)        −𝑒 𝑖𝜆 sin(𝜃 /2)                ­0        1   0     0®
                                                                                         ©                     ª
𝑈 1 (𝜆) =          ,    𝑈 3 (𝜃, 𝜙, 𝜆) = 𝑖𝜙                                    ,   CNOT = ­                     ®.
          0 𝑒 𝑖𝜆                        𝑒 sin(𝜃 /2)     𝑒 𝑖 (𝜆+𝜙) cos(𝜃 /2)              ­0        0   0     1®
                                                                                         «0        0   1     0¬
Quantum Algorithm Implementations for Beginners                                                                                           59


ibmqx2
                                                                            1                           1                         1

                                                                 0          2       3         0         2       3        0        2   3

                                                                            4                           4                         4


                                                                  Single Edge                     Triangle             Triangle plus Edge


Fig. 35. The CNOT connectivity and error rates of the ibmqx2 Computer (left) followed by the Single Edge
(center left), Triangle (center right) and four edge Triangle+Edge (right) graphs considered in the proof-of-
concept experiments.


  The inner loop of the algorithm first requires the application of the 𝛾 angle with the clause
Hamiltonians. For the MaxCut Hamiltonian, this can be expanded as follows,
                                      0000
                                                   !
                                                          1  0              0   0
                                 −𝑖𝛾 00 10 01 00
                                                        ­0 𝑒 −𝑖𝛾            0®  0
              𝛾
                                                        ©                     ª
         𝑒 −𝑖 2 (Id−𝑍 1𝑍 2 ) = 𝑒      0000             =­                                                                             (71)
                                                        ­0   0       𝑒 −𝑖𝛾 0®
                                                                              ®

                                                        «0   0         0    1¬
                                                          1      0 0 0     1    0   0   0      1                    0 0      0
                                                        ­0       1 0 0® ­0 𝑒 −𝑖𝛾 0      0 ® ­0                      1 0      0®
                                                        ©               ª ©                 ª ©                               ª
                                                       =­               ®·­                 ®·­
                                                        ­0       0 0 1® ­0      0   1   0 ® ­0                      0 0      1®
                                                                                                                              ®

                                                        «0       0 1 0¬ «0      0   0 𝑒 −𝑖𝛾 ¬ «0                    0 1      0¬
                                                        |         {z   } |        {z       } |                       {z       }
                                                                 CNOT12                 Id ⊗𝑈 1 (−𝛾 )               CNOT12

i.e., we observe that this gate can be implemented as a combination of two CNOT gates and one
𝑈 1 (−𝛾) gate, as indicated in Figure 36. It is also interesting to note the alternate implementation
of this gate in [34], which leverages a different variety of gate operations [116]. We also remark
here that the CNOT gates can be interpreted as computing and uncomputing the parity of qubits
1 and 2 inline, with the phase shift of the 𝑈 1 (−𝛾) gate applied to odd parities. For higher than
quadratic terms of 𝑍 -operators (such as 𝑍𝑖 𝑍 𝑗 𝑍𝑘 terms in the MaxE3Lin2 problem [49]), parities can
be computed by CNOT gates from all other qubits into a central qubit.

                                                                          U1
                                                                         (-gamma)




 Fig. 36. An IBM Quantum Experience score illustrating an implementation of the MaxCut edge gate (71).


  The next term in the loop is the application of the 𝛽 angle, which is expanded as follows,
                                                                     !
                                                             0    1
                                                       −𝑖𝛽                                                 
                                        −𝑖𝛽𝑋                 1    0 = cos(𝛽)              −𝑖 sin(𝛽)
                                    𝑒          =𝑒                                                                                     (72)
                                                                       −𝑖 sin(𝛽)           cos(𝛽)
Careful inspection of the IBM Quantum Experience gates reveals that this operation is implemented
by 𝑈 3 (2𝛽𝑘 , −𝜋/2, 𝜋/2). So we need to apply this gate to every qubit in the register. Putting all of these
components together, Figure 37 presents an IBM Quantum Experience circuit for implementing the
60                                                                                                                                         Abhijith J., et al.
q[0]

q[1]   H                                                      U3                                                           U3
                                                             (0.942...)                                                   (0.314...)



q[2]   H        U1            U1                 U1           U3           U1                    U1           U1           U3
               (-0.62...)    (-0.62...)         (-0.62...)   (0.942...)   (-1.25...)            (-1.25...)   (-1.25...)   (0.314...)



q[3]   H                                         U1           U3                                              U1           U3
                                                (-0.62...)   (0.942...)                                      (-1.25...)   (0.314...)



q[4]   H                                                      U3                                                           U3
                                                             (0.942...)                                                   (0.314...)




  c5
                                                                                                                                       1     2     3    4



Fig. 37. An IBM Quantum Experience circuit for 2-round QAOA of MaxCut on the “Triangle plus Edge” graph.
We can see the edge gate from Figure 36 replicated for the edges of the triangle between qubits 𝑞[2], 𝑞[3], 𝑞[4]
as well as the edge between qubits 𝑞[1], 𝑞[2]. Similarly, the vertical layers of 𝑈 3 gates implement 𝑒 −𝑖𝛽B .


quantum subroutine of QAOA for MaxCut on the “Triangle plus Edge” graph from Figure 35 with
parameters,
                            𝑟 = 2 : 𝛾 1 = 0.2 · 𝜋 = 0.628..,                           𝛽 1 = 0.15 · 𝜋 = 0.471..,
                                          𝛾 2 = 0.4 · 𝜋 = 1.256..,                     𝛽 2 = 0.05 · 𝜋 = 0.157...


12.4   A proof-of-concept experiment
With a basic implementation of QAOA for MaxCut in qiskit, a preliminary proof-of-concept study
is conducted to investigate the effectiveness of QAOA for finding high-quality cuts in the a) Single
Edge, b) Triangle and c) Triangle plus Edge graphs presented in Figure 35. For both a) and b), we
ran a numerical grid search for a for a 1-round QAOA with resolution 18 𝜋 and 10   1
                                                                                     𝜋, respectively,
using qiskit’s statevector_simulator. The statevector simulator allows for exact evaluation of
the expectation value ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩. In both cases, we found parameters 𝛽, 𝛾 resulting in a state
representing an optimum cut. For c), we ran a grid search on the statevector simulator for both
                                            1        1
1- and 2-round QAOA with resolution 1000      𝜋 and 20 𝜋 respectively. The parameter landscape for 1
round is given in Fig. 38 and overlayed with a basin-hopping approach.
   We then executed the QAOA subroutine for the best-found parameters on Hardware by execut-
ing the IBM Quantum Experience circuit on the ibmqx2 device using 4096 shots, and compared
the results to a Simulation with the same number of shots using the qasm_simulator. For both
computations we give the expectation/mean of the returned solutions and the probability to sample
the maximum cut and contrast these with the values for a Random cut. The simulation compu-
tation serves to demonstrate the mathematical correctness of the proposed QAOA circuit. The
hardware computation demonstrates the viability of the circuit in a deployment scenario where
environmental noise, intrinsic bias, and decoherence can have a significant impact on the results.
The random computation serves to demonstrate that the hardware results are better than what one
would expect by chance from pure noise.
   a) The first shot experiment considers the Single Edge graph from Figure 35 (center left) and
implements a 1-round QAOA with the parameters
                                            𝑟 = 1 : 𝛾 1 = 0.5 · 𝜋,                     𝛽 1 = 0.125 · 𝜋 .
The results are summarized in Table 4. The simulation results indicate that the proposed score is
mathematically sound and the hardware results indicate similar performance to the simulation,
with a few additional errors. The random results indicate that both the simulation and hardware
perform significantly better than random chance.
  b) The second shot experiment considers the Triangle graph from Figure 35 (center right) with
parameters
                                𝑟 = 1 : 𝛾 1 = 0.8 · 𝜋, 𝛽 1 = 0.4 · 𝜋 .
Quantum Algorithm Implementations for Beginners                                                                    61


                          Table 4. MaxCut QAOA with one round on a Single Edge.


                                                           Random        Simulation       Hardware
             Expected Size of a sampled cut                     0.500           1.000           0.950
             Probability of sampling a maximum cut              0.500           1.000           0.950


The results are summarized in Table 5. The simulation results indicate that the proposed circuit
is mathematically sound. Even though the QAOA circuit for a Triangle is longer than the QAOA
circuit for a Single Edge, the Hardware performance is better, most likely due to the more favourable
distribution of the cuts, also notable in Random.

                           Table 5. MaxCut QAOA with one round on a Triangle.


                                                           Random        Simulation       Hardware
             Expected Size of a sampled cut                     1.500           1.999           1.904
             Probability of sampling a maximum cut              0.750           1.000           0.952

   c) The third shot experiment considers the Triangle plus Edge graph from Figure 35 (right). We
run QAOA both in a 1-round and a 2-round scenario, implemented with the following parameters,
found through numerical grid searches with a resolution of 𝜋/1000 (1-round) and 𝜋/20, respectively
(2-round):
          𝑟 = 1 : 𝛾 1 = 0.208 · 𝜋,   𝛽 1 = 0.105 · 𝜋 .       𝑟 = 2 : 𝛾 1 = 0.2 · 𝜋,       𝛽 1 = 0.15 · 𝜋,
                                                                        𝛾 2 = 0.4 · 𝜋,    𝛽 2 = 0.05 · 𝜋 .

                      1-round QAOA: MaxCut of Triangle+Edge
    1.0
                                                                                                             2.5
    0.8
                                                                                                             2.0
    0.6
                                                                                                               , |C| ,
                                                                                                             1.5
/
    0.4
                                                                                                             1.0
    0.2
                                                                                                             0.5
    0.0
       0.0      0.2      0.4     0.6      0.8      1.0    1.2      1.4        1.6        1.8     2.0
                                                    /
Fig. 38. (Heatmap) Parameter landscape for a 1-round QAOA for MaxCut on the Triangle+Edge instance. We
observe the symmetry ⟨𝛽, 𝛾 | C |𝛽, 𝛾⟩ = 𝜋2 − 𝛽, 2𝜋 − 𝛾 C 𝜋2 − 𝛽, 2𝜋 − 𝛾 derived in Eq. (70). (Overlay) Using a
basin-hopping optimizer: A random initialization first explores a basin finding a local maximum; a random
perturbation next hops to worse-than-random parameters, but the exploration then finds a global optimum.
62                                                                                        Abhijith J., et al.


The results are summarized in Table 6, the 2-round circuit is shown in Figure 37. Simulation and
Hardware outperform Random both on 1-round and 2-round QAOA. However, the gains made
by Simulation in 2-round over 1-round QAOA almost vanish on the Hardware. This degradation
in performance is likely due to the double length in the circuit, making the experiment more
susceptible to gate errors, environmental noise and qubit decoherence.

               Table 6. MaxCut QAOA with several rounds on a Triangle plus Edge graph.


                                                           1-round QAOA          2-round QAOA
                                               Random      Simul.   Hardw.       Simul.     Hardw.
     Expected Size of a sampled cut                2.000    2.720     2.519       2.874         2.570
     Probability of sampling a maximum cut         0.375    0.744     0.652       0.895         0.727


Towards practical relevance. When going from the toy problems studied in this subsection towards
relevant problems, many problems and issues present themselves. A recent study explored these in
detail [65], here we just note a few of these questions:
   For example, the studied graphs would likely not fit the (planar) hardware connectivity of an
actual device; instead they might come from a random Erdős–Rényi, a random 𝐷-regular graph, or
even a dense graph such as in the Sherrington-Kirkpatrick model (a MaxCut problem for complete
graphs with edge weights). In the case of sparse graphs, one could resort to heuristic compilers
implementing SWAP operations to bring qubits representing adjacent nodes together. For dense
graphs (or hypergraphs), one can use (generalized) swap networks instead, which swap qubits such
that all pairs (sets) are adjacent at some point during its execution [93]. All of these choices affect
the quality of sampled solutions in the presence of noise.
   This gives rise to the question of up to which problem size and number of rounds the quality of
sampled solutions can be increased without gains disappearing due to noise. (A similar question
also arises even for idealized quantum devices, if one limits the number of evaluations a classical
optimizer can take; in this case a QAOA with fewer rounds might perform better due to the smaller
and thus better explored parameter search space [35].)
   As of now, quantum advantage for QAOA has not been achieved yet. Current devices are still too
noisy and the possible instances too small. Whether QAOA can achieve a significant speedup for
combinatorial optimization problems, or whether it enables better provable approximation ratios,
remains open.

13     QUANTUM PRINCIPAL COMPONENT ANALYSIS
13.1    Problem definition and background
In data analysis, it is common to have many features, some of which are redundant or correlated.
As an example, consider housing prices, which are a function of many features of the house, such
as the number of bedrooms, number of bathrooms, square footage, lot size, date of construction,
and the location of the house. Often, one is interested in reducing the number of features to the few,
most important features. Here, by important, we mean features that capture the largest variance in
the data. For example, if one is only considering houses on one particular street, then the location
may not be important, while the square footage may capture a large variance.
   Determining which features capture the largest variance is the goal of Principal Component
Anaylsis (PCA) [95]. Mathematically, PCA involves taking the raw data (e.g., the feature vectors for
Quantum Algorithm Implementations for Beginners                                                       63


various houses) and computing the covariance matrix, Σ. For example, for two features, 𝑋 1 and 𝑋 2 ,
the covariance is given by
                                                                 
                                      E(𝑋 1 ∗ 𝑋 1 ) E(𝑋 1 ∗ 𝑋 2 )
                               Σ=                                   ,                         (73)
                                      E(𝑋 2 ∗ 𝑋 1 ) E(𝑋 2 ∗ 𝑋 2 )
where E(𝐴) is the expectation value of 𝐴, and we have assumed that E(𝑋 1 ) = E(𝑋 2 ) = 0. Next, one
diagonalizes Σ such that the eigenvalues 𝑒 1 ≥ 𝑒 2 ≥ 𝑒 3 ≥ · · · are listed in decreasing order. Again,
for the two-feature case, this becomes
                                                       
                                               𝑒1 0
                                          Σ=              .                                        (74)
                                                0 𝑒2
Once Σ is in this form, one can choose to keep the features with 𝑛-largest eigenvalues and discard
the other features. Here, 𝑛 is a free parameter that depends on how much one wants to reduce the
dimensionality. Naturally, if there are only two features, one would consider 𝑛 = 1, i.e., the single
feature that captures the largest variance.
   As an example, consider the number of bedrooms and the square footage of several houses for
sale in Los Alamos. Here is the raw data, taken from www.zillow.com, for 15 houses:
𝑋 1 = number of bedrooms = {4, 3, 4, 4, 3, 3, 3, 3, 4, 4, 4, 5, 4, 3, 4}
𝑋 2 = square footage = {3028, 1365, 2726, 2538, 1318, 1693, 1412, 1632, 2875, 3564, 4412, 4444, 4278, 3064, 3857} .
                                                                                                   (75)
Henceforth, for scaling purposes, we will divide the square footage by 1000 and subtract off the
mean of both features. Classically, we compute the covariance matrix and its eigenvalues to be the
following:
                                          
                         0.380952 0.573476
                  Σ=                         , 𝑒 1 = 1.57286 , 𝑒 2 = 0.105029 .               (76)
                         0.573476 1.29693
   We now discuss the quantum algorithm for doing the above calculation, i.e., for finding the
eigenvalues of Σ.

13.2    Algorithm description
Before we discuss the algorithm we will provide a quick introduction to the concept of a density
matrix. Density matrices are used to represent probabilistic mixtures of quantum states. Suppose
that there is a quantum system whose state is not known, rather we know that it can be in one of
𝑀 states, |𝜓𝑖 ⟩, each occurring with probability 𝑝𝑖 . The state of this system is then represented by a
density matrix 𝜌, defined as
                                              𝑀
                                             ∑︁
                                         𝜌=      𝑝𝑖 |𝜓𝑖 ⟩ ⟨𝜓𝑖 | .                                  (77)
                                                   𝑖=1
If the state of a system is known (with probability 1) to be |𝜓 ⟩, then the density matrix would just
be |𝜓 ⟩ ⟨𝜓 | and the system is said to be in a pure state. Otherwise, the system is said to be in a mixed
state. So the density matrix can be seen as a generalization of the usual state representation with
the extra ability to represent a probabilistic mixture of quantum states. From the definition of the
density matrix it can be seen that it is a positive semi-definite matrix with unit trace. In fact, any
matrix that satisfies these two properties can be interpreted as a density matrix. More details on
the definition and interpretation of density matrices are given in the quantum tomography section
(Section 19).
   Density matrices are clearly more expressive than state vectors as state vectors can only represent
pure states. But, even a system in a mixed state can be seen as a part of a larger system that is in
64                                                                                          Abhijith J., et al.


a pure state. This process of converting a mixed state into a pure state of an enlarged system is
called purification. A mixed state of an 𝑛 qubit system can be purified by adding 𝑛 more qubits
and working with the 2𝑛 qubit system. Once purified, the joint system of 2𝑛 qubits will be in a
pure state while the first 𝑛 qubits will still be in the original mixed state. We will not discuss the
transformations required to purify a state. Interested readers are referred to Ref. [92] for a complete
discussion.
   The quantum algorithm for performing PCA presented in Ref. [85] uses the density matrix
representation. The algorithm discussed there has four main steps: (1) encode Σ in a quantum
density matrix 𝜌 (exploiting the fact that Σ is a positive semi-definite matrix), (2) prepare many
copies of 𝜌, (3) perform the exponential SWAP operation on each copy and a target system, and (4)
perform quantum phase estimation to determine the eigenvalues. For an implementation of this
quantum PCA algorithm on a noisy simulator, we refer the reader to Ref. [81], which also gives a
short-depth compilation of the exponential SWAP operation.
   However, given the constraint of only 5 qubits on IBM’s computer, preparing many copies of 𝜌
is not possible. Hence, we consider a simpler algorithm as follows. In the special case where there
are only two features, Σ and 𝜌 are 2 × 2 matrices (one qubit states), and 𝜌 can be purified to a pure
state |𝜓 ⟩ on two qubits. Suppose one prepares two copies of |𝜓 ⟩, which uses a total of 4 qubits,
then the fifth qubit (on IBM’s computer) can be used as an ancilla to implement an algorithm that
determines the purity 𝑃 := Tr(𝜌 2 ) of 𝜌. This algorithm was discussed, e.g., in Ref. [71]. It is then
straightforward to calculate the eigenvalues of Σ from 𝑃, as follows:
                                                    √︁
                                𝑒 1 = Tr(Σ) ∗ (1 + 1 − 2(1 − 𝑃))/2                                 (78)
                                                     √︁
                                𝑒 2 = Tr(Σ) ∗ (1 − 1 − 2(1 − 𝑃))/2 .                               (79)
We remark that recently (after completion of this review article), a simpler algorithm for computing
purity 𝑃 was given in Ref. [31]. While the results presented in what follows use the approach in
Ref. [71], the approach in Ref. [31] could lead to more accurate results.
   As depicted in Fig. 39, this simple algorithm is schematically divided up into four steps: (1) classical
pre-processing, (2) state preparation, (3) quantifying the purity, and (4) classical post-processing.
   In the first step, the classical computer converts the raw data vectors into a covariance matrix
Σ, then normalizes this matrix to form 𝜌 = Σ/Tr(Σ), then purifies it to make a pure state |𝜓 ⟩, and
finally computes the unitary 𝑈 prep needed to prepare |𝜓 ⟩ from a pair of qubits each initially in the
|0⟩ state.
   In the second step, the quantum computer actually prepares the state |𝜓 ⟩, or in fact, two copies
of |𝜓 ⟩, using 𝑈 prep , which can be decomposed as follows:
                                𝑈 prep = (𝑈𝐴 ⊗ 𝑈𝐵 )CNOT𝐴𝐵 (𝑈𝐴′ ⊗ 1𝐵 ) .                                  (80)
Note that 𝑈 prep acts on two qubits, denoted 𝐴 and 𝐵, and CNOT𝐴𝐵 is a CNOT gate with 𝐴 the
control qubit and 𝐵 the target. The single qubit unitaries 𝑈𝐴 , 𝑈𝐵 , and 𝑈𝐴′ can be written in IBM’s
standard form:
                                                                 
                                     cos(𝜃 /2)    −𝑒 𝑖𝜆 sin(𝜃 /2)
                                                                    ,                            (81)
                                  𝑒 𝑖𝜙 sin(𝜃 /2) 𝑒 𝑖𝜆+𝜙 cos(𝜃 /2)
where the parameters 𝜃 , 𝜆, and 𝜙 were calculated in the previous (classical pre-processing) step.
  The third step is purity calculation, which makes up the bulk of the quantum algorithm. As
shown in Fig. 39, first one does a Hadamard on an ancilla. Let us denote the ancilla as 𝐶, while the
other four qubits are denoted 𝐴, 𝐵, 𝐴 ′, and 𝐵 ′. During the state preparation step, qubits 𝐴 and 𝐵
were prepared in state |𝜓 ⟩ with the state of 𝐴 being 𝜌. Likewise we have the state of 𝐴 ′ to be 𝜌.
Next, qubit 𝐶 is used to control a controlled-SWAP gate, where the targets of the controlled-SWAP
                                                                                  FIG.p1:                                                                                 p p
 ofom
    ollows:
 This⌃P  from
 algorithm  , as
         algorithm   , as
                  Pfollows:follows:
                       iswasschematically
                               discussed              divided
                                             in Ref. XXX   e1 =Need state
                                                                       up
                                                                   Tr(⌃)     ⇤into
                                                                          citationpreparation,
                                                                                       four
                                                                                (1e1+=XX.
                                                                                        Tr(⌃)
                                                                                         1    It
                                                                                               e1steps:
                                                                                               2(1⇤is=(1then
                                                                                                          +
                                                                                                         Tr(⌃)
                                                                                                           P
                                                                                                             pquantifying
                                                                                                             ))/2classical
                                                                                                                 1⇤ (12(1
                                                                                                                           p
                                                                                                                straightforward    tothe     purity,
                                                                                                                               pre-processing,
                                                                                                                        + 1P ))/2 2(1   calculate
                                                                                                                                          P ))/2
                                                                                                                                              e    =the and        classical
                                                                                                                                                         eigenvalues
                                                                                                                                                      Tr(⌃)      ⇤ (6)
                                                                                                                                                                   (1  +     1 (
                                                                                       p                                                        1
 of
  ty,    from
     ⌃ and          , as  follows:
                  classical
                       pwas        post-processing.               p              p                           p             p
  hm
 This      is   schematically
        discussed
  lgorithm
  was    algorithm
  r(⌃)from
                  P
                  was          discussed
                        discussed
                         in  Ref.
          ⇤ (1 P+, as 1follows:      in
                                   XXX
                                2(1 e1 P
                                            divided
                                             in
                                            Need
                                          Ref.
                                           =))/2 Ref.
                                                 XXX
                                              Tr(⌃)     XXX
                                                          Need
                                                    citation
                                                           e
                                                    e1⇤=(12+up
                                                            Tr(⌃)1⇤ (12(1
                                                              1  =  into
                                                                 Need
                                                                  XX.
                                                                   Tr(⌃)  citation
                                                                   citation
                                                                          It ⇤ four
                                                                              is(1XX.
                                                                                  then
                                                                             + e21P +   steps:
                                                                                       XX.
                                                                                        It
                                                                                         straightforward
                                                                                          1
                                                                                      =))/2
                                                                                         2(1is
                                                                                        Tr(⌃) It2(1
                                                                                               e2⇤Pis
                                                                                                 hen =   classical
                                                                                                        then
                                                                                                          straightforward
                                                                                                           P
                                                                                                      (1))/2 ))/2   to    pre-processing,
                                                                                                                straightforward
                                                                                                         Tr(⌃)1⇤.(12(1          to
                                                                                                                        calculate
                                                                                                                       (6) 1P ))/2
                                                                                                                                   to
                                                                                                                                   the  calculate
                                                                                                                                                the
                                                                                                                                         eigenvalues
                                                                                                                                   calculate
                                                                                                                                  2(1. P ))/2 . (6) the  eigenvalues
                                                                                                                                                     eigenvalues   (6)
                                                                                                                                                                (6)(7)    p       (
 of
 dom classical
    ollows: ,          ppost-processing.
               as follows:
        Palgorithm                                                p              p p                                                          e2 = Tr(⌃) ⇤ (1                1
 This                     was discussed
                                      e    = in  Ref.
                                              Tr(⌃) e  ⇤XXX
                                                         = e12
                                                          (1    =Need
                                                            Tr(⌃)  Tr(⌃)
                                                                     1⇤ (1citation
                                                                             ⇤
                                                                           2(1  (1 +1P XX.
                                                                                         1
                                                                                       ))/2
                                                                                         2(1 .It2(1     then
                                                                                                   isP ))/2     straightforward to calculate (7)
                                                                                                             ))/2 .
                                                                                                           P .                                      the eigenvalues
                                                                                                                                                                (7)(6)
                                                                                                                                                                   (7)
    As depicted
  r(⌃)
 of       ⇤
         from (1 P , asin1As   depicted
                          follows:??,
                             Fig.2(1   As
                                        2     simple2??,inthis
                                               Fig.
                                            depicted
                                          Pin))/2
                                        this                      p ??,
                                                               Fig.
                                                         algorithm simple
                                                                        isthis algorithm
                                                                                 psimple
                                                                                       p is
                                                                            schematically        schematically
                                                                                            algorithm
                                                                                                 divided      isup into(7)four up
                                                                                                                        divided
                                                                                                                  schematically steps:into
                                                                                                                                   divided  four
                                                                                                                                         classical                             pre
                                                                                                                                                                      pre-processin
                                                                                                                                                              steps: classical
                                                                                                                                                           classical
                                                                                                                                                  steps:four
                                                                                                                                              up into
                                                                                                                                                    pre-processing,
                                                                                                                                                                     Classical    P
   tate   preparation, state        state
                               preparation,
                              quantifying
                                      e    =  thequantifying
                                            preparation,
                                              Tr(⌃)purity,
                                                    e  ⇤ = e12+
                                                          (1    = the
                                                               and
                                                            Tr(⌃)  Tr(⌃)
                                                                      ⇤      ⇤ (1the
                                                                     classical
                                                                     1  (1As
                                                                quantifying
                                                                        purity,
                                                                             +
                                                                           2(1      +    1classical
                                                                                  depicted
                                                                                    1  purity,
                                                                                     and
                                                                                       ))/2    2(1P
                                                                                   post-processing.
                                                                                     P   2(1       in
                                                                                                   and     P
                                                                                                          Fig.
                                                                                                           classical
                                                                                                         post-processing.
                                                                                                        ))/2 ))/2??,.    this   simple
                                                                                                                       post-processing.     algorithm
                                                                                                                                                   (6)       is  schematically
                                                                                                                                                                (6)(6)
                                                                                                                                                                   (7)
  n As
 depicted depicted
     Fig. ??,           in
                    Classical
                     Fig.
                inthis      ??,
                          simple   ??, this
                             Fig.this   1
                                    Pre-processing
                                       simple
                                    algorithm simple
                                                   is
                                                      1  algorithm
                                                       schematically
                                                  algorithm       is for is
                                                                  p         schematically
                                                                      schematically
                                                                             divided
                                                                                 p pup     divided
                                                                                              intodivided up up
                                                                                                        four   into
                                                                                                               steps: fourfour
                                                                                                                     into       steps:
                                                                                                                         classical
                                                                                                                            steps:       classical
                                                                                                                                   pre-processing,
                                                                                                                                    classical       pre-processing,
                                                                                                                                                pre-processing,
 mn, isquantifying    Quantum
          schematically           Algorithm
                                  divided     Implementations
                                               up e  into    2four
                                                                          Beginners                                                                                 65
   tate   preparation,
 preparation,
    As                        quantifying
                               purity,
                      quantifying
          depicted inthe     Fig.     the
                                  ??,e2    =
                                        this  the
                                              Tr(⌃)
                                              simplepurity,
                                                        and
                                                classical
                                            purity,
                                          and         2⇤=
                                                           eTr(⌃)
                                                          (1
                                                         algorithm
                                                             1  =    1steps:
                                                                      state
                                                                      classical
                                                                andTr(⌃)is
                                                                             ⇤ (1 +
                                                              post-processing.
                                                               classical
                                                                      ⇤ (1 2(1     classical
                                                                                  preparation,
                                                                                    post-processing.
                                                                                    1P
                                                                            schematically
                                                                                         1
                                                                            post-processing.
                                                                                         2(1
                                                                                       ))/2      pre-processing,
                                                                                             . 2(1P
                                                                                                 divided   quantifying
                                                                                                           P
                                                                                                        ))/2 ))/2
                                                                                                              . up  .
                                                                                                                     into four the       classicaland
                                                                                                                                steps:purity,      (7)   classical (7) post-proc
                                                                                                                                                                (7)(6)
                                                                                                                                                    pre-processing,
        Classical
  classical                Pre-processing
                  post-processing.
                                                                                       p
   tate
    As    preparation,        quantifying
                                  ??,   this the   purity, e2 =andTr(⌃)
                                                                     classical
                                                                             ⇤ (1
                                                                       Classical   post-processing.
                                                                                         1     2(1
                                                                                            Classical
                                                                                     Pre-processing        P ))/2
                                                                                                                up .
                                                                                                           Pre-processing
                                                                                                            Classical    Pre-processing                            (7) State p
  n  Fig.depicted
 depicted     ??,inthis in ??,
                     Fig.    Fig.
                          State
                          simple    preparation
                                 this
                                    algorithm
                                       simple simple
                                                   is    algorithm
                                                  algorithm
                                                       schematically    is schematically
                                                                  is schematically
                                                                             divided up          divided
                                                                                           divided
                                                                                              into      four
                                                                                                          up into
                                                                                                               steps:into
                                                                                                                      fourfour  steps:
                                                                                                                         classical
                                                                                                                            steps:       classical
                                                                                                                                    classical
                                                                                                                                   pre-processing,  pre-processing,
                                                                                                                                                pre-processing,
   tate   preparation,
 preparation,
  n,  quantifying             quantifying     the  purity,     and   classical
                                                                       Classical   post-processing.
                                                                                     Pre-processing
    As          Stateinthe
          depicted             purity,
                      quantifying
                             Fig. ??,the
                          preparation     and
                                        this            and
                                                classical
                                            purity,
                                                 Classical
                                              simple           classical    post-processing.
                                                              post-processing.
                                                                Pre-processing
                                                                 Classical
                                                         algorithm            Pre-processing
                                                                        is State
                                                                            schematically
                                                                                    preparation
                                                                                                 divided up
                                                                                                State preparation
                                                                                                                     into four steps: classical pre-processing,
                                                                                                                 State preparation                         Classical Pre-proce
   tate   preparation,
    Classical Pre-processing  quantifying     the  purity,     and     Classical
                                                                     classical       Pre-processing
                                                                                   post-processing.                                                                   Quantifyi
              Quantifying the purity  State preparation
                                                 State State  preparation
                                                        preparation
                                                   Classical  Pre-processing
                                                    Quantifying   theQuantifying the
                                                                      purity   Quantifying
                                                                                     purity the purity
                                   Classical Classical
                                             Pre-processing
                                                        Pre-processing                                                                                                                            State preparatio
       Quantifying
       State           the purity
             preparation
                                                       State  preparation
                                                    Quantifying   the purity
                                                   Classical Pre-processing
                                    Quantifying the
             Classical Post-processing         Quantifying
                                                      purity
                                                       State the
                                                  Classical      purity
                                                              preparation
                                                                    Classical Classical
                                                             Post-processing Post-processing
                                                                                        Post-processing                                                                                                 Classical P
                                      State preparation
                                                 State  preparation
                                                    Quantifying   the purity Purity
                        Classical                State                                                  Classical                                                                            Quantifying the p
      Classical the Pre-processing
     Quantifying Post-processing
                     purity                        Classical
                                   Classical Classical
                                                             Post-processing
                                                       State preparation
                                             Post-processing
                                                        Post-processing Calculation
                                              Preparation                                           Post-processing
                                              Quantifying the purity
                              Quantifying the
                                        Quantifying
                                               purity the purity
                                            Classical Post-processing
                        Data                  Quantifying  the purity                                                                                                                     Classical Post-proc
   Classical Post-processing        |0iData vectors
                                            Classical!       vectors
                                                      Post-processing
                                                   |0iData
                                                         ⌃!         |H!
                                                              |0iData
                                                               ⇢ !       vectors
                                                                       i ⌃vector       vector
                                                                            ! ⇢H! |⌃ i! ⇢ ! | i vector
                             Classical Classical
                                       Post-processing
                                                 Post-processing
    Data vectors ! ⌃ ! ⇢ ! | vector |0iData  vectors  !  ⌃  !  ⇢ !   | i
                                            Classical Post-processing SWAP
                                              Data vectors
                                                       Data! ⌃
                                                            vectors
                                                               !prep
                                                                  ⇢!
                                                                          vector
                                                                     ! |⌃ i
                                                                          !⇢vector
                                                                               ! | i vector            1                                                                P {e , e2 }|0iData vecto
                                                               U
 a vectors ! ⌃ ! ⇢ ! | i vector
                            |0iData
                    Algorithm       vectors !on
                                 Algorithm
                               implemented    ⌃ !  ⇢!| i
                                           Algorithm
                                             implemented
                                                IBM’s     vector
                                                     implemented
                                                         on IBM’s
                                                      5-qubit    on
                                                                  5-qubit
                                                                    IBM’scomputer
                                                              computer    5-qubit computer
                                      Algorithm   |0iData   vectors !on
                                                       implemented          ⌃!           | i vector
                                                                                    ⇢ ! 5-qubit
                                                                                IBM’s             computer
 vectors ! ⌃ ! ⇢       !| i
                 Algorithm    Datavector
                              Algorithmvectors
                                 implemented Data! ⌃ vectors
                                                          U
                                                          !prep
                                                implemented
                                                        on IBM’s
                                                             ⇢   !
                                                                 ! |⌃
                                                            Classicaloni!  vector
                                                                       5-qubit
                                                                          IBM’s
                                                                            ⇢      | i
                                                                              !Classical
                                                                                   computer
                                                                                     5-qubit
                                                                         Post-processingvectorcomputer
                                                                                           Post-processing
                                                                                            Classical             P {e1 , e2 }|0iData vectors ! ⌃
                                                                                                      Post-processing
hm implemented               on     IBM’s
                                      Algorithm    5-qubit
                                                       implemented computer
                                                            vectors !on         IBM’s    5-qubit  computer
                          Uprep
                                                  |0iData                   ⌃!      ⇢!| i
                                                            Classical Post-processing
                                                                                             vector               Algorithm implemented
mplemented on IBM’sAlgorithm             5-qubitClassical
                                         Classical        computer
                                                       implemented
                                                     Post-processing       on   IBM’s 5-qubit
                                                                    Post-processing
                                                                     Conclusions       Conclusionscomputer
                                                                                                  Conclusions
                 Algorithm
  ementedClassical
              on IBM’s        Algorithm
                                 implemented
                             5-qubit            implemented
                                            computer    on  Classical
                                                           IBM’s     on  Post-processing
                                                                       5-qubit
                                                                          IBM’s 5-qubit
                                                                                   computercomputer
                          Post-processing
                                      Algorithm implemented                on IBM’s 5-qubit computerAlgorithm implemented on IBM
                                                                     Conclusions
    The           The   advantage
                    of RB it   The
        advantagePost-processing
                               that itadvantage
                                       ofisRB itConclusions
                                                     of
                                                    thatRB
                                              insensitive   Classical
                                                             Conclusions
                                                          itto
                                                             isit that   Post-processing
                                                                  insensitive
                                                                        it is    to
                                                                 state-preparation       andto state-preparation
                                                                                    state-preparation
                                                                               insensitive   measurementand errors
                                                                                                             measurement
                                                                                                                   and
                                                                                                                    (SPAM),  errors
                                                                                                                        measurement (SPAM),
                                                                                                                               and that errors
                                                                                                                                          it  Classical    c
                                                                                                                                                   that itand
                                                                                                                                               (SPAM),
                                                                                                                                               and
                                                                                                                                             can           P
      Classical                          Classical Classical
                                                     Post-processing Conclusions
                                                                    Post-processing
  Classical
 be         Post-processing
               be
     implemented   implemented
                  more
    The advantage of   RB  be   implemented
                         eﬃciently
                            it that   more
                                       iton
                                          is        more
                                               eﬃciently
                                              logical
                                              insensitive   on
                                                        qubits
                                                            to     ogical
                                                           eﬃciently
                                                                  than
                                                            Classical          logical
                                                                           qubits
                                                                          on
                                                                        process
                                                                 state-preparation   than
                                                                                        qubits
                                                                                           process
                                                                                    tomography.
                                                                         Post-processing and   than   process
                                                                                                   tomography.
                                                                                             measurement      tomography.
                                                                                                             errors (SPAM),    and  that  it can
    TheRB
  advantage
  e of          RB
             that The
            protocol
        RBit of   it
                     Conclusions
                     itgoes
                     is RB
                        thatas The
                             protocol
                               it
                        insensitiveis RBtogoes
                                 follows.
                                      insensitive as to
                                            protocol     goes as
                                                      follows.
                                             state-preparation       Conclusions
                                                                    follows.
                                                          state-preparation
                                                                      and    measurement
                                                                                    and measurement
                                                                                              errors (SPAM),
                                                                                                         errors and
                                                                                                                (SPAM),
                                                                                                                      that it
                                                                                                                           and           can Post-proc
                                                                                                                                    Classical
                                                                                                                              canthat it
 be  implemented
        advantagemore
                    of RBeﬃciently
                           it that iton       logical   qubits    than   process    tomography.
    The
 plemented
   more
    The RB  Conclusions
            more
         eﬃciently
            protocolon  logical
                   eﬃciently
                       goes  as  onqubits
                                      logical
                                  follows.
                                          is insensitive
                                                Conclusions
                                             thanqubits
                                                     process
                                                            to
                                                             Conclusions
                                                          than
                                                                 state-preparation
                                                                 tomography.
                                                                   process    tomography.
                                                                     Conclusions
                                                                                         and measurement errors (SPAM), and that it can              Con
 beThe1.Conclusions
      implemented
          Randomly         more
                            1.
                           choose
                     Fig. 39.          ﬃciently
                                Randomlya
                                   Schematic 1. ofitm
                                            set          on
                                                   Randomly
                                                     choose
                                                       diagram   logical
                                                                     a
                                                               elements  set
                                                                          choose
                                                                        for    qubits
                                                                                 of
                                                                               thefrom quantum than
                                                                                              set    of  process
                                                                                           a state-preparation
                                                                                            elementsdenoted       elements
                                                                                                                 from
                                                                                                          algorithm        tomography.
                                                                                                                            G,for   from
                                                                                                                                 denoted
                                                                                                                                       PCA,...,G,inG denoted
                                                                                                                                                      the    special       case }.of, only   two    features.
   RB
 ocol       advantage   goes
                astofollows.
          protocol
         goes                            it
                                 RBfollows.
                             of as           that           is   insensitive          mto     G,          m            G    =   {G and1 ,       G
                                                                                                                                            measurement
                                                                                                                                                    m  }.
                                                                                                                                                       =    {G1    ,G..., =Gm
                                                                                                                                                                       errors {G      ..., Gm
                                                                                                                                                                                 (SPAM),
                                                                                                                                                                                  1             }.
                                                                                                                                                                                                and    that it The can
 ensitive
 be The
   advantage
  e of1. RB RB it
          Randomly
      implemented protocol
                     first
                    of
                   thatRB   ate-preparation
                            step
                           it
                           choose
                           moreit
                               isgoesis
                                    thata as
                                         classical
                                            it
                                    insensitive
                                            set
                                       ﬃcientlyfollows.
                                                isof m   pre-processing:
                                                         to
                                                         on     state-preparation
                                                      insensitive
                                                               elementsand
                                                                 logical     to     measurement
                                                                                   from
                                                                               qubits     transforming
                                                                                    state-preparation
                                                                                              G,
                                                                                               than   and
                                                                                                    denoted
                                                                                                         process      the
                                                                                                                 measurement
                                                                                                                       G    errors
                                                                                                                           and{G
                                                                                                                           tomography.
                                                                                                                            =raw      data
                                                                                                                                         ,    (SPAM),
                                                                                                                                              errors
                                                                                                                                    measurement
                                                                                                                                           ...,into
                                                                                                                                                G      a
                                                                                                                                                       }. covariance
                                                                                                                                                         (SPAM),       and
                                                                                                                                                                errors and      that
                                                                                                                                                                               matrix
                                                                                                                                                                            (SPAM),that it it
                                                                                                                                                                                          Σ,andcan
                                                                                                                                                                                             then
                                                                                                                                                                                               canthat    it canConclusions
                                                                                                                                                                                                     normalizing
    ThePrepare
      2.    advantage  qudit2.
                             of  in
                                 RB   state2.
                                Prepare  it  that  Prepare
                                                qudit
                                                |0i.   it   isin state
                                                                     qudit
                                                                 insensitive  |0i.in tostate |0i.
                                                                                              state-preparation                    and 1            m
                                                                                                                                            measurement                errors    (SPAM),        and thethatunitary
                                                                                                                                                                                                               it can
 ical
veto   toRandomly
       state-preparation
   choose
 Randomly
   more
plemented
    The
 be 1.
           qubits
             state-preparation
            RBa   set
                  more
              ﬃciently
      implemented
                       o
                  choose
                  protocolthan
                          compute
                            m a
                        of choose
                             on
                             ﬃciently
                           more
                                  set
                                 goes process
                                          and
                                        aof
                                 elements
                                    logical
                                         𝜌as =m
                                            set
                                       ﬃciently
                                                Σ/Tr(Σ),
                                                    measurement
                                                    elements
                                                    from
                                                qubits
                                               on
                                               follows.
                                                   of   mand
                                                         on
                                                            tomography.
                                                      logical   G,
                                                                than  measurement
                                                                    then
                                                               elements
                                                                 logical
                                                                        from
                                                                      denoted
                                                                     qubits   purifying
                                                                           process  G,
                                                                                  fromerrors
                                                                                    than
                                                                               qubits
                                                                                         G   The
                                                                                            denoted
                                                                                               than
                                                                                                      to
                                                                                              tomography.
                                                                                               =
                                                                                              G, process
                                                                                                   𝜌{G    advantage
                                                                                                      (SPAM),
                                                                                                    denoted
                                                                                                         1 ,aG
                                                                                                         process
                                                                                                                 errors
                                                                                                               two-qubit
                                                                                                              ..., tomography.
                                                                                                                    =G G {G
                                                                                                                          m= and
                                                                                                                             }. ,
                                                                                                                              1{G (SPAM),
                                                                                                                                    pure
                                                                                                                                   ...,
                                                                                                                           tomography.
                                                                                                                                        that
                                                                                                                                         G  of
                                                                                                                                             mstate
                                                                                                                                                }.RB
                                                                                                                                      1 , .., Gm }.
                                                                                                                                                   it |𝜓can ⟩,it
                                                                                                                                                             andand that thatit
                                                                                                                                                                        finally    itiscan insensitive
                                                                                                                                                                                   determining                       to state-p
      2.  Prepare      qudit      in
                              needed   state to |0i.
                                                   prepare              ⟩. The        second
 ocol
   RB
 its
ubits    goes
          protocol
      3.than    as
             thanprocessgoes
                     follows.
                          process
                            3.   as
                                 tomography.
                                Act   follows.
                                        on   tomography.
                                             3.
                                              the  Actqudit   on G|𝜓
                                                                   the
                                                                   with         †
                                                                              unitary
                                                                           qudit     bewith   The   0,step    †
                                                                                                         advantage
                                                                                                   unitary
                                                                                                implemented
                                                                                                                isforto    prepare†
                                                                                                                                       of
                                                                                                                                      for  two
                                                                                                                                        more RB    copies
                                                                                                                                                with   it   thatof= |𝜓
                                                                                                                                                                   with  ⟩m+1
                                                                                                                                                                       Git  by
                                                                                                                                                                             is implementing
                                                                                                                                                                                 insensitive
                                                                                                                                                                                     11.         = 11.𝑈to       on a
                                                                                                                                                                                                             state-preparati
                                                                                                                                                       }. bulk of the quantum algorithm. This than p
                                                                                                                                                        eﬃciently                  on      logical         qubits
          Act   on   the
                     𝑈  prepqudit      with     unitary              j+1 G          for     j  =Gj+1     Gm,
                                                                                                        ..,          with
                                                                                                                     G    j =G G 0,0 ..,
                                                                                                                                      =     Gj
                                                                                                                                           m,   =    0, ..,G11.
                                                                                                                                                        =    m,              G0==      G                 prep
    The
 Prepare
 udit       RB    protocol       goes     as   follows.
      2. in  state
              qudit|0i.  inchoose
                             state                                                                                       j+1                   m+1            0                           m+1
      1.  Randomly
          Prepare    quantum
                       qudit           |0i.set|0i.
                                        a
                                      computer.
                                 in state          of mThe     elements
                                                                   third †
                                                                                j
                                                                              stepfrom        G, denoted
                                                                                         is purity
                                                                                                              j
                                                                                                           calculation,G = {G     j
                                                                                                                                      1 , ..., G
                                                                                                                                    which       ismthe
      3.
   choose
 Randomly Act a onchoose
                  set
          Measure the
      4. Randomly     the
                        of  qudit
                            m
                     involves a        with
                                 elements
                                  set
                                Measure
                            4.qudit      of
                                          withm unitary
                                                    elements
                                                    from
                                                   Measure
                                             4.a †the
                                                    POVM  qudit G,G     from
                                                                      denoted
                                                                    Q†the
                                                                      with
                                                                     j+1    G
                                                                         on {Q
                                                                                    for
                                                                                    G,
                                                                                  POVM
                                                                              qudit    beG11j
                                                                                             The
                                                                                            denoted
                                                                                            with
                                                                                               =implemented
                                                                                                =   0,
                                                                                                    {G  ..,
                                                                                                      POVMRB
                                                                                                        },1 ,m,
                                                                                                            {Qwhere
                                                                                                              G
                                                                                                              ...,  = with
                                                                                                                      G protocol
                                                                                                                        1{G
                                                                                                                         1m= }.
                                                                                                                            we  G
                                                                                                                                ,
                                                                                                                                {Q ...,
                                                                                                                                   0more
                                                                                                                                       =
                                                                                                                                  typically
                                                                                                                                      }, G  G
                                                                                                                                           11m
                                                                                                                                           where}.
                                                                                                                                               m+1eﬃciently
                                                                                                                                                  goes  =
                                                                                                                                                       we
                                                                                                                                                     take
                                                                                                                                                        },  11.
                                                                                                                                                                as
                                                                                                                                                              typically
                                                                                                                                                             where         ontake
                                                                                                                                                                        follows.
                                                                                                                                                                    =a we        logical
                                                                                                                                                                                       Q0 =take
                                                                                                                                                                               typically
                                                                                                                                                                          |0ih0|.               qubits
                                                                                                                                                                                                |0ih0|.      than
                                                                                                                                                                                                            on|0ih0|.
                                                                                                                                                                                                                         process t
                                 indoing           Hadamard                    an     ancilla,       which          then      isQ used       to  implement                controlled-SWAP            gate         two
                                                                          =      j   0,            Qdenoted
                                                                                                      0=              ,GQ   = 1        0,,         Q0         Q0                                      Q  0 =
 Act1.                     choose       a   set    of          elements           from        G,                    0           {G  0                  }.
ments
 e    2.
    qudit
      3.     from
          Prepare
        onAct
      4.G,
             the
              with
                on
          Measure
                         G,
                       qudit
                   qudit
                      unitary
                     the
                     qubits
                        the
                                denoted
                             with
                            qudit
                                (from
                               qudit
                                      state
                                       unitary
                                     Gj+1
                                       with   G|0i.
                                           different
                                          with  unitary
                                                  j   Gor
                                                       G
                                                    POVM
                                                        m     j==
                                                            j+1   G
                                                                  G
                                                              copies
                                                                    {G
                                                                     0,
                                                                      j   for
                                                                          ..,
                                                                          ofG
                                                                            1  ,
                                                                               m,
                                                                                † j...,
                                                                                     =
                                                                                    forwith
                                                                                       , 11
                                                                                            G
                                                                                            0,
                                                                                            j
                                                                                         and Q
                                                                                                ..,
                                                                                              The
                                                                                               = m G }.
                                                                                                    m,
                                                                                                    0,
                                                                                                  then
                                                                                                      0  =
                                                                                                         RB
                                                                                                         .,with
                                                                                                             m,G
                                                                                                        },another
                                                                                                              where   protocol
                                                                                                                     with
                                                                                                                    m+1 G  0 =
                                                                                                                            we
                                                                                                                              =G  11.
                                                                                                                                    G
                                                                                                                             Hadamard
                                                                                                                                      1m+1
                                                                                                                                      =
                                                                                                                                           ...,
                                                                                                                                   typicallyG
                                                                                                                                                G
                                                                                                                                                =
                                                                                                                                             goes
                                                                                                                                                    m11.
                                                                                                                                                       the Q
                                                                                                                                                  ontakeas
                                                                                                                                                        =   11.follows.
                                                                                                                                                              ancilla.      Finally measuring ⟨𝑍 ⟩ on the
  m
 Prepare
 udit    in  denoted
              qudit
             state       in 5.G
                              tate=
                                Repeat {G    5.,   ...,
                                                   Repeat
                                               steps     G  2-4   }.Qj+1
                                                                   many
                                                                   steps  = |𝜓 {Q⟩),0to
                                                                                j
                                                                               2-4
                                                                                †times
                                                                                                                                   0           m+1                   =the |0ih0|.
      5.  Repeat      steps     2-4    many        times        into     order   2 ). many    into
                                                                                            estimate   order
                                                                                                     times     pGtointo   estimate
                                                                                                                       := order        0to    estimate
                                                                                                                                              the:=  probability            of           the of
                                                                                                                                                                               probability
                                                                                                                                                                               obtaining      probability
                                                                                                                                                                                               outcome                obtaining Q
                                                                                                                                                                                                             Q0of. outcome
                                                                                                                                                                                                      obtaining                   0.
                                                                                                                                                                                                                                out
                      |0i.             |0i.   1                m                                      0                      Pr(Q        ),pG           Pr(Q   pG00 ),:=   Pr(Q0 ),
 herom2.
      3.     G,
          Prepare
       qudit
 Measure
      4.  Act   with
               the
                on
          Measure   denoted
                       qudit
                     ancilla
                     the POVM
                      qudit
                        the     gives
                                with
                            quditin
                              qudit
                                      state
                                         GPOVM
                                       with
                                       Q  the
                                            =
                                          with =|0i.
                                                purity{G
                                                unitary
                                                {Q  POVM
                                                       0 ,Q 11 1
                                                               𝑃= ,
                                                                  G=...,
                                                                    {Q
                                                                    Q
                                                                    Q  Tr(𝜌
                                                                     j+10 },
                                                                          =0GG
                                                                             , where
                                                                               1
                                                                              {Qj1 mforThe
                                                                                       ,}.
                                                                                         Q  j 0we
                                                                                               =last
                                                                                                },     Randomly
                                                                                                      typically
                                                                                                    where
                                                                                                    0, step
                                                                                          11 1.Q0 }, where
                                                                                                        ..,  m,    is
                                                                                                                    we to
                                                                                                                     with   classically
                                                                                                                           take
                                                                                                                           typically
                                                                                                                            we G     Q=  choose
                                                                                                                                  typically
                                                                                                                                   0    0   G
                                                                                                                                            =  compute
                                                                                                                                              take
                                                                                                                                                |0ih0|.
                                                                                                                                               m+1      =
                                                                                                                                                        Q
                                                                                                                                                     take  01a
                                                                                                                                                             1.
                                                                                                                                                              =
                                                                                                                                                              Q the
                                                                                                                                                                  set
                                                                                                                                                                    =  eigenvalues
                                                                                                                                                                   |0ih0|.  of
                                                                                                                                                                          |0ih0|. m       using Eqs. (78)-(79).
                                                                                                                                                                                         elements             from        G,  den
                                                  †times into† order to 1.                             Randomly                     choose            atheset
      5. Repeat
          Repeat stepssteps     2-4    many                                                  estimate                                         thei,            hpGof
                                                                                                                                                     probability               elements
                                                                                                                                                                          theGobtaining
                                                                                                                                                                            of                     from
                                                                                                                                                                                              ofoutcome      G,  0p.denoted
                                                                                     0                                                                           0
 e
 Act3.6.onAct
    qudit     with
             the            6.with
                                Repeat
                                1-5    many  6.steps
                                                   Repeat
                                                  jtimes
                                                            1-5    many
                                                                   steps
                                                                into     order 1-5
                                                                                 times many
                                                                                      to      into
                                                                                            estimate   order
                                                                                                     times      pG  to
                                                                                                                   into:=   order
                                                                                                                          estimate
                                                                                                                        G0the
                                                                                                                             Pr(Q      0to),  estimate
                                                                                                                                    expectation                expectation
                                                                                                                                                           value      i,ofm         value
                                                                                                                                                                                expectation
                                                                                                                                                                                (averaged         over   all of
                                                                                                                                                                                                       (averaged
                                                                                                                                                                                                    value     Q             all G).
                                                                                                                                                                                                                       (averaged
                                                                                                                                                                                                                    G over
                                                                                                                                                                                                                                Gov=
                onqudit
                      unitary          unitary       for                  for          with                with                G),11.                11.
                                     G        Gunitary G      j
                                                            j+1=  Gj0,    ..,  m,
                                                                                † j  =      0,  ..,Gm,   =     hp
                                                                                                               G        i,   ==     G=       hp =                           p                     p           G).
 eps  4.
 Repeat   Measure
        2-4  many
             steps   thethe
                       2-4  qudit
                        times qudit
                             many  intowith
                                        j+1
                                          with
                                         times
                                           order    POVM
                                                     into
                                                        to        G
                                                               estimate
                                                                order
                                                                    Qj+1  =Gtoj
                                                                              {Q  pfor , 11
                                                                                   estimate
                                                                                         := j=     Q
                                                                                                Pr(Q0,0 ..,
                                                                                                      p},
                                                                                                        G0 ),
                                                                                                             m,
                                                                                                              where
                                                                                                             :=
                                                                                                                    G
                                                                                                                     with
                                                                                                                    m+1
                                                                                                                   the
                                                                                                                     Pr(Q   we0   typically
                                                                                                                           probability
                                                                                                                                   0
                                                                                                                                       m+1
                                                                                                                                      the   Gm+1G
                                                                                                                                                        = 11.Q
                                                                                                                                                   oftake
                                                                                                                                                        obtaining
                                                                                                                                               probability       0 =        outcome
                                                                                                                                                                           obtaining
                                                                                                                                                                     of |0ih0|.            outcome
                                                                                                                                                                                           Q0 .
                                                                                                                                                                                                    G
                                                                                                                                                                                                          Q0Q . 0.
      5.  Repeat
      6. Repeat       steps     2-4    many
                      steps 1-5 many times         times        into     order      G0to    estimate  0        p
                                                                into order to estimate hpG i, the expectation value of pG (averaged over all G).
                                                                                                                   G   :=    Pr(Q      0 ),   the    probability            of obtaining       outcome
 he
  r+1j4.
 Repeat
 eps
       qudit
 Measure
      5.G   † the
                with
              for
          Measure
         =Repeat
             0,       qudit
                     are
                .., m,   POVM
                      j1-5=
                        the
                      stepswith with
                            qubits
                                0,
                              qudit
                                2-4
                                       Q𝐴with
                                     ..,
                                      G   POVM
                                            =
                                          0m,
                                       many   ={Q
                                             and    with
                                                    POVM
                                                    Ginto
                                                      𝐴0
                                                   times
                                                         ,Q′1.1 =
                                                               Then,
                                                                  G=
                                                                into
                                                                    {Q
                                                                    Q
                                                                    Q     },
                                                                          1.
                                                                       001=
                                                                               11
                                                                            another
                                                                           0=  where
                                                                             ,{Q
                                                                         order      GG ,Q
                                                                                      to  1i,  2.
                                                                                           1 0the      Prepare
                                                                                                2.Qwhere
                                                                                               we
                                                                                                },     Prepare
                                                                                                      typically
                                                                                                      hp},G11.
                                                                                                 Hadamard
                                                                                            estimate  =       where we is   we  qudit
                                                                                                                              qudit
                                                                                                                           typically
                                                                                                                           take      Q
                                                                                                                              performed
                                                                                                                                  typically
                                                                                                                                        0   =inake in
                                                                                                                                                    state
                                                                                                                                                |0ih0|.
                                                                                                                                              theptake
                                                                                                                                                      on state
                                                                                                                                                        Q0𝐶.  =
                                                                                                                                                              Q
                                                                                                                                                     probability |0i.
                                                                                                                                                                   |0ih0|.
                                                                                                                                                                 Finally,
                                                                                                                                                                 0 =
                                                                                                                                                                          |0i.
                                                                                                                                                                      pG|0ih0|.
                                                                                                                                                                            ofG
                                                                                                                                                                                𝐶 is measured
                                                                                                                                                                               obtaining       outcome
                                                                                                                                                                                                         in the      𝑍
      6.1-5j steps
             many
          Repeat        times
                      steps  many
                                1-5into  times
                                       manyorder
                     basis. One can show that the  timesto
                                                        m+1    estimate
                                                                order
                                                                into        to
                                                                         order     estimate
                                                                                  hp0
                                                                                 finaltom+1 estimate  0
                                                                                            expectation
                                                                                                       expectation
                                                                                                              i,phpGthe:= the
                                                                                                                        i,
                                                                                                                    Gvalue
                                                                                                                             Pr(Qvalue
                                                                                                                            expectation0 ),
                                                                                                                                    expectation
                                                                                                                                   of
                                                                                                                                              of
                                                                                                                                         𝑍 on qubit
                                                                                                                                                         (averaged
                                                                                                                                                     value
                                                                                                                                                     G     valueof
                                                                                                                                                               𝐶 isof
                                                                                                                                                                              over
                                                                                                                                                                            (averaged
                                                                                                                                                                            p
                                                                                                                                                                         precisely
                                                                                                                                                                                      all
                                                                                                                                                                                (averaged    over
                                                                                                                                                                                           G).
                                                                                                                                                                                        the purity
                                                                                                                                                                                                     all all
                                                                                                                                                                                                  over    G).Q
                                                                                                                                                                                                         of 𝜌,G).0
                                                                                                                                                                                                                   i.e.,
   for
 Repeat
 eps    2-4
      6. Repeat
      5.   jQ =
             many
             steps 0,steps
                        ..,
                        times
                       2-4
                }, 11steps
                              m,
                             many     with
                                   into    orderG
                                         times          to0 =
                                                     into       orderGQ
                                                               estimate     to    pGto           11.
                                                                                         =estimate
                                                                                   estimate
                                                                                         :=     Pr(Q  pG0 ), :=    the
                                                                                                                     Pr(Q0 probability
                                                                                                                                 ),   the     theof
                                                                                                                                               probability
                                                                                                                                                        obtaining    of of obtaining
                                                                                                                                                                            outcome        Q0 . †
                                                                                                                                                                                           outcome        Q0 .Q .
                              Q2-4wemany           times        into
                                                                takeorder                   estimate                                                 probability            pGobtaining      Goutcome
                                                                           m+1
Q, 11=    Repeat
          {Q  00     where      1-5       typically
                                       many        times
                                  0 }, where we typically
                                                                into     order   0 =  to |0ih0|.
                                                                                             ⟨𝑍 3.
                                                                                               3. ⟩take
                                                                                                    𝐶 =
                                                                                                       Act
                                                                                                       Act   𝑝Q
                                                                                                               p
                                                                                                               hpGG on
                                                                                                                     on
                                                                                                                  0 −0
                                                                                                                       :=
                                                                                                                          𝑝the
                                                                                                                        i,=  Pr(Q
                                                                                                                            the
                                                                                                                              the
                                                                                                                            1 =
                                                                                                                                     qudit
                                                                                                                                    expectation
                                                                                                                                |0ih0|.
                                                                                                                                   Tr(𝜌
                                                                                                                                       0 ), 2
                                                                                                                                          qudit)   =with
                                                                                                                                                       𝑃 ,with   unitary
                                                                                                                                                           value of             (averaged
                                                                                                                                                                          unitary  G   j+1G      j for  Gj†j =
                                                                                                                                                                                                  over all
                                                                                                                                                                                                j+1             for
                                                                                                                                                                                                              G).0 0, .., m, with
                                                                                                                                                                                                                 (82) j = 0, ..,
 eps
 Repeat
      6.1-5  steps
             many
          Repeat       1-5
                        times
                      steps  many
                                1-5into  times
                                       manyorder     into
                                                   timesto      order
                                                               estimate
                                                                into        to
                                                                         order     estimate
                                                                                  hp  to   i,  the
                                                                                            estimate   expectation
                                                                                                      hp      i,    the     the  value
                                                                                                                            expectation       of
                                                                                                                                    expectation    p value valueof
                                                                                                                                                         (averaged    pof     over
                                                                                                                                                                            (averaged all
                                                                                                                                                                                (averaged    over
                                                                                                                                                                                           G).       all
                                                                                                                                                                                                  over    G).
                                                                                                                                                                                                         all
Q , 11 Q }, where we typically take Q = |0ih0|.
   o0estimate 0p := Pr(Q ), the probability of 0
                                              obtaining outcome Q .
            where 𝑝 0 (𝑝 1 ) 0is the probability for 4.  Measure
                                                              (one) the
                                                                                      G                   G    hp   G   i,                           G                  G   p G                               G).
 o order to estimate
               G
                           pG := Pr(Q0 ), the4.      the zero
                                                       probability
                                                         Measure      of qudit
                                                                    outcome      with POVM
                                                                              on0 𝐶.
                                                                         obtaining      outcome   QQ   =0 {Q
                                                                                                          . =0 , 11   Q0 }, where w
                The fourth step is classical post-processing,   wherethe    qudit with
                                                                      one converts           POVM
                                                                                     𝑃 into the           Q
                                                                                                eigenvalues   of {Q   0 , 11
                                                                                                                  Σ using     Q0 },
 ro to estimate
    estimate  hpG i,pthe
                     G  :=expectation
                               Pr(Q   0 ), the
                                           value probability
                                                 of p5.
                                                      G (averaged
                                                         Repeat  of obtaining
                                                                    over
                                                                  steps   all G).
                                                                         2-4   manyoutcome
                                                                                       times    Q
                                                                                               into0 .order  to    estimate  p G :=
 o order toEqs.   (78) andhp
              estimate       (79).i, the expectation value of p (averaged over all G).
                                G                    5. Repeat steps   G 2-4 many times into order to estimate
 r to estimate
             13.3 hpG    i, the expectation
                     Algorithm      implemented on   value
                                                     6. IBM’sof pG
                                                         Repeat      (averaged
                                                                  steps
                                                               5-qubit   1-5   manyover
                                                                        computer       timesallinto
                                                                                                G).order to estimate hpG i, t
                        The actual gate sequence that we 6.       Repeat
                                                            implemented       steps5-qubit
                                                                           on IBM’s 1-5 many     times
                                                                                           computer is    into
                                                                                                       shown     order
                                                                                                             in Fig.      to estimate
                                                                                                                     40. This
                        involved a total of 16 CNOT gates. The decomposition of controlled-SWAP into one- and two-qubit
                        gates is done first by relating it to the Toffoli gate:
                                                    controlled-SWAP𝐶𝐴𝐵 = ( 1𝐶 ⊗ CNOT𝐵𝐴 )Toffoli𝐶𝐴𝐵 ( 1𝐶 ⊗ CNOT𝐵𝐴 )                                                                                  (83)
                        and then decomposing the Toffoli gate, as in Ref. [110].
                           We note that the limited connectivity of IBM’s computer played a signficant role in determining
                        the algorithm. For example, we needed to implement a CNOT from q[1] to q[2], which required a
                        circuit that reverses the direction of the CNOT from q[2] to q[1]. Also, we needed a CNOT from
                        q[3] to q[1], which required a circuit involving a total of four CNOTs (from q[3] to q[2] and from
                        q[2] to q[1]).
66                                                                                              Abhijith J., et al.




Fig. 40. Actual circuit for quantum PCA implemented on IBM’s 5-qubit simulator and quantum computer.
The first three time slots in the score correspond to the state preparation step of the algorithm, and the
subsequent time slots correspond to the purity calculation step. Due to connectivity reasons, we chose qubit
q[3] as the ancilla and qubits q[1] and q[2] as the targets of the controlled-SWAP operation. We decomposed
the controlled-SWAP operation into CNOT gates by first relating it to the Toffoli gate via Eq. (83), and then
decomposing the Toffoli gate into CNOT gates [110].


   Our results are as follows. For the example given in Eq. (75), IBM’s 5-qubit simulator with 40960
trials gave:

                          𝑒 1 = 1.57492 ,    𝑒 2 = 0.102965    (IBM’s simulator) .                           (84)
A comparison with Eq. (76) shows that IBM’s simulator essentially gave the correct answer. On the
other hand, IBM’s 5-qubit quantum computer with 40960 trials gave:
     𝑒 1 = 0.838943 + 0.45396𝑖 ,     𝑒 2 = 0.838943 − 0.45396𝑖     (IBM’s Quantum Computer) .                (85)
This is a non-sensical result, since the eigenvalues of a covariance matrix must be (non-negative)
real numbers. So, unfortunately IBM’s quantum computer did not give the correct answer for this
problem.

14   QUANTUM SUPPORT VECTOR MACHINE
Support Vector Machines (SVM) are a class of supervised machine learning algorithms for binary
classifications. Consider 𝑀 data points of {(𝑥®𝑗 , 𝑦 𝑗 ) : 𝑗 = 1, 2, . . . , 𝑀 }. Here 𝑥®𝑗 is a 𝑁 -dimensional
vector in data feature space, and 𝑦 𝑗 is the label of the data, which is +1 or −1. SVM finds the
hyperplane 𝑤® · 𝑥® + 𝑏 = 0 that divides the data points into two categories so that 𝑤® · 𝑥®𝑗 + 𝑏 ≥ 1 when
𝑦 𝑗 = +1 and 𝑤® · 𝑥®𝑗 + 𝑏 ≤ −1 when 𝑦 𝑗 = −1, and that is maximally separated from the nearest data
points on each category. Least Squares SVM (LS-SVM) is a version of SVM [122]. It approximates
the hyperplane finding procedure of SVM by solving the following linear equation:
                                               1®𝑇
                                                        
                                         0               𝑏       0
                                                             =       .                                     (86)
                                         ®1 K + 𝛾 −1 1 𝛼®       𝑦®
Here K is called the kernel matrix of dimension 𝑀 × 𝑀, 𝛾 is a tuning parameter, and 𝛼® forms the
                             Í
normal vector 𝑤® where 𝑤® = 𝑀  𝑗=1 𝛼 𝑗 𝑥®𝑗 . Various definitions for the kernel matrix are available, but
the quantum SVM [102] uses linear kernel: 𝐾𝑖 𝑗 = 𝑥®𝑖 · 𝑥®𝑗 . Classically, the complexity of the LS-SVM
is O 𝑀 2 (𝑀 + 𝑁 ) .
   The quantum version of SVM performs the LS-SVM algorithm using quantum computers [102].
It calculates the kernel matrix using the quantum algorithm for inner product [84] on quantum
random access memory [60], solves the linear equation using a quantum algorithm for solving
linear equations [60], and performs the classification of a query data using the trained qubits
                                                                                                   with
a quantum algorithm [102]. The overall complexity of the quantum SVM is O log 𝑁 𝑀 .
   The algorithm is summarized below:
Quantum Algorithm Implementations for Beginners                                                        67


Algorithm 13 Quantum SVM [102]
  Input:
       • Training data set {(𝑥®𝑗 , 𝑦 𝑗 ) : 𝑗 = 1, 2, . . . , 𝑀 }.
       • A query data ®𝑥.
  Output:
       • Classification of ®
                           𝑥: +1 or −1.
  Procedure:
       Step 1. Calculate kernel matrix 𝐾𝑖 𝑗 = 𝑥®𝑖 · 𝑥®𝑗 using quantum inner product algorithm [84].
       Step 2. Solve linear equation Eq. (86) and find |𝑏, ®      𝛼⟩ using a quantum algorithm for solving
  linear equations [60] (training step).
       Step 3. Perform classification of the query data 𝑥® against the training results |𝑏, ®  𝛼⟩ using a
  quantum algorithm [102].


  The inner product calculation to compute the kernel matrix cannot be done reliably in the
currently available quantum processors. The other important part of the algorithm, which is linear
system solving, can be quantized and has been dealt with in Section IV.

15     QUANTUM SIMULATION OF THE SCHRÖDINGER EQUATION
15.1    Problem definition and background
The Schrödinger’s equation describes the evolution of a wave function 𝜓 (𝑥, 𝑡) for a given Hamil-
tonian 𝐻ˆ of a quantum system:
                                                  "              #
                           𝜕          ˆ             ℏ2𝑘ˆ 2
                        𝑖ℏ 𝜓 (𝑥, 𝑡) = 𝐻𝜓 (𝑥, 𝑡) =          +𝑉 (ˆ
                                                               𝑥) 𝜓 (𝑥, 𝑡),                  (87)
                          𝜕𝑡                         2𝑚
where the second equality illustrates the Hamiltonian of a particle of mass 𝑚 in a potential 𝑉 (𝑥).
Simulating this equation starting with a known wave function 𝜓 (𝑥, 0) provides knowledge about the
wave function at a given time 𝑡 𝑓 and allows determination of observation outcomes. For example,
           2
𝜓 (𝑥, 𝑡 𝑓 ) is the probability of finding a quantum particle at a position 𝑥 at time 𝑡 𝑓 .
   Solving the Schrödinger’s equation numerically is a common approach since analytical solutions
are only known for a handful of systems. On a classical computer, the numerical algorithm starts
by defining a wave function on a discrete grid 𝜓 (𝑥𝑖 , 0) with a large number of points 𝑖 ∈ [1, 𝑁 ].
The form of the Hamiltonian, Eq. (87), allows one to split the system’s evolution on a single time
step Δ𝑡 in two steps, which are easy to perform:
                           𝜓 (𝑥𝑖 , 𝑡𝑛+1 ) = 𝑒 −𝑖𝑉 (𝑥𝑖 )Δ𝑡 QFT†𝑒 −𝑖𝑘 Δ𝑡 QFT 𝜓 (𝑥𝑖 , 𝑡𝑛 ),
                                                                   2
                                                                                                     (88)
where we have assumed that ℏ = 1 and 𝑚 = 12 . And QFT and QFT† are the quantum Fourier transform
and its inverse. The quantum state evolution thus consists of alternating application of the phase
shift operators in the coordinate and momentum representations. These two representation are
linked together by the Fourier Transformation as in the following example of a free space evolution
of a quantum particle:
                                                            2
                                 𝜓 (𝑥𝑖 , 𝑡 𝑓 ) = QFT† 𝑒 −𝑖𝑘 𝑡 𝑓 QFT 𝜓 (𝑥𝑖 , 0),                      (89)
where 𝑉 (𝑥) = 0 for a free particle.
   We now discuss the quantum simulation of the Schrödinger’s equation similar to the one discussed
in [14], [118] that provides the wave function of the system at a given time 𝑡 𝑓 . Finding a proper
measurement on a quantum simulator that reveals information about the quantum system will
68                                                                                       Abhijith J., et al.

                                                 2
however be left out of the discussion. 𝜓 (𝑥, 𝑡 𝑓 ) will be the only information we will be interested
in finding out.

15.2     Algorithm description
A quantum algorithm that performs a quantum simulation of one dimensional quantum systems
was presented in [14]. The procedure is outlined in Algorithm 14.


Algorithm 14 Quantum simulation of Schrödinger equation [118], [14]
     Input:
          • Initial wave function
          • Time step size, Δ𝑡, and the number of time steps, 𝑇 .
          • The ability to apply phase shifts in the computational basis.
          • The potential function 𝑉 .
     Output:
          • Final wave function at time 𝑡 𝑓 = 𝑇 𝛿𝑡 when evolved using the Schrödinger equation with
     the potential 𝑉 .
     Procedure:
          Step 1. Encode the wave function on a N-point grid in a quantum state of 𝑛 = log2 (𝑁 )
     qubits. The value of this discretized wavefunction on a grid point is equal to the value of the
     original wave function at the same point. The constant of proportionality must then be calculated
     by renormalizing the discretized wavefunction.
          for 1 ≤ 𝑗 ≤ 𝑇 do
                  Step 2a. Apply the Quantum Fourier Transform (QFT) to go to the momentum
             representation.
                  Step 2b. Apply a diagonal phase shift of the form |𝑥⟩ → 𝑒 −𝑖𝑥 Δ𝑡 |𝑥⟩ in the computa-
                                                                                 2


             tional basis.
                  Step 2c. Apply the inverse Quantum Fourier Transform to come back to the position
             representation.
                  Step 2d. Apply a phase shift of the form |𝑥⟩ → 𝑒 −𝑖𝑉 (𝑥)Δ𝑡 |𝑥⟩ .
          end for
          Step 3. Measure the state in the computational basis.


   Figure 41 shows the following stages of the algorithm. The implementation of QFT was discussed
in Section IV. Implementing phase shifts corresponding to arbitrary functions can be done using a
series of controlled 𝑍 gates or CNOT gates [14]. Repeating the final measurement step over many
independent runs will let us estimate the probabilities |𝜓 (𝑥, 𝑡 𝑓 )| 2 . We will now consider a 2-qubit
example of the quantum simulation algorithm in the case of a free particle, 𝑉 (𝑥) = 0.
   Our initial wave function is a Π-function (a rectangular wave), which has {0, 1, 1, 0} representation
on a 2𝑛 -point grid for 𝑛 = 2 qubits. Its representation by the state of the qubits is proportional to
|0, 1⟩ + |1, 0⟩, which can be prepared by constructing the Bell state (see Fig. 1) and applying the 𝑋
gate to the first qubit.                                       
   We define the 2-qubit QFT as 𝑄𝐹𝑇 = SWAP12 𝐻 2 𝐶 2 P1 𝜋2 𝐻 1 , where 𝐶 2 P is a phase operator
controlled from the second qubit. This transformation applies phase shifts to the probability
amplitudes of the qubit states similar to the ones applied by the classical FFT to the function values.
Hence, the resulting momentum representation is identical to the classical one in a sense that it is
not centered around 𝑘 = 0, which can be easily remedied by a single 𝑋 1 gate.
Quantum Algorithm Implementations for Beginners                                                                                              69


         Classical                        State                           ΔH step                                   Final
      Pre-processing                   Preparation                    (HI /ΔH times)                                State

         ! |%& (()⟩
         ",
        (+ , , ∈ [0, 0]



                                                                                                                       %< HI = = J+ 3+
                                         0?                    0?

        %+ = %((+ )

                                                                                                RQ ΔH U (
                                         0;                    0;


                                                                             RQ ΔH S ;
                                               !BCDB
                                               A                       M                  M
                                                                                         TNOP
      3 {5} , 7 = log ; 0                0E                    0E
                                                                       NOP                                       +>?                     @

            @                            0F                    0F
      %< = = %+ 3+        5              0G                    0G                                                      5
           +>?
            !BCDB
            A


Fig. 41. The quantum simulation of the Schrödinger’s equation. The first stage is a classical pre-processing
that encodes the wave function to available qubits and derives a state preparation operator that takes
an all-zero state of a quantum computer to a desired state. The second stage prepares an initial state by
implementing the state preparation operator 𝑈ˆprep on a quantum computer. The third stage is an iterative
update looped over Δ𝑡 steps based on the operator splitting method.


|0⟩                                                                          𝑃 (2𝜙)

|0⟩    𝐻     𝑋    • 𝑋         𝐻   𝑃 ( 𝜋2 )    𝑃 (𝜙)                    •                    •                   𝑃 ( 𝜋2 )                 𝐻
|0⟩                                  •         𝐻       𝑋   𝑃 (2𝜙) •                              • 𝑋        𝐻      •

Fig. 42. The quantum circuit implementation of a 2-qubit algorithm that solves the Schrödinger’s equation
on a quantum computer. The initial state preparation is followed by the Quantum Fourier Transform and
centering of the momentum representation. The single qubit phase shift transformations are followed by
the two-qubit phase shift transformation that uses an ancillary qubit q[0]. The inverse Quantum Fourier
Transform preceded by removing the centering operation completes the circuit and returns the wave function
to the coordinate representation.

                                                                    √︃
   The momentum encoding adopted in this discussion is 𝑘 = − 21 Δ𝑡 1 + 𝑛𝑘=1 2𝑛−𝑘 𝑍𝑘 , where 𝜙
                                                                       𝜙    Í            

is a characteristic phase shift experienced by the state on a time step Δ𝑡. In this representation
−𝑖𝑘 2 Δ𝑡 phase shift contains one and two qubit contributions that commute with each other and can
be individually implemented. The one qubit phase shift gate has a straightforward implementation
but the two qubit phase shift gate requires an ancillary qubit according to Ref. [92], which results
in a three qubit implementation on a quantum computer. This implementation is captured in Fig 42
where removing the centering of the momentum representation and the inverse QFT have been
added in order to return to the coordinate representation.

15.3     Algorithm implemented on IBM’s 5-qubit computer
The implementation in Fig. 43 takes into account the topology of the chip and the availability of
the gates such as 𝑈 1 and 𝑈 2. Finally, it performs a consolidation of the single qubit gates in order
to reduce the number of physical operations on the qubits.
70                                                                                        Abhijith J., et al.




Fig. 43. The quantum circuit implementation of a 2-qubit algorithm that solves the Schrödinger’s equation
on the ibmqx4 quantum computer.


   The circuit in Fig. 43 was run on the ibmqx4 quantum chip, where the maximum number of
executions in a single run is 210 . The probabilities of observing qubit states in the computational
basis was measured for 𝜙 = 0, 𝜙 = 𝜋/2, 𝜙 = 𝜋, 𝜙 = 3𝜋/2 and 𝜙 = 2𝜋. We expect that as 𝜙 increases
from 0 to 𝜋 the wave function evolves from a Π-function to a uniform function to a function
peaked at the ends of the interval. The consecutive increase returns the wave function back to the
Π-function.
   We started with the 𝜙 = 0 case that should have reproduced our initial state with ideal probabilities
of {0, 0.5, 0.5, 0}. However, the observed probabilities were {0.173, 0.393, 0.351, 0.084}. Thus it was
surprising to see that the 𝜙 = 𝜋/2 case was very close to expected probability of 0.25 with the
observed values of {0.295, 0.257, 0.232, 0.216}. This surprise was however short lived as the 𝜙 = 𝜋
case has reverted back large errors for observed probabilities: {0.479, 0.078, 0.107, 0.335}. The final
two case had the following observed probabilities {0.333, 0.248, 0.220, 0.199} and {0.163, 0.419, 0.350,
0.068} respectively.

16     GROUND STATE OF THE TRANSVERSE ISING MODEL
In this section the ground state of the transverse Ising model is calculated using the variational
quantum eigenvalue solver, and the result is compared to the exact results. This is a hybrid method
that uses alternating rounds of classical and quantum computing.
   In the previous section we saw how to simulate the evolution of a single quantum particle. But
often, real world phenomena are dependent on the interactions between many different quantum
systems. The study of many-body Hamiltonians that model physical systems is the central theme
of condensed matter physics (CMP).
   Many-body Hamiltonians are inherently hard to study on classical computers as the dimension
of the Hilbert space grows exponentially with the number of particles in the system. But using a
quantum computer we can study these many-body systems with less overhead as the number of
qubits required only grows polynomialy.

16.1    Variational quantum eigenvalue solver
A central task in CMP is finding the ground state (lowest energy eigenstate) of a given Hamiltonian,
H,
                                            H |Ψ⟩ = 𝐸𝑔 |Ψ⟩.                                            (90)
   Studying the ground state gives us information about the low temperature properties of the
system. Once we know |Ψ⟩, we can deduce the physical properties from the wave function. In
this section, we will describe how to use IBM Q to find the ground state energy of the transverse
Ising model. We will not be using the ibmqx4 in this section. This is because the algorithm we
use will require many rounds of optimization. Each round requires us to run a circuit on the
quantum computer followed by a classical optimization step on a local machine. This process can
Quantum Algorithm Implementations for Beginners                                                        71




Fig. 44. Schematic view of the implementation of the variational quantum eigenvalue solver using a hybrid
classical and quantum circuit. The figure is adopted from Ref. [96].


be automated easily using Qiskit. But the long queuing times in IBM Q makes repeated runs on the
quantum processor impractical.
   To find the eigenvalue of a Hamiltonian, we could use the quantum phase estimation algorithm
that was discussed in Section IV. To do this we need the ability to perform controlled operations
with the unitary 𝑈 = exp(−𝑖H𝛿𝑡/ℏ), where 𝛿𝑡 is the time step. Then, by preparing different initial
states |𝜓𝑖 ⟩ and repeating the phase estimation many times one can obtain, in principle, the whole
spectrum of the eigenvalues and the corresponding eigenwave functions. For a general Hamiltonian,
however, the implementation of a controlled 𝑈 may be not straightforward. For realistic problems,
the quantum phase estimation circuits have large depth. This requires qubits with long coherence
times, which are not available at the time of writing. For CMP problems, we are mainly interested
in the lowest eigenvalue for most cases.
   To overcome these limitations, we use the recently developed variational quantum eigenvalue
solver (VQES) [89, 96]. The basic idea is to take the advantages of both quantum and classical
computers, as shown in Fig. 44. It allocates the classically easy tasks to classical computers and the
other tasks to quantum computers. The algorithm is summarized as follows:
  (1) Prepare a variational state |𝜓 (𝜃 𝑖 )⟩ with parameters 𝜃 𝑖 . For an efficient algorithm, the number
      of variational parameters should grow linearly with the system size.
  (2) Calculate the expectation value of the Hamiltonian using a quantum computer, 𝐸 = ⟨𝜓 |H |𝜓 ⟩/⟨𝜓 |𝜓 ⟩.
  (3) Use classical nonlinear optimizer algorithms to find new optimal 𝜃 𝑖 . In this report, we will
      use the relaxation method 𝜏0 𝜕𝑡 𝜃 𝑖 = −𝜕𝐸/𝜕𝜃 𝑖 , where 𝜏0 is a parameter to control the relaxation
      rate.
  (4) Iterate this procedure until convergence.
   VQES has the following advantage: For most CMP problems, where the interaction is local, we
can split the Hamiltonian into a summation over many terms. This means that we can parallelize
the algorithm to speed up the computation. The quantum expectation calculations for one term
in the Hamiltonian are relatively simple, thus no long coherence times are not required. On the
72                                                                                          Abhijith J., et al.




                       Ferromagnetic phase                  Paramagentic phase
                                                                                    ℎ
                                                    𝑔# Quantum phase transition


Fig. 45. Schematic view of the quantum phases described by the transverse Ising model. The arrows represent
the spin configuration in the ordered and disordered phases.


other hand, VQES also has limitations. Because of its variational nature, the trial wave function
needs to be prepared carefully. This usually requires physical insights into the problem. The ground
state eigenvalue and eigenwave function are biased by the choice of the trial wave functions. In
addition, VQES requires communications between classical and quantum computers, which could
be a bottleneck for the performance.

16.2   Simulation and results
We use VQES to find the ground state of the transverse Ising model (TIM) defined by
                                         ∑︁              ∑︁
                                 H =−        𝜎𝑖𝑧 𝜎𝑖+1
                                                  𝑧
                                                      −ℎ    𝜎𝑖𝑥 ,                                        (91)
                                                𝑖                 𝑖
where 𝜎 𝑧 , 𝜎 𝑥 are Pauli matrices and ℎ is the external magnetic field. Let us first review briefly the
physical properties of this Hamiltonian. This Hamiltonian is invariant under the global rotation of
spin along the 𝑥 axis by 𝜋, 𝑅𝑥 H𝑅𝑥† = H , where 𝑅𝑥 (𝜋) is the rotation operator
                                    𝑅𝑥 𝜎 𝑥 𝑅𝑥† = 𝜎 𝑥 , 𝑅𝑥 𝜎 𝑧 𝑅𝑥† = −𝜎 𝑧 .                               (92)
The TIM has two phases: When the transverse field ℎ is small, the spins are ordered ferromagnetically
and the rotational symmetry associated with 𝑅𝑥 is broken. In the ordered phase, the quantum
expectation value ⟨𝜎 𝑧 ⟩ ≠ 0. As ℎ is increased, there is a quantum phase transition from the ordered
phase to the disordered phase where ⟨𝜎 𝑧 ⟩ = 0, as the rotational symmetry is restored. The phase
diagram is shown schematically in Fig. 45.
  Using the phase diagram as a guide, first we propose a product state as a trial wave function.
The wave function can be written as
                                                      Ö
                                        |𝜓𝑖 (𝜃 𝑖 )⟩ =   𝑈 (𝜃 𝑖 )|0𝑖 ⟩.                           (93)
                                                        𝑖
Here 𝑈 (𝜃 𝑖 ) is the unitary operation which describes the spin rotation along the 𝑦 axis by an angle
𝜃𝑖 ,                                                                   
                                              cos(𝜃 𝑖 /2) − sin(𝜃 𝑖 /2)
                                 𝑈 (𝜃 𝑖 ) =                               ,
                                              sin(𝜃 𝑖 /2) cos(𝜃 𝑖 /2)
where 𝜃 𝑖 are the variational parameters. Here we have used the Bloch sphere representation for a
qubit state. For the TIM, we calculate the expectation value of
                              𝐸 𝐽 ,𝑖 = −⟨𝜓 |𝜎𝑖𝑧 𝜎𝑖+1
                                                 𝑧
                                                     |𝜓 ⟩, 𝐸𝑍,𝑖 = −⟨𝜓 |𝜎𝑖𝑥 |𝜓 ⟩.                         (94)
  The quantum circuit to perform the preparation of the state and calculation of the expectations
value are shown in Fig. 46(a) andFig. 46(b) . We have
                     𝐸 𝐽 ,𝑖 = −[𝑃 (𝑞𝑖 = 0) − 𝑃 (𝑞𝑖 = 1)] [𝑃 (𝑞𝑖+1 = 0) − 𝑃 (𝑞𝑖+1 = 1)],                  (95)

                                    𝐸𝑍,𝑖 = −[𝑃 (𝑞𝑖 = 0) − 𝑃 (𝑞𝑖 = 1)],                                   (96)
Quantum Algorithm Implementations for Beginners                                                                   73




                                      (a)                                     (b)




                                                         (c)

Fig. 46. Quantum circuits to prepare the trial wave-functions. The single qubit unitaries in the text can be
implemented using available gates in IBM Q. The first two circuits prepare unentangled trial states. Circuit (a)
can be used to measure ⟨𝜓 | 𝜎2𝑧 𝜎3𝑧 |𝜓 ⟩ . Circuit (b) can be used to measure the ⟨𝜓 | 𝜎3𝑥 |𝜓 ⟩. Circuit (c) prepares
the entangled trial state.


where 𝑃 (𝑞𝑖 = 0, 1) is the measured probability for the qubit 𝑞𝑖 in the |0⟩ or |1⟩ state. As we mentioned
before, the communication bottleneck prevented us from implementing this on ibmqx4. We ran the
code using the quantum simulator in Qiskit. The comparison of the results obtained from quantum
simulation and analytical results are shown in Fig. 47. Our trial wave function works very well
in the ordered phase, but the simulation results deviate from the exact solution in the quantum
phase transition region. This discrepancy is caused by the fact that we have neglected the quantum
entanglement in our trial wave function.
   In a second set of experiments, we use a trial wave function that includes quantum entanglement.
Because of the symmetry, |Ψ𝑖 (𝜃 𝑖 )⟩ and 𝑅𝑥 (𝜋)|Ψ𝑖 (𝜃 𝑖 )⟩ are two degenerate wave functions with
the same energy. The trial wave function can be written as a linear superposition of these two
degenerate wave functions
                                   |𝜓𝑖 (𝜃 𝑖 )⟩ = 𝛼 |Ψ𝑖 (𝜃 𝑖 )⟩ + 𝛽𝑅𝑥 (𝜋)|Ψ𝑖 (𝜃 𝑖 )⟩.                            (97)
The first step is to prepare |𝜓𝑖 (𝜃 𝑖 )⟩ using quantum circuit. To prepare an arbitrary state in a quantum
circuit is not trivial as it requires of the order of 2𝑛 CNOT gates, where 𝑛 is the number of qubits [98].
The state in Eq. (97) can be prepared easily using the circuit in Fig. 46(c). Here we consider 4 spins.
The first 𝑈 0 (𝜃, 𝜙) operation transforms the state into
                              |0000⟩ → 𝑒 𝑖𝜙 sin(𝜃 /2)|1000⟩ + cos(𝜃 /2)|0000⟩.
The first CNOT transforms the state into
                                    𝑒 𝑖𝜙 sin(𝜃 /2)|1100⟩ + cos(𝜃 /2)|0000⟩.
The second CNOT transforms the state into
                                    𝑒 𝑖𝜙 sin(𝜃 /2)|1110⟩ + cos(𝜃 /2)|0000⟩.
74                                                                                                    Abhijith J., et al.


              -���
        (a)
              -���


              -���
        𝐸/𝑁
                                                                                      ���������� �� ��������� ����

          �                                                                           ���������� �� ����

                                                                                          �����
              -���


              -���
                         ���   ���      ���      ���       ���      ���        ���
                                                  �
                   ���
        (b)
                   ���


                   ���
                                                                                     ���������� �� ��������� ����
              ��                                                                     ���������� �� ����
                   ���                                                                  �����

                                                                                        ���� ����

                   ���


                   ���
                         ���   ���     ���       ���      ���       ���        ���
                                                  �

Fig. 47. Comparison of the ground state energy (a) and average magnetization (b) 𝑀𝑥 = ⟨𝜓 | 𝑖 𝜎𝑖𝑥 |𝜓 ⟩/𝑁
                                                                                                Í
obtained by using the trial wave functions in Eq. (93) and the exact results. Here we have used the periodic
boundary condition. The simulations are run both on the quantum simulator (black symbols) and classical
computers (red symbols). The mean-field results (blue line) are also displayed for comparison.


The third CNOT transforms the state into
                                     𝑒 𝑖𝜙 sin(𝜃 /2)|1111⟩ + cos(𝜃 /2)|0000⟩.
Finally we apply 𝑈 (𝜃 𝑖 ) rotation and we obtain the desired state in Eq. (97). Here
                                                                             
                                               cos(𝜃 𝑖 /2)    − sin(𝜃 𝑖 /2)
                             𝑈 0 (𝜃, 𝜙) =                                       .
                                            𝑒 𝑖𝜙 sin(𝜃 𝑖 /2) 𝑒 𝑖𝜙 cos(𝜃 𝑖 /2)
  We then use VQES to find the ground state energy. As can be seen in Fig. 48, the new trial
function nearly reproduces the exact results in the whole magnetic field region and improves upon
the product state trial function.

17     QUANTUM PARTITION FUNCTION
17.1    Background on the partition function
Calculation or approximation of the partition function is a sub-step of inference problems in Markov
networks [78]. Even for small networks, this calculation becomes intractable. Therefore an efficient
Quantum Algorithm Implementations for Beginners                                                         75


                                          ���� �����          ����� ���� ������������

                                          ������� ������� ������������

                       ���
                                                       N=4
                      -���
                      -���

                �/�   -���
                      -���
                      -���
                      -���
                          ���       ���         ���               ���             ���   ���   ���
                                                                   �

Fig. 48. (color online) Comparison of the ground state energy obtained by using the trial wave functions in
Eqs. (93) and (97) and the exact result. Here we have used the periodic boundary condition. The number of
spins is 4.


quantum algorithm for the partition function would make many problems in graphical model
inference and learning tractable and scalable; the same holds for other problems in computational
physics [8, 55, 57, 58].
   The partition function is of particular interest for calculating probabilities from graphical models
such as Markov random fields [78]. For this article, we consider the graphical model form known as
the Potts model. Let Γ = (𝐸, 𝑉 ) be a weighted graph with edge set 𝐸 and vertex set 𝑉 and 𝑛 = |𝑉 |.
In the 𝑞-state Potts model, each vertex can be in any of 𝑞 discrete states. The Potts model is a
generalization of the classical Ising model. In the classical Ising model 𝑞 = 2, whereas in the Potts
model 𝑞 ≥ 2. The edge connecting vertices 𝑖 and 𝑗 has a weight 𝐽𝑖 𝑗 which is also known as the
interaction strength between corresponding states. The Potts model Hamiltonian for a particular
state configuration 𝜎 = (𝜎1, . . . , 𝜎𝑛 ) is
                                                       ∑︁
                                             𝐻 (𝜎) = −    𝐽𝑖 𝑗 𝛿𝜎𝑖 ,𝜎 𝑗 ,                          (98)
                                                          𝑖∼𝑗

where 𝑖 ∼ 𝑗 indicates that there exists an edge between vertices 𝑖 and 𝑗; and where 𝛿𝜎𝑖 ,𝜎 𝑗 = 1 if
𝜎𝑖 = 𝜎 𝑗 and 0 otherwise.
   The probability of any particular configuration being realized in the Potts model at a given
temperature, 𝑇 , is given by the Gibbs distribution:
                                                          1 −𝛽𝐻 (𝜎)
                                            𝑃 (𝜎) =         𝑒       ,                                 (99)
                                                          𝑍
where 𝛽 = 1/(𝑘𝐵𝑇 ) is the inverse temperature in energy units and 𝑘𝐵 is the Boltzmann constant.
The normalization factor, 𝑍 , is also known as the partition function:
                                              ∑︁
                                          𝑍=      𝑒 −𝛽𝐻 (𝜎) ,                            (100)
                                                       {𝜎 }
                                                                            FIG. 1:

76                                                                          FIG. 1:                   Abhijith J., et al.

       This algorithm was discussed in Ref. XXX Need citation XX. It is then straightforward to calculate th
       of ⌃ from P , as follows:                          −𝐻citation
                                                    abcNeed   (𝜎)
       This algorithm was discussed in Ref. XXX                        pXX. It is then straightforward to calculate th
       of ⌃ from P , as follows: a      b        e  000
                                                      =   𝐽
                                                        Tr(⌃)
                                                           𝑎𝑏 +⇤ 𝐽(1
                                                                  𝑏𝑐 +
                                                                     + 𝐽𝑎𝑐1   2(1 P ))/2
                                                   1
                                                    001 𝐽𝑎𝑏            p
                                                                       p
                                                 ee2010
                                                      = Tr(⌃)  ⇤ (1       1
                                                                          1 2(1
                                                                              2(1 P  P ))/2
                                                                                       ))/2 .
                                    c              1 =     𝑎𝑐 ⇤ (1 +
                                                        Tr(⌃)
                                                          𝐽
                                                                       p
          As depicted in Fig. ??, this simple e     011 𝐽𝑏𝑐is ⇤ (1
                                               algorithm
                                                   2 = Tr(⌃)   schematically
                                                                          1 2(1divided   up .into four steps: classical p
                                                                                     P ))/2
                              (a)     Graph         100
       state preparation, quantifying the purity, and 𝐽𝑏𝑐classical post-processing.
                              withthisthree
          As depicted in Fig. ??,       simple algorithm𝐽𝑎𝑐is schematically divided up into four steps: classical p
                                                    101
                              vertices the
       state preparation, quantifying   andpurity,110and 𝐽
                                                         classical
                                                           𝑎𝑏        post-processing.
                              three edges.                Classical
                                                    111 𝐽 +      𝐽 +𝐽 Pre-processing
                                                                   𝑎𝑏     𝑏𝑐      𝑎𝑐
                                                                    (b)
                                                                  Classical Pre-processing
                                                                        State preparation

Fig. 49. (a) Simple example with (b) the enumeration of state State
                                                             configurations and the value of the Hamiltonian
                                                                     preparation
                                                             Quantifying the purity
for a fully-connected 3-vertex Ising model (𝑞 = 2 Potts model)
                                                                   Quantifying
                                                                  Classical     the purity
                                                                            Post-processing
             Classical       Irreducible cyclic             State preparation and             Classical
           preprocessing      code via Shor’s             quantumClassical   Post-processing
                                                                   Fourier transform       post-processing
                                [n,k] code
                                                               vectors ! ⌃ ! ⇢ ! | i vector
                                                            Uprep
                                                       |0iData                                { }
                                Shor’s alg                          QFT
               Gauss                                           vectors ! ⌃ ! ⇢ ! | i vector
                                                            Uprep
                                                       |0iData
            elimination
                                                                        {Aicomputer
                                  { } Algorithm implemented on IBM’s 5-qubit }
             [n,k] code
                                             Algorithm implemented    on IBM’s 5-qubit computer
                                                           Classical Post-processing
                                  Quit, if
                                 not ICCC                      Repeat for each
                                                                  Classical Post-processing
                                                                                                Z
                                                                       Conclusions
                    Fig. 50. Overview of the quantum partition function algorithm.
                                                                    Conclusions
         The advantage of RB it that it is insensitive to state-preparation and measurement errors (SPAM), a
      be implemented more eﬃciently on logical qubits than process tomography.
         The advantage    of RB itasthat    it is insensitive to state-preparation and measurement     errors (SPAM), a
       {𝜎The
where be     RB protocol
          } means        fullgoes
                   the more
         implemented          set  of follows.
                               eﬃcientlyall possible
                                              on logicalstate configurations.
                                                          qubits than process There  are 𝑞𝑛 possible state
                                                                              tomography.
configurations,
             RBand
         1. Randomly
         The         so this
                        choose
                 protocol     is aaasset
                             goes  sum   ofover
                                             m a
                                       follows.     large from
                                                 elements number G,ofdenoted
                                                                      items G
                                                                            and=is{G1 ,
                                                                                   generally   intractable as
                                                                                        ..., Gm }.
well as difficult to approximate. The calculation of the partition function is #P-hard (i.e., it is a
counting 2.
          1. Prepare
             Randomly
          problem     qudit
                    which  isinat least
                         choose  state
                                   a set|0i.
                                         ofhard
                                        as   m elements  from G,class
                                                 as the NP-hard   denoted    G = {G1
                                                                         of decision   , ..., Gm }. There is no
                                                                                     problems).
known fully   polynomial
          2. Act
          3. Prepare  qudit
                  on the   randomized
                             in state
                         qudit    with |0i. approximation
                                        unitary  Gj+1 G†j forscheme   (fpras), and
                                                                         m, with  G0it=is G
                                                                                          unlikely   that there
                                                              j = 0, ..,                    m+1 = 11.
exists one [58].
          4. Measure
          3. Act      thequdit
                 on the   quditwith
                                withunitary
                                     POVMGQ   =G†j
                                            j+1 {Q0for, 11j =Q0,0 },  where
                                                                  .., m, withweG0 =
                                                                                typically
                                                                                    Gm+1take
                                                                                          = 11.Q0 = |0ih0|.
17.2   A simple example
          5.
          4. Repeat
             Measuresteps
                     the 2-4
                          quditmany
                                with times
                                      POVM into
                                              Q=order to11 Q
                                                  {Q0 ,   estimate  where
                                                               0 }, p G := we       the take
                                                                              typically
                                                                           Pr(Q0 ),     probability
                                                                                             Q0 = of   obtaining ou
                                                                                                   |0ih0|.
We give a small example with a graph of 𝑛 = 3, 𝑉 = {𝑎, 𝑏, 𝑐}, with edges between all pairs of vertices
for three 6.
          5. Repeat
          total edges,steps 1-5 many
                            2-4 in
                        pictured      times49a,
                                   Figure    into order
                                                and we to  estimate
                                                        use 𝑞 = 2 forphpGG i,
                                                                          :=
                                                                        binarythe
                                                                               Pr(Qexpectation
                                                                                     0 ),
                                                                                 states   theeach
                                                                                          on     value of p
                                                                                              probability
                                                                                                  vertex. of
                                                                                                          ToGobtaining  o
                                                                                                              (averagedou
demonstrate the calculation of the partition function, we first enumerate the configurations as
          6. Repeat steps 1-5 many times into order to estimate hpG i, the expectation value of pG (averaged o
shown in Fig. 49b.
   We plug the value of the Hamiltonian for each of the 𝑞𝑛 configurations into the partition function
given in Eq. (100) to get the normalization constant:

                              𝑍 = 2𝑒 𝛽 (𝐽𝑎𝑏 +𝐽𝑏𝑐 +𝐽𝑎𝑐 ) + 2𝑒 𝛽 𝐽𝑎𝑏 + 2𝑒 𝛽 𝐽𝑏𝑐 + 2𝑒 𝛽 𝐽𝑎𝑐 .                       (101)

Letting 𝐽𝑖 𝑗 = 1 for all 𝑖 ∼ 𝑗, gives:
                                                  𝑍 = 2𝑒 3𝛽 + 6𝑒 𝛽 .                                             (102)
Quantum Algorithm Implementations for Beginners                                                         77




       Fig. 51. Circuit for preparing the first two qubits and quantum Fourier transform on 2 qubits.



17.3   Calculating the quantum partition function
An efficient quantum algorithm for the partition function is given by [58] for Potts models whose
graph, Γ, has a topology such that it can be represented with an irreducible cyclic cocycle code
(ICCC). This stipulation is non-intuitive and it takes a quantum algorithm to efficiently determine if
a given graph meets this requirement. From the graph, Γ, calculate a cyclic code 𝐶 (Γ) that represents
the generating structure of the graph by using Gaussian elimination on the incidence matrix of the
graph, and then use Shor’s algorithm to determine the irreducible set of code words 𝜒. If the code is
not irreducible, then we will not be able to efficiently calculate the partition function for this graph.
   Assuming that the given graph is ICCC, √︁     the first step in the partition function algorithm is
to calculate the Gauss sum of 𝐺 F𝑞𝑘 = 𝑞𝑘 𝑒 𝑖𝛾 , where 𝛾 is a function of 𝜒. The difficult part is to
calculate 𝛾, which can be done efficiently using the quantum Fourier transform (QFT). Using the
set of values, {𝛾 } for all of the words, {𝜒 } in the code; we calculate the weight spectrum {𝐴𝑖 } of
the code representing Γ. From this weights spectrum, the partition function 𝑍 can be efficiently
calculated using classical computing.

17.4   Implementation of a quantum algorithm on the IBM Quantum Experience
We implemented one step of the full partition function algorithm using the IBM Quantum Experience.
The implemented algorithm is the 2-qubit quantum Fourier transform (QFT2), as the first step
in actual calculation of the partition function. The input to this step is the irreducible cocyclic
code. The irreducible cyclic code for the example problem of a 3-vertex Ising model is [1, −1] with
𝑛 = |𝑉 | = 3 and 𝑘 = |𝐸| −𝑐 (Γ) = 2, where 𝑐 (Γ) is the number of connected components in the graph
Γ. This small example does meet the ICCC requirement (as checked through classical calculation), so
we will continue with the calculation of the partition function of the example without implementing
the quantum algorithm for checking this requirement. In the fully-connected 3-vertex Ising model
example given, the input to QFT2 is 𝑞[0] = |+⟩ = |0⟩+|1⟩ √   and 𝑞 [1] = |−⟩ = |0⟩−
                                                                                 √
                                                                                    |1⟩
                                                                                        . In the sample
                                                           2                       2
score shown in Fig. 51, these qubits are prepared before the barrier. The QFT2 algorithm, as given
by the Qiskit Tutorial provided by IBM[4], is the rest of the code. The output bits should be read in
reverse order. Some gates could be added at the end of the QFT2 algorithm to read the gates in the
same order as the input.
   The result from simulating 1000 shots gives 𝑃 (𝛾 = 1) = 0.47 and 𝑃 (𝛾 = 3) = 0.53. The results
from running on the actual hardware are, 𝑃 (𝛾 = 0) = 0.077, 𝑃 (𝛾 = 1) = 0.462, 𝑃 (𝛾 = 2) = 0.075, and
𝑃 (𝛾 = 3) = 0.386. We can threshold the low-probability values of gamma, ensuring that no more
78                                                                                               Abhijith J., et al.


than the maximum number (as given in [58]) of distinct values of gamma remain. These gammas
are then plugged into the calculation of the weight spectrum and the partition function.

18     QUANTUM STATE PREPARATION
The problem of preparing an 𝑛-qubit state consists first of finding the unitary transformation that
takes the 𝑁 -dimensional vector (1,0,. . . 0) to the desired state (𝛼 1 , . . . , 𝛼 𝑁 ), where 𝑁 = 2𝑛 , and then
rendering the unitary transformation into a sequence of gates.

18.1    Single qubit state preparation
As discussed before, a single qubit quantum state |𝜓 ⟩ is represented as a superposition of |0⟩ and
|1⟩ states |𝜓 ⟩ = 𝛼 |0⟩ + 𝛽 |1⟩, where |𝛼 | 2 + |𝛽 | 2 = 1. The sizes |𝛼 | 2 and |𝛽 | 2 represent the probability
of |𝜓 ⟩ being |0⟩ or |1⟩. Up to a non-observable global phase, we may assume that 𝛼 is real, so that
|𝜓 ⟩ = cos 𝜃 |0⟩ + 𝑒 𝑖𝜙 sin 𝜃 |1⟩ for some angles 𝜃, 𝜙. In this way, we can represent the state as a point
on the unit sphere with 𝜃 the co-latitude and 𝜙 the longitude. This is the well-known Bloch sphere
representation. In this way, the problem of 1-qubit state preparation consists simply of finding the
unitary transformation that takes the North pole to (𝛼, 𝛽). In practice, this amounts to finding a
sequence of available gates on actual hardware that will leave the qubit in the desired state, to a
specified desired accuracy.
   To prepare a specified state |𝜓 ⟩, we must find a 2 × 2 unitary matrix 𝑈 taking the vector |0⟩ to
|𝜓 ⟩. An obvious simple choice for 𝑈 is
                                                            − sin 𝜃𝑒 −𝑖𝜙
                                                                         
                                                 cos 𝜃
                                       𝑈 =
                                               sin 𝜃𝑒 𝑖𝜙       cos 𝜃
   This gate is directly available in IBM Q and is implemented in a composite fashion on ibmqx4 at
the hardware level. If our goal is to initialize a base state with the fewest possible standard gates,
this may not be the best choice. Instead, it makes sense to consider a more general possible unitary
operator whose first column is our desired base state, and then determine the requisite number of
standard gates to obtain it.
   Any 2 × 2 unitary matrix may be obtained by means of a product of three rotation matrices, up
to a global phase
                                        𝑈 = 𝑒 𝑖𝛼 𝑅𝑧 (𝛽)𝑅 𝑦 (𝛾)𝑅𝑧 (𝛿)
where here 𝑅𝑧 (𝛽) = diag(𝑒 𝑖𝛽/2, 𝑒 −𝑖𝛽/2 ) and 𝑅 𝑦 (𝛾) is related to 𝑅𝑧 (𝛾) by 𝑅 𝑦 (𝛾) = 𝑆𝐻𝑅𝑧 (𝛾)𝐻𝑆𝑍 . The
rotation matrices 𝑅 𝑦 (𝛾) and 𝑅𝑧 (𝛽) correspond to the associated rotations of the unit sphere under
the Bloch representation. In this way, the above decomposition is a reiteration of the standard
Euler angle decomposition of elements of 𝑆𝑂 (3). Thus the problem of approximating an arbitrary
quantum state is reduced to the problem of finding good approximations of 𝑅𝑧 (𝛾) for various values
of 𝛾.
   There has been a great deal of work done on finding efficient algorithms for approximating
elements 𝑅𝑧 (𝛾) using universal gates to a specified accuracy. However, these algorithms tend to
focus on the asymptotic efficiency: specifying approximations with the desired accuracy which are
the generically optimal in the limit of small errors. From a practical point of view, this is an issue
on current hardware, since representations tend to involve hundreds of standard gates, far outside
the realm of what may be considered practical. For this reason, it makes sense to ask the question
of how accurately one may initialize an arbitrary qubit with a specified number of gates.
   We empirically observe that the maximum possible chordal distance from a point on the Bloch
sphere to the set of exact states decreases exponentially with the number of gates. With 30 gates,
every point is within a distance of 0.024 of a desired gate. Thus, to within an accuracy of about
Quantum Algorithm Implementations for Beginners                                                                79




Fig. 52. Possible exact state initializations using 10, 15, and 20 gates. With 20 gates, every point on the sphere
is within a distance of approximately 0.072 of an exactly obtainable state. With 30 gates, every point is within
0.024



2.5%, we can represent any base state as a product of about 30 states. We do so by preserving the
states generated by 30 gates, and then for any point finding the closest exact point.

18.2    Schmidt decomposition
The initialization of qubit states using more than one qubit is aided by the so-called Schmidt
decomposition, which we now introduce. Specifically, the Schmidt decomposition allows one to
initialize a 2𝑛-qubit state by initializing a single 𝑛-qubit state, along with two specific 𝑛-qubit gates,
combined together with 𝑛 CNOT gates.
   Mathematically, an arbitrary 2𝑛-qubit state |𝜓 ⟩ may be represented as a superposition
                               ∑︁          ∑︁
                    |𝜓 ⟩ =                         𝑎𝑖 1,...,𝑖𝑛 ,𝑗1,...,𝑗𝑛 |𝑖 1𝑖 2 . . . 𝑖𝑛 𝑗1 𝑗2 . . . 𝑗𝑛 ⟩ .
                            𝑖 1 ,...,𝑖𝑛 ∈ {0,1} 𝑗1 ,...,𝑗𝑛 ∈ {0,1}

In a Schmidt decomposition, we obtain such a state by strategically choosing two orthonormal
bases 𝜉 𝑗 , 𝜑 𝑗 for 𝑗 = 1, . . . , 2𝑛 of the Hilbert space of 𝑛-qubit states and then writing |𝜓 ⟩ as the
product
                                                                2𝑛
                                                                ∑︁
                                                     |𝜓 ⟩ =           𝜆𝑖 |𝜉𝑖 ⟩ |𝜑𝑖 ⟩ ,
                                                                𝑖=1

for some well-chosen 𝜆𝑖 ’s.
   The bases 𝜉 𝑗 and 𝜑 𝑗 may be represented in terms of two unitary matrices 𝑈 , 𝑉 ∈ 𝑈 (2𝑛 ), while
the 𝜆𝑖 ’s may be represented in terms of a single 𝑛-qubit state. We represent this latter state as
𝐵 |00 . . . 0⟩ for some 𝐵 ∈ 𝑈 (2𝑛 ). Then from a quantum computing perspective, the product in the
Schmidt decomposition may be accomplished by a quantum circuit combining 𝑈 , 𝑉 , and 𝐵 with 𝑛
CNOT gates as shown below for 𝑛 = 6.
   Let 𝐶𝑖𝑗 denote the CNOT operator with control 𝑗 and target 𝑖. Algebraically, the above circuit
may be written as a unitary operator 𝑇 ∈ 𝑈 (22𝑛 ) of the form
                                             1      2               𝑛
                              𝑇 = (𝑈 ⊗ 𝑉 ) (𝐶𝑛+1 ⊗ 𝐶𝑛+2 ⊗ · · · ⊗ 𝐶 2𝑛 ) (𝐵 ⊗ 𝐼 ).

We will use |𝑒 1 ⟩ , . . . , |𝑒 2𝑛 ⟩ to denote the standard computational basis for the space of 𝑛-qubit states,
in the usual order. We view each of the elements 𝑒 𝑗 as a vector in {0, 1}𝑛 . In this notation, the
formation of CNOT gates above acts on simple tensors by sending
                   1      2               𝑛
                  𝐶𝑛+1 ⊗ 𝐶𝑛+2 ⊗ · · · ⊗ 𝐶 2𝑛 : |𝑒𝑖 ⟩ 𝑒 𝑗 ↦→ |𝑒𝑖 ⟩ 𝑒𝑖 + 𝑒 𝑗 , 𝑒𝑖 , 𝑒 𝑗 ∈ {0, 1}𝑛 ,
80                                                                                                               Abhijith J., et al.



                                                  •
                                                          •
                                                                 •
                                    𝐵                                    •                    𝑈
                                                                                •
                                                                                    •


                                                                                              𝑉



                                          Fig. 53. Schmidt decomposition.


where addition in the above is performed modulo 2. Therefore the action of the operator 𝑇 associated
to the above circuit on the basis vector |00 . . . 0⟩ is
                                               1      2               𝑛
                   𝑇 |00 . . . 0⟩ = (𝑈 ⊗ 𝑉 ) (𝐶𝑛+1 ⊗ 𝐶𝑛+2 ⊗ · · · ⊗ 𝐶 2𝑛 ) (𝐵 ⊗ 𝐼 ) |00 . . . 0⟩
                                                                                        2𝑛
                                                                                        ∑︁
                                             1      2               𝑛
                                = (𝑈 ⊗ 𝑉 ) (𝐶𝑛+1 ⊗ 𝐶𝑛+2 ⊗ · · · ⊗ 𝐶 2𝑛 )                      𝑏𝑖1 |𝑒𝑖 ⟩ |𝑒 1 ⟩
                                                                                        𝑖=1
                                                2𝑛
                                                ∑︁
                                = (𝑈 ⊗ 𝑉 )             𝑏𝑖1 |𝑒𝑖 ⟩ |𝑒𝑖 ⟩
                                                 𝑖=1
                                    2𝑛
                                    ∑︁
                                =         𝑏𝑖1 (𝑈 |𝑒𝑖 ⟩) (𝑉 |𝑒𝑖 ⟩) = |𝜓 ⟩ .
                                    𝑖=1
Thus we see that the above circuit performs precisely the sum desired from the Schmidt decompo-
sition.
                                                               Í2𝑛
    To get the precise values of 𝑈 , 𝑉 , and 𝐵, we write |𝜓 ⟩ = 𝑖,𝑗=1 𝑎𝑖 𝑗 |𝑒𝑖 ⟩ 𝑒 𝑗 for some constants
𝑎𝑖 𝑗 ∈ C and define 𝐴 to be the 2 × 2 matrix whose entries are the 𝑎𝑖 𝑗 ’s. Then comparing this to
                                 𝑛       𝑛

our previous expression for |𝜓 ⟩, we see
                                 2𝑛
                                 ∑︁                        2𝑛
                                                           ∑︁
                                        𝑎𝑖 𝑗 |𝑒𝑖 ⟩ 𝑒 𝑗 =         𝑏𝑘1 (𝑈 |𝑒𝑘 ⟩) (𝑉 |𝑒𝑘 ⟩).
                                𝑖,𝑗=1                      𝑘=1

Multiplying on the left by ⟨𝑒𝑖 | 𝑒 𝑗 this tells us
                                                          2𝑛
                                                          ∑︁
                                                𝑎𝑖 𝑗 =          𝑏𝑘1𝑢𝑖𝑘 𝑣 𝑗𝑘 ,
                                                          𝑘=1

where here 𝑢𝑖𝑘 = ⟨𝑒𝑖 | 𝑈 |𝑒𝑘 ⟩ and 𝑣 𝑗𝑘 = 𝑒 𝑗 𝑉 |𝑒𝑘 ⟩ are the 𝑖, 𝑘’th and 𝑗, 𝑘’th entries of 𝑈 and 𝑉 ,
respectively. Encoding this in matrix form, this tells us
                                           𝑉 diag(𝑏𝑖1, . . . , 𝑏𝑖𝑛 )𝑈 𝑇 = 𝐴.
Then to calculate the value of 𝑈 , 𝑉 and the 𝑏𝑖1 ’s, we use the fact that 𝑉 is unitary to calculate:
                                    𝐴†𝐴 = 𝑈 𝑇 † diag(|𝑏𝑖1 | 2, . . . , |𝑏𝑖𝑛 | 2 )𝑈 𝑇 .
Thus if we let |𝜆1 | 2, . . . , |𝜆𝑛 | 2 be the eigenvalues of 𝐴†𝐴, and let 𝑈 to be a unitary matrix satisfying
                                    𝑈 𝑇 𝐴†𝐴𝑈 𝑇 † = diag(|𝜆1 | 2, . . . , |𝜆𝑁 | 2 ),
Quantum Algorithm Implementations for Beginners                                                              81


let 𝑏𝑖1 = 𝜆𝑖 for 𝑖 = 1, . . . , 𝑛 and let
                                            𝑉 = 𝐴𝑈 𝑇 † diag(𝜆1, . . . , 𝜆𝑛 ) −1 .
               is unitary, and one easily checks that 𝑉 is therefore also unitary. Moreover 𝑖 |𝑏𝑖1 | 2 =
                                                                                             Í
The matrix 𝑈
Tr(𝐴†𝐴) = 𝑖 |𝑎𝑖 𝑗 | 2 = 1, and so the 𝑏𝑖1 ’s are representative of an 𝑛-qubit state and can be taken as
             Í
the first column of 𝐵. Readers familiar with singular value decompositions (SVD) will recognize
that the Schmidt decomposition of a bipartite state is essentially the SVD of the coefficient matrix
𝐴 associated with the state. The 𝜆𝑖 coefficients being the singular values of 𝐴.

18.3    Two-qubit state preparation
An arbitrary two-qubit state |𝜓 ⟩ is a linear combination of the four base states |00⟩ , |01⟩ , |10⟩ , |11⟩
such that the square sum of the magnitudes of the coefficients is 1. In terms of a quantum circuit,
this is the simplest case of the circuit defined above in the Schmidt decomposition, and may be
accomplished with three 1-qubit gates and exactly 1 CNOT gate, as featured in Fig. 54.


                                                       𝐵     •       𝑈
                                                                     𝑉

Fig. 54. Circuit for two qubit-state preparation. The choice of 𝑈 , 𝑉 , and 𝐵 are covered comprehensively in the
Schmidt decomposition description.


18.4    Two-qubit gate preparation
In order to initialize a four-qubit state, we require the initialization of arbitrary two-qubit gates. A
two-qubit gate may be represented as an element 𝑈 of 𝑆𝑈 (4). As it happens, any element of 𝑈 (4)
may be obtained by means of precisely 3 CNOT gates, combined with 7 1-qubit gates arranged in a
circuit of the form given in Fig. 55.


                                            𝐶          𝑅1        •                  𝐴

                                            𝐷    •     𝑅2                𝑅3   •     𝐵

                         Fig. 55. Circuit implementation of an arbitrary two qubit gate.


   The proof of this is nontrivial and relies on a characterization of the image of 𝑆𝑈 (2) ⊗2 in 𝑆𝑈 (4)
using the Makhlin invariants [111]. We do not aim to reproduce the proof here. Instead, we merely
aim to provide a recipe by which one may successfully obtain any element of 𝑆𝑈 (4) via the above
circuit and an appropriate choice of the one-qubit gates.
   Let 𝑈 ∈ 𝑆𝑈 (4) be the element we wish to obtain. To choose 𝐴, 𝐵, 𝐶, 𝐷 and the 𝑅𝑖 ’s, let 𝐶 𝑖𝑗 denote
the CNOT gate with control on qubit 𝑖 and target qubit 𝑗 and define 𝛼, 𝛽, 𝛿 by
                                        𝑥 +𝑦        𝑥 +𝑧       𝑦 +𝑧
                                   𝛼=         , 𝛽=       ,𝛿=
                                          2           2          2
for 𝑒 𝑖𝑥 , 𝑒 𝑖𝑦 , 𝑒 𝑖𝑧 the eigenvalues of the operator 𝑈 (𝑌 ⊗ 𝑌 )𝑈 𝑇 (𝑌 ⊗ 𝑌 ). Then set
                            𝑅1 = 𝑅𝑧 (𝛿), 𝑅2 = 𝑅 𝑦 (𝛽), 𝑅3 = 𝑅 𝑦 (𝛼), 𝐸 = 𝐶 12 (𝑆𝑧 ⊗ 𝑆𝑥 )
82                                                                                               Abhijith J., et al.



                    𝐵     •    𝑈         •         𝐶1           𝑅1     •                 𝐴1

                               𝑉              •    𝐷1      •    𝑅2          𝑅3     •     𝐵1

                                                   𝐶2           𝑆1     •                 𝐴2

                                                   𝐷2      •    𝑆2           𝑆3    •     𝐵2


Fig. 56. Circuit for four qubit-state preparation. The four phases of the circuit are indicated in dashed boxes.


and also
                          𝑉 = 𝑒 𝑖𝜋 /4 (𝑍 ⊗ 𝐼 )𝐶 12 (𝐼 ⊗ 𝑅3 )𝐶 21 (𝑅1 ⊗ 𝑅2 )𝐶 12 (𝐼 ⊗ 𝑆𝑧† ),
where 𝑆𝑧 is the single qubit 𝜋/2 rotation around the 𝑧 axis. Define 𝑈e, 𝑉e by 𝑈e = 𝐸 †𝑈 𝐸 and 𝑉e = 𝐸 †𝑉 𝐸.
Let 𝐴,
    e𝐵 e be the real, unitary matrices diagonalizing the eigenvectors of 𝑈e𝑈e𝑇 and 𝑉 𝑉e𝑇 , respectively.
Set 𝑋 = 𝐴    e and 𝑌 = 𝑉 † 𝐵
          e𝑇 𝐵              e𝑇 e𝐴𝑈 . Then 𝐸𝑋 𝐸 † and 𝐸𝑌 𝐸 † are in 𝑆𝑈 (2) ⊗2 and we choose 𝐴, 𝐵, 𝐶, 𝐷
such that
                          (𝐴𝑆𝑧† ) ⊗ (𝐵𝑒 𝑖𝜋 /4 ) = 𝐸𝑋 𝐸 † and 𝐶 ⊗ (𝑆𝑧 𝐷) = 𝐸𝑌 𝐸 † .
By virtue of this construction, the above circuit is algebraically identical to 𝑈 .

18.5    Four qubit state preparation
For efficient four qubit state preparation we use the recipe in Ref.[97]. Results in the previous
sections show that any two-qubit state requires 1 CNOT gate, any two-qubit operator requires
three CNOT gates, and the Schmidt decomposition of a four qubit state requires two CNOT gates
. From this we see that we should be able to write a circuit initializing any four-qubit state with
only 9 CNOT gates in total, along with 17 one-qubit gates. This represents the second most simple
case of the Schmidt decomposition, which we write in combination with our generic expression
for 2-qubit gates as shown in Fig. 56. The above circuit naturally breaks down into four distinct
stages, as shown by the separate groups surrounded by dashed lines. During the first stage, we
initialize the first two qubits to a specific state relating to a Schmidt decomposition of the full 4
qubit state. Stage two consists of two CNOT gates relating the first and last qubits. Stages three and
four are generic circuits representing the unitary operators associated to the orthonormal bases in
the Schmidt decomposition.
   The results of this circuit implemented on a quantum processor are given in Fig. 57. While the
results when implemented on a simulator are given in Fig. 58.

19     QUANTUM TOMOGRAPHY
19.1    Problem definition and background
Quantum state estimation, or tomography, deals with the reconstruction of the state of a quantum
system from measurements of several preparations of this state. In the context of quantum com-
puting, imagine that we start with the state |00⟩, and apply some quantum algorithm (represented
by a unitary matrix 𝑈 ) to the initial state, thus obtaining a state |𝜓 ⟩. We can measure this state
in the computational 𝑧 basis, or apply some rotation (represented by 𝑉 ) in order to perform mea-
surements in a different basis. Quantum state tomography aims to answer the following question:
is it possible to reconstruct the state |𝜓 ⟩ from a certain number of such measurements? Hence,
quantum tomography is not a quantum algorithm per se, but it is an important procedure for
certifying the performance of quantum algorithms and assessing the quality of the results that
Quantum Algorithm Implementations for Beginners                                                               83




Fig. 57. Verification of 4 qubit state preparation on ibmqx2 which is a 5 qubit machine. The last qubit is not
used in the circuit. The above histogram shows that, the state prepared in ibmqx2 has nonzero overlaps with
basis states that are orthogonal to the target state to be prepared.




Fig. 58. Verification of the quantum circuit for four qubit-state preparation. The differences in the exact
and the simulator results are due to statistical fluctuations arising from the probabilistic nature of quantum
measurement. They will become closer to each other when the number of samples are increased.


can be corrupted by decoherence, environmental noise, and biases, inevitably present in analogue
machines. Moreover similar procedures can be used for certifying the initial state, as well as for
measuring the fidelity of gates.
   Given a single copy of the state, it is impossible to reconstruct |𝜓 ⟩: for example, there is no
quantum measurement that can even distinguish non-orthogonal quantum states, such as |0⟩ and
(|0⟩ + |1⟩)/2, with certainty. However, it is possible to perform quantum tomography when multiple
copies of the state is available. It means that one needs to run the quantum algorithm (i.e., apply 𝑈
to initial state) many times to produce many copies of the quantum state to be able to characterize
|𝜓 ⟩. Unfortunately, because of the noise, in practice it is impossible to obtain the exact same state
|𝜓 ⟩ every time; instead, one should see a mixture of different states: |𝜓 1 ⟩, |𝜓 2 ⟩, . . ., |𝜓𝑘 ⟩. In general,
there does not exist a single |𝜓 ⟩ describing this mixture. Therefore, we need a to use the density
matrix representation of quantum states. We briefly discussed this representation in the context of
quantum principal component analysis in Section XIV.
84                                                                                          Abhijith J., et al.


   Let us denote 𝑝𝑖 the probability of occurrence of the state |𝜓𝑖 ⟩. The density matrix of this ensemble
is given by,
                                               ∑︁
                                           𝜌=      𝑝𝑖 |𝜓𝑖 ⟩⟨𝜓𝑖 |.                                    (103)
                                                  𝑖
Using Í
      this more general definition of the state, the expected value of an observable 𝐴 is given by
⟨𝐴⟩ = 𝑝𝑖 ⟨𝜓𝑖 |𝐴|𝜓𝑖 ⟩ = Tr(𝐴𝜌). The density matrix has the following properties:
        𝑖
     • Tr 𝜌 = 1, i.e., probabilities sum to one;
     • 𝜌 = 𝜌 † , and 𝜌 ≽ 0, i.e., all eigenvalues are either positive or zero.
   The goal of quantum state tomography is to reconstruct the quantum state 𝜌 from many re-
peated runs of the quantum algorithm, using a set of measurements on 𝜌. Quantum measure-
ments are described by a collection of measurement operators 𝑀𝑖 that satisfy the completeness
relation 𝑖 𝑀𝑖† 𝑀𝑖 = 𝐼 . This condition ensures that the probabilities of measurement outcomes
           Í

𝑝𝑖 = Tr(𝜌𝑀𝑖† 𝑀𝑖 ) sum to one for any state 𝜌. In a popular setting for quantum tomography that
is closely related to what is currently achievable with modern quantum computers, the measure-
ment operators are chosen in a special class of projective measurements – projectors 𝑃𝑖 that satisfy
𝑃𝑖 𝑃 𝑗 = 𝛿𝑖,𝑗 𝑃𝑖 and 𝑖 𝑃𝑖 = 𝐼 given that in this case 𝑃𝑖† 𝑃𝑖 = 𝑃𝑖 , and hence the measurement probability
                    Í
is given by the relation 𝑝𝑖 = Tr(𝜌𝑃𝑖 ). This choice represents a single instance of a more general
measurement formalism that deals with situations when we are only interested in the probabilities
of the measurement outcomes, called Postive Operator-Valued Measures (POVM). In this introduction
we will only deal with projective measurements described above which will be sufficient for our
purpose, and refer the reader to [92] for details on POVMs and general measurement formalism.
   For a single qubit, examples of measurement projectors in the computational basis are given
by 𝑃0 = |0⟩⟨0| and 𝑃 1 = |1⟩⟨1|, and in the 𝑥-basis by 𝑃± = √1 (|0⟩ ± |1⟩) ⊗ √1 (⟨0| ± ⟨1|). At this
                                                                      2               2
point, once could ask: what is the set of projectors that represent a quorum, i.e. provides sufficient
information to identify the state of the system in the limit of a large number of observations?
The answer to this question is important for the quantum state tomography task, as it allows to
determine an informationally complete set of measurements that is necessary to reconstruct the
state. For a single-qubit example, the density matrix 𝜌 qubit can be decomposed as
                          Tr(𝜌 qubit )𝐼 + Tr(𝜌 qubit𝑋 )𝑋 + Tr(𝜌 qubit𝑌 )𝑌 + Tr(𝜌 qubit𝑍 )𝑍
                  𝜌 qubit =                                                                ,          (104)
                                                          2
where 𝑋 , 𝑌 , and 𝑍 are Pauli matrices, that can be interpreted
                                                              √        √ as projectors
                                                                              √       √ in the 𝑥-, 𝑦-, and
𝑧-basis. From this expression, it is easy to see that 𝐼 / 2, 𝑋 / 2, 𝑌 / 2, 𝑍 / 2 forms the set of
measurement operators that provide sufficient information for reconstructing the state 𝜌 qubit from
measurements 𝑝𝑖 = Tr(𝜌 qubit 𝑃𝑖 ). Using this example, a set of measurements for a general system 𝜌 is
said to be informationally complete if the relations 𝑝𝑖 = Tr(𝜌𝑃𝑖 ) can be inverted to unambiguously
reconstruct the state 𝜌. The state 𝜌 can be uniquely expressed using the obtained measurements
whenever the matrix Tr(𝑃𝑖 𝑃 𝑗 ) is invertible. For a multi-qubit state on 𝑛 qubits, a simple example of
an informationally complete set of measurements is given by a set of tensor products of all possible
combinations of Pauli matrices. Notice, however, that a smaller number of measurement operators
may be sufficient; the necessary number of measurement operators is related to the number of
independent parameters in the density matrix 𝜌.
   In real experiment, a finite number of measurements is collected for each measurement operator.
Given the measurement occurrences 𝑚𝑖 for each projector 𝑃𝑖 , we define the associated empiri-
cal frequency as 𝜔𝑖 = 𝑚𝑖 /𝑚. Then the quantum tomography problem can be stated as follows:
reconstruct 𝜌 from the informationally complete set of couples of projectors and measurement
Quantum Algorithm Implementations for Beginners                                                     85


frequencies {𝑃𝑖 , 𝜔𝑖 }. In other words, we would like to “match” Tr(𝑃𝑖 𝜌) and 𝜔𝑖 . The next section
presents a short overview of most popular general methods for the quantum state estimation.

19.2   Short survey of existing methods
Most popular methods for quantum tomography in the general case include:
  (1) Linear inversion. In this method, we simply aim at inverting the system of equations
      Tr(𝑃𝑖 𝜌) = 𝜔𝑖 . Although being fast, for a finite number of measurements thus obtained
      estimation 𝜌b does not necessarily satisfy 𝜌b ≽ 0 (i.e., might contain negative eigenvalues):
      this happens due to experimental inaccuracies and statistical fluctuations of coincidence
      counts, which leads to differences between the empirical measurement frequencies 𝜔𝑖 and
      the calculated values Tr(𝑃𝑖 𝜌) [70].
  (2) Linear regression. This method corrects for the disadvantages of the linear inversion by
      solving a constrained quadratic optimization problem [101]:
                                       ∑︁
                       𝜌b = argmin             [Tr(𝑃𝑖 𝜌) − 𝜔𝑖 ] 2    s.t. Tr 𝜌 = 1 and 𝜌 ≽ 0.
                               𝜌       𝑖


      However, this objective function implicitly assumes that the residuals are Gaussian-distributed,
      which may hold in a limit of a large number of independent measurements due to the central
      limit theorem, but does not necessarily apply in practice for a finite number of measurements
      where deviations from normal distribution can be important.
  (3) Maximum likelihood. In this by far most popular algorithm for quantum state estimation,
      one aims at maximizing the log-probability of observations [67, 70]:
                                       ∑︁
                        𝜌b = argmax             𝜔𝑖 ln Tr(𝑃𝑖 𝜌)      s.t. Tr 𝜌 = 1 and 𝜌 ≽ 0.
                                   𝜌       𝑖


      This is a convex problem that outputs a positive semidefinite (PSD) solution 𝜌b ≽ 0. However,
      it is often stated that the maximum likelihood (ML) method is slow, and several recent papers
      attempted to develop faster methods of gradient descent with projection to the space of PSD
      matrices, see e.g. [109]. Among other common criticisms of this method one can name the
      fact that ML might yield rank-deficient solutions, which results in an infinite conditional
      entropy that is often used as a metric of success of the reconstruction.
  (4) Bayesian methods. This is a slightly more general approach compared to the ML method
      which includes some prior [19], or corrections to the basic ML objective, see e.g., the so-called
      Hedged ML [18]. However, it is not always clear how to choose these priors in practice.
      Markov Chain Monte Carlo Methods that are used for general priors are known to be slow.
Let us mention that there exist other state reconstruction methods that attempt to explore a
particular known structure of the density matrix, such as compressed-sensing methods [62] in the
case of low-rank solutions, and matrix product states [38] or neural networks based approaches [126]
for pure states with limited entanglement, etc. One of the points we can conclude from this section
is that the ultimately best general method for the quantum state tomography is not yet known and
certainly depends on the applications. However, it seems that maximum likelihood is still the most
widely discussed method in the literature; in what follows, we implement and test ML approach to
quantum tomography on the IBM quantum computer.
86                                                                                              Abhijith J., et al.




Fig. 59. Left: measurements of the single qubit state after the application of the Hadamard gate, in 𝑧, 𝑦 and 𝑥
basis. Right: experimental setup for testing the effects of decoherence.

19.3    Implementation of the Maximum Likelihood method on 5-qubit IBM QX
We present an efficient implementation of the ML method using a fast gradient descent with an
optimal 2-norm projection [117] to the space of PSD matrices3 . In what follows, we apply quantum
tomography to study the performance of the IBM Q.
19.3.1 Warm-up: Hadamard gate. Let us start with a simple one-qubit case of the Hadamard gate, see
Fig. 59, Left. This gate transforms the initial qubit state |0⟩ as follows: 𝐻 : |0⟩ → |+⟩𝑥 = √1 (|0⟩ + |1⟩),
                                                                                               2
so that the density matrix should be close to 𝜌 = |+⟩𝑥 ⟨+|𝑥 . As discussed in section 19.1, for
performing quantum tomography in the single-qubit case, it is sufficient to collect measurements in
the 𝑥, 𝑦, and 𝑧 basis. In the limit of a large number of measurements, we expect to see the following
frequencies in the 𝑧, 𝑦, and 𝑥 basis (all vector expressions are given in the computational basis):
                                                                                             
 1       1       0     1               1 1        1      1 1           1           1 1            1 1
     → ,            → ,              √        → , √                → ,            √       → 1, √             → 0.
 0       2       1     2                2 𝑖       2       2 −𝑖         2            2 1            2 −1
   We learn the estimated density matrix 𝜌b from measurements in each basis using the maximum
likelihood method, and look at the decomposition:
                                       𝜌b = 𝜆1 |𝜓 1 ⟩⟨𝜓 1 | + 𝜆2 |𝜓 2 ⟩⟨𝜓 2 |,
which would allow us to see what eigenstates contribute to the density matrix, and what is their
                                                                                           1 𝑇
                                                                                       h     i
                                                                                         1
weight. Indeed, in the case of ideal observations we should get 𝜆1 = 1, with |𝜓 1 ⟩ = √2 √2 , and
                             1 𝑇
                     h         i
                       1
𝜆2 = 0 with |𝜓 2 ⟩ = √2 − √2 , corresponding to the original pure state associated with |+⟩𝑥 .
   Instead, we obtain the following results for the eigenvalues and associated eigenvectors after
8152 measurements (the maximum number in one run on IBM QX) in each basis (𝑧, 𝑦, 𝑥):
                                                                                  
                                 0.715 − 0.012𝑖                      0.699 − 0.012𝑖
                 𝜆1 = 0.968 →                     ,  𝜆2 = 0.032 →                      ,
                                     0.699                               −0.715
i.e., in 96% of cases we observe the state close to |+⟩𝑥 , and the rest corresponds to the state which
is close to |−⟩𝑥 . Note that the quantum simulator indicates that this amount of measurements is
sufficient to estimate matrix elements of the density matrix with an error below 10−3 in the ideal
noiseless case. In order to check the effect of decoherence, we apply a number of identity matrices
(Fig. 59, Right) which forces an additional waiting on the system, and hence promotes decoherence
of the state. When applying 18 identity matrices, we obtain the following decomposition for 𝜌b
                                                                                     
                                  0.727 − 0.032𝑖                         0.685 − 0.030𝑖
                 𝜆1 = 0.940 →                      ,   𝜆2 = 0.060 →                       ,
                                      0.686                                  −0.728
3 Thejulia implementation of the algorithm is available at http://gitlab.lanl.gov/QuantumProgramming2017/
QuantumTomography
Quantum Algorithm Implementations for Beginners                                                        87




Fig. 60. Left: example of a measurement of the two-qubit maximally entangled state created with the
combination of 𝐻 , 𝑋 and 𝐶𝑁𝑂𝑇 gates in the 𝑦𝑧 basis. Right: experimental setup for testing the effects of
decoherence.

while application of 36 identity matrices results in
                                                                                
                                0.745 − 0.051𝑖                      0.663 − 0.045𝑖
               𝜆1 = 0.927 →                      ,   𝜆2 = 0.073 →                    .
                                    0.664                               −0.747
The effect of decoherence is visible in the degradation of the eigenstates, as well as in a more
frequent occurrence of the eigenstate close to |−⟩𝑥 .
19.3.2 Maximally entangled state for two qubits. Let us now study the two-qubits maximally
entangled state, which is an important part of all quantum algorithms achieving quantum speed-up
over their classical counterparts. The state √1 (|10⟩ + |01⟩) we are interested in is produced by the
                                                 2
combination of 𝐻 , 𝑋 and 𝐶𝑁𝑂𝑇 gates as shown in Fig. 60, Left. We follow the same procedure as
in the case of the Hadamard gate, described above, and first estimate the density matrix 𝜌b using
8152 measurements for each of the 𝑧𝑧, 𝑦𝑦, 𝑥𝑥, 𝑧𝑥 and 𝑦𝑧 basis, and then decompose it as 𝜌b =
                                                                                       h             i𝑇
                                                                                         0 √1 √1 0 .
Í4
  𝑖=1 𝜆𝑖 |𝜓𝑖 ⟩⟨𝜓𝑖 |. Once again, ideally we should get 𝜆1 = 1 associated with |𝜓 1 ⟩ =       2   2
Instead, the analysis of the leading eigenvalues indicates that the eigenstate which is close (although
significantly distorted) to the theoretical “ground truth” |𝜓 1 ⟩ above occurs in the mixture only with
probability 0.87:
                           −0.025 − 0.024𝑖                             0.598      
                                                                                  
                                0.677                              0.123 + 0.468𝑖 
              𝜆1 = 0.871 → 
                                           ,         𝜆2 = 0.059 → 
                                                                                    .
                                 0.735                              −0.075 − 0.445𝑖 
                                                                                    
                                           
                           −0.029 − 0.017𝑖                         0.454 − 0.022𝑖 
                                                                                  
Our test of decoherence implemented using 18 identity matrices (see Figure 60, Right) shows that
the probability of the “original” entangled state decreases to 0.79:
                              −0.025 − 0.012𝑖                          0.997      
                                                                                  
                                   0.664                          −0.002 − 0.058𝑖 
              𝜆1 = 0.793 →   
                                               ,
                                                    𝜆2 = 0.111 →                  .
                                    0.747                            0.035 + 0.036𝑖 
                                                                                     
                                              
                              −0.017 − 0.008𝑖                      0.006 + 0.007𝑖 
                                                                                  
Interestingly enough, the second most probable eigenstate changes to the one that is close to |00⟩.
This might serve as an indication of the presence of biases in the machine.
   The application of the quantum tomography state reconstruction to simple states in the IBM
QX revealed an important level of noise and decoherence present in the machine. It would be
interesting to check if the states can be protected by using the error correction schemes, which is
the subject of the next section.
88                                                                                         Abhijith J., et al.


20     TESTS OF QUANTUM ERROR CORRECTION IN IBM Q
In this section, we study whether quantum error correction (QEC) can improve computation
accuracy in ibmqx4. The practical answer to this question seems to be “No”. Although some error
correction effects are observed in ibmqx4, improvements are not exponential and get completely
spoiled by errors induced by extra gates and qubits needed for the error correction protocols.

20.1    Problem definition and background
As we have seen throughout this review, the quality of computation on actual quantum processors
is degraded by errors in the system. This is because currently available chips are not fault tolerant. It
is widely believed that once the inherent error rates of a quantum processor is sufficiently lowered,
fault tolerant quantum computation will be possible using quantum error correction (QEC). The
current error rates of the IBM Q machines are not small enough to allow fault tolerant computation.
We refer the reader to a survey and introduction on QEC [42], while at the same time offering an
alternative point of view that we support with a few experiments on the IBM chip. Detailed studies
of QEC using more sophisticated error correcting schemes have been performed on IBM hardware
[124, 132, 134]. Qiskit also provides some tools that can be used for QEC. The recent work in Ref.
[133] introduces some of these capabilities of Qiskit with example code.
   The central idea of QEC is to use entanglement to encode quantum superposition in a manner
which is robust to errors. The exact encoding depends upon the kind of errors we want to protect
against. In this section we will look at a simple encoding that will protect against bit flip errors.
Here we encode a single qubit state,

                                        |𝜓 ⟩ = 𝐶 0 |0⟩ + 𝐶 1 |1⟩,                                     (105)

using an entangled state, such as

                                    |𝜓 ⟩ = 𝐶 0 |0⟩ ⊗𝑛𝑞 + 𝐶 1 |1⟩ ⊗𝑛𝑞 ,                                (106)

where 𝑛𝑞 is the number of qubits representing a single qubit in calculations.
   The assumption is that small probability errors will likely lead to unwanted flips of only one
qubit (in case when 𝑛𝑞 > 3 this number can be bigger but we will not consider more complex
situations here). Such errors produce states that are essentially different from those described by
Equation (106). Measurements can then be used to fix a single qubit error using, for instance, a
majority voting strategy. More complex errors are assumed to be exponentially suppressed, which
can be justified if qubits experience independent decoherence sources.
   We question whether QEC can work to protect quantum computations that require many
quantum gate operations for the following reason. The main source of errors then is not spontaneous
qubit decoherence but rather the finite fidelity of quantum gates. When quantum gates are applied
to strongly entangled states, such as (106), they lead to highly correlated dynamics of all entangled
qubits. We point out that errors introduced by such gates have essentially different nature from
random uncorrelated qubit flips. Hence, gate-induced errors may not be treatable by standard error
correction strategies when transitions are made between arbitrary unknown quantum state.
   To explore this point, imagine that we apply     √ a gate that rotates a qubit by an angle 𝜋/2. It
switches superposition states |𝜓 ± ⟩ = (|0⟩ ± |1⟩)/ 2 into, respectively, |0⟩ or |1⟩ in the measurement
basis. Let the initial state be |𝜓 + ⟩ but we do not know this before the final measurement. Initially,
we know only that initial state can be either |𝜓 + ⟩ or |𝜓 − ⟩. To find what it is, we rotate qubit to the
measurement basis. The gate is not perfect, so the final state after the gate application is

                                  |𝑢⟩ = cos(𝛿𝜙)|0⟩ + sin(𝛿𝜙)|1⟩,                                      (107)
Quantum Algorithm Implementations for Beginners                                                              89




                                                                  √
Fig. 61. Quantum circuit that creates the state |+⟩ = (|0⟩ + |1⟩)/ 2 then applies 16 T-gates that are equivalent
to the identity operation, and then applies the gate that transforms the entangled state into the trivial state
|0⟩.


with some error angle 𝛿𝜙 ≪ 1. Measurement of this state would produce the wrong answer 1 with
probability
                                               𝑃 ≈ (𝛿𝜙) 2 .                                               (108)
The value 1 − 𝑃 is called the fidelity of the gate. In IBM chip it is declared to be 0.99 at the time
of writing, which is not much. It means that after about 30 gates we should loose control. Error
correction strategies can increase the number of allowed gates by an order of magnitude even at
such a fidelity if we encode one qubit in three.
   In order to reduce this error, we can attempt to work with the 3-qubit version of the states in
Eq. (106). For example, let us consider the desired gate that transfers states
                                                          √
                                   |±⟩ = (|000⟩ ± |111⟩)/ 2,                                     (109)
into states |000⟩ and |111⟩ in the measurement basis, respectively. This gate is protected in the
sense that a single unwanted random qubit flip leads to final states that are easily corrected by
majority voting.
   However, this is not enough because now we have to apply the gate that makes a rotation by
𝜋/2 in the basis (109). The error in this rotation angle leads to the final state
                                 |𝑢⟩ = cos(𝛿𝜙)|000⟩ + sin(𝛿𝜙)|111⟩,                                       (110)
i.e., this particular error cannot be treated with majority voting using our scheme because it flips
all three qubits. On the other hand, this is precisely the type of errors that is most important when
we have to apply many quantum gates because basic gate errors are mismatches between desired
and received qubit rotation angles irrespectively of how the qubits are encoded. With nine qubits,
we could protect the sign in Eq. 110 but this was beyond our hardware capabilities.
   Based on these thoughts, traditional QEC may not succeed in achieving exponential suppression
of errors related to non-perfect quantum gate fidelity. The latter is the main source of decoherence
in quantum computing that involves many quantum gates. As error correction is often called the
only and first application that matters before quantum computing becomes viable at large scale,
this problem must be studied seriously and expeditiously. In the following subsection we report on
our experimental studies of this problem with IBM’s 5-qubit chip.

20.2   Test 1: errors in single qubit control
First, let us perform trivial operation shown in Fig. 61: we create a superposition of two qubit states
                                                         √
                                       |+⟩ = (|0⟩ + |1⟩)/ 2,                                      (111)
90                                                                                               Abhijith J., et al.




                                                                  √
Fig. 62. Quantum circuit that creates state |−⟩ = (|000⟩ − |111⟩)/ 2 then applies 16 T-gates that are equivalent
to the identity operation, and then applies the gate that transforms the entangled GHZ state back into the
trivial state |000⟩. Measurements that return 1 for only one of the three qubits are interpreted as the |000⟩
state at the end, while outcomes with two or three units are interpreted as the final state |111⟩.


then apply many gates that altogether do nothing, i.e., they just bring the qubit back to the
superposition state (111). We need those gates just to accumulate some error while the qubit’s state
is not trivial in the measurement basis. Finally, we apply the gate that transforms its state back to
|0⟩.
   Repeated experiments with measurements then produced wrong answer 13 times from 1000
samples. Thus, we estimate the error of the whole protocol, which did not use QEC, as
                                                 𝑃1 = 0.013,
or 1.6%. This is consistent and even better than declared 1% single gate fidelity because we applied
totally 18 gates.

20.3   Test 2: errors in entangled 3 qubits control
                                                                                                       √
Next, we consider the circuit in Fig. 62 that initially creates the GHZ state |−⟩ = (|000⟩ − |111⟩)/ 2,
then applies the same number, i.e. 16, of 𝑇 -gates that lead to the same GHZ state. Then we apply
the sub-circuit that brings the whole state back to |000⟩.
   Our goal is to quantify the precision of identifying the final result with the state |000⟩. If a single
error bit flip happens, we can interpret results |100⟩, |010⟩ and |001⟩ as |000⟩ using majority voting.
If needed, we can then apply a proper pulse to correct for this. So, in such cases we can consider the
error treatable. If the total sum of probabilities of the final state |000⟩ and final states with a single
bit flipped is larger than 𝑃1 from the previous single-qubit test, then we say that the quantum error
correction works, otherwise, it doesn’t. Our experiments showed that probabilities of events that
lead to wrong final interpretation are as follows:
                       𝑃 110 = 0.006,   𝑃101 = 0.02,    𝑃011 = 0.016,     𝑃111 = 0.005.
Thus, the probability to get the wrong interpretation of the result as the final state |111⟩ of the
encoded qubit is
                               𝑃3 = 𝑃 110 + 𝑃 101 + 𝑃 011 + 𝑃 111 = 0.047,
while the probability to get any error 1 − 𝑃 000 = 0.16.

20.4   Discussion
Comparing results of the tests without and with QEC, we find that the implementation of a simple
version of QEC does not improve the probability to interpret the final outcome correctly. The
error probability of calculations without QEC gives a smaller probability of wrong interpretation,
Quantum Algorithm Implementations for Beginners                                                                     91


𝑃1 = 1.3%, while the circuit with QEC gives an error probability 𝑃3 = 4.7%, even though we used
majority voting that was supposed to suppress errors by about an order of magnitude.
   More importantly, errors that lead to more than one qubit flip are not exponentially suppressed.
For example, the probability 𝑃 101 = 0.02 is close to the probability of a single bit flip event 𝑃010 =
0.029. We interpret this to mean that errors are not the results of purely random bit flip decoherence
effects but rather follow from correlated errors induced by the finite precision of quantum gates.
The higher error rate in 3-qubit case could be attributed to the much worse fidelity of the controlled-
NOT gate. The circuit itself produces the absolutely correct result |000⟩ in 84% of simulations. If
the remaining errors were produced by uncorrelated bit flips, we would see outcomes with more
than one wrong bit flip with total probability less than 1% but we found that such events have a
much larger total probability 𝑃 3 = 4.7%.
   In defense of QEC, we note that probabilities of single bit flip errors were still several times
larger than probabilities of multiple (two or three) wrong qubit flip errors. This means that at least
partly QEC works, i.e., it corrects the state to |000⟩ with 4.7% precision, versus the initially 16%
in the wrong state. So, at least some part of the errors can be treated. However, an efficient error
correction must show exponential suppression of errors, which was not observed in this test.
   Summarizing, this brief test shows no improvements that would be required for efficient quantum
error correction. The need to use more quantum gates and qubits to correct errors only leads to
a larger probability of wrong interpretation of the final state. This problem will likely become
increasingly much more important because without quantum error correction the whole idea
of conventional quantum computing is not practically useful. Fortunately, IBM’s quantum chips
can be used for experimental studies of this problem. We also would like to note that quantum
computers can provide computational advantages beyond standard quantum algorithms and using
only classical error correction [115]. So, they must be developed even if problems with quantum
error correction prove detrimental for conventional quantum computing schemes at achievable
hardware quality.

ACKNOWLEDGMENTS
We would like to acknowledge the help from numerous readers who pointed out errors and misprints
in the earlier version of the manuscript. The code and implementations accompanying the paper
can be found at https://github.com/lanl/quantum_algorithms.

REFERENCES
  [1] ibmq-device-information. https://github.com/Qiskit/ibmq-device-information/tree/master/backends/tenerife/V1.
      Accessed: 14-12-2019.
  [2] Scott Aaronson. Read the fine print. Nature Physics, 11(4):291–293, 2015.
  [3] Scott Aaronson and Lijie Chen. Complexity-theoretic foundations of quantum supremacy experiments. In Ryan
      O’Donnell, editor, 32nd Computational Complexity Conference, CCC 2017, July 6-9, 2017, Riga, Latvia, volume 79 of
      LIPIcs, pages 22:1–22:67. Schloss Dagstuhl - Leibniz-Zentrum fuer Informatik, 2017.
  [4] Héctor Abraham, Ismail Yunus Akhalwaya, Gadi Aleksandrowicz ...., and yotamvakninibm. Qiskit: An open-source
      framework for quantum computing, 2019.
  [5] A. Ambainis, H. Buhrman, P. Høyer, M. Karpinski, and P. Kurur. Quantum matrix verification. 2002.
  [6] Andris Ambainis. Quantum walk algorithm for element distinctness. SIAM Journal on Computing, 37(1):210–239,
      2007.
  [7] Andris Ambainis and R. Spalec. Quantum algorithms for matching and network flows. in Lecture Notes in Computer
      Science: STACS 2006, 3884, 2006.
  [8] Itai Arad and Zeph Landau. Quantum computation and the evaluation of tensor networks. SIAM Journal on Computing,
      39(7):3089–3121, 2010.
  [9] Frank Arute, Kunal Arya, Ryan Babbush, Dave Bacon, Joseph C Bardin, Rami Barends, Rupak Biswas, Sergio Boixo,
      Fernando GSL Brandao, David A Buell, et al. Quantum supremacy using a programmable superconducting processor.
      Nature, 574(7779):505–510, 2019.
92                                                                                                         Abhijith J., et al.


[10] Dave Bacon, Isaac L Chuang, and Aram W Harrow. The quantum schur and clebsch-gordan transforms: I. efficient
     qudit circuits. pages 1235–1244, 2007.
[11] Dave Bacon and Wim Van Dam. Recent progress in quantum algorithms. Communications of the ACM, 53(2):84–93,
     2010.
[12] Stefanie Barz, Ivan Kassal, Martin Ringbauer, Yannick Ole Lipp, Borivoje Dakić, Alán Aspuru-Guzik, and Philip
     Walther. A two-qubit photonic quantum processor and its application to solving systems of linear equations. Scientific
     reports, 4, 2014.
[13] Robert Beals. Quantum computation of Fourier transforms over symmetric groups . In Proceedings of STOC, pages
     48–53, 1997.
[14] Giuliano Benenti and Giuliano Strini. Quantum simulation of the single-particle Schrödinger equation. American
     Journal of Physics, 76(7):657–662, 2008.
[15] Charles H Bennett, Ethan Bernstein, Gilles Brassard, and Umesh Vazirani. Strengths and weaknesses of quantum
     computing. SIAM journal on Computing, 26(5):1510–1523, 1997.
[16] E. Bernstein and U. Vazirani. Quantum complexity theory. In Proc. of the Twenty-Fifth Annual ACM Symposium on
     Theory of Computing (STOC ’93), pages 11–20, 1993. DOI:10.1145/167088.167097.
[17] Dominic W Berry, Graeme Ahokas, Richard Cleve, and Barry C Sanders. Efficient quantum algorithms for simulating
     sparse hamiltonians. Communications in Mathematical Physics, 270(2):359–371, 2007.
[18] Robin Blume-Kohout. Hedged maximum likelihood quantum state estimation. Physical review letters, 105(20):200504,
     2010.
[19] Robin Blume-Kohout. Optimal, reliable estimation of quantum states. New Journal of Physics, 12(4):043034, 2010.
[20] Otakar Borůvka. O jistém problému minimálním. Práce Mor. Přírodově d. spol. v Brnř (Acta Societ. Scient. Natur.
     Moravicae), 3:37–58, 1926.
[21] Michel Boyer, Gilles Brassard, Peter Høyer, and Alain Tapp. Tight bounds on quantum searching. Fortschritte der
     Physik: Progress of Physics, 46(4-5):493–505, 1998.
[22] Lucas T. Brady, Christopher L. Baldwin, Aniruddha Bapat, Yaroslav Kharkov, and Alexey V. Gorshkov. Optimal
     Protocols in Quantum Annealing and Quantum Approximate Optimization Algorithm Problems. Physical Review
     Letters, 126:070505, 2021.
[23] G. Brassard et al. Quantum amplitude amplification and estimation. Quantum Computation and Quantum Information,
     9, 2002.
[24] Carlos Bravo-Prieto, Ryan LaRose, Marco Cerezo, Yigit Subasi, Lukasz Cincio, and Patrick J Coles. Variational quantum
     linear solver: A hybrid algorithm for linear systems. arXiv preprint arXiv:1909.05820, 2019.
[25] Sergey Bravyi, Alexander Kliesch, Robert Koenig, and Eugene Tang. Obstacles to Variational Quantum Optimization
     from Symmetry Protection. Physical Review Letters, 125:260505, 2020.
[26] H. Buhrman and R. Spalek. Quantum verification of matrix products. Proceedings of the seventeenth annual ACM-SIAM
     symposium on Discrete algorithm, pages 880–889, 2006.
[27] X.-D. Cai, C. Weedbrook, Z.-E. Su, M.-C. Chen, M. Gu, M.-J. Zhu, L. Li, N.-L. Liu, C.-Y. Lu, and J.-W. Pan. Experimental
     Quantum Computing to Solve Systems of Linear Equations. Physical Review Letters, 110(23):230501, June 2013.
[28] Kevin K. H. Cheung and Michele Mosca. Decomposing finite abelian groups. Quantum Info. Comput., 1(3):26–32,
     October 2001.
[29] Nai-Hui Chia, András Gilyén, Han-Hsuan Lin, Seth Lloyd, Ewin Tang, and Chunhao Wang. Quantum-Inspired
     Algorithms for Solving Low-Rank Linear Equation Systems with Logarithmic Dependence on the Dimension. In Yixin
     Cao, Siu-Wing Cheng, and Minming Li, editors, 31st International Symposium on Algorithms and Computation (ISAAC
     2020), volume 181 of Leibniz International Proceedings in Informatics (LIPIcs), pages 47:1–47:17, Dagstuhl, Germany,
     2020. Schloss Dagstuhl–Leibniz-Zentrum für Informatik.
[30] Andrew M Childs and Wim Van Dam. Quantum algorithms for algebraic problems. Reviews of Modern Physics, 82(1):1,
     2010.
[31] Lukasz Cincio, Yiğit Subaşı, Andrew T Sornborger, and Patrick J Coles. Learning the quantum algorithm for state
     overlap. New Journal of Physics, 20(11):113022, 2018.
[32] Jill Cirasella. Classical and quantum algorithms for finding cycles. MSc Thesis, pages 1–58, 2006.
[33] C. Codsil and H. Zhan. Discrete-time quantum walks and graph structures. pages 1–37, 2011.
[34] Rigetti Computing. Quantum approximate optimization algorithm. Published online at https://github.com/
     rigetticomputing/grove, 2017. Accessed: 12/01/2017.
[35] Jeremy Cook, Stephan Eidenbenz, and Andreas Bärtschi. The Quantum Alternating Operator Ansatz on Maximum
     k-Vertex Cover. In IEEE International Conference on Quantum Computing & Engineering QCE’20, pages 83–92, 2020.
[36] Stephen A. Cook. The complexity of theorem-proving procedures. In Proceedings of the Third Annual ACM Symposium
     on Theory of Computing, STOC ’71, pages 151–158, New York, NY, USA, 1971. ACM.
Quantum Algorithm Implementations for Beginners                                                                        93


 [37] D. Coppersmith and S. Winograd. Matrix multiplication via arithmetic progressions. Journal of symbolic computation,
      (9):251–280, 1990.
 [38] Marcus Cramer, Martin B Plenio, Steven T Flammia, Rolando Somma, David Gross, Stephen D Bartlett, Olivier
      Landon-Cardinal, David Poulin, and Yi-Kai Liu. Efficient quantum state tomography. Nature communications, 1:149,
      2010.
 [39] Sanjoy Dasgupta, Christos H. Papadimitriou, and Umesh Vazirani. Algorithms. McGraw-Hill, Inc., New York, NY,
      USA, 2008.
 [40] M. Dehn. Über unendliche diskontinuierliche gruppen. Mathematische Annalen, 71(1):116–144, Mar 1911.
 [41] D. Deutsch and R. Jozsa. Rapid solutions of problems by quantum computation. In Proc. of the Royal Society of London
      A, pages 439–553, 1992.
 [42] Simon J Devitt, William J Munro, and Kae Nemoto. Quantum error correction for beginners. Reports on Progress in
      Physics, 76(7):076001, 2013.
 [43] B. L. Douglas and J. B. Wang. Efficient quantum circuit implementation of quantum walks. Physical Review A,
      79(5):052335, 2009.
 [44] Iain Dunning, Swati Gupta, and John Silberholz. What Works Best When? A Systematic Evaluation of Heuristics for
      Max-Cut and QUBO. INFORMS Journal on Computing, 30(3):608–624, 2018.
 [45] Christoph Dürr, Mark Heiligman, Peter Høyer, and Mehdi Mhalla. Quantum query complexity of some graph
      problems. SIAM Journal on Computing, 35(6):1310–1328, 2006.
 [46] Christoph Durr and Peter Hoyer. A quantum algorithm for finding the minimum. arXiv preprint quant-ph/9607014,
      1996.
 [47] Jack Edmonds and Richard M. Karp. Theoretical improvements in algorithmic efficiency for network flow problems.
      Journal of the ACM, 19 (2):248–264, 1972.
 [48] Nayak F. Magniez A, J. Roland, and M. Santha. Search via quantum walk. SIAM Journal on Computing, 40(1):142–164,
      2011.
 [49] Edward Farhi, Jeffrey Goldstone, and Sam Gutmann. A Quantum Approximate Optimization Algorithm Applied to a
      Bounded Occurrence Constraint Problem. arXiv e-prints, 2014. arXiv:1412.6062.
 [50] Edward Farhi, Jeffrey Goldstone, and Sam Gutmann. A quantum approximate optimization algorithm, 2014.
 [51] Edward Farhi, Jeffrey Goldstone, Sam Gutmann, and Michael Sipser. Quantum Computation by Adiabatic Evolution.
      arXiv e-prints, 2000. arXiv:quant-ph/0001106.
 [52] L. R. Ford and D. R. Fulkerson. Maximal flow through a network. Canadian Journal of Mathematics, 8:399–404, 1956.
 [53] R. Freivalds. Fast probabilistic algorithms. In Proc. of 8th Symp. on Math. Foundations of Computer Science, pages
      57–69, 1979.
 [54] Michael R. Garey and David S. Johnson. Computers and Intractability; A Guide to the Theory of NP-Completeness. W.
      H. Freeman & Co., USA, 1979.
 [55] Silvano Garnerone, Annalisa Marzuoli, and Mario Rasetti. Efficient quantum processing of 3-manifold topological
      invariants. arXiv preprint quant-ph/0703037, 2007.
 [56] Iulia M Georgescu, Sahel Ashhab, and Franco Nori. Quantum simulation. Reviews of Modern Physics, 86(1):153, 2014.
 [57] Joseph Geraci. A new connection between quantum circuits, graphs and the ising partition function. Quantum
      Information Processing, 7(5):227–242, 2008.
 [58] Joseph Geraci and Daniel A Lidar. On the exact evaluation of certain instances of the Potts partition function by
      quantum computers. Communications in Mathematical Physics, 279(3):735–768, 2008.
 [59] András Gilyén, Srinivasan Arunachalam, and Nathan Wiebe. Optimizing quantum optimization algorithms via faster
      quantum gradient computation. In ACM-SIAM Symposium on Discrete Algorithms, SODA’2019, pages 1425–1444.
 [60] Vittorio Giovannetti, Seth Lloyd, and Lorenzo Maccone. Quantum random access memory. 100:160501, 04, 2008.
 [61] Michel X. Goemans and David P. Williamson. Improved Approximation Algorithms for Maximum Cut and Satisfiability
      Problems Using Semidefinite Programming. Journal of the ACM, 42(6):1115–1145, 1995.
 [62] David Gross, Yi-Kai Liu, Steven T Flammia, Stephen Becker, and Jens Eisert. Quantum state tomography via
      compressed sensing. Physical review letters, 105(15):150401, 2010.
 [63] Lov K Grover. A fast quantum mechanical algorithm for database search. In Proceedings of the twenty-eighth annual
      ACM symposium on Theory of computing, pages 212–219. ACM, 1996.
 [64] Eran Halperin, Dror Livnat, and Uri Zwick. MAX CUT in cubic graphs. Journal of Algorithms, 53(2):169–185, 2004.
 [65] Matthew P. Harrigan et al. Quantum approximate optimization of non-planar graph problems on a planar supercon-
      ducting processor. Nature Physics, 17(3):332–336, 2021.
 [66] Aram W Harrow, Avinatan Hassidim, and Seth Lloyd. Quantum algorithm for linear systems of equations. Physical
      review letters, 103(15):150502, 2009.
 [67] Zdenek Hradil. Quantum-state estimation. Physical Review A, 55(3):R1561, 1997.
 [68] Johan Håstad. Some Optimal Inapproximability Results. Journal of the ACM, 48(4):798–859, 2001.
94                                                                                                        Abhijith J., et al.


[69] IBM Corporation. IBM Quantum Experience. Published online at https://quantumexperience.ng.bluemix.net, 2016.
     Accessed: 12/01/2017.
[70] Daniel F. V. James, Paul G. Kwiat, William J. Munro, and Andrew G. White. Measurement of qubits. Phys. Rev. A,
     64:052312, 2001.
[71] Sonika Johri, Damian S Steiger, and Matthias Troyer. Entanglement spectroscopy on a quantum computer. Physical
     Review B, 96(19):195136, 2017.
[72] Stephan Jordan. Quantum Algorithm Zoo. Published online at https://math.nist.gov/quantum/zoo/, 2011. Accessed:
     3/18/2018.
[73] Stephen P. Jordan. Fast quantum algorithms for approximating some irreducible representations of groups . pages
     1–21, 2009.
[74] Petteri Kaski. Eigenvectors and spectra of cayley graphs, 2002.
[75] J. Kempe. Quantum random walks - an introductory overview. Contemporary Physics, 44(4):307–327, 2003.
[76] V. Kendon. Where to quantum walk. pages 1–13, 2011.
[77] Subhash Khot, Guy Kindler, Elchanan Mossel, and Ryan O’Donnell. Optimal Inapproximability Results for MAX-CUT
     and Other 2-Variable CSPs? SIAM Journal on Computing, 37(1):319–357, 2007.
[78] Daphne Koller and Nir Friedman. Probabilistic graphical models: principles and techniques. Adaptive Computation
     and Machine Learning. MIT Press, 2009.
[79] M W Krentel. The complexity of optimization problems. In Proceedings of the Eighteenth Annual ACM Symposium on
     Theory of Computing, STOC ’86, pages 69–76, New York, NY, USA, 1986. ACM.
[80] Thaddeus D Ladd, Fedor Jelezko, Raymond Laflamme, Yasunobu Nakamura, Christopher Monroe, and Jeremy Lloyd
     O’Brien. Quantum computers. Nature, 464(7285):45, 2010.
[81] R. LaRose, A. Tikku, É. O’Neel-Judy, L. Cincio, and P. J. Coles. Variational quantum state diagonalization. npj Quantum
     Information, 5(1):57, 2019.
[82] R. J. Lipton and K. W. Regan. Quantum algorithms via linear algebra. 2014.
[83] Seth Lloyd, Silvano Garnerone, and Paolo Zanardi. Quantum algorithms for topological and geometric analysis of
     data. Nature Communications, 2015.
[84] Seth Lloyd, Masoud Mohseni, and Patrick Rebentrost. Quantum algorithms for supervised and unsupervised machine
     learning. arXiv preprint arXiv:1307.0411, 2013.
[85] Seth Lloyd, Masoud Mohseni, and Patrick Rebentrost. Quantum principal component analysis. Nature Physics,
     10(9):631–633, 2014.
[86] Neil B Lovett, Sally Cooper, Matthew Everitt, Matthew Trevers, and Viv Kendon. Universal quantum computation
     using the discrete-time quantum walk. Physical Review A, 81(4):042330, 2010.
[87] Frederic Magniez, Miklos Santha, and Mario Szegedy. Quantum algorithms for the triangle problem. SIAM J. Comput.,
     pages 413–424, 2007.
[88] Enrique Martin-Lopez, Anthony Laing, Thomas Lawson, Roberto Alvarez, Xiao-Qi Zhou, and Jeremy L O’brien.
     Experimental realization of shor’s quantum factoring algorithm using qubit recycling. Nature photonics, 6(11):773–776,
     2012.
[89] Jarrod R McClean, Jonathan Romero, Ryan Babbush, and Alán Aspuru-Guzik. The theory of variational hybrid
     quantum-classical algorithms. New Journal of Physics, 18(2):023023, 2016.
[90] Ashley Montanaro. Quantum algorithms: an overview. npj Quantum Information, 2:15023, 2016.
[91] Michele Mosca. Quantum algorithms. In Computational Complexity, pages 2303–2333. Springer, 2012.
[92] Michael A. Nielsen and Isaac L. Chuang. Quantum Computation and Quantum Information. Cambridge University
     Press, Cambridge, United Kingdom, 2016. 10th Anniversary Edition.
[93] Bryan O’Gorman, William J. Huggins, Eleanor G. Rieffel, and K. Birgitta Whaley. Generalized swap networks for
     near-term quantum computing. arXiv e-prints, 2019. arXiv:1905.05118.
[94] Brian Olson, Irina Hashmi, Kevin Molloy, and Amarda Shehu. Basin Hopping as a General and Versatile Optimization
     Framework for the Characterization of Biological Macromolecules. Advances in Artificial Intelligence, 2012:674832,
     2012.
[95] Karl Pearson. On lines and planes of closest fit to systems of points in space. Philosophical Magazine Series 6,
     2(11):559–572, 1901.
[96] Alberto Peruzzo, Jarrod McClean, Peter Shadbolt, Man-Hong Yung, Xiao-Qi Zhou, Peter J. Love, Alán Aspuru-Guzik,
     and Jeremy L. O’Brien. A variational eigenvalue solver on a photonic quantum processor. Nature Communications,
     5:ncomms5213, July 2014.
[97] Martin Plesch and Časlav Brukner. Quantum-state preparation with universal gate decompositions. Physical Review
     A, 83(3):032302, 2011.
[98] Martin Plesch and Časlav Brukner. Quantum-state preparation with universal gate decompositions. Phys. Rev. A,
     83:032302, 2011.
Quantum Algorithm Implementations for Beginners                                                                              95


 [99] Carl Pomerance. A tale of two sieves. Notices Amer. Math. Soc, 43:1473–1485, 1996.
[100] John Preskill. Quantum computing and the entanglement frontier. Rapporteur talk at the 25th Solvay Conference on
      Physics, 19-22 October 2011.
[101] Bo Qi, Zhibo Hou, Li Li, Daoyi Dong, Guoyong Xiang, and Guangcan Guo. Quantum state tomography via linear
      regression estimation. Scientific reports, 3, 2013.
[102] Patrick Rebentrost, Masoud Mohseni, and Seth Lloyd. Quantum support vector machine for big data classification.
      Physical review letters, 113(13):130503, 2014.
[103] E. Riefful and W. Polak. Quantum computing: A gentle introduction. 2011.
[104] R. L. Rivest, A. Shamir, and L. Adleman. A method for obtaining digital signatures and public-key cryptosystems.
      Commun. ACM, 21(2):120–126, February 1978.
[105] Mehdi Saeedi and Igor L Markov. Synthesis and optimization of reversible circuits - a survey. ACM Computing
      Surveys (CSUR), 45(2):21, 2013.
[106] Miklos Santha. Quantum walk based search algorithms. In International Conference on Theory and Applications of
      Models of Computation, pages 31–46. Springer, 2008.
[107] N. Santhi. Quantum Netlist Compiler (QNC) software repository, November 2017. Applied for LANL LACC
      authorization for unlimited open-source release, December 2017.
[108] Maria Schuld, Ilya Sinayskiy, and Francesco Petruccione. An introduction to quantum machine learning. Contemporary
      Physics, 56(2):172–185, 2015.
[109] Jiangwei Shang, Zhengyun Zhang, and Hui Khoon Ng. Superfast maximum-likelihood reconstruction for quantum
      tomography. Physical Review A, 95(6):062336, 2017.
[110] Vivek V. Shende and Igor L. Markov. On the CNOT-cost of TOFFOLI gates. Quant. Inf. Comp., 9(5-6):461–486, 2009.
[111] Vivek V Shende, Igor L Markov, and Stephen S Bullock. Minimal universal two-qubit controlled-not-based circuits.
      Physical Review A, 69(6):062321, 2004.
[112] Neil Shenvi, Julia Kempe, and K Birgitta Whaley. Quantum random-walk search algorithm. Physical Review A,
      67(5):052307, 2003.
[113] Peter W Shor. Algorithms for quantum computation: Discrete logarithms and factoring. In Foundations of Computer
      Science, 1994 Proceedings., 35th Annual Symposium on, pages 124–134. IEEE, 1994.
[114] Peter W. Shor. Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer.
      SIAM Journal on Computing, 26(5):1484–1509, 1997.
[115] Nikolai A Sinitsyn. Computing with a single qubit faster than the computation quantum speed limit. Physics Letters
      A, 382(7):477–481, 2018.
[116] Robert S. Smith, Michael J. Curtis, and William J. Zeng. A practical quantum instruction set architecture, 2016.
[117] John A Smolin, Jay M Gambetta, and Graeme Smith. Efficient method for computing the maximum-likelihood
      quantum state from measurements with additive gaussian noise. Physical review letters, 108(7):070502, 2012.
[118] Rolando D Somma. Quantum simulations of one dimensional quantum systems. Quantum Information & Computation,
      16(13-14):1125–1168, 2016.
[119] Robert Spalek et al. Quantum algorithms, lower bounds, and time-space tradeoffs. ILLC,Amsterdam, 2006.
[120] V. Strassen. Gaussian elimination is not optimal. Numerische Mathematik, (13):354–356, 1969.
[121] Yiğit Subaşı, Rolando D Somma, and Davide Orsucci. Quantum algorithms for systems of linear equations inspired
      by adiabatic quantum computing. Physical review letters, 122(6):060504, 2019.
[122] J. A. K. Suykens and J. Vandewalle. Least squares support vector machine classifiers. Neural Process. Lett., 9(3):293–300,
      June 1999.
[123] Mario Szegedy. Quantum speed-up of markov chain based algorithms. In 45th Annual IEEE symposium on foundations
      of computer science, pages 32–41. IEEE, 2004.
[124] Maika Takita, Antonio D Córcoles, Easwar Magesan, Baleegh Abdo, Markus Brink, Andrew Cross, Jerry M Chow,
      and Jay M Gambetta. Demonstration of weight-four parity measurements in the surface code architecture. Physical
      review letters, 117(21):210505, 2016.
[125] IBM QX Team. IBM Q experience backend information. http://github.com/QISKit/ibmqx-backend-information, 2017.
      Last accessed: 12 December, 2017.
[126] Giacomo Torlai, Guglielmo Mazzola, Juan Carrasquilla, Matthias Troyer, Roger Melko, and Giuseppe Carleo. Neural-
      network quantum state tomography. Nature Physics, 14(5):447, 2018.
[127] L. M. K. Vandersypen, M. Steffen, G. Breyta, C. S. Yannoni, M. H. Sherwood, and I. L. Chuang. Experimental realization
      of Shor’s quantum factoring algorithm using nuclear magnetic resonance. Nature, 414:883–887, December 2001.
[128] Guifré Vidal. Efficient classical simulation of slightly entangled quantum computations. Physical review letters,
      91(14):147902, 2003.
[129] Zhihui Wang, Stuart Hadfield, Zhang Jiang, and Eleanor G. Rieffel. Quantum approximate optimization algorithm for
      MaxCut: A fermionic view. Physical Review A, 97:022304, 2018.
96                                                                                                     Abhijith J., et al.


[130] Zhihui Wang, Nicholas C. Rubin, Jason M. Dominy, and Eleanor G. Rieffel. 𝑋𝑌 mixers: Analytical and numerical
      results for the quantum alternating operator ansatz. Physical Review A, 101(1):012320, 2020.
[131] Chu Ryang Wie. A quantum circuit to construct all maximal cliques using Grover’s search algorithm. pages 1–13,
      2017.
[132] James R Wootton. Demonstrating non-abelian braiding of surface code defects in a five qubit experiment. Quantum
      Science and Technology, 2(1):015006, 2017.
[133] James R Wootton. Benchmarking near-term devices with quantum error correction. Quantum Sci. Technol., 5(4):044004,
      2020.
[134] James R Wootton and Daniel Loss. Repetition code of 15 qubits. Physical Review A, 97(5):052313, 2018.
[135] Zhi-Cheng Yang, Armin Rahmani, Alireza Shabani, Hartmut Neven, and Claudio Chamon. Optimizing Variational
      Quantum Algorithms Using Pontryagin’s Minimum Principle. Physical Review X, 7(2):021027, 2017.
[136] N. S. Yonofsky and M. A. Mannucci. Quantum computing for computer scientists. 2008.
[137] Yarui Zheng, Chao Song, Ming-Cheng Chen, Benxiang Xia, Wuxin Liu, Qiujiang Guo, Libo Zhang, Da Xu, Hui Deng,
      Keqiang Huang, et al. Solving systems of linear equations with a superconducting quantum processor. Physical
      Review Letters, 118(21):210504, 2017.
[138] Leo Zhou, Sheng-Tao Wang, Soonwon Choi, Hannes Pichler, and Mikhail D Lukin. Quantum Approximate Op-
      timization Algorithm: Performance, Mechanism, and Implementation on Near-Term Devices. Physical Review X,
      10(2):021067, 2020.

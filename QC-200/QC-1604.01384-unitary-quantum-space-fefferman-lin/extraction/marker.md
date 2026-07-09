# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.28.0
# Paper: arXiv:1604.01384 — Fefferman & Lin, 'A Complete Characterization of Unitary Quantum Space'
# Rationale: Marker CLI not installed locally or on paired hosts (uicgpu, m1); PyMuPDF layout-
# preserving text extraction is the labeled zero-dependency surrogate used by sibling QC-200
# replications (see e.g. QC-1611.05543-sparse-markovian-quantum-dynamics-childs).
# For the ground-truth text stream this replication actually reads, see work/paper.txt
# (pdftotext -layout).


<!-- ==== page 1 ==== -->
arXiv:1604.01384v2  [quant-ph]  21 Nov 2016
A Complete Characterization of Unitary Quantum Space
Bill Feﬀerman∗1 and Cedric Yen-Yu Lin†1
1Joint Center for Quantum Information and Computer Science (QuICS), University of
Maryland
November 22, 2016
Abstract
Motivated by understanding the power of quantum computation with restricted number of
qubits, we give two complete characterizations of unitary quantum space bounded computation.
First we show that approximating an element of the inverse of a well-conditioned eﬃciently
encoded 2k(n) × 2k(n) matrix is complete for the class of problems solvable by quantum circuits
acting on O(k(n)) qubits with all measurements at the end of the computation.
Similarly,
estimating the minimum eigenvalue of an eﬃciently encoded Hermitian 2k(n)×2k(n) matrix is also
complete for this class. In the logspace case, our results improve on previous results of Ta-Shma
[32] by giving new space-eﬃcient quantum algorithms that avoid intermediate measurements,
as well as showing matching hardness results.
Additionally, as a consequence we show that PreciseQMA, the version of QMA with exponen-
tially small completeness-soundess gap, is equal to PSPACE. Thus, the problem of estimating the
minimum eigenvalue of a local Hamiltonian to inverse exponential precision is PSPACE-complete,
which we show holds even in the frustration-free case. Finally, we can use this characterization
to give a provable setting in which the ability to prepare the ground state of a local Hamiltonian
is more powerful than the ability to prepare PEPS states.
Interestingly, by suitably changing the parameterization of either of these problems we can
completely characterize the power of quantum computation with simultaneously bounded time
and space.
∗wjf@umd.edu
†cedricl@umiacs.umd.edu


<!-- ==== page 2 ==== -->
1
Introduction
How powerful is quantum computation with a restricted number of qubits? In this work we will
study unitary quantum space-bounded classes - those problems solvable using a given amount
of (quantum and classical) space, with all quantum measurements performed at the end of the
computation. We give two sets of complete problems for these classes; to the best of our knowledge,
these are the ﬁrst natural complete problems proposed for quantum space-bounded classes.
The ﬁrst problem we consider, the k(n)-Well-conditioned Matrix Inversion problem, is a well-
conditioned version of the ubiquitous matrix inversion problem. The second problem we consider,
the k(n)-Minimum Eigenvalue problem, asks us to compute the minimum eigenvalue of a Hermitian
matrix to high precision – in the context of quantum complexity, this is a natural generalization of
the familiar local Hamiltonian problem [25]. Interestingly enough, the ﬁrst (resp. second) problem
is the space-bounded variant of a BQP-complete [20] (resp. QMA-complete [25]) problem; their
complexities coincide in the space-bounded regime. For the sake of readability, we defer precise
deﬁnitions of these problems and statements of our results until Sections 3 and 4.
We now proceed to give some justiﬁcation for the importance of our results. In the following
discussion, BQUSPACE[k(n)] refers to the class of problems solvable with bounded error by a
quantum algorithm running in O(k(n)); the subscript U indicates that the algorithm is unitary,
i.e. employs no intermediate measurements.
1.1
Background and Motivation
The Matrix Inversion problem is of central importance in computational complexity theory. Ma-
trix inversion is known to be complete for DET, the class of functions as hard as computing the
determinant of an integer matrix, which can be solved in classical O(log2(n)) space [6, 13]. It is a
major open problem to determine if Matrix Inversion can be solved in classical logarithmic space,
which would imply L = NL = DET.
Recently, Ta-Shma [32], building on work of Harrow, Hassidim, and Lloyd [20], showed that a
well-conditioned n×n matrix can be inverted (up to 1/ poly(n) error) by a quantum O(log n) space
algorithm using intermediate measurements. Similarly, Ta-Shma also gives an algorithm for com-
puting eigenvalues of a Hermitian matrix with similar space. These algorithms achieve a quadratic
advantage in space over the best known classical algorithms, which require Ω(log2 n) space. This is
the maximum quantum advantage possible, since Watrous has shown BQSPACE[k(n)] ⊆SPACE[O(k(n)2)]
[37, 38] even for quantum algorithms with intermediate measurements.
Our completeness result for matrix inversion, along with observing our algorithm for matrix
inversion (Theorem 15) actually gives a high-precision approximation, gives the following corollary
in the logspace case (see Remark 11).
Corollary 1. The problem of approximating, to constant precision, an entry of the inverse of an
n × n positive semideﬁnite matrix with condition number at most poly(n) is BQUL-complete under
L-reductions, where BQUL is the set of problems solvable in unitary quantum logspace. This problem
remains in BQUL even if 1/ poly(n) precision is required.
Similarly, restricting Thereom 4 to the logspace case gives the following corollary.
Corollary 2. The problem of approximating, to 1/ poly(n) precision, the minimum eigenvalue of
an n × n positive semideﬁnite matrix is BQUL-complete under L-reductions.
These corollaries improve upon Ta-Shma’s results [32] in two ways. First, our algorithms solve
these problems without needing intermediate measurements. Unlike in time complexity, where the
1


<!-- ==== page 3 ==== -->
“Principle of safe storage” gives a time-eﬃcient procedure to defer intermediate measurements,
these methods may incur an exponential blow-up in space.
One might wonder why we care so much about avoiding intermediate measurements.
The
main reason is that removing intermediate measurements from the computation allows us to give
matching hardness results, showing the optimality of our algorithms. This is the second way our
results improve on those of Ta-Shma. In particular, our proofs crucially use space-eﬃcient methods
for the ampliﬁcation of unitary quantum computations, which are not known in the non-unitary
model. This is because the techniques require applying the inverse of the circuit, which of course
is impossible if the circuit contains intermediate measurements. We will also rely on ideas from
Kitaev’s clock construction, which constructs a local Hamiltonian from a unitary quantum circuit.
Speciﬁcally, we will show that the problems of inverting well-conditioned matrices and com-
puting minimum eigenvalues of Hermitian matrices are hard for unitary quantum logspace under
L-reductions. In the case of our algorithm for Matrix Inversion, this means that the upper bound
on the condition number bound is unlikely to be improved upon. Likewise, this gives some of the
strongest evidence that even well-conditioned matrices cannot be inverted in deterministic logspace,
since otherwise our results would immediately imply L = BQUL, which seems quite unlikely.
Interestingly, although our algorithms for both problems use diﬀerent techniques from those
of Ta-Shma, our algorithm for computing the minimum eigenvalue is completely diﬀerent.
In
particular, our algorithm crucially relies on new methods for space eﬃcient QMA ampliﬁcation,
together with some of the most powerful recent results in Hamiltonian simulation [7, 9].
Concurrently with our work, Doron, Sarid, and Ta-Shma have shown that analogous problems
for stochastic matrices (e.g. computing the eigenvalue gap) are complete for classical randomized
logspace, or BPL [16, 15]. In addition, Le Gall has shown that analogous problems for Laplacian
matrices can be solved in BPL [18]. Since it is straightforward to see that Well-conditioned Matrix
Inversion reduces to Integer Matrix Inversion, we obtain a direct proof that BQUL ⊆DET, which
was previously known indirectly via the containments BQUL ⊆PL ⊆DET [38, 10].
Therefore the power of classical and quantum space-bounded classes are characterized by the
ability to approximate solutions of diﬀerent problems in DET (stochastic matrices for the former,
and Hermitian matrices for the latter). This could shed light on the diﬀerences between determin-
istic, randomized, and quantum space complexity. An open question is to ﬁnd a class of interesting
matrices whose inverse (or eigenvalues) can be computed in deterministic logspace.
Interestingly, if we change the scaling of the parameters in our Matrix Inversion and Minimum
Eigenvalue problems suitably, then we obtain problems that are known to be complete for BQP
[20] and QMA [25, 2]. Thus by appropriately bounding the dimension of the matrix and either the
condition number or the promise gap, we can give problems complete for quantum time or quantum
space. In fact we can strengthen these results to settings with a simultaneously bounded amount
of space and time; see Section 5.
1.2
Relationship with Matchgates
Matchgates are a subclass of quantum gates introduced by Valiant [34], who also showed that
nearest neighbor matchgate circuits (which we will just call matchgate computations) are classically
simulable. Matchgate computations were further shown to be equivalent to a one-dimensional model
of noninteracting fermions by Terhal and DiVincenzo [33]; and equivalent to unitary quantum
logspace by Jozsa, Kraus, Miyake, and Watrous [22]. Our complete problems therefore elucidate
the computational power of noninteracting fermions.
We know that sampling from output distributions of matchgate computations gives us the power
of BPL; but what is the computational power of computing exactly the output probabilities of
2


<!-- ==== page 4 ==== -->
matchgate computations? We conjecture that this computational power corresponds to DET, since
amplitudes of noninteracting fermion circuits are related to determinants (and see also the discussion
in the previous subsection). It is known that output probabilities of matchgate computations can
be exactly calculated by an eﬃcient classical algorithm [23], which is consistent with our conjecture
because DET ∈P.
1.3
Quantum Merlin-Arthur with Small Gap
A consequence of our proof of completeness for the k(n)-Minimum Eigenvalue problem is an equiv-
alence between space-bounded quantum computations and quantum Merlin-Arthur proof systems.
Here we give this equivalence for the polynomial space case: let PreciseQMA be the variant of QMA
with exponentially small completeness-soundness gap. Then we show the following:
Corollary 3. PreciseQMA = BQUPSPACE = PSPACE.
The second equality is due to Watrous [37, 38]. We give similar equivalences for space-bounded
quantum computations with and without a witness for other space bounds as well (Theorem 19).
We note that PreciseQMA is likely far more powerful than its classical counterpart. The anal-
ogous classical complexity class is contained in NPPP: given a classical witness, the veriﬁer runs a
classical computation that in the YES case accepts with probability at least c, or in the NO case
accepts with probability at most s, where c > s. Note that in the classical case c−s > exp(−poly)
is automatically satisﬁed. Since NPPP is in the counting hierarchy, the entirety of which is con-
tained in PSPACE (see e.g., [3]), we see that the quantum proof protocol is strictly stronger than
the classical one, unless the counting hierarchy collapses to the second level.
We also show that the local Hamiltonian problem is PSPACE-complete when the promise gap
is exponentially small (for details see Appendix G). This is in contrast to the usual case when
the gap is polynomially small, where the problem is QMA-complete. Perhaps more surprisingly,
PreciseQMA = PSPACE is more powerful than PostBQP = PP, the class of problems solvable with
postselected quantum computation [1].
Another consequence concerns Projected Entangled Pair States, or PEPS, a natural extension
of matrix product states to two and higher spatial dimensions, which can be described as the ground
state of certain frustration-free local Hamiltonians [36]. A characterization of the computational
power of PEPS was given in [30], and can be summarized as follows: let OP EP S be a quantum
oracle that, given the description of a PEPS, outputs the PEPS (so the output is quantum). Then
BQPOP EP S
∥,classical = PostBQP = PP, where (following Aaronson [1]) the subscript denotes that only
classical nonadaptive queries to the oracle are allowed. Moreover, let PQP stand for the set of
problems solvable by a quantum computer with unbounded error; then it can be straightforwardly
shown that PQPOP EP S
∥,classical = PP as well (see Appendix I).
On the other hand, suppose we have an oracle OLH that given the description of a local Hamil-
tonian, outputs a ground state of the Hamiltonian. Then our results show that PreciseQMA =
PSPACE ⊆PQPOLH
∥,classical. This shows that in the setting of unbounded-error quantum computation,
PEPS do not capture the full computational complexity of general local Hamiltonian ground states
unless PP = PSPACE. We leave open the problem of determining the complexity of BQPOLH
∥,classical.
Lastly, we are able to strengthen our characterization to show that PreciseQMA contains PSPACE
(see Appendix F), even when restricted to having perfect completeness. This allows us to prove
that testing if a local Hamiltonian is frustration-free is a PSPACE-complete problem (Appendix
G). We note that if the local Hamiltonian is promised to have a ground state energy of at least
1/ poly if it is frustrated, then this is the Quantum Satisﬁability problem deﬁned by Bravyi, which
3


<!-- ==== page 5 ==== -->
is known to be QMA1 complete [11, 19]. Our results show that if the promise gap is removed then
we instead get PSPACE-completeness.
2
Preliminaries
2.1
Quantum circuits
We will assume a working knowledge of quantum information. For an introduction, see [28].
A quantum circuit consists of a series of quantum gates each taken from some universal gateset,
such as the gateset consisting of Hadamard and Toﬀoli gates [31]. For functions f, g : N →N, we
say a family of quantum circuits {Qx}x∈{0,1}∗is f-time g-space uniformly generated if there exists
a deterministic classical Turing machine that on input x ∈{0, 1}n and i > 0 outputs the i-th gate
of Qx within time f(n) and workspace g(n) [28].
Our restriction to a speciﬁc gateset is without loss of generality, even for logarithmic space
algorithms: there exists a deterministic algorithm that given any unitary quantum gate U and a
parameter ǫ, outputs a sequence of at most polylog(1/ǫ) gates from any universal quantum gateset
that approximates U to precision ǫ in space O(log(1/ǫ)) and time polylog(1/ǫ) [35]. This improves
the Solovay-Kitaev theorem, which guarantees a space bound of polylog(1/ǫ); see e.g., [28].
2.2
Space-bounded computation
For our model of unitary quantum space-bounded computation, we consider a quantum system
with purely classical control, because there are no intermediate quantum measurements to condition
future operations on. Speciﬁcally, we use the following deﬁnition (see Appendix A for more details):
Deﬁnition 4. Let k(n) be a function satisfying Ω(log(n)) ≤k(n) ≤poly(n). A promise problem
L = (Lyes, Lno) is in QUSPACE[k(n)](c, s) if there exists a poly(|x|)-time O(k)-space uniformly
generated family of quantum circuits {Qx}x∈{0,1}∗, where each circuit Qx = Ux,TUx,T−1 · · · Ux,1 has
T = 2O(k) gates, and acts on O(k(|x|)) qubits, such that:
If x ∈Lyes:
D
0kQ†
x|1⟩⟨1|outQx
0kE
≥c.
(1)
Whereas if x ∈Lno:
D
0kQ†
x|1⟩⟨1|outQx
0kE
≤s.
(2)
Here out denotes a single qubit we measure at the end of the computation; no intermediate measure-
ments are allowed. Furthermore, we require c and s to be computable in classical O(k(n))-space.
For the rest of the paper we will always assume that Ω(log(n)) ≤k(n) ≤poly(n).
The bound T = 2O(k) on the circuit size comes from that any classical Turing machine generating
Qx using space O(k(|x|)) has at most 2O(k) conﬁgurations. We note that 2O(k) gates suﬃce to
approximate any gate on O(k) qubits to high accuracy (see e.g. [28, Chapter 4]). The poly(|x|)
time bound on the classical control can be assumed without loss of generality; see Appendix A.
Deﬁnition 5. BQUSPACE[k] = QUSPACE[k](2/3, 1/3).
Theorem 6 (Watrous [37, 38]). BQUSPACE[poly] = PSPACE.
We now deﬁne space- and time-bounded analogues of QMA:
4


<!-- ==== page 6 ==== -->
Deﬁnition 7. We say a promise problem L = (Lyes, Lno) is in (t, k)-bounded QMAm(c, s) if there
exists a t-time and (k+m)-space uniformly generated family of quantum circuits {Vx}x∈{0,1}∗, each
of size at most t(|x|), acting on k(|x|) + m(|x|) qubits, so that:
If x ∈Lyes there exists an m-qubit state |ψ⟩such that:

⟨ψ| ⊗
D
0k

V †
x |1⟩⟨1|outVx

|ψ⟩⊗
0kE
≥c.
(3)
Whereas if x ∈Lno, for all m-qubit states |ψ⟩we have:

⟨ψ| ⊗
D
0k

V †
x |1⟩⟨1|outVx

|ψ⟩⊗
0kE
≤s.
(4)
out denotes a single qubit measured at the end of the computation; no intermediate measurements
are allowed. Here c and s are computable in classical O(t(n))-time and O(k(n) + m(n))-space.
Deﬁnition 8. QMA = (poly, poly)-bounded QMApoly(2/3, 1/3).
Deﬁnition 9. PreciseQMA = S
c∈(0,1] (poly, poly)-bounded QMApoly(c, c −2−poly).
2.3
Other deﬁnitions and results
We use the following deﬁnition of eﬃcient encodings of matrices:
Deﬁnition 10. Let M be a 2k ×2k matrix, and A be a classical algorithm (e.g. a Turing machine)
speciﬁed using n bits. We say that A is an eﬃcient encoding of M if on input i ∈{0, 1}k, A
outputs the indices and contents of the non-zero entries of the i-th row, using at most poly(n) time
and O(k) workspace (not including the output size). Note that as a consequence M has at most
poly(n) nonzero entries in each row.
We will often specify a matrix M in the input by giving an eﬃcient encoding of M. The size of
the encoding is then the input size, which we will usually indicate by n.
Remark 11. It is not diﬃcult to see that any n × n matrix has an eﬃcient encoding of size O(n),
since it is straightforward to construct a classical O(log n)-size circuit that on input i, j outputs
the (i, j)-entry of the matrix.
In our results we will implicitly assume the existence of algorithms that compute some common
functions on n-bit numbers, such as sin, cos, arcsin, arccos and exponentiation, to within 1/ poly(n)
accuracy in classical O(log n) space. Algorithms for these tasks have been designed by Reif [29].1
Finally, we will need new results from the Hamiltonian simulation literature:
Theorem 12 ([7, 8, 9]). Given as input is the size-n eﬃcient encoding of a 2k(n) ×2k(n) Hermitian
matrix H. Then treated as a Hamiltonian, the time evolution exp(−iHt) can be simulated using
poly(n, k, ∥H∥max, t, log(1/ǫ)) operations and O(k + log(t/ǫ)) space.
While the space complexity was not explicitly stated in [7, 8, 9], it can be seen from the analysis
(see e.g. [8]). The crucial thing to notice in Theorem 12 is the polylogarithmic scaling in the error
ǫ; this implies that we can obtain polynomial precision in exp(−iHt) using only polynomially many
operations. Also note that the maximum eigenvalue of H, ∥H∥, satisﬁes ∥H∥≤poly(n)∥H∥max.
1Reif’s algorithms take only O(log log n log log log n) space, but for simplicity we only use the O(log n) bound.
5


<!-- ==== page 7 ==== -->
3
The Well-Conditioned Matrix Inversion Problem
We begin with a formal statement of the problem:
Deﬁnition 13 (k(n)-Well-conditioned Matrix Inversion). Given as input is the size-n eﬃcient
encoding of a 2k(n) × 2k(n) positive semideﬁnite matrix H with a known upper bound κ = 2O(k(n))
on the condition number, so that κ−1I ⪯H ⪯I, and s, t ∈{0, 1}k(n). It is promised that either
|H−1(s, t)| ≥b or |H−1(s, t)| ≤a for some constants 0 ≤a < b ≤1; determine which is the case.
Theorem 14. For Ω(log(n)) ≤k(n) ≤poly(n), O(k(n))-Well-conditioned Matrix Inversion is
complete for BQUSPACE[O(k(n))] under classical reductions using poly(n) time and O(k(n)) space.
Proof. We begin by giving a new space eﬃcient algorithm for this matrix inversion problem:
Theorem 15. Fix functions k(n), κ(n), and ǫ(n). Suppose we are given the size-n eﬃcient en-
coding of a 2k(n) × 2k(n) PSD matrix H such that κ−1I ⪯H ⪯I. We are also given poly(n)-time
O(k + log(κ/ǫ))-space uniform quantum circuits Ua and Ub acting on k qubits and using at most
T gates. Let Ua|0⟩⊗k(n) = |a⟩and Ub|0⟩⊗k(n) = |b⟩. The following tasks can be performed with
poly(n)-time O(k + log(κ/ǫ))-space uniformly generated quantum circuits with poly(T, k, κ, 1/ǫ)
gates and O(k + log(κ/ǫ)) qubits:
1. With at least constant probability, output an approximation of the quantum state H−1|b⟩/∥H−1|b⟩∥
up to error ǫ.
2. Approximate ∥H−1|b⟩∥to precision ǫ.
3. Approximate |⟨a|H−1|b⟩| to precision ǫ.
These circuits do not require intermediate measurements.
In fact our algorithm is much stronger: to solve k(n)-Well-conditioned Matrix Inversion we
merely need to approximate |⟨s|H−1|t⟩| to constant precision, while Theorem 15 actually gives an
approximation to precision 2−O(k) in O(k(n)) unitary quantum space. Moreover our algorithm does
not require s and t to be computational basis states.
We note that we can modify our deﬁnition of unitary quantum space-bounded classes to include
computing functions, for instance by adding a write-only one-way output tape of qubits to the
Turing machine (see the discussion in Appendix A), that are all measured at the very end of the
computation. The error reduction result (Corollary 33) later in our work allows the total error to
be reasonably controlled. With such a modiﬁcation we can compute the whole matrix inverse in
unitary quantum logspace. We will not pursue this modiﬁed model further in this work.
Proof. We ﬁrst brieﬂy summarize the algorithm of Ta-Shma [32], which is based on the linear sys-
tems solver of Harrow, Hassidim and Lloyd [20]. Ta-Shma shows that an n×n matrix with condition
number at most poly(n) can be inverted by a quantum logspace algorithm with intermediate mea-
surements; in our language this corresponds to solving O(log n)-Well-conditioned Matrix Inversion.
Our algorithm and Ta-Shma’s share the same initial procedure. In particular it is shown:
Lemma 16 (Implicit in [20, 32]). There is a poly-time O(k + log(κ/ǫ′))-space uniform quantum
unitary transformation WH over k +ℓ= O(k +log(κ/ǫ′)) qubits and using poly(k, κ/ǫ′) gates, such
that for any k-qubit input state |b⟩,
WH(|0⟩⊗ℓ⊗|b⟩) = α|0⟩out ⊗|ψb⟩+
p
1 −α2|1⟩out ⊗
ψ′
b
,
(5)
where |ψb⟩and |ψ′
b⟩are normalized states such that ∥|ψb⟩−|0⟩⊗ℓ−1 ⊗
H−1|b⟩
∥H−1|b⟩∥∥≤ǫ′, α is a positive
number satisfying |α −∥H−1|b⟩∥
κ
| ≤ǫ′, and “out” is a 1-qubit register.
6


<!-- ==== page 8 ==== -->
This lemma can be obtained by combining the Hamiltonian simulation algorithms of Berry et
al. (Theorem 12) with the analysis of Harrow, Hassidim and Lloyd [20]; a version without the time
bound is implicit in the proof of [32, Theorem 6.3]. For completeness, we sketch the proof below.
Proof sketch. Decompose |b⟩into the eigenbasis of H: |b⟩= P
λ aλ|vλ⟩, where λ are eigenvalues of
H and H|vλ⟩= λ|vλ⟩. The following procedure satisﬁes Lemma 16 (all steps are approximate):
1. Perform phase estimation on the operator exp(iH) and state |b⟩to compute the eigenvalues
of H into an ancilliary register, obtaining the state P
λ aλ|vλ⟩|λ⟩.
2. Implement the unitary transformation |λ⟩|0⟩→|λ⟩[(κλ)−1|0⟩+ (
p
1 −(κλ)−2|1⟩], to obtain
the state P
λ aλ|vλ⟩|λ⟩[(κλ)−1|0⟩+ (
p
1 −(κλ)−2|1⟩].
3. Uncompute the eigenvalues λ by running phase estimation in reverse, obtaining the state
P
λ aλ|vλ⟩|0⟩ℓ−1[(κλ)−1|0⟩+(
p
1 −(κλ)−2|1⟩]. Note that P
λ aλ|vλ⟩|0⟩ℓ−1(κλ)−1|0⟩= 1
κH−1|b⟩.
An appropriate error analysis of this procedure is the technical bulk of the proof; we refer the
reader to [20]. For Step 1, Ta-Shma showed how to implement exp(iH) in O(k + log(1/ǫ)) space
[32, Theorem 4.1] (their proof works for general matrices with eﬃcient encodings); recent sparse
Hamiltonian simulation algorithms (Theorem 12) give a time eﬃcient way to do this.
Intuitively, Lemma 16 gives a space-eﬃcient quantum algorithm that produces a state propor-
tional to H−1|b⟩with probability at least 1/κ. Our goal is to produce amplify the probability
from 1/κ to a constant, to produce a state with constant overlap to the state |0⟩out ⊗|ψb⟩together
with an estimate for α ≈∥H−1|b⟩∥. From here our algorithm diﬀers from Ta-Shma’s and uses a
combination of amplitude ampliﬁcation and phase estimation. This sidesteps both the somewhat
involved analysis and intermediate measurements of Ta-Shma’s algorithm.
Speciﬁcally, consider the two projectors
Π0 = |0⟩⟨0|⊗ℓ⊗|b⟩⟨b|,
Π1 = W †
H(|0⟩⟨0|out ⊗I)WH.
(6)
Π0 projects onto the initial subspace, while Π1 projects onto the initial states that would be accepted
by the ﬁnal measurement. The rotation R = −(I −2Π1)(I −2Π0) has eigenvalues e±i2 sin−1 α with
eigenvectors |ψ+⟩, such that |0⟩⊗ℓ⊗|b⟩= (|ψ+⟩+ |ψ−⟩)/
√
2 is a uniform superposition of the two
eigenvectors. Therefore phase estimation on the operator R and input state |0⟩⊗ℓ⊗|b⟩suﬃces
to give an estimate of α. Furthermore both eigenvectors have constant overlap with W †
H|ψb⟩, so
applying WH to the residual state of phase estimation allows us to complete the ﬁrst task as well.
We have addressed the ﬁrst two tasks in Theorem 15.
For the third task (approximating
|⟨a|H−1|b⟩|), we can choose Π′
1 = W †
H(|0⟩⟨0|out ⊗I)(Ianc ⊗|a⟩⟨a|)(|0⟩⟨0|out ⊗I)WH instead, and
phase estimation on R = −(I −2Π1)(I −2Π′
0) will give an estimate for |⟨a|H−1|b⟩|. See Appendix
B for the full proof.
We establish that k(n)-Well-conditioned Matrix Inversion is BQUSPACE[O(k)]-hard using a
similar argument to Harrow, Hassidim, and Lloyd [20], in which given a quantum circuit acting on
k(n) qubits we construct a eﬃciently encoded well-conditioned 2O(k) × 2O(k) matrix H, so that a
single element of H−1 is proportional to the success probability of the circuit. See Appendix C.
7


<!-- ==== page 9 ==== -->
4
The Minimum Eigenvalue Problem
Our second characterization of unitary quantum space is based on the following problem:
Deﬁnition 17 (k(n)-Minimum Eigenvalue problem). Given as input is the size-n eﬃcient encoding
of a 2k(n) × 2k(n) PSD matrix H, such that ∥H∥max = maxs,t |H(s, t)| is at most a constant. Let
λmin be the minimum eigenvalue of H. It is promised that either λmin ≤a or λmin ≥b, where a(n)
and b(n) are numbers such that b −a > 2−O(k(n)). Output 1 if λmin ≤a, and output 0 otherwise.
Theorem 18. For Ω(log(n)) ≤k(n) ≤poly(n), O(k(n))-Minimum Eigenvalue is complete for
BQUSPACE[O(k(n))] under classical reductions using poly(n) time and O(k(n)) space.
In the process of proving this result, we will also show the following equivalence:
Theorem 19. BQUSPACE[O(k(n))] is equivalent to the class of problems characterized by having
quantum Merlin Arthur proof systems running in polynomial time, O(k(n)) witness size and space,
and 2−O(k(n)) completeness-soundness gap. Or in other words,
BQUSPACE[O(k(n))] =
[
c−s≥2−O(k(n))
(poly, O(k(n)))-bounded QMAO(k(n))(c, s)
Our proof will consist of three steps.
Lemma 20 will show that k(n)-Minimum Eigenvalue
is in the generalized PreciseQMA class deﬁned in Theorem 19.
Lemma 21 will show that this
generalized PreciseQMA class is contained in BQUSPACE[k(n)]. Finally, Lemma 22 will show that
BQUSPACE[k(n)]-hardness of k(n)-Minimum Eigenvalue.
Lemma 20. k(n)-Minimum Eigenvalue is contained in (poly, O(k(n)))-bounded QMAO(k(n))(c, s)
for some c, s such that c −s > 2−O(k(n)).
Proof. We are given the size-n eﬃcient encoding of a 2k(n)×2k(n) PSD matrix H, and it is promised
that the smallest eigenvalue λmin of H is either at most a or at least b. Merlin would like to convince
us that λmin ≤a; he will send us a purported k-qubit eigenstate |ψ⟩of H with eigenvalue λmin.
Choose t = π/(poly(n)∥H∥max) ≤π/∥H∥; then all eigenvalues of Ht lie in the range [0, π], and
the output of phase estimation on exp(−iHt) will be unambiguous.
We perform, on ψ, phase
estimation of exp(−iHt) with one bit of precision:
|0⟩
H
•
H
1+e−iλt
2
|0⟩+ 1−e−iλt
2
|1⟩
|ψ⟩
e−iHt
|ψ⟩
(7)
Here the H gates on the ﬁrst qubit are Hadamard gates (and have nothing to do with the matrix
H). Theorem 12 gives an implementation of exp(−iHt) up to error ǫ = 2−Θ(k(n)) using poly(n)
operations and O(k(n)) space.
In Circuit (7) we’ve assumed |ψ⟩is an eigenstate of H with eigenvalue λ. If we measure the
control qubit at the end, the probability we obtain 0 is (1+cos(λt))/2. Therefore if ψ is a eigenstate
with eigenvalue at most a, we can verify this with probability at least c = (1+cos(at))/2−ǫ, where ǫ
is the error in the implementation of exp(−iHt). Otherwise if λmin ≥b, no state ψ will be accepted
with probability more than s = (1 + cos(bt))/2 + ǫ. The separation between c and s is at least
(cos(at) −cos(bt)) −2ǫ = 2 sin
(a + b)t
2

sin
(b −a)t
2

−2ǫ ≥2−O(k)
(8)
since sin x = Ω(x) for x ∈[0, 1], (a+b)t ≥(b−a)t = 2−O(k(n)), as long as we choose ǫ = 2−Θ(k(n)) to
be suﬃciently small enough. This therefore gives a (poly, Θ(k(n)))-bounded QMAΘ(k)(c, s) protocol
for c −s = 2−O(k(n)), as desired.
8


<!-- ==== page 10 ==== -->
Lemma 21. S
c−s≥2−O(k) (poly, O(k))-bounded QMAO(k)(c, s) ⊆BQUSPACE[k(n)].
Proof sketch. We only give a high level overview of the proof here; for the complete proof see
Appendix D. The core of the proof is to develop and use new space-eﬃcient QMA error reduction
procedures. Our procedures are based on the “in-place” QMA ampliﬁcation procedure of Marriott
and Watrous [26], which allows the error in a QMA proof system to be reduced without requiring
additional copies of the witness state. This was improved by Nagaj, Wocjan, and Zhang [27], whose
phase-estimation based procedure reduces the error to 2−r using only O

r log
1
c−s

additional qubits
and O(r/(c −s)) repetitions of the circuit and its inverse. We derive a procedure (Lemma 32) that
gives the same error bounds while using only O

r + log
1
c−s

additional qubits, but still using only
O(r/(c−s)) repetitions of the circuit; the improved space bound will be required for our purposes2.
Thus we can amplify the gap in our QMA protocols to still use O(k) space, but with completeness
1 −2−O(k) and soundness 2−O(k). We can now replace the witness by the completely mixed state
(or alternatively half of many EPR pairs), which gives us a computation with no witness such
that the resulting completeness and soundness are both exponentially small, but are still separated
by 2−O(k). Finally, we can once again apply our space-eﬃcient ampliﬁcation procedure to this
witness-free protocol, obtaining a computation in BQUSPACE[O(k)].
Lemma 22. O(k(n))-Minimum Eigenvalue is BQUSPACE[k(n)]-hard under classical poly-time
O(k(n))-space reductions.
Proof sketch. Again we only give an overview; see Appendix E for the full proof. Recall that our uni-
formity condition on k(n)-Minimum Eigenvalue implies that every language in k(n)-Minimum Eigenvalue
can be decided by a quantum circuit of size at most 2O(k(n)). We ﬁrst use our space-eﬃcient error
reduction procedure to amplify the gap; then we apply a variant of Kitaev’s clock construction [25]
to construct a Hamiltonian from this ampliﬁed circuit. We use a binary clock instead of a unary
one to save space; since the number of gates is at most 2O(k(n)), the clock only needs to be of size
O(k(n)), and the total dimension of the system is 2O(k(n)) as required. Therefore the Hamiltonian
is not local, but it remains sparse (with only a constant number of nonzero terms in each row).
Kitaev’s analysis then shows that we can obtain a gap inverse polynomial in the circuit size, or
inverse exponential in k(n).
Proof of Theorems 18 and 19. Immediate from Lemmas 20, 21, and 22.
Note the polynomial space case in Theorem 19 is Corollary 3, that PreciseQMA = PSPACE.
Finally, we end with two results particular to the polynomial space case. First of all, in the
equality PreciseQMA = PSPACE, we can actually achieve perfect completeness (c = 1) for the
QMA proof protocol, assuming the underlying gate set contains the Hadamard and Toﬀoli gates.
Moreover for perfect completeness we do not require that c −s > 2−poly:
Proposition 23. Let QMA(c, s) = (poly, poly)-bounded QMApoly(c, s). Then
PSPACE = QMA(1, 1 −2−poly) =
[
s<1
QMA(1, s),
where we assume that the gateset we use contains the Hadamard and Toﬀoli gates. In the last term,
the union is taken over all functions s(n) such that s(n) < 1 for all n.
2In recent work we improved this result to achieve such ampliﬁcation using only log
r
c−s additional space [17].
9


<!-- ==== page 11 ==== -->
The containment QMA(1, s) ⊆PSPACE is known [21]. We prove this proposition in Appendix F.
Our second result concerns the QMA-complete Local Hamiltonian problem. We show that if we
allow the promise gap to be exponentially small, then the problem becomes PSPACE-complete.
Deﬁnition 24 (Precise k-Local Hamiltonian). Given as input is a k-local Hamiltonian H =
Pr
j=1 Hj acting on n qubits, satisfying r ∈poly(n) and ∥Hj∥≤poly(n), and numbers a < b
satisfying b −a > 2−poly(n). It is promised that the smallest eigenvalue of H is either at most a or
at least b. Output 1 if the smallest eigenvalue of H is at most a, and output 0 otherwise.
Theorem 25. For any 3 ≤k ≤O(log(n)), Precise k-Local Hamiltonian is PreciseQMA-complete,
and hence PSPACE-complete.
See Appendix G for a proof. Combined with the perfect completeness results of Appendix F,
this will also give a proof that determining whether a local Hamiltonian is frustration-free is a
PSPACE-complete problem (Theorem 39 in Appendix G).
5
Complete problems for time- and space- bounded classes
As we noted in the introduction, variants of the problems we consider are already known to be
complete for other time-bounded quantum complexity classes. For example, consider the problem
of inverting an eﬃciently encoded 2O(k(n)) × 2O(k(n)) matrix with condition number at most κ(n).
If κ(n), k(n) = poly(n), this problem is BQP-complete [20]. Theorem 14 says that this problem is
instead BQUSPACE[O(k)]-complete if κ = 2O(k). Similarly, consider the problem of determining
whether the minimum eigenvalue of an eﬃciently encoded 2O(k(n)) × 2O(k(n)) matrix is at least b
or at most a, with b −a = g(n). If g = 1/ poly and k = poly then this problem is QMA-complete
[25, 2]. Theorem 18 says that this problem is instead BQUSPACE[O(k)]-complete if g = 2−O(k).
In both of the problems we consider, we have two parameters that we can vary: for matrix
inversion, the condition number κ and the matrix size k; and for minimum eigenvalue, the promise
gap size g = b−a and the matrix size k. Varying these two parameters independently gives complete
problems for quantum classes that are simultaneously bounded in time and space.
Theorem 26. Consider the class of problems solvable by a unitary quantum algorithm using
poly(T(n)) gates and O(k(n)) space, where Ω(log(n)) ≤k(n) ≤T(n) ≤2O(k) ≤2poly(n). This class
has the following complete problem under classical poly(n)-time and O(k(n))-space reductions:
Given as input is the size-n eﬃcient encoding of a 2O(k) × 2O(k) positive semideﬁnite matrix
H with a known upper bound κ = poly(T) on the condition number, so that κ−1I ⪯H ⪯I, and
s, t ∈{0, 1}k(n). It is promised that either |H−1(s, t)| ≥b or |H−1(s, t)| ≤a for some constants
0 ≤a < b ≤1; determine which is the case.
Theorem 27. For functions k(n), T(n) satisfying Ω(log(n)) ≤k(n) ≤T(n) ≤2O(k) ≤2poly(n),
[
c−s≥
1
poly(T )
(poly(n), O(k))-bounded QMAO(k)(c, s) = (poly(T), O(k))-bounded QMAO(k)(2/3, 1/3)
Furthermore, the following problem is complete for this class under classical poly(n)-time and
O(k(n))-space reductions:
Given as input is the size-n eﬃcient encoding of a 2O(k) × 2O(k) PSD matrix H, such that
∥H∥max = maxs,t |H(s, t)| is at most a constant.
Let λmin be the minimum eigenvalue of H.
It is promised that either λmin ≤a or λmin ≥b, where a(n) and b(n) are numbers such that
b −a ≥1/ poly(T). Output 1 if λmin ≤a, and output 0 otherwise.
10


<!-- ==== page 12 ==== -->
We omit the proofs; they are straightforward generalizations of the proofs in our paper. These
results interpolate between the time-bounded and space-bounded case: when T = poly(k) the
time-bound dominates and we obtain a time-bounded class; while when T = 2O(k) we obtain a
space-bounded class. Note that when T = 2O(k) then the complexity class in Theorem 27 is equal
to BQUSPACE[O(k)], as shown in Theorem 19.
6
Open Problems
This work leaves open several questions that may lead to interesting follow-up work:
1. Can we use our PreciseQMA = PSPACE result to prove upper or lower bounds for other
complexity classes?
2. Here we have shown PreciseQMA = PSPACE. Ito, Kobayashi and Watrous have shown that
QIP with doubly-exponentially small completeness-soundness gap is equal to EXP [21]. What
can be said about the power of QIP with exponentially small completeness-soundness gap?
3. In this paper we studied unitary quantum space complexity classes, and showed that k(n)-
Well-conditioned Matrix Inversion and k(n)-Minimum Eigenvalue characterize unitary quan-
tum space complexity. Can similar hardness results be shown for non-unitary quantum space
complexity classes?
7
Acknowledgements
We are grateful to Andrew Childs, Sevag Gharibian, David Gosset, Aram Harrow, Hirotada
Kobayashi, Robin Kothari, Tomoyuki Morimae, Harumichi Nishimura, Martin Schwarz, John Wa-
trous, and Xiaodi Wu for helpful conversations, to John Watrous for comments on a preliminary
draft, and to anonymous referees for suggestions. This work was supported by the Department of
Defense.
A
More details on space-bounded computation
For this section, it would be helpful to keep in mind that we always assume the space bound k(n)
always satisﬁes Ω(log(n)) ≤k(n) ≤poly(n).
We start with the deﬁnitions of classical bounded space computation. In discussion of space-
bounded classes, we usually consider Turing machines with two tapes, a read-only input tape
and a work tape; only the space used on the work tape is counted. For k : N →N, a function
f : {0, 1}∗→{0, 1}∗is said to be computable in k(n) space if any bit of f(x) can be computed by
a deterministic Turing machine using space O(k(|x|)) on the work tape. For example, L is the class
of functions that can be computed in O(log n) space.
We now discuss quantum space-bounded complexity classes; for a fuller discussion see [39]. A
straightforward way to deﬁne quantum space-bounded classes is to consider a Turing machine with
three tapes: a read-only classical input tape, a classical work tape, and a quantum work tape
(with two heads) consisting of qubits. This is the model considered in [32] and [38], except that
they allow intermediate measurements (and [38] allows even more general quantum operations).
In this work we consider only computations with no intermediate measurements: we can therefore
impose that there are no measurements on the quantum work tape until the register reaches a
speciﬁed end state, following which a single measurement is performed on the quantum tape and
the algorithm accepts or rejects according to the measurement. Therefore the operations performed
11


<!-- ==== page 13 ==== -->
by the algorithm will not depend on the quantum tape, since there is no way to read information
out of it until the end of the algorithm.
Instead of working with Turing machines, in quantum computation it is much more customary
(and convenient) to work with quantum circuits. For the setup above, since the operations on the
quantum tape are completely classically controlled, we can equivalently consider a quantum circuit
generated by a classical space-bounded Turing machine that computes the quantum gates one-by-
one and applies them in sequence. If the classical Turing machine is O(k(n))-space bounded, it has
at most 2O(k) conﬁgurations, and therefore there are at most 2O(k) quantum gates in the circuit.
Moreover, the O(k)-space bounded classical Turing machine can be replaced by a classical
circuit on O(k) bits, such that there is a poly(n)-time O(k)-space Turing machine that on input i
generates the i-th gate of the circuit (see e.g. [4, Section 6.8]). The classical circuit can then be
bundled into the quantum circuit, and we obtain a quantum circuit with at most 2O(k) gates, such
that each individual gate can be generated in classical poly(n)-time and O(k)-space. This justiﬁes
the deﬁnition of the complexity class QUSPACE[k(n)](c, s):
Deﬁnition 4. Let k(n) be a function satisfying Ω(log(n)) ≤k(n) ≤poly(n). A promise problem
L = (Lyes, Lno) is in QUSPACE[k(n)](c, s) if there exists a poly(|x|)-time O(k)-space uniformly
generated family of quantum circuits {Qx}x∈{0,1}∗, where each circuit Qx = Ux,TUx,T−1 · · · Ux,1 has
T = 2O(k) gates, and acts on O(k(|x|)) qubits, such that:
If x ∈Lyes:
D
0kQ†
x|1⟩⟨1|outQx
0kE
≥c.
(9)
Whereas if x ∈Lno:
D
0kQ†
x|1⟩⟨1|outQx
0kE
≤s.
(10)
Here out denotes a single qubit we measure at the end of the computation; no intermediate measure-
ments are allowed. Furthermore, we require c and s to be computable in classical O(k(n))-space.
B
Proof that O(k(n))-Well-conditioned Matrix Inversion ∈BQUSPACE[k(n)]
Theorem 15. Fix functions k(n), κ(n), and ǫ(n). Suppose we are given the size-n eﬃcient en-
coding of a 2k(n) × 2k(n) PSD matrix H such that κ−1I ⪯H ⪯I. We are also given poly(n)-time
O(k + log(κ/ǫ))-space uniform quantum circuits Ua and Ub acting on k qubits and using at most
T gates. Let Ua|0⟩⊗k(n) = |a⟩and Ub|0⟩⊗k(n) = |b⟩. The following tasks can be performed with
poly(n)-time O(k + log(κ/ǫ))-space uniformly generated quantum circuits with poly(T, k, κ, 1/ǫ)
gates and O(k + log(κ/ǫ)) qubits:
1. With at least constant probability, output an approximation of the quantum state H−1|b⟩/∥H−1|b⟩∥
up to error ǫ.
2. Estimate ∥H−1|b⟩∥up to precision ǫ.
3. Estimate |⟨a|H−1|b⟩| up to precision ǫ.
These circuits do not require intermediate measurements.
For convenience we also restate the following lemma:
Lemma 16 (Implicit in [20, 32]). There is a poly-time O(k + log(κ/ǫ′))-space uniform quantum
unitary transformation WH over k +ℓ= O(k +log(κ/ǫ′)) qubits and using poly(k, κ/ǫ′) gates, such
that for any k-qubit input state |b⟩,
WH(|0⟩⊗ℓ⊗|b⟩) = α|0⟩out ⊗|ψb⟩+
p
1 −α2|1⟩out ⊗
ψ′
b
,
(11)
12


<!-- ==== page 14 ==== -->
where |ψb⟩and |ψ′
b⟩are normalized states such that ∥|ψb⟩−|0⟩⊗ℓ−1 ⊗
H−1|b⟩
∥H−1|b⟩∥∥≤ǫ′, α is a positive
number satisfying |α −∥H−1|b⟩∥
κ
| ≤ǫ′, and “out” is a 1-qubit register.
Before we start the proof, we note that for ease of exposition we will actually use a limited
number of intermediate measurements of up to O(k + log(κ/ǫ)) qubits. These intermediate mea-
surements are not necessary, since they can be deferred to the end of the computation using only
O(k + log(κ/ǫ)) extra space, which ﬁts within our space bound. (It is only when the number of
intermediate measurements used is superlinear in the amount of space available that we cannot
defer measurements.)
Proof of Theorem 16. We ﬁrst show the ﬁrst item, i.e.
generating the state H−1|b⟩/∥H−1|b⟩∥.
Choose ǫ′ = O(ǫ/κ) in the statement of Lemma 16, keeping in mind for the rest of the proof that
log(κ/ǫ′) = O(log(κ/ǫ)). Note that |ψb⟩can be obtained by computing WHUb|0⟩all = WH(|0⟩anc ⊗
|b⟩), and then postselecting on the output qubit being in state |0⟩.
To obtain |ψb⟩with high
probability we can repeat this procedure many times until success.
We can then get a good
approximation to
H−1|b⟩
∥H−1|b⟩∥by tracing out the other ancilla qubits. For our setting we would like
to get by with a low space requirement and without using intermediate measurements, so instead
of repeating until success, we will apply amplitude ampliﬁcation to the above unitary WH. Deﬁne
the projectors Π0 and Π1 by
Π0 = |0⟩⟨0|anc ⊗|b⟩⟨b|
(12)
Π1 = W †
H(|0⟩⟨0|out ⊗I)WH
(13)
Deﬁne |v⟩= |0⟩anc ⊗|b⟩, and write
|v⟩= sin θ|w⟩+ cos θ
w⊥E
,
(14)
|w⟩= sin θ|v⟩+ cos θ
v⊥E
(15)
where
v⊥E
, |w⟩, and
w⊥E
are normalized states such that
Π0|v⟩= |v⟩,
Π0
v⊥E
= 0
(16)
Π1|w⟩= |w⟩,
Π1
w⊥E
= 0.
(17)
Note that
(⟨0|anc ⊗I)WH(|0⟩⟨0|anc ⊗|b⟩⟨b|)(|0⟩anc ⊗|b⟩) = WHΠ1Π0(|0⟩anc ⊗|b⟩) ∝WH|w⟩,
(18)
and therefore WH|w⟩is the postmeasurement state we desire.
The success probability of the
postselection step is simply ⟨v|Π0Π1Π0|v⟩= α2 = sin2 θ.
Consider now the operator R = −(I −2Π1)(I −2Π0); by analogy from Grover’s algorithm, it is
easy to see that R is a rotation operator with angle 2θ. It has eigenvalues e±i2θ, with the following
eigenvectors:
R|ψ+⟩= ei2θ|ψ+⟩,
|ψ+⟩≡
1
√
2

|v⟩+ i
v⊥E
= ie−iθ
√
2

|w⟩−i
w⊥E
(19)
R|ψ−⟩= e−i2θ|ψ−⟩,
|ψ−⟩≡
1
√
2

|v⟩−i
v⊥E
= −ieiθ
√
2

|w⟩+ i
w⊥E
(20)
13


<!-- ==== page 15 ==== -->
Note our initial state |v⟩is a uniform superposition of the eigenstates of R: |v⟩= 2−1/2(|ψ+⟩+|ψ−⟩).
We perform phase estimation of the rotation operator R on the state |v⟩with precision O(ǫ′) and
failure probability δ = 2−O(k) poly(κ/ǫ); this requires poly(T, k, κ, 1/ǫ) gates and O(k + log(κ/ǫ))
extra ancilla qubits to perform, and with probability 1 −δ outputs an estimate for either θ or
−θ with error O(ǫ′). Taking the absolute value of the sine of the output, we obtain an estimate
of α = sin θ with error O(ǫ′) = O(ǫ/κ). Since |α −∥H−1|b⟩∥
κ
| ≤ǫ′, this allows us to calculate an
estimate for ∥H−1|b⟩∥up to precision O(κǫ′) = O(ǫ), with probability 1 −2−O(k) poly(κ/ǫ). This
completes the second task.
To complete the ﬁrst task, we note that the residual state after the phase estimation procedure
is still a linear combination of |ψ+⟩and |ψ−⟩. If the phase estimation procedure above had output
an estimate ˜θ+ ≈O(ǫ′) θ (this happens with probability at least (1 −δ)/2), then because the we
set the failure probability to be δ, the residual state must be δ-close to |ψ+⟩. From (19) we see
that this residual state has constant overlap with |w⟩. Similarly, if the phase estimation procedure
had instead output an estimate close to −θ (this happens with probability at least (1 −δ)/2),
then we obtain a residual state δ-close to |ψ−⟩, and hence with constant overlap with |w⟩. By
applying WH to our state and verifying the ancilla qubits are all zero, we obtain the desired state
WH|w⟩≈H−1|b⟩with constant probability.
Finally, if an estimate for |⟨a|H−1|b⟩| is desired, we can consider instead the following modiﬁ-
cation to Π0 and Π1:
Π0 = |0⟩⟨0|anc ⊗|b⟩⟨b|
(21)
Π′
1 = W †
H(|0⟩⟨0|out ⊗I)(Ianc ⊗|a⟩⟨a|)(|0⟩⟨0|out ⊗I)WH
(22)
Since (|0⟩⟨0|out ⊗I)WH(|0⟩⊗ℓ⊗|b⟩) = α|0⟩out ⊗|ψb⟩, we see that
⟨v|Π0Π′
1Π0|v⟩= α2 

⟨0|⊗ℓ−1 ⊗⟨a|

|ψb⟩

2 .
(23)
⟨v|Π0Π′
1Π0|v⟩can be estimated in the same way that α has been estimated. Recalling that ∥|ψb⟩−
|0⟩⊗ℓ−1 ⊗
H−1|b⟩
∥H−1|b⟩∥∥≤ǫ′ and |α −∥H−1|b⟩∥
κ
| ≤ǫ′, this allows us to estimate |⟨a|H−1|b⟩| to O(ǫ)
precision.
C
k(n)-Well-conditioned Matrix Inversion is hard for BQSPACE[k(n)]
We begin our hardness proof by considering the following simple hard problem for BQUSPACE[k(n)]:
Deﬁnition 28 (k(n)-Quantum Circuit Acceptance). Given as input is the size-n classical algorithm
(Turing machine) that generates a quantum circuit Q acting on k(n) qubits with T = 2O(k(n)) 1-
or 2-qubit gates: on input i, the algorithm outputs the gate i-th gate of the circuit in polynomial
time and O(k(n)) space. It is promised that either the matrix entry |⟨0⊗k(n)|Q|0⊗k(n)⟩| ≥2/3 or
|⟨0⊗k(n)|Q|0⊗k(n)⟩| ≤1/3; determine which is the case.
Lemma 29 (Implicit in [5, 14]). O(k(n))-Quantum Circuit Acceptance is BQUSPACE[k(n)]-hard
under classical poly(n)-time, O(k(n))-space reductions.
Proof. This lemma is implicit in e.g., [5, 14]. We include the proof here for completeness. Suppose
we are given an x ∈{0, 1}n and would like to determine if x ∈Lyes for some L = {Lyes, Lno} ∈
BQUSPACE[k]. There is a quantum circuit on k(n) qubits, Qx = UT UT−1 · · · U1 of size T = 2O(k(n))
that decides x. That is,
Qx|0⊗k(n)⟩= √px|1⟩out|ψ1
x⟩+
p
1 −px|0⟩out|ψ0
x⟩.
(24)
14


<!-- ==== page 16 ==== -->
where out indicates the designated output qubit, and |ψ1
x⟩, |ψ0
x⟩are (k −1)-qubit states; px is the
probability that the computation accepts, so px ≥2/3 if x ∈Lyes and px ≤1/3 if x ∈Lno. Note
that the uniformity condition on BQUSPACE[k] guarantees the existence of a classical algorithm
that generates Qx.
We now describe a reduction which creates a related circuit ˜Qx with a single matrix entry that
is proportional to the acceptance probability of Qx. This new circuit ˜Qx takes the same number of
input qubits as Qx as well as an additional ancillary qubit. ˜Qx runs Qx, then using a single CNOT
gate copies the state of the output qubit to the ancillary qubit, ﬂips the ancillary qubit, and ﬁnally
applies the inverse, Q†
x, to the input qubits. It is straightforward to check that
⟨0|⟨0⊗k(n)| ˜Qx|0⊗k(n)⟩|0⟩= px.
(25)
Therefore knowing the single matrix entry ⟨0|⟨0⊗k(n)| ˜Qx|0⊗k(n)⟩|0⟩is suﬃcient to decide if x ∈Lyes.
Moreover, ˜Qx can be computed from Qx using polynomial time and O(k) space, and this completes
the proof.
Theorem 30. O(k(n))-Well-conditioned Matrix Inversion is BQUSPACE[k(n)]-hard under classi-
cal reductions computable in polynomial time and O(k(n)) space.
Proof. We will show that k(n)-Well-conditioned Matrix Inversion is as hard as k(n)-Quantum Circuit Acceptance.
Given an instance of the latter, i.e., a circuit on k(n) qubits, Q = UT UT−1 · · · U1 with T = 2O(k(n)),
deﬁne the following unitary of dimension 3T2k:
U =
T
X
t=1
|t + 1⟩⟨t| ⊗Ut + |t + T + 1⟩⟨t + T| ⊗I + |t + 2T + 1 mod 3T ⟩⟨t + 2T| ⊗U†
T+1−t
Crucially, note that for any t in the range [T, 2T] and any state |ψ⟩on k(n) qubits:
Ut|1⟩|ψ⟩= |t + 1⟩⊗Q|ψ⟩
(26)
Furthermore U3T = I, a fact we will soon exploit. We now construct the Hermitian matrix:
H =
"
0
I −Ue−1/T
I −U†e−1/T
0
#
(27)
H has dimension N = 6T2k and condition number κ ≤2T = 2O(k). Notice that given as input a
description of Q we can compute each entry of H to within 2−O(k(n)) error in O(k(n)) space, via
space eﬃcient algorithms for exponentiation [29]. Furthermore, H−1 is the following matrix:


0

I −U†e−1/T −1

I −Ue−1/T −1
0


(28)

I −Ue−1/T −1 is just the power series P∞
j=0 Uje−j/T =
1
1−e−3
P3T−1
j=0 Uje−j/T , where we’ve used
U3T = I. Therefore for any ﬁxed t ∈[0, 3T −1],
⟨0⊗k(n)|⟨t + 1|

I −Ue−1/T −1 |1⟩|0⊗k(n)⟩=
1
1 −e−3 ⟨0⊗k(n)|⟨t + 1|


3T−1
X
j′=0
Uj′e−j′/T

|1⟩|0⊗k(n)⟩
(29)
15


<!-- ==== page 17 ==== -->
which is a particular entry in H−1. In the second line we’ve used j = 3Tx + j′ for some integers x
and j′ ∈[0, 3T −1], and that U3T = I. For any t ∈[T, 2T], as a consequence of Equation 26 the
above quantity equals
e−t/T
1 −e−3 ⟨0⊗k(n)|Q|0⊗k(n)⟩.
(30)
In particular, an estimation of this entry of H−1 will solve k(n)-Quantum Circuit Acceptance.
D
Proof of Lemma 21
D.1
In-place gap ampliﬁcation of QMA protocols with phase estimation
We start out by proving the following lemma, which proves “in-place” gap ampliﬁcation of QMA
using phase estimation (see also the similar result of Nagaj et. al, Lemma 40 in Appendix H).
Lemma 31. For any functions t, k, r > 0,
(t, k)-bounded QMAm(c, s) ⊆

O
 t2r
c −s

, O

k + r + log

1
c −s

-bounded QMAm(1−2−r, 2−r).
Proof. Let L = (Lyes, Lno) be a promise problem in QMA(c, s) and {Vx}x∈{0,1}∗the corresponding
uniform family of veriﬁcation circuits. Deﬁne the projectors:
Π0 = Im ⊗
0kED
0k,
Π1 = V †
x (|1⟩⟨1|out ⊗Im+k−1) Vx
(31)
and the corresponding reﬂections R0 = 2Π0 −I, R1 = 2Π1 −I. Deﬁne φc = arccos √c/π and
φs = arccos √s/π (recalling that these functions can be computed to precision O(c −s) in space
O(log[1/(c −s)]). Now consider the following procedure:
1. Perform phase estimation of the operator R1R0 on the state |ψ⟩⊗
0kE
, with precision O(c−s)
and failure probability 2−r.
2. Output YES if the phase is at most (φc + φs)/2; otherwise output NO.
Phase estimation of an operator U up to precision a and failure probability ǫ requires α :=
⌈log2(1/a)⌉+ log2[2 + 1/(2ǫ)] additional ancilla qubits and 2α = O(1/(aǫ)) applications of the
control-U operation (see e.g. [28]). Thus, the above procedure can be implemented by a circuit of
size O(2rt/(c −s)) using O(r + log[1/(c −s)]) extra ancilla qubits. Using the standard analysis
of in-place QMA error reduction [26, 27], it can be shown that this procedure has completeness
probability at least 1 −2−r and soundness at most 2−r.
In Appendix H we will prove the following stronger error reduction lemma that gives the same
space bound but uses less time. This better time bound will be required for proving Lemma 22.
Lemma 32. For any functions t, k, r > 0,
(t, k)-bounded QMAm(c, s) ⊆

O
 rt
c −s

, O

k + r + log

1
c −s

-bounded QMAm(1−2−r, 2−r).
Thus, we get the following corollaries:
Corollary 33. For any r = O(k), QUSPACE[k](c, c −2−O(k)) ⊆QUSPACE[Θ(k)](1 −2−r, 2−r).
This corollary shows that error reduction is possible for unitary quantum O(k)-space bounded
classes, as long as the completeness-soundness gap is at least 2−O(k).
16


<!-- ==== page 18 ==== -->
Proof. This follows from Lemma 32 by taking m = 0, s = c −2−Θ(k), and r = Θ(k).
Corollary 34.
(t, k)-bounded QMAm(c, c −2−Θ(k)) ⊆

O

t2Θ(k)
, O (k)

-bounded QMAm(1 −2−(m+2), 2−(m+2)).
Proof. This follows from Lemma 32 by taking s = c −2−Θ(k) and r = m + 2.
D.2
Removing the witness of an ampliﬁed QMA protocol
Theorem 35. For any function t = 2O(k+m),
(t, k)-bounded QMAm(1 −2−(m+2), 2−(m+2)) ⊆QUSPACE[k + m](3/4 · 2−m, 1/4 · 2−m).
Proof. The proof is very similar to that of [26, Theorem 3.6]. For any functions m, k, consider a
problem L ∈(t, k)-bounded QMAm(1 −2−(m+2), 2−(m+2)), and let {V ′
x}x∈{0,1}∗be a uniform family
of veriﬁcation circuits for L with completeness 1 −2−(m+2) and soundness 2−(m+2).
For convenience, deﬁne the 2m × 2m matrix:
Qx := (I2m ⊗⟨0p|) V ′†
x |1⟩⟨1|outV ′
x (I2m ⊗|0p⟩) .
(32)
Qx is positive semideﬁnite, and ⟨ψ|Qx|ψ⟩is the acceptance probability of V ′
x on witness ψ. Thus
x ∈Lyes ⇒tr[Qx] ≥1 −2−(m+2) ≥3/4
(33)
since the trace is at least the largest eigenvalue, and m ≥0; likewise,
x ∈Lno ⇒tr[Qx] ≤2m · 2−(m+2) = 1/4
(34)
since the trace is the sum of the 2m eigenvalues, each of which is at most 2−(m+2).
Therefore our problem reduces to determining whether the trace of Qx is at least 3/4 or at
most 1/4. Now we show that using the totally mixed state 2−mIm (alternatively, preparing m EPR
pairs and taking a qubit from each pair) as the witness of the veriﬁcation procedure encoded by
Qx, succeeds with the desired completeness and soundness bounds. The acceptance probability is
given by tr(Qx2−mIm) = 2−m tr(Qx), which is at least 2−m · 3/4 if x ∈Lyes, and at most 2−m · 1/4
if x ∈Lno.
Thus we have reduced the problem L to determining if a quantum computation
with no witness, acting on k + m qubits, accepts with probability at least 3/4 · 2−m or at most
s′ = 1/4 · 2−m.
We can ﬁnally ﬁnish the proof of Lemma 21.
Proof of Lemma 21. This follows from Corollary 34, Theorem 35, and Corollary 33.
E
O(k(n))-Minimum Eigenvalue is hard for BQUSPACE[k(n)]
In this section we prove Lemma 22, stated here for convenience.
Lemma 22. O(k(n))-Minimum Eigenvalue is BQUSPACE[k(n)]-hard under classical poly-time
O(k(n))-space reductions.
17


<!-- ==== page 19 ==== -->
Proof. Let L = (Lyes, Lno) be a problem in BQUSPACE[k(n)], and suppose it has a veriﬁer that
uses t = 2O(k) gates with completeness 2/3 and soundness 1/3. By Lemma 32, we can amplify
the gap to get a new veriﬁer circuit that uses T = O(rt) gates, and has completeness c = 1 −2−r
and soundness s = 2−r. Choose r = O(k) large enough so that c ≥1 −1/T 3 and s ≤1/T 3, and
suppose Vx = Vx,TVx,T−1 · · · Vx,1 is the new (gap-ampliﬁed) veriﬁer circuit for L acting on k qubits.
Consider the Kitaev clock Hamiltonian:
H = Hin + Hprop + Hout
(35)
deﬁned on the Hilbert space C2k ⊗CT+1, where
Hin =
0kED
0k ⊗|0⟩⟨0|,
Hout = (|1⟩⟨1|out ⊗Ik−1) ⊗|T⟩⟨T|
(36)
Hprop =
T
X
j=1
1
2
h
−Vx,j ⊗|j⟩⟨j −1| −V †
x,j ⊗|j −1⟩⟨j| + I ⊗(|j⟩⟨j| + |j −1⟩⟨j −1|)
i
.
(37)
H is a sparse matrix - in fact, there are only a constant number of nonzero terms in each row.
Since each gate Vx,j can be computed in classical polynomial time and k(n) space, it follows that
so can the nonzero entries of H. Moreover, let λmin be the minimum eigenvalue of H; then it was
shown by Kitaev [25] that if x ∈Lyes then λmin ≤a = (1 −c)/(T + 1), while if x ∈Lno then
λmin ≥b = (1 −s)/T 3. Since c ≥1 −1/T 3 and s ≤1/T 3 we see that 2−O(k) < b −a.
F
Achieving Perfect Completeness for PreciseQMA
We now consider the problem of achieving perfect completeness for PreciseQMA. Speciﬁcally, we
will show the following:
Proposition 23. Let QMA(c, s) = (poly, poly)-bounded QMApoly(c, s). Then
PSPACE = QMA(1, 1 −2−poly) =
[
s<1
QMA(1, s),
where we assume that the gateset we use contains the Hadamard and Toﬀoli gates. In the last term,
the union is taken over all functions s(n) such that s(n) < 1 for all n.
Since PSPACE = PreciseQMA, this proposition shows that any PreciseQMA protocol can be
reduced to a diﬀerent PreciseQMA protocol with perfect completeness, i.e. in the YES case Arthur
accepts Merlin’s witness with probability 1. The reduction is rather roundabout, however, and it
would be interesting to see if a more direct reduction can be found.
The second equality follows from the ﬁrst equality and the result by [21] that QMA(1, s) ⊆
PSPACE. We will therefore only prove the ﬁrst equality.
Looking back at Circuit 7, we see that we almost have perfect completeness in our protocol al-
ready - if the Hamiltonian simulation of e−iHt could be done without error, then indeed the protocol
has perfect completeness. Our strategy will be perform a diﬀerent unitary that can be performed
exactly, but, like e−iHt, also allows us to use phase estimation to distinguish the eigenvalues of H.
Given a sparse Hamiltonian H (with at most d nonzero entries per row) and a number X ≥
maxj,ℓ|Hjℓ| that upper bounds the absolute value of entries of H, Andrew Childs deﬁned an eﬃ-
ciently implementable quantum walk [7, 12]. Each step of the quantum walk is a unitary U with
eigenvalues ei˜λ, where
˜λ = arcsin λ
Xd
(38)
18


<!-- ==== page 20 ==== -->
with λ representing eigenvalues of H. Note that the YES case λ = 0 corresponds to ˜λ = 0, and the
NO case λ ≥2−g(n) corresponds to ˜λ ≥2−g(n)/(Xd) since arcsin x ≥x for |x| ≤1. In the latter
case the ˜λ can be at most exponentially small, and therefore the stripped down version of phase
estimation still suﬃces to tell the two cases apart with exponentially small probability.
We now note that the Hamiltonian H we obtain from the hardness reduction from PSPACE
(Lemma 22) is of a very special form. Speciﬁcally, since BQUSPACE[poly] = PSPACE, we can
assume the veriﬁer circuit Vx is deterministic, so it has completeness 1 and soundness 0. Moreover,
all of its gates are classical, and hence all entries of the Kitaev clock Hamiltonian H are 0, ±1/2,
or 1.
For the matrix H satisfying the above, U can be implemented exactly with a standard gateset;
perfect completeness of the protocol will then follow. If H is a N × N matrix (where N = 2n), U
is (see presentation in [9, Section 3.1 and Lemma 10]) a unitary deﬁned on the enlarged Hilbert
space C2N ⊗C2N = (CN ⊗C2) ⊗(CN ⊗C2), as follows:
U = ST(I2N ⊗(I2N −2|0⟩⟨0|2N))T †
(39)
where the 2N subscript indicates a register of dimension 2N, the unitary S swaps the two registers,
and the unitary T is deﬁned by
T =
N−1
X
j=0
X
b∈{0,1}
(|j⟩⟨j| ⊗|b⟩⟨b|) ⊗|ϕjb⟩⟨0|2N
(40)
with |ϕj1⟩= |0⟩N|1⟩and
|ϕjb⟩=
1
√
d
X
ℓ∈Fj
|ℓ⟩


s
H∗
jℓ
X |0⟩+
s
1 −
|H∗
jℓ|
X |1⟩

,
(41)
where Fj index the nonzero entries in the j-th row. Recall that for any j, ℓ, Hjℓ= 0, ±1/2, or 1,
and hence we can take X = 1. If we furthermore assume d is a power of 2 (which we can always
do by adding indices of zero entries to Fj), it is straightforward to see that both S and T can
be implemented using just Hadamard gates and classical gates (Pauli-X, controlled-X, and Toﬀoli
gates) - the latter of which can be implemented using just Toﬀoli gates and access to a qubit in the
|1⟩state (which can be provided by the prover). Therefore U can be exactly implemented in any
gateset that allows Hadamard gates and Toﬀoli gates to be implemented exactly.
G
Precise Local Hamiltonian Problem
Recall the following deﬁnition:
Deﬁnition 24 (Precise k-Local Hamiltonian). Given as input is a k-local Hamiltonian H =
Pr
j=1 Hj acting on n qubits, satisfying r ∈poly(n) and ∥Hj∥≤poly(n), and numbers a < b
satisfying b −a > 2−poly(n). It is promised that the smallest eigenvalue of H is either at most a or
at least b. Output 1 if the smallest eigenvalue of H is at most a, and output 0 otherwise.
In this section we will prove the following:
Theorem 25. For any 3 ≤k ≤O(log(n)), Precise k-Local Hamiltonian is PreciseQMA-complete,
and hence PSPACE-complete.
19


<!-- ==== page 21 ==== -->
Proof. This proof follows straightforwardly by adapting the proof of [25] and [24]. The proof of
containment in PreciseQMA is identical to the containment of the usual Local Hamiltonian problem
in QMA; see [25] for details.
To show PreciseQMA-hardness, we note that for a QMA-veriﬁcation procedure with T gates,
completeness c and soundness s, [24] reduces this to a 3-local Hamiltonian with lowest eigenvalue
no more than (1 −c)/(T + 1) in the YES case, or no less than (1 −s)/T 3 in the NO case. For this
to specify a valid Precise Local Hamiltonian problem we need that
1 −s
T 3
−1 −c
T + 1 > 2−poly(n).
(42)
Recalling that we showed that perfect completeness can be assumed for PreciseQMA-hard problems,
we can take c = 1, s = 1 −2−poly(n) and the above inequality trivially holds. Hence any problem
in PSPACE can be reduced to a Precise 3-Local Hamiltonian problem.
In fact, even just testing whether a k-Local Hamiltonian is frustration-free is PSPACE-complete:
Deﬁnition 38 (Frustration-Free k-Local Hamiltonian). Given as input is a k-local Hamiltonian
H = Pr
j=1 Hj acting on n qubits, satisfying r ∈poly(n), each term Hj is positive semideﬁnite, and
∥Hj∥≤poly(n). Output 1 if the smallest eigenvalue of H is zero, and output 0 otherwise.
Theorem 39. Frustration-Free k-Local Hamiltonian is PSPACE-complete.
Proof. The containment in PSPACE follows from the proof of the containment of the usual Local
Hamiltonian problem in QMA [25], along with Proposition 23. PSPACE-hardness follows from the
proof of Theorem 25, by taking c = 1 in the proof.
H
In-place gap ampliﬁcation
In this appendix we will prove Lemma 32. To do so we ﬁrst start out with the following weaker
result:
Lemma 40 (Implicit in Nagaj, Wocjan, and Zhang [27]). For any functions t, k, r > 0,
(t, k)-bounded QMAm(c, s) ⊆

O
 rt
c −s

, O

k + r log

1
c −s

-bounded QMAm(1 −2−r, 2−r).
Proof. Let L = (Lyes, Lno) be a promise problem in QMA(c, s) and {Vx}x∈{0,1}∗the corresponding
uniform family of veriﬁcation circuits. Deﬁne the projectors:
Π0 = Im ⊗
0kED
0k
(43)
Π1 = V †
x (|1⟩⟨1|out ⊗Im+k−1) Vx
(44)
and the corresponding reﬂections:
R0 = 2Π0 −I,
R1 = 2Π1 −I.
(45)
Deﬁne φc = arccos √c/π and φs = arccos √s/π (recalling that these functions can be computed to
precision O(c −s) in space O(log[1/(c −s)]). Now consider the following procedure:
1. Perform r trials of phase estimation of the operator R1R0 on the state |ψ⟩⊗
0kE
, with
precision O(c −s) and 1/16 failure probability.
20


<!-- ==== page 22 ==== -->
2. If the median of the r results is at most (φc + φs)/2, output YES; otherwise output NO.
Phase estimation of an operator U up to precision a and failure probability ǫ requires α :=
⌈log2(1/a)⌉+ log2[2 + 1/(2ǫ)] additional ancilla qubits and 2α = O(1/(aǫ)) applications of the
control-U operation (see e.g. [28]). Thus, the above procedure, which uses r applications of phase
estimation to precision O(c −s), can be implemented by a circuit of size O(rt/(c −s)) using
O(r log[1/(c −s)]) extra ancilla qubits. Using the standard analysis of in-place QMA error reduc-
tion [26, 27], it can be seen that this procedure has completeness probability at least 1 −2−r and
soundness at most 2−r.
We can now prove Lemma 32, which we restate below:
Lemma 32. For any functions t, k, r > 0,
(t, k)-bounded QMAm(c, s) ⊆

O
 rt
c −s

, O

k + r + log

1
c −s

-bounded QMAm(1−2−r, 2−r).
Proof.
(t, k)-bounded QMAm(c, s) ⊆

O

t
c −s

, O

k + log

1
c −s

-bounded QMAm(3/4, 1/4)
⊆

O
 rt
c −s

, O

k + r + log

1
c −s

-bounded QMAm(1 −2−r, 2−r)
where the ﬁrst line follows by taking r = 2 in Lemma 31, and the second line follows from Lemma 40.
I
Proof sketch of PQPOP EP S
∥,classical = PP
Since PP ⊆BQPOPEPS
∥,classical ⊆PQPOPEPS
∥,classical [30], we only need to show that PQPOP EP S
∥,classical ⊆PP.
In [30] it was noted that all PEPS can be seen as the output of a quantum circuit followed by
a postselected measurement.
Therefore PQPOP EP S
∥,classical corresponds to the problems that can be
decided by a quantum circuit, followed by a postselected measurement (since the queries to OP EP S
are classical and nonadaptive, we can compose them into one single postselection), followed by a
measurement. In the YES case the measurement outputs 1 with probability at least c, whereas in
the NO case the measurement outputs 1 with probability at most s, with c > s. The standard
counting argument placing BQP inside PP then applies to this case as well; see for instance [1,
Propositions 2 and 3].
References
[1] Scott Aaronson. Quantum computing, postselection, and probabilistic polynomial-time. Pro-
ceedings of the Royal Society A, 461(2063):3473–3482, 2005.
[2] Dorit Aharonov and Amnon Ta-Shma. Adiabatic quantum state generation and statistical zero
knowledge. In Proceedings of the 35th Annual ACM Symposium on the Theory of Computing
(STOC), pages 20–29, 2003.
[3] Eric W. Allender and Klaus W. Wagner. Counting hierarchies: polynomial time and con-
stant depth circuits. In G. Rozenberg and A. Salomaa, editors, Current trends in Theoretical
Computer Science, pages 469–483. World Scientiﬁc, 1993.
21


<!-- ==== page 23 ==== -->
[4] Sanjeev Arora and Boaz Barak. Computational Complexity: A Modern Approach. Cambridge
University Press, New York, NY, USA, 2009.
[5] Charles H. Bennett, Ethan Bernstein, Gilles Brassard, and Umesh V. Vazirani. Strengths and
weaknesses of quantum computing. SIAM J. Comput., 26(5):1510–1523, 1997.
[6] Stuart J. Berkowitz. On computing the determinant in small parallel time using a small number
of processors. Information Processing Letters, 18(3):147–150, 1984.
[7] Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and Rolando D. Somma.
Exponential improvement in precision for simulating sparse Hamiltonians. In Proceedings of
the 46th Annual ACM Symposium on Theory of Computing (STOC), pages 283–292, New
York, NY, USA, 2014. ACM.
[8] Dominic W. Berry, Andrew M. Childs, Richard Cleve, Robin Kothari, and Rolando D. Somma.
Simulating Hamiltonian dynamics with a truncated Taylor series. Physical Review Letters,
114:090502, 2015.
[9] Dominic W. Berry, Andrew M. Childs, and Robin Kothari.
Hamiltonian simulation with
nearly optimal dependence on all parameters. In Proceedings of the 56th IEEE Symposium on
Foundations of Computer Science (FOCS), pages 792–809, 2015.
[10] A Borodin, S Cook, and N Pippenger. Parallel computation for well-endowed rings and space-
bounded probabilistic machines. Information and Control, 58(1-3):113–136, July 1984.
[11] Sergey Bravyi. Eﬃcient algorithm for a quantum analogue of 2-sat. arXiv preprint quant-
ph/0602108, 2006.
[12] Andrew Childs. On the relationship between continuous- and discrete-time quantum walk.
Communications in Mathematical Physics, 294:581–603, 2010.
[13] Stephen A. Cook. A taxonomy of problems with fast parallel algorithms. Information and
Control, 64(1-3):2 – 22, 1985. International Conference on Foundations of Computation Theory.
[14] Christopher M. Dawson, Andrew P. Hines, Duncan Mortimer, Henry L. Haselgrove, Michael A.
Nielsen, and Tobias Osborne. Quantum computing and polynomial equations over the ﬁnite
ﬁeld Z2. Quantum Information & Computation, 5(2):102–112, 2005.
[15] Dean Doron, Amir Sarid, and Amnon Ta-Shma. On approximating the eigenvalues of stochas-
tic matrices in probabilistic logspace. Electronic Colloquium on Computational Complexity
(ECCC) preprint TR16-120, 2016.
[16] Dean Doron and Amnon Ta-Shma. On the problem of approximating the eigenvalues of undi-
rected graphs in probabilistic logspace. In Proceedings of the 42nd International Colloquium
on Automata, Languages and Programming (ICALP), pages 419–431, 2015.
[17] Bill Feﬀerman, Hirotada Kobayashi, Cedric Yen-Yu Lin, Tomoyuki Morimae, and Harumichi
Nishimura. Space-eﬃcient error reduction for unitary quantum computations. In Proceedings
of the 43rd International Colloquium on Automata, Languages and Programming (ICALP),
pages 14:1–14:14, 2016.
[18] François Le Gall. Solving Laplacian systems in logarithmic space. arXiv preprint 1608.01426,
2016.
22


<!-- ==== page 24 ==== -->
[19] David Gosset and Daniel Nagaj. Quantum 3-SAT is QMA1-complete. In Proceedings of the
54th IEEE Annual Symposium on Foundations of Computer Science (FOCS), pages 756–765,
2013.
[20] Aram W Harrow, Avinatan Hassidim, and Seth Lloyd. Quantum algorithm for linear systems
of equations. Physical Review letters, 103(15):150502, 2009.
[21] Tsuyoshi Ito, Hirotada Kobayashi, and John Watrous. Quantum interactive proofs with weak
error bounds. In Proceedings of the 3rd Innovations in Theoretical Computer Science Confer-
ence (ITCS), pages 266–275, 2012.
[22] Richard Jozsa, Barbara Kraus, Akimasa Miyake, and John Watrous.
Matchgate and
space-bounded quantum computations are equivalent.
Proceedings of the Royal Society A,
466(2115):809–830, 2010.
[23] Richard Jozsa and Akimasa Miyake. Matchgates and classical simulation of quantum circuits.
Proceedings of the Royal Society A, 464(2100):3089–3106, 2008.
[24] Julia Kempe and Oded Regev. 3-local Hamiltonian is QMA-complete. Quantum Information
& Computation, 3(3):258–264, 2003.
[25] A. Yu. Kitaev, A. H. Shen, and M. N. Vyalyi. Classical and Quantum Computation. American
Mathematical Society, Boston, MA, USA, 2002.
[26] Chris Marriott and John Watrous. Quantum Arthur-Merlin games. Computational Complexity,
14(2):122–152, 2005.
[27] Daniel Nagaj, Pawel Wocjan, and Yong Zhang. Fast ampliﬁcation of QMA. Quantum Infor-
mation & Computation, 9(11):1053–1068, 2011.
[28] M. A. Nielsen and I. L. Chuang. Quantum Information and Computation. Cambridge Univer-
sity Press, Cambridge, UK, 2000.
[29] John H. Reif. Logarithmic depth circuits for algebraic functions. SIAM Journal on Computing,
15(1):231–242, 1986.
[30] Norbert Schuch, Michael M. Wolf, Frank Verstraete, and J. Ignacio Cirac. Computational
complexity of projected entangled pair states. Physical Review Letters, 98:140506, 2007.
[31] Yaoyun Shi. Both Toﬀoli and controlled-NOT need little help to do universal quantum com-
puting. Quantum Information & Computation, 3(1):84–92, January 2003.
[32] Amnon Ta-Shma. Inverting well conditioned matrices in quantum logspace. In Dan Boneh, Tim
Roughgarden, and Joan Feigenbaum, editors, Proceedings of the 46th Annual ACM Symposium
on Theory of Computing (STOC), pages 881–890. ACM, 2013.
[33] Barbara M. Terhal and David P. DiVincenzo. Classical simulation of noninteracting-fermion
quantum circuits. Physical Review A, 65(3):032325, 2002.
[34] Leslie G. Valiant.
Quantum circuits that can be simulated classically in polynomial time.
SIAM Journal on Computing, 31(4):1229–1254, 2002.
[35] Dieter van Melkebeek and Thomas Watson.
Time-space eﬃcient simulations of quantum
computations. Theory of Computing, 8:1–51, 2012.
23


<!-- ==== page 25 ==== -->
[36] F. Verstraete and J. I. Cirac. Renormalization algorithms for quantum-many body systems in
two and higher dimensions. arXiv preprint cond-mat/0407066, 2004.
[37] John Watrous. Space-bounded quantum complexity. Journal of Computer and System Sci-
ences, 59(2):281–326, 1999.
[38] John Watrous. On the complexity of simulating space-bounded quantum computations. Com-
putational Complexity, 12(1):48–84, 2003.
[39] John Watrous. Quantum computational complexity. In Robert A. Meyers, editor, Encyclopedia
of Complexity and Systems Science, pages 7174–7201. Springer, 2009.
24


# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:1304.5773 — Frank Gaitan and Lane Clark, 'Graph isomorphism and adiabatic quantum computing'
# Extraction performed 2026-07-05 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

Graph isomorphism and adiabatic quantum computing
Frank Gaitan1 and Lane Clark2
1Laboratory for Physical Sciences, 8050 Greenmead Dr, College Park, MD 20740
2Department of Mathematics, Southern Illinois University, Carbondale, IL 62901-4401
(Dated: October 29, 2018)
In the Graph Isomorphism (GI) problem two N-vertex graphs G and G′ are given and the task
is to determine whether there exists a permutation of the vertices of G that preserves adjacency
and transforms G →G′.
If yes, then G and G′ are said to be isomorphic; otherwise they are
non-isomorphic. The GI problem is an important problem in computer science and is thought to
be of comparable diﬃculty to integer factorization. In this paper we present a quantum algorithm
that solves arbitrary instances of GI and which also provides a novel approach to determining all
automorphisms of a given graph. We show how the GI problem can be converted to a combinatorial
optimization problem that can be solved using adiabatic quantum evolution. We numerically simu-
late the algorithm’s quantum dynamics and show that it correctly: (i) distinguishes non-isomorphic
graphs; (ii) recognizes isomorphic graphs and determines the permutation(s) that connect them; and
(iii) ﬁnds the automorphism group of a given graph G. We then discuss the GI quantum algorithm’s
experimental implementation, and close by showing how it can be leveraged to give a quantum al-
gorithm that solves arbitrary instances of the NP-Complete Sub-Graph Isomorphism problem. The
computational complexity of an adiabatic quantum algorithm is largely determined by the minimum
energy gap ∆(N) separating the ground- and ﬁrst-excited states in the limit of large problem size
N ≫1. Calculating ∆(N) in this limit is a fundamental open problem in adiabatic quantum com-
puting, and so it is not possible to determine the computational complexity of adiabatic quantum
algorithms in general, nor consequently, of the speciﬁc adiabatic quantum algorithms presented here.
Adiabatic quantum computing has been shown to be equivalent to the circuit-model of quantum
computing, and so development of adiabatic quantum algorithms continues to be of great interest.
PACS numbers: 03.67.Ac,02.10.Ox,89.75.Hc
I.
INTRODUCTION
An instance of the Graph Isomorphism (GI) problem
is speciﬁed by two N-vertex graphs G and G′ and the
challenge is to determine whether there exists a permu-
tation of the vertices of G that preserves adjacency and
transforms G →G′. When such a permutation exists,
the graphs are said to be isomorphic; otherwise they are
non-isomorphic.
GI has been heavily studied in com-
puter science [1]. Polynomial classical algorithms exist
for special cases of GI, still it has not been possible to
prove that GI is in P. Although it is known that GI is
in NP, it has also not been possible to prove that it is
NP-Complete. The situation is the same for Integer Fac-
torization (IF)—it belongs to NP, but is not known to be
in P or to be NP-Complete. GI and IF are believed to
be of comparable computational diﬃculty[2].
IF and GI have also been examined from the perspec-
tive of quantum algorithms and both have been con-
nected to the hidden subgroup problem (HSP) [3]. For
IF the hidden subgroup is contained in an abelian parent
group (Z∗
n = group of units modulo n), while for GI the
parent group is non-abelian (Sn = symmetric group on
n elements). While Fourier sampling allows the abelian
HSP to be solved eﬃciently[4], strong Fourier sampling
does not allow an eﬃcient solution of the non-abelian
HSP over Sn [5]. At this time an eﬃcient quantum algo-
rithm for GI is not known.
A number of researchers have considered using the
dynamics of physical systems to solve instances of GI.
Starting from physically motivated conjectures, these ap-
proaches embed the structure of the graphs appearing in
the GI instance into the Hamiltonian that drives the sys-
tem dynamics. In Ref. [6] the systems considered were
classical, while Refs. [7–11] worked with quantum sys-
tems.
• Building on Refs. [7] and [8], Refs. [9] and [10] pro-
posed using multi-particle quantum random walks
(QRW) on graphs as a means for distinguishing
pairs of non-isomorphic graphs.
Numerical tests
of this approach focused on GI instances involv-
ing strongly regular graphs (SRG). The adjacency
matrix for each SRG was used to deﬁne the Hamil-
tonian H(G) that drives the QRW on the graph
G.
The walkers can only hop between vertices
joined by an edge in G. The propagator U(G) =
exp[−iH(G)t] is evaluated at a ﬁxed time t for
each SRG associated with a GI instance.
The
two propagators are used to deﬁne a comparison
function that is conjectured to vanish for isomor-
phic pairs of SRGs, and to be non-zero otherwise.
Refs. [9] and [10] examined both interacting and
non-interacting systems of quantum walkers and
found that:
(i) no non-interacting QRW with a
ﬁxed number of walkers can distinguish all pairs
of SRGs; (ii) increasing the number of walkers in-
creases the distinguishing power of the approach;
and (iii) two-interacting bosonic walkers have more
distinguishing power than both one and two non-
arXiv:1304.5773v2  [quant-ph]  12 Feb 2014


---- page 2 ----

2
interacting walkers.
No analysis was provided of
the algorithm’s runtime T(N) versus problem size
N in the limit of large problem size N ≫1, and so
the computational complexity of this GI algorithm
is currently unknown.
Note that for isomorphic
pairs of graphs, this algorithm cannot determine
the permutation(s) connecting the two graphs, nor
the automorphism group of a given graph. Finally,
no discussion of the algorithm’s experimental im-
plementation is given.
• The GI algorithm presented in Ref. [11] is based
on adiabatic quantum evolution: here the problem
Hamiltonian is an Ising Hamiltonian that identiﬁes
the qubits with the vertices of a graph, and qubits
i and j interact antiferromagnetically only when
vertices i and j in the graph are joined by an edge.
It was conjectured that the instantaneous ground-
state encodes enough information about the graph
to allow suitably chosen measurements to distin-
guish pairs of non-isomorphic graphs. Physical ob-
servables that are invariant under qubit permuta-
tions are measured at intermediate times and the
diﬀerences in the dynamics generated by two non-
isomorphic graphs are assumed to allow the mea-
surement outcomes to recognize the graphs as non-
isomorphic. The algorithm was tested numerically
on (mostly) SRGs, and it was found that combina-
tions of measurements of the: (i) spin-glass order
parameter, (ii) x-magnetization, and (iii) total av-
erage energy allowed all the non-isomorphic pairs of
graphs examined to be distinguished. Ref. [11] did
not determine the scaling relation for the runtime
T(N) versus problem size N for N ≫1, and so
the computational complexity of this algorithm is
currently unknown.The algorithm is also unable to
determine the permutation(s) that connect a pair of
isomorphic graphs, nor the automorphism group of
a given graph. Ref. [11] discussed the experimental
implementation of this algorithm and noted that
the measurements available on the D-Wave hard-
ware do not allow the observables used in the nu-
merical tests to be measured on the hardware.
In this paper we present a quantum algorithm that
solves arbitrary instances of GI. The algorithm also pro-
vides a novel approach for determining the automorphism
group of a given graph. The GI quantum algorithm is
constructed by ﬁrst converting an instance of GI into an
instance of a combinatorial optimization problem whose
cost function, by construction, has a zero minimum value
when the pair of graphs in the GI instance are isomorphic,
and is positive when the pair are non-isomorphic. The
speciﬁcation of the GI quantum algorithm is completed
by showing how the combinatorial optimization problem
can be solved using adiabatic quantum evolution. To test
the eﬀectiveness of this GI quantum algorithm we nu-
merically simulated its Schrodinger dynamics. The sim-
ulation results show that it can correctly: (i) distinguish
pairs of non-isomorphic graphs; (ii) recognize pairs of iso-
morphic graphs and determine the permutation(s) that
connect them; and (iii) ﬁnd the automorphism group of
a given graph. We also discuss the experimental imple-
mentation of the GI algorithm, and show how it can be
leveraged to give a quantum algorithm that solves ar-
bitrary instances of the (NP-Complete) Sub-Graph Iso-
morphism (SGI) problem. As explained in Section IV,
calculation of the runtime for an adiabatic quantum al-
gorithm in the limit of large problem size is a fundamen-
tal open problem in adiabatic quantum computing. It
is thus not presently possible to determine the compu-
tational complexity of adiabatic quantum algorithms in
general, nor, consequently, of the speciﬁc adiabatic quan-
tum algorithms presented here. However, because adia-
batic quantum computing has been shown to be equiva-
lent to the circuit-model of quantum computing [12–14],
the development of adiabatic quantum algorithms contin-
ues to be of great interest. Just as with the GI algorithms
of Refs. [8]-[11], our GI algorithm also has unknown com-
plexity. However, unlike the algorithms of Refs. [8]-[11],
the GI algorithm presented here: (i) encodes the GI in-
stance explicitly into the cost function of a combinato-
rial optimization problem which is solved using adiabatic
quantum evolution without introducing physical conjec-
tures; and (ii) determines the permutation(s) connecting
two isomorphic graphs, and the automorphism group of
a given graph. As we shall see, our GI algorithm can be
implemented on existing D-Wave hardware using estab-
lished embedding procedures [15]. Such an implementa-
tion is in the works and will be reported elsewhere.
The structure of this paper is as follows. In Section II
we give a careful presentation of the GI problem, and
show how an instance of GI can be converted to an in-
stance of a combinatorial optimization problem whose
solution (Section III) can be found using adiabatic quan-
tum evolution. To test the performance of the GI quan-
tum algorithm introduced in Section III, we numerically
simulated its Schrodinger dynamics and the results of
that simulation are presented in Section IV. In Section V
we describe the experimental implementation of the GI
algorithm, and in Section VI we show how it can be used
to give a quantum algorithm that solves arbitrary in-
stances of the NP-Complete problem known as SubGraph
Isomorphism. Finally, we summarize our results in Sec-
tion VII. Two appendices are also included.
The ﬁrst
brieﬂy summarizes the quantum adiabatic theorem and
its use in adiabatic quantum computing, and the second
reviews the approach to embedding the problem Hamil-
tonian for an adiabatic quantum algorithm onto the D-
Wave hardware that was presented in Ref. [15].
II.
GRAPH ISOMORPHISM PROBLEM
In this Section we introduce the Graph Isomorphism
(GI) problem and show how an instance of GI can be con-
verted into an instance of a combinatorial optimization


---- page 3 ----

3
problem (COP) whose cost function has zero (non-zero)
minimum value when the pair of graphs being studied
are isomorphic (non-isomorphic).
A.
Graphs and graph isomorphism
A graph G is speciﬁed by a set of vertices V and a
set of edges E. We focus on simple graphs in which an
edge only connects distinct vertices, and the edges are
undirected. The order of G is deﬁned to be the number
of vertices contained in V , and two vertices are said to be
adjacent if they are connected by an edge. If x and y are
adjacent, we say that y is a neighbor of x, and vice versa.
The degree d(x) of a vertex x is equal to the number of
vertices that are adjacent to x. The degree sequence of a
graph lists the degree of each vertex in the graph ordered
from largest degree to smallest. A graph G of order N
can also be speciﬁed by its adjacency matrix A which is
an N × N matrix whose matrix element ai,j = 1 (0) if
the vertices i and j are (are not) adjacent. For simple
graphs ai,i = 0 and ai,j = aj,i since edges only connect
distinct vertices and are undirected.
Two graphs G and G′ are said to be isomorphic if there
is a one-to-one correspondence π between the vertex sets
V and V ′ such that two vertices x and y are adjacent in
G if and only if their images πx and πy are adjacent in
G′. The graphs G and G′ are non-isomorphic if no such
π exists. Since no one-to-one correspondence π can exist
when the number of vertices in G and G′ are diﬀerent,
graphs with unequal orders are always non-isomorphic. It
can also be shown [16] that if two graphs are isomorphic,
they must have identical degree sequences.
We can also describe graph isomorphism in terms of
the adjacency matrices A and A′ of the graphs G and
G′, respectively. The graphs are isomorphic if and only
if there exists a permutation matrix σ of the vertices of
G that satisﬁes
A′ = σAσT ,
(1)
where σT is the transpose of σ. It is straight-forward to
show that if G and G′ are isomorphic, then a permuta-
tion matrix σ exists that satisﬁes Eq. (1). To prove the
“only if” statement, note that the i-j matrix element of
the RHS is Aσi,σj. Eq. (1) is thus satisﬁed when a per-
mutation matrix σ exists such that A′
i,j = Aσi,σj. Thus
Eq. (1) is simply the condition that σ preserve adjacency.
Since a permutation is a one-to-one correpondence, the
existence of a permutation matrix σ satisfying Eq. (1)
implies G and G′ are isomorphic. Thus, the existence of
a permutation matrix σ satisfying Eq. (1) is an equivalent
way to deﬁne graph isomorphism.
The Graph Isomorphism (GI) problem is to determine
whether two given graphs G and G′ are isomorphic. The
problem is only non-trivial when G and G′ have the same
order and so we focus on that case in this paper.
B.
Permutations, binary strings, and linear maps
A permutation π of a ﬁnite set S = {0, . . . , N −1} is
a one-to-one correspondence from S →S which sends
i →πi such that πi ∈S, and πi ̸= πj for i ̸= j. The
permutation π can be written
π =

0
· · ·
i
· · · N −1
π0 · · · πi · · ·
πN−1

,
(2)
where column i indicates that π sends i →πi.
Since
the top row on the RHS of Eq. (2) is the same for all
permutations, all the information about π is contained
in the bottom row. Thus we can map a permutation π
into an integer string P(π) = π0 · · · πN−1, with πi ∈S
and πi ̸= πj for i ̸= j.
For reasons that will become clear in Section II C, we
want to convert the integer string P(π) = π0 · · · πN−1
into a binary string pπ. This can be done by replacing
each πi in P(π) by the unique binary string formed from
the coeﬃcients appearing in its binary decomposition
πi =
U−1
X
j=0
πi,j (2)j .
(3)
Here U ≡⌈log2 N⌉. Thus the integer string P(π) is trans-
formed to the binary string
pπ = (π0,0 · · · π0,U−1) · · · (πN−1,0 · · · πN−1,U−1) ,
(4)
where πi,j ∈{0, 1}. The binary string pπ has length NU,
where
N ≤2U ≡M + 1.
(5)
Thus we can identify a permutation π with the binary
string pπ in Eq. (4).
Let H be the Hamming space of binary strings of length
NU. This space contains 2NU strings, and we have just
seen that N! of these strings pπ encode permutations
π. Our last task is to deﬁne a mapping from H to the
space of N × N matrices σ with binary matrix elements
σi,j = 0, 1. The mapping is constructed as follows:
1. Let sb = s0 · · · sNU−1 be a binary string in H. We
parse sb into N substrings of length U as follows:
sb = (s0 · · · sU−1) (sU · · · s2U−1) · · ·
 s(N−1)U · · · sNU−1

.
(6)
2. For each substring siU · · · s(i+1)U−1, construct the
integer
si =
U−1
X
j=0
siU+j (2)j ≤2U −1 = M.
(7)
3. Finally,
introduce
the
integer
string
s
=
s0 · · · sN−1, and deﬁne the N × N matrix σ(s) to
have matrix elements
σi,j(s) =

0,
if sj > N −1
δi,sj, if 0 ≤sj ≤N −1,
(8)
where i, j ∈S, and δx,y is the Kronecker delta.


---- page 4 ----

4
Note that when the binary string sb corresponds to a per-
mutation, the matrix σ(s) is a permutation matrix since
the si formed in step 2 will obey 0 ≤si ≤N −1 and
si ̸= sj for i ̸= j. In this case, if A is the adjacency
matrix for a graph G, then A′ = σ(s)AσT (s) will be the
adjacency matrix for a graph G′ isomorphic to G. On
the other hand, if sb does not correspond to a permuta-
tion, then the adjacency matrix A′ = σ(s)AσT (s) must
correspond to a graph G′ which is not isomorphic to G.
The result of our development so far is the establish-
ment of a map from binary strings of length NU to N×N
matrices (viz. linear maps) with binary matrix elements.
When the string is (is not) a permutation, the matrix
produced is (is not) a permutation matrix. Finally, re-
call from Stirling’s formula that log2 N! ∼N log2 N −N
which is the number of bits needed to represent N!. Our
encoding of permutations uses N⌈log2 N⌉bits and so ap-
proaches asymptotically what is required by Stirling’s
formula.
C.
Graph isomorphism and combinatorial
optimization
As seen above, an instance of GI is speciﬁed by a pair of
graphs G and G′ (or equivalently, by a pair of adjacency
matrices A and A′). Here we show how a GI instance
can be transformed into an instance of a combinatorial
optimization problem (COP) whose cost function has a
minimum value of zero if and only if G and G′ are iso-
morphic.
The search space for the COP is the Hamming space
H of binary strings sb of length NU which are associated
with the integer strings s and matrices σ(s) introduced in
Section II B. The COP cost function C(s) contains three
contributions
C(s) = C1(s) + C2(s) + C3(s).
(9)
The ﬁrst two terms on the RHS penalize integer strings
s = s0 · · · sN−1 whose associated matrix σ(s) is not a
permutation matrix,
C1(s) =
N−1
X
i=0
M
X
α=N
δsi,α
(10)
C2(s) =
N−2
X
i=0
N−1
X
j=i+1
δsi,sj,
(11)
where δx,y is the Kronecker delta. We see that C1(s) > 0
when si > N −1 for some i, and C2(s) > 0 when si = sj
for some i ̸= j. Thus C1(s) + C2(s) = 0 if and only if
σ(s) is a permutation matrix. The third term C3(s) adds
a penalty when σ(s)AσT (s) ̸= A′:
C3(s) = ∥σ(s)AσT (s) −A′∥i.
(12)
Here ∥M∥i is the Li-norm of M. In the numerical sim-
ulations discussed in Section IV, the L1-norm is used,
though any Li-norm would be acceptable. Thus, when
G and G′ are isomorphic, C3(s) = 0, and σ(s) is the per-
mutation of vertices of G that maps G →G′. Putting all
these remarks together, we see that if C(s) = 0 for some
integer string s, then G and G′ are isomorphic and σ(s)
is the permutation that connects them.
On the other
hand, if C(s) > 0 for all strings s, then G and G′ are
non-isomorphic.
We have thus converted an instance of GI into an in-
stance of the following COP:
Graph Isomorphism COP: Given
the
N-vertex
graphs G and G′ and the associated cost function
C(s) deﬁned above, ﬁnd an integer string s∗that
minimizes C(s).
By construction: (i) C(s∗) = 0 if and only if G and G′ are
isomorphic and σ(s∗) is the permutation matrix mapping
G →G′; and (ii) C(s∗) > 0 if and only if G and G′ are
non-isomorphic.
Before moving on, notice that if G = G′, then C(s∗) =
0 since G is certainly isomorphic to itself. In this case
σ(s∗) is an automorphism of G. We shall see that the
GI quantum algorithm to be introduced in Section III
provides a novel approach for ﬁnding the automorphism
group of a graph.
III.
ADIABATIC QUANTUM ALGORITHM
FOR GRAPH ISOMORPHISM
A quantum algorithm is an algorithm that can be run
on a realistic model of quantum computation [17]. One
such model is adiabatic quantum computation [18] which
is based on adiabatic quantum evolution [19, 20]. The
adiabatic quantum optimization (AQO) algorithm [21] is
an example of adiabatic quantum computation that ex-
ploits the adiabatic dynamics of a quantum system to
solve a COP (see Appendix A for a brief overview). The
AQO algorithm uses the optimization problem cost func-
tion to deﬁne a problem Hamiltonian HP whose ground-
state subspace encodes all problem solutions. The algo-
rithm evolves the state of an L-qubit register from the
ground-state of an initial Hamiltonian Hi to the ground-
state of HP with probability approaching 1 in the adi-
abatic limit.
An appropriate measurement at the end
of the adiabatic evolution yields a solution of the opti-
mization problem almost certainly. The time-dependent
Hamiltonian H(t) for global AQO is
H(t) =

1 −t
T

Hi +
 t
T

HP ,
(13)
where T is the algorithm runtime, and adiabatic dynam-
ics corresponds to T →∞.
To map the GI COP onto an adiabatic quantum com-
putation, we begin by promoting the binary strings sb to
computational basis states (CBS) |sb⟩. Thus each bit in
sb is promoted to a qubit so that the quantum register


---- page 5 ----

5
contains L = NU = N⌈log2 N⌉qubits. The CBS are
deﬁned to be the 2L eigenstates of σ0
z ⊗· · · ⊗σL−1
z
. The
problem Hamiltonian HP is deﬁned to be diagonal in the
CBS with eigenvalue C(s), where s is the integer string
associated with sb:
HP |sb⟩= C(s)|sb⟩.
(14)
Note that (see Section II C) the ground-state energy of
HP will be zero if and only if the graphs G and G′ are
isomorphic. We will discuss the experimental realization
of HP in Section V. The initial Hamiltonian Hi is chosen
to be
Hi =
L−1
X
l=0
1
2
 Il −σl
x

,
(15)
where Il and σl
x are the identity and x-Pauli operator for
qubit l, respectively. The ground-state of Hi is the easily
constructed uniform superposition of CBS.
The quantum algorithm for GI begins by preparing the
L qubit register in the ground-state of Hi and then driv-
ing the qubit register dynamics using the time-dependent
Hamiltonian H(t). At the end of the evolution the qubits
are measured in the computational basis. The outcome
is the bit string s∗
b so that the ﬁnal state of the register is
|s∗
b⟩and its energy is C(s∗), where s∗is the integer string
derived from s∗
b. In the adiabatic limit, C(s∗) will be the
ground-state energy, and if C(s∗) = 0 ( > 0) the algo-
rithm decides G and G′ are isomorphic (non-isomorphic).
Note that any real application of AQO will only be ap-
proximately adiabatic. Thus the probability that the ﬁ-
nal energy C(s∗) will be the ground-state energy will be
1 −ϵ. In this case the GI quantum algorithm must be
run k ∼O(ln(1 −δ)/ ln ϵ) times so that, with probability
δ > 1 −ϵ, at least one of the measurements will return
the ground-state energy. We can make δ arbitrarily close
to 1 by choosing k suﬃciently large.
IV.
NUMERICAL SIMULATION OF
ADIABATIC QUANTUM ALGORITHM
In this Section we present the results of a numerical
simulation of the dynamics of the GI adiabatic quantum
algorithm (AQA). Because the GI AQA uses N⌈log2 N⌉
qubits, and these simulations were carried out using a
classical digital computer, we were limited to GI in-
stances involving graphs with order N ≤7. Although
we would like to have examined larger graphs, this sim-
ply was not practical. Note that the N = 7 simulations
use 21 qubits. These simulations are at the upper limit
of 20-22 qubits at which simulation of the full adiabatic
Schrodinger dynamics is feasible [22–24]. To simulate a
GI instance with graphs of order N = 8 requires a 24
qubit simulation which is well beyond what can be done
practically. The protocol for the simulations presented
here follows Refs. [22–25].
As explained in Appendix A, the runtime for an adia-
batic quantum algorithm is related to the minimum en-
ergy gap arising during the course of the adiabatic quan-
tum evolution. Thus, determining the runtime scaling
relation T(N) versus problem size N in the asymptotic
limit (N ≫1), reduces to determining the minimum
gap scaling relation ∆(N) for large N. This, however,
is a well-known, fundamental open problem in adiabatic
quantum computing, and so it was not possible to deter-
mine the asymptotic runtime scaling relation for our GI
AQA. Although our numerical simulations could be used
to compute a runtime for each of the GI instances con-
sidered below, we did not do so for two reasons. First,
as noted above, the GI instances that can be simulated
using a digital computer are limited to graphs with no
more than seven vertices. These instances are thus far
from the large problem-size limit N ≫1, and so the asso-
ciated runtimes tell us nothing about the asymptotic per-
formance of the GI AQA. Second, it is well-known that
the minimum energy gap encountered during adiabatic
quantum evolution (and which largely determines the
runtime) is sensitive to the particular Hamiltonian path
followed by the adiabatic quantum evolution [26, 27]. De-
termining the optimal Hamiltonian path which yields the
largest minimum gap, and thus the shortest possible run-
time, is another fundamental open problem in adiabatic
quantum computing. As a result, the Hamiltonian path
used in the numerical simulations (i. e. the linear interpo-
lating Hamiltonian H(t) in Eq. (13)) will almost certainly
be non-optimal, and so the runtime it produces will also,
almost certainly, be non-optimal, and thus a poor indi-
cator of GI AQA performance.
In Section IV A we present simulation results for sim-
ple examples of isomorphic and non-isomorphic graphs.
These examples allow us to illustrate the analysis of the
simulation results in a simple setting. Section IV B then
presents our simulation results for non-isomorphic in-
stances of: (i) iso-spectral graphs; and (ii) strongly regu-
lar graphs. Finally, Section IV C considers GI instances
where G′ = G.
Clearly, all such instances correspond
to isomorphic graphs since the identity permutation will
always map G →G and preserve adjacency. The situ-
ation is more interesting when G has symmetries which
allow non-trivial permutations as graph isomorphisms.
These self-isomorphisms are referred to as graph auto-
morphisms, and they form a group known as the auto-
morphism group Aut(G) of G. In this ﬁnal subsection we
use the GI AQA to ﬁnd Aut(G) for a number of graphs.
To the best of our knowledge, using a GI algorithm to
ﬁnd Aut(G) is new. In all GI instances considered in this
Section, the GI AQA correctly: (i) distinguished non-
isomorphic pairs of graphs; (ii) recognized isomorphic
pairs of graphs; and (iii) determined the automorphism
group of a given graph.


---- page 6 ----

6
A.
Illustrative examples
Here we present the results of a numerical simulation
of the GI AQA applied to two simple GI instances. In
Section IV A 1 (Section IV A 2) we examine an instance
of two non-isomorphic (isomorphic) graphs. For the iso-
morphic instance we also present the permutations found
by the GI AQA that transforms G into G′ while preserv-
ing adjacency.
1.
Non-isomorphic graphs
Here we use the GI AQA to examine a GI instance in
which the two graphs G and G′ are non-isomorphic. The
two graphs are shown in Figure 1. Each graph contains
s
s
s
s
0
3
1
2
G
s
s
s
s
0
3
1
2
@
@
@@
    G′
FIG. 1: Two non-isomorphic 4-vertex graphs G and G′.
4 vertices and 4 edges, however they are non-isomorphic.
Examining Figure 1 we see that the degree sequence for
G is {2, 2, 2, 2}, while that for G′ is {3, 2, 2, 1}.
Since
these degree sequences are diﬀerent we know that G and
G′ are non-isomorphic. Finally, the adjacency matrices
A and A′ for G and G′, respectively, are:
A =



0 1 0 1
1 0 1 0
0 1 0 1
1 0 1 0



;
A′ =



0 0 1 1
0 0 0 1
1 0 0 1
1 1 1 0


.
(16)
The GI AQA ﬁnds a non-zero ﬁnal ground-state energy
Egs = 4, and so correctly identiﬁes these two graphs
as non-isomorphic. It also ﬁnds that the ﬁnal ground-
state subspace has a degeneracy of 16. The linear maps
associated with the 16 CBS that span this subspace give
rise to the lowest cost linear maps of G relative to G′. As
these graphs are not isomorphic, these lowest cost maps
have little inherent interest and so we do not list them.
2.
Isomorphic graphs
Here we examine the case of two isomorphic graphs G
and G′ which are shown in Figure 2. Each graph con-
tains 4 vertices and 5 edges, and both graphs have degree
sequence {3, 3, 2, 2}. By inspection of Figure 2, the asso-
ciated adjacency matrices are, respectively,
A =



0 1 1 1
1 0 1 0
1 1 0 1
1 0 1 0



;
A′ =



0 1 1 1
1 0 0 1
1 0 0 1
1 1 1 0


.
(17)
s
s
s
s
@
@
@@
0
3
1
2
G
s
s
s
s
0
3
1
2
@
@
@@
    G′
FIG. 2: Two isomorphic 4-vertex graphs G and G′.
For these two graphs, the GI AQA ﬁnds a vanishing ﬁnal
ground-state energy Egs = 0 and so recognizes G and G′
as isomorphic. It also ﬁnds that the ﬁnal ground-state
subspace has a degeneracy of 4. The four CBS that span
this subspace give four binary strings sb. These four bi-
nary strings in turn generate four integer strings s which
are, respectively, the bottom row of four permutations
(see Eq. (2)). Thus, not only does the GI AQA recognize
G and G′ as isomorphic, but it also returns the 4 graph
isomorphisms π1, . . . , π4 that transform G →G′ while
preserving adjacency:
π1 =

0 1 2 3
0 2 3 1

;
π2 =

0 1 2 3
3 2 0 1

;
π3 =

0 1 2 3
3 1 0 2

;
π4 =

0 1 2 3
0 1 3 2

.
(18)
We will next explicitly show that π1 is a graph isomor-
phism; the reader can easily check that the remaining 3
permutations are also graph isomorphisms.
The permutation matrix σ1 associated with π1 is
σ1 =



1 0 0 0
0 0 0 1
0 1 0 0
0 0 1 0


.
(19)
Under π1, G is transformed to π1(G) which is shown
in Figure 3.
It is clear from Figure 3 that vertices x
s
s
s
s
@
@
@@
0
3
1
2
G
−→
s
s
s
s
0
1
2
3
@
@
@@
π1(G)
FIG. 3: Transformation of G produced by the permutation
π1.
and y are adjacent in G if and only if π1,x and π1,y are
adjacent in π1(G). The adjacency matrix for π1(G) is
σ1AσT
1 which is easily shown to be
σ1AσT
1 =



0 1 1 1
1 0 0 1
1 0 0 1
1 1 1 0


.
(20)
This agrees with the adjacency shown in π1(G) in Fig-
ure 3. Comparison with Eq. (17) shows that σ1AσT
1 = A′.


---- page 7 ----

7
Thus the permutation π1 does map G into G′ and pre-
serve adjacency and so establishes that G and G′ are
isomorphic.
Finally, note that G and G′ are connected by exactly
4 graph isomorphisms. Examination of Figure 2 shows
that the degree-3 vertices in G are vertices 0 and 2, while
in G′ they are vertices 0 and 3. Since the degree of a
vertex is preserved by a graph isomorphism [16], vertex
0 in G must be mapped to vertex 0 or 3 in G′. Then
vertex 2 (in G) must be mapped to vertex 3 or 0 (in G′),
respectively. This then forces vertex 1 to map to vertex
1 or 2, and vertex 3 to map to vertex 2 or 1, respectively.
Thus only 4 graph isomorphism are possible and these
are exactly the 4 graph isomorphisms found by the GI
AQA which appear in Eq. (18).
B.
Non-isomorphic graphs
In this subsection we present GI instances involving
pairs of non-isomorphic graphs. In Section IV B 1 we ex-
amine two instances of isospectral graphs; and in Sec-
tion IV B 2 we look at three instances of strongly regular
graphs. We shall see that the GI AQA correctly distin-
guishes all graph pairs as non-isomorphic.
1.
Iso-spectral graphs
The spectrum of a graph is the set containing all
the eigenvalues of its adjacency matrix.
Two graphs
are iso-spectral if they have identical spectra.
Non-
isomorphic iso-spectral graphs are believed to be diﬃcult
to distinguish [8, 9]. Here we test the GI AQA on pairs of
non-isomorphic iso-spectral graphs. The non-isomorphic
pairs of iso-spectral graphs examined here appear in
Ref. [28].
N = 5 : It is known that no pair of graphs with less
than 5 vertices is iso-spectral [28]. Figure 4 shows a pair
s
s
s
s
s
0
3
1
2
4
G
s
s
s
s
s




A
A
A
AA




D
D
D
DD
0
1
2
3
4
G′
FIG. 4: Two non-isomorphic 5-vertex iso-spectral graphs G
and G′.
of graphs G and G′ with 5 vertices which are isospec-
tral and yet are non-isomorphic.
Although both have
5 vertices and 4 edges, the degree sequence of G is
{2, 2, 2, 2, 0}, while that of G′ is {4, 1, 1, 1, 1}. Since they
have diﬀerent degree sequences, it follows that G and G′
are non-isomorphic. The adjacency matrices A and A′
for G and G′, respectively, are:
A =





0 1 0 1 0
1 0 1 0 0
0 1 0 1 0
1 0 1 0 0
0 0 0 0 0




; A′ =





0 1 1 1 1
1 0 0 0 0
1 0 0 0 0
1 0 0 0 0
1 0 0 0 0




.
(21)
It is straight-forward to show that A and A′ have the
same characteristic polynomial P(λ) = λ5 −4λ3 and
so G and G′ are iso-spectral.
Numerical simulation
of the dynamics of the GI AQA ﬁnds a non-zero ﬁnal
ground-state energy Egs = 5, and so the GI AQA
correctly distinguishes G and G′ as non-isomorphic
graphs.
N = 6 : The pair of graphs G and G′ in Figure 5 are
s
s
s
s
s
s
   @
@
@   @
@
@
0
1
2
4
3
5
G
s s
s
s
s
s
A
AA


A
AA
0
1
2
3
4 5
G′
FIG. 5: Two non-isomorphic 6-vertex iso-spectral graphs G
and G′.
iso-spectral and non-isomorphic. To see this, note that
although both graphs have 6 vertices and 7 edges, the
degree sequence of G is {5, 2, 2, 2, 2, 1}, while that of G′ is
{3, 3, 3, 3, 1, 1}. Since their degree sequences are diﬀerent,
G and G′ are non-isomorphic. The adjacency matrices A
and A′ of G and G′, respectively, are:
A =







0 1 0 0 0 1
1 0 0 0 0 1
0 0 0 0 0 1
0 0 0 0 1 1
0 0 0 1 0 1
1 1 1 1 1 0







; A′ =







0 1 0 0 0 0
1 0 1 1 0 0
0 1 0 1 1 0
0 1 1 0 1 0
0 0 1 1 0 1
0 0 0 0 1 0







.
(22)
Both A and A′ have the same characteristic polynomial
P(λ) = λ6 −7λ4 −4λ3 + 7λ2 + 4λ −1 which establishes
that G and G′ are iso-spectral.
Numerical simulation
of the dynamics of the GI AQA ﬁnds a non-zero ﬁnal
ground-state energy Egs = 7, and so the GI AQA cor-
rectly distinguishes G and G′ as non-isomorphic graphs.
2.
Strongly regular graphs
As we saw in Section II A, the degree d(x) of a vertex
x is equal to the number of vertices that are adjacent to
x. A graph G is said to be k-regular if, for all vertices x,
the degree d(x) = k. A graph is said to be regular if it is


---- page 8 ----

8
k-regular for some value of k. Finally, a strongly regular
graph is a graph with ν vertices that is k-regular, and
for which: (i) any two adjacent vertices have λ common
neighbors; and (ii) any two non-adjacent vertices have
µ common neighbors.
The set of all strongly regular
graphs is divided up into families, and each family is
composed of strongly regular graphs having the same
parameter values (ν, k, λ, µ). In this subsection we apply
the GI AQA to pairs of non-isomorphic strongly regular
graphs. An excellent test for this algorithm would be two
non-isomorphic strongly regular graphs belonging to the
same family as such graphs would then have the same or-
der and degree sequence. Unfortunately, to ﬁnd a family
containing at least two non-isomorphic strongly regular
graphs requires going to a family containing 16-vertex
graphs. For example, the family (16, 9, 4, 6) contains two
non-isomorphic strongly regular graphs.
Since the GI
AQA uses ν⌈log2 ν⌉qubits, simulation of its quantum
dynamics on 16-vertex graphs requires 64 qubits. This
is hopelessly beyond the 20–22 qubit limit for such
simulations discussed in the introduction to Section IV.
As noted there, this hard limit restricts our simulations
to graphs with no more than 7 vertices. Now the number
of connected strongly regular graphs with ν = 4, 5, 6, 7 is
3, 2, 5, 1, respectively. For each of the values ν = 4, 5, 6,
the
strongly
regular
graphs
are
non-isomorphic
as
desired, however, each graph belongs to a diﬀerent
family.
In light of the above remarks, the simulations
reported in this subsection are restricted to pairs of
connected non-isomorphic strongly regular graphs with
ν = 4, 5, 6. Ideally we would have simulated the GI AQA
on the above pair of 16-vertex strongly regular graphs,
however the realities of simulating quantum systems
on a classical computer made this test well beyond reach.
N = 4 : In Figure 6 we show two strongly regular 4-
s
s
s
s
  @
@
@
@
  0
3
1
2
G
s
s
s
s
0
3
1
2
  @
@
@
@
  G′
FIG. 6: Two 4-vertex non-isomorphic strongly regular graphs
G and G′.
vertex graphs G and G′. The parameters for G are ν = 4,
k = 2, λ = 0, and µ = 2; while for G′ they are ν = 4,
k = 3, λ = 2, and µ = 0. It is clear that G and G′ are
non-isomorphic since they contain an unequal number
of edges and diﬀerent degree sequences. The adjacency
matrices A and A′ for G and G′ are, respectively,
A =



0 1 0 1
1 0 1 0
0 1 0 1
1 0 1 0


; A′ =



0 1 1 1
1 0 1 1
1 1 0 1
1 1 1 0


.
(23)
Numerical simulation of the GI AQA dynamics ﬁnds a
non-zero ﬁnal ground-state energy Egs = 4 and so the GI
AQA correctly distinguishes G and G′ as non-isomorphic.
N = 5 : In Figure 7 we show two strongly regular 5-
s
s
s
s
s
  @
@
0
3
1
2
4
G
s
s
s
s
s
  @
@



A
A
A
A

HHHH
0
1
2
3
4
G′
FIG. 7: Two 5-vertex non-isomorphic strongly regular graphs
G and G′.
vertex graphs G and G′. The parameters for G are ν = 5,
k = 2, λ = 0, and µ = 1; while for G′ they are ν = 5,
k = 4, λ = 3, and µ = 0. It is clear that G and G′ are
non-isomorphic since they contain an unequal number
of edges and diﬀerent degree sequences. The adjacency
matrices A and A′ for G and G′ are, respectively,
A =





0 1 0 0 1
1 0 1 0 0
0 1 0 1 0
0 0 1 0 1
1 0 0 1 0




; A′ =





0 1 1 1 1
1 0 1 1 1
1 1 0 1 1
1 1 1 0 1
1 1 1 1 0




.
(24)
Numerical simulation of the GI AQA dynamics ﬁnds
a non-zero ﬁnal ground-state energy Egs = 10 and
so the GI AQA correctly distinguishes G and G′ as
non-isomorphic.
N = 6 : In Figure 8 we show two strongly regular 6-
s
s
s
s
s
s
     @
@
@
@@
   @
@
@
@
@
@
   0
4
1
3
2
5
G
s
3
s4
s1
s5
s
0
s
2 

A
AA
QQ
Q
Q
Q



h
h
h
h
h
h
(
(
(
(
(
(
P
P
P
P
P
P
P
P








G′
FIG. 8: Two 6-vertex non-isomorphic strongly regular graphs
G and G′.
vertex graphs G and G′. The parameters for G are ν = 6,
k = 3, λ = 0, and µ = 3; while for G′ they are ν = 6,
k = 4, λ = 2, and µ = 4. It is clear that G and G′ are
non-isomorphic since they contain an unequal number
of edges and diﬀerent degree sequences. The adjacency


---- page 9 ----

9
matrices A and A′ for G and G′ are, respectively,
A =







0 1 0 1 0 1
1 0 1 0 1 0
0 1 0 1 0 1
1 0 1 0 1 0
0 1 0 1 0 1
1 0 1 0 1 0







; A′ =







0 1 1 1 1 0
1 0 1 0 1 1
1 1 0 1 0 1
1 0 1 0 1 1
1 1 0 1 0 1
0 1 1 1 1 0







.
(25)
Numerical simulation of the GI AQA dynamics ﬁnds
a non-zero ﬁnal ground-state energy Egs = 10 and so
the GI AQA correctly distinguishes G and G′ as non-
isomorphic.
C.
Graph automorphisms
As noted in the Section IV introduction, we can ﬁnd
the automorphism group Aut(G) of a graph G using the
GI AQA by considering a GI instance with G′ = G. To
the best of our knowledge, such an application of a GI
algorithm is new.
Here the self-isomorphisms are per-
mutations of the vertices of G that map G →G while
preserving adjacency. Since G is always isomorphic to
itself, the ﬁnal ground-state energy will vanish: Egs = 0.
The set of CBS |sb⟩that span the ﬁnal ground-state sub-
space give rise to a set of binary strings sb that determine
the integer strings s = s0 · · · sN−1 (see Section II B) that
then determine the permutations π(s),
π(s) =

0
· · ·
i
· · · N −1
s0 · · · si · · ·
sN−1

,
(26)
which are all the elements of Aut(G). By construction,
the order of Aut(G) is equal to the degeneracy of the
ﬁnal ground-state subspace. In this subsection we apply
the GI AQA to the: (i) cycle graphs C4, . . . , C7; (ii) grid
graph G2,3; and (iii) wheel graph W7, and show that it
correctly determines the automorphism group for all of
these graphs.
1.
Cycle graphs
A walk W in a graph is an alternating sequence of
vertices and edges x0, e1, x1, e2, · · · , el, xl, where the
edge ei connects xi−1 and xi for 0 < i ≤l. A walk W
is denoted by the sequence of vertices it traverses W =
x0x1 · · · xl. Finally, a walk W = x0x1 · · · xl is a cycle if
l ≥3; x0 = xl; and the vertices xi with 0 < i < l are
distinct from each other and x0. A cycle with n vertices
is denoted Cn.
The automorphism group of the cycle graph Cn is the
dihedral group Dn [16]. The order of Dn is 2n, and it is
generated by the two elements α and β that satisfy the
following relations,
αn = e;
β2 = e;
αβ = βαn−1,
(27)
where e is the identity element. Because α and β are
generators of Dn, each element g of Dn can be written
as a product of appropriate powers of α and β:
g = αiβj
(0 ≤i ≤n −1 ;
0 ≤j ≤1).
(28)
We now use the GI AQA to ﬁnd the automorphism
group of the cycle graphs Cn for 4 ≤n ≤7. We will see
that the GI AQA correctly determines Aut(Cn) = Dn
for these graphs. We will work out C4 in detail, and then
give more abbreviated presentations for the remaining
cycle graphs as their analysis is identical.
N = 4: The cycle graph C4 appears in Figure 9. It
v
v
v
v
0
3
1
2
C4
FIG. 9: Cycle graph C4.
contains 4 vertices and 4 edges; has degree sequence
{2, 2, 2, 2}; and adjacency matrix
A =



0 1 0 1
1 0 1 0
0 1 0 1
1 0 1 0


.
(29)
Numerical simulation of the GI AQA applied to the
GI instance with G = C4 and G′ = G found a vanishing
ﬁnal ground-state energy Egs = 0. The GI AQA thus
correctly identiﬁes C4 as being isomorphic to itself. The
simulation also found that the ﬁnal ground-state sub-
space is 8-fold degenerate. Table I lists the integer strings
s = s0s1s2s3 that result from the eight CBS |sb⟩that
span the ﬁnal ground-state subspace (see Sections II B
and III). Each integer string s determines the bottom
row of a permutation π(s) (see eq. (26)). We explicitly
show that π(s), for the integer string s = 3210, is an au-
tomorphism of C4. The reader can repeat this analysis to
show that the seven remaining integer strings in Table I
also give rise to automorphisms of C4. Note that the CBS
that span the ﬁnal ground-state subspace determine all
the graph automorphisms of C4. This follows from the
manner in which the GI AQA is constructed since each
automorphism of C4 must give rise to a CBS with van-
ishing energy, and each CBS in the ﬁnal ground-state
subspace gives rise to an automorphism of C4. These au-
tomorphisms form a group Aut(C4) and the GI AQA has


---- page 10 ----

10
TABLE I: Automorphism group Aut(C4) of the cycle graph
C4 as found by the GI AQA. The ﬁrst row lists the integer
strings s = s0s1s2s3 determined by the labels of the eight
CBS |sb⟩that span the ﬁnal ground-state subspace (see text).
Each string s determines a graph automorphism π(s) via
Eq. (26). The second row associates each integer string s in
the ﬁrst row with a graph automorphism π(s). It identiﬁes
the two strings that give rise to the graph automorphisms
α and β that generate Aut(C4), and writes each graph
automorphism π(s) as a product of an appropriate power of
α and β. Note that e is the identity automorphism, and the
product notation assumes the rightmost factor acts ﬁrst.
s = s0s1s2s3 3012 2301 1230
0123
0321 3210 2103 1032
π(s)
α
α2
α3
α4 = e
β
αβ
α2β
α3β
found that the order of Aut(C4) is 8 which is the same
as the order of the dihedral group D4.
The permutation π∗≡π(s = 3210) is
π(3210) =
 
0 1 2 3
3 2 1 0
!
,
(30)
and the associated permutation matrix σ∗≡σ(3210) is
σ(3210) =





0 0 0 1
0 0 1 0
0 1 0 0
1 0 0 0




.
(31)
Under π∗, C4 is transformed to π∗(C4) which is shown
in Figure 10. It is clear from Figure 10 that x and y are
s
s
s
s
0
3
1
2
C4
−→
s
s
s
s
3
0
2
1
π∗(C4)
FIG. 10: Transformation of C4 produced by the permutation
π∗.
adjacent in C4 if and only if π∗,x and π∗,y are adjacent
in π∗(C4). Thus π∗is a permutation of the vertices of C4
that preserves adjacency and so is a graph automorphism
of C4.
We can also show this by demonstrating that
σ∗AσT
∗= A. Using Eqs. (29) and (31) it is easy to show
that
σ∗AσT
∗=





0 1 0 1
1 0 1 0
0 1 0 1
1 0 1 0




.
(32)
This agrees with the adjacency of edges in π∗(C4) ap-
pearing in Figure 10, and comparison with Eq. (29) shows
that σ∗AσT
∗= A, conﬁrming that π∗is an automorphism
of C4.
We now show that Aut(C4) is isomorphic to the di-
hedral group D4 by showing that the automorphisms
π(3012) ≡α and π(0321) ≡β generate Aut(C4), and
satisfy the generator relations (Eq. (27)) for D4.
The
second row of Table I establishes that α and β are the
generators of Aut(C4) as it shows that each element of
Aut(C4) is a product of an appropriate power of α and
β, and all possible products of powers of α and β appear
in that row. Now notice that
α =
 
0 1 2 3
3 0 1 2
!
(33)
corresponds to a clockwise rotation of C4 by 90◦(see
Figure 11) Thus four applications of α corresponds to
s
s
s
s
0
3
1
2
C4
−→
s
s
s
s
3
2
0
1
α(C4)
FIG. 11: Transformation of C4 produced by the automor-
phism α.
a 360◦rotation of C4 which leaves it invariant.
Thus
α4 = e. This can also be checked by composing α with
itself four times using Eq. (33). This establishes the ﬁrst
of the generator relations in Eq. (27). Similarly,
β =
 
0 1 2 3
0 3 2 1
!
(34)
corresponds to reﬂection of C4 about the diagonal pass-
ing through vertices 0 and 2 (see Figure 12). Thus two
s
s
s
s
0
3
1
2
C4
−→
s
s
s
s
0
1
3
2
β(C4)
FIG. 12: Transformation of C4 produced by the automor-
phism β.
applications of β leaves C4 invariant, and so β2 = e.
This establishes the second of the generator relations in
Eq. (27). Finally, to show the third generator relation
αβ = βα3, we simply evaluate both sides of this relation


---- page 11 ----

11
and compare results. Using Table I we ﬁnd that
αβ =
 
0 1 2 3
3 0 1 2
!  
0 1 2 3
0 3 2 1
!
=
 
0 1 2 3
3 2 1 0
!
(35)
βα3 =
 
0 1 2 3
0 3 2 1
!  
0 1 2 3
1 2 3 0
!
=
 
0 1 2 3
3 2 1 0
!
.
(36)
It is clear that αβ does equal βα3. Thus we have shown
that α and β: (i) generate Aut(C4); and (ii) satisfy the
generator relations (Eq. (27)) for the dihedral group D4,
and so generate a group isomorphic to D4. In summary,
we have shown that the GI AQA found all eight graph
automorphisms of C4, and that the group formed from
these automorphisms is isomorphic to the dihedral group
D4 which is the correct automorphism group for C4.
N = 5: The cycle graph C5 appears in Figure 13. It
v
v
v
v
v
    @
@
@
@
0
3
1
2
4
C5
FIG. 13: Cycle graph C5.
has 5 vertices and 5 edges; degree sequence {2, 2, 2, 2, 2};
and adjacency matrix
A =







0 1 0 0 1
1 0 1 0 0
0 1 0 1 0
0 0 1 0 1
1 0 0 1 0







.
(37)
Numerical simulation of the GI AQA applied to the
GI instance with G = C5 and G′ = G found a vanish-
ing ﬁnal ground-state energy Egs = 0.
The GI AQA
thus correctly identiﬁes C5 as being isomorphic to it-
self.
The simulation also found that the ﬁnal ground-
state subspace is 10-fold degenerate. Table II lists the
integer strings s = s0 · · · s4 that result from the ten CBS
|sb⟩that span the ﬁnal ground-state subspace (see Sec-
tions II B and III). Each integer string s ﬁxes the bottom
TABLE II: Automorphism group Aut(C5) of the cycle graph
C5 as found by the GI AQA. The odd rows list the integer
strings s = s0 · · · s4 determined by the labels of the ten CBS
|sb⟩that span the ﬁnal ground-state subspace (see text).
Each string s determines a graph automorphism π(s) via
Eq. (26).
Each even row associates each integer string s
in the odd row preceding it with a graph automorphism
π(s). It identiﬁes the two strings that give rise to the graph
automorphisms α and β that generate Aut(C5), and writes
each graph automorphism π(s) as a product of an appropriate
power of α and β. Note that e is the identity automorphism,
and the product notation assumes the rightmost factor acts
ﬁrst.
s = s0 · · · s4
40123
34012
23401
12340
01234
π(s)
α
α2
α3
α4
α5 = e
s = s0 · · · s4
04321
10432
21043
32104
43210
π(s)
β
αβ
α2β
α3β
α4β
row of a permutation π(s) (see eq. (26)) which is a graph
automorphism of C5. The demonstration of this is iden-
tical to the demonstration given for C4 and so will not be
repeated here. Just as for Aut(C4), the graph automor-
phisms in Table II are all the elements of Aut(C5) which
is seen to have order 10. Note that this is the same as
the order of the dihedral group D5.
We now show that Aut(C5) is isomorphic to the dihe-
dral group D5 by showing that the graph automorphisms
α = π(40123) and β = π(04321) generate Aut(C5), and
satisfy the generator relations (Eq. (27)) for D5.
The
second row of Table II establishes that α and β are the
generators of Aut(C5) as it shows that each element of
Aut(C5) is a product of an appropriate power of α and
β, and that all possible products of powers of α and
β appear in that row. Following the discussion for C4,
it is a simple matter to show that α corresponds to a
72◦clockwise rotation of C5.
Thus 5 applications of
α rotates C5 by 360◦which leaves it invariant.
Thus
α5 = e which is the ﬁrst of the generator relations in
Eq. (27). Similarly, β can be shown to correspond to a
reﬂection of C5 about a vertical axis passing through
vertex 0 in Figure 13.
Thus two applications of β
leave C5 invariant.
Thus β2 = e which is the second
generator relation in Eq. (27). Finally, using Table II,
direct calculation as in Eqs. (35) and (36) shows that
αβ = βα4 which establishes the ﬁnal generator relation
in Eq. (27). We see that α and β generate Aut(C5) and
satisfy the generator relations for D5 and so generate
a 10 element group isomorphic to D5.
In summary,
we have shown that the GI AQA found all ten graph
automorphisms of C5, and that the group formed from
these automorphisms is isomorphic to the dihedral group
D5 which is the correct automorphism group for C5.
N = 6:
The cycle graph C6 appears in Figure 14.
It
has
6
vertices
and
6
edges;
degree
sequence


---- page 12 ----

12
v
v
v
v
v
v
    @
@
@@
@
@
@
@
    0
4
1
3
2
5
C6
FIG. 14: Cycle graph C6.
{2, 2, 2, 2, 2, 2}; and adjacency matrix
A =









0 1 0 0 0 1
1 0 1 0 0 0
0 1 0 1 0 0
0 0 1 0 1 0
0 0 0 1 0 1
1 0 0 0 1 0









.
(38)
Numerical simulation of the GI AQA applied to the
GI instance with G = C6 and G′ = G found a vanish-
ing ﬁnal ground-state energy Egs = 0.
The GI AQA
thus correctly identiﬁes C6 as being isomorphic to it-
self.
The simulation also found that the ﬁnal ground-
state subspace is 12-fold degenerate. Table III lists the
TABLE III: Automorphism group Aut(C6) of the cycle graph
C6 as found by the GI AQA. The ﬁrst and third rows list the
integer strings s = s0 · · · s5 determined by the labels of the
twelve CBS |sb⟩that span the ﬁnal ground-state subspace
(see text). Each string s determines a graph automorphism
π(s) via Eq. (26).
The second and fourth rows associate
each integer string s in the ﬁrst and third rows with a graph
automorphism π(s). They also identify the two strings that
give rise to the graph automorphisms α and β that generate
Aut(C6), and write each graph automorphism π(s) as a
product of an appropriate power of α and β.
Note that
e is the identity automorphism, and the product notation
assumes the rightmost factor acts ﬁrst.
s = s0 · · · s5 501234 450123 345012 234501 123450 012345
π(s)
α
α2
α3
α4
α5
α6 = e
s = s0 · · · s5 105432 210543 321054 432105 543210 054321
π(s)
β
αβ
α2β
α3β
α4β
α5β
integer strings s = s0 · · · s5 that result from the twelve
CBS |sb⟩that span the ﬁnal ground-state subspace (see
Sections II B and III). Each integer string s ﬁxes the bot-
tom row of a permutation π(s) (see eq. (26)) which is a
graph automorphism of C6. The demonstration of this
is identical to the demonstration given for C4 and so will
not be repeated here. Just as for Aut(C4), the graph au-
tomorphisms in Table III are all the elements of Aut(C6)
which is seen to have order 12. Note that this is the same
as the order of the dihedral group D6.
We now show that Aut(C6) is isomorphic to the dihe-
dral group D6 by showing that the graph automorphisms
α = π(501234) and β = π(105432) generate Aut(C6),
and satisfy the generator relations (Eq. (27)) for D6.
The second and fourth rows of Table III establish that α
and β are the generators of Aut(C6) as they show that
each element of Aut(C6) is a product of an appropriate
power of α and β, and that all possible products of
powers of α and β appear in these two rows. Following
the discussion for C4, it is a simple matter to show
that α corresponds to a 60◦clockwise rotation of C6.
Thus 6 applications of α rotates C6 by 360◦which
leaves it invariant.
Thus α6 = e which is the ﬁrst of
the generator relations in Eq. (27).
Similarly, β can
be shown to correspond to a reﬂection of C6 about a
vertical axis that bisects C6. Thus two applications of
β leave C6 invariant. Thus β2 = e which is the second
generator relation in Eq. (27). Finally, using Table III,
direct calculation as in Eqs. (35) and (36) shows that
αβ = βα5 which establishes the ﬁnal generator relation
in Eq. (27). We see that α and β generate Aut(C6) and
satisfy the generator relations for D6 and so generate
a 12 element group isomorphic to D6. In summary, we
have shown that the GI AQA found all twelve graph
automorphisms of C6, and that the group formed from
these automorphisms is isomorphic to the dihedral group
D6 which is the correct automorphism group for C6.
N = 7:
The cycle graph C7 appears in Figure 15.
It
has
7
vertices
and
7
edges;
degree
sequence
v
v
v
v
v
v
v
    @
@
@
@
0
5
1
2
6
4
3
C7
FIG. 15: Cycle graph C7.


---- page 13 ----

13
{2, 2, 2, 2, 2, 2, 2}; and adjacency matrix
A =
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

0 1 0 0 0 0 1
1 0 1 0 0 0 0
0 1 0 1 0 0 0
0 0 1 0 1 0 0
0 0 0 1 0 1 0
0 0 0 0 1 0 1
1 0 0 0 0 1 0
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

.
(39)
Numerical simulation of the GI AQA applied to the
GI instance with G = C7 and G′ = G found a vanishing
ﬁnal ground-state energy Egs = 0. The GI AQA thus
correctly identiﬁes C7 as being isomorphic to itself. The
simulation also found that the ﬁnal ground-state sub-
space is 14-fold degenerate.
Table IV lists the integer
TABLE IV: Automorphism group Aut(C7) of the cycle graph
C7 as found by the GI AQA. The odd rows list the integer
strings s = s0 · · · s6 determined by the labels of the fourteen
CBS |sb⟩that span the ﬁnal ground-state subspace (see
text). Each string s determines a graph automorphism π(s)
via Eq. (26).
Each even row associates each integer string
s in the odd row preceding it with a graph automorphism
π(s).
They also identify the two strings that give rise to
the graph automorphisms α and β that generate Aut(C7),
and write each graph automorphism π(s) as a product
of an appropriate power of α and β.
Note that e is the
identity automorphism, and the product notation assumes
the rightmost factor acts ﬁrst.
s = s0 · · · s6
6012345
5601234
4560123
3456012
π(s)
α
α2
α3
α4
s = s0 · · · s6
2345601
1234560
0123456
π(s)
α5
α6
α7 = e
s = s0 · · · s6
0654321
1065432
2106543
3210654
π(s)
β
αβ
α2β
α3β
s = s0 · · · s6
4321065
5432106
6543210
π(s)
α4β
α5β
α6β
strings s = s0 · · · s6 that result from the fourteen CBS
|sb⟩that span the ﬁnal ground-state subspace (see Sec-
tions II B and III). Each integer string s ﬁxes the bottom
row of a permutation π(s) (see eq. (26)) which is a graph
automorphism of C7. The demonstration of this is iden-
tical to the demonstration given for C4 and so will not
be repeated here. Just as for Aut(C4), the graph auto-
morphisms in Table IV are all the elements of Aut(C7)
which is seen to have order 14. Note that this is the same
as the order of the dihedral group D7.
We now show that Aut(C7) is isomorphic to the dihe-
dral group D7 by showing that the graph automorphisms
α = π(6012345) and β = π(0654321) generate Aut(C7),
and satisfy the generator relations (Eq. (27)) for D7.
The second and fourth rows of Table IV establish that α
and β are the generators of Aut(C7) as they show that
each element of Aut(C7) is a product of an appropriate
power of α and β, and that all possible products of
powers of α and β appear in these two rows. Following
the discussion for C4, it is a simple matter to show that
α corresponds to a 2π/7 radian clockwise rotation of
C7. Thus 7 applications of α rotates C7 by 360◦which
leaves it invariant.
Thus α7 = e which is the ﬁrst of
the generator relations in Eq. (27).
Similarly, β can
be shown to correspond to a reﬂection of C7 about a
vertical axis that passes through vertex 0 in Figure 15.
Thus two applications of β leave C7 invariant.
Thus
β2 = e which is the second generator relation in Eq. (27).
Finally, using Table IV, direct calculation as in Eqs. (35)
and (36) shows that αβ = βα6 which establishes the
ﬁnal generator relation in Eq. (27). We see that α and
β generate Aut(C7) and satisfy the generator relations
for D7 and so generate a 14 element group isomorphic
to D7. In summary, we have shown that the GI AQA
found all fourteen graph automorphisms of C7, and
that the group formed from these automorphisms is
isomorphic to the dihedral group D7 which is the correct
automorphism group for C7.
2.
Grid graph G2,3
The grid graph G2,3 appears in Figure 16. It has 6
v
v
v
v
v
v
4
0
5
1
2
3
G2,3
FIG. 16: Grid graph G2,3.
vertices and 7 edges; degree sequence {3, 3, 2, 2, 2, 2}; and
adjacency matrix
A =









0 1 1 0 0 0
1 0 0 1 0 0
1 0 0 1 1 0
0 1 1 0 0 1
0 0 1 0 0 1
0 0 0 1 1 0









.
(40)
G2,3 has two reﬂection symmetries. The ﬁrst is reﬂection
about the horizontal line passing through vertices 2 and
3, and the second is reﬂection about a vertical line that
bisects G2,3.
Let α and β denote the permutation of


---- page 14 ----

14
vertices that these reﬂections produce. It follows from
their deﬁnition that α = π(452301) and β = π(103254).
They are the generators of the automorphism group of
G2,3: Aut(G2,3) = ⟨α, β⟩.
As reﬂections, they satisfy
α2 = β2 = e.
Applying these reﬂections successively
gives αβ = π(543210) which is a fourth symmetry of
G2,3. Applying these reﬂections in the reverse order, it
is easy to verify that αβ = βα. Thus Aut(G2,3) is a 4
element Abelian group generated by the reﬂections α and
β. Let us now compare this with the results found by the
GI AQA.
Numerical simulation of the GI AQA applied to
the GI instance with G = G2,3 and G′ = G found a
vanishing ﬁnal ground-state energy Egs = 0.
The GI
AQA thus correctly identiﬁes G2,3 as being isomorphic
to itself.
The simulation also found that the ﬁnal
ground-state subspace is 4-fold degenerate. Table V lists
TABLE V: Automorphism group Aut(G2,3) of the grid
graph G2,3 as found by the GI AQA. The ﬁrst row lists
the integer strings s = s0 · · · s5 determined by the labels of
the four CBS |sb⟩that span the ﬁnal ground-state subspace
(see text). Each string s determines a graph automorphism
π(s) via Eq. (26).
The second row associates each integer
string s in the ﬁrst row with a graph automorphism π(s).
They also identify the two strings that give rise to the graph
automorphisms α and β that generate Aut(G2,3), and write
each graph automorphism π(s) as a product of an appropriate
power of α and β. Note that e is the identity automorphism,
and the product notation assumes the rightmost factor acts
ﬁrst.
s = s0 · · · s5
452301
103254
012345
543210
π(s)
α
β
α2 = β2 = e
αβ
the integer strings s = s0 · · · s5 that result from the four
CBS |sb⟩that span the ﬁnal ground-state subspace (see
Sections II B and III). Each integer string s ﬁxes the
bottom row of a permutation π(s) (see eq. (26)) which
is a graph automorphism of G2,3.
The demonstration
of this is identical to the demonstration given for C4
and so will not be repeated here.
Notice that the GI
AQA found the graph automorphisms π(452301) and
π(103254) which implement the reﬂection symmetries of
G2,3 described above. As they implement reﬂections, it
follows that α2 = β2 = e. The GI AQA also found the
graph automorphism π(543210) which is the composite
symmetry αβ described above.
Using Table V, direct
calculation as in Eqs. (35) and (36) shows that αβ = βα.
Thus the GI AQA correctly found the two generators α
and β of Aut(G2,3); correctly determined all 4 elements
of Aut(G2,3); and correctly determined that Aut(G2,3)
is an Abelian group. In summary, the GI AQA correctly
determined the automorphism group of G2,3.
3.
Wheel graph W7
The wheel graph W7 appears in Figure 17. It has 7
v
v
v
v
v
v
v
        @
@
@
@
@
@
@@
    @
@
@@
@
@
@
@
    0
4
1
3
2
5
6
W7
FIG. 17: Wheel graph W7.
vertices and 12 edges; degree sequence {6, 3, 3, 3, 3, 3, 3};
and adjacency matrix
A =
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

0 1 0 0 0 1 1
1 0 1 0 0 0 1
0 1 0 1 0 0 1
0 0 1 0 1 0 1
0 0 0 1 0 1 1
1 0 0 0 1 0 1
1 1 1 1 1 1 0
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

.
(41)
The automorphism group Aut(W7) is isomorphic to the
dihedral group D6 which, as we have seen, has 12 ele-
ments and is generated by two graph automorphisms α
and β that satisfy the generator relations in Eq. (27) with
n = 6 and respectively, rotate W7 clockwise about vertex
6 by 60◦, and reﬂect W7 about a vertical axis through
vertex 6. The graph automorphisms of W7 thus ﬁx ver-
tex 6. Let us now compare this with the results found by
the GI AQA.
Numerical simulation of the GI AQA applied to the
GI instance with G = W7 and G′ = G found a vanish-
ing ﬁnal ground-state energy Egs = 0.
The GI AQA
thus correctly identiﬁes W7 as being isomorphic to it-
self.
The simulation also found that the ﬁnal ground-
state subspace is 12-fold degenerate. Table VI lists the
integer strings s = s0 · · · s6 that result from the twelve
CBS |sb⟩that span the ﬁnal ground-state subspace (see
Sections II B and III). Each integer string s ﬁxes the bot-
tom row of a permutation π(s) (see eq. (26)) which is a
graph automorphism of W7. The demonstration of this
is identical to the demonstration given for C4 and so will
not be repeated here. Just as for Aut(C4), the graph au-
tomorphisms in Table VI are all the elements of Aut(W7)
which is seen to have order 12. Note that this is the same
as the order of the dihedral group D6.


---- page 15 ----

15
TABLE VI: Automorphism group Aut(W7) of the wheel
graph W7 as found by the GI AQA. The odd rows list
the integer strings s = s0 · · · s6 determined by the labels
of the twelve CBS |sb⟩that span the ﬁnal ground-state
subspace (see text).
Each string s determines a graph
automorphism π(s) via Eq. (26). Each even row associates
each integer string s in the odd row preceding it with a
graph automorphism π(s). They also identify the two strings
that give rise to the graph automorphisms α and β that
generate Aut(W7), and write each graph automorphism π(s)
as a product of an appropriate power of α and β. Note that
e is the identity automorphism, and the product notation
assumes the rightmost factor acts ﬁrst.
s = s0 · · · s6
5012346
4501236
3450126
π(s)
α
α2
α3
s = s0 · · · s6
2345016
1234506
0123456
π(s)
α4
α5
α6 = e
s = s0 · · · s6
1054326
2105436
3210546
π(s)
β
αβ
α2β
s = s0 · · · s6
4321056
5432106
0543216
π(s)
α3β
α4β
α5β
We now show that Aut(W7) is isomorphic to the dihe-
dral group D6 by showing that the graph automorphisms
α = π(5012346) and β = π(1054326) generate Aut(W7),
and satisfy the generator relations (Eq. (27)) for D6. The
second and fourth rows of Table VI establish that α and
β are the generators of Aut(W7) as they show that each
element of Aut(W7) is a product of an appropriate power
of α and β, and that all possible products of powers of α
and β appear in these two rows. Following the discussion
for C4, it is a simple matter to show that α corresponds
to a 60◦clockwise rotation about vertex 6 of W7. Thus
6 applications of α rotates W7 by 360◦which leaves it
invariant. Thus α6 = e which is the ﬁrst of the generator
relations in Eq. (27). Similarly, β can be shown to corre-
spond to a reﬂection of W7 about a vertical axis passing
through vertex 6 of W7. Thus two applications of β leave
W7 invariant. Thus β2 = e which is the second generator
relation in Eq. (27). Finally, using Table VI, direct cal-
culation as in Eqs. (35) and (36) shows that αβ = βα5
which establishes the ﬁnal generator relation in Eq. (27).
We see that α and β generate Aut(W7) and satisfy the
generator relations for D6 and so generate a 12 element
group isomorphic to D6. In summary, we have shown
that the GI AQA found all twelve graph automorphisms
of W7, and that the group formed from these automor-
phisms is isomorphic to the dihedral group D6 which is
the correct automorphism group for W7.
V.
EXPERIMENTAL IMPLEMENTATION
In this section we express the GI problem Hamiltonian
HP in a form more suitable for experimental implemen-
tation. We saw in Section II C that the eigenvalues of HP
are given by the cost function C(s) which is reproduced
here for convenience:
C(s) = C1(s) + C2(s) + C3(s),
(42)
with
C1(s) =
N−1
X
i=0
M
X
α=N
δsi,α
(43)
C2(s) =
N−2
X
i=0
N−1
X
j=i+1
δsi,sj,
(44)
C3(s) = ∥σ(s)AσT (s) −A′∥i.
(45)
Here s = s0 · · · sN−1 is the integer string derived from the
binary string sb = (s0 · · · sU−1) · · · (s(N−1)U · · · sNU−1)
via Eqs. (6) and (7) with U = ⌈log2 N⌉.
The matrix
σ(s) was deﬁned in Eq. (8) as
σi,j(s) =
(
0,
if sj > N −1
δi,sj, if 0 ≤sj ≤N −1.
(46)
Note that σi,j(s) can be written more compactly as
σi,j(s) = δi,sj
M
Y
α=N
 1 −δsj,α

.
(47)
We see from Eqs. (42)–(45) and (47) that the s-
dependence of C(s) enters through the Kronecker deltas.
This type of s-dependence is not well-suited for experi-
mental implementation and so our task is to ﬁnd a more
convenient form for the Kronecker delta.
We begin with δa,b in the case where a, b ∈{0, 1}. Here
we write
δa,b = (a + b −1)2 =
(
0
(a ̸= b)
1
(a = b),
(48)
which can be checked by inserting values for a and b.
Now consider δs,k when s and k are U-bit integers. The
binary decompositions of s and k are
s =
U−1
X
i=0
si (2)i
(49)
k =
U−1
X
i=0
ki (2)i .
(50)
For s and k to be equal, all their corresponding bits must
be equal. Thus we can write
δs,k =
U−1
Y
i=0
δsi,ki
=
U−1
Y
i=0
(si + ki −1)2 =
(
1
(all si = ki)
0
(some si ̸= ki).(51)


---- page 16 ----

16
Eq. (51) allows each Kronecker delta appearing in C(s)
to be converted to a polynomial in the components of
the integer string s. From Eqs. (43) and (44) we see that
C1(s) and C2(s) are each 2U-local. For C3(s) we must
write σ(s)AσT (s) in a form that makes the Kronecker
deltas explicit. Using Eq. (47), we have
σ(s)AσT (s) =
N−1
X
i,j=0
σli(s)Aijσmj(s)
=
N−1
X
i,j=0
(
δl,si
M
Y
α=N
(1 −δsi,α)
)
Aij
×


δm,sj
M
Y
β=N
 1 −δsj,β



. (52)
Inserting Eq. (51) into Eq. (52), we see that σ(s)AσT (s)−
A′ is 4U(M −N + 1)-local. If we use the L1-norm (L2-
norm) in Eq. (45), then we see that C3(s) is 4U(M −N +
1)-local (8U(M −N + 1)-local).
The number of terms in C(s), and thus in HP , follows
straight-forwardly from Eqs. (43)-(45).
Starting with
C1(s), there is a term for each value of i and α that
appears in the sum. There are thus T1 = N(M −N + 1)
terms in C1(s).
From Eq. (5), M = 2U −1, where
U = ⌈log2 N⌉and N is the number of vertices in each
graph appearing in the GI instance. It follows from the
deﬁnition of U that M < 2N and so T1 < N(N +1). Re-
call from Section III that the number of qubits LN needed
for an N-vertex GI instance is LN = N⌈log2 N⌉. Thus
T1 < (LN/⌈log2 N⌉)(LN/⌈log2 N⌉+ 1) < CL2
N, where C
is an appropriate constant. Thus T1(LN) = O(L2
N). A
similar analysis shows that the number of terms in C2(s)
is T2(LN) = O(L2
N). Finally, C3(s) is the Li-norm of
an N × N matrix. For the L1-norm used in our simu-
lations, the number of terms in C3(s) is T3 = N 2. Fol-
lowing the above analysis, this gives T3(LN) = O(L2
N).
Putting everything together gives that the total num-
ber of terms associated with C(s), and so also HP , is
T(LN) = T1(LN)+T2(LN)+T3(LN) = O(L2
N). The ini-
tial Hamiltonian Hi contains one term for each qubit (see
Eq. (15)) and so the number of terms in Hi is LN. Thus
the total number of terms in the full time-dependent
Hamiltonian H(t) is O(L2
N) and so scales quadratically
with the number of qubits LN.
Clearly, the degree of diﬃculty associated with exper-
imentally implementing a quantum algorithm depends
strongly on the architecture of the hardware on which it
is to be run. The simplest situation would be an architec-
ture which allows an arbitrary number of qubits to be si-
multaneously coupled, independently of where they were
located on the processor.
Unfortunately, such a hard-
ware architecture does not presently exist. For hardware
platforms designed to run adiabatic quantum optimiza-
tion algorithms, the D-Wave hardware is furthest along
[29].
Each qubit on the D-Wave processor couples to
at most six neighboring qubits, and only two-qubit Ising
coupling interactions are possible. The initial Hamilto-
nian Hi (see Eq. (15)) is easily programmed onto the
hardware. However, a problem Hamiltonian HP which is
not of Ising form is more challenging, requiring an embed-
ding procedure that: (i) reduces all k-local interactions
with k ≥3 to 2-local form; and (ii) two-qubit coupling in-
teractions that match the hardware’s Chimera coupling-
graph. A procedure for carrying out this reduction based
on Ref. [15] is described in Appendix B. Alternative ap-
proaches appear in Refs. [30] and [31].
VI.
SUBGRAPH ISOMORPHISM PROBLEM
An instance of the SubGraph Isomorphism (SGI) prob-
lem consists of an N-vertex graph G and an n-vertex
graph H with n ≤N.
The question to be answered
is whether G contains an n-vertex subgraph that is iso-
morphic to H. The SGI problem is known to be NP-
Complete [32] and is believed to be more diﬃcult to solve
than the GI problem. Here we show how an instance of
SGI can be converted into an instance of a COP whose
cost function has a minimum value that vanishes when
G contains a subgraph isomorphic to H, and is greater
than zero otherwise. The SGI cost function will be seen
to be a natural generalization of the GI cost function
given in Eqs. (9)–(12). The SGI COP can then be solved
using adiabatic quantum evolution as was done for the
GI problem.
As with the GI problem, we would like to determine
whether there exists an isomorphism π of G that pro-
duces a new graph π(G) that contains H as a subgraph.
Just as with the GI problem, we consider linear maps
σ(s) (see Eqs. (6)–(8)) that transform the adjacency ma-
trix A of G to ˜A(s) = σ(s)AσT (s). We then search π(G)
to determine whether there is a subset of n vertices that
yields a subgraph that is equal to H.
To begin the process of converting an SGI instance into
an instance of a COP, let: (i) α label all the
 N
n

ways
of choosing n vertices from the N vertices in π(G); and
(ii) |i⟩(|αi⟩) be an n-component (N-component) vector
whose i-th (αi-th) component is 1, and all other compo-
nents are 0. Thus α labels the choice (α0, . . . , αn−1) of n
vertices out of the N vertices of π(G). We now show that
an n×N matrix Pα can be used to form an n×n matrix
Aα(s) whose matrix elements are the matrix elements of
˜A(s) associated with the n vertices appearing in α. To
that purpose, deﬁne
Pα =
n−1
X
i=0
|i⟩⟨αi|,
(53)
Aα(s) = Pα ˜A(s)P T
α ,
(54)
where
˜A(s) =
N−1
X
l,m=0
˜Al,m(s)|l⟩⟨m|.
(55)


---- page 17 ----

17
It follows from these deﬁnitions that
Aα(s) =
n−1
X
i,=0
|i⟩⟨αi|
N−1
X
l,m=0
˜Al,m(s)|l⟩⟨m|
n−1
X
j=0
|αj⟩⟨j|
=
n−1
X
i,j=0
˜Aαi,αj(s)|i⟩⟨j|.
(56)
Thus the matrix elements (Aα)i,j(s) are precisely the ma-
trix elements ˜Aαi,αj(s) associated with all possible pairs
of vertices drawn from (α0, . . . , αn−1). The matrix Aα(s)
is thus the adjacency matrix for the subgraph gα com-
posed of the vertices appearing in α, along with all the
edges in π(G) that join them. With Aα(s), we can, as in
the GI problem, test whether gα is equal to H by check-
ing whether ||Aα(s) −A′||i vanishes or not. Here A′ is
the adjacency matrix of the graph H, and ||O||i is the
Li-norm of O.
We can now deﬁne a cost function whose minimum
value vanishes if and only if G contains a subgraph g
that is isomorphic to H.
Because the transformation
σ(s) must be a permutation matrix when g is isomorphic
to H, we again introduce the penalty functions C1(s)
and C2(s) used in the GI COP to penalize those integer
strings s that produce a σ(s) that is not a permutation
matrix:
C1(s) =
N−1
X
i=0
M
X
α=N
δsi,α
(57)
C2(s) =
N−2
X
i=0
N−1
X
j=i+1
δsi,sj.
(58)
The ﬁnal penalty function C3(s) for the SGI problem
generalizes the one used in the GI problem. It is deﬁned
to be
C3(s) =
(
N
n)
Y
α=1
||Aα(s) −A′||i,
(59)
where the product is over all
 N
n

ways of choosing n
vertices out of N vertices. Note that C3(s) vanishes if and
only if G contains an n-vertex subgraph isomorphic to H.
This follows since, if G contains an n-vertex subgraph g
isomorphic to H, there exists a permutation π(s) of G
that has an n-vertex subgraph that is equal to H. Thus,
for this s, there is a choice α of n vertices that gives
a subgraph for which Aα(s) −A′ = 0. It follows from
Eq. (59) that C3(s) = 0. On the other hand, if C3(s) = 0,
it follows that at least one of the factor on the RHS of
Eq. (59) vanishes. Thus there is a choice α of n vertices
for which ||Aα(s) −A′||i = 0. Thus Aα(s) = A′, and so
G has a subgraph isomorphic to H.
The cost function for the SGI problem is now deﬁned
to be
C(s) = C1(s) + C2(s) + C3(s),
(60)
where C1(s), C2(s), and C3(s) are deﬁned in Eqs. (57)–
(59). This gives rise to the following COP:
SubGraph Isomorphism COP: Given an N-vertex
graph G and an n-vertex graph H with n ≤N,
and the associated cost function C(s) deﬁned in
Eq. (60), ﬁnd an integer string s∗that minimizes
C(s).
By construction: (i) C(s∗) = 0 if and only if G contains a
subgraph isomorphic to H, and σ(s∗) is the permutation
matrix that transforms G into a graph π(G) that has H
as a subgraph; and (ii) C(s∗) > 0 otherwise.
As with the GI COP, the SGI COP can be solved using
adiabatic quantum evolution. The quantum algorithm
for SGI begins by preparing the L = N⌈log2 N⌉qubit
register in the ground-state of Hi (see Eq. (15)) and
then driving the qubit register dynamics using the time-
dependent Hamiltonian H(t) = (1 −t/T)Hi + (t/T)HP .
Here the problem Hamiltonian HP is deﬁned to be
diagonal in the computational basis |sb⟩and to have
associated eigenvalues C(s), where s is found from sb
according to Eqs. (6)–(7). At the end of the evolution
the qubits are measured in the computational basis. The
outcome is the bit string s∗
b so that the ﬁnal state of the
register is |s∗
b⟩and its energy is C(s∗), where s∗is the
integer string derived from s∗
b.
In the adiabatic limit,
C(s∗) will be the ground-state energy, and if C(s∗) = 0
( > 0) the algorithm concludes that G contains (does
not contain) a subgraph isomorphic to H. In the case
where G does contain a subgraph isomorphic to H, the
algorithm also returns the permutation π∗= π(s∗) that
converts G to the graph π∗(G) that contains H as a
subgraph. Note that any real application of AQO will
only be approximately adiabatic. Thus the probability
that the ﬁnal energy C(s∗) will be the ground-state
energy will be 1 −ϵ.
In this case the SGI quantum
algorithm must be run k ∼O(ln(1 −δ)/ ln ϵ) times
so that, with probability δ > 1 −ϵ, at least one of
the measurements will return the ground-state energy.
We can make δ arbitrarily close to 1 by choosing k
suﬃciently large.
VII.
SUMMARY
In this paper we have presented a quantum algorithm
that solves arbitrary instances of the Graph Isomor-
phism problem and which provides a novel approach
for ﬁnding the automorphism group of a graph.
We
numerically simulated the algorithm’s quantum dynam-
ics and showed that it correctly: (i) distinguished non-
isomorphic graphs; (ii) recognized isomorphic graphs;
and (iii) determined the automorphism group of a given
graph. We also discussed the quantum algorithm’s exper-
imental implementation, and showed how it can be gener-
alized to give a quantum algorithm that solves arbitrary
instances of the NP-Complete SubGraph Isomorphism


---- page 18 ----

18
problem. As explained in Appendix A, the minimum en-
ergy gap for an adiabatic quantum algorithm largely de-
termines the algorithm’s computational complexity. De-
termining this gap in the limit of large problem size is
currently an important open problem in adiabatic quan-
tum computing (see Section IV). It is thus not possible
to determine the computational complexity of adiabatic
quantum algorithms in general, nor, consequently, of the
speciﬁc adiabatic quantum algorithms presented in this
paper. Adiabatic quantum computing has been shown to
be equivalent to the circuit-model of quantum comput-
ing [12–14], and so development of adiabatic quantum
algorithms continues to be of great interest.
Acknowledgments
We thank W. G. Macready and D. Dahl for many in-
teresting discussions, and F. G. thanks T. Howell III for
continued support.
Appendix A: Quantum adiabatic theorem
The question of how the state of a physical system
changes when the system’s environment undergoes a slow
variation is an old one. For quantum systems, the answer
is contained in the quantum adiabatic theorem which was
proved by Born and Fock not long after the birth of quan-
tum mechanics [33]. Subsequent work relaxed a number
of the assumptions underlying the original proof [34–43],
thereby widening the theorem’s range of validity. As the
physical setting for the quantum adiabatic theorem oc-
curs often, it forms the foundation for many important
applications in atomic, molecular, and chemical physics.
Recently, it has been used as the basis for a novel alter-
native approach to quantum computing known as adi-
abatic quantum computing [21, 22].
In this Appendix
we provide a brief review of the quantum adiabatic the-
orem (Appendix A 1) and then describe how it is used in
adiabatic quantum computing (Appendix A 2).
1.
Quantum adiabatic theorem
Consider a quantum system coupled to an environment
that changes slowly over a time T. The dynamical evolu-
tion of its state |ψ(t)⟩is determined by the Schrodinger
equation, which will be driven by a slowly-varying Hamil-
tonian H(t). The system’s Hilbert space is assumed to
be ﬁnite-dimensional with dimension d. Thus at each in-
stant t there will be d instantaneous energy eigenstates
|Ek(t)⟩satisfying
H(t)|Ek(t)⟩= Ek(t)|Ek(t)⟩,
(A1)
with E0(t) ≤E1(t) ≤· · · ≤Ed−1(t).
Now suppose that we initially prepare the quantum
system in the instantaneous energy eigenstate |Ek(0)⟩of
the initial Hamiltonian H(0).
The quantum adiabatic
theorem states that, in the limit T →∞, the ﬁnal state
|ψ(T)⟩will be (to within a phase factor) the instanta-
neous energy eigenstate |Ek(T)⟩of the ﬁnal Hamiltonian
H(T). Note that in our discussions of adiabatic quantum
computing, the initial state will always be the ground
state of H(0): |ψ(0)⟩= |E0(0)⟩.
For reasons that will become clear below, the energy
gap, ∆(t) = E1(t) −E0(t), separating the two lowest
instantaneous energy-levels proves to be extremely im-
portant in adiabatic quantum computing. Although it
is possible to prove the quantum adiabatic theorem for
systems with a vanishing energy gap [41], the rate of con-
vergence to the adiabatic limit can be arbitrarily slow.
On the other hand, when the gap ∆(t) is non-vanishing
for 0 ≤t ≤T, it is possible to estimate how large T must
be for the dynamics to be eﬀectively adiabatic. Starting
from the observation that for adiabatic dynamics there
will be negligible probability to ﬁnd the quantum system
at t = T in an energy-level other than the ground state,
a straightforward analysis [19, 20] leads to the following
adiabaticity constraint:
T ≫ℏM
∆2 ,
(A2)
where
M =
max
0≤s≤1
⟨E1(s)|d ˜H(s)
ds
|E0(s)⟩
 ,
(A3)
∆=
min
0≤s≤1 [E1(s) −E0(s)] ,
(A4)
s = t/T, and ˜H(s) = H(sT). The quantity ∆is the min-
imum energy gap arising during the adiabatic evolution.
The quantum adiabatic theorem provides a mechanism
for traversing a path |ψ(t)⟩through Hilbert space that
begins at a given state |ψi⟩and ends at a desired ﬁnal
state |ψf⟩. To see this, let Hi and Hf be local Hermi-
tian operators whose ground states are |ψi⟩and |ψf⟩,
respectively. An Hermitian operator is local if it couples
at most k particles, with k ﬁnite. Suppose that we can
apply a time-dependent Hamiltonian H(t) over a time-
interval 0 ≤t ≤T, with H(0) = Hi, and H(T) = Hf.
Suppose further that we prepare our quantum system in
the ground state |ψi⟩of Hi, and then apply H(t) to it. In
the limit T →∞, the quantum adiabatic theorem guar-
antees that the system at time T will be in the desired
state |ψf⟩. The outcome is thus a continuous path from
|ψi⟩to |ψf⟩.
2.
Adiabatic quantum computing
To connect this discussion to quantum computing,
imagine that there is a computational problem we would
like to solve, and that we are able to construct a local
Hamiltonian Hf whose ground state |ψf⟩encodes the so-
lution to our problem. Often, the computational basis


---- page 19 ----

19
states can be chosen to be the eigenstates of HP . Our
GI problem Hamiltonian HP is an example of such a
Hamiltonian (see Section III). Let Hi be a local Hamilto-
nian operator whose ground state |ψi⟩is easy to prepare
(e. g. see Eq. (15)). In adiabatic quantum computing,
the procedure presented in the preceding paragraph is
applied with |ψ(0)⟩= |ψi⟩and H(t) tracing out a path
from Hi to Hf (in the space of Hermitian operators).
Originally, Ref. [21] chose H(t) to linearly interpolate
from Hi to Hf:
H(t) = (1 −t/T) Hi + (t/T) Hf.
(A5)
Writing s = t/T and ˜H(s) = H(sT) gives
˜H(s) = (1 −s) Hi + sHf.
(A6)
More general interpolation schemes are possible: H(t) =
A(t)Hi + B(t)Hf, where we require A(0) = 1 (B(0) =
0) and A(T) = 0 (B(T) = 1).
See, for example,
Refs. [15, 25, 27]. By choosing T suﬃciently large, the ﬁ-
nal state |ψ(T)⟩can be brought arbitrarily close to |ψf⟩.
An appropriate measurement then yields |ψf⟩with prob-
ability close to 1, and thus yields the desired solution to
our computational problem.
Adiabatic quantum com-
puting thus ﬁnds the solution to a computational prob-
lem by homing in on the ground state |ψf⟩of Hf which
encodes the solution. The homing mechanism is provided
by the quantum adiabatic theorem. It has been shown
that adiabatic quantum computing has the same com-
putational power as the circuit model for quantum com-
puting [12–14]. It thus provides an important alternative
approach to quantum computing that is especially well
suited to problems that reduce to quantum state gener-
ation.
We are now in a position to state the protocol for the
adiabatic quantum evolution (AQE) algorithm [21]:
1. Prepare an n-qubit quantum register in the ground
state |ψi⟩of Hi.
2. At t = 0, apply H(t) to the quantum register for a
time T.
3. At time t = T, measure the qubits in the compu-
tational basis.
Because the computational basis states are typically
the eigenstates of Hf, the ﬁnal measurement leaves the
qubits in an eigenstate of Hf.
In the adiabatic limit
T →∞, the ﬁnal measurement leaves the qubits in the
ground-state of Hf (which encodes the solution we are
trying to ﬁnd) with probability Psuccess →1.
Now for large, but ﬁnite T, the Schrodinger dynamics
is approximately adiabatic. Thus, with probability 1−ϵ,
the measurement returns the problem solution. In this
case the AQE algorithm must be run more than once.
Suppose we run it κ times. The probability that we do
not get the problem solution in any of the κ runs is ϵκ.
We can make this probability take an arbitrarily small
value ˜ϵ by choosing κ ∼O(log(1/˜ϵ)). Thus with prob-
ability arbitrarily close to 1, one of the κ measurement
results will yield the problem solution.
The adiabaticity constraint (see Eq. (A2)) speciﬁes
a lower bound which the runtime T must exceed if the
Schrodinger dynamics is to be eﬀectively adiabatic. In
all applications of interest to date, the matrix element
M
appearing in this constraint scales polynomially
with problem size N. So long as this is true, Eq. (A2)
indicates that the scaling behavior of the runtime T(N)
is determined by the scaling behavior of the minimum
gap ∆(N).
Now, if at t = 0 the quantum register is
prepared in the ground state of the initial Hamiltonian
H(0), and its dynamics is eﬀectively adiabatic, its
state at later times will be eﬀectively restricted to the
subspace spanned by the instantaneous ground and ﬁrst
excited states.
Standard arguments [44] indicate that,
in the absence of symmetry, these two energy-levels will
typically not cross. Thus the minimum gap ∆(N) will
typically not vanish, and Eq. (A2) indicates that an ef-
fectively adiabatic dynamics can be obtained with ﬁnite
T(N).
An algorithm, classical or quantum, is said to
eﬃciently (ineﬃciently) solve a computational problem
if its runtime scales polynomially (super-polynomially)
with problem size.
Thus, if ∆(N) scales inverse poly-
nomially (super-polynomially) with N, then T(N) will
scale polynomially (super-polynomially) with N, and
the AQE algorithm will be an eﬃcient (ineﬃcient)
algorithm.
We see that the scaling behavior of the
minimum gap ∆(N) largely controls the computational
complexity of the AQE algorithm.
Appendix B: Embedding Procedure for D-Wave
Hardware
This Appendix brieﬂy describes the embedding pro-
cedure used in Ref. [15] to program a non-Ising problem
Hamiltonian HP onto a D-Wave One processor. The pro-
cessor architecture is shown in Fig. 18. This procedure
also applies to a D-Wave Two processor.
As discussed in Section III, the GI algorithm presented
in this paper constructs HP to: (i) be diagonal in the
computational basis {|a0 · · · aL−1⟩: ai = 0, 1}; and
(ii) have eigenvalues C(a), where a = a0 · · · aL−1, L is
the number of qubits, and C(a) is given by Eqs. (42)-(45)
with s →a.
The cost function C(a) is not yet ready
for experimental implementation for two reasons. First,
there are k-qubit interactions with k > 2 which cannot
be implemented as the processor can only couple pairs
of qubits; and second, two-qubit couplings may not
correspond to available couplings on the processor (see
Fig. 18). Procedures for removing each of these obstacles
are presented, respectively, in Appendices B 1 and B 2.
We summarize these procedures in Appendix B 3.
To
keep the discussion concrete, we examine a single k-qubit
coupling term A = a1 · · · ak with ai = 0, 1. The result-


---- page 20 ----

20
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68
69
70
71
72
73
74
75
76
77
78
79
80
81
82
83
84
85
86
87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126
127
128
FIG. 18: Layout of qubits and couplers for a D-Wave
One processor. The processor architecture is a 4 × 4 array
of unit cells, with each unit cell containing 8 qubits. Within a
unit cell, each of the 4 qubits in the left-hand partition (LHP)
connects to all 4 qubits in the right-hand partition (RHP),
and vice versa.
A qubit in the LHP (RHP) of a unit cell
also connects to the corresponding qubit in the LHP (RHP)
in the units cells above and below (to the left and right of)
it.
Most qubits couple to 6 neighbors.
Qubits are labeled
from 1 to 128, and edges between qubits indicate couplers
which may take programmable values. Grey qubits indicate
usable qubits, while white qubits indicate qubits which, due
to fabrication defects, could not be calibrated to operating
tolerances and were not used.
ing procedure must then be applied to each term in C(a).
1.
Reduction to pairwise coupling
Here we describe how to reduce a k-qubit coupling term
A = a1 · · · ak with ai = 0, 1 to a sum of 2-qubit (viz. pair-
wise) coupling terms.
We ﬁrst show how to reduce a
3-qubit coupling term to pairwise coupling terms (Ap-
pendix B 1 a), and then use lessons learned to reduce the
k-qubit term A to pairwise coupling (Appendix B 1 b).
a.
3-qubit case
We begin by showing how to reduce a 3-qubit coupling
term a1a2a3 to pairwise coupling by introducing: (i) an
ancillary variable b which takes only two values {0, 1};
and (ii) the penalty function
P(a1, a2; b) = a1a2 −2(a1 + a2)b + 3b.
(B1)
Notice that P(a1, a2; b) = 0 (> 0) when the input values
for a1, a2, and b satisfy b = a1a2 (b ̸= a1a2).
Now
consider the quadratic cost function
h(b) = ba3 + µP(a1, a2; b)
for given values of µ, a1, and a2. For µ suﬃciently large,
h(b) is minimized when the value of b satisﬁes the equality
constraint b∗= a1a2. As noted above, for this optimal
value of b, the penalty function P(a1, a2; b∗) = 0, and so
the optimum cost h(b∗) is
h(b∗) = b∗a3 + P(a1, a2; b∗)
= a1a2a3,
where b∗= a1a2 has been used in going from the ﬁrst to
the second line. Thus, for values of b satisfying the equal-
ity constraint b = a1a2, the cost function h(b), which is
a sum of 2-qubit coupling terms, reproduces the 3-qubit
coupling term a1a2a3. By choosing µ suﬃciently large,
values of b that do not satisfy the equality constraint
can be pushed to large cost (viz. energy), making such b
values inaccessible during adiabatic quantum evolution.
b.
k-qubit case
To reduce the k-qubit coupling term A = a1 · · · ak to
pairwise coupling we: (i) introduce ancillary bit vari-
ables b2, · · · , bk−1; and (ii) impose the constraints bk−1 =
ak−1ak and bj = ajbj+1 (j = 2, · · · , k −2) through the
penalty function
P(a; b) = P(ak−1, ak; bk−1) +
k−2
X
j=2
P(aj, bj+1; bj),
where a = (a1, · · · , ak), b = (b2, · · · , bk−1) and P(a, b; c)
is deﬁned in Eq. (B1).
The quadratic cost function
CA(a, b) is deﬁned to be
CA(a, b) = a1b2 + µ P(a; b).


---- page 21 ----

21
We require that the optimal values (a∗, b∗) satisfy the
k −1 imposed constraints so that P(a∗, b∗) = 0. For
optimal values, the cost function evaluates to
CA(a∗, b∗) = a∗
1b∗
2 + µP(a∗, b∗)
= a∗
1a∗
2b∗
3
= ...
= a∗
1 · · · a∗
k−2b∗
k−1
= a∗
1 · a∗
k,
where (in the interests of clarity) we have introduced the
constraints one at a time in going from one line to the
next. Here µ is a penalty weight whose value is chosen
large enough to freeze out non-optimal values of a and b
during adiabatic quantum evolution. Thus, for values of
a and b satisfying the k −1 equality constraints, and for
µ suﬃciently large, the cost function CA(a, b), which is
a sum of 2-qubit coupling terms, reproduces the k-qubit
coupling term A = a1 · · · ak as desired.
2.
Matching required couplings to hardware
couplings
A cost function with only pairwise coupling such as re-
sults from the procedure described in Appendix B 1 may
still not be experimentally realizable on a D-Wave proces-
sor as the pairwise couplings arising in CA(a, b) may not
match the two-qubit couplings available on the proces-
sor. The primal graph of a quadratic cost function such
as CA(a, b) is the graph whose vertices are the qubit vari-
ables, and whose edges indicate pairwise-coupled qubits.
An arbitrary primal graph can be embedded into a suﬃ-
ciently large qubit graph having the structure of Fig. 18.
An embedding maps a primal graph vertex to one or more
vertices in the qubit graph, where the image vertices form
a connected subgraph of the qubit graph. The string of
connected qubits are linked together with strong ferro-
magnetic couplings so that in the lowest energy state,
these qubits have identical Bloch vectors. For example,
to couple qubits 104 and 75 in Fig. 18 (which are not
directly coupled) with coupling strength J , we ferromag-
netically couple qubits 104, 112, and 107 using strongly
negative J104,112 and J107,112 values. Qubits 107 and 75
are directly coupled by the processor and so the desired
coupling J is applied to the edge (viz. coupler J107,75)
connecting qubits 107 and 75: J107,75 = J . The ferro-
magnetic chain thus eﬀects the desired coupling of qubits
104 and 75. This embedding procedure must be carried
out for each pair of primal graph vertices joined by an
edge whose associated qubits are not directly coupled in
the processor architecture.
3.
Summary
By combining the procedures described in this Ap-
pendix it is possible to transform any cost function C(a)
into a quadratic cost function with pairwise couplings
that matches the couplings speciﬁed by the processor ar-
chitecture. The trade-oﬀis the introduction of ancilla
qubits that are needed to reduce the coupling interactions
to pairwise coupling and to match the 2-qubit couplings
available on the processor.
[1] J. K¨obler, U. Sch¨oning, and J. Tor´an, The Graph Iso-
morphism Problem (Birkh¨auser, Boston, 1993).
[2] S. Arora and B. Barak, Computational Complexity (Cam-
bridge University Press, New York, 2009).
[3] R. Jozsa, Computing in Science and Engineering, 3, 34
(2001).
[4] E. Bernstein and U. Vazarani, in Proc. 25th Annual
ACM Symposium on the Theory of Computing, edited
by R. Kosaraju, D. Johnson, and A. Aggarwal (ACM,
San Diego, 1993), p. 11.
[5] C. Moore, A. Russell, and L. J. Schulman, in 46th Annual
IEEE Symposium on Foundations of Computer Science,
edited by E. Tardos (IEEE, Los Alamitos, CA, 2005), p.
479.
[6] V.
Gudkov
and
S.
Nussinov,
arXiv.org:cond-
mat/0209112v2 (2002).
[7] T. Rudolph, arXiv.org:quant-ph/0206068v1 (2002).
[8] S. Shiau, R. Joynt, and S.N. Coppersmith, Quantum Inf.
Compt. 5, 492 (2005).
[9] J. K. Gamble, M. Friesen, D. Zhou, R. Joynt, and S. N.
Coppersmith, Phys. Rev. B 81, 052313 (2010).
[10] K. Rudinger et al., Phys. Rev. A 86, 022334 (2012).
[11] I. Hen and A. P. Young, Phys. Rev. A 86, 042310 (2012).
[12] D. Aharonov, W. Van Dam, J. Kempe, Z. Landau, S.
Lloyd, and O. Regev, SIAM J. Comput. 37, 166 (2007).
[13] J. Kempe, A. Kitaev, and O. Regev, SIAM J. Comput.
35, 1070 (2006).
[14] R. Oliveira and B. Terhal, Quant. Inf. Comp. 8, 900
(2008).
[15] Z. Bian, F. Chudak, W. G. Macready, L. Clark, and F.
Gaitan, Phys. Rev. Lett. 111, 130505 (2013).
[16] G. Chartrand and P. Zhang, A First Course in Graph
Theory (Dover, Mineola, NY 2012).
[17] M. Mosca, in Encyclopedia of Complexity and System
Science, Robert A. Meyers, ed. (Springer, NY 2009),
p. 7088.
[18] D. Aharonov, W. van Dam, J. Kempe, Z. Landau, S.
Lloyd, and O. Regev, 45th Annual IEEE Symposium on
Foundations of Computer Science (FOCS’04), edited by
E. Upfal (IEEE, Los Alamitos, CA, 2004), p. 42.
[19] A. Messiah, Quantum Mechanics, Vol. II (Wiley, NY
1962), p. 750.
[20] Schiﬀ, L. I., 1968, Quantum Mechanics, 3rd Edition
(McGraw-Hill, New York).
[21] E. Farhi, J. Goldstone, S. Gutmann, and M. Sipser,
arXiv:quant-ph/0001116.


---- page 22 ----

22
[22] E. Farhi, J. Goldstone, S. Gutmann, J. Lapan, A. Lund-
gren, and D. Preda, Science 292, 472 (2001).
[23] F. Gaitan, Int. J. Quantum Inform. 4, 843 (2006).
[24] F. Gaitan, Complexity 14, 21 (2009).
[25] F. Gaitan and L. Clark, Phys. Rev. Lett. 108, 010501
(2012).
[26] E. Farhi, J. Goldstone, and S. Gutmann, arXiv:quant-
ph/0208135v1.
[27] J. Roland and N. J. Cerf, Phys. Rev. A 65, 042308 (2002).
[28] D. M. Cvetkovi´c, M. Doob, and H. Sachs, Spectra of
Graphs (Academic Press, New York, 1980).
[29] M. W. Johnson et al., Nature (London) 473, 194 (2011).
[30] R. Babbush, B. O’Gorman, and A. Aspuru-Guzik, Ann.
der Phys. 525, 877 (2013).
[31] J. D. Whitﬁeld, M. Faccin, and J. D. Biamonte, Euro.
Phys. Lett. 99, 57004 (2012).
[32] M. R. Garey and D. S. Johnson, Computers and In-
tractability (W. H. Freeman and Company, New York,
1979).
[33] Born, M. and V. Fock, Z. Phys. 51, 165 (1928).
[34] Kato, T., Phys. Soc. Jap. 5, 435 (1950).
[35] Avron, J. E., R. Seiler, and L. G. Yaﬀe, Commun. Math.
Phys. 110, 33 (1987); (Erratum: Commun. Math. Phys.
153, 649 (1993)).
[36] Nenciu, G., J. Phys. A 13, L15 (1980).
[37] Friedrichs, K. O., 1953, Special Topics in Quantum The-
ory, Lecture notes, Courant Institute of Mathematical
Science, New York University; 1955, On the Adiabatic
Theorem in Quantum Theory, Part I , Courant Institute
of Mathematical Sciences, New York University; 1956,
On the adiabatic theorem in quantum theory, Part II ,
Courant Institute of Mathematical Science, New York
University.
[38] Hagedorn, G., Ann. Phys. 196, 278 (1989).
[39] Avron, J. E., J. S. Howland, and B. Simon, Commun.
Math. Phys. 128, 497 (1990).
[40] Avron, J. E. and A. Elgart, Phys. Rev. A 58, 4300 (1998).
[41] Avron, J. E. and A. Elgart, Commun. Math. Phys. 203,
445 (1999).
[42] Narnhofer, H. and W. Thirring, Phys. Rev. A 26, 3646
(1982).
[43] Martinez, A. and S. Nakamura, C. R. Acd. Sci. Paris
318, 1153 (1994).
[44] Landau, L. D. and E. M. Lifshitz, 1977, Quantum Me-
chanics, 3rd Edition (Butterworth-Heinemann, imprint
of Elsevier Science, New York).

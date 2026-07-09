# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.28.0
# Paper: arXiv:0708.1879 — Giovannetti/Lloyd/Maccone, 'Quantum random access memory'
# Extraction performed 2026-07-06 (Marker not installed on host; see extraction/README.md).


---- page 1 ----

arXiv:0708.1879v2  [quant-ph]  26 Mar 2008
Quantum random access memory
Vittorio Giovannetti1, Seth Lloyd2, Lorenzo Maccone3
1NEST-CNR-INFM & Scuola Normale Superiore, Piazza dei Cavalieri 7, I-56126, Pisa, Italy.
2MIT, RLE and Dept. of Mech. Engin. MIT 3-160, 77 Mass. Av., Cambridge, MA 02139, USA.
3QUIT, Dip. Fisica “A. Volta”, Univ. Pavia, via Bassi 6, I-27100 Pavia, Italy.
A random access memory (RAM) uses n bits to randomly address N = 2n distinct memory cells.
A quantum random access memory (qRAM) uses n qubits to address any quantum superposition
of N memory cells. We present an architecture that exponentially reduces the requirements for a
memory call: O(log N) switches need be thrown instead of the N used in conventional (classical
or quantum) RAM designs. This yields a more robust qRAM algorithm, as it in general requires
entanglement among exponentially less gates, and leads to an exponential decrease in the power
needed for addressing. A quantum optical implementation is presented.
PACS numbers: 03.67.Lx,03.65.Ud,03.67.-a
A fundamental ability of any computing device is the
capacity to store information in an array of memory
cells [1]. The most ﬂexible architecture for memory ar-
rays is random access memory, or RAM, in which any
memory cell can be addressed at will [2].
A RAM is
composed of a memory array, an input register (“address
register”), and an output register. Each cell of the array
is associated with a unique numerical address. When the
address register is initialized with the address of a mem-
ory cell, the content of the cell is returned at the output
register (“decoding”). Just as RAM forms an essential
component of classical computers, quantum random ac-
cess memory, qRAM, will make up an essential compo-
nent of quantum computers, should large quantum com-
puters eventually be built. It has the same three basic
components as the RAM, but the address and output
registers are composed of qubits (quantum bits) instead
of bits. [The memory array can be either quantum or
classical, depending on the qRAM’s usage]. The qRAM
can then perform memory accesses in coherent quantum
superposition [3]: if the quantum computer needs to ac-
cess a superposition of memory cells, the address register
a must contain a superposition of addresses P
j ψj|j⟩a,
and the qRAM will return a superposition of data in a
data register d, correlated with the address register:
X
j
ψj|j⟩a
qRAM
−→
X
j
ψj|j⟩a|Dj⟩d ,
(1)
where Dj is the content of the jth memory cell. The pos-
sibility of eﬃciently implementing these devices would
yield an exponential speedup for pattern recognition al-
gorithms [4, 5, 6], period ﬁnding, discrete logarithm
and quantum Fourier transform algorithms over classical
data. Moreover, qRAMs are required for the implemen-
tation of various algorithms, such as quantum searching
on a classical database [3], collision ﬁnding [7], element-
distinctness in the classical [8] and quantum [9] settings,
and the quantum algorithm for the evaluation of general
NAND trees [10]. Finally, qRAMs permit the introduc-
tion of new quantum computation primitives, such as
quantum cryptographic database searches [11] or the co-
herent routing of signals through a quantum network of
quantum computers [12].
Both classical and quantum RAMs are computation-
ally expensive:
If the memory array is disposed in a
d-dimensional lattice, conventional architectures involve
throwing O(N 1/d) switches (i.e. two-body interactions)
to access one out of the N = 2n memory slots, where n is
the number of bits in the address register [2]. This expo-
nential use of resources translates into a relatively slow
speed and high energy usage for classical RAMs during
decoding, and to a high decoherence rate for qRAMs.
For this reason, up to now little attention has been de-
voted to developing a qRAM. In this paper we introduce
a new RAM architecture, dubbed “bucket-brigade,” that
reduces the number of switches that must be thrown dur-
ing a RAM call, quantum or classical, from O(N 1/d) to
O(log N).
If we neglect the travel time of the signals
along the wires connecting the device’s components, this
translates into an exponential reduction in the running-
time computational-complexity at the information theo-
retical level, when compared to conventional setups. As
will be shown, for qRAMs it entails an exponential reduc-
tion in the number of gates that need to be entangled for
each memory call, simplifying the qRAM circuit with re-
spect to the conventional architectures [3], and reducing
the need for expensive error correction routines. In addi-
tion, the reduction in the number of switchings translates
into a reduction of the energy employed in the routing,
which may yield more eﬃcient RAMs that use less power
during decoding than current architectures.
We start by describing the conventional RAM architec-
ture, showing why its direct translation to the quantum
realm is ineﬃcient and noise-prone. We then introduce
our bucket-brigade architecture and give an account of
the required resources in the classical and quantum set-
ting. We conclude introducing an illustrative example.
Quantum RAM
Even though more elaborate archi-
tectures exist [2] (such as ones using d-dimensional mem-
ory arrays), the basic RAM addressing scheme is simple:


---- page 2 ----

2
graph levels
0
1
2
3
4
root node
FIG. 1: Bifurcation graph of the RAM addressing.
Suppose that the N memory cells are placed at the end
of a bifurcation graph, composed by the n levels shown
in Fig. 1. The value of the jth bit in the address reg-
ister can be interpreted as the route to follow when one
has reached a node in the jth level of the graph: if the
value is 0, the left path must be followed; if it is 1, the
right path must be followed (e.g. an address register 010..
is interpreted as ‘left at the 0th level, right at the ﬁrst
level, left at the second’, etc.).
Each of the N possi-
ble values of the address register thus indicates a unique
route that crosses the whole graph and reaches one of the
memory cells [13]. An electronic implementation requires
placing one transistor in each of the two paths following
each node in the graph. Each address bit controls all the
transistors in one of the graph levels: it activates all the
transistors in the left paths if it has value 0, or all the
transistors in the right paths if it has value 1 [2]. Thus, an
exponential number of transistors must be activated at
each memory call to route the signals through the graph
(this entails an energy cost exponentially larger than the
cost of a single transistor activation.)
Direct translations of the above scheme into the quan-
tum realm [3] are quite impractical.
The n qubits of
the address register coherently control n quantum con-
trol lines, each of which acts coherently on an entire level
of the bifurcation graph. At each branch of the bifur-
cation graph, a 0 in the address register for that level
shunts signals along the left paths, and a 1 shunts sig-
nals along the right paths. Each binary address is cor-
related with a set of switches that pick out the unique
path through the graph associated with that address. A
coherent superposition of addresses is coherently corre-
lated, i.e. entangled, with a set of switches that pick out
a superposition of paths through the graph.
To com-
plete the quantum memory call, a quantum ‘bus’ is in-
jected at the root node and follows the superposition of
paths through the graph. Then the internal state of the
bus is changed according to the quantum information in
the memory slot at the end of the paths (e.g. through
a controlled-NOT transformation that correlates the bus
and the memory) [14]. Finally, in order to decorrelate the
bus position from the address register, the bus returns to
the root node by the same path. Like a quantum parti-
cle, the bus must be capable of traveling down a coherent
superposition of paths. Although not impossible, such a
qRAM scheme is highly demanding in practice for any
reasonably sized memory. In fact, to query a superposi-
tion of memory cells, the address qubits are in general en-
tangled with O(N) switches or quantum gates (or, equiv-
alently, they must control two-body interactions over ex-
ponentially large regions of space), i.e.
a state of the
form P
j ψj |j0j1 · · · jn−1⟩a ⊗|j0⟩s0|j1⟩⊗2
s1 · · · |jn−1⟩⊗2n−1
sn−1 ,
where jk is the kth bit of the address register, and sk is
the state of the 2k switches controlled by it. Such a gi-
gantic superposition is highly susceptible to decoherence
and requires costly quantum error correction whenever
the error rate is bigger than 2−n. In fact, if a single gate
out of the N = 2n gates in the array is decohered, then
the ﬁdelity of the state in average is reduced by a factor
of two, and if at least one gate in each of the k lines is
decohered, the ﬁdelity in average is reduced by 2−k.
The “bucket-brigade” is based on sending both the
address register and the signal through the bifurcation
graph.
Like buckets of water passed along a line of
improvised ﬁre-ﬁghters, they carve a route that crosses
the whole graph along which the information can be ex-
tracted. With respect to the conventional architecture
detailed above, the O(N) active logic gates are replaced
by memory elements, most of which are in a passive
wait state during each memory call. As a result, there
is an exponential reduction of active gates and of two-
body interactions, from O(N) to O(log2 N). This means
the bucket-brigade RAM could also be useful in classi-
cal computation to reduce the energy needed for the ad-
dressing. (Hybrid schemes that combine the two above
architectures might be more generally useful).
The basic idea follows. At each node of the graph of
Fig. 1 there is a trit, a three-level memory element. The
trit’s three levels are labeled wait, left, and right. A
trit in the level wait will change its value according to
the value of any incoming bit: if the incoming bit is 0,
it takes the value left, while if the incoming bit is 1, it
takes the value right. A trit in the level left or right will
deviate any incoming signal along the graph according to
its value. The protocol starts by initializing all the trits in
the state wait. Then the ﬁrst bit of the address register
is sent through the graph.
It will induce a change in
the root node, which will be transferred to left or right
depending on the bit’s value. Now the second bit of the
address register is sent through the graph. Depending on
the value of the ﬁrst node, it will be deviated left or right
and will meet one of the two nodes on the second level of
the graph (both of which are in a wait state). This node
will be transformed according to the bit’s value, and so
on. After all the log N bits of the address register have
passed through the graph, a single route of n = log N
left-right trit states has been carved through the graph
(see Fig. 2). All other trits remain in the wait state. Now
a bus signal can easily follow this route (by heeding the
indications of the trits it encounters) and ﬁnd its way to
the element in the memory array that the address register
was pointing to. Information is then extracted through
this route by sending back the bus signal, which must
again heed the directions of the trits it encounters while


---- page 3 ----

3
traveling to the graph’s root node.
In addition, every
time the bus signal on its way back encounters a trit, the
trit is reset to the wait state. Thus, the memory element
is addressed by the bus signal, which is then sent back to
the root node, and the graph is reset to its initial wait
state. Only log N trits have been involved in the memory
call.
memory cells
wait
wait
wait
wait
right
left
left
FIG. 2: Bifurcation graph of the bucket-brigade architecture.
Here the third memory cell is addressed (address register 010).
In the quantum realm the trits must be replaced by
qutrits, i.e. three-level quantum systems, described by
the vectors |wait⟩, |left⟩, and |right⟩. Now, when the
qubits of the address register are sent through the graph,
at each node they encounter a unitary encoding trans-
formation U. If the qutrit is initially in the |wait⟩state,
the unitary swaps the state of the qubit in the two |left⟩-
|right⟩levels of the qutrit (i.e. U|0⟩|wait⟩= |f⟩|left⟩
and U|1⟩|wait⟩= |f⟩|right⟩, where |f⟩is a ﬁduciary state
of the qubit). If the qutrit is not in the |wait⟩state, then
it simply routes the incoming qubit according to its state.
It is clear that an address register in a quantum super-
position will carve a superposition of routes through the
graph, so that any incoming qubit will exit the graph
in the corresponding superposition of locations. Once all
the register qubits are sent through the graph, a bus qubit
is injected and it reaches the end of the graph along the
requested superposition of paths. It then interacts with
the memory cells at such locations changing its state ac-
cording to their information content. Now the bus qubit
is sent back through the graph, exiting at the graph’s
root node.
Finally, starting from the last level of the
graph, the qutrits are subject to the inverse of the unitary
encoding transformation: a qutrit initially in the states
|left⟩or |right⟩is evolved back to the state |wait⟩, while
sending a qubit (containing the state of the |left⟩-|right⟩
levels) back through the graph, i.e. the transformation
U †|f⟩|left⟩= |0⟩|wait⟩or U †|f⟩|right⟩= |1⟩|wait⟩. In
order to activate this transformation at the right mo-
ment, various schemes are possible.
The simplest one
entails activating a classical control over all the qutrits
in each level of the tree, sequentially from the last level
up to the root node. Alternatively, one can send n con-
trol qubits along the superposed path, each of which con-
trols the unitary U † at one of the tree levels. A further
scheme entails introducing counters in each node, which
activate the U † unitary after a level-dependent number
of signals have transited. At the end, all qubits of the
address register have been ejected from the graph, which
is restored to its initial state of all qutrits in the |wait⟩
state, yielding the transformation of Eq. (1).
Similarly to what happens in quantum computation
with atomic ensembles [20], the noise resilience of the
bucket-brigade stems from the fact that in each branch
of the superposition only log N qutrits are not in the
passive |wait⟩state. In fact, for a query with a superpo-
sition of r memory cells, it is necessary to entangle only
O(r log N) qutrits, as the state of the device is of the
type P
j ψj|j0⟩t0|j1⟩t1(j0) · · · |jn−1⟩tn−1(jn−2)⊗ℓj |wait⟩tℓj ,
where tk represents the state of the one qutrit at the kth
level which is aimed to by the non-wait qutrit at the k−1
level, and where ℓj spans the other qutrits. Even if all of
the qutrits are involved in the superposition, the state is
still highly resilient to noise: if a fraction ǫ of the gates
are decohered (with ǫ log N < 1) then in average the ﬁ-
delity of the resulting state is O(1−ǫ log N) (compare this
to the 1/2 ﬁdelity reduction in the conventional qRAM
above). The noise resilience is, of course, greater in those
algorithms where r is small, such as the QPQ [11] or the
quantum routing [12]. Moreover, note that the exponen-
tially larger number of |wait⟩states could give signiﬁcant
overall errors even if their individual error rates are much
lower than those used in the left and right states.
Bucket-brigade
implementation
Like
cluster
state
quantum computation [15], the bucket-brigade only as-
sumes the possibility of operating coherently on a small
number O(log N) out of large number O(N) of ﬁrst-
neighbor connected quantum memory elements, and it
does not require macroscopic superposition states com-
posed of an exponentially large number of quantum gates.
Candidate systems for bucket-brigade qRAMs include
optical lattices [16, 17], Josephson arrays [18], arrays of
coherently coupled quantum dots, or strongly correlated
cavity arrays [19]. In order to be more speciﬁc on the
nature of the necessary resources, we present a proof-of-
principle implementation of the quantum bucket-brigade.
(It should be only considered as an illustrative exam-
ple, and not as an experimental proposal. More detailed
versions of bucket-brigade implementations will be pre-
sented in future work.) The qutrits at the nodes of the
graph of Fig. 1 are composed of trapped atoms or ions
with the level structure depicted in Fig. 3: a ground state
|wait⟩and two excited states |left⟩and |right⟩.
The
register and bus qubits are composed by photons, whose
encoding is in the polarization.
It is now possible to
use a photon in the polarization state |0⟩to muster a
|wait⟩→|left⟩atomic transition, and a photon in the
polarization state |1⟩to muster a |wait⟩→|right⟩transi-
tion. Furthermore by employing Raman techniques, one
use strong classical pulses that couple |wait⟩, |left⟩and
|right⟩with extra energy levels (not shown in the pic-
ture) to externally control the timing of such transitions.
Note that, being classical, such pulses do not need to act
locally on a single atom but they can interact with all


---- page 4 ----

4
the nodes of each level. Thus, a photon impinging on
an atom in the |wait⟩state transfers its internal state
to the |left⟩-|right⟩atomic levels. A photon impinging
on an atom which is in a |left⟩state, will excite a cyclic
transition (using the level |left′⟩) and is re-emitted by
the atom. The |left⟩→|left′⟩transition is insensitive
to the photon’s polarization and is coupled to an out-
going spatial mode departing the trapped atom in the
left direction. This means that a photon in any polar-
ization state that impinges onto an atom in the |left⟩
state is deviated along the graph towards the left. Anal-
ogously, a photon in any state impinging on an atom in
the |right⟩state is deviated towards the right.
As in
the |wait⟩→|left, right⟩transition, the timing of the
whole process can be controlled by coupling the involved
states with ancillary levels through strong classical Ra-
man pulses. After all the photons of the address register
are sent through the graph, a bus photon (initially in the
state |0⟩) is injected. Thanks to the above mechanism,
it crosses the graph in a coherent superposition of paths,
exiting at the location of the addressed cells and changing
its polarization state according to their memory content.
It is then reﬂected back through the graph and is again
deﬂected interacting with the atoms, so that it exits the
graph at the root node. To end the protocol, the Raman
process is inverted, step by step, starting from the last
level in the graph, so that the atomic levels |left⟩and
|right⟩are driven to the |wait⟩level, through the emis-
sion of a |0⟩or |1⟩photon respectively. Thus the address
register photons are emitted one-by-one and coherently
driven back through the graph to the root node.
|1⟩
|0⟩
|left⟩
|right⟩
|left′⟩
|right′⟩
|wait⟩
FIG. 3: Basic level structure of the atoms in a possible bucket-
brigade implementation. Some extra energy levels needed to
implement Raman transitions are not shown.
Conclusions
We have described a RAM architecture
where active gates are replaced by three-level memory
elements. It could give rise to a signiﬁcant simpliﬁcation
in the qRAM implementation, to exponentially reduced
decoherence rate and energy saving.
However, in cur-
rent RAMs, the primary sources of dissipation are leakage
current in the memory cells (for SRAMs) and refreshing
memory cells (for DRAMs). Energy costs in the mem-
ory access procedure are not currently important enough
to warrant accepting the additional delays and memory
elements of the bucket-brigade. For future, non-CMOS
RAMS, however, decoding energy costs may become im-
portant, so that the exponential savings of the bucket-
brigade architecture may prove signiﬁcant.
We acknowledge useful feedback from A. Childs and
support from Jeﬀrey Epstein.
[1] R.
Feynman,
Feynman
Lectures
on
Computation,
(Perseus Books Group, 2000).
[2] R. C. Jaeger, T. N. Blalock, Microelectronic circuit de-
sign, (McGraw-Hill, Dubuque, 2003), pg. 545
[3] M. A. Nielsen and I. L. Chuang, Quantum Computa-
tion and Quantum Information (Cambridge Univ. Press,
Cambridge, 2000).
[4] G. Schaller and R. Sch¨utzhold, Phys. Rev. A 74, 012303
(2006).
[5] R. Sch¨utzhold, Phys. Rev. A 67, 062311 (2003).
[6] C. A. Trugenberger, Phys. Rev. Lett. 87, 067901 (2001);
ibid. 89, 277903 (2002).
[7] G. Brassard, P. Høyer, and A. Tapp, ACM SIGACT
News (Cryptology Column), 28, 14 (1997).
[8] A. Ambainis, Proc. 45th IEEE FOCS’04, pg. 22 (2004),
preprint quant-ph/0311001.
[9] A. M. Childs, A. W. Harrow, and P. Wocjan, Proc. 24th
Symposium on Theoretical Aspects of Computer Science
(STACS 2007), Lecture Notes in Computer Science 4393,
598 (2007), preprint quant-ph/0609110.
[10] A. M. Childs et al., to be published in Proc. 48th
IEEE Symposium on Foundations of Computer Science
(FOCS’07), preprint quant-ph/0703015.
[11] V. Giovannetti, S. Lloyd, and L. Maccone, preprint
quant-ph/0708.2992 (2007).
[12] V. Giovannetti, S. Lloyd, and L. Maccone, unpublished.
[13] The d-dimensional RAM consists of d such graphs, each
addressing one side of a N 1/d × N 1/d × · · · array.
[14] We focus on the case in which we “read” from the mem-
ory, the “write” operation being completely analogous.
[15] R. Raussendorf and H. J. Briegel, Phys. Rev. Lett. 86,
5188 (2001).
[16] E. Jan´e et al., Quantum Inf. Comput. 3, 15-37 (2003).
[17] L.-M. Duan, E. Demler, and M. D. Lukin, Phys. Rev.
Lett. 91, 090402 (2003).
[18] A. Romito, R. Fazio, and C. Bruder, Phys. Rev. B 71,
100501(R) (2005).
[19] M. J. Hartmann, F. G. S. L. Brand, and M. B. Plenio,
Nature Physics 2, 849-855 (2006).
[20] C. W. Chou et al., Nature 438, 828 (2005); J. F. Sherson
et al., Nature 443, 557 (2006).

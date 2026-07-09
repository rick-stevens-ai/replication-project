# Implementation of the Quantum Fourier Transform

Extracted via MarkItDown (fallback stand-in for Marker; Marker + Nougat GPU stacks not installed locally at replication time — see report/failure_analysis.md).

---

9
9
9
1

n
u
J

6
1

1
v
9
5
0
6
0
9
9
/
h
p
-
t
n
a
u
q
:
v
i
X
r
a

Implementation of the Quantum Fourier Transform

Yaakov S. Weinstein∗, Seth Lloyd∗♯, David G. Cory
†

∗

d’Arbeloﬀ Laboratory for Information Systems and Technology
Department of Mechanical Engineering, M.I.T., Cambridge, MA 02139
Department of Nuclear Engineering, M.I.T Cambridge, MA 02139
†
♯Author to whom correspondence should be addressed

November 26, 2024

Abstract

The quantum Fourier transform has been implemented on a three bit nuclear magnetic resonance
(NMR) quantum computer, providing a ﬁrst step towards the realization of Shor’s factoring and
other quantum algorithms. Implementation of the QFT is presented with ﬁdelity measures, and
state tomography. Experimentally realizing the QFT is a clear demonstration of NMR’s ability to
control quantum systems.

PACS numbers 03.67.-a, 03.67.Lx, 02.70.-c, 89.70.+c

Quantum computers are devices that process
information in a way that preserves quantum co-
herence. Unlike a classical bit, a quantum bit,
or ‘qubit,’ can be in a superposition of 0 and
1 at once. This nonclassical feature of quan-
tum information allows quantum computers to
perform some computations faster than classical
computers. For example, quantum computers,
if constructed, could factor large numbers more
rapidly [1], search data basis more quickly [2],
and simulate quantum systems more eﬃciently
[3] than is possible using current classical algo-
rithms [4] [5] [6] [7] [8] [9] [10] [11].

A key subroutine of algorithms for factor-

ing and simulation [12] [13] [14] is the quan-
tum Fourier transform (QFT) [15] [16] [17]. In
essence the QFT takes a ‘position’ state
to
x
|
i
and is
the corresponding ‘momentum’ state
deﬁned as follows:

p
|

i

x
QF Tq|

i →

1
√q

q−1

Xp=0

e2πiap/q

p
|

.
i

(1)

Where q is the dimension of the systems Hilbert
space.

In general the QF Tq transforms the input am-

plitudes as,

QF Tq

x
f (x)
|

i →

˜f (p)
p
|

.
i

p
X

x
X

(2)

1

Where the coeﬃcients ˜f (p) are

To implement the QFT, these gates,

˜f (p) =

1
√q

e2πiap/qf (x).

(3)

a
X
For example, the two qubit QFT corresponds to
the unitary operator,

QF T4 =

1
1
1
1

1
2








1
i
1
i

−
−

1
1
−
1
1

−

1
i
−
1
−
i



.

(4)






This operator shows the QFT separating the in-
put states by 0 degrees in the ﬁrst row and col-
umn, and then by 90 degrees, 180 degrees and
270 degrees, multiples of π
2 .

Equation (4) shows that the QFT has eﬀects
similar to that of the classical Fourier transform.
In particular, if f (a) is periodic with period r,
then ˜f (c) will exhibit a spike at c = r. This is the
key to Shor’s algorithm which allows a quantum
computer to factor very large numbers in poly-
nomial time. The classical Fourier transform re-
veals the periodicity in functions, the QFT re-
veals periodicity of wavefunctions.

As formulated by Coppersmith, the QFT can
be constructed from two basic unitary opera-
tions, Aj, operating on the jth qubit

Aj =

1
√2

1
1

1
1 !

−

and Bjk operating on the jth and kth qubits

Bjk = 




where θjk = π/2k−j.

1 0 0
0
0 1 0
0
0 0 1
0
0 0 0 eiθjk



,






(5)

(6)

2

Bj,j+1Bj,j+2...Bj,L−1Aj

(7)

−

1. Re-
are implemented on the lead bit, j = L
peating the above sequence of gates to all L bits
as j is indexed from L
1 to 0 will complete the
−
QFT. This sequence of quantum logic gates can
be realized NMR. The idea of using nuclear spins
as the basic unit of a quantum computer was
proposed by Lloyd [18], and detailed schemes for
using NMR as a method of quantum computing
were proposed by Cory et al [19] and Gershen-
feld and Chuang [20].
In NMR a series of ra-
dio frequency pulses are used to control the ex-
cess magnetization of an ensemble of quantum
states. NMR experiments are easily visualized
by picturing the excess magnetization as a vec-
tor pointing in some direction and the pulses as
rotations about the various axes. In addition, a
bilinear coupling term in the Hamiltonian allows
for quantum superposition.

The Hamiltonian of a three spin (qubit) NMR

sample with J-coupling is

H =

ω1I z
1 I z

1 + ω2I z
2 + J1,3I z

2 + ω3I z
1 I z

3 +
3 + J2,3I z

2 I z
3 )

2π(J1,2I z

(8)

where Ii = σi/2. The three bit QFT was im-
plemented via NMR using the three carbon-13
spins of an alanine sample. The resonant fre-
quency of carbon-13 at 9.4 Tesla is approxi-
mately 100.617MHz. The carbonyl was labeled
spin 1, Cα was labeled spin 2, and Cβ spin 3. The
chemical shift of the three alanine carbons are
12587Hz, 0Hz, and -3435Hz respectively. Cou-
pling constants between the three spins are J12
= 54Hz, J23 = 35Hz, and J13 = 1.2Hz. Relax-
ation time T1 for alanine is approximately 1.56s
while T2 is about 420ms.

The Aj matrix described above can be broken
E− + σx(E+ + E−).

up into idempotents E+ −

The pulse sequence of the Aj gate can now be de-
termined using the geometric algebra formalism
[21],

π
2

j

(cid:18)

(9)

y −

Aj =

(π)j
x .

π
2 (cid:19)
This pulse program reads: apply a pulse along
the y-axis that rotates spin j 90 degrees, apply a
pulse along the x-axis that rotates j 180 degrees.
Magnetization on the z-axis would be rotated to
the positive x-axis. Since this experiment starts
with the spins at thermal equilibrium (pointing
along the z-axis) the above sequence for the Aj
gate can be replaced by the simpler π
2 pulse along
the positive y-axis.

The Bjk gate, which can be constructed using
the coupling between qubits, In terms of idempo-
2. Again
1E−
tents reduces to 1
using geometric algebra this yields the following
pulse sequence:

2+eiθE−

1E−

E−

−

(π)j

φ −

Bjk =

θ
2πJjk

(π)j
φ

−

(cid:17)

(10)

(cid:16)

θ
2

j,k

x −

π
2

j,k
y −
(cid:1)

π
2

j,k
−y .
(cid:1)

(cid:0)

(cid:0)

(cid:17)

(cid:16)
The notation θ/2πJjk represents an interval of
spin evolution under the coupling Hamiltonian.
The ﬁnal three pulses eﬀectively perform a ro-
tation around the z-axis. These pulses are not
necessary, however, since the same eﬀect may be
achieved by rotating the prior pulses of the ex-
periment.

The complete pulse program is the combina-
tion of Aj and Bjk gates described above.
In
this implementation, the necessity of performing
a swap gate has been removed by reordering the
bits at the appropriate interval.

The complete pulse program is,

3

QF T3 =

8 )x+cos( 3π

8 )y −

(π)2
x

1
−sin( 3π
(cid:1)

(π)3

x −

−

1
8J12

(π)2

−x

−

(cid:17)

(cid:0)
1
8J12

(cid:16)

π
2

(cid:17)
2
x+y
√2 −
−

(cid:16)
1
16J13

(cid:1)

(cid:0)
1
16J13

(cid:16)

(cid:17)

−

(cid:16)

(π)2

−x −

1
8J23

(π)2

x −

−

(cid:16)
(π)1

(cid:16)

(cid:17)
(π)3
−x −

(π)2

x −

π
2

(cid:0)

(π)2

x −

−

(cid:17)

(11)

1
8J23

(π)1

x −

−

(cid:17)

(π)2

−x −

(π)2

−x .

−x −

3
y −
(cid:1)

This sequence includes a number of (π) pulses
to refocus couplings during the intervals they
should be inactive.

The pulse sequence takes advantage of knowl-
edge of the starting state of the system at the
beginning and end of the program by replacing
Hadamard transforms with π
2 pulses. In the mid-
dle of the sequence the full Hadamard was indeed
used.

Figure 1 shows selected theoretical and exper-
imental spectra following the quantum Fourier
transform of the state I 1
z on the three
qubit NMR quantum computer.

z + I 2

z + I 3

The ﬁdelity of the QFT calculated using the

measure

F =

1
2

+

1
2

T r(ρtheoryρexp)

T r(ρ2

theory)

T r(ρ2

exp)

(12)

q

q

is 87%. Here ρ is the density matrix minus
the part that is proportional to the identity (in
NMR, this is called the ‘reduced’ density ma-
trix; it should not be confused with the reduced
density matrix got by partially tracing the den-
sity matrix for a composite quantum system over

A

B

C

200

150

100

50

0

−50

200

150

100

50

0

−50

200

150

100

50

0

−50

−100

200

300

400

500

−100

700

800

900

1000 1100

−100

2450 2500 2550 2600 2650

3

2

1

0

−1

x 108

x 108

3

2

1

0

x 108

3

2

1

0

3.38

3.4

3.42

−1

8.3

8.32

8.34

8.36

8.38

−1

9.68

9.69

9.7

x 104

x 104

9.71
x 104

Figure 1: The three carbon-13 atoms of alanine
after performance of the QFT. The top spectra
are theoretical while the bottom are experimen-
tal. Peaks in NMR spectra show the diﬀerence
in energy level of single spin ﬂips. Each spin has
four peaks since its energy level is dependent on
whether the other two spins are up (along the
magnet) or down. This shows up clearly in spin
B which has resolved J-couples to both of the
other spins. The J-coupling between the A and
C spins is very small and, therefore, the four
peaks are not totally resolved. These peaks tell
the magnitude of only some of the terms of the
density matrix.

some of its subsystems). This measure reﬂects
both imperfections in the applied pulses and de-
lays, as well as decoherence. To a ﬁrst approx-
imation, decoherence during the course of the
QFT attenuates the entire density matrix. This
is shown in ﬁgure 2. Therefore, we can approxi-
mately separate the errors caused by experimen-
tal imperfections by renormalizing ρexp to its at-
tenuated average. Using this the ﬁdelity of the
operations themselves is above 98% over the 6
gates in (11).

The ﬁdelity of 87% corresponds to an error
rate of 97.7% over the six gates which, while
high, does not attain the error rate of 10−4
required for robust quantum computation [22].
These errors arise primarily from spatial inho-
mogeneities in the radio frequency ﬁelds which
we believe can be improved.

In conclusion, using NMR, the QFT has been
implemented on a three bit quantum system and
the ﬁdelity with which we can transform an ini-
tially diagonal state has been measured. Al-
though the ﬁdelity does not reach that required
for fault tolerant computing,
it is easily high
enough to permit studies on small quantum sys-
tems including quantum simulations. A particu-
larly straightforward use of the QFT is in quan-
tum chaos: as Balazs and Voros [23] pointed out,
a simple version of the quantum baker’s map
can be performed by QFTs and Schack [24] has
shown how such a quantum map might be real-
ized on a quantum computer [25].

The authors thank S. S. Somaroo and C. H.
Tseng for helpful discussions. This work was
supported by DARPA.

References

4

4

2

0

4

2

0

4

2

0

1

2

3

4

5

6

7

8

1

2

3

4

5

6

7

8

1

2

3

4

5

6

7

8

2

0

−2

2

0

−2

2

0

−2

1

2

3

4

5

6

7

8

1

2

3

4

5

6

7

8

1

2

3

4

5

6

7

8

Figure 2: Theoretical and experimental results
of the ﬁnal density matrix after implementation
of the QFT on a thermal state. The left column
shows (from top to bottom) the theoretical, ex-
perimental and diﬀerence of the real components
of the three spin density matrix. The right col-
umn shows the same for the imaginary terms.
To read all the terms of the density matrix it
is necessary to rotate them into single spin sin-
gle quantum terms. The diagonal of the density
matrix can be seen running horizontally from the
left corner to the right corner, the magnitude of
all terms on the diagonal being zero. The states
are labeled from
at the left and count up
to

at the back and front corners.

000
i
|

111
i
|

[1] P. W. Shor, Polynomial-Time Algorithms
for Prime Factorization and Discrete Log-
arithms on a Quantum Computer, Siam.
J. Comput. 26 1484-1509 (1997), quant-
ph/9508027.

[2] L. Grover, Proceedings, 28th Annual ACM
Symposium on the Theory of Computing
(STOC), May 1996, pages 212-219.

[3] S. Lloyd, Universal Quantum Simulators,

Science, 273, 23 Aug. 1996.

[4] P. Benioﬀ, J. Stat. Phys. 22, 563, 1980.

[5] R. P. Feynman, Simulating Physics with
Computers, International Journal of Theo-
retical Physics, 21, Nos. 6/7, 1982.

[6] D. Deutsch, Quantum theory, the Church-
Turing principle and the universal quantum
computer, Proc. R. Soc. Lond. A 400, 97-
117 (1985).

[7] A. Steane, Rept. Prog. Phys. 61, 117-173

(1998).

[8] D. P. DiVincenzo, Two-Bit Gates are Uni-
for Quantum Computation, Phys.

versal
Rev. A 51, 1015 (1995).

[9] For an in depth discussion of quantum
computing see lecture notes of J. Preskill
http://www.caltech.edu/subpages/pmares.
html.

[10] D. S. Abrams, and S. Lloyd, Simulations
of many-body Fermi systems on a univer-
sal quantum computer, Phys. Rev. Lett. 79
(1997).

[11] S. S. Somaroo, et al, Quantum Simula-
tions on a Quantum Computer, quant-
ph/9905045.

5

[23] N. L. Balazs and A. Voros, The Quantized
Baker’s Transformation, Ann. of Phys.,
190, (1989).

[24] R. Schack, Using a Quantum Computer to
Investigate Quantum Chaos, Phys. Rev. A
57 (1998).

[25] This can also help study decoherence see
W. H. Zurek and J. P. Paz, Quantum
Chaos: A Decoherent Deﬁnition, Physica D
83 (1995).

[12] D. S. Abrams and S. Lloyd, A quantum
algorithm providing exponential speed in-
crease for ﬁnding eigenvalues and eigenvec-
tors, quant-ph/9807070.

[13] C. Zalka, Eﬃcient Simulation of Quantum
Systems by Quantum Computers Proc. Roy.
Soc. Lond. A 454 (1998) 313-322.

[14] S. Wiesner, Simulations of Many-Body
Quantum Systems by a Quantum Com-
puter, quant-ph/9603028.

[15] D. Coppersmith, An Approximate Fourier
Transform Useful in Quantum Factoring,
IBM Research Report RC19642, 1994.

[16] A. Ekert and R. Jozsa, Quantum Computa-
tion and Shor’s Factoring Algorithm, Rev.
Mod. Phys., 68, No. 3, 1996.

[17] R. Jozsa, Quantum Algorithms and the
Fourier Transform, Proc. Roy. Soc. Lond.
454 (1998).

[18] S. Lloyd, Science, 261, 1569-1571, 1993.

[19] D. G. Cory, A. F. Fahmy, and T. F. Havel,

Proc. Nat. Acad. Sci. 94, 1634.

[20] N. A. Gershenfeld and I. L. Chuang,
Bulk Spin-Resonance Quantum Computa-
tion, Science, 275, 17 Jan. 1997.

[21] S. S. Somaroo, D. G. Cory, T. F. Havel, Ex-
pressing the operations of quantum comput-
ing in multiparticle geometric algebra, Phys.
Lett. A, 240, 1998.

[22] E. Knill, R. Laﬂamme, W. H. Zurek, Re-
silient Quantum Computation: Error Mod-
els and Thresholds, Proc. Roy. Soc. Lond.
454 (1998).

6


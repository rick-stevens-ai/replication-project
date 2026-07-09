# Extraction (SURROGATE for Marker) — tool: PyMuPDF (fitz) v1.27.2.3
# Paper: arXiv:1501.00082 — Park et al., 'Hyperfine spin qubits in irradiated malonic acid: heat-bath algorithmic cooling'
# Rationale: Marker CLI not installed locally; PyMuPDF layout-preserving text extraction
# is the closest zero-dependency surrogate used by sibling QC-200 replications.
# For the ground-truth text stream this replication actually reads, see work/paper.txt (pdftotext -layout).



<!-- ==== page 1 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath
algorithmic cooling
Daniel K. Park · Guanru Feng · Robabeh
Rahimi · St´ephane Labruy`ere · Taiki Shibata ·
Shigeaki Nakazawa · Kazunobu Sato · Takeji
Takui · Raymond Laﬂamme · Jonathan Baugh
Abstract The ability to perform quantum error correction is a signiﬁcant hurdle
for scalable quantum information processing. A key requirement for multiple-round
quantum error correction is the ability to dynamically extract entropy from ancilla
qubits. Heat-bath algorithmic cooling is a method that uses quantum logic operations
to move entropy from one subsystem to another, and permits cooling of a spin qubit
below the closed system (Shannon) bound. Gamma-irradiated, 13C-labeled malonic
acid provides up to 5 spin qubits: 1 spin-half electron and 4 spin-half nuclei. The nu-
clei are strongly hyperﬁne coupled to the electron and can be controlled either by ex-
ploiting the anisotropic part of the hyperﬁne interaction or by using pulsed electron-
nuclear double resonance (ENDOR) techniques. The electron connects the nuclei to
a heat-bath with a much colder effective temperature determined by the electron’s
thermal spin polarization. By accurately determining the full spin Hamiltonian and
performing realistic algorithmic simulations, we show that an experimental demon-
stration of heat-bath algorithmic cooling beyond the Shannon bound is feasible in
both 3-qubit and 5-qubit variants of this spin system. Similar techniques could be
useful for polarizing nuclei in molecular or crystalline systems that allow for non-
equilibrium optical polarization of the electron spin.
Keywords Quantum information · Quantum error correction · Algorithmic cooling ·
Electron spin resonance · Electron nuclear double resonance
D.K. Park · G. Feng · R. Rahimi · S. Labruy`ere · R. Laﬂamme · J. Baugh
Institute for Quantum Computing, University of Waterloo, Waterloo, Ontario, N2L 3G1, Canada
D.K. Park · G. Feng · R. Rahimi · R. Laﬂamme · J. Baugh
Department of Physics and Astronomy, University of Waterloo, Waterloo, Ontario, N2L 3G1, Canada
T. Shibata · S. Nakazawa · K. Sato · T. Takui
Department of Chemistry and Molecular Materials Science, Graduate School of Science, Osaka City Uni-
versity, Sumiyoshi-ku, Osaka, 558-8585, Japan
R. Laﬂamme
Perimeter Institute for Theoretical Physics, Waterloo, Ontario, N2J 2W9, Canada
Canadian Institute for Advanced Research, Toronto, Ontario M5G 1Z8, Canada
J. Baugh
Department of Chemistry, University of Waterloo, Waterloo, Ontario, N2L 3G1, Canada
E-mail: baugh@uwaterloo.ca
arXiv:1501.00082v2  [quant-ph]  13 May 2015

<!-- ==== page 2 ==== -->
2
Daniel K. Park et al.
1 Introduction
Quantum Error Correction (QEC) is a critical tool for protecting quantum informa-
tion against the imperfections of realistic devices and to scale quantum processors up
to many qubits. Although a well developed theory exists [1–6] and experimental real-
izations at the several qubit level are recently emerging [7, 8], there remain challenges
for many potential implementations. Nuclear Magnetic Resonance (NMR) quantum
information processing has demonstrated a high degree of quantum control [9–11]
and the ability to efﬁciently characterize the noise, both intrinsic and extrinsic, that
affects the ﬁdelity of a quantum process [12]. One piece has however been missing:
the ability to efﬁciently polarize nuclear spin qubits on demand. The threshold theo-
rem for quantum computation tells us that a quantum circuit can be simulated with
arbitrarily high precision using a polynomial amount of resources as long as the error
per gate p is below a certain threshold value pth [45]. The theorem relies on assuming
that the ancilla qubits are in pure states at the beginning of each cycle of fault-tolerant
QEC. For example, the ﬁrst layer of concatenation of QEC typically reduces the ef-
fective error rate from p to cp2, where c is a system-dependent constant. However,
this theoretical gain is not generally achieved for the impure ancilla qubits charac-
teristic of real implementations [16]. Thus, an efﬁcient and experimentally feasible
method for cooling qubits to high purity prior to each QEC cycle is desirable for all
circuit implementations, including those based on nuclear spins.
Heat bath algorithmic cooling (HBAC) [13–15, 17, 18] is an efﬁcient method for
extracting entropy from a set of system qubits, allowing qubits to be cooled below
the bath temperature (i.e. beyond the closed-system, or Shannon, bound). Solid state
NMR experiments have demonstrated a sufﬁcient level of coherent control to execute
multiple rounds of algorithmic cooling, leading to spin polarizations exceeding the
thermal polarization [19, 20]. However, in a typical NMR setup, very low spin polar-
ization at thermal equilibrium will require highly precise control over tens of nuclear
spin qubits in order to polarize one ancilla qubit to order unity. Here, we explore the
use of an electron spin to assist in the HBAC protocol. Due to its much larger gyro-
magnetic ratio compared to nuclei, the electronic thermal spin polarization is about
103 times larger, and spin-lattice relaxation rates scale by a similar factor. Exploiting
the electronic spin-lattice relaxation as a reset operation, the electron can connect a
set of nuclear spins to heat bath with an effective temperature much lower than the
equilibrium nuclear spin temperature.
The stable malonyl radical ˙CH(COOH)2 has been extensively studied by elec-
tron spin resonance (ESR) studies of gamma-irradiated single crystals. The hyperﬁne
tensors of the α-proton and of the 13C-labeled methylene carbon were previously
published [21–23]. However, the hyperﬁne tensors of the 13C-labeled carboxyl car-
bons have not yet been reported. Including these two carboxyl carbons and assuming
they are spectroscopically distinct, the molecule can in principle realize a 5-qubit en-
semble quantum information processor, with 1 electron and 4 nuclear spins. In this
paper we study the per-13C-labeled radical and determine the hyperﬁne tensors of
the carboxyl carbons via ESR and electron-nuclear double resonance (ENDOR) ex-
periments on single crystal samples at room temperature. The carboxyl tensors are
in fact different owing to different dihedral angles of COOH relative to the C-C-

<!-- ==== page 3 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
3
C plane to accommodate the hydrogen bonding network; the carboxyl group with
a larger dihedral angle has a slightly weaker carbon hyperﬁne coupling. The previ-
ously published tensors describing the electronic g-factor and proton and methylene
carbon hyperﬁne couplings are conﬁrmed by our measurements. Given full knowl-
edge of the spin Hamiltonian, we determine the optimal magnetic ﬁeld orientations
for carrying out quantum algorithms, focusing on HBAC as the example of inter-
est. We consider two distinct methods for obtaining high ﬁdelity coherent control, (i)
use of anisotropic hyperﬁne interactions [24–26] facilitated by GRAPE [27] pulses,
and (ii) pulsed ENDOR control sequences. For brevity, we refer to approach (i) as
Anisotropic Hyperﬁne Control (AHC). The two control schemes have very different
criteria for choosing a suitable magnetic ﬁeld orientation, given the desire to reduce
the durations and optimize the ﬁdelities of the quantum operations. Simulations of
HBAC with realistic values of electronic spin-lattice relaxation time (T1), intrinsic
dephasing time (T2) and ensemble dephasing time (T ∗
2 ) are carried out for both the
3-qubit (methylene 13C) and 5-qubit (per-13C labeled) versions. The results indicate
that experimental cooling of nuclear spins beyond the thermal electron spin temper-
ature, while challenging, is feasible in this quantum processor. These techniques can
be applied to malonic acid or similar radical molecules at very low temperatures, or to
optically polarizable systems such as NV centers in diamond [28–30] or molecules
with photoexcited triplet states [31] at room temperature, to reach the nuclear spin
polarizations of order unity useful for QEC.
The reminder of the paper is organized as follows. Section 2 provides relevant
information about the properties and preparation of the single crystal samples. In
section 3, we review the extraction of g-factor and hyperﬁne tensors from orienta-
tion studies of ESR and ENDOR transitions, and report the tensors we determined
including the 13C carboxyl tensors. Section 4 presents criteria for choosing optimal
orientations of the magnetic ﬁeld with respect to the crystalline axes, to facilitate
control using either anisotropic hyperﬁne or pulsed ENDOR techniques. Realistic
simulations of HBAC protocols for both 3 and 5 qubits are described in section 5.
Conclusions are drawn in section 6.
2 Sample preparation
Malonic acid, CH2(COOH)2, crystalizes with a triclinic unit cell and belongs to the
P¯1 space group [32, 33] at temperatures above 47 K. At lower temperatures, a struc-
tural phase transition occurs that has been discussed previously [34–36]. Above 47
K, there are two molecules per unit cell related by inversion symmetry, making them
magnetically equivalent. We denote the methylene and carboxylic carbons as Cm
and C1,2, respectively. A schematic of the radical, obtained by removing one of the
methylene protons, is shown in Fig. 1. The unpaired electron is of p-orbital character
[22, 37, 38]. Malonic acid powder with all possible 13C isotopic labelling conﬁgura-
tions was purchased either from Sigma Aldrich or Cambridge Isotopes. Single crys-
tals were grown by slow evaporation from aqueous solutions at room temperature. To
form radicals, crystals were irradiated to a dose of about 2 kGy at room temperature
with γ-rays from a cobalt-60 pencil. Annealing at 60◦for 12-15 hours following the

<!-- ==== page 4 ==== -->
4
Daniel K. Park et al.
irradiation suppresses ESR signals from all other radical species except for the most
stable radical, ˙CH(COOH)2 [37]. Depending on the 13C labelling conﬁguration, 2, 3,
4 or 5 qubit samples are obtained as (e-H), (e-H-Cm), (e-H-C1,2) and (e-H-Cm-C1,2)
respectively, where e denotes the electron spin. The β-protons of the carboxyl groups
contribute to ESR line broadening and in some orientations can give rise to observ-
able splittings [39]. However, due to weak hyperﬁne coupling (< 6 MHz isotropic
coupling [39]) they are not useful as qubits.
Z"
X"
"
"
"
φ"
θ"
c"
a"
b"
(a)"
x’# 
y’#
z’#
sample#holder#
1"mm"
(b)#
Fig. 1 (a) Molecular structure of ˙CH(COOH)2 with unpaired electron density distribution schematically
represented by the blue shaded region. x and z are two principal axes of the α-proton hyperﬁne tensor, with
z along the Cm–α-proton interatomic vector and x along the cylindrical symmetry axis of the electronic
p-orbital. The y axis, not shown, is nearly parallel to the C1–C2 interatomic vector. The direction of the
static ﬁeld B0 can be described using polar angle θ and azimuthal angle φ in the principal axis system of
the α-proton hyperﬁne tensor. The directions of the crystallographic axes a, b and c with respect to the
molecular structure are illustrated by the green axes [32, 40]. c lies very close to the y axis of the α-proton
principal axis system. The direction cosines of a, b and c in the α-proton principal axis system are (0.1426,
-0.6588, 0.7387), (-0.9729, -0.1888, 0.1335) and (0.0222, 0.9969, -0.0752), respectively. (b) Schematic of
the crystal mounted on a sample holder for the orientation study (see section 3.2). Primed axes (x′, y′ and
z′) indicate the lab frame in which measurements are taken. The curved green arrow indicates rotation of
the crystal for orientation studies.
3 Spin Hamiltonian
The spin Hamiltonian of malonic acid with K nuclei contains electron Zeeman, electron-
nuclear hyperﬁne, and nuclear Zeeman terms as following:
ˆ
H =
ˆ
He +
ˆ
Hh f +
ˆ
Hn = µBgαβB0α ˆSβ +
K
∑
n=1

2πAn
αβ ˆSα ˆIn
β −γn ˆIn
αB0α

.
(1)
Here α,β ∈{x,y,z}, and the repeated index implies summation over all the values of
the index (similar to the Einstein summation convention, except all indices appear as
lower indices). We set ¯h = 1 so that all Hamiltonians will appear in angular frequency
units. ˆSα,β and ˆIα,β represent electron and nuclear spin operators, µB is Bohr mag-
neton, B0 = (B0x,B0y,B0z) is external magnetic ﬁeld and γn is the gyromagnetic ratio
for nuclear spin n. The second rank tensors g whose elements are gαβ, and An whose

<!-- ==== page 5 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
5
elements are An
αβ, are the electron g-tensor and the hyperﬁne tensor describing cou-
pling to nuclear spin n. In X-band (∼10 GHz) ESR, the electron Zeeman interaction
is the dominant Hamiltonian term. The nuclear dipole-dipole interaction is neglected
since it is typically at least two orders of magnitude smaller than the hyperﬁne inter-
action. When the nuclear Zeeman and hyperﬁne interaction energies are comparable
and much smaller than the electron Zeeman energy, taking B0 = B0z the secular spin
Hamiltonian can be written:
ˆ
H = ωS ˆSz −
K
∑
n=1
ωn
I ˆIn
z +2π ˆSz
K
∑
n=1
 An
zz ˆIn
z +Bn ˆIn
x

.
(2)
Here, ωS = gzzµBB0 is the electron Larmor frequency, ωn
I = γnB0 is the nuclear Lar-
mor frequency, and Bn =
q
(Anzx)2 +(Anzy)2.
3.1 Tensor extraction from ESR and ENDOR data
In this section, we brieﬂy review the Hamiltonian determination method explained
in [41]. First, we will consider the procedure to determine the g-tensor. For a static
magnetic ﬁeld B0 = B0(lx,ly,lz) (lx,ly and lz are direction cosines of the magnetic ﬁeld
in the axes of the crystal, and l2
x +l2
y +l2
z = 1), the electron Zeeman energy levels can
be rewritten as
E± = ±1
2µBB0(lαΓαβlβ)1/2,
(3)
where we introduce Γ = g·g. In the absence of nuclear spins, the magnetic resonance
condition ∆E = hν = µBgB0 leads to
g =
hν
µBB0
= ∆E
µBB0
= E+ −E−
µBB0
= (lαΓαβlβ)1/2,
(4)
where g is the experimentally observed value, ∆E is the difference between E+ and
E−, and ν is the frequency of the microwave (mw) ﬁeld. For B0 = B0(cosθ,sinθ,0),
using the symmetry Γαβ = Γβα, the dependence of g on θ can be written as
(g(θ))2 = lαΓαβlβ = Γxx cos2 θ +Γyy sin2 θ +2Γxy cosθ sinθ.
(5)
By measuring g(θ) at various θ and solving Eq. (5), Γxx, Γyy and Γxy can be deter-
mined. Similarly, by orienting B0 within the x-z and y-z planes and measuring g(θ)
for various θ (where θ is the angle between B and z, or between B and y), Γzz, Γxz and
Γyz can be determined. Therefore full knowledge of Γ can be obtained.
Now we consider the electron-nuclear coupled spin Hamiltonian which contains
ˆ
He,
ˆ
Hhf and
ˆ
Hn. In this case, the 1st order approximation of the energy levels of the
system are
EMSMI =gµBB0MS +
K
∑
n=1
{4π2
g2 (lαΓ An
αβ lβ)+ γ2
nB2
0
M2
S
−4π
gMS
γnB0(lα(g ·An)αβlβ)}1/2Mn
I MS,
(6)

<!-- ==== page 6 ==== -->
6
Daniel K. Park et al.
where ΓA = g·A·A·g, and MS and Mn
I are quantum numbers for the electron spin and
the nth nuclear spin, respectively. All ESR transitions can be classiﬁed into two types:
allowed and forbidden transitions. Allowed transitions correspond to electron-only
spin ﬂips, while forbidden transitions correspond to the ﬂips of electron spin along
with one or more nuclear spins. In the absence of anisotropic hyperﬁne coupling (the
terms with Bn coefﬁcient in Eq. (2)), forbidden transitions are completely suppressed
and produce no observable ESR signal. When Bn ̸= 0, these transitions can lead to
signals comparable to, but typically smaller than, the allowed transitions. For the pur-
pose of hyperﬁne tensor determination, it sufﬁces to track only allowed ESR transi-
tions. The nuclear Zeeman energy is generally much smaller than hyperﬁne coupling
strength and is usually omitted in the traditional process of determining hyperﬁne
tensors using ESR spectra. However when we determined hyperﬁne tensors in this
work, after the traditional process we implemented an optimization process which
takes the nuclear Zeeman energy into consideration. We will discuss this further in
Section 3.2. In the present section we will stick to the traditional process. Therefore,
after omitting the nuclear Zeeman energy, the ESR allowed transition energy gap in
the 1 electron-1 nucleus system is
∆E = gµBB0 + 2π
g (lαΓ A
αβlβ)1/2MI,
(7)
where the nuclear spin quantum numbers MI = ±1/2 represent spin up and spin down
states, respectively. The ESR spectrum then splits into two distinct peaks separated
by a frequency A = g−1(lαΓ A
αβlβ)1/2. Similar to Eq. (5), when the static magnetic
ﬁeld is B0 = B0(cosθ,sinθ,0) we have
(g(θ)A(θ))2 = Γ A
xx cos2 θ +Γ A
yy sin2 θ +2Γ A
xy cosθ sinθ,
(8)
and, as before, expressions for B0 in the x-z and y-z planes relate the other tensor
components of ΓA to (gA)2.
Another method to determine hyperﬁne tensors is to make use of ENDOR exper-
iments. For ENDOR transitions, which correspond to ∆MS = 0 and ∆MI = ±1, the
energy gap in the 1 electron-1 nucleus system can also be readily obtained from Eq.
(6) and its square is given by
∆E2 = γ2B2
0 + 4π2M2
S
g2
(lαΓ A
αβlβ)−4πMSγB0
g
(lα(g ·A)αβlβ).
(9)
Therefore, the ENDOR spectral peaks also split into two for MS = ±1/2. Supposing
that the observed ENDOR frequencies are ν± for MS = ±1/2, Eq. (9) can be rewritten
as
ν2
± = ν2
I + 1
4g2 (lαΓ A
αβlβ)∓νI
g (lα(g ·A)αβlβ),
(10)
where νI = γB0/2π. An equation similar to Eqs.(5) and (8) can be obtained when the
static magnetic ﬁeld is B0 = B0(cosθ,sinθ,0),
g
2νI
(ν2
−−ν2
+) = (g ·A)xx cos2 θ +(g ·A)yy sin2 θ +2(g ·A)xy cosθ sinθ.
(11)
Therefore, the magnitude of A can be extracted by measuring the orientation depen-
dence of g(ν2
−−ν2
+)/2νI in three distinct rotation planes.

<!-- ==== page 7 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
7
3.2 Continuous-wave ESR results
The tensor extraction model relies on two assumptions: the three planes of measure-
ment are mutually non-parallel and the axis of the rotation to go from one to another
belongs to both planes. The orientation experiments were designed to ensure that
both assumptions are satisﬁed. In each of the three non-parallel planes, we took 24,
9 and 46 measurements with 8◦, 20◦and 4◦angle steps for the methylene-labeled,
carboxyl-labeled and fully-labeled MA samples, respectively. The methylene-labeled
data was used to extract the α-1H and 13Cm tensors; the carboxyl-labeled data was
used to extract the 13C1,2 (average) tensor, and the fully-labeled data was used to
conﬁrm all the tensors by ﬁtting with simulated spectra. As discussed previously in
Section 3.1, we need only to detect the spectral positions of the allowed transitions,
which can be distinguished from forbidden transition peaks because of their larger
intensities. Each measured spectrum is ﬁt to a set of allowed transition peaks deﬁned
by their amplitude, frequency and a common line width.
The peak positions for all measurements in one plane give a set of trajectories for
that plane, from which we obtained the dependence of g and An on θ. Doing this in
all three planes allows extraction of the g-factor tensor g and hyperﬁne tensors An
by solving Eqs. (5) and (8). After this, we used the method of least square ﬁtting
to optimize g and An by minimizing the difference between the experimental peak
trajectories and the simulated trajectories. It should be noted that in X-band ESR the
nuclear Zeeman energy for 1H is about 15 MHz, which is comparable to the hyperﬁne
coupling of α-1H in some orientations. Therefore, in order to obtain more accurate
An tensors, we took into account the nuclear Zeeman energy when generating the
simulated peak trajectories in the optimization procedure. The only noticeable differ-
ence from including this energy was for the α-1H, as expected.
The g, AH, ACm and AC1,2 tensors were determined from continuous (CW) ESR
spectra as described above, and are listed in Table 1. The hyperﬁne tensors of C1 and
C2 are similar and require ENDOR measurements to be distinguished (see next sec-
tion). From the ESR data we obtained an average hyperﬁne tensor describing C1 and
C2, denoted as AC1,2. Negative signs of the principal values for AC1,2 were determined
by a quantum chemical calculation using the Gaussian program [46]. Similar to the
case of α-1H [22, 37, 38], the negative principal values are due to a negative spin
density on C1 and C2.
The results for g, AH and ACm are consistent with the published results in [21–
23, 36, 37, 40]. The simulated ESR peak trajectories generated from the tensors in
Table 1 are in excellent agreement with the experimental data, as the examples in
Figs. 2 and 3 demonstrate.
3.3 Continuous-wave ENDOR results
In this section we describe the use of ENDOR, which has higher spectral resolution
than ESR, to extract the distinct tensors describing AC1 and AC2. From Eq. (10) we
see that for each nucleus there are two resonant frequencies ν−and ν+. However,
in experiments we found that one or sometimes two of the four peaks of C1 and C2

<!-- ==== page 8 ==== -->
8
Daniel K. Park et al.
Direction cosines to AH principal axis
X
Y
Z
gxx
2.00250 ± 0.00038
-0.1657
0.9779
0.1272
gyy
2.00373 ± 0.00037
-0.9811
-0.1766
0.0797
gzz
2.00417 ± 0.00036
0.1004
-0.1115
0.9887
AH
xx
-26.6 ± 2.8
1
0
0
AH
yy
-56.0 ± 0.7
0
1
0
AH
zz
-91.5 ± 0.6
0
0
1
ACm
xx
24.5 ± 1.0
0.0696
-0.0019
0.9976
ACm
yy
43.0 ± 1.3
0.9962
0.0530
-0.0694
ACm
zz
212.3 ± 0.6
-0.0528
0.9986
0.0056
A
C1,2
xx
-36.1 ± 0.3
0.0627
0.0082
0.9980
A
C1,2
yy
-39.3 ± 0.3
0.9805
-0.1870
-0.0601
A
C1,2
zz
-40.6 ± 0.3
0.1862
0.9823
-0.0198
Table 1
Electronic g-factor and hyperﬁne coupling tensors determined from CW ESR measurements
(principal hyperﬁne values are given in MHz). Principal values are given in the left column, while direction
cosines relative to the principle axis system of the α-proton are given in the three right columns. The
uncertainties reﬂect a 90% conﬁdence interval. The tensor AC1,2 gives an estimate of the average of AC1
and AC2.
0
20
40
60
80
100
120
140
160
180
−60
−40
−20
0
20
40
60
θ (◦)
Magnetic ﬁeld (G)
 
 
Fig. 2
Comparison between the simulated ESR peak trajectories (red lines) and the experimental data
(blue dots) of the methylene 13C-labeled sample in one of the planes measured. The direction cosines of
the normal of this plane are (-0.3376 0.9405 0.0391) in the principal axis system of AH.
were obscured by the large peaks around 14.5 MHz that come from 1H spins which
have small hyperﬁne couplings with the electron radical (Fig. 4). The two higher
frequency peaks (in the range of 20−25 MHz) were clearly resolved in all measured
orientations. Judging from the sign of AC1,2, we infer that these two peaks correspond
to the νC1
+ and νC2
+ frequencies, with
(νn
+)2 = (νn
I )2 + 1
4g2 (lαΓ An
αβ lβ)−νn
I
g (lα(g·An)αβlβ) = (νn
I )2 + 1
g2 (lαKAn
αβlβ), (12)

<!-- ==== page 9 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
9
0
50
100
150
−60
−40
−20
0
20
40
60
θ (◦)
Magnetic ﬁeld (G)
 
 
Fig. 3
Comparison between the simulated ESR peak trajectories (red lines) and the experimental data
(blue dots) of the per-13C-labeled sample in one of the planes measured. The direction cosines of the
normal of this plane are (-0.3678 0.9287 -0.0483) in the principal axis system of AH.
where n = 1,2 for C1 and C2 and KAn = ΓAn/4 −νn
I gg · An. Using only the ν+ fre-
quencies requires a different approach than directly using Eq. (11). Instead of mea-
suring the orientation dependence of g((νn
−)2 −(νn
+)2)/2νn
I , we measured that of
g2((νn
+)2 −(νn
I )2) in three non-parallel planes to extract KAn using Eq. (12), and then
used KAn to calculate AC1 and AC2. In each plane, we took 9 measurements with 20◦
angle steps for the carboxyl-labeled MA sample. It should be mentioned that by using
Eq. (12) to obtain AC1 and AC2, we neglected the anisotropy of g. For the hyperﬁne
tensors, this approximation causes a difference in the principal values less than the
experimental uncertainty of ∼0.1 MHz. The experimentally determined AC1 and AC2
tensors are listed in Table 2.
Direction cosines to AH principal axis
X
Y
Z
AC1
xx
-37.0 ± 0.1
-0.5310
-0.0010
0.8474
AC1
yy
-40.5 ± 0.1
0.8452
-0.0724
0.5295
AC1
zz
-43.6 ± 0.1
0.0608
0.9974
0.0392
AC2
xx
-34.0 ± 0.1
-0.3477
-0.0449
-0.9365
AC2
yy
-37.4 ± 0.1
-0.2478
0.9677
0.0456
AC2
zz
-39.6 ± 0.1
-0.9043
-0.2479
0.3476
Table 2 Hyperﬁne coupling tensors for AC1 and AC2 determined from CW ENDOR measurements (prin-
cipal hyperﬁne values are given in MHz). Principal values are given in the left column, while direction
cosines relative to the principle axis system of the alpha-proton are given in the three right columns. The
uncertainties reﬂect a 90% conﬁdence interval.
Figs. 4 and 5 show the experimental ENDOR and ESR spectra, together with
the simulated spectra generated using the tensors given in Table 2, for the carboxyl-
labeled sample when the orientation of the magnetic ﬁeld is (0.6156 -0.7179 -0.3249)
in the principal axis system of AH. In Fig. 4, we can see that in this orientation there

<!-- ==== page 10 ==== -->
10
Daniel K. Park et al.
are three observable peaks of C1 and C2, while the peak with the lowest frequency
is obscured by the 1H peaks around 14.5 MHz. Excellent agreement between experi-
ment and simulation can be seen in these examples, and a similar level of agreement
was found for spectra in all measured orientations, indicating that the tensors in Table
2 are accurate.
10
15
20
25
30
−10
−5
0
5
10
15
Frequency(MHz)
Intensity (a. u.)
 
 
ENDOR
Simulation
ν+
1
ν+
2
ν−
2
ν−
1
Fig. 4
Comparison between the simulated ENDOR spectrum (red line) and the experimental spectrum
(black line) of the carboxyl 13C-labeled sample. The orientation of magnetic ﬁeld is (0.6156, -0.7179, -
0.3249) in the principal axis system of AH. In the area around 14.5 MHz, there are large peaks which come
from the distant 1H spins that have small hyperﬁne couplings with the electron radical. The ENDOR peak
for C2 with the frequency ν2
−= 14.9 MHz is obscured by these 1H peaks. The other three ENDOR peaks
for C1 and C2 with frequencies ν1
+ = 24.1 MHz, ν2
+ = 22.1 MHz and ν1
−= 16.8 MHz are clear.
3360
3380
3400
3420
3440
−10
−5
0
5
10
Field (G)
Intensity (a. u.)
 
 
ESR
Simulation
Fig. 5 Comparison between the simulated ESR spectrum (red line) and the experimental spectrum (black
line) of the carboxyl 13C-labeled sample. The orientation of magnetic ﬁeld is (0.6156, -0.7179, -0.3249) in
the principal axis system of AH. Using the tensors given in Table 2, the ESR peak positions are reproduced
well and the line broadening due to the hyperﬁne couplings of the two carboxyl carbons ﬁts well in all
measured orientations.

<!-- ==== page 11 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
11
4 Optimizing magnetic ﬁeld orientation for quantum control
4.1 Orientation criteria for AHC
In the presence of B0 = B0z, a hyperﬁne-coupled nuclear spin is quantized along the
direction of an effective ﬁeld
Beff = (B0 ±πAzz/γ)z±(πB/γ)x,
(13)
where B =
p
(Azx)2 +(Azy)2 and the ± sign depends on whether the electron spin is
parallel (|↑⟩) or anti-parallel (|↓⟩) to B0. The angle of nth nuclear spin quantization
axis from z is denoted as ηn
↑= arctan
 −Bn/(An
zz +ωn
I /π)

for electron spin |↑⟩and
ηn
↓= arctan
 −Bn/(An
zz −ωn
I /π)

for electron spin |↓⟩.
A requirement for achieving high control ﬁdelity is to implement gates on a
time scale fast compared to the electronic dephasing time T e
2 . The electron spin con-
trol Hamiltonian in the rotating frame is Hc(t) = ω1(t)( ˆSx cos(φ(t))+ ˆSy sin(φ(t)),
where ω1 and φ represent the microwave amplitude and phase, respectively. Consider
ω1 = constant, and φ = 0. Nuclear spin ﬂips can occur via electron-nuclear ﬂip-ﬂip
forbidden transitions driven at a rate ω1 sin(ηn)/2 where ηn = (ηn
↑−ηn
↓)/2. The
on-resonance allowed ESR transition is driven at ω1 cos(ηn)/2. Depending on the
nuclear isotope and the dc ﬁeld orientation, sin(ηn)/2 can be very small, preventing
efﬁcient control of the nuclear spins via microwave excitation. Thus, we aim to ﬁnd
an orientation that yields the set {An
zz,Bn} that maximizes the ratio of forbidden to
allowed transition rates, tan(ηn). Secondly, all allowed and forbidden transition fre-
quencies should be separated from each other by at least the ESR line width (∼12
MHz in the malonyl radical) in order to achieve universal control.
For the optimal orientation search, B0 is ﬁxed at 2π ·10 GHz/γe ≈3568 G (note
γe = gµB) and θ and φ (see Fig. 1(a)) are varied at 1◦angle steps. The maximum
values of tan(ηn) are 1.3, 0.14, 0.016, and 0.017 for H, Cm, C1, and C2, respec-
tively. The duration of a GRAPE optimal control [27] pulse to accomplish an arbitrary
unitary operation will scale as 1/tan(ηn). We have measured a nearly temperature-
independent electron spin dephasing time T e
2 ∼5 µs in this system, due to hyperﬁne
coupling with distant protons, and their mutual dipolar interaction induced dynamics.
Given that the shortest GRAPE pulses for arbitrary gates involving H require ∼500
ns, it is clear that high ﬁdelity control of C1, and C2 via AHC is simply not possi-
ble in this system. Moreover, the 5-qubit system contains 80 ESR resonances over
a maximum spectral range of 250 MHz, consisting of 16 allowed and 64 forbidden
transitions. Consequently, we ﬁnd maxθ,φ{min(δ)} = 1.4 MHz, where the elements
of δ are the distances between any two ESR transitions and maxθ,φ{} indicates the
maximization over all sets of {θ,φ} with 1◦angle step. In practice, it only makes
sense therefore to focus on the 3-qubit sample (e-H-Cm) for optimizing AHC control.
Nonetheless, for completeness we show in Table 3 the best possible orientation for
the 5-qubit system given these criteria.
For the 3-qubit sample, there are 4 allowed transitions and 8 forbidden transitions.
It is still not possible to ﬁnd orientations where min(δ) ≥12 MHz, rather we ﬁnd that
maxθ,φ{min(δ)} = 7.6 MHz. We focus on orientations that satisfy min(δ) ≥6 MHz,

<!-- ==== page 12 ==== -->
12
Daniel K. Park et al.
and then choose an orientation in which tan(ηH) and tan(ηCm) are both as large as
possible. The forbidden transition rates at this orientation are 0.1418 and 0.1203 for
H and Cm, respectively, and min(δ) = 6.1 MHz. These results are summarized in the
table below:
An
zz(MHz), Bn(MHz), tan(ηn)
θ,φ
H
Cm
C1
C2
min(δ)
(MHz)
5 qubit
54◦,123◦
-62.56,
23.67,
0.1948
121.23,
90.54,
0.0303
-40.03,
3.27,
0.0161
-37.29,
1.63,
0.0093
1.1
3 qubit
29◦, 13◦
-76.60,
27.07,
0.1418
29.21,
17.78,
0.1203
6.1
Table 3 Optimal orientations for AHC experiment with the fully-labeled (5 qubit) and Cm-labeled (3
qubit) malonyl radical, and corresponding values of hyperﬁne coupling constants An
zz and Bn, and the quan-
tity tan(ηn) characterizing the controllability of nuclear spin n. min(δ) represents the minimum separation
between ESR transitions.
4.2 Orientation criteria for ENDOR
In the ENDOR control scheme, nuclear spin rotations are implemented directly by ap-
plying radio-frequency (RF) pulses on resonance with the nuclear transitions. Hence,
tan(η) does not need to be large. In fact, it is desirable to minimize tan(η), because
the electron spin-lattice relaxation process induces nuclear spin relaxation through
the two-spin ﬂip forbidden transitions. As before, the allowed ESR transitions must
be separated by at least the ESR line width, and the NMR transitions must be sep-
arated by at least the NMR (ENDOR) linewidth. The latter is determined by the
nuclear dephasing time T n
2 >> T e
2 , and is therefore much narrower than the ESR
line width. The disadvantage of ENDOR control is that the RF pulses are typically
of order γe/γn ∼103 times slower than the microwave control of electron spin. This
severely limits the ability to perform arbitrary quantum algorithms within the elec-
tron T e
2 , however, in algorithmic cooling the electron spin is always in an eigenstate
during the nuclear rotations so that electronic dephasing is not an issue. Since the
hyperﬁne tensors of C1 and C2 are very similar, they cannot be separately addressed
by microwave pulses, but only with RF pulses. At ﬁrst glance, this seems to forbid
selective swap gates between the electron and C1 or C2, which is an essential step
for HBAC. Fortunately, we show in Section 5.2 that it is possible to realize a pulse
sequence combined with the electron refresh step in order to polarize both C1 and C2
to the bath polarization, as long as all NMR transitions can be addressed selectively,
and the nuclei H and Cm are separately addressable by microwave pulses.
The RF pulse durations are typically on the order of tens of µs, corresponding
to excitation bandwidths less than 100 kHz. Thus, for the 5 qubit sample, we search
for an orientation in which all NMR transition frequencies are at least 500 kHz apart,

<!-- ==== page 13 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
13
and all allowed ESR transition frequencies with the exception of the C1 and C2 res-
onances are at least 12 MHz apart. Then among this set, we select one orientation
in which tan(η) is as small as possible for all nuclei. The optimal orientation for the
fully-labeled molecule and relevant parameters in that orientation is given in Table
4. The minimum distance between ESR transitions in this orientation is 6 MHz due
to C1 and C2. All other ESR transitions are at least 13 MHz apart from each other.
Some forbidden transitions may be very close to the ESR allowed frequencies, but
this is not a serious issue since the forbidden transitions can be ignored when tan(η)
is small.
For the 3 qubit molecule, it is relatively easy to ﬁnd orientations in which the al-
lowed ESR transitions are separated by at least 12 MHz. Among that set, an optimal
orientation is chosen for which tan(η) is minimized for both H and Cm. The results
are summarized in Table 4.
An
zz(MHz), Bn(MHz), tan(ηn)
θ,φ
H
Cm
C1
C2
min(δ)
(MHz)
5 qubit
95.8◦,86.3◦
-56.36,
3.59,
0.048
209.48,
22.51,
0.0039
-43.50,
0.70,
0.0029
-37.56,
0.70,
0.004
6
3 qubit
90◦, 90◦
-56.0, 0,
0
211.83,
8.98,
0.0015
56
Table 4
Optimal orientations for the ENDOR control scheme with fully-labeled (5 qubit) and 13Cm-
labeled (3 qubit) molecules, corresponding values of hyperﬁne coupling constants An
zz and Bn, and the
quantity characterizing forbidden transition rates tan(ηn) for nuclear spin n. In these orientations, the
NMR transitions are well separated for high ﬁdelity control; the minimum distances between two NMR
transition frequencies are 1.8 MHz and 7.6 MHz for the 5 qubit and 3 qubit systems, respectively. Here,
min(δ) represents the minimum separation between allowed ESR transitions.
5 Simulation of Heat-Bath Algorithmic Cooling
The Partner Pairing Algorithm (PPA) [18] is the optimal method for implementing
HBAC when there is one reset qubit that thermalizes to the bath polarization εb much
faster than the relaxation rate of the system qubits. In this scenario, polarizing one
system qubit beyond εb can be achieved by repeatedly applying the entropy compres-
sion and refresh steps. The compression is a permutation that rearranges the diagonal
elements of the density matrix in non-increasing order so that the polarization of the
1st (target) qubit increases while the reset qubit polarization decreases. During the re-
fresh step, the reset qubit thermalizes to the bath temperature and the overall entropy
of the system is reduced. As this procedure is repeated, the polarization of the target
qubit, εt, asymptotically approaches a threshold value: εth = εb2n−2 if εb ≪2−n, and
polarization arbitrarily close to unity when εb ≫2−n, where n is the number of sys-
tem qubits used in the compression step [18, 42].

<!-- ==== page 14 ==== -->
14
Daniel K. Park et al.
We perform simulations of 3-qubit and 5-qubit HBAC for cooling one target qubit
below the electronic spin bath temperature using 13Cm-labeled and 13Cm,1,2-labeled
molecules. The HBAC protocol consists of two steps: (i) apply a swap gate between
the electron and each nucleus, with electron refresh steps in between, cooling all nu-
clei to the bath temperature; (ii) run multi-qubit compression to boost the polarization
of the target spin. For the 3 qubit case, the protocol we simulate is equivalent to the
PPA. For the 5 qubit simulation, designing the stepwise operations corresponding to
the PPA is challenging since each compression gate depends on the input state of
the gate and is generally a different gate for each compression step. Moreover, the
PPA compression gates may involve complicated pulse sequences. Thus, the 5-qubit
protocol simulated here is designed to be analogous to the 3-qubit sequence, i.e. a po-
larization transfer from the electron to all nuclei followed by a 5-qubit compression
step. This same sequence can be repeated until asymptotic polarization is reached,
although here we only simulated one round to demonstrate the feasibility of cooling
beyond the Shannon bound in this 5-qubit system.
Two control methods are tested for the HBAC simulations: AHC and ENDOR.
The electronic T1 and T2 processes are modelled as a Markovian dynamical map, and
simulated by solving a master equation of the Lindblad form [43, 44]. Inhomoge-
neous line broadening of the electron spin resonances, characterized by T ∗
2 , is taken
into account by averaging the simulation over a set of spin Hamiltonians in which the
magnitude of electron Zeeman energy is a Lorentzian-distributed random variable.
We use experimentally measured electron T1 and T2 values to determine the Lindblad
operators, and the measured ESR line width to determine the T ∗
2 Hamiltonian distri-
bution. The electron relaxation parameters are T1 = 27 µs, T2 = 5 µs, and T ∗
2 = 28 ns
at room temperature. In the following sections, we describe the simulations in detail
and report the results.
5.1 Simulation of 3-qubit HBAC
The quantum circuit for 3-qubit HBAC is shown in the top part of Fig. 6. Here, the
electron is chosen as the bath qubit whose polarization is εb ≈8×10−4 at room tem-
perature and at B0 = 2π ·10 GHz/γe ≈3568 G. Under these conditions, 1H and 13C
equilibrium polarizations are about 660 and 2620 times smaller than the electronic
polarization. For the 3-qubit PPA with completely mixed initial states, the ﬁrst two
entropy compression steps are polarization transfers (swaps) from the reset qubit to
the 1st (target) and the 2nd qubits. After the 3rd gate operation (3-qubit compression),
the target qubit polarization is higher than the bath polarization. These steps complete
one round of the 3-qubit PPA. In theory, the ﬁrst round of the 3-qubit PPA boosts the
polarization of one nuclear spin to 1.5εb −0.5ε3
b ≈1.5εb for small εb. By repeated
application of these steps, the nuclear spin is asymptotically polarized to 2εb. Note
that starting from the 2nd round, only one polarization swap gate is used since the
target nucleus is already polarized above the bath polarization.

<!-- ==== page 15 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
15
5.1.1 Anisotropic hyperﬁne control
The crystal orientation used for the 3-qubit experiment using the AHC method is
shown in Table 3. In this orientation, the forbidden transition rate of Cm in the pres-
ence of a resonant microwave ﬁeld is weaker than that of the α-proton. Consequently,
the Cm polarization decays slower than that of proton during electron reset. Therefore
Cm is chosen as the target qubit for cooling. The electron reset is done by waiting for
4.2×T e
1 in order to bring the electron polarization to about 98.5% its thermal polar-
ization. A longer waiting time, e.g. 5×T e
1 , brings the electron polarization to above
99%, however, we ﬁnd that the wait time of 4.2×T e
1 is optimal since nuclear spin po-
larizations decay during electron reset (due to the anisotropic hyperﬁne interaction).
The microwave ﬁeld swap and compression gates are designed using the gradient as-
cent pulse engineering (GRAPE) algorithm [27]. The GRAPE pulse lengths are 840
ns for the swap gates and 900 ns for the 3-qubit compression gate. The pulses are
optimized over the electron Zeeman Hamiltonian distribution in order to be robust to
T ∗
2 = 28 ns. The design ﬁdelities averaged over this distribution are 99%, 98% and
96% for the e-H swap, e-Cm swap, and 3-qubit compression, respectively. The bottom
part of Fig. 6 illustrates the implementation of controls necessary for the ﬁrst round
of 3-qubit HBAC using AHC.
R"
R"
C"
H
e"
R"
R"
…"
R"
R"
C"
H
e"
4.2"x"T1
e"
4.2"x"T1
e"
mw"
SWAP"
GRAPE&
SWAP"
GRAPE&
COMPRESSION"
GRAPE&
="Polariza3on"transfer"
="Compression"
R" ="Reset"
Fig. 6 Quantum circuit of 3-qubit HBAC using the AHC method. The electron spin is the reset qubit, and
it is refreshed by waiting for 4.2×T e
1 . In the optimal crystal orientation for AHC, the forbidden transition
strength of Cm is weaker than that of the proton. Consequently, the Cm polarization decays more slowly
during electron reset and Cm is chosen as the target qubit. Two rounds of the algorithm are shown in the
top panel. The 3-qubit PPA iteratively applies polarization transfer (shaded in blue) and the compression
(shaded in yellow). All gates are designed in the microwave domain using the GRAPE algorithm. The
GRAPE pulse lengths are 840 ns for the swap gates and 900 ns for the compression gate. A schematic of
the AHC sequence for this circuit is shown in the lower part.
Fig. 7 shows the polarization of Cm at the end of each round of 3-qubit HBAC.
The red curve is obtained when the simulation incorporates the experimentally deter-
mined, room temperature electron relaxation effects. The Cm polarization exceeds the
bath polarization after the ﬁrst round of HBAC, and increases further asymptotically
as the HBAC is repeated. Nevertheless, the polarization enhancement is below the
theoretically calculated value; after 9 HBAC rounds, the polarization of Cm is about

<!-- ==== page 16 ==== -->
16
Daniel K. Park et al.
1
2
3
4
5
6
7
8
9
1.2
1.4
1.6
1.8
2
HBAC Number of Rounds
ǫc
ǫb
 
 
Theory
T2=5 µs, T2*=28 ns
T2=T2*=5 µs
T2=20 µs, T2*=28 ns
Fig. 7 Simulation results for 3-qubit HBAC using AHC. The plot shows the ratio of the Cm polarization
(εc) and the electron bath polarization (εb) at the end of each HBAC round, up to 9 rounds. The black
dashed curve is the theoretical (ideal) value. The red curve is obtained by incorporating all experimentally
determined (room temperature) relaxation parameters. The blue curve is obtained by allowing the T ∗
2 of
the electron to equal T e
2 . The green curve is obtained by allowing T e
2 to be 20 µs, 4 times longer than the
measured value, in order to test the consequence of a longer T2.
76% of the theoretical value. The largest contribution to the error is the loss of nuclear
polarization due to the electron T1 process during the application of GRAPE pulses
and the electron refresh steps. In the absence of decoherence, the GRAPE pulses
transfer 99.6% and 99.8% of the electron polarization to Cm and H, respectively. The
compression gate polarizes the carbon to 1.49εb at the end of the ﬁrst round. How-
ever, when the T1 of the electron is introduced while T2 and T ∗
2 are still assumed to
be inﬁnite, the carbon and hydrogen polarizations prior to the compression step are
reduced to 94.4% and 94.3% of the electron polarization, and the compression yields
the carbon polarization of 1.39εb. Another source of the error is the ﬁnite ratio of
the electron T2 to the pulse duration; T e
2 is only about 5 to 6 times longer than the
GRAPE pulses. One can imagine another type of 3-qubit molecule whose electron T2
is longer, for instance, 20 µs. Then the polarization of the carbon after 7 rounds of
HBAC is 1.66εb, which is 83% of the theoretical value (i.e. the green curve in Fig. 7).
Finally, we consider a scenario in which the ESR linewidth is much narrower and T2
limited, i.e. T ∗
2 = T2 = 5 µs. This result is indicated in blue in Fig. 7. Although there
is a slight improvement by having a longer T ∗
2 , the experimental value of T ∗
2 does
not pose a signiﬁcant problem since the GRAPE pulses are designed to be robust to
inhomogeneous line broadening.
5.1.2 ENDOR control
In a pulsed ENDOR control scheme, the crystal orientation is chosen as shown in
Table 4. In this orientation, the forbidden transition rates are both minimized, and
it turns out the rate for H is weaker than that of Cm. Thus, H is chosen as the tar-
get qubit for cooling. The electron reset is done by waiting for 5 × T1 in order to
bring the electron polarization to 99.3% of the thermal polarization. The loss of
nuclear polarization during reset and control operations is negligible since the for-
bidden transition rates are both very weak. As shown in the bottom part of Fig. 8,

<!-- ==== page 17 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
17
the swap and compression gates can be decomposed into controlled-not (CNOT)
gates and a toffoli gate. These operations can be realized by selective microwave
and RF π-pulses. For example, the CNOT gate that ﬂips the H spin if the elec-
tron is ‘spin down’ can be realized by RF pulses at frequencies that correspond to
|↑H↑C↓e⟩↔|↓H↑C↓e⟩and |↑H↓C↓e⟩↔|↓H↓C↓e⟩transitions. In the compression step,
a Toffoli gate that ﬂips H spin if both Cm and electron are ‘spin down’ is required.
However, the Toffoli gate on the proton cannot be realized by this method because the
|↑H↑C↓e⟩↔|↓H↑C↓e⟩transition frequency is identical to the |↑H↓C↓e⟩↔|↓H↓C↓e⟩
frequency. On the other hand, a Toffoli gate that ﬂips the electron spin when both
H and Cm are ‘spin down’ can be realized by applying a microwave pulse at the
frequency of the |↓H↓C↑e⟩↔|↓H↓C↓e⟩transition, which is distinct from all other
allowed ESR transition frequencies. Therefore, we modify the quantum circuit to ex-
tract the entropy from the electron during the compression, and use an additional
swap gate to transfer the ﬁnal polarization to the proton (see Fig. 8).
This quantum circuit enables one to repeatedly apply HBAC for pumping the H
polarization. The compression step consists of four CNOT gates and a Toffoli gate,
as shown in Fig. 8. Since the goal of the compression is only to extract entropy from
the electron, the last two CNOT gates targetting the nuclear spins (shown in the red
dashed box in Fig. 8) are not necessary. Hence, the compression is reduced to two
CNOT gates and a Toffoli gate as shown in the middle part of Fig. 8. The rectangular-
shaped microwave and RF pulses shown at the bottom of Fig. 8 represent selective
π-pulses, and the different shading of these pulses illustrate different frequencies.
R"
R"
H
C#
e#
R"
R"
…
R"
R"
H
C#
e#
5"x"T1
e"
mw#
RF#
5"x"T1
e"
="Polariza1on"transfer"
="Compression"
R" ="Reset"
Fig. 8 Quantum circuit of the 3-qubit HBAC using ENDOR control. The electron is used as the reset qubit,
and it is refreshed by waiting for 5 × T1. In the crystal orientation optimized for ENDOR, the forbidden
transition rates of H are weaker than those of Cm, so H is chosen as the target qubit. The 3-qubit PPA
iteratively applies polarization transfer (shaded in blue) and compression (shaded in yellow). All gates
are realized using selective microwave and RF π-pulses. The compression step can only be implemented
here to boost the electron polarization (see text for explanation), so a swap gate between the electron and
proton is used to store the boosted polarization on the proton. The CNOT gates in the red dashed box are
not necessary and are left out of the simulated implementation. The quantum circuit in the middle shows
the gate decomposition of the swap and the compression into CNOT and Toffoli gates. The schematic of
the microwave and RF pulse sequence at the bottom shows that the CNOT and Toffoli gates can be realized
by transition-selective pulses. Shading illustrates different pulse frequencies.

<!-- ==== page 18 ==== -->
18
Daniel K. Park et al.
The maximum power for microwave pulses is chosen such that the Rabi frequency
is 25 MHz. In practice, the resonant microwave cavity has a ﬁnite bandwidth. This
means that more input power is needed in order to drive transitions whose frequency
is offset with respect to the cavity resonance frequency. Since the input power is lim-
ited in any real experimental setup, the pulse length must increase in order to apply
the π-pulse at the offset frequency. Fig. 9 shows a simulated ESR spectrum centered
at the resonator resonance frequency of 10 GHz (red), and the voltage transfer func-
tion for a resonator with quality factor (Q) of 100 (blue). If the pulse is applied at
a frequency at which the corresponding value of the transfer function is x, then the
pulse length must increase by a factor of 1/x to compensate for the loss in transmitted
power. This ﬁnite bandwidth effect must be taken into account in simulations because
the algorithm cannot be successful if microwave pulse durations become comparable
to the electron T2. In the present simulations, the resonator quality factor Q is set to
100 and microwave pulse lengths are adjusted accordingly. The RF π-pulses are re-
alized using 15 µs (H) and 60 µs (Cm) square pulses, reﬂecting typical RF ampliﬁer
output power levels and assuming an untuned (broadband) RF circuit.
9.8
9.9
10
10.1
10.2
0.5
1
Frequency (GHz)
 
 
ESR spectrum
Transfer function
Fig. 9 Simulated ﬁeld-sweep spectra for the 13Cm-labeled malonic acid in the orientation given in Table 4
(red), and voltage transfer function for a microwave cavity with Q = 100 (blue). The y-axis represents the
scaling factor of square root of the microwave power in the cavity a function of the microwave frequency.
Given a ﬁxed maximum available microwave power, pulse durations for offset pulses must be increased
relative to cavity-resonant pulses.
Using the room-temperature electron T1, the HBAC algorithm will not be suc-
cessful because RF pulse lengths are similar to T1. This can be solved by exploiting
longer T e
1 values at lower temperatures. In unlabelled, irradiated malonic acid, we
have found experimentally a T1 that grows roughly exponentially with temperature,
e.g. with values of 29 µs, 2.6 ms and 11 ms at room temperature, 43 K, and 22 K,
respectively. For simulating 3-qubit HBAC with ENDOR, we choose T1 = 2.6 ms
(ignoring the fact that a structural phase transition occurs at 47 K, probably compli-
cating the ESR spectrum). The selective microwave pulses must be designed with
a care. While each pulse selectively excites certain transitions, they must also be
broad enough to cover the ESR linewidth of about 12 MHz. First, we simulate 50
ns gaussian-shaped pulses with the full width at half maximum of 20 ns in order
to excite the entire ESR linewidth and remain selective on the particular transition.

<!-- ==== page 19 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
19
The result is shown in Fig. 10 in red. The main source of the error is the inability of
the Gaussian pulses to uniformly rotate all spins across the ESR linewidth; the pulse
bandwidth must be close to 50 MHz in order to fully excite the entire ESR line width,
but the minimum distance between two ESR allowed transition frequencies is about
56 MHz. Thus, even in the absence of T1 and T2 effects, each swap gate loses 8%
polarization. For the improved microwave control, selective π-pulses are engineered
using the GRAPE algorithm and can be made robust to T ∗
2 = 28 ns which corresponds
to the ESR line width of 12 MHz. Using this method, swap gates can transfer 98%
of the polarization from the electron to the target nuclear spin. The simulation results
for HBAC using GRAPE microwave pulses and rectangular RF pulses are shown in
blue in Fig. 10.
1
2
3
4
5
6
7
8
1.4
1.6
1.8
2
HBAC Number of Rounds
ǫH
ǫb
 
 
gaussian mw
GRAPE mw
Fig. 10
Simulation results of the 3-qubit HBAC using ENDOR control. The plot shows the ratio of H
polarization to the electron thermal polarization after each round of the HBAC, up to 8 rounds. The black
dashed curve is the theoretical value. The selective microwave π-pulses are designed in two different ways:
(i) 50 ns gaussian-shaped MW pulses with 20 ns full width at half maximum (red), (ii) and GRAPE pulses
(blue). In both cases, RF transitions are applied using square transition-selective pulses with 15 ns and 60
ns pulse lengths for H and Cm spins, respectively.
5.2 Simulating 5-qubit HBAC
As discussed in Section 4.1, due to weak forbidden transition rates of C1,2 and fre-
quency overlap among ESR transitions, the AHC scheme cannot be implemented in
the 5-qubit sample. Therefore, we focus on ENDOR control techniques in the simu-
lation of 5-qubit HBAC. Here, we simulate one round of the 5-qubit HBAC as shown
in Fig. 11, to demonstrate that cooling beyond the Shannon bound is experimentally
feasible in the 5-qubit molecule. The quantum circuit we employ for 5-qubit HBAC
is shown in Fig. 11. The electron is the target qubit, but the circuit can be easily mod-
iﬁed to cool a nuclear spin by adding a swap gate after the compression step. The-
oretically, by applying one round of the quantum circuit, the target qubit is cooled
to εb(15 −10ε2
b + 3ε4
b)/8 ≈1.875εb for small εb. The orientation of the magnetic
ﬁeld used in the simulation is shown in Table 4, and the electron polarization and

<!-- ==== page 20 ==== -->
20
Daniel K. Park et al.
relaxation parameters are the same as used in the 3-qubit ENDOR HBAC simulation.
The forbidden transition rates of the carbons are weaker than those of the proton, so
the polarization transfer to H is done just before the compression gate, as shown in
Fig. 11. Similar to the 3-qubit HBAC ENDOR circuit, the last CNOT gates in the
compression step (inside the red dashed box) are not necessary since the electron is
the target spin.
R"
R"
R"
R"
e
Cm$
C1$
C2$
H
="Polariza+on"transfer"
="Compression"
R" ="Reset"
Fig. 11 Quantum circuit for 5-qubit HBAC with the electron as the target spin. The polarization can be
transferred to a nuclear spin with an additional swap gate. The last CNOT gates inside the red dashed
box of the compression step are unnecessary, and are left out of the simulation. The open circles in the
controlled gates indicate that the target spin is ﬂipped if the control qubit is in the ‘spin up’ state. One
round of the algorithm shown.
The usual method for a swap gate between the electron and one of the carboxyl
carbons requires selective microwave control of C1 and C2. However, the hyperﬁne
tensors of C1 and C2 are very similar and the two spins cannot be separately addressed
by microwave pulses. However, they can be separately addressed with RF pulses
(see Section 4.2). Therefore, the polarization transfer step for C1,2 is modiﬁed as
shown in Fig. 12, and theoretically polarizes both C1 and C2 to the electron thermal
polarization.
e
C1$
C2$
R"
R"
ϵe$
ϵe$
ϵe$
Fig. 12 Circuit for polarization transfer between the electron and C1,2. The circuit brings C1 and C2 to the
bath temperature without selective microwave control, but requires selective RF pulses. The open circles
in the controlled gates indicate that the target spin is ﬂipped if the control qubit is in the ‘spin up’ state.
Note that the circuit shown in Fig. 11 is not the optimal cooling algorithm, i.e.
the PPA. Fig. 13 compares the PPA and our cooling algorithm by showing the target
qubit polarization εt compared to the bath polarization as a function of HBAC steps.
Here, each step consists of one refresh operation and one gate on the system qubits (in
contrast to the ‘round’ used previously). In the low bath polarization regime, the PPA
asymptotically increases the target qubit polarization to 8 times the bath polarization,
while repeated application of the algorithm shown in Fig. 11 yields an asymptotic

<!-- ==== page 21 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
21
enhancement of 4. While it is possible to ﬁnd sequences corresponding to the PPA, it
is an open question whether such sequences could be practically implemented in this
system. For the PPA, the gate decomposition of each system qubit operation depends
on the input state, and can result in a complicated pulse sequence. An advantage of
the algorithm implemented in our simulation is that the gate decomposition of each
step is relatively simple and the asymptotic limit can be reached by simply repeating
the quantum circuit.
0
50
100
150
200
0
2
4
6
8
Number of Refresh + Compression
ǫt
ǫb
 
 
PPA
Our HBAC
Fig. 13 Theoretical target qubit polarization εt normalized by the bath polarization, as a function of the
number of cooling steps, to show the difference between the 5-qubit PPA and the algorithm in Fig. 11.
Each step consists of one refresh operation and one gate on the system qubits. The red curve is obtained by
the PPA while the blue curve is obtained by repeated application of the quantum circuit shown in Fig. 11.
In the low polarization regime, the PPA allows the target qubit polarization to asymptotically approach 8
times the bath polarization, and 4 times the bath polarization with our algorithm.
As seen already in the 3-qubit HBAC simulation, designing microwave pulses
that uniformly rotate all spin across the ESR line width while remaining transition-
selective is a challenge. For the 5-qubit system, this problem is exacerbated since the
ESR transitions are more closely spaced in frequency. In order to obtain the maximum
polarization enhancement, GRAPE optimal control must again be used for designing
the selective microwave pulses. GRAPE pulses that are robust to the experimentally
determined value of T ∗
2 have been designed with at least 0.95 state ﬁdelity and with
200 ns pulse lengths for the mw pulses applied to Cm and C2, 900 ns for C1 and 1H,
and 100 ns for the 5-qubit compression. RF pulse lengths are chosen as 5 µs and 20
µs for 1H and 13C, respectively. Including the effects of the electron T1, T2, and T ∗
2 ,
the polarization enhancement after one round of 5-qubit HBAC is 1.67εb. A major
contribution to the error is the broad ESR line width compared to the spacing between
ESR resonances, which makes realizing high ﬁdelity transition-selective rotations on
a time scale short compared to T2 difﬁcult. Despite this, the simulation shows that a
single round of 5-qubit HBAC with a realistic control sequence and relaxation yields a
polarization enhancement beyond the Shannon bound, and also beyond the capability
of a single round of 3-qubit HBAC. Another simulation is performed assuming a
much narrower ESR line width, i.e. T ∗
2 = T2. In this case, all microwave pulses can
be designed with 99% unitary ﬁdelity at 100 ns pulse length, and all nuclei reach
at least 97% of the electron polarization during the polarization transfer steps. The

<!-- ==== page 22 ==== -->
22
Daniel K. Park et al.
polarization improvement after one round of 5-qubit HBAC is 1.79εb. This is 95% of
the polarization improvement predicted by the theory, similar to the result of the 3-
qubit HBAC simulation using ENDOR control with GRAPE microwave pulses. We
expect the single qubit polarization to reach above 3.6εb, 90% of the theoretical value,
as the algorithm is repeated, similar to the 3-qubit case. The result shows that for
HBAC with many qubits it is crucial to have a sharp ESR linewidth, which motivates a
search for electron-nuclear spin systems having narrower ESR lines than the malonyl
radical.
The 5-qubit HBAC results are summarized in Table 5.
Simulation
Theory
T ∗
2 = 5 µs
T ∗
2 = 28 ns
εt/εb
1.875
1.79
1.67
Table 5 Polarization of the target qubit compared to the bath qubit after one round of 5-qubit HBAC. The
quantum circuit for one round of 5-qubit HBAC is shown in Fig. 11. Results are shown for two different
values of T ∗
2 . The electron spin lattice relaxation time is T1 = 2.6 ms in this simulation.
Finally, we note two experimental caveats that are not taken into account in our
simulations, but do not invalidate the main results. In section 5, we accounted for
a type of cross-relaxation in which the nuclear polarization decays due to a com-
bination of the electronic spin-lattice relaxation process and the anisotropic term in
the spin Hamiltonian of the form ˆSz ˆIx. There is an additional cross-relaxation mech-
anism involving noise acting directly on the nuclear operators, which we have not
included in the Lindblad master equation. In future work, we plan to experimentally
measure the cross-relaxation rates as a function of orientation and temperature to
determine these additional contributions. If the additional mechanism is dominant,
going to lower temperatures may be required in order to achieve sufﬁciently long
nuclear T1 timescales. Secondly, a well known structural phase transition takes place
in malonic acid at 46 K [34–36], which we have not considered here. Below 46 K,
the P¯1 crystal symmetry is broken and there are two magnetically distinguishable
molecules per unit cell. We have observed certain ENDOR transitions to split into
two below 46 K, consistent with this phase change. However, experiments may be
designed using phase-cycling techniques in order to cancel signal contributions from
one of the molecules in the unit cell, so this does not in principle prevent the proposed
AC experiments from being carried out.
6 Conclusion
HBAC is an open-system cooling method that allows at least one qubit to be polarized
beyond the Shannon bound, starting from a set of initially mixed qubits and exploit-
ing a controlled interaction with a heat-bath. This is a promising tool for dynamically
preparing ancilla qubits to a sufﬁcient level of purity for quantum error correction. In
this work, we accurately determined the full spin Hamiltonian of a ﬁve qubit electron-
nuclear hyperﬁne coupled system in single crystal, irradiated malonic acid. Using the

<!-- ==== page 23 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
23
hyperﬁne tensors, we determined the optimal magnetic ﬁeld orientation for achieving
high ﬁdelity control using two control methods: anisotropic hyperﬁne control (AHC)
and pulsed ENDOR techniques. Computer simulations were carried out using real-
istic experimental conditions and including the relevant electron spin relaxation pa-
rameters, demonstrating that the realization of 3-qubit and 5-qubit HBAC is feasible
in this system. Using the 3-qubit molecule with AHC, the polarization of a nuclear
spin is predicted to increase above 1.5εb after 9 rounds of the cooling algorithm. The
ENDOR simulation assumed a lower temperature in which the electron T1 = 2.6 ms,
in order to have the T1 sufﬁciently long compared to RF pulse lengths. Using GRAPE
for selective microwave pulse design, the polarization of a nuclear spin is predicted
to increase above 1.8εb after 9 rounds of the cooling algorithm. There is a tradeoff
here between experimental simplicity and the achievable ﬁdelity; the AHC experi-
mental setup is simpler and can be performed at room temperature, but in general
yields lower ﬁdelities than the ENDOR approach at low temperature.
The carboxyl carbons in the 5-qubit sample have very weak forbidden transition
rates under an applied microwave ﬁeld, which prevents them from being practically
controllable using AHC. Hence, for the 5-qubit HBAC simulation, we focused on the
ENDOR control scheme. The 5-qubit simulation was again carried out at low tem-
perature for a longer T1, and the selective microwave pulses were designed using the
GRAPE method. After one round of 5-qubit HBAC, the simulation predicts that the
target qubit (the electron) would reach a polarization of 1.67εb. The major obstacle to
reaching the ideal value of 1.875εb is the small spacing between certain allowed ESR
transitions, similar in order to the ESR line width. Another simulation was performed
assuming T ∗
2 = T2 to predict the outcome of the algorithm given a molecule that is
similar to the malonic radical but with much sharper ESR transitions. Here, a target
qubit polarization of 1.79εb is obtained after one round of the algorithm.
We conclude that the experimental demonstration of 3- and 5-qubit algorithmic
cooling beyond the Shannon bound is feasible in the isotopically labelled malonyl
radical. The 5-qubit system can yield a larger polarization enhancement compared
to the 3-qubit system, as expected. The experimental value of T ∗
2 is found to be a
critical factor that limits the ﬁdelity of gate operations, and therefore the achievable
polarization under HBAC. Nearly ideal results are obtainable when T ∗
2 = T2.
Acknowledgements This research was supported by NSERC, the Canada Foundation for Innovation, CI-
FAR, the province of Ontario and Industry Canada. T. Takui would like to thank the support via Grants-in-
Aid for Scientiﬁc Research on Innovative Areas “Quantum Cybernetics” and Scientiﬁc Research (B) from
MEXT, Japan. The support for the present work by the FIRST project on “Quantum Information Process-
ing” from JSPS, Japan and by the AOARD project on “Quantum Properties of Molecular Nanomagnets”
(Award No. FA2386-13-1-4030) is also acknowledged. We acknowledge David Cory and Richard Oakley
for access to CW ESR spectrometers, Aaron Mailman for help with CW ESR, Jalil Assoud for assistance
with x-ray spectroscopy, and Robert Pasuta for help with gamma-irradiation of samples. We thank Dawei
Lu, Tal Mor and Yossi Weinstein for helpful discussions.
References
1. E. Knill, R. Laﬂamme, Physical Review A 55(2), 900 (1997)
2. E. Knill, R. Laﬂamme, W.H. Zurek, Science 279(5349), 342 (1998)

<!-- ==== page 24 ==== -->
24
Daniel K. Park et al.
3. J. Preskill, Proceedings of the Royal Society of London. Series A: Mathematical,
Physical and Engineering Sciences 454(1969), 385 (1998)
4. E. Knill, Nature 434(7029), 39 (2005)
5. P. Aliferis, D. Gottesman, J. Preskill, Quantum Information and Computation
8(3&4), 181 (2008)
6. D. Gottesman, Stabilizer codes and quantum error correction. Ph.D. thesis, Cal-
tech (1997), eprint: quant-ph/9705052
7. T.H. Taminiau, J. Cramer, T. van der Sar, V.V. Dobrovitski, R. Hanson, Nature
Nanotechnology 9(3), 171 (2014)
8. J. Kelly, R. Barends, A.G. Fowler, A. Megrant, E. Jeffrey, T.C. White, D. Sank,
J.Y. Mutus, B. Campbell, Y. Chen, Z. Chen, B. Chiaro, A. Dunsworth, I.C. Hoi,
C. Neill, P.J.J. OMalley, C. Quintana, P. Roushan, A. Vainsencher, J. Wenner,
A.N. Cleland, J.M. Martinis, Nature 519(7541), 66 (2015)
9. E. Knill, R. Laﬂamme, R . Martinez, C.H. Tseng, Nature 404(6776), 368 (2000)
10. C. Negrevergne, T. Mahesh, C. Ryan, M. Ditty, F. Cyr-Racine, W. Power,
N. Boulant, T. Havel, D. Cory, R. Laﬂamme, Physical Review Letters 96(17),
170501 (2006)
11. C.A. Ryan, M. Laforest, R. Laﬂamme, New Journal of Physics 11(1), 013034
(2009)
12. J. Emerson, M. Silva, O. Moussa, C. Ryan, M. Laforest, J. Baugh, D.G. Cory,
R. Laﬂamme, Science 317(5846), 1893 (2007)
13. P. O. Boykin, T. Mor, V. Roychowdhury, F. Vatan, R. Vrijen, Proc. Natl. Acad.
Sci. U.S.A 99, 3388 (2002)
14. J.M. Fernandez, S. Lloyd, T. Mor, V. Roychowdhury, International Journal of
Quantum Information 2(4), 461 (2004)
15. F. Rempp, M. Michel, G. Mahler, Physical Review A 76, 032325 (2007)
16. B. Criger, O. Moussa, R. Laﬂamme, Physical Review A 85, 044302 (2012)
17. P. Kaye, Quantum Information Processing 6(4), 295 (2007)
18. L. J. Schulman, T. Mor, Y. Weinstein, Physical Review Letters 94, 120501 (2005)
19. J. Baugh, O. Moussa, C.A. Ryan, A. Nayak, R. Laﬂamme, Nature 438(7067),
470 (2005)
20. C.A. Ryan, O. Moussa, J. Baugh, R. Laﬂamme, Physical Review Letters 100,
140501 (2008)
21. T. Cole, C. Heller, H. McConnell, Proceedings of the National Academy of Sci-
ences of the United States of America 45(4), 525 (1959)
22. T. Cole, C. Heller, Journal of Chemical Physics 34, 1085 (1961)
23. A. Horsﬁeld, J. Morton, D. Whiffen, Molecular Physics 4(4), 327 (1961)
24. N. Khaneja, Phys. Rev. A 76, 032326 (2007)
25. J.S. Hodges, J.C. Yang, C. Ramanathan, D.G. Cory, Physical Review A 78(1),
010303 (2008)
26. Y. Zhang, C.A. Ryan, R. Laﬂamme, J. Baugh, Physical Review Letters 107(17),
170503 (2011)
27. N. Khaneja, T. Reiss, C. Kehlet, T. Schulte-Herbr¨uggen, S.J. Glaser, Journal of
Magnetic Resonance 172(2), 296 (2005)
28. J. Loubser, J. Van Wyk, Reports on Progress in Physics 41(8), 1201 (1978)

<!-- ==== page 25 ==== -->
Hyperﬁne spin qubits in irradiated malonic acid: heat-bath algorithmic cooling
25
29. M.W. Doherty, N.B. Manson, P. Delaney, L.C. Hollenberg, New Journal of
Physics 13(2), 025019 (2011)
30. M. Doherty, F. Dolde, H. Fedder, F. Jelezko, J. Wrachtrup, N. Manson, L. Hol-
lenberg, Physical Review B 85(20), 205203 (2012)
31. W. Akhtar, V. Filidou, T. Sekiguchi, E. Kawakami, T. Itahashi, L. Vlasenko, J.J.L.
Morton, K.M. Itoh, Physical Review Letters 108, 097601 (2012)
32. J.A. Goedkoop, C.H. MacGillavry, Acta Crystallographica 10(2), 125 (1957)
33. N. Jagannathan, S. Rajan, E. Subramanian, Journal of chemical crystallography
24(1), 75 (1994)
34. J. Krzystek, A.B. Kwiram, A.L. Kwiram, The Journal of Physical Chemistry
99(1), 402 (1995)
35. M. Fukai, T. Matsuo, H. Suga, Thermochimica acta 183, 215 (1991)
36. R. McCalley, A.L. Kwiram, The Journal of Physical Chemistry 97(12), 2888
(1993)
37. H. McConnell, C. Heller, T. Cole, R. Fessenden, Journal of the American Chem-
ical Society 82(4), 766 (1960)
38. J. Morton, Chemical Reviews 64(4), 453 (1964)
39. E. Sagstuen, A. Lund, Y. Itagaki, J. Maruani, The Journal of Physical Chemistry
A 104(27), 6362 (2000)
40. J. Kang, S. Tokdemir, J. Shao, W.H. Nelson, Journal of Magnetic Resonance
165(1), 128 (2003)
41. N. Atherton, Principles of electron spin resonance (Ellis Horwood Limited,
1993)
42. O. Moussa, On heat-bath algorithmic cooling and its implementation in solid-
state NMR. Master’s thesis, University of Waterloo (2005)
43. G. Lindblad, Communications in Mathematical Physics 48, 119 (1976)
44. T.F. Havel, Journal of Mathematical Physics 44, 534 (2003)
45. P. Kaye, R. Laﬂamme. M. Mosca, An Introduction to Quantum Computing (Ox-
ford University Press, 2007)
46. M.J. Frisch, G.W. Trucks, H.B. Schlegel, G.E. Scuseria, M.A. Robb, J.R. Cheese-
man, G. Scalmani, V. Barone, B. Mennucci, G.A. Petersson, H. Nakatsuji, M.
Caricato, X. Li, H.P. Hratchian, A.F. Izmaylov, J. Bloino, G. Zheng, J.L. Son-
nenberg, M. Hada, M. Ehara, K. Toyota, R. Fukuda, J. Hasegawa, M. Ishida,
T. Nakajima, Y. Honda, O. Kitao, H. Nakai, T. Vreven, J. A. Montgomery, Jr.,
J.E. Peralta, F. Ogliaro, M. Bearpark, J.J. Heyd, E. Brothers, K.N. Kudin, V.N.
Staroverov, R. Kobayashi, J. Normand, K. Raghavachari, A. Rendell, J.C. Burant,
S.S. Iyengar, J. Tomasi, M. Cossi, N. Rega, J.M. Millam, M. Klene, J.E. Knox,
J.B. Cross, V. Bakken, C. Adamo, J. Jaramillo, R. Gomperts, R.E. Stratmann, O.
Yazyev, A.J. Austin, R. Cammi, C. Pomelli, J.W. Ochterski, R.L. Martin, K. Mo-
rokuma, V.G. Zakrzewski, G.A. Voth, P. Salvador, J.J. Dannenberg, S. Dapprich,
A.D. Daniels, ¨O. Farkas, J.B. Foresman, J.V. Ortiz, J. Cioslowski, and D.J. Fox,
Gaussian 09, Revision A.02 (Guassian, Inc., Wallingford CT, 2009)

Emerging research landscape of altermagnetism
Libor Šmejkal,1, 2 Jairo Sinova,1, 2 and Tomas Jungwirth2, 3
1

arXiv:2204.10844v1 [cond-mat.mes-hall] 22 Apr 2022

Institut für Physik, Johannes Gutenberg Universität Mainz, D-55099 Mainz, Germany
2
Institute of Physics, Czech Academy of Sciences,
Cukrovarnická 10, 162 00 Praha 6 Czech Republic
3
School of Physics and Astronomy, University of Nottingham, Nottingham NG7 2RD, United Kingdom
(Dated: April 25, 2022)
Magnetism is one of the largest, most fundamental, and technologically most relevant fields of
condensed-matter physics. Traditionally, two basic magnetic phases have been considered – ferromagnetism and antiferromagnetism. The breaking of the time-reversal symmetry and spin splitting
of the electronic states by the magnetization in ferromagnets underpins a range of macroscopic
responses in this extensively explored and exploited type of magnets. By comparison, antiferromagnets have vanishing net magnetization. This Perspective reflects on recent observations of materials hosting an intriguing ferromagnetic-antiferromagnetic dichotomy, in which spin-split spectra
and macroscopic observables, akin to ferromagnets, are accompanied by antiparallel magnetic order with vanishing magnetization, typical of antiferromagnets. An unconventional non-relativistic
symmetry-group formalism offers a resolution of this apparent contradiction by delimiting a third
basic magnetic phase, dubbed altermagnetism. Our Perspective starts with an overview of the
still emerging unique phenomenology of the phase, and of the wide array of altermagnetic material candidates. In the main part of the article, we illustrate how altermagnetism can enrich our
understanding of overarching condensed-matter physics concepts, and have impact on prominent
condensed-matter research areas.
CONTENTS

I. Introduction

1

II. Altermagnetic phase
A. Ab initio band-structures
B. Symmetry classification and description
C. Identification rules
D. Material candidates

3
3
4
6
7

III. Physical concepts
A. Kramers theorem
B. Fermi-liquid instabilities
C. Electron and magnon quasiparticles
D. Berry phase and non-dissipative transport

9
9
10
12
14

IV. Research areas
A. Spintronics
B. Ultra-fast optics and neuromorphics
C. Thermoelectrics, field-effect electronics and
multiferroics
D. Superconductivity

15
15
17

V. Conclusion
Acknowledgement

20
20

References

19
20

21

I.

INTRODUCTION

Magnetic solids are traditionally divided into two elementary phases – ferromagnets and antiferromagnets [1].

Ferromagnets, known for several millennia, are characterized by a strong macroscopic magnetization. They
generate a range of macroscopic phenomena originating
from the spin-split electronic band structure with broken
time-reversal (T ) symmetry, induced by the net magnetization. Antiferromagnets, on the other hand, were
discovered only a century ago, due to their vanishing net
magnetization that makes them behave in many aspects
as non-magnetic materials. In a traditional picture of
antiferromagnetism, a compensating antiparallel ordering of atomic magnetic moments, i.e. the effective cancellation of atomic moments leading to the vanishingly
small macroscopic net magnetization, has been thought
to generate no spin splitting of electronic states, and to
be invisible to the macroscopic electrical or optical probes
commonly used in ferromagnets.
Recently, diverse condensed matter research communities have been intrigued by theoretical predictions of T symmetry breaking macroscopic phenomena [2–16] and
spin-split band structures [2–9, 13–25], that are typical
of ferromagnets, in materials with compensated antiparallel magnetic ordering, that is characteristic of antiferromagnets. The apparent ferromagnetic-antiferromagnetic
dichotomy in these materials challenges the traditional
division of materials by the two basic magnetic phases.
A recent development [16] exploiting an unconventional
non-relativistic symmetry-group formalism [26–28] can
resolve this contradiction by delimiting, apart from the
traditional ferromagnetism and antiferromagnetism, a
third distinct and comparably abundant phase. This
third phase, dubbed altermagnetism, is characterized by
a compensated magnetic order with opposite-spin sublattices connected by crystal-rotation symmetries, and by
band structures with broken T -symmetry and alternating sign of the spin splitting in the momentum space. The
distinction of the three phases is highlighted in Fig. 1.

2
Altermagnet

M =0
Energy

(c)

C2,4,6

0

Y

Γ

(b)

M ̸= 0
Energy

(a)

Antiferromagnet

M =0
P

0

t

Energy

Ferromagnet

X

0

Y

Y

Γ

Γ

X

X

FIG. 1. Illustrative model distinction between conventional collinear ferromagnetic and antiferromagnetic phases, and the
emerging altermagnetic phase, highlighted in the crystal-structure real space and electronic-structure momentum space. (a)
Ferromagnetic model with one spin sublattice and corresponding magnetization (left panel), momentum-independent spin
splitting (right panel) and isotropic spin-split Fermi surfaces (inset of right panel). (b) Antiferromagnetic model with oppositespin sublattices connected by translation (t) or inversion (P) transformations, and corresponding zero net magnetization and
spin-degenerate bands. (c) Altermagnetic model with opposite-spin sublattices connected by rotation (C) transformation, and
corresponding zero net magnetization, anisotropic sublattice spin densities, spin splitting with alternating sign, and anisotropic
spin-split Fermi surfaces.

As we will discuss in this Perspective, altermagnetism
emerges on the basic level of the crystal-potential theory and effective single-particle non-relativistic description of band structures of collinear magnets. It is, therefore, a robust elementary magnetic phase. The theoretical prediction of altermagnetism thus complements in a
unique fundamental way modern studies of spin quantum
phases associated with more complex, and often more
subtle, topological phenomena, many-body correlations,
relativistic physics, or frustrated magnetic interactions
[29–38].
Altermagnetism is expected to be abundant in nature and to occur in both three-dimensional and twodimensional crystals, in diverse structural or chemistry
types, and in conduction types covering the whole spectrum from insulators to superconductors. In Sec. II, we
give an overview of the predicted characteristic features,
symmetries and material landscape of the altermagnetic
phase.
The properties connected to the spin-split T -symmetry
broken band structures of altermagnets open up a potential for previously unforeseeable developments in a broad
condensed-matter physics field. In Sec. III, we highlight
the distinct properties of altermagnets in the context
of overarching physical concepts of Kramers theorem,

Fermi-liquid instabilities, electron and magnon quasiparticles, and Berry phase and non-dissipative transport.
Sec. IV then outlines foreseen potential of altermagnets
in selected active research areas, including spintronics,
ultra-fast optics, neuromorphics, thermoelectrics, fieldeffect electronics, multiferroics, and high-temperature superconductivity.
While our focus in the following sections is on the
emerging field of altermagnetism from the theory perspective, we point out here that first measurements have
already indicated that altermagnetism can soon become
an active experimental field. Shortly after the theory
predictions of the possible coexistence of the compensated antiparallel magnetic order and the T -symmetry
breaking macroscopic phenomena, a supporting evidence
has been brought up by initial experiments [5, 10–12],
as highlighted in Tab. I. Apart from the fundamental
physics interests, we expect that intense experimental
research will be also driven by the potential impact of
altermagnetism on technology. Altermagnetism can occur in crystals with common light elements, high magnetic ordering temperatures and strong spin-coherence,
that are among the key prerequisites for practical device
applications.

3
Macroscopic response

Theory in RuO2

Experiment in RuO2

Theory in other materials

Anomalous Hall effect

2019 [3]

2020 [5]

SrRuO3 [39], Mn5 Si3 [6], κ-Cl [40], (Cr,Fe)Sb2 [7]

Spin current and torque

2020 [8, 16]

2021 [10–12]

κ-Cl [4], CaCrO3 [41]

TABLE I. Theoretical predictions, supported by experiments, of T -symmetry breaking macroscopic phenomena in RuO2 , and
a list of other altermagnetic materials in which these macroscopic responses were also theoretically predicted. The anomalous
Hall effect is a T -odd off-diagonal component of the electrical conductivity tensor [2]. The T -odd spin current can be generated
along or transverse to an applied electrical bias; an out-of-plane spin current generated by an in-plane electrical bias in an
altermagnetic layer can exert a torque on magnetic moments in an adjacent layer in a multilayer stack [8].

(a)

(c)

Y

(d)

RuO2

2

XB

z

y
x

XA

(b)

1

S’

ky

M
S

Y

S

Γ

X

(e)

FeF2

(f)

MnF2

kx

FIG. 2.
(a) Schematics of the rutile XY2 crystal structure with antiparallel magnetic moments on XA and XB magnetic
sublattices. (b) Brillouin zone of the rutile crystal and ab initio non-relativistic calculation of a wave-vector kz = 0 cut of the
anisotropic spin-split Fermi surface of metallic RuO2 . (c) Ab initio altermagnetic spin splitting of bands in RuO2 , calculated
without (red and blue) and with (black) relativistic spin-orbit coupling. (d) Ab initio altermagnetic spin-split Fermi surface for
selected kz values in RuO2 with correlations accounted for within the dynamical mean-field theory. (d,e) Ab initio altermagnetic
spin-split bands of insulating FeF2 and MnF2 , respectively. Adapted from Refs. [3, 18, 20, 42].
II.
A.

ALTERMAGNETIC PHASE
Ab initio band-structures

In Fig. 2 we show representative non-relativistic band
structures of metallic RuO2 [3, 8, 13, 14, 16, 18] and
insulating FeF2 [42] and MnF2 [20, 43], on which we illustrate key characteristics of the spin-split T -symmetry
broken band structures of altermagnets. These altermagnetic material examples belong to the family of crystals
with the rutile structure (Fig. 2a). For several insulating members of the rutile family, the compensated antiparallel arrangement of magnetic moments (Fig. 2a)
was well known already to Néel and his contemporaries
who, ironically, introduced them into the literature as
a classic representation of antiferromagnetism [44, 45].

The notion was based on focusing on the lattice of magnetic atoms alone, while omitting the essential role of
non-magnetic atoms on magnetism in the rutile crystals.
This may be one of the reasons why the spin splitting
and T -symmetry breaking of their non-relativistic band
structures (Figs. 2b-f) remained unnoticed for nearly a
century.
Remarkably, the room-temperature antiparallel magnetic ordering in metallic rutile RuO2 was discovered
[46, 47] and investigated [48, 49] only recently. The subsequent theoretical and experimental exploration of the
T -symmetry breaking macroscopic responses [3, 5, 8, 10–
14, 16, 18, 19] has made RuO2 one of the workhorse materials of the emerging research of altermagnetism.
Figures 2b-f show that the altermagnetic spin splitting
is strongly momentum-dependent in all three rutiles. In
RuO2 , it reaches in parts of the Brillouin zone a ∼1 eV

4
scale, which is comparable to the spin-splitting magnitudes in ferromagnets. Unlike ferromagnets, however, the
altermagnetic spin splitting in the non-relativistic bands
is accompanied by a zero net magnetization.
Figure 2 also illustrates that spin splittings in altermagnets can exceed by an order of magnitude the record
relativistic spin splittings in bulk crystals with heavy elements [50]. Moreover, unlike the momentum-dependent
spin textures in the relativistic bands, spin is a good
quantum number and the electronic states share a common momentum-independent spin quantization axis in
the non-relativistic bands of altermagnets.
The spin-split parts of the altermagnetic band structure are complemented by spin degeneracies along certain
lines or surfaces in the Brillouin zone. In Sec. II.B we will
show that non-relativistic symmetries of the altermagnetic spin group corresponding to the given crystal allow
for the spin splittings and protect the spin degeneracies
in high symmetry planes and lines [16].
Fermi surface cuts shown in Fig. 2b,d highlight the
typical anisotropic nature of the spin-split Fermi surfaces, with an equal number of states in the opposite spin
channels, and with the spin-momentum locking which is
even under the inversion of the momentum and breaks
T -symmetry.
Ab initio calculations in RuO2 shown in Fig. 2c,d also
demonstrate that the altermangetic spin splitting is only
weakly affected by the relativistic spin-orbit coupling,
and that the prominent features of the altermagnetic
spin-momentum locking are preserved when including
correlation effects beyond the local-spin-density approximation of the density-functional theory [3, 18, 20]. A
stable itinerant altermagnetism is further confirmed in
calculations without Hubbard correlations in other materials, such as Mn5 Si3 [6] or KRu4 O8 [16]. A sizable
altermangetic spin splitting survives also in the presence
of a strong alloying disorder, as shown in altermagnetic
Cr0.15 Fe0.85 Sb2 [7]. All this can be understood by the
fact that the altermagnetic symmetries, discussed in the
following section, can in principle hold equally well for
the effective single-particle Kohn-Sham potential, as well
as for the Dyson-equation description of correlated or
disordered systems. It highlights that the altermagnetic
phase is robust in a broad range of materials, can be
described within the effective single-particle Kohn-Sham
theory, and that the non-relativistic crystal potential can
play a dominant role in both uncorrelated and correlated
altermagnets.

B.

Symmetry classification and description

We now move from the microscopic ab initio theory to
a discussion of altermagnetism from the symmetry perspective. We start with an example comparing the description of RuO2 by relativistic magnetic-group symmetries and by non-relativistic spin-group symmetries [16].
This will illustrate why we choose the non-relativistic

spin-group formalism for the general symmetry classification and description of the altermagnetic phase.
The relativistic magnetic groups [51–56] consider
transformations in coupled real physical space and the
space of magnetic moment vectors. They have represented a primary symmetry tool for describing magnetic
structures in materials’ databases [55, 56], and have been
broadly applied in the research of equilibrium and nonequilibrium magnetic phenomena, including their mod[C2 ||C4z ]
ern topological variants
[57–62].
Non-relativistic spin symmetry

(a)

Relativistic magnetic symmetry

(b)

Top view

T Mz

y

[C2 ||C4z t]

x

RuA (mmm)

RuB (mmm)

T Mxȳ

Mxy

X

(c)
M[110]

T Mz
z
a2 , y
a1 , x

[C2 ||C4z t]

[E||Mi ]

T Mxȳ

X

Mxy

FIG. 3. (a) Schematic top view and 3D view of the RuO2
crystal with opposite spin directions on RuA and RuB sublattices depicted by red and blue color, oxygen atoms shown in
black, and with the depicted non-relativistic spin group symmetries in the notation of Ref. [16] (see text). Curved red
arrow and its label highlights the generator of opposite-spin
sublattice transformations, and the generators of the halving subgroup of same-spin sublattice transformations are also
highlighted (in black). (b,c) Schematic spin arrangement on
the RuO2 crystal with antiparallel (b) and parallel (c) spin
directions and the crystallographic spin-axis orientation depicted by red and blue arrows, and with the depicted relativistic magnetic symmetry group generators. The crossed arrow
highlights that the magnetic group contains no opposite spinsublattice transformation elements. (c) The spin-polarized
relativistic Fermi surface highlighting the presence of the approximate spin symmetry [C2 ||C4z ], omitted by the magnetic
group. (d) Relativistic momentum-resolved Berry curvature
hotspots originating from the avoided crossings along the
kx,y = 0 lines, whose position in the momentum space is
determined by the spin symmetries in the absence of the relativistic spin-orbit coupling. (e) Fermi surface resolved Berry
curvature of FeSb2 altermagnet illustrates pronounced contributions to Berry curvature from the quasi-nodal surface cross
kx = 0, ky = 0. Adapted from Ref. [16].

The non-relativistic spin group formalism [26–28] is a

5
generalization of the relativistic magnetic groups because
it allows for different transformations to act simultaneously in the decoupled spin and real space. The spin
groups have been employed only sporadically in magnetic
literature [16, 24, 25, 63–65].
The non-relativistic spin point group of RuO2 is a di2
rect product, r × RRuO
, of a spin-only group r = [C∞ k
s
E] + [C̄2 C∞ k T ] and of a non-trivial spin point group
2
RRuO
= [E k H] + [C2 k C4z ] [E k H] = 24/ 1m 2m 1m
s
[16]. In the spin-only group, C∞ is a group of arbitrary
rotations of the spin space around the common axis of
spins of the collinear magnet, E is real-space identity,
and C̄2 is a 180◦ spin-space rotation transformation (C2 )
around an axis perpendicular to the spins combined with
the spin-space inversion (i.e. time-reversal) [27, 28].
H = mmm is a halving subgroup of real-space transformations of the non-magnetic crystallographic group
4/mmm of RuO2 [16]. The subgroup [E k H], where E is
spin-space identity, contains symmetry transformations
which interchange atoms belonging only to one of the
two spin sublattices. Its generators, [E k Ē], [E k Mxy ],
and [E k Mz ], are shown in Fig. 3a. Here Ē is the spingroup notation [16, 27, 28] for real-space inversion (P),
and Mxy and Mz are real-space mirror transformations.
[C2 k C4z ], where C4z is a four-fold real-space rotation, is a generator of symmetry transformations which
interchange atoms between opposite-spin sublattices, as
also shown in Fig. 3a. The presence of symmetry transformations connecting the opposite-spin sublattices protects the zero net magnetization of the non-relativistic
magnetic structure of RuO2 . They also determine the
separation of opposite-spin equal-energy electronic states
in the momentum space, i.e., the symmetry-protected
spin-degenerate parts of the Brillouin zone, and the parts
where spin splitting is allowed by symmetry.
The relativistic magnetic point group of RuO2 is
m0 m0 m for the spin-axis direction shown in Fig. 3b.
Its generators are space-inversion, mirror Mz combined
with T -transformation, and mirror Mxy . The same
magnetic group describes a fully compensated antiparallel magnetic order (Fig. 3b), a parallel magnetic order with a strong non-relativistic ferromagnetic moment
(Fig. 3c), as well as an antiparallel magnetic order with
a weak uncompensated relativistic magnetization [16].
This example illustrates that the relativistic magnetic
groups do not generally separate between relativistic and
non-relativistic, compensated and non-compensated, or
collinear and non-collinear magnetic phases. Magnetic
space groups of type II, describing T -invariant crystals
without a magnetic order, are an exception for which a
transition to a non-relativistic physics description in decoupled spin and real space can be generally performed
by making a direct product with the spin-only group
SU (2) of arbitrary spin-space rotations [27, 66]. For
the remaining magnetic space groups of type I, III, and
IV, generally encompassing crystals with collinear and
non-collinear magnetic order [20, 22], a transition to
the non-relativistic physics description is not available

[16, 19, 21, 66].
Figure 4a shows that the prominent [C2 k C4z ] symmetry of the non-relativistic spin point group of RuO2 is
an apparent dominant features of the Fermi surfaces even
when the relativistic spin-orbit coupling is included in the
band-structure calculation. In contrast, the prominent
four-fold symmetry is absent in the relativistic magnetic
group. This illustrates that the non-relativistic spingroups represent an example of approximate, or so called
”hidden” symmetries. They allow for a systematic symmetry classification and description of magnetic phases
arising from the typically dominant non-relativistic crystal potentials [16, 26, 63, 64].
The spin-group formalism catagorizes all nonrelativistic collinear magnetic structures into three distinct phases [16]: (i) Ferromagnets (ferrimagnets) with
one spin lattice (or opposite-spin sublattices not connected by any symmetry transformation), (ii) spindegenerate antiferromagnets with opposite-spin sublattices connected by translation (spin-group symmetry
[C2 k t]) or inversion (spin-group symmetry [C2 k Ē]),
and (iii) altermagnets with opposite-spin sublattices connected by rotation transformations, but not connected by
translation or inversion.

(a)

(c)

ky

Γ

FeSb2

kx

[C2 ||C4z ]

(b)

RuO2
ky

Γ

(d)

kx

FIG. 4. (a) Spin-polarized relativistic Fermi surface highlighting the presence of the approximate spin symmetry
[C2 ||C4z ], omitted by the magnetic group. (b) Relativistic momentum-resolved Berry curvature hotspots originating
from the avoided crossings along the kx,y = 0 lines, whose
position in the momentum space is determined by the spin
symmetries in the absence of the relativistic spin-orbit coupling. (c) Fermi surface resolved Berry curvature of FeSb2 altermagnet illustrates pronounced contributions to Berry curvature from the quasi-nodal surface cross kx = 0, ky = 0. (d)
Brilouin zone notation. Adapted from Ref. [5, 7, 16].

6
The altermagnetic spin groups have a general form of
the direct product, r × Rs . Here the spin-only group,
r = [C∞ k E] + [C̄2 C∞ k T ],

(1)

is common to all three non-relativistic collinear phases,
while the non-trivial spin groups given by,
Rs = [E k H] + [C2 k A] [E k H],

(2)

correspond exclusively to altermagnets. Here A is the
real-space rotation transformation (proper or improper,
symmorphic or non-symmorphic). Altermagnets have

split, but equally populated spin-up and spin-down energy iso-surfaces in the non-relativistic band structure
that breaks T -symmetry. This makes altermagnetism
distinct from the ferromagnetic phase with a non-zero
net magnetization, the spin-degenerate antiferromagnetic phase, or non-magnetic relativistic systems with
T -invariant bands. In Tab. II we summarize the properties derived from the spin group symmetries, which will
guide our discussion in the following sections. The first
two lines regard symmetries of the spin-only group which
apply to all three non-relativistic collinear phases. The
remaining lines in Tab. II apply only to altermagnets.

Altermagnetic spin-group symmetries

Magnetic crystal structure

Non-relativistic band structure



C̄2 kT

Co-planar

Inversion symmetry

[C∞ k E]

Collinear

Spin good quantum number & k-independent


C̄2 kT × [C2 k A] [E k H]

Compensated

Spin splitting & broken T -symmetry

H

Sublattice spin-density anisotropy

Spin-Fermi-surface anisotropy



Lk ∩ AH 6= ∅

Spin-degenerate nodal lines or surfaces

Lk ∩ AH = ∅

Spin splitting at crystal-momentum k

LM ∩ AH = ∅

Spin splitting at TRIM M

Orbitally-degenerate Γ-point

Electric spin-splitting mechanism

TABLE II. Spin-group symmetries and corresponding magnetic crystal structure and non-relativistic band structure characteristics. The first two lines regard symmetries of the spin-only group that apply to all three non-relativistic collinear phases. The
remaining lines apply only to altermagnets. Symbol Lk marks the little group of real-space symmetry transformations which
map crystal-momentum k on itself or on a momentum which differs from k by a reciprocal lattice vector. M is a time-reversal
invariant momentum (TRIM). Adapted from Ref. [16]

We conclude this section by summarizing the basic elements of the algorithm for determining the alternagnetic
spin group (Eq. (2)). It can be constructed by identifying:
1. crystallographic group of the material,
2. crystallographic group of the spin-sublattice (in
the case of bipartite lattice the spin sublattice
point group corresponds directly to Wyckoff position point group),
3. crystallographic rotation transformation connecting the opposite-spin sublattices.
Taking RuO2 as an example, the crystallographic point
group is 4/mmm, the sublattice (Wyckoff) point group

is mmm, and the crystallographic point-group rotation
transformation connecting the opposite-spin sublattices
is C4z (cf. Fig. 3a).
C.

Identification rules

Elementary rules for identifying the altermagnetic
phase of a crystal can be summarized as follows:
1. there is an even number of magnetic atoms in the
unit cell and the number of atoms in the unit cell
does not change between the non-magnetic and
magnetic phases of the crystal (cf. two Ru atoms
in RuO2 unit cell, shown in Fig. 3a),

7
2. there is no inversion center between the sites occupied by the magnetic atoms from the opposite-spin
sublattices (cf. the absence of the inversion center
between the RuA and RuB sites in RuO2 because
of the oxygen atoms, shown in Fig. 3a),
3. the two opposite-spin sublattices are connected by
crystallographic rotation transformation, possibly

Insulator

Semiconductor

4. the spin group is determined by the algorithm described in Sec. II.B (cf. the RuO2 spin group given
by Eq. (2) with A = C4z and H = mmm).

La2CuO4

MnTe

V2Se2O

VNb3S6

Semimetal

Metal

combined with translation or inversion transformation (cf. the opposite-spin sublattices in RuO2 connected by C4z t transformation, shown in Fig. 3a),

Cr2O

FeSb2
3D

Layered

Quasi-2D

FIG. 5. Crystal structrures of selected altermagnetic candidates organized by dimensionality and conduction type. Adapted
from Ref. [7, 15, 16, 67].
D.

Material candidates

The rules from Sec. II.C can be used for highthroughput scanning of altermagnetic material candidates. This section gives an overview of the predicted
range of material types, illustrated on specific examples.
Symmetry prohibits a realization of altermagnetism
in one-dimensional (1D) chains, because of the absence
of rotation transformations in 1D. On the other hand,
Figs. 5-7, and the list of material candidates given below illustrate that altermagnetism can occur in twodimensional (2D) and three-dimensional (3D) crystals,
the conduction types can cover the whole spectrum from
insulators, semiconductors and semimetals, to metals and
superconductors, and the structure and chemistry types
can be also diverse:
• quasi-2D oxide insulator V2 Se2 O [15] or semimetal
Cr2 O [67],
• 3D rutile fluoride or oxide insulators FeF2 [42],
MnF2 [20, 43], MnO2 [17] and metal RuO2 [3, 18],

• perovskite oxide insulators LaMnO3 [22, 68],
CaCrO3 [9] and parent cuprate of high-Tc superconductor La2 CuO4 [16],
• ferrite insulator Fe2 O3 [16],
• pnictide with metal-insulator transition FeSb2 [7,
16] and metal CrSb [16],
• chalcogenide semiconductor MnTe [16]
(semi)metal VNb3 S6 [16], CoNb3 S6 [3],

and

• silicide metal Mn5 Si3 [6],
• organic insulator κ-Cl [4].
Crystallographic and spin groups, and other characteristics of the selected altermagnetic material candidates are
summarized in Tab. III.
A list of crystallographic symmetry groups that in
principle allow for hosting the altermagnetic phase is
given in Ref. [16]. We also point out that altermagnetism
can occur in structures with inversion symmetry (e.g. rutiles), or without inversion symmetry (e.g. VNb3 S6 or
CoNb3 S6 ).

8

(a)

FeSb2

(b) κ-Cl

(c)

Mn5Si3

(d) V2Se2O

Γ

M1

Energy (eV)
Energy (eV)

0
0

-0.2

-0.2

Γ0

M1

K

K

-M2
-M2

A

Γ

L1

A

Γ

L1

H

H

-L2
-L2

A
A

Energy (eV)
Energy (eV)

FIG. 6. (a-d) Ab initio spin-split band structures of depicted altermagnetic candidate materials. Adapted from Ref. [6, 7, 15, 69]

0

-0.2

-0.2

SOI
-M1

-M1

L1
L1

LSOI
2

M1 -M2
M1 -M2

0.5

M2

L2

M2

Energy (eV)
Energy (eV)

0.5
0
0
-0.5

-0.5
-1
-200

0

200

FIG. 7. Altermagnetic candidates identified from ab initio calculations, organizeed
in a Néel temperature vs. altermagnetic
-1
conductivity 200
(S/cm)
spin-splitting strength diagram. Adapted from Ref. [16] and references therein.-200Hall
0

Hall conductivity (S/cm)

9
Space group Spin point group Conduction TN (K) Splitting(meV) Anisotropy Refs.
RuO2
P 42 /mnm 24 /1m 1m 1m
M
400
1400
dxy ,P-2
[3, 18]
KRu4 O8
I4/m
24 /1m
M
300
dx2 −y2 , P-2 [16]
Mn5 Si3
P 63 /mcm 2m 2m 1m
M
∼200 150
dx2 −y2 , P-2 [6]
(Cr,Fe)Sb2 P nma
2m 2m 1m
M
<200
dxy ,P-2
[7]
CaCrO3
P nma
M
90
<200
d-wave,P-2 [9]
CrSb
P 63 /mmc 26 /2m 2m 1m
M
705
1200
g-wave,B-4 [16]
MnTe
P 63 /mmc 26 /2m 2m 1m
I
310
1100
g-wave,B-4 [16]
La2 CuO4 Bmab
2m 2m 1m
I
<317 10
dxy ,P-2
[16]
MnO2
P 42 /mnm 24 /1m 1m 1m
I
<900
dxy ,P-2
[17]
LaMnO3 P nma
I
139,5 20
P-2
[22, 68]
κ-Cl
P nma
I
23
<50
dxy ,P-2
[4]
MnF2
P 42 /mnm 24 /1m 1m 1m
I
67
297
dxy ,P-2
[20, 43]
V2 Se2 O
I
>1000
dx2 −y2 ,P-2 [15]
CuF2
P 21 /c
22 /2m
I
69
350
B-2
[16]
TABLE III. Altermagnetic candidates identified from ab initio calculations. We list the non-magnetic space group, spin point
group, conduction type, transition temperature, and altermagnetic spin-splitting magnitude and anisotropy type. ”P/B–#”
refers to the planar/bulk spin winding number, which around the Γ-point can take a value of 2, 4, or 6 (see Sec. III).
III.

PHYSICAL CONCEPTS

To illustrate the potential and stimulate future research of altermagnetism in a broad condensed-matter
physics field, we now discuss foreseen unique features of
the altermagnetic phase in the context of several overarching physical concepts.
A.

Kramers theorem

Energy bands are Kramers spin degenerate [70, 71]
across the whole Brillouin zone in all crystals that are
invariant under the symmetry transformation that combines T and space-inversion. Lifted Kramers spindegeneracy by breaking this crystal symmetry brings
forth a plethora of physically intriguing and technologically relevant phenomena, ranging from topological
phases of matter [36, 37, 57, 59, 60, 72–74] and dissipationless Hall transport [2, 32, 37], to charge-spin conversion effects in spintronic memory devices [35, 75–77].
For the many decades of spin-physics research, lifting of the Kramers spin degeneracy in energy bands has
been considered to originate from two basic mechanisms.
The first one links the broken space-inversion symmetry
to the spin space by the electron’s relativistic spin-orbit
coupling [78, 79]. It results in inversion-asymmetric spinsplit energy bands, and non-collinear spin textures (e.g.
Rashba) in the momentum space, illustrated in Fig. 8a.
The second mechanism is associated with T -symmetry
breaking by external magnetic field or by internal magnetization of ferromagnets (ferrimagnets) [51]. Microscopically, the latter tends to be dominated by a nonrelativistic magnetic-exchange interaction, and is commonly modelled by a momentum-independent effective
Zeeman term, as illustrated in Fig. 1a.
All magnetically ordered crystals have broken T symmetry. While this directly leads to the effective Zeeman spin splitting of energy bands in ferromagnets, spin

splitting has been commonly considered to be excluded
in crystals with a compensating antiparallel arrangement
of magnetic moments [1, 80–84]. Indeed, there are two
types of Kramers spin-degenerate antiferromagnets.
The first type has a symmetry combining T with
translation t in the antiferromagnetic crystal. The
T t-symmetry defines type-IV magnetic space groups.
Among those, only the antiferromagnetic crystals with
space-inversion symmetry have the Kramers spindegenerate bands. As a result, the bands have T symmetry, (s, k) = (−s, −k), and inversion symmetry, (s, k) = (s, −k), apart from being spin degenerate, (s, k) = (−s, k). Examples are FeRh or MnBi2 Te4
[85, 86]. In the non-relativistic limit and for collinear
antiferromagnetic order (cf. Sec. II.B), the Kramers
spin degeneracy is protected by the spin-group symmetry [C2 k t] alone, i.e., independent of whether the antiferromagnetic crystal is or is not inversion symmetric. We note that the non-relativistic collinear symmetry [C2 k t] does not imply that all materials described
by type-IV magnetic space groups have necessarily vanishing spin splitting in the non-relativistic limit. This
is because type-IV magnetic space groups encompass
also non-collinear magnets. However, all materials from
type-IV magnetic space groups have T -symmetric bands,
whether or not relativistic effects are included.
The second type of antiferromagnetic crystals with
Kramers spin-degenerate bands break space-inversion
and T (or T t) symmetries on their own, but have a symmetry combining the two transformations. In this case,
the Kramers spin-degenerate bands have broken inversion symmetry and broken T -symmetry. Here CuMnAs
or Mn2 Au are among the prominent material examples
[87–91]. The Kramers spin-degeneracy of non-relativistic
bands in these collinear antiferromagnets is protected by
spin symmetry [C2 k Ē],
 in combination with the spinonly group symmetry C̄2 kT (cf. 1st line in Tab. II). In
addition, the [C2 k Ē]-symmetry protects

 T -symmetry
of the non-relativistic bands, and C̄2 kT protects in-

10
version symmetry of bands in the non-relativistic limit.
Breaking of inversion symmetry and T -symmetry in the
band structure of this type of collinear antiferromagnets
is, therefore, purely of relativistic origin.

(a)

(c) Altermagnetic

Relativistic
E

ky

E

kx
ky

(b)

CoA

kx

(d)

Tt

CoB

RuB

RuA

[C2 ||C4 t]

FIG. 8.
(a) Model relativistic Rashba spin-split bands.
(b) Model of antiferromagnetic zero-magnetization crystal of
BiCoO3 with magnetic symmetry T t, and with broken spaceinversion symmetry. (c) Model non-relativistic altermagnetic
spin splitting. (d) Model of altermnagnetic crystal of RuO2
with non-relativistic spin symmetry [C2 k C4 t]. Adapted from
Ref. [16, 92].

While magnets with the compensated magnetic order were commonly associated with spin-degenerate
bands, Zeeman or relativistic spin-splitting mechanisms
were also discussed in antiferromagnets. An effective
ferromagnetic-like Zeeman splitting, and the corresponding T -symmetry breaking in the band structure, was associated in antiferromagnets with a net moment, suggested to occur due to canting, for instance in GdPtBi
[93]. Alternatively, a real Zeeman spin splitting was considered in antiferromagnets due to an external magnetic
field [94–96]. A T -symmetric relativistic Rashba splitting was predicted in antiferromagnets such as BiCoO3
with broken space-inversion symmetry, and with the opposite Co sublattices connected by the T t-symmetry, as
shown in Figs. 8a,b [92]. Another example of an unconventional magnetic and relativistic splitting has been experimentally demonstrated in surface states of antiferromagnetic NdBi [97]. Both of these types of spin splitting
offer intriguing interplay with antiferromagnetism. However, they also inherit a net magnetization (Fig. 1a) or a
non-collinear spin texture (Fig 8a) in the band structure,
characteristic of conventional ferromagnets or relativistic
spin-orbit-coupled systems, respectively.

Lifting of the Kramers spin degeneracy by the altermagnetic phase, illustrated in Figs. 8c,d, is distinct
from the conventional mechanisms. Unlike the relativistic spin-orbit coupling mechanism, it does not require
breaking of the space-inversion symmetry. In fact, the
non-relativistic band structure of altermagnets has the
inversion symmetry protected by the spin-group symmetry corresponding to the co-planarity of the magnetic order, as shown on the 1st line in Tab. II. This applies independently of the presence or absence of inversion symmetry in the magnetic crystal structure [16]. Also unlike
the relativistic spin-orbit coupling mechanism, the nonrelativistic electronic states in the altermagnetic bands
have a common spin-quantization axis and spin is a good
quantum number. These characteristics are protected by
the spin-group symmetry corresponding to the collinearity of the magnetic order, as highlighted on the 2nd line
in Tab. II.
Comparing to ferromagnets, altermagnets share the
strong non-relativistic T -symmetry breaking and spin
splitting in the band structure. In altermagnets, these
characteristics are allowed by the spin-group symmetry
shown on the 3rd line in Tab. II. The distinction from
ferromagnets is that the same spin-group symmetry also
protects the zero non-relativistic net magnetization in altermagnets.

B.

Fermi-liquid instabilities

In Fermi-liquid theory, interactions among electron
quasiparticles are described by Landau parameters in
spin-singlet and spin-triplet channels, using an orbital
angular momentum partial-wave expansion. Large (negative) values of Landau parameters lead to Pomeranchuk
Fermi-liquid instabilities [98, 99]. A prominent example
of an isotropic s-wave instability in the spin-triplet channel is Stoner ferromagnetism, which corresponds to the
momentum-independent effective Zeeman spin splitting
in the electronic band structure.
Theoretically, a rich landscape of quantum ordered
phases is linked to anisotropic (non-zero angular momentum) Landau parameters [99]. However, experimental indications of anisotropic Fermi-liquid instabilities are rare.
An example are nematic-phase instabilities in the spinsinglet channel with non-zero angular momenta. Their
typical characteristics are anisotropic distortions of Fermi
surfaces. Nematic instabilities were considered in fractional quantum Hall systems, Mott insulators or high-Tc
superconductors – all belonging to the family of complex
strongly correlated systems [99].
In analogy to Stoner ferromagnetism, non-zero angular
momentum instabilities in the spin-triplet channel typically break the SU (2) symmetry of the non-relativistic
non-magnetic Fermi liquid [99]. A characteristic feature
of a spin-triplet p-wave instability is a shift of spin-up
and spin-down Fermi surfaces in opposite directions. Unlike Stoner ferromagnetism dominated by the exchange

11

AKE

Energy (eV)

diagram and ab initio bands of RuO2 . Remarkably, the
mechanism is dominated by anisotropic exchange interaction, i.e., it persists without including correlation effects
beyond the local-spin-density approximation [16, 18].
An effective single-particle two-band Hamiltonian that
models
this mechanism contains,uapart
from the common
"BAND_S02_A0001UP.OUT.txt"
1:($2*13.6*2):(($9))
"BAND_S02_A0001DN.OUT.txt"
1:(($2*13.6*2)):(($9))
kinetic-energy
hopping term, au spin-dependent
hopping
due to the anisotropic exchange interaction in the alter-0.5
magnetic state [6, 7, 13]:

Energy (eV)

interaction, and in analogy to the nematic phases, the
spin-triplet p-wave instability was considered in correlated systems, e.g., in heavy fermion compounds [99].
Altermagnetism is not described by a p-wave (or higher
odd-parity wave) instability in the spin-triplet channel.
This is seen from the spin-group symmetry on the 1st
1
line in Tab. II, reflecting the co-planarity
of the magnetic crystal order, and the corresponding inversion symmetry of the spin-split band structure.0 On the other
hand, altermagnetism can be associated with even-parity
wave Fermi liquid instabilities in the -1
spin-triplet channel [16, 18]. We now illustrate on the band structure of
RuO2 that the predicted characteristics-2of the altermagnetic Fermi-liquid instabilities are extraordinary.

H = 2t cos kx cos-1ky + 2tJ sin kx sin ky σz .

1

0
Energy

0

1

-1.5
S'

2

Γ

S

-1

-2

-1.5

S'

S

Γ

s-wave exchange & anisotropic electric crystal potential
1

(c) 1

1

(d) 1
0.5

Energy
(t)
Energy

1

Energy (eV)

0

0

-1

-2
-2

2

2

0
-0.5
-1
-1.5
-2
-2.5

S'

Γ

S'S'
SM
1

Γ
Γ

S
S
M
2

S'

Γ

S

FIG. 9. (a) Schematic diagram of the anisotropic (d-wave) exchange Fermi-liquid instability in the altermagnet. Black line
corresponds to the spin-degenerate band in the non-magnetic
phase while red and blue lines are spin-split bands in the altermagnetic phase. (b) Spin-projected (and orbital-projected)
ab initio bands of RuO2 in the energy window corresponding to (a). (c) Schematic diagram of the isotropic (s-wave)
exchange Fermi-liquid instability combined with anisotropic
electric crystal potential in the altermagnet. Solid and dashed
black lines correspond to the spin-degenerate bands dominated by one or the other sublattice in the non-magnetic
phase, respectively. Red and blue lines are spin-split bands
in the altermagnetic phase. (d) Spin-projected (and orbitalprojected) ab initio bands of RuO2 in the energy window corresponding to (c). Pink boxes with labels ”1” and ”2” correspond to the full ab initio bands of RuO2 shown in Fig. 2c.
Adapted from Ref. [16].

A spin-splitting mechanism due to an anisotropic exchange interaction [13, 18, 20, 21] can be identified in
parts of the RuO2 band structure with a single two-fold
spin-degenerate band in the non-magnetic phase, which
undergoes in the altermagnetic phase an anisotropic
momentum-dependent spin splitting with alternating
sign [16]. This is illustrated in Figs. 9a,b on a schematic

-1.5 is plotted in Figs 10a,b. The
The model band structure
energy spectrum exhibits spin-degenerate nodal surfaces
at kx,y = 0, π, marked in grey in Fig. 10a, and protected
1
by mirror plane symmetries
that transform one spin sub0.5
lattice on the opposite-spin subblatice, and are contained
in the little groups of 0
the nodal-surface momenta (cf.
-0.5 resulting nodal structure and
5th line in Tab. II). The
-1 pattern corresponds to a dxy spin splitting modulation
wave symmetry. The -1.5
characteristic dxy -wave spin-up and
-2 are anisotropic and mutually
spin-down Fermi surfaces
-2.5 the [C2 k C4 ] spin-group symrotated by 90◦ , following
S'
Γ the corresponding
S
metry. ΓAb initioS bands ofS'RuO2 and
model thus illustrate an extraordinary spin-triplet Fermiliquid instability that, unlike the s-wave Stoner ferromagnetism, is anisotropic and, unlike the p-wave heavyfermion compounds, is uncorrelated and occurs in the
even-parity d-wave channel.
Remarkably, the ab initio band structure of RuO2
demonstrates an additional distinct spin-splitting mechanism. In this case, the size and momentum-dependence
of a strong non-relativistic altermagnetic spin splitting is
determined by the band splitting due to an anisotropic
crystal potential of the non-magnetic phase [16]. This
unconventional electric spin-splitting mechanism is illustrated on a schematic diagram in Fig. 9c. In the nonmagnetic state, there are two spin-degenerate bands that
cross at the four-fold spin and orbital-degenerate Γ-point,
while the orbital degeneracy is lifted away from the Γpoint (cf. 8th line in Tab. II). One of the two spindegenerate bands has a dominant projection on one sublattice while the other band on the other sublattice. The
bands are anisotropic due to the anisotropy of the electric
crystal potential (cf. 4th line in Tab. II). The anisotropies
of the spin-degenerate bands corresponding to the two
sublattices are mutually rotated by 90◦ , reflecting the
real-space C4 rotation symmetry which transforms one
crystal sublattice on the other. As a result, there is a
mutual momentum-dependent splitting between the two
spin-degenerate bands away from the Γ-point.
The altermagnetic phase brings an additional
momentum-independent (isotropic) exchange interaction, with opposite sign in the bands corresponding
to opposite-spin sublattices. As a result, two pairs of
spin-split bands form with opposite sign of the spin
splitting. For a given pair, the size and momentumdependence of the spin splitting is a copy of the size and
momentum-dependence of the orbital splitting in the
Energy (eV)

(a)

Energy (eV)

"BAND_S02_A0001UP.OUT.txt"
d-wave exchange u 01:($2*13.6*2):(($9))
"BAND_S02_A0001DN.OUT.txt" u 1:(($2*13.6*2)):(($9))
Model
RuO2
(b)
-1
-0.5
1
Energy (eV)

1

(3)

12
non-magnetic state. The presence of this microscopic
spin-splitting mechanism in RuO2 is again confirmed
by ab initio calculations shown in Fig. 9d. In this case,
the altermagnet can be viewed as two interpenetrating
s-wave Stoner ferromagnets with opposite magnetizations that, due to the interplay with anisotropies of the
electric crystal potential, generate spin-split d-wave-like
Fermi surfaces.

(a) Γ-point spin-winding QP

The potential richness of the landscape of altermagnetic Fermi-liquid instabilities can be further inferred
by inspecting the symmetries of all altermagnetic spin
groups. Each altermagnetic spin point group can be associated with a given minimum even-parity wave anisotropy
of the spin-split Fermi surfaces near the Γ-point [16].
Apart from d-wave, this minimum anisotropy can have
a g-wave or i-wave form [16, 21].

(c) TRIM-valley spin-polarized QP
S

Y
Γ

X

(d)

(b) 2

Energy (t)

Energy (t)

2

0

0

-2
-2
X

(e)

S

Γ

S'

Altermagnetic

Μ2

Μ1

Γ

Y

Relativistic

-K

X

S

Y

Γ

(f)
+K

FIG. 10. (a,b) Model of the altermagnetic quasiparticle with quadratic dispersion around the spin-degenerate Γ-point, and
spin-winding number 2 around the Γ-point. The model corresponds to Eq. (3). (c,d) Model of the altermagnetic spin-polarized
valley quasiparticle with no spin winding in the valley. The model corresponds to Eq. (4). The center of a valley is at TRIM, and
the spin polarization is opposite at TRIM X and Y. (e) Schematic illustration of distinct symmetries of band structures with
non-relativistic altermagnetic and relativistic non-magnetic valleys. (f) Real-space spin-dependent hoppings used to construct
model band structures in (a-c). Adapted from Refs. [6, 7, 13].
C.

Electron and magnon quasiparticles

The predicted extraordinary Fermi-liquid instabilities
in altermagnets can generate a variety of unconventional
electron quasiparticles. An example can be illustrated on
the energy bands of the model two-band Hamiltonian (3)
in the k·p approximation around the Γ-point, highlighted
by a dashed rectangle in Fig. 10b. The spin-dependent
part of the band structure is given by 2tJ kx ky σz . The
spin degeneracy of the Γ-point is generally protected in
altermagnets by the spin-group symmetry [C2 k A], because the Γ-point is invariant under any real-space symmetry transformation (including the rotations A). The
Γ-point spin degeneracy is analogous to the T -symmetric
relativistic bands. Here an example is the Rashba model

whose spin-dependent part is given by λ (kx σy − ky σx )
(Fig. 8a). However, unlike the linearly dispersing quasiparticles around the Γ-point of the inversion-asymmetric
relativistic bands, the altermagnetic quasiparticles in the
above model have a quadratic dispersion around the Γpoint, in line with the general inversion symmetry of
bands in altermagnets (cf. 1st line in Tab. II).
The altermagnetic quasiparticles are spin polarized
away from the Γ-point and can be assigned a spinwinding number. In analogy to relativistic systems, the
spin-winding number describes how many times spin reverses when completing a closed path around the Γ-point.
However, the spin-winding number of the above altermagnetic quasiparticle model is 2, in contrast to the spinwinding number 1 in the relativistic Rashba model. The

13
spin-winding numbers around the Γ-point in altermagnets have even-integer values, again because of the inversion symmetry of the bands. The spin winding of the altermagnetic quasiparticles can be planar (cf. relativistic
Rashba or Dresselhaus spin-textures) or bulk (cf. relativistic Weyl spin-texture) [16]. The allowed even-integer
values are 2, 4 or 6 in the vicinity of the Γ-point, and are
determined by the spin-group of the altermagnet [16].
This illustrates to potential richness of the spin-polarized
quasiparticles in altermagnets around the Γ-point.
We point out that the spin-winding number in the relativistic systems is associated with continuously varying
spin direction in the momentum space. In contrast, altermagnets show that non-zero integer invariants, describing how many times the quasiparticle spin reverses when
completing a closed path around the Γ-point, can exist also in systems where all spins share a common spin
quantization axis, and spin is a good quantum number.
A different type of predicted altermagnetic electron
quasiparticles can be illustrated on a two-band model
Hamiltonian [6, 7, 13]:
H = ±2tJ (cos kx − cos ky ) σz ,

(4)

whose energy spectrum is shown in Fig. 10d. (Around
the Γ-point, Eq. (4) is related to the model in Eq. (3) by
a 45◦ rotation of the momentum space, and by setting
t = 0).
In the k · p approximation around time-reversal invariant momenta (TRIMs) X and Y, highlighted by dashed
rectangles in Fig. 10d, the spectrum takes a form of spinsplit valleys given by (see Figs. 10c,d),
E± (X, k) = ±tJ (4 − k 2 ),
E± (Y, k) = ∓tJ (4 − k 2 ).

(5)

(Recall that a momentum k is time-reversal invariant
when it differs from −k by a reciprocal lattice vector.)
The spin-group symmetry condition allowing for the
spin-split TRIMs is given on the 7th line in Tab. II. The
possibility to observe spin-split valleys around TRIMs in
real materials is predicted by ab initio band structure calculations of the altermagnetic phase in, e.g., Mn5 Si3 [6]
(Fig. 6c). Besides 3D crystals, the altermagnetically spinsplit valleys can also form in 2D materials [15, 23, 100],
as predicted, e.g., in ab initio calculations of the band
structure of a monolayer insulator V2 Se2 O [15] (Fig. 6d).
Locally, the individual valleys around the X and Y
TRIMs are isotropic in the above model. This illustrates
that altermagnets can host spin-polarized quasiparticles
analogous to the model non-relativistic s-wave Stoner ferromagnet, with no spin winding around the TRIM. However, unlike ferromagnets, the altermagnetic spin-group
symmetries impose that each spin-split TRIM has a counterpart TRIM elsewhere in the Brillouin zone with opposite spin splitting. The presence of these TRIM pairs is
protected by the [C2 k A] [E k H] spin-group symmetries
(cf. 3rd line in Tab. II).

The altermagnetic spin-polarized quasiparticles in separate local valleys in the momentum space are reminiscent of relativistic spin-polarized valley-quasiparticles in
non-magnetic hexagonal 2D materials, such as transition metal dichalcogenides [101]. The common features
shared by the altermagnetic and relativistic quasiparticles are the opposite spin polarization in valleys occupying different parts of the Brillouin zone, and the zero net
spin polarization when integrated over the whole Brillouin zone. However, only altermagnets allow these valleys to be centered at TRIMs, as highlighted in Fig. 10e.
In the non-magnetic relativistic systems, spin splitting is
excluded by T -symmetry not only at the Γ-point, but at
all TRIMs.
So far we discussed the electron quasiparticles from the
symmetry perspective limited to the spin-group transformations acting on the spin and momentum-dependent
band structure. Additional rich quasiparticle physics,
including higher-order degeneracy quasiparticles, can
emerge from the analysis of spin-group transformations
acting on the electron wavefunctions (spin-group representations) [16, 24, 62, 64].
Besides the electron energy spectra and quasiparticles,
we foresee that the real-space symmetries of the altermagnetic crystal structure will be also reflected in unique
characteristics of the spin-wave spectra and magnon
quasiparticles [102].
The typically leading contribution to the magnon spectra can be obtained by mapping the spin-dependent electronic
P structure on the Heisenberg Hamiltonian, H =
− i6=j Jij êi êj [64, 103, 104]. Here êi is the direction
of the magnetic moment around an atom at position Ri ,
and Jij are Heisenberg exchange coupling parameters. In
the Heisenberg model, the real and spin space transformations are decoupled and the symmetries of the corresponding magnon bands can be described by the nonrelativistic spin-group formalism [26, 64].
In antiferromagnets, translation or inversion symmetry transformations connecting opposite-spin sublattices
protect double-degeneracy of the magnon spectra [26, 64].
This has been commonly illustrated on the opposite-spin
sublattices of rutile crystals, while omitting the presence
of non-magnetic atoms in these crystals [26, 64, 105]. We
have seen in Sec. II, however, that the non-magnetic Oatoms in rutile RuO2 (or F-atoms in rutile FeF2 and
MnF2 ) break the translation and inversion symmetries
connecting the opposite-spin sublattices. Instead of classic antiferromagnets [26, 44, 64, 105], rutiles are the prototypical representatives of altermagnetism, with interlinked unique properties of the real-space crystal structure and momentum-space electronic and magnonic band
structures [102].
In analogy to the electronic band structure, the doubledegeneracy of magnon bands is predicted to be lifted
in altermagnets, with the sign of the splitting alternating across the magnon Brillouin zone [102]. Magnons
in altermagnets can also feature antiferromagneticferromagnetic dichotomy. The dispersion of altermag-

14
netic magnons can be linear around the degenerate Γpoint, in analogy to antiferromagnets, while the Landau
damping in altermagnets can be comparably low to the
damping of magnons in ferromagnets due to the comparably large spin splitting of the electron quasiparticles
[102, 104].
D.

Berry phase and non-dissipative transport

Berry phase is a general concept in quantum mechanics [106]. A prototypical example is the Aharonov-Bohm
phase given by a real-space path integral of the electrodynamic vector potential along a closed loop or, equivalently, by an integral of the magnetic field over an area
enclosed by the loop. The phase can be macroscopically
observable by resistance oscillations in an applied magnetic field.
In the crystal momentum space, a Berry connection
analogue of the electrodynamic vector potential, and a
Berry curvature analogue of the magnetic field,
An (k) = ihunk |∇k unk i
Bn (k) = ∇k × An (k),

(6)

can also generate macroscopic observables. A prominent
example is the non-dissipative Hall current given by the
transverse conductivity [32],
Z
d3 k
e2 X
Hall
f [εn (k)]Bnz (k).
(7)
σxy
=−
~ n BZ (2π)3
Here f [εn (k)] is the Fermi-Dirac distribution function,
εn (k) is the energy of the Bloch state in band n with
crystal momentum k, and unk (r) is the periodic part of
the Bloch wavefunction.
Altermagnets are predicted to bring unique elements
into the physics of Berry phase phenomena [2, 3, 5–
7, 39, 40]. The Berry curvature near the Γ-point of a
k · p altermagnet-Rashba model [2], tk 2 + 2tJ kx ky σz +
λ (kx σy − ky σx ), is given by
2tJ λ2 kx ky
B(k)± = ∓ p 2
.
4tJ (kx ky )2 + λ2 k 2

(8)

Eq. (8) illustrates that the characteristic even-parity
wave (d-wave) anisotropy in the non-relativistic band
structure of altermagnets can be also reflected in their
relativistic Berry curvature. In contrast, a counterpart
ferromagnet-Rashba model, tk 2 +∆σz +λ (kx σy − ky σx ),
gives an isotropic Berry curvature near the Γ-point
[2, 32, 107–110], reflecting the principally isotropic swave nature of ferromagnetism.
The Berry curvature tends to reach the highest values near band (anti)crossings [2, 32], which implies another outstanding feature of altermagnets. In contrast
to the typically accidental (anti)crossings in ferromagnets, the spin-group symmetries of altermagnets impose
the presence of the nodal lines or nodal surfaces in the

band structure (cf. 5th line in Tab. II). When the
relativistic spin-orbit coupling is included, these nodal
lines or surfaces (which may be weakly gapped by the
spin-orbit coupling) become symmetry-defined Berrycurvature hotspots. This is illustrated in Fig. 4 on relativistic ab initio band structures of RuO2 and FeSb2
[2, 7, 13].
Since T is antiunitary in quantum mechanics, the
Berry curvature (6) is odd under T , T Bn (k) =
−Bn (−k). It implies that the integral in Eq. (7) vanishes in T -symmetric band structures. Breaking of T symmetry in the band structure of altermagnets is, therefore, the key property that allows for the observation of
macroscopic responses, such as the anomalous Hall effect
[2, 3]. Recent experiments [5] have detected the anomalous Hall effect in RuO2 of a comparable strength to typical Hall signals in ferromagnets. This is consistent with
the predicted strong altermagnetic T -symmetry breaking in the band structure of this compensated collinear
magnet [3, 5] (cf. Tab. I).
RuO2 is an example in which the lattice of the magnetic Ru atoms alone would have the opposite-spin sublattices connected by a translation. As mentioned above,
this symmetry would imply T -symmetry of the band
structure (and in combination with inversion symmetry
of the crystal also spin degeneracy). The presence of
the non-magnetic oxygen atoms is, therefore, essential
for the T -symmetry breaking (and spin splitting) in the
altermagnetic band structure of RuO2 and, consequently,
for the anomalous Hall effect [3]. The term crystal Hall
effect [3, 7, 39, 111] was introduced to highlight this feature. One of the implications, unparalleled in the conventional anomalous Hall effect in ferromagnets, is that
the crystal Hall effect in altermagnets is predicted to flip
sign not only when reversing the magnetic moments, but
also when the symmetry-breaking arrangement of nonmagnetic atoms reverses between the two magnetic sublattices [3].
Finally, we recall that in 2D systems, Eq. (7) turns into
a surface integral proportional to the Berry phase, which
becomes quantized when the integration covers the full
Brillouin zone in 2D insulators [112]. The corresponding
quantum Hall effect [113] was demonstrated in graphene
at room temperature [114] but it requires a strong magnetic field. The ferromagnetic quantum anomalous Hall
counterpart [115] can be observed at zero magnetic field
but, so far, has been limited to Kelvin temperatures
[37, 116]. Since altermagnetism can host the Berry phase
phenomena, and can occur in 2D crystals and in insulators, it opens new possibilities in the search for hightemperature zero-field quantum Hall phenomena. For a
further in-depth discussion of Berry phase physics and
non-dissipative Hall transport in altermagnets we refer
to the recent topical review [2].

15
IV.

RESEARCH AREAS

We now move to the discussion of the potential of altermagnetism in specific areas of condensed-matter research. We start from spintronics in which, besides the
anomalous Hall effect, initial theory predictions have
been recently supported by experiments.
A.

Spintronics

The T -symmetry broken electronic structure in ferromagnets is split into majority and minority spin bands.
This results in different conductivities of the two spin
channels, which makes electrical currents in ferromagnets spin polarized. Passing the spin-polarized current
between a reference and a sensing/recording ferromagnetic electrode in a multilayer structure can generate
giant magnetoresistance (GMR), tunneling magnetoresitance (TMR), and spin-transfer torque (STT) effects.
These principally non-relativistic strong responses underpin reading and writing of information in commercial
spintronic devices [75–77].
A STT mechanism in Kramers spin-degenerate antiferromagnets, proposed more than a decade ago [81], differs fundamentally from STT in ferromagnets. The theoretical model considered a transmission of a staggered
spin polarization from one to the other antiferromagnet,
The strong non-relativistic T -symmetry breaking and
spin splitting in altermagnetic bands directly opens the
possibility to not only replicate the concepts known from
ferromagnets, but also to enrich non-relativistic spintronics by new effects and functionalities linked to the zero
net magnetization [4, 8–15].
The anisotropy of the split and equally populated
spin-up and spin-down Fermi surfaces in altermagnets
(cf. Figs. 10a,b) results in spin-dependent anisotropic
group velocities, ∂E+ (k)/∂ki 6= ∂E− (k)/∂ki , where +/−
refers to the spin index. The corresponding conductivities are also spin-dependent and anisotropic. Considering x and y-direction as the anisotropic axes of the
spin-split Fermi surfaces, σ+,xx 6= σ−,xx , σ+,yy 6= σ−,yy ,
and σ±,xx = σ∓,yy . The electrical current then becomes
spin-polarized when the bias is applied along the x or ydirection, as schematically illustrated in Fig. 11a. Moreover, as a consequence of the T -symmetry breaking of the
spin-split bands, the sign of the spin polarization reverses
when reversing the altermagnetic order vector.
The above non-relativistic spin-current characteristics
are analogous to ferromagnets. In contrast to ferromagnets, the altermagnetic spin splitting is also predicted to
cause the reversal of the spin polarization of the current
when the applied electrical bias is flipped between the x
and y-direction.
The spin-polarized current directly implies a GMR effect in a stack comprising two altermagnets, separated
by a conductive non-magnetic spacer, with the altermagnetic order vectors oriented either parallel or antiparallel,

where the spin polarization and the antiferromagnetic orders in the electrodes were all commensurate. This is a
subtle, spin-coherent quantum-interference phenomenon
relying on perfectly epitaxial commensurate multilayers [81, 117–119]. Similarly delicate were the proposed
GMR/TMR effects in these antiferromagnetic structures
[117]. This may explain why experimentally, the viability of non-relativistic spintronic concepts in the conventional spin-degenerate antiferromagnets has not been
demonstrated to date.
As a result, the attention in the research of spintronics in Kramers spin-degenerate antiferromagnets turned
to relativistic phenomena [34]. Anisotropic magnetoresistance, which can be used to detect a 90◦ reorientation of the antiferromagnetic Néel vector [120], is an
example generally applicable to both types of Kramers
spin-degenerate antiferromagnets because it is an evenunder-T macroscopic response (cf. Sec. III.A). A 2nd order magnetoresistance, which can be used to detect a
180◦ reorientation of the Néel vector, is an example of
an odd-under-T response that occurs only in the second type of Kramers spin-degenerate antiferromagnets
with T -symmetry broken and inversion-symmetry broken band structures [121]. These magnetoreristance responses, as well as the spin-orbit torque (SOT) phenomena used to electrically induce the Néel vector reorientation [87], tend to be weak, owing to their relativistic
origin.
as illustrated in Fig. 11b. The GMR magnitude can be
estimated from the conventional current-in-plane GMR
expression derived in ferromagnets [75],
GMR =

1
1
(Rσ +
− 2),
4
Rσ

(9)

where Rσ = σ+,xx /σ−,xx = σ+,xx /σ+,yy = σ−,yy /σ−,xx .
Ab initio calculations in RuO2 give GMR reaching a
100% scale [13] (Fig. 11e), highlighting the expected large
GMR ratios in altermagnets.
As noted above, the polarization of the longitudinal
spin-polarized current in altermagnets is predicted to reverse not only with the reversal of the altermagnetic order
vector but also with the reorientation (e.g. by 90◦ ) of the
applied electrical bias. A directly related effect, also unparalleled in ferromagnets, is illustrated in Fig. 11c. For
a bias applied in the diagonal direction between the two
anisotropy axes of the spin-split Fermi surfaces, the longitudinal current is unpolarized. However, a spin-current
is generated in the transverse direction. The effect has
been predicted in a range of inorganic and organic materials [4, 8, 9, 15]. The altermagnet acts here as an
electrical spin-splitter, with a propagation angle between
spin-up and spin-down currents reaching 34◦ in RuO2 [8].
The corresponding charge-spin conversion ratio reaches
remarkable 28% (Fig. 11e), and the spin-conductivity is
a factor of three larger than the record value from a survey of 20,000 non-magnetic relativistic spin-Hall materials [122].
The outstanding charge-spin conversion characteristics

16

(a) Longitudinal spin-current

(b) Giant magnetoresistance

(c) Transverse spin-current

(d)
jS

(e)

Spin-splitter torque
n(m)

n(θ)

AM(FM)
E

AM

FIG. 11. (a) Schematics of the longitudinal spin-current in altermagnets. For an electric bias E applied along one of the
main anisotropy axes of the spin-split Fermi surfaces, the spin-up and spin-down charge currents are parallel but of different
magnitudes due to the Fermi surface anisotropies. As a result, the longitudinal charge current is spin-polarized. (b) Schematics
of a GMR stack in a current-in-plane geometry. As an example, we show the antiparallel configuration of the altermagnetic
order vectors in the two electrodes AM1 and AM2 . Interfaces are oriented along one of the main anisotropy axes of the spin-split
bands. Energy band cuts highlight the anisotropy around the Γ-point, resulting in anisotropic spin-dependent conductivities. (c)
Schematics of the transverse spin-current. For E applied in the diagonal direction between the two anisotropy axes of the spinsplit Fermi surfaces, the spin-up and spin-down charge currents combine in an unpolarized longitudinal charge current and in a
pure transverse spin-current. (d) Spin-splitter-torque concept on a schematic of altermagnetic / altermagnetic (ferromagnetic)
bilayer. A spin-current from the bottom altermagnet propagates in the out-of-plane direction and generates a spin-splittertorque on the altermagnetic (or ferromagnetic) order vector in top layer. (e) Ab initio longitudinal spin-up and spin-down
conductivities (red and blue), GMR, and the ratio of the transverse spin current relative to the longitudinal charge current
(SCR) in RuO2 . Adapted from Refs. [8, 13].

of altermagnetic RuO2 prompt a theoretical proposal of a
spin-splitter torque (SST) [8], in part already supported
by initial experiments [10–12] (cf. Tab. I). In the geometry schematically illustrated in Fig. 11d, an in-plane bias
generates the non-relativistic spin-current in the altermagnetic film along the out-of-plane direction, with the
polarization of the spin-current controlled by the orientation of the altermagnetic order vector. The spin current
then exerts a torque on the adjacent altermagnetic (or
ferromagnetic) layer. SST does not inherit the problems
of STT associated with the out-of-plane direction of the
applied electrical bias [76, 123]. Instead, it shares the inplane electrical-bias geometry of the SOT generated by
the relativistic spin-Hall polarizer, while circumventing
the limitations of the more subtle relativistic spintronic
effects [35].
Another foreseen non-relativistic spintronic effect is an
altermagnetic variant of the TMR in a tunnel junction
with an insulating spacer separating the two altermag-

netic electrodes [13, 14]. The altermagnetic TMR can
be illustrated on the model band structure with spinspit valleys (cf. Figs. 10c,d). The pairs of valleys with
opposite spin polarization result in the equal net population of spin-up and spin-down states, while the densities of states within a given valley become spin dependent, n+ (M1 ) 6= n− (M1 ), n+ (M2 ) 6= n− (M2 ), and
n± (M1 ) = n∓ (M2 ). For tunneling which conserves the
valley index, parallel and antiparallel configurations of
altermagnetic order vectors in the two layers, illustrated
in Fig. 12a, are predicted to give different conductances,
in analogy to ferromagnetic TMR. This can be seen by
applying the Jullière formula [75] per valley [13],
TMR =

1
1
(Rn +
− 2),
2
Rn

(10)

where the ratio of the spin-up and spin-down densities of
states in the valley is given by, Rn = n+ (M1 )/n− (M1 ) =
n+ (M1 )/n+ (M2 ) = n− (M2 )/n− (M1 ).

17
Ab initio calculations of ∼ 100% TMR ratios in RuO2
(Fig. 12b) or Mn5 Si3 [13, 14] illustrate the potential for
achieving large TMR responses in tunnel junctions with
altermagnetic electrodes.
Finally, we note that symmetry-wise, TMR is in principle expected in all altermagnetic spin groups [13], and
can reach large magnitudes as long as the spin-polarized

(a)

quasiparticles are well separated in the momentum space
to provide for the sufficiently decoupled spin transport
channels (Fig. 12c). On the other hand, the GMR derived from the anisotropy of the macroscopic (averaged
over momentum) spin-dependent conductivities, is predicted to be allowed only in selected altermagnetic spin
groups [13, 16].

Parallel

AM1

Tunneling
barrier

Antiparallel

AM1

AM2

(b)

Tunneling
barrier

AM2

(c)

FIG. 12. (a) Schematics of a TMR stack with an insulating barrier and altermagnetic electrodes with parallel and antiparallel
order vectors. Energy band cuts highlight the oppositely split valleys, resulting in valley and spin-dependent densities of
states. (b) Ab initio quantum-transmission calculations of the TMR in a RuO2 | TiO2 | RuO2 tunnel junction. (c) Model
spin and transport-momentum projected band structure, and relative difference between the conductances in the parallel and
antiparallel configuration of the altermagnetic order vectors in the two electrodes. The TMR is maximized for transport energies
corresponding to the spin-split valleys well separated in momentum. Adapted from Refs. [13, 14].
B.

Ultra-fast optics and neuromorphics

Achieving energy efficient fast switching is among the
key outstanding problems in spintronics [124, 125]. The
principally isothermal reorientation switching of magnetization in ferromagnets has a threshold when the electrical writing pulse-length is scaled down to the magnetization precession time-scale. This is determined by
the inverse of the magnetic resonance frequency which in
ferromagnets is typically in the GHz-range. The corresponding threshold writing pulse-length is then in the nsrange. For longer pulses, the switching current amplitude
is almost independent of the pulse length and, therefore,
the writing energy (Joule heating) linearly decreases with
decreasing pulse length. Below the threshold, however,
the writing current amplitude has to increase to keep the

magnetization precession time-scale comparable to the
pulse length. The energy in this regime starts to linearly increase with decreasing pulse length, making the
switching prohibitively energy-costly [124, 126–128]. The
∼ ns threshold of electrical writing pulse-lengths in ferromagnets applies to switching via current-induced Oersted
fields, as well as to the spintronic STT or SOT switching
mechanisms.
One of the driving ideas behind the antiferromagnetic
spintronics research has been the prospect of fast SOT
switching, enabled by the antiferromagnetic resonance
frequencies reaching a THz-scale [34, 129]. While in
ferromagnets the resonance frequency is determined by
the weak magnetic-anisotropy energy, in antiferromagnets it scales with the geometric mean of the magneticanisotropy energy and the strong exchange energy responsible for the antiparallel magnetic order [130].

18
Altermagnets can share with antiferromagnets the
exchange-enhanced resonance frequency, favorable for
achieving energy efficient reorientation switching at pulse
lengths well below ∼ ns. Unlike antiferromagnets, as discussed in Sec. IV.A, they are also predicted to enable
the favorable non-relativistic spin-torque mechanisms of
current-induced switching, as well as the readout by the
strong non-relativistic GMR/TMR responses.
A conceptually different approach to achieve higher
magnetization dynamic frequencies in ferromagnets, and
by this comparably higher writing speeds, is to utilize
the large exchange energy by exciting finite wave-vector
spin-waves. The process can be triggered, e.g., by strong
heating laser pulses [131, 132], and involves demagnetization of the ferromagnet. This brings us to the frontier research of ultra-fast switching in magnets by optical
fs-laser pulses [125]. The optical switching mechanisms
are principally distinct from the reorientation switching
of magnetization by Oersted fields or effective currentinduced spin-torque fields. The ultra-fast reorientation
switching by fs-laser pulses can involve, e.g., unequal
demagnetization/remagnetization dynamics of different
spin-sublattices in ferrimagnets, or demagnetization followed by domain-nucleation and expansion in ferromagnets [125]. The fundamental distinction between switching principles when using electrical and optical excitations splits spin-electronics and opto-spintronics in ferromagnets (ferrimagnets) into largely independent research
and development fields.
Recently, materials used in the antiferromagnetic spintronics research have opened a possibility to bridge the
electrical and optical switching by a unifying mechanism
that is principally different from all the above mechanisms based on the reorientation of the average magnetic order vector. Over the full range from ms electrical pulses to fs-laser pulses, the antiferromagnet can
be demagnetized and then quenched into a metastable
nano-fragmented antiferromagnetic domain state with
a higher resistivity than the uniform antiferromagnetic
ground state [133]. This quenching of the antiferromagnet into the multi-domain state does not involve a control of the mean orientation of the Néel vector. Once
the system is quenched into the complex magnetic textures after the electrical or optical excitation, the lack of
long-range stray fields in the antiferromagnetic crystals
can inhibit efficient removal of the non-equilibrium magnetic textures [133]. Since the required switching energy
is associated with bringing the system by the electrical or
optical excitation to the antiferromagnetic-paramagnetic
transition, it does not show the unfavorable increase of
the switching energy with decreasing pulse length, typical of the fast current-induced precessional reorientation
switching in ferromagnets.
Resistivity increase in the quenched state on the ∼
10 − 100% scale, and insensitivity to extreme magnetic
fields [133, 134], have been associated with the pulseinduced formation of atomically-sharp domain walls in
the antiferromagnetic film corresponding to an abrupt

flip of the sign of the Néel vector between two neighboring
atomic planes [135]. Thanks to the latest developments in
scanning transmission electron microscopy (STEM) with
sub-unit cell spin resolution [135, 136], the presence of
stationary atomically-sharp domain walls in the antiferromagnet has been visualized by direct imaging [135].
While so far explored in the Kramers spin-degenerate
antiferromagnets, quenching into the atomic-scale magnetic textures with pulse lengths ranging from ms down
to fs-scales may be equally applicable to altermagnets,
since they share with antiferromagnets the stray-fieldfree compensated magnetic ordering. Moreover, in altermagnets, each atomically-sharp domain wall separating
domains with opposite sign of the altermagnetic-order
vector can be viewed as a local GMR/TMR junction
that is self-assembled, and represents the ultimate downscaling of the width of the junction spacer. This additional GMR/TMR contributions to the resistances of the
atomically-sharp domain walls, absent in the Kramers
spin-degenerate antiferromagnets, can be expected to significantly enhance the resistive switching signals of the
quenched multi-domain (multi-domain-wall) states in altermagnets.
The above prospect of information coding down to
atomic length-scales and fs time-scale gives a strong
incentive for further development of microscopies with
ultra-high spatial and temporal resolution, and with both
charge and spin sensitivity. Recently reported STEM
images of altermagnetic ferrite Fe2 O3 with sub-unit cell
spin resolution represent a major step in this direction
[135, 136]. Another recent progress in scanning-probe
microscopy imaging of anisotropic charge distribution on
individual atoms [137] can facilitate a complementary insight into the microscopic spin-splitting mechanism (cf.
4th line in Tab. II and Sec. III.B), and the corresponding GMR/TMR mechanism in the altermagnet on the
nano-scale. High temporal resolution can be achieved
in pump-probe fs-laser experiments. They can utilize
expected large changes in reflectivity [133] of the altermagnet, that accompany the large quenching-induced resistive changes. Optical reflectivity can substitute here
the more elaborate and subtle magneto-optical detection
of dynamics of the magnetic-order vector, conventionally employed in the reorientation switching experiments
[125].
Apart from the interest in the area of ultra-fast optical switching by fs-laser pulses, the quenching mechanism
can have potential applications in neuromorphic computing. The quenching mechanism facilitates highly reproducible reversible analog switching and relaxation characteristics, reminiscent of spiking neural-network components [133, 138–141]. For example, the time dependence
in the studied antiferromagnets of the resistivity after
the pulse-excitation has a universal smooth form of a
Kohlrausch stretched-exponential relaxation [142]. This
can be used in neuromorphic circuits to mimic the neuron’s leaky integration, or to detect the pulse order and
delay that determine the synaptic weights [140, 143]. The

19
smooth analog switching and relaxation functions are
distinct from ferromagnetic neuromorphic devices whose
characteristic behavior are stochastic fluctuations between two states with opposite magnetization [144, 145].
Finally, we point out that the foreseen altermagnetic
neuromorphic devices with the ms-fs scalability of the
writing pulse-length, reversible and reproducible analog
time-dependent switching and relaxation characteristics,
and with strongly enhanced resistive switching signals by
the local GMR/TMR at atomically-sharp domain walls,
represent an attractive complementary research direction
to the more traditional charge-based neuromorphic devices. Charge memristors led to successful demonstrations of analog synapses in proof-of-concept artificial neural networks [146]. However, the ionic transport nature
of their operation, that facilitates large resistive switching signals and the memristive characteristics, also imposes principle endurance and speed limitations [147].
These limitations are absent in the spintronic neuromorphic devices, including the foreseen altermagnetic neuromorphic components, as they rely on the manipulation
of the charge and spin of electrons.

C.

Thermoelectrics, field-effect electronics and
multiferroics

The key merit of ferromagnets from energy-saving perspective is non-volatility, i.e., that they can store information even when power is switched off. On the other
hand, electrical reading and especially writing information into ferromagnetic memory devices can generate significant Joule heating [75]. This can be directly harvested
during the writing process in which the elevated temperature effectively reduces the equilibrium energy barrier
separating the states with opposite magnetization orientation. In the latest generation of hard disks, elevating the temperature of a bit while recording is provided
through an external laser heat-source. Similarly, the alloptical switching by laser pulses via the demagnetization
processes mentioned in Sec. IV.B is typically accompanied by significant heating effects. This brings us to a
discussion of how altermagnetism, rather the generating
heat, can contribute to energy harvesting in devices combining heat, charge and spin phenomena.
Ferromagnets have been considered for a direct heat
conversion to electricity [148]. Here the anomalous
Nernst effect, a thermo-electric counterpart of the
anomalous Hall effect, is regarded as an attractive candidate phenomenon [149]. The anomalous Nernst effect
generates an electric field in a transverse direction to the
thermal gradient. Particularly in thin-film or nanostructured heat-charge conversion device, the transverse geometry can significantly enhance the conversion efficiency
compared to the conventional longitudinal Seebeck effect
[149]. A complementary research area to the anomalous
Nernst effect are thermal counterparts of the GMR/TMR
and STT phenomena. Here the energy harvesting con-

cept is based on employing heat gradients, instead of
electrical bias, to directly read or write information in
a memory device [148].
Altermagnets significantly enlarge the material landscape for realizing and optimizing these thermo-electric
responses that originate, in analogy to their electronic
counterparts, from the T -symmetry broken spin-split
band structure. Unlike the typically metallic ferromagnets, altermagnets are predicted to span a broad
range of conduction types (cf. Sec. II.D). This is favorable because, from a general thermo-electric perspective,
semimetals or semiconductors are more suitable material types than metals due to the strong dependence of
their electronic structure on energy near the Fermi level.
A particularly intriguing case in this context are materials showing a metal-insulator transition. Among the
altermagnetic candidate materials, FeSb2 [7, 16] is an
example in which earlier studies reported an extraordinary (spin-independent) thermo-electric response, linked
to the metal-insulator transition [150].
Similar to thermoelectrics, the non-metallic materials
are favorable for field-effect electronics. A research of
ferromagnetic semiconductors, in particular of the Mndoped III-V compounds, was motivated by the prospect
of integrating spintronics with field-effect transistor functionalities in one material [151]. Because magnetism is
carrier-mediated in these materials, one of the driving
ideas in this area of research was the control of the magnetic order by electrostatic gating effects [152]. Research
of devices based on the III-V semiconductors also led
to discoveries of the spin Hall effect and SOT, that gave
birth to the field of relativistic spintronics [33, 35]. These
successes, on one hand, and the failure to achieve high
ferromagnetic transition temperatures in these semiconductors, on the other hand, provided one of the key incentives driving the research field of antiferromagnetic
relativistic spintronics [34]. Altermagnets open a new
prospect of materials combining not only high magnetic
transition temperatures with non-metallic band structures, but also with the strong non-relativistic spintronic
responses generated by the T -symmetry breaking and
spin splitting in the energy bands.
Multiferroic materials [153] can complement the magnetic semiconductors by offering a non-volatile electric
control of magnetism via the internal coupling between
the ferroelectric and magnetic orders. Only insulating
materials can be ferroelectric, otherwise the free carriers
would screen out the electric polarization. This again disfavors ferromagnets that are mostly metallic. The prominent multiferroic materials are non-centrosymmetric perovskite oxides with a compensated magnetic order [153].
As shown in Sec. II.D, altermagnetism is compatible with
this material family. Here CaMnO3 is an example multiferroic [154], that is also a material candidate for hosting
the altermagnetic phase [16].

20
D.

Superconductivity

The family of insulating perovskite oxides brings us
to its prominent cuprate member La2 CuO4 that, upon
doping, turns into a high-temperature d-wave superconductor [155]. The recognition that this cuprate crystal
belongs to an altermagnetic spin group with a d-wave
character of the spin-momentum locking [16] brings us
to foreseen research of the interplay of altermagnetism
and superconductivity [16, 156]. Research in this context may include areas such as the coexistence of altermagnetism and unconventional superconductivity with
anisotropic Cooper pairing [157], altermagnetic fluctuations as a pairing mechanism [157], or phenomena at
altermagnet/superconductor interfaces [158, 159].
Since altermagnets have spin-degenerate nodal lines or
surfaces protected by the spin-group symmetries, a spinsinglet Cooper pairing may occur for the corresponding
momenta, in analogy to conventional antiferromagnets.
For the spin-singlet case, the 2 × 2 Cooper-pair potential
ˆ
matrix (gap function or order parameter), ∆(k),
satisfies ∆↑↑ (k) = ∆↓↓ (k) = 0, ∆↓↑ (k) = −∆↑↓ (k), and
∆↑↓ (k) = ∆↑↓ (−k) [157]. The matrix is unitary, with
corresponding zero net spin average of the pairing state,
and describes even-parity wave Copper pairing, including
the anisotropic, e.g., d-wave pairing.
On the other hand, the altermagnetic spin-group symmetries also allow for spin-split and broken T -symmetry
parts of the Brillouin zone where, (s, k) 6= (−s, −k)
and AH k 6= k (cf. 3rd and 6th line in Tab. II). These
momenta can support spin-triplet Cooper pairing. In
analogy to ferromagnets, the spin-triplet Cooper-pair
potential matrix corresponding to a spin-split spin-up
ˆ (↑) (k), takes a form,
Fermi surface of the altermagnet, ∆
(↑)
(↑)
(↑)
(↑)
∆↑↓ (k) = ∆↓↑ (k) = ∆↓↓ (k) = 0, and ∆↑↑ (k) =
(↑)

−∆↑↑ (−k) [157]. The matrix in this case is non-unitary
and describes odd-parity wave Copper pairing [157]. Unlike ferromagnets, however, the altermagnetic spin-group
symmetries impose the presence of a counter-part spinˆ (↓) (k0 ) that
down Fermi surface with a corresponding ∆
(↓) 0
(↓) 0
(↓) 0
(↓)
satisfies, ∆↑↓ (k ) = ∆↓↑ (k ) = ∆↑↑ (k ) = 0, ∆↓↓ (k0 ) =
(↓)

(↓)

(↑)

−∆↓↓ (−k0 ), and ∆↓↓ (k0 ) = ∆↑↑ (k), where k0 = AH k.
On one hand, altermagnets can thus share with ferromagnets the spin-triplet symmetry of Cooper pairing
while, unlike ferromagnets on the other hand, a zero net
spin average of the spin-triplet superconducting state is
protected by the altermagnetic spin-group symmetries.
In the context of unconventional supercoductivity, the
ferromagnetic-antiferromagnetic dichotomy of altermagnetism, as well as the features unparalleled in neither
the conventional ferromagnets or antiferromagnets, mirror the discussion in the previous sections.
Apart from the compatibility of altermagnetism with
the different types of Cooper pairing, altermagnetic fluctuations can provided earlier unexplored mechanisms for
generating the pairing. Since the electron-phonon cou-

pling mechanism tends to be limited to the conventional
spin-singlet s-wave pairing [157], altermagnets can be
particularly relevant for research of the unconventional
superconductivity, including both the spin-singlet and
spin-triplet anisotropic types of Cooper pairing.
Finally, we foresee intriguing new physics at altermagnet/superconductor interfaces in areas including Andreev
reflection [158] or Majorana fermion quasiparticles [159].
On one hand, the behavior of alternagnets at these interfaces can be reminiscent of conventional antiferromagnets when dominated by the spin-symmetry protected
nodal lines or surface. On the other hand, interface orientations exposing the strong altermagnetic spin splitting
can generate a phenomenology similar to the ferromagnet/superconductor interfaces. As in the case of bulk
crystals, the research of interface effects can exploit the
predicted broad range of altermagnetic material types.

V.

CONCLUSION

In this Perspective we have drawn a picture of a third
basic magnetic phase that emerges on the fundamental
level of non-relativistic uncorrelated band-theory of nonfrustrated collinear magnets. The altermagnetic phase
can be uniquely defined in both crystal-structure real
space and electronic-structure momentum space, systematically classified and described by symmetry-group theory, and is predicted to be abundant among diverse
material types. Most importantly, the notion and the
significance of a distinct phase becomes apparent from
the unique ways in which altermagnetism can contribute
to the development of fundamental physical concepts,
and to the research in modern condensed-matter physics
fields. Given the still relatively early stage of our understanding of altermagnetism, and the limited space, our
choice of the discussion topics in this Perspective should
be regarded as broadly illustrative and provisional. We
can anticipate that in the near future, altermagnetism
will have impact in other fields including magnetic topological matter, magnonics, valleytronics, or axion electrodynamics. Fig. 13 summarizes the emerging research
landscape of altermagnetism.

Acknowledgement

We acknowledge fruitful interactions with Igor Mazin.
This work was supported by Ministry of Education of
the Czech Republic Grants LNSM-LNSpin, LM2018140,
Czech Science Foundation Grant No. 19-28375X, EU
FET Open RIA Grant No. 766566, SPIN+X (DFG
SFB TRR 173) and Elasto-Q-Mat (DFG SFB TRR 288).
We acknowledge the computing time granted on the supercomputer Mogon at Johannes Gutenberg University
Mainz (hpc.uni-mainz.de).

21

Magnonics

Spintronics

Magnetic topological matter

Axion electrodynamics

Energy (t)

Kramers theorem
Ultra-fast optics

-2

S'

S

Γ

Neuromorphics

Altermagnets

Berry phases

Fermi liquid instabilities

High-Tc superconductivity

Thermoelectrics

Electron quasiparticles
Valleytronics

Field-eﬀect electronics
Multiferroics

FIG. 13. Summary of the emerging research landscape of altermagnetism.

[1] L. Néel, Science 174, 985 (1971).
[2] L. Šmejkal, A. H. MacDonald, J. Sinova, S. Nakatsuji,
and T. Jungwirth, Nature Reviews Materials , published
on (2022), arXiv:2107.03321.
[3] L. Šmejkal, R. González-Hernández, T. Jungwirth,
and J. Sinova, Science Advances 6, eaaz8809 (2020),
arXiv:1901.00445.
[4] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Nature Communications 10, 4305
(2019), arXiv:1902.02506.
[5] Z. Feng, X. Zhou, L. Šmejkal, L. Wu, Z. Zhu, H. Guo,
R. González-Hernández, X. Wang, H. Yan, P. Qin,
X. Zhang, H. Wu, H. Chen, C. Jiang, M. Coey,
J. Sinova, T. Jungwirth, and Z. Liu, , (2020),
arXiv:2002.08712.
[6] H. Reichlova, R. Lopes Seeger, R. González-Hernández,
I. Kounta, R. Schlitz, D. Kriegner, P. Ritzinger,
M. Lammel, M. Leiviskä, V. Petřiček, P. Doležal,

E. Schmoranzerova, A. Bad, A. Thomas, V. Baltz,
L. Michez, J. Sinova, S. T. B Goennenwein, T. Jungwirth, and L. Smejkal, Macroscopic time reversal symmetry breaking arising from antiferromagnetic Zeeman
effect, Tech. Rep. (2020) arXiv:2012.15651v1.
[7] I. I. Mazin, K. Koepernik, M. D. Johannes, R. GonzálezHernández, and L. Šmejkal, PNAS 118, e2108924118
(2021), arXiv:2105.06356.
[8] R. González-Hernández, L. Šmejkal, K. Výborný, Y. Yahagi, J. Sinova, T. Jungwirth, and J. Železný, Physical
Review Letters 126, 127701 (2021), arXiv:2002.07073.
[9] M. Naka, Y. Motome, and H. Seo, Physical Review B
103, 125114 (2021), arXiv:2011.12459.
[10] A. Bose, N. J. Schreiber, R. Jain, D.-f. Shao, H. P. Nair,
J. Sun, X. S. Zhang, D. A. Muller, E. Y. Tsymbal, D. G.
Schlom, and D. C. Ralph, (2021), arXiv:2108.09150.
[11] H. Bai, L. Han, X. Feng, Y. Zhou, Q. Wang, W. Zhu,
X. Chen, F. Pan, X. Fan, and C. Song, (2021),

22
arXiv:2109.05933.
[12] S. Karube, T. Tanaka, D. Sugawara, N. Kadoguchi,
M. Kohda, and J. Nitta, (2021), arXiv:2111.07487.
[13] L. Šmejkal, A. B. Hellenes, R. González-Hernández,
J. Sinova, and T. Jungwirth, Physical Review X 12,
011028 (2022), arXiv:2103.12664.
[14] D.-F. Shao, S.-H. Zhang, M. Li, C.-B. Eom, and E. Y.
Tsymbal, Nature Communications 12, 7061 (2021),
arXiv:2103.09219.
[15] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia, and
J. Liu, Nature Communications 12, 2846 (2021).
[16] L. Šmejkal, J. Sinova, and T. Jungwirth, , (2021),
arXiv:2105.05820.
[17] Y. Noda, K. Ohno, and S. Nakamura, Physical Chemistry Chemical Physics 18, 13294 (2016).
[18] K.-H. Ahn, A. Hariki, K.-W. Lee, and J. Kuneš, Physical Review B 99, 184432 (2019).
[19] S. Hayami, Y. Yanagi, and H. Kusunose, Journal of the
Physical Society of Japan 88, 123702 (2019).
[20] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, Physical Review B 102, 014422 (2020).
[21] S. Hayami, Y. Yanagi, and H. Kusunose, Physical Review B 102, 144441 (2020).
[22] L.-D. Yuan, Z. Wang, J.-W. Luo, and A. Zunger, Physical Review Materials 5, 014409 (2021).
[23] S. A. Egorov and R. A. Evarestov, The Journal of Physical Chemistry Letters 12, 2363 (2021).
[24] P. Liu, J. Li, J. Han, X. Wan, and Q. Liu, (2021),
arXiv:2103.15723.
[25] J. Yang, Z.-X. Liu,
and C. Fang,
(2021),
arXiv:2105.12738.
[26] W. F. Brinkman and R. J. Elliott, Proceedings of the
Royal Society A: Mathematical, Physical and Engineering Sciences 294, 343 (1966).
[27] D. Litvin and W. Opechowski, Physica 76, 538 (1974).
[28] D. B. Litvin, Acta Crystallographica Section A 33, 279
(1977).
[29] F. D. M. Haldane, Reviews of Modern Physics 89,
040502 (2017).
[30] J. G. Bednorz and K. A. Müller, Angewandte Chemie
International Edition in English 27, 735 (1988).
[31] H. L. Stormer, Reviews of Modern Physics 71, 875
(1999).
[32] N. Nagaosa, J. Sinova, S. Onoda, A. H. MacDonald,
and N. P. Ong, Reviews of Modern Physics 82, 1539
(2010), arXiv:0904.4154.
[33] J. Sinova, S. O. Valenzuela, J. Wunderlich, C. H. Back,
and T. Jungwirth, Reviews of Modern Physics 87, 1213
(2015), arXiv:1411.3249.
[34] T. Jungwirth, X. Marti, P. Wadley, and J. Wunderlich, Nature Nanotechnology 11, 231 (2016),
arXiv:1606.04284.
[35] A. Manchon, J. Železný, I. M. Miron, T. Jungwirth,
J. Sinova, A. Thiaville, K. Garello, and P. Gambardella, Reviews of Modern Physics 91, 035004 (2019),
arXiv:1801.09636.
[36] M. Franz and L. Molenkamp, eds., Contemporary Concepts of Condensed Matter Science, vol. 6 - Topological
Insulators (Elsevier, 2013).
[37] Y. Tokura, K. Yasuda, and A. Tsukazaki, Nature Reviews Physics 1, 126 (2019).
[38] S. Nakatsuji and R. Arita, Annual Review of Condensed Matter Physics 13 (2022), 10.1146/annurevconmatphys-031620-103859.

[39] K. Samanta, M. Ležaić, M. Merte, F. Freimuth,
S. Blügel, and Y. Mokrousov, Journal of Applied
Physics 127, 213904 (2020).
[40] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Physical Review B 102, 075112
(2020).
[41] M. Naka, Y. Motome,
and H. Seo, Perovskite
as a spin current generator , Tech. Rep. (2020)
arXiv:2011.12459v1.
[42] S. López-Moreno, A. H. Romero, J. Mejı́a-López,
A. Muñoz, and I. V. Roshchin, Physical Review B 85,
134110 (2012).
[43] S. López-Moreno, A. H. Romero, J. Mejı́a-López, and
A. Muñoz, Physical Chemistry Chemical Physics 18,
33250 (2016).
[44] L. Néel, Reviews of Modern Physics 25, 58 (1953).
[45] N. Kurti, Selected Works of Louis Neel, 1st ed. (CRC
Press, 1988).
[46] T. Berlijn, P. C. Snijders, O. Delaire, H. D. Zhou, T. A.
Maier, H. B. Cao, S. X. Chi, M. Matsuda, Y. Wang,
M. R. Koehler, P. R. Kent, and H. H. Weitering, Physical Review Letters 118, 2 (2017), arXiv:1612.09589.
[47] Z. H. Zhu, J. Strempfer, R. R. Rao, C. A. Occhialini,
J. Pelliciari, Y. Choi, T. Kawaguchi, H. You, J. F.
Mitchell, Y. Shao-Horn, and R. Comin, Physical Review Letters 122, 017202 (2019), arXiv:1806.02036.
[48] S. W. Lovesey, D. D. Khalyavin, and G. van der Laan,
(2021), arXiv:2108.01972.
[49] C. A. Occhialini, V. Bisogni, H. You, A. Barbour, I. Jarrige, J. F. Mitchell, R. Comin, and J. Pelliciari, Physical
Review Research 3, 033214 (2021), arXiv:2108.06256.
[50] K. Ishizaka, M. S. Bahramy, H. Murakawa, M. Sakano,
T. Shimojima, T. Sonobe, K. Koizumi, S. Shin,
H. Miyahara, A. Kimura, K. Miyamoto, T. Okuda,
H. Namatame, M. Taniguchi, R. Arita, N. Nagaosa,
K. Kobayashi, Y. Murakami, R. Kumai, Y. Kaneko,
Y. Onose, and Y. Tokura, Nature Materials 10, 521
(2011).
[51] L. Landau and E. Lifshitz, Electrodynamics of Continuous Media, vol. 8 of Course of Theoretical Physics, 2nd
ed. (Pergamon Press, Oxford, 1965).
[52] N. V. Shubnikov and A. V. Belov, Colored Symmetry.
(Macmillan Publishers, New York, 1964).
[53] B. A. Tavger and V. M. Zaitsev, Soviet Physics JETP
3, 430 (1956).
[54] C. J. Bradley and A. P. Cracknell, The Mathematical
Theory of Symmetry in Solids (Oxford Univeristy Press,
1972).
[55] D. B. Litvin, Magnetic Group Tables (International
Union of Crystallography, Chester, England, 2013).
[56] S. V. Gallego, J. Manuel Perez-Mato, L. Elcoro, E. S.
Tasci, R. M. Hanson, K. Momma, M. I. Aroyo, and
G. Madariaga, J. Appl. Cryst 49, 1750 (2016).
[57] L. Šmejkal, Y. Mokrousov, B. Yan, and A. H. MacDonald, Nature Physics 14, 242 (2018), arXiv:1706.00670.
[58] H. Watanabe, H. C. Po, and A. Vishwanath, Science
Advances 4, eaat8685 (2018), arXiv:1707.01903.
[59] Y. Xu, L. Elcoro, Z. D. Song, B. J. Wieder, M. G.
Vergniory, N. Regnault, Y. Chen, C. Felser, and B. A.
Bernevig, Nature 586, 702 (2020).
[60] L. Elcoro, B. J. Wieder, Z. Song, Y. Xu, B. Bradlyn,
and B. A. Bernevig, Nature Communications 12, 5965
(2021), arXiv:2010.00598.

23
[61] J. Cano, B. Bradlyn, and M. G. Vergniory, APL Materials 7, 101125 (2019).
[62] P. M. Lenggenhager, X. Liu, T. Neupert,
and
T. Bzdušek, (2022), arXiv:2201.08404.
[63] A. F. Andreev and V. Marchenko, Uspekhi Fizicheskih
Nauk 130, 39 (1980).
[64] A. Corticelli, R. Moessner, and P. A. McClarty, Physical Review B 105, 064430 (2022), arXiv:2103.05656.
[65] I. Turek, (2022), arXiv:2201.11452.
[66] M.-T. Suzuki, T. Koretsune, M. Ochi, and R. Arita,
Physical Review B 95, 094406 (2017), arXiv:1611.06042.
[67] X. Chen, D. Wang, L. Li, and B. Sanyal, (2021),
arXiv:2104.07390.
[68] T. Okugawa, K. Ohno, Y. Noda, and S. Nakamura,
Journal of Physics: Condensed Matter 30, 075502
(2018).
[69] H. Seo and M. Naka, Journal of the Physical Society of
Japan 90, 064713 (2021), arXiv:2101.09883.
[70] H. A. Kramers, Proc. Amsterdam Acad. 33 (1930).
[71] E. Wigner, Nachrichten von der Gesellschaft der Wissenschaften zu Göttingen, Mathematisch-Physikalische
Klasse 1932, 546 (1932).
[72] B. Bradlyn, L. Elcoro, J. Cano, M. G. Vergniory,
Z. Wang, C. Felser, M. I. Aroyo, and B. A. Bernevig,
Nature 547, 298 (2017), arXiv:1703.02050.
[73] J. Zang, V. Cros, and A. Hoffmann, eds., Topology in
Magnetism, Springer Series in Solid-State Sciences, Vol.
192 (Springer International Publishing, Cham, 2018).
[74] M. G. Vergniory, L. Elcoro, C. Felser, N. Regnault, B. A.
Bernevig, and Z. Wang, Nature 566, 480 (2019).
[75] C. Chappert, A. Fert, and F. N. Van Dau, Nature Materials 6, 813 (2007), arXiv:1003.4058.
[76] D. C. Ralph and M. D. Stiles, Journal of Magnetism and
Magnetic Materials 320, 1190 (2008), arXiv:0711.4608.
[77] S. Bhatti, R. Sbiaa, A. Hirohata, H. Ohno, S. Fukami,
and S. Piramanayagam, Materials Today 20, 530
(2017).
[78] R. Winkler, Spin–Orbit Coupling Effects in TwoDimensional Electron and Hole Systems, Springer
Tracts in Modern Physics, Vol. 191 (Springer Berlin Heidelberg, Berlin, Heidelberg, 2003).
[79] N. P. Armitage, E. J. Mele, and A. Vishwanath,
Reviews of Modern Physics 90, 015001 (2018),
arXiv:1705.01111.
[80] E. Turov, Physical properties of magnetically ordered
crystals (Academic Press, New York, 1965).
[81] A. S. Núñez, R. A. Duine, P. Haney, and A. H. MacDonald, Physical Review B 73, 214426 (2006).
[82] C. Sürgers, G. Fischer, P. Winkel, and H. V. Löhneysen,
Nature Communications 5, 3400 (2014).
[83] C. Sürgers, W. Kittler, T. Wolf, and H. V. Löhneysen,
AIP Advances 6, 055604 (2016), arXiv:1601.01840.
[84] N. J. Ghimire, A. S. Botana, J. S. Jiang, J. Zhang, Y.-S.
Chen, and J. F. Mitchell, Nature Communications 9,
3280 (2018).
[85] X. Marti, I. Fina, C. Frontera, J. Liu, P. Wadley,
Q. He, R. J. Paull, J. D. Clarkson, J. Kudrnovský,
I. Turek, J. Kuneš, D. Yi, J.-H. Chu, C. T. Nelson,
L. You, E. Arenholz, S. Salahuddin, J. Fontcuberta,
T. Jungwirth, and R. Ramesh, Nature Materials 13,
367 (2014), arXiv:0402594 [cond-mat].
[86] M. M. Otrokov, I. I. Klimovskikh, H. Bentmann, D. Estyunin, A. Zeugner, Z. S. Aliev, S. Gaß, A. U. B. Wolter,
A. V. Koroleva, A. M. Shikin, M. Blanco-Rey, M. Hoff-

mann, I. P. Rusinov, A. Y. Vyazovskaya, S. V. Eremeev, Y. M. Koroteev, V. M. Kuznetsov, F. Freyse,
J. Sánchez-Barriga, I. R. Amiraslanov, M. B. Babanly,
N. T. Mamedov, N. A. Abdullayev, V. N. Zverev, A. Alfonsov, V. Kataev, B. Büchner, E. F. Schwier, S. Kumar, A. Kimura, L. Petaccia, G. Di Santo, R. C. Vidal, S. Schatz, K. Kißner, M. Ünzelmann, C. H. Min,
S. Moser, T. R. F. Peixoto, F. Reinert, A. Ernst, P. M.
Echenique, A. Isaeva, and E. V. Chulkov, Nature 576,
416 (2019), arXiv:1809.07389.
[87] J. Železný, H. Gao, K. Výborný, J. Zemen, J. Mašek,
A. Manchon, J. Wunderlich, J. Sinova, and T. Jungwirth, Physical Review Letters 113, 157201 (2014),
arXiv:1410.8296.
[88] P. Wadley, B. Howells, J. Železný, C. Andrews, V. Hills,
R. P. Campion, V. Novák, K. Olejnı́k, F. Maccherozzi,
S. S. Dhesi, S. Y. Martin, T. Wagner, J. Wunderlich,
F. Freimuth, Y. Mokrousov, J. Kuneš, J. S. Chauhan,
M. J. Grzybowski, A. W. Rushforth, K. Edmond, B. L.
Gallagher, and T. Jungwirth, Science 351, 587 (2016),
arXiv:1503.03765.
[89] L. Šmejkal, J. Železný, J. Sinova, and T. Jungwirth, Physical Review Letters 118, 106402 (2017),
arXiv:1610.08107.
[90] H. J. Elmers, S. V. Chernov, S. W. D’Souza,
S. P. Bommanaboyena, S. Y. Bodnar, K. Medjanik,
S. Babenkov, O. Fedchenko, D. Vasilyev, S. Y. Agustsson, C. Schlueter, A. Gloskovskii, Y. Matveyev, V. N.
Strocov, Y. Skourski, L. Šmejkal, J. Sinova, J. Minár,
M. Kläui, G. Schönhense, and M. Jourdan, ACS Nano
14, 17554 (2020).
[91] O. Fedchenko, L. Smejkal, M. Kallmayer, Y. Lytvynenko, K. Medjanik, S. Babenkov, D. Vasilyev,
M. Klaeui, J. Demsar, G. Schoenhense, M. Jourdan,
J. Sinova, and H.-J. Elmers, (2021), arXiv:2110.12186.
[92] K. Yamauchi, P. Barone, and S. Picozzi, Physical Review B 100, 245115 (2019).
[93] T. Suzuki, R. Chisnell, A. Devarakonda, Y. T. Liu,
W. Feng, D. Xiao, J. W. Lynn, and J. G. Checkelsky,
Nature Physics 12, 1119 (2016).
[94] R. Ramazashvili, Physical Review Letters 101, 137202
(2008).
[95] R. Ramazashvili, Physical Review B 79, 184432 (2009).
[96] E. J. Rozbicki, J. F. Annett, J.-R. Souquet, and A. P.
Mackenzie, Journal of Physics: Condensed Matter 23,
094201 (2011).
[97] B. Schrunk, Y. Kushnirenko, B. Kuthanazhi, J. Ahn,
L.-L. Wang, E. O’Leary, K. Lee, A. Eaton, A. Fedorov, R. Lou, V. Voroshnin, O. J. Clark, J. SánchezBarriga, S. L. Bud’ko, R.-J. Slager, P. C. Canfield, and A. Kaminski, Nature 603, 610 (2022),
arXiv:2203.12511.
[98] I. Pomeranchuk, Phys. JETP 8, 361 (1959).
[99] C. Wu, K. Sun, E. Fradkin, and S.-C. Zhang, Physical
Review B 75, 115103 (2007).
[100] S. A. Egorov, D. B. Litvin, and R. A. Evarestov,
The Journal of Physical Chemistry C , acs.jpcc.1c02653
(2021).
[101] J. R. Schaibley, H. Yu, G. Clark, P. Rivera, J. S. Ross,
K. L. Seyler, W. Yao, and X. Xu, Nature Reviews Materials 1, 16055 (2016).
[102] A. Marmodoro, L. Šmejkal, J. Sinova and T. Jungwirth,
to be submitted (2022).

24
[103] S. V. Halilov, H. Eschrig, A. Y. Perlov, and P. M.
Oppeneer, Physical Review B 58, 293 (1998).
[104] A. Marmodoro, S. Mankovsky, H. Ebert, J. Minár, and
O. O. Ondřejšipr, (2022), arXiv:2202.04525v1.
[105] S. M. Rezende, A. Azevedo, and R. L. Rodrı́guezSuárez, Journal of Applied Physics 126, 151101 (2019).
[106] M. V. Berry, Proceedings of the Royal Society of London. A. Mathematical and Physical Sciences 392, 45
(1984), arXiv:1108.0910.
[107] D. Culcer, A. MacDonald, and Q. Niu, Physical Review B - Condensed Matter and Materials Physics 68,
1 (2003), arXiv:0311147 [cond-mat].
[108] T. S. Nunner, N. A. Sinitsyn, M. F. Borunda, V. K.
Dugaev, A. A. Kovalev, A. Abanov, C. Timm, T. Jungwirth, J.-i. Inoue, A. H. MacDonald, and J. Sinova,
Physical Review B 76, 235312 (2007), arXiv:0706.0056.
[109] V. K. Dugaev, J. Barnaś, M. Taillefumier, B. Canals,
C. Lacroix,
and P. Bruno, Journal of Physics:
Conference
Series
104
(2008),
10.1088/17426596/104/1/012018.
[110] D. Xiao, M. C. Chang, and Q. Niu, Reviews of Modern
Physics 82, 1959 (2010), arXiv:0907.2021.
[111] D. F. Shao, J. Ding, G. Gurung, S. H. Zhang, and
E. Y. Tsymbal, Physical Review Applied 15, 1 (2021),
arXiv:2006.09624.
[112] M. Z. Hasan and C. L. Kane, Reviews of Modern Physics
82, 3045 (2010), arXiv:1002.3895.
[113] K. V. Klitzing, G. Dorda, and M. Pepper, Physical Review Letters 45, 494 (1980), arXiv:arXiv:1011.1669v3.
[114] K. S. Novoselov, Z. Jiang, Y. Zhang, S. V. Morozov,
H. L. Stormer, U. Zeitler, J. C. Maan, G. S. Boebinger,
P. Kim, and A. K. Geim, Science 315, 1379 (2007),
arXiv:0702408 [cond-mat].
[115] C.-Z. Chang, J. Zhang, X. Feng, J. Shen, Z. Zhang,
M. Guo, K. Li, Y. Ou, P. Wei, L.-L. Wang, Z.-Q. Ji,
Y. Feng, S. Ji, X. Chen, J. Jia, X. Dai, Z. Fang, S.-C.
Zhang, K. He, Y. Wang, L. Lu, X.-C. Ma, and Q.-K.
Xue, Science 340, 167 (2013), arXiv:arXiv:1212.4783.
[116] Y. Deng, Y. Yu, M. Z. Shi, Z. Guo, Z. Xu, J. Wang,
X. H. Chen, and Y. Zhang, Science 367, 895 (2020).
[117] A. H. MacDonald and M. Tsoi, Philosophical Transactions of the Royal Society A: Mathematical, Physical and Engineering Sciences 369, 3098 (2011),
arXiv:0510797 [cond-mat].
[118] H. B. M. Saidaoui, A. Manchon, and X. Waintal, Physical Review B 89, 174430 (2014),
arXiv:arXiv:1403.6383v1.
[119] M. Stamenova, R. Mohebbi, J. Seyed-Yazdi, I. Rungger,
and S. Sanvito, Physical Review B 95, 060403 (2017).
[120] A. B. Shick, S. Khmelevskyi, O. N. Mryasov, J. Wunderlich, and T. Jungwirth, Physical Review B 81, 212409
(2010), arXiv:1002.2151.
[121] J. Godinho, H. Reichlova, D. Kriegner, V. Novak,
K. Olejnik, Z. Kaspar, Z. Soban, P. Wadley, R. P. Campion, R. M. Otxoa, P. E. Roy, J. Zelezny, T. Jungwirth, and J. Wunderlich, Nature Communications 9,
4686 (2018), arXiv:1806.02795.
[122] Y. Zhang, Q. Xu, K. Koepernik, R. Rezaev, O. Janson,
J. Železný, T. Jungwirth, C. Felser, J. van den Brink,
and Y. Sun, npj Computational Materials 7, 167 (2021).
[123] A. Brataas, A. D. Kent, and H. Ohno, Nature Materials
11, 372 (2012).
[124] M. Baumgartner, K. Garello, J. Mendil, C. O.
Avci, E. Grimaldi, C. Murer, J. Feng, M. Gabureac,

C. Stamm, Y. Acremann, S. Finizio, S. Wintz, J. Raabe,
and P. Gambardella, Nature Nanotechnology 12, 980
(2017), arXiv:arXiv:1704.06402v1.
[125] A. V. Kimel and M. Li, Nature Reviews Materials 4,
189 (2019).
[126] D. Bedau, H. Liu, J. Z. Sun, J. A. Katine, E. E. Fullerton, S. Mangin, and A. D. Kent, Applied Physics Letters 97, 262502 (2010), arXiv:1009.5240.
[127] K. Garello, C. O. Avci, I. M. Miron, M. Baumgartner, A. Ghosh, S. Auffret, O. Boulle, G. Gaudin, and
P. Gambardella, Applied Physics Letters 105, 212402
(2014), arXiv:1310.5586.
[128] G. Prenat, K. Jabeur, P. Vanhauwaert, G. D. Pendina, F. Oboril, R. Bishnoi, M. Ebrahimi, N. Lamard,
O. Boulle, K. Garello, J. Langer, B. Ocker, M. C.
Cyrille, P. Gambardella, M. Tahoori, and G. Gaudin,
IEEE Transactions on Multi-Scale Computing Systems
2, 49 (2016).
[129] K. Olejnı́k, T. Seifert, Z. Kašpar, V. Novák, P. Wadley,
R. P. Campion, M. Baumgartner, P. Gambardella,
P. Němec, J. Wunderlich, J. Sinova, P. Kužel, M. Müller,
T. Kampfrath, and T. Jungwirth, Science Advances 4,
eaar3566 (2018), arXiv:1711.08444.
[130] C. Kittel, Phys. Rev. 82, 565 (1951).
[131] E. Beaurepaire, J. C. Merle, A. Daunois,
and
J. Y. Bigot, Physical Review Letters 76, 4250 (1996),
arXiv:9709264 [cond-mat].
[132] I. Radu, K. Vahaplar, C. Stamm, T. Kachel, N. Pontius, H. A. Dürr, T. A. Ostler, J. Barker, R. F. Evans,
R. W. Chantrell, A. Tsukamoto, A. Itoh, A. Kirilyuk,
T. Rasing, and A. V. Kimel, Nature 472, 205 (2011).
[133] Z. Kašpar, M. Surýnek, J. Zubáč, F. Krizek, V. Novák,
R. P. Campion, M. S. Wörnle, P. Gambardella,
X. Marti, P. Němec, K. W. Edmonds, S. Reimers, O. J.
Amin, F. Maccherozzi, S. S. Dhesi, P. Wadley, J. Wunderlich, K. Olejnı́k, and T. Jungwirth, Nature Electronics 4, 30 (2021).
[134] J. Zubáč, Z. Kašpar, F. Krizek, T. Förster, R. P. Campion, V. Novák, T. Jungwirth, and K. Olejnı́k, Physical
Review B 104, 184424 (2021), arXiv:2107.05724.
[135] F. Krizek, S. Reimers, Z. Kašpar, A. Marmodoro,
J. Michalička, O. Man, A. Edstrom, O. J. Amin, K. W.
Edmonds, R. P. Campion, F. Maccherozzi, S. S. Dnes,
J. Zubáč, J. Železný, K. Výborný, K. Olejnı́k, V. Novák,
J. Rusz, J. C. Idrobo, P. Wadley, and T. Jungwirth, Science Advances 8, eabn3535 (2022), arXiv:2012.00894.
[136] Y. Kohno, T. Seki, S. D. Findlay, Y. Ikuhara, and
N. Shibata, Nature 602, 234 (2022).
[137] B. Mallada, A. Gallardo, M. Lamanec, B. de la Torre,
V. Špirko, P. Hobza, and P. Jelinek, Science 374, 863
(2021).
[138] W. A. Borders, H. Akima, S. Fukami, S. Moriya,
S. Kurihara, Y. Horio, S. Sato, and H. Ohno, Applied
Physics Express 10, 013007 (2017).
[139] K. Olejnı́k, V. Schuler, X. Marti, V. Novák, Z. Kašpar,
P. Wadley, R. P. Campion, K. W. Edmonds, B. L. Gallagher, J. Garces, M. Baumgartner, P. Gambardella,
and T. Jungwirth, Nature Communications 8, 15434
(2017).
[140] A. Kurenkov, S. DuttaGupta, C. Zhang, S. Fukami,
Y. Horio, and H. Ohno, Advanced Materials 31,
1900636 (2019).
[141] A. Kurenkov, S. Fukami, and H. Ohno, Journal of Applied Physics 128, 010902 (2020).

25
[142] J. C. Phillips, Journal of Non-Crystalline Solids 352,
4490 (2006).
[143] Wulfram Gerstner and Werner M. Kistler, Spiking Neuron Models (Cambridge University Press, 2002).
[144] J. Grollier, D. Querlioz, and M. D. Stiles, Proceedings
of the IEEE 104, 2024 (2016).
[145] J. Kaiser, W. A. Borders, K. Y. Camsari, S. Fukami,
H. Ohno, and S. Datta, Physical Review Applied 17,
014016 (2022).
[146] C. Li, M. Hu, Y. Li, H. Jiang, N. Ge, E. Montgomery,
J. Zhang, W. Song, N. Dávila, C. E. Graves, Z. Li, J. P.
Strachan, P. Lin, Z. Wang, M. Barnell, Q. Wu, R. S.
Williams, J. J. Yang, and Q. Xia, Nature Electronics
1, 52 (2018).
[147] J. J. Yang, D. B. Strukov, and D. R. Stewart, Nature
Nanotechnology 8, 13 (2013), arXiv:1011.1669v3.
[148] G. E. Bauer, E. Saitoh, and B. J. Van Wees, Nature
Materials 11, 391 (2012), arXiv:1107.4395.
[149] M. Mizuguchi and S. Nakatsuji, Science and Technology
of Advanced Materials 20, 262 (2019).

[150] Q. Jie, R. Hu, E. Bozin, A. Llobet, I. Zaliznyak,
C. Petrovic, and Q. Li, Physical Review B 86, 115121
(2012), arXiv:1210.3355.
[151] H. Ohno, Science 281, 951 (1998).
[152] T. Dietl and H. Ohno, Reviews of Modern Physics 86,
187 (2014), arXiv:1307.3429.
[153] R. Ramesh and N. A. Spaldin, Nature Materials 6, 21
(2007).
[154] S. Bhattacharjee, E. Bousquet, and P. Ghosez, Physical
Review Letters 102, 117602 (2009), arXiv:0811.2344.
[155] Q. Si, R. Yu, and E. Abrahams, Nature Reviews Materials 1, 1 (2016), arXiv:1604.03566.
[156] I. I. Mazin, (2022), arXiv:2203.05000.
[157] M. Sigrist and K. Ueda, Reviews of Modern Physics 63,
239 (1991).
[158] I. I. Mazin, A. A. Golubov, and B. Nadgorny, Journal
of Applied Physics 89, 7576 (2001).
[159] K. Flensberg, F. von Oppen, and A. Stern, Nature
Reviews Materials 6, 944 (2021), arXiv:2103.05548.


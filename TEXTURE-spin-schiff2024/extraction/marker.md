Collinear Altermagnets and their Landau Theories
Hana Schiff,1, ∗ Paul McClarty,2, † Jeffrey G. Rau,3, ‡ and Judit Romhányi1, §

arXiv:2412.18025v3 [cond-mat.str-el] 18 Jul 2025

2

1
Department of Physics and Astronomy, University of California, Irvine, California 92697, USA
Laboratoire Léon Brillouin, CEA, CNRS, Université Paris-Saclay, CEA Saclay, 91191 Gif-sur-Yvette, France.
3
Department of Physics, University of Windsor, 401 Sunset Avenue, Windsor, Ontario, N9B 3P4, Canada
(Dated: August 21, 2025)

Altermagnets exhibit spontaneously spin-split electronic bands in the zero spin-orbit coupling
(SOC) limit arising from the presence of collinear compensated magnetic order. The distinctive
magneto-crystalline symmetries of altermagnets ensure that these spin splittings have a characteristic anisotropy in crystal momentum space. These systems have attracted a great deal of interest
due to their potential for applications in spintronics. In this paper, we provide a general Landau
theory that encompasses all three-dimensional altermagnets where the magnetic order does not enlarge the unit cell. We identify all crystal structures that admit altermagnetism and then reduce
these to a relatively small set of distinct possible Landau theories governing such systems. In the
zero SOC limit, we determine the possible local multipolar orders that are tied to the spin splitting
of the band structure. We make precise the connection between altermagnetism as defined at zero
SOC (“ideal” altermagnets) and the effects of weak SOC. In particular, we examine which response
functions allowed by symmetry when SOC is present are guaranteed by the spin-orbit free theory,
and spell out the distinctive properties of altermagnets in comparison with conventional collinear
antiferromagnets. Finally, we show how these ideas can be applied by considering a number of
altermagnetic candidate materials.

CONTENTS

A. Circumventing Spin Groups

17

B. Direct product representations of the SOC-free
paramagnetic group

19

C. Altermagnetic Structures Algorithm: Technical
Details

20
21

I. Introduction

2

II. Altermagnets from their symmetries

3

III. Altermagnetic Landau Theory at Zero SOC
A. Spin groups to point groups
B. Secondary Multipolar Order Parameters for
zero SOC

5
5
5

D. Consistency of SOC Landau Theory with
Magnetic Symmetry Analysis

IV. Altermagnetic Landau Theory at Finite SOC
A. Altermagnetic Landau Theories at Finite
SOC: General Remarks
B. Coupling to the Néel Vector at Finite SOC
C. Distinguishing between Néel AFMs and
Altermagnets
D. Multipolar Order in Altermagnets at Finite
SOC
E. Experimental Signatures of Altermagnetism

7

E. Symmetrization of tensor powers

22

F. Tensor & multipole components coupling to N

23

G. “Repackaging” Tensor Components

23

9
10

H. Table of space groups and Wyckoff positions
supporting altermagnetic order

25

V. Examples of Materials
A. Point group 2/m
B. Point group mmm
C. Point group 4/mmm
D. Point group 3m

12
12
13
14
15

I. Table of multipoles coupling to ΓN in the
SOC-free limit

30

J. Table of symmetry-allowed couplings with and
without SOC

31

VI. Discussion

16

Acknowledgments

∗ hschiff@uci.edu
† paul.mcclarty@cea.fr
‡ jrau@uwindsor.ca
§ jromhany@uci.edu

8
8
9

17

References

34

2
I.

INTRODUCTION

Understanding the interplay of heat, charge, and spin
transport in magnetic materials has proven to be an
important theme in modern condensed matter physics.
Falling broadly under the umbrella of spintronics research, a plethora of phenomena have been uncovered
that have motivated and guided the development of new
devices to manipulate these currents. Early work focused
on uncompensated magnetic metals that have a net magnetic moment, as these offer a straightforward means to
induce spin-polarized currents [1, 2]. For such currents to
be robust, as is necessary for devices to be useful, materials with weak spin-orbit coupling are preferable. As an
alternative, more recent research has explored compensated magnets, where the net moment is zero. These systems offer the potential to achieve THz switching speeds
due to the larger underlying exchange scale [3, 4]. However, generating spin currents is a challenge due to the
compensated order.
Recently, it has been recognized that intrinsic spinsplitting – characteristic of uncompensated magnets – is
possible even in compensated collinear antiferromagnets
at zero spin-orbit coupling. In many cases, this allows for
straightforward spin current generation [4–9]. This class
of magnets has sublattices with magnetic moments pointing in opposite directions, that are related not by translation or inversion, but instead by a spatial symmetry
involving a rotation or reflection. From a fundamental
point of view, these insights amount to the appearance
of new physics − often called altermagnetism − in the
remarkably simple setting of two sublattice collinear antiferromagnetism with spin isotropy in the interactions,
a context traditionally associated with spin degenerate
bands.
These altermagnets are sharply distinguished from
conventional ferromagnets or antiferromagnets in the idealized limit of zero spin-orbit coupling. In this limit
(“ideal altermagnetism”), the characteristic pattern of
spin splitting is symmetry enforced by the additional
spin rotation symmetries that appear in the absence of
spin-orbit coupling. While the weak spin-orbit coupling
present in real materials breaks these symmetries, the
dominant magnetic energy scale, derived from the idealized limit, controls many of the properties of real altermagnets and is crucial for understanding their behavior.
In ideal altermagnets, these spin symmetries impose
a compensated collinear antiferromagnetic order (magnetization M = 0) and preserve spin as a good quantum
number while lifting the spin-degeneracy often associated
with Néel antiferromagnets [4, 10, 11]. Overall compensation is preserved through the symmetry-imposed constraint that constant energy surfaces in momentum space
(and thus occupied electronic bands) display alternating
spin patterns [4, 5, 7, 9, 10, 12–16]. These spin splittings are even under inversion regardless of whether the
crystal is centrosymmetric [4, 7, 13–16] and can follow
d-wave, g-wave or i-wave form factors. These anisotropic

spin-splitting patterns are directly tied to their ability to
produce spin currents [17, 18] and are related to underlying secondary multipolar order parameters [19].
In the presence of weak SOC, some altermagnets produce a large anomalous Hall response that does not arise
from canting of their magnetic moments (i.e. weak ferromagnetism) [8, 20–23]. Other altermagnets exhibit a
wide range of novel responses brought to light in Refs. [7,
8, 24] including the thermal Hall effect [25], piezomagnetism [26], and anisotropic magnetoresistance [27, 28],
and topological transitions [29] among others, leading to
a great deal of interest in the unconventional transport
properties arising from altermagnetism. A crucial recent
development has been direct experimental imaging of the
altermagnetic spin splitting in candidate altermagnets
MnTe and CrSb using photoemission spectroscopy both
with and without spin polarization [30, 31]. As the definition of altermagnetism is grounded in symmetry, it has
implications for all magnetic degrees of freedom meaning
that a characteristic pattern of spin splitting of electronic
bands should coincide with an analogous chirality splitting pattern in the spin-wave spectrum. Evidence of such
a splitting of the magnon bands has been found in MnTe
using inelastic neutron scattering [32], but has not been
observed in the insulating candidate MnF2 [33].
Much of the theoretical activity in this field has been
focused on making detailed predictions of the properties of particular candidate altermagnetic materials using ab initio calculations of electronic band structures.
However, soon after the discovery of altermagnetism, it
was recognized that identification of candidate materials could be made on symmetry grounds under the assumption of weak SOC [4]. For this reason, lists of candidate altermagnetic materials have been compiled by
identifying materials possessing the characteristic magnetocrystalline symmetries from larger databases of magnetic materials [34]. It was further realized that the
ideal limit brings enhanced magnetic symmetries and
that these are intimately tied to the key features of altermagnetism [8, 15]. Understanding what properties of
altermagnets are consequences of these higher symmetries, and which are not, is thus an important question.
Further, understanding which features survive the introduction of weak spin-orbit coupling and whether those
features are unique to materials descended from ideal altermagnets is also essential in strengthening our understanding of the class of materials.
In this paper, we provide a general Landau theory of altermagnetism grounded in the enhanced symmetries enjoyed by these systems. By examining the ideal limit –
controlled by spin symmetries – and the physical setting
of finite SOC – controlled by ordinary magnetic symmetries – we are able to spell out many of the properties of
these systems independent of the details of the electronic
structure and also understand the extent to which properties of real materials are determined by the idealized
limit. Landau theory is the method of choice to study
properties common to the whole class of altermagnets

3
because it allows one to be precise about the symmetry breaking and characteristic order parameters of these
systems and to unify these with their observable features.
The paper is organized as follows. In Section II we
introduce altermagnets through a simple framework that
encodes their characteristic symmetries. We then formulate a criterion that identifies altermagnets based on the
transformation properties of the staggered magnetization
under the space group of the crystal. This criterion is
powerful enough to provide a complete classification of
altermagnets based on symmetry. We carry out this classification for all altermagnets where the magnetic unit
cell matches the crystal unit cell (i.e. Q = 0 order). We
include both centrosymmetric and non-centrosymmetric
crystal structures in our analysis. These results are summarized in a look-up table (presented in Table XII) containing those Wyckoff positions for each space group that
are altermagnetic if an appropriate collinear antiferromagnetic order is imposed at those sites. This result
provides a tool to comprehensively study all altermagnets
of a given crystal symmetry once the crystal symmetries
and magnetic structure are known and is conducive to
broad material searches for altermagnetic candidates.
Section III reviews the Landau theory of altermagnetism at zero SOC and in particular the fact that the
characteristic spin splitting can be inferred from the nature of a multipolar order parameter that is fixed by
the Néel order symmetry. Then using the classification
scheme from the previous section, we show that any altermagnet at zero SOC can be described by one of 54
possible Landau theories that we completely specify, including the associated multipolar order parameters and
spin splitting anisotropies. This unifies all zero SOC altermagnets into a simple scheme that can be applied to
any material candidate.
Section IV extends this analysis to Landau theories in
the more realistic case of altermagnetism at finite SOC.
The novelty of this (otherwise standard) analysis lies in
determining the special features arising from the particular magnetocrystalline symmetries of altermagnets, and
contrasting these with the ideal limit and with properties
of conventional antiferromagnets. Specifically, building
on the multipolar order parameter of the SO-free Landau
theory, we can identify symmetry-allowed characteristic
observables, such as the components of transport tensors
listed in Table V. Importantly, many of the characteristic responses that we identify at finite SOC are directly
implied by the features of the ideal altermagnetic state.
In Section V, we demonstrate the efficacy of our
method through a number of examples belonging to
different point groups. Our examples include CrF2 ,
La2 CuO4 , MnF2 , and Fe2 O3 . Throughout the text, we
use MnTe as a demonstrative example.
These discussions make reference to various comprehensive tables listed towards the end of the paper that
include: the classification of altermagnets, the tower of
multipolar couplings in the ideal limit together with explicit expressions for the lowest order multipole, and ta-

bles of allowed couplings to the Néel vector at finite SOC.
The paper is intended to be accessible to a general
audience with at least a cursory familiarity with group
theory. More technical discussions of various points may
be found in the Appendices. For example, in the main
text, we do not rely heavily on the formalism of spinspace groups though these are the complete symmetries
of the broken symmetry phase of altermagnets in the zero
SOC limit. In Appendices A and D, we explain why
we are able to avoid dealing with these groups for the
purposes of our analyses.

II.

ALTERMAGNETS FROM THEIR
SYMMETRIES

We begin this section with a general review of altermagnetism, translating the essential ideas into the language of representation theory. We then use this reformulation to perform a complete classification of crystal symmetries that are compatible with altermagnetism. We
note that our analysis concerns altermagnetism arising
from staggered dipolar order, and therefore does not encompass scenarios in which orbital ordering [35, 36], or
ferromultipolar order with zero dipolar moment [36, 37],
is responsible for altermagnetic spin-splitting.
Altermagnets are compensated collinear magnets with
intrinsic spin-split band structures at zero spin-orbit coupling 1 . The key is to identify magneto-crystalline symmetries that do not protect spin degeneracy. This can
be done in the simplest case, at zero spin-orbit coupling,
by first requiring collinearity of the magnetic structure
so that there is a global U(1) rotational symmetry in the
magnetic degrees of freedom. We further require that the
magnetic sublattices are related neither by inversion (I)
nor lattice translation (tR ).
Ideal altermagnets, due to their lack of SOC, have symmetries that transform only their spin degrees of freedom [4, 40–48]. For collinear spin arrangements, these
include all spin-space rotations about the moment direction, and all reflection planes containing this axis.
These spin-space mirror symmetries impose a constraint
on the bands requiring εs (k) = εs (−k) where s is spincomponent along the collinear axis. This can be seen by
expressing the spin-space mirrors as τ 2s⊥ , where τ denotes time reversal (the spin-inversion element) and 2s⊥
denotes a π spin-space rotation perpendicular to the mutual spin axis [42, 43, 49, 50]. This element preserves the
spin orientation while flipping the momentum.
When tR relates opposite spin sublattices, τ tR is a
symmetry of the magnetic state, and thus εs (k) =
ε−s (−k). Combined with the effect of the spin-space
mirrors, τ 2s⊥n , the bands then must be spin degenerate,

1 Generalizations

of the concepts to non-collinear compensated
magnets have been proposed [19, 38, 39]

4
εs (k) = ε−s (k). When I connects the magnetic sublattices in centrosymmetric systems, the collinear state
is invariant under τ I. Immediately, this symmetry also
implies spin-degenerate bands, εs (k) = ε−s (k).
Without τ I or τ tR as symmetries of the magnetically
ordered system, there is no constraint enforcing spin degeneracy throughout the entire Brillouin zone. As a result, opposite spin bands are generically split, though
they may remain degenerate along high symmetry lines
or points. Compensation of an ideal altermagnet must
then be enforced by a different symmetry relating the
opposite spin sublattices, an element that is neither I
nor tR .
The aforementioned symmetry constraints for ideal altermagnets can be encoded in the transformation properties of the Néel vector, N. Under transformations acting
only on the lattice (and not the spins, allowed by the
lack of SOC), N may at most change sign. Therefore,
N must transform as a one-dimensional, real representation, with the action of each lattice symmetry being +1
or −1 [4, 15, 19].
In the simplest case, N is assumed to be invariant under translations, implying that tR is represented by +1,
and the magnetic unit cell thus coincides with the crystallographic one (Q = 0 AFM order). The more general
case where the magnetic unit cell is enlarged is discussed
in Ref. [51]. For Q = 0 order at least, it is sufficient to
analyze transformation properties of N under the point
group of the lattice. Where there is inversion symmetry
in the magnetic structure, the invariance of N under I
means that in altermagnets I is also represented by +1
(and thus is in an inversion-even irrep of the point group).
Any such irrep, aside from the “trivial” irrep (where all
elements are represented by +1, corresponding to ferromagnetic order) is a potentially valid representation of
the symmetries of an altermagnetic order parameter.
Based on these transformation properties of N, one
can frame the search for altermagnetic orders as identifying structures in which N transforms as a nontrivial 1D
inversion-even irrep of the crystal point group. Practically, this can be accomplished by constructing a collinear
antiferromagnetic (AFM) order on each Wyckoff position
(WP) in each space group and isolating the cases where
the corresponding irrep ΓN under which N transforms
obeys the symmetry constraints described above. A detailed procedure for accomplishing this for an arbitrary
space group and WP is provided in Appendix C, and the
complete set of WPs compatible with altermagnetism is
given in Table XII. As there is a growing need for materials identification and design [52], these results may
help focus search efforts. We note here that our analysis
encompasses all viable WP (i.e. those of multiplicity two
or greater), and is thus distinct from and expands upon
the work of [53].
A few general results can narrow our search. First, we
can immediately rule out crystals with point groups 1, 1,
2
3, 3, 23, and m
3 because they contain no irreps satisfying
the conditions for altermagnetism. This omission leaves

TABLE I. Point groups supporting altermagnetic phases, corresponding space groups as they appear on Bilbao Crystallographic Server [54], and the irreducible representation ΓN under which the Néel vector N transforms. Note: non-conjugate
space groups arise with conjugate point groups 42m and
4m2, as well as 62m and 6m2. If these point groups are
treated as distinct, then in total, there are 54 altermagnetic
point groups irreps. Otherwise, there are 48.
Point group

Space group

ΓN irrep. of N

2

3–5

{B}

m

6–9

{A′′ }

2/m

10–15

{Bg }

222

16–24

{B1 , B2 , B3 }

mm2

25–46

{A2 , B1 , B2 }

mmm

47–74

{B1g , B2g , B3g }

4

75–80

{B}

4

81, 82

{B}

4/m

83–88

{Bg }

422

89–98

{A2 , B1 , B2 }

4mm

99–110

{A2 , B1 , B2 }

42m

111–114

{A2 , B1 , B2 }

4m2

115–122

{A2 , B1 , B2 }

4/mmm

123 –142

{B1g , A2g , B2g }

32

149–155

{A2 }

3m

156–161

{A2 }

3m

162– 167

{A2g }

6

168–173

{B}

6

174

{A′′ }

6/m

175, 176

{Bg }

622

177–182

{A2 , B1 , B2 }

6mm

183–186

{A2 , B1 , B2 }

6m2

187, 188

{A′2 , A′′1 , A′′2 }

62m

189, 190

{A′2 , A′′1 , A′′2 }

6/mmm

191–194

{B1g , A2g , B2g }
{A2 }

432

207–214

43m

215–220

{A2 }

m3m

221–230

{A2g }

26 of the 32 point groups that may host altermagnetic
order and 210 of the possible 230 space groups compatible
with altermagnetism listed in Table I.
We find that each of the 210 possible space groups
has at least one Wyckoff position that can support altermagnetism. Of the 1731 space group WPs, 1197 may
host altermagnetic order. More specifically, if we were
to count all sublattice orders generated by irreps on the
Wyckoff positions, 1941 out of 6714 options satisfy the
altermagnetic constraints. Altermagnetism, at least at
the level of symmetries, is therefore quite common and
one may expect to find many altermagnetic materials.
We note that in non-centrosymmetric groups, all

5
nontrivial, real, one-dimensional irreps correspond to
symmetry-compensated collinear magnetic order, coinciding with altermagnetism.2 If the magnetic unit cell
is not enlarged, any collinear antiferromagnet in these
space groups will necessarily be altermagnetic.
This analysis can be simplified by realizing that there
are 54 real, one-dimensional, nontrivial, and inversioneven (where applicable) irreducible representations of the
26 viable point groups, providing only 54 distinct SO-free
Landau theories. Studying these 54 cases, as opposed to
studying each structure defined by the possible Wyckoff positions, allows us to develop a broader understanding of altermagnets, more clearly delineate their common
properties, and identify what distinguishes different realizations.

III.

ALTERMAGNETIC LANDAU THEORY AT
ZERO SOC

Landau theory is a general framework for understanding symmetry-broken states of matter in terms of their
order parameters alone. Constrained only by the nature of the symmetry breaking, Landau theory allows
for generic predictions of properties near the phase transition, as well as the dependence of symmetry-allowed
response functions on the order parameter. We are interested in a second-order (or weakly first-order)transition
passing from a high-symmetry phase to an ordered phase
whose symmetries form a subgroup of those present in the
original phase.
For ideal altermagnets, the appropriate order parameter is the Néel vector N, which describes a staggered
magnetization. The high-symmetry paramagnetic phase
is invariant under all possible global spin transformations (rotations and time inversion), as well as all crystal
symmetries (i.e. the space group). Therefore, the general Landau theory for the thermodynamic potential (Φ)
takes the form
Φ(N) = a2 (N · N) + a4 (N · N)2 + . . . ,

(1)

where we have assumed Φ is an analytic function of the
order parameter, N. In the ordered phase, the order
parameter acquires a nonzero value, N ̸= 0. Because
ideal altermagnets lack SOC, the symmetries that leave
N invariant do not correspond to a magnetic space group,
where all transformations act simultaneously on spin and
lattice degrees of freedom. Instead, they belong to a more
general group of transformations: a spin-space group [40–
42, 50]. A spin-space group consists of all operations on
real space and spin space that leave the magnetic structure invariant, allowing for operations that transform the

spins and the lattice differently. All terms in the free energy and all combinations of N with other quantities that
N can couple to must transform trivially under the spin
group.
In the next brief subsection, we first show that these
conditions may be recast so that the Landau theory can
avoid using the language of spin groups, instead only requiring the more familiar point group symmetries.

A.

Spin groups to point groups

In the ideal altermagnetic phase, N transforms as the
trivial irrep of a spin group. We may alternatively view
N as transforming under a nontrivial irrep of the SO-free
paramagnetic group since this group is not the symmetry group of the ordered phase. Thus, to avoid using
spin groups one can make a trade-off and construct the
Landau theories using the nontrivial irreps of the SOfree paramagnetic group instead of the trivial irrep of
the more complicated spin group. In this case, quantities allowed to couple linearly must have in common at
least one irrep of the SO-free paramagnetic group.
We note that the formal Landau theory in terms of
spin groups can be recovered by restricting the SO-free
paramagnetic group to elements of the appropriate spin
group: with this restriction, N will transform trivially.
Appendix A details how this restriction reproduces the
Landau theory based on the spin group and provides an
in-depth justification of bypassing spin groups in the Landau theory.
The power of recasting the Landau theory in terms
of the SO-free paramagnetic group lies in the fact that
this group is a direct product of spin-space operations
and the space group. It turns out that for the cases relevant to Q = 0 collinear altermagnetism, the irreps of
this group are direct products of the irreps of its factors
(see Appendix B). This factorization of irreps enables
us to separate the spatial and spin degrees of freedom.
Recalling that N transforms trivially under translations,
we can restrict our focus to spatial symmetries of the
SO-free paramagnetic point groups. Here, N transforms
as a time-reversal odd vector under spin-space transformations, and under any ΓN of the crystal point group
satisfying the constraints in Sec. II.
So far, the Landau theory does not set altermagnets
apart from other SO-free antiferromagnets, except in
the particular transformation properties of N discussed
above. We now see that the essential features of ideal
altermagnets follow from the Landau theory formulated
in this setting.

B.

Secondary Multipolar Order Parameters for
zero SOC

2 We do not address compensated ferrimagnetism, which is possi-

ble when relaxing the constraint that compensation is symmetryenforced.

Secondary multipolar order parameters have significant implications for the spin-splitting structure of elec-

6
tronic bands, and they determine entire classes of observable quantities that couple to N in the presence of
SOC [19]. Momentum space multipoles have been utilized to classify spin-splitting [16, 53] and as order parameters [29] in altermagnets and in the broader context of
electronic band structures in magnetic materials [7, 55–
57]. Our results differ from these in that they fully exhaust all possibilities for collinear Q = 0 altermagnets,
and are applicable beyond the analysis of electronic spinsplitting.
The spirit of Landau theory is to identify all couplings
allowed by the choice of primary order parameter which
itself is defined through its symmetry properties. Here
the primary order parameter is N. For each of the 26
viable spin groups admitting altermagnetism, identified
in Table I, we may identify a multipolar order parameter
that couples linearly to N. We consider the time-reversal
breaking, spin symmetric, (magnetoelectric) multipoles
of the form
Z
d3 r [rµ1 · · · rµn ] m(r),
(2)
where n is a positive integer, rµ are spatial coordinates (x, y, or z), and m is the local magnetization density. The square brackets indicate symmetrization under permutations of the spatial coordinates x, y, and z.
We refer to this quantity as a magnetoelectric (n + 1)multipole, that is composed of a rank-1 time-reversal
breaking spin-dipole and a rank-n spatial multipole. For
example,
n = 0 corresponds to the magnetization M =
R 3
d r m(r), n = 1 is an inversion-breaking magnetoelectric quadrupole that
transforms as a rank-1 tensor in
R
both spin and real space d3 r rµ m(r), and n = 2 is an
inversion-symmetric
octupole with a rank-2 spatial comR
ponent d3 r [rµ1 rµ2 ] m(r).
For ideal altermagnets, we can always find some multipole of the form Eq. 2 that couples linearly to N [19].
A linear coupling requires that the decompositions of the
representations of N and the multipole into irreps of the
SO-free paramagnetic group have at least one irrep in
common. In spin space, the multipoles and N already
transform identically: the local magnetization density
m(r) and the Néel vector N transform as time-reversal
odd vectors under spin-space rotations and time inversion. Now, we must only check for compatibility between
N and the multipole under point group transformations,
noting that without SOC the magnetization density m(r)
transforms trivially under real space operations.
Because N transforms as ΓN under point group symmetries, the condition for linear coupling to an (n + 1)multipole amounts to checking that ΓN is contained in
the representation under which [rµ1 · · · rµn ] transforms3 .

3 As N and the multipole component transform identically the

latter is strictly not a secondary order parameter but a pseudoprimary order parameter. “Secondary” typically denotes an order parameter that transforms under a different irrep than the
primary order parameter [58].

d wave

g wave

i wave

FIG. 1. Illustrations of all possible altermagnetic spinsplitting anisotropies in momentum space allowed by symmetry. These correspond to the spatial anisotropies of the
lowest order multipole that can couple to the aletermagnetic
order parameter N.

Jahn Notation
In the following, we use the Jahn symbols [59, 60]
to denote the intrinsic symmetry properties of a tensor. In this notation, the symbol a marks the timereversal odd property, and e specifies that the tensor
is axial (i.e. inversion-even). The exponent of V n
corresponds to the rank of the tensor. For example,
the magnetization transforms as aeV (in the typical,
SOC case), corresponding to a time-reversal odd axial vector (rank-1 tensor), and the electric polarization would belong to V , a polar and time-reversal
even vector. Additionally, symmetry (antisymmetry) of pairs of indices is denoted by square (curly)
brackets. In this notation, [rµ1 · · · rµn ] transforms as
[V n ], a time-reversal even rank-n polar tensor that
is symmetric in all of its indices.
We find all SO-free Landau theories by determining the
n for which the multipole in Eq. 2 couples to N, for every possible altermagnetic structure. Each altermagnetic
structure found in Sec. II is identified in Table XII by a
Wyckoff position and an irrep ΓN of the crystal point
group. We check for all n ≤ 6 whether ΓN is contained
in [V n ], with the results listed in table XIII.
We then focus on the minimal multipole (i.e. with the
smallest possible n) and find the specific multipole com-

7
a

b

c

a

b

FIG. 2. The crystal structure of MnTe with space group symmetry P 63 /mmc. Magnetic Mn ions (red and blue denote
magnetic sublattices) reside on the 2a Wyckoff positions, at
{0, 0, 0} and {0, 0, 21 } within the unit cell. The Te ions (gray)
occupy the Wyckoff positios 4e, at { 31 , 23 , 14 }, and { 23 , 13 , 34 }.

ponents (by specifying the rµi appearing in Eq. 2) that
couple to N. The technical details of this procedure are
provided in Appendix F, and the multipole components
are given for each ΓN of every point group in the third
column of Table XIV. These results fully determine the
SO-free Landau theory.
As an example, let us consider the SO-free Landau theory for the semiconductor MnTe, whose crystal structure
and magnetic sublattices are given in Fig. 2. MnTe has
a Néel temperature of about 307 K. The space group for
this material is P 63 /mmc (No. 194), corresponding to
the point group 6/mmm. The magnetic Mn atoms reside
at the 2a Wyckoff position [26–28, 61–66]. By considering
which point group elements swap magnetic sublattices,
we find that the irrep of the altermagnetic Néel vector for
this crystal structure is ΓN = B2g (in agreement with the
tabulated result in Table XII). We systematically check
for which n the [V n ] representation contains the B2g irrep. The spatial part of the n = 1 multipole transforms
as V , the polar vector representation of 6/mmm, whose
decomposition A2u ⊕ E1u lacks ΓN . Neither [V 2 ] nor
[V 3 ] contain B2g in their decompositions, excluding the
n = 2 and n = 3 multipoles. The first multipole allowed to
couple with N is the n = 4 multipole. Here, [V 4 ] decomposes as 3A1g ⊕ B2g ⊕ B1g ⊕ 3E2g ⊕ 2E1g , containing B2g .
For each of the irreps appearing in this decomposition,
there is an appropriately transforming (set of) fourthorder polynomials in the rµ . The polynomial transforming as B2g is yz(y 2 − 3x2 ) as described in Appendix F.
Thus, theR precise SOC-free multipole coupling to N in
MnTe is d3 r yz(y 2 − 3x2 )m(r). The next allowed multipole has n = 6, as shown in Table XIII.
The spatial polynomials appearing in the secondary
(or pseudo-primary) multipolar order parameter are related to the spin-splitting pattern of electronic bands.
In centrosymmetric structures, we can identify the spinsplitting pattern with the n−order of the secondary multipole [19]. This correspondence follows from the sym-

metry equivalence of real-space terms rµ1 ...rµA m(r) and
reciprocal space terms kµ1 ...kµA s, where s is the spin of
a band [7, 16, 19]. In this context, the lowest order multipole being n = 4 in the above example of MnTe is
consistent with the observed g−wave spin-splitting pattern 4 [19]. When inversion is a symmetry, n is always
even because a polar vector changes sign under inversion.
The non-centrosymmetric altermagnets, allowing for
both even and odd n multipoles, deserve an additional
remark in connection to the spin splitting. The spin splitting is always even in momentum regardless of whether
the system is centrosymmetric or non-centrosymmetric,
due to the τ 2s⊥n symmetry present for collinear spins. We
find, however, that the lowest order multipole is often of
odd n. In these cases, the spin splitting is not dictated
by the lowest order multipole, but by the dominant even
multipole.
In addition to capturing the pattern of spin splitting in momentum space, the multipolar order parameter has a more direct interpretation as a local multipole
in the magnetization density of altermagnetic materials,
expected to be observable experimentally [19, 67].
IV.

ALTERMAGNETIC LANDAU THEORY AT
FINITE SOC

So far we have focused on the zero spin-orbit coupled
limit where altermagnetism is most clearly defined. In
this limit, we have been able to determine all possible
crystalline symmetries compatible with altermagnetism
and we have found the finite number of Landau theories
and multipolar order parameters corresponding to these
cases.
In real materials, spin-orbit coupling is finite. What
this means for the magnetic properties at the microscopic
level is somewhat involved. The specifics depend, among
other things, on the precise orbital content, the nature
of the spin-orbit coupling, and the crystal field. Here we
side-step these details and focus on the consequences of
symmetry alone.
We identify the lowest-order multipolar order at finite
SOC, to see what intrinsic features of zero SOC altermagnets are inherited by real materials. Then, we concern
ourselves with the physics of real materials by determining, on symmetry grounds, what responses are expected
in altermagnets. For example, noteworthy features of
certain metallic altermagnets are that they support spin
currents or anomalous Hall conductivity among other exotic transport properties.
We organize this section by first making some general
remarks about the nature of Landau theories for altermagnets at finite SOC. Then we provide a group theo-

4 We briefly comment that the choice of axes differs between this

work and that of Ref. [19], which results in a relabelling of the
B1g and B2g irreps

8
retic result that allows us to generalize the observations
of the next section to the full class of altermagnets. Then
we discuss the finite SOC analogs of the multipolar order
at zero SOC thus connecting the ideal limit to realistic
systems. Finally, we give an overview of the observable
quantities that might be of interest in the context of altermagnetism including their symmetry properties. In
the following section, we apply all these ideas to specific
materials candidates.
A.

Altermagnetic Landau Theories at Finite SOC:
General Remarks

Previously we observed that Landau theories at zero
SOC are completely determined from the transformation
properties of the Néel vector N, described by some irreducible representation, ΓN , of the crystal point group.
Crucially, in the paramagnetic phase, this Landau theory
is completely symmetric under spin rotations of N. The
full symmetry of the problem is the group of all rotations
SO(3) in spin space, along with G + τ G, where G is the
space group of the crystal acting purely on the lattice,
and τ denotes time reversal. Here, transformations of
the system may differ in spin-space and real space.
When SOC is finite, the symmetry group of the paramagnetic phase is lower because spatial transformations
and spin transformations are locked: transformations on
spins and the lattice are identical, with the caveat that
the spins transform axially. Pure spin rotation symmetry
is lost, meaning that the full symmetry of the SO-coupled
paramagnetic phase is given by G + τ G. Restricting our
attention again to Q = 0 orders, the moments transform
under the time reversal odd axial vector representation
of the point group of the lattice, denoted as aeV in Jahn
notation [59, 60] (introduced briefly in Sec. III), and the
Néel vector N transforms as
aeV ⊗ ΓN .

(3)

For example, in the previous section, we saw that for
MnTe, the irrep ΓN corresponds to B2g of 6/mmm. The
axial vector representation for 6/mmm decomposes as
A2g ⊕ E1g , where the 2D irrep corresponds to axial x and
y components. Thus, by taking the product of ΓN and
aeV we find that the Néel vector components {Nx , Ny }
and Nz transform as E2g and B1g respectively. If we restrict to an in-plane N = Nx x̂+Ny ŷ, as is experimentally
observed [68], then the Landau theory is given by
Φ = a2 (Nx2 + Ny2 ) + a4 (Nx4 + Ny4 ) + . . .

(4)

In the following subsection, we determine which tensors
can couple linearly to components of N.
B.

Coupling to the Néel Vector at Finite SOC

In this section, we give a simple criterion that allows
one to assess whether some components of a tensor ob-

servable ξ couple linearly to N, based on knowledge of
the multipolar order parameter of the SO-free theory. In
other words, we tie together features of the spin-splitting
at zero SOC and physical properties at finite SOC.
To set the stage, let ξ be a tensor that transforms under a representation Γξ of the spin-orbit coupled paramagnetic group. This tensor corresponds to some physical observable of the altermagnetic phase that we wish
to probe, such as electrical conductivity, magnetoresistance, etc. We also suppose that the SO-free theory
has a spin symmetric multipole with a spatial component transforming as [V n ] where n is the lowest rank
that appears in the Landau theory.
Linear coupling between N and ξ is allowed if their
representations share at least one common irrep in their
decompositions. This criterion is equivalent to the trivial
irrep appearing in the decomposition of Γξ ⊗ (aeV ⊗ ΓN ).
Recall that aeV is the time reversal odd axial vector representation. We may recast this condition into a more
practical form: that ΓN must appear in the decomposition of Γξ ⊗ aeV . That this condition is equivalent may
be seen by first invoking associativity of the direct product, so that we seek the trivial irrep in (Γξ ⊗ aeV ) ⊗ ΓN .
Then, it is clear that (Γξ ⊗ aeV ) must contain ΓN in
its decomposition for the trivial irrep to appear in this
product.
In our analysis of the SO-free limit, we established that
the lowest order altermagnetic multipolar order parameter coupling linearly to N has the smallest n for which ΓN
is contained in [V n ]. Therefore, if [V n ] is fully contained
in Γξ ⊗ aeV then ΓN will also be contained in Γξ ⊗ aeV ,
meaning N will couple to ξ. This criterion
[V n ] ⊆ Γξ ⊗ aeV

(5)

connects the Landau theories with and without SOC,
and allows us to identify quantities ξ directly predicted
by the SO-free analysis. We shall additionally see that
these ξ can differentiate between altermagnetic and nonaltermagnetic phases.
For a given (n + 1)-multipole from the SO-free theory,
we identify representations Γξ for which [V n ] is contained
in Γξ ⊗ aeV. Viable Γξ meet this condition for all point
groups; the presence of the (n + 1)-multipole without
SOC then guarantees coupling between N and ξ when
SOC is included, and this feature is a universal property
of the (n + 1)-multipole. Observables ξ obtained in this
fashion are fundamental in altermagnets; they arise due
to secondary multipolar order present in the ideal altermagnetic phase.
In Table II, we list the representations Γξ of the tensors that can couple linearly to N, based on the presence
of an (n + 1)-multipole. This table is somewhat spartan
containing only Jahn symbols of coupled quantities at
each multipolar rank. Later, we demonstrate the utility
of this table and spell out examples of explicit components of particular physical quantities that are relevant
to altermagnetism. A partial list of physical quantities

9
TABLE II. The representation Γξ for quantities ξ is guaranteed to couple linearly to N in the presence of SOC, based
on the rank-n multipole in the SOC-free limit. The representations are denoted by Jahn symbols, where aV is a timereversal odd (a) polar vector (V ), aeV is a time-reversal odd
(a) axial vector (eV ), aeV 2 is a time-reversal odd axial tensor of rank 2, and aeV [V 2 ] is a time-reversal odd axial rank-3
axial tensor that is symmetric in two indices. The n = 5 case
is absent because this multipole is not minimal for any irrep
of any point group (see Table XIII).
Multipole rank (n)

Representation Γξ

1

aV , aeV 2

2

aeV

3

aeV 2

4, 6

aeV [V 2 ]

of interest is given in Table V together with their transformation properties labeled by Γξ .
To give a flavor of how this table can be used, we return
to the case of MnTe. Recall from Sec. II that the minimal SO-free multipole for this system has spatial rank
n = 4. From Table II, any tensor transforming as aeV [V 2 ]
can couple to N. In words, these are spatially symmetric
rank-2 tensors times an axial time-reversal odd vector.
In Sec. IV E we make explicit the coupling between components of ξ and the components Ni of the Néel vector,
and to make concrete the physical quantities corresponding to ξ.
We emphasize that the observables ξ, derived from the
SO-free limit, are not the only quantities that are allowed
to couple to N in the spin-orbit coupled altermagnetic
phase. There are other quantities N can couple to, but
we would not view these quantities as being fundamentally related to the altermagnetism as they do not follow
from the idealized limit. Up to tensors of rank three, the
representations Γξ listed in Table II are the only types of
tensors fundamentally implied by the SO-free theory.

C.

Distinguishing between Néel AFMs and
Altermagnets

orders are odd.
In the end, the distinction is simple to state: any
inversion-even tensor couples linearly exclusively to altermagnets, while an inversion-odd tensor will couple only
to non-altermagnetic N, provided Q = 0.

D.

Multipolar Order in Altermagnets at Finite
SOC

We briefly question whether the secondary multipolar
order parameter, crucial to the SO-free theory, plays a
role in the finite SOC limit. Consider, again, multipoles
of mixed polar and magnetic character as in Eq. 2. Now,
with SOC these multipoles transform as aeV ⊗ [V n ]. The
multipoles for n equal to that of the SO-free case are
still able to couple to N in the presence of SOC, as both
share aeV, and we know ΓN ∈ [V n ]. As such, even in the
presence of SOC, the multipoles act as a secondary (or
pseudoprimary) order parameter.
To be concrete, we find the components of the multipole coupling to N for MnTe with SOC, which has
ΓN = B2g . One can show that from Eq. 3, the Nx
and Ny components of the Néel vector transform as
E2g , while Nz transforms as B1g . Since n = 4 is the
spatial order of the SO-free multipole, the SOC multipole transforms as the aeV ⊗ [V 4 ] representation of
6/mmm. The irrep decomposition for this representation
is 2A1g ⊕ 5A2g ⊕ 4B2g ⊕ 4B1g ⊕ 7E2g ⊕ 8E1g . Because this
decomposition contains B1g and E2g , the SOC multipole
for MnTe can couple to all components of the Néel vector.
From this calculation, it follows that there are four B1g
multipoles and seven E2g multipoles that are relevant to
the spin-orbit coupled case, a much richer selection than
the spin-orbit free case.

TABLE III. Transformation properties of the order parameter N in MnTe and the part of the integrand of the n = 4
spin-orbit coupled multipole in Eq. 2 to which the Néel vector
component couples.
Irrep.

Néel component

Multipole component
(x3 − 3xy 2 )zmz

Both altermagnetic and non-altermagnetic AFMs are
collinear, compensated magnetic structures. This makes
them difficult to distinguish in experiment. Here, we
underline that the ξ found in the previous section
are unique to altermagnets, in the sense that a nonaltermagnetic Néel AFM would not have a linear coupling between N and these quantities. We only need
to distinguish between these cases in centrosymmetric
crystals, since there is no distinction between altermagnetic and non-altermagnetic collinear AFM order in noncentrosymmetric crystals, as discussed in Sec. II. The
distinction between these two types of orders is a consequence of their parity under inversion symmetry. When
Q = 0, altermagnets are even, while non-altermagnetic

mx 
my
m 
(y 3 − 3yx2 ) ( xy )⊺ −myx
 2 2 ⊺
mx 
−y
z 2 x−2xy
my

(x − 3xy 2 ) ( xy )⊺
3

B1g

Nz

mx 
my
m 
2
1 3
z(xy − 3 x ) −myx
2xy
z 2 x2 −y2 mz

z(x2 y − 31 y 3 )

E2g

Nx
Ny

!



1 xy 3
x3 y− 3
2 2

x y



3

1 y4
−3
3


mz


2x y+2xy
mz
4
4

x −y
xmy +ymx
3
z xmx −ymy


xm +ym
z(x2 + y 2 ) xmxy −ymxy

10
Despite the complexity of the allowed multipoles in
MnTe with SOC it is instructive to see how to compute
the multipolar components that couple linearly to the
Néel vector in at least one case. This can be accomplished
using the procedure outlined in Appendix F. Because B1g
squares to the trivial irrep, Nz may couple to any of the
four B1g multipole components listed in Table III. And,
similarly, any of the seven symmetry-allowed multipolar
components may couple to the (Nx , Ny ) components.
The transformation properties of the Néel components
and multipole components are shown in Table III, where
we provide the integrand of the multipole from definition
Eq. 2. In each case, we have expressed the multipole
components in a simple basis, such that the dot product
with (Nx , Ny ) yields the allowed coupling. As the moments in the ordered phase of MnTe lie in the triangular
planes [68] the E2g multipoles are the ones that are experimentally relevant. As we should expect, when SOC
is present, the multipole is tied to the direction of the local magnetization density. In common with the SOC-free
case, the relevant multipoles are time-reversal odd with
rank n = 4 though the pattern of nodes is very different
to the case of the SOC-free multipole.
In general, the condition of Eq. (5) is equivalent to the
condition that the SOC multipole representation is contained within Γξ . This fortifies the notion that the multipolar order parameter plays a central role in dictating
the behavior of altermagnets.
As the example of MnTe indicates, we should expect a
considerable increase of complexity in the allowed multipoles in passing from the SO-free to the spin-orbit coupled case. While the SO-free analysis provides simple,
direct information about spin-splittings of the bands of
ideal altermagnets we do not expect detailed information
about multipoles in materials to shed much light on the
general phenomenon of altermagnetism. Therefore, we
do not tabulate the SOC multipole couplings in general.
However, because multipoles with SOC may be of interest in specific instances we emphasize that they may be
obtained using the same technique as all other tabulated
couplings that is described in Appendix F.

E.

Experimental Signatures of Altermagnetism

The goal of this section is to spell out the framework
that will allow us to make experimental predictions about
the behavior of altermagnets based on symmetry alone.
To this end, we now identify some concrete physical quantities corresponding to the tensor ξ from Sec. IV B. Further, we predict which components of ξ are generically
non-zero.
In Table V we provide a list of common equilibrium,
transport, and optical material properties transforming
under the representations Γξ identified to be relevant for
altermagnets in Table II (sourced from MTENSOR [60]).
For each property, we list its name and defining equation.
In some cases, the full tensor has one of the desired trans-

TABLE IV. Transformation properties of the order parameter
N in MnTe and the part of the magnetoresistance that is
symmetric in the first two indices.
Irrep.

Order
parameter

Magnetoresistance component

B1g

Nz

S
S
S
2Rxyx
+ Rxxy
− Ryyy


S
2Rxyz
S
S
Rxxz − Ryyz
 S

S
Ryzx + Rxzy
S
S
Rxzx
− Ryzy


E2g

Nx
Ny



formation properties. In other cases, it is only a part of
the tensor that transforms under a Γξ ; we specify this in
the fourth column of Table V.
For some tensors, the (anti)symmetric part may be
‘repackaged’ into a smaller object. A canonical example is the anomalous Hall conductivity (AHC), the antisymmetric part of the electrical conductivity tensor. In
Jahn notation, the full conductivity tensor transforms as
[V 2 ]∗ , a rank-2 polar tensor, with the time-reversal property τ σij = σji , denoted by the starred square bracket
A
[ ]∗5 . The AHC tensor, σij
= 12 (σij − σji ) transforms as an antisymmetric time-reversal odd rank-2 tensor a{V 2 }, whose three independent components, σyz ,
σzx , and σxy , can be “repackaged” into a magnetic axial
vector, σ = {σyz , σzx , σxy }, transforming as aeV . For
details about the repackaging of tensor components in
Table V see Appendix G.
Having fixed a set of observables, we compute the components of these quantities that couple linearly to components Ni of the Néel vector. These results are provided
for each point group in the final column of Table XIV.
To see how this information may be of use, we again
consider MnTe. In Sec. IV B we concluded that the MnTe
order parameter, N, couples to aeV [V 2 ] tensors due to
its n = 4 SO-free multipolar order parameter. One may
be interested, for example, in the non-zero components of
the magnetoresistance, Rijk , for spintronics applications.
We focus on the part that is symmetric in the first two
S
indices, Rijk
, as this part transforms as aeV [V 2 ]. We
have seen already that {Nx , Ny } transform under the E2g
irrep of 6/mmm, while Nz transforms as B1g . Our task
S
now is to find the components Rijk
that may couple to
Ni , i.e. components of these observables that transform
under the same irrep. The transformation properties of
S
Rijk
and Ni are listed in Table IV.

5 In ‘generalized’ Jahn notation [60], the star denotes that time-

reversal relates a tensor element to some other tensor element,
potentially of a different tensor (such as for the Seebeck and
Peltier effect).

11
TABLE V. Tensors transforming under the representations in Table II. In the last column, we denote the tensor part transforming under Γξ (details can be found in Bilbao’s MTENSOR package [60] and in Appendix G). Superscripts A and S indicate
the symmetric and antisymmetric parts of a tensor, respectively. Furthermore, εαij is the Levi-Civita symbol, Ji denotes an
electric current density, Ei an electric field, qi a thermal current, Hi a magnetic field, T temperature, Σij the stress, εij the
dielectric tensor, and ρij the resistivity tensor. Most notation coincides with that of Ref [60]. For aeV [V 2 ] our Jahn symbol
does not indicate which indices are symmetrized. All inverse effects have the same transformation properties and are omitted
from the table for brevity. All of these observables may appear in non-centrosymmetric altermagnets, while in centrosymmetric
altermagnets only those corresponding to even n multipoles may appear.
Γξ
aV

aeV

aeV 2

aeV [V 2 ]

n
1

2

1&3

4&6

Quantity (ξ)

Defining equation

Tensor part

Polar Toroidal Moment Ti

-

Full

Pyrotoroidic tensor ri

Ti = ri ∆T

Full

Magnetization Mi

-

Full

Electric conductivity σij

Ji = σij Ej

A = 1ε
σA
σα
2 αij ij

Soret thermodiffusion tensor sij

Ji = sij (∇T )j

1
A
sA
α = 2 εαij sij

Thermal conductivity κij

qi = κij (∇T )j

1
A
κA
α = 2 εαij κij

Peltier tensor πij

qi = πij Jj

Seebeck tensor βij

Ei = βij (∇T )j

Spontaneous Faraday effect Fij

-

A + βA )
S̃α = 12 εαij (πij
ij

Fα = 12 εαij Fij

Magnetoelectric tensor αij

Mi = αij Ej

Full

Piezomagnetic tensor Λijk

Mi = Λijk Σjk

Full

Second order magnetoelectric tensor αijk

Mi = αijk Ej Ek

Full

S
Magneto-optic Kerr effect zijk

S H
εij = izijl
l

Full

A
Quadratic magneto-optic Kerr effect iCijkl

A H H
εij = Cijkl
k l

A
Cαkl = 12 εαij Cijkl

Magnetoresistance Rijk

Ei = Rijk Jj Hk

S = 1 (R
Rijk
ijk + Rjik )
2

Righi-Leduc magnetorhermal tensor Qijk

qi = Qijk (∇T )j Hk

1
QS
ijk = 2 (Qijk + Qjik )

Ettinghausen tensor Mijk

qi = Mijk Jj Hk

Nernst tensor Nijk

Ei = Nijk (∇T )j Hk

Magnetic resistance tensor Tijkl

Ei = Tijkl Jj Hk Hl

A = 1ε
Tαkl
TA
2 αij ijkl

Magneto-heat-conductivity tensor Sijkl

qi = Sijkl (∇T )j Hk Hl

A = 1ε
Sαkl
SA
2 αij ijkl

Piezoresistivity tensor Πijkl

∆ρij = Πijkl Σkl

1
A
ΠA
αkl = 2 εαij Πijkl

Magneto–Seebek tensor αijkl

Ei = αijkl (∇T )j Hk Hl

Magneto-Peltier tensor Pijkl

qi = Pijkl Hk Hl Hj

The direct product B1g ⊗ B1g is A1g, providing the
S
S
S
invariant term Nz 2Rxyx
+ Rxxy
− Ryyy
. The products
of the E2g irreps decompose as A1g ⊕ A2g ⊕ E2g , and so
we expect one invariant coupling for each of the two E2g
irreps. The pairs of components in Table IV are expressed
such that their dot product with the in-plane Néel vector
gives rise to the allowed couplings.
S
S
The couplings in Table IV indicate that Rxyx
, Rxxy
,
S
S
S
S
S
S
S
S
Ryyy , Rxyz , Rxxz , Ryyz , Ryzx , Rxzy , Rxzx and Ryzy may
all generically be non-zero in MnTe. However, with N
restricted to an in-plane N = Nx x̂ + Ny ŷ in accordance
S
S
with experimental data [68], we expect Rxyx
, Rxxy
and
S
Ryyy to be zero.
Similar couplings between the order parameter and any
of the possible tensors can be found using the procedure
outlined in Appendix F. In Table XIV, we explicitly list
the couplings between Nα and tensor components of ξ
transforming under each possible representation Γξ . In
this table, polar vector (V ) components are expressed as
x, y and z, while axial vector (eV ) components are de-

S + NS )
Sijk = 12 (Mijk
ijk

A
Ã = 14 εαij (αA
ijkl − Pijkl )

noted by Rx , Ry and Rz . For example, the first coupling
in Table IV appears in Table XIV in a more general form,
applicable to any aeV [V 2 ] tensor, as
 
Nz 2xyRx + x2 − y 2 Ry .
(6)
In constructing the couplings in Table IV, then, Ni comS
ponents couple to Rijk
where i, j are given by the polar
components, and k is given by the axial components appearing in Eq. 6. For example, the first term in Eq. 6 corS
responds to the Nz Rxyx
term in the B1g coupling from
Table IV. Tables II and V can guide the experimental diagnosis of altermagnetic phases once the rank n of the
minimal SO-free multipole is determined. Taking the
representations Γξ guaranteed by the rank-n multipole
from Table II, one finds the corresponding measurable
quantities in Table V.
We have reduced the analysis of altermagnets from
hundreds of Wyckoff positions to 54 SO-free Landau
theories, and to four cases of measurable responses we
may expect, as shown in Table II. For example, a min-

12
imal multipole with n = 2 in the SO-free theory guarantees coupling to any magnetic axial vector, such as
the anomalous Hall conductivity (AHC), magnetization,
pyromagnetic tensor, etc., as listed in Table V. As we
have just seen, coupling with an n = 4 SO-free multipole,
as in MnTe, guarantees coupling to any aeV [V 2 ] quantity, including magnetoresistance, piezomagnetism, the
magneto-optic Kerr or Nernst effects, among others listed
in Table V. By combining the physical properties in Table V with the explicit tensor components in Table XIV,
we have laid foundations for the prediction of an abundance of experimentally accessible features of collinear
altermagnets.
For example, one can consider the generation of spincurrents by the application of electric fields – an important potential application of altermagnetic materials.
s
Here the spin conductivity σµν
has three indices: two
spatial indices µ,ν, and an index in spin space (here written as a vector). If we consider the symmetric components of this tensor, they are axial and odd under timereversal and thus transform as ae[V 2 ] spatially and as an
axial vector in spin space. Since N is time odd, axial,
transforms as a vector in spin space and as ΓN spatially,
s
and N thus requires that
a linear coupling of σµν
ΓN ⊆ [V 2 ]
This linear coupling then requires that the lowest-rank
multipole is n = 2 (a quadrupole).
This result can be made considerably stronger: altermagnets whose lowest rank multipoles have n > 2 have
vanishing spin conductivity. To see this, note that the
only axial, time-odd quantities that transform as a vector spin space that can be created using N are of the
form f (|N|2 )N where f is an arbitrary function. As |N|2
transforms trivially, this again transforms as ΓN and so
s
if ΓN ⊆ [V 2 ]. Thus altermagnets
can only appear in σµν
with n = 4 or n = 6 (i.e. with g-wave or i-wave spin
splitting) do not have spin currents generated by electric
fields in the SO-free limit.
We comment on the comparison between our framework and standard techniques at finite SOC using the
black & white groups. One may just as well analyze all
possible couplings at finite SOC; the result would be a potentially longer list of quantities than those listed in Table V. However, this approach would not distinguish between properties arising from altermagnetism, and those
simply arising from finite SOC. Herein lies the primary
benefit of our framework: whereas the properties listed in
Table V highlight only those quantities originating from
ideal altermagnetism in the SO-free limit, our framework
offers a bridge between the SO-free and SO-coupled theories. In addition, this perspective allows one to predict
altermagnetic couplings solely on the basis of the lowest
order pseudoprimary multipole.
There is a growing body of literature examining the
connection between the Néel vector and various physical properties in altermagnets. For example, the anomalous Hall conductivity or magnetization in the pres-

ence of SOC has been explored in works including
Ref. [8, 19, 23, 27, 69–71], among others. Here, we expand upon the previous literature by making a series of
predictions applicable to all symmetry classes of tensors
that may be seen as arising from altermagnetism, and by
providing a coherent framework for understanding how
these couplings arise.

V.

EXAMPLES OF MATERIALS

In the previous sections, we derived a Landau theory of
Q = 0 collinear altermagnets, capitalizing on the philosophy that the SO-free behavior dictates features in a real
material with weak SOC. These Landau theories serve as
a guide for experiments to identify altermagnetic phases.
We have already shown how to put Landau theory to
use through the example of MnTe. In general, based on
the WP of the magnetic ions, we can identify the irrep ΓN
under which N transforms in the SO-free theory. This
data can be found in Table XII. This irrep dictates the
order n of the SO-free (n + 1)-multipolar secondary order
parameter as defined in Eq. 2. Knowledge of this order
n is sufficient to identify physical quantities ξ that may
couple linearly to N when SOC is included. The viable
representation Γξ of ξ is listed in Table II for each n, and
is linked to physical properties in Table V. Finally, predictions of specific non-zero tensor components, as well
as the explicit form of the coupling are found in the final
column of Table XIV.
In the following, we illustrate how to apply these results to further examples of candidate altermagnetic materials and, in the process, make measurable predictions.
We focus on materials appearing in the altermagnetic
literature, such as those appearing in Ref. [15], many of
which also appear in Refs. [55] and [34]. Additionally, we
emphasize that such results, as well as our previous conclusions for MnTe, rely only on the magnetic symmetries
of the material and are therefore independent of the microscopic details of any particular material. In the case
of MnTe, for example, our results apply to apply to any
other 6/mmm material with ΓN = B2g .

A.

Point group 2/m

Among the transition metal fluorides XF2 (X = Cr,
Cu, Mn, F, Co, Ni, V) most are rutiles but two cases
(those with X = Cr and Cu) have a distorted rutile
structure [72] such that the crystal has monoclinic space
group P 21 /c (No. 14), with point group 2/m. The magnetic order is different in these two materials. We focus
on insulating CrF2 in this section, as is it a Q = 0 altermagnetic candidate. CrF2 has a Néel temperature of
roughly TN = 53K [73]. The crystal and magnetic sublattice structure is depicted in Fig. 3. For more details
on the material properties see Refs. [72, 73].

13
Because the two-fold rotation {2010 | 12 12 12 } and mirror
elements {m010 | 12 12 12 } swap sublattices, these elements
are represented by −1 in the irrep ΓN describing the Néel
vector’s spin-orbit free sublattice properties. Further, inversion leaves the sublattice structure invariant, so this
order is inversion-even. This corresponds to the Bg irrep
of 2/m, so ΓN = Bg for CrF2 . This is consistent with the
entry in Table XII corresponding to the 2b WP of space
group 14.
Our next step is to determine the SO-free multipole.
The minimal multipole coupling to N in absence of SOC
has n = 2 according to Table
R XIII, meaning that the multipole’s generic form is d3 r [rµ rν ] m(r). To determine
the polynomial [rµ rν ], one must find the order two polynomial in x, y, and z that transforms as the Bg irrep
of 2/m. Either by explicit checking or by using the procedure outlined in Appendix F, one finds that xy and
yz transform as Bg (matching the entry in Table XIV).
These SO-free multipoles are consistent with a d−wave
spin-splitting pattern in the band structure, matching
predictions in Refs [4, 15].
We are now prepared to find experimentally measurable responses of CrF2 due to altermagnetism when SOC
is included. The n = 2 SO-free multipole tells us that
in the presence of SOC, the Néel vector may couple to
any aeV tensor (according to Table II). Many responses,
listed in Table V, abide by this symmetry. We use the
thermal Hall conductivity (THC), κA as a representative
example.
1
A
Non-zero components κA
i = 2 εijk κjk of the THC couple to components Ni of the Néel vector. Our task is to
determine which κA
i are non-zero, and to which Ni components they couple in the Landau theory. Table VI lists
the irreps under which these components transform.
To this end, we look for components κA
j and Ni that
transform in the same way. Alternatively, we can ask for
the product of thermal Hall and Néel vector components

TABLE VI. Irreps of 2/m describing the transformation properties of the Néel vector components Ni and THC components
κA
i in CuF2 . Recall that N transforms under aeV ⊗ ΓN with
ΓN = Bg , while κA transforms under aeV.
Component i

x

y

z

Ni irrep

Ag

Bg

Ag

σiA irrep

Bg

Ag

Bg

that transform trivially (as Ag ) under the point group
2/m. With the knowledge that Bg squares to the trivial
irrep, we find the following allowed couplings:
A
A
A
κA
y ∼ Nx , κy ∼ Nz , κx ∼ Ny , κz ∼ Ny .

The neutron diffraction study of Ref. [73] reports a
nearly collinear antiferromagnetic structure with zero
propagation vector. A symmetry analysis reveals that
a single primary order parameter would have either moments in the x, z plane or in the y plane. In the study
of Ref. [73], it is noted that the best fit for their data
indicates order in the ac−plane, at an angle of 32◦ from
the c-axis; consistent with ordering in the Ag irrep, and
in this case, a THC signal and weak magnetization would
be expected along the ±y direction.
We note that the same neutron study additionally
reports a possible magnetic structure with moments
aligned and anti-aligned along one of the long Cr–F
bonds [72]. It may therefore be interesting to revisit the
problem of the precise magnetic order in this material.
In any case, one expects a thermal Hall effect in this
A
material either with components κA
x , κz for ordering in
the Bg irrep or, as seems more likely, a κA
y component
coming from order in the Ag irrep. In both cases, weak
ferromagnetism is anticipated.
We further note that the case of CuF2 which has
the same parent (paramagnetic) space group as CrF2
has magnetic order with propagation vector Q =
(1/2, 0, 0) [74] which requires a separate analysis that we
leave for future study.

B.

FIG. 3. The crystal structure of CrF2 with space group symmetry P 21 /c. We use the setting P 1 21 /n 1, related to the
original setting by {a, b, c} → {−a − c, b, a}. Magnetic Cr
ions (red and blue denote magnetic sublattices) reside on the
2b Wyckoff positions, at {0, 0, 0} and { 21 , 21 , 12 } within the unit
cell. The F ions (gray) occupy the Wyckoff positions 4e, at
±{x, y, z}, and ±{x + 21 , 12 − y, z + 21 }, forming a distorted
octahedral environment tilting out of the bc plane.

(7)

Point group mmm

CaCrO3 , LaMnO3 , and La2 CuO4 were proposed as
candidate altermagnetic materials with point group symmetry mmm in Ref. [15], and magneto-optical effect in
LaMO3 (M= Cr, Mn, and Fe) has been reported as early
as Ref. [75]. CaCrO3 and LaMnO3 have space group
symmetry P nma (No. 62), while La2 CuO4 belongs to
the space group symmetry Cmce (or Bmab). For concreteness, we consider La2 CuO4 though our predictions
based on symmetry are equally applicable to LaMnO3
and CaCrO3 .
The compensated magnetic order in insulating
La2 CuO4 has a Néel temperature of TN = 325K, and
is discussed in Ref. [76–83]. The crystal and sublattice

14

FIG. 4. La2 CuO4 structure and magnetic sublattices. The
space group is G = Bmab (No. 64). This setting is related to Cmce by c ↔ −b, and has a pure half-translation
{ 12 , 0, 12 }. Magnetic Cu atoms (red and blue) occupy the 4a
WP {0, 0, 0} and { 21 , 21 , 0}. La atoms (cyan) reside on the 8f
WP ±{x, y, 0}, ±{x + 21 , −y + 21 , 0}. O atoms (grey) occupy
two WP, 8f and 8e, at {x, 41 , 14 }, {x + 21 , 14 , 14 }, {−x, 43 , 34 },
{−x + 12 , 34 , 34 }).

structure is as shown in Fig. 4. We have shown the
crystal structure in the Bmab setting, whereas the irreps and WP in Table XII are derived in the standard
setting (Cmce in this case). Changes between settings
can be achieved using the tools available in the Bilbao
crystallographic server [54].
Group elements {2100 |000}, {1|000} and {m100 |000}
preserve the sublattice structure, while {2001 | 12 12 0},
{2010 | 21 12 0}, {m001 | 12 21 0} and {m010 | 12 12 0} swap the
sublattices.
To find the irrep ΓN describing the
sublattice-swapping properties of N, we assign −1 to
each of the sublattice-swapping elements. We find that
ΓN = B3g in mmm, consistent with our findings in Table XII for space group 64 and the copper WP (4a).
Having found ΓN , our next step is to determine the
order n of the SO-free multipole. From Table XIII, we
find that the minimal multipole has n = 2, and from Ta-

TABLE VII. Irreps of mmm describing the transformation
properties of the Néel vector components Ni and magnetization components Mi in La2 CuO4 . Recall that N transforms
under aeV ⊗ ΓN , while M transforms under aeV.
Component i

x

y

z

Ni irrep

Ag

B1g

B2g

Mi irrep

B3g

B2g

B1g

ble
R 3XIV we can see that this multipole is of the form
d r yz m(r). This is consistent with a d-wave spinsplitting pattern, aligning with the ab initio prediction
in Ref. [15].
We are now prepared to determine the spin-orbit coupled theory. For n = 2 multipoles, any aeV tensor has
components that couple linearly to N (see Table II).
Physical properties of this type include weak ferromagnetism M, among others listed in Table V. We use the
magnetization as a representative example. The components of N and of M transform according to the irreps
of mmm listed in Table VII.
By virtue of the 1D irreps squaring to the trivial irrep,
My can couple to Nz , and Mz can couple to Ny . As a
consequence, the y and z components of the magnetization, and any relevant aeV tensor, may generically be
nonzero in La2 CuO4 .
Experimentally, in Refs. [80] and [77] it was found that
the moments align along the crystallographic b-axis, corresponding with our Cartesian y-axis. For this reason, we
also expect a weak ferromagnetic component Mz along
the c-axis, consistent with the predictions and measurements of Refs. [82, 83]. Theoretical and experimental
aspects of La2 CuO4 are reviewed in [79].

C.

Point group 4/mmm

Three candidate altermagnetic materials with point
group symmetry 4/mmm are suggested in Ref. [15]:
MnF2 , MnO2 , RuO2 . We concentrate on the insulator
MnF2 , whose crystal structure [84, 85] is shown in Fig. 5,
to illustrate this class of examples.
The onset of antiferromagnetic ordering in MnF2 occurs at roughly TN = 67 K [86]. We begin our analysis by determining the sublattice preserving and sublattice swapping elements of the space group P 42 /mnm
(No. 136) [24, 84, 85]. The non-symmorphic elements {4001 | 21 12 21 }, {2100 | 12 21 12 }, {2010 | 21 21 12 } swap up- and
down-spin sublattices, while the symmorphic {I|000},
{2110 |000} and {2110 |000} preserve the sublattice structure. By ascribing the non-symmorphic elements with
the representation −1, we can identify the irrep ΓN for
MnF2 as B2g . This matches the finding for magnetic ions
at WP 2a in Table XII.
Next, we develop the SO-free Landau theory by identifying the lowest order n multipole coupling to the Néel
vector. From Table XIII we see that n = 2, and using Table
XIV we find that the multipole is of the
R
form d3 xy m(r). The xy integrand indicates a d-wave
spin-splitting pattern, consistent with the predictions in
Refs. [15] and [24]. Ab initio studies on MnF2 may be
found in Refs. [87] and [88].
As in our previous examples, the presence of an n = 2
multipole in the SO-free theory dictates that when SOC
is included, components of N may couple to an aeV tensor (see Table II). We will use the magnetization M as
an example, though other quantities may be found in Ta-

15
ble V. The irreps under which components of N and M
transform are provided in Table VIII. No linear coupling
is allowed with Nz and Mz , while we may use the procedure outlined in Appendix F to determine that the xand y-components may couple as
Nx M x − Ny M y ,

(8)

where Ni and Mi components correspond to the choice
of crystallographic axes depicted in Fig. 5. If the crystallographic axes are chosen to point in the directions
a′ = a + b, b′ = a − b and c′ = c (which corresponds
to the setting in Bilbao [89]), then the coupling is of the
form
Nx′ My′ + Ny′ Mx′ ,
(9)
which matches the entry for the B2g irrep of 4/mmm
in Table XIV, as well as the reported coupling in [19].
As a consequence of this coupling, a weak ferromagnetic
moment may develop in the crystallographic ab-plane.
Recalling that the thermal Hall conductivity κA transforms identically to the magnetization M, we see that
this result also implies generically non-zero allowed valA
ues of κA
x and κy , consistent with the theoretical results
of Ref. [25] examining thermal transport at zero field via
magnons in insulating rutile systems. Indeed, they find
that when N is aligned with the crystallographic c-axis,
A
κA
x and κy are zero while any canting gives rise to a nonzero value of these thermal conductivities.
It has been experimentally determined in Ref. [90] that
antiferromagnetic order in MnF2 is aligned along the

FIG. 5. The crystal and magnetic sublattice structure of
MnF2 , with space group P 42 /mnm (No. 136). Mn atoms
(red and blue denote magnetic sublattices) reside on the 2a
WP {0, 0, 0} and { 21 , 12 , 12 }, while F atoms (grey) occupy the
4f WP with positions ±{x, x, 0} and ±{−x + 21 , x + 12 , 12 }.

TABLE VIII. Irreps of 4/mmm describing the transformation properties of the Néel vector components Ni and magnetization components Mi in MnF2 . Recall that N transforms
under aeV ⊗ ΓN , while M transforms under aeV.
Component i

x

y

z

Ni irrep

Eg

Eg

B1g

Mi irrep

Eg

Eg

A2g

crystallographic c-axis, corresponding to a dominant Nz2
term in the free energy. This is likely due to the magnetostatic dipolar coupling. This coupling, while significantly
smaller than the exchange scale, pins the moments along
c and gaps out the magnon spectrum [91].
We note additionally that altermagnetic band structure in rutiles has been studied using spin-groups in
Ref. [50] where distinctive degeneracies of the band structure at zero SOC are discussed. The spin splitting and
momentum-space spin texture have been studied using
DFT in Ref. [24].

D.

Point group 3m

In the point group 3m, it has been suggested that the
insulating collinear antiferromagnetic state of hematite
Fe2 O3 below the Morin temperature TM = 265K [92] is
altermagnetic [15]. Magnetism in hematite has been a
longstanding and ongoing topic of research [93–98]. Proposed altermagnetic features of hematite have been investigated in Ref. [99], and recently, chiral splitting of
magnons in hematite has been investigated [100]. Here,
we develop the SO-free and SOC Landau theories for
hematite and compare them with known material properties.
To begin, we determine the irrep ΓN under which the
Néel vector transforms in the SO-free limit. The crystal
and magnetic sublattice structure for hematite is shown
in Fig. 6. This structure has the symmetry of space
group R3c (No. 167). The threefold element {3001 |000}
and inversion {I|000} preserve the sublattice structure,
while all three non-symmorphic two-fold axes {2100 |00 12 },
{2010 |00 21 } and {2110 |00 12 } (and corresponding mirrors)
swap the sublattices. Assigning −1 to the sublattice
swapping elements, we may deduce that the Néel vector transforms under ΓN = A2g , matching the entry for
magnetic ions at the 12c WP of space group 167 in Table XII.
We now seek the secondary multipolar order parameter
in the SO-free limit. From Table XIII we see that the
minimal multipole in 3m with ΓN = A2g has order n = 4,
and in
R Table XIV we see that this multipole is of the
form d3 r y(y 2 − 3x2 )z m(r). An SO-free multipole with
n = 4 corresponds to a g−wave spin-splitting pattern,
matching the pattern predicted in Refs. [15] and [4].
When SOC is included, we would expect an altermagnetic Néel vector in hematite to couple with tensors
transforming as aeV [V 2 ], on the basis of the order n = 4
of the SO-free multipole and Table II. Many physical
properties, listed in Table V obey this transformation
law; here, we will use the piezomagnetic tensor Λijk as
an illustrative example, where indices j and k are polar
and symmetrized, corresponding to components of the
strain tensor, while the i index denotes the magnetic axial component. The transformation properties of the Néel
components Ni and of Λijk are shown in Table IX. Both
couplings in the A1g irrep from Table IX are allowed. For

16

FIG. 6.
The crystal and magnetic sublattice struc167) in
ture of Fe2 O3 , with space group R3c (No.
the hexagonal setting.
Fe atoms (red and blue denote magnetic sublattices) reside on the 12c WP
{0, 0, z}, {0, 0, 12 − z}, {0, 0, −z}, and {0, 0, 21 + z}, while
O atoms (grey) occupy the 18e WP with positions
{x, 0, 14 }, {0, x, 14 }, {−x, −x, 41 }, {−x, 0, 43 }, {0, −x, 34 },
and
{x, x, 34 }. Note that the hexagonal setting has pure lattice
translations { 32 , 13 , 13 } and { 13 , 23 , 23 }.

TABLE IX. Transformation properties of the piezomagnetic
tensor Λijk and Néel vector Ni components in 3m, for Fe2 O3 .
Irrep.

Néel component

A1g

Nz

Piezomagnetic tensor
component
2Λxxy + Λyxx − Λyyy
Λyxz − Λxyz


−Λyzz

 Λxzz 

Eg

Nx
Ny

!

Λzzy
−Λzzx

Λxyz +Λyxz
Λxxz −Λyyz


4Λzxy
Λzxx −Λzyy


−2Λxxy +Λyxx
2Λyyx −Λxyy


Λxxy +Λyyy
−Λxxx −Λyyx



each of the six Eg irreps, one specific coupling between
(Nx , Ny ) and the Λijk is allowed. We have expressed
the twelve basis linear combinations such that their dot
product with the in-plane Néel components gives rise to
the allowed coupling.
These results may be derived using the method outlined in Appendix F, and are consistent with the listing
in Table XIV for 3m and irrep ΓN = A2g . As an example of the correspondence with Table XIV we consider
the last SOC coupling for 3m,
z 2 (Ny Rx − Nx Ry ) = Ny Rx z 2 − Nx Ry z 2 ,
which corresponds to a coupling of the form −Nx Λyzz +
Ny Λxzz . This is precisely the coupling we find from the
last Eg pair in Table IX.
Below the Morin transition, the magnetic order in
hematite has been measured to be collinear and com-

pensated, with the Néel vector pointing along the crystallographic c−axis [92, 95, 99]. This implies that only
the components of the piezomagnetic tensor appearing in
the A1g irrep are non-zero, corresponding to the strain
applied in the xy-plane.
The absence of magnetization below the Morin temperature [92, 95, 99] may also be understood on the basis of our results. We begin by noticing that aeV tensor
coupling is not guaranteed by the SO-free Landau theory
with n = 4 multipolar order, as can be seen from Table V.
Nevertheless, this does not reflect that coupling to aeV
quantities forbidden. The symmetry allowed form of the
coupling between the Néel vector and the magnetization
M is Nx My − Ny Mx . Since Nx and Ny are zero below
the Morin temperature, no linear coupling to the magnetization exists. Thus, we can conclude that Mx and My
vanish. The z-component of magnetization transforms as
A2g , and so it cannot couple to any Ni , implying that it
also vanishes.

VI.

DISCUSSION

Landau theory has rightly been central to condensed
matter physics since its inception; it supplies a unifying
framework for all symmetry-broken states of matter and,
as we have seen, it can be adapted to provide insights
on altermagnets as well. One distinctive feature of altermagnets is that they are most cleanly defined in the
limit of zero spin-orbit coupling. Nevertheless, materials
tend to have finite SOC and therefore one is interested in
those properties of altermagnets that are inherited from
the ideal limit. For these reasons, in this paper, we have
taken the dual approach of analyzing Landau theories at
both zero and finite SOC.
We began by specifying a simple criterion for determining altermagnetism in the ideal limit, in terms of the
transformation properties of the Néel vector. This rule
allows one to determine all magnetocrystalline symmetries compatible with altermagnetism, and to tabulate all
altermagnets from their space group, Wyckoff position,
and magnetic structure in the case where the magnetic
order does not enlarge the magnetic unit cell (which covers almost all cases considered to date).
Although the set of possible altermagnetic structures
is large, the Landau theories depend only on the (1D)
irrep of the crystal point group. This leads to a much
more manageable set of 54 possible Landau theories. For
these theories, we have determined the leading multipole
that couples to the Néel vector. This directly reveals the
pattern of spin splittings in the band structures in the
zero SOC limit. This work therefore supplies a classification of altermagnets based on symmetry alone and the
resulting Landau theories are tied to various observable
properties even in the ideal limit.
Turning to the realistic finite SOC limit, we have established a further criterion that ties the appearance of
the minimal allowed multipole in the zero SOC to lin-

17
ear couplings between the primary antiferromagnetic order parameter and a given response function. In other
words, we have made precise the notion that certain features of altermagnets at finite SOC are inherited from the
ideal limit and tabulated these features across all possible
Q = 0 altermagnetic orders.
To illustrate all of these ideas we have shown how to
identify altermagnetism given a magnetic structure in a
crystal and then establish its basic properties both including and stemming from the spin splitting in momentum space. Spin splitting on its own is directly measureable using (spin-polarized) ARPES. However, the
value of the symmetry analysis is that one can directly
compute symmetry-allowed components of electronic and
spintronic responses coupling spin, charge, and heat. We
have exemplified how to make experimentally relevant
predictions based on the symmetry analysis presented for
a number of different altermagnetic candidate materials.
Having determined the Landau theories describing altermagnets whose crystal and magnetic unit cells coincide, some questions for future investigation remain. A
natural extension of this work would consider the Q ̸= 0
“supercell” altermagnets introduced in Ref. [51]. In this
case, altermagnets may arise even in structures whose
point group is one of the six forbidden Q = 0 point
groups.
Further, the nature of non-centrosymmetric altermagnets has received limited attention [101]. Due to
the emergent inversion-symmetry of the band structure, there is a discrepancy between the lowest order allowed SO-free multipolar order parameter and the spinsplitting pattern in reciprocal space. It may be worth exploring different properties that would inherit the lowestorder multipolar symmetry.
Finally, the list of tensors corresponding to physical
properties used in this work is far from exhaustive. Future studies may seek to expand the present symmetry
analysis to other experimentally relevant features of altermagnetic systems.

ACKNOWLEDGMENTS

H.S. and J.R. were supported by the NSF through
grant DMR-2142554. Work at the University of Windsor
(J.G.R.) was funded by the Natural Sciences and Engineering Research Council of Canada (NSERC) (Funding
Reference No. RGPIN-2020-04970). P.M. acknowledges
funding from the CNRS.

The symmetry groups of ideal altermagnetic phases correspond to spin groups [4, 15]. Spin point groups describing SO-free cases are subgroups of Os (3) × O(3),
where Os (3) and O(3) contain the proper and improper
rotations in spin space (Rs ) and real space (Rl ), respectively [42, 49]. The improper rotations in spin space contain the time-reversal operator (spin-inversion), τ , and
the improper rotations in real space include the inversion
element, I. Group elements of Os (3) × O(3) are usually
written as [Rs ∥Rl ], where the first element acts on spin
and the second on lattice degrees of freedom [42, 49, 50].
When SOC is zero, the spin point group can be written
as b × S, where the spin-only group, b, describes symmetries dictated by mutual spin orientations (collinear,
coplanar, and non-collinear non-coplanar), and S is one
of the 598 non-trivial spin point groups [42, 49, 50].
There are 58 spin point groups describing collinear
antiferromagnetic spin arrangements, corresponding to
b∞ × S, with
b∞ = [SO(2)∥E] ⋊ { [E∥E], [τ 2⊥n ∥E] } and
S = [E∥H] + [τ ∥a][E∥H] ,

(A1)
(A2)

where [SO(2)∥E] is the group of spin-only rotations
about the shared spin axis n, and 2⊥n is a π−rotation
about an axis perpendicular to the spin axis. H is a standard crystallographic point group and the group H + aH
is isomorphic to F, the point group of the underlying
crystal structure [42, 49, 50].
The elements in the coset H preserve the sublattices,
while the elements in aH swap them. Thus the group element a must be paired with time-reversal τ in the spin
point group b∞ × S (see Eq. (A2)), so that the coset
[τ ∥a][E∥H] leaves the antiferromagnetic arrangement invariant.
The Néel vector describing an altermagnetic order
must be inversion-even. This constraint means that S
cannot contain the group element [τ ∥I], disqualifying 21
of the 58 possible spin groups corresponding to collinear
antiferromagnetism. These include any spin group based
2
on F = 1, 3, and m
3. These symmetry considerations
result in 37 spin point groups that are compatible with
altermagnetism.
It is possible to avoid complications associated with
the spin groups for collinear altermagnets as the Landau
theory is based on long-range order developing out of the
paramagnetic phase. Using the representation theory of
the SO-free paramagnetic group6 , the altermagnetic order parameter, N, does not belong to the fully symmetrical trivial irrep but instead transforms as a nontrivial
irrep. This nontrivial representation of the paramagnetic

Appendix A: Circumventing Spin Groups

In the Landau theory, conventionally, one uses the
symmetry group of the ordered phase, in which the
(primary and secondary) order parameters transform as
the fully symmetrical (trivial) irreducible representation.

6 When referring to groups containing antiunitary time-reversal,

the correct terminology is a “co-representation.” In these appendices, we use use representation and co-representation interchangeably, as antiunitarity is apparent from the group.

18
group becomes the trivial one if we restrict the group elements of the paramagnetic point group to those of the
spin point group corresponding to the order.
The advantage of the SO-free paramagnetic group is
that it can be written as a direct product of spin-only
and lattice-only transformations. The spin-only group
is Os (3), containing the proper and improper spin rotations and the lattice-only transformations encompass
the space group of the crystal, with point group F. Because of the constraint that N transforms trivially under
translations, it is sufficient to consider the properties of
N under the spin point group Os (3) × F, describing the
SO-free paramagnetic phase.
The Néel vector N transforms as a nontrivial irrep of
Os (3) × F, which can be expressed as a direct product
of the irreps of Os (3) and F. This is a non-trivial fact;
the co-irreps of direct product groups containing timereversal (or any antiunitary element) are generally not
tensor products of the groups that are multiplied. In
Appendix B we give a detailed argument as to why the
irreps can be written in such tensor-product form here.
Similar to the irreps of SO(3), the irreps of Os (3) are
labelled by angular momentum integers l ∈ N+ . Because
N is the three-component staggered magnetization, in
spin-space N transforms like a vector (l = 1) that is odd
under time-reversal symmetry. Furthermore, following
the main text notation, N transforms as the ΓN irreducible representation of the point group F. Altogether,
the Néel vector belongs to the Γl=1 ⊗ ΓN irrep of the
SO-free paramagnetic group Os (3) × F.
We will now show that there is a one-to-one correspondence between the spin point groups and the
non-trivial irreducible representations of crystallographic
point groups, with Γsl=1 ⊗ ΓN irrep reducing to the trivial
irrep of the true spin group of the ordered phase. This
correspondence allows us to derive the Landau theory of
altermagnets starting from the paramagnetic phase, using the irreps of Os (3) × F, and avoid using spin groups
altogether. This approach provides a conceptual simplification in the study of altermagnetism.
To encode a bipartite sublattice structure (necessary
for collinear antiferromagnetism), F must have a onedimensional real irreducible representation where the elements of H are represented by 1 and the elements of
aH are represented by −1. Three point groups, 1, 3, and
23, are immediately eliminated because they do not have
any nontrivial real one-dimensional irreducible representations. Consequently, there are no collinear antiferromagnetic spin point groups based on any of these three
point groups.
To encode the inversion-even criterion of altermagnetism, when F contains the inversion element I, i.e. F
is centrosymmetric, there must be at least one nontrivial one-dimensional real irreducible representation that is
also inversion even [19]. This condition disqualifies three
2
additional point groups: 1, 3, and m
3, as these do not
have any non-trivial one-dimensional real irreps that are
even under inversion.

Altogether, we have 26 remaining point groups F that
are compatible with altermagnetism. The question is
whether there is a correspondence between these point
groups and the 37 collinear spin point groups that can
describe altermagnetism. The answer is affirmative: the
non-trivial inversion-even one-dimensional real irreps of
the viable 26 point groups F are – up to relabelling coordinate axes – in a one-to-one correspondence with the
remaining nontrivial spin point groups S. We show this
correspondence in Table X.
We demonstrate the correspondence between the ΓN
irreps and the spin point groups on the example of point
group 4mm. There are two collinear spin groups corresponding to antiferromagnetic arrangements that can
be derived from 4mm: 1 41 m1 m = 1 4 + [τ ∥mx ]1 4, and
1 1 1
4 m m = 1 m1 m1 2 + [τ ∥4]1 m1 m1 2. In this notation
g
f indicates that the point group generator f appears
with spin-space element g, i.e. [g∥f ] is one of the generators of the spin point group [42]. The 1 superscript
indicates that the spin-space element is the time-reversal
operator, τ . The point group 4mm has three non-trivial,
one-dimensional irreps (inversion is not present in this
group): A2 , B1 , and B2 .
The irrep A2 of 4mm assigns 1 to the π2 and π rotations
about the z−axis, and −1 to the four reflections. This irrep is in direct correspondence with the spin point group
1 1 1
4 m m, where the mirrors are paired with time-reversal
τ.
The B1 and B2 irreps of 4mm assign 1 to the π rotation about the z− axis as well as two of the four mirrors,
while the four-fold rotations and remaining two mirrors
are assigned −1. To establish a connection to a spin
point group, the four elements represented by −1 in the
point group need to be composed with τ in the spin point
group. The two spin point groups obtained in this way
are conjugate to each other in Os3 × O3 and so they correspond to the same (class of) spin point groups [42, 50],
1 1 1
4 m m. The equivalence of these groups effectively
amounts to a relabelling of the x−axis to the axis at
an angle of 45◦ between the x− and the y−axes. Any
collinear antiferromagnet whose Néel vector transforms
under the A2 irrep of 4mm will have spin group symmetry given by 1 41 m1 m, whereas if N transforms under B2
or B3 of 4mm it will have spin point group symmetry
given by 1 41 m1 m, with appropriately chosen axes.
Another class of examples that clarifies this correspondence are the non-centrosymmetric point groups with
only one associated (collinear antiferromagnetic) spin
point group. These are 2, m, 222, 4, 4, 32, 3m, 6,
6, 43m, and 432. Aside from 222, each of these point
groups only has one non-trivial real one-dimensional irrep. This is precisely why they only have one corresponding (collinear antiferromagnetic) spin point group. In the
case of 222, there are three valid irreducible representations, but they give rise to spin point groups that are
conjugates in Os3 × O3 .
The one-to-one correspondence between the ΓN irreps

19
TABLE X. Point groups F that are compatible with altermagnetism and the nontrivial one-dimensional real inversion-even
irreps of N in them. The irreps inside the curly brackets are
identical up to axes relabelling. The last column contains the
nontrivial spin group that corresponds to the altermagnetic
order described by the ΓN irrep of the paramagnetic point
group.
F

ΓN

2

B

corresponding S
1

m

′′

A

1

2/m

Bg

1

1 + [τ ∥2] 1 1

222

{B1 , B2 , B3 }

1

2 + [τ ∥2] 1 2

mmm

{B1g , B2g , B3g }

1

1 + [τ ∥2] 1 1

1 + [τ ∥m] 1 1

2z /1 mz + [τ ∥2x ] 1 2z /1 mz

B

1

2 + [τ ∥4] 1 2

4

B

1

2 + [τ ∥4] 1 2

4/m

Bg

4

1

2/1 m + [τ ∥4] 1 2/1 m

A2

1

A2

1

3 + [τ ∥m] 1 3

3m

A2g

1

3 + [τ ∥m] 1 3

6

B

1

3 + [τ ∥6] 1 3

6

A′′

1

3 + [τ ∥6] 1 3

6/m

Bg

1

3 + [τ ∥6] 1 3

m3m

A2g

432

A2

1 1

A2

1 1

32
3m

43m
mm2
422
4mm
4/mmm
622
6mm
6/mmm
42m
(and 4m2)

2 3 + [τ ∥4] 1 21 3

2 3 + [τ ∥4] 1 21 3
1

{B1 , B2 }

1

2 + [τ ∥m] 1 2

m + [τ ∥2] 1 m

1

A2

4 + [τ ∥2x ] 1 4

1 1 1

{B1 , B2 }

1

{B1 , B2 }

1

A2g

1
1

4 + [τ ∥mx ] 1 4

m1 m1 2 + [τ ∥4] 1 m1 m1 2
4/1 m + [τ ∥mx ] 1 4/1 m

m1 m1 m + [τ ∥4] 1 m1 m1 m

A2

1

{B1 , B2 }

1 1
1

{B1 , B2 }

1 1

A2g

6 + [τ ∥2x ] 1 6

3 2 + [τ ∥6] 1 31 2

A2

6 + [τ ∥mx ] 1 6

3 m + [τ ∥6] 1 31 m

1

6/1 m + [τ ∥mx ] 1 6/1 m
1 1

3 m + [τ ∥6] 1 31 m

{B1g , B2g }
A2

1

B1

1 1 1

4 + [τ ∥2x ] 1 4

2 2 2 + [τ ∥4] 1 21 21 2

1

m1 m1 2 + [τ ∥4] 1 m1 m1 2

A′2

1

A′′1
A′′2

1 1

6 + [τ ∥mx ] 1 6

3 2 + [τ ∥6] 1 31 2

1 1

Appendix B: Direct product representations of the
SOC-free paramagnetic group

In this section, we clarify the argument that for quantities we are interested in, representations of the SO-free
paramagnetic group Os (3) × F can be expressed as the
direct product of representations of Os (3) and representations of F, where Os (3) ∼
= SO(3) + τ SO(3) and F is a
crystallographic point group.
The crucial point is that we are only interested in quantities whose real-space transformation properties are described by real representations of F, denoted by Γ(ν) .
The SO-free paramagnetic group can be expressed in
a coset decomposition of its unitary halving subgroup:
Os (3) × F = (SO(3) × F) + τ (SO(3) × F) .

(B1)

1 1 1

2 2 2 + [τ ∥4] 2 2 2

A2

{B1g , B2g }

3 + [τ ∥2] 3

2/1 m 3 + [τ ∥4] 1 2/1 m 3

A2

B2
6m2
(and 62m)

1

1

of the paramagnetic point group F and the possible altermagnetic spin point groups enables the derivation of
Landau theory using F. Based on symmetry arguments,
we ruled out six point groups that cannot support altermagnetic phases. The six nonviable point groups belong
to 20 space groups, therefore, we expect 210 out of 230
space groups to have at least one Wyckoff position that
can support altermagnetism. This is consistent with our
results shown in Appendix H.
We note that while we may avoid the use of spin groups
in the Landau theory, the representation theory of spin
groups becomes essential when discussing certain symmetry properties in the ordered phase − for example band
degeneracies − and phase transitions from the altermagnetic phase.

3 m + [τ ∥6] 1 31 m

The co-irreps of Os (3)×F will be induced from the irreps
of SO(3) × F, ∆(l) ⊗ Γ(ν) , where l ∈ N+ labels the irreps
of SO(3) and ν labels the irreps of F. The induction
scheme for each irrep depends on its reality because the
coset representative is simply τ , and so Dimmock’s test
reduces to the Frobenius-Schur indicator [50, 102–105].
Since ∆(l) are all real, the induction scheme depends
only on the reality of the point group irrep Γ(ν) . When
the irrep Γ(ν) is real, an element [aR∥f ] of this group
(where R ∈ SO(3), f ∈ F, and a is either the identity element or time-reversal τ ) can be chosen to be represented in the co-irrep by (−1)π(a) ∆(l) (R) × Γ(ν) (f ),
where π(E) = 0, and π(τ ) = 1. This choice of π(a)
corresponds to time-reversal inverting spins. Notice that
(−1)π(a) ∆(l) (R) corresponds to the “polar” l co-irrep of
Os (3), where τ corresponds to inversion element and is
represented by a scalar matrix −1 of appropriate dimen(s)
sion. These are the Γl irreps referred to in Ref. [19].
We have shown here that for real point group irreps,
the co-irrep of the SO-free paramagnetic group is simply
(s)
expressed as the direct product of the Γl co-irrep of
s
(ν)
O (3) and the point group irrep Γ .
We emphasize that without SOC, the irreducible representation of F describing real-space transformation properties of the Néel vector must be real, and so the co-irrep

20
of the SOC-free paramagnetic point group will be of the
direct-product form above.
We are also interested in the representations under
which the multipoles transform. We will now demonstrate that the representations describing SO-free multipoles can also be expressed in direct-product form.
A multipole’s real-space transformation properties under F L
are given by a generically reducible representation
(ν)
D =
, where the irreps with non-zero multiν aν Γ
plicity aν ̸= 0 are real irreps of F. In fact, this may be
chosen by using only the “physically irreducible” representations of the point groups [106], which are the irreps
allowed over R as opposed to C, and are appropriate for
a tensor constructed out of real-space coordinates. A
multipole’s spin-space transformation properties will be
L
(s)
given by a reducible (real) representation ∆ = l bl Γl
s
of O (3).
The direct product representation of Os (3) × F given
by ∆ ⊗ D can then be expressed as
!
!
M
M
(s)
(ν)
∆⊗D =
bl Γl
⊗
aν Γ
=

l

ν

M

(s)
bl aν Γl ⊗ Γ(ν) .

(B2)

l,ν
(s)

Due to the reality of Γsl and Γ(ν) , Γl ⊗ Γ(ν) are coirreps of Os (3) × F, and we have found the co-irrep decomposition of ∆ ⊗ D.
Formally, our claim that we can use direct product
representations of Os (3) × F for quantities we are interested in reduces to the fact that we only need coirreps falling into case (a) of Wigner’s co-irrep classification scheme [50, 102–105], as these are the co-irreps
appearing in the decompositions of any multipole’s representation. These case (a) co-irreps can be expressed as
a direct product of Os (3) co-irreps and F irreps.

Appendix C: Altermagnetic Structures Algorithm:
Technical Details

In this section, we outline an algorithm for identifying all crystal structures capable of supporting (Q = 0)
altermagnetism. This means that we can identify the
Wyckoff positions in each space group G whose sublattices satisfy the symmetry constraints outlined in Sec. II:
the spin sublattices, and consequently the Néel vector N
(both in absence of spin-orbit coupling) transform under a 1D, real irrep of the crystal point group F, that is
inversion-even in centrosymmetric cases. These Wyckoff
positions are candidates for positions of magnetic ions in
an altermagnet. The results of this algorithm are summarized in Tables I and XII. The Wyckoff positions and
space group elements used in our algorithm were obtained
from the Bilbao Crystallographic Server [54].
By selecting a Wyckoff position w
⃗ and acting on it
with all transformations of the space group, a lattice is

generated; in one unit cell, there will be nw⃗ atoms. For
these nw⃗ atoms to be compatible with altermagnetism,
it must be possible to place ‘up’ and ‘down’ spins on
each site, implying that the multiplicity nw⃗ must be even.
The symmetry constraints of altermagnetism described
in Sec. II dictate that these two sublattices must not be
mapped into one another by pure spatial translation or
inversion.
When we ask how the sublattices are mapped into one
another under lattice transformations, we are examining
the permutation action of the space group on the atoms.
Then naturally we are concerned with the permutation
representation of the space group on the lattice.
The group elements of G can be expressed in WignerSeitz notation as [f |t⃗], where f ∈ F is some O(3)
matrix, and t⃗ is a three-dimensional translation vector7 [104, 105]. This group element transforms the
atomic position ⃗r to f⃗r + ⃗t.
There is a great deal of redundancy in the action of
G on our lattice. Without any loss of information, we
may restrict our attention to the action of G on the nw⃗
atoms within a single unit cell, by treating every element
of G modulo translations. This means that we identify as
equivalent all elements [f |t⃗] with t⃗ vectors of the form t⃗ =
q⃗ + n1⃗a1 + n2⃗a2 + n3⃗a3 for {⃗ai |i ∈ {1, 2, 3}} representing
the primitive lattice vectors, ni ∈ Z, i ∈ {1, 2, 3} and
|⃗q| < |⃗ai |. The group composition is also treated modulo
this equivalence relation. This has the effect of reducing
the space group G to the quotient group F̃ = G/T(3)
where T(3) is the Abelian group of translations of the
lattice. This quotient group F̃ is isomorphic to the point
group F of the lattice, and it is this group F̃ for which
we would like to construct a permutation representation.
Each element [f |⃗q] ∈ F̃ will send an atom w
⃗ i within the
unit cell to another atom w
⃗ j within the unit cell. The
permutation representation ∆(f ) of this element will be
given by ∆(f )w
⃗i = w
⃗ j , resulting in a nw⃗ × nw⃗ matrix
whose i−th row contains exactly one 1 in the j−th column.
Let ΓN,α denote irreps of F ∼
= F̃ that satisfy the altermagnetic constraints. There may be several such irreps
in F and we index these by α. The Wyckoff position w
⃗
is compatible with altermagnetism if and only if the permutation representation ∆(F̃) contains any of the irreps
ΓN,α . This condition is easily checked by taking the inner
product of the characters χ(∆) = { Tr(∆(f )) | [f |⃗q] ∈ F̃}
of the permutation representation with the characters
ΓN,α (f ) of ΓN,α 8 [104, 105, 107]:
aΓN,α = (χ(∆), ΓN,α ) =

1 X
|F̃|

ΓN,α (f )χ(∆(f )).

f ∈F̃

7 the single vertical bar distinguishes space group elements from

the more general spin group notation
8 Because Γ
N,α is one-dimensional, the representation is equal to

its characters.

21
If the natural number aΓN,α ̸= 0, then this Wyckoff position w
⃗ can support an altermagnetic order with sublattice transformation properties dictated by the irrep ΓN,α .
The result of applying this algorithm to all Wyckoff positions in all 230 space groups are summarized in table
XII.
This technique can be adapted to study structures supporting any magnetic order of interest, so long as translational symmetry is preserved (i.e. translations act trivially on the level of permutations within the unit cell).
The extension of this technique to structures with an
enlarged magnetic unit cell is relatively straightforward,
but irrelevant to collinear altermagnets: the procedure is
modified only by the choice of translational group with
which G is quotiented.

Appendix D: Consistency of SOC Landau Theory
with Magnetic Symmetry Analysis

In Appendix A we demonstrated that the SO-free Landau theory derived in Sec. III is justified; all conclusions
based on our analysis with ordinary point groups are consistent with a Landau theory using a spin point group in
the ordered phase. Here, we provide the sibling argument
for the spin-orbit coupled Landau theory. This scenario is
more involved from the perspective of symmetries, than
the SO-free case.
In Sec. IV, we formulate Landau theories for altermagnets when SOC is included. By turning on spin-orbit coupling, we implicitly lock the spins to the lattice, making
it impossible to transform lattice and spin degrees of freedom separately. This reduces the symmetry of the paramagnetic phase to a so-called grey group. When assuming
translations act trivially, the spin-orbit coupled paramagnetic group is F + τ F, with F being the crystallographic
point group and τ being time-reversal. With SOC, in
passing from the high symmetry paramagnetic phase to
the collinear altermagnetic phase, the symmetry is reduced to a black & white magnetic group [105, 108, 109].
In the presence of SOC, each component of the Néel
vector may, in principle, transform under different irreps
of the paramagnetic grey group. Recall that the spinorbit coupled Néel vector N transforms as aeV ⊗ ΓN .
For each point group relevant to altermagnets, this representation decomposes into three one dimensional irreps,
one 1D and one 2D irrep, or a singular 3D irrep. Having
multiple order parameters, and having order parameters
whose irreps are larger than 1D makes the SOC Landau
theory slightly more subtle than in the SO-free case. A
one-to-one correspondence between the ordered symmetry group and the paramagnetic co-irrep is not guaranteed when SOC is included, due to the more complicated
nature of the order parameters.
Without this one-to-one correspondence, it may be
useful to remind the reader that there are two equivalent ways of formulating Landau theories. The (direct)
Landau problem is concerned with determining the possi-

ble symmetry groups of the ordered phase, given the high
symmetry phase’s group and the irrep under which the
order parameter transforms. The inverse Landau problem starts with known high and low symmetry groups
and asks which order parameters are possible. We have
seen that in the SO-free case, both problems are exactly
identical, not just equivalent [104]. In the spin-orbit coupled case they are not identical, and this fact has been the
root cause for decades of debate between the “representation analysis” approach and the “magnetic space group”
approach to understanding magnetic structures [110].
This being said, we take the approach of the direct
Landau problem. Each component Ni of the Néel vector transforms under an irrep of the paramagnetic group.
Necessarily, there will be at least one element that leaves
each component invariant. The intersection of these elements for all three components gives the black & white
point group corresponding to all components Ni being
non-zero.
Whether or not all three Ni are non-zero in a given
material, however, is not a question of symmetry: it
is a question of the microscopic theory governing the
magnetic interactions. With any Ni being zero, the
resulting black & white symmetry groups of the possible orders may be larger. In this way, we can see
that several black-and-white point groups may be identified with one paramagnetic (generically reducible) corepresentation describing the ordered phase.
With this in mind, we may now proceed in justifying
our use of ordinary point groups to determine the spinorbit coupled Landau theory. To do so, we must first
establish the co-irrep theory for the grey paramagnetic
groups, and demonstrate that the co-irreps under which
N transforms are completely determined by the decomposition of aeV ⊗ ΓN .
The co-irreps for grey point groups F + τ F are generated (induced) from each irrep Γ(ν) of F. The induction algorithm [102, 103, 105] depends on the reality of
the Γ(ν) . Following the classification in Ref. [105], all irreps of the crystallographic point groups are of the first
kind (real), except those with complex characters, which
are of the third kind (complex). The co-irreps arising
from real Γ(ν) are simple: we may choose that τ is represented by −IdimΓ(ν) (where IdimΓ(ν) is the identity matrix
of dimension equal to that of Γ(ν) )9 , physically corresponding to time-reversal inverting magnetic moments.
This choice completely determines the irrep of the paramagnetic group, and no information is lost in derivations
relying solely on the knowledge of Γ(ν) .
For the complex irreps Γ(ν) of F, the corresponding
co-irrep of F + τ F is doubled. The elements of F are

9 Formally, this choice corresponds to the single-valued co-irreps,

which are appropriate for integer angular momentum. A full
theory for half-integer angular momentum would use the doublevalued co-irreps.

22
represented by matrices
"
#
Γ(ν) (f )
0
,
0
Γ(ν)∗(f )

TABLE XI. Full co-irreps of 2/m + τ 2/m corresponding to
the point group irreps Ag and Bg .

(D1)

while the time-reversal element τ , which satisfies τ 2 = E,
may be represented by
"
#
0
−IdimΓ(ν)
.
(D2)
−IdimΓ(ν)
0
The equivalence of two co-representations of a magnetic group is determined entirely by the representation of the unitary coset (those elements without timereversal, i.e. F). If under the point group action N
transforms as aeV ⊗ ΓN , we then have a clear picture
of the corresponding co-irrep of the paramagnetic group.
When aeV contains only real irreps in its decomposition,
the true paramagnetic representation is generated by retaining aeV (f ) for elements of F while ascribing to the
elements τ f the representation −aeV (f ). It’s decomposition into paramagnetic co-irreps is given directly by the
decomposition of aeV into irreps Γ(ν) of F.
When aeV contains a complex irrep10 describing the
transformation of a Néel component Ni , the paramagnetic co-irrep corresponding to Ni will assign to the elements f ∈ F a matrix of the form Eq. D1, and to the
elments τ f the matrix given by composing Eq. D2 with
that of Eq. D1. The decomposition into paramagnetic coirreps is again determined entirely by the decomposition
of aeV in F, though the co-irreps have greater dimensions.
In both cases, whether Γ(ν) is real or complex, the
product of aeV with ΓN is no different than in the unitary
case, owing to the reality of ΓN . The true co-irrep in
the spin-orbit coupled paramagnetic phase is uniquely
determined by the decomposition of aeV ⊗ ΓN in F.
Because we are concerned with the direct Landau problem, in principle we may then make predictions about the
possible black-and-white point groups describing the low
symmetry phase. We provide a simple example, using
the CrF2 example in Sec. V. The crystallographic point
group is 2/m, with elements {E, I, 2y , my }. The SO-free
irrep ΓN is Bg , and aeV decomposes as Ag ⊕ 2B2g , implying that aeV ⊗ ΓN decomposes as Bg ⊕ 2Ag , with Nx
and Nz belonging to Ag and Ny belonging to Bg . In Table XI we show full co-irreps corresponding to Ag and Bg
in 2/m + τ 2/m.
If all three components Ni are non-zero, the only possible group that may describe the magnetic order is
1 = {E, I}, as this is the intersection of trivially represented elements in Ag and Bg . If only Nx and Nz

10 This is the case for the complex 1D irreps in point groups 4, 4,

4/m, 6, 6, and 6/m. The 2D irreps in centrosymmetric groups,
as well as 422, 4mm, 42m, 3m, 3m, 622, 6mm, and 62m are all
real. In 432, −43m and m3m, aeV transforms as a real 3D irrep.

E

I

2y

my

τ

τI

τ 2y

τ my

Ag

1

1

1

1

-1

-1

-1

-1

Bg

1

1

-1

-1

-1

-1

1

1

are non-zero, then the trivially represented elements in
Ag define the ordered phase symmetry group, 2/m =
{E, I, 2y , my }. If, on the other hand, only Ny is non-zero
then 2′ /m′ = {E, I, τ 2y , τ my } defines the symmetry of
the ordered phase. All three of these cases are encapsulated by our SOC Landau theory, so it is not in conflict
with an approach centered on magnetic groups.
Appendix E: Symmetrization of tensor powers

We summarize a well-known procedure for the symmetrization of tensor powers of any representation. Here,
let G be any discrete group and let D be a representation of G in some vector space V with a basis
{ |i⟩ | i ∈ {1, ..., dim(V )}}. The n-th tensor power of D,
denoted Dn , is a representation of G in the n-th Cartesian product of V , V ×n ≡ V × ... × V . The basis in V n
is {|i1 ⟩ ⊗ |i2 ⟩ ⊗ ... ⊗ |in ⟩ | i1 , i2 , ..., in ∈ {1, ..., dim(V )}}.
Symmetrizing means ‘equally representing’ vectors that
differ only by permutations of the components in different Cartesian factors of V . By this we mean that that
the vectors |i1 ⟩ ⊗ |i2 ⟩ ⊗ ... ⊗ |in ⟩ and |iπ−1 (1) ⟩ ⊗ |iπ−1 (2) ⟩ ⊗
... ⊗ |iπ−1 (n) ⟩ are treated as equivalent, where π is an element of the permutation group on n elements, Sn , that
is
!
1
2 ... N
π=
∈ Sn .
π(1) π(2) ... π(n)
This equivalence is achieved by projecting into the subspace of V n spanned by vectors transforming under the
trivial irrep of Sn . This projector is given [104] by
P
(+)
1
(n)
Pn = n!
(π), where d(n) (π) represents
π∈Sn 1 · d
n
π in V by
d(n) (π)|i1 ⟩ ⊗ |i2 ⟩ ⊗ ... ⊗ |iN ⟩
= |iπ−1 (1) ⟩ ⊗ |iπ−1 (2) ⟩ ⊗ ... ⊗ |iπ−1 (N ) ⟩.
Then, the symmetrized tensor power [Dn ] of D is given
by
n
o
[Dn ] = Pn(+) Dn (g)|g ∈ G .
This is the technique used to calculate the symmetrized
n-th tensor power of the polar vector representation when
studying the multipoles.
The characters of symmetrized n-th tensor power representations can be easily computed using the “birdtracks” method [111]. Up to n = 6, the character of

23
an element g ∈ G in the n-th symmetrized tensor power,
χ ([Dn ](g)), is given by


1
(χ(g))2 + χ(g 2 )
χ [D2 ](g) =
2!


1
χ [D3 ](g) =
(χ(g))3 + 3χ(g)χ(g 2 ) + 2χ(g 3 ) (E1)
3!

1
χ [D4 ](g) =
(χ(g))4 + 6(χ(g))2 χ(g 2 )
4!

+ 8χ(g)χ(g 3 ) + 3(χ(g 2 ))2 + 6χ(g 4 )

1
(χ(g))5 + 10(χ(g))3 χ(g 2 )
χ [D5 ](g) =
5!
+ 15χ(g)(χ(g 2 ))2 + 20(χ(g))2 χ(g 3 )+

20χ(g 2 )χ(g 3 ) + 30χ(g)χ(g 4 ) + 24χ(g 5 )


1
χ [D6 ](g) =
(χ(g))6 + 15(χ(g))4 χ(g 2 )+
6!
45(χ(g))2 (χ(g 2 ))2 + 15(χ(g 2 ))3 +
40(χ(g))3 (χ(g 3 )) + 120χ(g)χ(g 2 )χ(g 3 )

to find the symmetry-adapted basis (SAB) any representation. We have used this technique to identify the multipole components coupling to N in the absence of SOC
in Sec. III, as well as the components of tensors coupling
to N when SOC is included as discussed in Sec. IV. These
couplings are all summarized in Table XIV.
Γ
A group projector P11
(D) for a representation D onto
an irrep Γ of the group G is given by
Γ
P11
(D) =

|Γ| X ∗
Γ11 (g)D(g),
|G|

(F1)

g∈G

and it is non-zero provided Γ is present in the decomposition of D. In Eq. F1, Γ11 is the matrix element of Γ in
the first row and first column. If the dimension |Γ| of Γ
is one, then the SAB for the irrep Γ of D is given by a
Γ
basis in the image of P11
(D). If Γ has dimension |Γ| > 1,
then the SAB for Γ will be given by a basis the image
Γ
of P11
(D), as well as those vectors obtained by acting on
the previous vectors with each of the group operators
Γ
Pm1
(D) =

|Γ| X ∗
Γm1 (g)D(g),
|G|

+ 40(χ(g 3 ))2 + 90(χ(g))2 χ(g 4 )

g∈G

+ 90χ(g 2 )χ(g 4 ) + 144χ(g)χ(g 5 )

+ 120χ(g 6 )

where m ∈ {2, .., |Γ|}. To apply this procedure to [V n ],
for example, we first express these operators in matrix
form in a vector space where each standard basis vector
corresponds to one unique combination of x, y, and z
of order n (i.e. for N = 4, x2 yz is one basis vector, as
opposed to distinct vectors for xxyz, xyxz, xyzx, yxzx,
and yzxx). This step can be achieved for any power n using the symmetrization procedure outlined in Appendix
E on the space R3n , with basis elements given by ordered
strings with characters x, y or z. Then, the SAB vectors
for [V n ] will represent symmetrized polynomials of order
n that transform under the irrep Γ of the point group.

(E2)

in terms of the characters χ(D(g)) ≡ χ(g) of the original
representation D. With these character relations, one
can demonstrate that the symmetrized tensor powers of
(s)
Γl=1 have the following decompositions:
(s) ⊗2

(s)

(s)

(s) ⊗3

(s)

(s)

(s) ⊗4

(s)

(s)

(s)

(s) ⊗5

(s)

(s)

(s)

(s) ⊗6

(s)

(s)

(s)

[Γl=1 ] = Γl=0 ⊕ Γl=2
[Γl=1 ] = Γl=1 ⊕ Γl=3
[Γl=1 ] = Γl=0 ⊕ Γl=2 ⊕ Γl=4
[Γl=1 ] = Γl=1 ⊕ Γl=3 ⊕ Γl=5

Appendix G: “Repackaging” Tensor Components

(s)

[Γl=1 ] = Γl=0 ⊕ Γl=2 ⊕ Γl=4 ⊕ Γl=6 .
(s)

Only odd symmetrized tensor powers contain the Γl=1
representation, and so only these could couple to N. As
we are looking for the minimal such multipole in the
(s)
SOC-free limit, we can focus exclusively on the Γl=1 multipole, corresponding to m(r) in the integrand of Eq. 2
in III.
The character relations Eqs. E1 and E2 also allow us
to quickly decompose the characters of the symmetrized
polar vector powers [V n ] describing the spatial transformation properties of the SO-free multipoles of Sec. III.
Appendix F: Tensor & multipole components
coupling to N

Here we provide a brief overview of the well-known
group projector techniques [104, 105, 107, 112–114] used

To produce Table V, we utilize the MTENSOR [60] tables on the Bilbao Crystallographic Server. For each tensor type, we verify whether it is possible to “repackage”
the components of a tensor into a quantity transforming
as one of the d listed in Table II. Here we outline the
various types of “repacking” we can do, demonstrating
specific examples. The definitions and transformation
properties of the full tensors are discussed in Ref. [60].
Case 1: [V 2 ]∗ → a{V 2 } → aeV
The classic example is repackaging the antisymmetric part of a [V 2 ]∗ tensor, which transforms as a{V 2 }
into a magnetic axial vector aeV. Such an example is
that of the electrical conductivity, with defining equation
Ji = σij Ej . Using Onsager’s reciprocity, under timereversal symmetry τ the components of σij are related
by τ σij = σji , which gives it the [ · ]∗ unconventional

24
Jahn symbol [60]. The antisymmetric part of this tensor
A
= 12 (σij − σji ) is a a{V 2 } tensor (where { · } denotes
σij
antisymmetrization), responsible for the anomalous Hall
conductivity. There are three independent tensor components σyz , σzx and σxy which we may arrange into
a vector {σyz , σzx , σxy } to form a magnetic axial vector
aeV . To relate the rank two and rank one objects, we
A
use the identity σαA = 21 εαij σij
. We will use analogs of
this identity for larger tensor quantities.
Case 2: (V 2 )∗ → a{V 2 } → aeV
This case is similar to Case 1, except that the initial is not related to itself under time-reversal but rather
to another tensor quantity. A classic example of this
case is that of the Peltier πij and Seebeck βij tensors,
where by Onsager’s reciprocity πij is related to βij under τ by τ πij = βji and vice versa. In this case, we
first take the antisymmetric parts of each of these tenA
A
sors, πij
= 12 (πij − πji ) and βij
= 12 (βij − βji ). Next,
we define a symmetric combination of these two tensors:
A
A
S̃ij = 21 (πij
+ βij
). This tensor transforms as an a{V 2 }
object, so by Case 1 we can repackage this into a magnetic axial vector aeV by S̃α = 21 εαij S̃ij .
Case 3: a{V 2 }[V 2 ] → aeV [V 2 ]
This case is a direct consequence of Case 1. An example is that of the Quadratic magneto-optic Kerr tensor
A
. This tensor is defined as the antisymmetric part of
Cijkl
the Cotton-Moutton tensor [60]. By Onsager’s relation,
A
A
under τ the components are related by τ Cijkl
= −Cjikl
.
Using the Levi-Civita identity from Case 1, we obtain an
A
A
.
aeV [V 2 ] tensor via Cαkl
= 21 εαij Cijkl
Case 4: e{V 2 }∗ V → ae[V 2 ]V
For tensors of type e{V 2 }∗ V such as the magnetoresistance tensor Rijk , the tensor symmetrized under exS
= 21 (Rijk + Rjik )
change of the first two indices Rijk
2
transforms as a ae[V ]V tensor.
Case 5: (eV 3 )∗ → ae[V 2 ]∗ V → ae[V 2 ]V
Tensors transforming as an (eV 3 )∗ object such as
the Ettinghausen Mijk and Nernst Nijk tensors are related by Onsagers relation under time-reversal symmetry: τ Mijk = −Njik and vice versa. We first extract the components of these tensors symmetrized unS
der the first two indices, Mijk
= 12 (Mijk + Mjik ) and
1
Nijk = 2 (Nijk +Njik ), which both transform as ae[V 2 ]∗ V
tensors. Then, we define a symmetric combination of
S
S
these components: Sijk = 21 (Mijk
+ Nijk
), which will
2
now transform as an ae[V ]V tensor.
Case 6: [V 2 ]∗ V 2 → a{V 2 }V 2 → aeV
For tensors of the form [V 2 ]∗ V 2 such as the magnetic
resistance tensor Tijkl we apply the argument from Case

1. We first extract the component antisymmetric under
A
exchange of the first two indices Tijkl
= 12 (Tijkl − Tjikl )
2
2
that transforms as a a{V }[V ] tensor. Then we use
A
the Levi-Civita identity from Case 1 to obtain Tαkl
=
1
A
2
ε
T
.
This
tensor
transforms
as
aeV
[V
].
αij
ijkl
2
Case 7: (V 2 [V 2 ])∗ → ([V 2 ][V 2 ])∗ → aeV [V 2 ]
Quantities such as the magneto-Peltier Pijkl and
magneto-Seebeck αijkl tensors are related to each other
under time-reversal symmetry by Onsager’s relations,
τ αijkl = Pjikl . We first extract the components of these
tensors that are antisymmetric under exchange of the
A
A
first two indices, αijkl
= 21 (αijkl − αjikl ) and Pijkl
=
1
2
2 ∗
2 (Pijkl − Pjikl ), which transform as ([V ][V ]) quantities. Then, we define an antisymmetric combination
A
A
of these two tensors: Ã = 21 (αijkl
− Pijkl
), transform2
2
ing as a{V }[V ]. Finally, we use the identity from Case
1 to express this tensor as an aeV [V 2 ] object, Ãαkl =
1
2 εαij Ãijkl .

25
Appendix H: Table of space groups and Wyckoff positions supporting altermagnetic order

TABLE XII. Space group Wyckoff positions supporting altermagnetism, and the irreps ΓN under which N transforms.
PG

SG

WP

ΓN

PG

2

3

{2e}

{B}

mm2 28

4

{2a}

{B}

{2b, 2a}

{A2 }

5

{4c, 2b, 2a}

{B}

{2c}

{B2 }

6

{2c}

{A′′ }

29

{4a}

{A2 , B2 , B1 }

7

{2a}

{A′′ }

30

{4c}

{A2 , B2 , B1 }

8

{4b}

{A′′ }

9

{4a}

{A′′ }

2/m 10

{4o}

{Bg }

{4f, 2d, 2c, 2b, 2a}

{Bg }

m

11

12 {8j, 4h, 4g, 4f, 4e, 2d, 2b}

222

SG

31
32

{Bg }

WP

ΓN

{4d}

{A2 , B2 , B1 }

{2b, 2a}

{A2 }

{4b}

{A2 , B2 , B1 }

{2a}

{B2 }

{4c}

{A2 , B2 , B1 }

{2b, 2a}

{A2 }

13

{4g, 2d, 2c, 2b, 2a}

{Bg }

33

{4a}

{A2 , B2 , B1 }

14

{4e, 2d, 2c, 2b, 2a}

{Bg }

34

{4c}

{A2 , B2 , B1 }

15

{8f, 4e, 4d, 4c, 4b, 4a}

{Bg }

{2b, 2a}

{A2 }

{8f, 4e, 4c}

{A2 , B2 , B1 }

{2b}

{A2 }

16

17

35

{4u}

{B1 , B3 , B2 }

{2t, 2s, 2r, 2q}

{B1 }

{2p, 2o, 2n, 2m}

{B2 }

{4d}

{B1 }

{2l, 2k, 2j, 2i}

{B3 }

36

{8b, 4a}

{A2 , B2 , B1 }

{4e}

{B1 , B3 , B2 }

37

{8d, 4c}

{A2 , B2 , B1 }

{2d, 2c}

{B2 }

{2b, 2a}

{B3 }

38

{4b, 4a}

{A2 }

{8f }

{A2 , B2 , B1 }

{4c}

{B1 , B3 , B2 }

{4c}

{B1 }

{2b, 2a}

{B1 }

{4e, 4d}

{B2 }

19

{4a}

{B1 , B3 , B2 }

{8d, 4c}

{A2 , B2 , B1 }

20

{8c, 4b}

{B1 , B3 , B2 }

{4a}

{B3 }

{8l, 4k, 4h, 4g}

{B1 , B3 , B2 }

{4a}

{A2 }

{4j, 4i, 2b}

{B1 }

{4b}

{B2 }

{4f, 4e}

{B3 }

{8b}

{A2 , B2 , B1 }

18

21

39
40

41

24
mm2 25

26
27

{A2 }

{8c}

{A2 , B2 , B1 }

{4a}

22 {16k, 8j, 8i, 8h, 8g, 8f, 8e} {B1 , B3 , B2 }
23

{4b, 4a}

42 {16e, 8d, 8c, 8b, 4a}

{A2 }
{A2 , B2 , B1 }

{4d, 4b}

{B1 }

{8k, 4j, 4i, 4f, 2c}

{B1 , B3 , B2 }

{4h, 4g}

{B2 }

44 {8e, 4d, 4c, 2b, 2a}

{4e}

{B3 }

45

{8c, 4b, 4a}

{A2 , B2 , B1 }

{8d, 4c, 4a}

{B1 , B3 , B2 }

46

{8c, 4b, 4a}

{A2 , B2 , B1 }

{4b}

{B2 }

mmm 47

{4z, 4y}

{B1g }

{4i}

{A2 , B2 , B1 }

{8a}

{B1g , B3g , B2g }

{2f, 2e}

{B1 }

{4x, 4w}

{B2g }

{2h, 2g}

{B2 }

{4v, 4u}

{B3g }

{8m, 4f, 4e}

{B1g , B3g , B2g }

{4l, 4k}

{B1g }

43

48

{16b, 8a}

{A2 , B2 , B1 }
{A2 , B2 , B1 }

{4c}

{A2 , B2 , B1 }

{2b, 2a}

{B2 }

{4e}

{A2 , B2 , B1 }

{4j, 4i}

{B2g }

{2d, 2c, 2b, 2a}

{A2 }

{4h, 4g}

{B3g }

26
PG
PG

SG

WP

ΓN

SG

WP

ΓN

mmm 49

{8r}

{B1g , B3g , B2g }

{8l}

{B1g }

{4q, 4p, 4o, 4n, 4m, 2d, 2c, 2b, 2a}

{B1g }

{8i, 8h, 4d, 4c}

{B3g }

{4l, 4k}

{B2g }

68

{16i, 8g, 8f, 8e, 8d, 8c, 4b, 4a}

{B1g , B3g , B2g }

{4j, 4i}

{B3g }

{B1g }

{8m, 4f, 4e}

{B1g , B3g , B2g }

{4l, 4k}

{B1g }

69

{8h}
{32p, 16o, 16n, 16m,
16l, 16k, 16j, 8e, 8d, 8c}

{B1g , B3g , B2g }
{B1g }

50

51

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

{16o, 8n, 8m, 8k, 8j, 4g, 4f, 4e} {B1g , B3g , B2g }

{4j, 4i}

{B2g }

{8i, 4b}

{4h, 4g}

{B3g }

{8h}

{B2g }

{8l}

{B1g , B3g , B2g }

{8g}

{B3g }

{4j, 4i, 4h, 4g, 2d, 2c, 2b, 2a}

{B2g }

{32h, 16g, 16f, 16e, 16d, 16c}

{B1g , B3g , B2g }

{8b}

{B1g }

{4k}
52

mmm 67

{B3g }

{8e, 4b, 4a}

{B1g , B3g , B2g }

{4c}

{B1g }

{4d}

{B3g }

{8i}

{B1g , B3g , B2g }

{4g}

{B2g }

{4h, 4f, 4e, 2d, 2c, 2b, 2a}

{B3g }

{8f, 4b, 4a}

{B1g , B3g , B2g }

{4e, 4d}

{B1g }

{4c}

{B2g }

{8i}

70

{B1g , B3g , B2g }

71 {16o, 8m, 8l, 8k, 4j, 4i, 4h, 2d, 2b} {B1g , B3g , B2g }
{8n}

{B1g }

72

{16k, 8i, 8h, 8g, 8f, 8e, 4b, 4a}

{B1g , B3g , B2g }

{8j, 4d, 4c}

{B1g }

73

{16f, 8e, 8c, 8b, 8a}

{B1g , B3g , B2g }

{8d}

{B2g }

{16j, 8i, 8h, 8g, 4e, 4d, 4c}

{B1g , B3g , B2g }

{4b}

{B2g }

{8f, 4a}

{B3g }

74

4

75

{4d, 2c}

{B}

{4a}

{B}

{4h, 4g, 4f, 4e, 2d, 2c, 2b, 2a}

{B1g }

76

{8e, 4b, 4a}

{B1g , B3g , B2g }

77

{4d, 2c, 2b, 2a}

{B}

{4d, 4c}

{B1g }

78

{4a}

{B}

{8e, 4b, 4a}

{B1g , B3g , B2g }

79

{8c, 4b, 2a}

{B}

{4d}

{B1g }

80

{8b, 4a}

{B}

{4c}

{B3g }

81

{4h, 2g, 2f, 2e}

{B}

82

{8g, 4f, 4e, 2d, 2c, 2b}

{B}

83

{8l, 4k, 4j, 4i, 2f, 2e}

{Bg }

{8h}

4

{B1g , B3g , B2g }

{4g, 4f, 4e, 2d, 2c, 2b, 2a}

{B1g }

{8g, 4d, 4c}

{B1g , B3g , B2g }

4/m

84 {8k, 4j, 4i, 4h, 4g, 2d, 2c, 2b, 2a}

{Bg }

{8g, 4f, 4e, 4d}

{Bg }
{Bg }

{4f }

{B2g }

85

{4e}

{B3g }

86

{8g, 4f, 4e, 4d, 4c}

{B1g , B3g , B2g }

87

{16i, 8h, 8g, 8f, 4e, 4d, 4c, 2b}

{Bg }

{4c}

{B2g }

88

{16f, 8e, 8d, 8c, 4b, 4a}

{Bg }

{8c, 4b, 4a}

{B1g , B3g , B2g }

{8d, 4b, 4a}

422

89

{8p, 4i}

{B1 , A2 , B2 }
{A2 }

{8d, 4b, 4a}

{B1g , B3g , B2g }

{2h, 2g}

{4c}

{B2g }

{4o, 4n, 4m, 4l, 2f, 2e}

{B1 }

{16h, 8f, 8d, 4b}

{B1g , B3g , B2g }

{4k, 4j}

{B2 }

{8g, 4c}

{B1g }

{8g, 4d}

{B1 , A2 , B2 }

{8e, 4a}

{B3g }

{2c}

{A2 }

{16g, 8f, 8e, 8c}

{B1g , B3g , B2g }

{4f, 4e, 2b, 2a}

{B2 }

{8d, 4b, 4a}

{B3g }

{8d}

{B1 , A2 , B2 }

{4b, 4a}

{B1 }

{16r, 8n, 8m}

{B1g , B3g , B2g }

{8q, 8p, 4l, 4j, 4i, 4f, 4e}

{B1g }

{8o}

{B2g }

{16m, 8k, 8h}

{B1g , B3g , B2g }

{8l, 8j, 8i, 4f, 4e, 4d, 4c, 4b}

{B1g }

{8g}

{B3g }

90

91

92
93

{4c}

{B2 }

{8b}

{B1 , A2 , B2 }

{4a}

{B2 }

{8p, 4i, 4h, 4g}

{B1 , A2 , B2 }

{4m, 4l, 4k, 4j, 2d, 2c, 2b, 2a}

{B1 }

{4o, 4n, 2f, 2e}

{B2 }

27
PG

SG

422

94
95

96
97

98
4mm 99

100

101
102

WP

ΓN

PG

SG

4m2

115

{8g, 4d, 4c}

{B1 , A2 , B2 }

{4f, 4e, 2b, 2a}

{B2 }

{8d}

{B1 , A2 , B2 }

{4b, 4a}

{B1 }

{4c}

{B2 }

116

WP

ΓN

{8l}

{B1 , B2 , A2 }

{4i, 4h}

{A2 }

{4k, 4j, 2g, 2f, 2e}

{B1 }

{8j, 4i, 4h, 4g}

{B1 , B2 , A2 }

{4f, 4e, 2b, 2a}

{A2 }

{8b}

{B1 , A2 , B2 }

{4a}

{B2 }

{16k, 8j, 8i, 8f, 4e, 4d}

{B1 , A2 , B2 }

{4h, 4g, 2d, 2c}

{A2 }

{8h, 4c}

{B1 }

{2b, 2a}

{B2 }

{8g, 2b}

{B2 }

{8i, 4h, 4e}

{B1 , B2 , A2 }

117

118

{2d, 2c}

{B2 }

{8i, 4f, 4e}

{B1 , B2 , A2 }

{16g, 8f, 8c}

{B1 , A2 , B2 }

{4g, 4f, 2d, 2c}

{A2 }

{8e, 8d, 4b, 4a}

{B2 }

{2b, 2a}

{B2 }

{16j, 8i, 8h, 4f, 4e, 2d, 2c}

{B1 , B2 , A2 }

{8g}

{B1 , B2 , A2 }

{4f, 4e, 2c}

{B1 }

{4d}

{B2 }

{8d}

{B1 , B2 , A2 }

{8h, 4d}

{A2 }

{2a}

{A2 }

{4b}

{B2 }

{16j, 8h, 8g, 4d}

{B1 , B2 , A2 }

119
120

{8g, 2b}

{A2 }

{16i, 8g, 8f, 8e, 4c, 4a}

{B1 , B2 , A2 }

{4c, 2b}

{B2 }

{8e, 4c}

{B1 , B2 , A2 }

{8f, 4c}

{B1 }

{4d, 2b, 2a}

{B2 }

{8i, 4e, 2b}

{B2 }

{16e, 8d, 8c, 4b}

{B1 , B2 , A2 }

{4a}

{A2 }

{8d, 4b}

{B1 , B2 , A2 }

{4c, 2a}

{B2 }

121

122

{8d, 4c}

{B1 , B2 , A2 }

{16u, 8q, 8p}

{B1g , A2g , B2g }

{2b, 2a}

{A2 }

{8t, 8s, 4o, 4n, 4m, 4l, 4i, 2f, 2e}

{B1g }

104

{8c, 4b}

{B1 , B2 , A2 }

{8r, 4k, 4j}

{B2g }

{2a}

{A2 }

{16n, 8m, 8i, 4e}

{B1g , A2g , B2g }

105

{8f }

{B1 , B2 , A2 }

{4h, 4g, 2d, 2b}

{A2g }
{B1g }

103

4/mmm 123

124

{4e, 4d, 2c, 2b, 2a}

{B1 }

{8l, 8k, 4f }

106

{8c, 4b, 4a}

{B1 , B2 , A2 }

{8j}

{B2g }

107

{16e, 8d, 4b}

{B1 , B2 , A2 }

{16n}

{B1g , A2g , B2g }

{8c, 2a}

{B2 }

{4g}

{A2g }

108

{16d, 4a}

{B1 , B2 , A2 }

{8l, 8k}

{B1g }

{8c, 4b}

{B2 }

109

{16c, 8b, 4a}

{B1 , B2 , A2 }

110

{16b, 8a}

42m 111

112

113

114

125

{8m, 8j, 8i, 4h, 4f, 4e}

{B2g }

{16k, 8g, 8f }

{B1g , A2g , B2g }

{B1 , B2 , A2 }

{4e, 4d}

{A2g }

{8o, 4m}

{B1 , B2 , A2 }

{8j, 8i, 4c}

{B1g }

{4l, 4k, 4j, 4i, 2f, 2e}

{B1 }

{8h}

{B2g }

{16l, 8j, 8i}

{B1g , A2g , B2g }

126

{4n, 2h, 2g}

{B2 }

{8n, 4m, 4l, 4k}

{B1 , B2 , A2 }

{4e, 2b, 2a}

{A2g }

{2f, 2e}

{A2 }

{8k, 4h, 4g, 4f, 2d, 2c}

{B2g }

{16i, 8h, 8f, 4c}

{B1g , A2g , B2g }

{4e, 2b, 2a}

{A2g }

{4j, 4i, 4h, 4g, 2d, 2c, 2b, 2a}

{B1 }

{8f, 4d}

{B1 , B2 , A2 }

127

128

{8g, 4d}

{B2g }

{16k}

{B1g , A2g , B2g }

{B1 , B2 , A2 }

{8i, 4f }

{B1g }

{A2 }

{8j, 8h, 8g, 4e, 4d}

{B2g }

{2b, 2a}

{A2 }

{4e, 2c}

{B2 }

{8e, 4d, 4c}
{2b, 2a}

129

28
PG

SG

4/mmm 130

131

132

133

134

135

136

137

138

139

WP

ΓN

{16g, 8e, 8d}

{B1g , A2g , B2g }

PG

SG

3m 162

{A2g }
{A2g }
{A2g }

{4c, 4b}

{A2g }
{B2g }

164

{12j}

{16r, 8q}
{8p, 8o, 4m, 4l, 4k, 4j, 4i,
4h, 4g, 2d, 2c, 2b, 2a}

{B1g , A2g , B2g }

165

{12g, 6e, 4d, 4c, 2b}

{A2g }

166

{36i}

{A2g }

{8n}

{B2g }

{16p, 8n, 8k, 4f }

{B1g }

167 {36f, 18e, 18d, 12c, 6b}

{A2g }

168

{6d, 2b}

{B}

{B1g , A2g , B2g }

169

{6a}

{B}

{8m, 8l, 4e}

{B1g }

170

{6a}

{B}

{8o, 4j, 4i, 4h, 4g, 2c, 2a}

{B2g }

171

{6c}

{B}

{16k, 8g, 8f, 8e}

{B1g , A2g , B2g }

172

{6c}

{B}

{4d}

{A2g }

173

{6c, 2b, 2a}

{B}

{8i, 8h, 4b, 4a}

{B1g }

174

{6l, 2i, 2h, 2g}

{A′′ }

{12l, 4h}

{Bg }

{8j, 4c}

{B2g }

{16n, 8h}

{B1g , A2g , B2g }

{8j, 8i, 4c}

{B1g }

6

6

6/m 175
176
622 177

{12i, 6g, 4f, 4e, 2b}

{Bg }

{12n, 4h}

{A2 , B2 , B1 }

{8m, 8l, 8k, 4g, 4f, 4e, 4d}

{B2g }

{6i, 2e}

{A2 }

{16i, 8h, 8f, 8e, 4c, 4a}

{B1g , A2g , B2g }

{6m, 6l, 2d, 2c}

{B1 }

{4b}

{A2g }

{6k, 6j}

{B2 }

{8g, 4d}

{B2g }

{12c}

{A2 , B2 , B1 }

{16k, 8i, 8h, 4c}

{B1g , A2g , B2g }

{6b}

{B1 }

{4d}

{A2g }

{6a}

{B2 }

{8j, 4g, 4f, 4e, 2b, 2a}

{B2g }

{12c}

{A2 , B2 , B1 }

{16h, 8e}

{B1g , A2g , B2g }

{6b}

{B1 }

{8g, 4d, 4c}

{B1g }

{8f }

{B2g }

{16j, 8f }

{B1g , A2g , B2g }

{4b}

{A2g }

{6j, 6i}

{B1 }

{8i, 8h, 8g, 4e, 4d, 4c, 4a}

{B2g }

{6h, 6g}

{B2 }

{32o, 16n, 16l, 16k, 8g, 4d}

{B1g , A2g , B2g }

{12k}

{A2 , B2 , B1 }

{8j, 8i, 4c}

{B1g }

{6f, 6e}

{A2 }

{16m, 8h, 8f, 4e, 2b}

{B2g }

{6j, 6i}

{B1 }

178

179

180

181

{A2g }

182

{6a}

{B2 }

{12k}

{A2 , B2 , B1 }

{6f, 6e}

{A2 }

{6h, 6g}

{B2 }

{12i, 4f, 4e}

{A2 , B2 , B1 }

{16l, 8h, 8g, 4d, 4b}

{B2g }

{6h, 2d, 2c, 2b}

{B1 }

{32i, 16h, 16g, 8e, 4b, 4a}

{B1g , A2g , B2g }

{6g, 2a}

{B2 }

{16f, 8d, 8c}

{B1g }

6mm 183

142 {32g, 16f, 16e, 16d, 16c, 8b, 8a} {B1g , A2g , B2g }

3m

{12l, 4h}
{12i, 6g, 4f, 4e, 2b}

{8f, 4a}

{4c}

32

ΓN

163

140 {32m, 16k, 16j, 16i, 8f, 8e, 4a} {B1g , A2g , B2g }

141

WP

149

{6l, 2i, 2h, 2g}

{A2 }

150

{6g, 2d, 2c}

{A2 }

151

{6c}

{A2 }

152

{6c}

{A2 }

153

{6c}

{A2 }

154

{6c}

{A2 }

155

{18f, 9e, 9d, 6c}

{A2 }

156

{6e}

{A2 }

157

{6d, 2b}

158

{6d, 2c, 2b, 2a}

159

{6c, 2b, 2a}

{A2 }

160

{18c}

{A2 }

161

{18b, 6a}

{A2 }

184
185
186

{12f }

{A2 , B2 , B1 }

{6e, 2b}

{B1 }

{6d}

{B2 }

{12d, 4b}

{A2 , B2 , B1 }

{6c, 2a}

{A2 }

{12d, 4b}

{A2 , B2 , B1 }

{6c, 2a}

{B2 }

{12d}

{A2 , B2 , B1 }

{6c, 2b, 2a}

{B1 }

{12o}

{A′′1 , A′′2 , A′2 }

{A2 }

{6m, 6l}

{A′′1 }

{A2 }

{6n, 2i, 2h, 2g}

{A′′2 }

{12l, 4i, 4h, 4g}

{A′′1 , A′′2 , A′2 }

{6k, 2f, 2d, 2b}

{A′′1 }

{6j, 2e, 2c, 2a}

{A′2 }

6m2 187

188

29
PG
62m

SG
189

WP

ΓN

{12l, 4h}

{6h, 2d, 2c, 2b}

{A′′1 , A′′2 , A′2 }
{A′2 }
{A′′2 }
′′
{A1 , A′′2 , A′2 }
{A′′1 }
{A′2 }

{24r}

{A2g , B2g , B1g }

{6k, 6j, 2d, 2c}
{6i, 2e}
190

{12i, 4f, 4e}
{6g, 2a}

6/mmm 191

192

193

194

m3m

{12q, 12p}

{A2g }

{12n}

{B1g }

{12o, 4h}

{B2g }

{24m, 8h}

{A2g , B2g , B1g }

{12l, 12i, 6g, 4e, 4d, 2b}

{A2g }

{12k, 4c}

{B1g }

{12j}

{B2g }

{24l, 8h}

{A2g , B2g , B1g }

{12j, 4c}

{A2g }

{12k, 12i, 6f, 4e, 4d, 2b}

{B1g }

{24l}

{A2g , B2g , B1g }

{12j}

{A2g }

{12k, 12i, 6g, 4f, 4e, 2a}

{B2g }

221

{48n, 24l, 24k, 12h}

{A2g }

222

{48i, 24g, 16f, 8c}

{A2g }

223

{48l, 24k, 16i, 12h, 12g, 12f, 6b, 2a}

{A2g }

224

{48l, 24h}

{A2g }

225

{192l, 96j}

{A2g }

226

{192j, 96i, 96h, 64g, 48e, 24c, 8b}

{A2g }

227

{192i}

{A2g }

228

{192h, 96g, 96f, 64e, 48d, 32c, 16a}

{A2g }

229

{96l, 48i}

230 {96h, 48g, 48f, 32e, 24d, 24c, 16b, 16a}
432

207

{24k, 12h, 8g}

{A2 }

208

{24m, 12j, 12i, 12h, 8g, 6d, 2a}

{A2 }

209

{96j, 48i, 48h, 48g, 32f, 24d, 8c}

{A2 }

210

{96h, 48f, 32e, 8b, 8a}

{A2 }

211

{48j, 24i, 24h, 24g, 16f, 8c}

{A2 }

212

{24e, 8c}

{A2 }

213

{24e, 8c}

{A2 }

214 {48i, 24h, 24g, 24f, 16e, 12d, 12c, 8b, 8a}
43m

{A2g }
{A2g }

{A2 }

{24j, 12h}

{A2 }

216

{96i}

{A2 }

217

{48h, 24f }

{A2 }

218

{24i, 12h, 12g, 12f, 8e, 6b, 2a}

{A2 }

219

{96h, 48g, 48f, 32e, 24d, 24c, 8b, 8a}

{A2 }

220

{48e, 24d, 16c, 12b, 12a}

{A2 }

215

30
Appendix I: Table of multipoles coupling to ΓN in the SOC-free limit

ΓN V



V2

 

V3

  4  5  6
V
V
V

ΓN V



V2

2
B ✓

✓

✓

V3

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

A2 ✓

✓

✓

✓

✓

✓

✓

B2

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

B2 ✓

✓

✓

✓

✓

✓

✓

B3 ✓

✓

✓

✓

✓

✓

B2 ✓

✓

✓

✓

✓

✓

42m

222

A2
✓

A2

✓

✓

✓

✓

✓

B2 ✓

✓

✓

✓

✓

✓

B1 ✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

A2

✓

✓

✓

B2

✓

✓

✓

✓

B1

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

A′′1

✓

A′′2
A′2

✓

✓

B1g
A2g
B2g

✓

B1g

✓

✓

✓

B3g

✓

✓

✓

B2g

✓

✓

✓

A2 ✓

✓

B

✓

✓

✓

B ✓

✓

✓

Bg

✓

✓

✓

✓

A′′1

✓

✓

A′′2
A′2

✓

✓

✓

✓

✓

✓

3m
✓

✓

✓

A2

✓

✓

✓

A2g

✓

B
′′

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

A

✓

✓

✓

✓
✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

✓

43m

✓

✓
m3m

A2g
✓

✓
432

A2
✓

✓
✓
✓

B2g

✓

6/m
Bg

✓

6/mmm

A2
✓

6

422

✓
✓

✓

6m2

✓

6
✓

✓

B1g
✓

4/m

✓

A2g

3m

4

✓

62m

✓

32

4

✓

✓

4/mmm

mmm

6mm

✓

✓

A2

622

B1

4m2
B1 ✓
B2

mm2

  3  4  5  6
V
V
V
V

✓

✓

B1 ✓

V2

✓

2/m
✓



✓

B1

✓

B2

ΓN V

✓

✓

Bg

✓

  5  6
V
V

B2
A2

✓

A2 ✓

V4

B1

✓

A” ✓

B1

 

4mm

m
✓

 

✓

✓

TABLE XIII. Table of the (1, N ) spatial part of the SOC-free multipoles coupling to the possible Néel vectors in each point
group. Recall that in the spin space, the multipole has M = 1, i.e. the true multipole coupling to N is the direct product of
(s)
Γl=1 with the multipoles presented in this table.

31
Appendix J: Table of symmetry-allowed couplings with and without SOC

PG

2

ΓN

SO-Free Components

B

{z, x}

Guaranteed

SOC

Coupling

aV

{zNy , yNz , yNx , xNy }

aeV 2

{ zNz Rz , zNx Rz , zNy Ry , zNz Rx , zNx Rx ,
yNy Rz , yNz Ry , yNx Ry , yNy Rx , xNz Rz ,
xNx Rz , xNy Ry , xNz Rx , xNx Rx }

aV

{ zNz , zNx , yNy , xNz , xNx }

m

A′′

{y}

aeV 2

{ zNy Rz , zNz Ry , zNx Ry , zNy Rx , yNz Rz ,
yNx Rz , yNy Ry , yNz Rx , yNx Rx ,
xNy Rz , xNz Ry , xNx Ry , xNy Rx }

2/m

Bg

{xy, yz}

aeV

{ Ny Rz , Nz Ry , Nx Ry , Ny Rx }

B1

{z}

aeV

222

A2

{xy}

B2

{y}

aeV 2

{ zNx Rz , zNz Rx , yNx Ry , yNy Rx ,
xNz Rz , xNy Ry , xNx Rx }

aV

{zNx , xNz }

aeV 2

{ zNy Rz , zNz Ry , yNz Rz , yNy Ry ,
yNx Rx , xNx Ry , xNy Rx }

aeV

{ Nx Ry , Ny Rx }

aV

{ zNx , xNz }

aeV 2

{ zNy Rz , zNz Ry , yNz Rz , yNy Ry ,
yNx Rx , xNx Ry , xNy Rx }

aV

{ zNy yNz }

aeV 2

{ zNx Rz , zNz Rx , yNx Ry , yNy Rx ,
xNz Rz , xNy Ry , xNx Rx }

B1g

{xy}

aeV

{ Nx Ry , Ny Rx }

B3g

{yz}

aeV

{ Ny Rz , Nz Ry }

{xz}

aeV

{ Nx Rz , Nz Rx }

2

aeV

{ Nx Rx − Ny Ry , Ny Rx + Nx Ry }

aV

{ zNz , xNx + yNy , xNy − yNx }

aeV 2

{ zNz Rz , z (Nx Rx + Ny Ry ) , z (Ny Rx − Nx Ry ),
(Rz (xNx + yNy )) , Rz (xNy − yNx ),
Nz (xRx + yRy ) , Nz (xRy − yRx ) }

aeV

{ Nx Rx − Ny Ry , Ny Rx + Nx Ry }

aeV

{ Ny Ry − Nx Rx }

B2g
B

2

{y − x , xy}

4

B

{z}

4/m

Bg

{y 2 − x2 , xy}

422

{zNy , yNz }

{x}

B1

{ zNz Rz , zNy Ry , zNx Rx , yNy Rz ,
yNz Ry , xNx Rz , xNz Rx }

aV

{y}

mm2

4

2

{x}

B3

B2

mmm

{ yNx , xNy }

aV

2

2

B1

{y − x }

A2

{z}

B2

{xy}

B1

2

2

{y − x }

aV

{ yNx − xNy }

aeV 2

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }

aeV

{ Ny Rx + Nx Ry }

aeV

{ Ny Ry − Nx Rx }

TABLE XIV. For each point group and ΓN , the minimal SO-free multipole polynomial (see Eq. 2) is given in the third column.
The representation Γξ of the allowed tensor with SOC and its coupling to Ni components appear in last two columns.

32
PG

ΓN

SO-Free Components

4mm

B2

{xy}

aeV

{ Ny Rx + Nx Ry }

A2

{xy(x2 − y 2 )}

aeV [V 2 ]

{ zRz (yNx − xNy ) , y 2 Ny Rx − x2 Nx Ry ,
xy (Nx Rx − Ny Ry ) , x2 Ny Rx − y 2 Nx Ry ,
zNz (yRx − xRy ) , z 2 (Ny Rx − Nx Ry ) }

B1

{y 2 − x2 }

aeV

{ Ny Ry − Nx Rx }

{z}

aV

B2

{ yNx − xNy }

A2

{z(y 2 − x2 )}

aeV 2

{z}

aV

{ yNx − xNy }

aeV 2

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }

{xyz}

aeV 2

{z (Ny Rx + Nx Ry ) , Rz (yNx + xNy ), Nz (yRx + xRy )}

A2

{xy}

aeV

{ Ny Rx + Nx Ry }

B1g

2

{y − x }

aeV

{ Ny Ry − Nx Rx }

A2g

{xy(x2 − y 2 )}

aeV [V 2 ]

{ zRz (yNx − xNy ) , y 2 Ny Rx − x2 Nx Ry ,
xy (Nx Rx − Ny Ry ) , x2 Ny Rx − y 2 Nx Ry ,
zNz (yRx − xRy ) , z 2 (Ny Rx − Nx Ry ) }

B2g

{xy}

aeV

{Ny Rx + Nx Ry }

aV

{ yNx − xNy }

aeV 2

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ),
Nx (xRx − yRy ) − Ny (yRx + xRy ) }

42m

B1

Guaranteed

aeV

2

4m2
B2

4/mmm

2

SOC

Coupling

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }
{ zNy Ry − zNx Rx , Rz (yNy − xNx ), Nz (yRy − xRx ) }

32

A2

{z}

3m

A2

{y(y 2 − 3x2 )}

aeV 2

3m

A2g

{y(y 2 −3x2 )z}

aeV [V 2 ]

6

B

{x(3y 2 − x2 ), y(y 2 − 3x2 )}

aeV 2

{ Ny (yRy − xRx ) − Nx (yRx + xRy ),
Ny (yRx + xRy ) + Nx (yRy − xRx ) }

aV

{ zNz , xNx + yNy , xNy − yNx }

6

A′′

{z}

aeV 2

6/m

Bg

{xz(x2 − 3y 2 ), yz(y 2 − 3x2 )}

aeV [V 2 ]

A2

{z}

B2

{x(y 2 − 3x2 )}

2

622

B1

2

2

{y(y − 3x )}

{ zNz Rz , z (Nx Rx + Ny Ry ) , z (Ny Rx − Nx Ry ),
Rz (xNx + yNy ) , Rz (xNy − yNx ),
Nz (xRx + yRy ) , Nz (xRy − yRx ) }


{ Rz Ny y 2 − x2 − 4xyNx ,




Rz Nx y 2 − x2 + 4xyNy , Nz Ry y 2 − x2 − 4xyRx ,


Nz Rx x2 − y 2 − 4xyRy ,
z (Nx (xRx − yRy ) − Ny (yRx + xRy )),
z (Nx (yRx + xRy ) + Ny (xRx − yRy )) }
{ yNx − xNy }

aV
aeV

{ zNx Ry − zNy Rx , Rz (yNx − xNy ),
Ny (y Ry − xRx ) − Nx (yRx + xRy ) , Nz (yRx − xRy ) }


{ Rz Ny y 2 − x2 − 4xyNx , zRz (yNx − xNy ),



Nz Ry y 2 − x2 − 4xyRx , x2 + y 2 (Ny Rx − Nx Ry ),
yNx (2xRx + yRy ) − xNy (xRx + 2yRy ), zNz (yRx − xRy ),
z (Nx (yRx + xRy ) + Ny (xRx − yRy )),
z 2 (Ny Rx − Nx Ry ) }

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }

aeV 2

{ Ny (yRx + xRy ) + Nx (yRy − xRx ) }

2

{ Ny (yRy − xRx ) − Nx (yRx + xRy ) }

aeV

33
PG

ΓN

SO-Free Components

Guaranteed

A2

{3x5 y − 10x3 y 3 + 3xy 5 }

aeV [V 2 ]

B2

{x(y 2 − 3x2 )}

aeV 2

{ Ny (yRx + xRy ) + Nx (yRy − xRx ) }

2

{ Ny (yRy − xRx ) − Nx (yRx + xRy ) }


{ Rz Ny y 2 − x2 − 4xyNx ,


Nz Ry y 2 − x2 − 4xyRx ,

6mm
2

2

B1

{y(y − 3x )}

aeV

A′′1

{yz(y 2 − 3x2 }

aeV [V 2 ]

A′′2

{z}

A′2

{y(y 2 − 3x2 ))}

A′′1

2

2

{x(3y − x )}

aV

{ yNx − xNy }

aeV 2

{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }

aeV 2

{ Ny (yRy − xRx ) − Nx (yRx + xRy ) }

2

{ Ny (yRx + xRy ) + Nx (yRy − xRx ) }

aeV
aV

6/mmm

Coupling

{ zRz (yNx − xNy ), x2 + y 2 (Ny Rx − Nx Ry ),
yNx (2xRx + yRy ) − xNy (xRx + 2yRy ),
zNz (yRx − xRy ) , z 2 (Ny Rx − Nx Ry ) }

z (Nx (yRx + xRy ) + Ny (xRx − yRy )) }

62m

6m2

SOC

A′′2

{z}

aeV 2

A′2

{xz(x2 −3y 2 )}

aeV [V 2 ]

A2g

{3x5 y − 10x3 y 3 + 3xy 5 }

aeV [V 2 ]

B2g

{yz(y 2 −3x2 )}

aeV [V 2 ]

B1g

{xz(x2 −3y 2 )}

aeV [V 2 ]

{ yNx − xNy }
{ zNz Rz , z (Nx Rx + Ny Ry ),
Rz (xNx + yNy ) , Nz (xRx + yRy ) }


{ Rz Nx y 2 − x2 + 4xyNy ,


2
2
Nz Rx x − y − 4xyRy ,
z (Nx (xRx − yRy ) − Ny (yRx + xRy )) }

{ zRz (yNx − xNy ) , x2 + y 2 (Ny Rx − Nx Ry ),
yNx (2xRx + yRy ) − xNy (xRx + 2yRy ),
zNz (yRx − xRy ) , z 2 (Ny Rx − Nx Ry ) }


{ Rz Ny y 2 − x2 − 4xyNx ,


Nz Ry y 2 − x2 − 4xyRx ,
z (Nx (yRx + xRy ) + Ny (xRx − yRy )) }


{ Rz Nx y 2 − x2 + 4xyNy ,


Nz Rx x2 − y 2 − 4xyRy ,
z (Nx (xRx − yRy ) − Ny (yRx + xRy )) }

432

A2

{xyz}

aeV 2

43m

A2

{(x2 − y 2 )(x2 − z 2 )(y 2 − z 2 )}

aeV [V 2 ]

m3m

A2g

{(x2 −y 2 )(x2 −z 2 )(y 2 −z 2 )}

aeV [V 2 ]

{ Nz (yRx + xRy ) + Ny (zRx + xRz ) + Nx (zRy + yRz ) }



{Nz Rz y 2 − x2 + Ny Ry x2 − z 2 + Nx Rx z 2 − y 2 ,
zNz (xRx −yRy )+xNx (yRy −zRz )+Ny (yzRz −xyRx )}



{ Nz Rz y 2 − x2 + Ny Ry x2 − z 2 + Nx Rx z 2 − y 2 ,
(zNz (xRx −yRy )+xNx (yRy −zRz )+Ny (yzRz −xyRx ))}

34

[1] M. Dyakonov and V. Perel, Current-induced spin orientation of electrons in semiconductors, Physics Letters A
35, 459 (1971).
[2] J. Sinova, S. O. Valenzuela, J. Wunderlich, C. H. Back,
and T. Jungwirth, Spin hall effects, Rev. Mod. Phys.
87, 1213 (2015).
[3] D. Hou, Z. Qiu, and E. Saitoh, Spin transport in antiferromagnetic insulators: progress and challenges, NPG
Asia Materials 11, 35 (2019).
[4] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond conventional ferromagnetism and antiferromagnetism: A
phase with nonrelativistic spin and crystal rotation symmetry, Phys. Rev. X 12, 031042 (2022).
[5] T. Okugawa, K. Ohno, Y. Noda, and S. Nakamura,
Weakly spin-dependent band structures of antiferromagnetic perovskite LaMO3 (M=Cr, Mn, Fe), Journal
of Physics: Condensed Matter 30, 075502 (2018).
[6] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Spin current generation in organic
antiferromagnets, Nature Communications 10, 4305
(2019).
[7] H. Kusunose, R. Oiwa, and S. Hayami, Complete multipole basis set for single-centered electron systems, Journal of the Physical Society of Japan 89, 104704 (2020).
[8] L. Šmejkal, R. González-Hernández, T. Jungwirth, and
J. Sinova, Crystal time-reversal symmetry breaking and
spontaneous hall effect in collinear antiferromagnets,
Science Advances 6 (2020).
[9] M. Naka, Y. Motome, and H. Seo, Perovskite as a spin
current generator, Phys. Rev. B 103, 125114 (2021).
[10] I. I. Mazin, K. Koepernik, M. D. Johannes, R. GonzálezHernández, and L. Šmejkal, Prediction of unconventional magnetism in doped FeSb2 , Proceedings of the
National Academy of Sciences 118 (2021).
[11] I.
Mazin
(The
PRX
Editors),
Editorial:
Altermagnetism—a new punch line of fundamental magnetism, Phys. Rev. X 12, 040002 (2022).
[12] Y. Noda, K. Ohno, and S. Nakamura, Momentumdependent band spin splitting in semiconducting MnO2 :
a density functional calculation, Phys. Chem. Chem.
Phys. 18, 13294 (2016).
[13] K.-H. Ahn, A. Hariki, K.-W. Lee, and J. Kuneš, Antiferromagnetism in RuO2 as d-wave pomeranchuk instability, Phys. Rev. B 99, 184432 (2019).
[14] S. Hayami, Y. Yanagi, and H. Kusunose, Momentumdependent spin splitting by collinear antiferromagnetic
ordering, Journal of the Physical Society of Japan 88,
123702 (2019).
[15] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging research landscape of altermagnetism, Phys. Rev. X 12,
040501 (2022).
[16] P. G. Radaelli, A tensorial approach to ‘altermagnetism’
(2024), arXiv:2407.13548 [cond-mat.str-el].
[17] R. González-Hernández, L. Šmejkal, K. Výborný, Y. Yahagi, J. Sinova, T. Jungwirth, and J. Železný, Efficient electrical spin splitter based on nonrelativistic collinear antiferromagnetism, Phys. Rev. Lett. 126,
127701 (2021).
[18] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia,
and J. Liu, Multifunctional antiferromagnetic materials
with giant piezomagnetism and noncollinear spin cur-

rent, Nature Communications 12, 2846 (2021).
[19] P. A. McClarty and J. G. Rau, Landau theory of altermagnetism, Phys. Rev. Lett. 132, 176702 (2024).
[20] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Anomalous hall effect in κ-type
organic antiferromagnets, Phys. Rev. B 102, 075112
(2020).
[21] Z. Feng, X. Zhou, L. Šmejkal, L. Wu, Z. Zhu, H. Guo,
R. González-Hernández, X. Wang, H. Yan, P. Qin,
X. Zhang, H. Wu, H. Chen, Z. Meng, L. Liu, Z. Xia,
J. Sinova, T. Jungwirth, and Z. Liu, An anomalous hall
effect in altermagnetic ruthenium dioxide, Nature Electronics 5, 735 (2022).
[22] M. Naka, Y. Motome, and H. Seo, Anomalous hall effect in antiferromagnetic perovskites, Phys. Rev. B 106,
195149 (2022).
[23] L. Han, X. Fu, R. Peng, X. Cheng, J. Dai, L. Liu, Y. Li,
Y. Zhang, W. Zhu, H. Bai, Y. Zhou, S. Liang, C. Chen,
Q. Wang, X. Chen, L. Yang, Y. Zhang, C. Song, J. Liu,
and F. Pan, Electrical 180° switching of Néel vector
in spin-splitting antiferromagnet, Science Advances 10
(2024).
[24] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, Giant momentum-dependent spin splitting
in centrosymmetric low-Z antiferromagnets, Phys. Rev.
B 102, 014422 (2020).
[25] R. Hoyer, R. Jaeschke-Ubiergo, K.-H. Ahn, L. Šmejkal,
and A. Mook, Spontaneous crystal thermal hall effect in
insulating altermagnets (2024), arXiv:2405.05090 [condmat.mes-hall].
[26] T. Aoyama and K. Ohgushi, Piezomagnetic properties
in altermagnetic MnTe (2023), arXiv:2305.14786 [condmat.mtrl-sci].
[27] D. Kriegner, H. Reichlova, J. Grenzer, W. Schmidt,
E. Ressouche, J. Godinho, T. Wagner, S. Y. Martin,
A. B. Shick, V. V. Volobuev, G. Springholz, V. Holý,
J. Wunderlich, T. Jungwirth, and K. Výborný, Magnetic anisotropy in antiferromagnetic hexagonal mnte,
Phys. Rev. B 96, 214418 (2017).
[28] D. Kriegner, K. Výborný, K. Olejnı́k, H. Reichlová,
V. Novák, X. Marti, J. Gazquez, V. Saidl, P. Němec,
V. V. Volobuev, G. Springholz, V. Holý, and T. Jungwirth, Multiple-stable anisotropic magnetoresistance
memory in antiferromagnetic mnte, Nature Communications 7, 11623 (2016).
[29] R. M. Fernandes, V. S. de Carvalho, T. Birol, and R. G.
Pereira, Topological transition from nodal to nodeless
zeeman splitting in altermagnets, Phys. Rev. B 109,
024404 (2024).
[30] J. Ding, Z. Jiang, X. Chen, Z. Tao, Z. Liu, T. Li, J. Liu,
J. Sun, J. Cheng, J. Liu, Y. Yang, R. Zhang, L. Deng,
W. Jing, Y. Huang, Y. Shi, M. Ye, S. Qiao, Y. Wang,
Y. Guo, D. Feng, and D. Shen, Large band splitting in
g-wave altermagnet CrSb, Phys. Rev. Lett. 133, 206401
(2024).
[31] J. Krempaský, L. Šmejkal, and et. al., Altermagnetic
lifting of kramers spin degeneracy, Nature 626, 517
(2024).
[32] Z. Liu, M. Ozeki, S. Asai, S. Itoh, and T. Masuda, Chiral
split magnon in altermagnetic MnTe, Phys. Rev. Lett.
133, 156702 (2024).

35
[33] V. C. Morano, Z. Maesen, S. E. Nikitin, J. Lass,
D. G. Mazzone, and O. Zaharko, Absence of altermagnetic magnon band splitting in MnF2 (2024),
arXiv:2412.03545 [cond-mat.str-el].
[34] Y. Guo, H. Liu, O. Janson, I. C. Fulga, J. van den Brink,
and J. I. Facio, Spin-split collinear antiferromagnets: A
large-scale ab-initio study, Materials Today Physics 32,
100991 (2023).
[35] V. Leeb, A. Mook, L. Šmejkal, and J. Knolle, Spontaneous formation of altermagnetism from orbital ordering, Phys. Rev. Lett. 132, 236701 (2024).
[36] S. Giuli, C. Mejuto-Zaera, and M. Capone, Altermagnetism from interaction-driven itinerant magnetism,
Phys. Rev. B 111, L020401 (2025).
[37] R. Jaeschke-Ubiergo, V.-K. Bharadwaj, W. Campos,
R. Zarzuela, N. Biniskos, R. M. Fernandes, T. Jungwirth, J. Sinova, and L. Šmejkal, Atomic altermagnetism (2025), arXiv:2503.10797 [cond-mat.mtrl-sci].
[38] S.-W. Cheong and F.-T. Huang, Altermagnetism with
non-collinear spins, npj Quantum Materials 9 (2024).
[39] M. Hu, O. Janson, C. Felser, P. McClarty, J. van den
Brink, and M. G. Vergniory, Spin hall and edelstein effects in novel chiral noncollinear altermagnets (2024),
arXiv:2410.17993 [cond-mat.mtrl-sci].
[40] W. F. Brinkman and R. J. Elliott, Theory of Spin-Space
Groups, Proceedings of the Royal Society of London Series A 294, 343 (1966).
[41] W. Brinkman and R. J. Elliott, Space Group Theory
for Spin Waves, Journal of Applied Physics 37, 1457
(1966).
[42] D. B. Litvin, Spin point groups, Acta Crystallographica
Section A 33, 279 (1977).
[43] D. Litvin and W. Opechowski, Spin groups, Physica 76,
538 (1974).
[44] A. Corticelli, R. Moessner, and P. A. McClarty, Spinspace groups and magnon band topology, Phys. Rev. B
105, 064430 (2022).
[45] J. Yang, Z.-X. Liu, and C. Fang, Symmetry invariants
and classes of quasiparticles in magnetically ordered systems having weak spin-orbit coupling, Nature Communications 15 (2024).
[46] Y. Jiang, Z. Song, T. Zhu, Z. Fang, H. Weng, Z.-X.
Liu, J. Yang, and C. Fang, Enumeration of spin-space
groups: Toward a complete description of symmetries
of magnetic orders, Phys. Rev. X 14, 031039 (2024).
[47] X. Chen, J. Ren, Y. Zhu, Y. Yu, A. Zhang, P. Liu, J. Li,
Y. Liu, C. Li, and Q. Liu, Enumeration and representation theory of spin space groups, Phys. Rev. X 14,
031038 (2024).
[48] Z. Xiao, J. Zhao, Y. Li, R. Shindou, and Z.-D. Song,
Spin space groups: Full classification and applications,
Phys. Rev. X 14, 031037 (2024).
[49] P. Liu, J. Li, J. Han, X. Wan, and Q. Liu, Spin-group
symmetry in magnetic materials with negligible spinorbit coupling, Phys. Rev. X 12, 021016 (2022).
[50] H. Schiff, A. Corticelli, A. Guerreiro, J. Romhányi, and
P. McClarty, The crystallographic spin point groups and
their representations, SciPost Phys. 18, 109 (2025).
[51] R. Jaeschke-Ubiergo, V. K. Bharadwaj, T. Jungwirth,
L. Šmejkal, and J. Sinova, Supercell altermagnets, Phys.
Rev. B 109, 094425 (2024).
[52] C.-C. Wei, E. Lawrence, A. Tran, and H. Ji, Crystal
chemistry and design principles of altermagnets, ACS
Organic & Inorganic Au 4, 604 (2024).

[53] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F.
Agterberg, Minimal models for altermagnetism, Phys.
Rev. B 110, 144412 (2024).
[54] M. I. Aroyo, J. M. Perez-Mato, C. Capillas,
E. Kroumova, S. Ivantchev, G. Madariaga, A. Kirov,
and H. Wondratschek, Bilbao crystallographic server:
I. databases and crystallographic computing programs,
Zeitschrift für Kristallographie - Crystalline Materials
221, 15 (2006).
[55] S. Hayami, Y. Yanagi, and H. Kusunose, Bottom-up
design of spin-split and reshaped electronic band structures in antiferromagnets without spin-orbit coupling:
Procedure on the basis of augmented multipoles, Phys.
Rev. B 102, 144441 (2020).
[56] S. Hayami and H. Kusunose, Unified description of electronic orderings and cross correlations by complete multipole representation, Journal of the Physical Society of
Japan 93, 072001 (2024).
[57] M.-T. Suzuki, T. Koretsune, M. Ochi, and R. Arita,
Cluster multipole theory for anomalous hall effect in
antiferromagnets, Phys. Rev. B 95, 094406 (2017).
[58] P. Toledano and J. Toledano, Landau Theory Of
Phase Transitions, The: Application To Structural, Incommensurate, Magnetic And Liquid Crystal Systems,
World Scientific Lecture Notes In Physics (World Scientific Publishing Company, 1987).
[59] H. A. Jahn, Note on the Bhagavantam–Suranarayana
method of enumerating the physical constants of crystals, Acta Crystallographica 2, 30 (1949).
[60] S. V. Gallego, J. Etxebarria, L. Elcoro, E. S. Tasci, and
J. M. Perez-Mato, Automatic calculation of symmetryadapted tensors in magnetic and non-magnetic materials: a new tool of the Bilbao Crystallographic Server,
Acta Crystallographica Section A 75, 438 (2019).
[61] R. D. Gonzalez Betancourt, J. Zubáč, R. GonzalezHernandez, K. Geishendorf, Z. Šobáň, G. Springholz,
K. Olejnı́k, L. Šmejkal, J. Sinova, T. Jungwirth, S. T. B.
Goennenwein, A. Thomas, H. Reichlová, J. Železný, and
D. Kriegner, Spontaneous anomalous hall effect arising
from an unconventional compensated magnetic phase in
a semiconductor, Phys. Rev. Lett. 130, 036702 (2023).
[62] S. Greenwald, The antiferromagnetic structure deformations in CoO and MnTe, Acta Crystallographica 6, 396
(1953).
[63] M. Podgorny and J. Oleszkiewicz, Electronic structure
of antiferromagnetic mnte, Journal of Physics C: Solid
State Physics 16, 2547 (1983).
[64] E. Przedziecka, E. Kamiska, E. Dynowska, R. Butkut,
W. Dobrowolski, H. Kpa, R. Jakiela, M. Aleszkiewicz,
E. Usakowska, E. Janik, and J. Kossut, Preparation and
characterization of hexagonal MnTe and ZnO layers,
Physica Status Solidi C Current Topics 2, 1218 (2005).
[65] T. Komatsubara, M. Murakami, and E. Hirahara, Magnetic properties of manganese telluride single crystals,
Journal of the Physical Society of Japan 18, 356 (1963).
[66] W. Szuszkiewicz, B. Hennion, B. Witkowska,
E. Lusakowska, and A. Mycielski, Neutron scattering study of structural and magnetic properties of
hexagonal MnTe, Physica Status Solidi (c) 2, 1141
(2005).
[67] S. Bhowal and N. A. Spaldin, Ferroically ordered magnetic octupoles in d-wave altermagnets, Phys. Rev. X
14, 011019 (2024).
[68] Kunitomi, Nobuhiko, Hamaguchi, Yoshikazu, and An-

36
zai, Shuichiro, Neutron diffraction study on manganese
telluride, J. Phys. France 25, 568 (1964).
[69] M. Roig, Y. Yu, R. C. Ekman, A. Kreisel, B. M.
Andersen, and D. F. Agterberg, Quasi-symmetry constrained spin ferromagnetism in altermagnets (2024),
arXiv:2412.09338 [cond-mat.str-el].
[70] R.-C. Xiao, H. Li, H. Han, W. Gan, M. Yang, D.-F.
Shao, S.-H. Zhang, Y. Gao, M. Tian, and J. Zhou,
Anomalous-hall Néel textures in altermagnetic materials (2025), arXiv:2411.10147 [cond-mat.mtrl-sci].
[71] L. Attias, A. Levchenko, and M. Khodas, Intrinsic
anomalous hall effect in altermagnets, Physical Review
B 110 (2024).
[72] T. Chatterji and T. C. Hansen, Magnetoelastic effects
in jahn–teller distorted CrF2 and CuF2 studied by neutron powder diffraction, Journal of Physics: Condensed
Matter 23, 276007 (2011).
[73] J. W. Cable, M. K. Wilkinson, and E. O. Wollan, Neutron diffraction studies of antiferromagnetism in CrF2
and CrCl2 , Phys. Rev. 118, 950 (1960).
[74] P. Fischer, W. Hälg, D. Schwarzenbach, and
H. Gamsjäger, Magnetic and crystal structure of
copper(ii) fluoride, Journal of Physics and Chemistry
of Solids 35, 1683 (1974).
[75] I. V. Solovyev, Magneto-optical effect in the weak ferromagnets LaMO3 (M= Cr, Mn, and Fe), Phys. Rev. B
55, 8060 (1997).
[76] K. Yamada, E. Kudo, Y. Endoh, Y. Hidaka, M. Oda,
M. Suzuki, and T. Murakami, The effect of the heat
treatments on the antiferromagnetism in La2 CuO4−δ
single crystals, Solid State Communications 64, 753
(1987).
[77] D. Vaknin, S. K. Sinha, D. E. Moncton, D. C. Johnston,
J. M. Newsam, C. R. Safinya, and H. E. King, Antiferromagnetism in La2 CuO4−y , Phys. Rev. Lett. 58, 2802
(1987).
[78] J. D. Jorgensen, B. Dabrowski, S. Pei, D. G. Hinks,
L. Soderholm, B. Morosin, J. E. Schirber, E. L. Venturini, and D. S. Ginley, Superconducting phase of
La2 CuO4+δ : A superconducting composition resulting
from phase separation, Phys. Rev. B 38, 11337 (1988).
[79] M. A. Kastner, R. J. Birgeneau, G. Shirane, and Y. Endoh, Magnetic, transport, and optical properties of
monolayer copper oxides, Rev. Mod. Phys. 70, 897
(1998).
[80] M. Reehuis, C. Ulrich, K. Prokeš, A. Gozar, G. Blumberg, S. Komiya, Y. Ando, P. Pattison, and B. Keimer,
Crystal structure and high-field magnetism of La2 CuO4 ,
Phys. Rev. B 73, 144513 (2006).
[81] C. Lane, J. W. Furness, I. G. Buda, Y. Zhang, R. S.
Markiewicz, B. Barbiellini, J. Sun, and A. Bansil, Antiferromagnetic ground state of La2 CuO4 : A parameterfree ab initio description, Phys. Rev. B 98, 125140
(2018).
[82] T. Thio, T. R. Thurston, N. W. Preyer, P. J. Picone,
M. A. Kastner, H. P. Jenssen, D. R. Gabbe, C. Y. Chen,
R. J. Birgeneau, and A. Aharony, Antisymmetric exchange and its influence on the magnetic structure and
conductivity of La2 CuO4 , Phys. Rev. B 38, 905 (1988).
[83] T. Thio and A. Aharony, Weak ferromagnetism and
tricriticality in pure la2 cuo4 , Phys. Rev. Lett. 73, 894
(1994).
[84] W. H. Baur, Uber die Verfeinerung der Kristallstrukturbestimmung einiger Vertreter des Rutiltyps. II. Die

Difluoride von Mn, Fe, Co, Ni und Zn, Acta Crystallographica 11, 488 (1958).
[85] W. H. Baur and A. A. Khan, Rutile-type compounds.
IV. SiO2 , GeO2 and a comparison with other rutile-type
structures, Acta Crystallographica Section B 27, 2133
(1971).
[86] J. W. Stout and H. E. Adams, Magnetism and the third
law of thermodynamics. the heat capacity of manganous
fluoride from 13 to 320°K., Journal of the American
Chemical Society 64, 1535 (1942).
[87] I. de P. R. Moreira, R. Dovesi, C. Roetti, V. R.
Saunders, and R. Orlando, Ab initio study of MF2
(M=Mn,Fe,Co,Ni) rutile-type compounds using the periodic unrestricted hartree-fock approach, Phys. Rev. B
62, 7816 (2000).
[88] S. López-Moreno, A. H. Romero, J. Mejı́a-López, and
A. Muñoz, First-principles study of pressure-induced
structural phase transitions in MnF2 , Phys. Chem.
Chem. Phys. 18, 33250 (2016).
[89] M. I. Aroyo, A. Kirov, C. Capillas, J. M. Perez-Mato,
and H. Wondratschek, Bilbao Crystallographic Server.
II. Representations of crystallographic point groups and
space groups, Acta Crystallographica Section A 62, 115
(2006).
[90] R. A. Erickson, Neutron diffraction studies of antiferromagnetism in manganous fluoride and some isomorphous compounds, Phys. Rev. 90, 779 (1953).
[91] O. Nikotin, P. A. Lindgård, and O. W. Dietrich, Magnon
dispersion relation and exchange interactions in MnF2 ,
Journal of Physics C: Solid State Physics 2, 1168 (1969).
[92] F. J. Morin, Magnetic susceptibility of αFe2 O3 and
αFe2 O3 with added titanium, Phys. Rev. 78, 819
(1950).
[93] I. Dzyaloshinsky, A thermodynamic theory of “weak”
ferromagnetism of antiferromagnetics, Journal of
Physics and Chemistry of Solids 4, 241 (1958).
[94] T. Moriya, Anisotropic superexchange interaction and
weak ferromagnetism, Phys. Rev. 120, 91 (1960).
[95] A. H. Hill, F. Jiao, P. G. Bruce, A. Harrison, W. Kockelmann, and C. Ritter, Neutron diffraction study of mesoporous and bulk hematite, α-Fe2 O3 , Chemistry of Materials 20, 4891 (2008).
[96] T. Dannegger, A. Deák, L. Rózsa, E. Galindez-Ruales,
S. Das, E. Baek, M. Kläui, L. Szunyogh, and U. Nowak,
Magnetic properties of hematite revealed by an ab initio
parameterized spin model, Phys. Rev. B 107, 184426
(2023).
[97] R. Lebrun, A. Ross, O. Gomonay, V. Baltz, U. Ebels,
A.-L. Barra, A. Qaiumzadeh, A. Brataas, J. Sinova, and
M. Kläui, Long-distance spin-transport across the morin
phase transition up to room temperature in ultra-low
damping single crystals of the antiferromagnet α-Fe2 O3 ,
Nature Communications 11 (2020).
[98] T. S. Santoshi, S. Bharadwaj, M. C. Varma, V. Dhand,
and G. Choudary, Structural and magnetic properties of α-Fe2 O3 with lithium ferrite prepared using coprecipitation method and annealed at different temperatures, Chemical Physics Impact 9, 100717 (2024).
[99] E. F. Galindez-Ruales, L. Šmejkal, S. Das, E. Baek,
C. Schmitt, F. Fuhrmann, A. Ross, R. GonzálezHernández, A. Rothschild, J. Sinova, C. Y. You,
G. Jakob, and M. Kläui, Altermagnetism in the hopping
regime (2024), arXiv:2310.16907 [cond-mat.mtrl-sci].
[100] R. Hoyer, P. P. Stavropoulos, A. Razpopov, R. Valentı́,

37
L. Šmejkal, and A. Mook, Altermagnetic splitting of
magnons in hematite (α-fe2 o3 ) (2025), arXiv:2503.11623
[cond-mat.str-el].
[101] Y. Yu, M. B. Lyngby, T. Shishidou, M. Roig, A. Kreisel,
M. Weinert, B. M. Andersen, and D. F. Agterberg, Oddparity magnetism driven by antiferromagnetic exchange
(2025), arXiv:2501.02057 [cond-mat.str-el].
[102] E. Wigner, Group Theory: And its Application to the
Quantum Mechanics of Atomic Spectra, Pure and applied physics (Elsevier Science, 2012).
[103] J. O. Dimmock, Representation Theory for Nonunitary Groups, Journal of Mathematical Physics 4, 1307
(2004).
[104] M. Damnjanović, Symmetry in Quantum NonRelativistic Physics (2014).
[105] C. J. Bradley and A. P. Cracknell, The mathematical
theory of symmetry in solids. Representation theory for
point groups and space groups (Oxford University Press,
1972).
[106] H. T. Stokes, D. M. Hatch, and J. S. Kim, Images of
physically irreducible representations of the 230 space
groups, Acta Crystallographica Section A 43, 81 (1987).
[107] W. Hergert and R. Geilhufe, Group Theory in Solid

State Physics and Photonics: Problem Solving with
Mathematica (Wiley, 2018).
[108] M. Damnjanović and M. Vujičic, Subgroups of weakdirect products and magnetic axial point groups, Journal of Physics A General Physics 14, 1055 (1981).
[109] D. Litvin, Magnetic Group Tables (International Union
of Crystallography, 2014) pp. 1055–1063.
[110] V. Petřı́ček, J. Fuksa, and M. Dušek, Magnetic space
and superspace groups, representation analysis: competing or friendly concepts?, Acta Crystallographica
Section A 66, 649 (2010).
[111] S. Keppeler, Birdtracks for SU(N), SciPost Phys. Lect.
Notes , 3 (2018).
[112] M. Damnjanović and I. Milošević, Modified group projector technique: induced representations, Journal of
Physics A: Mathematical and General 28, 1669 (1995).
[113] G. F. Koster, Matrix elements of symmetric operators,
Phys. Rev. 109, 227 (1958).
[114] J.-Q. Chen, M.-J. Gao, and G.-Q. Ma, The representation group and its application to space groups, Rev.
Mod. Phys. 57, 211 (1985).


<!-- extracted via pdftotext | arxiv:1908.00986 | 2026-07-19T04:40:36Z -->
Symmetry breaking and skyrmionic transport in twisted bilayer graphene
Shubhayu Chatterjee,1 Nick Bultinck,1 and Michael P. Zaletel1

arXiv:1908.00986v2 [cond-mat.str-el] 28 Apr 2020

1

Department of Physics, University of California, Berkeley, California 94720, USA

Motivated by recent low-temperature magnetoresistance measurements in twisted bilayer
graphene aligned with hexagonal boron-nitride substrate, we perform a systematic study of possible symmetry breaking orders in this device at a filling of two electrons per moiré unit cell. We
find that the surprising non-monotonic dependence of the resistance on an out-of-plane magnetic
field is difficult to reconcile with particle-hole charge carriers from the low-energy bands in symmetry
broken phases. We invoke the non-zero Chern numbers of the twisted bilayer graphene flat bands to
argue that skyrmion textures provide an alternative for the dominant charge carriers. Via an effective field-theory for the spin degrees of freedom, we show that the effect of spin Zeeman splitting on
the skyrmion excitations provides a possible explanation for the non-monotonic magnetoresistance.
We suggest several experimental tests, including the functional dependence of the activation gap on
the magnetic field, for our proposed correlated insulating states at different integer fillings. We also
discuss possible exotic phases and quantum phase transitions that can arise via skyrmion-pairing
on doping such an insulator.

I.

INTRODUCTION

A series of recent experimental breakthroughs has uncovered surprising and fascinating correlated electron
phenomena in two-dimensional van der Waals moiré
materials. Transport experiments on twisted bilayer
graphene [1–3], ABC trilayer graphene on hexagonal
boron-nitride (hBN) [4, 5], and twisted double bilayer
graphene [6–8] show evidence of insulating states around
charge neutrality at electron fillings for which no singleparticle band-gap is expected. To make the story even
more interesting, superconducting domes flanking some
of these insulating states were observed [2, 3, 6, 8, 9]. In
Refs. [10–12], spatially resolved properties of the insulating states were studied using scanning tunneling microscopy (STM) experiments. Recently, transport experiments were also performed at larger temperatures, and
revealed an interesting broad temperature range with a
large and linearly increasing resistivity [13, 14].
The origin of the insulating and superconducting states
can be traced back to the presence of bands with vanishing bandwidth in the mini- or moiré Brillouin zone. In
twisted bilayer graphene (tBLG), such flat mini-bands
were predicted to occur at special ‘magic’ twist angles
between the top and bottom graphene layer [15]; an exact flat band criterion was later obtained in Ref. [16] for
a chiral approximation of the tBLG continuum model
[15, 17, 18]. In ABC trilayer graphene on hBN and
twisted double bilayer graphene, similar flat mini-bands
around charge neutrality can be obtained by applying a
suitable displacement field [4, 19, 20]. Interestingly, the
flat bands often also have non-trivial topological properties. For instance in tBLG, the flat bands have non-trivial
fragile topology protected by the space group symmetries [21–24]. In devices which have isolated flat bands,
one generally finds broad parameter regimes where these
bands have non-zero Chern number [19, 20, 25–28].
In this work, we focus on flat bands which have a gap
at the charge neutrality point (CNP). This is motivated
by the experiments of Refs. [29, 30], where the Dirac

cones in the tBLG flat bands are gapped by the C2v symmetry breaking AB-sublattice splitting induced by the
hBN substrate. Although we focus on the case where the
bandgap at charge neutrality has a trivial single-particle
origin, most of our results can also be applied to meanfield band structures where the gap at the CNP results
from spontaneous symmetry breaking induced by electron interactions. In tBLG, C2v T symmetry (with T
being time-reversal) needs to be spontaneously broken
in order to generate a mean-field gap at charge neutrality. Self-consistent Hartree-Fock studies have found that
this indeed happens for certain interaction strengths and
twist angles [3, 26, 31]. It was found that the C2v T symmetry breaking self-consistent Hartree-Fock solutions are
very susceptible to C3v breaking strain [31], an observation which agrees with the STM and transport experiments [32].
Our main focus is tBLG with a single-particle gap at
charge neutrality at electron filling ν = 2, i.e. at a doping of two electrons per moiré unit cell with respect to
charge neutrality. Based on a phenomenological meanfield analysis, we argue that the magnetoresistance measurements of Ref. [29] impose very non-trivial constraints
on the state that is realized at ν = 2. We analyse the different possible symmetry breaking orders and find that
(almost) all of them are hard to reconcile with the transport measurements of Ref. [29], given that we assume
the charge carriers to be conventional particle-hole excitations. However, because of the non-trivial topology
of the flat bands, skyrmions textures in a spin-polarized
flat band carry electric charge [33]. We study the potential role of skyrmions as the dominant charge carriers
and find that they provide a natural explanation of the
experimental data of Refs. [29, 30]. We therefore posit
that skyrmions contribute to transport in tBLG, and we
provide experimentally falsifiable predictions for the activation gap as a function of out-of-plane magnetic field for
insulators at ν = 2, 3 to test our assertion. Towards the
end of the manuscript, we speculate on skyrmion-pairing
and possible connections to superconductivity.

2
II.

MAGIC-ANGLE TWISTED BILAYER
GRAPHENE ALIGNED WITH HBN

We consider tBLG at the first magic angle θ ≈ 1.05◦
[15], encapsulated on both sides by a hBN substrate. If
hBN is sufficiently aligned with graphene, it induces a
non-negligible sublattice splitting ∆ σ z , which results in
a C2 T breaking mass term at the Dirac points [34–37].
Further, because of the mismatch in lattice constant between graphene and hBN, a second moiré pattern arises
[38]. As the rotation angle between graphene and hBN
decreases, both the induced Dirac mass term and the
strength of the second moiré pattern increase. There is a
regime where the hBN induced moiré pattern can be neglected, while there is nonetheless a sizable Dirac mass.
Here, we consider the situation where the top graphene
layer and hBN substrate are in this regime, while the
bottom graphene layer is sufficiently unaligned with hBN
and is therefore not affected by the substrate. We will
often use a hBN induced sublattice splitting of 15 meV,
which is expected to be a good estimate based on the
findings of Ref. [39]. We refer to Appendix A for a detailed discussion of the moiré Hamiltonian used in this
work.
In Refs. [27, 28], it was found that a non-zero sublattice splitting on one side of magic-angle tBLG gaps out all
Dirac cones of the moiré Hamiltonian. Because the two
Dirac cones in a single-valley moiré Hamiltonian, shown
in Fig. 1(a), originate from the two different graphene
layers, this is a consequence of the inter-layer coupling.
Ignoring spin, the single-valley moiré Hamiltonian with
sublattice splitting on one layer has two isolated flat
bands, as shown in Fig. 1(b). The Chern numbers of
these bands were calculated in Refs. [27, 28], and found
to be C = ±1. Note that once we know the Chern number C of one band, all the other Chern numbers are fixed.
This is because the total Chern number in one valley always adds up to zero (as long as the sublattice splitting is
not strong enough to mix the flat bands with the dispersive bands), and because the two valleys are interchanged
by time-reversal symmetry, which changes the sign of the
Chern number. With positive sublattice splitting ∆ on
one of the graphene layers, the band above charge neutrality in valley +, i.e. the valley at the K points of the
mono-layer graphene Brillouin zone, has C = −1.
In Refs. [29, 30], spontaneous time-reversal symmetry
breaking at ν = 3 was observed in a magic-angle tBLG
device where one of the graphene layers is nearly aligned
with hBN. In particular, Ref. [29] reported a rotational
mismatch between the top graphene layer and the hBN
substrate of ≈ 0.83◦ . In both experiments, the spontaneous time-reversal breaking is accompanied by a nonzero anomalous Hall effect. On top of this, ref. [30] observed insulating behavior at ν = 3, and a corresponding
quantized Hall conductance σxy = ±e2 /h. Because of
the non-zero Chern numbers of the flat bands with hBN
alignment, these experimental observations at ν = 3 can
be naturally explained if the Coulomb interactions cause

the electrons to spontaneously polarize into one valley
[27, 28]; complete spin polarization in addition to valley
polarization can lead to an insulator with quantized σxy .
In this work we focus on the experimental findings for the
same devices at filling ν = 2. At this filling, no anomalous Hall effect was observed, but a clear resistance peak
is nevertheless present [29, 30]. Although an activation
gap is yet to be observed at ν = 2 in transport measurements, this resistance peak hints at the possibility of a
true insulating state at zero temperature. Here we assume that such an insulating state is indeed realized at
lower temperatures.
Before going into the interaction effects that stabilize
the putative insulator at ν = 2, we first discuss one last
single-particle effect. In Ref. [29], it was observed that
applying a displacement field along one direction destroys
the resistance peak at ν = 2, while this peak is almost
insensitive to a displacement field applied in the other
direction. To understand this behavior, we studied the
effect of a non-zero potential energy difference between
top and bottom graphene layers on the flat bands. In
Fig. 1 (c), we show the density of states (DOS) of the
flat bands with a sublattice splitting ∆t = 15 meV, and a
potential energy difference ∆U = Ut −Ub of 0, 50 and −50
meV. We see that for ∆U = 50 meV, there is only a small
change in the conduction band DOS as compared to the
case when ∆U = −50 meV. Fig. 1 clearly shows that for
negative ∆U , the conduction band DOS decreases more,
and spreads over a larger energy window as function of
|∆U |. At the very least, this dependence of the DOS on
displacement field, and in particular on the sign of ∆U ,
is consistent with the scenario that the resistance peak
at ν = 2 is attributed to a correlated insulator, because
a lower DOS and a larger bandwidth reduce the effect of
electron interactions.

III.

POSSIBLE SYMMETRY BREAKING
ORDERS AT ν = 2

To address the nature of the correlated insulator observed at ν = 2, we follow the phenomenological approach of Ref. [28] and identify the symmetry breaking orders that are compatible with the experimental
observations (for simplicity, we neglect spatial symmetry breaking on the moiré scale). We note that recently
a similar phenomenological approach was used to distinguish different pairing order parameters in tBLG and
twisted double bilayer graphene [40, 41]. The dominant
terms in the Hamiltonian are U(2)+ ×U(2)− symmetric,
where the ± subscript refers to the valley quantum number. The U(2)+ ×U(2)− symmetry consists of overall
charge conservation, valley-charge conservation, and independent SU(2) spin rotations in each valley. We write
its corresponding Lie algebra as 1, τ z , s and τ z s, where
τ i and si are the Pauli matrices acting respectively on
the valley and spin indices. The total Hamiltonian also
contains terms that break the SU(2)+ ×SU(2)− subgroup

energy (meV)

3
30
20
10
0
10
20
30

t = 0,

U = 0 (meV)

K+ M K

30
20
10
0
10
20
30

M

(a)

DOS (meV 1AM 1)

3.0
2.5
2.0
1.5
1.0
0.5
0.0
10.0

t = 15,

U = 0 (meV)
K−

Γ
K+
K+ M K

2.5 0.0 2.5
Energy (meV)

5.0

(a)

7.5

10.0

1
−1
µ

0
0

−|mK |

(b)

5.0

−1
1

mK+

M

U = 50 meV
U = 0 meV
U = 50 meV

7.5

mK− = −mK+

|mK |

(b)

FIG. 2: (a) Mini-Brillouin zone with the Dirac cones at the K+
and K− points coming from the IVC insulator order parameter
M x (k)τ x + M y (k)τ y . Both Dirac cones have the same chirality.
The mass terms at K+ and K− , which have opposite signs, come
from the flat band dispersion: mK± = ±(ε+,K+ − ε+,K− )/2. (b)
Effect of a fictitious term µτ z on the IVC insulator mean-field
Hamiltonian. Tuning µ from minus infinity to plus infinity
induces two Chern number changing transitions, where the Chern
number of the valence (conduction) band changes from 1 (−1) to
0, and from 0 to −1 (1) (for positive ∆t ). In the figure, above the
µ axis we schematically show the valence and conduction bands
with their respective Chern number.

(c)
FIG. 1: (a) Band spectrum around charge neutrality of the
single-valley tBLG moiré Hamiltonian at the first magic angle
θ ≈ 1.05◦ . At the K points in the mini-Brillouin zones, Dirac
cones protected by C2v T are present. (b) With a sublattice
splitting ∆t of 15 meV on the top graphene layer, induced by
alignment with the hBN substrate, the Dirac cones acquire a
mass. The resulting isolated valence and conduction bands carry
non-zero Chern number |C| = 1. (c) The effect on the flat band
density-of-states (DOS) of a potential energy difference ∆U
between top and bottom graphene layers as a result of non-zero
displacement field, for ∆t = 15 meV. AM is the area of the moiré
unit cell. The valence (conduction) band DOS is strongly affected
by positive (negative) ∆U .

down to the physical SU(2) spin rotation group, but they
operate at much lower energy scales. We will ignore these
terms for now, and discuss them in more detail in the next
section. We can organize the fifteen order parameters
τ i sj into three different multiplets under U(2)+ ×U(2)−
[28]: (1) τ z , (2) (τ x/y , τ x/y s) and (3): (s, τ z s).
The order parameter τ z corresponds to a spin singlet,
valley-polarized insulator where all electrons occupy the
same valley. This possibility can readily be excluded,
since in this case the system would be an anomalous
Hall insulator with σxy = ±2e2 /h. However, no sign
of non-zero Hall conductivity at zero magnetic field was
observed at ν = 2 [29].
The second possibility is that the ground state corresponds to an intervalley coherent (IVC) state, with order parameter multiplet (τ x/y , τ x/y s). Let us pick the
τ x , τ y order parameters, and write the mean field Hamiltonian for the four bands above charge neutrality (includP
ing spin) as HM F = k c†k,τ,s [hk ]τ,s;τ 0 ,s0 ck,τ 0 ,s0 , where k
lies in the mini-Brillouin zone (MBZ). For the IVC state,
restricting to an out-of-plane magnetic field (Bk = 0),

hk =

(ε+,k − ε−,k ) z
τ ⊗ s0 + M x (k)τ x ⊗ s0 + M y (k)τ y ⊗ s0
2
µB gs B⊥ 0
µB gv (k)B⊥ z
τ ⊗ s0 −
τ ⊗ sz ,
(1)
−
2
2

where ετ,k is the band energy in valley τ . Note that
we have dropped an unimportant term proportional to
the identity. The first term on the second line in Eq.
(1) is the valley Zeeman term, with µB the Bohr magneton, which describes the coupling between an out-ofplane magnetic field B⊥ and the orbital magnetic moment of the electrons [42–44]. The last term is the conventional spin-Zeeman term. Time reversal acts on the
Hamiltonian in Eq. (1) as τ x K, where K means complex conjugation. Let us first analyze this mean field
Hamiltonian for B⊥ = 0. Because the flat bands above
charge neutrality have Chern number C = ±1, we know
that M (k) = M x (k) + iM y (k) has at least two nodes
in the mini-Brillouin zone with the same phase winding
[27, 45] (see also [46]). Assuming the minimal scenario
with only two nodes is realized, C3v and time-reversal
symmetry dictate that these nodes are located either at
the K+ and K− points of the mini-Brillouin zone, or
both at the Γ point. Since the IVC mass M set by the
Coulomb scale (≈ 20 meV) is expected to be much larger
than the non-interacting bandwidth (≈ 3 meV), the minimum band gap corresponds to the nodes of M (k) in the
MBZ. Therefore, when the nodes are at the K points,
the band gap of the mean field Hamiltonian is given by
|ε+,K+ − ε−,K+ | = |ε+,K+ − ε+,K− |, where we have used
ε−,k = ε+,−k as follows from time-reversal symmetry.
We will refer to this possibility as the IVC insulator. If
the nodes are both at Γ, then the mean field Hamiltonian
is a semi-metal, which we will refer to as the IVC semimetal. Let us first elaborate on the topological properties of the gapped bands of the IVC insulator. Because

4
↓

↓
↑

↑, ↓

∆SZ

∆V Z ↑

∆SZ
∆V Z

↓

↑, ↓

↓
↑

(a)

FIG. 3: Schematic charge gap ∆c as a function of B⊥ for the
IVC-I state, neglecting the small spin Zeeman effect. ∆c would
increase for uniform non-zero MIV C (k). This is not allowed by
the opposite Chern numbers of the two valleys and hence ∆c
decreases at one node of MIV C (k).

the nodes of ∆(k) have the same winding, the resulting Dirac cones in the mean field Hamiltonian have the
same chirality. The mass terms mK+ τ z and mK− τ z at
the K+ and K− points coming from the flat-band dispersion have opposite sign, as can easily be seen from
mK+ = (ε+,K+ − ε−,K+ )/2 = (ε+,K+ − ε+,K− )/2 and
mK− = (ε+,K− − ε−,K− )/2 = (ε+,K− − ε+,K+ )/2. So we
conclude that the bands of the IVC insulator mean field
Hamiltonian have zero Chern number. This can also be
seen by adding a fictitious term µτ z to the Hamiltonian
in Eq. (1). Tuning µ from minus infinity to plus infinity
induces two Chern number changing transitions, where
at each transition the Chern number changes by one at
a Dirac cone located at one of the nodes of M (k). This
is shown schematically in Fig. 2 (b).
Now we investigate the consequences of turning on a
non-zero out-of-plane magnetic field. We first consider
the IVC insulator. For non-zero B⊥ , the valley-Zeeman
term starts to compete with the mass terms mK+ τ z and
mK− τ z . Since mK+ = −mK− , the valley Zeeman effect
must decrease the gap at either K+ or K− (and increase
the gap at the other point, see Fig. 3), regardless of the
sign of the perpendicular magnetic field. At the twist
angle used in Ref. [29], and with ∆t = 15 meV, the magnitude of gv (k) is approximately 15 at the mini-Brillouin
zone K points [28]. Because of this, we can safely ignore
the spin-Zeeman term. From the mean-field Hamiltonian
Eq. (1), we see that the band gap of the IVC insulator
is given by
∆IV C−I (B⊥ ) = 2|mK | − µB |gv (K)B⊥ |

(2)

Irrespective of the sign of B⊥ , the band gap ∆IV C−I
closes when µB |g(K)B⊥ |/2 = |mK |, where |mK | =
|mK+ | = |mK− |. Given that |mK | ≈ 1.5 meV, we
find that the bandgap of the IVC insulator closes when
B⊥ ≈ 3 − 4 T. However, this behavior, schematically
depicted in Fig. 3, is difficult to reconcile with the experimental findings of Ref. [29] as the magnetoresistance
measurements show an increase in resistivity at ν = 2

(b)

↑

(c)

FIG. 4: Band spectrum around Γ of the IVC semi-metal
mean-field Hamiltonian, corresponding to Eq. (1) with both
nodes of M (k) located at Γ. (a) Band spectrum at B⊥ = 0. (b)
With non-zero B⊥ , the band spectrum develops a Fermi surface if
the spin-Zeeman splitting ∆SZ = |gs µB B⊥ | is greater than the
valley-Zeeman splitting ∆V Z = |gv (0)µB B⊥ |. (c) The opposite
case compared to (b). Now the valley-Zeeman splitting is larger
than the spin-Zeeman splitting, resulting in a gapped band
spectrum.

as a function of out-of-plane magnetic field, with a resistance peak around 6 T.
For the IVC semi-metal, the valley-Zeeman term will
generate a mass term at Γ. The spin-Zeeman term
lifts the spin degeneracy, which makes the valence and
conduction bands overlap around Γ. The net effect
of the out-of-plane magnetic field depends on the sign
of gs − gv (0), where gv (0) is the orbital g-factor at
Γ. As we show in Fig. 4, if the spin-Zeeman splitting
∆SZ (B⊥ ) = |gs µB B⊥ | is bigger than the valley-Zeeman
splitting ∆V Z (B⊥ ) = |gv (0)µB B⊥ |, a Fermi surface appears around Γ. If ∆V Z (B⊥ ) > ∆SZ (B⊥ ), then the
IVC semi-metal develops an energy gap at Γ. We find
that gv (0) depends sensitively on twist angle, lattice relaxation and sublattice splitting. However, generically
gv (0) > gs , such that an out-of-plane magnetic field creates a non-zero energy gap. The IVC semi-metal is thus
consistent with the magnetoresistance measurements of
Ref. [29]. However, we expect such a phase to be energetically unfavorable for two reasons. First, the Fermi surface is not entirely gapped out at B⊥ = 0, which means
that the fermions gain less correlation energy compared
to other order parameters that lead to a fully gapped
spectrum. Second, a double vortex in M (k) costs twice
the energy of two Rsingle vortices from a symmetry allowed
term of the form k |∇k M (k)|2 in the effective action, as
the latter endows a vortex with an energy cost proportional to the square of its winding number. Therefore,
below we will focus on the possibility of an insulating
state at ν = 2.
Let us also briefly comment on the possibility that
C3v and/or time-reversal are spontaneously broken. In
that case, the nodes of M (k) appear at generic positions
in the mini-Brillouin zone, and will be gapped out by
the mass terms (ε+,k − ε−,k )τ z /2 at the locations of the
nodes. For non-zero B⊥ , both the valley-Zeeman and the
spin-Zeeman terms will compete with these mass terms,
similar to the case when the nodes are at the K-points,
as long as time-reversal is preserved and hence the gap
decreases for either direction of B⊥ . However, if M (k)

5
spontaneously breaks time-reversal and C3v , it is possible
for both mass terms to have the same sign at the location
of the nodes. In this case, the band gap will decrease for
one direction of B⊥ , but increase for the other direction.
So this scenario could in principle explain the magnetoresistance measurements of Ref. [29], but it requires
strong breaking of valley-U(1), C3v and time-reversal. It
can readily be identified in experiments by doing magnetoresistance measurements for both directions of B⊥ and
observing opposite behavior of Rxx (B⊥ ).
The third and final possibility is that the insulator has
an order parameter in the multiplet (s, τ z s), in which case
the electrons fill one spin-polarized band in each valley.
Let us assume the order parameter is sz , and write down
a corresponding mean-field Hamiltonian:

hk =

(ε+,k − ε−,k ) z
τ ⊗ s0 + MS τ 0 ⊗ sz
2
µB gv (k)B⊥ z
µB gs B⊥ 0
−
τ ⊗ s0 −
τ ⊗ sz
2
2

(3)

In this case, the valley-Zeeman term competes with the
order parameter mass term MS sz , and the mean-field
band gap is given by
∆V I ≈ 2|MS | − µB |gv,max B⊥ | ,

(4)

where gv,max is the maximal value of gv (k) in the miniBrillouin zone. Note that we have assumed that MS is
much larger than the bandwidth of the flat bands, although our conclusions below will also be valid without
this assumption (as long as MS is bigger than the bandwidth). We have also ignored the spin-Zeeman term because the maximal orbital g-factor is much larger than
the spin g-factor. The bandgap ∆V I again decreases with
an out-of-plane magnetic field. So at first sight, also this
insulator seems incompatible [28] with the experimental
findings of Ref. [29]. However, in contrast to the IVC insulator, now the bands of the mean-field Hamiltonian in
Eq. (3) have Chern number C = ±1. It is well-known in
the context of quantum Hall ferromagnetism [33, 47, 48]
that skyrmion textures in a spin-polarized Landau level
carry electric charge [33]. This is also true for Chern
insulators, which means that there is another candidate
for the lowest-energy charged excitations. If skyrmions
are indeed the lowest-energy charge carriers, then the resistivity increase with out-of-plane magnetic field in the
transport measurements of Ref. [29] would result from
the spin-Zeeman term, which increases the energy of a
skyrmion. In the next sections, we examine this possibility in more detail. We note that skyrmions in general
flat moiré bands with non-zero Chern number were also
discussed in Ref. [19]. While Ref. [19] focuses on the
possibility of skyrmionic superconductivity for bosonic
skyrmions in C = 2 Chern bands, in our work we mainly
focus on fermionic skyrmions in C = 1 bands and their
implication on the gap.

IV.

SU(2)+ ×SU(2)− SYMMETRY BREAKING
EFFECTS

In the previous section we have argued that if the resistance peak observed in Ref. [29] at ν = 2 can be
attributed to an insulating state, then this insulator has
a symmetry breaking order parameter in the multiplet
(s, τ z s), and skyrmions as lowest-energy charge carriers.
Before discussing the skyrmion excitations in more detail, we first study the SU(2)+ ×SU(2)− symmetry breaking terms in the Hamiltonian, which distinguish between
the s and τ s order parameters. We want to know what
order parameter gives the lowest energy, i.e. whether
the SU(2)+ ×SU(2)− breaking terms favor spin alignment or anti-alignment between the different valleys. If
the spins are aligned in the two valleys (order parameter s), the insulator is a time-reversal symmetry breaking ferromagnet with a non-zero local spin moment. If
the spins in the valleys are anti-aligned (order parameter τ z s), the insulator is time-reversal symmetric which
implies there is no local spin moment. Because the electron spin in this state is locked to the valley quantum
number (sz = τ2 or sz = − τ2 ), we will refer to it as the
‘spin-valley locked state’. In a non-zero external magnetic field, the spins in the spin-valley locked insulator
will cant in the direction of the magnetic field, similar to
the canted anti-ferromagnet (CAF) [49–51]. The canted
spin-valley locked state which appears in this manuscript
is similar to the CAF occuring in the ν = 0 graphene
Landau levels [52–55].
A first microscopic SU(2)+ ×SU(2)− breaking term
comes from the Coulomb interaction, which takes the
form
1 XX
HC =
Vll0 (q) : ρl (q)ρl0 (−q) : ,
(5)
2A q
0
l,l

where l = t, b is a layer index and A is the area of the
mono-layer graphene unit cell. From now on we will always implicitly assume normal ordering. For the interaction potential we use a dual-gate screened Coulomb
potential, which in momentum space takes the form
e2
tanh(D|q|)
(6)
2r 0 |q|


e2
2e−2D|q|
−d|q|
Vtb (q) = Vbt (q) =
e
−
(7)
2r 0 |q|
1 + e−2D|q|

Vtt (q) = Vbb (q) =

where D is the distance from the tBLG to the metallic
gates, which we take to be three moiré lattice constants.
Eq. (7) holds when the inter-layer distance d, of the order
of one graphene lattice constant, is much smaller than the
gate distance D. Based on the findings of Ref. [56], we
take the hBN dielectric constant to be r = 6.6. The
layer resolved density operator ρl (q) is given by
1 X0 X †
ρl (q) = √
ψk+q,l,σ,s ψk,l,σ,s ,
N k σ,s

(8)

6
where N is the number of graphene unit cells and σ and
s are respectively sublattice and spin indices. We use
primed momentum sums to denote sums that run over
the mono-layer graphene Brillouin zone. A few remarks
are in order before we proceed with
R our analysis. We
have used the expression V (q) = d2 r V (r)eiq·r for the
interaction potential in Fourier space. This approximation is valid for a|q|  1, with a the graphene lattice
constant. However, the inter-valley scattering terms we
are interested in involve large momentum transfers between electrons, and are therefore not in the regime where
a|q|  1 holds. Although V (q) does not accurately describe lattice-scale interactions, we nevertheless still expect it to give a reliable estimate for the energy scale
of the inter-valley scattering, and to provide the correct
physical picture of the SU(2)+ ×SU(2)− symmetry breaking effects.
We now project the density operators in the flat bands
above charge neutrality, which gives
1 X X τ,τ 0
ρ̃l,g (q) = √
λl,g (q, k)c†k+q,τ ck,τ 0 .
N τ,τ 0 k

(9)

In this expression, both q and k lie in the mini-Brillouin
zone, and g is a moiré reciprocal lattice vector. The
operators ck,τ = (ck,τ,↑ , ck,τ,↓ )T annihilate an electron
with momentum k in the mini-band of valley τ . Note
that since we are only considering one band per valley,
we can use the valley index τ to label the mini-bands.
The form factors are defined using the moiré Hamiltonian
Bloch states |uτ (k)i as
0

0
λτ,τ
l,g (q, k) = huτ (k + q)|Sg Pl |uτ (k)i ,

(10)

where Pl projects onto layer l and Sg is a matrix with
entrees [Sg ]gi ,gj = δgi ,g+gj , where g, gi and gj are moiré
reciprocal lattice vectors. Using the projected density
operators, we write the Coulomb Hamiltonian as the sum
of an intra-valley and an inter-valley parts

K valleys (see Appendix A for additional details). Using
a standard Fierz identity we can write HIV as the sum of
an inter-valley density-density interaction and an intervalley Heisenberg or Hund’s coupling [19]. We focus only
on the SU(2)+ ×SU(2)− breaking term, i.e. the intervalley Heisenberg term. From Eq. (12) we see that it is
of the form
1 X X C
Vτ (q + k0 − k, k, k0 )
(14)
NA
0
q,k,k τ


X †
si
si
×
ck0 +q,−τ ck0 ,−τ
c†k−q,τ ck,τ ,
2
2
i

HC,J = −

where si are the Pauli matrices acting on spin indices.
To see whether the Hamiltonian in Eq. (14) prefers
ferro- or anti-ferromagnetically aligned spins in different
valleys, we define the four Slater determinants |τ, si =
Q
(NM !)−1/2 k c†k,τ,s |0i, where NM is the number of moiré
unit cells. The relevant matrix element determining the
inter-valley spin splitting in first order perturbation theory is given in terms of these Slater determinants as
h+, ↑; −, ↑ |HC,J |+, ↑; −, ↑i
1 XX C 0
V (k − k, k, k0 )
=−
4N A 0 τ τ

(15)

k,k

We have calculated this matrix element numerically, and
found that to a very good approximation it can be written
as a function of the inter-layer distance d as
1
h+, ↑; −, ↑ |HC,J |+, ↑; −, ↑i
NM
4π d

≈ −(0.20 − 0.16 e− 3 a ) meV ,

(16)

So the inter-valley Heisenberg coupling arising from
Coulomb interaction is ferromagnetic, and its magnitude
increases as a function of the inter-layer distance. This
is a consequence of the phase structure of the flat band
H̃C = HV + HIV ,
(11)
wave functions, which leads to the minus sign in front of
the exponential factor.
where HV is U(2)+ ×U(2)− symmetric. Here we are only
Next to the Coulomb interaction, there is a second
interested in the inter-valley part, which takes the form
source of SU(2)+ ×SU(2)− symmetry breaking, which
comes from lattice-scale phonons near the K points of
1 X X C
HIV =
Vτ (q, k, k0 )c†k+q,−τ ck,τ c†k0 −q,τ ck0 ,−τ , the graphene Brillouin zone. As discussed in detail in
2N A
Appendix B, the phonon-induced inter-valley coupling
q,k,k0 τ
projected into the flat bands is
(12)
where the flat-band projected interaction potential, degph X X P H
H
=
−
Vτ (q, k, k0 )
(17)
P
H
fined to include the form factors, is given by
N
0 τ
q,k,k
X
VτC (q, k, k0 ) =
Vll0 (q + g + 2X) ×
(13)
×c†k+q,−τ ck,τ c†k0 −q,τ ck0 ,−τ ,
l,l0 ,g

−τ,τ
0
λτ,−τ
l,g (q, k)λl0 ,−g (−q, k )

In the above expression, we use X to denote the position
of the center of the mini-Brillouin zone at the monolayer

where the phonon interaction strength is approximately
gph ≈ 630 meV. The phonon mediated interaction potenτ
tial is expressed in terms of the form factors fl,g
(q, k) =
x
hu−τ (k + q)|σ Sg Pl |uτ (k)i as

7
A.

VτP H (q, k, k0 ) =

X

−τ
τ
fl,g
(q, k)fl,−g
(−q, k0 ) .

(18)

l,g

As before, we can use a Fierz identity to isolate the
SU(2)+ ×SU(2)− symmetry breaking part of the Hamiltonian in Eq. (17). We find
HP H,J =

2gph X X P H
Vτ (q + k0 − k, k, k0 )
(19)
N
0
τ
q,k,k


X †
si
si
†
×
ck0 +q,−τ ck0 ,−τ
ck−q,τ ck,τ ,
2
2
i

The relevant matrix element for the phonon induced
inter-valley coupling Hamiltonian is
h+, ↑; −, ↑ |HP H,J |+, ↑; −, ↑i
gph X X P H 0
Vτ (k − k, k, k0 )
=
2N
0 τ

(20)

k,k

Evaluating this matrix element numerically, we find
1
h+, ↑; −, ↑ |HP H,J |+, ↑; −, ↑i ≈ 0.075 meV
NM

CHARGED SKYRMION EXCITATIONS

As mentioned previously, a skyrmion texture described
by a unit vector field n(r) in a spin polarized Chern band
carries electric charge, as follows from the following general relation between the excess charge density ρ(r) and
Pontryagin density [33]:
C
n(r) · (∂x n(r) × ∂y n(r)) ,
(22)
4π
where C is the Chern number. In order to identify
skyrmions as the dominant charge carriers, we have to
study their energetics, which is what we turn to next.
ρ(r) = −

For temperatures larger than the inter-valley Heisenberg coupling (T & 1K), the spins from opposite valleys
are decoupled via thermal fluctuations, while they remain
ferromagnetically correlated within each valley due to
the large Coulomb scale (as exemplified by the spin stiffness ρs calculated below). Therefore, let us first ignore
the inter-valley Heisenberg coupling and assume that the
Hamiltonian is SU(2)+ ×SU(2)− symmetric. In that case,
the lowest-energy skyrmions are skyrmions with topological charge ±1 in a single valley. Because the flat bands
have Chern number ±1, these skyrmions have electric
charge ±1 according to Eq. (22). The energy of such a
skyrmion is given by Esk = 4πρs [65], where ρs is the
spin stiffness. In Refs. [33, 66], a mean-field expression
for the spin stiffness of a spin polarized Landau level was
derived. In Appendix C, this expression is generalized
to the case of electrons
P interacting via a density-density
term of the form k Ṽ (k)ρ(k)ρ(−k), projected onto a
flat band with Berry curvature F(k). Using the same
approach as Ref. [66], we find the following approximate
expression for the spin stiffness:

(21)

We see that the phonon induced inter-valley Heisenberg
coupling is anti-ferromagnetic. Note that it is a significant fraction of the Coulomb inter-valley Heisenberg coupling in Eq. (16) for d ≈ a, so it cannot be neglected.
In fact, if one would not take a finite layer separation
into account in the Coulomb potential, the phonon contribution would dominate. We conclude that although
the system at ν = 2 will most likely be ferromagnetic
(FM) and spontaneously break time-reversal symmetry,
we can not rule out the spin-valley locked state (SVL)
where the electron spins are anti-aligned in different valleys (hτ z si 6= 0). The ferromagnetic state with order parameter s was also recently found to describe the ν = 2
insulator observed in twisted double bilayer-graphene [6–
8, 20]. The possibility of magnetic order in magic-angle
tBLG was also previously discussed in Refs. [26, 57–64].
V.

Skyrmion energy with SU(2)+ ×SU(2)−
symmetry

1
ρs =
8A

1 X
F(k0 )2
N 0
k

!

1 X
Ṽ (k)f 2 (k)|k|2
N

!
,

k

(23)
where A is the area of the unit cell, N is the number of
unit cells and f (k) = |λ(k, k0 )| for some representative
k0 . The only approximation used to derive Eq. (23) is
that the magnitude of the form factor |λ(k, q)| is independent of q. If the Berry curvature is completely uniform
throughout the Brillouin zone, Eq. (23) reduces to the
previously derived expression for Landau levels [33, 66].
From Eq. (23), we see that a non-homogeneous Berry
curvature leads to a higher spin stiffness, and therefore a
higher skyrmion energy.
If we apply Eq. (23) to tBLG, we find
!
X
1
1
0 2
ρs ≈
F(k ) ×
8AM NM 0
k ∈mBZ
!
1 X X
V (k + g)fg2 (k)|k|2 , (24)
N
g
k∈mBZ

where AM is the area of the moiré unit cell, N is the
number of mono-layer graphene unit cells, NM the number of moiré unit cells, g again denotes the moiré reciprocal lattice vectors, V (k) is the screened Coulomb
potential P
defined in Eqs. (6) and (7) (with d = 0), and
fg (k) = | l λ++
l,g (k, K+ /2)| (recall that K+ is the miniBZ K-point). The reason for defining fg (k) with respect
to the momentum
P point K+ /2 instead of the Γ point is
that we found | l λ++
l,g (k, q)| to be largely independent
of q, except near Γ.

8

2 X
V (k + g)fg2 (k) ,
Eph =
N

2.0
1.5
1.0
0.5

(25)

k,g

which agrees with the expression for the energy of a wellseparated particle-hole pair in the spin polarized lowest
Landau level [67], and sets the scale for the mean-field
gap MS .
In Fig. 5 we plot the ratio r = E2,sk /Eph of the energy
of a skyrmion pair over the energy of a well-separated
particle-hole pair for a dual-gate screened Coulomb potential, as a function of the sublattice splitting ∆t on
the top layer. The shape of this curve is completely determined by the distribution of the Berry curvature over
the mini-Brillouin zone. From Fig. 5 we see that r initially decreases very quickly, until it reaches a minimum
at ∆t ≈ 5 meV. This decrease follows from the fact that
the Berry curvature is initially peaked at the K points
because of the Dirac cones in the ∆t = 0 band spectrum,
but starts to smoothen out when ∆t increases. The ratio
r reaches a minimum for ∆t ≈ 5 meV. After this minimum, the Berry curvature starts to accumulate again,
this time at the Γ point. Now the spin stiffness increases
only slowly with ∆t . This is because a large value of
∆t is required in order to close the gap between the flat
band and the higher dispersive band at Γ, at which point
the Berry curvature would also become singular. However, for realistic values of ∆t , we see that the skyrmionpair energy is around 40 to 45 percent of the particlehole energy. For example, with ∆t = 15 meV, we find a
skyrmion-pair energy of ≈ 21 meV, and a particle-hole
energy of ≈ 48 meV.
The energy of a skyrmion in a single valley will increase
when the inter-valley Heisenberg coupling is taken into
account because this term wants to lock the spin moments in both valleys together and therefore penalizes a
skyrmion texture made from the spins in only one valley
but not the other. In the next section, we study the effect of non-zero inter-valley Heisenberg coupling in more
detail.

B.

2.5

r

The energy cost of a well-separated skyrmion pair
E2,sk = 8πρs is to be compared with the energy cost of
a particle-hole excitation in the spin polarized flat band.
Using the same approximation as for the calculation of
ρs , this energy cost in a mean-field decoupled Hamiltonian is readily found to be

Effective field theory description

In this section, we compute the energy of a charge
e skyrmion in a single valley with non-zero inter-valley
Heisenberg coupling. We take into account the change of
the ground state due to the external magnetic field, but
neglect the back-reaction of spins in the opposite valley

0.00

10

20

30

t (meV)

40

50

FIG. 5: Ratio r = E2,sk /Eph of the energy of a well-separated
skyrmion pair over the energy of a particle-hole excitation in a
SU(2)+ ×SU(2)− symmetric model as a function of the sublattice
splitting on the top graphene layer.

in response to the formation of a single skyrmion. We expect this to be a good approximation in the regime where
the inter-valley exchange, parameterized by ρ̄s , is weaker
than the spin stiffness ρs in each individual valley; this
is the case for tBLG on HBN as shown by our numerical
estimates (ρ̄s /ρs ≈ 0.1).
First, we consider the ferromagnet. A single skyrmion
in one valley contains spins which are not aligned with
the spins in the other valley, and also with the external
magnetic field B⊥ which aligns all spins with itself in the
ground state. The core-size (and energy) of a skyrmion is
determined by the competition between the Coulomb repulsion and exchange energy loss due to decoupling with
spins from the opposite valley (determined by ρ̄s ), and
with B⊥ . For small ρ̄s and B⊥ , the skyrmion would be
large as it would try to minimize Coulomb repulsion. On
increasing B⊥ , the Zeeman energy dominates and the
skyrmion size saturates to a small value of the order of
moiré lattice spacing aM . In this limit, the skyrmion energy also saturates to a maximum value; and a skyrmionantiskyrmion pair resembles a particle-hole pair.
To illustrate this schematically, we make an (oversimplified) estimate the energy Esk of a two-dimensional
skyrmion of linear size R, which is given by the sum of
its elastic energy Eel , Coulomb energy EC (for simplicity we temporarily ignore screening) and Zeeman-energy
EZ that receives contribution from both the inter-valley
coupling and the external magnetic field B⊥ :

2

e2
ρ̄s  R
Esk ≈ 4πρs +
+ gs µB B⊥ +
=⇒
4πR
2
aM
!1/3
1/3

a2M `2B̃
e2 a2M
Ropt ≈
≡
(26)
4π(gs µB B⊥ + ρ̄s /2)
a0
where a0 = m4π
2 is the effective Bohr radius, `B̃ =
ee
p
~/e[B⊥ + ρ̄s /(2gs µB )] is the effective magnetic length
and aM is the moiré lengthscale. At the optimal length-

9

(b)

(a)

FIG. 6: (a) Band-splitting and skyrmion gap in the ferromagnet as a function of B⊥ . (b) Green (brown) line schematically depicts the
charge gap ∆c as a function of B⊥ for the ferromagnet (spin-valley locked state). ∆c increases till B⊥ = BF M (BSV L ) when the
energies of the skyrmion-pair and particle-hole pair cross, and then drops.

scale, the energy of the skyrmion is given by
!1/3
e2
a0 aM
Esk (B⊥ ) − Esk (B⊥ = 0) ≈
4πaM
`2B̃
(
B⊥ , for gs µB B⊥  ρ̄s
∝
(27)
1/3
B⊥ for ρ̄s  gs µB B⊥
Therefore, Esk first increases linearly, and subsequently
sublinearly in B⊥ for small B⊥ ; this feature remains valid
even in presence of screening and can contribute to an
increasing charge gap on turning on B⊥ .
Next, we turn to a continuum field theory for a more
accurate estimate of the skyrmion energy. The effective
Lagrangian density for the ferromagnet can be described
by the following two-component O(3) non-linear σ model:

X 
L=
nS A[nτ ] · ∂t nτ (r) + gs µB B · nτ (r)
τ =±


nS 2 ρ̄s
ρs
(∇nτ (r))2 −
[n+ (r) − n− (r)]2
2
2
Z
1
−
dr 0 V (r − r 0 )ρ(r)ρ(r 0 )
(28)
2

−

where A[nτ ] corresponds to the vector potential of a unit
monopole with ∇n × A[nτ ] = nτP
, and nτ (r) lies on the
2-sphere (nτ · nτ = 1). ρ(r) = τ ρτ (r) with ρτ (r) =
τ
−C
4π nτ · (∂x nτ × ∂y nτ ) is the topological charge density
of the skyrmion (Cτ = ∓1 for valleys labeled
√ τ = ±),
ρ̄s is the inter-valley spin-stiffness, n = 2/( 3a2M ) is the
density of electrons and S = 1/2 is the electron spin
(~ = 1). In the ground state, n+ (r) = n− (r) for the
ferromagnet so the term with ρ̄s does not contribute.
To calculate the energy of a skyrmion configuration, it
is convenient to use complex coordinates z = x + iy, and
write the single skyrmion texture in terms of a complex
analytic function W (z) as follows [65].
nx − iny =

2W (z)
1 − |W (z)|2
,
n
=
z
1 + |W (z)|2
1 + |W (z)|2

(29)

As shown in Appendix D 1, we find that the field theory yields the following energy for the skyrmion ansatz
W (z) = R/z after optimizing its size R (α is an O(1)
numerical constant).

 
ν
∆
EC
Esk = 4πρs + αEC
ln 1 +
(30)
EC
∆
where ν = 1/2 (1/3) for strongly gate-screened (unscreened) Coulomb interaction (see Eq. (6)), and ∆ =
gs µB B⊥ + ρ̄s /2 is the effective Zeeman energy-scale in a
given valley. We conclude that irrespective of the precise details of screening, Esk increases sub-linearly with
B⊥ for small external fields. Though this effective theory cannot capture large B⊥ when lattice-scale effects
become important, the skyrmion energy is expected to
saturate as a skyrmion pair gets squeezed to a particlehole pair.
We can estimate the energy and size of a skyrmion for
screened Coulomb coupling with a screening length of the
order of aM . Taking Ec ≈ ρs ≈ 1 meV, we find that the
correction to the elastic energy of the skyrmion is ≈ 1
meV for B⊥ = 0 and ρ̄s = 0.12 meV. This implies that
the skyrmion-antiskyrmion pair still costs lower energy
than the particle-hole pair. The net magnetic moment
carried by the skyrmion is approximately 2.7 gs µB , so we
are in the regime where the skyrmion size is quite small.
Hence, the exact numerical estimates from our continuum model are not likely to be very accurate; however,
they are robust to small microscopic deformations of the
Hamiltonian and provide a reasonable sense of the relevant energy scales.
For the spin-valley locked state, we replace n− → −n−
in Eq. (28). While the Zeeman gap ∆ = ρ̄s /2 is identical
to the ferromagnet for B⊥ = 0, turning on B⊥ causes
spins from opposite valleys to cant towards itself, changing the ground state (however, spins within one valley remain ferromagnetically aligned). Interestingly, the effective Zeeman gap for a single valley (∆) remains constant
until the field reaches the critical value B⊥ = ρ̄s /(gs µB ),
at which point a transition to the ferromagnetic state oc-

10

FIG. 7: The band-gap evolution at ν = 3 as a function of B⊥ , for ∆V Z < ∆SZ and ∆V Z > ∆SZ . We have assumed that gv < 0, gs > 0
and |gv | > |gs |, following Refs. [27, 28].

curs (see Appendix D 1). Once the system is ferromagnetic, the skyrmion energy increases linearly as discussed
above. To summarize, we find the following behavior for
∆:
(
∆ = gs µB B̃ =

ρ̄s
ρ̄s
2 , B⊥ < gs µB
gs µB B⊥ − ρ̄2s , B⊥ ≥ gsρ̄µsB

(31)

Accordingly, the skyrmion size also remains fixed till
B⊥ = ρ̄s /(gs µB ) and then gradually decreases as B⊥
is tuned up further.

C.

Charge gap in a magnetic field at ν = 2

Having established that a skyrmion is the lowest energy
charge e excitation for small external fields, we now turn
to the longitudinal resistivity ρxx as a function of B⊥ .
We assume that the insulator at ν = 2 has an activated
ρxx which is governed by the gap ∆c to the charged excitation that costs the lowest energy. Because of the valleyand spin-Zeeman terms in Eq. (1), the bandgap decreases
with increasing B⊥ , and hence the gap to exciting an electron to an empty band decreases. On the other hand,
the single charge e skyrmion gap for the ferromagnet inν
creases as B⊥
(1/3 ≤ ν ≤ 1/2 depending on the nature
of screening) for small fields B⊥ . Therefore, the overall
charge gap ∆c = min{2Esk (B⊥ ), 2|MS | − µB |gv,max B⊥ |}
will initially increase as a function of B⊥ , and then start
dropping when the valley-Zeeman term dominates, as
schematically depicted in Fig. 6. Assuming that the behavior of the resistivity is determined entirely by the activation gap ∆c , charge e skyrmions can explain the peculiar behavior of ρxx (B⊥ ) [29]. For the spin-valley locked
state, the gap remains constant till B⊥ ≈ ρ̄s /(gs µB ),
and then increases; therefore it appears unlikely that the
ground state is the spin-valley locked state based on the
transport data. This agrees with the results of Section
IV, where we found the net inter-valley Heisenberg coupling to be ferromagnetic.

D.

Charge gap at ν = 3

Next, we turn our attention to the ν = 3 state and
discuss predictions for the charge gap in presence of B⊥ ,
assuming it is insulating in a high-quality sample. The
anomalous Hall effect and evidence of edge transport [29]
can be explained by a single spin and valley polarized
hole-band. Equivalently, three of the four conduction
bands are filled; for concreteness let us assume these are
(τ z , sz ) = (+, ↑), (−, ↑) and (+, ↓). If the lowest energy
charged excitations are skyrmions, then the energy of a
single isolated skyrmion is be given by Eq. (30). In particular, the elastic energy 4πρs of the skyrmion should
remain unchanged as the spin-stiffness ρs is insensitive
to the valley or spin quantum number of the conduction
band. The effective magnetic field seen by the skyrmion
B̃ is given by the sum of the external field B⊥ and the
internal field which is proportional to ρ̄s and the internal
Zeeman field from the ordered moments of the remaining filled bands. In our mean-field picture, the (+, ↑)
and (+, ↓) states form a spin-singlet at each k. Therefore, skyrmions cannot be excited in the τ = + valley. A
skyrmion excitation is possible in the τ = − valley, starting with electrons in the (−, ↓) band. Such a skyrmion
will see no background ordered moment, and therefore
have a lower energy Esk given by Eq. (30) with B̃ = B⊥ .
The charge gap ∆c is just 2Esk .
At higher external fields, we expect the charge gap to
be set by the particle-hole gap, as the skyrmion energy
increases with B⊥ . Note that although the degeneracy
between the four conduction bands is spontaneously broken at B⊥ = 0, turning on an infinitesimal B⊥ automatically chooses an arrangement of the bands via the valley
and spin Zeeman terms in the Hamiltonian. The behavior of the particle-hole gap as a function of B⊥ depends
on the sequence in which these bands are ordered with
energy, which in turn depends on the interaction induced
valley-Zeeman and spin-Zeeman gaps at zero B⊥ . If the
valley-Zeeman gap is larger than the spin-Zeeman gap,
the top two bands are spin-split and they move apart
under an applied B⊥ via the single-particle Zeeman shift
with a constant g-factor gs = 2. In contrast, if the spinZeeman gap dominates and the top two bands are valley-

11
split, then the particle-hole gap increases with B⊥ , but
with a g-factor gv (k0 ) where k0 corresponds to the point
where the gap is minimal at B⊥ = 0. The situation is
depicted schematically in Fig. (7), where we neglect the
dispersion of the flat bands (which is justified for a spatially uniform order parameter, as the gap magnitude is
set by the larger Coulomb scale).
To summarize, at ν = 3 the skyrmion energy is expected set the charge gap at B⊥ = 0, leading to a
non-linear onset with B⊥ . At intermediate fields the
skyrmion-antiskyrmion energy will exceed the particlehole energy. In this regime gap will continue to increase
with B⊥ , but linearly. Further, the coefficient of linear
increase can tell whether the valley Zeeman gap is larger
than the spin-Zeeman gap at B⊥ = 0, or vice-versa. At
even larger values of B⊥ , the valence bands which we
have neglected till now may come close the Fermi level,
resulting in a decrease of the charge gap.

VI.

SKYRMION PAIRING

In this section, we show that charge e fermionic
skyrmions have a generic tendency to attract and bind
into charge 2e bosonic pairs, leading to the exotic possibility of quantum phases (like superconductivity) that
can arise from skyrmion pairing at finite density at
T = 0. Although we use a semiclassical description for
the energetics to maintain an analytical handle and pinpoint the physical mechanism of pairing, the small size
of the skyrmions for parameters relevant to tBLG (see
section V B) motivates us to consider these skyrmions
(or skyrmion-pairs) as charged quantum quasiparticles.
Therefore, we can envision transitions to quantum liquid (superconductor) or quantum solid (Wigner crystal)
phases of 2e skyrmion-pairs at small but finite density of
charge carriers, in the same spirit as band structures or
phase transitions of charge-neutral quantum skyrmions
have been considered in two-dimensional chiral magnets
[68].
We first consider two skyrmions from the same Chern
band (same valley). If they have opposite phases in the
plane normal to the spin-ordering axis (x-y plane in our
scenario), they will always attract at large distance scales
(an opposite phase-winding skyrmion can be obtained
by n = (nx , ny , nz ) → (−nx , −ny , nz ) and has the same
topological and electric charge). The physical reason is
simple: for a pair of well-separated skyrmions of opposite phases (the distance between their centers 2L is much
larger than the typical skyrmion size R, but smaller than
the spin-correlation length ξs ), the components of the
spin pointing normal to the effective field B̃ are quenched
at distance L  ξs . This lowers the effective Zeeman energy, which is present in tBLG due to intervalley coupling
even at B⊥ = 0. Indeed, we show below that the effective Zeeman energy gain is logarithmic and this results
in a L−1 attractive force between these skyrmions that
always prevails the L−2 Coulomb replusion at large dis-

FIG. 8: Schematic depiction of the skyrmion-pair potential from a
single valley. The skyrmions can form a bound state if the
minima at 2Lopt is deeper than minima at L → ∞.

tances [69, 70] (or a screened Coulomb repulsion, which
decays exponentially at distances larger than the screening length). Therefore the skyrmions prefer to be paired
at the lowest energy scales (akin to vortices in a U(1) superfluid below the Berezinskii-Kosterlitz-Thouless transition temperature TBKT ).
We now consider an opposite phase skyrmion pair configuration in the ferromagnet, with a distance 2L between
their centers.
W (z) =

R
R
−
z−L z+L

(32)

The energy of the skyrmion-pair Epair can be computed
using the effective field theory in Eq. (28); the details are
relegated to Appendix D 2.
el
Z
C
Epair = Epair
+ Epair
+ Epair

= 8πρs +

8πgs µB B̃R2
√ 2
ln
3aM



2L
R


+

e2
4π(2L)
(33)

where B̃ = B⊥ + 2gρ̄ssµB is the effective Zeeman field at
ν = 2. Therefore, we confirm that the skyrmion-pair
attracts at distances L larger than R but smaller than
ξs , as depicted schematically in Fig. 8.
At finite density the charge 2e bosonic skyrmion-pairs
can either condense to form a superconductor, or form
into a Wigner crystal phase to minimize Coulomb repulsion [70]. Such superconductivity may be aided by
gate-screening of Coulomb interaction, or suppressed by
the Magnus force felt by a skyrmion-pair from the same
Chern band [71]. The exact phase diagram requires an
involved study we will not attempt here; instead we focus
on the symmetry properties of superconductor obtained
by such a condensate.
To derive the quantum numbers of the skyrmions and
skyrmion-pairs, we follow the approach in Ref. 70. we
note that if we write nx + iny ∼ eiφ sin θ, the classical
phase space variables (φ, nz ) can be promoted to canonically conjugate quantum operators (φ̂, 2ŝz ). The infinite
degeneracy with respect of rotation of phase φ for a single
classical skyrmion texture translates to
R a fixed quantum
number for the total spin Sz = (n/2) dr[nz (r) − 1] (recall that n is the electron density, and we have subtracted

12
out the background spin from the ground state). The size
of the quantum skyrmion R takes the closest possible
value to the classical minimum to ensure a half-integer
spin Sz . The same should be true for a skyrmion-pair,
the quantum 2e boson corresponding to classical texture
npair (r) carries a quantized integer spin given by
Z
n
dr [npair (r) · ẑ − 1]
(34)
Sz =
2
The 2e bosonic pair carries non-zero net spin; therefore its condensation breaks time-reversal, and ferromagnetism persists into the superconductor. This is easiest
to see in the small-size limit when the skyrmion pair resembles a hole pair, it carries spin S = 1, and its condensation leads to triplet superconductivity. However,
the symmetry properties of the superconductor do not
change away from this limit, where our proposed mechanism is operative. Hence, the quantum phase transition (QPT) from the ferromagnet to the superconductor
only breaks U(1) charge conservation, and is described
by the Abelian Higgs model (charged 2e scalar coupled
to a U(1) electromagnetic gauge field). Further, since the
2e boson carries charge ±2 under U(1)v (depending on
the valley/Chern sector), it transforms non-trivially under moiré lattice translations and its condensation will
lead to broken translation symmetry with a three-fold
enlarged unit cell. A similar scenario holds for the spinvalley locked state as well, making appropriate modifications to B̃ using Eq. (31).
Next, we consider skyrmion pairing from opposite
Chern sectors (or equivalently, from opposite valleys). In
case of the ferromagnet, a charge 2e pair requires pairing a skyrmion from one valley with an antiskyrmion
from the opposite valleys (since they have opposite Chern
numbers). This does not lead to any effective Zeeman
energy gain, and is therefore not favorable. However,
skyrmion pairing of opposite charges from opposite valleys is favored by both Coulomb and effective Zeeman
terms (as it locally preserves the inter-valley ferromagnetic configuration when the skyrmions sit on top of each
other with n+ (r) = n− (r)). Such a skyrmion pair again
carries a large spin. The resulting inter-valley coherent
state breaks valley U(1) and spin-rotation, and the QPT
is described by a complex scalar field theory. Note that
this state is distinct from the conventional time-reversal
preserving IVC phase discussed in the context of tBLG
[28]. Regardless, a uniform condensate of such skyrmion
pairs is also precluded by the opposite Chern number
of the bands. To understand this, one can again resort
the small size (or large field) limit, when the skyrmionantiskyrmion pair reduces to a particle-hole or exciton
pair carrying a net spin S = 1. Since the argument of
Ref. 27 relies solely on topological considerations and is
independent of the spin of charge carriers, we expect such
a uniform condensate to be energetically unfavorable. A
lattice of skyrmion-antiskyrmion pairs (analogous to the
exciton-vortex lattice discussed in Ref. 27) offers an attractive alternative, but more detailed investigations are

required to establish its stability.
For the spin-valley locked state, a skyrmionantiskyrmion pair from opposite valleys (both with same
charge) can avoid losing any exchange energy at zero B⊥
by keeping spins locally anti-aligned (n+ (r) = −n− (r) ≡
n(r)), and simultaneously quench the Coulomb energy
cost by having a very large radius R which is fixed by
small anisotropies beyond the SU(2)+ × SU(2)− symmetric limit. Such a charge 2e pair therefore only costs an
elastic energy of Epair ≈ 8πρs . In analogy with the previous discussion, the quantum number Qa of the skyrmionantiskyrmion pair under a generator T a ∈ {s, τ z s} of the
symmetry group SU(2)+ × SU(2)− are given by:

Qa =

n
2

Z

dr (nsk (r) − n0 ) · Tr[(τ z s)T a ]

(35)

where nsk (r) is the skyrmionic texture in n(r) and
n0 = (0, 0, 1) is the ground state configuration. From
Eq. (35), we note that the superconductor formed by
skyrmion pairing from opposite valleys in the spin-valley
locked state preserves global spin-rotation symmetries,
i.e, Qa = 0 ∀ T a ∈ {s}. Further, it also preserves timereversal and translation (being neutral under U(1)v ).
This necessarily implies that in case of a direct transition, the critical point that describes the QPT from
the spin-valley locked state (breaks spin-rotation symmetry, preserves U(1) charge conservation) to the superconductor (which breaks U(1) charge conservation but
preserves spin-rotation) is a deconfined quantum critical
point. The critical theory for this transition has been
discussed using a five-component ’super-spin’ order parameter in Ref. [72] that transforms as a vector under an
emergent SO(5) symmetry. The defects of the spin-Hall
like order parameter, which are skyrmion pairs, carry
charge 2e. Therefore proliferation of these defects leads
to suppression of anti-ferromagnetic order and simultaneous appearance of superconductivity. Approaching
from the opposite side, the defects of the superconductor, which are vortices, carry quantized spin. This can be
seen via the critical theory with the Wess-Zumino-Witten
term in Ref. [72]; the latter endows a superconducting
vortex with a spin-half. Hence, proliferation of vortices
destroys superconductivity and simultaneously results in
long-range magnetic order.
Lastly, we note that if this mechanism is operative in
tBLG, the critical temperature of the superconducting
transition would be set by the Heisenberg coupling J between the spins from opposite valleys (which provides
the binding energy). From Eq. (16), we therefore expect
Tc ∼ J ∼ 1K. An in-depth investigation of superconductivity via skyrmion-pairing, including a quantitative
estimate of Tc and a phase diagram as a function of doping, will be the subject of a forthcoming study [73].

13
VII.

DISCUSSION

We have argued that the ν = 2 resistance peak observed in magic-angle tBLG aligned with hBN observed
in Ref. [29, 30] arises from electrons filling a spin polarized band in each valley. The spins in different valleys
are most likely aligned ferromagnetically, but we cannot completely exclude the possibility that there is antiferromagnetic alignment between the valleys. The precise nature of the inter-valley spin correlation depends
on lattice-scale effects which determine the inter-valley
Heisenberg coupling and are not accurately captured by
our approach. However, irrespective of the spin alignment or anti-alignment between the valleys, we expect
skyrmion excitations to be lower in energy than particlehole excitations. Because of the the non-zero Chern
number of the flat bands, these skyrmions carry charge
±e, making them the most relevant charge carriers. Because skyrmions have a large effective g-factor, the spinZeeman term efficiently raises their energy, which we propose to be the origin of the increase in resistivity with
out-of-plane magnetic field observed in Ref. [29] at ν = 2.
We note that our diagnosis of a ferromagnetic insulator
at ν = 2 based on magnetotransport data is consistent
with recent predictions of ferromagnetic insulating states
at integer fillings of nearly flat bands based on exact diagonalization and DMRG studies of models appropriate
to tBLG on hBN [74].
Experimental probes: A natural question arises regarding experimental probes that distinguish between the different magnetic orders at ν = 2, since neutron-scattering
experiments may be difficult due to the two-dimensional
nature of the sample. The ferromagnet breaks timereversal symmetry, and therefore can be probed using
muon spin resonance. However, non-linear optical responses that are enhanced by orbital ferromagnetism in
flat bands as suggested in Ref. [75] will remain suppressed as there is no net valley-polarization at this filling. The spin-valley locked state breaks spin-rotation but
preserves time-reversal (since opposite valleys carry opposite spin), and is comparatively harder to detect. We
note that the collective magnons (which simultaneously
involve both valleys) have different dispersions in the two
cases (quadratic for FM, linear for spin-valley locked);
further ferromagnetic magnons gap out under a magnetic
field while antiferromagnetic magnons do not. Therefore,
studying the magnetic contribution to specific heat or
thermal conductivity; or performing spin-injection experiments (which can directly probe the magnon dispersion)
at the sample-edge [76, 77] can distinguish these states.
Since a skyrmion has a large number of flipped spins,
one can sense a trapped skyrmion in an impurity potential via spin-polarized STM, or local magnetometers like
a scanning nano-squid [78] or a Nitrogen-Vacancy (NV)
center [79]. Finally, if the state is indeed an AFM, then
applying a strong B⊥ will cant the spins and change the
ground state. As discussed, the charge e skyrmion gap
∆c (B⊥ ) will behave very differently from the ferromag-

net; it will stay constant till a critical field Bc that induces a phase transition to FM. Hence, a careful study
of the activation gap as a function of the magnetic field
can distinguish these scenarios. The said phase transition to a FM and associated critical signatures may also
be observed via thermodynamic probes.
Outlook : Recent theoretical and experimental works
have shown that flat bands with non-zero Chern number
are quite common in moiré materials [19, 80]. For example, Refs. [3, 26, 31] found either from experiments
or a self-consistent Hartree-Fock calculation that in certain regimes electron interactions in magic-angle tBLG
unaligned with hBN lead to a spontaneous breaking of
the C2v T symmetry protecting the Dirac cones, giving
rise to mean-field bands with Chern number equal to either ±2 [3, 26] or ±1 [3, 31]. In twisted double bilayer
graphene the C2 symmetry is broken explicitly on the
single-particle level, and the flat bands have Chern number 2 [20]. In Ref. [5], a Chern insulator at ν = 1 was
observed in ABC trilayer-graphene on hBN, which can
be understood from a Hartree-Fock study which predicts
mean-field bands with Chern number ±2 at intermediate
interaction strengths.
There is also mounting evidence that the insulating
states at integer ν result from spontaneous symmetry
breaking which lifts the spin and valley degeneracies, similar to what happens in quantum Hall ferromagnetism
[33, 47, 48]. The general picture that seems to emerge
at present is that this spin and valley degeneracy lifting occurs in a valley-U(1) preserving manner, i.e. without developing inter-valley coherence. For example, the
anomalous Hall effect at ν = 3 in tBLG aligned with
hBN observed in Refs. [29, 30] and the Chern insulator
at ν = 1 in trilayer graphene [5] can both naturally be attributed to a spontaneous valley polarization [5, 27, 28].
The insulators at ν = 1 and ν = 2 observed in twisted
double bilayer graphene in Ref. [6–8] were proposed to
respectively be a valley-polarized and valley-singlet ferromagnet [20]. A priori, skyrmions could play a role in
charge transport for any of these devices. However, this
is less likely for bands with higher Chern numbers because the spin stiffness increases quadratically with C
[19, 47]. We note that, interestingly, the ν = −2 insulator observed in ABC stacked trilayer graphene on hBN
[5] also shows an increased resistance peak under an applied out-of-plane magnetic field. ABC stacked trilayer
graphene has a large orbital g-factor [81], which means
that the valley-Zeeman effect dominates the spin-Zeeman
effect. Because of this, one expects that a slightly modified version of our discussion in the main text applies to
this device as well.
An important general open question concerns the connection between the insulators observed at integer fillings
in moiré materials and the superconducting domes which
result from doping these insulators. No superconducting
domes were observed in Refs. [29, 30], but this could be
because the temperatures in these experiments were too
high, or because of device quality. Further experimental

14
studies are needed to either rule out superconductivity
in magic-angle tBLG aligned with hBN, or to establish
its existence and measure its response to different electric and magnetic fields. If superconductivity is observed,
theory will have to come up with a pairing mechanism
for the charge carriers which are doped into the insulator.
In this work, we looked into the possibility of skyrmion
pairing, but other mechanisms are possible of course. For
example, Ref. [20] proposed a more conventional pairing
mechanism driven by ferromagnetic spin fluctuations to
explain the superconducting domes in twisted double bilayer graphene.
Finally, the precise connection between the insulators
observed in magic-angle tBLG aligned with hBN, and
those observed in the C2v symmetric devices [1, 3] where
the substrate does not significantly modify the singleparticle physics, is not clear. Theoretically, one would
like to understand what happens if one continuously
turns off the hBN-induced sublattice splitting. It is likely
that some insulators will undergo phase transitions, perhaps accompanied by changes in Chern number. Understanding this connection is an important missing piece in

[1] Yuan Cao, Valla Fatemi, Ahmet Demir, Shiang Fang,
Spencer L. Tomarken, Jason Y. Luo, Javier D. SanchezYamagishi, Kenji Watanabe, Takashi Taniguchi,
Efthimios Kaxiras, Ray C. Ashoori, and Pablo JarilloHerrero, “Correlated insulator behaviour at half-filling
in magic-angle graphene superlattices,” Nature 556, 80
EP – (2018).
[2] Matthew Yankowitz, Shaowen Chen, Hryhoriy Polshyn,
Yuxuan Zhang, K. Watanabe, T. Taniguchi, David
Graf, Andrea F. Young, and Cory R. Dean, “Tuning
superconductivity in twisted bilayer graphene,” Science
363, 1059–1064 (2019).
[3] Xiaobo Lu, Petr Stepanov, Wei Yang, Ming Xie, Mohammed Ali Aamir, Ipsita Das, Carles Urgell, Kenji
Watanabe, Takashi Taniguchi, Guangyu Zhang, Adrian
Bachtold, Allan H. MacDonald, and Dmitri K. Efetov, “Superconductors, orbital magnets and correlated
states in magic-angle bilayer graphene,” Nature (London) 574, 653–657 (2019), arXiv:1903.06513 [condmat.str-el].
[4] Guorui Chen, Lili Jiang, Shuang Wu, Bosai Lyu,
Hongyuan Li, Bheema Lingam Chittari, Kenji Watanabe, Takashi Taniguchi, Zhiwen Shi, Jeil Jung, Yuanbo
Zhang, and Feng Wang, “Evidence of a gate-tunable
mott insulator in a trilayer graphene moirésuperlattice,”
Nature Physics 15, 237–241 (2019).
[5] Guorui Chen, Aaron L. Sharpe, Eli J. Fox, Ya-Hui
Zhang, Shaoxin Wang, Lili Jiang, Bosai Lyu, Hongyuan
Li, Kenji Watanabe, Takashi Taniguchi, Zhiwen Shi,
T. Senthil, David Goldhaber-Gordon, Yuanbo Zhang,
and Feng Wang, “Tunable correlated Chern insulator
and ferromagnetism in a moiré superlattice,” Nature
(London) 579, 56–61 (2020), arXiv:1905.06535 [condmat.mes-hall].

the moiré puzzle.

Acknowledgements

It is a pleasure to thank Zhen Bi, Rafael Fernandez, David Goldhaber-Gordon, Jiang Kang, Eslam Khalaf, Biao Lian, Hoi Chun Po, Louk Rademaker, Cecile
Repellin, Todadri Senthil, Oskar Vafek, Ashvin Vishwanath, Fengcheng Wu, Andrea Young and Ya-Hui
Zhang for stimulating discussions. SC is particularly
thankful to Eslam Khalaf for clarifying the computation
of skyrmion quantum numbers, and related collaborations. SC acknowledges support from the ERC synergy
grant UQUAM via Ehud Altman. MZ and NB were supported by the DOE, office of Basic Energy Sciences under
contract no. DE-AC02-05-CH11231. This work was finalized in part at the Aspen Center for Physics, which is
supported by National Science Foundation grant PHY1607611.

[6] Xiaomeng Liu, Zeyu Hao, Eslam Khalaf, Jong Yeon
Lee, Kenji Watanabe, Takashi Taniguchi, Ashvin Vishwanath, and Philip Kim, “Spin-polarized Correlated Insulator and Superconductor in Twisted Double Bilayer
Graphene,” arXiv e-prints , arXiv:1903.08130 (2019),
arXiv:1903.08130 [cond-mat.mes-hall].
[7] Yuan Cao, Daniel Rodan-Legrain, Oriol RubiesBigordà, Jeong Min Park, Kenji Watanabe, Takashi
Taniguchi, and Pablo Jarillo-Herrero, “Electric Field
Tunable Correlated States and Magnetic Phase Transitions in Twisted Bilayer-Bilayer Graphene,” arXiv
e-prints , arXiv:1903.08596 (2019), arXiv:1903.08596
[cond-mat.str-el].
[8] Cheng Shen, Na Li, Shuopei Wang, Yanchong Zhao,
Jian Tang, Jieying Liu, Jinpeng Tian, Yanbang Chu,
Kenji Watanabe, and Takashi Taniguchi, “Observation
of superconductivity with Tc onset at 12K in electrically tunable twisted double bilayer graphene,” arXiv
e-prints , arXiv:1903.06952 (2019), arXiv:1903.06952
[cond-mat.supr-con].
[9] Yuan Cao, Valla Fatemi, Shiang Fang, Kenji Watanabe, Takashi Taniguchi, Efthimios Kaxiras, and Pablo
Jarillo-Herrero, “Unconventional superconductivity in
magic-angle graphene superlattices,” Nature 556, 43
EP – (2018).
[10] Alexander Kerelsky, Leo J McGilly, Dante M Kennes,
Lede Xian, Matthew Yankowitz, Shaowen Chen,
K Watanabe, T Taniguchi, James Hone, Cory Dean,
et al., “Maximized electron interactions at the magic
angle in twisted bilayer graphene,” Nature 572, 95–100
(2019).
[11] Youngjoon Choi, Jeannette Kemmer, Yang Peng, Alex
Thomson, Harpreet Arora, Robert Polski, Yiran Zhang,
Hechen Ren, Jason Alicea, Gil Refael, Felix von Oppen, Kenji Watanabe, Takashi Taniguchi, and Ste-

15
van Nadj-Perge, “Electronic correlations in twisted bilayer graphene near the magic angle,” Nature Physics
15, 1174–1180 (2019), arXiv:1901.02997 [cond-mat.meshall].
[12] Yuhang Jiang, Xinyuan Lai, Kenji Watanabe, Takashi
Taniguchi, Kristjan Haule, Jinhai Mao, and Eva Y.
Andrei, “Charge order and broken rotational symmetry in magic-angle twisted bilayer graphene,” Nature
(London) 573, 91–95 (2019), arXiv:1904.10153 [condmat.mes-hall].
[13] Yuan Cao, Debanjan Chowdhury, Daniel RodanLegrain, Oriol Rubies-Bigorda, Kenji Watanabe,
Takashi Taniguchi, T. Senthil, and Pablo JarilloHerrero, “Strange Metal in Magic-Angle Graphene with
near Planckian Dissipation,” Phys. Rev. Lett. 124,
076801 (2020), arXiv:1901.03710 [cond-mat.str-el].
[14] Hryhoriy Polshyn, Matthew Yankowitz, Shaowen Chen,
Yuxuan Zhang, K Watanabe, T Taniguchi, Cory R
Dean,
and Andrea F Young, “Large linear-intemperature resistivity in twisted bilayer graphene,”
Nature Physics 15, 1011–1016 (2019).
[15] Rafi Bistritzer and Allan H. MacDonald, “Moiré bands
in twisted double-layer graphene,” Proceedings of the
National Academy of Sciences 108, 12233–12237 (2011).
[16] Grigory Tarnopolsky, Alex Jura Kruchkov, and Ashvin
Vishwanath, “Origin of magic angles in twisted bilayer
graphene,” Phys. Rev. Lett. 122, 106405 (2019).
[17] J. M. B. Lopes dos Santos, N. M. R. Peres, and
A. H. Castro Neto, “Continuum model of the twisted
graphene bilayer,” Phys. Rev. B 86, 155449 (2012).
[18] J. M. B. Lopes dos Santos, N. M. R. Peres, and A. H.
Castro Neto, “Graphene bilayer with a twist: Electronic
structure,” Phys. Rev. Lett. 99, 256802 (2007).
[19] Ya-Hui Zhang, Dan Mao, Yuan Cao, Pablo JarilloHerrero, and T. Senthil, “Nearly flat chern bands in
moiré superlattices,” Phys. Rev. B 99, 075127 (2019).
[20] Jong Yeon Lee, Eslam Khalaf, Shang Liu, Xiaomeng
Liu, Zeyu Hao, Philip Kim, and Ashvin Vishwanath,
“Theory of correlated insulating behaviour and spintriplet superconductivity in twisted double bilayer
graphene,” Nature Communications 10, 5333 (2019),
arXiv:1903.08685 [cond-mat.str-el].
[21] Hoi Chun Po, Liujun Zou, Ashvin Vishwanath, and
T. Senthil, “Origin of mott insulating behavior and
superconductivity in twisted bilayer graphene,” Phys.
Rev. X 8, 031089 (2018).
[22] Liujun Zou, Hoi Chun Po, Ashvin Vishwanath, and
T. Senthil, “Band structure of twisted bilayer graphene:
Emergent symmetries, commensurate approximants,
and wannier obstructions,” Phys. Rev. B 98, 085435
(2018).
[23] Zhida Song, Zhijun Wang, Wujun Shi, Gang Li, Chen
Fang, and B. Andrei Bernevig, “All Magic Angles
in Twisted Bilayer Graphene are Topological,” Phys.
Rev. Lett. 123, 036401 (2019), arXiv:1807.10676 [condmat.mes-hall].
[24] Kasra Hejazi, Chunxiao Liu, Hassan Shapourian, Xiao
Chen, and Leon Balents, “Multiple topological transitions in twisted bilayer graphene near the first magic
angle,” Phys. Rev. B 99, 035111 (2019).
[25] Jianpeng Liu, Junwei Liu, and Xi Dai, “Pseudo Landau level representation of twisted bilayer graphene:
Band topology and implications on the correlated insulating phase,” Physical Review B 99, 155415 (2019),

arXiv:1810.03103 [cond-mat.mes-hall].
[26] Ming Xie and A. H. MacDonald, “Nature of the correlated insulator states in twisted bilayer graphene,” Phys.
Rev. Lett. 124, 097601 (2020).
[27] Nick Bultinck, Shubhayu Chatterjee, and Michael P.
Zaletel, “Anomalous Hall ferromagnetism in twisted
bilayer graphene,” arXiv e-prints , arXiv:1901.08110
(2019), arXiv:1901.08110 [cond-mat.str-el].
[28] Ya-Hui Zhang, Dan Mao, and T. Senthil, “Twisted bilayer graphene aligned with hexagonal boron nitride:
Anomalous Hall effect and a lattice model,” Physical
Review Research 1, 033126 (2019), arXiv:1901.08209
[cond-mat.str-el].
[29] Aaron L. Sharpe, Eli J. Fox, Arthur W. Barnard,
Joe Finney, Kenji Watanabe, Takashi Taniguchi,
M. A. Kastner, and David Goldhaber-Gordon, “Emergent ferromagnetism near three-quarters filling in
twisted bilayer graphene,” Science 365, 605–608 (2019),
arXiv:1901.03520 [cond-mat.mes-hall].
[30] M. Serlin, C. L. Tschirhart, H. Polshyn, Y. Zhang,
J. Zhu, K. Watanabe, T. Taniguchi, L. Balents, and
A. F. Young, “Intrinsic quantized anomalous Hall effect in a moiré heterostructure,” Science 367, 900–903
(2020), arXiv:1907.00261 [cond-mat.str-el].
[31] Shang Liu, Eslam Khalaf, Jong Yeon Lee, and Ashvin
Vishwanath, “Nematic topological semimetal and insulator in magic angle bilayer graphene at charge
neutrality,” arXiv e-prints , arXiv:1905.07409 (2019),
arXiv:1905.07409 [cond-mat.str-el].
[32] Ya-Hui Zhang, Hoi Chun Po, and T. Senthil, “Landau
level degeneracy in twisted bilayer graphene: Role of
symmetry breaking,” Phys. Rev. B 100, 125104 (2019).
[33] S. L. Sondhi, A. Karlhede, S. A. Kivelson, and E. H.
Rezayi, “Skyrmions and the crossover from the integer
to fractional quantum hall effect at small zeeman energies,” Phys. Rev. B 47, 16419–16426 (1993).
[34] Jeil Jung, Ashley M. DaSilva, Allan H. MacDonald, and
Shaffique Adam, “Origin of band gaps in graphene on
hexagonal boron nitride,” Nature Communications 6,
6308 EP – (2015).
[35] Pablo San-Jose, A. Gutiérrez-Rubio, Mauricio Sturla,
and Francisco Guinea, “Spontaneous strains and gap in
graphene on boron nitride,” Phys. Rev. B 90, 075428
(2014).
[36] B. Hunt, J. D. Sanchez-Yamagishi, A. F. Young,
M. Yankowitz, B. J. LeRoy, K. Watanabe, T. Taniguchi,
P. Moon, M. Koshino, P. Jarillo- Herrero, and R. C.
Ashoori, “Massive Dirac Fermions and Hofstadter Butterfly in a van der Waals Heterostructure,” Science 340,
1427–1430 (2013), arXiv:1303.6942 [cond-mat.mes-hall].
[37] F. Amet, J. R. Williams, K. Watanabe, T. Taniguchi,
and D. Goldhaber-Gordon, “Insulating Behavior at
the Neutrality Point in Single-Layer Graphene,” Phys.
Rev. Lett. 110, 216601 (2013), arXiv:1209.6364 [condmat.mes-hall].
[38] Jeil Jung, Arnaud Raoux, Zhenhua Qiao, and A. H.
MacDonald, “Ab initio theory of moiré superlattice
bands in layered two-dimensional materials,” Phys. Rev.
B 89, 205414 (2014).
[39] Hakseong Kim, Nicolas Leconte, Bheema L. Chittari,
Kenji Watanabe, Takashi Taniguchi, Allan H. MacDonald, Jeil Jung, and Suyong Jung, “Accurate Gap
Determination in Monolayer and Bilayer Graphene/hBN Moiré Superlattices,” Nano Letters 18, 7732–7741

16
(2018), arXiv:1808.06633 [cond-mat.mes-hall].
[40] Fengcheng Wu and Sankar Das Sarma, “Identification
of superconducting pairing symmetry in twisted bilayer graphene using in-plane magnetic field and strain,”
Phys. Rev. B 99, 220507 (2019), arXiv:1904.07875
[cond-mat.supr-con].
[41] Mathias S. Scheurer, Rhine Samajdar, and Subir
Sachdev, “Pairing in twisted double-bilayer graphene
and related moire superlattice systems,” arXiv e-prints
, arXiv:1906.03258 (2019), arXiv:1906.03258 [condmat.supr-con].
[42] T. Thonhauser, Davide Ceresoli, David Vanderbilt, and
R. Resta, “Orbital magnetization in periodic insulators,” Phys. Rev. Lett. 95, 137205 (2005).
[43] Di Xiao, Ming-Che Chang, and Qian Niu, “Berry phase
effects on electronic properties,” Rev. Mod. Phys. 82,
1959–2007 (2010).
[44] Di Xiao, Wang Yao, and Qian Niu, “Valley-contrasting
physics in graphene: Magnetic moment and topological
transport,” Phys. Rev. Lett. 99, 236809 (2007).
[45] Shuichi Murakami and Naoto Nagaosa, “Berry phase in
magnetic superconductors,” Phys. Rev. Lett. 90, 057002
(2003).
[46] Sasa Dukan and Zlatko Tesanovic, “Superconductivity in a high magnetic field: Excitation spectrum and
tunneling properties,” Phys. Rev. B 49, 13017–13023
(1994).
[47] S. M. Girvin and A. H. MacDonald, “Multicomponent
quantum hall systems: The sum of their parts and
more,” in Perspectives in Quantum Hall Effects (John
Wiley and Sons, Ltd, 2007) Chap. 5, pp. 161–224.
[48] J. P. Eisenstein and A. H. MacDonald, “Bose–einstein
condensation of excitons in bilayer electron systems,”
Nature 432, 691–694 (2004).
[49] Subir Sachdev and T. Senthil, “Zero temperature phase
transitions in quantum heisenberg ferromagnets,” Annals of Physics 251, 76 – 122 (1996).
[50] S. Das Sarma, Subir Sachdev,
and Lian Zheng,
“Double-layer quantum hall antiferromagnetism at filling fraction 2/m where m is an odd integer,” Phys. Rev.
Lett. 79, 917–920 (1997).
[51] S. Das Sarma, Subir Sachdev, and Lian Zheng, “Canted
antiferromagnetic and spin-singlet quantum hall states
in double-layer systems,” Phys. Rev. B 58, 4672–4693
(1998).
[52] Maxim Kharitonov, “Canted antiferromagnetic phase of
the ν=0 quantum hall state in bilayer graphene,” Phys.
Rev. Lett. 109, 046803 (2012).
[53] Maxim Kharitonov, “Edge excitations of the canted antiferromagnetic phase of the ν = 0 quantum hall state
in graphene: A simplified analysis,” Phys. Rev. B 86,
075450 (2012).
[54] S Pezzini, C Cobaleda, B A Piot, V Bellani, and E Diez,
“Canted antiferromagnetic to ferromagnetic phase transition in bilayer graphene,” Journal of Physics: Conference Series 647, 012044 (2015).
[55] A. F. Young, J. D. Sanchez-Yamagishi, B. Hunt, S. H.
Choi, K. Watanabe, T. Taniguchi, R. C. Ashoori, and
P. Jarillo-Herrero, “Tunable symmetry breaking and helical edge transport in a graphene quantum spin hall
state,” Nature 505, 528 EP – (2013).
[56] B. M. Hunt, J. I. A. Li, A. A. Zibrov, L. Wang,
T. Taniguchi, K. Watanabe, J. Hone, C. R. Dean,
M. Zaletel, R. C. Ashoori, and A. F. Young, “Di-

rect measurement of discrete valley and orbital quantum
numbers in bilayer graphene,” Nature Communications
8, 948 (2017).
[57] Luis A. Gonzalez-Arraga, J. L. Lado, Francisco Guinea,
and Pablo San-Jose, “Electrically controllable magnetism in twisted bilayer graphene,” Phys. Rev. Lett.
119, 107201 (2017).
[58] Alex Thomson, Shubhayu Chatterjee, Subir Sachdev,
and Mathias S. Scheurer, “Triangular antiferromagnetism on the honeycomb lattice of twisted bilayer
graphene,” Phys. Rev. B 98, 075109 (2018).
[59] Jian Kang and Oskar Vafek, “Strong coupling phases of
partially filled twisted bilayer graphene narrow bands,”
Phys. Rev. Lett. 122, 246401 (2019).
[60] Kangjun Seo, Valeri N. Kotov, and Bruno Uchoa, “Ferromagnetic Mott State in Twisted Graphene Bilayers
at the Magic Angle,” arXiv e-prints , arXiv:1812.02550
(2018), arXiv:1812.02550 [cond-mat.str-el].
[61] Xiao-Chuan Wu, Anna Keselman, Chao-Ming Jian,
Kelly Ann Pawlak,
and Cenke Xu, “Ferromagnetism and spin-valley liquid states in moiré correlated insulators,” Phys. Rev. B 100, 024421 (2019),
arXiv:1905.00033 [cond-mat.str-el].
[62] T. M. R. Wolf, J. L. Lado, G. Blatter, and O. Zilberberg, “Electrically Tunable Flat Bands and Magnetism
in Twisted Bilayer Graphene,” Phys. Rev. Lett. 123,
096802 (2019), arXiv:1905.07651 [cond-mat.mes-hall].
[63] Constantin Schrade and Liang Fu, “Spin-valley density
wave in moiré materials,” Phys. Rev. B 100, 035413
(2019), arXiv:1905.07401 [cond-mat.str-el].
[64] Yahya Alavirad and Jay D. Sau, “Ferromagnetism and
its stability from the one-magnon spectrum in twisted
bilayer graphene,” arXiv e-prints , arXiv:1907.13633
(2019), arXiv:1907.13633 [cond-mat.mes-hall].
[65] Alexander M. Polyakov and A. A. Belavin, “Metastable
States of Two-Dimensional Isotropic Ferromagnets,”
JETP Lett. 22, 245–248 (1975), [Pisma Zh. Eksp. Teor.
Fiz.22,503(1975)].
[66] K. Moon, H. Mori, Kun Yang, S. M. Girvin, A. H.
MacDonald, L. Zheng, D. Yoshioka, and Shou-Cheng
Zhang, “Spontaneous interlayer coherence in doublelayer quantum hall systems: Charged vortices and
kosterlitz-thouless phase transitions,” Phys. Rev. B 51,
5138–5170 (1995).
[67] S. M. Girvin, “The Quantum Hall Effect: Novel Excitations and Broken Symmetries,” in Topological Aspects of
Low Dimensional Systems, Vol. 69, edited by A. Comtet,
T. Jolicoeur, S. Ouvry, and F. David (Springer, Berlin,
Heidelberg, 1999) p. 53, arXiv:cond-mat/9907002 [condmat.mes-hall].
[68] Rina Takashima, Hiroaki Ishizuka, and Leon Balents,
“Quantum skyrmions in two-dimensional chiral magnets,” Phys. Rev. B 94, 134415 (2016).
[69] D. Lilliehöök, K. Lejnell, A. Karlhede, and S. L.
Sondhi, “Quantum hall skyrmions with higher topological charge,” Phys. Rev. B 56, 6805–6809 (1997).
[70] Yu. V. Nazarov and A. V. Khaetskii, “Quantum phase
transition in the skyrmion lattice,” Phys. Rev. Lett. 80,
576–579 (1998).
[71] Michael Stone, “Magnus force on skyrmions in ferromagnets and quantum hall systems,” Phys. Rev. B 53,
16573–16578 (1996).
[72] Tarun Grover and T. Senthil, “Topological spin hall
states, charged skyrmions, and superconductivity in two

17
dimensions,” Phys. Rev. Lett. 100, 156804 (2008).
[73] Eslam Khalaf, Shubhayu Chatterjee, Nick Bultinck,
Michael P. Zaletel, and Ashvin Vishwanath, “Charged
Skyrmions and Topological Origin of Superconductivity in Magic Angle Graphene,” arXiv e-prints
, arXiv:2004.00638 (2020), arXiv:2004.00638 [condmat.str-el].
[74] Cécile Repellin, Zhihuan Dong, Ya-Hui Zhang, and
T. Senthil, “Ferromagnetism in narrow bands of moir\’e
superlattices,” arXiv e-prints , arXiv:1907.11723 (2019),
arXiv:1907.11723 [cond-mat.str-el].
[75] Jianpeng Liu and Xi Dai, “Anomalous Hall effect,
magneto-optical properties, and nonlinear optical properties of twisted graphene systems,” arXiv e-prints
, arXiv:1907.08932 (2019), arXiv:1907.08932 [condmat.mes-hall].
[76] Shubhayu Chatterjee and Subir Sachdev, “Probing excitations in insulators via injection of spin currents,”
Phys. Rev. B 92, 165113 (2015).
[77] H. Zhou, H. Polshyn, T. Taniguchi, K. Watanabe,
and A. F. Young, “Solids of quantum Hall skyrmions
in graphene,” Nature Physics 16, 154–158 (2019),
arXiv:1904.11485 [cond-mat.mes-hall].
[78] Aviram Uri, Alexander Y. Meltzer, Yonathan Anahory,
Lior Embon, Ella O. Lachman, Dorri Halbertal, Naren
HR, Yuri Myasoedov, Martin E. Huber, Andrea F.
Young, and Eli Zeldov, “Electrically Tunable Multiterminal SQUID-on-Tip,” Nano Letters 16, 6910–6915
(2016), arXiv:1606.05088 [cond-mat.supr-con].
[79] Y Dovzhenko, F Casola, S Schlotter, TX Zhou,
F Büttner, RL Walsworth, GSD Beach, and A Yacoby,
“Magnetostatic twists in room-temperature skyrmions
explored by nitrogen-vacancy center spin texture reconstruction,” Nature communications 9, 2712 (2018).
[80] Jianpeng Liu, Zhen Ma, Jinhua Gao, and Xi Dai,
“Quantum valley hall effect, orbital magnetism, and
anomalous hall effect in twisted multilayer graphene systems,” Phys. Rev. X 9, 031021 (2019).
[81] Ya-Hui Zhang and T. Senthil, “Bridging hubbard
model physics and quantum hall physics in trilayer
graphene/h − BN moiré superlattice,” Phys. Rev. B 99,
205150 (2019).
[82] M. M. van Wijk, A. Schuring, M. I. Katsnelson, and
A. Fasolino, “Relaxation of moiré patterns for slightly
misaligned identical lattices: graphene on graphite,”
2D Materials 2, 034010 (2015), arXiv:1503.02540 [condmat.mes-hall].
[83] Kazuyuki Uchida, Shinnosuke Furuya, Jun-Ichi Iwata,
and Atsushi Oshiyama, “Atomic corrugation and electron localization due to moiré patterns in twisted bilayer
graphenes,” Phys. Rev. B 90, 155451 (2014).
[84] Xianqing Lin, Dan Liu, and David Tománek, “Shear
instability in twisted bilayer graphene,” Phys. Rev. B
98, 195432 (2018).
[85] Procolo Lucignano, Dario Alfè, Vittorio Cataudella,
Domenico Ninno, and Giovanni Cantele, “Crucial role
of atomic corrugation on the flat bands and energy
gaps of twisted bilayer graphene at the magic angle
θ ∼ 1.08◦ ,” Phys. Rev. B 99, 195419 (2019).
[86] Nguyen N. T. Nam and Mikito Koshino, “Lattice relaxation and energy band modulation in twisted bilayer
graphene,” Phys. Rev. B 96, 075311 (2017).
[87] Mikito Koshino, Noah F. Q. Yuan, Takashi Koretsune,
Masayuki Ochi, Kazuhiko Kuroki, and Liang Fu, “Max-

imally localized wannier orbitals and the extended hubbard model for twisted bilayer graphene,” Phys. Rev. X
8, 031087 (2018).
[88] Stephen Carr, Shiang Fang, Ziyan Zhu, and Efthimios
Kaxiras, “Exact continuum model for low-energy electronic states of twisted bilayer graphene,” Phys. Rev.
Research 1, 013001 (2019).
[89] Fengcheng Wu, A. H. MacDonald, and Ivar Martin, “Theory of phonon-mediated superconductivity in
twisted bilayer graphene,” Phys. Rev. Lett. 121, 257001
(2018).
[90] Biao Lian, Zhijun Wang, and B. Andrei Bernevig,
“Twisted bilayer graphene: A phonon-driven superconductor,” Phys. Rev. Lett. 122, 257002 (2019).
[91] Fengcheng Wu, Euyheon Hwang,
and Sankar
Das Sarma, “Phonon-induced giant linear-in-t resistivity in magic angle twisted bilayer graphene: Ordinary
strangeness and exotic superconductivity,” Phys. Rev.
B 99, 165112 (2019).
[92] Young Woo Choi and Hyoung Joon Choi, “Strong
electron-phonon coupling, electron-hole asymmetry,
and nonadiabaticity in magic-angle twisted bilayer
graphene,” Phys. Rev. B 98, 241412 (2018).
[93] Feng Wang, Weitao Liu, Yang Wu, Matthew Y. Sfeir,
Limin Huang, James Hone, Stephen O’Brien, Louis E.
Brus, Tony F. Heinz, and Y. Ron Shen, “Multiphonon
raman scattering from individual single-walled carbon
nanotubes,” Phys. Rev. Lett. 98, 047402 (2007).
[94] A. Sédéki, L. G. Caron, and C. Bourbonnais, “Electronphonon coupling and peierls transition in metallic carbon nanotubes,” Phys. Rev. B 62, 6975–6978 (2000).
[95] S. Piscanec, M. Lazzeri, Francesco Mauri, A. C. Ferrari, and J. Robertson, “Kohn anomalies and electronphonon interactions in graphite,” Phys. Rev. Lett. 93,
185503 (2004).
[96] Mikito Koshino and Young-Woo Son, “Moiré phonons
in twisted bilayer graphene,” Phys. Rev. B 100, 075416
(2019), arXiv:1905.09660 [cond-mat.mes-hall].
[97] D. M. Basko and I. L. Aleiner, “Interplay of coulomb
and electron-phonon interactions in graphene,” Phys.
Rev. B 77, 041409 (2008).
[98] NguyenAi Viet, Hiroshi Ajiki, and Tsuneya Ando,
“Lattice instability in metallic carbon nanotubes,” Journal of the Physical Society of Japan 63, 3036–3047
(1994).
[99] Hidekatsu Suzuura and Tsuneya Ando, “Phonons and
electron-phonon scattering in carbon nanotubes,” Phys.
Rev. B 65, 235412 (2002).
[100] Kohta Ishikawa and Tsuneya Ando, “Optical phonon interacting with electrons in carbon nanotubes,” Journal
of the Physical Society of Japan 75, 084713 (2006).
[101] Ken-ichi Sasaki and Riichiro Saito, “Pseudospin
and Deformation-Induced Gauge Field in Graphene,”
Progress of Theoretical Physics Supplement 176, 253–
278 (2008).
[102] G. D. Mahan, “Electron–optical phonon interaction in
carbon nanotubes,” Phys. Rev. B 68, 125409 (2003).
[103] A. Grüneis, R. Saito, T. Kimura, L. G. Cancado, M. A.
Pimenta, A. Jorio, A. G. Souza Filho, G. Dresselhaus, and M. S. Dresselhaus, “Determination of twodimensional phonon dispersion relation of graphite by
raman spectroscopy,” Phys. Rev. B 65, 155405 (2002).
[104] Jia-An Yan, W. Y. Ruan, and M. Y. Chou, “Phonon
dispersions and vibrational properties of monolayer, bi-

18

τ =−

G1

M
X

Γ
τ =−

Γ

K−
K+

τ =+
G2
b)

a)

FIG. 9: (a) The mono-layer graphene Brillouin zone with the two basis vectors G1 and G2 of the reciprocal lattice. We have indicated
the high-symmetry K points, where the Dirac cones are located, by the valley label τ = ±. (b) The mono-layer Brillouin zones of the top
and bottom graphene layer with relative twist angle θ. The vector X points from the common Γ point of the mono-layer Brillouin zones
to the center of the mini-Brillouin zone at the τ = + valley. In presence of C6 T symmetry, there are Dirac points at the K+ and K−
points of the mini Brillouin zone (which is depicted by the small hexagon).

layer, and trilayer graphene: Density-functional perturbation theory,” Phys. Rev. B 77, 125401 (2008).
[105] R M Ribeiro, Vitor M Pereira, N M R Peres, P R Briddon, and A H Castro Neto, “Strained graphene: tight-

binding and density functional calculations,” New Journal of Physics 11, 115002 (2009).
[106] S. A. Parameswaran, R. Roy, and S. L. Sondhi, “Fractional chern insulators and the W∞ algebra,” Phys. Rev.
B 85, 241308 (2012).

Supplementary material
Appendix A: moiré Hamiltonian

The spinless moiré Hamiltonian in valley +, i.e. around the K+ -points of the graphene Brillouin zone, is given by

H(k) =

X


X

htt (R(θ/2)(k + X + g1 ))δg ,g + hbb (R(−θ/2)(k + X + g1 ))δg ,g +
Tg̃tb δg1 ,g2 +g̃ + Tg̃bt δg1 +g̃,g2 
1 2
1 2

g1 ,g2

g̃

(A1)
Here, g1 and g2 lie on the moiré reciprocal lattice, R(±θ/2) is a rotation matrix over angle ±θ/2 with θ corresponding
to the first magic angle θ ≈ 1.05◦ [15]. htt (k) = −t0 h(k) + ∆t σ z (hbb (k) = −t0 h(k) + ∆b σ z ) is the mono-layer
graphene Hamiltonian of the top (bottom) layer with hopping strength t0 = 2.61 eV and a sublattice splitting ∆t σ z
(∆b σ z ). X is the position of the center of the mini-Brillouin zone at the mono-layer K+ -points as shown in Fig.9(b).
The inter-layer coupling is given by the matrices [15]

T0 =

Tg1 =

Tg2 =

w0 w1
w1 w0


(A2)

w0 w1 ω
w1 ω ∗ w0



w0 w1 ω ∗
w1 ω w0



(A3)
,

(A4)

where ω = ei2π/3 , g1 = (R(θ/2) − R(−θ/2))G1 and g2 = (R(θ/2) − R(−θ/2))G2 , with G1 and G2 the graphene
reciprocal lattice vectors shown in Fig. 9. The AB inter-layer hopping strength is w1 = 195 meV. To phenomenologically incorporate corrugation of the bilayer system [82–85] we use an AA-AB inter-layer hopping ratio w0 /w1 = 0.85
[86–88]. The moiré Hamiltonian in valley − can be obtained by acting with time-reversal on the moiré Hamiltonian
in valley +.

19
Appendix B: Phonon Hamiltonian and electron-phonon coupling

In this appendix, we review electron-phonon coupling in graphene, and phonon-mediated electron interactions in
tBLG. The potential relevance of phonons for the superconducting domes and transport in magic-angle tBLG graphene
was studied previously in Refs. [14, 89–92]. Our approach to incorporate the effects of phonons is most closely related
to that of Ref. [89], where mono-layer graphene phonons near both the Γ and K points were taken into account
(these are the modes that couple most efficiently to the electrons [93–95]). In Refs. [90, 91, 96], only long-wavelength
acoustic phonons were considered. Here, we ignore these acoustic modes, as they do not give rise to inter-valley
scattering for the electrons. The analysis below is solely based on the symmetry properties of graphene, and parallels
the approach of Ref. [97].

1.

Phonon Hamiltonian

We define the Fourier transformed displacement operators ûiq,σ for the carbon atoms and the canonical conjugate
operators p̂iq,σ as
1 X0 iq·RA i
ûA (RA )
e
ûiq,A = √
N q
1 X0 iq·(RA +δ1 ) i
ûiq,B = √
e
ûB (RA + δ1 )
N q
1 X0 −iq·RA i
p̂iq,A = √
e
p̂A (RA )
N q
1 X0 −iq·(RA +δ1 ) i
p̂iq,B = √
e
p̂B (RA + δ1 ) ,
N q

(B1)
(B2)
(B3)
(B4)

where i = x, y, σ denotes sublattice, N is the number of unit cells, RA denotes the positions of the A sublattice sites,
δ1 is one of the three vectors δl (l = 1, 2, 3) pointing from the A sublattice sites to the neighboring B sublattice sites.
Recall that we define primed sums to run over the graphene Brillouin zone. We only consider in-plane displacements,
as the out-of-plane displacements couple only weakly to the electrons. Using the combined four-dimensional index
ν = (i, σ), the phonon Hamiltonian can be written as


X
1 X0  1 X
Hph =
p̂q,ν p̂†q,ν + 2
ûq,ν D(q)νν 0 û†q,ν 0 
2 q
M ν
0
ν,ν


X
1 X0  1 X
†
j
†

p̂ν ejq,ν ej∗
=
ûq,ν ej∗
q,ν λq,j eq,ν 0 ûq,ν 0
q,ν 0 p̂ν 0 + 2
2 q
M 0
0
ν,ν ,j
ν,ν ,j


X
1 X0  1 X
p̂q,j · p̂†q,j + 2
ûq,j λq,j û†q,j  ,
=
2 q
M j
j
where M is the carbon atom mass. Using ωq,j =
as

(B5)

(B6)

(B7)

p
2λq,j /M , we define the phonon annihilation and creation operators

i
bq,j = p
p̂† +
2M ~ωq,j q,j

s

−i
p̂q,j +
2M ~ωq,j

s

b†q,j = p

λq,j
ûq,j
~ωq,j

(B8)

λq,j †
û
~ωq,j q,j

(B9)

In terms of the creation and annihilation operators, the phonon Hamiltonian becomes

20

Hph =

X0 X
q

j



1
~ωq,j b†q,j bq,j +
2

(B10)

Using the eigenvectors of the phonon Hamiltonian we can write the displacement operator in second quantization as

X0

ûν (r) =

s
~
(bqj + b†−qj )ejqν e−iq·r ,
2N M ωq,j

q,j

(B11)

For future convenience, we also introduce the notation
bq,j ≡ hejq |bq i
X
=
ej∗
q,ν bq,ν

(B12)
(B13)

ν

X

=

i
p
p̂†q,ν +
2M ~ωq,j

ej∗
q,ν

ν

2.

s

λq,j
ûq,ν
~ωq,j

!
(B14)

Electron-phonon coupling in graphene

In a tight-binding approximation, the only coupling between electrons and lattice vibrations occurs via the associated
spatial modulation of the tight binding parameters. In the case of graphene we write the tight-binding Hamiltonian
coupled to small lattice vibrations as [98–102]

H = −t0

X 3
X

3

†
ψR
ψRA +δl −
A

RA l=1

RA l=1

≈ −t0

X
X 3

∂t0 X X
†
(|δl + uA (RA ) − uB (RA + δl )| − aCC ) ψR
ψRA +δl + h.c.
A
∂aCC

†
ψR
ψRA +δl −
A

3

1

∂t0 X X
†
δl · (uA (RA ) − uB (RA + δl ))ψR
ψRA +δl + h.c.
A
aCC ∂aCC

(B15)

RA l=1

RA l=1

where t0 is the graphene hopping strength, aCC = |δl | the distance between two carbon atoms. Going to momentum
space, the electron-phonon coupling Hamiltonian becomes
3


∂t0 X0 X
†
δl · uA (q) − uB (q)e−iq·δl e−ik·δl ψk+q,A
ψk,B + h.c.
(B16)
aCC ∂aCC
k,q l=1
s
3


1 ∂t0 X0 X X
~
†
=−
ψk,B (bqj + b†−qj )
δl · ejq,A − ejq,B e−iq·δl e−ik·δl ψk+q,A
aCC ∂aCC
2N
M
ω
q,j
j

He−ph = −

1

k,q

l=1

By defining the vectors

|Vq,k i =

3 
X

δl eik·δl , −δl ei(k+q)·δl



,



|ejq i = ejq,A , ejq,B

(B17)

l=1

we can write the electron-phonon coupling Hamiltonian as

He−ph = −g̃

X X0
j

q,k

−1/2

†
ωq,j hVq,k |ejq i ψk+q,A
ψk,B (bqj + b†−qj ) + h.c.

(B18)

21
q
∂t0
~
1
where g̃ = aCC
2N M ∂aCC . Let us now examine how the symmetries of graphene are realized in this Hamiltonian.
We first consider the three-fold rotation symmetry group C3v and define the rotation matrix R3

R3 =

cos(2π/3) sin(2π/3)
− sin(2π/3) cos(2π/3)




=

√

3/2
−1/2
√
.
− 3/2 −1/2

(B19)

C3v symmetry of the phonon Hamiltonian implies that


D(R3 q) = R† D(q)R ,

with R =



R3
R3

,

(B20)

from which it follows that ωq,j = ωR3 q,j and R|ejq i = eiαq |ejR3 q i. The C3v symmetry of the electron-phonon Hamiltonian implies that
−1/2

−1/2

ωR3 q,j hVR3 q,R3 k |ejR3 q ihejR3 q |R|bq i = ωq,j hVq,k |ejq ihejq |bq i ,

(B21)

Because ωR3 q,j = ωq,j , we can see that this is true by doing following steps
hVR3 q,R3 k |ejR3 q ihejR3 q |R|bq i = hVR3 q,R3 k |RR† |ejR3 q ihejR3 q |R|bq i

(B22)

= e−iαk hVR3 q,R3 k |R|ejR3 q ihejq |bq ieiαk

(B23)

= hVq,k |ejq ihejq |bq i

(B24)

The C2v symmetry can be derived in a similar way, with the main difference that C2v interchanges the A and B
sublattices. So C2v symmetry implies that
−1/2

−1/2

ω−q,j hV−q,−k |ej−q ihej−q |R̃|bq i = ω−q,j hV−q,k+q |ej−q i∗ hejq |bq i ,


with R̃ =


−1
−1

(B25)

Equality (B25) follows from the definition of |Vk,q i, the C2v rotation symmetry of the phonon Hamiltonian which
implies that R̃|ejq i = eiβq |ej−q i, and |ejq i = |ej−q i∗ , which follows from hermiticity of the displacement operator. Time
reversal symmetry of the electron-phonon Hamiltonian in Eq. (B18) is more straightforward to see, as this simply
follows from the properties |V−q,−k i∗ = |Vq,k i and |ej−q i∗ = |ejq i.
We now focus on the coupling between lattice-scale phonons and low-energy electrons at the Dirac
cones. √
So in the

above electron-phonon Hamiltonian we fix both k and q to either K or −K, where K = 4π
3aCC is
,
0
and
a
=
3a
the graphene lattice constant. Specifically, the terms we are interested in are
He−ph ≈ −g̃

X

−1/2

†
ωK,j hVK |ejK iψ−K,A
ψK,B (bKj + b†−Kj )

(B26)

j

−g̃

X

−1/2

†
ωK,j hVK |ejK i∗ ψK,A
ψ−K,B (b−Kj + b†Kj ) + h.c. ,

j

where |VK i = |VK,K i. Let us now choose a basis in which the δl take the form
√
δ1 = aCC (0, 1) , δ2 = aCC

3 1
,−
2
2

√

!
= R3 δ1 ,

δ3 = aCC

3 1
−
,−
2
2

!
= R3 δ 2

(B27)

from which we see that eiK·δ1 = 1, eiK·δ2 = e2πi/3 ≡ ω and eiK·δ3 = ω 2 = ω −1 . The phonon Hamiltonian at the K+
point satisfies
†

R D(K)R = D(R3 K) = D(K − G2 ) =


1


e−iG2 ·δ1 1

D(K)


1


eiG2 ·δ1 1

,

(B28)

22
where we have used that R3 K = K − G2 , with G2 = √4π
3a

√

3 1
2 , 2



a reciprocal lattice vector. The last equality follows

from bq+G,A,xi = bq,A,xi and bq+G,B,xi = e
bq,B,xi for any reciprocal lattice vector G. Using that eiG2 ·δ1 = ω,
we see that the matrix R− = R3 ⊕ ω −1 R3 commutes with D(K). This means that the eigenvectors ejK are also
eigenvectors of R− , which has two non-degenerate eigenvalues 1 and ω −1 , and one two-fold degenerate eigenvalue ω.
The vector |VK i can be written as |VK i = |VKA i + |VKB i, where
iG·δ1

|VKA i =

3
X


δl eiK·δl , 0 ,

|VKB i =

l=1

3
X

0, −δl ei2K·δl



(B29)

l=1

These vectors have the property R− |VKA i = ω −1 |VKA i and R− |VKB i = |VKB i. This means that only two of the four
inner products hVK |ejK i are non-zero. The eigenvectors |ejK i which can couple to the electrons are those which have
eigenvalue 1 and ω −1 under R− . We can thus express |VK i in terms of the eigenvectors |ejK i as follows:

√

1
2
1
1
|VK i = √ (eiθK |e1K i + eiθK |e2K i) ,
6aCC
2

(B30)

This allows us to write the electron-phonon Hamiltonian as
j
j
2
X
eiθK †
e−iθK †
†
He−ph = −g̃ 3aCC
ψ−K,A ψK,B (bK,j + b−Kj ) + √
ψK,A ψ−K,B (b−K,j + b†Kj ) + h.c.
√
ω
ω
Kj
Kj
j=1

√

j

j

j

(B31)

j

From C2v symmetry we know that eiθK = eiθ−K = e−iθK , which implies that eiθK is real and can be absorbed in bK,j
and b†−K,j . So the final form for the electron-phonon coupling between lattice-scale phonons and low-energy electrons
at the K points is simply

He−ph = −g

2
X
j=1

√


1  †
†
ψ−K,A ψK,B (bK,j + b†−Kj ) + ψK,A
ψ−K,B (b−K,j + b†Kj ) + h.c. ,
ωK,j

(B32)

q
0
. Because the graphene phonon bands have little dispersion around the K-points [99, 103, 104],
where g = 2N3~M ∂a∂tCC
we will now simply ignore any momentum dependence and simply assume that (B32) holds for electrons close to the
K-points. We will also take ωK,1 = ωK,2 = ω0 .

3.

Phonon mediated electron interactions

The Hamiltonian describing the combined electron-phonon system, projected into the flat bands, takes the form

H = He + Hph + He−ph ,

(B33)

P
†
with He =
k,τ,s εk,τ ck,τ,s ck,τ,s . For the phonon Hamiltonian we take just two copies of the graphene phonon
Hamiltonian:

Hph =

XX
q,g l,j


~ωq+g,l,j

1
b†q+g,l,j bq+g,l,j +

2


,

(B34)

where q is defined to lie in the mini-Brillouin zone. We don’t consider out-of-plane phonon modes as these couple only
to the inter-layer tunneling, which is much smaller than the intra-layer hopping. Correspondingly, the electron-phonon
Hamiltonian is just two copies of Eq. (B32). If we project this into the flat bands, we get

23



g X X
He−ph = − √
hu−τ (k + q)|σ x Pl Sg |uτ (k)ic†k+q,−τ,s ck,τ,s bq+g+2τ X,l,j + b†−q−g−2τ X,l,j
ω0
τ,l,j,g k,q,s


g X X τ
fl,g (q, k)c†k+q,−τ,s ck,τ,s bq+g+2τ X,l,j + b†−q−g−2τ X,l,j ,
≡ −√
ω0

(B35)
(B36)

l,j,g k,q,τ,s

Using a Schrieffer-Wolff transformation we obtain following phonon-mediated electron interaction Hamiltonian
−τ
τ
fl,g
(k, q)fl,−g
(k0 , −q)
2g 2 X X X
0
c†
c
c†
c 0
~ω0
2 − (~ω )2 k+q,−τ,s k,τ,s k0 −q,τ,s0 k ,−τ,s
ω0
(ε
−
ε
)
k+q,−τ
k,τ
0
k,k0 ,q τ,s,s0 l


2g 2 ~ X X X X τ
−τ
≈−
fl,g (k, q)fl,−g
(k0 , −q) c†k+q,−τ,s ck,τ,s c†k0 −q,τ,s0 ck0 ,−τ,s0 ,
(~ω0 )2
0
0
τ

HP H =

k,k ,q s,s

l,g

where we have again ignored the phonon dispersion, and also the flat band dispersion. The interaction strength gph
used in the main text is
3~2 β 2
gph =
2M (~ω0 )2



t0
aCC

2
,

(B37)

where β = ∂ ln t0√
/∂ ln aCC . The numerical value gph ≈ 630 meV can be obtained by using ~ω0 = 0.16 eV, t0 = 2.61
eV, aCC = 0.25/ 3 nm and β = 3 [89, 105].
Appendix C: Spin stiffness in a spin polarized flat Chern band

In this section we derive an expression for the spin stiffness associated with a spin polarized flat Chern band. The
spin stiffness ρs appears in a long-wavelength description as the coefficient of the gradient term in the effective action
describing spin fluctuations:
ρs
2

Z

dr (∇n)2

(C1)

To derive ρs within mean-field theory, we generalize the calculation of Ref. [66] for a spin-polarized lowest Landau
level to a Chern insulator. We assume that in the ground state the spins are polarized in the z-direction. We create
a non-homogeneous spin texture by acting with eiÔ on the uniformly polarized ground state wave function. The
operator eiÔ is defined as
eiÔ = ei

P

r Ω(r)·S(r)

= ei

P

q Ω(q)·S(−q)

,

(C2)

where S(r) is the spin operator at site r. We will assume that the resulting spin texture consists only of small
fluctuations around the z-direction, such that Ω(r) ≈ ẑ × n(r), and
is slowly varying in space. If we project eiÔ in
P
i q Ω(q)·Sµ (−q)
iÔµ
a Chern band with band label µ, the resulting operator e
=e
is defined using the projected spin
operator
1 X
s
1 X
s
Sµ (−q) = √
huµ (k − q)|uµ (k)ic†k−q,µ ck,µ ≡ √
λµ (−q, k)c†k−q,µ ck,µ ,
2
2
N k
N k

(C3)

where the operator c†k,µ creates an electron with crystal momentum k in band µ, N is the number of unit cells,
s = (sx , sy , sz ) are the Pauli spin operators, and |uµ (k)i are the periodic Bloch states. From now on, we will drop
the band index µ. This should not cause any confusion, as we are always considering the same single band.
We are interested in the energy increase associated with the spin texture in the small |q| limit, which we get from

24

δE = heiÔ He−iÔ i − hHi
(C4)
1
(C5)
= ih[Ô, H]i − h[Ô, [Ô, H]]i + · · ·
2
P
For the Hamiltonian we use a general density-density interaction k Ṽ (k) : ρ(k)ρ(−k) : , projected into the flat Chern
band. So the commutator we need to calculate is
[Ô, H] =

XX
k,q

Ωi (q)Ṽ (k)[S i (−q), ρ(k)ρ(−k)]

(C6)

i

We can easily evaluate this by applying the identity
[S i (−q), ρ(k)ρ(−k)] = [S i (−q), ρ(k)]ρ(−k) + ρ(k)[S i (−q), ρ(−k)]
(C7)
P
Using the explicit expression ρ(k) = √1N k0 λ(k, k0 )c†k0 +k ck0 for the projected density operator, and Eq. (C3), we
find

[S i (−q), ρ(k)] =

si
1 X
(λ(k, k0 )λ(−q, k + k0 ) − λ(k, k0 − q)λ(−q, k0 )) c†k0 +k−q ck0
N 0
2

(C8)

si
1 X
Λk0 ,k,−q c†k0 +k−q ck0
N 0
2

(C9)

k

≡

k

and thus

[Ô, H] =


X
1 X i
σi
σi
Ω (q)Ṽ (k)
Λk0 ,k,−q c†k0 +k−q ck0 ρ(−k) + Λk0 ,−k,−q ρ(k)c†k0 −k−q ck0
N
2
2
0
i,k,q

(C10)

k

The expectation value of this commutator with respect to the homogeneously z-polarized Slater determinant vanishes
because Ωz = 0.
The double commutator determining the energy change in second order becomes

[Ô, [Ô, H]] =

1 X X
Ωi (q1 )Ωj (q2 )Ṽ (k) ×
N i,j
k,q1 ,q2

X
si
si
†
†
j
j
Λk0 ,k,−q1 [S (−q2 ), ck0 +k−q1 ck0 ρ(−k)] + Λk0 ,−k,−q1 [S (−q2 ), ρ(k)ck0 −k−q1 ck0 ] (C11)
2
2
0
k

Evaluating the expectation value of this double commutator is tedious, but straightforward. We find

h[Ô, [Ô, H]]i =

1 X i
Ω (q)Ωi (−q)Ṽ (k)
N2
i,k,q
X
×
Λk0 ,k,−q (λ(q, k0 + k − q)λ(−k, k0 + k) − λ(q, k0 − q)λ(−k, k0 + k − q))

(C12)

k0

To simplify the product of form factors λ, we work up to second order in q, because by assumption Ω(q) is a fast
decaying function. The interaction V (k) is in general not decaying fast enough to justify working up to second order in
k. However, the expectation value of the double commutator contains factors of the form λ(k, k0 ) = hu(k + k0 )|u(k0 )i,
which are expected to decay very fast in |k|. So this decay does allow us to work up to second order in k, but we need
to explicitly keep the function f (k, k0 ) = |λ(k, k0 )|. We expect the decay of the form factors not to vary too much
over the Brillouin zone, so we will use the function f (k) = |λ(k, k0 )| for a fixed representative k0 in the Brillouin
zone to enforce the fast decay in |k| (for example, Ref. [19] chose k0 = 0). The Taylor expanded expressions for the

25
form factors contain a term proportional to the Berry connection, which provides the connection between a Landau
level and a Chern band, as noted in Ref. [106]. After a few straightforward manipulations, we find for the energy
difference
X
1 X i
i
2
F(k0 )2 f 2 (k)
Ω
(q)Ω
(−q)
Ṽ
(k)(q
∧
k)
8N 2
0
i,k,q
k
!
!
X
X
X
1
1
1
=
F(k0 )2
Ṽ (k)f 2 (k)|k|2
(iq j Ωi (q))(−iq j Ωi (−q))
16 N 0
N
i,j,q
k
k
!
!
X
X
X
1
1
1
0 2
2
2
F(k )
Ṽ (k)f (k)|k|
(∇Ωi (r)) · (∇Ωi (r))
=
16 N 0
N
i,r
k
k
Z
ρs
d2 r (∇n)2 ,
→
2

δE =

(C13)

(C14)

(C15)
(C16)

where in the second line we have used (q ∧ k)2 = |q|2 |k|2 sin2 α, where α is the angle between q and k. Because Ṽ (k)
and to a good approximation also f (k) are isotropic, we can replace sin2 α by its average value 1/2. So we arrive at
the following Hartree-Fock expression for the spin stiffness
1
ρs =
8A

1 X
F(k0 )2
N 0
k

!

1 X
Ṽ (k)f 2 (k)|k|2
N

!
,

(C17)

k

where A is the area of the unit cell. In the continuum limit, the factor A−1 is interpreted as the charge density [47].

Appendix D: Skyrmion energetics
1.

Single skyrmions

In this section, we present an explicit evaluation of the energy of a skyrmion in a single-valley, using the twocomponent non-linear σ model discussed in Eq. (28), which we recall below for completeness. We assume that while
a skyrmion forms in a single valley, the spins in the other valley remain in their equilibrium configuration. We first
look at the ferromagnet.


Z
X 
ρs
nS 2 ρ̄s
1
2
L=
nS A[nτ ] · ∂t nτ (r) + gs µB B · nτ (r) − (∇nτ (r)) −
[(n+ (r) − n− (r)]2 −
dr 0 V (r − r 0 )ρ(r)ρ(r 0 )
2
2
2
τ =±
(D1)
We henceforth set S = 1/2 for the electron spin. We consider a single isolated skyrmion in valley + (say), completely
characterized by a complex function W (z) (see Eq. (29)) As shown by Belavin and Polyakov, any analytic complex
function W (z) with a single pole minimizes the elastic energy E el to be 4πρs [65], and the size of a charged skyrmion
in a Chern band is therefore determined by the competition between the effective Zeeman and Coulomb energies [33].
A skyrmion of linear size R can be described by W (z) = R/z, or more explicitly by


2xR
2yR r2 − R2
n+ (r) =
,
,
, and n− (r) = (0, 0, 1)
(D2)
r 2 + R2 r 2 + R2 r 2 + R2
We want to optimize the size R as a function of the ratio of effective Zeeman energy ∆ (which is a combination of
the external magnetic field B = B⊥ ẑ and the internal exchange field from the other valley ρ̄s n− (r) = ρ̄s ẑ) to the
Coulomb energy, i.e, g̃ which we define below.
g̃ ≡

∆
gs µB B̃
ρ̄s
=
, where B̃ = B⊥ +
2
e
EC
2gs µB
4πa

(D3)

M

If we naively use the effective Hamiltonian from Eq. (D1) to compute the energy, the Zeeman term will diverge as
a very large number of spins are flipped in our ansatz in Eq. (D2). There is a natural cutoff set by the correlation

26
length of spin fluctuations, as the Goldstone mode in a single valley gets gapped in presence of the effective magnetic
field B̃. In particular, we can use the equation of motion derived from Eq. (D1) to get the dispersion of a neutral
spin-wave.




2ρs 2
∂ψ+
2ρs 2
∂n+
=
∇ n+ + gs µB B̃ ẑ × n+ =⇒ i
=
∇ − gs µB B̃ ψ+ where ψ+ = n+,x + in+,y
∂t
n
∂t
n
2ρs 2
2ρs 2
=⇒ ωk =
k + gs µB B̃ ≡
(k + ξs−2 )
(D4)
n
n
1/2
 √
1/2
≈ E∆C
This implies that the spin-correlations fall off exponentially beyond a length-scale set by aξMs ≡ g µ3ρsB̃
,
s

B

2
is the density of electrons per band, and we have used that the spin-stiffness ρs is set by the Coulomb
where n = √3a
2
M

2

e
. Note that we treat  as a phenomenological dielectric constant that also takes into account
energy scale EC = 4πa
M
the renormalization of the bare Coulomb energy due to projection to the relevant flat bands. Therefore, we can write
down the total excitation energy of the skyrmion as the sum of the elastic contribution Eel , the effective Zeeman
contribution EZ and the Coulomb contribution.
Z
Z
gs µB B̃ κξs 2
1
d2 q
Esk = 4πρs + √ 2
V (q)ρq ρ−q
(D5)
d r [1 − nz (r)] +
2
(2π)2
3aM 0

The first term, which is the elastic contribution, is independent of the size of the skyrmion [65]. The effective Zeeman
energy, with a cutoff κξs for the domain of integration is given by (the additional scale factor of κ is added for later
analytical convenience)

 2
Z
gs µB B̃ κξs 2
R + (κξs )2
2πgs µB B̃R2
√
√
EZ =
(D6)
ln
d r [1 − nz (r)] =
R2
3a2M 0
3a2M
1
We first discuss the case of unscreened Coulomb interaction V (r) = 4πr
, Ras would be expected for a dilute gas
1
of skyrmions in the absence of gate-screening. Therefore, we take V (q) = d2 r V (r)eiq·r = 2q
and compute the
Coulomb energy
Z
R2
1
=⇒
ρ
=
d2 r ρ(r)eiq·r = −qR K1 (qR)
ρ(r) = − µν n · (∂µ n × ∂ν n) = −
q
8π
π(r2 + R2 )2
Z
Z ∞
1
e2
d2 q
3πe2
2
=⇒
V (q)ρq ρ−q =
(D7)
dt [tK1 (t)] = 8
2
2
(2π)
8πR 0
2 R

Now, we parametrize the size of the skyrmion by R = κaM (roughly speaking, κ2 counts the number of flipped spins),
and minimize the skyrmion energy Esk in Eq. (D5) as a function by κ.

 8 

 
−1/3
2π
EC
2
∆
3π 2 EC
EC
√
Esk (κ) = 4πρs + √ ∆κ2 ln 1 +
+
=⇒
κ
=
ln
1
+
optimal
∆
26 κ
∆
3
3 3π EC
Hence, we finally find that the energy of optimal size skyrmion is given by
 
1/3

 
1/3
 5 5 1/3 
∆
EC
∆
EC
3 π
√
ln 1 +
≈ 4πρs + 1.75 EC
ln 1 +
Esk = 4πρs + EC
EC
∆
EC
∆
213 3

(D8)

(D9)

We immediately see that our analytical estimate of Esk in Eq. (27) receives a logarithmic correction. For small
Zeeman fields B⊥ and intervalley coupling ρ̄s , the energy of the skyrmion grows as Esk (∆) ≈ [∆ ln(EC /∆)]1/3 . At
larger fields (when the Zeeman energy becomes roughly of the order of the Coulomb energy) the size of the skyrmion
will saturate, but an accurate estimate of the required magnetic field depends on lattice scale physics, and cannot be
obtained from the low-energy field theory.
Next, we turn to the effects of screening of the Coulomb interaction, which is relevant due to the metallic gates
used on twisted bilayer graphene (see Eq. (6)). Since the long-range (small q) nature of the Coulomb interaction is
responsible for the 1/R scaling of the Coulomb energy with skyrmion size, we expect this scaling and thereby the
optimal size and energy of the skyrmion to be significantly affected by screening. We assume that the gate-screened
Coulomb interaction takes the following form discussed in Eq. (6). In the limit of small linear size of the skyrmion
compared to the screening length D, i.e, R  D, screening effects are irrelevant and our previous result for the
skyrmion energy holds (Eq. (30)). However, the more relevant limit (where our continuum theory is likely to work

27
better) is the large skyrmion size limit with R  D, as the screening length is typically of the order of a few moiré
lattice spacings aM . In this limit, the interaction term reduced to a short-range (contact-like) term. More precisely,
the Fourier transformed charge density ρq is significant only for q . 1/R; in this regime qD  qR and therefore
2
Vscreened (q) ≈ e2D . Using Eq. (D5) and parametrizing R = κaM , we repeat the previous computations and find that
our results for optimal size and energy are altered as follows for D ≈ aM (α is an O(1) numerical constant).


 
−1/2
 
1/2
∆
∆
EC
EC
, and Esk = 4πρs + αEC
(D10)
κoptimal ∝
ln 1 +
ln 1 +
EC
∆
EC
∆
We note that the energy of the skyrmion grows as Esk (∆) ≈ [∆ ln(EC /∆)]1/2 as a function of the magnetic field in
this case. Therefore, it is reasonable to expect that Esk (∆) ≈ [∆ ln(EC /∆)]ν for some ν ∈ (1/3, 1/2) will accurately
capture intermediate screening. Irrespective of the exact value of the exponent ν, the estimate for the saturation
√
lengthscale for the skyrmion remains identical, i.e, `B̃ ≈ a0 aM .
Finally, we discuss how the energetics of the skyrmion in a magnetic field are significantly different for a spin-valley
locked state. In this case, the low energy Lagrangian density is given by:


Z
X 
ρs
nS 2 ρ̄s
1
2
L=
nS A[nτ ] · ∂t nτ (r) + gs µB B · nτ (r) − (∇nτ (r)) −
dr 0 V (r − r 0 )ρ(r)ρ(r 0 )
[(n+ (r) + n− (r)]2 −
2
2
2
τ =±
(D11)
In presence of a magnetic field B⊥ , the ground state is a canted antiferromagnet, with spins in each valley canting
towards B⊥ . The optimal canting angle θ0 (B⊥ ) can be obtained by minimizing the local energy for a spatially uniform
ground state with n+ = (cos θ, 0, sin θ), n− = (cos θ, 0, − sin θ).
gs µB
ρ̄s
ρ̄s
B · (n+ + n− ) + (n+ + n− )2 = −gs µB B⊥ sin θ +
sin2 θ;
2
8
2
(
g s µ B B⊥
, B⊥ ≤ gsρ̄µsB
∂E
ρ̄s
= 0 =⇒ sin θ0 =
∂θ θ=θ0
1, otherwise
E(θ) = −

(D12)

We now find the effective magnetic field Beff acting on the (ferromagnetic) spins of a single valley (say +), which will
determine the magnon gap ∆. We expect Beff,+ to be parallel to the ferromagnetic order parameter n+ at equilibrium;
we show that this is explicitly true below (taking êk and ê⊥ to be the axes parallel and normal to n+ (θ0 )).




ρ̄s
ρ̄s
ρ̄s
ρ̄s
Beff,+ = B⊥ ẑ −
n− (θ0 ) = B⊥ sin θ0 +
cos(2θ0 ) êk + B⊥ cos θ0 −
sin(2θ0 ) ê⊥ =
êk
2gs µB
2gs µB
2gs µB
2gs µB
(D13)
Therefore, the Zeeman gap for each valley is given by
(
∆ = gs µB |Beff | =

ρ̄s
ρ̄s
2 , B⊥ < gs µB
gs µB B⊥ − ρ̄2s , B⊥ ≥ gsρ̄µsB

(D14)

Therefore, we find that the unlike the ferromagnet, the Zeeman gap ∆ initially remains fixed as the spins in each
valley reorient in the ground state to give a canted antiferromagnet, and only starts to increase beyond a critical field
of Bc = ρ̄s /(gs µB ). This implies that the skyrmion size and the charge gap (due to charge e skyrmions) also remains
fixed till Bc . On further increasing B⊥ beyond Bc , we get analogous behavior to the ferromagnet, as the skyrmion
begins to shrink in size and increase in energy as (B⊥ − Bc )ν with logarithmic corrections.
2.

Skyrmion pairs

In this section, we compute energy of skyrmion pairs, and discuss the situations where skyrmion pairing is favored at
the lowest energy scales. First, let us consider the ferromagnet with hsz i 6= 0, and discuss pairing between skyrmionic
charges in the same valley. This will be the case when the inter-valley coupling J 0 is much smaller than the intravalley coupling J, as such a scenario will prefer the spins within the same valley to be aligned at the small cost of
misalignment of spins in opposite valleys. For a charge 2e pair, we need the skymions to carry the same Pontryagin
index but opposite phases. Therefore, consider the skyrmion pair ansatz given by:
W (z) =

R
R
−
z−L z+L

(D15)

28
The elastic energy for W (z) with 2 poles is 8πρs , while the effective Zeeman energy is given by:
Z
ρ̄s
gs µB B̃ ∞ 2
Z
d r [1 − nz (r)], where, as before B̃ = B⊥ +
Epair
= √ 2
gs µB
3aM 0

(D16)

We now expect the logarithmic divergence to be cut off by L instead of ξs , which we verify by an explicit calculation
below.
Z
Z 2π
2(2LR)2
gs µB B̃ ∞
Z
√
Epair =
dr
r
dθ
r4 − 2L2 r2 cos(2θ) + D4 + (2LR)2
3a2M 0
0
Z
∞
16πgs µB B̃R2 L2
2π
√ 2
=
dr r p
4 − L4 + 4D 2 R2 )2 + 16L6 R2
3aM
(r
0
 
8πgs µB B̃R2
2L
R
√ 2
≈
ln
for
1
(D17)
R
L
3aM
The Coulomb energy of interaction between the skyrmions (labeled ± according to their centers at ±L x̂) can be
written down as:
Z
d2 q
C
Epair
V (q)ρ+,q ρ−,−q where ρ±,q = ρq e±iq·Dx̂
= e2
(2π)2
Z ∞
e2
dq (qR)2 [K1 (qR)]2 J0 (2qL)
(D18)
=
4π 0
The integral in Eq. (D18) is cut off at q ≈ 1/L in the limit of small R/L (skyrmion sizes are small compared to their
separation), while for small separation 2L compared to the skyrmion size R it is cutoff by q ≈ 1/R. Recall that 2L is
the separation between the skyrmions, so in the limit of small R/L we can write down the net energy of the skyrmion
pair as follows (neglecting the self-Coulomb energy).
 
8πgs µB B̃R2
2L
e2
elastic
Z
C
√ 2
Epair = Epair + Epair + Epair = 8πρs +
ln
(D19)
+
R
4π(2L)
3aM
It is evident from Eq. (D19) that there is a minima in the energy at a finite separation 2L, and therefore a bound state
2
of two skyrmions will be formed. Minimizing Epair (L) in Eq. (33) as a function of L, we find that 2L ≈ aRM `2B̃ /a0
as the optimal separation between the skyrmions of size R. Since the inter-valley coupling ρ̄s is the smallest scale
in the problem, the corresponding magnetic length `B̃ will be very large and therefore our assumption of L  R is
self-consistent. We carefully note that the mean-separation 2L between the two skyrmions needs to be less than ξs , as
at very large distances greater than ξs only the repulsive Coulomb interaction, which disfavors pairing, operates [70].
1/2
Recall that ξs = E∆C
aM , so such a regime always exists as long as the effective Zeeman energy is not too large.
Further, as discussed in the main text (see also Ref. [70]), such a skyrmion pair carries spin, so the superconductor
obtained by skyrmion-pairing also breaks spin-rotation (and time-reversal) symmetry.
Skyrmionic charges pairing from opposite valleys need to have opposite Pontryagin indices so that they have the
same physical charge (because of their opposite Chern numbers). There are two ways to do so: n → −n (which will
cost a huge amount of energy in a large system as spins far away are antialigned) and n = (nx , ny , nz ) → (−nx , ny , nz )
or (nx , −ny , nz ), which will be relatively more favorable from energetic considerations. In either case, the skyrmion
pair configuration does not lead to a gain in the effective Zeeman energy (unlike the previous scenario) as there is no
quenching of the perpendicular components of the spin at distances larger than the skyrmion separation. Neither can it
gain energy from alignment of spins in opposite valleys by having the two skyrmions sit on top of each other (D . R),
as the requirement of opposite Pontryagin index forces the effective Zeeman energy to add up (it is approximately
2π ρ̄s (R/aM )2 ln(ξs /R) in the continuum limit), and further, the Coulomb energy of placing two charges on top of each
other also becomes large. Therefore, we conclude that there is no binding glue for skyrmions from opposite valleys in
the ferromagnet. On the contrary, both Coulomb and Zeeman energy favors a charge-neutral skyrmion-pairing from
opposite valleys, resulting in a time-reversal symmetry breaking intervalley coherent phase as discussed in the main
text.
Next, we turn to the spin-valley locked state. Once again, we start by discussing pairing between skyrmions in
the same valley at zero external magnetic field (B⊥ = 0). Skyrmions with opposite phases still lead to an effective
Zeeman energy (as B̃ ∝ ρ̄s 6= 0) which is logarithmic in their separation for D  R. The energy of the skyrmion pair
is given by
 
8π ρ̄s R2
2L
e2
elastic
Z
C
Epair = Epair
+ Epair
+ Epair
= 8πρs + √ 2 ln
+
(D20)
R
4π0 (2L)
3aM

29
which is identical to Eq. (33) for the ferromagnet at zero external magnetic field (B⊥ = 0). To summarize, the physics
of pairing is analogous to the corresponding ferromagnetic case, and the skyrmion pair will also carry a large spin.
Finally, we discuss the pairing between skyrmions in opposite valleys for the spin-valley locked state. In this case,
skyrmion from one valley and an anti-skyrmion from the opposite valley can prevent any loss of inter-valley exchange
energy by simply sitting on top of each other and locally satisfying n+ (r) = −n− (r). Such a configuration has twice
the charge of a single-valley skyrmion, so its Coulomb energy goes as 1/R where R is its size, and can be almost
negligible for a large enough skyrmion-sizes. In the limiting case of R → ∞, the energy of this skyrmion pair is simply
8πρs . Such a skyrmion-antisykrmion pair thus avoids both the effective Zeeman energy cost by keeping spins from
opposite valleys locally anti-aligned, and Coulomb energy cost by distributing the charge over a large lengthscale; it
is the minimum energy skyrmion pair.


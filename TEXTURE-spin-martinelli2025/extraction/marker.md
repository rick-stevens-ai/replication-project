Multipoles as quantitative order parameters for altermagnetic spin splitting
Francesco Martinelli,∗ Anouk Droux, and Claude Ederer†

arXiv:2512.17587v1 [cond-mat.mtrl-sci] 19 Dec 2025

Materials Theory, ETH Zürich, Wolfgang-Pauli-Strasse 27, 8093 Zürich, Switzerland
(Dated: December 22, 2025)
We establish a quantitative relation between the altermagnetic spin-splitting and different higher
order multipoles of the charge and magnetization density around the magnetic atoms. Magnetic
multipoles such as octupoles or triakontadipoles have been suggested as potential ferroic order
parameters for d- and g-wave altermagnetism, respectively, based mainly on qualitative symmetry
arguments. We use first-principles-based electronic structure calculations to establish a clear quantitative relation between the strength of the altermagnetic spin splitting and the magnitude of certain
local multipoles. We vary the magnitude of these multipoles either by applying an appropriate
constraint on the charge density or by varying a corresponding structural distortion mode, using
two simple perovskite materials, SrCrO3 and LaVO3 , as model systems. Our analysis indicates that
in general the altermagnetic spin splitting is not exclusively determined by the lowest order nonzero
magnetic multipole, but results from a superposition of contributions from different multipoles with
comparable strength, suggesting the need for a multi-component order parameter to describe altermagnetism. We also discuss different measures to quantify the overall spin-splitting of a material,
without relying on features that might be specific to only individual bands.

I.

INTRODUCTION

It has been recognized only very recently, that in certain antiferromagnets, now termed altermagnets, time reversal symmetry is broken such that the Kramer’s degeneracy of the electronic states is lifted even in the limit
of zero spin-orbit coupling, while the net magnetization
remains zero [1–23]. This means that, for a general kpoint in the Brillouin zone of an altermagnet, the spin
degeneracy of the electronic bands is lifted, but the presence of certain symmetry operations requires that this
spin-splitting is reversed in other regions of the Brillouin
zone, such that integrals over the whole Brillouin zone
do not carry any net spin dependence.
Altermagnets therefore combine aspects of both ferromagnetic and antiferromagnetic (AFM) materials. Their
antiferroic (AF) arrangement of magnetic dipoles is robust to stray magnetic fields and allows for faster dynamics, while the spin-splitting in their band-structure
enables k-dependent spin transport, with efficient spincurrent generation recently demonstrated [24–29]. Moreover, in addition to potential applications in conventional
spintronics, a plethora of other interesting properties of
altermagnets have been suggested, such as a spontaneous
Hall effect [5, 21, 30–34], multipole transport [35–37], unconventional superconducting properties [38–42], piezomagnetism [43, 44], chiral magnon splitting [45, 46], and
many others [47–53].
On the theoretical side, much work has been focused
on clarifying the symmetry aspects of altermagnets, in
terms of the underlying spin-symmetry groups [7, 8, 54–
56], where, in the absence of spin-orbit coupling, rotations in spin-space are decoupled from rotations in real

∗ fmartinelli@ethz.ch
† edererc@ethz.ch

space. Thereby, the presence of a non-relativistic spinsplitting (NRSS) requires the absence of symmetry elements that map one spin sub-lattice on the other via
simple translations or inversion, while the presence of a
symmetry operation that maps the two sublattices on
each other via a proper or improper rotation ensures a
vanishing net magnetization [7, 8]. However, a general
quantitative description that goes beyond symmetry arguments, and relates the overall magnitude of the NRSS
to a simple order parameter, remains to be fully established.
In a ferromagnet, the relevant order parameter is its
net magnetic dipole moment, or magnetization, and the
average spin-splitting is quantitatively related to this order parameter. For the case of altermagnets, higher order
magnetic multipole moments, specifically magnetic octupoles or triakontadipoles, have been suggested as suitable ferroic order parameters [18, 43], since the symmetries that allow these magnetic multipoles to be nonzero
are identical to the symmetries that allow for a NRSS.
Magnetic multipoles characterize the spatial distribution of the magnetization density around the magnetic
atoms, and can potentially provide a simple and systematic unifying framework for classifying ferroically ordered
magnetic states. Thereby, a non-vanishing net magnetic
dipole corresponds to ferromagnetic order, while altermagnetic states would correspond to a zero magnetic
dipole but non-vanishing higher order multipoles. The
lowest order non-vanishing magnetic multipole then determines the k-space symmetry of the NRSS, with, e.g.,
d-wave and g-wave patterns corresponding to magnetic
octupoles and triakontadipoles, respectively [56].
Nevertheless, while the general relation between magnetic multipoles and altermagnetic symmetry has been
pointed out several times [18, 43, 48, 53], a clear quantitative correspondence between the magnitude of these
multipole moments and the strength of the altermagnetic
spin splitting still needs to be established. Apart from

2
its fundamental relevance, an appropriate definition of
an altermagnetic order parameter allows for a quantitative comparison across different materials and can also
enable a more targeted search for “strong” altermagnets
with optimized properties. Furthermore, identification of
an appropriate order parameter might also allow to control the phase transition and domain formation via its
conjugate field.
Here, we explore the quantitative relation between the
overall strength of the altermagnetic NRSS and the magnitude of different charge and magnetic multipoles, using
electronic structure calculations based on density functional theory (DFT). To this end, we vary the magnitude of specific multipoles by constraining the underlying electron density accordingly [57], or by systematically
imposing different structural distortion modes. We then
monitor the resulting changes in the NRSS as well as the
corresponding k-space symmetry.
We use two different materials as “model systems” to
establish a quantitative relation between multipoles and
NRSS. First, SrCrO3 , with a simple perovskite structure
and C-type AFM order, which allows us to investigate the
emergence of a NRSS driven by a purely electronic symmetry breaking, achieved by applying suitable perturbations to constrain specific multipoles [57]. And second,
LaVO3 , as a representative of a structurally distorted
perovskite exhibiting the most commonly observed, socalled GdFeO3 -type distortion, which lowers the space
group symmetry to P bnm and involves collective rotations of the oxygen octahedra surrounding the magnetic
cations. As recently pointed out [58], the corresponding
distortions lead to different multipoles that allow for the
emergence of a NRSS in combinations with either A-, C-,
or G-type AFM order.
Our analysis shows that in many cases a clear quantitative relation, where the NRSS indeed scales with the
magnitude of specific multipoles, can be established, but
that in some cases the NRSS also emerges from a superposition of different components, with dominant contributions also from higher order multipoles than the
lowest order nonzero one. Furthermore, we also assess
strengths and limitations of different measures for the
overall NRSS, to ensure a reliable quantitative analysis.

FIG. 1. Top: Sketch of a charge density exhibiting a nonzero
Qx2 −y2 quadrupole, characterized by charge accumulation
(depletion) along the x (y) axis. Bottom: Sketch of a collinear
magnetization density with non-zero Oxz octupole. In the
red (blue) regions the magnetization points upwards (downwards).

A.

Multipoles and how to constrain them within
DFT

Multipoles provide a systematic parametrization of the
spatial dependence of the charge and magnetization densities around an atom (or other center). To treat charge
and magnetic multipoles on the same footing, we can define a generalized density, ϱpq (r) (where p ∈ {0, 1} and
q = −p, . . . , p) as follows:


ϱpq (r) = Trs ⟨r|σ̂qp ρ̂|r⟩

II.

THEORETICAL BACKGROUND AND
COMPUTATIONAL METHOD

In this section, we first summarize the definition of
multipoles of the charge and magnetization density, and
also provide the details of how we evaluate and constrain
local multipoles. We then define the measures we use
to quantify the NRSS, and finally we provide all other
relevant computational details.

.

(1)

Here, ρ̂ is the density operator, σ̂qp represents either the
identity operator in spin space (for p = 0) or the operator
corresponding to the Pauli matrices (for p = 1), and the
trace is taken over the spin degrees of freedom. Thus,
ϱ00 (r) is equal to the charge density, ρ(r), while ϱ1q defines
the components of the magnetization density m(r).
A general multipole of spatial order k can then be defined as the integral over a certain component of the den-

3
sity multiplied with k factors of the form ri :
Z
k,p
Mij...l,q =
ri rj · · · rl ϱpq (r)dr ,
| {z }

(2)

These spherical multipoles can then be transformed
to fully irreducible spherical tensors of rank r, with
r = |k − p|, . . . , k + p, by coupling the spatial and spin
indices [60–62]:

k such factors

where ri is a cartesian component of the vector r. Note
that in principle the full spatial depdendence of the density can be reconstructed from the full set of multipole
moments (with k = 0, 1, . . . , ∞). Such multipoles also
appear naturally if one considers the interaction energy
of a charge and magnetization density with an inhomogeneous electrostatic potential and a magnetic (Zeeman)
field, where each multipole then interacts with a specific
component or derivative of the corresponding field (see,
e.g., Refs [57–59]).
Expressing the integrand in Eq. (2) in spherical coordinates leads to a definition of spherical multipoles as:
Z
kp
Mhq = rk Yhk (θ, ϕ) ϱpq (r, θ, ϕ) dr .
(3)

wtkpr =

X

kpr
ξhqt

Z

Yhk (θ, ϕ) ϱpq (θ, ϕ) dΩ =

X

X

wtkpr =

kpr
ξhqt
Mkp
hq

,

(4)

h=−k...k
q=−p...p

kpr
where the coefficients ξhqt
are essentially Clebsch-Gordan
coefficients combining the two irreducible representations
corresponding to k and p, and t = −r, . . . , r.

For the purpose of this work, we can discard the radial dependence of the multipoles,
so that the integral in
R
Eq. (3) can be reduced to Yhk (θ, ϕ) ϱpq (θ, ϕ) dΩ, with a
suitably radially averaged density. Expressing this density in terms of the usual density matrix with respect to
spin and angular momenta then leads to:

kpr
ξhqt

ll′ h=−k...k
q=−p...p

h=−k...k
q=−p...p

X

X
s=−σ...σ
s′ =−σ...σ

⟨s|σqp |s′ ⟩

X

⟨lm|vhk |l′ m′ ⟩ρlms,l′ m′ s′

.

m=−l...l
m′ =−l′ ...l′

(5)

Here, vhk is the spherical tensor operator corresponding to
the spatial degrees of freedom in Eq. (3), emerging from
the integral over three spherical harmonics in Eq. (5) with
a suitably chosen normalization [62]. Thus, the different
indices of wtkpr refer to the full tensor rank (r) and corresponding tensor component (t), as well as the underlying
spatial/angular tensor rank (k) and spin tensor rank (p).
In particular, p = 0, 1 labels charge and magnetic multipoles, respectively.
In systems with spatial inversion symmetry, which is
the case for all systems considered in this work, only
multipoles with even k are nonzero. Furthermore, we restrict our analysis to the l = l′ = 2 components of the
density matrix centered on the transition metal cations,
which make up the largest part of the magnetization
density. This sector of the density matrix only allows
for nonzero multipoles with k = {0, 2, 4}. For the case
of the charge multipoles (p = 0), this corresponds to
monopoles, quadrupoles, and hexadecapoles. Regarding
the magnetic multipoles, we limit our interest to those
with maximum rank, r = k + p, i.e., dipoles, octupoles,
and triakontadipoles. Note that for the case of the mag-

E[{wtkpr }] =

min

ϱ(r),skpr
t

netic octupole, this highest rank component coincides
with the totally symmetric traceless part of the full tensor [63].
In the following, to ease notation by avoiding too
many indices, we use symbols Mt , Qt , Ot , Ht , and
Tt for magnetic dipoles, charge quadrupoles, magnetic
octupoles, charge hexadecapoles, and magnetic triakontadipoles, respectively. Furthermore, for the case of
quadrupoles
 and octupoles, we designate the spatial character by xy, yz, 3z 2 − r2 , xz, x2 − y 2 corresponding to
t = −2, . . . , 2, respectively, noting that for a collinear
magnetization density along z, the |t| = 3 components of
the octupole are zero [63]. To give some intuition regarding the anisotropy represented by different multipoles,
Fig. 1 depicts two examples corresponding to a charge
density with Qx2 −y2 ̸= 0 and a magnetization density
characterized by Oxz .
To induce a specific multipole on a given site, we employ the constrained DFT approach proposed in Ref. [57],
which minimizes the total energy functional, E0 [ϱ(r)],
with an added constraint:


X kpr  kpr
st
wt [ϱ(r)] − w̃tkpr
E0 [ϱ(r)] −
kprt

!
.

(6)

4
Here, ϱ(r) represents all components of the generalized
density defined in Eq. (1), w̃tkpr denotes the specific value
to which the wtkpr multipole is constrained, and skpr
is
t
a corresponding Lagrange multiplier. In practice, skpr
t
represents the strength of an orbital- and spin-dependent
local potential shift that is added to the resulting KohnSham potential in order redistribute the electrons such
that they produce the corresponding multipole.
Since in this work we only need to vary the local multipoles without constraining them to a specific fixed value,
we do not perform a minimization with respect to skpr
t
and instead vary the strength of the shift-potential, skpr
t ,
within a certain range and then monitor the resulting
multipoles. For simplicity, and to avoid complications
with potentially induced noncollinearities in the magnetization density, we only constrain local charge multipoles,
in most cases only the quadrupoles, and we only apply
constraints to one specific component at a time. Thereby,
we generally apply constraints of identical strength, but
varying signs, to all transition metal cations in the unit
cell. We distinguish A-, C-, and G-type patterns with
different relative signs on these sites corresponding to
wave vectors qA = (0, 0, 0.5), qC = (0.5, 0.5, 0), and
qG = (0.5, 0.5, 0.5) defined in terms of the reciprocal vectors of the underlying pseudocubic lattice.

of the overall NRSS as:
∆max = max |∆(ν, k)|
ν,k

,

(7)

i.e., the maximum absolute value of the local spin splitting across a certain subset of bands at all k-points. A
second measure is obtained by averaging the local NRSS
over a subset of bands and all k-points belonging to a
high-symmetry path (hsp) where a strong NRSS is expected to arise:
hsp

∆avg,hsp =

1 XX
|∆(ν, k)|
Nν Nk ν

.

(8)

k

Here, Nν and Nk are the number of bands and k-points,
respectively, that are included in the averaging, and we
use the absolute value, |∆(ν, k)|, to prevent spurious
cancellations between bands with opposite signs of the
NRSS. Note that this measure requires prior knowledge
about the k-space distribution of the NRSS. Here, we
always use a high-symmetry path along the k-space direction reciprocal to the real space direction of highest charge accumulation or depletion of the relevant
quadrupole. Finally, we define a third measure similar
to ∆avg,hsp , but now averaged over all k-points throughout the whole Brillouin zone (BZ):
BZ

∆avg,BZ =
B.

Quantitative measures for the NRSS

In order to establish a general relation between the
magnitude of certain multipoles and the magnitude of
the resulting NRSS, we compare three different possible
measures for the overall spin splitting, with the intention
to identify an ensemble quantity that captures the key
characteristics without relying on features that might be
specific to only certain bands or the need to manually
inspect the band-structure for each individual case. We
note that, while the definition of a reliable integrated
measure of the NRSS is very desirable for the purpose
of this work, in other cases, e.g., for specific applications
in spin transport, the focus is more on achieving a pronounced spin splitting of some bands immediately around
the Fermi level.
To this end, we first define the local, band- and kresolved NRSS as ∆(ν, k) = ϵν,↑ (k) − ϵν,↓ (k), where ν is
the band index and ϵν,σ (k) are the corresponding band
energies with spin projection σ, and the bands for each σ
are simply indexed in order of increasing energy. We note
that for cases where the local NRSS becomes larger than
the typical energy difference between subsequent bands,
this simple indexing can obviously lead to inconsistencies
between spin-up and spin-down bands corresponding to
the same ν, such that the local spin splitting is taken
between bands that are not necessarily degenerate in the
non-altermagnetic limit. We will come back to this problem later in Sec. III A 2.
We then define a first simple measure for the strength

1 XX
|∆(ν, k)|
Nν Nk ν

.

(9)

k

In principle, comparing ∆avg,BZ and ∆avg,hsp allows to
establish how confined the NRSS is in k-space.
C.

Computational details

Within the DFT framework, we perform electronic
structure calculations using the plane wave-based projector augmented wave (PAW) method [64, 65] implemented in the “Vienna Ab-Initio Simulation Package”
(VASP) [66, 67], employing the exchange-correlation
functional of Perdew, Burke, and Ernzerhof [68]. We
use the standard PAW potentials included in VASP, with
all relevant semi-core states included as valence electrons
only for relaxations, a plane-wave energy cutoff set to
700 eV, and a convergence threshold for the total energy
of 10−8 eV.
√ For √SrCrO3 , we use a unit cell corresponding to a
2 × 2 × 1 supercell of the primitive cell of the underlying ideal perovskite structure, in order to accommodate
the C-type AFM order. Calculations are performed on
an 11 × 11 × 15 Γ-centered k-grid. The symmetry lowering due to the C-type AFM order leads to a simple
tetragonal structure with relaxed lattice parameters of
a = 3.86 Å and c/a = 0.98. This structure is then kept
fixed for all subsequent calculations presented here.
Our calculations for LaVO3 are based on the experimentally obtained structure with P bnm symmetry from Ref. [69], using the corresponding primitive

5
√
√
unit cell which corresponds to a 2 × 2 × 2 supercell of the underlying simple perovskite structure. We
then use AMPLIMODES [70] to decompose the structural distortion of this P bnm structure relative to the
ideal cubic perovskite structure (with P m3̄m symmetry)
into symmetry-adapted modes, and construct hypothetical structures that contain only one specific symmetry
adapted mode with varying amplitude, while keeping the
lattice parameters fixed to that of the undistorted P m3̄m
reference structure (with the same volume per formula
unit as the experimental P bnm structure). For all these
structures, we perform calculations on a 12 × 12 × 8 Γcentered k-grid.
The required modifications to the VASP code that allow to perform calculations with constrained multipoles
are provided by the “multipyles” package [71], which is
also used to perform the subsequent analysis of the resulting multipoles.

III.
A.

RESULTS

Quantifying the induced altermagnetic
spin-splitting in SrCrO3

SrCrO3 has been investigated as a rare example for
an antiferromagnetic metal [72–78], and has also been
reported to exhibit a tendency towards orbital order in
combination with a Jahn-Teller distortion and a metalinsulator transition under tensile epitaxial strain [72].
However, the Kugel-Khomskii coupling between orbital
and spin-order leads to a preferential G-type AF orbital polarization in combination with C-type AFM order. The resulting symmetry is not compatible with
the presence of a ferroically ordered magnetic multipole and the emergence of a NRSS, even though the
resulting electronic structure can be classified as “antialtermagnetic” [79].
Here, we use C-type AFM SrCrO3 as a simple model
material, with no spontaneous orbital order. We induce
specific multipoles by applying corresponding constraints
to the charge density [57] and vary their magnitude. This
allows us to monitor the resulting NRSS as function of
different multipole moments in the absence of any structural distortion, i.e., the symmetry breaking and emerging NRSS in this case is of purely electronic origin.
To ensure a symmetry breaking compatible with a
NRSS, we always impose a C-type AF arrangement of
local charge multipoles on top of the C-type AFM configuration. This means that the product of the local
magnetic dipole and the charge quadrupole (or hexadecapole), which is symmetry-equivalent to the local magnetic octupole (or triakontadipole), has the same sign on
every site and thus allows for a ferroic octupolar (or triakontadipolar) order.

1.

Induced multipoles

In Fig. 2 we show the magnetic dipole moments, the
emerging C-type antiferroically ordered charge multipoles, and the ferroically ordered higher order magnetic
multipoles as function of the strength of each specific
quadrupolar perturbation applied. The reported values
correspond to one of the two Cr atoms in the unit cell.
Due to the C-type antiferroic arrangement, the magnetic dipole and charge multipoles on the other, otherwise symmetry-equivalent Cr atom have opposite signs,
while the signs of the higher order magnetic multipoles
are identical.
One can see that the magnetic dipoles are essentially
unaffected by the applied perturbation and remain constant, while all the other multipoles are zero in the unperturbed case and change sign if the sign of the applied local
perturbation potential is reversed. The induced charge
quadrupoles are linearly related to the perturbation over
the entire considered range. The emergence of certain
higher order charge multipoles is consistent with the specific symmetry-breaking introduced by the applied perturbation.
A nonzero charge multipole then also implies a corresponding nonzero magnetic multipole with the same
symmetry as the product of that charge multipole and
the magnetic dipole. Thus, as expected, each induced
charge quadrupole is accompanied by a ferroically ordered magnetic octupole. Since the magnetic dipoles
remain constant, the dependence of the magnetic octupoles on the applied pertubation mirrors, to a good approximation, the dependence of the corresponding charge
quadrupole. The same relation can be observed between
the charge hexadecapoles and corresponding magnetic
triakontadipoles. However, we also note that the octupoles are not strictly equal to the product of the corresponding charge quadrupole and the magnetic dipole,
which can be seen from small deviations from linear behavior specifically for Oxy and Ox2 −y2 . We also note
that the induced C-type anti-ferroically aligned charge
hexadecapoles do not necessarily show a linear dependence on the applied perturbation, in particular for the
case of the sxy and sx2 −y2 perturbations. This behavior is then also mirrored in the corresponding magnetic
triakontadipoles.

2.

Quantification of the (average) NRSS

In Fig. 3 we show how the three different measures for
the NRSS, defined in Sec. II B, behave as a function of
the different induced charge quadrupoles. We first observe that the overall trends are comparable for all three
measures and that each type of symmetry breaking has a
distinct impact on the NRSS. In particular, the strongest
NRSS is obtained from Qx2 −y2 , i.e., when the direction of
maximum charge accumulation/depletion is aligned with
the Cr-O bonds. The difference between the effect of

6

FIG. 2. Dependence of charge and magnetic multipoles corresponding to one of the two Cr atoms in the unit cell on an applied
202
charge quadrupolar perturbation. From left to right, the columns correspond to different perturbations: s202
−2 = sxy , s−1 = syz ,
202
s202
=
s
,
s
=
s
.
2
2
xz
1
2
x −y

FIG. 3. Evolution of the different measures for the overall NRSS as function of different induced local charge quadrupoles.
The three panels show the global maximum, ∆max (left), the average along the corresponding “ideal” high-symmetry k-paths,
∆avg,hsp (center), and the full BZ average ∆avg,BZ (right).

Qxy and Qxz /Qyz results from the different orientations
of these quadrupoles relative to the C-type wavevector,
qC = (0.5, 0.5, 0). Moreover, while there is a clear linear
dependence of ∆avg, hsp and ∆avg, BZ on both Qyz and
Qxz , the NRSS as function of Qxy and Qx2 −y2 shows
some deviations from a purely linear behavior (further
discussion of this behavior is provided at the end of this
subsection).
Regarding the different measures to quantify the
NRSS, it is apparent that ∆max exhibits a more complex behavior as function of Qt compared to ∆avg, hsp
and ∆avg, BZ . In particular, ∆max suffers from the fact
that the underlying ∆(ν, k) is obtained from the difference between spin-up and spin-down bands with the same
band index ν, ordered simply from lowest to highest en-

ergy. Thus, once the local NRSS for a particular band becomes larger than the initial energy difference to the next
highest or lowest band with the same spin, the bands can
cross, and the assignment between corresponding spin-up
and spin-down bands can become incorrect.
Band crossings between adjacent bands with the same
spin character can indeed be recognized in the bandstructures shown in Fig. 4, which correspond to the cases without and with an applied sxy perturbation. While the
bandstructure for the unperturbed case does not show
any spin-splitting, a NRSS appears for nonzero sxy along
the path Y − Γ − X, while the bands along the Γ − M directions remain spin-degenerate. This is consistent with
the symmetry of the Qxy quadrupole, noting that the
high symmetry k-points in Fig. 4 are indexed according

7

FIG. 4. Bandstructure of C-AFM SrCrO3 without (left)
and with (right) application of a quadrupolar perturbation
of sxy = 0.5 eV. The green circular area highlights a region
where problematic bands-crossing occur, leading to potentially incorrect assignment between spin-up and spin-down
bands and thus a slight underestimation of the total NRSS.

to the simple tetragonal BZ, while the local x-y axes are
rotated by 45◦ relative to the basal plane lattice vectors.
Importantly, we highlight in green one of the problematic band crossings, arising between the bands evolving
along the Γ–X direction from the first and the fourth
band above the Fermi energy at Γ, which split in opposite ways. For the former, the down-spin state is higher in
energy, whereas for the latter, the up-spin state is higher.
As a result, ∆(ν, k) couples the two bands incorrectly for
k-vectors close to X, leading to a small underestimation
of the overall NRSS.
Such bands-crossings are more likely to occur for larger
spin splitting, preventing the calculated ∆max from capturing the actual maximum splitting. The other two definitions of ∆ of course suffer from the same problem, but
the averaging over bands and k-points seems to provide
an effective way to partially suppress this issue. Including more k-points in the averaging can thus be expected
to further mitigate this band-crossing problem even at
larger perturbations, in particular if the larger set of kpoints includes regions in the BZ where the spin splitting
is weaker. This is consistent with the slightly more regular behavior of ∆avg, BZ compared to ∆avg, hsp in Fig. 3.
Nevertheless it is important to mostly focus on the low
perturbation regime, where bands-crossings are less likely
to occur.
With this in mind, we can now have a closer look at
the dependence of ∆avg, BZ on Qxy and Qx2 −y2 in Fig. 3.
As noted previously, both cases show deviations from
perfectly linear behavior. For increasing |Qx2 −y2 |, one
can first recognize a gradual deviation from linear behavior, typical for the increasing influence of higher order terms, and then observe a kink-like feature around
Qx2 −y2 = 0.3 (corresponding to sx2 −y2 = 0.4 eV). The
NRSS as functions of Qxy also exhibits as somewhat
sudden change in slope around Qxy = 0.1 (corresponding to sxy = 0.15 eV), separating two essentially linear
regimes below and above. Inspection of the induced mul-

FIG. 5. Evolution and distribution of the NRSS across band
indices in SrCrO3 for increasing quadrupolar perturbation
sxy . For reference, we indicate all bands that cross the Fermi
energy at least at one k-point in the BZ by νF .

FIG. 6. Unperturbed bandstructure of C-AFM SrCrO3 projected onto the Cr d-orbitals. The projection highlights two
distinct regions where the Cr d contributions is significant:
around and above the Fermi level, where the bands exhibits
dominant Cr d character, and towards the bottom of the otherwise O p-dominated bands, which also exhibit strong hybridization with the Cr d states.

tipole moments shown in Fig. 2, suggests that these more
sudden features in the NRSS appear to be related to
corresponding features in the higher order multipoles,
such as the emergence of a more substantial H−2 for
sxy > 0.15 eV, and a noticeable saturation of H2 (but
also Ox2 −y2 ) for sx2 −y2 > 0.4 eV. This indicates that the
NRSS might not necessarily be determined exclusively
by the lowest order nonzero multipole, but that higher
order multipoles can also contribute. We will come back
to this point in Sec. III B.

3.

Band- and k-resolved NRSS

Next, to further analyze the spin splitting resulting
from the different induced multipoles, we also look at
the energy-resolved (or rather band-resolved) and also
the k-resolved NRSS. In Fig. 5 we show the BZ-averaged
NRSS
P calculated for each band, defined as ∆loc (ν) =
1
k ∆(ν, k). It can be seen that the NRSS predomNk

8
inantly involves two groups of bands, one corresponding to energies around or above the Fermi level, and one
corresponding to energies of some eV below the Fermi
level. Inspection of the orbitally-projected band structure shown in Fig. 6 indicates that the strong spinsplitting of these bands correlates with the corresponding Cr d character, with the groups at higher and lower
energies corresponding to the anti-bonding and bonding
bands formed from the hybridization between atomic Cr
d and O p states, respectively. That the spin-splitting
correlates with the Cr d character is of course expected,
since these states carry most of the magnetization density.
From Fig. 5 one can also see that for small perturbations, sxy , the largest spin-splitting arises in the Cr
d-dominated antibonding bands around and above the
Fermi level, but that the splitting appears to saturate
for larger perturbations. This is likely due to increased
presence of band-crossings for stronger perturbations,
which can then shadow a further increase of the NRSS.
In contrast, the bands at lower energies with weaker Cr
d character show a more regular, gradual increase of
the NRSS with increasing perturbation. Thus including
these bands in the definition of ∆avg, BZ also dampens the
unwanted effect of potential band crossings and results
in a more faithful representation of the overall average
NRSS in the system.
Fig. 4 already indicates to some extent how the symmetry of the induced multipole is reflected in the kdependence of the resulting NRSS for the case of a Oxy
octupole, which translates into a k- and spin-dependence
of the form σz kx ky [43]. Consequently, a clear NRSS is
expected along the [110]-type directions in k-space, with
opposite signs for [110] relative to [1̄10], while spin degeneracy is expected to be preserved along the [100] and
[010] directions [7, 56]. This is indeed the case in the perturbed bandstructure shown in Fig. 4, noting again that
in our setup the tetragonal basal plane lattice vectors
(and thus the corresponding reciprocal lattice vectors)
are rotated by 45◦ around the z-axis relative to the x-y
axes that are aligned along the Cr-O bonds.
To also obtain a quantitative idea of the k-resolved
NRSS, we now analyze the local NRSSP
averaged over all
bands but for fixed k, ∆loc (k) = N1ν ν ∆(ν, k). The
upper and lower panels of Fig. 7 depict ∆loc (k) within
the kx -ky plane (and kz = 0), calculated for perturbations sxy = 0.5 eV and sx2 −y2 = 0.5 eV, respectively. As
expected, the sign and strength of the NRSS indeed reflect the reduced spin-space-group symmetry of the system, as described in [7, 56]. Consequently, the NRSS is
zero along the nodal planes of the imposed quadrupole,
while the strongest spin splitting can be observed vaguely
in the regions corresponding to highest charge accumulation or depletion of the correspondong quadrupole in
real space. Note that here we defined ∆loc (k) without
taking the absolute value of ∆(ν, k), and in Fig. 7 we
can indeed discriminate regions with net positive and
net negative NRSS, even though the sign of ∆(ν, k) is

FIG. 7. k dependence of the band-averaged NRSS, ∆loc (k)
for different quadrupolar perturbations, plotted for kz = 0.
The upper panel corresponds to a sxy = 0.5 eV, while the
lower panel corresponds to sx2 −y2 = 0.5 eV. Note that the
basal-plane reciprocal lattice directions ka and kb are rotated
by 45◦ around z relative to the cartesian axes.

band-dependent. This means that in principle ∆loc (k)
could become zero also away from the symmetry-imposed
nodal surfaces, and is therefore not necessarily guaranteed to always provide a faithful representation of the kdependence of the overall NRSS. However, in the present
case it appears to be instructive.
To further test the correspondence between the k-space
symmetry of the NRSS and the lowest order nonzero multipole, we now perform a calculation where we induce
a charge hexadecapole instead of a charge quadrupole.
Specifically we apply a shift-potential of the form s404
−4 ,
corresponding to a C-type AF ordered H−4 hexadeR xy(x2 −y2 )
ρ(r) dr.
capole, which is of the form H−4 ∝
r4
The resulting symmetry lowering does not allow for
charge quadrupoles or magnetic octupoles, but also induces a ferroically ordered T−4 magnetic triakontadipole.
If one considers the nodal structure of the NRSS produced by the s404
−4 perturbation shown in Fig. 8, one recognizes a clear g-wave pattern, with nodal planes corre-

9

FIG. 8. k-dependence (for kz = 0) of the band-averaged
NRSS (here defined in terms of the absolute value of ∆(ν, k))
for a hexadecapolar perturbation, s404
−4 = 0.5 eV.

sponding exactly to the nodal planes of H−4 in real space,
i.e., kx = 0, ky = 0, and kx = ±kyP
. Note that here we
1
defined the NRSS as ∆abs
(k)
=
loc
ν |∆(ν, k)| to avoid
Nν
sign cancellations between different bands, which would
indeed prevent a proper characterization of the NRSS in
this case.

B.

Quantifying the altermagnetic spin-splitting in
LaVO3

The example of SrCrO3 discussed in Sec. III A allowed
us to explore the relation between multipoles of the electronic charge and magnetization density and the resulting NRSS in a simple and well-defined setting. Notably,
the corresponding NRSS is caused by a purely electronic
symmetry breaking, without any resulting structural distortions, confirming the possibility of purely electronically driven altermagnetism.
However, since the emergence of these multipoles is not
energetically favorable in SrCrO3 , they had to be induced
artificially via an externally applied constraint. Higher
order local multipoles are stabilized in certain altermagnets simply by the intrinsic crystal symmetry, such as,
e.g., in the rutile structure [59]. However, the resulting multipoles and thus the corresponding NRSS cannot
easily be tuned. Another mechanism that can in principle stabilize potentially tunable multipoles is orbital order, and the accompanying Jahn-Teller distortion. The
possibility of orbital-order-induced NRSS has been suggested in Ref. [80]. However, the Goodenough-Kanamori
rules tend to favor combinations of magnetic dipolar and
charge quadrupolar order that are incompatible with altermagnetism [79].
An alternative way to obtain stable (and potentially
tunable) local quadrupole moments is thus through structural distortions that are driven by other mechanisms,
such as, e.g., the collective octahedral rotations fre-

quently occurring in perovskite systems. Altermagnetic
spin splittings have indeed been reported based on electronic structure calculations for several distorted perovskites with P bnm space group symmetry [8, 9, 58, 81–
83], even several years before the emergence of the term
altermagnetism [84]. A systematic classification of higher
order multipoles and their relation to different distortion modes has recently been presented in Ref. [58], using LaMnO3 as example. In this section, we built on
this work and establish a quantitative relation between
different distortion modes present in P bnm perovskites,
the resulting multipole moments, and the corresponding
NRSS.
We use LaVO3 as an example model material which
crystallizes in the P bnm distorted perovskite structure.
We note that below ∼ 140 K LaVO3 develops additional
structural distortion related to orbital order [69, 85].
However, since in the present case we want to focus exclusively on the effects of the octahedral rotations, we
essentially “switch off” the tendency for orbital order in
LaVO3 by not applying a Hubbard correction in our DFT
calculations.
As discussed in [58], the P bnm distortion allows for
local charge quadrupoles, with different quadrupoles arranged in A-, C-, and G-type patterns, respectively.
Thus, each quadrupolar component can couple to a
matching A, C, or G-type magnetic dipolar order, in all
cases resulting in a symmetry that is compliant with a
ferroic order of a specific magnetic octupole component.
In other words, this means that any P bnm distorted perovskite with an A-, C,- or G-type AFM order exhibits
a spin-group symmetry that is compatible with a NRSS
along specific k-space directions.
We first demonstrate that this conclusion can indeed
also be confirmed for the case of LaVO3 , by imposing
each of the three magnetic dipolar order patterns. Fig. 9
shows the calculated band-structures along the relevant
k-space directions. Consistent with Ref. [58], the P bnm
structure allows for an A-type ordered Qyz , a C-type ordered Qxy , and a G-type ordered Qxz local quadrupole
on the V sites. Thus, for each corresponding AFM dipolar order, a NRSS emerges along the [011] (Γ-T), [110]
(Γ-S), and [101] (Γ-U) directions in k-space, respectively.
Next, we use the mode decomposition of the experimental structure to isolate the three main distortion
modes, R5− , M2+ , and X5− , which describe out-of-phase
octahedral rotations around [110], in-phase octahedral
rotations around z, and antipolar displacements of the
La cations perpendicular to z (see, e.g., Ref. [58] for a
more detailed discussion of the different modes present
in P bmm distorted perovskites). Each of these modes
alone already produces a modulation of the charge density corresponding to a G-type, C-type, and A-type wavevector, respectively. However, while the lowest order
emerging local multipole for the R5− and X5− modes is a
quadrupole, the M2+ mode only results in a local charge
hexadacapole while all quadrupolar components remain
zero [58]. Leveraging this mode decomposition, we create

10

FIG. 9. Spin-polarized bandstructures of LaVO3 calculated for A-type AFM (left), C-type AFM (middle), and G-type AFM
(right) orders.

mode.
In Fig. 11 we show the dependence of all relevant
charge and magnetic multipoles (corresponding to one
of the V atoms) as a function of the different distortion
mode amplitudes, where in each case only the mode indicated on the x-axis of the corresponding plot is nonzero,
and an amplitude of 1.0 corresponds to the amplitude of
that mode in the experimental structure.

FIG. 10. Bandstructure of G-AFM LaVO3 in the parent cubic
structure (left) and a distorted structure with only the R5−
mode included (right).

distorted structures where only one of these modes appear at a time, while all other modes remain zero, thereby
selectively inducing only the specific multipoles to which
the selected mode couples. We then tune the amplitude
of the corresponding mode and monitor the magnitude
of the emerging multipoles as well as the corresponding
NRSS. In these calculations, we always impose a matching pattern on the magnetic dipoles, i.e., A-, G, and Ctype AFM for the X5− , R5− , and M2+ mode, respectively.
Fig. 10 compares the bandstructures of LaVO3 calculated for the completely undistorted cubic structure (with
P m3̄m symmetry) and a structure with only the R5−
mode included, with an amplitude corresponding to that
of the fully distorted structure, and G-type AFM order.
As expected, the undistorted structure does not exhibit
any NRSS, whereas the NRSS emerging in the R5− distorted structure closely resembles that of the rightmost
panel of Fig. 9 for the fully distorted G-AFM structure.
While there are some differences, since the presence of the
other modes affects the overall bandwidth and breaks additional symmetries, the strong similarity between these
two cases suggests that the NRSS in the fully distorted
G-AFM structure is indeed dominated mostly by the R5−

The X5− mode (see top row of Fig. 11) induces an Atype AF order of Qyz , H−3 , and H−1 charge multipoles,
which all increase linearly with the X5− mode amplitude.
We note that the corresponding magnitudes are significantly smaller, by approximately one order of magnitude,
compared to the charge multipoles that we induced in
SrCrO3 under the quadrupolar constraint. The magnitudes of the ferroically ordered magnetic multipoles are
even smaller relative to the SrCrO3 case, with Oyz and
T−1 about two orders of magnitude smaller, and T−3
even three orders of magnitude smaller. Furthermore,
both Oyz and T−3 already show clear deviations from a
purely linear dependence on the mode amplitude in the
given range. Curiously, the negative sign of Oyz is opposite to that of the product of the local magnetic dipole
(not shown) and the charge quadrupole. Furthermore,
the local magnetic dipole (not shown) is essentially constant as function of the X5− mode amplitude. Together
with the pronounced deviation from linear behavior of
the octupole, this again demonstrates that the magnetic
octupole is not merely a product of the magnetic dipole
and the charge quadrupole. Similar to what has already
been briefly alluded to in Sec. III A 1, this finding suggests that Ot and Qt · Mz should in principle be treated
as distinct order parameters.
For the R5− mode (middle row of Fig. 11), the dependence of the emerging G-type local quadrupole, Qxz , and
ferroically ordered octupole, Oxz , show a clear nonlinear
dependence on the distortion mode amplitude. Further
analysis shows that the G-type Qxz order indeed corresponds to a different irreducible representation as the R5−

11

FIG. 11. Different local multipole moments (corresponding to one of the V atoms in the cell) induced by the individual
distortion modes in LaVO3 . We show only the nonzero multipoles that are relevant for the altermagnetic symmetry breaking,
i.e., the AF ordered charge multipoles matching the AF pattern of the applied distortion mode and the ferroically ordered
magnetic multipoles. Note that the M2+ mode does note create any nonzero charge quadrupoles or magnetic octupoles.

mode, and therefore the two do not couple linear to each
other. On the other hand, the induced charge hexadecapoles and magnetic triakontadipoles scale linearly with
the distortion amplitude. The response in T1 is particularly strong, being one order of magnitude larger than
what we induced in SrCrO3 .
Finally, the M2+ mode leads to the emergence of a linearly increasing H−4 with C-type pattern and of a ferroically ordered T−4 . As expected from symmetry, no
lower-order multipoles are induced. The magnitudes in
this case are comparable to those induced in SrCrO3 .
Comparing the effects of the different modes shown in
Fig. 11, further reveals that the X5− mode induces relatively small multipoles compared to the other two modes.
This means that the X5− mode induces only a relatively
weak anisotropy of the charge and magnetization densities around the V cations, which can be attributed to
the nature of the X5− distortion, which primarily displaces the La atoms, while the other two modes affect
the oxygen octahedral environment around the V sites
more directly.
In Fig. 12, we plot the BZ-averaged NRSS, ∆avg,BZ , as
function of the three different distortion modes, and also
as function of all the various local charge and magnetic
multipoles that are induced by these distortion modes.
As a first observation, one can note that all three modes

give rise to an overall NRSS of comparable magnitude, in
spite of the fact that the absolute atomic displacements
related to these modes are different (and of course the
resulting k-space distribution of the NRSS is different
for each mode). We can also note that although some of
the multipoles in this case are significantly smaller than
what we induced in SrCrO3 , the resulting overall spin
splitting is only about half of what we discussed in that
case.
Focusing on each mode individually, one can see that
for the case of the X5− mode, the NRSS exhibits a fairly
regular behavior, with a linear initial increase as function
of all potential order parameters. In particular, the scaling of the NRSS with the lowest order charge and magnetic multipoles, i.e., the charge quadrupole and magnetic octupole, appears consistent with these quantities
acting as order parameters for the NRSS, even though the
same could also be stated about the higher order charge
hexadecapoles and magnetic triakontadipoles.
For the NRSS related to the R5− mode, the case is
clearly different. While the NRSS exhibits a regular behavior as function of the R5− mode amplitude, there is no
clear quantitative correlation with the charge quadrupole
and magnetic octupole. If plotted as a function of these
multipoles, the NRSS first increases steeply, while the
quadrupole and magnetic octupole remain nearly zero,

12

FIG. 12. BZ-averaged NRSS, ∆avg,BZ , as a function of the three different mode amplitudes and the corresponding induced
multipole moments, i.e, the AF aligned charge quadrupole, ferroic magnetic octupole, AF aligned hexadecapole, and ferroic
trikontadiapole. In cases where multiple components of the same rank coexist, only the dependence on the dominant contribution (largest magnitude) is plotted. For better comparison across the different modes, all multipoles are normalized relative to
their maximum values.

and then the NRSS stays nearly constant whereas the
two multipoles increase strongly. In contrast, the NRSS
scales very regularly both with the hexadecapole and the
triakontadipole. This strongly suggests that in this case
the main contribution to the NRSS comes from these
higher order multipoles rather than from the lowest order nonzero charge quadrupoles and magnetic octupoles.
Regarding the M2+ mode, the NRSS also exhibits a
regular scaling with these higher order multipoles, noting
again that no charge quadrupoles or magnetic octupoles
are symmetry-allowed in this case. Nevertheless the corresponding NRSS is nearly of the same magnitude as in
the other two cases, in spite of the lacking contributions
from these lower-order multipoles.
Collectively, this analysis strongly suggests, that the
total NRSS in fact emerges as a superposition of contributions from multipoles with different rank, and is not
necessarily dominated quantitatively by the lowest order
nonzero multipole. In addition, the simultaneous presence of all three distortion modes (plus two additional
minor ones) in the actual P bnm crystal structure leads to
a further superposition of different multipole components
with the same rank but different character t. We thus
propose that a potential altermagnetic order parameter
in general needs to be considered as a multi-dimensional
order parameter, with potentially rather high dimension.
The superposition of the total NRSS stemming from
different multipolar components can schematically be ex-

pressed as:
∆=

X
kprt

∆kpr
=
t

X

δtkpr wtkpr

,

(10)

kprt

with materials-specific coupling coefficients, δtkpr , for
each relevant multipole. We note that such a superposition is similar in spirit to a recently proposed decomposition of the k-dependent NRSS in terms of symmetryadapted plane waves [56], even though a potential relation between this symmetry-adapted plane wave decomposition and the decomposition in terms of spherical multipoles in Eq. (10) still needs to be established.
IV.

SUMMARY AND CONCLUSIONS

In this work, we have addressed the quantitative relation between the altermagnetic spin splitting and certain
multipoles of the charge and magnetization density as
corresponding order parameters. We used SrCrO3 and
LaVO3 as model materials for our calculations, but our
general conclusions should be applicable to a wide variety
of other materials.
We showed that a purely electronic symmetry breaking is sufficient to induce a substantial NRSS, which indicates that the definition of an electronic altermagnetic
order parameter is indeed reasonable. A corresponding
symmetry-breaking is generally related to a ferroic order
of magnetic multipoles of higher order than the simple
dipoles (or, equivalently, to a ferroic order of the product
of the local magnetic dipoles and a charge multipole).

13
For the case of SrCrO3 , for which we selectively induced different charge multipoles with a suitable ordering
pattern that also allows for a ferroic net magnetic multipole, we find that there is indeed a clear quantitative
relation between the emerging NRSS and the corresponding multipole. However, we also found first indications
that not only the lowest order nonzero multipole determines the overall strength of the NRSS, but that higher
order multipoles also contribute. Nevertheless, the nodal
structure of the NRSS in k-space is determined by the
lowest order nonzero multipoles, with ferroic octupolar
or triakontadipolar order resulting in d-wave and g-wave
symmetry, respectively.
In this context, we also assessed different simple measures to quantify the overall NRSS, and found the BZaveraged measure most suitable and rather insensitive to
potential inconsistencies in the band-assignments resulting from crossings of bands with the same spin character.
Most importantly, our analyis of the NRSS and corresponding multipoles related to different structural distortion modes in LaVO3 , which is representative for the huge
class of P bnm distorted perovskites, further revealed a
more complex picture, suggesting that the total NRSS

generally results from a superposition of different contributions of comparable magnitude related to multipoles of
different rank. A quantitative theory of altermagnetism
therefore needs to be based on a multi-dimensional order parameter containing multipoles of different rank as
well as different components of the same rank. Within
this framework, the total NRSS can then be described
as a sum over different channels, each related to a multipole of the charge and/or magnetization density, and
the strength of each contribution is governed by a corresponding materials-specific altermagnetic coefficient. In
future work, it might be instructive to isolate the contribution of each individual multipole, thus allowing for
a characterization of altermagnetic materials based on
their multipolar fingerprint.

[1] S. Hayami, Y. Yanagi, and H. Kusunose, MomentumDependent Spin Splitting by Collinear Antiferromagnetic
Ordering, Journal of the Physical Society of Japan 88,
123702 (2019).
[2] K.-H. Ahn, A. Hariki, K.-W. Lee, and J. Kuneš, Antiferromagnetism in RuO2 as d-wave Pomeranchuk instability, Physical Review B 99, 184432 (2019).
[3] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, Giant momentum-dependent spin splitting
in centrosymmetric low-z antiferromagnets, Physical Review B 102, 014422 (2020).
[4] S. Hayami, Y. Yanagi, and H. Kusunose, Bottom-up design of spin-split and reshaped electronic band structures
in antiferromagnets without spin-orbit coupling: Procedure on the basis of augmented multipoles, Physical Review B 102, 144441 (2020).
[5] L. Šmejkal, R. González-Hernández, T. Jungwirth, and
J. Sinova, Crystal time-reversal symmetry breaking and
spontaneous Hall effect in collinear antiferromagnets, Science Advances 6, eaaz8809 (2020).
[6] L.-D. Yuan, Z. Wang, J.-W. Luo, and A. Zunger, Prediction of low-Z collinear and noncollinear antiferromagnetic
compounds having momentum-dependent spin splitting
even without spin-orbit coupling, Physical Review Materials 5, 014409 (2021).
[7] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond Conventional Ferromagnetism and Antiferromagnetism: A
Phase with Nonrelativistic Spin and Crystal Rotation
Symmetry, Physical Review X 12, 031042 (2022).
[8] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging Research Landscape of Altermagnetism, Physical Review X
12, 040501 (2022).
[9] L.-D. Yuan and A. Zunger, Degeneracy Removal of
Spin Bands in Collinear Antiferromagnets with Non-

Interconvertible Spin-Structure Motif Pair, Advanced
Materials 35, 2211966 (2023).
[10] L.-D. Yuan, X. Zhang, C. M. Acosta, and A. Zunger,
Uncovering spin-orbit coupling-independent hidden spin
polarization of energy bands in antiferromagnets, Nature
Communications 14, 5301 (2023).
[11] Y. Guo, H. Liu, O. Janson, I. C. Fulga, J. van den Brink,
and J. I. Facio, Spin-split collinear antiferromagnets: A
large-scale ab-initio study, Materials Today Physics 32,
100991 (2023).
[12] S. Zeng and Y.-J. Zhao, Description of two-dimensional
altermagnetism: Categorization using spin group theory,
Physical Review B 110, 054406 (2024).
[13] S. Lee, S. Lee, S. Jung, J. Jung, D. Kim, Y. Lee, B. Seok,
J. Kim, B. G. Park, L. Šmejkal, C.-J. Kang, and C. Kim,
Broken Kramers Degeneracy in Altermagnetic MnTe,
Physical Review Letters 132, 036702 (2024).
[14] J. Krempaský, L. Šmejkal, S. W. D’Souza, M. Hajlaoui, G. Springholz, K. Uhlı́řová, F. Alarab, P. C.
Constantinou, V. Strocov, D. Usanov, W. R. Pudelko,
R. González-Hernández, A. Birk Hellenes, Z. Jansa,
H. Reichlová, Z. Šobáň, R. D. Gonzalez Betancourt,
P. Wadley, J. Sinova, D. Kriegner, J. Minár, J. H. Dil,
and T. Jungwirth, Altermagnetic lifting of Kramers spin
degeneracy, Nature 626, 517 (2024).
[15] S. Reimers, L. Odenbreit, L. Šmejkal, V. N. Strocov,
P. Constantinou, A. B. Hellenes, R. Jaeschke Ubiergo,
W. H. Campos, V. K. Bharadwaj, A. Chakraborty,
T. Denneulin, W. Shi, R. E. Dunin-Borkowski, S. Das,
M. Kläui, J. Sinova, and M. Jourdan, Direct observation
of altermagnetic band splitting in CrSb thin films, Nature
Communications 15, 2116 (2024).
[16] T. Aoyama and K. Ohgushi, Piezomagnetic properties
in altermagnetic MnTe, Physical Review Materials 8,

ACKNOWLEDGMENTS

This work was supported by ETH Zürich. Calculations
were performed on the ETH Zürich Euler cluster and
the Swiss National Supercomputing Center Eiger cluster
under Project ID s1304.

14
L041402 (2024).
[17] Z. Lin, D. Chen, W. Lu, X. Liang, S. Feng, K. Yamagami, J. Osiecki, M. Leandersson, B. Thiagarajan,
J. Liu, C. Felser, and J. Ma, Observation of Giant Spin
Splitting and d-wave Spin Texture in Room Temperature
Altermagnet RuO2 (2024), arXiv:2402.04995 [cond-mat].
[18] P. A. McClarty and J. G. Rau, Landau Theory of Altermagnetism, Physical Review Letters 132, 176702 (2024).
[19] L. Bai, W. Feng, S. Liu, L. Šmejkal, Y. Mokrousov, and
Y. Yao, Altermagnetism: Exploring New Frontiers in
Magnetism and Spintronics, Advanced Functional Materials 34, 2409327 (2024).
[20] T. Jungwirth, R. M. Fernandes, J. Sinova, and L. Smejkal, Altermagnets and beyond: Nodal magneticallyordered phases (2024), arXiv:2409.10034 [cond-mat].
[21] S.-W. Cheong and F.-T. Huang, Altermagnetism with
non-collinear spins, npj Quantum Materials 9, 13 (2024).
[22] P. G. Radaelli and G. Gurung, Color symmetry and altermagneticlike spin textures in noncollinear antiferromagnets, Physical Review B 112, 014431 (2025).
[23] M. Hu, X. Cheng, Z. Huang, and J. Liu, Catalog of cpaired spin-momentum locking in antiferromagnetic systems, Physical Review X 15, 021083 (2025).
[24] I. Mazin and The PRX Editors, Editorial:
Altermagnetism—A New Punch Line of Fundamental
Magnetism, Physical Review X 12, 040002 (2022).
[25] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, Spin current generation in organic antiferromagnets, Nature Communications 10, 4305 (2019).
[26] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia, and
J. Liu, Multifunctional antiferromagnetic materials with
giant piezomagnetism and noncollinear spin current, Nature Communications 12, 2846 (2021).
[27] R. González-Hernández, L. Šmejkal, K. Výborný, Y. Yahagi, J. Sinova, T. Jungwirth, and J. Železný, Efficient Electrical Spin Splitter Based on Nonrelativistic
Collinear Antiferromagnetism, Physical Review Letters
126, 127701 (2021).
[28] D.-F. Shao, S.-H. Zhang, M. Li, C.-B. Eom, and E. Y.
Tsymbal, Spin-neutral currents for spintronics, Nature
Communications 12, 7061 (2021).
[29] A. Bose, N. J. Schreiber, R. Jain, D.-F. Shao, H. P. Nair,
J. Sun, X. S. Zhang, D. A. Muller, E. Y. Tsymbal, D. G.
Schlom, and D. C. Ralph, Tilted spin current generated
by the collinear antiferromagnet ruthenium dioxide, Nature Electronics 5, 267 (2022).
[30] L. Šmejkal, A. H. MacDonald, J. Sinova, S. Nakatsuji,
and T. Jungwirth, Anomalous Hall antiferromagnets, Nature Reviews Materials 7, 482 (2022).
[31] H. Reichlová, R. L. Seeger, R. González-Hernández,
I. Kounta, R. Schlitz, D. Kriegner, P. Ritzinger, M. Lammel, M. Leiviskä, V. Petřı́ček, P. Doležal, E. Schmoranzerová, A. Bad’ura, A. Thomas, V. Baltz, L. Michez,
J. Sinova, S. T. B. Goennenwein, T. Jungwirth, and
L. Šmejkal, Macroscopic time reversal symmetry breaking by staggered spin-momentum interaction (2021),
arXiv:2012.15651 [cond-mat].
[32] Z. Feng, X. Zhou, L. Šmejkal, L. Wu, Z. Zhu, H. Guo,
R. González-Hernández, X. Wang, H. Yan, P. Qin,
X. Zhang, H. Wu, H. Chen, Z. Meng, L. Liu, Z. Xia,
J. Sinova, T. Jungwirth, and Z. Liu, An anomalous Hall
effect in altermagnetic ruthenium dioxide, Nature Electronics 5, 735 (2022).

[33] R. D. Gonzalez Betancourt, J. Zubáč, R. GonzalezHernandez, K. Geishendorf, Z. Šobáň, G. Springholz,
K. Olejnı́k, L. Šmejkal, J. Sinova, T. Jungwirth, S. T. B.
Goennenwein, A. Thomas, H. Reichlová, J. Železný, and
D. Kriegner, Spontaneous Anomalous Hall Effect Arising
from an Unconventional Compensated Magnetic Phase in
a Semiconductor, Physical Review Letters 130, 036702
(2023).
[34] T. Sato, S. Haddad, I. C. Fulga, F. F. Assaad, and J. Van
Den Brink, Altermagnetic Anomalous Hall Effect Emerging from Electronic Correlations, Physical Review Letters
133, 086503 (2024).
[35] H.-W. Ko and K.-J. Lee, Magnetic Octupole Hall Effect
in d-Wave Altermagnets (2025), arXiv:2508.00794 [condmat].
[36] S. Han, D. Jo, I. Baek, S. Cheon, P. M. Oppeneer, and
H.-W. Lee, Harnessing Magnetic Octupole Hall Effect to
Induce Torque in Altermagnets, Physical Review Letters
135, 076705 (2025).
[37] I. Baek, S. Han, and H.-W. Lee, Magnetic octupole Hall
effect in heavy transition metals, Physical Review B 112,
064421 (2025).
[38] I. I. Mazin, Notes on altermagnetism and superconductivity, AAPPS Bulletin 35, 18 (2025).
[39] D. Chakraborty and A. M. Black-Schaffer, Zero-field
finite-momentum and field-induced superconductivity in
altermagnets, Physical Review B 110, L060508 (2024).
[40] S.-B. Zhang, L.-H. Hu, and T. Neupert, Finitemomentum Cooper pairing in proximitized altermagnets,
Nature Communications 15, 1801 (2024).
[41] D. Zhu, Z.-Y. Zhuang, Z. Wu, and Z. Yan, Topological
superconductivity in two-dimensional altermagnetic metals, Physical Review B 108, 184505 (2023).
[42] S. Banerjee and M. S. Scheurer, Altermagnetic superconducting diode effect, Physical Review B 110, 024503
(2024).
[43] S. Bhowal and N. A. Spaldin, Ferroically Ordered Magnetic Octupoles in d -Wave Altermagnets, Physical Review X 14, 011019 (2024).
[44] P. G. Radaelli, Tensorial approach to altermagnetism,
Physical Review B 110, 214428 (2024).
[45] L. Šmejkal, A. Marmodoro, K.-H. Ahn, R. GonzálezHernández, I. Turek, S. Mankovsky, H. Ebert, S. W.
D’Souza, O. Šipr, J. Sinova, and T. Jungwirth, Chiral
Magnons in Altermagnetic RuO2 , Physical Review Letters 131, 256703 (2023).
[46] Z. Liu, M. Ozeki, S. Asai, S. Itoh, and T. Masuda, Chiral
Split Magnon in Altermagnetic MnTe, Physical Review
Letters 133, 156702 (2024).
[47] I. I. Mazin, K. Koepernik, M. D. Johannes, R. GonzálezHernández, and L. Šmejkal, Prediction of unconventional
magnetism in doped FeSb2, Proceedings of the National
Academy of Sciences 118, e2108924118 (2021).
[48] X. H. Verbeek, D. Voderholzer, S. Schären, Y. Gachnang,
N. A. Spaldin, and S. Bhowal, Nonrelativistic ferromagnetotriakontadipolar order and spin splitting in hematite,
Physical Review Research 6, 043157 (2024).
[49] K. V. Yershov, V. P. Kravchuk, M. Daghofer, and J. Van
Den Brink, Fluctuation-induced piezomagnetism in local
moment altermagnets, Physical Review B 110, 144421
(2024).
[50] G. Yang, Z. Li, S. Yang, J. Li, H. Zheng, W. Zhu,
Z. Pan, Y. Xu, S. Cao, W. Zhao, A. Jana, J. Zhang,
M. Ye, Y. Song, L.-H. Hu, L. Yang, J. Fujii, I. Vobornik,

15
M. Shi, H. Yuan, Y. Zhang, Y. Xu, and Y. Liu, Threedimensional mapping of the altermagnetic spin splitting
in CrSb, Nature Communications 16, 1442 (2025).
[51] L. Šmejkal, Altermagnetic multiferroics and altermagnetoelectric effect (2024), arXiv:2411.19928 [cond-mat].
[52] M. Gu, Y. Liu, H. Zhu, K. Yananose, X. Chen, Y. Hu,
A. Stroppa, and Q. Liu, Ferroelectric Switchable Altermagnetism, Physical Review Letters 134, 106802 (2025).
[53] J. Nag, B. Das, S. Bhowal, Y. Nishioka, B. Bandyopadhyay, S. Sarker, S. Kumar, K. Kuroda, V. Gopalan,
A. Kimura, K. G. Suresh, and A. Alam, GdAlSi: An
antiferromagnetic topological Weyl semimetal with nonrelativistic spin splitting, Physical Review B 110, 224436
(2024).
[54] D. B. Litvin and W. Opechowski, Spin groups, Physica
76, 538 (1974).
[55] D. B. Litvin, Spin point groups, Acta Crystallographica
Section A: Crystal Physics, Diffraction, Theoretical and
General Crystallography 33, 279 (1977).
[56] A. Urru, D. Seleznev, Y. Teng, S. Y. Park, S. E. ReyesLillo, and K. M. Rabe, G-type antiferromagnetic BiFeO3
is a multiferroic g-wave altermagnet, Physical Review B
112, 104411 (2025).
[57] L. Schaufelberger, M. E. Merkel, A. M. Tehrani, N. A.
Spaldin, and C. Ederer, Exploring energy landscapes of
charge multipoles using constrained density functional
theory, Physical Review Research 5, 033172 (2023).
[58] S. Bandyopadhyay, S. Picozzi, and S. Bhowal, Designing
nonrelativistic spin splitting in oxide perovskites, Physical Review B 112, 064405 (2025).
[59] S. Bhowal and N. A. Spaldin, Revealing hidden magnetoelectric multipoles using Compton scattering, Physical
Review Research 3, 033185 (2021).
[60] J. J. Sakurai and J. Napolitano, Modern Quantum Mechanics, 3rd ed. (Cambridge University Press, Cambridge, 2020).
[61] P. Santini, S. Carretta, G. Amoretti, R. Caciuffo,
N. Magnani, and G. H. Lander, Multipolar interactions
in f -electron systems: The paradigm of actinide dioxides,
Reviews of Modern Physics 81, 807 (2009).
[62] F. Bultmark, F. Cricchio, O. Grånäs, and L. Nordström,
Multipole decomposition of LDA + U energy and its application to actinide compounds, Physical Review B 80,
035121 (2009).
[63] A. Urru and N. A. Spaldin, Magnetic octupole tensor
decomposition and second-order magnetoelectric effect,
Annals of Physics 447, 168964 (2022).
[64] P. E. Blöchl, Projector augmented-wave method, Physical Review B 50, 17953 (1994).
[65] G. Kresse and D. Joubert, From ultrasoft pseudopotentials to the projector augmented-wave method, Physical
Review B 59, 1758 (1999).
[66] G. Kresse and J. Hafner, Ab initio molecular dynamics
for liquid metals, Physical Review B 47, 558 (1993).
[67] G. Kresse and J. Furthmüller, Efficient iterative schemes
for ab initio total-energy calculations using a plane-wave
basis set, Physical Review B 54, 11169 (1996).
[68] J. P. Perdew, K. Burke, and M. Ernzerhof, Generalized
Gradient Approximation Made Simple, Physical Review
Letters 77, 3865 (1996).
[69] P. Bordet, C. Chaillout, M. Marezio, Q. Huang, A. Santoro, S.-W. Cheong, H. Takagi, C. S. Oglesby, and
B. Batlogg, Structural Aspects of the Crystallographic-

Magnetic Transition in LaVO3 around 140 K, Journal of
Solid State Chemistry 106, 253 (1993).
[70] D. Orobengoa, C. Capillas, M. I. Aroyo, and J. M. PerezMato, AMPLIMODES: Symmetry-mode analysis on the
Bilbao Crystallographic Server, Journal of Applied Crystallography 42, 820 (2009).
[71] M. E. Merkel, Multipyles v1.1.0, Zenodo (2023).
[72] A. Carta and C. Ederer, Evidence for Jahn–Teller-driven
metal–insulator transition in strained SrCrO3 from firstprinciples calculations, Physical Review Materials 6,
075004 (2022).
[73] A. Carta, A. Panda, and C. Ederer, Emergence of a potential charge-disproportionated insulating state in SrCrO 3, Physical Review Research 6, 023240 (2024).
[74] A. C. Komarek, T. Möller, M. Isobe, Y. Drees, H. Ulbrich, M. Azuma, M. T. Fernández-Dı́az, A. Senyshyn,
M. Hoelzel, G. André, Y. Ueda, M. Grüninger, and
M. Braden, Magnetic order, transport and infrared optical properties in the ACrO3 system (a = Ca, Sr, and
Pb), Physical Review B 84, 125114 (2011).
[75] L. Ortega-San-Martin, A. J. Williams, J. Rodgers, J. P.
Attfield, G. Heymann, and H. Huppertz, Microstrain
Sensitivity of Orbital and Electronic Phase Separation
in SrCrO3 , Physical Review Letters 99, 255701 (2007).
[76] K. H. L. Zhang, Y. Du, P. V. Sushko, M. E. Bowden,
V. Shutthanandan, L. Qiao, G. X. Cao, Z. Gai, S. Sallis, L. F. J. Piper, and S. A. Chambers, Electronic and
magnetic properties of epitaxial perovskite SrCrO3(0 0
1), Journal of Physics: Condensed Matter 27, 245605
(2015).
[77] K.-W. Lee and W. E. Pickett, Orbital-ordering driven
structural distortion in metallic SrCrO3 , Physical Review
B 80, 125133 (2009).
[78] Y. Qian, G. Wang, Z. Li, C. Q. Jin, and Z. Fang, The
electronic structure of a weakly correlated antiferromagnetic metal, SrCrO3: First-principles calculations, New
Journal of Physics 13, 053002 (2011).
[79] Q. N. Meier, A. Carta, C. Ederer, and A. Cano,
(Anti-)Altermagnetism from Orbital Ordering in the
Ruddlesden-Popper Chromates Srn+1 Crn O3n+1 (2025),
arXiv:2502.01515 [cond-mat].
[80] V. Leeb, A. Mook, L. Šmejkal, and J. Knolle, Spontaneous formation of altermagnetism from orbital ordering,
Phys. Rev. Lett. 132, 236701 (2024).
[81] M. Naka, Y. Motome, and H. Seo, Altermagnetic perovskites, npj Spintronics 3, 1 (2025).
[82] S. Rooj, S. Saxena, and N. Ganguli, Altermagnetism in
the orthorhombic P nma structure through group theory
and DFT calculations, Physical Review B 111, 014434
(2025).
[83] R. M. Fernandes, V. S. de Carvalho, T. Birol, and R. G.
Pereira, Topological transition from nodal to nodeless
Zeeman splitting in altermagnets, Physical Review B
109, 024404 (2024).
[84] T. Okugawa, K. Ohno, Y. Noda, and S. Nakamura,
Weakly spin-dependent band structures of antiferromagnetic perovskite LaMO3 (M = Cr, Mn, Fe), Journal of
Physics: Condensed Matter 30, 075502 (2018).
[85] S. Miyasaka, Y. Okimoto, M. Iwama, and Y. Tokura,
Spin-orbital phase diagram of perovskite-type R VO 3 (
R = rare -earth ion or Y), Physical Review B 68, 100406
(2003).


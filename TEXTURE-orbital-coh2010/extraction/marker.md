<!-- extraction: pdftotext | arxiv:1010.6071 -->
Chern-Simons orbital magnetoelectric coupling in generic insulators
Sinisa Coh,1, ∗ David Vanderbilt,1 Andrei Malashevich,2 and Ivo Souza2

arXiv:1010.6071v1 [cond-mat.mtrl-sci] 28 Oct 2010

1

Department of Physics and Astronomy, Rutgers University, Piscataway, New Jersey 08854-8019, USA
2
Department of Physics, University of California, Berkeley, California 94720, USA
(Dated: May 31, 2018)
We present a Wannier-based method to calculate the Chern-Simons orbital magnetoelectric coupling in the framework of first-principles density-functional theory. In view of recent developments
in connection with strong Z2 topological insulators, we anticipate that the Chern-Simons contribution to the magnetoelectric coupling could, in special cases, be as large or larger than the total
magnetoelectric coupling in known magnetoelectrics like Cr2 O3 . The results of our calculations for
the ordinary magnetoelectrics Cr2 O3 , BiFeO3 and GdAlO3 confirm that the Chern-Simons contribution is quite small in these cases. On the other hand, we show that if the spatial inversion and
time-reversal symmetries of the Z2 topological insulator Bi2 Se3 are broken by hand, large induced
changes appear in the Chern-Simons magnetoelectric coupling.
PACS numbers: 75.85.+t,03.65.Vf,71.15.Rf

I.

INTRODUCTION

In recent years there has been a significant revival of
interest in magnetoelectric effects in solids, as surveyed in
several reviews.1–4 Potential applications of these materials have long been discussed5,6 in areas ranging from the
optical manipulation and frequency conversion to magnetoelectric memories. Of the various quantities that can be
discussed, the linear magnetoelectric coupling tensor αij
is clearly of primary interest, as it quantifies the leadingorder term in the coupling at small fields. We define it
as




∂Pi
∂Mj
αij =
=
,
(1)
∂Bj E
∂Ei B
where Pi is the electric polarization induced by the magnetic field Bj , or equivalently, Mj is the magnetization
induced by the electric field Ei . We use SI units (see
Sec. II A) and the derivatives are to be evaluated at zero
electric and magnetic field. In the special case that the
induced response (P or M) remains parallel to the applied field (B or E), the tensor α is purely diagonal with
equal diagonal elements, and its strength can be measured by a dimensionless scalar parameter θ defined via
αiso
ij =

θe2
δij .
2πh

(2)

More generally, depending on the magnetic point group
of the crystal, αij can have distinct diagonal components
as well as non-zero off-diagonal ones.
The linear magnetoelectric response αij can be decomposed into two contributions coming from purely electronic and from ionic responses respectively. The former
is defined as the magnetoelectric response that occurs
when atoms are not allowed to displace in response to the
applied field, while the latter is defined as the remaining
lattice-mediated response. One generally expects ionic
effects to dominate over electronic responses, as for example was shown recently in Ref. 7 and 8 for the case

of Cr2 O3 . Moreover, each of these components can be
decomposed further into spin and orbital parts, since the
magnetization induced by the electric field can be decomposed in that way. Here one would naively expect that
the spin contribution will dominate with respect to the
orbital one, since orbital moments are usually strongly
quenched by crystal fields. Mostly for this reason, realistic theoretical calculations of magnetoelectric coupling
have been developed7–9 only for the spin component.
As shown in Refs. 10 and 11 using two complementary approaches, the orbital magnetoelectric polarizability (OMP), defined as the contribution of orbital currents
to the magnetoelectric coupling αij , can be written as
the sum of three gauge-invariant contributions. One of
these, first discussed by Qi et al.12 and Essin et al.,13
is the Chern-Simons term (CSOMP). Since this contribution is purely isotropic, we can measure its strength
using the single parameter θ as in Eq. (2). In this paper
we will focus mostly on the CSOMP component of αij .
From an implementation viewpoint, the CSOMP component is quite different from the other two components of
the OMP: it can be calculated from a knowledge of the
ground-state electron wavefunctions alone, but only after
careful attention is given to the need to choose a smooth
gauge in discretized k-space.
One of the motivations for the current work is the possibility of finding a material whose CSOMP component of
the linear magnetoelectric tensor will be large compared
to the total coupling in known magnetoelectric materials.
As elaborated in more detail in Sec. II, the basis for this
possibility arises from the before-mentioned theoretical
developments14 and the experimental verification of the
existence of Z2 topological insulators such as Bi1−x Sbx ,
Bi2 Se3 , Bi2 Te3 and Sb2 Te3 .15–17 Roughly speaking, we
seek a material that is similar to a Z2 topological insulator, but having broken inversion and time-reversal symmetries. In order to take the first steps toward searching for such materials, we have set out to calculate the
CSOMP component of the magnetoelectric tensor in several compounds of interest using density-functional the-

2
ory.
The paper is organized as follows. In Sec. II we provide theoretical background by reviewing the previouslyderived10,11 expression for the α tensor, and by discussing the connection between bulk and surface properties in a way that is analogous to the theory of surface
charge and bulk electric polarization. We also review the
connection to Z2 topological insulators and make some
general comments about symmetry. In Sec. III we discuss the gauge-fixing issues that arise when discretizing
the CSOMP expression on a k-point mesh, and show how
these can be resolved using Wannier-based methods. By
this route, we arrive at an explicit expression for the
CSOMP in terms of position matrix elements between
Wannier functions. We evaluate this expression in the
density-functional context for several materials of interest in Sec. IV. Finally, we summarize and give an outlook
in Sec. V.

II.

BACKGROUND AND MOTIVATION

In this section we briefly summarize previous work
from Refs. 10 and 11 on the orbital magnetoelectric
coupling (OMP), describe relationships between bulk
and surface properties, discuss motivations for this work
based on the discovery of strong Z2 topological insulators, and present a brief symmetry analysis.

B.

Theory of orbital magnetoelectric coupling

The purely electronic orbital magnetoelectric coupling
αij can be written in terms of three gauge-invariant contributions
αij = αCS
eLC
eIC
ij + α
ij + α
ij ,

(4)

CS
where αCS
is the above-mentioned (isotropic)
ij = δij α
LC
CSOMP, while α
eij and α
eIC
ij are two additional contributions. The isotropic part of the OMP tensor has contributions from the two α
e terms as well as from the CSOMP
term. The three contributions to the OMP can compactly be expressed as


Z
e
2i
CS
3
α =η
(5)
d k ǫijk tr Ai ∂j Ak − Ai Aj Ak ,
2
3
Z
e i unk i,
α
eLC
d3 k h∂ek unk |(∂l Hk )|D
(6)
ij = ηǫjkl Im
Z
e i umk ihumk |(∂l Hk )|unk i,
α
eIC
d3 k h∂ek unk |D
ij = ηǫjkl Im

(7)

where the notations are defined as follows. An implied
sum notation applies to repeated Cartesian (ijkl) and
band (mn) indices, corresponding to a trace over occupied bands in the latter case (written explicitly as ‘tr’). A
common prefactor η = −e/~(2π)3 appears in each equation, with e > 0 being the magnitude of the electron
charge. The Berry connection
Amnkj = humk |i∂j |unk i

A.

Units and conventions

In this paper we use SI units and define α according
to Eq. (1) using independent field variables E and B. It
follows that α has the same units as the vacuum admittance 1/cµ0 .18 While this is convenient from the point of
view of first-principles theory, where B is fixed to zero
in practice, the more conventional definition in the literature is in terms of fixed E and H fields, in which case
one has




∂Pi
∂Mj
EH
αij =
= µ0
(3)
∂Hj E
∂Ei H
and αEH has units of inverse velocity.19 In the typical
case that the magnetic susceptibility of the material is
negligible, these are related by αEH = αµ0 , and one can
define a reduced (dimensionless) quantity αr = cµ0 α =
cαEH .18 Defined in this way, αr is numerically equal to
the value of the magnetoelectric coupling in Gaussian
units using the conventions of Rivera,19 which in turn
corresponds to the notation “g.u.” (“Gaussian units”) in
some recent papers.7,9 Furthermore, using the notation
of Eq. (2) for the isotropic magnetoelectric coupling, it
follows that the diagonal component of αr is just θ/π
times the fine structure constant (which is e2 cµ0 /2h in
SI units).

(8)

is defined in terms of the cell-periodic Bloch functions
|unk i = e−ik·r |ψnk i,
−ik·r

(9)
ik·r

which are the eigenvectors of Hk = e
He , where
H is the bulk periodic Hamiltonian of the crystal at zero
electric and magnetic field. ∂j and Dj are the partial
derivatives with respect to the j-th component of the
wavevector k and the electric field E respectively. Finally,
the tilde indicates a covariant derivative, ∂ej = Qk ∂j and
e j = Qk Dj , where Qk = 1 − |unk ihunk | (sum implied
D
over n). Additional screening contributions to α
eLC
ij and
IC
α
eij that occur in the context of self-consistent field calculations, not given here, can be found in Ref. 11.
As in the case of electronic polarization, one needs to
be careful about relating the above bulk expressions to
experimentally measurable physical quantities, since arbitrary surface modifications can contribute to the effective measurable OMP. The relationship between the
OMP and experimentally measurable responses are explained in more detail in the next section.
C.

Relation between bulk and surface properties

In order to discuss the relationship between bulk and
surface quantities in connection with the OMP, it is in-

3
structive first to review the corresponding connections in
the theory of electric polarization.
1.

Electric polarization and surface charge

We first review the relationship between the bulk electric polarization, as obtained from the crystal bandstructure according to the Berry-phase theory,20,21 and a measurable quantity which is the macroscopic dipole moment
of a finite sample cut from this crystal. Given the set of
valence Bloch wavefunctions |ψnk i of an insulating crystal, one can readily calculate the electronic contribution
to the polarization as the integral
Z
e X
Pi = −
(10)
d3 k hunk |i∂ki |unk i
(2π)3 n
over the Brillouin zone (BZ). Gauge changes (|unk i →
e−iβ(k) |unk i) can change the value of this integral only
by Re/Ω, where R is a lattice vector and Ω is the unit
cell volume. The value of this integral is therefore only
well-defined modulo Re/Ω. In what follows we assume
that a definite choice of gauge has been made so that a
definite value of P has been established. We now analyze
how, and under what circumstances, one can relate this
P to the (experimentally measurable) dipole moment d
of an arbitrarily faceted finite sample of this crystal.
At each local region on the surface of this finite sample,
assuming a perfect surface preparation (defect-free with
ideal periodicity), we can relate P to the surface charge
density σ at that same point via21

e 
σ = P + R · n̂ + ∆.
(11)
Ω
Here n̂ is the surface normal unit vector, R is a lattice
vector, and ∆ is an additional contribution present only
for metallic surfaces. The term involving R, which corresponds to an integer number of electrons per surface
unit cell, is required because, for a given surface n̂, it
may be possible to prepare the surface in different ways
(e.g., by adding or subtracting a layer of ions, or by filling or emptying a surface band) such that the surface
charge per cell changes by a quantum. Thus, R is in
general a surface-dependent quantity in Eq. (11). If the
surface patch under consideration is not insulating, then
∆ is a term which measures the contribution of the partially occupied surface bands to the surface charge, and
is proportional to the area fraction of occupied band in
k space. (In the case of an insulator with non-zero first
Chern number, this fraction has to be calculated with
special care,22 but we shall not consider this case in what
follows.)
Now, let us consider the special case that all surfaces
are insulating (∆ = 0) and that the surface charges of all
surface patches are consistent with a single vector value
of R (“global consistency”). Under these circumstances,
the macroscopic dipole moment d of the crystallite is

given by

e 
d=V P+ R ,
Ω

(12)

which can be obtained trivially by integrating Eq. (11).
Here V is the volume of entire finite sample. As could
be anticipated, d/V has a component depending only
on the bulk wavefunctions and our gauge choice, and an
additional component eR/Ω reflecting the preparation of
the surfaces.
2.

OMP and surface anomalous Hall conductivity

We now discuss a corresponding set of relationships between the bulk-calculated OMP and the surface anomalous Hall conductivity.
Using Eqs. (5), (6), and (7) one can calculate the tensor
α from the knowledge of bulk Hamiltonian of an insulating crystal. Analogously as in the case of polarization,
one can again show that a gauge change23 must either
leave α invariant or change it by a quantum m(e2 /h)I,
where m is an integer and I is the unit matrix. More
precisely, this gauge transformation will only affect the
CSOMP component αCS of the OMP, since the other two
e LC and α
e IC are fully gauge-invariant (see
contributions α
Ref. 11 for details).
We now imagine cutting a finite crystallite from this
infinite crystal, and we wish to relate α to its physically
observable linear magnetoelectric coupling β, defined for
a finite sample by
βij =

∂µj
∂di
=
,
∂Bj
∂Ei

(13)

where di is the dipole moment of the finite sample and µj
is its magnetic dipole moment. We want to discuss this
relationship in a way that is analogous to that between
the bulk P and sample dipole moment d in Sec. II C 1.
As follows from Eq. (1), the application of an electric
field Ej to the insulating crystal induces the magnetization
Mk = αjk Ej ,

(14)

where α is given by Eq. (4) and is only determined modulo the quantum m(e2 /h)I. Having a homogeneous Mk
inside the sample and Mk = 0 outside is equivalent to
having a surface current Ki equal to
Ki = ǫikl Mk nl ,

(15)

where nl is the surface unit normal. By eliminating Mk
from these equations, we see that having a magnetoelectric tensor α is equivalent to having a surface anomalous
AH
Hall conductivity σij
= ǫikl αjk nl . If the surface patch
in question is insulating, then its anomalous Hall conductivity should just be given, modulo m(e2 /h)I, by this
equation. If instead the surface patch is metallic, then

4
an additional surface contribution ∆ij should be present,
leading to the relation


e2
AH
σij
= ǫikl αjk + m δjk nl + ∆ij .
h

(17)

which follows by integrating Eq. (16) over all surfaces.
This equation is in close analogy to Eq. (12) for the case
of electric polarization. In particular, we see that β/V
has a component α depending only on the bulk wavefunctions and our gauge choice, and an additional component that is an integer multiple of (e2 /h)I, reflecting
the preparation of the surfaces.
As will be discussed in the next section, time-reversal
symmetry imposes additional constraints on α, and some
care is needed in the interpretation of Eq. (17) for the
case of Z2 topological insulators.

D.

(b)

Z2

Z2

Vacuum

Vacuum

(16)

This equation is in precise analogy to Eq. (11) relating
the polarization to the surface charge. Here ∆ij may in
general contain dissipative contributions, but in the dirty
limit it will be dominated by the intrinsic surface contribution that can be calculated as a 2D BZ integral of the
Berry curvature of the occupied surface states.24 The integer quantum m appearing in Eq. (16) corresponds to
the theoretical possibility that the surface preparation
can be changed in such a way that a surface band having
a nonzero Chern number may become occupied. For example, this could be done in principle by constructing a
2D quantum anomalous Hall layer (as described, e.g., by
the Haldane model25 ), straining it to be commensurate
with the surface, and adiabatically turning on hopping
matrix elements to “stitch it” onto the surface.
In the special case that all surface patches are insulating (∆ij = 0), and all surface patches have an anomalous
Hall conductivity given by Eq. (16) with the same value
of m (“global consistency”), we can relate the experimentally measurable magnetoelectric response β of the finite
crystallite to the bulk-calculated α via


e2
β =V α+m I ,
h

(a)

Motivation and relationship to strong Z2
topological insulators

In this Section, we give arguments to motivate our
hope that in certain materials the CSOMP might be
on the order of, or even much larger than, the total
magnetoelectric coupling in typical known magnetoelectric materials. For simplicity, we focus henceforth only
on the CSOMP part of the total OMP response, even
though there are additional contributions coming from
α
eLC and α
eIC . Thus, from now on, the quantity θ measures the strength of the CSOMP through the relation
αCS = θe2 /2πh.

FIG. 1. Identical samples cut from a strong Z2 topological
insulator, but with two different surface preparations. (a)
Time-reversal symmetry is preserved at vacuum-terminated
surfaces; the net magnetoelectric coupling of this sample is
zero. (b) Time-reversal symmetry is broken at the surface as
a result of exchange coupling to an insulating ferromagnetic
adlayer; if this opens a gap in the surface-state spectrum,
the entire sample will behave as if it has a magnetoelectric
coupling of exactly θ = π.

1.

Time-reversal symmetry constraints on θ

Let us analyze the allowed values of θ for an infinite bulk insulating system that respects time-reversal
(T ) symmetry. Since T flips the sign of the magnetic
field, it will also reverse the sign of θ. As mentioned
earlier in Sec. II C 2, however, the value of θ can be
changed by 2π under a gauge transformation. Therefore
one concludes12,13 that the allowed values of θ consistent with T symmetry are 0 mod 2π and π mod 2π, and
that these two cases provide a topological classification of
all T -invariant insulators. Indeed, this classification has
been shown12,13 to be identical to the one based on the
Z2 index, with Z2 -odd or “strong topological” insulators
having θ = π, while Z2 -even or “normal” insulators have
θ = 0, even though the Z2 index is most often introduced
e LC = α
e IC = 0 in
in a different context.26 (Incidentally, α
both cases since these terms are fully gauge-independent,
unlike the CSOMP term which can be changed by 2π.)
Consider now a finite sample of a normal (Z2 -even) T symmetric insulator (θ = 0 in the bulk) with insulating
surfaces (∆ij = 0) prepared in a way that the integer m
is nonzero, and the same on every surface. From Eq. (17)
we conclude that this sample will have a non-zero magnetoelectric response, β, proportional to m. Obviously a
sample that has T symmetry both in the bulk and on the
surface must have β = 0, and therefore we conclude that
this system needs to have broken T reversal symmetry
at the surface. As mentioned earlier, one could, at least
formally, prepare such a surface by starting from the one
that has m = 0 and then absorbing to each surface a
layer of anomalous Hall insulator25 with Chern index m.
Such a procedure will keep the surfaces insulating but it
will necessarily break the T -reversal symmetry.
Next we analyze the case of a strong Z2 topological
insulator having θ = π, or equivalently, α = αCS =
(e2 /2h) I. We first consider a sample of such a system

that has T symmetry conserved at its surfaces, as in
Fig. 1(a). Again, since the entire sample is T -symmetric,
its experimentally measurable magnetoelectric coupling
tensor β clearly has to vanish. Using Eq. (16) and the
fact that m can take on only integer, and not half-integer,
values, we conclude that the only way to make the response of the entire sample vanish is to have ∆ij be nonzero. This requires that the surfaces of such a system
must be metallic. Moreover, since the contribution ∆ij
of the metallic surface band to the surface anomalous Hall
conductivity is just given by the Berry phase around the
Fermi loop,24 the needed cancellation requires this Berry
phase to be exactly ±π. All this is in precise accord
with the known properties of Z2 -odd insulators and their
topologically protected surface states.26
The Kramers degeneracy at the Dirac cone in the surface bandstructure can be removed by the application of
a T -breaking perturbation to the surface. In principle,
this could be accomplished, for example, by applying a
local magnetic field to the surface or by interfacing the
surface to an insulating magnetic overlayer. In the latter
case, the interatomic exchange couplings provide a kind
of effective magnetic field acting on the surface layer of
the topological insulator. If the local Fermi level resides
in the gap opened by field, then the surface becomes insulating. If the field can be consistently oriented (see
Ref. 12) on each patch of the surface, either along or opposite the direction of surface normal vector n (as shown
in Fig. 1(b)), then the entire surface becomes insulating.
It is important that the field is applied consistently in
the same direction with respect to n, since conducting
channels will otherwise appear at domain boundaries.26
If all of these requirements are met, the surface contribution ∆ij to β vanishes, so that β = Vα with α given
only by bulk value of θ = π (assuming m = 0 for simplicity). Therefore such a sample of a strong Z2 topological
insulator would behave as if the entire sample has exactly
half a quantum of magnetoelectric coupling (θ = π), even
though its bulk is time-reversal symmetric!

2.

Prospects for large-θ materials

Recently surface-sensitive ARPES measurements have
experimentally confirmed that several compounds,15–17
including Bi1−x Sbx , Bi2 Se3 , Bi2 Te3 and Sb2 Te3 , do indeed behave as strong Z2 topological insulators. Therefore their bulk wavefunctions must be characterized by
θ = π. Up to now, the corresponding magnetoelectric
response has not been measured experimentally, in part
because of the difficulties in obtaining truly insulating behavior in the bulk, as well as the need to gap the surfaces
by putting them in contact with magnetic overlayers as
described earlier.
We believe that a more promising approach to observing a large CSOMP (i.e., θ comparable to π) is to consider
an insulator that has neither T nor spatial inversion symmetry. In this case the Z2 classification does not apply,

Symmetry breaking

5

θ arbitrary

Metal
θ = 0 mod 2π
θ = π mod 2π
Symmetry preserving

FIG. 2. (Color online) Schematic view of the allowable values
of θ in different parts of the two-parameter space of some unspecified model Hamiltonian. Horizontal axis corresponds to
the perturbation that preserves at least one of the symmetries
that render θ to be 0 or π (see Sec. II E). Vertical axis parameterizes a perturbation that breaks those symmetries and
allows θ to be arbitrary. See text for the details.

and the surface can be gapped without any need to apply
a T -breaking perturbation. (A more precise statement of
the symmetry considerations will be given in Sec. II E.)
The sample can then display a bulk magnetoelectric coupling of the simple form β = Vα. We note that an orbital magnetoelectric coupling of θ ≃ π (i.e., αr ≃ 1/137)
would correspond to αEH ≃ 24.3 ps/m, a value that is
significantly larger than the observed coupling in Cr2 O3 ,
one of the best-studied magnetoelectric materials. For
comparison, the reported experimental values for αEH
⊥ in
Cr2 O3 , which are presumably dominated by spin-lattice
coupling, range between 0.7 and 1.6 ps/m at 4.2 K.27,28
Of course, in order to have a good chance of finding
a material with a large θ, it may be advisable to look
for materials with some of the same characteristics as
the known Z2 -odd insulators, of which the most important is probably the presence of heavy atoms with strong
spin-orbit coupling. We see no strong reason why such a
search might not reveal a material having a large OMP
in the above sense.
To illustrate the kind of a search we have in mind, consider some model Hamiltonian that depends on two parameters, one that preserves either the T or spatial inversion symmetry (or both), and another that that breaks
symmetry such that θ takes a generic value. The possible behavior of such a model is sketched in Fig. 2, where
these two parameters are plotted along the horizontal
and vertical axes respectively. The figure also indicates
the generic value of θ in each region of parameter space.
Along the horizontal axis, where the extra symmetry is
present, three regions are indicated. The black dot indicates a point of gap closure forming the boundary between a normal T -symmetric insulator regime on the left
(θ = 0) and a strong Z2 topological insulator regime on
the right (θ = π). If the system is carried along the hori-

6
TABLE I. Magnetic point groups for which a non-zero
CSOMP is allowed by symmetry. Notation follows Ref. 29.
Point groups in bold allow only for a purely isotropic magnetoelectric tensor.
1
m′ m′ m′
6̄′
3m′
23

1̄′
4
6/m′
3̄′ m′
m′ 3

2
4̄′
422
622
432

m′
4/m′
4m′ m′
6m′ m′
4̄′ 3m′

2/m′
3
4̄′ 2m′
6̄′ m′ 2
m′ 3m′

222
m′ m′ 2
′
3̄
6
4/m′ m′ m′ 32
6/m′ m′ m′

III.

In this section we present our methods for calculating the CSOMP in the framework of density-functional
theory, and analyze in more detail its mathematical properties and the formal similarities to the formulas used to
calculate electric polarization and anomalous Hall conductivity.

A.

zontal axis, θ must be either 0 or π except at the critical
point, and it must therefore jump discontinuously when
passing through this point of metallic behavior. On the
other hand, if we now imagine passing from the Z2 -odd
to the Z2 -even phase along the dashed curve in Fig. 2,
θ can vary smoothly and continuously from π to 0 without any gap closure anywhere along the path. If we can
identify a material lying near, but not at, the right end of
this dashed path, it could be the kind of large-θ material
we seek.
Thus, our ultimate goal is to use first-principles calculations to search for a large θ, not in a topological insulator, but in an “ordinary” (but presumably strongly
spin-orbit coupled) insulating magnetic material. While
our work has yet to result in the identification of a largeθ material of this kind, it represents a first step in the
desired direction.

E.

General symmetry considerations

Recall that θ is a pseudoscalar that changes sign under time-reversal and spatial-inversion symmetries (since
B changes sign under T while E changes sign under inversion). On the other hand, θ is invariant under any
translation or proper rotation of a crystal. Therefore if
the magnetic point group of a crystal contains an element
that involves T , possibly combined with a proper rotation, the value of θ is constrained to be 0 or π (modulo
2π) as discussed earlier. The same happens if the magnetic point group contains inversion symmetry or any
other improper rotation.
All 32 of the 122 magnetic point groups that do not
contain such symmetry elements, and which therefore
allow for an arbitrary value of θ, are listed in Table I.
(The bold entries in the table are those magnetic groups
for which the tensor α must be isotropic, i.e., a constant
times the identity matrix; the same magnetic groups were
also analyzed in Ref. 18). Clearly we can constrain our
search for interesting materials to the cases listed in the
Table.

METHODS

Review of Berry formalism

Assume we are given the Bloch wavefunctions |ψnk i =
eik·r |unk i as a function of wavevector k in the ddimensional BZ (d = 1, 2, or 3) for an insulator having
valence bands indexed by n ∈ {1, . . . , N }. We work with
the cell-periodic Bloch functions unk (r) = e−ik·r ψnk (r)
and allow them to be mixed at each k point by an arbitrary k-dependent unitary matrix
|unk i → |umk iUmnk

(18)

(sum on m implied). After this gauge transformation the
wavefunctions are no longer eigenfunctions of the Hamiltonian, but they span the same N -dimensional subset of
the Hilbert space as the true eigenfunctions. For any
given choice of gauge, we define the Berry connection
Amnkj = humk |i

∂
|unk i,
∂kj

(19)

which is a k-dependent N × N × d matrix that measures,
at each k point, the infinitesimal phase difference between the m-th and n-th wavefunctions associated with
neighboring points along Cartesian direction j in k space.
This object was already briefly introduced in Eq. (8).
In the context of electronic structure calculations, we
can now list three material properties that can be evaluated knowing only the Berry connection: the electric
polarization, the intrinsic anomalous Hall conductivity,
and the CSOMP.
The electric polarization P already appears in dimension d = 1 and it can be evaluated as an integral of the
Berry connection over the one-dimensional BZ as20
Z
e
P =−
dk trAk ,
(20)
2π BZ
where the trace is performed over the band indices of the
Berry connection, as in Eq. (10). The integrand is also
referred to as the Chern-Simons 1-form, and its integral
over the BZ is well known to be defined only modulo
2π. Any periodic adiabatic evolution of the Hamiltonian
H(λ) whose first Chern number in (k, λ) space is non-zero
will change the integral above by a multiple of 2π.20
Unlike one-dimensional systems, crystals in d = 2 can
have an anomalous Hall conductivity. For a metal, the intrinsic contribution from a band crossing the Fermi level

7
(a)

P ∼

R

(b)

A

σ AH ∼

(c)

H

A

θ∼

R

with the integral of Berry connection in the square orthogonal to that direction (as in Eq. (21)), followed by a
symmetrization over the three Cartesian directions.
B.

A i ∂j A k

FIG. 3. Graphical interpretation of Eqs. (20) (a), (21) (b)
and (22) (c) in the case of one occupied electron band and
for cubic crystal symmetry, for simplicity. See text for more
detail.

can be evaluated as a line integral24,30
I
e2 1
dk · Ak
σ AH =
h 2π FL

(21)

over the Fermi loop. Fully-filled deeper bands can also
make a quantized contribution given by a similar integral, but around the entire BZ; this is the only contribution in the case of a quantum anomalous Hall insulator.25
(In both cases, the gauge choice on the boundary of the
region should be consistent with a continuous, but not
necessarily k-periodic, gauge in its interior; alternatively,
each expression can be converted to an area integral of a
Berry curvature to resolve any uncertainty about branch
choice. See Ref. 31 for more details.)
Finally, unlike one- or two-dimensional systems, threedimensional systems can have an isotropic magnetoelectric coupling. The CSOMP can be evaluated in d = 3 as
a BZ integration of a quantity involving the Berry connection:


Z
2i
1
3
d kǫijk tr Ai ∂j Ak − Ai Aj Ak . (22)
θ=−
4π BZ
3
The integrand in this expression is known as the ChernSimons 3-form, and its integral over the entire BZ is again
ill-defined modulo 2π, since any periodic adiabatic evolution of the Hamiltonian H(λ) whose second Chern number in (k, λ) space is non-zero will change θ by an integer
multiple of 2π.12,13
The sketches in Fig. 3 compare the geometrical characters of the operations needed to evaluate Eqs. (20-22)
in practice. We consider the case of one occupied electron band for simplicity. The polarization of Eq. (20) is
calculated by a line integral; on a discrete k-mesh, the
integral of the Berry connection A over each of line segment, as in Fig. 3(a), is converted to a discretized form
(see Eq. (23)). Similarly, in two dimensions the anomalous Hall conductivity of Eq. (21) can be calculated as
suggested in Fig. 3(b) by dividing the occupied part of
the BZ into small square segments and then integrating
A around each square. (Equivalently, one can integrate
A along the Fermi loop.31 ) In three dimensions, Fig. 3(c),
Eq. (22) can be evaluated by dividing the BZ into small
cubes. In each, one needs to multiply the integral of
A along one of the Cartesian directions (as in Eq. (20))

Numerical evaluation of θ

In electronic-structure calculations, the cell-periodic
wavefunctions |unk i are typically calculated on a uniform
k-space grid with no special gauge choice; in general, one
should assume that the phases have been randomly assigned. Nevertheless, it is straightforward to construct a
gauge-invariant polarization formula that is immune to
this kind of scrambling of the gauge.32 In one dimension
with kj for j ∈ {1, . . . , M } (where kM is the periodic image of point k1 ), the electronic polarization is calculated
as


e
P =
(23)
Im ln det Mk1 k2 Mk2 k3 ...MkM −1 kM
2π
where the overlap matrix Mkk′ is defined as
[Mkk′ ]mn = humk |unk′ i.

(24)

The reason for using Eq. (23) is that the determinant
of the matrix Mk1 k2 Mk2 k3 ...MkM −1 kM is gauge-invariant
under any transformation in the form of Eq. (18). Additionally, the implementation of Eq. (23) is numerically
stable even when there are band crossings. A similar
gauge-invariant discretization can also be used to calculate the anomalous Hall conductivity σ AH .31
Unfortunately, except in the single-band (“Abelian”)
case, we are unaware of any corresponding gaugeinvariant discretized formula for the integral of the
Chern-Simons 3-form. As a result, we have no prescription for computing the CSOMP that is exactly gaugeinvariant for a given choice of k mesh. This is a serious problem. Unlike the calculation of the polarization, which is straightforward even if the gauge is randomly scrambled at each mesh point, the calculation of
the CSOMP requires that we first identify a reasonably
smooth gauge on the discrete mesh.
The problem of finding a smooth gauge in k is essentially the same as that of finding well-localized Wannier
functions. For this reason, we have adopted here the
approach of first constructing a Wannier representation
for the valence bands, and then using it to compute the
CSOMP. In fact, starting from Eq. (22), we derive an expression that allows us to compute θ directly in the Wannier representation. Once we have well-localized Wannier functions, this guarantees smoothness of the gauge
and avoids problems with band crossings. Admittedly,
such a formula still depends on the gauge choice, meaning that different choices of Wannier functions will lead
to slightly different results. However, this difference will
vanish as one increases the density of the k-point mesh,
since in the continuum limit the k-space expression for
θ is gauge-invariant (modulo 2π). More precisely, we expect the calculation of θ to converge once the inverse of

8
the k-point mesh spacing becomes much larger than the
spread of the Wannier functions.
Therefore, we adopt the strategy of calculating θ on
k meshes of different density, and extrapolating θ to the
limit of an infinitely dense mesh. Furthermore, we construct maximally-localized Wannier functions (MLWF)
following Ref. 32, expecting this to give relatively rapid
convergence as a function of the k mesh density.
Recall that the Wannier function associated with (generalized) band index n in unit cell R is defined in terms
of the rotated Bloch states (18) as
Z
Ω
d3 k eik·(r−R) |umk iUmnk .
(25)
|Rni =
(2π)3
In the case of MLWFs, the Umnk are chosen in such a way
that the total quadratic spread of the Wannier function
is minimized.32 (In practice the BZ integral is replaced
by a summation over a uniform grid of k points.)
Using Eq. (25), one can relate the Berry-connection
matrix Amnkj in the smooth gauge to the Wannier matrix elements of the position operator through32
X
Amnkj =
eik·R h0m|rj |Rni.
(26)
R

Replacing each occurrence of Aj in Eq. (22) with the
above gives, after some algebra,
 X
1 (2π)3
1
θ=
ǫijk Im
h0m|ri |RnihRn|rj |0miRk
4π Ω
3
R

2X
−
h0l|ri |RmihRm|rj |PnihPn|rk |0li , (27)
3
RP

where the sum is implied over band (lmn) and Cartesian
(ijk) indices.
To obtain a more symmetric form, we introduce a modified position-operator matrix element between WFs defined as
hRm|r̃i |Pni = hRm|ri |Pni (1 − δmn δRP )

(28)

the reassignment of a Wannier function to a neighboring cell.) The validity of Eqs. (27) and (31) has been
tested numerically by comparing with the evaluation of
Eq. (22) for the case of a tight-binding model introduced
in Ref. 11. The evaluated expressions agreed to numerical accuracy after extrapolation to the infinitely dense
mesh. These expressions can also be shown to be gaugeinvariant by working directly within the Wannier representation.

C.

Computational details

Calculations of the electronic ground state and
of structural relaxations were performed using the
Quantum-ESPRESSO package,34 and the Wannier90
code35 was used for constructing maximally localized
Wannier functions. We used radial-grid discretized
HGH36 norm-conserving pseudopotentials. Calculations
were performed in the noncollinear spin framework, including spin-orbit effects as incorporated in the pseudopotentials. In all calculations we used the PerdewWang37 LDA energy functional. The pseudopotentials
used for Cr, Fe and Gd contain semi-core states, while
the ones for Al, Bi, Se and O do not.
The self-consistent calculations on Cr2 O3 were performed on a 4 × 4 × 4 Monkhorst-Pack38 grid in k space.
Non-self-consistent calculations for the Wannier-function
construction were performed on k-space grids containing
the origin and ranging in size from 6×6×6 to 12×12×12.
The plane-wave energy cutoff was chosen to be 150 Ry.
In the case of Bi2 Se3 , the self-consistent calculations
were performed on a 6 × 6 × 6 grid with energy cutoff of
60 Ry, while the non-selfconsistent calculation was done
on grids between 6 × 6 × 6 and 11 × 11 × 11.
The position-operator matrix elements h0m|rj |Rni
needed to evaluate Eq. (31) were calculated in k space
by inverting the Fourier sum in Eq. (26) over the nonself-consistent k-point mesh, and then approximating the
k derivative in Eq. (19) by finite differences on that mesh,
as detailed in Ref. 30.

and a notation for the Wannier center
τni = h0n|ri |0ni.

(29)

Then Eq. (27) becomes
1 (2π)3
ǫijk ×
(30)
θ=
4π  Ω
X
Im
h0m|r̃i |RnihRn|r̃j |0mi (Rk + τnk − τmk )
R

−

X2
RP

3


h0l|r̃i |RmihRm|r̃j |PnihPn|r̃k |0li . (31)

We find this form more convenient because it separates
the contributions of diagonal and off-diagonal elements
of position operators.33 (It is also manifestly invariant to

IV.

RESULTS AND DISCUSSION

A.

Conventional magnetoelectrics

In this section we present the results of our firstprinciples electronic-structure calculations of θ. We begin with conventional magnetoelectrics, i.e., materials
that are already experimentally known to have a nonzero magnetoelectric tensor. Some of these materials do
not allow all diagonal components of the magnetoelectric tensor to be non-zero. We omit those materials from
our analysis here, since we are interested in calculating
the CSOMP part of the magnetoelectric coupling, which
would vanish in such cases. We first present our results

9
(a)

(b)
3

3
A
B
C
A
B
C
A
B
C
A
B
C
A
B
C

FIG. 4. (Color online) (a) Rhombohedral unit cell of Cr2 O3 .
Magnetic moments on Cr atoms are indicated by red arrows
and oxygen octahedra are drawn around each Cr atom. (b)
Schematic of hexagonal unit cell of Bi2 Se3 with imposed local
Zeeman field on Bi atoms. Induced magnetic moments are
shown by red arrows. Thick blue lines indicate Se layers;
letters (ABC) indicate stacking sequence. In both panels, the
vertical line indicates the 3-fold rhombohedral axis, and the
cross designates a 2-fold rotation axis orthogonal to the plane
of the figure (also a center of inversion coupled with time
reversal).

on Cr2 O3 in some detail, and then briefly discuss our
results for BiFeO3 and GdAlO3 .

1.

Calculation of θ in Cr2 O3

We first fully relax the structure in the R3̄c space group
and obtain the Wyckoff position to be x = 0.1575 for Cr
atoms (4c orbit) and x = −0.0690 for O (6e orbit). The
length of the rhombohedral lattice vector is a = 5.3221 Å
while the rhombohedral angle is 53.01◦. The Cr atoms
have magnetic moments pointing along the rhombohedral
axis as illustrated in Fig. 4(a) in an antiferromagnetic arrangement. The value of the magnetic moment is 2.0 µB
per Cr atom and the electronic gap is 1.3 eV, which agrees
well with previous LDA+U calculations39,40 in the limit
where the on-site Coulomb parameter U is set to zero.
Neglecting for a moment the magnetic spins on the Cr
sites, the space-group generators are a three-fold rotation, a two-fold rotation, and an inversion symmetry as
indicated in Fig. 4(a). Its point group is therefore 3̄m.
If we now include the spins on the Cr atoms in the analysis, we find that the three-fold and two-fold rotations
remain, while the inversion becomes a symmetry only
when combined with time-reversal. Therefore the magnetic point group of Cr2 O3 is 3̄′ m′ .41 This magnetic point
group allows θ to be different from 0 or π, as discussed
in Sec. II E.
Figure 5 shows the calculated values of θ using Eq. (31)
for Cr2 O3 with k-space meshes of various densities. The

FIG. 5. (Color online) Calculated value of θ in Cr2 O3 for
varying densities of k-space grids, where ∆k is the nearestneighbor distance on the grid. Top axis specifies the size of the
corresponding uniform Monkhorst-Pack grid. Line indicates
a quadratic extrapolation of θ to the infinitely dense k mesh.

line indicates the second-order polynomial extrapolation
to an infinitely dense mesh. The extrapolated value of θ
is 1.3 × 10−3, which is a small fraction of the quantum of
EH
EH
OMP θ = 2π and corresponds to αEH
xx = αyy = αzz =
0.01 ps/m. The positive sign of θ pertains to the pattern
of Cr magnetic moments shown in Fig. 4(a); reversal of
all magnetic moments would flip the sign of θ.
In order to compare this value of the magnetoelectric
coupling with experimental values and other theoretical
calculations, we somewhat arbitrarily define
αeff =

|αxx | + |αyy | + |αzz |
.
3

(32)

The value of αeff obtained from the results of Ref. 8
is 0.23 ps/m for the purely electronic part of the spinmediated component. Therefore, our calculated CSOMP
contribution in Cr2 O3 amounts to only 4% of this electronic spin component. The ionic component of the
spin response calculated by the same authors results in
αeff = 0.74 ps/m, while the one calculated in Ref. 7 is
about 2.6 times smaller, 0.29 ps/m. (In both of these
calculations, αzz is zero.) Finally, experimental measurements of the magnetoelectric tensor in Cr2 O3 at
4.2 K vary between αeff = 0.55 ps/m and 1.17 ps/m (see
Refs. 27 and 28 respectively).
Clearly, our computed CSOMP contribution for Cr2 O3
is negligible, being two orders of magnitude smaller than
the dominant lattice-mediated spin contribution. This is
probably not surprising, since the spin-orbit coupling is
relatively weak in this material. Given that it is weak,
we can guess that that magnitude of the CSOMP should
be linear in the strength of the spin-orbit interaction in
Cr2 O3 . Our calculations allow us to check this by varying the spin-orbit interaction strength λSO between 0 (no
spin orbit) and 1 (full spin-orbit interaction). As shown
in Fig. 6, if we calculate θ for various intermediate values of λSO , we see that the CSOMP does indeed depend

10

FIG. 6. (Color online) Calculated θ in Cr2 O3 as a function
of spin-orbit coupling strength, scaled such that λSO = 1 corresponds to the full spin-orbit coupling strength and θ0 =
θ(λSO = 1).

FIG. 7. (Color online) Calculated value of θ in Bi2 Se3 for
varying densities of k-space grids, where ∆k is the nearestneighbor distance on the grid. Top axis specifies the size of the
corresponding uniform Monkhorst-Pack grid. Line indicates
a quadratic extrapolation of θ to the infinitely dense k mesh.

roughly linearly on λSO .

2.

Other conventional magnetoelectrics

We have also carried out calculations of θ in BiFeO3
and GdAlO3 , but with a smaller number of k-point grids
than in the case of Cr2 O3 . Therefore, our results are
less accurate, but should still give a correct order-ofmagnitude estimate of θ.
For BiFeO3 we perform the calculation in the 10-atom
antiferromagnetic unit cell (the long-wavelength spin spiral was suppressed). We obtain an electronic band gap
of 0.95 eV with magnetic moments of 3.5 µB on each Fe
atom, and with a net magnetization of 0.1 µB per 10-atom
primitive unit cell due to the canting of the Fe magnetic
moments. Extrapolating θ to an infinitely dense mesh
using just 6 × 6 × 6 and 8 × 8 × 8 k-point meshes, we obtain θ = 0.9 × 10−4 . In the case of GdAlO3 we calculate
the electronic band gap to be 5.0 eV and the Gd magnetic
moment to be 6.7 µB . We obtain a value of θ = 1.1×10−4
after extrapolating calculations using 4×4×4 and 6×6×6
k-space meshes. Thus, it is clear that the CSOMP is very
small in both materials.

B.

Strong Z2 topological insulators

We now investigate the CSOMP in the case of Bi2 Se3 ,
which is known experimentally17 and theoretically42 to
belong to the class of strong Z2 topological insulators.
In the absence of broken T symmetry, such a material
should have a θ of exactly π (modulo 2π). We first confirm this numerically. Then, in Sec. IV C, we also study
what happens when T is broken artificially by inducing
antiferromagnetic order on the Bi atoms and tracking the
resulting variation of θ.
Bi2 Se3 is known to belong to space group R3̄m, with

Bi at a 2c site and Se at the high-symmetry 1a site as
well as at a 2c site. In our calculations we find that
the Wyckoff parameters for Bi and Se are x = 0.4013
and 0.2085 respectively. We also find the length of the
rhombohedral lattice vector to be a = 9.5677 Å and the
rhombohedral angle to be only 24.77◦ . The electronic
gap is calculated to be 0.4 eV.
The generators of the R3̄m space group are again threefold and two-fold rotations and inversion (point group
3̄m). Since the system is nonmagnetic, the magnetic
space group also contains the T symmetry operator, and
its magnetic point group is 3̄m1′ . According to the analysis given in Sec. II E, it is clear that θ must therefore be
zero or π (modulo 2π).
Since we know that Bi2 Se3 is a strong Z2 topological insulator, we expect that θ should be equal to π
(modulo 2π). However, special care needs to be taken
in order to evaluate θ in such a case, because the choice
of a smooth gauge becomes problematic. Specifically,
it is known that the Z2 topology presents an obstruction to the construction of a Wannier representation (or
equivalently, a smooth gauge in k space) that respects T
symmetry.43,44 Therefore, during the maximal localization procedure, one needs to choose trial Wannier functions that do not take the form of Kramers pairs, thereby
explicitly breaking the T symmetry.45 (It is important to
note that this choice of Wannier functions does not bias
our calculation towards having θ = π, since the same
starting choice of T -symmetry-broken Wannier functions
for a normal T -symmetric insulator would result in θ = 0
up to the numerical accuracy of the calculation.)
Our results for θ in Bi2 Se3 are given in Fig. 7 for various densities of k meshes, ranging from 6 × 6 × 6 to
11 × 11 × 11. A quadratic polynomial extrapolation to
the infinitely dense mesh limit gives θ = 1.07π. This is in
reasonable agreement with the expected value of θ = π,
given the uncertainties in the extrapolation. (Of course,

11

FIG. 8. Calculated value of θ (vertical axis) and induced
magnetic moment on the Bi atom (horizontal axis) for Bi2 Se3
with artificially applied staggered Zeeman field on Bi atoms,
as described in the text. θ0 is the value of CSOMP when
magnetic field is not present.

if we make a time-reversed choice of starting Wannier
functions, we obtain θ = −1.07π, which is consistent,
within the errors, with θ = −π and modulo 2π to θ = π.)
Clearly the convergence with respect to mesh density is
somewhat slow, making a precise extrapolation difficult.
The reasons for this, and some possible paths to improvement, will be discussed in Sec. V.

C.

Z2 -derived nontopological insulators with
broken symmetries

Even though θ = π in Bi2 Se3 , a finite sample with T
symmetry preserved everywhere, including at the surfaces, will not exhibit any magnetoelectric coupling.
From the point of view of the discussion in Sec. II D, this
happens because of an exact cancellation between θ = ±π
contributions coming from the bulk (α) and metallic surface (∆) terms in Eq. (16). However, if one breaks the
T symmetry in the bulk (and possibly some other bulk
symmetries, as detailed in Sec. II E), the CSOMP term
can become allowed.
The magnetic space group of Bi2 Se3 contains both T
and spatial inversion symmetries. The presence of either
by itself is enough to insure that θ = 0 or π (modulo
2π). Now let us consider turning on, “by hand,” a local
Zeeman field on each Bi atom in the staggered arrangement shown in Fig. 4(b), i.e., with fields oriented parallel
to the rhombohedral axis and alternating in sign. The
induced magnetic moments along the three-fold axis preserve both three-fold and two-fold rotation symmetries;
both inversion and T symmetries are broken, but T taken
together with inversion is still a symmetry. The resulting
magnetic point group of the system is again 3̄′ m′ , as it
was for Cr2 O3 , and it does allow for a CSOMP (the same
magnetic arrangement has also been discussed in Ref. 46
in a different context).

In the density functional calculation one can easily apply a local Zeeman field to individual atoms in an arbitrary direction.47 Using this method, we have calculated the CSOMP in Bi2 Se3 with the pattern of local
fields described previously and illustrated in Fig. 4(b).
Fig. 8 presents the calculated values of θ as a function
of induced magnetic moment on Bi, where a positive µBi
corresponds to the pattern of magnetic moments indicated in Fig. 4(b). (Actually this was done by applying
the full extrapolation procedure of Fig. 7 for one case,
µBi = 0.16 µB , and using this to scale the results calculated on the 10 × 10 × 10 grid at other µBi .) The
dependence of the change in CSOMP on the magnetic
moment is linear over a wide range. One can see that
for a relatively moderate magnetic moment of ±0.27 µB ,
the value of θ is changed from π to π±0.55. (For much
higher local magnetic fields, Bi2 Se3 becomes metallic and
the CSOMP becomes ill-defined.)
These results indicate that it is possible, at least in
principle, for a magnetic material to have a large but
unquantized value of θ, thereby providing an incentive for
future searches for materials in which such a state arises
spontaneously, without the need to apply perturbations
by hand as done here.

V.

SUMMARY AND OUTLOOK

In this manuscript, we have presented a first-principles
method for calculating the Chern-Simons orbital magnetoelectric coupling in the framework of density-functional
theory. We have also carried out calculations of this
coupling for a few well-known magnetoelectric materials, namely Cr2 O3 , BiFeO3 and GdAlO3 . Unfortunately,
in these materials the CSOMP contribution to the total magnetoelectric coupling is quite small. This is not
surprising, since in most magnetoelectric materials the
coupling is expected to be dominated by the latticemediated response, whereas the CSOMP is a purely electronic (frozen-ion) contribution. Moreover, the CSOMP
is part of the orbital frozen-ion response, which is again
expected to be smaller then the spin response, except perhaps in systems with very strong spin-orbit coupling, as
discussed in Sec. I. For example, in Cr2 O3 the CSOMP
is about 4% of the frozen-ion spin contribution to the
magnetoelectric coupling.
On the other hand, we have reasons to believe that
in special cases the CSOMP contribution to the magnetoelectric coupling could be large compared to the total
magnetoelectric coupling in known magnetoelectrics such
as Cr2 O3 . After all, as already pointed out in Sec. II D 2,
Z2 topological insulators are predicted to display a large
magnetoelectric effect of purely orbital origin when their
surfaces are gapped in an appropriate way. If this is so,
why shouldn’t a similar effect occur in certain T -broken
systems?
As a proof of concept for the existence of those special
cases, we have considered Bi2 Se3 with inversion and time-

12
reversal symmetries explicitly broken “by hand.” Here
we find that with a relatively modest induced magnetic
moment on the Bi atoms, one can still achieve quite a
large change in the CSOMP.
On the computational side, there still remain several
challenges. For example, the convergence of our calculations of the CSOMP with respect to the k-point mesh
density is disappointingly slow. A direct calculation of
θ in Bi2 Se3 using a very dense mesh of 11 × 11 × 11 k
points only manages to recover about 30% of the converged value of θ = π, and an extrapolation procedure
is needed to brings us within 10% of that value. This
clearly points to the need for methodological improvements, and we now comment briefly on some possible
paths for future work.
The slow convergence that we observe is related in part
to the way in which we evaluate the position-operator
matrix elements h0m|rj |Rni. As discussed in Ref. 30,
the k-space procedure we adopted (see Sec. III C) entails
an error of O(∆k 2 ). Preliminary tests on a tight-binding
model suggest that an exponentially fast convergence of
θ can be achieved by an alternative procedure, in which
the WFs are first constructed on a real-space grid over
a supercell (whose size scales with the k-mesh density),
and the position matrix elements are then evaluated directly on that grid, as in Ref. 48. It may also be possible
to improve the k-space calculation by using higher-order
finite-difference formulas that have a more rapid convergence with respect to mesh density.
An alternative approach would be to develop a formula
for the CSOMP that is exactly gauge invariant in the case
of a discretized k-space grid. Such an expression already
exists for the case of electronic polarization, Eq. (23), but
we are aware of no counterpart for the CSOMP. Even
though such an approach would not necessarily provide
much faster convergence with respect to the k-space sampling, it would still be a significant improvement. For example, one would not need to construct a smooth gauge
in k space, which is a particular problem in the case of
Z2 insulators (or for a symmetry-broken insulator in the
vicinity of a Z2 phase). Another use of such a formula
would be to calculate with relative ease the Z2 index of
any insulator, even in the cases when other methods49–51
cannot be applied (for example, when inversion symmetry is not present).

Furthermore, a full calculation of the electronic contribution to the orbital magnetoelectric response should
also include the remaining two contributions given in
Eqs. (6) and (7). This calculation would also require a
knowledge of the first derivatives of the electronic wavefunctions with respect to electric field. While these
derivatives are available as part of the linear-response
capabilities of the Quantum-ESPRESSO package,34
some care is needed to arrive at a robust implementation of Eqs. (6) and (7), as will be reported in a future
communication.
Finally, recall that our calculations have all been carried out in the context of ordinary density-functional theory. In cases where orbital currents play a role, it is
possible that current-density functionals52,53 could give
an improved description. However, such functionals are
still in an early stage of development and testing, and
we prefer to focus first on exploring the extent to which
conventional density functionals can reproduce experimental properties of systems in which orbital currents
are present.
Overall, significant progress has been made in the ability to calculate the magnetoelectric coupling of real materials in the context of density-functional theory. The
methods described in Ref. 7 and 8 allow for the calculation of both the electronic and lattice components of
the spin (i.e., Zeeman) contribution to the magnetoelectric coupling. In principle at least, the lattice component
of the orbital contribution could be computed using the
methods of Ref. 54, while the remaining orbital electronic
contributions can be computed from the formulas derived
in Refs. 10 and 11 following the developments discussed
here. We thus expect that the computation of all of the
various contributions to the magnetoelectric coupling will
soon be accessible to modern density-functional methods.

∗

181–194.
G. A. Smolenski and I. E. Chupis, Sov. Phys. Usp. 25, 475
(1982).
7
J. Íñiguez, Phys. Rev. Lett. 101, 117201 (2008).
8
K. T. Delaney, E. Bousquet,
and N. A. Spaldin,
arXiv:0912.1335 (2009).
9
J. Wojdel and J. Íñiguez, Phys. Rev. Lett. 103, 267205
(2009).
10
A. M. Essin, A. M. Turner, J. E. Moore, and D. Vanderbilt, Phys. Rev. B 81, 205104 (2010).

sinisa@physics.rutgers.edu
M. Fiebig, J. Phys. D: Appl. Phys. 38, R123 (2005).
2
W. Eerenstein, N. D. Mathur, and J. F. Scott, Nature
442, 759 (2006).
3
M. Fiebig and N. A. Spaldin, Eur. Phys. J. B 71, 293
(2009).
4
J.-P. Rivera, Eur. Phys. J. B 71, 299 (2009).
5
V. E. Wood and A. E. Austin, in Magnetoelectric Interaction Phenomena in Crystals, edited by A. J. Freeman
and H. Schmid (Gordon and Breach, London, 1975) pp.
1

ACKNOWLEDGMENTS

We would like to acknowledge useful discussions with
J. R. Yates and Y. Mokrousov. The work was supported by NSF Grants DMR-0549198, DMR-0706493,
and DMR-1005838.

6

13
11

A. Malashevich, I. Souza, S. Coh, and D. Vanderbilt, New
J. Phys. 12, 053032 (2010).
12
X. Qi, T. L. Hughes, and S.-C. Zhang, Phys. Rev. B 78,
195424 (2008).
13
A. M. Essin, J. E. Moore, and D. Vanderbilt, Phys. Rev.
Lett. 102, 146805 (2009).
14
L. Fu and C. L. Kane, Phys. Rev. B 76, 045302 (2007).
15
D. Hsieh, D. Qian, L. Wray, Y. Xia, Y. S. Hor, R. J. Cava,
and M. Z. Hasan, Nature 452, 970 (2008).
16
D. Hsieh, Y. Xia, D. Qian, L. Wray, F. Meier, J. H. Dil,
J. Osterwalder, L. Patthey, A. V. Fedorov, H. Lin, A. Bansil, D. Grauer, Y. S. Hor, R. J. Cava, and M. Z. Hasan,
Phys. Rev. Lett. 103, 146401 (2009).
17
Y. Xia, D. Qian, D. Hsieh, L. Wray, A. Pal, H. Lin, A. Bansil, D. Grauer, Y. S. Hor, R. J. Cava, and M. Z. Hasan,
Nat. Phys. 5, 398 (2008).
18
Hehl, F. W., Obukhov, Y. N., Rivera, J.-P., and Schmid,
H., Eur. Phys. J. B 71, 321 (2009).
19
J.-P. Rivera, Ferroelectrics 161, 165 (1994).
20
R. D. King-Smith and D. Vanderbilt, Phys. Rev. B 47,
1651 (1993).
21
D. Vanderbilt and R. D. King-Smith, Phys. Rev. B 48,
4442 (1993).
22
S. Coh and D. Vanderbilt, Phys. Rev. Lett. 102, 107603
(2009).
23
Here we refer to a multiband gauge transformation having
the form of Eq. (18), since α can be shown to be fully
invariant under a single-band phase twist.
24
F. D. M. Haldane, Phys. Rev. Lett. 93, 206602 (2004).
25
F. D. M. Haldane, Phys. Rev. Lett. 61, 2015 (1988).
26
M. Z. Hasan and C. L. Kane, arXiv:1002.3895 (2010).
27
H. Wiegelmann, A. G. M. Jansen, P. Wyder, J. P. Rivera,
and H. Schmid, Ferroelectrics 162, 141 (1994).
28
E.
Kita,
K.
Siratori,
and
A.
Tasaki,
J. Appl. Phys. 50, 7748 (1979).
29
A. P. Cracknell, Magnetism in crystalline materials (Pergamon press, Oxford, 1975).
30
X. Wang, J. R. Yates, I. Souza, and D. Vanderbilt,
Phys. Rev. B 74, 195118 (2006).
31
X. Wang, D. Vanderbilt, J. R. Yates, and I. Souza, Phys.
Rev. B 76, 195109 (2007).
32
N. Marzari and D. Vanderbilt, Phys. Rev. B 56, 12847
(1997).
33
Even though Eqs. (27) and (31) are equivalent, the first
(second) term in Eq. (27) is not equal to the first (second)
term in Eq. (31).
34
P. Giannozzi, S. Baroni, N. Bonini, M. Calandra, R. Car, C. Cavazzoni, D. Ceresoli, G. L.

Chiarotti, M. Cococcioni, I. Dabo, A. Dal Corso,
S. de Gironcoli, S. Fabris, G. Fratesi, R. Gebauer,
U. Gerstmann, C. Gougoussis, A. Kokalj, M. Lazzeri,
L. Martin-Samos, N. Marzari, F. Mauri, R. Mazzarello,
S. Paolini, A. Pasquarello, L. Paulatto, C. Sbraccia, S. Scandolo, G. Sclauzero, A. P. Seitsonen,
A. Smogunov, P. Umari,
and R. M. Wentzcovitch,
J. Phys.: Condens. Matter 21, 395502 (19pp) (2009).
35
A.
A.
Mostofi,
J.
R.
Yates,
Y.-S.
Lee,
I. Souza,
D. Vanderbilt,
and N. Marzari,
Comput. Phys. Commun. 178, 685 (2008).
36
C. Hartwigsen, S. Goedecker,
and J. Hutter,
Phys. Rev. B 58, 3641 (1998).
37
J.
P.
Perdew
and
Y.
Wang,
Phys. Rev. B 45, 13244 (1992).
38
H.
J.
Monkhorst
and
J.
D.
Pack,
Phys. Rev. B 13, 5188 (1976).
39
N. J. Mosey and E. A. Carter, Phys. Rev. B 76, 155123
(2007).
40
S. Shi, A. L. Wysocki, and K. D. Belashchenko, Phys.
Rev. B 79, 104404 (2009).
41
Throughout the paper, the notation for magnetic point
groups follows Ref. 29.
42
H. Zhang, C.-X. Liu, X.-L. Qi, X. Dai, Z. Fang, and S.-C.
Zhang, Nat. Phys. 5, 438 (2008).
43
L. Fu and C. L. Kane, Phys. Rev. B 74, 195312 (2006).
44
R. Roy, Phys. Rev. B 79, 195321 (2009).
45
A. A. Soluyanov and D. Vanderbilt, arXiv:1009.141
(2010).
46
R. Li, J. Wang, X.-L. Qi, and S.-C. Zhang, Nat. Phys. 6,
284 (2010).
47
This is done by adding to the Kohn-ShamPenergy functional an energy penalty term of the form λ i (µi − µ̄i )2 ,
where µi is the actual value of the magnetic moment of
the i-th atom in the unit cell while µ̄i and λ are adjustable
parameters. The moments µi are calculated by integrating
the spin density within atom-centered spheres.
48
M.
Stengel
and
N.
A.
Spaldin,
Phys. Rev. B 73, 075121 (2006).
49
L. Fu,
C. L. Kane,
and E. J. Mele,
Phys. Rev. Lett. 98, 106803 (2007).
50
J.
E.
Moore
and
L.
Balents,
Phys. Rev. B 75, 121306 (2007).
51
R. Roy, Phys. Rev. B 79, 195322 (2009).
52
G. Vignale and M. Rasolt, Phys. Rev. B 37, 10685 (1988).
53
G. Vignale, Phys. Rev. B 70, 201102 (2004).
54
D. Ceresoli, T. Thonhauser, D. Vanderbilt, and R. Resta,
Phys. Rev. B 74, 024408 (2006).


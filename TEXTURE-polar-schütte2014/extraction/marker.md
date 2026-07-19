<!-- extracted via pdftotext | arxiv:1405.1568 | 2026-07-19T04:40:35Z -->
Magnon-skyrmion scattering in chiral magnets
Christoph Schütte and Markus Garst

arXiv:1405.1568v3 [cond-mat.str-el] 24 Sep 2014

Institut für Theoretische Physik, Universität zu Köln, Zülpicher Str. 77, 50937 Köln, Germany
(Dated: September 25, 2014)
Chiral magnets support topological skyrmion textures due to the Dzyaloshinskii-Moriya spinorbit interaction. In the presence of a sufficiently large applied magnetic field, such skyrmions
are large amplitude excitations of the field-polarized magnetic state. We investigate analytically
the interaction between such a skyrmion excitation and its small amplitude fluctuations, i.e., the
magnons in a clean two-dimensional chiral magnet. The magnon spectrum is found to include two
magnon-skyrmion bound states corresponding to a breathing mode and, for intermediate fields, a
quadrupolar mode, which will give rise to subgap magnetic and electric resonances. Due to the
skyrmion topology, the magnons scatter from an Aharonov-Bohm flux density that leads to skew
and rainbow scattering, characterized by an asymmetric differential cross section with, in general,
multiple peaks. As a consequence of the skew scattering, a finite density of skyrmions will generate
a topological magnon Hall effect. Using the conservation law for the energy-momentum tensor,
we demonstrate that the magnons also transfer momentum to the skyrmion. As a consequence,
a magnon current leads to magnon pressure reflected in a momentum-transfer force in the Thiele
equation of motion for the skyrmion. This force is reactive and governed by the scattering cross
sections of the skyrmion; it causes not only a finite skyrmion velocity but also a large skyrmion Hall
effect. Our results provide, in particular, the basis for a theory of skyrmion caloritronics for a dilute
skyrmion gas in clean insulating chiral magnets.
PACS numbers: 75.78.-n, 75.70.Kw, 75.30.Ds, 75.76.+j

I.

INTRODUCTION

The discovery of a magnetic skyrmion lattice in the
cubic chiral magnets by Mühlbauer et al.1 has triggered
a flurry of interest in magnetic skyrmion textures. These
magnets inherit the chirality from their B20 chiral atomic
crystal structure allowing for a spin-orbit DzyaloshinskiiMoriya interaction, that energetically stabilizes twisted
modulated magnetic textures like helices and skyrmions,
see Fig. 1. The possibility of magnetic skyrmion textures in the B20 compounds has been envisioned in early
seminal work by Bogdanov and collaborators.2–4 They
encompass a variety of materials with different electronic characteristics, for example, the metals MnSi1,5
and FeGe,6 the semiconductor Fe1−x Cox Si,7,8 and the insulator Cu2 OSeO3 ,9,10 that nevertheless share the same
magnetic properties and possess similar magnetic phase
diagrams.
The excitement aroused by skyrmions is attributed
to their topological properties. They are characterized by a finite topological winding number that is,
e.g., at the origin of a topological Hall effect,11,12 a
skyrmion-flow Hall effect,13 and a concomitant emergent
electrodynamics14,15 in the metallic B20 compounds.
Moreover, their topological origin also results in a finite gyrocoupling vector in the Thiele equation,16 that
describes their magnetization dynamics, and, as a consequence, the skyrmion motion is governed by a strong
spin-Magnus force.17–20 This peculiar dynamics combined with the smoothness of the skyrmion texture allows
for spin-transfer torque phenomena at ultralow threshold
currents,18,21–24 which makes magnetic skyrmion matter interesting for spintronic applications;25 see Ref. 26
for a recent review.
In insulating chiral magnets,

FIG. 1: Skyrmion texture of a chiral magnet.

skyrmions are also associated with interesting thermal
spin-transport effects. A thermal gradient is predicted
to induce a skyrmion motion that, counterintuitively, is
towards the heat source together with a skyrmion Hall
effect.27–29 Moreover, a thermal skyrmion ratchet has
been realized with the help of the topological magnon
Hall effect that arises due to magnon skew scattering off
skyrmions in the material.30
A prerequisite for a better understanding of such phenomena, however, is a detailed analysis of the magnonskyrmion interaction. For the skyrmion lattice, it is
known that apart from the long-wavelength spin-wave
excitations31,32 there are three magnetic resonances with
finite excitation frequencies, a single breathing mode
and two gyration modes.33–35 A natural question arises
whether a similar mode spectrum exists for a single magnetic skyrmion within a spin-polarized background. A
first numerical study of the magnon-skyrmion bound

2
states has been recently carried out by Lin et al..37 On
the other hand, the scattering of magnons from a single
skyrmion has been investigated with the help of micromagnetic simulations by Iwasaki et al..38 A characteristic skew scattering was found which was attributed to an
emergent Lorentz force that is generated by the skyrmion
topology. Moreover, the simulations revealed that the
skyrmion experiences a magnon pressure pushing it towards the magnon source, which was explained in terms
of momentum conservation.38
In the present work, we investigate the magnon fluctuations in the presence of a skyrmion texture analytically. Starting from the non-linear sigma model description of a two-dimensional chiral magnetic system, we derive in Sec. II the magnon Hamiltonian by expanding
around the skyrmionic saddle point solution. The spectrum of the magnon-skyrmion bound states is obtained,
and the magnon-skyrmion scattering cross section is analyzed in Sec. III. A theory for the magnon pressure, i.e.,
the momentum-transfer force exerted on the skyrmion by
a magnon current, is presented in Sec. IV, which in particular explains previous numerical work. We conclude
with a summary and discussion of the results in Sec. V.

II. THEORY FOR MAGNON-SKYRMION
SCATTERING IN A CHIRAL MAGNET
A.

Action of a two-dimensional chiral magnet

Our starting point is the standard model of cubic chiral magnets.39,40 We limit ourselves however to an effective two-dimensional magnetic system thus restricting
the spatial coordinate r to a plane. The orientation of
~ (r) = M n̂(r) is parametrised by a
the magnetisation M
unit vector n̂ that is governed by the Euclidean action of
the following non-linear sigma model

stiffness energy
ε0
Dzyaloshinskii-Moriya momentum
Q
~/a2
spin density
skyrmion radius
1/κ
Dzyaloshinskii-Moriya energy
εDM = ε0 a2 Q2
εgap = ε0 a2 κ2
magnon gap energy
Mmag = ~2 /(2ε0 a2 )
magnon mass
TABLE I: Parameters used throughout this work. The value
of κ can be tuned by the strength of the applied magnetic
field.

neglected because they are assumed to be weak and of
only minor importance for the problem investigated here.
We also neglect for simplicity dipolar interactions, which
are known to give rise to quantitative and qualitative
corrections though, e.g., for the magnetic resonances.35
The dynamic part is given by the Berry phase36
~
Ldyn = − 2 ~
A(n̂)idτ n̂
a

where a is a typical distance between the magnetic moments and τ = it is the imaginary time. The gauge
~ j /∂ n̂i = n̂k , and the Euler-Lagrange
field satisfies ijk ∂ A
equations of the action Eq. (1) reproduce the standard
Landau-Lifshitz equations for the magnetisation. Note
that we have chosen the sign of (3) such that the magnetization vector, n̂, is antiparallel to the spin vector as it is
the case for the magnetic moments of electrons. We neglect throughout this work additional degrees of freedom
that might give rise to dissipation usually represented by
a phenomenological Gilbert damping.

1.

Z β
S=

Z
dτ

d2 r L

with

L = Ldyn + Lstat

(1)

0

where β = 1/(kB T ) is the inverse temperature. The
Lagrangian consists of two parts. The static part reads
i
ε0 h
Lstat =
(dα n̂i )2 + 2Qiαj n̂i dα n̂j − 2κ2 n̂B̂
(2)
2
where here and in the following we use greek indices
for two-dimensional real-space vectors, α = 1, 2 with
d
e.g. d1 = dx
, and latin indices for the magnetisation vector, i, j, k = 1, 2, 3. ikj is the totally antisymmetric tensor with 123 = 1. The spin-orbit Dzyaloshinskii-Moriya
interaction is proportional to Q > 0 that we choose to be
positive representing a right-handed chiral magnetic system. ε0 is the energy scale associated with the stiffness
and κ > 0 measures the strength of the magnetic field.
We will consider here only the situation when the magnetic field is orthogonal to the two-dimensional plane,
B̂ = ẑ. In the following, cubic anisotropies39,40 will be

(3)

Length scales and parameters

The model (1) possesses three in general different
length scales: a, 1/κ and 1/Q. We are interested here
in the parameter regime where a single skyrmion is a
topologically stable excitation of the magnetic system
which is the case for intermediate values of the magnetic
field, κ ∼ Q. Whereas for small κ  Q the magnetic
system becomes unstable with respect to a proliferation
of skyrmions, for very large values κ  Q the energy
density in the core of a skyrmion is very high so that
amplitude fluctuations of the magnetisation become important eventually destroying the skyrmion.41 As we will
see below, 1/κ can be identified with the skyrmion radius. Moreover, we consider the limit of small spin-orbit
coupling implying Qa  1 to be a small parameter. This
implies, in particular, that a single skyrmion is composed
of many individual spins.
The magnon excitations of the field-polarised ground
state are characterised by a gap and a mass that are given
for later convenience in Table III.

3
10

spin vector indices i, j, k = 1, 2, 3
spatial indices
α, β, γ = 1, 2
space-time indices µ, ν, λ = 0, 1, 2

0
1

TABLE II: Indices used e.g. in the discussion of conserved
currents. For the time derivative we also use the notation
d0 = dt = idτ .

0.8

-10

0.6

0.4
0.2

-20

2.

We now turn to the discussion of the conserved currents associated with the Lagrangian (1). In the following, it will be convenient to use 2+1 dimensional spacetime vectors, for which we use the indices µ, ν, λ = 0, 1, 2
with the time-derivative d0 = idτ . However, we still reserve the indices α, β = 1, 2 for spatial vectors only, see
Table II.
The order parameter n̂ is an element of the twodimensional sphere S 2 . Its second homotopy group is
the group of integer numbers π2 (S 2 ) = Z, and, as a result, the order parameter allows for topological textures
in two spatial dimension. The associated 2+1 topological
current vector reads
jµtop =

1
µνλ n̂(dν n̂ × dλ n̂),
8π

(4)

where 012 = 1. In case the field configuration n̂ is nonsingular, i.e., in the absence of hedgehog defects in 2+1
space-time, this current is conserved
dµ jµtop = 0,

j0top =

1
n̂ (d1 n̂ × d2 n̂).
4π

(6)

The spatial integral over the charge density is quantised
d2 rj0top ≡ W ∈ Z,

(7)

and identifies the winding number W of the texture. In
this paper, we focus on the (baby-)skyrmion texture with
W = −1. For later convenience we note that the topological current can be expressed in terms of the spin-gauge
field of Eq. (3) as follows
jµtop =

1
~ λ n̂.
µνλ (dν A)d
4π

-30
0

(8)

There are also important Noether currents of the Lagrangian L related to momentum and angular momentum conservation that are discussed in detail in appendix
A.

0.4

0.8

0

1.2

1

2

3

4

1.6

5

2

FIG. 2: Energy dependence of the single skyrmion solution
as a function of the dimensionless parameter κ2 /Q2 . The
energy of the skyrmion is positive for κ2 > κ2cr ≈ 0.8Q2 . The
negative skyrmion energy for smaller κ signals an instability
of the magnetic systems towards a proliferation of skyrmions.
Inset shows two skyrmion profiles θ(ρ) for values of κ2 /Q2
marked as dots in the main panel.

B.

Saddle point solution of the magnetic skyrmion

For sufficiently large magnetic fields and, thus, large
values of κ, the action (1) is minimised by the fully polarised state n̂ = ẑ. A large amplitude excitation of this
state is the magnetic skyrmion texture with a winding
number W = −1, see Eq. (7). The skyrmion profile is
parameterised by n̂Ts = (sin θ cos ϕ, sin θ sin ϕ, cos θ) with
ϕ = χ + π/2,

(5)

as n̂ is a unit vector and n̂ dν n̂ = 0. The topological
charge density reads explicitly

Z

0

Topological charge

and θ = θ(ρ),

(9)

in terms of polar coordinates, ρ and χ, of
the
two-dimensional
spatial
distance
vector
δr T = (ρ cos χ, ρ sin χ). The Euler-Lagrange equation deriving from Eq. (2) yields the differential equation
obeyed by the function θ(ρ),2,3
θ00 +

θ0
sin θ cos θ 2Q sin2 θ
−
+
− κ2 sin θ = 0
ρ
ρ2
ρ

(10)

with the boundary conditions θ(0) = π and
limρ→∞ θ(ρ) = 0. Its solution possesses the asymptotics
(
π − c1 κρ for ρ → 0
(11)
θ(ρ) ≈
√c2 e−κρ for ρ → ∞
κρ
with positive coefficients c1 and c2 , that however depend
on the ratio κ/Q. The exponential decay for large distances identifies 1/κ as the skyrmion radius.
The boundary value problem (10) is easily numerically
solved with the help of the shooting method.42 Here, the
constant value c1 of the short-distance asymptotics (11)
is varied until one obtains a monotonous function θ(ρ)
with the required exponentially decaying behaviour at
large distances. Examples of the numerically obtained

4
profiles are shown in the inset of Fig. 2. The resulting
skyrmion texture is illustrated in Fig. 1.
Integrating the static skyrmion solution one obtains for
(0)
its saddle-point action Ss = β(εs + εFP ) where εFP =
2
−ε0 κ V is the energy of the field-polarized state, n̂FP ≡
ẑ, with the volume V and εs = ε0 E(κ2 /Q2 ) identifies the
energy of the skyrmion. The dimensionless function E is
shown in Fig. 2. The energy of the skyrmion is positive
as long as κ > κcr where
κ2cr ≈ 0.8Q2 .

(12)

For values smaller than the critical value κcr the magnetic system becomes unstable towards a proliferation of
skyrmions and, eventually, the formation of a skyrmion
lattice. In the following, we concentrate on the regime
with positive skyrmion energy, κ > κcr , where the
skyrmion is a large amplitude excitation of the fieldpolarised phase with a positive excitation energy.
C.

Effective theory for magnon excitations in the
presence of a skyrmion

The orthogonal frame êi depends on the radius ρ and the
angle χ that are here associated with the distance vector
δr T = (r − R)T = (ρ cos χ, ρ sin χ).
It is clear that this parameterization is invariant under
the local transformation
ê+ → ê+ e−iλ ,
iλ

ê− → ê− e ,

ψ → ψeiλ

(16)

∗

(17)

∗ −iλ

ψ →ψ e

with λ = λ(r − R(τ ), τ ). In the limit of large distances
from the skyrmion, |r−R(τ )| → ∞, the parameterisation
assumes the form
p
n̂(r, τ ) ≈ ẑ 1 − 2|ψ(r − R(τ ), τ )|2
h
i
1
+ √ (x̂ + iŷ) − ie−iϕ ψ(r − R(τ ), τ )
(18)
2
h
i
1
+ √ (x̂ − iŷ) ieiϕ ψ ∗ (r − R(τ ), τ )
2
The last two lines allow to identify the magnon wave function with respect to an orthogonal frame that becomes
the laboratory frame, x̂, ŷ and ẑ, at large distances,
ψLAB (r − R(τ ), τ ) = −ie−iϕ ψ(r − R(τ ), τ ).

We now consider spin-wave fluctuations, i.e., the
magnon modes in the presence of a single skyrmion in
a chiral magnet. A similar analysis for magnetic solitons and vortices in ferromagnets has been carried out
previously.43–46 For the parameterisation of the magnons
we introduce the local orthogonal frame êi (r)êj (r) = δij
with i, j = 1, 2, 3 and ê1 (r) × ê2 (r) = ê3 (r) where
ê3 (r) = n̂s (r) follows the static skyrmion profile. We
will use the following representation in terms of polar
and azimuthal angle, θ and ϕ, respectively, introduced
above
êT1 (r) = (− sin ϕ, cos ϕ, 0)
êT2 (r) = (− cos θ cos ϕ, − cos θ sin ϕ, sin θ)

(13)

êT3 (r) = (sin θ cos ϕ, sin θ sin ϕ, cos θ),
where ϕ = χ + π/2 and θ = θ(ρ). Furthermore, it is
convenient to introduce the chiral vectors
1
(14)
ê± = √ (ê1 ± iê2 )
2
that have the property ê+ ê+ = ê− ê− = 0 and ê+ ê− =
ê− ê+ = 1.
Due to translation invariance, the energy of the
skyrmion is independent of its position giving rise to
two zero modes associated with translations of the
skyrmion.47 In order to treat these zero modes we introduce two time-dependent collective coordinates RT (τ ) =
(Rx (τ ), Ry (τ )).
The remaining massive fluctuation
modes are represented by the dimensionless complex field
ψ(r, τ ). We use the parameterization
p
n̂(r, τ ) = ê3 (r − R(τ )) 1 − 2|ψ(r − R(τ ), τ )|2
+ ê+ (r − R(τ ))ψ(r − R(τ ), τ )
(15)
∗
+ ê− (r − R(τ ))ψ (r − R(τ ), τ ).

(19)

This will become important later for the discussion of
magnon scattering off the skyrmion.
Expanding the action (1) in the massive field ψ allows
us to study their properties and their influence on the
skyrmion.
1.

Zeroth order in the massive fluctuation field ψ

In zeroth order inR the fluctuation field ψ the Lagrangian is given by d2 rL(0) = εFP + εs + L(0) with
L(0) = −A(R)idτ R.

(20)

This term originates from the expansion of the dynamical
part of the action (3) and has the form of a massless
particle with coordinate R in the presence of a gauge
field A given by
Z
~
~ 3 (r − R))∂α ê3 (r − R). (21)
Aα (R) = − 2
d2 r A(ê
a
The electric field associated with this vector potential
vanishes as ∂τ Aα (R) = 0. The effective magnetic field
however is finite and determined by the skyrmion number
∂
Beff ≡ zαβ
Aβ (R)
∂Rα
Z
~
4π~
= 2
d2 r n̂s (∂1 n̂s × ∂2 n̂s ) = − 2 .
a
a

(22)

Note that in zeroth order in the magnon field ψ, the
gauge field (21) just coincides with the total canonical
momentum58
Z
∂L(0)
−
= Aα (R) = d2 r T0α
,
(23)
∂(idτ Rα )
ψ,ψ ∗ =0

5
where the energy-momentum tensor, Tµν , is defined in
Eq. (A4). The classical equations of motion deriving from
Lagrangian (20) have the form of a massless particle in a
magnetic field,
G × dt R = 0,

(24)

with G = Beff ẑ. They are to be identified with the wellknown Thiele equations for magnetic textures in the absence of a Gilbert damping, and G is the so-called gyrocoupling vector.16 At zeroth order in ψ, these equations
of motion also coincide with Eq. (A7) following from momentum conservation implying that the integrated topological current vanishes.

By completing the square, the Hamiltonian can be also
written in the form
h
i
H = ε0 a2 (−i∇ − τ z~a)2 + 1(V0 − ~a2 ) + τ x Vx , (30)
with the gauge field

~a =


cos θ
− Q sin θ χ̂.
ρ

Note that ~a assumes here the Coulomb gauge ∇~a = 0.
~ and the
The interaction between the magnon field ψ
zero mode is given by
(2)

Lint = −
2.

Second order in the massive fluctuations ψ

Expanding the Lagrangian density in second order in the
fluctuation field ψ one finds after some algebra
1 ~† z
~†H ψ
~ + L(2)
~+ 1 ψ
ψ τ ~∂τ ψ
int
2
2a
2a2

(26)

where τ z is a Pauli matrix and we used that the field
ψ = ψ(r − R(τ ), τ ) possesses an explicit and implicit
time-dependence, dτ ψ = ∂τ ψ − (∂γ ψ)dτ Rγ . The bosonic
Bogoliubov-deGennes Hamiltonian reads
H=
(27)


h
i
cos θ
sin θ
ε0 a2 − 1∇2 + 2τ z
−Q
i∂χ + 1V0 + τ x Vx .
2
ρ
ρ
The potentials are given by
1
1 + 3 cos(2θ) 3Q sin(2θ)
−
+ κ2 cos θ − Qθ0 − θ02
2
4ρ
2ρ
2
sin2 (θ) Q sin(2θ)
1
Vx =
+
− Qθ0 − θ02 ,
(28)
2ρ2
2ρ
2
V0 =

and only depend on the distance ρ to the skyrmion center
as θ = θ(ρ). Here, ∇2 is the two-dimensional Laplace
operator which reads in polar coordinates ∇2 = ∂ρ2 +
(1/ρ)∂ρ + ∂χ2 /ρ2 . For later reference, we note that the
derivative in polar coordinates is given by ∂α = ρ̂α ∂ρ +
∂
χ̂α ρχ with the unit vectors
ρ̂T = (cos χ, sin χ),

χ̂T = (− sin χ, cos χ).

~ ~† γ ~
ψ Γ ψ idτ Rγ .
2a2

(32)

The interaction vertex reads

We now turn to the magnon spectrum and its interaction with the skyrmion. The scattering of magnons
from the skyrmion does not conserve the magnon number, which is reflected in the presence of local, anomalous
quadratic terms ψψ and ψ ∗ ψ ∗ in the Hamiltonian. It is
therefore convenient to use the spinor notation
!
ψ
~
~ † = (ψ ∗ , ψ).
ψ=
,
ψ
(25)
ψ∗

L(2) =

(31)

(29)

Γγ = −τ z i∂γ − 1

cos θ
χ̂γ .
ρ

(33)

Whereas the first term just combines with the dynamic
part of the Lagrangian (26) to a total time derivative, the
second term derives from a spin connection attributed to
the local orthogonal frame (13).
If the skyrmion velocity vanishes, idτ R = 0, the Lagrangian reduces to the first two terms in Eq. (26). These
terms constitute a Bogoliubov-deGennes scattering problem and determine the spectrum of the magnons in the
presence of a skyrmion with idτ R = 0. It is important
to note that these terms and thus the spectrum do not
depend on the position of the skyrmion R itself as the
collective coordinate R can be eliminated by a change of
the integration variable r − R → r (Ref. 48).
III.

MAGNON SPECTRUM AND SKYRMION
SCATTERING CROSS SECTION

In the following we investigate the properties of the
magnons by analysing the eigenvalues and eigenstates
of the Hamiltonian (27). It requires the solution of a
Bogoliubov-deGennes scattering problem, which then allows us to determine the magnon-skyrmion bound states
and to address the magnon scattering cross section for
the case of a vanishing skyrmion velocity, idτ R = 0.
A.

Bogoliubov-deGennes scattering problem

The magnons are obtained as eigenstates of the eigenvalue problem
~ = ετ z ψ,
~
Hψ

(34)

with the Hamiltonian H given in Eq. (27). The Hamiltonian possesses the following particle-hole symmetry
τ x KHτ x K = H

(35)

6
4

where K is complex conjugation, which originates in the
fact that the magnetisation is a real quantity. As a consequence, the spectrum of H is characterized by pairs ±ε
~ is an eigenvector with
of eigenvalues. In particular, if ψ
x
~
eigenvalue ε then τ K ψ is an eigenvector with eigenvalue
−ε.
~ = eimχ ~ηm (ρ) with the angular momentum
Setting ψ
quantum number m and using H = H(−i∂χ ) the eigenvalue equation reduces to
H(m)~ηm = ετ z ~ηm .

0

Stability of the theory (26) then requires the energy to be
positive ε ≥ 0. The eigenvectors with negative eigenenergies, −ε ≤ 0, are then given by τ x Keimχ ~ηm = e−imχ ζ~−m
∗
where ζ~−m = τ x ~ηm
and

1.

2
1
0
-1

(36)

The spectrum of H contains discrete bound states labeled by the quantum number n and eigenfunctions ~ηm,n
as well as scattering states labeled by the energy ε and
eigenfunctions ~ηm,ε . These eigenfunctions will be normalized such that
Z ∞
†
dρρ ~ηm,n
τ z ~ηm,n0 = δn,n0 ,
(37)
0
Z ∞
†
dρρ ~ηm,ε
τ z ~ηm,ε0 = δ(ε − ε0 ).
(38)

H(−m)ζ~−m = −ετ z ζ~−m .

3

0

1

2

The skyrmion profile decays exponentially and its scattering potential is thus well localised. We recast the
Hamiltonian in terms of a scattering problem H(m) =
H0m + Vm . Here H0m describes the magnons in the absence of the skyrmion

i
h 
m2 + 1
∂ρ
2
z 2m
2
2
+
+
κ
−
τ
,
H0m =ε0 a 1 −∂ρ −
ρ
ρ2
ρ2
(40)
and the skyrmion matrix scattering potential Vm =
Vm (ρ) is given by
h
i
Vm (ρ) = ε0 a2 vz (ρ)τ z + v0 (ρ)1 + vx (ρ)τ x
(41)
with

cos θ − 1 Q sin θ
,
−
ρ2
ρ
3(cos(2θ) − 1) 3Q sin(2θ)
v0 (ρ) =
−
+ κ2 (cos θ − 1)
4ρ2
2ρ
θ02
− Qθ0 −
,
(42)
2
sin2 (θ) Q sin(2θ)
θ02
0
vx (ρ) =
+
−
Qθ
−
.
2ρ2
2ρ
2

4

FIG. 3: The potentials v0 , vx and vz of Eqs. (42) in units of
εgap plotted as functions of the dimensionless parameter κρ
for a value of κ = Q. All three potentials vanish exponentially
for κρ  1.

The potential Vm vanishes exponentially for κρ  1 as illustrated in Fig. 3. The anomalous potential vx that couples the two components of the wave function ~η vanishes
quadratically for κρ → 0 and exponentially for κρ → ∞.
(0)
(0)
Solutions of the free problem H0m ~ηm = ετ z ~ηm only
exist for energies
ε = ε0 a2 (κ2 + k 2 ) ≡ εgap +

(39)

Definition of the skyrmion scattering problem

3

~2 k 2
2Mmag

(43)

with the radial momentum k ≥ 0. This identifies
the magnon gap εgap = ε0 a2 κ2 and the magnon mass
~2 /(2Mmag ) = ε0 a2 , see Table III. The eigenfunctions
are given by
!
1
1
(0)
√
~ηm,ε
=
Jm−1 (kρ).
(44)
0
2ε0 a2
where Jν are Bessel functions of the first kind. They are
normalized such that
Z ∞
(0)† z (0)
dρρ ~ηm,ε
τ ~ηm,ε0
(45)
0
Z ∞
1
=
dρρJm−1 (kρ)Jm−1 (k 0 ρ) = δ(ε − ε0 )
2ε0 a2 0
where we used the completeness relation of the Bessel
functions
Z ∞
δ(k − k 0 ) = k
dρρJν (kρ)Jν (k 0 ρ).
(46)
0



vz (ρ) = −2m

2.

Asymptotics of eigenfunctions and scattering phase shifts

For small distances ρκ  1, the Hamiltonian reduces
to

i
h 
∂ρ
m2 + 1
2
zm
+
+
2τ
(47)
H(m) ≈ ε0 a 1 −∂ρ −
ρ
ρ2
ρ2
2

7
where we have omitted all terms of order O(1/(κρ)).
Note that the presence of the skyrmion inverts the sign
of the linear m-term for κρ  1 as compared to the free
Hamiltonian (40). From Eq. (47) follows the asymptotics
of the eigenfunction at small distances
!
c3 (κρ)|m+1|
for κρ  1,
(48)
~ηm ≈
c4 (κρ)|m−1|
with constant coefficients c3 and c4 .
The large distance asymptotics is governed by the free
Hamiltonian (40) and depends on the energy ε. For energies below the magnon gap ε < εgap the wave function
decays exponentially in κρ. For energies ε = εgap +ε0 a2 k 2
with k ≥ 0, the large distance asymptotics, κρ  1, is
given by
~ηm ≈
(49)
!
1
1
√
(cos(δm )Jm−1 (kρ) − sin(δm )Ym−1 (kρ)) ,
0
2ε0 a2
where Yν are the Bessel functions of the second kind, and
we introduced the phase shift δm . The second component
is exponentially small and has been set to zero.

B.

1
0.8

Magnon
continuum

0.6
0.4
0.2
0

0.5

0.6

0.7

0.8

0.9

1

1.1

FIG. 4: Energy spectrum of magnons in the presence of
a single skyrmion excitation of the field-polarised ground
state. The latter becomes thermodynamically unstable for
κ2 < κ2cr ≈ 0.8Q2 (dashed-dotted vertical line), see Eq. (12).
In addition to the continuous magnon spectrum for ε > εgap =
εDM κ2 /Q2 , one obtains in-gap bound states for smaller energies. The dashed vertical line signals the local bimeron instability identified by the vanishing of the quadrupolar eigenfrequency, see text. The images show snapshots of the corresponding excitation modes, see also Fig. 5.

Magnon-skyrmion bound states

In the following we discuss the magnon bound states
to be found within the energy range 0 ≤ ε < εgap .
1.

Cross-check: zero modes

Before turning to a discussion of the bound states,
however, we first perform an important cross-check. Although we are only interested here in the massive modes
with finite energy, the spectrum of the Hamiltonian must
also possess the zero modes corresponding to infinitesimal translations of the skyrmion, i.e., ê3 (r − R(τ )) ≈
ê3 (r) − ∂γ ê3 (r)Rγ (τ ). With the help of Eqs. (13) we
find
∂γ ê3 = −θ0 ρ̂γ ê2 +

sin θ
χ̂γ ê1 .
ρ

(50)

This allows to identify a zero mode with angular momentum m = −1,
1  sinρ θ − θ0 
zm
~η−1
=√
,
8 sinρ θ + θ0

(51)

normalized according to Eq. (37), and the corresponding
zm ∗
partner ζ~1zm = τ x (~η−1
) . Using the differential equation
(10) obeyed by θ(ρ) one can check explicitly that indeed
zm
H(−1)~η−1
= H(1)ζ~1zm = 0. Translations are then de~ zm = a ~η zm e−iχ +a∗ ζ~ zm eiχ
scribed by the wavefunction Ψ
−1
1

where the real and imaginary part of the coefficient a ∈ C
parametrize translations in y- and x-direction, respectively. Although there are two translational zero modes,
it should be kept in mind that they are represented by
a single zero mode in the spectrum obtained from the
eigenvalue equation (36) for the ~ηm wavefunctions.

2.

Massive magnon-skyrmion bound states

The massive bound states with finite energy are determined by solving the eigenvalue equation (36) numerically using again the shooting method.42 This is done by
first choosing a value for the ratio c3 /c4 in Eq. (48) as
well as the energy ε and afterwards checking whether the
numerically solution of the differential equation allows
for a bound state that is exponentially decaying at large
distances. This is iteratively repeated until a bound state
is found. The absolute value for c3 is afterwards fixed by
the normalization condition (37).
The resulting energy spectrum is shown in Fig. 4. In
the regime of a stable field-polarized state κ2 > κ2cr ≈
0.8Q2 , see Fig. 2, we find two bound states in addition to
the zero mode that is not shown. There exists a bound
breathing mode with m = 0 for all κ, and an additional
bound quadrupolar mode with m = −2 appears below
κ2 . 0.93Q2 . The eigenfrequency of this m = −2 mode
decreases with decreasing κ and eventually turns negative

8

1
0.5
0
-0.5
-1
0 1

5

10

15

FIG. 5: Time-dependence of the skyrmion profile for the
bound magnon modes with oscillation period T = ~/ε where
ε is the corresponding eigenenergy. The colour code reflects
the z-component of the local magnetisation. Corresponding
movies can be found in Ref. 50.

FIG. 6: Phase shifts of the scattering states for various angular momenta m for κ = Q; numerically exact values are
shown as solid lines, and the dashed lines are obtained within
the WKB approximation. For large angular momenta or high
energies the WKB approximation provides satisfying results.

for values of κ2 smaller than

distance in agreement with Eq. (49). In a second step,
the absolute value of, e.g., c3 is then fixed so that the
large distance asymptotics of the first component is consistent with Eq. (49), which ensures that the scattering
wave functions are normalised according to Eq. (38).
The energy dependence of the numerically obtained
phase shifts, δm , are shown for the lowest angular momenta as solid lines in Fig. 6 for κ = Q.

κ2bimeron ≈ 0.56Q2 .

(52)

This negative energy eigenvalue corresponds to a local
instability of the theory (26), and it translates to an instability of the single skyrmion with respect to a static
quadrupolar deformation. Such a deformed skyrmion can
also be identified as a bimeron, and this bimeron instability was previously pointed out by Ezawa.49 An additional
m = −3 mode materializes in the intermediate, thermodynamically metastable regime, κ2bimeron < κ2 < κ2cr , and
bound states with higher |m| do not exist in the locally
stable regime κ2 > κ2bimeron . Fig. 5 illustrates the spacetime dependence of the relevant bound magnon modes,
for movies see Ref. 50. All wave functions ~ηm (ρ) for the
bound states we have found numerically do not possess
any nodes, i.e., they do not have any zeros for some finite
value of ρ. We were not able to find bound states with a
single or more nodes.
The magnon spectrum of Fig. 4 agrees nicely with recent results of finite-size diagonalization of the LandauLifshitz-Gilbert equation by Lin et al..37 The only qualitative difference seems to be a hybridisation of the m = 0
and m = −2 mode close to their crossing at κ2 ≈ 0.875Q2
for the finite size system investigated in Ref. 37.

C.

Magnon scattering states

Magnon scattering states are obtained for energies
ε ≥ εgap . The corresponding wave functions are also obtained numerically with the help of the shooting method.
For a fixed energy ε one first finds a value for the ratio c3 /c4 of the small distance asymptotics, Eq. (48), so
that the numerical solution for the wave function ~ηm possesses a second component decaying exponentially with

1.

WKB approximation for the phase shift

For the discussion of the WKB approximation, we follow Langer51 , see also Ref. 52, and first substitute for
the radius ρ = ex /κ and ~u(x) = ~ηm (ex /κ) so that the
eigenvalue equation (36) simplifies for any x ∈ (−∞, ∞)
to
h
i
− ∂x2 − Λ(x) ~u(x) = 0,
(53)
where the matrix Λ is defined by
Λ(x) =
= −(m1 − τ z )2 − e2x (1 − τ z

(54)
ε
εgap

+

1
εgap

Vm (ex /κ)).

Eq. (53) has the form of a two-component Schrödinger
equation. The semiclassical approximation for such a
problem is discussed for example in Ref. 53. With the
help of the WKB Ansatz ~u(x) = ~u0 (x)eiS(x) and neglecting derivatives of ~u0 (x), the above differential equation
is converted into an algebraic one
h
i
(S 0 (x))2 1 − Λ(x) ~u0 (x) = 0.
(55)
This equation can be locally diagonalised for each position x. The interesting eigenvector is the one that becomes proportional to ~uT0 (x) ∝ (1, 0) for large distances.

9
5

5

4

Scattering cross section

4

3

3

2

2

1

1

0
-1
0

2.

2

4

6

8

0

0

2

4

6

8

FIG. 7: Effective WKB potential UWKB , Eq. (57), of the
magnon scattering states for various values of angular momentum m for κ = Q. In the classically allowed regimes, the
energy of the scattering states obeys ε > UWKB . In the left
panel, classical turning points, ρ0 , for the energy ε = 2εgap
are indicated by dots. For certain values of m the potential develops a local maximum giving rise to resonances that
are reflected in a pronounced energy dependence of the phase
shift.

The corresponding eigenvalue denoted as λ(x) then determines the function S 0 (x) with the help of which the
phase of the wave function can be evaluated in the lowest
order WKB approximation
p
Z ρ
Z x
p
λ(log(κρ0 ))
0
0
0
dρ
. (56)
S(x) =
dx λ(x ) =
ρ0
The evolution of the eigenvectors with x gives rise to
Berry phases that however contribute only in next-toleading order. The effective WKB potential
UWKB (ρ) = ε − εgap

λ(log(κρ))
,
ρ2 κ2

(57)

that is independent of the energy ε, is shown in Fig. 7 for
κ = Q. This potential possesses a single classical turning
point for angular momenta m ≤ −5 and m ≥ 2. For other
values of m, the potential develops a local maximum and
for certain energies three classical turning points then
appear. Neglecting corrections due to those additional
classical turning points, the scattering phase shift in the
WKB approximation is given by52
!
Z ρ̃ s
U
(ρ)
WKB
WKB
δm
= lim
k 2 + κ2 − κ2
− k dρ
ρ̃→∞ ρ
εgap
0
π
+ |m − 1| − kρ0 ,
(58)
2
p
where k = κ ε/εgap − 1. The distance ρ0 corresponds
here to the first classical turning point when approaching
the potential from large distances.
WKB
The results for δm
are shown in Fig. 6 as dashed
lines. It provides a good approximation to the numerically exact values (solid lines) for high energies and higher
angular momenta |m|. The sharp resonances for m = −3
and m = −4 are attributed to quasi bound states of the
effective potential (57).

The scattering amplitude f is defined in terms of the
long-distance asymptotic behaviour of the magnon wave
function but in the laboratory orthogonal frame as defined in Eq. (19),
!

eikρ 
1
scatter
~
ψLAB (r − R) =
eik(r−R) + f (χ) √
(59)
ρ
0
where (r − R)T = ρ(cos χ, sin χ). Comparison with
Eq. (49) yields for the scattering amplitude f
π
∞

e−i 4 X imχ i2δm+1
f (χ) = √
e
e
−1 ,
2πk m=−∞

(60)

p
with the momentum k = κ ε/εgap − 1. Note that the
phase shift δm+1 as defined in the local orthogonal frame
(49) enters the sum with the angular momentum m + 1.
The differential scattering cross section is then given by
dσ(ε)
= |f (χ)|2 .
dχ

(61)

The total scattering cross section finally reads
σ(ε) =

∞
4 X
sin2 δm+1 .
k m=−∞

(62)

An evaluation of the differential scattering cross section within the WKB approximation is shown in Fig. 8.
More precisely, we calculated the scattering amplitude
(60) entering (61) using the WKB approximation for the
phase shifts (58), and the sum over angular momentum
was cut off for |m| > 30. The cross section exhibits a pronounced asymmetry with respect to forward scattering,
χ = 0, with characteristic multiple peaks whose positions
shift with energy. Note that a peak in dσ/dχ at a negative angle χ corresponds to a pronounced scattering in
clockwise direction, i.e., to the right-hand side from the
perspective of the incoming wave. This so-called skew
scattering is also illustrated in Fig. 9 where we show the
scattering wave function in the same WKB approximation.
We consider here only the elastic scattering of
magnons. There are also inelastic scattering processes,
for example, when the magnons excite the breathing
bound state with m = 0 in Fig. 4. The inelastic scattering cross section of the skyrmion is beyond the scope
of the present work.

D.

Discussion of the magnon-skyrmion scattering

The skew scattering of magnons was recently observed
in micromagnetic simulations by Iwasaki et al.38 . These
authors also present a theory for the differential cross

10
(a)

(a)

40

5

30

0

-5

20

-10

10
0

10

-15
- 60

-90

- 45

- 30

-15

0

15

-20

30

-25
(b)

0

10

20

30

40

0

10

20

30

40

12
10

(b)

8

10
5

6

0

4

-5

2
-180

-150

-120

-90

-60

-30

0

30

FIG. 8: Differential cross section (61) evaluated within the
WKB approximation for various energies ε at magnetic fields
(a) κ2 = Q2 and (b) κ2 = 2Q2 . Skew scattering results in
a pronounced asymmetry with respect to forward scattering
χ = 0 with characteristic multiple peaks at high energies.

section and explain that the skew scattering arises from
an effective Lorentz force that emerges from the topological skyrmion texture. The theory of Ref. 38 for dσ/dχ
differs from ours, however, in two aspects. Firstly, the effective gauge potential for the magnons was assumed to
decay algebraically in Ref. 38 giving rise to a finite total
effective flux, whereas ours decreases exponentially with
distance resulting in a vanishing total effective flux. Secondly, the resulting effective flux density that we obtain
possesses a singularity at the skyrmion center. In the following, we explain in detail that this peculiar flux density
profile not only leads to skew scattering but is also at the
origin of rainbow scattering resulting in multiple peaks in
the differential cross section of Fig. 8.

-10
-15
-20
-25

FIG. 9: Scattering wave function in the WKB approximation
for the energy ε = 20εgap at κ = Q for an incoming wave
with k̂ = x̂. The arrows indicate the position of peaks in the
differential scattering cross section, see Fig. 8. The skyrmion
at the origin is represented by the circle with radius 1/κ.
scatter
~LAB
(r)−
Panel (a) shows only the scattered wave Re{(1, 0)ψ
ikr
scatter
~
e } and panel (b) displays Re{(1, 0)ψLAB (r)} of Eq. (59)
that exhibits the interference between the incoming and the
scattered wave.

ratory orthogonal frame is obtained from Eq. (31) with
the help of the singular gauge transformation Eq. (19),
ψ → ψLAB = −ie−iϕ ψ, and Eq. (9),

~aLAB = ~a − ∇χ = aχLAB χ̂ =
1.

Scattering from an effective magnetic flux

For high energies, ε  εgap , the scattering potential is essentially governed by vz (ρ) of Eqs. (42), see
Fig. 3, which in particular determines the position of
the classical turning point. As vz (ρ) is proportional to
the angular momentum m, this corresponds to scattering from an effective magnetic flux. Indeed, the effective gauge potential for the magnons within the labo-




cos θ − 1
− Q sin θ χ̂,
ρ
(63)

and vz (ρ) = −2maχLAB (ρ)/ρ. This gauge potential ~aLAB
is exponentially confined to the skyrmion area, which according to Stoke’s theorem implies a vanishing total flux.
The corresponding flux density, however, possesses an interesting structure. The first term on the right hand side
of Eq. (63) diverges for small radii as −2/ρ for θ → π

11
6

limit, the WKB scattering phase shift (58) assumes the
WKB
AB
Aharonov-Bohm form,55 δm
→ δm
with


 −π if m > 0
π
π
AB
δm = − |m + 1| + |m − 1| = 0 if m = 0 .

2
2
 π if m < 0
(68)

5
4
3
2
1
0
0

0.5

1

1.5

2

3

2.5

FIG. 10: Smooth part of the effective magnetic flux density
(65) for various values of κ.

This explains the asymptotic values obtained for the
phase shifts in Fig. 6 in the limit of high energies.
In the limit of low energies, ε → εgap , on the
other hand, one expects the phase shifts to obey Levinson’s theorem generalized to the case of Aharonov-Bohm
scattering,64
bound
AB
δm (εgap ) − δm (∞) = πNm
− δm
,

giving rise to a singular flux density,
beff (r − R) ≡ εzαβ ∂α~aLAB,β = −4πδ(r − R) + bsmth
eff (ρ).
(64)
The smooth part reads explicitly
bsmth
(65)
eff (ρ) =




1 cos θ − 1
cos θ − 1
− Q sin θ +
− Q sin θ .
∂ρ
ρ
ρ
ρ
It integrates to
Z ∞
∞
2π
dρ ρ bsmth
= 4π
eff (ρ) = 2π(cos θ − Qρ sin θ)
0

(69)

bound
where Nm
is the number of bound states with angular momentum number m. For our definition of the
AB
, and one obtains δm (εgap )/π =
phase shift δm (∞) = δm
bound
. For the specific value κ2 = Q2 there are two
Nm
magnon bound states present, see Fig. 4: the breathing
mode with m = 0 and the zero mode with m = −1.
Consequently, one expects all phase shifts to vanish at
the threshold εgap except δ0 (εgap ) = δ−1 (εgap ) = π for
κ2 = Q2 . This is in agreement with the numerically obtained values for the phase shifts presented in Fig. 6. Furthermore, the sharp drop of δ−2 (ε) close to the magnon
gap can be attributed to the bound state with m = −2
that materializes for slightly smaller values of κ.

0

(66)
and thus exactly cancels the singular part. The dependence of bsmth
eff (ρ) on the radius ρ is shown in Fig. 10 for
various values of κ. For κ2 /Q2 . 1.7, it possesses a local
maximum, and it even changes sign as a function of ρ for
κ2 /Q2 . 1.3.
Why is the flux density singular? Consider the orthogonal frame after the singular gauge transformation
iϕ +
(19), see Eq. (16), e.g., ê+
LAB = ie ê , as a function of
distance from the skyrmion center. For large distances
√1 (x̂ + iŷ) for θ = 0. On
θ → 0, and we recover ê+
LAB =
2
the other hand, very close to the skyrmion center θ ≈ π,
√1 (x̂ − iŷ)ei2χ becomes dependent on the
and ê+
LAB ≈
2
polar angle χ. It corresponds to an effectively rotating
frame that rotates twice upon encircling the core once,
resulting in the singular flux of −4π in Eq. (64).
Keeping only the effective magnetic scattering potential, the WKB potential of Eq. (57) simplifies to
(m − 1)2 − 2mρaχLAB (ρ)
UWKB (ρ)
≈1+
.
εgap
κ2 ρ2

(67)

At high energies, the classical turning point of this potential is asymptotically determined by the limiting value
ρaχLAB (ρ) → −2 for ρ → 0 corresponding to the scattering off a singular magnetic string with flux −4π. In this

2.

Classical deflection function & rainbow scattering

At fixed energies but in the limit of large angular momentum |m|  1, i.e., large impact parameter, the phase
shifts δm are eventually expected to vanish. Combined
with the Aharanov-Bohm constraint, Eq. (68), this has
the consequence that δm as a function of increasing but
negative m has to increase towards π, and for positive
and increasing m it again must increase towards zero,
see inset of Fig. 11. Treating the phase shift δm as a continuous function of m (except close to m = 0), it follows
that this function should change curvature. Equivalently,
its derivative, the classical deflection function54,56,57
Θm = 2

∂δm
,
∂m

(70)

possesses at least one stationary point with Θ0m = 0.
This is illustrated in Fig. 11. Note that the positive values obtained for Θm translate to a skew scattering at a
mathematically negative angle χ, that labels the vertical
axes of Fig. 8.
Generally, at such a stationary point multiple classical trajectories contribute to the scattering cross section
resulting in so-called rainbow scattering.54 For a single
stationary point, the scattering amplitude in the classical
limit is then described by the Airy function resulting in a

12

1.0
0.8
0.6

-20 -10

0.4

10

20

0.2
0.0
-30

-20

-10

0

10

20

mentum to the skyrmion. Using the conservation law
associated with translation invariance, we show that a
magnon current gives rise to a magnon pressure in the
form of a momentum-transfer force on the skyrmion.
This force enters the Thiele equation of motion for the
skyrmion, that can be interpreted as a constant flow of
momentum from the magnons to the skyrmion leading
to a constant skyrmion velocity. Evaluating the corresponding force explicitly, we arrive at an expression for
the skyrmion velocity Ṙ and the skyrmion Hall angle Φ.

30
A.

0
FIG. 11: Classical deflection function Θm = 2δm
of Eq. (70)
for the energy ε = 20εgap for various values of κ. As a function
of increasing κ, the three stationary points merge into a single
maximum. The inset shows the corresponding phase shifts
evaluated within the WKB approximation.

differential cross section with a sharp fall-off on the dark
side and an oscillatory behavior on the bright side of the
rainbow angle Θmst for which Θ0mst = 0. Interestingly,
the deflection function in Fig. 11 exhibits for κ2 = Q2
three stationary points whose contributions will interfere
in dσ/dχ as shown in Fig. 8(a) with a weight determined
by their curvature Θ00m . For increasing κ, the three stationary points merge into a single maximum, which in the
classical limit governs dσ/dχ at κ2 = 2Q2 as shown in
Fig. 8(b). The change in the number of stationary points
of Θm is related to the smooth part of the effective flux
density, see Fig. 10, which substantially alters its profile
on a similar scale of κ.

Effective skyrmion equation of motion
1.

Effective Thiele equation

As shown in appendix A, the conservation law deriving from space-time translation invariance reads, see
Eq. (A5),
stat
dµ Tµν
=

4π~
α0ν jαtop ,
a2

(71)

stat
is the energy-momentum tensor obtained
where Tµν
from the static part of the Lagrangian only, see Eq. (A4),
and jαtop is the spatial part of the topological current as
defined in Eq. (4).
Expanding the topological current up to second order
in the magnon fields we obtain

jαtop =

(72)
i
1
top(0)
~ † Γβ ψ)
~ + dβ (ψ
~ † τ z id0 ψ)
~
j0
d0 R α −
α0β d0 (ψ
8π
h

with the topological charge density of the static skyrmion
IV.

MAGNON PRESSURE ON THE SKYRMION

top(0)

j0
Consider a plane wave of magnons impinging on the
skyrmion as in Fig. 9(b). What is the pressure on the
skyrmion and will it be moving with a finite velocity Ṙ?
A skyrmion motion in a corresponding numerical experiment was recently observed by Iwasaki et al..38 It
was suggested by these authors that this motion can be
explained in terms of total momentum conservation implying, in particular, that the skyrmion can be considered
as a particle with well-defined momentum. However, the
notion of a conserved momentum for the field theory (1)
is subtle.58–61 We have recognized in section II C 1 that
in zeroth order in the massive modes ψ the skyrmion
coordinate, R, obeys the equation of motion of a massless particle in a magnetic field, Eq. (24). Its canonical
momentum (23) is spin-gauge dependent, and in general
neither well-defined nor conserved. Nevertheless, it was
argued in Ref. 60 that the coordinates Rα with α = 1, 2
are conjugate to each other and, therefore, can be interpreted as a momentum of the skyrmion texture, as
further discussed in Appendix A.
We explain below that magnons indeed transfer mo-

=

1 θ0 sin θ
1
n̂s (∂1 n̂s × ∂2 n̂s ) =
.
4π
4π ρ

(73)

The vertex Γβ is just the interaction vertex of Eq. (33).
Integrating the spatial component of Eq. (71) over space,
we arrive at an equation of motion for the skyrmion given
at this order by
G × d0 R = F ,

(74)

with G = − 4π~
It is just the Thiele equation of
a2 ẑ.
Eq. (24) but in the presence of an additional force F ,
that is given by
Fα =
(75)
Z
i
h

~
stat
~ † Γα ψ)
~ + dα (ψ
~ † τ z id0 ψ)
~
− d2 r dβ Tβα
+ 2 d0 (ψ
.
2a
We would like to determine the skyrmion velocity only in
linear response, so that we can limit ourselves to evaluate
the force F in zeroth order in d0 R. In a stationary scattering situation the second term on the right-hand side
in Eq. (75) vanishes and we neglect it in the following.

13
The integrand then reduces to a total derivative, and the
force is given by a surface integral. Choosing the surface
to be a circle with radius ρL ≫ 1/κ centered around the
skyrmion we finally obtain
Z 2π h
i
~
stat
~ † τ z id0 ψ)
~
F α = −ρL
dχ ρ̂β Tβα
+ 2 ρ̂α (ψ
2a
ρL
0
Z2π
mag
(76)
= −ρL dχ ρ̂β Tβα
ρL

0

One can verify that for large radii ρL the integrand is just
given by the spatial component of the energy-momentum
tensor of free magnons,
mag
Tµν
=

∂Lmag
~
d ψ
+ h.c. − δµν Lmag ,
~LAB ) ν LAB
∂(dµ ψ

(77)

with the Lagrangian

1 n ~  ~†
~LAB − (dτ ψ
~ † )τ z ψ
~LAB
ψLAB τ z dτ ψ
Lmag = 2
LAB
2a 2
o
~2
~ † )(dα ψ
~LAB ) + κ2 ψ
~† ψ
~LAB (78)
(dα ψ
+
LAB
LAB
2Mmag
but with the magnon field defined within the laboratory
orthogonal frame, see Eq. (19), and we have used the
expression for the magnon mass Mmag = ~2 /(2ε0 a2 ).
So we arrive at the result that the force, F , is just demag
termined by the net current of momentum, Tβα
, carried
by the magnons through the surface of the sample. This
net momentum is transfered to the skyrmion. Indeed,
using the results of appendix A 3 we can associate with
60,62,63
= 4π~
the skyrmion a momentum P skyr
α
a2 0αβ Rβ .
The Thiele equation (74) can then be rewritten in the
following form
d0 P skyr = F ,

(79)

which explicitly describes the flow of momentum between
the magnon subsystem and the skyrmion.
2.

Momentum-transfer force on the skyrmion

The force (76) only depends on the magnon wave function far away from the skyrmion so that we can use its
asymptotic scattering form. We consider a magnon plane
wave impinging from the left-hand side with fixed wave
vector k = kx̂ and on-shell energy ε
√
~LAB (r − R, t) = δ e−iεt/~ ψ
~ scatter (r − R),
ψ
(80)
LAB
√
as a function of real time t = −iτ . The amplitude is δ
~ scatter was specified already in Eq. (59). For the onand ψ
LAB
~LAB the Lagrangian Lmag vanishes,
shell wavefunction ψ
and the force is determined by
Fα =
Z 2π
− ρL

2

dχ ρ̂β
0

1
~
2a2 2Mmag

h

(81)
i
~ † )(∂α ψ
~LAB ) + h.c. .
(∂β ψ
LAB
ρL

FIG. 12: Illustration of the magnon pressure and the resulting skyrmion velocity, dt R. The magnons are emitted from
a source on the left-hand side, see also Fig. 9, and scatter
from the skyrmion represented by the circle with radius 1/κ.
The skyrmion experiences the force F given in Eq. (83) which
results in a finite skyrmion velocity dt R of Eq. (86), with a
skyrmion Hall angle Φ given in Eq. (87). The arrows only illustrate the orientation but not the length of the corresponding vectors.

With the help of the optical theorem
r
2π
Im{−ieiπ/4 f (χ = 0)}
σ=2
k
we find for the force the explicit expression
!
δ ~2 k 2
σk (ε)
F = 2
.
a 2Mmag σ⊥ (ε)

(82)

(83)

It depends on the energy-dependent longitudinal and
transversal cross sections
! Z
!
2π
σk (ε)
1 − cos χ dσ(ε)
=
dχ
.
(84)
dχ
− sin χ
σ⊥ (ε)
0
The force along the magnon wave vector k̂ T = (1, 0)
is determined by σk , which is an angular integral that
weights the factor 1 − cos χ with the differential cross
section. This structure is familiar from transport theory,
and signals that the flow of magnon momentum remains
unaltered for forward scattering resulting in a vanishing
contribution to the force. The component of F perpendicular to the wave vector, on the other hand, is governed
by σ⊥ and is here only finite due to the asymmetric skew
scattering.

B.

Skyrmion velocity and Hall angle Φ

The equation of motion (74) is easily solved and we
obtain a constant skyrmion velocity dt R = d0 R given by
dt Rα = −

a2
0αβ F β .
4π~

(85)

14
The skyrmion velocity reads explicitly
δ ~k 2
dt R =
8π Mmag

−σ⊥ (ε)
σk (ε)

!
.

(86)

The skyrmion velocity depends on its differential cross
section, and its orientation is governed by σ⊥ and σk . In
the linear response approximation, we can use the differential cross section evaluated in zeroth order in the
velocity-interaction (32) and can apply the results of
the previous section for dσ/dχ. At higher energies, the
skyrmion velocity dt R is approximately opposed to the
direction into which the magnons are preferentially scattered as σk (ε) > 0 and σ⊥ (ε) > 0, see the illustration in
Fig. 12. Such a direction for the skyrmion velocity was
numerically observed in Ref. 38.
To be more precise, we define the skyrmion Hall angle,
see Fig. 12,
σk (ε)
dt R y
Φ ≡ arctan
.
= arctan
−dt Rx
σ⊥ (ε)

(87)

An evaluation of Φ as a function of energy for various
values of κ is shown in Fig. 13. The Hall angle Φ for
values κ2 /Q2 = 1.25, 1.5, 1.75 and 2 is here evaluated
within the WKB approximation and therefore presented
only for energies ε/εgap > 10. The behavior of Φ for
lower energies is shown for κ2 = Q2 , for which we calculated the cross sections by using the exact phase shifts
for angular momenta −4 ≤ m ≤ 3 while the remaining
phase shifts up to |m| ≤ 30 are again evaluated within
the WKB approximation and higher angular momenta
are neglected. The scattering at low energies ε → εgap
is governed by s-wave scattering corresponding to the
phase shift δm with m = 1 in Eq. (60), see also Fig. 6. In
this limit, the magnon skew scattering is negligible, σ⊥
approximately vanishes, and the force (83) is practically
longitudinal to the incoming magnon momentum, F ∝ x̂.
This results in a maximum Hall angle of Φ = π/2 for
ε → εgap . For larger energies ε/εgap  1, on the other
hand, there is substantial magnon skew scattering giving rise to a finite σ⊥ and thus a finite transversal force
F⊥ ∝ σ⊥ that reduces Φ. The peak in the Hall angle at
around ε/εgap ≈ 2.5 for κ2 = Q2 can be attributed to
the resonance of the m = −3 mode, see Fig. 6.
The inset of Fig. 13 compares the skyrmion Hall angle Φ with the first moment hχiε , with hO(χ)iε =
R
1 2π
σ 0 dχO(χ)dσ/dχ. It was suggested in Ref. 38 that
the ratio −Φ/hχiε assumes the value of 1/2, which we
cannot confirm. This discrepancy is probably attributed
to an insufficient precision in the numerical experiment of
Ref. 38. Inspection of Eq. (87) reveals that a ratio of 1/2
would only obtain for a differential cross section with vanishing higher cumulants so that, e.g., hsin χiε = sinhχiε .
In the limit ε → εgap the ratio −Φ/hχiε even diverges as
hχiε → 0 in the limit of s-wave scattering.

FIG. 13: The skyrmion Hall angle Φ as defined in Eq. (87)
as a function of energy for various values of κ, for details see
text. The inset shows the ratio −Φ/hχiε . The Hall angle is
maximal Φ = π/2 in the limit ε → εgap where magnon s-wave
scattering prevails.

V.

SUMMARY AND DISCUSSION

A two-dimensional chiral magnet adopts a fieldpolarized ground state for a sufficiently large magnetic
field perpendicular to the film corresponding to κ > κcr
in Fig. 2. The magnetic skyrmion then corresponds to a
large-amplitude excitation with positive energy εs . Such
topological skyrmion excitations are always present in
an experimental system. Their density might either be
given by a thermal distribution reducing to a Boltzmann
factor e−βεs at lowest temperatures, or depend on the
history of the sample because the topological protection
of skyrmions results in long equilibration times.
In any case, the presence of a skyrmion will modify the
properties of the small amplitude fluctuations, i.e., the
magnon excitations. We investigated the basic aspects
of this magnon-skyrmion interaction in the present work.
Starting from the non-linear sigma model for chiral magnets (1), we first derived the magnon Hamiltonian (27)
by expanding around the skyrmionic saddle point solution. As the skyrmion scattering potential does not preserve the magnon number, this Hamiltonian was found
to possess a (bosonic) Bogoliubov-deGennes form. The
Hamiltonian also includes a term that explicitly depends
on the skyrmion velocity (32), whose consequences, however, have not been investigated yet in this work
Solving the Bogoliubov-deGennes scattering problem
we first determined the magnon spectrum. In the magnetic field regime where the field-polarized state is stable, we found two magnon-skyrmion bound states: the
breathing mode with m = 0 and the quadrupolar mode
with m = −2, see Figs. 4 and 5. For a visualization of

15
breathing mode m = 0

M3 , Q11 , Q22 , Q33 , T3

quadrupolar mode m = −2

Q11 , Q22 , Q12 , Q21

TABLE III: Moments that are excited by the magnonskyrmion bound state m = 0 and m = −2. Mi , Qij , and
Ti are the dipole, quadrupolar and toroidal moments, respectively, see Eq. (88).

these modes see also Ref. 50. For a smaller but finite
magnetic field, the quadrupolar eigenfrequency eventually vanishes signalling a local bimeron instability of the
single skyrmion. Our results are in good agreement with
a recent numerical diagonalization study.37
The bound magnon modes will give rise to weak subgap resonances in magnetic or electric resonance experiments whose weight will be proportional to the skyrmion
density in the sample. In order to determine their selection rules, we consider here the magnetic dipole, Mi ,
quadrupolar, Qij , and toroidal moment, Ti ,65 defined as
follows
Z
Mi = dr n̂i (r),
Z
1
(88)
Qij = dr (n̂i (r)n̂j (r) − δij ),
3
Z
Ti = dr iαj r α n̂j (r).
In the field-polarized state without a skyrmion, only the
components M3 and Qii with i = 1, 2, 3 are finite and
proportional to the volume V whereas all other components vanish. The skyrmion not only leads to a modification of these finite components of order O(V 0 ) but
also induces a finite toroidal moment T3 that scales as
the third power of the skyrmion radius, 1/κ,
Z ∞
1
T3 = 2π
(89)
dρρ2 sin θ = 3 T (κ2 /Q2 ),
κ
0
where T is a dimensionless function. If the skyrmion is
excited either with the breathing mode or the quadrupolar mode, oscillations of certain moments arise that are
listed in Table III. An ac magnetic or electric field could
couple to these moments and thus excite the corresponding magnon-skyrmion bound state. An ac magnetic field perpendicular to the film directly couples to
M3 , and will therefore excite, similar to the skyrmion
lattice,33 the breathing mode of the skyrmion. A perpendicular ac electric field, on the other hand, couples
to the polarization P3 , which for the insulating chiral magnet Cu2 OSeO3 is in general given by66,67 P ∝
(Q23 , Q31 , Q12 ), so that it will excite the quadrupolar
mode. As the toroidal moment couples to the cross product of electric and magnetic field, T ∼ E × H,65 in-plane
ac electric and magnetic fields might also be able to excite
the breathing mode.
Apart from the spectrum of magnon bound states,
we also discussed the differential cross section dσ/dχ

for magnon scattering off the skyrmion. The scattering potential, in particular, includes an Aharonov-Bohm
flux density that governs the scattering characteristics at
large magnon energies. While the total flux vanishes, the
density possesses a singularity at the skyrmion core that
is related to the non-trivial skyrmion topology. As explained in detail in section III D, this specific flux density
profile is at the origin of rainbow scattering giving rise to
an asymmetric differential cross section with oscillating
behavior as a function of the scattering angle, see Fig. 8.
Our results for dσ/dχ differ from the theory presented in
Ref. 38, that did not find oscillations of dσ/dχ characteristic for rainbow scattering. Importantly, the magnons
skew scatter from the skyrmion, see Fig. 9, as previously
pointed out in Ref. 38. This skew scattering generates a
topological magnon Hall effect30 that is proportional to
the skyrmion density.
The magnons not only scatter off but also transfer momentum to the skyrmion. The resulting magnon pressure on the skyrmion due to a constant magnon current
was determined in section IV. Starting from the conservation law associated with translation invariance of the
action (1), that is discussed in detail in appendix A, we
demonstrated that the magnon pressure enters as an effective force in the Thiele equation of motion (74) for the
skyrmion. This effective force is determined by the net
transfer of magnon momentum. It depends, in particular, on the magnon differential cross section, and it is
thus a reactive momentum-transfer force. The solution of
the resulting Thiele equation predicts a skyrmion velocity with a component longitudinal and transverse to the
magnon current. The transverse component is attributed
to the longitudinal scattering cross section σk , giving rise
to a large skyrmion Hall effect. Due to the asymmetric
skew scattering, there is also a finite transversal cross section σ⊥ , which determines the longitudinal motion. This
longitudinal motion is, interestingly, antiparallel to the
magnon current, i.e., it is towards the magnon source.
Our theory provides an explanation of the numerical experiment in Ref. 38 where a corresponding skyrmion motion was observed.
We note that our result for the magnon pressure due to
momentum-transfer is distinctly different from the conclusion drawn from the mode-decomposition theory of
Ref. 68, which has been invoked to explain the skyrmion
motion in Refs. 27–29. The latter theory, in particular,
predicts in the limit of vanishing Gilbert damping a vanishing skyrmion Hall effect and a universal longitudinal
skyrmion motion antiparallel to the magnon current that
is independent of the differential magnon scattering cross
section in contrast to our findings, Eq. (86). We believe
that our results for the magnon scattering cross section
as well as for the magnon pressure pave the way for a
genuine theory of skyrmion caloritronics,71 i.e., thermal
spin-transport phenomena for a dilute gas of skyrmions
in clean insulating chiral magnets.
There are several interesting open issues to be explored
in future work. Most importantly, the interaction be-

16
tween the magnons and the skyrmion velocity, Eq. (32),
naturally produces in second-order perturbation theory
an effective retarded skyrmion mass. It is an important
open question whether such a retarded mass allows for an
additional collective magnon-skyrmion bound state corresponding to a cyclotron mode of the massive Thiele
equation.69,70 Such a mode would be reminiscent of the
gyration modes observed as magnetic resonances in the
skyrmion lattice phase.33–35

Acknowledgments

We acknowledge helpful discussions with J. Iwasaki,
S. Komineas, S.-Z. Lin, N. Nagaosa, and, especially,
A. Rosch. We would also like to acknowledge an interesting conversation with B. A. Ivanov that motivated this
work.

Appendix A: Conserved Noether currents

We present a discussion of important Noether currents of the Lagrangian L of Eq. (1), i.e., the conservation laws deriving from translation and rotation invariance. Whereas these conservation laws are manifest spingauge invariant, the corresponding canonical energymomentum tensor and angular momentum vector current themselves depend on the spin-gauge potential.58–61
In general, this precludes the definition of a conserved total canonical momentum and angular momentum. However, in case the topological charge is preserved within
the sample a definition of a conserved total momentum
and angular momentum becomes possible in agreement
with previous findings by Papanicolaou and Tomaras.60
For the indices we use the conventions of Table II.

1.

Canonical energy-momentum tensor

The theory (1) is translationally invariant so that the
canonical energy momentum tensor
Tµν =

∂L
dν n̂ − δµν L
∂(dµ n̂)

(A1)

is conserved
dµ Tµν = 0.

(A2)

~ of
The tensor Tµν depends on the spin-gauge field A
Eq. (3). For example, the canonical momentum density
~ ~
T0α = − 2 Ad
α n̂
a

(A3)

~ 58 Nevertheless, the conservation law
is determined by A.
(A2) itself is gauge invariant. This is best seen by first

defining the energy-momentum tensor deriving from the
static Lagrangian Lstat only,
stat
Tµν
=

∂Lstat
dν n̂ − δµν Lstat .
∂(dµ n̂)

(A4)

The conservation law (A2) can then be written in the
manifest spin-gauge invariant form
stat
dµ Tµν
−

4π~
µ0ν jµtop = 0,
a2

(A5)

where we have used the identity of Eq. (8). So we arrive
stat
at the result that the divergence of Tµν
is given by the
topological current of Eq. (4).
that the integral over the spatial divergence
R Assuming
stat
stat
d2 rdα Tαµ
= 0, i.e., that Tαµ
vanishes on the surface
of the two-dimensional sample, it follows from the timecomponent of Eq. (A5) the conservation of total energy,
d0 E = 0, with
Z
Z
stat
E ≡ − d2 rT00
= d2 rLstat .
(A6)
Due to the anomalous form of the conservation law, however, we are in general not able to define a conserved total
momentum. Instead it follows from the spatial compostat
nent of (A5) with T0α
= 0 that the spatial integral over
the topological current vanishes
Z
4π~
− 2 α0β d2 r jαtop = 0.
(A7)
a
However, with the additional assumption that the conservation law for the topological current of Eq. (5) holds
and that the product r α jβtop vanishes on the surface, we
can write
Z
Z


d2 rjαtop = d2 r −dβ (r α jβtop ) + jαtop
(A8)
Z
Z
= − d2 r r α dβ jβtop = d0 d2 r r α j0top .
In this case, following Ref. 60 we can identify a total
conserved momentum
Z
4π~
(A9)
P α = − 2 0αβ d2 r r β j0top
a
with the first moment of the topological charge distribution.
In Ref. 60 this result for the conserved momentum was
obtained by starting directly from the equation for the
time-derivative of the topological charge density
4π~
stat
,
d0 j0top = 0αβ dα dγ Tγβ
a2

(A10)

which can be derived from Eq. (A5) by applying the
derivative α0ν dα with α = 1, 2, summing over ν, and
using the conservation law for the topological current
Eq. (5).

17
2.

(A19) is spin-gauge invariant whereas Jµ itself is not.
Introducing the part of the angular momentum current

Angular momentum

For completeness, we also discuss the conservation law
deriving from rotational invariance. Due to the spin-orbit
coupling Q, only the total angular momentum vector current obeys a conservation law. In the following, we first
discuss the spin-, afterwards the orbital and, finally, the
total angular momentum.
a. Spin angular momentum From the rotations by
an infinitesimal angle ω of the magnetisation around the
magnetic field direction B̂ = ẑ, n̂i → n̂i + δn̂i with
δn̂i = ωizk n̂k

(A11)

follows
∂Lstat
∂Lstat
izk n̂k −
izk dµ n̂k
∂ni
∂dµ n̂i
= −ε0 Q(n̂z dα n̂α − n̂α dα n̂z ).

dµ Sµ = −

(A12)

The 2+1 spin angular momentum current,
~
S0 = − 2 n̂z ,
a
∂Lstat
Sα = −
izk n̂k
∂dα n̂i
= −ε0 [izk n̂k dα n̂i + Q(n̂z n̂α − δzα )]

(A13)
(A14)

is not conserved as the right-hand side of Eq. (A12) is
finite due to the spin-orbit coupling Q. Note that according to our sign convention in Eq. (3) the magnetisation
vector points antiparallel to the spin vector as it is for
example the case for electrons.
b. Orbital angular momentum Performing an infinitesimal orbital rotation around the z-axis
δn̂i = −ωα0β r β dα n̂i

stat
J˜µ = Sµ + β0γ r γ Tµβ

that is manifest invariant, the conservation law assumes
the form
dµ J˜µ +

The time-dependence of the spatial integral over the density, J˜0 = − a~2 n̂z , is thus determined by the integrated
scalar product of the position vector r with the spatial
topological current jαtop . With the additional assumption that the topological current is conserved, Eq. (5),
and that the product r 2 jαtop vanishes on the surface, we
can rewrite the last term as a time derivative
Z
Z

1
2
top
d r r α jα = d2 r
dα (r 2 jαtop ) − r 2 dα jαtop
2
Z
1
= d0 d2 r r 2 j0top .
(A23)
2
As a result, we finally obtain


Z
~
2π~
J = d2 r − 2 n̂z + 2 r 2 j0top
a
a

(A17)

is not conserved because the energy-momentum tensor is
not symmetric due to the spin-orbit coupling Q.
c. Total angular momentum The theory (1) is invariant with respect to a combined rotation of spin and
real space around the magnetic field direction. As a result, the total angular momentum
(A18)

is conserved

for the conserved total angular momentum, d0 J = 0.60
Momentum and angular momentum of the
skyrmion

It is instructive to compute the momentum and the
angular momentum attributed to the magnetic skyrmion
solution of section II B. Neglecting the massive fluctuations, ψ, we obtain for the momentum (A9)
Z
4π~

d2 r r β j0top (r − R)
P skyr
=
−
0αβ
α
a2
ψ,ψ ∗ =0
4π~
= 2 0αβ Rβ .
(A25)
a
On this level of approximation, the conservation of P skyr
α
directly follows from the equation of motion (24),
d0 P skyr
=
α

dµ Jµ = 0,

(A24)

(A16)

The angular momentum

Jµ = Sµ + Lµ

(A21)

With the assumption that the current JR˜α vanishes on
the surface of the two-dimensional sample d2 rdα J˜α = 0
we find
Z
Z
4π~
2 ˜
d0 d r J 0 + 2
d2 r r α jαtop = 0.
(A22)
a

3.

Lµ = β0γ r γ Tµβ

4π~
r α jαtop = 0.
a2

(A15)

we obtain
dµ Lµ = β0α Tαβ .

(A20)

4π~
0αβ d0 Rβ = (G × d0 R)α = 0
a2

(A26)

(A19)

which follows from Eqs. (A12) and (A16). Similarly as
for the energy-momentum tensor, the conservation law

The angular momentum (A24) of the fully fieldpolarized state, n̂ = ẑ, is already non-zero and given
by the total spin of the sample, JFP = −V~/a2 where

18
V is the volume. Neglecting again the massive fluctuations, we find for the angular momentum attributed to
the skyrmion
− JFP
(A27)
Jskyr = J
ψ,ψ ∗ =0


Z
2π~
~
= d2 r − 2 (n̂z − 1) + 2 r 2 j0top
a
a
ψ,ψ ∗ =0


Z
2π~
~
= d2 r − 2 (n̂z − 1) + 2 (r − R)2 j0top
a
a
ψ,ψ ∗ =0


Z
2π~
+ d2 r
(2rR − R2 )j0top
a2
ψ,ψ ∗ =0
It turns out that the first line in the last equation exactly
vanishes,


Z
~
2π~
2
2 top
d r − 2 (n̂z − 1) + 2 (r − R) j0
a
a
ψ,ψ ∗ =0
Z ∞


2π~
ρ
= 2
dρ ρ −(cos θ − 1) + θ0 sin θ
a
2
0
2π~ 2 2 θ ∞
= 2 ρ sin
= 0,
(A28)
a
2 ρ=0

1

S. Mühlbauer, B. Binz, F. Jonietz, C. Pfleiderer, A. Rosch,
A. Neubauer, R. Georgii, and P. Böni, Science 323, 915
(2009).
2
A.N. Bogdanov and D.A. Yablonskii, Sov. Phys. JETP 68,
1 (1989).
3
A. Bogdanov and A. Hubert, Journal of Magnetism and
Magnetic Materials 138, 255 (1994).
4
U. K. Rößler, A. N. Bogdanov, and C. Pfleiderer, Nature
442, 797 (2006).
5
T. Adams, S. Mühlbauer, C. Pfleiderer, F. Jonietz, A.
Bauer, A. Neubauer, R. Georgii, P. Böni, U. Keiderling,
K. Everschor, M. Garst, and A. Rosch, Phys. Rev. Lett.
107, 217206 (2011).
6
X. Z. Yu, N. Kanazawa, Y. Onose, K. Kimoto, W. Z.
Zhang, S. Ishiwata, Y. Matsui, and Y. Tokura, Nat. Mater.
10, 106 (2011).
7
W. Münzer, A. Neubauer, T. Adams, S. Mühlbauer, C.
Franz, F. Jonietz, R. Georgii, P. Böni, B. Pedersen, M.
Schmidt, A. Rosch, and C. Pfleiderer, Phys Rev B 81,
041203 (2010).
8
X. Z. Yu, Y. Onose, N. Kanazawa, J. H. Park, J. H. Han,
Y. Matsui, N. Nagaosa, and Y. Tokura, Nature 465, 901
(2010).
9
S. Seki, X. Z. Yu, S. Ishiwata, and Y. Tokura, Science 336,
198 (2012).
10
T. Adams, A. Chacon, M. Wagner, A. Bauer, G. Brandl,
B. Pedersen, H. Berger, P. Lemmens, and C. Pfleiderer,
Phys. Rev. Lett. 108, 237204 (2012).
11
A. Neubauer, C. Pfleiderer, B. Binz, A. Rosch, R. Ritz, P.
G. Niklowitz, and P. Böni, Phys. Rev. Lett. 102, 186602
(2009).
12
M. Lee, W. Kang, Y. Onose, Y. Tokura, and N. P. Ong,
Phys. Rev. Lett. 102, 186601 (2009).
13
T. Schulz, R. Ritz, A. Bauer, M. Halder, M. Wagner,

due to the exponentially fast approach of the polar angle
θ to its boundary value at large distances, θ → 0. The
change of spin angular momentum due to the spatial dependence of n̂z (r) is thus exactly compensated by the orbital angular momentum that is carried by the skyrmion
texture. The skyrmion angular momentum then reduces
to

Z
2π~
d2 r (2rR − R2 )j0top
Jskyr = − 2
a
ψ,ψ ∗ =0
2π~ 2
=− 2 R .
(A29)
a

The time derivative of Jskyr , i.e., the torque assumes with
the help of Eq. (A26) the following intuitive form

d0 Jskyr = (R × d0 P skyr )z .

(A30)

C. Franz, C. Pfleiderer, K. Everschor, M. Garst, and A.
Rosch, Nat. Phys. 8, 301 (2012).
14
G. Volovik, The Universe in a Helium Droplet (Oxford
Univ. Press, 2003).
15
N. Nagaosa, X. Z. Yu, and Y. Tokura, Phil. Trans. R. Soc.
A 370, 5806 (2012).
16
A. A. Thiele, Phys. Rev. Lett. 30, 230 (1973).
17
M. Stone, Phys. Rev. B 53, 16573 (1996).
18
F. Jonietz, S. Mühlbauer, C. Pfleiderer, A. Neubauer, W.
Mnzer, A. Bauer, T. Adams, R. Georgii, P. Böni, R. A.
Duine, K. Everschor, M. Garst, and A. Rosch, Science 330,
1648 (2010).
19
K. Everschor, M. Garst, R. A. Duine, and A. Rosch, Phys.
Rev. B 84, 64401 (2011).
20
K. Everschor, M. Garst, B. Binz, F. Jonietz, S. Mühlbauer,
C. Pfleiderer, and A. Rosch, Phys. Rev. B 86, 054432
(2012).
21
X. Z. Yu, N. Kanazawa, W. Z. Zhang, T. Nagai, T. Hara,
K. Kimoto, Y. Matsui, Y. Onose, and Y. Tokura, Nature
Commun. 3, 988 (2012).
22
J. Iwasaki, M. Mochizuki, and N. Nagaosa, Nature Communications 4, 1463 (2013).
23
S.-Z. Lin, C. Reichhardt, C. D. Batista, and A. Saxena,
Phys. Rev. Lett. 110, 207202 (2013).
24
S.-Z. Lin, C. Reichhardt, C. D. Batista, and A. Saxena,
Phys. Rev. B 87, 214419 (2013).
25
J. Sampaio, V. Cros, S. Rohart, A. Thiaville, and A. Fert,
Nature Nanotech 8, 839 (2013).
26
N. Nagaosa and Y. Tokura, Nature Nanotech 8, 899 (2013).
27
L. Kong and J. Zang, Phys. Rev. Lett. 111, 67203 (2013).
28
S.-Z. Lin, C. D. Batista, C. Reichhardt, and A. Saxena,
Phys. Rev. Lett. 112, 187203 (2014).
29
A. A. Kovalev, Phys. Rev. B 89, 241101(R) (2014).
30
M. Mochizuki, X. Z. Yu, S. Seki, N. Kanazawa, W.

19
Koshibae, J. Zang, M. Mostovoy, Y. Tokura, and N. Nagaosa, Nature Materials 13, 241 (2014).
31
O. Petrova and O. Tchernyshyov, Phys. Rev. B 84, 214433
(2011).
32
J. Zang, M. Mostovoy, J. H. Han, and N. Nagaosa, Phys.
Rev. Lett. 107, 136804 (2011).
33
M. Mochizuki, Phys. Rev. Lett. 108, 017601 (2012).
34
Y. Onose, Y. Okamura, S. Seki, S. Ishiwata, and Y.
Tokura, Phys. Rev. Lett. 109, 37603 (2012).
35
T. Schwarze, J. Waizner, M. Garst, A. Bauer, I.
Stasinopoulos, H. Berger, C. Pfleiderer, and D. Grundler,
submitted.
36
A. Auerbach, Interacting Electrons and Quantum Magnetism, (Springer, New York, 1998).
37
S.-Z. Lin, C. D. Batista, and A. Saxena, Phys. Rev. B 89,
024415 (2014).
38
J. Iwasaki, A. J. Beekman, and N. Nagaosa, Phys. Rev. B
89, 064412 (2014).
39
P. Bak and M. H. Jensen, J. Phys. C 13, L881 (1980).
40
O. Nakanishi, A. Yanase, A. Hasegawa, and M. Kataoka,
Solid State Commun. 35, 995 (1980).
41
M. Ezawa, Physics Letters A 375, 3610 (2011).
42
D. D. Morrison, J. D. Riley, and J. F. Zancanaro, Communications of the ACM 12, 613 (1962).
43
A. M. Kosevich, B. A. Ivanov, and A. S. Kovalev, Physics
Reports 194, 117 (1990).
44
B. A. Ivanov, JETP Lett. 61, 917 (1995).
45
B. A. Ivanov, H. Schnitzer, F. G. Mertens, and G. M.
Wysin, Phys. Rev. B 58, 8464 (1998).
46
D. D. Sheka, B. A. Ivanov, and F. G. Mertens, Phys. Rev.
B 64, 024432 (2001).
47
We assume that Umklapp scattering can be neglected as
the size of the skyrmion, 1/κ, is incommensurate and large
compared to the lattice spacing a.
48
R. Rajaraman Solitons and instantons North-Holland,
Amsterdam (1982).
49
M. Ezawa, Phys. Rev. B 83, 100408(R) (2011).
50
Short movies visualising the bound magnon modes can be
found in the supplement.

51

R. E. Langer, Phys.Rev. 51, 669 (1937).
M. V. Berry and K. E. Mount, Reports on Progress in
Physics 35, 315 (1972).
53
H. Frisk and T. Guhr, Annals of Physics 221, 229 (1993).
54
K. W. Ford and J. A. Wheeler, Annals of Physics 7, 259
(1959).
55
Y. Aharonov and D. Bohm, Phys. Rev. 115, 485 (1959).
56
J. Herb, P. Meerwald, M. J. Moritz, and H. Friedrich, Phys.
Rev. A 60, 853 (1999).
57
M. Fink, J. Eiglsperger, H. Friedrich, and J. Madroñero,
Phys. Rev. A 80, 24701 (2009).
58
F. D. M. Haldane, Phys. Rev. Lett. 57, 1488 (1986).
59
G. E. Volovik, J. Phys. C: Solid State Phys. 20 L83 (1987).
60
N. Papanicolaou, and T. N. Tomaras, Nuclear Physics B
360, 425 (1991).
61
P. Yan, A. Kamra, Y. Cao, and G. E. W. Bauer, Phys.
Rev. B 88, 144413 (2013).
62
S. Komineas and N. Papanicolaou, Physica D 99, 81
(1996).
63
S. Komineas and N. Papanicolaou, New Journal of Physics
10, 043021 (2008).
64
D. D. Sheka and F. G. Mertens, Phys. Rev. A 74, 052703
(2006).
65
N. A. Spaldin, M. Fiebig, and M. Mostovoy, Journal of
Physics: Condensed Matter 20, 434203 (2008).
66
S. Seki, S. Ishiwata, and Y. Tokura, Phys. Rev. B 86,
060403 (2012).
67
Y.-H. Liu, Y.-Q. Li, and J. H. Han, Phys. Rev. B 87,
100402 (2013).
68
A. A. Kovalev and Y. Tserkovnyak, Europhys Lett 97,
67002 (2012).
69
B. A. Ivanov and V. A. Stephanovich, Physics Letters A
141, 89 (1989).
70
B. A. Ivanov and D. D. Sheka, JETP Letters 82, 436
(2005).
71
G. E. W. Bauer, E. Saitoh, and B. J. van Wees, Nat. Mater.
11, 391 (2012).
52


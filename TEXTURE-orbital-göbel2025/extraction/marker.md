INTERIM: pdftotext fallback, marker/nougat not installed on this node

Three-dimensional topological orbital Hall effect caused by magnetic hopfions
Börge Göbel1, ∗ and Samir Lounis1

arXiv:2506.11448v3 [cond-mat.mes-hall] 9 Oct 2025

1

Institut für Physik, Martin-Luther-Universität Halle-Wittenberg, D-06099 Halle (Saale), Germany
(Dated: October 10, 2025)

Magnetic hopfions are non-collinear spin textures that are characterized by an integer topological invariant,
called Hopf index. The three-dimensional magnetic solitons can be thought of as a tube with a twisted magnetization that has been closed at both ends to form a torus. The tube consists of a magnetic whirl called in-plane
skyrmion or bimeron. Although hopfions have been observed by microscopy techniques, their detection remains
challenging as they lack an electronic hallmark so far. Here we predict a three-dimensional orbital Hall effect
caused by hopfion textures: When an electric field is applied, the hopfion generates a transverse current of orbital
angular momentum. The effect arises due to the local emergent field that gives rise to in-plane and out-of-plane
orbital Hall conductivities. This orbital Hall response can be seen as a hallmark of hopfions and allows us to distinguish them from other textures, like skyrmioniums, that look similar in real-space microscopy experiments.
While the two-dimensional topological invariant of a skyrmion determines its topological Hall transport, the
unique three-dimensional topological orbital Hall effect can be identified with the three-dimensional topological invariant that is the Hopf index. Our results make hopfions attractive for spin-orbitronic applications because
their orbital signatures allow for their detection in devices and give rise to large orbital torques.

I.

INTRODUCTION

Non-collinear spin textures have emerged as a central topic
in condensed matter physics due to their rich physics and potential applications in spintronic devices. Unlike collinear
magnetic systems, where spins align uniformly in parallel
or antiparallel configurations, non-collinear arrangements exhibit spatially varying spin orientations that can even give rise
to topologically non-trivial spin textures, such as the family of
two-dimensional magnetic whirls [1] including skyrmions [2–
5], antiskyrmions [6–8] and bimerons [9–11]. These textures can be considered as solitons that can be moved by
current-induced spin torques and can be easily identified by
real-space microscopy imaging techniques. Their topological
nature gives rise to an effective magnetic field, called emergent field [12], that causes a topological Hall effect which is a
unique signature of skyrmions [13–16] and many related textures [10, 17–20].
Magnetic hopfions [21–35] consist of a bimeron tube that
has been twisted once and that has been merged at both ends
to form a torus. These non-collinear magnetic solitons are innately three-dimensional [cf. Fig. 1(a)], which makes their
physics even richer as they possess more degrees of freedom. For example, not only can they be moved by currents [28, 30] but also tilted [29, 30]. Detecting these objects
remains a difficult challenge, since hopfions do not exhibit
a sizable topological Hall effect [29] and typical real-space
microscopy techniques rely on two-dimensional projections
of the magnetic textures, which is problematic for a threedimensional soliton: The detectable signals caused by hopfions look similar to those of a skyrmionium [19, 36, 37] – a
skyrmion that resides at the center of another skyrmion with
reversed magnetization. Still, the experimental observation
of hopfions has been achieved using a combination of X-ray
photoemission electron microscopy (X-PEEM) and magnetic

∗ Correspondence email address: boerge.goebel@physik.uni-halle.de

soft X-ray transmission microscopy (MTXM) [32] or Lorentz
transmission electron microscopy (LTEM) [35]. However,
a more conclusive detection method would reveal the actual
three-dimensional texture which is, in principle, possible by
holography or tomography techniques using X-rays or electrons [38–45]. Unfortunately, these techniques are highly demanding and not compatible with potential spintronic applications of hopfions. A simple electric or magnetic signature of
hopfions is desired to make these textures usable in devices.
Therefore, we consider the research field of orbitronics
which has attracted great interest recently. It is concerned with
the orbital angular momentum and the related orbital current.
In equilibrium, the orbital angular momentum of a solid is often quenched because of the high symmetry, which is why the
magnetization of most ferromagnets originates from the spin
degree of freedom. However, when an electric field drives a
system out of equilibrium, a sizable density of orbital magnetic moment or transverse orbital currents can be generated.
These phenomena are called orbital Edelstein effect [46–59]
and orbital Hall effect [60–75], respectively, and they are often larger than their spin counter-parts. The orbital effects often exist even without the relativistic spin-orbit coupling and
only a small portion of these orbital signals gets converted to
a spin Edelstein effect or a spin Hall effect due to this relativistic mechanism. Non-collinear spin textures with a nontrivial topology, such as the magnetic skyrmion, give rise to an
orbital magnetization [76–78] in equilibrium, and have been
shown to exhibit a topological orbital Hall effect once an electric field is applied [75]. Even textures with a compensated
emergent field, such as antiferromagnetic skyrmions [79–82],
can exhibit such an effect [75] due to the local presence of an
emergent field, even though it is compensated on average.
In this paper, we use a tight-binding and Kubo approach
and predict a three-dimensional topological orbital Hall effect
caused by hopfion textures. This effect is generated by their
local emergent field that gives rise to an orbital Berry curvature [cf. Fig. 2] and causes out-of-plane and in-plane orbital
Hall conductivities [cf. Fig. 3]. The orbital Hall signatures
of a hopfion are unique and allow us to distinguish it from

2
(c) m(x,y,0)
(a) m(x,y,z)

(b) Bem(x,y,z)

y
x

z

(d) m(0,y,z)
z

y

z
y

y

x

x

FIG. 1. Magnetic hopfion. (a) Magnetic texture m(r) of a λ = 8a hopfion. (b) Corresponding emergent field B em (r). (c) A cut along the
xy plane reveals a magnetic skyrmionium. (d) A cut along the the yz plane reveals two in-plane skyrmions also called bimerons. The color
of the arrows in all panels encodes their orientation in the xy plane. White and black arrows point along the positive and negative z direction,
respectively. Note that these arrows that surround the hopfion have been plotted translucently to allow for a clearer view of the non-collinear
part of the texture.

two-dimensional topological textures, such as the skyrmion,
bimeron or skyrmionium. While the two-dimensional topological invariant of a skyrmion determines its topological Hall
transport, the unique three-dimensional orbital Hall transport
is a manifestation of the three-dimensional topological invariant called Hopf index. Although all results presented in this
paper rely on quantum mechanical calculations, they can be
understood semiclassically on the basis of the emergent field
of the textures and the carrier density of the conduction electrons.
This paper is structured as follows. We begin by detailing the tight-binding method used throughout this paper. In
Sec. II A we discuss the considered hopfion texture that enters the Hamiltonian and in Sec. II B we present the Kubo approach that allows us to calculate the orbital Hall conductivity.
The results of these calculations are presented in Sec. III A.
In Sec. III B we compare the results with the Hall transport
caused by textures that are closely related to hopfions: 1.
skyrmion tubes, 2. bimeron tubes and 3. skyrmionium tubes.
The energy dependencies of the orbital Hall conductivities can
be understood by analyzing the carrier density and the emergent magnetic field of these textures; cf. Sec. III C. Finally,
we conclude in Sec. IV.

II.

MODEL AND METHODS

Throughout this paper, we use a tight-binding model to describe the conduction electrons and their spins’ interaction
with the hopfion texture (Sec. II A). The orbital conductivity tensor elements are calculated based on a Kubo approach
(Sec. II B).

A.

Hopfion texture

First of all, we want to introduce the hopfion texture m(r)
and discuss its topological properties. m is the normalized
magnetic moment and r is the position vector.
p We use the
top-down view coordinates x, y with r =
x2 + y 2 the
distance and ϕ = arctan(y/x) the polar angle, as well as
the transformed
coordinates ρx = r − λ/2, ρy = z with
q
ρ=

ρ2x + ρ2y . The hopfion is modeled as


xρ −yρ 
sin(2πρ/λ) yrρ x
+yρy 
m(r) = sin(2πρ/λ) xρxrρ
− cos(2πρ/λ)

(1)

in
the
volume
of
the
torus
p
(x − λ/2 · cos ϕ)2 + (y − λ/2 · sin ϕ)2 + z 2
<
λ/2
and m(r) = ez elsewhere. This texture is topologically
equivalent to the ones used in the literature, e. g. Ref. [25, 29],
but has a homogeneous background. This is important because the orbital Hall transport will be calculated based on
a reciprocal-space approach, so we need periodicity in real
space. The texture above describes the texture in a unit cell of
size 2λ × 2λ × λ.
The hopfion texture is shown in Fig. 1(a) and can be thought
of as a skyrmion tube that is magnetized in the plane of
the tube, has been twisted once, and whose ends have been
merged to form a torus. In our calculations, the torus is located in the xy plane. If the three-dimensional magnetic texture is cut along the xy plane, the result is a skyrmionium – a
skyrmion that is positioned at the center of another skyrmion
with opposite magnetization. This cut containing the skyrmionium is shown in Fig. 1(c). If one cuts the hopfion along a
plane that contains the z axis, e. g. the yz plane, one can see
the texture of the skyrmion tube that forms the hopfion. How-

3

β,γ

(a)

(b)
10

Z
R

5
Energy [eV]

ever, as explained before, it is actually an in-plane magnetized skyrmion, which is called bimeron, and since the torus
is cut twice by the plane, we see two bimerons in Fig. 1(d).
In Sec. III B we will show that the orbital Hall response of a
hopfion is related to the orbital Hall responses of these twodimensional textures.
An explanation will be provided on the basis of the emergent field of a magnetic texture that is a quantity that determines its topological Hall transport and orbital Hall transport.
Its α = x, y, z component is defined as [12]


1X
∂m(r) ∂m(r)
Bem,α (r) =
ϵαβγ m(r) ·
×
.
2
∂β
∂γ

A
0

ΩΩLxyxyz
Lz

kz

2.0

+

1.5

X

-5

1.0

M

0.5

00

-10

(2)
The emergent field of a hopfion is shown in Fig. 1(b). Unlike
for the two-dimensional textures discussed before, it is noncollinear and has a toroidal configuration in the hopfion torus.
In the center of the hopfion it points out of the torus plane. On
average, the emergent field of the hopfion is compensated.
Two-dimensional topological textures, like magnetic
skyrmions, bimerons and skyrmioniums that constitute cuts
of the hopfion are characterized by the topological charge


Z
1
∂m(r) ∂m(r)
NSk =
m(r) ·
×
d2 r.
(3)
4π
∂β
∂γ
Here we have assumed that the texture changes in the βγ
plane and is constant along α. In this case, the topological
charge NSk is the integral of the perpendicular emergent field
Bem,α (r) over the whole texture. While a skyrmion and a
bimeron tube are characterized by a non-trivial topological
invariant NSk = ±1, the two-dimensional cuts through the
hopfion always contain two skyrmions or two bimerons with
opposite topological charges. Therefore, the skyrmionium in
Fig. 1(c) and the pair of bimerons in Fig. 1(d) are topologically trivial, NSk = 0.
A hopfion is a three-dimensional texture. Therefore, it is
not reasonable to characterize it by the topological charge NSk
as defined above. Still, the emergent field is important to characterize its topology. A hopfion is characterized by the Hopf
index [83–85]
Z
1
NH = −
B em (r) · A(r) d3 r.
(4)
(4π)2
It is NH = ±1 depending on the type of hopfion and is calculated from the emergent field B em (r) and the corresponding
vector potential A(r). Like every vector potential it is not
gauge invariant and fulfills ∇ × A = B em . The emergent
field and the Hopf index are gauge-invariant. So far, the role
of the Hopf index has only been discussed in terms of topological stability of the hopfion but not in terms of transport
properties. This is the purpose of this work as we identify the
unique orbital Hall response caused by hopfions.
Although the textures as defined throughout this section are
continuous functions of the position vector r, for the tightbinding calculations we consider a discrete lattice. Therefore, the texture m(r) is rather a set of magnetic moments

0.00 0.05 0.10 0.15
DOS

kx

ky

FIG. 2. Electronic properties caused by a hopfion with m = 7t.
(a) Density of states [Eq. (9)] (blue) and comparison to the density
of states without the hopfion (gray). (b) Slices of the orbital Berry
z
curvature ΩL
ν,xy (k) of the lowest band ν = 1.

{mi }i=1,...,N that are defined at the sites {r i }i=1,...,N . Since
the calculation of a three-dimensional magnetic texture is
computationally demanding, we are restricted when choosing
appropriate hopfion sizes for the calculations. Here we use a
unit cell consisting of N = 256 magnetic moments which is
enough to capture the topological properties of the hopfion as
well as of the skyrmionium and bimerons accurately.
B.

Calculation of Hall conductivities

The electronic Hamiltonian is based on a tight-binding approach and is written here in second quantization [75, 86–89]
X †
X
H = −t
ci cj + m
mi · (c†i σci ).
(5)
⟨ij⟩

i

c†i and ci are the creation and annihilation operators of an s
electron at site i. σ is the vector of Pauli matrices. The Hamiltonian has the dimension 2N × 2N .
The first term describes the kinetic energy of the conduction
electrons via hopping terms of the form −t exp[ik · (r i − r j )].
Here, k is the wave vector and r i − r j the hopping path. For
the hopping amplitude we choose t = 1 eV and for the lattice
constant a = 2.76 Å. We consider a three-dimensional cubic
lattice. The second term describes the coupling of the conduction electrons with the magnetic texture {mi } that is formed
by energetically lower states; e. g. by d electrons. Throughout this paper, we consider two cases: (i) the adiabatic limit
where the conduction electrons’ spins align almost perfectly
with the texture (here m = 7t), and the weak-coupling case,
where spin parallel and antiparallel states are hybridized (here
m = 2t).
Eq. (5) is the so-called sd-Hamiltonian in which only s
electrons are considered explicitly and d electrons enter only

4

This equation assumes temperature T = 0 and is a function
of the Fermi energy EF . We integrate over the orbital Berry
curvature
X ⟨νk|j Lz |µk⟩⟨µk|vy |νk⟩
x
2
z
. (7)
ΩL
ν,xy (k) = −2ℏ Im
(Eνk − Eµk )2
µ̸=ν

Although the electronic transport is determined by all occupied states, the influence of the d electrons is negligible because they are fully occupied and far away from the s states
near the Fermi level. For calculating the orbital Hall conductivity at finite temperatures T > 0, the orbital Berry curvature
is weighted by the Fermi-Dirac distribution function in the energy integral.
1 ∂H
We use the velocity operator vl
=
ℏ ∂kl
Lz
=
and
P the orbital current operator ⟨νk|jx |µk⟩
1
[⟨νk|v
|αk⟩⟨αk|L
|µk⟩
+
⟨νk|L
|αk⟩⟨αk|v
x
z
z
x |µk⟩].
α
2
The orbital angular momentum


eℏ2 X
1
1
⟨νk|Lz |αk⟩ = i
+
4gL µB
Eβk − Eνk
Eβk − Eαk

z
y
Lz

x

j Lz

Lx

E

j Lx

E

(a)

(b)
10

10

5

5
kBT

Energy [eV]

Energy [eV]

via their magnetic texture {mi }. This Hamiltonian is suitable for analyzing topological transport phenomena [75, 86–
89] and has the advantage that spin-orbit coupling is zero, so
that the pure topological influence of the magnetic texture on
the Hall conductivities can be calculated. Note that spin-orbit
coupling is not required for the emergence of a topological
Hall effect, topological orbital Hall effect or topological spin
Hall effect [75].
We diagonalize the sd-Hamiltonian to numerically determine its eigensystem. The eigenvalues Eνk constitute the
band structure with band index ν = 1, ..., 2N . From the
eigenvectors |νk⟩ we calculate the Hall conductivities. The
orbital Hall transport is quantified by the orbital Hall conductivity [66]
Z
eX 1
Lz
σxy
ΩLz (k) d3 k. (6)
(EF ) =
ℏ ν (2π)3 Eνk ≤EF ν,xy

0

-5

-5

-10

-10

0

500

1000

0.0t
0.025t
0.1t

0

1500

0

L

Orbital Hall conductivity σyzx [e/2aπ]

Orbital Hall conductivity σxyz [e/2aπ]

500

1000

1500
L

FIG. 3. Three-dimensional orbital Hall effect caused by a hopfion in
the strong-coupling limit. (a) The orbital conductivity tensor element
Lz
as a function of energy. This orbital Hall conductivity characσxy
terizes a transport of orbital angular momentum Lz in the Hopfion
plane xy. Application of an electric field E along y gives rise to an
orbital current j Lz along x; see schematic image above. The orbital
angular momentum is polarized out of plane. (b) The equivalent reL
Lx
sults for the σyz
= σzxy tensor element. The Hund’s coupling is
characterized by m = 7t so that the conduction electrons’ spins almost completely align with the hopfion texture. The color of the
curve indicates the temperature; see legend.

β̸=ν,α

× (⟨νk|vx |βk⟩⟨βk|vy |αk⟩ − ⟨νk|vy |βk⟩⟨βk|vx |αk⟩) (8)
has been calculated based on the modern formulation [90–95]
and takes into account inter-site contributions [66] that are
not considered in the often used atomic-center approximation.
Using this more accurate description has been shown to be of
crucial importance for topologically non-trivial spin textures
such as skyrmions, as the orbital angular momentum and the
corresponding orbital Hall conductivity are caused by large
cyclotron orbits generated by the texture’s emergent magnetic
field [75].
Although the focus of this paper is on orbital transport, we
also briefly mention the topological Hall conductivity and spin
Hall conductivity, as defined in Ref. [75].
III.

RESULTS AND DISCUSSION

Next, we present the results of our calculations and begin with the orbital Hall signatures of hopfions in Sec. III A.

Afterwards, in Sec. III B, we compare them with the typical
Hall signatures of related non-collinear textures: 1. skyrmion
tubes, 2. bimeron tubes and 3. skyrmionium tubes. In
Sec. III C, we present how the energy dependence of the orbital Hall conductivities can be understood by analyzing the
carrier density and the emergent field of these textures.
A.

Orbital Hall transport of hopfions

Diagonalizing the Hamiltonian [Eq. (5)] and using the hopfion texture [Eq. (1)] results in the band structure describing
electrons interacting with a periodic array of hopfions. In the
strong-coupling case, where m = 7t, the band structure exhibits 2 blocks consisting of 256 bands each. The conduction
electron spins align locally parallel and anti-parallel with the
hopfion texture in the two blocks, respectively. The blocks
are centered around ±m and have a band width of almost 12t.
Due to the large number of bands, it is not helpful to look at
the band structure directly, as the bands are very dense.

5

Instead, the density of states, shown in Fig. 2(a) for the
strong-coupling case m = 7t, reveals better how the states
are distributed in energy. This function quantifies the states in
an energy interval around E
Z
1 X
δ(E − Eνk ) d3 k.
(9)
DOS(E) =
(2π)3 ν
Near the band edges, we see an increase and a rather constant plateau near the centers of the blocks around ±m. The
density of states (blue) agrees rather well with the density
of states of the band structure that characterizes the underlying square lattice (gray). It consists of 2 bands that we have
shifted by ±m

(a)

(b)
10

10

5

5
Energy [eV]

Density of states

Energy [eV]

1.

0

-5

-10

-10

500

1000

1500

0

L

Orbital Hall conductivity σyzx [e/2aπ]

Orbital Hall conductivity σxyz [e/2aπ]

E3D (k) = −2t[cos(kx a) + cos(ky a) + cos(kz a)] ± m.
(10)
Due to the topological properties of the hopfion texture, an
emergent field arises that acts just like an actual magnetic
field that couples to the charge of the electrons. For a twodimensional system, like a thin sample hosting skyrmions, it
leads to the emergence of Landau levels whose energy is determined by the density of states [96] according to Onsager’s
quantization scheme [97]. Even though here the discussion
is more difficult, due to the three-dimensional nature of the
system and the globally compensated emergent field, we still
find that the density of states of the magnetic system (hosting a hopfion) and the non-magnetic system (characterized by
E3D (k)) are relatable.
In summary, the band structure exhibits a dense collection
of bands whose density of states agrees well with the density
of states of the non-magnetic system. The two cosine-shaped
bands of the cubic lattice condense to many rather flat bands
because of the emergent field of the hopfion. Next, we analyze the orbital Hall conductivity that is determined by the
eigenvectors that are affected by the emergent field as well.
2.

Orbital Hall transport

The bands exhibit non-vanishing orbital angular momenta
that have been calculated based on the modern formulation of
orbital magnetization [Eq. (8)]. Also, the hopfion gives rise
to a net orbital Berry curvature [shown in Fig. 2(b) for the
strong-coupling case m = 7t] that causes an orbital Hall conductivity; cf. Fig. 3. Interestingly, since the emergent field
[Fig. 1(b)] has components in all directions in space, not only
Lz
Lz
the orbital Hall tensor elements σxy
= −σyx
[presented in
Lx
Lx
Fig. 3(a)] are non-zero but also the elements σyz
= −σzy
=
L

L

σzxy = −σxzy [presented in Fig. 3(b)]. This is unlike the
orbital Hall effect of any two-dimensional texture in the xy
plane, which can only exhibit the orbital Hall conductivity
Lz
Lz
σxy
= −σyx
, as discussed in more detail in Sec. III B. Therefore, we call this unique signature of the hopfion the threedimensional orbital Hall effect.

0.0t
0.025t
0.1t

0

-5

0

kBT

500

1000

1500
L

FIG. 4. Three-dimensional orbital Hall effect caused by a hopfion in
the weak-coupling limit. The figure is analogue to Fig. 3 but with
a weaker Hund’s coupling of m = 2t. (a) The orbital conductivity
L
Lz
Lx
tensor element σxy
and (b) the tensor element σyz
= σzxy are shown
as a function of energy for various temperatures.

The presence of an orbital Hall effect is not related to the finite size of the hopfion but can be expected even for a perfectly
smooth texture because the orbital Hall conductivity is known
to be insensitive to the sign of the emergent field [75]. For
this reason, any texture with an emergent field can give rise
to an orbital Hall effect even if it is compensated on average.
We have recently demonstrated this for an antiferromagnetic
skyrmion which consists of 2 sublattices with opposite emergent fields. These opposite fields cause the same orbital Hall
conductivity because they give rise to opposite orbital angular
momenta and opposite charge Hall transport [75].
The energy-dependent curves in Fig. 3(a,b) look rather similar for both tensor components except for a difference in magnitude. Furthermore, they are almost identical for the upper
and lower block in energy and the signal is symmetric within
each block, starting at zero near the band edges and exhibiting a maximum near the center of each block. A detailed
analysis of the energy dependence of these orbital conductivities and their relation to the emergent field follows later
in Sec. III C. The magnitude of the orbital Hall conductivity
2
scales with the component of 1/ ⟨Bem,α
⟩ that is perpendicular to the plane of transport. Here, the bracket indicates an
average over the whole hopfion. The hopfion has a larger
2
out-of-plane component ⟨Bem,z
⟩ than the in-plane compo2
2
Lx
nents ⟨Bem,x ⟩ = ⟨Bem,y ⟩, which is why σyz
[presented in
Lz
Fig. 3(b)] is larger than σxy [presented in Fig. 3(a)] with maxe
e
imum value of ∼ 1500 2aπ
and ∼ 1200 2aπ
, respectively.
The orbital Hall conductivity for the weak-coupling case,
m = 2t, is shown in Fig. 4. We see the same tensor components as before but there is no separation into two blocks
anymore. Instead, spin parallel and antiparallel states that feel
opposite emergent fields are hybridized. However, since opposite emergent fields result in the same orbital Hall response,

6
this still leads to a considerable orbital Hall effect, even in
the weak-coupling limit. In fact, for some energies, the orbital Hall conductivity is even larger for m = 2t than in the
strong coupling case m = 7t. This is because the density
of states is larger when there is no formation of two separate
spin-polarized blocks in the band structure.
Lz
When comparing the in-plane orbital Hall conductivity σxy
Lx
in Fig. 4(a) with the out-of-plane orbital Hall conductivity σyz
in Fig. 4(b), we see similar energy dependencies but different peak structures near E = 0. For a smooth and infinitely
large texture with a homogeneous emergent field, we would
expect qualitatively equal curves. However, because of the finite size of the hopfion, differences occur near the center of
the energy range. Here electron-like spin parallel states hybridize with hole-like spin antiparallel states which is why
small changes or inhomogeneities in the emergent field can
lead to quite strong changes in the orbital Hall conductivities.
So far, we have discussed only one type of hopfion. We
have repeated our calculations from the strong-coupling limit,
m = 7t presented in Fig. 3, for different types of hopfions. By reversing mz , the Hopf index and the emergent field
change sign. As a consequence, the band structure changes
Eν (kx , ky , kz ) → Eν (kx , ky , −kz ). However, all orbital Hall
conductivity tensor elements remain unaffected by the change
of the Hopf index. The same happens when we reverse an inplane component, say mx , instead. Due to the opposite winding, the Hopf index and the emergent field change sign but
the orbital Hall conductivity is unaffected. This fits well the
explanation that the orbital Hall conductivity is caused by the
square of the emergent field, which is not sign-sensitive. We
will elaborate on this explanation in more detail in Sec. III C.
Before we continue, we would like to note that the bands
also exhibit a finite Berry curvature and spin Berry curvature
that give rise to a small topological Hall effect and spin Hall
effect, respectively. A smooth hopfion texture has a globally
compensated emergent field and so these effects are not expected. In our calculations, they occur because of the finite
size of the hopfion that is limited by the computation time.
The hopfion texture is not exactly smooth, which is why we
find a finite topological Hall and spin Hall conductivity near
the band edges. However, these signals are weak when we
compare them to other textures such as skyrmion tubes; cf.
Sec. III B. The effects would disappear for larger hopfion sizes
λ/a → ∞.

two bimerons; cf. Fig. 1(d). When a hopfion is cut along the
xy plane instead, the resulting texture is a skyrmionium; cf.
Fig. 1(c). Therefore, the results for the bimeron and for the
skyrmionium tube will help us to better understand the orbital
Hall signatures of the hopfion.

1.

Skyrmion tube

The first comparison with a two-dimensional texture that
comes to mind is to relate our findings to the orbital Hall response of a skyrmion tube. This texture [Fig. 5(a)] exhibits a
topologically non-trivial configuration in the two-dimensional
xy plane that is continued along the z direction. The corresponding emergent field [Fig. 5(b)] is collinear and points
along z because the texture only changes along the xy plane.
Lz
Lz
We find a sizable σxy
= −σyx
orbital conductivity tensor element [Fig. 5(c) for the strong coupling case m = 7t]
that exhibits a similar energy dependence as for the hopfion;
e
cf. with Fig. 3(a). The maximum is smaller with ∼ 650 2aπ
2
which is due to the larger emergent field component ⟨Bem,z ⟩
L

Lx
Lx
, σzxy
compared to the hopfion. The tensor elements σyz
, σzy
L
and σxzy that were all finite for the hopfion are now zero due
2
2
⟩ = 0. Instead, we find a non-zero topo⟩ = ⟨Bem,y
to ⟨Bem,x

logical Hall conductivity σxy = −σyx , presented in Fig. 5(d),
that was negligible for the hopfion. This is because the topolgical Hall effect scales with the average emergent field and
⟨Bem,z ⟩ is finite for the skyrmion while it is compensated for
the hopfion.
The emergent field gives rise to Landau levels that cause
a topological Hall effect and also an orbital Hall effect, as
shown previously for a skyrmion system [75] in analogy to a
quantum Hall system [74]. We have analyzed the Hall conductivities of a skyrmion texture in Ref. [75] but in a twodimensional system. The results presented in Fig. 5 differ
from these because here we consider skyrmion tubes that
extend infinitely along the z direction. Landau levels that
are rather flat in the kx ky plane have dispersion along the
kz direction because of the hopping of electrons along the
skyrmion tube direction. This leads, for example, to the different band width and the missing quantization in the topological
Hall conductivity in Fig. 5(d) in comparison to Ref. [75].
In summary, a skyrmion tube exhibits a similar orbital
Lz
Hall conductivity σxy
as a hopfion but a hopfion exhibits
L

B.

Comparison with related non-collinear textures

Before we dissect the origin of the orbital Hall effect in
more detail, first we want to compare our calculations with
those for related non-collinear spin textures: 1. skyrmion
tubes, 2. bimeron tubes and 3. skyrmionium tubes. We analyze their orbital Hall conductivities because a hopfion can
be understood as a bimeron tube that has been twisted and
closed to form a torus. This bimeron tube is topologically
equivalent to a skyrmion tube, because a bimeron is essentially a skyrmion in an in-plane magnet. For this reason, cutting a hopfion along a plane containing the z axis results in

Lx
an additional σyz
and σzxy orbital Hall conductivity. A
skyrmion on the other side exhibits a sizable topological Hall
response in the σxy tensor element which is negligible for
hopfions. Therefore, skyrmions and hopfions can be nicely
distinguished in transport experiments.

2.

Bimeron tube

The cross section of the hopfion torus consists of two inplane skyrmions, also called bimerons. In fact, a hopfion is
just a bimeron tube that has been twisted and closed to form
a torus. Furthermore, a bimeron is topologically equivalent

7
(b)

(c)

Bem(x,y,z)

Energy [eV]

m(x,y,z)

z

10

10

5

5
kBT

0.0t
0.025t
0.1t

0

0

-5

-5

-10

-10

z
y

x

(d)

Energy [eV]

(a)

y
x

0

200

400

600
L

800

Orbital Hall conductivity σxyz [e/2aπ]

-10

-5

0

5

10

σxyz Hall conductivity σxy [e2 /ha]σxyz
L

L

FIG. 5. Orbital Hall effect and topological Hall effect caused by a skyrmion tube. (a) Magnetic texture of the skyrmion tube. The color
indicates the orientation of the magnetic moments as in Fig. 1. (b) Corresponding emergent field that is collinear and points along the tube
Lz
direction. (c) Orbital Hall conductivity σxy
as a function of energy. (d) Topological Hall conductivity σxy as a function of energy. The color
of the curve indicates the temperature; see legend. The Hund’s coupling is characterized by m = 7t.

to a skyrmion, so it is natural to analyze the Hall transport of
bimerons tubes next. The tube is chosen to extend along x to
resemble one of the torus plane directions.
Lx
is shown in Fig. 6(b) as
The orbital Hall conductivity σyz
a function of energy. It is exactly the same as the orbital
Lz
Hall conductivity σxy
of a skyrmion tube that is shown in
Fig. 5(c) and was discussed before. The reason is that we
have constructed the bimeron such that it has the same profile
as the skyrmion. The two textures can be transformed from
one to another by spin rotations of 90◦ . Since the emergent
field is invariant under collective spin rotations, bimerons and
skyrmions exhibit the same emergent field. The only difference is that we have constructed the tubes along different directions (z for the skyrmion and x for the bimeron), which
is why the two textures exhibit different orbital conductivity
tensor elements.
Any cross section of a hopfion that contains the z axis consists of two bimerons with opposite emergent fields. As we
have shown now, such bimerons give rise to an orbital Hall
conductivity along the bimeron plane. The response is the
same for both bimerons, as the orbital Hall effect is insensitive to the sign of the emergent field. Each bimeron also
exhibits a topological Hall conductivity σyz . However, it is
exactly opposite for the two bimerons and cancels in total due
to the opposite emergent fields.
In summary, a pair of oppositely magnetized bimeron tubes
exhibits only an orbital Hall effect in the plane perpendicular
to the tube direction. This explains why a hopfion exhibits
L
L
Lx
Lx
orbital conductivity tensor elements σyz
, σzy
, σzxy and σxzy
and why it does not exhibit a sizable topological Hall effect
along these planes. Even the energy-dependencies of the orbital Hall conductivities exhibit a similar shape [cf. Fig. 3(b)

and Fig. 6(b)] but with a different maximum due to the dif2
2
ferent average emergent field ⟨Bem,x
⟩ and ⟨Bem,y
⟩ of the two
textures.

3.

Skyrmionium tube

If a hopfion is cut horizontally, the resulting texture is a
skyrmionium. This two-dimensional texture consists of a
skyrmion that is positioned at the center of another skyrmion
with opposite topological charge. The total topological charge
is compensated and therefore the average emergent field is
zero. However, since the two subskyrmions exhibit out-ofplane emergent fields, a skyrmionium exhibits an average
2
⟨Bem,z
⟩. Here we consider a skyrmionium tube where the
two-dimensional skyrmionium texture has been extended trivially along the z direction.
The skyrmionium tube exhibits an orbital Hall conductivLz
ity σxy
that is shown in Fig. 6(a). Due to the small size of the
skyrmionium and the inhomogeneity of the emergent field, the
curve is more noisy but in general has a similar energy dependence as all orbital Hall conductivities discussed before. This
result for the skyrmionium allows us to understand why the
hopfion exhibits an orbital Hall conductivity tensor element
Lz
σxy
; cf. Fig. 3(a). Both, the skyrmionium and the hopfion, do
not exhibit a sizable topological Hall conductivity σxy due to
the compensated emergent field, on average.

8
(a)

(b)

z
z

y
x

x

10

10

5

5
kBT

Energy [eV]

Energy [eV]

y

0.0t
0.025t
0.1t

0

0

-5

-5

-10

-10

0

200

400

600

800

L
Orbital Hall conductivity σxyz [e/2aπ]

0

200

400

600

800

L
Orbital Hall conductivity σyzx [e/2aπ]

FIG. 6. Orbital Hall effect caused by two-dimensional textures related to a hopfion. (a) Top: Magnetic texture of a magnetic skyrmionium tube. The color indicates the orientation of the magnetic moLz
ments as in Fig. 1. Bottom: Orbital Hall conductivity σxy
as a function of energy. The color of the curve indicates the temperature; see
legend. (b) Calculations for a magnetic bimeron tube. Here, the tenLx
is non-zero. The Hund’s coupling is characterized
sor element σyz
by m = 7t.

4.

Summary

In summary, the three-dimensional orbital Hall response
of a hopfion can be understood by analyzing the twodimensional textures that appear when the hopfion is cut along
a two-dimensional plane: A cut along the xy plane reveals a
skyrmionium that exhibits only an orbital Hall conductivity
Lz
σxy
and no corresponding topological Hall conductivity. A
cut along the yz plane reveals a pair of bimerons that only
Lx
give rise to an orbital Hall conductivity σyz
and not to a corresponding topological Hall conductivity. An equivalent reL
sult for σzxy can be found for the pair of bimerons that appear
when cutting the hopfion along the zx plane.

2
component squared ⟨Bem,α
⟩. This is because the emergent
field causes the transverse transport of electronic states and
also causes their orbital polarization. In a two-current model,
oppositely orbital polarized states move along opposite directions and give rise to a net orbital current that is independent
of the sign of the emergent field.
The recurring energy dependence is determined by the band
structure of the underlying cubic lattice. We have already
briefly identified the role of this band structure for the distribution of the electronic states in energy by discussing the
density of states in Sec. III A and we will do so in more detail
in the following.
As we have established in a previous work on magnetic
skyrmions [75], the energy dependencies of the charge, spin
and orbital Hall conductivities can
R be approximated dby the
1
density of states n′dD (E) = (2π)
δ(E − EdD (k)) d k and
d
RE ′
the carrier density ndD (E) = κ(E)
ndD (E ′ ) dE ′ calculated from the band structure of the underlying lattice EdD (k).
Here, κ(E) = ±1 is determined by the electronic character of
the Fermi line: electron-like (+1) vs hole-like (−1). In that
reference, a two-dimensional system, d = 2, in the xy plane
with an emergent field along z had been considered, and we
found that the orbital Hall conductivity can be approximated
as
[n2D (E)]2
1
Lz
σxy,approx,2D
(E) ∝
.
(11)
2
n′2D (E) ⟨Bem,z
⟩

Here, we generalize these findings of the two-dimensional
system to explain the results of three-dimensional systems,
d = 3, that were shown in Sec. III A. As an example, we
Lz
2
discuss σxy
that is determined by ⟨Bem,z
⟩. The other tensor
elements can be calculated analogously by rotating the coordinate system.
When transitioning from the two-dimensional system to the three-dimensional system, the band structure
of the underlying lattice changes from E2D (kx , ky ) =
−2t [cos(kx a) + cos(ky a)]
to
E3D (kx , ky , kz )
=
−2t [cos(kx a) + cos(ky a) + cos(kz a)], so in this particular case E3D (kx , ky , kz ) = E2D (kx , ky ) − 2t cos(kz a).
However, because the transverse transport occurs in the
plane perpendicular to B em (here the xy plane), we cannot
simply replace the density of states and carrier density of the
two-dimensional system with those of the three-dimensional
system. Instead, we consider a modified density of states, the
kz -resolved density of states
Z
1
n′ (E, kz ) =
δ(E − E3D (kx , ky , kz )) dkx dky
(2π)3
(12)
and carrier density
Z E

C.

Approximating the orbital Hall conductivities

As discussed in the previous sections, all non-zero orbital
Hall conductivities of the various textures exhibit a similar
energy dependence only with different magnitudes. The magLα
nitude of σβγ
is determined by the average emergent field

n(E, kz ) = κ(E, kz )

n′ (E ′ , kz ) dE ′

(13)

and integrate over the k direction along B em (here along kz ).
The resulting orbital Hall conductivity
Z
[n(E, kz )]2
1
Lz
σxy,approx,3D
(E) ∝
dkz .
(14)
2
⟨Bem,z ⟩
n′ (E, kz )

9

10

10

5
Energy [eV]

5
Energy [eV]

conductivity and the spin Hall conductivity as
Z
1
σxy,approx,3D (E) ∝ ±
n(E, kz ) dkz ,
⟨Bem,z ⟩
Z
1
Sz
σxy,approx,3D
(E) ∝
n(E, kz ) dkz ,
⟨Bem,z ⟩

0

0

-5

-5

-10

-10

0.0

0.1

0.2

0.3

0.4

0.5

L
Orbital Hall conductivity σapprox
[a.u.]

-0.2

-0.1

0.0

0.1

0.2

Hall conductivity σapprox [a.u.]

FIG. 7. Approximation of energy-dependent Hall conductivities for
textures with a finite emergent field in the strong-coupling limit. (a)
L
Orbital Hall conductivity σapprox
with the orbital angular momentum
L along the emergent field and the electric field and the transverse
orbital current in the plane perpendicular to it. (b) Topological Hall
conductivity σapprox in the plane perpendicular to the emergent field.
The Hund’s coupling is m = 7t so that the conduction electrons’
spins can be assumed to align with the magnetic texture.

is shown in Fig. 7(a) and resembles the previously calculated
orbital Hall conductivities of the various non-collinear magnetic textures well; cf. Figs. 3(a,b), 5(c), 6(a,b).
The results of the full quantum-mechanical calculations
are especially well reproduced for the skyrmion tube and the
bimeron tube; cf. Figs. 5(c), 6(b). For these textures, the
emergent field is rather smooth and does not change along
the tube direction, so that the assumptions of the approximation are well fulfilled: The electronic states are distributed according to the density of states of the underlying lattice and
the orbital Berry curvature does not change much along the
k direction that is along the direction perpendicular to the
Lz
Hall transport. As another example, the hopfion’s σxy
component [Fig. 3(a)] is also nicely approximated but there are
small deviations. These occur because the emergent field is
z
less smooth [Figs. 1(b)] and the orbital Berry curvature ΩL
xy
varies slightly along kz [Figs. 2(b)].
Overall, we have achieved a good semi-classical understanding of the orbital Hall effect in these three-dimensional
Lα
systems. The magnitude of σβγ
is determined by the aver2
age emergent field ⟨Bem,α
⟩ and the energy dependence can
be reconstructed based on the zero-field band structure of the
underlying lattice E3D (k). For the textures with a finite topological charge NSk (in this paper the skyrmion tube and the
bimeron tube), we can also approximate the topolgical Hall

(15)
(16)

by generalizing the two-dimensional formulas from Ref. [75]
in the same way as for the orbital Hall conductivity before.
The result for the topological Hall conductivity is shown in
Fig. 7(b) and reproduces the results of the full calculation very
well; cf. Fig. 5(d).
Our analysis allows the understanding of the functional
dependencies of the Hall conductivities presented throughout this paper. For the following discussion we consider the
states with negative energy in Fig. 7. The topological Hall
conductivity, shown in panel (b), characterizes charge transport. The energetically lower states are electron-like and the
higher states of each block are hole-like; the effective mass
changes sign and the states are affected oppositely by the
(emergent) magnetic field. Consequently, σapprox (E) exhibits
a sign change and has two extrema. However, the orbital Hall
conductivity, shown in panel (a), characterizes transport of orbital angular momentum. The orbital angular momentum of
a Bloch state is also dependent on the effective mass. Therefore, electron-like and hole-like states behave equally in terms
L
of the orbital Hall transport. Consequently, σapprox
(E) does
not change sign and exhibits only one extremum. By the same
arguments, we can understand that the orbital Hall conductivity is an even function of the (emergent) magnetic field, while
the topological Hall effect is odd [74, 75].

IV.

CONCLUSION

In summary, we have shown that a hopfion exhibits a threedimensional topological orbital Hall effect. The emergent
field itself is large within the hopfion but is compensated on
a global level which is why the charge and spin Hall conductivities are almost compensated. The square of the emergent
field, however, is finite on average and causes the orbital Hall
effect, which can be seen as a unique signature of the hopfion
phase: Since the hopfion is an innately three-dimensional texL
Lz
Lx
ture, it exhibits multiple tensor elements σxy
, σyz
and σzxy
[cf. Fig. 3], whereas a skyrmion tube, for example, is continued trivially along the tube direction and exhibits only an
orbital Hall transport within the skyrmion plane.
Two-dimensional textures, such as skyrmions, are characterized by the topological charge NSk that determines their
topological Hall transport. The hopfion is a three-dimensional
magnetic texture that is topologically characterized by the
Hopf index. However, so far, the significance of this topological invariant for a hopfion’s emergent electrodynamics has not
been known. Here we have shown that the three-dimensional
orbital Hall response of a hopfion can be seen as a signature
of the Hopf index. All results presented in this paper can be
interpreted based on the emergent field of the texture which,
in turn, determines its topological invariant.

10
Our findings present a reliable hallmark for identifying hopfions in experiments. This was difficult so far, because the
commonly used real-space techniques like LTEM penetrate
the sample and result in a projected image of the texture that
can hardly be distinguished from a skyrmionium. Measuring the orbital response of hopfions presents an alternative to
difficult and expensive holography and tomography measure-

ments [38–45]. Furthermore, hopfions can serve as generators of large orbital currents that can give rise to large torques
which are needed for spin-orbitronic devices.
Acknowledgements — This work was supported by the
EIC Pathfinder OPEN grant 101129641 “Orbital Engineering
for Innovative Electronics”.
Data Availability — The data that support the findings of
this article are openly available [98].

[1] B. Göbel, I. Mertig, and O. A. Tretiakov, Beyond skyrmions:
Review and perspectives of alternative magnetic quasiparticles,
Physics Reports 895, 1 (2021).
[2] A. Bogdanov and D. Yablonskii, Thermodynamically stable
vortices in magnetically ordered crystals. the mixed state of
magnets, Zh. Eksp. Teor. Fiz 95, 182 (1989).
[3] S. Mühlbauer, B. Binz, F. Jonietz, C. Pfleiderer, A. Rosch,
A. Neubauer, R. Georgii, and P. Böni, Skyrmion lattice in a
chiral magnet, Science 323, 915 (2009).
[4] X. Yu, Y. Onose, N. Kanazawa, J. Park, J. Han, Y. Matsui,
N. Nagaosa, and Y. Tokura, Real-space observation of a twodimensional skyrmion crystal, Nature 465, 901 (2010).
[5] N. Nagaosa, J. Sinova, S. Onoda, A. H. MacDonald, and N. P.
Ong, Anomalous Hall effect, Rev. Mod. Phys. 82, 1539 (2010).
[6] A. K. Nayak, V. Kumar, T. Ma, P. Werner, E. Pippel, R. Sahoo,
F. Damay, U. K. Rößler, C. Felser, and S. S. Parkin, Magnetic
antiskyrmions above room temperature in tetragonal Heusler
materials, Nature 548, 561 (2017).
[7] L. Peng, R. Takagi, W. Koshibae, K. Shibata, K. Nakajima, T.h. Arima, N. Nagaosa, S. Seki, X. Yu, and Y. Tokura, Controlled transformation of skyrmions and antiskyrmions in a noncentrosymmetric magnet, Nature Nanotechnol. 15, 181 (2020).
[8] J. Jena, B. Göbel, T. Ma, V. Kumar, R. Saha, I. Mertig,
C. Felser, and S. S. Parkin, Elliptical Bloch skyrmion chiral
twins in an antiskyrmion system, Nature Comms. 11, 1115
(2020).
[9] Y. Kharkov, O. Sushkov, and M. Mostovoy, Bound states of
skyrmions and merons near the Lifshitz point, Phys. Rev. Lett.
119, 207201 (2017).
[10] B. Göbel, A. Mook, J. Henk, I. Mertig, and O. A. Tretiakov,
Magnetic bimerons as skyrmion analogues in in-plane magnets,
Phys. Rev. B 99, 060407 (2019).
[11] N. Gao, S.-G. Je, M.-Y. Im, J. W. Choi, M. Yang, Q.-c. Li,
T. Wang, S. Lee, H.-S. Han, K.-S. Lee, et al., Creation and
annihilation of topological meron pairs in in-plane magnetized
films, Nature Comms. 10, 5603 (2019).
[12] N. Nagaosa and Y. Tokura, Topological properties and dynamics of magnetic skyrmions, Nature Nanotechnol. 8, 899 (2013).
[13] P. Bruno, V. Dugaev, and M. Taillefumier, Topological Hall effect and Berry phase in magnetic nanostructures, Phys. Rev.
Lett. 93, 096806 (2004).
[14] A. Neubauer, C. Pfleiderer, B. Binz, A. Rosch, R. Ritz,
P. Niklowitz, and P. Böni, Topological Hall effect in the A phase
of MnSi, Phys. Rev. Lett. 102, 186602 (2009).
[15] M. Lee, W. Kang, Y. Onose, Y. Tokura, and N. Ong, Unusual
Hall effect anomaly in MnSi under pressure, Phys. Rev. Lett.
102, 186601 (2009).
[16] M. Raju, A. Petrović, A. Yagil, K. Denisov, N. Duong,
B. Göbel, E. Şaşıoğlu, O. Auslaender, I. Mertig, I. Rozhansky, et al., Colossal topological hall effect at the transition between isolated and lattice-phase interfacial skyrmions, Nature

Comms. 12, 2758 (2021).
[17] B. Göbel, A. Mook, J. Henk, and I. Mertig, Antiferromagnetic
skyrmion crystals: Generation, topological Hall, and topological spin Hall effect, Phys. Rev. B 96, 060406 (2017).
[18] B. Göbel, A. Mook, J. Henk, and I. Mertig, The family of
topological Hall effects for electrons in skyrmion crystals, Eur.
Phys. J. B 91, 179 (2018).
[19] B. Göbel, A. Schäffer, J. Berakdar, I. Mertig, and S. Parkin,
Electrical writing, deleting, reading, and moving of magnetic
skyrmioniums in a racetrack device, Scientific Reports 9, 12119
(2019).
[20] P. K. Sivakumar, B. Göbel, E. Lesne, A. Markou, J. Gidugu,
J. M. Taylor, H. Deniz, J. Jena, C. Felser, I. Mertig, et al.,
Topological Hall signatures of two chiral spin textures hosted
in a single tetragonal inverse Heusler thin film, ACS Nano 14,
13463 (2020).
[21] H. Hopf, Über die Abbildungen der dreidimensionalen Sphäre
auf die Kugelfläche, Math. Ann. 104, 637 (1931).
[22] V. E. Korepin and L. D. Faddeev, Quantization of solitons, Theoretical and Mathematical Physics 25, 1039 (1975).
[23] P. Sutcliffe, Vortex rings in ferromagnets: Numerical simulations of the time-dependent three-dimensional Landau-Lifshitz
equation, Phys. Rev. B 76, 184439 (2007).
[24] P. Sutcliffe, Skyrmion knots in frustrated magnets, Phys. Rev.
Lett. 118, 247203 (2017).
[25] P. Sutcliffe, Hopfions in chiral magnets, Journal of Physics A:
Mathematical and Theoretical 51, 375401 (2018).
[26] Y. Liu, R. K. Lake, and J. Zang, Binding a hopfion in a chiral
magnet nanodisk, Phys. Rev. B 98, 174437 (2018).
[27] J.-S. B. Tai, I. I. Smalyukh, et al., Static hopf solitons and knotted emergent fields in solid-state noncentrosymmetric magnetic
nanostructures, Phys. Rev. Lett. 121, 187201 (2018).
[28] X. Wang, A. Qaiumzadeh, and A. Brataas, Current-driven dynamics of magnetic hopfions, Phys. Rev. Lett. 123, 147203
(2019).
[29] B. Göbel, C. A. Akosa, G. Tatara, and I. Mertig, Topological
Hall signatures of magnetic hopfions, Phys. Rev. Res. 2, 013315
(2020).
[30] Y. Liu, W. Hou, X. Han, and J. Zang, Three-dimensional dynamics of a magnetic hopfion driven by spin transfer torque,
Phys. Rev. Lett. 124, 127204 (2020).
[31] D. Raftrey and P. Fischer, Field-driven dynamics of magnetic
hopfions, Phys. Rev. Lett. 127, 257201 (2021).
[32] N. Kent, N. Reynolds, D. Raftrey, I. T. Campbell, S. Virasawmy, S. Dhuey, R. V. Chopdekar, A. Hierro-Rodriguez,
A. Sorrentino, E. Pereiro, et al., Creation and observation of
hopfions in magnetic multilayer systems, Nature Comms. 12,
1562 (2021).
[33] F. N. Rybakov, N. S. Kiselev, A. B. Borisov, L. Döring,
C. Melcher, and S. Blügel, Magnetic hopfions in solids, APL
Materials 10, 111113 (2022).

11
[34] D. Popadiuk, E. Tartakovskaya, M. Krawczyk, and K. Guslienko, Emergent magnetic field and nonzero gyrovector of the
toroidal magnetic hopfion, physica status solidi (RRL)–Rapid
Research Letters 17, 2300131 (2023).
[35] F. Zheng, N. S. Kiselev, F. N. Rybakov, L. Yang, W. Shi,
S. Blügel, and R. E. Dunin-Borkowski, Hopfion rings in a cubic
chiral magnet, Nature 623, 718 (2023).
[36] X. Zhang, J. Xia, Y. Zhou, D. Wang, X. Liu, W. Zhao, and
M. Ezawa, Control and manipulation of a magnetic skyrmionium in nanostructures, Phys. Rev. B 94, 094420 (2016).
[37] S. Zhang, F. Kronast, G. van der Laan, and T. Hesjedal, Realspace observation of skyrmionium in a ferromagnet-magnetic
topological insulator heterostructure, Nano Letters 18, 1057
(2018).
[38] D. Wolf, N. Biziere, S. Sturm, D. Reyes, T. Wade, T. Niermann,
J. Krehl, B. Warot-Fonrose, B. Büchner, E. Snoeck, et al., Holographic vector field electron tomography of three-dimensional
nanomagnets, Communications Physics 2, 87 (2019).
[39] P. A. Midgley and R. E. Dunin-Borkowski, Electron tomography and holography in materials science, Nature Mater. 8, 271
(2009).
[40] A. Hierro-Rodrı́guez, C. Quirós, A. Sorrentino, L. M. ÁlvarezPrado, J. I. Martı́n, J. M. Alameda, S. McVitie, E. Pereiro,
M. Velez, and S. Ferrer, Revealing 3d magnetization of thin
films with soft x-ray tomography: magnetic singularities and
topological charges, Nature Comms. 11, 6382 (2020).
[41] D. Wolf, S. Schneider, U. K. Rößler, A. Kovács, M. Schmidt,
R. E. Dunin-Borkowski, B. Büchner, B. Rellinghaus, and
A. Lubk, Unveiling the three-dimensional magnetic texture of
skyrmion tubes, Nature Nanotechnol. 17, 250 (2022).
[42] S. Seki, M. Suzuki, M. Ishibashi, R. Takagi, N. Khanh, Y. Shiota, K. Shibata, W. Koshibae, Y. Tokura, and T. Ono, Direct visualization of the three-dimensional shape of skyrmion
strings in a noncentrosymmetric magnet, Nature Materials 21,
181 (2022).
[43] F. S. Yasin, J. Masell, Y. Takahashi, T. Akashi, N. Baba,
K. Karube, D. Shindo, T. Arima, Y. Taguchi, Y. Tokura, et al.,
Bloch point quadrupole constituting hybrid topological strings
revealed with electron holographic vector field tomography,
Advanced Materials 36, 2311737 (2024).
[44] M. Winterott and S. Lounis, Unlocking hidden potential in electron holography of non-collinear spin textures, arXiv preprint:
10.48550/arXiv.2502.18949 (2025).
[45] G. Gubbiotti, A. Barman, S. Ladak, C. Bran, D. Grundler,
M. Huth, H. Plank, G. Schmidt, S. Van Dijken, R. Streubel,
et al., 2025 roadmap on 3d nano-magnetism, Journal of
Physics: Condensed Matter 37, 143502 (2024).
[46] L. Levitov, Y. V. Nazarov, and G. Eliashberg, Magnetoelectric
effects in conductors with mirror isomer symmetry, Soviet Journal of Experimental and Theoretical Physics 61, 133 (1985).
[47] T. Yoda, T. Yokoyama, and S. Murakami, Current-induced orbital and spin magnetizations in crystals with helical structure,
Scientific Reports 5, 12024 (2015).
[48] T. Yoda, T. Yokoyama, and S. Murakami, Orbital Edelstein effect as a condensed-matter analog of solenoids, Nano Lett. 18,
916 (2018).
[49] D. Go, J.-P. Hanke, P. M. Buhl, F. Freimuth, G. Bihlmayer, H.W. Lee, Y. Mokrousov, and S. Blügel, Toward surface orbitronics: giant orbital magnetism from the orbital Rashba effect at
the surface of sp-metals, Scientific Reports 7, 46742 (2017).
[50] L. Salemi, M. Berritta, A. K. Nandy, and P. M. Oppeneer,
Orbitally dominated Rashba-Edelstein effect in noncentrosymmetric antiferromagnets, Nature Comms. 10, 5381 (2019).

[51] A. Johansson, B. Göbel, J. Henk, M. Bibes, and I. Mertig, Spin
and orbital Edelstein effects in a two-dimensional electron gas:
Theory and application to SrTiO3 interfaces, Phys. Rev. Res. 3,
013275 (2021).
[52] Y. Liu, J. Xiao, J. Koo, and B. Yan, Chirality-driven topological
electronic structure of DNA-like materials, Nature Mater. 20,
638 (2021).
[53] B. Kim, D. Shin, S. Namgung, N. Park, K.-W. Kim, and
J. Kim, Optoelectronic manifestation of orbital angular momentum driven by chiral hopping in helical se chains, ACS Nano 17,
18873 (2023).
[54] A. El Hamdi, J.-Y. Chauleau, M. Boselli, C. Thibault, C. Gorini,
A. Smogunov, C. Barreteau, S. Gariglio, J.-M. Triscone, and
M. Viret, Observation of the orbital inverse Rashba–Edelstein
effect, Nature Phys. 19, 1855 (2023).
[55] K. Hagiwara, Y.-J. Chen, D. Go, X. L. Tan, S. Grytsiuk, K.H. O. Yang, G.-J. Shu, J. Chien, Y.-H. Shen, X.-L. Huang,
et al., Orbital topology of chiral crystals for orbitronics, Advanced Materials , 2418040 (2025).
[56] J. M. Lee, M. J. Park, and H.-W. Lee, Orbital Edelstein effect of
electronic itinerant orbital motion at edges, Phys. Rev. B 110,
134436 (2024).
[57] B. Göbel, L. Schimpf, and I. Mertig, Chirality-induced orbital
Edelstein effect in an analytically solvable model, Phys. Rev.
Res. 7, 033180 (2025).
[58] B. Göbel, I. Mertig, and S. Lounis, Chirality-induced selectivity of angular momentum by orbital Edelstein effect in carbon
nanotubes, Communications Physics 8, 395 (2025).
[59] O. Busch, F. Ziolkowski, B. Göbel, I. Mertig, and J. Henk, Nonlinear spin and orbital Rashba-Edelstein effects induced by a
femtosecond laser pulse: Simulations for Au(001), Phys. Rev.
Res. 7, 043023 (2025).
[60] S. Zhang and Z. Yang, Intrinsic spin and orbital angular momentum Hall effect, Phys. Rev. Lett. 94, 066602 (2005).
[61] B. A. Bernevig, T. L. Hughes, and S.-C. Zhang, Orbitronics:
The intrinsic orbital current in p-doped silicon, Phys. Rev. Lett.
95, 066601 (2005).
[62] H. Kontani, T. Tanaka, D. Hirashima, K. Yamada, and J. Inoue,
Giant intrinsic spin and orbital Hall effects in Sr2 M O4 (M =
Ru, Rh, Mo), Phys. Rev. Lett. 100, 096601 (2008).
[63] T. Tanaka, H. Kontani, M. Naito, T. Naito, D. S. Hirashima,
K. Yamada, and J. Inoue, Intrinsic spin Hall effect and orbital
Hall effect in 4d and 5d transition metals, Phys. Rev. B 77,
165117 (2008).
[64] H. Kontani, T. Tanaka, D. Hirashima, K. Yamada, and J. Inoue,
Giant orbital Hall effect in transition metals: Origin of large
spin and anomalous Hall effects, Phys. Rev. Lett. 102, 016601
(2009).
[65] D. Go, D. Jo, C. Kim, and H.-W. Lee, Intrinsic spin and orbital
Hall effects from orbital texture, Phys. Rev. Lett. 121, 086602
(2018).
[66] A. Pezo, D. G. Ovalle, and A. Manchon, Orbital Hall effect in
crystals: Interatomic versus intra-atomic contributions, Phys.
Rev. B 106, 104414 (2022).
[67] L. M. Canonico, T. P. Cysne, A. Molina-Sanchez, R. Muniz,
and T. G. Rappoport, Orbital Hall insulating phase in transition
metal dichalcogenide monolayers, Phys. Rev. B 101, 161409
(2020).
[68] T. P. Cysne, S. Bhowal, G. Vignale, and T. G. Rappoport, Orbital Hall effect in bilayer transition metal dichalcogenides:
From the intra-atomic approximation to the Bloch states orbital
magnetic moment approach, Phys. Rev. B 105, 195421 (2022).
[69] L. Salemi and P. M. Oppeneer, Theory of magnetic spin and
orbital Hall and Nernst effects in bulk ferromagnets, Phys. Rev.

12
B 106, 024410 (2022).
[70] O. Busch, I. Mertig, and B. Göbel, Orbital Hall effect and
orbital edge states caused by s electrons, Phys. Rev. Res. 5,
043052 (2023).
[71] Y.-G. Choi, D. Jo, K.-H. Ko, D. Go, K.-H. Kim, H. G. Park,
C. Kim, B.-C. Min, G.-M. Choi, and H.-W. Lee, Observation of
the orbital Hall effect in a light metal Ti, Nature 619, 52 (2023).
[72] I. Lyalin, S. Alikhah, M. Berritta, P. M. Oppeneer, and R. K.
Kawakami, Magneto-optical detection of the orbital Hall effect
in chromium, Phys. Rev. Lett. 131, 156702 (2023).
[73] O. Busch, F. Ziolkowski, B. Göbel, I. Mertig, and J. Henk, Ultrafast orbital Hall effect in metallic nanoribbons, Phys. Rev.
Res. 6, 013208 (2024).
[74] B. Göbel and I. Mertig, Orbital Hall Effect Accompanying
Quantum Hall Effect: Landau Levels Cause Orbital Polarized
Edge Currents, Phys. Rev. Lett. 133, 146301 (2024).
[75] B. Göbel, L. Schimpf, and I. Mertig, Topological orbital Hall
effect caused by skyrmions and antiferromagnetic skyrmions,
Communications Physics 8, 17 (2025).
[76] M. d. S. Dias, J. Bouaziz, M. Bouhassoune, S. Blügel, and
S. Lounis, Chirality-driven orbital magnetic moments as a new
probe for topological magnetic structures, Nature Comms. 7,
13613 (2016).
[77] F. R. Lux, F. Freimuth, S. Blügel, and Y. Mokrousov, Engineering chiral and topological orbital magnetism of domain walls
and skyrmions, Communications Physics 1, 60 (2018).
[78] B. Göbel, A. Mook, J. Henk, and I. Mertig, Magnetoelectric
effect and orbital magnetization in skyrmion crystals: Detection and characterization of skyrmions, Phys. Rev. B 99, 060406
(2019).
[79] J. Barker and O. A. Tretiakov, Static and dynamical properties
of antiferromagnetic skyrmions in the presence of applied current and temperature, Phys. Rev. Lett. 116, 147203 (2016).
[80] X. Zhang, Y. Zhou, and M. Ezawa, Magnetic bilayer-skyrmions
without skyrmion Hall effect, Nature Comms. 7, 10293 (2016).
[81] X. Zhang, Y. Zhou, and M. Ezawa, Antiferromagnetic
skyrmion: stability, creation and manipulation, Scientific Reports 6, 24795 (2016).
[82] W. Legrand, D. Maccariello, F. Ajejas, S. Collin, A. Vecchiola, K. Bouzehouane, N. Reyren, V. Cros, and A. Fert, Roomtemperature stabilization of antiferromagnetic skyrmions in
synthetic antiferromagnets, Nature Mater. 19, 34 (2020).
[83] J. Whitehead, An expression of Hopf’s invariant as an integral,
Proceedings of the National Academy of Sciences of the United
States of America 33, 117 (1947).

[84] F. Wilczek and A. Zee, Linking numbers, spin, and statistics of
solitons, Phys. Rev. Lett. 51, 2250 (1983).
[85] R. Knapman, M. Azhar, A. Pignedoli, L. Gallard, R. Hertel,
J. Leliaert, and K. Everschor-Sitte, Numerical calculation of the
Hopf index for three-dimensional magnetic textures, Phys. Rev.
B 111, 134408 (2025).
[86] K. Ohgushi, S. Murakami, and N. Nagaosa, Spin anisotropy
and quantum Hall effect in the kagomé lattice: Chiral spin state
based on a ferromagnet, Phys. Rev. B 62, 6065(R) (2000).
[87] K. Hamamoto, M. Ezawa, and N. Nagaosa, Quantized topological Hall effect in skyrmion crystal, Phys. Rev. B 92, 115417
(2015).
[88] B. Göbel, A. Mook, J. Henk, and I. Mertig, Unconventional
topological Hall effect in skyrmion crystals caused by the topology of the lattice, Phys. Rev. B 95, 094413 (2017).
[89] G. Yin, Y. Liu, Y. Barlas, J. Zang, and R. K. Lake, Topological
spin Hall effect resulting from magnetic skyrmions, Phys. Rev.
B 92, 024411 (2015).
[90] M.-C. Chang and Q. Niu, Berry phase, hyperorbits, and the
Hofstadter spectrum: Semiclassical dynamics in magnetic
Bloch bands, Phys. Rev. B 53, 7010 (1996).
[91] P. Oppeneer, Magneto-optical spectroscopy in the valenceband energy regime: relationship to the magnetocrystalline
anisotropy, J. Magn. Magn. Mater. 188, 275 (1998).
[92] D. Xiao, J. Shi, and Q. Niu, Berry phase correction to electron
density of states in solids, Phys. Rev. Lett. 95, 137204 (2005).
[93] T. Thonhauser, D. Ceresoli, D. Vanderbilt, and R. Resta, Orbital magnetization in periodic insulators, Phys. Rev. Lett. 95,
137205 (2005).
[94] D. Ceresoli, T. Thonhauser, D. Vanderbilt, and R. Resta, Orbital magnetization in crystalline solids: Multi-band insulators,
Chern insulators, and metals, Phys. Rev. B 74, 024408 (2006).
[95] A. Raoux, F. Piéchon, J.-N. Fuchs, and G. Montambaux, Orbital
magnetism in coupled-bands models, Phys. Rev. B 91, 085120
(2015).
[96] B. Göbel, A. Mook, J. Henk, and I. Mertig, Signatures of lattice
geometry in quantum and topological Hall effect, New J. Phys.
19, 063042 (2017).
[97] L. Onsager, Interpretation of the de Haas-van Alphen effect,
The London, Edinburgh, and Dublin Philosophical Magazine
and Journal of Science 43, 1006 (1952).
[98] Data are provided for figures shown in this paper,
https://doi.org/10.5281/zenodo.15609600.


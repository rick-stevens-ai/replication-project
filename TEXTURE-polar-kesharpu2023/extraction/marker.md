<!-- extraction: pdftotext | arxiv:2305.13423 -->
Factors affecting the topological Hall effect in strongly correlated layered magnets: spin of the
magnetic atoms, polar and azimuthal angle subtended by the spin texture
Kaushal Kumar Kesharpu1, ∗
1 Bogoliubov Laboratory of Theoretical Physics, Joint Institute for Nuclear Research, Dubna 141980, Russia

arXiv:2305.13423v3 [cond-mat.mes-hall] 26 Dec 2023

(Dated: December 27, 2023)
The Hamiltonian of a two dimensional (2D) magnetic material in the strong correlation regime with a spin texture,
for which both azimuthal and polar angle changes, is solved using 𝑠𝑢(2) path integral method. The dependence
of the Chern number on the atomic spin (𝑆), azimuthal angle (𝑞®1 ) and polar angle (𝑞®2 ) modulation vector of
the spin texture on a bipartite honeycomb lattice is found. For 𝑆 ≤ 3 it was found that Chern number depends
strongly on 𝑞®2 and 𝑆. We discuss applicability of the model to several van der Waals magnets. Experimentally, it
is expected that, with increase in spin modulation vector the sign of the topological Hall conductivity changes,
+𝜎𝑥𝑇𝑦𝐻 𝐸 → −𝜎𝑥𝑇𝑦𝐻 𝐸 or vice-versa, when 𝑆 is constant. We also propose several heterostrucures for experimental
realization of this effect.
I.

INTRODUCTION

Motion of electrons on an adiabatically changing chiral
spin texture in the strong coupling regime gives rise to the
topological Hall effect (THE) [1]. For the strong coupling
case the spin of the electrons follows the local direction of
the magnetization. If the magnetization varies in a closed
loop, then the electrons acquire a geometric phase in the
parameter space, which in turn gives rise to the THE [2–4].
A large number of spin textures — e.g. skyrmions [5–8],
conical [9–11], hedgehog [12], magnetic bubble [13] to name
a few [for a complete list see Tab. 1 of Ref. 4] — generating
THE had already been observed experimentally in 2D layered
magnetic materials [4]. Microscopically, the DzyloshinskiiMoriya interaction (DMI) [14, 15], the dipolar interaction[16],
frustrated chirality [17, 18], out-of-plane anisotropy [19, 20]
and Fermi surface curvatures [21] are responsible for THE.
Due to the involvement of these different microscopic effects
understanding the competition between them [22–25] and ways
to manipulate them is important from the point of view of
the fundamental physics as well as applied spintronics [26].
Recently, Van der Waals (vdW) magnets have emerged as one
of the promising class of materials for investigation of these
effects [27], due to the possibility of changing their properties
through intrinsic means (chemical doping [28], stacking order
and twist of the monolayers [27, 29–32], free carrier doping)
as well as extrinsic means (electric field, magnetic field, strain,
pressure [33]).
The vdW magnets are primarily divided into five different
family of compounds [28, 34]: (i) transition metal halides, (ii)
transition metal phosphorous tri-chalcogenides, (iii) transition
metal di-chalcogenides, (iv) ternary iron based tellurides, (v)
transition metal oxyhalides. In these compounds itinerant ferromagnetism, Kondo lattice bheaviour, and Mott insulating phase
[34–40] are observed due to the strong electronic correlation.
Keeping this in mind, to investigate the electronic properties of
these 2D materials with localized spin moments a low-energy
effective theory using 𝑠𝑢(2) path integral method was proposed
recently [41]. It was shown that the THE for a material with

∗ kesharpu@theor.jinr.ru

FIG. 1. Representation of spin texture given in Eq. (1) on a Bloch
sphere. 𝑆 𝑥 , 𝑆 𝑦 , and 𝑆 𝑧 represent the 𝑥, 𝑦, and 𝑧 component of the
spin. 𝑞®1 is the polar angle modulation vector and 𝑞®2 is the azimuthal
angle modulation vector.

honeycomb bipartite lattice and strongly coupled electron spin
to the background high spin-𝑆 conical spin texture — here
𝑆 is the effective magnetic moment of the magnetic atoms —
depends only on the: (i) atomic spin 𝑆 , (ii) and the spin modulation vector of the spin texture. In the investigated conical spin
texture only the azimuthal angle of the spin projection (on xy
plane) changed through neighboring sites. Hence naturally the
question arises, how the topological properties of the materials
changes if both the azimuthal angle as well as the polar angle
of the spin texture changes? To answer this question in this
work we analyzed the spin texture:
𝑆 𝑥 
sin 𝑞®1 𝑟®𝑖 cos 𝑞®2 𝑟®𝑖 
 


𝑆®𝑖 ≡ 𝑆 𝑦  = 𝑆  sin 𝑞®1 𝑟®𝑖 sin 𝑞®2 𝑟®𝑖 
𝑆𝑧 


cos 𝑞®1 𝑟®𝑖
 



(1)

Here 𝑆 𝑥 , 𝑆 𝑦 , and 𝑆 𝑧 are the 𝑥, 𝑦, and 𝑧 component of the

localized spin momentum 𝑆®𝑖 . 𝑞®1 = 𝑞 1𝑥 , 𝑞 1𝑦 and 𝑞®2 =
𝑞 2𝑥 , 𝑞 2𝑦 are the two spin modulating wave vectors on a 2D
plane. 𝑟®𝑖 = (𝑥, 𝑦) is the position vector on the 2D plane.
If 𝑆®𝑖 is represented on the Bloch sphere, where north pole
corresponds to the 𝑆 𝑧 = |+𝑆⟩ state and south pole corresponds
to the 𝑆 𝑧 = |−𝑆⟩ state, then 𝑞®1 is the polar angle modulating

2

Sz + Sx
+S

12
8

8

-4

-4

-8

-8
-4

0

x

4

8

S

12

-8

(a) Square
+S

4

8

S

12

4

4

0

0

y

8

-4

-8

0

8

x

-8

0

8

x

+S

12

8

Sz

M
0

0

+M

0

Magnetic moment
(a) Fe3 GeTe2

-4
-8
-8

-4

0

x

4

8

(c) Honeycomb

12

S

-12
-12

-8

-4

0

x

4

8

12

S

(d) Kagome

FIG. 2. Spin texture generated from Eq. (1) for 𝑞®1 = 𝑞®2 = (𝜋/6, 𝜋/6)
on (a) square, (b) triangular, (c) honeycomb, and (d) Kagome lattice.
The direction of the arrow represents the angle extended by 𝑆 𝑥 and
𝑆 𝑦 on 𝑥𝑦 plane, defined as: arctan 𝑆 𝑦 /𝑆 𝑥 . The color represents the
values of the 𝑆 𝑧 .

vector and 𝑞®2 is the azimuthal angle modulating vectors as
shown in Fig. 1. 𝑆 = 1/2, 1, 3/2, . . . is the highest spin state
of the background magnetic atoms. The spin texture on a 2D
square, triangular, honeycomb, and kagome lattice is shown
in 2. Here the 𝑆 𝑧 component is shown through color, and the
𝑆 𝑥 , 𝑆 𝑦 components are shown
through direction of the arrows

defined as arctan 𝑆 𝑦 /𝑆 𝑥 .
Experimentally analogous spin texture was observed in vdW
ferromagnet Fe3 GeTe2 (F3GT). It is a conductor with itinerant
ferromagnetism [44] and Kondo lattice behavior [45]. In F3GT
using scanning electron microscopy with polarization analysis
a modulated spin spiral on 𝑥𝑧 plane (Neel order), as well as on
𝑥𝑦 plane was observed [42]. The same spin texture was also
observed through Lorentz transmission electron microscopy
(LTEM) and micromagnetic simulations [46–48]. In Fig. 3a
using Eq. (1) with 𝑞®1 = (𝜋/8, 𝜋/8) and 𝑞®2 = (𝜋/4, 𝜋/4)
we plot qualitatively same spin texture as was experimentally
observed [see Fig. 1 of Ref. 42]. We say qualitatively, as one
can see the pronounced peak and dip of the magnetization for
𝑆 𝑧 +𝑆 𝑥 in comparison to 𝑆 𝑧 +𝑆 𝑦 , as was observed in experiment.
In another sister compound Cr2 Ge2 Te6 (CGT) through LTEM
analogous spin texture was detected [43]. In Fig. 3b using
Eq. (1) for 𝑞®1 = (𝜋/2, 0) and 𝑞®2 = (𝜋/3, 0) we reproduce
the experimentally observed spin texture [see Fig. 2c of Ref.
43]. Physically this spin texture can be thought of as Neel
spin order sandwiched in between two Bloch domain walls.
On a side note, such magnetic texture was also observed in
heterostructures of the multiple ferromagnetic monolayers. In
these materials combined effect of the perpendicular magnetic
anisotropy (PMA) — due to the dipole interaction between the

+S

12
8
4

0

0

Sz

-8

y

y

0

x

(b) Triangular

12

-12
-12

-4

Sz + Sy

12
8
4
0
-4
-8
-12

Sz

-8

-12
-12

y

0

0

Sz

y

4

0

0

Sz

y

4

-12
-12

+S

12

-4
-8
-12
-12

-8

-4

0

x

4

8

12

(b) Cr2 Ge2 Te6

FIG. 3. (a) Generation of the qualitative spin texture in Fe3 GeTe2
experimentally observed in Fig. 1 of Ref. [42] using Eq. (1). On
the left hand side the summation of magnetization along 𝑧 and 𝑥 axis
(𝑆 𝑧 + 𝑆 𝑥 ) is plotted. On the right the summation of magnetization
along 𝑧 and 𝑦 axis (𝑆 𝑧 + 𝑆 𝑦 ) is plotted. We observe more pronounced
magnetic texture for 𝑆 𝑧 + 𝑆 𝑥 compared to 𝑆 𝑧 + 𝑆 𝑦 ; the same was
observed in experiment. (b) Generation of the experimentally observed
spin texture in Cr2 Ge2 Te6 in Fig. 2c of Ref. [43], using Eq. (1), with
𝑞®1 = (𝜋/2, 0) and 𝑞®2 = (𝜋/3, 0).

layers — and the interfacial DMI give rise to the spin texture
[49]. In [Co/Ni]𝑛 /Ir/Pt(111) heterostructure depending on the
thickness of the magnetic multilayer stack [Co/Ni]𝑛 and the
Ir layer, either Bloch-type or Neel-type domain walls were
observed, however, for some specific thickness of both these
layers one can find both Bloch and Neel domain walls [50]. It
is in this region one can find the spin texture represented by Eq.
(1). The same is true for Co/Pd [51] and Fe/Ni/Cu(001) [52]
multilayers.
In this work we solve the Hamiltonian of the 2D magnetic
materials in the strong electron correlation limit with spin
texture given by Eq. (1). It is assumed that the system has
localized spin. The model can be applied to the arbitrary 2D
crystal structure with magnetic atoms having arbitrary high

3

b1
a2 a1
a3 b3
b2

model in strong coupling regime (the Hubbard model in strong
correlation regime) through the Hubbard 𝑋 𝑝𝑞 operators [58].
As there exist one-to-one mapping of the 𝑋 𝑝𝑞 operators to the
𝑝𝑞
𝑠𝑢(2) coherent state operators 𝑋𝑐𝑠
= ⟨𝑧, 𝑓 | 𝑋 𝑝𝑞 |𝑧, 𝑓 ⟩ [59–61]
— here the 𝑓 and 𝑧 are the spinless charged fermionic field
(holon) and spinful bosonic fields (spinon) respectively — one
can transform the 𝑋 𝑝𝑞 Hamiltonian into the coherent symbol
𝑝𝑞
𝑋𝑐𝑠
Hamiltonian. Finally the path integral approach is used
𝑝𝑞
to solve the resulting 𝑋𝑐𝑠
Hamiltonian containing the holon
and spinon degrees of freedom. Physically this Hamiltonian
represent the interaction of the strongly correlated itinerant
electrons with the background spin textures. We re-derived this
theory in App. A for convenience of the readers. The resulting
Hamiltonian given by Eq. (A17) is quite general, in the sense
that arbitrary two dimensional lattice structure and spin texture
can be plugged into it to solve the specific systems.

FIG. 4. The bipartite honeycomb lattice. 𝑎®1 , 𝑎®2 , and 𝑎®3 represent the
three nearest neighbor vectors. 𝑏® 1 , 𝑏® 2 , and 𝑏® 3 represents the three
next nearest neighbor vectors.

spin-𝑆. The high localized spin treatment of the problem is
necessary, as in 2D materials due to reduced coordination
number of the surface atoms the localized electronic bands at
surface become narrower compared to the bulk; the narrow band
favors the localization, exchange splitting and higher magnetic
moments [53]. Besides, the studied van der Waals magnets
have high correlation which favours narrower bands. It was
found that, for spin 𝑆 ≤ 3 in a bipartite honeycomb lattice for
polar spin modulation vector 𝑞®1 = (𝑞 1𝑥 , 0) and azimuthal spin
modulation vector 𝑞®2 = (𝑞 2𝑥 , 0), the Chern number depends
strongly on 𝑞®2 , weakly on 𝑞®1 ; for higher spins the effect of 𝑞®1
also increases [see Fig. 7]. The general expression of Chern
number, Eq. (7), is analogous to the Chern number found in
Ref. [54]; it represents the amount of effective magnetic flux
penetrating the single unit sublattice plaquette. We also found
that the Chern number depends in an analogous manner as the
Haldane model [55] for large 𝑆 and 𝑞 2𝑥 [see Fig. 9].
The article is structured as follows, in Sec. II we give the
resulting Hamiltonian on a bipartriate lattice. The complete
theory, and the mathematical procedure to solve the Hamiltonian is described in App. A and B respectively. In Sec. II A
and II B we find the Chern number for integer and half-integer
spins. In Sec. III we discuss different aspects of the topological
properties of the result, and possible experimental setups.

II.

As discussed in Sec. III E usually the magnetic atoms in vdW
magnets create honeycomb bipartite crystal structure. Hence,
at first, we solve the Eq. (A17) for bipartite lattice with spin
texture Eq. (1), then we impose the honeycomb lattice structure
to the resulting Hamiltonian. A bipartite lattice 𝐿 can be divided
into two sub lattices 𝐴 and 𝐵, i.e. 𝐿 = 𝐴 ⊕ 𝐵. Therefore the
nearest neighbor (NN) hopping is always related to the hopping
from one sub-lattice to the another (𝐴 → 𝐵, 𝐵 → 𝐴), and the
next nearest neighbor (NNN) hopping is related to the hopping
on the same sub-lattices (𝐴 → 𝐴, 𝐵 → 𝐵). Defining the NN
lattice vector as 𝑎 𝑛 , and NNN lattice vector as 𝑏 𝑛 , the bipartite
Hamiltonian, Eq. (A17), in momentum space can be written as
[see App. B for solution]:

𝐻 ( ®𝑘) =

∑︁

𝜓¯ 𝑘® H ( ®𝑘)𝜓 𝑘® .

𝑘®

METHOD AND CALCULATION

To model the vdW materials we start from the Kondo lattice
system where the localized magnetic moments on each lattice
sites behave as spinless scattering sites [56]. At large Kondo
coupling, i.e. when the coupling between the conduction
electron spins and the localized spin momentum is strong,
the Kondo lattice model is identical to the Hubbard model
with large electron correlation [57]. The necessary theory for
solving this model using 𝑠𝑢(2) path integral method was given
recently [41]. Basically the idea is to represent the Kondo lattice

h
The matrix 𝜓 𝑘® = 𝑓 ®𝑘, 𝐴

i𝑇
𝑓 ®𝑘,𝐵

contains the holon creation

®
operators of the 𝑘-th
momentum on the two sub-lattices 𝐴
and 𝐵 of the bipartite lattice. The single mode kernel of the
® = H0 ( 𝑘)
® · I + H𝑖 ( 𝑘)
® ·®
Hamiltonian is H ( 𝑘)
𝜎𝑖 . Here, I is
® are the
the unit matrix; ®
𝜎𝑖 are the Pauli matrices, and H𝑖 ( 𝑘)

4
corresponding kernels. Explicitly

∑︁

0

E(k)

0.2

0

E(k)



𝓅( 𝑘® ′ ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛 ,


𝑘®′

 𝑆


𝑎®𝑛
′𝑆
′
∗ cos 𝑘® 𝑎®𝑛
H𝑥 = +𝑡1 𝓌𝑛 F̂ 1 − ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
2



𝑎®𝑛 𝑆
H𝑦 = +𝑡1 𝓌𝑛′𝑆 F̂ 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
∗ sin 𝑘® 𝑎®𝑛
2
"
!# 𝑆
𝑏® 𝑛
𝑆
H𝑧 = −2𝑡2 𝓌𝑛 F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
∗
2
cos 𝑆 𝑞®2 𝑏® 𝑛 cos 𝑘® 𝑏® 𝑛 + 2𝑆 sin 𝑆 𝑞®2 𝑏® 𝑛

x|a1
x|a2

-0.4
/2










− sin 𝑆 𝑞®2 𝑏® 𝑛 sin 𝑘® 𝑏® 𝑛 + 2𝑆 cos 𝑆 𝑞®2 𝑏® 𝑛




Where,

Here, 𝑡1 and 𝑡 2 are the electron NN and NNN hopping factors.
𝑘® and 𝑘® ′ are the momentum which take values in the first
Brillouin zone (BZ). 𝓅( 𝑘® ′ ) is the Fourier coefficients of the
Fourier transform of the real space function [see Eq. (B9)]:
"
#
∑︁
1
®′
atan
𝓅( 𝑘® ′ )e−𝑖 𝑘 𝑟® . (3)
=
𝒽(𝑟) csc 𝑞®2 𝑏® 𝑛 + cot 𝑞®2 𝑏® 𝑛
𝑘′
𝒽(𝑟) is the function or 𝑟®𝑖 and 𝑞®1 as defined in Eq. (B3). The
𝓅( 𝑘® ′ ) is a function of 𝑞®1 and 𝑞®2 as the L.H.S. of Eq. (3)
depends on 𝑞®1 and 𝑞®2 . However irrespective of the values of
the 𝑞®1 and 𝑞®2 the values of 𝓅( 𝑘® ′ ) ≈ 0 in Brioullion zone for
almost all 𝑘® ′ [see Fig. 14]. The values of 𝓌𝑛 , 𝓌𝑛′ , ℊ𝑛 , and ℊ𝑛′
also depend on the spin modulation vectors 𝑞®1 and 𝑞®2 [see Fig.
6 and 15]. F̂ represents the Fourier transform operator;
«∗» is the convolution operator. 𝑆 is the effective spin of
the magnetic atoms. For the integer spins (𝑆 = 1, 2, . . . ) the
Fourier transform is easy to find. However, for half-integer spins
(𝑆 = 1/2, 3/2, . . . ) analytical expression of Fourier transform
can be found only in extreme limits of ℊ𝑛 and ℊ𝑛′ . Both these
cases along with their topological properties on a honeycomb
lattice are discussed in the following sections.

Chern number for Integer spin
Chern number for 𝑆 = 1

In this section we calculate the topological properties of the
Hamiltonian Eq. (2) for honeycomb lattice. The honeycomb

/2

/2

E(k)

z|b3

0
kx

/2

0.8
0.4

K
0
kx

K

K

0
-0.4

K

/2

x
y

-0.8

/2

/2

(c)

0
kx

z

/2

(d)

FIG. 5. Dependence of (a) H𝑥 and (b) H𝑦 on the momentum vector
𝑘 𝑥 corresponding to the three NN vectors; the value of 𝑘 𝑦 = 0
everywhere. We have taken
𝑞® = (𝜋/4, 0) and 𝑞®2 = (𝜋/4, 0). The
√  1
value of K = ±𝜋/ 3, 0 . (c) The same dependence of H𝑧 on
corresponding NNN vectors. (d) Summation of the previously plotted
three components of the H𝑥 , H𝑦 , and H𝑧 .

bipartite lattice is shown in Fig. 4. It has the following nearest
neighbor (NN, 𝑎®𝑛 ) and next nearest neighbor (NNN, 𝑏® 𝑛 ) wave
vectors:
!
!
√
√
3 1
3 1
𝑎®1 =
,
,
𝑎®2 = − ,
,
𝑎®3 = (0, 1) ,
2 2
2 2
!
!
√
√
√ 
®𝑏 1 = − 3 , 3 , 𝑏® 2 = − 3 , − 3 ,
𝑏® 3 = 3, 0 .
2 2
2
2
For 𝑆 = 1 Eq. (2) will be:
H0 = −2𝑡 2





h
i
ℊ𝑛
𝓌𝑛 1 +
cos 2𝑞®1 𝑏® 𝑛 ×
2
𝑛

∑︁



 


𝓅( 𝑘® ′ ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛




𝑘®′




′
∑︁
ℊ
H𝑥 = +𝑡1
𝓌𝑛′ 1 − 𝑛 cos 2𝑞®1 𝑎®𝑛 × cos 𝑘® 𝑎®𝑛
2
𝑛


∑︁
ℊ′
H𝑦 = +𝑡1
𝓌𝑛′ 1 − 𝑛 cos 2𝑞®1 𝑎®𝑛 × sin 𝑘® 𝑎®𝑛
2
𝑛
i
h
∑︁
ℊ𝑛
cos 2𝑞®1 𝑏® 𝑛 ×
H𝑧 = −2𝑡2
𝓌𝑛 1 +
2
𝑛





1.

y|a1
y|a2
y|a3

-0.4

(b)

z|b1
z|b2






!
"
! #
1 cos 𝑞®2 𝑏® 𝑛
1 cos 𝑞®2 𝑏® 𝑛
1
®
+
cos 𝑞®1 𝑏 𝑛 ; ℊ𝑛 ≡
−
𝓌𝑛 ;
𝓌𝑛 ≡ +
2
4
4
4
4



 
1
1 cos 𝑞®2 𝑎®𝑛
1 cos 𝑞®2 𝑎®𝑛
𝓌𝑛′ ≡ −
+
−
cos 𝑞®1 𝑎®𝑛 ; ℊ𝑛′ ≡
𝓌𝑛′ .
2
4
4
4
4
(2)

A.

0.4
0.2
0
-0.2
-0.4

K

-0.2

x|a3

0
kx

K

(a)



𝓅( 𝑘® ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 𝑛 .


𝑘®′


∑︁

0.4

0.2
-0.2






K

E(k)






K

0.4

H ( ®𝑘) = H0 I + H𝑥 ( ®𝑘)𝜎𝑥 + H𝑦 ( ®𝑘)𝜎𝑦 + H𝑧 ( ®𝑘)𝜎𝑧 ;
"
!# 𝑆
𝑏® 𝑛
𝑆
H0 = −2𝑡 2 𝓌𝑛 F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
∗
2





cos 𝑞®2 𝑏® 𝑛 cos 𝑘® 𝑏® 𝑛 + 2 sin 𝑞®2 𝑏® 𝑛

∑︁

− sin 𝑞®2 𝑏® 𝑛 sin 𝑘® 𝑏® 𝑛 + 2 cos 𝑞®2 𝑏® 𝑛

(4)



 


′
′ ®
®
®
®
𝓅( 𝑘 ) sin 𝑘 + 𝑘 𝑏 𝑛 .


𝑘®′


∑︁

For topological properties to appear the condition H𝑥 = H𝑦 = 0
and H𝑧 ≠ 0 should be satisfied simultaneously [ses Sec. 3.5.6

q2x

/2
0
/2

q2x

5

/2
0
/2

1(a1)

2(a2)

3(a3)

1(b1)

2(b2)

3(b3)

for derivation]:

H0 ≈ −2𝑡2

/2 0

q1x

0.0

/2

0.2

/2 0

q1x

0.4

/2

/2 0

0.6

0.8

q1x






/2

1.0

FIG. 
6. Plot of thedependence of the ℊ𝑛′ 
and ℊ𝑛 on the wave vectors
√
√
𝑞®1 = 2𝑞 1𝑥 / 3, 0 and 𝑞®2 = 2𝑞 2𝑥 / 3, 0 on a honeycomb bipartite
lattice calculated using Eq.
 (2). The values of 𝑞 1𝑥 and 𝑞 2𝑥 lies in the
√
√
range − 3𝜋/2, 3𝜋/2 .

√



of Ref. 62]. In our case if we take 𝑞®1 = 2𝑞 1𝑥 / 3, 0 and


√ 
√ 
𝑞®2 = 2𝑞 2𝑥 / 3, 0 , then at the point 𝐾® = ±𝜋/ 3, 0 the
condition is satisfied identically [see App. E]. To show this
graphically in Fig. 5 we plotted the three individual components
of H𝑥 (Fig. 5a), H𝑦 (Fig. 5b) and H𝑧 (Fig. 5c) corresponding
to the respective NN and NNN vectors for 𝑞®1 = (𝜋/4, 0) and
𝑞®2 = (𝜋/4, 0). We observe that all three components of H𝑥 are
® For H𝑦 the 𝑎®3 component is zero at 𝐾;
® the 𝑎®1 and
zero at 𝐾.
𝑎®2 components are of opposite sign. In result the sum of the all
® For H𝑧 the 𝑎®3 component
three component of H𝑦 is zero at 𝐾.
is zero at ®
𝐾, however the 𝑎®2 and 𝑎®3 components are non zero.
Chern number for this case is [see App. E]:
√

𝑐 1 = sgn [sin (𝑞 2𝑥 )] ,

3𝜋
−
≤ 𝑞 2𝑥 ≤
2

cos 𝑆 𝑞®2 𝑏® 𝑛 cos 𝑘® 𝑏® 𝑛 + 2𝑆 sin 𝑆 𝑞®2 𝑏® 𝑛

∑︁



 


𝓅( 𝑘® ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 𝑛 .




𝑘®′


(6)
Comparing Eq. (4) and Eq. (6) one can see the extra factor of
𝑆 appears in different terms of the Hamiltonian. For Eq. (6) the
topological condition, H𝑥 = H𝑦 = 0 and H𝑧 ≠ 0, is satisfied
√
√ 
simultaneously at 𝐾® = ±𝜋/ 3, 0 for 𝑞®1 = 2𝑞 1𝑥 / 3, 0 and

√ 
𝑞®2 = 2𝑞 2𝑥 / 3, 0 . The Chern number is [see App. E 2 for
derivation]:
− sin 𝑆 𝑞®2 𝑏® 𝑛 sin 𝑘® 𝑏® 𝑛 + 2𝑆 cos 𝑆 𝑞®2 𝑏® 𝑛

∑︁

√

3𝜋
.
2

(5)

Interestingly, the Chern number depends only on the spin wave
vectors 𝑞®2 = (𝑞 2𝑥 , 0) — the azimuthal angle. However, it does
not mean that when 𝑞®1 = 0 the topological effect is present;
it is absent [63]. Physically, it means for topological effects
to occur some inclination of spin vector is necessary, which is
related to nonzero effective magnetic field [64].

2.



 


𝓅( 𝑘® ′ ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛




𝑘®′




′
∑︁
𝑆ℊ
𝑛
cos 2𝑞®1 𝑎®𝑛 × cos 𝑘® 𝑎®𝑛
H𝑥 ≈ +𝑡1
𝓌𝑛′𝑆 1 −
2
𝑛


∑︁
𝑆ℊ𝑛′
′𝑆
H𝑦 ≈ +𝑡1
𝓌𝑛 1 −
cos 2𝑞®1 𝑎®𝑛 × sin 𝑘® 𝑎®𝑛
2
𝑛


∑︁
𝑆ℊ𝑛
cos 2𝑞®1 𝑏® 𝑛 ×
H𝑧 ≈ −2𝑡2
𝓌𝑛𝑆 1 +
2
𝑛









𝑆ℊ𝑛
𝓌𝑛𝑆 1 +
cos 2𝑞®1 𝑏® 𝑛 ×
2
𝑛

∑︁

Chern number for 𝑆 = 2, 3, . . .

For higher spin 𝑆 = 2, 3, . . . one will need to expand the
terms containing ℊ𝑛 and ℊ𝑛′ using binomial theorem [see App.
C]. In Fig. 6 we plotted the dependence of ℊ𝑛 and ℊ𝑛′ on
𝑞 1𝑥 and 𝑞 2𝑥 . We observe that the value of ℊ𝑛 and ℊ𝑛′ are
always positive and less than unity for most part of the phase
space 𝑞 1𝑥 and 𝑞 2𝑥 . Hence, one can neglect the higher powers
of ℊ𝑛 and ℊ𝑛′ and keeping terms only upto first power in the
binomial expansion. The resulting Hamiltonian is [see App. C





𝑆ℊ2
cos 2𝑞 1𝑥 (sin 𝑆𝑞 2𝑥 − 2𝑆𝜖 cos 𝑆𝑞 2𝑥 )
2
(7)


Í
′
′
®
®
Here, we introduced the symbol 𝜖 ≡ 𝓅(𝑘 ) sin 𝜋/2 + 𝑘 𝑏 1 ;
𝑐 1 = sign

1+

𝑘′

it’s value is always ≪ 1 over whole 𝑞 1𝑥 and 𝑞 2𝑥 phase space [see
Fig. 17]. One can see that, now the Chern number depends also
on the 𝑞 1𝑥 — the polar angle; for 𝑆 = 1 it was absent. In fact,
one can recover the Chern number for 𝑆 = 1, Eq. (5), from Eq.
(7). It can be seen as follows. For 𝑆 = 1 the |ℊ2 cos 2𝑞 1𝑥 /2| will
always be less than unity
 (as 0 ≤ ℊ2 ≤ 1).In result, the whole
𝑆ℊ
term 1 + 2 2 cos 2𝑞 1𝑥 will always be positive irrespective
of 𝑞 1𝑥 . Therefore this term will not have any affect on the 𝑐 1 ,
and one can drop this from Eq. (7). As mentioned before the
𝜖 ≪ 1; the only reason for including it in Eq. (7), is that for
large 𝑆 the term, 2𝑆𝜖 cos 𝑆𝑞 2𝑥 , might be larger than sin 𝑆𝑞 2𝑥 .
However, for 𝑆 = 1 the 2𝜖 cos 𝑆𝑞 2𝑥 will never be greater than
sin 𝑆𝑞 2𝑥 , apart from some narrow regions of 𝑞 1𝑥 -𝑞 2𝑥 phase
space. Hence, we will drop the 2𝜖 cos 𝑆𝑞 2𝑥 term also in Eq.
(7). Therefore we recovered the Eq. (5).

6
TABLE I. Hamiltonians for spin 𝑆 = 1/2 in extreme limits.
Case

ℊ𝑛′

ℊ𝑛

Hamiltonian

I
II
III
IV

≪1
≪1
∝1
∝1

∝1
≪1
∝1
≪1

Eq. (D11)
Eq. (D4)
Eq. (D10)
Eq. (D12)

B.

Chern number for Half-Integer Spins

Finding a general analytical expression of Chern number for
𝑆 = 1/2 is little bit tricky, as Fourier transform of the terms,

F̂

1 − ℊ𝑛′ cos 2𝑞®1



𝑎®𝑛
𝑟®𝑖 +
2

  1/2

𝑏® 𝑛
2

! # 1/2

"
F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +

,
FIG. 7. Chern number calculated using Eq. (7).

(8)
,

are not available. Therefore, one need to find the Hamiltonian
in the limiting cases of ℊ𝑛 and ℊ𝑛′ , and then make the necessary
conclusions. We can have four limiting case of ℊ𝑛 and ℊ𝑛′
in different combinations. The four cases and corresponding
Hamiltonian are given in Tab. II B. Observing these Hamiltonian we will see that they are analogous to the Eq. (4). Meaning,
the term containing 𝑘® remains same. The only difference is the
factors involving ℊ𝑛 and ℊ𝑛′ . Hence, their Chern number will
be given by Eq. (5).
The calculation for Hamiltonian for large half-integer 𝑆 is
given in App. D 2. The main idea is to represent:

proportional to the 𝑆 3 , hence, with increase in 𝑆 the threaded
magnetic field also increases.






𝑎®𝑛 1/2
𝑎®𝑛 1/2
1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
≈ 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2
2

 (𝑆−1/2)

𝑎®𝑛
× 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
.
2
(9)

Then use the approximations for 𝑆 = 1/2 (App. D 1) and higher
integer 𝑆 (App. II A 2) to find the Fourier transform of the
resulting expression. The calculation procedure is described in
App. D 2. The resulting Hamiltonians will also be analogous
to the Eq. (6). Therefore the Chern number will be given by
Eq. (7).

III.
A.

DISCUSSION

General formula for Chern number

From the above discussions we can conclude that Eq. (7)
gives the Chern number for both integer or half-integer spins. In
Fig. 7 we plotted the Chern number dependence on 𝑞 1𝑥 and 𝑞 2𝑥
for spin upto 𝑆 = 3. Near 𝑞 1𝑥 ≈ 0 and 𝑞 2𝑥 the Chern number
is not defined. The 𝑞 1𝑥 = 0 physically represent the spin
vector pointing towards the north pole, and 𝑞 2𝑥 = 0 represent
the rotation of the spin only along some fixed longitude of

B.

Energy band gap closing

/2

kx



Bloch sphere; both these cases have ill defined Chern number.
One can observe that apart from some small discrepancies in
most part of the figure the Chern number depends only on the
azimuthal modulating vector 𝑞 2𝑥 . Hence Eq. (5) can be used
as an approximated formula for Chern number. Physically, the
dependence of Chern number on 𝑆𝑞 2𝑥 can be understood as
the amount of effective magnetic field threading through three
lattice points locally [54]. The effective local magnetic
field
h
i
®
®
®
through three lattice points (𝑖, 𝑗, 𝑘) is B𝑒 𝑓 𝑓 = 𝑆𝑖 · 𝑆 𝑗 × 𝑆 𝑘 is

0

q2x = 1.73
q2x = 1.83
q2x = 1.93

/2

S=2

S = 2.5
q2x = 1.38
q2x = 1.48
q2x = 1.58

S=3
q2x = 1.15
q2x = 1.25
q2x = 1.35

0.2 0.1 0 -0.1 -0.2 0.2 0.1 0 -0.1 -0.2 0.2 0.1 0 -0.1 -0.2
E(kx)
E(kx)
E(kx)
√︁
FIG. 8. Dependence of energy 𝐸 (𝑘 𝑥 ) = H𝑥 + H𝑦 + H𝑧 on 𝑘 𝑥 ∈
(−𝜋, +𝜋) for different 𝑞 2𝑥 , and 𝑆 = 2, 5/2, 3.

From the energy band point of view valence and conduction

7
√︃
band are represented by the H0 ± H𝑥2 + H𝑦2 + H𝑧2 . The wave
vector 𝑞 2𝑥 controls the gap of the bands. At specific values
of the 𝑞 2𝑥 the gap closes at ± ®
𝐾, and there is a change of the
Chern number in the corresponding band. Explicitly the values
of 𝑞 2𝑥 where the gap closes is found as:
√ !

 
𝜋

𝑆𝑞 2𝑥 3 ∑︁ ® ′
2
′® 

®
𝑞 2𝑥 = √ arcsin 2𝑆 cos
+ 𝑘 𝑏2  .
𝓅( 𝑘 ) sin
2
2
3𝑆


𝑘®′


(10)

In Fig. 8 we show the values of 𝑞 2𝑥 where the gap closes
for different 𝑆2, 2.5, 3. The energy dispersion at the points at
which the gap closes can be represented through massive Dirac
Hamiltonian. The Berry phase is concentrated around these
points, hence, the Chern number can be calculated numerically
by integrating around these points.
C.

Comparison with Haldane model

FIG. 9. Chern number dependence on sub lattice potential 𝑀/𝑡 2 and
𝑞 2𝑥 for 𝑞 1𝑥 =0 given by Eq. (11).

If compared to the Haldane model [55], then the topological
property of the Haldane model was controlled by the sublattice symmetry breaking onsite potential (𝑀) and the phase
accumulation of electrons due to NNN hopping (defined as 𝜙
in Ref. [55]). In our case the factor 𝑆𝑞 2𝑥 plays the analogous
phase accumulation role due to NNN hopping. In fact we
can phenomenologically insert additional sublattice hopping
potential 𝑀 into the H𝑧 of Eq. (2). The Chern number in this
case is:
𝑐1 =
h


i
𝑆ℊ
sign 𝑀 − 2𝑡 2 1 + 2 2 cos 2𝑞 1𝑥 (sin 𝑆𝑞 2𝑥 − 2𝑆𝜖 cos 𝑆𝑞 2𝑥 )

−

2
h


i
𝑆ℊ
sign 𝑀 + 2𝑡 2 1 + 2 2 cos 2𝑞 1𝑥 (sin 𝑆𝑞 2𝑥 − 2𝑆𝜖 cos 𝑆𝑞 2𝑥 )
2

.
(11)

In Fig. 9 we plotted the Chern number dependence on 𝑀/𝑡2
and 𝑞 2𝑥 for 𝑆 = 3; the 𝑞 1𝑥 = 𝜋/4 is kept constant.

D.

Minimum Energy

To understand the thermodynamics of the system we calculate
the total internal energy of the system through equation:
∑︁
𝑈internal =
𝐸 (𝑘) 𝑓 [𝐸 (𝑘), 𝜇]
(12)
𝑘 ∈ 𝐵𝑍

𝐸 (𝑘) is the energy of the lowest band defined as H0 −
√︃
H𝑥2 + H𝑦2 + H𝑧2 in Eq. 𝑓 [𝐸 (𝑘), 𝜇] is the Fermi-Dirac distribution; 𝑘 𝐵 = 8.6 × 10−5 eV K−1 is the Boltzman constant;
𝑇 is the temperature. In our calculation we take 𝑇 ≈ 0 K.
The summation in Eq. (12) is taken over the whole Brillouin
zone. In Fig. 10 we plotted the 𝑈internal for different 𝑆. In most
cases the lowest energy has an anti-ferromagnetic configuration,
which was expected, as the original Hamiltonian, Eq. (A17)
will have lowest energy when the dot product of the 𝑆®𝑖 · 𝑆® 𝑗 will
have negative sign.

FIG. 10. Dependence of total energy on the wave vectors 𝑞 1𝑥 and
𝑞 2𝑥 . The total energy is calculated by integrating Eq. (12) over 1st
Brillouin zone of the honeycomb lattice.

E.

Perspective Materials for application of the model

In Tab. III E we give a list of widely studied vdW materials.
In these materials usually the magnetic layers are sandwiched
in between the non magnetic layer in different configurations.
For example, in F3GT a single Fe-Fe dumbbell and a single Fe
atom are placed alternatively in a honeycomb lattice pattern;
at the center of the honeycomb lattice the single Ge atom is
placed [65, 66]. This whole structure containing the Fe and
Ge atoms are sandwiched in between Te atoms. The F4GT has
the same honeycomb lattice structure, however, now instead of
single dumbbell two dumbbells of Fe atoms are present; the
single Fe atoms are absent [65, 66]. The structure of C2GT is
more complex. Single unit cell contains four different layers of
magnetic atoms [67]. However, If considered only the magnetic
Cr ions then they form an effective honeycomb lattice [67–69].
In Cr-X3 the Cr atoms are sandwiched in between layers of

8
TABLE II. Properties of vdW materials to which proposed model
can be applied. The spin lattice is the 2D crystal structure formed by
the magnetic atoms. Atomic spin is the effective localized magnetic
moments of the magnetic atoms.
Material

Crystal
Structure

Spin
Lattice

Atomic
Spin

Fe3 GeTe2
(F3GT)
Fe4 GeTe2
(F4GT)
Cr2 Ge2 Te6
(C2GT)
Cr-X3
X=Cl,Br,I

Hexagonal

Honeycomb

3

Rhombohedral

Honeycomb

7/2

Hexagonal

Honeycomb

3/2

Rhombohedral

Honeycomb

3/2

Te - Fe - Te
Fe - Fe
Te
Fe
Ge
(a) Fe3 GeTe2

Te - Fe - Fe
Fe - Fe - Te
Te
Fe
Ge
(b) Fe4 GeTe2

Cr (Upper)
Cr-Cr
(Upper-Down)

halide (X=Cl, Br, I) atoms. The Cr3+ ions form a honeycomb
lattice structure. The same honeycomb spin lattice is formed in
other transition metal trihalides [70].
All the aforementioned materials are natural bipartriate
lattice or can be treated as effective bipartriate lattice in some
special configurations. For example, although monolayer of
the Cr-X3 can not be considered as bipartite lattice, however,
due to stacking configuration of bilayers at low temperature
rhombohedral phase, one can consider them as bipartriate
lattice [30, 71, 72]. Besides, a sister compound CrMnI6 , where
alternate Cr atoms are replaced by the Mn atoms, is proposed,
whose monolayer can be considered as bipartite lattice [73, 74].
In F3GT the Fe-Fe dumbbell and Fe atoms corresponds to
the two sub-lattices of the bipartriate lattice. For F4GT the
bonding between Fe-Fe dumbbell and Te atoms creates an
effective bipartite lattice, i.e. the one of the sublattice contains
the dumbbell with upper Fe atom of the dumbbell bonded to
the Te atom, and the other sublattice contains the lower Fe atom
of the dumbbell bonded to the Te atom. In C2GT the strong
hybridization of the Cr 3𝑑, Ge 4𝑝 and Te 5𝑝 electrons gives
rise to the bipartite lattice [75].
Two fundamental requirement of the proposed model is the
localized spin momentum and strong electron correlation. In
F3GT the electron correlation is around 𝑈 = 5 to 5.5 eV [39, 40],
which is comparable to the 𝑈 = 6.2 eV for the prototypical
heavy Fermion compound CeIn3 . Regarding localized spin
momentum, recently, it was shown that 3𝑑 electrons of the Fe
ions in F3GT have a strong localized character [76, 77]. The
itinerant ferromagnetism observed before [44], is in fact due to
the delocalized Ge/Te 𝑝 electrons [76]. In case of Cr-X3 , the
Cr sites usually have localized spin 𝑆 = 3/2 [78, 79], and the
correlation between 3𝑑 electrons is 𝑈 ≈ 3 eV [80]. The same
is also true for C2GT with 𝑈 ≈ 4 eV [81].

Upper Layer
Down Layer

(c) CrI3

Cr
Mn

(d) CrMnI6

FIG. 11. Generation of magnetic bipartite honeycomb lattice.

F.

Experiments

Naturally, the question arises how the above effect can be
physically verified? One of the indirect way of confirming
this effect is through the hall resistivity measurement. The
resistivity due to topological Hall effect is proportional to the
Chern number [1, 3, 54]: 𝜌𝑇𝑥 𝑦𝐻 𝐸 = − 𝑒22𝜋ℏ
. The Hall resistivity
𝑐1
measurements are usually done under applied varying magentic
field where the THE appears as additional resistivity in some
magnetic field range, as in this field range the chiral spin texture
is stabilized. In our case, from a theoretical point of view, after
removing the ordinary Hall effect and anomalous Hall effect
[3, 4] we will see the sign change of the 𝜌𝑇𝑥 𝑦𝐻 𝐸 with changing
𝑞 2𝑥 . In Fig. 12 we plotted the dependence of 𝜌𝑇𝑥 𝑦𝐻 𝐸 on the

1
0
-1
1
0
-1

0

/4

THE
xy

/2

q2x

3 /4
THE
xy

1
0
-1

S = 0.5

S = 1.5
0

/4

/2

q2x

3 /4
THE
xy

1
0
-1

S = 2.5
0

/4

/2

q2x

3 /4
THE
xy

THE
xy

THE
xy

THE
xy

THE
xy

9

S = 3.5
0

/4

/2

q2x

3 /4

1
0
-1
1
0
-1
1
0
-1
1
0
-1

S = 1.0
0

/4

/2

3 /4

/2

3 /4

/2

3 /4

/2

3 /4

q2x

S = 2.0
0

/4

q2x

S = 3.0
0

/4

q2x

S = 4.0
0

/4

q2x

FIG. 12. Dependence of the topological Hall resistivity 𝜌𝑇𝑥 𝑦𝐻 𝐸 on the
azimuthal spin modulation vector 𝑞 2𝑥 . The 𝜌𝑇𝑥 𝑦𝐻 𝐸 is represented in
units of 2𝜋ℏ/𝑒 2 . The polar angle 𝑞 1𝑥 is kept constant.

azimuthal angle 𝑞 2𝑥 , while keeping 𝑞 1𝑥 = 𝜋/4 constant. One
can observe that for 𝑆 = 1/2, 1 there is no change in the sign
of the 𝜌𝑇𝑥 𝑦𝐻 𝐸 , hence, from Hall resistivity experiment it is not
possible to detect the predicted effect. However for higher
𝑆 = 5/2, 3, 7/2 there are multiple sign change with increasing
𝑞 2𝑥 . Therefore for materials with high magnetic moments
(F3GT, F4GT) are good experimental platforms to observe this
effect.

two sides of the domain-walls the 𝑧-component of the spin is
directed along opposite direction, while inside the domain-wall
the spin rotates on the 𝑥𝑦 and 𝑦𝑧 plane. The spin texture is
shown in Fig. 13. Inside the domain-walls the spin texture
(only along the length of the Skyrmion) can be given by Eq.
(1) [see Eq. (2) of Ref. 82]. In real materials the domain-wall
Skyrmion spin texture has already been predicted in Janus
monolayer of Cr-X3 [84], Mn3 Sn [85], chiral magnets [86, 87].
One can control the length of the Skyrmions — which is proportional to the 𝑞®2 — by tuning the PMA and DMI in these
materials [82, 88]. Several extrinsic and intrinsic methods are
available for modification of the PMA and DMI [35, 89, 90].
We propose a hetero-structure in which upper layer consists of
Janus Cr-X3 monolayer on the substrate for which the induced
DMI can be controlled by extrinsic means of strain, voltage, or
electric current [89].
Another idea to control 𝑞®2 is to have heterostructures with two
perpendicular DMI vectors: (i) bulk DMI, (ii) interfacial DMI.
The bulk DMI arises due to intrinsic broken bulk inversion
symmetry (𝑟 → −𝑟), and the interfacial DMI occurs due to
cosmetically broken mirror symmetry (𝑧 → −𝑧) at the interface
of the heterostructures [91, 92]. The structure specific bulk
DMI is hard to control, however, the interfacial DMI can be
controlled by the extrinsic means [93–97]. One can use the
Janus vdW magnets, where the bulk inversion symmetry is
broken naturally, as the upper layer [98]. For substrate one
can use the materials with strong spin orbit coupling, where
electrical control of DMI is possible [99].

IV.

CONCLUSION

In this work we analyzed the topological properties of the spin
texture Eq. (1) on a honeycomb lattice and strongly correlated
materials. We showed that, the Chern number depends strongly
on the azimuthal angle of the spin texture, on spin of the
magnetic atoms 𝑆, and weakly on polar spin modulation vector.
The model can be applied to the vdW magnets shown in Tab.
III E. We discuss some experimental setups for observing the
effects.
Length of Skyrmion

FIG. 13. domain-wall Skyrmion spin texture. The 𝑧 projection of the
spin on the walls are opposite to each other. The 𝑥 and 𝑦 projection of
the spin along the length of the Skyrmions is defined by Eq. (1) [see
Eq. (2) of Ref. 82]. The length of the Skyrmion which is proportional
to the spin modulation vector 𝑞®2 is controlled by DMI and PMA [82].

Now the question arises, how one can control the modulation
of the azimuthal vector 𝑞®2 . To generate such spin textures one
need to use materials or hetero-structures where different magnetic energy scales, e.g. exchange interaction, perpendicular
magnetic anisotropy (PMA), DMI, competes with each other;
the competition of these energy scales gives rise to different
exotic chiral spin textures [83]. One of the promising way for
verification of the Chern number dependence on 𝑞 2𝑥 is through
domain-wall Skyrmions [82]. In these spin texture on the

ACKNOWLEDGMENTS

The author will like to thank E. A. Kochetov and P. A.
Maksimov for important discussions on the problem. The
author acknowledges the financial support from the JINR grant
for young scientists and specialists, the Foundation for the
Advancement of Theoretical Physics and Mathematics ”Basis”
for grant # 23-1-4-63-1, RFBR grant No. 21-52-12027.

Appendix A: Theory

We will work in the strong correlation regime in which the
underlying Hilbert space is modified as the double occupancy is
prohibited. It results in constrained electrons operators which
are now isomorphic to the Hubbard operators [100]. Those

10
operators appear as a generators of the su(2|1) superalgebras. As
a result charge and spin degrees of freedom can be represented
as product of the SU(2|1) supergroup. This is applicable for
particles described by the 𝑆 = 1/2, however, for arbitrary spin
𝑆 > 1/2 one will use the 𝑠𝑢(2) algebra. In the 𝑆𝑈 (2) formalism
the required theory is constructed under the condition that the
background spin field affects the fermion hopping without
breaking the global symmetry. The 𝑠𝑢(2) coherent states (CS)
have these properties, as the electron hopping factor is affected
only due to CS overlap factors [101, 102]. In condensed matter
it is analogous to the Peierls phase factor generated in an
external magnetic field. It is the vector potential generated by
the non-collinear chiral spin textures [64]. Physically it can
be thought of fictitious magnetic field through a plaquete. In
field theory it is the same as the emergent artificial gauge field
generated by the 𝑈 (1) local connection one-form of the spin
𝑈 (1) complex line bundle. It provides a covariant (geometric)
quantization of a spin [103]. In this approach the underlying
base space appears as a classical spin phase space. It is a two
sphere 𝑆 2 which can be mapped to a complex projective space
𝐶𝑃1 , endowed with a set of local coordinates (𝑧, 𝑧¯). In this case
|𝑧⟩ of the principle
quantum spin is represented as the section

(monopole) line bundle 𝑃 𝐶𝑃1 , 𝑈 (1) . The local connection
of the bundle is 𝑎 (0) = 𝑖 ⟨𝑧| 𝑑 |𝑧⟩; 𝑑 is the exterior derivative.
Physically, we start from the lattice Kondo-model:
∑︁
𝐻=−
[𝑡 𝑖 𝑗 + 𝐽 𝑆(𝑆 + 1) 𝛿𝑖 𝑗 ]𝑐†𝑖 𝜎 𝑐 𝑗 𝜎
𝑖𝑗𝜎

+𝐽

∑︁

Ŝ𝑖 · (𝑐†𝑖 𝜎 ®
𝜎𝜎 𝜎 ′ 𝑐 𝑖 𝜎 ′ ).

The high spin CS theory is constructed from the fundamental
𝑆 = 1/2 representation:

 −𝑆
ˆ−
|𝑧⟩ = 1 + |𝑧| 2
e𝑧 𝑆 |𝑆⟩ .

Here |𝑆⟩ is the highest spin-S 𝑠𝑢(2) state; 𝑆ˆ − is the spin
lowering operator. The S-dependent partition function will be:
∫
𝑍=
𝐷 𝜇 (𝑧, 𝑓 ) exp A.
(A4)
The measure 𝐷 𝜇 (𝑧, 𝑓 ) is:
Ö 𝑆 𝑑 𝑧¯𝑖 (𝑡) 𝑑 𝑧¯𝑖 (𝑡)
 2 𝑑 𝑓¯𝑖 (𝑡)𝑑𝑓𝑖 (𝑡).
𝜋𝑖 
2
𝑖,𝑡
1 + |𝑧𝑖 |

𝐷 𝜇 (𝑧, 𝑓 ) =

𝛽

𝛽

∫

 i
∑︁ ∫ h
(0)
(0)
¯
A=
𝑖𝑎 𝑖 − 𝑓𝑖 𝜕𝑡 + 𝑖𝑎 𝑖
𝑓𝑖 𝑑𝑡 −
𝐻 𝑑𝑡. (A6)
𝑖

0

0

Here, 𝑖𝑎 𝑖(0) is the 𝑢(1)-valued connection one-form of the
magnetic monopole bundle as a spin kinetic term:
𝑖𝑎 𝑖(0) = − ⟨𝑧| 𝜕𝑡 |𝑧⟩ = 𝑆

𝑖

¤̄𝑧𝑧 − 𝑧¯ 𝑧¤
1 + |𝑧| 2

.

(A7)

It is analogous to the Berry connection. The Hamiltonian in A
can be written as:
∑︁
∑︁
𝐻=−
𝑡 𝑖 𝑗 𝑓¯𝑖 𝑓 𝑗 e𝑖𝑎 𝑗𝑖 + 𝐻.𝑐. + 𝜇
𝑓¯𝑖 𝑓𝑖 ,
(A8)
𝑖𝑗

𝑖

where,
 2𝑆
1 + 𝑧¯𝑖 𝑧 𝑗
= 
 
𝑆 .
2 𝑆
1 + |𝑧𝑖 | 2
1 + 𝑧𝑗
(A9)

𝑎 𝑖 𝑗 = −𝑖 log 𝑧𝑖 𝑧 𝑗 , 𝑧 𝑖 𝑧 𝑗

Under a global SU(2) rotation

𝑖, 𝑗, 𝜎

Here 𝑐¯𝑖 𝜎 = 𝑐 𝑖 𝜎 (1 − 𝑛𝑖 𝜎¯ ) is the constrained electron operator;
𝑛𝑖 𝜎¯ = 𝑐†𝑖 𝜎¯ 𝑐 𝑖 𝜎¯ is the number operator of the complementary
spin. The constraint operator as explained above can be dynamically factorized into the spinless charge fermionic field
𝑓𝑖 (holons) and spinfull bosonic 𝑧𝑖 fields (spinons) [41, 59].
It can be seen that as long as the fermionic field satisfy the
condition 𝑓𝑖2 ≡ 0, the local no double occupancy of strongly
correlated electron is satisfied rigorously. Here, the holons
acquire the band structure of their own; it is usual behavior
for fractionalized electrons [104]. The spinons are handled by
mean-field treatment.
The necessary theory was given by the authors recently
[41], hence, here we briefly derive the required Hamiltonian.

(A5)

Here 𝑧 𝑖 keeps track of the spin and complex, while 𝑓𝑖 keeps
track of charge and is a Grassman variable. The effective action
A is defined as:

(A1)

Here 𝑐†𝑖 𝜎 (𝑐 𝑖 𝜎 ) is the electron creation (annihilation) operator
with the spin 𝜎 on site 𝑖; 𝐽 > 0 is the exchange coupling
constant; ®
𝜎 is the vector of the Pauli spin matrices; Ŝ𝑖 is
the nuclear spin operator at i-th site. The extra 𝐽 dependent
term 𝐽 𝑆(𝑆 + 1) 𝛿𝑖 𝑗 introduced in the hopping parameter is to
make sure a finite 𝐽 → ∞ limit [57]. Under the mean field
approximation one can represent the nuclear spin operator as
product of the localized spin magnitude (𝑆) and their direction
(®
𝑛𝑖 ): Ŝ𝑖 = 𝑆 · 𝑛®𝑖 . In the large Kondo limit 𝐽 → ∞ the
Hubbard model goes into the 𝑈 → ∞ limit (strongly correlated
electronic system) [57]:
∑︁
𝐻≈−
𝑡 𝑖 𝑗 𝑐¯†𝑖 𝜎 𝑐¯ 𝑗 𝜎 .
(A2)

(A3)

𝑧𝑖 →

𝑢𝑧𝑖 + 𝑣
−𝑣¯ 𝑧𝑖 + 𝑢¯

(A10)

𝑎𝑖 𝑗 → 𝑎𝑖 𝑗 + 𝜃 𝑗 − 𝜃𝑖 .

(A11)

the phase will be:
𝑎 𝑖(0) → 𝑎 𝑖(0) − 𝜕𝑡 𝜃 𝑖 ,
Here,



𝑣 𝑧¯𝑖 + 𝑢
𝜃 𝑖 = 𝑖𝑆 log
;
𝑣¯ 𝑧𝑖 + 𝑢¯

"

#
𝑢 𝑣
∈ 𝑆𝑈 (2).
−𝑣¯ 𝑢¯

(A12)

The effective action A remains unchanged under 𝑆𝑈 (2) transformation of the 𝑧𝑖 in conjunction with 𝑈 (1) transformation

11
of the 𝑓𝑖 → e𝑖 𝜃𝑖 𝑓𝑖 . The real and imaginary part of the 𝑎 𝑗𝑖 is
defined as:
𝑎 𝑗𝑖 = 𝜙 𝑗𝑖 + 𝑖 𝜒 𝑗𝑖 ; 𝜙 𝑗𝑖 = 𝜙¯ 𝑗𝑖 ; 𝜒 𝑗𝑖 = 𝜒¯ 𝑗𝑖 .

(A13)

The 𝜙 𝑗𝑖 and 𝜒 𝑗𝑖 are defined as
1 + 𝑧¯𝑖 𝑧 𝑗
1 + 𝑧¯ 𝑗 𝑧 𝑖


𝑆 + 𝑆𝑖𝑧 𝑆 + 𝑆 𝑧𝑗 + 𝑆𝑖− 𝑆 +𝑗

= 𝑖𝑆 log
;

𝑆 + 𝑆𝑖𝑧 𝑆 + 𝑆 𝑧𝑗 + 𝑆 −𝑗 𝑆𝑖+


1 + 𝑧¯𝑖 𝑧 𝑗 1 + 𝑧¯ 𝑗 𝑧𝑖


= −𝑆 log
1 + |𝑧𝑖 | 2 1 + |𝑧 𝑗 | 2
!
𝑆®𝑖 · 𝑆® 𝑗 1
+
.
= −𝑆 log
2
2𝑆 2
= 𝑖𝑆 log

𝜙 𝑗𝑖

𝜒 𝑗𝑖


𝑆
e 𝜒𝑖 𝑗 = 𝓌𝑖𝑆𝑗 1 + ℊ𝑖 𝑗 cos 𝑞®1 2®
𝑟 𝑖 + 𝑟®𝑖 𝑗
;

𝑧
𝑧¯
1 1 − |𝑧| 2 +
, 𝑆𝑖 =
, 𝑆𝑖− =
.
𝑆𝑖𝑧 =
2
2
2 1 + |𝑧|
1 + |𝑧|
1 + |𝑧| 2

(A15)

𝑖, 𝑗


1
;
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗

h
i


𝑞® 𝑟®
𝑟®
2 + cos 𝑞®1 𝑟®𝑖 𝑗 + 4 cos 12 𝑖 𝑗 + 1 cos 2𝑞®1 𝑟®𝑖 + 2𝑖 𝑗


.
𝑟®
cos 𝑞®1 𝑟®𝑖 𝑗 − cos 2𝑞®1 𝑟®𝑖 + 2𝑖 𝑗

(B3)

(A16)

!𝑆
∑︁
𝑆®𝑖 · 𝑆®𝑗 1
+
𝑓¯𝑖 𝑓𝑖 .
+
𝜇
2
2𝑆 2
𝑖

𝑡𝑖 𝑗 𝑓¯𝑖 𝑓 𝑗 e𝑖 𝜙 𝑗𝑖

𝜙 𝑗𝑖 = 2𝑆 atan
𝒽(𝑟) ≡

This transformation is analogous to gauge fixing by choosing a
specific rotational covariant frame. The dynamical fluxes do
not depend on the chosen covariant frame. Substituting Eq.
(A14) in the dynamical Hamiltonian Eq. (A8) we get:
∑︁

(B2)

Here we defined 𝑟®𝑖 𝑗 = 𝑟®𝑗 − 𝑟®𝑖 . The values of 𝓌𝑖 𝑗 and ℊ𝑖 𝑗 are
bounded ∈ [0, 1], and constant for a given 𝑞®1 and 𝑞®2 . The 𝜙 𝑗𝑖
is:


There is a one-to-one correspondence between the 𝑠𝑢(2) generators and their CS symbols [61]. Under 𝑆𝑈 (2) global rotation
𝜒 𝑗𝑖 remains intact, however, 𝜙 𝑗𝑖 transforms as:
𝜙 𝑗𝑖 → 𝜙 𝑗𝑖 + 𝜃 𝑖 − 𝜃 𝑗 .



1
1 cos 𝑞®2 𝑟®𝑖 𝑗
𝓌𝑖 𝑗 ≡ +
+
cos 𝑞®1 𝑟®,
2
4
4



1 cos 𝑞®2 𝑟®𝑖 𝑗
ℊ𝑖 𝑗 ≡
𝓌𝑖 𝑗 .
−
4
4

(A14)

Here, 𝑆®𝑖 stands for the CS symbols of the 𝑠𝑢(2) generators [59].
The corresponding values are:

𝐻=−

the form of 𝑎 𝑖 𝑗 in Eq. (A11) under global 𝑆𝑈 (2) rotation.
The coherent states symbols in Eq. (A15) also changes from
𝑆®𝑖 → −𝑆®𝑖 . For bipartite lattice the total Hamiltonian will
contain three parts depending on hopping of electrons: (i)
𝐴 → 𝐴, (ii) 𝐵 → 𝐵, (iii) 𝐴 → 𝐵. For 𝐴 → 𝐴 (𝑖, 𝑗 ∈ 𝐴) the
𝜒 𝑗𝑖 is:

(A17)

Physically, this represents the interaction of the underlying spin
field and itinerant spinless fermions.

Appendix B: Solution of Hamiltonian on a bipartite lattice

We use the Hamiltonian Eq. (A17) with the spin texture
Eq. (1) to analyze the topological properties of the two band
materials, as they are the simplest one. We take a bipartite
lattice L with two sub-lattices A and B: 𝐿 = 𝐴 ⊕ 𝐵. The charge
and spin degrees of freedom on A sub-lattice are 𝑓𝑖 and 𝑧𝑖
respectively. For convenience on sub-lattice B we can define:

The 𝜙 𝑗𝑖 is a periodic, but bounded function. 𝒽(𝑟) is also a
periodic function which depends only on the polar angle 𝑞®1 .
For 𝐵 → 𝐵 the 𝜒𝑖 𝑗 remains same. However, the 𝜙 𝑗𝑖 𝑖, 𝑗 ∈ 𝐵 →
−𝜙 𝑗𝑖 𝑖, 𝑗 ∈ 𝐴 + 2𝑆 𝑞®2 𝑟®𝑖 𝑗 [105]. Explicitly,

𝜙 𝑗𝑖 = 2𝑆 atan


1
+ 2𝑆 𝑞®2 𝑟®𝑖 𝑗 .
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗
(B4)

For 𝐴 → 𝐵 the 𝜒 𝑗𝑖 is:

e

𝜒𝑖 𝑗

= 𝓌𝑖′𝑆𝑗



1 − ℊ𝑖′ 𝑗 cos 2𝑞®1





𝑟®𝑖 𝑗
𝑟®𝑖 +
2



𝑆

1
1 cos 𝑞®2 𝑟®𝑖 𝑗
−
+
cos 𝑞®1 𝑟®𝑖 𝑗 ;
2
4
4



1 cos 𝑞®2 𝑟®𝑖 𝑗
′
′
ℊ𝑖 𝑗 ≡
−
𝓌𝑖 𝑗 ,
4
4

𝓌𝑖′ 𝑗 ≡

;
(B5)

and the phase
(0)

𝑖 𝜃𝑖

𝑓𝑖 → 𝑓𝑖 e

,

1
𝑧𝑖 → − ;
𝑧¯𝑖

𝑖 ∈ 𝐵.

(B1)

Where 𝜃 𝑖(0) ≡ 𝜃 𝑖 | 𝑢=0,𝑣=1 . Under these transformations the 𝜒 𝑗𝑖
(0)
remains unchanged, while the 𝜙 𝑗𝑖 → 𝜙𝑖 𝑗 + 𝜃 (0)
𝑗 − 𝜃 𝑖 . This
transformation makes the calculation easier, while conserving

e𝑖 𝜙 𝑗𝑖 = 𝑒 𝑖𝑆 ( 𝑞®2 𝑟®𝑖 𝑗 − 𝜋 ) .

(B6)

Substituting the above derived 𝜙 𝑗𝑖 and 𝜒𝑖 𝑗 in Eq. (A17), and
assuming the inter-lattice hopping parameter (𝑡1 ) and intra-

12
®
The wave vector
over the first Brillouin zone. The
 𝑘 is taken

matrix 𝜓 𝑘® = 𝑓 𝑘, 𝐴 𝑓 𝑘,𝐵 contains the creation operators of the
® momentum on the A and B sub-lattices. The single mode
𝑘-th
® = H0 ( 𝑘)
® · I + H𝑖 ( 𝑘)
® ·®
kernel of the Hamiltonian is H ( 𝑘)
𝜎𝑖 .
®
Here, I is the unit matrix; ®
𝜎𝑖 are the Pauli matrices, and H𝑖 ( 𝑘)
are the corresponding kernels [106]. To find an analytical
formulation of H ( ®𝑘) we first represent:

 ∑︁
′
1
atan
=
𝓅(𝑘 ′ )e−𝑖𝑘 𝑟 ; (B9)
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗
𝑘′

lattice hopping parameter (𝑡2 ) we find the total Hamiltonian:
𝐻=



𝑟®𝑖 𝑗 𝑆
𝑆
¯
− 𝑡2
𝑓𝑖 𝑓 𝑗 𝓌𝑖 𝑗 1 + ℊ𝑖 𝑗 cos 2𝑞®1 𝑟®𝑖 +
2
𝑖, 𝑗 ∈ 𝐴





1
exp +𝑖𝑆 2 atan
− 𝑞®2 𝑟®𝑖 𝑗
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗



∑︁
𝑟®𝑖 𝑗 𝑆
𝑆
¯
− 𝑡2
𝑓𝑖 𝑓 𝑗 𝓌𝑖 𝑗 1 + ℊ𝑖 𝑗 cos 2𝑞®1 𝑟®𝑖 +
2
𝑖, 𝑗 ∈ 𝐵





1
exp −𝑖𝑆 2 atan
− 𝑞®2 𝑟®𝑖 𝑗
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗



∑︁
𝑟®𝑖 𝑗 𝑆
′
′𝑆
¯
.
+ 𝑡1
𝑓𝑖 𝑓 𝑗 𝓌𝑖 𝑗 1 − ℊ𝑖 𝑗 cos 2𝑞®1 𝑟®𝑖 +
2
𝑖∈ 𝐴
∑︁

it is the Fourier series representation. As the value of 𝓅(𝑘 ′ ) ≪
1 for most of the 𝑞®1 , 𝑞®2 as shown in Fig. 14, we can approximate



1
exp 𝑖 2𝑆 atan
𝒽(𝑟) csc 𝑞®2 𝑟®𝑖 𝑗 + cot 𝑞®2 𝑟®𝑖 𝑗
(B10)
∑︁
′
≈ 1 + 𝑖2𝑆
𝓅(𝑘 ′ )e−𝑖𝑘 𝑟 .

𝑗∈𝐵

(B7)
The first two terms — corresponding to the hopping either
only on sub-lattice A, or on sub-lattice B respectively — are
complex conjugate of each other. The third term corresponding
to the hopping between sub-lattice A and B does not contain
the imaginary part. Hence, the Hamiltonian and its complex
conjugate are not identical to each other, which breaks the time
reversal symmetry. At 𝑞®1 = 0 or at 𝑞®2 = 0 the 𝜙 𝑗𝑖 in Eq. (B3)
and (B4) collapses. In this case there won’t be any topological
properties. It was expected as planar spin textures does not
show any THE.
q1 = ( /2, /8),q2 = ( /4, pi/6)

(r)

q1 = ( /4, 0),q2 = ( /4, 0)

(r)

(k)

8
/2




𝑟®𝑖 𝑗 𝑆
∗
H0 = −2𝑡2 𝓌𝑖𝑆𝑗 F̂ 1 + ℊ𝑖 𝑗 cos 2𝑞 1 𝑟®𝑖 +
2
(
)


∑︁
′
′
®
®
®
cos 𝑆 𝑞®2 𝑟®𝑖 𝑗 cos 𝑘 𝑟®𝑖 𝑗 + 2𝑆 sin 𝑆 𝑞®2 𝑟®𝑖 𝑗
𝓅(𝑘 ) cos 𝑘 + 𝑘 𝑟®𝑖 𝑗
𝑘′



-4

0

ky

0

-4

/2

-8
-4
1.0

0

x

4

0.5

/2

8
0.0

0.0

0.2

0

/2

kx
0.4

0.6

0.8

(k)

0
/2

 𝑆

∗ cos 𝑘®𝑟®𝑖 𝑗

𝑘′
-8

-4

1.0

0

4

x

1

/2

8

0

1

(a)

0.0

0.2

0

kx
0.4

0.6

/2

(B11)

0.8

Here, F̂ represents the Fourier transform operator; «∗» is the
convolution operator.

1.0

(b)

q1 = ( /4, /4),q2 = ( /4, /4)

(r)

𝑟®𝑖 𝑗
2




𝑟®𝑖 𝑗 𝑆
∗ sin 𝑘®𝑟®𝑖 𝑗
H𝑦 = +𝑡 1 𝓌𝑖′𝑆𝑗 F̂ 1 − ℊ𝑖′ 𝑗 cos 2𝑞 1 𝑟®𝑖 +
2



𝑟®𝑖 𝑗 𝑆
H𝑧 = −2𝑡 2 𝓌𝑖𝑆𝑗 F̂ 1 + ℊ𝑖 𝑗 cos 2𝑞 1 𝑟®𝑖 +
∗
2
(
)


∑︁
′
′
− sin 𝑆 𝑞®2 𝑟®𝑖 𝑗 sin 𝑘®𝑟®𝑖 𝑗 + 2𝑆 cos 𝑆 𝑞®2 𝑟®𝑖 𝑗
𝓅(𝑘 ) sin 𝑘® + 𝑘® 𝑟®𝑖 𝑗 .

-8
-8



H𝑥 = +𝑡 1 𝓌𝑖′𝑆𝑗 F̂ 1 − ℊ𝑖′ 𝑗 cos 2𝑞 1 𝑟®𝑖 +

/2

4

y

0

ky

y

Using this the kenel H ( ®𝑘) can be written as:

8

4

q1 = ( /4, /8),q2 = ( /4, 0)

(r)

(k)

(k)

Appendix C: Hamiltonian for higher integer spins 𝑆 = 2, 3, 4, . . .

8

8
/2

-4

0

0

ky

ky

0

/2

4

y

4

y

𝑘′

-4

/2

Here we analyze the Hamiltonian, Eq. (B11) (in main text
Eq. (2), for higher integer spins 𝑆 = 2, 3, . . . . In Eq. (B11)
only four terms depends on spin:

0
/2

-8

-8
-8

-4

1.0

0.5

0

4

0.0

0.5

x

/2

8
1.0

0.0

0.2

0

/2

kx
0.4

0.6

0.8

(c)

-8
1.0

-4
1

0

x
0

4

/2

8
1

0.0

0.2

0

0.4

0.6

0.8

(d)

FIG. 14. Real space spin texture generated from Eq. (1) for different
𝑞®1 and 𝑞®2 , and their corresponding Fourier transformation.

In momentum space the two band Hamiltonian can be written
as:
∑︁
𝐻 ( ®𝑘) =
𝜓¯ 𝑘® H ( ®𝑘)𝜓 𝑘® .
(B8)
𝑘®

"

/2

kx

1.0

𝑏® 𝑛
1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
2

!# 𝑆 


𝑎®𝑛 𝑆
, (C1)
, 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2

𝓌𝑛𝑆 , and 𝓌𝑛′𝑆 . The values of 𝓌𝑛 and 𝓌𝑛′ depend only on 𝑞®1
and 𝑞®2 . In Fig. 15 we plot the dependence of the 𝓌𝑛 and
𝓌𝑛′ on 𝑞®1 = (𝑞 1𝑥 , 0) and 𝑞®2 = (𝑞 2𝑥 , 0) for honeycomb lattice

√
√
NN and NNN vectors; here 𝑞 1𝑥 = 𝑞 2𝑥 ∈ − 3𝜋/2, 3𝜋/2 .
The same dependence for ℊ𝑛 and ℊ𝑛′ is shown in Fig. 6. We
observe that for all the cases the values of 𝓌𝑛 , 𝓌𝑛′ , ℊ𝑛 , and ℊ𝑛′
are always smaller than unity for most values of 𝑞 1𝑥 and 𝑞 2𝑥 .
It is equal to unity only at some specific values of 𝑞 1𝑥 and 𝑞 2𝑥 .

q2x

q2x

13
1(a1)

/2
0
/2

3(a3)

is:
H0 ≈ −2𝑡2

∑︁


𝓌𝑛𝑆

𝑛

1(b1)

/2
0
/2
/2 0

q1x

0.0

2(a2)

2(b2)

/2

/2 0

q1x

0.2

0.4

3(b3)

/2

/2 0

0.6

0.8

q1x

/2

1.0

FIG. 15. Dependence
of 
the 𝓌𝑛′ and 𝓌𝑛 on the wave vectors
√ 
√
𝑞®1 = 2𝑞 1𝑥 / 3, 0 and 𝑞®2 = 2𝑞 2𝑥 / 3, 0 on a honeycomb bipartite
√
√
lattice. The value of 𝑞 1𝑥 and 𝑞 2𝑥 changes from 3𝜋/2 to − 3𝜋/2.

As a first step, to find the expression for Hamiltonian, one
needs to expand the terms containing power of 𝑆 in Eq. (C1)
using binomial theorem:







𝑆ℊ𝑛
®
1+
cos 2𝑞®1 𝑏 𝑛 ×
2



 


′
′ ®
®
®
®
𝓅( 𝑘 ) cos 𝑘 + 𝑘 𝑏 𝑛




𝑘®′




∑︁
𝑆ℊ𝑛′
′𝑆
cos 2𝑞®1 𝑎®𝑛 × cos 𝑘® 𝑎®𝑛
H𝑥 ≈ +𝑡1
𝓌𝑛 1 −
2
𝑛


∑︁
𝑆ℊ𝑛′
cos 2𝑞®1 𝑎®𝑛 × sin 𝑘® 𝑎®𝑛
H𝑦 ≈ +𝑡1
𝓌𝑛′𝑆 1 −
2
𝑛


∑︁
𝑆ℊ𝑛
𝑆
®
H𝑧 ≈ −2𝑡2
𝓌𝑛 1 +
cos 2𝑞®1 𝑏 𝑛 ×
2
𝑛





cos 𝑆 𝑞®2 𝑏® 𝑛 cos 𝑘® 𝑏® 𝑛 + 2𝑆 sin 𝑞®2 𝑏® 𝑛

∑︁



 


′
′ ®
®
®
®
𝓅( 𝑘 ) sin 𝑘 + 𝑘 𝑏 𝑛 .




𝑘®′


(C3)
The only difference between Eq. (C3) with Eq. (4) is the power
of 𝓌𝑛 and 𝓌𝑛′ , and the pre-factor of 𝑆 in the term containing
ℊ𝑛 and ℊ𝑛′ . We should mention that, even if we have kept full
expansion given in Eq. (C2) still Eq. (C3) would have the
analogous form.
− sin 𝑆 𝑞®2 𝑏® 𝑛 sin 𝑘® 𝑏® 𝑛 + 2𝑆 cos 𝑆 𝑞®2 𝑏® 𝑛

∑︁

Appendix D: Hamiltonians for half-integer spins
Hamiltonian For spin 𝑆 = 1/2

1.

3

(q1ri)

2

3

2

0

2

3

2

0

1
0
-1
-2

"

!# 𝑆

𝑏® 𝑛
1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
=
2
!
!
!
!
𝑏® 𝑛
𝑏® 𝑛
𝑆
𝑆 2
2
1+
ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
+
+...;
2
2
1
2


𝑎®𝑛 𝑆
1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
=
2
!
!
!
!
𝑏® 𝑛
𝑏® 𝑛
𝑆 ′
𝑆 ′2
2
1−
ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
+
ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
−....
2
2
1
2
(C2)


We observe that the expansion contains the higher powers of ℊ𝑛′
and ℊ𝑛 . As the values of ℊ𝑛′ and ℊ𝑛 are never greater than unity
[see Fig. 6], we can neglect their higher powers. Keeping this
in mind one can approximate, Eq. (2) to first order in ℊ𝑛 and
ℊ𝑛′ . The Fourier transform of the approximated Hamiltonian

-3
3

2

0

q1 ri

2

3

FIG. 16. Plot of the function 𝒻( 𝑞®1 𝑟®𝑖 ) given in Eq. (D5). It is
applicable in the limit 𝑔𝑛 ≈ 1. (inset) The function 𝒻( 𝑞®1 𝑟®𝑖 ) can be
approximated by combining two dirac combs shifted by a phase 𝜋
w.r.t each other.

We first find the Hamiltonian, Eq. (2), for 𝑆 = 1/2. As there
is no Fourier transform for the functions


  1/2
𝑎®𝑛
F̂ 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2
"
! # 1/2
𝑏® 𝑛
F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
,
2

(D1)

14
we will find the Fourier transform for the limiting case of ℊ𝑛
and ℊ𝑛′ . When ℊ𝑛 ≪ 1 one can approximate:
! # 1/2
𝑏® 𝑛
F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
2
"
!#
ℊ𝑛
𝑏® 𝑛
≈ F̂ 1 +
.
cos 2𝑞®1 𝑟®𝑖 +
2
2

𝜋 compared to each other:
∑︁
∑︁
𝒻( 𝑞®1 𝑟®𝑖 ) ≈
𝛿( 𝑞®1 𝑟®𝑖 − 2𝑛𝜋) −
𝛿( 𝑞®1 𝑟®𝑖 − (2𝑛 + 1)𝜋) (D6)

"

𝑛

(D2)

(D3)

Hence, when ℊ𝑛 ≪ 1 and ℊ𝑛′ ≪ 1 the complete Hamiltonian
can be approximated as:
H0 ≈ −2𝑡2

Here, 𝛿 is the Dirac delta function. Hence, explicitly we will
have:


𝛾
F̂ 1 − √ 𝒻( 𝑞®1 𝑟®𝑖 )
2 2
)#
(
"
∑︁
∑︁
𝛾
𝛿( 𝑞®1 𝑟®𝑖 − 2𝑛𝜋) −
𝛿( 𝑞®1 𝑟®𝑖 − (2𝑛 + 1)𝜋)
= F̂ 1 − √
2 2 𝑛
𝑛
(D7)

When ℊ𝑛′ ≪ 1 one can approximate:
  1/2


𝑎®𝑛
F̂ 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2



′
ℊ
𝑎®𝑛
≈ F̂ 1 − 𝑛 cos 2𝑞®1 𝑟®𝑖 +
.
2
2

𝑛

The fourier transform of Dirac comb is known. The Fourier
transform of the first part of the Eq. (D7):
"
#
∑︁
∑︁
F
𝛿( 𝑞®1 𝑟®𝑖 − 2𝑛𝜋) =
2 cos (2𝑛𝜋)
(D8)
𝑛

𝑛

Similarly we can write the Fourier transform of the second part
of the Eq. (D7). When ℊ𝑛′ ≈ 1 we proceed the same way;
defining ℊ𝑛′ = 1 − 𝛾𝑛′ we will have:

i
h
ℊ𝑛
cos 2𝑞®1 𝑏® 𝑛 ×
𝓌𝑛 1 +
4
𝑛

∑︁



 


𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝑞® 𝑏® 𝑛
𝓅( 𝑘 ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛
cos 2 cos 𝑘® 𝑏® 𝑛 + sin 2


2
2


𝑘®′




′
∑︁
ℊ
𝓌𝑛′ 1 − 𝑛 cos 2𝑞®1 𝑎®𝑛 × cos 𝑘® 𝑎®𝑛
H𝑥 ≈ +𝑡1
4
𝑛


∑︁
ℊ′
𝓌𝑛′ 1 − 𝑛 cos 2𝑞®1 𝑎®𝑛 × sin 𝑘® 𝑎®𝑛
H𝑦 ≈ +𝑡 1
4
𝑛
i
h
∑︁
ℊ𝑛
𝓌𝑛 1 +
H𝑧 ≈ −2𝑡2
cos 2𝑞®1 𝑏® 𝑛 ×
4
𝑛








𝑎®𝑛 1/2
F̂ 1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2




𝛾𝑛′
1 − ℊ′
≈ F̂ 1 + √ 𝒻( 𝑞®1 𝑟®𝑖 ) = F̂ 1 + √ 𝑛 𝒻 ′ ( 𝑞®1 𝑟®𝑖 ) ;
2 2
2 2


𝑎®𝑛
cos 2𝑞®1 𝑟®𝑖 + 2

 .
𝒻 ′ ( 𝑞®1 𝑟®𝑖 ) ≡
sin 𝑞®1 𝑟®𝑖 + 𝑎®2𝑛



 


𝑞®2 𝑏® 𝑛
𝑞®2 𝑏® 𝑛 ∑︁ ® ′
′ ®
®
®
®
®
− sin
sin 𝑘 𝑏 𝑛 + cos
𝓅( 𝑘 ) sin 𝑘 + 𝑘 𝑏 𝑛 .


2
2


𝑘®′


(D4)





When ℊ𝑛 ≈ 1 one first need to approximate ℊ𝑛 = 1 − 𝛾𝑛 ;
where 𝛾𝑛 is a small quantity. Further substituting this in Eq.
(D1) we will get:

(D9)

As in Eq. (D5),
Eq. (D9) is applicable when the condition

1 + cos 2𝑞®1 𝑟®𝑖 − 𝑎®2𝑛 ≫ 𝛾 is satisfied. The function 𝒻 ′ ( 𝑞®1 𝑟®𝑖 )
is defined everywhere except in the vicinity of 𝑞®1 𝑟®𝑖 ≈ 𝜋/2 −
( 𝑞®1 𝑎®𝑛 /2). The Fourier transform of Eq. (D9) is found by the
same way as in Eq. (D7). Substituting the Fourier transforms of
Eq. (D7) and Eq. (D9) in Eq. (2) we will get the Hamiltonian:
)#
(
∑︁
1 − ℊ𝑛 ∑︁
cos(2𝑛𝜋)
−
cos(2𝑛𝜋)
×
√
2
𝑛
𝑛
𝑛




 




𝑞® 𝑏® 𝑛
𝑞® 𝑏® 𝑛 ∑︁ ® ′
cos 2 cos 𝑘® 𝑏® 𝑛 + sin 2
𝓅( 𝑘 ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛


2
2


𝑘®′


"
(
)#
′
∑︁
∑︁
∑︁
1−ℊ
H𝑥 = +𝑡 1
𝓌𝑛′ 1 + √ 𝑛
cos(2𝑛𝜋) −
cos(2𝑛𝜋) × cos 𝑘® 𝑎®𝑛
2
𝑛
𝑛
𝑛
(
)#
"
′
∑︁
∑︁
∑︁
1 − ℊ𝑛
′
H𝑥 = +𝑡 1
cos(2𝑛𝜋) −
cos(2𝑛𝜋) × sin 𝑘® 𝑎®𝑛
𝓌𝑛 1 + √
2
𝑛
𝑛
𝑛
"
(
)#
∑︁
∑︁
1 − ℊ𝑛 ∑︁
H𝑧 = −2𝑡 2
𝓌𝑛 1 − √
cos(2𝑛𝜋) −
cos(2𝑛𝜋) ×
2
𝑛
𝑛
𝑛




 




𝑞® 𝑏® 𝑛
𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝓅( 𝑘 ) sin 𝑘® + 𝑘® ′ 𝑏® 𝑛 .
− sin 2 sin 𝑘® 𝑏® 𝑛 + cos 2


2
2


𝑘®′


(D10)
"

"
F̂ 1 + ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +

𝑏® 𝑛
2

H0 = −2𝑡2

!# 1/2





𝛾𝑛
1 − ℊ𝑛
≈ F̂ 1 − √ 𝒻( 𝑞®1 𝑟®𝑖 ) = F̂ 1 − √ 𝒻( 𝑞®1 𝑟®𝑖 ) ;
2 2
2 2


𝑏®𝑛
cos 2𝑞®1 𝑟®𝑖 + 2

 .
𝒻( 𝑞®1 𝑟®𝑖 ) ≡
®
cos 𝑞®1 𝑟®𝑖 + 𝑏2𝑛

(D5)

Eq. (D5)
is applicable only when the condition 1 +

®
cos 2𝑞®1 𝑟®𝑖 + 𝑏2𝑛 ≫ 𝛾 is satisfied. Besides, the function
𝒻( 𝑞®1 𝑟®𝑖 ) is defined everywhere except in the vicinity of
𝑞®1 𝑟®𝑖 ≈ 𝜋/2 − ( 𝑞®1 𝑏® 𝑛 /2). In Fig. 16 we plot the function
𝒻( 𝑞®1 𝑟®𝑖 ) for 𝛾 = 0.1; with increase in 𝛾 the shape of the function does not change much. In fact one can approximate this
function using Dirac comb, i.e. we can write the function as
summation of the two opposite valued Dirac combs shifted by

∑︁

𝓌𝑛 1 −

The Hamiltonian for ℊ′ ≪ 1 and ℊ ≈ 1 is found by using above
mentioned approximation. Specifically one will combine the

15
H0 and H𝑧 from Eq. (D10) and H𝑥 and H𝑦 from Eq. (D4).
Explicitly:
"

(
)#
∑︁
1 − ℊ𝑛 ∑︁
H0 = −2𝑡 2
𝓌𝑛 1 − √
cos(2𝑛𝜋) −
cos(2𝑛𝜋) ×
2
𝑛
𝑛
𝑛




 




𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝑞® 𝑏® 𝑛
cos 2 cos 𝑘® 𝑏® 𝑛 + sin 2
𝓅( 𝑘 ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛


2
2


𝑘®′




∑︁
ℊ𝑛′
′
®
𝓌𝑛 1 −
cos 2𝑞®1 𝑎®𝑛 × cos 𝑘 𝑎®𝑛
H𝑥 = +𝑡1
4
𝑛


∑︁
ℊ′
H𝑦 = +𝑡1
𝓌𝑛′ 1 − 𝑛 cos 2𝑞®1 𝑎®𝑛 × sin 𝑘® 𝑎®𝑛
4
𝑛
)#
(
"
∑︁
∑︁
1 − ℊ𝑛 ∑︁
cos(2𝑛𝜋) −
cos(2𝑛𝜋) ×
H𝑧 = −2𝑡2
𝓌𝑛 1 − √
2
𝑛
𝑛
𝑛



 





𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝑞® 𝑏® 𝑛
𝓅( 𝑘 ) sin 𝑘® + 𝑘® ′ 𝑏® 𝑛 .
− sin 2 sin 𝑘® 𝑏® 𝑛 + cos 2


2
2


𝑘®′


(D11)
∑︁

Similarly, for ℊ′ ≪ 1 and ℊ ≈ 1 the Hamiltonian is found by
combining the H𝑥 and H𝑦 from Eq. (D10) and H0 and H𝑧
from Eq. (D4).

TABLE III. Table showing dot product between lattice vectors and
vectors 𝑞®1 , 𝑞®2 , and ®
𝐾.






2𝑞
2𝑞
𝐾® = ± √𝜋 , 0
Lat. Vect.
𝑞®1 = √1𝑥 , 0
𝑞®2 = √2𝑥 , 0
3
3
3
√

𝑎®1 = 23 , 12
𝑞 1𝑥
𝑞 2𝑥
± 𝜋2
 √

𝑎®2 = −2 3 , 12
−𝑞 1𝑥
−𝑞 2𝑥
∓ 𝜋2
𝑎®3 = (0,
 √1) 
𝑏® 1 = −2 3 , 23
 √

𝑏® 2 = −2 3 , 23
√ 
𝑏® 3 = 3, 0

0

0

−𝑞 2𝑥

∓ 𝜋2

−𝑞 1𝑥

−𝑞 2𝑥

∓ 𝜋2

2𝑞 1𝑥

2𝑞 2𝑥

±𝜋

The integer power term (square) can be approximated as [see
App. C]:

2


𝑎®𝑛
𝑎®𝑛
≈ 1 − 2ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
.
1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2
2
(D14)
For ℊ𝑛′ ≪ 1 the square root term can be:


  1/2



ℊ𝑛′
𝑎®𝑛
≈1−
cos 2𝑞®1 𝑟®𝑖 +
.
2
2
(D15)
Multiplying Eq. (D14) and (D15) and keeping the terms only
first order in ℊ𝑛′ we will have:


H0 = −2𝑡 2

0
−𝑞 1𝑥

h
i
ℊ𝑛
𝓌𝑛 1 +
cos 2𝑞®1 𝑏® 𝑛 ×
4
𝑛

∑︁

1 − ℊ𝑛′ cos 2𝑞®1



𝑎®𝑛
𝑟®𝑖 +
2



 


𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝑞® 𝑏® 𝑛
𝓅( 𝑘 ) cos 𝑘® + 𝑘® ′ 𝑏® 𝑛
cos 2 cos 𝑘® 𝑏® 𝑛 + sin 2


2
2


  5/2


𝑘®′


)#
(
"
𝑎®𝑛
′
′
∑︁
∑︁
∑︁
1 − ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
1−ℊ
2
cos(2𝑛𝜋) × cos 𝑘® 𝑎®𝑛
cos(2𝑛𝜋) −
𝓌𝑛′ 1 + √ 𝑛
H𝑥 = +𝑡1
(D16)


2
′
𝑛
𝑛
𝑛
5ℊ𝑛
𝑎®𝑛
"
)#
(
≈1−
cos 2𝑞®1 𝑟®𝑖 +
.
∑︁
∑︁
1 − ℊ′ ∑︁
2
2
𝓌𝑛′ 1 + √ 𝑛
H𝑥 = +𝑡1
cos(2𝑛𝜋) × sin 𝑘® 𝑎®𝑛
cos(2𝑛𝜋) −
2
𝑛
𝑛
𝑛
h
i
For arbitrary half-integer 𝑆 Eq. (D16) can be written as:
∑︁
ℊ𝑛
®
𝓌𝑛 1 +
H𝑧 = −2𝑡2
cos 2𝑞®1 𝑏 𝑛 ×
4

  (𝑆−1/2)/2+1/2

𝑛







 


𝑞® 𝑏® 𝑛 ∑︁ ® ′
𝑞® 𝑏® 𝑛
− sin 2 sin 𝑘® 𝑏® 𝑛 + cos 2
𝓅( 𝑘 ) sin 𝑘® + 𝑘® ′ 𝑏® 𝑛 .


2
2


𝑘®′







2.

(D12)

Hamiltonian For spin 𝑆 = 3/2, 5/2, . . .

𝑎®𝑛
1 − ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
2


𝑎®𝑛
≈ 1 − 𝑆ℊ𝑛′ cos 2𝑞®1 𝑟®𝑖 +
.
2

(D17)

The same trick can be applied for finding the Hamiltonian
for other cases of ℊ𝑛 and ℊ𝑛′ . The total Hamiltonian will be
analogous to the Eqs. (D4), (D10), (D11), and (D12).

Hamiltonian for higher half-integer spin can be found by
combining the aproximation made for 𝑆 = 1/2 and for 𝑆 =
2, 3, . . . in App. C. For example for 𝑆 = 5/2 one can write the
term:

Appendix E: Chern number Calculations for Honeycomb
bipartriate lattice

  5/2
𝑎®𝑛
𝑟®𝑖 +
2


2 

  1/2
𝑎®𝑛
𝑎®𝑛
′
′
= 1 − ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
1 − ℊ𝑛 cos 2𝑞®1 𝑟®𝑖 +
.
2
2
(D13)

We first calculate the Chern number for 𝑆 = 1 using the
Hamiltonian Eq. (4). As mentioned before the Chern number
is calculated at values of momentum ±𝐾® when the condition
H𝑥 = H𝑦 = 0 and H𝑧 ≠ 0 is satisfied simultaneously
[see

√ 
Sec. 3.5.6 of Ref. 62]. If we take 𝑞®1 = 2𝑞 1𝑥 / 3, 0 and



1 − ℊ𝑛′ cos 2𝑞®1



1.

Spin 𝑆 = 1

16


√ 
√ 
𝑞®2 = 2𝑞 2𝑥 / 3, 0 , then at the point 𝐾® = ±𝜋/ 3, 0 the
condition is satisfied identically. To see this, defining the three
NN (𝑎 𝑛 ) and NNN (𝑏 𝑛 ) lattice vectors of the honeycomb lattice,
in Eq. (4) for spin 𝑆 = 1 we will get:
ℊ′
H𝑥 = + 𝑡 1 𝓌1′ 1 − 1 cos 2𝑞®1 𝑎®1 × cos 𝑘® 𝑎®1
2


ℊ2′
′
+ 𝑡 1 𝓌2 1 −
cos 2𝑞®1 𝑎®2 × cos 𝑘® 𝑎®2
2


ℊ3′
′
+ 𝑡1 𝓌3 1 −
cos 2𝑞®1 𝑎®3 × cos 𝑘® 𝑎®3
2


1

/2

q2x



0

0.5

(E1)
/2

/2


ℊ1′
′
cos 2𝑞®1 𝑎®1 × sin 𝑘® 𝑎®1
H 𝑦 = + 𝑡 1 𝓌1 1 −
2


ℊ2′
′
+ 𝑡 1 𝓌2 1 −
cos 2𝑞®1 𝑎®2 × sin 𝑘® 𝑎®2
2


ℊ3′
′
cos 2𝑞®1 𝑎®3 × sin 𝑘® 𝑎®3
+ 𝑡 1 𝓌3 1 −
2

0

q1x



FIG. 17. Dependence of

𝑘′

(E2)

i
h
ℊ1
cos 2𝑞®1 𝑏® 1 ×
− 2𝑡 2 𝓌1 1 +
2
(
)


∑︁
− sin 𝑞®2 𝑏® 1 sin 𝑘® 𝑏® 1 + 2 cos 𝑞®2 𝑏® 1
𝓅 (𝑘 ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 1
𝑘′

h

− sin 𝑞®2 𝑏® 2 sin 𝑘® 𝑏® 2 + 2 cos 𝑞®2 𝑏® 2

∑︁



𝓅 (𝑘 ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 2

𝑘′

i
ℊ3
− 2𝑡 2 𝓌3 1 +
cos 2𝑞®1 𝑏® 3 ×
2
(

h
i
ℊ1
− 2𝑡2 𝓌1 1 +
cos 2𝑞 1𝑥 ×
2
(
)


∑︁
′
′
± sin 𝑞®2𝑥 + 2 cos 𝑞 2𝑥
𝓅 (𝑘 ) sin ±𝜋/2 + 𝑘® 𝑏® 1
𝑘′

i
ℊ2
cos 2𝑞 1𝑥 ×
− 2𝑡2 𝓌2 1 +
2
(
) (E6)


∑︁
′
′
± sin 𝑞®2𝑥 + 2 cos 𝑞 2𝑥
𝓅 (𝑘 ) sin ±𝜋/2 + 𝑘® 𝑏® 2
h

i
ℊ3
cos 2𝑞 1𝑥 ×
− 2𝑡2 𝓌3 1 +
2
(
)


∑︁
+2 cos 𝑞 2𝑥
𝓅 (𝑘 ′ ) sin ±𝜋 + 𝑘® ′ 𝑏® 3
h

𝑘′

∑︁



𝓅 (𝑘 ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 3 .

(E3)
In Eqs. (E1), (E2), and (E3) we explicitly wrote the all
three components of the H𝑥 , H𝑦 and 𝐻 𝑧 . We dropped the H0
component as it does not play any role in determining the Chern
number.
one need to substitute
the values of 𝑎®𝑛 , 𝑏® 𝑛,
 Further
√ 
√ 
√
𝑞®1 = 2𝑞 1𝑥 / 3, 0 , 𝑞®2 = 2𝑞 2𝑥 / 3, 0 , and 𝐾® = ±𝜋/ 3, 0
in above equations. In Tab. E 1 we have given the dot product
of these values. Substituting these in Eqs. (E1)(E2)(E3) we
will get:
H𝑥 = 0,

(E4)

H𝑦 =


and 𝑞®2 √
= (𝑞 2𝑥 , 0).
√ In the figure only the 𝑞 1𝑥 and 𝑞 2𝑥 value changes
from − 3𝜋/2 to 3𝜋/2. The same is applicable for 𝑏® 2 .

)

𝑘′

± 𝑡 1 𝓌1′

𝓅(𝑘 ′ ) sin (𝜋/2 + 𝑘 ′ 𝑏 1 ) on 𝑞®1 = (𝑞 1𝑥 , 0)

𝑘′

)

h

− sin 𝑞®2 𝑏® 3 sin 𝑘® 𝑏® 3 + 2 cos 𝑞®2 𝑏® 3

0

H𝑧 =

H𝑧 =

i
ℊ2
cos 2𝑞®1 𝑏® 2 ×
− 2𝑡 2 𝓌2 1 +
2
(

Í

/2




ℊ1′
ℊ2′
′
1−
cos 2𝑞®1𝑥 ∓ 𝑡 1 𝓌2 1 −
cos 2𝑞®1𝑥 = 0,
2
2
(E5)

We observe that all the terms of H𝑥 are identically zero; the
term involving 𝑎®1 and 𝑎®2 are zero as cos 𝑘® 𝑎®1 = cos 𝜋/2 = 0
and cos 𝑘® 𝑎®2 = cos 𝜋/2 = 0; the term involving 𝑎 3 is zero as
𝓌3 = 0. For H𝑦 the summation of all three terms are zero;
® 3 = sin 0 = 0; the terms
the term involving 𝑎®3 is zero as sin 𝑘𝑎
involving 𝑎®1 and 𝑎®2 are opposite of each other, hence they
cancel. The three terms of the H𝑧 are not zero at ®
𝐾.
®
For H𝑧 the term containing 𝑏 3 one can observe
that both

𝓅(𝑘 ′ ) ∼ 0 [see Fig. 14] and the term sin ±𝜋 + 𝑘® ′ 𝑏® 3 ∼ 0;
hence, we can neglect this term due to at least an order of
smallness compared to other two terms. The terms containing 𝑏® 1 and 𝑏® 2 controls the Chern number. In these,
usually the terms containing summation over 𝑘® ′ are negligible for most values of
Í 𝑞 1𝑥 ′ and 𝑞 2𝑥 ; in ′ Fig. 17 we
showed the summation
𝓅(𝑘 ) sin (𝜋/2 + 𝑘 𝑏 1 ) ≪ 1 at
𝑘′
 √ 
𝐾® = 𝜋/ 3, 0 for arbitrary values of the 𝑞 1𝑥 and 𝑞 2𝑥 . It

√ 
should be kept in mind that at 𝐾® = −𝜋/ 3, 0 the summation

17
Í
𝑘′

𝓅(𝑘 ′ ) sin (𝜋/2 + 𝑘 ′ 𝑏 1 ) ≪ 1 will be negative. Due to small-

ness of the summation, the term containing the same, won’t
have any effect on the
ÍChern number, except at values where
sin 𝑞 2𝑥 ≲ 2 |cos 𝑞 2𝑥 | 𝓅(𝑘 ′ ) sin (𝜋/2 + 𝑘 ′ 𝑏 1 ), which is in the
𝑘′
√
vicinity 𝑞 2𝑥 ∼ 0 and 𝑞 2𝑥 ∼ ±𝜋/ 3. Away from these areas
one can easily find the Chern number analytically. We will
neglect the term containing the 𝓅(𝑘 ′ ).
The values of ℊ𝑛′ and 𝓌𝑛 are always positive and less than
unity. Hence, they also won’t have any effect on Chern number.
Therefore the Chern number will be defined by only the term
sin (𝑞 2𝑥 ). The first Chern number is calculated by using the
formula [See Eq. (42) of Ref. 62]:
𝑐1 =
n

o
n

o
√
√
sgn H𝑧 𝐾® = (𝜋/ 3, 0) − sgn H𝑧 𝐾® = (−𝜋/ 3, 0)
2

.
(E7)

Explicitly the Chern number will be:
𝑐 1 = sgn [sin (𝑞 2𝑥 )] .

for arbitrary 𝑆 is:
H𝑧 ≈


𝑆ℊ1
− 2𝑡 2 𝓌1𝑆 1 +
cos 2𝑞®1 𝑏® 1 ×
2
(
)


∑︁
′
′
− sin 𝑆 𝑞®2 𝑏® 1 sin 𝑘® 𝑏® 1 + 2𝑆 cos 𝑆 𝑞®2 𝑏® 1
𝓅 (𝑘 ) sin 𝑘® + 𝑘® 𝑏® 1
𝑘′





𝑆ℊ2
− 2𝑡 2 𝓌2𝑆 1 +
cos 2𝑞®1 𝑏® 2 ×
2
(
)


∑︁
− sin 𝑆 𝑞®2 𝑏® 2 sin 𝑘® 𝑏® 2 + 2𝑆 cos 𝑆 𝑞®2 𝑏® 2
𝓅 (𝑘 ′ ) sin 𝑘® + 𝑘® ′ 𝑏® 2 .
𝑘′

(E9)


√ 
√ 
Using 𝐾® = ±𝜋/ 3, 0 , 𝑞®1 = 2𝑞 1𝑥 / 3, 0 and 𝑞®2 =

√ 
2𝑞 2𝑥 / 3, 0 and substituting the corresponding value from
Tab. E 1 in Eq. (E9) we will get:
H𝑧 ≈

(E8)



𝑆ℊ1
− 2𝑡2 𝓌1𝑆 1 +
cos 2𝑞 1𝑥 ×
2
(
)


∑︁
′®
′
®
− sin 𝑆𝑞 2𝑥 + 2𝑆 cos 𝑆𝑞 2𝑥
𝓅 (𝑘 ) sin 𝜋/2 + 𝑘 𝑏 1
𝑘′

2.

Spin 𝑆 = 2, 3, . . .

The approximate Hamiltonian for higher spins is given in Eq.
(C3). If one compares the Hamiltonian Eq. (C3) and (4) they
almost look identical, except for extra 𝑆 factors occurring in
different places. Comparing H𝑥 in Eq. (C3) and (4) one will
observe two changes: (i) 𝓌𝑛′ has a power of 𝑆; (ii) ℊ𝑛′ has an
extra coefficient 𝑆. However, the terms involving momentum
𝑘® remains same. The similar is true for H𝑦 . For H𝑧 one can
observe five changes: (i) 𝓌𝑛 has a power of 𝑆; (ii) ℊ𝑛 has an
®
extra coefficient 𝑆; (iii)
 the angle of sin 𝑞®2 𝑏 𝑛 has now an 𝑆
coefficient: sin 𝑆 𝑞®2 𝑏® 𝑛 ; (iv) the angle of cos 𝑞®2 𝑏® 𝑛 has now an


𝑆 coefficient: cos 𝑆 𝑞®2 𝑏® 𝑛 ; (v) the last term has a coefficient
2𝑆. However, as in H𝑥 and H𝑦 in H𝑧 also the term containing
momentum 𝑘® remains same.
The topological properties is found from the same condition
H𝑥 = H𝑦 = 0 and H𝑧 ≠ 0. The H𝑥 and H𝑧 are zero at
√
√
√
𝐾® = ±𝜋/ 3, 0 , 𝑞®1 = 2𝑞 1𝑥 / 3, 0 and 𝑞®2 = 2𝑞 2𝑥 / 3, 0
due to the same reasons as explained for the 𝑆 = 1 case. For
H𝑧 the term containing 𝑏® 3 can be neglected due to two order
of smallness as explained for 𝑆 = 1 case. Therefore the terms
containing 𝑏® 1 and 𝑏® 2 which are non zero at 𝐾® controls the
Chern number. For 𝑆 = 2 case the Chern number can be
described by Eq. (E7): 𝑐 1 = sgn [sin (2𝑞 2𝑥 )] for most part of
the 𝑞 1𝑥 and 𝑞 2𝑥 phase space. However with increasing spin 𝑆
the expression will not work. Hence, a more general expression
for Chern number is needed.
From Eq. (C3) the terms of H𝑧 corresponding to 𝑏® 1 and 𝑏® 2


𝑆ℊ2
cos 2𝑞 1𝑥 ×
1+
2
(
)


∑︁
′
′
− sin 𝑆𝑞 2𝑥 + 2𝑆 cos 𝑆𝑞 2𝑥
𝓅 (𝑘 ) sin 𝜋/2 + 𝑘® 𝑏® 2 .


− 2𝑡2 𝓌2𝑆

𝑘′

(E10)
Although the summation over 𝓅(𝑘 ′ ) is always small
as shown in Fig.
the whole term,
17, however,

Í
′
′
®
®
2𝑆 cos 𝑆𝑞 2𝑥 𝓅 (𝑘 ) sin 𝜋/2 + 𝑘 𝑏 1 , might not be small
𝑘′

compared to the previous term sin 𝑆𝑞 2𝑥 , due to the coefficient 2𝑆 present in it. Hence now the effect of term containing
𝓅(𝑘 ′ ) should also be included; for 𝑆 = 1 it was neglected due
to smallness. For ease of analysis we approximate the whole
term with a small term 𝜖 independent of 𝑞 1𝑥 and 𝑞 2𝑥 :
𝜖≡

∑︁



𝓅 (𝑘 ′ ) sin 𝜋/2 + 𝑘® ′ 𝑏® 1 .

(E11)

𝑘′

Explicitly we will write:
2𝑆 cos 𝑆𝑞 2𝑥

∑︁



𝓅 (𝑘 ′ ) sin 𝜋/2 + 𝑘® ′ 𝑏® 1 ≡ 2𝑆𝜖 cos 𝑆𝑞 2𝑥 .

𝑘′

(E12)
Value of 𝜖 is positve for +𝐾® and negative for − ®
𝐾. The value of
𝓌1 is always positive and less than unity [see Fig. 15], hence
they wont affect the Chern number. Similarly, ℊ𝑛 is always
positive and less than unity. However, its coefficients: (i) 𝑆 may
be large, (ii) cos 2𝑞 1𝑥 can
h take positive iand negative values.
𝑆ℊ
Hence, now the term 1 + 2 1 cos 2𝑞 1𝑥 can also affect the
Chern number depending on 𝑆 and 𝑞 1𝑥 . All the above analysis

18
is true for 𝑏® 2 also. The Chern number using Eq. (E7) will be:



𝑆ℊ2
cos 2𝑞 1𝑥 (sin 𝑆𝑞 2𝑥 − 2𝑆𝜖 cos 𝑆𝑞 2𝑥 )
𝑐 1 = sign 1 +
2
(E13)

Appendix F: Neel type Skyrmion

3

1.00
0.75

2

0.50
0.25

0

0.00

Sz

y

1

0.25

-1

0.50

-2
-3

𝑟 𝑖 | is the length of the position vector at 𝑖-th site; 𝑥𝑖 (𝑦 𝑖 ) is
Here, |®
the 𝑥 (𝑦) component of the position vector 𝑟®𝑖 ; 𝑟 0 is the maximum
length of the Skx. 𝑝 is the polarity which represent the out of
plane of the magnetization of the Skx; its value changes from
+1 (−1) at the center to the −1 (+1) at the boundary. 𝜔 is the
vorticity which represent rotation of the magnetization around
the 𝑧-axis; it takes multiples of 2𝜋, 𝜔 = 0, ±1, ±2, . . . . 𝛾 is
the helicity which represent the rotation of the magnetization
around the 𝑖-th site. If we substitute 𝛾 = 0, 𝜔 = 1 and 𝜌 = 1
in Eq. (F1); and substituting 𝑥 𝑖 = |®
𝑟 𝑖 | cos 𝜙, 𝑦 𝑖 = |®
𝑟 𝑖 | sin 𝜙 we
will get:





𝑟 𝑖 | cos 𝜙
𝑆 
sin |𝑟𝜋0 | |®

 𝑥
 


 

𝑟 𝑖 | sin 𝜙  .
𝑆®𝑖,Skx = 𝑆 𝑦  = 𝑆  sin |𝑟𝜋0 | |®
 

 


𝑆𝑧 

𝑟𝑖 |

 
 cos |𝑟𝜋0 | |®



(F2)

0.75

-3

-2

-1

0

x

1

2

3

1.00

FIG. 18. Generation of single Neel type Skyrmion from Eq. (1).

Interestingly one can easily show the equivalence of the
magnetic Skyrmions (Skx) to the spin texture given in Eq. (1)
in specific limits. The magnetic Skx is represented as [see Eq.
(8) of Ref. 107]:





𝑟 𝑖 | | 𝑥𝑟®𝑖𝑖 | cos 𝛾 − 𝜔 | 𝑟𝑦®𝑖𝑖 | sin 𝛾 
𝑆 
sin |𝑟𝜋0 | |®
 𝑥





 

𝑟 𝑖 | | 𝑥𝑟®𝑖𝑖 | sin 𝛾 + 𝜔 | 𝑟𝑦®𝑖𝑖 | sin 𝛾  .
𝑆®𝑖,Skx = 𝑆 𝑦  = 𝑆  sin |𝑟𝜋0 | |®

 




𝑆𝑧 

𝜌 cos |𝑟𝜋0 | |®
𝑟𝑖 |

 



(F1)

[1] P. Bruno, V. K. Dugaev, and M. Taillefumier, Topological Hall
Effect and Berry Phase in Magnetic Nanostructures, Physical
Review Letters 93, 096806 (2004).
[2] S.-S. Zhang, H. Ishizuka, H. Zhang, G. B. Halász, and C. D.
Batista, Real-space Berry curvature of itinerant electron systems
with spin-orbit interaction, Physical Review B 101, 024420
(2020).
[3] G. Kimbell, C. Kim, W. Wu, M. Cuoco, and J. W. A. Robinson,
Challenges in identifying chiral spin textures via the topological
Hall effect, Communications Materials 3, 1 (2022).
[4] H. Wang, Y. Dai, G.-M. Chow, and J. Chen, Topological hall
transport: Materials, mechanisms and potential applications,
Progress in Materials Science 130, 100971 (2022).
[5] M. Raju, A. Yagil, A. Soumyanarayanan, A. K. C. Tan, A. Almoalem, F. Ma, O. M. Auslaender, and C. Panagopoulos, The
evolution of skyrmions in Ir/Fe/Co/Pt multilayers and their
topological Hall signature, Nature Communications 10, 696

Physically it represents the Neel-type Skx [107]. In Eq. (F2)
one needs to map 𝜙 → 𝑞 2 atan 2(𝑟 𝑖 ) and |𝑟𝜋0 | |®
𝑟 𝑖 | → 𝑞 1 |®
𝑟 𝑖 | to
see the similarity with Eq. (1). In contrast to Eq. (1) now the
spin modulating vectors become scalars. Besides for a single
Skx (not Skx lattice) the 𝑞 1 and 𝑞 2 can not be chosen arbitrary,
they are fixed:

𝑞 2 = 1,

𝑞1 =

𝜋
.
𝑟0

(F3)

In Fig. 18 we plotted the Skx spin texture using Eq. (F2).

(2019).
[6] A. Soumyanarayanan, M. Raju, A. L. Gonzalez Oyarce, A. K. C.
Tan, M.-Y. Im, A. P. Petrović, P. Ho, K. H. Khoo, M. Tran,
C. K. Gan, F. Ernult, and C. Panagopoulos, Tunable roomtemperature magnetic skyrmions in Ir/Fe/Co/Pt multilayers,
Nature Materials 16, 898 (2017).
[7] Q. Shao, Y. Liu, G. Yu, S. K. Kim, X. Che, C. Tang, Q. L. He,
Y. Tserkovnyak, J. Shi, and K. L. Wang, Topological Hall effect
at above room temperature in heterostructures composed of a
magnetic insulator and a heavy metal, Nature Electronics 2,
182 (2019).
[8] L. Wang, Q. Feng, Y. Kim, R. Kim, K. H. Lee, S. D. Pollard,
Y. J. Shin, H. Zhou, W. Peng, D. Lee, W. Meng, H. Yang, J. H.
Han, M. Kim, Q. Lu, and T. W. Noh, Ferroelectrically tunable
magnetic skyrmions in ultrathin oxide heterostructures, Nature
Materials 17, 1087 (2018).
[9] Y. Shiomi, S. Iguchi, and Y. Tokura, Emergence of topolog-

19
ical Hall effect from fanlike spin structure as modified by
Dzyaloshinsky-Moriya interaction in MnP, Physical Review B
86, 180404 (2012).
[10] N. J. Ghimire, R. L. Dally, L. Poudel, D. C. Jones, D. Michel,
N. T. Magar, M. Bleuel, M. A. McGuire, J. S. Jiang, J. F.
Mitchell, J. W. Lynn, and I. I. Mazin, Competing magnetic
phases and fluctuation-driven scalar spin chirality in the kagome
metal YMn 6 Sn 6 , Science Advances 6, eabe2680 (2020).
[11] M. Afshar and I. I. Mazin, Spin spiral and topological Hall
effect in Fe3 Ga4 , Physical Review B 104, 094418 (2021).
[12] Y. Fujishiro, N. Kanazawa, T. Nakajima, X. Z. Yu, K. Ohishi,
Y. Kawamura, K. Kakurai, T. Arima, H. Mitamura, A. Miyake,
K. Akiba, M. Tokunaga, A. Matsuo, K. Kindo, T. Koretsune, R. Arita, and Y. Tokura, Topological transitions among
skyrmion- and hedgehog-lattice states in cubic chiral magnets,
Nature Communications 10, 1059 (2019).
[13] L. Vistoli, W. Wang, A. Sander, Q. Zhu, B. Casals, R. Cichelero,
A. Barthélémy, S. Fusil, G. Herranz, S. Valencia, R. Abrudan,
E. Weschke, K. Nakazawa, H. Kohno, J. Santamaria, W. Wu,
V. Garcia, and M. Bibes, Giant topological Hall effect in
correlated oxide thin films, Nature Physics 15, 67 (2019).
[14] R. Wiesendanger, Nanoscale magnetic skyrmions in metallic
films and multilayers: A new twist for spintronics, Nature
Reviews Materials 1, 1 (2016).
[15] A. Fert, N. Reyren, and V. Cros, Magnetic skyrmions: Advances
in physics and potential applications, Nature Reviews Materials
2, 1 (2017).
[16] M. Ezawa, Giant Skyrmions Stabilized by Dipole-Dipole Interactions in Thin Ferromagnetic Films, Physical Review Letters
105, 197202 (2010).
[17] C. D. Batista, S.-Z. Lin, S. Hayami, and Y. Kamiya, Frustration
and chiral orderings in correlated electron systems, Reports on
Progress in Physics 79, 084504 (2016).
[18] K. Karube, J. S. White, D. Morikawa, C. D. Dewhurst, R. Cubitt,
A. Kikkawa, X. Yu, Y. Tokunaga, T.-h. Arima, H. M. Rønnow,
Y. Tokura, and Y. Taguchi, Disordered skyrmion phase stabilized
by magnetic frustration in a chiral magnet, Science Advances
4, eaar7043 (2018).
[19] A. O. Leonov, I. M. Tambovtcev, I. S. Lobanov, and V. M.
Uzdin, Stability of in-plane and out-of-plane chiral skyrmions
in epitaxial MnSi(111)/Si(111) thin films: Surface twists versus
easy-plane anisotropy, Physical Review B 102, 174415 (2020).
[20] M. Preißinger, K. Karube, D. Ehlers, B. Szigeti, H.-A. Krug
von Nidda, J. S. White, V. Ukleev, H. M. Rønnow, Y. Tokunaga,
A. Kikkawa, Y. Tokura, Y. Taguchi, and I. Kézsmárki, Vital
role of magnetocrystalline anisotropy in cubic chiral skyrmion
hosts, npj Quantum Materials 6, 1 (2021).
[21] R. Ozawa, S. Hayami, and Y. Motome, Zero-Field Skyrmions
with a High Topological Number in Itinerant Magnets, Physical
Review Letters 118, 147205 (2017).
[22] H. Komatsu, Y. Nonomura, and M. Nishino, Phase diagram of the two-dimensional dipolar Heisenberg model with
Dzyaloshinskii-Moriya interaction and Ising anisotropy, Physical Review B 103, 214404 (2021).
[23] B. Li, J.-Q. Yan, D. M. Pajerowski, E. Gordon, A.-M. Nedić,
Y. Sizyuk, L. Ke, P. P. Orth, D. Vaknin, and R. J. McQueeney,
Competing Magnetic Interactions in the Antiferromagnetic
Topological Insulator MnBi2 Te4 , Physical Review Letters 124,
167204 (2020).
[24] W. Sun, W. Wang, J. Zang, H. Li, G. Zhang, J. Wang, and
Z. Cheng, Manipulation of Magnetic Skyrmion in a 2D van der
Waals Heterostructure via Both Electric and Magnetic Fields,
Advanced Functional Materials 31, 2104452 (2021).
[25] A. Bernand-Mantel, C. B. Muratov, and T. M. Simon, Unravel-

ing the role of dipolar versus Dzyaloshinskii-Moriya interactions
in stabilizing compact magnetic skyrmions, Physical Review B
101, 045416 (2020).
[26] J. F. Sierra, J. Fabian, R. K. Kawakami, S. Roche, and S. O.
Valenzuela, Van der Waals heterostructures for spintronics and
opto-spintronics, Nature Nanotechnology 16, 856 (2021).
[27] K. S. Burch, D. Mandrus, and J.-G. Park, Magnetism in twodimensional van der Waals materials, Nature 563, 47 (2018).
[28] S. Yang, T. Zhang, and C. Jiang, Van der Waals Magnets:
Material Family, Detection and Modulation of Magnetism,
and Perspective in Spintronics, Advanced Science 8, 2002488
(2021).
[29] Q. Tong, M. Chen, and W. Yao, Magnetic Proximity Effect in a
van der Waals Moire Superlattice, Physical Review Applied 12,
024031 (2019).
[30] P. Jiang, C. Wang, D. Chen, Z. Zhong, Z. Yuan, Z.-Y. Lu, and
W. Ji, Stacking tunable interlayer magnetism in bilayer CrI3 ,
Physical Review B 99, 144401 (2019).
[31] S. K. Behura, A. Miranda, S. Nayak, K. Johnson, P. Das,
and N. R. Pradhan, Moiré physics in twisted van der Waals
heterostructures of 2D materials, Emergent Materials 4, 813
(2021).
[32] K. Tran, J. Choi, and A. Singh, Moiré and beyond in transition
metal dichalcogenide twisted bilayers, 2D Materials 8, 022002
(2020).
[33] K. F. Mak, J. Shan, and D. C. Ralph, Probing and controlling magnetic states in 2D layered magnetic materials, Nature
Reviews Physics 1, 646 (2019).
[34] Q. H. Wang, A. Bedoya-Pinto, M. Blei, A. H. Dismukes,
A. Hamo, S. Jenkins, M. Koperski, Y. Liu, Q.-C. Sun, E. J.
Telford, H. H. Kim, M. Augustin, U. Vool, J.-X. Yin, L. H. Li,
A. Falin, C. R. Dean, F. Casanova, R. F. L. Evans, M. Chshiev,
A. Mishchenko, C. Petrovic, R. He, L. Zhao, A. W. Tsen, B. D.
Gerardot, M. Brotons-Gisbert, Z. Guguchia, X. Roy, S. Tongay,
Z. Wang, M. Z. Hasan, J. Wrachtrup, A. Yacoby, A. Fert,
S. Parkin, K. S. Novoselov, P. Dai, L. Balicas, and E. J. G.
Santos, The Magnetic Genome of Two-Dimensional van der
Waals Materials, ACS Nano 16, 6960 (2022).
[35] H. Kurebayashi, J. H. Garcia, S. Khan, J. Sinova, and S. Roche,
Magnetism, symmetry and spin transport in van der Waals
layered systems, Nature Reviews Physics 4, 150 (2022).
[36] Y. Zhang, Y. Gu, H. Weng, K. Jiang, and J. Hu, Mottness in
two-dimensional van der Waals Nb3 X8 monolayers (X=Cl, Br
and I), Physical Review B 107, 035126 (2023).
[37] M. Corasaniti, R. Yang, K. Sen, K. Willa, M. Merz, A. A.
Haghighirad, M. Le Tacon, and L. Degiorgi, Electronic correlations in the van der Waals ferromagnet Fe3 GeTe2 revealed by
its charge dynamics, Physical Review B 102, 161109 (2020).
[38] S. Sarkar and P. Kratzer, Electronic correlation, magnetic
structure, and magnetotransport in few-layer CrI3 , Physical
Review Materials 4, 104006 (2020).
[39] J.-X. Zhu, M. Janoschek, D. S. Chaves, J. C. Cezar, T. Durakiewicz, F. Ronning, Y. Sassa, M. Mansson, B. L. Scott,
N. Wakeham, E. D. Bauer, and J. D. Thompson, Electronic correlation and magnetism in the ferromagnetic metal Fe3 GeTe2 ,
Physical Review B 93, 144404 (2016).
[40] S. Ghosh, S. Ershadrad, V. Borisov, and B. Sanyal, Unraveling
effects of electron correlation in two-dimensional Fen GeTe2 (n
= 3, 4, 5) by dynamical mean field theory, npj Computational
Materials 9, 86 (2023).
[41] K. K. Kesharpu, E. A. Kochetov, and A. Ferraz, Topological
Hall effect induced by classical large-spin background: $su(2)$
path-integral approach, Physical Review B 107, 155146 (2023).
[42] M. J. Meĳer, J. Lucassen, R. A. Duine, H. J. Swagten, B. Koop-

20
mans, R. Lavrĳsen, and M. H. D. Guimarães, Chiral Spin Spirals
at the Surface of the van der Waals Ferromagnet Fe3 GeTe2 ,
Nano Letters 20, 8563 (2020).
[43] M.-G. Han, J. A. Garlow, Y. Liu, H. Zhang, J. Li, D. DiMarzio,
M. W. Knight, C. Petrovic, D. Jariwala, and Y. Zhu, Topological
Magnetic-Spin Textures in Two-Dimensional van der Waals
Cr2 Ge2 Te6 , Nano Letters 19, 7859 (2019).
[44] Z. Fei, B. Huang, P. Malinowski, W. Wang, T. Song, J. Sanchez,
W. Yao, D. Xiao, X. Zhu, A. F. May, W. Wu, D. H. Cobden, J.-H.
Chu, and X. Xu, Two-dimensional itinerant ferromagnetism in
atomically thin Fe3 GeTe2 , Nature Materials 17, 778 (2018).
[45] Y. Zhang, H. Lu, X. Zhu, S. Tan, W. Feng, Q. Liu, W. Zhang,
Q. Chen, Y. Liu, X. Luo, D. Xie, L. Luo, Z. Zhang, and X. Lai,
Emergence of Kondo lattice behavior in a van der Waals itinerant
ferromagnet, Fe3 GeTe2 , Science Advances 4, eaao6791 (2018).
[46] B. Ding, X. Li, Z. Li, X. Xi, Y. Yao, and W. Wang, Tuning
the density of zero-field skyrmions and imaging the spin configuration in a two-dimensional Fe3 GeTe2 magnet, NPG Asia
Materials 14, 1 (2022).
[47] L. Peng, F. S. Yasin, T.-E. Park, S. J. Kim, X. Zhang, T. Nagai,
K. Kimoto, S. Woo, and X. Yu, Tunable Néel–Bloch Magnetic
Twists in Fe3 GeTe2 with van der Waals Structure, Advanced
Functional Materials 31, 2103583 (2021).
[48] Y. Gao, S. Yan, Q. Yin, H. Huang, Z. Li, Z. Zhu, J. Cai, B. Shen,
H. Lei, Y. Zhang, and S. Wang, Manipulation of topological
spin configuration via tailoring thickness in van der Waals
ferromagnetic Fe5-x GeTe2 , Physical Review B 105, 014426
(2022).
[49] I. Lemesh and G. S. D. Beach, Twisted domain walls and
skyrmions in perpendicularly magnetized multilayers, Physical
Review B 98, 104402 (2018).
[50] G. Chen, T. Ma, A. T. N’Diaye, H. Kwon, C. Won, Y. Wu,
and A. K. Schmid, Tailoring the chirality of magnetic domain
walls by interface engineering, Nature Communications 4, 2671
(2013).
[51] J. A. Garlow, S. D. Pollard, M. Beleggia, T. Dutta, H. Yang, and
Y. Zhu, Quantification of Mixed Bloch-N\’eel Topological Spin
Textures Stabilized by the Dzyaloshinskii-Moriya Interaction
in Co/Pd Multilayers, Physical Review Letters 122, 237201
(2019).
[52] G. Chen, J. Zhu, A. Quesada, J. Li, A. T. N’Diaye, Y. Huo, T. P.
Ma, Y. Chen, H. Y. Kwon, C. Won, Z. Q. Qiu, A. K. Schmid,
and Y. Z. Wu, Novel Chiral Magnetic Domain Wall Structure
in Fe/Ni/Cu(001) Films, Physical Review Letters 110, 177204
(2013).
[53] E. C. S. F. R. S, Ferromagnetism, Reports on Progress in Physics
11, 43 (1947).
[54] K. Ohgushi, S. Murakami, and N. Nagaosa, Spin anisotropy
and quantum Hall effect in the kagomé lattice: Chiral spin state
based on a ferromagnet, Physical Review B 62, R6065 (2000).
[55] F. D. M. Haldane, Model for a Quantum Hall Effect without
Landau Levels: Condensed-Matter Realization of the "Parity
Anomaly", Physical Review Letters 61, 2015 (1988).
[56] Kondo lattice model is derived from the periodic Anderson
model in the strong correlation regime [108, 109]. Periodic
Anderson model takes into account the hybridization of the
localized 𝑓 electrons.
[57] I. Ivantsov, A. Ferraz, and E. Kochetov, Strong correlation,
Bloch bundle topology, and spinless Haldane–Hubbard model,
Annals of Physics 441, 168859 (2022).
𝑝𝑞
[58] The Hubbard operators 𝑋𝑖 ≡ ⟨𝑝|𝑞⟩ describes the transition
at site from | 𝑝⟩ state to |𝑞⟩ state. Under strong correlation there
are three different states possible, i.e. states with up-spin |↑⟩,

↑0

down-spin |↓⟩ and empty site |0⟩. Hence, for example 𝑋𝑖
represent the transition from empty state to the up-spin state at
𝑖-th site. In terms of usual electron creation (𝑐†𝑖 𝜎 ), annihilation
(𝑐 𝑖 𝜎 ), and number (𝑛𝑖 𝜎 = 𝑐†𝑖 𝜎 𝑐 𝑖 𝜎 ) operators, the Hubbard
operators are represented as:
𝑋𝑖0𝜎 = 𝑐 𝑖 𝜎 (1 − 𝑛𝑖 𝜎 ′ ), 𝑋𝑖𝜎0 = (1 − 𝑛𝑖 𝜎 ′ )𝑐†𝑖 𝜎
∑︁
(1 − 𝑛𝑖 𝜎 ′ ) 𝑐†𝑖 𝜎 𝑐†𝑖 𝜎 (1 − 𝑛𝑖 𝜎 ′ ) .
𝑋𝑖00 = 1 −
𝜎

Above definition of Hubbard operators shows that the no double
occupancy condition is satisfied.
[59] A. Ferraz and E. Kochetov, Fractionalization of strongly correlated electrons as a possible route to quantum Hall effect
without magnetic field, Physical Review B 105, 245128 (2022).
[60] A. Ferraz and E. A. Kochetov, Effective action for strongly
correlated electron systems, Nuclear Physics B 853, 710 (2011).
[61] F. A. Berezin, Introduction to Superanalysis, edited by A. A.
Kirillov (Springer Netherlands, Dordrecht, 1987).
[62] M. Fruchart and D. Carpentier, An introduction to topological
insulators, Comptes Rendus Physique 14, 779 (2013).
[63] When 𝑞®1 = 0 the 𝜙 𝑗𝑖 = 0 in Eq. (B3). In this case the time
reversal symmetry is conserved.
[64] N. Nagaosa and Y. Tokura, Topological properties and dynamics
of magnetic skyrmions, Nature Nanotechnology 8, 899 (2013).
[65] J. Seo, D. Y. Kim, E. S. An, K. Kim, G.-Y. Kim, S.-Y. Hwang,
D. W. Kim, B. G. Jang, H. Kim, G. Eom, S. Y. Seo, R. Stania,
M. Muntwiler, J. Lee, K. Watanabe, T. Taniguchi, Y. J. Jo,
J. Lee, B. I. Min, M. H. Jo, H. W. Yeom, S.-Y. Choi, J. H. Shim,
and J. S. Kim, Nearly room temperature ferromagnetism in a
magnetic metal-rich van der Waals metal, Science Advances 6,
eaay8912 (2020).
[66] D. Kim, C. Lee, B. G. Jang, K. Kim, and J. H. Shim, Drastic
change of magnetic anisotropy in Fe3 GeTe2 and Fe4 GeTe2
monolayers under electric field studied by density functional
theory, Scientific Reports 11, 17567 (2021).
[67] C. Gong, L. Li, Z. Li, H. Ji, A. Stern, Y. Xia, T. Cao, W. Bao,
C. Wang, Y. Wang, Z. Q. Qiu, R. J. Cava, S. G. Louie, J. Xia,
and X. Zhang, Discovery of intrinsic ferromagnetism in twodimensional van der Waals crystals, Nature 546, 265 (2017).
[68] S. Selter, G. Bastien, A. U. B. Wolter, S. Aswartham, and
B. Büchner, Magnetic anisotropy and low-field magnetic phase
diagram of the quasi-two-dimensional ferromagnet Cr2 Ge2 Te6 ,
Physical Review B 101, 014440 (2020).
[69] A. O. Fumega, S. Blanco-Canosa, H. Babu-Vasili, P. Gargiani,
H. Li, J.-S. Zhou, F. Rivadulla, and V. Pardo, Electronic structure and magnetic exchange interactions of Cr-based van der
Waals ferromagnets. A comparative study between CrBr3 and
Cr2 Ge2 Te6 , Journal of Materials Chemistry C 8, 13582 (2020).
[70] S. Tomar, B. Ghosh, S. Mardanya, P. Rastogi, B. S. Bhadoria, Y. S. Chauhan, A. Agarwal, and S. Bhowmick, Intrinsic
magnetism in monolayer transition metal trihalides: A comparative study, Journal of Magnetism and Magnetic Materials 489,
165384 (2019).
[71] M. A. McGuire, H. Dixit, V. R. Cooper, and B. C. Sales,
Coupling of Crystal Structure and Magnetism in the Layered,
Ferromagnetic Insulator CrI 3 , Chemistry of Materials 27, 612
(2015).
[72] D. Soriano, C. Cardoso, and J. Fernández-Rossier, Interplay
between interlayer exchange and stacking in CrI3 bilayers, Solid
State Communications 299, 113662 (2019).
[73] H. Zhang, W. Yang, P. Cui, X. Xu, and Z. Zhang, Prediction
of monolayered ferromagnetic CrMnI6 as an intrinsic high-

21
temperature quantum anomalous Hall system, Physical Review
B 102, 115413 (2020).
[74] S. Zhang, X. Li, H. Zhang, P. Cui, X. Xu, and Z. Zhang,
Giant Dzyaloshinskii-Moriya interaction, strong XXZ-type
biquadratic coupling, and bimeronic excitations in the twodimensional CrMnI6 magnet, npj Quantum Materials 8, 1
(2023).
[75] K. Wang, S. Nikolaev, W. Ren, and I. Solovyev, Giant contribution of the ligand states to the magnetic properties of the
Cr2 Ge2 Te6 monolayer, Physical Chemistry Chemical Physics
21, 9597 (2019).
[76] K. Yamagami, Y. Fujisawa, B. Driesen, C. H. Hsu,
K. Kawaguchi, H. Tanaka, T. Kondo, Y. Zhang, H. Wadati,
K. Araki, T. Takeda, Y. Takeda, T. Muro, F. C. Chuang, Y. Niimi,
K. Kuroda, M. Kobayashi, and Y. Okada, Itinerant ferromagnetism mediated by giant spin polarization of the metallic ligand
band in the van der Waals magnet Fe5 GeTe2 , Physical Review
B 103, L060403 (2021).
[77] X. Xu, Y. W. Li, S. R. Duan, S. L. Zhang, Y. J. Chen, L. Kang,
A. J. Liang, C. Chen, W. Xia, Y. Xu, P. Malinowski, X. D. Xu,
J.-H. Chu, G. Li, Y. F. Guo, Z. K. Liu, L. X. Yang, and Y. L.
Chen, Signature for non-Stoner ferromagnetism in the van der
Waals ferromagnet Fe3 GeTe2 , Physical Review B 101, 201104
(2020).
[78] L. Craco, S. S. Carara, Y.-C. Shao, Y.-D. Chuang, and
B. Freelon, Mott localization in the van der Waals crystal
CrI3 : A GGA+DMFT study, Physical Review B 102, 195130
(2020).
[79] O. Besbes, S. Nikolaev, N. Meskini, and I. Solovyev, Microscopic origin of ferromagnetism in the trihalides CrCl3 and
CrI3 , Physical Review B 99, 104432 (2019).
[80] Y. O. Kvashnin, A. N. Rudenko, P. Thunström, M. Rösner, and
M. I. Katsnelson, Dynamical correlations in single-layer CrI3 ,
Physical Review B 105, 205124 (2022).
[81] G. Menichetti, M. Calandra, and M. Polini, Electronic structure
and magnetic properties of few-layer Cr2 Ge2 Te6 : The key role
of nonlocal electron–electron interaction effects, 2D Materials
6, 045042 (2019).
[82] R. Cheng, M. Li, A. Sapkota, A. Rai, A. Pokhrel, T. Mewes,
C. Mewes, D. Xiao, M. De Graef, and V. Sokalski, Magnetic
domain wall skyrmions, Physical Review B 99, 184412 (2019).
[83] W. Jiang, G. Chen, K. Liu, J. Zang, S. G. E. te Velthuis,
and A. Hoffmann, Skyrmions in magnetic multilayers, Physics
Reports Skyrmions in Magnetic Multilayers, 704, 1 (2017).
[84] C. Xu, J. Feng, S. Prokhorenko, Y. Nahas, H. Xiang, and
L. Bellaiche, Topological spin texture in Janus monolayers of
the chromium trihalides Cr(I, X)3 , Physical Review B 101,
060404 (2020).
[85] X. Li, C. Collignon, L. Xu, H. Zuo, A. Cavanna, U. Gennser,
D. Mailly, B. Fauqué, L. Balents, Z. Zhu, and K. Behnia,
Chiral domain walls of Mn3 Sn and their memory, Nature
Communications 10, 3021 (2019).
[86] T. Nagase, Y.-G. So, H. Yasui, T. Ishida, H. K. Yoshida,
Y. Tanaka, K. Saitoh, N. Ikarashi, Y. Kawaguchi, M. Kuwahara,
and M. Nagao, Observation of domain wall bimerons in chiral
magnets, Nature Communications 12, 3490 (2021).
[87] Y. Amari, C. Ross, and M. Nitta, Domain-wall skyrmion chain
and domain-wall bimerons in chiral magnets (2023).
[88] I. Lemesh, F. Büttner, and G. S. D. Beach, Accurate model of the
stripe domain phase of perpendicularly magnetized multilayers,
Physical Review B 95, 174423 (2017).
[89] F. Kammerbauer, F. Freimuth, R. Frömter, Y. Mokrousov, and
M. Kläui, Dzyaloshinskii–Moriya Interaction and Its CurrentInduced Manipulation, Journal of the Physical Society of Japan

92, 081007 (2023).
[90] B. Rana and Y. Otani, Towards magnonic devices based
on voltage-controlled magnetic anisotropy, Communications
Physics 2, 90 (2019).
[91] A. S. Ahmed, J. Rowland, B. D. Esser, S. R. Dunsiger, D. W.
McComb, M. Randeria, and R. K. Kawakami, Chiral bobbers
and skyrmions in epitaxial FeGe/Si(111) films, Physical Review
Materials 2, 041401 (2018).
[92] J. Rowland, S. Banerjee, and M. Randeria, Skyrmions in chiral
magnets with Rashba and Dresselhaus spin-orbit coupling,
Physical Review B 93, 020404 (2016).
[93] M. Schott, L. Ranno, H. Béa, C. Baraduc, S. Auffret,
and A. Bernand-Mantel, Electric field control of interfacial
Dzyaloshinskii-Moriya interaction in Pt/Co/AlOx thin films,
Journal of Magnetism and Magnetic Materials Magnetic Materials and Their Applications: In Memory of Dominique Givord,
520, 167122 (2021).
[94] B. Dai, M. Jackson, Y. Cheng, H. He, Q. Shu, H. Huang, L. Tai,
and K. Wang, Review of voltage-controlled magnetic anisotropy
and magnetic insulator, Journal of Magnetism and Magnetic
Materials 563, 169924 (2022).
[95] K. Nawaoka, S. Miwa, Y. Shiota, N. Mizuochi, and Y. Suzuki,
Voltage induction of interfacial Dzyaloshinskii–Moriya interaction in Au/Fe/MgO artificial multilayer, Applied Physics
Express 8, 063004 (2015).
[96] X. Ma, G. Yu, X. Li, T. Wang, D. Wu, K. S. Olsson,
Z. Chu, K. An, J. Q. Xiao, K. L. Wang, and X. Li, Interfacial control of Dzyaloshinskii-Moriya interaction in heavy
metal/ferromagnetic metal thin film heterostructures, Physical
Review B 94, 180408 (2016).
[97] H. Yang, O. Boulle, V. Cros, A. Fert, and M. Chshiev, Controlling Dzyaloshinskii-Moriya Interaction via Chirality Dependent
Atomic-Layer Stacking, Insulator Capping and Electric Field,
Scientific Reports 8, 12356 (2018).
[98] J. Jiang and W. Mi, Two-dimensional magnetic Janus monolayers and their van der Waals heterostructures: A review on
recent progress, Materials Horizons 10, 788 (2023).
[99] A. Manchon, J. Železný, I. M. Miron, T. Jungwirth, J. Sinova,
A. Thiaville, K. Garello, and P. Gambardella, Current-induced
spin-orbit torques in ferromagnetic and antiferromagnetic systems, Reviews of Modern Physics 91, 035004 (2019).
[100] P. B. Wiegmann, Superconductivity in strongly correlated
electronic systems and confinement versus deconfinement phenomenon, Physical Review Letters 60, 821 (1988).
[101] R. Shankar, Holes in a quantum antiferromagnet: A formalism
and some exact results, Nuclear Physics B 330, 433 (1990).
[102] W.-M. Zhang, D. H. Feng, and R. Gilmore, Coherent states:
Theory and some applications, Reviews of Modern Physics 62,
867 (1990).
[103] M. Stone, Supersymmetry and the quantum mechanics of spin,
Nuclear Physics B 314, 557 (1989).
[104] J. Maciejko and G. A. Fiete, Fractionalized topological insulators, Nature Physics 11, 385 (2015).
[105] On B sublattice 𝑆𝑖 → −𝑆𝑖 . Under this transformation the spin
part of the 𝜙 𝑗𝑖 in Eq. (A14) can be written as:



𝑆 − 𝑆𝑖𝑧 𝑆 − 𝑆 𝑧𝑗 + 𝑆𝑖− 𝑆 +𝑗



𝑆 − 𝑆𝑖𝑧 𝑆 − 𝑆 𝑧𝑗 + 𝑆 −𝑗 𝑆𝑖+



𝑆 + 𝑆𝑖𝑧 𝑆 + 𝑆 𝑧𝑗 + 𝑆 −𝑗 𝑆𝑖+ 𝑆 +𝑗 𝑆𝑖−


= 
· + −.
𝑆 + 𝑆𝑖𝑧 𝑆 + 𝑆 𝑧𝑗 + 𝑆𝑖− 𝑆 +𝑗 𝑆𝑖 𝑆 𝑗
.

22
® is a 2×2 matrix. In terms of Pauli matrices it is represented
[106] H ( 𝑘)
as

H ( ®𝑘) = H0 I + H𝑥 ( ®𝑘)𝜎𝑥 + H𝑦 ( ®𝑘)𝜎𝑦 + H𝑧 ( ®𝑘)𝜎𝑧 ,
where,
® =
H0 ( 𝑘)
H𝑧 ( ®𝑘) =

𝐻𝑖, 𝑗 ∈ 𝐴 + 𝐻𝑖, 𝑗 ∈ 𝐵
2
𝐻𝑖, 𝑗 ∈ 𝐴 − 𝐻𝑖, 𝑗 ∈ 𝐵
2



® = Re 𝐻𝑖 ∈ 𝐴, 𝑗 ∈ 𝐵 ,
, H𝑥 ( 𝑘)


, H𝑦 ( ®𝑘) = Im 𝐻𝑖 ∈ 𝐴, 𝑗 ∈ 𝐵 .

Here, I is the 2 × 2 unit matrix; 𝜎𝑥 , 𝜎𝑦 , and 𝜎𝑧 are the Pauli
matrices.
[107] B. Göbel, I. Mertig, and O. A. Tretiakov, Beyond skyrmions:
Review and perspectives of alternative magnetic quasiparticles,
Physics Reports Beyond Skyrmions: Review and Perspectives
of Alternative Magnetic Quasiparticles, 895, 1 (2021).
[108] H. Tsunetsugu, M. Sigrist, and K. Ueda, The ground-state phase
diagram of the one-dimensional Kondo lattice model, Reviews
of Modern Physics 69, 809 (1997).
[109] M. Gulacsi, The Kondo lattice model, Philosophical Magazine
86, 1907 (2006).


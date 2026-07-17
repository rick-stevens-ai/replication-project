<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2410.00820 -->

Topological orbital Hall effect caused by skyrmions and antiferromagnetic skyrmions
Börge Göbel,1, ∗ Lennart Schimpf,1 and Ingrid Mertig1

arXiv:2410.00820v3 [cond-mat.mes-hall] 12 Jan 2025

1

Institut für Physik, Martin-Luther-Universität Halle-Wittenberg, D-06099 Halle (Saale), Germany
(Dated: January 14, 2025)

Abstract. The topological Hall effect is a hallmark of topologically non-trivial magnetic textures such as magnetic skyrmions. It quantifies the transverse electric current that is generated once an electric field is applied and
occurs as a consequence of the emergent magnetic field of the skyrmion. Likewise, an orbital magnetization is
generated. Here we show that the charge currents are orbital polarized even though the conduction electrons
couple to the skyrmion texture via their spin. The topological Hall effect is accompanied by a topological orbital
Hall effect even for s electrons without spin-orbit coupling. As we show, antiferromagnetic skyrmions and antiferromagnetic bimerons that have a compensated emergent field, exhibit a topological orbital Hall conductivity
that is not accompanied by charge transport and can be orders of magnitude larger than the topological spin Hall
conductivity. Skyrmionic textures serve as generators of orbital currents that can transport information and give
rise to considerable orbital torques.

Introduction
Magnetic skyrmions are non-collinear spin textures that possess an innate stability due to their non-trivial real-space
topology [1–3]. They have been observed as individual magnetic objects [4–7] that may serve as carriers of information in
future storage technologies [5, 6]. At finite temperatures and
magnetic fields, they even form periodic lattices [7, 8] with a
rather homogeneous topological charge density nSk .
This topological charge density has been identified with
an effective magnetic field Bem ∝ nSk ez , called ‘emergent
field’ [3, 9] that affects the conduction electrons by changing the phase of the wave function; a Berry phase is accumulated [10, 11]. While the electron spins align with the
skyrmion texture, an effective Lorentz force acts on their
charges and leads to the emergence of transverse transport
phenomena: The topological Hall effect [12–14] describes
the emergence of a transverse charge current once an electric field is applied. It is the hallmark of the skyrmion crystal
phase and the magnitude of its resistivity can be used to measure the skyrmion and topological charge densities [15–17].
Since the spins align with the skyrmion texture, the currents
are also spin polarized and a topological spin Hall conductivity has been predicted [18–20]. When two skyrmions with
opposite topological charges are coupled to form an antiferromagnetic skyrmion [21–26], the topological spin Hall effect
is still present but it is not anymore accompanied by charge
transport [24, 27].
Different types of skyrmions have been observed on several
different length scales [28] and even nano-sized skyrmions
can be stabilized [8, 29]. In this case, the emergent field has
a magnitude of several thousand Tesla. As a consequence,
quantized transport effects occur [30–32] akin to the quantum
Hall effect in the presence of a large magnetic field [33–39].
In fact, if the coupling between conduction electron spins and
the skyrmion texture is strong, the system can be mapped to a
quantum Hall system [30–32] and Landau levels occur giving
rise to edge states in the form of skipping orbits.
Over the recent years, the orbital degree of freedom has

∗ Correspondence email address: boerge.goebel@physik.uni-halle.de

FIG. 1. Topological orbital Hall effect. The spin of the conduction
electron (black) aligns with the skyrmion texture (colored arrows; the
color resembles the out-of-plane orientation). While moving through
the skyrmion, the electron accumulates a Berry phase and is deflected
(topological Hall effect). Due to the cycloid trajectory (black), an
orbital angular momentum is generated and transported as an orbital
current (topological orbital Hall effect).

become increasingly relevant in the field of spinorbitronics,
manifesting itself in phenomena such as orbital magnetization [40–45], orbital torque [46, 47], orbital Edelstein effect [48, 49] and orbital Hall effect [50–77]. In the presence of
a magnetic field, charge currents form circular trajectories and
generate an orbital angular momentum that can be calculated
via the modern formulation of orbital magnetization [40–45].
This orbital magnetization has been considered for quantum
Hall systems as well as skyrmions [45, 78, 79]. Recently, we
have shown that the skipping orbits in quantum Hall systems
lead to orbital-polarized edge currents [67] that give rise to an
orbital Hall effect accompanying the (charge) Hall effect once
a transverse electric field is applied.
In this paper, we show that skyrmions give rise to a
topological orbital Hall effect (Fig. 1). The orbital currents
appear additionally to the topological (charge) Hall effect
giving rise to transverse orbital-polarized currents. By using
a tight-binding model and a Berry curvature approach, we
systematically compare the charge, spin and orbital Hall
conductivities. Furthermore, we analyze the edge states that

2

Lz

0

c

d

5

5

5

0

25
1.0

0.8

Energy [eV]

Energy [eV]

Energy [eV]

5

b

Energy [eV]

a

0

0

0.6

0

0.4

0.2

-25

-5

-5

0

0

π

-5

2π -10

-5

0

5

10

Lz
Lz
σxy
Hall conductivity σxy [e2 /h]σxy

Lz
Lz
σxy
Wave vector kx [1/λ]σxy

-5

0

50

100

150

Lz
Orbital Hall conductivity σxy
[e/2π ]

-4

-2

0

2

4

Sz
Spin Hall conductivity σxy
[e/4π ]

FIG. 2. Electronic transport in skyrmion crystals. a Band structure Eνk . The color code indicates the k- and band-resolved out-of-plane
orbital angular momentum Lz,ν (k) (blue: positive, red: negative). The band structure consists of 2 blocks corresponding to parallel and
anti-parallel spin alignment. b Hall conductivity σxy as a function of energy. It is quantized in units of e2 /h in the band gaps. c Orbital Hall
Lz
Sz
conductivity σxy
as a function of energy. d Spin Hall conductivity σxy
as a function of energy. These calculations correspond to a skyrmion
size of λ = 5a, and a Hund’s coupling of m = 5|t| = 5 eV.

occur when the skyrmion is on the nanometer scale. In this
scenario the emergent field of the skyrmion is extremely large
and Landau levels form. As we show, when two oppositely
magnetized skyrmions are coupled to form an antiferromagnetic skyrmion, the topological Hall effect is compensated
and only orbital and spin Hall effects emerge. Since the
orbital angular momentum of the conduction electrons in
a skyrmion system can be arbitrarily high, the topological
orbital Hall conductivity can be orders of magnitude larger
than the topological spin Hall conductivity.
Results and discussion
Spinorbitronic transport in non-collinear spin textures.
We consider a square lattice with lattice constant a = 2.76 Å
and a single s orbital per site for the conduction electrons.
The skyrmion texture is a rotational symmetric vector field
m(r) (normalized) with diameter λ which is shown in
Fig. 1 (for details see Methods section) that is formed by
energetically lower lying d electrons. The non-collinear
texture increases the magnetic unit cell to (λ/a) × (λ/a)
lattice sites.
The s-d Hamiltonian consists of a nearest-neighbor hopping term (amplitude t = −1 eV) and a Hund’s coupling term
(quantified by m)
X †
X
H=
t ci cj + m
mi · (c†i σci ).
(1)
⟨ij⟩

i

c†i and ci are the creation and annihilation operators at site i.
σ is the vector of the Pauli matrices characterizing the spin of
the conduction electrons. The eigenvalues Eνk are the band
structure (band index ν and wave vector k) and the eigenvec-

tors |νk⟩ will be used to determine the observables discussed
in this paper: Spin Sν,z (k) and orbital angular momentum
Lν,z (k), as well as the charge Hall conductivity σxy (EF ),
Sz
(EF ) and orbital Hall conductivity
spin Hall conductivity σxy
Lz
σxy (EF ) that are calculated as integrals over the Berry curvaz
(k) and orbital Berry
ture Ων,z (k), spin Berry curvature ΩSν,z
Lz
curvature Ων,z (k) over the Brillouin zone as functions of the
Fermi energy EF . For more details about the calculations, we
refer to the Methods section.
Band structure, orbital and spin angular momentum in
skyrmion textures. The band structure Eνk depends on the
strength of the Hund’s coupling m. Starting the discussion
from m = 0, all bands are spin degenerate and the band structure resembles the single tight-binding band of the square lattice E(k) = 2t[cos(kx a) + cos(ky a)] but backfolded into the
smaller magnetic Brillouin zone accounting for the skyrmion.
Upon increasing m, the electron spins start to align with the
skyrmion texture and the initially spin-degenerate bands start
to split. The band structure for m = 1 eV = |t| exhibits many
(avoided) band crossings and is shown in Fig. S1 of the Supplementary Material.
Once the coupling m is larger than the initial band
width 4|t|, the spins are almost completely aligned with the
skyrmion. Two blocks emerge – one for parallel spin alignment and one for antiparallel spin alignment – shifted by
±m, respectively. Results for m = 5 eV = 5|t| are shown
in Fig. 2(a). The bands in the two blocks are similar and
have a weak dispersion. In the limit of strong Hund’s coupling and large skyrmion sizes, the two blocks become completely equivalent. In this adiabatic limit, the bands are Landau levels akin to the bands of a quantum Hall system. In

3
c

b

n2/n’

±n
5

0

Lz

5

Energy [eV]

0

n

5

Energy [eV]

Energy [eV]

Energy [eV]

5

e

d

0

5

Energy [eV]

a

0

0

100
1.0

0.8

-5

0.6

0

-5

-5

-5

-5

0.4

0.2

-100
0

0

π

2π

-40

-20

0

20

40

Lz
Lz
Lz Lz
σxy Hall conductivity σxy [e2 /h]σxy
σxy
Wave vector kx [1/λ]σxy

0

1000

2000

3000

Lz
Orbital Hall conductivity σxy
[e/2π ]

-20

-10

0

10

20

Sz
Spin Hall conductivity σxy
[e/4π ]

0.0 0.1 0.2 0.3
Lz
Lz
σxy
DOS n'(E)σxy

FIG. 3. Simplified explanation of transport properties. a Band structure Eνk . The color code indicates the k- and band-resolved outof-plane orbital angular momentum Lz,ν (k) (blue: positive, red: negative). b Hall conductivity σxy as a function of energy. c Orbital Hall
Lz
Sz
conductivity σxy
as a function of energy. d Spin Hall conductivity σxy
as a function of energy. e Density of states n′ (E) of the band structure
of the underlying lattice E = 2t̃[cos(kx a) + cos(ky a)] shifted by ±m. The gray curves in b-d (scaled) resemble the trend expected based on
this zero-field band structure: ±n(E) in panel b, [n(E)]2 /n′ (E) in panel c, and n(E) in panel d. These calculations correspond to a skyrmion
size of λ = 10a and a Hund’s coupling of m = 5|t| = 5 eV.

Refs. [20, 31, 32], we have shown that the Hamiltonian hosting the non-collinear skyrmion texture can be transformed to
a quantum Hall Hamiltonian with a collinear magnetic field
coupling to the charge of the electrons. This magnetic field is
the ‘emergent field’ Bem mentioned in the introduction.
While the two blocks in the band structure are characterized by opposite spin alignment, that is rather homogeneous
within a block (Sν,z (k) ≈ ±ℏ/2 ⟨mz ⟩ with ⟨mz ⟩ the average
normalized out-of-plane magnetic moment of the skyrmion),
the orbital angular momentum Lν,z (k) is also roughly opposite comparing the two blocks but changes within a block. We
have added it as a color code to Fig. 2(a). Starting from the
lowest band, it is negative and increases in magnitude until it
changes sign near E = −m = −5 eV and decreases back to
zero. Its magnitude is much larger than the spin by multiple ℏ
(cf. legend in Fig. 2a).
Topological charge, spin and orbital Hall effect. The
analogy of the considered skyrmion system and a quantum
Hall system allows to understand the emergence of a topological Hall effect, as discussed in Refs. [31, 32]. Since the bands
are (at least partially) spin polarized, the corresponding currents are spin polarized, as discussed in Ref. [20]. Therefore, a
topological spin Hall conductivity occurs as well. As we have
just shown, the bands are also orbital polarized, so the emergence of a topological orbital Hall conductivity is expected as
well. The energy dependent curves of the Hall conductivity
Lz
σxy , orbital Hall conductivity σxy
and spin Hall conductivity
Sz
σxy are shown in Fig. 2(b-d), respectively. Note that the following discussion is only true in the strong-coupling limit of
the conduction electron spins and the magnetic texture. The

results for a weaker coupling of m = |t| = 1 eV are shown in
Fig. S1 of the Supplementary Material.
First, and most importantly, the orbital Hall conductivity
(panel c) is non-zero. This means, a skyrmion exhibits orbitaland spin-polarized currents; a topological orbital Hall effect is
superimposed on top of the previously observed topological
Hall and topological spin Hall effects.
Both orbital (c) and spin Hall conductivities (d) can exhibit
plateaus, e. g. between the two Landau levels near E = 3 eV.
However, the values are not quantized by a natural constant,
because spin and orbital angular momentum are no good
quantum numbers in the skyrmion system. The topological
Hall conductivity (b) on the other hand is quantized in units
of e2 /h due to the mathematical equivalence to a quantum
Hall system.
Since the electron spins align parallel with the skyrmion
in the lower block of the band structure and antiparallel in
the upper block, we see also two blocks in the conductivities. For the topological Hall effect (b), the signals are roughly
reversed, because the parallel and antiparallel alignment corresponds to an interaction with oppositely oriented emergent
fields Bem ∥ ±ez of the skyrmion. Both orbital (c) and
spin Hall conductivities (d) exhibit almost the same signals
comparing the two blocks because reversing the alignment of
the spins with the skyrmion texture does not only reverse the
emergent field but also Sz and Lz .
Within a block, the topological Hall conductivity (b) and
spin Hall conductivity (d) change sign. This is because the
electrons in the lower half of a block are characterized by a
positive effective mass and in the upper half by a negative effective mass (hole-like behavior) which is determined by the

4

FIG. 4. Edge states carrying orbital angular momentum. a Band structure of a slab with 10 skyrmions in the unit cell. The color indicates the
orbital angular momentum (see legend). Gray areas indicate bulk states, projected from the bulk band structure (cf. Fig. 2a). These calculations
correspond to a skyrmion size of λ = 5a, and a Hund’s coupling of m = 5|t| = 5 eV. b Zoom of the upper block for m = 900|t| = 900 eV
corresponding to the adiabatic limit of very strong coupling. c Layer-resolved probability of the two edge states highlighted in b, indicated
as (i) and (ii) . The unit cell is indicated in the middle. d Schematic visualization of the two edge states giving rise to charge currents j, spin
currents jS and orbital currents jL that are oriented oppositely at both edges. The magnetic skyrmions are resembled by the same color code
as in Fig. 1.

band structure of the underlying square lattice. Particles of opposite mass are deflected into opposite directions by the same
emergent magnetic field. However, by changing the sign of
the effective mass, Lz changes sign as well, as in classical
physics. For this reason, the orbital Hall conductivity (c) remains always positive.
Fig. 3 shows results analogous to Fig. 2 but for an increased
skyrmion diameter of λ = 10a. The main difference is that
there are more Landau levels and that the topological, orbital
and spin Hall conductivities as well as the orbital angular momentum are increased compared to λ = 5a. The scaling of
the Hall conductivities with the skyrmion area is shown in
Fig. S2 in the Supplementary Material. While the topological Hall and spin Hall conductivities increase linearly with the
skyrmion area, the orbital Hall conductivity increases quadratically.
The trend of the energy dependencies of the Hall conductivities can even be quantified based on the analysis of the zerofield band structure of the underlying square lattice E(k) =
2t[cos(kx a) + cos(ky a)] shifted by ±m. We relate the Hall
RE
conductivities to the carrier density n(E) = −∞ n′ (E ′ ) dE ′
and the density of states n′ (E). As a reasonable approxima-

tion, we can use the carrier density and density of states of the
zero-field band structure [32, 80]; shown in Fig. 3(e). Note
however that this simplified transport theory assumes large
skyrmions for which the Landau levels are dense as for the
case of λ = 10a presented in Fig. 3.
In the upper block of the band structure, where the conduction electrons feel a positive emergent field, the topological Hall conductivity is given by the carrier density n(E).
Note that we account for the electron-like and hole-like character of the states by the sign of n(E). In the lower block,
the topological Hall conductivity is reversed. In total, we find
σxy,approx (E) ∝ ±n(E) for the two blocks, respectively. The
spin Hall conductivity is roughly given by the product of the
topological Hall conductivity and the out-of-plane spin polarization that is opposite for the two blocks due to the opposite emergent field of the skyrmion acting on the correspondSz
ing conduction electrons. Therefore, σxy,approx
(E) ∝ n(E)
for both blocks. Likewise, the orbital Hall conductivity is
given as the product of the topological Hall conductivity and
the out-of-plane orbital angular momentum which scales with
Lz
±n/n′ . Therefore, σxy,approx
(E) ∝ [n(E)]2 /[n′ (E)] for
both blocks [67].
All three approximate dependencies have been added as

5
gray curves to Fig. 3(b-d). The approximation assumes a large
smooth skyrmion texture with a homogeneous emergent field.
The assumptions are not strictly fulfilled which shows in the
plateaus in the Hall conductivities that are not resembled and
the small deviations near the center of each block. Note also
the following technical detail: We have modified the hopping amplitude for the calculation of the density of states in
Fig. 3(e) to t̃ = cos(θij /2) t ≈ 0.9775 t to account for the
finite size of the skyrmion, as in Ref. [30]. θij is the angle
between two neighboring moments of the skyrmion.
Overall, the simplified explanation based on the density of
states resembles the topological Hall, spin Hall and orbital
Hall conductivities well. Also, it allows us to understand the
scaling of the effects with the skyrmion area. The orbital Hall
conductivity surpasses the spin Hall conductivity by orders of
magnitude because Lz can in principle have arbitrarily high
values while Sz is limited by ±ℏ/2. Lz scales roughly linearly
with the skyrmion area because larger skyrmions allow for
larger orbits. This leads to the quadratic dependence of the
orbital Hall conductivity on the skyrmion area presented in
Fig. S2(b) in the Supplementary Material.
To further confirm the validity of our calculations, we have
simulated the effect of disorder by adding random onsite energies in the range of [−0.2 eV, 0.2 eV]. As a result, we see
very similar conductivities, as presented in Fig. S3 in the Supplementary Material.
Edge states. By considering a slab geometry, we gain information about edge states contributing to the different transverse transport phenomena. We repeat the skyrmion unit cell
10 times along the y direction and keep periodicity along the
x direction. The corresponding band structure is shown in
Fig. 4a. Additionally, we have superimposed Lν,z (k∥ ) as a
color code (red and blue) and the projected bulk bands in gray.
Edge states are present that bridge the gaps between the bulk
states. As the main result, they are orbital and spin polarized.
The discussion becomes easier if we are in the adiabatic
limit where m ≫ |t|. Therefore, Fig. 4b shows the upper
block for m = 900|t| = 900 eV. Similar to the Landau levels appearing in the bulk, the edge states are orbital polarized
explaining the origin of the orbital Hall conductivity. In the
gap between the lowest two bands in the upper block, we observe two states labeled (i) and (ii). Fig. 4c shows that they
are located at opposite edges of the slab. Their orbital angular
momentum is positive and the spin and charge are negative.
This corresponds to the positive orbital Hall conductivity and
negative topological Hall and spin Hall conductivities calculated for the bulk at that energy. A schematic interpretation in
terms of skipping orbits is shown in Fig. 4d: By combining a
translational and rotational degree of freedom, orbital angular
momentum is transported along the edge as an orbital current.
Experimental detection. The detection of the orbital Hall
conductivity is challenging because orbital currents cannot be
measured directly. Three indirect approaches have been identified in the literature [67, 81]: (i) The orbital currents are injected into an attached ferromagnet where the spin-orbit coupling transforms them into spin currents that exhibit a torque
onto the magnetization that can be measured [47]. (ii) As our
slab calculations reveal, edge states occur that are orbital po-

larized. These states, as well as accumulation of orbital angular momentum can be measured by the magneto-optical Kerr
effect (MOKE) [62, 82]. (iii) The inverse orbital Hall effect
can be measured by injecting orbital currents and measuring
the charge current as a response, similar to how the inverse
orbital Edelstein effect was measured [49].
All three methods are applicable to observe the topological orbital Hall effect in skyrmion textures. However, besides the orbital contribution, a spin contribution emerges as
well. Our calculations presented in Fig. 2 have revealed that
the orbital Hall conductivity is always much larger than the
spin Hall conductivity in a skyrmion sample. Still, it is important to distinguish the individual contributions. For this
reason, we can utilize the dependence of the Hall conductivities on the skyrmion size; cf. Fig. S2 in the Supplementary Material. While the spin Hall conductivity scales linearly
with the skyrmion area, just as the topological Hall conductivity, the orbital Hall conductivity scales quadratically with
the skyrmion area. This is because the spin is limited by the
quantum number S = 1/2 but the orbital angular momentum
is not and increases with the skyrmion area. Due to this characteristic size dependence, the orbital Hall conductivity can be
extracted in an experiment by changing the skyrmion density
via a change in temperature or the external magnetic field. As
we will present in the following, this analysis becomes easier
for alternative magnetic textures beyond skyrmions, as some
of those textures do not exhibit a topological Hall effect or
spin Hall effect.
Different types of skyrmions.
Different types of
skyrmions have been observed in B20 materials such as
MnSi [2], magnetic multilayers like Ir/Fe/Co/Pt [83], centrosymmetric materials like Sc-doped barium ferrite [84], insulating multiferroics like Cu2 OSeO3 [85] and others. The
above discussed calculations can be repeated for other noncollinear spin textures related to skyrmions [28]. We start
by discussing other objects with a finite topological charge.
To classify such objects, one can introduce the topological
charge NSk = pv that is the product of polarity p = ±1
(out-of-plane orientation of the center magnetic moment) and
vorticity v = 0, ±1, ±2, .... The latter quantity relates the
polar angle of the position vector φ with the polar angle of
the magnetic texture ϕ via ϕ = vφ + γ. Here, γ is an offset
that is called helicity. Since the topological charge is independent of the helicity, Néel (γ = 0, π) and Bloch skyrmions
(γ = ±π/2) of otherwise equal profile and electronic properties exhibit the same topological Hall, spin Hall and orbital
Hall responses.
So far, we have discussed skyrmions that are characterized
by p = 1 and v = 1 so that they carry a topological charge of
NSk = +1. As a consequence, their emergent field for parallel spin-alignment points along +z. If we consider the same
skyrmions in a ferromagnetic background that is oriented oppositely, the polarity changes sign p = −1 and so does the
topological charge NSk = −1. As a consequence, the emergent field points along −z and so the topological Hall conductivity changes sign. However, the spin Hall conductivity and
the orbital Hall conductivity remain invariant because Sz and
Lz change sign as well, due to the reversed skyrmion texture

6
c

Energy [eV]

b

Energy [eV]

5

0

-5

d

e

5

5

Energy [eV]

a

0

-5

-5

0

5

-5

0

Lz
Lz
σxy
Hall conductivity σxy [e2 /h]σxy

0

200

400

600

800

Lz
Orbital Hall conductivity σxy
[e/2π ]

-10

-5

0

5

10

Sz
Spin Hall conductivity σxy
[e/4π ]

FIG. 5. Pure topological orbital Hall effect in antiferromagnetic skyrmion crystals. a Antiferromagnetic skyrmion in one layer. The
color resembles the out-of-plane orientation of the magnetic moments (arrows). b Synthetic antiferromagnetic skyrmion in two layers. c Hall
Sz
Lz
as a function of energy in an antiferromagnetic skyrmion
and e spin Hall conductivity σxy
conductivity σxy , d orbital Hall conductivity σxy
crystal characterized by second-nearest neighbor hopping t2 = −1 eV and a Hunds’s coupling strength of m = 5 eV and skyrmion size
λ = 8a.

and emergent field, respectively.
A similar discussion holds for antiskyrmions that have been
observed in the Heusler material MnPtSn [86] that are characterized by a negative vorticity v = −1. Antiskyrmions
and skyrmions in the same magnetic background (same polarity p) have opposite topological charges and therefore opposite emergent fields. As a consequence, they exhibit opposite topological Hall and spin Hall conductivities but the same
orbital Hall conductivities. If skyrmions and antiskyrmions
coexist at equal numbers, as is possible in frustrated magnets [29] or Heusler materials [87–90], the net topological
Hall and spin Hall conductivities are compensated but the orbital Hall effect is not which makes it ideal to detect topological magnetic textures if one is not sure about the type of
texture.
Fig. S4 in the Supplementary Material shows the numerically calculated Hall conductivities of a crystal of
Bloch skyrmions, antiskyrmions and bimerons (in-plane
skyrmions) [91, 92]. All three textures have been constructed
such that they have the same (or opposite) topological charge
density as the Néel skyrmion presented in Fig. 2. As long
as no spin-orbit coupling is considered, the Néel skyrmion,
Bloch skyrmion and bimeron have the same topological Hall
conductivity and the antiskyrmion has the exactly opposite
topological Hall conductivity due to the opposite topological charge density. The calculated spin Hall conductivitiy is
equal for the Néel and Bloch skyrmions and again opposite
for the antiskyrmion. The bimeron exhibits a vanishing spin
Sz
Hall conductivity σxy
because the out-of-plane net moment of
the bimeron is zero. Most importantly, all 4 textures exhibit
exactly the same orbital Hall conductivity.
The idea of coupling two skyrmionic textures with oppo-

site topological charges gave rise to other textures such as the
skyrmionium [93–95], the antiferromagnetic skyrmion [21–
26] or the antiferromagnetic bimeron [28, 92, 96]. In the
following, we will discuss the case of the antiferromagnetic
skyrmion in detail.
Pure topological orbital Hall effect in antiferromagnetic
skyrmions. To model an antiferromagnetic skyrmion, we take
the texture considered before and reverse every second magnetic moment in a checkerboard pattern (cf. Fig. 5a). This
allows to distinguish two skyrmions on two sublattices with
opposite magnetic moments and topological charges leading
to a compensated topological charge overall.
Besides this true antiferromagnetic skyrmion [21, 23, 24],
synthetic antiferromagnetic skyrmions (cf. Fig. 5b) have been
considered as well [22] and have even been observed experimentally in multilayer systems [25, 26]. In the latter case,
the interpretation of two coexisting sub-skyrmions is even
more applicable. This is especially true once we extend the
s-d Hamiltonian to first-nearest neighbor hopping with amplitude t1 (the hopping between the different sublattices) and
second-nearest neighbor hopping with amplitude t2 (the hopping within the sublattices) and consider only second-nearest
neighbor hopping t2 .
The corresponding charge, orbital and spin Hall conductivites for t1 = 0 and t2 = −1 eV are shown in Fig. 5c-e.
The bands are doubly degenerate resembling the opposite spin
alignment in the two sublattices hosting skyrmions with opposite emergent magnetic fields. As a consequence, the topological Hall effect is compensated for every energy (Fig. 5c) but
the orbital and spin Hall conductivities are finite (Fig. 5d,e).
Their energy dependencies are similar to those of the conventional skyrmion presented in Fig. 2c,d but their magnitude

7
is larger due to the two coexisting sublattices and the larger
skyrmion size. Qualitatively similar results can be obtained
for nearest-neighbor hopping only (t1 = −1 eV and t2 = 0,
presented in Fig. S5a-c of the Supplementary Material) and
both hoppings considered (t1 = −2/3 eV and t2 = −2/3 eV,
presented in Fig. S5d-f of the Supplementary Material).
Independent of the choice of hopping amplitudes, a pure
Hall effect of angular momentum (orbital and spin) emerges
while the charge transport is compensated. The precise energy
dependence, however, can be very different once the hoppings
are modified because the electronic structure changes.
Fig. S6 in the Supplementary Material shows equivalent
results for an antiferromagnetic bimeron [28, 92, 96]. Like
for the antiferromagnetic skyrmion discussed above, the
topological Hall effect vanishes due to a compensated topological charge. However, since the two bimerons do not have
a net out-of-plane moment, the spin Hall effect is zero as
well. Therefore, the antiferromagnetic bimeron, that has been
observed experimentally [97, 98], might be the ideal platform
to investigate the topological orbital Hall effect, as it exhibits
a pure orbital Hall effect that is not superimposed by a charge
or spin Hall effect.
Conclusions
In summary, we have shown that skyrmions and antiferromagnetic skyrmions give rise to a topological orbital Hall
effect. For conventional skyrmions, the net emergent field
forces electrons onto circular trajectories and causes skipping
orbits at the edges akin to the quantum Hall effect. This
gives rise to a topological Hall effect for which the charge
currents are spin and orbital polarized. An antiferromagnetic
skyrmions on the other hand, consists of two oppositely
oriented subskyrmions on two sublattices. The opposite
emergent fields cause opposite topological Hall effects
and opposite spin and orbital polarization giving rise to a
compensated topological Hall effect but net spin and orbital
Hall effects. An antiferromagnetic bimeron even exhibits a
pure orbital Hall effect.
Since the orbital angular momentum is not restricted by a
quantum number but increases with the skyrmion area, the
orbital Hall conductivity is much larger than the spin Hall
conductivity. The orbital Hall conductivity scales roughly
quadratically with the skyrmion area while the spin and charge
Hall conductivities scale roughly linearly (cf. Fig. S2 of the
Supplementary Material). This means these textures could
serve as generators of large orbital currents that can potentially transport information and give rise to considerable orbital torques [46, 47].
The results presented for the skyrmion can be carried over
to other topological spin textures such as antiskyrmions [86],
bimerons [91, 92, 99] and biskyrmions [100, 101]. Likewise,
the results of the antiferromagnetic skyrmion can be carried
over to other compensated topological spin textures such as
skyrmioniums [93–95].
It is worth noting again that in the present study we
have focused on the intrinsic contribution of a skyrmionic
texture to the orbital Hall effect in an easy-to-understand
model system. We have restricted the model to s orbitals,

have disregarded spin-orbit coupling and did not consider
scattering at defects. Taking these effects into account in a
future study could be interesting as additional effect like the
anomalous Hall effect or extrinsic effects like the ‘side jump’
and ‘skew scattering’ might occur that can be important
corrections [75, 77]. Furthermore, it has been shown recently
that the anomalous position has to be considered in the
definition of the velocity operator once the system includes
more than just s orbitals [73]. As explained in Ref. [76],
a complete quantum mechanical theory of non-equilibrium
orbital angular momentum dynamics is not yet available and
has to be derived from the ground up in the future.
Methods
Skyrmion texture.
modelled by

A skyrmion centered at r0 = 0 is



x sin(2πr/λ)/r
m = y sin(2πr/λ)/r 
cos(2πr/λ)

(2)

p
for r = x2 + y 2 < λ/2 and m = −ez otherwise.
Note that this is only an approximation for the normalized
skyrmion profile. The precise magnetization profile is determined by the interplay of several magnetic interactions and
depends on the magnetic parameters. Most important for our
purposes is the topological charge [3]


Z
∂m(r) ∂m(r)
1
m(r) ·
×
d2 r. (3)
NSk =
4π xy
∂x
∂y
which is an integer for the above considered Néel skyrmion,
NSk = +1.
Calculation of the observables.
as
Sz,ν (k) =

The spin is calculated

ℏ
⟨νk|σz |νk⟩.
2

(4)

We calculate the orbital angular momentum based on the modern formulation including the off-diagonal elements of the
tensor [57, 67]
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
β̸=ν,α

× (⟨νk|vx |βk⟩⟨βk|vy |αk⟩ − ⟨νk|vy |βk⟩⟨βk|vx |αk⟩) .
(5)
Here, v = ℏ1 ∇k H is the velocity operator. Lν,z (k) are the
diagonal elements of the tensor Lν,z (k) = ⟨νk|Lz |νk⟩. Note
that we have corrected a mistake in Ref. [57] where Im was
used instead of the imaginary unit i.
The intrinsic Hall conductivity [102]
Z
e2 X 1
σxy (EF ) = −
Ων,z (k) d2 k
(6)
h ν 2π Eνk ≤EF
is calculated by integrating the reciprocal space Berry curvature over all occupied states in the Brillouin zone (states below

8
the Fermi energy EF at zero temperature). The Berry curvature is [10]
Ων,z (k) = −2ℏ2 Im

X ⟨νk|vx |µk⟩⟨µk|vy |νk⟩
µ̸=ν

(Eνk − Eµk )2

.

The intrinsic orbital and spin Hall conductivities [57]
Z
eX 1
Lz
ΩLz (k) d2 k,
σxy
(EF ) =
ℏ ν (2π)2 Eνk ≤EF ν,z
Z
eX 1
Sz
σxy (EF ) =
ΩSz (k) d2 k
ℏ ν (2π)2 Eνk ≤EF ν,z

(7)

Code availability
The code that supports the findings of this work is available
from the authors on reasonable request.
(8)
(9)

are calculated from the orbital and spin Berry curvatures, respectively,
2
z
ΩL
ν,z (k) = −2ℏ Im

X ⟨νk|j Lz |µk⟩⟨µk|vy |νk⟩
x

µ̸=ν
z
(k) = −2ℏ2 Im
ΩSν,z

(Eνk − Eµk )2

X ⟨νk|j Sz |µk⟩⟨µk|vy |νk⟩
x

µ̸=ν

(Eνk − Eµk )2

Data availability
The data that support the findings of this work are available at
DOI: 10.5281/zenodo.13919926.

,

(10)

,

(11)

Acknowledgements
This work was supported by the EIC Pathfinder OPEN grant
101129641 “Orbital Engineering for Innovative Electronics”.
Author contributions
B.G. and L.S. performed calculations. B.G. wrote the
manuscript with significant inputs from all authors. B.G.
prepared the figures. All authors discussed the results. B.G.
planned the project. B.G. and I.M. supervised the project.
I.M. provided the funding.
Supplementary information
accompanies this paper at [insert link].

P
where ⟨νk|jxLz |µk⟩ = 12 α [⟨νk|vx |αk⟩⟨αk|Lz |µk⟩ +
⟨νk|Lz |αk⟩⟨αk|vx |µk⟩] is the orbital current operator and ⟨νk|jxSz |µk⟩ = 12 [⟨νk|vx |νk⟩⟨µk|Sz |µk⟩ +
⟨νk|Sz |νk⟩⟨µk|vx |µk⟩] the spin current operator.

Competing interests
The authors declare no competing interests.

[1] Bogdanov, A. & Yablonskii, D. Thermodynamically stable
vortices in magnetically ordered crystals. the mixed state of
magnets. Zh. Eksp. Teor. Fiz 95, 182 (1989).
[2] Mühlbauer, S. et al. Skyrmion lattice in a chiral magnet. Science 323, 915–919 (2009).
[3] Nagaosa, N. & Tokura, Y. Topological properties and dynamics of magnetic skyrmions. Nature Nanotechnol. 8, 899–911
(2013).
[4] Romming, N. et al. Writing and deleting single magnetic
skyrmions. Science 341, 636–639 (2013).
[5] Sampaio, J., Cros, V., Rohart, S., Thiaville, A. & Fert, A. Nucleation, stability and current-induced motion of isolated magnetic skyrmions in nanostructures. Nature Nanotechnol. 8, 839
(2013).
[6] Fert, A., Cros, V. & Sampaio, J. Skyrmions on the track. Nature Nanotechnol. 8, 152–156 (2013).
[7] Yu, X. et al. Real-space observation of a two-dimensional
skyrmion crystal. Nature 465, 901–904 (2010).
[8] Heinze, S. et al. Spontaneous atomic-scale magnetic skyrmion
lattice in two dimensions. Nature Phys. 7, 713–718 (2011).
[9] Schulz, T. et al. Emergent electrodynamics of skyrmions in a
chiral magnet. Nature Phys. 8, 301–304 (2012).
[10] Berry, M. V. Quantal phase factors accompanying adiabatic
changes. Proceedings of the Royal Society of London A:
Mathematical, Physical and Engineering Sciences 392, 45–57
(1984).
[11] Zak, J. Berry’s phase for energy bands in solids. Phys. Rev.
Lett. 62, 2747 (1989).
[12] Bruno, P., Dugaev, V. & Taillefumier, M. Topological Hall
effect and Berry phase in magnetic nanostructures. Phys. Rev.

Lett. 93, 096806 (2004).
[13] Neubauer, A. et al. Topological Hall effect in the A phase of
MnSi. Phys. Rev. Lett. 102, 186602 (2009).
[14] Lee, M., Kang, W., Onose, Y., Tokura, Y. & Ong, N. Unusual
Hall effect anomaly in MnSi under pressure. Phys. Rev. Lett.
102, 186601 (2009).
[15] Maccariello, D. et al. Electrical detection of single magnetic
skyrmions in metallic multilayers at room temperature. Nature
Nanotechnol. 13, 233 (2018).
[16] Sivakumar, P. K. et al. Topological Hall signatures of two chiral spin textures hosted in a single tetragonal inverse Heusler
thin film. ACS Nano 14, 13463–13469 (2020).
[17] Raju, M. et al. Colossal topological Hall effect at the transition between isolated and lattice-phase interfacial skyrmions.
Nature Comms. 12, 2758 (2021).
[18] Yin, G., Liu, Y., Barlas, Y., Zang, J. & Lake, R. K. Topological
spin Hall effect resulting from magnetic skyrmions. Phys. Rev.
B 92, 024411 (2015).
[19] Ndiaye, P. B., Akosa, C. A. & Manchon, A. Topological Hall
and spin Hall effects in disordered skyrmionic textures. Phys.
Rev. B 95, 064426 (2017).
[20] Göbel, B., Mook, A., Henk, J. & Mertig, I. The family of
topological Hall effects for electrons in skyrmion crystals. Eur.
Phys. J. B 91, 179 (2018).
[21] Barker, J. & Tretiakov, O. A. Static and dynamical properties of antiferromagnetic skyrmions in the presence of applied
current and temperature. Phys. Rev. Lett. 116, 147203 (2016).
[22] Zhang, X., Zhou, Y. & Ezawa, M. Magnetic bilayer-skyrmions
without skyrmion Hall effect. Nature Comms. 7, 10293
(2016).

References

9
[23] Zhang, X., Zhou, Y. & Ezawa, M. Antiferromagnetic
skyrmion: stability, creation and manipulation. Sci. Rep. 6,
24795 (2016).
[24] Göbel, B., Mook, A., Henk, J. & Mertig, I. Antiferromagnetic
skyrmion crystals: Generation, topological Hall, and topological spin Hall effect. Phys. Rev. B 96, 060406 (2017).
[25] Legrand, W. et al. Room-temperature stabilization of antiferromagnetic skyrmions in synthetic antiferromagnets. Nature
Mater. 19, 34–42 (2020).
[26] Dohi, T., DuttaGupta, S., Fukami, S. & Ohno, H. Formation and current-induced motion of synthetic antiferromagnetic skyrmion bubbles. Nature Comms. 10, 5153 (2019).
[27] Buhl, P. M., Freimuth, F., Blügel, S. & Mokrousov, Y. Topological spin Hall effect in antiferromagnetic skyrmions. physica status solidi (RRL)-Rapid Research Letters 11, 1700007
(2017).
[28] Göbel, B., Mertig, I. & Tretiakov, O. A. Beyond skyrmions:
Review and perspectives of alternative magnetic quasiparticles. Physics Reports 895, 1–28 (2021).
[29] Okubo, T., Chung, S. & Kawamura, H. Multiple-q states and
the skyrmion lattice of the triangular-lattice heisenberg antiferromagnet under magnetic fields. Phys. Rev. Lett. 108, 017206
(2012).
[30] Hamamoto, K., Ezawa, M. & Nagaosa, N. Quantized topological Hall effect in skyrmion crystal. Phys. Rev. B 92, 115417
(2015).
[31] Göbel, B., Mook, A., Henk, J. & Mertig, I. Unconventional
topological Hall effect in skyrmion crystals caused by the
topology of the lattice. Phys. Rev. B 95, 094413 (2017).
[32] Göbel, B., Mook, A., Henk, J. & Mertig, I. Signatures of
lattice geometry in quantum and topological Hall effect. New
J. Phys. 19, 063042 (2017).
[33] Landau, L. Diamagnetismus der Metalle. Z. Phys. 64, 629–
637 (1930).
[34] Onsager, L. Interpretation of the de Haas-van Alphen effect.
The London, Edinburgh, and Dublin Philosophical Magazine
and Journal of Science 43, 1006–1008 (1952).
[35] Hofstadter, D. R. Energy levels and wave functions of Bloch
electrons in rational and irrational magnetic fields. Phys. Rev.
B 14, 2239 (1976).
[36] Klitzing, K. v., Dorda, G. & Pepper, M. New method for highaccuracy determination of the fine-structure constant based on
quantized Hall resistance. Phys. Rev. Lett. 45, 494 (1980).
[37] Thouless, D., Kohmoto, M., Nightingale, M. & Den Nijs, M.
Quantized Hall conductance in a two-dimensional periodic potential. Phys. Rev. Lett. 49, 405 (1982).
[38] Hatsugai, Y., Fukui, T. & Aoki, H. Topological analysis of
the quantum Hall effect in graphene: Dirac-Fermi transition
across van Hove singularities and edge versus bulk quantum
numbers. Phys. Rev. B 74, 205414 (2006).
[39] Sheng, D., Sheng, L. & Weng, Z. Quantum Hall effect in
graphene: disorder effect and phase diagram. Phys. Rev. B 73,
233406 (2006).
[40] Chang, M.-C. & Niu, Q. Berry phase, hyperorbits, and
the Hofstadter spectrum: Semiclassical dynamics in magnetic
Bloch bands. Phys. Rev. B 53, 7010 (1996).
[41] Xiao, D., Shi, J. & Niu, Q. Berry phase correction to electron
density of states in solids. Phys. Rev. Lett. 95, 137204 (2005).
[42] Thonhauser, T., Ceresoli, D., Vanderbilt, D. & Resta, R. Orbital magnetization in periodic insulators. Phys. Rev. Lett. 95,
137205 (2005).
[43] Ceresoli, D., Thonhauser, T., Vanderbilt, D. & Resta, R. Orbital magnetization in crystalline solids: Multi-band insulators, Chern insulators, and metals. Phys. Rev. B 74, 024408

(2006).
[44] Raoux, A., Piéchon, F., Fuchs, J.-N. & Montambaux, G. Orbital magnetism in coupled-bands models. Phys. Rev. B 91,
085120 (2015).
[45] Göbel, B., Mook, A., Henk, J. & Mertig, I. Magnetoelectric effect and orbital magnetization in skyrmion crystals: Detection and characterization of skyrmions. Phys. Rev. B 99,
060406 (2019).
[46] Go, D. & Lee, H.-W. Orbital torque: Torque generation by
orbital current injection. Phys. Rev. Res. 2, 013177 (2020).
[47] Lee, D. et al. Orbital torque in magnetic bilayers. Nature
Comms. 12, 6710 (2021).
[48] Johansson, A., Göbel, B., Henk, J., Bibes, M. & Mertig, I.
Spin and orbital Edelstein effects in a two-dimensional electron gas: Theory and application to SrTiO3 interfaces. Phys.
Rev. Res. 3, 013275 (2021).
[49] El Hamdi, A. et al. Observation of the orbital inverse Rashba–
Edelstein effect. Nature Phys. 19, 1855–1860 (2023).
[50] Zhang, S. & Yang, Z. Intrinsic spin and orbital angular momentum Hall effect. Phys. Rev. Lett. 94, 066602 (2005).
[51] Bernevig, B. A., Hughes, T. L. & Zhang, S.-C. Orbitronics:
The intrinsic orbital current in p-doped silicon. Phys. Rev. Lett.
95, 066601 (2005).
[52] Kontani, H., Tanaka, T., Hirashima, D., Yamada, K. & Inoue,
J. Giant intrinsic spin and orbital Hall effects in Sr2 M O4 (M =
Ru, Rh, Mo). Phys. Rev. Lett. 100, 096601 (2008).
[53] Tanaka, T. et al. Intrinsic spin Hall effect and orbital Hall
effect in 4d and 5d transition metals. Phys. Rev. B 77, 165117
(2008).
[54] Kontani, H., Tanaka, T., Hirashima, D., Yamada, K. & Inoue,
J. Giant orbital Hall effect in transition metals: Origin of large
spin and anomalous Hall effects. Phys. Rev. Lett. 102, 016601
(2009).
[55] Go, D., Jo, D., Kim, C. & Lee, H.-W. Intrinsic spin and orbital
Hall effects from orbital texture. Phys. Rev. Lett. 121, 086602
(2018).
[56] Go, D., Jo, D., Lee, H.-W., Kläui, M. & Mokrousov, Y. Orbitronics: Orbital currents in solids. Europhys. Lett. 135, 37001
(2021).
[57] Pezo, A., Ovalle, D. G. & Manchon, A. Orbital Hall effect in
crystals: Interatomic versus intra-atomic contributions. Phys.
Rev. B 106, 104414 (2022).
[58] Canonico, L. M., Cysne, T. P., Molina-Sanchez, A., Muniz, R.
& Rappoport, T. G. Orbital Hall insulating phase in transition
metal dichalcogenide monolayers. Phys. Rev. B 101, 161409
(2020).
[59] Cysne, T. P., Bhowal, S., Vignale, G. & Rappoport, T. G. Orbital Hall effect in bilayer transition metal dichalcogenides:
From the intra-atomic approximation to the Bloch states orbital magnetic moment approach. Phys. Rev. B 105, 195421
(2022).
[60] Salemi, L. & Oppeneer, P. M. Theory of magnetic spin and
orbital Hall and Nernst effects in bulk ferromagnets. Phys.
Rev. B 106, 024410 (2022).
[61] Busch, O., Mertig, I. & Göbel, B. Orbital Hall effect and
orbital edge states caused by s electrons. Phys. Rev. Res. 5,
043052 (2023).
[62] Choi, Y.-G. et al. Observation of the orbital Hall effect in a
light metal Ti. Nature 619, 52–56 (2023).
[63] Cysne, T. P. et al. Disentangling orbital and valley Hall effects
in bilayers of transition metal dichalcogenides. Phys. Rev. Lett.
126, 056601 (2021).
[64] Barbosa, A. L., Canonico, L. M., Garı́a, J. H. & Rappoport, T. G. Orbital hall effect and topology on a two-

10
dimensional triangular lattice: from bulk to edge. arXiv
preprint arXiv:2311.11715 (2023).
[65] Seifert, T. S. et al. Time-domain observation of ballistic orbital-angular-momentum currents with giant relaxation
length in tungsten. Nature Nanotechnol. 18, 1132 (2023).
[66] Busch, O., Ziolkowski, F., Göbel, B., Mertig, I. & Henk, J.
Ultrafast orbital Hall effect in metallic nanoribbons. Phys. Rev.
Res. 6, 013208 (2024).
[67] Göbel, B. & Mertig, I. Orbital Hall Effect Accompanying
Quantum Hall Effect: Landau Levels Cause Orbital Polarized
Edge Currents. Physical Review Letters 133, 146301 (2024).
[68] Sahu, P., Bhowal, S. & Satpathy, S. Effect of the inversion
symmetry breaking on the orbital Hall effect: A model study.
Physical Review B 103, 085113 (2021).
[69] Bhowal, S. & Vignale, G. Orbital Hall effect as an alternative
to valley Hall effect in gapped graphene. Physical Review B
103, 195309 (2021).
[70] Salemi, L. & Oppeneer, P. M. First-principles theory of intrinsic spin and orbital Hall and Nernst effects in metallic
monoatomic crystals. Physical Review Materials 6, 095001
(2022).
[71] Sala, G. & Gambardella, P. Giant orbital Hall effect and
orbital-to-spin conversion in 3d, 5d, and 4f metallic heterostructures. Physical Review Research 4, 033037 (2022).
[72] Pezo, A., Garcı́a Ovalle, D. & Manchon, A. Orbital Hall
physics in two-dimensional Dirac materials. Physical Review
B 108, 075427 (2023).
[73] Go, D., Lee, H.-W., Oppeneer, P. M., Blügel, S. & Mokrousov,
Y. First-principles calculation of orbital Hall effect by Wannier interpolation: Role of orbital dependence of the anomalous position. Physical Review B 109, 174435 (2024).
[74] Wang, H. et al. Orbital origin of the intrinsic planar Hall effect.
Physical Review Letters 132, 056301 (2024).
[75] Liu, H., Cullen, J. H., Arovas, D. P. & Culcer, D. Quantum correction to the orbital Hall effect. arXiv preprint
arXiv:2408.05294 (2024).
[76] Atencia, R. B., Agarwal, A. & Culcer, D. Orbital angular momentum of Bloch electrons: equilibrium formulation,
magneto-electric phenomena, and the orbital Hall effect. arXiv
preprint arXiv:2403.07055 (2024).
[77] Liu, H. & Culcer, D. Dominance of extrinsic scattering mechanisms in the orbital Hall effect: Graphene, transition metal
dichalcogenides, and topological antiferromagnets. Physical
Review Letters 132, 186302 (2024).
[78] Dias, M. d. S., Bouaziz, J., Bouhassoune, M., Blügel, S. &
Lounis, S. Chirality-driven orbital magnetic moments as a new
probe for topological magnetic structures. Nature Comms. 7,
13613 (2016).
[79] Lux, F. R., Freimuth, F., Blügel, S. & Mokrousov, Y. Engineering chiral and topological orbital magnetism of domain
walls and skyrmions. Commun. Phys. 1, 60 (2018).
[80] Arai, M. & Hatsugai, Y. Quantum Hall effects of graphene
with multiorbitals: Topological numbers, Boltzmann conductance, and semiclassical quantization. Phys. Rev. B 79, 075429
(2009).
[81] Jo, D., Go, D., Choi, G.-M. & Lee, H.-W. Spintronics
meets orbitronics: Emergence of orbital angular momentum
in solids. npj Spintronics 2, 19 (2024).
[82] Lyalin, I., Alikhah, S., Berritta, M., Oppeneer, P. M. &
Kawakami, R. K. Magneto-optical detection of the orbital

Hall effect in chromium. Physical Review Letters 131, 156702
(2023).
[83] Soumyanarayanan, A. et al. Tunable room-temperature magnetic skyrmions in Ir/Fe/Co/Pt multilayers. Nature Materials
16, 898 (2017).
[84] Yu, X. et al. Magnetic stripes and skyrmions with helicity
reversals. Proceedings of the National Academy of Sciences
109, 8856–8860 (2012).
[85] Seki, S., Yu, X., Ishiwata, S. & Tokura, Y. Observation of
skyrmions in a multiferroic material. Science 336, 198–201
(2012).
[86] Nayak, A. K. et al. Magnetic antiskyrmions above room temperature in tetragonal Heusler materials. Nature 548, 561
(2017).
[87] Peng, L. et al. Controlled transformation of skyrmions and
antiskyrmions in a non-centrosymmetric magnet. Nature Nanotechnol. 15, 181–186 (2020).
[88] Jena, J. et al. Elliptical bloch skyrmion chiral twins in an antiskyrmion system. Nature Comms. 11, 1115 (2020).
[89] Jena, J. et al. Evolution and competition between chiral
spin textures in nanostripes with D2d symmetry. Sci. Adv. 6,
eabc0723 (2020).
[90] Göbel, B. & Mertig, I. Quaternary-digital data storage based
on magnetic bubbles in anisotropic materials. Phys. Rev. Appl.
15, 064052 (2021).
[91] Kharkov, Y., Sushkov, O. & Mostovoy, M. Bound states of
skyrmions and merons near the Lifshitz point. Phys. Rev. Lett.
119, 207201 (2017).
[92] Göbel, B., Mook, A., Henk, J., Mertig, I. & Tretiakov, O. A.
Magnetic bimerons as skyrmion analogues in in-plane magnets. Phys. Rev. B 99, 060407 (2019).
[93] Zhang, X. et al. Control and manipulation of a magnetic
skyrmionium in nanostructures. Phys. Rev. B 94, 094420
(2016).
[94] Zhang, S., Kronast, F., van der Laan, G. & Hesjedal, T. Realspace observation of skyrmionium in a ferromagnet-magnetic
topological insulator heterostructure. Nano Letters 18, 1057–
1063 (2018).
[95] Göbel, B., Schäffer, A. F., Berakdar, J., Mertig, I. & Parkin,
S. S. Electrical writing, deleting, reading, and moving of magnetic skyrmioniums in a racetrack device. Sci. Rep. 9, 12119
(2019).
[96] Shen, L. et al. Current-induced dynamics and chaos of antiferromagnetic bimerons. Physical Review Letters 124, 037202
(2020).
[97] Jani, H. et al. Antiferromagnetic half-skyrmions and bimerons
at room temperature. Nature 590, 74–79 (2021).
[98] Bhukta, M. et al. Homochiral antiferromagnetic merons, antimerons and bimerons realized in synthetic antiferromagnets.
Nature Communications 15, 1641 (2024).
[99] Gao, N. et al. Creation and annihilation of topological meron
pairs in in-plane magnetized films. Nature Comms. 10, 5603
(2019).
[100] Yu, X. et al. Biskyrmion states and their current-driven motion
in a layered manganite. Nature Comms. 5, 3198 (2014).
[101] Göbel, B., Henk, J. & Mertig, I. Forming individual magnetic
biskyrmions by merging two skyrmions in a centrosymmetric
nanodisk. Sci. Rep. 9, 9521 (2019).
[102] Nagaosa, N., Sinova, J., Onoda, S., MacDonald, A. H. & Ong,
N. P. Anomalous Hall effect. Rev. Mod. Phys. 82, 1539 (2010).


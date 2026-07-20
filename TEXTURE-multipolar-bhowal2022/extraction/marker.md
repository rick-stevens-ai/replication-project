Magnetic octupoles as the order parameter for unconventional antiferromagnetism
Sayantika Bhowal and Nicola A. Spaldin
Materials Theory, ETH Zurich, Wolfgang-Pauli-Strasse 27, 8093 Zurich, Switzerland
(Dated: December 8, 2022)
We show that time-reversal symmetry broken, centrosymmetric antiferromagnets with non-
relativistic spin-splitting are conveniently described in terms of the ferroic ordering of magnetic
octupoles. The magnetic octupoles are the lowest-order ferroically ordered magnetic quantity in this
case, and so are the natural order parameter for the transition into the magnetically ordered state.
They provide a uniﬁed description of the broken time-reversal symmetry and the non-relativistic spin
splitting as well as a platform for manipulating the latter, and account for other phenomena, such as
piezomagnetism, characteristic of this class of antiferromagnets. Unusually for antiferromagnets, we
show that the magnetic octupoles cause a non-zero magnetic Compton scattering, providing a route
for their direct experimental detection. We illustrate these concepts using density-functional and
model calculations for the prototypical non-relativistic spin-split antiferromagnet, rutile-structure
manganese diﬂuoride, MnF 2.
I. INTRODUCTION
The behavior that we now know as antiferromagnetism
was ﬁrst noticed around 100 years ago, when peaks in
both speciﬁc heat and magnetic susceptibility were ob-
served in materials such as MnO that have zero net mag-
netic moment [1, 2]. Soon after, N´ eel proposed a model
in which local magnetic dipole moments of equal magni-
tude on two sublattices order in an antiparallel fashion
[3]. While the predictions of the N´ eel model were consis-
tent with the observations [4], another ten years elapsed
before neutron diﬀraction provided the ﬁrst direct evi-
dence of antiferromagnetic ordering of magnetic dipoles
[5].
Usually the order parameter, ⃗L, of an antiferromag-
net (AFM) is deﬁned in terms of the diﬀerence between
the local magnetic dipole moments, ⃗M1 and ⃗M2, on the
two sublattices, ⃗L = ⃗M1− ⃗M2. Such a deﬁnition is con-
ceptually intuitive, but lacks the convenience provided
by ferroic order parameters such as the magnetization,
⃗M in ferromagnets or the electric polarization, ⃗P in fer-
roelectrics. For example, the antiferromagnetic vector
does not provide information about the conjugate ﬁeld
required to select for a particular antiferromagnetic do-
main, and fails to distinguish between antiferromagnets
that do or do not break time-reversal symmetry. The
magnetic dipoles, however, are just one of the terms in
a multipole expansion of the energy of a general magne-
tization density in a magnetic ﬁeld. They are generally
the lowest-order local multipole on an atomic site, which
makes them appealing for classifying magnetic order, but
there is no fundamental reason why they should necessar-
ily be the best choice. In particular, when the magnetic
dipoles order antiferromagnetically, higher order multi-
poles that order ferroically might be more suitable.
Indeed, such a higher-order-multipole description is
now established in the case of AFMs that break both
time-reversal (T ) and space-inversion ( I) symmetries,
and which are classiﬁed by the ferroic ordering of their
local magnetoelectric multipoles [6–8]. The magnetoelec-
tric multipoles make up the next-order term, beyond the
magnetic dipoles, in the multipole expansion of the mag-
netic interaction energy (see Eqn. 1), and so depend lin-
early on both position r and magnetic moment µ. All
suchT andI-broken AFMs therefore exhibit a linear
magnetoelectric response, in which an applied electric
ﬁeld induces a magnetization linear in the ﬁeld strength
and vice versa [9]. Their conjugate ﬁeld is the product
of electric and magnetic ﬁelds, which is exploited in so-
called magnetoelectric annealing to select for a particu-
lar antiferromagnetic domain in magnetoelectric devices
[10, 11]. The ferroic ordering of magnetoelectric multi-
poles also plays a crucial role in antiferromagnetic spin-
tronics [12, 13] and skyrmionics [14, 15], and can give rise
to unconventional transport properties [16].
Recently there has been renewed interest in a class of
AFMs that break time-reversal symmetry and exhibit a
spin-splitting of their energy bands that is not of relativis-
tic origin (in conventional antiferromagnets the bands are
doubly spin degenerate). First invoked in 1964 [17], such
non-relativistic spin-splitting (NRSS) is typically much
larger than relativistic Rashba-like spin splitting, and can
be substantial in materials containing only light elements.
An important recent development was the articulation of
guiding principles for realizing such unconventional mag-
netism in materials [18–22] so that proposed unconven-
tional properties of both fundamental and technological
importance [20, 23], including eﬃcient spin-current gen-
eration [24–26], spin-splitting torque [27, 28], giant mag-
netoresistance [29], spontaneous Hall eﬀect [30–32] and
superconductivity [33], chiral magnons [34] could now be
within reach. A new name was even introduced – alter-
magnet – to describe this class of AFMs [23] [see Fig.
1 (a)-(c)]. Note that many NRSS AFMs are centrosym-
metric and so are not described by ferroic ordering of
magnetoelectric multipoles.
Here we show that such time-reversal symmetry bro-
ken, centrosymmetric AFMs are conveniently described
in terms of the ferroic ordering of magnetic octupoles.
The magnetic octupoles form the next term in the mag-
netic multipole expansion after the magnetoelectric mul-
arXiv:2212.03756v1  [cond-mat.str-el]  7 Dec 2022

===PAGE BREAK===

2
kx
ky
Energy
kx
ky
Energy
kx
ky
EnergyFerromagnetConventional AntiferromagnetNRSSAntiferromagnet(a)(b)(c)
(d) (e)
abc
MnF
abc
FIG. 1. Non-relativistic spin-split (NRSS) antiferromagnets
and ferro-type magnetic octupolar order. (a)-(c) shows the
spin splitting of the bands for conventional ferromagnets (Zee-
man splitting), antiferromagnets (degenerate spin-polarized
bands), and the recently discovered AFMs with NRSS (sym-
metric in⃗k) of their bands. (d) and (e) show the antiferro-type
magnetic dipolar (arrows, (d)) order and ferro-type magnetic
O−
32 octupolar (colored anisotropic octupolar magnetic distri-
bution, (e)) order in MnF 2 respectively.
tipoles, and are the lowest-order ferroically ordered mag-
netic quantity in this case. They are the natural order
parameter for the transition into the magnetically or-
dered state, and provide a convenient and uniﬁed descrip-
tion of the broken T symmetry and the non-relativistic
spin splitting. Importantly for potential device appli-
cations, they provide a platform for manipulating the
spin-splitting. They also account for other phenomena
displayed by this class of AFMs such as the piezomag-
netic eﬀect [35, 36] and strong magnetic anisotropy [37],
and allow us to predict new behaviors such as an anti-
piezomagnetism. Finally, we show that, unusually for
an antiferromagnet, they will have a non-zero magnetic
Compton scattering, providing a route for their direct
experimental detection.
We illustrate our ideas using rutile-structure man-
ganese diﬂuoride, MnF2. MnF 2 has been widely explored
as a classic example of a two sub-lattice AFM over the
past century [38–40], and was recently identiﬁed as a pro-
totype centrosymmetric AFM with NRSS [18]. Impor-
tantly, Mn ions of opposite spin orientation have inequiv-
alent ﬂuorine environments (Fig. 1 (d)). This results in
identical, ferroically orderedO32− magnetic octupoles at
each Mn site (Fig. 1 (e)), which cause the broken T
symmetry in spite of the AFM spin compensation.
The remaidner of the manuscript is organized as fol-
lows. We begin by brieﬂy describing the crystal and mag-
netic structures of MnF 2 in Section II. This is followed
by our discussion of the ordered magnetic octupoles and
their role in NRSS in Section III. In Section IV we predict
new behaviors resulting from the ferromagneto-octupolar
order that await experimental veriﬁcation, and propose
magnetic Compton scattering as a route to the direct de-
tection of magnetic octupoles. Finally, we summarize our
results and discuss promising future directions in Section
V.
II. CRYSTAL AND MAGNETIC STRUCTURE
MnF2 crystallizes in the centrosymmetric tetrago-
nal rutile structure with the space group symmetry
P 42/mnm (D4h point group) [18, 41]. As depicted in
Fig. 1 (d), the unit cell contains two formula units, with
two Mn atoms at the corner and the center of the unit
cell, octahedrally coordinated by the F atoms. Impor-
tantly, the F environment around the Mn atom at the
center is rotated by 90 ◦ around the z axis with respect
to that at the corner Mn atom. As a result of this non-
equivalent F environment, the Mn sites, although equiv-
alent, are not related by a lattice translation. This has
a crucial impact on the symmetry of the AFM structure
of MnF2 (magnetic space group P 42′/mnm′) below the
N´ eel temperature (TN = 67 K [42]), where the collinear
Mn spins align antiparallely along [001] [43] [see Fig. 1
(d)]. Such a magnetic conﬁguration breaks the T sym-
metry despite the vanishing magnetization, since time-
reversal plus translation is not a symmetry of the anti-
ferromagnetic conﬁguration.
III. MAGNETIC OCTUPOLE AND
NON-RELATIVISTIC SPIN SPLITTING
The broken T symmetry in the absence of any net
magnetization is indicative of the existence of magnetic
multipole of higher order than the magnetic dipole. Such
multipoles appear in the expansion of the interaction en-
ergyEint between a spatially varying magnetic ﬁeld ⃗H(⃗ r)
and a magnetization density ⃗ µ(⃗ r) [8, 44],
Eint =−
∫
⃗ µ(⃗ r)· ⃗H(⃗ r)d3r
=−
∫
⃗ µ(⃗ r)· ⃗H(0)d3r
  
Dipolar term
−
∫
riµj(⃗ r)∂iHj(0)d3r
  
Magnetoelectric multipolar term
−
∫
rirjµk(⃗ r)∂i∂jHk(0)d3r
  
Octupolar term
... . (1)

===PAGE BREAK===

3
In a compensated AFM, the net magnetization ⃗M =∫
⃗ µ(⃗ r)d3r is absent and so the conventional dipolar Zee-
man term which is the ﬁrst term in the above expan-
sion, does not contribute. Furthermore, the presence
of inversion symmetry in centrosymmetric antiferromag-
nets with symmetric NRSS with respect to ⃗k forbids
the existence of any ferro-type magnetoelectric multipole
Mij =
∫
riµj(⃗ r)d3r since these break inversion symme-
try, forming the second term in Eq. (1). This makes
the ﬁrst symmetry-allowed ferro-type magnetic multi-
pole the inversion-symmetric rank-3 magnetic octupole,
Oijk =
∫
rirjµk(⃗ r)d3r, which forms the third term in
the above expansion. While this simple symmetry ar-
gument suggests that the magnetic octupole is the ﬁrst
allowed net nonzero magnetic multipole in a centrosym-
metric AFM with NRSS, its existence can only be con-
ﬁrmed through an explicit computational analysis of the
multipoles.
In the following we take MnF2 as a representative sys-
tem for such unconventional AFMs and explicitly analyze
the multipoles in the system. In particular, we focus on
the magnetic octupole, show its possible manipulation
via structural and magnetic modiﬁcations, and correlate
it to the characteristic non-relativistic spin splitting of
the energy bands.
A. Multipole Analysis
In order to compute the atomic-site multipoles, we
decompose the density matrix ρlm,l′m′, computed using
density-functional theory as implemented in the Elk code
(see the computational details in Appendix A), into ten-
sor moments [8]. Since the desired parity even multipoles
(as the structure has inversion symmetry) have contribu-
tions from even l +l′ terms, we evaluate both d−d and
p−p matrix element contributions. We consider both T
even (charge) and odd (magnetic) multipoles.
The computed magnetic octupoles,O32− andO30, and
electric quadrupoles, Q22− andQ20, are shown in Fig.
2 (a) and (c) as the relative strength of the spin-orbit
coupling constant, λr, is varied. As we can see from
this variation, the magnetic octupoles are non-zero even
without the presence of the spin-orbit coupling. It is
also clear from Fig. 2 that the magnitudes of the mag-
netic octupoles depend on λr, whereas the values of
the quadrupoles remain invariant, suggesting that the
quadrupoles have only structural origin while the mag-
netic octupoles may have both structural and magnetic
dependencies. We note that a pure structural origin of
quadrupoles is not a general case for any systems with
quadrupolar distortion, e.g., the quadrupoles in the iso-
space-group compound Ba 2MgReO6 (with a canted an-
tiferromagnetic spin conﬁguration) are reported to have
a strong spin dependence [45].
The computed magnetic multipoles show the presence
of a ferro-type magnetic octupole O32− (Fig. 1e) with
real-space representation xymz (where mz is the z com-
ponent of the magnetic moment) at the Mn sites, belong-
ing to the totally symmetric irreducible representation
A1g. The existence of the magnetic octupole is consistent
with theB−
1g active representation of MnF2 as well as the
symmetry analysis described earlier. The magnetic oc-
tupoleO30 with real-space representation (3z2−r2)mz,
also has a non-zero value at the Mn sites, however, they
have anti-parallel alignment between the Mn sites, result-
ing in an absence of net O30 octupole moment. We also
found non-zero magnetic octupole components Q(τ)
x2−y2
andt(τ)
z with ferro and antiferro-type alignments respec-
tively, which we will discuss later in Section IV A and in
Appendix D. In addition to these magnetic octupoles, the
crystal structure of MnF2 also hosts electric quadrupoles,
Q20 with (3z2−r2) distortion andQ22−, representing the
xy-structural distortion, which have ferro- and antiferro-
type alignments respectively.
For a physical understanding and better visualization,
we further compute the band-decomposed charge and
spin densities for the top valence band (which also under-
goes NRSS) in the electronic structure of MnF2, shown in
Fig. 3 (a) and the results are shown in Fig. 2 (e) and (g).
As apparent from the ﬁgure, the charge density around
the Mn atoms is highly anisotropic in the x−y plane,
a signature of the existing Q22− quadrupole. Interest-
ingly, the spin density around the Mn atoms, shown in
Fig. 2 (d), follows the anisotropic charge density, indicat-
ing a correlation between the spin anisotropy (quantiﬁed
by the magnetic octupoles) and the charge anisotropy
(quantiﬁed by the electric quadrupoles). This further
justiﬁes the dependence of the octupoles on λr.
B. Magnetic Octupolar Domains: Correlation to
Structure and Spin
We now show how the coupling between magnetic oc-
tupoles and charge quadrupoles determine the magnetic
octupolar domains. Since the magnetic octupoles are
linked to the NRSS, as we show in the next section, the
understanding of the magnetic octupolar domain is also
useful in manipulating the NRSS.
We begin by changing the ﬂuorine environment around
the Mn atoms, without aﬀecting the spin arrangements
at the Mn sites. Speciﬁcally, we change the coordinates
of the F ions from 4 f : (x,x, 0)→ 4g : (x,−x, 0), which
alters the F-Wyckoﬀ site symmetry from 4f to 4g, while
keeping the space-group symmetry unchanged. We note
that structurally (without considering the magnetism),
the new structure is equivalent to the original crystal
structure of MnF 2 (shown in Fig. 1 (c)), with a shifted
origin at (0.5,0.5,0.5), so that the central and corner Mn
atoms are exchanged in the new structure. This results
in a 90◦ alternation of MnF 6 octahedral rotation and,
hence, their distortion in the x−y plane (see Figs. 2
(e)-(h)). Correspondingly, this leads to a reversal of sign
in the computed antiferro-type Q22− quadrupole for the
modiﬁed structure, as depicted in Fig. 2 (d). This is also

===PAGE BREAK===

4
0 0.5 1 1.5 2-0.04
-0.02
0
0.02
0.04
           M
           M
-0.008
-0.004
0
0.004
Magnetic octupoles (   ) 
           M
           M
0 0.5 1 1.5 2-0.04
-0.02
0
0.02
0.04
-0.008
-0.004
0
0.004
Quadrupoles (a.u.)
Mn1
Mn2
µB
𝒬22-
O32-O30(a) (b)
(c) (d)𝒬20
Relative strength of the spin-orbit coupling
abc
Mn1
Mn2
Mn1
Mn2
Mn1
Mn2
(e) (f)
(g) (h)
90oalternatingoctahedra
FIG. 2. Variation of magnetic octupoles at the Mn atoms
as the relative strength of the spin-orbit coupling λr is varied
for the (a) crystal structure of MnF 2 and (b) for the modiﬁed
structure. The same variation of the charge quadrupoles for
the (c) crystal structure of MnF 2 and (d) for the modiﬁed
structure. Here λr =λf/λ, with λf andλ being the enforced
value of the spin-orbit coupling constant in the calculation
and its actual value in the material respectively. The band-
decomposed charge densities for the top valence band in Fig.
3 (a) of MnF 2 in the a-b plane for the (e) crystal structure
of MnF 2 and (f) for the modiﬁed structure. (g) and (h) are
the same, showing the band-decomposed magnetization den-
sities. The opposite MnF 6 octahedral rotations are indicated
in black arrows.
evident from the changes in the anisotropic charge den-
sity distribution around the Mn atoms in the modiﬁed
structure as shown in Fig. 2 (f). Note that the modiﬁed
ﬂuorine environment, however, does not aﬀect the dis-
tortion of the MnF6 octahedra alongz direction, and the
sign of the ferro typeQ20 quadrupole, therefore, remains
unaltered (see Fig. 2 (d)).
In order to see the impact of the charge quadrupoles on
the magnetic octupoles, we further analyze the magnetic
multipoles of this modiﬁed structure. Interestingly, our
computed octupoles show that the sign of the O32− oc-
tupole reverses whereas that of O30 remains as it is (see
Fig. 2 (b)), showing the reversal of the magnetic octupo-
lar domain. Corresponding changes in the anisotropic
magnetization density around the Mn atoms are shown
in Fig. 2 (h). This also emphasizes the correlation be-
tweenO32− octupole andQ22− quadrupole; andO30 oc-
tupole andQ20 quadrupole. Note that theO32− andO30
octupoles remain ferro- and antiferro-type respectively.
This suggests selecting the magnetic octupolar domain by
only changing the position of the non-magnetic F atoms,
without aﬀecting the magnetic Mn atom’s position or its
spin arrangements, emphasizing a strong interplay be-
tween lattice and the magnetic conﬁguration, quantiﬁed
by the magnetic octupole.
We close this section by describing the manipulation
of the magnetic octupole by ﬂipping the direction of all
the Mn-spins while keeping the same antiferromagnetic
arrangement between the Mn atoms. Physically, it cor-
responds to a diﬀerent antiferromagnetic domain. The
reversal of the Mn-spins results in a reversal of the sign
of both octupoles, in contrast to the previous case where
only the ferro-typeO32− octupole reverses its sign. Note
that, in this case electric quadrupoles remain the same,
as they do not depend on the spin arrangement. It is
interesting to point out that this manipulation of the
magnetic octupole has in fact important physical impli-
cations. For example, the two antiferromagnetic domains
with ferro-type octupoles of opposite sign can also be vi-
sualized as two separate ferro-octupolar domains. Such
re-visualization is particularly useful in describing impor-
tant physical properties that are characteristics of the
magnetic octupoles as well as understanding the conju-
gate ﬁelds for creating such ferro-octupolar domains, as
we discuss later in Section. IV.
C. Relevance to Non-relativistic Spin-splitting
Next we link the unconventional spin-splitting of the
energy bands in the Brillouin zone (BZ) of the anti-
ferromagnetic MnF 2 to the ferro-octupolar order using
the reciprocal-space representation of the ferro-type oc-
tupole. Since the magnetic octupole can be manipulated
by modifying the F-environment or the spin arrange-
ments, as discussed above, we show that these changes
can also be used to manipulate the spin-splitting of the
bands.
Our calculated antiferromagnetic band structure of
MnF2 both in the presence and absence of spin-orbit
interaction is depicted in Fig. 3(a). As we see from
the band structure, there is a signiﬁcant energy split-
ting between the up- and down-spin bands along Γ →
M direction in the BZ of MnF 2. Interestingly, the split-
ting is present even without the spin-orbit interaction,
and inclusion of spin-orbit interaction does not aﬀect the

===PAGE BREAK===

5
-0.8
-0.4
0
Energy (eV) -0.8
-0.4
0
Energy (eV)
Up
Down
-0.8
-0.4
0
Energy (eV) Up
Down
-0.04
-0.02
0
     (eV)
DFT
Model
∆εs
Γ (0.5,0.5,0)(-0.5,-0.5,0)
Γ ΓX M Γ XM ΓZ R ZA Z R A Z
(a)
(b) (d)
Γ (0.5,0.5,0)(0.5,-0.5,0)
(c)
FIG. 3. Spin splitting in MnF 2. (a) Band structure of MnF 2
in both absence and presence of spin-orbit interaction, de-
picting the spin splitting along M → Γ direction. The up
and down spin-polarized bands in absence of spin-orbit cou-
pling are shown in solid blue and red lines respectively and
the bands in presence of spin-orbit interaction are indicated
in green dots. (b) The corresponding band structure along
the same high-symmetryk path for the hypothetical modiﬁed
structure (see text for details), showing the reversal of spin
splitting along M → Γ. (c) Band structure of MnF 2 show-
ing the reversal of spin splitting as the momentum direction
changes from [1¯10] to [110]. (d) A comparison of the DFT re-
sult and the tight-binding analytical expression, Eq. (6), for
the energy splitting between the two top-most spin-polarized
bands in (a).
energy splitting along that direction, in agreement with
the reported band structure in Ref. 18. The splitting
is large compared to the typical relativistic Rashba-type
spin-splitting and does not require any broken inversion
symmetry of the structure [46].
To understand this unconventional spin-splitting in
MnF2, we analyze the reciprocal-space representation of
the ferro-typeO32− octupole. The reciprocal space rep-
resentations of the multipoles have been used successfully
to describe the band asymmetries in the BZ of noncen-
trosymmetric materials [12, 47, 48]. In contrast to the
odd-parity multipoles, for which the real and reciprocal-
space representations are rather counter-intuitive, for the
even-parity multipoles, such as the O32− magnetic oc-
tupole, that are relevant here the analysis is much more
straightforward. The reciprocal space representation in
this case can simply be obtained by replacing ⃗ r→⃗k so
that the reciprocal-space representation ofO32− octupole
(xymz in real space) is kxkymz. This immediately ex-
plains the splitting between up and down spin-polarized
bands, with the spin polarization along ˆz, along [110] di-
rection in the momentum space, e.g., Γ → M and A→ Z
directions in momentum space. Note that such splitting
will occur along any momentum direction with non-zero
kx and ky.
Interestingly, since the reciprocal space representation
is an even function of ⃗k, the resulting spin-splitting
should also be symmetric, in contrast to the anti-
symmetric spin splitting in the Rashba interaction. This
indeed is the case e.g., in MnF 2 with identical spin split-
ting along [110] and [ ¯1¯10] directions in the momentum
space. In addition from the representation kxkymz, we
also expect the spin-splitting to reverse as the direction
in the momentum space changes from [110] to [1 ¯10] (d-
wave spin splitting). Indeed, the computed DFT band
structure depicts such reversal of spin-splitting under C4
rotation of the momentum direction, as shown in Fig. 3
(b). The representation analysis, therefore, conﬁrms that
the ferro-type ordering of theO32− octupoles is responsi-
ble for the spin splitting of the energy bands, analogous to
the spin splitting of bands in a conventional ferromagnet
with ferro-type magnetic dipole. Note that the atomic-
site magnetic octupole, discussed here, is distinct from
the cluster and bond multipoles predicted by Hayami et.
al. [49, 50] for spin splitting in collinear antiferromag-
nets. The magnetic octupole description has the advan-
tage that it naturally occurs in a magnetic multipole ex-
pansion and also describes the order parameter for such
unconventional antiferromagnetism, as discussed above.
To further verify the role of O32− octupole in gener-
ating the spin-splitting, we analyze the spin-splitting of
the bands for the case of structural modiﬁcation, dis-
cussed in the previous section, for which the O32− oc-
tupole switches sign. As expected, in this case, the spin
splitting also reverses (see Fig. 3 (c)). Similar reversal of
the spin-splitting also occurs for the opposite magnetic
dipolar domain (not shown here), in which the magnetic
O32− octupoles also switch sign.
D. Role of microscopic parameters in the spin
splitting
Having shown that the ferro-type ordering of the mag-
netic octupoles generates the spin-splitting in MnF 2, to
determine the role of diﬀerent microscopic parameters,
such as electronic hopping, exchange splitting, etc., on
the strength of the spin splitting, we next carry out a
low-energy tight-binding (TB) analysis. For this pur-
pose, we construct a minimal four-band TB model in the
Bloch function basis with the order of the basis set in the
sequence{Mn1−dxz, Mn1−dyz, Mn2−dxz, Mn2−dyz}.
The Hamiltonian reads as follows
Ht =α(⃗k)I+β(⃗k)Σz⊗σx+γ(⃗k)Σx⊗σ0+δ(⃗k)Σx⊗σx. (2)
Here, I is a 4× 4 identity matrix, ⃗Σ and ⃗ σare the Pauli
matrices in the sublattice bases of Mn1 and Mn2 and
in the orbital bases of dxz and dyz respectively, and σ0
is an identity matrix in the orbital bases. The choice
of the orbitals is governed by the predominant orbital
characters of the top pair of valence bands along Γ →
M in the BZ of MnF 2 (see Fig. 6 in Appendix C). The

===PAGE BREAK===

6
functions α(⃗k),β (⃗k),γ (⃗k), and δ(⃗k) are determined by
the eﬀective d-d hopping parameters ( ti, i = 1, 4) and
the on-site energies (εi,i = 1, 2) of the orbitals and their
explicit functional forms are given below,
α(⃗k) =ε1 + 2t1 cos(kzc)
β(⃗k) =ε2 + 2t2 cos(kzc)
γ(⃗k) = 8t3 cos
(kxa
2
)
cos
(kya
2
)
cos
(kzc
2
)
δ(⃗k) =−8t4 sin
(kxa
2
)
sin
(kya
2
)
cos
(kzc
2
)
. (3)
Here, a and c are the lattice constants of the tetragonal
structure. For simplicity, we consider electronic hoppings
only up to second nearest neighbor and the realistic TB
parameters are extracted from the DFT band structure
of MnF2 using the NMTO downfolding technique [51].
The diagonalization of the Hamiltonian in Eq. 2, gives
us the four energy eigenvalues,
E−
± (⃗k) =α(⃗k)−{β(⃗k)2 + (δ(⃗k)±γ(⃗k))2}1/2
E+
±(⃗k) =α(⃗k) +{β(⃗k)2 + (δ(⃗k)±γ(⃗k))2}1/2. (4)
Analysis of the corresponding eigenvectors shows that
there is an energy splitting ∆E =E−
+ (⃗k)−E−
− (⃗k) between
bands of dominant Mn1 and Mn2 sublattice contribu-
tions. Note that such energy splitting between bands of
diﬀerent sublattice characters is present prior to includ-
ing the eﬀect of antiferromagnet exchange splitting J.
We now show that the inclusion of J translates the sub-
lattice splitting of the bands into the spin splitting of the
bands.
To include the eﬀect of the antiferromagnetic exchange,
we rewrite the Hamiltonian (2) in the basis of {Mn1−
dxz↑, Mn1−dyz↑, Mn2−dxz↑, Mn2−dyz↑, Mn1−dxz↓
, Mn1−dyz ↓, Mn2−dxz↓, Mn2−dyz ↓} and add the
exchange termHAFM
ex =JSz⊗ (Σz⊗σ0) to it. The full
Hamiltonian is given by,
H =S0⊗Ht +JSz⊗ (Σz⊗σ0) . (5)
Here, ⃗S andS0 are the Pauli matrices and the identity
matrix in the spin basis. The exchange splitting energy
between up and down spin polarized bands, 2 J≈ 5 eV,
extracted from the computed spin-polarized densities of
states of MnF 2.
By diagonalizing the Hamiltonian (5), we obtain the
energy eigenvalues and focus on the spin-polarized top
most valence bands, with energies E↑ andE↓. We note
that their eigenvalues are identical to those of E−
± in Eq.
(4), except that β(⃗k)→J +β(⃗k). Physically, this means
that the two Mn sublattices, that primarily contribute
to those bands, have opposite spin polarization in the
presence of antiferromagnetism and, therefore, they lead
to the spin splitting of the bands. The explicit analytical
form of the energy splitting is given by,
∆Es =E↑−E↓
={(J +β)2 + (δ−γ)2}1/2−{ (β +J) + (δ +γ)2}1/2
≈ 32
ϵ t3t4 sin(kxa) sin(kya). (6)
Here, in obtaining the last equality we have used the fact
that ϵ≫ (δ +γ), where ϵ =J +β≈J +ε2 + 2t2, using
Eq. 3 and ignoring terms that are second order in kz or
higher. Note that this approximation in ϵ becomes exact
in the kz = 0 plane, which contains the desired Γ → M
momentum direction of spin-splitting. For a realistic set
of parameters (listed in Appendix B), we compare the
analytical result in Eq. (6) to the DFT computed energy
splitting of the spin-polarized bands. As depicted in Fig.
3 (d), they agree reasonably with each other, suggesting
that our minimal model captures the essential physics of
the spin-splitting in MnF 2.
We pause here and analyze the obtained analytical re-
lation in Eq. (6) for the spin-splitting energy. First of all,
it is clear from Eq. (6), that ∆ Es(⃗k) = ∆Es(−⃗k), i.e., it
is symmetric in ⃗k, but changes sign under ( kx,ky) →
(kx,−ky), consistent with the computed DFT bands.
Secondly, we see that the splitting energy ∆ Es depends
directly on the inter-sublattice hopping parameters, t3
(intra-orbital) and t4 (inter-orbital) in the absence of
which ∆Es vanishes. This emphasizes the crucial role of
interaction between the two sublattices, which in com-
bination with the antiferromagnetic exchange, gener-
ates the spin splitting. Physically, this indicates that
a structure-spin correlation, a reminiscent of the mag-
netic octupole as discussed before, is responsible for the
spin splitting. It is interesting to point out that the
inter-sublattice hopping t4 (as well as the product t3t4)
in MnF 2 is a symmetric hopping and it changes sign
as the direction of hopping changes from [11z] to [1 ¯1z]
with z̸= 0 leading to symmetric spin splitting. This is
analogous to the antisymmetric hopping in a nonmag-
netic broken-inversion symmetric system that gives rise
to Rashba-like antisymmetric spin splitting of the energy
bands [48]. Finally, the TB analysis also provides a mi-
croscopic understanding of the reversal of spin splitting
described before. For the modiﬁed structure, the onsite
energy ε2 and the hopping t2 change sign, leading to a
sign change in β. While, the sign change does not af-
fect the energy eigenvalues E−
± (⃗k) in Eq. 4 (since the
dependence on β comes in even power), it reverses the
dominant sublattice contributions in the corresponding
eigenvectors (as also evident from the full DFT band
structure, depicted in the appendix C), resulting in a
reversal of sublattice splitting of bands. Since, the sub-
lattice splitting later transforms into the spin splitting,
this consequently leads to the reversal of the spin split-
ting. The reversal of spin-splitting for the other anti-
ferromagnetic domain follows directly from the resulting
sign change in the antiferromagnetic exchange J, which,
in turn, alters the spin polarization of the bands.

===PAGE BREAK===

7
Overall, the TB analysis provides a crucial insight into
the roles of diﬀerent microscopic parameters in generat-
ing the unconventional spin splitting of the energy bands
in MnF 2. The TB analysis further serves as a link be-
tween the proposed “modern” ferro-octupolar order and
the conventional antiferromagnetic dipolar order.
IV. IMPLICATIONS OF MAGNETIC
OCTUPOLE
The next step is to identify the implications of the
existing magnetic octupole in determining the physical
properties of a centrosymmetric AFM with NRSS as well
as its possible direct measurements. Here, we point out
(A) the resulting physical properties, piezo and anti-
piezomagnetic eﬀects and (B) the possible detection of
magnetic octupoles using the magnetic Compton scat-
tering eﬀect. Once again, we take MnF 2 as our example
material for illustration. We show that the existing ferro-
type magnetic octupole O32− describes the well-known
piezomagnetic eﬀect in MnF 2. More interestingly, how-
ever, the knowledge of the antiferro-type magnetic oc-
tupoleO30 helps us to predict a previously unknown anti-
piezomagnetic eﬀect. In addition to the underlying fun-
damental physics and technological applications of these
eﬀects, we also propose magnetic Compton scattering as
an experimental technique for the detection of the ap-
parently hidden magnetic octupoles. The corresponding
measurement set-up as a guidance for future experiments
are also discussed.
A. Piezo and Anti-piezomagnetic Eﬀects
The piezomagnetic eﬀect, describes changes in magne-
tization due to an applied stress or changes in shape due
to an applied magnetic ﬁeld. It is particularly promis-
ing for applications because it provides a means for ma-
nipulating magnetism via strain engineering in antifer-
romagnets. In addition, since it is a linear coupling
in contrast to the quadratic coupling in the commonly
used magnetostriction, it also allows for magnetization
switching. The recent demonstration that the dynami-
cally excited optical phonons can induce the symmetry-
breaking lattice distortions required in the piezomagnetic
eﬀect[52–54], has revived interest. Such optically induced
strain would overcome the limitation of a large mechan-
ical strain and lead to practical applications in memory
and spintronic devices.
The piezomagnetic eﬀect has been predicted and ex-
perimentally shown for some AFMs with NRSS [35, 36,
52]. In this section, we show that the piezomagnetic eﬀect
is the result of ferroic ordering of magnetic octupoles, and
illustrate our ideas for the speciﬁc example of MnF 2. In
addition, we predict an antipiezomagnetic eﬀect in MnF2
resulting from the antiferro-typeO30 magnetic octupole.
General symmetry description- We begin by correlat-
ing the symmetries of the magnetic octupole and the
piezomagnetic response. We note that both are rank-
3 tensors and have the same symmetry, breaking time-
reversal symmetry while keeping inversion symmetry in-
tact. To correlate the elements of the piezomagnetic re-
sponse to the magnetic octupole, we analyze the non-
zero elements in the magnetic octupole tensor Oijk =∫
µirjrkd3r following the tensor decomposition reported
in Ref. [55]. Note that in general i,j,k are the dummy
indices and to be consistent with the indices of the piezo-
magnetic response tensor Λijk, here we associate the in-
dexi to the magnetization and j andk to spatial coordi-
nates so that the octupole Oijk is symmetric under the
exchange of j and k indices by construction.
The octupole Oijk can be decomposed into a totally
symmetric tensorSijk of dimension 10 and an 8 dimen-
sional non-symmetric residue tensor Rijk, that account
for the 18 independent elements of Oijk [55]. The to-
tally symmetric tensor Sijk can be further decomposed
into a traceless totally symmetric part ˜Sijk and a trace
part Tijk of dimensions 7 and 3 respectively and the
residue tensorRijk into two irreducible components ˜R(5)
ijk
and ˜R(3)
ijk of dimensions 5 and 3 respectively, so that
Oijk = ˜Sijk +Tijk + ˜R(5)
ijk + ˜R(3)
ijk. The explicit forms
of each of these irreducible components are given in Ref.
[55]. Note that the 7 independent components of the to-
tally symmetric traceless part ˜Sijk can be built from the
spherical harmonics with l = 3 and, hence, these com-
ponents are often exclusively referred to as the magnetic
octupole, in contrast to the entire Oijk tensor.
We now explicitly consider the case of MnF 2, which
is known to exhibit a piezomagnetic eﬀect [35, 56–58]
with the non-zero elements of the piezomagnetic response
tensor Λijk, Λxyz = Λyxz̸= Λzxy so that,
Mx = Λxyzσyz,My = Λyxzσxz,Mz = Λzxyσxy, (7)
where ⃗M is the magnetization that results from the ap-
plication of shear stress σij. We show next that the non-
zero components of the piezomagnetic response of MnF 2
correlate to the ferro-type O32− octupole.
Analyzing the diﬀerent elements of ˜Sijk, we see that
theO32− octupole, which has a ferro-type ordering in
MnF2, appears only when i = x,j = y,k = z and for
the permutation of the indices. ˜Sijk being symmetric, all
these elements are equal in magnitude. Similarly, ana-
lyzing the elements of other irreducible components, we
ﬁnd that the only other multipole that has a ferro-type
ordering in MnF 2 isQ(τ)
x2−y2, identiﬁed as the x2−y2
quadrupole component of the toroidal moment density
τ(⃗ r) = ⃗ r×⃗ µ(⃗ r). This leads to non-zero elements in the
residue tensor ˜R(5)
ijk, with ˜R(5)
xyz = ˜R(5)
yzx̸= ˜R(5)
zxy. Com-
bining the ferro-type magnetic octupole components in
MnF2, and the tensor decomposition of the the mag-
netic octupole Oijk, we obtain Oxyz = Oyxz ̸= Ozxy.
This nicely correlates with the symmetry allowed as well

===PAGE BREAK===

8
as experimentally observed components of piezomagnetic
response for MnF 2 in Eq. 7, conﬁrming the one-to-one
correlation between the piezomagnetic response and the
magnetic octupole tensor.
Finally we also predict an anti-piezomagnetic response
in MnF 2 due to the antiferro-type O30 octupole. Upon
application of stress we expect an additional change in
the Mn spin moments which is, however, opposite for the
two Mn atoms so that their contributions cancel each
other, leading to a zero net magnetization. Here, the
tensor decomposition guides us in predicting which spin
components will change due to an applied strain with
a certain orientation. Therefore, we follow the same
procedure as before and analyze ﬁrst the elements of
the symmetric traceless ˜Sijk to identify the elements
of ˜Sijk in which the O30 octupole appears. These are
˜Sxxz = ˜Syyz̸= ˜Szzz. The elements with symmetric per-
mutation of these indices are also allowed. For these same
elements of the residue tensors ˜R(5)
ijk and ˜R(3)
ijk, we ﬁnd
that only ˜R(3)
xxz = ˜R(3)
yyz̸= ˜R(3)
zxx = ˜R(3)
zyy are non-zero due
to the existence of the antiferro-type multipole t(τ)
z , de-
ﬁned as the z component of the moment of the toroidal
moment density, in MnF2. This means that if both O30
and t(τ)
z were ferro-type, we would have the following
non-zero components in the piezomagnetic response
Λxxz = Λyyz, Λzxx = Λzyy, and Λ zzz . (8)
However, since in factO30 andt(τ)
z have antiferro-type ar-
rangement in MnF2, the ﬁrst equality in the above equa-
tion instead indicates that a spin component along ˆx (ˆy)
will develop at individual Mn sites if we apply a shearing
stressσxz (σyz) to the structure, with the developed spin
components having an anti-parallel alignment between
the Mn sites, so that there is no net magnetization along
ˆx (ˆy). We refer to this eﬀect as an anti-piezomagnetic
eﬀect due to the generation of anti-parallel spin compo-
nents upon application of stress in analogy to the piezo-
magnetic eﬀect where parallel spin moments are gener-
ated to give rise to a net change in magnetization.
DFT results for MnF 2- Next, to computationally verify
our symmetry-guided prediction of ananti-piezomagnetic
eﬀect and to better understand the microscopic details of
both piezo- and antipiezo-magnetic eﬀects, we explicitly
study the eﬀect of a shear stress σxz (σyz) on the mag-
netism of MnF 2 within the DFT framework. For each
value of strain, we relax the internal atomic coordinates
while ﬁxing the lattice constants to the strained values.
The results of our calculations are depicted in Fig. 4.
As is clear from Fig. 4 (a) and (c), application of shear
stress σxz (σyz) generates a net moment along ˆy (ˆx), as
expected due to the piezomagnetic eﬀect. In addition,
as shown in Fig. 4 (b) and (d), a tiny spin component
appears along ˆx (ˆy) at the individual Mn sites with an
antiparallel orientation at the neighboring Mn site, cor-
responding to the predicted anti-piezomagnetic eﬀect.
We see from Fig. 4 that both piezo- and antipiezo-
magnetic responses are linear in nature. Also, in both
0 0.04 0.08
-0.002
0
0.002
Net moment along y (    )
Domain 1
Domain 2
0 0.04 0.08
-0.0003
0
0.0003
Moment along x (    )
0 0.04 0.08
-0.002
0
0.002
Net moment along x (    )
0 0.04 0.08
-0.0003
0
0.0003
Moment along y (    )
xz
(a)
µB
µB
Bµ µB
σ σyz
(b)
(c)
(d)
λ  =2r
λ  =1r
Mn1
Mn2
Mn1
Mn2
FIG. 4. Piezo- and antipiezo-magnetic eﬀects in MnF 2. The
variation of (a) the net magnetic moment along the y direc-
tion and (b) the individual Mn magnetic moments along x
direction as the shear strain σxz is varied. The variations of
(c) the net magnetic moment along x direction and (d) the
individual Mn magnetic moments alongy direction as a func-
tion of the shear strain σyz, depicting the piezomagnetic and
antipiezomagnetic eﬀects driven by ferro-type and antiferro-
type magnetic octupoles in MnF 2. For the piezomagnetic ef-
fects in (a) and (c), the variations are shown for two diﬀerent
magnetic domains (in green and blue data points) while for
anti-piezomagnetic eﬀect the variations of local spin magnetic
moments (in green and blue data points) at two Mn atoms
are shown. In both cases, variations are also shown for two
diﬀerent strengths of the spin-orbit coupling constant, viz.,
λr = 1 (solid line) and λr = 2 (dashed line). The parameter
λr is deﬁned at the caption of Fig. 2.
cases the generated moments reverse their directions in
the opposite antiferromagnetic domain. Such a rever-
sal of moment direction is consistent with experimental
reports and can be understood from the fact that both
O32− andO30 octupoles have opposite signs in the oppo-
site antiferromagnetic domains.
Further, to understand the importance of spin-orbit
interaction on these eﬀects, we artiﬁcially doubled the
strength of the spin-orbit coupling in our calculation and
as depicted in Fig. 4, this results in an enhancement in
the generated moment for both cases. This suggests that,
unlike the magnetic Compton scattering described in the
next section, both piezo- and antipiezo-magnetic eﬀects
are relativistic eﬀects. Physically, this can be under-
stood from the fact that the stress applied to the struc-
ture needs to be coupled to the magnetization density of
the system, which is mediated via spin-orbit interaction.
We note that the dependence on the spin-orbit coupling
strength also helps to predict the hierarchy of the piezo
and antipiezo-magnetic eﬀects in diﬀerent materials. For
example, the relativistic piezo- and antipiezo-magnetic
eﬀects are expected to be much stronger in CoF 2 com-
pared to MnF 2 due to the strong spin-orbit interaction

===PAGE BREAK===

9
of the Co atoms in the former.
The predicted anti-piezomagnetic eﬀect should be ex-
perimentally observable by detecting the resulting spin
canting in the presence of a uniform stress. While the
early experiments [57], indeed, indicated rotation of spins
upon application of a shear stress so that an antiparallel
spin-component is generated in addition to a net mag-
netization in a piezomagnetic eﬀect, conﬁrmation of the
antipiezomagnetic eﬀect would require further measure-
ments to verify the linear generation and the switching
of canted moments. Another possibility of experimental
veriﬁcation would be to apply a dynamical stress, caus-
ing opposite stresses on the two Mn sublattices, so that
the anti-piezomagnetic eﬀect would lead to a net magne-
tization. Our work, correlating the piezo- and antipiezo-
magnetic eﬀects to the magnetic octupoles serves as a
guideline for future observation and manipulation of spin
arrangements using strain [52, 53].
B. Direct Detection of Magnetic Octupoles:
Magnetic Compton Proﬁle in an Antiferromagnet
The Compton scattering [59] of x-ray photons, which
was an early conﬁrmation of quantum mechanical be-
havior, is a widely used technique today in ﬁelds as di-
verse as radio-biology, astrophysics, and condensed mat-
ter physics. In condensed matter systems, it is used to
measure the electron density in momentum space or in
an extension known as magnetic Compton scattering, the
spin-dependent electron momentum density [60],
Jmag(pz) =
∫ ∫
[ρ↑(⃗ p)−ρ↓(⃗ p)]dpxdpy . (9)
Here, Jmag is the magnetic Compton proﬁle (MCP), the
key quantity measured in the magnetic Compton scatter-
ing measurements, and ρ↑(⃗ p) and ρ↓(⃗ p) are respectively
the up- and down- spin-polarized electron density in mo-
mentum space.
Magnetic Compton scattering has been extensively ap-
plied to ferri- and ferro-magnetic systems (with non-zero
magnetization) [61–73] to extract spin polarizations at
Fermi surfaces [70–72]. In one of our recent works, we
proposed that a spin-polarized electron density can also
exist in the momentum space of non-magnetic systems,
provided that the inversion symmetry is broken, leading
to a MCP [48]. To date, however, MCP has not been
proposed or measured in conventional antiferromagnets.
Because the up and down spin-polarized bands are degen-
erate, leading to vanishing spin-polarized electron density
in momentum space. Here we show that the spin-splitting
of the energy bands in antiferromagnets with ferro-type
magnetic octupoles results in a non-zero MCP, despite
the zero net magnetization. This, in turn, facilitates the
MCP as a direct probe for existence of ferro-type mag-
netic octupoles.
To verify the non-zero MCP for our example material
MnF2, we explicitly compute the MCP using the methods
implemented in the ELK code (see the computational
details in Appendix A). The computed MCP of MnF 2
along the [110] direction in momentum space is shown in
Fig. 5(a). This is to our knowledge the ﬁrst identiﬁcation
of a MCP in an AFM. We note that the MCP is present
even without including spin-orbit eﬀects, as expected due
to the non-relativistic spin splitting in MnF 2. Note also
that the integral of the MCP is zero, consistent with the
net vanishing moment in the system.
The characteristics of the computed MCP are quite
diﬀerent from those of nonmagnetic ferroelectrics. First,
the computed MCP is symmetric in ⃗ pin contrast to the
antisymmetric MCP in ferroelectrics [48]. This follows
from the symmetric and antisymmetric spin splitting in
MnF2 and ferroelectrics respectively. More importantly,
however, the magnitude of the MCP in MnF2 is larger by
about an order of magnitude compared to the computed
values for the ferroelectrics, PbTiO3 and GeTe [48]. This
again is associated with the large NRSS of the bands
in contrast to the weak relativistic spin-splitting of the
bands in ferroelectrics. Finally, as shown in Fig. 5 (a),
the MCP in MnF 2 changes sign as the momentum di-
rection is changed from the [110] to the [1 ¯10] direction,
unlike the case of ferroelectrics for which the proﬁle, be-
ing antisymmetric, switches sign as ⃗ p→− ⃗ p. Such sign
reversal of the MCP in MnF2 is understandable from the
reversal of the spin splitting as the momentum direction
changes from [110] to [1 ¯10] (see Fig. 3 (b)).
Since the magnetic octupole leads to the spin-splitting
of the bands, which, in turn, gives rise to the MCP, the
MCP provides a direct measurement of the existence of
ferroically ordered magnetic octupoles in MnF 2. For fur-
ther conﬁrmation we compute the MCPs for the cases of
the reversed structure and the other AFM domain (de-
scribed in section III B), for both of which the ferro-type
O32− magnetic octupole reverses sign. Indeed, the com-
puted MCPs, shown in Fig. 5 (a), reverse the sign of
their proﬁle, in agreement with our expectation.
Proposed Experimental Setup. The measurement setup
needed to detect magnetic octupoles using MCP will be
similar to that of a conventional magnetic Compton scat-
tering experiment with circularly polarized light. Gener-
ally, the measurements are performed in back-scattering
geometry with either parallel spin and momentum direc-
tions or along a momentum direction that has at least
one component along the direction of the spin polariza-
tion. Since the spin polarization direction in MnF 2 is
along ˆz, we further compute the MCPs along the [111]
direction in reciprocal space. As depicted in Fig. 5 (b),
the computed MCP, although smaller compared to that
along [110], still has a much larger magnitude compared
to the case of a ferroelectric, suggesting that it is likely
discernible in experiments.
We note that since the two antiferromagnetic domains
lead to opposite spin splitting, it is crucial to carry out
the measurements on a single antiferromagnetic domain
of MnF 2. Such a single antiferromagnetic domain can
be obtained by the simultaneous application of a uniax-

===PAGE BREAK===

10
-8 -4 0 4 8
p [a.u.]
-6
-3
0
3
6
MCP [10       /a.u.]
J     (p     )
J     (p     ) 
J     (p     )
J     (p     )
-8 -4 0 4 8
p [a.u.]
-4
-2
0
2
4 J     (p     )
J     (p     )
mag 110
mag 110
-
-2µB
mag
mag
111
111-
(a) (b)
mag
mag
110
110
RS
RD
µ
FIG. 5. Magnetic Compton proﬁles (MCPs) of MnF 2 along
(a) [110] and [1 ¯10] and (b) [111] and [1 ¯11] directions in the
momentum space. The reversal of the proﬁles is apparent
from (a) and (b) as the momentum direction changes by C4
rotation. Panel (a) also depicts the MCPs along [110] direc-
tion,J RS
mag(p110) andJ RD
mag(p110), for the hypothetical modiﬁed
structure and for the reversed magnetic domain respectively.
In both cases, the MCP switches sign compared to the proﬁle
of MnF2 along the same momentum direction.
ial stress and a magnetic ﬁeld while cooling the sample
through the N´ eel temperature TN ≈ 67 K [35, 58]. It
is interesting to point out here that the combination of
stress and magnetic ﬁeld is in fact the conjugate ﬁeld of
a magnetic octupole, and as described before each of the
antiferromagnetic domains can indeed be identiﬁed as a
ferro-octupolar domain. Such a single magnetic domain
is also referred to as a piezomagnetic domain due to its
close connection to the piezomagnetic eﬀect in MnF2 [58],
driven by the ferroic magnetic octupoles as discussed in
the previous section.
V. DISCUSSIONS AND OUTLOOK
To summarize, using MnF2 as an example material, we
have shown that the order parameter of centrosymmet-
ric antiferromagnets with NRSS is the magnetic octupole,
since it is the lowest-order ferroically ordered magnetic
quantity in this case. The ferromagneto-octupolar order-
ing provides a convenient description of the NRSS and
reveals the conjugate ﬁeld – a combined shear stress and
magnetic ﬁeld – which can in turn manipulate the NRSS
through selection of the magnetic domain. The magnetic
octupole description explains the reported piezomagnetic
response of such systems, and allows us to predict an as-
yet-unobserved nonlinear magnetoelectric eﬀect as well
as an antipiezomagnetic eﬀect resulting from an addi-
tional antiferroic arrangement of diﬀerent magnetic oc-
tupoles. Finally, we propose magnetic Compton scatter-
ing for the direct detection of magnetic octupoles in such
unconventional antiferromagnets.
We note that centrosymmetric antiferromagnets with
NRSS may also have higher-order ferroically ordered
even-parity magnetic multipoles in addition to their
ferromagneto-octupolar order. These higher-order mul-
tipoles are relevant for describing NRSS with g-wave
or i-wave symmetry. For example, Fe 2O3 in its low-
temperature state with magnetic moments oriented along
the symmetry axis, which is reported to have a g-wave
spin splitting [23], allows for a magnetic triakontadipole
in addition to the magnetic octupole. The connection
between this rank-5 even-parity magnetic multipole and
the corresponding g-wave NRSS is an interesting direc-
tion for future study.
In addition to providing important insight into the
newly discovered unconventional antiferromagnets with
NRSS, the results presented here are relevant for the pro-
longed eﬀort to reveal and detect the magnetic octupolar
phase [55, 74–84], as well as for potential applications
through strain engineering of antiferromagnetism via the
piezo- or antipiezo-magnetic eﬀect in spintronic devices.
We note that magnetic octupoles are also likely to be rele-
vant for the reported spin-phonon interaction [85, 86] and
surface magnetization [87] in MnF2, and could shed light
on the reported strong magnetic anisotropy in doped
FeSb2 [37].
Merging the seemingly disconnected ﬁelds of hidden
order, antiferromagnetic spintronics, and inelastic scat-
tering techniques, our work opens up new directions for
exploration which we hope will motivate both theoretical
and experimental investigation in the near future.
ACKNOWLEDGEMENTS
We thank Steve Collins, Jon Duﬀy, Urs Staub, and
Andrea Urru for stimulating discussions. NAS and SB
were supported by the ERC under the EU’s Horizon 2020
Research and Innovation Programme grant No 810451
and by the ETH Zurich. Computational resources were
provided by ETH Zurich’s Euler cluster, and the Swiss
National Supercomputing Centre, project ID eth3.
APPENDIX
A. Computational Details
The electronic structure of MnF 2 has been computed
using the linearized augmented plane wave (LAPW)
method as implemented in the ELK code [88, 89]. We
use the LDA+SOC+U formalism, with Ueﬀ = 5 eV at
the Mn site [18]. A basis set of lmax(apw) = 8, a 5× 5× 7
k-point sampling of the Brillouin zone are used to achieve
self-consistency. The product of the muﬃn-tin radius
(2.4, and 2 a.u. for Mn and F respectively) and the
maximum reciprocal lattice vector is taken to be 7. The
magnetic Compton proﬁle and the atomic-site multipoles
are computed using the extended versions [8, 90] of the
Elk code. The spin-polarized electron momentum densi-
ties are calculated and projected onto the selected mo-
mentum directions (⃗ p) to obtain the magnetic Compton

===PAGE BREAK===

11
-0.4
0
0.4
0.8Energy (eV)
-0.4
0
0.4
0.8Energy (eV)
-0.4
0
0.4
0.8Energy (eV)
-0.4
0
0.4
0.8Energy (eV)
XGMGZRAZ
GMGZRAZX GMGZRAZX
GMGZRAZX
(a) (b)
(c) (d)
Energy (eV)
Energy (eV)Energy (eV)
Energy (eV)
FIG. 6. Nonmagnetic band structure of MnF 2, showing the
dxz and dyz orbital contributions for the (a) Mn1 and (b)
Mn2 sublattices. (c) and (d) depict the same for the hypo-
thetical modiﬁed structure, indicating a reversal of Mn1 and
Mn2 sublattice contributions for the modiﬁed structure.
proﬁle following the implementations, reported in Ref.
[90]. The computed MCP is scaled to the factor that
normalizes the valence contribution of the total Comp-
ton proﬁle to the total number of valence electrons per
formula unit of MnF 2 in the calculation, which is 29 in
this case. For the computation of atomic-site multipoles,
the density matrixρlm,l′m′ is decomposed into the tensor
moments, of which the parity even tensor moments have
contributions from l = l′ terms. We, therefore, evalu-
ate both d−d and p−p matrix element contributions
for the multipoles at the Mn site. The electronic struc-
ture of MnF 2 is also computed within the plane-wave
based projector augmented wave (PAW) [91, 92] method
as implemented in the Vienna ab initio simulation pack-
age (VASP) [93, 94] and the results agree well with that
computed using the ELK code. The atomic relaxations in
presence of shear strain in the piezomagnetic eﬀect are
carried out until the Hellman-Feynman forces on each
atom becomes less than 0.01 eV/ ˚A.
B. Tight-binding Parameters
The realistic tight-binding parameters of the Hamilto-
nian (2), i.e., the eﬀective d−d hoppings ti (i = 1, 4)
and the onsite energies εi (i = 1, 2) in Eq. 3 are ex-
tracted from the DFT calculations by downfolding the
eﬀect of the F- p orbitals using the N th order muﬃn-tin
orbital (NMTO) method [51]. The computed parameters
are listed in Table I.
TABLE I. Tight-binding parameters of the Hamiltonian (2),
extracted using NMTO method.
d-d hopping parameters (Ry) Onsite energies (Ry)
t1 t2 t3 t4 ε1 ε2
0.0036 -0.0038 0.0040 0.0034 -0.1385 -0.0339
C. DFT band structures in absence of magnetism
The computed band structure in absence of magnetism
is shown in Fig. 6, depicting the splitting between bands
of two diﬀerent sublattice contributions along Γ → M.
For example, for the pair of bands around 1 eV along Γ→
M, the top band has predominant contributions from the
Mn1 sublattice while the bottom band is predominantly
of Mn2 sublattice character. For the modiﬁed structure,
described in Section III B, the computed atom and orbital
projected band structure shows that the band structure
remains identical except that the sublattice characters of
the same pair of bands are reversed.
[1] R. W. Millar, J. Am. Chem. Soc. 50, 1875 (1928).
[2] R. W. Tyler, Physical Review 44, 776 (1933).
[3] L. N´ eel, Ann. Phys.11, 232 (1936).
[4] H. Bizette, C. F. Squire, and Tsai, Comptes Rendus
207, 449 (1938).
[5] G. Shull and J. S. Smart, Phys. Rev. 76, 1256 (1949).
[6] C. Ederer and N. A. Spaldin, Phys. Rev. B 76, 214404
(2007).
[7] B. B. V. Aken, J. P. Rivera, H. Schmid, and M. Fiebig,
Nature 449, 702 (2007).
[8] N. A. Spaldin, M. Fechner, E. Bousquet, A. Balatsky,
and L. Nordstr¨ om, Phys. Rev. B88, 094429 (2013).
[9] N. A. Spaldin, M. Fiebig, and M. Mostovoy, J. Phys.
Condens. Matter 20, 434203 (2008).
[10] C. Binek and B. Doudin, J. Phys. Condens. Matter 17,
L39 (2005).
[11] P. Borisov, A. Hochstrat, X. Chen, W. Kleemann, and
C. Binek, Phys. Rev. Lett. 94, 117203 (2005).
[12] H. Watanabe and Y. Yanase, Phys. Rev. B 98, 245129
(2018).
[13] F. Th¨ ole, A. Keliri, and N. A. Spaldin, J. Appl. Phys.
127, 213905 (2020).
[14] B. G¨ obel, A. Mook, J. Henk, and I. Mertig, Phys. Rev.
B 99, 060406 (2019).
[15] S. Bhowal and N. A. Spaldin, Phys. Rev. Lett. 128,
227204 (2022).
[16] Y. Gao and D. Xiao, Phys. Rev. B 98, 060402 (2018).
[17] S. Pekar and G. Rashba, Zh. Eksp. Teor. Fiz. 47, 1927
(1964).
[18] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, Phys. Rev. B 102, 014422 (2020).
[19] L.-D. Yuan, Z. Wang, J.-W. Luo, and A. Zunger, Phys.
Rev. Materials 5, 014409 (2021).

===PAGE BREAK===

12
[20] L. ˇSmejkal, J. Sinova, and T. Jungwirth, Phys. Rev. X
12, 031042 (2022).
[21] L.-D. Yuan and A. Zunger, arXiv 2211.07803 (2022),
10.48550/ARXIV.2211.07803.
[22] L.-D. Yuan, X. Zhang, C. Mera, and A. Zunger,
arXiv2211.09921 (2022), 10.48550/ARXIV.2211.09921.
[23] L. ˇSmejkal, J. Sinova, and T. Jungwirth, arXiv
2204.10844 (2022), 10.48550/ARXIV.2204.10844.
[24] R. Gonz´ alez-Hern´ andez, L.ˇSmejkal, K. V´ yborn´ y, Y. Ya-
hagi, J. Sinova, T. c. v. Jungwirth, and J. ˇZelezn´ y, Phys.
Rev. Lett. 126, 127701 (2021).
[25] D.-F. Shao, S.-H. Zhang, M. Li, C.-B. Eom, and E. Y.
Tsymbal, Nat. Commun. 12, 7061 (2021).
[26] A. Bose, N. J. Schreiber, R. Jain, D.-F. Shao, H. P. Nair,
J. Sun, X. S. Zhang, D. A. Muller, E. Y. Tsymbal, D. G.
Schlom, and D. C. Ralph, Nat. Electron. 5, 267 (2022).
[27] H. Bai, L. Han, X. Y. Feng, Y. J. Zhou, R. X. Su,
Q. Wang, L. Y. Liao, W. X. Zhu, X. Z. Chen, F. Pan,
X. L. Fan, and C. Song, Phys. Rev. Lett. 128, 197202
(2022).
[28] S. Karube, T. Tanaka, D. Sugawara, N. Kadoguchi,
M. Kohda, and J. Nitta, arXiv 2111.07487 (2021),
10.48550/ARXIV.2111.07487.
[29] L. ˇSmejkal, A. B. Hellenes, R. Gonz´ alez-Hern´ andez,
J. Sinova, and T. Jungwirth, Phys. Rev. X 12, 011028
(2022).
[30] L. ˇSmejkal, R. Gonz´ alez-Hern´ andez, T. Jungwirth,
and J. Sinova, Science Advances 6, eaaz8809 (2020),
https://www.science.org/doi/pdf/10.1126/sciadv.aaz8809.
[31] Z. Feng, X. Zhou, L. ˇSmejkal, L. Wu, Z. Zhu, H. Guo,
R. Gonz´ alez-Hern´ andez, X. Wang, H. Yan, P. Qin,
X. Zhang, H. Wu, H. Chen, Z. Xia, C. Jiang, M. Coey,
J. Sinova, T. Jungwirth, and Z. Liu, arXiv2002.08712
(2020), 10.48550/ARXIV.2002.08712.
[32] L. ˇSmejkal, A. H. MacDonald, J. Sinova, S. Nakatsuji,
and T. Jungwirth, Nat. Rev. Mater. 7, 482 (2022).
[33] I. I. Mazin, arXiv 2203.05000 (2022),
10.48550/ARXIV.2203.05000.
[34] L. ˇSmejkal, A. Marmodoro, K.-H. Ahn, R. Gonzalez-
Hernandez, I. Turek, S. Mankovsky, H. Ebert, S. W.
D’Souza, O. ˇSipr, J. Sinova, and T. Jungwirth,
arXiv2211.13806 (2022), 10.48550/ARXIV.2211.13806.
[35] J. Baruchel, A. Draperi, M. E. Kadiri, G. Fillion,
M. Maeder, P. Molho, and J. L. Porteseil, J. Phys. Col-
loques 49, C8 (1988).
[36] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia, and
J. Liu, Nat. Commun. 12, 2846 (2021).
[37] I. I. Mazin, K. Koepernik, M. D. Johannes,
R. Gonz´ alez-Hern´ andez, and L. ˇSmejkal, Proc.
Natl. Acad. Sci. U.S.A. 118, e2108924118 (2021),
https://www.pnas.org/doi/pdf/10.1073/pnas.2108924118.
[38] W. de Haas, B. Schultz, and J. Koolhaas, Physica 7, 57
(1940).
[39] M. S. Seehra and R. E. Helmick, J. Appl. Phys. 55, 2330
(1984), https://doi.org/10.1063/1.333652.
[40] Z. Yamani, Z. Tun, and D. H. Ryan, Can. J. Phys. 88,
771 (2010), https://doi.org/10.1139/P10-081.
[41] W. H. Baur and A. A. Khan, Acta Crystallographica
Section B 27, 2133 (1971).
[42] J. W. Stout and H. E. Adams, J. Am. Chem. Soc. , J.
Am. Chem. Soc. 64, 1535 (1942).
[43] R. A. Erickson, Phys. Rev. 90, 779 (1953).
[44] N. A. Spaldin, M. Fiebig, and M. Mostovoy, J. Condens.
Matter Phys. 20, 434203 (2008).
[45] A. Mansouri Tehrani and N. A. Spaldin, Phys. Rev. Ma-
terials 5, 104410 (2021).
[46] K. Yamauchi, P. Barone, and S. Picozzi, Phys. Rev. B
100, 245115 (2019).
[47] S. Bhowal and N. A. Spaldin, Phys. Rev. Research 3,
033185 (2021).
[48] S. Bhowal, S. P. Collins, and N. A. Spaldin, Phys. Rev.
Lett. 128, 116402 (2022).
[49] S. Hayami, Y. Yanagi, and H. Kusunose, J. Phys. Soc.
Jpn. 88, 123702 (2019).
[50] S. Hayami, Y. Yanagi, and H. Kusunose, Phys. Rev. B
102, 144441 (2020).
[51] O. K. Andersen and T. Saha-Dasgupta, Phys. Rev. B 62,
R16219 (2000).
[52] A. S. Disa, M. Fechner, T. F. Nova, B. Liu, M. F¨ orst,
D. Prabhakaran, P. G. Radaelli, and A. Cavalleri, Nat.
Phys. 16, 937 (2020).
[53] F. Formisano, R. M. Dubrovin, R. V. Pisarev, A. K.
Zvezdin, A. M. Kalashnikova, and A. V. Kimel, Ann.
Phys. , 169041 (2022).
[54] F. Formisano, R. M. Dubrovin, R. V. Pisarev, A. M.
Kalashnikova, and A. V. Kimel, J. Phys. Condens. Mat-
ter 34, 225801 (2022).
[55] A. Urru and N. A. Spaldin, Ann. Phys. , 168964 (2022).
[56] I. Dzialoshinskii, Sov. Phys. – JETP 33, 1454 (1958).
[57] A. S. Borovik-romanov, J. Exptl. Theoret. Phys.38, 1088
(1960).
[58] J. Baruchel, M. Schlenker, and B. Barbara, J. Magn.
Magn. Mater. 15-18, 1510 (1980).
[59] A. H. Compton, Phys. Rev. 21, 483 (1923).
[60] P. M. Platzman and N. Tzoar, Phys. Rev. B 2, 3556
(1970).
[61] N. Sakai and K. ˆOno, Phys. Rev. Lett. 37, 351 (1976).
[62] M. J. Cooper, S. P. Collins, S. W. Lovesey, D. Laundy,
and D. N. Timms, Phys. Scr. T35, 103 (1991).
[63] J. A. Duﬀy, J. W. Taylor, S. B. Dugdale, C. Shenton-
Taylor, M. W. Butchers, S. R. Giblin, M. J. Cooper,
Y. Sakurai, and M. Itou, Phys. Rev. B81, 134424 (2010).
[64] M. Itou, A. Koizumi, and Y. Sakurai, Appl. Phys. Lett.
102, 082403 (2013).
[65] E. Zukowski, S. P. Collins, M. J. Cooper, D. N. Timms,
F. Itoh, H. Sakurai, H. Kawata, Y. Tanaka, and A. Ma-
linowski, J. Condens. Matter Phys. 5, 4077 (1993).
[66] J. A. Duﬀy, J. E. McCarthy, S. B. Dugdale,
V. Honkim¨ aki, M. J. Cooper, M. A. Alam, T. Jarlborg,
and S. B. Palmer, J. Condens. Matter Phys. 10, 10391
(1998).
[67] J. A. Duﬀy, S. B. Dugdale, J. E. McCarthy, M. A. Alam,
M. J. Cooper, S. B. Palmer, and T. Jarlborg, Phys. Rev.
B 61, 14331 (2000).
[68] Z. F. Banﬁeld, J. A. Duﬀy, J. W. Taylor, C. A. Steer,
A. Bebb, M. J. Cooper, L. Blaauw, C. Shenton-Taylor,
and R. Ruiz-Bustos, J. Condens. Matter Phys. 17, 5533
(2005).
[69] C. Shenton-Taylor, J. A. Duﬀy, J. W. Taylor, C. A. Steer,
D. N. Timms, M. J. Cooper, and L. V. Blaauw, J. Con-
dens. Matter Phys. 19, 186208 (2007).
[70] J. A. Duﬀy, J. Phys. Conf. Ser. 443, 012011 (2013).
[71] P. E. Mijnarends, S. Kaprzyk, B. Barbiellini, Y. Li, J. F.
Mitchell, P. A. Montano, and A. Bansil, Phys. Rev. B
75, 014428 (2007).
[72] T. Mizoroki, M. Itou, Y. Taguchi, T. Iwazumi, and
Y. Sakurai, Appl. Phys. Lett. 98, 052107 (2011).

===PAGE BREAK===

13
[73] B. L. Ahuja, AIP Conf Proc 1512, 26 (2013).
[74] P. Santini and G. Amoretti, Phys. Rev. Lett. 85, 2188
(2000).
[75] Y. Kuramoto and H. Kusunose, J. Phys. Soc. Jpn. 69,
671 (2000), https://doi.org/10.1143/JPSJ.69.671.
[76] H. Kusunose, JPSJ News and Comments 4, 06 (2007),
https://doi.org/10.7566/JPSJNC.4.06.
[77] T. Matsumura, T. Yonemura, K. Kunimori, M. Sera, and
F. Iga, Phys. Rev. Lett. 103, 017203 (2009).
[78] M.-T. Suzuki, T. Koretsune, M. Ochi, and R. Arita,
Phys. Rev. B 95, 094406 (2017).
[79] T. Higo, H. Man, D. B. Gopman, L. Wu, T. Koretsune,
O. M. J. van ’t Erve, Y. P. Kabanov, D. Rees, Y. Li, M.-
T. Suzuki, S. Patankar, M. Ikhlas, C. L. Chien, R. Arita,
R. D. Shull, J. Orenstein, and S. Nakatsuji, Nat. Photon
12, 73 (2018).
[80] A. S. Patri, A. Sakai, S. Lee, A. Paramekanti, S. Nakat-
suji, and Y. B. Kim, Nat. Commun. 10, 4092 (2019).
[81] D. D. Maharaj, G. Sala, M. B. Stone, E. Kermarrec,
C. Ritter, F. Fauth, C. A. Marjerrison, J. E. Greedan,
A. Paramekanti, and B. D. Gaulin, Phys. Rev. Lett.
124, 087206 (2020).
[82] G. Khaliullin, D. Churchill, P. P. Stavropoulos, and H.-
Y. Kee, Phys. Rev. Research 3, 033163 (2021).
[83] M. Kimata, N. Sasabe, K. Kurita, Y. Yamasaki,
C. Tabata, Y. Yokoyama, Y. Kotani, M. Ikhlas,
T. Tomita, K. Amemiya, H. Nojiri, S. Nakatsuji, T. Ko-
retsune, H. Nakao, T.-h. Arima, and T. Nakamura, Nat.
Commun. 12, 5582 (2021).
[84] S. Voleti, K. Pradhan, S. Bhattacharjee, T. Saha-
Dasgupta, and A. Paramekanti, arXiv 2211.07666
(2022), 10.48550/ARXIV.2211.07666.
[85] D. J. Lockwood and M. G. Cottam, J. Appl. Phys. 64,
5876 (1988), https://doi.org/10.1063/1.342186.
[86] M. G. Cottam and D. J. Lockwood, Low Temp. Phys.
45, 78 (2019), https://doi.org/10.1063/1.5082316.
[87] V. I. Nizhankovskii, A. I. Kharkovskil, and A. J. Zaleski,
Acta Phys. Pol. A 97(3), 487–490 (2000).
[88] “The Elk Code,” http://elk.sourceforge.net/.
[89] D. Ernsting, D. Billington, T. D. Haynes, T. E. Mil-
lichamp, J. W. Taylor, J. A. Duﬀy, S. R. Giblin, J. K.
Dewhurst, and S. B. Dugdale, J. Phys. Condens. Matter
26, 495501 (2014).
[90] D. Ernsting, D. Billington, T. D. Haynes, T. E. Mil-
lichamp, J. W. Taylor, J. A. Duﬀy, S. R. Giblin, J. K.
Dewhurst, and S. B. Dugdale, J. Condens. Matter Phys.
26, 495501 (2014).
[91] P. E. Bl¨ ochl, Phys. Rev. B50, 17953 (1994).
[92] G. Kresse and D. Joubert, Phys. Rev. B 59, 1758 (1999).
[93] G. Kresse and J. Hafner, Phys. Rev. B 47, 558 (1993).
[94] G. Kresse and J. Furthm¨ uller, Phys. Rev. B 54, 11169
(1996).
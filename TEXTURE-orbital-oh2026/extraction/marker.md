<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2605.21124 -->

Observation of spin-free interatomic orbital angular momentum in a chiral crystal
Dongjin Oh,1, ∗ Sungsoo Hahn,2 Chiara Pacella,3, 4 Junseo Yoo,1
Angel Rubio,4, 5, 6 Domenico Di Sante,3, † and Changyoung Kim1, ‡

arXiv:2605.21124v1 [cond-mat.mtrl-sci] 20 May 2026

1

Department of Physics and Astronomy, Seoul National University, Seoul, 08826, Korea
2
MAX IV Laboratory, Lund University, 22100 Lund, Sweden
3
Department of Physics and Astronomy, University of Bologna, Bologna, Italy
4
Max Planck Institute for the Structure and Dynamics of Matter, Hamburg, Germany
5
Nano-Bio Spectroscopy Group, Departmento de Física de Materiales,
Universidad del País Vasco, San Sebastián, Spain
6
Center for Computational Quantum Physics, The Flatiron Institute, New York, NY, USA
The inherent spin-orbit interaction of electrons inevitably couples spin to the orbital angular
momentum (OAM), posing a fundamental challenge to spin-free orbital transport. Here, we propose a novel strategy to achieve spin-decoupled OAM states in crystalline solids. Using angleresolved photoemission spectroscopy (ARPES), we resolve well-isolated s-orbital bands in a chiral
Te crystal, clearly separated from the p-orbital manifold. Combined circular dichroism ARPES and
first-principles calculations reveal that these bands host OAM arising exclusively from interatomic
hopping, with no intra-atomic contribution. Spin-resolved ARPES further confirms the absence of
SAM, providing decisive evidence of spin-free OAM states. These findings establish the existence
of OAM without spin polarization in crystalline solids and highlight the essential role of interatomic OAM. This work provides a general framework for designing spinless OAM states, opening
an opportunity toward pure orbital currents for orbitronics.

Orbital angular momentum (OAM, ⃗
L) and spin angu⃗
lar momentum (SAM, S) constitute fundamental quantum degrees of freedom of electrons that govern the magnetic properties of condensed matter systems [1]. While
the contribution of OAM has long been regarded as negligible due to its quenching in crystalline environments
[2], its pivotal role in emergent correlated and topological phenomena has recently gained increasing recognition
in quantum material research [3–11]. These advances underscore that, in stark contrast to the conventional notion
of orbital quenching, OAM should be treated as an indispensable degree of freedom in modern condensed matter
physics.
While OAM and SAM originate from fundamentally
distinct origins, disentangling their respective contributions is generally nontrivial. In the presence of atomic
⃗ · S,
⃗ the OAM
spin-orbit coupling (SOC) HSOC ∼ −L
and SAM of electrons become intrinsically entangled
[Fig. 1(a)]. Consequently, under finite SOC, the emergence of OAM is inherently accompanied by a corresponding spin component. For this reason, materials
composed of light elements with small atomic number
Z, and thus weak SOC, are widely regarded as promising platforms for maximizing (minimizing) orbital (spin)
contributions [12, 13]. As such, establishing a fundamental framework for suppressing SAM contributions is a
central challenge in the realization of genuinely spin-free
OAM states [Fig. 1(b)].
A refined classification of OAM provides key insights
into the realization of spinless OAM states. Electronic

∗ Corresponding Author: djeeoh@snu.ac.kr
† Corresponding Author: domenico.disante@unibo.it
‡ Corresponding Author: changyoung@snu.ac.kr

OAM can be categorized into two distinct subtypes
⃗ Atom ), which orig[14, 15]. The first is atomic OAM (L
inates from the OAM of atomic orbitals. Accordingly,
s-orbital electrons are typically considered to carry no
⃗
LAtom . For other orbitals, ⃗
LAtom inevitably couples to
SAM via atomic SOC, posing a fundamental obstacle
to spin-decoupled OAM states. The second contribution is itinerant OAM ( ⃗
LItin ), arising from the geometric phase of Bloch wavefunctions acquired through interatomic electron hopping [14, 15]. Because this contribution does not depend on the atomic orbital char⃗ Itin
acter, even s-orbital electrons can exhibit a finite L
[15, 16]. Moreover, since atomic orbitals with s character carry no ⃗
LAtom , they are not directly coupled to
atomic SOC and do not inherently lead to spin polarization. Taken together, these points indicate that SOC-free
⃗ Itin in the absence
s-orbital electrons may sustain finite L
Atom
of ⃗
L
, offering a viable pathway toward spinless OAM
states. However, despite increasing theoretical attention
[16–20], experimental verification of this itinerant component remains scarce, as prior studies have predominantly
⃗ Atom [3, 21–26].
emphasized the role of L
To realize ⃗
LItin states without spin polarization under
this framework, we focus on chiral materials featuring helical lattice geometry, where interatomic electron hopping
⃗ Itin . In this Letter, we investican naturally generate L
gate the s-orbital states in a chiral Te crystal. A combination of angle-resolved photoemission spectroscopy
(ARPES)-based experiments and first-principles calculations reveals that these states carry finite OAM of purely
interatomic origin while exhibiting no SAM. Our results
⃗ Itin in crystalline
not only underscore the critical role of L
solids but also point to a compelling route to engineering spin-free OAM states by leveraging this interatomic

2

FIG. 1.
(a,b) Schematics of spin-orbit-coupled (a) and
spin-free orbital angular momentum (OAM) states (b). Red,
blue arrows and yellow spheres indicate OAM, spin angular
momentum (SAM), and electrons, respectively. (c) Illustration of chirality-induced orbital selectivity (CIOS) in a righthanded chiral chain. Blue and red circular arrows denote the
⃗ Itin . (d) Tight-binding band structure of sx-component of L
orbital electronic states in a single helical chiral chain. OAM
values are color coded.

contribution.
As an ideal model system, we consider a chiral chain
with a helical lattice structure, in which the microscopic
⃗ Itin can be understood intumechanism underlying L
itively [Fig. 1(c)]. In this chiral lattice, electrons propagating along the chain axis (x-axis) follow helical hopping
path. Therefore, in a right handed chiral chain, electrons
moving in the +x (−x) direction with positive (negative)
group velocity vg acquire +LItin
(−LItin
) [Fig. 1(c)].
x
x
This microscopic mechanism underlying the formation
⃗ Itin is known as chirality-induced orbital selectivity
of L
(CIOS) [27], which can be regarded as the orbital analogue of chirality-induced spin selectivity [28]. This real
space picture can be naturally translated into the band
representation. For a chiral chain possessing threefold
screw-rotation symmetry, a tight-binding model predicts
three electronic bands, as shown in Fig. 1(d) [27]. In this
momentum space representation, the sign of LItin
follows
x

the group velocity of the bands: bands with ∂E/∂k > 0
exhibit +LItin
, whereas those with ∂E/∂k < 0 exhibit
x
−LItin
. This simple model thus provides clear and inx
tuitive insight into how chiral electron hopping, dictated
⃗ Itin .
by the underlying lattice geometry, gives rise to L
In this work, we particularly focus on the s-orbital
⃗ Itin .
states in a helical lattice to verify the existence of L
⃗
Because s-orbital electrons inherently carry no LAtom ,
this offers a clear advantage by enabling the elimination
⃗ Itin .
of atomic contribution and the direct probing of L
We note that elemental Te crystal meets all the essential
criteria for realizing our proposed framework. As illustrated in Fig. 2(a) and 2(b), Te crystalizes in a chiral
chain structure composed of monoatomic helical lattices.
However, since prior studies have concentrated on the
low-energy p states [29–32], these s-orbital bands have so
far remained experimentally unexplored. Therefore, the
first objective of this work is the experimental identification of the s-orbital bands in chiral Te.
To experimentally explore the s-orbital bands in Te, we
performed ARPES experiments. Consistent with previous studies, Te crystal can be easily cleaved along the
(101̄0) surface due to its van der Waals nature [29–
32]. This cleavage plane enables access to the Γ-A-H-K
high symmetry k-path, highlighted as the red plane in
Fig. 2(c). Indeed, the measured Fermi surface using 90
eV photon energy shown in Fig. 2(d) agrees well with
prior result [29], confirming the well cleaved (101̄0) surface.
Figure 2(e) displays the energy-momentum dispersion
along the A-Γ-A high-symmetry k-path, corresponding
to the direction parallel to the Te chiral chain axis. Interestingly, alongside the 5p bands observed within the
E − EF = −6 to 0 eV window, we clearly resolve highly
dispersive 5s bands in the deeper binding energy range of
E − EF = −15 to −8 eV. The dispersion of the s-orbital
states is more clearly visualized in the second-derivative
spectra shown in Fig. 2(f). Remarkably, the experimentally observed dispersion of the s-orbital bands along the
Te chain axis is in striking agreement with the tightbinding band structure of a single chiral chain [Fig. 1(d)].
This excellent agreement between experiment and the
tight-binding model prediction establishes the s-orbital
electronic states in Te crystal as an ideal and experimentally accessible platform for validating our proposed
route toward spin-free OAM states.
We further performed CD-ARPES experiments to verify whether the s-orbital bands of Te carry ⃗
LItin as predicted by the tight-binding model. CD-ARPES technique can probe OAM components that are parallel to
the light propagation direction [33–35]. Therefore, in the
typical ARPES geometry illustrated in Fig. 3(a), where
the incident light impinges obliquely within the plane
of incidence (xz-plane), CD-ARPES allows access to the
x- and z-components of OAM (Lx and Lz ). Following
this methodology, we intentionally align the [0001] axis
of Te along the x-axis of our experimental coordinate
[Fig. 3(a)] in order to probe OAM component parallel

3

FIG. 2. (a,b) Top (a) and side (b) views of the crystal structure of elemental Te. (c) Brillouin zone of Te. The red plane
indicates the momentum regions accessible by ARPES at 90 eV photon energy. The kx , ky , and kz are defined with respect
to the coordinate of the ARPES experimental geometry. (d) Fermi surface of Te measured at a photon energy of 90 eV. The
black dashed rectangle marks the boundary of the first Brillouin zone. The red solid line denotes the plane of incidence in the
ARPES experimental geometry. (e) Raw ARPES spectrum of Te along the A-Γ-A high-symmetry k-path. (f) Corresponding
second-derivative ARPES spectrum. The ARPES spectra shown in (d), (e), and (f) are obtained by averaging data acquired
with right- and left-circularly polarized light.

to the chain. Furthermore, we carefully aligned crystallographic axis such that the [101̄0] direction lies in the
plane of incidence. Therefore, in this experimental coordinate, Lx and Lz are defined as the components parallel
to kx and kz , respectively [Fig. 2(c)].
Figure 3(b) shows the ARPES spectra measured using
right-circular polarization (RCP). Under RCP illumination, only the s-orbital band with negative vg is observed.
In contrast, as shown in Fig. 3(c), a band with positive
vg becomes visible under left-circular polarization (LCP)
light, while the photoelectron intensity of the negative
vg band is reduced. These ARPES spectra acquired under RCP and LCP illumination give rise to the corresponding CD-ARPES spectrum, which clearly exhibits
two bands with opposite CD signs crossing each other
[Fig. 3(d)]. The magnitude of CD at E − EF = −9.2
−1
eV and kx = ±0.4 Å reaches ∓17%, indicating a sizable and physically meaningful CD signal (Supplemental
Material).
Importantly, the observed CD-ARPES spectrum,
which maps the momentum distribution of CD along the
A-Γ-A k-path, reflects the intrinsic CD signal. This highsymmetry CD-ARPES spectrum was obtained along the
−1
ky = 0 Å
line [red solid line in Fig. 2(d)], which is
aligned with the plane of incidence in our experimental geometry [Fig. 3(a)]. In such CD-ARPES configuration, the extrinsic geometrical CD contribution vanishes
−1
−1
at ky = 0 Å [36], whereas away from ky = 0 Å , the
intrinsic CD can be hindered by the extrinsic geometrical CD. Therefore, the measured CD-ARPES spectrum

presented in Fig. 3(d) represents the intrinsic CD signal
of the s-orbital electronic states in Te crystal, which is
proportional to Lx and Lz .
We further conducted SARPES measurements to examine the SAM character of the s-orbital states. The
SARPES measurements were conducted in the same
experimental geometry as the CD-ARPES experiments
[Fig. 3(e)], and spin-resolved energy distribution curves
−1
(SEDCs) were extracted at kx = −0.25 Å , as indicated by the black dashed line in Fig. 3(b). Figures 3(f)3(h) display the measured SEDCs projected onto the Sx ,
Sy , and Sz components, respectively. Interestingly, in
contrast to the presence of a finite CD signal, SEDCs
for spin-up and spin-down contributions show no discernible difference for all three orthogonal spin components. These results indicate the absence of SAM polarization in the s-orbital states of Te, unlike the pronounced radial SAM texture observed in the low-energy
p-orbital bands [29, 30].
Our complementary CD-ARPES and SARPES measurements clearly reveal the emergence of an intrinsic
CD signal in s-orbital states without any accompanying
SAM polarization. It is also worth noting that the observed momentum distribution of CD shown in Fig. 3(d)
⃗ Itin character predicted by CIOS in a
is reminiscent of L
single chiral chain [Fig. 1(d)], capturing the band crossing between the +LItin
and −LItin
states. This suggest
x
x
that the s-orbital electrons hosted by the helical lattice
⃗ Itin .
of the Te can indeed form OAM states induced by L
Itin
Beyond comparison with Lx texture of a single chi-

4

FIG. 3. (a) Schematic illustration of CD-ARPES geometry. The purple arrow denotes incident light with right- and leftcircular polarization (RCP and LCP). (b,c) ARPES spectra of the s-orbital bands measured using RCP (b) and LCP (c). (d)
Corresponding CD-ARPES spectrum (ICD = IRCP − ILCP ). (e) Schematic illustration of the SARPES geometry. (f-h) Spinresolved energy distribution curves (SEDCs) for the Sx (f), Sy (g), and Sz (h) components. The red and blue curves represent
the spin-up and spin-down contributions, respectively. The SEDCs are extracted along the black dashed line indicated in (b).

ral chain model, we further investigate the OAM and
SAM characteristics of the s-orbital states in the Te crystal using first-principles calculations, to elucidate how
these properties evolve from an isolated chain to an array
of chiral chains (Supplemental Material). We examine
the OAM character of s-orbital states using two different theoretical frameworks: atomic-centered approximation (ACA) and modern theory of orbital magnetization
⃗ Itin is completely
[14, 16–20]. In the former approach, L
neglected, and the entire OAM contribution is approxi⃗ Atom . In contrast, the modern theory allows
mated as L
one to compute the global OAM ( ⃗
LGlob ), in which both
⃗
LAtom and ⃗
LItin are simultaneously present. Therefore,
by comparing the OAM character calculated using these
two different approaches, we can gain insight into how
⃗
LAtom and ⃗
LItin incorporate to the s-orbital states.
Figure 4(a) shows the ⃗
LAtom character of s-orbital
states obtained using ACA method as well as SAM polarization. As intuitively expected, these calculations
further confirm that the s-orbital bands indeed do not
⃗ Atom . Moreover, these s-orbital bands do not excarry L
hibit spin splitting as these bands are not affected by
atomic SOC and therefore remain spin-degenerate. Consequently, no spin polarization appears in these bands.
These first-principles calculations are consistent with the
SARPES results, which experimentally demonstrate the
absence of spin polarization [Figs. 3(f)-3(h)].

⃗ Atom texture obtained using
Remarkably, whereas the L
Glob
⃗
the ACA vanishes, the L
calculated within the modern theory framework yields a finite value as shown in
⃗ Glob contains
Fig. 4(b). It is worth noting that although L
Atom
Itin
contributions from both ⃗
L
and ⃗
L
, the s-orbital
states considered here show no contribution from ⃗
LAtom ,
as evidenced in Fig. 4(a). Thus, ⃗
LGlob can effectively
Itin
⃗
be treated as L
for s-orbital electrons. Indeed, LItin
x
texture calculated using tight-binding model for a single chiral chain [Fig. 1(d)] and LGlob
from first-principles
x
calculation for Te crystal [Fig. 4(b), left] show excellent
agreements.
In contrast to the tight-binding model for a single chiral chain [Fig. 1(d)], first-principles calculations for chi⃗ Glob
ral Te crystal reveal finite y- and z-components of L
Glob
Glob
(Ly
and Lz ), as shown in Fig. 4(b). This deviation likely originates from interchain electron hopping.
Indeed, as shown in Fig. 4(c), the iso-energy surface at
E−EF = −9.5 eV exhibits pronounced three-dimensional
dispersion across the Brillouin zone, directly evidencing
electronic coupling between neighboring chains. Correspondingly, the ⃗
LGlob texture projected onto this isoenergy surface displays a complex structure, while preserving the sign reversal of LGlob
between positive and
x
negative kx regions. These results demonstrate that
first-principles calculations faithfully capture the intri⃗ Itin texture arising from three-dimensional eleccate L

5
tronic hybridization in bulk chiral Te.

It is worth noting that although both LItin
and LItin
x
z
components are encoded in the CD-ARPES signal—
making their experimental separation challenging—our
combined CD-ARPES measurements and first-principles
⃗ Itin texture,
calculations unambiguously reveal a pure L
Atom
⃗
without any L
contribution. This constitutes the
first direct spectroscopic evidence for the existence of
⃗ Itin and highlights its fundamental importance in crysL
talline solids. Furthermore, SARPES measurements
demonstrate that engineering s-orbital electrons offers a
promising route to realizing spin-decoupled OAM states
governed by ⃗
LItin . Although the relevant s-orbital states
in chiral Te crystal lie far from the Fermi level, limiting
their immediate practical applicability, our findings lay
the foundation for the rational design of material platforms for spin-free orbitronics.

FIG. 4. OAM and SAM characteristics of s-orbital states in a
right-handed Te crystal. (a) Expectation values of LAtom
and
x
Sx (left), LAtom
and Sy (middle), and LAtom
and Sz (right).
y
z
Each ⃗
LAtom is evaluated within ACA. (b) Expectation values
Glob
of Lx
(left), LGlob
(middle), and LGlob
(right) calculated
y
z
using modern theory of orbital magnetization. (c) Texture of
⃗ Glob mapped onto the iso-energy surface at E − EF = −9.5
L
eV. The color scale represents the magnitude of LGlob
.
x

[1] L. L. Hirst, The microscopic magnetization: concept andapplication, Rev. Mod. Phys. 69, 607 (1997).
[2] C. Kittel, Introduction to solid state physics, 8th ed. (Wiley, Hoboken, NJ, 2005).
[3] Y.-G. Choi, D. Jo, K.-H. Ko, D. Go, K.-H. Kim, H. G.
Park, C. Kim, B.-C. Min, G.-M. Choi, and H.-W. Lee,
Observation of the orbital Hall effect in a light metal Ti,
Nature 619, 52 (2023).
[4] A. El Hamdi, J.-Y. Chauleau, M. Boselli, C. Thibault,
C. Gorini, A. Smogunov, C. Barreteau, S. Gariglio, J.-M.
Triscone, and M. Viret, Observation of the orbital inverse
Rashba–Edelstein effect, Nat. Phys. 19, 1855 (2023).

Acknowledgments—This work was supported by the
National Research Foundation of Korea (NRF) grant
funded by the Korean government (MSIT) (No.
2022R1A3B1077234) and also by GRDC(Global Research Development Center) Cooperative Hub Program through the National Research Foundation of
Korea(NRF) funded by the Ministry of Science and
ICT(MSIT) (RS-2023-00258359). Support from the Institute of Applied Physics at Seoul National University
is acknowledged. We acknowledge the MAX IV Laboratory for beamtime on the Bloch beamline under proposal
20252331. Research conducted at MAX IV, a Swedish
national user facility, is supported by Vetenskapsrådet
(Swedish Research Council, VR) under contract 201807152, Vinnova (Swedish Governmental Agency for Innovation Systems) under contract 2018-04969 and Formas
under contract 2019-02496.

D.O., S.H., and C.P. contributed equally.

[5] J. Liu and X. Dai, Orbital magnetic states in moiré
graphene systems, Nat Rev Phys 3, 367 (2021).
[6] E. Redekop, C. Zhang, H. Park, J. Cai, E. Anderson,
O. Sheekey, T. Arp, G. Babikyan, S. Salters, K. Watanabe, T. Taniguchi, M. E. Huber, X. Xu, and A. F. Young,
Direct magnetic imaging of fractional Chern insulators in
twisted MoTe2 , Nature 635, 584 (2024).
[7] T. Han, Z. Lu, G. Scuri, J. Sung, J. Wang, T. Han,
K. Watanabe, T. Taniguchi, L. Fu, H. Park, and
L. Ju, Orbital multiferroicity in pentalayer rhombohedral
graphene, Nature 623, 41 (2023).
[8] M. Ünzelmann, H. Bentmann, P. Eck, T. Kißlinger,

6
B. Geldiyev, J. Rieger, S. Moser, R. C. Vidal, K. Kißner,
L. Hammer, M. A. Schneider, T. Fauster, G. Sangiovanni,
D. Di Sante, and F. Reinert, Orbital-Driven Rashba Effect in a Binary Honeycomb Monolayer AgTe, Phys. Rev.
Lett. 124, 176401 (2020).
[9] K. Hagiwara, Y. Chen, D. Go, X. L. Tan, S. Grytsiuk,
K. O. Yang, G. Shu, J. Chien, Y. Shen, X. Huang, I. Cojocariu, V. Feyer, M. Lin, S. Blügel, C. M. Schneider,
Y. Mokrousov, and C. Tusche, Orbital Topology of Chiral Crystals for Orbitronics, Adv. Mater. 37, 2418040
(2025).
[10] S. Fukami, K.-J. Lee, and M. Kläui, Challenges and opportunities in orbitronics, Nat. Phys. 10.1038/s41567025-03143-w (2025).
[11] D. Oh, C. Pacella, X. Luo, C. Jozwiak, A. Bostwick,
E. Rotenberg, M. Leandersson, C. Polley, A. Rubio,
D. Di Sante, and R. Comin, p-Wave Orbital Angular
Momentum Texture in a Chiral Crystal, preprint at
https://arxiv.org/abs/2605.15544 (2026).
[12] D. Jo, D. Go, and H.-W. Lee, Gigantic intrinsic orbital
Hall effects in weakly spin-orbit coupled metals, Phys.
Rev. B 98, 214405 (2018).
[13] D. Go, D. Jo, H.-W. Lee, M. Kläui, and Y. Mokrousov,
Orbitronics: Orbital currents in solids, EPL 135, 37001
(2021).
[14] T. Thonhauser, D. Ceresoli, D. Vanderbilt, and R. Resta,
Orbital Magnetization in Periodic Insulators, Phys. Rev.
Lett. 95, 137205 (2005).
[15] R. Burgos Atencia, A. , Amit, , and D. Culcer, Orbital
angular momentum of Bloch electrons: equilibrium formulation, magneto-electric phenomena, and the orbital
Hall effect, Adv. Phys. 9, 2371972 (2024).
[16] O. Busch, I. Mertig, and B. Göbel, Orbital Hall effect
and orbital edge states caused by s electrons, Phys. Rev.
Research 5, 043052 (2023).
[17] S. Bhowal and G. Vignale, Orbital Hall effect as an alternative to valley Hall effect in gapped graphene, Phys.
Rev. B 103, 195309 (2021).
[18] A. Pezo, D. García Ovalle, and A. Manchon, Orbital Hall
effect in crystals: Interatomic versus intra-atomic contributions, Phys. Rev. B 106, 104414 (2022).
[19] A. Pezo, D. García Ovalle, and A. Manchon, Orbital Hall
physics in two-dimensional Dirac materials, Phys. Rev. B
108, 075427 (2023).
[20] T. P. Cysne, S. Bhowal, G. Vignale, and T. G. Rappoport, Orbital Hall effect in bilayer transition metal
dichalcogenides: From the intra-atomic approximation
to the Bloch states orbital magnetic moment approach,
Phys. Rev. B 105, 195421 (2022).
[21] S. R. Park, C. H. Kim, J. Yu, J. H. Han, and C. Kim,
Orbital-Angular-Momentum Based Origin of RashbaType Surface Band Splitting, Phys. Rev. Lett. 107,
156803 (2011).
[22] S. R. Park, J. Han, C. Kim, Y. Y. Koh, C. Kim, H. Lee,
H. J. Choi, J. H. Han, K. D. Lee, N. J. Hur, M. Arita,
K. Shimada, H. Namatame, and M. Taniguchi, Chiral Orbital-Angular Momentum in the Surface States of
Bi2 Se3 , Phys. Rev. Lett. 108, 046805 (2012).
[23] J.-H. Park, C. H. Kim, J.-W. Rhim, and J. H. Han, Orbital Rashba effect and its detection by circular dichroism
angle-resolved photoemission spectroscopy, Phys. Rev. B
85, 195401 (2012).
[24] B. Kim, P. Kim, W. Jung, Y. Kim, Y. Koh, W. Kyung,
J. Park, M. Matsunami, S.-i. Kimura, J. S. Kim, J. H.

Han, and C. Kim, Microscopic mechanism for asymmetric charge distribution in Rashba-type surface states and
the origin of the energy splitting scale, Phys. Rev. B 88,
205408 (2013).
[25] D. Go, D. Jo, C. Kim, and H.-W. Lee, Intrinsic Spin and
Orbital Hall Effects from Orbital Texture, Phys. Rev.
Lett. 121, 086602 (2018).
[26] M. Ünzelmann, H. Bentmann, T. Figgemeier, P. Eck,
J. N. Neu, B. Geldiyev, F. Diekmann, S. Rohlf, J. Buck,
M. Hoesch, M. Kalläne, K. Rossnagel, R. Thomale,
T. Siegrist, G. Sangiovanni, D. D. Sante, and F. Reinert, Momentum-space signatures of Berry flux monopoles
in the Weyl semimetal TaAs, Nat. Commun. 12, 3650
(2021).
[27] B. Göbel, L. Schimpf, and I. Mertig, Chirality-induced
orbital Edelstein effect in an analytically solvable model,
Phys. Rev. Research 7, 033180 (2025).
[28] R. Naaman, Y. Paltiel, and D. H. Waldeck, Chiral
molecules and the electron spin, Nat Rev Chem 3, 250
(2019).
[29] G. Gatti, D. Gosálbez-Martínez, S. Tsirkin, M. Fanciulli,
M. Puppin, S. Polishchuk, S. Moser, L. Testa, E. Martino, S. Roth, P. Bugnon, L. Moreschini, A. Bostwick,
C. Jozwiak, E. Rotenberg, G. Di Santo, L. Petaccia,
I. Vobornik, J. Fujii, J. Wong, D. Jariwala, H. Atwater, H. Rønnow, M. Chergui, O. Yazyev, M. Grioni, and
A. Crepaldi, Radial Spin Texture of the Weyl Fermions in
Chiral Tellurium, Phys. Rev. Lett. 125, 216402 (2020).
[30] M. Sakano, M. Hirayama, T. Takahashi, S. Akebi,
M. Nakayama, K. Kuroda, K. Taguchi, T. Yoshikawa,
K. Miyamoto, T. Okuda, K. Ono, H. Kumigashira,
T. Ideue, Y. Iwasa, N. Mitsuishi, K. Ishizaka, S. Shin,
T. Miyake, S. Murakami, T. Sasagawa, and T. Kondo,
Radial Spin Texture in Elemental Tellurium with Chiral
Crystal Structure, Phys. Rev. Lett. 124, 136404 (2020).
[31] K. Nakayama, M. Kuno, K. Yamauchi, S. Souma, K. Sugawara, T. Oguchi, T. Sato, and T. Takahashi, Band splitting and Weyl nodes in trigonal tellurium studied by
angle-resolved photoemission spectroscopy and density
functional theory, Phys. Rev. B 95, 125204 (2017).
[32] K. Nakayama, A. Tokuyama, K. Yamauchi, A. Moriya,
T. Kato, K. Sugawara, S. Souma, M. Kitamura,
K. Horiba, H. Kumigashira, T. Oguchi, T. Takahashi,
K. Segawa, and T. Sato, Observation of edge states
derived from topological helix chains, Nature 631, 54
(2024).
[33] S. Moser, A toy model for dichroism in angle resolved
photoemission, J. Electron Spectrosc. Relat. Phenom.
262, 147278 (2023).
[34] T. Figgemeier, M. Ünzelmann, P. Eck, J. Schusser,
L. Crippa, J. Neu, B. Geldiyev, P. Kagerer, J. Buck,
M. Kalläne, M. Hoesch, K. Rossnagel, T. Siegrist, L.-K.
Lim, R. Moessner, G. Sangiovanni, D. Di Sante, F. Reinert, and H. Bentmann, Imaging Orbital Vortex Lines in
Three-Dimensional Momentum Space, Phys. Rev. X 15,
011032 (2025).
[35] D. Oh, H. Bentmann, and R. Comin, Interplay of
orbital angular momentum and chirality, Nat. Phys.
10.1038/s41567-025-03113-2 (2025).
[36] S. S. Brinkman, X. L. Tan, B. Brekke, A. C. Mathisen,
O. Finnseth, R. J. Schenk, K. Hagiwara, M.-J. Huang,
J. Buck, M. Kalläne, M. Hoesch, K. Rossnagel, K.-H.
Ou Yang, M.-T. Lin, G.-J. Shu, Y.-J. Chen, C. Tusche,
and H. Bentmann, Chirality-driven orbital angular mo-

7
mentum and circular dichroism in cosi, Phys. Rev. Lett.
132, 196402 (2024).
[37] G. Kresse and J. Furthmüller, Efficiency of ab-initio total
energy calculations for metals and semiconductors using
a plane-wave basis set, Computational Materials Science
6, 15 (1996).
[38] G. Kresse and J. Furthmüller, Efficient iterative schemes
for ab initio total-energy calculations using a plane-wave
basis set, Physical Review B 54, 11169 (1996).
[39] P. E. Blöchl, Projector augmented-wave method, Physical Review B 50, 17953 (1994).
[40] G. Kresse and D. Joubert, From ultrasoft pseudopotentials to the projector augmented-wave method, Physical
Review B 59, 1758 (1999).
[41] J. P. Perdew, K. Burke, and M. Ernzerhof, Generalized
gradient approximation made simple, Physical Review
Letters 77, 3865 (1996).
[42] D. Hobbs, G. Kresse, and J. Hafner, Fully unconstrained
noncollinear magnetism within the projector augmentedwave method, Physical Review B 62, 11556 (2000).
[43] S. Steiner, S. Khmelevskyi, M. Marsman, and G. Kresse,
Calculation of the magnetic anisotropy with projectedaugmented-wave methodology and the case study of disordered fe1−x cox alloys, Physical Review B 93, 224425

(2016).
[44] A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards,
S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder,
and K. A. Persson, The materials project: A materials
genome approach to accelerating materials innovation,
APL Materials 1, 011002 (2013).
[45] N. Marzari and D. Vanderbilt, Maximally localized generalized wannier functions for composite energy bands,
Physical Review B 56, 12847 (1997).
[46] A. A. Mostofi, J. R. Yates, Y.-S. Lee, I. Souza, D. Vanderbilt, and N. Marzari, wannier90: A tool for obtaining maximally-localised wannier functions, Computer
Physics Communications 178, 685 (2008).
[47] G. Pizzi, V. Vitale, R. Arita, S. Blügel, F. Freimuth,
G. Géranton, M. Gibertini, D. Gresch, C. Johnson,
T. Koretsune, J. Ibañez-Azpiroz, H. Lee, J.-H. Lihm,
D. Marchand, A. Marrazzo, Y. Mokrousov, J. I. Mustafa,
Y. Nohara, Y. Nomura, L. Paulatto, S. Poncé, T. Ponweiser, J. Qiao, F. Thöle, S. S. Tsirkin, M. Wierzbowska,
N. Marzari, D. Vanderbilt, I. Souza, A. A. Mostofi, and
J. R. Yates, Wannier90 as a community code: new features and applications, Journal of Physics: Condensed
Matter 32, 165902 (2020).
[48] Postwan,
https://github.com/philipp-eck/post_
wan.git.


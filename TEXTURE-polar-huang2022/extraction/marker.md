# Huang et al. 2022 — Marker extraction (PROSE artifact)

> **NOTE — interim extraction.** The `marker` binary (`marker_single`) is NOT
> installed on this packaging host; only `pdftotext` (poppler) is available.
> This file is the documented interim fallback: `pdftotext -layout` output,
> which best preserves column/table/section structure and reads like the paper.
> **Fidelity loss:** Unicode math symbols and inline equations are degraded
> (pdftotext cannot render LaTeX math — subscripts/vectors/Greek collapse). The
> authoritative equation transcriptions live in `report/REPORT.tex` and in the
> companion `extraction/nougat.mmd` (math artifact).
> **Regenerate with real tool:** `marker_single textures-polar-huang2022.pdf extraction/ --output_format markdown`
>
> Paper: Huang, Shao, Tsymbal, "Ferroelectric control of magnetic skyrmions in
> two-dimensional van der Waals heterostructures", arXiv:2202.11348.

---

  Ferroelectric control of magnetic skyrmions in two-dimensional van
  der Waals heterostructures
  Kai Huang,1 Ding-Fu Shao,2,* and Evgeny Y. Tsymbal1,†
  1
   Department of Physics and Astronomy & Nebraska Center for Materials and Nanoscience, University of Nebraska, Lincoln, Ne-
  braska 68588-0299, USA
  2
      Key Laboratory of Materials Physics, Institute of Solid State Physics, HFIPS, Chinese Academy of Sciences, Hefei 230031, China
  KEYWORDS. Spintronics, Magnetic Skyrmions, Ferroelectricity, Van der Waals Heterostructures.



  ABSTRACT: Magnetic skyrmions are chiral nanoscale spin textures which are usually induced by Dzyaloshinskii–Moriya interaction (DMI).
  Recently, magnetic skyrmions have been observed in two-dimensional (2D) van der Waals (vdW) ferromagnetic materials, such as Fe3GeTe2.
  The electric control of skyrmions is important for their potential application in low-power memory technologies. Here, we predict that DMI
  and magnetic skyrmions in a Fe3GeTe2 monolayer can be controlled by ferroelectric polarization of an adjacent 2D vdW ferroelectric In2Se3.
  Based on density functional theory and atomistic spin-dynamics modeling, we find that the interfacial symmetry breaking produces a sizable
  DMI in a Fe3GeTe2/In2Se3 vdW heterostructure. We show that the magnitude of DMI can be controlled by ferroelectric polarization reversal,
  leading to creation and annihilation of skyrmions. Furthermore, we find that the sign of DMI in a In2Se3/Fe3GeTe2/In2Se3 heterostructure
  changes with ferroelectric switching reversing the skyrmion chirality. The predicted electrically controlled skyrmion formation may be inter-
  esting for spintronic applications.


   Magnetic skyrmions are topological magnetic quasiparticles exhibit-        been shown to efficiently manipulate skyrmions in magnetic thin films
ing a whirling spin texture in real space [1]. These spin-chiral objects      interfaced with perovskite ferroelectrics [21-24].
have recently attracted significant interest due to the rich physics and         The recent discoveries of two-dimensional (2D) van der Waals
promising spintronic applications [2-6]. The formation of magnetic            (vdW) materials exhibiting spontaneous electric or magnetic polariza-
skyrmions usually requires a strong Dzyaloshinskii-Moriya interaction         tions [25-38] opened a new dimension in exploring and exploiting fer-
(DMI) – an exchange interaction between adjacent magnetic moments             roic and topological properties of materials including magnetic skyrmi-
driven by structural asymmetry and spin-orbit coupling [7-9]. Bulk            ons. In a 2D ferromagnet, the symmetry breaking required for DMI to
magnets hosting magnetic skyrmions are limited to those with chiral           be realized by the interfacial proximity effect in a vdW heterostructure
crystal structures that support a finite DMI [2,10-13]. The skyrmions         [39]. This allows the stabilization of magnetic skyrmions in a device
in these chiral magnets are usually observed at low temperature, which        with minimum thickness and even in the absence of the external mag-
limits potential applications. Alternatively, a strong DMI can be in-         netic field, as has been demonstrated in the recent experiments [40-
duced by symmetry breaking and strong spin-orbit coupling at inter-           43].
faces in the multilayer films composed of magnetic and heavy-metal
layers [2,14-16]. This allows the formation of skyrmions at high tem-
perature.
   Currently, the efforts are aimed at exploring the material systems
producing stable magnetic skyrmions that can be conveniently manip-
ulated by external stimulus. Typically, the generation of magnetic skyr-
mions requires an external magnetic field to adjust a delicate balance
between the exchange, anisotropy, DMI, and Zeeman energy contribu-
tions controlling different types of spin textures. Using an electric field   FIG. 1: (a) Schematic of a vdW heterostructure composed of a 2D ferro-
is however a more energy-efficient method to control skyrmions which          magnet and a 2D ferroelectric, where the switching of electric polarization
can be used in low-power spintronics. It has been demonstrated that           ( ⃗ ) can reversibly create and annihilate magnetic skyrmions. (b) Sche-
magnetic skyrmions can be created and annihilated by voltage-con-             matic of a vdW heterostructure where a 2D ferromagnet is sandwiched be-
trolled exchange coupling or magnetic anisotropy [17,18]. Another ap-         tween two identical 2D ferroelectrics. The simultaneous switching of the
proach to electrically control skyrmions is to exploit switchable polari-     polarizations of the top and bottom ferroelectrics ( ⃗ and ⃗ ) changes the
zation of an adjacent ferroelectric material [19,20]. This method has         chirality of magnetic skyrmions.
   A nonvolatile control of magnetic skyrmions by electric field is de-       axes along the in-plane directions of the nearest Fe neighbors (Fig.
sirable for device applications. The recently discovered 2D ferroelectric     2(b)). The absence of DMI in monolayer Fe3GeTe2 can be understood
materials [30-31,44-45], such as In2Se3 [46-49], can be used to mediate       by comparing the energies of two artificial magnetic configurations
this effect. Due to their switchable electric polarization [50-54], the 2D    with opposite chirality. As schematically shown in Fig. 2(c), the clock-
ferroelectrics can provide a voltage tunable interface proximity effect to    wise (CW) and counterclockwise (CCW) configurations of Fe3GeTe2
other 2D materials. In particular, the electric polarization of a 2D ferro-   can be transformed to each other by a      operation. This is due to
electric is expected to efficiently control DMI in an adjacent 2D ferro-      reversing the in-plane components of the Fe moments but conserving
magnet. This is due to DMI being sensitive to the interface orbital hy-       the out-of-plane component, i.e.
bridizations and charge transfer effects [55]. As a result, when hetero-
                                                                                                     ,    ,       = −      ,−       ,   .          (1)
structured with 2D ferromagnets, 2D ferroelectrics can be used to me-
diate the electrical control DMI and thus skyrmion behaviors [56,57].            As a result, the DMI energy  which is determined by the energy
                                                                              difference between the CW and CCW states [63]
   Fe3GeTe2 is a representative 2D ferromagnetic metal [58] which can
be used as a viable material to explore the control of skyrmions by fer-                                      ∝      −          ,                  (2)
roelectric polarization. Experimentally, the emergence of skyrmions              is zero due to the equal values of      and       enforced by     .
has been demonstrated in Fe3GeTe2, under certain conditions [40-43].          Similarly,    ∥ forbids the chiral magnetic configurations and results
Theoretically, when interfaced with a 2D ferroelectric In2Se3 layer (Fig.     in zero DMI in monolayer Fe3GeTe2.
1(a)), different magnitudes of DMI are expected in Fe3GeTe2 depend-
ing ferroelectric polarization of In2Se3. This may lead to the reversable
creation and annihilation of magnetic skyrmions. A Fe3GeTe2 mono-
layer can be further sandwiched between two identical ferroelectric
In2Se3 layers (Fig. 1(b)). In this case, a simultaneous switching of po-
larization in both layers is equivalent to applying a symmetry operation
to the whole system, which is expected to change the sign of DMI and
thus reverse the chirality of magnetic skyrmions.
   In this work, using first-principles density functional theory (DFT)
calculations, we demonstrate that DMI in a Fe3GeTe2 monolayer can
be induced and controlled when it is interfaced with a 2D ferroelectric       FIG. 2: (a,b) The atomic structure of monolayer Fe3GeTe2 – side view (a)
In2Se3 layer. In such a Fe3GeTe2/In2Se3 vdW heterostructure, we find          and top view (b). (c) The artificial magnetic configurations of clockwise
that the reversal of ferroelectric polarization of In2Se3 switches the DMI    (CW) and counterclockwise (CCW) chirality along the [010] direction.
from a large to small value. As a result, based on our atomistic spin-dy-     Red arrows denote the magnetic moment of Fe. The horizontal blue line in
namics modeling, we predict the reversable creation and annihilation          (a) denotes the mirror plane . Blue arrows in (b) denote the symmetry
of skyrmions in the system. Further, we show that the DMI sign in a           operations     ∥ combining time reversal symmetry and two-fold rota-
In2Se3/Fe3GeTe2/In2Se3 sandwich structure changes with ferroelectric          tion symmetry ∥ with respect to the three in-plane axes. Orange and
polarization switching, resulting in the reversal of magnetic skyrmion        green arrows in (c) denote the Heisenberg exchange parameters ( ) and
chirality. Our results show a possibility of the nonvolatile control of       DMI coefficient ( ) between the Fe moments, respectively.
magnetic skyrmions in monolayer Fe3GeTe2 by an electric field, which
may be interesting for the potential application of skyrmion systems.            These symmetry constraints can be broken if the top and bottom
   Fe3GeTe2 is a hexagonal layered ferromagnetic metal with the easy          surfaces of the monolayer Fe3GeTe2 become asymmetric due to an in-
axis along the [001] direction [59-61]. Each Fe3GeTe2 layer contains          terface proximity effect. Here, we consider the proximity of 2D ferroe-
five atomic layers stacked with Te-FeⅠ-GeFeⅡ-FeⅠ-Te sequence, where           lectric In2Se3 interfaced with monolayer Fe3GeTe2. A monolayer In2Se3
FeⅠ denotes the upmost and downmost Fe atoms, and FeⅡ denotes the             contains five triangular lattices stacked with Se-In-Se-In-Se sequence.
Fe atom in the central GeFe plane (Fig. 2(a,b)). In its bulk phase, adja-     The central Se atom is located at one of the two asymmetric but topo-
cent Fe3GeTe2 monolayers are rotated by 180° with respect to each             logically identical sites, associated with a finite out-of-plane polariza-
other, forming a centrosymmetric structure with a magnetic point              tion ⃗ pointing in opposite directions [34,49]. Recent reports show
group 6/       ′ ′ . The presence of inversion symmetry in bulk               that In2Se3 can be effectively used in vdW heterostructures to provide a
Fe3GeTe2 prohibits a finite DMI and hence magnetic skyrmions are not          nonvolatile control of 2D electronic structures despite of very weak in-
expected to emerge in bulk Fe3GeTe2.                                          terlayer coupling [50-53]. Due to both having hexagonal atomic struc-
   Recently, Fe3GeTe2 has been successfully exfoliated down to a mon-         tures and similar in-plane lattice constants [60,64 ], Fe3GeTe2 and
olayer [58,59]. In the absence of the bulk interlayer stacking, mono-         In2Se3 are well matched to construct commensurate vdW heterostruc-
layer Fe3GeTe2 is noncentrosymmetric and belongs to the magnetic              tures. In such heterostructures, the       and      ∥ symmetries are bro-
point group 6 2 . Although the inversion symmetry is broken, the              ken, making DMI finite and thus the appearance of magnetic skyrmions
DMI in monolayer Fe3GeTe2 is still vanishing due to other symmetry            possible. The DMI can be further controlled by ferroelectric polariza-
operations [62], such as (001) mirror plane reflection     (Fig. 2(a)),       tion of In2Se3, resulting in variable behaviors of magnetic skyrmions.
and symmetry operation        ∥ combining  time  reversal symmetry
and two-fold rotation symmetry ∥ with respect to the three in-plane
                                                                                                                                                      2
                                                                              ( ) (Figs. 3(d)), due to the electron charge transfer from Fe3GeTe2
                                                                              to In2Se3. Polarization switching from up to down does not notably
                                                                              change the bands contributed by Fe3GeTe2. However, it shifts the
                                                                              In2Se3 bands to lower energy due to the field effect resulting from the
                                                                              polarization charge of In2Se3.




FIG. 3: (a) Fe3GeTe2/In2Se3 vdW heterostructure for opposite polariza-
tions in In2Se3. (b) In2Se3/Fe3GeTe2/In2Se3 vdW heterostructure. (c) The
band structure of a freestanding Fe3GeTe2 monolayer. (d) The band struc-
ture of Fe3GeTe2/In2Se3 for In2Se3 polarization pointing up (left) and
down (right). (e) The band structure of In2Se3/Fe3GeTe2/In2Se3. The col-
ored dots in (d,e) indicate the bands contributed by In2Se3.

   First, we ascertain that our calculations correctly predict the ground
state of monolayer Fe3GeTe2 and monolayer In2Se3. For Fe3GeTe2, the
magnetic moments of the Fe atoms are calculated to be (Fe ) =
2.18      and (Fe ) = 1.09 . The total energy calculation pre-
dicts an out-of-plane anisotropy with the magnetocrystalline anisot-
ropy energy = [ ] − [ ] = 3.07 meV/f. u. = 8.57 MJ/m .
These values are consistent well with the previous calculations [61].
The band gap and ferroelectric polarization of In2Se3 are estimated to
be 0.64 eV and 1.45 μC/cm , respectively, slightly different to these
reported in Ref. [49] but do not influence the results in this work (see
                                                                              FIG. 4: Calculated magnetic parameters for Fe3GeTe2/In2Se3 and
supporting information).
                                                                              In2Se3/Fe3GeTe2/In2Se3 heterostructures. (a) Magnetic moments of Fe at-
   We then construct a vdW heterostructure by attaching monolayer             oms. (b) Heisenberg exchange parameters ( ) denoted in Fig. 2(c). (c) Ex-
Fe3GeTe2 on top of monolayer In2Se3 (Fig. 3(a)). To ensure that the           change stiffness ( ), magnetic anisotropy ( ), and the DMI coefficient
Fe3GeTe2/In2Se3 stacking corresponds to the ground state, we calcu-           ( ). The single arrows (↑ or ↓) and double arrows (↑↑ or ↓↓) denote the
late the total energy of the bilayer as a function of the lateral alignment   polarization direction in Fe3GeTe2/In2Se3 and In2Se3/Fe3GeTe2/In2Se3,
of the two monolayers (see Supplemental Material for details). We find        respectively.
that the ground state corresponds to the stacking order where FeI at-
oms lie atop the nearest In atom (Fig. 3(a)).                                    Figure 4 shows results of our calculations of the magnetic parameters
   Figures 3 (c,d) show the band structure of the freestanding mono-          for the Fe3GeTe2/In2Se3 bilayer. We find that the magnetic moments of
layer Fe3GeTe2 in comparison to that of the bilayer Fe3GeTe2/In2Se3.          the top FeI atom (denoted by FeI,t) and the central FeII atom do not
We find that the Fe3GeTe2 electronic bands in the bilayer structure           change much compared to those in the freestanding Fe3GeTe2. On the
(Fig. 3(d)) do not change much compared to those in the freestanding          contrary, the magnetic moment of the bottom FeI atom (denoted by
Fe3GeTe2 (Fig. 3(c)). This is due to negligible orbital hybridization         FeI,b), which lies closer to the interface with In2Se3, is reduced by about
across the interface reflecting weak vdW interactions. The bilayer            ~0.1 compared to that in the freestanding Fe3GeTe2. This is due to
bands exhibit a rigid shift toward higher energy resulting from a differ-     the electron charge transfer from Fe3GeTe2 to In2Se3 not related to fer-
ent chemical potential in the heterostructure. The electronic bands           roelectric polarization. The polarization switching in In2Se3 does not
contributed by In2Se3 in the bilayer (denoted by colored dots) are also       produce notable changes in the magnetic moments due to the small po-
similar to those in its freestanding form (not shown). However, the           larization of In2Se3. This is consistent with the similar band structures
conduction band minimum of In2Se3 is shifted below the Fermi level

                                                                                                                                                       3
contributed by Fe3GeTe2 in the Fe3GeTe2/In2Se3 bilayer for different          two interfaces (top and bottom) in the In2Se3/Fe3GeTe2/In2Se3 tri-
polarizations.                                                                layer, where at one interface the polarization is pointing toward the
   The difference in the magnetic moments of the FeI,t and FeI,b atoms        Fe3GeTe2 layer and at the other interface the polarization is pointing
reflects the broken mirror symmetry in the bilayer. As a result, the Hei-     away from the Fe3GeTe2 layer. Therefore, the interfacial proximity ef-
senberg exchange coupling between FeI,t and FeII ( ) is different from        fect on the DMI constant in the In2Se3/Fe3GeTe2/In2Se3 trilayer is a
that between FeI,b and FeII ( ) (Fig. 4(b)). We find that the changes of      sum of the two contributions from two Fe3GeTe2/In2Se3 interfaces.
the Heisenberg exchange parameters and the derived exchange stiff-               The predicted ferroelectric switching of DMI in the
ness ( ) induced by ferroelectric switching are not significant (Fig.         Fe3GeTe2/In2Se3 and In2Se3/Fe3GeTe2/In2Se3 heterostructures indi-
4(b,c)) due to the small ferroelectric polarization in In2Se3. Similarly,     cates a possibility of the electric field control of magnetic skyrmions in
change in the magnetic anisotropy parameter ( ) in response to ferro-         these systems. To demonstrate this effect, we perform the atomistic
electric switching is also not large (Fig. 4(c)).                             spin-dynamics modeling using LLG equation
  The DMI coefficient        can be calculated using [63]                                      ⃗                                         ⃗
                                                                                                   =−      ⃗ × ⃗ +             ⃗ ×               .        (4)
                                      −
                              =                ,                    (3)         Here      is the Gilbert damping constant, is the gyromagnetic ra-
                                    4√3 ℎ
                                                                                          ⃗
   where , ℎ are the lattice constant and layer thickness, respectively.      tio, ⃗ =    ⃗
                                                                                              is the unit magnetization vector for each sublattice with
The finite is supported by the magnetic point group 3 ′1 of the
                                                                              the magnetization ⃗ . The magnetic field ⃗ = −                     is determined
Fe3GeTe2/In2Se3 heterostructure due to broken          and                                                                                   ⃗
                                                              ∥ symme-
                                                                              by the spin Hamiltonian:
tries. We find a large ↑ = 0.28 mJ/m (DMI for polarization of the
In2Se3 is pointing upward) and a small ↓ = 0.06 mJ/m (DMI for                   =−             ⃗ ⋅ ⃗ +         ⃗ ⋅    ⃗ × ⃗ −                    (   ⋅ ⃗ ) (5)
polarization of the In2Se3 is pointing downward). Such a sizable change
in the DMI induced by polarization switching is in contrast to the rela-        where is the magnetic moment of a Fe atom, is the exchange
tively small changes in other magnetic properties. This is due to DMI
                                                                              coupling, ⃗ is the DMI vector, is the magnetic anisotropy energy
being very sensitive to the structural asymmetry, which can be effec-
tively controlled by ferroelectric switching.                                 per Fe atom, and      is the direction of the easy axis.

   Next, we construct a In2Se3/Fe3GeTe2/In2Se3 vdW heterostructure               A supercell of Fe3GeTe2 monolayer with the size of 60 nm × 60 nm
by adding an additional monolayer In2Se3 on the top of                        is used in our simulation. In this supercell, nonmagnetic Ge and Te at-
Fe3GeTe2/In2Se3 (Fig. 3(b)). In order to ensure the low energy stack-         oms are ignored, only Fe honeycomb lattice is kept. A round ferromag-
ing at both interfaces, the top In2Se3 layer is obtained by applying a mir-   netic domain is initially set in the center of the supercell, where the
ror reflection of the bottom In2Se3 monolayer. Figure 3(e) shows the          magnetic moments are pointing along +z/-z directions inside/outside
calculated band structure of the In2Se3/Fe3GeTe2/In2Se3 trilayer with         the domain wall. The magnetic configuration of the system is then re-
polarizations pointing upward for both In2Se3 layers. We find that the        laxed to the equilibrium state. The round domain can gradually relax to
electronic bands contributed by Fe3GeTe2 show negligible changes              a stable skyrmion or shrink and eventually disappear in the background
compared to those in the Fe3GeTe2/In2Se3 bilayer. At the same time,           depending on the magnetic parameters used in the simulation.
the bands contributed by In2Se3 can be considered as a superposition             We find no magnetic skyrmion emerging in our atomistic modeling
of these for Fe3GeTe2/In2Se3 with opposite polarizations (Figs.               with the magnetic parameters given in Fig. 4. This can be explained
3(c,d)).                                                                      from the expected radius ( ) of a skyrmion [65]
   Figure 4 shows the calculated magnetic parameters for the
In2Se3/Fe3GeTe2/In2Se3 heterostructure. The magnitudes of the mag-                                   =                               .                    (6)
netic moments, Heisenberg exchange parameters, and magnetic ani-                                               16       −
sotropy reveal slight changes compared to these of the                           For the calculated magnetic parameters in Fig. 4, we obtain the larg-
Fe3GeTe2/In2Se3 structure. As expected, the magnetic moments                  est to be ~0.03 nm, which is too small to observe. This is due to a
  (Fe , ) and (Fe , ) as well as the exchange constants and                   very large magnetic anisotropy predicted theoretically for Fe3GeTe2
swap their values upon the simultaneous switching of polarizations of         [61] compared to the recent experimental measurements where mag-
both In2Se3 layers. This is because such a switching is equivalent to ap-     netic skyrmions were observed in various Fe3GeTe2 based systems [40-
plying     ∥ operation to the system, which swap the moments and ex-          43].
change parameters on top and bottom of the GeFeII plane.                         It is known that the magnetic anisotropy of Fe3GeTe2 can be strongly
   The DMI coefficient for polarization of both In2Se3 layers pointing        suppressed by many factors such as doping and temperature [66-68].
upward (downward) is calculated to be ↑↑ ≈ 0.22 mJ/m ( ↓↓ ≈                   Indeed, if we use the calculated and parameters and the radius of
−0.24 mJ/m ). We see that within the calculation accuracy, ↑↑ ≈               the magnetic skyrmions ~100 nm reported experimentally [40-43],
− ↓↓ , i.e. the sign of the DMI coefficient changes with polarization         a much weaker magnetic anisotropy ~0.008 MJ/m is estimated by
switching, which is due to ferroelectric switching being equivalent to        Eq. (4). We thus assume a moderate anisotropy value of ~0.04 MJ/
the      ∥ symmetry transformation. Comparing the DMI coefficients            m for our modelling to qualitatively demonstrate ferroelectric effect
for the Fe3GeTe2/In2Se3 and In2Se3/Fe3GeTe2/In2Se3 structures (Fig.           on the appearance of skyrmions in the considered systems.
4), we find ↑↑ ≈ ↑ − ↓ . This result follows from the presence of
                                                                                                                                                            4
FIG. 5: (a,b,c,d) Results of atomistic spin-dynamics modeling of the Fe3GeTe2/In2Se3 vdW heterostructure (a,b) and the In2Se3/Fe3GeTe2/In2Se3
vdW heterostructure (c,d) for different ferroelectric polarizations.

   With this value of K, the results of our atomistic spin-dynamics        the DMI sign was changed with ferroelectric switching, resulting in
modeling predict for the Fe3GeTe2/In2Se3 heterostructure, that a           the reversal of chirality of the magnetic skyrmions. Our work
Néel-type skyrmion of about 12 nm in diameter emerges when the             demonstrated a possibility of the nonvolatile control of magnetic
polarization is pointing upward (Fig. 5(a)) and disappears when the        skyrmions in monolayer Fe3GeTe2 by an applied electric field, which
polarization is pointing downward (Fig. 5(b)). Such creation and           is promising for the potential device application of skyrmion sys-
annihilation of a magnetic skyrmion in this heterostructure is due to      tems.
the change of DMI with reversal of ferroelectric polarization of
In2Se3. For the In2Se3/Fe3GeTe2/In2Se3 heterostructure, we obtain a        ASSOCIATED CONTENT
skyrmion of about 6 nm in diameter (Fig. 5(c)). As expected, its chi-      Supporting Information
rality is reversed with reversal of polarization of In2Se3 (Fig. 5(d))     Additional details of computational methods; theoretical derivation of
due to the change of the DMI sign.                                         the DMI vector; calculation of the DMI vectors in Fe3GeTe2 based sys-
   Previous investigations showed that magnetic skyrmions can be           tems; total energy calculations of the most stable Fe3GeTe2/In2Se3
                                                                           stacking order.
moved at a high speed by a moderate electric current, indicating
promising spintronic applications [1]. A well-controlled writing and
                                                                           AUTHOR INFORMATION
erasing process is required prior to such applications. The creation
and annihilation of skyrmions by voltage is desirable for this pur-        Corresponding Authors
pose, due to low energy consumption. Our work demonstrates that            Ding-Fu Shao – https://orcid.org/0000-0002-2732-4131; Email:
the required functional behavior can be achieved in a                      dfshao@issp.ac.cn
Fe3GeTe2/In2Se3 system where the interfacial proximity of a 2D             Evgeny Y. Tsymbal – https://orcid.org/0000-0002-6728-5480; Email:
magnet and a 2D ferroelectric induces DMI dependent on ferroelec-          tsymbal@unl.edu
tric polarization. The controllable chirality of skyrmions in a
                                                                           Authors
In2Se3/Fe3GeTe2/In2Se3 heterostructure may be interesting for pro-
grammable skyrmion-based memories and logic [69]. The proposed             Kai Huang – https://orcid.org/0000-0001-5527-3426; Email:
                                                                           kai.huang@huskers.unl.edu
approach is not limited to the Fe3GeTe2/In2Se3 system, but should
be valid for vdW heterostructures constructed from other 2D ferro-         Notes
ics.                                                                       The authors declare no competing financial interest.
   In conclusion, based on first-principles DFT calculations and at-
omistic spin-dynamics modelling, we have demonstrated that the             ACKNOWLEDGMENTS
Dzyaloshinskii–Moriya interaction in monolayer Fe3GeTe2 can be             The authors thank Robert Streubel for stimulating discussions. This
induced and controlled by ferroelectric polarization of an adjacent        work was supported by the by the EPSCoR RII Track-1 (NSF Award
ferroelectric In2Se3. For a Fe3GeTe2/In2Se3 vdW heterostructure, we        OIA-2044049) program. Computations were performed at the Univer-
have predicted that the reversal of ferroelectric polarization of In2Se3   sity of Nebraska Holland Computing Center.
can switch the DMI of the system from a large to small value, result-
ing in the reversible skyrmion creation and annihilation. For a
In2Se3/Fe3GeTe2/In2Se3 vdW heterostructure, we have shown that

                                                                                                                                               5
    (1) Rößler, U. K.; Bogdanov, A. N.; Pfleiderer, C. Spontaneous skyrmion              (21) Wang, L.; Feng, Q.; Kim, Y.; Kim, R.; Lee, K. H.; Pollard, S. D.; Shin,
ground states in magnetic metals. Nature 2006, 442, 797–801.                         Y. J.; Zhou, H.; Peng, W.; Lee, D.; Meng, W.; Yang, H.; Han, J. H.; Kim, M.;
    (2) Fert, A.; Reyren, N.; Cros, V. Magnetic skyrmions: advances in phys-         Lu, Q.; Noh, T. W. Ferroelectrically tunable magnetic skyrmions in ultrathin
ics and potential applications. Nat. Rev. Mater. 2017, 2, 17031.                     oxide heterostructures. Nature Mater. 2018, 17, 1087–1094.
    ( 3 ) Tokura, Y.; Tokura, Y. Magnetic skyrmion materials. Chem. Rev.                 (22) Tsymbal, E. Y.; Panagopoulos, C. Whirling spins with a ferroelectric.
2021, 121, 2857–2897.                                                                Nature Mater. 2018, 17, 1054–1055.
    (4) Göbel, B.; Mertig, I.; Tretiakov, O. A. Beyond skyrmions: Review and             (23) Tikhonov, Yu.; Kondovych, S.; Mangeri, J.; Pavlenko, M.; Baudry,
perspectives of alternative magnetic quasiparticles. Phys. Rep. 2021, 895, 1–        L.; Sené, A.; Galda, A.; Nakhmanson, S.; Heinonen, O.; Razumnaya, A.;
28.                                                                                  Luk’yanchuk, I.; Vinokur, V. M. Controllable skyrmion chirality in ferroelec-
    (5) Everschor-Sitte, K.; Masell, J.; Reeve, R. M.; Kläui, M. Perspective:        trics. Scientific Reports 2020, 10, 8657.
Magnetic skyrmions—Overview of recent progress in an active research                     (24) Wang, Y.; Sun, J.; Shimada, T.; Hirakata, H.; Kitamura, T.; Wang, J.
field. J. Appl. Phys. 2018, 124, 240901.                                             Ferroelectric control of magnetic skyrmions in multiferroic heterostruc-
    ( 6 ) Nagaosa, N.; Tokura, Y. Topological properties and dynamics of             tures. Phys. Rev. B 2020, 102, 014440.
magnetic skyrmions. Nature Nanotech 2013, 8, 899–911.                                    (25) Gong, C.; Zhang, X. Two-dimensional magnetic crystals and emer-
    (7) Dzyaloshinsky, I. A thermodynamic theory of “weak” ferromagnetism            gent heterostructure devices. Science 2019, 363, eaav4450.
of antiferromagnetics. J. Phys. Chem. Solids 1958, 4, 4.                                 (26) Gibertini, M.; Koperski, M.; Morpurgo, A. F.; Novoselov, K. S. Mag-
    (8) Moriya, T. New Mechanism of Anisotropic Superexchange Interac-               netic 2D materials and heterostructures. Nat. Nanotechnol. 2019, 14, 408–
tion. Phys. Rev. Lett. 1960, 4, 228.                                                 419.
    ( 9) Moriya, T. Anisotropic superexchange interaction and weak ferro-                (27) Huang, P.; Zhang, P.; Xu, S.; Wang, H.; Zhang, X.; Zhang, H. Recent
magnetism. Phys. Rev. 1960, 120, 91.                                                 advances in two-dimensional ferromagnetism: materials synthesis, physical
    ( 10 ) Mühlbauer, S.; Binz, B.; Jonietz, F.; Pfleiderer, C.; Rosch, A.;          properties and device applications. Nanoscale 2020, 12, 2309–2327.
Neubauer, A.; Georgii, R.; Böni, P. Skyrmion Lattice in a Chiral Magnet. Sci-            (28) Jiang, X.; Liu, Q.; Xing, J.; Liu, N.; Guo, Y.; Liu, Z.; Zhao, J. Recent
ence 2009, 323, 5916.                                                                progress on 2D magnets: Fundamental mechanism, structural design and
    (11) Tanigaki, T.; Shibata, K.; Kanazawa, N.; Yu, X.; Onose, Y.; Park, H.        modification. Appl. Phys. Rev. 2021, 8, 031305.
S.; Shindo, D.; Tokura, Y. Real-space observation of short-period cubic lat-             (29) Gong, C.; Li, L.; Li, Z.; Ji, H.; Stern, A.; Xia, Y.; Cao, T.; Bao, Wei;
tice of skyrmions in MnGe. Nano Lett. 2015, 15, 5438–5442.                           Wang, C.; Wang, Y.; Qiu, Z. Q.; Cava, R. J.; Louie, S. G.; Xia, J.; Zhang, X.
    (12) Seki, S.; Yu, X. Z.; Ishiwata, S.; Tokura, Y. Observation of Skyrmions      Discovery of intrinsic ferromagnetism in two-dimensional van der Waals
in a Multiferroic Material. Science 2012, 336, 198–201.                              crystals. Nature 2017, 546, 265–269.
    (13) Kézsmárki, I.; Bordács, S.; Milde, P.; Neuber, E.; Eng, L. M.; White,           ( 30) Wu, M. Two-dimensional van der Waals ferroelectrics: Scientific
J. S.; Rønnow, H. M.; Dewhurst, C. D.; Mochizuki, M.; Yanai, K.; Nakamura,           and technological opportunities. ACS Nano 2021, 15, 9229–9237.
H.; Ehlers, D.; Tsurkan, V.; Loidl, A. Néel-type skyrmion lattice with con-              (31) Tsymbal, E. Y. Two-dimensional ferroelectricity by design. Science
fined orientation in the polar magnetic semiconductor GaV4S8. Nature Ma-             2021, 372, 1389–1390.
ter. 2015, 4, 1116–1122.                                                                 (32) Belianinov, A.; He, Q.; Dziaugys, A.; Maksymovych, P.; Eliseev, E.;
    (14) Heinze, S.; von Bergmann, K.; Menzel, M.; Brede, J.; Kubetzka, A.;          Borisevich, A.; Morozovska, A.; Banys, J.; Vysochanskii, Y.; Kalinin, S. V.
Wiesendanger, R.; Bihlmayer, G.; Blügel, S. Spontaneous atomic-scale mag-            CuInP2S6 Room Temperature Layered Ferroelectric. Nano Lett. 2015, 15,
netic skyrmion lattice in two dimensions. Nature Phys. 2011, 7, 713–718.             3808–3814.
    ( 15 ) Boulle, O.; Vogel, J.; Yang, H.; Pizzini, S.; Chaves, D. de Souza;            (33) Chang, K.; Liu, J.; Lin, H.; Wang, N.; Zhao, K.; Zhang, A.; Jin, F.;
                                                   -Prejbeanu, L. D.; Klein, O.;     Zhong, Y.; Hu, X.; Duan, W.; Zhang, Q.; Fu, L.; Xue, Q.-K.; Chen, X.; Ji, S.-
Belmeg-uenai, M.; Roussigné, Y.; Stashkevich, A.; Chérif, S. M.; Aballe, L.;         H. Discovery of robust in-plane ferroelectricity in atomic-thick SnTe. Science
Foerster, M.; Chshiev, M.; Auffret, S.; Miron, I. M.; Gaudin, G. Room-tem-           2016, 353, 274-278.
perature chiral magnetic skyrmions in ultrathin magnetic nanostructures.                 (34) Xiao, J.; Zhu, H.; Wang, Y.; Feng, W.; Hu, Y.; Dasgupta, A.; Han, Y.;
Nature Nanotech. 2016, 11, 449–454.                                                  Wang, Y.; Muller, D. A.; Martin, L. W.; Hu, P.; Zhang, X. Intrinsic two-di-
    (16) Woo, S.; Litzius, K.; Krüger, B.; Im, M.-Y.; Caretta, L.; Richter, K.;      mensional ferroelectricity with dipole locking. Phys. Rev. Lett. 2018, 120,
Mann, M.; Krone, A.; Reeve, R. M.; Weig, M.; Agrawal, P.; Lemesh, I.;                227601.
Mawass, M.-A.; Fischer, P.; Kläui, M.; Beach, G. S. D. Observation of room-              (35) Fei, Z.; Zhao, W.; Palomaki, T. A.; Sun, B.; Miller, M. K.; Zhao, Z.;
temperature magnetic skyrmions and their current-driven dynamics in ul-              Yan, J.; Xu, X.; Cobden D. H. Ferroelectric switching of a two-dimensional
trathin metallic ferromagnets. Nature Mater. 2016, 15, 501–506.                      metal. Nature 2018, 560, 336–339.
    (17) Hsu, P.-J.; Kubetzka, A.; Finco, A.; Romming, N.; von Bergmann,                 (36) Sharma, P.; Xiang, F.-X.; Shao, D.-F.; Zhang, D.; Tsymbal, E. Y.;
K.; Wiesendanger R. Electric-field-driven switching of individual magnetic           Hamilton, A. R.; Seidel, J. A room-temperature ferroelectric semimetal. Sci.
skyrmions. Nature Nanotech. 2017, 12, 123–126.                                       Adv. 2019, 5, eaax5080.
    (18) Bhattacharya, D.; Razavi, S. A.; Wu, H.; Dai, B.; Wang, K. L.; Atu-             (37) Yasuda, K.; Wang, X.; Watanabe, K.; Taniguchi, T.; Jarillo-Herrero,
lasimha, J. Creation and annihilation of non-volatile fixed magnetic skyrmi-         P. Stacking-engineered ferroelectricity in bilayer boron nitride. Science 2021,
ons using voltage control of magnetic anisotropy. Nature Electronics 2020, 3,        372, 1458–1462.
539–545.                                                                                 (38) Stern, M. V.; Waschitz, Y.; Cao, W.; Nevo, I.; Watanabe, K.; Tanigu-
    ( 19 ) Liang, J.; Cui, Q.; Yang, H. Electrically switchable Rashba-type          chi, T.; Sela, E.; Urbakh, M.; Hod, O.; Shalom, M. B. Interfacial ferroelectric-
Dzyaloshinskii-Moriya interaction and skyrmion in two-dimensional mag-               ity by van der Waals sliding. Science 2021, 372, 1462–1466.
netoelectric multiferroics. Phys. Rev. B 2020, 102, 220409(R).                           (39)                   -Abiague, A.; Scharf, B.; Dery, H.; Belashchenko, K.
    (20) Cui, Q.; Zhu, Yi.; Jiang, J.; Liang, J.; Yu, D.; Cui, P.; Yang, H. Ferro-   Proximitized materials. Mater. Today 2019, 22, 85-107.
electrically controlled topological magnetic phase in a Janus-magnet-based               (40) Park, T.-E.; Peng, L.; Liang, J.; Hallal, A.; Yasin, F. S.; Zhang, X.;
multiferroic heterostructure. Phys. Rev. Research 2021, 3, 043011.                   Song, K. M.; Kim, S. J.; Kim, K.; Weig, M.; Schütz, G.; Finizio, S.; Raabe, J.;


                                                                                                                                                                    6
Garcia, K.; Xia, J.; Zhou, Y.; Ezawa, M.; Liu, X.; Chang, J.; Koo, H. C.; Kim,            (54) Shao, D.-F.; Ding, J.; Gurung, G.; Zhang, S.-H.; Tsymbal, E. Y. In-
Y. D.; Chshiev, M.; Fert, A.; Yang, H.; Yu, X.; Woo, S. Néel-type skyrmions           terfacial crystal Hall effect reversible by ferroelectric polarization. Phys. Rev.
and their current-induced motion in van der Waals ferromagnet-based het-              Applied 2021, 15, 024057.
erostructures. Phys. Rev. B 2021, 103, 104410.                                            (55) Yang, H.; Boulle, O.; Cros, V.; Fert, A.; Chshiev, M. Controlling
    (41) Ding, B.; Li, Z.; Xu, G.; Li, Hang; Hou, Z.; Liu, E.; Xi, X.; Xu, F.; Yao,   Dzyaloshinskii-Moriya interaction via chirality dependent atomic-layer
Y.; Wang, W. Observation of magnetic skyrmion bubbles in a van der Waals              stacking, insulator capping and electric field. Scientific Reports 2018, 8, 2356.
ferromagnet Fe3GeTe2. Nano Lett. 2020, 2, 20.                                             (56) Chen, D.; Sun, W.; Li, H.; Wang, J.; Wang, Y. Tunable magnetic an-
    (42) Wu, Y.; Zhang, S.; Zhang, J.; Wang, W.; Zhu, Y. L.; Hu, J.; Yin, G.;         isotropy and Dzyaloshinskii-Moriya interaction in an ultrathin van der Waals
Wong, K.; Fang, C.; Wan, C.; Han, X.; Shao, Q.; Taniguchi, T.; Watanabe,              Fe3GeTe2/In2Se3 heterostructure. Front. Phys. 2020, 8, 402.
K.; Zang, J.; Mao, Z.; Zhang, X.; Wang, K. L. Néel-type skyrmion in                       (57) Li, C.; Yao, X.; Chen, G. Writing and deleting skyrmions with elec-
WTe2/Fe3GeTe2 van der Waals heterostructure. Nat. Commun. 2020, 11,                   tric fields in a multiferroic heterostructure. Phys. Rev. Research 2021, 3,
3860.                                                                                 L012026.
    (43) Yang, M.; Li, Q.; Chopdekar, R. V.; Dhall, R.; Turner, J.; Carlström,            (58) Deng, Y.; Yu, Y.; Song, Y.; Zhang, J.; Wang, N. Z.; Sun, Z.; Yi, Y.;
J. D.; Ophus, C.; Klewe, C.; Shafer, P.; N'Diaye, A. T.; Choi, J. W.; Chen, G.;       Wu, Y. Z.; Wu, S.; Zhu, J.; Wang, J.; Chen, X. H.; Zhang, Y. Gate-tunable
Wu, Y. Z.; Hwang, C.; Wang, F.; Qiu, Z. Q. Creation of skyrmions in van der           room-temperature ferromagnetism in two-dimensional Fe3GeTe2. Nature
Waals ferromagnet Fe3GeTe2 on (Co/Pd)n superlattice. Sci. Adv. 2020, 6,               2018, 563, 94–99.
eabb5157.                                                                                 (59) Fei, Z.; Huang, B.; Malinowski, P.; Wang, W.; Song, T.; Sanchez, J.;
    (44) Osada, M.; Sasaki, T. The rise of 2D dielectrics/ferroelectrics. APL         Yao, W.; Xiao, D.; Zhu, X.; May, A. F.; Wu, W.; Cobden, D. H.; Chu, J.-H.;
Materials 2019, 7, 120902.                                                            Xu, X. Two-dimensional itinerant ferromagnetism in atomically thin
    (45) Guan, Z.; Hu, H.; Shen, X.; Xiang, P.; Zhong, N.; Chu, J.; Duan, C.          Fe3GeTe2. Nature Mater. 2018, 17, 778–782.
Recent progress in two-dimensional ferroelectric materials. Adv. Electron.                (60) Chen, B.; Yang, J.; Wang, H.; Imai, M.; Ohta, H.; Michioka, C.; Yo-
Mater. 2020, 6, 1900818.                                                              shimura, K.; Fang, M. Magnetic properties of layered itinerant electron fer-
    (46) Cui, C.; Hu, W.-J.; Yan, X.; Addiego, C.; Gao, W.; Wang, Y.; Wang,           romagnet Fe3GeTe2. J. Phys. Soc. Jpn. 2013, 82, 124711.
Z.; Li, L.; Cheng, Y.; Li, P.; Zhang, X.; Alshareef, H. N.; Wu, T.; Zhu, W.;              (61) Zhuang, H. L.; Kent, P. R. C.; Hennig, R. G. Strong anisotropy and
Pan, X.; Li, L.-J. Intercorrelated in-plane and out-of-plane ferroelectricity in      magnetostriction in the two-dimensional Stoner ferromagnet Fe3GeTe2.
ultrathin two-dimensional layered semiconductor In2Se3. Nano Lett. 2018,              Phys. Rev. B 2016, 93, 134407.
18, 1253                                                                                  (62) Laref, S.; Kim, K.; Manchon, A. Elusive Dzyaloshinskii-Moriya in-
    (47) Zhou, Y.; Wu, D.; Zhu, Y.; Cho, Y.; He, Q.; Yang, X.; Herrera, K.;           teraction in monolayer Fe3GeTe2. Phys. Rev. B 2020, 102, 060402(R).
Chu, Z.; Han, Y.; Downer, M. C.; Peng, H.; Lai, K. Out-of-plane piezoelec-                (63) Yang, H.; Thiaville, A.; Rohart, S.; Fert, A.; Chshiev, M. Anatomy of
                                           -In2Se3 nanoflakes. Nano Lett. 2017,       Dzyaloshinskii-Moriya interaction at Co/Pt interfaces. Phys. Rev. Lett. 2015,
17, 5508–5513.                                                                        115, 267210.
    (48) Xue, F.; Hu, W.; Lee, K.-C.; Lu, L.-S.; Zhang, J.; Tang, H.-L.; Han,             (64) Tao, X.; Gu, Y. Crystalline                                             -
A.; Hsu, W.-T.; Tu, S.; Chang, W.-H.; Lien, C.-H.; He, J.-H.; Zhang, Z.; Li,          dimensional In2Se3 thin layers. Nano Lett. 2013, 13, 3501–3505.
L.-J.; Zhang, X. Room-                                                            -       (65) Wang, X.S.; Yuan, H.Y.; Wang, X.R. A theory on skyrmion size. Com-
In2Se3 nanoflakes down to the monolayer limit. Adv. Funct. Mater. 2018, 28,           mun. Phys. 2018, 1, 31.
1803738.                                                                                  (66) Wanga, Y.-P.; Chen, X.-Y.; Long, M.-Q. Modifications of magnetic
    (49) Ding, W.; Zhu, J.; Wang, Z.; Gao, Y.; Xiao, D.; Gu, Y.; Zhang, Z.;           anisotropy of Fe3GeTe2 by the electric field effect. Appl. Phys. Lett. 2020,
Zhu, W. Prediction of intrinsic two-dimensional ferroelectrics in In2Se3 and          116, 092404.
other III2-VI3 van der Waals materials. Nat. Commun. 2017, 8, 14956.                      (67) Park, S. Y.; Kim, D. S.; Liu, Y.; Hwang, J.; Kim, Y.; Kim, W.; Kim, J.-
    (50) Gong, C.; Kim, E. M.; Wang, Y.; Lee, G.; Zhang, X. Multiferroicity           Y.; Petrovic, C.; Hwang, C.; Mo, S.-K.; Kim, H.-J.; Min, B.-C.; Koo, H. C.;
in atomic van der Waals heterostructures. Nat. Commun. 2019, 10, 2657.                Chang, J.; Jang, C.; Choi, J. W.; Ryu, H. Controlling the magnetic anisotropy
    ( 51 ) Wang, Z.; Zhu, W. Tunable band alignments in 2D ferroelectric              of the van der waals ferromagnet Fe3GeTe2 through hole doping. Nano. Lett.
  ‑In2Se3 based Van der Waals heterostructures. ACS Appl. Electron. Mater.            2020, 20, 95–100.
                                                                                          (68) Tan, C.; Lee, J.; Jung, S.-G.; Park, T.; Albarakati, S.; Partridge, J.;
2021, 3, 5114–5123.
                                                                                      Field, M. R.; McCulloch, D. G.; Wang, L.; Lee, C. Hard magnetic properties
    (52) Wan, S.; Li, Y.; Li, W.; Mao, X.; Wang, C.; Chen, C.; Dong, J.; Nie,
                                                                                      in nanoflake van der Waals Fe3GeTe2. Nat. Commun. 2018, 9, 1554.
A.; Xiang, J.; Liu, Z.; Zhu, W.; Zeng, H. Nonvolatile ferroelectric memory
                                                                                          (69) Srivastava, T.; Schott, M.; Juge, R.;
                     -In2Se3. Adv. Funct. Mater. 2019, 29, 1808606.
                                                                                      Roussigné, Y.; Bern-Mantel, A.; Ranno, L.; Pizzini, S.; Chérif, S.-M.; Stash-
    (53) Li, Y.; Chen, C.; Li, W.; Mao, X.; Liu, H.; Xiang, J.; Nie, A.; Liu, Z.;
                                                                                      kevich, A.; Auffret, S.; Boulle, O.; Gaudin, G.; Chshiev, M.; Baraduc, C.; Béa,
Zhu, W.; Zeng, H. Orthogonal electric control of the out-of-plane field-effect
                                                                                      H. Large-Voltage Tuning of Dzyaloshinskii–Moriya Interactions: A Route
                       -In2Se3. Adv. Electron. Mater. 2020, 6, 2000061.
                                                                                      toward Dynamic Control of Skyrmion Chirality. Nano Lett. 2018, 18, 4871–
                                                                                      4877.




                                                                                                                                                                      7

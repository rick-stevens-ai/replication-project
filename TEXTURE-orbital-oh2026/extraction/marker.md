# oh2026 — "p-wave orbital angular momentum texture in a chiral crystal"
# Oh, Pacella, Luo, ... Di Sante, Comin — arXiv:2605.15544v1 (2026)

> **PROVENANCE / EXTRACTION NOTE (read first)**
> - The real **`marker`** binary (`marker_single`) is **NOT installed** on this host.
> - This file is the **documented interim fallback**: `pdftotext -layout` output, lightly
>   normalized into the prose artifact role (section flow + captions).
> - **Equation rendering is degraded**: Unicode math (⃗L, subscripts, k-vectors, Greek) is
>   mangled by pdftotext — a known limitation. Do NOT trust math glyphs here.
> - **Authoritative equation transcriptions live in `report/REPORT.tex` and `extraction/nougat.mmd`.**
> - Regenerate with the real tool once available:
>   `marker_single textures-orbital-oh2026.pdf extraction/ --output_format markdown`
>
> Role split: **marker.md = human-readable PROSE**; **nougat.mmd = machine-readable MATH.**

---

                                                                        p-wave orbital angular momentum texture in a chiral crystal

                                                            Dongjin Oh,1, ∗ Chiara Pacella,2, 3, † Xiangyu Luo,1 Chris Jozwiak,4 Aaron Bostwick,4 Eli Rotenberg,4
                                                            Mats Leandersson,5 Craig Polley,5 Angel Rubio,3, 6, 7 Domenico Di Sante,2, ‡ and Riccardo Comin1, §
                                                                        1
                                                                         Department of Physics, Massachusetts Institute of Technology, Cambridge, MA, USA
                                                                            2
                                                                              Department of Physics and Astronomy, University of Bologna, Bologna, Italy
                                                                        3
                                                                          Max Planck Institute for the Structure and Dynamics of Matter, Hamburg, Germany
                                                                        4
                                                                          Advanced Light Source, Lawrence Berkeley National Laboratory, Berkeley, CA, USA
                                                                                        5
                                                                                          Max IV Laboratory, Lund University, Lund, Sweden
                                                                                6
                                                                                  Nano-Bio Spectroscopy Group, Departmento de Física de Materiales,
                                                                                          Universidad del País Vasco, San Sebastián, Spain
arXiv:2605.15544v1 [cond-mat.mtrl-sci] 15 May 2026




                                                                     7
                                                                       Center for Computational Quantum Physics, The Flatiron Institute, New York, NY, USA
                                                                     The spin and orbital angular momentum (SAM and OAM) are conceptually analogous, yet their
                                                                  roles in condensed matter systems have not been often treated on equal footing. While SAM has
                                                                  been extensively explored, OAM has long been regarded as quenched in crystalline environments and
                                                                  thus largely overlooked. Recent experimental and theoretical advances, however, have demonstrated
                                                                  that OAM can drive a variety of novel electronic phenomena, highlighting the importance of probing
                                                                  OAM textures in the electronic band structure. Here, we investigate the momentum-space OAM
                                                                  texture of (TaSe4 )2 I, a one-dimensional chiral crystal. Using circular-dichroism angle-resolved pho-
                                                                  toemission spectroscopy (CD-ARPES), we uncover a p-wave OAM texture accompanied by OAM
                                                                  dipole structures. This orbital p-wave texture is intimately connected to, and thus controllable
                                                                  by, the chirality of the host lattice. Complementary spin-resolved ARPES measurements and first-
                                                                  principles calculations reveal that the OAM polarization overwhelmingly dominates the low-energy
                                                                  electronic properties of (TaSe4 )2 I, far exceeding the SAM polarization. These observations repre-
                                                                  sent the experimental verification of a new type of OAM texture in crystalline materials. Most
                                                                  importantly, these findings underscore a promising material platform for spinless orbitronics appli-
                                                                  cations and lay the foundation for realizing multipolar OAM textures−orbital counterparts of the
                                                                  spin textures in unconventional magnets.


                                                                      I.    INTRODUCTION                               advances have revealed mechanisms that can generate
                                                                                                                       OAM in electronic states, both dynamically and stati-
                                                        The spin angular momentum (SAM, S)        ⃗ and orbital        cally, challenging this long-held view [5–12].
                                                                                     ⃗
                                                     angular momentum (OAM, L) of the electron share a                    Driven by the growing interest in OAM in crystalline
                                                     close conceptual analogy [1]. The SAM, a fundamen-                systems, various forms of momentum space (⃗k-space)
                                                     tal quantum property of the electron, gives rise to a             OAM textures have recently been explored. Representa-
                                                     spin magnetic moment described by the relation m      ⃗s =        tive examples include the Rashba-type surface states in
                                                           ⃗
                                                     −egS S/2me , where e is the elementary charge, gS (≈              the two-dimensional electron gas systems and the topo-
                                                     2) is the spin g-factor, and me is the electron rest mass         logically protected surface states of topological insula-
                                                     [Fig. 1(a)]. Similarly, an electron can exhibit OAM when          tors, both of which host helical OAM textures and the
                                                     it physically rotates in real space [Fig. 1(b)]. This cir-        associated orbital Edelstein effect [Fig. 1(c)] [6, 10, 13–
                                                     cular motion of electron generates orbital magnetic mo-           15]. In addition, theoretical predictions have suggested
                                                     ment given by m                ⃗
                                                                      ⃗ L = −egL L/2m     e , where gL (= 1) is
                                                                                                                       the emergence of radial OAM textures in elemental sele-
                                                     an orbital g-factor. It is important to note that both            nium crystals [Fig. 1(d)] [16]. Such OAM textures defined
                                                     the SAM and OAM contribute to the net magnetiza-                  in two-dimensional ⃗k-space have further been extended
                                                     tion of materials [1–3]. Despite these similarities, spin-        into three-dimensions, giving rise to OAM vortex lines
                                                     based functionalities−such as information processing us-          [Fig. 1(e)] [17] and OAM monopoles [Fig. 1(f)] [18, 19].
                                                     ing SAM, commonly referred to as spintronics−have seen            Thus, the discovery of novel ⃗k-space OAM textures is
                                                     remarkable progress, whereas OAM has only recently be-            promoting the advancement of OAM physics and may
                                                     gun to attract attention for its significance. This discrep-      open the door for device applications that leverage the
                                                     ancy largely stems from the long-standing assumption              orbital degree of freedom, a paradigm often referred to
                                                     that OAM is quenched by the crystal field in crystalline          as orbitronics.
                                                     solids [4]. However, recent theoretical and experimental             It is worth noting that these ⃗k-space OAM textures
                                                                                                                       closely mirror their SAM counterparts. For example, the
                                                                                                                       helical OAM texture exhibiting orbital-momentum lock-
                                                     ∗ Corresponding Author: djeeoh@gmail.com                          ing is analogous to the spin-momentum locking with he-
                                                     † Corresponding Author: chiara.pacella2@unibo.it                  lical SAM texture, while the radial OAM texture finds
                                                     ‡ Corresponding Author: domenico.disante@unibo.it                 its analogue in the radial SAM texture [14, 16, 20, 21].
                                                     § Corresponding Author: rcomin@mit.edu
                                                                                                                       Such a one-to-one correspondence between ⃗k-space OAM
                                                                                                                           2




FIG. 1.    ⃗k-space SAM and OAM textures in solids. (a,b) Illustrations of SAM (a) and OAM (b) of an electron (yellow
spheres). Blue and red arrows represent angular momenta (S ⃗ and L)
                                                                 ⃗ and their corresponding magnetic moments (m
                                                                                                             ⃗ s and m ⃗ L ),
                            ⃗
respectively. (c-f) Various k-space OAM textures: helical OAM texture (c); radial OAM texture (d); OAM vortex line (e); and
OAM monopole (f). (g-j) ⃗k-dependent SAM textures in magnets with multipolar symmetry form factors: s- (g); p- (h); d - (i);
and g-wave SAM textures (j). Blue and red colors denote spin-up and spin-down polarizations, respectively.


and SAM textures naturally raises the outstanding ques-          tial as an ideal platform for spinless orbitronics applica-
tion: can OAM textures with multipolar symmetry form             tions. Furthermore, our work provides a pathway toward
factors−analogous to the pairing symmetry form factors           realizing pure OAM phenomena with minimal SAM con-
in superconductors and to the ⃗k-dependent SAM tex-              tributions, while also laying the fundamental groundwork
tures recently realized in unconventional magnets−also           for realizing multipolar OAM textures, orbital counter-
exist? [22–30]. In this context, exploring OAM tex-              parts of spin textures with higher-order form factors in
tures that mimic the experimentally verified d - and g-          unconventional magnets [22–25, 27, 28, 30].
wave SAM textures observed in altermagnets [Fig. 1(i)
and 1(j)] [24, 27] as well as the p-wave SAM textures of
certain noncollinear magnets [Fig. 1(h)] [29], is an im-                     II.   CD-ARPES ON (TaSe4 )2 I
portant frontier and an exciting challenge for advancing
OAM physics.
                                                                   Figure 2(a) illustrates the crystal structure of
   Here, we report on the ⃗k-space imaging of a p-wave           (TaSe4 )2 I, which features a highly anisotropic 1D chain
OAM texture in the 1D chiral crystal (TaSe4 )2 I. Us-            composed of Ta and Se atoms aligned along the x -axis.
ing circular dichroism angle-resolved photoemission spec-        Notably, the Se atoms form a helical structure that
troscopy (CD-ARPES), we directly visualize the dipo-             wraps around the central 1D Ta chain, as illustrated in
lar ⃗k-space OAM texture, which displays a characteris-          Figs. 2(a) and 2(b). The room temperature metallic elec-
tic p-wave symmetry form factor. We further find that            tronic structure of (TaSe4 )2 I in the low energy range,
the polarity of the odd-parity OAM pattern reverses be-          characterized by linear band crossings, contains contri-
tween two distinct enantiomers (two mirror counterparts          butions from both Se 4p and Ta 5d orbital characters
for chiral objects) of (TaSe4 )2 I, as expected on symme-        (see Fig. S1 in Supplemental Material) [31].
try grounds. This finding indicates that the p-wave OAM            To experimentally probe the OAM texture in this
texture is controllable via structural chirality. Comple-        system, we carried out CD-ARPES experiments on
mentary spin-resolved ARPES (SARPES) measurements                (TaSe4 )2 I single crystals. Recent experimental and
reveal negligible ⃗k-space spin splitting in (TaSe4 )2 I, con-   theoretical advancements have established that CD-
sistent with first-principles calculations. These results        ARPES−defined as the difference in ARPES intensity
strongly suggest that OAM dominates the low-energy               obtained using right- and left-circularly polarized (RCP
electronic properties of (TaSe4 )2 I, underscoring its poten-    and LCP) light, IRCP (k)−ILCP (k)−can effectively probe
                                                                                                                              3




FIG. 2. CD-ARPES of (TaSe4 )2 I. (a) 1D chiral chain structure composed of Se (red and yellow spheres) and Ta (blue sphere)
atoms. (b) x -axis view of the crystal structure of (TaSe4 )2 I. Transparency of the sphere reflects the atomic height along x -
direction. (c) Experimental geometry of CD-ARPES. (d,e) Constant energy contour maps of enantiomer A (d) and enantiomer B
(e) obtained at E = −0.25 eV with 75 eV photon energy. The left and right panels of (d) and (e) show polarization-integrated
and CD photoelectron intensities, respectively. The green dashed lines indicate the plane of incidence of the experimental
geometry. (f-m) CD-ARPES spectra of enantiomer A (f-i) and enantiomer B (j-m), extracted along the dashed lines marked in
(d) and (e). The green arrows denote the node where the CD signal changes sign.


momentum-space OAM textures [6, 13, 15, 17, 32–35].               crystallographic axes relative to the experimental geom-
This technique is sensitive to OAM components aligned             etry is essential to isolate intrinsic OAM contributions
parallel to the direction of light propagation [17, 36]. Ac-      in the CD-ARPES signal. To this end, we precisely ori-
cordingly, when the incident light impinges obliquely on          ented the chain axis of (TaSe4 )2 I along the x -axis of the
the sample surface within the plane of incidence [cor-            experimental geometry, as depicted in Fig. 2(c), to fa-
responding to the xz -plane in Fig. 2(c)], it enables de-         cilitate detection of the Lx component which is oriented
tection of both x - and z -components of the OAM (Lx              parallel to the chain direction. This contrasts with pre-
and Lz ). Therefore, proper alignment of the sample’s             vious CD-ARPES studies on (TaSe4 )2 I, where the chain
                                                                                                                              4

axis was aligned perpendicular to the plane of incidence          in the −kx and +kx regions possess OAM components
[37, 38]. Additionally, in line with standard CD-ARPES            oriented in opposite directions, but also that the polarity
methodology, the experimental geometry was carefully              of the OAM texture can be controlled through structural
configured such that the surface normal of the cleaved            chirality.
crystal lay within the plane of incidence [39, 40]. Note             Not only for the sign reversal of CD between enan-
that all ARPES measurements were conducted at room                tiomers A and B, a global inversion of the overall momen-
temperature (300 K) to avoid the complex lattice distor-          tum distribution of the CD is also observed. Comparing
tions associated with the charge density wave transition          the CD-ARPES spectra of enantiomers A and B at ky =
of (TaSe4 )2 I (TCDW ∼ 275 K), allowing us to focus on            +0.25 Å−1 [Figs. 2(g) and 2(k)], the CD node indicated
the intrinsic properties stemming from its pristine chiral        by green arrows, where the sign of the CD signal reverses,
structure.                                                        appears at kx = −0.2 Å−1 , E = −0.6 eV for enantiomer
   Figure 2(d) and 2(e) show the measured constant en-            A, whereas it shifts to kx = +0.2 Å−1 for enantiomer B at
ergy contours at E = −0.25 eV near the first Brillouin            the same energy. A similar inversion of the CD-ARPES
zone for the A and B enantiomers of (TaSe4 )2 I, obtained         spectra is also observed at ky = −0.25 Å−1 [Figs. 2(h)
using 75 eV photon energy. As shown in the polarization-          and 2(i)]. This behavior originates from the fact that
integrated ARPES spectra [IRCP + ILCP , in the left               enantiomers A and B are mirror counterparts of each
panels of the Fig. 2(d) and 2(e)], (TaSe4 )2 I displays a         other [see Fig. S3 in Supplemental Material] [31]. As
strongly anisotropic electronic band structure character-         structural mirror images, their CD-ARPES spectra are
ized by open Fermi contours, highlighting the 1D na-              correspondingly related through mirror symmetry. Ap-
ture of its low-energy electronic states, in agreement with       plying a mirror operation along the x-direction (Mx ) to
previous ARPES studies [38, 41, 42]. It is worth not-             the CD-ARPES spectrum in Fig. 2(g) (the +ky region)
ing that the polarization-integrated maps of enantiomers          reverses the sign of kx while leaving the sign of Lx and ky
A and B exhibit distinct spectral intensity distributions.        unchanged, since ⃗k is a polar vector and L ⃗ is an axial vec-
While both enantiomers display stronger intensity in the          tor [43]. This transformation reproduces the CD-ARPES
band at negative kx , enantiomer A shows enhanced in-             spectrum shown in Fig. 2k [see Fig. S3(b) in Supplemen-
tensity in the negative kx and ky region [third quadrant          tal Material] [31]. The same mirror symmetry relation-
in Fig. 2(d)], whereas enantiomer B exhibits stronger in-         ship holds between Figs. 2(h) and 2(l). Furthermore, ap-
tensity in the negative kx and positive ky region [second         plying a mirror operation along the y-direction (My ) to
quadrant in Fig. 2(e)]. These enantiomer-specific fea-            the CD-ARPES data in Figs. 2(g) and 2(h) leaves kx un-
tures in the photoelectron maps highlight the chirality-          changed but reverses the signs of ky and Lx , thereby re-
dependent electronic properties of (TaSe4 )2 I. We note           producing Figs. 2(l) and 2(k), respectively [see Fig. S3(c)
that two bands forming the linear crossing are not well re-       in Supplemental Material] [31].
solved in the constant energy contour data at E = −0.25              We note that, although the Lz component can in prin-
eV, but they become clearly distinguishable at higher             ciple contribute to the CD-ARPES spectra under our ex-
binding energies [see Fig. S2 in Supplemental Material]           perimental geometry, the symmetry relations discussed
[31]. However, the spectral weight of the outer bands             above indicate that its contribution to the observed CD-
is significantly suppressed due to matrix-element effects.        ARPES spectra is negligible. When the OAM aligns
Therefore, the spectral weight observed in Figs. 2(d)             along the z-direction, it undergoes a sign reversal un-
and 2(e) is dominated by the inner bands.                         der both Mx and My , in contrast to Lx [see Fig. S4
   A particularly intriguing feature was observed in the          in Supplemental Material] [31]. Consequently, the sign
constant energy contours obtained from the CD-ARPES               of Lz would remain unchanged under Mx , which is in-
measurements. The CD maps [right panels of the                    compatible with the observation that Figs. 2(g) and 2(k)
Figs. 2(d) and 2(e)], which are likewise predominantly            [and likewise Figs. 2(h) and 2(l)] are related as Mx mirror
contributed by the CD signal of the inner bands, clearly          counterparts. Together, these symmetry characteristics
show that enantiomers A and B exhibit opposite odd-               demonstrate that the observed CD-ARPES spectra pre-
parity CD signals, reflecting their distinct structural chi-      dominantly reflect Lx , and that these unique CD-ARPES
rality. As further illustrated in Fig. 2(f)-(i), the electronic   features in (TaSe4)2 I arise directly from its structural chi-
band of enantiomer A exhibits negative CD (marked with            rality.
the red color scale) in the negative kx region at low en-            It is worth emphasizing that the observed CD-ARPES
ergies (E − EF ≥ −0.8 eV), largely independent of ky .            signals are unlikely to arise from extrinsic geometrical
In contrast, the band in the positive kx region within            effects [34, 40, 44], which are commonly known to in-
the same energy window displays positive CD [Figs. 2(f)-          fluence CD-ARPES measurements. This conclusion is
(i)]. On the other hand, odd-parity CD for enantiomer             supported by several key observations. First, in the low-
B shows the opposite behavior, with positive CD in the            energy region within the first Brillouin zone (|kx | < 0.5
−kx region and negative CD in the +kx region [Figs. 2(j)-         Å−1 ), the CD signal shows little to no sign reversal across
(m)], confirming the enantiomer-dependent CD response.            the ky axis (which is perpendicular to the plane of inci-
Based on these CD-ARPES experiemtns, we can experi-               dence in our experimental geometry), a behavior incon-
mentally infer not only that the low-energy bands located         sistent with extrinsic geometrical CD. When the plane
                                                                                                                           5




FIG. 3. p-wave OAM texture in (TaSe4 )2 I. (a,b) x -component of OAM (Lx ) textures in the energy-momentum dispersion
of enantiomer A (a), and B (b), extracted at ky = 0 Å−1 . Left and right panels in (a) and (b) show results without and
with SOC, respectively. (c,d) Lx textures of enantiomer A (c) and B (d) in the kx -ky plane. Left and right panels illustrate
constant energy contours at E − EF = 0 eV and −0.25 eV, respectively. (e) Schematic illustration of ⃗k-space OAM texture.
Green solid curves represent the electronic bands of (TaSe4 )2 I in kx -ky plane. Red and blue arrows indicate negative and
positive Lx , respectively. The momentum spacing between the inner and outer bands is exaggerated for clarity. (f) Real-space
Wannier function corresponding to the low-energy electronic states. Blue and yellow spheres correspond to Ta and Se atoms,
respectively. Cyan and yellow iso-surfaces represent positive and negative values of the Wannier funtion, respectively.


of incidence is aligned with the xz -plane, obliquely inci-     ky = 0 Å−1 , and is independent of the material’s intrinsic
dent circularly polarized light inherently breaks the hor-      electronic properties. However, contrary to this notion,
izontal mirror symmetry (My ) with respect to the xz -          enantiomers A and B of (TaSe4 )2 I show no sign reversal
plane. As a result, if the surface normal of the sample lies    of the CD signal across ky = 0 Å−1 in either the positive
within the plane of incidence, the ARPES spectra taken          or negative kx regions, as evident in Figs. 2(d)-(m). This
along the ky direction generally become asymmetric with         strongly suggests that the CD signals in these momentum
respect to ky = 0 Å−1 for both RCP and LCP light,               and energy ranges are governed primarily by intrinsic CD
yielding IRCP (kx , +ky ) ̸= IRCP (kx , −ky ) [see Fig. S5 in   contributions, rather than extrinsic effects. Secondly, the
Supplemental Material] [31]. Moreover, since RCP and            observed odd-parity CD-ARPES spectra is reversible be-
LCP light are mirror counterparts under My , the relation       tween the two enantiomers, whereas the extrinsic geo-
IRCP (kx , ±ky ) = ILCP (kx , ∓ky ) holds. This leads to an     metrical CD is enantiomer-independent. The CD signals
extrinsic geometrical CD signal that is, by symmetry, an        exhibiting sign reversal across ky = 0 Å−1 , a hallmark of
odd function with respect to ky = 0 plane, typically pro-       extrinsic geometrical effects, appear only at higher bind-
ducing a horizontal node where the CD signal vanishes at        ing energies and far from the Brillouin zone center [see
                                                                                                                          6

Fig. S6 in Supplemental Material] [31]. Crucially, these       outer (larger kx ) bands share the same sign of Lx . In
features are present in both enantiomers and are inde-         contrast, the bands at negative kx exhibit the opposite
pendent of their structural chirality, further confirming      sign of Lx , demonstrating a dipolar OAM texture with
their extrinsic origin. Taken together, these observations     p-wave symmetry form factor. Near the Brillouin zone
collectively support the conclusion that the enantiomer-       boundary, the OAM undergoes a sign reversal, in rea-
dependent odd-parity CD-ARPES data present in Fig. 2           sonable agreement with the CD-ARPES measurements
faithfully reflects intrinsic CD contributions arising from    [see Fig. S5 in Supplemental Material] [31]. This p-wave
inherent electronic states intertwined with the chiral lat-    OAM texture becomes even more pronounced at higher
tice structure of (TaSe4 )2 I. We also note that while ex-     binding energy (E − EF = −0.25 eV), as shown in the
trinsic geometrical CD contributions are negligible in the     right panel of Fig. 3(c). The polarity inversion of the
low-energy spectra measured using 75 eV photon energy,         p-wave OAM texture in enantiomer B is also more dis-
they become more pronounced at higher photon energies          tinctly captured at this binding energy [Fig. 3(d)]. To
[see Fig. S7 in Supplemental Material] [31]. In addi-          obtain a complete picture, we thoroughly examine the
tion, photon energy-dependent CD sign reversals, com-          full OAM texture of (TaSe4 )2 I by further evaluating the
monly observed in CD-ARPES, are also detected. The             Ly and Lz components, as illustrated in Fig. 3(e) [see
photon energy dependence in CD-ARPES spectra may               Fig. S10 Supplementary] [31]. Although the low-energy
originate from final-state effect and inter-atomic interfer-   band structure of (TaSe4 )2 I contains a weak Ly compo-
ence [19, 34, 44, 45]. We further note that the observed       nent (while Lz remains absent), the overall OAM struc-
odd-parity momentum distribution of the CD can be at-          ture still predominantly exhibits a p-wave symmetry form
tributed to the OAM character of the initial electronic        factor [Fig. 1(h)]. These first-principles calculations are
states, rather than to optical activity effects [see Supple-   in good agreement with the CD patterns observed in the
mentary Section SVII] [31]. Therefore, we conclude that        low-energy ARPES spectra (Fig. 2), reinforcing the iden-
the measured CD-ARPES spectra are a direct manifes-            tification of a p-wave OAM texture in (TaSe4 )2 I.
tation of the OAM texture of the initial electronic states        It is important to emphasize that the characteristic
of (TaSe4 )2 I.                                                p-wave OAM texture observed in (TaSe4 )2 I is distinct
                                                               from the texture obtained by transforming a radial OAM
                                                               texture−defined on a closed Fermi contour−to the 1D
   III.   p-WAVE OAM TEXTURE IN (TaSe4 )2 I                    limit where the contour becomes open [see Fig. S11 in
                                                               Supplemental Material] [31]. For example, in the simple
   To obtain deeper insight into the observed angular dis-     radial OAM case, the OAM vectors in the +kx and +ky
tribution of the CD signal in the low-energy regime, we        regions (the first quadrant in kx -ky plane) have the same
performed first-principles calculations to evaluate the or-    signs for Lx and Ly . In contrast, in (TaSe4 )2 I, the OAM
bital degree of freedom in (TaSe4 )2 I. Fig. 3(a) presents     vectors in the same ⃗k region exhibit opposite signs for
the calculated energy-momentum dispersion of enan-             Lx and Ly [see Fig. S10 in Supplemental Material] [31].
tiomer A projected onto Lx . In the non-relativistic limit     Moreover, approximating the OAM texture of (TaSe4 )2 I
(without spin-orbit coupling, SOC), shown in the left          as a 1D limit of a simple radial configuration fails to ac-
panel of Fig. 3(a), enantiomer A exhibits linearly dis-        count for the sign reversal observed along its constant
persing low-energy bands with +Lx in the +kx region,           energy contours [Fig. 3(c) and 3(d)]. Therefore, these
while the sign of Lx reverses in the −kx region, demon-        observations indicate that the p-wave OAM texture can
strating an odd-parity Lx texture. Interestingly, even         be regarded as an inherent multipolar OAM characteris-
in the relativistic limit with SOC, the low-energy bands       tic of (TaSe4 )2 I.
exhibit a small energy splitting (< 5 meV), and both              To shed light onto the microscopic origin of the fi-
split branches retain the same sign of Lx [right panel of      nite OAM, we analyze the linearly dispersing low-energy
Fig. 3(a)]. This result indicates that the low-energy OAM      bands within the framework of a minimal tight-binding
textures are almost identical in the non-relativistic and      model [see Fig. S1 in Supplemental Material] [31].
relativistic limits of (TaSe4 )2 I. Moreover, enantiomer B     Specifically, we project the first-principles electronic
hosts an OAM texture with the opposite sign of Lx com-         band structure onto a set of maximally localized Wannier
pared to that of enantiomer A, as shown in Fig. 3(b).          functions derived from Ta-dx2 orbitals, i.e., the conven-
Notably, the ⃗k-dependent OAM texture at ky = 0 Å−1            tional dz2 orbitals aligned along the x-direction of the chi-
consists solely of the Lx component, while the perpen-         ral chains. As shown in Fig. 3(f), the resulting Wannier
dicular components Ly and Lz are absent [see Fig. S9 in        functions, while dominated by dx2 character, also exhibit
Supplemental Material] [31].                                   substantial p-like contributions from the Se atoms. Im-
   We further investigate the ⃗k-space OAM texture away        portantly, this p orbital character is inherited from the
from ky = 0 Å−1 . Fig. 3(c) and 3(d) display constant en-      Wannier functions in order to faithfully reproduce and
ergy contours in the kx -ky plane projected onto Lx . At       interpolate the original DFT bandstructure. This is con-
the Fermi level of enantiomer A [left panel of Fig. 3(c)],     sistent with the orbitally resolved DFT band structure in
the OAM texture for positive kx clearly shows positive         Fig. S1 of Supplemental Material, which highlights a siz-
Lx near ky = 0 Å−1 , as both the inner (smaller kx ) and       able Se contribution to the relevant bands. Consequently,
                                                                                                                                7




FIG. 4. SAM texture in (TaSe4 )2 I. (a,b) ⃗k-space SAM texture of (TaSe4 )2 I at ky = 0 Å−1 , projected onto the x -component of
SAM, Sx , (a) and y- and z -components, Sy and Sz , (b). (c) Schematic illustration of the ⃗k-space SAM texture in the low-energy
electronic states of TaSe4 )2 I. Grey planes indicate the linearly dispersing bands. Red and blue arrows correspond to positive
and negative Sx , respectively. (d-i) Spin-resolved ARPES (SARPES) spectra of (TaSe4 )2 I. (d) and (e) show spin-resolved
energy distribution curves (SEDCs) projected onto Sx , collected at ∓0.19 Å−1 , respectively. (f) and (g), as well as (h) and (i),
display the same SEDCs, but projected onto the Sy and Sz spin components, respectively. Red and blue indicate spin-up and
spin-down components, respectively, while green curves show the differences between the spin-up and spin-down channels.


because the dx2 component of the Wannier function does             mental Material] [31]. Interestingly, as discussed above,
not contribute to the local OAM, the finite Lx polariza-           the SOC-induced band splitting near the Fermi level is
tion of the bands originates from the py and pz orbitals           negligibly small, and the two split branches carry oppo-
within the plane perpendicular to the chiral chains. They          site SAM, resulting in an almost vanishing net spin po-
indeed act as orbital polarizers of the Wannier functions.         larization at the Fermi surface. Since this spin-splitting
                                                                   energy scale (< 5 meV) is far below the thermal energy at
                                                                   room temperature (∼ 25 meV), the spin split bands are
   IV.    ⃗k-SPACE SAM TEXTURE IN (TaSe4 )2 I                      thermally activated, implying that the SAM contribu-
                                                                   tion to the low-energy electronic properties of (TaSe4 )2 I
   We further examine the ⃗k-space SAM texture in the              is negligible at room temperature. Accordingly, the ef-
electronic structure of (TaSe4 )2 I, given that electronic         fective ⃗k-space SAM texture can be represented as shown
bands hosting OAM textures typically acquire concomi-              in Fig. 4(c). Notably, while the spin-split bands possess
tant SAM through SOC. As shown in Figs. 4(a) and 4(b),             opposite SAM signs, they retain the same sign of OAM
the calculated spin textures exhibit a finite Sx compo-            (Fig. 3), indicating that only OAM polarization persists
nent, mirroring the behavior observed in the OAM sec-              at the Fermi surface. These unique OAM and SAM tex-
tor, while the Sy and Sz components are absent. More-              tures suggest that L⃗ serves as the good quantum number
over, the calculated spin polarizations of enantiomer A            governing the low-energy electronic states, with SAM be-
and B display opposite signs of Sx , consistent with the           ing secondarily locked to the OAM through weak SOC
corresponding OAM textures [see Fig. S12 in Supple-                [14]. In addition, the dominant energy scale of inversion-
                                                                                                                          8

symmetry breaking in (TaSe4 )2 I, arising from its chiral        pathway to realize p-wave SAM texture driven by struc-
structure and exceeding that of SOC, is likely a key factor      tural chirality intertwined with SOC. This approach of-
in these SAM and OAM structures [7].                             fers a distinct advantage over unconventional magnets,
   The SAM textures in (TaSe4 )2 I obtained from first-          such as altermagnets, which rely on antiferromagnetic
principles calculations show reasonably good agreement           ordering, as the characteristic size of structurally chiral
with our SARPES measurements conducted at room                   domains is generally much larger than that of antifer-
temperature. As shown in Fig. 4(d) and 4(e), spin-               romagnetic domains. Harnessing structural chirality to
resolved energy distribution curves collected at kx =            engineer p-wave SAM textures thus provides a promis-
±0.19 Å−1 , where the ARPES spectral weight is most              ing route toward realizing coherent p-wave SAM textures
pronounced, exhibit no detectable Sx polarization, as            over long length scales. Such a strategy could open the
the tiny spin splitting is intrisically obscured by the lim-     door to novel emergent phenomena, including unconven-
ited energy resolution of the SARPES technique and by            tional chiral superconductivity [47].
the thermal broadening at room temperature. These re-               Studies of OAM and SAM in (TaSe4 )2 I further provide
sults are nevertheless consistent with the presence of sub-      fundamental insight into the innate electronic properties
resolution spin splitting projected onto Sx . Moreover, no       in helical chain structures. Recent studies of quantum
discernible spin polarization is observed in Sy and Sz           materials have proposed that OAM may serve as the mi-
[Figs. 4(f)- 4(i)], in line with the first-principles results    croscopic origin of spin transport phenomena such as the
[Fig. 4(b)]. The absence of measurable spin polarization         spin Hall and Rashba effects [6, 8, 32, 48]. Within this
near the Fermi level provides direct experimental evi-           broader context, our findings highlight that OAM could
dence that OAM, rather than SAM, has a leading role in           also underlie chirality-induced spin selectivity (CISS), a
the low-energy electronic properties of (TaSe4 )2 I. There-      distinctive spin transport effect in helical chain systems
fore, (TaSe4 )2 I offers a significant advantage for realizing   which shows spin current parallel to the chain direc-
spinless orbitronics applications.                               tion [49–51]. Specifically, in the absence of SOC, low-
                                                                 energy electronic states carry only OAM, while SOC
                                                                 couples SAM to OAM, generating spin splitting and en-
                   V.    DISCUSSION                              abling spin transport phenomena [see Fig. S13 in Sup-
                                                                 plemental Material] [31]. This framework allows CISS to
                                                                 be reinterpreted as a consequence of more fundamental
   Through a systematic spectroscopic study on
                                                                 effect−chirality-induced orbital selectivity (CIOS). This
(TaSe4 )2 I, we find a dipolar OAM texture characterized
                                                                 connection may also shed light on the long-standing puz-
by a p-wave symmetry form factor, with a negligible
                                                                 zle that the magnitude of CISS depends sensitively on
SAM contribution to the low-energy physics. This
                                                                 the SOC strength of the electrodes used in measurments
makes (TaSe4 )2 I a promising material platform for
                                                                 [52, 53]. Taken together, our results provide an impor-
future spinless orbitronics [9, 46]. Furthermore, we
                                                                 tant clue toward establishing a correct fundamental un-
demonstrate that the polarity of p-wave OAM texture
                                                                 derstanding of both CISS and CIOS.
is controllable through structural chirality, reminiscent
of the tunable OAM monopoles observed in 3D chiral
topological semimetal [19]. This observation can be
regarded as the orbital counterpart of p-wave SAM                                        Outlook
texture, recently realized in helimagnetic state of NiI2
[29]. From a symmetry perspective, (TaSe4 )2 I and NiI2 ,           In this work, we experimentally and theoretically re-
which exhibit p-wave OAM and SAM, respectively, share            alize and verify an OAM texture with a p-wave sym-
a profound similarity. In the former, inversion symmetry         metry form factor in a crystalline solid. Realizing such
is broken by the chiral crystal structure, whereas in            an OAM structure establishes a foundation for explor-
the latter it is broken by the chiral magnetic order. In         ing the orbital analogs of SAM texture with multipolar
addition, the polarity of p-wave OAM in (TaSe4 )2 I and          symmetry form factors in unconventional magnets [22–
p-wave SAM in NiI2 can be controlled via chirality in            25, 27, 28]. Looking forward, continued experimental and
lattice and spin degrees of freedom, respectively.               theoretical advances may enable the realization of higher-
   By noting that the p-wave OAM texture emerging from           order multipolar OAM textures, such as d -, f -, g-, and
the helical chain structure can be directly connected to a       even i -wave symmetries, extending beyond the p-wave
p-wave SAM texture in helimagnet, we further establish           regime [30]. Moreover, the direct detection of OAM-
the analogy between chiral crystal structures and chiral         related phenomena will present the next important chal-
magnetic orders [see Fig. S13 in Supplemental Mate-              lenge. Such effects should be experimentally accessible
rial] [31]. In the non-relativistic limit, the helical chain     using state-of-the-art techniques, such as ultra-sensitive
structure hosts a p-wave OAM texture. Then, when a               magneto-optical Kerr effect measurements capable of re-
sufficiently strong SOC is taken into account, it can give       solving Kerr rotation on the order of a few nanoradians
rise to pronounced p-wave SAM texture. By pinpointing            [9]. In this respect, our work provides a fundamental step
this microscopic mechanism of coupled OAM and SAM in             toward a more complete understanding of OAM-rooted
1D chiral lattice structures, our study highlights a novel       effects in quantum materials.
                                                                                                                                  9

                ACKNOWLEDGMENTS                                     that the plane of incidence include the normal vector of
                                                                    the cleaved (TaSe4 )2 I surface. The angle of incidence was
  This work was supported by the Air Force Office of                set to 54.75◦ .
Scientific Research (AFOSR) under grant FA9550-22-1-                  Spin-resolved ARPES experiments were performed at
0432. This research used resources of the Advanced Light            the Bloch beamline of MAX IV, utilizing very low en-
Source, which is a DOE Office of Science User Facility              ergy electron diffraction (VLEED) spin detectors. All
under contract no. DE-AC02-05CH11231. D.O. and C.P.                 spin-resolved ARPES data were also collected at room
contributed equally.                                                temperature.


                                                                                       3. DFT calculations
                APPENDIX: METHODS

                 1. Single crystal growth
                                                                       All theoretical calculations were carried out within
                                                                    the framework of ab initio Density functional theory
                                                                    (DFT), implemented in the FPLO (Full-Potential Local-
   Single crystals of (TaSe4 )2 I were grown using the chem-        Orbital) package [54, 55]. The exchange–correlation
ical vapor transport (CVT) method. A mixture of Ta,                 energy was treated within the generalized gradi-
Se, and I precursors was placed in a quartz tube, which             ent approximation (GGA), in the parametrization of
was then sealed under vacuum. The quartz ampule was                 Perdew–Burke–Ernzerhof 96 (PBE). Total energies were
heated in a two-zone furnace, with the cold and hot zones           converged to better than 10−8 eV, while the accuracy
maintained 400 ◦ C and 520 ◦ C, respectively. After one             for the self-consistent charge densities was set to 10−6
week, needle-like (TaSe4 )2 I single crystals, a few milime-        eV. For the cases where spin–orbit coupling (SOC) plays
ters in size, were obtained. The stoichiometry of the syn-          a role, fully relativistic calculations were performed us-
thesized crystals was confirmed using Energy-dispersive             ing the four-component Dirac formalism implemented
X-ray spectroscopy (EDX).                                           in FPLO. The Brillouin zone was sampled using a
                                                                    Monkhorst–Pack k-point mesh of 12 × 12 × 12. The re-
                                                                    laxed structural parameters were taken from the Materi-
                2. ARPES measurements                               als Project [56–58].
                                                                       In order to extract tight-binding (TB) models of the
   The CD-ARPES measurements were carried out at                    two enantiomers, their Bloch states were projected onto
Beamline 7.0.2 (MAESTRO) of the Advanced Light                      maximally localized Wannier functions using the FPLO
Source (ALS). Single crystals of (TaSe4 )2 I were mechan-           Wannier function module. The atomic orbitals chosen as
ically cleaved at room temperature in an ultra-high-                trial functions were Ta-5d, Ta-6s, Se-4p and I-5p. The
vacuum (UHV) ARPES chamber (∼4 × 10−11 torr). The                   minimal toy-model based solely on Ta-dz2 orbitals as trial
CD-ARPES data were acquired at room temperature us-                 functions was extracted through the Wannier90 package
ing a horizontal analyzer slit. Constant energy contour             [59]. The post-processing of the TB models relied on a
maps were obtained with a photoelectron deflector, with             in-house python code [60]. The Wannier functions were
precise alignment of the experimental geometry to ensure            visualized thanks to the Vesta software.




 [1] L. L. Hirst, The microscopic magnetization: concept an-             nathan, M. W. Haverkort, T. K. Kim, M. Hoesch, J. Fujii,
     dapplication, Rev. Mod. Phys. 69, 607 (1997).                       I. Vobornik, A. P. Mackenzie, and P. D. C. King, Maxi-
 [2] G. G. Scott, Review of Gyromagnetic Ratio Experiments,              mal Rashba-like spin splitting via kinetic-energy-coupled
     Rev. Mod. Phys. 34, 102 (1962).                                     inversion-symmetry breaking, Nature 549, 492 (2017).
 [3] R. A. Reck and D. L. Fry, Orbital and Spin Magnetization        [8] D. Go, D. Jo, C. Kim, and H.-W. Lee, Intrinsic Spin and
     in Fe-Co, Fe-Ni, and Ni-Co, Phys. Rev. 184, 492 (1969).             Orbital Hall Effects from Orbital Texture, Phys. Rev.
 [4] C. Kittel, Introduction to solid state physics, 8th ed. (Wi-        Lett. 121, 086602 (2018).
     ley, Hoboken, NJ, 2005).                                        [9] Y.-G. Choi, D. Jo, K.-H. Ko, D. Go, K.-H. Kim, H. G.
 [5] B. A. Bernevig, T. L. Hughes, and S.-C. Zhang, Orbitron-            Park, C. Kim, B.-C. Min, G.-M. Choi, and H.-W. Lee,
     ics: The Intrinsic Orbital Current in $p$-Doped Silicon,            Observation of the orbital Hall effect in a light metal Ti,
     Phys. Rev. Lett. 95, 066601 (2005), publisher: American             Nature 619, 52 (2023).
     Physical Society.                                              [10] S. Ding, Z. Liang, D. Go, C. Yun, M. Xue, Z. Liu,
 [6] S. R. Park, C. H. Kim, J. Yu, J. H. Han, and C. Kim,                S. Becker, W. Yang, H. Du, C. Wang, Y. Yang, G. Jakob,
     Orbital-Angular-Momentum Based Origin of Rashba-                    M. Kläui, Y. Mokrousov, and J. Yang, Observation of the
     Type Surface Band Splitting, Phys. Rev. Lett. 107,                  Orbital Rashba-Edelstein Magnetoresistance, Phys. Rev.
     156803 (2011).                                                      Lett. 128, 067201 (2022).
 [7] V. Sunko, H. Rosner, P. Kushwaha, S. Khim, F. Maz-             [11] A. El Hamdi, J.-Y. Chauleau, M. Boselli, C. Thibault,
     zola, L. Bawden, O. J. Clark, J. M. Riley, D. Kasi-                 C. Gorini, A. Smogunov, C. Barreteau, S. Gariglio, J.-M.
                                                                                                                               10

     Triscone, and M. Viret, Observation of the orbital inverse        Symmetry, Phys. Rev. X 12, 031042 (2022).
     Rashba–Edelstein effect, Nat. Phys. 19, 1855 (2023).         [23] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging Re-
[12] R. Burgos Atencia, A. , Amit, , and D. Culcer, Orbital            search Landscape of Altermagnetism, Phys. Rev. X 12,
     angular momentum of Bloch electrons: equilibrium for-             040501 (2022).
     mulation, magneto-electric phenomena, and the orbital        [24] J. Krempaský, L. Šmejkal, S. W. D’Souza, M. Ha-
     Hall effect, Adv. Phys.: X 9, 2371972 (2024).                     jlaoui, G. Springholz, K. Uhlířová, F. Alarab, P. C.
[13] S. R. Park, J. Han, C. Kim, Y. Y. Koh, C. Kim, H. Lee,            Constantinou, V. Strocov, D. Usanov, W. R. Pudelko,
     H. J. Choi, J. H. Han, K. D. Lee, N. J. Hur, M. Arita,            R. González-Hernández, A. Birk Hellenes, Z. Jansa,
     K. Shimada, H. Namatame, and M. Taniguchi, Chi-                   H. Reichlová, Z. Šobáň, R. D. Gonzalez Betancourt,
     ral Orbital-Angular Momentum in the Surface States of             P. Wadley, J. Sinova, D. Kriegner, J. Minár, J. H. Dil,
     Bi2 Se3 , Phys. Rev. Lett. 108, 046805 (2012).                    and T. Jungwirth, Altermagnetic lifting of Kramers spin
[14] B. Kim, P. Kim, W. Jung, Y. Kim, Y. Koh, W. Kyung,                degeneracy, Nature 626, 517 (2024).
     J. Park, M. Matsunami, S.-i. Kimura, J. S. Kim, J. H.        [25] S. Lee, S. Lee, S. Jung, J. Jung, D. Kim, Y. Lee, B. Seok,
     Han, and C. Kim, Microscopic mechanism for asymmet-               J. Kim, B. G. Park, L. Šmejkal, C.-J. Kang, and C. Kim,
     ric charge distribution in Rashba-type surface states and         Broken Kramers Degeneracy in Altermagnetic MnTe,
     the origin of the energy splitting scale, Phys. Rev. B 88,        Phys. Rev. Lett. 132, 036702 (2024).
     205408 (2013).                                               [26] Y.-P. Zhu, X. Chen, X.-R. Liu, Y. Liu, P. Liu, H. Zha,
[15] M. Ünzelmann, H. Bentmann, P. Eck, T. Kißlinger,                  G. Qu, C. Hong, J. Li, Z. Jiang, X.-M. Ma, Y.-J. Hao,
     B. Geldiyev, J. Rieger, S. Moser, R. C. Vidal, K. Kißner,         M.-Y. Zhu, W. Liu, M. Zeng, S. Jayaram, M. Lenger,
     L. Hammer, M. A. Schneider, T. Fauster, G. Sangiovanni,           J. Ding, S. Mo, K. Tanaka, M. Arita, Z. Liu, M. Ye,
     D. Di Sante, and F. Reinert, Orbital-Driven Rashba Ef-            D. Shen, J. Wrachtrup, Y. Huang, R.-H. He, S. Qiao,
     fect in a Binary Honeycomb Monolayer AgTe, Phys. Rev.             Q. Liu, and C. Liu, Observation of plaid-like spin split-
     Lett. 124, 176401 (2020).                                         ting in a noncoplanar antiferromagnet, Nature 626, 523
[16] B. Kim, D. Shin, S. Namgung, N. Park, K.-W. Kim, and              (2024).
     J. Kim, Optoelectronic Manifestation of Orbital Angu-        [27] B. Jiang, M. Hu, J. Bai, Z. Song, C. Mu, G. Qu, W. Li,
     lar Momentum Driven by Chiral Hopping in Helical Se               W. Zhu, H. Pi, Z. Wei, Y.-J. Sun, Y. Huang, X. Zheng,
     Chains, ACS Nano 17, 18873 (2023).                                Y. Peng, L. He, S. Li, J. Luo, Z. Li, G. Chen, H. Li,
[17] T. Figgemeier, M. Ünzelmann, P. Eck, J. Schusser,                 H. Weng, and T. Qian, A metallic room-temperature d-
     L. Crippa, J. Neu, B. Geldiyev, P. Kagerer, J. Buck,              wave altermagnet, Nat. Phys. 21, 754 (2025).
     M. Kalläne, M. Hoesch, K. Rossnagel, T. Siegrist, L.-K.      [28] C. Song, H. Bai, Z. Zhou, L. Han, H. Reichlova, J. H. Dil,
     Lim, R. Moessner, G. Sangiovanni, D. Di Sante, F. Rein-           J. Liu, X. Chen, and F. Pan, Altermagnets as a new class
     ert, and H. Bentmann, Imaging Orbital Vortex Lines in             of functional materials, Nat Rev Mater 10, 473 (2025).
     Three-Dimensional Momentum Space, Phys. Rev. X 15,           [29] Q. Song, S. Stavrić, P. Barone, A. Droghetti, D. S. An-
     011032 (2025).                                                    tonenko, J. W. F. Venderbos, C. A. Occhialini, B. Ilyas,
[18] Q. Yang, J. Xiao, I. Robredo, M. G. Vergniory, B. Yan,            E. Ergeçen, N. Gedik, S.-W. Cheong, R. M. Fernandes,
     and C. Felser, Monopole-like orbital-momentum lock-               S. Picozzi, and R. Comin, Electrical switching of a p-wave
     ing and the induced orbital transport in topological              magnet, Nature 642, 64 (2025).
     chiral semimetals, Proc. Natl. Acad. Sci. U.S.A. 120,        [30] M. Ezawa, Third-order and fifth-order nonlinear spin-
     e2305541120 (2023).                                               current generation in g-wave and i-wave altermagnets and
[19] Y. Yen, J. A. Krieger, M. Yao, I. Robredo, K. Manna,              perfectly nonreciprocal spin current in f-wave magnets,
     Q. Yang, E. C. McFarlane, C. Shekhar, H. Borrmann,                Phys. Rev. B 111, 125420 (2025).
     S. Stolz, R. Widmer, O. Gröning, V. N. Strocov, S. S. P.     [31] See Supplemental Material at [URL will be inserted by
     Parkin, C. Felser, M. G. Vergniory, M. Schüler, and               publisher] for additional information on orbital char-
     N. B. M. Schröter, Controllable orbital angular momen-            acters of low-energy electronic structure of (TaSe4 )2 I,
     tum monopoles in chiral topological semimetals, Nat.              constant energy contours of (TaSe4 )2 I at E = −0.45
     Phys. , 1 (2024).                                                 eV, mirror-symmetry effects on crystal momentum and
[20] M. Sakano, M. Hirayama, T. Takahashi, S. Akebi,                   orbital angular momentum, extrinsic geometrical effect
     M. Nakayama, K. Kuroda, K. Taguchi, T. Yoshikawa,                 in CD-ARPES, circular-dichroism of constant energy
     K. Miyamoto, T. Okuda, K. Ono, H. Kumigashira,                    contours at vraious binding energies, photon energy-
     T. Ideue, Y. Iwasa, N. Mitsuishi, K. Ishizaka, S. Shin,           dependent CD-ARPES spectra of the A enantiomer
     T. Miyake, S. Murakami, T. Sasagawa, and T. Kondo,                (TaSe4 )2 I, the connection between CD-ARPES spectra
     Radial Spin Texture in Elemental Tellurium with Chiral            and OAM, detailed OAM texture of (TaSe4 )2 I, radial
     Crystal Structure, Phys. Rev. Lett. 124, 136404 (2020).           OAM texture with open Fermi contour in 1D limit,
[21] G. Gatti, D. Gosálbez-Martínez, S. Tsirkin, M. Fanciulli,         enantiomer-dependent SAM textures of (TaSe4 )2 I, p-
     M. Puppin, S. Polishchuk, S. Moser, L. Testa, E. Mar-             wave SAM texture in spin helix and helical lattice, and
     tino, S. Roth, P. Bugnon, L. Moreschini, A. Bostwick,             the role of spin-orbit coupling in (TaSe4 )2 I. The Supple-
     C. Jozwiak, E. Rotenberg, G. Di Santo, L. Petaccia,               mental Material includes Refs. [7, 14, 36].
     I. Vobornik, J. Fujii, J. Wong, D. Jariwala, H. Atwa-        [32] J.-H. Park, C. H. Kim, J.-W. Rhim, and J. H. Han, Or-
     ter, H. Rønnow, M. Chergui, O. Yazyev, M. Grioni, and             bital Rashba effect and its detection by circular dichroism
     A. Crepaldi, Radial Spin Texture of the Weyl Fermions in          angle-resolved photoemission spectroscopy, Phys. Rev. B
     Chiral Tellurium, Phys. Rev. Lett. 125, 216402 (2020).            85, 195401 (2012).
[22] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond Con-         [33] M. Ünzelmann, H. Bentmann, T. Figgemeier, P. Eck,
     ventional Ferromagnetism and Antiferromagnetism: A                J. N. Neu, B. Geldiyev, F. Diekmann, S. Rohlf, J. Buck,
     Phase with Nonrelativistic Spin and Crystal Rotation              M. Hoesch, M. Kalläne, K. Rossnagel, R. Thomale,
                                                                                                                             11

     T. Siegrist, G. Sangiovanni, D. D. Sante, and F. Rein-           from a topological insulator, Phys. Rev. Res. 7, 033027
     ert, Momentum-space signatures of Berry flux monopoles           (2025).
     in the Weyl semimetal TaAs, Nat. Commun. 12, 3650           [46] D. Jo, D. Go, and H.-W. Lee, Gigantic intrinsic orbital
     (2021).                                                          Hall effects in weakly spin-orbit coupled metals, Phys.
[34] S. S. Brinkman, X. L. Tan, B. Brekke, A. C. Mathisen,            Rev. B 98, 214405 (2018).
     Ø. Finnseth, R. J. Schenk, K. Hagiwara, M.-J. Huang,        [47] R. Nakajima, D. Hirobe, G. Kawaguchi, Y. Nabei,
     J. Buck, M. Kalläne, M. Hoesch, K. Rossnagel, K.-H.              T. Sato, T. Narushima, H. Okamoto, and H. M. Ya-
     Ou Yang, M.-T. Lin, G.-J. Shu, Y.-J. Chen, C. Tusche,            mamoto, Giant spin polarization and a pair of antipar-
     and H. Bentmann, Chirality-Driven Orbital Angular Mo-            allel spins in a chiral superconductor, Nature 613, 479
     mentum and Circular Dichroism in CoSi, Phys. Rev.                (2023).
     Lett. 132, 196402 (2024).                                   [48] S. Bhowal and S. Satpathy, Intrinsic orbital moment
[35] D. Oh, H. Bentmann, and R. Comin, Interplay of                   and prediction of a large orbital Hall effect in two-
     orbital angular momentum and chirality, Nat. Phys.               dimensional transition metal dichalcogenides, Phys. Rev.
     10.1038/s41567-025-03113-2 (2025).                               B 101, 121112 (2020).
[36] S. Moser, A toy model for dichroism in angle resolved       [49] B. Göhler, V. Hamelbeck, T. Z. Markus, M. Kettner,
     photoemission, J. Electron Spectrosc. Relat. Phenom.             G. F. Hanne, Z. Vager, R. Naaman, and H. Zacharias,
     262, 147278 (2023).                                              Spin Selectivity in Electron Transmission Through Self-
[37] S. Kim, R. C. McKay, N. Bielinski, C. Zhao, M.-K. Lin,           Assembled Monolayers of Double-Stranded DNA, Science
     J. A. Hlevyack, X. Guo, S.-K. Mo, P. Abbamonte, T.-              331, 894 (2011).
     C. Chiang, A. Schleife, D. P. Shoemaker, B. Bradlyn,        [50] R. Naaman, Y. Paltiel, and D. H. Waldeck, Chiral
     and F. Mahmood, Kramers-Weyl fermions in the chi-                molecules and the electron spin, Nat Rev Chem 3, 250
     ral charge density wave material (TaSe4 )2 I, preprint at        (2019).
     https://arxiv.org/abs/2108.10874 (2021).                    [51] R. Naaman, Y. Paltiel, and D. H. Waldeck, Chiral In-
[38] H. Yi, Z. Huang, W. Shi, L. Min, R. Wu, C. M. Pol-               duced Spin Selectivity and Its Implications for Biological
     ley, R. Zhang, Y.-F. Zhao, L.-J. Zhou, J. Adell, X. Gui,         Functions, Annu. Rev. Biophys. 51, 99 (2022).
     W. Xie, M. H. W. Chan, Z. Mao, Z. Wang, W. Wu, and          [52] Y. Adhikari, T. Liu, H. Wang, Z. Hua, H. Liu,
     C.-Z. Chang, Surface charge induced Dirac band splitting         E. Lochner, P. Schlottmann, B. Yan, J. Zhao, and
     in a charge density wave material (TaSe4 )2 I, Phys. Rev.        P. Xiong, Interplay of structural chirality, electron spin
     Research 3, 013271 (2021).                                       and topological orbital in chiral molecular spin valves,
[39] Y. H. Wang, D. Hsieh, D. Pilon, L. Fu, D. R. Gardner,            Nat. Commun. 14, 5163 (2023).
     Y. S. Lee, and N. Gedik, Observation of a Warped Helical    [53] B. Yan, Structural Chirality and Electronic Chirality
     Spin Texture in Bi2 Se3 from Circular Dichroism Angle-           in Quantum Materials, Annu. Rev. Mater. Res. 54, 97
     Resolved Photoemission Spectroscopy, Phys. Rev. Lett.            (2024).
     107, 207602 (2011).                                         [54] K. Koepernik and H. Eschrig, Full-potential nonorthogo-
[40] S. Cho, J.-H. Park, J. Hong, J. Jung, B. S. Kim,                 nal local-orbital minimum-basis band-structure scheme,
     G. Han, W. Kyung, Y. Kim, S.-K. Mo, J. Denlinger,                Phys. Rev. B 59, 1743 (1999).
     J. H. Shim, J. H. Han, C. Kim, and S. R. Park, Ex-          [55] I. Opahle, K. Koepernik, and H. Eschrig, Full-potential
     perimental Observation of Hidden Berry Curvature in              band-structure calculation of iron pyrite, Phys. Rev. B
     Inversion-Symmetric Bulk 2H−WSe2 , Phys. Rev. Lett.              60, 14035 (1999).
     121, 186401 (2018).                                         [56] M. K. Horton, P. Huck, R. X. Yang, J. M. Munro,
[41] C. Tournier-Colletta, L. Moreschini, G. Autès, S. Moser,         S. Dwaraknath, A. M. Ganose, R. S. Kingsbury, M. Wen,
     A. Crepaldi, H. Berger, A. L. Walter, K. S. Kim, A. Bost-        J. X. Shen, T. S. Mathis, A. D. Kaplan, K. Berket,
     wick, P. Monceau, E. Rotenberg, O. V. Yazyev, and                J. Riebesell, J. George, A. S. Rosen, E. W. C. Spotte-
     M. Grioni, Electronic Instability in a Zero-Gap Semicon-         Smith, M. J. McDermott, O. A. Cohen, A. Dunn, M. C.
     ductor: The Charge-Density Wave in (TaSe4 )2 I, Phys.            Kuner, G.-M. Rignanese, G. Petretto, D. Waroquiers,
     Rev. Lett. 110, 236401 (2013).                                   S. M. Griffin, J. B. Neaton, D. C. Chrzan, M. Asta,
[42] M.-K. Lin, J. A. Hlevyack, C. Zhao, P. Dudin, J. Avila,          G. Hautier, S. Cholia, G. Ceder, S. P. Ong, A. Jain,
     S.-K. Mo, C.-M. Cheng, P. Abbamonte, D. P. Shoe-                 and K. A. Persson, Accelerated data-driven materials
     maker, and T.-C. Chiang, Unconventional Spectral Gaps            science with the materials project, Nature Materials
     Induced by Charge Density Waves in the Weyl Semimetal            10.1038/s41563-025-02272-0 (2025).
     (TaSe4 )2 I, Nano Lett. 24, 8778 (2024).                    [57] A. Jain, S. P. Ong, G. Hautier, W. Chen, W. D. Richards,
[43] J. Rodríguez-Carvajal and F. Bourée, Symmetry and                S. Dacek, S. Cholia, D. Gunter, D. Skinner, G. Ceder,
     magnetic structures, EPJ Web of Conferences 22, 00010            and K. A. Persson, Commentary: The materials project:
     (2012).                                                          A materials genome approach to accelerating materials
[44] J. Erhardt, C. Schmitt, P. Eck, M. Schmitt, P. Keßler,           innovation, APL Materials 1, 011002 (2013).
     K. Lee, T. Kim, C. Cacho, I. Cojocariu, D. Baranowski,      [58] I. Petousis, D. Mrdjenovich, E. Ballouz, M. Liu, D. Win-
     V. Feyer, L. Veyrat, G. Sangiovanni, R. Claessen, and            ston, W. Chen, T. Graf, T. D. Schladt, K. A. Persson,
     S. Moser, Bias-Free Access to Orbital Angular Momen-             F. B. Prinz, A. S. Rosen, E. W. C. Spotte-Smith, M. J.
     tum in Two-Dimensional Quantum Materials, Phys. Rev.             McDermott, O. A. Cohen, A. Dunn, M. C. Kuner, G.-
     Lett. 132, 196401 (2024).                                        M. Rignanese, G. Petretto, D. Waroquiers, S. M. Griffin,
[45] I. Sidilkover, Y. Yen, S. W. D’Souza, J. Schusser,               J. B. Neaton, D. C. Chrzan, M. Asta, G. Hautier, S. Cho-
     A. Pulkkinen, C. R. Rotundu, M. Hashimoto, D. Liu,               lia, G. Ceder, S. P. Ong, and A. Jain, High-throughput
     Z.-X. Shen, J. Minár, M. Schüler, H. Soifer, and J. A.           screening of inorganic compounds for the discovery of
     Sobota, Reexamining circular dichroism in photoemission          novel dielectric and optical materials, Scientific Data 4,
                                                                                                                         12

     160134 (2017).                                                weiser, J. Qiao, F. Thöle, S. S. Tsirkin, M. Wierzbowska,
[59] G. Pizzi, V. Vitale, R. Arita, S. Blügel, F. Freimuth,        N. Marzari, D. Vanderbilt, I. Souza, A. A. Mostofi, and
     G. Géranton, M. Gibertini, D. Gresch, C. Johnson,             J. R. Yates, Wannier90 as a community code: new fea-
     T. Koretsune, J. Ibañez-Azpiroz, H. Lee, J.-M. Lihm,          tures and applications, Journal of Physics: Condensed
     D. Marchand, A. Marrazzo, Y. Mokrousov, J. I. Mustafa,        Matter 32, 165902 (2020).
     Y. Nohara, Y. Nomura, L. Paulatto, S. Poncé, T. Pon-     [60] Post wan by philipp eck, https://github.com/
                                                                   philipp-eck/post_wan.git.

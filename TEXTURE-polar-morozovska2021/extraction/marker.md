<!--
NOTE ON THIS EXTRACTION ARTIFACT (marker.md) — READ FIRST
==========================================================
* The real `marker` binary (marker-pdf) is NOT installed on this packaging host
  (only poppler's `pdftotext` is available). This file is the DOCUMENTED INTERIM
  FALLBACK, not genuine Marker output.
* ROLE of this file: the PROSE artifact. Body below is `pdftotext -layout`
  (column/table/heading structure preserved) — reads like the paper.
* FIDELITY CAVEAT: equation rendering is DEGRADED. Unicode math glyphs and
  multi-line equation layout (superscripts, tensor indices, integrals) are
  mangled by pdftotext — this is a known poppler limitation, NOT a physics gap.
  The AUTHORITATIVE, hand-transcribed LaTeX of every governing equation lives in
  report/REPORT.tex, and the numbered equations are also transcribed in
  extraction/nougat.mmd (the MATH artifact).
* TO REGENERATE PROPERLY (when marker is installed):
      marker_single textures-polar-morozovska2021.pdf ./extraction/ --output_format markdown
* Paper: Morozovska et al., "Chiral Polarization Textures Induced by the
  Flexoelectric Effect in Ferroelectric Nanocylinders", arXiv:2104.00598.
-->

# Chiral Polarization Textures Induced by the Flexoelectric Effect in Ferroelectric Nanocylinders

*(Interim pdftotext -layout extraction — see NOTE above)*

---

         Chiral Polarization Textures Induced by the Flexoelectric Effect in Ferroelectric
                                                Nanocylinders
     Anna N. Morozovska 1*, Riccardo Hertel2†, Salia Cherifi-Hertel2, Victor Yu. Reshetnyak3,
                                    Eugene A. Eliseev4, and Dean R. Evans5‡


                    1
                        Institute of Physics, National Academy of Sciences of Ukraine,
                                       46, pr. Nauky, 03028 Kyiv, Ukraine
2
    Université de Strasbourg, CNRS, Institut de Physique et Chimie des Matériaux de Strasbourg,
                                      UMR 7504, 67000 Strasbourg, France
                              3
                                  Taras Shevchenko National University of Kyiv,
                                  Volodymyrska Street 64, Kyiv, 01601, Ukraine
     4
         Institute for Problems of Materials Science, National Academy of Sciences of Ukraine,
                                     Krjijanovskogo 3, 03142 Kyiv, Ukraine
             5
                 Air Force Research Laboratory, Materials and Manufacturing Directorate,
                            Wright-Patterson Air Force Base, Ohio, 45433, USA


                                                   Abstract
Polar chiral structures have recently attracted much interest within the scientific community, as they pave
the way towards innovative device concepts similar to the developments achieved in nanomagnetism.
Despite the growing interest, many fundamental questions related to the mechanisms controlling the
appearance and stability of ferroelectric topological structures remain open. In this context, ferroelectric
nanoparticles provide a flexible playground for such investigations. Here, we present a theoretical study
of ferroelectric polar textures in a cylindrical core-shell nanoparticle. The calculations reveal a chiral
polarization structure containing two oppositely oriented diffuse axial domains located near the cylinder
ends, separated by a region with a zero-axial polarization. We name this polarization configuration
“flexon” to underline the flexoelectric nature of its axial polarization. Analytical calculations and
numerical simulation results show that the flexon’s chirality can be switched by reversing the sign of the
flexoelectric coefficient. Furthermore, the anisotropy of the flexoelectric coupling is found to critically
influence the polarization texture and domain morphology. The flexon rounded shape, combined with its
distinct chiral properties and the localization nature near the surface, are reminiscent of Chiral Bobber
structures in magnetism. In the azimuthal plane, the flexon displays the polarization state of a vortex with
an axially polarized core region, i.e., a meron. The flexoelectric effect, which couples the electric


*          Corresponding author 1: anna.n.morozovska@gmail.com
†          Corresponding author 2: riccardo.hertel@ipcms.unistra.fr
‡          Corresponding author 4: dean.evans@afresearchlab.com

                                                       1
polarization and elastic strain gradients, plays a determining role in the stabilization of these chiral states.
We discuss similarities between this interaction and the recently predicted ferroelectric Dyzaloshinskii-
Moriya interaction leading to chiral polarization states.


                                           I. INTRODUCTION
Research on ferroelectric materials has received growing interest over the past years, driven in
part by the potential of these material systems for low-power technological applications in a
broad spectrum of domains [1, 2], ranging from high-density data storage to optical nano-
devices. A central aspect of this field of research is the formation of ferroelectric domain
structures [3], and more generally the micro- and nanoscale structure of the polarization field [4].
Traditionally, research on ferroelectrics is centered on the study of bulk materials and thin films
[5, 6, 7], but recently ferroelectric nanoparticles have also attracted increasing interest [8, 9, 10,
11, 12, 13, 14]. In ferroelectric thin films and nanoparticles, the polarization structure is strongly
affected by electrostatic (depolarizing) fields [15, 16, 17, 18], as well as by strain and strain
gradients [19, 20, 21, 22] via the flexoelectric effect [23, 24, 25, 26].
        Although the foundations for the theoretical description of ferroelectrics have been
established decades ago [27], understanding the complex physical properties of these material
systems remains a challenge for fundamental research. Recent progress in this field, achieved to
a large extent through advanced imaging techniques [28] and by employing modern numerical
simulations [29], includes the discovery of highly complex polarization structures, such as flux
closure [5, 30] and bubble domains [31], meandering [32, 33] and/or labyrinthine [11, 34]
structures, non-Ising type chiral domain walls [35], polarization vortices in thin layers [36, 37,
38], nanodots [39] or nanopillars [40], or polar skyrmions [41, 42].
        While skyrmions and other chiral structures have dominated the past decade of research
in magnetism [43], these topological states have received less attention by the ferroelectric
community. Only recently a strong interest has emerged in chiral polarization structures, which
can be attributed to the observation of skyrmion states in ferroelectrics [41-42]. However, the
theoretical understanding of these structures is not as advanced as it is in the case of their
magnetic counterparts, and the mechanism that underpins the formation of skyrmions in
ferroelectrics is not fully understood. The fundamental interaction stabilizing the magnetic
version of these structures in chiral ferromagnets [44, 45] is the Dzyaloshinky-Moriya Interaction
(DMI). The DMI favors the formation of helical structures with a well-defined handedness as
they occur, e.g., along the radial direction of skyrmions. As scientists working on ferroelectrics
hope to replicate the success that chiral structures have witnessed in magnetism, the possibility


                                                       2
of a “ferroelectric DMI” has recently been discussed [46]. However, Erb and Hlinka [47] showed
that only very few exotic ferroelectrics could theoretically sustain an intrinsic DMI-type
interaction since it requires particular symmetry properties of the crystal lattice. Here we discuss
the flexoelectric coupling as an alternative mechanism that can generate chiral polarization states
in ferroelectrics.
        The thermodynamic description of the flexoelectric effect is given by the Lifshitz
invariant in the free energy expansion [22]. It is known that, in magnetic materials, the
occurrence of similar Lifshitz invariants converts directly into an antisymmetric coupling known
as the DMI [48, 49], which favors the formation of helicoidal structures with a specific chirality.
The existence of a ferroelectric counterpart of the DMI was recently predicted by first-principles
simulations [46]. The ferroelectric analogue of the DMI was discussed in the context of Lifshitz
invariants by Strukov and Levanyuk [50], and more recently by Erb and Hlinka [47], who argued
that a ferroelectric DMI can exist. In addition to the remarkable similarity in the mathematical
form of the flexoelectric Lifshitz invariant and DMI, the flexoelectric term appears to have a
similar impact as the DMI in terms of the formation of chiral structures.
        By means of the finite element modeling (FEM) based on the Landau-Ginzburg-
Devonshire (LGD) theory, this paper shows that an anisotropic flexoelectric effect can give rise
to a previously unexplored type of polarization state with distinct chiral properties. Remarkably,
these homochiral properties are not induced by a DMI term. This finding suggests that the
recently discussed DMI in ferroelectrics is not the only possible mechanism for the formation of
homochiral polarization states, and that anisotropic flexoelectric effects offer an alternative
pathway to stabilize such structures in ferroelectric nanostructures. We discuss common aspects
of the DMI and the flexoelectric effect, which are both derived from Lifshitz invariants in the
framework of the Landau theory of second-order phase transitions [22].


                 II. CONSIDERED PROBLEM AND MATERIAL PARAMETERS
        Using a LGD phenomenological approach along with electrostatic equations and
elasticity theory, we model the polarization, the internal electric field, and the elastic stresses and
strains in a core-shell nanoparticle using FEM, where the ferroelectric core is made of BaTiO3
and has a cylindrical shape. The aspect ratio of the nanocylinder radius 𝑅 to its length ℎ is
significantly higher than unity. The z-axis is parallel to the cylinder axis (Fig. 1). The shell is an
elastically soft paraelectric or high-k semiconductor with a thickness ∆𝑅 ≪ 𝑅 and screening
length Λ ≥ 1 nm. The coverage can be artificial (e.g., a soft organic semiconductor or vacancy-
enriched SrTiO3) or natural, and in the latter case it would originate from the polarization

                                                  3
screening by surrounding media. The core-shell nanoparticle is placed in a very soft elastic
medium.
                                                     z




                                                                                soft medium
                                                 core
                                                     P3                h

                                      shell
                                              P1,2
                                                     2R

FIGURE 1. A cylindrical ferroelectric nanoparticle (core) of radius 𝑅, covered with an elastically soft
semiconducting shell with a thickness ∆𝑅 ≪ 𝑅 and screening length Λ of 1 nm, placed in an isotropic
elastically soft effective medium. The direction of axial polarization 𝑃3 is shown by the straight orange
arrow, and lateral components 𝑃1,2 are shown by the curled red-blue arrow to highlight their vortex-type
structure.


        The LGD free energy functional G of the nanoparticle core includes a Landau energy –
an expansion on powers of 2-4-6 of the polarization (𝑃𝑖 ), 𝐺𝐿𝑎𝑛𝑑𝑎𝑢 ; a polarization gradient energy,
𝐺𝑔𝑟𝑎𝑑 ; an electrostatic energy, 𝐺𝑒𝑙 ; an elastic, electrostriction contribution 𝐺𝑒𝑠 , a flexoelectric
contribution, 𝐺𝑓𝑙𝑒𝑥𝑜 ; and a surface energy, 𝐺𝑆 . It has the form [51]:
                      𝐺 = 𝐺𝐿𝑎𝑛𝑑𝑎𝑢 + 𝐺𝑔𝑟𝑎𝑑 + 𝐺𝑒𝑙 + 𝐺𝑓𝑙𝑒𝑥𝑜 + 𝐺𝑓𝑙𝑒𝑥𝑜 + 𝐺𝑆 ,                               (1a)
                       𝐺𝐿𝑎𝑛𝑑𝑎𝑢 = ∫𝑉𝑐 𝑑3 𝑟 [𝑎𝑖 𝑃𝑖2 + 𝑎𝑖𝑗 𝑃𝑖2 𝑃𝑗2 + 𝑎𝑖𝑗𝑘 𝑃𝑖2 𝑃𝑗2 𝑃𝑘2 ],                  (1b)
                                                                 𝑔        𝜕𝑃 𝜕𝑃
                                        𝐺𝑔𝑟𝑎𝑑 = ∫𝑉𝑐 𝑑 3 𝑟 𝑖𝑗𝑘𝑙 𝑖  𝑘
                                                                    ,                                  (1c)
                                                           2 𝜕𝑥 𝜕𝑥          𝑗          𝑙

                                                                     𝜀 𝜀
                                𝐺𝑒𝑙 = − ∫𝑉𝑐 𝑑 3 𝑟 (𝑃𝑖 𝐸𝑖 + 0 𝑏 𝐸𝑖 𝐸𝑖 ),                                (1d)
                                                                      2
                                                         𝑠
                                 𝐺𝑒𝑠 = − ∫𝑉𝑐 𝑑3 𝑟 ( 𝑖𝑗𝑘𝑙 𝜎𝑖𝑗 𝜎𝑘𝑙 + 𝑄𝑖𝑗𝑘𝑙 𝜎𝑖𝑗 𝑃𝑘 𝑃𝑙 ),                  (1e)
                                                     2
                                                             𝐹             𝜕𝑃                 𝜕𝜎
                                 𝐺𝑓𝑙𝑒𝑥𝑜 = − ∫𝑉𝑐 𝑑 3 𝑟 𝑖𝑗𝑘𝑙 (𝜎𝑖𝑗 𝜕𝑥𝑘 − 𝑃𝑘 𝜕𝑥𝑖𝑗 ),                       (1f)
                                                       2                        𝑙                  𝑙

                                         1           (𝑆)
                                  𝐺𝑆 = 2 ∫𝑆 𝑑 2 𝑟 𝑎𝑖𝑗 𝑃𝑖 𝑃𝑗 .                                          (1g)

Here 𝑉𝐶 is the core volume. The coefficient 𝑎𝑖 linearly depends on temperature T, 𝑎𝑖 (𝑇) =
𝛼𝑇 [𝑇 − 𝑇𝐶 ], where 𝛼 𝑇 is the inverse Curie-Weiss constant and 𝑇𝐶 is the ferroelectric Curie
temperature renormalized by surface tension/intrinsic surface stresses [52, 53, 54] and surface


                                                     4
bond contraction [55, 56]. Tensor components 𝑎𝑖𝑗 are regarded as temperature-independent. The
tensor 𝑎𝑖𝑗 is positively defined if the ferroelectric material undergoes a second order transition
to the paraelectric phase and negative otherwise. The higher nonlinear tensor 𝑎𝑖𝑗𝑘 and the
gradient coefficients tensor 𝑔𝑖𝑗𝑘𝑙 are positively defined and regarded as temperature-
independent. In Eq.(1e), 𝜎𝑖𝑗 is the stress tensor, 𝑠𝑖𝑗𝑘𝑙 is the elastic compliances tensor, and 𝑄𝑖𝑗𝑘𝑙
is the electrostriction tensor. In the Lifshitz invariant, Eq.(1f), 𝐹𝑖𝑗𝑘𝑙 is the flexoelectric tensor.
        Landau-Khalatnikov equations [57, 58] obtained from a variation of the free energy (1),
mathematical formulation of the electrostatic and elastic sub-problem (see e.g. [59]), initial and
boundary conditions (see e.g. [60, 61, 62]), sensitivity to the shape of the cylinder ends,
polarization gradient coefficients, shell dielectric permittivity and semiconducting properties,
and other details of FEM are given in Appendix A of Suppl. Mat. [63]. The ferroelectric,
dielectric, and elastic properties of the BaTiO3 core are collected from Refs. [64, 65, 66, 67, 68
and 69] and given in Table SI.


                         III. RESULTS OF FINITE ELEMENT MODELING
                                 A. FEM Results at Room Temperature
        Images in Figs. 2a and 3a are calculated without electrostriction (𝑄𝑖𝑗 = 0) and
flexoelectric (𝐹𝑖𝑗 = 0) couplings between the electric polarization and elastic stresses. For the
case a very prolate dipolar kernel oriented along z-axis appears inside the cylindrical core. The
kernel has relatively thin 180-degree domain walls, which are mostly uncharged because they
are parallel to the kernel axis and cylinder lateral surface. The bound charges appear at the walls
only in a small spatial region near the kernel that is contact with the cylinder ends, where the
180-degree walls become counter head-to-head walls. The axial polarization 𝑃3 inside the kernel
is high, 𝑃3 ~ − (20 − 25) C/cm2 (this is very close to the bulk polarization of BaTiO3
~26 C/cm2), and the surrounding core has relatively small axial polarization of the opposite
sign, 𝑃3 ~(0 − 5) C/cm2. The lateral components of polarization, 𝑃1 and 𝑃2 , form a two-
dimensional (2D) vortex without a central empty core, because a dipolar kernel evolves instead
(Fig. S4 [63]). The two symmetrical Bloch points with 𝑷 = 0 are located at the junction of the
dipolar kernel with the cylinder ends. The “up” or “down” orientation of polarization component
𝑃3 inside the kernel is determined by random noise in the initial conditions.
      Images in Figs. 2b-d and 3b-e are calculated for a nonzero electrostriction coupling (𝑄𝑖𝑗 ≠
0) and either negative, zero, or positive values of the flexoelectric coefficients 𝐹𝑖𝑗 . In the presence
of electrostriction coupling the dipolar kernel disappears completely (Figs. 2c and 3c). The

                                                   5
flexoelectric effect induces an axial component of polarization consisting of two oppositely
oriented diffuse 𝑃3 -domains located near the cylinder ends and separated by a region with 𝑃3 ≈
0 (Figs. 2b, 2d and 3b, 3d).



      (a) 𝐹𝑖𝑗 = 0                 (b) 𝐹𝑖𝑗 < 0               (c) 𝐹𝑖𝑗 = 0                 (d) 𝐹𝑖𝑗 > 0
        𝑄𝑖𝑗 = 0                     𝑄𝑖𝑗 ≠ 0                   𝑄𝑖𝑗 ≠ 0                     𝑄𝑖𝑗 ≠ 0
              P3 (μC/cm2)                 P3 (μC/cm2)                P3 (μC/cm2)                 P3 (μC/cm2)




    Dipolar kernel               Negative flexon               No flexon                Positive flexon




FIGURE 2. Distribution of the polarization component 𝑃3 (the top row) inside a cylindrical nanoparticle
and a magnified view on the flexon structure (the bottom row). The arrows show the orientation of
polarization vector 𝑷. The images are calculated without electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric
(𝐹𝑖𝑗 = 0) couplings (a); with electrostriction coupling (𝑄𝑖𝑗 ≠ 0) and negative (b), or zero (c), or positive
(d) values of flexoelectric coefficients 𝐹𝑖𝑗 . The values of 𝐹𝑖𝑗 and all other parameters are given in Table
SI, 𝑇 = 300 K. Note the different scales for 𝑃3 -distributions in plots (a)-(d) in order to maintain a contrast
between the different regions.


      The diffuseness of the 𝑃3 -domain walls is dictated by the need to decrease the
depolarization field produced by the bound charges of the head-to-head domain walls. The 𝑃3 -
domains are located near the cylinder ends, and their length (about 10 nm) and lateral size (about
5 nm) are almost independent on the cylinder length if ℎ ≫ 5 nm. The component 𝑃3 is very
small (|𝑃3 | ≤ 0.4 C/cm2), but it increases up to 1.2 C/cm2 with the flexoelectric coupling
increase (Figs. 3e) and then saturates (Figs. 3f). The axial 𝑃3 -domains, which have opposite

                                                      6
direction of polarization, change their direction under the transformation 𝐹𝑖𝑗 → −𝐹𝑖𝑗 (compare
the position of red and blue diffuse spots of the 𝑃3 distributions in Fig. 3b and 3d), while the
distribution of the lateral components 𝑃1,2 and the polarization magnitude 𝑃 are virtually
independent of the 𝐹𝑖𝑗 sign and magnitude (Figs. S4-5 [63]).
       The maximal (𝑃𝑚𝑎𝑥 ) and minimal (𝑃𝑚𝑖𝑛 ) values of 𝑃3 are shown by the red and blue
curves in Fig. 3f. The values 𝑃𝑚𝑎𝑥 and 𝑃𝑚𝑖𝑛 are even functions of the flexoelectric coupling
strength 𝑓, where 𝐹𝑖𝑗 = 𝑓𝐹𝑖𝑗0 and the reference values of 𝐹𝑖𝑗0 are given in Table SI. The extremal
(maximal or minimal) value 𝑃𝑒 in the center of the diffuse axial P3-domain is an odd function of
𝑓, which is zero at 𝐹𝑖𝑗 = 0 (the green curve in Fig. 3f). Note that the 𝑃𝑒 value frequently differs
from 𝑃𝑚𝑎𝑥 and 𝑃𝑚𝑖𝑛 values due to the presence of the small sixteen 𝑃3 -domains localized near
the top and bottom junction of the sidewall with the cylinder ends (bottom row in Fig. S5 [63]).
       For the remainder of the paper, we refer to the localized polarization structure near the
wire ends as a “flexon” for the sake of brevity and to underline the flexoelectric nature of its
axial polarization. The main effect of a change of sign in the flexoelectric coefficients is the
reorientation of the flexon axial polarization. The polarization structures at the wire ends shown
in Fig. 2b-2d and Fig. 3b-2d display localized chiral structures with different chirality on
opposite ends of the wire, and their chirality changes upon reversal of the sign of the flexoelectric
coupling constant.
       To understand the chirality change, we derived in Appendix E [63] an approximate
analytical expression for the polarization distribution inside the flexon:
                 𝑃1 (𝜌, 𝜑, 𝑧) ≈ 𝑝(𝜌, 𝑧)sin𝜑,           𝑃2 (𝜌, 𝜑, 𝑧) ≈ −𝑝(𝜌, 𝑧)cos𝜑,                               (2a)
                           𝑄44                                           𝐹 −𝐹 −𝐹       𝜕
                                𝑝(𝜌,𝑧)[𝑢13 (𝜌,𝜑,𝑧)sin𝜑−𝑢23 (𝜌,𝜑,𝑧)cos𝜑]− 11 44 12 𝑢33 (𝜌,𝜑,𝑧)
                            𝑠44                                            𝑠11 −𝑠12   𝜕z
       𝑃3 (𝜌, 𝜑, 𝑧) ≈         𝑄 +2𝑄12 2           𝑄 −𝑄                             𝐹 −𝐹                  ,        (2b)
                        2[𝑎1 − 11        𝑝 (𝜌,𝑧)− 11 12 𝑢33 +[𝑔11 +(𝐹11 −𝐹44 −𝐹12 ) 11 12 ]𝐿𝑧𝐶 +𝑔44 𝐿𝑥𝐶 ]
                               𝑠11 +2𝑠12          𝑠11 −𝑠12                         𝑠11 −𝑠12

                                                                                       𝜌
where {𝜌, 𝜑, 𝑧} are cylindrical coordinates, the function 𝑝(𝜌, 𝑧)~tanh (𝐿𝑥 ), 𝐿𝑥𝐶 and 𝐿𝑧𝐶 are lateral
                                                                                       𝐶

and axial correlation lengths. The functions 𝑢𝑖𝑗 (𝜌, 𝜑, 𝑧) are elastic strains, 𝑠𝑖𝑗 are elastic
compliances; 𝑄𝑖𝑗 are electrostriction tensor components, 𝑔𝑖𝑗 are polarization gradient
coefficients written in Voigt notations. The first term in Eq.(2b) is induced by the electrostriction
                                                       𝐹 −𝐹 −𝐹12 𝜕
coupling, and the second term, proportional to 11𝑠 −𝑠
                                                   44
                                                                           𝑢33 (𝜌, 𝜑, 𝑧), is the flexon.
                                                            11   12   𝜕z

       In order to quantify the chirality of the polarization structure and its variation along the
                                                                                           1       𝜕𝑝⃗      𝜕𝑝⃗
cylinder axis, in Appendix F [63] we calculate the topological index 𝑛 = 4𝜋 ∫𝑆 𝑝⃗ [𝜕𝑥 × 𝜕𝑦 ] 𝑑𝑥𝑑𝑦




                                                        7
                                                 𝑃⃗⃗
[70] of the unit polarization orientation 𝑝⃗ =         for the integration over the cylinder cross-section
                                                 𝑃

{𝑥, 𝑦}. For the case of 𝑃3 (𝜌 = 𝑅, 𝑧) → 0, z-dependence of the topological index is
                                             3   𝑃 (𝜌=0,𝑧)           sign[𝑓]𝑧
                                   𝑛(𝑧) = − 2𝑃(𝜌=0,𝑧) ≅−                        .                      (3)
                                                                   2√1+(𝑧 2 ⁄𝐵)

Here sign[𝑓] is the sign of the flexoelectric coefficients 𝐹𝑖𝑗 , 𝐵 is a positive constant, which
depends on the absolute value of |𝐹𝑖𝑗 |. 𝑛(𝑧) is a normalized profile of 𝑃3 (𝜌 = 0, 𝑧), and so
𝑛(𝑧) = 0 for 𝐹𝑖𝑗 = 0, and its sign is defined by the sign of 𝐹𝑖𝑗 . The dependence 𝑛(𝑧) is shown
in Fig. 3g and Fig. S10a for zero, positive, and negative 𝐹𝑖𝑗 . Since the value 𝑃(0, 𝑧) is very close
to the 𝑃3 (0, 𝑧) near the cylinder ends (Fig. S10a and S10b), and 𝑃3 (0, 𝑧) vanishes in the central
part of a nanoparticle, the topological index continuously changes from -½ to +½ with a z-
coordinate change from one cylinder end to the other. The result clearly shows the localization
of the chiral structures – the flexons – at the ends of the wires. The topological index, which can
be interpreted as the degree to which a structure is chiral, changes sign from one end to the other,
and changes sign upon reversal of the sign of 𝐹𝑖𝑗 . It also increases in magnitude with increasing
absolute value of |𝐹𝑖𝑗 |. These properties are evidence of an obvious correlation between the
flexoelectric effect and the formation of chiral polarization structures.
       The revealed type of isolated chiral polarization structures, i.e., flexons, display
topological features of a three-dimensional meron. In this sense, the polarization vortex in the
XY-plane can be interpreted as the Bloch-like transition region of a meron connecting
polarization directions of opposite P3 sign in the core region and in the outer cylindrical shell
(Fig. 2). The flexon polarization 𝑃⃗⃗ develops a characteristic drop-shape with a chiral structure
localized near the surfaces of the cylinder that is reminiscent of the chiral-bobber state found in
non-centrosymmetric magnetic films [71] and nanoparticles [72]. It is worth noting that similar,
skyrmion-like configurations at the ends of cylindrical nanowires have also been predicted
analytically [73] and numerically [74] in the case of non-chiral ferromagnetic materials, but only
in the form of transient configurations appearing during the dynamic magnetization reversal
process. Here, the skyrmion-like polarization structures appear as stable states in the
ferroelectrics, owing to a chiral-symmetry breaking effect of the flexoelectric coupling. In
contrast to previous findings [75, 76, 77], the flexon structure is chiral [78] and almost uncharged
because 𝑑𝑖𝑣𝑃⃗⃗ ≅ 0 (Fig. S9b [63]).




                                                       8
                 (a) 𝐹𝑖𝑗 = 0      (b) 𝐹𝑖𝑗 < 0      (c) 𝐹𝑖𝑗 = 0          (d) 𝐹𝑖𝑗 > 0          (e) 𝐹𝑖𝑗 >> 0
                   𝑄𝑖𝑗 = 0          𝑄𝑖𝑗 ≠ 0          𝑄𝑖𝑗 ≠ 0              𝑄𝑖𝑗 ≠ 0               𝑄𝑖𝑗 ≠ 0
                                                                2
                 P3 (μC/cm2)      P3 (μC/cm2)       P3 (μC/cm )          P3 (μC/cm2)            P3 (μC/cm2)



                                                  Pmax
                                Pmax
  z-coordinate




                                        Pe                                  flexon                 flexon

                                Pmin               Pmin



            x-coordinate          x-coordinate      x-coordinate           x-coordinate        x-coordinate


                                                                    Pmax
                          (f)
 P3 (μC/cm2)




                                                                                Top. index
                                                                                             (g)

                                                   Pe
                                                         Pmin
                                                                                                    z (nm)


                                       Flexoelectric coupling amplitude f (rel. units)
FIGURE 3. Distribution of the polarization component 𝑃3 (the top row) in the XZ cross-section of the
nanoparticle. Images are calculated without electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric (𝐹𝑖𝑗 = 0) coupling
(a); with electrostriction coupling (𝑄𝑖𝑗 ≠ 0) and negative (b), zero (c), positive (d), or high positive (e)
values of flexoelectric coefficients 𝐹𝑖𝑗 . The bottom part (f) is the dependence of the maximal (red curve,
𝑃𝑚𝑎𝑥 ) and minimal (blue curve, 𝑃𝑚𝑖𝑛 ) values of 𝑃3 on the relative amplitude of the flexoelectric coupling
strength 𝑓. The green curve is the extremal (maximal or minimal) value 𝑃𝑒 in the center of the top axial
𝑃3 -domain. Here 𝐹𝑖𝑗 = 𝑓𝐹𝑖𝑗0 , the values of 𝐹𝑖𝑗0 and all other parameters are given in Table SI, 𝑇 = 300
K. The Z-profile of the polarization topological index 𝑛(𝑧) is shown in the inset (g) for zero (black line),
positive (red curve), and negative (blue curve) 𝐹𝑖𝑗 . Note the different scales for 𝑃3 in the plots (a) and (b)-
(e) in order to maintain a contrast between the different regions.




                                                          9
       As a rule, the flexoelectric tensor component 𝐹44 is either poorly known from experiments
or ill-defined from ab initio calculations; therefore, we can vary it over a wide range to determine
the degree by which the flexoelectric coupling anisotropy influences the morphology of the
polarization state. Corresponding FEM results are shown in Fig. 4. The top and middle rows
illustrate that the 𝑃3 distribution changes very strongly when 𝐹44 varies from high negative to
high positive values, while the other components of the flexoelectric tensor are fixed and equal
to the tabulated values 𝐹11 = 2.4 ∙10-11m3/C and 𝐹12 = 0.5 ∙ 10-11m3/C.
       The flexon contains two pronounced axial domains located near the cylinder ends, which
have thick diffuse domain walls and opposite polarization directions, and exist at high negative
(Fig. 4a) and high positive (Fig. 4b and 4e) 𝐹44 values. The 𝑃3 -domains become smaller and
more diffuse with a decrease of |𝐹44 |; but they are still visible and practically do not change their
shape, size, or polarization distribution for small |𝐹44 | values over the range |𝐹44 | ≤ 0.06
(Fig. 4b). The flexon becomes faint and almost disappears when 𝐹44 approaches the value 𝐹44 =
𝐹11 − 𝐹12 = 1.9 ∙ 10-11 m3/C corresponding to the isotropic symmetry of 𝐹𝑖𝑗 (Fig. 4c). The value
will be referred to as “isotropic” below.
       The dependence of the maximal (red curve, 𝑃𝑚𝑎𝑥 ) and minimal (blue curve, 𝑃𝑚𝑖𝑛 ) values
of the polarization component 𝑃3 on the relative amplitude f of the flexoelectric coefficient 𝐹44
                                   0       0
is shown in Fig. 4f, where 𝐹44 = 𝑓𝐹44 and 𝐹44 = 0.06 ∙ 10-11 m3/C. The values 𝑃𝑚𝑎𝑥 and 𝑃𝑚𝑖𝑛
reach a very diffuse plateau-like minimum and maximum, respectively, at the isotropic value
𝐹44 = 𝐹11 − 𝐹12 . The green curve in Fig. 4f is the extremal value 𝑃𝑒 in the center of the bottom
axial 𝑃3 -domain. The extremal value 𝑃𝑎 in the center of the diffuse 𝑃3 -domain changes its sign
in the immediate vicinity of the isotropic value 𝐹44 = 𝐹11 − 𝐹12 . The values 𝑃𝑚𝑎𝑥 , 𝑃𝑚𝑖𝑛 , and 𝑃𝑒
have no definite parity, because they are neither odd nor even functions of the flexoelectric
coefficient 𝐹44 amplitude 𝑓. From Fig. 4f we can conclude that the anisotropy of the flexoelectric
coupling critically influences the morphology of the flexon, where the axial part of the flexon
                                     𝐹 −𝐹 −𝐹12 𝜕𝑢33
polarization is proportional to − 11𝑠 −𝑠
                                      44
                                                       [Eq.(2b)], this proportionality along with
                                        11   12   𝜕z

Fig. S9 qualitatively describes the curves’ behavior in Fig. 4f.




                                                  10
 (a) high neg.                    (b) small         (c) isotropic         (d) positive       (e) high pos.
   𝐹44 = −6                     |𝐹44 | ≤ 0.06         𝐹44 = 1.9             𝐹44 = 3             𝐹44 = 6

       P3 (μC/cm2)               P3 (μC/cm2)          P3 (μC/cm2)           P3 (μC/cm2)           P3 (μC/cm2)
  z-coordinate




                                                                                           Pmin
                                       flexon                                 Pe
                                                                                           Pmax


             x-coordinate         x-coordinate       x-coordinate        x-coordinate         x-coordinate


                                                                                    Pmax
    P3 (μC/cm )




                          (f)
  2




                                                               Pe


                                Pmin
                                                                              F44=F11-F12


                                Flexoelectric coefficient F44 amplitude f (rel. units)

FIGURE 4. Distribution of the polarization component 𝑃3 in the XZ cross-section of cylindrical core (the
top row). Images are calculated for the fixed values 𝐹11 = 2.4 ∙10-11 m3/C and 𝐹12 = 0.5 ∙ 10-11 m3/C,
while the value of 𝐹44 varies from -6 to 6 (in 10-11m3/C) as indicated in the legends. The bottom part (f)
is the dependence of the maximal (red curve, 𝑃𝑚𝑎𝑥 ) and minimal (blue curve, 𝑃𝑚𝑖𝑛 ) values of 𝑃3 on the
relative amplitude f of the flexoelectric coefficient 𝐹44 in the core. The green curve is the extremal
                                                                                         0       0
(maximal or minimal) value 𝑃𝑒 in the center of the bottom axial 𝑃3 -domain. Here 𝐹44 = 𝑓𝐹44 and 𝐹44 =
0.06 ∙ 10-11 m3/C. The electrostriction coupling coefficients 𝑄𝑖𝑗 and all other parameters are listed in
Table SI, 𝑇 = 300 K. Note the different scales for 𝑃3 in the plots (a)-(e) in order to maintain a contrast
between the different regions.


                        B. Temperature Behavior of the Flexon-Type Polarization Distribution
                  To define the temperature interval in which flexons exist as stable or meta-stable states,
we performed FEM in the temperature range from 50 K to 400 K using different initial

                                                          11
distribution of polarization in a cylindrical core. Typical FEM results are shown in Fig. 5, where
the columns (a)-(e) correspond to the temperature increase from 240 K to 370 K; the structure of
the azimuthal components of the polarization vector, 𝑃1 and 𝑃2 , is vortex-like and shows weak
variations when approaching the surface over the same temperature range (see the direction of
arrows at the bottom image of Figs. S7 [63]).



   (a) T=240 K                                (b) T=270 K (c) T=300 K (d) T=340 K (e) T=370 K
                                P3 (μC/cm2)                P3 (μC/cm2)    P3 (μC/cm2)   P3 (μC/cm2)    P3 (μC/cm2)
    z-coordinate flux-closure




                                                                                                          disappearence
                                              flexon formation




                                                                                                              flexon
                                                                                              flexon
                                                                               flexon
                                  bidomai
                                       n




                x-coordinate                    x-coordinate             x-coordinate   x-coordinate   x-coordinate

FIGURE 5. Distribution of polarization component 𝑃3 in XZ cross-sections of the nanoparticle core.
Different columns are calculated for the temperatures 𝑇 = 240, 270, 300, 340, and 370 K (a, b, c, d, e).
All other parameters are listed in Table I. Note the different scales for 𝑃3 in the plots (a) and (b)-(e) in
order to maintain a contrast between the different regions.


                                A bidomain configuration of 𝑃3 is stable at temperatures lower than 250 K (Figs. 5a).
The bidomain structure has a relatively thin uncharged 180-degree domain wall inside the
cylinder, which transforms into a flux-closure domain near the electrically-open cylinder ends.
An initial four-domain polarization distribution relaxes to a flexon-like domain structure in the
temperature range 260 K < 𝑇 < 360 K (Figs. 5b-d). The flexon gradually disappears at 𝑇 >
370 K (the middle image in Figs. 5e). The ferroelectric polarization inside the core significantly
decreases at 𝑇 > 370 K and completely disappears at 𝑇~400 K (the top image in Figs. 5e). The
structure becomes faint with a temperature increase above 370 K (Figs. 5e), hence, the flexon-
type polarization distribution exists in a relatively wide temperature range 260 K < 𝑇 < 360 K.




                                                                              12
The axial counter domains inherent to flexons are the most pronounced feature over the narrower
range 290 K < 𝑇 < 340 K.


                                            IV. DISCUSSION
       Any deviation from a four quadrants domain configuration in the flexon-type polarization
distribution is found to be metastable. This is because the antiparallel bidomain-type polarization
distribution (starting from a random noise) has a lower free energy in a BaTiO3 cylindrical
nanoparticle. The derived energy values at room temperature are 𝐺𝑓𝑙 = −3.6 ∙ 10−18 J and
𝐺𝑏𝑑 = −4.0 ∙ 10−18 J in the flexon and the bidomain structure, respectively. The energy
difference between these states, ∆𝐺 = 4 ∙ 10−19 J is much higher (about 100 𝑘𝐵 𝑇) than the
                                                                         ∆𝐺
thermal energy barrier 𝑘𝐵 𝑇 at room temperature. However, the ratio 𝑘 𝑇 strongly decreases with
                                                                          𝐵

as the temperature increases. The linear relative dielectric permittivity in both states is about 110
at room temperature and it strongly increases with temperature. Furthermore, our numerical
simulations show that a spontaneous off-field transition from the flexon to the bidomain
polarization state does not occur, whereas the in-field transition is possible (corresponding
hysteresis loops are shown in Appendix D [63]). Thus, the bidomain and flexon states of a
prolate core-shell ferroelectric nanoparticle can be considered as the exited and ground state of
a two-level system suitable for information recording. The two-level system can imitate qubits
                                                  ∆𝐺
operating in the temperature range where 1 < 𝑘 𝑇 < 5. Furthermore, the bidomain polarization
                                                   𝐵

state corresponds to an antiferroelectric-like state of the nanoparticle polarization, which can be
represented as two antiparallel nanoscopic dipoles. The flexon is a much more complex achiral
vortex-like configuration containing two counter dipole nanodomains with diffuse relaxor-like
polar properties. Thus, an ensemble of prolate core-shell ferroelectric nanoparticles, where a
given nanoparticle is either in a flexon or a bidomain state, can be an alternative media for
information processing. The media may exhibit unusual properties including antiferroelectric
and/or relaxor-like polarization states, which can lead to additional functionalities. Note that the
appearance of the antiferroelectric and relaxor-like glass states, as well as a newly discovered
liquid glass state [79] with additional (anti)ferroelectric ordering and other cross-talk effects, are
possible in a suspension of the prolate core-shell ferroelectric nanoparticles.
       The relatively wide temperature range (about 100 K) corresponding to the stability or
meta-stability of the flexon-type polarization distribution gives us the hope that the domain
morphology can be observed experimentally. Specifically, the measurements of local vertical
displacement by piezoresponse force microscopy (PFM) visualize the distribution of 𝑃3 (𝑟⃗) at

                                                 13
distances ~ 10 nm from the ends of a nanoparticle, but the resolution procedure for the local
piezoresponse of diffuse domains under the surface is far not straightforward [80, 81]. This is
because PFM is a near-field method. A complementary tool to probe chiral polar textures is far-
field nonlinear optical microscopy [82], which has a comparatively much lower resolution than
PFM, yet optimum focusing methods and the experimental geometry allow for overcoming the
diffraction limit. For example, second-harmonic generation microscopy was successfully used
by the community to precisely study semiconductor nanowires [83]. This method should also be
capable of providing complementary information on the 3D ferroelectric domain structure (being
sensitive to 𝑃1,2 and 𝑃3 ) by using polarimetry analysis (see, e.g., [84]). Another promising
method is resonant elastic soft X-ray scattering, a synchrotron-based method sensitive to chiral
polar arrangements through dichroism effects [85, 86]. This method was successfully applied to
detect different topological structures, including vortices [36], skyrmions [41], and chiral domain
walls [87].
       Note that Liu et al. [39] revealed that an axial polarization component of the vortex can
appear in ferroelectric PbTiO3 nanodots due to the flexoelectric effect. Thus, the paper [39] and
this work predict different flexo-sensitive vortex-like states with an axial polarization in
ferroelectrics nanoparticles of various geometry. At that this work reveals the critical influence
of the flexoelectric coefficients sign and anisotropy on the appearance and properties of the axial
polarization, and, most important, on the chirality of a ferroelectric vortex. Qualitatively, both
works, [39] and this one, illustrate that flexoelectricity can change the chiral state of a
polarization texture, and this work studies the behavior of a topological index (in fact a skyrmion
number) that quantifies the change (see Fig. 3g).
       The main features characterizing polarization structures stabilized by DMI-type
interactions are their breaking of chiral symmetry and their incommensurability, i.e., a long-
period modulation in space that is unrelated to the crystalline lattice parameter. The appearance
of such chiral incommensurate phases can generally be attributed to specific energy terms in the
Landau-Ginzburg potential, known as Lifshitz invariants [49, 88]. Only a few ferroelectrics have
crystalline structures whose symmetry allows such Lifshitz invariants; therefore, an interaction
directly analogous to the magnetic DMI is generally not found in ferroelectrics. However,
although not identical in its mathematical form, the energy density due to the flexoelectric
coupling [23] is similar to a DMI-type energy term related to a linear Lifshitz invariant.
Accordingly, we argue that the flexoelectric coupling can lead to polarization states with
properties similar to those generated by a DMI-type interaction. Such a connection between
flexoelectric coupling, Lifshitz invariants, and DMI has been discussed before in the case of

                                                14
liquid crystals [89]. It was found that flexoelectricity in liquid crystals can play a central role in
the development of modulated phases that are analogous to those known from chiral
ferromagnets [90]. Our study shows that –similar to liquid crystals, where elastic strains fields
couple to electric fields– the flexoelectric effect through which strain fields couple to the electric
polarization field can lead to comparable modulated phases with chiral properties in a
ferroelectric nanoparticle.


                              V. SUMMARY AND CONCLUSIONS
Using FEM simulations based on the phenomenological LGD approach alongside electrostatic
equations and elasticity theory, we identify a characteristic polarization structure developing
between two oppositely oriented axial domains located near the cylinder ends. This polar
structure, which we named “flexon”, displays chiral features that are connected to the
flexoelectric coupling. In the azimuthal plane, the flexon polarization forms a localized chiral
structure resembling a meron, or a vortex with a central kernel. Analytical calculations and FEM
prove that the flexon axial polarization, and thus its chirality, switches upon a change of the sign
of the flexoelectric coefficients. We also observe that the anisotropy of the flexoelectric coupling
critically influences the flexon formation and the related domain morphology. This observation
corroborates the link between chirality and flexocoupling, and it identifies the flexoelectric effect
as the driving force stabilizing these structures.
       While in magnetic systems with strong DMI, similar localized chiral structures have been
reported [71], the polarization state discussed here is formed without any ferroelectric
counterpart of the DMI [46]. We recall that, like the DMI, the flexoelectric coupling is derived
as a Lifshitz invariant [Eq. (1f)] in the context of the Landau theory of phase transitions [22],
and that such linear Lifshitz invariants generally play a key role in the formation of helical
structures [49, 88]. The fact that both the DMI and the flexoelectric stabilize structures with a
specific chirality demonstrates an analogy between these two interactions which appears to have
been overlooked in the literature of ferroelectric solids. An important difference compared to the
classical DMI is that the flexoelectric coupling is ubiquitous in ferroelectrics, whereas the
ferroelectric DMI is forbidden by symmetry in most material types. Therefore, a chiral
interaction mediated by the flexoelectric effect can potentially be found in all ferroelectrics. The
coupling of the electric polarization and elastic strain gradients could thus be a much more
commonly accessible alternative interaction for the formation of chiral and achiral structures [75,
76]. This coupling could also open the possibility of generating and dissolving chiral polarization
states through strain engineering [91].

                                                 15
        We predict that the pronounced flexon-type polarization distribution with two axial
counter domains exists in the temperature range 290 K < 𝑇 < 340 K. The relatively wide
temperature range (about 50 K) corresponding to the stability or meta-stability of the flexon-type
polarization distribution give us the hope that the flexons can be observed experimentally.
However, the analysis of the hysteresis loops leads to the conclusion that flexons and other
domain configurations cannot be resolved from macroscopic measurements of the average
polarization in a homogeneous electric field. We anticipate that flexons can be reliably observed,
e.g., by the local methods using a strong gradient of electric field, such as PFM, which gives us
the information about the distribution of polarization with a nanoscale resolution.


        Acknowledgements. A.N.M. acknowledges EOARD project 9IOE063 and related
STCU partner project P751. R.H. and S.C.-H. acknowledge funding from the French National
Research Agency through contract ANR-18-CE92-0052 “TOPELEC”. V.Y.R. acknowledges the
support of COST Action CA17139. A portion of FEM was conducted at the Center for
Nanophase Materials Sciences, which is a DOE Office of Science User Facility (CNMS Proposal
ID: CNMS2021-B-00843).

                                           REFERENCES

1       J. F. Scott, Applications of modern ferroelectrics. Science 315, 954 (2007).
2       K. M. Rabe, C. H. Ahn, and J.-M. Triscone, Editors, Physics of Ferroelectrics, 1st ed.
(Springer Berlin Heidelberg, 2007).
3       A. K. Tagantsev, L. E. Cross, and J. Fousek, Domains in Ferroic Crystals and Thin Films, 1st
ed. (Springer New York, NY, 2010).
4       S. V. Kalinin, Y. Kim, D. Fong, and A. N. Morozovska. Surface-screening mechanisms in
ferroelectric thin films and their effect on polarization dynamics and domain structures, Rep. Prog.
Phys. 81, 036502 (2018).
5       C. T. Nelson, B. Winchester, Y. Zhang, S. J. Kim, A. Melville, C. Adamo, C. M. Folkman, S.
H. Baek, C. B. Eom, D. G. Schlom, L. Q. Chen, and X. Pan. Spontaneous vortex nanodomain arrays at
ferroelectric heterointerfaces, Nano Lett. 11, 828 (2011).
6       C.-L. Jia, K. W. Urban, M. Alexe, D. Hesse, and I. Vrejoiu. Direct observation of continuous
electric dipole rotation in flux-closure domains in ferroelectric Pb (Zr, Ti)O3, Science 331, 1420 (2011).
7       Y. L. Tang, Y. L. Zhu, X. L. Ma, A. Y. Borisevich, A. N. Morozovska, E. A. Eliseev, W. Y.
Wang, Y. J. Wang, Y. B. Xu, Z. D. Zhang, and S. J. Pennycook. Observation of a periodic array of flux-
closure quadrants in strained ferroelectric PbTiO3 films, Science 348, 547 (2015).
8       S. Lin, T. Lü, C. Jin, and X. Wang. Size effect on the dielectric properties of BaTiO 3

                                                    16
nanoceramics in a modified Ginsburg-Landau-Devonshire thermodynamic theory. Phys. Rev. B 74,
134115 (2006).

9    Yu. A. Barnakov, I. U. Idehenre, S. A. Basun, T. A. Tyson, and D. R. Evans. Uncovering the Mystery
of Ferroelectricity in Zero Dimensional Nanoparticles. Royal Society of Chemistry, Nanoscale Adv. 1,
664 (2019).
10      E. A. Eliseev, A. V. Semchenko, Y. M. Fomichov, M. D. Glinchuk, V. V. Sidsky, V. V. Kolos,
Yu M. Pleskachevsky, M. V. Silibin, N. V. Morozovsky, and A. N. Morozovska. Surface and finite size
effects impact on the phase diagrams, polar, and dielectric properties of (Sr, Bi)Ta 2O9 ferroelectric
nanoparticles. J. Appl. Phys. 119, 204104 (2016).

11      E. A. Eliseev, Y. M. Fomichov, S. V. Kalinin, Y. M. Vysochanskii, P. Maksymovich and A. N.
Morozovska. Labyrinthine domains in ferroelectric nanoparticles: Manifestation of a gradient-induced
morphological phase transition, Phys. Rev. B 98, 054101 (2018).
12      A. N. Morozovska, Y. M. Fomichov, P. Maksymovych, Y. M. Vysochanskii, and E. A. Eliseev.
Analytical description of domain morphology and phase diagrams of ferroelectric nanoparticles. Acta
Mater. 160, 109 (2018).

13      A. N. Morozovska, E. A. Eliseev, R. Hertel, Y. M. Fomichov, V. Tulaidan, V. Yu. Reshetnyak,
and D. R. Evans. Electric Field Control of Three-Dimensional Vortex States in Core-Shell Ferroelectric
Nanoparticles. Acta Materialia, 200, 256 (2020).

14      A. N. Morozovska, E. A. Eliseev, Y. M. Fomichov, Y. M. Vysochanskii, V. Yu. Reshetnyak,
and D. R. Evans. Controlling the domain structure of ferroelectric nanoparticles using tunable shells.
Acta Materialia, 183, 36 (2020).

15      A.N. Morozovska, E.A. Eliseev, M.D. Glinchuk. Ferroelectricity enhancement in confined
nanorods: Direct variational method, Phys. Rev. B. 73, № 21, 214106 (2006).
16      A. N. Morozovska, M. D. Glinchuk, E. A. Eliseev. Phase transitions induced by confinement of
ferroic nanoparticles. Phys. Rev. B 76, 014102 (2007).

17      I. S. Vorotiahin, E. A. Eliseev, Q. Li, S. V. Kalinin, Y. A. Genenko and A. N. Morozovska.
Tuning the Polar States of Ferroelectric Films via Surface Charges and Flexoelectricity, Acta Materialia
137, 85 (2017).
18      E. A. Eliseev, I. S. Vorotiahin, Y. M. Fomichov, M. D. Glinchuk, S. V. Kalinin, Y. A.
Genenko, and A. N. Morozovska. Defect driven flexo-chemical coupling in thin ferroelectric films,
Phys. Rev. B 97, 024102 (2018).
19      G. Catalan, B. Noheda, J. McAneney, L. J. Sinnamon, J. M. Gregg, Strain gradients in epitaxial
ferroelectrics, Phys. Rev B 72, 020102 (2005).
20      M. S. Majdoub, P. Sharma, and T. Cagin. Enhanced size-dependent piezoelectricity and
elasticity in nanostructures due to the flexoelectric effect, Phys. Rev B 77, 125424 (2008).


                                                    17
21        F. Ahmadpoor, P. Sharma, Flexoelectricity in two-dimensional crystalline and biological
membranes, Nanoscale 7, 16555 (2015).
22        E. A. Eliseev, A. N. Morozovska, M. D. Glinchuk, and R. Blinc. Spontaneous
flexoelectric/flexomagnetic effect in nanoferroics. Phys. Rev. B 79, 165433, (2009).
23        Flexoelectricity in Solids: From Theory to Applications. Ed. by A. K. Tagantsev and P. V.
Yudin, World Scientific (2016).
24        A. N. Morozovska, E. A. Eliseev, Y. A. Genenko, I. S. Vorotiahin, M. V. Silibin, Ye Cao, Y.
Kim, M. D. Glinchuk, and S. V. Kalinin. Flexocoupling impact on the size effects of piezo- response
and conductance in mixed-type ferroelectrics-semiconductors under applied pressure. Phys. Rev. B 94,
174101 (2016).

25        A. N. Morozovska, E. A. Eliseev, C. M. Scherbakov, and Y. M. Vysochanskii. The influence
of elastic strain gradient on the upper limit of flexocoupling strength, spatially-modulated phases and
soft phonon dispersion in ferroics. Phys. Rev. B 94, 174112 (2016).

26        B. Wang, Y. Gu, S. Zhang, L.-Q. Chen. Flexoelectricity in solids: Progress, challenges, and
perspectives. Progress in Materials Science 106, 100570 (2019).
27        A. F. Devonshire, Theory of ferroelectrics, Adv. Phys. 3, 85 (1954).
28        A. Gruverman, M. Alexe, and D. Meier. Piezoresponse force microscopy and nanoferroic
phenomena, Nat. Comm. 10, 1 (2019).
29        J.-J. Wang, B. Wang, and L.-Q. Chen. Understanding, Predicting, and Designing Ferroelectric
Domain Structures and Switching Guided by the Phase-Field Method, Ann. Rev. Mater. Res. 49, 127
(2019).
30        R. G. P. McQuaid, L. J. McGilly, P. Sharma, A. Gruverman, and J. M. Gregg. Mesoscale flux-
closure domain formation in single-crystal BaTiO3, Nat. Commun. 2, 404 (2011).
31        Q. Zhang, L. Xie, G. Liu, S. Prokhorenko, Y. Nahas, X. Pan, L. Bellaiche, A. Gruverman, N.
Valanoor, A. Gruverman, and N. Valanoor. Nanoscale bubble domains and topological transitions in
ultrathin ferroelectric films, Adv. Mater. 29, 1702375 (2017).
32        E. A. Eliseev, A. N. Morozovska, C. T. Nelson, and S. V. Kalinin. Intrinsic structural
instabilities of domain walls driven by gradient couplings: meandering anferrodistortive-ferroelectric
domain walls in BiFeO3, Phys. Rev. B 99, 014112 (2019).
33        M. J. Han, E. A. Eliseev, A. N. Morozovska, Y. L. Zhu, Y. L. Tang, Y. J. Wang, X. W. Guo,
X. L. Ma. Mapping gradient-driven morphological phase transition at the conductive domain walls of
strained multiferroic films, Phys. Rev. B 100, 104109 (2019).
34        Y. Nahas, S. Prokhorenko, J. Fischer, B. Xu, C. Carrétéro, S. Prosandeev, M. Bibes, S. Fusil,
B. Dkhil, V. Garcia, and L. Bellaiche. Inverse transition of labyrinthine domain patterns in ferroelectric
thin films, Nature 577, 47 (2020).



                                                    18
35        S. Cherifi-Hertel, H. Bulou, R. Hertel, G. Taupier, K. D. Dorkenoo, C. Andreas, J. Guyonnet, I.
Gaponenko, K. Gallo, and P. Paruch, Non-ising and chiral ferroelectric domain walls revealed by
nonlinear optical microscopy. Nat. Commun. 8, 15768 (2017).
36        B. J. Rodriguez, X. S. Gao, L. F. Liu, W. Lee, I. I. Naumov, A. M. Bratkovsky, D. Hesse, and
M. Alexe. Vortex polarization states in nanoscale ferroelectric arrays, Nano Lett. 9, 1127 (2009).
37        N. Balke, B. Winchester, W. Ren, Y. H. Chu, A. N. Morozovska, E. A. Eliseev, M. Huijben, R.
K. Vasudevan, P. Maksymovych, J. Britson, S. Jesse, I. Kornev, R. Ramesh, L. Bellaiche, L. Q. Chen,
and S. V. Kalinin. Enhanced electric conductivity at ferroelectric vortex cores in BiFeO3, Nat. Phys. 8,
81 (2012).
38        A. K. Yadav, C. T. Nelson, S. L. Hsu, Z. Hong, J. D. Clarkson, C. M. Schlepütz, A. R.
Damodaran, P. Shafer, E. Arenholz, L. R. Dedon, D. Chen, A. Vishwanath, A. M. Minor, L. Q. Chen, J.
F. Scott, L. W. Martin, and R. Ramesh. Observation of polar vortices in oxide superlattices, Nature 530,
198 (2016).
39        C. Liu, J. Wang, G. Xu, Ma. Kamlah, and T.-Y. Zhang. An isogeometric approach to
flexoelectric effect in ferroelectric materials. International Journal of Solids and Structures 162, 198
(2019).
40        Y. Li, K. Chu, C. Liu, P. Jiang, K. Qu, P. Gao, J. Wang, F. Ren, Q. Sun, L. Chen, and J. Li.
Superelastic oxide micropillars enabled by surface tension–modulated 90° domain switching with
excellent fatigue resistance, PNAS 118, e2025255118 (2021).
41        S. Das, Y. L. Tang, Z. Hong, M. A. P. P. Gonçalves, M. R. McCarter, C. Klewe, K. X. Nguyen,
F. Gómez-Ortiz, P. Shafer, E. Arenholz, V. A. Stoica, S.-L. Hsu, B. Wang, C. Ophus, J.F. Liu, C.T.
Nelson, S. Saremi, B. Prasad, A.B. Mei, D.G. Schlom, J. Íñiguez, P. García-Fernández, D.A. Muller,
L.Q. Chen, J. Junquera, L.W. Martin, and R. Ramesh. Observation of room-temperature polar
skyrmions, Nature 568, 368 (2019).
42        J. Hlinka, and P. Ondrejkovic. Skyrmions in ferroelectric materials. Solid State Physics, 70, 143
(2019), Chapter 4 in “Recent Advances in Topological Ferroics and Their Dynamics” Edited by Robert
L. Stamps and Helmut Schultheiss. Academic Press (2019).
43        G. Finocchio, F. Büttner, R. Tomasello, M. Carpentieri, and M. Kläui. Magnetic skyrmions:
from fundamental to applications, J. Phys. D:Appl. Phys. 49, 423001 (2016).
44        I. Dzyaloshinsky, A thermodynamic theory of “weak” ferromagnetism of antiferromagnetics. J.
Phys. Chem. Solids 4, 241 (1958).
45        T. Moriya, Anisotropic superexchange interaction and weak ferromagnetism. Phys. Rev. 120,
91 (1960).
46        H. J. Zhao, P. Chen, S. Prosandeev, S. Artyukhin, and L. Bellaiche. Dzyaloshinskii–Moriya-
like interaction in ferroelectrics and antiferroelectrics, Nat. Mater. 20, 341 (2021).
47        K. C. Erb, and J. Hlinka. Vector, bidirector, and Bloch skyrmion phases induced by structural
crystallographic symmetry breaking, Phys. Rev. B 102, 024110 (2020).
                                                     19
48        A. N. Bogdanov, and D. A. Yablonskii. Thermodynamically stable “vortices” in magnetically
ordered crystals, The mixed state of magnets. Zh. Eksp. Teor. Fiz 95, 178 (1989).
49        A. Bogdanov. On the stability of localized states in nonlinear field models with Lifshitz
invariants, Journal of Experimental and Theoretical Physics Letters 68, 317 (1998).
50        B. A. Strukov and A.P. Levanyuk, Ferroelectric Phenomena in Crystals, Springer 1998.
51        E. A. Eliseev, A. N. Morozovska, R. Hertel, H. V. Shevliakova, Y. M. Fomichov, V. Yu.
Reshetnyak, and D. R. Evans. Flexo-Elastic Control Factors of Domain Morphology in Core-Shell
Ferroelectric Nanoparticles: Soft and Rigid Shells. Acta Materialia, 212, 116889 (2021).
52        W. Ma. Surface tension and Curie temperature in ferroelectric nanowires and nanodots. Appl.
Phys. A 96, 915 (2009).

53        J. J. Wang, E. A. Eliseev, X. Q. Ma, P. P. Wu, A. N. Morozovska, and Long-Qing Chen. Strain
effect on phase transitions of BaTiO3 nanowires, Acta Materialia 59, 7189 (2011).
54        J. J. Wang, X. Q. Ma, Q. Li, J. Britson, Long-Qing Chen. Phase transitions and domain structures
of ferroelectric nanoparticles: Phase field model incorporating strong elastic and dielectric
inhomogeneity, Acta Mater. 61, 7591 (2013).

55        H. Huang, C. Q. Sun, P. Hing. Surface bond contraction and its effect on the nanometric sized
lead zirconate titanate. J. Phys.: Condens. Matter 12, L127 (2000).

56        H. Huang, C. Q. Sun, Z. Tianshu, P. Hing. Grain-size effect on ferroelectric Pb(Zr1−xTix)O3 solid
solutions induced by surface bond contraction. Phys. Rev. B 63, 184112 (2001).

57        L. D. Landau, and I. M. Khalatnikov. On the anomalous absorption of sound near a second
order phase transition point. In Dokl. Akad. Nauk SSSR, 96, 469 (1954).

58        J. Hlinka. Mobility of Ferroelectric Domain Walls in Barium Titanate. Ferroelectrics 349, 49
(2007).

59        S.P. Timoshenko, J.N. Goodier. Theory of Elasticity. McGraw-Hill, N. Y., 1970.

60        A. K. Tagantsev, G. Gerra, and N. Setter. Short-range and long-range contributions to the size
effect in metal-ferroelectric-metal heterostructures. Phys. Rev. B 77, 174111 (2008).

61        M. Stengel and N. A. Spaldin, Origin of the dielectric dead layer in nanoscale capacitors,
Nature (London) 443, 679 (2006).

62        M. Stengel, D. Vanderbilt, and N. A. Spaldin. First-principles modeling of ferroelectric
capacitors via constrained displacement field calculations. Phys. Rev. B 80, 224110 (2009).

63        See Supplementary Materials for calculation details [URL will be provided by Publisher]
64        J. Hlinka and P. Márton. Phenomenological model of 90-degree domain wall in BaTiO3 type
ferroelectrics. Phys. Rev. B 74, 104104 (2006).



                                                    20
65        A.J. Bell. Phenomenologically derived electric field-temperature phase diagrams and
piezoelectric coefficients for single crystal barium titanate under fields along different axes, J. Appl.
Phys. 89, 3907 (2001).

66        D. Berlincourt, and H. Jaffe. Elastic and piezoelectric coefficients of single-crystal barium
titanate. Phys. Rev. 111, 143 (1958).

67        I. Ponomareva, A.K. Tagantsev, L. Bellaiche. Finite-temperature flexoelectricity in
ferroelectric thin films from first principles, Phys. Rev. B 85, 104101 (2012).

68        G. Shirane, and A. Takeda. Transition energy and volume change at three transitions in barium
titanate, J. Phys. Soc. Jap. 7, 1 (1952).

69        H. D. Megaw. Temperature changes in the crystal structure of barium titanium oxide. Proc. R.
Soc. Lond. A. 189, 261 (1947).

70        K. Everschor-Sitte, J. Masell, R. M. Reeve, and M. Kläui. Perspective: Magnetic skyrmions—
Overview of recent progress in an active research field. J. Appl. Phys. 124, 240901 (2018).
71        F. N. Rybakov, A. B. Borisov, S. Blügel, and N. S. Kiselev. New type of stable particle-like
states in chiral magnets, Phys. Rev. Lett. 115, 117201 (2015).
72        S. A. Pathak, and R. Hertel. Three-dimensional chiral magnetization structures in FeGe
nanospheres, Phys. Rev. B 103, 104414 (2021).
73        H. B. Braun. Nucleation in ferromagnetic nanowires—magnetostatics and topology, J. Appl.
Phys. 85, 6172 (1999).
74        R. Hertel and J. Kirschner. Magnetic drops in a soft-magnetic cylinder, Journal of Magnetism
and Magnetic Materials 278, L291 (2004).
75        P. V. Yudin, A. K. Tagantsev, E. A. Eliseev, A. N. Morozovska and N. Setter. Bichiral
structure of ferroelectric domain walls driven by flexoelectricity, Phys. Rev. B 86, 134102 (2012).
76        E. A. Eliseev, P. V. Yudin, S. V. Kalinin, N. Setter, A. K. Tagantsev and A. N. Morozovska.
Structural phase transitions and electronic phenomena at 180-degree domain walls in rhombohedral
BaTiO3, Phys. Rev. B 87, 054111 (2013).
77        Y. Gu, M. Li, A. N. Morozovska, Yi Wang, E. A. Eliseev, V. Gopalan, and L.-Q. Chen. Non-
Ising Character of a Ferroelectric Wall Arises from a Flexoelectric Effect, Phys. Rev. B 89, 174111
(2014).
78        We define an achiral structure as one that is equal to its mirror image, and a chiral structure as
one that displays a handedness such that it is distinctly different from its mirror image. Systems governed
by chiral-symmetry breaking interactions, such as the DMI, favor the formation of chiral structures with
one specific handedness. Those systems are sometimes called homochiral.
79        J. Roller, A. Laganapan, J.-M. Meijer, M. Fuchs, and A. Zumbusch. Observation of liquid glass
in suspensions of ellipsoidal colloids, Proceedings of the National Academy of Sciences, 118, no. 3
(2021).
                                                     21
80      S. V. Kalinin, E. Karapetian, and M. Kachanov, Nanoelectromechanics of piezoresponse force
microscopy, Phys. Rev. B 70, 184101 (2004).
81      D. A. Scrymgeour and V. Gopalan. Nanoscale piezoelectric response across a single
antiparallel ferroelectric domain wall, Phys. Rev. B 72, 024103 (2005).
82      S. Cherifi-Hertel, C. Voulot, U. Acevedo-Salas, Y. Zhang, O. Crégut, K. D, Dorkenoo, and R.
Hertel. Shedding light on non-Ising polar domain walls: Insight from second harmonic generation
microscopy and polarimetry analysis, J. Appl. Phys. 129, 081101 (2021).
83      G. Bautista, J. Mäkitalo, Ya Chen, V. Dhaka, M. Grasso, L. Karvonen, H. Jiang et al. Second-
harmonic generation imaging of semiconductor nanowires with focused vector beams, Nano Lett. 15,
1564 (2015).
84      M. Timofeeva, A. Bouravleuv, G. Cirlin, I. Shtrom, I. Soshnikov, M. Reig Escalé, A.
Sergeyev, and R. Grange. Polar second-harmonic imaging to resolve pure and mixed crystal phases
along GaAs nanowires, Nano Lett. 16, 6290 (2016).
85      P. Shafer, P. García-Fernández, P. Aguado-Puente, A. R. Damodaran, A. K. Yadav, C.T.
Nelson, S. L. Hsu, J. C. Wojdeł, J. Íñiguez, L. W. Martin, and E. Arenholz, Emergent chirality in the
electric polarization texture of titanate superlattices. Proceedings of the National Academy of Sciences,
115, 915 (2018).
86      S. W. Lovesey, G. van der Laan. Resonant x-ray diffraction from chiral electric-polarization
structures, Phys. Rev. B 98, 155410 (2018).
87      J. Y. Chauleau, T. Chirac, S. Fusil, V. Garcia, W. Akhtar, J. Tranchida, P. Thibaudeau, I.
Gross, C. Blouzon, A. Finco, and M.Bibes. Electric and antiferromagnetic chiral textures at multiferroic
domain walls, Nature Materials, 19, 386 (2020).
88      Y. A. Izyumov. Modulated, or long-periodic, magnetic structures of crystals, Sov. Phys. Usp.
27, 845 (1984).
89      A. Sparavigna, A. Strigazzi, and A. Zvezdin. Electric-field effects on the spin-density wave in
magnetic ferroelectrics, Phys. Rev. B 50, 2953 (1994).
90      A. Sparavigna. Role of Lifshitz invariants in liquid crystals, Materials, 2, 674 (2009).
91      A. R Damodaran, J. C. Agar, S. Pandya, Z. Chen, L. Dedon, R. Xu, B. Apgar, S. Saremi, and
L. W. Martin. New modalities of strain-control of ferroelectric thin films, J. Phys.: Condens. Matter 28,
263001 (2016).




                                                   22
                                     Supplementary Materials to

“Chiral Polarization Textures Induced by the Flexoelectric Effect in Ferroelectric
                                                Nanocylinders”

           APPENDIX A. Mathematical Formulation of the Problem and FEM Details
                             A. Mathematical Formulation of the Problem

We use the Landau-Ginzburg-Devonshire (LGD) approach combined with electrostatic equations,
because this method has proven to be successful in establishing the physical origin of anomalies in
phase diagrams, determining polar and dielectric properties of ferroelectric nanoparticles [1, 2], and
calculating the changes of their domain structure morphology with size reduction [3, 4]. The LGD
approach allows for the consideration of various size and surface effects, such as correlation effects
and depolarization fields arising in the case of incomplete polarization screening [5], surface bond
contraction [6, 7], and intrinsic surface stresses and strains [8, 9, 10].
       The LGD free energy functional G additively includes a Landau expansion on powers of 2-4-6
of the polarization (𝑃𝑖 ), 𝐺𝐿𝑎𝑛𝑑𝑎𝑢 ; a polarization gradient energy contribution, 𝐺𝑔𝑟𝑎𝑑 ; an electrostatic
contribution, 𝐺𝑒𝑙 ; the elastic, electrostriction, flexoelectric contributions, 𝐺𝑒𝑠+𝑓𝑙𝑒𝑥𝑜 ; and a surface
energy, 𝐺𝑆 . It has the form [3, 10, 11]:
                           𝐺 = 𝐺𝐿𝑎𝑛𝑑𝑎𝑢 + 𝐺𝑔𝑟𝑎𝑑 + 𝐺𝑒𝑙 + 𝐺𝑒𝑠+𝑓𝑙𝑒𝑥𝑜 + 𝐺𝑆 ,                                         (A.1a)
                         𝐺𝐿𝑎𝑛𝑑𝑎𝑢 = ∫𝑉𝑐 𝑑3 𝑟 [𝑎𝑖 𝑃𝑖2 + 𝑎𝑖𝑗 𝑃𝑖2 𝑃𝑗2 + 𝑎𝑖𝑗𝑘 𝑃𝑖2 𝑃𝑗2 𝑃𝑘2 ],                         (A.1b)
                                                                    𝑔   𝜕𝑃 𝜕𝑃
                                               𝐺𝑔𝑟𝑎𝑑 = ∫𝑉𝑐 𝑑 3 𝑟 𝑖𝑗𝑘𝑙 𝑖  𝑘
                                                                           ,                                    (A.1c)
                                                                  2 𝜕𝑥 𝜕𝑥𝑗      𝑙

                                                 𝜀 𝜀            𝜀                      𝜀
                   𝐺𝑒𝑙 = − ∫𝑉𝑐 𝑑3 𝑟 (𝑃𝑖 𝐸𝑖 + 02 𝑏 𝐸𝑖 𝐸𝑖 ) − 20 ∫𝑉𝑠 𝜀𝑖𝑗𝑆 𝐸𝑖 𝐸𝑗 𝑑 3 𝑟 − 20 ∫𝑉𝑜 𝜀𝑖𝑗
                                                                                              𝑒
                                                                                                 𝐸𝑖 𝐸𝑗 𝑑 3 𝑟,   (A.1d)

                                           𝑠                                               𝜕𝑃       𝜕𝜎
              𝐺𝑒𝑠+𝑓𝑙𝑒𝑥𝑜 = − ∫𝑉𝑐 𝑑3 𝑟 ( 𝑖𝑗𝑘𝑙 𝜎𝑖𝑗 𝜎𝑘𝑙 + 𝑄𝑖𝑗𝑘𝑙 𝜎𝑖𝑗 𝑃𝑘 𝑃𝑙 + 𝐹𝑖𝑗𝑘𝑙 (𝜎𝑖𝑗 𝜕𝑥𝑘 − 𝑃𝑘 𝜕𝑥𝑖𝑗 ))             (A.1e)
                                        2                                                       𝑙        𝑙

                                                   1          (𝑆)
                                           𝐺𝑆 = 2 ∫𝑆 𝑑 2 𝑟 𝑎𝑖𝑗 𝑃𝑖 𝑃𝑗 .                                          (A.1f)

Here 𝑉𝑐 and 𝑉𝑠 are the core and shell volume, respectively. The coefficient 𝑎𝑖 linearly depends on
temperature T, 𝑎𝑖 (𝑇) = 𝛼 𝑇 [𝑇 − 𝑇𝐶 ], where 𝛼 𝑇 is the inverse Curie-Weiss constant and 𝑇𝐶 is the
ferroelectric Curie temperature renormalized by electrostriction and surface tension. Tensor
components 𝑎𝑖𝑗 are regarded as temperature-independent. The tensor 𝑎𝑖𝑗 is positively defined if the
ferroelectric material undergoes a second order transition to the paraelectric phase and negative
otherwise. The higher nonlinear tensor 𝑎𝑖𝑗𝑘 and the gradient coefficients tensor 𝑔𝑖𝑗𝑘𝑙 are positively
defined and regarded as temperature-independent. The following designations are used in Eq.(A.1e):


                                                          1
𝜎𝑖𝑗 is the stress tensor, 𝑠𝑖𝑗𝑘𝑙 is the elastic compliances tensor, 𝑄𝑖𝑗𝑘𝑙 is the electrostriction tensor, and
𝐹𝑖𝑗𝑘𝑙 is the flexoelectric tensor.
        For cubic (m3m) point symmetry group of the parent phase the explicit form of the “half”
Lifshitz invariant for the flexoeffect is
                                                                     𝜕𝑃                                      𝜕𝑃
                ∆𝐺𝑓𝑙𝑒𝑥𝑜 = [𝜎11 𝐹11 + (𝜎22 + 𝜎33 )𝐹12 ] 𝜕𝑥1 + [𝜎22 𝐹11 + (𝜎11 + 𝜎33 )𝐹12 ] 𝜕𝑥2 + [𝜎33 𝐹11 +
                                                                          1                                          2

                                  𝜕𝑃3                      𝜕𝑃    𝜕𝑃                𝜕𝑃        𝜕𝑃        𝜕𝑃        𝜕𝑃
              (𝜎11 + 𝜎22 )𝐹12 ]         + 𝐹44 [𝜎12 (𝜕𝑥1 + 𝜕𝑥2 ) + 𝜎13 (𝜕𝑥1 + 𝜕𝑥3 ) + 𝜎23 (𝜕𝑥2 + 𝜕𝑥3 )]                                 (A.2)
                                  𝜕𝑥3                        2       1              3         1         3                2


      Allowing for the Khalatnikov mechanism of polarization relaxation [12], minimization of the
free energy (A.1) with respect to polarization leads to three coupled time-dependent Euler-Lagrange
                                                                              𝛿𝐺        𝜕𝑃
equations for polarization components inside the core, 𝛿𝑃 = −𝛤 𝜕𝑡𝑖 , where 𝑖 = 1, 2, 3. The explicit
                                                                               𝑖

form of the equations for a ferroelectric crystal with m3m parent symmetry is:

         𝜕𝑃
       𝛤 𝜕𝑡1 + 2𝑃1 (𝑎1 − 𝑄12 (𝜎22 + 𝜎33 ) − 𝑄11 𝜎11 ) − 𝑄44 (𝜎12 𝑃2 + 𝜎13 𝑃3 ) + 4𝑎11 𝑃13 + 2𝑎12 𝑃1 (𝑃22 +
                                                                                                                                      𝜕2𝑃
                 𝑃32 ) + 6𝑎111 𝑃15 + 2𝑎112 𝑃1 (𝑃24 + 2𝑃12 𝑃22 + 𝑃34 + 2𝑃12 𝑃32 ) + 2𝑎123 𝑃1 𝑃22 𝑃32 − 𝑔11 𝜕𝑥 21 −
                                                                                                                                        1

                                     𝜕2 𝑃1       𝜕2 𝑃1               𝜕𝜎             𝜕𝜎        𝜕𝜎            𝜕𝜎               𝜕𝜎
                            𝑔44 (            +           ) = −𝐹11 𝜕𝑥11 − 𝐹12 ( 𝜕𝑥22 + 𝜕𝑥33 ) − 𝐹44 ( 𝜕𝑥12 + 𝜕𝑥13 ) + 𝐸1
                                     𝜕𝑥22        𝜕𝑥32                     1              1         1             2                3


                                                                                                                                      (A.3a)

         𝜕𝑃
      𝛤 𝜕𝑡2 + 2𝑃2 (𝑎1 − 𝑄12 (𝜎11 + 𝜎33 ) − 𝑄11 𝜎22 ) − 𝑄44 (𝜎12 𝑃1 + 𝜎23 𝑃3 ) + 4𝑎11 𝑃23 + 2𝑎12 𝑃2 (𝑃12 +
                                                                                                                                      𝜕2𝑃
                𝑃32 ) + 6𝑎111 𝑃25 + 2𝑎112 𝑃2 (𝑃14 + 2𝑃22 𝑃12 + 𝑃34 + 2𝑃22 𝑃32 ) + 2𝑎123 𝑃2 𝑃12 𝑃32 − 𝑔11 𝜕𝑥 22 −
                                                                                                                                        2

                                     𝜕2 𝑃2       𝜕2 𝑃2               𝜕𝜎            𝜕𝜎         𝜕𝜎            𝜕𝜎               𝜕𝜎
                            𝑔44 (            +           ) = −𝐹11 𝜕𝑥22 − 𝐹12 ( 𝜕𝑥11 + 𝜕𝑥33 ) − 𝐹44 ( 𝜕𝑥12 + 𝜕𝑥23 ) + 𝐸2
                                     𝜕𝑥12        𝜕𝑥32                     2              2         2             1                3


                                                                                                                                      (A.3b)

         𝜕𝑃
      𝛤 𝜕𝑡3 + 2𝑃3 (𝑎1 − 𝑄12 (𝜎11 + 𝜎22 ) − 𝑄11 𝜎33 ) − 𝑄44 (𝜎13 𝑃1 + 𝜎23 𝑃2 ) + 4𝑎11 𝑃33 + 2𝑎12 𝑃3 (𝑃12 +
                                                                                                                                      𝜕2𝑃
                𝑃22 ) + 6𝑎111 𝑃35 + 2𝑎112 𝑃3 (𝑃14 + 2𝑃32 𝑃12 + 𝑃24 + 2𝑃22 𝑃32 ) + 2𝑎123 𝑃3 𝑃12 𝑃22 − 𝑔11 𝜕𝑥 23 −
                                                                                                                                        3

                                     𝜕2 𝑃3       𝜕2 𝑃3               𝜕𝜎            𝜕𝜎         𝜕𝜎            𝜕𝜎               𝜕𝜎
                            𝑔44 (            +           ) = −𝐹11 𝜕х33 − 𝐹12 ( 𝜕х11 + 𝜕х22 ) − 𝐹44 ( 𝜕𝑥13 + 𝜕𝑥23 ) + 𝐸3
                                     𝜕𝑥12        𝜕𝑥22                     3              3         3             1                2


                                                                                                                                      (A.3c)

        The temperature-dependent Khalatnikov coefficient 𝛤 [13] determines the relaxation time of
the polarization 𝜏𝐾 = 𝛤 ⁄|𝛼|. Consequently, 𝜏𝐾 typically varies in the range (10-9 – 10-6) seconds for
                                                                            ′
temperatures far from TC. As argued by Hlinka et al. [14], we assumed that 𝑔44 = −𝑔12 in Eqs.(A.3).

                                                                 2
The boundary condition for polarization at the core-shell interface 𝑟 = 𝑅 accounts for the flexoelectric
effect:
                                           (𝑆)                   𝜕𝑃
                                      𝑎𝑖𝑗 𝑃𝑗 + (𝑔𝑖𝑗𝑘𝑙 𝜕𝑥𝑘 − 𝐹𝑘𝑙𝑖𝑗 𝜎𝑘𝑙 ) 𝑛𝑗 |                      =0                 (A.4)
                                                                      𝑙                     𝑟=𝑅

where n is the outer normal to the surface, i = 1, 2, 3. In our FEM studies, we use the so-called “natural”
                                                      (𝑆)
boundary conditions corresponding to 𝑎𝑖𝑗 = 0.
          The electric field components 𝐸𝑖 in Eq.(A.3) are derived from the electric potential 𝜑 in a
conventional way, 𝐸𝑖 = −𝜕𝜑⁄𝜕𝑥𝑖 . The potential 𝜑𝑓 satisfies the Poisson equation in the ferroelectric
cylinder (subscript "f"):
                              𝜕2       𝜕2         𝜕2              𝜕𝑃
                      𝜀0 𝜀𝑏 (𝜕𝑥 2 + 𝜕𝑥 2 + 𝜕𝑥 2 ) 𝜑𝑓 = 𝜕𝑥𝑖 ,                      𝑥12 + 𝑥22 ≤ 𝑅 ∩ 0 ≤ 𝑥3 ≤ ℎ,       (A.5a)
                                  1         2         3                   𝑖


          The electric potential 𝜑𝑒 in the external region outside the core-shell nanoparticle satisfies the
Laplace equation (subscript "e"):

                             𝜕2       𝜕2         𝜕2
                    𝜀0 𝜀𝑒 (𝜕𝑥 2 + 𝜕𝑥 2 + 𝜕𝑥 2) 𝜑𝑒 = 0,                        𝑥12 + 𝑥22 > 𝑅 ∪ 𝑥3 < 0 ∪ 𝑥3 > ℎ,      (A.5b)
                              1        2          3


          Equations (A.5) are supplemented with the continuity conditions for electric potential and linear
screening conditions for the normal components of the electric displacements at the cylinder surface S
[4]:
                                                                                                       𝜑
                                             (𝜑𝑒 − 𝜑𝑓 )|𝑆 = 0, 𝒏(𝑫𝑒 − 𝑫𝑓 )|𝑆 = − Λ𝑓 .                               (A.6a)

The boundary condition (A.6a) corresponds to the surface of the core covered by an ultrathin
semiconductor shell with an effective screening length Λ ≥1 nm [15, 16, 17]. Note that a screening
length greater than 0.1 nm leads to the domain formation in the core. The case Λ → ∞ corresponds to
an electrical open-circuit condition. We impose an electrical open-circuit condition at the cylinder ends
to make the vortex-type polarization energetically favorable. Either charges are absent or the applied
voltage is fixed at the boundaries of the computation region:

                     𝜕 𝜑𝑒                         𝜕 𝜑𝑒
                         𝑛𝑙 |    𝐿
                                      = 0,                𝑛𝑙 |        𝐿
                                                                          = 0, 𝜑𝑒 |𝑧=+𝐿 = 0, 𝜑𝑒 |𝑧=−𝐿 = 𝑉𝑒 .        (A.6b)
                      𝜕𝑥 𝑙    𝑥=±                 𝜕 𝑥𝑙       𝑦=±                        2                  2
                                 2                                    2


          Elastic equations of state follow from the variation of the energy (A.1e) with respect to elastic
          𝛿𝐺
stress, δ𝜎 = −𝑢𝑖𝑗 . In the oversimplified case
           𝑖𝑗


                                                                      𝜕𝑃
                        𝑠𝑖𝑗𝑘𝑙 𝜎𝑘𝑙 + 𝑄𝑖𝑗𝑘𝑙 𝑃𝑘 𝑃𝑙 + 𝐹𝑖𝑗𝑘𝑙 𝜕𝑥 𝑙 = 𝑢𝑖𝑗 ,                   0 < 𝑟 ≤ 𝑅,          0<𝑧≤ℎ,   (A.7a)
                                                                          𝑘




                                                                          3
                                                            𝜕𝑃
                     𝜎𝑖𝑗 = 𝑐𝑖𝑗𝑘𝑙 𝑢𝑘𝑙 − 𝑞𝑖𝑗𝑘𝑙 𝑃𝑘 𝑃𝑙 − 𝑓𝑖𝑗𝑘𝑙 𝜕𝑥 𝑙 ,   0 < 𝑟 ≤ 𝑅,        0<𝑧≤ℎ,                        (A.7b)
                                                               𝑘


where 𝑢𝑖𝑗 is the strain tensor components related to the displacement components 𝑈𝑖 in the following
way: 𝑢𝑖𝑗 = (𝜕𝑈𝑖 /𝜕𝑥𝑗 + 𝜕𝑈𝑗 /𝜕𝑥𝑖 )/2. For cubic (m3m) point symmetry group of the parent phase the
strain components are:

                                                                            𝜕𝑃                 𝜕𝑃          𝜕𝑃
       𝑢11 = 𝑠11 𝜎11 + 𝑠12 (𝜎22 + 𝜎33 ) + 𝑄11 𝑃12 + 𝑄12 (𝑃22 + 𝑃32 ) + 𝐹11 𝜕𝑥1 + 𝐹12 (𝜕𝑥2 + 𝜕𝑥3 ) (A.8a)
                                                                                 1                     2        3


                                                                            𝜕𝑃                 𝜕𝑃          𝜕𝑃
       𝑢22 = 𝑠11 𝜎22 + 𝑠12 (𝜎11 + 𝜎33 ) + 𝑄11 𝑃22 + 𝑄12 (𝑃12 + 𝑃32 ) + 𝐹11 𝜕𝑥2 + 𝐹12 (𝜕𝑥1 + 𝜕𝑥3 ) (A.8b)
                                                                                 2                     1        3


                                                                            𝜕𝑃                 𝜕𝑃          𝜕𝑃
      𝑢33 = 𝑠11 𝜎33 + 𝑠12 (𝜎11 + 𝜎22 ) + 𝑄11 𝑃32 + 𝑄12 (𝑃22 + 𝑃12 ) + 𝐹11 𝜕𝑥3 + 𝐹12 (𝜕𝑥1 + 𝜕𝑥2 )                    (A.8c)
                                                                                 3                     1    2


                                                                                     𝜕𝑃       𝜕𝑃
                                             𝑢12 = 𝑠44 𝜎12 + 𝑄44 𝑃1 𝑃2 + 𝐹44 (𝜕𝑥1 + 𝜕𝑥2 )                           (A.8d)
                                                                                      2        1


                                                                                     𝜕𝑃       𝜕𝑃
                                              𝑢13 = 𝑠44 𝜎13 + 𝑄44 𝑃1 𝑃3 + 𝐹44 (𝜕𝑥1 + 𝜕𝑥3 )                          (A.8e)
                                                                                          3        1


                                                                                     𝜕𝑃       𝜕𝑃
                                              𝑢23 = 𝑠44 𝜎23 + 𝑄44 𝑃3 𝑃2 + 𝐹44 (𝜕𝑥2 + 𝜕𝑥3 )                          (A.8f)
                                                                                          3        2


Equations (A.8) should be considered along with equations of mechanical equilibrium 𝜕𝜎𝑖𝑗 (𝒙)⁄𝜕𝑥𝑖 =
0 and compatibility equations 𝑒𝑖𝑘𝑙 𝑒𝑗𝑚𝑛 𝜕 2 𝑢𝑙𝑛 (𝒙)⁄𝜕𝑥𝑘 𝜕𝑥𝑚 = 0, which are equivalent to the
mechanical displacement vector Ui continuity [18]. The boundary conditions for elastic stresses are the
virtual absence of their normal components at the nanoparticle surface, as the ambient media is
regarded absolutely soft.

                                  B. Finite Element Modelling Details

       Electrical boundary conditions. We consider the case when the surface of the core is covered
by an elastically soft ultrathin (its thickness ∆𝑅~(1 − 4) nm) paraelectric or high-k semiconductor
shell with a screening length Λ~1 nm. The coverage can be artificial (e.g., a soft organic semiconductor
or vacancy-enriched SrTiO3) or natural, where in the latter case it would originate from the polarization
screening by surrounding media. Note that a screening length larger than 0.1 nm weakly effects the
core domain structure, in this case the screening acts as an electrical open-circuit condition. Thus, we
impose an electrical open-circuit condition at the cylinder ends to make the vortex-type polarization
energetically favorable.
       Initial conditions, shape, and gradient effects variability. We use a four 90-degree domain
configuration in the XY-plane with superimposed small random noise as an initial distribution of
polarization. These four domains determine the direction of the lateral polarization vorticity. When

                                                       4
using a purely random noise as the initial distribution of polarization, the domain structure relaxes to
structure resembling 180-degree domains in thin c+/c- films. This process occurs because the
depolarization field favors a polarization orientation along the z-axis of the elongated cylinder;
however, the vorticity of polarization components appears near the cylinder ends (an analog of the
flux-closure a-domains in thin films).
        FEM simulations are performed in COMSOL@MultiPhysics software, using electrostatics,
solid mechanics, and general math (PDE toolbox) modules. The size of the computational region is not
less than 4040160 nm3, and is commensurate with the cubic unit cell constant (about 0.4 nm) of
BaTiO3 at room temperature. The minimal size of a tetrahedral element in a mesh with fine
discretization is equal to the unit cell size, 0.4 nm, the maximal size is (0.8 – 1.2) nm in the core, 1.6
nm in the (1-4) nm thick elastically soft paraelectric or high-k semiconductor shell, and 4 nm in the
dielectric medium (Fig. S1). The dependence on the mesh size is verified by increasing the minimal
size to 0.8 nm. We verified that this only results in minor changes in the electric polarization, electric
field, and elastic stress and strain, such that the spatial distribution of each of these quantities becomes
less smooth (i.e., they contain numerical errors in the form of a small random noise). However, when
using these larger cell sizes, all significant details remain visible, and more importantly, the system
energy remains essentially the same with an accuracy of about 0.1%.


            (a) “sharp”                   (b) rounded ends                  (c) spherical
               ends                        with 𝑅𝑐ℎ = 1 nm                 ends 𝑅𝑐ℎ = 5 nm




            Element size (nm)               Element size (nm)               Element size (nm)

Figure S1. Examples of mesh for the sharp edges (a), rounded edges (b) and rounded caps (c) of the cylindrical
nanoparticle. The color corresponds to the size of the mesh elements.




                                                      5
              Table SI. LGD coefficients and other material parameters of BaTiO3 nanocylinders

         Coefficient                              Numerical value                               References

b, e                    b = 7 (core background), e = 10 (surrounding)                        14
ai (in mJ/C2)            a1 = 3.34(T−381)105, T = 3.34105 (a1 = −2.94107 at 298 K)          19
aij (in m5J/C4)          a11 = 4.69(T−393)106–2.02108, a12 = 3.230108,                       19
                         (a11 = −6.71108 at 298 K)
                         a111 = −5.52(T-393)107+2.76109, a112 = 4.47109, a123 = 4.91109     19
aijk (in m9J/C6)
                         (at 298 K a111 = 82.8108, a112 = 44.7108, a123 = 49.1108)
Qij (m4/C2)              Q11=0.11, Q12= -0.043, Q44=0.059                                       19
sij (in 10-12 Pa-1)      s11=8.3, s12= −2.7, s44=9.24                                           20
gij (in 10-10m3J/C2)     g11=5.0, g12= −0.2, g44= 0.2                                           14
                         F11 = 2.4, F12 = 0.5, F44 = 0.06 (these values are recalculated from   21
Fij (in 10-11m3/C)
                         the values f11 = 5.1, f12 = 3.3, f44 = 0.065 V calculated in [21]
fij (in V)
                         The equality 𝐹44 = 𝐹11 − 𝐹12 is valid in the isotropic case.
                         0 (since its characteristic values are unknown for BaTiO3 and
vijklm
                         other perovskites)
ai(s)                    0 (that corresponds to the so-called natural boundary conditions)
  (𝑐)                                                                                           22, 23
𝛽𝑇 (in 10-6K-1)          9.8 (thermal expansion coefficient)
  (𝑐)                                                                                           Recalculated
𝑎𝑐𝑢𝑏𝑖𝑐 (in Å)            4.035 Å lattice constant at 1000 C
                                                                                                from [23]
R and h (in nm)          R = 10 (vary from 2 to 20 nm), h = 80 (vary from 8 to 160 nm)


Effect of the cylinder ends shape on the polarization distribution
            FEM, performed for the sharp and rounded ends of cylindrical core at room temperature with
nominal values of the flexoelectric tensor components 𝐹𝑖𝑗 (listed in Table SI), reveals that the
distribution of the polarization component 𝑃3 depends critically on the curvature radius of the cylinder
ends (Fig. S2). The increase of the curvature leads to both a strong increase of the 𝑃3 value and a
simultaneous gradual transformation of the multiple edge domains into a bidomain c+/c- configuration,
which contains flux-closure domains near the spherical ends (top row in Fig. S2). For the sharp and
slightly rounded ends, the distribution 𝑃3 becomes much more contrasting with increasing 𝐹𝑖𝑗 ; but the
dependence of 𝑃3 on 𝐹𝑖𝑗 virtually disappears as the curvature increases (compare the top and bottom
rows in Fig. S2). FEM results presented below are performed for the cylindrical core with sharp ends,
because this shape is the most sensitive to the flexoelectric coupling.




                                                          6
            (a) “sharp”          (b) rounded ends           (c) rounded ends           (d) spherical ends
               ends               with 𝑅𝑐ℎ = 1 nm           with 𝑅𝑐ℎ = 1.8 nm           with 𝑅𝑐ℎ =5 nm

                      P3 (μC/cm2)             P3 (μC/cm2)               P3 (μC/cm2)             P3 (μC/cm2)
  Nominal Fij




                        P3 (μC/cm)              P3 (μC/cm)               P3 (μC/cm2)            P3 (μC/cm2)
  High 6 Fij




Figure S2. Distribution of the polarization component P3 in three different cross-sections of the cylindrical
nanoparticle with sharp ends (a), rounded ends with curvature 𝑅𝑐ℎ =1 nm (b) and 1.8 nm (c); and hemispherical
ends (d). The values of the flexoelectric coefficients are 𝐹11 = 2.4 ∙10-11m3/C, 𝐹12 = 0.5 ∙ 10-11m3/C, and 𝐹44 =
0.06 ∙ 10-11m3/C for the top row; 𝐹11 = 144 ∙10-11m3/C, 𝐹12 = 3 ∙ 10-11m3/C, and 𝐹44 = 0.36 ∙ 10-11m3/C for the
bottom row. Temperature 𝑇 = 300 𝐾. All other parameters are listed in Table SI.

                Note, that the vortex stability in a ferroelectric nanoparticle depends on many physical factors
including the particle geometry, electric screening and elastic boundary conditions. In particular,
depending on the electric boundary conditions and aspect ratio of length to radius, the vortex-type
polarization can be stable, metastable or unstable in a very prolate cylinder. Here we use not very
prolate cylinders with an aspect ratio varying from 4:1 to 8:1 (see Table SI); and the cylinder ends are
electrically open, which corresponds to a weak electric screening. The electrical open-circuit condition
at the cylinder ends makes the vortex-type polarization energetically favorable independently on the
presence of the flexoelectric coupling. The single-domain state can be stable in a much more prolate


                                                            7
cylinders with an aspect ratio much more than 10 covered by the shell with a very small or zero
effective screening length Λ (see e.g., Ref.[24]).


 Effect of polarization gradient coefficients on the polarization distribution
       We performed FEM for temperatures (200 – 400) K using zero and nominal values of the
electrostriction tensor components 𝑄𝑖𝑗 ; and zero, positive, and negative values of 𝐹𝑖𝑗 . Three values of
𝑔𝑖𝑗 were taken: a nominal value and a factor of ten larger and smaller than the nominal value. The
nominal values of 𝑄𝑖𝑗 , 𝐹𝑖𝑗 , and 𝑔𝑖𝑗 are listed in Table SI. Large values of 𝑔𝑖𝑗 lead to an increase of the
domain wall thickness and makes the domain structure insensitive to 𝐹𝑖𝑗 values; very large values of
𝑔𝑖𝑗 eventually prevent the domain formation. This result expected, since, according to the Ginzburg-

Landau theory, the thickness of the uncharged 180-degree domain wall is proportional to √𝑔44 for the
considered geometry. The situation for small values of 𝑔𝑖𝑗 is much more interesting.
       Typical distributions of the polarization component P3, and polarization magnitude 𝑃 calculated
for small 𝑔𝑖𝑗 and the different values of electrostriction and flexoelectric coupling coefficients are
shown in Fig. S3. For 𝑄𝑖𝑗 = 0 and 𝐹𝑖𝑗 = 0, the reduction of 𝑔𝑖𝑗 by a factor of ten leads to the decrease
of the domain wall width only (Fig. S3a). For nonzero nominal values of 𝑄𝑖𝑗 , the reduction of 𝑔𝑖𝑗 by
a factor of ten leads to the appearance of quasi-periodic spot-like 𝑃3 -domains located near the lateral
surface of the cylinder (shown by blue and red spots in the top row of Figs. S3b-d) instead of two
diffuse axial domains shown in Fig. S2a. These spot-like domains are insensitive to the magnitude and
sign of 𝐹𝑖𝑗 , if its absolute value is less than 4 ∙ 10−11 m3/C (Figs. S3b-d). The sharp transformation of
the quasi-stable spot-like 𝑃3 -domains into a stable bidomain configuration with flux-closure domains
at the cylinder ends appears at unrealistically high values of 𝐹𝑖𝑗 (Fig. S3e). The distributions of
polarization magnitude 𝑃 calculated for nonzero 𝑄𝑖𝑗 and |𝐹𝑖𝑗 | < 4 ∙ 10−11 m3/C reveal a twisted central
line with quasi-periodically located multiple Bloch points, 𝑷 = 0, whose patterns are shown in the
bottom row of Figs. S3b-d.
       The influence of small 𝑔𝑖𝑗 values can be explained in the following way. According to the
Ginzburg-Landau theory, the thickness of the domain wall is directly associated with the gradient
coefficient. Thus, a decrease in the gradient coefficients leads to a decrease in the thickness of the
domain walls, which affects the size of the domains in the transverse direction. This is exactly what is
shown in Fig. S3, calculated for small values of the gradient coefficients. The small 𝑔𝑖𝑗 values leads to
the decrease of the domain wall energy, and, consequently, can lead to the formation of labyrinthine
domain patterns [3, 4] or other gradient-driven structural instabilities, such as domain wall meandering
[25, 26]. An increase in flexoelectric coefficients leads to an increase in effective gradient coefficients,
                                                     8
as a consequence of this, the domain size increases. More importantly, the increase of |𝐹𝑖𝑗 | to the value

                      |𝑔 |
comparable with √ 𝑐𝑖𝑗 , where 𝑐 is the geometry-dependent combination of elastic modulus, can lead

to the appearance of spatially modulated domain patterns [27]. For the small 𝑔𝑖𝑗 values used in
Fig. S3b-d, the influence of 𝑔𝑖𝑗 and 𝐹𝑖𝑗 support the formation of spatially-modulated domain spots and
Bloch points twisting (similar to meandering).
        FEM performed for sharp and rounded ends of a cylindrical BaTiO3 core reveals that the
distribution of the polarization components depends critically on the curvature radius of the cylinder
ends and is highly sensitive to the values of polarization gradient coefficients.


   (a) 𝐹𝑖𝑗 =0            (b) 𝐹𝑖𝑗 <0            (c) 𝐹𝑖𝑗 = 0              (d) 𝐹𝑖𝑗 > 0             (e) |𝐹𝑖𝑗 | ≫ 0
    𝑄𝑖𝑗 = 0               𝑄𝑖𝑗 ≠ 0                𝑄𝑖𝑗 ≠ 0                  𝑄𝑖𝑗 ≠ 0                  𝑄𝑖𝑗 ≠ 0

          P3 (μC/cm2)           P3 (μC/cm2)            P3 (μC/cm2)               P3 (μC/cm2)           P3 (μC/cm2)




           P (μC/cm2)              P (μC/cm2)            P (μC/cm2)              P (μC/cm2)            P (μC/cm2)




Figure S3. Distribution of the polarization component P3 (top row) and polarization magnitude 𝑃 (bottom row)
in three different cross-sections of the nanoparticle core. Different columns are calculated for the different values
of electrostriction and flexoelectric coupling coefficients. The following values of gradient coefficients are used:
𝑔11 = 1 ∙10-10m3/F, 𝑔12 = −0.04 ∙ 10-10m3/F, and 𝑔44 = 0.04 10-11m3/F. Temperature 𝑇 = 300 𝐾. All other
parameters are listed in Table SI.
                                                         9
Effect of the shell dielectric properties on the domain structure
       The dominant vortex-type polarization 𝑃⃗1 + 𝑃⃗2 , which is directed tangentially to the lateral
surface of the cylinder (Fig. S4, top row), appears much bigger than the axial component 𝑃3
perpendicular to the cylinder ends. Actually, a comparison of the scales for 𝑃3 and 𝑃 in Fig. S4 shows
that 𝑃 ≫ |𝑃3 | and 𝑃 ≈ |𝑃⃗1 + 𝑃⃗2 |, and so |𝑃⃗1 + 𝑃⃗2 | ≫ |𝑃3 |. Consequently, the resulting depolarization
field 𝐸3 created by the component 𝑃3 is very small inside the particle. The field 𝐸3 is determined by
the dielectric properties of the shell and, in particular, 𝐸3 slightly decreases with the increase of the
shell dielectric permittivity. A shell with a very high relative dielectric permittivity (e.g., vacancy-
enriched paraelectric SrTiO3) can provide an effective screening of the axial polarization component
in a prolate cylindrical multiaxial ferroelectric core, while the dielectric properties of the shell virtually
do not effect on vortex-type polarization 𝑃⃗1 + 𝑃⃗2 . Being energetically preferable, the appearance of a
shell-insensitive vortex-type polarization in a multiaxial ferroelectric core, such as BaTiO3, is very
probable [28]. This qualitative statement is confirmed quantitatively by the very small 𝑑𝑖𝑣𝑃⃗ and
depolarization electric field 𝐸3 in the core (Fig. S9a and S9c).




                                                     10
           (a) 𝐹𝑖𝑗 = 0                 (b) 𝐹𝑖𝑗 < 0                    (c) 𝐹𝑖𝑗 = 0                  (d) 𝐹𝑖𝑗 > 0
             𝑄𝑖𝑗 = 0                     𝑄𝑖𝑗 ≠ 0                        𝑄𝑖𝑗 ≠ 0                      𝑄𝑖𝑗 ≠ 0
                                  2                              2                             2                       2
                      P3 (μC/cm )               P3 (μC/cm )                       P3 (μC/cm )             P3 (μC/cm )




                                        2                                                           2                      2
                             P (μC/cm )               P (μC/cm )
                                                                          2
                                                                                        P (μC/cm )               P (μC/cm )
   z-coordinate




                                                           .05                               .04                   .05
                  x-coordinate              x-coordinate                      x-coordinate              x-coordinate

Figure S4. Distribution of the polarization vector P inside a cylindrical nanoparticle (top row) and polarization
magnitude 𝑃 (bottom row) in the XZ cross-section of the nanoparticle. The images are calculated without
electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric (𝐹𝑖𝑗 = 0) couplings (a). In the case where electrostriction coupling
in non-zero (𝑄𝑖𝑗 ≠ 0), the values of the flexoelectric coefficients 𝐹𝑖𝑗 are varied: negative (b), zero (c), and
positive (d). The arrow color corresponds to the value of 𝑃3 (red-blue scale). The values of 𝐹𝑖𝑗 and all other
parameters are given in Table SI, 𝑇 = 300 K.


                  A strong influence of the shell dielectric properties on the core domain structure is possible for
a uniaxial ferroelectric core [29], since a polarization rotation is impossible in this case. In particular,
a weak screening can lead to the formation of labyrinthine domains in nanoparticles of uniaxial
ferroelectrics CuInP2S6 [3] and Sn2P2S6 [4].
                  The elastic properties of the shell are important for spherical core-shell nanoparticles, where
the vortices orientation is determined by an elastic anisotropy of the shell [30]. FEM calculations show
that in the case of the cylindrical core-shell BaTiO3 nanoparticles, the vortex axis is oriented along the


                                                                     11
cylinder axis and is nearly independent of the shell dielectric and elastic properties; therefore, role of
the shell for a prolate multiaxial cylindrical core is much weaker than it is for a uniaxial spherical core.


         APPENDIX B. Influence of the Flexoelectric Coupling Strength and Anisotropy on the
                           Domain Structure of a Cylindrical Nanoparticle
       The distribution of the polarization component 𝑃3 in three different cross-sections of the
nanoparticle core, polarization magnitude 𝑃 in the XZ cross-section of the nanoparticle, and isosurfaces
of polarization components 𝑃1,2,3 are shown in Fig. S5. The images are calculated without
electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric (𝐹𝑖𝑗 = 0) coupling (Fig. S5a); with electrostriction
coupling (𝑄𝑖𝑗 ≠ 0) and negative (Fig. S5b), zero (Fig. S5c), positive (Fig. S5d), or high positive
(Fig. S5e) values of the flexoelectric coefficients 𝐹𝑖𝑗 .
       The extremal (maximal or minimal) value 𝑃𝑒 in the center of the diffuse axial P3-domain, shown
by the green curve in Fig. 3f (main text), frequently differs from 𝑃𝑚𝑎𝑥 and 𝑃𝑚𝑖𝑛 values due to the
presence of the small sixteen 𝑃3 -domains localized near the top and bottom junction of cylindrical
sidewall with the ends (bottom raw in Fig. S5). The polarization direction alternates in these 180-
degree domains, with four “up” and four “down” domains at each junction. These alternating 𝑃3 -
domains are not the part of flexon, because they are induced by the electrostriction coupling. Their
structure depends weakly on the flexoelectric coupling strength 𝑓, if 𝑓 is small. However, the shape of
each domain significantly changes and the size of each domain moderately increases as |𝐹𝑖𝑗 | increases
(compare Fig. S5d and Fig. S5e). The change of polarization direction occurs in each of the 16
alternating 𝑃3 -domains at 𝐹𝑖𝑗 → −𝐹𝑖𝑗 (compare Fig. S5b and Fig. S5d).




                                                     12
          (a) 𝐹𝑖𝑗 = 0      (b) 𝐹𝑖𝑗 < 0                (c) 𝐹𝑖𝑗 = 0              (d) 𝐹𝑖𝑗 > 0         (e) 𝐹𝑖𝑗 >> 0
            𝑄𝑖𝑗 = 0          𝑄𝑖𝑗 ≠ 0                    𝑄𝑖𝑗 ≠ 0                  𝑄𝑖𝑗 ≠ 0              𝑄𝑖𝑗 ≠ 0
                                                                               2
                  P3 (μC/cm2)        P3 (μC/cm2)               P3 (μC/cm )            P3 (μC/cm2)              P3 (μC/cm2)
  z-coordinate




            x-coordinate    x-coordinate              x-coordinate             x-coordinate            x-coordinate
                                                      2                    2                       2                        2
                  P (μC/cm2)          P (μC/cm )              P (μC/cm )              P (μC/cm )              P (μC/cm )
  z-coordinate




                                               ..05                  .04                     .05                      .06
         x-coordinate           x-coordinate              x-coordinate             x-coordinate          x-coordinate




                                         Alternating 𝑃3 -domains




                                                Isosurfaces

Figure S5. Distribution of the polarization component P3 (top row) and polarization magnitude (middle row)
in the XZ cross-section of the nanoparticle. Bottom row: isosurfaces of zero polarization components P1 (gray),
P2 (green), and nonzero 𝑃3 =  0.1,  0.1,  0.2, and  0.4 µC/cm2 (red and blue). Images are calculated without
electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric (𝐹𝑖𝑗 = 0) coupling (a); with electrostriction coupling (𝑄𝑖𝑗 ≠ 0) and

                                                              13
negative (b), zero (c), positive (d), or tripled positive (e) values of flexoelectric coefficients 𝐹𝑖𝑗 . Reference values
of 𝐹𝑖𝑗 and all other parameters are given in Table SI. Temperature 𝑇 = 300 𝐾.


        The distribution of the polarization component 𝑃3 in three different cross-sections of the
nanoparticle core, 𝑃3 distribution XZ cross-section, and isosurfaces of polarization components 𝑃1,2,3
are shown in Fig. S6. Images are calculated for the fixed values 𝐹11 = 2.4 ∙10-11m3/C and 𝐹12 = 0.5 ∙
10-11m3/C are, and the value of 𝐹44 varies from -6 to 6 (in 10-11m3/C) as indicated in the legends to
Fig. S6a-f. The flexon containing two pronounced axial domains located near the cylinder ends exists
at large negative (Fig. S6a) and large positive (Fig. S6f) 𝐹44 values. The 𝑃3 -domains become smaller
and more diffuse with a decrease of |𝐹44 |; but they are still visible and practically do not change their
shape, size, or polarization distribution for small |𝐹44 | values over the range |𝐹44 | ≤ 0.06 (Fig. S6b-
d). The flexon becomes faint and almost disappears when 𝐹44 approaches the value 𝐹44 = 𝐹11 − 𝐹12 =
1.9 ∙ 10-11 m3/C, corresponding to the isotropic symmetry of 𝐹𝑖𝑗 (Fig. S6e).




                                                           14
   (a) high              (b) negative     (c) zero          (d) positive      (e) isotropic        (f) high
  𝐹44 = −6               𝐹44 = −0.06      𝐹44 = 0            𝐹44 = 0.06         𝐹44 = 1.9          𝐹44 = 6

                 P3 (μC/cm2)   P3 (μC/cm2)      P3 (μC/cm2)      P3 (μC/cm2)       P3 (μC/cm2)         P3 (μC/cm2)
  z-coordinate




     x-coordinate          x-coordinate      x-coordinate      x-coordinate    x-coordinate      x-coordinate




                                                              Isosurfaces

Figure S6. Distribution of polarization component 𝑃3 in three different cross-sections of the nanoparticle core
(top row), and 𝑃3 in the XZ cross-section of cylindrical core (middle row). Bottom row: isosurfaces of
polarization components 𝑃1 (gray), 𝑃2 (green), and 𝑃3 (red and blue). Zero values correspond 𝑃1 and 𝑃2
isosurfaces, while isosurfaces of 𝑃3 correspond to the values 𝑃3 =  0.1,  0.2, and  0.4 µC/cm2 for the images
(a)-(d), (e), and (f) respectively. The images are calculated for the fixed values 𝐹11 = 2.4 ∙10-11m3/C and 𝐹12 =
0.5 ∙ 10-11m3/C, while the value of 𝐹44 varies from -6 to 6 (in 10-11m3/C) as indicated in the legends. All other
parameters are listed in Table SI. Temperature 𝑇 = 300 𝐾.




                                                        15
          APPENDIX C. Temperature Behavior of the Flexon-Type Polarization Distribution
       To define the temperature interval, where flexons exist being stable or meta-stable, we
performed FEM in the temperature range from 50 K to 400 K using different initial distributions of
polarization in a cylindrical core. Typical FEM results are shown in Fig. S7, where the columns (a)-
(e) correspond to the temperature increase from 240 K to 370 K.
       A bidomain configuration of 𝑃3 is stable at temperatures lower than 250 K (Figs. S7a). The
bidomain structure has a relatively thin uncharged 180-degree domain wall inside the cylinder, which
transforms into a flux-closure domain near the electrically-open cylinder ends (top and middle images
in Figs. S7a). The origin of the flux-closure domain is the core tendency to minimize its electrostatic
energy, because a flux-closure domain wall creates a much weaker depolarization field (in fact
negligibly small) compared to the field that the charged 180-degree domain wall would create. The
structure of the P-vector is vortex-like and changes moderately when approaching the surface at 𝑇 ≤
240 K (as seen from the direction of arrows in the bottom image of Figs. S7a).
       We revealed that an initial four-domain polarization distribution relaxes to a flexon-like domain
structure in the temperature range 260 K < 𝑇 < 360 K (middle row in Figs. S7b-d). The structure of
the P-vector is vortex-like, which weakly changes when approaching the surface in the same
temperature range (as seen from the direction of arrows at the bottom image of Figs. S7b-d). A
relatively small domain wall broadening exists near the cylinder ends, which can be seen from the
polarization magnitude distribution at 260 K < 𝑇 < 360 K (top images of Figs. S7b-d).
       The flexon gradually disappears at 𝑇 > 370 K (middle image in Figs. S7e). The ferroelectric
polarization inside the core significantly decreases at 𝑇 > 370 K and completely disappears at
𝑇~400 K (top image in Figs. S7e). The lateral components 𝑃1 and 𝑃2 form a vortex-like structure and
their distribution is nearly independent of the coordinate 𝑧 along the cylinder axis. Hence, the vortex-
like structure of the P-vector is insensitive to the surface presence. The structure becomes faint with a
temperature increase above 370 K (note that the arrows length decreases in the bottom image of
Figs. S7e). The flexon-type polarization distribution exists over a relatively wide temperature range
260 K < 𝑇 < 360 K. The axial counter domains inherent to flexons are the most pronounced feature
over the narrower range 290 K < 𝑇 < 340 K. The relatively wide temperature range (about 100 K)
corresponding to the stability or meta-stability of the flexon-type polarization distribution gives us the
hope that the domain morphology can be observed experimentally.




                                                   16
       (a) T=240 K                    (b) T=270 K (c) T=300 K (d) T=340 K (e) T=370 K
                      P (μC/cm2)                    P (μC/cm2)         P (μC/cm2)      P (μC/cm2)     P (μC/cm2)
       z-coordinate
       flux-closure




                       P3 (μC/cm2)                       P3 (μC/cm2)    P3 (μC/cm2)    P3 (μC/cm2)    P3 (μC/cm2)




                                                                                                        disappearence
                                      flexon formation




                                                                                                            flexon
       z-coordinate




                                                                                            flexon
                                                                             flexon
                           bidomain




                x-coordinate               x-coordinate                x-coordinate   x-coordinate   x-coordinate




Figure S7. Distribution of polarization magnitude 𝑃 (top row) and its component 𝑃3 (middle row) in XZ cross-
sections of the nanoparticle core. Bottom row: distribution of polarization vector P shown by arrows colored
according to the value of 𝑃3 . Different columns are calculated for the temperatures 𝑇 = 240, 270, 300, 340,
and 370 K (a, b, c, d, e). All other parameters are listed in Table SI.



                                                                            17
             APPENDIX D. Influence of an External Electric Field on the Flexon Dynamics
The orientation of 𝑃3 can be readily changed by the application of an external electric field. Typical
quasistatic hysteresis loops of 𝑃3 (𝑈) are shown in Figs. S8a-d, where the black loops correspond to
the average polarization ̅̅̅
                         𝑃3 (𝑈); blue and red loops correspond to the minimal (𝑃𝑚𝑖𝑛 (𝑈)) and maximal
(𝑃𝑚𝑎𝑥 (𝑈)) values of 𝑃3 (𝑈) at a given voltage 𝑈. The loops of ̅̅̅
                                                               𝑃3 (𝑈) are very slim, voltage-symmetric
(since their shape is symmetrical with respect to the transformation 𝑈 → −𝑈), and belong to the
antiferroelectric type (since they are double loops with ̅̅̅
                                                         𝑃3 (𝑈) = 0). The loops of 𝑃𝑚𝑖𝑛 (𝑈) and 𝑃𝑚𝑎𝑥 (𝑈)
are strongly voltage-asymmetric and contain two single loops of different shape and size, which we
refer to as “major” and “minor” loops. The loop 𝑃𝑚𝑖𝑛 (𝑈) is strongly shifted downward, and the loop
𝑃𝑚𝑎𝑥 (𝑈) is strongly shifted upward.
       The loops in Figs. S8a-S8c are calculated for nonzero electrostriction coupling coefficients
𝑄𝑖𝑗 and negative, zero, or positive flexoelectric coupling coefficients 𝐹𝑖𝑗 . The main difference between

the loops shown in Figs. S8a, S8b, and S8c, appear in a horizontal shift of the asymmetric loops
𝑃𝑚𝑖𝑛 (𝑈) and 𝑃𝑚𝑎𝑥 (𝑈), originating from the effective “flexoelectric” field. The field is proportional to
the combination of 𝐹𝑖𝑗 , and so its direction is defined by the sign of 𝐹𝑖𝑗 , and it is absent for 𝐹𝑖𝑗 = 0. In
                                                                                          𝜕𝑢
the linear approximation, the flexoelectric field is proportional to (𝐹11 − 𝐹44 − 𝐹12 ) 𝜕𝑧33 , where 𝑢33 is

the component of elastic strain tensor (details are in Appendix E). The proportionality partially
explains the right shift (𝑈𝑖𝑛𝑡 > 0) of the intersection point between major and minor loops calculated
for 𝐹𝑖𝑗 ≤ 0 (shown in Figs. S8a-b) and the left shift of the intersection point calculated for 𝐹𝑖𝑗 > 0
(shown in Fig. S8c).
       The loops in Fig. S8d are calculated without electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric
coupling (𝐹𝑖𝑗 = 0). Here the loop of ̅̅̅
                                     𝑃3 (𝑈) is almost indistinguishable from the loops ̅̅̅
                                                                                       𝑃3 (𝑈) shown in
Figs. S8a-8c for 𝑄𝑖𝑗 ≠ 0. The subtle difference is an ultra-small coercivity at 𝑈 = 0, which is absent
for the loops in Figs. S8a-c. The minor loops of 𝑃𝑚𝑖𝑛 (𝑈) and 𝑃𝑚𝑎𝑥 (𝑈) are very small in comparison
with the major loops, and they are also significantly smaller than the minor loops shown in Figs. S8a-
S8c. The intersection point of major and minor loops corresponds to 𝑈𝑖𝑛𝑡 = 0.
       The bottom row in Fig. S8 shows 𝑃3 distributions for different voltages, from which it follows
that different 𝑃3 distributions averaged over the core volume correspond to the same average value,
̅̅̅
𝑃3 (𝑈). Thus, the analysis of the hysteresis loops leads to the conclusion that flexons cannot be
distinguished from macroscopic (e.g., capacitance) measurements of the average polarization in a
homogeneous electric field, they can only be registered by local probing methods using the strong
gradient of electric field with a nanoscale resolution, such as piezoresponse force microscopy (PFM).



                                                     18
                                   (a) 𝐹𝑖𝑗 <0, 𝑄𝑖𝑗 ≠ 0               (b) 𝐹𝑖𝑗 = 0, 𝑄𝑖𝑗 ≠ 0
                                   𝑃𝑚𝑎𝑥
   Polarization (μC/cm2)



                                                                     𝑃𝑚𝑎𝑥                       𝑃̅
                                   major                 𝑃̅
                                   loop

                                                   𝑃𝑚𝑖𝑛
                                          minor
                                                                                      𝑃𝑚𝑖𝑛
                                          loop



                                   (c) 𝐹𝑖𝑗 > 0, 𝑄𝑖𝑗 ≠ 0               (d) 𝐹𝑖𝑗 =0, 𝑄𝑖𝑗 = 0
  Polarization (μC/cm2)




                                   𝑃𝑚𝑎𝑥                              𝑃𝑚𝑎𝑥
                                                          𝑃̅                                   𝑃̅



                                                  𝑃𝑚𝑖𝑛                                 𝑃𝑚𝑖𝑛



                                     Voltage U (V)                      Voltage U (V)




                           -20 V                                                                +20 V
                                    U = -5 V                   U=0              U = +5 V

Figure S8. Dependence of the average polarization component ̅̅̅
                                                            𝑃3 (black loops) and its minimal 𝑃𝑚𝑖𝑛 (blue
loops) and maximal 𝑃𝑚𝑎𝑥 (red loops) values on the applied voltage 𝑈. Black dots connected with a vertical
dashed line correspond to 𝑈𝑖𝑛𝑡 . Plots (a-d) are calculated for different values of electrostriction and flexoelectric
coupling coefficients, as written in the legends. The plots (a-c) are calculated for nonzero electrostriction
coupling coefficients (𝑄𝑖𝑗 ≠ 0) and negative (a), zero (b), or positive (c) flexoelectric coupling coefficients 𝐹𝑖𝑗 .
Plot (d) is calculated without electrostriction (𝑄𝑖𝑗 = 0) and flexoelectric (𝐹𝑖𝑗 = 0) coupling. Temperature 𝑇 =
                                                                19
300 𝐾, the distance between the electrodes is 60 nm. All other parameters are listed in Table SI. The bottom
row shows 𝑃3 distributions for different voltages U. Different distributions corresponding to the same U illustrate
a rather small hysteresis effect.



                                             APPENDIX E. Approximate Analytical Solution

                     𝜕𝜎            𝜕𝜎         𝜕𝜎
      Since 𝜕𝑥𝑖1 = 𝜕𝑥𝑖2 = 𝜕𝑥𝑖3 = 0 in accordance with mechanical equilibrium equations, the right-
                          𝑖             𝑖             𝑖

hand sides in Eqs. (A.3) can be rewritten as:

            𝜕𝑃
       𝛤 𝜕𝑡1 + 2𝑃1 (𝑎1 − 𝑄12 (𝜎22 + 𝜎33 ) − 𝑄11 𝜎11 ) − 𝑄44 (𝜎12 𝑃2 + 𝜎13 𝑃3 ) + 4𝑎11 𝑃13 + 2𝑎12 𝑃1 (𝑃22 +
                                                                                                                                                                                 𝜕2 𝑃1
                          𝑃32 ) + 6𝑎111 𝑃15 + 2𝑎112 𝑃1 (𝑃24 + 2𝑃12 𝑃22 + 𝑃34 + 2𝑃12 𝑃32 ) + 2𝑎123 𝑃1 𝑃22 𝑃32 − 𝑔11                                                                       −
                                                                                                                                                                                 𝜕𝑥12

                                                              𝜕2𝑃       𝜕2𝑃                                               𝜕𝜎                        𝜕
                                                      𝑔44 ( 𝜕𝑥 21 + 𝜕𝑥 21 ) = −(𝐹11 − 𝐹44 − 𝐹12 ) 𝜕х11 − 𝐹12 𝜕х 𝑇𝑟𝜎̂ + 𝐸1 (E.1a)
                                                                2          3                                                   1                        1


            𝜕𝑃
       𝛤 𝜕𝑡2 + 2𝑃2 (𝑎1 − 𝑄12 (𝜎11 + 𝜎33 ) − 𝑄11 𝜎22 ) − 𝑄44 (𝜎12 𝑃1 + 𝜎23 𝑃3 ) + 4𝑎11 𝑃23 + 2𝑎12 𝑃2 (𝑃12 +
                                                                                                                                                                                 𝜕2𝑃
                          𝑃32 ) + 6𝑎111 𝑃25 + 2𝑎112 𝑃2 (𝑃14 + 2𝑃22 𝑃12 + 𝑃34 + 2𝑃22 𝑃32 ) + 2𝑎123 𝑃2 𝑃12 𝑃32 − 𝑔11 𝜕𝑥 22 −
                                                                                                                                                                                    2

                                                           𝜕2𝑃          𝜕2𝑃                                               𝜕𝜎                        𝜕
                                                      𝑔44 ( 𝜕𝑥 22 + 𝜕𝑥 22 ) = −(𝐹11 − 𝐹44 − 𝐹12 ) 𝜕𝑥22 − 𝐹12 𝜕х 𝑇𝑟𝜎̂ + 𝐸2 (E.1b)
                                                                1          3                                                   2                        2


            𝜕𝑃
       𝛤 𝜕𝑡3 + 2𝑃3 (𝑎1 − 𝑄12 (𝜎11 + 𝜎22 ) − 𝑄11 𝜎33 ) − 𝑄44 (𝜎13 𝑃1 + 𝜎23 𝑃2 ) + 4𝑎11 𝑃33 + 2𝑎12 𝑃3 (𝑃12 +
                                                                                                                                                                                 𝜕2𝑃
                          𝑃22 ) + 6𝑎111 𝑃35 + 2𝑎112 𝑃3 (𝑃14 + 2𝑃32 𝑃12 + 𝑃24 + 2𝑃22 𝑃32 ) + 2𝑎123 𝑃3 𝑃12 𝑃22 − 𝑔11 𝜕𝑥 23 −
                                                                                                                                                                                    3

                                                           𝜕2 𝑃3        𝜕2 𝑃3                                             𝜕𝜎                        𝜕
                                                      𝑔44 (         +           ) = −(𝐹11 − 𝐹44 − 𝐹12 ) 𝜕х33 − 𝐹12 𝜕х 𝑇𝑟𝜎̂ + 𝐸3 (E.1c)
                                                           𝜕𝑥12         𝜕𝑥22                                                   3                        3


                                                                                𝜕𝜎                   𝜕𝜎       𝜕𝜎                           𝜕𝜎                𝜕𝜎
The derivation is straightforward: −𝐹11 𝜕х33 − 𝐹12 ( 𝜕х11 + 𝜕х22 ) − 𝐹44 ( 𝜕𝑥13 + 𝜕𝑥23 ) = −(𝐹11 −
                                                                                     3                    3           3                         1                   2

     𝜕𝜎33                     𝜕𝜎11          𝜕𝜎22                                              𝜕𝜎33            𝜕
𝐹44 ) 𝜕х − 𝐹12 ( 𝜕х + 𝜕х ) = −(𝐹11 − 𝐹44 − 𝐹12 ) 𝜕х − 𝐹12 𝜕х 𝑇𝑟𝜎̂, where 𝑇𝑟𝜎̂ = 𝜎11 + 𝜎22 +
        3                          3          3                                                 3                 3

            𝜕𝜎            𝜕𝜎                 𝜕𝜎
𝜎33 and 𝜕𝑥13 + 𝜕𝑥23 ≡ − 𝜕х33 .
                 1             2                  3


        Elastic stresses existing in the system can be found from Eq.(A.6) as:

                                                                                                                               𝜕𝑃                           𝜕𝑃           𝜕𝑃
            𝜎11 = 𝑐11 𝑢11 + 𝑐12 (𝑢22 + 𝑢33 ) − 𝑞11 𝑃12 − 𝑞12 (𝑃22 + 𝑃32 ) − 𝑓11 𝜕𝑥1 − 𝑓12 (𝜕𝑥2 + 𝜕𝑥3 ), (E.2a)
                                                                                                                                       1                        2            3


                                                                                                                               𝜕𝑃                       𝜕𝑃              𝜕𝑃
         𝜎22 = 𝑐11 𝑢22 + 𝑐12 (𝑢11 + 𝑢33 ) − 𝑞11 𝑃22 − 𝑞12 (𝑃12 + 𝑃32 ) − 𝑓11 𝜕𝑥2 − 𝑓12 (𝜕𝑥1 + 𝜕𝑥3 ), (E.2b)
                                                                                                                                       2                        1            3


                                                                                                                           𝜕𝑃                       𝜕𝑃                  𝜕𝑃
        𝜎33 = 𝑐11 𝑢33 + 𝑐12 (𝑢11 + 𝑢22 ) − 𝑞11 𝑃32 − 𝑞12 (𝑃22 + 𝑃12 ) − 𝑓11 𝜕𝑥3 − 𝑓12 (𝜕𝑥1 + 𝜕𝑥2 )                                                                               (E.2c)
                                                                                                                                   3                        1            2



                                                                                         20
                                                                                 𝜕𝑃           𝜕𝑃
                                                𝜎12 = 𝑐44 𝑢12 − 𝑞44 𝑃1 𝑃2 − 𝑓44 (𝜕𝑥1 + 𝜕𝑥2 ),                                     (E.2d)
                                                                                   2           1


                                                                                  𝜕𝑃          𝜕𝑃
                                                𝜎13 = 𝑐44 𝑢13 − 𝑞44 𝑃1 𝑃3 − 𝑓44 (𝜕𝑥1 + 𝜕𝑥3 ),                                     (E.2e)
                                                                                      3            1


                                                                                      𝜕𝑃       𝜕𝑃
                                                  𝜎23 = 𝑐44 𝑢23 − 𝑞44 𝑃3 𝑃2 − 𝑓44 (𝜕𝑥2 + 𝜕𝑥3 ).                                   (E.2f)
                                                                                          3            2


                𝑄                1                    𝐹
Here 𝑞44 = 𝑠 44, 𝑐44 = 𝑠 and 𝑓44 = 𝑠44 .
                 44              44                       44


        In the virtual absence of a depolarization field, which is true with high accuracy for a vortex
                                          𝜕𝑃
type polarization, the divergence 𝑑𝑖𝑣𝑃⃗ = 𝜕𝑥𝑖 should be very small. Indeed, the approximation 𝑑𝑖𝑣𝑃⃗ ≈
                                                               𝑖

0 is valid inside the cylindrical core (Fig. S9b).

        We also note the polarization magnitude 𝑃 = √𝑃12 + 𝑃22 + 𝑃32 is very close to the constant value
                                                                                                           𝜕𝑃
everywhere, except for the vortex core (Fig. S5, middle row), and its derivative 𝜕х is negligibly small
                                                                                                            3

everywhere, except in the immediate vicinity of the vortex core when in contact with the cylinder ends.
For this case we obtain that:

         ̂
      𝜕𝑇𝑟𝜎        𝜕                                                                              ̂
                                                                                              𝜕𝑇𝑟𝑢
               = 𝜕х [(𝑐11 + 2𝑐12 )𝑇𝑟𝑢̂ − (𝑞11 + 2𝑞12 )𝑃2 − (𝑓11 + 2𝑓12 )𝑑𝑖𝑣𝑃⃗] ≈ (𝑐11 + 2𝑐12 ) 𝜕х (E.3)
        𝜕х3           3                                                                                                       3


and

        𝜕𝜎33        𝜕                                                                                           𝜕𝑃
               = 𝜕х [𝑐11 𝑢33 + 𝑐12 (𝑢11 + 𝑢22 ) + (𝑞11 − 𝑞12 )𝑃32 − 𝑞12 𝑃2 − (𝑓11 − 𝑓12 ) 𝜕𝑥3 −𝑓12 𝑑𝑖𝑣𝑃⃗] ≈
        𝜕х3             3                                                                                        3

                                            𝜕                                                                          𝜕2 𝑃3
                                                 [(𝑐11 − 𝑐12 )𝑢33 + 𝑐12 Tr𝑢̂ + (𝑞11 − 𝑞12 )𝑃32 ] − (𝑓11 − 𝑓12 )                    (E.4)
                                           𝜕х3                                                                         𝜕𝑥32

                                   ̂
                                𝜕𝑇𝑟𝑢
        Assuming that 𝜕х ≈ 0 and using the smallness of 𝑃3 , we can obtain the approximate linearized
                                     3

equation for 𝑃3 :

                    𝜕2𝑃                  𝜕2 𝑃      𝜕2 𝑃                                                                        𝜕𝑢
 2𝑎1∗ 𝑃3 − 𝑔11
            ∗     3
                    − 𝑔44 ( 𝜕𝑥 23 + 𝜕𝑥 23) ≈ 𝑄44 (𝜎13 𝑃1 + 𝜎23 𝑃2 ) − (𝐹11 − 𝐹44 − 𝐹12 )(𝑐11 − 𝑐12 ) 𝜕𝑥33 +
               𝜕𝑥 2         3               1         2                                                                             3

                                                                                                                     𝐸3 ,          (E.5)

where            𝑎1∗ = 𝑎1 − 𝑄12 𝑇𝑟𝜎̂ − (𝑄11 − 𝑄12 )𝜎33 ≈ 𝑎1 − 𝑄12 (𝑐11 + 2𝑐12 )𝑇𝑟𝑢̂ − (𝑞11 + 2𝑞12 )𝑝2 −
(𝑄11 − 𝑄12 )[(𝑐11 − 𝑐12 )𝑢33 + 𝑐12 Tr𝑢̂] ≈ 𝑎1 − (𝑞11 + 2𝑞12 )𝑝2 − (𝑄11 − 𝑄12 )(𝑐11 − 𝑐12 )𝑢33                                       and
 ∗
𝑔11 = 𝑔11 + (𝐹11 − 𝐹44 − 𝐹12 )(𝑓11 − 𝑓12 ). The simplest 2D polarization vortex can be modeled by the
functions
                                                          𝑃1 = 𝑝(𝑟)𝑠𝑖𝑛𝜑, 𝑃2 = −𝑝(𝑟)𝑐𝑜𝑠𝜑 and 𝑃3 = 0.                               (E.6a)
These polarization components in cylindrical coordinates are
                                                                    21
                                                                        𝑃𝑟 = 0, 𝑃𝜑 = −𝑝(𝑟) and 𝑃3 = 0.                           (E.6b)

It is easy to check that in the case 𝑑𝑖𝑣𝑃⃗ = 0 for arbitrary 𝑝(𝜌). For a 2D-vortex with an empty core we
                                           𝜌
can assume that 𝑝(𝜌) ≈ 𝑡𝑎𝑛ℎ (𝐿𝑥 ), where 𝐿𝑥𝐶 is a transverse correlation length.
                                           𝐶


        Using Eqs.(E.6) as a zero approximation we obtain from Eq.(E.2) that 𝜎13 = 𝑐44 𝑢13 , 𝜎23 =
𝑐44 𝑢23 and 𝜎33 = (𝑐11 − 𝑐12 )𝑢33 + 𝑐12 Tr𝑢̂ − 𝑞12 𝑝2

                                                                                                        𝜕𝑢33
                                        𝑄44 𝑐44 𝑝(𝑢13 𝑠𝑖𝑛𝜑−𝑢23 𝑐𝑜𝑠𝜑)−(𝐹11 −𝐹44 −𝐹12 )(𝑐11 −𝑐12 )
                                                                                                        𝜕𝑥3
               𝑃3 ≈ 2[𝑎 −(𝑞 +2𝑞             2                                                               𝑧       𝑥        ,   (E.7a)
                           1     11    12 )𝑝 −(𝑄11 −𝑄12 )(𝑐11 −𝑐12 )𝑢33 +(𝑔11 +(𝐹11 −𝐹44 −𝐹12 )(𝑓11 −𝑓12 ))𝐿𝐶 +𝑔44 𝐿𝐶 ]


        Next, we consider several model cases. The first case is an absolutely rigid shell covering the
ferroelectric core, when the maximal stresses evolved in the system can be roughly estimated from
Eqs.(A.8) at 𝑢𝑖𝑗 = 0. The second case corresponds to a very soft shell covering the rigid ferroelectric
core, when the stresses are minimal and the strains (at least near the cylinder ends) can be roughly
estimated from Eqs.(E.2) at 𝜎𝑖𝑗 = 0. Furthermore, the compatibility conditions should be valid.

                                                                                                  𝑄 −𝑄
        Using the relations 𝑞11 − 𝑞12 = (𝑄11 − 𝑄12 )(𝑐11 − 𝑐12 ) = 𝑠11−𝑠 12, 𝑞11 + 2𝑞12 = (𝑄11 +
                                                                                                   11    12

                               𝑄11 +2𝑄12                           1                     1
2𝑄12 )(𝑐11 + 2𝑐12 ) = 𝑠 +2𝑠 , 𝑐11 − 𝑐12 = 𝑠 −𝑠 , 𝑐44 = 𝑠                                      and 𝑓11 − 𝑓12 = (𝐹11 − 𝐹12 )(𝑐11 −
                                 11   12                      11       12                44

        𝐹 −𝐹
𝑐12 ) = 𝑠11 −𝑠12 , we obtain that
         11    12


                                               𝑄44                      𝐹 −𝐹 −𝐹       𝜕
                                                   𝑝(𝑢13 𝑠𝑖𝑛𝜑−𝑢23 𝑐𝑜𝑠𝜑)− 11 44 12 𝑢33
                                               𝑠44                         𝑠11 −𝑠12   𝜕z
                          𝑃3 ≈         𝑄 +2𝑄12 2 𝑄11 −𝑄12                             𝐹 −𝐹                            ,          (E.7b)
                                 2[𝑎1 − 11       𝑝 −         𝑢 +[𝑔11 +(𝐹11 −𝐹44 −𝐹12 ) 11 12 ]𝐿𝑧𝐶 +𝑔44 𝐿𝑥𝐶 ]
                                       𝑠11 +2𝑠12     𝑠11 −𝑠12 33                      𝑠11 −𝑠12


                                                                                                   𝜌
where {𝜌, 𝜑, 𝑧} are cylindrical coordinates, the function 𝑝(𝜌) ≈ 𝑡𝑎𝑛ℎ (𝐿𝑥 ), and 𝐿𝑥𝐶 and are lateral and
                                                                                                    𝐶

axial correlation lengths. The functions 𝑢𝑖𝑗 (𝜌, 𝜑, 𝑧) are elastic strains, 𝑠𝑖𝑗 are elastic compliances, 𝑄𝑖𝑗
are electrostriction tensor components, 𝑔𝑖𝑗 are polarization gradient coefficients written in Voight
notations. From Eq.(E.7b) the axial part of the flexon polarization is proportional to
  𝐹 −𝐹44 −𝐹12 𝜕
− 11𝑠                𝑢33 (𝜌, 𝜑, 𝑧), and this proportionality along with Fig. S9o qualitatively describes the
     11 −𝑠12    𝜕z

curves’ behavior in Fig. 3f and 4f in the main text.
        Using Eqs.(E.1), we can “recover” an analog of Eq.(A.2) for a “full” Lifshitz invariant:
                                      𝐹 −𝐹44 −𝐹12        𝜕𝑃                 𝜕𝜎       𝐹            𝜕𝑃               ̂)
                                                                                                               𝜕𝑇𝑟(𝜎
                          𝐺𝑓𝑙𝑒𝑥𝑜 = 11               (𝜎𝑖𝑖 𝜕x 𝑖 − 𝑃𝑖 𝜕x𝑖𝑖 ) + 212 [𝑇𝑟(𝜎̂) 𝜕х 𝑖 − 𝑃𝑖                       ],       (E.8a)
                                               2            𝑖                    𝑖                  𝑖           𝜕х𝑖
                     𝜕𝑃
Assuming that 𝜕х 𝑖 ≈ 0 (as it should be for the mostly uncharged domain structures) and making an
                      𝑖

integration over parts in the second term in Eq.(E.8a), we obtain:


                                                                       22
                                                                    𝐹 −𝐹44 −𝐹12        𝜕𝑃          𝜕𝜎
                                                          𝐺𝑓𝑙𝑒𝑥𝑜 ≈ 11             (𝜎𝑖𝑖 𝜕x 𝑖 − 𝑃𝑖 𝜕x𝑖𝑖 ).          (E.8b)
                                                                         2                  𝑖           𝑖

Elementary, but cumbersome calculations lead to an “odd” flexo-field in the boundary conditions
 .           .     𝐹 −𝐹 −𝐹 𝑄 −𝑄         .
∫𝑉 𝐺𝑓𝑙𝑒𝑥𝑜 ≈ ∫𝑉 𝐺0 + 11 244 12 11 3 12 ∫𝑆𝑖 𝑃𝑖3 .

           To verify the analogy with a Dyzaloshinskii-Moryia interaction (DMI), we attempt to convert
the Lifshitz invariants into chiral interactions of a DMI type. Using 𝑑𝑖𝑣𝑃⃗ = 0 for the uncharged domain
structures and making straightforward analytic manipulations for the cubic m3m point symmetry group
of the BaTiO3 parent phase, the explicit form of the Lifshitz invariant (1f) is 𝐺𝑓𝑙𝑒𝑥𝑜 ≈
𝐹11 −𝐹44 −𝐹12           𝜕𝑃       𝜕𝜎
                (𝜎𝑖𝑖 𝜕𝑥𝑖 − 𝑃𝑖 𝜕𝑥𝑖𝑖 ), where a summation over “i” is performed [Eqs.(E.8)]. The elastic stress
       2                  𝑖           𝑖

𝜎𝑖𝑗 contains a contribution proportional to 𝑄𝑖𝑗𝑘𝑙 𝑃𝑘 𝑃𝑘 , which originates from the electrostriction

                                                                                  𝐹11 −𝐹44 −𝐹12                    𝜕𝑃
coupling. For the 𝑃3 -component we determine that the term                                        𝑄12 ((𝑃12 + 𝑃22 ) 𝜕𝑥3 −
                                                                                        2                            3


     𝜕(𝑃12 +𝑃22 )
𝑃3                  ) is present in the Lifshitz invariant (1f). A similar invariant has been discussed in Ref. [31]
        𝜕𝑥3

in the context of incommensurate phases with a defined chirality. This is consistent with our finding of
the formation of a flexon induced by the invariant.




                                                            23
     (a) 𝑃𝑧               (b) 𝑑𝑖𝑣𝑃⃗                 (c) 𝐸𝑧               (d) 𝜎𝑟𝑟                 (e) 𝜎𝜑𝜑
                μC/cm2                 C/cm3                    V/cm                  GPa                     GPa




                                                                                                      𝜕
    (f) 𝜎𝑧𝑧              (g) 𝜎𝑟𝑧                 (h) 𝜎𝑟𝜑                 (i) 𝑇𝑟[𝝈]              (j)        𝑇𝑟[𝝈]
                                                                                                      𝜕𝑧
                GPa                    MPa                     MPa                   GPa                     GPa/m




                                                                              𝜕                        𝜕
     (k)
           𝜕
                𝜎𝑧𝑧        (l) 𝑇𝑟[𝑢]                (m) 𝑢𝑧𝑧             (n)        𝑇𝑟[𝑢]        (o)        𝑢𝑧𝑧
           𝜕𝑧                                                                 𝜕𝑧                      𝜕𝑧
                                           %                       %                  1/μm                       1/μm
           GPa/m




Figure S9. Distribution of polarization component 𝑃𝑧 (a), its divergency 𝑑𝑖𝑣𝑃⃗ (b), electric field component 𝐸𝑧
(c), nonzero elastic stresses (d-i), their derivatives (j, k), strain components (l,m) and its gradients (n, o) in three
different cross-sections of the cylindrical core. A cylindrical coordinate system {𝑟, 𝜑, 𝑧} is used for the
mechanical stress, strain, electric field and polarization. Note that the stress component 𝜎𝑧𝜑 = 0 (in spherical
coordinates). Temperature 𝑇 = 300 𝐾. All other parameters are listed in Table SI.




                                                          24
                          APPENDIX F. Topological Index and Toroidal Moment

First, let us calculate the topological index 𝑛 of the unit polarization orientation [32]
                                                              1         𝜕𝑝     𝜕𝑝
                                                       𝑛 = 4𝜋 ∫𝑆 𝑝 [𝜕𝑥 × 𝜕𝑦 ] 𝑑𝑥𝑑𝑦                                                  (F.1)

for zero, positive, and negative flexoelectric tensor coefficients. The integration is performed over the
                                             𝑃⃗
cylinder cross-section, and here 𝑝 = 𝑃.

          The flexon polarization has the following structure in Cartesian coordinates
                       𝑃1 ≈ 𝑝(𝑟, 𝑧) cos[𝜑(𝛼, 𝑧)], 𝑃2 ≈ 𝑝(𝑟, 𝑧) sin[𝜑(𝛼, 𝑧)], 𝑃3 ≈ 𝜂(𝑟, 𝑧).                                         (F.2a)
                                               𝜋
Here 𝑝(𝑟, 𝑧) > 0, and 𝜑(𝛼, 𝑧) ≈ 𝛼 − 2 , where 𝛼 is the polar angle, 𝑥 = 𝑟 cos 𝛼, and 𝑦 = 𝑟 sin 𝛼. The

polarization magnitude is 𝑃(𝑟, 𝑧) = √𝑝2 (𝑟, 𝑧) + 𝜂2 (𝑟, 𝑧).
          Let us introduce the unit polarization as:
                      𝑝 ≈ {sin[𝜃(𝑟, 𝑧)] cos[𝜑(𝛼, 𝑧)] , sin[𝜃(𝑟, 𝑧)] sin[𝜑(𝛼, 𝑧)] , cos[𝜃(𝑟, 𝑧)]},                                  (F.2b)
                                                   𝑝(𝑟,𝑧)                                          𝜂(𝑟,𝑧)
where the functions sin[𝜃(𝑟, 𝑧)] =                                and cos[𝜃(𝑟, 𝑧)] =                              .
                                            √𝑝2 (𝑟,𝑧)+𝜂 2 (𝑟,𝑧)                            √𝑝2 (𝑟,𝑧)+𝜂2 (𝑟,𝑧)

          The gradients of the unit polarization can be written as
                                     𝜕𝑝                              𝜕𝜃 𝑥                      𝜕𝜑 𝜕𝛼                               𝜕𝜃 𝑥
                                          ≈ {cos[𝜃] cos[𝜑] 𝜕𝑟 𝑟 − sin[𝜃] sin[𝜑] 𝜕𝛼 𝜕𝑥 , cos[𝜃] sin[𝜑] 𝜕𝑟 𝑟 +
                                     𝜕𝑥
                                                                                           𝜕𝜑 𝜕𝛼                      𝜕𝜃 𝑥
                                                                     + sin[𝜃] cos[𝜑] 𝜕𝛼 𝜕𝑥 , − sin[𝜃] 𝜕𝑟 𝑟 },                      (F.2c)
                                     𝜕𝑝                              𝜕𝜃 𝑦                      𝜕𝜑 𝜕𝛼                              𝜕𝜃 𝑦
                                          ≈ {cos[𝜃] cos[𝜑] 𝜕𝑟 𝑟 − sin[𝜃] sin[𝜑] 𝜕𝛼 𝜕𝑦 , cos[𝜃] sin[𝜑] 𝜕𝑟 𝑟 +
                                     𝜕𝑦
                                                                                           𝜕𝜑 𝜕𝛼                      𝜕𝜃 𝑦
                                                                     + sin[𝜃] cos[𝜑] 𝜕𝛼 𝜕𝑦 , − sin[𝜃] 𝜕𝑟 𝑟 },                      (F.2d)
                                                                                                                              𝑦
Here we used 𝜕𝑟/𝜕𝑥 = 𝑥/𝑟 and 𝜕𝑟/𝜕𝑦 = 𝑦/𝑟. Below we use the following relations 𝑟 cos 𝛼 =
          𝜕𝛼    𝜕𝛼    𝑥            𝜕𝑟                 𝜕𝛼               𝜕𝛼           𝑦
𝑟 sin 𝛼 𝜕𝑦 ⇒ 𝜕𝑦 = 𝑟 2       and       sin 𝛼 + 𝑟 𝜕𝑥 cos α ⇒ 𝜕𝑥 = − 𝑟 2 .                    After      obvious,          but       tedious
                                   𝜕𝑥

transformations we obtain:
                                    𝜕𝑝       𝜕𝑝                   𝜕𝜃 𝜕𝜑 𝑥 𝜕𝛼        𝑦 𝜕𝛼     sin[𝜃] 𝜕𝜃 𝜕𝜑
                                  𝑝 [𝜕𝑥 × 𝜕𝑦 ] = sin[𝜃] 𝜕𝑟 𝜕𝛼 (𝑟 𝜕𝑦 − 𝑟 𝜕𝑥 ) ≡                                .                    (F.2e)
                                                                                               𝑟      𝜕𝑟 𝜕𝛼

Note, that this relation remains unchanged even if one could take into account the radial dependence
of polarization magnitude, 𝑃(𝑟, 𝑧) = √𝑃12 + 𝑃22 + 𝑃32 .
          Using the representation (F.2b) and reproducing the detailed calculations in Ref. [33], we
obtain:
                  𝑅               𝜕𝜃(𝑟,𝑧)          2𝜋 𝜕𝜑(𝛼,𝑧)           1
      𝑛(𝑧) = ∫0 sin[𝜃(𝑟, 𝑧)]                𝑑𝑟 ∫0                 𝑑𝛼 = 4𝜋 [cos[𝜃(𝑟, 𝑧)]]𝜃(𝑟=𝑅,𝑧)
                                                                                        𝜃(𝑟=0,𝑧)
                                                                                                 [𝜑(𝛼, 𝑧)]𝛼=2𝜋
                                                                                                          𝛼=0 (F.3a)
                                    𝜕𝑟                 4𝜋𝜕𝛼
                                                                               𝜋                                        𝜂(𝑟,𝑧)
Here R is the cylinder radius. Substituting here 𝜑(𝛼, 𝑧) ≈ 𝛼 − 2 and cos[𝜃(𝑟, 𝑧)] =                                                    we
                                                                                                                  √𝑝2 (𝑟,𝑧)+𝜂2 (𝑟,𝑧)

obtain

                                                                25
                                  1         𝜂(𝑅,𝑧)                    𝜂(0,𝑧)                          𝜂(0,𝑧)
                           𝑛(𝑧) ≈ 2 (                       −                         )=−                            ,          (F.3b)
                                       √𝑝2 (𝑅,𝑧)+𝜂2 (𝑅,𝑧)        √𝑝2 (0,𝑧)+𝜂2 (0,𝑧)             2√𝑝2 (0,𝑧)+𝜂 2 (0,𝑧)

since 𝜂(𝑅, 𝑧) = 0 and 𝑝(𝑅, 𝑧) > 0.
        The dependence 𝑛(𝑧) is shown in Fig. S10a for zero (green horizontal line), positive (3 solid
curves), and negative (3 dashed curves) flexoelectric tensor coefficients 𝐹𝑖𝑗 . The black curves 𝐹𝑖𝑗 values
are listed in Table SI; the red curves are calculated for twice the value of 𝐹𝑖𝑗 (labeled as “2𝐹𝑖𝑗 ”) and
the blue curves are calculated for six times the value of 𝐹𝑖𝑗 (labeled as “6𝐹𝑖𝑗 ”). The Z-profile of the
axial polarization 𝑃3 (0, 𝑧) and polarization magnitude 𝑃(0, 𝑧) are shown in Fig. S10b and Fig. S10c,
respectively. Symbols are calculated by FEM for positive 𝐹𝑖𝑗 (black diamonds), 2𝐹𝑖𝑗 (red triangles)
and 6𝐹𝑖𝑗 (blue squires). An applied voltage is absent in Fig. S10.
        Solid and dashed curves are the interpolation functions.
                                                𝑧                              𝑧+z                  𝑧−z
                               𝑃3 (0, 𝑧) = 𝑓 𝐿 (1 + 𝐴𝑧 2 ) (tanh [ z 𝑚] − tanh [ z 𝑚 ]),                                         (F.4a)
                                                                                 0                     0

                                            1          𝑧2                             𝑧+z                   𝑧−z
                            𝑃(0, 𝑧) = 𝑔 𝐿 √1 + 𝐵 (1 + 𝐴𝑧 2 ) (tanh [ z 𝑚] − tanh [ z 𝑚]),                                       (F.4b)
                                                                                          0                      0

                                                                        f       𝑧
                                                          𝑛(𝑧) = − 𝑔                   .                                         (F.4c)
                                                                            √1+(𝑧 2 ⁄𝐵)

Here 𝑓, 𝑔, 𝐴, 𝐵, z0 , and z𝑚 are the fitting parameters to FEM results, which are listed in Table SII.
The length scale 𝐿 = 1 nm. The amplitude 𝑓 increases with the increase of flexoelectric coupling
strength and saturates at high |𝐹𝑖𝑗 |. Since the value 𝑃(0, 𝑧) is very close to the 𝑃3 (0, 𝑧) near the cylinder
end, but 𝑃3 (0, 𝑧) vanishes in the nanoparticle center, the topological index continuously changes from
-½ to +½ with a z-coordinate change from one cylinder end (𝑧 = −20 nm) to another (𝑧 = +20 nm).


                                 Table SII. Fitting parameters for Eqs.(F.4)

    Fitting                                                 Flexoelectric coefficients 𝐹𝑖𝑗
   parameter       −6𝐹𝑖𝑗         −2𝐹𝑖𝑗              −𝐹𝑖𝑗               0                  𝐹𝑖𝑗           2𝐹𝑖𝑗              6𝐹𝑖𝑗
  𝑓 (μC/cm2)       –0.011       –0.0071         –0.0045                 0             0.0045          0.0071             0.011
  𝑔 (μC/cm2)       0.0305       0.0224           0.0174               N/A             0.0174          0.0224             0.0305
   𝐴 (nm-2)        0.0100       0.0125           0.0110               N/A             0.0110          0.0125             0.0100
    𝐵 (nm2)          5            10                 15               N/A                 15               10              5
    z0 (nm)          1.8          2.2                2.3              N/A              2.3                 2.2            1.8
   z𝑚 (nm)          17.8         17.5               17.5              N/A              17.5             17.5              17.8




                                                            26
         Topological index n                                                       (a)


                                                    - - - 6Fij ≪ 0                                                                 6Fij ≫ 0
                                                    - - - 2Fij < 0       Fij = 0                                                   2 Fij > 0
                                                    - - - - Fij < 0                                                                  Fij > 0




                                                                    z coordinate (nm)
  Axial polarization P3(0,z) (μC/cm2)




                                                          (b)                                                                      (c)
                                                                                       Full polarization P(0,z) ((μC/cm2)




                                                                                                                              ___6Fij ≫ 0
                                                                                                                              ___2 Fij > 0
                                                                                                                              ___ Fij > 0




                                                  z-coordinate (nm)                                                         z-coordinate (nm)

Figure S10. (a) Z-dependence of the polarization orientation topological index 𝑛(𝑧) for zero (green horizontal
line), positive (solid curves), and negative (dashed curves) flexoelectric tensor coefficients 𝐹𝑖𝑗 . For the black
curves 𝐹𝑖𝑗 values are listed in Table S1, for the red curves we used 2𝐹𝑖𝑗 , and blue curves, we used 6𝐹𝑖𝑗 . (b-c)
Z-profile of the axial polarization 𝑃3 (b) and polarization magnitude 𝑃 (c) calculated at 𝑟 = 0. Symbols are
calculated by FEM for positive 𝐹𝑖𝑗 (black diamonds), 2𝐹𝑖𝑗 (red triangles), and 6𝐹𝑖𝑗 (blue squires). Solid and
dashed curves are fitting functions listed in the text. Referenced values of 𝐹𝑖𝑗 and all other parameters are given
in Table SI. Temperature 𝑇 = 300 𝐾, 𝑈 = 0.


                                        As a next step, let us calculate the toroidal moment (TM):
                                                                                ⃗⃗ = 1 ∫ [𝑃⃗ × 𝑟]𝑑 3 𝑟
                                                                                𝑀                                                               (F.5)
                                                                                     𝑉 𝑉


                                                                                  27
The integration here is performed over the nanoparticle volume 𝑉 = 𝜋𝑅 2 ℎ. The toroidal moment (F.5)
is independent on the coordinate origin of radius-vector 𝑟, only if all three components of electric
polarization have a zero average over the nanoparticle volume. This is true in the considered case for
𝑈 = 0 (no applied voltage).
       Let us estimate the toroidal moment using the following approximation for polarization
distribution:
                                              𝑃1 ≈ 𝑝(𝑟, 𝑧) sin[𝛼],    𝑃2 ≈ −𝑝(𝑟, 𝑧) cos[𝛼],        𝑃3 ≈ 𝜂(𝑟, 𝑧),   (F.6a)
where the coordinates are
                                                 𝑥 = 𝑟 cos[𝛼],        𝑦 = 𝑟 sin[𝛼],                     𝑧 = 𝑧.     (F.6a)
The vectorial product is:
       [𝑃⃗ × 𝑟] = −𝑒⃗⃗⃗𝑥 (𝑝(𝑟, 𝑧) cos[𝛼] 𝑧 + 𝜂(𝑟, 𝑧)𝑟 sin[𝛼]) + ⃗⃗⃗⃗
                                                                𝑒𝑦 (𝜂(𝑟, 𝑧)𝑟 cos[𝛼] − 𝑝(𝑟, 𝑧) sin[𝛼] 𝑧) +
                                                                                          𝑒𝑧 𝑝(𝑟, 𝑧)𝑟
                                                                                          ⃗⃗⃗                      (F.7a)
After the integration we obtain that only the z-component of the TM is nonzero:
                                                                    2 𝑅
                                                           ⃗⃗ ≈ ⃗⃗⃗
                                                           𝑀    𝑒𝑧 𝑅2 ∫0 𝑝(𝑟, 𝑧)𝑟𝑑𝑟.                               (F.7b)

Since the magnitude 𝑝(𝑟, 𝑧) is almost independent of the flexoelectric coupling (see e.g. Fig. S5, the
middle row), the TM appears nearly the same for zero, positive, and negative flexoelectric tensor
coefficients. To make an analytical estimate in Eq.(F.7b), one can use the following approximation for
                                                   𝑟
the magnitude 𝑝(𝑟, 𝑧) ≅ 𝑝0 𝑡𝑎𝑛ℎ (𝑟 ), where the 𝑝0 and 𝑟0 are temperature-dependent. This results in:
                                                   0
                                                            2                         2                      2
                                          𝜋
                      𝑀    𝑒𝑧 𝑝0 {1 − 𝑑2 (12 + PolyLog [2, −𝑒 −𝑑 ]) + 2𝑑Log [1 + 𝑒 −𝑑 ]},
                      ⃗⃗ ≈ ⃗⃗⃗                                                                                      (F.8)
            𝑟
where 𝑑 = 𝑅0 and PolyLog[𝑥] is a polylogarithmic function. Figure S11 shows the dependence of the
                𝑀
normalized TM 𝑝 on the parameter d.
                 0
                            Mz (rel. units)




                                                                     Ratio r0/R
                                                                              𝑀
Figure S11. The dependence of the normalized toroidal moment 𝑝 on the parameter d.
                                                                                  0




                                                                     28
                                                                   ⃗⃗ = 1 ∫ [𝑃⃗ × 𝑟]𝑑 3 𝑟, appears almost
        In contrast to the topological index, the toroidal moment, 𝑀    𝑉 𝑉

                                                                                        ⃗⃗ is, for the most
the same for zero, positive, and negative flexoelectric tensor coefficients. The reason 𝑀
                                                     ⃗⃗ is equal to the integral of polarization magnitude
part, unaffected by the flexoelectric effect is that 𝑀
                            2   𝑅
                ⃗⃗ ≈ ⃗⃗⃗
𝑝(𝜌, 𝑧), namely 𝑀    𝑒𝑧 𝑅2 ∫0 𝑝(𝜌, 𝑧)𝜌𝑑𝜌, where the magnitude 𝑝(𝜌, 𝑧) is nearly independent on the

flexoelectric coupling (e.g., Fig. S5, the middle row).


                                                   References

1        S. Lin, T. Lü, C. Jin, and X. Wang. Size effect on the dielectric properties of BaTiO3 nanoceramics in
a modified Ginsburg-Landau-Devonshire thermodynamic theory. Phys. Rev. B 74, 134115 (2006).

2        E. A. Eliseev, A. V. Semchenko, Y. M. Fomichov, M. D. Glinchuk, V. V. Sidsky, V. V. Kolos, Yu M.
Pleskachevsky, M. V. Silibin, N. V. Morozovsky, and A. N. Morozovska. Surface and finite size effects impact
on the phase diagrams, polar, and dielectric properties of (Sr, Bi)Ta2O9 ferroelectric nanoparticles. J. Appl. Phys.
119, 204104 (2016).

3        E. A. Eliseev, Y. M. Fomichov, S. V. Kalinin, Y. M. Vysochanskii, P. Maksymovich and A. N.
Morozovska. Labyrinthine domains in ferroelectric nanoparticles: Manifestation of a gradient-induced
morphological phase transition. Phys. Rev. B 98, 054101 (2018).

4        A. N. Morozovska, Y. M. Fomichov, P. Maksymovych, Y. M. Vysochanskii, and E. A. Eliseev.
Analytical description of domain morphology and phase diagrams of ferroelectric nanoparticles. Acta Mater.
160, 109 (2018).

5        A. N. Morozovska, M. D. Glinchuk, E. A. Eliseev. Phase transitions induced by confinement of ferroic
nanoparticles. Phys. Rev. B 76, 014102 (2007).

6        H. Huang, C. Q. Sun, P. Hing. Surface bond contraction and its effect on the nanometric sized lead
zirconate titanate. J. Phys.: Condens. Matter 12, L127 (2000).

7        H. Huang, C. Q. Sun, Z. Tianshu, P. Hing. Grain-size effect on ferroelectric Pb(Zr1−xTix)O3 solid
solutions induced by surface bond contraction. Phys. Rev. B 63, 184112 (2001).

8        W. Ma. Surface tension and Curie temperature in ferroelectric nanowires and nanodots. Appl. Phys. A
96, 915 (2009).

9        J. J. Wang, X. Q. Ma, Q. Li, J. Britson, Long-Qing Chen. Phase transitions and domain structures of
ferroelectric nanoparticles: Phase field model incorporating strong elastic and dielectric inhomogeneity, Acta
Mater. 61, 7591 (2013).

10       J. J. Wang, E. A. Eliseev, X. Q. Ma, P. P. Wu, A. N. Morozovska, and L.-Q. Chen. Strain effect on
phase transitions of BaTiO3 nanowires. Acta Mater. 59, 7189 (2011).



                                                        29
11      A. N. Morozovska, E. A. Eliseev, Y. A. Genenko, I. S. Vorotiahin, M. V. Silibin, Ye Cao, Y. Kim, M.
D. Glinchuk, and S. V. Kalinin. Flexocoupling impact on the size effects of piezo- response and conductance
in mixed-type ferroelectrics-semiconductors under applied pressure. Phys. Rev. B 94, 174101 (2016).

12       L. D. Landau, and I. M. Khalatnikov. On the anomalous absorption of sound near a second order
phase transition point. In Dokl. Akad. Nauk SSSR, 96, 469 (1954).

13      J. Hlinka. Mobility of Ferroelectric Domain Walls in Barium Titanate. Ferroelectrics 349, 49 (2007).

14      J. Hlinka and P. Márton. Phenomenological model of 90-degree domain wall in BaTiO3 type
ferroelectrics. Phys. Rev. B 74, 104104 (2006).

15       A. K. Tagantsev, G. Gerra, and N. Setter. Short-range and long-range contributions to the size effect
in metal-ferroelectric-metal heterostructures. Phys. Rev. B 77, 174111 (2008).

16       M. Stengel and N. A. Spaldin, Origin of the dielectric dead layer in nanoscale capacitors, Nature
(London) 443, 679 (2006).

17       M. Stengel, D. Vanderbilt, and N. A. Spaldin. First-principles modeling of ferroelectric capacitors via
constrained displacement field calculations. Phys. Rev. B 80, 224110 (2009).

18       S.P. Timoshenko, J.N. Goodier. Theory of Elasticity. McGraw-Hill, N. Y., 1970.

19       A.J. Bell. Phenomenologically derived electric field-temperature phase diagrams and piezoelectric
coefficients for single crystal barium titanate under fields along different axes, J. Appl. Phys. 89, 3907 (2001).

20       D. Berlincourt, and H. Jaffe. Elastic and piezoelectric coefficients of single-crystal barium titanate.
Phys. Rev. 111, 143 (1958).

21       I. Ponomareva, A.K. Tagantsev, L. Bellaiche. Finite-temperature flexoelectricity in ferroelectric thin
films from first principles, Phys. Rev. B 85, 104101 (2012).

22       G. Shirane, and A. Takeda. Transition energy and volume change at three transitions in barium
titanate, J. Phys. Soc. Jap. 7, 1 (1952).

23       H. D. Megaw. Temperature changes in the crystal structure of barium titanium oxide. Proc. R. Soc.
Lond. A. 189, 261 (1947).
24
         A.N. Morozovska, E.A. Eliseev, M.D. Glinchuk. Ferroelectricity enhancement in confined nanorods:
Direct variational method, Phys. Rev. B. 73, № 21, 214106 (2006).
25       E. A. Eliseev, A. N. Morozovska, C. T. Nelson, and S. V. Kalinin. Intrinsic structural instabilities of
domain walls driven by gradient couplings: meandering anferrodistortive-ferroelectric domain walls in
BiFeO3. Phys. Rev. B, 99, 014112 (2019).
26       M. J. Han, E. A. Eliseev, A. N. Morozovska, Y. L. Zhu, Y. L. Tang, Y. J. Wang, X. W. Guo, X. L.
Ma. Mapping gradient-driven morphological phase transition at the conductive domain walls of strained
multiferroic films. Phys. Rev. B 100, 104109 (2019).


                                                        30
27      A. N. Morozovska, E. A. Eliseev, C. M. Scherbakov, and Y. M. Vysochanskii. The influence of
elastic strain gradient on the upper limit of flexocoupling strength, spatially-modulated phases and soft phonon
dispersion in ferroics. Phys. Rev. B 94, 174112 (2016).

28      A. N. Morozovska, E. A. Eliseev, R. Hertel, Y. M. Fomichov, V. Tulaidan, V. Yu. Reshetnyak, and
D. R. Evans. Electric Field Control of Three-Dimensional Vortex States in Core-Shell Ferroelectric
Nanoparticles. Acta Materialia, 200, 256 (2020).

29      A. N. Morozovska, E. A. Eliseev, Y. M. Fomichov, Y. M. Vysochanskii, V. Yu. Reshetnyak, and D.
R. Evans. Controlling the domain structure of ferroelectric nanoparticles using tunable shells. Acta Materialia,
183, 36 (2020).

30      E. A. Eliseev, A. N. Morozovska, R. Hertel, H. V. Shevliakova, Y. M. Fomichov, V. Yu. Reshetnyak,
and D. R. Evans. Flexo-Elastic Control Factors of Domain Morphology in Core-Shell Ferroelectric
Nanoparticles: Soft and Rigid Shells. Acta Materialia, 212, 116889 (2021).

31      B. A. Strukov and A.P. Levanyuk, Ferroelectric Phenomena in Crystals, Springer 1998.

32      K. Everschor-Sitte, J. Masell, R. M. Reeve, and M. Kläui. Perspective: Magnetic skyrmions—
Overview of recent progress in an active research field. J. Appl. Phys. 124, 240901 (2018).

33      https://physics.stackexchange.com/questions/587236/skyrmion-number




                                                       31

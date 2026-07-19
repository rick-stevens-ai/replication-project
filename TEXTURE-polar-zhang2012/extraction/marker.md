<!--
NOTE ON EXTRACTION PROVENANCE
=============================
This is the MARKER (prose) extraction artifact for arXiv:1211.0762.
The real `marker` binary (datalab-to/marker) is NOT installed on this host;
only poppler's `pdftotext` is available. This file is the DOCUMENTED INTERIM
FALLBACK: `pdftotext -layout` output, which best preserves column/section/
figure-caption structure so the paper reads as prose.

Fidelity note: Unicode/LaTeX math is DEGRADED by pdftotext (superscripts,
Greek, and matrix layout break). This is a known extraction-tooling limit,
NOT a physics gap. The authoritative, hand-transcribed equations live in
  ../report/REPORT.tex   (numbered, full LaTeX)
  ./nougat.mmd           (Key-equations block, LaTeX)

Regenerate with the real tool when available:
  marker_single textures-polar-zhang2012.pdf ./ --output_format markdown
-->

# Spin-orbital Texture in Topological Insulators

*(pdftotext -layout interim extraction — prose/structure preserving)*

                                                                                  Spin-orbital Texture in Topological Insulators
                                                                                    Haijun Zhang1 , Chao-Xing Liu2 & Shou-Cheng Zhang1
                                                                   1
                                                                    Department of Physics, McCullough Building, Stanford University, Stanford, CA 94305-4045
                                                            2
                                                                Department of Physics, The Pennsylvania State University, University Park, Pennsylvania 16802-6300
                                                                                                  (Dated: November 27, 2024)
                                                                    Relativistic spin-orbit coupling plays an essential role in the field of topological in-
                                                                 sulators and quantum spintronics. It gives rise to the topological non-trivial band
                                                                 structure and enables electric manipulation of the spin degree of freedom. Because of
arXiv:1211.0762v1 [cond-mat.mes-hall] 5 Nov 2012




                                                                 the spin-orbit coupling, rich spin-orbital coupled textures can exist both in momentum
                                                                 and in real space. For three dimensional topological insulators in the Bi2 Se3 family,
                                                                 topological surface states with pz orbitals have a left-handed spin texture for the upper
                                                                 Dirac cone and a right-handed spin texture for the lower Dirac cone. In this work, we
                                                                 predict a new form of the spin-orbital texture associated with the px and py orbitals.
                                                                 For the upper Dirac cone, a left-handed (right-handed) spin texture is coupled to the
                                                                 “radial” (“tangential”) orbital texture, whereas for the lower Dirac cone, the coupling
                                                                 of spin and orbital textures is the exact opposite. The “tangential” (“radial”) orbital
                                                                 texture is dominant for the upper (lower) Dirac cone, leading to the right-handed spin
                                                                 texture for the in-plane orbitals of both the upper and lower Dirac cones. A spin-
                                                                 resovled and photon polarized angle-resolved photoemission spectroscopy experiment
                                                                 is proposed to observe this novel spin-orbital texture.

                                                                 PACS numbers: 71.20.-b,73.43.-f,73.20.-r


                                                                       I.   INTRODUCTION                                a           ky                    b        ky


                                                      Three-dimensional topological insulators (TIs) are new                                      kx                            kx
                                                   states of quantum matter with helical gapless surface
                                                   states consisting of odd number of Dirac cones inside
                                                   the bulk band gap protected by time-reversal symmetry
                                                   (TRS).1–4 The underlying physical origin of the topo-
                                                   logical property of TIs is the strong spin-orbit coupling
                                                   (SOC), which plays a similar role as the Lorentz force in
                                                   the Quantum Hall state. Due to the SOC interaction, the        FIG. 1. (color online) a, b, The tangential orbital texture
                                                   spin and momentum are locked to each other, forming a          with the right-handed helical spin texture (a) and the radial
                                                   spin texture in the momentum space for the surface states      orbital texture with the left-handed helical spin texture (b)
                                                   of TIs5–7 . The spin texture has been directly observed        for the upper Dirac cone.
                                                   in the spin-resolved angle-resolved photon emission spec-
                                                   troscopy (spin-resolved ARPES)8–12 . The spin texture
                                                                                                                  (px and py orbitals) reveal more intriguing features: for
                                                   gives rise to a non-trivial Berry phase for the topological
                                                                                                                  the upper Dirac cone of surface states, a “radial” orbital
                                                   surface states and suppresses the backscatterings under
                                                                                                                  texture is coupled to a left-handed spin texture and a
                                                   TRS, leading to possible device applications in spintron-
                                                                                                                  “tangential” orbital texture is coupled to a right-handed
                                                   ics.
                                                                                                                  spin texture. For the lower Dirac cone, the coupling be-
                                                      Besides the spin texture, it has also been shown re-        tween spin and orbital textures is exactly opposite. An
                                                   cently that the atomic p orbitals of the Bi2 Se3 family of     electron spin-resolved and photon polarized ARPES ex-
                                                   topological insulators form a pattern in the momentum          periment is proposed to observe this novel spin-orbital
                                                   space, dubbed as the orbital texture, for the topological      texture of the surface states of TIs.
                                                   surface states.13,14 In this work, we predict a coupled
                                                   spin-orbital texture for the topological surface states.
                                                   Based on both the effective k· p theory and ab-initio cal-               II.     EFFECTIVE THEORY OF THE
                                                   culations, we find, besides the usual locking between the                        SPIN-ORBITAL TEXTURE
                                                   electron spin and the crystal momentum, the spin tex-
                                                   ture is also locked to the atomic orbital texture, which is      The surface states of TIs are described by the Dirac
                                                   dubbed as “spin-orbital texture”. We show that pz or-          type of effective Hamiltonian5,15
                                                   bitals have left-handed spin texture for the upper Dirac
                                                                                                                                  Hsurf (kx , ky ) = ~vf (σ x ky − σ y kx ) ,        (1)
                                                   cone and right-handed spin texture for the lower Dirac
                                                   cone, sharing the same feature as the total spin texture       with the Fermi velocity vf and Pauli matrix σ. The
                                                   of the surface states. In contrast, the in-plane orbitals      salient feature of this effective Hamiltonian is the “spin-
                                                                                                                                     2


          a                                                               b




                                                                          c




FIG. 2. (color online) a, The Dirac cone of Bi2 Se3 on the surface with the normal direction [0001] with the spin texture marked
by blue arrows. b, c, The projection of pz orbital and the related in-plane spin texture for upper (b) and lower (c) Dirac
cones. More red means more pz character. The red arrows represent the in-plane spin texture related to the pz orbitals. The
insets are the schematics of the spin texture marked by green arrows.


momentum locking”, which means for a fixed momentum                 symmetry considerations. Generally the basis |Ψ± 21 i de-
k, the “spin”, denoted by the Pauli matrix σ, has a fixed           pends on the momentum k and we can expand it up to
direction for the eigenstate of the Hamiltonian. Since the                                                  (0)        (1)
                                                                    the first order in k as |Ψ± 21 i = |Ψ± 1 i + |Ψ± 1 i. Here we
“spin” is always perpendicular to the momentum, we can                                                        2          2
                                                                    are only interested in the p orbitals of Bi and Se atoms in
introduce a helicity operator, defined as ĥ = k1 ẑ · (~k × ~σ )   the topological insulator Bi2 Se3 and can decompose the
which commutates with the Hamiltonian, to determine                 zeroth-order wavefunction as
the handness of the “spin” texture. For the upper Dirac
                                                                           (0)
                                                                                  X
cone of surface states, the helical operator ĥ = −1, lead-             |Ψ± 1 i =     [u0,α |α, pz , ↑ (↓)i + v0,α |α, p± , ↓ (↑)i] (2)
                                                                             2
ing to a left-handed “spin” texture in the momentum                                 α
space while for the lower Dirac cone, ĥ = 1 yields a a             and the first-order wavefunction as
right-handed “spin” texture. However, one should note                 (1)
                                                                              X
that here the “spin” is not the real spin, but the total            |Ψ± 1 i =     [ ± k± (iu1,α |α, p∓ , ↑ (↓)i + iv1,α |α, pz , ↓ (↑)i)
                                                                        2
angular momentum J~ = S    ~ + L,
                                ~ which is a combination                       α                                                     (3)
of the real spin S~ and the orbital angular momentum L         ~                    ∓ iw1,α k∓ |α, p± , ↑ (↓)i]
due to SOC. Consequently, the basis of the surface effec-           where k± = kx ± iky , | ↑i and | ↓i denote the spin, |pz i
tive Hamiltonian (1) are denoted as |ΨJz =± 12 i with the           and |p± i = ∓ √12 (|px i ± i|py i) denote different p orbitals,
lower indices ± 21 representing the total angular momen-            and α denotes indices other than the spin and orbital,
tum along z direction. In order to understand what is               such as atom indices. Here u0(1),α , v0(1),α and w1,α are
the texture for the real spin S, ~ it is necessary to write         material-dependent parameters. By comparing with the
down the explicit form of the basis wavefunction |Ψ± 21 i.          ab-initio calculations, we find that we can take them to
                                                                    be real. |Ψ 21 i and |Ψ− 12 i are related to each other by
  The form of the basis |Ψ± 12 i can be constructed by              TRS. The expressions of the basis (2) and (3) can be
                                                                                                                                    3


                    a                                                    b




                    c                                                    d




FIG. 3. (color online) a, b, c, d, The px projection on the states of upper (a) and lower (c) Dirac cones, and the py projection
of upper (b) and lower (d) Dirac cones. More red means more px character in (a) and (c), and more red means more py
character in (b) and (d). The red arrows indicate the in-plane spin texture related to the orbitals. The insets are the schematics
of the spin texture.


substituted into the eigen
                        h wavefunctions of the    i Hamil-               Fig. 1a,b, respectively. From the expressions (4) and (5),
tonian (1), |Φ± i = √12 ±ie−iθk |Ψ 21 i + |Ψ− 21 i , yielding            we can clearly see that |pz i orbital is coupled to the left-
                                                                         handed spin texture | ↑θ i for the upper Dirac cone and
the following forms of the wavefunctions
                                                                         the right-handed spin texture | ↓θ i for the lower Dirac
            X                                                            cone. Furthermore, for the upper Dirac cone, the radial
    |Φ+ i =    [(u0,α − v1,α k)|α, pz , ↑θ i
                                                                         orbital texture |pr i is always coupled to the left-handed
               α
                                                                         spin texture | ↑θ i and the tangential orbital texture |pt i
                        i
                     − √ (v0,α − u1,α k − w1,α k)|α, pr , ↑θ i(4)        is always coupled to the right-handed spin texture | ↓θ i.
                         2                                               The situation is exactly opposite for the lower Dirac cone.
                        1                                                   The expressions (4) and (5) are the main analytical
                     + √ (v0,α − u1,α k + w1,α k)|α, pt , ↓θ i]
                         2                                               results of this paper, which show explicitly the spin-
                                                                         orbital texture. To confirm our analytical results, ab-
             X
   |Φ− i =         [(u0,α + v1,α k)|α, pz , ↓θ i
              α
                                                                         initio method is adopted to calculate the projection of
                       i                                                 surface states on the spin and orbital basis, defined by
                    + √ (v0,α + u1,α k + w1,α k)|α, pr , ↓θ i (5)        the quantity
                        2
                       1                                                               ±
                                                                                      Di,η = hΦ± |(|pi ihpi | ⊗ sη )|Φ± i,        (6)
                    − √ (v0,α + u1,α k − w1,α k)|α, pt , ↑θ i].
                        2
                                                                         where pi = px , py , pz for the three p orbitals, s0 = 12×2
Here | ↑θ (↓θ )i = √12 (+(−)ie−iθk | ↑i+ | ↓i) stands for the            denotes the charge part and sx,y,z denote the three Pauli
left-handed (right-handed) helical spin texture and |pr i =              matrices for the spin. In the following, we will compare
                                                                                                                         ±
cos θk |px i + sin θk |py i, |pt i = − sin θk |px i + cos θk |py i are   the analytical calculation of the intensity Di,η    with ab-
the radial and tangential orbital textures, as shown in                  initio calculations.
                                                                                                                                 4

         a                                                                b




                                                   px upper Dirac cone
         c                       0.06              py upper Dirac cone
                                                   px lower Dirac cone
                                                                         d 0.4
             Character Density




                                                   py lower Dirac cone
                                 0.05                                                  0.3




                                                                            Polarization
                                 0.04                                                  0.2

                                 0.03
                                                                                           0.1
                                 0.02
                                                                                            0
                                    0   1/2π   π     3/2π         2π                             0   0.04   0.08    0.12
                                               θ                                                      Energy (eV)

FIG. 4. (color online) a, b, The tangential orbital texture with the related in-plane spin texture for the upper Dirac cone (a)
and the radial orbital texture for the lower (b) from ab-initio calculations. More red means more px character, and more blue
means more py character. The red arrows represent the total in-plane spin texture related to px and py orbitals. c, The px
and py projections onto upper and lower Dirac cones. The solid curves are the px and py projections for the upper Dirac cone
at energy level 0.10eV, and the dashed for the lower Dirac cone at the energy −0.07eV. The basic feature is the π period which
exactly agrees with the prediction by the effective model. d, Orbital polarization Ppx . The energy of Dirac point is shifted to
be zero. The positive value of the orbital polarization represents the radial orbital texture, and the negative value represents
the tangential orbital texture. In order to plot more visually, the Ppx for the upper Dirac cone is inversed, marked by the red
color. Ppx is exact zero at Dirac point, which indicates the transition point between the tangential and radial orbital textures.


      III.     SPIN-ORBITAL TEXTURE FROM                                 of all the orbitals are only for the first Se and Bi atoms
               AB-INITIO CALCULATIONS                                    on the top surface of the free-standing model.
                                                                            The surface states of Bi2 Se3 consist of a single Dirac
   The Vienna Ab-initio Simulation Package (VASP)16,17                   cone at Γ point on one surface inside the large bulk band
is employed to carry out ab-initio calculations with the                 gap (∼ 0.3eV)5,21 , which provides an ideal material to
framework of the Perdew-Burke-Ernzerhof-type (PBE)18                     study the coupling of spin and orbital textures of sur-
generalized gradient approximation (GGA) of density                      face states. As the starting point, we compare the bulk
functional theory19 . Projector augmented wave (PAW)                     band structure of Bi2 Se3 with the previous calculation5
pseudo-potentials are used for all of the calculations in                and find good agreements. The surface states are ob-
this work20 . 10×10×10 and 10×10×1 are used for k-grid                   tained from the calculation of a free-standing structure
of bulk and free-standing calculations, respectively. The                with the normal direction [0001], as shown in Fig. 2a.
kinetic energy cutoff is fixed to 450eV. 6 quintuple layers              The blue arrows represent the spin texture, where the
(QLs) are fixed in the supercell for free-standing calcu-                spin is mainly lying in plane near the Dirac point. The
lations, and the thickness of vacuum is taken to be 50Å.                spin texture is left-handed for the upper Dirac cone and
The lattice constant and the atomic parameters are di-                   right-handed for the lower one, the same as the total
rectly obtained from experiments. SOC is included with                   angular momentum texture. To understand the under-
the non self-consistent calculation. In order to compare                 lying physics, we calculate the spin texture for different
with the result of ARPES experiments, the projections                    atomic orbitals. For pz orbitals, a left-handed helical
                                                                                                                                           5
                                                                                                   P
spin texture is found for the upper Dirac cone and a                          4[− sin θk , cos θk ] α (v0,α ∓ ku1,α
                                                                                                                 P)kw1,α , which shows a
right-handed texture for the lower Dirac cone, as shown                       right-handed spin texture when α (v0,α ∓ku1,α )kw1,α >
in Fig. 2b,c. The schematic of the spin texture are                           0. Especially, if k gets close zero, both the total spin tex-
shown in the inset. Here the background color indi-                           ture [Dx± , Dy± ] of the in-plane orbitals and the difference
cates the projection of pz orbitals, which is isotropic,                      between px and py orbitals Dp±x ,0 −Dp±y ,0 approaches zero,
and the red arrows represent the corresponding in-plane                       also as shown in Fig. 4a,b.
spin texture. The spin texture of pz orbitals can be re-                         Therefore, there is a transition from a tangential or-
produced with the expressions [Dp±z ,σx , Dp±z ,σy , Dp±z ,σz ] =             bital texture in the upper Dirac cone to a radial orbital
± α (u0,α ∓ v1,α k)2 [sin θk , − cos θk , 0] with ‘±’ for the
   P
                                                                              texture in the lower Dirac cone, switching exactly at the
upper and lower Dirac cone and ~k = (k, θk ) in the polar                     Dirac point. To quantitatively describe this transition,
coordinate.                                                                   we introduce a polarization quantity
   The spin textures for in-plane orbitals are shown in
Fig. 3a,b for the upper Dirac cone and in Fig. 3c,d for                                       Dpx ,0 (±, θ = 0) − Dpx ,0 (±, θ = 90)
                                                                                  Ppx (±) =                                              (9)
the lower Dirac cone, respectively. We find that the asso-                                    Dpx ,0 (±, θ = 0) + Dpx ,0 (±, θ = 90)
ciated spins for px and py orbitals don’t rotate clockwise
or anti-clockwise around the Dirac point as in the case                       with ‘±’ for upper and lower Dirac cones. The plot of
of pz orbitals, but instead, they take the form                               Ppx (±) is shown in Fig. 4d where the energy level of the
                                          2
                                       X v0,α                                 Dirac point is shifted to zero. In order to show the plot
    [Dp±x ,x , Dp±x ,y , Dp±x ,z ] = ∓        [sin θk , cos θk , 0] (7)       more visually, we reverse the value of the Ppx (+) for the
                                       α
                                          2                                   upper Dirac cone plotted with the red. The feature of
                                            2
                                         X v0,α                               Ppx (±) undoubtedly indicates that the state of the lower
    [Dp±y ,x , Dp±y ,y , Dp±y ,z ] = ±            [sin θk , cos θk , 0] (8)   Dirac cone forms a radial orbital texture, and the state of
                                         α
                                             2                                the upper Dirac cone forms a tangential orbital texture.
for small k around the Γ point. The corresponding spin                        The Dirac point is shown to be the exact transition point
textures are shown schematically in the inset of Fig. 3a,c                    from the tangential to radial orbital texture. This is ex-
for px orbitals in upper and lower Dirac cones and in                         actly the behavior observed in a recent experiment and
the inset of Fig. 3b,d for py orbitals. Unlike pz or-                         explained within the first principle calculations14 . The
bitals, the amplitude of px and py orbitals for the sur-                      numerical results fit well to the analytical calculation,
face states is not isotropic, but has 2θk angular depen-                      with the expression
dence around the Fermi surface, as shown in Fig. 4c.                                             P
We may take the difference of the amplitudes between                                           2 α (v0,α ∓ Eu1,α /~vf )Ew1,α /~vf
                                                                               Ppx (±) = ∓ P h                                         i
px and py orbitals, as shown by colors in Fig. 4a,b.                                                                 2     2 2     2 2
                                                                                              α (v0,α ∓ Eu1,α /~vf ) + E w1,α /~ vf
Here more red means more px character, and more blue                                                                                    (10)
means more py character. The angular dependence in-                           with the energy     E.      For   small E around   Dirac point,
                                                                                           P
dicates a tangential orbital texture for the upper Dirac                                        v0,α w1,α 2E
cone and a radial orbital texture for the lower Dirac                         Ppx (±) ∝ ∓ Pα (v    0,α )
                                                                                                         2 ~v
                                                                                                              f
                                                                                                                 shows the linear dependence
                                                                                               α

cone, as schematically shown by the inset of Fig. 4a,b,                       on energy, as found in Fig. 4d.
respectively. This orbital texture was experimentally ob-                       Although in-plane orbitals show different spin textures
served recently14 . Furthermore, we also plot the total                       compared to pz orbitals, we stress the pz orbitals (50%)
spin textures for in-plane orbitals on the same figure,                       dominate the states near the Dirac point with px and
which show a right-handed texture for both upper and                          py only around 30%. Therefore, the spin texture for the
lower Dirac cones. All these salient feature can be un-                       whole states show left-handed for the upper Dirac cone
derstood by the wavefunctions (4) and (5). For the up-                        and right-handed for the lower Dirac cone, the same as
per Dirac cone, although both | ↑θ i|pr i and | ↓θ i|pt i                     that of pz orbitals, as well as the total angular momentum
terms exist in the wavefunction                                               texture.
                                 P (4), their associated coef- 2
ficients   are unequal. When       α (v0,α − u1,α k + w1,α k) >
                             2
P
   α (v0,α − u1,α k − w1,α k) , | ↓θ i|pt i term dominates over
| ↑θ i|pr i term, dominantly giving a tangential orbital tex-                                    IV.    DISCUSSION
ture coupled to a right-handed   P spin texture. Similarly,2for
the  lower   Dirac cone, when      α (v0,α + u1,α k + w1,α k) >                  In order to detect the spin texture of electrons, the
                               2
P
   α (v0,α + u1,α k − w1,α k) , | ↓θ i|pr i term in the wave-                 spin-resolved ARPES technology has been developed
function (5) is dominant, yielding a radial orbital texture                   by taking advantage of spin-dependent scatting pro-
coupled to a right-handed spin texture. The difference                        cesses and precisely measuring the magnitude of the
between px and py orbitals can       P be calculated directly                 asymmetry in the spin-dependent intensity with per-
as Dp±x ,0 − Dp±y ,0 = ∓2 cos 2θk α [(v0,α ∓ ku1,α )kw1,α ],                  fect spin-polarimeters.12 The non-trivial spin texture
which indeed shows a 2θk angular dependence, and                              of surface states of TIs has been clearly observed by
the total spin textures for in-plane orbitals can be ob-                      experiments.8–12 In addition, the orbital character can
tained as [Dx± , Dy± ] = [Dp±x ,x + Dp±y ,x , Dp±x ,y + Dp±y ,y ] =           be detected through the photon polarization selection
                                                                                                                            6

rules22 based on the symmetry analysis. With this tech-         tially motivated this work. This work is supported by the
nology, the orbital texture of surface states of Bi2 Se3 was    Defense Advanced Research Projects Agency Microsys-
reported recently by a polarized ARPES experiment.14            tems Technology Office, MesoDynamic Architecture Pro-
Therefore, it is possible to combine these two technologies     gram (MESO) through the contract number N66001-11-
together in an electron spin-resolved and photon polar-         1-4105 and by the DARPA Program on ”Topological
ized ARPES experiment, with both the spin and orbital           Insulators – Solid State Chemistry, New Materials and
textures extracted in the same measurement. The pre-            Properties”, under the award number N66001-12-1-4034.
dicted spin-orbital texture can be directly confirmed in
this type of experiment, which can explicitly reveal how
SOC plays a role in the real material at the atomic level.


            V.    ACKNOWLEDGMENTS

  We would like to thank Dr. Dan Dessau for sharing his
experimental data and for useful discussions, which par-




1
   X.-L. Qi and S.-C. Zhang, Physics Today 63, 33 (2010).          Chuang, D.-H. Lee, I. R. Fisher, R. J. Birgeneau, Z.-X.
2
   J. E. Moore, Nature 464, 194 (2010).                            Shen, Z. Hussain, and A. Lanzara, Phys. Rev. B 84,
 3
   M. Z. Hasan and C. L. Kane, Rev. Mod. Phys. 82, 3045            165113 (2011).
                                                                13
   (2010).                                                         S. R. Park, J. Han, C. Kim, Y. Y. Koh, C. Kim, H. Lee,
 4
   X.-L. Qi and S.-C. Zhang, Rev. Mod. Phys. 83, 1057              H. J. Choi, J. H. Han, K. D. Lee, N. J. Hur, M. Arita,
   (2011).                                                         K. Shimada, H. Namatame, and M. Taniguchi, Phys. Rev.
 5
   H. Zhang, C.-X. Liu, X.-L. Qi, X. Dai, Z. Fang, and S.-C.       Lett. 108, 046805 (2012).
                                                                14
   Zhang, Nature Physics 5, 438 (2009), 10.1038/nphys1270.         Y. Cao, J. A. Waugh, X.-W. Zhang, J.-W. Luo, Q. Wang,
 6
   W. Zhang, R. Yu, H.-J. Zhang, X. Dai, and Z. Fang, New          T. J. Reber, S. K. Mo, Z. Xu, A. Yang, J. Schneeloch,
   Journal of Physics 12, 065013 (2010).                           G. Gu, M. Brahlek, N. Bansal, S. Oh, A. Zunger, and D. S.
 7
   O. V. Yazyev, J. E. Moore, and S. G. Louie, Phys. Rev.          Dessau, ArXiv e-prints (2012), arXiv:1209.1016 [cond-
   Lett. 105, 266806 (2010).                                       mat.mtrl-sci].
 8                                                              15
   D. Hsieh, Y. Xia, L. Wray, D. Qian, A. Pal, J. H. Dil,          C.-X. Liu, X.-L. Qi, H. Zhang, X. Dai, Z. Fang, and S.-C.
   J. Osterwalder, F. Meier, G. Bihlmayer, C. L. Kane, Y. S.       Zhang, Phys. Rev. B 82, 045122 (2010).
                                                                16
   Hor, R. J. Cava, and M. Z. Hasan, Science 323, 919 (2009),      G. Kresse and J. Hafner, Phys. Rev. B 47, 558 (1993).
                                                                17
   http://www.sciencemag.org/content/323/5916/919.full.pdf.        G. Kresse and D. Joubert, Phys. Rev. B 59, 1758 (1999).
 9                                                              18
   S. Souma, K. Kosaka, T. Sato, M. Komatsu, A. Takayama,          J. P. Perdew, K. Burke, and M. Ernzerhof, Phys. Rev.
   T. Takahashi, M. Kriener, K. Segawa, and Y. Ando, Phys.         Lett. 77, 3865 (1996).
                                                                19
   Rev. Lett. 106, 216803 (2011).                                  P. Hohenberg and W. Kohn, Phys. Rev. 136, B864 (1964).
10                                                              20
   S.-Y. Xu, L. A. Wray, Y. Xia, F. v. Rohr, Y. S. Hor, J. H.      P. E. Blöchl, Phys. Rev. B 50, 17953 (1994).
                                                                21
   Dil, F. Meier, B. Slomski, J. Osterwalder, M. Neupane,          Y. Xia, D. Qian, D. Hsieh, L. Wray, A. Pal, H. Lin, A. Ban-
   H. Lin, A. Bansil, A. Fedorov, R. J. Cava, and M. Z.            sil, D. Grauer, Y. S. Hor, R. J. Cava, and M. Z. Hasan,
   Hasan, arXiv: cond-mat/1101.3985 (2011).                        Nature Physics 5, 398 (2009), 10.1038/nphys1274.
11                                                              22
   Z.-H. Pan, E. Vescovo, A. V. Fedorov, D. Gardner, Y. S.         A. Damascelli, Z. Hussain, and Z.-X. Shen, Rev. Mod.
   Lee, S. Chu, G. D. Gu, and T. Valla, Phys. Rev. Lett.           Phys. 75, 473 (2003).
   106, 257004 (2011).
12
   C. Jozwiak, Y. L. Chen, A. V. Fedorov, J. G. Analytis,
   C. R. Rotundu, A. K. Schmid, J. D. Denlinger, Y.-D.

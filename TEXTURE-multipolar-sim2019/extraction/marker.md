<!--
EXTRACTION ARTIFACT: marker.md  (PROSE artifact)
=================================================
NOTE ON PROVENANCE / FIDELITY:
  * The real `marker` binary (marker-pdf) is NOT installed on this host.
  * This file is the DOCUMENTED INTERIM FALLBACK: `pdftotext -layout` output,
    which preserves the paper's two-column reading flow and section structure.
  * Equation rendering is DEGRADED: Unicode math and the anti-commuting Dirac
    matrices / spherical-harmonic d_i(k) do not survive pdftotext cleanly.
    This is a known pdftotext limitation, NOT a physics gap.
  * AUTHORITATIVE equation transcriptions live in report/REPORT.tex and in the
    math artifact extraction/nougat.mmd.
  * Regenerate with the real tool when available:
        marker_single textures-multipolar-sim2019.pdf ./extraction --output_format markdown
-->

# Multipolar superconductivity in Luttinger semimetals (Sim et al. 2019, arXiv:1911.13224)

_Interim prose extraction (pdftotext -layout). See REPORT.tex for authoritative equations._

                                                                                  Multipolar superconductivity in Luttinger semimetals

                                                     GiBaik Sim,1, ∗ Archana Mishra,1, 2, † Moon Jip Park,1, ‡ Yong Baek Kim,3, 4, § Gil Young Cho,5, ¶ and SungBin Lee1, ∗∗
                                                                  1
                                                                      Department of Physics, Korea Advanced Institute of Science and Technology, Daejeon 305-701, Korea
                                                                          2
                                                                            International Research Centre MagTop, Institute of Physics, Polish Academy of Sciences,
                                                                                               Aleja Lotników 32/46, PL-02668 Warsaw, Poland
                                                                              3
                                                                                Department of Physics, University of Toronto, Toronto, Ontario M5S 1A7, Canada
                                                                                  4
                                                                                    School of Physics, Korea Institute for Advanced Study, Seoul 02455, Korea
                                                                                    5
                                                                                      Department of Physics, POSTECH, Pohang, Gyeongbuk 790-784, Korea
                                                                                                           (Dated: December 5, 2019)
                                                                  Topological superconductivity in multiband systems has received much attention due to a variety of possible
                                                               exotic superconducting order parameters as well as non-trivial bulk and surface states. While the impact of
arXiv:1911.13224v2 [cond-mat.str-el] 4 Dec 2019




                                                               coexisting magnetic order on superconductivity has been studied for many years, such as ferromagnetic super-
                                                               conductors, the implication of coexisting multipolar order has not been explored much despite the possibility
                                                               of multipolar hidden order in a number of f -electron materials. In this work, we investigate topological prop-
                                                               erties of multipolar superconductors that may arise when quadrupolar local moments are coupled to conduction
                                                               electrons in the multiband Luttinger semimetal. We show that the multipolar ordering of local moments leads to
                                                               various multipolar superconductors with distinct topological properties. We apply these results to the quadrupo-
                                                               lar Kondo semimetal system, PrBi, by deriving the microscopic multipolar Kondo model and examining the
                                                               possible superconducting order parameters. We also discuss how to experimentally probe the topological na-
                                                               ture of the Bogoliubov quasiparticles in distinct multipolar superconductors via doping and external pressure,
                                                               especially in the context of PrBi.


                                                     One of the foremost themes in contemporary condensed                   On the other hand, unlike the half-Heuslers addressed
                                                  matter physics is the realization of topological supercon-             above, other series of half-Heuslers like TbPdBi and HoPdBi
                                                  ductivity (TSC), where Bogoliubov-de Gennes (BdG) quasi-               exhibit unconventional superconductivity coexisting with
                                                  particles are characterized by non-trivial topology[1–4].              magnetic ordering from rare-earth ions Tb and Ho.[41, 42]
                                                  Among the numerous proposals to realize the TSCs[5–11],                These materials are extremely interesting platforms for the
                                                  a promient route is to utilize multiband or multi-orbital              study of the interplay between the magnetic degrees of free-
                                                  superconductivity[12–32], where the Cooper pairs possess               dom and unconventional superconductivity in multi-orbital
                                                  non-zero angular momentum through the interband pairing                systems. Furthermore, the pyrochlore oxide Cd2 Re2 O7 and Pr
                                                  channels. A representative example is the superconductiv-              based intermetallic compounds Pr(TM)2 X20 (TM=Ti,V,Rh,Ir
                                                  ity in pseudospin j = 3/2 Luttinger semimetals[33, 34] with            and X=Al,Zn) have recently been found to show coexistence
                                                  low-energy excitations described by quadratic band touching.           of multipolar order and superconductivity.[43–49] For exam-
                                                     The multiband nature of the Luttinger semimetals has moti-          ple, Pr(TM)2 X20 systems show superconductivity near and
                                                  vated intensive research on the possible unconventional super-         below the temperature where the multipolar ordering is de-
                                                  conductors supporting the Coopr pairs with higher pseudospin           veloped [48, 50–54]. Another semimetallic system, PrBi, is
                                                  angular momentum j [12–24]. In particular, it has been shown           known to have both the quadrupolar degrees of freedom com-
                                                  that the electron-electron interaction favors the d-wave pair-         ing from Pr ions and the j = 3/2 Luttinger semimetal. Re-
                                                  ing channels in the j = 2 manifold over the s-wave in the j            cent experiments on this material have confirmed the exis-
                                                  = 0 state[19]. Such unconventional superconductors possess             tence of ferro-quadrupolar order originating from the local-
                                                  a number of striking features including the emergent topolog-          ized moments of Pr ions, which may indicate the importance
                                                  ical boundary states and the Bogoliubov Fermi surfaces with            of the quadrupolar Kondo effect[55]. Such situation is anal-
                                                  non-trivial Chern numbers.[13–15, 35] All these interesting            ogous to ferromagnetic superconductors, where the presence
                                                  properties arise uniquely in multiband systems and result from         of magnetism can significantly alter the nature of the super-
                                                  the interplay between spin-orbit coupling and inter-band pair-         conducting state. Hence it is conceivable that the presence
                                                  ing channels.[13, 22] Among various candidate materials, a             of multipolar order could change the nature of the resulting
                                                  half-Heusler compound, YPtBi, shows the linear temperature             multipolar superconductors in some fundamental ways.
                                                  dependence of London penetration depth[36], indicating the                In this paper, motivated by the intertwined physics of mul-
                                                  existence of unconventional nodal line superconductivity. In           tipolar order and superconductivity, we discuss how their co-
                                                  addition, other half-Heusler compounds such as LuPdBi and              existence can give rise to multipolar superconductivity with
                                                  LaBiPt also exhibit superconductivity[37, 38]. These half-             unique topological properties. In particular, we consider PrBi
                                                  Heusler compounds have negligible anisotropies of the Fermi            system as a concrete example and derive the microscopic
                                                  surface near the quadratic band touching point[39, 40]. There-         quadrupolar Kondo model, where the non-Kramers doublet
                                                  fore, the Luttinger model with SO(3) or cubic symmetries               of the localized Pr moments and the Bi itinerant electrons
                                                  have been employed to explain the superconductivity in these           described by the Luttinger model are interacting with each
                                                  materials.[12, 17, 19, 23]                                             other. In the absence of quadrupolar order, we first discuss
                                                                                                                                               2
                                                                          P
the superconducting phases within the cubic symmetric Lut-                   a Hda with
tinger model. We find that time-reversal-symmetry break-
ing d-wave superconductors occur in the weak coupling limit,                             Hs = gs (ψ † γ45 ψ ∗ )(ψ T γ45 ψ),
while the time-reversal symmetry is restored in the strong cou-                        Hda = gda (ψ † γa γ45 ψ ∗ )(ψ T γ45 γa ψ),       (3)
pling limit. In the presence of quadrupolar order, however, we
                                                                          where gs = 41 (g0 + a ga ), gda = 41 (g0 + ga − b6=a gb ),
                                                                                                P                                 P
find that the superconducting instabilities are significantly al-
tered in the way that the quadrupolar order induces Fermi sur-            and γ45 = iγ4 γ5 . It is remarkable that the repulsive elec-
face distortion and stabilizes the multipolar superconductiv-             tron interaction with coefficients ga > 0 can naturally in-
ity with mixtures of distinct d-wave pairing order parameters.            duce the d-wave pairing instabilities.[19] For simplicity, we
Moreover, we find that these superconducting phases harbor                set coefficients ga = g1 and hence, gs = 41 (g0 + 5g1 ) and
topologically non-trivial gapless nodal line or nodal surface             gda = 41 (g0 − 3g1 ). In this work, we assume that the d-wave
excitations, the nature of which sensitively depending on the             pairing channel is attractive such that gda = −g and neglect
quadrupolar order. Thus, one could change the topological                 Hs . Within the standard mean-field decomposition, HI can
properties of the multipolar superconductors by controlling               be rewritten as follows up to the constant terms:
the coexisting multipolar oder. This would be a good exam-                              X
                                                                               HI = −g        (ψ † γa γ45 ψ ∗ )∆a + (ψ T γ45 γa ψ)∆∗a , (4)
ple of magnetic topological phases that could be controlled                                a
by magnetism. Based on our theory, we also propose vari-
ous experiments that can probe the topological nature of the              where the superconducting order parameters are explicitly
Bogoliubov quasiparticles in multipolar superconductors, an-              given as
ticipating potential applications to PrBi materials with doping                                        T
                                                                                                ∆a = hψ−k γ45 γa ψk i.                       (5)
and external pressure.
   Luttinger model and electron interaction — We start by                 The order parameter ∆a with a ∈ (1, 2, · · · 5) represents the
describing the kinetics of the itinerant electrons with the               d-wave quintet pairings (j = 2). In particular, ∆eg ≡(∆1 , ∆2 )
Luttinger-semimetal Hamiltonian,                                          represents the two d-wave pairings, (dx2 −y2 , d3z2 −r2 ) with eg
                                                                          symmetry, and ∆t2g ≡ (∆3 , ∆4 , ∆5 ) represents the three d-
                                   5
                                   X                                      wave pairings, (dyz , dzx , dxy ) with t2g symmetry. Through-
               H0 (k) = c0 k 2 +         ci di (k)γi −µ,           (1)    out our study, we consider the specific parameter set, which
                                   i=1                                    is relevant to PrBi, in Eq.(1) and analyze the properties of
                                                                          superconducting states; c0 = −6(a/π)2 eV, ceg ≡ c1 = c2 =
in four component spinor basis defined as ψ ≡                             −2(a/π)2 eV, and ct2g ≡c3 =c4 =c5 =−1(a/π)2 eV with the
(ψ3/2 , ψ1/2 , ψ−1/2 , ψ−3/2 ) and with the five 4 × 4                    lattice constant a and the chemical potential µ=−0.6eV, for
anti-commuting Dirac matrices, γi .[56] Here, µ is                        the cubic symmetric case. Here and below, we consider the
the chemical potential, di (k) represent           √ the five real        case where there are two distinct doubly degenerate Fermi sur-
l = 2 spherical harmonics with d1 = 3(kx2 − ky2 )/2,                      faces for µ < 0 (normal band structure). Although we focus
            2      2
                                   √                   √
         √ z − k )/2, d3 (k)= 3ky kz , d4 (k)= 3kz kx , and
d2 (k)=(3k                                                                on the specific parameter set, we emphasize that similar argu-
d5 (k)= 3kx ky . The Dirac matrices,γi , are explicitly given             ment holds for different cases and the emergence of complex
as γ1 = σ x ⊗ I, γ2 = σ z ⊗ σ z , γ3 = σ z ⊗ σ y , γ4 = σ z ⊗ σ x , and   superconducting states due to intertwined multipolar order is
γ5 = σ y ⊗ I where σ α are the Pauli matrices and I is the 2×2            a generic feature.
identity matrix. It is worth to note that Eq.(1) is a complete               We first briefly discuss the superconducting phases in the
representation of kinetics in Luttinger semimetal when both               absence of coexisting quadrupolar order, with the cubic sym-
inversion symmetry and time-reversal symmetry are present.                metric Luttinger model where the coefficients in Eq.(1) are
In Eq.(1), c0 quantifies the particle-hole asymmetry of the               of the form, |ceg |>|ct2g |. In general, the free energy for the
model, whereas, ci quantify the kinetic term proportional to              ∆eg pairing state is given as Feg = reg |∆eg |2 + q1 |∆eg |4 +
each of the d-wave harmonics. When all ci are the same, the               q2 (∆1 ∆∗2 − ∆2 ∆∗1 )2 while the free energy for the ∆t2g pair-
model in Eq. (1) becomes fully spherical symmetric retaining              ing state is given as Ft2g = rt2g |∆t2g |2 + q10 |∆t2g |4 + q20 |∆t2g ·
SO(3) symmetry. In the case of cubic symmetry, whereas,                   ∆t2g |2 + q30 (|∆3 |2 |∆4 |2 + |∆4 |2 |∆5 |2 + |∆5 |2 |∆3 |2 ).[57]
we have c1,2 6= c3,4,5 [23].                                              Within one-loop calculation, the instability towards the ∆eg
   We now discuss the superconductivity emerging from this                pairing is shown to be stronger than the ∆t2g pairing with
multiband Luttinger semimetal when the electron-electron in-              |ceg | > |ct2g |, i.e., reg < rt2g (See Section I of Supplemen-
teractions are present[19],                                               tary Information for details). For the ∆eg pairing, there are
                                                                          three possible superconducting states with the order param-
                                                                          eters ∆eg = (1, 0), (0, 1), and (1, i). By comparing the
                                    X
              HI = g0 (ψ † ψ)2 +          ga (ψ † γa ψ)2 .         (2)
                                     a                                    mean-field energy at zero temperature, for weak coupling
                                                                          limit, i.e., small g limit, we find that the time-reversal sym-
Using the Fierz identity, HI can be exactly rewritten in terms            metry breaking superconducting phase is chosen, which is de-
of the s-wave and d-wave pairing channels, HI = Hs +                      scribed by dx2 −y2 + id3z2 −r2 pairing or the order parameter
                                                                                                                                            3




                   0.4



                   0.3



                   0.2



                   0.1




                                               0.5                      1.                     1.5



FIG. 1. (color online) Multipolar superconducting phases as functions of J˜K hO20 i [(a/π)2 eV] and the interaction strength g [eV] with
c0 =−6(a/π)2 eV, ceg =c1 =c2 =−2(a/π)2 eV, cη =c3 =c4 =(−1 − J˜K hO20 i)(a/π)2 eV, c5 =−1(a/π)2 eV, and µ=−0.6eV based on Eq.(1)
and Eq.(7). We find four distinct superconducting states: time-reversal symmetry breaking state with dx2 −y2 + id3z2 −r2 pairing (purple
line), dyz +idzx pairing (blue), time-reversal symmetric state with d3z2 −r2 pairing (green), and dyz +dzx pairing (brown). Four insets show
the gap structure of these states. Note that the hO20 i = 0 vertical thick line corresponds to the case with the cubic symmetry in the absence
of quadrupolar order. Here, each semi transparent yellow surface represents the normal state Fermi surface. For multipolar superconductor
with time-reversal symmetry breaking, the Bogoliubov Fermi surfaces exist. Red, green and blue colored Bogoliubov Fermi surfaces indicate
distinct Chern numbers 2, 0, and −2 respectively. For multipolar superconductor with time-reversal symmetry, each solid (dashed) ring
indicates the nodal ring, which is protected by the non-trivial winding number 2 (−2). See the main text for more details.




∆eg = (1, i). In this phase, the Bogoliubov quasiparticles               (−2) which belongs to the 2Z classification of DIII Class[58].
form sixteen distinct pockets as shown in the bottom left inset
of Fig.1. Furthermore, we find that each pocket colored red
(blue) is characterized by non-trivial Chern number 2 (−2),
classified by 2Z Chern number corresponding to Class D in
the Altland-Zirnbauer classification with additional inversion              Multipolar Kondo coupling— When multipolar degrees of
symmetry[58].                                                            freedom are present in the system, one should consider an ef-
   With increasing interaction strength g, we observe the su-            fective Kondo coupling between the localized multipolar mo-
perconducting phase transition occurs from the dx2 −y2 +                 ments and itinerant electrons. In this section, we consider the
id3z2 −r2 pairing state to the time-reversal symmetric d3z2 −r2          microscopic model focusing on PrBi and derive the multipolar
pairing state. This phase transition can be understood as the            Kondo coupling between the eg -type quadrupolar moments in
effect of band flattening near the quadratic band touching               Pr3+ and the strongly spin-orbit coupled electrons of Bi 6p
point. More precisely, the electron interaction starts to domi-          orbitals. The eg -type quadrupolar degrees of freedom in the
nate over the kinetic energy at large g and the system behaves           cubic symmetric√model is represented in terms of the Stevens
similarly to the case with small µ due to the band flattening            operators O22 = 23 (Jx2 −Jy2 ) and O20 = 12 (3Jz2 −J 2 ) with the
near k = 0 which favors the d3z2 −r2 pairing state[19]. In               µ-th component of total angular momentum Jµ [59, 60]. Re-
Fig.1, the vertical thick line at J˜K hO20 i = 0 corresponds to          garding PrBi, we consider the interpenetrating face-centered
dx2 −y2 + id3z2 −r2 pairing and there is the phase transition to         cubic (FCC) lattice system, where the quadrupolar degrees of
d3z2 −r2 beyond that, as the interaction strength g increases.           freedom O22 and O20 of the localized electrons reside in one
The BdG energy spectrum of this phase possesses gapless                  FCC lattice and the itinerant electrons with p orbitals reside in
nodal rings as shown in the top left inset of Fig.1. In this             another FCC lattice (For details, see Fig.S3 in Supplementary
time-reversal symmetric superconductor, the solid (dashed)               Information). Then, one can write down the effective Kondo
nodal line is protected by a non-trivial winding numbers 2               coupling between the quadrupolar order parameters O22 and
                                                                                                                                      4

O20 and the itinerant p electrons as the following,                   represented as[66],
          XX                                                         Fη = rη |∆η |2 + q1 |∆η |4 + q2 |∆η ∆η |2 + q3 (|∆3 |4 + |∆4 |4 ).
                                                                 
HK = JK             O22 Γa1,ij c†iaα cjaα + O20 Γa2,ij c†iaα cjaα .
           hi,ji a,α                                                  Once the instability of the ∆η pairing gets stronger than the
                                                                (6)   ∆2 pairing, the phase transition to the ∆η pairing occurs. For
Here, c†iaα and ciaα are the electron creation and annihilation       weak coupling limit, the system develops time-reversal sym-
operators at site i with orbital a ∈ (x, y, z) and spin α ∈ (↑, ↓).   metry breaking superconductivity with the dyz + idzx pairing
Γa1,ij and Γa2,ij are site- and orbital-dependent form factors for    and the order parameters ∆η = (1, i). This result is distinct
the Kondo coupling with quadrupoles O22 and O20 respec-               from the cubic case, where the dx2 −y2 +id3z2 −r2 pairing with
tively (See Section II of Supplementary Information for de-           ∆eg = (1, i) is chosen. As shown in the bottom right in-
tails). We note that the quadrupolar degrees of freedom which         set of Fig.1, the Bogoliubov quasiparticles form four Fermi
is time-reversal symmetric, can only couple to the spin inde-         surfaces along kz axis with the Chern number ±2 and two
pendent electron hoppings with the form factors that trans-           Fermi surfaces located at kz = 0 with the Chern number 0.
form exactly the same as O22 and O20 . Now we take into ac-           With increasing g, the phase transition occurs favoring distinct
count j = 3/2 basis in the presence of the spin-orbit coupling        superconducting phase with the dyz + dzx pairing described
of p electrons and project Eq.(6) onto j = 3/2 basis with the         by the order parameter ∆η = (1, 1). In this case, the time-
projection operator Pj=3/2 [61]. Then one gets the following          reversal symmetry is recovered and the Bogoliubov quasipar-
Kondo coupling,                                                       ticles form four nodal rings with the winding numbers ±2 as
    H̃K (k) = Pj=3/2 HK (k)Pj=3/2                                     shown in the top right inset of Fig.1.
                 √                                                      Discussion — We have studied exotic multipolar supercon-
            = J˜K ( 3O20 +O22 )d3 (k)γ3                               ductors and their topological properties, which arise from the
               √                                                     intertwined multipolar order and electron correlations in the
            + ( 3O20 −O22 )d4 (k)γ4 − 2O22 d5 (k)γ5 , (7)             Luttinger semimetal. Considering the electron Coulomb in-
                                                                      teraction as the dominant driving force for superconductivity,
in four component spinor basis ψ and with J˜K ≡ JK ( πa )2 .          we have shown that the d-wave pairing channel in the pseu-
In Eq.(7), one can clearly see that O20 -type ferro-quadrupolar       dospin j = 2 manifold becomes attractive and there exists spe-
ordering breaks the three-fold rotation symmetry, while O22 -         cial selection of the d-wave superconducting order parame-
type ferro-quadrupolar ordering breaks both the three-fold and        ters. When the quadrupolar order of localized moments coex-
the four-fold rotation symmetries. Recent experiment on PrBi          ists, we have demonstrated how it can change the supercon-
compound has confirmed O20 -type ferro-quadrupolar order              ducting phases of the Luttinger semimetals. In particular, we
hO20 i =6 0, which has also been discussed within the Lan-            consider the eg -type quadrupolar order O20 and O22 present in
dau theory analysis on symmetry grounds[55, 62, 63]. Thus,            the cubic symmetric systems. We derived the effective Kondo
we focus on the case when O20 -type ferro-quadrupolar order           coupling between the quadrupolar local moments and con-
is present, hO20 i =
                   6 0 and hO22 i = 0.                                duction electrons via the microscopic model with spin-orbit-
   Ferro-quadrupolar order and superconductivity — When               coupled p electrons and projecting it onto the pseudospin j
hO20 i 6= 0, the symmetry of the system is lowered to D4h from        = 3/2 Luttinger Hamiltonian. It turns out that the onset of
Oh group[64, 65]. One can easily see from both Eq.(1) and             ferro-quadrupolar order largely affects the Fermi surface dis-
Eq.(7) that ferro-quadrupolar order gives rise to anisotropies        tortion, and thereby causes dramatic changes in preferred su-
in coefficients, c3 = c4 6= c5 and results in Fermi surface dis-      perconducting order parameters. We emphasize that such phe-
tortion. In this case, the coefficient cη≡c3=c4 is renormalized       nomena are quite unique in the interacting Luttinger semimet-
in Eq.(1) and the spontaneous Fermi surface distortion occurs         als with relatively small carrier densities, where the effective
via the effective Kondo coupling shown in Eq.(7). In partic-          Kondo coupling with the quadrupolar degrees of freedom can
ular, when the quadrupolar order induces the Fermi surface            sensitively control the nature of the superconducting order pa-
distortion, we find that the properties of the d-wave super-          rameters and the associated topological properties.
conductivity is dramatically changed. In Fig.1, we plot the              Recent experiments on the semimetallic compound PrBi
phase diagram within mean-field approximation as functions            have confirmed the existence of O20 -type ferro-quadrupolar
of J˜K hO20 i and the interaction strength g at zero tempera-         order below the transition temperature TQ = 0.08K[55]. In
ture. With the onset of O20 -type ferro-quadrupolar order, the        this material, the localized moments of Pr3+ ions form a Γ3
instability towards the ∆2 pairing is shown to be stronger than       non-Kramers doublet via strong spin-orbit coupling, which
the ∆1 pairing, which is consistent with the result of one-loop       only allows higher multipolar moments, but no dipole mo-
calculation (See Section I of Supplementary Information for           ment. Whereas, the itinerant electrons of Bi 6p orbitals form
details). Thus the system prefers the d3z2 −r2 pairing with           a strongly correlated Luttinger semimetal with small carrier
∆eg = (0, 1) in both weak and strong coupling limits. With            density[55, 67]. Since the system contains tiny carrier den-
further increase of J˜K hO20 i, however, the instability towards      sity, one may expect to control electron correlation via doping
the ∆η≡(∆3 , ∆4 ) pairing becomes stronger than the ∆2 pair-          and external pressure, resulting in superconductivity driven
ing. In general, the free energy for the ∆η pairing state is          by the interplay between the quadrupolar Kondo effect and
                                                                                                                                         5

the electron interaction. In such cases, as shown in Fig.1, the             Review B 86, 214514 (2012).
multipolar superconductivity with distinct d-wave pairing or-           [8] G. Bednik, A. Zyuzin, and A. Burkov, Physical Review B 92,
der parameters are stabilized and depending on the presence                 035153 (2015).
and absence of ferro-quadrupolar order, the character of super-         [9] Y. Li and F. Haldane, Physical review letters 120, 067003
                                                                            (2018).
conductivity and topological nature of the Bogoliubov quasi-           [10] S. Nadj-Perge, I. K. Drozdov, J. Li, H. Chen, S. Jeon, J. Seo,
particles may be sensitively changed. This can be verified by               A. H. MacDonald, B. A. Bernevig, and A. Yazdani, Science
probing surface modes using scanning tunneling microscope.                  346, 602 (2014).
Moreover, for multipolar superconductors with time-reversal            [11] Q. L. He, L. Pan, A. L. Stern, E. C. Burks, X. Che, G. Yin,
symmetry breaking pairing channels, the location of Bogoli-                 J. Wang, B. Lian, Q. Zhou, E. S. Choi, et al., Science 357, 294
ubov Fermi surfaces with non-trivial Chern numbers can be                   (2017).
sensitively changed, depending on distinct mixtures of the d-          [12] P. Brydon, L. Wang, M. Weinert, and D. Agterberg, Physical
                                                                            review letters 116, 177001 (2016).
wave pairings, i.e. dx2 −y2 + id3z2 −r2 or dyz + idzx as shown         [13] D. Agterberg, P. Brydon, and C. Timm, Physical review letters
in the bottom insets of Fig.1. Thus, one expects strong angle               118, 127001 (2017).
dependence of the Hall effect signal, which would distinguish          [14] C. Timm, A. Schnyder, D. Agterberg, and P. Brydon, Physical
different superconducting phases.                                           Review B 96, 094526 (2017).
   With growing interest on multipolar order, often termed as          [15] P. Brydon, D. Agterberg, H. Menke, and C. Timm, Physical
“hidden order”, it is now known that there exist many systems,              Review B 98, 224509 (2018).
                                                                       [16] H. Menke, C. Timm,           and P. Brydon, arXiv preprint
where both multipolar order and superconductivity may coex-
                                                                            arXiv:1909.10956 (2019).
ist. For instance, beyond the quadrupolar Kondo semimetal              [17] B. Roy, S. A. A. Ghorashi, M. S. Foster, and A. H. Nevidom-
PrBi, the materials like rare-earth half-heusler compounds,                 skyy, Physical Review B 99, 054505 (2019).
Pr based cage compounds Pr(Ti,V,Ir)2 (Al,Zn)20 and lacunar             [18] A. Szabo, R. Moessner,          and B. Roy, arXiv preprint
spinel compounds Ga(Ta,Nb)4 (S,Se)8 contain spin-orbit en-                  arXiv:1811.12415 (2018).
tangled pseudospin degrees of freedom and sometimes exhibit            [19] I. Boettcher and I. F. Herbut, Physical review letters 120,
(anti-) ferro-quadrupolar order in addition to superconductiv-              057002 (2018).
                                                                       [20] I. F. Herbut, I. Boettcher, and S. Mandal, Physical Review B
ity. In such cases, the multipolar Kondo coupling and strongly
                                                                            100, 104503 (2019).
interacting multi-orbital electrons play an important role to          [21] G. Sim, A. Mishra, M. J. Park, Y. B. Kim, G. Y. Cho, and
determine the characteristics of superconductivity. Our results             S. Lee, Physical Review B 100, 064509 (2019).
can be used to understand how these two phenomena can be               [22] J. W. Venderbos, L. Savary, J. Ruhman, P. A. Lee, and L. Fu,
intertwined with each other and how the topological proper-                 Physical Review X 8, 011029 (2018).
ties of multipolar superconductors could be controlled via the         [23] L. Savary, J. Ruhman, J. W. Venderbos, L. Fu, and P. A. Lee,
multipolar order. Our work provides an important platform for               Physical Review B 96, 214514 (2017).
                                                                       [24] W. Yang, Y. Li, and C. Wu, Physical review letters 117, 075301
the discovery of magnetic topological superconductors that
                                                                            (2016).
can be controlled by electron correlation or multipolar mag-           [25] C. Wu, J. Hu, and S.-C. Zhang, International Journal of Modern
netism.                                                                     Physics B 24, 311 (2010).
   Y.B.K. is supported by the NSERC of Canada, Canadian                [26] S. Tchoumakov, L. J. Godbout, and W. Witczak-Krempa, arXiv
Institute for Advanced Research, and Center for Quantum                     preprint arXiv:1910.04189 (2019).
Materials at the University of Toronto. G.Y.C. is supported            [27] M. A. Continentino, F. Deus, I. T. Padilha, and H. Caldas, An-
by BK21 plus program, POSTECH. A.M. is supported by                         nals of Physics 348, 1 (2014).
                                                                       [28] G. A. Hamilton, M. J. Park, and M. J. Gilbert, Physical Review
BK21 plus. G.B.S., M.J.P., and S.B.L. are supported by
                                                                            B 100, 134512 (2019).
the KAIST startup, BK21 and National Research Foundation               [29] M. Kriener, K. Segawa, Z. Ren, S. Sasaki, and Y. Ando, Phys-
Grant (NRF-2017R1A2B4008097).                                               ical review letters 106, 127004 (2011).
                                                                       [30] S. Deng, L. Viola, and G. Ortiz, Physical review letters 108,
                                                                            036803 (2012).
                                                                       [31] T. Kawakami, T. Okamura, S. Kobayashi, and M. Sato, Physi-
                                                                            cal Review X 8, 041026 (2018).
 [1] X.-L. Qi, T. L. Hughes, S. Raghu, and S.-C. Zhang, Physical       [32] G. Sim, M. J. Park,            and S. Lee, arXiv preprint
     review letters 102, 187001 (2009).                                     arXiv:1909.04015 (2019).
 [2] X.-L. Qi, T. L. Hughes, and S.-C. Zhang, Physical Review B        [33] J. M. Luttinger and W. Kohn, Physical Review 97, 869 (1955).
     81, 134508 (2010).                                                [34] J. Luttinger, Physical review 102, 1030 (1956).
 [3] M. Z. Hasan and C. L. Kane, Reviews of Modern Physics 82,         [35] H. Oh and E.-G. Moon, arXiv preprint arXiv:1911.08487
     3045 (2010).                                                           (2019).
 [4] M. Sato and Y. Ando, Reports on Progress in Physics 80,           [36] H. Kim, K. Wang, Y. Nakajima, R. Hu, S. Ziemak, P. Syers,
     076501 (2017).                                                         L. Wang, H. Hodovanets, J. D. Denlinger, P. M. Brydon, et al.,
 [5] L. Fu and C. L. Kane, Physical review letters 100, 096407              Science advances 4, eaao4513 (2018).
     (2008).                                                           [37] G. Goll, M. Marz, A. Hamann, T. Tomanic, K. Grube,
 [6] S. B. Chung, X.-L. Qi, J. Maciejko, and S.-C. Zhang, Physical          T. Yoshino, and T. Takabatake, Physica B: Condensed Matter
     Review B 83, 100512 (2011).                                            403, 1065 (2008).
 [7] G. Y. Cho, J. H. Bardarson, Y.-M. Lu, and J. E. Moore, Physical   [38] Y. Nakajima, R. Hu, K. Kirshenbaum, A. Hughes, P. Syers,
                                                                                                                                             6

     X. Wang, K. Wang, R. Wang, S. R. Saha, D. Pratt, et al., Sci-            S. Nakatsuji, Physical review letters 113, 267001 (2014).
     ence advances 1, e1500242 (2015).                                   [53] T. J. Sato, S. Ibuka, Y. Nambu, T. Yamazaki, T. Hong, A. Sakai,
[39] M. Meinert, Physical review letters 116, 137001 (2016).                  and S. Nakatsuji, Physical Review B 86, 184419 (2012).
[40] T. Oguchi, Physical Review B 63, 125115 (2001).                     [54] K. Matsubayashi, T. Tanaka, A. Sakai, S. Nakatsuji, Y. Kubo,
[41] H. Xiao, T. Hu, W. Liu, Y. Zhu, P. Li, G. Mu, J. Su, K. Li, and          and Y. Uwatoko, Physical review letters 109, 187004 (2012).
     Z. Mao, Physical Review B 97, 224511 (2018).                        [55] X. He, C. Zhao, H. Yang, J. Wang, K. Cheng, S. Jiang, L. Zhao,
[42] S. Radmanesh, C. Martin, Y. Zhu, X. Yin, H. Xiao, Z. Mao,                Y. Li, C. Cao, S. Wang, et al., arXiv preprint arXiv:1909.04446
     and L. Spinu, Physical Review B 98, 241111 (2018).                       (2019).
[43] M. Hanawa, Y. Muraoka, T. Tayama, T. Sakakibara, J. Yamaura,        [56] I. Boettcher and I. F. Herbut, Physical Review B 93, 205138
     and Z. Hiroi, Physical Review Letters 87, 187001 (2001).                 (2016).
[44] S.-W. Huang, H.-T. Jeng, J. Lin, W. Chang, J. Chen, G. Lee,         [57] M. Sigrist and K. Ueda, Reviews of Modern physics 63, 239
     H. Berger, H. Yang, and K. S. Liang, Journal of Physics: Con-            (1991).
     densed Matter 21, 195602 (2009).                                    [58] T. Bzdušek and M. Sigrist, Physical Review B 96, 155105
[45] J. Harter, Z. Zhao, J.-Q. Yan, D. Mandrus, and D. Hsieh, Sci-            (2017).
     ence 356, 295 (2017).                                               [59] K. Stevens, Proceedings of the Physical Society. Section A 65,
[46] Y. Matsubayashi, T. Hasegawa, N. Ogita, J.-i. Yamaura, and               209 (1952).
     Z. Hiroi, Physica B: Condensed Matter 536, 600 (2018).              [60] K. Lea, M. Leask, and W. Wolf, Journal of Physics and Chem-
[47] I. Ishii, H. Muneshige, S. Kamikawa, T. K. Fujita, T. Onimaru,           istry of Solids 23, 1381 (1962).
     N. Nagasawa, T. Takabatake, T. Suzuki, G. Ano, M. Akatsu,           [61] G. L. Stamokostas and G. A. Fiete, Physical Review B 97,
     et al., Physical Review B 87, 205106 (2013).                             085150 (2018).
[48] T. Onimaru, K. T. Matsumoto, Y. F. Inoue, K. Umeo, Y. Saiga,        [62] S. Lee, S. Trebst, Y. B. Kim, and A. Paramekanti, Physical
     Y. Matsushita, R. Tamura, K. Nishimoto, I. Ishii, T. Suzuki,             Review B 98, 134447 (2018).
     et al., Journal of the Physical Society of Japan 79, 033704         [63] F. Freyer, J. Attig, S. Lee, A. Paramekanti, S. Trebst, and Y. B.
     (2010).                                                                  Kim, Physical Review B 97, 115111 (2018).
[49] T. Onimaru, N. Nagasawa, K. Matsumoto, K. Wakiya,                   [64] J. Ruan, S.-K. Jian, H. Yao, H. Zhang, S.-C. Zhang, and
     K. Umeo, S. Kittaka, T. Sakakibara, Y. Matsushita, and T. Tak-           D. Xing, Nature communications 7, 11136 (2016).
     abatake, Physical Review B 86, 184426 (2012).                       [65] D. Shao, J. Ruan, J. Wu, T. Chen, Z. Guo, H. Zhang, J. Sun,
[50] A. Sakai, K. Kuga, and S. Nakatsuji, Journal of the Physical             L. Sheng, and D. Xing, Physical Review B 96, 075112 (2017).
     Society of Japan 81, 083702 (2012).                                 [66] V. P. Mineev, K. Samokhin, and L. Landau, Introduction to
[51] T. Onimaru, K. Matsumoto, Y. Inoue, K. Umeo, T. Sakakibara,              unconventional superconductivity (CRC Press, 1999).
     Y. Karaki, M. Kubota, and T. Takabatake, Physical review let-       [67] A. Vashist, R. Gopal, D. Srivastava, M. Karppinen, and
     ters 106, 177001 (2011).                                                 Y. Singh, Physical Review B 99, 245131 (2019)
[52] M. Tsujimoto, Y. Matsumoto, T. Tomita, A. Sakai, and




    SUPPLEMENTARY INFORMATION FOR “MULTIPOLAR SUPERCONDUCTIVITY IN LUTTINGER SEMIMETALS”

                               GINZBURG-LANDAU FREE ENERGY AND ONE-LOOP EXPANSION

   In this section, we compute the coefficient of the quadratic term, ra , in the Ginzburg-Landau free energy F (∆a ) to compare
the strength of instabilities towards ∆a pairing. We first introduce the free electron propagator
                                                                          −ik0 − c0 k 2 + i ci di (k)γi + µ
                                               X                                             P
                     G(K) = (ik0 + c0 k 2 +        ci di (k)γi − µ)−1 = P                                       .           (S1)
                                                                             i (ci di (k)) − (c0 k + ik0 − µ)
                                                                                          2       2           2
                                                i

Here K ≡ (k0 , k) and k0 = 2π(n + 1/2)T denotes the Matsubara frequency. Then, the free energy is written as,
                                                  XZ Λ 1
                                 ~ = 1 |∆|
                              F (∆)      ~ 2+T                        ˆ
                                                            tr(−G(K)∆G(−K)      T ˆ† m
                                                                                  ∆ ) ,                                                   (S2)
                                       g          m,n k
                                                         m

      ˆ =    P
where ∆         a γa γ45 ∆a . Let F2 (∆a ) be the contribution to the free energy that contains 2nd power of ∆a . We have

                                                                 1         1
                                                    F2 (∆a ) =     |∆a |2 − La ∆∗a ∆a                                                     (S3)
                                                                 g         2
with
                                                         XZ Λ
                                                La = T               tr(G(K)γa G(−K)γa )
                                                          k0     k


which is represented as a Feynman diagram shown in Fig.S1. In this expression, we use the relation γ45 G(K)T γ45 = G(K).
                                                                                                                                     7


                                                                   K


                                                                 −K
FIG. S1. Diagrammatic representation of La . Each solid arrow refer free electron propagator, G(K), with K = (k0 , k) while each wiggly
line indicate insertion of ∆a with vertex γa .


  Meanwhile, we can parametrize the terms in free energy accordingly.
                                                           F2 (∆a ) = ra |∆a |2
Choosing the specific configurations,
                        ∆1eg = (1, 0), ∆2eg = (0, 1), ∆1t2g = (1, 0, 0), ∆2t2g = (0, 1, 0), ∆3t2g = (0, 0, 1)                     (S4)
we apply Eq.S3 and
                        F2 (∆1eg ) = r1 , F2 (∆2eg ) = r2 , F2 (∆1t2g ) = r3 , F2 (∆2t2g ) = r4 , F2 (∆3t2g ) = r5                (S5)

to get the coefficients ra . Then one can write the coefficients as below with k̂0 = k0 /T = 2π(n+1/2), ĉi = ci /T and µ̂ = µ/T .
                                                        P                2                2          2     2      2
                                                                                                                    
                                                      2    i (ĉi di (k)) − 2(ĉa da (k)) − (ĉ0 k − µ̂) − k̂0
                                 Z X
                     1       1/2
               ra = + T                                                                                                           (S6)
                     g
                                        P                                            P                                       
                                           i (ĉi di (k)) − (ĉ0 k − µ̂ + ik̂0 )
                                                         2            2            2
                                                                                         i (ĉi di (k)) − (ĉ0 k − µ̂ − ik̂0 )
                                                                                                       2        2             2
                                  k n

Remarkably, ra −rb can be simply expressed as the following,
                                                             −4(ĉa da (k))2 + 4(ĉb db (k))2
                            Z X
                        1/2
            ra − rb = T           P                                          P                                       .        (S7)
                                      i (ĉi di (k)) − (ĉ0 k − µ̂ + ik̂0 )
                                                    2        2             2
                                                                                 i (ĉi di (k)) − (ĉ0 k − µ̂ − ik̂0 )
                                                                                               2        2             2
                             k n

    In Fig.S2, we plot the numerical evolution of coefficients, r̃a ≡ ra /T 1/2 − 1/g, as a function of Ô20 ≡ ĉ5 − ĉη with
ĉ0 = −2000(a/π)2 , ĉeg ≡ ĉ1 = ĉ2 = −2000/3(a/π)2 , ĉη ≡ ĉ3 = ĉ4 = (−1000/3 − Ô20 )(a/π)2 , ĉ5 = −1000/3(a/π)2 , and
µ̂ = −200 as appropriate for PrBi. First, it clearly shows that the instablity towards ∆eg pairing is stronger than ∆t2g pairing,
i.e., r̃eg ≡ r̃1 = r̃2 < r̃t2g ≡ r̃3 = r̃4 = r̃5 , with Ô20 = 0 for cubic symmetry as stated in the main text. Moreover, Fig.S2
also shows that the instability towards ∆2 pairing becomes stronger than ∆1 pairing, i.e., r̃2 < r̃1 , as soon as O20 -type ferro-
quadrupolar order becomes finite, Ô20 6= 0. Finally, it tells us that the instability towards ∆η ≡ (∆3 , ∆4 ) pairing becomes
stronger than ∆2 pairing, r̃η ≡ r̃3 = r̃4 < r̃2 , for Ô20 > ĉ5 − ĉeg = 1000/3(a/π)2 .


                                   KONDO COUPLING AND FERMI SURFACE DISTORTION

   In this section, we derive the effective Kondo coupling between the quadrupolar order parameters and the itinerant j = 3/2
electrons for the interpenetrating FCC lattice system. We start by introducing the Kondo model where the quadrupolar order
parameters O22 and O20 and the itinerant t2g electrons couple as the following,
                                             XX                                                  
                                   HK = JK           O22 Γa1,ij c†iaα cjaα + O20 Γa2,ij c†iaα cjaα .                     (S8)
                                               hi,ji a,α


Here, c†iaα and ciaα are the electron creation and annihilation operators at site i with orbital a ∈ (x, y, z) and spin α ∈ (↑, ↓).
We consider the case where the quadrupolar degrees of freedom from the localized electron reside in one FCC lattice and the
itinerant electrons with p orbitals reside in another FCC lattice as in Fig.S3. Then one of the Kondo coupling terms, which
couples itinerant electrons in px orbital with other itinerant electrons in py orbital residing on nearest neighbor sites, can be
written as below.
                                             O22 (c†ix yα cixα − c†iy xα ciyα + c†i−x yα cixα − c†i−y xα ciyα )
                                        X
                            Hixy = JK                                                                                         (S9)
                                           α
                                                                                                                                              8




                                    100           200       300          400         500          600      ▼
              -0.0035                                                                 ▼
                                                                  ▼
              -0.0040                         ▼                                                                           ●

                     ◆
                     ▲
                     ▼                                                                                                    ■
              -0.0045
                                                                                                           ●
                                                                                                           ■             ◆
                                             ◆
                                             ▲
              -0.0050                                                                  ●
                                                                                       ■                                  ▲
                                                                  ●
                                                                  ◆
                                                                  ▲
                                                                  ■
              -0.0055                                                                                                     ▼
                                             ●
                                             ■
              -0.0060                                                                  ◆
                                                                                       ▲

                     ●
                     ■
              -0.0065                                                                                      ◆
                                                                                                           ▲

FIG. S2. (color online) Plot of coefficients, r̃a ≡ ra /T 1/2 − 1/g, as a function of Ô20 [(a/π)2 ] with ĉ0 = −2000(a/π)2 , ĉeg ≡ ĉ1 = ĉ2 =
−2000/3(a/π)2 , ĉη ≡ ĉ3 = ĉ4 = (−1000/3 − Ô20 )(a/π)2 , ĉ5 = −1000/3(a/π)2 , and µ̂ = −200. These numbers are relevant to PrBi.




FIG. S3. (color online) Position of the quadrupolar degrees of freedom and the itinerant electrons with p orbitals in the interpenetrating FCC
lattice system. One of two quadrupole moments, O22 , is colored red and blue. px orbital is colored green and yellow.




where the site index ia represents the nearest neighbor of site i in a direction. Here, the − sign for the second term comes from
the O22 , which transforms as O22 → −O22 under C4z (π/2 rotation about z axis). Using C31 rotation (2π/3 rotation along
(111) direction), we can write symmetry related terms as below,



                                          √
                               X 1          3
                     Hiyz = JK   (− O22 −     O20 )(c†iy zα ciyα − c†iz yα cizα + c†i−y zα ciyα − c†i−z yα cizα ),
                               α
                                   2       2
                                          √
                               X 1          3
                     Hizx = JK   (− O22 +     O20 )(c†iz xα cizα − c†ix zα cixα + c†i−z xα cizα − c†i−x zα cixα ).                       (S10)
                               α
                                   2       2
                                                                                                                     9
                                                      P
After Fourier transforming the Hamiltonian, HK =        i (Hixy + Hiyz + Hizx ), and expanding around k = 0, the Kondo
Hamiltonian is written as
                                     2 X X
                                      a
                        HK (k) = JK                  (O22 (−kx2 − ky2 − kx ky )(c†kxα ckyα + c†kyα ckxα )
                                      π          α
                                            k
                                            √
                                    1          3
                               + (− O22 −        O20 )(−ky2 − kz2 − ky kz )(c†kyα ckzα + c†kzα ckyα )
                                    2       √ 2
                                    1          3
                                                 O20 )(−kz2 − kx2 − kz kx )(c†kzα ckxα + c†kxα ckzα ) .
                                                                                                      
                               + (− O22 +                                                                         (S11)
                                    2         2
By projecting onto j = 3/2 basis with the projection operator Pj=3/2 , one gets the following Kondo coupling,

                     H̃K (k) = Pj=3/2 HK (k)Pj=3/2
                                  √                       √                                    
                             = J˜K ( 3O20 +O22 )d3 (k)γ3 +( 3O20 −O22 )d4 (k)γ4 − 2O22 d5 (k)γ5                  (S12)

in four component spinor basis ψ.

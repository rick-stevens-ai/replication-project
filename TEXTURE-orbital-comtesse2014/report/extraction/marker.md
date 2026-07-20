# INTERIM: pdftotext fallback (marker unavailable in this environment)

> This is an interim Markdown extraction produced with `pdftotext -layout` as a stand-in for a marker-pdf conversion. Layout/figures are approximate; equations are not LaTeX-reconstructed. Source: textures-orbital-comtesse2014.pdf (Comtesse et al., arXiv:1401.8148).

                                                     First-principles calculation of the instability leading to giant inverse magnetocaloric
                                                                                              effects

                                                    D. Comtesse,1 M. E. Gruner,1 M. Ogura,2 V. V. Sokolovskiy,3, 4 V. D. Buchelnikov,4 A. Grünebohm,1 R. Arróyave,5
                                                         N. Singh,6 T. Gottschall,7 O. Gutfleisch,7 V. A. Chernenko,8 F. Albertini,9 S. Fähler,10 and P. Entel1, ∗
                                                                                  1
                                                                                       Faculty of Physics and Center for Nanointegration, CENIDE,
                                                                                        University of Duisburg-Essen, D-47048 Duisburg, Germany
                                                                              2
                                                                                Department of Physics, Graduate School of Science, Osaka University,
                                                                                          Machikaneyama 1-1, Toyonaka, Osaka 560-0043, Japan
arXiv:1401.8148v1 [cond-mat.mtrl-sci] 31 Jan 2014




                                                                        3
                                                                          National University of Science and Technology, ’MIS&S’, 119049 Moscow, Russia
                                                                4
                                                                  Condensed Matter Physics Department, Chelyabinsk State University, 454021 Chelyabinsk, Russia
                                                                                            5
                                                                                              Department of Materials Science and Engineering,
                                                                                        Texas A&M University, College Station, Texas 77843, USA
                                                                   6
                                                                     Department of Engineering Technology, University of Houston, Houston, Texas 77204, USA
                                                                        7
                                                                          Materials Science, Technical University Darmstadt, D-64287 Darmstadt, Germany
                                                                              8
                                                                                BCMaterials,University of Basque Country (UPV/EHU)and Ikerbasque,
                                                                                           Basque Foundation for Science, Bilbao 48011, Spain
                                                                                 9
                                                                                   IMEM-CNR, Parco Area delle Scienze 37/A, I-43124 Parma, Italy
                                                                                    10
                                                                                       IFW Dresden, P. O. Box 270116, D-01171 Dresden, Germany
                                                                                                         (Dated: February 3, 2014)
                                                                    The structural and magnetic properties of functional Ni-Mn-Z (Z = Ga, In, Sn) Heusler alloys
                                                                 are studied by first-principles and Monte Carlo methods. The ab initio calculations give a basic
                                                                 understanding of the underlying physics which is associated with the strong competition of ferro-
                                                                 and antiferromagnetic interactions with increasing chemical disorder. The resulting d-electron or-
                                                                 bital dependent magnetic ordering is the driving mechanism of magnetostructural instability which
                                                                 is accompanied by a drop of magnetization governing the size of the magnetocaloric effect. The
                                                                 thermodynamic properties are calculated by using the ab initio magnetic exchange coupling con-
                                                                 stants in finite-temperature Monte Carlo simulations, which are used to accurately reproduce the
                                                                 experimental entropy and adiabatic temperature changes across the magnetostructural transition.

                                                                 PACS numbers: 75.50.-y, 75.10.-b, 75.30.Sg


                                                       Following the concepts of Hume-Rothery the influence         MCE can be influenced when Ni is substituted in part
                                                    of composition on martensitic and magnetic transforma-          by Co: It is strongly enhanced in the case of In-based in-
                                                    tion temperatures is commonly condensed as a depen-             termetallics [19, 20] (with adiabatic temperature change
                                                    dency of electrons per atom (e/a-ratio) [1]. Experiment         ∆Tad = −6 K in 2 T field [20]) while in the case of Ga
                                                    and first-principles calculations, however, reveal that the     the MCE is turned from direct to inverse by decoupling
                                                    Z element in Ni-Mn-Z Heusler alloys (Z = Ga, In, Sn)            Tm and Curie temperature TC [21] (with ∆Tad = −1.6
                                                    also affects the transformation temperatures substan-           K in 1.9 T field [22, 23]).
                                                    tially [2]. Moreover, recent experiments on samples with           Chemical disorder in the Mn-rich Heusler alloys is re-
                                                    identical composition but different heat treatment indi-        sponsible for competing magnetic interactions (ferromag-
                                                    cate that chemical disorder also plays an important role        netic versus antiferromagnetic) because the extra Mn
                                                    [3–5]. Here, we use first-principles calculations to iden-      atoms occupy lattice sites of the Z-sublattice which in-
                                                    tify the influence of chemical disorder on the magnetic         teract antiferromagnetically with the Mn atoms on the
                                                    exchange parameters and derive guidelines for a further         Y-sublattice due to RKKY-type interactions. This com-
                                                    systematic improvement of magnetocaloric materials [6].         petition of magnetic interactions leads to the characteris-
                                                                                                                    tic drop of magnetization curves at Tm , which is observed
                                                       Besides the magnetocaloric effect (MCE) in Gd and
                                                                                                                    in Ni-(Co)-Mn-Z materials [14–16, 19–23]. (The magne-
                                                    other alloys at room temperature [7, 8], the metamag-
                                                                                                                    tostructural transformation was originally discussed for
                                                    netic Ni-Mn based Heusler materials [9, 10], have at-           Ni-excess Ni-Mn-Ga alloys which was interpreted as mag-
                                                    tracted much interest recently [11, 12]. In these alloys the
                                                                                                                    netic dilution effect [24].)
                                                    metamagnetic features are responsible for magnetic glass
                                                    behavior and frustration due to chemical disorder [13–15]          Previously, Monte Carlo (MC) methods [17, 18] and
                                                    as well as unusual magnetization behavior under an ex-          first-principles tools [25–27] have been used to explore the
                                                    ternal magnetic field such as a large jump of the magne-        phase diagram and magnetostructural transformation of
                                                    tization ∆M (Tm ) at the martensitic/magnetostructural          the magnetocaloric materials as a function of tempera-
                                                    transformation temperature Tm [16]. This gives rise to          ture and e/a [2, 28].
                                                    the large inverse MCE of the materials [9, 10, 17, 18]. The       In this letter we show that basically the magnetic ex-
                                                                                                                                                                                                                                            2

                         4                                                                 15                                                                      Ni45Co5Mn37In13              (a)    Ni45Co5Mn37In13                (b)
                                      (a) Ni50Mn30Ga20                                                   (b) Ni50Mn30Ga20
                                                                                                                                                              5    c/a=1.00, ferro                     c/a=1.21, ferri
                                                                                           10
                         2                 c/a=1.00                                                            c/a=1.22
                                                                                            5




                                                                                                                                       DOS (states/eV/f.u.)
        (meV)




                         0




                                                                         (meV)
                                                                                            0
                                                                                                                                                              0
 total -total




                        -2                                                                  -5




                                                                   total-total
                                                  Ni-Ni                                                                Ni-Ni
                                                                                           -10
        J ij




                                                                         J ij
                        -4                        Ni-MnY                                                               Ni-MnY                                             Total                                 Total
                                                                                                                                                                          Ni                                    Ni
                                                  Ni-MnZ                                                               Ni-MnZ                                             MnY                                   MnY
                                                                                       -15
                                                  MnY-MnY                                                              MnY-MnY                                -5          MnZ                                   MnZ
                        -6                        MnY-MnZ                                                              MnY-MnZ
                                                                                           -20                                                                            Co x 5                                Co x 5
                                                  MnZ-MnZ                                                              MnZ-MnZ
                                                                                                                                                                     -6           -4   -2   0   2         -6            -4   -2   0   2
                        -8                                                             -25
                             0.5     1.0        1.5          2.0                                 0.5     1.0        1.5          2.0                                                            E-EFermi (eV)
                                   Distance (a)                                                        Distance (a)
                    15                                                                     20
                                      (c) Ni50Mn30Ga20                                                   (d) Ni50Mn30Ga20
                                                                                                                                       FIG. 2: Element resolved density of states of (a) austenite
                                           c/a=1.00                                                                                    (L21 , a = 5.96 Å) and (b) martensite (L10 , a = b = 5.6 Å,
                                                                                                               c/a=1.22
                        10
                                                                                           15                                          c = 6.76 Å, c/a = 1.21) of Ni45 Co5 Mn37 In13 showing the sta-
                                                  Ni-Ni
                                                  Ni - MnY
                                                                                                                       Ni-Ni
                                                                                                                       Ni-MnY
                                                                                                                                       bilization of martensite due to the formation of a pseudogap
      J ij2g 2g (meV)




                                                                         J ij2g 2g (meV)




                                                  Ni-MnZ                                   10                          Ni-MnZ          at EF (“ferri” means that the spin of Mn on the In sites is
                                                  MnY-MnY
                        5
                                                  MnY-MnZ
                                                                                                                       MnY-MnY         reversed).
                                                                                                                       MnY-MnZ
 t -t




                                                                   t -t




                                                  MnZ-MnZ                                   5                          MnZ-MnZ


                        0
                                                                                            0                                          where ∆i is the difference in the inverse single-site scat-
                                                                                                                                       tering t-matrices for spin-up and spin-down states, ∆i =
                        -5
                             0.5     1.0        1.5          2.0
                                                                                            -5
                                                                                                 0.5     1.0        1.5          2.0
                                                                                                                                       t−1     −1
                                                                                                                                        i↑ − ti↓ , and τ is the scattering path operator. Since
                                   Distance (a)                                                        Distance (a)                    we use the spherical potential and scalar relativistic ap-
                        5
                                   (e) Ni50Mn30Ga20
                                                                                             5                                         proximation, the t-matrices are diagonal. Thus, we can
                                                                                                        (f) Ni50Mn30Ga20
                                       c/a=1.00
                                                                                                                                       decompose the Jij and extract the contribution between
                        0
                                                                                             0                                         L states (L = (l, m) indicates the set of angular momen-
                                                                                                               c/a=1.22                tum and magnetic quantum number) at the i-th site and
  J ijg g (meV)




                                                                           J ijg g (meV)




                                                                                            -5                                         L′ states at the j-site as
                        -5                                                                                                                                 Z ǫF
                                                                                                                                                        1
e -e




                                                                    e -e




                                                                                                                                               L−L′                        ij          ji
                                                Ni-Ni                                      -10                        Ni-Ni                  Jij     =           dE Im∆iL τ↑LL ′ ∆jL′ τ↓L′ L . (2)
                                                Ni-MnY                                                                Ni-MnY                           4π −∞
                                                Ni-MnZ                                                                Ni-MnZ
                -10
                                                MnY-MnY                                    -15                        MnY-MnY
                                                MnY-MnZ                                                               MnY-MnZ
                                                                                                                                          This allows to calculate element as well as orbital re-
                                                MnZ-MnZ                                                               MnZ-MnZ          solved magnetic coupling constants as shown, e.g., in Fig.
                -15                                                                        -20                                         1 for disordered, non-stoichiometric Ni50 Mn30 Ga20 . (The
                             0.5     1.0       1.5           2.0                                 0.5     1.0          1.5        2.0
                                   Distance (a)                                                        Distance (a)                    effect of disorder on martensitic transformation has also
                                                                                                                                       been discussed by [30].)
  FIG. 1:    (a-f) Element and orbital resolved magnetic ex-
                                                                                                                                          From the behavior of the magnetic coupling constants
  change parameters of austenite and martensite Ni50 Mn30 Ga20
  from ab initio calculations (not all contributions are shown).                                                                       in Fig. 1 for austenite and martensite Ni50 Mn30 Ga20
  It is obvious that the effect of ferromagnetic interactions is                                                                       as a function of the distance between the atoms we
  largely compensated by the influence of the antiferromag-                                                                            notice the nearly perfect compensation of ferromag-
  netic interactions. (Austenite: a = 5.85 Å, martensite:                                                                             netic interactions associated with the more itinerant d-
  a = b = 5.47 Å, c = 6.68, Å, c/a = 1.22.)                                                                                          electron t2g states and antiferromagnetic interactions
                                                                                                                                       of magnetic moments associated with the more local-
                                                                                                                                       ized eg states. This destabilizes ferromagnetic austen-
  change interactions obtained from first-principles calcu-                                                                            ite which undergoes a magnetostructural transformation
  lations allows to calculate the MCE as a function of tem-                                                                            to paramagnetic martensite (after addition of Co [21]).
  perature across the magnetostructural transition.                                                                                    The magnetic exchange coupling constants of tetrago-
     Before addressing the MCE, we would like to high-                                                                                 nally distorted martensite (c/a = 1.22) cannot stabi-
  light the complex magnetic behavior of the disordered                                                                                lize ferromagnetic order any more. In the MC simu-
  Ni-(Co)-Mn-Z alloys with excess Mn. We evaluate the                                                                                  lations we use the magnetic exchange parameters from
  effective exchange coupling constants Jij using the KKR                                                                              the zero-temperature ab initio calculations for austen-
  CPA method [26, 27] where, following the prescription of                                                                             ite and martensite which we let merge at Tm . Ther-
  [29], the Jij are obtained from                                                                                                      mal spin fluctuations will further help to stabilize the
                      Z ǫF                                                                                                             “paramagnetic” gap at T < Tm below the magnetic
                    1              h               i
            Jij =          dE Im Tr ∆i τ↑ij ∆j τ↓ji ,    (1)                                                                           jump ∆M (Tm ) [22, 23]. This shows that the marten-
                   4π −∞                                                                                                               sitic/magnetostructural instability is to a large extent
                                                                                                                                                                                                                                                                                 3

                              100          Hext = 1.6 T    (a) Ni50Mn25Ga25 (poly-domain)                                                           100
                                                                                                                                                                       (b) Ni45Co5Mn37In13 (poly-domain)                                                      (2 T)exp
                              90                                                                                                                    90
                                                                                          Theory (MC)                                                                  Theory (MC)
     Magnetization (Am /kg)
                              80                                                                                                                    80                                                                                                        (2 T)theo




                                                                                                                           Magnetization (Am /kg)
                                                                                                  (M)
                                                                                                K ani = 0.023 meV
                                                                                                                                                                                         1
                                           Hext = 0.8 T                                                                                                                                                                                 Dashed lines:
                              70                                                                                                                    70
     2




                                                                                                                           2




                                                                                                                                                           Tetragonal distortion (ε)
                                                                                                  (A)     -2   (M)
                                                                                                K ani = 10 K ani                                                                       0.8                                              Experimental data of
                              60                                                                                                                    60                                                                                   J. Liu et al., NM 11,
                                                                                                                                                                                       0.6
                              50           Hext = 0.4 T                                                                                             50                                                                                   620 (2012)
                                                                                                                                                                                       0.4                                                      (M)
                                                                                                                                                                                                                                              K ani = 0.08 meV
                              40                                                                                                                    40
                                                                                                                                                                                       0.2                                                      (A)    -2    (M)
                                                                                                                                                                                                   10 mT                                      K ani = 10 K ani
                              30                                                                                                                    30                                             2T
                                           Hext = 0.1 T                                                                                                                                 0
                                                                                                                                                                                             280     300   320    340
                              20                                                                                                                    20                                                                                                      (10 mT)theo
                                                                                                                                                                                             Temperature (K)

                              10        Dashed lines: Experimental data of                                                                          10
                                        P. J. Webster et al., Phil. Mag. 49, 295 (1984)                                                                                                                                                                 (10 mT)exp
                               0                                                                                                                     0
                                    0     50       100    150   200     250    300        350       400        450   500                                  280                                  290               300        310         320            330                340
                                                                Temperature (K)                                                                                                                                    Temperature (K)


FIG. 3: (a) Monte Carlo magnetization curves (solid lines) of Ni50 Mn25 Ga25 from the Potts model using ab initio magnetic
exchange and magnetocrystalline anisotropy parameters, in comparison with experiment [34]. The jump of the magnetization
curves vanishes for sufficiently large fields. (b) Theoretical and experimental magnetization curves of Ni45 Co5 Mn37 In13 in a
small and large external magnetic field of 10 mT and 2 T [20]. Here, the jump ∆M does not vanish for increasing magnetic
fields. The inset shows the hysteresis from the first-order cubic-tetragonal transformation.

                                                                                                                                                                                                                 X
driven by the atomic disorder leading to strong com-                                                                                                                                          + Kani                    δSi ,Sk Mi2 ,                                           (3)
petition of ferro- and antiferromagnetic interactions of                                                                                                                                                          i
approximately equal strength. This is responsible for                                                                                                                                                 X                                               X
                                                                                                                                                                                                                                                                          !
the breakdown of ferromagnetic order in austenite and                                                                                                 Hel = −                                                σi σj       J + U1 gµB Hext                       δσi σg
the appearance of the “paramagnetic gap” below Tm in                                                                                                                                                  hiji                                              i
martensite.                                                                                                                                                                                                X
                                                                                                                                                                                                                      1 − σi2       1 − σj2 .
                                                                                                                                                                                                                                          
                                                                                                                                                                                              −K                                                                                (4)
   We emphasize that the same scenario works in case                                                                                                                                                       hiji

of Ni-(Co)-Mn-(In, Sn). With addition of Co (Co is                                                                            The Ji,j are the magnetic exchange parameters for each
likely to replace Ni because of similar coordination chem-                                                                 structure. Since mapping of ab initio energies is only
istry), the ferromagnetic tendencies increase but also the                                                                 onto Jij with unit length of spins, field terms must in-
“disordered nature” of the magnetic interactions, which                                                                    clude explicitely Mi , Mi2 , where Mi is the ab initio value
governs the magnetostructural instability. Although, Co                                                                    of magnetization of atom at site i taken to be dimension-
leads to a decrease of Tm , it clearly has a favorable effect                                                              less. J and K are the elastic and U1 (Ui,j ) the mag-
regarding the magnetocaloric properties. This is because                                                                   netoelastic interaction parameters (Hint couples Mi Mj
Co hybridizes strongly with Ni states (see Fig. 2) and                                                                     and σi2 , σj2 with strength Uij [17, 33]). The Kronecker
causes more spin disorder in the Heusler materials which                                                                   symbol restricts the spin-spin interactions to those be-
leads to larger magnetic entropy and adiabatic temper-                                                                     tween the same Potts-q states. The spin moment of Mn
ature changes. (Note that competing interactions have                                                                      is S = 25 and we identify the 2S + 1 spin projections
also been discussed for Ni-Mn-Ga in [31, 32].)                                                                             with qMn = 1 . . . 6. Likewise, we assume S = 1 for Ni
                                                                                                                           and S = 32 for Co. The BEG model defines σi = 0, ±1
  The jump ∆M (Tm ) which is accompanied by break-                                                                         for austenite and two martensitic variants, respectively
down of long-range ferromagnetism, large magnetic fluc-                                                                    [17, 18, 33]; it allows first-order martensitic phase trans-
tuations and a large entropy change across the magne-                                                                      formation with thermal hysteresis for sufficiently large
tostructural transition, is at the heart of the giant inverse                                                              biquatratic elastic interaction (0.2 < K/J < 0.37; we
MCE.                                                                                                                       have adopted 0.23 for Ni-(Co)-Mn-In alloys). Because of
                                                                                                                           the magnetoelastic coupling term the jump ∆M (Tm ) is
  Regarding thermodynamic properties we use the
                                                                                                                           coupled to the martensitic transformation and exhibits
Blume-Emery-Griffiths (BEG) model [33] for austenite-
martensite transformation in combination with the Potts                                                                    hysteresis as well.
                                                                                                                              We mimic the magnetic aspect of polycrystalline ma-
model for the magnetic part and a magnetoelastic inter-
                                                                                                                           terials by magnetic domain blocks with random initial
action term [17, 18]: H = Hm + Hel + Hint where
                                                                                                                           spin configurations in each domain. The spins from dif-
                                                                                                                           ferent domain blocks can interact with probability W =
                                            X                                        X                                     min(1, exp(−|Kani |Mi2 /gµB Hext |Mi |). This stochastic
    Hm = −                                         Ji,j δSi ,Sj − gµB Hext                       δSi ,Sg Mi                competition between the magnetic anisotropy field and
                                            hiji                                          i                                external magnetic field allows to realize experimental
                                                                                                                                                                          4

trends of magnetization curves, see Fig. 3.                       jump of magnetization and magnetic entropy, dTm /dHext
   Hence, the extended Potts model in Eqs. (3-4) al-              is the shift of structural phase transition in the magnetic
lows us to describe magnetic, structural as well as cou-          field and ∆f (T, Hext ) is the change of austenite fraction
pled magnetostructural phase transitions [17, 18]. Fig-           caused by a field change, and C(T, Hext ) is the total spe-
ure 3 shows magnetization curves in small and large               cific heat. In our calculations the value of dTm /dHext
magnetic fields for polycrystalline Ni50 Mn25 Ga25 and            was taken from experiment [20], whereas ∆M and ∆f
Ni45 Co5 Mn37 In13 in comparison to experiment [20, 34].          were obtained from MC simulations.
   Note that there is a distinctive difference between
M (T ) of the two materials.                                                         Ni45Co5Mn37In13 (poly-domain)
                                                                              2
   For ferromagnetic Ni-Mn-Ga alloys near stoichiome-                                Theory (MC)
try the jump vanishes for sufficiently large magnetic field
                                                                              0
when overcoming the magnetocrystalline anisotropy in                                                                                       14

agreement with experiment [11, 12, 34]. However, the                                                                                       12




                                                                     ∆T (K)
                                                                              -2                                                           10




                                                                                                                          ∆Smag (J/kg K)
jump persists for the Mn-rich Ni-Co-Mn-(Ga, In, Sn) up                                                                                      8
                                                                                                                                                          Inverse MCE
                                                                                                                                            6
to large magnetic fields [19–23] because of strong an-                        -4                                                            4
                                                                                                                                                          Direct MCE
                                                                                                                                                      ∆Hext = 2 T
                                                                                                                                            2
tiferromagnetic MnY -MnZ interactions competing with                                                                                        0
                                                                                   ∆Hext = 2 T
the ferromagnetic ones. Note that for Ni45 Co5 Mn37 In13                      -6
                                                                                                                                           -2

                                                                                                             Dashed line:          300     350       400
magnetization jump and hysteretic behavior in Fig. 3(b)                              Inverse MCE                                       Temperature (K)
                                                                                     Direct MCE              Experimental data of
agree well with experiment [20].                                              -8                             J. Liu et al, NM 11, 620 (2012)

   Total enery calculations and MC simulations show                                  280         300   320       340        360                 380   400           420
                                                                                                             Temperature (K)
that the magnetostructural instability observed in
Mn-rich systems [14–16, 19–23] is accompanied by                  FIG. 4: Adiabatic temperature change of the direct (red
a transition from ferromagnetic austenite to fer-                 circles) and inverse (blue squares) MCE of polycrystalline
rimagnetic/paramagnetic martensite, although, zero-               Ni45 Co5 Mn37 In13 as obtained from the extended Potts model
temperature energy differences, (Ef erro − Ef erri ) may          (diamonds: results for single-domain state; inset: tempera-
already become small in austenite (this is the case for           ture variation of the entropy).
Ni50−x Cox Mn25+y Sn25−y at a critical Co concentration).
Free energies are difficult to evaluate on an ab initio ba-          Results for the MCE of Ni-Co-Mn-In alloys are shown
sis because of chemical disorder, softenig of lattice vi-         in Fig. 4 which demonstrates the enhancement of cooling
brations in austenite and magnetic excitations, which is          up to -6 K compared to samples without Co (≈ −3 K)
beyond the scope of the present paper.                            [20]. The enhancement is caused by the increased mag-
   The adiabatic temperature changes across Curie tem-            netic disorder leading to larger ∆Smag (T, Hext ). How-
perature (direct MCE) and across magnetostructural                ever, systematic comparison is difficult because of either
transformation (inverse MCE) are determined by the                different sample preparation or compositions, compare,
isothermal magnetic entropy change and total specific             for instance, the different values reported for ∆Smag
heat (sum of magnetic and lattice specific heat, where            and ∆Tad regarding Ni-Mn-In alloys [19, 20, 35]. The
the latter part is taken from the Debye model). These             key figure of merit in these alloys is large: we obtain
quantities can be calculated from the relations:                  RCPinv = −132 J/kg for Ni45 Co5 Mn37 In13 .
                                                                     In this paper we have shown that MCE is determined
                                H
                                Zext
                                          T
                                                    
                                                        ∂M
                                                                 by the influence of competing ferromagnetic and antifer-
                                       ′
        ∆Tad (T, Hext ) = −µ0       dH                            romagnetic interactions in Ni-Co-Mn-Z alloys [2]. The ab
                                       C(T, H ′ )       ∂T
                                0
                                                             H′   initio magnetic exchange parameters are the decisive pa-
                           ∆Smag (T, Hext )                       rameters which determine the jump ∆M (Tm , Hext ) and
                       ≈ −T                   ,        (5)        the size of the MCE. From the predictive power of ab
                              C(T, Hext )
                                                −1              initio calculations regarding the influence of the mag-
                                            dTm                   netic coupling constants to optimize the MCE, it might
   ∆Smag (Tm , Hext ) = ∆M (Tm , Hext )              , (6)
                                           dHext                  be worth to create even more spin disorder and larger
                      ∆Smag (Tm , Hext )                          isothermal entropy changes by looking for the effects of
 ∆Tad (T, Hext ) = −T                    ∆f (T, Hext ) (7)        Cr and Gd added to Ni-Co-Mn-Z materials.
                        C(T, Hext )
                                                                     As already indicated by several experiments [1, 3–5]
Here, ∆Smag (T, Hext ) = Smag (T, Hext ) − Smag (T, 0) is         our calculations show that e/a ratios are not sufficient
the entropy difference for finite and zero field. We use          for describing the transformation behavior (like disor-
the Maxwell relation in Eq. (5) for the direct MCE while          der broadened first-order magnetostructural phase tran-
for the inverse MCE at the first-order magnetostructural          sition, range of coexistence of phases and metastabil-
transition we use instead Eqs. (6) and (7) based on the           ity [14–16, 36] and magnetic cluster formation [13]) and
Clausius-Clapeyron equation. ∆M and ∆Smag are the                 MCE in Heusler alloys completely. Though this con-
                                                                                                                              5

cept of itinerant electrons gives a rough overview on the             P. Lázpita, J. Gutiérrez, and I. Orue, Appl. Phys. Lett.
transformation temperatures, the interaction of the local-            102, 071904 (2013).
ized electronic orbitals influences the exchange parame-         [17] V. D. Buchelnikov, P. Entel, S. V. Taskaev, V. V.
                                                                      Sokolovskiy, A. Hucht, M. Ogura, H. Akai, M. E. Gruner,
ters and thus the size of the magnetocaloric effect. In
                                                                      and S. K. Nayak, Phys. Rev. B 78, 184427 (2008).
particular, our calculations identify that it is beneficial      [18] V. D. Buchelnikov, V. V. Sokolovskiy, S. V. Taskaev, V.
having specific chemical environment for the MnY and                  V. Khovaylo, A. A. Aliev, L. N. Khanov, A. B. Batdalov,
MnZ atoms since this optimizes the compensation of fer-               P. Entel, H. Miki, and T. Takagi, J. Phys. D: Appl. Phys.
romagnetic and antiferromagnetic interactions. As chem-               44, 064012 (2011).
ical order is susceptible to time and temperature during         [19] D. Bourgault, J. Tillier, P. Courtois, D. Maillard, and X.
the sample preparation in addition to composition, this               Chauld, Appl. Phys. Lett. 96, 132501 (2010).
guideline will allow for a systematic optimization of mag-       [20] J. Liu, T. Gottschall, K. P. Skokov, J. D. Moore, and O.
netocaloric materials.                                                Gutfleisch, Nature Mater. 11, 620 (2012).
                                                                 [21] S. Fabbrici, J. Kamarad, Z. Arnold, F. Casoli, A.
   We thank the DFG (SPP 1599) for financial sup-                     Paoluzi, F. Bolzoni, R. Cabassi, M. Solzi, G. Porcari,
port. RA and NS acknowlege support from NSF through                   C. Pernechele, and F. Albertini, Acta Mater. 59, 412
Grants DMR-0844082 and 0805293.                                       (2011).
                                                                 [22] G. Porcari, S. Fabbrici, C. Pernechle, F. Albertini, M.
                                                                      Buzzi, A. Paoluzi, J. Kamarad, Z. Arnold, and M. Solzi,
                                                                      Phys. Rev. B 85, 024414 (2012).
                                                                 [23] G. Porcari, F. Cugini, S. Fabbrici, C. Pernechle, F. Al-
   ∗
     Electronic address: entel@thp.uni-duisburg.de                    bertini, M. Buzzi, M. Mangia, and M. Solzi, Phys. Rev.
 [1] V. A. Chernenko, Scripta Mater. 40, 523 (1999).                  B 86, 104432 (2012).
 [2] P. Entel, M. Siewert, M. E. Gruner, H. C. Herper, D.        [24] V. V. Khovaylo, V. D. Buchelnikov, R. Kainuma, V. V.
     Comtesse, R. Arróyave, N. Singh, A. Talapatra, V. V.            Koledov, M. Ohtsuka, V. G. Shavrov, T. Takagi, S. V.
     Sokolovskiy, V. D. Buchelnikov, F. Albertini, L. Righi,          Taskaev, aand A. N. Vasiliev, Phys. Rev. B 72, 224408
     and V. A. Chernenko, EPJB 86, 65 (2013).                         (2005).
 [3] W. Ito, Y. Imano, R. Kainuma, Y. Sutou, K. Oikawa,          [25] http://cms.mpi.univie.ac.at/VASP/ (new release: VASP
     and K. Ishida, Metall. Mater. Trans. A 38, 759 (2007).           5.3.3). G. Kresse and J. Furthmüller, Phys. Rev. B 54,
 [4] S. Kustov, M. L. Corró, J. Pons, and E. Cesari, Appl.           11169 (1996).
     Phys. Lett. 94, 191901 (2009].                              [26] The Munich SPR-KKR package, version 6.3, H. Ebert
 [5] R. Niemann, L. Schultz, and S. Fähler, J. Appl. Phys.           et al., http://olymp.cup.uni-muenchen.de/SPRKKR. H.
     111, 093909 (2012).                                              Ebert, D. Ködderitzsch, and J. Minár, Rep. Prog. Phys.
 [6] K. G. Sandeman, Scipta Mater. 67, 566 (2012).                    74, 096501 (2011).
 [7] V. K. Pecharsky and K. A. Gschneidner, Jr. Phys. Rev.       [27] M. Ogura, C. Takahashi. and H. Akai, J. Phys.: Condens.
     Lett. 78, 4494 (1997).                                           Matter 19, 365226 (2007).
 [8] O. Tegus, E. Brück, K. H. J. Buschow, and F. R. de Boer,   [28] M.A. Uijttewaal, T. Hickel, J. Neugebauer, M.E. Gruner,
     Nature 415, 150 (2002).                                          and P. Entel, Phys. Rev. Lett. 102, 035702 (2009).
 [9] T. Krenke, E. Duman, M. Acet, E. F. Wassermann. X           [29] A. I. Liechtenstein, M. I. Katsnelson, V. P. Antropov, and
     Moya, L. Mañosa, and A. Planes, Nature Mater. 4, 957            V. A. Gubanov, J. Magn. Magn. Mater. 67, 65 (1987).
     (2005).                                                     [30] H. B. Luo, C. M. Li, Q. M. Hu, S. E. Kulkova, B. Johans-
[10] R. Kainuma, Y. Imano, W. Ito, Y. Sutou, H. Morito,               son, L. itos, and R. Yang Acta Mater. 59, 5938 (2011).
     H. Okamato, S. Kitakami, O. Oikawa, A. Fujita, T.           [31] I. Galanakis and E. Şaşıoğlu, Appl. Phys. Lett. 98,
     Kanomata, and K. Ishida, Nature 439, 957 (2006).                 102514 (2011).
[11] A. Planes, L. Mañosa, and M. Acet, J. Phys.: Condens.      [32] P. Lázpita, M. Barandiarán, J. M. Gutiérrez, J. Feucht-
     Matter 21, 233201 (2009).                                        wanger, V. A. Chernenko, and M. R. Richard, New J.
[12] M. Acet, Ll. Mañosa, and A. Planes, in: Handbook of             Phys. 13, 033039 (2011).
     Magnetic Materials, vol. 19, edited by K. H. J. Buschow     [33] T. Castan, E. Vives, and P.-A. Lindgard, Phys. Rev. B
     (Elsevier, Amsterdam, 2011). pp. 231-289.                        60, 7071 (1999).
[13] K. P. Bhatti, S. El-Khatib, V. Srivastava, R. D. James,     [34] P. J. Webster, K. R. A. Ziebeck, S. L. Town, and M. S.
     and C. Leighton, Phys. Rev. B 85, 134450 (2012).                 Peak, Philos. Mag. B 49, 295 (1984).
[14] D. Y. Cong, S. Roth, and L. Schultz, Acta Mater. 60,        [35] X. Moya, L. Mañosa, A. Planes, S. Aksoy, M. Acet, E. F.
     5335 (2012).                                                     Wassermann, and T. Krenke, Phys. Rev. B 75, 184412
[15] A. Lakhani, A. Banerjee, P. Chaddah, X. Chen, and R.             (2007).
     V. Ramanujan, J. Phys.: Condens. Matter 24, 386004          [36] L. H. Bennett, V. Provenzano, R. D. Shull, I. Levin, E.
     (2012).                                                          Della Torre, and Y. Jin, J. All. Comp. 525, 34 (2012).
[16] J. M. Barandiarán, V. A. Chernenko, E. Cesari, D. Salas,

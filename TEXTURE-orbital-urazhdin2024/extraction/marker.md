<!--
NOTE — INTERIM EXTRACTION (marker.md)
=====================================
The real `marker` binary (marker-pdf) is NOT installed on this packaging host;
only poppler's `pdftotext` is available. This file is the DOCUMENTED INTERIM
FALLBACK for artifact #2 (the human-readable PROSE extraction), produced with:

    pdftotext -layout textures-orbital-urazhdin2024.pdf _layout.txt

Fidelity caveats (known pdftotext limits, NOT physics gaps):
  * Unicode math / super-/sub-scripts are degraded or reflowed; multi-line
    equations break across lines. Treat inline equations here as approximate.
  * The AUTHORITATIVE equation transcriptions (LaTeX) live in
    ../report/REPORT.tex and in the companion math artifact nougat.mmd.

To regenerate with the real tool once installed:
    marker_single textures-orbital-urazhdin2024.pdf ./ --output_format markdown

Role of this file: PROSE artifact (section text + figure captions, reading like
the paper). The MATH artifact (hand-transcribed numbered equations) is nougat.mmd.
-->

# Urazhdin (2024) — Atomic and inter-atomic orbital magnetization induced in SrTiO3 by chiral phonons
**arXiv:2408.08683v3 [cond-mat.mtrl-sci]** · Sergei Urazhdin, Emory University

*(Interim layout-mode extraction below; see nougat.mmd / REPORT.tex for equations.)*

---

                                                     Atomic and inter-atomic orbital magnetization induced in SrTiO3 by chiral phonons

                                                                                                                                       Sergei Urazhdin
                                                                                                         Department of Physics, Emory University, Atlanta, GA, USA

                                                                                     An unexpectedly large transient magnetization induced by circularly polarized ferroelectric
                                                                                  phonons was recently observed in a nonmagnetic insulator SrTiO3 [Nature 628, 534 (2024)]. We
                                                                                  use a minimal molecular orbital model to demonstrate two electronic contributions to this effect.
                                                                                  An atomic orbital contribution arises from the pumping of orbital angular momentum of Ti by
                                                                                  chiral motion of coordinating oxygen atoms. An additional inter-atomic contribution is associated
                                                                                  with the transient circulating current around the oxygen atoms, resulting in efficient dressing of
                                                                                  phonons by electron dynamics. The insights provided by our model may facilitate the development
arXiv:2408.08683v3 [cond-mat.mtrl-sci] 5 Jun 2025




                                                                                  of ultrafast magnetization control and orbitronic sources.


                                                                                       I.   INTRODUCTION                                             Ionic magnetic moment. The most tractable of the
                                                                                                                                                  discussed mechanisms is the Ampere field produced by
                                                                                                                                                  the rotating ion polarization P [5, 6]. ∂t P gives the
                                                       Basini et al [1] recently showed that chiral ferroelectric
                                                                                                                                                  current density, so the magnetization is proportional to
                                                    phonons generated in strontium titanate SrTiO3 (STO)
                                                                                                                                                  P × ∂t P. The relation between the magnetization and
                                                    by circularly polarized THz pulses produce large tran-
                                                                                                                                                  angularPmomentum density carried by the phonon is
                                                    sient magnetization detected as a magneto-optic Kerr ef-
                                                                                                                                                  µuc = i γi Li , where Li = Mi Qi × Q̇i is P     the angular
                                                    fect (MOKE) signal. A DC signal was observed in ad-
                                                                                                                                                  momentum of ion i in a unit cell (u.c.), γi = i eZi /2Mi
                                                    dition to an oscillating signal due to the THz ionic Kerr
                                                                                                                                                  is its gyromagnetic ratio, Zi is the Born effective charge
                                                    effect [2]. It was interpreted as the dynamical Barnett
                                                                                                                                                  of ion i, Mi is mass, and Qi is displacement [5, 7].
                                                    effect − the inverse of the Einstein-de Haas effect − in
                                                    which mechanical rotation of a solid induces magnetiza-                                          To evaluate this effect for Al2 O3 , we assume that
                                                    tion MBE [3]. In the simplest interpretation, opposite-                                       ZAl , ZO are isotropic and the same for all 12 Al and
                                                    phase circulating motion of ions produces circulating                                         18 O atomsPin the u.c. The magnetic moment is then
                                                    local currents and thus magnetic moments [Fig. 1(a)].                                         µuc = ω/2 i eZi Q2i , where ω is frequency. For Al2 O3 ,
                                                    However, the estimated ionic effect was too small, sug-                                       ω ∼ 1014 s−1 (wavelength 20 µm), ZAl ≈ −3, ZO ≈ 2,
                                                    gesting that circularly polarized phonons may efficiently                                     and QO = −3MAl QAl /2M0 ≈ −1.1QAl . Evaluation
                                                    couple to the electronic subsystem inducing spin and/or                                       of displacement amplitude for the large optical field
                                                    orbital electron polarization.                                                                E > 105 V/cm2 used in Ref. [4] requires nonlinear
                                                       In a related experiment, magnetization of a transi-                                        analysis of lattice dynamics. For an estimate, we use
                                                    tion metal-rare earth alloy ferrimagnet (FIM) film was                                        QAl = 0.1 Å corresponding to the relative Al-O displace-
                                                    reversed via optical excitation of circularly-polarized                                       ment amplitude of 10%. The resulting magnetic moment
                                                    phonons in Al2 O3 and SiO2 substrates [4]. This effect was                                    is µuc ≈ 5 × 10−27 J/T (5 × 10−4 µB ), and the magnetiza-
                                                    attributed to either the Ampere field driven by the dy-                                       tion is M = µuc /V ∼ 20 A/m, where V = 254 Å3 is u.c.
                                                    namical lattice polarization, or alternatively to the elec-                                   volume. This results in a field B = µ0 M = 2 × 10−5 T
                                                    tronic magnetization induced by transfer of angular mo-                                       inside the magnetized substrate volume. At the location
                                                    mentum from the lattice via the dynamical crystal field                                       of the FIM film above this volume, the field is produced
                                                    or spin-orbit coupling (SOC). The lack of the accepted                                        only by the fringe effects determined by the spatial pro-
                                                    mechanism for these effects reflects the complexity of cou-                                   file of magnetization, which is smaller. We arrive at the
                                                    pled electron-phonon dynamics, which is outlined below                                        same conclusion as Ref. [1], that ionic effects alone may
                                                    as the motivation for the proposed model.                                                     be insufficient to explain the observations.
                                                                                                                                                     Analysis of angular momentum transfer from the lat-
                                                                                                                                                  tice to electrons is complicated by the distinction be-
                                                    (a)             y                       (b)                      (c)                          tween the true angular momentum J of phonons, which
                                                                        O1
                                                                                                                P                        P
                                                                                   P                pz                     -pz                    is conserved for an isolated solid, and their angular quasi-
                                                          O2                                  -pz                                                 momentum JQ [6, 8]. The latter arises in the analysis of
                                                                                                                     -pz
                                                                                       O4
                                                                                                                                                  quasiparticle scattering on the lattice [9], but similarly
                                                                                       x                                         dxz
                                                               Ti                                               pz                                to the Bloch momentum is generally not conserved. This
                                                                                                          dxz                                pz
                                                                             O3                                                                   quantity also does not account for rotations of the entire
                                                                                                          pz                       -pz
                                                                                                                                                  lattice, so it cannot describe Einstein-de Haas or Bar-
                                                                                                                                                  nett effects. In the studies of molecular dynamics, this
                                                    Figure 1. (a) Schematic of atomic trajectories in the circularly                              problem is addressed by separating rigid rotations and
                                                    polarized ferroelectric phonon mode. (b),(c) bonding molec-                                   vibrations, known as Eckart convention [10].
                                                    ular orbitals derived from the Ti dxy orbital for two opposite                                   Electronic magnetism driven by lattice dynam-
                                                    phases of atomic motion in the adiabatic approximation.                                       ics. Angular momentum of Bloch electrons on the static
                                                                                                                        2

lattice is well understood, although the significance of or-   pretations of phenomena involving angular momentum of
bital contribution has been recognized only recently [11].     coupled electron-phonon system, one may ask whether it
However, its coupling to angular momentum of lattice           is possible to develop a minimal model that allows one to
dynamics can be complex. Nonlinear multi-phonon pro-           identify the dominant effects. In this paper, we address
cesses are essential for angular momentum conservation         this question by considering a simple molecular orbital
in spin-lattice interaction [12]. Furthermore, orbital mo-     approximation for the valence states in STO. Our mini-
ment of electrons can relax into the lattice on femtosec-      mal model shows that chiral phonons produce both intra-
ond timescale [13], which can lead to a non-perturbative       and inter-atomic orbital polarization of electrons due to
coupling regime where angular momentum is collectively         transient dynamical reconstruction of electronic states,
carried by the electron-phonon coupled system and is de-       renormalizing the magnetic moments of phonons. The
scribed by a new quasiparticle, the angulon [14].              microscopic insights provided by our model may facilitate
   Spin-lattice interaction has been extensively studied in    the development of methods to efficiently control magne-
the context of spin relaxation [15]. In Van Vleck’s mech-      tization and generate orbital moments in orbitronic ap-
anism, spin interacts with the lattice via magnetic dipole     plications via lattice dynamics [23].
field of phonons [16]. Alternatively, interaction can be
mediated by SOC. For magnetic solids, this can result in
direct transfer of angular momentum between phonons                      II.   ANALYSIS AND RESULTS
and electron spins, which is facilitated by the almost
gapless spectrum of spin excitations [6]. First princi-                    II.1.   Molecular orbital model
ples calculations suggest that spin-lattice interaction can
be dominated by the dynamical lattice inversion sym-              Atomic motion in the ferroelectric mode impacts pre-
metry breaking, which in magnetic materials results in         dominantly the valence electronic states forming conduc-
Dzyaloshinskii-Moriya-type spin interactions [17]. These       tion and valence bands, because both the energies and
mechanisms are relevant to paramagnetic or ferromag-           the populations of the latter are sensitive to atomic dis-
netic spins, but not non-magnetic STO.                         placements. In STO, these states are derived from the
   Coupling of electron orbital magnetization to lattice       2p orbitals of oxygen and t2g 3d-orbitals of Ti, with neg-
dynamics does not require SOC. The geometric mecha-            ligible contribution from Sr [24, 25]. One can thus focus
nism is associated with the Berry phase of the wavefunc-       on the effects of gyration of oxygen atoms relative to
tion cyclically perturbed by the lattice dynamics which        Ti they coordinate. We assume that the driving optical
can produce magnetization even in insulators [18–20],          field is incident in the z-direction, resulting in gyration
making this mechanism potentially relevant to the dis-         in the xy plane, Fig. 1(a). Since the dynamics is quasi-
cussed effects. Orbital magnetization is expected to scale     uniform through the crystal, it does not produce charge
linearly with the displacement amplitude, which appears        currents across unit cells. Therefore, molecular orbital
to contradict the quadratic dependence of magnetization        (MO) approximation can provide a minimal model for
on field amplitude observed in Ref. [1].                       the dynamical effects.
   Chiral phonon-induced electron magnetism observed in           The significance of coupling between atomic motion
paramagnetic rare earth compounds [21] was explained           and the electronic state in STO becomes apparent by con-
by the splitting of the 4f levels by the dynamical crys-       sidering, for example, the bonding MO derived from the
tal field, which plays the role of a large effective mag-      Ti dxz orbital. We assume that in equilibrium, all the Ti-
netic field efficiently polarizing a partially occupied SOC    O bonds are equal, as expected for the room-temperature
electronic level manifold [22]. However, this mecha-           cubic phase. Without ferroelectric distortion, the dxz or-
nism is not directly applicable to insulators such as STO      bital of Ti hybridizes only with the pz orbitals of the
with quenched spin and orbital degrees of freedom. The         two oxygen atoms on the x-axis [26]. In the presence of
atomic shells of all three atomic species in STO are filled    ferroelectric distortion, it becomes hybridized with the
or empty, so their Zeeman-like splitting by the dynam-         pz orbitals of the two oxygen atoms on the y-axis, with
ical crystal field does not in itself result in spin or or-    the orbital phases dependent on the instantaneous di-
bital polarization. In the electronic band picture all the     rection of displacement vector Q = Q(cos ωt, c sin ωt),
bands are either filled or empty, and are consequently         where c = ±1 is the mode chirality, Figs. 1(b),(c). The
magnetically and electrically inert. A large band gap of       same picture holds for the MO derived from the dyz or-
∆ = 3.2 eV between the filled valence and the empty            bital, with the x- and y-axes exchanged, i.e., strong hy-
conduction bands prevents phonon-driven electronic ex-         bridization along the y-axis, and alternating hybridiza-
citation. The energy of the ferroelectric phonon with fre-     tion along the x-axis. For superpositions of dxz and dyz
quency f = ω/2π = 3 THz is only Eph = h̄ω = 12.4 meV.          orbitals, dynamical hybridization along both axes results
Linear excitation via single-phonon absorption is not pos-     in the oscillating relative
                                                                                        √ phase, generating orbital states
sible, as it requires Eph > ∆. Because of the vast dif-        dσ = −(σdxz + idyz )/ 2 characterized by unquenched
ference of energy scales, perturbative nonlinear (multi-       orbital moment σ = ±1 along the z-axis.
phonon) effects also cannot explain the observations.             The SOC neglected in the above analysis mixes the
   Given the complexity and diversity of possible inter-       dxz and dyz orbitals into dσ and their superpositions
                                                                                                                                         3

(a)                                 (b)                                       In Eq. (2), we√use trigonometric parametrization with
                 ψa+, ψa-                        1              Q             θa,b = tan−1 Ed2t−E
                                                                    ϕ
                                                                                                  T i−O
                                                                                                     a,b
                                                                                                         to simplify state normalization.
 d+ , d-                                     d+                          x    The Ti-O bonding states and the non-bonding states are
                              ∆                        ϕ1                     filled, while the antibonding state is empty, with the gap
                                                 ϕ2
                    ψn2
                                                        ϕ4
                                                                                                       r
  4×pz                                 2                                                       Ed         Ed2
                    ψn1                           ϕ3                4                     ∆=        +         + 2t2T i−O + 2tO−O      (4)
                                                                                                2          4
                                           eiϕ              3
                 ψb+, ψb-
                                                                              between the antibonding and the nonbonding state ψn2
                                                                              representing the bandgap of STO, Fig. 2(a).
Figure 2. (a) MO crystal-field splitting of the levels de-                       We now analyze the effect of ferroelectric displace-
rived from the considered atomic orbitals. ∆ represents the                   ments on the hybridization and the resulting perturba-
bandgap. (b) Illustration of the mechanism for the complex                    tion of the MO states. Rotation of the displacement vec-
phase acquired by the matrix elements between Ti dσ and O                     tor results in the periodic modulation of both the bond
pz orbitals due to the ferroelectric displacement.
                                                                              length and its direction. The former entails modula-
                                                                              tion of the matrix element amplitude, while the latter
                                                                              − complex phase due to the chirality of the dσ orbitals,
with dxy orbitals entangled with spin, forming Kramers
                                                                              Fig. 2(b). Taking into account the directional depen-
doublets [27]. For instance, one such doublet is d+ | ↓⟩,
                                                                              dence of the matrix element phases in the symmetric
d− | ↑⟩. Thus, it is sufficient to analyze the effects of dy-
                                                                              state, the perturbation of the matrix elements describ-
namical hybridization on the MOs derived from the states
                                                                              ing hopping from the Ti orbital dσ to nth oxygen is
dσ , with the spin playing the role of a passive index de-
termined by the orbital state. The Ti spin-orbit splitting
                                                                                           δtn,σ = Qeiσnπ/2 [al cos ξ + iσat sin ξ],   (5)
λ = 17 meV is negligible compared to the insulating gap
∆ = 3.2 eV defining the characteristic energy scale. A                        where ξ = φ−nπ/2, φ is the polar angle of instantaneous
finite amplitude of dxy in some of the SOC states does                        displacement and al , at are real parameters with units of
not affect the mechanism discussed below.                                     force describing the effects of displacement Q in the di-
   We now consider the MO states formed by Ti dσ or-                          rection of and normal to the bond, respectively. Since
bitals and the pz orbitals of the four oxygen atoms coordi-                   tT i−O < 0 and Q > 0, ξ = 0 describes increased length
nating Ti in the xy plane. We count the energy relative to                    of the Ti-O4 bond, so al > 0. Likewise, Q > 0, ξ = π/2
the atomic oxygen p-level. In the absence of ferroelectric                    describes a shift of O4 in the +y direction, which is equiv-
distortion, the two-fold degenerate Ti atomic levels dσ                       alent to the positive (negative) phase shift of the orbital
with energy Ed and the four degenerate pz -levels of oxy-                     d+ (d− ), corresponding to at > 0 in Eq. (5). These pa-
gen are split due to hybridization into two orbitally non-                    rameters can be obtained from ab-initio calculations or
degenerate and two orbitally degenerate states, Fig. 2(a).                    by the Koster-Slater method, as discussed below.
The non-degenerate states are the bonding and the an-
                                                                                 For the circularly polarized phonon mode, φ = cωt
tibonding states of the four oxygen atoms, both non-
                                                                              with chirality c = ±1. Then
bonding with Ti,
                    1X            1X                                                   δtn,σ = Qa+ eicσωt + (−1)n Qa− e−icσωt .        (6)
           ψn1 =       pn , ψn2 =    (−1)n pn ,                         (1)
                    2             2
                                                                              where we use a± = (al ± at )/2. The first term is
                                            th
where pn denotes the pz orbital of n oxygen, n = 1..4                         isotropic, enabling coupling between the isotropic non-
[see Fig. 1(a)]. Their energies are En1,n2 = ±2tO−O ,                         bonding state ψn1 [Eq. (1)] and ψa,σ . The corresponding
where tO−O < 0 is the matrix element between pz orbitals                      matrix element is Vσ,n1 = 2 sin θa Qa+ e−icσωt . Mean-
of the nearest-neighbor oxygen atoms. The two orbitally                       while, the second term in Eq. (6) couples ψa,σ to ψn2 ,
degenerate states are the antibonding and the bonding                         with the matrix element Vσ,n2 = 2 sin θa Qa− eicσωt .
states with respect to the Ti-O hybridization,
                    cos θa,b X inσπ/2                                              II.2.     Transient Atomic Orbital Magnetism
         ψaσ,bσ =             e       pn + sin θa,b dσ ,                (2)
                       2
with energies                                                                    We now show that time-dependent hybridization asso-
                               r                                              ciated with the chiral phonon results in transient atomic
                       Ed          Ed2                                        polarization. If a+ and a− were equal, then Vσ,n2 =
                Ea,b =    ±            + 2t2T i−O ,                     (3)   V−σ,n1 and phonons would not break the symmetry be-
                       2            4
                                                                              tween the orbitals d+ and d− carrying orbital moment.
where tT i−O < 0 denotes the hopping matrix element                           However, since both al and at are positive, a+ > a− . The
from the pz orbital of oxygen No.4 to dσ orbital of                           first term in Eq. (6) is dominant, resulting in a chiral per-
Ti, tT i−O = ⟨dσ |Ĥ|p4 ⟩, where Ĥ is the Hamiltonian.                       turbation due to different phonon-driven admixing of ψ+
                                                                                                                            4

and ψ− to the non-bonding states. Qualitatively, the fac-              We now estimate the relationship between induced
tor e±iωt either increases or decreases the time-dependent          magnetization and the amplitude Q of atomic displace-
phase difference between ψn1,n2 and ψa,σ orbitals, result-          ment. The antibonding mode ψa,σ describing the con-
ing in the dependence of MO mixing on the product of                duction band states is dominated by the Ti d-orbitals,
phonon chirality c and orbital moment σ.                            i.e. sin θa <
                                                                                ∼ 1. We evaluate the effective forces a+ , a−
  We use time-dependent perturbation theory [28] with               using the Koster-Slater method [31]. The value of at is
respect to δtn,σ to analyze this effect. Approximating              determined by the bonding energy geometrically scaled
the time dependence of phonon amplitude by Q(t) =                   by the directional dependence of orbital phase,
Qe−|t|/τ with the temporal pulse width τ ≫ h̄/∆, the
probability to find an electron in the state ψa,σ at the                         at = −tT i−O /rT i−O ≈ 5.7 eV /nm,      (10)
polarization maximum at t = 0 is
                                                                    where rT i−O = 0.2 nm is the titanium-oxygen distance,
                                                                    and tT i−O = −Vpdπ = 1.14 eV with the standard nota-
                           4 sin2 θa Q20 (a2+ − a2− )               tion for the hopping matrix element between the d and p
          pσ (t = 0) = −                                ,     (7)   orbitals [31]. Meanwhile, al is the derivative of the bond
                           (∆ − cσh̄ω)2 + h̄2 /τ 2                  energy with respect to the oxygen-titanium distance,
where we have neglected the contribution of tO−O to the                         dtT i−O (rT i−O )   7at
denominator dominated by the Ti-O bonding. Account-                      al =                     =     = 20.0 eV /nm,   (11)
                                                                                     drT i−O         2
ing for the two possible directions of spin doubling the
considered orbital effect and using 1/τ ≪ ∆/h̄, the in-             where we used the semi-empirical dependence
duced orbital moment mz (t = 0) = −2µB (p+ − p− ) is                                       −7/2
                                                                    tT i−O (rT i−O ) ∝ rT i−O [31].       Thus, we estimate
                                                                    a+ ≈ 13 eV/nm, a− ≈ 7 eV/nm. These numbers are
                       32µB ch̄ω sin2 θa Q20 (a2+ − a2− )           order-of-magnitude estimates due to the semi-empirical
      mz,a (t = 0) ≈                                      ,   (8)
                                     ∆3                             nature of matrix element scaling with the bond length
                                                                    and the neglected ellipticity of atomic motion. To
where µB is Bohr magneton. The magnetic moment is                   determine more precise values of these parameters,
quadratic in the displacement amplitude Q, consistent               additional first-principles calculations are warranted.
with the observations of Ref. [1]. Note that (a2+ − a2− ) =            For h̄ω/∆ ≈ 0.004, orbital moment of the order of 10−2
al at , showing that an unquenched orbital state required           µB estimated in Ref. [1] requires amplitude Q ≈ 0.08 nm,
for a finite at is essential for electron magnetization.            which is unrealistically large despite STO’s proximity to
   The experiment of Ref. [1] also showed that the mag-             ferroelectric phase transition. Below, we discuss another,
nitude of induced magnetization closely followed the                inter-atomic contribution that constructively combines
phonon amplitude, disappearing together with the lat-               with the discussed intra-atomic effect. Other possible
ter. Our analysis reproduces this transient behavior as             contributions not captured by our MO model are also ex-
well. According to the time-dependent perturbation the-             pected to constructively add, by angular momentum con-
ory, the probability that electron is found in the state            servation argument. Furthermore, impurity states can
ψa,σ at t ≫ τ is                                                    be qualitatively interpreted in terms of a reduced effec-
                                                                    tive gap ∆ in Eq. (8), which can result in a significant
                         16h̄2 sin2 θa Q20 (a2+ − a2− )             contribution to transient magnetic moment. Altogether,
         pσ (t = ∞) =                                   .     (9)
                              τ 2 (∆ − cσh̄ω)4                      these effects may account for the observed magnitude of
                                                                    induced magnetization.
Using the experimental parameters of Ref. [1], this value
is scaled by the factor 4τ 2 ∆2 /h̄2 ∼ 6 × 10−5 compared
to the maximum transient amplitude Eq. (7). In other                   II.3.    Transient interatomic orbital magnetism
words, the probability that an electron is actually ex-
cited from the valence band into the conduction band                   In the modern theory of orbital magnetism, atomic or-
due to the interaction with phonons is negligible. Tran-            bital magnetization discussed above generally co-exists
sient magnetization cannot be described as electronic ex-           with interactomic contribution [35]. Optical phonons
citation driven by the electron-phonon interaction in the           break both time and spatial inversion symmetries, which
rigid-band approximation. Instead, it can be interpreted            is generally expected to result in a non-vanishing Berry
as a virtual excitation of conduction-band electrons, i.e.          curvature underlying this contribution [19]. Berry cur-
a transient state that results from the dynamical evo-              vature of electronci bands is usually interpreted as a ge-
lution of the band states coupled non-perturbatively to             ometric effect in the reciprocal space. Nevertheless, one
the lattice dynamics, which vanishes together with the              can ask whether the minimal real-space MO model in-
phonon-driven mixing of electronic states. Analysis of              troduced in this work can account for this mechanism,
electron-phonon coupling in several other materials ar-             providing a simple estimate for its significance. Qualita-
rived at a similar conclusion [20, 29, 30], suggesting that         tively, the MO wavefunction ψ(Q) has a non-trivial or-
it may be quite general.                                            bital structure parametrized by the 2D manifold of ionic
                                                                                                                                5

   (a)                                  (b)                        gen atom is
                          Eeff
   Eeff    O1                                                                                   1 2 sin θa Qa+ ei∆t
                                              O1 O2 O3 O4
                                                                                              cn ≈−
                                                                                                2         ∆2                  (13)
          Ti     O4                                                             i(cωt−πn/2)           −i(cωt−πn/2)
                                                                      ∗[(∆ − ω)e            + (∆ + ω)e             ].
    O2
          O3                     Eeff                              According to this expression, the wavefunction acquires a
                                                                   chiral phase winding around the oxygen atoms, resulting
                      Eeff
                                                                   in a circulating current between sites n and n + 1
Figure 3. (a) Interatomic orbital magnetization in the MO                                      2etO−O
approximation results from the charge re-distribution among                       In,n+1 = −          Im(c∗n cn+1 ),          (14)
                                                                                                  h̄
the oxygen atoms coordinating Ti, due to the modulation of
hybridization matrix elements. The color intensity represents      where e is the magnitude of electron charge. This cur-
electron density. (b) Analogy to the Thouless pump. The            rent includes an oscillating component and a constant
dots show the location of maximum electron density.                contribution
                                                                                             32etO−O sin2 θa Q2 a2+ ωc
                                                                             ⟨In,n+1 ⟩ = −                             .      (15)
                                                                                                       ∆3
displacement field Q = (Qx , Qy ), enabling a finite Berry
curvature Ωxy = 2Im(⟨∂ψ/∂Qy |∂ψ/∂Qx ⟩) [20].                       Since the current is proportional to ω, the charge trans-
   The interatomic magnetic moment in the MO model                 ferred per period is independent of ω, consistent with the
results from the charge re-distribution due to the vari-           geometric origin of this effect. The magnetic moment is
ation of Ti-O bonds. The closest to Ti oxygen atom is
                                                                                 a2             8ea2 tO−O sin2 θa Q2 a2+ ωc
most strongly hybridized, resulting in the largest elec-             mz1 = −        ⟨In,n+1 ⟩ =                               (16)
tronic density. In the top panel of Fig. 3(a), this is the                       4                         ∆3
top oxygen atom. Conversely, the bottom oxygen in this             where a = 0.39 nm is the lattice constant of STO. Similar
panel has the smallest charge. This can be interpreted as          analysis for ψn2 yields
electron charge polarization due to the effective electric
field Eef f directed downward, opposite to the ionic polar-                              8ea2 tO−O sin2 θa Q2 a2− ωc
ization. As the displacement vector rotates, the effective                       mz2 =                               .        (17)
                                                                                                    ∆3
field rotates together with it, resulting in a chiral motion
of this polarization charge, i.e. a circulating current.           Since a+ > a− , the two contributions do not cancel, re-
                                                                   sulting in a non-vanishing total orbital moment. Taking
  The amount of charge transferred around the four oxy-
                                                                   into account the two spin directions, we obtain the total
gen atoms is independent of the period, consistent with
                                                                   inter-atomic orbital moment
the geometric origin of this process. It can be interpreted
by analogy to the Thouless pump [36], as illustrated in                                32µ1 ch̄ω sin2 θa Q20 (a2+ − a2− )
Fig. 3(b). The four-well profile represents the depen-                       µz,ia =                                      .   (18)
                                                                                                     ∆3
dence of crystal potential on direction, with the minima
along the Ti-O bonds labeled O1 -O4 in Fig. 3(b). As               the same expression as Eq. (8) for the atomic mo-
the displacement vector rotates, this energy landscape is          ment, except it is scaled by the magnetic moment µ1 =
periodically modulated, resulting in charge pumping as             −ea2 tO−O /2h̄ instead of the Bohr magneton. In partic-
indicated by a filled dot and curved arrows. In contrast           ular, the induced moment is quadratic in displacement
to the Thoughless pump, finite size results in transfer of         and is transient, consistent with the experimental obser-
non-integer charge per cycle.                                      vations. We use Koster-Slater approximation to estimate
   To analyze this effect, we use the time-dependent per-          tO−O = −0.8 eV, giving µ1 ≈ 1.6µB . It is remarkable
turbation approximation for the MO states discussed                that two contributions of different origin and expressed
above. We will show that the perturbed non-bonding                 in terms of unrelated material parameters give such sim-
states ψn1,n2 acquire a chiral amplitude on the oxygen             ilar results. This is consistent with other studies suggest-
atoms, resulting in a circulating current that produces            ing that intra- and inter-atomic contributions to orbital
interatomic magnetization. The lowest-order correction             magnetization are usually comparable [37].
to the non-bonding wavefunction ψn1 is
                                                                          III.     DISCUSSION AND SUMMARY
                 (1)
                          X        ei(∆/h̄−σω)
                ψn1 = −      Vσ,n1             ψaσ .        (12)
                                    ∆ − σh̄ω                          We showed that a minimal molecular orbital approx-
                           σ
                                                                   imation can serve as a testbed for the mechanisms con-
                                                                   tributing to magnetism induced by interaction between
The resulting time-dependent amplitude cn on nth oxy-              lattice dynamics and electrons, enabling simple estimates
                                                                                                                          6

of the relevant contributions. Chiral lattice dynamics        by the large gap ∆ = 3.2 eV of STO and is robust with
produces intra-atomic orbital electron magnetization due      respect to thermal relaxation. Phonon-induced electron
to the polarization of the Ti atom, as well as inter-atomic   magnetization only requires a Kramer’s doublet formed
contribution due to the chiral current circulating around     by orbitally nontrivial states, which is general to non-
oxygen atoms coordinating it. The magnetization esti-         magnetic materials with p or d bonding. However, its
mated in our model is smaller than experimentally ob-         efficiency can be enhanced by degenerate orbital states
served. Remarkably, the inter-atomic contribution is very     whose superpositions can support large unquenched or-
close to intra-atomic contribution. This suggests that        bital moments. In our model, both the intra- and the
additional contributions not captured by our model may        inter-atomic moments, Eqs. (8), (18) are proportional to
also be similar. Such contributions may include the cur-      (a2+ − a2− ) = al at . The coefficient at reflecting orbital
rent circulating around the square plaquettes whose vor-      chirality would vanish for an orbitally quenched state, re-
texes are formed by the Ti atoms, as well as orbitals         sulting in vanishing electronic orbital moment. In STO,
dxy , px and pz and the corresponding bonds. In contrast      a finite at results from the orbital polarization of the anti-
to ionic motion, different electronic contributions should    bonding states d+ , d− . The condition for orbital degen-
add constructively based on the general angular momen-        eracy is naturally satisfied by the high-symmetry (e.g.
tum conservation argument, which altogether may ac-           cubic or tetragonal) phases of complex oxides. In sys-
count for the observed large moment.                          tems with C3 symmetry such graphene, this degeneracy
                                                              is a direct consequence of the chirality of its irreducible
   Our model of STO provides a tractable example of
                                                              representations.
non-perturbative electron-phonon interaction that can-
                                                                 In our analysis, the magnetic polarization scales with
not be interpreted in the language of electron-phonon
                                                              the gap as 1/∆3 at ∆ ≫ h̄ω, resulting in a dramatic in-
scattering, supporting the proposed strong-coupling the-
                                                              crease of efficiency at small gap. At ∆ = ω, the orbital
ories [14]. The transient nature of induced electronic
                                                              moment in the approximation Eq. (8) diverges, which
magnetism shows that the demonstrated effects describe
                                                              corresponds to resonant excitation of the chiral state ψa,σ
dressing of chiral phonons by electron dynamics, result-
                                                              with σ = c. As evidenced from Eq. (9), for h̄ω approach-
ing in re-normalization of the phonon magnetic moment.
                                                              ing ∆, the non-transient orbital moment also increases,
A similar conclusion was reached in the analysis of geo-
                                                              signifying an increased population of orbitally polarized
metric phonon magnetism in gapped bilayer graphene,
                                                              electrons excited into the conduction band. This depen-
where non-geometric phonon magnetic moment is ab-
                                                              dence allows control of the induced magnetic moment by
sent [20]. In contrast to the inverse cubic dependence
                                                              gap modulation [20]. A similar effect can be achieved
on the gap obtained in out analysis, the magnetization
                                                              by doping [30]. Efficient resonant enhancement was ob-
in graphene was shown to scale inversely with the square
                                                              served in narrow-gap materials [21], and supported by
of the gap, warranting further analysis and experimental
                                                              analysis in terms of phonon-induced splitting of Kramers
studies. Our analysis also predicts that induced magne-
                                                              doublet [29, 38]. This mechanism of controlled genera-
tization is quadratic in ionic displacement, instead of the
                                                              tion of orbital moments can be attractive for orbitronic
linear dependence in Ref. [20], which is consistent with
                                                              applications, bypassing the electrical currents needed in
the experiment.
                                                              the the orbital moment generation by orbital Hall ef-
    The demonstrated effect is a general consequence of       fect [23, 39]. Importantly, orbital magnetization can be
cogwheel-like locking between the phase of atomic or-         transferred across interfaces between different materials
bitals with finite orbital moments and the positions of       due to the orbital selectivity of hybridization [13], and
coordinating atoms. Just as the static crystal field gen-     used to control the magnetic state via SOC [40, 41].
erally quenches orbital moments, dynamical crystal field         Acknowledgments. This work was supported by the
results in modulation of their unquenched components,         NSF award ECCS-2005786. I thank Stefano Bonetti and
i.e. transient orbital moments. All the bands remain          Alexander Balatsky for the helpful discussions, and Do-
filled or empty in this process. Therefore, it is protected   minik Juraschek for the feedback on the manuscript.




 [1] M. Basini, M. Pancaldi, B. Wehinger, M. Udina,                540–544 (2024).
     V. Unikandanunni, T. Tadano, M. C. Hoffmann, A. V.        [5] D. M. Juraschek, M. Fechner, A. V. Balatsky, and N. A.
     Balatsky, and S. Bonetti, Nature 628, 534–539 (2024).         Spaldin, Phys. Rev. Mater. 1, 014401 (2017).
 [2] M. Basini, M. Udina, M. Pancaldi, V. Unikandanunni,       [6] A. Rückriegel, S. Streib, G. E. W. Bauer, and
     S. Bonetti, and L. Benfatto, Phys. Rev. B 109, 024309         R. A. Duine, Physical Review B 101, 10.1103/phys-
     (2024).                                                       revb.101.104402 (2020).
 [3] S. J. Barnett, American Journal of Physics 16, 140–147    [7] D. M. Juraschek and N. A. Spaldin, Phys. Rev. Mater.
     (1948).                                                       3, 064405 (2019).
 [4] C. S. Davies, F. G. N. Fennema, A. Tsukamoto, I. Raz-     [8] S. Streib, Phys. Rev. B 103, L100409 (2021).
     dolski, A. V. Kimel, and A. Kirilyuk, Nature 628,         [9] J. J. Nakane and H. Kohno, Phys. Rev. B 97, 174403
                                                                                                                              7

     (2018).                                                          B 106, 224519 (2022).
[10] R. G. Littlejohn and M. Reinsch, Rev. Mod. Phys. 69,        [28] L. D. Landau and E. M. Lifshitz, Quantum mechanics,
     213 (1997).                                                      3rd ed., edited by J. Menzies (Butterworth-Heinemann,
[11] D. Go, D. Jo, H.-W. Lee, M. Kläui, and Y. Mokrousov,            Oxford, England, 1981).
     EPL 135, 37001 (2021).                                      [29] S. Chaudhary, D. M. Juraschek, M. Rodriguez-Vega, and
[12] D. A. Garanin and E. M. Chudnovsky, Physical Review              G. A. Fiete, Phys. Rev. B 110, 094401 (2024).
     B 103, 10.1103/physrevb.103.l100412 (2021).                 [30] R. M. Geilhufe and W. Hergert, Phys. Rev. B 107,
[13] S. Urazhdin, Phys. Rev. B 108, L180404 (2023).                   L020406 (2023).
[14] J. H. Mentink, M. I. Katsnelson, and M. Lemeshko, Phys-     [31] W. A. Harrison, Electronic Structure and the Properties
     ical Review B 99, 10.1103/physrevb.99.064428 (2019).             of Solids: The Physics of the Chemical Bond (Dover Pub-
[15] Proceedings of the Royal Society of London. Series               lications, New York, 1989).
     A. Mathematical and Physical Sciences 264, 458–484          [32] C. Kittel, Indirect exchange interactions in metals, in
     (1961).                                                          Solid State Physics (Elsevier, 1969) p. 1–26.
[16] J. H. Van Vleck, Phys. Rev. 57, 426 (1940).                 [33] W. D. Rice, P. Ambwani, M. Bombeck, J. D. Thompson,
[17] S. Mankovsky, S. Polesya, H. Lange, M. Weißenhofer,              G. Haugstad, C. Leighton, and S. A. Crooker, Nature
     U. Nowak, and H. Ebert, Physical Review Letters 129,             Materials 13, 481–487 (2014).
     10.1103/physrevlett.129.067202 (2022).                      [34] S. Ivanov, J. Peacock, and S. Urazhdin, Phys. Rev.
[18] T. Thonhauser, D. Ceresoli, D. Vanderbilt, and                   Mater. 7, 014404 (2023).
     R. Resta, Physical Review Letters 95, 10.1103/phys-         [35] R. Resta, Journal of Physics: Condensed Matter 22,
     revlett.95.137205 (2005).                                        123201 (2010).
[19] L. Trifunovic, S. Ono, and H. Watanabe, Phys. Rev. B        [36] D. J. Thouless, Phys. Rev. B 27, 6083 (1983).
     100, 054408 (2019).                                         [37] A. Pezo, D. Garcı́a Ovalle, and A. Manchon, Phys. Rev.
[20] X.-W. Zhang, Y. Ren, C. Wang, T. Cao, and                        B 106, 104414 (2022).
     D. Xiao, Physical Review Letters 130, 10.1103/phys-         [38] H. Mustafa, C. Nnokwe, G. Ye, M. Fang, S. Chaudhary,
     revlett.130.226302 (2023).                                       J.-A. Yan, K. Wu, C. J. Cunningham, C. M. Hemesath,
[21] J. Luo, T. Lin, J. Zhang, X. Chen, E. R. Blackert, R. Xu,        A. J. Stollenwerk, P. M. Shand, E.-H. Yang, G. A. Fiete,
     B. I. Yakobson, and H. Zhu, Science 382, 698–702 (2023).         R. He, and W. Jin, ACS Nano 19, 11241 (2025).
[22] D. M. Juraschek, T. Neuman, and P. Narang, Physical         [39] D. Go, F. Freimuth, J.-P. Hanke, F. Xue, O. Gomonay,
     Review Research 4, 10.1103/physrevresearch.4.013129              K.-J. Lee, S. Blügel, P. M. Haney, H.-W. Lee, and
     (2022).                                                          Y. Mokrousov, Phys. Rev. Res. 2, 033401 (2020).
[23] H. Kontani, T. Tanaka, D. S. Hirashima, K. Yamada,          [40] S. Ding, A. Ross, D. Go, L. Baldrati, Z. Ren, F. Freimuth,
     and J. Inoue, Phys. Rev. Lett. 102, 016601 (2009).               S. Becker, F. Kammerbauer, J. Yang, G. Jakob,
[24] A. H. Kahn and A. J. Leyendecker, Phys. Rev. 135,                Y. Mokrousov, and M. Kläui, Phys. Rev. Lett. 125,
     A1321 (1964).                                                    177201 (2020).
[25] L. F. Mattheiss, Phys. Rev. B 6, 4718 (1972).               [41] S. Lee, M.-G. Kang, D. Go, D. Kim, J.-H. Kang, T. Lee,
[26] M. T. Dylla, S. D. Kang, and G. J. Snyder, Angewandte            G.-H. Lee, J. Kang, N. J. Lee, Y. Mokrousov, S. Kim,
     Chemie International Edition 58, 5503 (2019).                    K.-J. Kim, K.-J. Lee, and B.-G. Park, Communications
[27] S. Urazhdin, E. Towsif, and A. Mitrofanov, Phys. Rev.            Physics 4, 10.1038/s42005-021-00737-7 (2021).

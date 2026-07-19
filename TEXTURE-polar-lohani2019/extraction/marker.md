# Lohani et al. 2019 — Quantum skyrmions in frustrated ferromagnets (arXiv:1901.03343)

> **EXTRACTION NOTE:** `marker` and `nougat` binaries are NOT installed on this host
> (`which marker nougat` → not found). This file is an **interim extraction produced with
> `pdftotext -layout`** as the fallback mandated by the computational-replication-execution
> skill (§2 Parse). Equations render as linearized text, not LaTeX. Regenerate with Marker
> when the binary is available. Source PDF: textures-polar-lohani2019.pdf

---

                                                                                 Quantum skyrmions in frustrated ferromagnets

                                                                             Vivek Lohani1 ,∗ Ciarán Hickey1 , Jan Masell1 , and Achim Rosch1,2
                                                                    1
                                                                        Institute for Theoretical Physics, University of Cologne, 50937 Cologne, Germany and
                                                                             2
                                                                               Department of Physics, Harvard University, Cambridge MA 02138, USA

                                                                  We develop a quantum theory of magnetic skyrmions and antiskyrmions in a spin-1/2 Heisenberg
                                                               magnet with frustrating next-nearest neighbor interactions. Using exact diagonalization we show
                                                               numerically that a quantum skyrmion exists as a stable many-magnon bound state and investigate
                                                               its quantum numbers. We then derive a phenomenological Schrödinger equation for the quantum
                                                               skyrmion and its internal degrees of freedom. We find that quantum skyrmions have highly unusual
                                                               properties. Their bandwidth is exponentially small and arises from tunneling processes between
                                                               skyrmion and antiskyrmion. The bandstructure changes both qualitatively and quantitatively when
                                                               a single spin is added or removed from the quantum skyrmion, reflecting a locking of angular
arXiv:1901.03343v3 [cond-mat.str-el] 7 Oct 2019




                                                               momentum and spin quantum numbers characteristic for skyrmions. Additionally, while for weak
                                                               forces the quantum skyrmion is accelerated parallel to the force, it moves in a perpendicular direction
                                                               for stronger fields.


                                                     Magnetic skyrmions are textures in the magnetization           identify skyrmion-like quantum states. While a “topo-
                                                  which can be characterized by a topological winding num-          logical quantization” does not exist in the quantum case,
                                                  ber. Magnetic skyrmions were first discovered in the chi-         one still obtains well defined “quantized” particles as sta-
                                                  ral cubic magnet MnSi [1] and subsequently in a wide              ble many-magnon bound states. For the purpose of this
                                                  range of chiral magnets, magnetic monolayers and lay-             paper we therefore define a quantum skyrmion as a sta-
                                                  ered magnetic systems with sizes ranging from nanome-             ble bound state which has properties that smoothly con-
                                                  ters to micrometers [2–9]. Skyrmions can be manipu-               nect to classical skyrmion states. We will show that such
                                                  lated by small electric [6–8] and heat currents [10] which        states are stable even in the presence of quantum tunnel-
                                                  makes them interesting for future applications, such as           ing and use correlation functions to show their relation
                                                  data storage [11].                                                to classical skyrmions.
                                                     A single skyrmion in a magnetic film can be viewed as a           The second question concerns the quantum proper-
                                                  particle. A direct consequence of its topological winding         ties of such a skyrmion state. The ground state prop-
                                                  number is that its equation of motion [12] is dominated           erties of a single quantum skyrmion in a chiral magnet
                                                  by a ‘gyrocoupling’ to an effective magnetic field arising        are (at least to leading order approximation) rather ob-
                                                  from the Berry phases picked up from the spins during             vious: as their dynamics is governed by a large mag-
                                                  the motion of the texture. Furthermore, its equation of           netic field, the ground state is localized in a Landau level
                                                  motion as a classical particle can be described by a damp-        with edge channels at the sample boundary. Corrections
                                                  ing constant, an effective mass and a special gyrodamp-           to this picture arise from an exponentially small lattice
                                                  ing [13]. Viewing the skyrmion as a classical particle is         potential which gives rise to a bandstructure [15, 16].
                                                  justified in most experimental situations: the skyrmions          Only a few studies have considered quantum properties
                                                  are often large objects involving a large number of spins         of skyrmions. Lin and Bulaevskii [17] investigated the
                                                  and the coupling to electrons in a metal or to thermal            role of a defect for skyrmions localized in a Landau band
                                                  magnons will destroy effects of quantum coherence.                and Psaroudaki et al. [18] calculated the skyrmion mass
                                                     An interesting fundamental question concerns the               in a quantum model, while Derras-Chouk et al. investi-
                                                  quantum nature of magnetic skyrmions. Experimentally,             gated the quantum collapse of a skyrmion due to tunnel-
                                                  they will mainly be of importance in insulating magnets           ing processes [19]. Diaz and Arovas considered the in-
                                                  [4] at temperatures well below the bulk gap of the un-            verse process − the nucleation of skyrmions by quantum
                                                  derlying ferromagnet. Two important questions arise               tunneling [20]. In an interesting study, Takashima, Hi-
                                                  in this context: (i) How can one define and identify a            roaki and Balents [15] showed that it is possible to obtain
                                                  skyrmion in a quantum spin system, and (ii) what are              a Bose-Einstein condensate of skyrmions. Very recently,
                                                  the quantum properties of such a state. In the classi-            Ochoa and Tserkovnyak [16] gave a concise overview of
                                                  cal case, the quantized winding number can be used to             the quantum properties of skyrmions in chiral magnets,
                                                  uniquely identify skyrmions. Due to Heisenberg’s un-              including their semiclassical dynamics.
                                                  certainty principle, this is, however, not possible in the           In this paper we will investigate the quantum dynam-
                                                  quantum case, as has been pointed out e.g. in Ref. [14],          ics of skyrmions with internal degrees of freedom. We
                                                  where it was also suggested to compare spin-spin corre-           will consider the two-dimensional ferromagnetic quantum
                                                  lation functions of classical and quantum spin systems to         Heisenberg model where skyrmions arise in the presence
                                                                                                                    of frustrating antiferromagnetic next-nearest neighbor in-
                                                                                                                    teractions. Frustration stabilized skyrmions are expected
                                                                                                                    to be much smaller than skyrmions stabilized by weak
                                                  ∗ vlohani@smail.uni-koeln.de
                                                                                                                    spin-orbit interactions, therefore quantum effects might
                                                                                                                                 2

(a)                            (b)                              investigating both the coupling to the helicity degree of
                                                                freedom and the skyrmion-antiskyrmion tunneling.


                                                                         I.   SKYRMIONS IN FRUSTRATED
                                                                                 FERROMAGNETS


(c)                            (d)                                 We consider an XXZ spin-1/2 Heisenberg model on a
                                                                triangular lattice at zero temperature in a magnetic field:
                                                                                     X                X
                                                                         H = − J1        Si · Sj + J2   Si · Sj
                                                                                        hiji               hhijii
                                                                                               X                    X
                                                                                          −K          Siz Sjz − B       Siz .   (1)
                                                                                               hiji                 i

                (e)
                                                                J1 is a ferromagnetic nearest-neighbor coupling (set to
                                                                1 in the following) and J2 an antiferromagnetic next-
                                                                nearest neighbor coupling which can destabilize the fer-
                                                                romagnetic state. For J2 > 1/3 the spin-waves of the
                                                                ferromagnetic ground state have a maximum rather than
                                                                a minimum of their dispersion at zero momentum and
                                                                the corresponding non-linear-σ model obtains a neg-
FIG. 1. Schematic plot of the classical spin configurations     ative spin-stiffness favouring non-trivial magnetic tex-
of skyrmions and antiskyrmions. In (a), (b) skyrmions with
                                                                tures [23, 24]. K > 0 effectively leads to an easy-axis
helicity φ = 0 and φ = π/2 are shown. In (c), (d) the cor-
responding antiskyrmions are displayed. Skyrmions are rota-     anisotropy which helps to stabilize skyrmion solutions
tionally symmetric as the spin rotates with the spatial coor-   and B is an external magnetic field. The model is spin-
dinate. For antiskyrmions the direction of spatial and spin     rotation invariant around the z axis.
rotations is opposite, see Eq. (2). A quantum skyrmion in
a frustrated magnet can tunnel between skyrmion and anti-
skyrmion states and is approximately described by superpo-                         A.    Classical solutions
sitions of classical configurations, as shown in (e).
                                                                   The classical variant of our model (1) (with a local
                                                                anisotropy term K(Siz )2 instead of the nearest neighbor
be more important in this case. In the classical limit,         term KSiz Sjz ) has been shown [23, 24] to support mag-
skyrmion states in frustrated magnets have first been in-       netic skyrmions and antiskyrmions which have by sym-
vestigated by Ivanov et al. [21] and more recently by           metry exactly the same energy. A classical field configu-
Okubo et al. [22], Leonov and Mostovoy [23], Lin and            ration of a single skyrmion embedded in a ferromagnetic
Hayami [24], and Zhang et al. [25, 26]. They obtained           background can be described by two polar angles θs (r −
classical skyrmion solutions by minimizing a classical en-      R) and φs (r − R). Here (sin θs cos φs , sin θs sin φs , cos θs )
ergy functional. Remarkably, due to the absence of spin-        describes the orientation of a classical spin and R is the
orbit interactions, skyrmion and antiskyrmion have ex-          position of the skyrmion. In the continuum limit, θs (x)
actly the same energy. Furthermore, the spins can rotate        depends only on the distance from the skyrmion cen-
freely around the z axis. This leads to two internal de-        ter, x = |r − R|, smoothly interpolating between a cen-
grees of freedom, the helicity φ describing rotations of        tral spin pointing opposite to the ferromagnetic state,
spin and the skyrmion charge σ = ±1, see Fig. 1. Inter-         θs (0) = π, and the ferromagnetic state, θs (x → ∞) = 0.
estingly, the motion of the skyrmion is thereby coupled to      The in-plane angle φs takes the simple form
a precession of the helicity [23–25, 27–29]. Recently, the
Tokura group [30] reported the discovery of skyrmions                         φs (x) = σφ(x) + φ0 ,          σ = ±1 ,           (2)
in a centrosymmetric metallic material magnet, where
skyrmion formation seems to be mainly driven by frus-           where φ is the polar angle in real space. For σ = 1 one
trating interactions rather than spin-orbit coupling. A         obtains a skyrmion where the spin rotation follows the
number of other candidate systems have, e.g., been dis-         spatial rotation. For an antiskyrmion, σ = −1, the spin
cussed in Ref. [25].                                            rotation and spatial rotation occur in opposite directions,
   In the following we will first show numerically, using       see Fig. 1. Changing the parameter φ0 induces a rotation
exact diagonalization, that a skyrmion exists as a many-        of spins. For φ0 = 0 or φ0 = π/2 one obtains, for ex-
body bound state in a quantum system and that it is             ample, the so-called Néel skyrmions or Bloch skyrmions,
a stable quantum excitation. In a second step we will           respectively. The energy of the classical solutions is inde-
develop a phenomenological theory of skyrmion motion            pendent of φ0 due to spin-rotation symmetry about the
                                                                                                                                                           3

               0.02   0.02                                 0.06   0.06                   to the ferromagnetic state of the flake are denoted by
                                                                                         En (Nf , lz ) (the index n refers to the enumeration scheme
    0.02   0.24   0.61   0.24     0.02          0.06   0.43   0.88   0.43      0.06
                                                                                         for eigenstates within a definite Nf -lz sector). E0 (Nf , lz )
 0.02   0.61   0.73   0.73    0.61    0.02   0.06   0.88   0.54   0.54   0.88     0.06   is the energy of the ground state in a given Nf -lz sector.
    0.24   0.73          0.73     0.24          0.43   0.54          0.54      0.43
                                                                                         Sotnikov et al. [14] have also used exact diagonalization
                                                                                         of a quantum magnet to search for skyrmion-like ground
 0.02   0.61   0.73   0.73    0.61    0.02   0.06   0.88   0.54   0.54   0.88     0.06
                                                                                         states in a small flake. However, in contrast to our study
    0.02   0.24   0.61   0.24     0.02          0.06   0.43   0.88   0.43      0.06      they use much smaller flakes, open boundary conditions
                                Nff ==77
                                                                                         and a Hamiltonian dominated by Dzyaloshinskii Moriya
 K ==0.05
 K     0.05    0.02   0.02      N            KK==
                                                0.06
                                                  0.06     0.06   0.06      NNff =
                                                                                 = 99
                                m    = 00
                                 lzz =                                       m
                                                                             lz z== 2
                                                                                    2    interactions.
                                                                                            From a quantum mechanical point of view, a skyrmion
FIG. 2. Magnetic structure of a quantum skyrmion calculated                              in a ferromagnetic background is a bound state compris-
for a flake with 31 sites embedded in a ferromagnetic back-                              ing of a fixed number of flipped spins, Nf . To demon-
ground. The quantum skyrmions shown are bound states of                                  strate that such a bound state exists, we have to show
7 (left) and 9 (right) flipped spins (J2 = 0.5, left: K = 0.05,                          that it is has a lower energy compared to a bound state
right K = 0.06). The color encodes hSiz i. The numbers in the                            with Nf − Ne flipped spins, where Ne flipped spins have
circles show antiferromagnetic correlations of the skyrmion                                                                                 m
                                                                                         ‘evaporated’ and are located at the minimum Emin       of the
spin in the xy-plane C⊥ = −4hSix Sīx + Siy Sīy i, where Sī is the                     magnon band of an infinitely large ferromagnet with
spin located at position −ri opposite to the spin Si located
at position ri . Note that hSix i = hSiy i = 0 as the quantum                             m
                                                                                         Emin = 3K                                                        (3)
skyrmion is an eigenstate of Sz . The left panel displays a                                             " 6                                               #
linear superposition of skyrmion and antiskyrmion (lz = 0)                                               X J1                           J2
with vanishing spin currents (c.f. lowest panel in Fig. 1).                                    + min               (1 − cos(kδi1 )) −      (1 − cos(kδi2 )) ,
                                                                                                   k
                                                                                                         i=1
                                                                                                               2                        2
The right panel displays a many-body state with finite an-
gular momentum (lz = 2) which we identify as a quantum
                                                                                         where δi1 and δi2 are vectors connecting the nearest and
skyrmion. The width of the black and grey arrows indicates
the size of the z-component of the spin current (largest value:                          next-nearest neighbors, respectively.
0.1 J1 ) on nearest-neighbor and next-nearest neighbor links,                              On this account we demand that E0 (Nf , lz ) < E0 (Nf −
                                                                                                         m
respectively.                                                                            Ne , lz ) + Ne Emin or, equivalently,

                                                                                                         E0B (Nf , lz ) < E0B (Nf − Ne , lz )             (4)
z axis. Also the energies of skyrmion and antiskyrmion,                                  for all 1 ≤ Ne ≤ Nf , where
σ = ±1, are identical as one can map the skyrmion to
the antiskyrmion by several symmetry transformations,                                                  EnB (Nf , lz ) = En (Nf , lz ) − Nf Emin
                                                                                                                                            m
                                                                                                                                                          (5)
for example by the product of time reversal and a rota-
tions of all spins (but not of space) by π around the x                                  is the binding energy of Nf spins, which can be viewed as
axis.                                                                                    the energy gained when Nf spins come together to form
                                                                                         a bound state instead of dispersing to infinity at the bot-
                                                                                         tom of the magnon band (E0B (0, lz ) = 0 by definition).
                                                                                         The binding energy is independent of the external mag-
                         B.       Quantum skyrmion
                                                                                         netic field as we consider the stability of the skyrmion
                                                                                         with respect to spin-conserving processes and thus com-
   In the following we want to investigate numerically                                   pare only states with the same value of Sz .
whether the full quantum model (1), made from quantum                                       Note that the energy E0 (Nf , lz ) for fixed Nf will al-
spins with s = 1/2, also supports stable skyrmion con-                                   ways decrease when the size of the flake is increased.
figurations. We will use exact diagonalization results of                                Therefore, the numerically determined value for E0B is
small systems embedded in a ferromagnetic background.                                    a rigorous upper bound for the binding energy in the in-
We have two goals: (i) to show rigorously that the pure                                  finite system. If we numerically find negative values for
quantum model is characterized by stable, many-particle                                  E0B in our finite size system, this would then rigorously
bound states and (ii) to identify the skyrmion nature of                                 establish the existence of multi-particle bound states on
those bound states using various correlation functions.                                  the infinite lattice.
   We consider an approximately round flake of 31 sites                                     Fig. 3 shows that for sufficiently large values of K and
embedded in a ferromagnetic background, see Fig. 2.                                      J2 , binding energies become negative and have a min-
Eigenstates are characterized by the number of flipped                                   imum as function of Nf at Nf = Nfmin . This proves
spins, Nf = Szfm − Sz , where Szfm = 31/2 is the total                                   the existence of multi-spin bound states in our model.
magnetization of the ferromagnetic state. Furthermore,                                   These states are our candidates for quantum skyrmions,
the flake has a 6-fold rotation symmetry with group ele-                                 the quantum counterparts of the classical skyrmion solu-
ments {exp[iLz 2π6 j] | j = 0, . . . , 5}, which allows us to use                        tions, as discussed in more detail below.
the angular momentum, lz = 0, 1, . . . , 5, defined modulo                                  The phase diagram in Fig. 4 gives an overview for
6 as a second quantum number. Eigenenergies relative                                     which values of J2 and K one can obtain skyrmion-like
                   0.8

                                                                                                                                                                                      4
                   0.6


                   0.4
(a) 0.2                                           K = 0.02   (b) 0.8             lz = 0                       J2 = 0.7       size. In Fig. 4(a) the points mark parameter values for
             EB
       0.1
                   0.2
                                                                                 lz = 1,5                                    which we obtain numerically a clear minimum when plot-
                                                                    0.6          lz = 2,4
                                                                                                                             ting the binding energy per flipped spin as function of Nf
       0.0         0.0                                                           lz = 3
                                                                                                                          l =(with   Nf ≤ 8 as our numerics is restricted to Nf ≤ 9).
                                                                    0.4
                                                                                                                          z   0
E0B




                                                             E0B
      -0.1        -0.2
                                                                    0.2                                                   l =For
                                                                                                                          z   1,5 these parameters our numerics indicates that for a
                                                                                                                          l =fixed
                                                                                                                          z   2,4    small magnetization (or a fixed, sufficiently large
      -0.2
                         0      2             4        6      8     0.0                                                   l =3
      -0.3        J2 = 0.5                        Nf
                                                                                                                          z
                                                                                                                             external magnetic field) it is energetically favorable to
                                                                   -0.2    K = 0.06                                          form separate skyrmions in a ferromagnetic background
      -0.4                               K = 0.07                                                     J2 = 0.5
             0           2      4             6        8                  0           2          4        6         8
                                                                                                                             rather than a single spin-down domain without internal
                                    Nf                                                               Nf                      structure. The dashed line shows that the upper phase
                                                                                                                                                                            m
                                                                                                                             boundary approximately follows the line Emin      = 0. We
FIG. 3. Binding energy of Nf -down spins embedded in a                                                                       find stable, finite-size, multi-spin bound states when at
ferromagnet as a function of Nf . Negative values fulfilling                                                                 zero magnetic field the underlying ferromagnet is intrin-
                                                                                                                                                  m
the inequality (4) are stable multi-spin bound states, often                                                                 sically unstable, Emin   < 0, with respect to spin flips.
with skyrmion signatures (see Fig. 2). The arrows denote the
                                                                                                                                 This implies that a magnetic field is needed to stabi-
states with the lowest binding energy per flipped spin, which
are expected to proliferate in the thermodynamic limit. (a)
                                                                                                                             lize both the ferromagnetic state and possible skyrmion
K is varied from 0.02 (top curve) to 0.07 (J2 = 0.5). (b) J2                                                                 phases thermodynamically, as is known from the classi-
takes values from 0.5 to 0.7 in steps of 0.05 (K = 0.06).                                                                    cal case [22–24]. Fig. 4(b) investigates which fields are
                                                                                                                             needed (for J2 = 0.5). The ferromagnet is energetically
                                                                                                                             stable with respect to spin flips above the red dot-dashed
 (a) 0.20                                                         (b) 0.25
                                                                                                                             line. Below the lower solid black line, a single skyrmion
                                                                          0.20                                FM             has a negative energy compared to the ferromagnetic
        0.15
                                                                          0.15                                               state and, consequently, the ferromagnet becomes unsta-
                                                                                           stable meta-                      ble with respect to proliferation of skyrmions. Typically,
  K




                                                                    B




        0.10
                                                                          0.10            skyrmions stable
                                                                                                      skyrmions              a skyrmion lattice will form in this regime (in a tiny re-
        0.05                  m
                             Emin =0
                                                                          0.05
                                                                                     J2 = 0.5                                gion of the phase diagram also a Bose-Einstein conden-
                                                                          0.00                                               sate of skyrmions may be realized [15]). Note that also
        0.00
            0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7                                      0        0.03   0.06     0.09     0.12      other ordered phases (e.g. helical states) may compete
                                         J2                                                         K                        with the skyrmion lattice − we did not try to investi-
                                                                                                                             gate such phases as the focus of our investigation are the
FIG. 4.      Phase diagrams. (a) Parameters for which sta-                                                                   properties of single quantum skyrmions.
ble multiple-spin bound states are found in a ferromagnet,
see Fig. 3. These states fulfill Eq. (4) and are thus stable                                                                     Therefore, we are mainly interested in the question
against ‘quantum evaporation’ of magnons into the ferromag-                                                                  whether single skyrmions may exist as (meta-) stable ex-
net. The dots denote parameters for which the binding energy                                                                 citations above the ferromagnetic ground state. Above,
per flipped spin has a minimum as a function of Nf . The red                                                                 we have shown that quantum skyrmions exist as stable
dots denote parameters where additionally the bound state                                                                    many-magnon bound states in a sector of fixed magneti-
with the lowest binding-energy per flipped spin obeys the                                                                    zation. In a real material magnetization is not fixed due
                                                    m
skyrmion selection rule, Eq. (11). Dashed line: Emin    = 0, see                                                             to the presence of weak spin-orbit coupling terms and
text. (b) A magnetic field is needed to stabilize the ferromag-                                                              dipolar interactions. Furthermore, acoustic phonons can
netic and the skyrmion phase. Below the red dot-dashed line                                                                  absorb energy. As a result, any state with energy higher
the ferromagnet (FM) is energetically unstable with respect
                                                                                                                             than the ground state will ultimately decay. Neverthe-
to single spin flips. In the light-gray region the ferromagnet
is the groundstate but skyrmions exist as metastable excita-
                                                                                                                             less, metastable skyrmions (light grey area in Fig. 4(b))
tions. In the dark-shaded region the system can minimize                                                                     exist which we define by two conditions: (i) a metastable
its energy by the proliferation of skyrmions and a skyrmion                                                                  skyrmion cannot decay by spin-conserving processes, i.e.,
lattice is expected to form. The black dashed line is deter-                                                                 by terms included in our Hamiltonian, and (ii) it cannot
mined from the condition that the skyrmion with the lowest                                                                   decay by an (incoherent) sequence of processes where a
energy reaches the largest number of spin flips, Nf = 9, in                                                                  single spin flips and the energy is lowered. The first
our simulation.                                                                                                              condition is independent of the external field B and is
                                                                                                                             fulfilled for skyrmions obeying the inequality (4); the
                                                                                                                             second condition requires that at least one of the sta-
bound states. First, a sufficiently large frustrating in-                                                                    ble skyrmions (according to the first condition) has a
teraction, J2 & 0.45, is required, which leads to a neg-                                                                     lower energy than the groundstate with one flipped spin
ative stiffness of the ferromagnet which changes sign for                                                                    less. The second condition compares the energy of states
J2 = 1/3. For fixed J2 , a small uniaxial anisotropy K is                                                                    with different magnetization and thus depends on B.
needed: it favours states where the down-spins stay to-                                                                      Roughly, our results are generally consistent with the
gether rather than fly apart. For too large an anisotropy,                                                                   phase diagram obtained for a classical model by Leonov
however, it is energetically favourable to form a single                                                                     and Mostovoy [23] (for a quantitative comparison with
down-spin domain instead of a skyrmion of well-defined                                                                       their phase diagram, K has to be multiplied by a fac-
                                                                                                                                    5

tor of 6 and B with a factor of 2); the only main differ-          obtain the following selection rule for the eigenvalues lz
ence seems to be that our metastability regime is smaller,         of Lz of skyrmions localized in space
which may be traced back to tunneling processes that do                   
not exist in the classical limit.                                            Nf − 1        mod 6 for skyrmions
                                                                     lz =                                             . (11)
  For a classical skyrmion (antiskyrmion), a clockwise                       −(Nf − 1)     mod 6 for antiskyrmions
rotation in space is accompanied by clockwise (anticlock-
                                                                   On the classical level, the locking of angular momentum
wise) rotation of spins, respectively. This suggests that
                                                                   and spin quantum number arises naturally as a skyrmion
the spin and angular momentum quantum numbers are
                                                                   is invariant under simultaneous, identical rotations of
not independent. For the following discussion it will be
                                                                   space and spin about the z axis, and is thus an eigen-
useful to translate the classical wave function into a quan-
                                                                   state of Lz + Sz , see Fig. 1. In contrast, one has to rotate
tum mechanical one. A quantum state of a skyrmion at
                                                                   space and spin in opposite directions to obtain the same
position R with helicity φ0 can be approximated by the
                                                                   configuration for an antiskyrmion, which is therefore an
spin-coherent state
                                                                   eigenstate of Lz − Sz . The unexpected shift by 1 in the
                      Y         z        y       z                 quantum number is related to the fact that a simulta-
        |σ, R, φ0 i ≈    e−iφi Si e−iθi Si eiφi Si |F M i (6)
                                                                   neous rotation does not affect the central spin, thereby
                          i
                                                                   rendering the relevant number of flipped spins equal to
with σ = ±1 for skyrmion and antiskyrmion, respec-                 Nf − 1 rather than Nf . We have checked this physical
tively. The angle φi = φs (ri − R) is defined in Eq. (2)           picture using a Schrödinger equation for the coordinate
and θi = θs (ri − R) characterizes the tilt of the spin.           R developed in section II B, from which, in the conclud-
This wave function is expected to become more and more             ing section, we will argue that this shift arises from the
accurate for larger and larger skyrmions as the magnetic           confinement of the skyrmion in the finite size system con-
texture can be locally approximated by a non-fluctuating           sidered here.
ferromagnet. As the wave function is not expected to be               Both skyrmions and antiskyrmions share the property
accurate on a quantitative level for small skyrmions, we           that the xy-component of spins located on opposite sites
will use it below only for qualitative arguments.                  of the skyrmion center are antiparallel. We hence cal-
   The operator which shifts φ0 is thePtotal spin minus            culate C⊥,i = −4hSix Sīx + Siy Sīy i, where Sī is the spin
                                             z   N                 located at position −ri opposite to the the location ri of
the spin of the ferromagnet ∆Sz =         i Si − 2 1 with
eigenvalues −Nf ,                                                  spin Si . Classically one finds that the maximal value of
                                                                   C⊥ = 1 is obtained for spins with vanishing Sz compo-
                e−iϕ∆Sz |σ, R, φ0 i = |σ, R, φ0 + ϕi,        (7)   nent. For the quantum skyrmions, we also obtain strong
                                                                   antiferromagnetic correlations, see Fig. 2. In Fig. 5 we
and an eigenstate of ∆Sz is obtained from                          plot the maximal anticorrelation, C⊥ = maxi C⊥i , for
                                                                   groundstate spin configurations with different angular
                       dϕ −iϕ(Nf +∆Sz )
                     Z
       |σ, R, Nf i ∝      e             |σ, R, 0i            (8)   momentum quantum numbers, lz , and number of flipped
                       2π                                          spins, Nf . Large anticorrelations are found whenever the
                                                                   selection rule given in (11) is obeyed, while the correla-
with ∆Sz |σ, R, Nf i = −Nf |σ, R, Nf i by construction.
                                                                   tions are much weaker when it is violated. This con-
  For the triangular lattice also a rotation of the position
                                                                   firms our analytical arguments: for a ‘proper’ quantum
of the atoms by the angle 2π  6 n is a symmetry transfor-          skyrmion spin and angular momentum quantum num-
mation,
                                                                   bers are locked by our selection rule. Changing the spin
           2π                                       2π             also changes the angular momentum. Whether the wave
    e−i 6 nLz |σ, R, φ0 i = |σ, R̂ 2π
                                    6 n
                                        R, φ0 − σ      ni,   (9)   function with the lowest energy (per flipped spin) obeys
                                                     6
                                                                   the selection rule or not depends on parameters as shown
where R̂ 2π   is the 2 × 2 matrix rotating the 2d skyrmion         in Fig. 4. If the selection rule is not obeyed, the ground-
          6 n
coordinate. Applying this to the state (8) we can com-             state can be viewed as a ‘doped’ skyrmion, wherein an
pensate the shift of φ0 by a rotation of the spins and             extra spin has been added or removed. The fact that the
find                                                               quantum skyrmions do not always obey simple ground-
                                                                   state selection rules should not be too surprising from the
      2π                         2π
  e−i 6 nLz |σ, R, Nf i = e−i 6 nσNf |σ, R̂ 2π
                                             6 n
                                                 R, Nf i. (10)     point of view that also for atoms or nuclei simple rules
                                                                   determining ground-state quantum numbers often fail.
To compare to our numerical result, we consider a situ-               We have also calculated a parameter related to the
ation where the skyrmion is localized close to the origin          winding number of the skyrmion [31],
R ≈ 0 (this part of the analysis will have to be modified                                h                                    i
                                                                                      −1            8hSi ·(Sj ×Sk )i
when we consider below skyrmions without a confining
                                                                             P
                                                                               4 tan       1+4(hSi ·Sj i+hSi ·Sk i+hSj ·Sk i)
flake). As for R = 0 the phase of the wave function (6)               W =                                                       , (12)
                                                                                                  2π
is ill-defined, we consider the limit R → 0, where the
                                                  2π
rotation of R leads to an extra phase factor e−iσ 6 aris-          where the sum is evaluated over a triangulation of the
ing from the central spin. Taking this into account, we            lattice (i, j, k being the sites in a triangle ∆ in the tri-
                                                                                                                                                         6

(a)                                                                                       two variables, the position R and the helicity φ0 of the
      0.8                                                                                 skyrmion, the low-energy Hilbert space will be spanned
                                                                                          by these two variables and the corresponding conjugate
                                                                            Nf = 4
      0.6                                                                                 momenta, P and Sz . Our goal is to discuss a phe-
                                                                            Nf = 5
                                                                                          nomenological Hamiltonian Hs valid at energies well be-
 C




      0.4                                                                   Nf = 6
                                                                                          low the spin gap of the bulk phase and below the energy
                                                                            Nf = 7
      0.8                                         0.8
                                                                                          of possible high-energy excitation of the skyrmion. For
      0.2                                                                   Nf = 8
                                                                                          a skyrmion with a radius much larger than the lattice
                                                                            Nff =
                                                                            N   =94       constant, effects of  Nf =the
                                                                                                                      4 underlying lattice potential are
      0.6
      0.0                                         0.6
                                                                            Nf = 5        exponentially smallf and
                                                                                                                N   = 5   will be ignored in this section
            0        1              2        3              4       5
 C




                                             C
      0.4                                         0.4                       Nf = 6        (but are discussed briefly
                                                                                                                N f = 6    in subsection II B and in more
                                        lz
                                                                            Nf = 7        detail in AppendixNA).  f = 7 Using the fact that the skyrmion is
(b) 0.6
    0.2                                           0.2                       Nf = 8        a large object, its dynamics
                                                                                                                Nf = 8       is expected to be governed by
      0.4                                                                   Nf = 9        small values of theNmomentum
                                                                                                                  f =9           P and small deviations of
      0.0                     0.8                 0.0                                     Sz from its ground state value. Hence, the effective low-
      0.2 0          1              2         3         0   4   1   5   2             3       4           5
                                                                                          energyNtheory
                                                                                                   f =4
                                                                                                             can be obtained from the first few terms
W




      0.0                     0.6       lz                                    lz          of a Taylor
                                                                                                  Nf = 5 series in the momentum and the deviation of
                         C




    -0.2                                                                                  Sz from
                              0.4                                                                 Nf =its
                                                                                                        6 ground-state value,
    -0.4                                                                                         Nf = 7
                                                                                                    (P − σz A(R))2
                                                                                                 f =8
                                                                                              HsN=                     1 + κ(Sz − Sz0 )
                                                                                                                                        
    -0.6                      0.2
                                                                                                Nf = 9    2M
            0        1              2         3             4       5
                              0.0                                                                      (Sz − Sz0 )2
                                    0   lz    1             2       3         4           5         +               − F Rx (1 − κ0 (Sz − Sz0 )).      (13)
                                                                                                           2Θ
                                               lz
FIG. 5. Maximal antiferromagnetic correlation C⊥ of the xy                                Here σz is ±1 for skyrmions and antiskyrmions, respec-
component of the spin (upper panel) and approximate wind-                                 tively, M is the effective mass [13, 18], F is an external
ing number W (lower panel) as function of angular momen-                                  force pointing in the x direction, κ and κ0 describe that
tum lz (J2 = 0.5, K = 0.05) for states with Nf = 4, 5, . . . , 9
                                                                                          the skyrmion mass and the effective force depend on the
flipped spins. Correlations are largest when the selection rule
Eq. (11) is obeyed. For Nf = 5, 6, 8, 9 also the winding num-
                                                                                          size of the skyrmion, and Θ parametrizes how the energy
ber W peaks at the expected value given by Eq. (11). For                                  depends on the deviation of Sz from the real number Sz0
Nf = 4, 7 instead, both skyrmion and antiskyrmion are in                                  (see Fig. 3). Experimentally, the force can, e.g., be real-
the lz = 0 sector and the ground state is a linear superpo-                               ized by a small gradient in the external magnetic field. In
                                                                                                          ∂Bz                         1
sition of skyrmion and antiskyrmion with vanishing winding                                this case, F = ∂R  x
                                                                                                               (Sz0 −N/2) and κ0 = N −S 0 . Forces can
                                                                                                                                    2   z
number.                                                                                   also arise, e.g., from the proximity to a sample bound-
                                                                                          ary. Finally, A(R) is an effective vector potential, arising
                                                                                          from the Berry phase of the spins which rotate when the
angulation) such that each triangle is oriented counter-
                                                                                          skyrmion moves. The classical and quantum equations of
clockwise. In the classical limit, W as defined above is
                                                                                          motion of a skyrmion are identical to those of a particle
quantized and obtains an integer value. For quantum
                                                                                          in a huge orbital magnetic field [12, 13, 16],
spins this will not be the case. In the lower panel of
Fig. 5 we show W as a function of lz for different values                                                                  4π
of Nf . For lz = 0, 3 the groundstate is a linear superpo-                                                    Bd = 4πns = √     ,                     (14)
sition of skyrmion and antiskyrmion and W vanishes by                                                                       3a2
symmetry. For the other values of lz we find again that
                                                                                          where ns is the spin density and the numerical value is
|W | is maximal when the selection rule (11) is obeyed,
                                                                                          given for a triangular lattice with lattice constant a. Its
confirming our interpretation of the bound-magnon state
                                                                                          strength corresponds exactly to one flux quantum per
as a skyrmion.
                                                                                          area of the unit cell (for a spin 1/2), i.e. about 400, 000 T
                                                                                          if the size of the unit cell is 1 Å2 . We will focus our
                                                                                          analysis only on the lowest Landau level as we expect
       II.       MOBILE QUANTUM SKYRMIONS
                                                                                          that the next Landau level has an energy larger than the
                                                                                          spin gap of the ferromagnet, implying that the effective
      A.        Interplay of motion and helicity rotation                                 Hamiltonian (13) is not valid for the second Landau level
                                                                                          [15, 16].
  We will now investigate the low-energy quantum dy-                                         The Hamiltonian (13) can easily be solved analytically
namics of a skyrmion first ignoring the possibility of                                    as Sz is conserved and the remaining Hamiltonian cor-
skyrmion-antiskyrmion tunneling, which will be the fo-                                    responds to the text-book Landau level problem. In the
cus of the next subsection.                                                               gauge where A = (0, −Bd x, 0), the momentum ky per-
  As the classical skyrmion solution is parametrized by                                   pendicular to the force is a good quantum number and
                                                                                                                                    7

the exact energies of the eigenstates are given by                   respectively. As in the classical case, the drift velocity vs
                                                                     of the quantum skyrmion in real space is perpendicular
                                            (Nf − Nf0 )2
                      
 ±          Bd       1                                               to the force and simply given by the ratio of external
EN f ,ky ,n
            =    n+        1 − κ(Nf − Nf0 ) +
            M        2                           2Θ                  force and magnetic field
    ky F (1 + κ (Nf − Nf )) F M (1 + κ (Nf − Nf0 ))2
               0         0       2          0
                                                                                 ∂ ±             F
  ∓                          −                          ,                vs =      E          = ∓ (1 + κ0 (Nf − Nf0 )).          (16)
               Bd               2Bd2 1 − κ(Nf − Nf0 )                           ∂ky Nf ,ky ,n    Bd
                                                  (15)
                                                                     It is opposite for skyrmions and antiskyrmions, which is
where n is the Landau level index, Nf parametrizes, as               perhaps the easiest way to distinguish them experimen-
above, the number of flipped spins, Nf0 = N/2 − Sz0 , and            tally in cases where a direct measurement of the spin
±1 describes the solution for a skyrmion or antiskyrmion,            configuration is not possible.




FIG. 6. Snapshots of the probability distribution, |ψ(φ0 , Ry )|2 , of the helicity φ0 and the y-coordinate of the quantum mechanical
wave function, for times t = 0, 20, 40, 150, 300, of an antiskyrmion driven by a magnetic field gradient (initial condition:
                    2          2   2                                                       √
ψ(Ry , φ0 ) ∼ e− sin (φ0 /2)/δφ e−Ry Bd /4 , with width δφ = π8 , M/Bd = 10, Θ = 20, F/ Bd = 0.025, κ = κ0 = 0.1, Nf0 = − B2M  d κΘ
                                                                                                                                    ).
For short times the angle φ0 grows linearly in time, but its wave function also spreads. For long times, the wave function splits
into distinct wave packets. This does not reflect an interference effect but arises because the velocity depends on the number
of flipped spins, Nf (see Eq. (16)). It therefore indicates a perfect entanglement of position and Nf . For a skyrmion the same
result is obtained with Ry → −Ry .

  A measurement of the helicity φ0 of the skyrmion (e.g.,            viously been observed that in classical models the he-
by an electron microscope which is sensitive to the in-              licity dynamics is coupled to the translational motion
plane orientation of spins [2]) will result in a collapse of         of skyrmions and antiskyrmions when skyrmion motion
the wave function to a state with fixed φ0 (within mea-              is induced by various forces, most notably spin-orbit
surement accuracy) described by a superposition of states            torques [24, 25, 28]. These dissipative forces are, how-
with different values of Nf . As −Nf is the conjugate mo-            ever, associated with extra channels of decoherence not
mentum to φ0 , one will subsequently observe a precession            captured in our effective model. A direct comparison can
                                                ∂    ±
of φ0 with the group velocity h∂t φ0 i ≈ − ∂N     f
                                                    ENf ,ky ,n
                                                               .     hence only be made to the dynamics induced by field gra-
Remarkably, the motion of the skyrmion induces an ad-                dients studied in Ref. [29], where, however, no detailed
ditional precession of the helicity and therefore of the in-         analysis has been given.
plane spins on top of the quantum mechanical precession                 We have checked that straightforward classical simu-
for F = 0,                                                           lations (not shown) of our model reproduce a precession
                                                                     of the helicity proportional to F 2 if a small field gra-
                                                    F 2M
    hφ̇0 i ≈ hφ̇0 iF =0 + κ0 F hRx i + (κ + 2κ0 )        ,   (17)    dient is applied. For J1 = 1, J2 = 0.5, K = 0.05,
                                                    2Bd2             and an average magnetic field chosen to describe about
                           k
                                                                     7 flipped spins we find both for skyrmions and anti-
where we used that ∓ Byd = hRx i for a wave function                                               2
in the lowest Landau level. More precisely, the result               skyrmions that Φ̇0 ≈ 6 J11a2 BFd , which is consistent
shown above holds only when the force is turned on adi-              with (2κ0 + κ)M ≈ 12 J1 /a2 (or M ∼ 30 J1 /a2 using that
abatically. Switching the force suddenly excites higher              κ0 = 1/Nf and assuming κ ∼ κ0 ). The simulation result
quantum numbers n (thus possibly leaving the range of                has been obtained using the standard Landau-Lifshitz-
applicability of our low-energy Hamiltonian).                        Gilbert equation in the limit of weak damping α, and we
  In several studies, e.g. [23–25, 27–29], it has pre-               find that Φ̇0 is approximately independent of α in the
                                                                                                                           8

long-time limit. Note, however, that the long-time and                B.   Skyrmion-Antiskyrmion tunneling
vanishing-damping limits do not necessarily commute. A
value of κ ∼ 1/Nf is also consistent with the assump-           We will now consider the consequences of skyrmion-
tion that the mass is proportional to Nfβ which implies       antiskyrmion tunneling. Using that 1/Θ in Eq. (13) is
κ = β/Nf (Ref. [13] obtains β = 2 from a classical calcu-     expected to be much larger than the exponentially small
lation). The parameter Θ can be obtained by a straight-       tunneling rate, we assume in the following that the mag-
forward fit to the Sz dependence of the skyrmion energies     netization of the skyrmion is fixed to its ground state
available to us from the exact diagonalization results. For   value. The effective Hamiltonian for the tunneling prob-
the parameters quoted above, we find Θ ≈ 20/J1 . The          lem is therefore given by
value of Θ has also been estimated previously for classical
                                                                      (P − σz A(R))2
models in Ref. [25, 32]. In our units their formulae trans-    Ht =                  + ∆†R σ + + ∆R σ − + V (R), (18)
late to Θ = 1/(3K) and Θ = 1/(6K), respectively, which                     2M
differs from our result. Nevertheless, this concludes our     where ∆R is an operator encoding the position depen-
estimation of all parameters of the effective model defined   dence of the tunneling amplitude (specified in more de-
in Eq. (13).                                                  tails below in Eq. (29)), σ ± = 12 (σx ± iσy ) are operators
                                                              which induce transitions from skyrmion to antiskyrmion
                                                              and back, and V (R) is the periodic potential generated
                                                              by the underlying lattice of the spins. Even in the ab-
                                                              sence of tunneling, such a periodic potential delocalizes
                                                              quantum particles in the lowest Landau level and leads to
   Beyond the classical effects, the quantum mechanical       a finite dispersion. V (R) is, however, exponentially small
model predicts new phenomena. First, due to the Heisen-       in Rs /a, the ratio of skyrmion radius and lattice constant
berg uncertainty relation a measurement of the helicity       [15]. For our skyrmions we show in Appendix A 2 that
with precision δφ0 leads to an uncertainty in the con-        V (R) is indeed tiny (∼ 10−4 J1 for one set of parameters)
jugate variable Nf − Nf0 and a subsequent quantum-            and much smaller than estimates of the tunneling rates.
mechanical spread of the wave function. This effect           We therefore set V (R) to zero in this section and discuss
rapidly washes out the precession of the helicity, see        effects of a finite V (R) only in Appendix A.
Fig. 6, where less than half of a 2π precession is ob-           It is tempting to use in Eq. (18) a vector potential,
served before the wave function covers all angles. To         e.g., of the form A = B2d R × ẑ with ∇ × A = Bd ẑ in
observe at least a full rotation of φ0 , the condition        combination with a constant ∆. While this choice of the
F 2 ΘM
   Bd2
       |κ + 2κ0 |δφ0 & 1 must be fulfilled. Using the pa-     vector potential is completely appropriate in the absence
rameters of Fig. 6, characteristic of a skyrmion of O(10)     of tunneling, it leads to unphysical results (a single local-
flipped spins, the required force would be very large, of     ized state at the origin of the coordinate system) in the
the order of 0.1 J1 /a (corresponding to a field gradient     presence of tunneling. To understand the problem it is
of 0.01 J1 /a). Such a large force cannot be realized by      useful to realize that the tunneling event can be viewed
a field gradient in a bulk sample (it can, however, arise     as a sudden sign change of the vector potential. Such
from confining forces at the edge of the sample). We con-     a sign change creates an unphysical electric field spike
clude that for small skyrmions consisting only of O(10)       E = Ḃ2d R × z growing linear in distance from the origin.
flipped spins, the quantum mechanical spread of the wave         It is thus imperative that we rederive more carefully
function is likely to dominate the drift of the angle ob-     the vector potential of the skyrmion. It originates from
tained classically. The second effect is that the position    the Berry phases of the underlying spin-1/2 system.
of the particle Ry gets entangled with the magnetization      Parametrizing each spin with a unit vector n̂i with angles
of the skyrmion. Similar to a Stern-Gerlach setup, where      θi and φi , the Berry phase action of the spins can con-
the trajectories of particles depend on Sz , the velocity     veniently be computed using a singular vector potential
of the skyrmion, Eq. (16), depends on the discrete vari-      as (n̂). We use a gauge choice where as = 1−cos     θ
                                                                                                             sin θ φ̂ with φ̂
able Nf , and consequently the wave function eventually       being the unit vector in φ direction (this gauge choice is
splits into separate wave packets distinguished by their      also compatible with the wave function (6)). Using that
local magnetization, see Fig. 6. This is also a purely        n̂i = n̂(ri − R), we obtain for the Berry phase action of
quantum mechanical effect arising from the quantization       the spin-1/2 system [33]
of the magnetization. As the magnetization for each of
                                                                         1                      d                     dR
                                                                           Z     XZ                   Z
these wavepackages is fixed, the conjugate variable, the
                                                                  SB =        dt       as (n̂i ) n̂i ≈ dt σz A(R)
helicity, shows maximal uncertainty. To observe the ef-                  2                      dt                    dt
                                                                                  i
fect, we require that δt∆v & a, where ∆v = κ0 BFd is                                                                    (19)
the velocity difference of two skyrmion states differing
by ∆Nf = ±1 and δt is the time scale on which the             with the vector potential
skyrmion propagates in a quantum coherent way. From
                                                                                          1X            dn̂i
this condition and the estimate κ0 ∼ 1/Nf , we obtain the                   σz Aα (R) =       as (n̂i )      .          (20)
                    N                                                                     2 i           dRα
requirement δt & F af .
                                                                                                                                9

A(R) is singular when the center of the skyrmion R                   |σ, R, Nf i in Eq. (6). Importantly, the angular momen-
where the spin points down is located exactly at the lo-             tum of the wave function is given by Eq. (11), where the
cation of a spin, R = ri , because we used a gauge choice            origin of the −1 term can be traced back to the singular
for which as is singular at θ = π. Our choice of the gauge           gauge transformation.
has the advantage that the vector potential of skyrmion                 The momentum eigenstates (without normalization)
and antisykrmion (σz = ±1) are opposite to each other.               are given by
When calculating A and the magnetic field correspond-                                         X
ing to A one has to take into account the singularity and                          ψ±,k (R) =    eikri ψ± (R − ri ).     (25)
one finds                                                                                          i

                                                                   This eigenstate is unique within the lowest Landau level
                Bd −Ry             X
                                                                     which contains exactly one state per flux quantum. Thus,
          A=                  −∇        φ(R − ri ),   (21)
                 2    Rx                                             for skyrmions and antiskyrmions, there is precisely one
                                     i
                     X                                               state per unit cell of the lattice, each. As the tunneling
          B = Bd −       2π δ 2 (R − ri ).            (22)
                                                                     matrix element is much smaller than any Landau level
                          i
                                                                     spacing, we can ignore Landau level mixing and compute
We obtain a constant uniform magnetic field Bd and for               the tunneling matrix elements projected onto the lowest
R = ri an extra contribution localized in δ functions and            Landau level directly,
carrying exactly one flux quantum per lattice      site. The
                                                                                            R ∗
                                                                                              ψ−,k ∆R ψ+,k d2 R
magnetic field integrated over a unit cell, U C B d2 r van-
                                            R
                                                                           δk =                                       1/2
ishes, as expected for a vector potential which is periodic
                                                                                  R ∗                R ∗
                                                                                     ψ+,k ψ+,k d2 R ψ−,k     ψ−,k d2 R
in space. Note that A is periodic, A(R + ri ) = A(R), as                         P 0 ikri
the linear term in R in the first term in Eq. (21) is exactly                         δ e
                                                                              = P i ri ikri                                 (26)
canceled by a similar contribution from the second term                             i ri e
                                                                                     α
(assuming that the lattice approximately has the shape                           R ∗                        R ∗
of a disc). We have checked this property numerically.               with αri = R ψ+   (R)ψ+ (R − ri ) = ψ−      (R)ψ− (R − ri )
In the absence of tunneling, one can gauge away the sin-             and δr0i = ψ−   ∗
                                                                                       (R)∆R ψ+ (R − ri ). The denominator
gular part of the magnetic field using a singular gauge              is needed as we used non-orthonormal wave functions.
transformation. In the presence of tunneling, however,               Within the lowest Landau level of skyrmions and anti-
such a gauge transformation will modify the tunneling                skyrmions, the Hamiltonian in momentum space is then
term in a singular way.                                              simply described by
    To obtain eigenstates and low-energy spectrum of the                                                0 δk∗
                                                                                                             
Hamiltonian (18), we first construct for ∆R = 0 eigen-                                 Hk = E0 1 +                          (27)
                                                                                                       δk 0
states of momentum k both for skyrmions and anti-
skyrmions. Starting from the well-known Landau lev-                  with eigenvalues
                                              Bd 2
els in
      a constant
                   magnetic field, ψ ∼ e− 4 r for A =                                        Ek = E0 ± |δk |.               (28)
Bd −Ry
               , we first perform a singular gauge trans-               The tunneling process is expected to be local and
  2     Rx
formation to obtain the corresponding eigenstate for the             also the overlaps αri decay rapidly with distance
                                                                                 −Bd kri k2    kri k2
vector potential (21),                                               (αri = e        4    eiπ a2 , and numerically equal to
                        1/2                                        1, −0.16, −0.004, 0.0007, −3 · 10−6 onsite and for nearest,
                    Bd            Bd   2     P                       next-nearest, third- and forth next neighbors). Note that
     ψ± (R) =                   e− 4 R e∓i   j φ(R−rj )   ,   (23)   P
                                                                           α   = 0  reflecting the fact that the wave function
                    2π                                                  ri  ri

                                                                     ψ±,k (R) carries angular momentum ±1 and therefore has
where the only difference between skyrmions and anti-                to vanish for k = 0.
skyrmions is the sign of the phase factors. As the vector               Tunneling is constrained by the crystalline symmetry
potential A is a periodic function of R, one can sim-                and the relative angular momentum of skyrmion and an-
ply translate the wave function by a lattice vector ri to            tiskyrmion encoded in the spin-wave function |σ, R, Nf i.
obtain another (in general not orthonormal) eigenstate               The difference of the angular momentum of the spin-part
localized around ri . An approximation for the corre-                of the wave function is 2Nf mod 6. As a phenomeno-
sponding many-body wave function localized around the                logical ansatz we expand the tunneling matrix element in
site ri is                                                           lattice harmonics, keeping the lowest-order term allowed
                     Z                                               by symmetry,
      |σ, ri , Nf i ∼ d2 R ψσ (R − ri ) |σ, R, Nf i. (24)                      
                                                                                1P
                                                                                                             for Nf = 0 mod 3
                                                                                     5     −i 4π  n    iG   R
                                                                       ∆R = δ        n=0 e           e        for Nf = 1 mod 3 ,
                                                                                                6         n

Note that in the many-body wave function the singu-                             P5
                                                                               
                                                                                           i 4π n   iG    R
                                                                                     n=0 e        e           for Nf = 2 mod 3
                                                                                              6         n
lar terms e−σiφ(R−ri −rj ) at lattice points ri + rj cancel
exactly with a singular contribution in the definition of                                                                     (29)
                                                                                                                                                                  10

          1.0                                            2                                                   0.0
                                Nf = 0 mod 3                                                                                       Nf = 2 mod 3
                                                                                              0.0
                            M                                        Nf = 1 mod 3                                           Nf = 2 mod 3
          0.5                                            1                                                 -0.5
                           K




                                                                                                   E k c /  2
                                                                                            -0.5
Ek / 




                                               Ek / 
          0.0                                            0                                                 -1.0




                                                                                    E k c /  2
                                                                                            -1.0
         -0.5                                           -1                                                 -1.5



                                                                                                                            
         -1.0                                           -2                                  -1.5           -2.0
                                                                                                                   M                    K       M
                M                   K     M                 M          K     M

                                                                                                                       
                                                                                            -2.0
                                                                                                    M                              K        M


                                                                                          FIG. 8. Bandstructure due to skyrmion-antiskyrmion tun-
                                                                                          neling for Nf = 2 mod 3 and δ = 0.1 ωc , where ωc is the
                                                                                          cyclotron frequency. In contrast to the case shown in Fig. 7,
FIG. 7. Bandstructure of skyrmions in a triangular lattice in-
                                                                                          the bandwidth is not linear in the tunneling rate δ but propor-
duced by skyrmion-antiskyrmion tunneling of strength δ. The
                                                                                          tional to δ 2 /ωc . The splitting of the two bands is proportional
bandstructure depends sensitively on the number of flipped
                                                                                          to δ 3 /ωc2 . The right panel shows the trajectory of a classical
spins Nf forming the skyrmion and antiskyrmion bound state.
                                                                                          particle in a magnetic field with random changes of the sign
For Nf = 0 mod 3 the band minimum is at the Γ point while
                                                                                          of the charge to mimic tunneling skyrmion-antiskyrmion tun-
Dirac points are located at the K points. For Nf = 1 mod 3
                                                                                          neling events.
the band minimum is located at the K point and a quadratic
band touching occurs at the Γ point. See Fig. 8 for Nf = 2
mod 3.
                                                                                          the limit k → 0, the k dependent tunneling is highly
                                                                                          singular,
where Gn are six reciprocal lattice vectors obtained by                                                                         (kx + iky )2
rotating the first one, G1 , by the angle 2π
                                           6 (n − 1). The
                                                                                                                       δk = δ                       for k → 0.   (30)
                                                                                                                                  kx2 + ky2
tunneling rate δ is expected to be exponentially small in
the skyrmion size. For Nf = 1 mod 3 we can obtain                                         This implies that the eigenfunction of the effective Hamil-
an estimate of the tunneling rate using the splitting of                                  tonian (27) obtains a Berry phase 2π when circling in mo-
the lowest two energy level within our exact diagonaliza-                                 mentum space around k = 0. This Berry phase cancels,
tion result. For Nf = 7, J2 = 0.5, K = 0.05 we find,                                      however, exactly, a corresponding singular Berry phase
for example, in the lz = 0 sector a sizeable tunneling                                    arising from the definition of the momentum eigenstates,
splitting ∆Et ≈ 0.05 J1 . Since this splitting arises from                                Eq. (25) and the resulting wave function and bandstruc-
tunneling of localized skyrmion and antiskyrmion, it is                                   ture are both smooth and non-singular for k → 0.
approximately equal to 2δ00 ≈ 3.1δ, from which we esti-                                     For Nf = 1 mod 3 the bandstructure is completely
mate δ = ∆Et /2δ00 ≈ 0.015 J1 . Note that this tunneling                                  changed. As shown in the right panel of Fig. 7, we ob-
rate is much larger than our estimate for the amplitude                                   tain a parabolic band-touching at the Γ point. This is a
of the periodic potential V0 ≈ 7 · 10−5 J1 derived in Ap-                                 direct consequence of the finite angular momentum of the
pendix A 2 for the same parameters.                                                       wave function. The quadratic band touching is thereby
   In Fig. 7 the resulting bandstructure is shown Nf = 0                                  associated with a Berry phase of 2π for an adiabatic path
mod 3 and Nf = 1 mod 3, while Fig. 8 displays the                                         around the Γ point. We find numerically that the band-
bandstructure for Nf = 2 mod 3. The qualitative dif-                                      minima are now located at the two K points. Thus,
ference between the three bandstructures can be traced                                    at low energies, the skyrmion obtains a new quantum
back to the angular momentum of skyrmions and anti-                                       number describing in which band-minimum the quantum
skyrmions.                                                                                skyrmion is located.
   The bandstructure for Nf = 0 mod 3 in the left panel                                     For Nf = 2 mod 3 we obtain numerically that the
of Fig. 7 is regular and non-singular. This is, perhaps,                                  tunneling from the lowest Landau level of the skyrmion
surprising as our analysis of localized skyrmions and an-                                 and the antiskyrmion is not possible, δk = 0. We have
tiskyrmions revealed that in this case skyrmion and an-                                   not been able to find an analytic argument proving this.
tiskyrmion are in different angular momentum channels                                     To calculate the band-structure in this case, we therefore
lz = ∓1 and the localized skyrmions do not tunnel into                                    have to consider Landau-level mixing induced by the tun-
each other. In contrast tunneling for k = 0 is possible and                               neling process. We have used a discretized version of the
non-singular. Apparently, the mobile skyrmions transfer                                   Hamiltonian (18) to calculate numerically the resulting
the angular momentum to the emergent magnetic field                                       bandstructure. As is shown in Fig. 8, the bandwidth is
when tunneling. Mathematically, we find that tunneling                                    proportional to the square of the (exponentially small)
is dominated by the nearest-neighbor tunneling matrix                                     tunneling rate δ in this case and thus much smaller than
element δr0i while local tunneling vanishes, δ00 = 0. In                                  for Nf = 0, 1 mod 3 where a dispersion linear in δ was
                                                                                                                       11

obtained. The energy splitting of the two bands is even        a skyrmion, see Figs. 7 and 8. When the number of
smaller, of order δ 3 . Due to the finite angular momen-       flipped spins Nf is 0 or 1 mod 3, the bandwidth is pro-
tum we obtain again a quadratic band touching at the           portional to the tunneling rate, while it is quadratic in
Γ point where also the minimum of the dispersion is lo-        the tunneling rate for Nf = 2 mod 3.
cated. As the effects of tunneling are strongly suppressed        It is interesting to consider the response of the quan-
in this case, one has to reconsider the effects of a tiny      tum skyrmion to an external force or a confining poten-
periodic potential V (R), which can also induce a finite       tial. For simplicity, we consider the simple case, where
bandwidth. We discuss this case in Appendix A and find         Nf is a multiple of 3, where the bandstructure has a
quantitative but no qualitative changes of the bandstruc-      unique minimum at the Γ point. A weak force, F  δ/a,
ture for Nf = 2 mod 3 .                                        therefore simply leads to an acceleration of the particle
  All results in this section have been derived under the      parallel to the external force and to Bloch oscillations.
assumption that the Hamiltonian (18) is valid. One as-         As the particle is a superposition of skyrmion and anti-
sumption which me made is that the tunneling ∆ is local        skyrmion states, the quantum skyrmion effectively car-
and just a function of the coordinate R but not of the         ries a topological charge 0 and does not see the emergent
momentum. While this is an ad-hoc assumption, we ex-           magnetic field. For large forces, F  δ/a, the picture
pect that all qualitative features of the bandstructure,       changes completely. In this case, tunneling is suppressed.
which rely purely on symmetry, will remain the same if         Skyrmion and antiskyrmion move with velocity ± BFd , see
more complicated tunneling terms are considered.               Eq. (16), perpendicular to the external force in oppo-
                                                               site directions. The crossover between the two regimes
                                                               is driven by the force-induced Zener tunneling between
      III.   CONCLUSIONS AND OUTLOOK                           the two states. Using the splitting of skyrmion and an-
                                                               tiskyrmion trajectories, one can use an external force to
   We have shown that a skyrmion in a frustrated magnet        implement Stern-Gerlach type of experiments using field
is a quantum particle with a list of rather unusual proper-    gradients. Close to a sample boundary, which will likely
ties. Most importantly, the motion of the skyrmion and         acts as a repulsive force for skyrmion and antiskyrmions,
the internal degrees of freedom are directly coupled. As       one can expect chiral edge channels for skyrmions and
was already known from the classical theory, the helicity      antiskyrmions running in opposite directions and its an
couples to the motion of the skyrmion which leads to a         interesting open problem how these edge states merge
characteristic precession of the spin when the skyrmion        with the bulk bands and how this affects the scattering
is moving in the presence of an external force. For small      of quantum skyrmions from sample boundaries. Simi-
skyrmions this effect is difficult to observe due to a com-    larly, in a weak confining potential, the ground state is
bination of Heisenberg’s uncertainty principle and the         unique with vanishing angular momentum, while a strong
quantum mechanical spread of the (helicity-) wave func-        confining potential, such that V0 a2  δ, leads to the dou-
tion. Furthermore, position and spin become strongly           bly degenerate groundstate with angular momentum ±1,
entangled during time evolution which leads to a char-         as observed for the exact diagonalization of small finite
acteristic quantization of the skyrmion velocity in the        systems.
presence of a force.                                              Our study has focused on single skyrmions – the next
   The helicity and simultaneously the position of a mov-      step is to consider pairs of skyrmions and their mutual
ing skyrmion can be measured using, e.g., an electron          interactions. The interaction potential has an oscillat-
microscope [2]. It would, for example, be interesting to       ing sign [24] as the magnons in the ferromagnetic state
study how the quantum mechanical spread of the helicity        have a minimum at finite momentum. This will lead to
and the entanglement of spin and position is affected by       the formation of boundstate and, for a finite skyrmion
the presence of thermal magnons or by continuous weak          density, to crystalline phases.
measurements due to the electron microscope itself.
   In the absence of an external force and of tunneling,
a skyrmion is localized in the lowest Landau level. In
this case skyrmion-antiskyrmion tunneling can delocal-
                                                                              ACKNOWLEDGMENTS
ize the particle. A semiclassical explanation of this effect
is shown in the right panel of Fig. 8: During a tunnel-
ing event the effective charge of the skyrmion changes,          We acknowledge useful discussions with L. Heinen, S.
allowing for skyrmion motion not confined by cyclotron         C. Morampudi, and A. Vishwanath. A.R. wants to thank
orbits. The corresponding bandwidth is thereby natu-           the Department of Physics at Harvard University for
rally set by the tunneling rate. The internal angular          hospitality. This work was supported by the Deutsche
momentum of skyrmion and antiskyrmion imposes, how-            Forschungsgemeinschaft (DFG, German Research Foun-
ever, strong constraints on possible tunneling events. As      dation) - Projektnummer 277146847 - CRC 1238 (project
for skyrmions, spin and angular momentum are locked to         C04, A.R., J.M., and V.L.), Projektnummer 277101999
each other. This implies that the bandstructure changes        - TRR 183 (project B01, C. H.) and the MIT-Harvard
drastically when a single spin is added or removed from        Center for Ultracold Atoms (CUA).
                                                                                                                                                                           12

    Appendix A: Effect of lattice potential on the                          5                                                             5
                  bandstructure

                                                                            0                                                             0
   The discrete atomic lattice breaks the continuous




                                                                 Ek / δ




                                                                                                                               Ek / δ
translational symmetry and thereby induces a periodic
                                                                          -5                                                            -5
potential V (R) for the skyrmion position R. Such a peri-
odic potential is potentially important as in the presence                                                  Nf = 0 mod 3                                         Nf = 1 mod 3
of both magnetic field and periodic potential, Landau                     -10                                                           -10
bands are not completely flat but obtain a dispersion. In                       M                       Γ            K     M                  M            Γ           K        M
order to estimate the impact of this effect, we derive an                                                   V0/δ = 0       V0/δ = 2               V0/δ = 20
approximation for V (R) and include it in our bandstruc-
ture calculation.
                                                                 FIG. 9. Bandstructure for Nf = 0 mod 3 (left panel) and
   The atomic triangular lattice or our model (see Fig. 2)
                                                                 for Nf = 1 mod 3 (right panel) for V0 /δ = 0, 2 and 20, where
is characterized by the lattice constant a. A skyrmion is        V0 is the strength of the periodic potential and δ the skyrmion-
a smooth texture with radius Rs  a. It effectively av-          antiskyrmion tunneling rate. In our model system, we esti-
erages over many lattice sites and consequently Fourier          mate that V0  δ.
components of the resulting periodic potential are expo-
nentially small in |qi |Rs [15, 16], where qi are the recipro-
cal lattice vectors. Ergo, the periodic lattice potential of
                                                                                                    0
the skyrmion is with exponential precision described by
only the six shortest reciprocal lattice vectors. Its shape




                                                                                    E k ωc / δ 2
                                                                                                   -2                                                 V0ωc /δ 2 = 0
is completely fixed by symmetry,
                                                                                                                                                      V0ωc /δ 2 = 2
              6                                                                                    -4
                                                                                                                                                      V0ωc /δ 2 = 10
              X
 V (R) = V0         ei qj ·R
              j=1                                                                                  -6                    Nf = 2 mod 3
                                           
                    2πRx       2πRy         4πRy                                                        M        Γ             K          M
         = V0 2 cos        cos √      + cos √       .
                      a          3a           3a
                                                 (A1)
                                                                 FIG. 10. Bandstructure for different values of V0 ωc /δ 2 for
The prefactor V0 is the only free parameter, expected to         Nf = 2 mod 3. In this case Ek /δ 2 is just a function of
                                                                 V0 ωc /δ 2 . Qualitatively, the shape of the bandstructure does
be exponentially small in Rs /a.
                                                                 not change significantly upon increasing V0 ωc /δ 2 ; the quanti-
  The periodic lattice potential V (R) has to be added           tative changes can be significant, though. For high V0 ωc /δ 2 ,
to to our phenomenlogical Hamiltonian,                           the bandstructure becomes independent of Nf .
         (P − σz A(R))2
 Ht =                      + V (R) σ0 + ∆†R σ + + ∆R σ − ,
                2M
                                                       (A2)      our model, see below) the effect of the periodic potential
where σ0 is the 2×2 identity matrix. In the following, we        can be neglected, small corrections linear in V0 /δ do not
will first discuss how a finite V0 affects the bandstructure     change any qualitative features of the bandstructure. For
of the quantum skyrmions both for small and large values         V0  δ the dispersion is mainly determined by the peri-
of V0 , then we will show that V0 is very tiny for the           odic potential. The splitting of the two bands, however,
quantum skyrmions discussed in our paper.                        is governed by the skyrmion-antiskyrmion tunneling. For
                                                                 Nf = 0 mod 3 the minimum of the bands is always at
                                                                 the Γ point, while for Nf = 1 mod 3 it moves from the
    1.    Effect on the bandstructure for arbitrary              K points towards the Γ point.
                    potential strength                              For Nf = 2 mod 3, see Fig. 10, the dispersion in the
                                                                 absence of a periodic potential is not proportional to δ
   The bandstructure of quantum skyrmions described by           but to δ 2 /ωc , instead, see also Fig. 8. The lattice po-
Eq. (A2))can be obtained from a straightforward exact            tential is expected to create a first order perturbative
diagonalization of a discretized version of the Hamilto-         correction proportional to V0 but not lift the skyrmion-
nian. Our discussion will focus on the case V0 > 0, the          antiskyrmion degeneracy. For a combination of weak tun-
sign obtained in subsection A 2.                                 neling and lattice potential, therefore, the bandstructure
   In Fig. 9 we show the resulting bandstructure for             Ek ωc /δ 2 is expected to be a function of V0 ωc /δ 2 . The nu-
Nf = 0, 1 mod 3 and three values of V0 /δ, where δ is            merical results for the bandstructure are shown in Fig. 10
the skyrmion-antiskyrmion tunneling rate δ defined in            for various values of V0 ωc /δ 2 . The effect of the lattice po-
Eq. 29. For small δ and V0 , the dispersion in units             tential V (R) is less pronounced in the qualitative sense,
of the tunneling rate, Ek /δ, depends only on the ratio          although, there can be significant quantitative changes
V0 /δ. As expected, for V0  δ (the relevant limit within        when V0 is varied for a fixed δ.
                                                                                                                           13

2.   Classical approximation for the lattice potential           obtain from the energy difference between the skyrmion
                                                                 centered on a bond and a plaquette V0 = 8.15 · 10−5 and
                                                                 for centered on a site and a plaquette V0 = 7.90 · 10−5 .
   In order to estimate the prefactor V0 of the lattice po-      The good agreement between the two estimates with a
tential we can employ a classical approximation of the           precision of 3% shows that Eq. (A1) is well justified. By
magnetization by replacing the quantum mechanical spin           performing atomistic simulations with a small applied
operators S in the Hamiltonian, Eq. (1), with classical          electric current, we could furthermore drive the skyrmion
Heisenberg spins m with kmk = 1/2. We can exploit                to other intermediate positions and evaluate its energy
that the skyrmion position is fixed by symmetry if it is         which is in excellent agreement with the simple ansatz in
initialized on a highly symmetric point. Thus we use             Eq. (A1).
standard relaxation algorithms without artificially fixing          ∆mz varies slightly as function of position within the
any spins to calculate the energy of a skyrmion which is         classical approximation while it is integer valued and con-
centered (i) on a lattice site, (ii) on a plaquette, and (iii)   served in the quantum theory. We therefore performed
on a bond between lattice sites, respectively. Although          a second calculation, where we adjusted the external
we only require the energies of two positions for fitting        magnetic field for each position of the skyrmion such
V0 , we can use the third position to validate the simplified    that ∆mz = 7 is fixed. This yields V0 = 7.20 · 10−5
ansatz for the potential, Eq. (A1).                              (V0 = 7.41 · 10−5 ) when comparing bond- and plaquette
   The skyrmion that we consider in Sec. II B is stabi-          centered skyrmions (from the difference of site-centered
lized for J1 = 1, J2 = 0.5, K = 0.05, a = 1, and 7               and plaquette-centered skyrmions). Both numbers agree
flipped spins. In the classical system, we have to tune          up to an error of 3% and do not differ significantly from
the external magnetic field such that the latter condition       the results obtained for constant magnetic field.
is fulfilled. Hence, we choose it such that the skyrmion            As we estimate from the exact diagonalization result
centered on a lattice site has a difference in the total mag-    that the tunneling rate for the same set of parameters
netization of ∆mz = 7 with respect to a fully polarized          is 0.015, our results indicate that the potential is much
state. Keeping the magnetic field fixed to this value, we        smaller than the tunneling rate, V0  δ.




 [1] S. Mühlbauer, B. Binz, F. Jonietz, C. Pfleiderer,               Rev. B 90, 174434 (2014).
     A. Rosch, A. Neubauer, R. Georgii, and P. Böni, Sci-       [14] O. M. Sotnikov, V. V. Mazurenko, J. Colbois, F. Mila,
     ence 323, 915 (2009).                                            M. I. Katsnelson, and E. A. Stepanov, arXiv e-prints
 [2] X. Yu, Y. Onose, N. Kanazawa, J. H. Park, J. H. Han,             , arXiv:1811.10823 (2018), arXiv:1811.10823 [cond-
     Y. Matsui, N. Nagaosa, and Y. Tokura, Nature 465, 901            mat.str-el].
     (2010).                                                     [15] R. Takashima, H. Ishizuka, and L. Balents, Phys. Rev.
 [3] S. Heinze, K. von Bergmann, M. Menzel, J. Brede, A. Ku-          B 94, 134415 (2016).
     betzka, R. Wiesendanger, G. Bihlmayer, and S. Blügel,      [16] H. Ochoa and Y. Tserkovnyak, ArXiv e-prints (2018),
     Nature Physics 7, 713 (2011).                                    arXiv:1807.02203 [cond-mat.mes-hall].
 [4] S. Seki, X. Z. Yu, S. Ishiwata, and Y. Tokura, Science      [17] S.-Z. Lin and L. N. Bulaevskii, Phys. Rev. B 88, 060404
     336, 198 (2012).                                                 (2013).
 [5] N. Nagaosa and Y. Tokura, Nat. Nanotech. 8, 899 (2013).     [18] C. Psaroudaki, S. Hoffman, J. Klinovaja, and D. Loss,
 [6] S. Woo, K. Litzius, B. Krüger, M.-Y. Im,                        Phys. Rev. X 7, 041045 (2017).
     L. Caretta, K. Richter, M. Mann, A. Krone, R. M.            [19] A. Derras-Chouk, E. M. Chudnovsky,           and D. A.
     Reeve, M. Weigand, et al., Nat. Mater.            (2016),        Garanin, Phys. Rev. B 98, 024423 (2018).
     10.1038/nmat4593.                                           [20] S. A. Diaz and D. P. Arovas, ArXiv e-prints (2016),
 [7] F. Jonietz, S. Mühlbauer, C. Pfleiderer, A. Neubauer,           arXiv:1604.04010 [cond-mat.str-el].
     W. Münzer, A. Bauer, T. Adams, R. Georgii, P. Böni,       [21] B. Ivanov, V. Stephanovich, and A. Zhmudskii, Journal
     R. Duine, et al., Science 330, 1648 (2010).                      of Magnetism and Magnetic Materials 88, 116 (1990).
 [8] T. Schulz, R. Ritz, A. Bauer, M. Halder, M. Wagner,         [22] T. Okubo, S. Chung, and H. Kawamura, Phys. Rev.
     C. Franz, C. Pfleiderer, K. Everschor, M. Garst, and             Lett. 108, 017206 (2012).
     A. Rosch, Nature Physics 8, 301 EP (2012).                  [23] A. O. Leonov and M. Mostovoy, Nature Communications
 [9] W. Jiang, G. Chen, K. Liu, J. Zang, S. G. t. Velthuis,           6, 8275 (2015).
     and A. Hoffmann, 704, 1 (2017).                             [24] S.-Z. Lin and S. Hayami, Phys. Rev. B 93, 064430 (2016).
[10] M. Mochizuki, X. Z. Yu, S. Seki, N. Kanazawa,               [25] X. Zhang, J. Xia, Y. Zhou, X. Liu, H. Zhang, and
     W. Koshibae, J. Zang, M. Mostovoy, Y. Tokura, and                M. Ezawa, Nature Communications 8, 1717 (2017).
     N. Nagaosa, Nature Materials 13, 241 EP (2014).             [26] J. Xia, X. Zhang, M. Ezawa, Z. Hou, W. Wang, X. Liu,
[11] K. Everschor-Sitte, J. Masell, R. M. Reeve,          and         and Y. Zhou, arXiv e-prints , arXiv:1812.00520 (2018),
     M. Kläui, Journal of Applied Physics 124, 240901 (2018),        arXiv:1812.00520 [cond-mat.mes-hall].
     https://doi.org/10.1063/1.5048972.                          [27] S. A. Dı́az and R. E. Troncoso, Journal of Physics: Con-
[12] A. Thiele, Phys. Rev. Lett. 30, 230 (1973).                      densed Matter, 28, 426005 (2016).
[13] C. Schütte, J. Iwasaki, A. Rosch, and N. Nagaosa, Phys.    [28] U. Ritzmann, S. von Malottki, J.-V. Kim, S. Heinze,
                                                                                                                            14

     J. Sinova, and B. Dupé, Nature Electronics 1, 451 (2018).   [31] A. V. Oosterom and J. Strackee, IEEE Transactions on
[29] J. J. Liang, J. H. Yu, J. Chen, M. H. Qin, M. Zeng, X. B.         Biomedical Engineering, IEEE Transactions on Biomed-
     Lu, X. S. Gao, and J.-M. Liu, New Journal of Physics              ical Engineering BME-30, 125 (Feb. 1983).
     20, 053037 (2018).                                           [32] A. O. Leonov and M. Mostovoy, Nature Communications
[30] T. Kurumaji, T. Nakajima,              M. Hirschberger,           8, 14394 (2017).
     A. Kikkawa, Y. Yamasaki, H. Sagayama, H. Nakao,              [33] A. Altland and B. D. Simons, Condensed matter field the-
     Y. Taguchi, T.-h. Arima, and Y. Tokura, ArXiv e-prints            ory, 2nd ed. (Cambridge Univ. Press, Cambridge, 2012).
     (2018), arXiv:1805.10719 [cond-mat.str-el].

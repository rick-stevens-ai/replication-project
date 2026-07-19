<!-- extracted via pdftotext | arxiv:1701.07256 | 2026-07-19T04:40:35Z -->
Skyrmion-Antiskyrmion pair creation by in-plane currents
Martin Stier,1 Wolfgang Häusler,1, 2 Thore Posske,1 Gregor Gurski,1 and Michael Thorwart1

arXiv:1701.07256v3 [cond-mat.mes-hall] 12 Apr 2017

1

I. Institut für Theoretische Physik, Universität Hamburg, Jungiusstraße 9, 20355 Hamburg, Germany
2
Institut für Physik, Universität Augsburg, 86135 Augsburg, Germany

Magnetic skyrmions can be considered as topologically protected localized vortex-like spin textures. Due
to their stability, their small size, and the possibility to move them by low electric currents they are promising
candidates for spintronic devices. Without violating topological protection, it is possible to create skyrmionantiskyrmion pairs, as long as the total charge remains unchanged. We derive a skyrmion equation of motion
which reveals how spin-polarized charge currents create skyrmion-antiskyrmion pairs. It allows to identify
general prerequisites for the pair creation process. We corroborate these general principles by numerical simulations. On a lattice, where topological protection becomes imperfect, the antiskyrmion partner of the pairs is
annihilated and only the skyrmion survives. This eventually changes the total skyrmion number and yields a
new way of creating and controlling skyrmions.

Magnetic skyrmions (Sks) are vortex-like localized magnetization configurations [1, 2] which have been predicted [3]
before they were discovered experimentally [4–7] in magnetic
layers with a strong spin-orbit interaction [8–10]. Despite
their potentially small size [11, 12], their thermodynamic stability is considerably strong [5, 7, 13]. This is a consequence
of the particular magnetic configuration which can be characterized by a total topological charge or Sk number Q. It can
take integer values only and therefore cannot be changed continuously [14, 15]. This feature protects magnetic Sks against
typical drawbacks of solid state systems such as disorder or
imperfect fabrication [8, 9, 16]. Together with the property of
easy repositioning by rather tiny in-plane electrical currents
[17–21], this makes single Sks attractive candidates for future
racetrack memory devices [17, 22–26]. Creation of Sks has
been reported in the vicinity of notches [18], by circular currents [27], by geometrical constraints [28] or by sweeping the
external magnetic field [29]. Controlled creation and annihilation of individual Sks has been demonstrated [30]. Each of
these processes has to overcome topological protection and
the precise mechanism of each way of Sk creation has to be
determined.
In this work, we derive a Sk equation of motion which
reveals the details of the process how total the topological
charge Q changes by an applied in-plane current. We find
this to happen in two steps. First, a skyrmion-antiskyrmion
(Sk-ASk) pair is created [29] from small spatial fluctuations
of the magnetization. Pair creation does not change the total
topological charge Q, since the Sk and the ASk have equal
topological charge of opposite sign, respectively. By the externally applied current the Sk and ASk get spatially further
separated. The Sk equation of motion reveals the relevant
terms at work which are not captured by the common Thiele
approximation [31, 32]. Finally, the ASk, being no stable solution for a given Zeeman field and a Dzyaloshinsky-Moriya
interaction, decays due to Gilbert damping. It is this second
step, which is ultimately responsible for changing Q, crucially
relying on dissipation. All general findings are confirmed by
extended numerical simulations.
Recently, Sk-ASk pair creation by in-plane currents in systems without Dzyaloshinsky-Moriya interaction has also been

reported and investigated numerically [33]. Additionally, Sk
creation by in-plane currents also has been observed in experiment [34].
The two-dimensional magnetization configuration
M(x, y, t) of a single current-driven Sk evolves in time
according to the extended Landau-Lifshitz-Gilbert (LLG)
equation [35–38]
∂t n = − n × Beff + αn × ∂t n

(1)

+ (v s · ∇)n − βn × (v s · ∇)n
where n = M/|M| is a normalized vector field. All interactions of the Hamiltonian H describing the system are contained in the effective field Beff = −∂H/∂n. Below, in Eq. (8),
we specify the Hamiltonian for a lattice model, but its detailed
form is not relevant for the following consideration. Beff already contains the gyromagnetic ratio and we set ~ = 1. Further important parameters are the Gilbert damping constant α
and the non-adiabaticity parameter β. In this work, we focus
specifically on the impact of spin-polarized electric currents
v s = pa3 jc /(2e) [39] flowing in the magnetic plane with spin
polarization p and lattice constant a, proportional to a charge
current density jc . With the vector field n(x, y, t), we then define the topological charge density
q(x, y, t) = n · [(v̂ · ∇)n × (v̂⊥ · ∇)n] ,
and the total topological charge
Z
1
d2 r q(x, y, t) ,
Q = Q(t) =
4π

Q∈Z.

(2)

(3)

In fact, this homotopy invariant completely determines the
topological properties of Sks even though it does not specify, e.g, the vorticity of a Sk (ASk) without further definitions
[14, 15, 40]. In our work, however, the magnetic background
will be fixed in such a way that Q > 0 (Q < 0) refers to
skyrmions (antiskyrmions) [41]. For convenience, we take
the direction of the spin current v s as reference direction,
v̂ = v s /|v s| and v̂⊥ = ẑ × v̂. While the topological invariant
Q is conserved in time at low energies, the time evolution of
q(x, y, t) describes the current-induced local motion of Sks. In

2
particular, as discussed below, it also describes the generation
or annihilation of Sk-ASk pairs.
To reveal the Sk-ASk pair creation mechanism, we decompose the effective field according to
Beff = b∥ n + b⊥1 (v s · ∇)n + b⊥2 n × (v s · ∇)n .

(4)

By combining Eqs. (1), (2) and (4), we readily obtain the Sk
equation of motion


(2)
∂t q = −∇ · j(1)
+
j
(5)
Sk
Sk ,
with the Sk currents
j(1)
Sk = − j1 qv s ,
n
(2)
jSk = j2 [(v̂ · ∇)n · (v̂⊥ · ∇)n]v s
o
− [(v̂ · ∇)n]2 v⊥ ,

(6a)
(6b)
(6c)

with contributions parallel to the current flow (∝ v s ) and perpendicular to it (∝ v⊥ ≡ ẑ × v s ). The coefficients read
j1 =[1 + αβ + αb⊥1 + b⊥2 ]/(1 + α2 ) ,
2

j2 =[α − β − b⊥1 + αb⊥2 ]/(1 + α ) .

(7a)
(7b)

The Sk equation of motion (5) resembles a continuity equation
[42] which connects the topological charge density q with the
Sk current density. We note, however, that conservation of Q
in Eq. (3) in the present case is not a consequence of Noether’s
theorem, albeit conserved quantities may still exist for Eq. (5)
[43] under continuous variation of n [26].
(2)
The physical meaning of j(1)
Sk and jSk becomes apparent
when we consider Sks in the steady state where ∂t n = 0 and
thus ∂t q = 0. For not too large current densities, no major
structural changes of the magnetization occur and Beff remains
parallel to n. Then, the perpendicular components b⊥1 = b⊥2
vanish and the coefficients j1 and j2 in Eq. (7) are constant. A
case of special importance occurs when α = β, which implies that j1 = 1, j2 = 0. Then, j(2)
Sk = 0, such that the
undistorted topological charge density q moves with the velocity −v s , according to Eq. (6a). This motivates us to call
j(1)
Sk a Sk current density. When α , β (but still assuming
b⊥1 = b⊥2 = 0), j2 becomes nonzero. Then, we may rewrite
Eqs. (6b,6c) in the form j(2)
Sk = − j2 q(η∥ v s +η⊥ v⊥ ), with the coefficients η∥ = (v̂·∇)n·(v̂⊥ ·∇)n/q and η⊥ = −[(v̂·∇)n]2 /q. We
can simplify η∥ = cot γ, where γ is the angle between (v̂ · ∇)n
and (v̂⊥ · ∇)n. This term ∝ η∥ only adds to the contribution
of j(1)
Sk (though with a dependence on the shape of the vector
field n) to drive positive and negative topological charge density along ±v s depending on the explicit angle γ.
Crucial for the following is the term ∝ η⊥ . First, it points perpendicularly to the externally applied spin current and, second, it drives negative and positive topological charge densities in opposite directions, as it changes sign under the inversion q → −q. This is essentially the Sk Hall effect [14, 26, 44–
47], but for arbitrary topological charge density. We therefore

identify the contribution (6c) as being responsible for separating negative from positive topological charge density resulting in a common Sk-ASk pair. The separation takes place
perpendicularly to the external current. Actually, this process
can be expected to be a common scenario in real materials
for sufficiently strong applied charge current densities. The
only further prerequisites are α − β , 0 and small spatial fluctuations of the Sk density q(x, y, t), which also imply finite
gradients (v̂ · ∇)n and (v̂⊥ · ∇)n and thus a finite j(2)
Sk . A finite gradient (v̂⊥ · ∇)n is, strictly speaking, not necessary for
a non-vanishing current j(2)
Sk [cf. Eq. (6c)]. Nevertheless, it is
important for a finite divergence ∇ · j(2)
Sk , 0. Only in this case,
the skyrmion current cannot be gauged away and is physically
relevant. Then, regions of opposite signs appear quite naturally in the topologically trivial state Q = 0, as regions of
finite q, which we have postulated, have to cancel each other
to sum up to zero. Ultimately, a Sk-ASk pair is formed out of
these fluctuations. We note in passing that the detailed motion
of ASks is typically more complicated than that of Sks, since
commonly, an isolated ASk is not a stationary solution and
thus, already for v s = 0, Beff is clearly not parallel to n, which
implies that b⊥ , 0.
In the following, we illustrate these general principles for a
concrete model realized by the Hamiltonian [19]
X
 X

Br · nr
(8)
H =−J
nr · nr+ex + nr+ey −
−D

r
X
h
r

r

 i

nr × nr+ex · e x + nr × nr+ey · ey


defined on lattice sites r (unit lattice constant) in two dimensions. It supports Sks in a certain parameter regime of
the phase diagram. J is the exchange interaction and D the
Dzyaloshinsky-Moriya interaction (DMI) strength. We use
the values J = 1meV, D/J = 0.18 reported for MnSi [19].
Here, we only discuss a bulk DMI which stabilizes Bloch
Sks. Yet, we have also verified our findings for systems
with an interfacial DMI which stabilizes Néel Sks [48, 49].
No qualitative modifications occur and our findings apply to
both kinds of Sks. In the numerical simulations, we use a
L x × Ly = 160 × 160 square lattice with periodic boundary conditions. For convenience, we translate v s = pa3 Ic /2e
into a charge current density Ic by assuming full polarization p = 1 and a lattice constant a = 0.5nm. Depending
on the magnitude of the externally controlled Zeeman field
B, either a helical phase, a Sk lattice or the ferromagnetic
(field polarized) phase is the ground state [19, 29]. A field
B = (0, 0, Bz) = −0.03 J ẑ is in fact strong enough to align
all magnetic moments, n(x, y, t) ≡ −ẑ. Then, q(x, y, t) remains
zero everywhere and, according to Eqs. (5) and (6), for all
times, since j(1,2)
Sk = 0, even at non-zero applied current densities.
To realize at least a small initial non-zero topological
charge density q, we add a tiny modulation to the magnetic
field pointing in the y-direction, i.e., By = b0 [sin(2πx/L x ) +
sin(2πy/Ly)] and b0 = Bz /100. As a matter of fact, the precise

3

FIG. 1. (Color online). Snapshots of the topological charge density q (insets) in the relevant 80 × 80 section of the total lattice and the magnetic
texture (arrows) in a magnified section (marked by the dashed rectangles within the insets) at the times as indicated. The initial topological
charge adopted by the applied inhomogeneous magnetic field is tiny (see q for t = 0 which is multiplied by 107 for clarity). From these
fluctuations the Sk-ASk pair is created by a current in x-direction by separating positive and negative topological charge density perpendicular
to the current direction (here, in the y-direction). The ASk is eventually destroyed around t ≈ 6300ps and only the Sk survives. Parameters are
chosen as Ic = 7.7 × 1011 A/m2 , α = 0.25 and β = 0. Color code refers to topological charge density q always.

form of the initial inhomogeneous magnetization configuration is of minor importance. The time evolution of the system
is calculated by solving the extended LLG Eq. (1) by standard
advanced numerical methods.
Starting from the fully field polarized state n(x, y) ≡ −ẑ,
we first let the system accommodate to the additional By field,
at zero external current. After this initial equilibration, we
switch on the current at t = 0 and calculate q(x, y, t) at every
time step. A movie of this evolution is available in the SM [50]
while a selection of snapshots of q is shown in Fig. 1. Initially,
the very small amplitude b0 of By generates a tiny seed topological charge density of both positive and negative sign with
an overall Q = 0. Gradually, under the influence of the external current, Sk-ASk pairs begin to form with growing magnitudes of q. Consistent with our theoretical prediction, the Sk
and ASk centers separate in the y-direction, perpendicular to
the external current flow. After its full development, since it is
unstable, the ASk disappears on a time scale ∝ 1/α. Thereby
its diameter shrinks relatively quickly, eventually below the
lattice constant. At this moment, Q(t) abruptly changes by
one.
As the evolution of Sk-ASk pairs is interfered by the relatively short life time of the ASk we further illustrate the details of this process by an additional movie [50] where we set
the DMI to zero. Then, neither the Sk nor the ASk is energetically preferred and the full Sk-ASk pair evolves in time as

recently reported in Ref. [33].
The scenario of Sk creation is demonstrated further in
Fig. 2, where we show the time-dependence of Q(t). Over
large time spans, the total topological charge takes an integer values, while occasionally Q(t) jumps to the next integer
within a short transition time. These transitions are accompanied by sudden
R rises of the total negative topological charge
1
dxdy q(x, y, t), a quantity that we define by
QASk (t) = 4π
q<0
integrating over negative Sk-density only. During the times
when Q(t) stays integer, QASk (t) may decrease gradually with
time. This indicates the gradual creation of Sk-ASk pairs,
their growth and their spatial separation, before the finally isolated, but unstable ASk annihilates during a time much shorter
than the duration of its creation, as described above. This
initial gradual development of the first Sk-ASk pair due to
a weak spatial inhomogeneity of the Zeeman field is clearly
seen in Fig. 2. On the other hand, as soon as a finite number
of Sks exist (after 6300 ps in Fig. 2), their intrinsic inhomogeneous magnetization suffices to facilitate further creation of
Sk-ASk pairs in their surroundings, even at a homogeneous
Zeeman-field as we have convinced ourselves independently.
Since the system starts very close to the ferromagnetic
ground state, the Sk creation costs energy. This energy is
pumped into the system by the charge current. Figure 2 confirms the connection between the increase of the energy and

4

FIG. 2. (Color online). Black solid line: Time-dependence of the
total topological charge Q(t). Black dashed line: R
Time-dependence
1
of the total negative charge defined as QASk (t) = 4π
dxdyq(x, y, t)
q<0
stemming from negative q only. Note that QASk does not need to be
integer and that the restriction to lattice points imposes some small,
unimportant ambiguity on the precise determination of q(x, y, t). Red
dashed line: Time-dependence of the energy in reference to the initial energy, E − E0 ≡ E(t) − E(t = 0), per lattice site. Before every
Q-jump, QASk gradually decreases, accompanied by an increase of
the energy which eventually is taken from the external current. Parameters as in Fig. 1.

of negative Sk-density.
The duration for Sk creation can be quantified by the time
τ which we define as the time span from the onset of the current flow till the creation of the first Sk. This creation time is
a combination of the time τpair needed to form a sufficiently
large Sk-ASk pair and the annihilation time τASk of the ASk.
Since both processes happen at least partially simultaneously,
the resulting τ is not a direct sum of both. Still, τASk ≪ τpair
such that we can safely take τ ≈ τpair . Since we attribute the
creation of Sk-ASk pairs to the existence of a finite j(2)
Sk , we
expect Sks to be created faster when the magnitude of j(2)
Sk is
larger. From Eqs. (6b, 6c, 7b) we find |j(2)
|
∝
(α
−
β)I
in
the
c
Sk
limit of vanishing b⊥1 and b⊥2 . In Fig. 3, this relation between
τ and j(2)
Sk is confirmed by the numerical results. Indeed, τ depends on |α − β| and Ic . In particular, no Sks can be created
when α = β which implies that the dissipative current is essential for the charge current-induced Sk creation. Still, finite
creation times appear in an experimentally relevant parameter
regime. Finally, we note that even though we have chosen a
particular seed magnetic field By,r to create topological charge
density fluctuations, their precise origin is not important. In
fact, only an inhomogeneous q(x, y), besides α , β and Ic , 0,
is necessary for j(2)
Sk to become non-vanishing. Thus, a multitude of ways are eligible to create such fluctuations, for example by local fields, material modification, or by temperature.
On the other hand, a change of Q will often be undesirable
in distinct set-ups. Then, j(2)
Sk -contributions to Eqs. (6) should
be suppressed by a proper choice of the material with a small

|α − β|, or by avoiding magnetization fluctuations, apart from
simply working in the low current regime.
In this work, we have established the skyrmion equation of
motion by combining the general definition of the skyrmion
density and the extended Landau-Lifshitz-Gilbert equation.
We here define skyrmion current densities that conserve the
total topological charge of a sample. In the presence of an
in-plane spin current, we identify terms that give rise to simple movement of skyrmions against the externally applied
charge flow. Other contributions to skyrmion current densities that we identify explicitly drive the separation of positive
skyrmion density from negative antiskyrmion density perpendicularly to the charge current flow. These latter contributions
eventually cause the creation of skyrmion-antiskyrmion pairs,
already out of very small magnetic inhomogeneities. The theoretical predictions are corroborated by numerical simulations
and applied to systems with bulk and interfacial DMI.
We acknowledge support from the DFG SFB 668 (project
B16).

Detailed spin structure of skyrmionic objects

In the main body of the paper, we focus on the dynamics
of the skyrmion density as the important quantity to describe
skyrmions or antiskyrmions, respectively. Still, these objects
have an internal magnetic structure given by the magnetization n(x, y, t). In particular, different kinds of DzyaloshinskiiMoriya interactions (DMI) may stabilize different types of
skyrmions. In this Appendix, we show exemplary magnetic
structures for
• bulk DMI
given by the
 i HbDMI =
 Hamiltonian

P h
−D r nr × nr+ex · e x + nr × nr+ey · ey which stabilizes Bloch-like skyrmions (cf. Fig. 4 and movie
“SK density vs time bulkDMI.avi”),
• interfacial
DMI given by the Hamiltonian HiDMIi =
P h
−D r (ẑ × x̂) · (nr × nr+ex ) + (ŷ × ẑ) · (nr × nr+ey )
which
stabilizes
Neél-like
skyrmions
(cf.
Fig.
5
and
movie
“SK density vs time interfacialDMI.avi”),
and,
• no DMI with means stabilization neither of Blochlike nor of Neél-like skyrmions (cf. Fig. 6 and movie
“SK density vs time zeroDMI.avi”).
All figures are snapshots taken from movies which we
also provide as Supplemental Material online in the “other
formats” option on the article’s arXiv page. Even though the
explicit magnetic structures differ for the according DMI, no
qualitative changes for the pair creation process, as described
in the main article, were observed.
We have used the same parameter set as before. The calculations were performed on a L x × Ly = 160 × 160 square
lattice with periodic boundary conditions, external magnetic

5

FIG. 3. (Color online). Decadic logarithm of the Sk creation time τ in dependence of (a) the Gilbert damping constant α and the nonadiabaticity parameter β for Ic = 1012 A/m2 , and, (b) the ratio β/α and the charge current density Ic for α = 0.05. Finite creation times are
never achieved at β = α (dashed lines).

field B = (0, 0, Bz) = −0.03 J ẑ , spin velocity v s = −300m/s,
Gilbert damping α = 0.25 and non-adiabaticity β = 0. To
create initial fluctuations of the skyrmion density, a tiny
modulation to the magnetic field pointing in the y-direction,
i.e., By = b0 [sin(2πx/L x ) + sin(2πy/Ly)] and b0 = Bz/100 has
been added to the external field.

[1] T. Skyrme, Nucl. Phys. 31, 556 (1962).
[2] N. Kiselev, A. Bogdanov, R. Schäfer, and U. Rößler, J. Phys.
D Appl. Phys. 44, 392001 (2011).
[3] A. Bogdanov and A. Hubert, J. Mag. Mag. Mat. 138, 255
(1994).
[4] X. Yu, N. Kanazawa, Y. Onose, K. Kimoto, W. Zhang, S. Ishiwata, Y. Matsui, and Y. Tokura, Nat. Mater. 10, 106 (2011).
[5] S. Heinze, K. Von Bergmann, M. Menzel, J. Brede, A. Kubetzka, R. Wiesendanger, G. Bihlmayer, and S. Blügel, Nat. Phys.
7, 713 (2011).
[6] C. Hanneken, F. Otte, A. Kubetzka, B. Dupé, N. Romming,
K. von Bergmann, R. Wiesendanger, and S. Heinze, Nat. nanotechnol. 10, 1039 (2015).
[7] S. Mühlbauer, B. Binz, F. Jonietz, C. Pfleiderer, A. Rosch,
A. Neubauer, R. Georgii, and P. Böni, Science 323, 915 (2009).
[8] A. Bogdanov, Sov. Phys. JETP Lett. 62, 247 (1995).
[9] A. Bogdanov and A. Hubert, J. Mag. Mag. Mat. 195, 182
(1999).
[10] U. Rößler, A. Bogdanov, and C. Pfleiderer, Nature 442, 797
(2006).
[11] K. Shibata, X. Yu, T. Hara, D. Morikawa, N. Kanazawa, K. Kimoto, S. Ishiwata, Y. Matsui, and Y. Tokura, Nat. nanotechnol.
8, 723 (2013).
[12] N. Romming, A. Kubetzka, C. Hanneken, K. von Bergmann,
and R. Wiesendanger, Phys. Rev. Lett. 114, 177203 (2015).
[13] J. Hagemeister, N. Romming, K. von Bergmann, E. Vedmedenko, and R. Wiesendanger, Nat. Comm. 6, 8455 (2015).
[14] X.-L. Qi, Y.-S. Wu, and S.-C. Zhang, Phys. Rev. B 74, 085308
(2006).
[15] M. W. Hirsch, “Degrees, intersection numbers, and the euler
characteristic,” in Differential Topology (Springer New York,
New York, NY, 1976) pp. 120–141.

[16] A. Rosch, Nat. nanotechnol. 8, 160 (2013).
[17] J. Sampaio, V. Cros, S. Rohart, A. Thiaville, and A. Fert, Nat.
nanotechnol. 8, 839 (2013).
[18] J. Iwasaki, M. Mochizuki, and N. Nagaosa, Nat. nanotechnol.
8, 742 (2013).
[19] J. Iwasaki, M. Mochizuki, and N. Nagaosa, Nat. Comm. 4,
1463 (2013).
[20] F. Jonietz, S. Mühlbauer, C. Pfleiderer, A. Neubauer,
W. Münzer, A. Bauer, T. Adams, R. Georgii, P. Böni, R. Duine,
et al., Science 330, 1648 (2010).
[21] X. Yu, N. Kanazawa, W. Zhang, T. Nagai, T. Hara, K. Kimoto,
Y. Matsui, Y. Onose, and Y. Tokura, Nat. Comm. 3, 988 (2012).
[22] S. Krause and R. Wiesendanger, Nat. Mater. 15, 493 (2016).
[23] S. Woo, K. Litzius, B. Krüger, M.-Y. Im, L. Caretta, K. Richter,
M. Mann, A. Krone, R. M. Reeve, M. Weigand, et al., Nat.
Mater. , 501 (2016).
[24] X. Zhang, G. Zhao, H. Fangohr, J. P. Liu, W. Xia, J. Xia, and
F. Morvan, Sci. Rep. 5 (2015).
[25] A. Fert, V. Cros, and J. Sampaio, Nat. nanotechnol. 8, 152
(2013).
[26] N. Nagaosa and Y. Tokura, Nat. nanotechnol. 8, 899 (2013).
[27] Y. Tchoe and J. H. Han, Phys. Rev. B 85, 174416 (2012).
[28] W. Jiang, P. Upadhyaya, W. Zhang, G. Yu, M. B. Jungfleisch,
F. Y. Fradin, J. E. Pearson, Y. Tserkovnyak, K. L. Wang,
O. Heinonen, S. G. E. te Velthuis, and A. Hoffmann, Science
349, 283 (2015).
[29] W. Koshibae and N. Nagaosa, Nat. Comm. 7 (2016).
[30] N. Romming, C. Hanneken, M. Menzel, J. E. Bickel, B. Wolter,
K. von Bergmann, A. Kubetzka, and R. Wiesendanger, Science
341, 636 (2013).
[31] A. Thiele, Phys. Rev. Lett. 30, 230 (1973).
[32] J. Müller and A. Rosch, Phys. Rev. B 91, 054410 (2015).
[33] K. Everschor-Sitte, M. Sitte, T. Valet, J. Sinova, and
A. Abanov, arXiv:1610.08313 (2016).
[34] X. Yu, D. Morikawa, Y. Tokunaga, M. Kubota, T. Kurumaji,
H. Oike, M. Nakamura, F. Kagawa, Y. Taguchi, T.-h. Arima,
M. Kawasaki, and Y. Tokura, Adv. Mat. , 1606178 (2017),
1606178.
[35] G. Tatara, H. Kohno, and J. Shibata, Phys. Rep. 468, 213
(2008).
[36] Z. Li and S. Zhang, Phys. Rev. Lett. 92, 207203 (2004).
[37] Y. B. Bazaliy, B. Jones, and S.-C. Zhang, Phys. Rev. B 57,
R3213 (1998).
[38] M. Lakshmanan, Philosophical Transactions of the Royal Soci-

6

FIG. 4. Skyrmion density q(x, y, t) at t = 6296ps. The marked area is magnified on the left-hand
side where the arrows
also showi the mag

P h
netization n(x, y, t) in the xy plane. The bulk Dzyaloshinskii-Moriya interaction HbDMI = −D r nr × nr+ex · ex + nr × nr+ey · ey stabilizes
Bloch-like skyrmions.

7

FIG. 5. Skyrmion density q(x, y, t) at t = 4933ps. The marked area is magnified on the left-hand side where the arrows also
show h
the magnetization n(x, y, t) in the xy plane.
In contrast to Fig. 4 an interfacial Dzyaloshinskii-Moriya interaction HiDMI =
i
P
−D r (ẑ × x̂) · (nr × nr+ex ) + (ŷ × ẑ) · (nr × nr+ey ) has been used, which stabilizes Neél-like skyrmions.
ety of London A: Mathematical, Physical and Engineering Sciences 369, 1280 (2011).
[39] S. Zhang and S. S.-L. Zhang, Phys. Rev. Lett. 102, 086601
(2009).
[40] C. Heo, N. S. Kiselev, A. K. Nandy, S. Blügel, and T. Rasing,
Sci. Rep. 6 (2016).
[41] A. Bogdanov and D. Yablonskii, Zh. Eksp. Teor. Fiz 95, 182
(1989).
[42] M. Garst, “Topological skyrmion dynamics in chiral magnets,”
in Topological Structures in Ferroic Materials: Domain Walls,
Vortices and Skyrmions, edited by J. Seidel (Springer International Publishing, Cham, 2016) pp. 29–53.
[43] G. S. Frederico and D. F. Torres, J. Math. Anal. Appl. 334, 834
(2007).
[44] M. Stone, Phys. Rev. B 53, 16573 (1996).

[45] Y. Nakatani, J. Shibata, G. Tatara, H. Kohno, A. Thiaville, and
J. Miltat, Phys. Rev. B 77, 014439 (2008).
[46] X. Zhang, G. Yu, W. Zhang, X. Wang, M. Benjamin Jungfleisch, J. E. Pearson, X. Cheng, O. Heinonen, K. L.
Wang, Y. Zhou, A. Hoffmann, and S. G. E. te Velthuis, Nat.
Phys. 13, 162–169 (2016).
[47] K. Litzius, I. Lemesh, B. Krüger, P. Bassirian, L. Caretta,
K. Richter, F. Büttner, K. Sato, O. A. Tretiakov, J. Förster, R. M.
Reeve, M. Weigand, I. Bykova, H. Stoll, G. Schutz, G. S. D.
Beach, and M. Kläui, Nat. Phys. 13, 170–175 (2016).
[48] A. Thiaville, S. Rohart, É. Jué, V. Cros, and A. Fert, Europhys.
Lett. 100, 57002 (2012).
[49] M. Benitez, A. Hrabec, A. Mihai, T. Moore, G. Burnell, D. McGrouther, C. Marrows, and S. McVitie, Nat. Comm. 6 (2015).
[50] See Supplemental Material at the ancillary file section of arXiv
(“other formats”) for movies of skyrmion-pair evolution.

8
(a)

(b)

FIG. 6. Skyrmion density q(x, y, t) at (a) t = 10772ps and (b) t = 14392ps. The marked areas are magnified on the left-hand side where the
arrows also show the magnetization n(x, y, t) in the xy plane. The Dzyaloshinskii-Moriya interaction is set to zero. This has two consequences:
(i) neither the skyrmion nor the antiskyrmion is preferred and both types are symmetrically created and (ii) skyrmions can be of Neél or Bloch
shape.


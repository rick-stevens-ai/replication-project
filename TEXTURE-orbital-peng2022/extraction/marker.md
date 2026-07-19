<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2209.07051 -->

Spin-orbital-angular-momentum-coupled quantum gases
Shi-Guo Peng, and Kaijun Jiang
State Key Laboratory of Magnetic Resonance and Atomic and Molecular Physics,
Innovation Academy for Precision Measurement Science and Technology,
Chinese Academy of Sciences, Wuhan 430071, China and
Center for Cold Atom Physics, Chinese Academy of Sciences, Wuhan 430071, China

arXiv:2209.07051v2 [cond-mat.quant-gas] 5 Nov 2022

Xiao-Long Chen, and Ke-Ji Chen
Department of Physics and Key Laboratory of Optical Field Manipulation of Zhejiang Province,
Zhejiang Sci-Tech University, Hangzhou 310018, China

Peng Zou
College of Physics, Qingdao University, Qingdao 266071, China

Lianyi He
Department of Physics and State Key Laboratory of Low-Dimensional
Quantum Physics, Tsinghua University, Beijing 100084, China
(Dated: November 8, 2022)
We briefly review the recent progress of theories and experiments on spin-orbital-angularmomentum (SOAM)-coupled quantum gases. The coupling between the intrinsic degree of freedom
of particles and their external orbital motions widely exists in the universe, and leads to a broad
variety of fundamental phenomena in both classical physics and quantum mechanics. The recent
realization of synthetic SOAM coupling in cold atoms has attracted a great deal of attention, and
stimulated a large amount of considerations on exotic quantum phases in both Bose and Fermi gases.
In this review, we present a basic idea of engineering SOAM coupling in neutral atoms, starting
from a semiclassical description of atom-light interaction. Unique features of single-particle physics
in the presence of SOAM coupling are discussed. The intriguing ground-state quantum phases of
weakly interacting Bose gases are introduced, with emphasis on a so-called angular stripe phase,
which has not yet been observed at present. It is demonstrated how to generate a stable giant
vortex in a SOAM-coupled Fermi superfluid. We also discuss the topological characters of a Fermi
superfluid in the presence of SOAM coupling. We then introduce the experimental achievement of
SOAM coupling in 87 Rb Bose gases and its first observation of phase transitions. The most recent
development of SOAM-coupled Bose gases in experiments is also summarized. Regarding the controllability of ultracold quantum gases, it opens a new era, from the quantum simulation point of
view, to study the fundamental physics resulting from SOAM coupling as well as newly emergent
quantum phases.

CONTENTS

V. SOAM-coupled Fermi gases
A. Pairing physics under SOAM coupling
B. SOAM-coupling-induced vortex states
C. SOAM-coupling-induced topological states

10
10
10
12

VI. Experiment achievements

14

VII. Conclusions and outlooks

16

I. Introduction

1

II. Spin-orbital-angular-momentum coupling
A. Semiclassical theory of atom-light
interactions
B. SOAM-coupled Hamiltonian and
symmetries

3

4

VIII. acknowledgments

18

III. Single-particle physics
A. Single-particle spectrum
B. Spin textures
C. Artificial gauge field

5
5
6
6

References

18

IV. SOAM-coupled Bose gases
A. Gross-Pitaevskii theory and a variational
approach
B. Typical ground-state phases
C. Exotic angular stripe phases

7

3

7
8
9

I.

INTRODUCTION

The spin-orbital-angular-momentum (SOAM) coupling, the coupling between the spin degree of freedom
and the external orbital motion, is one of the most common phenomena in our nature. A prominent example in
classical physics is the astronomical fact that the Moon

2
always shows the same side to the Earth, known as the
tidal locking or the spin-orbit locking [1]. In atomic
physics, SOAM coupling is a relativistic effect, which
gives rise to the fine structure of energy levels of hydrogen atoms [2]. A similar effect occurs for protons
and neutrons moving inside the nucleus, leading to a
shift in their energy levels in the nucleus shell model
[3]. In condensed-matter physics, an analogous coupling between the electron spin and its velocity, namely
the spin-linear-momentum (SLM) coupling or spin-orbit
(SO) coupling, results in a variety of intriguing and fundamental phenomena, such as the spin-Hall effect or
topological insulators [4], which have potential applications in quantum devices. Although numerous fascinating behaviors of many-body quantum systems are closely
related to SOAM or SO coupling, they are mostly intractable or manifest themselves under extreme conditions. Therefore, it is of important significance to find a
system, which could mimic the unique features of SOAMor SO-coupled quantum systems in a controllable way.
Owing to the advances in the experimental technique,
ultracold atomic gases acquire a high degree of controllability and tunability in interatomic interaction, geometry,
purity, atomic species, and lattice constant (of optical
lattices) [5–9]. To date, ultracold quantum gases have
emerged as a versatile platform for exploring a broad variety of many-body phenomena and can realize physical
effects with analogs throughout physics [4, 10, 11]. However, unlike charged particles, neutral atoms cannot experience the influence of external electromagnetic fields.
Fortunately, thanks to the controlling of atom-light interaction, the internal hyperfine states of neutral atoms,
playing a role of (pseudo-)spin, are coupled to their linear momentum of center-of-mass motion, which equivalently introduces a class of SO couplings experienced
by atoms. For example, the theoretical scheme of realizing a one-dimensional (1D) SO coupling with equal
Rashba and Dresselhaus strengths was proposed in cold
atoms according to a Raman process with a simple Λtype configuration [12]. Then the basic idea was broadly
applied in experiments with both bosonic and fermionic
atoms [13–27]. Soon, an impressive amount of theoretical
and experimental efforts have been devoted to the realization of high-dimensional SO coupling [28–41]. The highdimensional SO coupling corresponds to a non-Abelian
gauge field and has nontrivial geometric or topological
effects, which are absent in systems with 1D SO coupling. Regarding the controllability of ultracold quantum
gases, it opens a new era, from the quantum simulation
point of view, to study the fundamental physics resulting from SO-coupling as well as newly emergent quantum
phases [42–44].
Though the SO coupling has intensively been studied in the field of condensed matter as well as in ultracold atoms, it is different from the original meaning of
SO coupling in atomic physics, in which it indicates the

coupling between the spin and the orbital angular momentum. Recently, such type of SO coupling, i.e., the
SOAM coupling, is theoretically proposed in cold atoms
and enriches our understanding of quantum many-body
physics [45–52]. It is experimentally achieved in 87 Rb
Bose gases according to a Raman process by using a
pair of copropagating laser beams operated in LaguerreGaussian (LG) modes [53–55]. The ground-state phase
diagram of the systems is confirmed. The hysteresis loop
is observed across the phase boundary, which is a hallmark of the first-order phase transitions. This is due
to the unique property of the quantized angular momentum, unlike that of the linear momentum in SLM-coupled
systems [56–59]. Later on, a considerable amount of
attention has been paid to a supersolid-like phase [60–
64], namely the angular stripe phase, which breaks the
U(1) gauge symmetry to behave like a superfluid and also
breaks the angular translational symmetry (or the rotational symmetry) to manifest spatial order in the angular density [65]. Nevertheless, this kind of angular stripe
phases has not yet been observed because of the narrow
window of parameters that is hardly reached in experiments at present [63].
Soon, the idea of SOAM coupling is theoretically generalized to fermionic systems [66, 67], where the pairing mechanics plays a crucial role in the Fermi superfluid. While it is shown that the SOAM coupling leads
to the spin-dependent vortex formation in Bose-Einstein
condensates, SOAM coupling alone does not induce vortices in a Fermi superfluid, since fermions in a Cooper
pair would acquire opposite orbital angular momenta
that cancel each other, yielding a superfluid devoid of
vortices. However, by introducing a moderate detuning
away from the two-photon resonance in the Raman process, which breaks the time-reversal symmetry of systems, a giant vortex superfluid phase could remain stable in SOAM-coupled Fermi gases. The Cooper pairs
can possess quantized angular momenta, featured as an
angular analog of the Fulde-Ferrell pairing state in SOcoupled Fermi gases, where Cooper pairs inevitably carry
finite center-of-mass momentum due to the asymmetry
of SO-dressed Fermi surface under Zeeman field [68–74].
These SOAM-coupling induced vortices have fascinating
and unique features. For example, their size could be
as strikingly large as the length scale comparable to the
waist of Raman beams. This is markedly different from
previously studied vortices in atomic Fermi superfluids, where changes in the vortex-core structure predominantly take place within a short-length scale set by the interatomic separation [75, 76]. Besides, the vortex core exhibits a large spin imbalance, which originates from spinpolarized vortex-bound states, or the so-called Caroli–de
Gennes–Matricon (CdGM) states [77], and would serve
as an ideal experimental signal. Subsequently, the topological characters of a ring-shape SOAM-coupled Fermi
superfluid are explored, in which the ac-stark potential

3
of Raman beams provides a strong radial confinement
[78]. The genic features of topological superfluid are encoded in the quantized angular degree of freedom. Nevertheless, a fundamental hurdle to the experimental observation of the SOAM-coupling-induced pairing states is
the inevitable heating during the Raman process, which
makes it difficult to cool the system below the superfluid
transition temperature. Instead, it is reasonable to expect that molecule states in the SOAM-coupled Fermi
gases could survive even above the critical temperature,
as what occurs in SO-coupled systems [19, 79]. Accordingly, a scenario, using the radio-frequency spectroscopy
based on two-body physics, provides an accessible detection of the pairing mechanics under current experimental
conditions [80].
The rest of the review is arranged as follows. In
the next section, we present the theoretical scheme of
how the SOAM-coupling effect could be achieved in cold
atoms according to a Raman transition. Starting from
a semiclassical description of atom-light interaction, the
effective Hamiltonian of a single atom is derived. The
possible symmetries of the system are then discussed,
which play an important role in understanding the fundamental properties of the system. In Sec. III, singleparticle physics is introduced, including the energy spectrum and the intriguing spin texture of the ground state.
The emergent synthetic gauge field experienced by cold
atoms in the presence of atom-light interaction is also
demonstrated. In Sec. IV, the ground-state properties
of weakly interacting SOAM-coupled Bose gases are discussed, based on the solution of the Gross-Pitaevskii
equation. The quantum phases of Bose condensates are
then identified as well. The emphasis on the properties of
the angular stripe phases is presented. We also propose
possible scenarios to enlarge the window of parameters
that might be accessible in experiments to observe them.
It follows the discussion on the ground state of interacting SOAM-coupled Fermi gases in Sec. V. The pairing
mechanism of fermions in the presence of SOAM-coupling
is introduced. Two exotic pairing states, i.e., SOAMcoupling-induced giant vortex and topological superfluid
states, are shown to be stabilized under SOAM coupling.
Subsequently, the most recent progress of experiments
related to SOAM-coupled quantum gases is summarized
in Sec. VI. Sec. VII is devoted to the conclusions and
outlooks for future advances.

II.

SPIN-ORBITAL-ANGULAR-MOMENTUM
COUPLING

The key idea of generating SOAM coupling in neutral
atoms has been proposed by several earlier works [46–
48], in which two hyperfine states of atoms are coupled
by a pair of copropagating LG beams according to a Raman process as shown in Fig. 1. The two LG beams

Figure 1. Scheme of the SOAM coupling. Two hyperfine
states of atoms (denoted by |↑i and |↓i) are coupled to
an excited state |3i by a pair of far-detuned copropagating
Laguerre-Gaussian beams E± (r, t). Here, δ and ∆ are the
two-photon and single-photon detunings respectively.

carry different orbital angular momenta along the direction of beam propagation, that leads to an orbital angular
momentum change of atoms when transitioning between
the two ground hyperfine states. In the following, we
are going to derive the effective Hamiltonian of an alkali
metal atom in the presence of a pair of Raman LG beams
based on the semiclassical description of atom-light interaction [45, 81, 82].

A.

Semiclassical theory of atom-light interactions

In the semiclassical theory, the atom-light interaction
during the Raman process is described by the following
Hamiltonian


~ω↑ 0 V↑3
Ĥal =  0 ~ω↓ V↓3 
(1)
V3↑ V3↓ ~ω3
T

in the bare hyperfine basis [|↑i , |↓i , |3i] , where ~ωσ
(σ =↑, ↓, 3) is the bare energy of atoms in different hyperfine states, and Vσσ0 = − hσ| d · E(±) |σ 0 i characterizes
the dipole interactions between the valence electron and
light fields. Here, d is the electric moment of the valence
electron and
E± (r, t) =


1 
ê± E± (r) e−iω± t + h.c.
2

(2)

are the electric fields experienced by atoms, where ê±
denote the unit vectors of the polarization direction of
light, ω± are the angular frequencies of Raman beams,
and E± (r) are the spatial complex amplitudes. The wave
function of atoms can also be written in the bare hyperfine basis as


c↑ (t) e−iη↑ t
Ψ (t) =  c↓ (t) e−iη↓ t  ,
(3)
c3 (t) e−iη3 t

4
and ησ are arbitrary factors that are chosen for later convenience. Inserting Eqs. (1) and (3) into the Schrödinger
equation i~∂t Ψ = Ĥal Ψ and by choosing
1
(ω↑ + ω↓ − ω+ + ω− ) ,
2
1
η↓ = (ω↑ + ω↓ + ω+ − ω− ) ,
2
1
η3 = (ω↑ + ω↓ + ω+ + ω− ) ,
2
η↑ =

(4)
(5)
(6)

we easily obtain
dc↑
δ
1
∗
= + c↑ + ρ∗+ E+
(r) c3 ,
dt
2
2
dc↓
δ
1
∗
i~
= − c↓ + ρ∗− E−
(r) c3 ,
dt
2
2
1
1
dc3
= ρ+ E+ (r) c↑ + ρ− E− (r) c↓ − ∆c3
i~
dt
2
2

i~

ρ+ E+ (r)
ρ− E− (r)
c↑ +
c↓ .
2∆
2∆

(8)
(9)

(10)

After inserting Eq. (10) into Eqs. (7) and (8), we arrive
at
  
 
d c↑
δ/2 + χ+ (r)
Ω (r)
c↑
i~
=
,
Ω∗ (r)
−δ/2 + χ− (r)
c↓
dt c↓
(11)
where
2

|ρ± E± (r)|
,
4∆
∗
(r) E− (r)
ρ∗ ρ− E+
Ω (r) ≡ +
4∆

χ± (r) ≡

(12)
(13)

are respectively the diagonal and off-diagonal ac-stark
shifts. We find that the diagonal ac-stark shift χ± (r)
provides an effective trapping potential for atoms that
could be removed by properly choosing a tune-out wavelength of LG beams in the experiment [55, 83, 84].
The off-diagonal ac-stark shift Ω (r) leads to a spacedependent coupling between two hyperfine states |↑i and
|↓i, and then results in a SOAM coupling of atoms as we
will see below.
B.

where I0 and w are respectively the intensity and waist
of the beams, and l± are their winding numbers. Here,
we have adopted a polar coordinate r = (r, ϕ). Consequently, the single-atom Hamiltonian in the presence of
Raman LG beams takes an effective form of

(7)

under the rotating-wave approximation (RWA) [81],
where ρ+ ≡ h3| − d · ê+ |↑i and ρ− ≡ h3| − d · ê− |↓i are
the matrix elements of the electric dipole moments, and
δ/~ ≡ (ω+ − ω− ) − (ω↓ − ω↑ ) and ∆/~ ≡ (ω+ + ω− ) /2 −
[ω3 − (ω↑ + ω↓ ) /2] are respectively the two-photon and
single-photon detunings. When the excited state |3i is
far from the resonance, we may adiabatically eliminate it
by setting ∂t c3 (t) = 0, and then Eq. (9) yields
c3 ≈

atoms are confined in the z = 0 plane, and the pair of
Raman LG beams copropagate along the −z direction
with the spatial complex amplitude
 r |l± |
p
2
2
e−r /w ,
(14)
E± (r) = 2I0 eil± ϕ
w

SOAM-coupled Hamiltonian and symmetries

Without loss of generality, we consider a twodimensional (2D) configuration for simplicity in that

~2 2
∇ + Vext (r) + Ĥso
2m

(15)


δ/2 + χ (r) Ω (r) e−i2nϕ
,
Ω (r) e+i2nϕ −δ/2 + χ (r)

(16)

Ĥ0 = −
with

Ĥso =

where Vext (r) = mω 2 r2 /2 is the external harmonic potential, n = (l+ − l− ) /2 is the angular momentum trans2
2
|l |+|l |
ferred to atoms, and Ω (r) ≡ ΩR (r/w) + − e−2r /w ,
∗
with the coupling strength ΩR = ρ+ ρ− I0 /2∆, is the
radial Rabi frequency. Here, we have assumed χ+ (r) =
χ− (r) ≡ χ (r) for simplicity, which is only dependent
on |r| = r. Besides, we also discard the internal phase
difference between the matrix elements of electric dipole
moments ρ+ and ρ− that is irrelevant to the problem.
Let us then analyse the possible symmetries of the
single-atom Hamiltonian (15). It is obvious that the rotational symmetry with respect to the z axis is broken by
the dependence of Raman coupling Ĥso on the azimuthal
angle ϕ. The orbital angular momentum of the atom is
thus no longer conserved, since it follows a change of orbital angular momentum accompanied by the spin flip in
the Raman process [46, 60, 62]. By introducing a unitary
transformation Û = exp (inϕσ̂z ), the single-atom Hamiltonian becomes Ĥ0 = Û Ĥ0 Û † , i.e.,
~ ∂ ∂
r
+
2mr ∂r ∂r
2

Ĥ0 = −



L̂z − n~σ̂z

2

2mr2

δ
+ Vext (r) + χ (r) + Ω (r) σ̂x + σ̂z , (17)
2
where L̂z = −i~∂/∂ϕ, and σ̂x,z are Pauli matrices. We
find that the angular momentum L̂z commutes with the
single-atom Hamiltonian Ĥ0 under the unitary transformation Û , and thus L̂z is conserved. Therefore, the
original single-atom Hamiltonian Ĥ0 demonstrates the
symmetry under the redefined rotational transformation
R̂ (ϕ) ≡ Û † e−iL̂z ϕ/~ Û . Then L̂z may be regarded as the
operator of quasi-angular momentum (QAM), and each
eigenstate of the system possesses definite values of QAM
characterized by the corresponding quantum number lz .
It is related to the angular momentum of each spin component in the laboratory frame by l↑,↓ = lz ∓ n. Here, we

5
find that the term of L̂z σ̂z appears, which characterizes
the crucial SOAM-coupling effect that is well familiar to
us in atomic physics.
At the resonance of Raman coupling with δ = 0, the
system demonstrates an additional symmetry, namely
the time-reversal symmetry. The single-atom Hamiltonian Ĥ0 commutes with the time-reversal operator
T̂ = σ̂x K̂, and thus is invariant under the time-reversal
transformation, where K̂ denotes the operator of complex
conjugation [46, 62]. This symmetry may be translated
into
a iQAM frame as T̂ = Û T̂ Û † , and then we have
h
T̂ , Ĥ0 = 0. The time-reversal symmetry guarantees
that the spectrum of a single atom is symmetric about
the QAM lz = n.
III.

SINGLE-PARTICLE PHYSICS
A.

Single-particle spectrum

Regarding the rotational symmetry of the single-atom
Hamiltonian (17), each eigenstate of a single atom should
possess a definite QAM lz , whose wave function may be
written as


ψ↑ (r) eilz ϕ
√ .
(18)
Ψlz (r) =
ψ↓ (r)
2π
Then the Schrödinger equation Ĥ0 Ψlz (r) = EΨlz (r) reduces to two coupled one-dimensional radial equations
of ψ↑,↓ (r), which are easily solved by using the finitedifference method [46]. The single-particle dispersion relations between the energy E and QAM lz are shown
in Fig. 2 for three typical coupling strengths. Here, the
winding numbers of two Raman beams are respectively
chosen to be l+ = −2 and l− = 0, and we consider the
situation at the two-photon resonance with δ = 0. The
symmetry of the single-particle dispersion about lz = 0
is guaranteed by the time-reversal symmetry T̂ discussed
above. This means that the Schrödinger equation is invariant under the exchange of the spin indices, which
sends n → −n as well.
In the absence of SOAM coupling, i.e., ΩR = 0, the energy band structure is simply that of the spinor harmonic
oscillator with the excitation interval ~ω. The ground
state is characterized by the QAM lz = ±1, which is doubly degenerate. The angular momentum for each spin
component in the laboratory frame is (l↑ , l↓ ) = (0, −2)
and (l↑ , l↓ ) = (2, 0) corresponding to the QAM lz = −1
and 1, respectively. As the SOAM-coupling strength ΩR
gradually increases, the spin is no longer a good quantum number, and small amounts of atoms are transferred
into the previously vacant spin component, while the
ground state still has the two-fold degeneracy with definite QAM. By further increasing the coupling strength,
the system finally jumps into the QAM lz = 0 ground

10

10

8

8

6

6

4

4

2

2

6
4
2

0
-4

-2

0

2

0

0
4 -4

-2

0

2

-2
4 -4

-2

0

2

4

Figure 2. The single-particle dispersion for three typical
SOAM-coupling strength ΩR /~ω = 0, 100 and 250 (left to
right). The energy is characterized by two quantum numbers, i.e., the radial quantum number or band index n and
the quasi angular momentum lz . Here, we have set the twophoton detuning δ = 0 and the off-diagonal ac-stark shift
χ (r)=0 as well.
2.5

2.5

2.5

2

2

2

1.5

1.5

1.5

1

1

1

0.5

0.5

0.5

0
-4 -3 -2 -1 0 1 2 3 4

0
-4 -3 -2 -1 0 1 2 3 4

0
-4 -3 -2 -1 0 1 2 3 4

Figure 3. Lowest energy band in the single-particle dispersion
at (a) negative, (b) zero, and (c) positive two-photon detuning
δ when the SOAM-coupling strength ΩR increases (top to
bottom). Adapted from Ref. [60].

state, which gives rise to a first-order phase transition
to a spin-balanced population [55]. This is due to the
unique property of the quantized angular momentum in
SOAM-coupled systems. In SLM-coupled systems, such
phase transition is a continuous type, where the doubly
degenerate ground states finally merge into each other as
the Raman-coupling strength increases [56–59].
Let us look closely at the evolution of the lowestenergy band as presented in Fig. 3 at different coupling
strengths. Its symmetry about lz = 0 is preserved by
the time-reversal symmetry at the two-photon resonance
δ = 0 as shown in Fig. 3(b). We demonstrate how the
ground state evolves from the doubly degenerate states
(lz = ±1) into a single one (lz = 0) as the coupling
strength increases. However, away from the two-photon
resonance with δ 6= 0, we find that the degeneracy of the
ground states at weak coupling strength is lifted, since
the time-reversal symmetry is broken by the two-photon
detuning (as shown in Fig. 3(a) and (c)). The ground
state is located either at lz = −1 or 1 determined by
the sign of the two-photon detuning. This gives rise to
an additional first-order phase transition by continuously
varying the two-photon detuning [55]. At strong coupling
strength, the system again jumps into the QAM lz = 0
ground state as we discussed above.

6
C.

Artificial gauge field

In the following, we are going to demonstrate how the
artificial (synthetic) gauge field may emerge for neutral
atoms in the presence of atom-light interactions. It is one
of the essential ingredients for the simulation of charged
particles moving in the electromagnetic field by using
cold atoms [10, 90–93], which gives rise to a series of
intriguing phenomena, such as the spin Hall effect [94–
96]. To this end, we may simply rewrite the atom-light
Hamiltonian (16) in an explicit form of
Ĥso = Z (r) · s

Figure 4. Spin texture of the ground state of a SOAM-coupled
system at different coupling strengths. The arrows point in
the direction of the local spin S, and the color represents the
projection of the spin onto the z axis. The figure is adapted
from Ref. [46], as well as corresponding parameters therein.

B.

Spin textures

The SO coupling gives rise to intriguing spin textures.
For example, it has been found in studies of 2D Rashba
SO-coupled BECs [85, 86] and BECs exposed to LG
beams [87] that the spin texture contains a topological
knot known as a 2D skyrmion. It is one kind of topological defects protected by their topological nontriviality.
Regarding the spin texture of SOAM-coupled systems, it
is useful to define a spin vector [46, 85, 86]
S (r) =

Ψ† (r) ŝΨ (r)
|Ψ (r)|

2

,

with the spin operator ŝ = (~/2) (σ̂x , σ̂y , σ̂z ).
skyrmion number defined as
1
nskyrmion =
4π

Z

S · (∂x S × ∂y S) dr

(19)
The

(20)

is a measure of the winding of the spin texture, which
distinguishes a skyrmion texture from that of the vacuum. If it equals 1 or −1, a topological knot exists in the
spin texture [88, 89]. The ground-state spin texture at
four typical coupling strengths is presented in Fig. 4. At
weak coupling strength, the two-fold degenerate ground
state gives rise to a spin texture corresponding to a half
skyrmion. As the coupling strength increases, the ground
state finally jumps to the QAM lz = 0 state. The system
reaches a spin-balanced state, which does not support a
skyrmion texture. The local spin becomes planar and
lies in the x − y plane, and thus the skyrmion number
vanishes.

with the effective Zeeman field


δ
2
Ω (r) cos 2nϕ, Ω (r) sin 2nϕ,
.
Z (r) =
~
2

(21)
(22)

We find easily that the Raman-induced atom-light interaction effectively provides a spin-magnetic interaction
equivalent to that for a spin-half charged particle in a
space-dependent Zeeman field Z (r). The diagonalization
of Ĥso simply gives the dressed spin states [10], i.e.,




cos (θ/2)
−e−iφ sin (θ/2)
|ζ+ i =
, |ζ− i =
eiφ sin (θ/2)
cos (θ/2)
(23)
with eigenvalues ±~ |Z (r)| /2, respectively, and tan φ =
tan 2nϕ and tan θ = 2Ω (r) /δ, which determine the orientation of the effective Zeeman field. It is obvious that
|ζ± i denotes the states that the pseudo-spin of the atom
aligns along or inversely to the direction of the local Zeeman field. In the following, let us consider the atom
moves slowly in the space-dependent Zeeman field Z (r),
and its pseudo-spin follows adiabatically one of the eigenstates of Ĥso , namely for example |ζ+ i. Then the full
wave function of the atom can be written as |Ψ (r, t)i =
ψ+ (r, t) |ζ+ i, the evolution of which is governed by the
Schrödinger equation i~∂t |Ψ (r, t)i = Ĥ0 |Ψ (r, t)i under
the Hamiltonian (15). Here, ψ+ (r, t) is the spatial wave
function characterizing the center-of-mass motion of the
atom in the internal dressed state |ζ+ i. By projecting
the Schrödinger equation onto the internal dressed state
|ζ+ i, we obtain easily


2
P̂
−
A
∂ψ+
~ |Z| 

=
+ Vext + W +
i~
 ψ+ . (24)
∂t
2m
2
Two geometric potentials A and W emerge in addition to
the external trapping potential Vext and Zeeman energy
~ |Z| /2, which are respectively the vector potential [10]
A (r) ≡ hζ+ | i~∇ |ζ+ i =

~
(cos θ − 1) ∇φ,
2

(25)

and the scalar potential
W (r) ≡

i
~2
~2 h
2
2
2
|hζ− | ∇ |ζ+ i| =
(∇θ) + sin2 θ (∇φ) .
2m
8m
(26)

7
It is obvious that Eq. (24) takes the same form as that
for a spin-half particle with a unit charge (q = 1) [2].
The effective magnetic field B (r) associated with A (r)
is

B (r) = ∇ × A (r) =

~
∇ (cos θ) × ∇φ.
2

(27)

Here, we should pay special attention to the difference
between the Zeeman field Z (r) and the effective magnetic field B (r): the Zeeman field Z (r) only lifts the
degeneracy of the bare spin states and does not affect
the center-of-mass motion of the atom, while B (r) is the
magnetic field experienced by the center-of-mass motion
of the atom when it moves in the presence of the atomlight interaction and keeps staying in the internal dressed
state |ζ+ i. In the presence of Raman LG beams, the effective magnetic field B (r) takes the explicit form of
"
#
δ/2
n~ ∂
p
êz ,
B (r) =
r ∂r Ω2 (r) + δ 2 /4

(28)

which is perpendicular to the x − y plane and along the
z axis.

IV.

SOAM-COUPLED BOSE GASES

The interatomic interaction plays a crucial role in interacting many-body quantum systems. In this section, we
are going to introduce the ground-state quantum phases
of weakly-interacting Bose-Einstein condensates (BECs)
in the presence of SOAM coupling, within the framework
of the mean-field theory based on the Gross-Pitaevskii
(GP) equation. The interaction gives rise to the appearance of a variety of intriguing angular stripe phases,
which have not yet been observed in current experiments.
The possible theoretical scheme is proposed for observing
angular stripe phases in the 41 K atomic gas with tunable
interatomic interactions.
The mean-field Hamiltonian of a weakly interacting
Bose gas in the presence of SOAM coupling takes the
form of


Z
Ĥ =

dr
+




Ψ∗↑ , Ψ∗↓ Ĥ0



Ψ↑
Ψ↓



o
g↑↑
g↓↓
4
4
2
2
|Ψ↑ | +
|Ψ↓ | + g↑↓ |Ψ↑ | |Ψ↓ | , (29)
2
2

where Ĥ0 is the single-particle Hamiltonian (17), Ψ (r) ≡

T
Ψ↑ (r) , Ψ↓ (r) is the spinor wave function for the condensate, and gσσ0 is the effective 2D intra- (σ = σ 0 ) and
inter-species (σ 6= σ 0 ) interaction strength.

Figure 5. (Top three panels) Typical spin-component, total
density profiles in four distinct phases. (Bottom panel) In
(a-d), the corresponding angular density-density correlation
function 1 − g (2) (θ) is shown. The results for spin-up, spindown and total density are indicated by circles, crosses and
solid lines, respectively. Here, I is for the vortex-antivortex
pair phase, II is for the half-skyrmion phase, III and IV are
for angular stripe phases. Adapted from Ref. [60].

A.

Gross-Pitaevskii theory and a variational
approach

When the interaction is taken into account, the nonlinearity may spontaneously break the rotational symmetry
of the system. We can no longer assume that the condensate possesses the definite QAM lz . The ground-state
solution of the GP equation is first attempted by using
a split-step imaginary time evolution [46]. Three kinds
of quantum phases are identified: two of them still preserve the rotational symmetry as the many-body analogs
of the single-particle ground state, while the third one is
a newly emergent angular stripe phase, which does not
possess a definite QAM and breaks the rotational symmetry.
Therefore, apart from the angular stripe phase, one
may take the states with a definite QAM for the condensates as a good starting point when taking into account
interactions. If the system or the condensate wave function preserves the axial symmetry, one may consider the
QAM lz as a good quantum number and adopt the Ansatz
for the condensate [60]


flz ↑ (r) eilz ϕ
√ ,
ψlz (r) =
flz ↓ (r)
2π

(30)

with the radial wave function flz σ , and substitute it into
the GP equation,


Ĥ0 (L̂z ) + diag(L↑ , L↓ ) ψlz = µψlz ,

(31)

8
where µ is the chemical potential, and the diagonal element takes the form of Lσ ≡ gσσ nσ + g↑↓ nσ̄ (spin index
σ 6= σ̄). Thus, one can then determine the ground-state
wave function ψlz of the rotationally symmetric phases
at zero temperature by solving self-consistently this GP
equation.
Nonetheless, to capture the exotic angular stripe phase
that does not possess a definite QAM, a variational
Ansatz with various angular momenta is adopted for
the condensate wave function in determining the ground
state with an energy-minimizing method [60].
In the realistic configuration of recent experiments [53,
55], the orbital angular momentum transferred by the LG
lasers is n = ±1, giving rise to minima with the QAM
located at lz = ±1, or 0 in the single-particle dispersion.
Thus, the adopted variational Ansatz could be taken as
Ψ (r) = αeiθα ψ−1 + βeiθβ ψ0 + γeiθγ ψ1 ,

(32)

with real weighting coefficients α, β, γ and the associated
phases θα , θβ , and θγ . In general, ψlz is the state with a
definite QAM lz , which can either be the single-particle
state or the one obtained by self-consistently solving the
GP equation (31) when the interaction is taken into account. Nonetheless, the latter is adopted here which contributes a lower mean-field energy than the one from the
single-particle states particularly at low Rabi frequencies
or at relatively strong interactions [60]. Therefore, the
ground-state wave function Ψ (r) is then determined from
the minimization of the mean-field energy in Eq. (29)
with respect to the variational parameters. It’s worth
mentioning that, three definite-QAM states are merely
sufficient here, regarding the recent experimental configuration with the transferred orbital angular momentum
n = ±1 [55]. One may need more definite-QAM states
in the variational Ansatz for larger n.
B.

Typical ground-state phases

After solving self-consistently the GP equation in
Eq. (31) and minimizing the total energy in Eq. (29)
with a constructed variational Ansatz, the ground-state
wave function Ψ(r) can then be calculated and the phase
diagram at zero temperature is conveniently depicted for
a weakly-interacting SOAM-coupled Bose gas [60]. In
general, four distinct phases can be identified in the parameter space of gσσ0 and Ω at a vanishing two-photon
detuning δ = 0. The first is the vortex-antivortex pair
phase which behaves as a vortex, as shown by the first
column in Fig. 5. It locates at zero QAM lz = 0
(i.e., β = 1, α = γ = 0) with zero magnetization
hσz i = 0 and hσx i = −1. The second one is the halfskyrmion phase with two spin-component densities being
a Thomas-Fermi-like distribution and a vortex (see the
second column in Fig. 5). This phase is magnetic, i.e.,
hσz i 6= 0 and hσx i 6= 0, with a definite QAM at lz = −1

Figure 6. A typical phase diagram in the δ-Ω plane of a
SOAM-coupled 41 K gas with inter- and intra-species interactions modulated by the Feshbach resonance technique. The
color indicates the expectation value of spin magnetization
hσz i in the condensate wave function determined by a variational approach. The magenta diamonds indicate the regime
of angular stripe phase III determined by another imaginarytime propagation method (itpm). The green crosses indicate
the selected positions for four distinct phases in Fig. 5, respectively. Here, the Roman numbers stand for the same phases
as those in Fig. 5. Adapted from Ref. [60].

or 1 (i.e., α = 1, β = γ = 0 or γ = 1, α = β = 0). The
third and fourth ones are called angular stripe phases
shown by the peanut-like and halo-like density profiles in
the last two columns of Fig.
√ 5. Both of them have no
definite lz with α = γ = 1/ 2, β = 0 or α = γ 6= 0, β 6= 0
and they have no magnetization hσz i = 0 and hσx i 6= 0.
In addition, one can further investigate the elementary
excitation spectrum to distinguish these phases and then
characterize the phase transitions. The spectrum of a
SOAM-coupled Bose gas is discrete due to the quantized
angular momentum. In detail, the vortex-antivortex
pair phase possesses a symmetric spectrum with a single
phonon mode, see Fig. 7(a). However, the half-skyrmion
phase breaks spontaneously the double degeneracy in
the single-particle dispersion and thus has an excitation
spectrum with a discrete roton-maxon structure [60], as
shown in Fig. 7(b). Most interestingly, owing to the spontaneous breaking of both the U(1) gauge symmetry and
the continuous rotational symmetry, the excitation spectrum in the angular stripe phase exhibits two gapless
Goldstone modes [61], see Fig. 7(c). A summary of the
properties of these typical phases can be found in Table I.
It should be noted that these phases described above are
based on recent experimental configurations with small
transferred angular momentum n, and we use them for
a brief illustration. It is possible to find more nontrivial phases such as other angular stripe phases with superposition of large-angular-momentum states under the
condition of larger n [61, 63] or complex vortex molecule
states [62]. Among these typical ground-state phases, the
most intriguing one is the angular stripe phase, which attracts intensive research attention and will be discussed

9
Table I. A table of the classification of the typical phases in a realistic SOAM-coupled 87 Rb gas with the transferred angular
momentum n = −1 at vanishing two-photon detuning δ = 0 [55].
Vortex-antivortex pair phase
hσz i = 0, hσx i = −1
non-magnetic
β=1
0
(1, −1)
T
R(R)
single minimum
symmetric, single phonon

Spin polarizations
Magnetization
Coefficients in Eq. (32)
lz in Eq. (30)
hL̂z i in ψlz ↑↓
Symmetrya
Symmetry in n↑↓ (n)
Single-particle dispersion
Excitation spectrum
a T , R and C

Angular stripe phases

Reference

hσz i 6= 0, hσx i 6= 0
hσz i = 0, hσx i 6= 0
[55, 60, 62]
magnetic
non-magnetic
[55, 60, 62]
√
α = 1 or γ = 1
α = γ = 1/ 2 or α, β, γ 6= 0
[60]
1 or −1
indefinite
[61–63]
(2, 0) or (0, −2)
indefinite
[61–63]
T
T
[62]

C
(C
)
[60]
R(R)
C2 (C2 ) or 

2 2
double degeneracy
double degeneracy
[53, 55, 60, 61]
asymmetric, roton structure symmetric, two phonons
[60, 61]

2 denote the time-reversal symmetry, continuous and two-fold rotational symmetries, respectively.

2

2

2

1

1

1

0
-4

0
-4

0
-2

-2

Half-skyrmion phase

0

2

4

-2

0

2

4

supersolidity using dipolar quantum gases of lanthanide
atoms (i.e., 162 Dy, 164 Dy, and 166 Er) without any external optical lattice [102–104], and very recently one of
them extended successfully into two dimensions [105].

-1

0

1

2

Figure 7. Excitation spectrum as a function of the quasiangular momentum l of Bogoliubov quasiparticles in three
typical ground-state phases, i.e., (a) vortex-antivortex pair
phase, (b) half-skyrmion phase, and (c) angular stripe phase.
The figures are remade based on data in Refs. [60, 61].

in detail in the following.

C.

Exotic angular stripe phases

In the past decade, an exotic phase of matter has
attracted tremendous attention in ultracold quantum
gases, i.e., namely the stripe phase, which breaks spontaneously U(1) gauge symmetry and spatial translational symmetry [56, 97–99]. As a consequence, quantum gases will exhibit a superfluid behaviour and meanwhile show a periodic modulation in the density distribution. These counterintuitive features associate closely
this nontrivial phase to the long-sought supersolid phase
in solid Helium since the 1960s [65], i.e., a rigid, spatially ordered solid that flows like a fluid without friction. Whether such a superfluid state can exist remains
unclear for more than 50 years until the seminal breakthroughs using ultracold atoms. In 2017, two groups from
ETH Zurich and MIT created successfully an ultracold
quantum gas featuring supersolid properties using BoseEinstein condensates with optical cavities or spin-orbit
coupling [100, 101]. Later in 2019, three independent
groups from Stuttgart, Florence, and Innsbruck observed

In the presence of SOAM coupling, several kinds of
angular stripe phases are theoretically predicted as introduced above, which take the analogous behavior as
that of supersolid. Here, we have discussed two kinds of
angular stripe phases: phase (III), a superposition state
of two orbital-angular-momentum states (lz = ±1), and
phase (IV), a superposition state of three orbital-angularmomentum states (lz = 0, ±1). Although experimentalists have achieved successfully most of the ground-state
quantum phases of a SOAM-coupled Bose gas, the nontrivial angular stripe phase remains elusive in the laboratory. There are two main obstacles. Firstly, the typical
energy scale of the SOAM coupling is about EL ∼ 1/R2
with the atomic cloud size R. To enhance the SOAMcoupling effect to reach the regime of the angular stripe
phase, one needs to reduce the atomic size R which decreases the perimeter of the cloud and instead presents
fewer periods of density order in the angular direction.
Secondly, recent experimental attempts are made in a
87
Rb BEC. The critical Rabi frequency of the angular
stripe phase is thus small due to the tiny difference between the intra- and inter-species interactions. As a consequence, the period of stripes becomes so small that the
stripes show too low contrast and visibility, which makes
them hard to be detected.
The interatomic interaction is one of the crucial factors
to affect the parameter space of angular stripe phases as
well as the visibility. This is quite similar to the situation
when concerning the stripe phase in a SO-coupled Bose
gas [56]. The stripe phase prefers the region where the
inter-species interaction is pretty smaller than the intraspecies interaction. To this end, 41 K atomic gases provide
a promising candidate for exploring angular stripe phases
with tunable interactions according to the Feshbach res-

10
onance centered at the magnetic field B0 = 51.95G [60].
Near the Feshbach resonance, the intraspecies scattering lengths are approximately constant, and the interspecies one can be tuned in a wide range [106, 107].
By setting typical realistic parameters, the phase diagram is determined and the angular stripe phases can
occupy a relatively large parameter space, as shown in
Fig. 6. An angular density-density correlation function
R 2π
R 2π
(2)
gi (θ) ≡ 0 ni (ϕ)ni (ϕ + θ)dϕ/ 0 n2i (ϕ)dϕ can be introduced to estimate the visibility
R ∞ in density profile, with
the angular density ni (ϕ) = 0 rdrni (r, ϕ), and the label i =↑, ↓ for each spin component and null for the total
density. In contrast to other phases, the novel angular
stripe phases break the rotational symmetry and exhibit
spatial density modulation in the angular direction. Two
angular stripe phases feature considerable spatial modulation and contrast in the angular density-density correlation for both spin components as well as the total
one, as shown in Figs. 5(c) and 5(d). This hallmark feature might be useful in directly probing the existence of
the angular stripes in future experiments with ultracold
atoms.
There are also other theoretical attempts and developments emphasizing the angular stripe phases in SOAMcoupled Bose gases. For example, by utilizing LG beams
with higher-order orbital angular momenta, it is shown
that angular stripe phases can be achieved in a wide window of experimentally accessible parameters with high
visibility contrast [63, 66]. Besides, A number of distinct
quantum phases are identified according to the symmetry
analysis, and a complex vortex molecule state is discovered, which plays an important role in the continuous
phase transitions [62]. For a ring-shaped BEC in the
presence of SOAM coupling, the fine structures of angular stripe phases are explored [64].

V.

SOAM-COUPLED FERMI GASES

The pairing mechanism plays a crucial role in the Fermi
superfluid. While it is shown that the SOAM coupling
leads to the spin-dependent vortex formation in BoseEinstein condensates, SOAM coupling alone does not induce vortices in a Fermi superfluid, since fermions in a
Cooper pair would acquire opposite orbital angular momenta that cancel each other, yielding a superfluid devoid of vortices. In this section, we are going to discuss
the unique features of SOAM-coupled Fermi superfluid
at zero temperature, with emphasis on two exotic pairing
states, i.e., SOAM-coupling-induced vortex and topological superfluid states.

A.

Pairing physics under SOAM coupling

It is well known that a two-component spin-balance
Fermi gas becomes unstable in the presence of an
arbitrary small attractive interaction. The resulting
instability gives rise to a Bardeen-Cooper-Schrieffer
(BCS) ground state with zero center-of-mass momentum. It is also well accepted that in a Fermi superfluid with spin-imbalance or Zeeman fields, exotic pairing states emerge, for instance, Fulde-Ferrell and LarkinOvchinnikov states [108, 109], where the former pairing
state carries finite center-of-mass momentum and the latter oscillates both in coordinate and momentum spaces.
Whereas, these novel states are only stable in a very small
parameter region, which is one of the reasons for the exclusiveness of their experimental observations. However,
the experimental achievement of SO coupling in cold
atoms offers a new platform to pursue these long soughtafter states. For instance, the interplay of SO coupling,
Zeeman fields and interactions provides an alternative
mechanism to induce Fulde-Ferrell-Larkin-Ovchinnikov
(FFLO) states [68–74]. Besides SO-coupling-induced
FFLO states, topological band structures become accessible under SO coupling [39, 40, 110–112], which lays
the fertile ground for topological superfluid–for instance,
aided by the Zeeman fields and interactions, a topological
superfluid emerges in a 2D Fermi gas under the Rashbatype SO coupling [113–119].
Intuitively, SOAM coupling as an angular analog of
the conventional SO coupling, two novel pairing states
can be expected. One is the SOAM-coupling-induced
pairing state with finite quantized angular momenta,
which is nothing but a vortex state. The other is the
SOAM-coupling-induced angular topological superfluid
state, the analog of the topological superfluid state in a
one-dimensional lattice gas under a one-dimensional SO
coupling, where quantized angular momenta in the former play the role of discretized linear momenta of the latter. In this review, whether the above two expectational
pairing states, i.e., SOAM-coupling-induced vortex and
topological superfluid states, could be stabilized is clarified. In the following, the former issue will be addressed
in Sec. V B and the latter in Sec. V C.
B.

SOAM-coupling-induced vortex states

As illustrated in Fig. 8, a two-component Fermi gas is
confined in the x − y plane, where the two ground states
are labeled by ↑ and ↓, respectively. The two-photon
Raman process is driven by two copropagating Raman
beams carrying different orbital angular momenta −l1 ~
and −l2 ~ [see Figs. 8(a), 8(b)], and is characterized by
the inhomogeneous Raman coupling Ω(r), two-photon
detuning δ and a phase winding e−2ilϕ . Here, the polar coordinate r = (r, ϕ) is taken. After a unitary trans-

11
3

(b)
l2 ~

⌦(r) ⇠ e

Atom

l2 ~
l1 ~

x

/2

|#i

z

/2

| "i

2

V1

N

V2

SF

1

2

Em,n /EF

Em,n /EF

2
0
2

l1 ~

(c)
20

10

0

m

10

20

0

(a)

0
0

2

0.8

1.2

1.6

/EF

(d)
20

0.4

10

0

m

10

20

Figure 8. (a) SOAM coupling in atoms induced by a pair
of copropagating Raman beams carrying different orbital angular momenta (−l1 ~ and −l2 ~), with a transferred angular
momentum 2l~ = (l1 − l2 )~. (b) Schematic illustration of
the level scheme. (c)(d) Single-particle energy spectra under SOAM coupling for δ = 0 (c), and δ/EF = 0.4 (d) with
EF = ~2 kF2 /(2M ) the Fermi energy and kF the Fermi vector. Black dashed lines denote potential Fermi surfaces in a
many-body setting. Adapted from Ref. [66].

formation, the effective single-particle Hamiltonian again
reduces to Eq. (17). As we can see that the Raman coupling Ω(r) and two-photon detuning δ serve as effective
transverse and longitudinal Zeeman fields, respectively,
which play crucial roles in stabilizing vortices. Different from the LG Raman beams used in previous experiments [53, 55], Chen et al. propose Raman coupling
2
2
as Ω(r) = Ω0 e−2r /w [66], with Ω0 the peak intensity
and w the beam waist, which can be experimentally realized [120]. Such a choice of the Raman beams is mainly
on the basis that the LG Raman beams used in current
experiments are suppressed over a considerable region
near r = 0, giving rise to an almost vanishing spin mixing effect in the vicinity, which is unfavorable for vortex
formation essentially. Here, Raman lasers are assumed to
operate at the tune-out wavelength [55, 83, 84], leading
to a vanishing diagonal ac-stark potential that is consistent with the experiment [55]. The external potential
Vext (r) is chosen as an isotropic hard-wall box trap with
a radius R, which offers a natural boundary.
It is helpful for understanding the mechanism of vortex formation by analysis of the single-particle properties
before moving to the many-body calculation. Figs. 8(c)
and (d) illustrate the impact of the two-photon detuning δ on the single-particle spectrum. At the resonance
with δ = 0, the time-reversal symmetry gives rise to
Em,n = E−m,n . Whereas away from the resonance at finite δ, the breaking of the time-reversal symmetry results
in a deformation of the Fermi surface. In the many-body
setting when the attractive interaction is taken into ac-

0.15

0.40

F/N EF

y

r2
2w
2

⌦0 /EF

(a)

0.35

0.10

(b)
0

0.4

/EF

0.8

0.30

(c)
0

0.4

0.8

1.2

/EF

Figure 9. (a) Phase diagram of a two-dimensional Fermi superfluid with SOAM coupling in the Ω0 -δ plane. The phase
diagram includes the usual superfluid state with κ = 0, the
normal state with ∆ = 0, and two vortex states with κ = −1:
a fully gapped vortex states (V 1) and a gapless vortex state
(V 2). (b)(c) Free energies F of the superfluid (κ = 0; red
dashed), vortex (κ = −1; blue solid) and normal (black
dotted) states as functions of δ, with Ω0 /EF = 2 (b) and
Ω0 /EF = 0.5 (c). Adapted from Ref. [66].

count, pairing predominantly occurs between unlike spins
with the same radial quantum number n to maximize the
overlap of radial wave functions. Thus, for the symmetric eigenspectrum under δ = 0, it is more favorable for
two fermions with opposite angular quantum numbers (m
and −m), forming a Cooper pair with a zero total angular
momenta. In contrast, under a finite δ with asymmetric
eigenspectrum, the two fermions in a Cooper pair may
possess different values of |m|, leading to a pairing state
with a nonzero quantized angular momentum, which is
the so-called vortex state. Such a mechanism for the
vortex formation is analogous to that of the SO-couplinginduced Fulde-Ferrell states, where the interplay between
SO coupling and Zeeman fields gives rise to the deformation of Fermi surfaces with broken time-reversal symmetry in the momentum space [70–74].
Chen et al. confirm the above analysis by solving the
many-body problem under the Bogoliubov–de Gennes
(BdG) formalism [66]. Specifically, the order parameter is written in the form of ∆(r) = ∆(r)eiκϕ , where the
vorticity κ = 0 (κ 6= 0) indicates the superfluid (vortex)
state. With different κ ∈ Z, the BdG equation and ∆(r)
are solved self-consistently with a fixed particle number.
The ground state is then determined by comparing the

12

∆(r)/EF

1.2

0.8

0.4

0

0

0.2

0.4

r/R

0.6

0.8

1

Figure 10. Order parameter profiles for kF w = 5 (blue solid),
kF w = 10 (black dashed), and kF w = 15 (red dash-dotted).
We fix δ/EF = 0.84 and kF R = 15. Adapted from Ref. [66].

free energies of vortex states with different κ, the usual
superfluid state (κ = 0), and the normal state (∆ = 0).
As shown in Fig. 9(a), Chen et al. give a typical phase
diagram of the system with SOAM coupling in the Ω0 –δ
plane. For δ > 0 (δ < 0), vortex states with κ = −1
(κ = 1) emerge, with the phase boundaries unchanged to
the sign of δ. At small Ω0 and δ, the ground state is a
usual superfluid (SF) with a zero vorticity κ = 0. Under sufficiently large Ω0 and/or δ, the free-energy difference between the SF and normal (N ) states becomes vanishingly small, and hence the system enters the normal
state. Remarkably, two vortex states emerge between SF
and N states. For example, with a fixed Ω0 /EF = 1.5
[see Fig. 9(a)], the ground state is in the SF state under
small detunings δ, and becomes a fully-gapped vortex
state (V 1) beyond a critical value of δ. Further increase
of δ gives rise to a gapless vortex state (V 2), whose bulk
excitation gap closes. In Figs. 9(b), 9(c), free energies
of different states are compared, as the phase diagram
is traversed. Especially, for the case with Ω0 = 0.5EF ,
the ground state remains vortexless for finite δ, despite
the deformation of the Fermi surface under SOAM coupling and effective Zeeman fields. This originates from
the quantized nature of the angular momentum, and is
on the sharp contrary to the SO-coupling-induced FuldeFerrell state which carries a nonzero, continuously varying center-of-mass momentum in the presence of SO coupling and Zeeman fields [68–74].
Remarkably, as illustrated in Fig. 10, the SOAMinduced vortex state features a giant and tunable vortexcore size, similar to that in a BEC interacting with a
microwave field [121]. The vortex-core size, characterized by variations of the order parameter, is comparable
to the waist w of LG beams. Compared to the conventional vortex states in atomic Fermi superfluids, where
changes in the vortex-core structure predominantly take
place within a short length scale set by the interatomic

separation [75, 76], these SOAM-coupling-induced vortex
states, with tunable size and core structure, provide unprecedented experimental access to topological defects in
Fermi superfluids.
Different from Chen et al.’s configuration, Wang et al.
investigate a similar vortex-forming scheme under SOAM
coupling [67]. Most strikingly, they predict that an unprecedented vortex state, which is an angular analog of
SO-coupling-induced Larkin-Ovchinnikov state, to occur.
Nevertheless, for the inevitable heating introduced by
the Raman process, it is difficult to cool a realistic Fermi
gas with SOAM coupling below the superfluid temperature [122], which leads to the exclusiveness of SOAMcoupling-induced novel states. Instead, concerning the
persistence of dressed molecules above the critical temperature in Fermi gases with SO coupling [19, 79], it is
reasonable to expect that molecular states in a SOAMcoupled Fermi gas should be readily accessible under typical experimental conditions. Based on the above consideration, Han et al. studied the two-body bound states
in a SOAM-coupled quantum gas of fermions very recently [80]. They identify the condition for the emergence
of molecular states with finite total angular momenta and
propose to detect the molecules according to the radiofrequency spectroscopy. As the molecular states can form
above the superfluid transition temperature, Han et al.
offer an experimentally more accessible route toward the
study of the underlying pairing mechanism under SOAM
coupling.
C.

SOAM-coupling-induced topological states

As discussed in Sec. V A, it is expected that SOAM
coupling can induce a topological superfluid with the help
of Zeeman fields and interactions. While, implemention
of SOAM coupling relies on the spatial dependence of
the LG beams, which gives rise to the dimensionality of
atomic gases must higher than one; whereas, it is also
realized that the Fermi superfluid becomes gapless and
losses its topological features when its spatial dimensionality higher than that of SO coupling [70, 123]. Such
that the one-dimensional nature of the SOAM coupling
(coupling only occurs along the azimuthal direction) imposes a stringent constraint on the stability of an angular topological superfluid. Whether such a topological
superfluid can also be stabilized under SOAM coupling
should be verified. It is shown that the stability of a fully
gapped angular topological superfluid survives the constraint above, provided that the radial motion of atoms
is sufficiently suppressed and then the topological gap is
not closed [78].
The survives of the angular topological superfluid can
be understood through the following analysis. As shown
in Eq. (17), the Raman coupling and the diagonal acstark potential can be written as Ω(r) = Ω0 I(r) and

13

0

<latexit sha1_base64="saL2ZRVHk9n58r3nWRlff1Y3dEI=">AAAB63icbVBNS8NAEJ3Ur1q/qh69LBbBU0mqqMeiF48V7Ae0oWy2m3bp7ibsboQS+he8eFDEq3/Im//GTZqDtj4YeLw3w8y8IOZMG9f9dkpr6xubW+Xtys7u3v5B9fCoo6NEEdomEY9UL8CaciZp2zDDaS9WFIuA024wvcv87hNVmkXy0cxi6gs8lixkBJtMagxiNqzW3LqbA60SryA1KNAaVr8Go4gkgkpDONa677mx8VOsDCOcziuDRNMYkyke076lEguq/TS/dY7OrDJCYaRsSYNy9fdEioXWMxHYToHNRC97mfif109MeOOnTMaJoZIsFoUJRyZC2eNoxBQlhs8swUQxeysiE6wwMTaeig3BW355lXQade+qfvFwWWveFnGU4QRO4Rw8uIYm3EML2kBgAs/wCm+OcF6cd+dj0Vpyiplj+APn8wfDn44R</latexit>

<latexit sha1_base64="saL2ZRVHk9n58r3nWRlff1Y3dEI=">AAAB63icbVBNS8NAEJ3Ur1q/qh69LBbBU0mqqMeiF48V7Ae0oWy2m3bp7ibsboQS+he8eFDEq3/Im//GTZqDtj4YeLw3w8y8IOZMG9f9dkpr6xubW+Xtys7u3v5B9fCoo6NEEdomEY9UL8CaciZp2zDDaS9WFIuA024wvcv87hNVmkXy0cxi6gs8lixkBJtMagxiNqzW3LqbA60SryA1KNAaVr8Go4gkgkpDONa677mx8VOsDCOcziuDRNMYkyke076lEguq/TS/dY7OrDJCYaRsSYNy9fdEioXWMxHYToHNRC97mfif109MeOOnTMaJoZIsFoUJRyZC2eNoxBQlhs8swUQxeysiE6wwMTaeig3BW355lXQade+qfvFwWWveFnGU4QRO4Rw8uIYm3EML2kBgAs/wCm+OcF6cd+dj0Vpyiplj+APn8wfDn44R</latexit>

<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

0.5

<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

0.5 0 0.5

<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

0.5
<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

<latexit sha1_base64="IsoRpY84Ef9JIvt9AL2h3OlWweE=">AAAB6nicbVDLTgJBEOzFF+IL9ehlIjHxhLtq1CPRi0d88EhgQ2aHASbMzm5meo1kwyd48aAxXv0ib/6NA+xB0Uo6qVR1p7sriKUw6LpfTm5hcWl5Jb9aWFvf2Nwqbu/UTZRoxmsskpFuBtRwKRSvoUDJm7HmNAwkbwTDq4nfeODaiEjd4yjmfkj7SvQEo2ilu8ej206x5JbdKchf4mWkBBmqneJnuxuxJOQKmaTGtDw3Rj+lGgWTfFxoJ4bHlA1pn7csVTTkxk+np47JgVW6pBdpWwrJVP05kdLQmFEY2M6Q4sDMexPxP6+VYO/CT4WKE+SKzRb1EkkwIpO/SVdozlCOLKFMC3srYQOqKUObTsGG4M2//JfUj8veWfnk5rRUucziyMMe7MMheHAOFbiGKtSAQR+e4AVeHek8O2/O+6w152Qzu/ALzsc391GNmQ==</latexit>

<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

0.5 0

0.5

0

1

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

<latexit sha1_base64="IsoRpY84Ef9JIvt9AL2h3OlWweE=">AAAB6nicbVDLTgJBEOzFF+IL9ehlIjHxhLtq1CPRi0d88EhgQ2aHASbMzm5meo1kwyd48aAxXv0ib/6NA+xB0Uo6qVR1p7sriKUw6LpfTm5hcWl5Jb9aWFvf2Nwqbu/UTZRoxmsskpFuBtRwKRSvoUDJm7HmNAwkbwTDq4nfeODaiEjd4yjmfkj7SvQEo2ilu8ej206x5JbdKchf4mWkBBmqneJnuxuxJOQKmaTGtDw3Rj+lGgWTfFxoJ4bHlA1pn7csVTTkxk+np47JgVW6pBdpWwrJVP05kdLQmFEY2M6Q4sDMexPxP6+VYO/CT4WKE+SKzRb1EkkwIpO/SVdozlCOLKFMC3srYQOqKUObTsGG4M2//JfUj8veWfnk5rRUucziyMMe7MMheHAOFbiGKtSAQR+e4AVeHek8O2/O+6w152Qzu/ALzsc391GNmQ==</latexit>

x/R

x/R

<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

2⇡
<latexit sha1_base64="saL2ZRVHk9n58r3nWRlff1Y3dEI=">AAAB63icbVBNS8NAEJ3Ur1q/qh69LBbBU0mqqMeiF48V7Ae0oWy2m3bp7ibsboQS+he8eFDEq3/Im//GTZqDtj4YeLw3w8y8IOZMG9f9dkpr6xubW+Xtys7u3v5B9fCoo6NEEdomEY9UL8CaciZp2zDDaS9WFIuA024wvcv87hNVmkXy0cxi6gs8lixkBJtMagxiNqzW3LqbA60SryA1KNAaVr8Go4gkgkpDONa677mx8VOsDCOcziuDRNMYkyke076lEguq/TS/dY7OrDJCYaRsSYNy9fdEioXWMxHYToHNRC97mfif109MeOOnTMaJoZIsFoUJRyZC2eNoxBQlhs8swUQxeysiE6wwMTaeig3BW355lXQade+qfvFwWWveFnGU4QRO4Rw8uIYm3EML2kBgAs/wCm+OcF6cd+dj0Vpyiplj+APn8wfDn44R</latexit>

<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

<latexit sha1_base64="r5ioNOsGkxPSeYG/c7ahAeez5Oc=">AAAB6nicbVDLTsMwENyUVymvAkcuFhUSp5IAAo4VXDiWRx9SG1WO67RWHTuyHaQo6idw4QBCXPkibvwNbpsDtIy00mhmV7s7QcyZNq777RSWlldW14rrpY3Nre2d8u5eU8tEEdogkkvVDrCmnAnaMMxw2o4VxVHAaSsY3Uz81hNVmknxaNKY+hEeCBYygo2VHtKT+1654lbdKdAi8XJSgRz1Xvmr25ckiagwhGOtO54bGz/DyjDC6bjUTTSNMRnhAe1YKnBEtZ9NTx2jI6v0USiVLWHQVP09keFI6zQKbGeEzVDPexPxP6+TmPDKz5iIE0MFmS0KE46MRJO/UZ8pSgxPLcFEMXsrIkOsMDE2nZINwZt/eZE0T6veRfXs7rxSu87jKMIBHMIxeHAJNbiFOjSAwACe4RXeHO68OO/Ox6y14OQz+/AHzucP+NeNmg==</latexit>

<latexit sha1_base64="r5ioNOsGkxPSeYG/c7ahAeez5Oc=">AAAB6nicbVDLTsMwENyUVymvAkcuFhUSp5IAAo4VXDiWRx9SG1WO67RWHTuyHaQo6idw4QBCXPkibvwNbpsDtIy00mhmV7s7QcyZNq777RSWlldW14rrpY3Nre2d8u5eU8tEEdogkkvVDrCmnAnaMMxw2o4VxVHAaSsY3Uz81hNVmknxaNKY+hEeCBYygo2VHtKT+1654lbdKdAi8XJSgRz1Xvmr25ckiagwhGOtO54bGz/DyjDC6bjUTTSNMRnhAe1YKnBEtZ9NTx2jI6v0USiVLWHQVP09keFI6zQKbGeEzVDPexPxP6+TmPDKz5iIE0MFmS0KE46MRJO/UZ8pSgxPLcFEMXsrIkOsMDE2nZINwZt/eZE0T6veRfXs7rxSu87jKMIBHMIxeHAJNbiFOjSAwACe4RXeHO68OO/Ox6y14OQz+/AHzucP+NeNmg==</latexit>

(c) 0.50

2⇡

<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

y/R

(b) 0.50

2⇡

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

y/R

<latexit sha1_base64="wTaNJzeCFMfd/+VvzEsZNI9Ll5g=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0hU1GPRi8eK9gPaUDbbabt0swm7G6GE/gQvHhTx6i/y5r9x2+agrQ8GHu/NMDMvTATXxvO+ncLK6tr6RnGztLW9s7tX3j9o6DhVDOssFrFqhVSj4BLrhhuBrUQhjUKBzXB0O/WbT6g0j+WjGScYRHQgeZ8zaqz04Ll+t1zxXG8Gskz8nFQgR61b/ur0YpZGKA0TVOu27yUmyKgynAmclDqpxoSyER1g21JJI9RBNjt1Qk6s0iP9WNmShszU3xMZjbQeR6HtjKgZ6kVvKv7ntVPTvw4yLpPUoGTzRf1UEBOT6d+kxxUyI8aWUKa4vZWwIVWUGZtOyYbgL768TBpnrn/pnt9fVKo3eRxFOIJjOAUfrqAKd1CDOjAYwDO8wpsjnBfn3fmYtxacfOYQ/sD5/AFWGI0v</latexit>

<latexit sha1_base64="r5ioNOsGkxPSeYG/c7ahAeez5Oc=">AAAB6nicbVDLTsMwENyUVymvAkcuFhUSp5IAAo4VXDiWRx9SG1WO67RWHTuyHaQo6idw4QBCXPkibvwNbpsDtIy00mhmV7s7QcyZNq777RSWlldW14rrpY3Nre2d8u5eU8tEEdogkkvVDrCmnAnaMMxw2o4VxVHAaSsY3Uz81hNVmknxaNKY+hEeCBYygo2VHtKT+1654lbdKdAi8XJSgRz1Xvmr25ckiagwhGOtO54bGz/DyjDC6bjUTTSNMRnhAe1YKnBEtZ9NTx2jI6v0USiVLWHQVP09keFI6zQKbGeEzVDPexPxP6+TmPDKz5iIE0MFmS0KE46MRJO/UZ8pSgxPLcFEMXsrIkOsMDE2nZINwZt/eZE0T6veRfXs7rxSu87jKMIBHMIxeHAJNbiFOjSAwACe4RXeHO68OO/Ox6y14OQz+/AHzucP+NeNmg==</latexit>

0.1

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

(a) 0.50
<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

0.5

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

0.5 0 0.5

<latexit sha1_base64="MWaPrA5CHfCyIH75AHDH7L1twxc=">AAAB63icbVDLSsNAFL3xWeur6tLNYBHcGBLfy6IblxXsA9pQJtNJO3RmEmYmQgn9BTcuFHHrD7nzb5y0WWjrgQuHc+7l3nvChDNtPO/bWVpeWV1bL22UN7e2d3Yre/tNHaeK0AaJeazaIdaUM0kbhhlO24miWISctsLRXe63nqjSLJaPZpzQQOCBZBEj2OTSqede9ipVz/WmQIvEL0gVCtR7la9uPyapoNIQjrXu+F5iggwrwwink3I31TTBZIQHtGOpxILqIJveOkHHVumjKFa2pEFT9fdEhoXWYxHaToHNUM97ufif10lNdBNkTCapoZLMFkUpRyZG+eOozxQlho8twUQxeysiQ6wwMTaesg3Bn395kTTPXP/KPX+4qNZuizhKcAhHcAI+XEMN7qEODSAwhGd4hTdHOC/Ou/Mxa11yipkD+APn8wfFy41q</latexit>

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

<latexit sha1_base64="Nf+gaCzAaTGa0bjhpjzXxW/8PJk=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgadn1fQx68RjRPCBZwuxkkgyZnV1meoWw5BO8eFDEq1/kzb9xkuxBowUNRVU33V1hIoVBz/tyCkvLK6trxfXSxubW9k55d69h4lQzXmexjHUrpIZLoXgdBUreSjSnUSh5MxzdTP3mI9dGxOoBxwkPIjpQoi8YRSvde+55t1zxXG8G8pf4OalAjlq3/NnpxSyNuEImqTFt30swyKhGwSSflDqp4QllIzrgbUsVjbgJstmpE3JklR7px9qWQjJTf05kNDJmHIW2M6I4NIveVPzPa6fYvwoyoZIUuWLzRf1UEozJ9G/SE5ozlGNLKNPC3krYkGrK0KZTsiH4iy//JY0T179wT+/OKtXrPI4iHMAhHIMPl1CFW6hBHRgM4Ale4NWRzrPz5rzPWwtOPrMPv+B8fANcKI0z</latexit>

<latexit sha1_base64="IsoRpY84Ef9JIvt9AL2h3OlWweE=">AAAB6nicbVDLTgJBEOzFF+IL9ehlIjHxhLtq1CPRi0d88EhgQ2aHASbMzm5meo1kwyd48aAxXv0ib/6NA+xB0Uo6qVR1p7sriKUw6LpfTm5hcWl5Jb9aWFvf2Nwqbu/UTZRoxmsskpFuBtRwKRSvoUDJm7HmNAwkbwTDq4nfeODaiEjd4yjmfkj7SvQEo2ilu8ej206x5JbdKchf4mWkBBmqneJnuxuxJOQKmaTGtDw3Rj+lGgWTfFxoJ4bHlA1pn7csVTTkxk+np47JgVW6pBdpWwrJVP05kdLQmFEY2M6Q4sDMexPxP6+VYO/CT4WKE+SKzRb1EkkwIpO/SVdozlCOLKFMC3srYQOqKUObTsGG4M2//JfUj8veWfnk5rRUucziyMMe7MMheHAOFbiGKtSAQR+e4AVeHek8O2/O+6w152Qzu/ALzsc391GNmQ==</latexit>

x/R

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

<latexit sha1_base64="nhfHEoHTXuTHVmzhTmCeuSukVgw=">AAAB/nicbVBNS8NAEN34WetXVDx5CRahPVgTFfVYFIonqWA/oA1hs520SzebsLsRSij4V7x4UMSrv8Ob/8Ztm4O2Phh4vDfDzDw/ZlQq2/42FhaXlldWc2v59Y3NrW1zZ7cho0QQqJOIRaLlYwmMcqgrqhi0YgE49Bk0/cHN2G8+gpA04g9qGIMb4h6nASVYackz94vV46pnl06Kdx2IJWVatEueWbDL9gTWPHEyUkAZap751elGJAmBK8KwlG3HjpWbYqEoYTDKdxIJMSYD3IO2phyHIN10cv7IOtJK1woioYsra6L+nkhxKOUw9HVniFVfznpj8T+vnajgyk0pjxMFnEwXBQmzVGSNs7C6VABRbKgJJoLqWy3SxwITpRPL6xCc2ZfnSeO07FyUz+7PC5XrLI4cOkCHqIgcdIkq6BbVUB0RlKJn9IrejCfjxXg3PqatC0Y2s4f+wPj8AVOwk9E=</latexit>

1

(F

<latexit sha1_base64="LypLBnc4HHKf0aJof+/kYGe9cbg=">AAACBHicbZDLSgMxFIbP1Futt1GX3QwWoW7qjIi6LLpxJRXsBdqhZNJMG5pkhiQjlKELN76KGxeKuPUh3Pk2pu0g2vpD4Mt/ziE5fxAzqrTrflm5peWV1bX8emFjc2t7x97da6gokZjUccQi2QqQIowKUtdUM9KKJUE8YKQZDK8m9eY9kYpG4k6PYuJz1Bc0pBhpY3XtYofEijKDKRfj4/LNz9096tolt+JO5SyCl0EJMtW69menF+GEE6ExQ0q1PTfWfoqkppiRcaGTKBIjPER90jYoECfKT6dLjJ1D4/ScMJLmCO1M3d8TKeJKjXhgOjnSAzVfm5j/1dqJDi/8lIo40UTg2UNhwhwdOZNEnB6VBGs2MoCwpOavDh4gibA2uRVMCN78yovQOKl4ZxXv9rRUvcziyEMRDqAMHpxDFa6hBnXA8ABP8AKv1qP1bL1Z77PWnJXN7MMfWR/fe2SX+g==</latexit>

✏mn /(N ✏0 )
<latexit sha1_base64="k4pRQpe3usGJ4ql/zXemjo24WSs=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4sSQq6rHoxWMV+wFtKJvtpF262YTdjVBC/4EXD4p49R9589+4bXPQ1gcDj/dmmJkXJIJr47rfztLyyuraemGjuLm1vbNb2ttv6DhVDOssFrFqBVSj4BLrhhuBrUQhjQKBzWB4O/GbT6g0j+WjGSXoR7QvecgZNVZ6OPW6pbJbcacgi8TLSRly1Lqlr04vZmmE0jBBtW57bmL8jCrDmcBxsZNqTCgb0j62LZU0Qu1n00vH5NgqPRLGypY0ZKr+nshopPUoCmxnRM1Az3sT8T+vnZrw2s+4TFKDks0WhakgJiaTt0mPK2RGjCyhTHF7K2EDqigzNpyiDcGbf3mRNM4q3mXl/P6iXL3J4yjAIRzBCXhwBVW4gxrUgUEIz/AKb87QeXHenY9Z65KTzxzAHzifP+Z+jPQ=</latexit>

(c)

y/R

(b)

<latexit sha1_base64="mINfg+aHheM79HZECEqXxvUGVvY=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVvV6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDfTmMvQ==</latexit>

F0 )/(N ✏0 )

1 (a)

2

<latexit sha1_base64="Yu7fyWbWS+dMYB8zVdixVT5Ge88=">AAAB6XicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMYh6QhDA76U2GzM4uM7NCWPIHXjwo4tU/8ubfOEn2oIkFDUVVN91dfiy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUy6caBZdYN9wIbMUKaegLbPqj26nffEKleSQfzTjGbkgHkgecUWOlh7NKr1hyy+4MZJl4GSlBhlqv+NXpRywJURomqNZtz41NN6XKcCZwUugkGmPKRnSAbUslDVF309mlE3JilT4JImVLGjJTf0+kNNR6HPq2M6RmqBe9qfif105McN1NuYwTg5LNFwWJICYi07dJnytkRowtoUxxeythQ6ooMzacgg3BW3x5mTQqZe+yfH5/UareZHHk4QiO4RQ8uIIq3EEN6sAggGd4hTdn5Lw4787HvDXnZDOH8AfO5w/oAoz1</latexit>

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

0.4

<latexit sha1_base64="k4pRQpe3usGJ4ql/zXemjo24WSs=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4sSQq6rHoxWMV+wFtKJvtpF262YTdjVBC/4EXD4p49R9589+4bXPQ1gcDj/dmmJkXJIJr47rfztLyyuraemGjuLm1vbNb2ttv6DhVDOssFrFqBVSj4BLrhhuBrUQhjQKBzWB4O/GbT6g0j+WjGSXoR7QvecgZNVZ6OPW6pbJbcacgi8TLSRly1Lqlr04vZmmE0jBBtW57bmL8jCrDmcBxsZNqTCgb0j62LZU0Qu1n00vH5NgqPRLGypY0ZKr+nshopPUoCmxnRM1Az3sT8T+vnZrw2s+4TFKDks0WhakgJiaTt0mPK2RGjCyhTHF7K2EDqigzNpyiDcGbf3mRNM4q3mXl/P6iXL3J4yjAIRzBCXhwBVW4gxrUgUEIz/AKb87QeXHenY9Z65KTzxzAHzifP+Z+jPQ=</latexit>

1

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>


<latexit sha1_base64="B+z8DZ+vtK0ker/mXuFRrBICV1o=">AAAB7XicbVBNSwMxEJ2tX7V+VT16CRbBU9lVUY9FLx4r2A9ol5JNs21sNglJVihL/4MXD4p49f9489+YtnvQ1gcDj/dmmJkXKc6M9f1vr7Cyura+UdwsbW3v7O6V9w+aRqaa0AaRXOp2hA3lTNCGZZbTttIUJxGnrWh0O/VbT1QbJsWDHSsaJnggWMwItk5qdkdYKdwrV/yqPwNaJkFOKpCj3it/dfuSpAkVlnBsTCfwlQ0zrC0jnE5K3dRQhckID2jHUYETasJsdu0EnTilj2KpXQmLZurviQwnxoyTyHUm2A7NojcV//M6qY2vw4wJlVoqyHxRnHJkJZq+jvpMU2L52BFMNHO3IjLEGhPrAiq5EILFl5dJ86waXFbP7y8qtZs8jiIcwTGcQgBXUIM7qEMDCDzCM7zCmye9F+/d+5i3Frx85hD+wPv8AZjIjyc=</latexit>

<latexit sha1_base64="x7/jvIEwHZRaVwWP6+D3P9u2vVs=">AAAB6nicbVBNS8NAEJ3Ur1q/qh69LBbBU0i0qMeiF48V7Qe0oWy2m3bpZhN2J0Ip/QlePCji1V/kzX/jts1Bqw8GHu/NMDMvTKUw6HlfTmFldW19o7hZ2tre2d0r7x80TZJpxhsskYluh9RwKRRvoEDJ26nmNA4lb4Wjm5nfeuTaiEQ94DjlQUwHSkSCUbTSvedWe+WK53pzkL/Ez0kFctR75c9uP2FZzBUySY3p+F6KwYRqFEzyaambGZ5SNqID3rFU0ZibYDI/dUpOrNInUaJtKSRz9efEhMbGjOPQdsYUh2bZm4n/eZ0Mo6tgIlSaIVdssSjKJMGEzP4mfaE5Qzm2hDIt7K2EDammDG06JRuCv/zyX9I8c/0L9/yuWqld53EU4QiO4RR8uIQa3EIdGsBgAE/wAq+OdJ6dN+d90Vpw8plD+AXn4xtapI0y</latexit>

1

2

<latexit sha1_base64="mINfg+aHheM79HZECEqXxvUGVvY=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVvV6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDfTmMvQ==</latexit>

<latexit sha1_base64="E3Dd7EEE/tukiUzX7wafS3WOaK0=">AAAB6HicbVDLTgJBEOzFF+IL9ehlIjHxRHbRqEeiF4+QyCOBDZkdemFkdnYzM2tCCF/gxYPGePWTvPk3DrAHBSvppFLVne6uIBFcG9f9dnJr6xubW/ntws7u3v5B8fCoqeNUMWywWMSqHVCNgktsGG4EthOFNAoEtoLR3cxvPaHSPJYPZpygH9GB5CFn1FipXukVS27ZnYOsEi8jJchQ6xW/uv2YpRFKwwTVuuO5ifEnVBnOBE4L3VRjQtmIDrBjqaQRan8yP3RKzqzSJ2GsbElD5urviQmNtB5Hge2MqBnqZW8m/ud1UhPe+BMuk9SgZItFYSqIicnsa9LnCpkRY0soU9zeStiQKsqMzaZgQ/CWX14lzUrZuypf1C9L1dssjjycwCmcgwfXUIV7qEEDGCA8wyu8OY/Oi/PufCxac042cwx/4Hz+AH69jL4=</latexit>

2

<latexit sha1_base64="Yu7fyWbWS+dMYB8zVdixVT5Ge88=">AAAB6XicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMYh6QhDA76U2GzM4uM7NCWPIHXjwo4tU/8ubfOEn2oIkFDUVVN91dfiy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUy6caBZdYN9wIbMUKaegLbPqj26nffEKleSQfzTjGbkgHkgecUWOlh7NKr1hyy+4MZJl4GSlBhlqv+NXpRywJURomqNZtz41NN6XKcCZwUugkGmPKRnSAbUslDVF309mlE3JilT4JImVLGjJTf0+kNNR6HPq2M6RmqBe9qfif105McN1NuYwTg5LNFwWJICYi07dJnytkRowtoUxxeythQ6ooMzacgg3BW3x5mTQqZe+yfH5/UareZHHk4QiO4RQ8uIIq3EEN6sAggGd4hTdn5Lw4787HvDXnZDOH8AfO5w/oAoz1</latexit>

<latexit sha1_base64="k4pRQpe3usGJ4ql/zXemjo24WSs=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4sSQq6rHoxWMV+wFtKJvtpF262YTdjVBC/4EXD4p49R9589+4bXPQ1gcDj/dmmJkXJIJr47rfztLyyuraemGjuLm1vbNb2ttv6DhVDOssFrFqBVSj4BLrhhuBrUQhjQKBzWB4O/GbT6g0j+WjGSXoR7QvecgZNVZ6OPW6pbJbcacgi8TLSRly1Lqlr04vZmmE0jBBtW57bmL8jCrDmcBxsZNqTCgb0j62LZU0Qu1n00vH5NgqPRLGypY0ZKr+nshopPUoCmxnRM1Az3sT8T+vnZrw2s+4TFKDks0WhakgJiaTt0mPK2RGjCyhTHF7K2EDqigzNpyiDcGbf3mRNM4q3mXl/P6iXL3J4yjAIRzBCXhwBVW4gxrUgUEIz/AKb87QeXHenY9Z65KTzxzAHzifP+Z+jPQ=</latexit>

1

<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>



2

<latexit sha1_base64="mINfg+aHheM79HZECEqXxvUGVvY=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVvV6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDfTmMvQ==</latexit>

<latexit sha1_base64="E3Dd7EEE/tukiUzX7wafS3WOaK0=">AAAB6HicbVDLTgJBEOzFF+IL9ehlIjHxRHbRqEeiF4+QyCOBDZkdemFkdnYzM2tCCF/gxYPGePWTvPk3DrAHBSvppFLVne6uIBFcG9f9dnJr6xubW/ntws7u3v5B8fCoqeNUMWywWMSqHVCNgktsGG4EthOFNAoEtoLR3cxvPaHSPJYPZpygH9GB5CFn1FipXukVS27ZnYOsEi8jJchQ6xW/uv2YpRFKwwTVuuO5ifEnVBnOBE4L3VRjQtmIDrBjqaQRan8yP3RKzqzSJ2GsbElD5urviQmNtB5Hge2MqBnqZW8m/ud1UhPe+BMuk9SgZItFYSqIicnsa9LnCpkRY0soU9zeStiQKsqMzaZgQ/CWX14lzUrZuypf1C9L1dssjjycwCmcgwfXUIV7qEEDGCA8wyu8OY/Oi/PufCxac042cwx/4Hz+AH69jL4=</latexit>

(d)

n" (e)
n#

n (m)/n0

<latexit sha1_base64="k4pRQpe3usGJ4ql/zXemjo24WSs=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4sSQq6rHoxWMV+wFtKJvtpF262YTdjVBC/4EXD4p49R9589+4bXPQ1gcDj/dmmJkXJIJr47rfztLyyuraemGjuLm1vbNb2ttv6DhVDOssFrFqBVSj4BLrhhuBrUQhjQKBzWB4O/GbT6g0j+WjGSXoR7QvecgZNVZ6OPW6pbJbcacgi8TLSRly1Lqlr04vZmmE0jBBtW57bmL8jCrDmcBxsZNqTCgb0j62LZU0Qu1n00vH5NgqPRLGypY0ZKr+nshopPUoCmxnRM1Az3sT8T+vnZrw2s+4TFKDks0WhakgJiaTt0mPK2RGjCyhTHF7K2EDqigzNpyiDcGbf3mRNM4q3mXl/P6iXL3J4yjAIRzBCXhwBVW4gxrUgUEIz/AKb87QeXHenY9Z65KTzxzAHzifP+Z+jPQ=</latexit>

1

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>


<latexit sha1_base64="B+z8DZ+vtK0ker/mXuFRrBICV1o=">AAAB7XicbVBNSwMxEJ2tX7V+VT16CRbBU9lVUY9FLx4r2A9ol5JNs21sNglJVihL/4MXD4p49f9489+YtnvQ1gcDj/dmmJkXKc6M9f1vr7Cyura+UdwsbW3v7O6V9w+aRqaa0AaRXOp2hA3lTNCGZZbTttIUJxGnrWh0O/VbT1QbJsWDHSsaJnggWMwItk5qdkdYKdwrV/yqPwNaJkFOKpCj3it/dfuSpAkVlnBsTCfwlQ0zrC0jnE5K3dRQhckID2jHUYETasJsdu0EnTilj2KpXQmLZurviQwnxoyTyHUm2A7NojcV//M6qY2vw4wJlVoqyHxRnHJkJZq+jvpMU2L52BFMNHO3IjLEGhPrAiq5EILFl5dJ86waXFbP7y8qtZs8jiIcwTGcQgBXUIM7qEMDCDzCM7zCmye9F+/d+5i3Frx85hD+wPv8AZjIjyc=</latexit>

1

2

<latexit sha1_base64="mINfg+aHheM79HZECEqXxvUGVvY=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVvV6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDfTmMvQ==</latexit>

<latexit sha1_base64="E3Dd7EEE/tukiUzX7wafS3WOaK0=">AAAB6HicbVDLTgJBEOzFF+IL9ehlIjHxRHbRqEeiF4+QyCOBDZkdemFkdnYzM2tCCF/gxYPGePWTvPk3DrAHBSvppFLVne6uIBFcG9f9dnJr6xubW/ntws7u3v5B8fCoqeNUMWywWMSqHVCNgktsGG4EthOFNAoEtoLR3cxvPaHSPJYPZpygH9GB5CFn1FipXukVS27ZnYOsEi8jJchQ6xW/uv2YpRFKwwTVuuO5ifEnVBnOBE4L3VRjQtmIDrBjqaQRan8yP3RKzqzSJ2GsbElD5urviQmNtB5Hge2MqBnqZW8m/ud1UhPe+BMuk9SgZItFYSqIicnsa9LnCpkRY0soU9zeStiQKsqMzaZgQ/CWX14lzUrZuypf1C9L1dssjjycwCmcgwfXUIV7qEEDGCA8wyu8OY/Oi/PufCxac042cwx/4Hz+AH69jL4=</latexit>

n" (f)
n#

<latexit sha1_base64="ODY4ZnaltwpwnQuHXGC2DvYbdRA=">AAAB83icbZBLSwMxFIXv1Fetr6pLN4NFcFVmRNRlQRCXFewDOkPJpJk2NJOEPJQyFPwVblwo4tY/485/Y/pYaOuBwMc5N+TmJJJRbYLg2yusrK6tbxQ3S1vbO7t75f2DphZWYdLAggnVTpAmjHLSMNQw0paKoCxhpJUMryd564EoTQW/NyNJ4gz1OU0pRsZZEe/mkZVIKfE47pYrQTWYyl+GcA4VmKveLX9FPYFtRrjBDGndCQNp4hwpQzEj41JkNZEID1GfdBxylBEd59Odx/6Jc3p+KpQ73PhT9/eNHGVaj7LETWbIDPRiNjH/yzrWpFdxTrm0hnA8eyi1zDfCnxTg96gi2LCRA4QVdbv6eIAUwsbVVHIlhItfXobmWTW8qIZ355XazdOsjiIcwTGcQgiXUINbqEMDMEh4hld486z34r17H7PRgjev8BD+yPv8AepYkq0=</latexit>

n"
n#

<latexit sha1_base64="ODY4ZnaltwpwnQuHXGC2DvYbdRA=">AAAB83icbZBLSwMxFIXv1Fetr6pLN4NFcFVmRNRlQRCXFewDOkPJpJk2NJOEPJQyFPwVblwo4tY/485/Y/pYaOuBwMc5N+TmJJJRbYLg2yusrK6tbxQ3S1vbO7t75f2DphZWYdLAggnVTpAmjHLSMNQw0paKoCxhpJUMryd564EoTQW/NyNJ4gz1OU0pRsZZEe/mkZVIKfE47pYrQTWYyl+GcA4VmKveLX9FPYFtRrjBDGndCQNp4hwpQzEj41JkNZEID1GfdBxylBEd59Odx/6Jc3p+KpQ73PhT9/eNHGVaj7LETWbIDPRiNjH/yzrWpFdxTrm0hnA8eyi1zDfCnxTg96gi2LCRA4QVdbv6eIAUwsbVVHIlhItfXobmWTW8qIZ355XazdOsjiIcwTGcQgiXUINbqEMDMEh4hld486z34r17H7PRgjev8BD+yPv8AepYkq0=</latexit>

<latexit sha1_base64="iUNRPzO1zgkuvg3JB5Yn/hhq/aQ=">AAAB9XicbVDLSgMxFL2pr1pfVZdugkVwVWZE1GVBEJcV7APasWTSTBuaSYYkYylDwc9w40IRt/6LO//G9LHQ1gMXDufcy733hIngxnreN8qtrK6tb+Q3C1vbO7t7xf2DulGppqxGlVC6GRLDBJesZrkVrJloRuJQsEY4uJ74jUemDVfy3o4SFsSkJ3nEKbFOepCdrN1VQ0m0VsNxp1jyyt4UeJn4c1KCOaqd4pebpmnMpKWCGNPyvcQGGdGWU8HGhXZqWELogPRYy1FJYmaCbHr1GJ84pYsjpV1Ji6fq74mMxMaM4tB1xsT2zaI3Ef/zWqmNroKMyyS1TNLZoigV2Co8iQB3uWbUipEjhGrubsW0TzSh1gVVcCH4iy8vk/pZ2b8o+3fnpcrN0yyOPBzBMZyCD5dQgVuoQg0oaHiGV3hDQ/SC3tHHrDWH5hEewh+gzx9+fpOU</latexit>

<latexit sha1_base64="ODY4ZnaltwpwnQuHXGC2DvYbdRA=">AAAB83icbZBLSwMxFIXv1Fetr6pLN4NFcFVmRNRlQRCXFewDOkPJpJk2NJOEPJQyFPwVblwo4tY/485/Y/pYaOuBwMc5N+TmJJJRbYLg2yusrK6tbxQ3S1vbO7t75f2DphZWYdLAggnVTpAmjHLSMNQw0paKoCxhpJUMryd564EoTQW/NyNJ4gz1OU0pRsZZEe/mkZVIKfE47pYrQTWYyl+GcA4VmKveLX9FPYFtRrjBDGndCQNp4hwpQzEj41JkNZEID1GfdBxylBEd59Odx/6Jc3p+KpQ73PhT9/eNHGVaj7LETWbIDPRiNjH/yzrWpFdxTrm0hnA8eyi1zDfCnxTg96gi2LCRA4QVdbv6eIAUwsbVVHIlhItfXobmWTW8qIZ355XazdOsjiIcwTGcQgiXUINbqEMDMEh4hld486z34r17H7PRgjev8BD+yPv8AepYkq0=</latexit>

<latexit sha1_base64="iUNRPzO1zgkuvg3JB5Yn/hhq/aQ=">AAAB9XicbVDLSgMxFL2pr1pfVZdugkVwVWZE1GVBEJcV7APasWTSTBuaSYYkYylDwc9w40IRt/6LO//G9LHQ1gMXDufcy733hIngxnreN8qtrK6tb+Q3C1vbO7t7xf2DulGppqxGlVC6GRLDBJesZrkVrJloRuJQsEY4uJ74jUemDVfy3o4SFsSkJ3nEKbFOepCdrN1VQ0m0VsNxp1jyyt4UeJn4c1KCOaqd4pebpmnMpKWCGNPyvcQGGdGWU8HGhXZqWELogPRYy1FJYmaCbHr1GJ84pYsjpV1Ji6fq74mMxMaM4tB1xsT2zaI3Ef/zWqmNroKMyyS1TNLZoigV2Co8iQB3uWbUipEjhGrubsW0TzSh1gVVcCH4iy8vk/pZ2b8o+3fnpcrN0yyOPBzBMZyCD5dQgVuoQg0oaHiGV3hDQ/SC3tHHrDWH5hEewh+gzx9+fpOU</latexit>

<latexit sha1_base64="iUNRPzO1zgkuvg3JB5Yn/hhq/aQ=">AAAB9XicbVDLSgMxFL2pr1pfVZdugkVwVWZE1GVBEJcV7APasWTSTBuaSYYkYylDwc9w40IRt/6LO//G9LHQ1gMXDufcy733hIngxnreN8qtrK6tb+Q3C1vbO7t7xf2DulGppqxGlVC6GRLDBJesZrkVrJloRuJQsEY4uJ74jUemDVfy3o4SFsSkJ3nEKbFOepCdrN1VQ0m0VsNxp1jyyt4UeJn4c1KCOaqd4pebpmnMpKWCGNPyvcQGGdGWU8HGhXZqWELogPRYy1FJYmaCbHr1GJ84pYsjpV1Ji6fq74mMxMaM4tB1xsT2zaI3Ef/zWqmNroKMyyS1TNLZoigV2Co8iQB3uWbUipEjhGrubsW0TzSh1gVVcCH4iy8vk/pZ2b8o+3fnpcrN0yyOPBzBMZyCD5dQgVuoQg0oaHiGV3hDQ/SC3tHHrDWH5hEewh+gzx9+fpOU</latexit>

0.2

<latexit sha1_base64="wI8ZE0iLZfwihoYgup9p6xA4Whg=">AAAB+nicbVBNS8NAEJ34WetXqkcvwSLUS01U1GPRi8cK9gPaEDbbTbt0dxN2N0qJ/SlePCji1V/izX/jts1BWx8MPN6bYWZemDCqtOt+W0vLK6tr64WN4ubW9s6uXdprqjiVmDRwzGLZDpEijArS0FQz0k4kQTxkpBUObyZ+64FIRWNxr0cJ8TnqCxpRjLSRArskgqyraJ+jcYUfn4jADeyyW3WncBaJl5My5KgH9le3F+OUE6ExQ0p1PDfRfoakppiRcbGbKpIgPER90jFUIE6Un01PHztHRuk5USxNCe1M1d8TGeJKjXhoOjnSAzXvTcT/vE6qoys/oyJJNRF4tihKmaNjZ5KD06OSYM1GhiAsqbnVwQMkEdYmraIJwZt/eZE0T6veRfXs7rxcu87jKMABHEIFPLiEGtxCHRqA4RGe4RXerCfrxXq3PmatS1Y+sw9/YH3+AHLFk3k=</latexit>

Figure 11. Bogoliubov spectra of the Fermi superfluid under
SOAM coupling, with a vanishing two-photon detuning δ = 0,
and an increasing Ω0 : (a) Ω0 /0 = 0.15, (b) Ω0 /0 = 0.18, and
(c) Ω0 /0 = 0.2. Adapted from Ref. [78].

2

<latexit sha1_base64="Yu7fyWbWS+dMYB8zVdixVT5Ge88=">AAAB6XicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMYh6QhDA76U2GzM4uM7NCWPIHXjwo4tU/8ubfOEn2oIkFDUVVN91dfiy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUy6caBZdYN9wIbMUKaegLbPqj26nffEKleSQfzTjGbkgHkgecUWOlh7NKr1hyy+4MZJl4GSlBhlqv+NXpRywJURomqNZtz41NN6XKcCZwUugkGmPKRnSAbUslDVF309mlE3JilT4JImVLGjJTf0+kNNR6HPq2M6RmqBe9qfif105McN1NuYwTg5LNFwWJICYi07dJnytkRowtoUxxeythQ6ooMzacgg3BW3x5mTQqZe+yfH5/UareZHHk4QiO4RQ8uIIq3EEN6sAggGd4hTdn5Lw4787HvDXnZDOH8AfO5w/oAoz1</latexit>

<latexit sha1_base64="B+z8DZ+vtK0ker/mXuFRrBICV1o=">AAAB7XicbVBNSwMxEJ2tX7V+VT16CRbBU9lVUY9FLx4r2A9ol5JNs21sNglJVihL/4MXD4p49f9489+YtnvQ1gcDj/dmmJkXKc6M9f1vr7Cyura+UdwsbW3v7O6V9w+aRqaa0AaRXOp2hA3lTNCGZZbTttIUJxGnrWh0O/VbT1QbJsWDHSsaJnggWMwItk5qdkdYKdwrV/yqPwNaJkFOKpCj3it/dfuSpAkVlnBsTCfwlQ0zrC0jnE5K3dRQhckID2jHUYETasJsdu0EnTilj2KpXQmLZurviQwnxoyTyHUm2A7NojcV//M6qY2vw4wJlVoqyHxRnHJkJZq+jvpMU2L52BFMNHO3IjLEGhPrAiq5EILFl5dJ86waXFbP7y8qtZs8jiIcwTGcQgBXUIM7qEMDCDzCM7zCmye9F+/d+5i3Frx85hD+wPv8AZjIjyc=</latexit>

<latexit sha1_base64="TRrcPO/c59N30njxu7WAooHOoxs=">AAAB6nicbVBNS8NAEJ34WetX1aOXxSJ4CkkV9Vj04rGi/YA2lM120i7dbMLuRiilP8GLB0W8+ou8+W/ctjlo64OBx3szzMwLU8G18bxvZ2V1bX1js7BV3N7Z3dsvHRw2dJIphnWWiES1QqpRcIl1w43AVqqQxqHAZji8nfrNJ1SaJ/LRjFIMYtqXPOKMGis9eG6lWyp7rjcDWSZ+TsqQo9YtfXV6CctilIYJqnXb91ITjKkynAmcFDuZxpSyIe1j21JJY9TBeHbqhJxapUeiRNmShszU3xNjGms9ikPbGVMz0IveVPzPa2cmug7GXKaZQcnmi6JMEJOQ6d+kxxUyI0aWUKa4vZWwAVWUGZtO0YbgL768TBoV1790z+8vytWbPI4CHMMJnIEPV1CFO6hBHRj04Rle4c0Rzovz7nzMW1ecfOYI/sD5/AFXnI0w</latexit>

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

χ(r) = χ0 I(r), consistent with configurations of current
experiments on SOAM coupling [53, 55]. Here, Ω0 is
the effective SOAM-coupling strength, χ0 is the trapping strength
of the diagonal ac-stark potential, and
√
2
2
I(r) = ( 2r/w)2l e−2r /w is the spatial intensity profile
of LG lasers, with w the beam waist. Different from the
SOAM-induced vortex state in Sec. V B, here, χ(r) provides an extra confinement potential, which plays an important role in stabilizing the topological superfluid. For
a confinement that is sufficiently tight along the radial
direction, the radial degrees of freedom of the atoms are
frozen, and the remaining quantized angular motion is
then well-captured by an effective one-dimensional model
with discretized modes. Intuitively, such a scenario occurs when the trap p
depth χ0 is so large that the radial excitation energy (∼ |χ0 |~2 /(mw2 )) becomes much larger
than any other relevant energy scales of
pthe system. The
atoms are then localized near r0 =
l/2w in the radial direction and the system reduces to an effective onedimensional model along the angular direction.
The above analysis is confirmed through the BdG approach [78]. As illustrated in Fig. 11, Chen et al. show
the Bogoliubov quasiparticle spectrum in a sufficiently
deep ac-stark potential with χ0 /0 = −8 in the unit of
energy 0 = π 2 ~2 /(2M r02 ). For the case with δ = 0,
the ground state always emerges at κ = 0. Here, consistent with Sec. V B, the vorticity κ = 0 (κ 6= 0) denotes the superfluid (vortex) state. By increasing the
coupling strength Ω0 , the Bogoliubov spectrum undergoes a gap-closing and re-opening process, reminiscent of
that of a topological phase transition. Specifically, the
Bogoliubov quasiparticle excitation is fully gapped under small Ω0 [Fig. 11(a)], and then becomes gapless at
a critical Ωc0 /0 ≈ 0.18 [Fig. 11(b)], and finally is again
fully gapped for further increasing Ω0 [Fig. 11(c)]. The
process of gap closing and re-opening is further demonstrated as a topological phase transition by calculating
the Zak phase of the one-dimensional effective Hamiltonian [78]. Besides, it is also demonstrated that the angular topological superfluid is stabilized when the ac-stark
potential becomes sufficiently large.

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

<latexit sha1_base64="3ctmGRRee+ET+lCZf7yt6t6knas=">AAAB6nicbVDLSgNBEOyNrxhfUY9eBoPgxbAbRT0GvXiMaB6QLGF20kmGzM4uM7NCWPIJXjwo4tUv8ubfOEn2oIkFDUVVN91dQSy4Nq777eRWVtfWN/Kbha3tnd294v5BQ0eJYlhnkYhUK6AaBZdYN9wIbMUKaRgIbAaj26nffEKleSQfzThGP6QDyfucUWOlh7OK2y2W3LI7A1kmXkZKkKHWLX51ehFLQpSGCap123Nj46dUGc4ETgqdRGNM2YgOsG2ppCFqP52dOiEnVumRfqRsSUNm6u+JlIZaj8PAdobUDPWiNxX/89qJ6V/7KZdxYlCy+aJ+IoiJyPRv0uMKmRFjSyhT3N5K2JAqyoxNp2BD8BZfXiaNStm7LJ/fX5SqN1kceTiCYzgFD66gCndQgzowGMAzvMKbI5wX5935mLfmnGzmEP7A+fwBVhaNLw==</latexit>

20

0
<latexit sha1_base64="TpN6sRMdEhkCqnjWyIQJr5WE10I=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivV3V6p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kDe7WMvA==</latexit>

m
<latexit sha1_base64="S5XWwBfQPtVLgOy9+vbVX3rINBE=">AAAB6HicbVBNS8NAEJ34WetX1aOXxSJ4KomKeix68diC/YA2lM120q7dbMLuRiihv8CLB0W8+pO8+W/ctjlo64OBx3szzMwLEsG1cd1vZ2V1bX1js7BV3N7Z3dsvHRw2dZwqhg0Wi1i1A6pRcIkNw43AdqKQRoHAVjC6m/qtJ1Sax/LBjBP0IzqQPOSMGivVo16p7FbcGcgy8XJShhy1Xumr249ZGqE0TFCtO56bGD+jynAmcFLsphoTykZ0gB1LJY1Q+9ns0Ak5tUqfhLGyJQ2Zqb8nMhppPY4C2xlRM9SL3lT8z+ukJrzxMy6T1KBk80VhKoiJyfRr0ucKmRFjSyhT3N5K2JAqyozNpmhD8BZfXibN84p3VbmoX5art3kcBTiGEzgDD66hCvdQgwYwQHiGV3hzHp0X5935mLeuOPnMEfyB8/kD2CmM+Q==</latexit>

20
<latexit sha1_base64="a7FjbJwZqcMVu/+hCUOUc2/YWxU=">AAAB6XicbVBNS8NAEJ34WetX1aOXxSJ4KkkV9Vj04rGK/YA2lM120y7dbMLuRCih/8CLB0W8+o+8+W/ctjlo64OBx3szzMwLEikMuu63s7K6tr6xWdgqbu/s7u2XDg6bJk414w0Wy1i3A2q4FIo3UKDk7URzGgWSt4LR7dRvPXFtRKwecZxwP6IDJULBKFrpoer2SmW34s5AlomXkzLkqPdKX91+zNKIK2SSGtPx3AT9jGoUTPJJsZsanlA2ogPesVTRiBs/m106IadW6ZMw1rYUkpn6eyKjkTHjKLCdEcWhWfSm4n9eJ8Xw2s+ESlLkis0XhakkGJPp26QvNGcox5ZQpoW9lbAh1ZShDadoQ/AWX14mzWrFu6yc31+Uazd5HAU4hhM4Aw+uoAZ3UIcGMAjhGV7hzRk5L8678zFvXXHymSP4A+fzB+yTjPg=</latexit>

Figure 12. (a)–(c) Free energies of pairing states as functions
of κ, with a fixed two-photon detuning δ/0 = −1.6. The insets show the phase of the order parameter. Here, F0 denotes
the ground-state free energy. (d)–(f) Density distribution of
the ground state in the angular-momentum space, where we
define n0 = N/(πr02 ). Here, the blue solid (red dashed) curve
denotes the density distribution of spin-up (spin-down) component. (a), (d) and (b), (e) are the vortexless superfluid
states with Ω0 /0 = 0.1 and 0.16, respectively. (c), (f) is a
topological vortex state with Ω0 /0 = 0.18. Adapted from
Ref. [78].

Building upon the topological superfluid state above,
an exotic topological vortex state can be induced by taking the two-photon detuning δ into account, which deforms the Fermi surface. As shown in Figs. 12(a)–12(c),
the free energy is generically asymmetric with respect
to κ = 0 at a finite δ. The asymmetry becomes more
apparent with increasing Ω0 , until the ground-state order parameter eventually acquires a finite phase with
κ 6= 0. Intriguingly, such a transition into the vortex
state is topological. As demonstrated in [78], while the
Fermi-surface deformation is manifested as the asymmetric spectral shape with respect to m = 0, the closing and
re-opening of the energy gap persist. Indeed, after the
gap is reopened, the angular momentum of the ground
state jumps from κ = 0 to κ = 1. The ground state
simultaneously becomes topological, which is confirmed
by the Zak-phase calculation. Conceptually, such an exotic topological vortex state is the angular version of the
topological Fulde-Ferrell state under the conventional SO
coupling [71–74].
In addition, the topological vortex leaves a direct signature in the angular-momentum-space density profile,
as illustrated in Figs. 12(d)–(f). The density profile of
the minority spin species exhibits a dip close to κ/2 only
in the topological vortex state [Fig. 12(f)], since the spin
polarization in the vortex state is a direct result of the
two-photon detuning, which plays the role of an effective
Zeeman field. Similar signatures have been identified in

14
the topological Fulde-Ferrell state under SO coupling.
The origin of angular topological superfluid comes from
the interplay of interactions, Zeeman fields and SOAM
couplings. As topological superfluids are believed to host
Majorana zero modes at boundaries, once a boundary is
created, for instance, by shining a strong laser beam to
break the ring geometry of the ac stark potential, Majorana zero modes should be observed.
VI.

EXPERIMENT ACHIEVEMENTS

The SOAM coupling has been achieved in 87 Rb Bose
gases independently by two experiment groups [53–55],
following the earlier theoretical proposals [46–48]. The
Zeeman sublevels of the ground hyperfine manifold |F =
1〉 are coupled by a pair of copropagating LG beams according to a Raman transition. It leads to an orbital
angular momentum change of atoms during the transition between the ground Zeeman states, which play
the role of spin. The realization of SOAM coupling in
cold atoms has recently been reported in a spin-1 87 Rb
BEC [53], in which the atoms are loaded into the middleenergy state of three Raman-dressed states. The correlations between spin and orbital angular momentum in this
Raman-dressed state are confirmed. Then the groundstate quantum phase transitions are observed in the same
bosonic system [54], known as the Hess-Fairbank effect [124, 125]. Meanwhile, the SOAM coupling was also
demonstrated in an effective spin-half atomic gas [55], following a similar Raman scheme. The ground-state phase
diagram is comprehensively studied, and the first-order
phase transitions are identified. In the follows, we are
going to introduce the main achievements in these experiments.
In the experiment of Lin’s group [53], the three
hyperfine states of the ground-state manifold
|F = 1, mF = 0, ±1i of 87 Rb atoms are coupled by
a pair of Raman beams as illustrated in Fig. 13, one
of which is an LG beam carrying orbital angular
momentum l = 1. The center-of-mass angular momentum of atoms changes during the transition between
different hyperfine states. This effectively produces a
light-induced effect of a spin |F| = 1 particle moving in
a magnetic Zeeman field Ωef f , which results in a SOAM
coupling after a local spin rotation. In the experiment,
the BEC is initially prepared in the bare hyperfine
state |mF = −1i, and then is transferred to |mF = 0i.
After slowly switching on the Raman fields, the atoms
are adiabatically loaded into the Raman-dressed polar
state |ξ0 i with hFi = 0, the middle-energy eigenstate of
Ωef f · F with the form of [126]
|ξ0 i = −

e−iϕ sin β
eiϕ sin β
√
√
|−1i + cos β |0i +
|+1i (33)
2
2

in the bare hyperfine basis |mF = 0, ±1i, where β (r) =

Figure 13. The schematic of energy-level diagram of Raman
transition in [53]. The hyperfine states of the ground-state
manifold |F = 1i of 87 Rb atoms are coupled by a pair of Raman beams, in which one is a LG beam denoted by “LG” and
the other one is a Gaussian beam denoted by “G”. Here, δ is
the Raman detuning that is tunable in the experiment, and
ωq ≈ 2π × 50Hz is the quadratic Zeeman shift.

arctan [Ω (r) /δ] is the polar angle of the light-induced
magnetic Zeeman field Ωef f . Here, Ω (r) is the Ramancoupling strength and δ is the Raman detuning. After
the adiabatic loading, one easily finds a correlation between the atom spin (hyperfine state) and its orbital angular momentum: the atoms acquire an orbital angular momentum ∆l = 1 (∆l = −1) when transitioning
from |mF = 0i to |mF = −1i (|mF = +1i). Therefore,
the vortex structures are anticipated in the bare hyperfine states |mF = ±1i. The Raman-dressed state |ξ0 i is
conveniently characterized by the QAM lz = 0 in the
rotating frame, and the angular momenta of bare hyperfine states in the laboratory frame are, respectively,
lmF =0 = lz and lmF =±1 = lz ∓ 1.
The vortex structures in the bare hyperfine states
could be probed according to a Stern-Gerlach scheme after a time-of-flight (TOF) expansion by simultaneously
turning off the Raman beams and external trap. The
density profile of bare hyperfine components |mF i after 24ms TOF with holding time 1ms are presented in
Fig. 14(a) for different Raman detunings, as well as the
corresponding total density profile (or optical density)
presented in Fig. 14(b). It is easily found that the
|mF = 0i component carries zero angular momentum,
while the |mF = ±1i components carry the same magnitude of angular momentum indicated from their same
hole sizes. The interference pattern between |mF = ±1i
components shown in Fig. 14(c) implies that they carry
the opposite rotation directions of vortices with angular
momentum l = ∓1.
While the SOAM coupling is demonstrated according
to adiabatically loading atoms into the middle-energy
Raman-dressed state |ξ0 i, the effective light-induced
gauge potential in this dressed state is zero, i.e., A0 =
0 [53], which leads to a vanishing magnetic field experienced by atoms, i.e., B = ∇ × A0 . Subsequently, Lin’s

15

Figure 15. (a) Observation of the phase transition of the
SOAM-coupled ground state between |lg | = 1 and lg = 0
states. The solid and dashed lines are the calculations for
the ideal case and that including the detuning noise in the
experiment. Then density profiles of bare hyperfine states
at δ/2π = 50 and 400Hz are displayed, corresponding to the
QAMs lg = 0 and 1, respectively. (b) Schematic of the spin
textures at δ > 0, where the arrows show the direction of the
transverse spin (hFx i , hFy i). Adapted from Ref. [54].

Figure 14. Demonstration of SOAM coupling in 87 Rb BEC
adiabatically loaded into the Raman-dressed state |ξ0 i. The
images are taken after 24ms TOF with holding time 1ms. (a)
The density profiles of bare hyperfine components |mF i for
different Raman detunings. The blue, red, and green curves
are experimental data for |0i, |+1i and |−1i components, respectively. The black dashed (dash-dotted) curve denotes the
predictions from Eq. (33) magnified by 9.1 in the radial position for |0i (|±1i), while the colored dashed curves are the
full numerical simulations of TOF from 3D time-dependent
Schördinger equation. (b) Radial cross section of the total optical density. Colored solid and dotted (black dashed) curves
indicate the experimental data (TOF simulation at δ = 0).
(c) Interference pattern between |±1i components at δ = 0.
Adapted from Ref. [53].

group further reports the realization of non-zero gauge
potential with SOAM coupling by adiabatically loading
atoms into the Raman-dressed state |ξ−1 i, the lowestenergy eigenstate of Ωef f · F [54, 126],
|ξ−1 i = e

i(θ+γ)

 iϕ
sin β
e
(1 − cos β) |−1i − √ |0i
2
2

e−iφ
+
(1 + cos β) |+1i , (34)
2

where θ + γ is the phase introduced by a gauge transformation. Then an azimuthal gauge potential is induced
by SOAM coupling, taking the form of A−1 = (~/r) cos β
under the choice of θ + γ = 0, which gives rise to an effective magnetic field experienced by atoms. The mag-

netic flux through the atomic cloud can be tuned via
the Raman detuning δ. This leads to a phase transition
of the SOAM-coupled ground state from one to another
QAM. In the experiment [54], it is demonstrated that
the QAM of the ground state changes from lg = ±1 to 0
as the Raman detuning |δ| continuously decreases. The
phase transition occurs at the critical Raman detuning
|δ| ≈ 2π × 210Hz as shown in Fig. 15(a). At a detuning
below the critical value, i.e., δ = 2π × 50Hz, the system
stays at the ground state with QAM lg = 0. The corresponding mechanical angular momenta of bare hyperfine
states |mF i are lmF = (1, 0, −1) for mF = (+1, 0, −1)
in the laboratory frame. The same hole sizes in the
|mF = +1i and |mF = −1i are observed in the experiment as shown in Fig. 15(a). At a detuning above the
critical value, i.e., δ = 2π × 400Hz, the SOAM-coupled
ground state transits to the state with QAM lg = 1,
which corresponds to the mechanical angular momenta of
bare hyperfine states lmF = (2, 1, 0) for mF = +1, 0, −1
in the laboratory frame. Then the vortex with larger
hole size in |mF = +1i, compared to that in |mF = −1i,
is anticipated and is experimentally confirmed.
Soon, the ground-state quantum phase diagram of
this SOAM-coupled system is comprehensively studied
in an effective spin-half 87 Rb atomic gas [55]. Due to a
larger quadratic Zeeman shift ωq = 2π × 5.52kHz compared to that of [53, 54], the third Zeeman hyperfine
state |F = 1, mF = +1i is far-off-resonant, and is then
dropped out from the problem. In addition, one of the
two Raman beams is operated in a higher LG mode with

16
a winding number l1 = −2. It gives rise to a rich groundstate phase diagram as presented in Fig. 16. The whole
system is therefore governed by the Hamiltonian (15) in
the presence of LG Raman beams, which introduces an
effective SOAM coupling L̂z σ̂z as seen in Eq. (17) after a
unitary transformation. Here, a tune-out wavelength of
LG beams is chosen [127]. It ensures that any observed
circular structure of atomic clouds is resulted from the
vortex formation due to the SOAM coupling, excluding
the trapping effect of the diagonal ac-stark potential χ (r)
of LG beams.
In order to explore the ground-state quantum phases
of the system, the Raman beams need to be introduced
adiabatically. After preparing the BEC in the hyperfine state |mF = −1i by setting a large detuning δ =
2π × 400kHz, the Raman beams are turned on. Then the
detuning δ is ramped to the desired value adiabatically.
This process keeps the system remaining in the ground
state all the time. Subsequently, the transitions between
different ground-state quantum phases could be studied
following different paths P1,2,3,4 as shown in Fig. 16(c).
For example, along the path P1 , the Raman coupling
strength is fixed at ΩR /~ω = 1604.5 in the unit of
harmonic energy, while the detuning δ adiabatically decreases across the phase boundary. The SOAM-coupled
system transits from the half-skyrmion phase with QAM
lz = 1 to the vortex-antivortex phase with QAM lz = 0.
The phase transition can experimentally be identified according to the change of density profiles of bare hyperfine states: the vortex structure exists only in the spin-↑
atomic cloud in the half-skyrmion phase, while both spin
states exhibit vortex formations in the vortex-antivortex
phase. The analogous procedures are performed along
the paths P2,3,4 .
The spin-resolved density profiles are presented in
Fig. 17 across different phase boundaries. To confirm the formation of vortices that the circular structures of atom clouds carry angular momenta, a resonant radio-frequency (rf) pulse is applied, that transfers
the atoms between internal Zeeman hyperfine states |↑i
and |↓i [128–130]. The appearance of the interference
pattern in each spin component during TOF, as shown
in Fig. 17, implies that the circular structures are indeed vortices before the rf transition. The spin polarization hσ̂z i = (N↑ − N↓ ) / (N↑ + N↓ ) is an additional
indicator of the phase transitions, which jumps among
hσ̂z i = 0, ±1 across different phase boundaries. Here,
N↑(↓) is the atom number for the spin-↑ (↓)component.
The spin polarization is presented as a function of the
two-photon detuning δ in Fig. 17. The evident jump
behavior during phase transitions is observed in the experiment even at finite temperatures. Regarding these
characteristic behaviors across the phase transitions, it
allows us to identify the boundaries of different groundstate quantum phases. Then the ground-state phase diagram is conveniently mapped out in the parameter space

(b)

(a)
݈ଶ ൌ Ͳ

x

y

݈ଵ ൌ െʹ

BEC

݈ଶ ൌ Ͳ
԰߱௭ 

B

ߜ Τʹ
ȁെͳۧ ൌ ȁ՝ۧ

ߜ Τʹ
ȁͲۧ ൌ ȁ՛ۧ
͵ߜ Τʹ ൅ʹ԰߱௤ 

z

(c)

_՛!
_՝!

݈ଵ ൌ െʹ

ȁ൅ͳۧ

lz=0
P1

P4
_՛!
_՝!

lz=-1

P3
P2

lz=1

_՛!
_՝!

Figure 16. Schematic of SOAM coupling. (a) Experimental
setup. (b) The energy diagram of Raman transition. The
hyperfine states |mF = 0i = |↑i and |mF = −1i = |↓i are
coupled by a pair of Raman beams, one of which is operated
in the LG mode with a winding number l1 = −2. The third
hyperfine state |mF = +1i is far-off-resonant due to a large
quadratic Zeeman shift ωq ≈ 2π ×5.52kHz. Here, δ is the twophoton detuning. (c) The ground-state phase diagram. Three
single-particle ground-state phases are characterized by the
QAM lz = 0, ±1. The corresponding lowest-band dispersion
as well as the typical density profiles is illustrated in the insets. Here, the phase transitions are studied in the experiment
following four typical paths P1,2,3,4 . Adapted From Ref. [55].

spanned by the detuning δ and the coupling strength ΩR ,
as illustrated in Fig. 18.

VII.

CONCLUSIONS AND OUTLOOKS

In conclusion, the most recent advances in both
the theories and experiments of spin-orbital-angularmomentum (SOAM) coupled quantum gases are briefly
summarized in this review. The basic idea of engineering
SOAM coupling in ultracold atoms is presented, and exotic quantum phases of Bose gases are introduced as well
as those of Fermi gases in the presence of SOAM coupling. In spite of remarkable progress in this field, it is
far from the end of the story. There could be further developments in SOAM-coupled quantum gases, since several issues still require more theoretical and experimental
efforts.
Few-body physics—As a building block of interacting
many-body systems, the few-body problem is of important significance in ultracold atoms. For instance, the
two-body physics determines the essential interaction parameter in the many-body Hamiltonian, and even dominates crucial quantum correlations in many-body systems, such as Tan’s relations [131–133]. Besides, the

17
Interfere

|՛>

25.8

20.7

50

-5.2

100

150

200

d/hw

1500

1.0

0

1000
0.5

|՛>

12.9

-6.5

-38.7

lz=-1

WR/hw=1134.5

lz=1

0.0
-0.5
-1.0
-100

|՝>

ࢾ
= 38.7
԰࣓

1

0

<s z>

P2

-0.5

-1.0

|՝>
ࢾ
= 51.6
԰࣓

< sz>

lz=0

2000

WR/hw=1604.5

WR/hw

P1

< s z>

0.0

500
-50

0

50

100

d/hw

-1

-40

-20

0

20

40

d/hw
0.0

d/hw=12.9

ષࡾ
=
԰࣓

P4

<sz>

-0.5

-1.0

|՝>

1220.8 1495.1 1614.9

500

1831.1

1000
1500
WR/hw

2000

1.0

|՛>

<s z>

P3

|՛>

0.5

d/hw=-12.9
0.0

|՝>

ષࡾ
= 1141.9 1431.5
԰࣓

1556.2 1779.5

Figure 18. The ground-state phase diagram of a SOAMcoupled condensate. Three quantum phases are characterized by QAMs lz = 0, ±1. The solid curves denote the phase
boundaries predicted by the mean-field theory, which are experimentally confirmed. The background color denotes the
spin polarization hσ̂z i. Adapted from Ref. [55].

1000

1500

2000

WR/hw

Figure 17. The spin-resolved density profiles after a 20ms
TOF expansion across different phase-transition boundaries
along four exemplary paths P1,2,3,4 (left panel), and the corresponding spin polarization hσ̂z i (right panel). The black
dashed (red solid) curve is the theoretical prediction at zero
temperature (at finite temperature T /Tc = 0.32). Adapted
from Ref. [55].

few-body problem itself displays intriguing features such
as the Feshbach resonance and Efimov effect. The fewbody problem has intensively been studied in spin-linearmomentum-coupled quantum gases [134–140], while the
theory for SOAM-coupled systems is still elusive to date.
Rich physics in this new few-body system is remained to
be discovered in near future, which could provide deep insight into many-body properties of SOAM-coupled quantum gases.
Finite-temperature phase diagrams—The current theory of SOAM-coupled quantum systems is constructed in
the framework of the zero-temperature mean-field theory.
For example, the ground-state quantum phases of Bose
gases are based on the solution of the Gross-Pitaevskii
equation, while the giant vortex Fermi superfluid is predicted by the zero-temperature Bogoliubov-de Gennes
formalism. The natural question arises whether these exotic quantum phases are stable enough against the thermal fluctuation at finite temperature as well as against
the quantum fluctuation at zero temperature beyond the

mean-field theory [58]. A more comprehensive theoretical
analysis is required to address these issues, and is necessary for the comparison with experimental observations
as well.
Experimental perspectives—The angular stripe phases
of SOAM-coupled Bose gases have not yet been observed in experiments. It is energetically favored for an
intraspecies interaction strength larger than the interspecies one (i.e., g↑↑ , g↓↓ > g↑↓ ). However, there is no
convenient Feshbach resonance of 87 Rb atoms to adjust
interactions. The angular stripe phase lies in a narrow
parameter window due to the small difference between
g↑↑ (or g↓↓ ) and g↑↓ for 87 Rb atomic gases. For this
reason, the 41 K atomic gas becomes one of the promising candidates for future experiments [60], in which the
interspecies scattering length can be tuned in a wide
range near the Feshbach resonance centered at the magnetic field B0 = 51.95G, while the intraspecies scattering
lengths are approximately constant. By choosing appropriately the interatomic scattering lengths, the window of
angular stripe phases in the parameter space is enlarged,
which can be operated easily in experiments [60].
Moreover, the SOAM coupling is not realized in Fermi
gases at present, which would provide a new platform
to investigate exotic vortex and topological superfluid
states. Other interesting directions, such as the nonequilibrium or the dynamics, BCS-BEC crossover, and
quantum fluctuations of Fermi gases with SOAM coupling are yet to be explored. All these fascinating and
remarkable phenomena are devoted to future studies.

18
VIII.

ACKNOWLEDGMENTS

We are grateful for inspiring discussions with TianYou Gao, Wei Yi and Fan Wu. SGP and KJ are
supported by the National Natural Science Foundation
of China under Grant Nos. 11974384 and 12121004,
the National Key R&D Program under Grant No.
2022YFA1404102, Chinese Academy of Sciences under
Grant No. YJKYYQ20170025, K. C. Wong Education Foundation under Grant No. GJTD-2019-15, and
the Natural Science Foundation of Hubei Province under Grant No. 2021CFA027. XLC is supported by the
Natural Science Foundation of China under Grant No.
12204413 and the Science Foundation of Zhejiang SciTech University under Grant No. 21062339-Y. KJC is
supported by the Natural Science Foundation of China
under Grant No. 12104406 and the Science Foundation of
Zhejiang Sci-Tech University under Grant No. 21062338Y. PZ is supported by the National Natural Science Foundation of China under Grant No. 11804177. LYH is supported by the National Key R&D Program under Grant
No. 2018YFA0306503.

[1] R. Barnes, Formation and Evolution of Exoplanets
(Wiley-VCH 2010).
[2] L. D. Landau and E. M. Lifshitz, Quantum mechanics
(Non-relativistic theory) (Butterworth-Heinemann, Oxford 2007).
[3] I. Talmi, Nuclear shell theory, (Academic Press 1963).
[4] X.-L. Qi and S.-C. Zhang, The quantum spin hall effect
and topological insulators, Physics Today 63, 33 (2010).
[5] I. Bloch, J. Dalibard, and W. Zwerger, Many-body
physics with ultracold gases, Rev. Mod. Phys. 80, 885
(2008).
[6] S. Giorgini, L. P. Pitaevskii, and S. Stringari, Theory of
ultracold atomic Fermi gases, Rev. Mod. Phys. 80, 1215
(2008).
[7] T. Kohler, K. Goral, and P. S. Julienne, Production of
cold molecules via magnetically tunable Feshbach resonances, Rev. Mod. Phys. 78, 1311 (2006).
[8] C. Chin, R. Grimm, P. Julienne, and E. Tiesinga, Feshbach resonances in ultracold gases, Rev. Mod. Phys. 82,
1225 (2010).
[9] C. Gross and I. Bloch, Quantum simulations with ultracold atoms in optical lattices, Science 357, 995 (2017).
[10] J. Dalibard, F. Gerbier, G. Juzeliunas, and P. Ohberg,
Colloquium: Artificial gauge potentials for neutral
atoms, Rev. Mod. Phys. 83, 1523 (2011).
[11] D. A. Abanin, E. Altman, I. Bloch, and M. Serbyn, Colloquium: Many-body localization, thermalization, and
entanglement, Rev. Mod. Phys. 91, 021001 (2019).
[12] X.-J. Liu, M. F. Borunda, X. Liu, and J. Sinova, Effect of Induced Spin-Orbit Coupling for Atoms via Laser
Fields, Phys. Rev. Lett. 102, 046402 (2009).
[13] Y.-J. Lin, K. Jimenez-Garcia, and I. B. Spielman, Spinorbit-coupled Bose-Einstein condensates, Nature 471,
83 (2011).

[14] R. A. Williams, L. J. LeBlanc, K. Jimenez-Garcia, M. C.
Beeler, A. R. Perry, W. D. Phillips, and I. B. Spielman,
Synthetic Partial Waves in Ultracold Atomic Collisions,
Science 335, 314 (2012).
[15] P.-J. Wang, Z- Q. Yu, Z.-K. Fu, J. Miao, L.-H. Huang,
S.-J. Chai, H. Zhai, and J. Zhang, Spin-orbit coupled
degenerate Fermi gases, Phys. Rev. Lett. 109, 095301
(2012).
[16] L. W. Cheuk, A. T. Sommer, Z. Hadzibabic, T. Yefsah,
W. S. Bakr, and M. W. Zwierlein, Spin-injection spectroscopy of a spin-orbit coupled Fermi gas, Phys. Rev.
Lett. 109, 095302 (2012).
[17] J.-Y. Zhang, S.-C. Ji, Z. Chen, L. Zhang, Z.-D. Du,
B. Yan, G.-S. Pan, B. Zhao, Y.-J. Deng, H. Zhai, S.
Chen, and J.-W. Pan, Collective Dipole Oscillations of
a Spin-Orbit Coupled Bose-Einstein Condensate, Phys.
Rev. Lett. 109, 115301 (2012).
[18] A. J. Olson, S.-J. Wang, R. J. Niffenegger, C.-H. Li,
C. H. Greene, and Y.-P. Chen, Tunable Landau-Zener
transitions in a spin-orbit-coupled Bose-Einstein condensate, Phys. Rev. A 90, 013616 (2014).
[19] Z.-K. Fu, L.-H. Huang, Z.-M. Meng, P.-J. Wang, L.
Zhang, S.-Z. Zhang, H. Zhai, P. Zhang, and J. Zhang,
Production of Feshbach molecules induced by spin-orbit
coupling in Fermi gases, Nat. Phys. 10, 110 (2014).
[20] S.-C. Ji, J.-Y. Zhang, L. Zhang, Z.-D. Du, W. Zheng, Y.J. Deng, H. Zhai, S. Chen, and J.-W. Pan, Experimental
determination of the finite-temperature phase diagram
of a spin-orbit coupled Bose gas, Nat. Phys. 10, 314
(2014).
[21] S.-C. Ji, L. Zhang, X.-T. Xu, Z. Wu, Y.-J. Deng, S.
Chen, and J.-W. Pan, Softening of Roton and Phonon
Modes in a Bose-Einstein Condensate with Spin-Orbit
Coupling, Phys. Rev. Lett. 114, 105301 (2015).
[22] C. Hamner, Y.-P. Zhang, M. A. Khamehchi, M. J.
Davis, and P. Engels, Spin-Orbit-Coupled Bose-Einstein
Condensates in a One-Dimensional Optical Lattice,
Phys. Rev. Lett. 114, 070401 (2015).
[23] K. Jimenez-Garcia, L. J. LeBlanc, R. A. Williams, M.
C. Beeler, C. Qu, M. Gong, C. Zhang, and I. B. Spielman, Tunable Spin-Orbit Coupling via Strong Driving in
Ultracold-Atom Systems, Phys. Rev. Lett. 114, 125301
(2015).
[24] N. Q. Burdick, Y.-J. Tang, and B. L. Lev, LongLived Spin-Orbit-Coupled Degenerate Dipolar Fermi
Gas, Phys. Rev. X 6, 031022 (2016).
[25] B. Song, C.-D. He, S.-C. Zhang, E. Hajiyev, W. Huang,
X.-J. Liu, and G. B. Jo, Spin-orbit-coupled two-electron
Fermi gases of ytterbium atoms, Phys. Rev. A 94,
061604 (2016).
[26] J.-R. Li, W.-J. Huang, B. Shteynas, S. Burchesky, F.
C. Top, E. Su, J. Lee, A. O. Jamison, and W. Ketterle,
Spin-Orbit Coupling and Spin Textures in Optical Superlattices, Phys. Rev. Lett. 117, 185301 (2016).
[27] L. F. Livi, G. Cappellini, M. Diem, L. Franchi, C. Clivati, M. Frittelli, F. Levi, D. Calonico, J. Catani, M. Inguscio, and L. Fallani, Synthetic Dimensions and SpinOrbit Coupling with an Optical Clock Transition, Phys.
Rev. Lett. 117, 220401 (2016).
[28] K. Osterloh, M. Baig, L. Santos, P. Zoller, and M.
Lewenstein, Cold atoms in non-Abelian gauge potentials: From the Hofstadter "Moth" to lattice gauge theory, Phys. Rev. Lett. 95, 010403 (2005).

19
[29] J. Ruseckas, G. Juzeliunas, P. Ohberg, and M. Fleischhauer, Non-Abelian gauge potentials for ultracold
atoms with degenerate dark states, Phys. Rev. Lett. 95,
010404 (2005).
[30] G. Juzeliunas, J. Ruseckas, and J. Dalibard, Generalized
Rashba-Dresselhaus spin-orbit coupling for cold atoms,
Phys. Rev. A 81, 053403 (2010).
[31] D. L. Campbell, G. Juzeliunas, and I. B. Spielman, Realistic Rashba and Dresselhaus spin-orbit coupling for
neutral atoms, Phys. Rev. A 84, 025602 (2011).
[32] J. D. Sau, R. Sensarma, S. Powell, I. B. Spielman, and
S. Das Sarma, Chiral Rashba spin textures in ultracold
Fermi gases, Phys. Rev. B 83, 140510 (2011).
[33] B. M. Anderson, I. B. Spielman, and G. Juzeliunas,
Magnetically Generated Spin-Orbit Coupling for Ultracold Atoms, Phys. Rev. Lett. 111, 125301 (2013).
[34] Z.-F. Xu, L. You, and M. Ueda, Atomic spin-orbit
coupling synthesized with magnetic-field-gradient pulses,
Phys. Rev. A 87, 063634 (2013).
[35] X.-J. Liu, K. T. Law, and T. K. Ng, Realization of 2D
Spin-Orbit Interaction and Exotic Topological Orders in
Cold Atoms, Phys. Rev. Lett. 112, 086401 (2014).
[36] B. M. Anderson, G. Juzeliunas, V. M. Galitski, and I.
B. Spielman, Synthetic 3D Spin-Orbit Coupling, Phys.
Rev. Lett. 108, 235301 (2012).
[37] Y. H. Lu, B. Z. Wang, and X. J. Liu, Ideal Weyl
semimetal with 3D spin-orbit coupled ultracold quantum
gas, Science Bulletin 65, 2080 (2020).
[38] B.-Z. Wang, Y.-H. Lu, W. Sun, S. Chen, Y.-J. Deng,
and X.-J. Liu, Dirac-, Rashba-, and Weyl-type spin-orbit
couplings: Toward experimental realization in ultracold
atoms, Phys. Rev. A 97, 011605 (2018).
[39] L.-H. Huang, Z.-M. Meng, P.-J. Wang, P. Peng, S.-L.
Zhang, L.-C. Chen, D.-H. Li, Q. Zhou, and J. Zhang,
Experimental realization of two-dimensional synthetic
spin-orbit coupling in ultracold Fermi gases, Nat. Phys.
12, 540 (2016).
[40] Z. Wu et al., Realization of two-dimensional spin-orbit
coupling for Bose-Einstein condensates, Science 354, 83
(2016).
[41] Z.-Y. Wang, X.-C. Cheng, B.-Z. Wang, J.-Y. Zhang, Y.H. Lu, C.-R. Yi, S. Niu, Y.-J. Deng, X.-J. Liu, S. Chen,
and J.-W. Pan, Realization of an ideal Weyl semimetal
band in a quantum gas with 3D spin-orbit coupling, Science 372, 271 (2021).
[42] H. Zhai, Spin-orbit coupled quantum gases, Int. J. Mod.
Phys. B 26, 1230001 (2012).
[43] H. Zhai, Degenerate quantum gases with spin-orbit coupling: A review, Rep. Prog. Phys. 78, 026001 (2015).
[44] L. Zhang, and X.-J. Liu, Spin-orbit coupling and topological phases for ultracold atoms, arXiv:1806.05628
(2018) (published book, Synthetic Spin-Orbit Coupling
in Cold Atoms, pp. 1-87 (2018) Chapter 1: Spin-orbit
Coupling and Topological Phases for Ultracold Atoms).
[45] X.-J. Liu, H. Jing, X. Liu, and M.-L. Ge, Generation of
two-flavor vortex atom laser from a five-state medium,
Eur. Phys. J. D 37, 261 (2006).
[46] M. DeMarco and H. Pu, Angular spin-orbit coupling in
cold atoms, Phys. Rev. A 91, 033630 (2015).
[47] K. Sun, C.-L. Qu, and C.-W. Zhang, Spin-orbitalangular-momentum coupling in Bose-Einstein condensates, Phys. Rev. A 91, 063627 (2015).
[48] C.-L. Qu, K. Sun, and C. W. Zhang, Quantum phases of
Bose-Einstein condensates with synthetic spin-orbital-

angular-momentum coupling, Phys. Rev. A 91, 053630
(2015).
[49] Y.-X. Hu, C. Miniatura, and B. Gremaud, Halfskyrmion and vortex-antivortex pairs in spinor condensates, Phys. Rev. A 92, 033615 (2015).
[50] L. Chen, H. Pu, and Y.-B. Zhang, Spin-orbit angular
momentum coupling in a spin-1 Bose-Einstein condensate, Phys. Rev. A 93, 13629 (2016).
[51] I. Vasic and A. Balaz, Excitation spectra of a BoseEinstein condensate with an angular spin-orbit coupling,
Phys. Rev. A 94, 033627 (2016).
[52] J.-P. Hou, X.-W. Luo, K. Sun, and C.-W. Zhang, Adiabatically tuning quantized supercurrents in an annular Bose-Einstein condensate, Phys. Rev. A 96, 011603
(2017).
[53] H. R. Chen et al., Spin-orbital-angular-momentum coupled Bose-Einstein condensates, Phys. Rev. Lett. 121,
113204 (2018).
[54] P. K. Chen, L. R. Liu, M. J. Tsai, N. C. Chiu, Y.
Kawaguchi, S. K. Yip, M. S. Chang, and Y. J. Lin,
Rotating atomic quantum gases with light-induced azimuthal gauge potentials and the observation of the
Hess-Fairbank effect, Phys. Rev. Lett. 121, 250401
(2018).
[55] D. Zhang et al., Ground-state phase diagram of a spinorbital-angular-momentum coupled Bose-Einstein condensate, Phys. Rev. Lett. 122, 110402 (2019).
[56] Y. Li, L. P. Pitaevskii, and S. Stringari, Quantum
tricriticality and phase transitions in spin-orbit coupled Bose-Einstein condensates, Phys. Rev. Lett. 108,
225301 (2012).
[57] G. I. Martone, Y. Li, L. P. Pitaevskii, and S. Stringari,
Anisotropic dynamics of a spin-orbit-coupled BoseEinstein condensate, Phys. Rev. A 86, 063621 (2012).
[58] X.-L. Chen, X.-J. Liu, and H. Hu, Quantum and thermal
fluctuations in a Raman spin-orbit-coupled Bose gas,
Phys. Rev. A 96, 013625 (2017).
[59] X.-L. Chen, J. Wang, Y. Li, X.-J. Liu, and H. Hu, Quantum depletion and superfluid density of a supersolid in
Raman spin-orbit-coupled Bose gases, Phys. Rev. A 98,
013614 (2018).
[60] X.-L. Chen, S.-G. Peng, P. Zou, X.-J. Liu, and H. Hu,
Angular stripe phase in spin-orbital-angular-momentum
coupled Bose condensates, Phys. Rev. Research 2,
033152 (2020).
[61] K.-J. Chen, F. Wu, J.-S. Hu, and L.-Y. He, Groundstate phase diagram and excitation spectrum of a
Bose-Einstein condensate with spin-orbital-angularmomentum coupling, Phys. Rev. A 102, 013316 (2020).
[62] Y. Duan, Y. M. Bidasyuk, and A. Surzhykov, Symmetry breaking and phase transitions in bose-einstein condensates with spin-orbital-angular-momentum coupling,
Phys. Rev. A 102, 063328 (2020).
[63] N. C. Chiu, Y. Kawaguchi, S. K. Yip, and Y. J. Lin,
Visible stripe phases in spin-orbital-angular-momentum
coupled Bose-Einstein condensates, New J. Phys. 22,
093017 (2020).
[64] Y. M. Bidasyuk, K. S. Kovtunenko, and O. O.
Prikhodko, Fine structure of the stripe phase in ringshaped Bose-Einstein condensates with spin-orbitalangular-momentum coupling, Phys. Rev. A 105, 023320
(2022).
[65] M. Boninsegni and N. V. Prokof’ev, Colloquium: Supersolids: What and where are they?, Rev. Mod. Phys.

20
84, 759 (2012).
[66] K.-J. Chen, F. Wu, S.-G. Peng, W. Yi, and L. He,
Generating giant vortex in a Fermi superfluid via spinorbital-angular-momentum coupling, Phys. Rev. Lett.
125, 260407 (2020).
[67] L.-L. Wang, A.-C. Ji, Q. Sun, and J. Li, Exotic vortex states with discrete rotational symmetry in atomic
Fermi gases with spin-orbital-angular-momentum coupling, Phys. Rev. Lett. 126, 193401 (2021).
[68] L. Dong, L. Jiang, H. Hu, and H. Pu, Finite-momentum
dimer bound state in a spin-orbit-coupled Fermi gas,
Phys. Rev. A 87, 043616 (2013).
[69] V. B. Shenoy, Flow-enhanced pairing and other unusual
effects in Fermi gases in synthetic gauge fields, Phys.
Rev. A 88, 033609 (2013).
[70] F. Wu, G.-C. Guo, W. Zhang, and W. Yi, Unconventional superfluid in a two-dimensional Fermi gas with
anisotropic spin-orbit coupling and Zeeman fields, Phys.
Rev. Lett. 110, 110401 (2013).
[71] C.-L. Qu, Z. Zheng, M. Gong, Y. Xu, L. Mao, X.-B. Zou,
G.-C. Guo, and C.-W. Zhang, Topological superfluids
with finite-momentum pairing and Majorana fermions,
Nat. Comm. 4, 2710 (2013).
[72] W. Zhang and W. Yi, Topological Fulde-Ferrell-LarkinOvchinnikov states in spin-orbit-coupled Fermi gases,
Nat. Comm. 4, 2711 (2013).
[73] C. Chen, Inhomogeneous topological superfluidity in
one-dimensional spin-orbit-coupled Fermi gases, Phys.
Rev. Lett. 111, 235302 (2013).
[74] X.-J. Liu and H. Hu, Topological Fulde-Ferrell superfluid
in spin-orbit-coupled atomic Fermi gases, Phys. Rev. A
88, 023622 (2013).
[75] R. Sensarma, M. Randeria, and T. L. Ho, Vortices in superfluid Fermi gases through the BEC to BCS crossover,
Phys. Rev. Lett. 96, 090403 (2006).
[76] C.-C. Chien, Y. He, Q.-J. Chen, and K. Levin, Groundstate description of a single vortex in an atomic Fermi
gas: From BCS to Bose-Einstein condensation, Phys.
Rev. A 73, 041603 (2006).
[77] C. Caroli, P. G. Degennes, and J. Matricon, Bound
fermion states on a vortex line in a type-II superconductor, Phys. Lett. 9, 307 (1964).
[78] K.-J. Chen, F. Wu, L. He, and W. Yi, Angular topological superfluid and topological vortex in an ultracold
Fermi gas, Phys. Rev. Research 4, 033023 (2022).
[79] R. A. Williams, M. C. Beeler, L. J. LeBlanc, K. JimenezGarcia, and I. B. Spielman, Raman-induced interactions
in a single-component Fermi gas near an s-wave Feshbach resonance, Phys. Rev. Lett. 111, 095301 (2013).
[80] Y. Han, S.-G. Peng, K.-J. Chen, and W. Yi, Molecular state in a spin-orbital-angular-momentum coupled
Fermi gas, Phys. Rev. A 106, 043302 (2022).
[81] M. O. Scully and M. S. Zubairy, Quantum optics (Cambridge University Press, 2008).
[82] K. P. Marzlin, W.-P. Zhang, and E. M. Wright, Vortex coupler for atomic Bose-Einstein condensates, Phys.
Rev. Lett. 79, 4728 (1997).
[83] W. F. Holmgren, R. Trubko, I. Hromada, and A. D.
Cronin, Measurement of a wavelength of light for which
the energy shift for an atom vanishes, Phys. Rev. Lett.
109, 243004 (2012).
[84] C. D. Herold, V. D. Vaidya, X. Li, S. L. Rolston, J.
V. Porto, and M. S. Safronova, Precision measurement
of transition matrix elements via light shift cancellation,

Phys. Rev. Lett. 109, 243003 (2012).
[85] H. Hu, B. Ramachandhran, H. Pu, and X.-J. Liu, Spinorbit coupled weakly interacting Bose-Einstein condensates in harmonic traps, Phys. Rev. Lett. 108, 010402
(2012).
[86] B. Ramachandhran, B. Opanchuk, X.-J. Liu, H. Pu, P.
D. Drummond, and H. Hu, Half-quantum vortex state
in a spin-orbit-coupled Bose-Einstein condensate, Phys.
Rev. A 85, 023606 (2012).
[87] L. S. Leslie, A. Hansen, K. C. Wright, B. M. Deutsch,
and N. P. Bigelow, Creation and detection of skyrmions
in a Bose-Einstein condensate, Phys. Rev. Lett. 103,
250401 (2009).
[88] B. Binz and A. Vishwanath, Chirality induced
anomalous-hall effect in helical spin crystals, Physica
B Condens. Matter 403, 1336 (2008).
[89] S. Muhlbauer, B. Binz, F. Jonietz, C. Pfleiderer, A.
Rosch, A. Neubauer, R. Georgii, and P. Boni, Skyrmion
lattice in a chiral magnet, Science 323, 915 (2009).
[90] Y.-J. Lin, R. L. Compton, K. Jimenez-Garcia, J. V.
Porto, and I. B. Spielman, Synthetic magnetic fields for
ultracold atoms, Nature 462, 627 (2009).
[91] Y.-J. Lin, R. L. Compton, A. R. Perry, W. D. Phillips, J.
V. Porto, I. B. Spielman, and B. Collaboration, BoseEinstein condensate in a uniform light-induced vector
potential, Phys. Rev. Lett. 102, 130401 (2009).
[92] R. Dum and M. Olshanii, Gauge structures in atomlaser interaction: Bloch oscillations in a dark lattice,
Phys. Rev. Lett. 76, 1788 (1996).
[93] P. M. Visser and G. Nienhuis, Geometric potentials for
subrecoil dynamics, Phys. Rev. A 57, 4581 (1998).
[94] S.-L. Zhu, H. Fu, C.-J. Wu, S.-C. Zhang, and L.-M.
Duan, Spin Hall effects for cold atoms in a light-induced
gauge potential, Phys. Rev. Lett. 97, 240401 (2006).
[95] X.-J. Liu, X. Liu, L. C. Kwek, and C. H. Oh, Optically
induced spin-Hall effect in atoms, Phys. Rev. Lett. 98,
026602 (2007).
[96] M. C. Beeler, R. A. Williams, K. Jimenez-Garcia, L. J.
LeBlanc, A. R. Perry, and I. B. Spielman, The spin Hall
effect in a quantum gas, Nature 498, 201 (2013).
[97] C. Wang, C. Gao, C.-M. Jian, and H. Zhai, Spin-Orbit
Coupled Spinor Bose-Einstein Condensates, Phys. Rev.
Lett. 105, 160403 (2010).
[98] C.-J. Wu, I. Mondragon-Shem, and X.-F. Zhou, Unconventional Bose-Einstein Condensations from Spin-Orbit
Coupling, Chin. Phys. Lett. 28, 097102 (2011).
[99] T.-L. Ho and S. Zhang, Bose-Einstein Condensates with
Spin-Orbit Interaction, Phys. Rev. Lett. 107, 150403
(2011).
[100] J. Léonard, A. Morales, P. Zupancic, T. Esslinger,
and T. Donner, Supersolid formation in a quantum gas
breaking a continuous translational symmetry, Nature
543, 87 (2017).
[101] J.-R. Li, J. Lee, W. Huang, S. Burchesky, B. Shteynas,
F. C. Top, A. O. Jamison, and W. Ketterle, A stripe
phase with supersolid properties in spin–orbit-coupled
Bose–Einstein condensates, Nature 543, 91 (2017).
[102] L. Tanzi, E. Lucioni, F. Famá, J. Catani, A. Fioretti, C.
Gabbanini, R. N. Bisset, L. Santos, and G. Modugno,
Observation of a Dipolar Quantum Gas with Metastable
Supersolid Properties, Phys. Rev. Lett. 122, 130405
(2019).
[103] F. Böttcher, J.-N. Schmidt, M. Wenzel, J. Hertkorn,
M. Guo, T. Langen, and T. Pfau, Transient Supersolid

21
Properties in an Array of Dipolar Quantum Droplets,
Phys. Rev. X 9, 011051 (2019).
[104] L. Chomaz, D. Petter, P. Ilzhöfer, G. Natale, A. Trautmann, C. Politi, G. Durastante, R. M. W. van Bijnen, A.
Patscheider, M. Sohmen, M. J. Mark, and F. Ferlaino,
Long-Lived and Transient Supersolid Behaviors in Dipolar Quantum Gases, Phys. Rev. X 9, 021012 (2019).
[105] M. A. Norcia, C. Politi, L. Klaus, E. Poli, M. Sohmen,
M. J. Mark, R. N. Bisset, L. Santos, and F. Ferlaino, Two-dimensional supersolidity in a dipolar quantum gas, Nature 596, 357 (2021).
[106] M. Lysebo and L. Veseth, Feshbach resonances and transition rates for cold homonuclear collisions between 39 K
and 41 K atoms, Phys. Rev. A 81, 032702 (2010).
[107] L. Tanzi, C. R. Cabrera, J. Sanz, P. Cheiney, M. Tomza,
and L. Tarruell, Feshbach resonances in potassium BoseBose mixtures, Phys. Rev. A 98, 062712 (2018).
[108] P. Fulde and R. A. Ferrell, Superconductivity in a Strong
Spin-Exchange Field, Phys. Rev. 135, A550 (1964).
[109] A. I. Larkin and Y. N. Ovchinnikov, Nonuniform State
of Superconductors, Sov. Phys. JETP 20, 762 (1965).
[110] X.-J. Liu, Z.-X. Liu, and M. Cheng, Manipulating Topological Edge Spins in a One-Dimensional Optical Lattice, Phys. Rev. Lett. 110, 076401 (2013).
[111] X.-J. Liu, K.T. Law, and T.K. Ng, Realization of 2D
Spin-Orbit Interaction and Exotic Topological Orders in
Cold Atoms, Phys. Rev. Lett. 112, 086401 (2014).
[112] Z. Meng, L. Huang, P. Peng, D. Li, L. Chen, Y. Xu,
C. Zhang, P. Wang, and J. Zhang, Experimental Observation of a Topological Band Gap Opening in Ultracold Fermi Gases with Two-Dimensional Spin-Orbit
Coupling, Phys. Rev. Lett. 117, 235304 (2016).
[113] L. Fu and C. L. Kane, Superconducting Proximity Effect
and Majorana Fermions at the Surface of a Topological
Insulator, Phys. Rev. Lett. 100, 096407 (2008).
[114] J. D. Sau, R. M. Lutchyn, S. Tewari, and S. Das Sarma,
Generic New Platform for Topological Quantum Computation Using Semiconductor Heterostructures, Phys.
Rev. Lett. 104, 040502 (2010).
[115] J. Alicea, Majorana fermions in a tunable semiconductor device, Phys. Rev. B 81. 125318 (2010).
[116] Y. Oreg, G. Refael, and F. von Oppen, Helical Liquids
and Majorana Bound States in Quantum Wires, Phys.
Rev. Lett. 105, 177002 (2010).
[117] L. Mao, J. Shi, Q. Niu, and C. Zhang, Superconducting Phase with a Chiral f-Wave Pairing Symmetry and
Majorana Fermions Induced in a hole-doped Semiconductor, Phys. Rev. Lett. 106, 157003 (2011).
[118] S. Tewari, T. D. Stanescu, J. D. Sau, and S. Das Sarma,
Topologically non-trivial superconductivity in spin-orbitcoupled systems: bulk phases and quantum phase transitions, New J. Phys. 13, 065004 (2011).
[119] J. Zhou, W. Zhang, and W. Yi, Topological superfluid
in a trapped two-dimensional polarized Fermi gas with
spin-orbit coupling, Phys. Rev. A 84, 063603 (2011).
[120] Y. S. Rumala and A. E. Leanhardt, Optical vortex with
a small core and Gaussian intensity envelope for lightmatter interaction, J. Opt. Soc. Am. B 34, 909 (2017).
[121] J.-L. Qin, G.-J. Dong, and B. A. Malomed, Stable giant
vortex annuli in microwave-coupled atomic condensates,

Phys. Rev. A 94, 053611 (2016).
[122] X. Cui, B. Lian, T.-L. Ho, B. L. Lev, and H. Zhai, Synthetic gauge field with highly magnetic lanthanide atoms,
Phys. Rev. A 88, 011601(R) (2013).
[123] W. Yi and G.-C. Guo, Phase separation in a polarized
Fermi gas with spin-orbit coupling, Phys. Rev. A 84,
031608(R) (2011).
[124] G. B. Hess and W. M. Fairbank, Measurements of Angular Momentum in Superfluid Helium, Phys. Rev. Lett.
19, 216 (1967).
[125] R. Ishiguro, O. Ishikawa, M. Yamashita, Y. Sasaki, K.
Fukuda, M. Kubota, H. Ishimoto, R. E. Packard, T.
Takagi, T. Ohmi, and T. Mizusaki, Vortex Formation
and Annihilation in Three Textures of Rotating Superfluid 3 He-A, Phys. Rev. Lett. 93, 125301 (2004).
[126] T.-L. Ho, Spinor Bose Condensates in Optical Traps,
Phys. Rev. Lett. 81, 742 (1998).
[127] F. Schmidt, D. Mayer, M. Hohmann, T. Lausch, F. Kindermann, and A. Widera, Precision measurement of the
87
Rb tune-out wavelength in the hyperfine ground state
F = 1 at 790 nm, Phys. Rev. A 93, 022507 (2016).
[128] M. R. Matthews, B. P. Anderson, P. C. Haljan, D. S.
Hall, C. E. Wieman, and E. A. Cornell, Vortices in a
Bose-Einstein condensate, Phys. Rev. Lett. 83, 2498
(1999).
[129] M. F. Andersen, C. Ryu, P. Clade, V. Natarajan, A.
Vaziri, K. Helmerson, and W. D. Phillips, Quantized
rotation of atoms from photons with orbital angular momentum, Phys. Rev. Lett. 97, 170406 (2006).
[130] K. C. Wright, L. S. Leslie, A. Hansen, and N. P. Bigelow,
Sculpting the Vortex State of a Spinor BEC, Phys. Rev.
Lett. 102, 030405 (2009).
[131] S. Tan, Energetics of a strongly correlated Fermi gas,
Ann. Phys. 323, 2952 (2008).
[132] S. Tan, Large momentum part of a strongly correlated
Fermi gas, Ann. Phys. 323, 2971 (2008).
[133] S. Tan, Generalized virial theorem and pressure relation
for a strongly correlated Fermi gas, Ann. Phys. 323,
2987 (2008).
[134] X.-L. Cui, Mixed-partial-wave scattering with spin-orbit
coupling and validity of pseudopotentials, Phys. Rev. A
85, 022705 (2012).
[135] P. Zhang, L. Zhang, and Y. J. Deng, Modified BethePeierls boundary condition for ultracold atoms with
spin-orbit coupling, Phys. Rev. A 86, 053608 (2012).
[136] X.-L. Cui and W. Yi, Universal Borromean Binding in
Spin-Orbit-Coupled Ultracold Fermi Gases, Phys. Rev.
X 4, 031026 (2014).
[137] Z.-Y. Shi, X.-L. Cui, and H. Zhai, Universal Trimers Induced by Spin-Orbit Coupling in Ultracold Fermi Gases,
Phys. Rev. Lett. 112, 013201 (2014).
[138] S.-G. Peng, C.-X. Zhang, S. Tan, and K. Jiang, Contact
Theory for Spin-Orbit-Coupled Fermi Gases, Phys. Rev.
Lett. 120, 060408 (2018).
[139] C.-X. Zhang, S.-G. Peng, and K.-J. Jiang, Universal
relations for spin-orbit-coupled Fermi gases in two and
three dimensions, Phys. Rev. A 101, 043616 (2020).
[140] C.-X. Zhang and S.-G. Peng, Universal scattering phase
shift in the presence of spin-orbit coupling, Phys. Rev.
Research 3, 013054 (2021).


Fractionalized Altermagnets:
from neighboring and altermagnetic spin-liquids to spin-symmetric band splitting
João Augusto Sobral,1 Subrata Mandal,1 and Mathias S. Scheurer1
Institute for Theoretical Physics III, University of Stuttgart, 70550 Stuttgart, Germany

We study quantum-fluctuation-driven fractionalized phases in the vicinity of altermagnetic order.
First, the long-range magnetic orders in the vicinity of collinear altermagnetism are identified; these
feature a non-coplanar “orbital altermagnet” which has altermagnetic symmetries in spin-rotation
invariant observables. We then describe neighboring fractionalized phases with topological order
reached when quantum fluctuations destroy long-range spin order, within Schwinger-boson theory
and an SU(2) gauge theory of fluctuating magnetism. Discrete symmetries remain broken in some
of the fractionalized phases, with the orbital altermagnet becoming an “altermagnetic spin liquid”.
We compute the electronic spectral function in the doped system, which is characterized by split
Fermi surfaces with preserved spin-rotation symmetry.

I.

INTRODUCTION

In the last few years, there has been an increasing
amount of research on “altermagnets” (AMs) [1–68]. Unlike antiferromagnets, the total magnetic moment in AMs
does not vanish as a result of translations combined
with time-reversal (Θ) symmetry but, instead, due to
the product Θg where g is a point-group symmetry, e.g.,
four-fold rotational symmetry g = C4z on the square lattice [2]. While many of the above mentioned studies deal
with the non-trivial impact of altermagnetic moments on
quantum physics, e.g., on the electronic band structure
or on the properties of superconductivity, studying the
impact of quantum fluctuations on the altermagnetic order itself is far less explored. In this work, we address
the regime of strong quantum fluctuations which restore
spin-rotation (SR) invariance in AMs and in other neighboring non-trivial magnetic orders, both in insulators and
metallic phases. This is also relevant in light of recent experiments that indicate the interplay between altermagnetism and frustration for thin films of Mn5 Si3 [69, 70]
and CsCr3 Sb [49].
More specifically, we start from magnetically ordered
phases close to a square-lattice AM in a checkerboard
Heisenberg model [42, 45, 71–79] supplemented by ringexchange terms. Apart from the collinear AM and other
non-collinear states that preserve all symmetries modulo
SRs (i.e., will appear symmetric in SR-invariant observables), there are also nematic spin orders and an orbital
AM. The last phase, which is connected to the collinear
AM by a second-order phase transition in our model, is
characterized by scalar spin chiralities which are staggered on the lattice in a way that preserves ΘC4z and
translation, akin to the spin order of the prototypical
AM. We characterize the associated spin-liquid phases
obtained by “quantum melting” any of these magnetic
orders. We present Schwinger-Boson (SB) [72, 80–84]
ansätze for each of them and demonstrate that these
spin liquids inherit discrete broken symmetries. Most

notably, the orbital AM becomes an altermagnetic spinliquid which is characterized by the same altermagnetic
spatial arrangement of scalar spin chiralities. Finally,
we supplement this with an SU(2) gauge theory [85–92],
which allows us to generalize these fractionalized orders
to the doped system. Remarkably, the spectral function
of the itinerant electrons exhibits peaks similar to the
spin-splitting in AMs, while maintaining SR invariance.

II.

CLASSICAL PHASE DIAGRAM

Although the concepts are more general, we start, for
concreteness, our discussion with a minimal Heisenberg
model. To be able to capture AMs, we need two sublattices (A, B) per unit cell, which we place on the bonds
of a square lattice, see Fig. 1(a). Denoting the spin operators on bond i by Ŝ i , the Hamiltonian reads as
H = J1

X
⟨i,j⟩

+K

Ŝ i · Ŝ j + J2

X

Ŝ i · Ŝ j

(1)

⟨⟨i,j⟩⟩


 

i
X h
Ŝ i · Ŝ j Ŝ k · Ŝ l + Ŝ i · Ŝ l Ŝ k · Ŝ j .
k
j

□

arXiv:2410.10949v2 [cond-mat.str-el] 16 May 2025

1

l

i

If we only included the first term—the nearest-neighbor
exchange interaction, which we choose to obey J1 > 0
here—the model would become identical to a squarelattice antiferromagnet (with the lattice rotated by 45◦ ).
Adding the next-nearest neighbor couplings J2 (solid
blue lines in Fig. 1a) leads to the checkerboard model
[42, 45, 71–79]. To lift degeneracies and stabilize additional phases, we further include the ring exchange term
in the second line of Eq. (1); it couples any four spins,
i, j, k, l, on bonds with a common vertex in a way that
preserves the C4v point group symmetries, time-reversal
Θ, SR, as well as Bravais-lattice translational symmetry.
We first analyze the magnetic phases in the classical

2
global SRs, all magnetic point-group symmetries are preserved, which will also play an important role to our
later discussion of nearby spin liquids. Since this implies that all SR-invariant observables must also respect
all symmetries of our model, we can conveniently probe
these symmetries using the nearest neighbor scalar and
(anti-clockwise) triple products S EP = (S 1 · S 2 , S 2 ·
S 3 , S 3 · S 4 , S 4 · S 1 )T and χEP = (S 1 · (S 2 × S 3 ) ,
T
S 2 · (S 3 × S 4 ) , S 3 · (S 4 × S 1 ) , S 4 · (S 1 × S 2 )) , respectively, where the sites are labeled as in Fig. 1(a).
Indeed, we can see from Table I that all components of
S EP are identical (isotropic/non-nematic) and χEP = 0
(preserved Θ/non-chiral).

FIG. 1: (a) Bravais lattice (black squares), spins (red, orange
sublattices), and couplings J1 , J2 and K of the model (1).
(b) Classical phase diagram, with the corresponding phases
defined in (c) and Table I. (d) Nearest-neighbor spin products
S EP and (e) scalar spin chiralities χEP along two different
one-dimensional cuts through (b). The background coloring
in (d-e) refers to |S 1 · S 2 | as defined in the colorbar in (b).

limit and make the ansatz
S ℓ (R) ∝ â cos(Q · R − φℓ ) + b̂ sin(Q · R − φℓ ) + ĉ ηℓ , (2)
for the direction of the magnetization on sublattice ℓ =
A, B in square-lattice unit cell R; here â, b̂, ĉ are three
arbitrary three-component orthonormal vectors. Without loss of generality, we set φA = 0 and φB ≡ φ and
minimize the classical energy with respect to the variational parameters {Qx , Qy , φ, ηA , ηB } (see Appendix A).
In agreement with the nearest-neighbor square-lattice
antiferromagnet model, the system favors an antiparallel alignment of the spins on the two sublattices,
S A (R) = −S B (R) = â, for small K and J2 , see
phase A1 in Fig. 1(b,c). Importantly, though, finite
K and J2 in Eq. (1) break the artificial translational
symmetry at J2 = K = 0 relating the two sublattices A and B; instead, they are related by a C4z
rotational symmetry in the full model, making A1 a
collinear AM. It has vanishing total magnetization, M =
P
Modulo
R,ℓ S ℓ (R) = 0, as guaranteed by C4z Θ.

Turning on sufficiently large K > 0, it becomes energetically favorable to reduce the magnitude of the
nearest-neighbor spin products, by developing a finite
canting. This leads to the second-order phase transition into the canted AM (A2 ), S A,B (R) = ±â + ηĉ, see
Fig. 1(b-d). As summarized in Table I, this leads to a finite magnetization M ̸= 0 while the symmetries (modulo
SR) are identical to those of A1 . In the phase diagram
in Fig. 1(b), there is one more fully symmetric phase,
denoted by A3 ; the sufficiently large J2 leads to finite
Qx,y = π while positive K favors perpendicular spins in
the two sublattices (φ = π/2), see Fig. 1(c). As a result of
translational symmetry the magnetization vanishes, and
the state can be thought of as an antiferromagnet with
four spins in the enlarged unit cell.
Furthermore, the phase diagram contains two nematic
phases, denoted by B1,2 which break C4z rotational symmetry in SR-invariant observables while retaining Θ symmetry, see Fig. 1(c) and Table I. The phase B1 is reached
via a first-order transition from A3 by reversing the sign
of K leading to parallel spins in the unit cell (φ = 0).
Meanwhile B2 is stabilized when K > 0 dominates the
energetics leading to a phase with only one of Qx , Qy
non-zero (and equal to π).
Finally, in the most frustrated region of the phase diagram in Fig. 1(b), a non-coplanar phase (C) is stabilized. As can be seen in Fig. 1(e), this state is reached
from the collinear AM A1 via a second-order phase transition, where the scalar spin chiralities become non-zero,
breaking Θ in SR-invariant observables. Importantly, the
chiralities are staggered, χEP ∝ (−1, 1, −1, 1), in a way
that preserves C4z Θ (and σv Θ). As such, phase C behaves like an AM in SR-invariant observables, i.e., is associated with (when adding charge carriers, see Sec. IV
below) a special arrangement of orbital currents [90, 92–
94], where the corresponding orbital magnetic moments
are finite locally but vanish globally — not as a result of
translational symmetry but due to C4z Θ. For this reason,
we refer to phase C as an “orbital AM” [38].

3
TABLE I: Summary of the magnetic phases for the spin model (1). We list one possible set of parameters for Eq. (2) and the
values of S EP , χEP (s0 , s′0 , ξ0 ∈ R+ are non-universal parameters depending on the couplings). We further indicate whether
the total magnetization M is finite and the magnetic point symmetries of spin-rotation-invariant observables (through their
generators); these are also the symmetries of the associated spin liquids in Fig. 2 and the itinerant fractionalized phases with
topological order discussed below. The invariant gauge group (IGG) of these two descriptions coincide and are listed in the
last column.
Label
A1

Type
collinear AM (isotropic, non-chiral)

S EP
− (1, 1, 1, 1)

χEP
(0, 0, 0, 0)

A2

canted AM (isotropic, non-chiral)

− (s0 , s0 , s0 , s0 )

(0, 0, 0, 0)

(0, 0, π, η, η)

̸= 0 C4z , σv , Θ

Z2

A3

orthogonal AFM (isotropic, non-chiral)

(0, 0, 0, 0)

(0, 0, 0, 0)

(π, π, π/2, 0, 0)

0

C4z , σv , Θ

Z2

B1

collinear nematic (non-chiral)

(−1, 1, −1, 1)

(0, 0, 0, 0)

(π, π, 0, 0, 0)

0

C2z , σd

U(1)

B2

collinear odd parity (non-chiral)

(1, 1, −1, −1)

(0, 0, 0, 0)

(π, 0, 0, 0, 0)

0

σv , Θ

U(1)

(π, π, π/2, η, −η)

0

C4z Θ, σv Θ

Z2

C

orbital AM (isotropic, staggered chirality) − (s′0 , s′0 , s′0 , s′0 ) (−ξ0 , ξ0 , −ξ0 , ξ0 )

III.

NEARBY SPIN LIQUIDS

Having established the classical phase diagram, we
next discuss spin-liquid phases that can be reached from
the respective magnetically ordered phases once quantum
fluctuations restore SR invariance. To this end, we will
first use a SB description [80, 81] where the spin operators
in Eq. (1) are rewritten as Ŝ i = b̂†iσ σ σσ′ b̂iσ′ /2, introducing a local U(1) gauge redundancy, b̂j,σ → eiϕj b̂j,σ ; here
σ are Pauli matrices and b̂i,σ canonical bosons. Since
this enlarges the Hilbert space of spin-S operators, the
local constraint n̂i = 2S, n̂i = b̂†iσ b̂iσ , is imposed. Decoupling the resulting boson-boson interactions in the spin
Hamiltonian, leads to a free boson Hamiltonian
Hb =

X
1X ∗
(Bij b̂iσ b̂†jσ − A∗ij σ b̂iσ b̂j−σ + H.c.) − µ
n̂i ,
2 i,j
i

where Aij , Bij ∈ C can be computed within selfconsistent mean-field theory; the same applies for the
Lagrange multiplier µ introduced to treat the local constraint on average. However, as this mean-field approach
is typically not quantitatively reliable, we here take a
different perspective: we systematically study possible
ansätze for Aij , Bij , starting with only nearest-neighbor
terms and adding further-neighbor couplings until we find
a spin-liquid where Bose condensation (see Appendix B).
leads to a (apart from global SRs) unique magnetic
ground state that is identical to one of the phases in
Fig. 1(b) and Table I; in this way, we can associate a
spin-liquid with each of these magnetic phases.
For all of them, restricting the model to nearest and
next-nearest-neighbor bonds i, j in Aij , Bij which (upon
proper gauge choice) do not increase the unit cell turns
out to be sufficient. We define all of these ansätze diagrammatically in Fig. 2. For instance, we see that
the ansatz for A1 only involves Aij on nearest-neighbor

(Qx , Qy , φ, ηA , ηB ) M Symmetries IGG
(0, 0, π, 0, 0)
0 C4z , σv , Θ U(1)

bonds. Being left invariant by a U(1) gauge transformation consisting of phases of alternating signs in the two
sublattices, it is a U(1) spin liquid. It is straightforward
to show that the ansatz is invariant (modulo gauge transformations) under all symmetries of the model (1), which
we also demonstrated by computing the expectation values of S EP and χEP in the spin-liquid phase: indeed,
as also indicated in Fig. 2, we get ⟨S EP
l ⟩ = const and
⟨χEP ⟩ = 0.

-1

1

-1

1

FIG. 2: Diagrammatic definition of the Schwinger-Boson ansätze, where blue (black and grey) arrows indicate real Aij
(imaginary and real Bij ) on the respective bonds, for the spinliquids associated with the magnetic phases in Fig. 1(b,c). We
further indicate the expectation values of S EP using colored
ellipses and, for phase C, of χEP (only showing two triple
products in each of the nearest two unit cells for clarity) in
the respective spin liquids. The patterns extend through the
entire lattice.

The ansatz for A2 has additional imaginary Bij on
nearest neighbor bonds, which not only control the canting in the associated magnetically ordered phase but also
lead to a Z2 spin liquid. Just as the ansatz for A1 ,
this Z2 spin liquid also respects all symmetries of the
Hamiltonian. Also for the third magnetic phase, A3 ,
which respects all symmetries modulo SRs, the associ-

4
ated SB ansatz, now with second-nearest-neighbor terms,
see Fig. 2, leads to a fully symmetric Z2 spin liquid.
In contrast, the spin liquids associated with the remaining phases have reduced symmetries. As one would
expect, the spin liquids of the nematic magnetic phases
B1,2 are nematic themselves: as can be seen from the correlators ⟨S EP ⟩ shown along with the ansätze in Fig. 2 and
upon noting that still ⟨χEP ⟩ = 0 (Θ is not broken), they
obey the exact same symmetries as listed in Table I for
B1,2 . Finally, the spin liquid associated with the orbital
AM also has reduced symmetries: we find isotropic correlators ⟨S EP
l ⟩ = const but staggered scalar spin chiralities
⟨χEP ⟩ ∝ (−1, 1, −1, 1); while SR invariance is restored,
the altermagnetic arrangement of orbital moments (being
translation invariant but odd under C4z ) survive in the
neighboring spin-liquid phase, which can thus be thought
of as an “altermagnetic spin liquid”. This phase hosts vison excitations associated with local distortions of the
magnetization pattern [95] that could be detected with
local experimental probes [96].

IV.

FRACTIONALIZED ITINERANT SYSTEMS

One of the central aspects of AMs is their impact on the
spectrum of itinerant electrons, creating a momentumdependent spin splitting of their bands. We here address
the related question but in the regime where the spin
degrees of freedom are in a spin-liquid state. To this
end, we assume that mobile electrons are added to the
model studied above which we describe by the creation
operators ĉ†R,ℓ,σ of spin-σ electrons on the bond (R, ℓ)
in Fig. 1(a). We include nearest (t1 ) and next-nearestneighbor (t2 ) hopping [19] and couple the electrons locally to the magnetic moments ΦR,ℓ as
Z
Sc =

dτ

X †
cR,ℓ,σ σ σ,σ′ cR,ℓ,σ′ · ΦR,ℓ

(3)

R,ℓ

where we switched to a path integral description with
imaginary time τ (see Appendix C for more details). Assuming non-fluctuating long-range order, ΦR,ℓ → S ℓ (R),
and taking, e.g., the collinear AM order S A,B (R) = ±êz
of phase A1 , we obtain the bands and Fermi surface
with the characteristic spin splitting of AMs shown in
Fig. 3(a,b).
To describe the regime of strong quantum fluctuations, where SR invariance is restored, we employ the
approach of Refs. 85–92, where a transformation into
a rotating reference frame in spin space is performed
using the dynamical bosonic SU(2) matrices R(τ ) in
cR,ℓ,σ (τ ) = [RR,ℓ (τ )]σ,α ψR,ℓ,α (τ ). Physically, R capture
the spin degrees of freedom and are directly related to
the bosons in our SB approach above, while the charge
is carried by the fermionic “chargons” ψ. This rewriting

(a) 4

(b)

(c)

2
0

0
-2
0

(d)

0

(e)

(f)
max

25
20
15
10
5

min

FIG. 3: Band structure (a) along the ky = 0 line and (b) Fermi
surfaces for the long-range A1 order. The electronic Green’s
function is a convolution (c) of the chargon and spinon Green’s
function. (d) Electronic spectral function in the presence of
long-range order (Aσk (ω), left) and in the fractionalized phase
with spin-rotation invariance and topological order (Ak (ω),
right) at k = (π, 0). In (e) and (f), the spectral function
in the fractionalized phase is shown at ω = 0 as a function
of momentum k and as a function of energy ω and kx at
ky = 0, respectively. We use t2 /t1 = 0.3, chemical potential
µ/t1 = −1.2, H0 /t1 = 1, temperature T /t1 = 0.1, and a lifetime broadening of η/t1 = 0.05.

introduces a local SU(2) redundancy as the physical de†
grees of freedom are unchanged under RR,ℓ → RR,ℓ VR,ℓ
and ψR,ℓ,α → VR,ℓ ψR,ℓ for arbitrary SU(2) matrices VR,ℓ .
We introduce the field H R,ℓ via
†
H R,ℓ · σ = ΦR,ℓ · RR,ℓ
σRR,ℓ ,

(4)

which can be intuitively thought of as Φ represented in
a rotating reference frame; in the emergent gauge theory,
H R,ℓ plays the role of the Higgs field. By construction,
Eq. (3) can be compactly restated as a coupling between
the chargons and the Higgs field [see Eq. (C6)].
If both RR,ℓ and H R,ℓ condense, we will just reobtain
long-range magnetic order; upon choosing a gauge where
⟨RR,ℓ ⟩ = 1, the magnetic texture is equal to the texture
of ⟨H R,ℓ ⟩, allowing us to connect the Higgs-field configurations to the classical magnetic orders studied above.
When the bosons are gapped, ⟨RR,ℓ ⟩ = 0, SR invariance
is restored, even when the Higgs field is still condensed
⟨H R,ℓ ⟩ ̸= 0, which defines a phase with topological order.
Despite the preserved SR symmetry, discrete symmetries
can still be broken [90, 92]. As the symmetry analysis is
mathematically identical to studying whether the associated classical magnetic orders preserve a symmetry modulo SRs, we conclude that the associated doped spin liquids have the same symmetries as those listed in Table I.
That is, in agreement with our Schwinger-Boson study,
the fractionalized phases associated with A1,2,3 will respect all symmetries, those with B1,2 will be nematic,

5
and the one for phase C will exhibit altermagnetic loop
currents [90, 92]. Notably, both approaches also yield the
same invariant gauge groups.

The gauge theory further allows one to compute the
electronic spectral function in those phases [91, 97], which
is obtained as a convolution of the chargon and spinon
Green’s functions, see Fig. 3(c). Focusing for concreteness on the fractionalized phase of A1 , we compare the resulting spectral function with the one in the magnetically
ordered phase in Fig. 3(d). As a result of the restored
SU(2) SR symmetry, the spectral function Ak (ω) in the
fractionalized phase does not depend on spin and yet has
peaks centered around the same frequencies as the state
with long-range AM order. This signals fractionalization since, for a given spin species, each peak in the right
panel is associated with “half an electron”. When plotting
Ak (ω) as a function of k at the Fermi level, i.e., ω = 0,
in Fig. 3(e) we clearly see the characteristic k-dependent
splitting of the Fermi surfaces. The band splitting persists at energies away from the Fermi level, see Fig. 3(f),
which further reveals that there are additional (incoherent) high-energy features associated with the presence of
spinons. A combination of quantum oscillations (probing the chargons) and (spin-resolved) photoemission [61]
[measuring Ak (ω)] can identify signatures of such a fractionalized state experimentally.

[1] L.-D. Yuan, Z. Wang, J.-W. Luo, E. I. Rashba, and
A. Zunger, “Giant momentum-dependent spin splitting
in centrosymmetric low- Z antiferromagnets,” Physical
Review B 102, 014422 (2020).
[2] L. Šmejkal, J. Sinova, and T. Jungwirth, “Beyond Conventional Ferromagnetism and Antiferromagnetism: A
Phase with Nonrelativistic Spin and Crystal Rotation
Symmetry,” Physical Review X 12, 031042 (2022).
[3] L. Šmejkal, J. Sinova, and T. Jungwirth, “Emerging Research Landscape of Altermagnetism,” Physical Review
X 12, 040501 (2022).
[4] K.-H. Ahn, A. Hariki, K.-W. Lee, and J. Kuneš, “Antiferromagnetism in RuO 2 as d -wave Pomeranchuk
instability,” Physical Review B 99, 184432 (2019).
[5] S. Bhowal and N. A. Spaldin, “Ferroically Ordered Magnetic Octupoles in d-Wave Altermagnets,” Phys. Rev. X
14, 011019 (2024).
[6] G. Cuono, R. M. Sattigeri, J. Skolimowski, and C. Autieri, “Orbital-selective altermagnetism and correlationenhanced spin-splitting in transition metal oxides,”
Journal of Magnetism and Magnetic Materials 586,
171163 (2023), arxiv:2306.17497 [cond-mat].
[7] Y. Guo, H. Liu, O. Janson, I. C. Fulga, J. van den Brink,
and J. I. Facio, “Spin-split collinear antiferromagnets:
A large-scale ab-initio study,” Materials Today Physics

V.

CONCLUSION

In summary, our work shows that driving altermagnets
into the frustrated regime with competing couplings in
scenarios where quantum fluctuations play an important
role gives rise to very rich physics, such as orbital altermagnets, various interesting spin liquids, including states
with altermagnetic correlations in the charge sector, as
well as the emergence of spin–symmetric band splitting.
Given the increasingly large number of candidate materials for altermagnets [26], which typically exhibit multiple complex moments in their unit cell, it seems plausible
that altermagnetic systems with sufficient degree of frustration [49, 69, 70] can be identified.
ACKNOWLEDGMENTS

The authors acknowledge funding by the European Union (ERC-2021-STG, Project 101040651—
SuperCorr). Views and opinions expressed are however
those of the authors only and do not necessarily reflect
those of the European Union or the European Research
Council Executive Agency. Neither the European Union
nor the granting authority can be held responsible for
them. J.A.S is thankful for discussions with Sayan Banerjee, Shubhayu Chatterjee, Lucas Pupim and Vitor Dantas. M.S.S. acknowledges discussions and a previous collaboration with Sayan Banerjee on altermagnetism.

32, 100991 (2023).
[8] T. A. Maier and S. Okamoto, “Weak-coupling theory of
neutron scattering as a probe of altermagnetism,” Physical Review B 108, L100402 (2023).
[9] I. I. Mazin, “Altermagnetism in MnTe: Origin, predicted manifestations, and routes to detwinning,” Physical Review B 107, L100418 (2023).
[10] V. Oganesyan, S. A. Kivelson, and E. Fradkin, “Quantum theory of a nematic Fermi fluid,” Physical Review
B 64, 195109 (2001).
[11] T. Sato, S. Haddad, I. C. Fulga, F. F. Assaad, and
J. van den Brink, “Altermagnetic Anomalous Hall Effect Emerging from Electronic Correlations,” Phys. Rev.
Lett. 133, 086503 (2024).
[12] C. R. W. Steward, R. M. Fernandes,
and
J. Schmalian, “Dynamic paramagnon-polarons in altermagnets,” Physical Review B 108, 144418 (2023).
[13] I. Turek, “Altermagnetism and magnetic groups with
pseudoscalar electron spin,” Physical Review B 106,
094432 (2022).
[14] J. A. Ouassou, A. Brataas, and J. Linder, “Dc Josephson Effect in Altermagnets,” Physical Review Letters
131, 076003 (2023).
[15] I. I. Mazin, K. Koepernik, M. D. Johannes, R. GonzálezHernández, and L. Šmejkal, “Prediction of unconven-

6
tional magnetism in doped FeSb2 ,” Proceedings of the
National Academy of Sciences 118, e2108924118 (2021).
[16] S. Hayami, Y. Yanagi, and H. Kusunose, “Momentumdependent spin splitting by collinear antiferromagnetic
ordering,” Journal of the Physical Society of Japan 88,
123702 (2019).
[17] L. Šmejkal, R. González-Hernández, T. Jungwirth, and
J. Sinova, “Crystal time-reversal symmetry breaking
and spontaneous hall effect in collinear antiferromagnets,” Science Advances 6, eaaz8809 (2020).
[18] B. Brekke, A. Brataas,
and A. Sudbø, “Twodimensional altermagnets: Superconductivity in a minimal microscopic model,” Physical Review B 108, 224421
(2023).
[19] P. Das, V. Leeb, J. Knolle, and M. Knap, “Realizing Altermagnetism in Fermi-Hubbard Models with Ultracold
Atoms,” Phys. Rev. Lett. 132, 263402 (2024).
[20] A. Fakhredine, R. M. Sattigeri, G. Cuono, and C. Autieri, “Interplay between altermagnetism and nonsymmorphic symmetries generating large anomalous Hall
conductivity by semi-Dirac points induced anticrossings,” Physical Review B 108, 115138 (2023).
[21] Y. Fang, J. Cano, and S. A. A. Ghorashi, “Quantum
Geometry Induced Nonlinear Transport in Altermagnets,” Phys. Rev. Lett. 133, 106701 (2024).
[22] V. Leeb, A. Mook, L. Šmejkal, and J. Knolle, “Spontaneous Formation of Altermagnetism from Orbital Ordering,” Phys. Rev. Lett. 132, 236701 (2024).
[23] I. Mazin, R. González-Hernández, and L. Šmejkal, “Induced Monolayer Altermagnetism in MnP(S,Se)3 and
FeSe,” (2023), arxiv:2309.02355 [cond-mat].
[24] L. Šmejkal, A. Marmodoro, K.-H. Ahn, R. GonzálezHernández, I. Turek, S. Mankovsky, H. Ebert, S. W.
D’Souza, O. Šipr, J. Sinova, and T. Jungwirth, “Chiral Magnons in Altermagnetic RuO2 ,” Physical Review
Letters 131, 256703 (2023).
[25] C. Sun and J. Linder, “Spin pumping from a ferromagnetic insulator into an altermagnet,” Physical Review B
108, L140408 (2023).
[26] Z.-F. Gao, S. Qu, B. Zeng, Y. Liu, J.-R. Wen, H. Sun,
P.-J. Guo, and Z.-Y. Lu, “AI-accelerated Discovery
of Altermagnetic Materials,” Natl Sci Rev , nwaf066
(2025).
[27] C. W. J. Beenakker and T. Vakhtel, “Phase-shifted
Andreev levels in an altermagnet Josephson junction,”
Physical Review B 108, 075425 (2023).
[28] X. Zhou, W. Feng, R.-W. Zhang, L. Šmejkal, J. Sinova,
Y. Mokrousov, and Y. Yao, “Crystal thermal transport
in altermagnetic RuO2 ,” Phys. Rev. Lett. 132, 056701
(2024).
[29] R. M. Fernandes, V. S. de Carvalho, T. Birol, and R. G.
Pereira, “Topological transition from nodal to nodeless
zeeman splitting in altermagnets,” Phys. Rev. B 109,
024404 (2024).
[30] C. Sun, A. Brataas, and J. Linder, “Andreev reflection
in altermagnets,” Phys. Rev. B 108, 054511 (2023).
[31] S.-B. Zhang, L.-H. Hu, and T. Neupert, “Finitemomentum Cooper pairing in proximitized altermagnets,” Nat. Commun. 15, 1 (2024).
[32] H. G. Giil and J. Linder, “Superconductor-altermagnet
memory functionality without stray fields,” Phys. Rev.

B 109, 134511 (2024).
[33] D. Zhu, Z.-Y. Zhuang, Z. Wu, and Z. Yan, “Topological superconductivity in two-dimensional altermagnetic
metals,” Phys. Rev. B 108, 184505 (2023).
[34] Y.-X. Li and C.-C. Liu, “Majorana corner modes and
tunable patterns in an altermagnet heterostructure,”
Phys. Rev. B 108, 205410 (2023).
[35] S. A. A. Ghorashi, T. L. Hughes, and J. Cano, “Altermagnetic Routes to Majorana Modes in Zero Net Magnetization,” Phys. Rev. Lett. 133, 106601 (2024).
[36] Q.
Cheng
and
Q.-F.
Sun,
“Orientationdependent
josephson
effect
in
spin-singlet
superconductor/altermagnet/spin-triplet
superconductor junctions,” Phys. Rev. B 109, 024517 (2024).
[37] D. S. Antonenko, R. M. Fernandes, and J. W. F.
Venderbos, “Mirror Chern Bands and Weyl Nodal Loops
in Altermagnets,” Phys Rev Lett 134, 096703 (2025).
[38] Y. Yu, H. G. Suh, M. Roig, and D. F. Agterberg, “Altermagnetism from coincident Van Hove singularities:
application to κ-Cl,” Nat Commun 16, 1 (2025).
[39] M. Wei, L. Xiang, F. Xu, L. Zhang, G. Tang, and
J. Wang, “Gapless superconducting state and mirage
gap in altermagnets,” Phys. Rev. B 109, L201404
(2024).
[40] P. A. McClarty and J. G. Rau, “Landau theory of altermagnetism,” Phys. Rev. Lett. 132, 176702 (2024).
[41] S. Banerjee and M. S. Scheurer, “Altermagnetic superconducting diode effect,” Phys. Rev. B 110, 024503
(2024).
[42] K. V. Yershov, V. P. Kravchuk, M. Daghofer, and
J. van den Brink, “Fluctuation-induced piezomagnetism
in local moment altermagnets,” Phys. Rev. B 110,
144421 (2024).
[43] B. Brekke, A. Brataas,
and A. Sudbø, “Twodimensional altermagnets: Superconductivity in a minimal microscopic model,” Phys. Rev. B 108, 224421
(2023).
[44] Q. Cui, B. Zeng, P. Cui, T. Yu, and H. Yang, “Efficient spin seebeck and spin nernst effects of magnons in
altermagnets,” Phys. Rev. B 108, L180401 (2023).
[45] P. M. Cônsoli and M. Vojta, “SU(3) altermagnetism:
Lattice models, chiral magnons, and flavor-split bands,”
arXiv e-prints (2024), arXiv:2402.18629 [cond-mat.strel].
[46] T. Jungwirth, R. M. Fernandes, J. Sinova,
and
L. Smejkal, “Altermagnets and beyond:
Nodal
magnetically-ordered phases,” arXiv e-prints (2024),
arXiv:2409.10034 [cond-mat.mtrl-sci].
[47] V. S. de Carvalho and H. Freire, “Unconventional superconductivity in altermagnets with spin-orbit coupling,”
Phys Rev B 110, L220503 (2024).
[48] G. Sim and J. Knolle, “Pair Density Waves and Supercurrent Diode Effect in Altermagnets,” arXiv e-prints
(2024), arXiv:2407.01513 [cond-mat.supr-con].
[49] C. Xu, S. Wu, G.-X. Zhi, G. Cao, J. Dai, C. Cao,
X. Wang, and H.-Q. Lin, “Altermagnetic ground state
in distorted Kagome metal CsCr3Sb5,” Nat Commun
16, 1 (2025).
[50] A. Bose, S. Vadnais, and A. Paramekanti, “Altermagnetism and superconductivity in a multiorbital t − J
model,” Phys Rev B 110, 205120 (2024).

7
[51] J. Ōiké, K. Shinada, and R. Peters, “Nonlinear magnetoelectric effect under magnetic octupole order: Application to a d-wave altermagnet and a pyrochlore lattice
with all-in/all-out magnetic order,” Phys Rev B 110,
184407 (2024).
[52] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F.
Agterberg, “Minimal models for altermagnetism,” Phys.
Rev. B 110, 144412 (2024).
[53] M. Zhao, W.-W. Yang, X. Guo, H.-G. Luo, and
Y. Zhong, “Altermagnetism in heavy-fermion systems:
Mean-field study on the Kondo lattice,” Phys Rev B
111, 085145 (2025).
[54] T. Aoyama and K. Ohgushi, “Piezomagnetic properties
in altermagnetic MnTe,” Phys. Rev. Mater. 8, L041402
(2024).
[55] H. Bai, Y. C. Zhang, Y. J. Zhou, P. Chen, C. H. Wan,
L. Han, W. X. Zhu, S. X. Liang, Y. C. Su, X. F. Han,
F. Pan, and C. Song, “Efficient Spin-to-Charge Conversion via Altermagnetic Spin Splitting Effect in Antiferromagnet RuO2 ,” Physical Review Letters 130, 216701
(2023).
[56] J. Krempaský, L. Šmejkal, S. W. D’Souza, M. Hajlaoui, G. Springholz, K. Uhlířová, F. Alarab, P. C.
Constantinou, V. Strocov, D. Usanov, W. R. Pudelko,
R. González-Hernández, A. Birk Hellenes, Z. Jansa,
H. Reichlová, Z. Šobáň, R. D. Gonzalez Betancourt,
P. Wadley, J. Sinova, D. Kriegner, J. Minár, J. H. Dil,
and T. Jungwirth, “Altermagnetic lifting of Kramers
spin degeneracy,” Nature 626, 517 (2024).
[57] S. Lee, S. Lee, S. Jung, J. Jung, D. Kim, Y. Lee,
B. Seok, J. Kim, B. G. Park, L. Šmejkal, C.-J. Kang,
and C. Kim, “Broken Kramers Degeneracy in Altermagnetic MnTe,” Phys. Rev. Lett. 132, 036702 (2024).
[58] S. Reimers, L. Odenbreit, L. Šmejkal, V. N. Strocov,
P. Constantinou, A. B. Hellenes, R. Jaeschke Ubiergo,
W. H. Campos, V. K. Bharadwaj, A. Chakraborty,
T. Denneulin, W. Shi, R. E. Dunin-Borkowski, S. Das,
M. Kläui, J. Sinova, and M. Jourdan, “Direct observation of altermagnetic band splitting in CrSb thin films,”
Nat. Commun. 15, 1 (2024).
[59] Z. Feng, X. Zhou, L. Šmejkal, L. Wu, Z. Zhu, H. Guo,
R. González-Hernández, X. Wang, H. Yan, P. Qin,
X. Zhang, H. Wu, H. Chen, Z. Meng, L. Liu, Z. Xia,
J. Sinova, T. Jungwirth, and Z. Liu, “An anomalous
Hall effect in altermagnetic ruthenium dioxide,” Nature
Electronics 5, 735 (2022).
[60] A. Bose, N. J. Schreiber, R. Jain, D.-F. Shao, H. P.
Nair, J. Sun, X. S. Zhang, D. A. Muller, E. Y. Tsymbal,
D. G. Schlom, and D. C. Ralph, “Tilted spin current
generated by the collinear antiferromagnet ruthenium
dioxide,” Nature Electronics 5, 267 (2022).
[61] J. Liu, J. Zhan, T. Li, J. Liu, S. Cheng, Y. Shi, L. Deng,
M. Zhang, C. Li, J. Ding, Q. Jiang, M. Ye, Z. Liu,
Z. Jiang, S. Wang, Q. Li, Y. Xie, Y. Wang, S. Qiao,
J. Wen, Y. Sun, and D. Shen, “Absence of Altermagnetic Spin Splitting Character in Rutile Oxide RuO2 ,”
Phys Rev Lett 133, 176401 (2024).
[62] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia,
and J. Liu, “Multifunctional antiferromagnetic materials with giant piezomagnetism and noncollinear spin
current,” Nat. Commun. 12, 1 (2021).

[63] F. Ferrari and R. Valentí, “Altermagnetism on the
Shastry-Sutherland lattice,” Phys Rev B 110, 205140
(2024).
[64] I. V. Solovyev, “Magneto-optical effect in the weak ferromagnets LaMO3 (M= Cr, Mn, and Fe),” Phys Rev B
55, 8060 (1997).
[65] Y. Noda, K. Ohno, and S. Nakamura, “Momentumdependent band spin splitting in semiconducting MnO2:
a density functional calculation,” Phys Chem Chem
Phys 18, 13294 (2016).
[66] M. Naka, S. Hayami, H. Kusunose, Y. Yanagi, Y. Motome, and H. Seo, “Spin current generation in organic
antiferromagnets,” Nat Commun 10, 1 (2019).
[67] M. Naka, Y. Motome, and H. Seo, “Perovskite as a spin
current generator,” Phys Rev B 103, 125114 (2021).
[68] T. Okugawa, K. Ohno, Y. Noda, and S. Nakamura,
“Weakly spin-dependent band structures of antiferromagnetic perovskite LaMO3 (M = Cr, Mn, Fe),” J
Phys.: Condens Matter 30, 075502 (2018).
[69] N. Biniskos, F. J. dos Santos, K. Schmalzl, S. Raymond,
M. dos Santos Dias, J. Persson, N. Marzari, S. Blügel,
S. Lounis, and T. Brückel, “Complex magnetic structure and spin waves of the noncollinear antiferromagnet
Mn5 Si3 ,” Phys Rev B 105, 104404 (2022).
[70] C. Sürgers, G. Fischer, W. H. Campos, A. B. Hellenes,
L. Šmejkal, J. Sinova, M. Merz, T. Wolf, and W. Wernsdorfer, “Anomalous Nernst effect in the noncollinear antiferromagnet Mn5Si3,” Commun Mater 5, 1 (2024).
[71] R. R. P. Singh, O. A. Starykh, and P. J. Freitas, “A new
paradigm for two-dimensional spin liquids,” Journal of
Applied Physics 83, 7387 (1998).
[72] J.-S. Bernier, C.-H. Chung, Y. B. Kim, and S. Sachdev,
“Planar pyrochlore antiferromagnet: A large-N analysis,” Phys. Rev. B 69, 214427 (2004).
[73] R. F. Bishop, P. H. Y. Li, D. J. J. Farnell, J. Richter,
and C. E. Campbell, “Frustrated Heisenberg antiferromagnet on the checkerboard lattice: J1 -J2 model,”
Phys. Rev. B 85, 205122 (2012).
[74] M. Sadrzadeh and A. Langari, “Phase diagram of J1-J2
transverse field Ising model on the checkerboard lattice:
a plaquette-operator approach,” Eur. Phys. J. B 88, 1
(2015).
[75] P. H. Y. Li and R. F. Bishop, “Ground-state phase structure of the spin- 12 anisotropic planar pyrochlore,” Journal of Physics: Condensed Matter 27, 386002 (2015).
[76] J.-B. Fouet, M. Mambrini, P. Sindzingre, and C. Lhuillier, “Planar pyrochlore: A valence-bond crystal,” Phys.
Rev. B 67, 054411 (2003).
[77] B. Canals, “From the square lattice to the checkerboard
lattice: Spin-wave and large-n limit analysis,” Phys.
Rev. B 65, 184408 (2002).
[78] O. Tchernyshyov, O. A. Starykh, R. Moessner, and
A. G. Abanov, “Bond order from disorder in the planar
pyrochlore magnet,” Phys. Rev. B 68, 144422 (2003).
[79] Y.-H. Chan, Y.-J. Han, and L.-M. Duan, “Tensor
network simulation of the phase diagram of the frustrated J1 -J2 Heisenberg model on a checkerboard lattice,” Phys. Rev. B 84, 224407 (2011).
[80] A. Auerbach, Interacting electrons and quantum magnetism (Springer Science & Business Media, 2012).

8
[81] A. Auerbach and D. P. Arovas, “Schwinger bosons approaches to quantum antiferromagnetism,” Introduction
to Frustrated Magnetism: Materials, Experiments, Theory , 365 (2010).
[82] N. Read and S. Sachdev, “Large-n expansion for frustrated quantum antiferromagnets,” Phys. Rev. Lett. 66,
1773 (1991).
[83] X. Yang and F. Wang, “Schwinger boson spin-liquid
states on square lattice,” Phys. Rev. B 94, 035160
(2016).
[84] R. Samajdar, S. Chatterjee, S. Sachdev, and M. S.
Scheurer, “Thermal hall effect in square-lattice spin liquids: A schwinger boson mean-field study,” Phys. Rev.
B 99, 165126 (2019).
[85] B. I. Shraiman and E. D. Siggia, “Mobile vacancies in a
quantum heisenberg antiferromagnet,” Phys. Rev. Lett.
61, 467 (1988).
[86] H. J. Schulz, “Effective action for strongly correlated
fermions from functional integrals,” Phys. Rev. Lett. 65,
2462 (1990).
[87] J. R. Schrieffer, “Pairing, magnetic spin fluctuations,
and superconductivity near a quantum critical point,”
Journal of Superconductivity 17, 539 (2004).
[88] S. Sachdev, M. A. Metlitski, Y. Qi, and C. Xu, “Fluctuating spin density waves in metals,” Phys. Rev. B 80,
155129 (2009).
[89] Y. Qi and S. Sachdev, “Effective theory of fermi pockets in fluctuating antiferromagnets,” Phys. Rev. B 81,
115129 (2010).
[90] S. Chatterjee, S. Sachdev, and M. S. Scheurer, “Intertwining Topological Order and Broken Symmetry in a
Theory of Fluctuating Spin-Density Waves,” Phys. Rev.
Lett. 119, 227002 (2017).
[91] M. S. Scheurer, S. Chatterjee, W. Wu, M. Ferrero, A. Georges, and S. Sachdev, “Topological order in the pseudogap metal,” Proceedings of the
National Academy of Science 115, E3665 (2018),
arXiv:1711.09925 [cond-mat.str-el].
[92] M. S. Scheurer and S. Sachdev, “Orbital currents in insulating and doped antiferromagnets,” Phys. Rev. B 98,
235126 (2018).
[93] M. E. Simon and C. M. Varma, “Detection and implications of a time-reversal breaking state in underdoped
cuprates,” Phys. Rev. Lett. 89, 247003 (2002).
[94] C. M. Varma, “Non-fermi-liquid states and pairing instability of a general model of copper oxide metals,”
Phys. Rev. B 55, 14554 (1997).
[95] P. M. Bonetti, S. Mandal, J. A. Sobral, and M. S.
Scheurer, “In preparation,” (2025).
[96] A. Jahin, H. Zhang, G. B. Halász, and S.-Z. Lin, “Quasiparticle Interference in Kitaev Quantum Spin Liquids,”
Phys Rev Lett 134, 126501 (2025).
[97] W. Wu, M. S. Scheurer, S. Chatterjee, S. Sachdev,
A. Georges, and M. Ferrero, “Pseudogap and fermisurface topology in the two-dimensional hubbard
model,” Phys. Rev. X 8, 021048 (2018).
[98] D. P. Kingma and J. Ba, “Adam:
A Method
for Stochastic Optimization,” arXiv
(2014),
10.48550/arXiv.1412.6980, 1412.6980.
[99] L. Messio, C. Lhuillier, and G. Misguich, “Lattice
symmetries and regular magnetic orders in classical

frustrated antiferromagnets,” Phys. Rev. B 83, 184401
(2011).
[100] C. Hickey, L. Cincio, Z. Papić, and A. Paramekanti,
“Emergence of chiral spin liquids via quantum melting of
noncoplanar magnetic orders,” Phys. Rev. B 96, 115115
(2017).
[101] N. N. Bogolyubov, “On the theory of superfluidity,” J.
Phys. (USSR) 11, 23 (1947).
[102] J. Valatin, “Comments on the theory of superconductivity,” Il Nuovo Cimento (1955-1965) 7, 843 (1958).
[103] J. Colpa, “Diagonalization of the quadratic boson hamiltonian with zero modes: Ii. physical,” Physica A: Statistical Mechanics and its Applications 134, 417 (1986).
[104] M. wen Xiao, “Theory of transformation for the diagonalization of quadratic hamiltonians,”
(2009),
arXiv:0908.0787 [math-ph].
[105] S. Sachdev, “Quantum phase transitions of antiferromagnets and the cuprate superconductors,” in Modern
Theories of Many-Particle Systems in Condensed Matter Physics, edited by D. C. Cabra, A. Honecker, and
P. Pujol (Springer Berlin Heidelberg, Berlin, Heidelberg,
2012) pp. 1–51.
[106] A. V. C. Ar. Abanov and J. Schmalian, “Quantumcritical theory of the spin-fermion model and its application to cuprates: Normal state analysis,” Advances in
Physics 52, 119 (2003).
[107] N. Read and S. Sachdev, “Spin-peierls, valence-bond
solid, and néel ground states of low-dimensional quantum antiferromagnets,” Phys. Rev. B 42, 4568 (1990).
[108] R. K. Kaul, A. Kolezhuk, M. Levin, S. Sachdev, and
T. Senthil, “Hole dynamics in an antiferromagnet across
a deconfined quantum critical point,” Phys. Rev. B 75,
235122 (2007).

9
Appendix A: Classical Phase Diagram

As discussed in the main text, to study the ordered phases for H defined in Eq. (1), we start from the classical limit
S → ∞. For this, we consider the classical ansatz (2) for the two sub-lattices in the unit cell given by
p
T
2
S A,α = (cos(Q · R), sin(Q · R), ηA ) / 1 + ηA
p
,
T
2
S B,α = (cos(Q · R − φ), sin(Q · R − φ), ηB ) / 1 + ηB

(A1)

where α = {Qx , Qy , φ, ηA , ηB } is a set of variational parameters yet to be determined. We determine the classical
phase diagram by minimizing the classical energy H (S A,α · S B,α ) expression with respect to the parameters α, using
a combination of grid search over the variational parameters’ space plus gradient descent-like optimization methods
to find energetically favored configurations.
The first step for the grid search method consists of defining an energy grid with a total of LGD equally spaced values
for each of the variational parameters in α, with the domains for the initial values α0 defined as Q0x , Q0y , φ0 ∈ [−π, π]
0
0
and ηA
, ηB
∈ [−10, 10]. For each pair of coupling constants (J2 /J1 , KS 2 /J1 ), we identify the configurations α0 which
have the lowest energy within the computed energy grid. These configurations are then selected as a starting point
for the gradient descent algorithm. These set of parameters α0 are iteratively updated with the standard formula
α = α0 − λ∂H/∂α. Here, λ is the learning rate, and each iteration constitutes one epoch. Our simulations included
λ ∈ [0.1, 0.001] over different runs up to 4 × 104 epochs. We repeated this process for varying energy grid sizes
L ∈ [10, 40]. Additionally, we also considered one variation of the standard gradient-descent method called ADAM,
which introduces adaptable learning rates for each of the variational parameters [98]. After convergence, the minimum
energy configurations at each (KS 2 /J1 , J2 /J1 ) point are characterized by the sets αconv . Their energies were then
compared to determine the phase boundaries in Fig. 1(b). A particular set for each of the phases in the classical phase
diagram (b) can be seen in Table I, as well as their spin textures S A,B (αconv ) in Fig. 1(c).

FIG. 4: Phase diagram of the model (1) in the classical limit S → ∞, focused around the region where the orbital AM (C) is
located. (b) and (c) show one-dimensional cuts for the phase transition A1 → C → A3 from the perspective of the variational
parameters αconv . The colormap in (a) refers to the absolute value of the scalar spin chirality |S 1 · (S 2 × S 3 ) |, whereas the
background color in (b) and (c) to the absolute value of the nearest-neighbor spin product |S 1 · S 2 |.

As stated in the main text, each magnetic phase can also be characterized by two sets of observables: the nearestneighbor spin products on the elementary plaquette (EP) given by S EP and the scalar spin chiralities χEP . The
latter are crucial for characterizing non-coplanar textures [90, 99, 100]. The orbital AM C is the only phase in the
EP
classical phase diagram with non-zero scalar
 spin chirality. It has a staggered pattern χ (see Table I) that evolves
2
continuously for varying KS /J1 , J2 /J1 , as can be seen in Fig. 1 (e) and Fig. 4 (a). The continuous change of
this observable is accompanied by a similar behavior from the perspective of the variational parameters ηA and ηB
obtained in αconv , which always obey the constraint ηA + ηB = 0, see Fig. 4(b). Likewise, the nearest-neighbor spin
products S EP also vary continuously in C and A2 , see Fig. 1(b, d) and background color in Fig. 4(b, c). The other
phases A1 , B1 , B2 and A3 have fixed values for S EP and zero scalar spin chirality (see Table I).

10
Appendix B: Schwinger-Boson ansätze
1.

General formalism

In this section we discuss in more detail the SB description of the spin-liquid states considered in the main text,
as well as their associated magnetic orders obtained after the bosonic condensation. We start by rewriting the
Hamiltonian (1), without the ring exchange term K, in terms of the operators
Ŝ i =

1
2

X

b̂†iσ σ σσ′ b̂iσ′ .

(B1)

σ,σ ′ =↑,↓

The inclusion of only J1 and J2 exchange interactions in the SB formalism turns out to be sufficient to identify
ansätze corresponding to all the magnetic phases present in the classical phase diagram in Fig. 1(b). Using the SU(2)
completeness relation
σ µµ′ · σ νν ′ =

3
X

k
k
σµµ
′ σνν ′ = 2δµν ′ δµ′ ν − δµµ′ δνν ′ ,

(B2)

k=1
†
we can rewrite the dot product of spins as Ŝ i · Ŝ j = B̂ij
Bij − Â†ij Aij , where Âij and B̂ij are bond operators defined as

Âij =

1
2

X

b̂iσ (iσy )σσ′ b̂jσ

and B̂ij =

σ,σ ′ =↑,↓

1 X
b̂iσ b̂†jσ .
2

(B3)

σ=↑,↓

These are typically referred to as paring and hopping operators, respectively. After a Hubbard-Stratonovich transformation, we obtain the decoupled mean-field Hamiltonian
HMF =

X †
X 1

∗
(Bij
b̂iσ b̂†jσ − A∗ij σ b̂iσ b̂j−σ + H.c.) + (|Aij |2 − |Bij |2 )/Jij − µ
b̂iσ b̂iσ ,
2
i,j,σ
i

(B4)

where µ is the chemical potential and Aij , Bij are the mean-field values of the bond operators, i.e.,
⟨Âij ⟩ = Aij /Jij

and ⟨B̂ij ⟩ = Bij /Jij .

(B5)

Equation (B4) has the same functional
form as the Hamiltonian Hb mentioned in the main text, apart from the
P
0
constant energy shift HMF
= i,jσ (|Aij |2 − |Bij |2 )/Jij . The mean-field parameters Aij , Bij can assume complex
∗
values and satisfy the constraints Aij = −Aji , and Bij = Bji
. The Hamiltonian (B4) exhibits an emergent U(1) gauge
symmetry, which can be clearly seen by noticing that HMF remains invariant under a local U(1) gauge transformation
defined by
b̂iσ → eiϕi b̂iσ ,

σ =↑, ↓

Aij → ei(ϕi +ϕj ) Aij ,

(B6)

Bij → ei(ϕi −ϕj ) Bij .
Consequently, each spin-liquid ansatz can be identified through gauge-invariant fluxes defined as
∗
∗
AA
Φ□
ijkl = Arg[Aij Ajk Akl Ali ];
□AB
Φijkl
= Arg[Aij A∗jk Bkl Bli ];

e □AB = Arg[Aij B ∗ A∗ Bli ];
Φ
jk kl
ijkl

(B7)

∗
Φ∆
ijk = Arg[Aij Ajk Bki ];
∗
2
Φ∆
ijk = Arg[Bij Ajk Aki ].
□AB e □AB
∆
∆
∆
∆
AA
We will henceforth refer to each ansatz according to the notation [Φ□
1234 , Φ1234 , Φ1234 , {Φ123 , Φ234 , Φ341 , Φ412 },
∆2
∆2
∆2
∆2
{Φ123 , Φ234 , Φ341 , Φ412 }].

11
Focusing on ansätze and gauges where the Aij , Bij respect the Bravais-lattice translational symmetry, the Hamilto1 P −ik.r
nian (B4) can be rewritten in momentum space after taking the Fourier transformation b̂r,α,σ = √
b̂k,α,σ ,
ke
N
T

P
as HMF = k Ψ†k Mk (Aij , Bij ) Ψk + const. Here, Ψk = b̂kA↑ , b̂kB↑ , b̂†−kA↓ , b̂†−kB↓
is the Nambu spinor and the
4 × 4 matrix Mk is given by

∗ e−ikx + B eikx − 2µ
∗
B24
ξ̃k
−2iA24 sin(kx )
−ξ−k
24

∗ eiky + B e−iky − 2µ
1
ξ̃k
B13
ξk
2iA13 sin(ky )


13
Mk (Aij , Bij ) = 
 (B8)
∗
∗
∗
ik
−ik
x
x


2
2iA24 sin(kx )
ξk
B24 e
+ B24 e
− 2µ
ξ̃−k
−ik
ik
∗
∗
∗
∗
y
y
−ξ−k
−2iA13 sin(ky )
ξ̃−k
B13 e
+ B13 e
− 2µ


∗
with ξ˜k = B23
+ B12 e−iky + B34 eikx + B14 e−i(ky −kx ) and ξk = −A12 e−iky + A23 − A34 eikx − A14 e−i(ky −kx ) .

a.

Diagonalization of the quadratic bosonic Hamiltonians

In order to diagonalize HMF , we consider the Bogoliubov-Valatin transformation, a well-known method for diagonalizing a general quadratic bosonic Hamiltonian [101–104]. For simplicity, we suppress the momentum index k for
now and consider a Hamiltonian H of the form

T
1
H = Ψ† Mk Ψ with
Ψ† = b̂†1 , . . . , b̂†N , b̂1 , . . . , b̂N
,
(B9)
2
with N different values of internal quantum numbers describing degrees of freedom such as spin or sublattice, for
example. We then reformulate the bosonic Hamiltonian H in terms of a new set of creation and annihilation op†
and γ̂m ). The diagonalizability of the original bosonic Hamiltonian H ensures the existence of such a
erators (γ̂m
transformation matrix T that turns Mk into a simplified diagonal-matrix form in


ω1 0 . . . 0



T
 0 ω2 . . . 0 
1
†
†
†

H = Γ† T † Mk T Γ with T † Mk T = 
,
Ψ
=
T
Γ
and
Γ̂
≡
γ̂
,
.
.
.
,
γ̂
,
γ̂
,
.
.
.
,
γ̂
.
1
N
. 
1
N
 .. .. . .
2
. .. 
. .
0

0 . . . ω2N

(B10)
The transformation matrix T can be constructed from the eigenvectors (V (ωi )) of Kk = ρ3 Mk , known as the dynamic
matrix. The eigenvalues of the dynamic matrix Kk appear in pairs and are real if Kk is diagonalizable. Furthermore,
the pair of eigenvalues is generally related to two eigenvectors, one with a positive norm and the other with a negative
norm, i.e.,
!
1N ×N
0
†
†
V (ωi )ρ3 V (ωi ) = 1 and V (−ωi )ρ3 V (−ωi ) = −1, where ρ3 =
.
(B11)
0
−1N ×N
Finally, bosonic commutation relations constrain the transformation matrix T to be paraunitary, i.e., T ρ3 T † = ρ3 ,
suggesting a natural order for grouping the eigenvectors in T as
(


T −1 Kk T = diag(ω1 , . . . , ωN , −ω1 , . . . , −ωN ),
T = V (ω1 ), . . . , V (ωN ), V (−ω1 ), . . . , V (−ωN ) , yielding
T −1 Mk T = diag(ω1 , . . . , ωN , ω1 , . . . , ωN ).
(B12)
b.

Determining the magnetic order

In the SB formalism, bosonic condensation occurs at specific momentum points ±k0 , corresponding to the minima
of the spinon bands, which are obtained from the diagonalization of Kk . At a critical chemical potential µc , these
points are associated with zero-energy eigenvectors Ψi . In real space, the condensate can then be expressed as a linear
combination of these eigenvectors as (assuming for concreteness that k0 ̸= −k0 )

T
⟨Ψ⟩ = ⟨b̂rA↑ ⟩, ⟨b̂rB↑ ⟩, ⟨b̂†rA↓ ⟩, ⟨b̂†rB↓ ⟩
= eik0 ·r (z1 Ψ1 + z2 Ψ2 ) + e−ik0 ·r (z3 Ψ3 + z4 Ψ4 ) with zi ∈ C.
(B13)

12
The expectation value of the spins at positions r (spin texture) can then be obtained from
⟨S µ (r)⟩ = Xµ† σXµ ,

(B14)


T
up to global SR transformations, where Xµ = ⟨b̂rµ↑ ⟩, ⟨b̂rµ↓ ⟩ . Here, µ refers to the sublattice indices, and σ =
T

(σx , σy , σz ) . Finally, spin liquid ansätze can be directly associated to classically magnetic ordered phases using these
expressions. In what follows, we outline the key intermediate steps in employing this procedure for the ansätze in
Fig. 2 and the magnetic phases in Fig. 1(b, c):
• A1 phase - U(1) [0, 0, 0, {0, 0, 0, 0}, {0, 0, 0, 0}]:
The gauge-flux structure is given by only non-zero nearest-neighbor bonds Aij [see Fig. 2]:
A12 = A1 , A23 = A1 , A34 = −A1 , A41 = −A1 ;
A13 = 0, A24 = 0;
B12 = 0, B23 = 0, B34 = 0, B41 = 0;

(B15)

B13 = 0, B24 = 0.
For this state, we find four-fold degenerate spinon dispersions (related to Mk , see (B12))
q
ω = A1 2 f1 (k) + µ2 with f1 (k) = 2 cos (kx ) sin2 (ky /2) + cos (ky )

(B16)

The spinon condensation occurs at Q = (0, π) as the chemical potential approaches µc = 2A1 . There are four
zero-energy eigenvectors, which are given by
!T
!T
p
p
µc − −4A21 + µ2c
µc + −4A21 + µ2c
1
1
ψ1 =
, 0, 0, 1
, ψ2 =
, 0, 0, 1
,
Nψ1
2A1
Nψ2
2A1
(B17)
!T
!T
p
p
2
2
2
2
µc + −4A1 + µc
−µc − −4A1 + µc
1
1
0, −
0,
ψ3 =
, 1, 0
and ψ4 =
, 1, 0
,
Nψ3
2A1
Nψ4
2A1
where Nψi represents the corresponding normalization factors for each eigenvector. For the cases where we do not
analytically diagonalize Kk , condensation is reached numerically by introducing a small offset in µ → µc + ∆µ,
where ∆µ ≃ 10−10 . After considering equations (B13) and (B14), we calculate the observables S EP and χEP
and conclude that the resulting magnetic order corresponds to the AM A1 in Fig. 1(e).
• A2 phase - Z2 [0, π, 0, {0, 0, 0, 0}, {0, 0, 0, 0}]:
This ansatz is obtained from the previous U(1) case by turning on the nearest-neighbor bonds Bij as [see Fig. 2]:
A12 = A1 , A23 = A1 , A34 = −A1 , A41 = −A1 ;
A13 = 0, A24 = 0;
B12 = iB1 , B23 = iB1 , B34 = −iB1 , B41 = −iB1 ;

(B18)

B13 = 0, B24 = 0.
The corresponding dispersions are given by
q
p
ω± = (A21 − B12 ) f2 (k) + µ2 ± |B1 g(k)| A2 f2 (k) + µ2 ,

(B19)

with f2 (k) = 2 cos(ky ) sin2 (kx /2) + cos (kx ) and g (k) = 4 sin (kx /2) cos (ky /2).
p The spinon condensation takes
place at the point Q = (π, 0) as the chemical potential approaches µc = −2 A21 + B12 . The associated zeroenergy eigenvectors to the condensation are expressed as
!T
!T
p
p
A21 + B12 B1
A21 + B12
1
1
B1
(B20)
ψ1 =
−
, i , 0, 1
and ψ2 =
i ,
, 1, 0
,
Nψ
A1
A1
Nψ
A1
A1
with Nψ representing the normalization factor. The resulting magnetic order associated to the condensation is
the canted AM A2 phase in Fig. 1(e).

13
• B1 phase - U(1) [0, 0, 0, {0, 0, 0, 0}, {0, 0, 0, 0}]:
The gauge-flux structure is given by real nearest-neighbor and next-nearest-neighbor bonds Aij [see Fig. 2]:
A12 = A1 , A23 = 0, A34 = −A1 , A41 = 0;
A13 = A2 , A24 = −A2 ;
B12 = 0, B23 = 0, B34 = 0, B41 = 0;

(B21)

B13 = 0, B24 = 0.
This leads to doubly degenerate bands whose dispersions are:
r
q
1
2A21 f3 (k) + 4µ2 − 2A22 f4 (k) ± |A2 m+ (k)| −8A21 f3 (k) − 2A22 m2− (k),
ω± =
2

(B22)

with f3 (k) = cos (kx + ky ) − 1, f4 (k) = sin2 (kx ) + sin2 (ky ) and m± (k) = sin (kx ) ± sin (ky ). Bosonic condensation takes place at µc = A1 + A2 and Q = ± (π/2, π/2). Approaching the condensation numerically
T
with A1 = −0.2 and A2 = −0.5, the zero-energy eigenvectors at Q are given by ψ1 = 21 (1, 1, i, i) and ψ2 =
T
1
2 (−i, −i, 1, 1) , with B1 being the associated magnetic order.
• B2 phase - U(1) [0, 0, 0, {0, 0, 0, 0}, {0, π, 0, 0}]:
The gauge-flux structure is given by both real nearest-neighbor and next-nearest-neighbor bonds Aij and Bij
[see Fig. 2]:
A12 = 0, A23 = 0, A34 = −A1 , A41 = −A1 ;
A13 = 0, A24 = A2 ;
B12 = B1 , B23 = B1 , B34 = 0, B41 = 0;

(B23)

B13 = B2 , B24 = 0.
It leads to doubly degenerate bands. The spinon condensation
p takes place at Q = ± (π/2, 0) as we approach the
critical chemical potential given by µc = 12 (A2 + B2 ) − 12 A22 + 4B12 − 2A2 B2 + B22 . Approaching the condensation numerically with A1 = −0.12, A2 = −0.35, B1 = −0.6 and B2 = 0.3, we find the eigenvectors at Q to be
T
T
given by ψ1 = (0.60752, 0.36185, 0.60750i, 0. + 0.36183i) and ψ2 = (−0.6075i, −0.36183i, 0.60752, 0.36185) .
The resulting magnetic order associated to the condensation is the B2 phase in Fig. 1(c).
• A3 phase - Z2 [π, 0, 0, {0, 0, 0, 0}, {0, 0, 0, 0}]:
The gauge-flux structure is given by real nearest-neighbor and next-nearest-neighbor bonds Aij [see Fig. 2]:
A12 = −A1 , A23 = A1 , A34 = −A1 , A41 = −A1 ,
A13 = −A2 , A24 = −A2 ;
B12 = 0, B23 = 0, B34 = 0, B14 = 0;

(B24)

B13 = 0, B24 = 0.
In this case, we discover the spinon bands to be doubly degenerate bands, given by
r
q
√
1
4A21 f5 (k) + 4µ2 − 2A22 f4 (k) ± 2 |A2 m− (k)| −8A21 f5 (k) + 2A22 m2+ (k),
ω± =
2

(B25)

with f5 (k) = sin (kx ) sin (ky ) − 1, f4 (k) = sin2 (kx ) + sin2 (ky ) and m± (k) = sin (kx ) ± sin (ky ). The
minimum √of the dispersion appears at ±Q = ± (−π/2, π/2), with critical chemical potential given by
µc = − 2A1 + A2 . For A1 = −0.3 and A2 = −0.5, the normalized eigenvectors are given by ψ1 =
T
T
(0.353553 (1 − i) , −0.5i, 0.353554 (1 + i) , 0.5) and ψ2 = (0.5, 0.353554 (1 − i) , 0.5i, 0.353553 (1 + i)) . The resulting magnetic order associated to the condensation is the A3 phase in Fig. 1(c).
• C phase - Z2 [π, π, π, {

3π π 3π π
3π π 3π π
, ,
, }, { , ,
, }].
2 2 2 2
2 2 2 2

14
Finally, the ansatz related to the orbital AM C takes into account all types of bonds Aij and Bij , i.e.,
A12 = −A1 , A23 = A1 , A34 = −A1 , A41 = −A1 ;
A13 = −A2 , A24 = −A2 ;

(B26)

B12 = iB1 , B23 = iB1 , B34 = iB1 , B41 = −iB1 ;
B13 = iB2 , B24 = −iB2 .

This results in two doubly degenerate bands which display minima at Q = ± (−π/2, π/2).
For A1 = −0.3, A2 = −0.2, B1 = −0.35 and B2 = −0.1, the zero-energy eigenvectors
T
are given by ψ1 = (0.41574 + 0.17646i, 0.54409, 0.38472 + 0.38472i, −0.41874 + 0.16920i) and ψ2 =
T
(0.41874 − 0.16919i, 0.38472 − 0.38472i, 0.54409, −0.17646 + 0.41574i) .
In addition, the spin correlations S EP and the spin scalar chiralities χEP can also be calculated in the spin liquid
regime to be further compared with the same observables for the classically magnetic orders. In the QSL regime, the
expectation values are determined by evaluating all possible Wick contractions of the Schwinger boson operators in
Ŝ i · Ŝ j and Ŝ i · (Ŝ j × Ŝ k ). Using equations (B1) and (B3), these are given by
⟨Ŝ i · Ŝ j ⟩ =

3  |Bij |2 − |Aij |2 
,
2
2
Jij

(B27)

and
⟨Ŝ i · (Ŝ j × Ŝ k )⟩ = −

h
i
3
Im(Bij Bjk Bki ) + Im(Aij A∗jk Bki ) + Im(Bij Ajk A∗ki ) + Im(A∗ij Bjk Aki ) .
Jij Jjk Jki

(B28)

These quantities in the quantum spin liquid (QSL) regime are gauge invariant, as expected. Moreover, equation
(B28) confirms that a mean-field ansatz based on purely real Aij and Bij is incapable of generating spin liquids with
non-zero χEP , and, by extension, non-coplanar magnetic phases upon bosonic condensation. More specifically, by
3π π 3π π
3π π 3π π
, }, { , ,
, }] we confirm that the expected staggered chirality pattern
using the ansatz Z2 [π, π, π, { , ,
2 2 2 2
2 2 2 2
for phase C can be found in both regimes, see Table II.
TABLE II: Values of the observables S EP and χEP according to equations (B27) and (B28) before (in the quantum spin liquid
regime) and after bosonic condensation (for the equivalent classical magnetic order). The latter is calculated using equations
(B13) and (B14). For the QSLs, the observables are presented up to a multiplicative factor. The non-universal parameters
s0 , s′ , s1 , χ1 ∈ R+ depend on the mean-field values Aij and Bij .
QSL

Condensate

Label

S EP

χEP

S EP

χEP

A1
A2
A3
B1
B2
C

(−1, −1, −1, −1)
(−1, −1, −1, −1)
(−1, −1, −1, −1)
(−1, 0, −1, 0)
(1, 1, −s1 , −s1 )
(−1, −1, −1, −1)

(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
(1, −1, 1, −1)

(−1, −1, −1, −1)
s0 (−1, −1, −1, −1)
(0, 0, 0, 0)
(−1, 1, −1, 1)
(1, 1, −1, −1)
s′ (−1, −1, −1, −1)

(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
(0, 0, 0, 0)
χ1 (−1, 1, −1, 1)

2.

CP1 action for (A1 )

In this section, we present the continuum-field theoretical description of the transition from the spin-liquid phase to
altermagnetic order in the case of the A1 phase. Following Read and Sachdev’s procedure [82, 105], we parameterize
the bosonic operators in A and B sublattices using slowly varying fields, i.e.,
bA,ri ,α = ψA,α (r i )eiQ·ri ,

(B29)

y
bB,ri ,α = σαβ
ψB,β (r i )eiQ·ri ,

(B30)

15
where Q is the position in momentum space where spinon condensation takes place. With A1 < 0, in case of our
ansatz for the A1 phase (as described in Fig. 2 of the main text), we found dispersion minimum to be at Q = (0, π).
To derive the continuum field theory, we plug equations (B29-B30) into the mean-field Hamiltonian (B4), and carry
out a gradient expansion, which leads to (in an action description)
Z

d2 r
a2

Z



d
d
∗
∗
∗
ψA,α + ψB,α
ψB,α − µ ψA,α
ψA,α + ψB,α
ψB,α
dτ
dτ
2
i

A
a
1
∗
∗
∗
∗
∇ψA,α ∇ψB,α + ∇ψA,α
.
+ 2A1 ψA,α ψB,α + ψA,α
∇ψB,α
ψB,α
−
4

S=

dτ

h

∗
ψA,α

Next, we introduce two fields defined by zα =
Z
S=

d2 r
a2

Z
dτ

h

zα∗

(B31)

∗
∗
ψA,α − ψB,α
ψA,α + ψB,α
√
√
and πα =
and rewrite the action as
2
2

i
d
d 
A1 a2
πα + πα∗ zα + (2A1 − µ)|zα |2 − (2A1 + µ)|πα |2 −
|∇zα |2 − |∇πα |2 .
dτ
dτ
4

(B32)

As can be seen from Eq. (B32), in this new form, πα fields turn out to be massive, whereas zα fields become massless
near the critical µc = 2A1 , marking the phase transition from the U(1)[0, 0, 0, {0, 0, 0, 0}, {0, 0, 0, 0}] spin-liquid to
altermagnetic order A1 . Note that the critical chemical potential µc is the same as the one obtained previously within
the SB framework, exemplifying the consistency between both approaches. Finally, integrating the πα fields and
restoring gauge invariance by introduction of the gauge field aµ , we arrive at the following effective action
Z
Seff =

d2 r
4a

Z cβ
0

i
h
∆2
dτ̄ |(∂µ − iaµ )zα |2 + 2 |zα |2 .
c

(B33)

This essentially describes the massive spinons zα coupled to a compact U(1) gauge field, where c = |A1 |a is the spinon
aτ
velocity, ∆2 = (µ2 − 4A21 ), and aτ̄ =
.
c
Appendix C: Electronic spectral function

In this Appendix, we explain the details on how the electronic properties inside the fractionalized AM phases in
Fig. 3 of the main text are computed. The total spin-fermion-model-like action, S = Se + Sc + SΦ , we start from
consists of three parts: first the non-interaction electronic action,


Z β
X †
X
Se =
(C1)
dτ 
cR,ℓ,σ (∂τ − µ)cR,ℓ,σ −
tR,ℓ;R′ ,ℓ′ c†R,ℓ,σ cR′ ,ℓ′ ,σ  ,
0

R,R′ ,ℓ,ℓ′

R,ℓ

where c†R,ℓ,σ are the (τ -dependent) electronic fields associated with the creation of an electron in the unit cell labeled
by the Bravais lattice site R, of sublattice ℓ = A, B, and of spin σ. Note that Se is invariant under global SR
(summation over repeated σ indices is implied). Although most of the following analysis is more generally valid,
we later choose the hopping matrix elements tR,ℓ;R′ ,ℓ′ as described in the main text with nearest and next-nearest
neighbor hopping on the lattice in Fig. 1(a). These electrons are coupling via [σ = (σx , σy , σz )T is a vector of Pauli
matrices]
Z β
Sc =

dτ
0

X †
cR,ℓ,σ σ σ,σ′ cR,ℓ,σ′ · ΦR,ℓ

(C2)

R,ℓ

to a bosonic field Φ which describes fluctuations of the electronic spins. While at high-energies the action SΦ of Φ
can just be obtained via a Hubbard-Stratonovich decoupling of some bare electronic interactions, we here think of S
as an effective low-energy action, just as in the celebrated spin-fermion model [106], and take


Z β

X
X
1
2
SΦ =
dτ 
(∂τ ΦR,ℓ ) + V (Φ2R,ℓ ) +
JR,ℓ;R′ ,ℓ′ ΦR,ℓ · ΦR′ ,ℓ′  .
(C3)
4g0 0
′
′
R,ℓ

R,R ,ℓ,ℓ

16
Here JR,ℓ;R′ ,ℓ′ are effective exchange coupling constants, akin to Jj in the spin model (1).
To describe the fractionalized phases, characterized by topological order, we transform into a rotating reference
frame in spin space via [85–87]
cR,ℓ,σ (τ ) =

X

(C4)

(RR,ℓ (τ ))σ,α ψR,ℓ,α (τ ).

α=±

In Eq. (C4), R are (space-time dependent, bosonic) SU(2) matrices, physically related to the spinons and, thus, to
the Schwinger bosons in Eq. (B1) in the spin-liquid regime. While the spin is carried by R, the charge is governed by
the fermionic “chargon” fields ψ; to indicate that the latter do not carry spin, we use α = ± (rather than σ =↑, ↓) to
label its two components. As the physical electrons are invariant under the local reparameterization,
†
RR,ℓ (τ ) → RR,ℓ (τ )VR,ℓ
(τ ),

ψR,ℓ (τ ) → VR,ℓ (τ )ψR,ℓ (τ ),

†
VR,ℓ
(τ )VR,ℓ (τ ) = 1,

(C5)

inserting Eq. (C4) into S, as we shall do in the following, will lead to an SU(2) gauge theory.
To discuss the action of spinons and chargons, we start with the coupling Sc which can be exactly rewritten as
Z β
Sc =

dτ
0

X

†
ψR,ℓ,α
σ α,α′ ψR,ℓ,α′ · H R,ℓ ,

(C6)

R,ℓ

where H plays the role of a Higgs field, transforming under the adjoint representation of the SU(2) gauge transformation (C5). It is formally related to the collective boson Φ via
†
H R,ℓ · σ = ΦR,ℓ · RR,ℓ
σRR,ℓ

and thus (ΦR,ℓ )a =

i
1 h
†
tr σa RR,ℓ σRR,ℓ
· H R,ℓ .
2

(C7)

Inserting the parameterization (C4) into the non-interacting electronic part Se of the action will lead to quartic terms;
as in Ref. 91, we will decouple those into chargon and spinon parts. This leads to the chargon action


Z β
X †
X
†
(C8)
Sψ =
dτ 
ψR,ℓ,α (∂τ − µ)ψR,ℓ,α −
(UR,ℓ;R′ ,ℓ′ )α,α′ ψR′ ,ℓ′ ,α′  ,
tR,ℓ;R′ ,ℓ′ ψR,ℓ,α
0

R,R′ ,ℓ,ℓ′

R,ℓ

†
where (UR,ℓ;R′ ,ℓ′ )α,α′ = ⟨(RR,ℓ
RR′ ,ℓ′ )α,α′ ⟩ and the spinon contribution

e
SR
=

Z β
0


X
†
χTR,ℓ;R,ℓ RR,ℓ
dτ tr 
∂τ RR,ℓ −
R,ℓ


X

†
RR′ ,ℓ′  ,
tR,ℓ;R′ ,ℓ′ χTR,ℓ;R′ ,ℓ′ RR,ℓ

(C9)

R,R′ ,ℓ,ℓ′

†
ψR′ ,ℓ′ ,α′ ⟩.
with the 2 × 2 matrices (χR,ℓ;R′ ,ℓ′ )α,α′ = ⟨ψR,ℓ,α
Finally, plugging Eq. (C7) into SΦ in Eq. (C3) leads to coupling terms between the Higgs field and the spinons.
To describe the fractionalized phase with topological order, we follow previous works, see, e.g., Ref. 91, and keep the
Higgs field at the saddle point value H R,ℓ → ⟨H R,ℓ ⟩. Note that ⟨H R,ℓ ⟩ ̸= 0 does not break SR symmetry as the
Higgs field is invariant under SRs [cf. Eq. (C6)], as long as the bosons R remain gapped/not condensed. We can now
associate non-magnetic fractionalized states with each of the phases in the classical phase diagram in Fig. 1(b) by
choosing ⟨H R,ℓ ⟩ to be equal to the respective spin texture in the gauge where the bosons RR,ℓ will condense in a
spatially uniform way, ⟨RR,ℓ ⟩ = R0 , once the gap closes. For, in that case, we see in Eq. (C7) that ⟨ΦR,ℓ ⟩ will be
equal to ⟨H R,ℓ ⟩ apart from a global SR. To keep the discussion concise, we focus on phase A1 , the collinear AM, in
the following; without loss of generality we choose a gauge where

⟨H R,ℓ ⟩ = H0 êz sℓ ,

with sA = −sB = 1.

In this gauge, it is convenient to use the CP1 parameterization
!
∗
(zR,ℓ )↑ −(zR,ℓ
)↓
†
RR,ℓ =
, with zR,ℓ
zR,ℓ = 1.
∗
(zR,ℓ )↓ (zR,ℓ
)↑

(C10)

(C11)

17
†
The reason is that this leads to the intuitive form, N R,ℓ = zR,ℓ
σzR,ℓ , of the normalized altermagnetic order parameter
N R,ℓ = sℓ ΦR,ℓ /|ΦR,ℓ | as readily follows from Eq. (C7). We next express SΦ in Eq. (C3) in terms of N R,ℓ , yielding


Z β
X
X
1
2
dτ 
SΦ =
(∂τ N R,ℓ ) +
sℓ sℓ′ JR,ℓ;R′ ,ℓ′ N R,ℓ · N R′ ,ℓ′  , g = g0 /H02 ,
(C12)
4g 0
′
′
R,ℓ

R,R ,ℓ,ℓ

which we next study in the continuum limit; to this end, we introduce the continuum fields n(τ, x) and m(τ, x) with
the constraints n2 = 1 and n · m = 0 and write
p
(C13)
N R,ℓ (τ ) = n(τ, R + v ℓ ) 1 − m2 (τ, R + v ℓ ) + sℓ m(τ, R + v ℓ ), with v A = x̂/2, v B = ŷ/2.
Including nearest (J1 ) and next-nearest-neighbor (J2 ) exchange couplings, just like in the spin model we study, see
Fig. 1(a) of the main text, and expanding up to second order in gradients and m, we find the non-linear sigma model
Z β
i
h
1
2
2
2
SΦ =
dτ d2 x (∂τ n) + v 2 (∂x n) + v 2 (∂y n) + r m2 ,
(C14)
4g 0
with v 2 = J1 /2 − J2 /4 and r = 8J1 . As expected, the ferromagnetic fluctuations m are massive, r > 0, and can thus
be neglected, i.e., N R,ℓ (τ ) ≃ n(τ, R + v ℓ ). The AM fluctuations n are governed by the usual relativistic form in
Eq. (C14), which in turn can be restated [89, 107] as the CP1 model
Z
z,c
−1
SΦ = g
dτ d2 x |(∂µ − iaµ )zα |2 ,
(C15)
where aµ is an emergent U(1) gauge field; this is exactly the same continuum field theory we derived for the SB
mean-field ansatz for phase A1 in Appendix B 2. As in Ref. 91, we will neglect the gauge-field fluctuations, which are
not expected to change the results qualitatively [108], and work on the lattice, i.e., use
XX


†
SΦz,c = g −1 T
zn,q
zn,q Ω2n + Eq2 ,
Eq2 = 2J 2 (2 − cos qx − cos qy ) + ∆2
(C16)
Ωn

q

for the bosons in Eq. (C11); here ∆ is the bosonic gap that has to be finite in the spin-liquid regime with topological
†
order and is determined by the condition ⟨zR,ℓ
zR,ℓ ⟩ = 1. For the numerics presented in Fig. 3(d-f) of the main text,
we used J/t1 = 1 and ∆/t1 = 0.01.
With the spinon action (C16) at hand, we can simplify the form of the chargon action in Eq. (C8). In the gauge
†
†
leading to Eq. (C16), we immediate conclude that UR,ℓ;R′ ,ℓ′ = diag(⟨zR,ℓ
zR′ ,ℓ′ ⟩ , ⟨zR
′ ,ℓ′ zR,ℓ ⟩). As the spinon dispersion
Eq is even in q, the two terms on the diagonal of UR,ℓ;R′ ,ℓ′ are identical (and real) such that we are left with
UR,ℓ;R′ ,ℓ′ = 1ZR,ℓ;R′ ,ℓ′ ,

ZR,ℓ;R′ ,ℓ′ ∈ R.

(C17)

As the spinon (and chargon) theory is further invariant under all spatial symmetries, there will only be two independent
values, Z and Z ′ , renormalizing, respectively, the nearest- (t) and next-nearest-neighbor hopping (t′ ) of the chargons
relative to the bare electrons, t → Zt and t′ → Z ′ t′ . One can determine Z and Z ′ by solving the chargon and spinon
theory self-consistently [91], yielding order-1 values. To facilitate the comparison of the non-interacting spectra and
of the spectral function in the fractionalized theory in Fig. 3 of the main text, we simply set Z = Z ′ = 1 in the
following. Including the contribution from the Higgs field, the full chargon action can be written as
X 1 X †
Sψ + Sc = T
ψk,α [−iωn + ϵk τ0 + g α
(C18)
k · τ ] ψk,α ,
N
ω
n

k

where τj are Pauli matrices in sublattice space and


α
ikx
ϵk = −t′ (cos kx + cos ky ) − µ, (g α
+ ei(kx −ky ) + e−iky ,
k )x + i(g k )y = t 1 + e
′
(g α
k )z = −t (cos kx − cos ky ) + H0 α.

(C19)
(C20)

Consequently, the chargon Green’s function (a matrix in sublattice space) reads as

Gψ
α,α′ (iωn , k) = δα,α′

iωn − ϵk + g α
·τ
 k
,
+
−
iωn − Ek,α iωn − Ek,α

±
Ek,α
= ϵk ± |g α
k |.

(C21)

18
Finally, we can compute the electron Green’s function, Ge (iωn , k), which by virtue of the rewriting (C4) becomes
a convolution of the chargon and spinon Green’s function, see also the diagram in Fig. 3(c). After straightforward
algebra, we find
[Ge (iωn , k)]ℓ,σ;ℓ′ ,σ′ = δσ,σ′ T

X 1 XX
Ωm

N

(C22)

iq(v ℓ′ −v ℓ )
Gz (iΩm , q)Gψ
,
α,α (iωn − iΩm , k − q)e

q α=±

where Gz (iΩn , q) = g/(Ω2n + Eq2 ) is the spinon Green’s function associated with Eq. (C16). We can directly see that
the convolution with the spinons restored full SU(2) SR invariance (∝ δσ,σ′ ). More explicitly, the resultant spectral
function we plot in the main text is written as
Ak (ω) = −
=−

1
Im tr [Ge (ω + iη, k)]
4π


(C23)


X
XX
iωn − iΩm − ϵk−q + g α
g
1
k−q · τ
T



Im
2
2
−
πN
Ω + Eq iω − iΩ − E +
iωn − iΩm − Ek−q,α
q
n
m
Ωm α=± m
k−q,α

.

(C24)

iωn →ω+iη

As the spinon gap ∆ has a more direct physical meaning than the coupling constant g, we fix ∆ and then think of g
as a function of ∆ (and not vice versa), g = g(∆). It was shown in Ref. 91 that the above approximations leave the
frequency sum rule,
Z ∞
dω Ak (ω) = 1,
(C25)
−∞

untouched. We use Eq. (C25) to determine g for each ∆, yielding the non-trivial check that a single g can ensure
that Eq. (C25) holds at all k.


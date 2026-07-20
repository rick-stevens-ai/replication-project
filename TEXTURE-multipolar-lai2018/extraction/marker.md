Kondo Destruction and Multipolar Order – Implications for Heavy Fermion Quantum Criticality
Hsin-Hua Lai,1 Emilian M. Nica,2 Wen-Jun Hu,1 Shou-Shu Gong,3 Silke Paschen,4 and Qimiao Si1
1

arXiv:1807.09258v1 [cond-mat.str-el] 24 Jul 2018

Department of Physics and Astronomy, Rice University, Houston, Texas 77005, USA
2
Department of Physics and Astronomy and Quantum Materials Institute,
University of British Columbia, Vancouver, B.C., V6T 1Z1, Canada
3
Department of Physics, Beihang University, Beijing 100191, China
4
Institute of Solid State Physics, Vienna University of Technology, Wiedner Hauptstr. 8-10, 1040 Vienna, Austria
(Dated: July 25, 2018)
Quantum criticality beyond the Landau paradigm represents a fundamental problem in condensed matter and
statistical physics. Heavy fermion systems with multipolar degrees of freedom can play an important role in the
search for its universal description. We consider a Kondo lattice model with both spin and quadrupole degrees
of freedom, which we show to exhibit an antiferroquadrupolar phase. Using a field theoretical representation of
the model, we find that Kondo couplings are exactly marginal in the renormalization group sense in this phase.
This contrasts with the relevant nature of the Kondo couplings in the paramagnetic phase and, as such, it implies
that a Kondo destruction and a concomitant small to large Fermi surface jump must occur as the system is tuned
from the antiferroquadrupolar ordered to the paramagnetic phase. Implications of our results for multipolar
heavy fermion physics in particular and metallic quantum criticality in general are discussed.

Introduction— In strongly correlated systems, multiple
building blocks often interplay with each other and create a
variety of quantum phases and their transitions. Examples include the spin, orbital and nematic degrees of freedom in the
iron-based systems [1, 2], which lead to a rich landscape of
electronic orders, and the spin and valley degrees of freedom
in bilayer graphenes twisted by magic angles [3, 4], which
appear to yield a surprising Mott insulator near which superconductivity develops. The multiple degrees of freedom allow
for not only the commonly observed antiferromagnetic (AF)
states, but also “hidden” orders, with unusual order parameters that cannot readily be probed by experiments directly.
A prominent example is the quadrupolar order, which breaks
the spin-rotational symmetry as in any conventional magnetic
order but, unlike the latter, preserves the time-reversal symmetry. Such an order has been proposed for frustrated magnetic systems [5–8] and even for the nematic phase of the ironchalcogenide FeSe [9–11]. Multipolar degrees of freedom are
also being discussed in noncollinear antiferromangets [12].
They also arise in many heavy fermion metals, producing a
variety of fascinating properties [13–18].
Heavy fermion compounds typically involve local spin moments, which experience RKKY interactions between each
other and Kondo interactions with conduction electrons, and
exhibit quantum phase transitions between paramagnetic and
AF ground states [19, 20]. While the Kondo effect has been a
hallmark of heavy fermion physics, a Kondo destruction has
been shown to arise from the dynamical competition between
the RKKY and Kondo interactions [21, 22]. It has been
demonstrated in studies of Kondo lattice models from both
the paramagnetic [21] and AF-ordered [23] sides. Because
the Kondo destruction yields quantum criticality that is beyond the Landau framework of order-parameter fluctuations,
it is important to assess its universality by considering settings
that involve other types of local degrees of freedom.
An especially opportune setting arises in heavy fermion
systems with co-existing local spin and multipolar moments

[13, 14], which allow for not only AF orders but also
quadrupolar ones. In Ce3 Pd20 Si6 , an antiferroquadrupolar
(AFQ) order has been experimentally determined [24], and
a sequence of quantum critical points was discovered upon
tuning by a magnetic field [14]. Theoretical calculations that
approach the transitions from the paramagnetic side demonstrated a sequential Kondo destruction [14]. This provides the
motivation to study the Kondo effect and Fermi surface in the
AFQ ordered state.
In this Letter, we address this pressing problem using a
spin-1 Kondo lattice model, which contains both spin and
quadrupole local degrees of freedom. We demonstrate a robust AFQ phase, and describes its low-energy effective theory
in terms of a quantum non-linear sigma model (NLsM) [8].
Adapting a combined boson-fermion renormalization group
(RG) procedure [25], we show that the Kondo couplings are
exactly marginal in the RG sense and thereby establish a
Kondo destruction in the multipolar order.
The model we consider is HKL = HS + Hc + HK , with
i
Xh
2
(1)
Jij (Si · Sj ) + Kij (Si · Sj ) ,
HS =
ij

Hc =

X

†
ǫk ψkα
ψkα ,

(2)

k,α=x,y,z

HK =

X
j


I
II
JK
Sj · sc,j + JK
Qj · qc,j ,

(3)

where HS represents the spin-1 bilinear-biquadratic Hamiltonian, in which we choose Jij = Jn , Kij = Kn for i, j
connected by nth-neighbor bonds. The spin-1 nature implies that the existence of local quadrupolar moments. The 5component quadrupolar operator at site i, Qi , can be defined
2
2
2
2
as: Qix −y
= (Six )2 − (Siy )2 , Qi3z −r = [2(Siz )2 − (Six )2 −
√
xy
y
y
y z
y 2
z y
(Si ) ]/ 3, Qi = Six Si + Si Six , Qyz
i = Si Si + Si Si ,
z x
x z
and Qzx
i = Si Si + Si Si . The biquadratic term can be reexpressed as (Si ·Sj )2 = (Qi ·Qj )/2−(Si ·Sj )/2+(S2i S2j )/3.
At the high-symmetry point, Jn = Kn , the symmetry is en-

2

(a)

FIG. 1. (Color online) Top panel:Illustration of the phase diagram
as a function of K2 that contains the (π, π)-AFQ with J1 = 1.0
and K1 = 1.2. The quantum disordered phase has been studied before [26]. Bottom left panel:The quadrupolar structure factor, mQ ,
which shows strong peaks at (π, π). Bottom right panel:The finitesize scaling of the spin dipolar and spin quadrupolar order parameters, which shows finite mQ at q = (π, π) and vanishing magnetic
order parameter in the thermodynamic limit.

hanced from SU(2) to SU(3). Here, the spin and quadrupolar moments can be transformed to each other under SU(3)
rotations. Our focus will be on the AFQ phase away from
the SU(3) point; however, as we will see, the time-reversalinvariant basis that is natural for the SU(3) point – which can
be related to the sz = ±1, 0 basis under a unitary transformation – will greatly facilitate our analysis. Hc describes the
conduction electrons, which have three flavors with flavor index α = x, y, z in the SU(3) time-reversal-invariant basis.
Within the 3-flavor conduction electron description, both the
electrons’ spin sc and their 5-component quadrupoles, qc , are
expressed in bilinear forms (see Supplemental Materials for
explicit forms of qc ). HK represents the Kondo couplings between the local moments and conduction electrons.
Existence of (π, π) antiferroquadrupolar order— We first
study the spin-1 bilinear-biquadratic lattice model, Eq. (1),
numerically using the large-scale Density Matrix Renormalization Group (DMRG) analysis. It is known that this
SU(3)-symmetric point can host a phase with both spin and
quadrupolar orders, which can be transformed to each other
under SU(3) transformations [5–8]. Away from the SU(3)
point, we find that increasing the weight of the biquadratic
terms can stabilize the quadrupolar order. To illustrate the
robustness of the quadrupolar order in this model, we fix
J1 = 1, K1 = 1.2, and determine the phase diagram as a
function of K2 /J1 (J2 = 0), which is shown in Fig. 1. We
find the the AFQ order with q = (π, π). This (π, π)-AFQ is
a two-sublattice order characterized by the staggered expec2
2
2
2
tation values of the Qx −y , i.e., hQjx −y i ∼ (−1)j . The
(π, π)-AFQ phase can be identified by calculating the spin
structure factor (m2S ) and quadrupolar structure factor (m2Q ).
As illustration, we consider the case K2 /J1 = −0.3, which
shows strong peak at q = (π, π) for m2Q and much weaker
peak at q = (π, 0)/(0, π) for m2S , shown in the bottom left
panel of Fig. 1 for system size Ly = 8. Performing the finitesize scaling analysis, bottom right panel of Fig. 1, we find
nonzero m2Q and vanishing m2S , which shows the presence of

(b)

(c)

FIG. 2. (Color online) (a):The real-space pattern of d vectors for
the lowest-energy state at SU(3) point with J1 = K1 > 0 and
J2 = K2 < 0. (b):The partitioning of the square lattice used in the
derivation of the field theory for the (π, π) AFQ order. The square
lattice is divided into clusters (red squares) containing 8 bonds.
Fields are defined at the centre of the clusters (blue dots), and we
perform gradient expansions about these points. (c):Illustration of a
cluster containing 4 nearest-neighbor bonds (red lines) and 4 secondneighbor bonds (dashed lines).

the (π, π)-AFQ order.
Non-linear sigma model for (π, π)-AFQ— Because the
commensurate AFQ breaks the spin-rotational symmetry but
is time-reversal invariant, we can expect three Goldstone
modes. To specify the low-energy effective theory including couplings that involve the conduction electrons, we describe the Kondo lattice model using a NLsM representation
by adapting the method illustrated in Ref. [8]. We first introduce√the SU(3) time-reversal-invariant
basis, |xi = i(|1i −
√
|1̄)/ 2,
|yi = (|1i + |1̄)/ 2,
|zi = −i|0i, where
|S z = 1i ≡ |1i. The state at site j can be written in terms
of dj = (dxj , dyj , dzj ), where dα
j are complex numbers, with
constraints from the normalization and from fixing the global
phase among dα=x,y,a , i.e., dj · d̄j = 1, and d2j = d̄2j , where
d¯ means complex conjugate of d. The Hamiltonian is then
re-expressed as (see Supplemental Materials [27])
X

Jn |di · d̄j |2 + Jn′ |di · dj |2 ≡ HSU(3) + H ′ ,(4)
HS =
ij

where we have ignored the inconsequential constant terms.
We define the deviations from the SU(3) couplings, Jn′ ≡
Kn − Jn , and explicitly separate the SU(3)-invariant part of
the Hamiltonian HSU(3) from the SU(3)-breaking part H ′ . At
the SU(3) point, i.e., Jn′ = 0 or Jn = Kn , we can see that HS
becomes a pure function of |(di · d¯j )|2 . For the lowest-energy
real-space pattern, we need to minimize the nearest-neighbor
|di · d¯j | and maximize the 2nd-neighbor |di · d¯j |. For obtaining the NLsM description, we choose the ground state pattern
of the (π, π)-AFQ,which satisfies the above requirement, as
gs T
T
(dgs
A ) = 1 0 0 , and (dB ) = 0 1 0 . Such a pattern
is illustrated in Fig. 2(a), which gives the correct (π, π)-AFQ
order at the semi-classical level.
Starting from the SU(3) point, we know that the ground
state energy is invariant under the global rotation d → Ud,
provided that U−1 = U† . To describe global rotations, we
find that Gell-Mann matrices provide a natural choice of basis

3
at the SU(3)-symmetric point. In general, we require 6 distinct generators for SU(3). However, for the present (π, π)AFQ phase, only 4 out of 6 are needed. The 4 Gell-Mann
matrices we choose are represented by λ1−4 (see Supplemental Materials for the explicit matrix forms). The global rotations in the complex space can be expressed as U(φ) ≡
P
exp[i 4p=1 λp φp ]. Besides the global rotations that preserve
the ground state energy, we also need to consider the rotations
involving the canting of the directors of ground state configurations, which increase the energy. The canting fields are
represented as µ1∼4 (see Supplemental Materials for details).
The general rotations can be represented as
P4

z

z

D(φ, ℓ, v) = ei p=1 λp φp +iµ1 ℓ1 +iµ2 vA +iµ3 vB +iµ4 ℓ2
∞
X
n
≃ U (φ)
(iµ1 ℓz1 + iµ2 vA + iµ3 vB + iµ4 ℓz2 ) , (5)

obtained after the gradient expansion. The detailed results
are presented in the Supplemental Materials, and all the terms
(Lkin , Hs ) are functions of ℓz1 , ℓz2 , vA/B , and na . Integrating out the canting fields by solving the differential equations,
δL/δℓz1 = 0, δL/δℓz2 = 0, δL/δvA = 0, δL/δvB = 0 within
the steepest-descent approximation, we obtain the NLsM for
the (π, π)-AFQ at the harmonic level. Stability requires K1 >
0, K2 < 0, K1 − J1 ≥ 0, J2 − K2 > 0, J1 + J2 − K2 > 0,
and K1 + 2K2 − 4J2 ≥ 0. Focusing on the regime away from
the SU(3) point, Jn′ 6= 0, we find that φ4 can be ignored since
it represents the spin-wave mode that is always gapped due to
the finite mass term. The effective NLsM for the (π, π)-AFQ
is
X
(∂τ φ1 )2
+ 2(K1 − 2K2 )
(∂λ φ1 )2
4(J1 + J2 − K2 )
λ
"
#
2
X
X
(∂τ φa )
2
+
− 2K2
(∂λ φa ) . (8)
8(J2 − K2 )
a=2,3

LsM
LN
≃
S

n=0

where we approximately separate out the global rotation matrix U (φ) and Taylor expand the terms involving the canting fields. The general configuration of da=A/B can be obtained by applying the general rotation on the chosen ground
gs
state configurations dgs
a=A/B , i.e., da = D(φ, ℓ, v)da . To
obtain the low-energy descriptions within the harmonic theory, we keep the Taylor expansion up to n = 2. Introducing
ℓz ≡ ℓz1 + iℓz2 and re-parametrizing
 x x x
nA nB nC

(6)
U = nyA nyB nyC  = nA nB nC ,
nzA nzB nzC

where the vectors nTa = nxa nya nza inherit the constraints
of d with na · n̄b6=a = 0, n2a = n2a , and na · n̄a = 1, with the
vector nc ≡ n̄A × n̄B being introduced as a convenient piece
of book-keeping in the present (π, π)-AFQ. It is not an independent degrees of freedom, we can fully re-express da=A/B
as functions of na , ℓz , and vA/B (see Supplemental Materials). Taylor expanding U (φ) and keeping only the leading
linear terms in φ, we can see that na and the bosonic field
φ1∼4 are related by




1
φ1 + iφ4
,
1
(7)
nA ≃ −φ1 + iφ4  ; nB ≃ 
−φ3
φ2

where nC = n̄A × n̄B . Away from the SU(3) point, we assume that H ′ can be treated perturbatively and does not affect
our results in any significant manner.
Adopting the strategy of Ref. [8], we partition the square
lattice into clusters (Figs. 2(b)-2(c)), each of which containing 8 bonds [4 nearest-neighbor bonds and 4 second-neighbor
bonds (dashed lines)], and perform the gradient expansion
about the center of a cluster. Within the cluster picture,
the
function can be concisely expressed as Z =
R partition
D[d]e−S [d] , where the action includes the kinetic terms
Skin and the Hamiltonian terms SH , S = Skin + SHs . The
Rβ
continuous descriptions of Skin = 0 dτ Lkin and SHs =

Rβ 
Rβ
dτ HS = 0 dτ HSU(3) + H ′ can be straightforwardly
0

λ

Kondo couplings— Using the identity da = D(φ, ℓ, v)dgs
a ,
and Eqs. (5)-(7), we can straightforwardly write down the
fluctuating 8-component spin/quadrupolar field in the NLsM
description (detailed in Supplemental Materials). Concisely,
the 8-component field can be separate into a uniform part and
an oscillating part,
Q(r) ≃ Q0 + QM cos(M · r),

(9)

where M ≡ (π, π), Qq represents the low-energy 8component field with momenta q = 0, M . We remark
that that the uniform part contains a “static” background of
2
2
2
2
Q3z −r that can directly couple to the qc3z −r of the 3-flavor
conduction electrons due to he Kondo couplings, Eq. (3). This
2
2
static background Q3z −r field is only invariant under rotation between x-y plane, which breaks the SU(3) symmetry of
the conduction elections down to SU(2)×U(1), where SU(2)
is spanned by the cx and cy conduction elections and U(1) is
spanned by cz . We expect that the Fermi velocities of cx and
cy are the same (vx = vy ) but is different from that of cz (vz ).
To be specific, at low energies, the conduction electrons in
the presence of the static quadrupolar background is
Z
X
Sc ≃ dd Kdǫ
ψα† (K, iǫ)(iǫ − ξK )ψα (K, iǫ) +
α=x,y

+

Z

d K dǫ ψz† (K ′ , iǫ′ )(iǫ′ − ξ̃K ′ )ψz (K ′ , iǫ′ ),
d

′

′

(10)

where ξK = vF (K − KF ), and ξ̃K ′ = ṽF (K ′ − KF′ ), where
KF and KF′ are Fermi momenta for cx/y and cz and are
generically different. The spin dipolar and quadrupolar degrees of freedom consisting of ψx/y and ψz fermions, e.g.,
sxc ∼ ψy† ψz − ψz† ψy , can be ignored due to the finite energy gap (∆E) between the ψx/y bands and the ψz band,
2
2
∆E ∝ JK hQ3z −r i.

4
Shifting our focus to the Kondo couplings, Eq. (3), we can
now re-express them as


i y
y
I
z
x
x
LK =−JK 2ℓ2 + (nA − n̄A − nB + n̄B ) szc −
2


1 y
y
x
x
z
II
−JK 2ℓ1 + (nA + n̄A + nB + n̄B ) qcxy , (11)
2
where only the uniform part Q0 couples to the conduction
electrons near the Fermi surface. We integrate out the canting
field within the steepest descent approximation. After some
algebra, we conclude that the effective low-energy description
of the action is S = SsN LsM + SK + Sc , where SSN LsM and
Sc are defined in Eqs. (8) and (10), and SK is
Z β
Z
dτ
SK ≃
d2 rλz (szc ∂τ φ1 ) ,
(12)
2
0
I
where λz = −iJK
/[4(J1 + J2 − K2 )] is the dimensionless
coupling.
Exact marginality of Kondo couplings— We now analyze
the scaling of the Kondo coupling λz in the (π, π)-AFQ using the RG procedure described in Ref. [25]. For clarity, we
introduce Φa (r, τ ) ≡ ∂τ φa (r, τ ). The scaling dimension
of Φa (r, τ ) can be directly read out, ∆[Φa (r, τ )] = 1, indicating that the scaling dimension of its Fourier partner as
∆[Φa (q, ω)] = −d, where d is the spatial dimension. For
the conduction electron fields, we obtain that ∆[ψc (K, ω)] =
−3/2. We can see that, at the tree level, the Kondo coupling is marginal, ∆[SK ] = ∆[dkdǫdd qdωψcx† (k + q, ǫ +
ω)ψcy (k, ω)Φ1 (q, ω)] = 1 + 1 + d + 1 + 2(−3/2) − d = 0
(see Supplemental Materials). .
We then turn to what happens beyond the tree level.
Considering a spherical Fermi surface of conduction electrons, we approximate their contribution via a momentum
integral near Fermi surface. Keeping the most relevant
R
R K +Λ
R
term, we obtain dd K = KFF−Λ K d−1 dK dd−1 ΩK ≃
RΛ
R
KFd−1 −Λ dk dd−1 ΩK , where we introduce k = KF − K
and keep only the KFd−1 terms after Taylor expansion. Now
the kinetic part of the fermions can be re-expressed as
Z
Sc ≃ KFd−1 dkα dd−1 ΩK dǫψcα† (iǫα − vFα kα ) ψcα
Z

= dk̄α dd−1 Ω̄K dǭψ̄cα† ǭα − vFα k̄α ψ̄cα ,
(13)

where we introduce the dimensionless couplings, ǫ = Λǭ, k =
Λk̄, ΩK = Ω̄K , KFd−1 Λ3 ψ † ψ = ψ̄ † ψ̄. For the action of
the
similar transformation,
R 2bosonic2fields,2Eq.2 (8), we perform
R
d qdω(q + ω )φ1 (q, ω) = d2 q̄dω̄(q̄ 2 + ω̄ 2 )φ̄21 (q̄, ω̄),
where we define Λ5 φ21 = φ̄21 . Plugging the new definition
intoR the Kondo action, we find that at d = 2 it takes the form
∼ dkdǫd2 qdωψcx† (k + q, ǫ + ω)ψcy (k, ω)ωφ1 (q, ω), which
leads to
√
Λ
SK
∝
,
(14)
Sc
KF

where we can see in the limit Λ/KF → 0, i.e., the Fermi momentum is much larger than the thin-shell momentum cut-off
near the Fermi surface, the Kondo coupling is heavily suppressed. Therefore,
√ the Kondo vertex is associated with positive powers of Λ/KF which is vanishingly small. As the
number of powers of Kondo couplings increases, so does the
suppression factor, and, therefore, all higher-order terms are
suppressed, which means that the scaling result at tree-level
RG analysis is exact. The Kondo coupling is indeed exactly
marginal.
This exact marginality implies that the Kondo coupling
does not flow to strong coupling. In other words, in the AFQ
phase, the local moments do not form a multipolar Kondo singlet with the conduction electrons. Thus, the RG fixed point in
the parameter regime we consider, namely weak Kondo coupling in the presence of an AFQ, shows the physics of Kondo
destruction.
Implications for the quantum phases and their transitions
in heavy fermion metals— The Kondo destruction we have
shown, when the multipolar RKKY interactions dominate
over the corresponding Kondo interactions, has a clear physical picture. In the AFQ order, the local degrees of freedom are
strongly coupled with each other and become manifested as
three quadrupolar Goldstone modes at low energies. Because
these are collective bosonic modes, they can scatter the conduction electrons, but cannot form an entangled Kondo singlet with the latter. By contrast, it is well-known that when
the Kondo interactions dominate over the RKKY interactions,
they are marginally relevant and flow towards strong coupling,
thereby yielding a Kondo entangled state 14; physically, the
local degrees of freedom will be able to lower the ground
state energy of the system by binding with the conduction
electrons into a singlet state. Calculations on the dynamical
competition between RKKY and Kondo interactions from the
Kondo-dominated side in Ref. 14 led to the proposal for two
stages of Kondo destructions. Our asymptotically exact results from the opposite end shows that multipolar Kondo destruction does take place on the ordered side. As such, our
results help establish a robust theoretical foundation for the
notion of sequential Kondo destruction [14].
Our findings set the stage for detailed studies of heavy
fermion materials with both spin and orbital moments in their
ground state. The simplest case arises in Ce-based systems of
cubic point symmetry if the Γ8 quartet is the ground state of
the 2 F5/2 multiplet [28]. Examples where a continuous phase
transition to a state with AFQ order was observed are, in addition to the aforementioned Ce3 Pd20 Si6 [24], CeB6 [29] and,
tentatively, CeTe [30] and CeCoSi [31] under pressure.
Conclusion– We have studied a spin-1 Kondo lattice model
with co-existing spin and quadrupolar local moments and
used density matrix renormalization group analysis to firmly
demonstrate the presence of an antiferroquadrupolar order.
We have derived a non-linear sigma model description of the
antiferroquadrupolar order and, based on a renormalizationgroup analysis, found that the Kondo couplings are exactly
marginal in this phase. Our results help provide a robust theo-

5
retical foundation for the recently advanced notion of sequential localization in multipolar Kondo lattice systems [14]. Our
findings point to a growing list of heavy fermion metals with
multipolar degrees of freedom as a new setting for the exploration towards a universal description of beyond-Landau
quantum criticality and strange metal physics. In general, they
illustrate how the interplay between entwined degrees of freedom can give rise to novel phases and unusual excitations, a
theme that is centrally important to a broad range of strongly
correlated systems.
Acknowledgement– The work at Rice was in part supported
by the NSF (DMR-1611392), the Robert A. Welch Foundation (C-1411), the ARO (W911NF-14-1-0525), the BigData Private-Cloud Research Cyberinfrastructure MRI Award
funded by NSF (CNS-1338099), and an IBM Shared University Research (SUR) Award. H.-H.L. has been supported
by a Smalley Postdoctoral Fellowship at the Rice Center for
Quantum Materials. SP acknowledges financial support from
the Austrian Science Fund (project P29296-N27). Q.S. acknowledges the support of ICAM and a QuantEmX grant
from the Gordon and Betty Moore Foundation through Grant
No. GBMF5305, the hospitality of University of California at
Berkeley and of the Aspen Center for Physics, which is supported by NSF grant No. PHY-1607611, and the hospitality
and support by a Ulam Scholarship from the Center for Nonlinear Studies at Los Alamos National Laboratory.

[1] Y. Kamihara, T. Watanabe, M. Hirano, and H. Hosono,
Journal of the American Chemical Society 130, 3296 (2008).
[2] Q.
Si,
R.
Yu,
and
E.
Abrahams,
Nature Reviews Materials 1, 16017 (2016).
[3] Y. Cao, V. Fatemi, S. Fang, K. Watanabe, T. Taniguchi, E. Kaxiras, and P. Jarillo-Herrero, Nature 556, 43 (2018).
[4] Y. Cao, V. Fatemi, A. Demir, S. Fang, S. L. Tomarken, J. Y.
Luo, J. D. Sanchez-Yamagishi, K. Watanabe, T. Taniguchi,
E. Kaxiras, R. C. Ashoori,
and P. Jarillo-Herrero,
Nature 556, 80 (2018).
[5] N. Papanicolaou, Nuclear Physics B 305, 367 (1988).
[6] H.
Tsunetsugu
and
M.
Arikawa,
Journal of the Physical Society of Japan 75, 083701 (2006).
[7] A.
Läuchli,
F.
Mila,
and
K.
Penc,
Phys. Rev. Lett. 97, 087205 (2006).
[8] A. Smerald and N. Shannon, Phys. Rev. B 88, 184430 (2013).
[9] R. Yu and Q. Si, Phys. Rev. Lett. 115, 116401 (2015).
[10] Q. Wang, Y. Shen, B. Pan, X. Zhang, K. Ikeuchi, K. Iida, A. D.
Christianson, H. C. Walker, D. T. Adroja, M. Abdel-Hafiez,
X. Chen, D. A. Chareev, A. N. Vasiliev, and J. Zhao, Nature
Communications 7, 12182 (2016).
[11] H.-H. Lai, W.-J. Hu, E. M. Nica, R. Yu, and Q. Si,
Phys. Rev. Lett. 118, 176401 (2017).
[12] M.-T. Suzuki, T. Koretsune, M. Ochi,
and R. Arita,
Phys. Rev. B 95, 094406 (2017).
[13] J. Custers, K.-A. Lorenzer, M. Mller, A. Prokofiev,
A. Sidorenko, H. Winkler, A. M. Strydom, Y. Shimura,
T. Sakakibara, R. Yu, Q. Si, and S. Paschen, Nature Materials 11, 189 (2012).
[14] V. Martelli, A. Cai, E. M. Nica, M. Taupin, A. Prokofiev, C.-C.

Liu, H.-H. Lai, R. Yu, R. Küchler, A. M. Strydom, D. Geiger,
J. Haenel, J. Larrea, Q. Si, and S. Paschen, arXiv:1709.09376
(2017).
[15] A.
Sakai
and
S.
Nakatsuji,
Journal of the Physical Society of Japan 80, 063701 (2011).
[16] S. Lee, S. Trebst, Y. B. Kim,
and A. Paramekanti,
arXiv:1806.02842 (2018).
[17] E. D. Bauer, N. A. Frederick, P.-C. Ho, V. S. Zapf, and M. B.
Maple, Phys. Rev. B 65, 100506 (2002).
[18] A. McCollam, B. Andraka,
and S. R. Julian,
Phys. Rev. B 88, 075102 (2013).
[19] Q. Si and F. Steglich, Science 329, 1161 (2010).
[20] P. Coleman and A. J. Schofield, Nature 433, 226 (2005).
[21] Q. Si, S. Rabello, K. Ingersent,
and J. L. Smith,
Nature 413, 804 (2001).
[22] P. Coleman, C. Pépin, Q. Si,
and R. Ramazashvili,
Journal of Physics: Condensed Matter 13, R723 (2001).
[23] S. J. Yamamoto and Q. Si, Phys. Rev. Lett. 99, 016401 (2007).
[24] P. Y. Portnichenko, S. Paschen, A. Prokofiev, M. Vojta,
A. S. Cameron, J.-M. Mignot, A. Ivanov, and D. S. Inosov,
Phys. Rev. B 94, 245132 (2016).
[25] S.
J.
Yamamoto
and
Q.
Si,
Journal of Low Temperature Physics 161, 233 (2010).
[26] W.-J. Hu, S.-S. Gong, H.-H. Lai, H. Hu, Q. Si, and A. H. Nevidomskyy, arXiv:1711.06523 (2017).
[27] See Supplemental Material for more details of derivations[url].
[28] S. Paschen and J. Larrea J., J. Phys. Soc. Jpn. 83, 061004
(2014).
[29] H. Nakao, K. Magishi, Y. Wakabayashi, Y. Murakami,
K. Koyama, K. Hirota, Y. Endoh,
and S. Kunii,
J. Phys. Soc. Jpn. 70, 1857 (2001).
[30] Y. Kawarasaki, T. Matsumura, M. Sera, and A. Ochiai, J. Phys.
Soc. Jpn. 80, 023713 (2011).
[31] H. Tanida,
Y. Muro,
and T. Matsumura,
J. Phys. Soc. Jpn. 87, 023705 (2018).

Supplemental Material for Kondo destruction in multipolar order and implications for
heavy-fermion quantum criticality
Hsin-Hua Lai,1 Emilian M. Nica,2 Wen-Jun Hu,1 Shou-Shu Gong,3 and Qimiao Si1
1

arXiv:1807.09258v1 [cond-mat.str-el] 24 Jul 2018

Department of Physics and Astronomy, Rice University, Houston, Texas 77005, USA
2
Department of Physics and Astronomy and Quantum Materials Institute,
University of British Columbia, Vancouver, B.C., V6T 1Z1, Canada
3
Department of Physics and International Research Institute of Multidisciplinary Science, Beihang University, Beijing 100191, China
(Dated: July 25, 2018)
In this supplemental material, we give more details on the DMRG calculations and the derivations for parts
of the main text.

DMRG RESULTS FOR THE SPIN STRUCTURE FACTOR

The DMRG [S1, S2] simulations have been performed on the geometry of a rectangular cylinder, with periodic boundary
conditions in the y direction and open boundaries in the x direction. We study the system with Ly up to 8. By keeping up to
4000 SU(2) DMRG states, our calculations have the largest truncation errors around 10−5 to show high accuracy. We calculate
the spin-spin (Si · Sj ) and quadrupolar-quadrupolar (Qi · Qj ) correlation functions, where Qi is the quadrupolar operator [S3]
and the quadrupolar term can be reexpressed as Qi · Qj = 2(Si · Sj )2 + Si · Sj − 8/3. We perform Fourier transformation for
the correlation functions to obtain the spin and quadrupolar structure factors as
m2S (q) =

1 X
hSi · Sj ieiq·(ri −rj )
Ns2 i,j

m2S (q) =

1 X
hQi · Qj ieiq·(ri −rj ) ,
Ns2 i,j

(S1)

and
(S2)

where the sites i, j are chosen over the middle Ns = Ly × Ly sites in order to avoid the effects of open edge [S4]. Fig. S1 shows
the spin structure factor m2S with J1 = 1, K1 = 1.2, K2 = −0.3 on the Ly = 8 cylinder, which has weak peaks at momenta
(π, 0) and (0, π). The quadrupolar structure factor m2Q has been shown in the main text.
3-FLAVOR ELECTRON REPRESENTATIONS OF S = 1 SPIN AND QUADRUPOLE

For conduction electrons, we consider 3-flavor electrons with flavor index α = x, y, z. The three flavor of fermions can be
transformed to each other by SU(3) symmetry. For each lattice site, the total electron density is one, which means that each

FIG. S1. (Color online) The spin structure factor m2S by DMRG with J1 = 1, K1 = 1.2, K2 = −0.3 on the Ly = 8 cylinder.

2
flavor of electron is 1/3-filled
D

E 1
†
ψiα
ψiα =
3

(S3)

The spin and quadrupole operators can be written in the 3-flavor electrons as,
†
sα
c,i = −iǫαβγ ψiβ ψiγ ,
2

(S4)

2

x −y
†
†
qc,i
= −ψix
ψix + ψiy
ψiy ,
2

3z −r
qc,i

2

√
†
†
†
= (ψix
ψix + ψiy
ψiy − 2ψiz
ψiz )/ 3,

xy
†
†
qc,i
= −ψix
ψiy − ψiy
ψix ,
yz
†
†
qc,i = −ψiy ψiz − ψiz ψiy ,
†
†
zx
qc,i
= −ψiz
ψix − ψix
ψiz .

(S5)
(S6)
(S7)
(S8)
(S9)

The spin and quadrupolar operators can also be transformed to each other under the SU(3) rotations.

CONTINUUM THEORY AT SU(3) POINT

Let’s focus first on the SU(3) point, where Jn = Kn . We consider the time-reversal invariance basis
1̄i
1̄i
√
√
|xi = i |1i−|
, |yi = |1i+|
, |zi = −i|0i,
2
2

(S10)

where |S z = 1i ≡ |1i and etc. A general wave function at a site j can be written in the form
|dj i = dxj |xi + dyj |yi + dzj |zi,

(S11)

dj = (dxj , dyj , dzj )

(S12)

where we can introduce the vector notation as

is a 3 vector of complex numbers. Separating the real and imaginary parts of dj gives
dj = uj + ivj .

(S13)

Requiring the wave functions to be normalizd gives the constraints,
dj · d̄j = 1 → u2j + vj2 = 1.

(S14)

d2j = d̄2j → uj · vj = 0.

(S15)

The overall phase can be fixed by requiring

Within the spin-coherent state framework, we can obtain
Sj = 2uj × vj ,

(S16)

and in terms of the components of the d we can obtain
S α = −iǫαβγ d¯β dγ ,

Q

x2 −y 2

x 2

(S17)
y 2

= −|d | + |d | ,

1 
Q3z −r = √ |dx |2 + |dy |2 − 2|dz |2 ,
3
Qxy = −d¯x dy − d¯y dx ,
Qyz = −d¯y dz − d¯z dy ,
Qzx = −d¯z dx − d¯x dz .
2

2

(S18)
(S19)
(S20)
(S21)
(S22)

3

FIG. S2. Illustration of the effects of rotations in the complex director configurations space for (π, π)-AFQ. (a) Illustration of the real
component of the directors (red cylinders). (b) Effects of the global rotation around ẑ-axis, which preserve the angle between the directors (c)
Illustration of the rotation using one of the canting fields, µ1 , which changes the angle between the directors that increases the energy.

The Hamiltonian can be re-expressed as
X

 X 
J2 |di · d̄j |2 + (K2 − J2 )|di · dj |2 + K2
J1 |di · d̄j |2 + (K1 − J1 )|di · dj |2 + K1 +
HS =
hhijii

hiji

X

 X 
J2 |di · d̄j |2 + J2′ |di · dj |2 + K2 ,
J1 |di · d̄j |2 + J1′ |di · dj |2 + K1 +
≡
hhijii

hiji

where we defined Kn − Jn ≡ Jn′ which break the SU(3) symmetry and from now on we will ignore the constants. At SU(3)
point, we can see that that Hamiltonian becomes
X
X
SU(3)
J2 |di · d̄j |2 .
(S23)
J1 |di · d̄j |2 +
=
HS
hhijii

hiji

For obtaining the non-linear sigma model (NLsM) description, we can follow the approaches detailed by A. Smerald et al. [S5]
One choice for the ground state of such a (π, π)-AFQ is
 
 
1
0
0 , dgs = 1 .
dgs
=
(S24)
A
B
0
0

The Hamiltonian, Eq. (S23), is invariant under the global rotation d → Ud, provided that U−1 = U† . In general, there should
be 6 distinct generators for SU(3), however, for the present (π, π)-AFQ phase with only two directors, only 4 out of 6 are needed
for a complete description of the global rotations which maintain the energy of the ground state. Fig. S2 illustrate the effects of
all possible rotations, some of which preserve the energy while some increase the energy. Let’s first study the global ratations.
The natural choices of the matrices at SU(3) are Gell-Mann matrices, which can be used to describe the rotation of the ground
state configuration. Ignoring the diagonal Gell-Mann matrices, we are left with 6 matrices. However, only 4 are needed for a
complete description of the global rotations for the (π, π)-AFQ with only two mutually orthogonal directors. The 4 Gell-Mann
matrices I choose are,








0 −i 0
0 0 i
0 0 0
0 1 0
λ1 =  i 0 0 λ2 =  0 0 0
λ3 = 0 0 −i λ4 = 1 0 0 .
(S25)
0 0 0
−i 0 0
0 i 0
0 0 0
The global rotation in complex space can be written as

U(φ) ≡ ei

P4

j=1 λj φj

.

Fig. S2 (b) gives an illustration of the global rotation around real ẑ-axis using U(φ1 , 0, 0, 0).

(S26)

4
On the other hand, we also need to consider the rotations involving canting of the directors ground state configurations, which
increases the energy. The canting fields I choose are








0 −i 0
0 0 −1
0 0 0
0 1 0
µ1 = −i 0 0 µ2 = 0 0 0  µ3 = 0 0 1 µ4 = −1 0 0 .
(S27)
0 0 0
1 0 0
0 −1 0
0 0 0

The general configuration of dA and dB can be obtained by operating the general rotation on the chosen ground state configugs
rations dgs
A and dB described above,
D(φ, ℓ, v) = ei

P4

z
z
p=1 λp φp +iµ1 ℓ1 +iµ2 vA +iµ3 vB +iµ4 ℓ2

,

(S28)

where
gs
dA = D(φ, ℓ, v)dgs
A , dB = D(φ, ℓ, v)dB .

Expanding the canting terms up to quadratic order, we can approximate



2
1 − 21 (ℓz1 )2 + (ℓz2 )2 + vA

ℓz1 − iℓz2
dA ≃ U(φ) 
ivA


ℓz1 + iℓz2


2 
dB ≃ U(φ) 1 − 21 (ℓz1 )2 + (ℓz2 )2 + vB
−ivB

(S29)

(S30)

(S31)

Introducing ℓz ≡ ℓz1 + iℓz2 and reparametrizing

 x x x
nA nB nC
U = nyA nyB nyC 
nzA nzB nzC

(S32)

where the vectors na inherit the constraints of d with

na · n̄b6=a = 0, n2a = n2a
na · n̄a = 1,

(S33)
(S34)

where the vector nc ≡ n̄A × n̄B is introduced as a convenient piece of book-keeping in the present (π, π)-AFQ (two sub lattice
order), and is not an independent degrees of freedom.
Going to continuum limit involves the assumption that physically interesting variation takes place on a length scale much
larger than the lattice constant a ≡ 1 and so gradients within the placate are small. In addition, the continuum field theory should
describe the dynamics of both the broken symmetry state and the nearby paramagnetic region, in which the order parameter is
assumed to be locally robust but slowly varying over macroscopic length sales. It is therefore necessary to allow the fields to
fluctuate in space and time. From now on , all the parameters are allowed to fluctuate in space-time domain, (r, τ ).
The partition function is
Z
SU (3)
SU(3)
= D[d]e−S [d] ,
(S35)
Z
SU(3)

where the action includes S

= Skinetic + SHs . Let’s focus on the Hamiltonian term first.

Continuum theory for Hamiltonian terms

The action for the Hamiltonian term is
SHs =

Z β
0

1
=
2

SU(3)

dτ HS

Z β
0

dτ

Z

SU(3)

d2 rHS,clus ,

(S36)

5
where we focus on one cluster instead of a single site and the 2 in the denominator is the effective cluster area. Within the cluster
picture, we can write down the Hamiltonian term in terms of dj . Then we can perform a gradient expansion,
1
dj (r + ǫi , τ ) ≃ dj (r, τ ) + (ǫi · ∇)dj (r, τ ) + (ǫi · ∇)2 dj (r, τ ),
2
(S37)
to give a continuum theory of the Hamiltonian term. For a square cluster with 4 sites, let’s explicitly write down the Hamiltonian
terms below.
SU(3)

SU(3)

SU(3)

HS,clus = HJ1 ,clus + HJ2 ,clus ,
where


1 1
1 1
dA (r + (− , − ), τ ) · d̄B (r + ( , − ), τ )
2 2
2 2

2

2

1 1
1 1
+ dA (r + (− , − ), τ ) · d̄A (r + (− , ), τ )
2 2
2 2
2
2
1 1
1 2
1 1
1 1
(S38)
+ dB (r + ( , − ), τ ) · d̄A (r + ( , ), τ ) + dB (r + (− , ), τ ) · d̄A (r + ( , ), τ ) ,
2 2
2 2
2 2
2 2

2
2
1 1
1 1
1 1
1 1
SU(3)
HJ2 ,clus =J2 dA (r + (− , − ), τ ) · d̄A (r + ( , ), τ ) + dB (r + ( , − ), τ ) · d̄A (r + (− , ), τ )
2 2
2 2
2 2
2 2
2
2
1 1
1 3
1 3
1 1
(S39)
+ dA (r + ( , ), τ ) · d̄A (r + (− , ), τ ) + dB (r + (− , ), τ ) · d̄A (r + ( , ), τ ) .
2 2
2 2
2 2
2 2
SU(3)
HJ1 ,clus =−J1

We now perform gradient expansion for each term
(1) J1 terms:
4 dA · d̄B

2

+2

X

λ=x,y

2
dA · ∂λ d¯B .

(S40)

(2) J2 terms:
−2

i
X h
2
2
2
2
.
|∂λ dA | + |∂λ dB | − 2 dA ∂λ d¯A − dB ∂λ d¯B

(S41)

λ=x,y

Combining all terms leads and using Eqs. (S30)-(S31),
dA · d̄B

2

i
h
2
2
≃ 4 (ℓz1 ) + (ℓz2 ) ,
2

(S42)
2

dA · ∂λ=x,y d̄B ≃ |nA · ∂λ n̄B | ,
dA · d̄A ≃ dB · d̄B ≃ 1,

(S43)
(S44)

we obtain that
SU(3)
HS,clus ≃16J1


i
h
X
X 
2
2
2
2
2
z 2
z 2
|nA ∂x n̄B | − 2J2
(ℓ1 ) + (ℓ2 ) + 2J1
|∂λ nA | + |∂λ nB | − |nA ∂λ nA | − |nB ∂λ n̄B | ,
λ=x,y

λ=x,y

(S45)

where we explicitly ignore constant terms.

Continuum theory for the kinetic terms

The action for the kinetic terms is quantum-mechanical in origin and is
Z β Z
Z Z
X


1
1 β
2
Skin ≃
d r
d2 r d̄A ∂τ dA + d̄B ∂τ dB .
d̄a ∂τ da =
2
2
0
0
a=A,B

Using again Eqs. (S30)-(S31) leads to the Lagrangian for the kinetic term as

(S46)

6

Lkin,clus ≃n̄A ∂τ nA + n̄B ∂τ nB + 2ℓz1 (n̄A ∂τ nB − nA ∂τ n̄B ) − 2iℓz2 (n̄A ∂τ nB + nA ∂τ n̄B )
−ivA (n̄c ∂τ nA + nc ∂τ n̄A ) − ivB (n̄B ∂τ nc + nB ∂τ n̄c ) .

(S47)

SU(3)
LsM
Therefore, the Lagrangian for continuum theory is LN
= Lkin,clus + LS,clus , Eq. (S45) + Eq. (S47).
S

Away from SU(3) point

We now introduce SU(3) breaking terms to break the SU(3) down to SU(2). In principle, if we focus on the AFQ phase, the
SU(2) symmetry will guarantee there are 3 gapless Goldstone modes associated with the quadrupole wave fluctuations. The
SU(3)-breaking terms added are
2
2
X 
X
~i · S
~j .
~i · S
~j + J ′
(S48)
S
S
H ′ = J1′
2
hhijii

hiji

In terms of d framework,
H ′ =J1′

X
hiji

2

|di · dj | + J2′

X

hhijii

2

|di · dj | ,

where we ignore the constant terms. We again focus on a cluster and perform gradient expansion. Let’s write down each
contributions separately.
(1) J1′ terms:
2

4 |dA · dB | + 2

X

2

|dA · ∂λ dB | .

(S49)

X h
2 i
2
2
2
.
(∂λ dA ) + ∂λ d¯A + (∂λ dB ) + ∂λ d¯B

(S50)

λ=x,y

(2) J2′ terms:
d2A d¯2A + d2B d¯2B −

λ=x,y

We then use Eqs. (S30)-(S31) simplify the results above in terms of the parametrization fields na and the canting fields
ℓz1 , ℓz2 , vA , vB . The only new assumption we need to use is that in the AFQ phase the parametrization fields na inherit the
constraints of the original vector d. In AFQ, d is purely real or purely imaginary. Without loss of generality, we assume it is
purely real. The additional constraints are
na · n̄a = 1 → n2a ≃ 1,

(S51)

na · n̄b6=a = 0 → na · nb6=a ≪ 1.

(S52)

We can then obtain approximately,
2

2
d2A ≃ 1 − 2 (ℓz2 ) − 2vA
,
2
2
2 ¯2
|dA · dA | = d d ≃ 1 − 4 (ℓz ) − 4v 2 ,

|dB · dB |

2

2
A
A A
2
,
= d2B d¯2B ≃ 1 − 4 (ℓz2 )2 − 4vB

(S53)
(S54)
(S55)

where we used the approximation n2A n̄2A ≃ 1 ≃ n2B n̄2B . In the end, we can conclude that SU(3) breaking Hamiltonian i
(ignoring constants)
′
Hclus
≃J1′

"

−J2′

4 |nA · nB |
"

2

+ 16 (ℓz1 )2 + 2

2
16 (ℓz2 ) + 8

X
λ


2

2
vA
+ vB

|nA ∂λ nB |

2

#

#

X
2
2
2
2
.
+
(∂λ nA ) + (∂λ n̄A ) + (∂λ nB ) + (∂λ n̄B )
λ

(S56)

7
For obtaining the NLsM for the (π, π)-AFQ, we need to combine Eq. (S45), Eq. (S47), and Eq. (S56) and integrate out the
canting fields within the steepest-decent approximation. Solving the differential equations,
δL
δℓz = 0;
δL
δvA = 0;

δL
δℓz = 0,
δL
δvB = 0.

(S57)

We obtain
n̄A ∂τ nB − nA ∂τ n̄B
,
16(J1 + J1′ )
i(n̄A ∂τ nB + nA ∂τ n̄B )
ℓz2 =
,
16(J1 − J2′ )
i(n̄C ∂τ nA + nC ∂τ n̄A )
vA = −
,
16J2′
i(n̄B ∂τ nC + nB ∂τ n̄C )
vB = −
.
16J2′

ℓz1 = −

(S58)
(S59)
(S60)
(S61)

Plugging the solutions back to the Lagrangian, we obtain the LN LsM,plus
LN LsM,clus =n̄A ∂τ nA + n̄B ∂τ nB −

2

2

2

[n̄A ∂τ nB + nA ∂τ n̄B ]
[n̄C ∂τ nA + nC ∂τ n̄A ] [n̄B ∂τ nC + nB ∂τ n̄C ]
[n̄A ∂τ nB − nA ∂τ n̄B ]
−
+
+
−
16(J1 + J1′ )
16(J1 − J2′ )
32J2′
32J2′
i
X
X
Xh
2
2
2
2
2
2
+2J1
|nA ∂λ n̄B | + 2J1′
|nA ∂λ nB | − 2J2
|∂λ nA | + |∂λ nB | − |n̄A ∂λ nA | − |n̄B ∂λ nB | +

−

λ=x,y

λ

λ

i
Xh
2
2
2
2
2
−J2′
(∂λ nA ) + (∂λ n̄A ) + (∂λ nB ) + (∂λ n̄B ) + 4J1′ |nA · nB | .

(S62)

λ

We now derive the linearized action by re-expressing na in terms of bosonic fields φ1,2,3,4 , with






−φ2
1
φ1 + iφ4
 ; nC ≃  φ3  ,
1
nA ≃ −φ1 + iφ4  ; nB ≃ 
1
−φ3
φ2

(S63)

the linearized harmonic Lagrangian for (π, π)-AFQ is
"
#
X
X
X
(∂τ φa )2
(∂τ φ1 )2
2
2
+ 2(K1 − 2K2 )
− 2K2
(∂λ φ1 ) +
(∂λ φa ) +
L≃
4(J1 + J2 − K2 )
8(J2 − K2 )
a=2,3
λ

2

+

(∂τ φ4 )
+ 2(K1 + 2K2 − 4J2 )
4K1

LsM
≡ LN
(φ1 , φ2 , φ3 , φ4 ).
S

X
λ

λ

(∂λ φ4 )2 + 16(K1 − J1 )φ24 −
(S64)

Ignoring the terms thtat couple to the conduction electrons’ degrees of freedom, we can see the stability for (π, π)-AFQ
requires positive stiffness leading to the conditions
K1 > 0,

K2 < 0,

(S65)

K1 − J1 ≥ 0, J2 − K2 > 0,
J1 + J2 − K2 > 0, K1 + 2K2 − 4J2 ≥ 0.

(S66)
(S67)

If we focus on the regime where K1 > J1 , we can see that φ4 is always gapped due to the finite mass term and can be ignored.
N LsM
The effective low-energy description of the action, S(π,π)−AF
Q , is
"
(
#)
Z β
Z
2
2
X
X
X
dτ
(∂
φ
)
(∂
φ
)
τ
a
τ
1
N LsM
S(π,π)−AF
+ 2(K1 − 2K2 )
− 2K2
(∂λ φ1 )2 +
d2 r
(∂λ φa )2
.
Q ≃
2
4(J1 + J2 − K2 )
8(J
−
K
)
2
2
0
a=2,3
λ

λ

(S68)

8
KONDO EFFECTS IN THE (π, π)-AFQ

We now consider the Kondo effects in the (π, π)-AFQ. Eqs. (S30)-(S31) give the general parameterizations for the d vectors
on the sublattices A and B as


1
1 2
2
(S69)
+ nB ℓ̄z + nc (ivA ) ,
dA = nA 1 − |ℓz | − vA
2
2


1 2
1
2
+ nA ℓz + nc (−ivB ) .
(S70)
dB = nB 1 − |ℓz | − vB
2
2
In order to extract the low-energy description of the Kondo coupling, we first need to extract the low-energy continuum theory de2
2
2
2
scriptions of the 8 component operator that consists of 3-component S x,y,z , and 5-component Qx −y , Q3z −r , Qxy , Qyz , Qzx .
Since we have the expressions of the fluctuating d vectors, we can write down the fluctuating 8-component dipole-quadrupole
moment,




0
−2vB − (nzB − n̄zB )
z
z

 −2vA + i(nA − n̄A ) 


 0

 z

 z
 i ℓ − ℓ̄z − i(nyA − n̄yA ) 
 i ℓ − ℓ̄z + i(nxB − n̄xB ) 








−1
1
.



(S71)
QA = 

 , QB = 
√1
√1




3
3


− ℓz + ℓ̄z − (ny + n̄y )
− ℓz + ℓ̄z − (nx + n̄x )


B
B 
A
A 




−(nz + n̄z )
0
−(nzA + n̄zA )

B

B

0

We can then write down the low-energy descriptions of the 8-component moment as



 

 
− vB + 2i (nzB − n̄zB )
− vB + 2i (nzB − n̄zB)


 
− vA − 2i (nzA − n̄zA )
vA − 2i (nzA − n̄zA )


 
−2ℓz2 − i (nyA − n̄yA − nxB + n̄xB )  i (ny − n̄y + nx − n̄x ) 
2
B
B 
A

  2 A


 
0
1
 cos(K · r)
+
Q(r, t) ≃ 


 
√1
0




3
−2ℓz − 1 (ny + n̄y + nx + n̄x )  1 [ny + n̄y − (nx + n̄x )]
B
B 

1
2 A 1 A
B
B 
A
A
2


 
− 2 (nzB + n̄zB )
− 12 (nzB + n̄zB )
1
z
z
1
z
z
− 2 (nA + n̄A )
2 (nA + n̄A )
≡ Q0 + QM cos (M · r) ,

(S72)

(S73)

where we explicitly separate out the uniform part and the oscillatory part. First we note that the uniform part contains a “static”
2
2
2
2
2
2
background of Q3z −r that directly couple to the qc3z −r of the 3-flavor conduction electrons. This static background Q3z −r
field is only invariant under rotation between x-y plane, which, therefore, should break the SU(3) symmetry of the conduction
elections dow to SU(2)×U(1), where SU(2) is spanned by the cx and cy conduction elections and U(1) is spanned by cz . We
then expect that the low-energy descriptions of conduction electrons cx and cy should be different from that of cz , i.e., the Fermi
velocities of cx and cy are the same (vx = vy ) but is different from that of cz (vz ).
Explicitly, the low-energy theory of the conduction electrons in the presence of the static quadrupolar background is
Z
X Z
Sc ≃
(S74)
dd Kdǫψα† (K, iǫ)(iǫ − ξk )ψα (K, iǫ) + dd K ′ dǫ′ ψz† (K ′ , iǫ′ )(iǫ′ − ξ̃K ′ )ψz (K ′ , iǫ′ ),
α=x,y

where ξK = vF (K − KF ), and ξ˜k′ = ṽF (K ′ − KF′ ), where kF and kF′ are generically different. We want to remark that due
to the band splitting between the x, y- and z- fermions, the spin dipolar and quadrupolar degrees of freedom consisting of ψx/y
and ψz fermions, i. e., sxc ∼ ψy† ψz − ψz† ψy , can be ignored due to the finite energy gap.
Since we have the NLsM description of all the fields, we can also re-express the Kondo couplings within the NLsM con2
2
struction. Ignoring the gapped fields due to the static hQ3z −r i background in the (π, π)-AFQ, we can write down the Kondo
coupling Lagrangian as




1 y
i y
y
y
z
x
x
z
II
x
x
z
I
(S75)
LK =−JK 2ℓ2 + (nA − n̄A − nB + n̄B ) sc − JK 2ℓ1 + (nA + n̄A + nB + n̄B ) qcxy .
2
2

9
We again integrate out the canting fields by utilizing the steepest descent approximation with
δL
δℓz = 0,
δL
δvB = 0.

δL
δℓz = 0;
δL
δvA = 0;

(S76)

We then get the results
ℓz1 = −

II
n̄A ∂τ nB − nA ∂τ n̄B
JK
+
q xy ,
′
16(J1 + J1 )
16(J1 + J1′ ) c

(S77)

I
JK
i(n̄A ∂τ nB + nA ∂τ n̄B )
+
sz ,
′
16(J1 − J2 )
16(J1 − J2′ ) c
i(n̄C ∂τ nA + nC ∂τ n̄A )
vA = −
,
16J2′
i(n̄B ∂τ nC + nB ∂τ n̄C )
.
vB = −
16J2′

ℓz2 =

(S78)
(S79)
(S80)

We can plug the solutions back to the Lagrangian to obtain
L =n̄A ∂τ nA + n̄B ∂τ nB −

2

2

2

[n̄A ∂τ nB − nA ∂τ n̄B ]
[n̄A ∂τ nB + nA ∂τ n̄B ]
[n̄C ∂τ nA + nC ∂τ n̄A ] [n̄B ∂τ nC + nB ∂τ n̄C ]
−
+
+
−
16(J1 + J1′ )
16(J1 − J2′ )
32J2′
32J2′
i
h
X
X
X
+2J1
|nA ∂λ n̄B |2 + 2J1′
|nA ∂λ nB |2 − 2J2
|∂λ nA |2 + |∂λ nB |2 − |n̄A ∂λ nA |2 − |n̄B ∂λ nB |2 +
−

λ=x,y

−J2′

λ

λ

i
Xh
2
2
2
2
2
(∂λ nA ) + (∂λ n̄A ) + (∂λ nB ) + (∂λ n̄B ) + 4J1′ |nA · nB | −
λ


i (n̄A ∂τ nB + nA ∂τ nB ) z
i y
sc
(nA − n̄yA − nxB + n̄xB ) +
2
8(J1 − J2′ )


n̄A ∂τ nB − nA ∂τ n̄B xy
II 1
qc −
(nyA + n̄yA + nxB + n̄xB ) −
−JK
2
8(J1 + J1′ )

I
−JK

−



I 2
II 2
(JK
)
(JK
)
(szc )2 −
(q xy )2 ,
′
16(J1 − J2 )
16(J1 + J1′ ) c

(S81)

2

2

where we explicitly suppress the constant static backgroun Q3z −r field which breaks SU(3) symmetry between three flavored
conduction electrons. Focusing on the quadrupolar order, we again use the identity n̄a ∂τ na = 1/2∂τ (na )2 ≃ 0, and can be
ignored.
Re-express the fields in the bosonic fields using Eq. S63, the Lagrangian becomes
"
#
X
X
X
(∂τ φa )2
(∂τ φ1 )2
2
2
L≃
+ 2(K1 − 2K2 )
− 2K2
(∂λ φ1 ) +
(∂λ φa ) +
4(J1 + J2 − K2 )
8(J2 − K2 )
a=2,3
λ

λ

X
(∂τ φ4 )2
+ 2(K1 + 2K2 − 4J2 )
(∂λ φ4 )2 + 16(K1 − J1 )φ24 −
+
4K1
λ

I
I 2
iJK
(J II )2
(JK
)
iJ II
−
szc (∂τ φ1 ) + K qcxy (∂τ φ4 ) − K (qcxy )2 −
(sz )2
4(J1 + J2 − K2 )
4K1
16K1
16(J1 + J2 − K2 ) c

LsM
≡ LN
(φ1 , φ2 , φ3 , φ4 ) + LK + L(ψ 4 ),
S

(S82)

where the last two terms L(ψ 4 ) only renormalize the Fermi velocity and the quartic fermion terms and can be ignored. Focusing
on the point away from the SU(3) point, K1 > J1 , we can also ignore φ4 due to the finite mass term. In the end we conclude the

10
NLsM for the (π, π)-AFQ in the presence of Kondo couplings to the 3-flavor conduction electrons is
"
(
#)
Z β
Z
2
2
X
X
X
(∂
φ
)
dτ
(∂
φ
)
τ
a
τ
1
N LsM
+ 2(K1 − 2K2 )
− 2K2
d2 r
(∂λ φ1 )2 +
S(π,π)−AF
(∂λ φa )2
,
Q ≃
2
4(J1 + J2 − K2 )
8(J
−
K
)
2
2
0
a=2,3
λ

λ

(S83)

SK ≃
Sc ≃

Z β
0

Z

dτ
2

Z

d2 r (λz szc ∂τ φ1 ) ,

dd Kdǫ

X

α=x,y

ψα† (K, iǫ)(iǫ − ξK )ψα (K, iǫ) +

(S84)
Z

dd K ′ dǫ′ ψz† (K ′ , iǫ′ )(iǫ′ − ξ̃K ′ )ψz (K ′ , iǫ′ ),

(S85)

I
where we define λz = −iJK
/[4(J1 + J2 − K2 )], ξK = vF (K − KF ), and ξ̃K ′ = ṽF (K ′ − K̃F′ ).

EXACT MARGINALITY OF KONDO COUPLINGS

In this work, we follow the scaling procedure illustrated in Ref. [S6] to conclude the exact marginality of the Kondo coupling λz in the (π, π)-AFQ. For clarity in the scaling analysis, we first define Φa (r, τ ) ≡ ∂τ φa (r, τ ). The scaling dimension of Φa (r, τ ) can be directly read out, ∆[Φa (r, τ )] = 1, which leads to the scaling dimension of its Fourier partner as
∆[Φa (q, ω)] = −d, where d is the spatial dimension. For the conduction electron fields, the scaling dimension of a sermonic
field is ∆[ψc (K, ω)] = −3/2. We can see that at tree level, the scaling dimension of the Kondo coupling is marginal,
∆[SK ]
tree−level

= ∆[dkdǫdd qdωψcx† (k + q, ǫ + ω)ψcy (k, ω)Φ1 (q, ω)] = 1 + 1 + d + 1 + 2(−3/2) − d = 0. (S86)

Now we will show that the result at tree level is exact based on procedure in Ref. [S6].
Considering a spherical Fermi surface of conduction electrons, we first re-express the momentum integral in the part of the
action of the conduction electron as the momentum integral near the Fermi surface. Keeping the most relevant term, we obtain
Z
Z KF +Λ
Z
Z Λ
Z
dd K =
K d−1 dK dd−1 ΩK ≃ KFd−1
dk dd−1 ΩK
(S87)
KF −Λ

−Λ

, where we introduce k = KF − K and keep only the KFd−1 terms after Taylor expansion. Now the kinetic part of the fermions
can be re-expressed as

Sc ≃ KFd−1

Z

dkα dd−1 ΩK dǫψcα† (iǫα − vFα kα ) ψcα =

Z


dk̄α dd−1 Ω̄K dǭψ̄cα† ǭα − vFα k̄α ψ̄cα ,

(S88)

where we introduce the dimensionless couplings, ǫ = Λǭ, k = RΛk̄, ΩK = Ω̄K , KFd−1 Λ3 ψ † ψR = ψ̄ † ψ̄. For the action of
the bosonic fields, Eq. (S83), we perform similar transformation, d2 qdω(q 2 + ω 2 )φ21 (q, ω) = d2 q̄dω̄(q̄ 2 + ω̄ 2 )φ̄21 (q̄, ω̄),
2
5 2
where
R we define Λ φ1 = φ̄1 . Plugging the new definition into the Kondo action, we find that at d = 2 it takes the form
∼ dkdǫd2 qdωψcx† (k + q, ǫ + ω)ψcy (k, ω)ωφ1 (q, ω), which leads to
√
Λ
SK
1+1+2+1 −3 1−2 1− 52
=
∝Λ
Λ KF Λ
,
(S89)
Sc
KF
where we can see in the limit Λ/KF → 0, i.e., the Fermi momentum is much larger than the thin-shell momentum cut-off near
the Fermi surface, the Kondo coupling is heavily suppressed.Therefore, the Kondo vertex is associated with positive powers of
√
Λ/KF which is vanishingly small. As the number of powers of Kondo couplings increases, so does the suppression factor,
and, therefore, all higher-order terms are suppressed, which means that the scaling result at tree-level RG analysis is exact. The
Kondo coupling is indeed exactly marginal.

[S1] S. R. White, Phys. Rev. Lett. 69, 2863 (1992).
[S2] I. McCulloch and M. Gulácsi, Europhysics Letters 57, 852 (2002).
[S3] M. Blume and Y. Y. Hsieh, Journal of Applied Physics 40, 1249 (1969).
[S4] W.-J. Hu, H.-H. Lai, S.-S. Gong, R. Yu, A. H. Nevidomskyy, and Q. Si, ArXiv e-prints (2016), arXiv:1606.01235 [cond-mat.str-el].
[S5] A. Smerald and N. Shannon, Phys. Rev. B 88, 184430 (2013).
[S6] S. J. Yamamoto and Q. Si, Journal of Low Temperature Physics 161, 233 (2010).


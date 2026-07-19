Topological phase transitions and thermal Hall effect in a noncollinear spin texture
Ken Chen,1, 2 Qiang Luo,3, ∗ Bin Xi,4 Hong-Gang Luo,1, 2 and Jize Zhao1, 2, †

arXiv:2312.10473v2 [cond-mat.str-el] 9 May 2024

1
School of Physical Science and Technology & Key Laboratory of Quantum
Theory and Applications of MoE, Lanzhou University, Lanzhou 730000, China
2
Lanzhou Center for Theoretical Physics, Key Laboratory of Theoretical Physics of Gansu Province,
Lanzhou University, Lanzhou, Gansu 730000, China
3
College of Physics, Nanjing University of Aeronautics and Astronautis, Nanjing, 211106, China
4
College of Physics Science and Technology, Yangzhou University, Yangzhou 225002, China
(Dated: May 10, 2024)

The noncollinear spin textures provide promising avenues to stabilize exotic magnetic phases and
excitations. They have attracted vast attention owning to their nontrivial band topology in the past
decades. Distinct from the conventional route of involving the Dzyaloshinskii-Moriya interaction
in a honeycomb magnet, the interplay of bond-dependent Kitaev and Γ interactions, originating
from the spin-orbit coupling and octahedra crystal field in real materials, has demonstrated to be
another source to generate noncollinear spin textures with multiple spins in a magnetic unit cell.
Notably, earlier works have revealed a triple-meron crystal (TmX) consisting of eighteen spins in
the frustrated Kitaev-Γ model. Aligning with previous efforts, here we attempt to identify that the
TmX hosts several peculiar features with the help of the linear spin-wave theory. To begin with, the
symmetric anisotropic exchanges are beneficial for the existence of nonreciprocal magnons, which are
stabilized by an external magnetic field. Further, within the regime of TmX, successive topological
phase transitions occur, accompanied by the changes of Chern number in value and thermal Hall
conductivity in sign. In addition, topological nature of magnons is also verified by the onset of chiral
edge modes in a nanoribbon geometry. Our findings pave the way to study topological phenomena
of noncollinear spin textures in potential Kitaev materials.

I.

INTRODUCTION

The theory of topological band structures has been extended beyond the electronic system to embrace topological magnon insulators and magnonic Dirac and Weyl
semimetals [1–3]. The magnons are the quanta of the
low-energy collective excitations which are ubiquitous in
magnetic materials. They are able to transfer spins without producing Joule heating and are believed to have
significant impacts on spintronics serving as ingredients
to low-energy consumption devices [4, 5]. As the inversion or time-reversal symmetry breaks, it is natural to
expect the magnon band structure to display nontrivial
topological signatures [6–9]. Of note is that a temperature gradient can induce a magnon flow, leading to the
thermal Hall effect due to a transversal magnon current
through the nonzero Berry curvature [10–22].
The Dzyaloshinskii-Moriya interaction has been well
recognized to obtain nontrivial magnon bands [1–3, 6, 8].
It not only acts as a virtual magnetic field but introduces
an effective non-Abelian gauge field for magnons, leaving
the possibility of nontrivial Berry curvature. Experimentally, the thermal Hall effect has been observed in various ferromagnetic insulators where the DzyaloshinskiiMoriya interaction is demonstrated to play a vital role
[23–26]. However, the Dzyaloshinskii-Moriya interaction is an antisymmetric exchange interaction that is in-

∗ qiangluo@nuaa.edu.cn
† zhaojz@lzu.edu.cn

duced by inversion symmetry breaking. It is thus either
symmetry-forbidden or usually acquires a small intensity
in further nearest-neighbor interactions. On the other
hand, quantum materials with bond-dependent Kitaevtype interactions emerge as the focus of experimental and
theoretical studies over the past years [27–36]. These
competing exchange couplings strongly promote the frustration, giving rise to exotic phases of matter such as
quantum spin liquids [37–39] and nematic paramagnet
[40, 41]. Notably, the Kitaev-type interactions, associated with the spin-orbit coupling, have been interpreted
as another source to generate topological magnon excitations [42–47]. The magnon bands of Kitaev honeyomb magnets can carry nonzero Chern number and chiral
edge modes at high magnetic field [42–44]. In addition,
the thermal hall conductivity undergoes a sign change
as the direction of the in-plane magnetic field reverses
[48]. Moreover, the abnormal phenomena in a couple of
thermal Hall measurements on α-RuCl3 [49–51], together
with other Kitaev materials like Na2 Co2 TeO6 [52, 53] and
MnPS3 [20], render the topological magnon as a promising carrier to dominate these tempting behaviors at low
temperatures.
Nevertheless, the topological magnon on a honeycomb
lattice has been so far mainly studied in strong or modest
magnetic field, at which the underlying spins are parallel or nearly parallel [42–44, 48, 54]. The topological
magnon in noncollinear spin textures with a large magnetic unit cell at a weak magnetic field thus calls for
an urgent study. It is revealed that the competition between the Kitaev and Γ interactions can generate many
noncoplanar magnetic orders [30, 45, 55–62], such as the

2
(6+18) state [45, 59, 60], the nested zigzag-stripy order
[58], and the C3 -like [59] triple-meron crystal (TmX) [60].
Among them, the TmX is extremely alluring in that it
has three merons within one magnetic unit cell and it occupies a large area in the phase diagram of the K-Γ model
where K < 0 and Γ > 0 [59, 60]. Thus, in this work, we
focus on the magnon excitation in such order with the
help of the linear spin-wave theory. Our results manifest
that nontrivial magnon band topology is widely present
within the parameter range of interest. The competition
between Kitaev and Γ interactions also produces topological phase transitions within the magnetically ordered
phase. In this respect, the non-reciprocity of magnons
is revealed and multiple topological phases are distinguished by the Chern number. Moreover, we calculate
the experimentally observable thermal Hall conductivity
and discuss its consistency with band topology at low
temperatures.

II.

MODEL AND METHODS

For the study of the topological magnon in a honeycomb lattice, the model is given by
i X
X h
KSiγ Sjγ + Γ(Siα Sjβ + Siβ Sjα ) +
H=
h · Si , (1)
⟨i,j⟩γ

i

where Si = (Six , Siy , Siz ) represents pseudospin operators
at site i. For simplicity, only the interactions among the
nearest-neighbor spins are considered. In the first two
terms, K and Γ are bond-directional exchange couplings
of the Kitaev and Γ terms, respectively. For each bond,
we can indicate an Ising axis γ and label the bond as
αβ(γ), with α and β representing the other two remaining components. Beyond the cubic {ex , ey , ez } axis, there
is a relevant crystallographic
{a, b, c} frame in
√ which
√
2, b = (−ex − ey + 2ez )/ 6, and
a = (−ex + ey )/ √
c = (ex + ey + ez )/ 3. In what follows, we will stick to
the {a, b, c} coordinate system [see the inset in Fig. 1(a)],
and the honeycomb lattice lies in the a-b plane. The last
term in Eq. (1) represents the magnetic field and its direction is perpendicular to honeycomb plane, i.e., h = hc.
In this work, we parameterize (K, Γ) = E0 (cos ϕ, sin ϕ)
and let h varies freely.
To obtain configurations of classical ground states
(S → ∞), we perform the parallel-tempering Monte
Carlo simulations in combination with heat-bath updates
and over-relaxation methods [63]. After the Monte Carlo
simulations, the classical ground state configurations can
be obtained by iteratively aligning the spins with their
local fields
P[64]. The static structure factor is given by
Sq = N12 ij Si · Sj eıq·(Ri −Rj ) , where N is the number
of sites and Ri is the location of spin at site i.
Then, we use the linear spin-wave theory to consider
magnon excitations in the magnetically ordered state. It
is implemented by the the Holstein-Primakoff approximation. When there are multiple spins in a magnetic

unit cell, the spin at site i can be expressed as [65]
r
S
Si =
(ūi b†i + ui bi ) + vi (S − b†i bi ),
2

(2)

where b†i (bi ) is bosonic creation (annihilation) operator. The auxiliary vector vi is the classical spin direction vi = Si /S = (sin θi cos ϕi , sin θi cos ϕi , cos θi ) while
vector ui can be calculated by ui = (cos θi cos ϕi −
ı sin ϕi , cos θi sin ϕi + ı cos ϕi , − sin θi ). After all spins
within the magnetic unit cell are quantized, we can write
the Hamiltonian in the reciprocal space as follows [30]
H = S(S + 1)E0 Eg +

E0 S X †
Ψ H q Ψq .
2 q q

(3)

Here, S 2 E0 Eg in the first part of Eq. (3) is the classical
ground-state energy, while the second part stands for the
quantum fluctuations due to magnons. Ψq = (bq , b†−q )T ,
bq = (b1q , . . . , bN q ) and N is the number of spins in one
magnetic unit cell. Thus, the matrix Hq can be divided
into four blocks,


Aq Bq
Hq =
,
(4)
B∗−q AT
−q
where Aq and Bq are both N -dimensional matrices. Of
note is that the contribution of the magnetic field has
been included in Eg and Hq . For example, it is added
to each diagonal element in the form of −h cos θi / (E0 S)
in the latter. The Hq is diagonalized by the Bogoliubov
transformation,
Ψ†q Hq Ψq = Ψ†q (Tq−1 )† [Tq† Hq Tq ]Tq−1 Ψq = Φ†q Eq Φq ,
(5)
where Tq is the transform matrix and

Eq = diag E1,q , . . . , EN ,q , E1,−q , . . . , EN ,−q
(6)
contains the magnon dispersions. Since Φq can also
†
)T where
be divided into two parts Φq = (βq , β−q
βq = (β1q , . . . , βN q ), the Bogoliubov transformation has
a more detailed form [66],



 


∗
bq
βq
βq
Uq V−q
= Tq
=
. (7)
†
†
†
∗
Vq U−q
b−q
β−q
β−q
We can obtain the Berry curvature of the n-th energy
band with the help of Tq matrix
Ωnq = −2Im

2N
X
(ΣT † ∂x Hq Tk )nm (ΣT † ∂y Hq Tk )mn
k

m=1
m̸=n

k

[(ΣEq )mm − (ΣEq )nn ]2

,

(8)
where Σ = diag(1N ×N , −1N ×N ). The Chern number
of magnon band n is the sum of Berry curvature in first
Brillouin zone,
Z
1
Cn =
Ωnq d2 q.
(9)
2π q∈FBZ

3

(a)

(d)

bx
y z
c
a

r2

y
x
Sc

1.0

r1

0.0

Enq

0.5
1.0

−0.5

(b)

qb

−1.0

0.5

0.08

0.0

(c)

0.06

qa

−0.5

0.04
0.02

−1.0

0.00

FIG. 1: (a) Top view of spin configuration in the TmX phase where ϕ = 0.64π and h/ (E0 S) = 0.1. The small arrows indicate
directions of spins and the colors are based on their out of plane components Sc . The magnetic unit cell is shown in the gray
area which includes eighteen spins. Two long pink arrows r1 and r2 represent the primitive vectors. The inset indicates the
{a, b, c} coordinate system and three kinds of bonds in the honeycomb lattice are labeled as x, y, and z, respectively. (b) The
first Brillouin zone is marked by the dashed line. The high-symmetry points and a special path in the reciprocal space are
shown. (c) The static structure factor of the configurations in (a). The ordering wave vector locates at 2M/3 point. (d) The
magnon band structure along the special path in (b) and the color in each band stands for the normalized Berry curvature.
The green zone declares that the lowest three magnon bands is well separated from the others with a global band gap.

III.

RESULTS

In our previous work [60], it is revealed that the TmX
can be realized in the dominant Γ region and stabilized
by the negative single-ion anisotropy or an out-of-plane
magnetic field in the Kitaev-Γ model. The typical spin
configuration of the TmX is shown in Fig. 1(a), and the
gray area containing eighteen spins marks the magnetic
unit cell (N = 18). It displays an intricate pattern in
which the core spins point along the c-axis while the
surrounding spins lie almost in the honeycomb plane.
Figure 1(c) presents the corresponding static structure
factor of the TmX, and a distinct ordering wave vector
located at 2M/3 point is observed. Of note is that such
an interesting order belongs to the degenerate manifold
of the classical honeycomb Γ model, and its spin-wave
energy is surprisingly equal to that of the four-sublattice
zigzag order [39]. The magnon band structure along the
high-symmetry points depicted in Fig. 1(b) is shown in
Fig. 1(d), and the color in each band stands for the normalized Berry curvature. It is observed that the lowest

magnon band acquires a sizeable excitation gap at the
Γ point, and the lowest three magnon bands are well
separated from the others with a global band gap. Further, as will be shown later, at least some of total Berry
curvature in the magnon bands does not cancel out, indicating that topologically nontrivial Chern number exists.
In what follows, we aim to unveil the topological phase
transitions within the TmX. Topological signatures such
as the thermal Hall conductivity and chiral edge modes
are also studied.
A.

Topological phase diagram

Despite great efforts, the notorious difficulty in mapping out the ground-state phase diagram of the KitaevΓ model remains unsolved even at the classical level
(for a review, see Ref. [62]). However, armed with advanced Monte Carlo methods, there has been a consensus on the recognition of the C3 -like TmX stemming
from the dominant Γ region. This phase is relatively
stable against ferromagnetic Kitaev interaction and ex-

4
(a)

I

II

III

IV

V

III

IV

V

(b)

I

II

φ/π
FIG. 2: (a) Topological phase diagram in the ϕ-h plane. Five
topological phases are distinguished through the Chern numbers and we distinguish them with Roman numerals I-V separately. (b) Behavior of the Chern numbers of the three lowest
bands when h/ (E0 S) = 0.1.

tends to a large regime in the presence of bond/single-ion
anisotropy [59, 60]. Meanwhile, we identify that the TmX
can survive on the existence of a small out-of-plane magnetic field, and the fact that the magnetic field can open
up the band gap is beneficial for the occurrence of topological magnons. Due to the competition between the
Kitaev and Γ interactions, as well as the enhancement
of magnetic field, it leaves the possibility of topological
phase transitions within the wide regime of TmX.
The Chern number associated with the Berry curvature is the most prominent quantity to capture topological phase transitions, which manifests itself by the
change in value. Figure 2(a) shows the topological phase
diagram of the TmX in the range of ϕ/π ∈ [0.56, 0.64]
and h/ (E0 S) ∈ [0.04, 0.12]. There are at least five
distinct topological phases which have different sets of
Chern numbers for the full magnon bands. Specifically,
sets of the Chern numbers (C1 , C2 , C3 ) of the lowest
three magnon bands are (−2, 2, 0), (1, −1, 0), (0, 0, 0),
(0, 1, −1), and (−1, 2, −1) for the phases ranging from
I to V. We note that the phase III is indeed topological
as its Chern number of the fifth magnon band is nonzero.
To further affirm the existence of topological phase transitions, we present the behaviors of Chern numbers in the
lowest three magnon bands as a function of ϕ at h/ (E0 S)
= 0.1, see Fig. 2(b). These curves clearly demonstrate
successive topological phase transitions via the change of
Chern numbers. In addition to topological phase transitions, we emphasize that there is no magnetic phase transition within the regime of TmX. This can be seen by the

facts that the first and second derivatives of the groundstate energy do not show any singularity, and intensities
of the out-of-plane moment and static structure factor at
2M/3 point are smoothly changed as ϕ varies (for illustration, see Appendix A). Therefore, similar to the spinflop phase identified in the extended Kitaev model [20],
our work provides another example where the topological phase transitions can occur even though the magnetic
phase transition is absent.
The nonreciprocal magnons come from the spatial inversion symmetry breaking [67, 68] and is
known to be stabilized by the dipole-dipole anisotropy,
the Dzyaloshinskii-Moriya interaction, the symmetric
anisotropic exchange, etc [68].
The nonreciprocal
magnon dispersions are stated as En,q ̸= En,−q , whereby
magnons at momentum q have different energy from
those at −q. They can be detected experimentally in
LiFe5 O8 and α-Cu2 V2 O7 , and the relevant physical phenomena such as nonreciprocal optical response and nonreciprocal spin Seebeck effect are also studied theoretically [67]. In this regard, it is naturally to ask if the
nonreciprocal magnons occur in the TmX. The configuration in the TmX has double degeneracy that the vertical
spins are at the different sublattices [60]. The nonreciprocal magnons are expected to appear since any of the
degenerate configurations breaks the sublattice symmetry.
Figure 3 shows the typical spin-wave dispersions Enq
and the Berry curvatures Ωnq of the lowest magnon band
(n = 1). As can be seen from Fig. 3(a), the nonreciprocal magnons are clearly reflected in the relation E1,q ̸=
E1,−q . This asymmetry is demonstrated by the energy
difference between the neighboring points at the corners
of the first Brillouin zone, i.e., δEn = |EnK1 − EnK2 |. It
is found that δEn is finite throughout the regime of TmX,
advocating the existence of nonreciprocal magnons. Interestingly, the kinks in the curves of δEn (n = 1, 2,
3) are coincident with the topological phase transitions,
see Appendix B. Further, as shown in Fig. 3(b), the
Berry curvatures Ω1,q are mostly concentrated around
the points pertaining band gaps. However, distributions
of the Berry curvatures throughout the first Brillouin
zone are rather distinct among different phases. To begin with, values of the Berry curvature in phases I, II,
or V are overwhelmingly negative or positive, leading to
a finite Chern number ultimately. The Chern numbers
of these three regimes are −2, 1, and −1, respectively.
Nevertheless, the Chern numbers in phase III and IV are
zero but their reasons are different. In phase III, both
area and intensity of the Berry curvature in the negative
and positive regimes are close, and the Chern number is
thus zero. By contrast, in phase IV, although intensities
of the Berry curvature at corners of the first Brillouin
zone are extremely large, area of the regime of positive
Brillouin zone is so small that it cancels with that of
the negative counterpart. Finally, the first four magnon
bands, together with the individually normalized Berry
curvature, are shown in Fig. 3(c). It is found that the

5

I: φ = 0.560π

II: φ = 0.580π

III: φ = 0.600π

IV: φ = 0.625π

V: φ = 0.640π

E1q

(a)

Ω1q

(b)

Enq

(c)

FIG. 3: (a) and (b) show the typical spin-wave dispersions Enq and the Berry curvatures Ωnq of each phase when h/ (E0 S) = 0.1.
Here, the lowest magnon bands with n = 1 are considered. (c) The band structure of the four lowest bands. The colors stand
for the normalized Berry curvature and the Chern number is indicated for each band.

fourth magnon bands of these topological phases always
acquire a zero Chern number and are well separated from
the lowest three with global band gaps. Recalling that
magnons follow the Bose-Einstein distribution, topological quantities of magnons should highly rely on the lowest
energy bands at low temperature. The above fact thus
highlights the importance of the role played by the lowest three bands. Also, the intricate relation between the
Berry curvature and magnon energy accounts for the elusive behaviors of various topological quantities.

B.

Chiral edge modes

The nontrivial band topology can be confirmed by calculating the chiral edge states in a nanoribbon geometry [8]. When the open boundary condition is adopted,
there will be chiral edge states connecting the upper and
lower energy bands. According to the bulk-edge correspondence, the number of pairs of edge states in the
nth band
P gap is consistent with the winding number
Wn = m≤n Cn [69]. We here consider the phase V since
it is the only case where both W1 ( = −1) and W2 ( = +1)
are nonzero. However, in contrast to the well recognized

cases where global band gaps exist, the first two global
band gaps are absent [as shown in Fig. 1(d)], challenging
the capture of well-defined edge states. Figure 4(a) shows
the magnon band structure on a nanoribbon geometry at
ϕ = 0.64π and h/ (E0 S) = 0.1. Strictly speaking, at the
edge of the open boundary, the configuration is no longer
a perfect TmX shape, but the influence of the boundary
will decrease as the system size increases. Therefore, we
ignore the influence of boundary conditions on the configuration, and construct the configuration of nanoribbon
geometry by translating a single TmX magnetic unit cell.
We manage to identify a pair of additional bands (shown
as red lines) connecting the upper and lower bulk bands.
These four bands are mixed with the bulk ones and are
only distinguishable at certain momentum intervals, leaving the possibility to study the chiral edge modes thereof.
We proceed to reveal the magnonic contribution of
the wave functions of these chiral edge modes in real
space. Following the definition proposed in Ref. [66], the
magnonic contribution at site i is given by
†
χi (q) = |⟨GS|biq βnq
|GS⟩|2 = |Uqi,n |2 ,

(10)

†
where βnq
|GS⟩ is the single magnon state and |GS⟩ is
the ground state that satisfies βnq |GS⟩ = 0. The matrix

6

(a)
D

Enq

C

B

A

element Uqi,n is the part of the transformation matrix
Tq , see Eq. (7). Figure 4(b) shows the magnonic contribution of four representative points labeled as A-D in
Fig. 4(a). It is thus clear that magnons are localized
at different edges of the nanoribbons, indicating these
additional bands are indeed chiral edge modes. In addition, we also calculate the magnonic contribution of other
bands that are equipped with the same band energy of
the individual points at A-D. It is observed that χi (q) is
almost uniformly distributed in the nanoribbon geometry and their intensities are rather small, advocating the
nontrivial properties of the chiral edge modes shown in
Fig. 4(b).
C.

Thermal Hall effect

Upon applying a longitudinal temperature gradient,
the nonzero Berry curvature can carry a transverse heat
current, leading to the magnon thermal Hall effect. It is
manifested by a nonzero thermal Hall conductivity (κab )
defined as [14],

0

v1/2

v1

(b)

r1
r2

κab = −

N Z
2
T X
kB
c2 [ρ (Enq )] Ωnq d2 q,
4π 2 ℏ n=1 q∈FBZ


where ρ(Enq ) = 1/ eE0 SEnq /kB T − 1 is the BoseEinstein distribution. The weighting function c2 (x) =
(1 + x) ln2 [(1 + x)/x] − ln2 (x) − 2Li2 (−x), with Li2 (x)
being the polylogarithm function.
Figure 5 shows behaviors of κab /T at five selected
points in each distinct topological phase. In the hightemperature limit, κab saturates to the value of [15]
XZ
2
κlim
=
f
racE
Sk
4π
ℏ
Enq Ωnq d2 q, (12)
0
B
ab
n

FIG. 4: (a) The magnon spin-wave dispersions on a nanoribbon geometry at ϕ = 0.64π and h/ (E0 S) = 0.1. The energy
bands that contain chiral edge modes are depicted in red.
The periodic boundary condition is used along r1 direction
while open boundary condition is used along r2 direction.
The length in r2 direction is 20 times the primitive vector
while in r1 direction it equals to the primitive vector. The v1
in the horizontal axis is the inverse primitive vector of r1 . (b)
The intensities reveal the real space magnonic contribution
χi (q) at four representative points (labeled as A-D in (a))
with chiral edge modes. The r1 direction is enlarged twice for
better visual effect.

(11)

q∈FBZ

indicating that κab /T obeys the law of ∝ T −1 at sufficiently large temperature. As inferred from Eq. (12),
the saturation value depends on the distributions of dispersion relation and Berry curvature of each band. It is
observed from Fig. 5 that the saturation value decreases
with the increase of ϕ. Further, κab /T displays a pronounced peak at each curve. The magnitudes (in unit
2
of πkB
/ (6ℏ)) are smaller than 1/2, the half-quantized
value in the case of majorana fermion. By contrast, positions of these peaks are insensitive to ϕ and are close
to kB T / (E0 S) ≈ 0.7. It is interesting to note that the
energy scale of this temperature falls in the global band
gap that separates the lowest three magnon band with
others [see Fig. 1(d)]. This result demonstrates that the
former plays a vital role in the low-temperature thermal
Hall conductivity. As seen from inset of Fig. 5, κab /T
opens up exponentially when T is relatively small. As
T further increases, there are kind of enhancement of
κab /T in the curves of ϕ/π = 0.56 (phase I) and 0.64
(phase V). This may result from the higher Chern number of 2 existed in the lowest three magnon bands. Note-

7
worthily, when ϕ/π = 0.625 (phase IV), κab /T undergoes an appreciable sign change from negative to positive at kB T / (E0 S) ≃ 0.21. Notice that the first magnon
band is trivial, the negative thermal Hall conductivity at
low temperature is thus attributed to the second magnon
band which owns a Chern number of +1. The interplay
of the lowest three magnon bands is shown in Appendix
C.

(a)

(b)

IV

2
/ (6ℏ)) as a function of T for
FIG. 5: κab /T (in units of πkB
different ϕ that belong to phase I-V separately. The inset
shows the magnified results of the low-temperature. In region with relatively high temperature up to kB T / (E0 S) ≲ 8,
we consistently ignore the influence of thermal fluctuations
on magnetic configurations and the magnon-magnon interactions.

To better visualize the sign change in κab at low temperature, we present the contour plot of κab in Fig. 6(a)
as a function of T in the regime of TmX. At low temperatures [e.g., kB T / (E0 S) = 0.02], signs of kxy are basically positive in phases I and II, while they are negative in phases III, IV, and V. Since signs of κab in all
the five phases are positive at large enough temperature,
the latter are expected to undergo sign changes as T is
further lifted. Of note is that the sign change in phase
IV is the most prominent and it remains negative when
kB T / (E0 S) ≲ 0.21. Figure 6(b) shows κab as a function of ϕ for four different temperatures. At each temperature, κab changes nonmonotonously with ϕ and the
unusual behaviors may have a plausible relation to the
underlying topological phase transitions. Specifically, it
is observed that the sign of κab in phase IV is different
from its neighboring phases. For the selected temperatures kB T / (E0 S) = 0.08, 0.12, and 0.16, locations of
the sign changes are robust and coincide nicely with the
phase boundaries of phase IV (see the shaded pink region). Our result reveals that the sign change of thermal
Hall conductivity is amenable to serve as a diagnosis of
topological phase transitions.

FIG. 6: (a) The contour plot of κab in as a function of T
and ϕ. (b) shows κab as a function of ϕ for four different
temperatures. The shaded pink region indicates the range of
phase IV.

IV.

CONCLUSIONS

In this paper, we have studied the topological phase
transitions and nontrivial thermal Hall effect in a
noncollinear spin texture termed triple-meron crystal
(TmX). It is discovered that the TmX occupies a large
parameter region near the Γ limit and is stabilized by
the out-of-plane magnetic field in the Kitaev-Γ model
through parallel-tempering Monte Carlo simulations.
Further, we obtain the magnon dispersions and Berry
curvatures successfully with the help of the linear spinwave theory, from which the Chern number, chiral edge
mode, and thermal Hall conductivity can be calculated.
Throughout the regime of TmX, we map out a topological phase diagram by the Chern number and identify
five distinct topological phases therein. Due to the existence of symmetric anisotropic exchanges, the topological
magnons display nonreciprocal structures and the behavior of nonreciprocity is helpful to reveal the underlying
topological phase transitions. The topological nature of
magnons is also verified by the onset of chiral edge modes
in a nanoribbon geometry. We confirm that the pair of
nontrivial edge states equals to that of the winding number at the corresponding band level. Finally, we observe
that the thermal Hall conductivity (κab ) enjoys a sign
change at low temperature in some parameter region and
the peak of κab /T is modest and comparable to the half-

8
quantized value due to majorana fermion. Guided by the
topological phase diagram, we can relate the sign change
in κab to a certain species of topological phase transition.
The significance of our work lies in that it underscores
topological magnons in a noncollinear spin texture stabilized by Kitaev interactions, thus it should illuminate
future studies of bosonic topological band theory on Kitaev materials. In addition to the content presented in
this article, there are still some issues worth further research. First of all, while we have predicated that the
TmX can be realized in higher-spin Kitaev magnets, potential candidates are still lacking. We thus hope that
our finding could stimulate the synthesis of proper materials so as to solidify the topological magnons. Next,
the magnon-magnon interactions may lead to the decay
of quasiparticles [70–75] or make them more stable [76].
Recent works have also pointed out that the magnonmagnon interactions may have a promoting effect on the
formation of band topology [72, 77]. Hence, it is meaningful to further discuss the relevant fields based on our
work. Finally, since the phonons are omnipresent and
play a crucial role in the low-energy thermal transport,
it is necessary to analyze the effect of spin-lattice coupling on the thermal Hall conductivity of certain materials [78–80].

(a)

(b)

φ/π
FIG. 7: (a) The first-order ∂Eg /∂(ϕ/π) and second-order
∂ 2 Eg /∂(ϕ/π)2 derivatives of the ground-state energy per site.
(b) The square of the out-of-plane component of spin ⟨Sc2 ⟩ and
static structure factor Sq at q = 2M/3 point.

that there is no magnetic phase transition in the regime
of TmX.
Acknowledgments

We would like to thank Satoru Hayami for helpful discussions. This work is supported by the National Key
R&D Program of China (Grants No. 2022YFA1402704),
by the National Natural Science Foundation of China
(Grants No. 12274187, No. 12304176, No. 12247183,
No. 12247101, No. 11834005), and by the Natural Science Foundation of Jiangsu Province (Grant No.
BK20220876). The computations are partially supported
by High Performance Computing Platform of Nanjing
University of Aeronautics and Astronautics (NUAA).

Appendix A: Absence of magnetic phase transition

We note that there is no magnetic phase transition
within the wide regime of TmX under a small magnetic
field. As a comparison, a series of topological phases are
recognized in the TmX, see Fig. 2(a). In this appendix,
we focus on the line h/ (E0 S) = 0.1 as an example to
confirm the absence of magnetic phase transition. Figure 7(a) shows the first-order ∂Eg /∂(ϕ/π) and secondorder ∂ 2 Eg /∂(ϕ/π)2 derivatives of the ground-state energy as a function of ϕ. These curves are smooth enough,
ruling out a possibility of displaying kink, jump, or divergence. Further, square of the out-of-plane component
of spin ⟨Sc2 ⟩ and static structure factor Sq at q = 2M/3
point are shown in Fig. 7(b). They are also smoothly varied as ϕ, indicating that the magnetic phase transition is
unlikely to occur. Taken together, it is safely to conclude

Appendix B: Evidence of nonreciprocal magnons

The high symmetry points K1 and K2 have opposite positions q in reciprocal space. According to the
spin-wave dispersions shown in Fig. 3(a), the quantity
δEn = |EnK1 − EnK2 | serves as an indicator of nonreciprocity. Figure 8 shows δEn (n = 1, 2, 3) as a
function of ϕ when h/ (E0 S) = 0.1. Apparently, all
the δEn ’s are finite and their values becomes larger and
larger averagely as n increases, confirming the existence
of nonreciprocal magnons. In addition, it is interesting
to note that δEn ’s have an implicit relation to the underlying topological phase transitions. As can be seen
from Fig. 3(c), due to the nonreciprocity of magnons,
the difference in band gaps between K1 and K2 points
is significant. When a phase transition occurs, the energy band only closes at one point among them, and the
Berry curvature corresponding to this point contributes
the most to the Chern number. This further leads to the
connection between topological phase transitions and the
quantity δEn = |EnK1 − EnK2 |. For example, δE1 has
two kinks at II-III and IV-V transitions, δE2 has three
kinks at II-III, III-IV, and IV-V transitions, while δE3
has one kink at III-IV transition. These kinks are precisely located at the topological phase transition points.
In addition, δEn do not show a kink at I-II transition.
This is because the closure point of the energy band is no
longer the K1 or K2 point during such topological phase
transition.

9

V
I

II

III

IV

FIG. 8: The difference in magnon energy at K1 and K2 points
of band n (= 1, 2, 3) as a function of ϕ.

Appendix C: Dissecting the thermal Hall
conductivity in phase IV

As seen from Fig. 6(a), the thermal Hall conductivity
of phase IV has a sizable negative value when the temperature is small, and it becomes positive as the temperature
increases. Since the lowest three magnon bands have a

[1] P. A. McClarty, Topological Magnons: A Review, Annu.
Rev. Condens. Matter Phys. 13, 171 (2022).
[2] Z.-X. Li, Y. Cao, and P. Yan, Topological insulators
and semimetals in classical magnetic systems, Phys. Rep.
915, 8 (2021).
[3] F. Zhuo, J. Kang, A. Manchon, and Z. Cheng, Topological phases in magnonics: A review, Adv. Phys. Res.
2023, 2300054 (2023).
[4] B. Lenk, H. Ulrichs, F. Garbs, and M. Münzenberg,
The building blocks of magnonics, Phys. Rep. 507, 107
(2011).
[5] A. V. Chumak, V. I. Vasyuchka, A. A. Serga, and B.
Hillebrands, Magnon spintronics, Nat. Phys. 11, 453
(2015).
[6] L. Zhang, J. Ren, J.-S. Wang, and B. Li, Topological
magnon insulator in insulating ferromagnet, Phys. Rev.
B. 87, 144101 (2013).
[7] R. Shindou, R. Matsumoto, S. Murakami, and J.-i. Ohe,
Topological chiral magnonic edge mode in a magnonic
crystal, Phys. Rev. B. 87, 174427 (2013).
[8] A. Mook, J. Henk, and I. Mertig, Edge states in topological magnon insulators, Phys. Rev. B. 90, 024412 (2014).
[9] K. Nakata, S. K. Kim, J. Klinovaja, and D. Loss,
Magnonic topological insulators in antiferromagnets,
Phys. Rev. B. 96, 224414 (2017).
[10] H. Katsura, N. Nagaosa, and P. A. Lee, Theory of the
Thermal Hall Effect in Quantum Magnets, Phys. Rev.
Lett. 104, 066403 (2010).
[11] T. Qin, Q. Niu, and J. Shi, Energy Magnetization and

significant contribution to thermal Hall conductivity at
low temperatures, here we calculate their thermal Hall
conductivity separately. We recall that the first three
Chern numbers in this phase are (0, 1, −1). As the Berry
curvature cancels out in the first band, it means that this
band plays an insignificant role when compared with the
remaining two. As shown in Fig. 9, the contribution of
first band is indeed tiny except at the low enough temperature and is two orders smaller than that of the second and third bands when kB T / (E0 S) = 0.3. According
to the definition in Eq. (11), the sign of thermal Hall
conductivity is generally opposing to its Chern number.
Thus, the signs of thermal Hall conductivity in the second
and third bands are negative and positive, respectively.
Notably, it is seen that band 2 completely offsets the
contributions of bands 1 and 3, resulting in a negative
thermal Hall conductivity in the low-temperature region
(see the purple dotted line). As a comparison, we also
present the total contribution of all eighteen bands, and
the two curves are relatively consistent when kB T / (E0 S)
is less than 0.16. As the temperature increases, the total
thermal conductivity of the three lowest bands remains
negative, while the thermal conductivity of the total eighteen bands begins to increase and changes its sign at
kB T / (E0 S) ≈ 0.21, indicating that higher magnon bands
begin to play a vital role afterwards.

2
FIG. 9: κab /T (in units of πkB
/ (6ℏ)) as a function of T at
a representative point (ϕ = 0.625π,h/ (E0 S) = 0.1) in phase
IV. The curves n = 1, 2, 3 are the results coming from the
individual band. Results of total three lowest bands n = 1 →
3 and all eighteen bands n = 1 → 18 are also provided.

the Thermal Hall Effect, Phys. Rev. Lett. 107, 236601
(2011).
[12] R. Matsumoto and S. Murakami, Theoretical Prediction
of a Rotating Magnon Wave Packet in Ferromagnets,

10
Phys. Rev. Lett. 106, 197202 (2011).
[13] T. Ideue, Y. Onose, H. Katsura, Y. Shiomi, S. Ishiwata,
N. Nagaosa, and Y. Tokura, Effect of lattice geometry
on magnon Hall effect in ferromagnetic insulators, Phys.
Rev. B. 85, 134411 (2012).
[14] R. Matsumoto, R. Shindou, and S. Murakami, Thermal
Hall effect of magnons in magnets with dipolar interaction, Phys. Rev. B. 89, 054420 (2014).
[15] A. Mook, J. Henk, and I. Mertig, Magnon Hall effect and
topology in kagome lattices: A theoretical investigation,
Phys. Rev. B. 89, 134409 (2014).
[16] S. Murakami and A. Okamoto, Thermal Hall Effect of
Magnons, J. Phys. Soc. Jpn. 86, 011010 (2017).
[17] A. Mook, J. Henk, and I. Mertig, Thermal Hall effect in
noncollinear coplanar insulating antiferromagnets, Phys.
Rev. B 99, 014427 (2019).
[18] Y.-f. Yang, G.-M. Zhang, and F.-C. Zhang, Universal
Behavior of the Thermal Hall Conductivity, Phys. Rev.
Lett. 124, 186602 (2020).
[19] H. Xu, S.-f. Cheng, S. Bao, J.-S. Wen, Experimental Progress in Thermal Hall Conductivity Research
on Strongly Correlated Electronic Systems, Progress in
Physics 42, 159-183 (2022).
[20] R. R. Neumann, A. Mook, J. Henk, and I. Mertig, Thermal Hall Effect of Magnons in Collinear Antiferromagnetic Insulators: Signatures of Magnetic and Topological
Phase Transitions, Phys. Rev. Lett. 128, 117201 (2022).
[21] M.-H. Zhang, and D.-X. Yao, Topological magnons on
the triangular kagome lattice, Phys. Rev. B. 107, 024408
(2023).
[22] X.-T. Zhang, Y. H. Gao, G. Chen, Thermal Hall effects
in quantum magnets, Phys. Rep. 1070, 1 (2024).
[23] Y. Onose, T. Ideue, H. Katsura, Y. Shiomi, N. Nagaosa,
and Y. Tokura, Observation of the Magnon Hall Effect,
Science 329, 297 (2010).
[24] R. Chisnell, J.S. Helton, D.E. Freedman, D.K. Singh, R.I.
Bewley, D.G. Nocera, and Y.S. Lee, Topological Magnon
Bands in a Kagome Lattice Ferromagnet, Phys. Rev.
Lett. 115, 147201 (2015).
[25] M. Hirschberger, J. W. Krizan, R. J. Cava, and N. P.
Ong, Large thermal Hall conductivity of neutral spin excitations in a frustrated quantum magnet, Science 348,
106 (2015)
[26] M. Hirschberger, R. Chisnell, Y. S. Lee, and N.P. Ong,
Thermal Hall Effect of Spin Excitations in a Kagome
Magnet, Phys. Rev. Lett. 115, 106603 (2015).
[27] S. Trebst, C. Hickey, Kitaev materials, Phys. Rep. 950,
1 (2022).
[28] S. M Winter, A. A Tsirlin, M. Daghofer, J. van den Brink,
Y. Singh, P. Gegenwart and R. Valentı́, Models and materials for generalized Kitaev magnetism, J. Phys.: Condens. Matt. 29, 493002 (2017).
[29] K. Ran, J. Wang, W. Wang, Z.-Y. Dong, X. Ren, S.
Bao, S. Li, Z. Ma, Y. Gan, Y. Zhang, J. T. Park, G.
Deng, S. Danilkin, S.-L. Yu, J.-X. Li, and J. Wen, SpinWave Excitations Evidencing the Kitaev Interaction in
Single Crystalline α-RuCl3 , Phys. Rev. Lett. 118, 107203
(2017).
[30] L. Janssen, and M. Vojta, Heisenberg−Kitaev physics
in magnetic fields, J. Phys.: Condens. Matt. 31, 423002
(2019).
[31] C. Xu, J. Feng, H. Xiang, and L. Bellaiche, Interplay
between Kitaev interaction and single ion anisotropy in
ferromagnetic CrI3 and CrGeTe3 monolayers, npj Com-

put. Mater. 4, 57 (2018).
[32] I. Lee, F. G. Utermohlen, D. Weber, K. Hwang, C.
Zhang, J. van Tol, J. E. Goldberger, N. Trivedi, and
P. C. Hammel, Fundamental spin interactions underlying the magnetic anisotropy in the Kitaev ferromagnet
CrI3 , Phys. Rev. Lett. 124, 017201 (2020).
[33] G. Lin, et al., Field-induced quantum spin disordered
state in spin-1/2 honeycomb magnet Na2 Co2 TeO6 , Nat.
Commun. 12, 5559 (2021).
[34] X. Li, Y. Gu, Y. Chen, V. O. Garlea, K. Iida, K. Kamazawa, Y. Li, G. Deng, Q. Xiao, X. Zheng, Z. Ye, Y.
Peng, I. A. Zaliznyak, J. M. Tranquada, and Y. Li, Giant
Magnetic In-Plane Anisotropy and Competing Instabilities in Na3 Co2 SbO6 , Phys. Rev. X 12, 041024 (2022).
[35] W. Yao, Y. Zhao, Y. Qiu, C. Balz, J. R. Stewart, J.
W. Lynn, and Y. Li, Magnetic ground state of the
Na2 Co2 TeO6 Kitaev spin liquid candidate, Phys. Rev.
Res. 5, L022045 (2023).
[36] G. Lin, J. Jiao, X. Li, M. Shu, O. Zaharko, T. Shiroka,
T. Hong, A. I. Kolesnikov, G. Deng, S. Dunsiger, H.
Zhou, T. Shang, and J. Ma, Static magnetic order with
strong quantum fluctuations in spin-1/2 honeycomb magnet Na2 Co2 TeO6 , arXiv:2312.06284 (2023).
[37] J. Wang, B. Normand, and Z.-X. Liu, One Proximate Kitaev Spin Liquid in the K-J-Γ Model on the Honeycomb
Lattice, Phys. Rev. Lett. 123, 197201 (2019).
[38] A. Ralko and J. Merino, Novel Chiral Quantum Spin Liquids in Kitaev Magnets, Phys. Rev. Lett. 124, 217203
(2020).
[39] Q. Luo, J. Zhao, H.-Y. Kee, and X. Wang, Gapless quantum spin liquid in a honeycomb Γ magnet, npj Quantum
Mater. 6, 57 (2021).
[40] H.-Y. Lee, R. Kaneko, L. E. Chern, T. Okubo, Y. Yamaji,
N. Kawashima, and Y. B. Kim, Magnetic-field induced
quantum phases in tensor network study of Kitaev magnets, Nat. Commun. 11, 1639 (2020).
[41] M. Gohlke, L. E. Chern, H.-Y. Kee, and Y. B. Kim,
Emergence of nematic paramagnet via quantum orderby-disorder and pseudo-Goldstone modes in Kitaev magnets, Phys. Rev. Research 2, 043023 (2020).
[42] P. A. McClarty, X.-Y. Dong, M. Gohlke, J. G. Rau,
F. Pollmann, R. Moessner, and K. Penc, Topological
magnons in Kitaev magnets at high fields, Phys. Rev.
B. 98, 060404(R) (2018).
[43] D. G. Joshi, Topological excitations in the ferromagnetic
Kitaev-Heisenberg model, Phys. Rev. B. 98, 060405(R)
(2018).
[44] Z.-X. Luo and G. Chen, Honeycomb rare-earth magnets with anisotropic exchange interactions SciPost Phys.
Core 3, 004 (2020).
[45] L. E. Chern, R. Kaneko, H.-Y. Lee, and Y. B. Kim, Magnetic field induced competing phases in spin-orbital entangled Kitaev magnets, Phys. Rev. Research 2, 013014
(2020).
[46] E. Aguilera, R. Jaeschke-Ubiergo, N. Vidal-Silva, Luis E.
F. Foa Torres, and A. S. Nunez, Topological magnonics
in the two-dimensional van der Waals magnet CrI3 , Phys.
Rev. B 102, 024409 (2020).
[47] E. Z. Zhang, L. E. Chern, and Y. B. Kim, Topological magnons for thermal Hall transport in frustrated
magnets with bond-dependent interactions, Phys. Rev.
B 103, 174402 (2021).
[48] L. E. Chern, E. Z. Zhang, and Y. B. Kim Sign Structure
of Thermal Hall Conductivity and Topological Magnons

11
for In-Plane Field Polarized Kitaev Magnets, Phys. Rev.
Lett. 126, 147201 (2021).
[49] Y. Kasahara, T. Ohnishi, Y. Mizukami, O. Tanaka, Sixiao Ma, K. Sugii, N. Kurita, H. Tanaka, J. Nasu, Y. Motome, T. Shibauchi, and Y. Matsuda, Majorana quantization and half-integer thermal quantum Hall effect in a
Kitaev spin liquid, Nature 559, 227 (2018).
[50] P. Czajka, T. Gao, M. Hirschberger, P. Lampen-Kelley,
A. Banerjee, J. Yan, D. G. Mandrus, S. E. Nagler, and N.
P. Ong, Oscillations of the thermal conductivity in the
spin-liquid state of α- RuCl3 , Nat. Phys. 11, 915 (2021).
[51] H.-Y. Kee, Thermal Hall conductivity of α- RuCl3 , Nat.
Mater. 22, 6 (2023).
[52] H. Takeda, J. Mai, M. Akazawa, K. Tamura, J. Yan,
K. Moovendaran, K. Raju, R. Sankar, K.-Y. Choi, and
M. Yamashita, Planar thermal Hall effects in the Kitaev
spin liquid candidate Na2 Co2 TeO6 , Phys. Rev. Research
4, L042035 (2022).
[53] S. Guang, N. Li, R. L. Luo, Q. Huang, Y. Wang, X.
Yue, K. Xia, Q. Li, X. Zhao, G. Chen, H. Zhou, and
X. Sun, Thermal transport of fractionalized antiferromagnetic and field-induced states in the Kitaev material
Na2 Co2 TeO6 , Phys. Rev. B 107, 184423 (2023).
[54] Q. Luo and H.-Y. Kee, Interplay of magnetic field and
trigonal distortion in the honeycomb Γ model: Occurrence of a spin-flop phase, Phys. Rev. B 105, 174435
(2022).
[55] J. G. Rau, E. K.-H. Lee, and H.-Y. Kee, Generic Spin
Model for the Honeycomb Iridates beyond the Kitaev
Limit, Phys. Rev. Lett. 112, 077204 (2014).
[56] L. E. Chern, Finn L. Buessen, and Y. B. Kim, Classical
magnetic vortex liquid and large thermal Hall conductivity in frustrated magnets with bond-dependent interactions, npj Quantum Mater. 6, 33 (2021).
[57] K. Liu, N. Sadoune, Nihal Rao, J. Greitemann, and L.
Pollet, Revealing the phase diagram of Kitaev materials
by machine learning: Cooperation and competition between spin liquids, Phys. Rev. Research 3, 023016 (2021).
[58] N. Rao, K. Liu, M. Machaczek, and L. Pollet, Machinelearned phase diagrams of generalized Kitaev honeycomb
magnets, Phys. Rev. Research 3, 033223 (2021).
[59] A. Rayyan, Q. Luo, and H.-Y. Kee, Extent of frustration in the classical Kitaev-Γ model via bond anisotropy,
Phys. Rev. B 104, 094431 (2021).
[60] K. Chen, Q. Luo, Z. Zhou S. He, B. Xi, C. Jia, H.-G. Luo
and J. Zhao, Triple-meron crystal in high-spin Kitaev
magnets, New J. Phys. 25, 023006 (2023).
[61] P. P. Stavropoulos, Y. Yang, I. Rousochatzakis, and N.
B. Perkins, Complex orders and chirality in the classical
Kitaev-Γ model, arXiv:2311.00037 (2023).
[62] I. Rousochatzakis, N. B. Perkins, Q. Luo, and H. Y. Kee,
Beyond Kitaev physics in strong spin-orbit coupled magnets, Rep. Prog. Phys. 87, 026502 (2024).
[63] K. Hukushima and K. Nemoto, Exchange Monte Carlo
method and application to spin glass simulations, J.
Phys. Soc. Jpn. 65, 1604 (1996).
[64] L. Janssen, E. C. Andrade, and M. Vojta, HoneycombLattice Heisenberg-Kitaev Model in a Magnetic Field:

Spin Canting, Metamagnetism, and Vortex Crystals,
Phys. Rev. Lett. 117, 277202 (2016).
[65] S. Toth and B. Lake, Linear spin wave theory for single-Q
incommensurate magnetic structures, J. Phys.: Condens.
Matter 27, 166002 (2015).
[66] S. A. Dı́az, J. Klinovaja, and D. Loss, Topological Magnons and Edge States in Antiferromagnetic
Skyrmion Crystals, Phys. Rev. Lett. 122, 187203 (2019).
[67] T. Matsumoto, and S. Hayami, Nonreciprocal magnons
due to symmetric anisotropic exchange interaction in
honeycomb antiferromagnets, Phys. Rev. B. 101, 224419
(2020).
[68] S. Hayami, and T. Matsumoto, Essential model parameters for nonreciprocal magnons in multisublattice systems, Phys. Rev. B. 105, 014404 (2022).
[69] Y. Hatsugai, Chern number and edge states in the integer
quantum Hall effect, Phys. Rev. Lett. 71, 3697 (1993).
[70] M. E. Zhitomirsky and A. L. Chernyshev, Colloquium:
Spontaneous magnon decays, Rev. Mod. Phys. 85, 219
(2013).
[71] A. Mook, J. Klinovaja, and D. Loss, Quantum damping of skyrmion crystal eigenmodes due to spontaneous
quasiparticle decay, Phys. Rev. Research 2, 033491
(2020).
[72] A. Mook, K. Plekhanov, J. Klinovaja, and D. Loss,
Interaction-Stabilized Topological Magnon Insulator in
Ferromagnets, Phys. Rev. X 11, 021061 (2021).
[73] J. Habel, A. Mook, J. Willsher, and J. Knolle, Breakdown
of chiral edge modes in topological magnon insulators,
Phys. Rev. B 109, 024441 (2024).
[74] Y.-S. Lu, J.-L. Li, and C.-T. Wu, Topological Phase
Transitions of Dirac Magnons in Honeycomb Ferromagnets, Phys. Rev. Lett. 127, 217202 (2021).
[75] S. Koyama and J. Nasu, Flavor-wave theory with quasiparticle damping at finite temperatures: Application to
chiral edge modes in the Kitaev model, Phys. Rev. B
108, 235162 (2023).
[76] R. Verresen,R. Moessner, F. Pollmann, Avoided quasiparticle decay from strong quantum interactions, Nat.
Phys. 15, 750 (2019).
[77] M. Gohlke, A. Corticelli, R. Moessner, P. A. McClarty,
and A. Mook, Spurious Symmetry Enhancement in Linear Spin Wave Theory and Interaction-Induced Topology
in Magnons, Phys. Rev. Lett. 131, 186702 (2023).
[78] N. Li, R. R. Neumann, S. K. Guang, Q. Huang, J. Liu, K.
Xia, X. Y. Yue, Y. Sun, Y. Y. Wang, Q. J. Li, Y. Jiang, J.
Fang, Z. Jiang, X. Zhao, A. Mook, J. Henk, I. Mertig, H.
D. Zhou, and X. F. Sun, Magnon-polaron driven thermal
Hall effect in a Heisenberg-Kitaev antiferromagnet, Phys.
Rev. B 108, L140402 (2023).
[79] Y. Choi, H. Yang, J. Park, and J.-G. Park, Sizable suppression of magnon Hall effect by magnon damping in
Cr2 Ge2 Te6 , Phys. Rev. B 107, 184434 (2023).
[80] C. Xu, H. Zhang, C. Carnahan, P. Zhang, D. Xiao, and X.
Ke, Thermal Hall effect in the van der Waals ferromagnet
CrI3 , Phys. Rev. B 109, 094415 (2024).


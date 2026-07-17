<!-- Extraction method: pdftotext FALLBACK (marker CLI unavailable on host). arxiv_id=2607.15228 -->

Magnetic Order in bilayer Ruddlesden-Popper Nickelates
Yiming Wang,1, ∗ Guijing Duan,2, ∗ Zhiguang Liao,2 Kuan-Sen Lin,1 Rong Yu,2, † and Qimiao Si1, ‡
1

Department of Physics & Astronomy, Extreme Quantum Materials Alliance,
Smalley-Curl Institute, Rice University, Houston, Texas 77005, USA
2
School of Physics and Key Laboratory of Quantum State Construction and Manipulation (Ministry of Education),
Renmin University of China, Beijing, 100872, China

arXiv:2607.15228v1 [cond-mat.supr-con] 16 Jul 2026

The recent discovery of high-temperature superconductivity in the bilayer nickelate La3 Ni2 O7 has
led to extensive interest in the correlation physics of its normal state. Given that the superconducitivity develops near a density wave order in the phase diagram, it is important to elucidate
the nature of this order. Based on the accumulated experimental evidence for a bad metal state in
proximity to an orbital-selective Mott phase, here we describe magnetic correlations of the system in
a conceptually new way – in terms of effective local moments experiencing a combination of RKKY
and superexchange interactions. This gives rise to a magnetic order with a wavevector that is close to
Q = (π/2, π/2) and, at the same time, yields a clear understanding of the associated spin dynamics.
Our results are consistent with the rapidly emerging experiments about the magnetic correlations in
the density wave order of the bilayer nickelate. Implications for unconventional superconductivity
in this and related multiorbital systems are discussed.

Introduction. Bilayer nickelate La3 Ni2 O7 shows high
temperature superconductivity both in bulk crystals under pressure [1] and in thin films at ambient pressure [2–
4]. The discovery has motivated extensive experimental investigations on this and related Ruddlesden-Popper
nickelates [5–12]. It also opens a new window into the
understanding of the basic physics of high temperature
and unconventional supercondcutors and, as such, led
to enormous theoretical efforts [13–46]. Importantly,
optical conductivity and angle resolved photoemission
spectroscopy (ARPES) measurements at ambient pressure have provided fairly direct evidence for the importance of orbital-selective electron correlations [47, 48].
These spectroscopic experiments are captured in terms
of bad metallicity with orbital-selective Mott correlations [13, 49, 50]. Combined with first-principles studies,
it has become clear that the low-energy physics is primarily governed by Ni 3d electrons in the eg manifold –
the strongly hybridizing 3dx2 −y2 and 3dz2 orbitals [51].
The dx2 −y2 orbitals predominantly dictate the in-plane
intralayer hopping, whereas the dz2 orbitals facilitate
strong interlayer coupling, creating a highly anisotropic
electronic environment.
While epitaxial strain enables superconductivity in
thin films at ambient pressure, the bulk compound under ambient conditions is known to exhibit an electronic
density-wave order at low temperatures (below about
150 K). We start from the salient experimental observations about this density-wave order at the ambient pressure. Local probes have played an integral role. Zerofield muon spin resonance (µSR) measurements reported
bulk magnetic order below TN ≃ 154 K, with oxygen
deficiency broadening the internal field distribution [52].
Consistently, 139 La nuclear magnetic resonance (NMR)
measurements found a magnetic transition around the
same temperature [53]. More recently, 139 La nuclear
quadrupolar resonance (NQR) measurements indicated

that charge modulation and magnetic broadening appear
together below TDW ∼ 153 K [54]. These results implicate the spin and charge correlations of the system at
ambient conditions.
As a more direct motivation, recent scattering measurements have begun to clarify the structure and dynamics of the ordered state. Resonant inelastic x-ray
spectroscopy (RIXS) in a bilayer nickelate observed welldefined magnetic excitations [55], while resonant soft xray scattering has revealed a related magnetic order [56].
Neutron diffraction subsequently resolved the magnetic
structure, with magnetic scattering appearing below approximately 150 K and an antiferromagnetic stacking of
the two layers within a bilayer [57, 58]. Most directly, recent inelastic neutron scattering measurements on singlecrystalline La3 Ni2 O7 observed spin excitations centered
near (0, 0.5, 2.5) [corresponding to an in-plane wavevector
(π/2, π/2) in the unfolded 1-Ni Brillouin zone] [59].
It is believed that the density-wave order comes from
the same electronic degrees of freedom (the aforementioned Ni 3d-electrons in the eg manifold) that are responsible for the correlated normal state and superconductivity. Accordingly, understanding the nature of the
density wave order is a key to elucidating the microscopic
physics of this high temperature superconductor. The
theoretical approach to this issue is still limited, mostly
from a weak coupling Fermi surface nesting instabilities
[60–62] or the strong coupling limit with purely localized moments experiencing superexchange interactions
[63, 64]. How to approach this problem building on the
understanding about the normal state remains an open
issue.
In this work, we propose a theoretical framework that
is anchored by the orbital-selective correlations experimentally observed in the normal state [13, 49]. The
latter is illustrated in Fig. 1(a). This regime, shown as
bad metal, is in proximity to an orbital selective Mott

2
system by a bilayer two-orbital Hubbard model H =
HTB + Hint . Here, the kinetic part is described by a
tight-binding (TB) Hamiltonian:
X αβ †
X
HTB =
til,jl′ dilασ djl′ βσ +
ϵα d†ilασ dilασ (1)
ijll′ αβσ

ilασ

where the tαβ
il,jl′ and ϵα refer to hopping integrals and
crystal-field levels taken from Ref. 49, respectively. The
local Hubbard-Kanamori interaction on each Ni site
reads
X
X
nilxσ nilzσ′
Hint = U
nila↑ nila↓ + U ′
i,l,σ,σ ′

i,l,a

− JH

X

d†ilxσ d†ilzσ′ dilxσ′ dilzσ

i,l,σ,σ ′

FIG. 1: (a) Sketched ground-state phase diagram as a
function of the correlation strength U/t and electron
occupation number N of the bilayer two-orbital
Hubbard model for La3 Ni2 O7 . The physical system,
indicated by the red star near N = 3 (where N counts
the Ni eg electrons per unit cell) resides in the
bad-metal regime, situated in proximity to an
orbital-selective Mott phase (OSMP). The black line
above the solid circle denotes a Mott insulator (MI) at
the (so-far not-reached) heavily-electron doped case of
N = 4. Adapted from Ref. [49]. (b)
Orbital-differentiated properties of the bad-metal state.
The dz2 orbital exhibits a relatively large incoherent
spectral weight, which contributes to the formation of
effective spin moments, whereas the dx2 −y2 orbital is
characterized by a relatively more coherent part that
makes the system metallic. (c) Illustration of the
effective spin moment coming from the relevant dz2 and
dx2 −y2 orbitals. (d) The dominant spin exchange
interactions in the system, which emerge from an
interplay between itinerant-electron-mediated RKKY
coupling and superexchange coupling (see the main
text).

phase. Here, as we will describe, there are two distinct
processes contributing to the exchange interactions, corresponding to Ruderman-Kittel-Kasuya-Yosida (RKKY)
type magnetic exchange and superexchange interactions.
We show that an antiferromagnetic ground state with
an ordering wavevector close to Q = (π/2, π/2) naturally develops. We demonstrate that this magnetically
ordered phase supports multi-branch magnetic excitations, which are consistent with the recent experimental
observations. Our results underscore the essential role
of orbital-selective electron correlations in determining
the magnetic properties of the bilayer nickelate and provide direct insight into understanding the origin of hightemperature superconductivity in this system.
Models and Conventions. We describe the La3 Ni2 O7

+ JH


X †
dilx↑ d†ilx↓ dilz↓ dilz↑ + H.c. ,

(2)

i,l

where the intraorbital Hubbard repulsion U , the interorbital density repulsion U ′ , and the Hund’s rule coupling JH satisfy the rotationally invariant relation U ′ =
U − 2JH [65].
Building upon the recently introduced global phase diagram [49], shown in Fig. 1(a), the system is characterized by substantial electronic correlations. At the physical filling N = 3, which counts the number of Ni eg
electrons per unit cell, it resides in a bad-metal regime
with strong orbital selectivity, which is under the influence of an orbital-selective Mott phase (OSMP) proximate to the putative half-filled (N = 4) Mott insulating
state. In this bad-metal regime, the single-particle spectral function for each orbital decomposes into coherent
and incoherent components – c.f., Fig. 1(b). The coherent component lies close to the Fermi energy EF , whereas
the charge excitations in the incoherent component are
largely gapped, such that its dominant contribution to
the low-energy physics is an effective local moment – as
illustrated in Fig. 1(c). Owing to the pronounced orbital
selectivity in La3 Ni2 O7 , the spectral weight of the dx2 −y2
orbital resides more in the coherent part, while that of the
dz2 orbital mainly populates the incoherent part. The local moment is therefore primarily associated with the dz2
orbital, despite both orbitals contributing to the overall
spin spectral weight (see Fig. 1(c)).
To construct a tractable low-energy description, we decompose the original hopping terms into two sectors. The
first sector contains the incoherent degrees of freedom
exclusively, which gives rise to superexchange interactions among the local moments. The second sector involves the coherent quasiparticles and their hybridization
with the incoherent part. Integrating out the coherent
fermions transforms this hybridization into an effective
RKKY interaction among the local moments. To make
concrete progress, and taking advantage of the contrast
between the dominant weight in the incoherent and coherent parts of the spectrum from the two orbitals, we

3
adopt a first approximation in which the coherent part is
attributed solely to the dx2 −y2 orbital with quasiparticle
weight Zx , and the incoherent part to the dz2 orbital with
weight 1−Zz . Values of quasiparticle spectral weights are
adapted from Ref. [49] via a slave-spin approach [66, 67].
In other words, we construct the exchange interactions
by considering the limit Zx ≫ Zz , though we expect
the results to qualitatively apply over a wider parameter regime. Two distinct processes contribute to the
exchange coupling. One is the superexchange coupling
between the dz2 -derived local moments on neighboring
s
2 2
δ-sites, which reads Jil,jl
′ ∼ 4(1 − Zz ) til,jl′ /U [68]; this
contribution, familiar in d-electron systems, is an adiabatic continuation of what happens in the single-orbital
or degenerate-multi-orbital systems.
The other is an RKKY coupling, which takes the form
2
Jllr ′ (q) = −jxz
(q)χll′ , (q), which can be considered as
the adiabatic continuation of what happens in the extremely orbital-selective case of Anderson lattice models [69]. Here, jxz (q) denotes a smooth q-dependent
inter-orbital exchange coupling between the dz2 orbital
local moments and the coherent dx2 −y2 orbital carriers,
and χll′ (q) is the layer resolved magnetic susceptibility
at the wave vector q in the dx2 −y2 orbital channel. We
then arrive at the following effective spin Hamiltonian to
describe the magnetism of the La3 Ni2 O7 system:
Hspin =

X

s
r
Jil,jl
′ + Jil,jl′ Sil · Sjl′



(3)

ij,ll′

Here Sil denotes the effective local spin degree of freedom
coming from the incoherent part of the electron spectrum. Further details are provided in the Supplemental
Material [70].
The RKKY interaction. Taking into account the mirror symmetry between the two layers A and B, we define
the susceptibilities in even and odd channels as superpositions of the layer-resolved susceptibilities:
χeven = χAA + χBB + χAB + χBA ,
χodd = χAA + χBB − χAB − χBA .

(4)

Figure 2(a) presents the dx2 −y2 -projected χeven (q) and
χodd (q) in the non-interacting limit (U = 0) for wave
vectors q along the (0, 0)–(π, π) direction, at the nominal
electron filling N = 3. Notably, χodd (q) exhibits a prominent peak not too far away from (0.5π, 0.5π). The peak
arises from nesting between the electron-like α and holelike β Fermi-surface sheets. Although the precise value of
this peak wavevector is somewhat sensitive to the details
in the tight-binding parameterization of the DFT-derived
bands, it is generically close to exactly (0.5π, 0.5π); in
our calculation, it is at q1 ≈ (0.6π, 0.6π). χeven (q) also
displays several peaks at nearby wave vectors. As the interaction U increases, the coherent quasiparticle spectral
weight of the dx2 −y2 orbital is progressively reduced.

FIG. 2: (a) Static spin susceptibility for x2 − y 2 orbitals
at N = 3 and U = 0. (b) Ratio of the intralayer RKKY
interactions J3r /J1r as a function of U .

We now Fourier transform the momentum-space
RKKY interaction into real space. Our analysis reveals
that the dominant coupling is the third-nearest-neighbor
term, J3r . As shown in Fig. 2(b), the ratio J3r /J1r remains
greater than unity over a broad range of U and increases
significantly with growing U , reaching its largest values
near U ∼ 4 eV. At the same time, the in-plane superexchange interaction will be short-ranged. Thus, we expect
the leading exchange interactions to come from the shortrange part.
Magnetic order and excitations. As discussed above,
for intermediate electronic correlations (U ∼ 4 eV), the
3rd-nearest-neighbor RKKY coupling J3r becomes dominant, leading to a growing degree of magnetic frustration.
To explicitly determine these consequences, we analyze
the magnetic properties of the spin model in Eq. 3. The
model is then simplified to a J ⊥ -J1 -J3 model on the bilayer square lattice, where J ⊥ is dominated by the interlayer superexchange, while J1 and J3 are predominantly
sourced from the RKKY couplings.
For each set of exchange parameters, we first identify the candidate ordering wave vector using the Luttinger–Tisza method [71], which seeks the momentumspace minimum of J(q). This ordering vector is subsequently refined via a variational optimization [72], which

4

FIG. 3: The U dependence of the component q of the
ordering wave vector Q = (q, q) of the magnetic ground
state of an effective local spin model involving
superexchange and RKKY interactions obtained via
variational optimization. The wave vector is close to
Q = (π/2, π/2).

minimizes the classical magnetic energy with respect to
both the propagation vector and the spin orientations
within the reference unit cell. Within the parameter
range considered, the ground state is an antiferromagnet
with spins in the top and bottom layers aligned antiparallelly. In each layer, a magnetic order is stabilized at the
wave vector (q, q). At U = 0, q ≈ 0.56π, close to the peak
position q1 of χodd . As U increases, the enhanced ratio
J3 /J1 drives a gradual shift of the magnetic ordering vector Q, as illustrated in Fig. 3. This behavior is consistent
with the magnetic order observed experimentally.
Using the optimized classical magnetic configuration
as a reference, we compute the corresponding magnetic
excitations. Fig. 4 presents the calculated spin-wave
spectrum in the vicinity of the ordering wave vector
(π/2, π/2), along the (π/4, π/4)–(3π/4, 3π/4) direction
of the two-Ni Brillouin zone at U = 4 eV. With the approach detailed in the Supplemental Material [70], the exchange parameters are as follows: the interlayer superexchange J ⊥ S = 75 meV, the intralayer RKKY interactions J1 S = 1.9 meV, J3 S = 4.6 meV, and the interlayer
RKKY interaction J1′ S = 1.38 meV. The corresponding
spectrum comprises a low-energy acoustic branch and a
higher-energy optical branch; the acoustic branch softens at the ordering wave vector Q ≈ (π/2, π/2). Owing
to the incommensurate nature of the order, each branch
splits into three modes: the original mode ϵ(q) and two
folded replicas ϵ(q ± Q). The overall bandwidth of the
calculated spectrum is approximately 80 meV, in good
agreement with the energy scale observed in recent RIXS
experiments [73].
Discussions and conclusions. We have shown how
a magnetic order with the ordering wavevector near
(π/2, π/2) develops in a natural and robust way from the

FIG. 4: Intensity-weighted spin-wave spectrum along
(π/4, π/2)–(3π/4, π/2) of the 2-Ni Brillouin zone in the
antiferromagnetic ground state with ordering wave
vector Q = (0.508π, 0.508π) at U = 4.0 eV. The
corresponding exchange parameters are J ⊥ S = 75 meV,
J1 S = 1.9 meV, J3 S = 4.6 meV, J1′ S = 1.38 meV (see
the main text).

strong orbital-selective correlations observed in the normal state of the bilayer nickelates. In addition to providing the understanding of the scattering experiments mentioned earlier, the proposed mechanism is also consistent
with a recent systematic experiment [74]. More broadly,
the interplay between the superexchange and RKKY interactions within an orbital-selective framework serves as
a conceptually new way to understand the magnetic correlations of multiorbital d-electron systems in such a bad
metal regime.
We briefly discuss several topics that deserve further
investigations. We have focused on the understanding
of the magnetic order in bilayer nickelates; while symmetry dictates an associated charge order, we leave a
systematic study of the latter as a subject of future studies. Experimentally, materials quality has so far limited the understanding of charge order in the bilayer
nickelate, in contrast to what happens in the trilayer
nickelate [75–78]. Another topic of considerable interest
is the interplay between quantum spin singlet correlations among the adjacent interlayer dz2 orbitals within
each bilayer. Several factors need to be taken into account. The Hund’s coupling, which is large compared
to the interlayer dz2 exchange coupling, reduces the tendency towards the interlayer dz2 dimer singlet [49]. The
inter-orbital exchange coupling (jxz (q)) considered in the
present work goes along the same direction. Qualitatively, these combined mechanisms ultimately enable a
magnetically ordered ground state with a substantial reduction of the ordered moment, as recently observed by
neutron scattering measurements [59]. These qualitative
considerations notwithstanding, it will be instructive to
map out the quantitative phase diagram that delineates

5
the interlayer-spin-singlet and antiferromagnetically ordered phases; such a detailed study is left for the future.
∗

We now turn to the implications of our findings for
the superconducting pairing mechanism. The calculated
spin-wave spectrum reveals intense low-energy magnetic
fluctuations, particularly the softening of the acoustic
mode near the incommensurate ordering wave vector
Q ≈ (π/2, π/2). In the presence of the nonzero coherent electron spectral weights (with a smaller quasiparticle weight for dz2 electrons than dx2 −y2 electrons), the
relatively short-range exchange interactions can drive superconducting pairing [50]. Moreover, because the system resides in close proximity to the itinerant-localized
crossover, tuning a non-thermal parameter –such as pressure or electron doping – modulates the interplay of
magnetic correlations and quantum fluctuations and can
serves a dual role. It weakens the long-range magnetic
order and allows the same electrons to instead develop
superconducting pairing.
In conclusion, we have developed a theoretical framework based on orbital-selective electronic correlations to
understand the magnetic properties of the bilayer nickelate superconductor La3 Ni2 O7 . Motivated by the proximity to an orbital-selective Mott phase, we construct a
low-energy description in which the incoherent (mostly
dz2 ) degrees of freedom give rise to local moments, while
the coherent (mostly dx2 −y2 ) electrons mediate effective RKKY interactions. The resulting spin Hamiltonian, comprising both RKKY and superexchange couplings, naturally stabilizes an antiferromagnetic order
with a wave vector near (π/2, π/2), in agreement with
the recent scattering observations in the bilayer nickelates. The calculated spin-wave spectrum exhibits an
acoustic branch softening at the ordering wave vector and
an overall bandwidth of approximately 80 meV, which
are consistent with RIXS and inelastic neutron scattering
measurements. Our results strongly suggest that orbitalselective correlations are an essential ingredient for the
magnetism of the bilayer nickelates. Furthermore, the
findings highlight the low-energy magnetic correlations
as promising routes towards the superconductivity in this
system, thereby expanding the general understanding of
unconventional and high temperature superconductivity
in strongly correlated systems.
We thank H. Chen, X. Lu, K. M. Shen, X. Wu, Y. Wu,
and J. Zhan for useful discussions. Work at Rice was primarily supported by the U.S. Department of Energy, Office of Science, Basic Energy Sciences, under Award No.
DE-SC0018197. Work at Renmin University was supported in part by the National Natural Science Foundation of China (Grants No. 12334008). Q.S. acknowledge
the hospitality of the Aspen Center for Physics, which is
supported by NSF Grant No. PHY-2210452.

These authors contributed equally to this study.
rong.yu@ruc.edu.cn
‡
qmsi@rice.edu.cn
[1] H. Sun, M. Huo, X. Hu, J. Li, Z. Liu, Y. Han, L. Tang,
Z. Mao, P. Yang, B. Wang, et al., Nature 621, 493 (2023).
[2] E. K. Ko, Y. Yu, Y. Liu, L. Bhatt, J. Li, V. Thampy,
C.-T. Kuo, B. Y. Wang, Y. Lee, K. Lee, J.-S. Lee, B. H.
Goodge, D. A. Muller, and H. Y. Hwang, Nature 638,
935 (2025).
[3] G. Zhou, W. Lv, H. Wang, Z. Nie, Y. Chen, Y. Li,
H. Huang, W.-Q. Chen, Y.-J. Sun, Q.-K. Xue, and
Z. Chen, Nature 640, 641 (2025).
[4] Y. Liu, E. K. Ko, Y. Tarn, L. Bhatt, B. H. Goodge,
D. A. Muller, S. Raghu, Y. Yu, and H. Y. Hwang, Nature
Materials 24, 1221 (2025).
[5] Y. Zhang, D. Su, Y. Huang, Z. Shan, H. Sun, M. Huo,
K. Ye, J. Zhang, Z. Yang, Y. Xu, Y. Su, R. Li, M. Smidman, M. Wang, L. Jiao, and H. Yuan, Nat. Phys 20,
1269–1273 (2024).
[6] N. Wang, G. Wang, X. Shen, J. Hou, J. Luo, X. Ma,
H. Yang, L. Shi, J. Dou, J. Feng, J. Yang, Y. Shi, Z. Ren,
H. Ma, P. Yang, Z. Liu, Y. Liu, H. Zhang, X. Dong,
Y. Wang, K. Jiang, J. Hu, S. Nagasaki, K. Kitagawa,
S. Calder, J. Yan, J. Sun, B. Wang, R. Zhou, Y. Uwatoko,
and J. Cheng, Nature 634, 579 (2024).
[7] B. Hao, M. Wang, W. Sun, Y. Yang, Z. Mao, S. Yan,
H. Sun, H. Zhang, L. Han, Z. Gu, et al., Nature Materials
24, 1756 (2025).
[8] G. Zhou, W. Lv, H. Wang, Z. Nie, Y. Chen, Y. Li,
H. Huang, W.-Q. Chen, Y.-J. Sun, Q.-K. Xue, and
Z. Chen, Nature 640, 641–646 (2025).
[9] Y. Liu, E. K. Ko, Y. Tarn, L. Bhatt, J. Li, V. Thampy,
B. H. Goodge, D. A. Muller, S. Raghu, Y. Yu, and H. Y.
Hwang, Nature Materials 24, 1221–1227 (2025).
[10] G. Zhou, H. Wang, H. Huang, Y. Chen, F. Peng, W. Lv,
Z. Nie, W. Wang, J.-F. Jia, Q.-K. Xue, and Z. Chen, National Science Review 13, 10.1093/nsr/nwag151 (2026).
[11] S. Fan, M. Ou, M. Scholten, Q. Li, Z. Shang, Y. Wang,
J. Xu, H. Yang, I. M. Eremin, and H.-H. Wen, Science
Advances 12, 10.1126/sciadv.aeg2429 (2026).
[12] I. Plokhikh, T. J. Hicken, L. Keller, V. Pomjakushin,
S. H. Moody, P. Foury-Leylekian, J. J. Krieger,
H. Luetkens, Z. Guguchia, R. Khasanov, and D. J.
Gawryluk, Unraveling spin density wave order in layered nickelates La3 Ni2 O7 and La2 PrNi2 O7 via neutron
diffraction (2025).
[13] Z. Liao, L. Chen, G. Duan, Y. Wang, C. Liu, R. Yu, and
Q. Si, Phys. Rev. B 108, 214522 (2023).
[14] X.-Z. Qu, D.-W. Qu, J. Chen, C. Wu, F. Yang, W. Li,
and G. Su, Phys. Rev. Lett 132, 036502 (2024).
[15] Griffin Heier, Kyungwha Park, Sergey Y. Savrasov, Physical Review B 109, 104508 (2024).
[16] J. Zhan, Y. Gu, X. Wu, and J. Hu, Phys. Rev. Lett. 134,
136002 (2025).
[17] Y.-H. Tian, Y. Chen, J.-M. Wang, R.-Q. He, and Z.-Y.
Lu, Phys. Rev. B 109, 165154 (2024).
[18] W.-X. Chang, S. Guo, Y.-Z. You, and Z.-X. Li, arXiv
preprint arXiv:2311.09970 (2023).
[19] Q. Qin and Y.-f. Yang, Phys. Rev. B 108, L140504
(2023).
[20] Z. Luo, B. Lv, M. Wang, W. Wú, and D.-X. Yao, npj
†

6
Quantum Mater. 9, 61 (2024).
[21] K. Jiang, Z. Wang, and F.-C. Zhang, Chin. Phys. Lett.
41, 017402 (2024).
[22] J. Huang, Z. Wang, and T. Zhou, Phys. Rev. B 108,
174501 (2023).
[23] Y.-f. Yang, G.-M. Zhang, and F.-C. Zhang, Phys. Rev. B
108, L201108 (2023).
[24] C. Lu, Z. Pan, F. Yang, and C. Wu, Phys. Rev. Lett 132,
146002 (2024).
[25] J.-R. Xue and F. Wang, Chin. Phys. Lett. 41, 057403
(2024).
[26] J. Chen, F. Yang, and W. Li, Phys. Rev. B 110, L041111
(2024).
[27] T. Kaneko, H. Sakakibara, M. Ochi, and K. Kuroki, Phys.
Rev. B 109, 045154 (2024).
[28] M. Kakoi, T. Kaneko, H. Sakakibara, M. Ochi, and
K. Kuroki, Phys. Rev. B 109, L201124 (2024).
[29] H. Sakakibara, N. Kitamine, M. Ochi, and K. Kuroki,
Phys. Rev. Lett 132, 106002 (2024).
[30] Q.-G. Yang, D. Wang, and Q.-H. Wang, Phys. Rev. B
108, L140505 (2023).
[31] R. Jiang, J. Hou, Z. Fan, Z.-J. Lang, and W. Ku, Phys.
Rev. Lett 132, 126503 (2024).
[32] H. Liu, C. Xia, S. Zhou, and H. Chen, Nature Communications 16, 1054 (2025).
[33] X.-Z. Qu, D.-W. Qu, X.-W. Yi, W. Li, and G. Su, Phys.
Rev. B 112, L161101 (2025).
[34] H. Yang, H. Oh, and Y.-H. Zhang, Phys. Rev. B 110,
104517 (2024).
[35] J.-X. Zhang, H.-K. Zhang, Y.-Z. You, and Z.-Y. Weng,
Phys. Rev. Lett 133, 126501 (2024).
[36] D.-C. Lu, M. Li, Z.-Y. Zeng, W. Hou, J. Wang, F. Yang,
and Y.-Z. You, arXiv preprint arXiv:2308.11195 (2023).
[37] Z. Fan, J.-F. Zhang, B. Zhan, D. Lv, X.-Y. Jiang, B. Normand, and T. Xiang, Phys. Rev. B 110, 024514 (2024).
[38] Y.-Y. Zheng and W. Wú, Phys. Rev. B 111, 035108
(2025).
[39] H. Schlömer, U. Schollwöck, F. Grusdt, and A. Bohrdt,
Commun. Phys. 7, 366 (2024).
[40] S. Bötzel, F. Lechermann, J. Gondolf, and I. M. Eremin,
Phys. Rev. B 109, L180502 (2024).
[41] S. Bötzel, F. Lechermann, T. Shibauchi, and I. M.
Eremin, arXiv preprint arXiv:2411.01935 (2024).
[42] H. Oh and Y.-H. Zhang, Phys. Rev. B 108, 174511
(2023).
[43] Y. Zhang, L.-F. Lin, A. Moreo, and E. Dagotto, Phys.
Rev. B 108, L180510 (2023).
[44] Y. Zhang, L.-F. Lin, A. Moreo, T. A. Maier, and
E. Dagotto, Nat. Commun. 15, 2470 (2024).
[45] J. Mei, T. Xie, and K. Jiang, Itinerant nature of
spin-density-wave order in ruddlesden-popper nickelates
(2026).
[46] G. Duan, Y. Wang, Z. Liao, C. Liu, and R. Yu, Communications in Theoretical Physics 78, 065702 (2026).
[47] Z. Liu, M. Huo, J. Li, Q. Li, Y. Liu, Y. Dai, X. Zhou,
J. Hao, Y. Lu, M. Wang, et al., Nat. Commun 15, 7570
(2024).
[48] J. Yang, H. Sun, X. Hu, Y. Xie, T. Miao, H. Luo,
H. Chen, B. Liang, W. Zhu, G. Qu, et al., Nat. Commun 15, 4373 (2024).
[49] Z. Liao, Y. Wang, L. Chen, G. Duan, R. Yu, and Q. Si,
Phys. Rev. B 114, 045112 (2026).
[50] G. Duan, Z. Liao, L. Chen, Y. Wang, R. Yu, and Q. Si,
Orbital-selective correlation effects and superconducting

pairing symmetry in a multiorbital t-j model for bilayer
nickelates (2025), arXiv:2502.09195.
[51] Z. Luo, X. Hu, M. Wang, W. Wú, and D.-X. Yao, Phys.
Rev. Lett. 131, 126001 (2023).
[52] K. Chen, X. Liu, J. Jiao, M. Zou, C. Jiang, X. Li, Y. Luo,
Q. Wu, N. Zhang, Y. Guo, and L. Shu, Phys. Rev. Lett.
132, 256503 (2024).
[53] D. Zhao, Y. Zhou, M. Huo, Y. Wang, L. Nie, Y. Yang,
J. Ying, M. Wang, T. Wu, and X. Chen, Science Bulletin
70, 1239 (2025), arXiv:2402.03952 [cond-mat.supr-con].
[54] J. Luo, J. Feng, G. Wang, N. N. Wang, J. Dou,
A. F. Fang, J. Yang, J. G. Cheng, G.-q. Zheng, and
R. Zhou, Chinese Physics Letters 42, 067402 (2025),
arXiv:2501.11248 [cond-mat.supr-con].
[55] X. Chen, J. Choi, Z. Jiang, J. Mei, K. Jiang, J. Li,
S. Agrestini, M. Garcia-Fernandez, X. Huang, H. Sun,
D. Shen, M. Wang, J. Hu, Y. Lu, K.-J. Zhou, and
D. Feng, Nature Communications 15, 9597 (2024),
arXiv:2401.12657 [cond-mat.supr-con].
[56] N. K. Gupta, R. Gong, Y. Wu, M. Kang, C. T. Parzyck,
B. Z. Gregory, N. Costa, R. Sutarto, S. Sarker, A. Singer,
D. G. Schlom, K. M. Shen, and D. G. Hawthorn, Nature
Communications 16, 6560 (2025).
[57] I. Plokhikh, T. J. Hicken, L. Keller, V. Pomjakushin,
S. H. Moody, P. Foury-Leylekian, J. J. Krieger,
H. Luetkens, Z. Guguchia, R. Khasanov, and D. J.
Gawryluk, (2025), arXiv:2503.05287 [cond-mat.suprcon].
[58] H. Zhong, B. Hao, A. Chen, X. Huang, C. Li, W. Zhang,
C. Liu, K. Kummer, N. Brookes, Y. Nie, T. Schmitt, and
X. Lu, Chinese Physics Letters 43, 060717 (2026).
[59] L. Chen, E. Zhang, Y. Hao, Y. Zhu, B. Cui, D. L.
Abernathy, T. J. Williams, Y. Ikeda, H. Zhang,
F. Liu, W. Wang, Q. Wang, and J. Zhao, (2026),
arXiv:2605.03448 [cond-mat.str-el].
[60] Y.-B. Liu, H. Sun, M. Zhang, Q. Liu, W.-Q. Chen, and
F. Yang, Phys. Rev. B 112, 014510 (2025).
[61] J. Zhan, X. Wu, and J. Hu, Magnetic configurations and
excitations in high-tc multilayer nickelates (2026).
[62] L. B. Braz, S. Bötzel, F. Lechermann, I. Plokhikh,
R. Khasanov, L. G. G. V. D. da Silva, and I. M. Eremin,
Density waves in low-pressure bilayer nickelates (2026).
[63] X.-S. Ni, Y. Ji, L. He, T. Xie, D.-X. Yao, M. Wang, and
K. Cao, npj Quantum Materials 10, 10.1038/s41535-02500740-z (2025).
[64] H.-X. Wang, H. Oh, T. Helbig, B. Y. Wang, J. Li, Y. Yu,
H. Y. Hwang, H.-C. Jiang, Y.-M. Wu, and S. Raghu, Origin of spin stripes in bilayer nickelate La3 Ni2 O7 (2026),
arXiv:2509.25344 [cond-mat.supr-con].
[65] C. Castellani, C. R. Natoli, and J. Ranninger, Physical
Review B 18, 4945–4966 (1978).
[66] R. Yu and S. Qimiao, Phys. Rev. B 86, 085104 (2012).
[67] R. Yu and Q. Si, Phys. Rev. B 96, 125110 (2017).
[68] W. Ding, R. Yu, Q. Si, and E. Abrahams, Phys. Rev. B
100, 235113 (2019).
[69] Y. Wang, G. Duan, R. Yu, and Q. Si, unpublished (2026).
[70] See Supplemental Information [http://link...] for details
about the orbital-selective band renormalization of the
bilayer two-orbital Hubbard model and formulism and
results of the susceptibility and the RKKY interaction.
[71] J. M. Luttinger and L. Tisza, Physical Review 120, 1580
(1960).
[72] D. Dahlbom, H. Zhang, C. Miles, S. Quinn, A. Niraula,
B. Thipe, M. Wilson, S. Matin, H. Mankad, S. Hahn,

7
et al., arXiv preprint arXiv:2501.13095 (2025).
[73] X. Chen, J. Choi, Z. Jiang, J. Mei, K. Jiang, J. Li,
S. Agrestini, M. Garcia-Fernandez, H. Sun, X. Huang,
et al., Nat. Commun 15, 9597 (2024).
[74] Y. Wu et al. (2026), unpublished.
[75] A. Suthar, V. Sundaramurthy, M. Bejas, C. Le,
P. Puphal, P. Sosa-Lizama, A. Schulz, J. Nuss, M. Isobe,
P. A. van Aken, Y. E. Suyolcu, M. Minola, A. P. Schnyder, X. Wu, B. Keimer, G. Khaliullin, A. Greco, and
M. Hepting, Multiorbital character of the density wave
instability in la4 ni3 o10 (2025), arXiv:2508.06440 [condmat.str-el].
[76] D.-H. Gim, C. H. Park, and K. H. Kim, Phys. Rev. Lett.
135, 136505 (2025).
[77] M. R. Norman, Phys. Rev. B 112, 075149 (2025).
[78] J. Zhang, D. Phelan, A. S. Botana, Y.-S. Chen, H. Zheng,
M. Krogstad, S. G. Wang, Y. Qiu, J. A. RodriguezRivera, R. Osborn, S. Rosenkranz, M. R. Norman, and
J. F. Mitchell, Nat. Commun. 11, 6003 (2020).

1

Supplemental Material for “Magnetic Order in bilayer Ruddlesden-Popper Nickelates”

ORBITAL-SELECTIVE RENORMALIZATION OF THE COHERENT ELECTRONIC STRUCTURE

The tight-binding Hamiltonian of the bilayer two-orbital Hubbard model introduced in Eqns. (1) and (2) of the
main text reads
X
X
†
HTB =
tαβ
(ϵα − µ)nilασ ,
(S1)
il,jl′ diασ djβσ +
ijll′ ,αβ,σ

il,α,σ

where l, l′ are layer indices, i, j label sites within each layer, and α, β denote the orbital indices. The hopping
amplitudes tαβ
il,jl′ refer to the hopping integral, ϵα denotes the crystal-field levels of the two eg orbitals, and µ is the
chemical potential.
For each interaction strength U , we solve the two-orbital Hubbard model within the slave-spin mean-field approach [66, 67]. This calculation yields the orbital-dependent quasiparticle spectral weights Zα (U ) and static energy
shifts λα (U ). We then use these quantities to construct a renormalized tight-binding Hamiltonian for the coherent
part of electrons, in which the hopping amplitudes and onsite energies are modified according to the slave-spin results.
The resulting quasiparticle Hamiltonian is
X
X q
†
′
Zα (U )Zβ (U ) tαβ
[ϵα + λα (U ) − µ(U )] nilασ .
(S2)
Heff =
il,jl′ dilασ djl βσ +
ijll′ ,αβ,σ

il,α,σ

Thus, the slave-spin quasiparticle weights directly renormalize the bare hopping amplitudes to
q
Zα (U )Zβ (U ) tαβ
teαβ
(U
)
=
′
il,jl′ .
il,jl

(S3)

The orbital-dependent shifts λα (U ) similarly renormalize the onsite energies. In this way, the correlation effects to
the coherent electrons are incorporated into an effective quasiparticle tight-binding Hamiltonian. This procedure
incorporates the orbital-dependent quasiparticle renormalization induced by local electronic correlations into the
effective single-particle Hamiltonian. It therefore allows us to describe the strongly correlated and orbital-selective
regime beyond a weak-coupling treatment based on the bare tight-binding bands.
The resulting orbital-selective regime admits a simple low-energy interpretation. The more dispersive dx2 −y2 quasiparticles form the itinerant sector and determine the particle-hole susceptibility. The more strongly renormalized
dz2 sector mainly contributes local moment degree of freedom in low energy, whose dominant short-range interaction
is the antiferromagnetic interlayer superexchange J ⊥ . A smooth q-dpendent interorbital exchange coupling jxz (q),
taking into account effects of both onsite Hund’s rule interaction and inter-site hybridizations, connects the coherent
and incoherent sectors, allowing the itinerant dx2 −y2 quasiparticles to mediate RKKY interactions between the dz2
moments.
To evaluate the itinerant-electron response, we use the renormalized quasiparticle Hamiltonian obtained from the
slave-spin calculation in the preceding section. On an Nk × Nk momentum mesh, we diagonalize its single-particle
matrix as
X
(Heff )ab (k; U )ubn (k; U ) = ξn (k; U )uan (k; U ),
(S4)
b

Here orbital and layer indices are combined into the indices a, b (e.g., a = lα).
The static susceptibility of the renormalized quasiparticles is then calculated via
χab;cd (q; U ) = −

1 XX
ucm (k + q; U )u∗am (k + q; U )
Nk2
m,n
k

× ubn (k; U )u∗dn (k; U )Lmn (k, q; U ),

(S5)

2
where
Lmn (k, q; U ) =

f [ξm (k + q; U )] − f [ξn (k; U )]
.
ξm (k + q; U ) − ξn (k; U )

(S6)

For vanishing denominator in the calculation, the ratio is evaluated using its limiting value given by the derivative
of the Fermi function. The interaction strength U affects the susceptibility through the slave-spin renormalized
quasiparticle energies and eigenvectors.
With strong orbital selectivity, the local moments originate predominantly from the dz2 sector, whereas longrange RKKY interactions are mediated by the more itinerant dx2 −y2 quasiparticles. We therefore project the two
susceptibility vertices onto the dx2 −y2 orbital, and the layer-resolved susceptibility after the projection is defined as
χll′ (q; U ) ≡ χlx,lx;l′ x,l′ x (q; U ),

(S7)

where x denotes the dx2 −y2 orbital and l, l′ = A, B.
The even and odd bilayer channels used in the main text are then given by
χeven (q; U ) = χAA (q; U ) + χBB (q; U ) + χAB (q; U ) + χBA (q; U ),
χodd (q; U ) = χAA (q; U ) + χBB (q; U ) − χAB (q; U ) − χBA (q; U ).

(S8)

RKKY EXCHANGE INTERACTIONS

In the orbital-selective regime, charge fluctuations in the dz2 sector are strongly suppressed, and their low-energy
degrees of freedom are represented by localized moments. According to the discussion in the main text, the exchange
interactions among these local moments are from two distinct processes. One is the superexchange interaction between
the local moments. Based on analysis in Ref. 68, the superexchange coupling for the incoherent local moments reads
s
2 2
Jil,jl
′ ∼ 4(1 − Zz ) til,jl′ /U , which is renormalized by the spectral weights of the incoherent electrons.
The other process contributing to exchange interaction is the RKKY interaction among the local moments mediated
by the coherent electrons. The coupling between the incoherent local moments in the dz2 orbital and the coherent
quasiparticles in the dx2 −y2 orbital includes both an onsite Hund’s rule coupling and an inter-site hybridization. These
give rise to the following interorbital exchange interaction:
X
Hxz =
jllxz′ (q)Sil · sjl′ eiq·(Ri −Rj ) ,
(S9)
ij,ll′ ,q

where Silz denotes the localized moment associated with the dz2 orbital, sil is the spin density of the itinerant dx2 −y2
quasiparticles, and jllxz′ (q) is a smooth q-dependent interorbital exchange coupling between dx2 −y2 and dz2 orbitals.
To the second order in jllxz′ (q), integrating out the itinerant quasiparticles generates the effective RKKY interaction
among local moments
X
Hr =
Jllr ′ (Ri − Rj )Sil · Sjl′ ,
(S10)
ij,ll′

with
Jllr ′ (R) = −

X

2

eiq·R (jllxz′ (q)) Re χll′ (q),

(S11)

q

where the momentum sum is performed over an Nq × Nq mesh.
With consideration of both superexchange and RKKY interactions, we obtain the effective local spin model for the
magnetism of La3 Ni2 O7 as
X
X
s
r
Hspin =
Jil,jl′ Sil · Sjl′ =
(Jil,jl
(S12)
′ + Jil,jl′ ) Sil · Sjl′ ,
ijll′

ijll′

which arrives at Eq. (3) of the main text. For dz2 orbital, the interlayer nearest neighbor hopping t⊥ dominant.
We then expect that the corresponding interlayer exchange coupling J ⊥ = JiA,iB is dominant by the superexchange
s
s
process, e.g. J ⊥ ≈ JiA,iB
. With t⊥ ∼ 0.6 eV, and the Zz value from slave-spin calculation [49], we obtain JiA,iB
S ≈ 75

3

FIG. S1: Calculated nearest-neighbor (J1 ) and third-neighbor (J3 ) RKKY exchange couplings as functions of the
Hubbard interaction U . Both exchange couplings and U are in units of eV.

meV. On the other hand, intralayer and further neighboring interlayer couplings are estimated to be at or less than the
r
order of 1 meV. Therefore, these exchange couplings are predominantly from RKKY interaction, e.g. Jil,jl′ ≈ Jil,jl
′
for i ̸= j. Defining the intra- and inter-layer susceptibilities as
χeven (q) + χodd (q)
χAA (q) + χBB (q)
=
,
2
4
χAB (q) + χBA (q)
χeven (q) − χodd (q)
χinter (q) =
=
,
2
4

χintra (q) =

(S13)

The exchange couplings of several neighboring spin pairs are as follows:
r
J1 = Jintra
(Rij = (1, 0)) ,

r
J2 = Jintra
(Rij = (1, 1)) ,

r
J3 = Jintra
(Rij = (2, 0)) ,

r
J1′ = Jinter
(Rij = (1, 0)) .

(S14)

Here Rij are defined on the square lattice in units of the lattice spacing. Values of these exchange couplings are
obtained via Eq. (S11) by taking |jllxz′ (q)| ≈ j xz = 1 eV (neglecting its slow q dependence, given that it is dominant
by the Hund’s rule coupling). Fig. S1 shows evolution of the in-plane nearest and the 3rd-nearest neighbor exchange
interactions with U . We find J3 > J1 with increasing U up to U <
∼ 6 eV, and the J3 /J1 ratio develops a sharp peak
at about 4 eV.


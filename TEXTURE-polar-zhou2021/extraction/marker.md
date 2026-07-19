<!-- extracted via pdftotext | arxiv:2104.12990 | 2026-07-19T04:40:36Z -->
Local Manipulation and Topological Phase Transitions of Polar Skyrmions
Linming Zhou1, Yongjun Wu*, 1, 2, Sujit Das3, Yunlong Tang3, Cheng Li1, Yuhui Huang*, 1, He
Tian4, Long-Qing Chen5, Ramamoorthy Ramesh*, 3, Zijian Hong*, 1, 2
1

Lab of Dielectric Materials, School of Materials Science and Engineering, Zhejiang University,

Hangzhou, Zhejiang 310027, China
2

Cyrus Tang Center for Sensor Materials and Applications, State Key Laboratory of Silicon

Materials, Zhejiang University, Hangzhou, Zhejiang 310027, China
3

Department of Materials Science and Engineering, University of California, Berkeley, CA

94720, USA
4

Center of Electron Microscopy, State Key Laboratory of Silicon Materials, School of

Materials Science and Engineering, Zhejiang University, Hangzhou, Zhejiang 310027, China
5

Department of Materials Science of Engineering, The Pennsylvania State University,

University Park, PA 16802, USA
Topological phases such as polar skyrmions have been a fertile playground for ferroelectric
oxide superlattices, with exotic physical phenomena such as negative capacitance. Herein, using
phase-field simulations, we demonstrate the local control of the skyrmion phase with electric
potential applied through a top electrode. Under a relatively small electric potential, the
skyrmions underneath the electrode can be erased and recovered reversibly. A topologically
protected transition from the symmetric to asymmetric skyrmion bubbles is observed at the
edge of the electrode. While a topological transition to a labyrinthine domain requires a high
applied potential, it can switch back to the skyrmion state with a relatively small electric
potential. The topological transition from +1 to 0 occurs before the full destruction of the bubble
state. It is shown that the shrinking and bursting of the skyrmions leads to a large reduction in
the dielectric permittivity, the magnitude of which depends on the size of the electrode.

* Corresponding authors: Y.W. (yongjunwu@zju.edu.cn), Y. H. (huangyuhui@zju.edu.cn)
R.R.(rramesh@berkeley.edu), Z.H. (hongzijian100@zju.edu.cn)
1

Introduction
Complex ferroelectric topological patterns have garnered enormous interest recently,
driven by the formation of polar vortices [1-5], flux-closure domains [6, 7], polar spirals [8, 9],
skyrmions [10-12], and merons [13], etc., which have largely rejuvenated the understanding of
ferroelectrics and the associated theoretical frameworks [14]. These polar textures exhibit exotic
physical phenomena such as negative capacitance [15-17], chirality [18-22], ultrafast light-induced
supercrystal formation [23], etc. In particular, the polar skyrmion, a nontrivial whirl-like structure
with a topological charge of ±1, has been discovered in the PbTiO3/SrTiO3 (PTO/STO)
superlattice system. It has triggered considerable attention for potential nano-electronic device
applications, like in the non-centrosymmetric ferromagnetic counterparts [24, 25]. Previous
studies have shown that the polar skyrmion in the PTO/STO system is topologically protected
during electrical switching, akin to those observed in the ferromagnetic systems [16]. The
dynamics of the skyrmion switching process could also induce transitions from a skyrmion to
other topological states of matter in a reversible fashion [11]. Despite all these exciting
discoveries, one intriguing question has yet to be answered: how can we locally
move/manipulate the polar skyrmion? This could stimulate the next level of interest in
technological applications such as ferroelectric racetrack memories or other electronic devices.

Results
In this article, we report the local electric erasure/recovery of polar skyrmions via an
external electric field through a narrow top electrode contact. Details of the phase-field
simulations are given in the Methods. The simulation setup is described in Fig. 1, where the
PbTiO3/SrTiO3 (PTO/STO) superlattice is epitaxially grown on top of a (001)-STO substrate.
A three-dimensional mesh of 320320350 is built, with each grid representing 1 unit cell. A
bottom electrode is introduced between the film and substrate, while a narrow electrode with
2

designed width (d0= 8 nm and 32 nm) along the X-dimension is deposited on top of the film.
The top view shows the equilibrium polar skyrmion structure in the PTO layer (Fig. 1b), which
is consistent with previous reports [10, 16]. Fig. 1(c) shows the magnified view of the in-plane
vector mapping, which indicates the formation of a hedgehog-like skyrmion structure. To
quantify the topological feature of the polar skyrmion, the Pontryagin density q is calculated,
1

𝜕𝑃⃗

𝜕𝑃⃗

i.e., 𝑞 = 4𝜋 ⃗𝑃 . (𝜕𝑥 × 𝜕𝑦 ), where ⃗𝑃 is the polarization vector. The topological charge can be
obtained by the surface integral of the Pontryagin density over xy space, 𝑄 = ∬ 𝑞𝑑𝑥𝑑𝑦 [12, 2728]

. The planar view of the Pontryagin density for the top PTO layer is plotted in Fig. 1(d). It

shows the formation of ring-like structures, which are planar projections of the Neel component
of the dipolar distribution of the Pontryagin density for smooth skyrmion bubbles [11]. While
the line profile shows two peaks on the two edges of the ring (Fig. 1e), for each ring, the total
topological charge is +1. An electric potential is then applied through the top electrode, with
the potential profile given in Fig. 1(f).

Fig. 1 Initial setup, topological feature and the applied potential profile. (a) Schematics of the PTO/STO
superlattice system. (b) Planar view of the in-plane polarization magnitude from phase-field, showing the
formation of skyrmion bubbles. (c) Magnified view of the polar skyrmion bubble overlaid with the in-plane polar
vector. (d) Planar view of the Pontryagin density distribution. (e) Magnified view of the Pontryagin density

3

distribution on a single bubble, with line profile overlaid. (f) The applied voltage profile, the width of the electrode
is d0, while the magnitude of the voltage is 0.

In the first study, a +6 V is applied through an 8 nm wide top electrode. The kinetic
evolution pathway of the skyrmions is shown in Fig. 2(a)-2(c). The skyrmions underneath the
electrode region shrink after 100 timesteps, and then gradually disappear. In the neighboring
regions, the skyrmions are pushed away from the electrode, which become asymmetric where
it is darker near the electrode side and brighter on the other side. Eventually, all the skyrmions
underneath the electrode region are erased. The dynamics of the evolution pathway is presented
in supplementary video S1. The polar structure of the asymmetric skyrmion in the vicinity of
the electrode is highlighted in Fig. 2(d); a large in-plane polarization is observed which points
away from the planar electrode. While close to the electrode side, the in-plane polarization
becomes much smaller in magnitude. To understand this phenomenon, the electric field
distribution of the top PTO layer is plotted (Fig. S2a and S2b), indicating that the electric field
is predominantly pointing downwards underneath the electrode region, which triggers the
switching of skyrmions to form a simple c- domain. In the neighboring regions, a large in-plane
electric field can be observed due to the sharp potential transition from +6 V to 0 V, which
drives the asymmetric skyrmion transition and pushes them away from the electrode. The
topological feature of the asymmetric bubble is given in Fig. 2(e). The distribution of the
Pontryagin density is asymmetric with the left side of the ring having a higher Pontryagin
density, corresponding to a single peak on the left from the line plot. The topological charge for
the asymmetric bubble is also +1, demonstrating that the symmetric to asymmetric bubble
transition is also topologically protected. The Pontryagin density for the asymmetric bubble is
further plotted with different switching timesteps (Fig. 2f). It can be observed that a single peak
formed after 200 timesteps, which shows a right shift with continuous evolution of the
asymmetric skyrmion. Meanwhile, as a comparison, for the skyrmion bubbles underneath the
4

electrode, the Pontryagin density is symmetric on the two sides of the ring, which increases
with the decreasing of the bubble size until it bursts after ~104 timesteps (Fig. S2d).

Fig. 2 Kinetics and topological transition of the skyrmion switching and recovery under a small applied
potential of 6 V and narrow electrode of 8 nm. (a)-(c) The kinetic evolution pathway after 102, 103 and 104
timesteps, respectively. The white dashed lines mark the electrode region. (d) Magnified view of the asymmetric
skyrmion overlaid with the inplane polar vector. (e) Pontryagin density distribution on an asymmetric bubble, with
line profile overlaid. (f) Line plots of the Pontryagin density over different timesteps. (g)-(i) The relaxation kinetics
after the field is removed, after 100, 400 and 104 timesteps, respectively. The arrows indicate the nucleation of new
skyrmions.

Upon removal of the applied electric field, the asymmetric skyrmions first expand and
relax to symmetric skyrmions, then the nucleation and growth of new skyrmions can be
observed to fill in the regions underneath the original electrode (Fig. 2g-2i). After 104 timesteps,
the system reverts to a fully skyrmionic state. Thus, we have demonstrated the ability to locally
erase and reset the skyrmion state, which is electrically controllable and reversible.

5

On the other hand, when the applied bias is large (e.g., +9 V, Fig. 3), the skyrmion
shrinking and dissipation process is also observed underneath the electrode region, similar to
the previous case. However, in the neighboring regions, the skyrmions “melt” and merge to
form long stripe domains along the Y direction. After 104 timesteps, all the skyrmions
underneath the electrode regions are erased, while the neighboring regions are filled with long
stripes (Fig. 3c). These stripe domains have a large unidirectional in-plane polarization pointing
away from the electrode region (Fig. S3a and S3b). This can be rationalized since under +9 V,
the in-plane field is much higher as compared to the +6 V case, which is sufficient to switch all
the skyrmions to a unidirectional in-plane polarization and connect them (Fig. S3c and S3d).
The topological feature after 100 timesteps is plotted in Fig. 3(d). It can be seen that the
Pontryagin density of the skyrmions underneath the electrode behaves similar to the previous
case which increases in magnitude with decreasing the bubble size. Meanwhile, an interesting
topological pattern is observed in the vicinity of the electrode where the rings show alternating
positive and negative Pontryagin density on the two sides (Fig. 3e), which gives rise to a net
topological charge of 0. This demonstrates the switching of the topological pattern even before
the full destruction of the bubble structure. It can also be observed that the shape of the
Pontryagin density is preserved during the consequent switching process, while the peak value
shrinks and completely disappears when the bubbles join to form long stripes (Fig. 3f).
When the applied potential is removed, the stripe domains expand towards the electrode
region, forming labyrinthine domains to reduce the depolarization field in this system. Unlike
the unidirectional stripes formed in the initial switching process, these labyrinthine domains
have alternating in-plane polarization components to minimize the depolarization field. New
stripes nucleate and grow underneath the electrode region, from the vicinity of the old stripes
to the center of the electrode region (Fig. 3g and 3h). The detailed switching and recovery
process is further provided in supplementary videos S2. Previously, topological transitions
6

from vortex to skyrmions by thermal or electrical driving forces have been widely reported [11,
30, 31]

. Here in this study, we have demonstrated an electric field-driven localized topological

transition from skyrmions to labyrinthine domains, with both states being stable at room
temperature and zero field. The net skyrmion number of the whole simulation system (which is
calculated by integrating the Pontryagin density for the entire top PTO surface) is shown for
different switching processes (Fig. 3i). It can be observed that with a small applied voltage bias
and a narrow electrode, the total skyrmion number decreases first as the skyrmion bubbles burst
but recovers after the applied bias is removed. Under a high electric field with a wide electrode,
the total skyrmion number drops significantly which cannot be restored even after the applied
electric field is removed.

Fig. 3 Kinetics and topological transition of the skyrmion switching and recovery under high potential of
+9 V and wide electrode of 32 nm. (a)-(c) The kinetic evolution after 100, 400 and 104 timesteps. The white
dashed region is the electrode. (d) 2-D plot of the Pontryagin density on the top PTO layer after 100 timesteps. (e)
Magnified view of the Pontryagin density distribution on a bubble, with line profile overlaid, showing a distinct

7

topological feature with negative Pontryagin density on the left and positive Pontryagin density on the right. (f)
Evolution of the line plot of the Pontryagin density. (g)-(h) The relaxation kinetics after the field is removed, after
100 and 104 timesteps. The formation of stable long stripes is observed. (i) Comparison of the evolution of the
total skyrmion number during the switching and recovery process under low and high bias.

A cycling test is further performed (Fig. 4) to showcase the controllable reverse transition,
starting from the state after poling by +9 V and relaxed to zero after 104 timesteps (Fig. 4a). An
opposite bias of -6 V is applied later (Fig. 4b), which melts the vortex and labyrinthine domains
to skyrmion bubbles through a Rayleigh-Plateau mechanism (see supplementary video S3 for
details), as has been reported previously [11]. After the field is removed, these residual small
bubbles expand to become normal skyrmions, while the nucleation of skyrmions in other
regions is also observed (Fig. 4c). On the two sides near the electrode, the labyrinthine domains
remain since the in-plane field generated under -6 V is not large enough to erase them. Then, in
the second cycle, +9 V is applied again to erase the skyrmion bubbles (Fig. 4d) with pure cdomain underneath the electrode region, which switch back to the labyrinthine state again after
the field is removed (Fig. 4e). A potential of -6 V is applied to start the second cycle, leading to
the topological transition between labyrinthine domains and skyrmions (Fig. 4f) and the
skyrmion state is stable when the applied field is removed (Fig. 4g). Thus, we have realized the
localized reversible transitions between skyrmions and labyrinthine domains through control of
the magnitude of the applied voltage.
To further understand the properties accompanying the topological transitions, the
dielectric properties underneath the electrode regions of the different states are further plotted
in Fig. 4(h). The initial dielectric constant of the skyrmion bubble is ~650, which agrees with
the previous experimental measurements and theoretical calculations [16]. It can be observed that
with the increase of the applied electric field, the dielectric permittivity decreases. This is
largely due to the shrinking and switching of the skyrmions, which decreases the area with
negative permittivity inside the PTO layers, consistent with previous studies [13, 14]. Notably,
8

under the same applied voltage, generally the wider the electrode, the larger the dielectric
permittivity. This can be understood since under the same, nominal out-of-plane electric field,
the remaining skyrmion density/area is much larger for the case with a wider electrode than a
narrower electrode, as evidenced by Fig. S4(a) and S4(b). This will contribute to extra, negative
capacitance regions that will ultimately increase the overall dielectric property.

When the

electrode is thin (e.g., 8 nm), with a large nominal applied field (i.e., +800 kV/cm), the dielectric
constant underneath the electrode shows an 80% reduction due to the erasure of the polar
skyrmions with large negative capacitance regions, indicating the large tunability of the device.

Fig. 4 Cycling test and reversible transition between labyrinthine state and skyrmion. (a)-(d) The kinetic
evolution of the first cycle, after applying -6 V to erase the labyrinthine domains to form stable skyrmion when
field is removed, while applying +9 V could erase the skyrmions and form labyrinthine state. (e)-(g) The second
cycle from vortex to skyrmion after applying -6 V. (h) local dielectric permittivity as a function of nominal applied
electric field through a narrow top electrode.

Discussion
In conclusion, we report the local control of polar skyrmions through a top electrode in the
PTO/STO superlattice system. Under a small applied potential with a narrow electrode
geometry, the skyrmions underneath the electrode can be locally erased while the skyrmions in
9

the neighboring regions are repelled by the electrode, giving rise to asymmetric shapes with inplane polarization mainly pointing away from the electrode, both the symmetric and
asymmetric skyrmion bubbles exhibit a topological charge of +1, showing that the asymmetric
to symmetric skyrmion transition is topologically protected. The skyrmion state is recovered
when the potential is removed. Meanwhile, with a large applied potential and a wide electrode,
labyrinthine domains form on the two sides of the electrode, and remain stable even when the
applied potential is removed. Interestingly, in this case, the topological transition from +1 to 0
occurs even before the full destruction of the bubble state, with a negative/positive Pontryagin
density on the left/right side of the bubble. As a comparison, the total topological charge of the
system can be recovered under small bias, while under large applied potential and wide
electrode, the total topological charge is largely decreased which can’t be restored when the
field is removed. The labyrinthine states can be switched back to the skyrmion state after
applying a relatively smaller potential. Thus, we realized a reversible transition between
skyrmion and labyrinthine states through controlling the distribution of the applied potential.
The dielectric permittivity is further calculated, which shows a large reduction/tunability under
a high field. This can be attributed to the erasure of the skyrmion regions with negative
permittivity. We envision this work to spur further interests in the skyrmion physics in
ferroelectric systems as well as the potential applications towards nano-electronic device
applications.

10

Methods：
Phase-field simulations.
Phase-field simulations are performed for the [(PbTiO3)16/(SrTiO3)16] superlattices on
SrTiO3 (001) substrate, by solving the time dependent Ginzburg-Landau equations [31-33]:
𝑑𝑃⃗
𝑑𝑡

= −𝐿

δF(𝑃⃗ ,∇𝑃⃗ )
δ𝑃⃗

(1)

Where ⃗𝑃 is the spontaneous polarization vector, t is the evolution timestep. The kinetic
coefficient L is related to the domain wall mobility. The free energy F can be expressed by the
volume integral of the elastic, electric, Landau and gradient energy densities, i.e.,
𝐹(𝑃⃗, ∇𝑃⃗) = ∫(𝑓𝑒𝑙𝑎𝑠 + 𝑓𝑒𝑙𝑒𝑐 + 𝑓𝐿𝑎𝑛𝑑 + 𝑓𝑔𝑟𝑎𝑑 )𝑑𝑉

(2)

The Landau chemical energy density can be written as:
𝑓𝐿𝑎𝑛𝑑 = 𝛼𝑖𝑗 𝑃𝑖 𝑃𝑗 + 𝛽𝑖𝑗𝑘𝑙 𝑃𝑖 𝑃𝑗 𝑃𝑘 𝑃𝑙 + ⋯

(3)

In this study, the Landau polynomial is expanded to the sixth order, with the coefficients
taken from previous literatures [26, 34].
The electric energy density is calculated by:
1

𝑓𝑒𝑙𝑒𝑐 = − 2 𝐸𝑖 𝑃𝑖 + 𝑘𝑖𝑗 𝐸𝑖 𝐸𝑗

(4)

Where 𝑘𝑖𝑗 is the background dielectric constant, which is set as 40 in this study [35-37].
The local electric field E can be obtained by:

𝐸𝑖 = −∇𝑖 𝜑. The closed boundary conditions are

set such that the electric potential 𝜑 is zero and the applied potential on the film/substrate
interface and the top of the thin film, respectively.
The elastic energy density can be obtained:
0
0
𝑓𝑒𝑙𝑎𝑠 = 𝐶𝑖𝑗𝑘𝑙 (𝜀𝑖𝑗 − 𝜀𝑖𝑗
)(𝜀𝑘𝑙 − 𝜀𝑘𝑙
)

11

(5)

0
Where Cijkl is the elastic stiffness tensor, 𝜀𝑖𝑗
is the eigen strain due to the ferroelectric
0
phase transition, 𝜀𝑖𝑗
= 𝑄𝑖𝑗𝑘𝑙 𝑃𝑘 𝑃𝑙 , Q is the electrostriction coefficient tensor. The strain tensor

𝜀𝑖𝑗 can be calculated by solving the elastic equilibrium equation. An iterative perturbation
method is used to consider the elastic anisotropy for the PTO and STO layers [38]. The
pseudocubic lattice constants for PTO and STO are set as 3.957 Å and 3.905 Å, respectively to
determine the lattice mismatch. Thin film elastic boundary condition is used where the out-ofplane stress on the top of the thin film is set as zero while the displacement on the bottom of
the substrate far away from the electrode/thin film interface is zero.
The gradient energy density is further expressed as:
𝑓𝑔𝑟𝑎𝑑 = 𝑔𝑖𝑗𝑘𝑙 ∇𝑗 𝑃𝑖 . ∇𝑙 𝑃𝑘

(6)

Where g is the gradient coefficient tensor.
Detailed numerical calculations and the simulation parameters can be found in the
published literature [8, 11, 26]. The simulation system is discretized into a 3-D mesh of
320320350, with each grid representing 1 unit cell. A periodic boundary condition is applied
on the in-plane dimensions, while a superposition method is used on the out-of-plane direction.
The out-of-plane direction consists of 30 grids of substrate, 272 grids of thin films with periodic
stacking of PTO16/STO16 and 48 layers of air. The normalized timestep is 0.01 in this study.
ΔP

The local dielectric constant is obtained by: 𝜀33 = 𝜀 ΔE3 + 𝜀𝑏 , while the macroscopic
0

dielectric constant can be calculated by 𝜀̅̅̅̅
33 =

<ΔP3 >𝑑
𝜀0 φ

3

+ 𝜀𝑏 , where< ΔP3 > is the average of

the change in out-of-plane polarization underneath the electrode, while d is the thickness of the
film, and φ is the applied electric potential.

12

Sample preparation.
[(PbTiO3)n/(SrTiO3)n]m superlattices were synthesized on TiO2-terminated singlecrystalline SrTiO3 (001) substrates via reflection high-energy electron diffraction (RHEED)assisted pulsed-laser deposition (KrF laser). The growth temperature and oxygen pressure for
the bottom SrTiO3 layer were 700°C and 50 mTorr, respectively. The PbTiO3 and the top
SrTiO3 were grown at 610 °C in 100 mTorr oxygen pressure. For all materials, the laser fluence
was 1.5 J/cm2 with a repetition rate of 10 Hz. RHEED was used during the deposition to ensure
the maintenance of a layer-by-layer growth mode for both the PbTiO3 and SrTiO3. The specular
RHEED spot was used to monitor the RHEED oscillations. After deposition, the
heterostructures were annealed for 10 minutes in 50 Torr oxygen pressure to promote full
oxidation and then cooled down to room temperature at that oxygen pressure.
Scanning transmission electron microscopy.
Plan-view samples of the SrTiO3/PbTiO3 superlattices for STEM experiments were prepared
by gluing a 2.5 mm × 2.5 mm film on a 3 mm molybdenum grid. Cross-sectional samples of
the SrTiO3/PbTiO3 superlattices for TEM experiments were prepared by gluing two 3 mm × 2
mm films face-to-face on a 3 mm molybdenum grid. Samples were then ground, dimpled, and,
finally, ion milled. A Gatan PIPS II was used for the final ion milling. Before ion milling, the
samples were dimpled down to less than 20 μm. HAADF-STEM images were recorded by using
the Cs-corrected TEAM1 FEI Titan microscope working at 300 kV at room temperature. A
HAADF detector resulting in “Z-contrast” images were used to record the HAADF-STEM
images. The beam convergence angle was 17 mrad. The dark-field diffraction contrast image
was recorded using a TitanX microscope (FEI) working at 300 kV.
13

Acknowledgements
A start-up grant from Zhejiang University is acknowledged (Z. H.). This work was
financially supported by the Fundamental Research Funds for the Central Universities (No.
2021FZZX003-02-03). The phase-field simulation is performed on Shanghai Supercomputing
Center (SSC), specifically on the MoFang III cluster.
Author contributions
Z. H. conceived the idea. L. Z. performed the phase-field simulations with the help from L. C.
S. D. carried out the synthesis of the superlattice samples. Y. T. and H. T. performed the TEM
characterization. L. Z., Y. W., S. D., Y. T., L. -Q. C., R. R., Z. H. analyzed the data and co-wrote
the manuscript. Y. W., Y. H., L. -Q. C., R. R., and Z. H. supervised the research. All authors
contributed to the discussions and manuscript preparations.
Ethics declarations
Competing interests
The authors declare no competing interests.

14

References
[1] I. Naumov, L. Bellaiche, H. Fu, Unusual phase transitions in ferroelectric nanodisks and nanorods, Nature 432,
737 (2004).
[2] I. Naumov, H. Fu, Vortex-to-Polarization Phase Transformation Path in Ferroelectric Pb(Zr, Ti)O3
Nanoparticles, Phys. Rev. Lett. 98, 077603 (2007).
[3] C. T. Nelson, B. Winchester, Y. Zhang, et al., Spontaneous Vortex Nanodomain Arrays at Ferroelectric
Heterointerfaces. Nano Lett. 11, 828– 834 (2011).
[4] A. Yadav, C. T. Nelson, S. -L. Hsu, et al., Observation of Polar Vortices in Oxide Superlattices, Nature 530,
198-201 (2016).
[5] W. Geng, X. Guo, Y. Zhu, et al., Rhombohedral–Orthorhombic Ferroelectric Morphotropic Phase Boundary
Associated with a Polar Vortex in BiFeO3 Films. ACS Nano 12 (11), 11098-11105 (2018).
[6] Y. L. Tang, Y. L. Zhu, X. L. Ma, et al., Observation of a periodic array of flux-closure quadrants in strained
ferroelectric PbTiO3 films. Science 348, 547–551 (2015).
[7] X. Li, C. Tan, C. Liu, et al., Atomic-scale observations of electrical and mechanical manipulation of topological
polar flux closure, PNAS 117 (32), 18954-18961 (2020).
[8] Z. Hong, L. -Q. Chen, Switchable polar spirals in tricolor oxide superlattices, Acta Mater. 164, 493-498 (2019).
[9] J. Peters, G. Apachitei, R. Beanland, et al., Polarization curling and flux closures in multiferroic tunnel junctions,
Nat. Commun. 7, 13484 (2016).
[10] S. Das, Y. L. Tang, Z. Hong, et al., Observation of room-temperature polar skyrmions, Nature 568, 368–
372(2019).
[11] Z. Hong, L. Chen, Blowing polar skyrmion bubbles in oxide superlattices, Acta Mater. 152, 155-161 (2018).
[12] Y. Nahas, S. Prokhorenko, L. Louis, et al., Discovery of stable skyrmionic state in ferroelectric
nanocomposites. Nat. Comm. 6, 8542 (2015).
[13] Y. J. Wang, Y. P. Feng, Y. L. Zhu, et al., Polar meron lattice in strained oxide ferroelectrics, Nat. Mater. 19,
881–886 (2020).
[14] S. Das, Z. Hong, M. McCarter, et al., A new era in ferroelectrics, APL Mater. 8, 120902 (2020).
[15] A. K. Yadav, K. X. Nguyen, Z. Hong, et al., Spatially resolved steady-state negative capacitance, Nature 565,
468–471(2019).
[16] S. Das, Z. Hong, V. A. Stoica, et al., Local negative permittivity and topological phase transition in polar
skyrmions, Nat. Mater. (2020).
[17] Jorge Íñiguez, Pavlo Zubko, Igor Luk’yanchuk, Andrés Cano, Ferroelectric negative capacitance, Nat. Rev.
Mater. 4 (4), 243-256 (2019).
[18] P. Shafer, P. García-Fernández, P. Aguado-Puente, et al., Emergent chirality in the electric polarization texture

15

of titanate superlattices, PNAS 115(5), 915-920 (2018).
[19] S. Prosandeev, S. Prokhorenko, Y. Nahas, and L. Bellaiche, Prediction of a novel topological multidefect
ground state, Phys. Rev. B 100, 140104(R) (2019).
[20] T. Shimada, L. Lich, K. Nagano, et al., Polar Superhelices in Ferroelectric Chiral Nanosprings, Sci. Rep. 6,
35199 (2016).
[21] L. Lich, T. Shimada, J. Wang, et al., Switching the chirality of a ferroelectric vortex in designed nanostructures
by a homogeneous electric field, Phys. Rev. B 96, 134119 (2017).
[22] Y. Tikhonov, S. Kondovych, J. Mangeri, et al., Controllable skyrmion chirality in ferroelectrics, Sci. Rep. 10,
8657 (2020).
[23] V. A. Stoica, N. Laanait, C. Dai, et al., Optical creation of a supercrystal with three-dimensional nanoscale
periodicity, Nat. Mater. 18, 377–383 (2019).
[24] K. Yamada, S. Kasai, Y. Nakatani, et al. Electrical switching of the vortex core in a magnetic disk, Nat. Mater.
6, 270–273 (2007).
[25] J. Sampaio, V. Cros, S. Rohart, et al. Nucleation, stability and current-induced motion of isolated magnetic
skyrmions in nanostructures, Nat. Nanotechnol. 8, 839–844 (2013).
[26] Z. Hong, A. R. Damodaran, F. Xue, et al., Stability of Polar Vortex Lattice in Ferroelectric Superlattices, Nano
Lett. 17, 2246−2252 (2017).
[27] Y. Zhou, M. Ezawa, A reversible conversion between a skyrmion and a domain-wall pair in a junction
geometry, Nat. Commun. 5, 4652 (2014).
[28] N. Nagaosa, Y. Tokura, Topological properties and dynamics of magnetic skyrmions, Nat. Nanotechnol. 8,
899e911(2013).
[29] Y. Nahas, S. Prokhorenko, J. Fischer, et al., Inverse transition of labyrinthine domain patterns in ferroelectric
thin films, Nature 577, 47 (2020).
[30] Y. Nahas, S. Prokhorenko, Q. Zhang, et al., Topology and control of self-assembled domain patterns in lowdimensional ferroelectrics, Nat. Commun. 11, 5779 (2020).

[31] Y. L. Li, S. Y. Hu, Z. K. Liu, et al. Effect of Substrate Constraint on the Stability and Evolution of
Ferroelectric Domain Structures in Thin Films. Acta Materialia 50(2), 395-411(2002).

16

[32] L. Q. Chen, Phase-Field Models for Microstructure Evolution. Ann. Rev. Mater. Res. 32, 113-140 (2002).
[33] L. Q. Chen, Phase-field method of phase transitions/domain structures in ferroelectric thin films: A review.
J. Am. Ceram. Soc. 91(6), 1835-1844 (2008).
[34] M. Haun, E. Furman, S. Jiang, H. Mckinstry, L. Cross, Thermodynamic theory of PbTiO 3. J. Appl. Phys. 62,
3331-3338 (1987).
[35] A. Tagantsev, Landau Expansion for Ferroelectrics: Which Variable to Use? Ferroelectrics 375, 19-27 (2008).
[36] A. Tagantsev, The role of the background dielectric susceptibility in uniaxial ferroelectrics. Ferroelectrics 69,
321-323 (1986).
[37] Y. Zheng, C. Woo, Giant piezoelectric resistance in ferroelectric tunnel junctions. Nanotechnology 20, 075401
(2009).
[38] J. Wang, X. Ma, Q. Li, J. Britson, L. Chen, Phase transitions and domain structures of ferroelectric
nanoparticles: Phase field model incorporating strong elastic and dielectric inhomogeneity. Acta Mater. 61(20),
7591 (2013).

17


# Marker extraction (pdftotext interim) — arXiv:2411.05576

> Source: zhang2024.pdf -> pdftotext. Full text in work/textures-polar-zhang2024.txt

Observation of Moiré Plasmonic Skyrmion Clusters
Lan Zhang 1, Lipeng Wan 1,2,* , Weimin Deng 1,*, Liang Hou1, Jumin Qiu 1,
Qiushun Zou 3, Tongbiao Wang 1, Daomu Zhao 4, Tianbao Yu 1,*
1

School of Physics and Material Science & Jiangxi Provincial Key Laboratory of Photodetectors,
Nanchang University, Nanchang 330031, China;
2
Leiden Institute of Physics, Leiden University, Leiden, CA 2333, The Netherlands;
3
Faculty of Electrical Engineering and Computer Science, Laboratory of Infrared Material and Devices,
Zhejiang Key Laboratory of Advanced Optical Functional Materials and Devices, Advanced Technology
Research Institute, Ningbo University, Zhejiang 315211, China;
4
Zhejiang Key Laboratory of Micro-nano Quantum Chips and Quantum Control, School of Physics, Zhejiang
University, Hangzhou 310058, China;
* Corresponding Authors: Lwanoptics@ncu.edu.cn; dengweimin@ncu.edu.cn; yutianbao@ncu.edu.cn;

Skyrmions are topological defects belonging to nontrivial homotopy classes in particle theory. Their
remarkably stable topology has recently been observed in electromagnetic waves. For the evanescent
fields near a surface, this has been realized so far only for elementary optical skyrmions, with a fixed
skyrmion number. Here we report, both in theory and experiment, the concept of moiré plasmonic
skyrmion clusters, where multi-skyrmions are nested to form a large optical skyrmion cluster. By
leveraging twistronics engineering of plasmonic nanostructures, we demonstrate both crystallized
and quasi-crystallized optical skyrmion lattices, revealing an unprecedented degree of topological
control. In a misaligned composite nanostructure, the rapid inverting of optical skyrmion number is
achieved, which is explained by a lattice model. This topological change of moiré plasmonic skyrmion
clusters can serve as a precise beacon of the relative alignment deviation between composite
nanostructures.

INTRODUCTION

Topology continues to reform optical physics, offering vast
opportunities for fundamental research and technological
applications, including high-dimensional vortices [1],
polarization singularities [2], and correlation switch [3].
Skyrmions are topologically stable quasiparticles, originally
proposed as a topological soliton solution by the British
particle physicist Tony Skyrme in his study of unified field
theory. Apart from the field of high energy physics,
skyrmions have been discovered in many other fields, such
as Bose–Einstein condensates [4], liquid crystals [5], and
magnetic materials [6]. In 2018, two pioneering schemes for
realizing optical skyrmion lattices were proposed [7,8], by
either utilizing surface plasmon polaritons (SPPs)
interference to form on-chip optical polarization skyrmions,
or exploiting the topological defects in the local optical spin
field, forming an isolated optical spin skyrmion. The time
dynamics of optical skyrmion were also well-resolved [9,10].
The concept of skyrmion was later extended to various wave

configuration [11–15], such as Stokes parameter of paraxial
propagating light [16], pseudo-spin vector in photonic
crystals [17], supertoroidal pulses [18], electromagnetic
vector of spoof localized surface plasmons [19–21] and
optical skyrmion beam generators [22]. Characterized by
their ultracompact size and high stability, photonic
skyrmions enable the realization of pico-metric
displacement sensing [23].
Optical skyrmions are typically generated as isolated
unit or periodic lattices with fixed symmetry and skyrmion
number. This limits the capacity of photonic devices by
encoding information in the topological degree of skyrmions.
To advance higher density information storage technologies
and photonic devices, high-degree optical skyrmions with
tunable skyrmion numbers are essential. Only quite recently,
outstanding work has revealed that the symmetry of the
photonic skyrmion lattice can be modified by tuning the
wavelength [24], but no study has directly been explored in
the high-degree optical skyrmion. The major challenge is the
fact that the multiple 3D topology structures should be

manipulated on a 2D plane simultaneously.
In this work, we theoretically propose and
experimentally observe the plasmonic skyrmion clusters, in
which multiple Néel-type plasmonic skyrmions nested to
form a large optical skyrmion cluster, where the information
encoded by the number of skyrmion units exceeding one
provides higher storage density for photonic devices. This is
achieved using twistronics engineering of plasmonic
nanostructure system. The composite six-fold symmetric
nanostructure with an engineered twist is used to excites 3D
polarization “quasi-particles states” interference on a 2D
plane. We found that in the composite nanostructures, the
optical skyrmion number is rapidly reversed for the certain
alignment deviations. Twisting the composite six-fold
symmetric nanostructures enables the generation of moiré
optical skyrmions superlattice, which is induced by the
interference of dual groups of skyrmion lattices in one plane.
This resembles the twisted bilayer graphene [25–27] and
twisted bilayer photonic crystals [28–31]. Our proposed
skyrmion superlattices may have different crystal or
quasicrystal structure with well-defined symmetry and
periodicity, depending on the twist angle. Since optical
skyrmions are topologically stable quasiparticles, the
changes in the twist angle of a few degrees allow us to track
the optical skyrmion on the nanoscale. Continuous changes
in the twist angle result in the observation of the nucleation
as well as the collapse of optical skyrmions.

RESULTS

Moiré-induced optical skyrmion clusters
Figure 1 shows the concept and generation method of
moiré optical skyrmion clusters. We proposed a
twisted plasmonic platform [Fig. 1A], where composite
nanostructures with a twist are introduced into the
same film. This excites the superposition of well-

defined
transverse-magnetic
(TM)
guided
waves, leveraging two hexagonal nanoslits with
controlled twist angle to generate superimposed
plasmonic polarization states. Excited by propagating
light with spin angular momentum 𝝈 = ±𝟏 impinging
on this composite nanostructure, the threedimensional (3D) polarized electric field on the 2D film
is governed by the superposition of dual groups of
plasmonic wave, 𝐄𝒂 (𝐫, 𝟎) and its twisted replica
𝐄𝒃 (𝐫, 𝜽). Such surface waves propagate in the transverse
plane and evanescently decay in the axial direction. The zcomponent of the electric field thus takes the form of
𝐸 𝑧 (𝐫) = 𝐸𝑎𝑧 (𝐫, 0) + 𝐸𝑏𝑧 (𝐫, 𝜃)
̃ −𝑖(𝐤𝑗 (0)∙𝐫−𝜙𝑗 ) + ∑𝑁=6
̃ −𝑖[𝐤𝑗 (𝜃)∙𝐫−𝜙𝑗 −∆𝜙] },
= e−|𝑘𝑧|z {∑𝑁=6
𝑗=1 E𝑗 𝑒
𝑗=1 E𝑗 𝑒

(1)

where 𝐤𝑗 (𝜃) = ℝ𝑘𝑡 [cos 𝜑𝑗 , sin 𝜑𝑗 ] with ℝ being the 2D
unitary rotation matrix [cos 𝜃, − sin 𝜃 ; sin 𝜃 , cos 𝜃], 𝑘𝑡
and 𝑘𝑧 are the transverse and axial components of the
wave vector such that 𝑘𝑡2 + 𝑘𝑧2 = 𝑘02 , relating to the
free-space wavenumber 𝑘0. ̃
E𝑗 is the amplitude of each
surface wave. ∆𝜙 denotes the relative phase difference
between the two groups of electric fields, and 𝜙𝑗 denotes
the orientation-associated geometric phase of the jth
nanoslit, i.e. 𝜙𝑗 = 2𝜋𝜎𝑗⁄𝑁 . To ensure the in-phase
condition for all nanoslits pairs, two nanoslits is shifted by
half an SPP wavelength 𝜆S .
According to Eq. (1), we plot the axial field component
at 𝜃 = 38.21 degrees. Superimposed optical polarization
lattices are observed [Fig. 1B]. For the total interference 3D
polarization vector 𝐄̅, after normalization, we have
Re[𝐄𝒂 (𝐫,0) + 𝐄𝒃 (𝐫,𝜃)]
𝐄̅(𝐫, 𝜃) = |𝐄 (𝐫,0)
.
(𝐫,𝜃)|
𝒂

+ 𝐄𝒃

(2)

Figure 1. Moiréoptical skyrmion cluster generator. (A) The nanostructure consists of two groups of hexagonal nanoslits with a relative twist etched on a gold
layer, producing high-degree plasmonic skyrmion clusters. (B) Real component of the axial electric field at 38.21-degrees twist that sculptures the typical moiré

optical skyrmion superlattice. (C) Vector representation of the local unit electric field vector of the same twist angle of (B) showing optical skyrmion cluster. (D)
Fourier spectral of the axial electric field component. (E) The relationship between twist angle and moiréoptical skyrmion period.

To gain insight about the polarization topology, we
calculate the skyrmion number 𝑄(𝜃) per unit cell,
which characterizes the number of “quasi-particle”
skyrmion in a wave, is
𝑄(𝜃) =

1
4𝜋

∬𝐶𝑒𝑙𝑙 s (𝐫, 𝜃)𝑑𝐫,

(3)

where the integral covers the unit cell, and s is the
skyrmion number density (SND), takes the form of
s(𝐫, 𝜃) = 𝐄̅ ∙ [∂𝑥 𝐄̅ × ∂𝑦 𝐄̅].

(4)

Deriving the transverse electric field from Maxwell's
equations, we obtain the 3D polarization structure, as seen
in Fig. 1C, and skyrmion number for each unit is calculated to
be Q = -3. This is a manifestation of optical skyrmion
cluster, which is in contrast to the elementary optical
skyrmion (Q = ±1) lattice with C4 and C6 symmetry.
To interpret this, we consider interference of two
skyrmion lattices 𝑹𝑎 = 𝑛1𝒂1 + 𝑛2𝒂2 and 𝑹𝒃 = 𝑛1′ 𝒂′𝟏 +
𝑛2′ 𝒂′𝟐 = ℝ𝑹𝒂 , where 𝑛1, 𝑛2, 𝑛1′ , 𝑛2′ are integers, and the
lattice is described by two primitive lattice vectors
𝒂𝟏 = (𝛼, 0) and 𝒂𝟐 = (𝛼⁄2 , √3𝛼⁄2) with 𝛼 being the
distance between the closest skyrmions. The
interference of dual groups of skyrmion lattices
described by 𝑹𝑎 and 𝑹𝑏 reshapes the topology of the
electric field. In the case that 𝑹𝑎 = 𝑹𝑏 holds for a set of

integers {𝑛1 , 𝑛2 , 𝑛1′ , 𝑛2′ } , the resulting superimposed
electric field remains periodic, while superimposed
patterns in all other cases are quasi-periodic. The
generated cell of moirésuperlattice is much larger than
the nontwisted case, with each cell contains multiple
skyrmion units (See Supplemental Material S5). It is
this trick that allows us to generate the optical
skyrmion cluster that contains multiple skyrmion units,
enabling not only the on-chip crystallization of optical
skyrmion but also their quasi-crystallization.
To understand the plasmonic skyrmion clusters in
momentum space, we proceed by analyzing the real
component of the axial electric field in the spatial-frequency
domain. This is achieved by performing a 2D Fourier
transform of the axial field described by Eq. (1)
𝑆̃(𝒇) = ∑𝑁=12
𝑗=1 𝛾𝑗 𝛿(𝐤𝑗 − 2π𝒇),

(5)

where δ denotes the Dirac delta function, and the function ϒj
denotes the weight of the respective spatial frequency
component. The vector fj = kj/2π describes the frequency of
the interfered SPP waves. This is manifested in the spatial
frequency domain as interference of the lattice topology {f1,
f3, …, f9, f11} and the lattice topology {f2, f4, …, f10, f12} with the
twist angle θ, and the magnitude | fj | equals to kspp/2π, see
Fig. 1D.

Figure 2. Simulation and experimental demonstration of the periodic plasmonic skyrmion clusters. (A) The commensurate twist angle for the generation of
optical skyrmion superlattices. (B)-(C) Simulation results of moiréoptical skyrmion superlattices with well-defined symmetry at several commensurate twist
angles. (B) 𝜃 = 21.79°, (C) 𝜃 = 38.21°. Each figure contains simulated interference patterns of the real part of the axial field component. The unit cell of moiré
optical skyrmions is marked with a black dotted line, the patterns of the real part (top) and skyrmion number density (SND) (bottom) are shown on the left. (D)
Fourier spectral of the axial electric field component at 38.21 degrees. (E) The spatial distribution of skyrmions along a black dashed line at different twist angles.
(F) Schematic of the experimental setup. (G)-(I) Experimental results counterpart of (B)-(D). (J) Scanning electron microscope image of a 21.79-degree twisted
composite nanostructure sample.

Experimental measurement of optical skyrmion
clusters
To verify moiré optical skyrmion cluster predicted by this
concept and obtain accurate optical responses, both fullwave numerical simulations and near-field experimental
measurements were carried out. We fabricated samples

with controlled angle to generate diverse skyrmion clusters,
a scattering near-field scanning optical microscopy (Neaspec
neaSNOM) was used to measure the amplitude and phase of
the axial electric field on a 2D space via pseudo heterodyne
interferometric, as illustrated in Fig. 2F (details in
Supplemental Material). The Au film must have an adequate

thickness to block light from areas without nanoslits,
thereby avoiding unwanted waveguide phenomena and
ensuring ease of fabrication. The nanoslits are carved in the
120 nm Au layer atopped a 1 mm glass substrate, using a 3nm Ti adhesion layer between the gold and glass. The slits
are 15 m in length and 200 nm in width. The composite
nanostructure is illuminated by a 633 nm laser with lefthanded circular polarization at normal incidence, converting
free-space propagating light to an SPP mode with moiré
topology defects. The slit-scattering loss and slight position
shifts of the nanoslits cause minimal amplitude asymmetry,
which does not impair our results [32] (For the properties of
excited surface waves, see Supplemental Materials).
Periodic plasmonic skyrmion clusters-The plasmonic
skyrmion clusters are periodic only at specific twist angle, as
the relation 𝑹𝑏 = 𝑹𝑎 holds. For hexagonal lattices, this
leads to the commensurate twists with cos 𝜃 =
[(𝑝2 + 4𝑚𝑝+𝑚2)⁄2(𝑚2 + 𝑚𝑝 + 𝑝2 )] parameterized by
the integers p and m [33]. Figure 2A illustrates these angles
for various indices p and m. Depending on the value of θ,
the skyrmion number per unit cell changes.
SPPs are excited at the interface of air and gold in our
system at two commensurate twist angles, i.e. 21.79 degrees
and 38.21 degrees. Figure 2J shows the scanning electronic
microscopic (SEM) image of the sample with a twist angle of
21.79 degrees. Figure 2G presents the measured axial
electric field. Based on the experimental parameters, the
simulated axial electric field and SND are shown in Figs. 2B
and 2C. The spatial Fourier filtering technique is used to
remove the noise and background to obtain the Fourier

spectrum, as shown in Fig. 2I. This shows a good match to the
numerical [Fig. 2D] and theoretical prediction [Fig. 1D]. The
skyrmion cluster pattern can therefore be extracted. It can be
clearly observed that each lattice unit cell contains one and
three optical skyrmion units for 21.79 degrees and 38.21
degrees, respectively. They are periodically arranged in the
2D plane, which agrees with our theoretical expectations.
This phenomenon is analogous to the recently reported
skyrmion bags in liquid crystals [34]. Note that the twisting
center is not perfectly located at the center of the skyrmion
unit (See Supplemental Material S6). The deviation between
simulation and experiment in plasmonic 3D polarization is
attributed to the imperfect alignment, which includes
wavevector and polarization of incident beam, as well as
errors in sample fabrications. The change in skyrmion
number as the twist angle varies is a result of the modulation
of polarization, due to the interference between the two
twisted polarization lattices.
The period of the plasmonic skyrmion cluster
decreases sharply with the rotating angle θ, viz., 𝑔m (𝜃) =
𝛼⁄√2(1 − cos 𝜃), 𝜃 ∈ (0, 𝜋/6) [35], and is related to the
wavelength 𝜆S 𝑔m (𝜃, 𝜆S ) = 2𝜆S⁄√6(1 − cos 𝜃) , see Fig.
1E. The optical skyrmion period at 21.79 degrees and 38.21
degrees are both 3.12𝜆S [Fig. 2E], in accordance with the
moiré period given by 𝑔m (𝜃, 𝜆S ) . Compared to the
conventional optical skyrmion lattice with a skyrmion
number of one per lattice cell and fixed skyrmion density,
higher-degree skyrmion cluster with skyrmion numbers
larger than one can be formed.

Figure 3. Simulation and experimental demonstration of the quais-periodic plasmonic skyrmion clusters. (A)-(B) Simulation results of moiré
optical skyrmion superlattices with well-defined symmetry at several incommensurate twist angles. (A) 𝜃 = 15°, (B) 𝜃 = 30°. Each figure
contains simulated interference patterns of the real part of the axial field component. The unit cell of moiré optical skyrmions is marked with
a black dotted line, the patterns of the real part (top) and skyrmion number density (SND) (bottom) are shown on the left. (C) Fourier spectral
of the axial electric field component at 30 degrees. (D) The spatial distribution of skyrmions along a black dashed line at different twist angles.
(E)-(G) Experimental results counterpart of (A)-(C). (H) Scanning electron microscope image of a 30-degree twisted composite nanostructure
sample.

Quais-periodic plasmonic skyrmion clusters-Of
particular interest is the case as the twist angle is
incommensurate. The SEM image of the sample with an

incommensurate twist angle of 30 degrees is provided in Fig.
3H. The optical skyrmion lattices, referred to as superhexagonal topology [36], can persist in the aperiodic case,

as illustrated in Figs. 3A and 3E for a 15-degrees twist,
containing five optical skyrmion units in the highdegree skyrmion cluster. Instead, for the 30-degrees
twisted configuration [Fig. 3B and 3F], the optical skyrmion
units form a more disordered pattern, lacking the symmetry
observed in the 15-degree configuration. This disordered
skyrmion arrangement can be identified in Fig. 3D.
Compared to the numerical Fourier spectrum [Fig. 3C],
the measurement [Fig. 3G] shows a double ring shape,
which could be the unwanted phase ramp due to the
synchronization during measurements. Moiré
interference in composite nanostructures breaks the
conventional periodic symmetry in skyrmions but
unexpectedly spawns optical skyrmions topological

states
with
quasi-crystalline
order.
This
quasicrystallize state of optical skyrmion not only
retains the topologically conserved properties of
individual skyrmion (Q = -1), but also forms a Penroselike lattice by quasi-periodic spatial arrangement.
Quasicrystallize states of optical skyrmion originate
from the interference mismatch of the dual twisted
skyrmion lattice, which reveals the coexistence of hidden
long-range order and short-range disorder. It is noteworthy
that the quasicrystallize state under 30 degrees twist has no
periodic supercells. The optical skyrmion with multi-degreeof-freedom encoding capabilities (e.g., Q-value and Qposition) can empower the photonic integrated circuits for
high-throughput optical information processing.

Figure 4. Nanoscale dynamics of optical skyrmions. (A)-(C) The real part of the axial electric field, spanning an area of 12 μm × 12 μm. The
position of one skyrmion is selected in each image and marked with a black frame. (A) 𝜃0 = 21.79°, (B) 𝜃0 = 15°, (C) 𝜃0 = 21.79°. (D)-(F) The
movement of single skyrmion under small change in twist angles. The center of the skyrmion at each twist angle is marked by a yellow dot and
is compared with the center of the skyrmion at twist angle θ0 marked by a gray dot, θ0 are (D) 21.79 degs, (E) 15 degs, (F) 21.79 degs. (D)-(F)
correspond to the skyrmion marked in (A)-(C). (G)-(I) The relationship between Δθ = θ-𝜃 0 and |Γ(θ0 , ∆θ)|, here |Γ(θ0 , ∆θ)| is the distance
between skyrmion center at angle θ and 𝜃0. The scale bars are 200nm.

Tracking the “quasiparticles” of light at nanoscale
To further demonstrate the nanoscale behavior of
plasmonic skyrmion clusters in our system, we study
the configuration with small change of the twist angle,
providing a platform to track the nanoscale change of
optical skyrmion unit. Figures 4A-4C depict the out-ofplane electric field distribution in an area of 12 μm × 12
μm. Figures 4D–4F show the vector representation of
the transverse electric field within the black boxes of
Figs. 4A-4C. The center of optical skyrmion, determined
by the location of the minimum transverse (in-plane)
electric field, is pinpointed with its sign of skyrmion
number.
In small change of the twist angles, the skyrmion
topology is robust, but the nanoscale change in
displacement of optical skyrmion is pronounced. In

Figs. 4G-4I, we plot the skyrmion movement |Γ(θ0 , ∆θ)|
as a function of the change in twist angle. The change of
one degree induces the displacement of skyrmion
around 20 nm. Such displacement of the skyrmion is
not symmetric with positive and negative changes in
the twist angle. This is expected since, the change of
evanescent field is not linear with respect to the twist
angle, but modulated by the cosine function, as can be
seen from Eq. (1).
Alignment deviation beacon via optical skyrmions
Although the moiré optical skyrmion is robust to the
small change of twist angle, the effect caused by the
alignment deviation between the composite structures
cannot be mitigated. We first consider non-twisted
composite nanostructures θ = 0, in which there is a

lateral misaligned error ∆𝐫(∆𝑥, ∆𝑦) = (𝑥 − 𝑥𝑠 , 𝑦 − 𝑦𝑠 )
[Fig. 5A]. Such polarization topology is distorted
accompanied with symmetries breaking, the critical
aspect of this misalignment lies in the emergence of
topological transition. This takes place when two
triangular skyrmion lattices interfere to generate a
honeycomb lattice, thus resulting in the inversion of
skyrmion number. The critical inversion condition of
the optical skyrmion number is (see Supplemental
Material S7)
∆𝐫 =

𝜺

√3

(𝑛1 𝒂𝟏 + 𝑛2 𝒂𝟐 ); (𝑛1 − 𝑛2 ) ≢ 0 {mod 3},

(6)

where 𝜺 is a 2x2 antisymmetric matrix that relates the
coordinates of the composite structures and the optical
skyrmion lattices. In the case that (𝑛1 − 𝑛2 ) ≡
0 {mod 3} , two sets of excited skyrmion lattices are
coincides, showing the absence of optical skyrmion
switching. To prove this, we numerically simulate the

misaligned error and scan the skyrmion number per
lattice versus the alignment deviations along the y-axis
( ∆x = 0, Fig. 5C) and the x-axis ( ∆𝑦 = 0, Fig. 5D),
respectively. When the condition given by Eq. (6) is
satisfied, rapid inversion of the optical skyrmion
number from negative to positive is observed, and in
the intermediate state, these optical skyrmions
collapse. Note that inversion does not occur when the
displacement is along the x axis [Fig. 5D]. The physical
picture becomes trivial for the twisted cases θ≠0, as the
sudden switch of optical skyrmion state disappears due
to the symmetry breaking of the superposed structures.
Figures 5E-5G show the axial electric field for the
structural alignment deviations (𝛼, 0) , (𝛼/2, √3𝛼/2)
and (0, √3𝛼) at 30 degrees twist, respectively. The
displacement induces the translation of the optical
skyrmion superlattice, which can be interpreted from
the change in the constant phase factor.

Figure 5. Optical skyrmions in the composite nanostructure with lateral misaligned error. (A) The structure consists of two sets of hexagonal
slits with a relative displacement error ∆𝐫 = (∆𝑥, ∆𝑦). For the non-twist case, the theoretically predicted locations (B) where the skyrmion
nucleate, with the red and blue circles representing the positive and negative skyrmion topological points. Optical skyrmion number along the
y-axis (x = 0) (C) and x-axis (y = 0) (D), from which the skyrmion topology is observed to reverse along the y-direction. The orange, green and
blue solid circles represent the positive, zero and negative skyrmion topology in the simulation scan. The insets present the real part of the
axial electric field (left) and optical skyrmion number density (right) at ∆𝑦/λ𝑠𝑝𝑝 = 0 and 2/3 (C), and at ∆𝑥/λ𝑠𝑝𝑝 = 2/√3 (D). The electric field
and skyrmion number density are plotted at 5*5 μm. For the twist case θ = 30 degs with displacement error. The real part of the axial electric
field at (E) ∆𝑥 = 𝛼, ∆𝑦 = 0; (F) ∆𝑥 = 𝛼/2, ∆𝑦 = √3𝛼/2; (G) ∆𝑥 = 0, ∆𝑦 = √3𝛼. The line-filled circle in (F)-(G) marks an optical skyrmion unit
when there is no alignment error, and the yellow solid circle represents the corresponding displaced skyrmion unit if the composite structure
is misaligned.

DISCUSSION
In conclusion, we theoretically propose and
experimentally measure the plasmonic skyrmion clusters
containing multi-skyrmions in a unit cell. Dual groups of
optical skyrmion lattices are interfered to generate
plasmonic skyrmion clusters via twistronics engineering of
plasmonic nanostructures. This method provides a step

towards high-degree optical skyrmions. The twist angle
controls the nanoscale change of optical skyrmion, affording
a powerful platform to engineer and explore the plasmonic
skyrmion clusters in commensurate and incommensurate
geometries. The experimental results corroborate our
numerical and theoretical findings, which demonstrate the
moiré-induced phenomena in twist-plasmonic systems. The

formation of multi-skyrmion complexes showcases the
potential of twist-angle degrees of freedom for controlling
high-dimensional topology at subwavelength scales.
In the case of well-aligned composite structures, the
resulting moiré pattern facilitates the formation of optical
skyrmions with a well-defined skyrmion number. However,
displacement errors of the structures can cause the switch of
skyrmion topology, providing applications in the
characterization of twisted bilayer structures and in the
alignment of lithography mask. For instance, the nanometerscale optical metrology could be achieved by measuring the
change of skyrmion number. Our results are quite general, as
it can not only be integrated into various photonic
devices [37–39] and technologies [40–42], offering
promising functionalities [43,44] and improved
performance [45], but also be applied to other wave systems,
ranging from water waves [46] to partially coherent
waves [47–49]. More broadly, our results suggest that moiré
engineering- previously confined to van der Waals materials
- represents a universal strategy for manipulating quasiparticle topology across wave systems.

MATERIALS AND METHODS

Numerical Implementation
For numerical simulations of the near-field of the
plasmonic system, a 3D finite-difference time-domain
(FDTD) method is performed to solve Maxwell’s
equation numerically in time domain. The composite
nanostructure and monitoring points are placed within
a 35 µm × 30 µm × 1.5 µm volume, with perfectly
matched layer (PML) boundaries are set in all the
directions. A mesh with a resolution of 20 nm × 20 nm
× 5 nm is used to cover both the nanostructure and the
monitoring points, ensuring adequate sampling of the
polarization state of the optical skyrmion. The
thickness and permittivity of the gold film are set as 120
nm and 𝜀 = −10.6 + 1.7𝑖 [50], respectively. In the
simulation, a left circularly polarized Gaussian beam
with a wavelength of 633 nm is incident on the
plasmonic nanostructure. The beam waist is larger
than the dimensions of the sample structure to ensure
all the nanoslits are well excited.
Sample Fabrication
The samples are fabricated on a 120 nm-thick Au layer,
which was deposited previously on a 1 mm-thick glass
substrate using Electron beam evaporation (HHV,
AUTO500) with a deposited rate of 1 A/s. A 3-nm Ti is
used as the adhesion layer between the gold and glass.
Subsequently, the SPP coupling composite structures
with nanoslits width 150 nm is etched using focused
ion beam etching (Helios G4) from the metal side. This
is controlled by the software named NanoBuilder. The
etching parameters were set as 7 pA and 30 kV,

respectively. The fabricated sample was verified by the
scanning electron microscope (SEM), as shown in
Supplementary Material S1. Recessed structures in
these samples hinder the emission and detection of
secondary electrons, leading to localized attenuation
that appears as darker regions in the SEM images. The
topological properties of skyrmions are highly
sensitive to angular dislocations within composite
nanostructures (see Supplementary Material S8),
necessitating high precision in sample fabrication. The
processing errors are minimized within acceptable
limits. Specifically, for twist angles of 21.79°, 38.21°,
15°, and 30°, the processing errors are 1.3%, 0.8%,
1.1%, and 1.2%, respectively. These underscore the
level of precision required to accurately capture the
topological dynamics of skyrmions.
Near-field Measurements
The amplitude of the near field signal is measured using a
scattering (aperture-free) Near-field Scanning Optical
Microscope (s-NSOM, Neaspec Itd. VIS-neaSCOPE+s type),
with the experimental configuration schematically
illustrated in Fig. 3A. A 633-nm continuous wave laser
(Cobalt) is employed, with its beam split into two optical
paths. One beam is weakly focused by a plano-convex lens,
illuminating the sample from the glass side in a transmission
mode configuration. The second beam is utilized for
interferometric pseudo-heterodyne detection, which is
modulated by a vibrating mirror with a frequency of 300 Hz
interfered with the signal scattered from the sample to
reconstruct the full electric field information, including
amplitude and phase. To achieve circularly polarized
incident light, a quarter wave plate is positioned in the
optical path before the sample. The sample is positioned on
a moving stage, where a silicon atomic force microscope
(AFM) tip coated with platinum scattered predominantly the
axial electric field component into a detector. The tip vibrates
at oscillation frequencies between 200 and 230 kHz. The
tapping amplitude is 50 to 70 nm. This nanotip scatters
predominantly the axial electric field component into a
detector through a parabolic mirror, where the integration
time of detector is set to be 10-16 ms to ensure a good
signal to noise ratio. The desirable electric field, stemming
from the near field of the structure, is then demodulated at
higher harmonics of the tip’s vibration, to suppress the
scattered free-space background signal [51]. In the
measurements, the signal is extracted from the second
demodulation order.
Acknowledgements. The authors would like to thank
Neaspec GmbH and Quantum Design Co., Ltd. for help and
guidance in experimental measurements and analysis.

Funding. National Natural Science Foundation of China
(62305146, 12474299, 12164027); Training Program for
Academic and Technical Leaders of Major Disciplines in
Jiangxi Province (20243BCE51163); Natural Science
Foundation of Jiangxi Province (20232BAB211031,
20242BAB20023) and Nanchang University Youth Training
Program (PYQN20230064); the Project of Preeminent
Youth Fund of Jiangxi Province (20224ACB211002); Jiangxi
Provincial Key Laboratory of Photodetectors (No.
2024SSY03041).
Competing interests: the authors declare that they have no
competing interests.

Deleting Single Magnetic Skyrmions, Science 341,
636 (2013).
[7]

L. Du, A. Yang, A. V. Zayats, and X. Yuan, Deepsubwavelength features of photonic skyrmions in
a confined electromagnetic field with orbital
angular momentum, Nat. Phys. 15, 650 (2019).

[8]

S. Tsesses, E. Ostrovsky, K. Cohen, B. Gjonaj, N. H.
Lindner, and G. Bartal, Optical skyrmion lattice in
evanescent electromagnetic fields, Science 361,
993 (2018).

[9]

T. J. Davis, D. Janoschka, P. Dreher, B. Frank, F. J.
Meyer zu Heringdorf, and H. Giessen, Ultrafast
vector imaging of plasmonic skyrmion dynamics
with deep subwavelength resolution, Science 368,
386 (2020).

[10]

Y. Dai, Z. Zhou, A. Ghosh, R. S. K. Mong, A. Kubo, C.
Bin Huang, and H. Petek, Plasmonic topological
quasiparticle on the nanometre and femtosecond
scales, Nature 588, 616 (2020).

[11]

H. Teng, J. Zhong, J. Chen, X. Lei, and Q. Zhan,
Physical conversion and superposition of optical
skyrmion topologies, Photonics Res. 11, 2042
(2023).

[12]

S. Wang, Z. Zhou, Z. Zheng, J. Sun, H. Cao, S. Song, Z.
L. Deng, F. Qin, Y. Cao, and X. Li, Topological
Structures of Energy Flow: Poynting Vector
Skyrmions, Phys. Rev. Lett. 133, 73802 (2024).

[13]

D. A. Smirnova, F. Nori, and K. Y. Bliokh, WaterWave Vortices and Skyrmions, Phys. Rev. Lett. 132,
54003 (2024).

[14]

Y. Shen, Q. Zhang, P. Shi, L. Du, X. Yuan, and A. V.
Zayats, Optical skyrmions and other topological
quasiparticles of light, Nat. Photon. 18, 15 (2024).

[15]

L. Du, Z. Huang, J. Zhang, F. Ye, Q. Dai, H. Deng, G.
Zhang, and Z. Sun, Nonlinear physics of moiré
superlattices, Nat. Mater. 23, 1179 (2024).

[16]

S. Gao, F. C. Speirits, F. Castellucci, S. FrankeArnold, S. M. Barnett, and J. B. Götte, Paraxial
skyrmionic beams, Phys. Rev. A 102, 53513
(2020).

Data and materials availability: All data needed to
evaluate the conclusions in the paper are present in the
paper and/or the Supplementary Materials.
Note Added: After this work was completed, two related
preprints, arXiv: 2411.00645 and arXiv 2411.03032, came
to our attention.
Supplementary Materials
This PDF file includes:
Supplementary Text
Figs. S1 to S5
REFERENCES
[1]

B. C. Hiesmayr, M. J. A. De Dood, and W. Löffler,
Observation of Four-Photon Orbital Angular
Momentum Entanglement, Phys. Rev. Lett. 116, 1
(2016).

[2]

R. D. Muelas-Hurtado, K. Volke-Sepúlveda, J. L. Ealo,
F. Nori, M. A. Alonso, K. Y. Bliokh, and E. Brasselet,
Observation of Polarization Singularities and
Topological Textures in Sound Waves, Phys. Rev.
Lett. 129, 204301 (2022).

[3]

L. Wan, D. Raveh, T. Yu, D. Zhao, and O. Korotkova,
Optical resonance with subwavelength spectral
coherence switch in open-end cavity, Sci. China
Physics, Mech. Astron. 66, (2023).

[4]

U. Al Khawaja and H. Stoof, Skyrmions in a
ferromagnetic Bose - Einstein condensate, Nature
411, 918 (2001).

[5]

J. I. Fukuda and S. Žumer, Quasi-two-dimensional
Skyrmion lattices in a chiral nematic liquid crystal,
Nat. Commun. 2, (2011).

[17]

C. Guo, M. Xiao, Y. Guo, L. Yuan, and S. Fan, Meron
Spin Textures in Momentum Space, Phys. Rev. Lett.
124, 106103 (2020).

[6]

B. W. Niklas Romming, Christian Hanneken,
Matthias Menzel, Jessica E. Bickel and R. W. Kirsten
von Bergmann, André Kubetzka, Writing and

[18]

Y. Shen, Y. Hou, N. Papasimakis, and N. I. Zheludev,
Supertoroidal light pulses as electromagnetic

skyrmions propagating in free space, Nat.
Commun. 12, 1 (2021).
[19]

A. Mcwilliam, C. M. Cisowski, Z. Ye, F. C. Speirits, J.
B. Götte, S. M. Barnett, and S. Franke-arnold,
Topological Approach of Characterizing Optical
Skyrmions and Multi-Skyrmions, Laser Photon.
Rev. 2300155, 1 (2023).

[31]

J. Duan, N. Capote-Robayna, J. Taboada-Gutiérrez,
G. Álvarez-Pérez, I. Prieto, J. Martín-Sánchez, A. Y.
Nikitin, and P. Alonso-González, Twisted NanoOptics: Manipulating Light at the Nanoscale with
Twisted Phonon Polaritonic Slabs, Nano Lett. 20,
5323 (2020).

[32]

Y. M. J. & W. C. Wonjun Choi, Yonghyeon Jo, Joonmo
Ahn, Eunsung Seo, Q-Han Park, Control of
randomly scattered surface plasmon polaritons
for multiple-input and multiple-output plasmonic
switching devices, Nat. Commun. 8, 14636 (2017).

[20]

Y. Shen, E. C. Martínez, and C. Rosales-Guzmán,
Generation of Optical Skyrmions with Tunable
Topological Textures, ACS Photon. 9, 296 (2022).

[21]

Z. L. Deng, T. Shi, A. Krasnok, X. Li, and A. Alù,
Observation of localized magnetic plasmon
skyrmions, Nat. Commun. 13, 2 (2022).

[33]

M. Oudich, X. Kong, T. Zhang, C. Qiu, and Y. Jing,
Engineered moiré photonic and phononic
superlattices, Nat. Mater. 23, 1169 (2024).

[22]

W. Lin, Y. Ota, Y. Arakawa, and S. Iwamoto, On-Chip
Optical Skyrmionic Beam Generators, Optica 11,
1588 (2024).

[34]

D. Foster, C. Kind, P. J. Ackerman, J. B. Tai, M. R.
Dennis, and I. I. Smalyukh, Two-dimensional
skyrmion bags in liquid crystals and ferromagnets,
Nat. Phys. 15, 655 (2019).

[23]

A. Yang, X. Lei, P. Shi, F. Meng, M. Lin, L. Du, and X.
Yuan, Spin-Manipulated Photonic Skyrmion-Pair
for Pico-Metric Displacement Sensing, Adv. Sci. 10,
2 (2023).

[35]

[24]

M. Lin, Q. Liu, H. Duan, L. Du, and X. Yuan,
Wavelength-tuned
transformation
between
photonic skyrmion and meron spin textures, Appl.
Phys. Rev. 11, (2024).

H. Kumar, D. Er, L. Dong, J. Li, and V. B. Shenoy,
Elastic deformations in 2D van der waals
heterostructures
and
their
impact
on
optoelectronic properties: Predictions from a
multiscale computational approach, Sci. Rep. 5, 1
(2015).

[36]

G. Iooss and A. M. Rucklidge, Patterns and
Quasipatterns from the Superposition of Two
Hexagonal Lattices, SIAM J. Appl. Dyn. Syst. 21,
1119 (2022).

[37]

C. Genet and T. W. Ebbesen, Light in tiny holes,
Nature 445, 39 (2007).

[38]

J. Lin, J. P. B. Mueller, Q. Wang, G. Yuan, N. Antoniou,
X. C. Yuan, and F. Capasso, Polarization-controlled
tunable directional coupling of surface plasmon
polaritons, Science 340, 331 (2013).

[39]

M. C. Dheur, E. Devaux, T. W. Ebbesen, A. Baron, J.
C. Rodier, J. P. Hugonin, P. Lalanne, J. J. Greffet, G.
Messin, and F. Marquier, Single-plasmon
interferences, Sci. Adv. 2, 1 (2016).

[40]

A. Libster-Hershko, R. Shiloh, and A. Arie, Surface
plasmon polaritons on curved surfaces, Optica 6,
115 (2019).

[41]

I. Dolev, I. Epstein, and A. Arie, Surface-plasmon
holographic beam shaping, Phys. Rev. Lett. 109, 1
(2012).

[42]

D. Denkova, N. Verellen, A. V. Silhanek, V. K. Valev,
P. Van Dorpe, and V. V. Moshchalkov, Mapping

[25]

[26]

Y. Cao et al., Correlated insulator behaviour at halffilling in magic-angle graphene superlattices,
Nature 556, 80 (2018).
M. Yankowitz, S. Chen, H. Polshyn, Y. Zhang, K.
Watanabe, T. Taniguchi, D. Graf, A. F. Young, and C.
R. Dean, Tuning superconductivity in twisted
bilayer graphene, Science 363, 1059 (2019).

[27]

E. Y. Andrei and A. H. MacDonald, Graphene
bilayers with a twist, Nat. Mater. 19, 1265 (2020).

[28]

L. Du, M. R. Molas, Z. Huang, G. Zhang, F. Wang, and
Z. Sun, Moiré photonics and optoelectronics,
Science 379, 1313 (2023).

[29]

P. Wang, Y. Zheng, X. Chen, C. Huang, Y. V.
Kartashov, L. Torner, V. V. Konotop, and F. Ye,
Localization and delocalization of light in photonic
moiré lattices, Nature 577, 42 (2020).

[30]

Q. Fu, P. Wang, C. Huang, Y. V. Kartashov, L. Torner,
V. V. Konotop, and F. Ye, Optical soliton formation
controlled by angle twisting in photonic moiré
lattices, Nat. Photon. 14, 663 (2020).

Magnetic Near-Field Distributions of Plasmonic
Nanoantennas, in ACS NANO (2013), pp. 3168–
3176.

[47]

Y. Chen, A. Norrman, S. A. Ponomarenko, and A. T.
Friberg, Optical Coherence and Electromagnetic
Surface Waves, 1st ed., Vol. 65 (Elsevier B.V., 2020).

[43]

H. Y. Luan, Y. H. Ouyang, Z. W. Zhao, W. Z. Mao, and
R. M. Ma, Reconfigurable moiré nanolaser arrays
with phase synchronization, Nature 624, 282
(2023).

[48]

D. Li and D. Pacifici, Strong amplitude and phase
modulation of optical spatial coherence with
surface plasmon polaritons, Sci. Adv. 3, (2017).

[49]
[44]

Z. Jin et al., Phyllotaxis-inspired nanosieves with
multiplexed orbital angular momentum, ELight 1,
1 (2021).

D. Morrill, D. Li, and D. Pacifici, Measuring
subwavelength spatial coherence with plasmonic
interferometry, Nat. Photon. 10, 681 (2016).

[50]
[45]

P. Wang, Q. Fu, V. V Konotop, Y. V Kartashov, and F.
Ye, Observation of localization of light in linear
photonic quasicrystals with diverse rotational
symmetries, Nat. Photon. 18, 224 (2024).

P. Dvořák, T. Neuman, L. Břínek, T. Šamořil, R.
Kalousek, P. Dub, P. Varga, and T. Šikola, Control
and near-field detection of surface plasmon
interference patterns, Nano Lett. 13, 2558 (2013).

[46]

B. Wang, Z. Che, C. Cheng, C. Tong, L. Shi, Y. Shen, K.
Y. Bliokh, and J. Zi, Topological water-wave
structures manipulating particles, Nature 638,
394 (2024).

[51]

E. Ostrovsky, K. Cohen, S. Tsesses, B. Gjonaj, and G.
Bartal, Nanoscale control over optical singularities,
Optica 5, 283 (2018).


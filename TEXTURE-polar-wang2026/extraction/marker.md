<!-- extraction: pdftotext | arxiv:2604.26100 -->
Hidden Crossover and Relaxor-Like Response from Emerging Polar Skyrmion Correlations in
Ferroelectric Superlattices
Zhi-Yang Wang,1 Fei Yang,1, ∗ and Long-Qing Chen1, †
1 Department of Materials Science and Engineering and Materials Research Institute,

arXiv:2604.26100v1 [cond-mat.mtrl-sci] 28 Apr 2026

The Pennsylvania State University, University Park, PA 16802, USA
(Dated: April 30, 2026)
Polar skyrmions in ferroelectric superlattices are nanoscale topological polarization textures typically regarded as weakly coupled objects confined to individual layers, with a role secondary to that of the underlying
symmetry-breaking order parameter. Here using large-scale phase-field simulations of ferroelectric superlattices, we uncover a hidden thermal crossover deep inside the ferroelectric phase, where polar skyrmions evolve
from an uncorrelated, layer-resolved state into an interlayer-correlated ensemble. This crossover occurs without
additional symmetry breaking or a new order parameter, but produces a pronounced broad peak in the dielectric
susceptibility. The anomaly originates from the competition between correlation-enhanced response, associated with the growth of interlayer skyrmion correlations, and polarization-induced stiffness, which suppresses
dielectric fluctuations at low temperature. Under AC driving, the peak shifts with frequency, resembling relaxor
ferroelectrics despite the absence of quenched disorder or polar nanoregions. Our results establish a disorder-free
route to relaxor-like dielectric response and identify topological defect correlations as an organizing principle
for thermodynamic anomalies, providing a mechanism distinct from conventional critical behavior associated
with symmetry breaking and divergent order-parameter fluctuations.

Introduction.—Macroscopic thermodynamic anomalies in
ordered phases are commonly understood through the Landau
paradigm, in which thermodynamic responses are governed by
symmetry breaking, the associated order parameter [1], and
its various smooth fluctuations [2–11]. This framework has
been remarkably successful in describing ferroelectric transitions, where the dielectric susceptibility is tied to the onset and
growth of spontaneous polarization. However, ordered phases
can also host topological defects with well-defined topological
charges, i.e., singular configurations of the order parameter
that cannot be removed by smooth deformations [12], such as
vortices in superconductors [13–15], skyrmions in magnetic
systems [16–18], and disclinations in liquid crystals [19, 20].
These defects act as emergent objects with their own interactions, correlations, and dynamics, introducing a layer of
collective behavior beyond that captured by the conventional
order parameter. Their collective organization can dominate
macroscopic responses: proliferation, binding, or unbinding
of defects can control phase coherence and transport properties even in the absence of a conventional symmetry-breaking
transition, as exemplified by vortex physics in superconductors [13, 15] and the Berezinskii-Kosterlitz-Thouless transition [21–23]. These examples illustrate that collective phenomena in many-body systems can be governed not only by
symmetry breaking, but also by the topology and correlations of emergent defects that may dominate thermodynamic
response deep inside an ordered phase [24–26].
Polar skyrmions are topological defects in ferroelectric systems [27–31], characterized by a quantized skyrmion number [18, 32],


∫
𝜕 𝑝® 𝜕 𝑝®
1
𝑑 2 𝑟® 𝑝® ·
×
,
(1)
𝑁 𝑠𝑘 =
4𝜋
𝜕𝑥 𝜕𝑦
here 𝑝® denotes the normalized polarization vector field. Recent
advances in atomic-resolution imaging have established their

existence in ferroelectric superlattices, such as PbTiO3 /SrTiO3
(PTO/STO) [33]. These topological textures exhibit unconventional functionalities, including local negative dielectric
response [28], structural chirality [34], and terahertz collective dynamics [31], highlighting their potential as a platform
for emergent mesoscale physics. A central open question is
whether polar skyrmions can develop collective correlations
beyond their conventional description as weakly interacting,
layer-confined topological textures [35, 36], while they are
often treated as isolated topological excitations. This raises a
more fundamental issue: how are such correlations encoded in
the thermodynamic response of a material? In particular, it remains unclear whether the evolution from uncorrelated to correlated skyrmion states corresponds to a genuine symmetrybreaking phase transition, or instead reflects a correlationdriven crossover with distinct signatures in measurable quantities such as the dielectric susceptibility.
Driving a temperature-induced crossover between uncorrelated and coherently coupled polar skyrmions requires a superlattice in which the dielectric spacer develops a strongly
temperature-dependent polarization. In such structures, dipolar fields originating from the ferroelectric layers can penetrate
the spacer once it becomes sufficiently polarized, thereby enabling interlayer skyrmion coupling [37, 38]. Here we show
that polar skyrmions in oxide superlattices can develop strong
interlayer correlations upon cooling, giving rise to a hidden
thermal crossover that does not involve symmetry breaking or
the emergence of a new order parameter, but instead reflects
a collective reorganization of defect correlations and strongly
modifies the dielectric response. Using large-scale phase-field
simulations of prototypical (Pb 𝑥 Sr1−𝑥 TiO3 )/(PbTiO3 ) superlattices, we find that skyrmions evolve upon cooling from an
uncorrelated layer-resolved state into an interlayer-correlated
state. This crossover originates from the gradual buildup of
interlayer correlations: while skyrmions remain effectively de-

2
coupled at high temperature, cooling enhances the polarization
of the spacer layer, which activates dipolar-mediated coupling
and drives the formation of correlated skyrmion stacks. The
crossover produces a broad dielectric susceptibility peak well
below the ferroelectric transition temperature. Unlike a critical
anomaly, this peak results from the competition between the
growth of skyrmion correlations and the increasing stiffness
of the polarized state. Remarkably, under AC driving the peak
shifts with frequency, giving rise to a relaxor-like response in
a structurally ordered system. These results establish topological defect correlations as a route to thermodynamic anomalies and relaxor-like dynamics beyond conventional symmetrybreaking and disorder-based mechanisms.
Model—To investigate the thermodynamic properties of the
(Pb 𝑥 Sr1− 𝑥 TiO3 )16 /(PTO)16 superlattices across a range of temperatures, we employ the phase-field method. The polarization
® 𝑟 ) = (𝑃1 , 𝑃2 , 𝑃3 ) is taken as the order parameter to
vector 𝑃(®
construct the total free energy of the system [39]:
∫ h
i
® + 𝑓g (∇ 𝑃)
® + 𝑓elas ( 𝑃,
® 𝜀𝑖 𝑗 ) + 𝑓elec ( 𝑃,
® 𝐸)
® 𝑑𝑉,
𝐹=
𝑓L ( 𝑃)

the isotropic background dielectric constant and 𝜖 0 being the
vacuum dielectric permittivity.
The kinetics of the polarization is governed by the timedependent Ginzburg-Landau (TDGL) equation:
𝛿𝐹
𝜕𝑃𝑖 (®
𝑟 , 𝑡)
= −Γ
,
𝜕𝑡
𝛿𝑃𝑖 (®
𝑟 , 𝑡)

(7)

which relaxes the system toward thermodynamic equilibrium.
Here, Γ is a kinetic coefficient associated with domain-wall
mobility. Simulations are performed on a 200Δ × 200Δ × 200Δ
grid with Δ = 0.4 nm. The superlattice is constructed along
the 𝑧 direction, consisting of a substrate (20 grids), a central superlattice region (176 grids), and a top air layer (4
grids). The superlattice comprises alternating (PTO)16 and
(Pb 𝑥 Sr1−𝑥 TiO3 )16 layers, repeated five times, starting from a
(Pb 𝑥 Sr1−𝑥 TiO3 )16 block. The parameters of the free-energy
density function [42], together with full numerical details and
boundary conditions, are provided in the Supplemental Material, including Ref. [39–58].

𝑉

where the quadratic coefficient 𝛼𝑖 (𝑇) follows a Curie-Weiss
temperature dependence, while higher-order coefficients 𝛼𝑖 𝑗
and 𝛼𝑖 𝑗 𝑘 are taken to be temperature-independent.
Spatial variations are penalized by the gradient term,
𝑓g =

𝜕𝑃𝑖 𝜕𝑃 𝑘
1
𝐺 𝑖 𝑗 𝑘𝑙
,
2
𝜕𝑥 𝑗 𝜕𝑥𝑙

(4)

which is assumed here to take the isotropic form: 𝑔(𝜕 𝑗 𝑃𝑖 ) 2 ,
representing the nearest-neighbor interactions. Elastic effects
are incorporated through electrostrictive coupling,
𝑓elas =

1
1
𝐶𝑖 𝑗 𝑘𝑙 𝑒 𝑖 𝑗 𝑒 𝑘𝑙 = 𝑐 𝑖 𝑗 𝑘𝑙 (𝜀 𝑖 𝑗 − 𝜀 𝑖0𝑗 ) (𝜀 𝑘𝑙 − 𝜀 0𝑘𝑙 ),
2
2

(5)

with the spontaneous strain 𝜀 𝑖0𝑗 = 𝑄 𝑖 𝑗 𝑘𝑙 𝑃 𝑘 𝑃𝑙 . The mechanical
equilibrium is enforced via 𝜕 𝑗 𝜎𝑖 𝑗 = 0 under thin-film boundary
conditions [40]. Here, 𝐶𝑖 𝑗 𝑘𝑙 is the elastic stiffness, 𝑒 𝑖 𝑗 is the
elastic strain, 𝑄 𝑖 𝑗 𝑘𝑙 represents the electrostrictive coefficients,
and 𝜎𝑖 𝑗 is the elastic stress.
The electrostatic contribution is given by
1
𝑓elec = − 𝜖 0 𝜅 𝑏 𝐸 𝑖2 − 𝐸 𝑖 𝑃𝑖 ,
2

(6)

where the electric field 𝐸® is obtained by solving the Poisson
® = 0 assuming zero free charge denequation ∇ · (𝜖 𝑏 𝐸® + 𝑃)
sity and short circuit boundary condition[41], with 𝜅 𝑏 being

0.5

900

0.4
0.3

600

300

0.2

Interlayer
Uncorrelated-correlated
Crossover

0

200

400

0.1

600

(b) 1500

800

1000

Polarization (C/m2)

(3)

0.6
Ferroelectric
Transition

Susceptibility

𝑓L = 𝛼𝑖 𝑃𝑖2 + 𝛼𝑖 𝑗 𝑃𝑖2 𝑃2𝑗 + 𝛼𝑖 𝑗 𝑘 𝑃𝑖2 𝑃2𝑗 𝑃2𝑘 ,

(a) 1200

0

AC-1 tp=t 0

DC
AC-2 tp=2t0

Susceptibility

(2)
where the four terms correspond to Landau-Devonshire bulk
energy, gradient energy, elastic energy, and electrostatic energy, respectively. The Landau-Devonshire energy density is
expanded to the sixth order in 𝑃® to capture the ferroelectric
phase transitions:

AC-3 tp=3t0

1000

500

0

0

200

400

600

Temperature (K)

800

1000

FIG. 1. (a) DC dielectric susceptibility (blue dash-dotted curve)
and spatially averaged polarization magnitude (orange dashed curve
with cross markers) of the (Pb 𝑥 Sr1− 𝑥 TiO3 )16 /(PbTiO3 )16 superlattice
as functions of temperature for 𝑥 = 0.3. (b) AC and DC dielectric
susceptibilities of the same superlattice as functions of temperature
for 𝑥 = 0.3. The period 𝑡 𝑝 of the applied AC electric field is an integer
multiple of the fundamental period 𝑡 0 (see Supplementary Material).
The black arrow indicates the direction of the dielectric-peak shift.

3
Results—We first focus on a representative composition 𝑥 =
0.3 and compute the dielectric susceptibility as a function of
temperature. As shown in Fig. 1, two distinct features are
observed. A sharp, discontinuous peak at 𝑇𝑐 ∼ 800 K marks
the first-order ferroelectric transition, where cubic symmetry is
broken in both PTO and Pb 𝑥 Sr1− 𝑥 TiO3 layers via a proximity
effect, and a finite polarization develops across the superlattice
(orange cross curve). This corresponding dielectric response
follows conventional critical behavior governed by symmetry
breaking and divergent order-parameter fluctuations.
In conventional ferroelectrics (e.g., PbTiO3 [59–62]), the
dielectric susceptibility decreases monotonically upon cooling below the transition temperature. In contrast, in the
(Pb 𝑥 Sr1− 𝑥 TiO3 )/(PbTiO3 ) superlattice, a second broad peak
emerges at ∼ 500 K within the ferroelectric phase. The
polarization varies smoothly across this temperature without
any discontinuity, excluding an additional symmetry-breaking

(a) 700 K

500 K

300 K

100 K

(b)

transition and identifying this feature as a crossover. The
presence of this broad peak therefore signals a qualitative reorganization within the ferroelectric phase, which we attribute
to the onset of correlated polar skyrmion behavior.
Remarkably, under an applied AC electric field, the susceptibility peak shifts toward higher temperature with increasing
driving frequency, reminiscent of relaxor-like dielectric behavior [63]. This resemblance is striking because the present
superlattice is structurally ordered and contains no quenched
disorder or polar nanoregions. Therefore, the broad dispersive
response cannot be attributed to the conventional relaxor mechanism [63]. Instead, it indicates the slow collective relaxation
of an emerging interlayer-correlated skyrmion ensemble. The
frequency-dependent shift thus provides dynamical evidence
that the dielectric anomaly is controlled by defect correlations
rather than by a conventional ferroelectric transition.

(c)

FIG. 2. (a) Polar structures of the (Pb 𝑥 Sr1− 𝑥 TiO3 )16 /(PTO)16 superlattice (x=0.3) at T = 700 K, 500 K, 300 K, and 100 K, illustrating the
progressive spatial organization of polar textures upon cooling. (b) Temperature dependence of the out-of-plane skyrmion correlation function,
the correlation length (blue circles in the inset), and the oscillation amplitude (orange crosses in the inset). The colors of the correlation-function
curves indicate temperature. (c) Polarization ratio 𝛾 between Pb 𝑥 Sr1− 𝑥 TiO3 and PTO layers (blue circles), together with its first derivative
(orange crosses) and second derivative (inset) with respect to 𝑇.

To elucidate the origin of this crossover, we examine the
evolution of the polar structure at representative temperatures
(700 K, 500 K, 300 K, and 100 K), as shown in Fig. 2(a).
Below the ferroelectric transition (∼ 800 K), a finite polarization develops and polar skyrmions emerge in the PTO layers.
At high temperatures, these skyrmions are essentially uncorrelated and randomly distributed across different layers. Upon
cooling, however, they progressively align and form correlated structures along the out-of-plane direction, indicating
the emergence of interlayer correlation. To quantify this behavior, we compute the out-of-plane autocorrelation function

of the normalized polarization field 𝑝® = ®
𝑃/| ®
𝑃|,
∫
1
𝐶 (𝑧) =
𝑝(𝑥 ′ , 𝑦 ′ , 𝑧 ′ ) · ®
®
𝑝(𝑥 ′ , 𝑦 ′ , 𝑧 ′ + 𝑧)𝑑𝑥 ′ 𝑑𝑦 ′ 𝑑𝑧 ′ . (8)
𝑉 𝑉
The correlation function in Fig. 2(b) exhibits a damped oscillatory behavior with an additional linear decay. The oscillatory component reflects the periodic arrangement of polar
skyrmions across different PTO layers, while the exponential envelope captures the finite interlayer correlation length.
The linear decay originates from a finite-size geometric effect,
arising from the reduced overlap volume at large separations.
As the temperature decreases, the decay of the correlation
function becomes progressively slower, indicating an increas-

4
ing out-of-plane correlation length. To quantify this evolution,
we fit the data using an exponentially damped harmonic form
with a finite-size correction,

i
 𝑧 
h
 2𝜋𝑧
𝑧
+ 𝜙 + 𝐶0 exp −
1−
, (9)
𝐶 (𝑧) = 𝐴 cos
𝜆0
𝜉
𝐿

Paraelectric

900

T (K)

where 𝐴 is the oscillation amplitude, 𝜆0 = 12.8 nm corresponds to the superlattice periodicity, and 𝜉 denotes the outof-plane correlation length of the superlattice. Such a form is
characteristic of a correlated but non-long-range-ordered state
with finite coherence length. The geometry factor (1 − 𝑧/𝐿)
accounts for the finite thickness of the system. The extracted
temperature dependence of 𝜉 and 𝐴 is shown in the inset of
Fig. 2(b). Upon cooling, 𝜉 increases monotonically, demonstrating the progressive buildup of interlayer skyrmion correlations. In contrast, the oscillation amplitude 𝐴 decreases,
indicating that the layer-resolved modulation becomes weaker
as skyrmion textures in different PTO layers evolve toward a
more correlated interlayer configuration.
Physically, the emergence of correlations is often associated with the development of collective degrees of freedom,
even in the absence of a conventional symmetry-breaking order parameter. The interlayer correlations of polar skyrmions
here are controlled by the polarization of the Pb 𝑥 Sr1−𝑥 TiO3
layers, which mediate the coupling between the adjacent PTO
layers. At high temperatures, the weak polarization of the
Pb 𝑥 Sr1− 𝑥 TiO3 layers effectively decouples the neighboring
PTO layers, resulting in uncorrelated, layer-resolved skyrmion
distributions. Upon cooling, however, the polarization of the
Pb 𝑥 Sr1− 𝑥 TiO3 layers increases more rapidly than that of the
PTO layers, enabling dipolar interactions to propagate across
the spacer more effectively and thereby enhancing interlayer
coupling. The enhanced coupling promotes a coherent alignment of skyrmions across different layers, which reduces the
polarization gradient energy and stabilizes the correlated state.
To quantify this mechanism, we introduce the polarization ratio 𝛾 = 𝑃Pb 𝑥 Sr1− 𝑥 TiO3 /𝑃PTO [Fig. 2(c)], together with
its first and second temperature derivatives. As temperature
decreases, 𝛾 grows monotonically with a crossover from rapid
increase to saturation, reflecting the strengthening of interlayer coupling. Notably, near 𝑇 ∼ 500 K, the curvature of
𝛾(𝑇) changes sign, i.e., 𝑑 2 𝛾/𝑑𝑇 2 = 0, signaling an inflection
point. This temperature coincides with the broad peak in the
dielectric susceptibility below the ferroelectric transition, providing a direct link between the evolution of interlayer coupling
and the thermodynamic response. We therefore identify this
inflection point as the characteristic crossover temperature.
The correlation length 𝜉 [inset of Fig. 2(b)] reflects the
strength of the effective interlayer coupling, which is controlled
by the polarization ratio 𝛾, and increases upon cooling. This
evolution of skyrmion correlations directly impacts the dielectric response. Phenomenologically, the dielectric response is
enhanced by the growth of the correlated volume associated
with skyrmion stacking, but suppressed by the increasing stiffness of the polarized state. In this sense, the susceptibility is
controlled by two competing tendencies: an increasing corre-

1100

700

Skyrmions - Uncorrelated

500
300
100

Skyrmions - Correlated
0

0.1

0.2

xPb

0.3

0.4

FIG. 3. The calculated temperature-composition regime map of
(Pb 𝑥 Sr1− 𝑥 TiO3 )16 /(PTO)16 superlattices. The green, blue, and orange regions denote the paraelectric regime, uncorrelated skyrmion
regime, and interlayer-correlated skyrmion regime, respectively. Diamonds mark the characteristic crossover temperature between the
uncorrelated and correlated skyrmion regimes, while squares denote
the ferroelectric transition temperature extracted from simulations.
The color shading is a guide to the eye.

lation scale, represented by 𝜉 (𝑇), and an effective polarization
stiffness, denoted by 𝐾 (𝑇). The broad maximum in 𝜒(𝑇) naturally emerges when the enhancement from growing skyrmion
correlations is overtaken by the stiffening of the ferroelectric background at lower temperature. This competition gives
rise to a broad susceptibility peak well below the ferroelectric
transition, revealing a hidden crossover governed by defect
correlations rather than the symmetry breaking described by
the conventional Landau paradigm of phase transitions.
Increasing the Pb concentration in the Pb 𝑥 Sr1−𝑥 TiO3 layers enhances their polarization, thereby strengthening the interlayer coupling between skyrmions in adjacent PTO layers. This leads to a pronounced compositional dependence
of the crossover temperature between uncorrelated and correlated skyrmion states. To reveal this dependence, we
construct a temperature-composition regime map for the
(Pb 𝑥 Sr1−𝑥 TiO3 )16 /(PTO)16 superlattice (Fig. 3). The blue
and orange regions correspond to uncorrelated and correlated
skyrmion states, respectively, separated by a crossover regime
(white region). For low Pb concentration (𝑥 ≲ 0.1), skyrmions
remain effectively uncorrelated over the entire temperature
range. At higher concentrations, a crossover emerges, with the
crossover temperature (diamonds) increasing monotonically
with 𝑥, reflecting the enhanced interlayer coupling. At high
temperatures (𝑇 ≳ 850 K), the system enters a paraelectric
phase (green region). The ferroelectric transition temperature
𝑇𝑐 (squares) exhibits a weak dependence on composition. This
weak variation arises from the transition being dominated by
the PTO layers where 𝑇𝑐 is substantially higher than that of

5
Pb 𝑥 Sr1− 𝑥 TiO3 in the composition range (0 ≤ 𝑥 ≤ 0.4), resulting in an almost 𝑥 Pb -independent transition temperature.
Discussion.—Our results demonstrate that thermodynamic
responses in ferroelectric superlattices can be governed by correlations among topological defects rather than by symmetry
breaking alone. The crossover identified here does not introduce a new order parameter, but reflects a collective reorganization of polar skyrmions from an uncorrelated layer-resolved
state into an interlayer-correlated ensemble. It therefore represents a correlation-driven thermodynamic anomaly, rather
than a true thermodynamic phase transition. This establishes
a qualitatively different mechanism in which defect correlations, rather than symmetry, control macroscopic observables.
A central consequence of this mechanism is the emergence
of a pronounced and broad dielectric susceptibility peak deep
within the ordered phase. Unlike conventional anomalies
tied to criticality, this feature originates from the competition between correlation-enhanced response and polarizationinduced stiffness. The maximum in susceptibility appears
when these two tendencies balance, providing a mechanism
distinct from conventional critical behavior tied to symmetry
breaking and divergent order-parameter fluctuations. A particularly important implication is the emergence of relaxor-like
dynamics without quenched disorder. Conventional relaxor
ferroelectrics are commonly associated with chemical disorder and polar nanoregions, whereas the present superlattice
is structurally ordered. The frequency-dependent shift of the
dielectric peak instead originates from the slow collective dynamics of correlated polar skyrmions, establishing a disorderfree microscopic route to broad, dispersive dielectric response.
More broadly, our work identifies topological defect correlations as an organizing principle for functional responses
in ferroic materials. They are expected to impact a wide
range of functional properties, including dielectric, non-linearoptical [64], and thermal transport [65]. As the crossover identified here suggests a mechanism for generating non-monotonic
thermodynamic responses and is controlled by the polarization contrast between the constituent layers, it can be tuned
by composition, temperature, and superlattice design. This
provides a practical strategy for engineering dielectric and dynamical properties through controlled defect correlations. The
same principle may also be relevant to other ordered media in
which topological textures form interacting ensembles, including magnetic skyrmions and ferroic domain textures.
Acknowledgments— This work is supported by the Army Research Office under the ETHOS MURI via cooperative agreement W911NF-21-2-0162 for the development of oxide superlattice materials. All the simulations in this work are done
by the commercial software MuPRO. Long-Qing Chen has a
financial interest in MuPRO, LLC, a company which licenses
and markets the software package used in this research.

∗ fzy5099@psu.edu

† lqc3@psu.edu

[1] L. D. Landau and E. M. Lifshitz, Course of Theoretical Physics
(Elsevier, 2013).
[2] Y. Nambu, Quasi-particles and gauge invariance in the theory
of superconductivity, Phys. Rev. 117, 648 (1960).
[3] J. Goldstone, Field theories with “superconductor” solutions,
Nuovo Cim. 19, 154 (1961).
[4] J. Goldstone, A. Salam, and S. Weinberg, Broken symmetries,
Phys. Rev. 127, 965 (1962).
[5] Y. Nambu, Nobel Lecture: Spontaneous symmetry breaking in
particle physics: A case of cross fertilization, Rev. Mod. Phys.
81, 1015 (2009).
[6] F. Yang and M. W. Wu, Gauge-invariant microscopic kinetic theory of superconductivity: Application to the optical response of
Nambu-Goldstone and Higgs modes, Phys. Rev. B 100, 104513
(2019).
[7] V. Ambegaokar and L. P. Kadanoff, Electromagnetic properties
of superconductors, Il Nuovo Cimento 22, 914 (1961).
[8] P. B. Littlewood and C. M. Varma, Gauge-invariant theory of
the dynamical interaction of charge density waves and superconductivity, Phys. Rev. Lett. 47, 811 (1981).
[9] F. Yang and M. W. Wu, Theory of coupled dual dynamics of
macroscopic phase coherence and microscopic electronic fluids:
Effect of dephasing on cuprate superconductivity, Phys. Rev. B
104, 214510 (2021).
[10] F. Yang and L. Q. Chen, Microscopic phase-transition theory of
charge density waves: Revealing hidden crossovers of phason
and amplitudon, Phys. Rev. Lett. 136, 146503 (2026).
[11] D. Pekker and C. M. Varma, Amplitude/Higgs Modes in Condensed Matter Physics, Annu. Rev. Condens. Matter Phys. 6,
269 (2015).
[12] N. D. Mermin, The topological theory of defects in ordered
media, Rev. Mod. Phys. 51, 591 (1979).
[13] A. A. Abrikosov, The magnetic properties of superconducting
alloys, J. Phys. Chem. Solids 2, 199 (1957).
[14] H. F. Hess, R. B. Robinson, R. C. Dynes, J. M. Valles, and J. V.
Waszczak, Scanning-Tunneling-Microscope observation of the
Abrikosov flux lattice, Phys. Rev. Lett. 62, 214 (1989).
[15] G. Blatter et al., Vortices in high-temperature superconductors,
Rev. Mod. Phys. 66, 1125 (1994).
[16] U. K. Rößler, A. N. Bogdanov, and C. Pfleiderer, Spontaneous
Skyrmion ground states in magnetic metals, Nature 442, 797
(2006).
[17] S. Mühlbauer et al., Skyrmion lattice in a chiral magnet, Science
323, 915 (2009).
[18] N. Nagaosa and Y. Tokura, Topological properties and dynamics
of magnetic skyrmions, Nat. Nanotechnol. 8, 899 (2013).
[19] M. J. Stephen and J. P. Straley, Physics of liquid crystals, Rev.
Mod. Phys. 46, 617 (1974).
[20] G. P. Alexander et al., Colloquium: Disclination loops and defects in nematic liquid crystals, Rev. Mod. Phys. 84, 497 (2012).
[21] J. M. Kosterlitz and D. J. Thouless, Ordering, metastability and
phase transitions in two-dimensional systems, J. Phys. C: Solid
State Phys. 6, 1181 (1973).
[22] J. M. Kosterlitz, The critical properties of the two-dimensional
XY model, J. Phys. C: Solid State Phys. 7, 1046 (1974).
[23] J. M. Kosterlitz, Kosterlitz–Thouless physics: a review of key
issues, Rep. Prog. Phys. 79, 026001 (2016).
[24] F. Yang, Y. Shi, and L.-Q. Chen, Preformed cooper pairing and
the uncondensed normal-state component in phase-fluctuating
monolayer cuprate superconductivity, Phys. Rev. B 113, 104523
(2026).
[25] F. Yang and L. Q. Chen, Tractable framework for phase transitions in phase-fluctuating disordered two-dimensional super-

6
conductors: Applications to bilayer MoS2 and disordered InO 𝑥
thin films, Phys. Rev. B 113, 094517 (2026).
[26] F. Yang, G. D. Zhao, Y. Shi, and L. Q. Chen, Microscopic
phase-transition framework for gate-tunable superconductivity
in monolayer WTe2 , Phys. Rev. B 113, L100501 (2026).
[27] C. Paillard and B. Dkhil, Vibrational responses of polar
skyrmions, Nat. Phys. 21, 1877 (2025).
[28] S. Das, Z. Hong, V. A. Stoica, M. A. P. Gonçalves, Y. T.
Shao, E. Parsonnet, E. J. Marksz, S. Saremi, M. R. McCarter, A. Reynoso, C. J. Long, A. M. Hagerstrom, D. Meyers,
V. Ravi, B. Prasad, H. Zhou, Z. Zhang, H. Wen, F. Gómez-Ortiz,
P. Garcı́a-Fernández, J. Bokor, J. Íñiguez, J. W. Freeland, N. D.
Orloff, J. Junquera, L. Q. Chen, S. Salahuddin, D. A. Muller,
L. W. Martin, and R. Ramesh, Local negative permittivity and
topological phase transition in polar skyrmions, Nat. Mater. 20,
194 (2021).
[29] S. Wang, W. Li, C. Deng, Z. Hong, H.-B. Gao, X. Li, Y. Gu,
Q. Zheng, Y. Wu, P. G. Evans, J.-F. Li, C.-W. Nan, and Q. Li,
Giant electric field-induced second harmonic generation in polar
skyrmions, Nat. Commun. 15, 1374 (2024).
[30] F.-H. Gong, Y.-L. Tang, Y.-J. Wang, Y.-T. Chen, B. Wu, L.-X.
Yang, Y.-L. Zhu, and X.-L. Ma, Absence of critical thickness for
polar skyrmions with breaking the kittel’s law, Nat. Commun.
14, 3376 (2023).
[31] W. Li, S. Wang, P. Peng, H. Han, X. Wang, J. Ma, J. Luo, J.M. Liu, J.-F. Li, C.-W. Nan, and Q. Li, Terahertz excitation of
collective dynamics of polar skyrmions over a broad temperature
range, Nat. Phys. 21, 1965 (2025).
[32] J. Junquera et al., Topological phases in polar oxide nanostructures, Rev. Mod. Phys. 95, 025001 (2023).
[33] S. Das et al., Observation of room-temperature polar skyrmions,
Nature 568, 368 (2019).
[34] M. R. McCarter et al., Structural chirality of polar skyrmions
probed by resonant elastic x-ray scattering, Phys. Rev. Lett. 129,
247601 (2022).
[35] J. Ren, L. Liu, F. Sun, Q. He, M. Wu, W. Chen, and Y. Zheng,
Emergence and transformation of polar Skyrmion lattices via
flexoelectricity, npj Comput. Mater. 10, 216 (2024).
[36] W. R. Geng, Y. L. Zhu, M. X. Zhu, Y. L. Tang, H. J. Zhao,
C. H. Lei, Y. J. Wang, J. H. Wang, R. J. Jiang, S. Z. Liu, X. Y.
San, Y. P. Feng, M. J. Zou, and X. L. Ma, Dipolar wavevector
interference induces a polar Skyrmion lattice in strained BiFeO3
films, Nat. Nanotechnol. 20, 366 (2025).
[37] Z. Wang and L.-Q. Chen, Reversible phase transition between
vortex lattice and hexagonal polar Skyrmion crystals, Nano Lett.
23, 9907 (2023).
[38] Z. Wang and L.-Q. Chen, Tuning topology phases by controlling
effective screening and depolarization in oxide superlattices,
Nano Lett. 24, 5761 (2024).
[39] L.-Q. Chen, Phase-field method of phase transitions/domain
structures in ferroelectric thin films: A review, J. Am. Ceram.
Soc. 91, 1835 (2008).
[40] Y. L. Li et al., Effect of substrate constraint on the stability and
evolution of ferroelectric domain structures in thin films, Acta
Mater. 50, 395 (2002).
[41] Y. L. Li et al., Effect of electrical boundary conditions on ferroelectric domain structures in thin films, Appl. Phys. Lett. 81,
427 (2002).
[42] A. M. Ross and L.-Q. Chen, Thermodynamics and ferroelectric
properties of Pb1− 𝑥 Sr 𝑥 TiO3 solid solutions, Acta Mater. 261,
119405 (2023).
[43] L.-Q. Chen, Phase-field models for microstructure evolution,
Annu. Rev. Mater. Res. 32, 113 (2002).

[44] V. B. Shirokov, A. G. Razumnaya, and A. S. Mikheykin, Thermodynamic theory of Pb 𝑥 Sr1− 𝑥 TiO3 solid solutions, J. Phys.
Chem. Solids 161, 110395 (2022).
[45] X. Xing et al., Solid solution Pb1− 𝑥 Sr 𝑥 TiO3 and its thermal
expansion, J. Alloys Compd. 360, 286 (2003).
[46] L.-Q. Chen and J. Shen, Applications of semi-implicit fourierspectral method to phase-field equations, Comput. Phys. Commun. 108, 147 (1998).
[47] F. Xue et al., Phase-field simulations of ferroelectric domain
structures in PbZr 𝑥 Ti1− 𝑥 O3 bilayers, Acta Mater. 61, 2909
(2013).
[48] J. J. Wang et al., Phase transitions and domain structures of
ferroelectric nanoparticles: Phase-field model incorporating
strong elastic and dielectric inhomogeneity, Acta Mater. 61,
7591 (2013).
[49] P. Yudin et al., Ferroelectric phase transitions induced by a strain
gradient, Phys. Rev. Res. 3, 033213 (2021).
[50] T. Grieb et al., Determination of the chemical composition of
GaNAs using STEM HAADF imaging and STEM strain state
analysis, Ultramicroscopy 117, 15 (2012).
[51] M. Petit et al., Depth analysis of the in-plane lattice constants
in compressively strained La0.67 Ca0.33 MnO3 thin films, J. Appl.
Phys. 97, 093706 (2005).
[52] F. Yang and M. W. Wu, Theory of Higgs modes in d-wave
superconductors, Phys. Rev. B 102, 014511 (2020).
[53] R. Shimano and N. Tsuji, Higgs mode in superconductors, Annu.
Rev. Condens. Matter Phys. 11, 103 (2020).
[54] R. Matsunaga, Y. I. Hamada, K. Makise, Y. Uzawa, H. Terai,
Z. Wang, and R. Shimano, Higgs Amplitude Mode in the BCS
Superconductors Nb1− 𝑥 Ti 𝑥 N Induced by Terahertz Pulse Excitation, Phys. Rev. Lett. 111, 057002 (2013).
[55] R. Matsunaga, N. Tsuji, H. Fujita, A. Sugioka, K. Makise,
Y. Uzawa, H. Terai, Z. Wang, H. Aoki, and R. Shimano, Lightinduced collective pseudospin precession resonating with Higgs
mode in a superconductor, Science 345, 1145 (2014).
[56] F. Yang and M. W. Wu, Optical response of Higgs mode in
superconductors at clean limit: formulation through Eilenberger
equation and Ginzburg-Landau Lagrangian, J. Phys.: Condens.
Matter 36, 425701 (2024).
[57] F. Yang and M. W. Wu, Optical response of Higgs mode in
superconductors at clean limit, Ann. Phys. 453, 169312 (2023).
[58] P. Tang, R. Iguchi, K.-i. Uchida, and G. E. W. Bauer, Excitations
of the ferroelectric order, Phys. Rev. B 106, L081105 (2022).
[59] F. Yang and L. Chen, First-principles-inspired thermodynamic
framework linking the condensed ground state to displacive ferroelectric phase transitions, arXiv:2412.04308 (2024).
[60] M. J. Haun, E. Furman, S. Jang, H. McKinstry, and L. Cross,
Thermodynamic theory of PbTiO3 , J. Appl. Phys. 62, 3331
(1987).
[61] J. Remeika and A. Glass, The growth and ferroelectric properties
of high resistivity single crystals of lead titanate, Mater. Res.
Bull. 5, 37 (1970).
[62] S. Ikegami, I. Ueda, and T. Nagata, Electromechanical properties
of PbTiO3 ceramics containing La and Mn, J. Acoust. Soc. Am.
50, 1060 (1971).
[63] A. A. Bokov and Z.-G. Ye, Recent progress in relaxor ferroelectrics with perovskite structure, J. Mater. Sci. 41, 31 (2006).
[64] F. Yang, X. J. Li, D. Talbayev, and L. Q. Chen, Terahertzinduced second-harmonic generation in quantum paraelectrics:
Hot-phonon effect, Phys. Rev. Lett. 135, 056901 (2025).
[65] G. D. Zhao, F. Yang, and L. Q. Chen, Role of ferrons in the
heat capacity and thermal transport of displacive ferroelectrics,
Phys. Rev. B 112, 014115 (2025).


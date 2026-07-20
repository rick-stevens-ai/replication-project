# Extraction: marker.md (interim)

**Paper:** Thermally Configurable Multi-Order Polar Skyrmions in Multiferroic Oxide Superlattices
**Authors:** Kefan Liu, Yuhui Huang, Xiangwei Guo, Yongjun Wu, Juan Li, Zijian Hong (2026)
**Group:** Zhejiang University (Hong Zijian group).

> NOTE: `marker`/`nougat` neural extractors were not available in this offline runner.
> This file is an INTERIM extraction produced with `pdftotext -layout` (poppler),
> carrying an explicit header so downstream consumers know the provenance.
> Text body below is the raw pdftotext dump.

---

Thermally Configurable Multi-Order Polar Skyrmions in Multiferroic
Oxide Superlattices
Kefan Liu1, Yuhui Huang1, 2, Xiangwei Guo1, *, Yongjun Wu1, 2, 3, 4, *, Juan Li5, Zijian Hong1, 2, 3,
                                                 4, *




1
    State Key Laboratory of Silicon and Advanced Semiconductor Materials, School of
Materials Science and Engineering, Zhejiang University, Hangzhou, Zhejiang 310058, China.
2
    Zhejiang Key Laboratory of Advanced Solid State Energy Storage Technology and
Applications, Taizhou Institute of Zhejiang University, Taizhou, Zhejiang 318000, China.
3
    Institute of Fundamental and Transdisciplinary Research, Zhejiang University, Hangzhou
310058, China
4
    School of Engineering, Hangzhou City University, Hangzhou, Zhejiang 310015, China
5
    College of Materials Science and Engineering, Zhejiang University of Technology,

Hangzhou 310014, China.




Corresponding
*
                   authors:    l240441@zju.edu.cn       (XG);    yongjunwu@zju.edu.cn         (YW);
hongzijian100@zju.edu.cn (ZH)




                                                 1
Abstract
Polar topological textures in low-dimensional ferroelectrics have emerged as a versatile
platform for high-density information storage and neuromorphic computing. While low-order
topological states, such as vortices and skyrmions, have been extensively studied, high-order
polar topological families remain largely unexplored due to their higher energy requirements
and limited stabilization methods. Here, using a BiFeO3 (BFO)-based multiferroic superlattice
as a model system, we demonstrate a thermal-modulation strategy that stabilizes multi-order
polar skyrmions and enables reversible tuning of their topological order through phase-field
simulations. It was found that temperature modulation drives the system from polar solitons
through 1π-, 2π-, 3π-, and 4π-skyrmion states, with closed heating-cooling path analyses
revealing the widest thermal stability window for 2π-skyrmions (up to 600 K). Leveraging
this robustness, 2% Sm doping in BFO lowers the transition temperatures, enabling room-
temperature stabilization of 2π-skyrmions. These findings enrich the fundamental
understanding of multi-order polar topologies and establish a tunable strategy for realizing
variable-order topological configurations in practical memory devices.


Keywords: multiferroic superlattices, multi-order polar skyrmion, thermal-control strategy,
phase-field simulations, Sm doping




                                              2
1. Introduction
       Topologically protected polar textures, which are nanoscale ferroic objects, have
received growing attention due to their diverse physical properties and potential applications
in advanced information technologies. [1–4] These applications include beyond-CMOS devices,
racetrack memories, and neuromorphic computing systems. In recent years, various polar
topological textures have been identified in low-dimensional ferroelectric heterostructures,
such as polar flux closure, [5] vortices [6], merons [7], skyrmions [8], and Solomon rings [9], etc.
These polar topologies provide a versatile platform for observing unconventional physical
phenomena, resulting from the complex interactions between swirling polarization and
external stimuli. A wide range of emergent properties has been reported, i.e., negative
capacitance, [10,11] chirality, [12,13] ultrafast collective oscillations, [14] reversible inversion
symmetry, [15] and ultrahigh energy-storage density, [16] offering exciting opportunities for
fundamental physics research and the development of next-generation multifunctional
nanoelectronics.
       In addition to polar vortices, solitons, and skyrmions which have been widely observed,
research has now shifted toward discovering and manipulating multi-order skyrmions (kπ-
skyrmion, k = 1, 2, 3, ...) to expand the capacity of next-generation electronic applications.
Multi-order skyrmions exhibit concentric azimuthal rotations of in-plane polarization around
a central core, with their net topological charge Q alternating between ±1 (for odd values of k,
such as 1π- and 3π-) and 0 (for even values of k, such as 2π- and 4π-skyrmions) [17-21]. For
example, a doughnut-like polar high-order radial vortex, analogous to magnetic skyrmionium,
was recently observed in BiFeO3 (BFO) nanoislands through boundary condition engineering
   . This highlights both the feasibility of such structures and the current scarcity of related
[21]


studies. However, it should be noted that multi-order skyrmions are inherently more
challenging to stabilize and manipulate due to their larger spatial size and higher energetic
cost [22-25]. The limited progress in this area underscores the urgent need for new strategies to
explore, stabilize, and modulate multi-order polar topologies for future applications.
       Thermally driven topological transitions have emerged as exciting and promising
methods for manipulating polar topological states, allowing access to configurations that
traditional methods cannot achieve. The change of temperature can induce deterministic
switching between different textures by modulating the competition among temperature-
dependent Landau energy, elastic energy, electrostatic energy, and gradient energy. [26, 27]
Additionally, higher-order topologies are often higher-energy configurations which is often
difficult to form naturally [28]. Controlled thermal excitation can, in principle, provide the
                                                 3
necessary energy to overcome kinetic barriers and reveal otherwise inaccessible states.
However, a key challenge lies in identifying a carefully tuned temperature window that can
trigger topological transitions while remaining suitable for in-situ implementation. This would
enable reversible thermal switching between multi-order polar topological structures and
allow for precise control over their topological order.
     In this study, we employ a BFO-based multiferroic superlattice as the model system and
use a thermal control strategy to achieve stable multi-order polar skyrmion states. This
approach enables reversible topological transitions among these states, allowing for precise
control over their skyrmion order. By modulating temperature, we drive the system through
successive skyrmion states, transitioning from 1π to 4π configurations. Our analysis of
controlled heating and cooling paths demonstrates the reversibility of these multi-order
transformations. Additionally, we predict that doping with Samarium (Sm) effectively lowers
the transition temperatures and can even stabilize 2π skyrmions at room temperature for the
superlattice system. This research enhances our fundamental understanding of multi-order
polar topological states and establishes a pathway for realizing variable-order topological
configurations in multistate memory devices.


2. Results and discussion
2.1. Diverse polar topologies in multiferroics and thermal modulation framework
       The schematic diagrams illustrating various polar topologies, including vortices,
solitons, and kπ-skyrmions, are presented in Figure 1(a). Among them, the high order
skyrmions are usually high energy states that is difficult to stabilize at room temperature. In
this study, using phase-field simulations (details in Methods) we propose a thermally driven
modulation strategy to stabilize and manipulate the multi-order polar skyrmions. The
[(BiFeO3)7/(SrTiO3)4]8 superlattice (BFO/STO) grown on a (001)pc-LaAlO3 (LAO) substrate
is chosen as the model system (Figure 1b), which has shown to host solitons at room
temperature [29]. The spontaneous polarization state within the BFO layers is mainly
influenced by the following key factors: the epitaxial constraints, which arise from the
mechanical boundary conditions imposed by the LAO substrate; the depolarization field,
resulting from the electrical boundary conditions introduced by the dielectric STO layers
(Figure 1c); external heating, which affects the Landau energy landscape as the second-order
Landau coefficient is modeled as a temperature-dependent tensor (details of this parameter
can be found in Supplementary Table S1). [31–33] Further information about the simulation
methodology is available in Methods.

                                                4
Figure 1. Schematics of the topological polar textures and simulation setup. (a)
Representative polar textures characterized by different topological charge Q: polar vortex
with Q=0, polar soliton with Q=1 and multi-order polar skyrmions with Q=0 or 1 (including
1π-, 2π-, 3π- and 4π-skyrmions). (b) Schematic of the phase-field simulation setup for the
BFO7/STO4 superlattices. (c) Atomic schematic of the boundary conditions applied in the
BFO/STO superlattices and influence of thermal field.

2.2. Thermally induced multi-order polar skyrmions in BFO/STO superlattices
    The temperature-induced evolution of polar textures in the BFO/STO superlattices
simulated by the phase-field simulations is presented in Figure 2. At room temperature (300
K), the system exhibits spatially dispersed solitons with a size of ~10 nm (Figure 2a) and a
topological charge of 1 (calculated by integrating the local Pontryain density, Figure 2b),
characterized by a bimeron-type texture with a converging in-plane polarization distribution
(Figure 2c). The sparse distribution of soliton units gives rise to a relatively low-density
topological phase. Upon heating to 600 K, a clear phase transition occurs wherein the polar
solitons evolve into compact, regularly arranged low-order 1π-skyrmions (Figure 2d,e). This
transformation is accompanied by the disappearance of bimeron structures and the emergence
of symmetric skyrmionic textures (Figure 2f). Compared to the ~20 u.c.-wide polar solitons,
the thermally stabilized 1π-skyrmions exhibit a reduced diameter of ~10 u.c. (Figure 2g,h),
enabling a denser packing of topological units. Despite their smaller size, both topological
states share a common polarization texture, featuring a downward-oriented core encircled by
upward-pointing polarization, and a topological charge of Q = −1. This thermally driven polar
soliton-to-1π-skyrmion transition consequently leads to a progressive increase in the total

                                             5
planar topological charge by 153% (Figure 2i), reflecting that thermal excitation can further
enhance the potential information storage density to ~1.03 × 1013 bit/in2.




Figure 2. The topological polar soliton at room temperature and emergent 1π-skyrmion
under low thermal fields. (a, b) Planar view of the out-of-plane polarization magnitude and
the corresponding Pontryagin density distribution of BFO layer at 300K, showing the
stabilization of polar soliton at the room temperature. (c) Magnified view of the polar soliton
overlaid with the in-plane polar vector. (d, e) Planar view of the out-of-plane polarization
magnitude and the corresponding Pontryagin density distribution of BFO layer at 600K,
showing the formation of polar 1π-skyrmion under low thermal field. (f) Magnified view of
the polar 1π-skyrmion overlaid with the in-plane polar vector. (g, h) Magnified view of the
out-of-plane polarization distribution on a single soliton and 1π-skyrmion with red line profile
overlaid. (i) Temperature dependence of the total topological charge of BFO layer during the
transition from polar soliton to 1π-skyrmion induced by low thermal fields.

     Interestingly, thermal excitation is further demonstrated to be effective in increasing the
topological order of skyrmions under higher temperatures (Figure 3). At 800 K, a
labyrinthine-type polar texture emerges in the system (Figure 3a), giving rise to a concentric
nested skyrmion structure with opposing topological charges as revealed by Pontryagin
density calculations (Figure 3b). Analysis of a single topological unit confirms a divergent
polarization pattern (Q = +1) in the center and a convergent pattern (Q = −1) in the periphery,
resulting in a net topological charge of zero (Figure 3c). Upon further heating to 1000 K, a
clear labyrinth-to-bubble transition occurs, marked by the emergence of well-defined domain
walls separating topological units (Figure 3d). Pontryagin density analysis identifies three


                                               6
concentric topological layers (Figure 3e), with an additional outer ring exhibiting a divergent
polarization configuration, thereby increasing the net topological charge to +1 (Figure 3f).




Figure 3. Thermal driven phase transitions and temperature phase diagram for the
BFO-based superlattice. (a, b) Planar view of the out-of-plane polarization magnitude and
the corresponding Pontryagin density distribution of BFO layer at 800K, showing the
formation of mixed polar 1π-skyrmion and 2π-skyrmion under medium thermal fields. (c)
Magnified view of the 2π-skyrmion overlaid with the in-plane polar vector. (d, e) Planar view
of the out-of-plane polarization magnitude and the corresponding Pontryagin density
distribution of BFO layer at 1000K, showing the formation of mixed polar 2π-skyrmion and
3π-skyrmion under medium thermal fields. (f) Magnified view of the polar 3π-skyrmion
overlaid with the in-plane polar vector. (g, h) Magnified view of the out-of-plane polarization
distribution on a single 2π-skyrmion and 3π-skyrmion with red line profile overlaid. (i)
Temperature dependence of the total topological charge of BFO layer when the 2π-skyrmion
and 3π-skyrmion were formed under medium thermal fields. (j) The topological temperature
phase diagram with the order evolution of polar skyrmion.

     The multi-order nature of these polar textures is further confirmed by analyzing the
azimuthal rotation of out-of-plane polarization. At 600 K, a 2π rotation of the polarization is
                                              7
observed from the core to the outer region, corresponding to 2π-skyrmions (Figure 3g).
While under a higher temperature of 1000 K, the polarization rotation extends to 3π,
indicating the formation of 3π-skyrmions (Figure 3h). The larger diameter of 3π-skyrmions
(~32 u.c.) compared to 2π ones (~24 u.c.) reduces their areal density, leading to a slight
decrease in the overall topological charge (Figure 3i). This trend becomes more pronounced
as the proportion of 3π-skyrmions increases. At 1400 K, the system evolves into four-layer
nested textures, identified as 4π-skyrmions with zero net topological charge (Q = 0;
Supplementary Figure S1a-c), accompanied by a further decline in total topological charge.
A temperature-dependent topological order transition phase diagram was constructed for this
process (Figure 3j). The system exhibits mixed-phase regions between 700-1400 K, where
only two adjacent skyrmion orders (e.g., 1π and 2π) can coexist. The vortex-array phase is
confined to a narrow window near the onset of the paraelectric transition.
2.3. Reversible thermal modulation of multi-order polar skyrmions
     The above results demonstrate that heating effectively tunes the topological order of
polar skyrmions. A key question for practical applications, however, is whether these multi-
order topological states are thermally reversible upon cooling, and how robust their
topological protection is under temperature cycling. To address this, we simulated cooling
pathways by reversing the temperature sequence used during heating (Figure 4a-d,f).
Remarkably, as the system cooled to 1000 K, 800 K, and 300 K, the corresponding 3π-
skyrmions, 2π-skyrmions, and solitons were recovered in sequence, indicating an overall
reversible evolution with only minor thermal hysteresis. However, at 600 K, a deviation from
the heating path was observed: instead of 1π-skyrmions, 2π-skyrmions reappeared (Figure
4e). This behavior was reproduced across different cooling trajectories (Supplementary
Figure S2), suggesting enhanced topological protection of 2π-skyrmions, which suppresses
the reformation of the 1π-state. To test this further, reheating experiments were conducted
(Supplementary Figure S3). When the system was first cooled to 400 K and then reheated to
600 K, it transitioned directly from solitons to 2π-skyrmions, bypassing the 1π-state. Only
when cooled to 300 K and reheated to 600 K did the 1π-skyrmions re-emerge, confirming that
the reappearance of the 1π-state depends sensitively on the cooling depth and path.




                                               8
Figure 4. Reversibility of multi-order polar topological structures during thermal
modulation. (a-f) Planar views of the out-of-plane polarization magnitude at different cooling
stages: (a) 1400 K, (b) after cooling to 1000 K, (c) 800 K, (d) 600 K, (e) 500 K, and (f) 300 K.
The evolution illustrates the transformation of multi-π polar textures, including their partial
retention or decay into lower-order structures or solitons. (g) Schematic illustration of the
temperature-driven transition pathways of multi-order polar topological phases, highlighting
the reversibility and stability of distinct configurations.

2.4. Chemical doping-assisted stabilization of room-temperature multi-order skyrmions
     Although thermal excitation can effectively induce multi-order skyrmions, the
volatilization of Bi2O3 at elevated temperatures poses challenges for high temperature
applications.[34–38] The wide thermal stability range of 2π-skyrmions, as reported above,
nevertheless offers a promising alternative. To this end, we developed a strategy combining
chemical doping, i.e., via Sm3+ doping in BFO (BSFO), with thermal pathways to stabilize
2π-skyrmions at room temperature (Figure 5). Sm doping could insert a chemical pressure
that lowers both the Curie temperature and lattice constants, providing similar effect as
thermal field (Figure 5a).[31–33] We first examined doping-induced topological transitions at
room temperature by varying Sm content from 2% to 16% (Supplementary Figure S4).
Increasing Sm concentration led to reduced topological unit size and increased density,
yielding a transition from solitons to 1π-skyrmions. A Sm content-temperature phase diagram
was constructed (Figure 5b). The phase diagram indicates that as Sm concentration increases,
kπ-skyrmions emerge at lower temperatures. However, as the Sm concentration increases,
multi-order skyrmions gradually annihilate from higher to lower order. This is because the

                                               9
formation of multi-order skyrmions requires a larger initial volume of topological units. Sm
doping reduces the size of topological units, thereby limiting the nucleation of multi-order
skyrmions. It identifies an elliptical “2π-zone” where stable room-temperature 2π-skyrmions
can form, particularly at 2% and 4% Sm concentrations. Further heating studies showed that
only samples with ≤4% Sm content exhibited multi-order skyrmions (Supplementary Figure
S5-S8), as the smaller topological units promoted by higher doping hinder the nucleation of
complex structures.
     Guided by this phase space, we applied the previously established thermal cycling
protocol (Figure 5c-e). Comparative analysis of heating and cooling cycles for 2% and 4%
Sm-doped samples (Supplementary Figure S9-S10) revealed that both could stabilize 2π-
skyrmions at room temperature, though with different thermal requirements. Specifically, 4%
Sm-doped BSFO required heating to 800 K, whereas 2% Sm-doped BSFO achieved similar
skyrmion density at 600 K, an advantage for material integrity. Post-cooling observations
showed that 2π-skyrmions evolved morphologically, with smoother peripheries and a shape
transition from elliptical to bubble-like configurations (Figure 5d,e). Based on these findings,
we propose an optimized protocol for room-temperature 2π-skyrmion generation (Figure 5f):
(1) using 2% Sm-doped BFO, (2) thermal activation at 600 K, and (3) controlled cooling to
room temperature. This three-step method reliably stabilizes 2π-skyrmions at operational
conditions while minimizing thermal degradation.




                                              10
Figure 5. Chemical doping combined with thermal path enables room-temperature
stabilization of multi-order polar skyrmions. (a) Schematic of the Sm-doping mechanism
in BFO and simulation setup, illustrating the competition between Curie temperature
modulation and epitaxial strain. (b) Sm concentration and temperature topological phase
diagram. (c-e) Planar views of out-of-plane polarization magnitude overlaid with in-plane
polarization vectors for 2% Sm doping at (c) 300 K, (d) 600 K, and (e) after cooling from
600 K to 300 K, revealing the thermal-path-dependent stabilization of 2π-skyrmions. (f)
Schematic of room-temperature 2π-skyrmions enabled by Sm doping and controlled thermal
evolution.


3. Conclusion and outlook
     In summary, our phase-field simulations on BFO-based multiferroic superlattices
demonstrate that thermal modulation offers an effective route to stabilize and control multi-
order polar skyrmions. The system undergoes a sequential evolution from solitons to 1π-4π
skyrmion states upon heating. Interestingly, it is noted that during the transition from solitons
to 1π-skyrmions at 650 K, the density of topological units in the system increases by 153%,
achieving an information storage density of 1.03 × 1013 bit/in2. The closed heating-cooling
path analyses confirm reversible order switching of low- and high-order polar skyrmions, with
2π-skyrmions displaying the widest thermal stability window (up to 600 K). Furthermore, 2%
Sm doping in BFO lowers the transition temperatures and, as evidenced by the Sm
concentration-temperature phase diagram, defines an optimal regime for dense 2π-skyrmion
                                           11
formation, enabling their robust stabilization at room temperature. These findings not only
highlight the power of thermal-control engineering as an effective strategy for constructing
multi-order polar skyrmions in oxide superlattices but also enable customized doping
protocols for multi-state memory systems, allowing precise stabilization of target polar
topological states within specific operational temperature ranges.


4. Experimental Section
Phase-field modeling of the BFO/STO superlattices
     Phase-field simulations are conducted to determine the equilibrium polarization
configurations of the (BFO7/STO4)8 superlattice epitaxially grown on LAO-(001)pc, by
numerically solving the time-dependent Ginzburg-Landau equation:[39–41]
                                            ��      �� �
                                               =− �                                                  (1)
                                            ��       ��
where t, L, � represent the evolution time step, the kinetic coefficient, and the order parameter,
respectively. In this model, two feature vectors serve as order parameters: the spontaneous
polarization vector (�), and the oxygen octahedral tilt vector (�). The total free energy F is
given by the volume integration of Landau (����� ), elastic (����� ), electrostatic (����� ), and
gradient energy densities (����� ), which can be expressed by:

          � �, � =         ����� �, � + ����� �, �, � + ����� �, � + ����� �, � ��                   (2)

The Landau energy density is calculated using a fourth-order polynomial expansion:
      ����� �, � = ��� �� �� + ����� �� �� ���� ++ ��� �� �� + ����� �� �� ���� + ����� ���� �� ��   (3)
where the ��� , ����� , ��� , ����� , and ����� are the Landau, oxygen octahedral tilt, and their
coupling coefficients, respectively. The elastic energy density can be expressed as:
                            ����� �, �, � = ����� ��� − �0�� ��� − �0��                              (4)
where the ����� is the elastic stiffness coefficient tensor, and ��� is the is the epitaxial strain
applied to the substrate. The eigen strain �0�� is coupled to the spontaneous polarization and the
oxygen octahedral tilt through:
                                     �0�� = ℎ���� �� �� + ����� ����                                 (5)
where the ℎ���� and ����� are the electrostriction coefficient tensor. The ��� can be determined
by solving the elastic equilibrium equation (���,� = 0). The pseudocubic lattice parameters for
BFO and STO are taken as 3.965 Å and 3.905 Å, respectively, for the lattice mismatch
calculation. The elastic boundary conditions are defined such that the out-of-plane stress at

                                                  12
the thin film surface vanishes, while the displacement at the substrate base far from the thin
film is constrained to zero. The electric energy density can be performed as:
                                            1
                               ����� �, � =− ���� − ��� �0 �� ��                              (6)
                                            2
where the ��� is the background dielectric constant, and the �0 is the vacuum dielectric
constant. The calculation employs the electric equilibrium equation (���,� = 0), assuming that
the equilibrium speed of the electric field is much faster than the domain evolution. The local
electric field �� can be calculated by �� =− ∇� � . The electric boundary conditions are set
where the electric potential � is zero at both the film-substrate interface and the top surface of
the film. The gradient energy density can be calculated as:
                           ����� �, � = ����� ∇� �� ∇� �� + ����� ∇� �� ∇� ��                 (7)
where the ����� and ����� are the polar and rotation gradient coefficient, respectively.
     A three-dimensional computational domain was discretized using a mesh of 200 × 200 ×
150 grids, with a uniform grid spacing of 0.4 nm. Along the out-of-plane direction, the grid
distribution was allocated as follows: 30 grids for the substrate, 87 grids for the superlattice,
and 33 grids for the air layer. To simulate initial polarization nucleation, random noise with a
small amplitude (<0.0001 μC·cm⁻²) was introduced into the system. The temperature was
uniformly applied to the entire system. For the heating process, we used the room-temperature
results as initial configurations for the heating simulations to ensure consistency with actual
experiments.
Topological density calculation
     The topological charge is characterized by integrating the Pontryagin density (q) of thin
film horizontal cross-sectional slices, calculated by:[7]
                                               1     �� ��
                      �=       � ���� =          �∙(   ×   ) ����                             (8)
                                              4�     �� ��
Sm doping of BFO layer
     To account for the Sm doping effects, modifications were applied to the second-order
Landau coefficients:[31]
                              �11 = �0 � − �� �       = �0 � − (�� − ���)                     (9)
                              �11 = �0 � − �� �        = �0 � − (�� − ���)                  (10)
where α11 and β11 represent the modified Landau coefficients for polarization and oxygen
octahedral rotation, respectively. Tc denotes the Curie temperature. α0, β0, cp, and cq are
material-specific constants (see Supplementary Table S1 for complete parameter values).
The x means the content of doped Sm.
                                                 13
     Additionally, the compressive strain in the superlattice decreases with increasing Sm
content. The epitaxial strain in the superlattice is modified with Sm content according to the
following equation:
                                                         �� − �� �
                                     �11 � = �22 � =                                      (11)
                                                             ��
where �� and �� represent the lattice constant of the substrate and film, respectively. Here we
treat both the substrate and thin film as pseudocubic structures. The details of Sm doping-
induced variations in BSFO lattice constants are shown in Supplementary Figure S11.[33]


Acknowledgements
Z. H. and K. L. are grateful for the technical support for Nano-X from Suzhou Institute of
Nano-Tech and Nano-Bionics, Chinese Academy of Sciences (SINANO). The financial
supports from the National Natural Science Foundation of China (Nos. 92166104, 92463306,
12174328, ZH), the Joint Funds of the National Natural Science Foundation of China (No.
U21A2067, YW), and the Natural Science Foundation of Zhejiang Province (No.
LR25E020003, ZH; No. LD24E020003, YW) are acknowledged. X.G. is supported by the
National Natural Science Foundation of China (No. 52202151) and China Postdoctoral
Science Foundation (No. 2022M722715). YW is also supported by the Special Support Plan
for High Level Talents in Zhejiang Province (No. 2023R5231).
Conflict of Interest
The authors declare no competing interests.
Data Availability Statement
All data used are available within this manuscript and Supplementary Information. Further
information can be acquired from the corresponding authors upon reasonable request.
Code Availability Statement
The phase-field simulation was performed with the Mu-PRO software package
(https://muprosoftware.com).
Author contributions
Kefan Liu: Conceptualization, Data curation, Formal analysis, Visualization, Writing–original

draft, Writing–review and editing.

Yuhui Huang: Writing–review and editing, Validation, Supervision.

Yongjun Wu: Writing – original draft, Writing – review and editing, Supervision, Funding
acquisition, Resources.

                                              14
Xiangwei Guo: Conceptualization, Methodology, Software, Writing–review and editing.

Juan Li: Funding acquisition, Resources, Writing–review and editing.

Zijian Hong: Conceptualization, Writing–original draft, Writing–review and editing, Formal
analysis, Funding acquisition, Resources, Software, Validation .




Supporting Information
Supporting Information is available from the corresponding author (ZH).


                                            Received: ((will be filled in by the editorial staff))
                                             Revised: ((will be filled in by the editorial staff))
                                    Published online: ((will be filled in by the editorial staff))




                                             15
References
[1]   J. Junquera, Y. Nahas, S. Prokhorenko, L. Bellaiche, J. Íñiguez, D. G. Schlom, L.-Q.
      Chen, S. Salahuddin, D. A. Muller, L. W. Martin, R. Ramesh, Rev. Mod. Phys. 2023,
      95, 025001.
[2]   I. A. Lukyanchuk, A. G. Razumnaya, S. Kondovych, Y. A. Tikhonov, B. Khesin, V. M.
      Vinokur, Phys. Rep. 2025, 1110, 1.
[3]   X. Guo, L. Zhou, B. Roul, Y. Wu, Y. Huang, S. Das, Z. Hong, Small Methods 2022, 6,
      2200486.
[4]   V. Govinden, S. Prokhorenko, Q. Zhang, S. Rijal, Y. Nahas, L. Bellaiche, N. Valanoor,
      Nat. Mater. 2023, 22, 553.
[5]   Y. L. Tang, Y. L. Zhu, X. L. Ma, A. Y. Borisevich, A. N. Morozovska, E. A. Eliseev,
      W. Y. Wang, Y. J. Wang, Y. B. Xu, Z. D. Zhang, S. J. Pennycook, Science 2015, 348,
      547.
[6]   A. K. Yadav, C. T. Nelson, S. L. Hsu, Z. Hong, J. D. Clarkson, C. M. Schlepuëtz, A. R.
      Damodaran, P. Shafer, E. Arenholz, L. R. Dedon, D. Chen, A. Vishwanath, A. M.
      Minor, L. Q. Chen, J. F. Scott, L. W. Martin, R. Ramesh, Nature 2016, 530, 198.
[7]   Y. J. Wang, Y. P. Feng, Y. L. Zhu, Y. L. Tang, L. X. Yang, M. J. Zou, W. R. Geng, M.
      J. Han, X. W. Guo, B. Wu, X. L. Ma, Nat. Mater. 2020, 19, 881.
[8]   W. R. Geng, Y. L. Zhu, M. X. Zhu, Y. L. Tang, H. J. Zhao, C. H. Lei, Y. J. Wang, J. H.
      Wang, R. J. Jiang, S. Z. Liu, X. Y. San, Y. P. Feng, M. J. Zou, X. L. Ma, Nat.
      Nanotechnol. 2025, 20, 366.
[9]   J. Wang, D. Liang, J. Ma, Y. Fan, J. Ma, H. M. Jafri, H. Yang, Q. Zhang, Y. Wang, C.
      Guo, S. Dong, D. Liu, X. Wang, J. Hong, N. Zhang, L. Gu, D. Yi, J. Zhang, Y. Lin, L.
      Q. Chen, H. Huang, C. W. Nan, Nat. Commun. 2023, 14, 3941.
[10] A. K. Yadav, K. X. Nguyen, Z. Hong, P. García-Fernández, P. Aguado-Puente, C. T.
      Nelson, S. Das, B. Prasad, D. Kwon, S. Cheema, A. I. Khan, C. Hu, J. Íñiguez, J.
      Junquera, L. Q. Chen, D. A. Muller, R. Ramesh, S. Salahuddin, Nature 2019, 565, 468.
[11] S. Das, Z. Hong, V. A. Stoica, M. A. P. Gonçalves, Y. T. Shao, E. Parsonnet, E. J.
      Marksz, S. Saremi, M. R. McCarter, A. Reynoso, C. J. Long, A. M. Hagerstrom, D.
      Meyers, V. Ravi, B. Prasad, H. Zhou, Z. Zhang, H. Wen, F. Gómez-Ortiz, P. García-
      Fernández, J. Bokor, J. Íñiguez, J. W. Freeland, N. D. Orloff, J. Junquera, L. Q. Chen,
      S. Salahuddin, D. A. Muller, L. W. Martin, R. Ramesh, Nat. Mater. 2021, 20, 194.




                                            16
[12] P. Shafer, P. García-Fernández, P. Aguado-Puente, A. R. Damodaran, A. K. Yadav, C.
       T. Nelson, S. L. Hsu, J. C. Wojdeł, J. Iñiguez, L. W. Martin, E. Arenholz, J. Junquera,
       R. Ramesh, Proc. Natl. Acad. Sci. U. S. A. 2018, 115, 915.
[13] Y. T. Shao, S. Das, Z. Hong, R. Xu, S. Chandrika, F. Gómez-Ortiz, P. García-
       Fernández, L. Q. Chen, H. Y. Hwang, J. Junquera, L. W. Martin, R. Ramesh, D. A.
       Muller, Nat. Commun. 2023, 14, 1355.
[14] Q. Li, V. A. Stoica, M. Paściak, Y. Zhu, Y. Yuan, T. Yang, M. R. McCarter, S. Das, A.
       K. Yadav, S. Park, C. Dai, H. J. Lee, Y. Ahn, S. D. Marks, S. Yu, C. Kadlec, T. Sato,
       M. C. Hoffmann, M. Chollet, M. E. Kozina, S. Nelson, D. Zhu, D. A. Walko, A. M.
       Lindenberg, P. G. Evans, L. Q. Chen, R. Ramesh, L. W. Martin, V. Gopalan, J. W.
       Freeland, J. Hlinka, H. Wen, Nature 2021, 592, 376.
[15] L. Caretta, Y. T. Shao, J. Yu, A. B. Mei, B. F. Grosso, C. Dai, P. Behera, D. Lee, M.
       McCarter, E. Parsonnet, K. P. Harikrishnan, F. Xue, X. Guo, E. S. Barnard, S.
       Ganschow, Z. Hong, A. Raja, L. W. Martin, L. Q. Chen, M. Fiebig, K. Lai, N. A.
       Spaldin, D. A. Muller, D. G. Schlom, R. Ramesh, Nat. Mater. 2023, 22, 207.
[16] Y. Liu, J. Liu, H. Pan, X. Cheng, Z. Hong, B. Xu, L. Q. Chen, C. W. Nan, Y. H. Lin,
       Adv. Mater. 2022, 34, 2108772.
[17] M. Shen, Y. Zhang, J. Ou-Yang, X. Yang, L. You, Appl. Phys. Lett. 2018, 112, 062403.
[18] S. Komineas, N. Papanicolaou, Phys. Rev. B 2015, 92, 174405.
[19] X. Zhang, J. Xia, Y. Zhou, D. Wang, X. Liu, W. Zhao, M. Ezawa, Phys. Rev. B 2016,
       94, 094420.
[20] A. G. Kolesnikov, M. E. Stebliy, A. S. Samardak, A. V. Ognev, Sci. Rep. 2018, 8,
       16966.
[21]   W. R. Geng, X. Guo, Y. L. Zhu, D. Ma, Y. L. Tang, Y. J. Wang, Y. Wu, Z. Hong, X. L.
       Ma, Nat. Commun. 2025, 16, 2804.
[22]   D. Foster, C. Kind, P. J. Ackerman, J. S. B. Tai, M. R. Dennis, I. I. Smalyukh, Nat.
       Phys. 2019, 15, 655.
[23]   J. Jiang, Y. Wu, L. Kong, Y. Zhang, S. Qiu, H. Zhang, Y. Ke, S. Wang, M. Tian, J.
       Tang, Nano Lett. 2025, 25, 3282.
[24]   J. Seidel, Nat. Mater. 2019, 18, 188.
[25]   S. Yang, Y. Zhao, K. Wu, Z. Chu, X. Xu, X. Li, J. Åkerman, Y. Zhou, Nat. Commun.
       2023, 14, 3406.
[26] P. Tong, L. Zhou, K. Du, M. Zhang, Y. Sun, T. Sun, Y. Wu, Y. Liu, H. Guo, Z. Hong,
       Y. Xie, H. Tian, Z. Zhang, Nat. Phys. 2025, 21, 464.

                                               17
[27] Z. Wang, M. Guo, H. A. Zhou, L. Zhao, T. Xu, R. Tomasello, H. Bai, Y. Dong, S. G.
      Je, W. Chao, H. S. Han, S. Lee, K. S. Lee, Y. Yao, W. Han, C. Song, H. Wu, M.
      Carpentieri, G. Finocchio, M. Y. Im, S. Z. Lin, W. Jiang, Nat. Electron. 2020, 3, 672.
[28] X. Guo, M. M. Seyfouri, K. Liu, P. Tong, Y. Huang, D. Sando, H. Tian, Y. Wu, N.
      Valanoor, Z. Hong, Nanoscale 2025, 17, 14348.
[29] V. Govinden, P. Tong, X. Guo, Q. Zhang, S. Mantri, M. M. Seyfouri, S. Prokhorenko,
      Y. Nahas, Y. Wu, L. Bellaiche, T. Sun, H. Tian, Z. Hong, N. Valanoor, D. Sando, Nat.
      Commun. 2023, 14, 4178.
[30] J. Tang, Y. Wu, W. Wang, L. Kong, B. Lv, W. Wei, J. Zang, M. Tian, H. Du, Nat.
      Nanotechnol. 2021, 16, 1086.
[31] F. Xue, L. Liang, Y. Gu, I. Takeuchi, S. V. Kalinin, L. Q. Chen, Appl. Phys. Lett. 2015,
      106, 012903.
[32] Z. Liao, F. Xue, W. Sun, D. Song, Q. Zhang, J. F. Li, L. Q. Chen, J. Zhu, Phys. Rev. B
      2017, 95, 214101.
[33] D. V. Karpinsky, A. Pakalniškis, G. Niaura, D. V. Zhaludkevich, A. L. Zhaludkevich,
      S. I. Latushka, M. Silibin, M. Serdechnova, V. M. Garamus, A. Lukowiak, W. Stręk, M.
      Kaya, R. Skaudžius, A. Kareiva, Ceram. Int. 2021, 47, 5399.
[34] Y. Nahas, S. Prokhorenko, J. Fischer, B. Xu, C. Carrétéro, S. Prosandeev, M. Bibes, S.
      Fusil, B. Dkhil, V. Garcia, L. Bellaiche, Nature 2020, 577, 47.
[35] A. B. Mei, Y. Tang, J. Schubert, D. Jena, H. Xing, D. C. Ralph, D. G. Schlom, APL
      Mater. 2019, 7, 071101.
[36] A. B. Mei, S. Saremi, L. Miao, M. Barone, Y. Tang, C. Zeledon, J. Schubert, D. C.
      Ralph, L. W. Martin, D. G. Schlom, APL Mater. 2019, 7, 111101.
[37] J. H. Haeni, C. D. Theis, D. G. Schlom, J. Electroceramics 2000, 4, 385.
[38] J. F. Ihlefeld, W. Tian, Z. K. Liu, W. A. Doolittle, M. Bernhagen, P. Reiche, R. Uecker,
      R. Rramesh, D. G. Schlom, IEEE Trans. Ultrason. Ferroelectr. Freq. Control 2009, 56,
      1528.
[39] Z. Hong, J. Britson, J. M. Hu, L. Q. Chen, Acta Mater. 2014, 73, 75.
[40] L. Q. Chen, J. Am. Ceram. Soc. 2008, 91, 1835.
[41] Y. L. Li, S. Y. Hu, Z. K. Liu, L. Q. Chen, Appl. Phys. Lett. 2002, 81, 427.




                                             18
TOC figure




   19

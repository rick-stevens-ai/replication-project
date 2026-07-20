# Extraction (marker interim) — Yuan & Chen 2023

**Paper:** Hexagonal Close-packed Skyrmion Lattice in Ultrathin Ferroelectric PbTiO3 Films
**Authors:** S. Yuan, Z. Chen (corresp.), S. Prokhorenko, Y. Nahas, L. Bellaiche, C. Liu, B. Xu, L. Chen, S. Das, L. W. Martin
**Method:** phase-field (Landau-Ginzburg-Devonshire) simulation of polar textures

> NOTE: `marker`/`nougat` neural OCR was not available in this environment.
> This is a faithful text extraction produced with `pdftotext -layout` as an
> interim stand-in, with a marker-style header prepended. Full extracted text
> follows below (source of truth = work/pdftotext_layout.txt).

---

      Hexagonal Close-packed Skyrmion Lattice in Ultrathin
                  Ferroelectric PbTiO3 Films

                            Shuai Yuan and Zuhuang Chen*
  School of Materials Science and Engineering, Harbin Institute of Technology, Shenzhen
  518055, China and Flexible Printed Electronics Technology Center, Harbin Institute of
                           Technology, Shenzhen 518055, China


              Sergei Prokhorenko, Yousra Nahas and Laurent Bellaiche
Physics Department and Institute for Nanoscience and Engineering, University of Arkansas,
                              Fayetteville, AR 72701, USA


                                      Chenhan Liu
Micro- and Nano-scale Thermal Measurement and Thermal Management Laboratory, School
of Energy and Mechanical Engineering, Nanjing Normal University, Nanjing, 210046, P. R.
                                        China


                                         Bin Xu
Institute of Theoretical and Applied Physics and School of Physical Science and Technology,
                     Soochow University, Suzhou, Jiangsu 215006, China


                                       Lang Chen
 Department of Physics, Southern University of Science and Technology, Shenzhen, 518055,
                                          China


                                        Sujit Das
     Materials Research Centre, Indian Institute of Science, Bangalore, 560012, India


                                     Lane W. Martin
   Department of Materials Science and Engineering, University of California, Berkeley,
   California 94720, USA and Materials Sciences Division, Lawrence Berkeley National
                      Laboratory, Berkeley, California 94720, USA


                             *Email: zuhuang@hit.edu.cn




                                            1
Abstract:

Polar skyrmions are topologically stable, swirling polarization textures with particle-

like characteristics, which hold promise for next-generation, nanoscale logic and

memory. While understanding of how to create ordered polar skyrmion lattice

structures and how such structure respond to applied electric fields, temperature, and

film thickness remains elusive. Here, using phase-field simulations, the evolution of

polar topology and the emergence of a phase transition to a hexagonal close-packed

skyrmion lattice is explored through the construction of a temperature-electric field

phase diagram for ultrathin ferroelectric PbTiO3 films. The hexagonal-lattice skyrmion

crystal can be stabilized under application of an external, out-of-plane electric field

which carefully adjusts the delicate interplay of elastic, electrostatic, and gradient

energies. In addition, the lattice constants of the polar skyrmion crystals are found to

increase with film thickness, consistent with expectation from Kittel’s law. Our studies

pave the way for the development of novel ordered condensed matter phases assembled

from topological polar textures and related emergent properties in nanoscale

ferroelectrics.




                                           2
     The topological phases, as defined by its topological invariants, is the new state of

matter that has only recently been recognized. Within this field, the topological domain

structures in ferroic materials have been known as a source of exotic phenomena [1-

10]. Among them, magnetic skyrmions have been extensively studied in recent years

for potential applications in low-power and high-efficiency spintronic devices including

memories, logic gates, etc.[11-15]. Skyrmion crystals (SkX), or periodic, lattice-like

organizations of skyrmions, in analogy to the vortex phase of type-II superconductors,

have been theoretically predicted and experimentally confirmed in several different

classes of magnetic materials [16-28]. In contrast to their magnetic counterparts,

however, polar skyrmions in ferroelectrics are much less explored [29-32]. Thanks to

recent advances in theoretical calculations, synthesis of high-quality thin films, and

characterization techniques, polar skyrmions have been observed very recently in

[PbTiO3 (PTO)]n/[SrTiO3 (STO)]n superlattices [33], where exotic emergent properties

such as negative permittivity and chirality have been observed [34,35]. Understanding

of the evolution of these exotic dipolar textures with temperature T and electric field E

(i.e., the T-E phase diagram) remains elusive but is important if researchers want to

manipulate these objects for practical use. Even more fundamental and still not

demonstrated is if one can actually realize a SkX based on these polar textures in

ferroelectrics [30]. It is conceivable that a close-packed polar SkX could be achieved by

further controlling the balance between the charge and lattice degrees of freedom (i.e.,

electrostatic and elastic boundary conditions); something that would promote additional

detail study of these emergent features and their possible collective behaviors [36].

                                            3
Thus, there is strong motivation to study the T-E phase diagram and to explore the

formation conditions and phase transition mechanisms for polar SkX in ferroelectric

materials.

       Given the fact that most SkX in ferromagnets are stabilized by an external magnetic

field, this begs the question as to whether a similar phenomenon could also occur in

ferroelectric films under electric fields. Here, phase-field simulations are used to

produce a T-E phase diagram of polar structures and to explore the possible existence

of polar SkX in thin films of the prototypical ferroelectric PTO. The simulations reveal

that a hexagonal polar SkX phase can be induced in a narrow region below the Curie

temperature of PTO on the phase diagram. The simulations further demonstrate the

dependence of the lattice constant and stability of the SkX as a function of film thickness.

       Similar to Ref. [33], the PTO films are assumed to grow along the [001] pseudo-

cubic direction. An external electric field denoted as 𝑬𝑒𝑥𝑡 = (0, 0, 𝐸𝑧 ) was applied

along [001] (where the x, y, and z axis of Cartesian coordinates correspond to the [100],

[010], and [001] pseudo-cubic direction, respectively). According to Landau-Ginzburg-

Devonshire theory, the free energy is expressed as 𝐹 = ∫𝑉 (𝑓𝐿𝑎𝑛𝑑 + 𝑓𝑔𝑟𝑎𝑑 + 𝑓𝑒𝑙𝑎𝑠 +

𝑓𝑒𝑙𝑒𝑐 )𝑑𝑉 + ∫𝑆 𝑓𝑠𝑢𝑟𝑓 𝑑𝑆 , where 𝑓𝐿𝑎𝑛𝑑 , 𝑓𝑔𝑟𝑎𝑑 , 𝑓𝑒𝑙𝑎𝑠 , 𝑓𝑒𝑙𝑒𝑐 , and 𝑓𝑠𝑢𝑟𝑓 represent the

bulk Landau potential, gradient, elastic, electrostatic, and surface energy densities,

respectively. The electrostatic energy density can be expressed as 𝑓𝑒𝑙𝑒𝑐 = −𝑷𝑖 𝑬𝑖 −
1                                    1
 𝜀 𝑬 𝑬 = −𝑷𝑖 [𝑬𝑒𝑥𝑡 + (1 − 𝜃)𝑬𝑑𝑒𝑝 ] − 2 𝜀𝑏 [𝑬𝑒𝑥𝑡 + (1 − 𝜃)𝑬𝑑𝑒𝑝 ][𝑬𝑒𝑥𝑡 + (1 −
2 𝑏 𝑖 𝑖        𝑖             𝑖              𝑖             𝑖      𝑖

    𝑑𝑒𝑝                        𝑑𝑒𝑝
𝜃)𝑬𝑖      ], where 𝜃, 𝑬𝑒𝑥𝑡
                       𝑖 , 𝑬𝑖        , 𝜀𝑏 are the screening factor, external electric field,

depolarization field under open-circuit boundary conditions, and the background

                                               4
permittivity, respectively. As the default conditions, the screening factor θ is set to 0.6

to achieve an appropriate depolarization field (wherein 𝜃 = 0 corresponds to ideal

open-circuit conditions and 𝜃 = 1 corresponds to ideal short-circuit conditions), and

the substrate strain ε is set to −1.0% to ensure that the polarization has a preferred

orientation along the out-of-plane direction. Details of the formalism are provided in

the Supplemental Material [37].

     An epitaxial (001)-oriented PTO film of size 48 𝑛𝑚 × 48 𝑛𝑚 × 6 𝑛𝑚 is

considered as the initial specimen. As Ez increases from zero at room temperature, the

domain structure in the film undergoes a complex topological-phase transition (Fig. 1a).

To summarize the evolution of the system as the field is increased from zero to 1.8

MV/cm (top to bottom), we show the real-space distribution of local polarization (Fig.

1a), Pontryagin density (Fig. 1b), and free-energy density (Fig. 1c) of the top surface of

the film [37]. The Pontryagin density, as a typical O(3) topological invariant, is used to

identify the topological nature of the swirling domain structures [68]. At 𝐸𝑧 = 0, the

PTO films exhibit a labyrinth domain pattern (denoted as the L phase) with meandering

features as described before [30,69] (top row, Fig. 1a), where the white arrows and

colors denote the direction of in-plane polarization, the saturation of the color represents

the polarization magnitude, and the dark regions are domains with out-of-plane

polarizations. Similar morphology has been experimentally observed in STO/PTO/STO

tri-layer films and [PTO]n/[STO]n superlattices at room temperature under zero applied

field [33,70], indicating the validity of this simulation approach. The Pontryagin density

is weak at 𝐸𝑧 = 0, except slightly larger at the junctions of the labyrinth domain (first

                                             5
row, Fig.1b). The meandering feature of the L phase can be identified clearly from the

energy-density map (first row, Fig.1c) wherein the energy-density is high at regions

where there is strong out-of-plane polarization (dark regions; first row, Fig.1a),

reflecting the huge energy cost due to the depolarization field. As 𝐸𝑧 increases,

individual skyrmions are first generated at the junctions of the labyrinth domains. When

Ez reaches 0.6 MV/cm, local skyrmions emerge and coexist with the labyrinth domains

(denoted as the Sk & L phase) (second row, Fig. 1a). The Pontryagin density is larger at

each skyrmion core (second row, Fig.1b), and the topological charge of the skyrmion is

calculated to be 1 through the surface integration of the Pontryagin density [35].

Correspondingly, the free-energy-density distribution shows that the annular transition

region which possesses in-plane polarizations is in a low-energy state (second row, Fig.

1c). Upon further increasing Ez to 1.2 MV/cm, a complete SkX with well-ordered

hexagonal, close-packed features is observed (third row, Fig. 1a); analogous to the

classical SkX in helical magnets [20,21]. The Pontryagin density also exhibits

hexagonal order, with the brightest (largest value) regions corresponding to the

positions of the skyrmion cores (third row, Fig. 1b). The hexagonal arrangement is also

seen in the energy-density map (third row, Fig. 1c) where the density is large at each

skyrmion core, periphery, and the interfacial region between two neighboring

skyrmions (where out-of-plane polarization dominates), while it is small at the annular

transition region from the core to the periphery of each skyrmion (where in-plane

polarization dominates). Finally, when Ez reaches 1.8 MV/cm, the SkX phase is

destroyed and transformed into the topologically trivial single-domain phase with pure

                                           6
out-of-plane polarization (denoted as a ferroelectric FE phase; fourth row, Fig. 1a),

where the Pontryagin density (fourth row, Fig. 1b) is essentially zero and the energy

density (fourth row, Fig. 1c) is homogeneously large. Similar skyrmion nucleation and

SkX-formation were achieved as we varied the temperature under a constant external

electric field (𝐸𝑧 = 0.4 MV/cm; Fig. 1d~f). There, as the temperature is increased, the L

phase observed at 100 K transforms to a mixed Sk & L phase at 450 K, before fully

transforming to a hexagonal, close-packed SkX at 500 K, and, ultimately, the domain

contrast disappears at ~600 K.

     To gain further insights into the nature of the SkX, the SkX phase was simulated in

larger cells, including a PTO film of size 160 𝑛𝑚 × 160 𝑛𝑚 × 6 𝑛𝑚 at 𝑇 = 500 K.

Distinct from the L phase at 300 K, the initial state at Ez = 0 in the film at higher

temperature of 500 K is the stripe domain (denoted as the S phase; Supplemental

Material [37]). For this same simulation cell, however, increasing the field to Ez = 0.6

MV/cm results in a hexagonal SkX phase with a periodic array of swirling polar textures

over the entire surface (Fig. 2a). The polarization distribution of a single skyrmion in

this SkX phase is further examined (left column, Fig. 2a) and it is seen that the top and

bottom planes of each skyrmion are center-convergent and center-divergent,

respectively, while the middle plane has a purely out-of-plane polarization component.

That is, the polarization vectors rotate within the plane parallel to the radial direction,

indicating that the SkX phase is of Néel-type. Noting that the Néel-type SkX phase is

different from the skyrmion bubble found in PTO/STO superlattices reported in

previous studies [33]. Although both are composed of two standard Néel-type skyrmion

                                            7
hats of the top and bottom layers, the connected cylindrical domain wall at the middle

layer exhibits different characteristics, wherein the former is an Ising-type wall with

out-of-plane polarizations while the latter is Bloch-type with in-plane ones [33]. Such

a difference could be due to the larger compressive strain in the current model, which

would favor out-of-plane polarization. Besides, the two-point correlation function and

the spectra density function have been employed to characterize the ordering of

topology in the films quantitatively [37].

     To better understand the formation mechanism of the SkX phase, a schematic is

drawn to analyze the difference and correlation between the domain structures before

and after the application of an external electric field (Fig. 2b). Before Ez is applied, for

both the L and S phases, the cross-section view of the domain structures exhibits

periodic, long-range-ordered clockwise (CW) and counterclockwise (CCW) polar

vortices (Fig. 2bi) [69]. Upon application of a positive Ez, the upward polarization

region (crimson) is enhanced, and the downward polarization region (indigo) is

depressed which results in the adjacent CW-CCW vortices being forced to approach

and pair with each other. Ultimately, this results in the formation of Néel-type

skyrmions where the polarization at the skyrmion core (periphery) is oriented

antiparallel (parallel) to the applied field Ez (Fig. 2bii). The interfacial region between

two neighboring skyrmions would, effectively, acts as a topological protection zone.

This is supported by the energy-density map in the SkX phase shown previously (third

row, Fig.1c) since the energy density in the interfacial region is much larger than that

near the skyrmion, thus, it would be difficult for the skyrmion to cross the barrier of the

                                             8
interfacial region and destroy the close-packed lattice phase. The close-packed SkX

lattice phase, in turn, forms from the delicate interplay of elastic, electrostatic, and

gradient energies. First, the depolarization field, due to the incomplete screening of the

polarization at the surfaces, favors 180° domains (i.e., L or S domains), which is the

basis for the formation of the SkX phase. Second, in contrast to the effect of the

depolarization field, both the compressive strain and external electric field favor the

formation of (uniform) out-of-plane polarization. On the other hand, the gradient energy

is mainly related to the polarization inhomogeneity. These energy terms are all in

competition and eventually result in the formation of complex polar textures. In

particular, the strong competition between the considerable depolarization field caused

by incomplete screening and the applied electric field appears to be the most critical to

induce the topological-phase transition from stripe domain to the SkX phase.

     To more completely describe the evolution of the skyrmions under electric field

and temperature, we further constructed a phase diagram of the polar textures. Figure 3

shows the T-E phase diagram under Ez for a 48 𝑛𝑚 × 48 𝑛𝑚 × 6𝑛𝑚 film. Six

characteristic polarization structures are found across the range of temperatures and

electric field probed herein, including: SkX (Fig. 3a), L (Fig. 3b), S (Fig. 3c), Sk glass

(denoting the disordered, sparse skyrmion phase; Fig. 3d), mixed Sk & L (Fig. 3e), and

mixed Sk & FE (Fig. 3f). The SkX phase (outlined in white, Fig. 3g) has the absolute

value of topological charge of 1 and the Sk glass phase corresponds to a topological

charge of slightly less than 1. The S and FE phases have a topological charge of zero,

while the L phase should (ideally) have zero topological charge, but it can fluctuate

                                            9
between 0 to 0.1 depending on the degree of meandering in the maze. For the mixed-

phase regions (i.e., Sk & FE and Sk & L phases) the topological charge is between 0

and 1. It is interesting to note that an inverse-phase transition takes place as one

progresses from the low-temperature L phase to the high-temperature S phase with

increasing temperature. A similar inverse-phase transition has been reported recently in

PbZr0.4Ti0.6O3 ultrathin films using first-principles-based effective Hamiltonian

simulations [71]. From the global T-E diagram, the SkX phase occurs only between 300

K and 500 K. Furthermore, as mentioned above, two different topological-phase

transitions exist to reach the SkX phase: 1) the S to SkX transition with increasing

electric field (active from 470 to 500 K) and 2) the L to SkX transition with increasing

electric field (active from 300 to 470 K) [37]. Finally, the skyrmions completely

disappear for Ez > 2.6 MV/cm or T > 550 K, which suggests a transition into the

collinear polar state (i.e., the FE phase). For the comparative verification of the

effectiveness of these results, we conducted simulations via a first-principles effective

Hamiltonian method to further support the existence of polar SkX in PbTiO3 ultrathin

films [37]. Besides, we have investigated the general characteristics of SkX in a broader

system, e.g., tetragonal PbZr1-xTixO3 (x=0.6) films under appropriate boundary

conditions [37].

     After clarifying the formation mechanism of the hexagonal, close-packed SkX

phase, the influence of film thickness on the hexagonal lattice constant and stability of

the SkX phase was further explored. PTO films with size 80 𝑛𝑚 × 80 𝑛𝑚 × ℎ 𝑛𝑚 at

500 K were selected to simulate the thickness evolution of the polar texture. The

                                           10
simulations reveal that the film thickness ℎ plays a significant role in the polar textures

(Fig. 4a). For films with h < 5 nm, topologically trivial polar structures, such as in-

plane-polarized domains, single domain, or even paraelectric states dominate mainly

due to the large depolarization field in ultrathin films [72]. For relatively thicker films,

the SkX phases emerge and is stabilized within the range 5.0 nm < h < 13.0 nm due to

a subtle competition and balance between the depolarization field and external electric

field. For a given film thickness, it is found that the distance between two adjacent

skyrmion cores (i.e., the modulated period of the S phase in Fig. 2bi), remains

unchanged with varying external electric fields. Therefore, the lattice constant w of the

hexagonal polar SkX is defined as the distance between the cores of two adjacent

skyrmions (Fig. 4b) [73]. Two typical cases of the polarization distributions of SkX

phases with ℎ = 11.2 nm (Fig. 4b) and 6 nm (Fig. 4c) are shown, whereby 𝑤 is

found to be 20.5 nm and 13.6 nm, respectively. Generally, topologically trivial domains

in ferroelectric, ferromagnetic, and ferroelastic films obey Kittel’s law scaling wherein

the domain width scales with the square root of film thickness [74-76]. It is interesting

to note that the square of the hexagonal lattice constant w is found to be linearly

proportional to the film thickness h, that is, the lattice size of the topological domain

structure follows Kittel’s scaling law. In thicker films (13 nm < h < 18 nm), the

formation of the SkX phase becomes challenging due to the weak depolarization field

and, instead, the disordered Sk glass state becomes dominant in this thickness range.

     In summary, phase-field simulations establish a global T-E phase diagram of the

polar structures and reveal the existence of hexagonal, close-packed Néel-type polar

                                            11
SkX in ferroelectric PTO thin films. The results further demonstrate that the lattice

constant of the SkX is linearly proportional to the square root of the film thickness,

following the Kittel’s scaling law. The SkX phase in the ferroelectric PTO films is

constructed in a periodic lattice manner similar to atomic or molecular crystals,

resembling those composed by various topological solitons in other physical contexts,

such as the skyrmion lattice in magnetic materials and liquid crystals [77-79], vortex

rings in superfluids and ultra-cold gases [80,81], etc. These findings open a way for

further exploration of ordered condensed-matter phases assembled from polar

skyrmions and other topological soliton “building blocks” in nanoscale ferroelectric

materials.




Acknowledgement

This work was funded by the National Natural Science Foundation of China (Grant Nos.

U1932116 and 51802057), Guangdong Basic and Applied Basic Research Foundation

(Grant No. 2020B1515020029), Shenzhen Science and Technology Innovation project

(Grant No. JCYJ20200109112829287), and Shenzhen Science and Technology

Program (Grant No. KQTD20200820113045083). Z.H.C. has been supported by “the

Fundamental    Research    Funds    for   the   Central   Universities”   (Grant   No.

HIT.OCEF.2022038) and “Talent Recruitment Project of Guangdong” (Grant No.

2019QN01C202). S.Y. acknowledges the financial support from China Postdoctoral

Science Foundation (No. DB24407028), and Guangxi Science and Technology

Program (Grant No. AD20159059). S.P., Y.N. and L.B. are grateful for the support by

                                          12
the Vannevar Bush Faculty Fellowship (VBFF) Grant No. N00014-20-1-2834 from the

Department of Defense, and the Army Research Office under the ETHOS MURI Grant

W911NF-21-2-0162. The first-principles based effective Hamilton simulations were

performed the University of Arkansas with the support from the Arkansas High

Performance Computing Center (AHPCC). B. Xu acknowledges financial support from

National Natural Science Foundation of China under Grant No. 12074277. C. L.

acknowledges the financial support from the Natural Science Foundation of Jiangsu

Province (Grant no. BK20210565). S.D. acknowledges Science and Engineering

Research Board (SRG/2022/000058) and Indian Institute of Science start-up grant for

financial support. L.W.M. acknowledges support from the Army Research Office under

the ETHOS MURI via cooperative agreement W911NF-21-2-0162.




                                        13
References
[1] F. D. M. Haldane, Nobel lecture: Topological quantum matter, Rev. Mod. Phys. 89, 040502 (2017).
[2] J. M. Kosterlitz, Nobel lecture: Topological defects and phase transitions, Rev. Mod. Phys. 89, 040501
(2017).
[3] Y. Zheng and W. Chen, Characteristics and controllability of vortices in ferromagnetics, ferroelectrics,
and multiferroics, Rep. Prog. Phys. 80, 086501 (2017).
[4] P. Zubko, J. C. Wojdel, M. Hadjimichael, S. Fernandez-Pena, A. Sené, I. Luk'yanchuk, J. M. Triscone,
and J. Íniguez, Negative capacitance in multidomain ferroelectric superlattices, Nature 534, 524 (2016).
[5] Y. J. Wang, Y. P. Feng, Y. L. Zhu, Y. L. Tang, L. X. Yang, M. J. Zou, W. R. Geng, M. J. Han, X. W.
Guo, B. Wu, and X. L. Ma, Polar meron lattice in strained oxide ferroelectrics, Nat. Mater. 19, 881 (2020).
[6] D. Rusu, J. J. P. Peters, T. P. A. Hase, J. A. Gott, G. A. A. Nisbet, J. Strempfer, D. Haskel, S. D.
Seddon, R. Beanland, A. M. Sanchez, and M. Alexe, Ferroelectric incommensurate spin crystals, Nature
602, 240 (2022).
[7] S. Q. Chen, S. Yuan, Z. P. Hou, Y. L. Tang, J. P. Zhang, T. Wang, K. Li, W. W. Zhao, X. J. Liu, L.
Chen, L. W. Martin, Z. H. Chen, Recent progress on topological structures in ferroic thin films and
heterostructures, Adv. Mater. 33, 2000857 (2021).
[8] N. D. Mermin, The topological theory of defects in ordered media, Rev. Mod. Phys. 51, 591 (1979).
[9] R. I. Eglitis and D. Vanderbilt, Ab initio calculations of BaTiO 3 and PbTiO3 (001) and (011) surface
structures, Phys. Rev. B 76, 155439 (2007).
[10] R. I. Eglitis, S. Piskunov, and Y. F. Zhukovskii, Ab initio calculations of PbTiO 3/SrTiO3 (001)
heterostructures, Phys. Status Solidi C 13, 913 (2016).
[11] T. H. R. Skyrme, A unified field theory of mesons and baryons, Nucl. Phys. 31, 556 (1962).
[12] R. Wiesendanger, Nanoscale magnetic skyrmions in metallic films and multilayers: a new twist for
spintronics, Nat. Rev. Mater. 1, 1 (2016).
[13] G. Finocchio, F. Büttner, R. Tomasello, M. Carpentieri, and M. Kläui, Magnetic skyrmions: from
fundamental to applications, J. Phys. D: Appl. Phys. 49, 423001 (2016).
[14] X. Zhang, Y. Zhou, K. M. Song, T.-E. Park, J. Xia, M. Ezawa, X. Liu, W. Zhao, G. Zhao and S. Woo,
Skyrmion-electronics: writing, deleting, reading and processing magnetic skyrmions toward spintronic
applications, J. Phys.: Condens. Matter 32, 143001 (2020).
[15] U. K. Roessler, A. N. Bogdanov, and C. Pfleiderer, Spontaneous skyrmion ground states in magnetic
metals, Nature 442, 797 (2006).
[16] B. Keimer, F. Doğan, I. A. Aksay, R. W. Erwin, J. W. Lynn, and M. Sarikaya, Inclined-Field Structure,
Morphology, and Pinning of the Vortex Lattice in Microtwinned YBa 2Cu3O7, Science 262, 83 (1993).
[17] J. Lynn, N. Rosov, T. Grigereit, H. Zhang, and T. Clinton, Vortex dynamics and melting in niobium,
Phys. Rev. Lett. 72, 3413 (1994).
[18] A. Bogdanov and D. Yablonskii, Thermodynamically stable “vortices” in magnetically ordered
crystals. The mixed state of magnets, Zh. Eksp. Teor. Fiz 95, 182 (1989).
[19] A. Bogdanov and A. Hubert, Thermodynamically stable magnetic vortex states in magnetic crystals,
J. Magn. Magn. Mater. 138, 255 (1994).
[20] S. Mühlbauer, B. Binz, F. Jonietz, C. Pfleiderer, A. Rosch, A. Neubauer, R. Georgii, and P. Böni,
Skyrmion lattice in a chiral magnet, Science 323, 915 (2009).
[21] X. Yu, Y. Onose, N. Kanazawa, J. H. Park, J. Han, Y. Matsui, N. Nagaosa, and Y. Tokura, Real-space
observation of a two-dimensional skyrmion crystal, Nature 465, 901 (2010).

                                                    14
[22] I. Kézsmárki, S. Bordács, P. Milde, E. Neuber, L. M. Eng, J. S. White, H. M. Rønnow, C. D.
Dewhurst, M. Mochizuki, K. Yanai, H. Nakamura, D. Ehlers, V. Tsurkan, and A. Loidl, Néel-type
skyrmion lattice with confined orientation in the polar magnetic semiconductor GaV 4S8. Nat. Mater. 14,
1116 (2015).
[23] W. Münzer, A. Neubauer, T. Adams, S. Mühlbauer, C. Franz, F. Jonietz, R. Georgii, P. Böni, B.
Pedersen, M. Schmidt, A. Rosch, and C. Pfleiderer, Skyrmion lattice in the doped semiconductor Fe 1-
xCoxSi, Phys. Rev. B 81, 041203 (2010).

[24] M.-G. Han, J. A. Garlow, Y. Kharkov, L. Camacho, R. Rov, J. Sauceda, G. Vats, K. Kisslinger, T.
Kato, O. Sushkov, Y. Zhu, C. Ulrich, T. Söhnel, and J. Seidel, Scaling, rotation, and channeling behavior
of helical and skyrmion spin textures in thin films of Te-doped Cu2OSeO3, Sci. Adv. 6, eaax2138 (2020).
[25] D. Foster, C. Kind, P. J. Ackerman, J.-S. B. Tai, M. R. Dennis, and I. I. Smalyukh, Two-dimensional
skyrmion bags in liquid crystals and ferromagnets, Nat. Phys. 15, 655 (2019).
[26] J. Tang, Y. Wu, W. Wang, L. Kong, B. Lv, W. Wei, J. Zang, M. Tian, and H. Du, Magnetic skyrmion
bundles and their current-driven dynamics, Nat. Nanotechnol. 16, 1086 (2021).
[27] Y. Wang, L. Wang, J. Xia, Z. Lai, G. Tian, X. Zhang, Z. Hou, X. Gao, W. Mi, C. Feng, M. Zeng, G.
Zhou, G. Yu, G. Wu, Y. Zhou, W. Wang, X. Zhang, and J. Liu, Electric-field-driven non-volatile multi-
state switching of individual skyrmions in a multiferroic heterostructure, Nat. Commun. 11, 3577 (2020).
[28] X. B. Zhao, C. M. Jin, C. Wang, H. F. Du, J. D. Zang, M. L. Tian, R. C. Che, and Y. H. Zhang, Direct
imaging of magnetic field-driven transitions of skyrmion cluster states in FeGe nanodisks, Proc. Natl.
Acad. Sci. U. S. A. 113, 4918 (2016).
[29] Y. Nahas, S. Prokhorenko, L. Louis, Z. Gui, I. Kornev, and L. Bellaiche, Discovery of stable
skyrmionic state in ferroelectric nanocomposites, Nat. Commun. 6, 8542 (2015).
[30] Y. Nahas, S. Prokhorenko, Q. Zhang, V. Govinden, N. Valanoor, and L. Bellaiche, Topology and
control of self-assembled domain patterns in low-dimensional ferroelectrics, Nat. Commun. 11, 5779
(2020).
[31] M. P. Gonçalves, C. Escorihuela-Sayalero, P. Garca-Fernández, J. Junquera, and J. Íñiguez,
Theoretical guidelines to create and tune electric skyrmion bubbles, Sci. Adv. 5, eaau7023 (2019).
[32] Z. Hong and L.-Q. Chen, Blowing polar skyrmion bubbles in oxide superlattices, Acta Mater. 152,
155 (2018).
[33] S. Das, Y. L. Tang, Z. Hong, M. A. P. Gonçalves, M. R. McCarter, C. Klewe, K. X. Nguyen, F.
Gómez-Ortiz, P. Shafer, E. Arenholz, V. A. Stoica, S.-L. Hsu, B. Wang, C. Ophus, J. F. Liu, C. T. Nelson,
S. Saremi, B. Prasad, A. B. Mei, D. G. Schlom, J. Íñiguez, P. García-Fernández, D. A. Muller, L.-Q. Chen,
J. Junquera, L. W. Martin, and R. Ramesh, Observation of room-temperature polar skyrmions, Nature
568, 368 (2019).
[34] S. Das, Z. Hong, V. A. Stoica, M. A. P. Gonçalves, Y. T. Shao, E. Parsonnet, E. J. Marksz, S. Saremi,
M. R. McCarter, A. Reynoso, C. J. Long, A. M. Hagerstrom, D. Meyers, V. Ravi, B. Prasad, H. Zhou, Z.
Zhang, H. Wen, F. Gómez-Ortiz, P. García-Fernández, J. Bokor, J. Íñiguez, J. W. Freeland, N. D. Orloff,
J. Junquera, L.-Q. Chen, S. Salahuddin, D. A. Muller, L. W. Martin, and R. Ramesh, Local negative
permittivity and topological phase transition in polar skyrmions, Nat. Mater. 20, 194 (2021).
[35] L. Han, C. Addiego, S.Prokhorenko, M. Wang, H. Fu, Y. Nahas, X. Yan, S. Cai, T. Wei, Y. Fang, H.
Liu, D. Ji, W. Guo, Z. Gu, Y. Yang, P. Wang, L. Bellaiche, Y. Chen, D.Wu, Yu. Nie, and X. Pan, High-
density switchable skyrmion-like polar nanodomains integrated on silicon, Nature 603, 63 (2022).
[36] I. Kornev, H. Fu, and L. Bellaiche, Ultrathin films of ferroelectric solid solutions under a residual
depolarizing field, Phys. Rev. Lett. 93, 196104 (2004).

                                                   15
[37] See Supplemental Material at [URL] for the phase-field modelling, calculations of topological
charges, characterization of SkX ordering, typical evolution processes of topological phase transitions,
effects of screening factors and misfit strain on T-E phase diagram, and verification via first-principles
effective Hamiltonian simulations, which includes which includes Refs. [38-67].
[38] A. K. Tagantsev, Landau expansion for ferroelectrics: Which variable to use?, Ferroelectrics 375, 19
(2008).
[39] Y. Zheng and C. H. Woo, Thermodynamic modeling of critical properties of ferroelectric
superlattices in nano-scale, Appl. Phys. A 97, 617 (2009).
[40] H. L. Hu and L.-Q. Chen, Three‐dimensional computer simulation of ferroelectric domain formation,
J. Am. Ceram. Soc. 81, 492 (1998).
[41] S. Yuan, W. J. Chen, L. L. Ma, Y. Ji, W. M. Xiong, J. Y. Liu, Y. L. Liu, B. Wang, and Y. Zheng,
Defect-mediated vortex multiplication and annihilation in ferroelectrics and the feasibility of vortex
switching by stress, Acta Mater. 148, 330 (2018).
[42] J. Hlinka and P. Marton, Phenomenological model of a 90° domain wall in BaTiO 3-type
ferroelectrics, Phys. Rev. B 74, 104104 (2006).
[43] J. J. Wang, X. Q. Ma, Q. Li, J. Britson, and L.-Q. Chen, Phase transitions and domain structures of
ferroelectric nanoparticles: Phase field model incorporating strong elastic and dielectric inhomogeneity,
Acta Mater. 61, 7591 (2013).
[44] A. G. Khachaturyan, Theory of structural transformations in solids (Courier Corporation, 2013).
[45] S. Yuan, W. J. Chen, J. Y. Liu, Y. L. Liu, B. Wang, and Y. Zheng, Torsion-induced vortex switching
and skyrmion-like state in ferroelectric nanodisks, J. Phys.: Condens. Matter 30, 465304 (2018).
[46] A. K. Tagantsev, G. Gerra, and N. Setter, Short-range and long-range contributions to the size effect
in metal-ferroelectric-metal heterostructures, Phys. Rev. B 77, 174111 (2008).
[47] R. Kretschmer and K. Binder, Surface effects on phase transitions in ferroelectrics and dipolar
magnets, Phys. Rev. B 20, 1065 (1979).
[48] W. L. Zhong, Y. G. Wang, P. L. Zhang, and B. D. Qu, Phenomenological study of the size effect
on phase transitions in ferroelectric particles, Phys. Rev. B 50, 698 (1994).
[49] L.-Q. Chen, Phase-field models for microstructure evolution, Annu. Rev. Mater. Res. 32, 113 (2002).
[50] L.-Q. Chen, Phase‐field method of phase transitions/domain structures in ferroelectric thin films: a
review, J. Am. Ceram. Soc. 91, 1835 (2008).
[51] G. B. Arfken and H. J. Weber, Mathematical methods for physicists (American Association of
Physics Teachers, 1999).
[52] B.-K. Lai, I. Ponomareva, I. Naumov, I. Kornev, H. Fu, L. Bellaiche, and G. Salamo, Electric-field-
induced domain evolution in ferroelectric ultrathin films, Phys. Rev. Lett. 96, 137602 (2006).
[53] Y. Ji, W. Chen, and Y. Zheng, Crossover of polar and toroidal orders in ferroelectric nanodots with
a morphotropic phase boundary and nonvolatile polar-vortex transformations, Phys. Rev. B 100, 014101
(2019).
[54] C. Wu, W. Chen, D. Ma, C. H. Woo, and Y. Zheng, Effects of the surface charge screening and
temperature on the vortex domain patterns of ferroelectric nanodots, J. Appl. Phys. 112, 104108 (2012).
[55] N. A. Pertsev, A. G. Zembilgotov, and A. K. Tagantsev, Effect of mechanical boundary conditions
on phase diagrams of epitaxial ferroelectric thin films, Phys. Rev. Lett 80, 1988 (1998).
[56] M. J. Haun, E. Furman, S. J. Jang, H. A. McKinstry, and L. E. Cross, Thermodynamic theory of
PbTiO3, J. Appl. Phys 62, 3331 (1987).
[57] K. Ishikawa and T. Uemori, Surface relaxation in ferroelectric perovskites, Phys. Rev. B 60, 11841

                                                    16
(1999).
[58] C. H. Woo and Y. Zheng, Depolarization in modeling nano-scale ferroelectrics using the Landau
free energy functional, Appl. Phys. A 91, 59 (2008).
[59] L.D. Landau, J.S. Bell, M.J. Kearsley, L. P. Pitaevskii, Electrodynamics of Continuous Media
(Elsevier, 2013).
[60] S. Niezgoda, D. Fullwood, and S. Kalidindi, Delineation of the space of 2-point correlations in a
composite material system, Acta Mater. 56, 5285 (2008).
[61] A. Cecen, T. Fast, and S. R. Kalidindi, Versatile algorithms for the computation of 2-point spatial
correlations in quantifying material structure, Integr. Mater. Manuf. I. 5, 1 (2016).
[62] P. Altschuh, Y. C. Yabansu, J. Hötzer, M. Selzer, B. Nestler, and S. R. Kalidindi, Data science
approaches for microstructure quantification and feature identification in porous membranes, J. Membr.
Sci. 540, 88 (2017).
[63] R. Bostanabad, Y. Zhang, X. Li, T. Kearney, L. C. Brinson, D. W. Apley, W. K. Liu, and W. Chen,
Computational microstructure characterization and reconstruction: Review of the state-of-the-art
techniques, Prog. Mater. Sci. 95, 1 (2018).
[64] J. W. Cooley and J. W. Tukey, An algorithm for the machine calculation of complex Fourier series,
Math. Comput. 19, 297 (1965).
[65] U. V. Waghmare and K. M. Rabe, Ab initio statistical mechanics of the ferroelectric phase transition
in PbTiO3, Phys. Rev. B 55, 6161 (1997).
[66] I. Ponomareva, I. I. Naumov, I. Kornev, H. Fu, and L. Bellaiche, Atomistic treatment of depolarizing
energy and field in ferroelectric nanostructures, Phys. Rev. B 72, 140102 (2005).
[67] V. Govinden, S. Rijal, Q. Zhang, Y. Nahas, L. Bellaiche, N. Valanoor, and S. Prokhorenko, Stability
of ferroelectric bubble domains, Phys. Rev. Materials 7, L011401 (2023).
[68] N. Nagaosa and Y. Tokura, Topological properties and dynamics of magnetic skyrmions, Nat.
Nanotechnol. 8, 899 (2013).
[69] A. K. Yadav, C. T. Nelson, S. L. Hsu, Z. Hong, J. D. Clarkson, C. M. Schlepütz, A. R. Damodaran,
P. Shafer, E. Arenholz, L. R. Dedon, D. Chen, A. Vishwanath, A. M. Minor, L.-Q. Chen, J. F. Scott, L.
W. Martin, and R. Ramesh, Observation of polar vortices in oxide superlattices, Nature 530, 198 (2016).
[70] R. Zhu, Z. Jiang, X. Zhang, X. Zhong, C. Tan, M. Liu, Y. Sun, X. Li, R. Qi, K. Qu, Z. Liu, M. Wu,
M. Li, B. Huang, Z. Xu, J. Wang, K. Liu, P. Gao, J. Wang, J. Li, and X. Bai, Dynamics of Polar Skyrmion
Bubbles under Electric Fields, Phys. Rev. Lett. 129, 107601 (2022).
[71] Y. Nahas, S. Prokhorenko, J. Fischer, B. Xu, C. Carrétéro, S. Prosandeev, M. Bibes, S. Fusil, B.
Dkhil, V. Garcia, and L. Bellaiche, Inverse transition of labyrinthine domain patterns in ferroelectric thin
films, Nature 577, 47 (2020).
[72] J. Junquera and P. Ghosez, Critical thickness for ferroelectricity in perovskite ultrathin films, Nature
422, 506 (2003).
[73] S. Seki, X. Z. Yu, S. Ishiwata, and Y. Tokura, Observation of skyrmions in a multiferroic material,
Science 336, 198 (2012).
[74] S. K. Streiffer, J. A. Eastman, D. D. Fong, C. Thompson, A. Munkholm, M. R. Murty, O. Auciello,
G. R. Bai, and G. B. Stephenson, Observation of Nanoscale 180° Stripe Domains in Ferroelectric PbTiO3
Thin Films, Phys. Rev. Lett. 89, 067601 (2002).
[75] M. Daraktchiev, G. Catalan, and J. F. Scott, Landau theory of ferroelectric domain walls in
magnetoelectrics, Ferroelectrics 375, 122 (2008).
[76] G. Catalan, J. Seidel, R. Ramesh, and J. F. Scott, Domain wall nanoelectronics, Rev. Mod. Phys. 84,

                                                    17
119 (2012).
[77] D. C. Wright and N. D. Mermin, Crystalline liquids: the blue phases, Rev. Mod. Phys. 61, 385 (1989).
[78] A. Nych, J.-I Fukuda, U. Ognysta, S. Žumer, and I. Muševič, Spontaneous formation and dynamics
of half-skyrmions in a chiral liquid-crystal film, Nat. Phys. 13, 1215 (2017).
[79] P. J. Ackerman and I. I. Smalyukh, Static three-dimensional topological solitons in fluid chiral
ferromagnets and colloids, Nat. Mater. 16, 426 (2017).
[80] G. W. Rayfield and F. Reif, Quantized vortex rings in superfluid helium, Phys. Rev. 136, A1194
(1964).
[81] J. Ruostekoski and J. R. Anglin, Creating vortex rings and three-dimensional skyrmions in Bose-
Einstein condensates, Phys. Rev. Lett. 86, 3934 (2001).




                                                   18
FIG. 1 (color online). Variation of polar texture with electric field and temperature
in a PbTiO3 film mimicked by size of 𝟒𝟖 𝒏𝒎 × 𝟒𝟖 𝒏𝒎 × 𝟔 𝒏𝒎. Evolution of (a)
polarization configuration, (b) Pontryagin density, and (c) free energy density of the top
layer of the film with increment of an electric field at 𝑇 = 300 K. d)-f) The topological
transition with increment of temperature at a fixed electric field 𝐸𝑧 = 0.4 MV/cm.




                                           19
FIG. 2 (color online). Nature of the SkX and its formation mechanism. (a) The SkX
in a PbTiO3 film of 160 nm × 160 nm × 6 nm. The plane view of the Pz distribution
of SkX is on the right, and the polarization distributions on the top layer, middle layer,
and bottom layer of the white-marked region are on the left. The golden arrow indicates
the polarization vector. (b) Schematic of SkX formation mechanism from the cross-
sectional perspective of the film. The green dots indicate vortex cores. Crimson and
indigo represent region with polarizations upward and downward, respectively.




                                           20
FIG. 3 (color online). T-E phase diagram of polar texture in a 𝟒𝟖 𝒏𝒎 × 𝟒𝟖 𝒏𝒎 ×
𝟔𝒏𝒎 PTO film, the color bar denotes the absolute value of the topological charge
Q. Six typical domain structures are shown around the phase diagram (g), including (a)
SkX, (b) parallel-stripe domain (S), (c) labyrinth-stripe domain (L), (d) the disordered
sparse skyrmions (Sk glass), (e) mixed phase of Sk glass and labyrinth-stripe domain
(Sk & L), (f) mixed phase of Sk glass and single domain (Sk & FE).




                                          21
FIG. 4 (color online). Kittel’s law in the SkX phase. (a) Thickness dependence of the
polar structures in films of 80 𝑛𝑚 × 80 𝑛𝑚 × ℎ. The straight line is a fit to Kittel’s
law. Polarization distribution of the SkX phases for film thickness ℎ of (b) 11.2 nm and
(c) 6.0 nm.




                                          22

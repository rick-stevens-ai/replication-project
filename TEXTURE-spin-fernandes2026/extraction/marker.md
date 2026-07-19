<!--
EXTRACTION ARTIFACT: marker.md
Paper: Anomalous Hall viscosity of altermagnets (arXiv:2606.26239)
Authors: Iksu Jang, Rui Aquino, Jorg Schmalian, Rafael M. Fernandes (2026)

TOOL STATUS: marker (marker-pdf) is NOT installed on this host.
This file is an INTERIM extraction produced with `pdftotext -layout`
(poppler) as the fallback documented in the computational-replication-execution
skill. Layout mode preserves column/table structure adequately for the
method + parameter extraction that drove the replication. Equations render
as broken Unicode (a known pdftotext limitation on math-heavy PDFs); the
math-aware companion extraction/nougat.mmd carries the same content, and the
clean equation transcriptions live in report/REPORT.tex.

Regenerate with marker once available:
    marker_single textures-spin-fernandes2026.pdf --output_dir extraction/
-->

# Anomalous Hall viscosity of altermagnets

                                                                                             Anomalous Hall viscosity of altermagnets

                                                                              Iksu Jang,1 Rui Aquino,2, 3, 4 Jörg Schmalian,1, 5 and Rafael M. Fernandes2, 3
                                                                     1 Institute for Theory of Condensed Matter, Karlsruhe Institute of Technology, Karlsruhe 76131, Germany
                                                                                         2 Department of Physics, The Grainger College of Engineering,

                                                                                     University of Illinois Urbana-Champaign, Urbana, Illinois 61801, USA
                                                                        3 Anthony J. Leggett Institute for Condensed Matter Theory, The Grainger College of Engineering,

                                                                                     University of Illinois Urbana-Champaign, Urbana, Illinois 61801, USA
                                                                                4 ICTP South American Institute for Fundamental Research, São Paulo, SP, Brazil
                                                                 5 Institute for Quantum Materials and Technologies, Karlsruhe Institute of Technology, Karlsruhe 76131, Germany

                                                                                                               (Dated: June 26, 2026)
arXiv:2606.26239v1 [cond-mat.mes-hall] 24 Jun 2026




                                                                      We show that the phonon Hall viscosity at zero magnetic field is a natural probe of altermagnetism. First, we
                                                                   demonstrate that the finite elements of the Hall viscosity tensor unambiguously distinguish altermagnets from
                                                                   ferromagnets and conventional antiferromagnets. We then microscopically compute the Hall viscosity in models
                                                                   for 𝑑-wave and 𝑔-wave altermagnets, and find a strong sensitivity to electronic spectrum features such as gapped
                                                                   Dirac points and Lifshitz transitions. This sensitivity reflects a strain-space Berry curvature monopole, which
                                                                   contrast to the multipolar character of the standard momentum-space Berry curvature in altermagnets. Since the
                                                                   Hall viscosity can be probed experimentally through magneto-acoustic measurements, it provides a compelling
                                                                   method to probe the broken symmetries and topology of insulating altermagnets.


                                                        Altermagnets are compensated magnets that are invariant
                                                     under a combination of time reversal and a crystalline operation
                                                     that involves rotations, such as proper rotations, mirror
                                                     reflections, glide reflections, and screw rotations [1, 2]. This
                                                     symmetry endows altermagnets with distinctive 𝑑-wave, 𝑔-
                                                     wave, or 𝑖-wave characters, manifested both in the momentum
                                                     dependence of the spin-splitting of the electronic bands and in
                                                     the real-space spin density [3, 4]. However, the experimental
                                                     challenges in directly probing momentum-space spin-splitting
                                                     motivates the search for global response functions that not only
                                                     encode the symmetry of altermagnets, but also their unique
                                                     topological properties [5–11].
                                                        The anomalous Hall conductivity, a primary probe of non-
                                                     trivial topology [12, 13], vanishes in pure altermagnets due
                                                     to the multipolar character of their momentum-space Berry
                                                     curvature [11]. In the presence of spin-orbit coupling (SOC),           FIG. 1. Non-dissipative stress components 𝑇𝑥 𝑥 and 𝑇𝑦𝑦 generated
                                                     it can become non-zero either for specific moment directions            by a dynamic shear strain 𝜀¤ 𝑥 𝑦 due to the anomalous Hall viscosity
                                                     [14–18] or when external uniaxial strain is applied [11].               in a tetragonal system. Red and blue refer to spin-up and spin-down
                                                     Nevertheless, most altermagnetic candidates are insulators [2,          densities. The stress symmetry is determined by the type of magnetic
                                                                                                                             state: in a 𝑑-wave altermagnetic (AM) state, a symmetry-preserving
                                                     19–21], which limits the use of the Hall conductivity as a
                                                                                                                             static stress 𝑇𝑥 𝑥 = 𝑇𝑦𝑦 is generated (a), while in a ferromagnetic (FM)
                                                     probe of altermagnetism. Lattice responses, on the other                state, tetragonal-symmetry-breaking stress 𝑇𝑥 𝑥 = −𝑇𝑦𝑦 appears (b).
                                                     hand, can be measured in both metals and insulators. It is
                                                     thus valuable to elucidate the lattice responses of altermagnets,
                                                     particularly given their unique magneto-elastic properties, of          viscosity, we find that ferromagnets and altermagnets display
                                                     which piezomagnetism is the posterchild [22–37].                        finite but distinct Hall viscosity tensor elements at zero field.
                                                        Here, we show that the Hall viscosity, which is measured             To elucidate the microscopic mechanism, we calculate the
                                                     through sound waves rather than static strain, provides a               anomalous Hall viscosity in representative minimal models
                                                     natural probe of altermagnetic order and of the underlying              for tetragonal 𝑑-wave and hexagonal 𝑔-wave altermagnetism.
                                                     topology of the band structure. Also known as phonon                    In both cases, the Hall viscosity reflects a net strain-space
                                                     Hall viscosity, it is the antisymmetric, non-dissipative part           Berry curvature monopole, in sharp contrast to the multipolar
                                                     of the viscosity tensor that relates time-dependent strain to           character of the momentum-space Berry curvature that governs
                                                     transverse stress (Fig. 1). While previous works focused on             the anomalous Hall conductivity.
                                                     the Hall viscosity of magnetic insulators and quantum Hall                 This connection with the strain-space Berry curvature
                                                     systems in an external magnetic field [38–48], our focus is             makes the Hall viscosity highly sensitivity to special features
                                                     on the zero-field (i.e., anomalous) response. In contrast               of the altermagnetic electronic states. In 𝑑-wave altermagnets,
                                                     to antiferromagnets, which cannot have an anomalous Hall                we find it to be dominated by the spin-polarized Dirac points
                                                                                                                                                     2

that are gapped by the SOC [6]. This allows us to interpret the           where the minus superscript denotes a TRS-odd irrep. These
Hall viscosity as the “Hall conductivity” due to emergent spin-           irreps correspond to different even-parity 𝑸 = 0 magnetic
dependent electromagnetic gauge fields generated by dynamic               orders in the presence of SOC [25]. 𝐴2𝑔         − and 𝐸 − transform
                                                                                                                                       𝑔
strain. In 𝑔-wave altermagnets, we show that the strain-induced           like the out-of-plane and in-plane magnetization, respectively,
modification of the SOC is the main feature responsible for a             thus describing either ferromagnetic or mixed altermagnetic
finite anomalous Hall viscosity, which is strongly impacted by            order parameters (i.e., altermagnets with weak ferromagnetism
the saddle-points of the electronic bands. Importantly, while             due to SOC). In contrast, 𝐴1𝑔         − , 𝐵 − , and 𝐵 − describe
                                                                                                                       1𝑔              2𝑔
SOC is essential for a non-zero Hall viscosity, weak SOC                  pure altermagnetic order parameters (i.e., with a symmetry-
does not necessarily imply a small Hall viscosity. In fact,               enforced zero magnetization) with, respectively, 𝑔-wave,
the magnitude of our calculated Hall viscosity is comparable              𝑑 𝑥 𝑦 -wave, and 𝑑 𝑥 2 −𝑦 2 -wave spin-splitting symmetry. Thus,
to what was recently reported for 𝛼-RuCl3 using the acoustic              Eq. (3) implies that each type of magnetic order parameter is
Faraday effect [49].                                                      associated with a unique combination of non-zero anomalous
   Symmetry analysis: At low frequencies, dynamical                       Hall viscosity tensor elements, demonstrating the suitability
stresses 𝑇𝑖 𝑗 (𝑡) in a many-body system are related to time-              of 𝜂𝑖𝐻𝑗 𝑘𝑙 to distinguish between magnetic orders. Consider,
                                                                          for instance, the cases of a 𝑑 𝑥 2 −𝑦 2 altermagnet (𝐵2𝑔          − ) and a
dependent strain 𝜀 𝑘𝑙 (𝑡) via
                                                                                                                                     −
                                                                          ferromagnet with out-of-plane magnetization (𝐴2𝑔 ). While the
              𝑇𝑖 𝑗 (𝑡) = 𝐶𝑖 𝑗 𝑘𝑙 𝜀 𝑘𝑙 (𝑡) + 𝜂𝑖 𝑗 𝑘𝑙 𝜕𝑡 𝜀 𝑘𝑙 (𝑡) .   (1)   same anomalous Hall viscosity elements are non-zero in both
                                                                          cases, they have different relative signs: 𝜂 𝐻    𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦 𝑦 𝑥 𝑦 ≠ 0 for
                                                                                                                                        𝐻

The first term is the elastic tensor, whereas the second term             the altermagnet and 𝜂 𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦 𝑦 𝑥 𝑦 ≠ 0 for the ferromagnet,
                                                                                                      𝐻         𝐻
usually accounts for the fact that deformations performed                 resulting in different stresses generated by the same dynamic
at a finite rate are dissipative and generate heat. However,              shear strain, see Fig. 1. The End Matter shows the symmetry-
the elements 𝜂𝑖𝐻𝑗 𝑘𝑙 of the viscosity tensor 𝜂𝑖 𝑗 𝑘𝑙 that are             allowed 𝜂𝑖𝐻𝑗 𝑘𝑙 for altermagnets in various point groups.
antisymmetric under 𝑖 𝑗 ←→ 𝑘𝑙 are non-dissipative. This Hall                   Microscopic expression: To investigate the microscopic
viscosity tensor is odd under time reversal and even under                origin of the anomalous Hall viscosity in altermagnets, we
inversion, giving rise to the effective elastic action                    consider a system described by Bloch states 𝑢 𝒌,𝑏 with crystal
                            ∫                                             momentum 𝒌 and band index 𝑏. The full Hamiltonian
                          1                                               is
                   𝑆eff =        𝜂 𝐻 𝜀 𝑖 𝑗 𝜕𝑡 𝜀 𝑘𝑙 ,
                          2 𝑥,𝑡 𝑖 𝑗 𝑘𝑙
                                                           (2)            Í H𝒌 = H𝒌,0 + H𝒌, 𝜀 with a strain-free contribution H𝒌,0 =
                                                                              𝑏 𝜉𝒌𝑙 𝑢 𝒌,𝑏   𝑢 𝒌,𝑏 and a strain-dependent term H𝒌, 𝜀 =
                                                                                       𝑖𝑗                                                           𝑖𝑗
                                                                          𝜀 𝑖 𝑗 𝑏𝑏′ 𝛾𝑏𝑏′ ( 𝒌) 𝑢 𝒌,𝑏 𝑢 𝒌,𝑏′ . The coupling matrices 𝛾𝑏𝑏′
                                                                               Í
       ∫
with 𝑥,𝑡 denoting integration over space and time. This
                                                                          determine the electron-phonon coupling to acoustic lattice
elastic (phonon) Hall viscosity should not to be confused
                                                                          vibrations in the band basis [11]. The stress tensor 𝑇𝑖 𝑗
with the viscoelastic Hall response of an electronic fluid in
                                                                          generated by a dynamic strain that slowly varies in time can
the hydrodynamic regime [40, 50–52]. Since a finite Hall
                                                                          then be obtained through the quasi-adiabatic expansion [38]:
viscosity requires broken time-reversal symmetry (TRS), it
has often been investigated as a response to an external
                                                                                                   
                                                                                              𝛿H𝒌       𝛿 ⟨H𝒌 ⟩ Õ (𝑏)
                                                                                     𝑇𝑖 𝑗 =           =         +      Ω𝑖 𝑗 𝑘𝑙 ( 𝒌) 𝜕𝑡 𝜀 𝑘𝑙 ,       (4)
magnetic field [43, 45–47]. For instance, in a 2D isotropic                                   𝛿𝜀𝑖 𝑗      𝛿𝜀 𝑖 𝑗   𝑘𝑙,𝑏
system subjected to a magnetic field, the only allowed non-
zero element is 𝜂 𝐻𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦 𝑦 𝑥 𝑦 , corresponding to the stress-
                                𝐻                                         from which we readily identify the Hall viscosity
strain relationship shown in Fig. 1(b). By symmetry, a
                                                                                                 ℏÕ
ferromagnet must display the same non-zero element, but                                𝜂𝑖𝐻𝑗 𝑘𝑙 =      𝑓 (𝜉𝒌𝑏 ) Ω𝑖(𝑏)  (
                                                                                                                  𝑗 𝑘𝑙 𝒌) ,                        (5)
at zero applied field, corresponding to an anomalous Hall                                        𝑉
                                                                                                         𝒌𝑏
viscosity. However, there are other ordered phases that break
                                                                          and the strain-space Berry curvature
TRS, such as antiferromagnetic and altermagnetic orders.
While the combination of time-reversal and translational (or
                                                                                                                                                    
                                                                          Ω𝑖(𝑏)
                                                                             𝑗 𝑘𝑙
                                                                                  ( 𝒌) = 𝑖   𝜕 𝜀𝑖𝑗 𝑢 𝒌,𝑏 | 𝜕 𝜀 𝑘𝑙 𝑢 𝒌,𝑏 − 𝜕 𝜀 𝑘𝑙 𝑢 𝒌,𝑏 | 𝜕 𝜀𝑖𝑗 𝑢 𝒌,𝑏
inversion) symmetries enforce 𝜂𝑖𝐻𝑗 𝑘𝑙 = 0 in antiferromagnets,
the symmetries of altermagnetism are generally compatible                                        Õ 𝛾 𝑖 𝑗′ ( 𝒌) ∗ 𝛾 𝑘𝑙′ ( 𝒌)
                                                                                                     𝑏𝑏           𝑏𝑏
with finite Hall viscosity tensor elements at zero fields.                             = 2Im                                  ,                    (6)
                                                                                                𝑏′ ≠𝑏    (𝜉𝒌𝑏 − 𝜉𝒌𝑏′ ) 2
   To show this, we employ group theory to decompose the
15-dimensional reducible representation consisting of the non-            where 𝑉 is the volume and 𝑓 is the Fermi-Dirac distribution.
zero elements of 𝜂𝑖𝐻𝑗 𝑘𝑙 into irreducible representations (irreps)        In Ref. [55], we derive this result without invoking the quasi-
of the point group describing the paramagnetic phase. This                adiabatic approximation. In order for the Hall viscosity in
task is greatly simplified by expressing 𝜂𝑖𝐻𝑗 𝑘𝑙 in terms of the so-      Eq. (6) to be finite, H𝒌, 𝜀 must not commute with H𝒌,0 ,
                                                                                       𝑖𝑗
called Jahn symbols [53] as 𝑎 𝑉 2 𝑉 2 [54]. For example,                  otherwise 𝛾𝑏′ 𝑏 is diagonal. Moreover, SOC must be present
                                      

in a tetragonal system with point group 𝐷 4ℎ , we find:                   to induce local Berry curvature. To elucidate the microscopic
                                                                          properties that govern Ω𝑖(𝑏)
                                                                                                    𝑗 𝑘𝑙 , we compute it in minimal models
                      −      −      −      −
                                              ⊕ 4𝐸 𝑔− ,
         2  2
   𝑎      𝑉 𝑉      → 𝐴1𝑔 ⊕ 2𝐴2𝑔 ⊕ 2𝐵1𝑔 ⊕ 2𝐵2𝑔                       (3)   for tetragonal 𝑑-wave and hexagonal 𝑔-wave altermagnets.
                                                                                                                                                            3

   Tetragonal 𝑑-wave altermagnets: The Lieb lattice model
of Ref. [6] (see also [7, 56]) provides a convenient description
of a 𝑑-wave altermagnet on the tetragonal lattice (irrep 𝐵2𝑔 − ),

being realized in materials of the families 𝑅 2 Mn2 Se2 O3 [57–
59], 𝐴V2 Te2 O [22, 60–62] and Fe2 𝑋 2 O (𝑋=Cl, Br, I) [63].
The model shown in Fig. 2 (a) has non-magnetic atoms on
the sites of a square lattice and magnetic atoms on the bond
centers with opposite out-of-plane spins related by a 90◦ crystal
rotation. The strain-free Hamiltonian is thus invariant under a
combination of a 90◦ rotation and time-reversal [6, 7]

       H𝒌,0 = 𝜀 0,𝒌 + 𝑡1,𝒌 𝜏1 + 𝑡3,𝒌 𝜏3 + 𝜆®𝒌 · 𝜎
                                                ® 𝜏2 + 𝐽𝜙𝜏3 𝜎3 ,       (7)

with sublattice and spin-space Pauli matrices 𝜏𝑖 and 𝜎𝑖 ,
respectively. The first three terms depend on the hopping
parameters shown in Fig. 2 (a) through 𝜀0,𝒌 = −𝑡2 𝑓0,𝒌 ,
𝑡 1,𝒌 = −𝑡1 𝑓1,𝒌 , and 𝑡 3,𝒌 = −𝑡 𝑑 𝑓3,𝒌 , with 𝑡 2 = (𝑡2𝑎 + 𝑡2𝑏 )/2 and
                                                                       𝑘
𝑡 𝑑 = (𝑡 2𝑎 − 𝑡2𝑏 )/2, and lattice harmonics      𝑓1,𝒌 = 4 cos 𝑘2𝑥 cos 2𝑦
and 𝑓0(3) ,𝒌 = 2 cos 𝑘 𝑥 ± cos 𝑘 𝑦 . The SOC term has the
                                       
                                    𝑘
simple form 𝜆®𝒌 = 𝜆 sin 𝑘2𝑥 sin 2𝑦 𝒛ˆ and 𝜙 is the altermagnetic
order parameter. The symmetry-allowed strain Hamiltonian
contains the three distinct in-plane strain irreps of the
tetragonal group (see also [11, 64])

                                        
                       (𝐴 )                  (𝐵 )           (𝐵 )
H𝒌, 𝜀 = 𝜀 𝑥 𝑥 + 𝜀 𝑦 𝑦 𝛾𝒌 1𝑔 + 𝜀 𝑥 𝑥 − 𝜀 𝑦 𝑦 𝛾𝒌 1𝑔 + 2𝜀 𝑥 𝑦 𝛾𝒌 2𝑔
                                                               (8)            FIG. 2. (a) Lieb-lattice model for 𝑑-wave altermagnetism [6] and
with coupling matrices:                                                       (b) the corresponding band structure with bands labeled by (1,2,3,4).
                                                                              Pink and blue refer to spin up and down states, respectively. The
     ( 𝐴1𝑔 )    (𝐴 )              (𝐴 )          (𝐴 )
    𝛾𝒌       = 𝑔0 1𝑔 𝑓0,𝒌 𝜏0 + 𝑔1 1𝑔 𝑓1,𝒌 𝜏1 + 𝑔3 1𝑔 𝑓3,𝒌 𝜏3 ,                solid (dashed) lines correspond to non-zero (zero) SOC. The Dirac
                                                                              points are located along the green dashed lines. (c) Strain-space Berry
     ( 𝐵1𝑔 )
    𝛾𝒌       = 2𝑔 ( 𝐵1𝑔 ) 𝜏3 ,                                                curvature elements of the second band, (c) 21 (Ω 𝑥(2)𝑥 𝑥 𝑦 + Ω 𝑦𝑦   (2)
                                                                                                                                                     𝑥 𝑦 ) and
                                                                                    1    (2)         (2)                            1
     ( 𝐵2𝑔 )                   𝑘𝑥    𝑘𝑦                                       (d) 2 (Ω 𝑥 𝑥 𝑥 𝑦 − Ω 𝑦𝑦 𝑥 𝑦 ). (e) Hall viscosity 𝜂 ≡ 2 (𝜂 𝑥 𝑥 𝑥 𝑦 + 𝜂 𝑦𝑦
                                                                                                                                 𝐻       𝐻           𝐻
                                                                                                                                                         𝑥𝑦) =
    𝛾𝒌       = −2𝑔 ( 𝐵2𝑔 ) sin    sin 𝜏1 .                     (9)
                               2     2                                        𝜂 𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦𝑦 𝑥 𝑦 as a function of the chemical potential and (f) of the
                                                                                𝐻           𝐻

                                                                              altermagnetic order parameter 𝜙 at 𝜇 = 0. Here, 𝑣 uc is the unit cell
Here, 𝑔𝑖(Γ) are coupling constants with magnitudes comparable                 volume. The values of the tight binding parameters used here are
to the hopping parameters [11]. The electronic dispersion of                  shown in the SM [55].
H𝒌,0 has four spin-polarized Dirac points at the Brillouin zone
boundaries for |𝜙| < 𝜙 𝑐 = |4𝑡 𝑑 /𝐽 |, which are gapped by SOC,
as shown by the green lines at momenta at 𝒌 ∗,1 and 𝒌 ∗,2 in                  curvature can be uniquely employed to disentangle the intrinsic
Fig. 2 (b). Being sources of large Berry curvature, these                     multipolar structure of the Berry curvature of altermagnets.
gapped Dirac points determine not only the behavior of the                    Using Eq. (5), these results give 𝜂 𝐻     𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦 𝑦 𝑥 𝑦 ≠ 0, in
                                                                                                                                    𝐻

momentum-space Berry curvature quadrupole [6, 11, 35, 65],                    agreement with our group-theory analysis. Moreover, as
but also the properties of the strain-space Berry curvature of                shown in Fig. 2 (e) and (f), not only is 𝜂 𝐻 proportional to
Eq. (5). The latter, in turn, gives the non-zero Hall viscosity               the altermagnetic order parameter 𝜙, but it also is the largest
tensor elements in the altermagnetic phase, which according                   for the chemical potential values for which the system is in
to our group theory analysis are 𝜂 𝐻              𝐻                           the insulating phase. This demonstrates the suitability of
                                      𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦 𝑦 𝑥 𝑦 ≠ 0.
                                                                              exploiting the Hall viscosity to measure altermagnetic order
   Figs. 2 (c)-(d) show 21 (Ω 𝑥(2)𝑥 𝑥 𝑦 ± Ω 𝑦(2)𝑦 𝑥 𝑦 ), respectively,        in insulators.
computed at the second band in Fig. 2 (b). Both show large                       To gain further insights into the topological origin of the
local Berry curvature values near the gapped Dirac points at                  Hall viscosity, we expand the Hamiltonian around the Dirac
𝒌 ∗,1 and 𝒌 ∗,2 . While for Ω 𝑥(2)𝑥 𝑥 𝑦 + Ω 𝑦(2)𝑦 𝑥 𝑦 these values have the   points labeled by valley 𝜅 = ±1 and spin 𝜎 =↑, ↓, as shown in
same sign near all Dirac points, resulting in a Berry curvature               Fig. 3(a). Inclusion of SOC leads to the characteristic Dirac
monopole, for Ω 𝑥(2)𝑥 𝑥 𝑦 −Ω 𝑦(2)𝑦 𝑥 𝑦 the Berry curvature changes sign       Hamiltonian (see [55]):
under a 90◦ rotation, resulting in a Berry curvature quadrupole
consistent with the quadrupolar structure of the momentum-
                                                                                             Õ 
                                                                                                    𝑣 𝑖𝜎,𝜅 𝑝 𝑖 − A𝑖𝜎,𝜅 𝛼𝑖𝜎 + 𝑚 𝜎 𝛽             (10)
                                                                                                                      
                                                                                     H=
space Berry curvature Ω̃ 𝑥 𝑦 [11]. Thus, the strain-space Berry                             𝜎,𝜅 ,𝑖=𝑥,𝑦
                                                                                                                                                            4

                                        (b)
(a)                                           50                                     Hexagonal 𝑔-wave altermagnets: The tetragonal 𝑑-wave
                                              40                                 altermagnet studied above is essentially a 2D model. In
                                              30                                 contrast, 𝑔-wave altermagnetism in hexagonal lattices, as
                                              20
                                                                                 realized in CrSb [73–76], MnTe [77–81], and Co1/4 NbSe2 [82–
                                              10
                                                                                 85], is intrinsically 3D. To investigate their Hall viscosity, we
                                              0
                                                  -6   -4   -2   0   2   4   6   adopt the minimal model of Ref. [7], with point group 𝐷 6ℎ . As
                                                                                 illustrated in Fig. 4 (a), the two magnetic atoms are not on the
                                                                                 same plane, but are related by a sixfold screw rotation, i.e., a
FIG. 3. (a) The four spin-polarized Dirac points of the Lieb lattice             sixfold rotation followed by a half-translation along the 𝑧-axis.
model are located at the Brillouin zone boundaries when |𝜙| < 𝜙 𝑐 .
                                                                                 The Hamiltonian H𝒌,0 has the same form of Eq. (7), but the
They are labeled by their spin (𝜎 =↑, ↓) and valley (𝜅 = ±1) quantum
numbers (𝜎,𝜅). (b) Comparison between the Hall viscosity 𝜂 𝐻 =                   functions depend explicitly on 𝑘 𝑧 and the SOC term 𝜆®𝒌 has
 𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦𝑦 𝑥 𝑦 from the full tight-binding model (pink solid line)
𝜂𝐻           𝐻                                                                   in-plane components (see the Supplementary Material [55]).
and from the Dirac theory of Eq. (12) (blue dashed line). For the                   We focus on moments aligned along the 𝑧-axis, relevant for
parameters values used here, see the SM [55].
                                                                                 CrSb and Co1/4 NbSe2 , in which case the altermagnetic order
                                                                                 parameter 𝜙 in Eq. (7) transforms as the 𝐵1𝑔        − irrep of 𝐷 .
                                                                                                                                                  6ℎ
with Dirac matrices 𝛼𝑖𝜎 and 𝛽, velocities 𝑣 𝑖𝜎,𝜅 , and SOC-                      This gives spin-split nodal planes along 𝑘 𝑧 = 0 and 𝑘 𝑦 = 0 (and
                         p                                                       symmetry-related planes), which are partially gapped by SOC,
generated mass 𝑚 𝜎 = 𝜎𝜆 1 − 𝜙/𝜙 𝑐 . Crucially, strain appears
                                                                                 as shown in the electronic dispersion of Fig. 4 (b). In this case,
as an electromagnetic gauge field with
                                                                                 our group-theory analysis predicts non-zero Hall viscosity
                   𝜀 𝑥 𝑥 ± 𝜀 𝑦 𝑦 ∝ A ↑,𝜅  ↓,𝜅
                                     𝑥 ∓ A𝑦 ,
                                                                                 tensor components 𝜂 𝐻  𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦 𝑦 𝑥𝑧 = −𝜂 𝑥 𝑦 𝑦𝑧 . We therefore
                                                                                                                    𝐻           𝐻
                                                                                                                       𝑖𝑗
                                                                                 consider the coupling matrices 𝛾𝑏′ 𝑏 in H𝒌, 𝜀 associated with
                          𝜀 𝑥 𝑦 ∝ A ↑,𝜅  ↓,𝜅
                                    𝑦 + A𝑥 .                             (11)
                                                                                 the in-plane and out-of-plane shear strains, (𝜀 𝑥 𝑥 − 𝜀 𝑦 𝑦 , 𝜀 𝑥 𝑦 )
This is analogous to the emergent magnetic fields in graphene                    and (𝜀 𝑥𝑧 , 𝜀 𝑦𝑧 ).
arising from static but spatially varying strain [66, 67]. In our                     Fig. 4 (c) displays our results for 12 (Ω 𝑥(4)𝑥 𝑥𝑧 − Ω 𝑦(4)𝑦 𝑥𝑧 ) along
case, because the strain is dynamic and the system is in the                     the 𝑘 𝑧 = 0 plane, regularized for clearer presentation (see SM)
altermagnetic phase, the gauge fields correspond to emergent                     and calculated at the band 4 highlighted in Fig. 4 (b). This
electrical fields, like in Refs. [68–71], which are however spin-                Berry curvature component is even with respect to reflections
dependent. As a result, the Hall viscosity can be expressed in                   along the 𝑘 𝑥 and 𝑘 𝑦 mirrors, and thus averages to a finite
terms of the Hall conductivity 𝜎𝑥𝐻𝑦 (of unit charge 𝑒 = 1) of a                  value. Fig. 4 (d) shows the behavior of the in-plane integrated
single Dirac point as:                                                           Berry curvature as a function of 𝑘 𝑧 , 21 ( Ω̄ 𝑥(4)𝑥 𝑥𝑧 − Ω̄ 𝑦(4)𝑦 𝑥𝑧 ) where
                                                                                 Ω̄ 𝑥(4)𝑥 ( 𝑦 𝑦) 𝑥𝑧 (𝑘 𝑧 ) = 𝑘 ,𝑘 Ω 𝑥(4)𝑥 ( 𝑦 𝑦) 𝑥𝑧 ( 𝒌). Its sudden change
                                      (                                                                     ∫
    𝐻           𝐻             𝐻     𝐶0 sign(𝑚)     if 𝜇𝑟2 < 𝑚 2
                                                              2 , (12)
                                           4𝜋                                                             𝑥   𝑦
  𝜂 𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦 𝑦 𝑥 𝑦 = 𝐶0 𝜎𝑥 𝑦 =        𝑚            2
                                    ℏ   4 𝜋 | 𝜇𝑟 | if 𝜇𝑟 > 𝑚                     around 2𝑘𝜋𝑧 ≈ 0.25 originates from a Lifshitz transition of the
                                                                                 Fermi surface, which in turn is manifested as sudden changes of
where 𝜇𝑟 is the chemical potential relative to the Dirac point,                  the Hall viscosity 𝜂 𝐻
                                                                                                      𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦 𝑦 𝑥𝑧 as a function of the chemical
                                                                                                                  𝐻
        p                                   (𝐴 )
𝑚 = 𝜆 1 − 𝜙/𝜙 𝑐 and 𝐶0 = 8ℏ2 𝑔 ( 𝐵2𝑔 ) 𝑔3 1𝑔 /(𝑣 uc 𝑡 1 𝑡 𝑑 ). As                potential 𝜇 in Fig. 4(e), thus showcasing the sensitivity of
shown in Fig. 3(b), this expression is in quantitative agreement                 the Hall viscosity to the topology of the band structure (a
with the full tight-binding calculation of the Hall viscosity, at                detailed analysis is shown in [55]). Importantly, a non-zero
least for small SOC-induced gap [72]. We emphasize that                          𝜂 𝐻 requires the strain Hamiltonian to also modify the SOC.
Eq. (12) does not imply that the system has an anomalous                         Without such a strain-induced SOC term, we find a vanishing
Hall conductivity; instead, it simply expresses the fact that                    Hall viscosity. Finally, Fig. 4(f) directly demonstrates the
the anomalous Hall viscosity is proportional to the anomalous                    proportionality between the anomalous Hall viscosity and the
Hall conductivity of a single Dirac point, generated by the                      altermagnetic order parameter 𝜙.
emergent gauge fields of Eq. (11). Once the contributions of                        Discussion : The calculated Hall viscosity 𝜂 𝐻 in Fig. 2(e)
all Dirac points are added, only the anomalous Hall viscosity                    and Fig. 4(e) acquires values of the order of 10 ℏ/𝑣 uc which,
survives.                                                                        taking a typical unit cell volume 𝑣 uc = 𝑎 30 with 𝑎 0 = 5Å, gives
   It is also instructive to express Eq. (2) in terms of the
                                                                                 𝜂 𝐻 ∼ 8.15 𝜇Pa · s. These are comparable to the values recently
emergent gauge fields:
                                                                                 reported in 𝛼-RuCl3 under an external magnetic field [49],
                         Õ ∫                                                     measured through the acoustic Faraday effect [49, 86–89]. In
                     𝐻
             𝑆eff = 𝜎𝑥 𝑦   𝜎      𝜖𝑖 𝑗 A𝑖𝜎,𝜅 𝜕𝑡 A 𝜎,𝜅
                                                  𝑗   ,       (13)               a hexagonal system like 𝛼-RuCl3 , this effect arises because the
                         𝜎,𝜅      𝑥,𝑡
                                                                                                       𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦 𝑦 𝑥 𝑦 generated by the magnetic
                                                                                 Hall viscosity term 𝜂 𝐻            𝐻

with 𝜖 𝑖 𝑗 the 2D Levi-Civita symbol. This action is noting                      field lifts the degeneracy of the transverse acoustic waves
but the temporal version of two Chern-Simons actions with                        propagating along the 𝑐-axis, which results in a rotation of
opposite Hall conductivities for the two spin sectors, ensuring                  the circular polarization of an incident transverse strain wave.
a vanishing Hall conductivity but a finite Hall viscosity.                       In a hexagonal 𝑔-wave altermagnet like CrSb, however, the
                                                                                                                                                     5

(a)                                 (b)                                           altermagnets through the Hall viscosity, which in turn can be
                                              4                                   measured via magneto-acoustic measurements that are similar
                               Cr (A)         3                                   to the conventional acoustic Faraday effect. Microscopically,
                               Cr (B)         2
                                                        4                         we demonstrated that because the Hall viscosity is governed by
                               Sb
                                              1
                                                    3                             the strain-space Berry curvature, it becomes highly sensitive
                                                                                  to the underlying electronic structure, being strongly enhanced
                                              0
                                                  1 2
                                              1

                                                                                  near SOC-gapped Dirac crossings, Lifshitz transitions, and
                                                            M   K
                                                                                  other band-structure singularities.
(c)                                 (d)
                                                                                     These results highlight that the Hall viscosity probes not
                                                                                  only symmetry breaking, but also the topological properties
                                                                                  of altermagnets. Often, the latter are described in terms
                                                                                  of the properties of the momentum-space Berry curvature,
                                                                                  which in altermagnets has a multipolar structure. While the
                                                                                  magnetic moment direction or strain can distort it to produce
                                                                                  a net nonzero momentum-space Berry curvature, the resulting
                                                                                  anomalous Hall conductivity can only be measured in metallic
                                                                                  or weakly semiconducting materials. In contrast, the strain-
(e)                                     (f)                                       space Berry curvature displays a monopole structure even in
      60                                                                          unstrained pure altermagnets, and the resulting phonon Hall
      30
                                                                                  viscosity can be measured also in insulators, which comprise
       0
                                                                                  the vast majority of altermagnetic material candidates.
      -30

      -60
                                                                                     Acknowledgments: We are grateful to P. Brouwer, W. J.
            -3   -2   -1   0   1
                                                                                  Meese, D. J. Schultz, J. Sinova, S. Sorn, D. Valentinis,
                                                                                  and J. Venderbos for helpful discussions. I.J. and J.S.
                                                                                  were supported by the German Research Foundation TRR
FIG. 4. (a) Hexagonal lattice model for 𝑔-wave altermagnetism.                    288-422213477 ELASTO-Q-MAT, Project A07.                   R.A.
Open and closed symbols refer to atoms away and at the 𝑧 = 0                      acknowledges partial support from the Brazilian agencies
plane, respectively. (b) Band structure of the model with band labels             CNPq through a postdoctoral fellowship (Proc. 201212/2025-
(1,2,3,4); the inset shows the first Brillouin zone. Solid and dashed             0) and from FAPESP (Grant No. 2023/05765-7). R.M.F.
lines represent the cases with and without SOC, respectively; note                acknowledges support from the Research Corporation for
that, without SOC, there is no spin-splitting at 𝑘 𝑧 = 0. The values of           Science Advancement through the Cottrell SEED Award CS-
the parameters used here are given in the SM [55]. (c) Berry curvature
                                                                                  SEED-2025-012 and a Mercator Fellowship from the German
component (Ω 𝑥(4)𝑥 𝑥𝑧 − Ω 𝑦𝑦   (4)
                                  𝑥𝑧 )/2. (d) 𝑘 𝑧 -dependence of the Berry
               (4)         (4)                                                    Research Foundation (DFG) through Grant No. TRR 288,
curvature ( Ω̄ 𝑥 𝑥 𝑥𝑧 − Ω̄ 𝑦𝑦 𝑥𝑧 )/2 integrated over the in-plane momenta.
                                                                                  422213477 Elasto-Q-Mat.
(e) Hall viscosity 𝜂 𝐻 = 𝜂 𝐻    𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦𝑦 𝑥𝑧 as a function of the chemical
                                            𝐻

potential 𝜇 and (f) of the altermagnetic order parameter 𝜙 for fixed
𝜇/𝑡 1 = 0.5.


                                                                                   [1] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond conventional
zero-field Hall viscosity term 𝜂 𝐻                                                     ferromagnetism and antiferromagnetism: A phase with
                                     𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦 𝑦 𝑥𝑧 does not mix
                                                 𝐻
                                                                                       nonrelativistic spin and crystal rotation symmetry, Phys. Rev.
the 𝑐-axis sound waves. Nevertheless, one can still exploit
                                                                                       X 12, 031042 (2022).
the near-degeneracy of the transverse modes propagating                            [2] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging Research
along a direction that is tilted slightly away from the 𝑐-axis.                        Landscape of Altermagnetism, Phys. Rev. X 12, 040501 (2022).
Because sound propagation is birefringent along this direction,                    [3] T. Jungwirth, R. M. Fernandes, E. Fradkin, A. H. MacDonald,
the linear polarization of an incident transverse wave will                            J. Sinova, and L. Å mejkal, Altermagnetism: An unconventional
generally rotate even in the paramagnetic phase. However,                              spin-ordered phase of matter, Newton 1, 100162 (2025).
the combination of near-degenerate sound velocities with the                       [4] T. Jungwirth, J. Sinova, R. M. Fernandes, Q. Liu, H. Watanabe,
                                                                                       S. Murakami, S. Nakatsuji, and L. Å mejkal, Symmetry,
                 𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦 𝑦 𝑥𝑧 ensures that the altermagnetic
form factor of 𝜂 𝐻           𝐻
                                                                                       microscopy and spectroscopy signatures of altermagnetism,
contribution to the polarization rotation becomes sizable. A                           Nature 649, 837 (2026).
full analysis of magneto-acoustic setups that can be used to                       [5] Y. Fang, J. Cano, and S. A. A. Ghorashi, Quantum Geometry
probe the Hall viscosity of magnetically ordered states will be                        Induced Nonlinear Transport in Altermagnets, Phys. Rev. Lett.
presented elsewhere [90].                                                              133, 106701 (2024).
                                                                                   [6] D. S. Antonenko, R. M. Fernandes, and J. W. F. Venderbos,
   In summary, we have established the anomalous Hall                                  Mirror chern bands and weyl nodal loops in altermagnets, Phys.
viscosity as a natural bulk geometric response of altermagnets.                        Rev. Lett. 134, 096703 (2025).
Our group-theory analysis enables one to distinguish                               [7] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F. Agterberg,
between ferromagnets, conventional antiferromagnets, and                               Minimal models for altermagnetism, Phys. Rev. B 110, 144412
                                                                                                                                             6

     (2024).                                                             [27] P. A. McClarty and J. G. Rau, Landau Theory of
 [8] P. Rao, A. Mook, and J. Knolle, Tunable band topology and                Altermagnetism, Phys. Rev. Lett. 132, 176702 (2024).
     optical conductivity in altermagnets, Phys. Rev. B 110, 024425      [28] K. V. Yershov, V. P. Kravchuk, M. Daghofer, and J. van den
     (2024).                                                                  Brink, Fluctuation-induced piezomagnetism in local moment
 [9] K. Parshukov, R. Wiedmann, and A. P. Schnyder, Topological               altermagnets, Phys. Rev. B 110, 144421 (2024).
     responses from gapped Weyl points in 2D altermagnets,               [29] L. Attias, A. Levchenko, and M. Khodas, Intrinsic anomalous
     arXiv:2403.09520 (2024).                                                 Hall effect in altermagnets, Phys. Rev. B 110, 094425 (2024).
[10] T. Farajollahpour, R. Ganesh, and K. Samokhin, Light-induced        [30] A. R. Chakraborty, J. Schmalian, and R. M. Fernandes,
     charge and spin Hall currents in materials with C4 K symmetry,           Magnetic-field-tuned       randomness      in    inhomogeneous
     npj Quantum Materials 10, 29 (2025).                                     altermagnets, Phys. Rev. B 112, 035146 (2025).
[11] K. Takahashi, C. R. W. Steward, M. Ogata, R. M. Fernandes,          [31] Y. Jiang, X. Zhang, H. Bai, Y. Tian, B. Zhang, W.-J. Gong,
     and J. Schmalian, Elasto-Hall conductivity and the anomalous             and X. Kong, Strain-engineering spin-valley locking effect in
     Hall effect in altermagnets, Phys. Rev. B 111, 184408 (2025).            altermagnetic monolayer with multipiezo properties, Applied
[12] N. Nagaosa, J. Sinova, S. Onoda, A. H. MacDonald, and N. P.              Physics Letters 126 (2025).
     Ong, Anomalous Hall effect, Rev. Mod. Phys. 82, 1539 (2010).        [32] H. Schiff, P. McClarty, J. G. Rau, and J. Romhányi, Collinear
[13] L. Å mejkal, A. H. MacDonald, J. Sinova, S. Nakatsuji, and               altermagnets and their landau theories, Phys. Rev. Res. 7, 033301
     T. Jungwirth, Anomalous hall antiferromagnets, Nature Reviews            (2025).
     Materials 7, 482 (2022).                                            [33] M. Hu, X. Cheng, Z. Huang, and J. Liu, Catalog of 𝐶-paired
[14] L. Šmejkal, R. GonzÃ¡lez-HernÃ¡ndez, T. Jungwirth,                       spin-momentum locking in antiferromagnetic systems, Phys.
     and      J.   Sinova,      Crystal     time-reversal   symmetry          Rev. X 15, 021083 (2025).
     breaking and spontaneous hall effect in collinear                   [34] B. Karetta, X. H. Verbeek, R. Jaeschke-Ubiergo, L. Šmejkal,
     antiferromagnets, Science Advances 6, eaaz8809 (2020),                   and J. Sinova, Strain-controlled 𝑔- to 𝑑-wave transition in
     https://www.science.org/doi/pdf/10.1126/sciadv.aaz8809.                  altermagnetic crsb, Phys. Rev. B 112, 094454 (2025).
[15] K. P. Kluczyk, K. Gas, M. J. Grzybowski, P. Skupiński,              [35] H. Radhakrishnan, B. Bell, C. Ortix, and J. Venderbos,
     M. A. Borysiewicz, T. Fas, J. Suffczyński, J. Z. Domagala,               Topological piezomagnetic effect in two-dimensional dirac
     K. Grasza, A. Mycielski, M. Baj, K. H. Ahn, Výborný,                     quadrupole altermagnets, arXiv:2602.05894 (2026).
     M. Sawicki, and M. Gryglas-Borysiewicz, Coexistence of              [36] M. Khodas, S. Mu, I. I. Mazin, and K. D. Belashchenko, Tuning
     anomalous Hall effect and weak magnetization in a nominally              of altermagnetism by strain, Phys. Rev. B 113, 104422 (2026).
     collinear antiferromagnet MnTe, Phys. Rev. B 110, 155201            [37] R. Ohlendorf, L. Buiarelli, H. M. Noad, A. P. Mackenzie,
     (2023).                                                                  R. M. Fernandes, T. Birol, J. Schmalian, and E. Gati, Probing
[16] L. Attias, A. Levchenko, and M. Khodas, Intrinsic anomalous              multipolar order in the candidate altermagnet MnF2 through the
     Hall effect in altermagnets, Phys. Rev. B 110, 094425 (2024).            elastocaloric effect under strain, arXiv:2601.19343 (2026).
[17] M. Roig, Y. Yu, R. C. Ekman, A. Kreisel, B. M.                      [38] J. E. Avron, R. Seiler, and P. G. Zograf, Viscosity of quantum
     Andersen, and D. F. Agterberg, Quasisymmetry-constrained                 Hall fluids, Phys. Rev. Lett. 75, 697 (1995).
     spin ferromagnetism in altermagnets, Phys. Rev. Lett. 135,          [39] M. Barkeshli, S. B. Chung, and X.-L. Qi, Dissipationless phonon
     016703 (2025).                                                           Hall viscosity, Phys. Rev. B 85, 245107 (2012).
[18] A. Osin, A. Levchenko, and M. Khodas, Extrinsic anomalous           [40] B. Bradlyn, M. Goldstein, and N. Read, Kubo formulas for
     Hall effect in altermagnets, arXiv:2511.03151 (2025).                    viscosity: Hall viscosity, Ward identities, and the relation with
[19] Y. Guo, H. Liu, O. Janson, I. C. Fulga, J. van den Brink, and            conductivity, Phys. Rev. B 86, 245309 (2012).
     J. I. Facio, Spin-split collinear antiferromagnets: A large-scale   [41] T. Qin, J. Zhou, and J. Shi, Berry curvature and the phonon Hall
     ab-initio study, Mater. Today Phys. 32, 100991 (2023).                   effect, Phys. Rev. B 86, 104305 (2012).
[20] J. Sødequist and T. Olsen, Two-dimensional altermagnets             [42] H. Shapourian, T. L. Hughes, and S. Ryu, Viscoelastic response
     from high throughput computational screening: Symmetry                   of topological tight-binding models in two and three dimensions,
     requirements, chiral magnons, and spin-orbit effects, Applied            Phys. Rev. B 92, 165131 (2015).
     Physics Letters 124 (2024).                                         [43] T. Saito, K. Misaki, H. Ishizuka, and N. Nagaosa, Berry phase
[21] X. Wan, S. Mandal, Y. Guo, and K. Haule, High-throughput                 of phonons and thermal Hall effect in nonmagnetic insulators,
     search for metallic altermagnets by embedded dynamical mean              Phys. Rev. Lett. 123, 255901 (2019).
     field theory, Phys. Rev. Lett. 135, 106501 (2025).                  [44] B. S. Kim, Modeling Hall viscosity in magnetic-skyrmion
[22] H.-Y. Ma, M. Hu, N. Li, J. Liu, W. Yao, J.-F. Jia,                       systems, Phys. Rev. Res. 2, 013268 (2020).
     and J. Liu, Multifunctional antiferromagnetic materials with        [45] M. Ye, L. Savary, and L. Balents, Phonon Hall viscosity in
     giant piezomagnetism and noncollinear spin current, Nature               magnetic insulators, arXiv:2103.04223 (2021).
     communications 12, 2846 (2021).                                     [46] Y. Zhang, Y. Teng, R. Samajdar, S. Sachdev, and M. S. Scheurer,
[23] S. Bhowal and N. A. Spaldin, Ferroically ordered magnetic                Phonon Hall viscosity from phonon-spinon interactions, Phys.
     octupoles in 𝑑-wave altermagnets, Phys. Rev. X 14, 011019                Rev. B 104, 035103 (2021).
     (2024).                                                             [47] B. Flebus and A. H. MacDonald, Phonon Hall viscosity of ionic
[24] C. R. W. Steward, R. M. Fernandes, and J. Schmalian, Dynamic             crystals, Phys. Rev. Lett. 131, 236301 (2023).
     paramagnon-polarons in altermagnets, Phys. Rev. B 108, 144418       [48] H.-L. Kim, T. Saito, H. Yang, H. Ishizuka, M. J. Coak, J. H.
     (2023).                                                                  Lee, H. Sim, Y. S. Oh, N. Nagaosa, and J.-G. Park, Thermal Hall
[25] R. M. Fernandes, V. S. de Carvalho, T. Birol, and R. G. Pereira,         effects due to topological spin fluctuations in YMnO3 , Nature
     Topological transition from nodal to nodeless Zeeman splitting           Communications 15, 243 (2024).
     in altermagnets, Phys. Rev. B 109, 024404 (2024).                   [49] A. Shragai, E. Horsley, S. Kim, Y.-J. Kim, and B. Ramshaw,
[26] T. Aoyama and K. Ohgushi, Piezomagnetic properties in                    Phonon Hall viscosity and the intrinsic thermal Hall effect of
     altermagnetic MnTe, Phys. Rev. Mat. 8, L041402 (2024).                   𝛼-RuCl3 , Nature 652, 1166 (2026).
                                                                                                                                               7

[50] M. Müller, J. Schmalian, and L. Fritz, Graphene: A nearly           [70] A. Cortijo, Y. Ferreirós, K. Landsteiner, and M. A. Vozmediano,
     perfect fluid, Phys. Rev. Lett. 103, 025301 (2009).                      Visco elasticity in 2d materials, 2D Materials 3, 011002 (2016).
[51] J. M. Link, P. P. Orth, D. E. Sheehy, and J. Schmalian, Universal   [71] Y. Ferreiros and M. A. H. Vozmediano, Elastic gauge fields
     collisionless transport of graphene, Phys. Rev. B 93, 235447             and Hall viscosity of dirac magnons, Phys. Rev. B 97, 054404
     (2016).                                                                  (2018).
[52] A. A. Herasymchuk, E. V. Gorbar, and P. O. Sukhachov,               [72] Notice that whenever the chemical potential lies within the gap of
     Viscoelastic tensor and hydrodynamics of altermagnets, Phys.             the Dirac spectrum, the Hall viscosity is independent of both the
     Rev. B 112, 075150 (2025).                                               order parameter 𝜙 and the spin-orbit coupling 𝜆. However, the
[53] H. Jahn, Note on the Bhagavantam–Suranarayana method                     limit 𝜙 → 0 cannot be taken, since well-separated Dirac points
     of enumerating the physical constants of crystals, Acta                  exist only for sufficiently large values of the order parameter.
     Crystallographica 2, 30 (1949).                                     [73] J. Ding, Z. Jiang, X. Chen, Z. Tao, Z. Liu, T. Li, J. Liu, J. Sun,
[54] 𝑉 stands, as usual, for a polar vector, square brackets imply a          J. Cheng, J. Liu, Y. Yang, R. Zhang, L. Deng, W. Jing, Y. Huang,
     symmetric combination, curly brackets imply an anti-symmetric            Y. Shi, M. Ye, S. Qiao, Y. Wang, Y. Guo, D. Feng, and D. Shen,
     combination, and 𝑎 denotes time reversal.                                Large band splitting in 𝑔-wave altermagnet CrSb, Phys. Rev.
[55] See              Supplemental               Material           at        Lett. 133, 206401 (2024).
     https://journals.aps.org/authors/supplemental-material-             [74] G. Yang, Z. Li, S. Yang, J. Li, H. Zheng, W. Zhu, Z. Pan, Y. Xu,
     instructions for details of tight binding model of the hexagonal         S. Cao, W. Zhao, A. Jana, J. Zhang, M. Ye, Y. Song, L.-H.
     system and acoustic Faraday effect.                                      Hu, L. Yang, J. Fujii, I. Vobornik, M. Shi, H. Yuan, Y. Zhang,
[56] B. Brekke, A. Brataas, and A. Sudbø, Two-dimensional                     Y. Xu, and Y. Liu, Three-dimensional mapping and electronic
     altermagnets: Superconductivity in a minimal microscopic                 origin of large altermagnetic splitting near Fermi level in CrSb,
     model, Phys. Rev. B 108, 224421 (2023).                                  arXiv:2405.12575 (2024).
[57] C.-C. Wei, X. Li, S. Hatt, X. Huai, J. Liu, B. Singh, K.-M.         [75] C. Li, M. Hu, Z. Li, Y. Wang, W. Chen, B. Thiagarajan,
     Kim, R. M. Fernandes, P. Cardon, L. Zhao, T. T. Tran, B. A.              M. Leandersson, C. Polley, T. Kim, H. Liu, C. Fulga, M. G.
     Frandsen, K. S. Burch, F. Liu, and H. Ji, La2 O3 Mn2 Se2 : A             Vergniory, O. Janson, O. Tjernberg, and J. van den Brink,
     correlated insulating layered d-wave altermagnet, Phys. Rev.             Topological Weyl Altermagnetism in CrSb, arXiv:2405.14777
     Mater. 9, 024402 (2025).                                                 (2024).
[58] P.-H. Chang, K. D. Belashchenko, and I. I. Mazin, Inverse lieb      [76] M. Long, T. I. Weinberger, Z. Wu, M. F. Hansen, R. Tao,
     materials: Altermagnetism and more, npj Quantum Materials                M. Shrestha, D. Graf, Y. Skourski, F. M. Grosche, and A. G.
     (2026).                                                                  Eaton, 3d bulk-resolved 𝑔-wave magnetic order parameter
[59] L. Garcia-Gassull, A. Razpopov, P. P. Stavropoulos, I. I.                symmetry in the metallic altermagnet CrSb, arXiv:2601.14526
     Mazin, and R. Valentí, Microscopic origin of the magnetic                (2026).
     interactions and their experimental signatures in altermagnetic     [77] I. Mazin, Altermagnetism in MnTe: Origin, predicted
     La2 O3 Mn2 Se2 , npj Spintronics 4, 9 (2026).                            manifestations, and routes to detwinning, Phys. Rev. B 107,
[60] F. Zhang, X. Cheng, Z. Yin, C. Liu, L. Deng, Y. Qiao,                    L100418 (2023).
     Z. Shi, S. Zhang, J. Lin, Z. Liu, et al., Crystal-symmetry-paired   [78] J. Krempaský, L. Šmejkal, S. W. D’Souza, M. Hajlaoui,
     spin–valley locking in a layered room-temperature metallic               G. Springholz, K. Uhlířová, F. Alarab, P. C. Constantinou,
     altermagnet candidate, Nature Physics 21, 760 (2025).                    V. Strocov, D. Usanov, W. R. Pudelko, R. González-Hernández,
[61] B. Jiang, M. Hu, J. Bai, Z. Song, C. Mu, G. Qu, W. Li,                   A. Birk Hellenes, Z. Jansa, H. Reichlová, Z. Šobáň, R. D.
     W. Zhu, H. Pi, Z. Wei, et al., A metallic room-temperature               Gonzalez Betancourt, P. Wadley, J. Sinova, D. Kriegner,
     d-wave altermagnet, Nature Physics 21, 754 (2025).                       J. Minár, J. H. Dil, and T. Jungwirth, Altermagnetic lifting of
[62] B. Thapa, P.-H. Chang, K. Belashchenko, and I. I. Mazin, Is              kramers spin degeneracy, Nature 626, 517 (2024).
     altermagnetism in vanadium oxychalcogenides a lost cause?,          [79] O. Amin, A. Dal Din, E. Golias, Y. Niu, A. Zakharov,
     arXiv:2602.18672 (2026).                                                 S. Fromage, C. Fields, S. Heywood, R. Cousins, F. Maccherozzi,
[63] Y.-K. Wang, S. Li, and S. A. Yang, Two-dimensional                       et al., Nanoscale imaging and control of altermagnetism in
     altermagnetic iron oxyhalides: Real chern topology and valley–           MnTe, Nature 636, 348 (2024).
     spin–lattice coupling, Nano Letters 26, 831 (2026).                 [80] T. Osumi, S. Souma, T. Aoyama, K. Yamauchi, A. Honma,
[64] B. Bell and J. Venderbos, Orbital piezomagnetic polarizability           K. Nakayama, T. Takahashi, K. Ohgushi, and T. Sato,
     of pure insulating altermagnets, arXiv:2602.10076 (2026).                Observation of a giant band splitting in altermagnetic mnte,
[65] I. Mazin, R. González-Hernández, and L. Šmejkal, Induced                 Phys. Rev. B 109, 115102 (2024).
     Monolayer Altermagnetism in MnP(S,Se)3 and FeSe,                    [81] A. D. Din, D. Usanov, L. Šmejkal, S. D’Souza, F. Guo,
     arXiv:2309.02355 (2023).                                                 O. Amin, E. Dawa, R. Campion, K. Edmonds, B. Kiraly, et al.,
[66] M. A. Vozmediano, M. Katsnelson, and F. Guinea, Gauge fields             Unconventional relativistic spin polarization of electronic bands
     in graphene, Physics Reports 496, 109 (2010).                            in an altermagnet, arXiv:2511.01690 (2025).
[67] N. Levy, S. A. Burke, K. Meaker, M. Panlasigui, A. Zettl,           [82] R. B. Regmi, H. Bhandari, B. Thapa, Y. Hao, N. Sharma,
     F. Guinea, A. C. Neto, and M. F. Crommie, Strain-induced                 J. McKenzie, X. Chen, A. Nayak, M. El Gazzah, B. G. Márkus,
     pseudo–magnetic fields greater than 300 tesla in graphene                et al., Altermagnetism in the layered intercalated transition metal
     nanobubbles, Science 329, 544 (2010).                                    dichalcogenide CoNb4 Se8 , Nature Communications 16, 4399
[68] F. von Oppen, F. Guinea, and E. Mariani, Synthetic electric              (2025).
     fields and phonon damping in carbon nanotubes and graphene,         [83] J. Graham, T. Hicken, R. Regmi, M. Janoschek, I. Mazin,
     Phys. Rev. B 80, 075420 (2009).                                          H. Luetkens, N. Ghimire, and Z. Guguchia, Local
[69] A. Cortijo, Y. Ferreirós, K. Landsteiner, and M. A. H.                   probe evidence supporting altermagnetism in Co1/4 NbSe2 ,
     Vozmediano, Elastic gauge fields in weyl semimetals, Phys. Rev.          arXiv:2503.09193 (2025).
     Lett. 115, 177202 (2015).                                           [84] N. Dale, O. A. Ashour, M. Vila, R. B. Regmi, J. Fox, C. W.
                                                                              Johnson, A. Fedorov, A. Stibor, N. J. Ghimire, and S. M. Griffin,
                                                                                                                                                                      8

     Non-relativistic spin splitting above and below the fermi level                         effect in Tb3 Ga5 O12 , Phys. Rev. B 81, 214415 (2010).
     in a 𝑔-wave altermagnet, arXiv:2411.18761 (2024).                                  [90] R. Aquino, I. Jang, J. Schmalian, and R. M. Fernandes, Probing
[85] E. Day-Roberts, H. Wu, O. Erten, and A. Botana, An                                      the Hall viscosity of altermagnets using a modified acoustic
     altermagnetic materials library in intercalated transition-metal                        Faraday effect, unpublished.
     dichalcogenides, arXiv:2601.02481 (2026).                                          [91] H. T. Stokes, D. M. Hatch, and B. J. Campbell, ISOTROPY
[86] C. Kittel, Interaction of spin waves and ultrasonic waves in                            Software Suite, iso.byu.edu (2022).
     ferromagnetic crystals, Phys. Rev. 110, 836 (1958).                                [92] M. I. Aroyo, J. M. Perez-Mato, C. Capillas, E. Kroumova,
[87] S. Wang and J. Crow, Acoustic Faraday rotation, IEEE                                    S. Ivantchev, G. Madariaga, A. Kirov, and H. Wondratschek,
     Transactions on Magnetics 7, 138 (1971).                                                Bilbao Crystallographic Server:             I. Databases and
[88] Y. Lee, T. M. Haard, W. P. Halperin, and J. A. Sauls, Discovery                         crystallographic computing programs, Zeitschrift für
     of the acoustic Faraday effect in superfluid 3 He-B, Nature 400,                        Kristallographie-Crystalline Materials 221, 15 (2006).
     431 (1999).
[89] A. Sytcheva, U. Löw, S. Yasin, J. Wosnitza, S. Zherlitsyn,
     P. Thalmeier, T. Goto, P. Wyder, and B. Lüthi, Acoustic Faraday


                                                                       END MATTER

   In Table I we list the independent non-vanishing elements of the Hall viscosity tensor 𝜂𝑖𝐻𝑗 𝑘𝑙 generated by different types of
ferromagnetic and altermagnetic order in the most symmetric tetragonal, hexagonal, and cubic point groups [25]. The presence
of SOC is assumed. We used the software Isotropy [91] and the Bilbao Crystallographic Server [92] to obtain these results. Note
that additional elements follow from the relations 𝜂𝑖𝐻𝑗 𝑘𝑙 = 𝜂 𝐻
                                                               𝑗𝑖𝑘𝑙 = 𝜂𝑖 𝑗𝑙𝑘 = −𝜂 𝑘𝑙𝑖 𝑗 .
                                                                       𝐻          𝐻

   We consider separately the altermagnetic (AM) and ferromagnetic (FM) order parameters. When the√order parameter is
multi-dimensional, we show explicitly the order parameter components that are non-zero, e.g. (1, 0, 0) or ( 3, 1). In this table,
the (𝑥, 𝑦, 𝑧) coordinates refer to the coordinates in the magnetically ordered state, which can be rotated with respect to the
coordinates of the paramagnetic phase depending on which order parameter components condense [92]. Note that, for the cubic
point group, the 𝑖-wave AM order parameter that transforms as the 𝐴1𝑔         − irrep does not have a non-zero Hall viscosity tensor

element.

         Point Group          AM irrep.                 Hall viscosity tensor                              FM irrep.       Hall viscosity tensor
         tet. 𝐷 4ℎ (4/𝑚𝑚𝑚)     − (𝑔-wave)                                                                     −
                                                        𝜂𝐻                                                                   𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧
                              𝐴1𝑔                                    𝐻                                                     𝜂𝐻                𝐻          𝐻
                                                          𝑥 𝑥𝑧𝑧 = 𝜂 𝑦𝑦𝑧𝑧                                   𝐴2𝑔
                               −
                              𝐵1𝑔 (𝑑-wave)                𝐻            𝐻 , 𝜂𝐻
                                                        𝜂 𝑥 𝑥𝑧𝑧 = −𝜂 𝑦𝑦𝑧𝑧                                  𝐸 𝑔− (1, 0)     𝜂 𝑥 𝑥 𝑥 𝑦 , 𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧 , 𝜂 𝑥 𝑦𝑧𝑧
                                                                                                                             𝐻           𝐻          𝐻
                                                                                  𝑥 𝑥 𝑦𝑦
                               − (𝑑-wave)               𝜂 𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝐻                         𝐸 𝑔− (1, 1)       𝑥 𝑥 𝑦𝑧 , 𝜂 𝑦𝑦𝑦𝑧 , 𝜂 𝑧𝑧 𝑦𝑧 , 𝜂 𝑥 𝑦 𝑥𝑧
                              𝐵2𝑔                         𝐻           𝐻                                                    𝜂𝐻           𝐻          𝐻         𝐻
                                                                                 𝑥 𝑦𝑧𝑧
                             − (𝑖-wave)
         hex. 𝐷 6ℎ (6/𝑚𝑚𝑚) 𝐴1𝑔                                                                               −
                                                        𝜂𝐻                                                               𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧
                                                                        𝐻                                              𝜂𝐻              𝐻         𝐻
                                                          𝑥 𝑥𝑧𝑧 = 𝜂 𝑦𝑦𝑧𝑧                                   𝐴2𝑔
                             −
                           𝐵1𝑔 (𝑔-wave)                   𝐻
                                                        𝜂 𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦𝑦  𝐻               𝐻                  −
                                                                                                           𝐸 1𝑔 (1, 0) 𝜂 𝑥 𝑥 𝑦𝑧 , 𝜂 𝑦𝑦𝑦𝑧 , 𝜂 𝑧𝑧 𝑦𝑧 , 𝜂 𝐻
                                                                                                                         𝐻          𝐻        𝐻
                                                                              𝑥𝑧 = −𝜂 𝑥 𝑦𝑦𝑧                                                            𝑥 𝑦 𝑥𝑧
                             − (𝑔-wave)
                                                                                                                 √
                                                                                                             − ( 3, 1) 𝜂 𝐻
                                                        𝜂𝐻                                                               𝑥 𝑥 𝑦𝑧 , 𝜂 𝑦𝑦𝑦𝑧 , 𝜂 𝑧𝑧 𝑦𝑧 , 𝜂 𝑥 𝑦 𝑥𝑧
                                                                          𝐻             𝐻                                           𝐻        𝐻         𝐻
                           𝐵2𝑔                            𝑥 𝑥 𝑦𝑧 = −𝜂 𝑦𝑦𝑦𝑧 = 𝜂 𝑥 𝑦 𝑥𝑧                      𝐸 1𝑔
                             − (1, 0) (𝑑-wave)
                           𝐸 2𝑔                         𝜂𝐻        , 𝜂 𝐻     ,  𝜂 𝐻
                                                          𝑥 𝑥 𝑦𝑦      𝑥 𝑥𝑧𝑧      𝑦𝑦𝑧𝑧
                             −
                                 √
                                                        𝜂𝐻𝑥 𝑥 𝑥 𝑦 , 𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑧𝑧 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧
                           𝐸 2𝑔 ( 3, 1)                               𝐻          𝐻          𝐻


         cub. 𝑂 ℎ (𝑚 𝑚𝑚)         − (𝑑-wave)                                                            − (1, 0, 0) 𝜂 𝐻
                                                     𝜂𝐻                                                               𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧
                              𝐴2𝑔                                  𝐻            𝐻                                                  𝐻          𝐻
                     ¯                                 𝑥 𝑥 𝑦𝑦 = 𝜂 𝑦𝑦𝑧𝑧 = 𝜂 𝑧𝑧 𝑥 𝑥                     𝑇1𝑔
                                 −
                              𝐸 𝑔 (1, 0) (𝑑-wave) 𝜂 𝑥 𝑥𝑧𝑧 = 𝜂 𝑦𝑦𝑧𝑧
                                                       𝐻          𝐻                                    −
                                                                                                      𝑇1𝑔 (1, 1, 1) 𝜂 𝑥 𝑥 𝑥 𝑦 = −𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥𝑧 𝑦𝑧 ,
                                                                                                                      𝐻            𝐻          𝐻
                                    √
                              𝐸 𝑔− ( 3, 1)           𝜂𝐻𝑥 𝑥𝑧𝑧   = −𝜂 𝐻 , 𝜂𝐻
                                                                    𝑦𝑦𝑧𝑧       𝑥 𝑥 𝑦𝑦                               𝜂𝐻            𝐻            𝐻
                                                                                                                      𝑥 𝑥 𝑥𝑧 = −𝜂 𝑦𝑦 𝑥𝑧 = 𝜂 𝑦𝑧 𝑥 𝑦
                               −
                              𝑇2𝑔 (1, 0, 0) (𝑑-wave) 𝜂 𝑥 𝑥 𝑥 𝑦 = 𝜂 𝑦𝑦 𝑥 𝑦 , 𝜂 𝑥 𝑦𝑧𝑧
                                                       𝐻           𝐻          𝐻
                               − (1, 1, 1)           𝜂𝐻𝑥 𝑥𝑧𝑧 = 𝜂 𝑦𝑦𝑧𝑧 , 𝜂 𝑥 𝑦 𝑥𝑧 = 𝜂 𝑥 𝑥 𝑦𝑧 = −𝜂 𝑦𝑦𝑦𝑧
                              𝑇2𝑔                                 𝐻          𝐻        𝐻          𝐻



TABLE I. Non-zero elements of the Hall viscosity tensor 𝜂𝑖𝐻𝑗 𝑘𝑙 in point groups 𝐷 4ℎ , 𝐷 6ℎ , and 𝑂 ℎ for altermagnetic (AM) and ferromagnetic
(FM) orders.
                Supplementary Material: Anomalous Hall viscosity of altermagnets

                      Iksu Jang,1 Rui Aquino,2, 3, 4 Jörg Schmalian,1, 5 and Rafael M. Fernandes2, 3
         1
             Institute for Theory of Condensed Matter, Karlsruhe Institute of Technology, Karlsruhe 76131, Germany
                                 2
                                   Department of Physics, The Grainger College of Engineering,
                              University of Illinois Urbana-Champaign, Urbana, Illinois 61801, USA
               3
                 Anthony J. Leggett Institute for Condensed Matter Theory, The Grainger College of Engineering,
                              University of Illinois Urbana-Champaign, Urbana, Illinois 61801, USA
                        4
                          ICTP South American Institute for Fundamental Research, São Paulo, SP, Brazil
                                       5
                                         Institute for Quantum Materials and Technologies,
                                  Karlsruhe Institute of Technology, Karlsruhe 76131, Germany
                                                       (Dated: June 26, 2026)




                                                                  CONTENTS

S1. Hall viscosity beyond the adiabatic approximation:                                                                  1

S2. Tetragonal d-wave altermagnetic model                                                                               2
    A. Numerical values of TB parameters                                                                                2
    B. Dirac theory and emergent gauge fields                                                                           2

S3. Hexagonal g-wave altermagnetic model                                                                                3
    A. Symmetries of CrSb                                                                                               3
    B. Tight-binding parameters                                                                                         5

S4. Hall viscosity and kz -dependent Lifshitz transitions                                                               6
    A. Details of the Berry curvature calculation                                                                       6

    References                                                                                                          6


                    S1.       HALL VISCOSITY BEYOND THE ADIABATIC APPROXIMATION:

  In the main text we used the adiabatic approximation to determine the Hall viscosity, an approach that is well
defined for gapped systems, but may be problematic in the presence of gapless excitations. To address this issue we
rederive Eq. (5) without relying on the adiabatic approximation. We consider the following strain-dependent action
                                Z h                                                                          i
                                                                                                  αβ
                      †
                  S[Ψ , Ψ, ε] =      Ψ†k (τ )∂τ Ψk (τ ) + Ψ†k (τ )H0,k Ψk (τ ) + εαβ (τ )Ψ†k (τ )Hε,k Ψk (τ ) . (S1)
                                      τ,k

By integrating out the fermion fields, we obtain the effective action in terms of the strain field ϵ.
                                                  1X
                                           Seff =      εαβ (iΩ)εγδ (−iΩ)Παβ,γδ (iΩ),
                                                  2
                                                    iΩ
                                                    X h αβ             γδ
                                                                                   i
                                    αβ,γδ
                                   Π      (iΩ) = T     tr Hε,k Gk,iω Hε,k Gk,iω+iΩ ,                                  (S2)
                                                                 k,iω

where Gk,iω = [iω − H0,k ]−1 . Performing the Matsubara sum and the analytic continuation iΩ → ω + iγ, we obtain
                                                               h ⟨uk,m |Hαβ |uk,n ⟩⟨uk,n |Hγδ |uk,m ⟩            i
                                                                         ϵ,k               ϵ,k
                                           X
                          αβ,γδ
                          Π       (ω) =            nF (ξkn )                                            − (n ↔ m) .   (S3)
                                                                        ξkn − ξkm + ω + iη
                                          k,n̸=m

Here, |uk,n ⟩ and ξkn are the n-th eigenvector and eigenvalue of H0,k , respectively. This serves as finite ω contribution
to the elastic tensor. To first order in ω, we obtain
                                                  1   dω
                                                    Z
                                         Seff = −        iωϵαβ (ω)ϵγδ (−ω)η αβ,γδ                                     (S4)
                                                  2   2π
                                                                                                                       2

from which we readily identify the Hall viscosity
                                     XX          2nF (ξkn )     h
                                                                            αβ                    γδ
                                                                                                               i
                         η αβ,γδ =                           Im   ⟨u k,m |H ϵ,k |u k,n ⟩⟨u k,n |H ϵ,k |u k,m ⟩      (S5)
                                               (ξkm − ξkn )2
                                     k n̸=m

in agreement with Eqs. (2) and (5).


                          S2.    TETRAGONAL d-WAVE ALTERMAGNETIC MODEL

                                        A.     Numerical values of TB parameters

  For the results presented in Fig. 2 in the main text, we used the following numerical values of parameters

                                 t2 = t1 /2,      td = 2t1 ,    λ = 2t1 ,     J = t1 ,     ϕ = ϕc /2                (S6)
                                        (A )   (B )                  (A )                 (A )
                                       g1 1 = g1 2 = αt1 ,          g3 1 = αtd ,         g0 1 = αt2                 (S7)

with t1 = 1 and α = 8.
   For Fig. 3 in main text, comparing results obtained from the Dirac theory and the tight binding model, we use
following numerical values of parameters:

                             t2 = 0,    td = 0.705t1 ,      λ = 0.025t1 ,      J = t1 /2,        ϕ = ϕc /2,         (S8)

which gives v1 = v3 = 1.41t1 ,   m = 0.175t1 , with
                                        (A )       (B )              (A )                 (A )
                                       g1 1 = g1 2 = αt1 ,          g3 1 = αtd ,         g0 1 = 0,                  (S9)

where α = 8.


                                       B.    Dirac theory and emergent gauge fields

   Here, we expand the Lieb-lattice Hamiltonian Eqs. (7) and (8) in the vicinity of the Dirac points. In the absence
of spin orbit coupling, i.e. for λ = 0, there are four Dirac nodes at the boundary of the Brillouin zone. To make the
analysis easier, we consider the Brillouin zone defined by kx , ky ∈ (0, 2π) as shown in Fig. 3(a). Let us assume without
restriction that td , J, ϕ > 0. Provided 0 < ϕ < ϕc = 4td /J, spin up states have two Dirac points located at (k0 , π)
and (2π − k0 , π), while spin down states have Dirac points at (π, k0 ) and (π, 2π − k0 ), as depicted in Fig. 3(a), with
the momentum scale k0 = arccos (2ϕ/ϕc − 1). For J = 0 (ϕc = ∞), k0 = π and the Dirac points merge at (±π, ±π)
to become quadratic band touching points. In the vicinity of these Dirac points and for small spin-orbit coupling, we
obtain

                                             H0↑,κ (p) = κv1 py τ1 + κv3 px τ3 + mτ2 ,                             (S10)

where κ = ±1 stands for the valley indices (κ = +1: (k0 , π), κ = −1: (2π − k0 , π)) and p ispa momen-
tum vector
        p measured
             p     with respect to each
                                    p valley momentum. The velocities are given as v1 = 2t1 ϕ/ϕc and
v3 = 4td ϕ/ϕc 1 − ϕ/ϕc , while m = λ 1 − ϕ/ϕc is the mass. For the down spins we have

                                             H0↓,κ (p) = κv1 px τ1 − κv3 py τ3 − mτ2 ,                             (S11)

where κ = ±1 stands for the valley points (π, k0 ) and (π, 2π − k0 ) respectively.
  The strain terms at the Dirac points are
                                                       
                                 Hεσ,κ = 2 εxx + εyy (g 0 τ0 + σg 3 τ3 ) − 4εxy g 1 τ1
                                                       
                                       + 2 εxx − εyy g ′3 τ3                                                       (S12)

             (A )                       (A )                                                     p
with g 0 = 2g0 1g (ϕ/ϕc − 1), g 3 = 2g3 1g ϕ/ϕc , g ′3 = 2g (B1g ) (ϕ/ϕc − 1), and g 1 = g (B2g ) 1 − ϕ/ϕc . The spin
dependence of the strain term is a consequence of the fact that the location of the Dirac points is different for spin-up
                                                                                                                              3

                                                        σ
and spin-down states. This yields the stress tensors Txx+yy     = 2 (g 0 τ0 + σg 3 τ3 ), Txx−yy = 2g 3 τ3 , and Txy = −4g 1 τ1 .
The Hamiltonian in the presence of stain is then given by Eq. (10) in the main text, with gauge fields
                                            ′                                              
                                ↑,κ          g 3 (εxx − εyy ) − g 3 (εxx + εyy ) 2g 1 εxy
                              A     = 2κ                                         ,
                                                              v3                       v1
                                                        ′
                                                                                           
                                ↓,κ          2g 1 εxy g 3 (εxx − εyy ) + g 3 (εxx + εyy )
                              A     = 2κ             ,                                                                  (S13)
                                                v1                     v3

and Dirac matrices α↑ = (τ3 , τ1 ), α↓ = (τ1 , τ3 ), and β = τ2 , obeying the usual Clifford algebra. For the velocities,
it holds v ↑,κ = κ (v3 , v1 ) while v ↓,κ = κ (v1 , −v3 ). By analyzing the Hall conductivity of a single gapped Dirac point
with respect to these emergent gauge fields, we obtain the result given in the main text. Using Eq. (S13) and Eq. (13),
we then obtain the following effective action in terms of the strain field:
                                                         8g1 g3 H
                                                                  Z
                                                Seff =         σ       (ϵxx + ϵyy )ϵ̇xy                                (S14)
                                                          t1 td xy t,x
             H
which gives ηxx+yy,xy = 8g 1 g3 H
                         t1 td σxy .



                            S3.    HEXAGONAL g-WAVE ALTERMAGNETIC MODEL

  In this section, we provide a detailed description of the hexagonal model for g-wave altermagnetism corresponding
to space group P 63 /mmc (No. 194), which is relevant for CrSb, following Ref. [1].


                                                   A.     Symmetries of CrSb



      (a)                                                           (b)


                                                     Cr (A)                                              Cr (A)

                                                     Cr (B)                                              Sb (Top)

                                                     Sb                                                  Sb (Bottom)




                             FIG. S1: (a) Unit-cell of the CrSb. (b) Top-view of the CrSb lattice.

   Fig. S1 illustrates the unit cell of CrSb, which crystallizes in space group 194 (P 63 /mmc), as well as the top-view
of the lattice. We define the lattice vectors a1 , a2 , and a3 according to the coordinates in Fig. S1 to construct the
space group representations.
   The generators of the space group, expressed in Seitz notation {R|t}, are:

                                  1,   {3001 |0, 0, 0},   {2001 |0, 0, 1/2},   {2110 |0, 0, 0},   I

where the indices nml for the rotation axes and translation vectors denote the direction na1 + ma2 + la3 . Following
Ref. [1], we consider the electrons on the two Cr sublattices (A, B) as the primary degrees of freedom. Sublattices A
and B are located at (0, 0, 0) and (0, 0, 1/2), respectively.
  The field operators in momentum space are given by:
                                                       1 X −ik·(R+⃗ηα )
                                           cα,σ (k) = √     e           cα,σ (R),                                         (S15)
                                                        N R
                                                                                                                                 4

with sublattice vectors ⃗ηA = 0 and ⃗ηB = 21 a3 . We thus define the four-component spinor as:
                                                                                                         T
                                          ψ(k) = cA,↑ (k) cA,↓ (k) cB,↑ (k) cB,↓ (k)                          .               (S16)


                     Generator         Operator Transformation Vector Relation
                                       (                                      (
                                         c†A (R) → c†A (R′ )       ′            3001 a1 = a2
                     {3001 |0, 0, 0}                              R = 3001 R,
                                         c†B (R) → c†B (R′ )                    3001 a2 = −a1 − a2
                                       (                                      (
                                         c†A (R) → c†B (R′ )       ′            2001 a1 = −a1
                     {2001 |0, 0, 1/2}                            R = 2001 R,
                                         c†B (R) → c†A (R′ + a3 )               2001 a2 = −a2
                                                                              
                                                                              2110 a1 = a2
                                       (
                                         c†A (R) → c†A (R′ )
                                                                              
                                                                   ′
                     {2110 |0, 0, 0}                              R = 2110 R, 2110 a2 = a1
                                         c†B (R) → c†B (R′ − a3 )             
                                                                                2110 a3 = −a3
                                                                              
                                       (
                                           †         †   ′
                                         cA (R) → cA (R )
                     I                                            R′ = −R
                                         c†B (R) → c†B (R′ − a3 )

 TABLE S1: Space-group symmetry operations on the fermionic operators for space group 194, relevant to hexagonal CrSb.



                      Space group operations (194)                               Point group operations (D6h )

                      {6001 |0, 0, 1/2} = {2001 |0, 0, 1/2}{3001 |0, 0, 0} C6
                      {3001 |0, 0, 0}                                            C3
                      {2001 |0, 0, 1/2}                                          C2
                      {2100 |0, 0, 0}, {2110 |0, 0, 0}, {2010 |0, 0, 0}          C2′′ (2100 )
                      {21̄10 |0, 0, 0}, {2210 |0, 0, 0}, {2120 |0, 0, 0}         C2′ (2120 )
                      I                                                          I

 TABLE S2: Correspondence between the symmetry operations in the space group 194 and the symmetry operations of the
                                               point group D6h .

  Table S1 summarizes the action of the symmetry operations of the space group on the fermion operators. In the
spinor representation, these operations are:
                                                                                                 π
                                 {3001 |0, 0, 0}ψ(k){3001 |0, 0, 0}−1 = (τ0 ⊗ ei 3 σz )ψ(3001 k),                             (S17)
                                                                           −1         i k2z             iπ
                                                                                                         2 σz
                            {2001 |0, 0, 1/2}ψ(k){2001 |0, 0, 1/2}              =e            (τx ⊗ e           )ψ(2001 k),   (S18)
                                                                           −1                   iπ
                                                                                                 2 σx
                                 {2110 |0, 0, 0}ψ(k){2110 |0, 0, 0}             = (τ0 ⊗ e               )ψ(2110 k),           (S19)
                                                                           −1
                                                               Iψ(k)I           = (τ0 ⊗ σ0 )ψ(−k).                            (S20)

  It is convenient to use the correspondence between operations in space group 194 and those of the underlying D6h
point group, as shown in Table S2. This correspondence is obtained by comparing the character table of each case.
Using this correspondence, the fermionic bilinears can be classified into irreducible representations of D6h as follows:

   • ψ † (k)τ0 ψ(k) : A1g

   • ψ † (k)τ1 ψ(k) : A1g
                       −
   • ψ † (k)τ2 ψ(k) : B2g

   • ψ † (k)τ3 ψ(k) : B2g

  where the minus superscript indicates a time-reversal odd irrep.
                                                                                                                                                  5

                                                          B.   Tight-binding parameters

                                                                                                                                        †
                                                                                                                                 P
  Using the spinors introduced above, it is now straightforward to construct the Hamiltonian H =                                     k ψ (k)Hk ψ(k).
Following Ref. [1], the strain-free part of the Hamiltonian Hk,0 is given by:

                                          Hk,0 = ε0,k + t1,k τ1 + t3,k τ3 + τ2⃗λk · ⃗σ + Jϕτ3 σ3 ,                                            (S21)

where the hopping terms are:
                                                                   √         !
                                                  kx                   3ky
                  ε0,k = t1        cos kx + 2 cos    cos                         + t2 cos kz − µ,                                             (S22)
                                                   2                   2
                              kz
                  t1,k = t3 cos  , t3,k = t4 sin kz fy (fy2 − 3fx2 ),                                                                         (S23)
                               2
                              kz                                kz                      kz
                  λx,k = λ cos (fx2 − fy2 ), λy,k = −2λ cos fx fy ,                        fx (fx2 − 3fy2 ),
                                                                                               λz,k = λz sin         (S24)
                              2                                 2                       2
                                                                          √                √                √
                                                                            3k                                3k
and with hexagonal form factors defined as fx = sin kx + sin k2x cos 2 y and fy = 3 cos k2x sin 2 y . Here, x is
the direction parallel to the a1 in Fig. S1, corresponding to the crystallographic direction [100]. Note that the
                                                   −
altermagnetic order parameter ϕ transforms as B1g      = B2g ⊗ A−              †
                                                                  2g , since ψ (k)τ3 ψ(k) transforms as B2g , as reflected
in the transformation properties of the function t3,k , and σ3 transforms as A−  2g .
   The strain Hamiltonian Hk,ε consists of two parts corresponding to the shear components that transform as the
E1g (out-of-plane shear) and E2g (in-plane shear) irreps of the point group D6h :
                                          (E      )       (E   )
                            Hk,ε = Hk,ε1g + Hk,ε2g ,                                                                                          (S25)
                                              h                            i                h                           i
                            (E )                       (xz)           (yz)                           (xz)          (yz)
                           Hk,ε1g = gτ(E
                                       1
                                         1g )
                                                ε xz f 1,k  +  ε yz f 1,k    τ 1 + g (E1g )
                                                                                     τ3       ε xz f 3,k  + ε yz f 3,k    τ3 ,                (S26)
                                                                    2    2
                                              h                                             i
                            (E )                                 (x −y )               (xy)
                           Hk,ε2g = gτ(E
                                       1
                                         2g )
                                                (εxx − εyy )f1,k            − 2εxy f1,k τ1
                                                                    (x2 −y 2 )
                                                 h                                             i
                                                                                          (xy)
                                    + gτ(E3
                                            2g )
                                                   (ε xx  − ε yy )f 3,k        −  2ε xy f 3,k    τ3
                                             (E
                                            2g        )
                                       + gSOC  fSOC,k [(εxx − εyy )σx − 2εxy σy ] τ2                                                          (S27)
        (Γ)                                                                          (α)
where gi     are the coupling constants and the form factors fi,k are:
                                                             √     !                              √
        (xz)        8       kz       kx          kx            3ky          (xz)           kx       3ky
       f1,k = − √ sin          sin        2 cos       + cos          ,     f3,k = −4 sin      sin       ,                                     (S28)
                     3       2        2            2           2                            2       2
                                          √                                                                     √     !
        (yz)            kz        kx        3ky                             (yz)      4                kx         3ky
       f1,k = −8 sin         cos      sin        ,                         f3,k = √       cos kx − cos     cos          ,                     (S29)
                          2        2        2                                          3                2         2
                                                         √     !                                            √
    (x2 −y 2 )    8       kz                    kx         3ky          (x2 −y 2 )
                                                                                      √             kx        3ky
   f1,k        = √ cos          cos kx − cos         cos         ,     f3,k        = − 3 sin kz cos    sin        ,                           (S30)
                   3       2                     2         2                                         2        2
                                        √                                                                        √      !
        (xy)           kz      kx         3ky                               (xy)                         kx         3ky
       f1,k = 8 cos        sin      sin       ,                            f3,k = sin kz sin kx + sin        cos          ,                   (S31)
                       2        2         2                                                               2         2
                    kz
     fSOC,k = cos      .                                                                                                                      (S32)
                    2
  The results shown in the main text were obtained for the following set of tight-binding parameters:

                              t2 = 0.6t1 ,        t3 = 0.3t1 ,     t4 = 0.2t1 ,         λ = λz = 0.5t1 ,    ϕz = 0.5t1 ,
                                                                                            (E2g )
                                           gτ(E
                                              1
                                                1g )
                                                     = gτ(E
                                                          3
                                                            1g )
                                                                 = gτ(E
                                                                      1
                                                                        2g )
                                                                             = gτ(E
                                                                                  3
                                                                                    2g )
                                                                                         = gSOC    = 8t1 .

   For the quantitative analysis of the Hall viscosity it is necessary to relate the typical values of the electron-strain
couplings g = αt1 to the hopping elements t1 . Consider hopping elements between orbitals of angular   momentum     ℓ and
                                                                                             ′
ℓ′ at a distance r and with equilibrium distance r0 . They behave like t(r) ∼ t0 (r/r0 )−(ℓ+ℓ +1) ≈ t0 1 + α r−r
                                                                                                               r0
                                                                                                                  0
                                                                                                                      [2, 3].
                                                                                                                          6

Then, the dimensionless constant is α = ℓ + ℓ′ + 1. Hence, α = 1 describes hopping between two s-orbitals, while
α = 5 refers to hopping between two d-orbitals. If the hopping is a consequence of a second order process between two
orbitals with angular momentum ℓ via an intermediate orbital with angular momentum ℓ′ , we obtain α = 2 (ℓ + ℓ′ + 1).
Hence hopping between two d-orbitals (ℓ = 2) via a p-orbital (ℓ′ = 1) yield the value used here, α = 8.


                  S4.   HALL VISCOSITY AND kz -DEPENDENT LIFSHITZ TRANSITIONS

   We demonstrate that the abrupt changes in the Hall viscosity of the hexagonal g-wave altermagnet are directly
linked to Lifshitz transitions. Figs. S2(a)–(c) show the changes in the Fermi surface as the chemical potential varies
within the narrow range in which the Hall viscosity shows sharp changes. In all cases, we observe Lifshitz transitions
from closed to open Fermi surfaces around the high-symmetry L and M points, establishing the connection between
Lifshitz transitions and changes in the Hall viscosity. In contrast, when the Lifshitz transition takes place near the
H and K points, the Hall viscosity does not display sharp changes, as shown in Fig. S2(d). This distinction arises
because the strain-dependent Hamiltonian Hϵ,k at these points either vanishes or couples to only a single component
of the strain tensor, thereby precluding a Hall response.


                                   A.   Details of the Berry curvature calculation

  In the numerical calculation of the Hall viscosity, in order to avoid high symmetry points that usually coincide with
time-reversal invariant-momenta, we set our grids as follows:
                                                                            
                                     i − 0.5       j − 0.5        k − 0.5   i = 1, . . . , N1
                                                                            
                          kijk = G1          + G2          + G3           ,   j = 1, . . . , N2                   (S33)
                                       N1            N2             N3      
                                                                              k = 1, . . . , N3
                                                                            

where G1 , G2 , and G3 are the reciprocal lattice vectors defined as:
                                                     
                                                  1               4π
                                 G1 = 2π x̂ + √ ŷ , G2 = √ ŷ,              G3 = 2πẑ.                               (S34)
                                                   3                3
   We found that the numerical calculation of the Hall viscosity tensor for the hexagonal g-wave model converges poorly
as a function of grid size. This is because of the change of the projected two-dimensional Fermi surface topology as
a function of kz . NearR the kz planes associated with these Lifshitz transitions, the kx , ky -integrated Berry curvature,
defined as Ω̄(kz ) ≡ kx ,ky Ω(kx , ky , kz ), exhibits severe oscillations depending on the grid resolution. Consequently,
                                                  R
the Hall viscosity, which is proportional to kz Ω̄(kz ), converges extremely slowly, failing to stabilize even when the
grid dimensions N1 × N2 × N3 approach 500 × 500 × 500.
   To resolve this issue, we introduced the Fermi-Dirac distribution function with temperature scales T ≈ N18t  N2 N3 . This
                                                                                                                  1

thermal broadening acts as a numerical low-pass filter that effectively smooths out the topological transitions across
the discrete grid slices. As a result, the Hall viscosity tensor converges significantly faster and remains robust against
variations in grid configuration. For the numerical results presented in the main text, we set N1 = N2 = N3 = 240,
which corresponds to a regularizing temperature scale of T /t1 = 5.8 × 10−7 .
   We note that, although the numerical grid was chosen to avoid all high-symmetry points, certain momentum points
still exhibit large local Berry curvature values. This high concentration makes it difficult to clearly identify the
underlying symmetry properties of the Berry curvature. To resolve this, we introduce a regularized Berry curvature
for Figs. 4(d) and 4(e) in main text, defined as:

                                          (l),reg
                                                           X γ αβ (k)∗ γ γδ (k)
                                                                  ml       ml
                                        Ωαβγδ (k) = 2Im                    2         .                                (S35)
                                                           m̸=l
                                                                (ξkl − ξkm ) + δ 2
  For these figures, we set δ = 0.5t1 . Note that this regularized version is strictly used for visual presentation in these
specific plots; all calculations for the Hall viscosity tensor presented in the main text were performed using the exact
formulation with δ = 0.




[1] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F. Agterberg, Minimal models for altermagnetism, Phys. Rev. B 110,
    144412 (2024).
                                                                                                                             7




FIG. S2: Hall viscosity and Lifshitz transitions in the hexagonal g-wave altermagnetic model. (a)–(c) Hall viscosity within the
   chemical potential intervals (a) −2.3 ⪅ µ/W ⪅ −1.9, (b) −1.3 ⪅ µ/W ⪅ −0.8, and (c) −0.1 ⪅ µ/W ⪅ 0.3 (blue-shaded
regions), accompanied by the evolution of the Fermi surface. These panels demonstrate that Lifshitz transitions at the L and
M high-symmetry points correlate with abrupt changes in the Hall viscosity. (d) In contrast, Lifshitz transitions at the H and
           K points within the range −1.7 ⪅ µ/W ⪅ −1.2 (green-shaded region) do not exhibit a similar behavior.


[2] W. A. Harrison, Electronic structure and the properties of solids: the physics of the chemical bond, Courier Corporation
    (2012).
[3] K. Takahashi, C. R. W. Steward, M. Ogata, R. M. Fernandes, and J. Schmalian, Elasto-Hall conductivity and the anomalous
    Hall effect in altermagnets, Phys. Rev. B 111, 184408 (2025).

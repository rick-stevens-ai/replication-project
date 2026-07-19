<!--
INTERIM: pdftotext fallback, marker/nougat not installed.
=================================================================
This file is the PROSE artifact (role: marker.md). The real `marker`
binary is NOT installed on this host (`which marker` -> not found), so
this is a documented interim produced with poppler `pdftotext -layout`.

  Regenerate with the real tool when available:
      marker_single textures-orbital-cullen2025.pdf ./extraction/ --output_format markdown

KNOWN FIDELITY LOSS: Unicode/LaTeX math is degraded (matrix layout,
Greek letters, sub/superscripts break under pdftotext). The AUTHORITATIVE
equation transcriptions live in report/REPORT.tex and in
extraction/nougat.mmd (the math artifact). Below is the layout-preserving
text dump used for section structure and figure captions.
=================================================================
-->

# Cullen, Wang & Culcer 2025 - Orbital Hall effect in spin-3/2 hole-doped semiconductors (arXiv:2509.20436v3)

                                                        Orbital Hall effect in spin-3/2 hole-doped semiconductors and its implications for
                                                                                             orbitronics
                                                                                    James H. Cullen,1, ∗ Zhanning Wang,1 and Dimitrie Culcer1
                                                                          1
                                                                              School of Physics, The University of New South Wales, Sydney 2052, Australia
                                                                                                         (Dated: June 19, 2026)
                                                                     State-of-the-art magnetic devices rely on faster, more efficient memory elements. A major re-
                                                                  cent advance is the discovery of orbital torques, which use the orbital angular momentum of Bloch
                                                                  electrons to switch the magnetisation of an adjacent ferromagnet, motivating the search for orbi-
                                                                  tronic materials with strong orbital responses, exemplified by the orbital Hall effect (OHE). Here
arXiv:2509.20436v3 [cond-mat.mes-hall] 18 Jun 2026




                                                                  we propose p-type semiconductors, with a focus on Ge, as orbitronic platforms. We demonstrate
                                                                  that bulk holes in five common semiconductors exhibit a large orbital Hall conductivity of order
                                                                  103 (ℏ/e)Ω−1 cm−1 , exceeding the spin-Hall effect by 2-3 orders of magnitude. The calculation is
                                                                  performed within the framework of the modern theory of orbital magnetisation, while incorporating
                                                                  recently-discovered quantum corrections to the OHE. Moreover, we argue that bulk p-type Ge and
                                                                  Si serve as ideal testbeds for the orbital torque resulting from a charge current, since the spin- and
                                                                  orbital-Edelstein effects are forbidden by symmetry. Our results provide a blueprint for producing
                                                                  strong orbital torques in magnetic devices with p-type semiconductors, guiding experimental work
                                                                  in this direction.


                                                                     I.   INTRODUCTION                                 system is well understood [64–69], most interest in the
                                                                                                                       OAM at present is motivated by its out-of-equilibrium
                                                        Orbital dynamics in condensed matter systems have              properties [70–74], where fundamental issues need to be
                                                     come under renewed scrutiny in recent years with an               resolved. As an example, it was shown recently that
                                                     intense focus on out-of-equilibrium phenomena broadly             quantum corrections to the OHE can overwhelm the con-
                                                     encompassed by the field of orbitronics [1–4]. The study          ventional terms, while disorder can dominate the effect
                                                     of orbitronic phenomena involving the electrical gener-           in certain systems[36, 58]. An important fundamental
                                                     ation and transport of Bloch electrons’ orbital angular           question concerns inversion symmetric systems, on which
                                                     momentum (OAM) has witnessed significant experimen-               there has been a significant body of work [75], motivated
                                                     tal progress [5–18]. This is chiefly motivated by the no-         in part by recent experiments [35, 42].
                                                     tion of an orbital torque, that is, a torque exerted on an           The modern theory of orbital magnetisation shows that
                                                     adjacent magnetisation by a non-equilibrium OAM den-              orbital magnetisation of charge carriers in solids can be
                                                     sity, and is regarded as an orbital analogue of the vari-         constructed via the Berry connection of Bloch wavefunc-
                                                     ous spin torque mechanisms that have received consider-           tions. This theory was derived using both semiclassical
                                                     able attention in magnetic systems [19–31]. One of the            and Wannier approaches [64–69], and has been used to
                                                     principal mechanisms responsible for the orbital torque is        describe the orbital magnetisation both in and out of
                                                     the orbital Hall effect (OHE), which represents a flow of         equilibrium [69, 73, 76]. Theoretical research on OAM
                                                     OAM in response to an electric field [32–34]. The OHE             dynamics in inversion symmetric systems has employed
                                                     has been actively studied recently spurred by its poten-          approaches that rely either on symmetry or on the atomic
                                                     tial application in magnetic memory devices [12, 35–62].          OAM operator, with virtually no work, to our knowl-
                                                        In light of the intense activity on orbital dynamics           edge, within the framework of the modern theory of or-
                                                     the overarching technological question concerns which             bital magnetisation. This is perhaps because the modern
                                                     mechanisms and which materials help us maximise or-               theory makes an explicit connection between the equi-
                                                     bital torques on ferromagnetic memory elements. In this           librium OAM and the Berry curvature, which has been
                                                     connection we recently showed that the bulk states of             studied overwhelmingly in systems that break inversion
                                                     topological insulators give rise to a large OHE in an elec-       symmetry. To summarise, an active search is underway
                                                     tric field, building on earlier work demonstrating that           for efficient orbitronic materials, while inversion symmet-
                                                     orbital and spin effects in topological insulator surface         ric systems have received little attention in the context
                                                     states are of a similar order of magnitude [63]. In gen-          of the modern theory of orbital magnetisation.
                                                     eral, orbital and spin effects cannot be distinguished ex-           In light of these outstanding questions, in this work
                                                     perimentally, and at the moment the only indication of            we propose bulk p-type semiconductors as promising
                                                     their relative magnitudes comes from theoretical calcula-         platforms for orbitronic applications. We demonstrate
                                                     tion. Moreover, whereas the equilibrium OAM in a clean            that holes in Si, Ge, GaAs, InAs and InSb exhibit
                                                                                                                       a large OHE with orbital Hall conductivities of order
                                                                                                                       103 (ℏ/e)Ω−1 cm−1 , a similar order of magnitude to the
                                                                                                                       spin Hall effect in Pt and the orbital Hall effect recently
                                                     ∗ Author    to whom correspondence     should   be   addressed:   observed in light metals [60, 77]. Additionally, we find
                                                       james.cullen@unsw.edu.au                                        that the OHE in spin-3/2 hole systems exceeds the spin-
                                                                                                                                 2

Hall effect (SHE) by 2-3 orders of magnitude. Of these                                            Ge dispersion
semiconductors, we believe hole-doped Ge to have partic-
ular promise as an orbitronic material. Aside from prox-                   0.5
imity to Si microfabrication, ensuring high sample quality                                 HH
comparable to Si, hole-doped Ge has the additional ad-                                     LH
                                                                           0.4             SO
vantages of ultrahigh mobilities [78, 79] and considerably
stronger spin-orbit coupling than Si, making it a material




                                                             Energy (eV)
of choice for electrically-operated semiconductor quan-                    0.3
tum computing.[80, 81] Additionally, a recent experiment
has demonstrated a large inverse orbital Hall effect in Ge
using YIG/W/Ge and YIG/Pt/Ge heterostructures [62].                        0.2
The results indicate that the magnitude of the OHE ef-                               ∆so
fect in Ge is of a similar order of magnitude to the SHE
in Pt, which is consistent with our results, and suggests                  0.1
similar magnitudes may be achieved in the other semi-
conductors investigated here.
                                                                            0                                               EF
   Our findings have several implications for orbitronics.
Firstly, they identify a set of common p-type semiconduc-                        0         0.1        0.2     0.3   0.4   0.5
tors as promising orbitronic materials. In this context,                                              k x (nm -1)
Ge and Si holes are optimal systems to test the size of
the orbital torque arising from the OHE experimentally,
                                                             Figure 1.    Dispersion for holes in Ge, showing the heavy
because the spin- and orbital-Edelstein effects are pro-     (HH), light (LH) and split-off (SO) hole bands. In this figure
hibited by symmetry in the bulk of these materials. This     the bands have been inverted so the energy is positive. Here
implies that only the OHE and SHE are present, and our       we have chosen a Fermi energy of 10 meV, which is the largest
calculation, treating OHE and SHE on the same footing,       Fermi energy we consider in this work.
shows that OHE ≫ SHE. Secondly, our work shows that
the OHE is present in inversion-symmetric systems even
within the framework of the modern theory of orbital
magnetisation. The modern theory is of course general,       didates for building orbitronic devices.
but has overwhelmingly been applied to systems breaking
inversion symmetry, which often ensure a sizable Berry
                                                                                     II.   RESULTS AND DISCUSSION
curvature. Nevertheless, in the Luttinger model, even
in the spherical approximation, the Berry curvature and
OAM are both finite at a given wave vector, even though                                          A.   Hamiltonian
their integrals over occupied states naturally vanish in
the absence of time-reversal breaking mechanisms. The          The valence band of diamond and zinc-blende semi-
finite Berry curvature and OAM are responsible for the       conductors can be described by the Luttinger-Kohn-Bir-
large OHE that we identify. Our results are a similar or-    Pikus Hamiltonian given in Refs. 83 and 84:
der of magnitude to recent computational studies for Ge
and Si, [75] although a direct comparison is somewhat         H0 =
                                                                                                                 √ 
                                                                                                    − √12 S − 2R
                                                               
difficult given the rather different methodology used in          P +Q     S       R          0
earlier approaches, which have focused on the atomic cen-                                          √          q          
                                                                S∗      P −   Q    0        R         2Q          3
                                                                                                                      S 
tred approximation. Unifying these different perspectives      
                                                                                                   q              2
                                                                                                                 √ 
                                                                                                                          
on a technical level will be an important undertaking for       R∗        0     P −  Q     −S         3 ∗
                                                                                                         S    −     2Q    ,
future studies. Finally, from a technical perspective, our
                                                               
                                                                             ∗        ∗
                                                                                                    √2 ∗          1     ∗
                                                                                                                          
                                                                0         R      −S       P +Q       2R − √2 S 
                                                                                                                         
results highlight once more the necessity of incorporat-
                                                                √1 ∗ √                     √
                                                                                 q                                       
                                                                                    3
ing quantum corrections in the evaluation of the OHE,          − 2 S       2Q        S       2R P − δso           0 
                                                                                                                          
                                                                √                  2
showing that once more the correction is larger than the                 q         √                                      
conventional contribution.                                       − 2R∗     3 ∗
                                                                           2 S   −   2Q    − √1 S
                                                                                               2
                                                                                                       0     P   −   δ so

   A short summary of this work is as follows: We cal-                                                                     (1)
                                                                                                             2       2
culate the orbital and spin Hall effects in the 4 & 6        where m0 is the bare electron mass,  √ P  =  −ℏ   γ 1 k   /2m  0,

band Luttinger-Kohn-Bir-Pikus Hamiltonian. We cal-           Q = ℏ2 γ2 /2m0 (2kz2 − k∥2 ), S = 3ℏ2 γ3 kz k− /m0 and
                                                                   √
culate both the conventional contribution and quantum        R = 3ℏ2 /2m0 (γ2 (kx2 − ky2 ) − 2iγ3 kx ky ), where γ1,2,3
corrections to the orbital current [82], showing that the    are the Luttinger parameters. This Hamiltonian de-
quantum corrections dominate. We find that the orbital       scribes 6 bands, 4 are degenerate at k = 0 these cor-
Hall conductivity in spin-3/2 hole systems exceeds the       respond to states with total angular momentum 3/2,
spin Hall conductivity by 2-3 orders of magnitude, and       the other 2 bands are separated by a large gap δso
we propose p-type Si, Ge, GaAs, InAs and InSb as can-        due to the spin-orbit coupling of the atomic orbital
                                                                                                                                                                 3

ξL · s and correspond the spin degenerate states with                                            combination L̂ = m   2 (r̂ × v̂ − v̂ × r̂), where v̂ is the veloc-
total angular momentum 1/2. The Hamiltonian H0 is                                                ity operator and r̂ the position operator. Note that the
a k · p Hamiltonian whose matrix elements, as well as                                            mass appearing in the OAM operator is the bare elec-
the Luttinger parameters, are determined by the ⟨u|p|m⟩                                          tron mass, hence for holes we use the negative of the
matrix elements of the basis states at the band edge                                             electron mass. The local circulation part of the equilib-
(k = 0). The Hamiltonian (1) is written in the basis                                             rium OAM for band m and wavevector k is calculated
{| 23 , 32 ⟩, | 32 , 12 ⟩, | 32 , − 12 ⟩, | 32 , − 32 ⟩, | 12 , 12 ⟩, | 12 , − 12 ⟩} where the   as Lm       m                     m
                                                                                                      i,k = − ℏ ϵijl Im⟨∂j umk |ϵk − H0 |∂l umk ⟩[64–69]. The
first number indicates the total angular momentum and                                            orbital angular momentum of 3D holes in band m and
the second number indicates its projection onto Jz .[84]                                         wave vector k, retaining the spherical approximation, is
    Holes with their total angular momentum equal to 3/2
                                                                                                                          3ℏγ̄ki
and Jz projection equal to ±3/2 at the band centre are                                                             Lm
                                                                                                                    i,k =   k (σz ⊗ I)
                                                                                                                                      mm
                                                                                                                                         ,                     (4)
known as heavy holes while those with Jz = ±1/2 are
known as light holes due to their different effective masses                                     where σz is the z Pauli matrix and I is the 2 × 2 identity
shown in Fig. 1. This figure also shows the two bands                                            matrix. It is evident from the above that, despite the
with total angular momentum equal to 1/2 with gap δso                                            presence of inversion symmetry in the Luttinger model,
– these are referred to as the split-off bands. The split-off                                    the Berry curvature of each band does not vanish, and
band gap energies for each of the semiconductors con-                                            the OAM is finite for a hole in band m with wavevector
sidered in this work are given in Tab. I. For materials                                          k. However, the integral of both the OAM and Berry
with a large split-off band gap such as Ge, GaAs, InAs                                           curvature over occupied states will vanish as expected,
and InSb, we can simply use the upper 4 × 4 block from                                           since the system has time reversal symmetry.        These
(1) to describe the system,[85] given that we only con-                                          results remain true if the spherical approximation is re-
sider small number densities/Fermi energies as indicated                                         moved and the model is extended to 6×6, as we do in the
in Fig. 1. We note that the effective spin-3/2 of hole sys-                                      remainder of this work, except the results can no longer
tems in such 4 × 4 models leads to dynamics that either                                          be written in a simple and revealing analytical form.
has no equivalent in electron systems [86] or is very dif-
ficult to observe in electron systems.[87] For describing
Si the 6 × 6 model is the minimum requirement due to                                                          C.    Non-equilibrium formalism
the smaller split-off band gap (∼ 40 meV) and the large
relative difference between the γ2 and γ3 Luttinger pa-                                             To evaluate the orbital and spin Hall effects we require
rameters. At the same time, qualitative insight can still                                        the non-equilibrium correction to the density matrix in
be gained by considering the effective spin-3/2 dynamics                                         an electric field, for which we use the linear response the-
of the top valence bands.                                                                        ory following the approach of Refs. 88 and 89. The single-
    Additionally, we can also use the spherical approxima-                                       particle density operator obeys the quantum Liouville
tion, which works well for Ge, GaAs, InAs and InSb, and                                          equation, ∂ ρ̂/∂t + (i/ℏ)[Ĥ, ρ̂] = 0, where Ĥ = Ĥ0 + ĤE .
reduces the effective Hamiltonian to
                                                                                                 Here Ĥ0 is the band Hamiltonian and ĤE = eE · r̂ is the
                                 ℏ2
                                       (γ1 + 52 γ̄)k 2 − 2γ̄(k · J )2 ,
                                                                                   
                 H0 = − 2m                                                                 (2)   potential due to the external electrical field. We work
                                                                                                 in the Hilbert space spanned by Bloch wave-functions
where Ji are the spin 3/2 matrices and γ̄ = (γ2 + γ3 )/2.                                          Ψmk = eik·r umk . In the crystal momentum repre-
The 4 × 4 spherical model above allows for the straight-                                         sentation the equilibrium density matrix has the diagonal
forward analytical calculation of the orbital current. In                                        form ρmn
                                                                                                        0k = fmk δmn , where fmk ≡ f (εmk ) is the Fermi-
this work employ the 4 × 4 model with and without the                                            Dirac distribution for band m. In an electric field the
spherical approximation, primarily for analytical insight,                                       density matrix can be written as ρ̂ = ρ0 + ρE , and, in
as well as the full 6×6 model for numerical accuracy. For                                        linear response, it has been shown that in the absence of
the 4 × 4 model in the spherical approximation we calcu-                                         disorder[88]
late the orbital and spin Hall conductivities analytically,
whereas for the other two models we calculate orbital                                                               f (εmk ) − f (εnk )
Hall conductivity numerically.                                                                              ρmn
                                                                                                             Ek =                       eE · Rmn
                                                                                                                                              k        ,       (5)
                                                                                                                        εmk − εnk

                                                                                                 where Rmnk     = ⟨unk |i∂umk /∂k⟩ is the Berry connection.
       B.      Equilibrium OAM and Berry curvature
                                                                                                 In this work we do not consider disorder-induced extrin-
                                                                                                 sic terms and instead focus only on the intrinsic contri-
   The Berry curvature for band m and wavevector k is                                            butions.
defined as Ωm
            i,k = ϵijl Im⟨∂j umk |∂l umk ⟩ and for 3D holes                                         Now, our evaluation of the orbital current follows the
in the spherical Luttinger model it takes the form                                               calculation in Ref.
                                                                                                                   1
                                                                                                                      82. The orbital current operator is
                                Ωm       ki mm                                                   defined as ȷ̂α  = 2 L̂α , v̂δ , where the OAM polarization
                                 i,k = − k3 Jz .                                         (3)                  δ
                                                                                                 is taken to be along the α-direction while the transport
The Berry curvature is closely related to the equilibrium                                        direction is denoted by δ. The expectation values of ȷ̂
OAM. The OAM operator is defined as the symmetrised                                              is then evaluated by taking the trace with the density
                                                                                                                                     4

matrix. Once ρmnEk is found the expectation value of the                 Expressions for the proper spin Hall current have been
orbital current can be written as                                     derived in Refs. 77, 90, and 91 using both semiclassical
                                                                      and fully quantum mechanical formalisms. Here we fol-
        mϵαβγ X            mm           mm
⟨ȷ̂α
   δ⟩ =   4        Rβ , ρEk       vδ , vγ    +                        low the quantum mechanical formulation based on Bloch
               m,k                                                    wavefunctions from Refs. 77 and 90. The general analyt-
                     h
                         DΞ0β
                                imn              mn                  ical expression for the intrinsic proper spin Hall conduc-
    mϵαβγ   X 2eEµ       Dkµ          + ℏvβ , ρEk                     tivity in systems with arbitrary degeneracies is
i     4                                                {vγ , vδ }nm
                       εn − εm                                           l
                                                                                       X X                  h
                                                                                                                mn nn′ n′ m
                                                                                                                                i
      m̸=n,k                                                            σij,SHE = − 2e
                                                                                     ℏ          f (ε mk )Im  R̃ i,k šl,k R̃j,k   , (7)
   mϵ     X  h      Dvδ mn nm
                       i
                                                                                         k mnn′
+ i 4αβγ       vγ ,        ρ ,
                    Dkβ k Ek
            m̸=n,k                                                    where s is the spin operator. The check over the spin
                                                         (6)          term indicates the inclusion of only band diagonal matrix
where m and  0 nmn
                   are band indices, E is the external elec-          elements and elements between degenerate states, and
tric field, Ξβ       = 12 Rmn
                           β (fm + fn ), and the covariant            the tilde over the Berry connection indicates the inclusion
derivative DO/Dkj = ∂O/∂kj − i[Rj , O]. This orbital                  of only matrix elements between non-degenerate states.
current expression (6) was derived in Ref. 82 and shown               The distinction between the conventional and proper spin
to be gauge invariant. The expression in (6) contains the             currents in the spin Hall effect is important for materials
quantum correction to the orbital current ∆j that arises              in which the spin is not conserved. A similar distinction
due to the inclusion of all matrix elements, intra-band               will likely need to be made with respect to the orbital
and inter-band, of the position and velocity operators.               current; however, the most appropriate way to do this
The conventional part of the orbital current is contained             remains an open question in the field. It was recently
in the first term of (6), but only contains the off-diagonal          shown in Ref. 92 that the OAM is conserved when there
components of the velocity operators, while the quantum               is no orbital magneto-electric effect in the bulk, and as
correction comprises all the other terms in (6). We note              such the definition used for the orbital current in this
that the conventional calculation of the orbital current              work is applicable to the models used.
only includes diagonal elements       of the OAM operator                Finally, whereas it is not the aim of the present paper
in the trace ⟨Jδα ⟩ = Tr 21 L̂α , v̂δ ρ, whereas the quan-
                            
                                                                      to revisit the substantial debate surrounding the spin-
tum correction accounts for the remainder of the matrix               Hall effect, we note in passing that a separate expres-
elements appearing in this trace. The conventional ap-                sion for the spin-Hall conductivity has been derived in
proach does not have a physical justification for ignor-              the literature. [91, 93] This expression is qualitatively
ing these terms. Additionally, the quantum corrections                very similar to ours and yields results of the same order
include terms corresponding to both local and itinerant               of magnitude, yet differs in a number of details, which
circulation, so these corrections are also important in ma-           will be discussed in a future publication. Nevertheless,
terials with their OAM localised about the atomic centre.             for the purposes of comparing OHE and SHE dynamics
In the limit where γ̄ → 0 all states become degenerate                these distinctions are immaterial, and we expect our ob-
and the intrisinc part of the nonequilibrium density ma-              servations to hold regardless of the explicit form used to
trix ρEk becomes zero, as such in this limit the orbital              determine the spin current.
current trivially vanishes.
   The quantum correction ∆j can be split into three con-
tributions ∆j1,2,3 [82]. The first contribution ∆j1 can be                              D.    OHE calculations
related to the generation of an inter-band polarization by
an applied electric field, displacing electrons away from               Here we present our results for the OHE, and include
their equilibrium center of mass. This dipole rotates,                results for the SHE to enable a complete characterisation.
generating an OAM, and the OAM is then convected                      We first derived analytical expressions for the orbital and
generating an orbital current. This mechanism can also                spin conductivities based on the spherical 4 × 4 model:
be used to describe the conventional contribution. The                derivations of these expressions can be found in SUP-
first quantum correction ∆j1 and the second ∆j2 are the               PLEMENTARY NOTES I–III. Additionally, we present
two most dominant contributions to the orbital current                numerical calculations of the orbital Hall conductivity
in holes. ∆j2 arises due to the interband matrix elements             based on both the 4 × 4 model and the 6 × 6 model with-
of the OAM operator, these elements represent the com-                out the spherical approximation.
ponents of the OAM that fluctuate with time. While                      The orbital Hall conductivity based on the analytical
these matrix elements do not contribute to the expecta-               calculation is plotted in Fig. 2, the figure shows all the
tion value of the OAM in equilibrium, they do contribute              orbital Hall conductivity components for Ge. We find
to the orbital current. The last contribution to quantum              the the orbital Hall conductivity to be of the same or-
correction ∆j3 arises due to the non-commutativity of                 der of magnitude to the spin Hall effect in Pt and the
the position and velocity operators. For both the 4 × 4               orbital Hall effect in light metals [60, 77]. Moreover, as
and 6 × 6 Luttinger models, ∆j3 has opposite sign to all              shown in Fig. 2, the quantum corrections ∆σ1,2 are the
other contributions to the orbital current.                           dominant contributions to the orbital Hall conductivity.
                                                                                                                                                      5

                         Ge OHE in spherical approximation                                                    SHE in p-type semiconductors
                         0.1                                                                                      Ge
                                                                                                       1.5

                         0.0                                                                                      GaAs

                                                                                                       1.0        InAs
                        - 0.1




                                                                      σ zx, SHE × 10- 3 ( e nm- 1 )
                                                                                                                  InSb
    σ y zx (e nm- 1 )




                        - 0.2                                                                          0.5

                        - 0.3
                                    σL
                                                                                                       0.0
                        - 0.4       σ conv




                                                                     y
                        - 0.5
                                    Δσ 1                                                              - 0.5
                                    Δσ 2
                        - 0.6
                                    Δσ 3                                                              - 1.0
                                0        2   4      6   8    10
                                                                                                              0          2   4       6     8     10
                                                                                                                             EF ( meV)
                                             EF (meV)
                                                                  Figure 3. The proper spin Hall conductivity vs the Fermi
Figure 2. The orbital Hall conductivity vs the Fermi energy in
                                                                  energy in for four semiconductors in the spherical approxi-
Ge in the spherical approximation. We have also plotted the
                                                                  mation. Here we use the Luttinger parameters from Ref. 84.
conventional part of the orbital Hall conductivity σconv along
                                                                  Note the difference of three orders of magnitude in the scale
with the quantum corrections ∆σ. Here we use the Luttinger
                                                                  of the y-axis as compared to the orbital Hall conductivity.
parameters γ1 = 13.38 and γ̄ = 4.97.



                                                                  obtained using the spherical approximation and the reg-
The dominance of the quantum correction is consistent             ular 4 × 4 model is 8% for Ge. Furthermore, we find
with our previous results in Refs. 52 and 82, and high-           that the inclusion of the split-off band does not signifi-
lights the importance of including these corrections when         cantly affect the magnitude of the orbital Hall conduc-
calculating the orbital current.                                  tivity (correction of 12%). As such, we do not expect the
   We have plotted the spin Hall conductivity vs the              inclusion of further bands to have a significant effect on
Fermi energy in Fig. 3, as shown in the figure we find            the magnitude of the orbital Hall conductivity because
the spin Hall conductivity to be 2-3 orders of magnitude          of the increasingly large energy separations with the hole
smaller than the orbital Hall conductivity. We have ex-           bands. The main changes in the results between the 4×4
cluded Si from Fig. 3 due to the inapplicability of the           and 6 × 6 models are in the conventional term and the
spherical approximation to this material. We find the             third quantum correction; however, these contributions
spin and orbital conductivities to have the same sign in          almost exactly cancel.
both Ge, Si and GaAs, while in InAs and InSb their signs             Using the full 6 × 6 model we have plotted the orbital
are opposite. The spin and orbital conductivities having          Hall conductivity for Ge, Si, GaAs, InAs and InSb in
the same sign in Ge and Si differs from the ab-initio cal-        Fig. 5. We find the orbital Hall conductivity to be of
culation of Ref. 75. At the moment, however, our results          comparable magnitude in all materials studied 10−1 −100
and the results of Ref. 75 cannot be compared directly,           e nm−1 . As such, all of these semiconductors exhibit
since Ref. 75 introduced the OAM from the perspective             very large orbital Hall effects and have potential for use
of atomic orbitals, which is somewhat different from the          in building orbitronic devices.
way it is determined in the modern theory. Furthermore,
for completeness we indicate that Ref. 75 focussed on the
conventional spin current, which can have opposite sign                                                   E.      Implications for orbitronics
to the proper spin current[77]. However, the conventional
and proper spin currents typically yield results that are            Our main finding is that the OHE of holes in bulk semi-
close in magnitude.                                               conductors is very large, it is 2-3 orders of magnitude
   We have numerically calculated the orbital Hall con-           larger than the SHE and is of a similar order of mag-
ductivity using the 4 × 4 and 6 × 6 Luttinger models              nitude to the OHE calculated in weakly SOC metals in
without the spherical approximation to compare with our           Ref. 60. We have plotted the orbital Hall conductivity vs
analytical 4 × 4 calculation. A plot of the orbital Hall          the Fermi energy for these semiconductors in Fig. 5, we
conductivity including all components for these models            considered the most common semiconductors described
is shown in Fig. 4 for comparison with Fig. 2. As is              by the Luttinger Hamiltonian: Si, Ge, GaAs, InAs and
shown, the difference between orbital Hall conductivities         InSb. In all of these calculations we have used the 6 × 6
                                                                                                                                      6

                          Ge OHE in 4 × 4 and 6 × 6 models                                        OHE in p-type semiconductors
      a)                                                                                   0.0

                       0.0
                                                                                          - 0.5




                                                                      σ y zx (e nm- 1 )
                      - 0.2
  σ y zx (e nm- 1 )




                                                                                          - 1.0


                                  σL                                                                  Ge
                                                                                          - 1.5
                      - 0.4                                                                           Si
                                  σ conv
                                  Δσ 1                                                                GaAs
                                                                                          - 2.0
                                  Δσ 2                                                                InAs
                      - 0.6
                                  Δσ 3                                                                InSb
                                                                                          - 2.5
                                                                                                  0        2   4      6     8    10
                              0        2   4     6    8      10
                                                                                                               EF (meV)
                                           EF (meV)
                                                                  Figure 5. The orbital Hall conductivity vs Fermi energy for
      b) 0.2                                                      various hole-doped semiconductors calculated using the 6 ×
                                                                  6 Luttinger Hamiltonian. Luttinger parameters have been
                                                                  taken from Ref. 84.
                       0.0
  σ y zx (e nm- 1 )




                      - 0.2                                       bility of holes in Si and a greater order of magnitude than
                                                                  the mobility in GaAs, InAs and InSb [96–101]. From this
                                                                  perspective, since the OHE in Ge is greater than in Si,
                                  σL                              Ge is an optimal material for orbitronic applications. We
                      - 0.4
                                  σ conv                          also note that, although efficient OAM injection via OHE
                                                                  requires a 3D structure, mobilities measured in 2D Ge
                                  Δσ 1                            structures are considerably higher than the above value,
                      - 0.6
                                  Δσ 2                            offering the prospect of further improvement[78, 79].
                                                                     Our study, taken together with the observations above,
                                  Δσ 3                            suggests the viability of Ge-metal interfaces, for example
                      - 0.8
                              0        2   4     6    8      10   Ge/Co, where Co is a metal of choice in spintronic fer-
                                           EF (meV)               romagnetic structures [102, 103]. This interface, and its
                                                                  relatives, have featured in a number of studies [104–107],
                                                                  including a recent study linked to spin injection [104],
Figure 4. The orbital Hall conductivity vs the Fermi energy
                                                                  but we are not aware of its use for orbitronic applica-
in Ge for a) the 4 × 4 Luttinger Hamiltonian and b) the 6 × 6
Luttinger Hamiltonian without the spherical approximation.        tions. Given the difference in magnitude of the spin and
We have plotted the conventional part of the orbital Hall con-    orbital Hall effects we can expect that for any significant
ductivity σconv along with the quantum corrections ∆σ. Here       orbital-to-spin conversion > 0.2% the orbital Hall effect
we use γ1 = 13.38, γ2 = 4.24 and γ3 = 5.69.                       will dominate the torque in a Ge/ferromagnetic device.
                                                                  Fig. 6 shows a provisional sketch that illustrates one pos-
                                                                  sible geometry for a Ge orbital torque device. The Ge/Co
                                                                  device depicted in Fig. 6 includes a hypothetical barrier
Luttinger Hamiltonian without the spherical approxima-            layer, as these layers are often used to assist with orbital-
tion and including the split-off band. Despite p-type Ge          to-spin conversion [12, 14], however, the barrier layer may
exhibiting the third largest orbital Hall conductivity of         not be necessary. In such a device the orbital Hall effect
the materials studied we believe it is the best candidate         can be studied via the magnetisation dynamics in the
for building orbitronic devices. Ge is grown to a high            ferromagnet [108].
degree of purity resulting in ultrahigh quality samples,             In order for an orbital current to exert a torque on
benefits from its proximity to Si microfabrication tech-          a magnetisation it is thought that the OAM undergoes
nologies, and exhibits substantial hole mobilities even in        an orbital-to-spin conversion process, the exact mecha-
the bulk. The time of flight hole mobility in 3D Ge at 40K        nisms behind this phenomenon are largely unknown for
has been measured to be of the order of 105 cm2 /(Vs)             all forms of the Bloch OAM. As such, methods for en-
[94, 95], this is a similar order of magnitude to the mo-         hancing the orbital-to-spin conversion are still rather am-
                                                                                                                               7

                         Band gaps                                             Orbital torque in a Ge device
          Ge        Si        GaAs       InAs      InSb
∆so (eV) 0.296      0.0441     0.341     0.380     0.810
∆c (eV) 0.8         3.4        1.5       0.42      0.24

Table I. The split-off band energy splitting ∆so and direct                    M                                       Co
valence-conduction band gaps ∆c for different semiconduc-
tors, values taken from Ref. 84.

                                                                     z
biguous. Although there is a proposed mechanism for
the atomic OAM converting to spin via on-site spin-orbit                                                    y
coupling, this mechanism lacks rigorous theoretical justi-                x                              Jzx
fication. Additionally, the details of the transport of the          y          E
Bloch OAM, both local and itinerant, and its conserva-                                                                 Ge
tion across interfaces are again open questions in the field.
So, calculations of the orbital Hall conductivity are the       Figure 6. Diagram of the orbital Hall torque in a Ge/Co het-
primary indicator of whether a material can generate a          erostructure. Here the applied electric field generates trans-
large orbital torque. Our calculations for the orbital Hall     verse orbital currents via the intrinsic orbital Hall effect. The
effect in p-type semiconductors is the same order of mag-       orbital current will generate an orbital accumulation. The
nitude as what has been theoretically predicted for Ti,         orbital angular momentum is then converted into spin which
however, measurements for the orbital torque in Ti/Ni           generates a torque on the magnetisation in the Co layer. A
bilayers have estimated the orbital Hall conductivity to        barrier layer may be used to assist with orbital-to-spin con-
be an order of magnitude smaller[35], this discrepancy is       version.
likely due to the combination of the orbital transparency
of the interface and the orbital-to-spin conversion effi-
ciency of the device.                                           larger spin-orbit coupling in holes compared with elec-
                                                                trons in Si, we expect p-type Si to potentially exhibit an
                                                                even larger orbital torque.
          F.   Testbed for orbital Hall torque

   Distinguishing orbital and spin effects is not possible      G.       Inversion symmetric structures and the modern
using currently available experimental techniques, and                                    theory
at the moment the best one can do is to calculate these
effects theoretically and determine whether one clearly           The primary technological motivation of the present
dominates over the others. Similarly, distinguishing be-        work is to uncover the orbitronic properties of p-type
tween angular momentum generated via different mecha-           semiconductors by determining the OHE in of holes
nisms is equally challenging. In addition to the spin Hall      within the framework of the modern theory of orbital
effect, a steady-state spin density can be generated in an      magnetisation, incorporating the quantum corrections,
electric field via the magneto-electric effect, also known      and studying the OHE and SHE on the same footing.
as the Edelstein effect [109, 110]. Likewise, the orbital       At the moment there is no study of the OAM and OHE
magneto-electric effect refers to the intrinsic generation      for the Luttinger Hamiltonian in the modern theory.
of a steady state orbital polarization by an electric field     A strong theoretical motivation for working within the
[73, 111–122]. However, the spin- and orbital-Edelstein         modern theory is the need to understand (i) the OHE in
effects require gyrotropic symmetry, which is absent in         inversion-symmetric spin-3/2 systems within this frame-
zincblende materials. Given that the orbital Hall con-          work, as well as (ii) the role of spin-orbit coupling in
ductivity is three orders of magnitude larger than the          giving rise to the OHE.
spin Hall conductivity in Ge holes and two orders larger          To illustrate this need we emphasise that our results
in Si holes, this suggests that in the bulk virtually all the   are in sharp contrast to the earlier method introduced in
angular momentum dynamics comes from the OHE. The               Ref. 32, where a nominally similar calculation was per-
dynamics near the interface need to be examined sepa-           formed for Si holes, which, however, neglected spin-orbit
rately, since other mechanisms may contribute to angular        coupling. The Hamiltonian of Ref. 32 was expressed in
momentum accumulation there [93], nevertheless we ex-           terms of a pseudo-OAM operator, and the transport of
pect OHE to be a strong contributor there. Hence, our           this pseudo-OAM was investigated in the absence of spin-
results indicate that 3D Ge and Si structures are suitable      orbit coupling, yielding finite results. Nevertheless, if
testbeds for the strength of the orbital Hall torque[123].      one were to calculate the OAM for this effective Hamil-
Additionally, it was recently demonstrated that n-type          tonian according to the modern theory the result will
Si can exhibit a sizable orbital torque[124]. Due to the        immediately seen to be zero since spin-orbit coupling is
                                                                                                                       8

absent. Within the modern theory the OAM in the Lut-          perspective, exemplified by Ref. 75, takes as its start-
tinger Hamiltonian is entirely due to the spin-orbit inter-   ing point the OAM of atomic states and constructs the
action encapsulated in the Luttinger parameters γ2 and        overall OAM response of a solid to an electric field.
γ3 . Hence one cannot speak of OHE, or any OAM ef-            The other perspective is provided by the modern the-
fects, in a hole gas in the modern theory in the absence      ory, whose Bloch function formulation is used in this
of spin-orbit coupling. This is consistent with the find-     work, and which can also be cast in terms of Wannier
ings of a recent theory of angular momentum transport.        functions[2, 64–69]. The quantities calculated using these
[93] It follows that the pseudo-OAM contained in the ba-      methodologies are clearly related and lead to the same
sis envelope functions of Ref. 32, which can be regarded      observable. The modern theory and atomic OAM have
as a parent Hamiltonian of the Luttinger Hamiltonian, is      produced consistent results for the orbital magnetisation
a distinct physical quantity from the OAM of the mod-         for materials with their OAM concentrated about the
ern theory. The approach of Ref. 32 is already of ques-       atomic centre. [135] As such, since the modern theory ac-
tionable validity for Si, where spin-orbit coupling is not    counts for all components of Bloch electron OAM not just
negligible for hole systems, in fact it has been used very    the local circulation,[66, 69] the atomic OAM approach
successfully for electrical spin manipulation in quantum      is assumed to be subsumed by the modern theory, with
computing. Such an approach would be entirely incor-          the exception of some 2D models in which in-plane OAM
rect for Ge, GaAs, InAs and InSb, where spin-orbit cou-       in the modern theory is forbidden. The exact relation-
pling is inherently strong. Likewise, Ge has been used to     ship between the atomic OAM and modern theory has
achieve fast EDSR [125] as well as two-qubit logic [126]      not been clarified to date. Determining where these per-
in hole qubits. This motivated us to cast a fresh glance      spectives intersect will be a task for future studies. Both
at the OHE in spin-3/2 hole systems in the context of         approaches show that OAM conservation is not guaran-
the modern theory.                                            teed [92, 136, 137], however, in the modern theory the
   An additional motivation is the fact that studies within   conditions required for OAM conservation have been de-
the modern theory often focus on inversion breaking           termined [92]. Since there is no orbital magneto-electric
systems[50, 73, 82, 127–131], which typically exhibit large   effect in the Si and Ge there will be no net torque on
values of the Berry curvature[131]. Yet, as is evident in     the OAM captured by the modern theory, and hence
this work, a large Berry curvature and OAM do not re-         the OAM will be conserved in these materials. In this
quire inversion symmetry breaking [132]: they are large       context we note that the fundamental definition of the
for spin-3/2 holes described by the Luttinger Hamilto-        magnetic moment has also come under scrutiny recently
nian, even when the spherical approximation is applied.       [138]. Although disorder can dominate the conventional
The correct symmetry analysis for the Berry curvature         contribution to the orbital Hall conductivity in certain
was performed in Ref. 133. Additionally, for centrosym-       systems[36, 58], we have ignored disorder effects in this
metric, time-reversal-invariant systems in which the or-      work. In general for a full calculation of the orbital cur-
bital Berry curvature is zero, such as those considered       rent the exact role of disorder is unknown at this point in
in Ref. 134, we find that while the conventional contri-      time. As disorder is yet to be properly treated in a com-
bution to the OHE is zero the total OHE including the         plete evaluation of the orbital current including quantum
quantum correction can be nonzero.                            corrections beyond a simple relaxation time approxima-
   Nevertheless it is important to keep in mind the lim-      tion [82], we intend to address this in future work.
itations of effective mass studies, whose applicability is
restricted to the conduction and valence band extrema.
The orbital Hall conductivity for the full band structure                  H.   Role of Zitterbewegung
of Ge and Si was recently calculated using ab initio tech-
niques in Ref. 75, while accounting fully for spin-orbit         In this work we have focussed on intrinsic effects in
effects. In the regions where numerical comparison is         the presence of an electric field. These stem from the
possible our results are approximately of the same order      inter-band part of the density matrix and are related to
of magnitude, though it should be noted that the mag-         inter-band mixing induced by an electric field, in other
nitude of our results grows much faster with the Fermi        words, Zitterbewegung. All contributions to the intrin-
energy. However, a direct comparison is challenging at        sic orbital and spin currents arise due to interband el-
the moment, since Ref. 75 used a basis of atomic OAM          ements of the nonequilibrium density matrix and Berry
states, and the OAM operator entering the orbital cur-        connection. In the absence of spin-orbit coupling the Lut-
rent is the atomic OAM operator. In our evaluation, the       tinger parameters γ2 and γ3 vanish, as does the split-off
OAM is computed using the modern theory and the ef-           energy gap, hence the split-off band will become degen-
fective mass envelope functions, incorporating additional     erate with the light and heavy hole bands at k = 0.
quantum corrections which we recently shown to be vital       Thus, in the limit of vanishing spin-orbit coupling, all
in this formulation.                                          states are degenerate so the interband elements of the
   These observations open up an important and inter-         non-equilibrium density matrix vanish. Additionally, the
esting question for future research. At the moment two        Hamiltonian becomes proportional to the identity ma-
perspectives exist in the study of OAM in solids. One         trix and the Berry connection also vanishes. In this limit
                                                                                                                        9

the effects discussed in this work will vanish (although       will be: ∼ 3 times smaller in Si, similar in GaAs, and
in practice the OHE and SHE may have small contri-             ∼ 2 − 5 times greater in Ge, InAs, and InSb. Based on
butions due to Zitterbewegung involving the conduction         these figures, we estimate that a calculation using the
band, which is not included here, as explained below).         8 × 8 Luttinger model including the conduction band for
Nevertheless, in general spin-orbit coupling is not neces-     Si and GaAs is likely to introduce a correction to the
sary to generate an OHE. The key mechanism is Zitter-          orbital Hall conductivity of ∼ 10%, in Ge and InAs we
bewegung [82, 127, 139], which can be associated with          expect the correction to be larger ∼ 30 − 40%. For InSb
spin-orbit coupling as it is here, with pseudospin dynam-      there could be a correction as large as ∼ 80% from includ-
ics as in graphene, or with some other phenomenon in           ing the conduction band, given the large values calculated
more complex band structures.                                  for InSb such a correction would still yield a sizable or-
                                                               bital Hall conductivity. With this in mind the results for
                                                               InSb should be viewed as indicative, with further analy-
    I.   Limits of applicability of the k · p method           sis required. Nevertheless, very generally, the correction
                                                               obtained by including the split-off band is only a fraction
                                                               of the orbital Hall conductivity arising from the original
   The k · p models used in this work are low k expan-
                                                               4 × 4 model, and therefore even when considering the
sions about the valence band centre [84]. The Berry
                                                               limitations of our approach, the core conclusions of this
connection and curvature play crucial roles in the mod-
                                                               work are still valid: a large orbital Hall effect exists in
ern theory of orbital magnetisation. These quantities of-
                                                               p-type semiconductors, and it is dominated by the quan-
ten require more sophisticated models to effectively cap-
                                                               tum correction.
ture the behaviour of the Bloch wavefunction. How-
ever, at the low carrier densities we are interested in
to describe semiconductor transport, the most impor-                               III.   CONCLUSIONS
tant quantity that needs to be captured is the Berry
curvature monopole at the band centre which decays
as 1/k 2 . The k · p Hamiltonians we use here are ex-            We have demonstrated that hole-doped semiconduc-
panded in terms of the Bloch wavefunction at the band          tors Ge, Si, GaAs, InAs and InSb exhibit a large or-
edge (k =                                                      bital Hall effect and are suitable platforms for orbitronic
          Pk0 )[85, 140]. This expansion takes the form        applications. The OHE response stems from Zitterbewe-
|umk ⟩ = n cnmk |uP   nk0 ⟩, and the derivative is expressed
as ∂/∂k α |umk ⟩ =              α                              gung induced by spin-orbit coupling, is dominated by the
                        n (∂/∂k cnmk )|unk0 ⟩ which enters
the Berry connection and the Berry curvature. These            quantum correction, and exceeds the spin-Hall effect by
wavefunctions are then approximated by retaining only          2-3 orders of magnitude. The absence of spin and orbital
a few bands that are close in energy. This is an excel-        Edelstein effects suggests both Ge and Si as platforms
lent approximation for the small Fermi energies consid-        for testing the strength of the orbital Hall torque. Fi-
ered in this work EF < 10 meV. Since these Fermi ener-         nally, our work shows that the OAM and OHE calculated
gies also correspond to the most experimentally accessi-       within the framework of the modern theory of orbital
ble carrier densities there is no loss of generality. Addi-    magnetisation are strong for the Luttinger Hamiltonian
tionally, effectively implementing the modern theory of        even in the spherical approximation, providing an exam-
orbital magnetism through more sophisticated ab-initio         ple of strong orbital dynamics in an inversion-symmetric
models can be very expensive computationally, often re-        system.
quiring a large number of atomic orbitals spanning a sub-
stantial energy range. [141]
                                                                             IV.     DATA AVAILABILITY
   Including coupling to further bands will give correc-
tions to the values calculated in this work, and these cor-
rections will depend on the ratio of the k · p coupling          The authors declare that the data supporting the find-
strength to the direct energy gap between the bands.           ings of this study are available within the paper and its
The difference in the orbital Hall conductivity between        supplementary information file.
the 4 × 4 and 6 × 6 models is 12% for Ge, as is shown in
Fig. 4. An important point to note is that the conduction
band coupling elements may be fairly sizable and could                  V.    AUTHOR CONTRIBUTIONS
introduce non-negligible corrections. Values for the di-
rect conduction-valence band gap δc are given in Tab. I.          J. H. C and Z. W performed the orbital and spin Hall
For the carrier densities considered in this work the con-     effect calculations. J. H. C made the figures. J. H. C and
duction band coupling to band gap ratio can be up to:          D. C wrote the manuscript. D. C Supervised the project.
18% in Si, 23% in GaAs, 61% in Ge, 71% in InAs and
108% in InSb. The coupling strength to gap ratios for all
other bands are much smaller and should introduce neg-                  VI.    COMPETEING INTERESTS
ligible corrections [84]. The conduction band coupling to
gap ratio compared to the split-off band coupling ratio          The authors declare no competing interests.
                                                                                                                              10

          VII.    ACKNOWLEDGEMENTS                                lowship FT190100062. We are very grateful to Tatiana
                                                                  Rappoport, Hyun Woo Lee, Kyoung-Whan Kim, Jung
  . This work is supported by the Australian Research             Hoon Han, Francesco Borsoi, Joe Salfi, and Henri Jaffres
Council Discovery Project DP2401062 and Future Fel-               for stimulating discussions.




 [1] D. Das, Orbitronics in action, Nature Physics 19, 1085–            Communications Physics 6, 32 (2023).
     1085 (2023).                                                  [14] T. Li, L. Liu, X. Li, X. Zhao, H. An, and K. Ando,
 [2] R. B. Atencia, A. Agarwal, and D. Culcer, Orbital an-              Giant orbital-to-spin conversion for efficient current-
     gular momentum of bloch electrons: equilibrium for-                induced magnetization switching of ferrimagnetic in-
     mulation, magneto-electric phenomena, and the orbital              sulator, Nano Letters 23, 7174–7179 (2023), pMID:
     Hall effect, Advances in Physics: X 9, 2371972 (2024),             37466330.
     https://doi.org/10.1080/23746149.2024.2371972.                [15] J. Xiao, Y. Liu, and B. Yan, Memorial Volume for
 [3] D. Go, D. Jo, H.-W. Lee, M. Kläui, and Y. Mokrousov,              Shoucheng Zhang (World Scientific, 2021) Chap. Chap-
     Orbitronics: Orbital currents in solids, Europhysics Let-          ter 13, pp. 353–364.
     ters 135, 37001 (2021).                                       [16] Y. Tokura, K. Yasuda, and A. Tsukazaki, Magnetic
 [4] P. Wang, F. Chen, Y. Yang, S. Hu, Y. Li, W. Wang,                  topological insulators, Nature Reviews Physics 1, 126–
     D. Zhang, and Y. Jiang, Orbitronics: Mechanisms, ma-               143 (2019).
     terials and devices, Advanced Electronic Materials ,          [17] D. Go, D. Jo, K.-W. Kim, S. Lee, M.-G. Kang, B.-G.
     2400554 (2024).                                                    Park, S. Blügel, H.-W. Lee, and Y. Mokrousov, Long-
 [5] J. Kim, D. Go, H. Tsai, D. Jo, K. Kondou, H.-W.                    range orbital torque by momentum-space hotspots,
     Lee, and Y. Otani, Nontrivial torque generation by                 Physical review letters 130, 246701 (2023).
     orbital angular momentum injection in ferromagnetic-          [18] N. H. Aase, E. W. Hodt, K. B. Hallberg, A. Sudbø, and
     metal/Cu/Al2 O3 trilayers, Phys. Rev. B 103, L020407               J. Linder, Orbital splitter effect and spatial resolution
     (2021).                                                            of current-induced orbital accumulation, Phys. Rev. B
 [6] X. Chen, Y. Liu, G. Yang, H. Shi, C. Hu, M. Li, and                112, 014409 (2025).
     H. Zeng, Giant antidamping orbital torque originating         [19] A. Sakai and H. Kohno, Spin torques and charge trans-
     from the orbital Rashba-Edelstein effect in ferromag-              port on the surface of topological insulator, Physical
     netic heterostructures, Nature Communications 9, 2569              Review B 89, 165307 (2014).
     (2018).                                                       [20] K. Yasuda, A. Tsukazaki, R. Yoshimi, K. Kondou,
 [7] D. Go and H.-W. Lee, Orbital torque: Torque gener-                 K. Takahashi, Y. Otani, M. Kawasaki, and Y. Tokura,
     ation by orbital current injection, Phys. Rev. Res. 2,             Current-nonlinear Hall effect and spin-orbit torque mag-
     013177 (2020).                                                     netization switching in a magnetic topological insulator,
 [8] D. Lee, D. Go, H.-J. Park, W. Jeong, H.-W. Ko, D. Yun,             Physical review letters 119, 137204 (2017).
     D. Jo, S. Lee, G. Go, J. H. Oh, K.-J. Kim, B.-G. Park,        [21] G. Tatara, H. Kohno, J. Shibata, Y. Lemaho, and K.-J.
     B.-C. Min, H. C. Koo, H.-W. Lee, O. Lee, and K.-J.                 Lee, Spin torque and force due to current for general
     Lee, Orbital torque in magnetic bilayers, Nature Com-              spin textures, Journal of the Physical Society of Japan
     munications 12, 6710 (2021).                                       76, 054707–054707 (2007).
 [9] Z. C. Zheng, Q. X. Guo, D. Jo, D. Go, L. H. Wang,             [22] H. Kohno, G. Tatara, and J. Shibata, Microscopic calcu-
     H. C. Chen, W. Yin, X. M. Wang, G. H. Yu, W. He, H.-               lation of spin torques in disordered ferromagnets, Jour-
     W. Lee, J. Teng, and T. Zhu, Magnetization switching               nal of the Physical Society of Japan 75, 113706–113706
     driven by current-induced torque from weakly spin-orbit            (2006).
     coupled zr, Phys. Rev. Res. 2, 013127 (2020).                 [23] K. Belashchenko, A. A. Kovalev, and M. Van Schilf-
[10] S. Lee, M.-G. Kang, D. Go, D. Kim, J.-H. Kang, T. Lee,             gaarde, First-principles calculation of spin-orbit torque
     G.-H. Lee, J. Kang, N. J. Lee, Y. Mokrousov, S. Kim,               in a co/pt bilayer, Physical Review Materials 3, 011401
     K.-J. Kim, K.-J. Lee, and B.-G. Park, Efficient con-               (2019).
     version of orbital Hall current to spin current for spin-     [24] A. Manchon, J. Železný, I. M. Miron, T. Jungwirth,
     orbit torque switching, Communications Physics 4, 234              J. Sinova, A. Thiaville, K. Garello, and P. Gambardella,
     (2021).                                                            Current-induced spin-orbit torques in ferromagnetic
[11] S. Ding, A. Ross, D. Go, L. Baldrati, Z. Ren,                      and antiferromagnetic systems, Rev. Mod. Phys. 91,
     F. Freimuth, S. Becker, F. Kammerbauer, J. Yang,                   035004 (2019).
     G. Jakob, Y. Mokrousov, and M. Kläui, Harnessing             [25] B. K. Nikolić, K. Dolui, M. D. Petrović, P. Plecháč,
     orbital-to-spin conversion of interfacial orbital currents         T. Markussen, and K. Stokbro, First-principles quan-
     for efficient spin-orbit torques, Phys. Rev. Lett. 125,            tum transport modeling of spin-transfer and spin-orbit
     177201 (2020).                                                     torques in magnetic multilayers, Handbook of Materials
[12] G. Sala and P. Gambardella, Giant orbital Hall effect              Modeling: Applications: Current and Emerging Mate-
     and orbital-to-spin conversion in 3d, 5d, and 4f metallic          rials , 499–533 (2020).
     heterostructures, Phys. Rev. Res. 4, 033037 (2022).           [26] P. Gambardella and I. M. Miron, Current-induced spin–
[13] H. Hayashi, D. Jo, D. Go, T. Gao, S. Haku,                         orbit torques, Philosophical Transactions of the Royal
     Y. Mokrousov, H.-W. Lee, and K. Ando, Observation                  Society A: Mathematical, Physical and Engineering Sci-
     of long-range orbital transport and giant orbital torque,          ences 369, 3175–3197 (2011).
                                                                                                                                 11

[27] A. Qaiumzadeh, R. A. Duine, and M. Titov, Spin-orbit               torque in Nb/Ni and Ta/Ni bilayers, Phys. Rev. B 106,
     torques in two-dimensional Rashba ferromagnets, Phys.              184406 (2022).
     Rev. B 92, 014402 (2015).                                     [45] G. Sala, H. Wang, W. Legrand, and P. Gambardella, Or-
[28] R. A. Duine, A. S. Núñez, J. Sinova, and A. H. MacDon-           bital hanle magnetoresistance in a 3d transition metal,
     ald, Functional Keldysh theory of spin torques, Phys.              Phys. Rev. Lett. 131, 156703 (2023).
     Rev. B 75, 214420 (2007).                                     [46] J. Zhang, H. Xie, X. Zhang, Z. Yan, Y. Zhai, J. Chi,
[29] A. Brataas, A. D. Kent, and H. Ohno, Current-induced               H. Xu, Y. Zuo, and L. Xi, The giant orbital Hall effect
     torques in magnetic materials, Nature materials 11,                in Cr/Au/Co/Ti multilayers, Applied Physics Letters
     372–381 (2012).                                                    121, 172405 (2022).
[30] K. M. D. Hals and A. Brataas, Phenomenology of                [47] B. Bony, S. Krishnia, Y. Xu, S. Collin, A. Fert, J.-M.
     current-induced spin-orbit torques, Phys. Rev. B 88,               George, M. Viret, V. Cros, and H. Jaffrès, Quantita-
     085423 (2013).                                                     tive analysis of vectorial torques in thin 3d Co ferro-
[31] K. M. D. Hals and A. Brataas, Spin-motive forces and               magnet using orbital-spin conversion, arXiv e-prints ,
     current-induced torques in ferromagnets, Phys. Rev. B              arXiv–2501 (2025).
     91, 214401 (2015).                                            [48] A. El Hamdi, J.-Y. Chauleau, M. Boselli, C. Thibault,
[32] B. A. Bernevig, T. L. Hughes, and S.-C. Zhang, Orbi-               C. Gorini, A. Smogunov, C. Barreteau, S. Gariglio, J.-
     tronics: The intrinsic orbital current in p-doped silicon,         M. Triscone, and M. Viret, Observation of the orbital in-
     Phys. Rev. Lett. 95, 066601 (2005).                                verse Rashba–Edelstein effect, Nature Physics 19, 1855–
[33] T. Tanaka, H. Kontani, M. Naito, T. Naito, D. S. Hi-               1860 (2023).
     rashima, K. Yamada, and J. Inoue, Intrinsic spin Hall         [49] D. B. Fonseca, L. L. A. Pereira, and A. L. R. Barbosa,
     effect and orbital Hall effect in 4d and 5d transition met-        Orbital Hall effect in mesoscopic devices, Phys. Rev. B
     als, Phys. Rev. B 77, 165117 (2008).                               108, 245105 (2023).
[34] H. Kontani, T. Tanaka, D. S. Hirashima, K. Yamada,            [50] K. Shinada, A. Kofuji, and R. Peters, Quantum theory
     and J. Inoue, Giant orbital Hall effect in transition met-         of the intrinsic orbital magnetoelectric effect in itinerant
     als: Origin of large spin and anomalous Hall effects,              electron systems at finite temperatures, Phys. Rev. B
     Phys. Rev. Lett. 102, 016601 (2009).                               107, 094106 (2023).
[35] Y.-G. Choi, D. Jo, K.-H. Ko, D. Go, K.-H. Kim, H. G.          [51] L. M. Canonico, T. P. Cysne, T. G. Rappoport, and
     Park, C. Kim, B.-C. Min, G.-M. Choi, and H.-W. Lee,                R. Muniz, Two-dimensional orbital Hall insulators,
     Observation of the orbital Hall effect in a light metal            Physical Review B 101, 075429 (2020).
     Ti, Nature 619, 52–56 (2023).                                 [52] J. H. Cullen, H. Liu, and D. Culcer, Giant orbital Hall
[36] H. Liu and D. Culcer, Dominance of extrinsic scatter-              effect due to the bulk states of 3d topological insulators,
     ing mechanisms in the orbital Hall effect: Graphene,               npj Spintronics 3, 22 (2025).
     transition metal dichalcogenides, and topological anti-       [53] A. Kazantsev, A. Mills, E. O’Neill, H. Sun, G. Vignale,
     ferromagnets, Phys. Rev. Lett. 132, 186302 (2024).                 and A. Principi, Nonconservation of the valley density
[37] A. Pezo, D. Garcı́a Ovalle, and A. Manchon, Orbital                and its implications for the observation of the valley Hall
     Hall effect in crystals: Interatomic versus intra-atomic           effect, Phys. Rev. Lett. 132, 106301 (2024).
     contributions, Phys. Rev. B 106, 104414 (2022).               [54] H. Sun, A. Kazantsev, A. Principi, and G. Vignale, Non-
[38] L. Salemi and P. M. Oppeneer, First-principles the-                conserved density accumulations in orbital hall trans-
     ory of intrinsic spin and orbital Hall and nernst effects          port: Insights from linear response theory, Phys. Rev.
     in metallic monoatomic crystals, Phys. Rev. Mater. 6,              B 111, 075432 (2025).
     095001 (2022).                                                [55] H. Sun and G. Vignale, Theory of magnetoresis-
[39] T. P. Cysne, M. Costa, L. M. Canonico, M. B. Nardelli,             tance due to edge orbital moment accumulation, arXiv
     R. B. Muniz, and T. G. Rappoport, Disentangling or-                preprint arXiv:2408.02887 (2024).
     bital and valley Hall effects in bilayers of transition       [56] S. Bhowal and G. Vignale, Orbital Hall effect as an al-
     metal dichalcogenides, Phys. Rev. Lett. 126, 056601                ternative to valley Hall effect in gapped graphene, Phys.
     (2021).                                                            Rev. B 103, 195309 (2021).
[40] L. M. Canonico, T. P. Cysne, A. Molina-Sanchez, R. B.         [57] T. P. Cysne, S. Bhowal, G. Vignale, and T. G. Rap-
     Muniz, and T. G. Rappoport, Orbital Hall insulating                poport, Orbital Hall effect in bilayer transition metal
     phase in transition metal dichalcogenide monolayers,               dichalcogenides: From the intra-atomic approximation
     Phys. Rev. B 101, 161409 (2020).                                   to the bloch states orbital magnetic moment approach,
[41] S. R. Luis M. Canonico, Jose H. Garcı́a, Real-space cal-           Phys. Rev. B 105, 195421 (2022).
     culation of orbital Hall responses in disordered materi-      [58] A. Veneri, T. G. Rappoport, and A. Ferreira, Extrinsic
     als, arXiv:2404.01739 (2024).                                      orbital hall effect: Orbital skew scattering and crossover
[42] P. Wang, Z. Feng, Y. Yang, D. Zhang, Q. Liu, Z. Xu,                between diffusive and intrinsic orbital transport, Phys.
     Z. Jia, Y. Wu, G. Yu, X. Xu, and Y. Jiang, Inverse                 Rev. Lett. 134, 136201 (2025).
     orbital Hall effect and orbitronic terahertz emission ob-     [59] D. Go, D. Jo, C. Kim, and H.-W. Lee, Intrinsic spin
     served in the materials with weak spin-orbit coupling,             and orbital Hall effects from orbital texture, Phys. Rev.
     npj Quantum Materials 8, 28 (2023).                                Lett. 121, 086602 (2018).
[43] I. Lyalin, S. Alikhah, M. Berritta, P. M. Oppeneer, and       [60] D. Jo, D. Go, and H.-W. Lee, Gigantic intrinsic orbital
     R. K. Kawakami, Magneto-optical detection of the or-               Hall effects in weakly spin-orbit coupled metals, Phys.
     bital hall effect in chromium, Phys. Rev. Lett. 131,               Rev. B 98, 214405 (2018).
     156702 (2023).                                                [61] J. M. Lee, Universal intrinsic orbital dynamics from
[44] S. Dutta and A. A. Tulapurkar, Observation of nonlo-               berry curvature in electronic two-band systems, Physi-
     cal orbital transport and sign reversal of dampinglike             cal Review B 112, 054441 (2025).
                                                                                                                              12

[62] E. Santos, J. Abrão, J. Costa, J. Santos, G. Rodrigues-          der, Applied Physics Letters 123 (2023).
     Junior, J. Mendes, and A. Azevedo, Negative orbital          [80] G. Scappucci, C. Kloeffel, F. A. Zwanenburg, D. Loss,
     Hall effect in germanium, Physical Review Applied 22,             M. Myronov, J.-J. Zhang, S. De Franceschi, G. Kat-
     064071 (2024).                                                    saros, and M. Veldhorst, The germanium quantum in-
[63] S. R. Park, J. Han, C. Kim, Y. Y. Koh, C. Kim, H. Lee,            formation route, Nature Reviews Materials 6, 926–943
     H. J. Choi, J. H. Han, K. D. Lee, N. J. Hur, M. Arita,            (2021).
     K. Shimada, H. Namatame, and M. Taniguchi, Chi-              [81] Y. Fang, P. Philippopoulos, D. Culcer, W. Coish, and
     ral orbital-angular momentum in the surface states of             S. Chesi, Recent advances in hole-spin qubits, Materials
     bi2 se3 , Phys. Rev. Lett. 108, 046805 (2012).                    for Quantum Technology 3, 012003 (2023).
[64] J. Shi, G. Vignale, D. Xiao, and Q. Niu, Quantum the-        [82] H. Liu, J. H. Cullen, D. P. Arovas, and D. Culcer, Quan-
     ory of orbital magnetization and its generalization to            tum correction to the orbital Hall effect, Physical Re-
     interacting systems, Phys. Rev. Lett. 99, 197202 (2007).          view Letters 134, 036304 (2025).
[65] T. Thonhauser, D. Ceresoli, D. Vanderbilt, and               [83] J. M. Luttinger and W. Kohn, Motion of electrons and
     R. Resta, Orbital magnetization in periodic insulators,           holes in perturbed periodic fields, Physical Review 97,
     Phys. Rev. Lett. 95, 137205 (2005).                               869 (1955).
[66] D. Vanderbilt, Berry Phases in Electronic Struc-             [84] R. Winkler, Spin-Orbit Coupling Effects in Two-
     ture Theory: Electric Polarization, Orbital Magnetiza-            Dimensional Electron and Hole systems (Springer,
     tion and Topological Insulators (Cambridge University             Berlin, 2003).
     Press, 2018).                                                [85] W. W. Chow and S. W. Koch, Semiconductor-laser fun-
[67] R. Resta, Magnetic circular dichroism versus orbital              damentals: physics of the gain materials (Springer Sci-
     magnetization, Phys. Rev. Res. 2, 023139 (2020).                  ence & Business Media, 2013).
[68] D. Ceresoli, T. Thonhauser, D. Vanderbilt, and               [86] D. Culcer, C. Lechner, and R. Winkler, Spin precession
     R. Resta, Orbital magnetization in crystalline solids:            and alternating spin polarization in spin-3/2 hole sys-
     Multi-band insulators, chern insulators, and metals,              tems, Physical review letters 97, 106601 (2006).
     Phys. Rev. B 74, 024408 (2006).                              [87] H. Liu, E. Marcellina, A. Hamilton, and D. Culcer,
[69] T. Thonhauser, Theory of orbital magnetization in                 Strong spin-orbit contribution to the hall coefficient of
     solids, International Journal of Modern Physics B 25,             two-dimensional hole systems, Physical Review Letters
     1429–1458 (2011).                                                 121, 087701 (2018).
[70] J. Voss, I. Ado, and M. Titov, Non-equilibrium orbital       [88] D. Culcer, A. Sekine, and A. H. MacDonald, Interband
     edge magnetization, arXiv preprint arXiv:2405.11979               coherence response to electric fields in crystals: Berry-
     (2024).                                                           phase contributions and disorder effects, Phys. Rev. B
[71] S. Ding, Z. Liang, D. Go, C. Yun, M. Xue, Z. Liu,                 96, 035106 (2017).
     S. Becker, W. Yang, H. Du, C. Wang, Y. Yang,                 [89] R. B. Atencia, Q. Niu, and D. Culcer, Semiclassical re-
     G. Jakob, M. Kläui, Y. Mokrousov, and J. Yang, Ob-               sponse of disordered conductors: Extrinsic carrier veloc-
     servation of the orbital Rashba-Edelstein magnetoresis-           ity and spin and field-corrected collision integral, Phys.
     tance, Phys. Rev. Lett. 128, 067201 (2022).                       Rev. Res. 4, 013001 (2022).
[72] J. M. Lee, M. J. Park, and H.-W. Lee, Orbital Edelstein      [90] H. Liu, J. H. Cullen, and D. Culcer, Topological na-
     effect of electronic itinerant orbital motion at edges,           ture of the proper spin current and the spin-Hall torque,
     Physical Review B 110, 134436 (2024).                             Phys. Rev. B 108, 195434 (2023).
[73] C. Xiao, H. Liu, J. Zhao, S. A. Yang, and Q. Niu, Ther-      [91] C. Xiao and Q. Niu, Conserved current of nonconserved
     moelectric generation of orbital magnetization in met-            quantities, Phys. Rev. B 104, L241411 (2021).
     als, Phys. Rev. B 103, 045401 (2021).                        [92] R. B. Atencia, D. P. Arovas, and D. Culcer, Intrinsic
[74] A. Pezo, J.-M. George, and H. Jaffrès, Theory of spin            torque on the orbital angular momentum in an electric
     and orbital charge conversion at the surface states of            field, Phys. Rev. B 110, 035427 (2024).
     Bi1−x Sbx topological insulator, Physical Review Re-         [93] T. Valet, H. Jaffres, V. Cros, and R. Raimondi, Quan-
     search 6, 043332 (2024).                                          tum kinetic anatomy of electron angular momenta edge
[75] I. Baek and H.-W. Lee, Negative intrinsic orbital Hall            accumulation, arXiv preprint arXiv:2507.06771 (2025).
     effect in group xiv materials, Phys. Rev. B 104, 245204      [94] L. Reggiani, C. Canali, F. Nava, and G. Ottaviani, Hole
     (2021).                                                           drift velocity in germanium, Physical Review B 16, 2781
[76] A. Malashevich, I. Souza, S. Coh, and D. Vanderbilt,              (1977).
     Theory of orbital magnetoelectric response, New Jour-        [95] G. Ottaviani, C. Canali, F. Nava, and J. Mayer, Hole
     nal of Physics 12, 053032 (2010).                                 drift velocity in high-purity Ge between 8 and 220 k,
[77] H. Ma, J. H. Cullen, S. Monir, R. Rahman, and D. Cul-             Journal of Applied Physics 44, 2917–2918 (1973).
     cer, Spin-Hall effect in topological materials: evaluating   [96] G. Ottaviani, L. Reggiani, C. Canali, F. Nava, and
     the proper spin current in systems with arbitrary de-             A. Alberigi-Quaranta, Hole drift velocity in silicon,
     generacies, npj Spintronics 2, 55 (2024).                         Phys. Rev. B 12, 3318–3329 (1975).
[78] L. E. Stehouwer, C. X. Yu, B. van Straaten, A. Tosato,       [97] V. L. Dalal, A. Dreeben, and A. Triano, Temperature
     V. John, D. Degli Esposti, A. Elsayed, D. Costa, S. D.            dependence of hole velocity in p-gaas, Journal of Ap-
     Oosterhout, N. W. Hendrickx, et al., Exploiting strained          plied Physics 42, 2864–2867 (1971).
     epitaxial germanium for scaling low-noise spin qubits at     [98] S. Adachi, Properties of Group-iv, III-v and II-VI Semi-
     the micrometre scale, Nature Materials , 1–7 (2025).              conductors (John Wiley & Sons, 2005).
[79] L. E. Stehouwer, A. Tosato, D. Degli Esposti, D. Costa,      [99] A. Filipchenko and L. Bolshakov, Mobility of holes in p-
     M. Veldhorst, A. Sammak, and G. Scappucci, Germa-                 InSb crystals, physica status solidi (b) 77, 53–58 (1976).
     nium wafers for strained quantum wells with low disor-
                                                                                                                                 13

[100] F. Kesamanly, T. Lagunova, D. Nasledov, L. Nikolaeva,               ism angle-resolved photoemission spectroscopy, Physical
      and M. Pivovarov, Electrical properties of p-type crys-             Review B—Condensed Matter and Materials Physics
      tals of indium arsenide(p-type InAs single crystals elec-           85, 195401 (2012).
      tric properties from 2 to 300 degrees k reveal features       [117] A. Johansson, Theory of spin and orbital Edelstein ef-
      explainable by two band conductivity model), FIZIKA I               fects, Journal of Physics: Condensed Matter 36, 423002
      TEKHNIKA POLUPROVODNIKOV 2, 56–63 (1968).                           (2024).
[101] M. Zimpel, M. OSZWALDOWSKI, and J. Goc, Mo-                   [118] K. Osumi, T. Zhang, and S. Murakami, Kinetic magne-
      bility of holes in insb, Acta Physica Polonica. A 75,               toelectric effect in topological insulators, Communica-
      297–300 (1989).                                                     tions Physics 4, 211 (2021).
[102] S. D. Bader and S. S. P. Parkin, Spintronics, Annu. Rev.      [119] W.-Y. He, D. Goldhaber-Gordon, and K. T. Law, Giant
      Condens. Matter Phys. 1, 71–88 (2010).                              orbital magnetoelectric effect and current-induced mag-
[103] C. Felser, G. H. Fecher, and B. Balke, Spintronics: a               netization switching in twisted bilayer graphene, Nature
      challenge for materials science and solid-state chemistry,          communications 11, 1650 (2020).
      Angewandte Chemie International Edition 46, 668–699           [120] A. Johansson, B. Göbel, J. Henk, M. Bibes, and
      (2007).                                                             I. Mertig, Spin and orbital Edelstein effects in a two-
[104] Z. Nedelkoski, J. A. Do Nascimento, K. Hamaya, and                  dimensional electron gas: Theory and application to
      V. K. Lazarov, Effects of atomic structures at Co2 Fe               srtio3 interfaces, Phys. Rev. Res. 3, 013275 (2021).
      (Al0.5 , Si0.5 )/Ge interfaces on spin-electronic proper-     [121] D. Hara, M. S. Bahramy, and S. Murakami, Current-
      ties, Journal of Physics D: Applied Physics 58, 245301              induced orbital magnetization in systems without in-
      (2025).                                                             version symmetry, Phys. Rev. B 102, 184404 (2020).
[105] J.-S. Tsay, Y. Yao, W. Cheng, T. Tseng, K. Wang, and          [122] L. M. Canonico, J. H. GarcÃa, A. W. Cummings, and
      C. Yang, Magnetic properties influenced by interfaces               S. Roche, Spin polarization driven by itinerant orbital
      in ultrathin Co/Ge (1 0 0) and Co/Ge (1 1 1) films,                 angular momentum in van der waals heterostructures,
      Applied surface science 219, 88–92 (2003).                          arXiv preprint arXiv:2507.12587 (2025).
[106] S. Dhar and V. Kulkarni, Atomic transport in Cu/Ge            [123] A. Bose, F. Kammerbauer, R. Gupta, D. Go,
      and Co/Ge systems during ion-beam mixing, Thin Solid                Y. Mokrousov, G. Jakob, and M. Kläui, Detection
      Films 333, 20–24 (1998).                                            of long-range orbital-Hall torques, Phys. Rev. B 107,
[107] J.-S. Tsay, Y. Chen, W. Cheng, K. Wang, and Y. Yao,                 134423 (2023).
      Magnetic properties of co/ge (111) films: effects of          [124] R. Matsumoto, R. Ohshima, Y. Ando, D. Go,
      growth temperatures, physica status solidi (b) 244,                 Y. Mokrousov, and M. Shiraishi, Observation of giant
      4507–4511 (2007).                                                   orbital Hall effect in si, arXiv preprint arXiv:2501.14237
[108] A. R. Mellnik, J. Lee, A. Richardella, J. L. Grab, P. J.            (2025).
      Mintun, M. H. Fischer, A. Vaezi, A. Manchon, E.-A.            [125] N. W. Hendrickx, W. I. L. Lawrie, L. Petit, A. Sam-
      Kim, N. Samarth, et al., Spin-transfer torque generated             mak, G. Scappucci, and M. Veldhorst, A single-hole spin
      by a topological insulator, Nature 511, 449–451 (2014).             qubit, Nature Communications 11, 10.1038/s41467-020-
[109] V. M. Edelstein, Spin polarization of conduction elec-              17211-7 (2020).
      trons induced by electric current in two-dimensional          [126] N. Hendrickx, D. Franke, A. Sammak, G. Scappucci,
      asymmetric electron systems, Solid State Communica-                 and M. Veldhorst, Fast two-qubit logic with holes in
      tions 73, 233–235 (1990).                                           germanium, Nature 577, 487–491 (2020).
[110] A. Aronov and Y. B. Lyanda-Geller, Nuclear electric           [127] J. H. Cullen, D. P. Arovas, R. Raimondi, and
      resonance and orientation of carrier spins by an electric           D. Culcer, Quantum geometry and dipolar dynamics
      field, Soviet Journal of Experimental and Theoretical               in the orbital magneto-electric effect, arXiv preprint
      Physics Letters 50, 431 (1989).                                     arXiv:2505.02911 (2025).
[111] I. A. Ado, M. Titov, R. A. Duine, and A. Brataas, Or-         [128] J. Salvador-Sánchez, L. M. Canonico, A. Pérez-
      bital Edelstein effect from the gradient of a scalar poten-         Rodrı́guez, T. P. Cysne, Y. Baba, V. Clericò, M. Vila,
      tial, arXiv:2407.00516 (2024), arXiv:2407.00516 [cond-              D. Vaquero, J. A. Delgado-Notario, J. M. Cari-
      mat.mes-hall].                                                      dad, K. Watanabe, T. Taniguchi, R. A. Molina,
[112] T. Yoda, T. Yokoyama, and S. Murakami, Orbital Edel-                F. Domı́nguez-Adame, S. Roche, E. Diez, T. G. Rap-
      stein effect as a condensed-matter analog of solenoids,             poport, and M. Amado, Generation and control of non-
      Nano Letters 18, 916–920 (2018).                                    local chiral currents in graphene superlattices by orbital
[113] T. Yoda, T. Yokoyama, and S. Murakami, Current-                     Hall effect, Phys. Rev. Res. 6, 023212 (2024).
      induced orbital and spin magnetizations in crystals with      [129] P. Sahu, S. Bhowal, and S. Satpathy, Effect of the in-
      helical structure, Scientific Reports 5, 12024 (2015).              version symmetry breaking on the orbital Hall effect: A
[114] L. Salemi, M. Berritta, A. K. Nandy, and P. M. Op-                  model study, Phys. Rev. B 103, 085113 (2021).
      peneer, Orbitally dominated Rashba-Edelstein effect in        [130] S. Bhowal and S. Satpathy, Intrinsic orbital moment
      noncentrosymmetric antiferromagnets, Nature Commu-                  and prediction of a large orbital Hall effect in two-
      nications 10, 5381 (2019).                                          dimensional transition metal dichalcogenides, Phys.
[115] D. Go, J.-P. Hanke, P. M. Buhl, F. Freimuth,                        Rev. B 101, 121112 (2020).
      G. Bihlmayer, H.-W. Lee, Y. Mokrousov, and S. Blügel,        [131] A. Pezo, D. Garcı́a Ovalle, and A. Manchon, Orbital
      Toward surface orbitronics: giant orbital magnetism                 Hall physics in two-dimensional dirac materials, Phys.
      from the orbital Rashba effect at the surface of sp-                Rev. B 108, 075427 (2023).
      metals, Scientific Reports 7, 46742 (2017).                   [132] M. Costa, B. Focassio, L. M. Canonico, T. P. Cysne,
[116] J.-H. Park, C. H. Kim, J.-W. Rhim, and J. H. Han, Or-               G. R. Schleder, R. B. Muniz, A. Fazzio, and T. G.
      bital Rashba effect and its detection by circular dichro-
                                                                                                                          14

      Rappoport, Connecting higher-order topology with the       figure the bands have been inverted so the energy is pos-
      orbital hall effect in monolayers of transition metal      itive. Here we have chosen a Fermi energy of 10 meV,
      dichalcogenides, Phys. Rev. Lett. 130, 116204 (2023).      which is the largest Fermi energy we consider in this
[133] D. Culcer, A. MacDonald, and Q. Niu, Anomalous Hall        work.
      effect in paramagnetic two-dimensional systems, Phys.
      Rev. B 68, 045327 (2003).                                     Figure 2: The orbital Hall conductivity vs the Fermi
[134] S. Han, H.-W. Lee, and K.-W. Kim, Microscopic study        energy in Ge in the spherical approximation. We have
      of orbital textures, Current Applied Physics 50, 13–24     also plotted the conventional part of the orbital Hall con-
      (2023).                                                    ductivity σconv along with the quantum corrections ∆σ.
[135] J.-P. Hanke, F. Freimuth, A. K. Nandy, H. Zhang,           Here we use the Luttinger parameters γ1 = 13.38 and
      S. Blügel, and Y. Mokrousov, Role of berry phase theory   γ̄ = 4.97.
      for describing orbital magnetism: From magnetic het-
      erostructures to topological orbital ferromagnets, Phys.      Figure 3: The proper spin Hall conductivity vs the
      Rev. B 94, 121114 (2016).                                  Fermi energy in for four semiconductors in the spherical
[136] D. Go, F. Freimuth, J.-P. Hanke, F. Xue, O. Gomonay,       approximation. Here we use the Luttinger parameters
      K.-J. Lee, S. Blügel, P. M. Haney, H.-W. Lee, and         from Ref. 84. Note the difference of three orders of mag-
      Y. Mokrousov, Theory of current-induced angular mo-
                                                                 nitude in the scale of the y-axis as compared to the orbital
      mentum transfer dynamics in spin-orbit coupled sys-
      tems, Phys. Rev. Res. 2, 033401 (2020).
                                                                 Hall conductivity.
[137] S. Han, H.-W. Lee, and K.-W. Kim, Orbital dynamics in        Figure 4: The orbital Hall conductivity vs the Fermi
      centrosymmetric systems, Phys. Rev. Lett. 128, 176601      energy in Ge for a) the 4 × 4 Luttinger Hamiltonian and
      (2022).                                                    b) the 6 × 6 Luttinger Hamiltonian without the spherical
[138] I. Ado, M. Titov, R. A. Duine, and A. Brataas, Magnetic
                                                                 approximation. We have plotted the conventional part of
      moment of electrons in systems with spin-orbit coupling,
      arXiv preprint arXiv:2503.10956 (2025).
                                                                 the orbital Hall conductivity σconv along with the quan-
[139] R. B. Atencia, Quantum geometry and linear orbital re-
                                                                 tum corrections ∆σ. Here we use γ1 = 13.38, γ2 = 4.24
      sponse in arbitrary su(2) representation, arXiv preprint   and γ3 = 5.69.
      arXiv:2512.04164 (2025).                                     Figure 5: The orbital Hall conductivity vs Fermi en-
[140] M. P. Marder, Condensed matter physics (John Wiley         ergy for various hole-doped semiconductors calculated us-
      & Sons, 2010).
                                                                 ing the 6 × 6 Luttinger Hamiltonian. Luttinger parame-
[141] K. J. Vidarte, H. P. Veiga, J. M. Lopes, R. Cardias,
      A. Ferreira, T. P. Cysne, and T. G. Rappoport, Real-       ters have been taken from Ref. 84.
      space spectral approach to orbital magnetization, arXiv      Figure 6: Diagram of the orbital Hall torque in a
      preprint arXiv:2512.01575 (2025).                          Ge/Co heterostructure. Here the applied electric field
                                                                 generates transverse orbital currents via the intrinsic or-
                                                                 bital Hall effect. The orbital current will generate an
             VIII.    FIGURE CAPTIONS                            orbital accumulation. The orbital angular momentum is
                                                                 then converted into spin which generates a torque on the
  Figure 1: Dispersion for holes in Ge, showing the heavy        magnetisation in the Co layer. A barrier layer may be
(HH), light (LH) and split-off (SO) hole bands. In this          used to assist with orbital-to-spin conversion.

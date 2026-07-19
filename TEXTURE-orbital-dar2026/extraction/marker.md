<!-- NOTE: INTERIM: pdftotext fallback -->
<!--
  ARTIFACT 2 (marker.md) — PROSE extraction.
  The real `marker` binary is NOT installed on this packaging host (only
  poppler `pdftotext` is available). This file is the DOCUMENTED interim
  fallback: `pdftotext -layout textures-orbital-dar2026.pdf`.
  Regenerate with the real tool via:
      marker_single textures-orbital-dar2026.pdf ./extraction/ --output_format markdown
  FIDELITY CAVEAT: block/column structure is preserved reasonably, but Unicode
  math (ϱ, α, σ, subscripts) is degraded — equation rendering is lossy. The
  AUTHORITATIVE equation transcriptions live in report/REPORT.tex and in
  extraction/nougat.mmd (Key equations block). This is an extraction-tooling
  gap, NOT a physics gap.
-->

# Altermagnetic spin textures coupled to superconductors (Dar, Scheurer, Schrade, arXiv:2607.15249v1)
# --- prose extraction (pdftotext -layout) below ---

                                                                   Altermagnetic spin textures coupled to superconductors:
                                                           Domain wall spin-triplet superconductivity and supercurrent-induced torques

                                                                                 Yasir Dar,1 Mathias S. Scheurer,2, ∗ and Constantin Schrade1, †
                                                                            1
                                                                              Hearne Institute of Theoretical Physics, Department of Physics & Astronomy,
                                                                                       Louisiana State University, Baton Rouge LA 70803, USA
                                                                       2
                                                                         Institute for Theoretical Physics III, University of Stuttgart, 70550 Stuttgart, Germany
                                                                     Motivated by the absence of sizable stray fields and the recently discovered highly non-trivial
                                                                  impact of altermagnetic textures on itinerant electrons, we here study the form of Cooper pairs in
                                                                  spatially varying altermagnets coupled to conventional s-wave superconductors. As a consequence of
                                                                  the detrimental impact of altermagnetism on spin-singlet pairing and the local symmetry reduction
                                                                  caused by textures in the magnetic order parameter, we show that superconductivity predominantly
                                                                  impacts the regions between altermagnetic domains. Focusing on a planar radial domain wall for
                                                                  concreteness, we show that emergent Zeeman and spin-orbit fields create spatially separated triplet
                                                                  hotspots and transitions between nodal and fully gapped superconducting regions, whose structure
                                                                  is set by both the domain wall and the altermagnetic order parameter. We also identify a reciprocal
                                                                  effect, where a supercurrent generates a quasiparticle-mediated quadrupolar torque that inherits the
                                                                  symmetry of the altermagnetic order. Our results show that accounting for spatial inhomogeneities in
arXiv:2607.15249v1 [cond-mat.supr-con] 16 Jul 2026




                                                                  the altermagnetic order parameter is essential for an understanding of the superconducting proximity
                                                                  effect and suggest that hybrid systems of altermagnetic textures and superconductors offer unique
                                                                  opportunities for local engineering of Cooper pairs and for detecting altermagnetic order.


                                                                       I.   INTRODUCTION
                                                                                                                      (a)
                                                                                                                                                                      altermagnetic
                                                        Large-scale spatial textures in the magnetic order pa-              Domain wall
                                                                                                                                                                      texture
                                                     rameter, such as domain walls, naturally occur in many
                                                     magnetic materials [1–4] as a result of the competition of
                                                     different interaction energies, complex dynamics during
                                                     the formation of magnetic order, and the interplay with
                                                     short-range inhomogeneities “pinning” them. As such,
                                                     spin textures are of fundamental importance for under-
                                                     standing the physics of magnets, both because they can                                                         superconductor
                                                     crucially modify expectations based on theoretical con-
                                                     siderations for the idealized homogeneous magnet and
                                                     because they provide additional opportunities for rich           (b)   Geometric Zeeman field    (c)      Emergent SOC
                                                     physics and applications [2–7]. For instance, such spa-
                                                     tial (r) variations in the orientation n(r) of the mag-
                                                     netic order parameter have been shown to give rise to
                                                     emergent electrodynamics for metallic ferromagnets [8–
                                                     14] and antiferromagnets [15–18], where spatial gradients
                                                     in n alter the effective hopping amplitudes of the itiner-
                                                     ant electrons.
                                                        Recently, altermagnets [19, 20] have been established                        Domain wall                    Domain wall
                                                     as another class of magnets with favorable properties
                                                     in the itinerant case: while symmetry guarantees that
                                                     the net magnetization vanishes, the non-relativistic spin-       FIG. 1.     Circular altermagnetic Néel domain wall
                                                     degeneracy of the electronic bands is spontaneously split        proximitized by a superconductor. (a) Altermagnetic
                                                     by the altermagnetic order parameter. Driven by their            texture on a superconducting layer. Orange and blue ellipses
                                                     potential for spintronic applications, altermagnets have         denote the two sublattices (τz = ±). Arrows show the lo-
                                                                                                                      cal in-plane Néel vector orientation. The circle marks the
                                                     been actively studied, both theoretically and experimen-
                                                                                                                      wall radius, R, and the shaded annulus marks the domain
                                                     tally, in recent years [19–23]. However, although domain         wall region where the Néel vector rotates. (b) Geometric Zee-
                                                                                                                      man field, Vz (r), normalized by its maximum. The d-wave
                                                                                                                      altermagnetic order gives a fourfold multipolar pattern. (c)
                                                     ∗ Correspondence to: mathias.scheurer@itp3.uni-stuttgart.de      Emergent spin-orbit coupling, α(r), normalized by its maxi-
                                                     † Correspondence to: cschrade@lsu.edu                            mum. It is localized at the wall and points radially. Panel (a)
                                                                                                                      is schematic and not to scale.
                                                                                                                                2

                                                               the local spectrum is fully gapped or has point nodes also
walls are known to be ubiquitous in altermagnetic ma-          depends on the position on the domain wall. Finally,
terials, most works have focused on the homogeneous            we uncover a supercurrent-induced quadrupolar torque
limit, n(r) = n0 . Apart from studies on the impact            distorting the domain wall boundary, which is again as-
on the order parameter fields themselves [24–28] and the       sociated with Vz and comes on top of other forces, e.g.,
consequences of atomic-scale defects [29–36], the con-         those moving the domain wall and discussed in [46]. More
sequences of slowly varying altermagnetic textures on          generally, our work generalizes the emergent field of su-
the electronic spectral properties have only very recently     perconducting altermagnets [47], which—with the excep-
been addressed [37, 38].                                       tion of atomic-scale disorder studies [29, 30, 34–36]—
   Following the nomenclature of Ref. 38, a coplanar tex-      primarily focused on the homogeneous limit. It further
ture in an altermagnet, like the circular domain wall          shows that altermagnets provide a very versatile alter-
shown in Fig. 1(a), leads to two main effects, to leading      native to ferromagnets [48, 49] to locally engineer the
order in the inverse exchange coupling constant: first,        Cooper-pair wave function; they not only suppress the
there is an emergent Zeeman field, Vz , which is unique        detrimental stray fields but also allow additional effects,
to altermagnets, i.e., vanishes in the antiferromagnetic       like Vz and the associated triplet hotspots, opening up
limit, and encodes the dominant orbital character of its       new paths for superconducting spintronics.
order parameter. For instance, for a d-wave altermagnet,
Vz exhibits four sign changes upon encircling a domain
                                                                                 II.    NORMAL-STATE
wall, as illustrated in Fig. 1(b). Second, the spatial vari-
ation in n induces a spin-orbit coupling term (which sur-
vives in the antiferromagnetic limit, in contrast to Vz );       To define the theoretical modeling and the notation,
at fixed position r, it is proportional to the projection      we start with a concise derivation of the effective normal-
of the momentum of the electrons on the vector α(r),           state Hamiltonian for itinerant electrons moving through
which is oriented perpendicular to the domain wall, see        an altermagnetic texture, following Ref. 38. Our starting
Fig. 1(c).                                                     point is the altermagnetic texture model
   Motivated by these findings, which reveal the highly          ĥ(r, p̂) = ε0,p̂ + tx,p̂ τx + tz,p̂ τz + Jτz n(r) · s − µ   (1)
non-trivial impact of textures in altermagnets on the
Bloch Hamiltonian, we here explore how such inhomo-            which generalizes the minimal models of uniform alter-
geneities in the order parameter can be used to locally        magnets [29, 50, 51] to a spatially varying Néel vector,
induce and control superconducting correlations and fur-       n(r). Here, τ = (τx , τy , τz ) acts in sublattice space,
ther study the inverse effect of supercurrent-driven con-      s = (sx , sy , sz ) in spin space, and p̂ = −iℏ(∂x , ∂y )T . The
trol of altermagnetic textures. While our theory also          term ε0,p̂ is sublattice independent, while tx,p̂ and tz,p̂ de-
applies to itinerant altermagnets that become supercon-        scribe inter-sublattice and sublattice-antisymmetric hop-
ducting at low enough temperatures, i.e., altermagnetism       ping. For concreteness, we focus on a d-wave texture
and superconductivity emerge spontaneously in the same         with ε0,p̂ = ϱ0 (p̂2x + p̂2y ), tx,p̂ = ϱx + ϱ3 (p̂2x + p̂2y ), and
material, an experimentally likely more flexible scenario      tz,p̂ = ϱz (p̂2x − p̂2y ). For a uniform Néel vector, Eq. (1) re-
is based on the proximity effect [34, 39–42]: as shown in      produces the usual d-wave altermagnetic band splitting.
Fig. 1(a), in a heterostructure of a superconductor and           It will be convenient to work in a rotating frame where
an altermagnet, the two phases influence each other via        the local spin quantization axis aligns with the direc-
the superconducting proximity effect and exchange inter-       tion of the Néel vector. We therefore choose a uni-
actions.                                                       tary transformation U (r) such that U † [n(r) · s]U = sz .
                                                               The spatial dependence of the texture in this rotating
   In this work, we assume that the unperturbed super-
                                                               frame enters the Hamiltonian through a shift of the
conductor is in a conventional spin-singlet pairing state.
                                                               momentum operator by a spin-dependent gauge field,
Since the altermagnet lifts the spinful Kramers degener-
                                                               π̂ ≡ U † p̂U = p̂ − A(r) with Ai (r) = αi (r) · s. The
acy, it suppresses the singlet pairing correlations. How-
                                                               full rotating frame Hamiltonian reads
ever, spatial variations in its order parameter lead to
α ̸= 0, which locally induces triplet components that                  ĥrot (r, π̂) = ε0,π̂ + tx,π̂ τx + tz,π̂ τz + Jτz sz   (2)
gap out the Fermi surfaces – reminiscent of domain wall
superconductivity discussed in ferromagnets [43–45]. In          Let us now take J > 0 as the largest energy scale
addition, the anisotropies around domain walls inher-          and project Eq. (2) onto the low-energy subspace with
ited from the orbital nature of the altermagnet lead to        S ≡ τz sz = −1 with projector P− = (1−S)/2. From this
“hotspots” of the admixed triplet component at certain         projection, we will obtain an effective Hamiltonian with
positions on the domain wall, and the momentum de-             emergent fields that act on the low-energy spin. We split
pendence of the admixed equal-spin triplet component is        the gauge field into longitudinal and transverse parts,
                                                                       ∥                                   ∥
shown to wind upon encircling the domain wall. Whether         Ai = Ai + A⊥                                      z
                                                                             i . The longitudinal part, Ai = αi (r)sz ,
                                                                                                                                           3

acts within the low-energy subspace, while the transverse              to S = +1 and thus vanish under projection onto the
                    y
part, A⊥      x
       i = αi sx +αi sy , couples the low- and high-energy             low-energy subspace. The inter-sublattice singlet, τx isy ,
subspaces. We further define the longitudinally shifted                pairs the low-energy states directly and survives the pro-
                          ∥
momentum Π̂i = p̂i − Ai (r), so that π̂i = Π̂i − A⊥  i (r).
                                                                       jection onto the low-energy subspace. Hence, we will
The projection of Eq. (2) onto the S = −1 subspace gives               focus on

   ĥproj (r, Π̂) = ε0,Π̂ + tz,Π̂ σz + ϱ0 V0 (r) + ϱz Vz (r)σz                                 ˆ
                                                                                               ∆(r) = ∆(r) τx isy                    (6)
                 + ĥSOC (r, Π̂)                                 (3)                                ˆ − = ∆(r)(−iσy ) in
                                                                       in the following, obeying P− ∆P
                                                                       the low-energy subspace. The effective Bogoliubov-de
Here, σx = P− τx sx P− , σy = −P− τx sy P− , and σz =
                                                                       Gennes (BdG) Hamiltonian then takes the form
P− τz P− are the Pauli matrices in the low-energy sub-
space; due to spin-sublattice locking, one can think of σj                                                                        
                                                                                             ĥproj (r, Π̂)   ∆(r) (−iσy )
as acting on either spin or sublattice degrees of freedom.               ĤBdG (r, Π̂) =                                               .
                                                                                            −∆∗ (r) (−iσy ) −[ĥproj (r, −Π̂)]T
  Two comments about the low-energy effective Hamilto-
                                                                                                                                (7)
nian in Eq. (3) are in order: First, the itinerant electrons
                                                                       This effective Hamiltonian shows that, within the low-
are subject to a scalar potential, V0 (r), and an effective
                                                                       energy subspace, the texture is subject to an effective
Zeeman field, Vz (r). These fields are given by
                                                                       s-wave pairing, in addition to the texture-induced fields.
                     V0 (r) = ℏ2 δ ij gij (r),                         All texture-induced fields are spatially varying, and Vz (r)
                                                                 (4)   retains the d-wave structure of the altermagnetic order
                     Vz (r) = ℏ2 η ij gij (r),                         through the form factor, η ij . Our expectation is that
                                                                       the texture and the altermagnetic form factor control the
where η ij = diag(1, −1)ij and gij (r) = ∂i n(r)·∂j n(r)/4.
                                                                       local spin dependence of the induced pairing correlations.
Notably, Vz (r) acts as a spatially varying spin splitting
in the low-energy subspace. It is unique to the altermag-
net and vanishes in the antiferromagnetic limit, ϱz = 0.                  IV.    NAMBU-SPACE GREEN’S FUNCTION
The fact that kT ηk = kx2 − ky2 encodes the orbital char-
acter of the altermagnet and g is the real-space quantum
                                                                          The pairing correlations are given by the off-diagonal
metric associated with the texture Hamiltonian n(r) · s
                                                                       components of the Nambu-space Green’s function. We
underscores the geometric nature of V0 and Vz .
                                                                       will now discuss how to compute the Nambu-space
   Second, the itinerant electrons are also subject to an
                                                                       Green’s function in a local, semiclassical approximation.
emergent spin-orbit coupling, generated by the transverse
gauge field,                                                              Our focus will be, for concreteness, on a planar radial
                                                                       domain wall, n(r) = (cos ϕ(r), sin ϕ(r), 0), with ϕ(r) =
                                                                       (π/2) tanh[(r − R0 )/w]. Here, R0 is the wall radius, w
                     X
 ĥSOC (r, p̂) = −ϱ3     [{p̂i , αix (r)}σx − {p̂i , αiy (r)}σy ] .
                      i=x,y
                                                                       the wall width, and (r, χ) are polar coordinates with r =
                                                            (5)        (r cos χ, r sin χ).
This term provides a spatially varying   spin mixing.   It can            For this radial domain wall texture, the projected
also be written as ĥSOC = −ϱ3 i=x,y P− τx {p̂i , A⊥
                                 P                                     normal-state Hamiltonian of Eq. (3) simplifies greatly.
                                                       i }P− ,
                                                                       The longitudinal gauge field can be removed by
from which it follows that ĥSOC (r, p̂) = ĥSOC (r, Π̂) since
   ∥                                                                   the unitary, W (r)Π̂x,y W † (r) = p̂x,y with W (r) =
{Ai , A⊥
       i } = 0.                                                        e−iϕ(r)σz /2 . The emergent spin-orbit coupling simpli-
   A natural question is: How do these emergent fields                               (0)
                                                                       fies to W ĥSOC W † = (1/2){p̂, α(r)}σx , where α(r) =
affect the Cooper pair wavefunction upon proximitizing                       ′
                                                                       ℏϱ3 ϕ (r)r̂ with the radial unit vector r̂; see Fig. 1(c).
the altermagnetic texture and a superconductor, as illus-
                                                                       The effective normal-state Hamiltonian then takes on the
trated schematically in Fig. 1(a)?
                                                                       form
                                                                                                                    1
         III.   SUPERCONDUCTING STATE                                   ĥproj (r, p̂) = ξ(r, p̂)σ0 + bz (r, p̂)σz + {p̂, α(r)}σx . (8)
                                                                                                                    2

   To address this question, let us assume for concreteness            Here, the spin-independent term is ξ(r, p̂) = ϱ0 p̂2 +
                                                                                                          2
that the superconductor is a conventional, s-wave spin-                ϱ0 V0 (r) − µ with V0 (r) = ℏ4 ϕ′ (r)2 . The spin-splitting
singlet state, inducing a momentum-independent spin-                   term is bz (r, p̂) = ϱz (p̂ · ηp̂) + ϱz Vz (r, χ) with Vz (r, χ) =
                           ˆ
singlet pairing potential ∆(r)    ∝ isy in the altermagnet.            ℏ2 ′     2          ℏ2 ′     2
                                                                        4 ϕ (r) r̂ · ηr̂ = 4 ϕ (r) cos 2χ and r̂ = (cos χ, sin χ). A
Fermionic antisymmetry, ∆    ˆ = −∆  ˆ T , allows the sublat-          consequence of Eq. (8) is that the BdG Hamiltonian for
tice matrix multiplying isy to be τ0 , τx , or τz . The                the planar domain wall can be written in terms of the
intra-sublattice singlets, τ0 isy and τz isy , couple S = −1           usual momentum operator, ĤBdG (r, Π̂) = ĤBdG (r, p̂).
                                                                                                                                                                      4

   Let us now discuss the Nambu-space Green’s func-                                                
                                                                                                                                                               
                                                                                 (a)                                       (b)
tion. It is defined as the solution of the Gor’kov equa-
                                                                                                                                                               
tion, (iωn − ĤBdG (r 1 , p̂1 ))G(r 1 , r 2 ; iωn ) = δ (r 1 − r 2 )
                                                                                                nodal
where ωn are the fermionic Matsubara frequencies. We                                            point                                                          




                                                                                                                                                                      
                                                                       
will rewrite the Gor’kov equation in a “phase-space                          
                                                                                                                                                               
form”, which has been previously used in the quasi-                                      

classical theory of superconductivity [52]. We there-                                                                                                         
                                                                        
fore adopt a position-space representation of operators,                                                                               
O(r 1 , r 2 ) ≡ ⟨r 1 |Ô|r 2 ⟩. We then introduce center-of-                                                                         
                                                                                                                                                              
                                                                                                                                 
mass and relative coordinates, R = (r 1 + r 2 )/2 and
ρ = r 1 − Rr 2 , and perform the “Wigner transform”,                            (c)                          Line cut      (d)                    Line cut
                           i
O(R, p) = d2 ρ e− ℏ p·ρ O R + ρ2 , R − ρ2 . Here, p is
the relative momentum. The Gor’kov equation then




                                                                       
takes on the form,
                                                                                                                 nodal
          (iωn − HBdG (R, p)) ⋆ G(R, p; iωn ) = 1.              (9)                                            point
                                                                                                    
                                                                             
Here, HBdG (R, p) and G(R, p; iωn ) are matrix-valued                                                                            
                                                                                                                         
functions on the classical phase space, (R, p). Quan-
tum corrections are encoded in the “Moyal product”,                    FIG. 2.      Local quasiparticle spectrum for different
                                           ←
                                           − →  −     ←−
O1 (R, p) ⋆ O2 (R, p) = O1 (R, p) exp[ iℏ
                                        2 (∇R · ∇p − ∇p ·              points along a proximitized circular altermagnetic do-
→
−
∇ R )]O2 (R, p). This rewrite of the Gor’kov equation will             main wall. (a,b) Lower positive-energy quasiparticle band,
be the starting point for the local, semiclassical approxi-            E− (R, p)/∆, evaluated on the radial domain wall at the wall
mation.                                                                positions χ = 0 and χ = π/4. Dashed contours indicate the
                                                                       condition b2z = ξ 2 + ∆2 . A nodal point additionally requires
  We now assume that the texture-induced fields, V0 (r),
                                                                       pR = 0, so that the emergent spin-orbit coupling vanishes.
Vz (r), and α(r), vary slowly on the scale of the Fermi
                                                                       (c,d) At χ = 0, four nodal points appear in the quasiparticle
wavelength and the superconducting coherence length.                   spectrum. At χ = π/4, the quasiparticle spectrum       is fully
Under this assumption, the local, semiclassical approx-                                                                p
                                                                       gapped. The momentum normalization is p0 = µ/ϱ0 .
imation involves retaining only the lowest-order term
in the expansion of the Moyal product, O1 (R, p) ⋆
O2 (R, p) ≈ O1 (R, p)O2 (R, p). Interestingly, since the               R = |R| arises from the emergent spin-orbit coupling.
texture-induced fields are local functions in phase space,             For the radial domain wall, αp (R) = ℏϱ3 ϕ′ (R)pR , where
this approximation already captures the leading order                  pR = p · r̂ is the radial momentum.
at which texture effects enter the Nambu-space Green’s                    To describe the effective low-energy pairing, we
function. Specifically, we approximate the Nambu-space                 now move to the helicity basis, defined as the eigen-
Green’s function as,                                                   basis of the local normal-state Hamiltonian.            The
                                            −1                       normal-state Hamiltonian is hproj (p) = ξ(p)σ0 +
          G(R, p; iωn ) ≈ iωn − HBdG (R, p) .          (10)            αp σx + bz (p)σz .         Its helicity eigenstates satisfy
We will now use this approximate form to address the                   hproj (p)|s, p⟩ = [ξ(p) + sλp ] |s, p⟩ with s = ± and
question on the spin structure of the pairing correlations             λp = (bz (p)2 + αp2 )1/2 . Equivalently, the unitary ma-
and the quasiparticle spectrum.                                        trix, Up , whose columns are the helicity eigenstates,
                                                                       obeys, Up† hproj (p)Up = ξ(p)σ0 + λp σz . An explicit choice
                                                                       of eigenstates is |+, p⟩ = (cos(θp /2), sin(θp /2))T and
         V.    QUASIPARTICLE SPECTRUM                                  |−, p⟩ = (− sin(θp /2), cos(θp /2))T with cos θp = bz /λp
                                                                       and sin θp = αp /λp .
   We first discuss the local quasiparticle spectrum, be-                 We next transform the superconducting order parame-
cause it will provide us with an intuition for the discus-             ter to the helicity basis, ∆hel (p) = Up† ∆(p)U−p
                                                                                                                       ∗
                                                                                                                         . We find
sion on the pairing correlations. The local quasiparticle              the form
energies of HBdG (R, p) are,                                                                                    
                                                                                                     ∆ αp −bz
                                                                                         ∆hel (p) =                .           (12)
  E± (p) = [∆2 + ξ(p)2 + αp2 + bz (p)2                                                               λp bz αp
              q                                         (11)
           ± 2 ξ(p)2 [αp2 + bz (p)2 ] + ∆2 bz (p)2 ]1/2                The diagonal entries describe pairing between states in
                                                                       the same helicity band, |+, p⟩ ↔ |+, −p⟩ and |−, p⟩ ↔
Here, we omitted the position argument, since we will                  |−, −p⟩. By contrast, the off-diagonal terms pair states
work at fixed R. The factor αp (R) ≡ p · α(R) with                     in different helicity bands, |+, p⟩ ↔ |−, −p⟩.
                                                                                                                                                   5

   Suppose that, at a given momentum p, only one helic-              
                                                                    (a)                                   
                                                                                                                 (b)            
                                                                                        Domain
ity band, s, lies near the Fermi level, while the other is                           R   wall

separated by an energy large compared with the induced
pairing scale. We then neglect the interband pairing and




                                                                   
retain only the pairing within band s. The resulting low-              
energy BdG Hamiltonian is

                                                                                                       
                                          
            (eff)         ξ + sλp ∆αp /λp                                       p-wave nodes
          HBdG,s (p) =                       .              (13)                         
                          ∆αp /λp −ξ − sλp
                                                                    
                                                                   (c)                                           
                                                                                                                  (d)
                                                                           
Its spectrum is     Es2
                      = (ξ + sλp )    2
                                          + ∆2 αp2 /λ2p .
                                                      The
normal-state dispersion, ξ(p) + sλp , is even in momen-




                                                                                                                                               F"" (normalized)
tum, whereas the intraband pairing amplitude is odd,
α−p = −αp and λp = λ−p . The projected theory there-




                                                                   
                                                                                                                                            
fore describes an odd-parity superconductor within each
nondegenerate helicity species.




                                                                                                                                                         <latexit sha1_base64="0X63Fg7aXONSg6TMucRRExVFC90=">AAAC6XichVHLSgNBECzXd3xFPQoSDIKnsImCHgUfeBEUTBSMhNl1TJbsi9mJoiE3f8CbePXmVX9Gv8WDteNGUBFnme2e6uqa7mkn9r1E2/brgDU4NDwyOjaem5icmp7Jz87VkqijXFl1Iz9SJ45IpO+Fsqo97cuTWEkROL48dtpbafz4UqrEi8IjfR3Ls0A0Q+/Cc4Um1Mgv1gOhW67wu7u9RrfeiYVS0VXf9hr5ol2yzSr8dsqZU0S2DqL8G+o4RwQXHQSQCKHp+xBI+J2iDBsxsTN0iSl6nolL9JBjbocsSYYg2ua/ydNphoY8p5qJyXZ5i8+tmFnAMveuUXTITm+V9BPad+4bgzX/vKFrlNMKr2kdKo4bxX3iGi0y/ssMMma/lv8z0640LrBhuvFYX2yQtE/3S2ebEUWsbSIF7BhmkxqOOV/yBULaKitIX7mvUDAdn9MKY6VRCTNFQT1Fm74+6+GYyz+H+tupVUrl1VLlcK24WcoGPoYFLGGFU13HJvZwwDpc3OIJz3ix2taddW89fFKtgSxnHt+W9fgBy9qcdw==</latexit>
   We can further understand the spin structure of in-
                                                                     
duced pariring by transforming the superconducting or-                                                                                         
                                                                                                                                
der parameter from the helicity basis back to the σz basis                                                                 

and decomposing it into singlet and triplet components
as [ψ(p)σ0 + d(p) · σ]iσy . In this case, we find                  FIG. 3. Radial altermagnetic domain wall generates
                                                                   spin-polarized triplet correlations. Equal-spin triplet
                                                                   correlator, F↑↑ (R, p), for a proximitized radial altermagnetic
          ∆αp2            ∆αp                                      domain wall normalized to its maximum. Insets indicate
 ψ(p) =        , d(p) = −     (±1, ibz (p)/λp , 0)T . (14)         the position, R, on the wall. (a,c) Antiferromagnetic limit,
          2λ2p            2λp
                                                                   ϱz = 0. The emergent spin-orbit coupling generates a p-wave
                                                                   triplet component with nodes at pR = p · R̂ = 0 (red line).
Thus, in the limit of strong altermagnetism, we ob-                Additional nodes arise at ξ(R, p) = 0 (dashed line). (b,d)
tain predominantly nonunitary equal-spin triplet pair-             Altermagnetic case, ϱz ̸= 0. The p-wave triplet component
ing, with d = (∓1, i, 0)T ∆α/(2bz ) + O(α2 /b2z ) and ψ =          is now modulated by the d-wave altermagnetic form factor.
0 + O(α2 /b2z ). The two signs correspond to the two he-           Hence, the additional nodes arise at ξ(R, p) − bz (R, p) = 0.
licity bands, which predominantly support the ↑↑ and
↓↓ pairing channels, respectively. As can also be seen
in Eq. (14), the low-energy pairing correlations are only                                VI.      PAIRING CORRELATIONS
non-zero if αq ̸= 0 and, thus, only sizeable in the vicinity
of the domain wall. Given the dominance of the triplet                Having discussed the local quasiparticle spectrum
component, altermagnetic domain wall systems therefore             and the effective low-energy BdG Hamiltonian, we will
realize domain wall spin-triplet superconductivity.                next turn to the induced pairing correlations. To this
    In addition to studying the low-energy superconduct-           end, we study the anomalous electron-hole block of the
ing order parameter, we can also determine when the full           Nambu-space Green’s function. It reads F (R, p; iωn ) ≡
spectrum is gapped and when nodal points arise. From               ⟨e|G(R, p; iωn )|h⟩ where |e⟩ = (1, 0)T and |h⟩ = (0, 1)T
E+ 2 2
     E− = (ξ 2 +∆2 −λ2p )2 +4∆2 αp2 , we see that nodes only       are vectors in Nambu space. We focus P on the equal-time
arise if simultaneously αp = 0 and b2z = ξ 2 + ∆2 . This           pairing correlator, Fσσ′ (R, p) ≡ T ωn Fσσ′ (R, p; iωn ).
behavior is illustrated in Fig. 2, where the momenta obey-         Evaluating Eq. (10) and performing the Matsubara sum
ing these two constraints are shown as solid and dashed            at zero temperature gives,
black lines, respectively. We can see that, depending on                                          ∆(R)αp (R)
the position on the domain wall, which determines the                  Fσσ (R, p) =                          [σξ(R, p) − bz (R, p)] , (15)
                                                                                                   D(R, p)
orientation of the line with αp = 0, the superconducting
spectrum either exhibits nodal points at the intersection          where σ = +1 for ↑↑ pairs and σ = −1 for ↓↓ pairs.
of the two lines, see Fig. 2(a,c), or is fully gapped (no in-      We remark that, in this context, ↑ and ↓ are the labels
tersection of the solid and dashed lines), see Fig. 2(b,d).        for eigenstates of σz in the local rotating frame, not in
We emphasize that this directional dependence of the               the fixed laboratory frame of the system. In the labo-
type of excitation spectrum is crucially connected to the          ratory frame, ↑ would refer to a local spin orientation
altermagnetic nature of the system since b2z = ξ 2 + ∆2            that is antiparallel to n(R), whereas ↓ would refer to a
has no solutions for bz = 0, making the system generi-             local spin orientation that is parallel to n(R). For our
cally fully gapped in the antiferromagnetic limit.                 radial domain wall texture, we have n(r ≪ R0 ) = −ŷ,
                                                                                                                               6

n(R0 ) = +x̂, and n(r ≫ R0 ) = +ŷ. As a result, the             (a)                               (b)
spin polarization of the Cooper pairs will reverse upon
traversing the wall. However, since n(R) = n(R) there
is no azimuthal winding of the spin direction upon encir-
cling the wall at a fixed radius, R.
   Equation (15) is one of our main results and several
comments are in order:
                                                                                 Triplet hotspot                 Domain wall
   First, we note that equal-spin triplets are generated
only where the texture produces a nonzero emergent spin-         (c)                               (d)
orbit coupling. For the radial domain wall, αp (R) =
ℏϱ3 ϕ′ (R)pR , where pR = p·r̂ and R = |R|. Triplet gener-
ation is therefore localized at the wall, where ϕ′ (R) ̸= 0.
It is also momentum selective. We see that tangential
momenta with pR = 0 give no conversion. Thus, the
equal-spin triplet correlator has nodes along pR = 0. Be-
cause the radial direction, r̂, changes around the wall,
these nodes rotate when moving to different wall posi-
tions, as we show with red lines in Fig. 3.
   Second, the factor in brackets of Eq. (15) contains a         (e)                                (f)
first contribution ∝ ξ(R, p). This contribution is present
even when the altermagnetic splitting is absent, ϱz = 0.
In this situation, it produces nodes on the circle ϱ0 p2 =                 AM
µ−ϱ0 V0 (R), assuming that the right-hand side is positive,                AFM
see dashed circles in Fig. 3(a,c).
   Third, the second contribution ∝ bz (R, p) in Eq. (15)
is ∝ ϱz and, thus, unique to the altermagnet. It changes
the node condition to σξ(R, p) − bz (R, p) = 0, which            FIG. 4. Spin-polarized triplet hotspots at a proximi-
evaluates to (ϱ0 − σϱz )p2x + (ϱ0 + σϱz )p2y = µ − ϱ0 V0 (R) +   tized radial altermagnetic domain wall. (a) Equal-spin
σϱz Vz (R, χ). For ϱ0 > |ϱz | and a positive right-hand          triplet intensity, It (r), for a radial AM wall, ϱz ̸= 0. The
side, this equation describes a spin-dependent ellipse in        wall generates triplets, while the d-wave AM splitting pro-
momentum space. Thus, the altermagnet creates an                 duces a fourfold hotspot pattern. (b) Non-AM limit (ϱz = 0).
anisotropy on the pairing correlations. This anisotropy          Triplets remain localized at the wall, but the angular mod-
will lead to a spatially nonuniform distribution of spin-        ulation is absent. (c,d) Spin-resolved intensities: It↑↑ peaks
polarized triplet correlations around the wall, as is visible    near χ = ±π/2, whereas It↓↓ peaks near χ = 0, π. (e) On-wall
in Fig. 3(b,d). We will refer to the associated points on        cut of It , comparing AM and non-AM cases. (f) On-wall spin
                                                                 selectivity St (χ), with positive (negative) values denoting ↑↑
the domain wall with maximum net triplet contributions
                                                                 (↓↓) dominance.
as “triplet hotspots”.
   To describe the formation of the triplet hotspots, we
move from the relative momentum, p, to the relative
                                                                    We have evaluated the triplet intensities and the spin-
coordinate of a Cooper pair, ρ, via an inverse Wigner
                                   R d2 p i p·ρ                  selectivity numerically. Our results are shown in Fig. 4.
transformation, Fσσ (R, ρ) =         (2πℏ)2 e
                                              ℏ   Fσσ (R, p).    In the altermagnetic case, Fig. 4(a), the total triplet in-
To quantify the net triplet strength, we focus on small ρ        tensity is localized along the wall but is not uniform.
                                R d2 p
and expand Fσσ (R, ρ) ∼ ℏi ρ· (2πℏ)    2 p Fσσ (R, p), where     Instead, it forms a fourfold “hotspot” pattern. Notably,
the integral expression corresponds to the short-range p-        this angular modulation disappears in the antiferromag-
wave triplet amplitude. The lowest order contribution            netic limit, ϱz = 0, shown in Fig. 4(b). This comparison
in the expansion of the exponential vanishes because the         thus shows that the emergent spin-orbit coupling gener-
pairing correlator is odd in momentum, since αp ∝ pR .           ates equal spin-triplet correlations around the wall, while
We define the associated spin-resolved triplet intensity         the altermagnetic anisotropy redistributes the equal spin-
                                                                 triplet correlations in a nonuniform way.
                                                2
                              d2 p
                        Z
                                                                    We can also understand the formation of these triplet
           Itσσ (R) ≡              p Fσσ (R, p) .        (16)
                            (2πℏ)2                               hotspots from the individual intensities of ↑↑ and ↓↓
                                                                 pairs, as shown in Fig. 4(c). The ↑↑ intensity is largest
Moreover, we introduce the total triplet intensity as            near χ = ±π/2, whereas the ↓↓ intensity is largest near
It (R) ≡ It↑↑ (R) + It↓↓ (R) and the spin-selectivity as         χ = 0, π. The total intensity is enhanced where the
St (R) ≡ [It↑↑ (R) − It↓↓ (R)]/[It↑↑ (R) + It↓↓ (R)].            spin-resolved intensities overlap, producing the total spin
                                                                                                                               7

triplet hotspots of Fig. 4(e). Interestingly, at the same lo-   (a)                                 (b)
cations, the relative spin polarization is reduced because                                                      Q
both spin species contribute. This is reflected in the spin
selectivity, Fig. 4(f), whose extrema occur along the prin-
cipal axes where one equal-spin component dominates.

                                                                        Q
 VII.    SUPERCURRENT-INDUCED TORQUES                                                      torque
                                                                            supercurrent
   So far, we have seen that an altermagnetic texture can
be used to induce spatially varying spin-triplet correla-       (c)                                 (d)
tions. We now consider a converse question: how does a                 Q
                                                                                                           Q
supercurrent let an s-wave superconductor act back on
the texture? This question is important because it asks
how an altermagnetic texture can, in principle, be ma-
nipulated by a supercurrent.
   To address this question, we stick to our example of
the planar radial domain wall, but assume that the ap-
plied supercurrent leads to a finite Cooper-pair momen-                           Domain wall
tum ℏQ ̸= 0, i.e., set ∆(R) → eiQ·R ∆(R). Within the
semiclassical approximation, the BdG Hamiltonian (with
appropriately re-defined Nambu spinors) is                      FIG. 5. Supercurrent-induced torque hotspots at a
                                                                radial altermagnetic domain wall. (a) A supercurrent
 HBdG (R, p; Q)                                  (17)           produces an out-of-plane torque on the in-plane Néel vector
   
    hproj (R, p + ℏQ/2)       ∆(R)(−iσy )
                                                               of the altermagnetic texture. (b) Altermagnetic torque contri-
 =                                                 ,                      Vz
                                                                bution, τQ   , for a current along the x direction. The torque is
       −∆(R)(−iσy )     −[hproj (R, −p + ℏQ/2)]T
                                                                localized near the domain wall and has the quadrupolar pat-
                                                                tern set by the d-wave order parameter. (c) For a diagonal
where we chose a gauge with real-valued ∆(R). For
                                                                current, χQ = π/4, the altermagnetic torque vanishes. (d)
brevity, we will now omit the (R, p) arguments in the           Rotating the current from x to y reverses the torque pattern.
following.                                                      All torques are normalized by their maximum.
   The supercurrent-induced torque follows from the
supercurrent-induced change in the free energy density
upon varying the angle ϕ(R) defining the local orien-           obeys diag(1, −1, −1, 1)HBdG (p, Q)diag(1, −1, −1, 1) =
tation n(R) = (cos ϕ(R), sin ϕ(R), 0) of the texture. Up        HBdG (−p, −Q), which corresponds to spinful π rotation
to a texture-independent additional term, which does not        along the z axis. After the momentum integration, the
affect the torque, the free energy density is given by,         free energy is therefore even under Q → −Q and, there-
                   T X                                          fore, cannot carry a finite supercurrent in equilibrium.
     Ω[ϕ, Q] = −       Tr ln [iωn − HBdG (Q)] .         (18)    The leading supercurrent-induced change to the free en-
                   2 ω
                       n                                        ergy density is given by the superfluid stiffness, DQ (R).
                                                                   For a planar texture, the resulting torque has only an
Here, the trace is over Nambu, spin, and phase space
                                                                out-of-plane component and is obtained by varying the
degrees of freedom. For small Cooper-pair momenta, we
                                                                change in the free energy density with respect to the tex-
can expand the change in the free energy density due to
                                                                ture angle,
the supercurrent, ΩQ ≡ Ω[ϕ, Q] − Ω[ϕ, 0]. Up to second
order in the Cooper-pair momentum, we have,                                                                δΩQ
                                                                                      τQ (R) = −                .           (20)
                Z
                                  Q2                                                                      δϕ(R)
          ΩQ ≈ d2 R [QJQ (R) +       DQ (R)].      (19)
                                   2
                                                                  To evaluate this torque, we need the dependence of DQ
                                                                on the texture-induced fields. For the planar radial wall,
Here, a non-zero linear term, JQ (R) = Q̂i J i (R),
                                                                V0 = (ℏ2 /4)δ ij ∂i ϕ ∂j ϕ , Vz = (ℏ2 /4)η ij ∂i ϕ ∂j ϕ, and αi =
with the unit-vector components Q̂i = Qi /Q, would
                                                                ℏϱ3 ∂i ϕ. Assuming a slowly-varying texture, we expand
stabilize Q ̸= 0 at equilibrium.       The quadratic
                                                                the superfluid stiffness up to the lowest non-vanishing
term, DQ (R) = Q̂i Q̂j Dij (R), describes the super-
                                                                order in these fields,
fluid stiffness along the supercurrent direction. For
the radial domain wall, the linear term vanishes.                                                      1
To see this, we note that the BdG Hamiltonian                    DQ ≈ D̄Q + ϱ0 C̄0,Q V0 + ϱz C̄z,Q Vz + Āmn αm αn . (21)
                                                                                                       2 Q
                                                                                                                                          8

Here, D̄Q , C̄0,Q , C̄z,Q , and Āmn
                                  Q  are the Taylor coeffi-                    along x and y generate opposite torques, while a diagonal
cients of the expansion, which need to be evaluated in                         current, for example χQ = π/4, switches the altermag-
the uniform limit, V0 = Vz = αi = 0.                                           netic torque off. The current direction thus controls both
   Three remarks about this expansion are in order: First,                     the sign and the magnitude of the altermagnetic torque.
the leading order contribution from the emergent spin-                            Second, the torque is localized at the domain wall. The
orbit coupling is quadratic. To see this, we note from                         radial factor, ϕ′′ (R) − ϕ′ (R)/R is nonzero only where the
Eq. (8) that sending α → −α is equivalent to a π-                              Néel vector rotates. The supercurrent therefore produces
rotation in spin space around the z-axis, implying that                        “torque hotspots” near the domain wall.
the spectrum must be invariant under this transforma-                             Third, the altermagnetic torque is a quasiparticle re-
tion. Hence, the superfluid stiffness cannot contain terms                     sponse. At zero temperature, f ′ (E) and f ′′ (E) have sup-
that are odd in α. Second, the expansion in Eq. (21) con-                      port only at zero quasiparticle energy. Thus, in a zero-
tains only terms up to second order in the gradients of ϕ,                     temperature fully gapped superconducting state, C̄z = 0
while O[(∂i ϕ)4 ] terms are neglected. Third, the term in                      and the altermagnetic torque vanishes. It remains fi-
the expansion that is unique to the altermagnet is ∝ Vz .                      nite though if the superconductor exhibits a Bogoliubov
   We now insert the expansion of Eq. (21) into the free                       Fermi surface with Ēsτ (p) = 0. At finite tempera-
energy density and compute the torque by performing                            ture, thermally excited quasiparticles can produce a finite
the variational derivative. We find three contributions,                       torque even in the fully gapped regime.
                                                      V0
one for each of the texture-induced fields, τQ = τQ      +
  Vz    SOC
τQ + τQ . Specifically,
                                                                                    VIII.    DOMAIN WALL DEFORMATION
                       Q2
                              2                  
                  V0          ℏ ϱ0
                 τQ  =    ∂j       C̄0,Q δ ij ∂i ϕ ,                              Finally, an interesting question is how the altermag-
                       2       2                                                               Vz
                        2
                              2                                              netic torque, τQ   , can deform a radial domain wall. We
                  Vz   Q      ℏ ϱz         ij                                  will address this question by showing that the altermag-
                τQ =      ∂j       C̄z,Q η ∂i ϕ ,                     (22)
                       2       2                                               netic torque deforms a circular planar domain into an
                SOC    Q2 h 2 2 jn           i                                 ellipse with an orientation that is set by the direction of
               τQ    =    ∂j ℏ ϱ3 ĀQ ∂n ϕ .
                       2                                                       the supercurrent.
                                                                                  We begin by relating a deformation of the wall position
                              Vz
We will now focus on τQ          , since it is unique to the alter-            to a deformation of the altermagnetic texture. In the ab-
magnet.                                                                        sence of the torque, we describe the planar domain wall in
   For the radial wall, we can evaluate the altermagnetic                      terms of a texture angle, ϕ0 (r) = (π/2) tanh[(r − R0 )/w].
contribution explicitly. We set Q̂ = (cos χQ , sin χQ ) and                    Upon application of the altermagnetic torque, we as-
R = R(cos χ, sin χ). The altermagnetic torque is then                          sume that the domain wall radius deforms in an angle-
given by,                                                                      dependent way, R0 → R(χ) = R0 + δu(χ). This de-
                                                                               formation is, to linear order, equivalent to a change
             ℏ2 ϱz Q2                                        ϕ′ (R)
                                                                    
     Vz
    τQ =               C̄z cos 2χQ cos 2χ ϕ (R) −  ′′
                                                                       .       of the texture angle, ϕ0 (r) → ϕ0 (r) + δϕ(r, χ) with
                 4                                              R              δϕ(r, χ) = −ϕ′0 (r)δu(χ).
                                                                       (23)       To realize such a texture deformation, the altermag-
Here, the coefficient C̄z can be calculated from the spec-                     netic torque has to perform mechanical work on the tex-
trum of the proximitized uniform d-wave altermagnet.                           ture. This work is given by,
The BdG eigenvalues of the latter are given by Ēsτ =                                                 Z
sϱz (p2x − p2y ) + τ [(ϱ0 p2 − µ)2 + ∆2 ]1/2 with s, τ = ±. We                               δWQ = d2 r τQ   Vz
                                                                                                                (r, χ)δϕ(r, χ).       (25)
then find,
                                                                               Inserting the expression for the altermagnetic torque
                   d2 p X
             Z
         ηij
 C̄z =                         s[f ′′ (Ēsτ )v̄sτ
                                               i    j
                                                  v̄sτ + f ′ (Ēsτ )m̄ij
                                                                       sτ ].
                                                                               from Eq. (23), Rwe see that this work has a quadrupolar
          4      (2πℏ)2 s,τ                                                    form, δWQ ∝ dχ cos 2χ δu(χ), up to an overall radial
                                                           (24)                prefactor.
        i
Here, v̄sτ  = ℏ ∂pi Ēsτ , m̄ij    2
                             sτ = ℏ ∂pi ∂pj Ēsτ , and f (E) =                    To demonstrate this elliptical deformation, it is now
1/(eβE + 1) is the Fermi function.                                             useful to decompose the wall displacement into angular
   Eq. (23) and Eq. (24) are the main results of this sec-                     harmonics. We write δu(χ) = δu0 +δu1 cos χ+δu′1 sin χ+
tion. Several points about them are noteworthy:                                δu2 cos 2χ + δu′2 sin 2χ + · · · . Here, δu0 describes a uni-
   First, the supercurrent produces a quadrupolar alter-                       form expansion of the wall. The two first harmonics,
magnetic torque around the domain wall, due to the                             δu1 cos χ and δu′1 sin χ, describe shifts of the domain wall
cos 2χ factor that originates from the d-wave order pa-                        in the x- and y-directions. The second harmonics de-
rameter. In addition, the factor cos 2χQ shows that the                        scribe quadrupolar distortions of the wall. By the or-
torque is controllable by the current direction. Currents                      thogonality of the angular harmonics, all terms vanish in
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   9

δWQ except the term ∝ δu2 cos 2χ. This term will give           (a)
rise to the elliptical deformation.
   We will now evaluate the work for the non-zero defor-
mation mode. We set δu(χ) = δu2 cos 2χ and perform
the radial and angular integrals in Eq. (25). We find
that,
             δWQ = FQ δu2 ,
                       π3 2                             (26)
               FQ =       ℏ ϱz Q2 C̄z cos 2χQ .
                      8w2                                       (b)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           (c)
                                                                               Q k x̂
                                                                                 <latexit sha1_base64="l7j8n7Jg436+0Rk+sN727jEOfPY=">AAAC6XichVHLahtBECxtHpaUh5X4GAhLRCAnsbINyVGQOPhiUMB6gCTE7GosL5p9MDsSVoRu/oHcQq6++Wr/jPMtObh2sgokJniW2e6prq7pnvZTFWbG825KzoOHjx5vlSvVJ0+fPd+uvXjZzZK5DmQnSFSi+77IpApj2TGhUbKfaikiX8meP/uYx3sLqbMwiY/NMpWjSEzj8CQMhCE0rr0e+omaZMuIZjVMhRZKSeUOT4VZna3X41rda3h2uXedZuHUUax2UvuJISZIEGCOCBIxDH0FgYzfAE14SImNsCKm6YU2LrFGlblzsiQZguiM/ylPgwKNec41M5sd8BbFrZnp4i33Z6vok53fKulntL+4v1ps+t8bVlY5r3BJ61OxYhWPiBucknFfZlQwN7Xcn5l3ZXCCD7abkPWlFsn7DP7ofGJEE5vZiIsDy5xSw7fnBV8gpu2wgvyVNwqu7XhCK6yVViUuFAX1NG3++qyHY27+O9S7Tne30dxr7H7Zr7caxcDLeIU3eMepvkcLh2izjgDnuMQVrp2Z88357vz4TXVKRc4O/lrOxS0i7pwx</latexit>
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    Q k ŷ
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      <latexit sha1_base64="ARttM1uq5mq3ALrgaFhMHFZu7mc=">AAAC6XichVHLSiNBFD22zzg+orMcGBrDgKvQUUGXgg9mMxDBqJCEUN2pxCbVD6orQgzZzQ/MTtzObrb6MzPf4sLTNa2gIlZTfW+de+6pe+v6qQoz43l/p5zpmdm5+YXS4qel5ZXV8tr6WZYMdSAbQaISfeGLTKowlg0TGiUvUi1F5Ct57g8O8vj5ldRZmMSnZpTKdiT6cdgLA2EIdcpfW36iutkoohm3UqGFUlK5rUthxqPJpFOueFXPLvetUyucCopVT8r/0EIXCQIMEUEihqGvIJDxa6IGDymxNsbENL3QxiUmWGTukCxJhiA64L/PU7NAY55zzcxmB7xFcWtmuvjGfWwVfbLzWyX9jPaB+9pi/XdvGFvlvMIRrU/FklX8QdzgkoyPMqOC+VTLx5l5VwY97NluQtaXWiTvM3jWOWREExvYiIsjy+xTw7fnK75ATNtgBfkrPym4tuMurbBWWpW4UBTU07T567Mejrn2eqhvnbOtam27unWyU9mvFgNfwBdsYJNT3cU+vqPOOgL8xB/c4d4ZOL+cG+f2P9WZKnI+48Vyfj8CJVacMg==</latexit>




Here, FQ is a generalized force acting on the displace-          deformed
                                                                 domain wall
ment δu2 . From the cos 2χQ dependence, we see that
this generalized force is controlled by the direction of the
applied supercurrent.
   We can now determine the equilibrium shape of the                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          undeformed
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              (no torque)
domain wall by balancing the generalized force FQ with
a phenomenological restoring force from the domain wall.
We write this restoring force as Frest = −kδu2 , where k is     FIG. 6. Supercurrent torque coefficient and current-
a phenomenological stiffness parameter. Force balancing         controlled domain-wall deformation. (a) Temperature
then requires FQ + Frest = 0. This constraint gives the         dependence of the altermagnetic torque coefficient, C̄z , nor-
                                                                malized to its maximum in the plotted range. Curves show
following equilibrium shape of the domain wall,
                                                                different altermagnetic splittings, ϱz µ/(ϱ0 ∆0 ). The torque
            R(χ) = R0 + δu2 cos 2χ,                             is quasiparticle-mediated. It vanishes at T = 0 for a fully
                                                                gapped spectrum and is suppressed again as the gap closes
                       π3 2                             (27)
              δu2 =         ℏ ϱz Q2 C̄z cos 2χQ .               near Tc . (b,c) The torque deforms a radial domain wall into an
                      8w2 k                                     ellipse. A supercurrent with Cooper-pair momentum Q ∥ x̂
                                                                deforms the radial domain wall along one principal axis of
Hence, for sufficiently small δu2 , the resulting equilibrium
                                                                the dx2 −y2 altermagnetic form factor. A supercurrent with
shape of the domain wall is elliptical. The elongation of
                                                                Q ∥ ŷ deforms the wall along the other principal axis. Plots
the ellipse is set by the sign of δu2 or, equivalently, by      are schematic.
the supercurrent direction, cos 2χQ . For δu2 > 0, the
ellipse will be elongated along x, while for δu2 < 0 it
will by elongated along y. Importantly, the supercurrent
                                                                altermagnet, scanning probes, in particular scanning tun-
does not allow for a continuous rotation of the ellipse.
                                                                neling microscopy, could be used to pick up the local
Instead, the possible elongation directions are fixed by
                                                                gap formation around domain walls. Consequently, one
the altermagnetic anisotropy.
                                                                would expect a transition from gapless spectra in homo-
                                                                geneous regions of the altermagnet to angular-dependent
      IX.   DISCUSSION AND CONCLUSION                           transitions from V-shaped to U-shaped tunneling spectra
                                                                around domain walls.
  In this work, we have shown that domain wall textures            Second, our findings also have implications for intrin-
or other forms of order parameter inhomogeneities, which        sic, i.e., interaction-induced, superconductivity in the al-
are expected to typically be present in altermagnetic sam-      termagnet itself: in the scenario with dominant inter-
ples, can play an important role for superconductivity:         actions in the spin-singlet Cooper-pair channel, a ho-
  First, while the time-reversal-odd spin-splitting of the      mogeneous altermagnetic order parameter can suppress
Fermi surfaces in a homogeneous altermagnet naturally           pairing; however, it might still nucleate around domain
suppresses the formation of a superconducting gap from          wall boundaries based on the mechanism we discuss here,
proximity-induced singlet pairing, domain-wall bound-           which should again be clearly visible in scanning probe
aries locally induce triplet components due to the emer-        experiments. Although in a very different regime, we
gent spin-orbit coupling; as we have shown, this gaps           note the similarity to the prediction [34, 36] that local,
out the BdG spectra in the vicinity of the domain wall          non-magnetic defects can enhance pairing in altermag-
and the spatial asymmetry of the altermagnet leads to re-       nets.
maining nodal points in momentum space or fully gapped             Third, it is instructive to provide a material estimate
spectra, depending on the position on the domain wall.          for the importance of the proposed spin triplet pairing.
As such, while the proximity effect from a superconduc-         We focus on Mn5 Si3 , as a candidate d-wave altermag-
tor into an altermagnet might not lead to significant           net [53]. The ratio between the spin triplet pairing,
global low-energy pairing correlations across the whole         ∆t , and the proximity-induced gap, ∆, is approximately
                                                                                                                               10
               p
∆t /∆ ∼ α/[ α2 + (∆AM /2)2 ], where α is an estimate                              ACKNOWLEDGMENTS
for the emergent spin-orbit coupling and ∆AM for the al-
termagnetic band splitting. At the domain wall radius,
we estimate α ∼ πℏv3 /4w with v3 = 2ϱ3 pF being a ve-
locity scale and pF being a Fermi momentum scale. We
take vF ∼ 2 × 106 m s−1 [54] and assume v3 ∼ 0.5vF .                 M.S.S. thanks S. Banerjee and U. Seifert for insight-
For a wall width w ∼ 50 nm, we find α ∼ 10.3 meV. For             ful discussions and acknowledges funding by the Euro-
∆AM ∼ 100 meV [55], this gives ∆t /∆ ∼ 0.2. Assum-                pean Union (ERC-2021-STG, Project 101040651— Su-
ing a proximity-induced gap of ∆ ∼ 0.5 meV, we find a             perCorr). Views and opinions expressed are however
triplet pairing contribution of ∆t ∼ 0.1 meV.                     those of the authors only and do not necessarily reflect
   Finally, in addition to the formation of spin-triplet su-      those of the European Union or the European Research
perconductivity, we have also shown that the application          Council Executive Agency. Neither the European Union
of a supercurrent can lead to torques on the textures.            nor the granting authority can be held responsible for
In particular, the resulting deformations of the domain           them. C.S. acknowledges support from the Louisiana
wall structure depend on the structure of the altermag-           Board of Regents. This work was performed in part at
netic order parameter. These results point to new ways            the Aspen Center for Physics, which is supported by Na-
of controlling altermagnetic textures with supercurrents.         tional Science Foundation grant PHY-2210452.




 [1] A. Hubert and R. Schäfer, Magnetic domains: the analy-            A. Rosch, “Emergent electrodynamics of skyrmions in a
     sis of magnetic microstructures (Springer Science & Busi-         chiral magnet,” Nature Physics 8, 301 (2012).
     ness Media, 1998).                                           [14] Y. Onishi, N. Paul, and L. Fu, “Emergent curved space
 [2] D. Kumar, T. Jin, R. Sbiaa, M. Kläui, S. Bedanta,                 and gravitational lensing in quantum materials,” Phys.
     S. Fukami, D. Ravelosona, S.-H. Yang, X. Liu, and S. N.           Rev. B 113, 024401 (2026).
     Piramanayagam, “Domain wall memory: Physics, mate-           [15] R. Cheng and Q. Niu, “Electron dynamics in slowly vary-
     rials, and devices,” Phys. Rep. 958, 1 (2022).                    ing antiferromagnetic texture,” Phys. Rev. B 86, 245118
 [3] G. Venkat, D. A. Allwood, and T. J. Hayward, “Mag-                (2012).
     netic domain walls: types, processes and applications,”      [16] O. Gomonay, “Berry-phase effects and electronic dynam-
     J. Phys. D: Appl. Phys. 57, 063001 (2023).                        ics in a noncollinear antiferromagnetic texture,” Phys.
 [4] A. Fert, N. Reyren, and V. Cros, “Magnetic skyrmions:             Rev. B 91, 144421 (2015).
     advances in physics and potential applications,” Nat.        [17] A. Okabayashi and T. Morinari, “Theory of spin mo-
     Rev. Mater. 2, 17031 (2017).                                      tive force in one-dimensional antiferromagnetic domain
 [5] Y. Zhou, S. Li, X. Liang, and Y. Zhou, “Topological Spin          wall,” Journal of the Physical Society of Japan 84, 033706
     Textures: Basic Physics and Devices,” Adv. Mater. 37,             (2015).
     e2312935. (2025), 38861696.                                  [18] Y. Yamane, J. Ieda, and J. Sinova, “Electric voltage
 [6] S. S. Parkin, M. Hayashi, and L. Thomas, “Magnetic                generation by antiferromagnetic dynamics,” Phys. Rev.
     domain-wall racetrack memory,” science 320, 190 (2008).           B 93, 180408 (2016).
 [7] A. Fert, V. Cros, and J. Sampaio, “Skyrmions on the          [19] I.    Mazin     (The     PRX       Editors),    “Editorial:
     track,” Nature nanotechnology 8, 152 (2013).                      Altermagnetism—a new punch line of fundamental
 [8] G. E. Volovik, “Linear momentum in ferromagnets,”                 magnetism,” Phys. Rev. X 12, 040002 (2022).
     Journal of Physics C: Solid State Physics 20, L83 (1987).    [20] L. Šmejkal, J. Sinova, and T. Jungwirth, “Emerging re-
 [9] P. Bruno, V. K. Dugaev, and M. Taillefumier, “Topolog-            search landscape of altermagnetism,” Phys. Rev. X 12,
     ical hall effect and berry phase in magnetic nanostruc-           040501 (2022).
     tures,” Phys. Rev. Lett. 93, 096806 (2004).                  [21] S. S. Fender, O. Gonzalez, and D. K. Bediako, “Al-
[10] S. A. Yang, G. S. D. Beach, C. Knutson, D. Xiao, Q. Niu,          termagnetism: A chemical perspective,” Journal of the
     M. Tsoi, and J. L. Erskine, “Universal electromotive force        American Chemical Society 147, 2257 (2025).
     induced by domain wall motion,” Phys. Rev. Lett. 102,        [22] R. Tamang, S. Gurung, D. P. Rai, S. Brahimi, and
     067201 (2009).                                                    S. Lounis, “Altermagnetism and altermagnets: A brief re-
[11] P. N. Hai, S. Ohya, M. Tanaka, S. E. Barnes, and                  view,” Magnetism 5 (2025), 10.3390/magnetism5030017.
     S. Maekawa, “Electromotive force and huge magnetore-         [23] T. Jungwirth, R. M. Fernandes, E. Fradkin, A. H. Mac-
     sistance in magnetic tunnel junctions,” Nature 458, 489           Donald, J. Sinova, and L. Šmejkal, “Altermagnetism: An
     (2009).                                                           unconventional spin-ordered phase of matter,” Newton 1
[12] S. E. Barnes and S. Maekawa, “Generalization of fara-             (2025), 10.1016/j.newton.2025.100162.
     day’s law to include nonconservative spin forces,” Phys.     [24] O. Gomonay, V. P. Kravchuk, R. Jaeschke-Ubiergo, K. V.
     Rev. Lett. 98, 246601 (2007).                                     Yershov, T. Jungwirth, L. Šmejkal, J. v. d. Brink, and
[13] T. Schulz, R. Ritz, A. Bauer, M. Halder, M. Wagner,               J. Sinova, “Structure, control, and dynamics of altermag-
     C. Franz, C. Pfleiderer, K. Everschor, M. Garst, and              netic textures,” npj Spintronics 2, 35 (2024).
                                                                                                                               11

[25] Z. Jin, Z. Zeng, Y. Cao, and P. Yan, “Skyrmion hall effect         prints (2026), arXiv:2601.03348 [cond-mat.mes-hall].
     in altermagnets,” Phys. Rev. Lett. 133, 196701 (2024).        [43] A. I. Buzdin and A. S. Mel’nikov, “Domain wall supercon-
[26] H. Vakili, E. Schwartz, and A. A. Kovalev, “Spin-transfer          ductivity in ferromagnetic superconductors,” Phys. Rev.
     torque in altermagnets with magnetic textures,” Phys.              B 67, 020503(R) (2003).
     Rev. Lett. 134, 176401 (2025).                                [44] Z. Yang, M. Lange, A. Volodin, R. Szymczak, and
[27] R. Zarzuela, R. Jaeschke-Ubiergo, O. Gomonay, L. Šme-              V. V. Moshchalkov, “Domain-wall superconductivity in
     jkal, and J. Sinova, “Transport theory and spin-transfer           superconductor–ferromagnet hybrids,” Nat. Mater. 3,
     physics in d-wave altermagnets,” Phys. Rev. B 111,                 793 (2004).
     064422 (2025).                                                [45] A. Maiani, A. C. C. Drachmann, L. Galletti, C. Schrade,
[28] R. Burkard, M. S. Scheurer, and U. F. P. Seifert,                  Y. Liu, R. S. Souto, and S. Vaitiekėnas, “Percolative
     “Anisotropic vacancy-induced magnetization textures in             supercurrent in superconductor–ferromagnetic insulator
     altermagnets,” arXiv e-prints (2026), arXiv:2607.07789             bilayers,” Phys. Rev. B 111, 174509 (2025).
     [cond-mat.str-el].                                            [46] H. Vakili, M. Ali, I. Žutić,            and A. A. Ko-
[29] J. Gondolf, A. Kreisel, M. Roig, Y. Yu, D. F. Agter-               valev, “Supercurrent-Driven Néel Torque in Supercon-
     berg, and B. M. Andersen, “Local signatures of alter-              ductor/Altermagnet Hybrids,” arXiv e-prints (2026),
     magnetism,” Phys. Rev. B 111, 174436 (2025).                       arXiv:2603.22243 [cond-mat.mes-hall].
[30] A. Maiani and R. S. Souto, “Impurity states in alter-         [47] Y. Fukaya, B. Lu, K. Yada, Y. Tanaka, and J. Cayao,
     magnetic superconductors,” Phys. Rev. B 111, 224506                “Superconducting phenomena in systems with unconven-
     (2025).                                                            tional magnets,” Journal of Physics: Condensed Matter
[31] P. Sukhachov and J. Linder, “Impurity-induced friedel              37, 313003 (2025).
     oscillations in altermagnets and p-wave magnets,” Phys.       [48] J. Linder and J. W. A. Robinson, “Superconducting spin-
     Rev. B 110, 205114 (2024).                                         tronics,” Nat. Phys. 11, 307 (2015).
[32] H.-R. Hu, X. Wan, and W. Chen, “Quasiparticle in-             [49] F. S. Bergeret, A. F. Volkov, and K. B. Efetov,
     terference in altermagnets,” Phys. Rev. B 111, 035132              “Odd triplet superconductivity and related phenomena
     (2025).                                                            in superconductor-ferromagnet structures,” Rev. Mod.
[33] W. Chen, X. Zhou, D. Zhang, Y.-Q. Xu, and W.-K. Lou,               Phys. 77, 1321 (2005).
     “Impurity scattering and friedel oscillations in altermag-    [50] M. Roig, A. Kreisel, Y. Yu, B. M. Andersen, and D. F.
     nets,” Phys. Rev. B 110, 165413 (2024).                            Agterberg, “Minimal models for altermagnetism,” Phys.
[34] M. M. Vasiakin and A. S. Mel’nikov, “Disorder-enhanced             Rev. B 110, 144412 (2024).
     superconductivity in altermagnet-superconductor hy-           [51] M. Roig, Y. Yu, R. C. Ekman, A. Kreisel, B. M. Ander-
     brids,” Phys. Rev. B 111, L100502 (2025).                          sen, and D. F. Agterberg, “Quasisymmetry-constrained
[35] G. A. Bobkov, I. V. Bobkova, and A. M. Bobkov, “Prox-              spin ferromagnetism in altermagnets,” Phys. Rev. Lett.
     imity effect in superconductor/antiferromagnet hybrids:            135, 016703 (2025).
     Néel triplets and impurity suppression of superconduc-        [52] Y. Nagai and H. Nakamura, “Multi-band eilenberger the-
     tivity,” Phys. Rev. B 108, 054510 (2023).                          ory of superconductivity: Systematic low-energy projec-
[36] D. Sedov and M. S. Scheurer, “Quantum geometry                     tion,” Journal of the Physical Society of Japan 85, 074707
     and impurity sensitivity of superconductors without                (2016), https://doi.org/10.7566/JPSJ.85.074707.
     time-reversal symmetry: application to rhombohedral           [53] H. Reichlova, R. Lopes Seeger, R. González-Hernández,
     graphene and altermagnets,” arXiv e-prints (2025),                 I. Kounta, R. Schlitz, D. Kriegner, P. Ritzinger,
     arXiv:2510.19943 [cond-mat.supr-con].                              M. Lammel, M. Leiviskä, A. Birk Hellenes, K. Olejník,
[37] A. Maiani, “Optical and transport anisotropies in                  V. Petřiček, P. Doležal, L. Horak, E. Schmoranzerova,
     spin-textured altermagnets,” arXiv e-prints         (2026),        A. Badura, S. Bertaina, A. Thomas, V. Baltz, L. Michez,
     arXiv:2602.14950 [cond-mat.mes-hall].                              J. Sinova, S. T. B. Goennenwein, T. Jungwirth, and
[38] C. Schrade and M. S. Scheurer, “Altermagnetic spin tex-            L. Šmejkal, “Observation of a spontaneous anomalous
     tures: Emergent electrodynamics, quantum geometry,                 hall response in the mn5si3 d-wave altermagnet candi-
     and probes,” arXiv e-prints (2026), arXiv:2602.20236               date,” Nature Communications 15, 4961 (2024).
     [cond-mat.mes-hall].                                          [54] C. Sürgers, G. Fischer, W. H. Campos, A. B. Hellenes,
[39] N. Heinsdorf and M. Franz, “Proximitizing altermagnets             L. Šmejkal, J. Sinova, M. Merz, T. Wolf, and W. Werns-
     with conventional superconductors,” Phys. Rev. B 113,              dorfer, “Anomalous nernst effect in the noncollinear anti-
     L020501 (2026).                                                    ferromagnet mn5si3,” Communications Materials 5, 176
[40] A. Hadjipaschalis, S. A. A. Ghorashi, and J. Cano, “Ma-            (2024).
     joranas with a twist: Tunable majorana zero modes in al-      [55] H. Reichlová, R. L. Seeger, R. González-Hernández,
     termagnetic heterostructures,” Phys. Rev. B 112, 214430            I. Kounta, R. Schlitz, D. Kriegner, P. Ritzinger, M. Lam-
     (2025).                                                            mel, M. Leiviskä, V. Petříček, P. Doležal, E. Schmoranze-
[41] O. Alam, A. Pal, P. Dutta, and A. Saha, “Proximity-                rová, A. Bad’ura, A. Thomas, V. Baltz, L. Michez,
     induced superconductivity and emerging topological                 J. Sinova, S. T. B. Goennenwein, T. Jungwirth, and
     phases in altermagnet-based heterostructures,” Phys.               L. Šmejkal, “Macroscopic time reversal symmetry break-
     Rev. B 113, 155429 (2026).                                         ing by staggered spin-momentum interaction,” (2021),
[42] C. Schrade, S. Manna, and M. S. Scheurer, “Al-                     arXiv:2012.15651 [cond-mat.mes-hall].
     termagnetic superconducting diode effect from non-
     collinear compensated magnetism in Mn3 Pt,” arXiv e-
                                                                                                                             1

                                                   Supplemental Material
                                Yasir Dar1 , Mathias S. Scheurer2 , and Constantin Schrade1
 1
     Hearne Institute of Theoretical Physics, Department of Physics & Astronomy, Louisiana State University, Baton
                                                   Rouge LA 70803, USA
                2
                  Institute for Theoretical Physics III, University of Stuttgart, 70550 Stuttgart, Germany


                         S1.    EFFECTIVE BOGOLIUBOV-DE GENNES HAMILTONIAN

  In this first section, we provide more details on the derivation of the effective low-energy Bogoliubov-de Gennes
(BdG) Hamiltonian for an altermagnetic texture proximitized by an s-wave superconductor.


                                                S1.1.     Normal-state Hamiltonian

     For convenience, we begin by redisplaying the normal state Hamiltonian for our altermagnetic spin texture,
                                      ĥ(r, p̂) = ε0,p̂ + tx,p̂ τx + tz,p̂ τz + J τz n(r) · s − µ,                        (S1)
Here, the Pauli matrices, τx,y,z , act in sublattice space and the Pauli matrices sx,y,z act in spin space. Moreover,
p̂ = −iℏ∇ is the momentum operator, µ is the chemical potential, and n(r) is the spatially-varying Néel vector. We
will assume that the exchange coupling, J > 0, is the dominant energy scale. For the kinetic terms, we will focus on
a d-wave altermagnetic spin texture, ε0,p̂ = ϱ0 (p̂2x + p̂2y ) , tz,p̂ = ϱz (p̂2x − p̂2y ), and tx,p̂ = ϱx + ϱ3 (p̂2x + p̂2y ).


                                                         S1.2.     Rotating frame

     As a first step, we move to a rotation frame where the local spin quantization axis aligns with n(r).

The unitary transformation to the rotating frame is defined through the requirement, U † (r) [n(r) · s] U (r) = sz . We
can write this transformation explicitly by parametrizing the Néel vector as,
                                                                                                           
                                                                         i
         n(r) = (sin θ cos ϕ, sin θ sin ϕ, cos θ) so that U (r) ≡ exp − θ(r) (− sin ϕ(r)sx + cos ϕ(r)sy ) .         (S2)
                                                                         2
Because U (r) is spatially varying, the momenta in the texture Hamiltonian will be shifted by a gauge potential,
                               Ai (r) = iℏU † (r)∂i U (r)        with π̂i ≡ U † (r)p̂i U (r) = p̂i − Ai (r).              (S3)
The resulting normal-state Hamiltonian in the rotating frame is thus given by,
                          ĥrot (r, π̂) ≡ U † (r) ĥ(r, p̂) U (r) = ε0,π̂ + tx,π̂ τx + tz,π̂ τz + J τz sz − µ,            (S4)
as already discussed in the main text.

We now add a technical consideration. We decompose the gauge field into components that are either paral-
                                                                ∥                       ∥
lel or perpendicular to the spin quantization axis, Ai (r) = Ai (r) + A⊥                                    ⊥
                                                                          i (r) with Ai ∝ sz , and Ai ∝ sx , sy . Such a
                                                                                            ∥
decomposition allows us to introduce the longitudinally shifted momentum, Π̂i ≡ p̂i − Ai (r) so that π̂i = Π̂i − A⊥i (r).
Using the texture parametrization given above, we can write the longitudinal and transversal components as,
                                          
                  ∥                       θ                       ℏ
                Ai (r) = −ℏ (∂i ϕ) sin 2
                                             sz , and A⊥  i (r) =   [(∂i θ) eϕ − sin θ (∂i ϕ) er ] · (sx , sy ).    (S5)
                                          2                       2
with the unit vectors er = (cos ϕ, sin ϕ)T and eϕ = (− sin ϕ, cos ϕ)T . We can also write the transversal component as,
                                     X                                        1
                       A⊥
                        i (r) = ℏ           eia (r) sa   with      eix (r) = − [(∂i θ) sin ϕ + sin θ(∂i ϕ) cos ϕ] ,
                                    a=x,y
                                                                              2
                                                                                                                          (S6)
                                                                            1
                                                                   eiy (r) = [(∂i θ) cos ϕ − sin θ(∂i ϕ) sin ϕ] .
                                                                            2
                                                                                                                             2

                                       S1.3.    Bogoliubov-de Gennes Hamiltonian

   As a second step, we introduce the superconducting pairing and the BdG Hamiltonian. We define ψ̂(r) =
(ĉ+,↑ , ĉ+,↓ , ĉ−,↑ , ĉ−,↓ )T as the electron spinor in spin- and sublattice-space, and Ψ̂(r) = (ψ̂(r), ψ̂ † (r)T )T as the
Nambu spinor. In this basis, the BdG Hamiltonian is given by,
                                                                          ˆ
                                                                                   
                                                               ĥ(r, p̂) ∆(r)
                                                 ĤBdG (r) = ˆ †                      .                                    (S7)
                                                                ∆ (r) −ĥT (r, −p̂)
We will choose the pairing matrix to be of the form,
                                                      ˆ
                                                      ∆(r) = ∆(r) τx (isy ).                                              (S8)
As discussed in the main text, this pairing matrix corresponds to inter-sublattice spin-singlet pairing and will be non-
zero upon projection onto the low-energy subspace of the normal-state Hamiltonian. To introduce this low-energy
subspace, we define the operators S ≡ τz sz and the corresponding projectors P± ≡ 21 (1 ± S). We associate S = −1
with the low-energy subspace with projector P− , and S = +1 with the high-energy subspace with projector P+ .


                          S1.4.   Bogoliubov-de Gennes Hamiltonian in the rotating frame

  As a third step, we transform the BdG Hamiltonian into the rotating frame. We define,
                                                  
                                       U (r)  0
                              U(r) =                 so that ĤBdG,rot ≡ U † ĤBdG U.                                     (S9)
                                         0 U ∗ (r)

We note that U † (r)(isy )U ∗ (r) = isy . As a result, the pairing term is unchanged upon moving to the rotating frame.
The BdG Hamiltonian in the rotating frame reads,
                                                                                        
                                                        ĥrot (r, π̂)   ∆(r)τx (isy )
                                   ĤBdG,rot (r) =                                         .                      (S10)
                                                     −∆∗ (r)τx (isy ) −[ĥrot (r, −π̂)]T


                          S1.5.   Low-energy effective Bogoliubov-de Gennes Hamiltonian

  As a fourth step, we project the BdG Hamiltonian onto the S = −1 subspace.

To formulate the projection, it is initially useful to define Pauli matrices, σx,y,z , that act in the low-energy
S = −1 subspace spanned by |1⟩ and |2⟩. These Pauli matrices can be defined as, σ0 ≡ P− τ0 s0 P− , σx ≡ P− τx sx P− ,
σy ≡ −P− τx sy P− , and σz ≡ P− τz s0 P− .

Next, we define the projector onto the low-energy subspace,
                                                              
                                                         P− 0
                                                 P− ≡            .                                                       (S11)
                                                          0 P−
The low-energy effective BdG Hamiltonian is then given by,
                                                                                            
                                                          ĥproj (r, Π̂)   ∆(r) (−iσy )
                        ĤBdG,proj ≡ P− ĤBdG,rot P− =                                         .                         (S12)
                                                         −∆∗ (r) (−iσy ) −[ĥproj (r, −Π̂)]T
Here, the diagonal components involve the projected normal-state Hamiltonian,
                                                                                                 (0)
                          ĥproj (r, Π̂) = ε0,Π̂ + tz,Π̂ σz + ϱ0 V0 (r) + ϱz Vz (r) σz − µ + ĥSOC (r).                  (S13)
with the emergent spin-orbit coupling,

                                  ĥSOC (r) = −ϱ3 P− τx {p̂i , A⊥i } P−
                                                                                                                         (S14)
                                                   X
                                            = −ℏϱ3       ({p̂i , eix (r)}σx − {p̂i , eiy (r)}σy ) .
                                                      i=x,y
                                                                                                                                3

                                   2
which arises from τx π̂ 2 = τx Π̂ − τx {Π̂i , A⊥         ⊥ ⊥                          ⊥             ⊥
                                               i } + τx Ai Ai and noting that {Π̂i , Ai } = {p̂i , Ai }.


The projected normal-state Hamiltonian also contains the quantum metric and the scalar potentials,
                          1
              gij (r) ≡     ∂i n(r) · ∂j n(r),   V0 (r) ≡ ℏ2 δ ij gij (r),    Vz (r) ≡ ℏ2 η ij gij (r),   η = diag(1, −1).   (S15)
                          4

                             S1.6.     Radial domain wall and removal of the gauge potential

  As a fifth step, we focus on the example of a radial domain wall texture. For this texture, we will show that the
longitudinal gauge field can be removed through a unitary transformation, so that the low-energy BdG Hamiltonian
takes on a particularly simple form.

We initially parametrize the radial domain wall texture as,

                                                                                        r − R0
                                                                                              
                                                                         π    π
                 n(r) = (cos ϕ(r), sin ϕ(r), 0) with              θ(r) =
                                                                  and ϕ(r) = tanh                ,                           (S16)
                                                                         2    2           w
                                                                            p
where we have introduced the parametrization r = (r cos χ, r sin χ) with r = x2 + y 2 .

For this radial domain wall texture, the longitudinal gauge field and the shifted momenta are,

                                          ∥         ℏ                                  ℏ
                                         Ai (r) =     (∂i ϕ)σz     and Π̂i = p̂i −       (∂i ϕ)σz ,                          (S17)
                                                    2                                  2
where we have used that P− sz P− = −σz .

An important simplification for the radial domain wall example is that the longitudinal gauge field can be
removed from the kinetic terms via the unitary,
                                                                          i
                                                         W (r) ≡ e− 2 ϕ(r)σz ,                                               (S18)

which satisfies the following properties,

                                                                    (0)           ℏϱ3 X
                             W (r)Π̂i W † (r) = p̂i    and       W ĥSOC W † =             {p̂i , ∂i ϕ(r)}σx .               (S19)
                                                                                   2 i=x,y

To show these properties, we have used that W † σx W = cos ϕ σx − sin ϕ σy .

We apply this transformation to the Bogoliubov-de Gennes Hamiltonian via,
                                                                
                                                    W (r)   0
                                           W(r) =                  .                                                         (S20)
                                                      0   W ∗ (r)

The transformed Bogoliubov-de Gennes Hamiltonian is given by,
                                                                                                                        
                                                                      †           ĥproj (r, p̂) ∆(r)(−iσy )
                 ĤBdG,proj (r, p̂) → W(r)ĤBdG,proj (r, Π̂)W (r) =                 ∗                                        (S21)
                                                                                 −∆ (r)(−iσy ) −ĥproj (r, −p̂)T

with the transformed normal-state Hamiltonian,
                                                                                          ℏϱ3 X
                   ĥproj (r, p̂) → ε0,p̂ + tz,p̂ σz + ϱ0 V0 (r) + ϱz Vz (r)σz − µ +               {p̂i , ∂i ϕ(r)}σx .       (S22)
                                                                                           2 i=x,y
                                                                                                                        4

                                       S2.   ANOMALOUS GREEN’S FUNCTION

 In this section, we provide more details on the derivation of the anomalous Green’s function for the radial alter-
magnetic texture discussed in the main text.


                                    S2.1.    Coordinates and normal state Hamiltonian

  As a first step, we parameterize the center-of-mass coordinate and relative momentum,
                                R = R(cos χ, sin χ),       and     p = p(cos(χ + δ), sin(χ + δ)).                    (S23)
With this choice, we have pR = p · R̂ = p cos δ and p2x − p2y = p2 cos 2(χ + δ). The semiclassical normal state
Hamiltonian then takes on the form,
                                        hproj (R, p) = ξ(R, p) + αp (R)σx + bz (R, p)σz                              (S24)
with
                                 ℏ2 ϱ 0 ′
                ξ(R, p) = ϱ0 p2 +      ϕ (R)2 − µ,                          αp (R) = p · α(R) = ℏϱ3 ϕ′ (R)p cos δ,
                                   4                                                                                 (S25)
                                              ℏ2 ϱ z ′
            bz (R, p) = ϱz p2 cos 2(χ + δ) +        ϕ (R)2 cos 2χ.
                                               4

                                    S2.2.    Evaluating the anomalous Green’s function

  As a second step, we obtain the anomalous Green’s function from the off-diagonal components of the Nambu space
Green’s function as given in the main text,
                                                                                                  
                                        −1                          hproj (R, p)    ∆(R)(−iσy )
      G(R, p; iωn ) ≈ iωn − HBdG (R, p)      with HBdG (R, p) =                                      .     (S26)
                                                                    −∆(R)(−iσy ) −hproj (R, −p)T
Here, for simplicity, we have chosen ∆(R) to be real-valued. From a matrix inversion, we find for the off-diagonal
components,
                                           2∆ αp (ξ − bz )                                2∆ αp (ξ + bz )
                        F↑↑ (iωn ) =     2     2 )(ω 2 + E 2 ) ,    F↓↓ (iωn ) = −      2     2 )(ω 2 + E 2 ) .      (S27)
                                       (ωn + E+     n      −                          (ωn + E+     n      −

Here, we have dropped the (R, p) arguments from the respective expressions for notational brevity. The local quasi-
particle energies are given by,
                                                             q
                                 2
                                E± = ∆2 + ξ 2 + αp2 + b2z ± 2 ξ 2 (αp2 + b2z ) + ∆2 b2z .                    (S28)

We can now compute the equal-time pairing correlation by summing over the Matsubara frequencies,
                                                      X
                                      Fσσ (R, p) = T      Fσσ (R, p; iωn ).                                          (S29)
                                                                   ωn

We find that,
                                                                                    
                                                  ∆      tanh(E− /2T ) tanh(E+ /2T )
                            Fσσ = αp (σξ − bz ) 2    2                −                .                             (S30)
                                               E+ − E−        E−            E+
The result in the main text is the zero-temperature limit of this expression. Here, we have used that,
                                                                                      
                                       1                  1           1           1
                                     2 )(ω 2 + E 2 ) =  2 − E2           2 −         2   ,                           (S31)
                            (ωn2 + E+     n     −      E+    −    ωn2 + E−    ωn2 + E+
and the Matsubara sum,
                                                                                     
                                                  X       1        1             E
                                              T                 =    tanh                 .                          (S32)
                                                  n
                                                      ωn2 + E 2   2E             2T
                                                                                                                     5

                                   S3.    SUPERCURRENT-INDUCED TORQUES

                                                S3.1.    Free energy density

   In this first subsection, we provide more details on obtaining the free energy density of the BdG Hamiltonian with
a finite Cooper-pair momentum.

We begin by redisplaying the BdG Hamiltonian with a finite Cooper-pair momentum,
                                                                                        
                                          hproj (R, p + ℏQ/2)        ∆(R)(−iσy )
                       HBdG (R, p; Q) =                                                T   ,                     (S33)
                                            −∆(R)(−iσy )      − [hproj (R, −p + ℏQ/2)]
and the free energy,
                                                        T X
                                         Ω[ϕ, Q] = −        Tr ln [iωn − HBdG (Q)] .                             (S34)
                                                        2 ω
                                                           n


For the subsequent calculations, it will be useful to write the free energy more explicitly in terms of the eigenbalues
of the BdG Hamiltonian. We will denote these eigenvalues by Ea (R, p; Q) with a = 1, · · · , 4. We can note that (up
to an energy-independent constant),
                     T X                   1                                                  1
                   −       ln [iωn − E] = g(E) with g ′ (E) = f (E) and f (E) = E/T                .              (S35)
                     2 ω                   2                                              e     +1
                            n


As a result, the change in the free energy due to the finite Cooper-pair momentum can be written as,
                                                                 4
                                                           d2 p X
                                              Z      Z
                                            1     2
                  ΩQ ≡ Ω[ϕ, Q] − Ω[ϕ, 0] =      d R                 [g(Ea (R, p; Q)) − g(Ea (R, p; 0))]          (S36)
                                            2            (2πℏ)2 a=1

We remark that this change in the free energy should, in principle, also comprise a contribution from the double of
the degrees of freedom in the Nambu representation. However, this contribution is texture-independent. It will thus
not be of relevance for our subsequent considerations. It reads,
                       d2 p                                                   d2 p
          Z       Z                                                Z      Z
        1     2                                                       2
             d R            tr [hproj (R, p + q) − hproj (R, p)] =   d  R          [ξ(R, p + q) − ξ(R, p)] ,  (S37)
        2            (2πℏ)2                                                 (2πℏ)2
where the trace is over the effective spin degrees of freedoms and we used that σx and σz are traceless.


                                                S3.2.    Superfluid stiffness

  In this second subsection, we provide more details on obtaining an expression for the superfluid stiffness.

The superfluid stiffness, Dij (R), is defined through the expansion of the free energy,
                                        Z                    Z
                                            2      i       1
                                 ΩQ = d R Qi J (R) +           d2 R Qi Qj Dij (R) + . . . .                      (S38)
                                                           2
To obtain an explicit expression for it, we note the expansion,
                                                              1
                       g(Ea (p; Q)) = g(Ea ) + Qi f (Ea )vai + Qi Qj f ′ (Ea )vai vaj + f (Ea )mij
                                                                                                  
                                                                                                a + ...,         (S39)
                                                              2
where we have adopted the short-hand notations,
                                                      ∂Ea (p; Q)                ∂ 2 Ea (p; Q)
                           Ea ≡ Ea (p; 0),    vai ≡                  ,   mij
                                                                          a ≡                 .                  (S40)
                                                        ∂Qi      Q=0              ∂Qi ∂Qj Q=0
A direct comparsion then gives the expression,
                                                     4
                                               d2 p X  ′
                                          Z
                                   ij   1
                                                        f (Ea )vai vaj + f (Ea )mij
                                                                                    
                                 D =                                             a .                             (S41)
                                        2    (2πℏ)2 a=1
                                                                                                                           6

                                    S3.3.     Gradient expansion of the superfluid stiffness

  In this third subsection, we provide more details on the gradient expansion of the superfluid stiffness. Specifically,
up to second order in gradients of the texture angle, we have,
                                                                     1
                             Dij = D̄ij + ϱ0 C̄0ij V0 + ϱz C̄zij Vz + Āij;mn αm αn + O (∂i ϕ)4 .
                                                                                              
                                                                                                                        (S42)
                                                                     2
Here, we have defined,

                                                         ∂Dij                     ∂Dij                      ∂ 2 Dij
                         D̄ij = Dij ,         C̄0ij =             ,    C̄zij =             ,   Āij;mn =            .   (S43)
                                                        ∂(ϱ0 V0 )                ∂(ϱz Vz )                 ∂αm ∂αn

The overline should be understood as evaluating the derivative first and, subsequently, evaluating the expression in
the uniform limit,

                                                              V0 = Vz = αi = 0.                                         (S44)

We note that there is no term linear in αm in the expansion. Changing αm → −αm , or equivalently αp σx → −αp σx ,
is generated by a π-rotation around the z-axis in spin space. Since this is a basis transformation, the spectrum and
the superfluid stiffness are invariant under αm → −αm .


                                      S3.4.       Quasiparticle spectrum in limiting cases

  In this fourth subsection, we provide the quasiparticle spectrum of the proximitized planar domain wall in limiting
cases that will be of relevance for our subsequent discussions.

First, in the absence of the emergent spin-orbit coupling, αp = 0, the quasiparticle spectrum is given by,

                      ξ(p + ℏQ/2) − ξ(p − ℏQ/2) s
       Esτ (p; Q) =                            + [bz (p + ℏQ/2) + bz (p − ℏQ/2)]
                                  2             2
                         r                                                                                              (S45)
                                    1                                                            2
                      + τ ∆(R)2 + [ξ(p + ℏQ/2) + ξ(p − ℏQ/2) + s (bz (p + ℏQ/2) − bz (p − ℏQ/2))] .
                                    4
Second, if also the Cooper-pair momentum vanishes, Q = 0, then the quasiparticle spectrum is given by,
                                                                    p
                                  Esτ (p) ≡ Esτ (p; 0) = sbz (p) + τ ξ(p)2 + ∆2 .                                       (S46)

Third, if we adopt also the uniform limit where also V0 = Vz = 0, then the quasiparticle spectrum takes on the form,
                                                                p
                                   Ēsτ (p) = sϱz η mn pm pn + τ (ϱ0 p2 − µ)2 + ∆2 .                           (S47)


                                               S3.5.      Superfluid stiffness coefficient

  In this fifth subsection, we provide more details on evaluating the coefficient C̄zij .

First, we write the superfluid stiffness in the form,
                                                      4
                                                d2 p X ij
                                          Z
                                      1
                           D   ij
                                    =                   D             with   Daij ≡ f ′ (Ea )vai vaj + f (Ea )mij
                                                                                                               a.       (S48)
                                      2       (2πℏ)2 a=1 a

The coefficient C̄zij is then given by,
                                                                              4
                                                                        d2 p X ∂Daij
                                                                  Z
                                                            1
                                                    C̄zij =                                .                            (S49)
                                                              2       (2πℏ)2 a=1 ∂(ϱz Vz )
                                                                                                                           7

Second, we apply the chain rule to find,

       ∂Daij                                                       ∂vai               ∂vaj                 ∂mij
                                                                                             
                    ∂Ea  ′′        i j     ′      ij
                                                       ′                   j     i                            a
                =           f (Ea )va va + f (Ea )ma + f (Ea )             va + v a             + f (Ea )           .   (S50)
      ∂(ϱz Vz )   ∂(ϱz Vz )                                      ∂(ϱz Vz )          ∂(ϱz Vz )             ∂(ϱz Vz )

We will be interested in this expression in the uniform limit. When αp = 0, the geometric Zeeman field, Vz , enters
the quasiparticle energies, Esτ (p; Q), only as a Q-independent shift. As a result,

                                                  ∂vai                     ∂mija
                                                          = 0 and                   = 0.                                (S51)
                                                ∂(ϱz Vz )                 ∂(ϱz Vz )
We then find the following expressions for the superfluid stiffness coefficient,
                                                     4 
                                               d2 p X
                                         Z                        
                                     1                    ∂Ea        ′′
                             C̄zij =                                 f (Ēa )v̄ai v̄aj + f ′ (Ēa )m̄ij
                                                                                                        
                                                                                                     a .                (S52)
                                     2       (2πℏ)2 a=1 ∂(ϱz Vz )

In the uniform limit, we can label the quasiparticle energies by a = (s, τ ). In this case, the above expressions simplifies
to,

                                            d2 p
                                        Z
                                      1            X 
                              C̄zij =                    s f ′′ (Ēsτ )v̄sτ
                                                                         i    j
                                                                                 + f ′ (Ēsτ )m̄ij
                                                                                                   
                                                 2
                                                                            v̄sτ                sτ .                 (S53)
                                      2   (2πℏ) s,τ =±1

We now want to derive the tensorial structure of C̄zij . We therefore focus on the relevant limit when V0 = αp = 0.
In this case, the system is invariant under an exchange of coordinates, x ↔ y, combined with a spin-flip operation.
More precisely, at the level of the normal-state Hamiltonian,
                                                                           
                                                                        0 1
                     Ux hproj (Xp; −Vz )Ux† = hproj (p; Vz ) with X ≡          and Ux = −iσx .                (S54)
                                                                        1 0

At the level of the BdG Hamiltonian,
                                                                                                         
                                                                                                   Ux 0
                        Ux HBdG (Xp; XQ, −Vz )Ux† = HBdG (p; Q, Vz )                with     Ux =           .           (S55)
                                                                                                    0 Ux∗

Because the trace-log is invariant under unitary transformations and the momentum integration is unchanged under
p → Xp, the free energy satisfies,

                                                   ΩQ (Vz , Q) = ΩQ (−Vz , XQ).                                         (S56)

To fulfill this requirement, the superfluid stiffness needs to satisfy,

                                                   Dij (Vz ) = X i k X j l Dkl (−Vz )                                   (S57)

and the Vz coefficient in the gradient expansion of the superfluid stiffness needs to satisfy,

                                                         C̄zij = −Xki Xlj C̄zkl .                                       (S58)

This condition constrains the Vz to the form,
                                                                                        1
                                      C̄zij = C̄z η ij   or, equivalently, C̄z =          ηij C̄zij .                   (S59)
                                                                                        2
In particular, we note that the contribution to the superfluid stiffness that is ∝ Vz can be written as,
                                                      Vz
                                                     DQ  ≡ ϱz Vz Q̂i Q̂j C̄zij
                                                          = ϱz Vz C̄z (Q̂2x − Q̂2y )                                    (S60)
                                                          = ϱz Vz C̄z cos 2χQ

with the parameterization Q̂ = (cos χQ , sin χQ ).
                                                                                                                                      8

                                                    S3.6.    Torque contributions

  In this sixth subsection, we provide more details on the derivation of the contributions to the supercurrent-induced
torque.

We will focus on the planar radial texture with Néel vector n(R) = (cos ϕ(R), sin ϕ(R), 0). Since the Néel
vector varies only within the x-y-plane, the only component of the supercurrent-induced torque is in the z-direction
and given by,
                                                                    
                                                                δΩQ
                                             τQ (R) = −ẑ · n ×        .                                       (S61)
                                                                 δn
To evaluate this torque component, we consider the variation of the supercurrent-induced change of the free energy
density with respect to n(R), or, equivalently, ϕ(R). We find that,
                                  Z                     Z
                                     2   δΩQ                    δΩQ
                                    d R       δϕ = δΩ = d2 R         · δn
                                          δϕ                     δn
                                                        Z
                                                                δΩQ
                                                      = d2 R         · (ẑ × n) δϕ                           (S62)
                                                                 δn
                                                        Z                     
                                                                           δΩQ
                                                      = d2 R ẑ · n ×            δϕ.
                                                                            δn
We thus conclude that,
                                                                           δΩQ
                                                            τQ (R) = −         .                                                 (S63)
                                                                            δϕ
As a next step, we return to the gradient expansion of the superfluid stiffness,
                                                                     1
                               DQ = D̄Q + ϱ0 C̄0,Q V0 + ϱz C̄z,Q Vz + Āmn                4
                                                                                            
                                                                        Q αm αn + O (∂i ϕ)    ,                                  (S64)
                                                                     2
with D̄Q = Q̂i Q̂j D̄ij , C̄0,Q = Q̂i Q̂j C̄0ij , C̄z,Q = Q̂i Q̂j C̄zij , and Āmn
                                                                                Q = Q̂i Q̂j Ā
                                                                                               ij;mn
                                                                                                     . We now recall that for our d-wave
radial domain wall texture, we have,
                                           ℏ2 ij                       ℏ2 ij
                                    V0 =     δ ∂i ϕ ∂j ϕ,      Vz =      η ∂i ϕ ∂j ϕ,       αi = ℏt3 ∂i ϕ                        (S65)
                                           4                           4
with the variations,
                                ℏ2 ij                       ℏ2 ij
                                   δ ∂i ϕ ∂j δϕ, δVz =
                               δV0 =                          η ∂i ϕ ∂j δϕ, δαi = ℏt3 ∂i δϕ.                                     (S66)
                                 2                          2
We can now use these expressions for computing the variation of the free energy,
                                   Q2
                                       Z
                                          d2 R ϱ0 C̄0,Q δV0 + ϱz C̄z,Q δVz + Āmn
                                                                                        
                           δΩQ ≈                                               Q αn δαm
                                    2
                                   Q2
                                       Z
                                =         d2 R TQj ∂j δϕ                                                                         (S67)
                                    2
                                     Q2
                                         Z
                                =−          d2 R (∂j TQj )δϕ
                                      2
In the last equality, we have integrated-by-parts and excluded the boundary term due to periodic boundary conditions
in ϕ. Moreover, we have defined,
                                           ℏ2 ϱ0                   ℏ2 ϱ z
                                   TQj =         C̄0,Q δ ij ∂i ϕ +        C̄z,Q η ij ∂i ϕ + ℏ2 t23 Ājn
                                                                                                     Q ∂n ϕ.                     (S68)
                                            2                       2
We can now read off the torque as,
                                                             V0    Vz    SOC
                                                       τQ = τQ  + τQ  + τQ   .                                                   (S69)
with
                    Q2
                           2
                                                              Q2
                                                                     2
                                                                                                          Q2 h 2 2 jn
                                                                                        
             V0            ℏ ϱ0                       Vz             ℏ ϱz                                                   i
            τQ  =      ∂j       C̄0,Q δ ij ∂i ϕ ,    τQ  =       ∂j       C̄z,Q η ij ∂i ϕ ,         α
                                                                                                   τQ =     ∂j ℏ t3 ĀQ ∂n ϕ .   (S70)
                    2       2                                 2       2                                   2
                                                                                                                       9

                                       S4.    DOMAIN WALL DEFORMATION

  In this section, we will provide details on the deformation of the planar radial domain wall with Néel vector
n(r) = (cos ϕ0 (r), sin ϕ0 (r), 0) due to the altermagnetic torque. Here, ϕ0 (r) = (π/2) tanh((r − R0 )/w) is the texture
angle in the absence of the torque.

Suppose that the altermagnetic torque,
                                                        ϕ′0 (r)                   ℏ2 ϱz Q2
                                                               
                         Vz                     ′′
                        τQ  (r) = TQ cos 2χ    ϕ0 (r) −             with   TQ =            C̄z cos 2χQ ,           (S71)
                                                           r                          4
gives rise to a small deformation of the Néel texture, ϕ0 (r) → ϕ0 (r) + δϕ(r). In this case the work done by torque is
given by,
                                                      Z
                                                              Vz
                                              δWQ = d2 r τQ      (r)δϕ(r).                                       (S72)

Suppose now that this deformation of the Néel texture is due to an angular-dependent change of the domain wall
radius,
                                                      R(χ) = R0 + u(χ).                                            (S73)
In this case the angle in the texture angle changes to,
                                                ϕ(r, χ) ≡ ϕ0 (r − u(χ))
                                                                                                                   (S74)
                                                        ≈ ϕ0 (r) − u(χ)ϕ′0 (r).
Hence, for a small radial displacement δu(χ), we have a change of the texture angle,
                                                  δϕ(r, χ) = −ϕ′0 (r)δu(χ).                                        (S75)
The resulting work done on the texture is given by,
                                  Z
                          δWQ = r dr dχ τQ    Vz
                                                 (r, χ)[−ϕ′0 (r)δu(χ)]
                                                             Z ∞
                                                                                       ϕ′0 (r)
                                        Z                                                     
                                                                        ′      ′′
                               = −TQ dχ cos 2χ δu(χ)              r dr ϕ0 (r) ϕ0 (r) −                             (S76)
                                                               0                          r
                                       2 Z
                                  TQ π
                               ≡           dχ cos 2χ δu(χ)
                                    2w
where we have evaluated the radial integral in the limit when R0 ≫ w,
                                      Z ∞
                                                                  ϕ′ (r)      π2
                                                                        
                                           r dr ϕ′0 (r) ϕ′′0 (r) − 0       ≈−                                      (S77)
                                       0                            r         2w
It is now useful to perform a Fourier expansion δu(χ),
                           δu(χ) = δu0 + δu1 cos χ + δu′1 sin χ + δu2 cos 2χ + δu′2 sin 2χ + . . .                 (S78)
All shown contributions except the one ∝ δu2 vanish upon insertion into the expression for δWQ . As a result,
                                                                π3 2
                                   δWQ = FQ δu2       with   FQ = ℏ ϱz Q2 C̄z cos 2χQ                              (S79)
                                                               8w
where FQ is a generalized force that acts on the coordinate u2 .

In equilibrium, we assume that this force is approximately balanced by a restoring force that is linear in u2 ,
Frest = −ku2 . In equilibrium, when FQ + Frest = 0, we find,
                                                   π3 2
                                               u2 =   ℏ ϱz Q2 C̄z cos 2χQ .                                        (S80)
                                                  8wk
In this situation, the parameterization of the domain wall is given by,
                                                   R(χ) = R0 + u2 cos 2χ,                                          (S81)
which shows that the domain wall takes on an elliptical shape.
                                                                                                                                10

                                             S5.       SIMULATION DETAILS

                                      S5.1.        Simulation parameters for Fig. 2

  In Fig. 2 of the main text, we plot the local quasiparticle spectrum for the radial domain wall given by,
                                                               q
                                   2
                                 E±  = ∆2 + ξ 2 + αp2 + b2z ± 2 ξ 2 (αp2 + b2z ) + ∆2 b2z .                                   (S82)

The relevant quantities entering this expression are,
                                  ϱ0 ′
                     ξ = ϱ 0 p2 +     ϕ (R)2 − µ,                                      αp = ϱ3 ϕ′ (R) px cos χ + py sin χ ,
                                                                                                                         
                                   4
                                          ϱz                                                    π
                                                                                                         
                                                                                                           r − R0
                                                                                                                             (S83)
                    bz = ϱz (p2x − p2y ) + ϕ′ (R)2 cos 2χ,                            ϕ′ (r) =     sech2            .
                                          4                                                    2w            w

The simulation parameters are,

                                                 ϱ0        ϱz        ϱ3       µ       ∆ R0     w
                                              1.00 0.40 0.70 1.70 0.25 6.0 1.65

                                    TABLE S1. Simulation parameters for Fig. 2.
                                                                                                            p
We remark that in all simulations, we set ℏ = 1 and use the momentum scale p0 =                                 µ/ϱ0 .


                                      S5.2.        Simulation parameters for Fig. 3

  In Fig. 3 of the main text, we plot the equal-spin correlation function,
                                                                                    
                                                 ∆       tanh(E− /2T ) tanh(E+ /2T )
                           F↑↑ = αp (ξ − bz ) 2      2                  −              .                                      (S84)
                                             E+ − E−           E−           E+

The simulation parameters are,

                                            ϱ0        ϱz        ϱ3        µ       ∆     T     R0   w
                                            1.00 0.40 0.70 1.70 0.25 0.06 6.0 1.65

                                    TABLE S2. Simulation parameters for Fig. 3.




                                      S5.3.        Simulation parameters for Fig. 4

  In Fig. 4 of the main text, we plot the triplet intensity,
                                                                                                        2
                                                                         d2 p
                                                            Z
                                       Itσσ (R) =                             2
                                                                                p Fσσ (R, p) .                                (S85)
                                                                |p|≤pc (2πℏ)


The simulation parameters are,

                                       ϱ0     ϱz       ϱ3        µ        ∆       T      R0    w       pc
                                      1.00 0.70 0.90 1.70 0.25 0.06 6.0 1.10 2.15p0

                                    TABLE S3. Simulation parameters for Fig. 4.
                                                                                                                      11

                                            S5.4.    Simulation details for Fig. 5

  In Fig. 5 of the main text, we plot the altermagnetic torque for a given Q̂ = (cos χQ , sin χQ ). It is given by,

                                                                         ϕ′ (r)
                                                                               
                                      Vz                          ′′
                                     τQ (r, χ) ∝ cos 2χQ cos 2χ ϕ (r) −           .                                 (S86)
                                                                           r

We plot the results in terms of the dimensionless radial coordinate, r/R0 . We further choose R0 /w = 7.5.


                                            S5.5.    Simulation details for Fig. 6

  In Fig. 6 of the main text, we evaluate the torque coefficient,

                                           d2 p
                                       Z
                                   ηij            X 
                                                       s f ′′ (Ēsτ )v̄sτ v̄sτ + f ′ (Ēsτ )m̄,ij
                                                                       ,i ,j
                                                                                                  
                             C̄z =              2                                             sτ .                 (S87)
                                    4    (2πℏ) s,τ =±1

In our simulations, we set ℏ = kB = 1. For the uniform quasiparticle levels, we take,
                                                     p
                             Ēsτ = sϱz p2 cos 2θ + τ ξ 2 + ∆(T )2 with ξ = ϱ0 p2 − µ.                             (S88)

For the temperature dependence of the superconducting gap, we choose,
                                                  r        !
                                                    Tc
                            ∆(T ) = ∆0 tanh 1.74       −1      with ∆0 = 1.76Tc .                                  (S89)
                                                     T

The additional terms in the expression for the torque coefficient are given by,

                                i    j                                     ξ                 ξ2
                          ηij v̄sτ v̄sτ = ϱ20 p2 cos 2θ + 2sτ ϱ0 ϱz p             p2 + ϱ2z 2     p2 cos 2θ,
                                                                        ξ 2 + ∆2          ξ + ∆2
                                                                                                                   (S90)
                                                              ∆2
                             ηij m̄ijsτ = sϱ  z + τ ϱ 2
                                                      z            3/2
                                                                       p2 cos 2θ,
                                                        (ξ 2 + ∆2 )

where we have parameterized the momentum as px = p cos θ and py = p sin θ. We then perform a change of variables,
p2 = (ξ + µ)/ϱ0 , so that the integration measures changes to,
                                                                    Z ξcutoff        Z 2π
                                                d2 p
                                           Z
                                                            1
                                                    2
                                                      =                         dξ          dθ.                    (S91)
                                               (2π)     2ϱ0 (2π)2    −µ               0

The simulation parameters are,

                                                     Tc ∆0 ϱ0       µ     ξcutoff
                                                     1.0 1.76 1.0 12.0 72.0

                                     TABLE S4. Simulation parameters for Fig. 6.

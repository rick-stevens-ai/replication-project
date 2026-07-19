<!-- extraction: pdftotext | arxiv:2510.13185 -->
The nature of polar distortions in ferroelectrics
Hong Jian Zhao,1, 2, 3 Laurent Bellaiche,4 and Yanming Ma5, 1
1

arXiv:2510.13185v1 [cond-mat.mtrl-sci] 15 Oct 2025

Key Laboratory of Material Simulation Methods and Software of Ministry of Education,
College of Physics, Jilin University, Changchun 130012, China
2
Key Laboratory of Physics and Technology for Advanced Batteries (Ministry of Education),
College of Physics, Jilin University, Changchun 130012, China
3
International Center of Future Science, Jilin University, Changchun 130012, China
4
Smart Functional Materials Center, Physics Department and Institute for Nanoscience and Engineering,
University of Arkansas, Fayetteville, Arkansas 72701, USA
5
School of Physics, Zhejiang University, Hangzhou 310058, China
Polar distortion, the collective off-center displacements of atoms, is a fingerprint of a ferroelectric
that governs its properties and functionalities. Since the 1970s, the concepts of proper, improper and
triggered ferroelectrics have been established to shed light on a diversity of polar distortion mechanisms. Such concepts assign a single nature to polar distortion and are helpful to interpret how
polar distortions occur in conventional ferroelectrics such as barium titanate. However, applying
these concepts to complex ferroelectrics (e.g., polar orthorhombic hafnia) is notoriously challenging
and can yield highly controversial arguments. Here we resolve this issue by developing a tailor-made
graph theory for clarifying the nature of polar distortions in complex ferroelectrics, which emphasizes
that polar distortions in such ferroelectrics usually exhibit multiple natures among proper, improper
and triggered characteristics. We demonstrate the robustness of our theory by working with perovsktie superlattices and polar orthorhombic hafnia (i.e., two representative cases). We successfully
identify the mixed proper-improper nature in perovsktite superlattices and reconcile the controversy on polar orthorhombic hafnia by confirming its mixed trigger-improper nature. Our work will
definitely lead to a revisitation of concepts in ferroelectric physics and provide opportunities for
discovering novel ferroelectrics and related phenomena.

Introduction. Ferroelectrics are advanced materials with
broad technological applications (e.g., energy harvesters,
sensors, actuators and non-volatile memories) [1–3]. A
defining feature of a ferroelectric is the polar distortion
— a manifestation of the collective off-center displacements of atoms [4, 5]. The polar distortion in a ferroelectric governs its properties (e.g., dielectric and piezoelectric responses, ferroelectric hysteresis, and polarization
switching dynamics) and functionalities [4–6]. Since the
1970s, the concepts of proper, improper and triggered
ferroelectrics have been established [4–8]. In proper ferroelectrics, polar distortions appear as primary order parameters (OPs) [9] and may induce secondary OPs [4–
6]. Alternatively, polar distortions occur in improper
or triggered ferroelectrics as secondary or coupled OPs
— rooted in nonpolar OPs [4–8]. These textbook concepts assume that polar distortion has a single proper,
improper or triggered feature [4–6], and succeed in elucidating the polar natures in conventional ferroelectrics
such as barium titanate. In sharp contrast, applying such
concepts to complex ferroelectrics is rather challenging
and can yield highly controversial arguments. A notorious example is the polar orthorhombic hafnia compatible
with silicon-based electronics [10–14]. As an elusive case,
this material was recognized as proper [15], improper [16–
18] or even triggered [19] ferroelectric in literature.
We resolve such an issue by developing a graph theory
tailor-made for clarifying the nature of polar distortions
in complex ferroelectrics. We emphasize that complex
ferroelectrics can exhibit multiple natures among proper,

improper and triggered characteristics. We demonstrate
the robustness of our theory by working with two
representative cases — that is, perovskite superlattices
and polar orthorhombic hafnia — both of which exhibit
elusive polar distortions. Our theory not only correctly
captures the mixed proper-improper nature in perovskite
superlattices, but also unifies the conflicting arguments
in Refs. [15–19] regarding polar orthorhombic hafnia
(confirming its mixed triggered-improper nature).
The selection of the reference phase. For a ferroelectric,
let the symmetry groups of its paraelectric and ferroelectric phases be G0 and G, respectively. The ferroelectric
phase transition is associated with the symmetry breaking from G0 to G. This is described by a subgroup chain
as G0 ⊇ G1 ⊇ · · · ⊇ G, where G1 and · · · characterize the
symmetry groups of the intermediate phases. The subgroup chains are usually not unique: G0 ⊇ G′1 ⊇ · · · ⊇ G
may serve as another subgroup chain. The description of
the ferroelectric distortion lies in the selection of a nonpolar reference phase, but this selection has arbitrariness.
For instance, G0 , G1 , G′1 , and other states may be selected as reference phases if these states are not polar.
Different choices of the reference phases may lead to
inconsistent or contradictory conclusions. To show this,
let us imagine that the G phase has a polar p and two
nonpolar (q1 , q2 ) OPs defined with respect to the G0
phase. We further assume that the ferroelectricity in the
G phase is improper and is originating from the pq1 q2
trilinear coupling. This means that the reversal of the

2
ferroelectric polarization involves the reversal of either
q1 or q2 (but not both). The transition from G0 phase
to G phase is associated with G0 ⊇ Gp1 ⊇ G(p,q1 ,q2 ) ,
G0 ⊇ Gq11 ⊇ G(p,q1 ,q2 ) , or G0 ⊇ Gq12 ⊇ G(p,q1 ,q2 )
subgroup chain — the superscript representing the
condensed OPs. By selecting Gq11 as the reference phase,
we conclude that the ferroelectric switching involves the
reversal of p and q2 OPs. However, selecting Gq12 as the
reference phase will lead to a very different conclusion,
that is, the ferroelectric switching reverses both p and
q1 . Such contradictory conclusions are due to the local
and biased analyses of ferroelectric distortion based
on low-symmetric Gq11 and Gq12 reference phases. For
this reason, we emphasize the necessity to select the
highest-symmetric G0 state as the reference phase.
This will enable a global description of ferroelectric distortions and avoid inconsistent or contradictory analyses.

propose the proper membership coefficient η as
η = (|P | ∧ |P0 |)/(|P | ∨ |P0 |),

where ∧ (∨) selects the minimum (maximum) value between |P | and |P0 |. At the probability level, a larger η
implies that P is more likely inherited from P0 .
When superimposing several nonpolar distortions on
the reference phase, the symmetry of such a phase may
be broken. If the symmetry breaking is compatible with
a polar distortion, the ferroelectric contains improper
components. In the following, we develop a graph theory that determines whether a ferroelectric contains improper components. Superimposing one or several nonpolar OPs on the reference phase results in 2n different
distortion states that are represented by the elements in
P(Q), the power set of Q given by
n
P(Q) = {Q̃ | Q̃ ⊆ Q} = ∅, {q1 }, {q2 }, · · · , {qn },
{q1 , q2 }, {q1 , q3 }, · · · {qn−1 , qn }, {q1 , q2 , q3 },
o
{q1 , q2 , q4 }, · · · , {qn−2 , qn−1 , qn }, · · · , Q ,

FIG. 1. Sketches of nonpolar hierarchy graph (a) and polar
hierarchy graph (b). The set associated with each vertex (being omitted) is indicated by arrows pointing to that vertex.
For instance, the vertexes marked by G13 and G0 have sets of
{q1 , q3 } and ∅, respectively. In panels (a) and (b), the vertexes
with yellow (gray) color share identical crystal structures as
that for G0 (G123 ); the vertexes with white color have crystal
structures that are not equivalent to each other. We further
assume that the G̃1 vertex has a polar space group, vertexes
with gray color have polar space groups, and other vertexes
have nonpolar space groups.

Proper and improper components. Our discussion is built
upon the notions of proper and improper components.
To introduce these notions, we start from a ferroelectric
with n nonpolar OPs, and such nonpolar OPs form a set
Q = {qi | i = 1, 2, · · · , n}. The ferroelectric also has a
polar distortion p and a ferroelectric polarization P . We
say that this ferroelectric contains a proper component if
superimposing p distortion on the reference phase yields
a nonzero electric polarization P0 (i.e., p being a primary
OP [20]). In the ferroelectric phase, the P0 polarization
may be suppressed by some nonpolar OPs and enhanced
by the others. Therefore, P usually differs from P0 , and
the proximity between |P0 | and |P | provides a “measurement” of the proper component. Motivated by this, we

(1)

(2)

where ∅ empty set means that no nonpolar OPs are superimposed on the reference phase, Q means that all the
nonpolar OPs are superimposed, {qi } means that only qi
is superimposed, {qi , qj } means that both qi and qj are
superimposed, and so forth. The aforementioned 2n distortion states and their relations can be well described by
our proposed nonpolar hierarchy graph. In such a graph,
there are n directed edges and 2n vertexes. The edges
and vertexes represent nonpolar distortions and nonpolar distortion states, respectively [see Eq. (2)].
For every pair of (A, B) vertexes, we draw a qi directed
edge from A to B if A ⊆ B and B − A = {qi }; otherwise, the A and B vertexes are not connected by any
edges. We term the ∅ and Q vertexes as the start and
end vertexes, respectively. Each vertex is valued via the
following procedures: (i) we create the structural distortions in the reference phase according to the vertex, (ii)
we perform first-principles structural relaxations for the
initially created crystal structure, and (iii) we assign the
vertex to the relaxed crystal structure and the resulting
space group [21]. Vertexes that have equivalent crystal
structures are colored with the same color, while vertexes
that have unique crystal structures are uncolored (i.e.,
with white color). We can deduce that the ferroelectric
contains no improper components if there are no vertexes
with polar space group. On the contrary, a {qi , qj , · · · }
vertex with a polar space group indicates that the combination of {qi , qj , · · · } nonpolar OPs yields improper polarization. Walking along the directed edges from the ∅
vertex to a vertex with polar space group yields a path
associated with an improper component (termed as “improper path”). An improper path is irreducible when it
contains only one vertex with polar space group. Otherwise, the path can be further shortened as an irreducible

3
path. Each irreducible improper path indicates a combination of nonpolar OPs — involving a minimal number
of OPs — that drives an improper component.
The interplay among polar and nonpolar OPs can be
further understood by constructing the polar hierarchy
graph as follows. First, we represent the vertexes for the
polar hierarchy graph by the {{p}∪Q̃ | Q̃ ⊆ Q} set, where
p is the polar distortion and Q = {qi | i = 1, 2, · · · , n}.
Then, the polar hierarchy graph is readily obtained by
following the rules for constructing nonpolar hierarchy
graph (see above). The comparison between nonpolar
and polar hierarchy graphs allows us to explore the nature of polar distortion in a ferroelectric. If nonpolar
hierarchy graph contains enough information, the construction of polar hierarchy graph can be omitted.
As a demonstration, we assume that a ferroelectric
has nonpolar {q1 , q2 , q3 } OPs and a polar p OP. Figure 1
schematizes its nonpolar and polar hierarchy graphs,
and these graphs deliver abundant information. First,
G0 and G1 vertexes have equivalent crystal structure
and therefore q1 is not a primary OP. Second, q1 can be
stabilized in the presence of q2 , q3 , or p (see G12 , G13 ,
and G̃1 vertexes). Third, q2 and q3 are primary OPs and
the (q2 , q3 ) combination yields an improper polarization.
Finally, p is not a primary OP and this ferroelectric
contains no proper component [see Fig. 1(b)].
Complex ferroelectrics with mixed characteristics. Following Refs. [4–8, 19, 22], we revisit the concepts of
proper, improper and triggered ferroelectrics. Ideally,
conventional ferroelectrics have the following features:
(i) Proper ferroelectric [4–6]. A material has a polar distortion as its primary OP and contains no improper components. Nonpolar distortions (if existing)
only slightly modify the primary polar OP.
(ii) Improper ferroelectric [4–6]. A material has no
polar distortion as its primary OP. The polar distortion
originates from improper components that are not associated with any secondary nonpolar OPs.
(iii) Triggered ferroelectric [7]. A material contains
neither proper nor improper components. The polar distortion is triggered by one or several nonpolar OPs.
In sharp contrast, complex ferroelectrics usually go beyond these ideal situations and showcase multiple features. Typical examples include:
(iv) Mixed proper-improper ferroelectric [4–6, 22]. A
material has both proper and improper components.
(v) Mixed proper-triggered ferroelectric [7, 8]. A material has a proper component but has no improper components. The collaborative couplings between polar and
nonpolar OPs trigger the simultaneous occurrence of polar distortion and nonpolar OP(s).
(vi) Mixed triggered-improper ferroelectric [6, 7, 19]. A
material has no proper component. The polar distortion
is triggered by improper components, and the nonpolar
OPs associated with these improper components are not

FIG. 2. Ferroelectricity in the ABO3 /A′ BO3 perovskite superlattice. Panels (a) and (b) sketch the nonpolar M 2+ and
M 5− distortions, where gray arrows represent ionic motions.
The A, A′ , B and O ions are represented by purple, pink, cyan
and orange spheres, respectively. In panel (b), the motions
of A, A′ and B ions (being very tiny) are not shown. Panel
(c) is the nonpolar hierarchy graph for LaGaO3 /YGaO3 and
SrTiO3 /CaTiO3 superlattices. Panel (d) shows the strain dependent polarizations. The strain for LaGaO3 /YGaO3 and
SrTiO3 /CaTiO3 is defined with respect to a0 = 5.44 Å and
a0 = 5.46 Å, respectively.

all primary OPs.
In complex ferroelectrics, boundaries between proper,
improper and triggered mechanisms can be very fuzzy.
Regarding this, our proposed η coefficient [see Eq. (1)]
provides a “measurement” of the proper degree of the
ferroelectricity. The nature of polar distortion in a
ferroelectric with triggered features can be explored by
comparing its polar and nonpolar hierarchy graphs. In
the following sections, we shall demonstrate the applications of our theory to several complex ferroelectrics.
Example I: Ferroelectricity in perovskite superlattices.
Our first example is the short period ABO3 /A′ BO3 perovskite superlattices. Figures 2(a)–(b) sketch two primary nonpolar OPs in ABO3 /A′ BO3 , namely, M 2+ and
M 5− distortions. Such two OPs are defined with respect
to the P 4/mmm reference phase. The (M 2+ , M 5− ) combination yields improper polarization, and this is termed
as “hybrid improper ferroelectricity” [23–28]. A typical
hybrid improper ferroelectric is the LaGaO3 /YGaO3 superlattice (space group being P 21 am) that is predicted

4

FIG. 3. Ferroelectricity in orthorhombic HfO2 . Panels (a)—(d) sketch four nonpolar distortion modes in HfO2 , where gray
arrows represent ionic motions. The Hf and O ions are represented by green and yellow spheres, respectively. Panel (e) is the
phase transition graph for HfO2 . Note that the 42 screw axis in P 42 /nmc is along the x direction.

by Ref. [26]. Figure 2(c) shows the nonpolar hierarchy graph for LaGaO3 /YGaO3 , where the start and end
vertexes represent reference and ferroelectric phases, respectively. We identify two shortest improper paths between the start and end vertexes, and both paths involve
the combination of M 2+ and M 5− nonpolar OPs. This
confirms that LaGaO3 /YGaO3 indeed contains improper
component, which is consistent with Ref. [26]. The comparison between P 21 am and P 4/mmm phases yields a
Γ5− polar distortion. This Γ5− distortion is compatible
with the P 4/mmm reference phase, resulting in an electric polarization of P0 = 51.3 µC/cm2 . The ferroelectric
P 21 am phase has a polarization of P = 10.9 µC/cm2 .
According to Eq. (1), the proper membership η coefficient is ∼ 21% and this implies that the ferroelectricity
in LaGaO3 /YGaO3 is largely improper.
We move on to examine the ferroelectric nature in the
SrTiO3 /CaTiO3 superlattice which contains an active
ion for proper ferroelectricity (i.e., Ti4+ ). The nonpolar
OPs and nonpolar hierarchy graph for SrTiO3 /CaTiO3
resemble those for LaGaO3 /YGaO3 [see Figs. 2(a)–(c)].
Similar to LaGaO3 /YGaO3 , SrTiO3 /CaTiO3 has an
improper component. The P0 and P polarization values
for SrTiO3 /CaTiO3 are 39.6 and 22.2 µC/cm2 , respectively. The η membership coefficient for SrTiO3 /CaTiO3
reaches ∼ 56%, and such a value implies that the ferroelectricity in SrTiO3 /CaTiO3 is proper by a slight
majority. Figure 2(d) shows the P and P0 polarizations for LaGaO3 /YGaO3 and SrTiO3 /CaTiO3 films
that depends on the biaxial strain (in-plane lattice
parameter) [29]. In LaGaO3 /YGaO3 , P0 is obviously
enhanced by increasing the in-plane lattice parameter,
while P remains nearly unchanged. This implies that
the P0 polarization is significantly suppressed by M 2+

and/or M 5− OPs, and the polarization in P 21 am
LaGaO3 /YGaO3 is predominantly contributed by the
(M 2+ , M 5− ) combination. As for SrTiO3 /CaTiO3 , both
P0 and P are significantly enhanced by increasing the
in-plane lattice parameter. The similar trends for P0 and
P suggests that P in P 21 am SrTiO3 /CaTiO3 is mostly
inherited from P0 . In Fig. 5 of the End Matter [30], we
show the η coefficients for these two materials as functions of strains. We find that strain only slightly affects
the proper component in LaGaO3 /YGaO3 but significantly increases such a component in SrTiO3 /CaTiO3 .
Example II: Ferroelectricity in polar orthorhombic hafnia. The next example is the orthorhombic HfO2 with
a P ca21 space group. References [15–19] select F m3̄m,
P 42 /nmc or P bcn phase as its reference phase. We shall
show that selecting the F m3̄m reference phase (as is done
in Refs. [16, 17, 19]) can not only interpret the results in
Refs. [15, 18] but also provide more deep understandings
of the ferroelectric nature in P ca21 HfO2 . With respect
to F m3̄m phase, we identify four nonpolar OPs in P ca21
HfO2 and demonstrate them in Figs. 3(a)–(d). Compared
with the F m3̄m reference phase, P ca21 HfO2 contains a
Γ4− polar distortion. Such a distortion is not compatible with the F m3̄m phase (i.e., P0 = 0). The nonpolar
hierarchy graph of HfO2 is shown in Fig. 3(e). The end
vertex is associated with the polar P ca21 phase which
implies that HfO2 contains improper components. From
the graph, we identify the irreducible improper paths
that involve (X 5+ , X 2− ), (X 5+ , X 3− ), and (X 5+ , X 5− )
OPs. Among the four nonpolar distortions, only the X 2−
mode is the primary OP, while the other three are not.
The role of the X 2− OP is very special in P ca21 HfO2 .
Superimposing this OP on the F m3̄m phase yields the

5

FIG. 4. The ferroelectricity in orthorhombic HfO2 driven by the X 5+ distortion. Panels (a), (b), and (c) sketch the Xx5+ ,
Xy5+ , and Xz5+ modes, respectively. The X 5+ mode, the compass and the axis labels can be found in Fig. 3. Panel (d) shows
the polarization of HfO2 as a function of the Xy5+ distortion (i.e., QXy5+ ). See Methods for the computational details.

P 42 /nmc phase. Our phonon calculation confirms that
the P 42 /nmc phase has no imaginary phonon modes,
which suggests the triggered ferroelectric nature (coinciding with Ref. [19]). We further find that removing
X 5+ edges breaks the connectivity between the start and
end vertexes. Hence, P ca21 HfO2 is a mixed triggeredimproper ferroelectric, and the (X 2− , X 5+ ) combination
is critical for creating the ferroelectric polarization.
The nonpolar X 5+ mode in Fig. 3(d) involves noncollinear motions of O ions. Such motions can be further
decomposed into Xx5+ , Xy5+ and Xz5+ collinear modes
[see Figs. 4(a)–(c)]. To compare with Refs. [15, 18], we
construct a more complicated nonpolar hierarchy graph
by working with X 2− , X 5− , Xx5+ , Xy5+ and Xz5+ nonpolar OPs (see Fig. 6 of the End Matter). Using P 42 /nmc
phase as a reference phase, Ref. [18] argues that the
polarization in P ca21 HfO2 arises from the combination
of Y4− and Y2+ OPs which, in essence, correspond to our
Xx5+ and Xz5+ OPs, respectively. As shown in Fig. 6, the
(X 2− , Xx5+ , Xz5+ ) combination yields the polar P ca21
phase. Recalling that the P 42 /nmc phase is created by
condensing the X 2− mode, the (Xx5+ , Xz5+ ) combination
yields an improper component in the P 42 /nmc phase
— coinciding with Ref. [18]. Different from Ref. [18],
Ref. [15] selects the P can state as a reference phase, and
conclude that the polarization in P ca21 HfO2 is proper.
Our analysis suggests that condensations of X 2− , X 5−
and Xz5+ OPs result in the P can state. Taking the
P can phase as a reference, the polarization in P ca21
HfO2 is associated with Xy5+ or Xx5+ nonpolar OP. As a
illustration, we show that Xy5+ can induce polarization
in the P can state [see Fig. 4(d)]. To summarize this
paragraph, our theory enables a global description of
the ferroelectricity in P ca21 HfO2 , and this unifies the
arguments in Refs. [15–19].
Perspective. We explicitly establish the concepts of complex ferroelectrics with multiple natures among proper,
improper and triggered characteristics. The necessity for
introducing such concepts is justified by that complex

ferroelectrics can yield exotic phenomena that are unlikely to occur in conventional ferroelectrics. Very recently, Ref. [22] predicts the coexisted proper and improper characteristics and the resultant ferrielectric-like
unusual hysteresis in CsNbW2 O9 . Another example is
the unusual hysteresis feature arisen in P ca21 HfO2 with
mixed triggered-improper characteristics [19].
The development of Landau theory is the textbook
approach for understanding the polar distortion in ferroelectrics [4, 5]. However, due to incomplete and biased
analyses of energetic couplings, such an approach may
lead to conflicting pictures for complex ferroelectrics. In
this regard, our graph theory provides a straightforward
way for clarifying the polar distortion natures in complex
ferroelectrics. This will definitely deepen our knowledge
on ferroelectric physics and benefit the discovery of novel
ferroelectrics and related phenomena.
Acknowledgements. We thank the support from the
National Natural Science Foundation of China with
Grants No. 12274174, No. 52288102, No. 52090024, and
No. 12034009. L.B. acknowledges the Vannevar Bush
Faculty Fellowship (VBFF) grant No. N00014-20-12834 from the Department of Defense and award No.
DMR-1906383 from the National Science Foundation
AMASE-i Program (MonArk NSF Quantum Foundry).

[1] L. W. Martin and A. M. Rappe, Nat. Rev. Mater. 2,
16087 (2016).
[2] F. Li, B. Wang, X. Gao, D. Damjanovic, L.-Q. Chen, and
S. Zhang, Science 389 (2025).
[3] U. Schroeder, M. H. Park, T. Mikolajick, and C. S.
Hwang, Nat. Rev. Mater. 7, 653–669 (2022).
[4] B. A. Strukov and A. P. Levanyuk, Ferroelectric Phenomena in Crystals (Springer Berlin Heidelberg, 1998).
[5] R. Blink and B. Zeks, Soft Modes in Ferroelectrics
and Antiferroelectrics (Amsterdam: North-Holland, New
York: American Elsevier, 1974).

6
[6] A. P. Levanyuk and D. G. Sannikov, Sov. Phys. Usp. 17,
199–214 (1974).
[7] J. Holakovský, Phys. Status Solidi B 56, 615–619 (1973).
[8] I. A. Kornev and L. Bellaiche, Phys. Rev. B 79, 100105
(2009).
[9] In pseudoproper ferroelectrics, the polar distortion is
driven by another distortion, where both distortions have
identical symmetry [4]. Because of this, we can merge
these distortions as an effective polar distortion and treat
pseudoproper ferroelectrics as proper ferroelectrics.
[10] B. Noheda, P. Nukala, and M. Acuautla, Nat. Mater. 22,
562–569 (2023).
[11] U. Schroeder, M. H. Park, T. Mikolajick, and C. S.
Hwang, Nat. Rev. Mater. 7, 653–669 (2022).
[12] S. Kang, W.-S. Jang, A. N. Morozovska, O. Kwon, Y. Jin,
Y.-H. Kim, H. Bae, C. Wang, S.-H. Yang, A. Belianinov,
S. Randolph, E. A. Eliseev, L. Collins, Y. Park, S. Jo,
M.-H. Jung, K.-J. Go, H. W. Cho, S.-Y. Choi, J. H.
Jang, S. Kim, H. Y. Jeong, J. Lee, O. S. Ovchinnikova,
J. Heo, S. V. Kalinin, Y.-M. Kim, and Y. Kim, Science
376, 731–738 (2022).
[13] J. A. Eastman, Nat. Mater. 21, 845–847 (2022).
[14] T. S. Böscke, J. Müller, D. Bräuhaus, U. Schröder, and
U. Böttger, Appl. Phys. Lett. 99, 102903 (2011).
[15] A. Raeliarijaona and R. E. Cohen, Phys. Rev. B 108,
094109 (2023).
[16] L. Yu, H. J. Zhao, P. Chen, L. Bellaiche, and Y. Ma, Nat.
Commun. 14, 8127 (2023).
[17] H.-J. Lee, M. Lee, K. Lee, J. Jo, H. Yang, Y. Kim,
S. C. Chae, U. Waghmare, and J. H. Lee, Science 369,
1343–1347 (2020).
[18] F. Delodovici, P. Barone, and S. Picozzi, Phys. Rev.
Mater. 5, 064405 (2021).
[19] S. Jung and T. Birol, arXiv:2502.08633v2 (2025).
[20] Our work focuses on the ground state structural properties of ferroelectrics. The primary and non-primary OPs
are referred to as stable and unstable modes, respectively.
[21] We may employ the graph-theoretical approach to understand the magnetically induced ferroelectricity in type-II
multiferroics. In such cases, we should include magnetic
order parameters and work with magnetic space groups.
[22] C. A. M. Scott, F. D. Morrison, and N. C. Bristowe,
arXiv:arXiv:2510.02604 (2025).
[23] E. Bousquet, M. Dawber, N. Stucki, C. Lichtensteiger,
P. Hermet, S. Gariglio, J.-M. Triscone, and P. Ghosez,
Nature 452, 732–736 (2008).
[24] H. J. Zhao, J. Íñiguez, W. Ren, X. M. Chen, and L. Bel-

laiche, Phys. Rev. B 89, 174101 (2014).
[25] N. A. Benedek and C. J. Fennie, Phys. Rev. Lett. 106,
107204 (2011).
[26] J. M. Rondinelli and C. J. Fennie, Adv. Mater. 24,
1961–1968 (2012).
[27] A. T. Mulder, N. A. Benedek, J. M. Rondinelli, and C. J.
Fennie, Adv. Funct. Mater. 23, 4810–4820 (2013).
[28] Z. Zanolli, J. C. Wojdel, J. Íñiguez, and P. Ghosez, Phys.
Rev. B 88, 060102 (2013).
[29] To mimic a film on a cubic substrate, we set its in-plane
lattice parameters equal to each other. In its bulk counterpart, such two lattice parameters may be different. In
our cases, LaGaO3 /YGaO3 or SrTiO3 /CaTiO3 film with
zero strain do not exactly correspond to LaGaO3 /YGaO3
or SrTiO3 /CaTiO3 bulk material.
[30] The End Matter section includes our methods and two
supplementary figures (citing Refs. [31–44]).
[31] G. Kresse and J. Furthmüller, Phys. Rev. B 54, 11169
(1996).
[32] G. Kresse and D. Joubert, Phys. Rev. B 59, 1758 (1999).
[33] J. P. Perdew, A. Ruzsinszky, G. I. Csonka, O. A. Vydrov,
G. E. Scuseria, L. A. Constantin, X. Zhou, and K. Burke,
Phys. Rev. Lett. 100, 136406 (2008).
[34] P. E. Blöchl, Phys. Rev. B 50, 17953 (1994).
[35] R. D. King-Smith and D. Vanderbilt, Phys. Rev. B 47,
1651 (1993).
[36] G. Henkelman, B. P. Uberuaga, and H. Jónsson, J. Chem.
Phys. 113, 9901 (2000).
[37] G. Henkelman and H. Jónsson, J. Chem. Phys. 113, 9978
(2000).
[38] C. Capillas, E. S. Tasci, G. de la Flor, D. Orobengoa,
J. M. Perez-Mato, and M. I. Aroyo, Z. Kristallogr 226,
186–196 (2011).
[39] D. Orobengoa, C. Capillas, M. I. Aroyo, and J. M. PerezMato, J. Appl. Crystallogr. 42, 820–833 (2009).
[40] J. M. Perez-Mato, D. Orobengoa, and M. I. Aroyo, Acta
Cryst. A 66, 558–590 (2010).
[41] H. T. Stokes, D. M. Hatch, and B. J. Campbell, FINDSYM, ISOTROPY Software Suite, https://iso.byu.
edu.
[42] H. T. Stokes and D. M. Hatch, J. Appl. Crystallogr. 38,
237 (2005).
[43] K. Momma and F. Izumi, J. Appl. Crystallogr. 44, 1272
(2011).
[44] J. D. Hunter, Comput. Sci. Eng. 9, 90 (2007).

End Matter

Methods. We use the VASP [31, 32] code and employ the PBEsol [33] functional (PAW [34] potentials) to perform our
first-principles numerical simulations. We set the kinetic energy cutoff as 600 eV, and solve the following electronic
configurations: (5s, 5p, 5d, 6s) for La, (4s, 4p, 4d, 5s) for Y, (3d, 4s, 4p) for Ga, (4s, 4p, 5s) for Sr, (3s, 3p, 4s) for Ca,
(3s, 3p, 3d, 4s) for Ti, (5s, 5p, 5d, 6s) for Hf, and (2s, 2p) for O. We use a 8 × 8 × 6 k-point mesh for LaGaO3 /YGaO3
and SrTiO3 /CaTiO3 and a 10 × 10 × 10 k-point mesh for HfO2 ; such meshes correspond to the lattices demonstrated
in Figs. 2(a) and 3(a). We perform the structural relaxations by setting the force convergence criterion as 0.001 eV/Å.
When mimicking a strained film on a cubic substrate, we fix the in-plane lattice vectors of the film to (a, 0, 0) and
(0, a, 0) — a being adjusted according to the substrate lattice constant. Then, we relax the out-of-plane lattice vector
together with the atomic positions. We compute the electric polarization values for LaGaO3 /YGaO3 , SrTiO3 /CaTiO3 ,
and HfO2 by the Berry phase method [35] with the help of the VTST tookit [36, 37]. We carry out our symmetry

7
analysis by the PSEUDO [38], AMPLIMODES [39, 40] and FINDSYM [41, 42] tookits, visualize our crystal structures
and atomic motions by the VESTA [43] code, and prepare our plots by the Matplotlib library [44].
When calculating Fig. 4(d), the amplitude of the Xx5+ mode is fixed to 0, amplitudes of X 2− and X 5− modes are
fixed to their values in bulk P ca21 HfO2 , and the amplitude of the Xy5+ mode is fixed to −100%, −50%, 0%, 50%,
or 100% of that in bulk P ca21 HfO2 ; furthermore, an initial Xz5+ distortion is given according to its amplitude in
bulk P ca21 HfO2 , and Γ4− , X 3− and Xz5+ modes are free to relax. Such calculations are achieved by the “selective
dynamics” strategy (see https://www.vasp.at/wiki/index.php/POSCAR) by fixing the fractional coordinates of
several ions and relaxing the other degrees of freedom including the lattice vectors. Therefore, the fixed amplitudes
are performed at the level of fixed ionic fractional coordinates.
Two supplementary figures. We also provide two supplementary figures to support our discussion in the Main Text.
Figures 5 shows the η membership coefficients for strained LaGaO3 /YGaO3 and SrTiO3 /CaTiO3 , while Figure 6
demonstrates a nonpolar hierarchy graph for P ca21 HfO2 constructed with respect to five nonpolar OPs.

100

LYGO
SCTO

80

(%)

60
40
20
0

2

1

0
Strain (%)

1

2

FIG. 5. The strain-dependent membership coefficients for LaGaO3 /YGaO3 and SrTiO3 /CaTiO3 superlattices.

8

FIG. 6. The nonpolar hierarchy graph for HfO2 constructed with respect to X 2− , X 5− , Xx5+ , Xy5+ , and Xz5+ distortion modes.
Note that the 42 screw axis in P 42 /nmc is along the x direction. Furthermore, the P can is the non-standard setting for the
P bcn space group.


Strain-induced nonrelativistic altermagnetic spin splitting effect
Wancheng Zhang ,1, 2 Mingkun Zheng,1, 2 Yong Liu,3 Zhenhua Zhang ,1, 2, ∗ Rui Xiong ,3, † and Zhihong Lu

1, 2, ‡

1 State Key Laboratory of Advanced Refractories, Wuhan University of Science and Technology, Wuhan 430081, People’s Republic of China
2 School of Materials and Metallurgy, Wuhan University of Science and Technology, Wuhan 430081, People’s Republic of China
3 Key Laboratory of Artificial Micro- and Nano-structures of Ministry of Education,

arXiv:2503.17916v4 [cond-mat.mtrl-sci] 16 Jul 2025

School of Physics and Technology, Wuhan University, Wuhan 430072, People’s Republic of China
Recent studies reveal that T -odd spin currents generated via the nonrelativistic altermagnetic spin splitting
effect (ASSE) exhibit significant potential for spintronics applications, with both computational and experimental
validations. Addressing the scarcity of conductive altermagnets, we propose strain engineering as a reliable
method for inducing altermagnetism. Focusing on rutile-structured OsO2 , first-principles calculations show
that minor equibiaxial tensile strain (Ets =3%) induces nonmagnetic-to-altermagnetic transitions, achieving an
ASSE-driven spin-charge conversion ratio (𝜃 AS ) of ∼7%—far surpassing conventional spin Hall angles (𝜃 IS ).
Calculations reveal that substantial 𝜃 AS persists even in the absence of spin-orbit coupling, with its magnitude
positively correlating to nonrelativistic spin splitting magnitude, which further confirms the strain-induced
ASSE’s nonrelativistic origin. Further investigation reveals that RuO2 exhibits analogous phenomena, which
may resolve recent controversies regarding its magnetic properties. Our research opens new simple pathways for
developing next-generation altermagnetic spintronic devices.
Published in Physical Review B: Phys. Rev. B 112, 024415 (2025)
I.

INTRODUCTION

Altermagnetism, recently established as the third fundamental class of magnetism alongside ferromagnetism and antiferromagnetism, exhibits a unique duality: vanishing net magnetization in real space (like antiferromagnetism) combined
with broken time-reversal symmetry (T ) in reciprocal space
(akin to ferromagnetism). Unlike conventional antiferromagnets where opposite spin sublattices are linked by translation
or inversion symmetry, altermagnets feature sublattices connected via rotational symmetry operations (proper/improper,
symmorphic/non-symmorphic) [1–4]. This distinct symmetry landscape generates a nonrelativistic spin-splitting effect
(analogous to even-parity 𝑑-, 𝑔-, or 𝑖-wave symmetry) with
momentum-dependent alternating spin patterns, enabling phenomena such as the altermagnetic spin-splitting effect (ASSE),
which generate a transverse pure spin current when a charge
current flows along specific crystallographic directions-even
in the absence of relativistic spin-orbit coupling (SOC) [5–
7]. These spin currents arise from spin-momentum locking in
the electronic structure, providing a dissipationless pathway
for spin-charge interconversion, which is critical for field-free
magnetization switching in magnetic random-access memory
(MRAM) [8, 9].
At present, most identified altermagnetic materials are semiconductors or insulators, such as MnTe [10–12] and recently
proposed two-dimensional altermagnetic systems fabricated
by stacking and twisting [13–15]. Metallic altermagnets remain scarce, with 𝑑-wave RuO2 [5–7, 16–20] and 𝑔-wave
CrSb [21–23] being prominent examples. Moreover, the entire
spin conductivity tensors of the 2 6/2 𝑚 2 𝑚 1 𝑚 spin Laue group
with 𝑔-wave symmetry are forced to vanish. In this scenario,

∗ Contact author:zzhua@wust.edu.cn

† Contact author:xiongrui@whu.edu.cn
‡ Contact author:zludavid@live.com

spin current generation requires the introduction of shear strain
in the 𝑥𝑦-plane to reconfigure its spin-momentum pattern into
𝑑-wave symmetry [24]. Although RuO2 has been proposed
as a prototypical 𝑑-wave altermagnet, experimental validation remains contentious: the angle resolved photoemission
spectroscopy (ARPES) and spin-resolved ARPES (SARPES)
studies report no detectable momentum-dependent spin splitting [19], whereas magnetic circular dichroism (MCD) measurement unambiguously demonstrates T -symmetry breaking in its band structure [20]. The latest muon spin relaxation/rotation (𝜇SR) studies even point to the nonmagnetism
of RuO2 [25, 26]. This discrepancy underscores the need for alternative material platforms with unambiguous altermagnetic
signatures. Here, we propose a strategy for designing altermagnetic materials: inducing altermagnetism via strain engineering in material systems with altermagnetic crystal symmetry.
In this work, we systematically investigate the strain-induced
ASSE in bulk OsO2 using ab initio calculations. Bulk OsO2
single crystals exhibit nonmagnetic metallic behavior with a
room-temperature resistivity of ∼ 6 × 10−5 Ω · cm [27, 28],
while the monolayer 1𝑇 [29] and 1𝑇 ′ [30] phases of OsO2
are calculated to be ferromagnetic metal and nonmagnetic
semiconductor, respectively. We propose equibiaxial tensile
strain Ets as an effective and easily achievable method to induce altermagnetism in bulk OsO2 . Our calculations reveal
a strain-dependent alternating Fermi surface, which becomes
increasingly pronounced with increasing Ets . In the absence
of Hubbard 𝑈 correction, this alternating pattern is observed
at the 𝑘 𝑧 = 𝜋/2𝑐 plane and disappears when Ets reaches 6%.
Using maximally localized Wannier functions in conjunction
with linear response theory and the Kubo formula (detailed in
Sec. II), we calculate the ASSE-induced T -odd spin conductivity 𝜎𝑥𝑧,odd
and spin-charge conversion ratio 𝜃 AS . Enhancement
𝑦
of both the nonrelativistic altermagnetic spin-splitting conductivity (ASSC) and 𝜃 AS with an increase in Ets is observed.
These values are found to be significantly larger than those of

2
the conventional SOC-dependent T -even intrinsic spin Hall
conductivity (ISHC) 𝜎𝑥𝑧 𝑦 and its associated spin-charge conversion ratio (i.e., spin Hall angle) 𝜃 IS .
Our study establishes a feasible method for strain-induced
altermagnetism, and identifies OsO2 as a potential altermagnet
and viable platform for field-free switching of perpendicular
magnetization in MRAM devices. The ASSE-generated spin
currents circumvent the limitations of relativistic conventional
spin Hall effect (CSHE) mechanisms, offering enhanced efficiency and scalability compared to conventional spin-orbit
torque (SOT) mechanisms. By bridging the gap between altermagnetic theory and functional material design, this work
opens new avenues for materials exhibiting altermagnetic crystal symmetry in next-generation spintronics.
II.

METHODOLOGY

Our first-principles calculations are implemented in the Vienna 𝑎𝑏 𝑖𝑛𝑖𝑡𝑖𝑜 Simulation Package (vasp) following the density functional theory [31–33]. Projected augmented-wave
pseudopotentials are utilized to describe the ion-electron interaction, while Perdew-Burke-Ernzerhof (PBE) and the generalized gradient approximation (GGA) are adopted as the
exchange-correlation potentials [34, 35]. Besides, the cutoff
energy of the plane-wave basis is set to 520 eV. In the process

𝛾,odd

𝜎𝛼𝛽

=−

𝑒ℏ
𝜋

∫

of structure optimization, the convergence criteria of energy
and residual force are set to 1×10−8 eV and 0.01 eV/Å, respectively. During structural optimization, the Brillouin zone (BZ)
is sampled using a Γ-centered 7 × 7 × 11 Monkhorst-pack 𝑘
mesh. In self-consistent field (SCF) calculations, a 9 × 9 × 13
Monkhorst-pack 𝑘 mesh is employed to obtain an accurate
electronic structure. In this work, maximally localized Wannier functions and the Kubo formula are utilized to calculate
the ISHC [36, 37]. The tight-binding models are calculated
by wannier90 [38]. To handle the rapid variation of the spin
Berry curvature (SBC), the BZ integration is conducted using
a dense 𝑘 mesh with 500 × 500.
Since the response of metals to electric fields can be well
described by the linear response theory, the T -odd spin conductivity and spin-charge conversion ratio within the linear response theory are evaluated using the Kubo formula in the approximation of the constant scattering rate 𝚪, as implemented
in the wannier-linear-response code [5, 6, 39]. In this constant 𝚪 approximation, it is assumed that the only effect of disorder is a constant band broadening, which modifies Green’s
functions of the perfect periodic system in the following approach: 𝐺 𝑅 (𝜀) = 1/(𝜀 − 𝐻ˆ + 𝑖0+) → 1/(𝜀 − 𝐻ˆ + 𝑖𝚪), where
𝐻ˆ denotes the Hamiltonian, 𝜀 denotes energy, and 𝐺 𝑅 is the
retarded Green’s function [40]. The Kubo formula within the
constant 𝚪 approximation can be split into the T -odd contribution [41]

𝐴|𝜓 𝑚k ⟩⟨𝜓 𝑚k | 𝑣ˆ 𝛽 |𝜓 𝑛k ⟩)
𝑑 3 k ∑︁ 𝚪2 Re(⟨𝜓 𝑛k | ˆ
,
3
(2𝜋) 𝑛,𝑚 [(𝐸 𝐹 − 𝜀 𝑛k ) 2 + 𝚪2 ] [(𝐸 𝐹 − 𝜀 𝑚k ) 2 + 𝚪2 ]

(1)

and the T -even contribution given in the 𝚪 → 0 limit by [42]

𝑛 occ

𝛾,even
𝜎𝛼𝛽 = −2𝑒ℏ

∫

unocc
ˆ 𝑚k ⟩⟨𝜓 𝑚k | 𝑣ˆ 𝛽 |𝜓 𝑛k ⟩)
Im(⟨𝜓 𝑛k | 𝐴|𝜓
𝑑 3 k 𝑚∑︁
,
(2𝜋) 3 𝑛≠𝑚
(𝜀 𝑛k − 𝜀 𝑚k ) 2

where 𝑒 represents the (positive) elementary charge; 𝛼, 𝛽, 𝛾 =
𝑥, 𝑦, 𝑧 represent the directions of spin current, electric field,
and spin polarization, respectively; k stands for the Bloch
wave vector; 𝑛 and 𝑚 are the band indices; 𝜓 𝑛k , 𝜀 𝑛k denote
the Bloch function for band 𝑛 at k and the corresponding band
energy, respectively; 𝐸 𝐹 denotes the Fermi energy, and 𝑣ˆ 𝛽 is
the velocity operator. In Eq. (2), the sum is restricted to 𝑚,
𝑛 such that 𝑛 is occupied and 𝑚 is unoccupied. Eqs. (1), (2)
𝛾
can describe the spin conductivity by setting operator 𝐴ˆ = 𝑗ˆ𝛼 ,
𝛾
1
where 𝑗ˆ𝛼 = 2 { 𝑠ˆ𝛾 ,𝑣ˆ 𝛼 } is the spin current operator and 𝑠ˆ𝛾 =
ℏ
𝜎𝛾 is the spin operator. Eq. (1) can be further adjusted to
2ˆ
calculate the charge conductivity by simply setting the operator
𝐴ˆ = −𝑒 𝑣ˆ 𝛼 , while changing the left side of the equation to
𝜎𝛼𝛽 [39, 41, 43]. A constant 𝚪 that determines the broadening

(2)

magnitude is used, which can be estimated by comparing the
calculated conductivity with the experimental conductivity.
Time reversal is an antiunitary operator that will transform the
ˆ 𝑛k ⟩ → ⟨𝜓 𝑛k |T 𝐴T
ˆ |𝜓 𝑛k ⟩ ∗ [44], so
matrix elements as ⟨𝜓 𝑛k | 𝐴|𝜓
Eqs. (1) and (2) will transform differently under time reversal.
It should be noted that the transformation under time reversal
is the opposite for conductivity and spin conductivity. This
is because the spin current operator contains an additional
spin operator that is odd under time reversal. Thus, for spin
conductivity, Eq. (1) is odd under time reversal, while Eq. (2)
is even [39].
For the convenience of SBC’s calculation, Eq. (2) can be
further rewritten into the form of Eq. (3), which is also known
as the Kubo-Greenwood formula for the direct current (DC)

3
ISHC of a crystal in the independent-particle approximation,

𝛾

𝜎𝛼𝛽 =

and it is written as [36, 37]

∑︁ 2 Im[⟨𝜓 𝑛k | 𝑗ˆ𝛼𝛾 |𝜓 𝑚k ⟩⟨𝜓 𝑚k | − 𝑒 𝑣ˆ 𝛽 |𝜓 𝑛k ⟩]
ℏ ∑︁ ∑︁
,
𝑓 𝑛k
V 𝑐 Nk
(𝜀 𝑛k − 𝜀 𝑚k ) 2
𝑛
𝑚≠𝑛

(3)

k

where V𝑐 represents the cell volume, Nk represents the number
of 𝑘-points used for sampling the Brillouin zone, and 𝑓𝑛k =
𝑓 (𝜀 𝑛k ) represents the Fermi-Dirac distribution function.
Eq. (3) can be further divided into the band-projected Berry
curvature-like term
𝛾

Ω𝑛, 𝛼𝛽 (k) = ℏ2

∑︁ −2Im[⟨𝜓 𝑛k 1{ ˆ𝜎𝛾 , 𝑣ˆ 𝛼 } 𝜓 𝑚k ⟩⟨𝜓 𝑚k 𝑣ˆ 𝛽 𝜓 𝑛k ⟩]
2

(𝜀 𝑛k − 𝜀 𝑚k ) 2

𝑚≠𝑛

(a)

(b)
Strain
R
X⋆

,

X

z

kx

(4)
and the 𝑘-resolved term that sums over occupied bands
∑︁
𝛾
𝛾
Ω 𝛼𝛽 (k) =
𝑓𝑛k Ω𝑛, 𝛼𝛽 (k),

x

and the SHC can be represented as
𝛾

𝑒 1 ∑︁ 𝛾
Ω 𝛼𝛽 (k).
2 V𝑐 Nk

(6)

k

𝛾

𝛾

The unit of Ω𝑛, 𝛼𝛽 (k) is length2 , and the unit of 𝜎𝛼𝛽 is
(ℏ/𝑒)S/length.

III.
A.

y

Os:

Z
A
Γ⋆

M⋆'

M⋆

Γ
M

ky

O:

(5)

𝑛

𝜎𝛼𝛽 =

kz

DISCUSSION

Crystal and electronic band structure of OsO2

OsO2 crystallizes in the well-known rutile structure [45, 46]
[as shown in Fig. 1(a)], with experimental lattice constants of
𝑎 ≈ 4.50 Å and 𝑐 ≈ 3.18 Å [27, 47, 48]. This is close to our
structural optimization results (𝑎 = 4.522 Å and 𝑐 = 3.215 Å)
without considering strain. The results from Ref. [49] demonstrate that the DFT calculations (partial density of states) of
OsO2 without considering the Hubbard 𝑈 correction agree
well with the experiment (high-resolution valence band spectra). Therefore, our discussion in the main text focuses mainly
on the 𝑈 = 0 case. Simultaneously, we address the scenario
with on-site Coulomb interaction in Appendix. Unlike RuO2 ,
where experimental data support the selection of 𝑈 values,
current research lacks experimental studies on the magnetism
of OsO2 . Consequently, we determined 𝑈 = 1.13 eV via the
linear response approach [50], as shown in Fig. A1. Notably,
at this 𝑈 value, OsO2 remains non-magnetic. Additionally, we
also examined the evolution of magnetism in OsO2 under different 𝑈 values (see Table S1 in Supplemental Material [51]).
Notably, when the Coulomb interaction term 𝑈 ⩾ 1.5 eV,
OsO2 exhibits more pronounced altermagnetism compared to
the strain-induced effects observed in the absence of 𝑈. For
the sake of rigor, we selected 𝑈 = 2.0 eV to simulate the scenario where OsO2 intrinsically possesses altermagnetism, and

FIG. 1. (a) The crystal structure of bulk rutile OsO2 . The red
arrow indicates the direction of equibiaxial tensile strain Ets ; the red
and blue spheres represent Os atoms with spin-up and spin-down
states respectively, and the gray spheres represent oxygen atoms. (b)
The schematic diagram of OsO2 ’s three-dimensional Brillouin zone
(BZ), with high-symmetry points indicated by red dots. The blue
cross-section indicates the 𝑘 𝑧 = 𝜋/2𝑐 plane where the alternating
pattern occurs.

we examined strain effects on the ASSE-driven spin-charge
conversion ratio (𝜃 AS ) under this condition (Table S2 [51]).
This comprehensive approach enables systematic investigation of strain effects on OsO2 , whose magnetic ground state is
experimentally undetermined.
When the on-site Coulomb interaction was not taken into
account, we conducted tests on equibiaxial strain (𝑥𝑦 plane) of
OsO2 at intervals of 1% within the range from −6% to +6%.
We found that only when the strain is greater than 2% (i.e.,
equibiaxial tensile strain Ets ), does OsO2 exhibit relatively
obvious altermagnetism. We also noticed that when Ets is
within the range of 2% ∼ 5%, its magnetism is enhanced as
Ets increases. However, when Ets reaches 6%, its magnetism
instead weakens. Since equibiaxial compressive strain cannot
induce magnetism in OsO2 , this work only considers the case
of equibiaxial tensile strain (Ets ). We list the changes of the
lattice constants of OsO2 , the magnetic moment of Os atoms,
and the maximum splitting in the bands of OsO2 near the Fermi
level with Ets ranging from 0% to 6% in Table I.
The electronic band structures and density of states (DOS)
of OsO2 under different Ets without SOC are shown in
Fig. S1 [51]. The metallicity remains unchanged with the
variation of Ets from 1% to 6%. When Ets reaches 2%, a subtle
spin splitting can be observed. As Ets increases to 6%, a tendency towards degeneracy emerges. When Ets is equal to 2%
and 3%, the maximum splitting occurs along the Γ - 𝑀 path.
In other cases, the maximum splitting occurs along the 𝐴 - 𝑍
path. We provide a clearer illustration of the spin splitting and
its magnitude in Fig. S2 [51], and the orbital-resolved SOC

4
TABLE I. Evolution of OsO2 ’s lattice constants, magnetic moments, spin splitting, and spin-resolved Fermi surface shapes under different Ets .
Ets (%)
0

Lattice constants (Å)
𝑎
𝑐
4.522

3.215

Magnetic moment
of Os atoms (𝜇 𝐵 )

|Splitting| max (meV)
near the Fermi level

± 0.000

−

Spin-resolved Fermi surface
@ 𝑘 𝑧 = 𝜋/2𝑐 plane (with SOC)
0.10

0.0
0.10

1

4.568

3.169

± 0.002

62.8 @ 𝐴 − 𝑍

-0.10
0.0
0.10

2

4.612

3.125

± 0.028

209.2 @ Γ − 𝑀

-0.10
0.0

0.10

3

4.658

3.080

± 0.349

256.3 @ Γ − 𝑀

-0.10

0.0
0.10

4

4.703

3.043

± 0.468

275.5 @ 𝐴 − 𝑍

-0.10
0.0
0.10

5

4.749

3.003

± 0.500

110.0 @ 𝐴 − 𝑍

-0.10
0.0
0.10

6

4.795

2.965

± 0.150

0.11 @ 𝐴 − 𝑍

-0.10
0.0

-0.10

band structures are displayed in Fig. S3 [51].
As discussed previously, it can be observed that both the
magnetic moment of Os atoms and the maximum splitting
exhibit a trend of first increasing and then decreasing as Ets
increases. We know that the equibiaxial tensile strain in the
𝑥𝑦 axis direction (an increase in 𝑎 and 𝑏) will inevitably lead
to the compressive strain towards the center of the material
along the 𝑧 axis (a decrease in 𝑐) due to the Poisson effect [52].
This is also consistent with our calculation results, as shown in
Table I, where we can observe that the decrease in the lattice
constant 𝑐 is slightly greater than the increase in 𝑎.

B.

Strain-induced special alternating Fermi surface

It is noteworthy that when Ets is within the range of
2% ∼ 5%, the spin-resolved Fermi surface of OsO2 at the
𝑘 𝑧 = 𝜋/2𝑐 plane shows an obvious alternating pattern, which
is also listed in Table I. This is strong evidence for the altermagnetism of OsO2 . We also calculated the 3D spin-resolved
Fermi surface of OsO2 under different Ets (see Fig. S4 in the
Supplemental Material [51]). However, due to the complex
shape, it is difficult to observe the internal situation through
the outer surface from a 3D perspective. Therefore, we presented the projections of the 3D spin-resolved Fermi surface
of OsO2 at different 𝑘 𝑧 planes in the form of slices, as shown in
Fig. 2. Interestingly, for the case without strain, even in the absence of magnetism, the spin-resolved Fermi surface of OsO2
still exhibits an alternating pattern at the 𝑘 𝑧 = 𝜋/𝑐 plane, as
shown in Fig. 2(a) and Fig. S5 [51]. As the slices move downward, the spin-up and spin-down components (i.e., the red and
blue parts) gradually blend together and become indistinguish-

able, which can be observed more clearly in Fig. S5 [51]. At
present, we are not clear about the specific reasons for this
phenomenon, and it is also beyond the scope of discussion
in this paper. However, its physical origin is still worthy of
further investigation. Fig. 2(b) shows the spin-resolved Fermi
surface of OsO2 with Ets = 0% and Hubbard parameter 𝑈 = 2
eV for comparison. The alternating pattern can be observed
at the 𝑘 𝑧 = 0 and 𝑘 𝑧 = 𝜋/𝑐 planes, while the other slices
are very “clean”, which is similar to the results of DFT + 𝑈
calculations for RuO2 (the 3D spin-resolved Fermi surface of
RuO2 is displayed in Fig. S4 [51]).
As can be observed from Table I and Fig. 2, with the increase
of Ets , the spin-up and spin-down states gradually split along
a specific direction under the action of the crystal field, and
an alternating pattern is formed at the 𝑘 𝑧 = 𝜋/2𝑐 plane, which
is similar to the case in CrSb [22], indicating the emergence
of altermagnetism. Our orbital-resolved band structure analysis reveals that the electronic states near the Fermi level in
OsO2 are predominantly contributed by the Os 𝑑 𝑧 2 , 𝑑 𝑥 2 −𝑦 2 , and
𝑑 𝑥𝑧 + 𝑑 𝑦𝑧 orbitals. Under increasing Ets , the 𝑑 𝑧 2 -dominated
bands exhibit contrasting evolution trends: they shift downward along the Γ-𝑋-𝑀-Γ path (𝑘 𝑧 = 0 plane) while moving
upward along the 𝑍-𝑅-𝐴-𝑍 path (𝑘 𝑧 = 𝜋/𝑐 plane), eventually
crossing the Fermi level at the 𝑘 𝑧 = 𝜋/𝑐 plane (Fig. S3 [51]).
The 𝑘 𝑧 = 𝜋/2𝑐 plane is exactly the momentum region lying
between the 𝑘 𝑧 = 0 and 𝑘 𝑧 = 𝜋/𝑐 planes. It may serve as
the boundary region for two opposite trends of band evolution,
leading to the alternation of the spin polarization and the formation of an alternating pattern. We plot the band structures
of OsO2 at the 𝑘 𝑧 = 𝜋/2𝑐 plane with Ets increasing from 1% to
6%, as shown in Fig. 3. At the Fermi level, the band evolution
along the Γ★-𝑀 ★ path can be well correlated with Fig. 2 and

5
(a)

(c)
R

X

Z
A

Γ
M

R

R

X

(b)

(d)

X

Z
A

Γ
M

R

R

X

A

Γ
M

R

X

R

X

(f)
Z

(e)

X

Z
A

Γ
M

R

X

(g)
R

X

Z
A

Γ
M

R

X

R

X

Z
A

Γ
M

R

X

(h)
R

X

Z
A

Γ
M

R

X

R

X

Z
A

Γ
M

R

X

FIG. 2. The shapes of spin-resolved Fermi surfaces at different 𝑘 𝑧 planes for OsO2 under Ets values of (a) 0%, (b) 0% (𝑈 = 2.0 eV), (c) 1%,
(d) 2%, (e) 3%, (f) 4%, (g) 5%, and (h) 6%. The red and blue colors represent spin-up and spin-down, respectively.

Table I. These split bands that form the alternating patterns
near the Fermi level are mainly contributed by Os 𝑑 𝑥𝑧 + 𝑑 𝑦𝑧
and 𝑑 𝑥 2 −𝑦 2 orbitals. As can be clearly observed from Fig. 3,
even in the absence of SOC, the altermagnetic spin splitting
can still occur, which further confirms its nonrelativistic origin. In addition, it is also discernible that the introduction of
SOC instead weakens the spin splitting, resulting in a narrower
gap between the spin-up and spin-down bands, espetially for
Ets = 4% and 5%. This may lead to a weakening of the ASSEinduced transverse spin current, which will be discussed in
detail in the next section (Sec. III C).
It is noted that as 𝑘 𝑧 becomes larger, the pattern on the 𝑘
slice changes more and more drastically with the variation of
Ets . When Ets increases from 1% to 5%, the red and blue
concentric circles at the 𝑘 𝑧 = 0 plane only expand slightly
and separate a little; for the 𝑘 𝑧 = 𝜋/2𝑐 plane, we can clearly
observe how the alternating elliptical patterns evolve; while
for the 𝑘 𝑧 = 𝜋/𝑐 plane, the changes are quite drastic. When
Ets is further increased to 6% [Fig. 2(h)], the spin-up and spindown states begin to degenerate, which indicates that a greater
Ets may lead to the disappearance of altermagnetism. From
Table I, we can clearly see the correlation between the magnetic
moment of Os atoms, the magnitude of spin splitting, and the
shape of the spin-resolved Fermi surface. In Sec. III C, we will
further explore the relationship between these factors and the
ASSE-induced T -odd spin conductivity 𝜎𝑥𝑧,odd
𝑦 , as well as its
spin-charge conversion ratio 𝜃 AS .

C.

nonrelativistic ASSC induced by strain

An important application of altermagnets in the field of
spintronics is the T -odd spin current generated by the nonrelativistic ASSE. Although the magnetism of RuO2 is still
controversial, its significant spin-charge conversion efficiency
has been confirmed both in theoretical calculations [5, 6] and
experiments [6, 7, 16, 17]. This new mechanism enables an applied in-plane electrical current to generate a pure spin current
polarized along the Néel vector in the out-of-plane direction
from the RuO2 film into a recording FM layer. This makes it
possible to control the direction of spin polarization by adjusting the direction of the Néel vector [43]. We also calculated the
magnetocrystalline anisotropy energy (MAE) of OsO2 with Ets
ranging from 2% to 5%, as shown in Fig. S6 [51]. It can be observed that the Néel vector N̂ of OsO2 remains aligned along
the [001] direction (i.e., the 𝑧-axis), consistent with RuO2 .
Calculations show that in RuO2 , the spin-charge conversion
ratio of the T -odd ASSC induced by the ASSE can reach an
astonishing 28% [5], and its characteristic of not being dependent on SOC further makes ASSE a highly promising theoretical guideline for the design of next-generation spintronic
devices.
In this section, we systematically investigated the straininduced nonrelativistic ASSE in OsO2 . Using linear response theory and Eq. (1), we calculated the T -odd ASSC
𝛾
𝜎𝑥𝑧,odd
and charge conductivity 𝜎𝑥 𝑥 by setting 𝐴ˆ to 𝑗ˆ𝛼 and
𝑦

6
(a)

w/o SOC

2

w SOC

(b)

<Sz>

M*

(d)

Γ*

M*' M*

w/o SOC

2

Γ*

w SOC

M*

Γ*

M*' M*

w/o SOC

2

+

Γ*

w SOC

M*

Γ*

M*' M*

Γ*

M*'

M*' M*

w/o SOC

Γ*

w SOC

M*'

<Sz>
+

Up
Down

1

0

−2

Γ*

2

+

0

−1

−1

−1

M*

(f)

<Sz>

Up
Down

E - EF (eV)

E - EF (eV)

0

+

0

−2

M*'

1

1

<Sz>

−1

(e)

<Sz>

Up
Down

w SOC
Up
Down

1

0

−2

M*'

w/o SOC

2

+

−1

−1

E - EF (eV)

(c)

<Sz>

E - EF (eV)

E - EF (eV)

E - EF (eV)

0

−2

w SOC
Up
Down

1

1

−2

w/o SOC

2

+

Up
Down

M*

Γ*

M*' M*

Γ*

M*'

−2

M*

Γ*

M*' M*

Γ*

M*'

FIG. 3. Evolution of band structures with Ets ranging from 1% to 6% [labeled (a) to (f)] at the 𝑘 𝑧 = 𝜋/2𝑐 plane with and without SOC. The
positions of the high symmetry points Γ★, 𝑀 ★, and 𝑀 ★′ are displayed in Fig. 1(b). Red and blue represent opposite spins.

−𝑒 𝑣ˆ 𝛼 , respectively, as well as their ratio |𝜃 AS | = |𝜎𝑥𝑧,odd
𝑦 /𝜎𝑥 𝑥 |,
as shown in Fig. 4. Typically, we determine the value of
the scattering rate 𝚪 based on experimentally measured conductivity. The room-temperature conductivity of OsO2 is
∼ 16666.67 S/cm [27, 28], as shown by the gray dashed
line in Fig. 4(b), indicating that the corresponding 𝚪 value at
Ets = 0% should be ∼ 27 meV. A challenging issue is the absence of experimental conductivity data for OsO2 under strain,
leaving no basis for determining 𝚪 in such conditions. For the
convenience of comparison, we assume that strain does not
alter the conductivity of OsO2 ; thus, for all Ets from 0% to 6%,
we adopt the experimental value of 16666.67 S/cm to determine 𝚪. In fact, the strains involved in this work are extremely
small and likely have negligible effects on conductivity. More
importantly, the calculated ASSC 𝜎𝑥𝑧,odd
and charge conduc𝑦
tivity 𝜎𝑥 𝑥 exhibit an approximately linear relationship with
𝚪, resulting in their ratio |𝜃 AS | (exactly what we focus on)
being robust against variations in 𝚪, as shown in Fig. 4(c).
Therefore, errors in 𝚪 do not significantly affect our conclusions, thus the assumption of strain-independent conductivity
for OsO2 here is reasonable. Following this assumption, the
|𝜃 AS | curve under different Ets is plotted after determining 𝚪,
shown as the red line in Fig. 4(d), which is compared with the
maximum spin splitting near the Fermi surface without SOC:
|Splitting| max (black line) and the intrinsic spin Hall angle
(ISHA) |𝜃 IS | (blue line) associated with the relativistic CSHE.
Discussions about CSHE in OsO2 will be detailed in Sec. III D.
Specific values of 𝚪, charge conductivity 𝜎𝑥 𝑥 , ASSC |𝜎𝑥𝑧,odd
𝑦 |,
and |𝜃 AS | are provided in Table S3 [51].
It can be observed from Fig. 4(d) that when SOC is ne-

glected, the variation trend of |𝜃 AS | coincides with that of the
spin splitting magnitude. When SOC is considered, the situation changes notably. OsO2 achieves the highest spin-charge
conversion efficiency |𝜃 AS | ≈ 7% at Ets = 3%. This value
significantly exceeds the ISHA |𝜃 IS | generated via CSHE in
OsO2 , and surpasses those of a series of 4𝑑 and 5𝑑 transition
metals including Nb, Ta, Mo, Pd, and Pt [36, 53, 54]. It is
noteworthy that when Ets = 4% and 5%, the |𝜎𝑥𝑧,odd
𝑦 | curve
without SOC exhibits an overall enhancement compared to
other curves, as shown by the purple and gold dashed lines
in Fig. 4(a). This implies that under the same scattering rate
𝚪, the introduction of SOC leads to a smaller ASSC, which
may be related to the narrower spin splitting induced by SOC
discussed in the previous section (Sec. III B). This effect can
be directly observed in Figs. 3(d) and 3(e). Meanwhile, in the
absence of SOC, the electronic structure of OsO2 (Fig. S1 [51])
exhibits more electronic states near the Fermi level compared
to the SOC-included case (Fig. S3 [51]), which leads to higher
charge conductivity. As shown in Fig. S7 [51], the 𝜎𝑥 𝑥 without SOC is systematically shifted upward relative to the SOCincluded 𝜎𝑥 𝑥 [Fig. 4(b)] within the same 𝚪 range, manifested
as larger 𝚪 values corresponding to the experimental conductivity (Table S3 [51]). The complex interaction of these
factors ultimately results in the maximum |𝜃 AS | at Ets = 3%
in the presence of SOC [Fig. 4(d)], demonstrating that the
strong SOC in OsO2 is beneficial for its strain-induced ASSE.
It is worth mentioning that we also investigate the magnetic
moment of Ru variation with equibiaxial strain Es in RuO2 in
the absence of Hubbard 𝑈 correction (Table S4 [51]). The
results reveal that RuO2 exhibits no magnetism without strong

7

(a) 100000

(c)
2% w SOC
3% w SOC
4% w SOC
5% w SOC

3000
2500

1500

0.1
0% w SOC
1% w SOC
2% w SOC
3% w SOC
4% w SOC
5% w SOC
6% w SOC

0.001

1

J
z

σzxy

5%

0

2%

1000

6

500

3

20

100

24

28

32

36

40

4%
3%

2%

1

Γ (meV)

Γ (meV)
0%
1%
2%
3%
4%
5%
6%

20000

15000

10000

10

100

Γ (meV)
300

8
|Splitting|max (meV)
|θAS| (%) w SOC
|θAS| (%) w/o SOC
|θIS| (%)

250

5%

16666.67

16666.67

(d)

w/o SOC

5%

0

x

100000

4%

3

9

y

10

(b)
σxx w SOC (S/cm)

0% w/o SOC
1% w/o SOC
2% w/o SOC
3% w/o SOC
4% w/o SOC
5% w/o SOC
6% w/o SOC

w SOC

3%

6

2000

10

1E-5

9

|θAS| (%)

z, odd
| [(ћ/e) S/cm]
|σxy

1000

2% w/o SOC
3% w/o SOC
4% w/o SOC
5% w/o SOC

6%

200

0%
1%
4%
2%

150

3%

50

6

4

100

2

0

0

1

10

100

24

25

26

27

28

29

30

0

31

1

2

3

4

5

6

(%)

Γ (meV)

Γ (meV)

FIG. 4. (a) T -odd ASSC |𝜎𝑥𝑧,odd
𝑦 |, (b) charge conductivity 𝜎𝑥 𝑥 , and (c) spin-charge conversion ratio |𝜃 AS | as functions of the scattering rate
𝚪. (d) The variation of |Splitting| max , |𝜃 AS |, and |𝜃 IS | with Ets . The inset in the lower right corner of (a) reveal the directions of charge current
𝐽 (red arrow), Néel vector (marked as N̂ with a violet arrow), spin polarization (indicated by the green arrow), and the spin current (denoted
by the black arrow). The insets on the right side of (a) and (b) illustrate local details. The solid and dashed lines in (a), (c), and (d) represent
results with and without SOC, respectively. The intensity of the background color in (d) indicates the magnitude of the values.
⊥|
TABLE II. Calculated ISHC 𝜎𝑥𝑧 𝑦 and corresponding ISHA |𝜃 IS | of (001)-oriented OsO2 , as well as 𝜎𝑧𝑧𝑥 and corresponding out-of-plane |𝜃 IS
of (101)-oriented OsO2 under different equibiaxial tensile strain Ets .

Ets (%)

𝜎𝑥𝑧 𝑦 [(ℏ/𝑒)S/cm]

|𝜃 IS | (%)

𝜎𝑧𝑧𝑥 [(ℏ/𝑒)S/cm]

⊥ | (%)
|𝜃 IS

0
1

10.80
−50.15

0.06
0.30

−
108.25

−
0.65

2

−141.37

0.85

86.34

0.52

3
4

−153.17
−134.09

0.92
0.81

7.24
−87.53

0.04
0.53

5
6

−166.85
−280.55

1.00
1.68

−80.96
−311.87

0.49
1.87

Coulomb correlation, while minor equibiaxial strain can induce altermagnetism. This suggests the necessity for experimental characterization of the Hubbard 𝑈 parameter’s value
in RuO2 . Weaker electronic correlations in RuO2 may explain
the ongoing controversies regarding its magnetic properties.

D.

Relativistic CSHE in OsO2

with Ets in range of 1% to 6% are illustrated in Fig. 5. The
corresponding results for Ets = 0% are shown in Fig. S8 [51].
The SBC is plotted by taking the logarithm of Eqs. (4) and (5)
to more clearly show the rapid variation of SBC. This strategy
was also employed in previous studies [37, 55, 56], and its
definition is given by
(
′

Ω =
As a 5𝑑 heavy metal, Os exhibits strong SOC, which is
expected to generate a large ISHC. This section will continue
to investigate the effects of equibiaxial tensile strain Ets on the
ISHC 𝜎𝑥𝑧 𝑦 and SBC in OsO2 , calculated using Eqs. (4) and
(5), respectively. The calculated ISHC 𝜎𝑥𝑧 𝑦 and the SBC Ω𝑧𝑥 𝑦
resolved band structures as well as the 𝑘-resolved SBC of OsO2

sgn(Ω) log10 |Ω|,
Ω
10 ,

|Ω| > 10
,
|Ω| ⩽ 10

(7)

where sgn(Ω) means taking the sign of Ω.
Table II lists the values of ISHC 𝜎𝑥𝑧 𝑦 at 𝐸 = 𝐸 𝐹 and ISHA
|𝜃 IS | = |𝜎𝑥𝑧 𝑦 /𝜎exp | under different Ets , where 𝜎exp represents
the experimental conductivity at room temperature, i.e., ∼
16666.67 S/cm [27, 28]. Our calculated ISHC magnitude

8

Γ

Z

R

A

Z

-200

-0.5

0

0.5

-1.0

X

M

Γ

Z

R

A

Z

-0.5

Γ

Z

R

A

Z

-0.5
-600 -400 -200

0.0

k-resolved SBC @ E = EF

0.5

0

Γ

X

M

Γ

Z

R

A

Z

-0.5

X

M

Γ

Z

R

A

Z

ISHC
0.5

0.0

0.0

0

E - EF (eV)

0.5

k-resolved SBC @ E = EF

1.0

0.0

0.5
0.0
-0.5

200

σzxy [(ћ/e)·S/cm]

200

σzxy [(ћ/e)·S/cm]

0.5

0.0

-0.5
-600 -400 -200

-0.5
-600 -400 -200 0

-0.5

-0.5

0.0

200

0.0

Γ

(f)

ISHC
0.5

-0.5

σzxy [(ћ/e)·S/cm]

log10|Ωzxy(k)| (Å2)

0.5

0.0

-0.5

σzxy [(ћ/e)·S/cm]

0.5

k-resolved SBC @ E = EF

0.5

-1.0

-400-200 0 200 400

-0.5

0.0

0.0

Γ

M

0.0

-0.5

-1.5

X

-0.5

log10|Ωzxy(k)| (Å2)

0.0
k-resolved SBC @ E = EF

0.5

E - EF (eV)

0.0

-0.5

E - EF (eV)
Γ

(e)

ISHC
0.5

0.5

0.0

-0.5

200

σzxy [(ћ/e)·S/cm]

0.0

E - EF (eV)

M

E - EF (eV)

(d)

X

ISHC
0.5

0.0

0.0

-0.5

-0.5

Γ

E - EF (eV)

0.0
k-resolved SBC @ E = EF

0.5

0.5
0.5

-0.5

E - EF (eV)

-0.5

0.0

0.0

0.0

(c)

ISHC
0.5

-0.5

log10|Ωzxy(k)| (Å2)

log10|Ωzxy(k)| (Å2)

E - EF (eV)

0.0
k-resolved SBC @ E = EF

0.5

0.5
0.5

log10|Ωzxy(k)| (Å2)

E - EF (eV)

E - EF (eV)

0.0

-0.5

log10|Ωzxy(k)| (Å2)

(b)

ISHC
0.5

E - EF (eV)

0.5
0.5

E - EF (eV)

(a)

Γ

X

M

Γ

Z

R

A

Z

-0.5

-0.5
-400

-200

0

σzxy [(ћ/e)·S/cm]

FIG. 5. Band structures projected by SBC Ω 𝑧𝑥 𝑦 on a logarithmic scale using Eq. (7) and 𝑘-resolved SBC of OsO2 under Ets values of (a) 1%,
(b) 2%, (c) 3%, (d) 5%, and (e) 6%. The ISHC 𝜎𝑥𝑧 𝑦 as a function of Fermi energy is shown on the right.

(a)

(b)

(c)

0.3
0.2

0.1

0.0

(d)

(e)

(f)
-0.1
-0.2

-0.3

FIG. 6. The 𝑘-resolved SBC Ω 𝑧𝑥 𝑦 on a logarithmic scale calculated
using Eq. (7) in a 2D BZ slice at the 𝑘 𝑧 = 𝜋/2𝑐 plane of OsO2 , under
Ets values of (a) 1%, (b) 2%, (c) 3%, (d) 5%, and (e) 6% at 𝐸 = 𝐸 𝐹 .
The black lines denote the intersections of the Fermi surface with the
slices. The red and blue colors represent positive and negative SBC
Ω 𝑧𝑥 𝑦 (in unit of Å2 ), respectively.

without strain (i.e., Ets = 0%) is 10.80 (ℏ/𝑒)S/cm, which
is close to previous computational values [9 (ℏ/𝑒)S/cm] in
Ref. [57]. From both Table II and Fig. 4(d), it can be observed
that the magnitude of ISHA |𝜃 IS | exhibits an almost positive
correlation with Ets , and it remains significantly lower than
|𝜃 AS | when ASSE exists in OsO2 (i.e., Ets = 2% ∼ 5%). This
further demonstrates the superiority of ASSE over CSHE and
the potential breakthroughs brought by strain engineering.
We know that ISHC is directly related to the SBC, which
acts as a magnetic field in momentum space [43]. Some sharp
peaks caused by the bands crossing near the Fermi energy can
be observed at specific 𝑘 paths in the 𝑘-resolved SBC, as illustrated in Fig. 5. It can be seen that strain has relatively minor
effects on the band structure near the Fermi level of OsO2 ,
which leads to similar 𝑘-resolved SBC patterns and comparable energy-dependent ISHC trends under different strains. We

are particularly interested in how the alternating pattern at the
𝑘 𝑧 = 𝜋/2𝑐 plane influences SBC, and therefore we calculated
the projected 𝑘-resolved SBC on this slice, as shown in Fig. 6.
The overlapping regions of the two ellipses result in nearly vanishing SBC, while the elliptical tips enhance SBC, producing
larger negative values. Beyond these features, the overall SBC
remains largely unaffected. This observation further confirms
the distinct physical origins between ASSE and CSHE.
As a supplement, we also offer the calculated T -odd ASSC
and T -even ISHC tensors in units of (ℏ/𝑒)S/cm for OsO2 with
different growth orientations and charge current directions,
as displayed in Tables S5 and S6 [51]. For (001)-oriented
𝛾
OsO2 , only components 𝜎𝛼𝛽 with mutually orthogonal 𝛼, 𝛽,
𝛾 (i.e., the Levi-Civita tensor 𝜖 𝛼𝛽𝛾 ≠ 0) are non-zero. For
(101)-oriented OsO2 , the coordinate system is transformed
from that of a (001)-oriented OsO2 using a rotation matrix
(counterclockwise rotation about the 𝑦[010] axis by 𝜑)
!
cos 𝜑 0 sin 𝜑
0
1 0 ,
D=
− sin 𝜑 0 cos 𝜑
where for the case of (001)-to-(101)-oriented rotation, 𝜑 =
arctan 𝑎𝑐 . The tensors for (101)-oriented OsO2 are then
obtained as follows [6]
(101)
(001)
P
𝑛
𝜎𝑖𝑘𝑗 = 𝑙,𝑚,𝑛 D𝑖𝑙 D 𝑗𝑚 D 𝑘𝑛 𝜎𝑙𝑚
.

(8)

Similar to the case discussed in Ref. [6], when an electric
field is applied along the [010] direction for (101)-oriented
OsO2 , the T -even spin current flow in the [001] direction
exhibits both a component of flow in the vertical direction and
a component of spin polarization out of plane, with amplitude
(001)
𝑥
𝜎𝑧𝑦
sin 𝜑 cos 𝜑.

Simultaneously, the spin current flow in the [100] direction
also has a component of spin current flow in the vertical direc-

9
tion with a component of spin polarization out of plane, with
amplitude
(001)
𝜎𝑥𝑧 𝑦 sin 𝜑 cos 𝜑.

Thus, under the condition
(001)

(001)
𝑦

(001)

− 𝜎𝑧𝑥𝑦 = 𝜎𝑧 𝑥 ≠ 𝜎𝑥𝑧 𝑦 ,
the T -even mechanism can generate a non-zero net verticallyflowing spin current with out-of-plane spin polarization, characterized by
(101)
(001)
(001)
(101)
𝑦
𝜎𝑧𝑥𝑦 sin 𝜑 cos 𝜑 + 𝜎𝑥𝑧 𝑦 sin 𝜑 cos 𝜑 = 𝜎𝑧𝑧𝑥 = − 𝜎𝑦 𝑥 ,

(9)

which is crucial for field-free perpendicular magnetic switching. This particular spin current can also be generated through
the T -odd ASSE mechanism, with detailed calculation results
shown in Table S5 [51]. At Ets = 3%, |𝜎𝑧𝑧,odd
𝑥 | reaches up to
646.96 (ℏ/𝑒)S/cm. However, unlike the case in the T -even
mechanism, in T -odd ASSC tensors, only the components
with spin polarization aligned with the direction of Néel vector
N̂ can be generated in the absence of SOC [6, 43]. Actually,
these components in (101)-oriented OsO2 will cancel each
other due to N̂ along the [001] and [001̄] directions between
different domains, i.e.,
(101) N̂ ↓
(101) tot
(101) N̂ ↑
𝑧,odd
𝑧,odd
𝜎𝑧 𝑥 = 𝜎𝑧 𝑥 + 𝜎𝑧¯𝑧¯𝑥,odd → 0,

where N̂ ↑ and N̂ ↓ denote the Néel vector oriented along the
[001] and [001̄] directions, respectively. Therefore, we focus
exclusively on the T -even mechanism, which is unconstrained
by the Néel vector here.
The calculated values of T -even 𝜎𝑧𝑧𝑥 in (101)-oriented
OsO2 under different Ets are displayed in Table II, with full
T -even ISHC tensors detailed in Table S6. For comparison,
we also present T -odd ASSC tensors with Ets ranging from
2% ∼ 5% in Table S5 [51]. It can be observed from Table II
that a 6% equibiaxial tensile strain in (001)-oriented OsO2 is
⊥ | as high as 1.87%,
able to induce an out-of-plane ISHA |𝜃 IS
far exceeding that in RuO2 [6] and even surpassing the conventional ISHA in (001)-oriented OsO2 . This can be simply
achieved by rotating OsO2 to the (101)-oriented configuration.
Through Table S6, it is noted that as Ets increases, the value of
𝜎𝑧𝑥𝑦 transitions from positive to negative, while 𝜎𝑥𝑧 𝑦 remains
consistently negative. According to Eq. (9), the value of 𝜎𝑧𝑧𝑥
in (101)-oriented OsO2 initially cancels out due to opposing
signs as Ets increases, reaching a minimum at Ets = 3%. Subsequently, it enhances due to identical signs, ultimately attaining
a maximum at Ets = 6%.
IV.

CONCLUSION

This work proposes strain engineering as a novel viable approach to induce ASSE, successfully achieving equibiaxial tensile strain Ets -induced ASSE in OsO2 . We observed the emergence of alternating patterns at the 𝑘 𝑧 = 𝜋/2𝑐 plane and nonrelativistic spin splitting along specific high-symmetry paths,

while evaluating the T -odd ASSC |𝜎𝑥𝑧,odd
𝑦 | and spin-charge
conversion ratio |𝜃 AS | generated by strain-induced ASSE in
OsO2 . Our findings reveal that |𝜃 AS | reaches a maximum of
∼ 7% under Ets = 3%, and notably maintains ∼ 5% even without SOC—significantly surpassing the ISHA |𝜃 IS | generated
by CSHE in OsO2 . We also find that |𝜃 AS | exhibits a positive
correlation with the magnitude of spin splitting, both showing
an initial increase followed by a decrease as Ets grows, whereas
|𝜃 IS | displays an almost monotonic increase with increasing Ets .
Calculations of spin Berry curvature (SBC) further demonstrate the distinct physical origins between ASSE and CSHE
in OsO2 . Additionally, we predict that when Ets = 6%, the
⊥|
(101)-oriented OsO2 will generate an out-of-plane ISHA |𝜃 IS
of ∼ 1.87%, which makes it highly promising for applications
in the field-free perpendicular magnetic switching. Finally,
we find that strain can also induce altermagnetism in RuO2 ,
which not only demonstrates the universal feasibility of strain
engineering for altermagnetism generation but also provides
a plausible explanation for the longstanding debate regarding
the existence of magnetism in RuO2 . Further calculations considering the on-site Coulomb interaction (details in Appendix
section) indicate that, under reasonable Hubbard 𝑈 correction,
our proposed strain-induced ASSE remains effective, yielding
a |𝜃 AS | of up to 16.36% without SOC. Even under the assumption that OsO2 is intrinsically altermagnetic (𝑈 = 2.0 eV
case), where larger strains substantially complicate the behavior, a slight 1% strain still improves the spin-charge conversion
ratio (Table S2 [51]). This further highlights the robustness of
strain engineering in enhancing the conversion efficiency. This
work provides new insights for altermagnet discovery and establishes theoretical foundations for designing next-generation
altermagnetic spintronic devices.
ACKNOWLEDGMENTS

The authors would like to acknowledge the financial support from National Key Research and Development Program
of China (Grant No. 2022YFA1602701), and National Natural Science Foundation of China (Grants No. 12204364, No.
12327806, and No. 12227806). Numerical calculation is supported by the High-Performance Computing Center of Wuhan
University of Science and Technology.
DATA AVAILABILITY

The data that support the findings of this article are openly
available [58].
Appendix: Results with Hubbard U correction

As shown in Fig. A1, the linear response approach [50] indicates that 𝑈 = 1.13 eV is appropriate for our system. Detailed
results at 𝑈 = 1.13 eV are tabulated in Tables S7 and S8 [51].
Table S7 presents the evolution of lattice constants, magnetic
moment of Os atoms, and spin-resolved Fermi surface at the

10

𝑘 𝑧 = 𝜋/2𝑐 with equibiaxial tensile strain Ets . Table S8 shows
the dependence of scattering rate 𝚪, charge conductivity 𝜎𝑥 𝑥 ,
ASSC 𝜎𝑥𝑧,odd
𝑦 , and spin-charge conversion ratio |𝜃 AS | on Ets .
For 𝑈 = 1.13 eV with Ets varying between 1%–6%, Fig. S9
displays shapes of spin-resolved Fermi surfaces at different 𝑘 𝑧
planes (the corresponding 3D Fermi surfaces are displayed in
Fig. S12), while Fig. S10 shows the evolution of band structures with and without SOC. The case of Ets = 0% is displayed
in Fig. S13. Strain- and 𝚪-dependent curves from Table S8 are
presented in Fig. S11, with Fig. S11(d) specifically showing
|𝜃 AS | versus Ets at different 𝑈 values [51].
Unlike the case without Hubbard 𝑈 correction, when
𝑈 = 1.13 eV, OsO2 exhibits a monotonic increase in both
ASSC 𝜎𝑥𝑧,odd
and spin-charge conversion ratio |𝜃 AS | with in𝑦
creasing Ets . At Ets = 6%, |𝜃 AS | reaches 12.43%, nearly twice
the maximum value achieved without Hubbard 𝑈 correction.
When SOC is excluded, |𝜃 AS | reaches up to 16.36%. As clearly

observed in Fig. S10, the introduction of SOC reduces the spin
splitting magnitude; this reduction is more pronounced than
that observed without 𝑈 (Fig. 3), resulting in a larger |𝜃 AS | in
the absence of SOC.
At 𝑈 = 1.13 eV, significant changes occur in the spinresolved Fermi surface on the 𝑘 𝑧 = 𝜋/2𝑐 plane. Compared
to previous results (Fig. 2), it becomes more dispersed. At
Ets = 4%, no distinct alternating pattern is observable. As
clearly seen in Fig. S10(d), a bandgap opens at the Fermi level
on the 𝑘 𝑧 = 𝜋/2𝑐 plane, causing the disappearance of the alternating pattern, which shifts to other energy levels. Moreover,
when Ets = 4% and without SOC, OsO2 becomes ferromagnetic [Fig. S10(d)]. This situation is analogous to the case
with 𝑈 = 2.0 eV, Ets = 5% (Table S2 [51]). However, the
latter remains ferromagnetic when SOC is included, while the
former becomes altermagnetic when SOC is considered. Notably, when |𝜃 AS | reaches 6%, the spin-resolved Fermi surface
of OsO2 becomes distinctly asymmetric [Fig. S9(f)]. Careful observation reveals that this asymmetry emerges as early
as |𝜃 AS | = 5% [Fig. S9(e) shows a larger red ellipse in the
bottom-left corner compared to the top-right corner]. Additionally, under 𝑈 = 1.13 eV and zero strain, an alternating
pattern persists in the spin-resolved Fermi surfaces despite
a zero magnetic moment on Os atoms, consistent with observations made without 𝑈 correction. Currently, we cannot
provide a definitive explanation for these phenomena, and exploring their underlying physical mechanisms lies beyond the
scope of this work. Therefore, we refrain from further detailed
discussion here.
In summary, our calculations demonstrate that strain engineering can always enhance the ASSE-induced spin-charge
conversion ratio in OsO2 , regardless of whether the on-site
Coulomb interaction is considered or the material itself is altermagnetic. This robust and universal enhancement highlights
the fundamental significance of our findings and underscores
the broader applicability of strain engineering strategy for altermagnetic spintronics.

[1] L. Šmejkal, J. Sinova, and T. Jungwirth, Beyond Conventional
Ferromagnetism and Antiferromagnetism: A Phase with Nonrelativistic Spin and Crystal Rotation Symmetry, Phys. Rev. X
12, 031042 (2022).
[2] L. Šmejkal, J. Sinova, and T. Jungwirth, Emerging Research
Landscape of Altermagnetism, Phys. Rev. X 12, 040501 (2022).
[3] C. Song, H. Bai, Z. Zhou, L. Han, H. Reichlova, J. H. Dil, J. Liu,
X. Chen, and F. Pan, Altermagnets as a new class of functional
materials, Nat. Rev. Mater. 10, 473 (2025).
[4] L. Bai, W. Feng, S. Liu, L. Šmejkal, Y. Mokrousov, and Y. Yao,
Altermagnetism: Exploring New Frontiers in Magnetism and
Spintronics, Adv. Funct. Mater. 34, 2409327 (2024).
[5] R. González-Hernández, L. Šmejkal, K. Výborný, Y. Yahagi,
J. Sinova, T. c. v. Jungwirth, and J. Železný, Efficient Electrical
Spin Splitter Based on Nonrelativistic Collinear Antiferromagnetism, Phys. Rev. Lett. 126, 127701 (2021).
[6] A. Bose, N. J. Schreiber, R. Jain, D.-F. Shao, H. P. Nair, J. Sun,
X. S. Zhang, D. A. Muller, E. Y. Tsymbal, D. G. Schlom, and
D. C. Ralph, Tilted spin current generated by the collinear anti-

ferromagnet ruthenium dioxide, Nat. Electron. 5, 267 (2022).
[7] H. Bai, Y. C. Zhang, Y. J. Zhou, P. Chen, C. H. Wan, L. Han,
W. X. Zhu, S. X. Liang, Y. C. Su, X. F. Han, F. Pan, and
C. Song, Efficient Spin-to-Charge Conversion via Altermagnetic
Spin Splitting Effect in Antiferromagnet RuO2 , Phys. Rev. Lett.
130, 216701 (2023).
[8] F. Liu, Z. Zhang, X. Yuan, Y. Liu, S. Zhu, Z. Lu, and
R. Xiong, Giant tunneling magnetoresistance in insulated altermagnet/ferromagnet junctions induced by spin-dependent tunneling effect, Phys. Rev. B 110, 134437 (2024).
[9] Z. Zhang, Y. Liu, Z. Lu, and R. Xiong, Interfacial modulation of
magnetic relaxation and electrical characteristic in RuO2 /CrO2
antiferromagnet-half metal bilayer, Mater. Des. 238, 112651
(2024).
[10] J. Krempaský, L. Šmejkal, S. W. D’Souza, M. Hajlaoui,
G. Springholz, K. Uhlířová, F. Alarab, P. C. Constantinou,
V. Strocov, D. Usanov, W. R. Pudelko, R. González-Hernández,
A. Birk Hellenes, Z. Jansa, H. Reichlová, Z. Šobáň, R. D. Gonzalez Betancourt, P. Wadley, J. Sinova, D. Kriegner, J. Minár,

6.2

NSCF
SCF

Number of d-electrons

6.1
6.0
5.9
5.8
5.7
5.6
5.5
−0.2

−0.1

0.0

0.1

0.2

U (eV)

FIG. A1. Hubbard 𝑈 parameter determined by linear response approach.

11
J. H. Dil, and T. Jungwirth, Altermagnetic lifting of Kramers
spin degeneracy, Nature 626, 517 (2024).
[11] S. Lee, S. Lee, S. Jung, J. Jung, D. Kim, Y. Lee, B. Seok,
J. Kim, B. G. Park, L. Šmejkal, C.-J. Kang, and C. Kim, Broken
Kramers Degeneracy in Altermagnetic MnTe, Phys. Rev. Lett.
132, 036702 (2024).
[12] T. Osumi, S. Souma, T. Aoyama, K. Yamauchi, A. Honma,
K. Nakayama, T. Takahashi, K. Ohgushi, and T. Sato, Observation of a giant band splitting in altermagnetic MnTe, Phys. Rev.
B 109, 115102 (2024).
[13] B. Pan, P. Zhou, P. Lyu, H. Xiao, X. Yang, and L. Sun, General
Stacking Theory for Altermagnetism in Bilayer Systems, Phys.
Rev. Lett. 133, 166701 (2024).
[14] S. Zeng and Y.-J. Zhao, Bilayer stacking 𝐴-type altermagnet:
A general approach to generating two-dimensional altermagnetism, Phys. Rev. B 110, 174410 (2024).
[15] Y. Liu, J. Yu, and C.-C. Liu, Twisted Magnetic Van der Waals
Bilayers: An Ideal Platform for Altermagnetism, Phys. Rev.
Lett. 133, 206702 (2024).
[16] H. Bai, L. Han, X. Y. Feng, Y. J. Zhou, R. X. Su, Q. Wang,
L. Y. Liao, W. X. Zhu, X. Z. Chen, F. Pan, X. L. Fan, and
C. Song, Observation of Spin Splitting Torque in a Collinear
Antiferromagnet RuO2 , Phys. Rev. Lett. 128, 197202 (2022).
[17] S. Karube, T. Tanaka, D. Sugawara, N. Kadoguchi, M. Kohda,
and J. Nitta, Observation of Spin-Splitter Torque in Collinear
Antiferromagnetic RuO2 , Phys. Rev. Lett. 129, 137201 (2022).
[18] Y. Zhang, H. Bai, L. Han, C. Chen, Y. Zhou, C. H. Back,
F. Pan, Y. Wang, and C. Song, Simultaneous High ChargeSpin Conversion Efficiency and Large Spin Diffusion Length in
Altermagnetic RuO2 , Adv. Funct. Mater. 34, 2313332 (2024).
[19] J. Liu, J. Zhan, T. Li, J. Liu, S. Cheng, Y. Shi, L. Deng, M. Zhang,
C. Li, J. Ding, Q. Jiang, M. Ye, Z. Liu, Z. Jiang, S. Wang, Q. Li,
Y. Xie, Y. Wang, S. Qiao, J. Wen, Y. Sun, and D. Shen, Absence
of Altermagnetic Spin Splitting Character in Rutile Oxide RuO2 ,
Phys. Rev. Lett. 133, 176401 (2024).
[20] O. Fedchenko, J. Minár, A. Akashdeep, S. W. D’Souza, D. Vasilyev, O. Tkach, L. Odenbreit, Q. Nguyen, D. Kutnyakhov,
N. Wind, L. Wenthaus, M. Scholz, K. Rossnagel, M. Hoesch,
M. Aeschlimann, B. Stadtmüller, M. Kläui, G. Schönhense,
T. Jungwirth, A. B. Hellenes, G. Jakob, L. Šmejkal, J. Sinova,
and H.-J. Elmers, Observation of time-reversal symmetry breaking in the band structure of altermagnetic RuO2 , Sci. Adv. 10,
eadj4883 (2024).
[21] S. Reimers, L. Odenbreit, L. Šmejkal, V. N. Strocov, P. Constantinou, A. B. Hellenes, R. Jaeschke Ubiergo, W. H. Campos,
V. K. Bharadwaj, A. Chakraborty, T. Denneulin, W. Shi, R. E.
Dunin-Borkowski, S. Das, M. Kläui, J. Sinova, and M. Jourdan,
Direct observation of altermagnetic band splitting in CrSb thin
films, Nat. Commun. 15, 2116 (2024).
[22] J. Ding, Z. Jiang, X. Chen, Z. Tao, Z. Liu, T. Li, J. Liu, J. Sun,
J. Cheng, J. Liu, Y. Yang, R. Zhang, L. Deng, W. Jing, Y. Huang,
Y. Shi, M. Ye, S. Qiao, Y. Wang, Y. Guo, D. Feng, and D. Shen,
Large Band Splitting in 𝑔-Wave Altermagnet CrSb, Phys. Rev.
Lett. 133, 206401 (2024).
[23] T. Urata, W. Hattori, and H. Ikuta, High mobility charge transport in a multicarrier altermagnet CrSb, Phys. Rev. Mater. 8,
084412 (2024).
[24] K. D. Belashchenko, Giant Strain-Induced Spin Splitting Effect
in MnTe, a 𝑔-Wave Altermagnetic Semiconductor, Phys. Rev.
Lett. 134, 086701 (2025).
[25] M. Hiraishi, H. Okabe, A. Koda, R. Kadono, T. Muroi, D. Hirai,
and Z. Hiroi, Nonmagnetic Ground State in RuO2 Revealed by
Muon Spin Rotation, Phys. Rev. Lett. 132, 166702 (2024).
[26] P. Keßler, L. Garcia-Gassull, A. Suter, T. Prokscha, Z. Salman,

D. Khalyavin, P. Manuel, F. Orlandi, I. I. Mazin, R. Valentí, and
S. Moser, Absence of magnetic order in RuO2 : insights from
𝜇SR spectroscopy and neutron diffraction, npj Spintronics 2, 50
(2024).
[27] D. B. Rogers, R. D. Shannon, A. W. Sleight, and J. L. Gillson,
Crystal chemistry of metal dioxides with rutile-related structures, Inorg. Chem. 8, 841 (1969).
[28] J. Horkans and M. W. Shafer, An Investigation of the Electrochemistry of a Series of Metal Dioxides with Rutile-Type
Structure: MoO2 , WoO2 , ReO2 , RuO2 , OsO2 , and IrO2 , J.
Electrochem. Soc. 124, 1202 (1977).
[29] Y. Wang, F. Li, H. Zheng, X. Han, and Y. Yan, Large magnetic
anisotropy and its strain modulation in two-dimensional intrinsic
ferromagnetic monolayer RuO2 and OsO2 ", Phys. Chem. Chem.
Phys. 20, 28162 (2018).
[30] G.-Z. Liu, S.-T. Sun, Y. B. Chen, S.-H. Yao, and J. Zhou, Firstprinciples studies on the crystal structure and electronic properties of two-dimensional RuO2 and OsO2 , Phys. Rev. B 109,
075411 (2024).
[31] G. Kresse and J. Hafner, Ab initio molecular dynamics for liquid
metals, Phys. Rev. B 47, 558 (1993).
[32] G. Kresse and J. Furthmüller, Efficient iterative schemes for
ab initio total-energy calculations using a plane-wave basis set,
Phys. Rev. B 54, 11169 (1996).
[33] G. Kresse and D. Joubert, From ultrasoft pseudopotentials to
the projector augmented-wave method, Phys. Rev. B 59, 1758
(1999).
[34] P. E. Blöchl, Projector augmented-wave method, Phys. Rev. B
50, 17953 (1994).
[35] J. P. Perdew, K. Burke, and M. Ernzerhof, Generalized Gradient
Approximation Made Simple, Phys. Rev. Lett. 77, 3865 (1996).
[36] G. Y. Guo, S. Murakami, T.-W. Chen, and N. Nagaosa, Intrinsic Spin Hall Effect in Platinum: First-Principles Calculations,
Phys. Rev. Lett. 100, 096401 (2008).
[37] J. Qiao, J. Zhou, Z. Yuan, and W. Zhao, Calculation of intrinsic
spin Hall conductivity by Wannier interpolation, Phys. Rev. B
98, 214402 (2018).
[38] A. A. Mostofi, J. R. Yates, Y.-S. Lee, I. Souza, D. Vanderbilt,
and N. Marzari, wannier90: A tool for obtaining maximallylocalised Wannier functions, Comput. Phys. Commun. 178, 685
(2008).
[39] J. Železný, Y. Zhang, C. Felser, and B. Yan, Spin-Polarized
Current in Noncollinear Antiferromagnets, Phys. Rev. Lett. 119,
187204 (2017).
[40] T. Tanaka, H. Kontani, M. Naito, T. Naito, D. S. Hirashima,
K. Yamada, and J. Inoue, Intrinsic spin Hall effect and orbital
Hall effect in 4𝑑 and 5𝑑 transition metals, Phys. Rev. B 77,
165117 (2008).
[41] F. Freimuth, S. Blügel, and Y. Mokrousov, Spin-orbit torques in
Co/Pt(111) and Mn/W(001) magnetic bilayers from first principles, Phys. Rev. B 90, 174423 (2014).
[42] H. Li, H. Gao, L. P. Zârbo, K. Výborný, X. Wang, I. Garate,
F. Doǧan, A. Čejchan, J. Sinova, T. Jungwirth, and A. Manchon,
Intraband and interband spin-orbit torques in noncentrosymmetric ferromagnets, Phys. Rev. B 91, 134402 (2015).
[43] W. Zhang, M. Zheng, Y. Liu, P. Zhang, Z. Zhang, R. Xiong, and
Z. Lu, Unconventional spin Hall effect in rutile Cr0.5 𝑋0.5 O2
(𝑋 = Ti, V, Os, Fe), Phys. Rev. B 110, 214419 (2024).
[44] J. Železný, H. Gao, A. Manchon, F. Freimuth, Y. Mokrousov,
J. Zemen, J. Mašek, J. Sinova, and T. Jungwirth, Spin-orbit
torques in locally and globally noncentrosymmetric crystals:
Antiferromagnets and ferromagnets, Phys. Rev. B 95, 014403
(2017).
[45] K. Li, J. Feng, W. Zhang, Z. Zhang, R. Xiong, and Z. Lu,

12
Enhancing spin splitting by symmetry and molecular orbital
hybridization in VO2 , Comput. Mater. Sci. 222, 112100 (2023).
[46] Z. Zhang, M. Cheng, Z. Fan, Y. Liu, D. Wang, K. Wang,
R. Xiong, and Z. Lu, The high magnetoresistance performance
of epitaxial half-metallic CrO2 -based magnetic junctions, Phys.
Chem. Chem. Phys. 25, 1848 (2023).
[47] C.-E. Boman, Precision determination of the crystal structure of
osmium dioxide, Acta Chem. Scand 24, 123 (1970).
[48] Y. C. Venudhar, L. Iyengar, and K. V. Krishna Rao, Anomalous
thermal expansion of osmium dioxide, Cryst. Res. Technol. 20,
1393 (1985).
[49] A. Regoutz, A. M. Ganose, L. Blumenthal, C. Schlueter, T.-L.
Lee, G. Kieslich, A. K. Cheetham, G. Kerherve, Y.-S. Huang,
R.-S. Chen, G. Vinai, T. Pincelli, G. Panaccione, K. H. L. Zhang,
R. G. Egdell, J. Lischner, D. O. Scanlon, and D. J. Payne,
Insights into the electronic structure of oso2 using soft and hard
x-ray photoelectron spectroscopy in combination with density
functional theory, Phys. Rev. Mater. 3, 025001 (2019).
[50] M. Cococcioni and S. de Gironcoli, Linear response approach
to the calculation of the effective interaction parameters in the
LDA + 𝑢 method, Phys. Rev. B 71, 035105 (2005).
[51] See Supplemental Material at [URL will be inserted by publisher] for (i) the influence of Hubbard 𝑈 correction on OsO2 ,
(ii) supplemental band structures, (iii) 3D Fermi surfaces, (iv)
magnetocrystalline anisotropy energy (MAE) of OsO2 under
different Ets , (v) the 𝚪 values determined from experimental

data and the corresponding calculated results, (vi) charge conductivity without SOC, (vii) strain-induced altermagnetism in
RuO2 , (viii) CSHE in OsO2 without strain, (ix) ASSC and ISHC
tensors of (001) & (101)-oriented OsO2 , and (x) supplemental
figures for U = 1.13 eV case.
[52] G. N. Greaves, A. L. Greer, R. S. Lakes, and T. Rouxel, Poisson’s
ratio and modern materials, Nat. Mater. 10, 823 (2011).
[53] M. Morota, Y. Niimi, K. Ohnishi, D. H. Wei, T. Tanaka, H. Kontani, T. Kimura, and Y. Otani, Indication of intrinsic spin Hall
effect in 4𝑑 and 5𝑑 transition metals, Phys. Rev. B 83, 174405
(2011).
[54] Y. Wang, P. Deorani, X. Qiu, J. H. Kwon, and H. Yang, Determination of intrinsic spin Hall angle in Pt, Applied Physics
Letters 105, 152412 (2014).
[55] J. Zhou, J. Qiao, A. Bournel, and W. Zhao, Intrinsic spin Hall
conductivity of the semimetals MoTe2 and WTe2 , Phys. Rev. B
99, 060408(R) (2019).
[56] J. Li, H. Jin, Y. Wei, and H. Guo, Tunable intrinsic spin Hall
conductivity in bilayer PtTe2 by controlling the stacking mode,
Phys. Rev. B 103, 125403 (2021).
[57] Y. Sun, Y. Zhang, C.-X. Liu, C. Felser, and B. Yan, Dirac nodal
lines and induced spin Hall effect in metallic rutile oxides, Phys.
Rev. B 95, 235104 (2017).
[58] W. Zhang and Z. Lu, Raw data associated with the manuscript
"strain- induced nonrelativistic altermagnetic spin splitting effect", 10.5281/zenodo.15359109 (2025).


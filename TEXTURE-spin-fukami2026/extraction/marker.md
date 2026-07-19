<!-- extracted via pdftotext | arxiv:2605.18009 | 2026-07-19T04:40:35Z -->
Multi-rotational switching in a noncollinear antiferromagnet
by spin-orbit torque
Yuma Sato1,2, Yutaro Takeuchi3,4*, Yuta Yamane1,5*, Shun Kanai1,2,4,6,7,8,
and Shunsuke Fukami 1,2,4,8,9,10*
1

2

Department of Electronic Engineering, Graduate School of Engineering, Tohoku University,
Sendai 980-8579, Japan
3

4
5

Research Center for Magnetic and Spintronic Materials, National Institute for Materials
Science, Tsukuba 305-0047, Japan

WPI-Advanced Institute for Materials Research, Tohoku University, Sendai 980-8577, Japan

Frontier Research Institute for Interdisciplinary Sciences, Tohoku University, Sendai 980-8578,
Japan
6

Division for the Establishment of Frontier Sciences of Organization for Advanced Studies,
Tohoku University, Sendai 980-8577, Japan
7

8
9

Laboratory for Nanoelectronics and Spintronics, Research Institute of Electrical
Communication, Tohoku University, Sendai 980-8577, Japan

National Institutes for Quantum Science and Technology, Takasaki 370-1292, Japan

Center for Science and Innovation in Spintronics, Tohoku University, Sendai 980-8577, Japan

Center for Innovative Integrated Electronic Systems, Tohoku University, Sendai 980-8572, Japan
10

Inamori Research Institute for Science, Kyoto 600-8411, Japan

*e-mail: TAKEUCHI.Yutaro@nims.go.jp, yuta.yamane.e8@tohoku.ac.jp,
s-fukami@riec.tohoku.ac.jp

Abstract
Spintronics has advanced through discoveries of various electrically-driven spin
dynamics in nanomagnets. Here, we report a novel switching dynamics of spin systems
driven by spin-orbit torque, using a noncollinear antiferromagnetic nanodot. With electric
pulses spanning a wide range of durations and amplitudes, we find an unconventional
insensitivity of a threshold current density to pulse duration in switch-back events. This
observation is attributed to a previously unrecognized process, in which the noncollinear
antiferromagnetic order undergoes multiple rotations before completing reversal – a
phenomenon we term multi-rotational switching. Our theoretical analysis reveals that
multi-rotational switching arises from the interplay of three key factors: current-driven
coherent rotation of the noncollinear antiferromagnetic order, field-induced reorientation
of the uncompensated net magnetization, and thermal fluctuations. These findings
establish a microscopic mechanism governing current-induced switching in noncollinear
antiferromagnets, a topic of growing interest for next-generation spintronics technologies,
opening a new route to controlling antiferromagnetic order in nanodevices.

Introduction
Antiferromagnets (AFMs) exhibit rich and fascinating spin physics, and are expected to
play important roles in next-generation information technologies1–4. Their spin structures
are inherently robust against external magnetic disturbances owing to their vanishingly
small net magnetization. Moreover, their inertial spin dynamics and exchange-enhanced
frequencies enable device operations that are faster and more energy efficient than those
of conventional magnetic systems5–8. Among various classes of AFMs, noncollinear
AFMs represented by Mn3X (X = Sn, Ge and so on) have attracted particular interest in
spintronics. They are characterized by a triangular spin order, that is, a noncollinear AFM
order, realized on the stacked Kagome lattice formed by Mn ions. Noncollinear AFMs
not only enjoy the general advantages of AFMs, but also host a variety of exotic
phenomena associated with their topological electronic band structures and the magnetic
symmetry of the noncollinear AFM order9–21.
Manipulation of AFM order is a key requirement for AFM-based technologies.
Recent studies have demonstrated that noncollinear AFM order can be driven into
continuous rotational motion by all-electrical means7,22,23, exploiting spin-orbit torque
(SOT)24–27. This phenomenon is understood based on angular-momentum transfer from
injected spin currents to the rotational dynamics of the noncollinear AFM order28–30.
Deterministic bipolar switching of noncollinear AFM order utilizing SOT has also been
reported with the assistance of an in-plane magnetic field, where the switching polarity is
set by the directions of the current and the field31–36. This SOT-switching scheme
superficially resembles its ferromagnetic counterpart, although the equation of motion
governing noncollinear AFM order differs fundamentally from that of ferromagnetic
magnetization7,28,30,35,37. Several mechanisms have been proposed to explain this bipolar
SOT switching in both epitaxial7,22,32,35 and polycrystalline31,33,34,38 thin films. For
epitaxial films, which are particularly important for uncovering the fundamental aspects
of noncollinear AFM dynamics, the observed switching has been attributed to a
competition between current-driven rotation of the noncollinear AFM order and fieldinduced reorientation of the uncompensated net magnetization7,22,32,35. Despite these
extensive studies, the microscopic dynamics of noncollinear AFM order underlying the
bipolar SOT switching remain incompletely understood, limiting further exploration of
the functional potential of noncollinear AFMs.
Here we reveal a previously unrecognized dynamical mode of noncollinear AFM
order that emerges in bipolar SOT switching. Using a noncollinear AFM nanodot, we
observe an unconventional switching phase diagram as a function of current-pulse

duration and amplitude, in which the switching-back threshold current density depends
only weakly on the pulse duration. We show that this is explained by the spatial
asymmetry introduced by the in-plane field, combined with SOT and thermal fluctuations,
causing the noncollinear AFM order to undergo multiple rotations before completing the
switching. We refer to this phenomenon as multi-rotational switching. The experimental
observations are well captured by a theoretical model we develop, which reproduces the
key features of the switching phase diagram. Our finding of multi-rotational switching
sheds new light on the microscopic process underlying the SOT switching of AFM order,
and opens a pathway to novel device concepts enabled by AFM-based SOT, including
robust switching over a wide range of pulse durations, from nanoseconds to milliseconds
and beyond.

Sample fabrication and characterization
To investigate single-domain noncollinear AFM dynamics, we fabricate a
heterostructure incorporating a nanodot of Mn 3 Sn (Fig. 1a). The stack structure
consists of W(2 nm)/Ta(3 nm)/Mn₃Sn(20 nm)/MgO(1.3 nm)/Ru(1 nm), deposited
on a MgO (110) substrate by magnetron sputtering. The epitaxial Mn 3 Sn film
exhibits (11#00)-plane, or M-plane, crystallographic orientation 22,35,39 , where the
Kagome planes in Mn 3 Sn are perpendicular to the film plane. The stack is
processed into a Hall device with a Mn 3 Sn nanodot formed on a cross-shaped W/Ta
channel 7,40 . The nominal dot diameter is 200 nm, and the channel width and length
are 250 nm and 600 nm, respectively. Displayed in Fig. 1b is an image of the
fabricated nanodot sample, captured by scanning electron microscopy. See
Materials and methods for more details about sample preparation.
To confirm the noncollinear AFM order in our Mn 3 Sn nanodot, we measure
the anomalous Hall resistance 𝑅! as a function of the out-of-plane field 𝐻" (Fig.
1c). We then establish the SOT-driven rotation and the field-assisted bipolar
switching of the noncollinear AFM order in the DC regime. Figure 1d shows 𝑅!
as a function of 𝐽!# , the current density in the heavy metal (W/Ta) layers, under
various in-plane fields 𝐻$ applied parallel to the current. With 𝐻$ = 0 , the
fluctuation in 𝑅! is observed above sufficiently large 𝐽!# , arising from the SOTdriven continuous rotation of the noncollinear AFM order22 . When a nonzero 𝐻$
is applied, bipolar switching of 𝑅! is observed. The threshold current density
decreases with increasing 𝐻$ , and the switching polarity depends on the sign of

𝐻$ . This switching behaviour can be attributed to the SOT-driven rotation of the
noncollinear AFM order being balanced by 𝐻$ , which favors alignment of the
uncompensated net magnetization along its direction 32 .

Switching probability measurements
Next, we perform switching experiments using current pulses with pulse duration 𝜏%
ranging from 5 ns to 5 ms, along with a DC in-plane magnetic field (Fig. 1a). Before each
pulse, the Mn3Sn nanodot is initialized to the “down” state, where 𝑅! < 0. The nanodot
is considered “switched” when the post-pulse state is “up” (𝑅! > 0). See Materials and
methods and Supplementary Figs. 1 and 2 for more details on the experimental procedure.
Figures 2a-d show the switching probability 𝑃 as a function of 𝐽!# , under
𝜇& 𝐻$ = 100 mT and for four different 𝜏% . Here, 𝑃 is defined as the ratio of successful
switching events out of 60 pulse applications and 𝜇& is the vacuum permeability. A
common trend across all four cases is that 𝑃 initially increases with 𝐽!# and reaches
unity. With further increase in 𝐽!# , 𝑃 starts to decrease and asymptotically approaches
0.5. We define the critical current density 𝐽'( (𝐽') ) as the current density at which P first
touches 0.5 (0.75) during the switching (switching-back) process for a given 𝜏% . The
asymmetry between the critical currents for the switching and switching-back arises from
the broken ±𝑥 symmetry due to 𝐻$ . In the present configuration, 𝐻$ assists the downto-up rotation of the noncollinear AFM order (switching) while it opposes the up-to-down
(switching-back)41.
The dependence of 𝑃 on (𝐽!# , 𝜏% ) for the case of 𝜇& 𝐻$ = 100 mT is
summarized by the two-dimensional color map in Fig. 2e. (The magnetic-field
dependence of the switching properties will be discussed later.) It is observed that 𝐽'(
decreases with increasing 𝜏% , whereas 𝐽') is largely insensitive to 𝜏% . The 𝜏%
dependence of 𝐽'( can be readily understood: with thermal fluctuations, a longerduration pulse increases the probability of thermally-assisted switching. A similar pulseduration dependence of the switching current has also been reported in ferromagnets26,42.
In contrast, the weak 𝜏% dependence of 𝐽') defies such a straightforward explanation,
with no comparable phenomenon known in ferromagnets. In what follows, we discuss the
microscopic origin of this unconventional switching behaviour.

Numerical simulation and theoretical modelling
We model the Mn3Sn nanodot by a three-sublattice AFM with each sublattice (A, B, and
C) carrying the same saturation magnetization 𝑀* . The sublattice magnetizations 𝒎+ ,
𝒎, , and 𝒎- are assumed to obey the coupled Landau–Lifshitz–Gilbert (LLG)
equations43, with thermal fluctuations incorporated according to the fluctuationdissipation theorem44. In general, the noncollinear AFM order formed by the sublattice
magnetizations in Mn3Sn can be described by two Néel vectors37, or equivalently a cluster
octupole moment45. Since all sublattice magnetizations are well confined in the Kagome
planes, however, the noncollinear AFM order can be represented by a single Néel vector
𝒏=

𝒎! /𝒎" 0)𝒎# 28,30
1√)

. The three sublattice magnetizations maintain nearly 120°

orientations with each other, ensuring that √2|𝒏| ≃ 1. See Materials and methods for
further details of our model and calculations. Figure 2f shows the calculated switching
probability 𝑃(𝐽!# , 𝜏% ) from the down (√2𝑛" ≃ −1) to up (√2𝑛" ≃ +1) state, obtained
by numerically solving the coupled LLG equations with 𝜇& 𝐻$ = 100 mT and 𝜏%
ranging from 2 ns to 100 ns. Here, 𝑃 is defined in the same way as in Fig. 2e. The
simulation successfully reproduces the experimentally observed trends of 𝐽'( and 𝐽')
as functions of (𝐽!# , 𝜏% ).
To understand the origin of the weak 𝜏% dependence of 𝐽') , we now develop a
theoretical model of the Néel vector dynamics. Figure 2g summarizes the key results of
our analysis, the derivation of which is presented in the following. Specifically, the
switched region between 𝐽'( and 𝐽') (the red region in Fig. 2f) will be shown to consist
of two sub-regimes (Fig. 2g), separated by an additional threshold current density 𝐽34567
defined below. It will become clear that, in the region between 𝐽34567 and 𝐽') , the Néel
vector undergoes multiple rotations before completing the reversal, that is, multirotational switching, and that the observed insensitivity of 𝐽') to 𝜏% is rooted in the
nature of this multi-rotational switching. These findings convey a central message of this
work.
We introduce an angular variable 𝜃 as in the inset of Fig. 3a. The coupled LLG
equations for the three sublattice magnetizations are reduced to the equation of motion
for 𝜃 7,28,30
1 𝜕)𝜃
𝜕𝜃 𝛾𝐻9
𝑀:= −𝛼
−
sin 2𝜃 − 𝛾𝐻$
cos 𝜃 − 𝛾𝐷* 𝐽!# + 𝐹6< (𝑇).
)
𝛾𝐻8 𝜕𝑡
𝜕𝑡
2
3𝑀;

(1)

We outline a derivation of Eq. (1) in Materials and methods. Here, the left-hand side

represents the inertial term, with 𝛾 denoting the gyromagnetic ratio and 𝐻8 the
effective field associated with the antiferromagnetic exchange coupling. The right-hand
side contains five “forces” originating from: (1) the damping torques with 𝛼 the Gilbert
damping constant, (2) the global uniaxial anisotropy characterized by the effective field
𝐻9 , (3) Larmor torques from the external field 𝐻$ with 𝑀=' the uncompensated net
magnetization, (4) the SOT with 𝐷* a constant describing the Slonczewski-like torque,
and (5) thermal fluctuations with 𝐹6< (𝑇) the Langevin force and 𝑇 the sample
temperature. The Néel vector dynamics is, therefore, mathematically equivalent to that of
a point mass 𝑚 = (𝛾𝐻8 )0( subject to the frictional (𝛼), stochastic, and conservative
forces, with the latter arising from a tilted-washboard potential
𝑢(𝜃) =

>?$
)

@

sin) 𝜃 + 𝛾𝐻$ 1@%# sin 𝜃 + 𝛾𝐷* 𝐽!# 𝜃,

(2)

&

given in the unit of angular frequency. Under the condition

>?$
)

@

≫ 𝛾𝐻$ 1@%# , the first two
&

terms stabilize the up state (𝜃 = 2𝑛𝜋) and the down state [𝜃 = (2𝑛 − 1)𝜋] by
creating asymmetric potential barriers between them (Fig. 3a), where 𝑛 is an integer.
With 𝐻$ > 0, the barrier 𝛥ABCD→4F , for the “right-going” down-to-up transition, is
lower than 𝛥4F→ABCD , for the “right-going” up-to-down. The last term in Eq. (2), linear
in 𝜃, introduces a global tilt to the potential. Notice that 𝐷* < 0 for our system due to
the negative sign of the effective spin Hall angle of Ta/W underlayer (see Materials and
methods). Both 𝛥ABCD→4F and 𝛥4F→ABCD decrease with increasing 𝐽!# (≥ 0) , and
vanish at

(

(

@

%#
∗
𝐽!# ≈ 𝐽'(
≡ |I | X) 𝐻9 − 1√)@
𝐻$ Y
'

&

and

(

(

@

%#
∗
𝐽')
≡ |I | X) 𝐻9 + 1√)@
𝐻$ Y,
'

&

respectively.
In the framework of Eq. (2), 𝐽'( corresponds to the current density at which
𝛥ABCD→4F is sufficiently reduced for the down-to-up transition to become thermally
activated, causing 𝑃 to reach 0.5, while 𝛥4F→ABCD remains too large to be overcome.
This is schematically illustrated in Fig. 3a. Starting from the initial state 𝜃 = 𝜋, the
octupole moment passes through the barrier 𝛥ABCD→4F with thermal assistance and
settles in the up state 𝜃 = 2𝜋, completing a 𝜋 switching. Figure 3b displays a result of
the LLG simulation, showcasing a representative example of the Néel vector dynamics
corresponding to Fig. 3a. The plot shows the time evolutions of the z component of the
Néel vector (normalized to unity) for 𝜏% = 10 ns and 𝜇& 𝐻$ = 100 mT. At zero
∗
temperature, 𝐽'( coincides with 𝐽'(
.

∗
As 𝐽!# is further increased beyond 𝐽'(
such that 𝛥4F→ABCD is sufficiently

lowered, the down-to-up transition becomes dominated by coherent SOT driving,
whereas the up-to-down transition is thermally activated (Fig. 3c): The Néel vector
therefore experiences multiple rotations during a pulse. Once a thermally-assisted up-todown transition occurs (e.g., 2𝜋-to-3𝜋), the Néel vector is immediately driven back to the
up state (4𝜋) by SOT. Consequently, the Néel vector predominantly resides in the up state
during the pulse, resulting in a high probability of being found in the up state after the
pulse. A result of the LLG simulation corresponding to Fig. 3c is shown in Fig. 3d.
We define 𝐽34567 as the current density at which the probability 𝑃J of a single
π rotation drops to 0.5 due to the onset of multiple rotations. (Switching events involving
𝜋, 3𝜋, 5𝜋, … rotations are all counted in 𝑃, whereas only the 𝜋 rotation contributes to
𝑃J .) The regime 𝐽34567 ≤ 𝐽!# < 𝐽') is thus identified as the multi-rotational switching
regime (Fig. 2g), where 𝑃 ≅ 1 while 𝑃J ≪ 1 over most of this regime. Accordingly,
the switched regime (𝐽'( ≤ 𝐽!# < 𝐽') ) consists of two distinct sub-regimes: the 𝜋switching regime (𝐽'( ≤ 𝐽!# < 𝐽34567 where 𝑃J ≅ 1) and the multi-rotational
switching regime (𝐽34567 ≤ 𝐽!# < 𝐽') where 𝑃J ≪ 1). The former follows a
thermally-assisted mechanism analogous to that in ferromagnets, whereas the latter
reveals a distinctive dynamical mode characteristic of AFMs.
∗
Once 𝐽!# exceeds 𝐽')
, both potential barriers disappear, and 𝜃 undergoes
continuous downhill motion (Fig. 3e). The corresponding Néel vector dynamics is a
continuous coherent rotation primarily driven by SOT (Fig. 3f). The numerically obtained
∗
𝐽') is well reproduced by the analytical 𝐽')
(Fig. 2g). Establishing a rigorous theoretical
∗
connection between 𝐽') and 𝐽') is nontrivial, since the latter is defined through the
switching probability at finite temperature. Nonetheless, the close quantitative agreement
∗
between 𝐽')
and 𝐽') , for the parameter values relevant to a Mn3Sn nanodot, strongly
indicates that the weak 𝜏% dependence of 𝐽') originates from the transition between
multi-rotational switching and coherent rotation: Once the potential barriers vanish, the
Néel vector rotates freely without thermal activation, making the switching threshold
essentially independent of pulse duration.

We now revisit the numerical result for the switching probability 𝑃(𝐽!# , 𝜏% )
(Fig. 2f), and decompose it into the probabilities 𝑃()L0()J of (2𝑛 − 1)𝜋 rotations.
Figure 4a shows 𝑃J as a function of (𝐽!# , 𝜏% ), where 𝑃J ≅ 1 within the 𝜋-switching
regime (𝐽'( ≤ 𝐽!# < 𝐽34567 ). Correspondingly, 𝑃()L0()J for 𝑛 > 1 attain
appreciable values for 𝐽34567 ≤ 𝐽!# (Figs. 4b and c). The summation ∑LN( 𝑃()L0()J of
the switching probabilities with multiple rotations is plotted in Fig. 4d: It reaches unity

in the regime 𝐽34567 ≤ 𝐽!# < 𝐽') , confirming that the switching in this regime takes
place overwhelmingly via the multi-rotational switching. In the coherent-rotation regime
(𝐽') ≤ 𝐽!# ) , ∑LN( 𝑃()L0()J asymptotically approaches 0.5 from above as 𝐽!#
increases. This is because Néel vector dynamics is so rapid (Fig. 3f) that the final state,
up or down, becomes effectively stochastic, as the thermal fluctuation spoils the time
coherence in the Néel vector dynamics. Perfect coherence is restored at zero-temperature
for 𝐽') ≤ 𝐽!# 7. The results in Fig. 4 clearly demonstrate, once again, that for 𝐽'( ≤ 𝐽!# ,
Néel vector dynamics under SOT and an in-plane field falls into the three distinct regimes.

Magnetic-field dependence of switching properties
Finally, we investigate the magnetic-field dependence of the switching behaviour. Figures
5a-c show the experimental 𝑃(𝐽!# , 𝜏% ) for three different values of 𝐻$ . As 𝐻$
increases, 𝐽'( and 𝐽') are shifted overall downwards and upwards, respectively. This is
understood as 𝛥ABCD→4F (𝛥4F→ABCD ) is lowered (raised) by 𝐻$ , which is consistent
with what is predicted from Eq. (2). This trend is well reproduced by the LLG simulations
(Figs. 5d-f). In Fig. 5g, the open circles represent the experimental 𝐽####
') (𝐻$ ), defined as
the 𝜏% -averaged 𝐽') (𝜏% , 𝐻$ ), with the error bars indicating the standard deviation. The
∗
numerically obtained 𝐽####
') (𝐻$ ) (open squares with error bars) and the theoretical 𝐽')
(solid line) are also shown. The close quantitative agreement among these three datasets
provides strong additional support for the validity of our theoretical model. No switched
regime is experimentally observed under zero magnetic field (Materials and methods and
Supplementary Fig. 3), confirming that both the 𝜋 switching and multi-rotational
switching require the asymmetric potential barriers arising from the in-plane field.

Summary
We have revealed multi-rotational switching, a novel dynamical mode at play in the SOT
switching of noncollinear AFM order, in a nanodot device. The unconventional switching
behaviour experimentally observed is well reproduced by numerical simulations, and the
underlying physics is captured by our theoretical modelling of Néel vector dynamics
under an effective potential energy landscape. Since the factors necessary for multirotational switching, namely SOT-driven rotation of the AFM order, field-induced
reorientation of the magnetization and thermal fluctuations, are universally expected in
easy-plane AFMs, the discovered mechanism is broadly relevant to a wide range of
spintronic systems of current interest.
The multi-rotational switching reported in this work enables reliable operation
of SOT devices across a broad area in the (𝐽!# , 𝜏% ) space, owing to the thermal
robustness of 𝐽') and its tunability via an external magnetic field. The insensitivity of
𝐽') to thermal disturbance, and thus to 𝜏% , also points to the potential for a single AFM
device to function as both a memory element and an oscillator. This dual functionality
can be accessed by simply tuning 𝐽!# below 𝐽') (memory mode) or above 𝐽')
(oscillator mode). The thermal robustness of 𝐽') is further demonstrated by numerical
simulations, by confirming its insensitivity to sample size, as shown in Materials and
methods and Supplementary Fig. 4.

Fig. 1. Schematic and characterizations of the Mn3Sn nanodot sample. a, SOT
switching of the noncollinear AFM order in the Mn3Sn nanodot, with the orange arrow
indicating the Néel vector. b, Scanning electron microscope image of the fabricated Hall
device. c, 𝑅? -𝐻" curve for the Mn3Sn nanodot. d, 𝑅? -𝐽!# curves in DC experiments
(the current pulse duration being 100 ms) with various in-plane magnetic field 𝐻$ , where
𝜇& is the vacuum permeability.

Fig. 2. Switching probability measurements. a-d, 𝑃 versus 𝐽!# with four different
𝜏O . e-f, Two-dimensional mappings of 𝑃(𝐽!# , 𝜏O ) with 𝜇& 𝐻$ = 100 mT, obtained by
experiment (e) and simulation (f). g, Phase diagram identifying the three distinct
switching regimes for the numerical result in f.

Fig. 3. Theoretical and numerical analyses on the SOT switching of the Néel vector.
Schematic illustrations of Néel vector dynamics based on the analytical model with Eqs.
(1) and (2) in the 𝜋-switching regime (a), the multi-rotational switching regime (c), and
the coherent rotation regime (e). The unit of 𝑢(𝜃) is arbitrary. Numerical simulations for
the time evolution of the Néel vector in the corresponding regimes are shown in (b), (d)
and (f). In the simulation, the current pulse is applied from 5 ns to 15 ns and 𝜇& 𝐻$ =
100 mT.

Fig. 4. Numerical results for the probabilities of multiple rotations of the Néel vector.
a-c, Probabilities of the Néel vector completing 𝜋 (a), 3𝜋 (b) and 5𝜋 (c) rotations, as
functions of 𝐽!# and 𝜏O . d, Summation of the probabilities of 3𝜋 , 5𝜋 , 7𝜋 , …
rotations, corresponding to the probability of multi-rotational switching.

Fig. 5. Magnetic-field dependence of the switching properties. a-f, 𝑃(𝐽!# , 𝜏O ) for
three different 𝐻$ , obtained by experiment (a-c) and simulation (d-f). g, 𝐻$ dependence
∗
of the experimental and numerical 𝐽####
') and the theoretical 𝐽') . The error bars indicate
the standard deviation.

References
1. T. Jungwirth, X. Marti, P. Wadley, and J. Wunderlich, “Antiferromagnetic spintronics,”
Nat. Nanotechnol. 11, 231–241 (2016).
2. V. Baltz et al., “Antiferromagnetic spintronics,” Rev. Mod. Phys. 90, 015005 (2018).
3. J. Železný, P. Wadley, K. Olejník, A. Hoffmann, and H. Ohno, “Spin transport and spin
torque in antiferromagnetic devices,” Nat. Phys. 14, 220–228 (2018).
4. J. Han, R. Cheng, L. Liu, H. Ohno, and S. Fukami, “Coherent antiferromagnetic
spintronics,” Nat. Mater. 22, 684–695 (2023).
5. A. V. Kimel et al., “Inertia-driven spin switching in antiferromagnets,” Nat. Phys. 5,
727–731 (2009).
6. K. Olejník et al., “Terahertz electrical writing speed in an antiferromagnetic memory,”
Sci. Adv. 4, eaar3566 (2018).
7. Y. Takeuchi et al., “Electrical coherent driving of chiral antiferromagnet,” Science 389,
830–834 (2025).
8. H. Tsai et al., “Picosecond ultralow-power switching device based on an
antiferromagnet,” Science 392, 761–765 (2026).
9. H. Chen, Q. Niu, and A. H. MacDonald, “Anomalous Hall effect arising from
noncollinear antiferromagnetism,” Phys. Rev. Lett. 112, 017205 (2014).
10. J. Kübler and C. Felser, “Non-collinear antiferromagnets and the anomalous Hall
effect,” EPL 108, 67001 (2014).
11. S. Nakatsuji, N. Kiyohara, and T. Higo, “Large anomalous Hall effect in a noncollinear antiferromagnet at room temperature,” Nature 527, 212–215 (2015).
12. A. K. Nayak et al., “Large anomalous Hall effect driven by a nonvanishing Berry
curvature in the noncollinear antiferromagnet Mn3Ge,” Sci. Adv. 2, e1501870 (2016).
13. X. Li et al., “Anomalous Nernst and Righi-Leduc effects in Mn3Sn: Berry curvature
and entropy flow,” Phys. Rev. Lett. 119, 056601 (2017).
14. J. Liu and L. Balents, “Anomalous Hall effect and topological defects in
antiferromagnetic Weyl semimetals: Mn3Sn/Ge,” Phys. Rev. Lett. 119, 087202 (2017).
15. W. Feng, G.-Y. Guo, J. Zhou, Y. Yao, and Q. Niu, “Large magneto-optical Kerr effect

in noncollinear antiferromagnets Mn3X (X = Rh, Ir, Pt),” Phys. Rev. B 92, 144426 (2015).
16. T. Higo et al., “Large magneto-optical Kerr effect and imaging of magnetic octupole
domains in an antiferromagnetic metal,” Nat. Photonics 12, 73–78 (2018).
17. M. Ikhlas et al., “Large anomalous Nernst effect at room temperature in a chiral
antiferromagnet,” Nat. Phys. 13, 1085–1090 (2017).
18. J. Železný et al., “Spin-polarized current in noncollinear antiferromagnets,” Phys. Rev.
Lett. 119, 187204 (2017).
19. M. Kimata et al., “Magnetic and magnetic inverse spin Hall effects in a non-collinear
antiferromagnet,” Nature 565, 627–630 (2019).
20. X. Chen et al., “Octupole-driven magnetoresistance in an antiferromagnetic tunnel
junction,” Nature 613, 490–495 (2023).
21. J. Han et al., “Room-temperature flexible manipulation of the quantum-metric
structure in a topological chiral antiferromagnet,” Nat. Phys. 20, 1110–1117 (2024).
22. Y. Takeuchi et al., “Chiral-spin rotation of non-collinear antiferromagnet by spin–
orbit torque,” Nat. Mater. 20, 1364–1370 (2021).
23. G. Q. Yan et al., “Quantum sensing and imaging of spin–orbit-torque-driven spin
dynamics in the non-collinear antiferromagnet Mn3Sn,” Adv. Mater. 34, 2200327 (2022).
24. A. Manchon and S. Zhang, “Theory of nonequilibrium intrinsic spin torque in a single
nanomagnet,” Phys. Rev. B 78, 212405 (2008).
25. I. M. Miron et al., “Perpendicular switching of a single ferromagnetic layer induced
by in-plane current injection,” Nature 476, 189–193 (2011).
26. L. Liu et al., “Spin-torque switching with the giant spin Hall effect of tantalum,”
Science 336, 555–558 (2012).
27. S. Fukami, T. Anekawa, C. Zhang, and H. Ohno, “A spin–orbit torque switching
scheme with collinear magnetic easy axis and current configuration,” Nat. Nanotechnol.
11, 621–625 (2016).
28. E. V. Gomonay and V. M. Loktev, “Using generalized Landau-Lifshitz equations to
describe the dynamics of multi-sublattice antiferromagnets induced by spin-polarized
current,” Low Temp. Phys. 41, 698 (2015).
29. H. Fujita, “Field-free, spin-current control of magnetization in non-collinear chiral

antiferromagnets,” Phys. Status Solidi RRL 11, 1600360 (2017).
30. Y. Yamane, O. Gomonay, and J. Sinova, “Dynamics of noncollinear antiferromagnetic
textures driven by spin current injection,” Phys. Rev. B 100, 054415 (2019).
31. H. Tsai et al., “Electrical manipulation of a topological antiferromagnetic state,”
Nature 580, 608–613 (2020).
32. T. Higo et al., “Perpendicular full switching of chiral antiferromagnetic order by
current,” Nature 607, 474–479 (2022).
33. B. Pal et al., “Setting of the magnetic structure of chiral kagome antiferromagnets by
a seeded spin-orbit torque,” Sci. Adv. 8, eabo5930 (2022).
34. G. K. Krishnaswamy et al., “Time-dependent multistate switching of topological
antiferromagnetic order in Mn3Sn,” Phys. Rev. Appl. 18, 024064 (2022).
35. J.-Y. Yoon et al., “Handedness anomaly in a non-collinear antiferromagnet under
spin–orbit torque,” Nat. Mater. 22, 1106–1113 (2023).
36. Y. Kobayashi, Y. Shiota, H. Narita, T. Ono, and T. Moriyama, “Pulse-width
dependence of spin–orbit torque switching in Mn3Sn/Pt thin films,” Appl. Phys. Lett. 122,
122405 (2023).
37. A. F. Andreev and V. I. Marchenko, “Symmetry and the macroscopic dynamics of
magnetic materials,” Sov. Phys. Usp. 23, 21 (1980).
38. Z. Zhou et al., “Field-free full switching of chiral antiferromagnetic order,” Nature
651, 341–347 (2026).
39. J. Yoon et al., “Crystal orientation and anomalous Hall effect of sputter-deposited
non-collinear antiferromagnetic Mn3Sn thin films,” Appl. Phys. Express 13, 013001
(2019).
40. Y. Sato et al., “Thermal stability of non-collinear antiferromagnetic Mn3Sn nanodot,”
Appl. Phys. Lett. 122, 122404 (2023).
41. A. Shukla, S. Qian, and S. Rakheja, “Impact of strain on the SOT-driven dynamics of
thin film Mn3Sn,” J. Appl. Phys. 135, 123903 (2024).
42. R. H. Koch, J. A. Katine, and J. Z. Sun, “Time-resolved reversal of spin-transfer
switching in a nanomagnet,” Phys. Rev. Lett. 92, 088302 (2004).
43. E. M. Lifshitz and L. P. Pitaevskii, Statistical Physics, Course of Theoretical Physics

Vol. 9, Pt. 2 (Pergamon, Oxford, 1980).
44. W. F. Brown, “Thermal fluctuations of a single-domain particle,” Phys. Rev. 130,
1677–1686 (1963).
45. M.-T. Suzuki, T. Koretsune, M. Ochi, and R. Arita, “Cluster multipole theory for
anomalous Hall effect in antiferromagnets,” Phys. Rev. B 95, 094406 (2017).

Materials and methods
Sample preparation
The MgO layer was deposited by RF sputtering at room temperature, while W, Ta, Mn3Sn,
and Ru layers were deposited by DC sputtering at 400 °C on a heated stage. The deposited
stack was annealed at 500 °C for an hour in a vacuum. The buffer layer W(2 nm)/Ta(3
nm) is for epitaxial growth of the M-plane oriented hexagonal D019-Mn3Sn22,39. The
structural properties of our sample are similar to those in our previous study7. The stack
was processed into a Hall device using electron beam lithography and Ar ion milling. To
protect the channel layer, we deposited Ta(3 nm)/Ru(1 nm) films after the fabrication of
the Mn3Sn nanodot. The coplanar waveguide and contact pads made of Cr(5 nm)/Au(100
nm) electrodes were formed after fabricating the channel.

DC measurements
In the DC-regime measurements (Fig. 1c and d), a current source (Yokogawa; Model
GS200) was used for electric current application into the channel. The Hall voltage was
measured using a voltmeter (Keithley; Model 2182A) with a DC current of 0.1 mA,
corresponding to 𝐽!# = 4.26 MA cm-2. The shunt current was estimated by a method
we reported in our previous study7. The 𝑅! - 𝐻" hysteresis curve was obtained by
sweeping 𝐻" at a rate of 10 mT/s. For the 𝑅! -𝐽!# measurement, we injected a 100 mspulse from the current source.

Switching probability measurement
In the switching probability measurements (Fig. 2a-e and Fig. 5a-c), pulse and DC
voltages were applied into the channel from a function generator (Keysight; Model
81160). The Hall voltage was measured by a voltmeter (Keithley; Model 2182A) in the
presence of a DC voltage of 30 mV, corresponding to 𝐽!# = 3.42 MA cm-2. The
transmitted waveforms of the applied pulse and DC voltages were monitored using an
oscilloscope (Agilent; Model DSOX93204A) connected to the output side of the
waveguide. Supplementary Fig. 1 shows the measured waveforms of the applied voltage
( 𝑉P*' ) for four different 𝜏O . The amplitude of the pulse current is determined by
𝑉P*' /𝑅P*' , where 𝑅P*' (= 50 Ω) is the internal impedance of the oscilloscope.
The procedure of the switching-probability measurement is schematically shown in
Supplementary Fig. 2a. First, the octupole state in the Mn3Sn nanodot was initialized to
a low 𝑉! state by a pulse with 𝐽!# = −55 MA cm-2 and 𝜏O = 5 ms, under an in-plane
magnetic field. The histogram of the measured 𝑉! after the initialization is displayed in
Supplementary Fig. 2b, which confirms the successful initialization with no writing error.
Next, the writing pulse was applied and then 𝑉! was measured. This whole sequence
was repeated 60 times to evaluate 𝑃 for given (𝐽!# , 𝜏O ). Supplementary Figs. 2c-f show
the distributions of 𝑉! against 𝐽!# for 𝜏% = 5 ns, 500 ns, 50 𝜇s and 5 ms, respectively,
with 𝜇& 𝐻$ = 200 mT. The gap between the high and low values of 𝑉! is sufficiently
large for an unambiguous evaluation of 𝑃.

Numerical simulation
We model our Mn3Sn nanodot by the following magnetic energy density
)

𝑢 = 𝐽& h 𝒎Q ∙ 𝒎R − 𝐷& 𝒆T ∙ h 𝒎Q × 𝒎R − 𝐾 h m𝒎Q ∙ 𝒆9,Q n
Q,R

Q,R

−

QU+,,,-

𝐾"
)
h m𝒎Q ∙ 𝒆9",Q n − 𝑀V 𝑯 ∙ h 𝒎Q
3
QU+,,,-

where

𝐽&

(3),

QU+,,,-

𝐷&

is the antiferromagnetic exchange coupling constant,

is the

Dzyaloshinskii-Moriya coupling constant, 𝐾 is the uniaxial anisotropy constant
originating from the local crystalline symmetry, 𝐾" represents the global uniaxial
anisotropy induced predominantly by the interface, and 𝑯 is the external magnetic field.
The unit vectors 𝒆9,Q and 𝒆9",Q , representing the easy axes of the anisotropies, are given
𝟏

√𝟑

𝟏

√𝟑

𝟏

√𝟑

by 𝒆9,W = − 𝟐 𝒆$ + 𝟐 𝒆" , 𝒆9,[ = − 𝟐 𝒆$ − 𝟐 𝒆" , 𝒆9,' = 𝒆$ , 𝒆9",W = 𝟐 𝒆$ − 𝟐 𝒆" ,
√𝟑

𝟏

𝒆9",[ = − 𝟐 𝒆$ − 𝟐 𝒆" , and 𝒆9",' = 𝒆" . Here we set the 𝑥 , 𝑦 , and 𝑧 axes along
# 00], respectively, of Mn3Sn.
[112#0], [0001] and [11
The coupled LLG equations for the sublattice magnetizations are given by
𝜕𝒎Q
𝜕𝒎Q
= −𝛾𝒎Q × m 𝑯Q\]] + 𝑯Q6< n + 𝛼𝒎Q ×
− 𝛾𝐷V 𝐽!# 𝒎Q × (𝒎Q × 𝒔)
𝜕𝑡
𝜕𝑡

(4),

( ^_

where 𝑯Q\]] = − @ ^𝒎 is the effective magnetic field exerted on 𝒎Q , and 𝑯Q6<
(

)

Q,`
Q,`
Q,a
(𝑡′)〉 =
describes thermal fluctuations satisfying 〈 𝐻6< (𝑡)〉 = 0 and 〈 𝐻6< (𝑡) 𝐻6<
)bc* d

JI + f

(

g

𝛿 𝛿(𝑡 − 𝑡′) , with 𝜇, 𝜈 = 𝑥, 𝑦, 𝑧 , 𝑘[ the Boltzmann constant, 𝑉 =
>@ e `a

the

volume of the Mn3Sn nanodot, and 𝐷 and 𝑑 the diameter and thickness of the nanodot,
( ℏi

respectively. The last term in Eq. (4) represents the SOT with 𝐷V = 1 )j@',f and 𝜃*!
-

denoting the effective spin Hall angle. The factor 1/3 in 𝐷V reflects the sublattice
symmetry where the spin current injected into Mn3Sn is transferred equiprobably to each
of the three magnetic sublattices.
The antiferromagnetic order parameters for a noncollinear AFM can be constructed
as28,30
𝒏( =

𝒎W + 𝒎[ − 2𝒎'
3√2

,

𝒏) =

−𝒎W + 𝒎[
√6

Assuming the net magnetization to be sufficiently small as |𝒎| =

.

(5)

|𝒎. /𝒎* /𝒎/ |
1

≪ 1, it

is straightforward to show 𝒏( ∙ 𝒏) ≃ 0 and |𝒏( | ≃ |𝒏) | ≃ 1/√2. Therefore, tracking
either one of 𝒏( or 𝒏) is sufficient to capture the dynamics of the noncollinear AFM
order in Mn3Sn. 𝒏( can be interpreted as corresponding to the octupole moment, and in
the main text, we adopted the notation 𝒏 ≡ 𝒏( .
For the simulations discussed in the main text, we employed the following
parameters: 𝐽& = 8 × 10k Jm-3, 𝐷& = 6 × 10l Jm-3, 𝐾 = 2.5 × 10m Jm-3, 𝐾" = 9 ×
10) Jm-3, 𝑀V = 0.5 T, 𝛾 = 2.21 × 10m mA-1s-1, 𝛼 = 0.005, 𝜃*! = −0.1, 𝑑 = 20
nm, 𝐷 = 200 nm, and 𝑇 = 300 K.

Theoretical analysis
Our derivation of Eq. (1) in the main text follows Ref. [30]. Here we outline the derivation
briefly. We first rewrite the LLG equations (4) in terms of (𝒏( , 𝒏) , 𝒎), and introduce the
angular variable by 𝒏( =

𝟏
√𝟐

and 𝐷& > 0, one finds 𝒏) =

(sin 𝜃 , 0, cos 𝜃). Because of the conditions 𝒏( ∙ 𝒏) ≃ 0
𝟏
√𝟐

J

J

•sin X𝜃 + ) Y , 0, cos X𝜃 + ) Y€. Taking advantage of the

condition |𝒎| ≪ 1, a perturbative treatment of 𝒎 up to its first order leads to an
expression of 𝒎 as a function of 𝒏( 28,30. Putting all these together, we arrive at the
1n

)9

equation of motion for 𝜃 , that is Eq. (1), where 𝐻8 = @0 and 𝐻9 = 1@1 . The
-

@ 9

uncompensated net magnetization is given by 𝑀=' = n-

0

-

in equilibrium without an

external field.
∗
∗
𝐽'(
and 𝐽')
are derived from Eq. (2) as follows. A critical current density and the

corresponding critical angle 𝜃 ∗ are defined as (𝐽' , 𝜃) that simultaneously satisfy
𝜕i 𝑢 = 0 and 𝜕i) 𝑢 = 0. Assuming that |𝐻$ | is sufficiently small that it hardly affects
J 1J mJ kJ

𝜃 ∗ , we find 𝜃 ∗ ≅ g , g , g , g . The critical angle corresponding to the down-to-up
transition, with the initial state 𝜃 = 𝜋, is therefore

mJ
g

mJ

. Substituting 𝜃 = g to 𝜕i 𝑢 =

∗
∗
0, we reach the expression of 𝐽'(
given in the main text. 𝐽')
can be obtained in a similar

fashion considering the up-to-down transition.

Switching probability at zero field
Supplementary Fig. 3 shows the experimental 𝑃(𝐽!# , 𝜏O ) measured in the absence of
external magnetic field. There appears only one critical current density that separates the
non-switched (blue color) and the coherent rotation (green color) regimes. The absence
of the switched regime can also be derived analytically by setting 𝐻$ = 0 in Eq. (2).

Nanodot-diameter dependence of the switching probability
Supplementary Fig. 4 shows the calculated 𝑃(𝐽!# , 𝜏O ) with 𝜇& 𝐻$ = 100 mT for
different nanodot diameters 𝐷, corresponding to different levels of thermal fluctuation
(see the definition of the thermal fields 𝑯Q6< given above). As 𝐷 decreases, i.e., as
thermal fluctuations increase, 𝐽'( becomes lower. This is because the 𝜋 switching with
thermal assistance takes place more readily under stronger thermal fluctuations. In
contrast, 𝐽') is largely insensitive to thermal fluctuations, consistent with the physical
picture discussed in the main text.

!

"

#

$

Supplementary Fig. 1. Transmitted waveforms of the applied pulse voltages. The
transmitted voltage 𝑉6opDV with an input pulse voltage of 500 mV is plotted for four
different 𝜏O .

Supplementary Fig. 2. Scheme for the switching probability measurement. a,
Procedure of the switching probability measurement. b, Histogram of 𝑉! measured after
the initialization. c-f, Distribution of 𝑉! against 𝐽!# , measured after applications of the
writing pulse with four different 𝜏O .

Supplementary Fig. 3. Switching probability with no external field. The
experimentally observed 𝑃(𝐽!# , 𝜏O ) with 𝐻$ = 0.

Supplementary Fig. 4. Numerical results for the nanodot-diameter dependence of
the switching probability. 𝑃(𝐽!# , 𝜏O ) with 𝜇& 𝐻$ = 100 mT for three different
nanodot diameters 𝐷 are plotted: 𝐷 = 200 nm (a), 160 nm (b), and 120 nm (c).

Acknowledgements
The authors thank J.-Y. Yoon and K. V. D. Zoysa for valuable discussions, and Y. Nakano,
T. Tanno, I. Morita, R. Ono, and M. Musya for their technical support. This work was
supported by Japan Society for the Promotion of Science KAKENHI (grant nos.
23K26521, 24H00039, 24H02235, 24KJ0432 and 25K01276), Japan Science and
Technology Agency PRESTO (grant no. JPMJPR24H6) and TI-FRIS program, Iketani
Science and Technology Foundation, and Seiko Instruments Advanced Technology
Foundation.


# Operator learning for energy-efficient building ventilation control with computational fluid dynamics simulation of a real-world classroom

**Authors**: Yuexin Bian, Oliver Schmidt, Yuanyuan Shi
**Affiliation**: UC San Diego (ECE + MAE)
**Journal**: *Applied Energy* (2025); preprint arXiv:2504.21243v2 (Nov 2025)
**DOI**: 10.1016/j.apenergy.2025.127035
**OSTI ID**: 3365432

---

*Text extracted from the OSTI PDF (6.5 MB, MD5 69f130eadf8f1ad658af821773d2f447) with pdftotext; headings and blank-line structure re-flowed to Markdown. Figures, LaTeX-rendered equations, and multi-column layout artifacts are lost — see the source PDF for those. This file is a Marker/Nougat-style textual proxy used because neither marker-pdf nor nougat-ocr was available in the replication environment.*

---

Operator learning for energy-efficient building ventilation control with
computational fluid dynamics simulation of a real-world classroom
Yuexin Biana , Oliver Schmidtb and Yuanyuan Shia,∗

arXiv:2504.21243v2 [eess.SY] 18 Nov 2025

Department of Electrical and Computer Engineering, University of California San Diego , La Jolla, 92037, USA
Department of Mechanical and Aerospace Engineering, University of California San Diego , La Jolla, 92037, USA

ARTICLE INFO

ABSTRACT

Keywords:
Building energy systems
Ventilation control
Energy efficiency
Indoor air quality
Neural operator learning

Energy-efficient ventilation control plays a vital role in reducing building energy consumption while
ensuring occupant health and comfort. While Computational Fluid Dynamics (CFD) simulations
provide detailed and physically accurate representation of indoor airflow, their high computational
cost limits their use in real-time building control. In this work, we present a neural operator learning
framework that combines the physical accuracy of CFD with the computational efficiency of machine
learning to enable building ventilation control with the high-fidelity fluid dynamics models. Our
method jointly optimizes the airflow supply rates and vent angles to reduce energy use and adhere
to air quality constraints. We train an ensemble of neural operator transformer models to learn the
mapping from building control actions to airflow fields using high-resolution CFD data. This learned
neural operator is then embedded in an optimization-based control framework for building ventilation
control. Experimental results show that our approach achieves significant energy savings compared
to maximum airflow rate control, rule-based control, as well as data-driven control methods using
spatially averaged CO2 prediction and deep learning–based reduced-order model, while consistently
maintaining safe indoor air quality. These results highlight the practicality and scalability of our
method in maintaining energy efficiency and indoor air quality in real-world buildings.

## 1. Introduction

Buildings account for nearly 40% of global energy consumption [1], with Heating, Ventilation, and Air Conditioning (HVAC) systems being among the primary contributors.
Effective ventilation is critical not only for reducing energy
use but also for maintaining indoor air quality, which directly
impacts occupant health and comfort [2]. The urgency of
this issue has grown in light of the COVID-19 pandemic,
as building system operators and public health agencies
have increasingly emphasized the need for adaptive ventilation systems that respond to occupancy and pollutant levels
throughout the indoor space [3].
Despite this urgency, most building HVAC systems still
rely on fixed or rule-based ventilation strategies [4, 5, 6],
which are often overly conservative. For instance, maximum
fresh-air intake policies implemented at UC San Diego [6] in
response to health concerns have led to 2–2.5× increases in
energy usage. This highlights the critical trade-off between
maintaining indoor air quality and minimizing energy consumption, and the need for intelligent control methods that
balance these competing demands.
Recent advances in data-driven control approaches,
including model predictive control (MPC) [7, 8, 9, 10]
and reinforcement learning (RL) [11, 12, 13, 14, 15], have
shown strong potential for building ventilation management. However, most existing methods represent indoor air
states—such as CO2 concentration or temperature—using
spatially aggregated variables, typically measured at a single
point or averaged over an entire zone. For example, MPC
and RL-based strategies often model CO2 dynamics using
∗ Corresponding author

ORCID (s): 0000-0002-6182-7664 (Y. Shi)

Yuexin Bian et al.: Preprint submitted to Elsevier

ordinary differential equations (ODEs) [14, 16] or neural
networks [7, 8, 15] that predict future mean values based
on current measurements and control inputs. While computationally efficient, these low-dimensional representations
ignore spatial variations of indoor airflow velocity fields
and pollutant distribution that arise from the ventilation
layout, control actions, and occupancy patterns. As a result,
such controllers fail to capture the localized effects of
ventilation decisions. They may over-ventilate the entire
space to maintain air quality at a single location, wasting
energy, or overlook under-ventilated regions that compromise occupant health and comfort. This gap highlights
the need for spatiotemporal indoor airflow modeling to
accurately capture how ventilation control actions affect
air quality—crucial for maintaining occupant health while
enabling energy-efficient building HVAC operation.
To accurately model airflow dynamics and indoor air
quality, Computational Fluid Dynamics (CFD) simulations
are widely adopted in building ventilation research [17]. For
example, Bianco et al. [18] employed CFD to assist in the
design of ventilation units for buildings, while Gao et al. [19]
used CFD to analyze airflow fields in an isothermal chamber
under fixed ventilation rates. Bulinska et al. [20] modeled
CO2 distribution in a bedroom to inform optimal sensor
placement, while Mou et al. [21] simulated airflow and
CO2 concentration in a seminar room, capturing complex
3D ventilation patterns. Similarly, Ning et al. [22] used
CFD to evaluate the influence of supply outlet height on
indoor air distribution in a bedroom. Extending to classroom
environments, Mahmoud [23] applied CFD to analyze the
dispersion of human-generated aerosols and CO2 , offering
insights into ventilation design for indoor air quality.
Page 1 of 14

Operator learning for energy-efficient building ventilation control

Building Airflow
Modeling

Operator Learning

Decoder

Embeddingg

Encoder

Physics PDE model
CFD simulation

thousandfold speedup
in forecast

Energy-eﬃcient
Building control
Optimal control

Airflow

Supply airflow rate
Vent angle

Neural operator
prediction

Energy Saving
Predictive air distribution

Figure 1: Schematic of our data-driven operator learning framework for energy-efficient ventilation control. Computational fluid
dynamics (CFD) simulations are used to model complex 3D airflow and CO2 spatiotemporal dynamics. An ensemble of neural
operator transformer models is trained to learn the mapping between ventilation control actions and airflow field evolution.
Leveraging high-fidelity simulation data, our approach enables real-time optimization of ventilation strategies to minimize energy
consumption while maintaining indoor air quality.

Although CFD simulations can accurately model indoor
airflow fields, solving the governing partial differential equations (PDEs) using numerical solvers, such as finite element and finite volume methods, are computationally expensive [24]. This high cost makes it impractical to embed CFD
solvers directly into real-time control loops, where rapid decisions must be made in response to changing occupancy and
environmental conditions. Consequently, most CFD-based
studies [21, 22, 23] focus on offline analysis and system
design rather than real-time control. Our prior work [25] attempted to bridge this gap using a differentiable PDE-based
framework that optimizes control via adjoint methods. While
this approach enabled physically grounded optimization, it
required repeatedly solving PDE-constrained optimization
and was limited to a 2D setting with simplified geometry,
highlighting a key scalability bottleneck.
To address these limitations, in this work, we propose a
data-driven operator learning framework to approximate the
input–output behavior of CFD simulations. Neural operators
are designed to learn mappings between infinite-dimensional
function spaces, enabling them to approximate the solution
operator of PDEs across a family of initial and boundary
conditions [26, 27]. Previous studies [28, 29] have used
conventional neural networks to learn indoor air dynamics
from CFD data. However, these models operate in finitedimensional spaces and typically require fixed spatial grids,
making them inflexible and often requiring retraining under
new control or occupancy settings. In contrast, neural operators learn mappings between continuous functions, allowing
predictions to be queried at arbitrary spatial locations within
the room. This functional formulation captures how ventilation control actions shape the entire indoor airflow and
air quality distribution, enabling flexible and efficient ventilation control across diverse operating conditions. Several
neural operator architectures have demonstrated strong performance in modeling complex physical systems. For example, Deep Operator Networks (DeepONets) [27] and Fourier
Yuexin Bian et al.: Preprint submitted to Elsevier

Neural Operators (FNOs) [26] enable efficient approximation of fluid dynamics with significantly reduced computational cost. These models have shown success in applications
such as turbulent flow prediction [30], vehicle aerodynamics [31], and indoor airflow modeling [19]. More recently,
General Neural Operator Transformers (GNOTs) [32] have
extended these capabilities to irregular spatial domains and
multiple input functions, making them well suited for modeling building airflow with complex geometries and diverse inputs (e.g., control actions, occupancy, and past room states).

### 1.1. Summary of contributions

In this work, we propose a data-driven operator learning
framework for energy-efficient building ventilation control,
validated in a real-world classroom using CFD simulations
(Figure 1). While prior studies [19, 33] have applied neural
operators for airflow prediction, our work advances this
line in two key ways: (i) we propose an ensemble neural
operator transformer model that enhances prediction accuracy and robustness, and (ii) we introduce the integration
of operator learning into closed-loop control for building
energy management. This is substantially more challenging,
as performance must account for both predictive accuracy
and reliable control under energy and air quality constraints.
We benchmark our approach against data-driven ventilation control methods using averaged models (e.g., MLPs)
and deep learning–based reduced-order models (e.g., UNets) [34]. Unlike MLPs, neural operators capture full spatial airflow fields, and unlike reduced-order models, they
learn mappings between function spaces rather than pointwise values. This functional representation captures how
control actions shape the entire airflow patterns and resulting
indoor air quality. CFD-validated experiments demonstrate
that these advantages enable neural operators to achieve
more energy-efficient and healthier indoor environments
compared to finite-dimensional alternatives. Our key contributions are summarized as follows:

Page 2 of 14

Operator learning for energy-efficient building ventilation control

• Ensemble neural operator transformer: We propose
an ensemble neural operator transformer model to
predict building airflow velocity and CO2 fields under
varying HVAC control actions and occupancy levels.
This model improves prediction accuracy compared
to individual neural operator models and achieves
a remarkable speed-up of over 250,000× relative to
CFD simulations, enabling accurate indoor air quality
prediction with high computational efficiency.
• Building control with operator learning: We incorporate the learned neural operator into an optimization framework for energy-efficient ventilation control
subject to air quality constraints. Compared to maximum airflow control, rule-based control, and datadriven control using averaged prediction or reducedorder models, our approach enables more effective
closed-loop building ventilation control under varying
occupancy, achieving lower energy use and significantly fewer CO2 violations.

• Opensource building CFD dataset: We develop and
release a high-fidelity, open-access building dataset
derived from CFD simulations of a real-world classroom. Along with the dataset, we publish the underlying 3D room model and the files required to
reproduce and extend the simulations. The dataset
includes airflow velocity fields and CO2 fields under
diverse HVAC control actions and occupancy levels,
providing a reproducible benchmark for training and
evaluating machine learning models in building ventilation control applications.

## 2. Problem formulation

In this section, we introduce the governing dynamics of
indoor airflow and CO2 transport, and formulate the learning
and control problems. The CFD simulation setup and dataset
description are provided in Section 3.

### 2.1. Governing equations for CO2 dynamics

Let Ω ⊂ ℝ3 be the spatial domain of interests, and
let 𝑡 ∈ ℝ+ denote time. We define 𝐶(𝒙, 𝑡) as the CO2
concentration
at spatial
[
] location 𝒙 ∈ Ω and time 𝑡. Let
𝑚(𝑡) = 𝑚𝑟 (𝑡) 𝑚𝑎 (𝑡) ∈ ℝ12 be the control actions (airflow
rates 𝑚𝑟 ∈ ℝ6 and airflow angles 𝑚𝑎 ∈ ℝ6 ) for the six
groups of supply vents, and 𝑛𝑝 (𝑡) ∈ ℝ denote the occupancy
number. The distribution of CO2 in an indoor environment
follows the advection-diffusion equation [25, 35],
𝜕𝐶(𝒙, 𝑡)
+ 𝒖(𝒙, 𝑡) ⋅ ∇𝐶(𝒙, 𝑡) = 𝐷eff ∇2 𝐶(𝒙, 𝑡) + 𝑆(𝒙, 𝑡), (1)
𝜕𝑡
where
• 𝐶(𝒙, 𝑡) is the CO2 concentration (ppm) at location 𝒙
and time step 𝑡.

• 𝒖(𝒙, 𝑡) is the airflow velocity field obtained from CFD
simulations, by solving the incompressible NavierStokes equations. The boundary conditions at the
Yuexin Bian et al.: Preprint submitted to Elsevier

supply vents depend on the ventilation control 𝑚(𝑡),
thereby allowing the control action to influence 𝒖(𝒙, 𝑡)
throughout the domain. The numerical model for the
airflow velocity field is presented in the Appendix-A.

• 𝐷eff is the diffusion coefficient for CO2 in the air.

• 𝑆(𝒙, 𝑡) represents the CO2 source term, which models
occupant-generated CO2 on the designated occupancy
surface. This source depends on the occupancy level
𝑛𝑝 (𝑡) and we assume that the exhaled air rate is 6 L/min
per person following [36] .

### 2.2. Data-driven modeling with neural operator

Solving PDEs numerically is computationally expensive, making traditional CFD models impractical for realtime building control applications. To address this limitation, we aim to learn a neural operator 𝜃 that efficiently
maps historical CO2 concentrations, control actions, and
occupancy levels to future CO2 concentration distributions.
Formally, the neural operator learns the following mapping,
)
(
(2)
𝜃 ∶ 𝐶(𝒙, 𝜏)𝜏∈[𝑡−𝐻,𝑡] , 𝑚, 𝑛𝑝 ↦ 𝐶(𝒙, 𝜏)𝜏∈(𝑡,𝑡+𝑇 ]
where 𝐶(𝒙, 𝜏)𝜏∈[𝑡−𝐻,𝑡] is the historical CO2 fields over period [𝑡 − 𝐻, 𝑡] and 𝐶(𝒙, 𝜏)𝜏∈(𝑡,𝑡+𝑇 ] is the predicted future
CO2 fields over the future interval (𝑡, 𝑡 + 𝑇 ]. Our forecasting approach incorporates historical CO2 concentrations to
account for temporal dependencies inherent to the system’s
physics (e.g., diffusion and advection dynamics). We assume
that the control 𝑚 and occupancy 𝑛𝑝 remain fixed over (𝑡, 𝑡 +
𝑇 ]. In building control applications, the transient dynamics
of airflow and CO2 transport evolve rapidly over a short
time horizon—typically within a few minutes. However,
building control settings and occupancy levels generally
remain constant during these intervals (e.g., a fixed HVAC
setpoint over a 5-minute or 15-minute interval [6]). This
assumption thus maintains consistency between the physical
model and practical control timescales.
In practice, we rarely have continuous access to the
CO2 distribution over space and time. Instead, we rely on
a discretized approximation of the underlying functions. For
simplicity and consistency, we reuse the symbols 𝑡, 𝐻, 𝑇 as
discrete time indices. Let {𝑥𝑖 }1≤𝑖≤𝑁𝑥 be a spatial grid and
𝐶𝑖𝑡 ∈ ℝ be the CO2 concentration at spatial grid point 𝑥𝑖
and time step 𝑡. We collect the recent history of CO2 fields
over the last 𝐻 time steps, along with the fixed parameters
𝑚 and 𝑛𝑝 . Define the discrete input set
 = {(𝑥𝑖 , 𝐶𝑖𝑡−𝐻∶𝑡 )}1≤𝑖≤𝑁𝑥 ∪ {𝑚} ∪ {𝑛𝑝 },

(3)

although  is finite-dimensional, it represents the sampled
version of the underying function 𝐶(𝒙, 𝜏) over the history
window [𝑡 − 𝐻, 𝑡]. From this discrete representation, the
neural operator 𝜃 produces predicted future concentrations
𝑡+1∶𝑡+𝑇
𝐶̂1≤𝑖≤𝑁
(with short-hand notation ̂
𝐶), which approximate
𝑥
the continuous output function ̂
𝐶(𝒙, 𝜏) for 𝜏 ∈ (𝑡, 𝑡 + 𝑇 ]:
𝑡+1∶𝑡+𝑇
𝐶̂1≤𝑖≤𝑁
= 𝜃 ().
𝑥

(4)
Page 3 of 14

Operator learning for energy-efficient building ventilation control

Outlet vents

Occupant

Inlet vents

(a) Picture of the studied room and geometrical model of the room.

(b) Visualization of CO2 field and airflow velocity field.

Figure 2: (a) The picture of the studied room and the geometry of the CFD model: a classroom with a ventilation system including
18 inlet vents and 2 outlet vents on the ceiling. Occupants are modeled as a single rectangular cuboid with a prescribed CO2 mass
flux to represent CO2 effects of varying occupancy levels. (b) Visualization of the CFD simulation results of CO2 concentration
and airflow velocity fields - one example from the developed CFD dataset.

### 2.3. Ventilation control optimization

The learned neural operator 𝜃 can be integrated into
the building ventilation control optimization problem. The
resulting optimization problem is formulated in (5).
min

𝑚=[𝑚𝑟 ,𝑚𝑎 ]

s.t.

𝑤1 ‖𝐶̂ − 𝐶target ‖22 + 𝑤2 ‖𝑚 − 𝑚(0) ‖22 + 𝑤3 ‖𝑚𝑟 ‖1 ,

(5a)

𝑡−𝐻∶𝑡
𝐶̂ ← 𝜃 ({𝐶1≤𝑖≤𝑁
} ∪ {𝑚} ∪ {𝑛𝑝 }),
𝑥

𝑚𝑟 ≤ 𝑚𝑟 ≤ 𝑚𝑟 , 𝑚𝑎 ≤ 𝑚𝑎 ≤ 𝑚𝑎 .

(5b)

(5c)

In the objective function (5a), the first term quantifies the
deviation between predicted CO2 concentrations 𝐶̂ and the
desired CO2 level 𝐶target over a prediction horizon 𝑇 . This
term is commonly used in indoor air quality ventilation
control studies, as seen in prior works [16, 37]. The second
term penalizes deviations of the optimized control actions
from the previous control action 𝑚(0) . This is important
for real-world building management, where large deviations
in control actions are typically avoided to maintain system
stability and operational safety [25, 38]. By encouraging
control actions to remain close to 𝑚(0) , we also reduce the
risk of extrapolating beyond the model’s training domain,
thereby increasing the reliability of the predictions. The third
Yuexin Bian et al.: Preprint submitted to Elsevier

term represents the energy consumption, measured through
the L1 norm of the ventilation rate [25]. The coefficients
𝑤1 , 𝑤2 , 𝑤3 balance the relative importance of these objectives. Constraint (5b) describes that the predicted CO2
concentrations is obtained via the trained neural operator
model in Eqn (4), while constraint (5c) ensures that both
mechanical ventilation rates 𝑚𝑟 and vent angles 𝑚𝑎 remain
within their physical limits.

Remark 1. In this study, we do not explicitly model or

control indoor temperature in the problem formulation. This
choice is motivated by the fact that CO2 concentration
responds on a much faster time scale than temperature,
which evolves more slowly because of the building’s thermal
inertia. By focusing on the faster dynamics-airflow and
CO2 transport, we are able to evaluate the proposed control
strategy in a more responsive setting. We note that thermal
effects are still captured, as our CFD simulations solve the
energy equation (18) which models the transport of thermal
energy within the airflow and include occupant heat sources
and boundary temperature conditions. Extending the formulation to include indoor temperature modeling and thermal
control remains a valuable direction for future work, and our
framework is compatible with such multi-objective settings.
Page 4 of 14

Operator learning for energy-efficient building ventilation control

## 3. The BEAR-CFD data

The CFD simulation is developed based on a real-world
classroom located in University of California, San Diego.
The classroom is equipped with a ceiling-mounted ventilation system. The ventilation system includes 2 outlet vents
and 18 inlet vents grouped into six zones, each allowing independent control of airflow rates and supply airflow angles
to optimize energy efficiency while maintaining high indoor
air quality. Figure 2(a) illustrates the physical classroom and
its corresponding 3D computer-aided design (CAD) model
representation, and Figure 2(b) presents an example of the
CO2 concentration and velocity fields visualization. This
section provides a detailed description of the simulation
setup and the open-source dataset.

### 3.1. CFD simulation setup
#### 3.1.1. Geometry

The simulated domain represents a mechanically ventilated classroom with dimensions of 19m × 13m × 3.5m,
see Figure 2 (a). The ventilation system consists of 18
rectangular inlet vents, each measuring 0.1349m in width
and 0.3048m in height, and 2 ceiling-mounted outlet vent.
Fresh air is supplied through the inlets at prescribed velocity
and angle conditions, and exhausted through the outlets,
forming a displacement ventilation flow pattern.

#### 3.1.2. Occupant modeling
Occupants are collectively represented by a single, centrally positioned rectangular cuboid, visualized in Figure 2(a,
right). This abstraction aggregates the influence of multiple
seated individuals into a compact volume that approximates
their combined occupied zone [39, 40].
CO2 emissions from occupants are represented as a
surface mass flux boundary condition and are modeled using
the species transport equation [20, 23]. To simulate varying occupancy levels (ranging from 10 to 80 people), we
prescribe a total CO2 mass flux of 𝑛𝑝 × 0.00012 kg/s on
the cuboid surface, where 𝑛𝑝 is the number of occupants.
This corresponds to a constant breathing rate of 6 L/min per
person, following the simplified exhalation model in [20]. A
constant surface temperature is applied to the cuboid.
#### 3.1.3. Mesh
The fluid domain is discretized into approximately 0.245
million tetrahedral elements to resolve airflow and CO2
transport dynamics. Local mesh refinement is applied near
critical regions, including the occupant cuboid, inlet and
outlet vents, and wall boundaries, to capture steep gradients
in velocity and scalar fields. Mesh quality is assessed using
standard metrics: the minimum orthogonal quality is 0.172,
and the maximum aspect ratio is 43.33, indicating an acceptable mesh for transient indoor airflow simulations.
#### 3.1.4. Numerical models and boundary conditions
Airflow and CO2 dynamics within the classroom are
simulated using the commercial CFD software ANSYS Fluent [41]. The incompressible Navier–Stokes equations are
Yuexin Bian et al.: Preprint submitted to Elsevier

Table 1
Boundary conditions.
Boundary surface

Boundary conditions

Inlet vents

velocity intlet, 𝐶inlet
=400ppm,
𝑇inlet =20◦ C, 𝑚𝑟 ∼ 𝑈 [0.324, 3.24]m/s,
𝑚𝑎 ∼ 𝑈 [45, 135]◦
Pressure outlet
No-slip and adiabatic walls, 𝑇wall =
21◦ 𝐶
mass flow inlet, 𝐶occupant
=
40000ppm, 𝑇occupant =25◦ C [20]

Outlet vents
Walls
Occupant surface

solved to capture airflow behavior, coupled with species
transport equations to model the distribution of CO2 , O2 ,
H2 O, and N2 . Turbulence is modeled using the 𝑘–𝜔 SST
(Shear Stress Transport) model, which is well-suited for predicting indoor near-wall flow behavior [42]. The governing
equations are discretized using the finite volume method,
with second-order schemes for both momentum and species
transport. The energy equation is also activated to solve for
temperature.
The boundary surfaces include walls, inlet and outlet
vents, and the occupant surface. A summary of boundary
conditions is provided in Table 1. Inlets are modeled as velocity boundaries with prescribed temperature (𝑇inlet ), CO2
concentration (𝐶inlet ), velocity magnitude (𝑚𝑟 ), and velocity
angle (𝑚𝑎 ) [20, 23]. To introduce airflow variability, the
inlet velocities and angles for vent groups are randomly
sampled from uniform distributions. A maximum velocity
of 3.24 m/s corresponds to 10 air changes per hour (ACH),
based on operational data. Outlets are modeled as pressure
boundaries, and all walls are treated as no-slip, adiabatic
surfaces with fixed temperature.

Remark 2. The CFD simulations used in this work follow

standard modeling practices for indoor airflow [40, 20, 43],
and are designed to provide consistent and reproducible
training data for future research. The simulation setup assumes constant air density (incompressible flow), omitting
the buoyancy effects. This simplification is reasonable in
mechanically ventilated classrooms where forced ventilation
dominates airflow. Nevertheless, we acknowledge that in
densely occupied spaces, buoyancy forces may contribute
to airflow patterns. Extending the CFD setup to incorporate
buoyancy remains an important direction for future work,
and our framework is readily adaptable to such enhanced
simulations as well as to other CFD configurations and
building control systems.

### 3.2. Bear-CFD Dataset

Bear-CFD dataset is generated through a structured CFD
simulation workflow designed to capture the spatiotemporal
dynamics of indoor CO2 levels under varying ventilation and
occupancy conditions. The dataset is publicly available at
https://ucsdsmartbuilding.github.io/CFD-DATA.html.

Page 5 of 14

Operator learning for energy-efficient building ventilation control

The simulations include both steady-state and transient
flow cases. Specifically, we run 10 steady-state simulations
under different boundary conditions. These steady-state results are then used as initial conditions for 300 transient
simulations, each lasting 30 minutes of physical time and
resolved at 10-second time steps. This initialization strategy
ensures that each transient simulation begins from a realistic
state shaped by prior control conditions. Without this step,
starting from uniform or arbitrary states (e.g., same CO2
everywhere) could introduce artificial transients unrelated
to the actual control inputs. Simulation outputs are saved
every 30 seconds, resulting in 60 time steps per transient
case. Transient simulations capture the temporal evolution
of airflow dynamics, reflecting unsteady effects influenced
by varying boundary conditions. We leverage this transient
data to train our neural operators.
To generate the dataset, for each simulation, key control
parameters, including supply airflow rates (𝑚𝑟𝑖 ) and airflow
angles (𝑚𝑎𝑖 ) for the 𝑖-th group of inlet vents (𝑖 = 1, … , 6), as
well as the occupant count (𝑛𝑝 )—are independently sampled
from uniform distributions:
𝑚𝑟𝑖 ∼ 𝑈 [𝑚𝑟 , 𝑚𝑟 ], 𝑚𝑎𝑖 ∼ 𝑈 [45◦ , 135◦ ], 𝑖 ∈ [1, … , 6],
𝑛𝑝 ∼ 𝑈 [10, 80],

(6)

where 𝑚𝑟𝑖 is the airflow rate for the 𝑖-th group of vents,
bounded between 𝑚𝑟 = 0.324m/s (10% of maximum) and
𝑚𝑟 =3.24m/s; 𝑚𝑎𝑖 is the airflow angle of the 𝑖-th group of
vents, spanning 45◦ to 135◦ ; and 𝑛𝑝 is the number of occupants in the classroom. Each transient simulation follows
this two-phase procedure: (1) Steady-state initialization: A
random initial condition is selected from the 10 steady-state
simulations. (2) Transient simulation: Control parameters
(𝑚𝑟𝑖 , 𝑚𝑎𝑖 ) and occupancy 𝑛𝑝 are sampled. The simulation
runs for 30 minutes, with CO2 and airflow fields recorded
at 30-second intervals over 𝑇 = 60 time steps. The CO2
concentrations were monitored at two critical planes:
• HVAC surface: A horizontal plane at 2.9-meter height
near the ventilation inlets, capturing the supply and
returning air quality.

• People surface: A horizontal plane at 1.6-meter height
(average breathing height for standing adults), representing air quality at occupant exposure levels [44].

In our CFD simulation, the sitting surface is near the occupancy boundary, leading to potential inaccuracies from
numerical artifacts and boundary effects. Thus, we focused
on heights where airflow and CO2 dispersion are more
reliably captured.
The dataset is distributed in both ANSYS FLUENT’s
native format (.cas and .dat files) and Python pickle (.pkl)
format. The FLUENT files preserve the complete simulation
environment and solution data, while the pickle format enables efficient programmatic access to the numerical results
through standard Python libraries. The dataset includes spatiotemporal fields of CO2 concentrations, airflow rates, vent
angles, and occupancy, as detailed in Table 2.
Yuexin Bian et al.: Preprint submitted to Elsevier

Table 2
Data fields in the BEAR-CFD dataset pickle (.pkl) format.
Field
HVAC surface
CO2 -HVAC
People surface

CO2 -People
steady case
𝑛𝑝
𝑚𝑟𝑖
𝑚𝑎𝑖

Description
ndarray (𝑁hvac , 3), spatial coordinates of grid points on HVAC surfaces
ndarray (𝑁hvac ,𝑇 ), CO2 concentration time series at HVAC surface
ndarray (𝑁people , 3), spatial coordinates of grid points on people surfaces
ndarray (𝑁people ,𝑇 ), CO2 concentration time series at people surface
int, Identifier for the initial steadystate condition used in the simulation
int, number of occupant
float, airflow rate (m/s) for 𝑖-th group
of vents
float, angle (◦ ) for 𝑖-th group of vents

## 4. Methodology

In this work, we propose a data-driven operator learning
framework to model the indoor air quality and optimize
ventilation control for energy efficiency. The core component is an ensemble neural operator transformer architecture, 𝜃 , shown in Figure 3. In figure 3(a), the neural
operator architecture enables fast building CFD simulations
by processing multiple inputs: query points, supply airflow
rates, airflow angles, and historical CO2 concentrations. The
trained operator learning model uses these inputs to predict
future CO2 , which are then utilized to determine optimal
ventilation control parameters by solving the optimization
problem defined in Equation (5). In the following subsections, we will first explain the concept of operator neural
transformer, then detail describe the control algorithm.

### 4.1. Ensemble neural operator transformer

Existing operator learning approaches, while effective
in many applications, often struggle with limited training
data. To address this limitation, we enhance the General
Neural Operator Transformer (GNOT) [32] by ensemble
learning [45]. The network architecture of the proposed
model together with the control is illustrated in Figure 3.
In the following subsections, we will describe the input
encoding and ensemble learning for GNOT.

#### 4.1.1. Input encoding
The model takes the input mesh, historical CO2 concentrations, and control parameters (including ventilation
control actions and the number of occupants), as inputs. To
accommodate these heterogeneous inputs, a general encoder,
highlighted in green in Figure 3, is employed to transform
them into the feature embedding 𝑌 ∈ ℝ𝑁×𝑛𝑒 , where 𝑁
denotes an arbitrary number of input elements and 𝑛𝑒 is the
embedding dimension. The model employs simple multilayer perceptrons (MLPs), denoted as 𝑓𝑤1 , 𝑓𝑤2 , 𝑓𝑤3 , to map
each type of input to its corresponding embedding.
Page 6 of 14

Operator learning for energy-efficient building ventilation control
Future CO2
concentrations

Gating

Ymesh
Past CO2
concentrations
Control
parameters

KC

Encoder

YC

(

np )

Encoder

VC

Heterogeneous
Normalized
Cross-Attention

+

FFN

FFN
FFN

Kparam

Normalized
self
Attention

Q

K

V

Vparam

Yparam

m

+

+

Q

Encoder

+

Input mesh

FFN

FFN
FFN

Mean

μC

Variance
× multiple

σC2

(a) Neural operator transformer Gθ architecture.
Model 1

min w1∥ C ̂ − Ctarget∥22 + w2∥m − m (0)∥22 + w3∥m r∥1

Model 2

m=[m r,m a]

t−H:t
s.t. C ̂ ← Gθ ({C1≤x≤N
} ∪ {m} ∪ {np})
x

Optimal m

m r ≤ m r ≤ m r, m a ≤ m a ≤ m a

…
Optimization

C ̂

Model

Nensemble

CO2 concentration predictions

(b) Ventilation control with the ensemble neural operator.

Figure 3: Overview of the proposed data-driven operator learning framework for energy-efficient ventilation control. The framework
consists of two phases: (1) the learning phase, where neural operator transformers are trained to map past air field data and
ventilation control parameters to future air field evolution, and (2) the control phase, where the trained ensemble neural operator is
integrated into an optimization framework to solve the ventilation control problem. This approach enables real-time optimization
of airflow supply rates and vent angles while maintaining air quality standards.

• Input mesh: A MLP maps the mesh points to query
embeddings 𝑌mesh = (𝑓𝑤1 (𝑥𝑖 ))1≤𝑖≤𝑁𝑥 ∈ ℝ𝑁𝑥 ×𝑛𝑒 .

concentrations, characterized by the mean (𝜇𝐶 ) and variance
(𝜎𝐶2 ). Specifically, the model predicts:

• Past CO2 concentrations: At time 𝑡, we have {𝑥𝑖 , 𝑐𝑖 }1≤𝑖≤𝑁𝑥 ,
(7a)
𝜇𝐶 , 𝜎𝐶2 = 𝜃 (),
𝑡−𝐻∶𝑡
where 𝑐𝑖 = 𝐶𝑖
represents the historical CO2
𝑡+1∶𝑡+𝑇
𝑡+1∶𝑡+𝑇
],
(7b)
], 𝜎𝐶2 = Var[𝐶̂1≤𝑖≤𝑁
𝜇𝐶 = 𝔼[𝐶̂1≤𝑖≤𝑁
levels at position 𝑥𝑖 . A MLP encodes both positions
𝑥
𝑥
and concentrations to produce the feature 𝑌𝐶 =
where [𝜇𝐶 ]𝑡𝑖 , [𝜎𝐶2 ]𝑡𝑖 represents the mean and variance at loca(𝑓𝑤2 (𝑥𝑖 , 𝑐𝑖 ))1≤𝑖≤𝑁𝑥 ∈ ℝ𝑁𝑥 ×𝑛𝑒 .
tion 𝑖 and time step 𝑡. The model is trained using the Negative
• Control parameters: A MLP encodes control paramLog-Likelihood (NLL) loss, defined as:
eters [𝑚, 𝑛𝑝 ] ∈ ℝ13 into embeddings 𝑌param =
(
)
𝑁𝑥 𝑇
2 𝑡+𝑘
𝑡+𝑘
𝑡+𝑘 2
𝑓𝑤3 ([𝑚, 𝑛𝑝 ]) ∈ ℝ1⋅𝑛𝑒 .
1 ∑ ∑ log(2𝜋[𝜎𝐶 ]𝑖 ) (𝐶𝑖 − [𝜇𝐶 ]𝑖 )
=
+
𝑁𝑥 𝑇 𝑖=1 𝑘=1
2
2[𝜎𝐶2 ]𝑡+𝑘
𝑖
#### 4.1.2. Ensemble learning of GNOT
(8)
As shown in Figure 3(a), GNOT begins by encoding
where 𝐶𝑖𝑡+𝑘 ∈ ℝ is the true value at 𝑥𝑖 and time 𝑡 + 𝑘.
input features and updating them using a heterogeneous norBy minimizing the NLL loss, the model learns to jointly
malized cross-attention layer, followed by a normalized selfoptimize the mean and variance predictions, effectively mitattention layer to refine representations. To effectively capigating overfitting [45].
ture spatial heterogeneity, GNOT incorporates a geometric
We train an ensemble of neural operator transformers,
gating mechanism that leverages the query point coordinates
with the final prediction obtained by averaging outputs from
to compute a weighted combination of expert feed-forward
multiple independently trained models. Let 𝜇𝐶(𝑛) denote the
networks (FFNs). The model stacks 𝑁 such attention blocks
mean prediction of the 𝑛-th model. The ensemble prediction
to produce the final predictions.
is then computed as,
While GNOT is originally designed to output only the
mean of the prediction, we enhance its robustness by in𝑁ensemble
∑
1
troducing an ensemble-based extension. Instead of training
𝜇𝐶(𝑛) ,
(9a)
𝜇𝐶ensemble =
𝑁
GNOT to minimize mean squared error or relative error, we
ensemble
𝑛=1
modify it to predict a probability distribution for future CO2
𝜇𝐶(𝑛) , (𝜎 2 )(𝑛)
= 𝜃𝑛 (),
(9b)
𝐶
Yuexin Bian et al.: Preprint submitted to Elsevier

Page 7 of 14

Operator learning for energy-efficient building ventilation control

Algorithm 1 Algorithm for solving (5)
Require: Neural operator transformers 𝜃 ,
𝑡−𝐻∶𝑡 , 𝑛
1:
Control inputs 𝐶1≤𝑖≤𝑁
𝑝

Ensure: 𝑚(0)
⊳ initial control actions
2: for 𝑖𝑡𝑒 = 0, 1, … MaxIte do
3:
obtain future CO2 predictions 𝐶̂ (9)(11)
4:
evaluate loss (𝑚) (10)
5:
compute the gradient ∇(𝑚)
6:
update the control vector with step size 𝜂:
𝑥

𝑚(𝑖𝑡𝑒+1) ← 𝑚(𝑖𝑡𝑒) − 𝜂∇(𝑚)
project the update 𝑚 to satisfy the box constraints (5c)
8: end for
9: Return 𝑚
7:

where 𝑁ensemble represents the number of models in the
ensemble, 𝜃𝑛 is the model parameters for 𝑛-th trained neural
operator. This ensemble approach not only improves prediction accuracy but also enhances the reliability of ventilation
control, as demonstrated in our experiments.

### 4.2. Control algorithm

With the learned ensemble neural operator transformer
model, we are ready to solve the building control problem in
(5). Recall that the objective function of the building control
problem is defined as:
(𝑚) = 𝑤1 ‖𝐶̂ − 𝐶target ‖22 + 𝑤2 ‖𝑚 − 𝑚(0) ‖22 + 𝑤3 𝑇 ‖𝑚𝑟 ‖1
(10)
where the first term ‖𝐶̂ − 𝐶target ‖22 is defined as,
‖𝐶̂ − 𝐶target ‖22 =

𝑇 𝑁𝑥
1 ∑ ∑ ̂𝑡+𝑘
− 𝐶target 𝑡+𝑘
)2
(𝐶
𝑖
𝑁𝑥 𝑇 𝑘=1 𝑖=1 𝑖

and 𝑤1 , 𝑤2 , 𝑤3 are weighting coefficients. 𝐶̂ represents the
predicted CO2 concentrations generated by the ensemble
neural operator (9):
𝐶̂ = 𝜇𝐶ensemble .

(11)

To solve the building control problem in (5), we leverage
the differentiability of the neural operator 𝜃 and propose
a gradient-based method to update the control actions for
ventilation. To ensure that the control vector 𝑚 remains
within feasible bounds (5c), we use a projected gradient
descent method. Specifically, after computing the gradient
of the objective function with respect to 𝑚, the control vector
is updated and then clipped to satisfy the predefined bounds.
Our optimization procedure is summarized in Algorithm 1.

operator, and (2) control experiments to evaluate the effectiveness of our data-driven ventilation control framework.
The source code, input data, and trained models from all
experiments are available on GitHub1 . All experiments are
conducted on NVIDIA GeForce RTX 2080 Ti GPUs.

### 5.1. Learning results

We train our ensemble neural operator transformer to
predict CO2 levels on the people surface. The number of
query points is 𝑁𝑥 = 7462, and we select 𝐹 = 12 and 𝑇 = 6,
meaning that the model utilizes data from the past 12 time
steps (equivalent to 6 minutes) to forecast CO2 levels over
the next 6 time steps (3 minutes). The dataset is divided into
an 80% training set and a 20% testing set to evaluate model
performance. We train 𝑁ensemble = 5 independent models
and compute the mean of their predictions as the final output.
We use the AdamW optimizer with a cyclical learning rate
schedule, and each model is trained for 200 epochs.
To evaluate model performance, we use the average 𝑙2
̂
(𝑑) ∈ ℝ𝑁𝑥 ×𝑇
relative error as the primary metric. Let 𝐶 (𝑑) , 𝐶
denote the ground truth and the predicted mean future CO2
concentrations for the 𝑑-th sample, respectively, and let 𝐷
represent the total dataset size. The error is defined as:
𝐷
̂
(𝑑) − 𝐶 (𝑑) ‖
1 ∑ ‖𝐶
2
.
𝑙2 =
(𝑑)
𝐷 𝑑=1
‖𝐶 ‖2

(12)

Figure 4 shows the training convergence and test performance of the five neural operator transformers over 200
epochs. The left plot presents the NLL loss (8), while the
right shows the 𝑙2 relative error on both training and test sets.
Table 3 list the 𝑙2 error metrics for the five trained models
(Model 1 to Model 5) and the ensemble model, evaluated on
both the training and testing datasets. Notably, the ensemble
model achieves the lowest errors, with a training 𝑙2 error of
5.9% and a testing 𝑙2 error of 10.90%. The ensemble model
consistently outperforms the individual models, leading to
more robust and accurate predictions. The performance improvement can be attributed to the ensemble model’s ability
to mitigate potential overfitting of individual models by
averaging out their prediction errors.
Figure 5 shows the ground truth CO2 concentration fields
with predictions from the ensemble model and Model 3
(best-performing individual model), along with their relative errors for three test cases. Overall, the neural operator
framework shows strong capability in predicting complex
spatial CO2 distributions under varying control parameters.
The ensemble model achieves lower relative errors and more
accurately captures spatial patterns compared to Model 3.
In Section 5.4, we further demonstrate its effectiveness in
activating control actions and optimizing the air quality.

### 5.2. Ventilation control results

## 5. Numerical experiments

In this section, we evaluate the performance of the proposed framework through two experiments: (1) learning
experiments to assess the accuracy of the ensemble neural
Yuexin Bian et al.: Preprint submitted to Elsevier

We now evaluate the control performance under three
occupancy scenarios: high (𝑛𝑝 = 75), medium (𝑛𝑝 =
45), and low (𝑛𝑝 = 15). According to ASHRAE Standard
1 https://github.com/alwaysbyx/BuildingControlCFD

Page 8 of 14

Operator learning for energy-efficient building ventilation control

Figure 4: Training loss (NLL loss) during training (left) and the 𝑙2 error for the training (middle) and test sets (right). The 𝑙2
error (12) is computed based on the ground truth and the model’s mean prediction output.

𝑙2 error (Train)
𝑙2 error (Test)

Model 1
6.35%
12.09%

Model 2
6.33%
11.83%

Model 3
6.33%
11.82%

Model 4
6.35%
12.74%

Model 5
6.33%
13.01%

Ensemble
5.9%
10.90%

Table 3
The 𝑙2 error for five independently trained neural operator transformer models (Model 1 to Model 5) and their ensemble.

62.1 [46], classrooms typically require 4–6 air changes per
hour (ACH) to ensure adequate ventilation and indoor air
quality. For all scenarios in this study, the initial control
actions are initialized at 5 ACH (within the recommended
range) for supply vents, with inlet angles fixed at a 90◦
downward orientation to align with conventional HVAC
configurations. We evaluate the following control strategies:
• Max Control: The airflow rate is set to its maximum
value, with the inlet angle fixed at 90◦ downward.
• Baseline Control: The control actions determined
based on the ASHRAE standard as 5 ACH with 90◦
downward angle, serving as a baseline for comparison.
• Rule-based Control: The airflow rate is set proportionally to the occupancy level, calculated as the number of occupants divided by the maximum occupancy,
with 90◦ downward angle.
Ground truth

Prediction (ensemble)

Prediction (model3)

• Data-driven (DL-Avg): We employ a neural network
to predict the average CO2 concentration at the center
of the occupancy surface. Ventilation control actions
are optimized based on (5) with the prediction.
• Data-driven (DL-ROM): We implement a state-ofthe-art Deep Learning–based Reduced-Order Modeling approach(DL-ROM) [34] to approximate the spatiotemporal CO2 distribution. The resulting surrogate
model is integrated into our ventilation control optimization framework (5) to optimize control actions.

• Ours: We use the proposed ensemble neural operator
transformer to model the spatiotemporal dynamics of
CO2 concentrations. The learned neural operator is
then used within the same ventilation control optimization framework in (5) to optimize control actions.

For our optimization solver, we choose 𝐶target = 400
(ppm) to ensure that the CO2 concentration loss is more
Relative error (ensemble) Relative error (model 3)

Figure 5: Operator Learning: Visualization of the ground truth, corresponding predictions from the ensemble model and Model
3, and the relative errors between the ground truth and predictions at the final time step.
Yuexin Bian et al.: Preprint submitted to Elsevier

Page 9 of 14

Operator learning for energy-efficient building ventilation control
Case

1

2

3

Control Strategy
Max Control
Baseline Control
Rule-based Control
Data-driven(DL-Avg)
Data-driven(DL-ROM)
Ours
Max Control
Baseline Control
Rule-based Control
Data-driven(DL-Avg)
Data-driven(DL-ROM)
Ours
Max Control
Baseline Control
Rule-based Control
Data-driven(DL-Avg)
Data-driven(DL-ROM)
Ours

Mean CO2 (ppm)
Average Final Step
565.6
534.0
616.1
612.3
567.4
533.5
604.4
595.2
626.2
635.8
600.7
587.9
546.7
512.2
599.9
595.9
593.7
584.6
584.7
562.1
602.7
600.1
605.0
600.0
532.3
497.6
585.2
578.0
650.7
712.7
576.9
566.0
590.3
590.2
589.4
585.4

Peak CO2 (ppm)
Average Final Step
895.7
854.2
1203.0
1143.6
898.1
807.9
1021.6
971.6
1300.1
1326.7
1060.2
1004.0
800.0
741.3
1097.3
1108.4
1057.6
1059.3
912.7
914.6
1062.2
1066.2
1044.1
881.4
754.0
692.0
1034.2
1013.9
1361.4
1623.1
946.1
978.3
1121.6
1208.4
984.4
949.8

CO2 > 1200ppm (%)
Average Final Step
0.00
0.00
1.32
0.00
0.00
0.00
0.00
0.00
8.34
10.56
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
0.00
15.67
35.26
0.00
0.00
0.13
0.70
0.00
0.00

Energy
Consumption (%)
100.0
50.0
93.8
83.3
44.6
65.8
100.0
50.0
56.2
83.0
50.8
43.8
100.0
50.0
18.8
66.1
49.4
55.2

Table 4
Comparison of CO2 metrics (mean, peak, and violation percentages) and energy consumption across different control strategies.
"Average" refers to the temporal mean over the simulation period, while "Final Step" refers to the CO2 level at the end of
the simulation. Our approach achieves significant ventilation energy savings compared to the other control approaches while
maintaining acceptable CO2 violation levels.

broadly activated across the spatial domain, enabling more
effective optimization with respective to the control actions.
We choose 𝑤1 = 1, 𝑤2 = 0.4 and 𝑤3 = 0.12 through
empirical tuning to balance air quality, energy consumption,
and control smoothness. These weights are used consistently
across all control experiments.
We validate the three control strategies using CFD simulations. Performance is measured using three metrics: mean
CO2 (ppm), peak CO2 (ppm), and CO2 violation (%), dePeak CO2 −1200
fined as
. As suggested by [47], 1200 ppm
1200
is the maximum acceptable CO2 level for human health.
For each metric, we record both the temporal average over
the simulation period and the value at the final time step.
Energy consumption is modeled as the percentage of the
maximum power required to operate the ventilation system
at its maximum airflow rate, providing a normalized measure
of energy usage relative to the system’s peak capacity:
1∑ 𝑟 𝑟
𝑚 ∕𝑚 × 100%,
6 𝑖=1 𝑖
6

𝐸(𝑚) =

(13)

where 𝑚𝑟𝑖 represents the ventilation rate for the 𝑖-th vent, and
𝑚𝑟 = 3.24 (m/s) is the maximum ventilation rate.
The results are summarized in Table 4. The experimental
results demonstrate the effectiveness of the proposed control
strategy (Ours) in balancing air quality and energy consumption in the first two cases. In Case 3, under the lowoccupancy scenario, the optimization favors maintaining
higher air quality, leading to slightly higher energy consumption than the baseline control. Compared to the Max
control strategy, our method achieves comparable air quality performance while reducing energy usage by 34–56%.
Yuexin Bian et al.: Preprint submitted to Elsevier

Compared to the baseline control, our approach effectively
lowers CO2 levels and adheres to air quality constraints with
slight energy increase. Rule-based control suffers from CO2
violations (e.g., 35.2% final-step violation in Case 3) due to
its reliance on well-chosen static operation schedules. Unlike
rule-based systems, which require manual fine-tuning of
thresholds for different room layouts and occupancy levels,
our method autonomously adapts to operation conditions
and reduces energy consumption by 12-28% in Cases 1-2
while maintaining safe CO2 levels.
In addition, our method outperforms data-driven control
(DL-Avg) and (DL-ROM) by maintaining good energy efficiency without incurring any violations of the air quality
constraints. While the DL-Avg approach can optimize ventilation locally, it has two key limitations: (1) it primarily
predict average CO2 concentrations rather than spatial variations, and (2) it cannot effectively map control actions to
real-time CO2 distributions across different zones. While
the DL-ROM approach captures spatial-temporal airflow
dynamics, it is less effective at modeling the relationship
between control inputs and the resulting air distributions
compared to our method. For completeness, we present the
learning results of DL-ROM in Appendix B.

### 5.3. Multi-step ventilation control results

To assess the proposed operator learning model in realistic control scenarios, we extend the single-step optimization
in Section 5.2 to a multi-step planning horizon. Specifically,
a 30-minute ventilation horizon is considered with 10 planning steps, each optimizing control over the next 6 time steps
(3 minutes), yielding 60 control steps in total. The initial step
(𝑡 = 0) is initialized using historical CO2 data from Scenario
Page 10 of 14

Operator learning for energy-efficient building ventilation control

without capturing the dynamic spatial shifts of peak concentrations over time. As a result, the control decisions fail
to address localized high-risk areas, leading to both higher
energy consumption and more CO2 violations.
In addition, we plot the time series of control actions
for the six groups of vents, under our approach in Figure 7.
Notably, the airflow rates for vent groups 2 and 6 exhibit a
strong correlation with occupancy, increasing during higher
occupancy periods to enhance ventilation. Additionally, the
controller consistently assigns the highest airflow to vent
group 1, while groups 3, 4, and 5 maintain relatively low flow
rates. This likely reflects spatial differences in ventilation
effectiveness, with the optimization learns to prioritize vents
that more effectively contribute to CO2 removal.

### 5.4. Effectiveness of the ensemble model

Figure 6: Comparison of occupancy profile, energy consumption, and peak CO2 concentration over a 60-step period.
The top panel illustrates dynamic occupancy changes, the
middle panel shows corresponding energy consumption as a
percentage of the maximum, and the bottom panel depicts
CO2 concentration levels with the threshold limit (1200 ppm)
indicated by a dashed line.

1 in Subsection 5.2, while subsequent steps use the predicted
CO2 levels by recursively rolling out the learned operator
model with previously optimized controls.
Figure 6 illustrates the performance of the proposed
control strategy in comparison to other control methods.
The occupancy profile (top) shows significant variations
over time. Our strategy dynamically adjusts ventilation in
response to occupancy levels. At the beginning, when occupancy is high, the controller increases airflow to mitigate
CO2 accumulation. Although occupancy drops shortly after,
the controller maintains a moderately high ventilation rate
to clear the residual CO2 from the earlier crowded period.
In contrast, during later low-occupancy intervals, lower accumulated CO2 allows the system to reduce airflow further,
resulting in greater energy savings.
Over the control period, total energy consumption for
Max, Baseline, Rule-based, Data-driven (DL-Avg), Datadriven (DL-ROM), and our method is 100%, 50%, 63.1%,
55.3%, 57.6%, and 50.6%, respectively. In terms of CO2 violations, Max control yields zero violations; Baseline, Rulebased, and DL-ROM incur 17, 10, and 7 violations; DLAvg results in 37 violations and ours incurs only 1 violation.
The relatively poor performance of DL-Avg stems from its
reliance on predicting only the average CO2 concentration,
Yuexin Bian et al.: Preprint submitted to Elsevier

In this subsection, we demonstrate the effectiveness of
the ensemble model in control compared to individual models, serving as an ablation study. As shown in Section 5.1, the
ensemble model achieves the lowest prediction error among
all models. Building on these results, we further illustrate
that the ensemble model, which aggregates predictions from
multiple independently trained neural operators, consistently
outperforms individual models in the control stage.
To gain more insights from the optimization results,
we set the coefficient for energy consumption 𝑤3 = 0 in
the building control problem (5). This allows the control
strategy to prioritize air quality without considering energy
cost. We optimize the control actions for a case in which
the control parameters are randomly selected, using both the
individual models and the ensemble model. The resulting
control actions are illustrated in Figure 8. We observe that
the ensemble model consistently reaches maximum airflow
rates for all inlet vents, which align with the optimal action
in this test case as the energy cost coefficient 𝑤3 = 0. In
contrast, the individual models exhibit variability in their
control actions, with some models failing to achieve the
maximum airflow rates across all vents.

### 5.5. Runtime analysis

To evaluate the computational efficiency of our proposed
operator learning for building ventilation control, we analyze
the runtime associated with each stage of the algorithmic
pipeline, including the cost of generating CFD data, training
time of the neural operator models, and performing inference
during control deployment.
Table 5 summarizes the runtime of each component.
The CFD simulations are conducted using ANSYS Fluent
in parallel 6 cores, while neural operator training was performed using 2 RTX 2080 Ti GPUs. We observe that CFD
simulation takes 1,253.7 seconds to compute the transient
flow over six time steps (3 minutes), whereas the neural
operator transformer completes the same task in just 0.005
seconds. This represents a remarkable speed-up of approximately 250,000 times compared to the CFD simulation. Although the learning phase requires moderate computational
resources (the training of the five transformer models takes
16 GPU hours in total), the resulting neural operator enables
Page 11 of 14

Operator learning for energy-efficient building ventilation control
Table 5
Runtime of the operator learning pipeline.
Stage
Learning
CFD data generation

Time Cost

Neural operator training

3.5 CPU hours per simulation, totaling 1100
CPU hours
16 GPU hours

Control
CFD simulation (Sec 5.2)
CFD simulation (Sec 5.3)
Inference (ours)

1253.7 seconds
3.5 hours
<0.005 seconds

rapid inference and real-time building control with the highfidelity indoor fluid dynamics models.

## 6. Conclusion and future work

In this work, we propose a novel operator learning framework for energy-efficient ventilation control. Our approach
involves training an ensemble of neural operator transformer
models to learn the mapping from past CO2 fields, occupancy levels, and control actions to future CO2 fields.
The ensemble model demonstrates superior predictive performance compared to individual models. We further integrate the learned neural operator into building ventilation optimization to optimize control actions. Using CFD
simulations, we validate the proposed approach achieves
substantial energy savings compared to maximum airflow
control, rule-based control, and data-driven methods based
on average CO2 predictions and reduced-order modeling. In
addition, compared to baseline control, our method maintains similar energy consumption while significantly reducing CO2 violations. We open-source the CFD data to facilitate further research in developing machine learning models
for building ventilation control with PDE-based models.
Promising future directions include extending the framework to more complex building environments, such as multizone systems. In addition, real-world experiments with integrated sensing and actuation systems are planned to validate
the framework’s practical performance.

## Acknowledgments

The authors gratefully acknowledge Ling Zhong for the
framework visualization design. This work is supported by
a Schmidt Sciences AI2050 Early Career Fellowship, NSF
grant ECCS-2442689, and DOE grant DE-SC0025495.

## References

[1] K. J. Chua, S. K. Chou, W. Yang, J. Yan, Achieving better energyefficient air conditioning–a review of technologies and strategies,
Applied Energy 104 (2013) 87–104.
[2] B. Chenari, J. D. Carrilho, M. G. Da Silva, Towards sustainable,
energy-efficient and healthy ventilation strategies in buildings: A
review, Renewable and Sustainable Energy Reviews 59 (2016) 1426–
1447.

Yuexin Bian et al.: Preprint submitted to Elsevier

[3] A. H. Hosseinloo, S. Nabi, A. Hosoi, M. A. Dahleh, Data-driven
control of covid-19 in buildings: a reinforcement-learning approach,
IEEE Transactions on Automation Science and Engineering (2023).
[4] S. Shi, S. Miyata, Y. Akashi, Event-driven model-based optimal
demand-controlled ventilation for multizone vav systems: Enhancing
energy efficiency and indoor environmental quality, Applied Energy
377 (2025) 124683.
[5] REHAV, Covid 19 guidance, https://www.rehva.eu/activities/covid19-guidance.
[6] Y. Bian, X. Fu, B. Liu, R. Rachala, R. K. Gupta, Y. Shi, Bear-data:
Analysis and applications of an open multizone building dataset, in:
Proceedings of the 10th ACM International Conference on Systems
for Energy-Efficient Buildings, Cities, and Transportation, 2023, pp.
240–243.
[7] J. Drgoňa, J. Arroyo, I. C. Figueroa, D. Blum, K. Arendt, D. Kim,
E. P. Ollé, J. Oravec, M. Wetter, D. L. Vrabie, et al., All you need to
know about model predictive control for buildings, Annual Reviews
in Control 50 (2020) 190–232.
[8] Y. Chen, Y. Shi, B. Zhang, Optimal control via neural networks: A
convex approach, in: International Conference on Learning Representations, 2018.
[9] Y. Gao, S. Miyata, Y. Akashi, Energy saving and indoor temperature
control for an office building using tube-based robust model predictive
control, Applied Energy 341 (2023) 121106.
[10] W. Su, Z. Ai, J. Liu, B. Yang, F. Wang, Maintaining an acceptable
indoor air quality of spaces by intentional natural ventilation or intermittent mechanical ventilation with minimum energy use, Applied
Energy 348 (2023) 121504.
[11] Y. Du, H. Zandi, O. Kotevska, K. Kurte, J. Munk, K. Amasyali, E. Mckee, F. Li, Intelligent multi-zone residential hvac control strategy
based on deep reinforcement learning, Applied Energy 281 (2021)
116117.
[12] T. Yang, L. Zhao, W. Li, J. Wu, A. Y. Zomaya, Towards healthy and
cost-effective indoor environment management in smart homes: A
deep reinforcement learning approach, Applied Energy 300 (2021)
117335.
[13] H. Wang, X. Chen, N. Vital, E. Duffy, A. Razi, Energy optimization
for hvac systems in multi-vav open offices: A deep reinforcement
learning approach, Applied Energy 356 (2024) 122354.
[14] W. Shang, J. Liu, C. Wang, J. Li, X. Dai, Developing smart air purifier
control strategies for better iaq and energy efficiency using reinforcement learning, Building and Environment 242 (2023) 110556.
[15] C. Li, C. Cui, M. Li, A proactive 2-stage indoor co2-based demandcontrolled ventilation method considering control performance and
energy efficiency, Applied Energy 329 (2023) 120288.
[16] B. Li, B. Wu, Y. Peng, W. Cai, Tube-based robust model predictive control of multi-zone demand-controlled ventilation systems for
energy saving and indoor air quality, Applied Energy 307 (2022)
118297.
[17] W. Tian, X. Han, W. Zuo, M. D. Sohn, Building energy simulation
coupled with cfd for indoor environment: A critical review and recent
applications, Energy and Buildings 165 (2018) 184–199.
[18] N. Bianco, A. Fragnito, M. Iasiello, G. M. Mauro, A cfd multiobjective optimization framework to design a wall-type heat recovery
and ventilation unit with phase change material, Applied Energy 347
(2023) 121368.
[19] H. Gao, W. Qian, J. Dong, J. Liu, Rapid prediction of indoor airflow
field using operator neural network with small dataset, Building and
Environment 251 (2024) 111175.
[20] A. Bulińska, Z. Popiołek, Z. Buliński, Experimentally validated cfd
analysis on sampling region determination of average indoor carbon
dioxide concentration in occupied space, Building and Environment
72 (2014) 319–331.
[21] J. Mou, S. Cui, D. W. Y. Khoo, Computational fluid dynamics modelling of airflow and carbon dioxide distribution inside a seminar room
for sensor placement, Measurement: Sensors 23 (2022) 100402.
[22] M. Ning, S. Mengjie, C. Mingyin, P. Dongmei, D. Shiming, Computational fluid dynamics (cfd) modelling of air flow field, mean age of

Page 12 of 14

Operator learning for energy-efficient building ventilation control
air and co2 distributions inside a bedroom with different heights of
conditioned air supply outlet, Applied Energy 164 (2016) 906–915.
[23] M. M. A. Mahmoud, P. Bahl, A. d. A. Aquino, C. Maclntyre, S. Bhattacharjee, D. Green, N. Cooper, C. Doolan, C. de Silva, A numerical
framework for the analysis of indoor air quality in a classroom, Journal
of Building Engineering 92 (2024) 109659.
[24] C. Michoski, M. Milosavljević, T. Oliver, D. R. Hatch, Solving
differential equations using deep neural networks, Neurocomputing
399 (2020) 193–212.
[25] Y. Bian, X. Fu, R. K. Gupta, Y. Shi, Ventilation and temperature
control for energy-efficient and healthy buildings: A differentiable
PDE approach, Applied Energy 372 (2024) 123477.
[26] Z. Li, N. B. Kovachki, K. Azizzadenesheli, K. Bhattacharya, A. Stuart, A. Anandkumar, et al., Fourier neural operator for parametric partial differential equations, in: International Conference on Learning
Representations.
[27] L. Lu, P. Jin, G. Pang, Z. Zhang, G. E. Karniadakis, Learning nonlinear operators via deeponet based on the universal approximation
theorem of operators, Nature machine intelligence 3 (3) (2021) 218–
229.
[28] Q. Zhou, R. Ooka, Neural network for indoor airflow prediction with
cfd database, in: Journal of Physics: Conference Series, Vol. 2069,
IOP Publishing, 2021, p. 012154.
[29] A. Warey, S. Kaushik, B. Khalighi, M. Cruse, G. Venkatesan, Datadriven prediction of vehicle cabin thermal comfort: using machine
learning and high-fidelity simulation results, International Journal of
Heat and Mass Transfer 148 (2020) 119083.
[30] Y. Wang, Z. Li, Z. Yuan, W. Peng, T. Liu, J. Wang, Prediction of
turbulent channel flow using fourier neural operator-based machinelearning strategy, Physical Review Fluids 9 (8) (2024) 084604.
[31] Z. Li, N. Kovachki, C. Choy, B. Li, J. Kossaifi, S. Otta, M. A.
Nabian, M. Stadler, C. Hundt, K. Azizzadenesheli, et al., Geometryinformed neural operator for large-scale 3d pdes, Advances in Neural
Information Processing Systems 36 (2024).
[32] Z. Hao, Z. Wang, H. Su, C. Ying, Y. Dong, S. Liu, Z. Cheng, J. Song,
J. Zhu, Gnot: A general neural operator transformer for operator
learning, in: International Conference on Machine Learning, PMLR,
2023, pp. 12556–12569.
[33] X. Ding, H. Zhang, W. Zhang, W. Zhang, Y. Xuan, A fourier neural
operator-based method for rapid prediction of 3d indoor airflow
dynamics, in: Building Simulation, Springer, 2025, pp. 1–17.
[34] P. Pant, R. Doshi, P. Bahl, A. Barati Farimani, Deep learning for
reduced order modelling and efficient temporal evolution of fluid
simulations, Physics of Fluids 33 (10) (2021).
[35] A. Bulińska, Z. Buliński, A cfd analysis of different human breathing
models and its influence on spatial distribution of indoor air parameters, Computer Assisted Methods in Engineering and Science 22 (3)
(2017) 213–227.
[36] Y. He, Y. Chu, H. Zang, J. Zhao, Y. Song, Experimental and cfd study
of ventilation performance enhanced by roof window and mechanical ventilation system with different design strategies, Building and
Environment 224 (2022) 109566.
[37] X. Sha, Z. Ma, S. Sethuvenkatraman, W. Li, Online learningenhanced data-driven model predictive control for optimizing hvac
energy consumption, indoor air quality and thermal comfort, Applied
Energy 383 (2025) 125341.
[38] S. Zhang, Z. Ai, Z. Lin, Novel demand-controlled optimization of
constant-air-volume mechanical ventilation for indoor air quality,
durability and energy saving, Applied Energy 293 (2021) 116954.
[39] Y. Chen, Y. Shi, B. Zhang, Modeling and optimization of complex
building energy systems with deep neural networks, in: 2017 51st
Asilomar Conference on Signals, Systems, and Computers, IEEE,
2017, pp. 1368–1373.
[40] A. C. D’Alicandro, A. Mauro, Experimental and numerical analysis
of co2 transport inside a university classroom: effects of turbulent
models, Journal of Building Performance Simulation 16 (4) (2023)
434–459.
[41] U. Manual, Ansys fluent 12.0, Theory Guide 67 (2009).

Yuexin Bian et al.: Preprint submitted to Elsevier

[42] M. Abuhegazy, K. Talaat, O. Anderoglu, S. V. Poroseva, Numerical
investigation of aerosol transport in a classroom with relevance to
covid-19, Physics of Fluids 32 (10) (2020).
[43] K. Weekly, N. Bekiaris-Liberis, M. Jin, A. M. Bayen, Modeling
and estimation of the humans’ effect on the co 2 dynamics inside a
conference room, IEEE Transactions on Control Systems Technology
23 (5) (2015) 1770–1781.
[44] ASHRAE Standard 55–thermal environmental conditions for human
occupancy, Tech. rep., ASHRAE Inc., Atlanta, GA (1992).
[45] B. Lakshminarayanan, A. Pritzel, C. Blundell, Simple and scalable
predictive uncertainty estimation using deep ensembles, Advances in
neural information processing systems 30 (2017).
[46] ASHRAE Standard 62.1–ventilation for acceptable indoor air quality,
Tech. rep., ASHRAE Inc., Atlanta, GA (2010).
[47] W. Zhang, W. Wu, L. Norford, N. Li, A. Malkawi, Model predictive
control of short-term winter natural ventilation in a smart building
using machine learning algorithms, Journal of Building Engineering
73 (2023) 106602.

A. Airflow dynamics modeling

Indoor air is modeled as an incompressible fluid consisting of four species, namely: oxygen (O2 ), carbon dioxide
(CO2 ), water steam (H2 O) and nitrogen (N2 ) [35], where
each gas species (O2 , CO2 , H2 O, N2 ) is assigned a constant
density. The numerical model is based on the Navier-Stokes
equations for incompressible flow, incorporating continuity, momentum, energy conservation, and turbulence model
equations, along with species transport equations.
The general form of the continuity equation is:
𝜕𝜌
+ ∇ ⋅ (𝜌𝒖) = 0,
𝜕𝑡

(14)

𝜕𝑌𝑖
1
+ ∇ ⋅ (𝑌𝑖 𝒖) = −∇ ⋅ 𝒋𝑖 ,
𝜕𝑡
𝜌

(15)

where 𝜌 is fluid density and 𝒖 is the velocity field. In
our simulations, ANSYS Fluent solves this equation under
the incompressible flow assumption by setting the density
𝜌 as constant. The conservation equations for air constituents govern the transport and distribution of individual
gas species within the airflow.

where 𝑖 denotes three air constituents, namely, O2 , CO2 and
H2 O, 𝑌𝑖 is the mass fraction of the 𝑖-th air constituent, and
𝜌 is density of fluid. The mass flux of the 𝑖-th constituent
can be calculated 𝒋𝑖 = −𝐷eff ∇𝑌𝑖 , where 𝐷eff is the effective
diffusion coefficient which includes turbulence effects. The
mass fraction of N2 was calculated from the sum of mass
fractions of all air species which should be equal to unity.
CO2 concentration can be converted from mass fraction of
CO2 with
𝐶(𝒙, 𝑡) = 𝑌CO2 (𝒙, 𝑡) ⋅ 106 ⋅

molecular weight of CO2
, (16)
molecular weight of air

where molecular weight of CO2 = 44.01g/mol and molecular weight of air is 28.97g/mol. The momentum equation
describes the motion of air as an incompressible fluid, governed by the Navier-Stokes equations:
𝜕(𝜌𝒖)
+ ∇ ⋅ (𝜌𝒖𝒖) = −∇𝑝 + 𝜌𝒈 + ∇ ⋅ (𝜇∇𝒖) − ∇ ⋅ 𝜏𝑡 , (17)
𝜕𝑡
Page 13 of 14

Operator learning for energy-efficient building ventilation control

where 𝑝 is the pressure field, 𝒈 is a vector of gravitational
acceleration, 𝜇 is a molecular dynamic viscosity and 𝜏𝑡 is a
turbulence tensor. The energy conservation equation governs
the transport of thermal energy within the airflow,
)
(
∑
𝜕(𝜌𝑒)
+ ∇ ⋅ (𝜌𝑒𝒖) = ∇ ⋅ (𝑘eff ∇𝑇 ) − ∇
ℎ𝑖 𝒋𝑖 , (18)
𝜕𝑡
𝑖
where 𝑒 is a specific internal energy, 𝑘eff is an effective
heat conductivity, 𝑇 is fluid temperature and ℎ𝑖 refers to a
specific enthalpy of fluid. The turbulence model equations
approximate the effects of small-scale turbulent eddies
)
(
𝜕𝒖𝑖 𝜕𝒖𝑗
2
+
− 𝜌𝜅𝛿𝑖𝑗 ,
𝜏𝑡,𝑖𝑗 = 𝜇𝑡
𝜕𝑥𝑗
𝜕𝑥𝑖
3
where 𝜇𝑡 is a turbulent viscosity, 𝜅 is a turbulent kinetic
energy and 𝛿𝑖𝑗 is Kronecker’s delta.
The domain boundary 𝜕𝑍 encompasses all surfaces,
including walls, ventilation interfaces, and occupant boundaries. We further define Ωsupply as the inlet vent boundary,
Ωoccupant as the occupant surface boundary, Ωreturn as the
outlet vent boundary. The airflow boundary conditions are
then given by:
⎡ sin(𝑚𝑎𝑖 (𝑡)) ⎤
⎥ , ∀𝒙 ∈ Ωsupply,𝑖 ,
0
⎥
𝑎
⎣− cos(𝑚𝑖 (𝑡))⎦

𝒖(𝒙, 𝑡) = 𝑚𝑟𝑖 (𝑡) ⎢
⎢
𝒖(𝒙, 𝑡) =

(19a)

⎡0⎤
⋅ 𝑁occupant ⋅ ⎢0⎥ , ∀𝒙 ∈ Ωoccupant ,
⎢ ⎥
𝐴occupant
⎣1⎦
(19b)
𝑣occupant

𝒏 ⋅ ∇𝒖 = 0, ∀𝑧 ∈ return ,

(19c)

𝒖(𝒙, 𝑡) = 0, ∀𝒙 ∈ 𝜕Ω ⧵ (Ωsupply ∪ Ωoccupant ∪ Ωreturn ).
(19d)

(19a) specifies that the airflow velocity at 𝑖-th group of
supply vents is determined by its corresponding airflow rate
𝑚𝑟𝑖 (𝑡) and direction angle 𝑚𝑎𝑖 (𝑡). (19b) relates the airflow
rate to the number of occupants, where the exhaled air rate
𝑣occupant is set to 6 L/min per person [36], and 𝐴occupant
denotes the occupant boundary area. Constraint (19c) sets
the Neumann boundary conditions at the return vent and
constraint (19d) applies Dirichlet conditions to all other
boundaries by setting the airflow velocity as zero [25].

B. Learning results of deep learning-based
reduced-order modeling of CFD data

We compare the proposed neural operator learning approach against a state-of-the-art deep learning-based reducedorder modeling for predicting the spatial-temporal dynamics of CO2 concentration and building ventilation control.
Specifically, follow the work [34], which employed 3D
autoencoder and U-Net architectures to perform nonlinear
reduced-order modeling of CFD dynamics. We then integrate this learned surrogate model into our ventilation
control optimization (5) to optimize control actions.
Yuexin Bian et al.: Preprint submitted to Elsevier

Model

Ours
DL-ROM

𝑙2
error
(train
dataset)
5.9%
8.4%

𝑙2
error
(test
dataset)
10.9%
9.6%

Control
Landscape
Error(CLE)
0.17
0.26

Table 6
𝑙2 error and Control Landscape Error (CLE) for each model,
with the best performance highlighted in bold.

Apart from 𝑙2 error, we propose a new metric, Control
Landscape Error (CLE), to quantify discrepancies between
ground-truth CFD results and model predictions (our neural
operator or DL-ROM [34]) under different control conditions. We generate 16 unique control combinations by
uniformly sampling airflow angles from 45◦ to 135◦ and
rates from 0 to 3.24 m/s, applied identically across all six
vents. For each, we simulate the future CO2 distribution
and use it to evaluate model accuracy across varying control
inputs. We include a representative visualization in Figure 9
to complement this quantitative evaluation. The control objective includes the term ‖𝐶̂ − 𝐶target ‖22 , which measures the
deviation of the predicted CO2 concentration from the target
value. We visualize this objective value (with CO2 concentrations standardized using Z-score normalization) for the
ground truth CFD simulations, our neural operator ensemble, and the DL-ROM baseline. Our model captures the
control-performance landscape more accurately, especially
in lower-velocity regimes (that saves energy), whereas DLROM tends to over-smooth the variations, particularly at the
extremes of the action space. This result demonstrates that
our neural operator preserves the input-output sensitivity of
the system, which is crucial for robust control optimization.
The model performance is reported in Table 6, where
CLE is defined as
1 ∑|
|
CLE =
|‖𝐶 − 𝐶target ‖22 − ‖𝐶𝑖,model − 𝐶target ‖22 | ,
|
𝑁 𝑖=1 | 𝑖,gt
(20)
where 𝐶𝑖,gt and 𝐶𝑖,model denote the ground truth and modelpredicted CO2 fields for the 𝑖-th control input, and 𝑁 is
the number of evaluated inputs. Here, we generate 2 test
samples (requiring approximately 32 CPU hours in total),
each containing 16 control input pairs, resulting in 𝑁 =
32 evaluations. While DL-ROM achieves a slightly lower
𝑙2 error on the test set, our operator-based model attains
a lower CLE, indicating better accuracy in capturing the
control-response relationship. This highlights a key strength
of our method: although the global 𝑙2 error is comparable,
our model more faithfully preserves the sensitivity of CO2
outcomes to varying control inputs.
𝑁

Page 14 of 14

Operator learning for energy-efficient building ventilation control

Figure 7: Time series of control actions of our approach. Top
plot shows the airflow angles and bottom shows airflow rates
for 6 group of inlet vents under dynamic occupancy levels.

Figure 8: Control actions (flow rates and angles) for individual
models (Model 1 to Model 5) and the ensemble model across
six inlet vents for one case. The ensemble model consistently
achieves maximum airflow rates for all inlet vents.

Yuexin Bian et al.: Preprint submitted to Elsevier

Page 15 of 14

Operator learning for energy-efficient building ventilation control

Figure 9: Visualization of control objective values ‖𝐶̂ − 𝐶target ‖22 across a grid of control inputs (airflow rate and vent angle),
evaluated using (left) ground truth CFD simulations, (middle) our neural operator ensemble, and (right) DL-ROM [34].

Yuexin Bian et al.: Preprint submitted to Elsevier

Page 16 of 14
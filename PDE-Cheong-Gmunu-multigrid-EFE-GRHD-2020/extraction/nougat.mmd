Gmunu: Toward multigrid based Einstein field
equations solver for general-relativistic
hydrodynamics simulations
Patrick Chi-Kit Cheong

arXiv:2001.05723v2 [gr-qc] 14 Apr 2020

E-mail: chi-kit.cheong@ligo.org

Lap-Ming Lin
E-mail: lmlin@cuhk.edu.hk

Tjonnie Guang Feng Li
E-mail: tgfli@cuhk.edu.hk
Department of Physics, The Chinese University of Hong Kong, Shatin, N. T., Hong
Kong
Abstract.
We present a new open-source axisymmetric general relativistic hydrodynamics
code Gmunu (General-relativistic multigrid numerical solver) which uses a multigrid
method to solve the elliptic metric equations in the conformally flat condition (CFC)
approximation on a spherical grid. Most of the existing relativistic hydrodynamics
codes are based on formulations which rely on a free-evolution approach of numerical
relativity, where the metric variables are determined by hyperbolic equations without
enforcing the constraint equations in the evolution. On the other hand, although
a fully constrained-evolution formulation is theoretical more appealing and should
lead to more stable and accurate simulations, such an approach is not widely
used because solving the elliptic-type constraint equations during the evolution is
in general more computationally expensive than hyperbolic free-evolution schemes.
Multigrid methods solve differential equations with a hierarchy of discretizations and
its computational cost is generally lower than other methods such as direct methods,
relaxation methods, successive over-relaxation. With multigrid acceleration, one can
solve the metric equations on a comparable time scale as solving the hydrodynamics
equations. This would potentially make a fully constrained-evolution formulation
more affordable in numerical relativity simulations. As a first step to assess the
performance and robustness of multigrid methods in relativistic simulations, we develop
a hydrodynamics code that makes use of standard finite-volume methods coupled with
a multigrid metric solver to solve the Einstein equations in the CFC approximation.
In this paper, we present the methodology and implementation of our code Gmunu
and its properties and performance in some benchmarking relativistic hydrodynamics
problems.

Gmunu: Multigrid methods for solving Einstein field equations

2

Keywords: Article preparation, IOP journals Submitted to: Class. Quantum Grav.

1. Introduction
In the past decade, numerical relativity has matured to the state that stable and robust
numerical calculations of the Einstein equations with or without matter has become
feasible. The spacetimes of many interesting astrophysical systems such as stellar core
collapses and binary systems of compact objects have been accurately modeled (see, e.g.,
[43, 14, 13] for recent reviews). In the standard 3 + 1 decomposition of spacetime, the
Einstein equations are split into a set of evolution equations and constraint equations.
Nevertheless, one still has the freedom to choose the basic variables to evolve and
reformulate the resulting systems of differential equations in order to improve the
stability and accuracy of numerical simulations. This results in different formulations of
numerical relativity, such as the so-called BSSN [49, 2], CCZ4 [7], and Z4c [6] schemes,
which are popular choices for numerical modelings. The practical applications of these
different formulations are based on a free-evolution approach where the constraint
equations are first solved for preparing the initial data and used subsequently only
as an indicator to monitor the numerical accuracy during the evolution (see, e.g., [37]).
Alternatively, one can also formulate the Einstein equations based on a fully
constrained-evolution approach where the constraint equations are solved and fulfilled
to within the discretization errors during the evolution. Despite the fact that a
constrained-evolution approach is theoretical appealing, such an approach is not
popular among numerical relativists since solving the elliptic-type constraint equations
during the evolution is generally computational expensive. In contrast to the
active development and applications of free-evolution formulations, the last proposed
constrained formulation of the Einstein equations was already 15 years ago due to
Bonazzola et al. [8]. The fully constrained-evolution formulation of Bonazzola et al.
[8] has been employed to simulate pure gravitational wave spacetime [8], and also an
oscillating neutron star by ignoring the back-reaction of the gravitational waves into the
fluid dynamics [16]. However, the application of this constrained scheme and assessment
of its performance in modelling more generic dynamical spacetimes without symmetry
is still a largely unexplored area.
It is worth to point out that the fully constrained scheme of Bonazzola et al. [8]
automatically reduces to the so-called conformally flat condition (CFC) approximation
to general relativity [55, 32] if a tensor field hij introduced in their formulation is
set to zero (see [15] for a detailed discussion). The CFC approximation results in a
simpler set of elliptic equations for the metric sector. Numerical simulations based on
the CFC scheme have been successfully carried out for various astrophysical problems
[18, 40, 48, 4, 3, 5, 38] and the scheme has also been shown to be a good approximation
to full general relativity in rotating iron core collapses [41]. However, the original CFC
scheme suffers from mathematical non-uniqueness problems when the system is too

Gmunu: Multigrid methods for solving Einstein field equations

3

compact. In order to overcome the non-uniqueness issue, the scheme was reformulated
and extended to the so-called extended CFC (xCFC) scheme so that the modelling of
extreme spactimes such as black hole formation becomes possible [15, 39, 16].
We have in our mind a motivation to experiment and develop our own general
relativistic hydrodynamics code based on the fully constrained formulation of Bonazzola
et al. [8] (or other similar constrained formulations if available in the future) which
maximizes the use of elliptic-type equations for the metric sector of the system in
the evolution. In this paper, we take a first step along this direction by developing
a relativistic hydrodynamics code based on the xCFC scheme. Although it is not fully
general relativistic, the xCFC scheme contains a set of similar, but simpler, elliptic
equations as the fully constrained formulation. We can thus use the xCFC scheme to
evaluate the performance and robustness of our metric solver.
As already pointed out, it is known in general that solving the elliptic equations
frequently in a fully constrained or xCFC scheme during a simulation is computationally
expensive. Many numerical methods have been explored to deal with such elliptic
systems, including finite-difference methods, different types of iterative solvers, and
spectral methods (see [17, 19, 12] and references therein). A seminal work is due
to Dimmelmeier et al. [19] which combines a finite-difference grid and a spectral
grid, on which the hyperbolic hydrodynamics and elliptic metric equations are solved,
respectively. However, even though the spectral method is known to be extremely
fast and accurate, the metric solver is still one of the bottlenecks to slow down a
hydrodynamics simulation as the communication between variables defined on the two
different grids is time consuming especially in the multidimensional cases [20, 19]. In this
work, we demonstrate that our nonlinear cell-centred multigrid method is not only an
efficient strategy to solve the elliptic metric equations, but also can be straightforwardly
used in hydrodynamical simulations.
Multigrid methods solve differential equations with a hierarchy of discretizations
and its computational cost is generally lower than other methods such as direct methods,
relaxation methods, and successive over-relaxation [28]. The multigrid strategy has been
employed in a wide range of problems and it has also been used to generate initial data
in numerical relativity [31, 22, 36]. However, multigrid methods have not been applied
in any constrained-evolution schemes for numerical relativity. In order to couple to
the matter directly, nonlinear cell-centred multigrid (CCMG) and the corresponding
boundary treatments are needed, the latter of which is more complicated than the
vertex-centred multigrid and is still being actively studied in the computational physics
and applied mathematics.
Our aim is to construct a direct, rapid, and robust multidimensional metric solver
which can be easily coupled to the matter based on the non-linear cell-centred multigrid
strategy. In this paper, we present the methodology and implementation of our new
open-source axisymmetric general relativistic hydrodynamics code Gmunu (Generalrelativistic MUltigrid NUmerical solver), which solves the hydrodynamics equations
using standard finite-volume methods and the xCFC metric equations using a multigrid

4

Gmunu: Multigrid methods for solving Einstein field equations

approach on a spherical grid. Gmunu is written in the Fortran90 programming language
and is released as open source. To the best of our knowledge, this is the first relativistic
hydrodynamics code that makes use of a multigrid solver in dynamical simulations.
We also perform various benchmarking tests in relativistic hydrodynamics to assess the
performance and robustness of our code.
The paper is organised as follows. In section 2 we outline the formalism we used in
this work. The details of the numerical settings and, the methodology, implementation
of our hydrodynamics solver and our multigrid solver are presented in section 3 and
section 4 respectively. The code tests and results are presented in section 5 and section 6.
The performance of our multigrid solver is presented in section 7. This paper ends with
a discussion section in section 8.
2. Formulations
2.1. Metric equations and Conformal flatness approximation
We use the standard ADM 3+1 formalism [27, 1]. The metric can be written as


ds2 = −α2 dt2 + γij dxi + β i dt dxj + β j dt ,

(1)

where α is the lapse function, β i is the spacelike shift vector and γij is the spatial metric.
In the 3+1 formalism, the Einstein equations are split into a set of constraint equations
which must be satisfied on every hypersurface
R + K 2 − Kij K ij = 16πE,
ij

ij

(2)

i

∇i (K − γ K) = 8πS ,

(3)

and a set of the evolution equations for γij and the extrinsic curvature Kij
∂t γij = − 2αKij + ∇i βj + ∇j βi ,


k

∂t Kij = − ∇i ∇j α + α Rij + KKij − 2Kik Kj
k

k

+ β ∇k Kij + Kik ∇j β + Kjk ∇i β

− 4πα 2Sij − γij Skk − E ,

k

(4)
(5)

where ∇i is the covariant derivative with respect to the three-metric γij , Rij is the
corresponding Ricci tensor, R is the scalar curvature and K is the trace of the
extrinsic curvature Kij . For the matter sources, E := nµ nν T µν , S i := −nµ γνi T µν and
S ij := γµi γνj T µν , where T µν is the energy-momentum tensor and nµ is the unit normal
vector of a spacelike hypersurface.
It is difficult to maintain the constraint equations in the numerical evolution of
the evolution equations above because these ADM equations are numerically unstable.
There are serveral different re-formulations of 3 + 1 numerical relativity that can lead to
stable evolutions [49, 2, 7, 6]. However, these schemes are based on a free-evolution
approach where the Einstein equations are evolved with hyperbolic-type equations.

Gmunu: Multigrid methods for solving Einstein field equations

5

The constraint equations are only used for solving the initial data and serve as a
monitor for numerical errors during the simulations. On the other hand, a fullyconstrained evolution approach where the constraints are enforced at each time step is
generally not favored as solving the elliptic-type constraint equations is computational
expensive comparing to hyperbolic equations [45]. We have a motivation to develop and
experiment efficient multigrid solvers for elliptic-type metric equations that one needs
in order to carry out fully-constrained evolutions for numerical relativity. As a first step
towards this goal, our relativistic hydrodynamics code employs the xCFC scheme which
is an improved version of the CFC approximation to general relativity.
In a CFC approximation [17, 12], the three metric γij is assumed to be decomposed
according to
γij := ψ 4 fij ,
(6)
where fij is a time independent flat background metric and ψ is the conformal factor
which is a function of space and time. Another assumption is the maximal slicing
condition of foliations
K = 0.
(7)
With these conditions, one can derive the time derivative of the conformal factor ψ and
also the extrinsic curvature Kij
ψ
∇k β k ,
6 

1
2
k
Kij =
∇i βj + ∇j βi − γij ∇k β .
2α
3

∂t ψ =

(8)
(9)

The CFC approximation of the ADM equations can be reduced into five coupled nonlinear elliptic equations


1
ij
˜
∆ψ = −2πE − K Kij ψ 5 ,
(10)
8


7
ij
5
˜
(11)
∆(αψ) = αψ 2π (E + 2S) + Kij K ,
8



˜ i + 1∇
˜i ∇
˜ j β j = 16παψ 4 f ij Si + 2ψ 10 K ij ∇
˜ j αψ −6 ,
∆β
(12)
3
˜ i and ˜
where ∇
∆ are the covariant derivative and the Laplacian with respect to the flat
three metric fij , respectively.
The original CFC scheme suffers from mathematical non-uniqueness problems. The
CFC scheme was later reformulated so that the elliptic equations are fully decoupled
and the local uniqueness of the solution is guaranteed. The reformulated CFC scheme
is the so-called xCFC scheme [15], which is the scheme that we implemented in Gmunu.
In the xCFC scheme, one introduces a vector potential X i , and the metric can be solved

Gmunu: Multigrid methods for solving Einstein field equations

6

by the following equations:


˜i ∇
˜ i + 1∇
˜ j X j = 8π S̃ i ,
∆X
3
˜ = −2π Ẽψ −1 − 1 fik fjl Ãkl Ãij ψ −7 ,
∆ψ
 8


7
kl
ij
−8
−2
˜
∆(αψ)
= (αψ) 2π Ẽ + 2S̃ ψ + fik fjl Ã Ã ψ
,
8

1 ˜ i  ˜ j
˜
˜ j αψ −6 ,
∆β i + ∇
∇j β = 16παψ −6 f ij S̃i + 2Ãij ∇
3

(13)
(14)
(15)
(16)

where Ẽ := ψ 6 E, S̃i := ψ 6 Si and S̃ := ψ 6 S are the rescaled fluid source terms.
The tensor field Ãij can be approximated on the CFC approximation level by (see
the Appendix of [15]):
˜ k X k f ij .
˜ iX j + ∇
˜ jXi − 2∇
Ãij ≈ ∇
3

(17)

2.2. General relativistic hydrodynamics equations
The evolution equations for the matter are derived from the local conservations of the
rest-mass and energy-momentum:
∇µ (ρuµ ) = 0 and ∇ν T µν = 0,

(18)

where ρ is the rest-mass density of the fluid and uµ is the fluid four-velocity. For a
perfect fluid, the energy-momentum tensor is given by T µν = ρhuµ uν + P g µν , where P
is the pressure, h = 1 +  + P/ρ is the enthalpy, and  is the specific internal energy.
The three-velocity v i of the fluid as measured by the Eulerian observers of four-velocity
βi
ui
nµ is given by v i = αu
0 + α . In the flux-conservative Valencia formulation (e.g., [25]),
the set of hydrodynamics equations are given by
√
√
√
∂t ( γU ) + ∂i ( −gF i ) = −gQ,

(19)

where
  

D
ρW
  

U = Sj  = 
ρhW 2 vj
,
2
τ
ρhW − P − D


D (v i − β i /α)


F i = Sj (v i − β i /α) + δji P  ,
τ (v i − β i /α) + P v i


0




∂g
Q =  T µν ∂xνjµ − Γλµν gλj  .

ln α
µν 0
α T µ0 ∂∂x
Γµν
µ − T

(20)

(21)

(22)

Gmunu: Multigrid methods for solving Einstein field equations

7

As shown in Eq. (22), the source terms Q contain the time derivatives of the metric
quantities. In order to reduce the accumulated error due to the time update, it is good
to avoid the time derivatives in the code. We can rewrite the Qj terms into compact
form [19]
∂gµν
1
.
(23)
Qj = T µν
2
∂xj
It is also possible to bypass the time derivatives in the Qτ term (i.e., the last element
of the vector in Eq. (22)):

(24)
Qτ =T 00 Kij β i β j − β k ∂k α

+ T 0j 2Kjk β k − ∂j α + T ij Kij .

In order to adapt to the extended CFC scheme, we have to evolve the conformal
transformed conserved quantities, the (non-conformal transformed) conserved variables
and thus the primitive variables will be updated once the conformal factor ψ is solved.
In particular, we define Ũ ≡ ψ 6 U , F̃ i ≡ ψ 6 F i and Q̃ ≡ ψ 6 Q. We can then
reformulate the hydrodynamics equations as

∂ Ũ
1 ∂  2 r
1 ∂ 
+ 2
αr F̃ +
α sin θF̃ θ = αQ̃.
∂t
r ∂r
sin θ ∂θ

(25)

In the case that we need to solve the metric, we pass the conformal conserved quantities
into the metric solver. Both metric quantities and primitive hydrodynamic variables
will then be updated.
3. Numerical methods and implementation
We use spherical polar coordinates {r, θ, φ} and adopt the axial symmetry with cellcentered discretization. In particular, the coordinate grid covers 0 < r < rmax and
0 < θ < π/2 and we discretize it into nr × nθ cells with uniform coordinate grid spacing,
i.e. ∆r = rmax /nr and ∆θ = π/2nθ .
Gmunu solves the general relativistic hydrodynamic equations by using standard
high-resolution shock-capturing (HRSC) schemes [33]. In particular, various different
cell-interface reconstruction methods and Riemann solvers are implemented and tested.
For the cell-interface reconstruction, we have implemented piecewise constant scheme
(PC), monotonized-central limiter (MC), 5th order weighted-essentially nonoscillatory
scheme (WENO5) [50] and 5th order monotonicity preserving scheme (MP5) [52]. For
the Riemann solver, the Rusanov flux (also known as Total variation diminishing LaxFriedrichs scheme (TVDLF)) [53], Harten-Lax-van Leer (HLL) [30], Harten-Lax-van
Leer-Einfeldt (HLLE) [23, 29], Marquina flux formula [21] have been implemented.
For the recovery of the primitive variables (ρ, vi , P ) from the conservative variables
(D, Si , τ ), we follow the formulation presented in the Appendix C in [26] and use
Regula-Falsi method to find the root. This formulation was shown to be not only robust,
accurate and efficient, but also suitable for different kinds of relativistic hydrodynamical

Gmunu: Multigrid methods for solving Einstein field equations

8

simulations [47, 26]. For the region outside the star, we fill with an “atmosphere” of
density ρatmo = 10−6 ρmax (t = 0), where ρmax (t = 0) is the maximum density over the
whole computational domain initially at time t = 0, and use the standard atmosphere
treatment during the simulation. In particular, if the density at a particular grid drops
below ρatmo , the density at that grid is reset to ρatmo . The velocity of that grid is also set
to be zero and other primitive variables such as the specific internal energy  is updated
accordingly.
Unless otherwise specified, the simulations reported in this paper were preformed
with HLLE Riemann solver and the MC reconstruction method. We also use a 3rd
order Runge-Kutta integrator for the time integration. It is not necessary to solve the
metric at each time step [17, 12]. To speed up the simulations, we solve the metric
at every 50 time steps, and extrapolate the metric in between. Detailed analysis of
frequency of solving the metric can be found in section 7.2. A practical difficulty related
to spherical coordinates is that the convergence of grid points near the pole axis puts
a severe constraint on the time step imposed by the Courant-Friedrichs-Levy stability
condition in numerical simulations. In order to increase the size of the time steps in our
simulations, we treat the first 10 grid points, which cover about 5% of the stellar radius,
as a spherically symmetric core (i.e., only radial motions are allowed). This should be a
good approximation as non-radial fluid motions in the core is negligibly small. We used
the open-source code XNS [12, 42, 43, 44], which is also based on the CFC approximation,
to generate initial neutron-star models for our dynamical simulations.
4. Nonlinear cell-centered multigrid metric solver
4.1. Metric solver with xCFC scheme
By following [15], the metric equations Eqs. (13)-(16) can be decoupled, thus they
can be solved in a hierarchical way and the local uniqueness is guaranteed. Once
the time integration at each time step for the hydrodynamics equations is completed,
the conformally rescaled hydrodynamical conserved variables (D̃, S̃i , τ̃ ) are updated,
and they will be used to solve the metric equations. The steps for solving the metric
equations are summarized in the following:
(i) Solve Eq. (13) for the vector potential X i from the conserved variables S̃i .
(ii) Calculate the tensor Ãij in Eq. (17) from the vector potential X i .
(iii) Solve Eq. (14) for the conformal factor ψ.
(iv) With the updated conformal factor ψ, calculate the conserved variables (D, Si , τ )
and thus convert the conserved variables to the primitive variables (ρ, vi , P ). Then
S̃ can be worked out consistently.
(v) Solve Eq. (15) for the lapse function α.
(vi) Solve Eq. (16) for the shift vector β i .

Gmunu: Multigrid methods for solving Einstein field equations

9

To solve the metric equations, appropriate boundary conditions at the origin and
outer computational boundary are required. In the practical simulations of spheric-like
astrophysical systems (e.g. isolated neutron star and core-collapse supernova), as the
spacetime at the star surface is close to spherically symmetric, setting the Schwarzschild
solution as the outer boundary condition is usually a good approximation [17, 19]. In
order to let the solution fall off as the Schwarzschild solution at large distance, we require
ψ = Cr + 1, α = Cr + 1 and X i = β i = 0 at the outer boundary (r = rmax ). In Gmunu, we
impose the boundary conditions
∂ψ
1−ψ
,
=
∂r rmax
r
∂α
1−α
,
=
∂r rmax
r
βi
Xi

rmax
rmax

(26)
(27)

= 0,

(28)

= 0.

(29)

More detailed implementation of the metric equations and boundary conditions at the
axis and the origin can be found in Appendix A.
4.2. An overview of multigrid
Multigrid is an efficient method for solving elliptic partial differential equations with low
memory and work complexity. Different modes are filtered out with different rates at
different resolutions. For some low-frequency modes, it is computationally expensive to
compute directly on a high-resolution discretization. However, it can be done efficiently
at a low-resolution discretization. The main concept of the multigrid method is to solve
the problem recursively with a series of coarse grids. It is noted that the multigrid
method is not a single method but a strategy with many possible implementations.
However, the elements needed to construct a multigrid solver is more or less the same
for different implementations. For instance, as shown in figure 1, the key ingredients of
multigrid solver includes (1) a cycle framework, the backbone of the whole solver which
describe the structure of the multigrid solver (see figure 1 for examples), (2) inter grid
transfer operators to connect the solver with different levels, where the operators that
map the values from a fine to a coarse grid are called restriction and the mapping from a
coarse to the fine grid are called prolongation. (3) smoothers to smooth the solutions at
different resolutions and (4) direct solvers to obtain the solutions at the coarsest level.
4.3. Nonlinear multigrid: The Full Approximation Scheme
Due to the nonlinearity of the Einstein equations needed to be solved (i.e. Eqs. (13)(16)), nonlinear multigrid method is required. The implementations for the multigrid
for non-linear elliptic equations are different from the linear cases. Two well-known
methods for solving non-linear partial differential equations with multigrid techniques

10

Gmunu: Multigrid methods for solving Einstein field equations
S

S

S

S

S

S

S

S

S

S

S

S

Sol

Sol

(a) V-cycle

S

S

S

Sol

S

Sol

(b) F-cycle

S

S

S

S

S
S

S

S

S

S

S

Sol

Solver

S

Smoother
Restriction

S

S

S

Sol

Sol

Sol

S

Sol

Prolongation

S

(c) W-cycle

Figure 1: Three types of (4-grid) cycles can be used in multigrid methods. “S” denotes
smoothing while “Sol” denotes solving the equation directly. Each descending line
\ represents restriction and each ascending line / represents prolongation. The key
ingredients of multigrid solver includes a cycle framework, restriction and prolongation
operators, smoothers and solvers.
are the Full Approximation Scheme (FAS) [10] and Newton-multigrid (Newton-MG)
[11, 54]. The two methods are widely used and obtained successes in various problems.
We refer the interested reader to [9] for a detailed comparison of the two methods. Due
to the fact that the memory used is low in FAS, the current version of Gmunu adopts
the FAS algorithm (see [10, 9, 46] and references therein for more details).
Here we briefly outline how the Full Approximation Scheme works. To solve an
nonlinear elliptic equation L(u) = f , where L is some elliptic operator, u is the solution
and f is the source term, we can discretize the equation on a grid with resolution h as
Lh (uh ) = fh .

(30)

Suppose we have obtained an approximate solution ũh through the smoothing processes
(note that smoothers is a kind of solver, but slow), we can find the desired correction
eh so that the equation Lh (ũh + eh ) = fh is solved. The residual rh is defined by
rh :=Lh (ũh + eh ) − Lh (ũh )
=fh − Lh (ũh )

(31)

By transfering the first line of the Eq. (31) to a coarse grid with resolution 2h through
the restriction operator R, we have
L2h (u2h ) = R(uh ) − L2h (R(ũh )).

(32)

Gmunu: Multigrid methods for solving Einstein field equations

11

Note that the RHS of Eq. (32) can now be treated as a new source term, that is,
f2h := R(uh ) − L2h (R(ũh )). Let v denote the approximate solution of Eq. (32), we can
then obtain the coarse-grid correction:
ẽ2h = v − R(uh ),

(33)

and thus the new approximate solution on resolution h is
=ũh + P(ẽ2h )
ũnew
h

=ũh + P(v − R(uh )),

(34)

where P is the prolongation operator. Note that FAS can also be used to solve linear
elliptic equations. Algorithm 1 shows the pseudocode of a single cycle of the non-linear
multigrid elliptic partial differential equation solver implemented in Gmunu.
Algorithm 1:
A single cycle of the non-linear multigrid elliptic partial
differential equation solver implemented in Gmunu.
/* Before solving any equations, we have to initialize the γ based
on what cycle type we want to use. In particular:
*/
/* V-cycle: set γ = 1
*/
/* W-cycle: set γ = 2
*/
/* F-cycle: set γ = 2
*/
/*
*/
MG(ul , fl )
if l = 1 then
ul ← Solve(ul )
if F-cycle then
γ←1
end
else
ul ← Smoothing(ul , fl ) ;
/* Pre-smoothing */
rl ← fl − Ll (ul ) ;
/* calculating the residual */
rl−1 ← Restriction(rl ) ;
/* restriction of the residual */
ul−1 ← Restriction(ul ) ;
/* restriction of the solution */
fl−1 ← rl−1 + Ll−1 (ul−1 ) ;
v ← ul−1 ;
/* Recursive call for the coarse grid correction
*/
for i = 1 to γ do
v ← MG(v, fl−1 )
end
ul ← ul + Prolongation(v − ul−1 ) ;
/* Prolongation */
ul ← Smoothing(ul , fl ) ;
/* Post-smoothing */
if finest level and F-cycle then
γ←2
end
end

Gmunu: Multigrid methods for solving Einstein field equations



1


4


1
1

1
∗

1

h







2h

(a) piecewise constant restriction



1
 3
1 


16 
 3
1

12

h
3 1
9 3 


∗


9
9 3 
3
3 1 2h
3
9

(b) bi-linear prolongation

Figure 2: The stencil notation of the interpolation operators implemented in Gmunu.
The “*” denotes the location of the coarse grid node. The notation shows the weighting
of the value which are the neighbors of the coarse grid node “*”.
4.4. Cell-centered discretization and intergrid transfer operators
As mentioned in section 2.1, the source terms of the metric equations consist of the
hydrodynamical variables. Meanwhile, since Gmunu solves the hydrodynamics with
finite volume approach, the grids are discretized with cell-centred discretization. On
the other hand, the discretization for the metric solver is in general different from the
hydrodynamics sector. For instance, for the pseudospectral method, the choice of grid
points has to be consistent with the basis functions which can not be chosen arbitrarily.
The corresponding interpolation or extrapolation are needed so that the hydrodynamical
variables can be passed correctly into the metric solver (e.g. [19, 12]), which might be
another bottleneck of the computational time of the simulations. In order to adapt the
grid of the hydrodynamics sector so that the hydrodynamical variables can be passed
into the metric solver without any interpolation or extrapolation, we implemented the
cell-centred multigrid (CCMG) [35, 28], which is one of the novelties of Gmunu.
Constructing a cell-centred multigrid solver is non-trivial. Unlike the vertex-centred
case, in which a node of the coarse grid is also a node of the fine grid, the nodes on coarser
grids do not form a subset of the fine grid nodes in the case of cell-centred discretization.
The choices of inter-grid transfer operators and the boundary condition implementation
are different from the vertex-centred cases. There are also many possible approaches
for different situations. Indeed, constructing problem-independent efficient cell-centred
transfer operators is still under an active research area in computational physics and
applied mathematics (see [35] and references therein).
There are many possible choices of restriction and prolongation operators and they
cannot be chosen arbitrarily [35, 28]. In Gmunu, we adopt the most standard combination,
i.e., piecewise constant restriction (figure 2a) and bi-linear prolongation (figure 2b).
4.5. Key features of the nonlinear cell-centered multigrid metric solver in Gmunu
This section shortly summarizes the key features of the metric solver implemented in
Gmunu. In our multigrid metric solver, we adopt the Full Approximation Storage (FAS)

Gmunu: Multigrid methods for solving Einstein field equations

13

to deal with the nonlinear metric equations with V-, W- and F-cycle implemented.
For the smoother and solvers, we use the standard red-black nonlinear Gauss-Seidel
relaxation [46]. In particular, the smoother consists of 15-times relaxations and the
direct solver consists of 200-times relaxations. For the inter-grid transfer operators, we
adopt piecewise constant restriction (figure 2a) and bi-linear prolongation (figure 2b).
Note that multigrid solvers are iterative solvers. Practically, this function has to be
called until the solution converges, i.e., when the L∞ or L1 norm of the residual is below
some chosen threshold value.
5. Code tests 1: Hydrodynamics solver
We present a set of numerical tests of Gmunu. Table 1 lists the models we used in various
tests. The name of the models are originally defined in the literature [20, 15]. All the
models are constructed with the polytropic equation of state with Γ = 2 and K = 100
(in units of (c = G = M = 1)).
Table 1: The equilibrium neutron star models we used in this paper. The name of the
models are originally defined in the literature [20, 15]. “BU” represents a sequence of
fixed central rest-mass density ρc = 1.28 × 10−3 uniformly rotating models, and “SU”
is a nonrotating unstable model. All the models are constructed with the polytropic
equation of state with Γ = 2 and K = 100. Ω is the angular velocity; M is the
gravitational mass; re and rp are the equatorial and polar radii, respectively. Unless
otherwise noted, we use units where c = G = M = 1.
Model
BU0
SU
BU2
BU8

ρc [10−3 ] Ω [10−2 ] M [M ]
re
rp /re
1.28
0.000
1.400
8.13 1.00
8.00
0.000
1.447
4.27 1.00
1.28
1.509
1.468
8.56 0.90
1.28
2.633
1.693
11.30 0.60

We first perform two standard tests in a static background metric, namely, (1)
the planar shocktube problem for special-relativistic hydrodynamics [34] and (2) the
evolution of a static stable neutron star on a fixed background metric in the Cowling
approximation [51]. In the following, we show the performance of Gmunu in these tests.
5.1. Relativistic shocktube
The shocktube problem is a standard test to access the shock-capturing ability of a
relativistic hydrodynamics code. In this test, we follow the setup proposed in [34]. In
particular, we assume flat spacetime and perform the simulation with planar geometry,
for x = [0, 1] with 1000 grid points. For the matter, we use the Γ-law equation of state
with Γ = 5/3, and the initial conditions are set in table 2. In this test, we used HLLE

14

Gmunu: Multigrid methods for solving Einstein field equations
Table 2: Initial conditions for the relativistic shocktube problem.
x < 0.5
x > 0.5
ρ = 10
ρ=1
P = 13.33 P = 0
v=0
v=0

ρ/10,P/20,v

as Riemann solver with WENO5 reconstruction and RK3 for time integration. Figure 3
shows the comparison between the numerical results and the analytic solutions for the
density, pressure and velocity profiles at t = 0.4. The figure shows that our numerical
results agree with the analytic solutions very well.
1.0

ρ/10

0.8

P/20
v

0.6
0.4
0.2
0.0
0.0

0.2

0.4

0.6

0.8

1.0

x

Figure 3: The density (red stars), pressure (blue squares) and velocity (green triangles)
are shown at t = 0.4 for the relativistic shocktube test problem. The solid lines are the
analytic solutions. The numerical results obtained by Gmunu agree very well with the
analytic solutions.

5.2. Spherical star evolutions with static metric
The test we report here is the evolution of a stable spherically symmetric neutron
star on a static background metric. Although it is an equilibrium solution of the
Einstein equations, the diffusion at the contact discontinuity of the neutron star surface
triggers the natural oscillation modes which were well studied for this kind of polytropic
star [51]. The oscillation modes of a neutron star can be obtained approximately by
perturbation calculations in the Cowling approximation [56, 51, 57]. They can also be
extracted by nonlinear hydrodynamical simulation with a fixed background metric. By
comparing the simulated results with the oscillation modes obtained in the Cowling

15

Gmunu: Multigrid methods for solving Einstein field equations

[ρc (t)/ρc (0) − 1] × 104

approximation, we can thus focus and check the correctness of our hydrodynamics
solver on a fixed background spacetime. In this test, we simulate the stable spherically
symmetric neutron star BU0 model as mentioned in the table 1. We setup a 1D run
with the resolution nr × nθ = 640 × 1 and keep the background metirc fixed during the
simulation.
The upper panel of figure 4 shows the relative variation of the central density ρc
as a function of time. The relative variation of the density is of the order 10−4 . The
oscillation modes extracted from the simulation also agree very well with those obtained
in the Cowling approximation.
2
0

−2
−4
0

2

4

6

8

10

t (ms)
×1010

FFT of ρc (t)

1.00
0.75

F
H1
H2
H3

0.50
0.25
0.00
1000

2000

3000

4000
5000
f (Hz)

6000

7000

8000

Figure 4: The evolution of a stable spherical symmetric neutron star (TOV star) with
the resolution nr × nθ = 640 × 1. Upper panel : The relative variation of the central
density in time. Lower panel : The Fourier transform of the central density. The
vertical lines represent the frequencies of the oscillation modes calculated in the Cowling
approximation.

6. Code tests 2: Metric solver
After demonstrating that Gmunu can solve the relativistic hydrodynamics equations
correctly, we then test the capacity of our metric solver. Here we will mainly focus
on hydrodynamic evolution with dynamical spacetime.

16

Gmunu: Multigrid methods for solving Einstein field equations
6.1. Stability of a stable TOV star

The first test we perform is the stability of a stable spherically symmetric neutron star
BU0. Even though BU0 is a 1D model, we run this test with a 2-dimensional setup.
The resolution of the simulation is nr × nθ = 640 × 64, where r = [0, 30] and θ = [0, π/2].
While BU0 is a static and stable configuration, the discretization errors and the
diffusion at the contact discontinuity of the neutron star surface trigger stellar oscillation
modes. The upper panel of figure 5 shows the relative variation of the central density
ρc as a function of time. The relative variation of the density is of the order 10−4 . The
code is able to evolve BU0 stably for more than 10 ms as expected since BU0 is a stable
configuration.

[ρc (t)/ρc (0) − 1] × 104

5.0
2.5
0.0
−2.5
−5.0
−7.5

FFT of v r (t) and v θ (t)

−10.0

0

2

4

6
t (ms)

8

10

12

FFT(v r )
0.06

FFT(v θ )
F
H1
H2
H3

0.04
0.02
0.00
1000

2000

3000

4000
5000
f (Hz)

6000

7000

8000

Figure 5: A 2-D evolution of a stable spherically symmetric neutron star (TOV star)
with the resolution nr × nθ = 640 × 64. Upper panel : The relative variations of the
centeral density in time. The variations are about the order of O(10−4 ). Lower panel :
The Fourier transform of the radial velocity v r (t) and non-radial velocity v θ (t) at r = 5,
θ = π/4 (inside the neutron star). The vertical lines represent the known eigenmodes
frequency. Our results agree with the known eigenmodes.
One way to test if the code handles a dynamical spacetime correctly, at least in the
linear regime for small perturbations, is to extract the eigenmode frequencies from the
simulations and compare them with the known values from perturbative calculations. In
order to compare the eigenmodes more clearly, instead of applying the Fourier transform
on the central density directly, we analyse the radial component of the velocity v r and
the θ-component v θ at r = 5, θ = π/4 (inside the neutron star). The lower panel of

Gmunu: Multigrid methods for solving Einstein field equations

17

figure 5 shows the Fourier transform of v r and v θ . The vertical dashed lines represent
the known and well-tested eigenmode frequencies. Our results agree with the known
eigenmode frequencies [24, 20, 12]. Note that the eigenmode frequencies of an oscillating
neutron star in a dynamical spacetime are significantly different from those obtained by
Cowling approximation where the metric is kept fixed in time [20], as shown in table 3.

Table 3: The eigenmode frequencies of an oscillating neutron star extracted from our
simulations. The results of the dynamical spacetime case are significantly different from
the static spacetime case.
Dynamical spacetime
Yes
No

F (kHz) H1 (kHz) H2 (kHz) H3 (kHz)
1.417
3.919
5.920
7.753
2.701
4.547
6.303
8.104

6.2. Stability of rotating neutron stars
The tests we perform in this subsection are the stability of stable rotating neutron stars.
The resolution of these simulation is again nr × nθ = 640 × 64, with r = [0, 30] and
θ = [0, π/2].
The upper panel of figure 6 shows the evolution of a rotating stable neutron star
BU2. This model is stably evolved for more than 20 ms, where the relative variation
of ρc is about the order of O(10−4 ). The Fourier transforms of v r and v θ are shown in
the lower panel of the figure 6. The extracted eigenmodes again agree with the known
results [20].
Comparing the density profiles and the rotational velocity profiles at later times
with the initial profiles serves as another indicator for code performance. Figure 7
shows the comparison between the initial density profiles and the rotational velocity
(solid lines) with the same quantities (dashed lines) at Tmax = 20 ms of BU2. It can be
seen that the density profiles along the equatorial and polar radii are maintained very
well during the evolution. However, the rotational profile is slightly suppressed at the
surface of the star. This is due to the fact that the Riemann solver HLLE we used in
these tests is known to be too diffusive to deal with the star surface or any discontinuous
surface [12].
The same test with the same numerical setup has been done for the model BU8.
Unlike the moderately rotating case BU2, model BU8 is a rapidly rotating neutron star
which is close to the mass shedding limit and therefore this test is more demanding.
Even for this demanding case with the diffusive Riemann solver HLLE, Gmunu is able
to maintain this model for more than 20 ms. The relative variation in ρc is about
O(10−3 ) as shown in the upper panel of figure 8. The oscillation modes extracted from

18

Gmunu: Multigrid methods for solving Einstein field equations
[ρc (t)/ρc (0) − 1] × 104

5.0
2.5
0.0
−2.5
−5.0
−7.5

−10.0

0.0

2.5

5.0

7.5

10.0
t (ms)

12.5

15.0

17.5

20.0

FFT of v r (t) and v θ (t)

0.08
FFT(v r )
FFT(v θ )
F
H1

0.06
0.04

2
2

0.02

f
p1

i2

0.00
0

1000

2000

3000
f (Hz)

4000

5000

6000

Figure 6: The evolution of a stable rotating neutron star (BU2) with the resolution
nr × nθ = 640 × 64. Upper panel : The relative variation of the centeral density in time.
The variation is about the order of O(10−4 ). Lower panel : The Fourier transform of
the central density. The vertical lines represent the known and well-tested eigenmode
frequencies [20]. Our results agree with the known eigenmodes.
Tmax = 20 ms
1.0

Tmax = 20 ms
1.0

equatorial initial
equatorial
pole initial
pole

0.6

hp

v φ vφ

i

0.8

0.4

v φ vφ /max

0.8

equatorial initial
equatorial

0.4

p

ρ/ρc

0.6

0.2

0.2

0.0

0.0
0

5

10
r (km)

15

20

0

5

10
r (km)

15

20

Figure 7: Comparison between the initial density profiles and the rotational velocity
(solid lines) and the some quantities (dashed lines) at Tmax = 20 ms of a stable rotating
neutron star BU2. The left panel shows a comparison between the initial normalized
density profiles along the polar and equatorial radii and the same quantities at Tmax .
The right panel compares the rotational velocity profiles at times t = 0 and t = Tmax .
the simulation also agree with the results reported by other groups [20], as shown in

19

Gmunu: Multigrid methods for solving Einstein field equations

[ρc (t)/ρc (0) − 1] × 103

the lower panel in figure 8. Moreover, as shown in the left panel in figure 9, the density
profiles are well-preserved even up to Tmax = 20 ms. However, unlike the previous cases,
the average value of the central density decreases slowly during the evolution, and the
angular velocity profile is slightly distorted at the surface of the star.
0

−2
−4
−6

FFT of v r (t) and v θ (t)

0.0

2.5

5.0

7.5

10.0
t (ms)

12.5

15.0

17.5

20.0

FFT(v r )

0.2

FFT(v θ )
F
H1

0.1

2

f

0.0
0

1000

2000

3000
f (Hz)

4000

5000

6000

Figure 8: The evolution of a stable rapidly rotating neutron star (BU8) with the
resolution nr × nθ = 640 × 64. Long term evolution of a rapidly rotating neutron
star in a dynamical spacetime is known as a challenging test. Even though the HLLE
solver might be too diffusive, Gmunu is still able to maintain this model for more than 20
ms with small variations and the fluid behaves correctly and the extracted eigenmodes
agree with the results from the other groups [20]. Upper panel : The relative variation
of the central density ρc is about O(10−3 ) and the average value ρc decreases slowly
during the evolution. Lower panel : The Fourier transform of the radial velocity v r (t)
and non-radial velocity v θ (t) at r = 5, θ = π/4 (inside the neutron star). The vertical
lines represent the known and well-tested eigenmode frequencies [20].

6.3. Migration of an unstable TOV star
Previous tests are all based on the evolution of stable neutron stars, where the
configurations are almost stationary with some perturbations. In this subsection, we
report the performance of the code in the fully non-linear regime with significant
changes and coupling in the metric and fluid variables. One of the standard tests
for hydrodynamical evolution coupled with dynamical spacetime in the fully non-linear
regime is the migration of an unstable neutron star [24, 6, 15, 12]. Following [15],

20

Gmunu: Multigrid methods for solving Einstein field equations
Tmax = 20 ms
1.0

Tmax = 20 ms
1.0

equatorial initial
equatorial
pole initial
pole

0.6

hp

v φ vφ

i

0.8

0.4

v φ vφ /max

0.8

equatorial initial
equatorial

0.4

p

ρ/ρc

0.6

0.2

0.2

0.0

0.0
0

5

10
r (km)

15

20

0

5

10
r (km)

15

20

Figure 9: Comparison between the initial density profiles and the normalized rotational
velocity (solid lines) and the some quantities (dashed lines) at Tmax = 20 ms of a stable
rotating neutron star BU8. The left panel shows a comparison between the initial
normalized density profiles along the polar and equatorial radii and the same quantities
at Tmax . The right panel compares the rotational velocity profiles at times t = 0 and
t = Tmax . Due to the fact that the HLLE solver is too diffusive to deal with the surface
of a rapidly rotating star, the angular velocity profile is slightly distorted at the star
surface.
we use model SU for this migration test, which lies on the unstable branch of the
mass-radius curve. In this test, we setup a 1D run with a simulation box r = [0, 30]
with 1024 grid points. As the star evolves and migrates to the corresponding stable
configuration ρc = 1.346 × 10−3 with the same mass, the radius of the star expands to a
large value. Unlike the previous cases, we adopt the ideal gas (gamma-law) equation of
state P = (Γ − 1)ρ with K = 100 and Γ = 2 for the fluid so that we can also capture
the shock heating effect.
Figure 10 shows the evolution of the central density ρc as a function of time. The
oscillations are damped due to the fact that shock waves are formed at every pulsation
and some kinetic energy is dissipated into thermal energy. Our results agree with the
results from previous works (see, e.g. [15]).
7. Performance of the metric solver
7.1. Convergence properties
In this section, we demonstrate the convergence properties and performance of our
multigrid metric solver. We solve the metric of model BU8 (see table 1), which represents
a rapidly rotating neutron star and far from spherically symmetric, with our metric
solver with the resolution nr × nθ = 640 × 64. The computational domain covers
r = [0, 30] and θ = [0, π/2]. To compare the convergence rate, we focus on solving the
lapse function α with the flat space initial guess α = 1.

21

Gmunu: Multigrid methods for solving Einstein field equations

1.0

ρc (t)/ρc (0)

0.8
0.6
0.4
0.2
0.0
0

2

4
t (ms)

6

8

Figure 10: Evolution of the central density for an unstable spherically symmetric neutron
star with the resolution nr ×nθ = 1024×1. The dashed line represents the central density
ρc of the neutron star on the stable branch.
Figure 11 shows the L1 norm of the residual of Eq. (15) as a function of the number
of iterations with different level of V-cycle. The number represents how deep the solver
goes when solving for the lapse function. The horizontal black dashed line represents
the threshold tolerance. As we can see in figure 11, the solver converges faster when it
goes to a deeper level. Also, it takes O(105 ) iterations (not shown in the plot) to reach
the threshold tolerance for the V1 (or Gauss-Seidel) case, while it takes only 37 steps
for the V6 case.
In practice, at the beginning of the simulation, we use the initial data provided by
XNS as initial guess. During the evolution, we use the previous solution as initial guess
for the next iteration. This makes the solver converge much faster as the solutions on
previous time step are usually good approximation to the solution.
7.2. Frequency of solving the metric
Since the metric variables only vary slightly within one hydrodynamics time step in most
situations, it is in general not necessary to solve the metric equations at every time step
in order to reduce the computational time. We in practice only solve the metric equations
for every few tens of time steps and use extrapolation to obtain the metric quantities in
between. Here we shall study the accuracy and speed of solving the metric with different
frequencies. We introduce the metric resolution parameter ∆n, which represents the

22

Gmunu: Multigrid methods for solving Einstein field equations

102

L1 norm

100

10−2

10−4
V1
V2
V3
V4
V5
V6

10−6

10−8
0

10

20

30
40
Number of iterations

50

60

Figure 11: L1 norm of residual of Eq. (15) of an highly non-spherically symmetric
model BU8 as a function of the number of iterations with different level of V-cycle.
The convergence rate increases with the level of the V-cycle. Even if the multigrid
solver starts from the flat space initial guess, it takes only about 40 iterations for V6 to
converge to the prescribed tolerance (horizational black dashed line).
number of time steps between solving the metric [17]. To see how ∆n affects the
accuracy and the performance of our code, we performed simulations with the same
setting table 4 but with different metric resolution parameter, i.e. ∆n = 5, 10, 30, 50.
Table 4: The simulation setting we used for metric resolution parameter analysis.
Model
Riemann solver
reconstruction scheme
nr × nθ
range of r
range of θ
Tmax [ms]

BU8
HLLE
MC
640 × 64
[0, 30]
[0, π/2]
20

Figure 12 shows the Fourier transform of the radial velocity v r (t) at r = 5, θ = π/4
(inside the neutron star) of different metric resolution parameter ∆n. The vertical
dashed lines represent the known eigenmode frequencies. As shown in figure 12, the

23

Gmunu: Multigrid methods for solving Einstein field equations

eigenmode frequencies are almost the same for all ∆n. This result demonstrates that it
is not necessary to set a small ∆n for mildly dynamical spacetimes such as oscillating
rotating neutron stars. We leave the study of more generic dynamical spacetimes for
future investigation. Since the computational cost of extrapolation is much smaller than
the metric solver (see below), it is employed in our code to obtain the metric quantities
for times within each ”step” ∆n. Here we note that 4-points Lagrange interpolation is
used for metric extrapolation in Gmunu.

∆n = 50 + extrapolation
∆n = 50
∆n = 30
∆n = 10
∆n = 5
F
2
f

0.20

0.15

0.10

0.05

0.00
0

500

1000

1500

2000
f (Hz)

2500

3000

3500

4000

Figure 12: The Fourier transform of the radial velocity v r (t) at r = 5, θ = π/4
(inside the neutron star BU8) of different ∆n. For more detailed simulation setting,
see table 4. The vertical dashed lines represent the known eigenmode frequencies. All
the extracted eigenmodes frequencies agree with the known results even for ∆n = 50
without metric extrapolation case. However, although the results have no significant
differences between these settings, the computational cost is significantly high if the
metric resolution parameter ∆n is too small (see Table 5).
The computational cost of our metric solver is comparable to the hydrodynamics
solver. To demonstrate this, we again perform the same simulations but the maximum
time step n is limited to 104 , with code profiler. Table 5 shows the percentages of time
spent on different routines on each hydrodynamic step. As expected, the results show
that with smaller ∆n, the time spent on the multigrid (MG) metric solver is longer. For
the case ∆n = 50 and extrapolating the metric in between, the computational cost of
our metric solver is roughly 1.22 times larger than the hydrodynamics solver. It can also
be seen from the table that the computational time is dominated by the metric solver

Gmunu: Multigrid methods for solving Einstein field equations

24

if ∆n ∼ O(1).
Table 5: The percentages of time spent on different routines on each hydrodynamic step.
These are the simulations of BU8 with HLLE and MC limiter where the maximum time
step n is limited to 104 . The “hydro step” here includes only the hydrodynamics solver
and the multigrid (MG) metric solver, other routines such as data output is not included
in this step. Note that we ignored the routines of which the contribution is less than
1%.
∆n
50
30
10
5
Riemann solver 11.21 8.77 4.11
2.61
reconstruction
19.69 15.4 7.74
4.59
rhydro [%]
source terms
8.40 6.57 3.30
1.96
con2prim
4.30 3.35 1.65 ≤ 1.00
MG solver
48.87 60.08 80.11 88.40
rmetric [%]
extrapolation
6.02 4.66 2.19
1.15
rmetric /(1 − rmetric )
1.22 1.84 4.65
8.57
Note that these tests were performed with the most basic (also the fastest) available
setting of hydrodynamics solver (HLLE and MC limiter) on a rapidly rotating neutron
star BU8. While in practical use, we often use more accurate hydrodynamics solver
and reconstruction scheme such as WENO5 or MP5 which make the corresponding
computational cost for the hydrodynamics higher. Moreover, unlike the rapidly rotating
model BU8, the spacetimes of most of the isolated neutron stars deviate not too much
from spherical symmetry. In these cases, the multigrid solver usually converges faster
than the highly-asymmetric cases. In other words, for modelling isolated neutron stars,
we expect that the computational cost of our metric solver is almost the same as
(sometimes even lower than) the hydrodynamics solver.
8. Conclusion
We present the methodology and implementation of Gmunu, a new general-relativistic
hydrodynamics code which makes use of cell-centered nonlinear multigrid methods
to solve the elliptic-type metric equations in the extended conformally flat condition
(xCFC) approximation to general relativity. The set of hydrodynamics equations are
solved with standard high-resolution shock-capturing schemes. Four different Riemann
solvers have been implemented in the code: TVDLF [53], HLL [30], HLLE [23, 29], and
Marquina flux formula [21]. For the cell-interface reconstruction, various options are
also available: PC, MC, WENO5, and MP5.
We have tested Gmunu with some benchmarking tests for relativistic hydrodynamics
codes such as the relativistic shocktube problem, the evolution of rapidly rotating

Gmunu: Multigrid methods for solving Einstein field equations

25

neutron stars, and the migration from an unstable TOV star to a corresponding stable
solution with the same mass.
The main novelties of Gmunu are the following:
• Although the system is highly nonlinear and fully coupled, our multigrid solver is
robust and converges rapidly. In practical use (e.g. solving the metric in every 50
steps, and extrapolating in between), the computational time needed for solving
the (elliptic-type) metric equations is comparable to the hydrodynamics step.
• In contrast to the code presented in [19] where the hydrodynamic and metric
variables are defined in two different grids, our multigrid metric solver uses the same
grid as the hydrodynamics sector. This avoids the need to perform interpolations
for the variables defined in two different grids.
• Even using spherical polar coordinates, besides standard boundary conditions, our
code does not require special treatment or regularization near the origin and pole
axis.
We have demonstrated that multigrid method is an efficient strategy to solve
nonlinear elliptic metric equations in hydrodynamical simulations. It seems to be
promising that the method would make fully-constrained evolution scheme in numerical
relativity become more affordable computationally.
In the future, we shall extend Gmunu to a fully-constrained scheme in exact general
relativity such as the formulation of Bonazzola et al. [8]. While numerical-relativity
codes based on a free-evolution approach are standard choices for modelling dynamical
spacetimes, it is still challenging for these codes to preform stable and accurate long-term
evolutions of compact objects. It would be interesting to see whether a fully-constrained
evolution code could improve the situation without requiring much more computational
resources in the future.
Not only this work can be further investigated on the numerical relativity side,
Gmunu can also be entended for realistic astrophysical applications such as core-collapse
supernova simulations. Future work includes code parallelisation, the development of
full 3D metric solver and microphysics implementation.
9. Acknowledgements
PCKC thanks Elias Most for the useful discussion about the details of conserved to
primitive variables, and Ninoy Rahman for the detailed discussion about the special
treatment at the centre of the simulation box. This work was partially supported
by grants from the Research Grants Council of the Hong Kong (Project No. CUHK
14310816 and CUHK 24304317), the Croucher Innovation Award from the Croucher
Fundation Hong Kong and by the Direct Grant for Research from the Research
Committee of the Chinese University of Hong Kong.

26

Gmunu: Multigrid methods for solving Einstein field equations
Appendix A. Implementation of the metric equations

By following Ref. [15, 12], Eqs. (13)-(16) can be solved in the given order. In the flat
spacetime, the Laplacian of a scalar function u(r, θ) is


1 ∂ 2u
∂ 2 u 2 ∂u
∂u
+
.
(A.1)
∆u = 2 +
+ cot θ
∂r
r ∂r r2 ∂θ2
∂θ
In our implementation for the vector equations, we solve for the orthonormal-basis
components for vector fields instead of coordinate-basis components. We rewrite a
generic vector as
X r̂ := X r ,

(A.2)

X θ̂ := rX θ ,

(A.3)

X φ̂ := r sin θX φ .

(A.4)

The conformal vector Laplacian (the left hand side of Eqs. (13) and (16)) are
!

∂X θ̂
1 ∂
2
r̂
θ̂
r̂
r̂
+ cot θX +
∇j X j ,
(∆X) = ∆X − 2 X +
r
∂θ
3 ∂r

2 ∂X r̂
1 ∂
j
+
∇
X
,
j
r2 ∂θ
3r ∂θ
X φ̂
,
(∆X)φ̂ = ∆X φ̂ −
r sin θ
(∆X)θ̂ = ∆X θ̂ +

(A.5)
(A.6)
(A.7)

where the divergence of the vector X is
∂X r̂ 1
+
∇j X j =
∂r
r

∂X θ̂
2X r̂ +
+ cot θX θ̂
∂θ

!

.

(A.8)

Note that from the numerical point of view, Eqs. (13) and (16) are the same
equations with different source terms. On the other hand, it is better to solve the
scalar equations, Eqs. (14) and (15), for the deviation of the functions from their
asymptotic-flatness limits ψ → 1 and α → 1 due to the non-linearity of the equations.
For instance, instead of solving for the conformal factor ψ directly, we solve for its
deviation δψ := ψ − 1.
Appendix A.1. Boundary conditions at the origin and the axis
We first discuss the inner boundary (r → 0) and also the boundary conditions at the
axis (θ = 0 or θ = π/2). For the scalar variables, as they have to be continuous across
all boundaries, we impose the symmetric boundary condition for all boundaries except
at the outer boundary (r = rmax ). However, the boundary conditions for vectors are
non-trival. Here we followed the approach in Ref. [17], which is summerized in table A1.

Gmunu: Multigrid methods for solving Einstein field equations

27

Table A1: Boundary conditions for the vector components at centre and axis. The plus
sign “+” means symmetric boundary condition whereas the minus sign “−” represent
anti-symmetric boundary condition.
βr
centre
−
pole
+
equator +

βθ
+
−
−

βφ
+
+
+

Appendix A.2. Discretization
In Gmunu, the metric solver are formulated in second-order accuracy. In particular, the
finite differences of the derivatives in Gmunu are the following:
∂u
ui+1,j − ui−1,j
,
=
∂r i,j
2∆r
∂u
ui,j+1 − ui,j−1
=
,
∂θ i,j
2∆θ
∂ 2u
ui+1,j − 2ui,j + ui−1,j
,
=
2
∂r i,j
∆r2
∂ 2u
ui,j+1 − 2ui,j + ui,j−1
=
,
2
∂θ i,j
∆θ2
ui+1,j+1 − ui+1,j−1 − ui−1,j+1 + ui−1,j−1
∂ 2u
=
.
∂θ∂r i,j
4∆θ∆r

(A.9)
(A.10)
(A.11)
(A.12)
(A.13)

References
[1] M. Alcubierre. Introduction to 3+1 Numerical Relativity. Oxford University Press, 2008.
[2] T. W. Baumgarte and S. L. Shapiro. Numerical integration of Einstein’s field equations. Phys.
Rev. D, 59(2):024007, Jan 1999.
[3] A. Bauswein, S. Goriely, and H. T. Janka. Systematics of Dynamical Mass Ejection,
Nucleosynthesis, and Radioactively Powered Electromagnetic Signals from Neutron-star
Mergers. Astrophys. J., 773(1):78, Aug 2013.
[4] A. Bauswein, H. T. Janka, K. Hebeler, and A. Schwenk. Equation-of-state dependence of the
gravitational-wave signal from the ring-down phase of neutron-star mergers. Phys. Rev. D,
86(6):063001, Sep 2012.
[5] A. Bauswein, N. Stergioulas, and H. T. Janka. Revealing the high-density equation of state through
binary neutron star mergers. Phys. Rev. D, 90(2):023002, Jul 2014.
[6] S. Bernuzzi and D. Hilditch. Constraint violation in free evolution schemes: Comparing the
BSSNOK formulation with a conformal decomposition of the Z4 formulation. Phys. Rev. D,
81(8):084003, Apr 2010.
[7] C. Bona, T. Ledvinka, C. Palenzuela, and M. Žáček. General-covariant evolution formalism for
numerical relativity. Phys. Rev. D, 67(10):104005, May 2003.

Gmunu: Multigrid methods for solving Einstein field equations

28

[8] S. Bonazzola, E. Gourgoulhon, P. Grand clément, and J. Novak. Constrained scheme for
the Einstein equations based on the Dirac gauge and spherical coordinates. Phys. Rev. D,
70(10):104007, Nov 2004.
[9] K. Brabazon, M. Hubbard, and P. Jimack. Nonlinear multigrid methods for second order
differential operators with nonlinear diffusion coefficient. Computers & Mathematics with
Applications, 68(12, Part A):1619 – 1634, 2014.
[10] A. Brandt. Multi-level adaptive solutions to boundary-value problems. Math. Comp., 31(138):333–
390, 1977.
[11] W. L. Briggs, S. F. McCormick, et al. A multigrid tutorial, volume 72. Siam, 2000.
[12] Bucciantini, N. and Del Zanna, L. General relativistic magnetohydrodynamics in axisymmetric
dynamical spacetimes: the x-echo code. A&A, 528:A101, 2011.
[13] G. Camelio, T. Dietrich, M. Marques, and S. Rosswog. Rotating neutron stars with non-barotropic
thermal profile. arXiv e-prints, page arXiv:1908.11258, Aug 2019.
[14] G. Camelio, T. Dietrich, and S. Rosswog. Disc formation in the collapse of supramassive neutron
stars. Mon. Not. Roy. Astron. Soc., 480(4):5272–5285, Nov 2018.
[15] I. Cordero-Carrión, P. Cerdá-Durán, H. Dimmelmeier, J. L. Jaramillo, J. Novak, and
E. Gourgoulhon. Improved constrained scheme for the Einstein equations: An approach to
the uniqueness issue. Phys. Rev. D, 79(2):024017, Jan 2009.
[16] I. Cordero-Carrión, P. Cerdá-Durán, and J. M. Ibáñez. Gravitational waves in dynamical
spacetimes with matter content in the fully constrained formulation. Phys. Rev. D, 85(4):044023,
Feb 2012.
[17] H. Dimmelmeier, J. A. Font, and E. Müller. Relativistic simulations of rotational core collapse I.
Methods, initial models, and code tests. Astron. Astrophys., 388:917–935, Jun 2002.
[18] H. Dimmelmeier, J. A. Font, and E. Müller. Relativistic simulations of rotational core collapse II.
Collapse dynamics and gravitational radiation. Astron. Astrophys., 393:523–542, Oct 2002.
[19] H. Dimmelmeier, J. Novak, J. A. Font, J. M. Ibáñez, and E. Müller. Combining spectral and shockcapturing methods: A new numerical approach for 3d relativistic core collapse simulations. Phys.
Rev. D, 71:064023, Mar 2005.
[20] H. Dimmelmeier, N. Stergioulas, and J. A. Font. Non-linear axisymmetric pulsations of rotating
relativistic stars in the conformal flatness approximation. Mon. Not. Roy. Astron. Soc.,
368(4):1609–1630, Jun 2006.
[21] R. Donat and A. Marquina. Capturing Shock Reflections: An Improved Flux Formula. Journal
of Computational Physics, 125(1):42–58, Apr 1996.
[22] W. E. East, F. M. Ramazanoǧlu, and F. Pretorius. Conformal thin-sandwich solver for generic
initial data. Phys. Rev. D, 86(10):104053, Nov 2012.
[23] B. Einfeldt. On godunov-type methods for gas dynamics. SIAM Journal on Numerical Analysis,
25(2):294–318, 1988.
[24] J. A. Font, T. Goodale, S. Iyer, M. Miller, L. Rezzolla, E. Seidel, N. Stergioulas, W.-M. Suen,
and M. Tobias. Three-dimensional numerical general relativistic hydrodynamics. II. Long-term
dynamics of single relativistic stars. Phys. Rev. D, 65(8):084024, Apr 2002.
[25] J. A. Font, M. Miller, W.-M. Suen, and M. Tobias. Three-dimensional numerical general relativistic
hydrodynamics: Formulations, methods, and code tests. Phys. Rev. D, 61(4):044011, Feb 2000.
[26] F. Galeazzi, W. Kastaun, L. Rezzolla, and J. A. Font. Implementation of a simplified approach
to radiative transfer in general relativity. Phys. Rev. D, 88(6):064009, Sep 2013.
[27] E. Gourgoulhon. 3+1 Formalism and Bases of Numerical Relativity. arXiv e-prints, pages gr–
qc/0703035, Mar 2007.
[28] W. Hackbusch. Multi-Grid Methods and Applications, volume 4. 01 1985.
[29] A. Harten, P. Lax, and B. Leer. On upstream differencing and godunov-type schemes for hyperbolic
conservation laws. SIAM Review, 25(1):35–61, 1983.
[30] A. Harten, P. D. Lax, and B. van Leer. On Upstream Differencing and Godunov-Type Schemes
for Hyperbolic Conservation Laws, pages 53–79. Springer Berlin Heidelberg, Berlin, Heidelberg,

Gmunu: Multigrid methods for solving Einstein field equations

29

1997.
[31] S. H. Hawley, M. J. Vitalo, and R. A. Matzner. Spin Dependence in Computational Black Hole
Data. arXiv e-prints, pages gr–qc/0604100, Apr 2006.
[32] J. A. Isenberg. Waveless Approximation Theories of Gravity. International Journal of Modern
Physics D, 17(2):265–273, Jan 2008.
[33] J. M. Mart, J. M. Ibáez, and J. A. Miralles. Numerical relativistic hydrodynamics: Local
characteristic approach. Phys. Rev. D, 43(12):3794–3801, Jun 1991.
[34] J. M. Martı́ and E. Müller. Numerical hydrodynamics in special relativity. Living Reviews in
Relativity, 6(1):7, Dec 2003.
[35] M. Mohr and R. Wienands. Cell-centred multigrid revisited. Computing and Visualization in
Science, 7(3):129–140, Oct 2004.
[36] N. Moldenhauer, C. M. Markakis, N. K. Johnson-McDaniel, W. Tichy, and B. Brügmann. Initial
data for binary neutron stars with adjustable eccentricity. Phys. Rev. D, 90(8):084043, Oct
2014.
[37] P. J. Montero, T. W. Baumgarte, and E. Müller. General relativistic hydrodynamics in curvilinear
coordinates. Phys. Rev. D, 89(8):084043, Apr 2014.
[38] B. Müller. The dynamics of neutrino-driven supernova explosions after shock revival in 2D and
3D. Mon. Not. Roy. Astron. Soc., 453(1):287–310, Oct 2015.
[39] B. Müller, T. M. Tauris, A. Heger, P. Banerjee, Y.-Z. Qian, J. Powell, C. Chan, D. W. Gay, and
N. Langer. Three-dimensional simulations of neutrino-driven core-collapse supernovae from lowmass single and binary star progenitors. Mon. Not. Roy. Astron. Soc., 484(3):3307–3324, Apr
2019.
[40] R. Oechslin, S. Rosswog, and F.-K. Thielemann.
Conformally flat smoothed particle
hydrodynamics application to neutron star mergers. Phys. Rev. D, 65(10):103005, May 2002.
[41] C. D. Ott, H. Dimmelmeier, A. Marek, H. T. Janka, B. Zink, I. Hawke, and E. Schnetter. Rotating
collapse of stellar iron cores in general relativity. Classical and Quantum Gravity, 24(12):S139–
S154, Jun 2007.
[42] A. G. Pili, N. Bucciantini, and L. Del Zanna. Axisymmetric equilibrium models for magnetized
neutron stars in General Relativity under the Conformally Flat Condition. Mon. Not. Roy.
Astron. Soc., 439(4):3541–3563, Apr 2014.
[43] A. G. Pili, N. Bucciantini, and L. Del Zanna. General relativistic neutron stars with twisted
magnetosphere. Mon. Not. Roy. Astron. Soc., 447:2821–2835, Mar. 2015.
[44] A. G. Pili, N. Bucciantini, and L. Del Zanna. General relativistic models for rotating magnetized
neutron stars in conformally flat space-time. Mon. Not. Roy. Astron. Soc., 470(2):2469–2493,
Sep 2017.
[45] W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery. Numerical Recipes in
FORTRAN (2Nd Ed.): The Art of Scientific Computing. Cambridge University Press, New
York, NY, USA, 1992.
[46] W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery. Numerical recipes in Fortran
90, volume 2. Cambridge university press Cambridge, 1996.
[47] L. Rezzolla and O. Zanotti. Relativistic Hydrodynamics. 2013.
[48] M. Saijo. The Collapse of Differentially Rotating Supermassive Stars: Conformally Flat
Simulations. Astrophys. J., 615:866–879, Nov. 2004.
[49] M. Shibata and T. Nakamura. Evolution of three-dimensional gravitational waves: Harmonic
slicing case. Phys. Rev. D, 52(10):5428–5444, Nov 1995.
[50] C.-W. Shu. High Order Weighted Essentially Nonoscillatory Schemes for Convection Dominated
Problems. SIAM Review, 51(1):82–126, Jan 2009.
[51] N. Stergioulas, T. A. Apostolatos, and J. A. Font. Non-linear pulsations in differentially rotating
neutron stars: mass-shedding-induced damping and splitting of the fundamental mode. Mon.
Not. Roy. Astron. Soc., 352(4):1089–1101, Aug 2004.
[52] A. Suresh and H. T. Huynh. Accurate Monotonicity-Preserving Schemes with Runge Kutta Time

Gmunu: Multigrid methods for solving Einstein field equations

30

Stepping. Journal of Computational Physics, 136(1):83–99, Sep 1997.
[53] G. Tóth. A General Code for Modeling MHD Flows on Parallel Computers: Versatile Advection
Code. Astrophysical Letters and Communications, 34:245, Jan 1996.
[54] U. Trottenberg, C. Ulrich Trottenberg, C. Oosterlee, A. Schuller, A. Brandt, P. Oswald, and
K. Stüben. Multigrid. Elsevier Science, 2001.
[55] J. R. Wilson and G. J. Mathews. Relativistic Numerical Hydrodynamics. Cambridge Monographs
on Mathematical Physics. Cambridge University Press, 2003.
[56] S. Yoshida, L. Rezzolla, S. Karino, and Y. Eriguchi. Frequencies of f-Modes in Differentially
Rotating Relativistic Stars and Secular Stability Limits. Astrophys. J. Lett., 568(1):L41–L44,
Mar 2002.
[57] S. Yoshida, S. Yoshida, and Y. Eriguchi. R-mode oscillations of rapidly rotating barotropic stars in
general relativity: analysis by the relativistic Cowling approximation. Mon. Not. Roy. Astron.
Soc., 356(1):217–224, Jan 2005.


# A Dynamically Adaptive Multilevel Wavelet Collocation Method for Solving Partial Differential Equations in a Finite Domain

**Authors:** Oleg V. Vasilyev and Samuel Paolucci
**Affiliation:** Department of Aerospace and Mechanical Engineering, University of Notre Dame
**Journal:** Journal of Computational Physics 125, 498–512 (1996)
**DOI:** 10.1006/JCPH.1996.0111

_Extraction tool: pdftotext (poppler); marker/nougat unavailable on host. Layout normalized manually where obvious._

JOURNAL OF COMPUTATIONAL PHYSICS 125, 498–512 (1996)
ARTICLE NO. 0111

A Dynamically Adaptive Multilevel Wavelet Collocation Method for
Solving Partial Differential Equations in a Finite Domain
OLEG V. VASILYEV AND SAMUEL PAOLUCCI
Department of Aerospace and Mechanical Engineering, University of Notre Dame, Notre Dame, Indiana 46556
Received May 9, 1995

A dynamically adaptive multilevel wavelet collocation method
is developed for the solution of partial differential equations. The
multilevel structure of the algorithm provides a simple way to adapt
computational refinements to local demands of the solution. High
resolution computations are performed only in regions where sharp
transitions occur. The scheme handles general boundary conditions. The method is applied to the solution of the one-dimensional
Burgers equation with small viscosity, a moving shock problem,
and a nonlinear thermoacoustic wave problem. The results indicate
that the method is very accurate and efficient. Q 1996 Academic
Press, Inc.


## 1. Introduction


A multilevel wavelet collocation method for the solution
of partial differential equations has been developed recently by Vasilyev et al. [1]. The method utilizes the classical idea of collocation with the wavelet approximation.
The authors suggest two different approaches of treating
general boundary conditions: differential and integral. The
differential approach uses standard wavelets as a basis
and results in a differential–algebraic system of equations,
where the algebraic part arises from the boundary conditions. The integral approach utilizes extended wavelets,
which satisfy boundary conditions exactly. This approach
results in a system of coupled ordinary differential equations. The method is tested on the one-dimensional Burgers equation with small viscosity and the solutions were
compared with those resulting from the use of other methods. Their results indicate that the method is competitive
with well-established numerical algorithms.
The multilevel wavelet collocation method proposed in
[1] is based on the localization property of wavelets. Due
to the fact that the zero-mean restriction plays no role in
the algorithm, the method is applicable with any suitable
basis function which has compact or essentially compact
support in both physical and wavenumber spaces. Another
very important aspect of the algorithm is its spectral accuracy [1]. Unfortunately while spectral convergence of the
method is indicated by the numerical results, an analytical
proof is lacking at this time.
498
0021-9991/96 $18.00
Copyright  1996 by Academic Press, Inc.
All rights of reproduction in any form reserved.

Liandrat and Tchiamichian [2], Bacry et al. [3], Maday
and Ravel [4], and Bertoluzza et al. [5] have shown that
the multiresolution structure of wavelet bases is a simple
and effective framework for spatially adaptive algorithms.
In their Galerkin algorithms, they retain wavelets, whose
coefficients are larger than a given threshold. In order to
be able to track singularities they also retain wavelets that
are adjacent to such regions. This adaptive procedure,
based on the analysis of wavelet coefficients, allows them
to follow the local structures of the solution.
In wavelet Galerkin algorithms nonlinearities can be
handled using either the connection coefficients (see [3])
introduced by Beylkin [6, 7] or quadrature formulae (see
[4]). The first approach is computationally expensive, due
to the summations over multiple indices. The second one
loses its accuracy due the approximate calculations of the
scalar products (see [8]). In contrast, the treatment of nonlinear terms in the multilevel wavelet collocation method
(see [1]) is a straightforward task due to the collocation
nature of the algorithm.
Most of the wavelet algorithms for solving partial differential equations can handle periodic boundary conditions
easily. The effective treatment of general boundary conditions is still an open question even though different possibilities of dealing with this problem have been studied.
One approach is to use wavelets specified on an interval
as suggested by Meyer [9] and Andersson et al. [10]. These
wavelets are constructed satisfying certain boundary conditions. The disadvantages of this approach are inconvenience of implementation and wavelet dependence on
boundary conditions. A more satisfactory approach is to
make a change of variable in conjunction with the tau
method to treat Dirichlet boundary conditions [4]. This
approach may lead to some instabilities associated with
the introduction of extra equations to treat boundary conditions, which in turn makes the system of equation overdetermined.
The main objective of the present work is to extend the
collocation method developed in [1] and to incorporate
the dynamically adaptive multilevel algorithm suggested
by Liandrat and Tchamitchian [2]. The essential feature

499

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

of the multilevel wavelet collocation method is that the
unknown functions themselves are solved for at collocation
points, in comparison with the wavelet Galerkin algorithms
which solve for wavelet coefficients. Even though wavelet
coefficients do not explicitly enter into the final form of
the wavelet collocation method, an adaptive algorithm
analogous to the one proposed in [2] can be utilized.
The rest of the paper is organized as follows. In Section
2 we briefly review the wavelet interpolation technique
developed in [1] with modifications which allow the extension to an adaptive algorithm. The dynamically adaptive
method for solving partial differential equations is described in Section 3. Finally, in Section 4, the method is
applied to the solution of the Burgers equation with small
viscosity, the modified Burgers equation producing a moving shock solution, and a nonlinear thermoacoustic wave
problem.

## 2. Wavelet Interpolation


u J(x) 5

O O c c (x),
J

j50 k[Z j

j
k

j
k

J
m

j

(3)

J

where
C j,J
k,m 5

O (A ) D , 0 # j # J, k [ Z , m [ Z , (4)
j,j 21
k,p

p[Z

j,J
p,m

j

J

j

l,j
5
Ai,k

c kj (x il ),

D j,J
i,m 5

5

0 # l, j # J, i [ Z l, k [ Z j,

R j,J
i,m 2

(5)

OO OR A C ,
j21

j,J
i,p

J,l
p,k

l,J
k,m

l50 p[Z J k[Z l

1 # j # J, i [ Z j, m [ Z J,
j 5 0, i [ Z 0, m [ Z J.

J
R 0,
i,m ,

(6)

21
denotes the
In the above expressions the operator (A j, j )k,p
(k, p)-element of the inverse of the matrix A j,j and the
l,j
operator R i,m
is the restriction operator defined as

l,j
5
R i,m

H

j
1 for x il 5 x m
,

(7)

0 otherwise.

Since the restriction operator is known, than we have
0,J
an explicit form for D0,J
i,m and, consequently, for Ck,m . Then
j,J
j,J
using (4) and (6) the operators Di,m and C k,m are obtained recursively.
Next, the interpolation operator is defined as

(1)

u J(x) 5

O I (x)u ,
J
i

i

(8)

i[Z J

where hZ j : 22L1j21 2 Nl , ..., 2L1j21 1 Nrj and Nl , Nr are
the number of external wavelets on each side of the domain
V. Note that levels j 5 0 and j 5 J correspond respectively
to the coarsest and finest scales present in the approximation, and the largest scale present in the approximation is
determined by L.
For clarity of discussion we will call wavelets corresponding to the same j as wavelets at the j level of resolution,
and for notational convenience we use the superscript to
denote the level of resolution and the subscript to denote
the location in physical space (with the exception of aj).
We follow [1] in defining a set of collocation points
hx ij : i [ Z j j in such a way that for any j (0 # j # J 2 1)
the following relation between the collocation points at
different levels of resolution is satisfied
hx ij j , hx ij11j.

j,J
k,m

m[Z


### 2.1. Interpolation On A Regular Grid

Let us consider a function u(x) defined on a closed interval V ; [xl , xr]. If we take c kj (x) 5 aj21/2c ((x 2 b kj )/aj),
where c (x) is a wavelet and aj 5 22ja0 , b kj 5 (xr 1 xl)/2 1
aj b0 k, a0 5 22L(xr 2 xl)/b0 , and L [ Z, then it can be
shown (see [1]) that there exist b0, L, Nl , Nr such that u(x)
can be approximated as

O C u , 0 # j # J, k [ Z ,

c kj 5

(2)

Then the operator C j,s
k,m which maps the set of functional
values at the J level of resolution into the set of wavelet
coefficients at the j level can be constructed (see [1]):

where
Ii (x) 5

O O c (x)C , i [ Z .
J

j
k

j,J
k,i

J

(9)

j50 k[Z j

Since the collocation points are known, the interpolation
operator can be constructed. In addition, using (1), (4),
(5), (6), and (9) the mth derivative of the approximate
function can be written as
u J(m)(x) 5

O D (x)u ,
(m)
i

i[ Z

J
i

(10)

J

where
D i(m) (x) 5

O O c (x)C , i [ Z .
J

j(m)
k

j,J
k,i

J

(11)

j50 k[Z j

Note that Di(0)(x) 5 Ii (x).
All wavelets whose centers are located within the do-

500

VASILYEV AND PAOLUCCI

FIG. 1. Locations of collocation points and wavelets near xl for
Nl 5 2.

main, will be called internal wavelets; the other wavelets
will be called external wavelets. Since every wavelet is
characterized by its location b kj , then for internal wavelets
these locations seem to be the most natural choice for
collocation points, provided that wavelets are symmetric
and nonzero at b kj . Nonsymmetrical wavelets can also be
utilized, but in this case the choice for collocation points
is not clear. Collocation points for external wavelets are
located as described in [1]. Briefly, at any level of resolution
j the collocation points corresponding to the external wavelets are located in the intervals [xl , xl 1 b0 aj ] and [xr 2
b0 aj , xr] and are taken to correspond to the collocation
points of possible internal wavelets of smaller scales. The
placement strategy is illustrated in Fig. 1 with two external
wavelets (Nl 5 2).
We enumerate the collocation points in such a way that
for any j (0 # j # J ) and i, k [ Z J, x ij , x kj if and only if
i , k. Subsequently, it is easy to show that
x 2j 2L1j212Nl 5 xl , x 2j L1j211Nr 5 xr .

depends upon the local regularity of u(x) in the neighborhood of location b kj . As mentioned in [1], numerical results
indicate that for appropriately chosen Nl and Nr the
method converges uniformly with increasing J. This indicates a decay of the magnitude of wavelet coefficients as the
level of resolution increases. For the algorithm presented in
[1] we show a typical collocation grid using a seven-level
approximation. This grid, reproduced in Fig. 3b, is used
regardless of the approximation function, assuming it can
resolve all the scales present in the function. It seems that
for a function which has singularities or sharp transitions,
it is far from the optimal representation. In Fig. 3a we
illustrate a function defined on the interval [21, 1] which
has a sharp transition. For this function we present in Fig.
3c the grid of collocation points of the correlation function
of the Daubechies scaling function of order 5 with coefficients whose absolute value is larger than a threshold « 5
5 3 1023. We see a pyramid of collocation points that
marks the location of the sharp transition. The width and
height of the pyramid depend mostly on the magnitude of
the gradient of u(x), the size of the wavelet support, and
the type of wavelet. In our case, out of the 275 collocation
points (shown in Fig. 3b) only the 34 (shown in Fig. 3c)
correspond to the wavelet coefficients which are above the
threshold. This example indicates the tremendous saving
if we design the algorithm to automatically take into account the structure of the approximated function.
The approximation (1) can be rewritten as a sum of two
terms composed of wavelets whose amplitudes are above
and below the threshold «:

(12)

Up to this point we have indicated that c (x) is a wavelet;
however, we emphasize that the present method is applicable for any suitable function, provided it has compact or
essentially compact support. In order not to cloud the
discussion we will keep referring to our functions as wavelets, keeping in mind that true wavelets have additional
properties. In fact, we illustrate the method using the correlation function of the Daubechies scaling function of order
5 with b0 5 1.0 (see Beylkin and Saito [11]). We choose
the order 5 as a compromise between the requirement on
continuity of the second derivative (which we will need
later) and the demand to have the support as small as
possible. The correlation function of Daubechies scaling
function of order 5 and its Fourier transform C(j ) 5
1y
e2y c (x)e2ij x dx are shown in Fig. 2. Note that for symmetrical functions the imaginary part of the Fourier transform
is always zero.

### 2.2. Interpolation On An Irregular Grid

c kj

apThe absolute value of the wavelet coefficient
pearing in the approximation (1) and computed in (3)

u J(x) 5 u J$(x) 1 u J,(x),

(13)

where
u J$(x) 5

O O c c (x), u (x) 5 O O c c (x). (14)
J

j
k

j50 k[Z j

J

j
k

J
,

j50 k[Z j

uc jk u$«

j
k

j
k

uc jk u,«

Let us formulate and prove the following proposition.
PROPOSITION 1. For any « . 0 there exists a positive
constant C̃ such that iu J(x) 2 u J$ (x)iL2(V) 5 iu J,(x)iL2(V) #
«C̃.
Proof.

iu J,(x)iL2(V) 5

#

I

I

O O c c (x)
J

j50 k[Z

j
k

j
k

j

uc jk u,«

L2(V)

O O uc u ic (x)i
J

j50 k[Z j

uc jk u,«

j
k

j
k

L2(V) # «NWi

c (j )iL2(R) ,

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

501

FIG. 2. The correlation function of the Daubechies scaling function of order 5 (c (x)) and its Fourier transform (C(j )).

where NW is the total number of wavelets. The last inequality follows since uc kj u , « and ic kj (x)iL2(V) # ic (j )iL2(R).

uc kj u $ aj1/2«.

The estimate for the constant C̃ can be made much
less conservative at the expense of complicating the proof.
Consequently, Proposition 1 allows us to omit wavelets
whose coefficients are below a certain threshold, and if we
keep in approximation (1) only coefficients which are
above the threshold, then we will still retain a good approximation. Due to the collocation nature of the algorithm
we are interested in the Ly norm of the error and, since
the magnitude of wavelet c kj (x) is of the order aj21/2, we
only retain wavelets whose amplitude satisfy the criteria

Note that by omitting a wavelet whose amplitude is below
the threshold, the collocation point associated with this
wavelet should be omitted as well. We call the grid of
collocation points an irregular grid G$ if at least one collocation point at any level of resolution is omitted. Otherwise
we will call it a regular grid G. Examples of regular and
irregular grids of wavelet collocation points are presented
respectively in Figs. 3b and 3c. Note that the irregular grid
becomes a regular one by setting the threshold parameter
« to zero.

(15)

FIG. 3. (a) Function u(x), (b) regular grid (« 5 0), (c) irregular grid (« 5 5 3 1023, M 5 0, C 5 0), (d) irregular grid (« 5 5 3 1023, M 5 1,
C 5 1) of wavelet collocation points used in approximating the function.

502

VASILYEV AND PAOLUCCI

If we look closely at Fig. 3c we see that the relation (2)
between collocation points at different levels is violated.
However, the algorithm on the irregular grid can be formally interpreted as the algorithm on a regular one where
the coefficients which are below the threshold are set to
zero. Let us define two subsets of integers Z $j , Z j and
Z C , Z J such that x ij [ G$ if and only if i [ Z $j and
J
j
x Jk [ <j50 hx m
: m [ Z $j j if and only if k [ Z C. In other
j
words, Z $ is the set of indices of wavelets (and collocation
points) at the j level of resolution, and Z C is the set of
indices of the ultimate set of collocation points used in the
interpolation. Subsequently, Eqs. (3), (4), (6), (10), and
(11) can be rewritten as

O C u , 0 # j # J, k [ Z ,
C 5 O (A ) D ,
c kj 5

j, J
k,m

m[Z

j

J
m

$

(16)

C

j,J
k,m

j,j 21
k,p

j,J
p,m

p[Z j$

0 # j # J, k [ Z $j , m [ Z C, (17)

D j,J
i,m 5

5

R j,J
i,m 2

OO OR A C ,
j2 1

j,J
i,p

J,l
p,k

1 # j # J, i [ Z $j , m [ Z C,
j 5 0, i [ Z 0$, m [ Z C,

O D (x)u ,
(x)C , i [ Z .
D (x) 5 O O c
(m)
i

i[Z

(m)
i

J
i

(18)
(19)

C

J

j(m)
k

j,J
k,i

C

where F is a linear or nonlinear operator. We illustrate
the method by solving (21), together with the Dirichlet
boundary conditions,
u(xl , t) 5 ul (t), u(xr , t) 5 ur (t).

$

uJ(m)(x) 5

­u
5 F(t, x, u, ux , uxx) for t . 0, u(x, 0) 5 u0 (x), (21)
­t

l,J
k,m

l50 p[Z C k[Z l

J
R 0,
i,m ,

tive approach and the second is the integral approach.
Since the objective of this paper is to present an adaptive
algorithm, we will illustrate it using the derivative approach
only, keeping in mind that the same adaptive procedure
with slight modifications can be applied with the integral
approach as well. We also note that in general the integral
adaptive approach requires more degrees of freedom than
the derivative one. This is due to the fact that extended
wavelets, which are used in the integral approach, have
larger support than regular wavelets once they are close
to the boundary of the domain.
We will demonstrate the method through its application
to the solution of a second-order partial differential equation of the type

(20)

j50 k[Z j

$

Equations (16)–(20) can be formally obtained by substituting the sets of the subscripts Z $j and Z C, instead of Z j and
Z J, respectively. Note that in the process of this formal
substitution, Z J$ is substituted everywhere, where Z j appeared for j 5 J, and Z C, where Z J appears explicitly. Also
note that the size of the matrix Aj,j is determined by the
number of elements in the set Z $j .
Since the main objective of this work is to use an irregular grid in an adaptive algorithm for solving partial differential equations, we will not elaborate any further on the
influence of all the parameters associated with the algorithm on the interpolation characteristics. For this purpose
we refer the reader to [1] for the case where « 5 0.

## 3. The Dynamically Adaptive Algorithm


The treatment of general boundary conditions on a finite
domain is one of the difficulties for most wavelet algorithms. In [1] two different approaches of dealing with
boundary conditions are suggested. The first is the deriva-

(22)

The time integration algorithm can be chosen depending
on the applications. It can be either explicit or implicit.
For some applications it can be mixed. For example, in
many applications in fluid mechanics the Adams–
Bashforth scheme is used for nonlinear terms and the
Crank–Nicolson scheme is used for the linear terms. In
our work we do not concentrate on the time integration
scheme, since we want to focus on the adaptation in scale
and space, retaining the freedom to choose the integration
algorithm which is most appropriate for the particular application. In the present research we use a fifth-order Gear
implicit integration algorithm implemented in the IMSL
routine IVPAG [12].
We refer to the present method as dynamically adaptive
in the sense that the irregular grid of collocation points is
dynamically adapted in time and follows the local structures that appear in the solution. Let us describe the way
we adapt the computational grid in time. The most straightforward approach for dynamical adaptation of the irregular
grid is to retain only those collocation points for which the
magnitude of associated wavelet coefficients satisfy criteria
(15). Even though this approach works in interpolation
problems, it is not applicable in the solution of partial
differential equations for the following two reasons: the
first reason is that, due to the finite support of wavelet and
the recursive character of the algorithm, any change in a
wavelet coefficient affects adjacent wavelets at the same
and finer levels of resolution; the second reason is that, in
order for the algorithm to be able to track sharp transitions

503

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

in the solution, we have to retain wavelets whose amplitude
can possibly become significant during the next time interval. Both reasons suggest that we retain collocation points
associated with wavelets that are adjacent in location and
scale. Thus, at any instant of time the grid of wavelet
coefficients should include wavelets belonging to an adjacent zone. We say that the wavelet c sk belongs to the adjacent zone of wavelet c ij (i.e., for which criteria (15) is
satisfied), if the following relations are satisfied
us 2 j u # M, ux sk 2 x ij u # Caj ,

(23)

where C defines the width of the adjacent zone in physical
space and M determines the extent of which coarser and
finer scales are included into the adjacent zone. In Fig. 3d
the irregular wavelet collocation grid for the function
shown in Fig. 3a is obtained with C 5 1 and M 5 1. Note
that, as discussed earlier, the irregular wavelet collocation
grid shown in Fig. 3c corresponds to the case with C 5 0
and M 5 0.
The values of C and M affect the total number of collocation points present in the irregular grid at any instant of
time and the time interval during which the calculations
can be carried out without modifying the computational
grid and subsequently the matrix operators required in
the computations. Note that in order to have an efficient
algorithm we want to keep the number of collocation points
as small as possible while at the same time we want to be
able to resolve all sharp transitions present in the solution.
Furthermore, for efficiency reasons we would like to minimize changes in the collocation grid. If ts (x kj ) is the time
scale of development coarser aj21 or finer scale aj11 in the
neighborhood of x kj , and tc (x kj ) 5 Caj /v(x kj ), where
v(x kj ) is local convection speed, then the time interval
during which the computational grid can be kept unchanged is determined by t 5 minj,k (ts (x kj ), tc (x kj )). For
convenience we denote t1 5 minj,k (ts (x kj )) and t2 5
minj,k (tc (x kj )). In other words, in problems for which the
convection time scale t2 is much larger than the time scale
associated with development of sharp transitions t1 , the
value of C should be taken larger than in problems for
which sharp transitions develop on a time scale much
smaller than the one associated with convection. As far as
the value of M is concerned, we found that the choice of
M 5 1 is the best compromise between requirements to
minimize the number of collocation points and upgrade
the computational grid as rare as possible.
Let us denote by G $t the irregular grid of wavelet collocation points that are retained to approximate the solution
at time t. Following the classical collocation approach and
evaluating (19), (20) at collocation points hx Ji : i [ Z C j at
the finest level of resolution we obtain
u iJ(m)(t) 5

O D u (t),
(m)
i,k

k[Z C

J
k

(24)

(m)
D i,k
5

O O c (x )C ,
J

j(m)
p

j50 p[Z

J
i

j, J
p,k

(25)

j

$

where i [ Z C and C j,p,kJ is given by (17). From (12) it
follows that
x J22L1J212Nl 5 xl , x J2L1J211Nr 5 xr ,

(26)

and (21) reduces to a system of nonlinear ordinary differential equations,
d J
(1) J
(2) J
u k (t), D i,k
u k (t)),
u (t) 5 F(t, x Ji , u Ji (t), D i,k
dt i

(27)

u Ji (0) 5 u0 (x Ji ),
where i [ Z C and repeated indices imply summation over
Z C. The boundary conditions (22) become
u J22L1J212Nl(t) 5 ul (t), u J2L1J211Nr(t) 5 ur (t) .

(28)

After solving (27) with boundary conditions (28), the solution on the interval is approximated by
u J(x, t) 5

O I (x)u (t).
i

i[Z

J
i

(29)

C

Note that for Neumann or mixed boundary conditions,
(28) is replaced by an algebraic relation in terms of u Ji ,
i [ Z C. Thus one has to solve a differential–algebraic
system of equations, which can be rewritten as a system
of coupled ordinary differential equations by expressing
the values of the function at the end points in terms of its
values at the interior locations.
Let us summarize the numerical algorithm. Assuming
that a time integration scheme is chosen, the present numerical algorithm involves three steps:
1. Assume we have computed the approximate solution u Ji (t) at positions on the irregular grid G $t (from initial
conditions or from the previous time step). For a given
threshold « we adjust G t$1Dt based on the magnitude of
wavelet coefficients at time t which are obtained using (16).
2. If G $t and G t$1Dt are the same go to step 3; otherwise:
a. values of the solution u Ji (t) at collocation points
of G t$1Dt , which are not included in G $t , are computed using (29), and
b. recalculate operator C j,p,kJ and the derivative ma(m)
trix D i,k
using (17) and (25), respectively.
3. Integrate (27) to obtain new values u Ji (t 1 Dt) at
positions on the irregular grid G t$1Dt , and go back to step 1.

504

VASILYEV AND PAOLUCCI

The basic hypothesis behind this algorithm is that during
a time interval Dt, the domain of wavelets with significant
coefficients does not move in phase space beyond the border of the irregular grid. With such an algorithm the irregular grid of wavelet collocation points is dynamically
adapted in time and follows the local structures that appear
in the solution. The accuracy in the adaptive multilevel
wavelet algorithm depends upon the threshold parameter
«. In addition, other parameters such as L, J, b0 , Nl , Nr ,
and the choice of wavelet affect the performance of the
algorithm for fixed «. If all parameters are appropriately
chosen, so that all the scales present in the problem are
resolved, then the accuracy of the method is determined
solely by «. The accuracy of the algorithm is increased with
the decrease of « until it reaches a limit determined by J.
In this case in order to further increase the accuracy by
decreasing «, J should be increased first. In other words
for each J there exists «J such that, in order for the approximation error to be determined by «, the threshold parameter must satisfy the inequality « $ «J .
Note that the most computationally expensive part of
the proposed algorithm is recalculating matrices C j,p,kJ and
(m)
. If N C is the total number of collocation points and
D i,k
MW is the parameter which depends on the support (or
effective support) of the wavelet (MW effectively defines
j, j
the bandwidth of the matrices A i,k
, A J,i,kj , c j(m)
(x Ji )), then
k
the upper bound of the total number of operations involved
in calculating the matrix operators is given by C1 MW N C
(MW 1 C2 N C ) and the storage requirement based on the
matrix structures is C3 N C (MW 1 C4 N C ), where the coefficients Ci (i 5 1, ..., 4) are of order 1. In contrast with
the nonadaptive algorithm [1], where these matrices are
calculated only once, here whenever the irregular grid
G $t changes these matrices have to be recalculated. However, because of the substantial decrease in the number of
collocation points on each level of resolution in comparison
with the nonadaptive approach, the resulting algorithm
is considerably more efficient. In addition, the numerical
procedure can be organized very efficiently by appropriately modifying the previously known matrices whenever
additional wavelets or collocation points are added.

## 4. Results And Discussion


In order to test the ability of the numerical algorithm
to resolve rapid and localized variations in the solution,
we consider three different problems. The first problem
tests the ability to resolve a shock which is fixed in space
but whose gradient changes in time. The second problem
tests the ability to resolve a moving shock. The third problem illustrates the ability of the algorithm to be successfully
applied to more complicated problems.
The rest of the section is organized as follows. In the
first subsection we discuss the problem formulations and

in the second we present numerical results. In both subsections, because of the fact that the first two problems have
analytical solutions with which we can more rigorously
check the algorithm, we split the discussion into two parts.
In the first part we discuss the performance of the algorithm
and its competitiveness with other numerical methods
based on the results of the first two test problems. In the
second part we illustrate the application of the present
algorithm to the solution of third problem.

### 4.1. Problem Formulations

I. Burgers Equation. For the first test problem we consider the Burgers equation
­2 u
­u
­u
1 u 5 n 2 , x [ (21, 1), t . 0,
­t
­x
­x

(30)

with initial and boundary conditions
u(x, 0) 5 2sin(fx), u(61, t) 5 0

(31)

whose analytical solution is known (see [13]). Also note
that the boundary conditions at the two ends are of Dirichlet type and, since the wavelets that we utilize are symmetric, we use the same number of external wavelets on each
side of the domain, i.e., Nl 5 Nr 5 N. In light of (27) and
(28) the problem reduces to

O

d J
(1)
(2)
u i (t) 5
[2u Ji(t)D i,k
1 nD i,k
] u Jk (t),
dt
C
k[Z
u Ji(0) 5 2sin(fx Ji),

(32)

u J6(2L1J211N )(t) 5 0,
where i [ Z C, i ? 6(2L1J21 1 N ). The system (32) is solved
with the fixed integration step Dt 5 5 3 1024 /f.
II. Modified Burgers. Equation. As a second test problem we consider the modified Burgers equation,
­u
­u
­2u
1 (v 1 u) 5 n 2 , x [ (2y, 1y), t . 0, (33)
­t
­x
­x
where v is a constant. The initial and boundary conditions are
u(x, 0) 5 2tanh

S D

x 2 x0
, u(6y, t) 5 71.
2n

(34)

The analytical solution of this problem is a shock wave
moving with the uniform velocity v given by

505

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

u(x, t) 5 2tanh

S

D

x 2 x0 2 vt
.
2n

For numerical purposes, due to the exponential decay of
the solution at infinity, the problem can be considered in
a finite domain. Thus for n 5 1022, x0 5 20.25, v 5 1, and
0 # t # 0.5, it is legitimate to consider the problem in the
domain x [ [21, 1] with Dirichlet boundary conditions.
Analogous to the first test problem we take Nl 5 Nr 5 N.
In light of (27) and (28) the problem reduces to

O

d J
(1)
(2)
u i (t) 5
[2(v 1 u Ji(t))D i,k
1 nD i,k
] u Jk (t),
dt
C
k[Z
u Ji(0) 5 2tanh

S

D

where Pr is the Prandtl number, and c is the ratio of specific
heats, which is assumed to be temperature independent.
Nondimensional viscosity and thermal conductivity are approximated by
e(T ) 5 c1 Ï1 1 T 1 c2 , k(T ) 5 c3 Ï1 1 T 1 c4 . (41)
The boundary conditions are

and the initial conditions are

x Ji 2 x0
,
2n

(36)

r(x, 0) 5 V(x, 0) 5 T(x, 0) 5 0.

where i [ Z C, i ? 6(2L1J21 1 N ). The system (36) is solved
with the fixed integration step Dt 5 5 3 1024.
III. Nonlinear Thermoacoustic Waves Problem. As a
third problem we consider a nonlinear thermoacoustic
(TAC) wave problem. Below we just give the mathematical
formulation of the problem. For details regarding the physical aspects of the problem we refer to [14]. Let us briefly
describe the origin of the equations. Consider a compressible ideal gas between two rigid walls. The gas is initially
quiescent at a uniform pressure and temperature. As a
result of a temperature change at the left boundary, deviations from quiescent values will occur. We denote the nondimensional velocity, density, pressure, and temperature
deviations by V, r, P, and T, respectively. The nondimensional continuity, momentum, energy, and state equations
for the one-dimensional nonlinear TAC wave are given by

F

G

1

2

,

J
i

­(rV ) J
,
­x i

2

1
­V
e(T )
c(1 1 r Ji ) ­x
­x

d J
­T
T 5 2V Ji
dt i
­x

J
i

(39)

(44)

­P J
1
J
c(1 1 r i ) ­x i

2 (c 2 1)

3
­T
k(T )
4Pr(1 1 r Ji ) ­x
­x

c21
e(T Ji )
1 1 r Ji

­V
­x

J

,

(45)

i

1 1 P Ji ­V J
1 1 r Ji ­x i
J
i

J 2

,

(46)

i

P Ji 5 r Ji 1 T Ji 1 r Ji T Ji,

(47)

T J2(2L1J211N )(t) 2 Tw(t)

rJi(0) 5 V Ji(0) 5 T Ji(0) 5 0,

3
­T
k(T )
4Pr(1 1 r) ­x
­x
c21
­V
e(T )
11r
­x

i

2

5 T J(2L1J211N )(t) 5 V J6(2L1J211N )(t) 5 0,

­T
1 1 P ­V
­T
1V
1 (c 2 1)
­t
­x
1 1 r ­x

F G
S D

J

d J
­V
V 5 2V Ji
dt i
­x

1

­V
1
e(T )
, (38)
1
c(1 1 r) ­x
­x

S D S D
S D
S D
S F GD
S D
S D
S F GD
FS D G

d J
­V
ri 5 2
dt
­x

(37)

­V
­V
1
­P
1V
52
­t
­x
c(1 1 r) ­x

(43)

The temperature at the left wall is taken to be Tw (t) 5
AH(t), where H(t) is the Heaviside function.
Analogous to the previous two problems we take Nl 5
Nr 5 N. In light of (27) and (28), the problem (37)–(43)
reduces to

1

­r ­V ­(rV )
1
1
5 0,
­t ­x
­x

1

(40)

T(0, t) 2 Tw (t) 5 T(L, t) 5 V(0, t) 5 V(L, t) 5 0 (42)

u J6(2L1J211N )(t) 5 71,

5

P 5 r 1 T 1 rT,

(35)

(48)
(49)

where i [ Z C for Eqs. (44), (47), (49) and i [ Z C, i ?
6(2L1J21 1 N ) for (45), (46), since the values for velocity
and temperature at the boundaries are determined by (48).
For clarity of presentation we denote

506

VASILYEV AND PAOLUCCI

SD O

­f J
5
D (1) f J .
­x i k[Z C i,k k

(50)

Note that there are two different forms of the discretization
of terms such as (­/­x)(e(T )(­V/­x)), the conservative
form

S F

­V
e(T )
­x
­x

GD O
J
i

5

k[Z

(1)
D i,k
e(T Jk)

C

O D V , (51)
(1)
k,l

l[Z

J
l

C

and the nonconservative form,

S F

­V
e(T )
­x
­x

GD

J
i

OD V
(52)
de
1
(T ) O D T O D V .
dT

5 e(T Ji )

(2)
i,k

k[Z

J
k

C

J
i

(1)
i,k

k[Z C

J
k

(1)
i,l

FIG. 4. Analytical solution of the Burgers equation at times t 5
2i/5f, i 5 O(1)5.

J
l

l[Z C

We find that both formulations lead to numerically indistinguishable results.
The problem is solved with c1 5 1.489, c2 5 20.489,
c3 5 1.66, c4 5 20.66, A 5 1, c 5 1.4, and Pr 5 Df, which
correspond to nitrogen gas at a reference temperature of
300 K. The system of Eqs. (44)–(49) is solved using an
adaptive time integration step Dt such that Dt # t, where
t is the maximum time interval during which the computational grid can remain unchanged.

### 4.2. Numerical Results

Problems I and II. Basdevant et al. [13] presented a
comparative study of spectral and finite difference methods
for the solution of (30) and (31) with n 5 1022 /f. For such
a small viscosity, the solution develops into a sawtooth
wave at the origin for t * 1/f. The gradient at the origin
reaches its maximum value u­u/­xux50umax 5 152.0051616 at
time tmax 5 1.60369/f. In the second test problem the region
of large gradients is moving with the constant velocity v.
The maximum value of the gradient is u­u/­xumax 5 1/(2n),
which for n 5 1022 becomes u­u/­xumax 5 50. It appears
from the study of Basdevant et al. [13] that the performance
of a numerical method can be judged from its ability to
resolve the large gradient regions that develop in the solutions, which are given in Fig. 4 for the first test problem
and by (35) for the second one.
The dynamical adaptation of the solution and irregular
grids G $t of wavelet collocation points is illustrated in Figs.
5 and 6 for first and second problems, respectively. In
both cases we use the dynamically adaptive multilevel
collocation method with the correlation function of the
Daubechies scaling function of order 5 with b0 5 1.0,
N 5 1 and threshold parameter « 5 1 3 1023. The evolution

of the solution of Burgers equation from the uniformly
smooth distribution to the shock structure results in the
growth of the wavelet coefficients corresponding to the
smaller scales, which in turn results in the refinement of
the grid. Figure 5 illustrates the progressive refinement of
the irregular grid with the decrease of the shock thickness.
In the second test problem we demonstrate that the algorithm dynamically adapts to the moving irregularities of
the solution. Figure 6 shows that the region of collocation
points associated with the small scales moves with the
shock, thus permitting continuous proper resolution of the
shock structure.
In Figs. 7a and b we show how the total number of
collocation points N C change with time for the first and
second test problems. In Fig. 7a we note that N C progressively increases with time until the gradient of the solution
reaches its maximum. Then due to the viscous diffusion
the value of the gradient decreases on a much slower time
scale, which in turn results in a slow decrease of N C. In
Fig. 7b we see that the total number of collocation points
oscillates around the average of N C 5 101. The reason for
these oscillations is the sensitivity of the total number of
collocation points on whether the shock is located at a
collocation point or between collocation points.
The numerical results indicate that the biggest errors
occur in the neighborhood of the shocks. Due to finite
viscosity, the shock has a finite width. One would expect
to resolve a shock properly if the scale associated with the
finest level of resolution is smaller than the width of the
shock. Since for our particular problem b0 aJ 5 212L2J, then
the shock can be resolved with sufficient accuracy with
L 1 J $ 9 in the first test problem and with L 1 J $ 7 in
the second one. For a more thorough discussion on this
issue we refer to [1]. Note that even though the shock is
resolved with L 5 1, J 5 8 and with L 5 1, J 5 7 in first

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

507

FIG. 5. Evolution of the solution (left column) and collocation points (right column) for the solution of the Burgers equation using the correlation
function of the Daubechies scaling function of order 5.

and second test problems, respectively, the error in the
neighborhood of the shock is determined by J in both cases
(« , «J in these cases). Addition of an extra level decreases
«J and changes the inequality to « . «J , which in turn
increases the accuracy of the solutions (see Tables I and
II, cases 2 and 3).
The performance of the adaptive algorithm is strongly
affected by the choice of wavelet. Although not given here,
numerical results indicate that the adaptive algorithm using
the correlation function of the Daubechies scaling function
requires considerably fewer collocation points than using

the Gaussian function or the Mexican hat wavelet. This
phenomenon is associated with the localization properties
of these bases. The Mexican hat wavelet has the worst
localization, so that the adaptive algorithm utilizing it requires considerably more collocation points and, consequently, wavelets.
We emphasize that the multilevel approach is essential
for an efficient adaptive algorithm. For fixed «, with the
decrease in number of levels of resolution the number of
wavelets increases (see Tables I and II, cases 4–6). The
algorithm becomes practically nonadaptive if only few lev-

508

VASILYEV AND PAOLUCCI

FIG. 6. Evolution of the solution (left column) and collocation points (right column) for the solution of the modified Burgers equation using
the correlation function of the Daubechies scaling of order 5.

els are utilized. This can be explained simply by the fact
that more wavelets are required to approximate the large
scales, which could be accomplished more effectively with
fewer wavelets of larger scale.
Note that with an increase of the threshold parameter
« the number of collocation points decreases dramatically
(see Tables I and II, cases 1, 2, 4). We point out that the
algorithm becomes nonadaptive; i.e., it utilizes a regular
grid, when « is set to zero (Tables I and II, Case 1).
Summarizing the results presented in Tables I and II
we see that the dynamically adaptive multilevel wavelet

collocation method (« . 0) requires considerably fewer
degrees of freedom than the nonadaptive method (« 5
0) without much loss in accuracy of the solution. This
considerable reduction is achieved due to the local grid
refinement which is done automatically based on the analysis of wavelet coefficients. With regard to the accuracy of
the solution in comparison with those obtained with other
numerical algorithms, we can say that for the same accuracy the adaptive multilevel wavelet collocation method
requires substantially fewer degrees of freedom than spectral, finite difference, and nonadaptive wavelet Galerkin

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

509

FIG. 7. Time evolution of the total number of collocation points N C for (a) the first test problem with M 5 1 and C 5 1, (b) the second test
problem with M 5 1 and C 5 2, (c) the third test problem with M 5 1 and C 5 2, using the correlation function of the Daubechies scaling function
of order 5 and « 5 1 3 1023.

schemes (see [1, 2]). In comparing the adapative wavelet
Galerkin method of Liandrat and Tchamitchian [2] with
the present algorithm, we observe that both require practically the same number of degrees of freedom to achieve
comparable accuracy. However, the present algorithm has
two clear advantages, in comparison with adaptive wavelet
Galerkin algorithms. The first advantage is the simplicity
in the treatment of general boundary conditions. The second is the handling of nonlinearities which requires only
O(N C ) operations, while the wavelet Galerkin algorithms
require O(n2) operations [4], where n is the total number

of wavelets. In addition, treatment of nonlinear terms in
partial differential equations leads to loss of accuracy due
to the approximate calculation of scalar products using
quadrature rules. For detailed discussion on the error associated with the use of quadrature formulas we refer to [8].
We also note that an adapative wavelet Galerkin method
cannot take advantage of the fast wavelet transform, unless
the solution is interpolated to the finest uniform grid, as
is originally done in [15]; but this procedure is even more
computationally expensive. The only disadvantage of the
present algorithm is the O((N C )2) operations involved in

510

VASILYEV AND PAOLUCCI

TABLE I
Numerical Results Obtained with the Present Algorithm for the Solution of Burgers Equation Using the Correlation Function of
the Daubechies Scaling Function of Order 5 with N 5 1 and b0 5 1.0
L
1
2
3
4
5
6

1
1
1
1
6
8

«

Maximum number of
collocation points

ftmax

Numerical
2(­u/­x)(0, tmax)

max uu 2 u J u

0
1 3 1023
1 3 1023
5 3 1023
5 3 1023
5 3 1023

515
99
115
95
159
515

1.6030
1.6030
1.6035
1.6030
1.6035
1.6050

149.28
149.28
151.90
149.27
149.32
147.15

1.72 3 1023
1.73 3 1023
1.04 3 1024
1.67 3 1023
1.91 3 1023
1.09 3 1022

J
8
8
9
8
3
1

calculations of matrix operators. But even with this disadvantage the present algorithm is very competitive with
wavelet Galerkin algorithms for the solution of nonlinear problems.
Problem III. The thermoacoustic wave problem is
fairly difficult to solve numerically because of the existence
of two very different spatial scales present in the problem.
The first scale is given by the size of the domain, while
the second is associated with the nonlinear wave itself.
Furthermore, for small time a small region of very large
gradients exists close to the left wall.
Let us briefly discuss the evolution of the solution. The
abrupt temperature change at the left wall generates a
pressure wave, which propagates at the local speed of
sound of the medium and gradually, over a long time scale,
damps out because of thermal and viscous diffusion. Once
the wave reaches a wall it reflects and propagates in the
opposite direction. The process of reflection and diffusion
continues until the wave dies out and a quiescent thermal
conduction condition is achieved. For full discussion of this
problem we refer to [16].
The dynamical adaptation of the solution and the irregular grid G $t of wavelet collocation points is illustrated in

x,t

Fig. 8. The results are shown for the dynamically adaptive
multilevel collocation method with the correlation function
of the Daubechies scaling function of order 5 with b0 5
1.0, N 5 1 and threshold parameter « 5 1 3 1023. From
the figure we see that for small time, in order to resolve
the region of sharp gradients, small scale wavelets are
present in the approximation. With the time evolution of
the solution the finest level of resolution gradually decreases. This is caused by the decreasing steepness of the
wave due to heat and viscous diffusion. In addition, the
fine levels of resolution are not present in regions far from
the wave.
In comparison with the first two problems, which are
described by single equations with one dependent variable,
the thermoacoustic wave problem involves four unknowns,
three partial differential equations (continuity, momentum, and energy), and one algebraic relation (equation of
state). Thus the adaptation of the irregular grid G $t of
wavelet collocation points is based on the analysis of coefficients associated with all the dependent variables. The
irregular grid G $t is constructed as a union of irregular
grids corresponding to each dependent variable. Note that
the present algorithm can be easily extended to the case
where each variable is treated on separate computational

TABLE II
Numerical Results Obtained with the Present Algorithm for the Solution of Modified Burgers Equation Using the Correlation
Function of the Daubechies Scaling Function of Order 5 with N 5 1 and b0 5 1.0

1
2
3
4
5
6

L

J

«

Maximum number of
collocation points

Numerical
u­u/­xumax

max uu 2 u J u

1
1
1
1
5
7

7
7
8
7
3
1

0
1 3 1023
1 3 1023
5 3 1023
5 3 1023
5 3 1023

259
94
110
83
103
259

49.86
49.86
50.00
49.92
49.94
49.64

4.31 3 1024
4.95 3 1024
1 61 3 1024
4.27 3 1023
2.12 3 1023
9.48 3 1023

x,t

ADAPTIVE MULTILEVEL WAVELET COLLOCATION METHOD

511

FIG. 8. Evolution of the pressure (left column) and collocation points (right column) for the one-dimensional nonlinear thermoacoustic wave
problem with t0 5 L 5 13000 and A 5 1, using the correlation function of the Daubechies scaling function of order 5.

grids. The mapping from one grid to another can be
achieved via wavelet interpolation. This may be very important for the problems where scales associated with the
different variables are considerably different. In such a
case the computational cost could be reduced substantially.
We also note that examination of the irregular grid gives
information on the structure of the solution. For example,
the irregular grid shown in Fig. 8 indicates the presence
of a boundary layer at the left wall, which is not apparent
in the pressure distribution. The presence of a boundary
layer in density, temperature, and velocity profiles results

in the ultimate computational grid which reflects the presence of the boundary layer at the left wall. Were each
variable solved on a separate grid, the computational grid
for the pressure in the neighborhood of the left wall would
not have collocation points corresponding to the fine levels
of resolution.
In Fig. 7c we show the time evolution of the total number
of collocation points N C. The time interval for which the
computational grid can be kept unchanged is much less
than the time t0 5 L associated with the wave traveling
from one wall to another. Since the results in Fig. 7c are

512

VASILYEV AND PAOLUCCI

FIG. 9. Comparison of solutions at different times for the one-dimensional nonlinear thermoacoustic wave problem with t0 5 L 5 13000 and
A 5 1 using the dynamically adaptive wavelet collocation method (3) and a finite difference method (– – –) [16].

presented on a scale comparable with t0 , it is difficult to
see the fast variations in N C. Nevertheless we observe that
the total number of collocation points gradually decreases,
which is caused by the increase in the finest scale of the
solution due to the thermal and viscous dissipations, and
noticeable decreases in N C are observed at times when the
shock is in the neighborhood of a wall.
In Fig. 9 we present a comparison with the numerical
result obtained by Huang and Bau [16] using a finite difference approximation on a uniform grid. In order to obtain
the results shown in Fig. 9, they use 6000 grid points, while
in our algorithm the number of collocation points did not
exceed 195 at any time. In addition, small oscillations were
observed in their solution at small times due to the unresolved scales associated with the initial large gradients.


## 5. Conclusions


A dynamically adaptive wavelet collocation method
based on a wavelet interpolation technique is developed
for the solution of partial differential equations in a finite
domain. The method is tested on the one-dimensional
Burgers equation, the modified Burgers equation with
small viscosities, and a one-dimensional nonlinear thermoacoustic wave problem. The results indicate that the computational grid and associated wavelets can very efficiently
adapt to the local irregularities of the solution in order to
resolve regions of large gradients. The multilevel approach
is essential for the present algorithm. The method can
handle general boundary conditions. The present algorithm is not only very competitive with adaptive wavelet
Galerkin algorithms, in addition it has distinctive advantages in the treatment of general boundary condition and
nonlinearities.
Future areas of further development include the applica-

tion to two- and three-dimensional domains. This work is
currently underway.
ACKNOWLEDGMENT
The research reported in this paper has been partially supported by
National Science Foundation under Grant No. CTS-9201152 and the
Center of Applied Mathematics of the University of Notre Dame.

REFERENCES
1. O. V. Vasilyev, S. Paolucci, and M. Sen, J. Comput. Phys. 120, 33
(1995).
2. J. Liandrat and P. Tchamitchian, NASA Contractor Report 187480,
ICASE Report 90-83, NASA Langley Research Center, Hampton,
VA 23665-5225, 1990 (unpublished).
3. E. Bacry, S. Mallat, and G. Papanicolau, Math. Model. Numer. Anal.
26, 793 (1992).
4. Y. Maday and J. C. Ravel, C. R. Acad. Sci. Paris 315, 85 (1992).
5. S. Bertoluzza, Y. Maday, and J. Ravel, Comput. Methods Appl. Mech.
Eng. 116, 293 (1994).
6. G. Beylkin, R. Coifman, and V. Rokhlin, Tech. Rep. YALEU/DCS/
RR-696, Yale University, August 1989 (unpublished).
7. G. Beylkin, SIAM J. Numer. Anal. 29(6), 1716 (1992).
8. W. Sweldens and R. Piessens, SIAM J. Numer. Anal. 31, 1240 (1994).
9. Y. Meyer, Ondelettes et opérateurs (Hermann, Paris, 1990).
10. L. Andersson, N. Hall, B. Jawerth, and G. Peters, ‘‘Wavelets on a
Closed Subsets of the Real Line,’’ in Recent Advances in Wavelet
Analysis (Academic Press, San Diego, 1993).
11. G. Beylkin and N. Saito ‘‘Wavelets, Their Autocorrelation Functions,
and Multidimensional Representation of Signals,’’ in Proceedings of
SPIE—The International Society of Optical Engineering, Vol. LB26,
Int. Soc. for Optical Engineering (Bellingham, 1993).
12. IMSL Mathematical Library, Version 1.1, 1989.
13. C. Basdevant, M. Deville, P. Haldenwang, J. M. Lacroix, J. Ouazzani,
R. Peyret, P. Orlandi, and A. T. Patera, Comput. & Fluids 14, 23
(1986).
14. Y. Huang and H. H. Bau, Int. J. Heat Mass Transfer 38, 1329 (1995).
15. Y. Maday and J. C. Ravel, C. R. Acad. Sci. Paris 312, 405 (1991).
16. Y. Huang and H. H. Bau, Int. J. Heat Mass Transfer, to appear.



## Verdict

**Verdict: NO-GO**. — no replication evidence; only PDF text extraction, empty work/ and evidence dirs, no code/results

<!-- census-verdict: NO-GO assigned 2026-07-08 by LLM judge (Argo Opus) -->

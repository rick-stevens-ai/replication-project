# Marker extraction — pdftotext fallback

**Note:** marker-pdf/nougat were not available on the CherryRd host or on
uicgpu (checked with `which marker_single`, `which nougat` — both absent) at
the time of this replication (2026-07-06). The paper text below is the
`pdftotext -layout paper.pdf` extraction, which for this document (LA-4553-MS,
Los Alamos OSTI PDF) is high-fidelity — the OSTI PDF was produced by
ABBYY Recognition Server (see PDF metadata) and yields clean, well-ordered
text. Equations use ASCII-approximate glyphs; the full LaTeX-quality parse
belongs in `nougat.mmd` when the central corpus is regenerated (see stub).

Paper identifiers for the corpus resolver:
- Title: The Direct Solution of the Discrete Poisson Equation on Irregular Regions
- Authors: B. L. Buzbee, F. W. Dorr, J. A. George, G. H. Golub
- Journal: SIAM Journal on Numerical Analysis, Vol. 8, No. 4, Dec. 1971 (also LA-4553-MS Los Alamos technical report, and Stanford Univ. Report CS-71-195)
- DOI: 10.1137/0708066
- OSTI: 4060961
- OA source: https://www.osti.gov/servlets/purl/4060961 (GREEN OA via S2)
- Local PDF: `../paper.pdf`
- PDF SHA-256: `fd92c5ccee14f40c2ed0fd7208f17cfaf079c41a1b9b2bf3f45f2943c5da35b9`
- PDF size: 1,340,222 bytes (31 pages)

---

## Paper text (pdftotext -layout)

```
 LA-4553-MS




                        The Direct Solution of the
                     Discrete Poisson Equation on
                                  Irregular Regions




                                                                                0

 losvyalamos
scientific laboratory
 of the University of California
   LOS ALAMOS, NEW MEXICO 87544

      /        \
                                                         BTSTBIBWION or THIS DOCUMENT IS UNIJMJTKU
                                         UNITED STATES
                                    ATOMIC ENERGY COMMISSION
                                     CONTRACT W-7405-ENG. 36
                            DISCLAIMER

This report was prepared as an account of work sponsored by an
agency of the United States Government. Neither the United States
Government nor any agency thereof, nor any of their employees,
makes any warranty, express or implied, or assumes any legal liability
or responsibility for the accuracy, completeness, or usefulness of any
information, apparatus, product, or process disclosed, or represents
that its use would not infringe privately owned rights. Reference
herein to any specific commercial product, process, or service by
trade name, trademark, manufacturer, or otherwise does not
necessarily constitute or imply its endorsement, recommendation, or
favoring by the United States Government or any agency thereof. The
views and opinions of authors expressed herein do not necessarily
state or reflect those of the United States Government or any agency
thereof.




                          D IS C L A IM E R

Portions of this document may be illegible in electronic image
products. Images are produced from the best available
original document.
   This report was prepared as an account of work sponsored by the United
States Government. Neither the United States nor the United States Atomic
Energy Commission, nor any of their employees, nor any of their contrac­
tors, subcontractors, or their employees, makes any warranty, express or im­
plied, or assumes any legal liability or responsibility for the accuracy, com­
pleteness or usefulness of any information, apparatus, product or process dis­
closed, or represents that its use would not infringe privately owned rights.




This report expresses the opinions of the author or authors and does not nec­
essarily reflect the opinions or views of the Los Alamos Scientific Laboratory.




       Printed in the United States of America. Available from
                 National Technical Information Service
                    U. S. Department of Commerce
                         6285 Port Royal Road
                      Springfield, Virginia 22151
             Price: Printed Copy $3.00; Microfiche $0.95                          ^
                                                                                                   LA-4553-MS
                                                                                                   UC-32
                                                                                                   ISSUED: May 1971




   losvValamos
 scientific laboratory
   of the University of California
      LOS ALAMOS, NEW MEXICO 87544

          /        \
                                                      This report was prepared as an account of work
                                                      sponsored by the United States Government. Neither
                                                      the United States nor the United States Atomic Energy
                                                      Commission, nor any of their employees, nor any of
                                                      their contractors, subcontractors, or their employees,
                                                      makes any warranty, express or implied, or assumes any
                                                      legal liability or responsibility for the accuracy, com­
                                                      pleteness or usefulness of any information, apparatus,
                                                      product or process disclosed, or represents that its use
                                                      would not infringe privately owned rights.




                               The Direct Solution of the
                            Discrete                                                               on
                                        Irregular Regions*

                                                             by

                                                      B. L. Buzbee
                                                       F. W. Dorr
                                                      A. George**
                                                     G. H. Golub**




                                   *Also issued as Stanford University Report CS-71-195.




*‘Present address: Stanford University. The work of these authors was supported by the Office of Naval Research
  under grant No. N 0013-67-A-00112-0029, and by the Atomic Energy Commission under grant No. AT(04-3)326,
  PA-30.
                                                                    OTSTRTBTWION OF THIS DOCUMENT IS UNUMI
                            Abstract



    There are several very fast direct methods which can be used to

solve the discrete Poisson equation on rectangular domains.   We show that

these methods can also be used to treat problems on irregular regions.




                                ii
1.   Introduction.      Within the past few years, several very fast and accurate

direct methods have been developed for solving finite difference approximations

to the Poisson equation,


              Au = f      in   R ,

               u = g      on   SR .


These methods can usually be applied only on rectangular regions, although the

differential operator and boundary conditions can be more general than those in

the Poisson equation.     In this paper, we will show how these algorithms for

rectangular domains can also be used effectively on irregular regions.               The

approach used is similar to that employed by Hockney [16, 17], Buneman [7]^

and George [l4].     We also mention the work of Angel [1-4], Angel and Kalaba [5],

Collins and Angel [9], Kalaba [20], and Roache [22] on the use of direct methods

for problems in irregular regions.

     We will not discuss the details of any specific direct method.               A survey

of these procedures is given in [11], and in particular we cite the recent work

of Buneman [6], Buzbee, Golub, and Nielson [8], and Hockney [16].

     We will also not consider the derivation of the finite difference equations

that approximate the partial differential equation.             This subject is treated in

detail by Forsythe and Wasow [13], and we assume that the problem has been

reduced to finding the solution of a matrix equation             Ax = y .    The matrix    A

is frequently very large and sparse, but its structure does not permit the

application of the most efficient direct methods.             For our computational procedure,

we alter certain rows of       A   to obtain’a matrix       B , and we will show how to

define a modified right-hand side         z       so that the solution   x   also satisfies the

equation   Bx = z .    The matrix     B   is chosen so that these equations can be

solved by the direct methods.



                                              1
     This method is computationally advantageous -when we are solving a

sequence of equations   Ax^ =      .   This situation frequently arises in

time-dependent partial differential equations, in nonlinear problems, and in

linear problems where the right-hand side is varied but the region and

differential operator remain the same.      After some initial computation, each

solution      can be obtained in approximately twice the time required for

the solution of an equation     Bx = z .

     In Sections 2 and 3 we derive this algorithm in a general form.     We

describe a number of applications of the method in Sections U and 5> and in

Section 6 we present some computational results.




                                        2
2.   Method of Solution if det B ^ 0 . Suppose that we are given an n by n

matrix A and an integer p with 1 £ p s n .           We wish to modify p rows of A

to obtain another matrix B .    Without loss of generality we assume that the

first p rows of A are to be changed, since we can achieve this situation

by multiplying A by a suitable permutation matrix.         However, we emphasize

that this multiplication should not be done explicitly in the computational

procedure.    Rather, the rearrangement of rows should be done implicitly by

indexing.    The direct methods mentioned later in the paper require that B

has a particular structure, which could be altered by the permutation

transformation.

      Partition A in the form



                                A =              f



where        is a p by n matrix and           is an (n - p) by n matrix.   We then

write


                                        B,
                                B =              )



where B^ is a p by n matrix.          For the remainder of this section, we

assume that det B / 0 .
        Suppose we are given a linear equation Ax = y .      We partition y in

the same way as A, and write


                                         yl
                                y=
                                         £2


                                         3
Let y be any vector of the form


                                            h

                                            12


If W is an arbitrary nonsingular p by p matrix, we define an n by p

matrix W by


                                            W

                                             0


     Define the p by p matrix C by


                                   C


Following Hockney [l6], we call C the capacitance matrixr Assume that there

exists a p by 1 vector p that is a solution to the equation


                              C0 = y      - A B"1 y                                   (1)


Since   A    and   B   differ only in the first       p   rows, it is easy to verify that

a solution    x    to the equation     Ax = y      is given by


                               x = B"1 (y + VP)


We first show that this method of obtaining the solution x will be valid

whenever the original system Ax = y is consistent.

Theorem.     If det B ^ 0 , then


                                       (det A) (;let w)
                                           det B

¥ Hockney actually refers to C ^ as the capacitance matrix. Since C may
   be singular in our development, we have adopted the present notation.

                                            b
If the system Ax * y is consistent, then Eg. (l               is also consistent.
Proof.    Partition B_1 in the form


                              B   M1*!           "a) ’
where       is n hy p and           is n by (n - p) .        It then follows that



                   BB"1 =
                             B1D1         BlV            1
                             A2D1         A2D2           °


and



                       -1
                            Vl           ^2
                  AB
                            Vl           A2B2
Thus we have

                            C = A1B“1W = A1D1W           ,


and so


                            det C = det (A^ D^) det W

                                    = det (A B"1) det W

                                        (det A) (detW)
                                    =        det B


        To prove the consistency statement, suppose CT r = 0 .           Write




                                           5
and define an n t>y 1 vector y by



                            r



We then have




Since the system Ax = y is assumed to be consistent, we therefore have
 T                                 T
Ml y = 0 , which is the same as rv
   /vs
                                 y (y,
                                     *+±
                                         - X rsj*Cl
                                             y0) = 0 . But then



               JCT(Z1 - AiB"1z) “ XT(Zi -            - *1X2)




                                  = 0    ,


which is the consistency condition for Eq. (l).

     The Woodbury formula [l8, pp. 123 -124] for the inverse of a matrix

(B + F G) is


               B + FG           (i - p (:I + GB -1


This equation has been used in direct methods for solving the Poisson equation
by George [1*0 , and for the biharmonic equation by Golub [15].   If A is non­

singular we write


                             A = B + FG       ,

                                     6
vhere F = W , and G is the p hy n matrix given by

                             G = W1                 .


For the case in which A is nonsingular, the algorithm we have derived is
equivalent to using the Woodbury formula for A-1.

     Suppose that we have a very efficient method for solving equations of

the form Bz = w .      The solution of the equation Ax = y then proceeds in
the following steps:
     (1)   Compute C = A1B-1W        ,
     (2)   Compute x = B~^y    ,

     (3)   Solve the equation C p = y. - A_ x

The solution x can then be obtained from the formula


                              x = B’1 (y + Wp)          .                                 (2)


If it is possible to store the vector x and the matrix B = B”1^ , then x

can also be coniputed from


                                   x = x + Bp   .                                         (3)


The decision whether to use Eq. (2) or Eq. (3) would be made on consideration

of storage requirements, and on the relative speed of solving the system in

Eq. (2) versus multiplying by the matrix in Eq. (3).             For problems arising

from elliptic difference equations, it is frequently better to use Eq. (2)
because B has a band structure, but the matrix B may be full.

     The type of application we have in mind for this method is one in which
we have to solve a number of equations Ax. = y              .   In this case, we compute

the capacitance matrix and factor it as part of a preprocessing stage.              The

solution of each equation Ax. = y. is then approximately as fast as the time


                                         7
it takes to solve two equations B z = w .

     To be specific, let e(n) denote the number of arithmetic operations

necessary to solve a system B z = w .     Then to compute C and form its LU

decomposition in a preprocessing stage requires approximately


                                    2       5
                         p9(n) + k^p n + k2p^


operations (cf. [19, Sec. 2.l]).    In many cases the matrix    is sparse,

and this estimate is

                                pe(n) + k3p3                                   (4)


operations.   To compute the solution to a particular equation Ax = y using

Eq. (2) takes an additional
                                                   p
                           2 9(n) + kj^pn + k^ p


operations.   If A1 is sparse and we let W = I , this estimate can be replaced

by

                                2 0(n) + kgp2                                  (5)


operations.   To compute a particular solution using Eq. (3) requires

                                                  2
                              e(n) + k^pn + kgP                                (6)




operations.   In general this estimate cannot be reduced, because the matrix

B may be full.




                                      8
5-     Method of Solution if                 rank(B) = n-1 .              The method derived in Section 2

gives a procedure for finding a                     p    by     1   vector     &       such that a solution            x

to    Ax = y        also satisfies the equation



                                Bx = y +



If    B       is singular, it may not be possible to find such a vector                              6 .     To show
                           T
this, suppose             B v = 0      but     v ^ 0 .        In order for         5   to exist, we must

satisfy the consistency condition


                                 vT(y + ^       ^ ei) = 0           .                                        (7)
                                         i=l

       T                                                 T
If    v e^ = 0            for    1 < i < p      and     v y / 0 , it is not possible to satisfy

Eq. (7)•        However, if         A    is nonsingular this difficulty does not arise,
                                                                          T                   T
because then the only vector                    v     satisfying         B v = 0       and   v e^ = 0      for

l<i<p               is     v = 0.

       We will now describe an algorithm we have used when                                   rank(B) = n-1       and

A     is nonsingular.             There are two advantages in treating this particular case.

First, the construction is quite simple, and it is easy to see how the method

could be extended to a more general matrix                              B .   Second, the case          rank(B) = n-1

has a special significance in the solution of partial differential equations,

because this condition is satisfied by the matrix corresponding to the

Neumann problem.                For simplicity, we assume that the matrix                      W   of Section 2

is the identity matrix.


Theorem 2.               Assume that     A     is nonsingular and             rank(B) = n-1 , and let              u
                                                                              T
and       v   be two non-zero vectors satisfying                        Bu = B v = 0 .        Then there exists an
                                                                 T
integer         k   with        1 < k < p      such that        v e^ / 0 .      Define a constant



                                                         9
                           a         (ffk) -l            >

and let    x    be a solution to


                           Bx = y - (a vT y) ek                               .


For   1 < i < P       and       i / k             let                Be               solution to


                           B3l =                                                      ’


and let         = u .          Let       C        be the             p       by       p    matrix whose               i-th    column is

the vector         7|^ .       Then          C     is non singular, and, if                                  ft   is the solution to


                           CP = yi - A1 x                        ,


the solution      x     to     Ax = y              is given by


                                     P
                           ■ x = x + £                  Pi %             •
                           ~         ~           i^l


Proof.     If we partition                   v     in the same way as                            y , we have
 T     T       T                                  T          T             T                                         T
A v = A1 v1 + A2 v2             and              B v =               v^ + A2 v2 .                    Thus if        B v = 0    and
                                    T
v^ = 0    we would have            A v = 0 .                 Since                A       is nonsingular and               v / 0     this

cannot happen, and hence                          / 0 .

      To prove that            C     is nonsingular, we show that                                            Cp = 0      implies   p = 0 .
                                                                                                                             P
Suppose     p    is an arbitrary vector such that                                           Cp = 0                Then   x = kPi

satisfies       Ax = 0 , and hence                      x = 0 .               This implies that                       Bx = 0 , or



                                                                                            e.
                                                                                                 )   e
                                                                                                         k    ’




                                                                     10
Thus          = 0   for     1 < i < p      and       i / k , and the condition      x = 0   then

implies that              = 0 .     Thus   p = 0 , and so        C     is nonsingular.


Remark.       As we discussed in Section 2, the computation proceeds in the following

steps:

        (1)   Compute (and factor)          C ,

        (2)   Compute       x ,

        (3)    Solve for      p .

The solution        x     can then he obtained from the formula




However, if the problem arises from a partial differential equation, it is more

efficient computationally to obtain                    x    in the form

                              x = x + p u        ,

where     x    is a solution to



                                                                 i=l
                                                                 i/k

and



                                                 i=l




                                                       11
4. Applications to Partial Differential Equations by Imbedding.           Suppose we

are given a two-dimensional bounded region R in the x - y plane, and we wish

to find a solution u to the Poisson equation,

                               Au=f           inR      ,1

                                u = g         on SR    .1


We assume that this differential equation is approximated by a finite differ­

ence equation (cf. Forsythe and Wasow Llj]).           Thus we have a finite set of
unknowns {Ik | 1 £ i s nQ } which approximate the solution u at the grid

points.   If we denote by         a finite difference approximation to the Laplacian

operator A, by R^ the discrete interior of the grid, and by S R^ the discrete

boundary of the grid, then the discrete Poisson equation can be written in the

form


                            Ahu=f            in Rh
                                                                                      (8)
                               U = g         on SR^


       Let R, be a discrete rectangular region such that R^ c R^ and

S R^ c R^ U S R^ , and let        = S R^ n       .    Extend the functions f and g
to the regions R^ and SR^ U Sr^ respectively, and consider the equation


                       V =f             in ^ - Sh           '
                                                                                       (9)
                          U = g         on       u          .


We will solve Eq. (9), and the solution U will then also satisfy Eq. (8).

       Equation (9) is a linear equation in the unknowns {U^Jlii^n).
Observe that we may have increased the number of unknowns by the imbedding

process, so that   iu. * n .   We write Eq. (9) as a matrix equation AU = V ,


                                         12
and the matrix A can frequently be chosen to be block tridiagonal with

tridiagonal matrices as the non-zero blocks (cf. [13]).

        Let p be the number of grid points in            .   We modify the p rows of

A and V corresponding to the equations


                             U = g     on Sh         ’


and replace them with the equations


                            v=              on S,


This defines a new matrix B and a new right-hand side V .             An equation
BU = V corresponds to the difference equation


                                       in
                          V=f                K
                                                                                       (10)
                             U » g     on d


Since       is a rectangular region, we have very fast methods for solving

Eq. (10). We can now apply the method of Section 2 to solve the equation

AU = V by using the modified matrix B .

     To illustrate this construction, let R be a rectangular region with

an interior rectangle removed, such as that shown in Figure 1.            For simplic­

ity, we assume that the discrete boundary dR.            is a subset of dR.    The

imbedding rectangle is ^       ^ U     U T^ .       The only function extension re­

quired for this example is that f be defined (arbitrarily) in S^ U T^ .

To define this extension, we can set f = 0 in S^ U T^ , or we can define f

so that it is continuous in all of R^ .      The advantage of using a continuous

f is that the solution to Eq. (10) is then smooth.            However, the direct

methods used to solve Eq. (10) are so accurate that the smoothness of the

solution does not appear to influence the computational results.            Therefore,

                                       13
in the examples we have considered, we extend f hy setting f - 0 in

shu Tn •
     If we let W = I in the method of Section 2, this algorithm is closely-

connected with the discrete Green’s function for the region            (cf. [13,

pp. 31^-33j8]).   In fact, the method is then equivalent to adding suitable

multiples of the discrete Green’s function for the points on               so that

the boundary conditions on         will be satisfied.   Since we have Dirichlet

boundary conditions on       , by a proper ordering of the unknowns we can write


                                  A1 = (I     0)   .


Since B is positive definite and

                         C = (I       0) B"1 ^ I




we see that C is also positive definite in this case.          This is advantageous

because Cholesky decomposition can then be used to compute an LLT decomposi­

tion of C (cf. [12, Chap. 233).
     If the grid on       has N points on a side, we have n =          .    In that

case, we can solve the system BU = V        in approximately

                              e(N) = 5N2 loggN


operations (cf. [ll, p. 26o3).      The preprocessing then takes


                             5pN2log2N + k3p3


operations (cf. Eq. (4)).    To solve Eq. (8) for a particular choice of f

and g by using Eq. (2) with W = I takes an additional
                                  10 N2 log2 N + k6 P2



operations (cf. Eq. (5)).         If we use Eq. (3) to compute the solution, it

takes an additional


                            5 N2 log2 N +         p N2 + kg p2



operations (cf. Eq. (6)).         Thus if p » loggN          it is faster to use Eq. (2)

to compute the solution.      We also observe that for this problem the matrix

B-   is full [23, p. 85], so to store B in using Eq. (3) would require pN

locations.   Thus for large values of p and N it is both faster and more

economical in terms of storage to use Eq. (2) to compute the solution to a

particular equation.

     It should be clear that the imbedding procedure can be applied to other

elliptic difference operators with other types of boundary conditions.                 To

be a practical procedure, we simply require that we have a fast method for

solving the imbedded problem in the rectangular region.

     As another example, consider the region shown in Figure 2.                This problem

arises in the time-dependent study of a rotating fluid [10], and the fluid surface

is moving slowly.   We are given Dirichlet boundary data on                   , and Neumann

boundary data on    cS^ -     .    The imbedding rectangle is                   U   U T^ , and

we use Neumann boundary conditions on             8r^ .    Thus   B   corresponds to the Neumann

problem on   R^ , and the rank of        B    is n - 1 .     The method of Section 3 can then

be applied, and direct methods for solving the rectangular Neumann problem are

given in [8].

     For an example with the Poisson operator in another geometry, consider

the region in the    z -r   plane shown in Figure 3•              This problem arises in the




                                             15
time-dependent study of a plasma [21], and a Poisson equation must be solved

at each time step.    The boundary conditions are Dirichlet on        and Neumann

on         .   We use Neumann boundary conditions on          and-            and
Dirichlet boundary conditions on     dR^^    and   dR/^   for the imbedding

region   R^ = R^ U     U T^ .   The elliptic difference equation in   R^   is solved

by the method of matrix decomposition [8].




                                       16
5.   Applications to Partial Differential Equations by Splitting.           There are

many problems for which the imbedding approach is not an economical algorithm.

For example, imbedding the region in a rectangle may introduce an excessively

large number of additional unknowns that are not necessary to the solution of

the original problem.   Another instance is one in which the differential oper­

ator or the mesh size changes in different parts of the region.             In this

section, we give two such examples.     In each case, the method of Section 2

can be used to split the problem into two rectangular problems, which can be

solved by the usual, direct methods.

      Consider the elongated L-shaped region in Figure 4, and the equation


                          V =f              in Rh        ’

                             U = g          on 51^       .



We assume that points on the line marked             are all grid points.     To define

the matrix B , we replace the equations



                              V =f             on Th
by the equations


                             U = g          on T^    ,



where g has been (arbitrarily) extended to T^ .              The solution of an equation

BU = V now consists of solving the two rectangular problems


                         V. =f         in                -

                           Ui = g      on                ,


for i = 1 , 2 . We can then apply the method of Section 2 to solve the original


                                       17
problem.    This algorithm is similar to one developed in [ 8, Sec. 9] for

non-rectangular regions.

      As another example, consider the multiple-material problem shown in
Figure 5.    The differential equation is


                 A (o(x) I7)+             (T(y) I7) = f(x>y) >

and

                                r a1(x)        in R(l)     ,
                       a(x) =   j
                                ( a2(x)        in IT2'     .


The functions o-^Cx), c2(x), and T(y) are assumed to be smooth .           Dirichlet

data is given on 5 R , and we require that a             be continuous across the
boundary between R^ and R^ .           The computational procedure is essentially

the same as that for the L-shaped region.       The only difference is that in
forming the matrix B we replace the equations for the continuity of

across the line T^ by the equations


                              U = g        on T^


As before, the equation BU = V        corresponds to the two rectangular problems

                     Su.
           Tx (ai(x) Tt\) + Ty
                             ^ (T(y)
                               /     Su.
                                     T t) = ^ y)                   in
                                                                        R (i)


                                       ui (x , y) = g(x , y)       on SR (i)


for i = 1 , 2 . These problems can be solved directly by the method of matrix

decomposition [ 8, Sec. 83.     A similar method can be used for the case in

which r(y) is only piecewise smooth.

                                          18
     It is clear that this splitting method can be applied to the Poisson

equation in regions such as that in Figure 5 when different mesh sizes are
used in       and R^ .    The method developed in [ 8 , Sec. 8] can also be

adapted to include rectangular problems with irregular meshes.




                                   19
6.   Computational Results.      In Table 1 we have tabulated some computational

results for two regions of the form of Figure 1.         In each case, a square

with sides of length 1 has a symmetrically located square removed from its

center.     For region 1 the inner square has sides of length -g-, and for

region 2 the inner sides are of length         .    We solve the Poisson equation
                                                                       2          2
with Dirichlet boundary conditions for the function u(x , y) = x            + y       .

This function was selected because there is no truncation error, and all of

the measured error is due to inaccuracies in the solution of the difference

equations.      All of the computations were performed on a CDC 6600 computer.

        The iterative methods used are:

        SOR :   point successive overrelaxation [23, p. 58^

        SLOR:   successive line overrelaxation [23, p. 8ol,

        ADI :   Peaceman-Rachford alternating direction implicit iteration

                [2tj Chap. 6],

The iteration parameters used are those for the imbedding rectangle                   , and

for ADI the parameters for cycles of length four axe calculated by the

Wachspress algorithm [2bf Chap. 6],       The initial guess is identically zero,

and the iterations axe terminated when the maximum difference between iterates
                     -5
is less than 10           .

        The direct method used is variant one of the Buneman algorithm [8 ^ Sec. ll].

Preprocessing times are given in Table 2.          Computational results for a similar

problem axe given in [1*0.

        The problem described in Section 4 for the region in Figure 2 has been

treated by Daly and Nichols [10].      The mesh used has     23X 40 = 920    points.

Using the direct method of matrix decomposition, a particular solution requires

about     30 - 50$   of the time required for a point Gauss-Seidel iterative procedure.




                                         20
     The problem discussed in Section 4 for the region in Figure 3 has been

treated by Morse and Rudsinski [21],     The mesh used has 52 x 98 = 5096

points, and the preprocessing time is approximately 150 seconds.     The region

and differential operator are very seldom changed, so the factored capacitance

matrix is stored on magnetic tape.     Thus there is essentially no preprocessing

time for the execution of the program.      To solve for a particular solution

requires about 2 seconds, -which is approximately 4o$ of the time required for

a successive line overrelaxation iterative procedure.




                                       21
Table 1.   Computational results for solving the discrete Poisson equation^




Region      h      p      Method      Maximum       Computation       Scaled
                                       Error        Time (Sec.)     Computation
                                                                       Time

                          SOR        5.02 (-6)         3.586          21.866
             1
                   16     SLOR       7.63 (- 6)        2.654          16.183
            32
                          ADI        2.36 (-6)         1.128           6.878

                          Direct     4.44 (-13)        0.164           1.000
  1

                          SOR        8.12 (-6)        29.388          43.994
            1                                         21.424
                   32     SLOR       7.95 (-6)                        32.072
                          ADI        3.41 (-6)         5.642           8.446
                          Direct     1.90 (-12)        0.668           1.000

                          SOR        2.35 (-6)         3.570          21.250
             i
                  32      SLOR       6.48 (-6)         2.558          15.226
            32
                          ADI        2.11 (-6)         0.870           5.179
                          Direct     3.77 (-13)        0.168           1.000
  2

                          SOR        2.02 (-6)        29.624          43.565
            1      64     SLOR       9.96 (-6)        20.510          30.162
           3T
                          ADI        3.57 (-6)         5.332           7.841
                          Direct     1.54 (-12)        0.680           1.000




                                     22
Table 2.   Preprocessing time for the direct method results in Table 1




                 Region           h           Preprocessing
                                               Time (Sec.)
                                   1              1.062
                                  32
                    1
                                  1               8.670
                                 ST

                                   1              2.188
                                  32
                    2
                                   1             17.698
                                  3T




                                       23
                      dR,




                                        o< 1)
                                        R.




 Figure 1.   Region in the x-y plane.




 Figure 3.   Region in the z-r plane.




2h
References


[1]    E. Angel, "Discrete invariant imbedding and elliptic boundary-value problems
       over irregular regions," J. Math. Anal. Appl., 23 (1968), pp. 4-71-484.

[2]    E. Angel, "Dynamic programming and linear partial differential equations,"
       J. Math. Anal. Appl., 23 (1968), pp. 628-638.

[3]    E. Angel, "A building block technique for elliptic boundary-value problems
       over irregular regions," J. Math. Anal. Appl., 26 (1969), PP- 75-81.

[4]    E.. Angel, "Inverse boundary-value problems:    elliptic equations," J. Math.
       Anal. Appl., 30 (1970), pp. 86-98.

[5]    E. Angel and R. Kalaba, "A one sweep numerical method for vector-matrix
       difference equations with two-point boundary conditions," Report 70-16,
       Department of Electrical Engineering, University of Southern California,
       Los Angeles, 1970.

[6]    0. Buneman, "A compact non-iterative Poisson solver," Report SUIFR-294,
       Institute for Plasma Research, Stanford University, Stanford, California,
       1969.

 [7]   0. Buneman, "Computer simulation of the satellite photosheath,"
       Report ESRIN-92, European Space Research Institute, Rome, 1970.

 [8]   B. L. Buzbee, G. H. Golub, and C. W. Nielson, "On direct methods for
       solving Poisson’s equations," SIAM J. Numer. Anal., to appear.

 [9]   D. C. Collins and E. Angel, "The diagonal decomposition technique applied
       to the dynamic programming solution of elliptic partial differential
       equations," J. Math. Anal. Appl., to appear.

[10]   B. Daly and B. Nichols,   Los Alamos Scientific Laboratory, Los Alamos,
       New Mexico, personal communication, November 1970*

[11]   F. ¥. Dorr, "The direct solution of the discrete Poisson equation on a
       rectangle," SIAM Rev., 12 (1970), pp. 248-263.

[12]   G. E. Forsythe and C. B. Moler, Computer Solution of Linear Algebraic
       Systems, Prentice-Hall, Englewood Cliffs, New Jersey, 1967.

                                        25
[13]   G. E. Forsythe and W. R. Wasow, Finite-Difference Methods for Partial
       Differential Equations, Wiley, New York, i960.

[14]   J. A. George, "The use of direct methods for the solution of the discrete
       Poisson equation on non-rectangular regions," Report STAN-CS-70-159^
       Computer Science Department, Stanford University, Stanford, California, 1970.

[15]   G. H. Golub, "An algorithm for the discrete biharmonic equation,"
       unpublished, 1970•

[16]   R. W. Hockney, "The potential calculation and some applications,"
       Methods in Computational Physics, 9 (1970), pp. 135-211.

[17]   R. W. Hockney, "P0T4 - a fast direct Poisson-solver for the rectangle
       allowing some mixed boundary conditions and internal electrodes,"
       to appear.

[18]   A. S. Householder, The Theory of Matrices in Numerical Analysis, Blaisdell,
       New York, 1964.

[19]   E. Isaacson and H. B. Keller, Analysis of Numerical Methods, Wiley,
       New York, 1966.

[20]   R. Kalaba, "A one sweep method for linear difference equations with two
       point boundary conditions," Report 69-23, Department of Electrical
       Engineering, University of Southern California, Los Angeles, 1969.

[21]   R. L. Morse and L. Rudsinski, Los Alamos Scientific Laboratory, Los Alamos,
       New Mexico, personal communication, August 1970.

[22]   P. J. Roache, "A direct method for the discretized Poisson equation,"
       Report SC-RR-70-579> Sandia Laboratories, Albuquerque, New Mexico, 1970.

[23]   R. S. Varga, Matrix Iterative Analysis, Prentice-Hall, Englewood Cliffs,
       New Jersey, 1962.

[24]   E. L. Wachspress, Iterative Solution of Elliptic Systems, Prentice-Hall,
       Englewood Cliffs, New Jersey, 1966.




                                        26                        CMs 297 (40)
```
